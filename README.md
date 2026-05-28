# claude-tool-audit

Interactive auditor for tools you're considering adding to a Claude Code project.

Scores candidate tools (MCP servers, hooks, skills, sub-agents, third-party CLIs)
against **four gates** — **Obs · Cost · Simp · Corr** — on a letter scale
(A+ · A · B · C · D · F). The rubric is the talk's `gates-scored-tools.md`
made runnable: per-use-case scoring, no averaging, **one failing gate = drop**.

Also helps set a **per-gate budget** for a new project and pick a **vendoring
strategy** (build / buy / wrap / vendor / defer) per category.

---

## The four gates

- **Obs ▸ Observability & Ownership** — how it works *inside*. Scannable? Auditable supply chain? No black box?
- **Cost** — $/request, $/run, **tokens too**. The fast modes are great and expensive.
- **Simp ▸ Simplicity & Maintainability** — will it make sense in 3 months? Can a teammate run it without you?
- **Corr ▸ Correctness of Output** — deterministic-enough? Verifiable? Falsifiable? Or running on faith?

Your project may add **one fifth gate** (Ethics / Privacy / Latency / Compliance)
if it actually changes a decision the four gates don't.

## Why letters, not numbers

The four gates aren't directly comparable, and you **can't sum or average them**.
A great `Corr` doesn't buy back a failing `Obs`. The letter scale forces a per-gate
verdict; the engineering decision lives in the threshold, not the aggregate.

> Can't decide A or B? Pick B. Can't decide D or F? Pick F.

---

## Install (local)

```bash
git clone https://github.com/mbrian23/claude-tool-audit ~/plugins/claude-tool-audit
# Then in Claude Code:
/plugin install ~/plugins/claude-tool-audit
```

Or test without installing:

```bash
cc --plugin-dir ~/plugins/claude-tool-audit
```

## Use

| Skill | Trigger | What it does |
|-------|---------|--------------|
| `audit-tool` | `/claude-tool-audit:audit-tool <tool-name>` | Walks you through scoring one candidate against the four gates **for a specific use case**. Produces a scored markdown file `compare-scores.py` can parse. |
| `audit-project` | `/claude-tool-audit:audit-project` | Scans `.claude/`, plugin configs, `.mcp.json`, hooks, sub-agents, permission entries in the current repo and audits the portfolio. |
| `budget-planner` | `/claude-tool-audit:budget-planner` | Interactive scoping → recommends a **letter threshold per gate**, picks a vendoring strategy, optionally writes `budget.md` and `vendoring.md`. |

A fourth skill, `scoring-fundamentals`, auto-triggers when you ask about scoring, gates, or risk evaluation.

## What's encoded

- `references/gates.md` — the four gates with A+..F per-letter rubrics, threshold mindset, fifth-gate guidance.
- `references/black-box-risks.md` — four black-box smells with **letter knocks** (each smell drops a letter on listed gates).
- `references/cost-risks.md` — context amplification, agent recursion, unbounded calls; **letter caps on Cost**.
- `references/vendoring.md` — Build / Buy / Wrap / Vendor / Defer; tactic-to-gate matrix.
- `examples/*.md` — worked audits using the canonical letter Scores table so `scripts/compare-scores.py` can parse them.

## Compare scores

```bash
python3 scripts/compare-scores.py
```

Reads every `examples/*.md`, extracts the **Scores** table, prints a side-by-side
comparison. **No sum, no average** — flags each tool's worst gate so the "one
failing gate = drop" rule is visible at a glance.

Sample output:

```
Tool                Obs  Cost  Simp  Corr   Worst    Use case
-------------------------------------------------------------
claude-md-bloated     C     D     C     D  D (Cost)  Trying to use CLAUDE.md for enforcement…
claude-md-tight      A+     A    A+     A   A (Cost) Project conventions and always-on facts…
context7-mcp          D     C    A+     A   D (Obs)  Live library docs for fast-moving APIs…
permissions          A+    A+    A+    A+   A+ (Obs) The lightest fix in the decision framework…
playwright-mcp        A     A     A    A+   A (Obs)  UI verification on internal product…
slack-mcp             C     A     A     B   C (Obs)  Ops/on-call automation…
vercel-mcp            C     A     A     B   C (Obs)  Deploy automation in a Vercel-hosted project…
```

The contrast between `claude-md-tight` and `claude-md-bloated` is the canonical
demonstration: **same tool, different use case, very different scores**.

## Reproducing the plugin

Built end-to-end via the `/plugin-dev:create-plugin` workflow against the
[meetup-27-may](https://github.com/mbrian23/meetup-27-may) talk repo. The rubric
is the talk's `gates-scored-tools.md` (with the letter scale from slide 17 of the
deck) made runnable.

See [`MILESTONES.md`](./MILESTONES.md) for the build sequence.

## License

MIT
