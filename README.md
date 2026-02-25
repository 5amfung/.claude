# .claude
Claude Code configuration

## Quick Start
Make a backup of existing `.claude` and `.claude.json`.

```bash
cd ~
git clone https://github.com/5amfung/.claude.git
cd <your_project>
claude
```

## Development
Add configuration, agents, plugins, skills, or whatnot at project level.
They will become user level `~/.claude` when this repo is cloned to the
user home directory.

```bash
mkdir dot-claude-dev
cd dot-claude-dev
git clone https://github.com/5amfung/.claude.git
claude # do stuff a project level
```
