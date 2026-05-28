# Build milestones

This plugin was built in eight milestones. Each is independently verifiable.

- **M1 — Scaffold.** `.claude-plugin/plugin.json`, `README.md`, `.gitignore`, directory tree.
- **M2 — Rubric references.** `references/gates.md`, `references/black-box-risks.md`, `references/cost-risks.md`, `references/vendoring.md`.
- **M3 — Skills.** `skills/audit-tool/SKILL.md`, `skills/audit-project/SKILL.md`, `skills/budget-planner/SKILL.md`, `skills/scoring-fundamentals/SKILL.md`. Plus thin `commands/*.md` wrappers for slash-command invocation.
- **M4 — Worked examples.** Scored audits under `examples/` for Playwright MCP, Context7 MCP, Slack MCP, Vercel MCP. Plus `claude-md-tight.md` vs `claude-md-bloated.md` (same primitive, different use case) and `permissions.md` (the A+ no-brainer).
- **M5 — Compare script.** `scripts/compare-scores.py` parses every example's letter Scores table, renders a side-by-side comparison, flags each tool's worst gate. **No sum, no average.**
- **M6 — Validate & test.** Plugin-validator clean, `python3 scripts/compare-scores.py` parses all examples, skills load when invoked.
- **M7 — Publish.** `mbrian23/claude-tool-audit` on GitHub (private at first, flip to public when ready), README install instructions verified.
- **M8 — Align to talk design.** Refactored from a 7-dimension numeric rubric to the talk's 4-gate letter scale (Obs/Cost/Simp/Corr, A+..F). Scoring framed as per-use-case throughout. Removed sum/average column. Added the `claude-md-tight` vs `claude-md-bloated` example pair to make the per-use-case principle concrete.

## Reproducing from scratch

```bash
# In Claude Code, inside any working directory:
/plugin-dev:create-plugin Create a Claude Code tool auditor…
```

…then follow the milestones above. The skills are intentionally short — they
reach into `references/` and `examples/` rather than embedding the rubric inline,
so the rubric stays the single source of truth.

## Design notes

The rubric explicitly **does not** support summing or averaging the gates. The
talk's framing is "engineering lives in the threshold" — you set a per-gate
budget, and any tool below the budget on *any single gate* is dropped, regardless
of how it scores elsewhere. The compare script flags each tool's worst gate
exactly so the dropping logic is visible at a glance.

Scores are per-**use case**, not per-tool. The same primitive (e.g. `CLAUDE.md`)
scores A+/A/A+/A used as tight conventions, and C/D/C/D used as a bloated
enforcement document. Audits must name the use case — the parser requires it.
