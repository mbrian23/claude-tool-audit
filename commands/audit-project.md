---
description: Audit the current repo's full Claude Code setup — MCP servers, hooks, skills, sub-agents, settings — and produce a portfolio view.
argument-hint: "[optional: project root path, defaults to cwd]"
allowed-tools: ["Read", "Bash", "Glob", "Grep", "AskUserQuestion", "Write"]
---

Invoke the `audit-project` skill at
`${CLAUDE_PLUGIN_ROOT}/skills/audit-project/SKILL.md`.

Pass `$ARGUMENTS` as the project root (default: cwd). Follow the skill's six-step
procedure: enumerate the surface, classify by type and trust origin, establish
project context, score each (tool, use case) pair against the four gates, produce
a portfolio view (failing gates per tool, redundancies, concentration risk), and
recommend the top three actions.

Use the rubric at `${CLAUDE_PLUGIN_ROOT}/references/gates.md` and the matrix at
`${CLAUDE_PLUGIN_ROOT}/references/vendoring.md`. Letters only — never sum or
average across gates.
