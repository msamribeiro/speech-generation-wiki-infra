@AGENTS.md

## Claude Code integration

The project subagents in `.claude/agents/` are thin adapters that preload the canonical workflow
skills from `.agents/skills/`. Use those subagents for isolated or parallel work when helpful.
Do not copy workflow rules into this file or into Claude auto-memory.
