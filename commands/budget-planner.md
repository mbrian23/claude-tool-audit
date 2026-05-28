---
description: Set per-gate letter budgets for a Claude Code project across the four gates (Obs / Cost / Simp / Corr, A+..F) plus an optional fifth gate, and recommend a vendoring strategy per category. Optionally writes budget.md and vendoring.md into the project.
argument-hint: "[optional: project name or one-line description]"
allowed-tools: ["Read", "Write", "AskUserQuestion", "Bash"]
---

Invoke the `budget-planner` skill at
`${CLAUDE_PLUGIN_ROOT}/skills/budget-planner/SKILL.md`.

Pass `$ARGUMENTS` as the project description. Follow the skill's four-step
procedure: scope (horizon / audience / data sensitivity / latency / optional
fifth gate), produce per-gate letter thresholds and headroom using `gates.md`
and `cost-risks.md`, surface mitigation patterns with concrete locations, and (on
confirmation) write `budget.md` and `vendoring.md` into the project.

Interactive by default. File writes require explicit user confirmation.
