---
description: Audit one candidate Claude Code tool against the rubric. Interactive scoring across the four gates (Obs / Cost / Simp / Corr) on the A+..F letter scale; produces a recommendation (Build/Buy/Wrap/Vendor/Defer/Reject).
argument-hint: "[tool name or description]"
allowed-tools: ["Read", "Write", "Bash", "AskUserQuestion", "WebFetch"]
---

Invoke the `audit-tool` skill at `${CLAUDE_PLUGIN_ROOT}/skills/audit-tool/SKILL.md`.

Pass `$ARGUMENTS` through as the candidate tool to audit. Follow the skill's
five-step procedure: establish project context AND use case, enumerate the
surface, score the four gates (Obs / Cost / Simp / Corr) on the letter scale
(A+ · A · B · C · D · F), apply black-box and cost knocks, and produce a vendoring
recommendation using the matrix in `${CLAUDE_PLUGIN_ROOT}/references/vendoring.md`.

Interactive by default. End with the canonical Scores table — letters only, no
sum or average — same format as `${CLAUDE_PLUGIN_ROOT}/examples/*.md` so
`scripts/compare-scores.py` can parse the output if the user persists it.
