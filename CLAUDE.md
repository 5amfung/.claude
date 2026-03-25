## Workflow Orchestration

0. **Git Worktrees**
    - Before creating a worktree or branch, ask the user for a meaningful name.
    - Format: `claude-short-description`.
    - Never auto-generate branch names without confirmation.
1. **Plan Mode Default**
    - Use `superpower:brainstorm` skill (if available) or plan mode for ANY non-trivial task (3+ steps or architectural decisions)
    - If something goes sideways, STOP and re-plan immediately – don't keep pushing
    - Use plan mode for verification steps, not just building
    - Write detailed specs upfront to reduce ambiguity
2. **Subagent Strategy**
    - Use subagents liberally to keep main context window clean
    - Offload research, exploration, and parallel analysis to subagents
    - For complex problems, throw more compute at it via subagents
    - One track per subagent for focused execution
3. **Self-Improvement Loop**
    - After ANY correction from the user, write rules for yourself that prevent the same mistake
    - **Capture Lessons**: Update auto memory after corrections
    - Ruthlessly iterate on these lessons until mistake rate drops
    - Review lessons at session start for relevant project
4. **Verification Before Done**
    - Never mark a task complete without proving it works
    - Diff behavior between main and your changes when relevant
    - Ask yourself: "Would a staff engineer approve this?"
    - Run tests, check logs, demonstrate correctness
5. **Demand Elegance (Balanced)**
    - For non-trivial changes: pause and ask "is there a more elegant way?"
    - If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
    - Skip this for simple, obvious fixes – don't over-engineer
    - Challenge your own work before presenting it
6. **Autonomous Bug Fixing**
    - When given a bug report: just fix it. Don't ask for hand-holding
    - Point at logs, errors, failing tests – then resolve them
    - Zero context switching required from the user
    - Go fix failing CI tests without being told how

## Core Principles

- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary, hacky fixes. Don't just patch things up.
- **Minimal Impact**: Changes should only touch what's necessary. Avoid introducing bugs.
- **Write Clean Code**: Follow Clean Code guideline.

## Command Execution Rules

- **Always run from the project root.** Never `cd` into subdirectories.
- **Be consistent.** Use the same CLI tool and invocation pattern every time. Never mix `npx`/`pnpm exec`/direct paths for the same tool.
- **Pre-approve CLIs**: Before executing a multi-step task, identify **all** CLI tools needed (`pnpm`, `git`, `node`, `find`, `python3`, etc.) and run a benign command for each (e.g., `--version`) to trigger permission approval upfront. Avoids and minimizes interruptions mid-task.
- **Subagents follow the same rules.** Include these rules in subagent prompts.
- **Use rg (ripgrep) over grep command** for performance gain.