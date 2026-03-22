#!/usr/bin/env python3
"""
Claude Code Hook: Auto-Approve Safe Bash Commands
===================================================
This hook runs as a PermissionRequest hook for the Bash tool.
It auto-approves commands composed entirely of known-safe CLI tools,
including piped and chained commands that would otherwise trigger
repeated permission prompts.

If any sub-command is not in the safe list, the hook exits silently
and the normal permission prompt is shown.

Read more about hooks here: https://docs.anthropic.com/en/docs/claude-code/hooks

Configuration (add to ~/.claude/settings.json):
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/auto-approve-safe-commands.py"
          }
        ]
      }
    ]
  }
}
"""

import json
import re
import shlex
import sys

# Tools considered safe for auto-approval.
# Excludes command launchers (xargs, env, node, npx, bun, bunx, awk)
# because they can execute arbitrary commands via arguments.
_SAFE_COMMANDS = frozenset({
    # Package managers (run scripts from package.json — acceptable in trusted projects).
    "pnpm",
    "npm",
    # Dev tools.
    "vite",
    "tsc",
    "vitest",
    "playwright",
    "prettier",
    "eslint",
    # Standard Unix utilities (read-only or output-only).
    "basename",
    "cat",
    "column",
    "comm",
    "cut",
    "date",
    "diff",
    "dirname",
    "echo",
    "false",
    "grep",
    "head",
    "jq",
    "less",
    "ls",
    "printf",
    "readlink",
    "realpath",
    "rg",
    "sort",
    "tail",
    "test",
    "tr",
    "true",
    "uniq",
    "wc",
    "which",
    # Git and GitHub CLI.
    "git",
    "gh",
    # File inspection.
    "file",
    "stat",
})

# Patterns that are never safe, regardless of the command prefix.
_DANGEROUS_PATTERNS = [
    re.compile(r"\brm\s+-(r|rf|fr)\b"),
    re.compile(r"\brm\s+-[a-z]*r"),
    re.compile(r"\bdrop\s+table\b", re.IGNORECASE),
    re.compile(r"\bsudo\b"),
    re.compile(r"\bchmod\s+777\b"),
    re.compile(r"\bcurl\b"),
    re.compile(r"\bwget\b"),
    re.compile(r"\bnc\b"),
    re.compile(r"\bdd\b"),
    re.compile(r"\bmkfs\b"),
    re.compile(r"\btruncate\b"),
    re.compile(r"\bshred\b"),
    re.compile(r"\bpkill\b"),
    re.compile(r"\bkillall\b"),
    re.compile(r"\bmv\b.*\b/dev/null\b"),
    # Dangerous subcommands for tools in the safe list.
    re.compile(r"\bsed\s+(-i|--in-place)\b"),
    re.compile(r"\bfind\b.*\s-(exec|execdir|delete)\b"),
    re.compile(r"\bgit\s+(filter-branch|!)\b"),
    re.compile(r"\bgit\s+config\s+.*alias\b"),
    re.compile(r"\bgit\s+push\s+.*--force\b"),
    re.compile(r"\bgit\s+reset\s+--hard\b"),
]

# Patterns that indicate shell substitution or indirect execution.
_SHELL_SUBSTITUTION_PATTERNS = [
    re.compile(r"`[^`]+`"),           # Backtick command substitution.
    re.compile(r"\$\([^)]+\)"),       # $() command substitution.
    re.compile(r"<\([^)]+\)"),        # <() process substitution.
    re.compile(r">\([^)]+\)"),        # >() process substitution.
]


def _has_dangerous_pattern(command: str) -> bool:
    """Check the full command string for known dangerous patterns."""
    for pattern in _DANGEROUS_PATTERNS:
        if pattern.search(command):
            return True
    return False


def _has_shell_substitution(command: str) -> bool:
    """Reject commands containing shell substitution that could hide payloads."""
    for pattern in _SHELL_SUBSTITUTION_PATTERNS:
        if pattern.search(command):
            return True
    return False


def _strip_env_vars_and_redirects(part: str) -> str:
    """Remove leading env var assignments (FOO=bar) and trailing redirects."""
    # Strip inline env vars like DEBUG=1 or FOO="bar".
    part = re.sub(r"^(\s*\w+=\S*\s*)+", "", part)
    # Strip redirections like 2>&1, >/dev/null, 2>/dev/null.
    part = re.sub(r"\d*>&?\d+", "", part)
    part = re.sub(r"[<>]+\s*/dev/null", "", part)
    return part.strip()


def _extract_first_word(part: str) -> str:
    """Extract the command name from a shell fragment."""
    cleaned = _strip_env_vars_and_redirects(part)
    if not cleaned:
        return ""
    # Use shlex to handle quoting, fall back to simple split.
    try:
        tokens = shlex.split(cleaned)
    except ValueError:
        tokens = cleaned.split()
    if not tokens:
        return ""
    first_word = tokens[0]
    # Strip subshell prefix $( using proper prefix removal, not lstrip.
    if first_word.startswith("$("):
        first_word = first_word[2:]
    elif first_word.startswith("("):
        first_word = first_word[1:]
    return first_word


def _is_safe_command(command: str) -> bool:
    """Return True if every sub-command in a compound command is safe."""
    if _has_dangerous_pattern(command):
        return False

    # Reject any form of shell substitution — regex cannot parse these safely.
    if _has_shell_substitution(command):
        return False

    # Split on shell operators while preserving sub-commands.
    # Handles: &&, ||, ;, | (but not ||= or &&=).
    parts = re.split(r"\s*(?:\|\||&&|[;|])\s*", command)

    for part in parts:
        part = part.strip()
        if not part:
            continue

        first_word = _extract_first_word(part)
        if not first_word:
            continue

        if first_word not in _SAFE_COMMANDS:
            return False

    return True


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    tool_name = input_data.get("tool_name", "")
    if tool_name != "Bash":
        # Not a Bash command — let the normal prompt handle it.
        sys.exit(0)

    tool_input = input_data.get("tool_input", {})
    command = tool_input.get("command", "")

    if not command:
        sys.exit(0)

    if _is_safe_command(command):
        # Auto-approve: output the PermissionRequest allow decision.
        result = {
            "hookSpecificOutput": {
                "hookEventName": "PermissionRequest",
                "decision": {
                    "behavior": "allow",
                },
            },
        }
        json.dump(result, sys.stdout)
        sys.exit(0)

    # Not safe — exit silently to show the normal permission prompt.
    sys.exit(0)


if __name__ == "__main__":
    main()
