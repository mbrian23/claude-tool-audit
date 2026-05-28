# claude-tool-audit

Interactive auditor for tools you're considering adding to a Claude Code project.

Scores candidates against **four gates** on a letter scale (A+ · A · B · C · D · F):

- **Obs** ▸ **Observability & Ownership** — how it works *inside*. Scannable? Auditable supply chain? No black box?
- **Cost** — `$`/request, `$`/run, **tokens too**. The fast modes are great and expensive.
- **Simp** ▸ **Simplicity & Maintainability** — will it make sense in 3 months? Can a teammate run it without you?
- **Corr** ▸ **Correctness of Output** — deterministic-enough? Verifiable? **Falsifiable?** Or running on faith?

The rubric is per-use-case (same primitive used differently scores differently),
no averaging, **one failing gate = drop**.

Also helps set a **per-gate budget** for a new project and pick a **vendoring
strategy** (build / buy / wrap / vendor / defer) per category.

Live corpus of 29+ worked audits ▸ [**mbrian23.github.io/claude-tool-audit**](https://mbrian23.github.io/claude-tool-audit/)

---

## Why letters, not numbers

The four gates aren't directly comparable, and you **can't sum or average them**.
A great `Corr` doesn't buy back a failing `Obs`. The letter scale forces a per-gate
verdict; the engineering decision lives in the threshold, not the aggregate.

The full scale:

| Letter | Meaning |
|--------|---------|
| **A+** | Exemplary ▸ best-in-class on this gate |
| **A**  | Good ▸ a strong reason to pick it |
| **B**  | Acceptable ▸ within budget for most projects |
| **C**  | Mediocre ▸ wouldn't pick *for this reason* |
| **D**  | Poor ▸ noticeably weak |
| **F**  | Failure ▸ a clear miss; drop it for this use case |

> Can't decide A or B? Pick B. Can't decide D or F? Pick F. The letter forces a verdict; the *gap* is the warning.

A project may legitimately add **one fifth gate** (Ethics, Privacy, Latency,
Compliance) when its profile demands it.

---

## Install

This repo is itself a single-plugin marketplace. Install via the standard Claude
Code plugin flow — no special flags, no local clones required.

```text
# Inside Claude Code:
/plugin marketplace add mbrian23/claude-tool-audit
/plugin install claude-tool-audit@claude-tool-audit
```

Then restart the session (or run `/plugin reload`) so the skills register.

### Updating

```text
/plugin marketplace update claude-tool-audit
/plugin install claude-tool-audit@claude-tool-audit
```

### Removing

```text
/plugin uninstall claude-tool-audit@claude-tool-audit
/plugin marketplace remove claude-tool-audit
```

### Local development

If you want to hack on the plugin itself:

```bash
git clone https://github.com/mbrian23/claude-tool-audit ~/code/claude-tool-audit
```

```text
# In Claude Code, add the local path as a marketplace:
/plugin marketplace add ~/code/claude-tool-audit
/plugin install claude-tool-audit@claude-tool-audit
```

---

## Use

Three user-invokable slash commands plus an auto-trigger knowledge skill.

| Command | What it does |
|---------|--------------|
| `/claude-tool-audit:audit-tool <tool>` | Walks you through scoring one candidate against the four gates **for a specific use case**. Produces a scored markdown file `compare-scores.py` can parse. |
| `/claude-tool-audit:audit-project` | Scans `.claude/`, plugin configs, `.mcp.json`, hooks, sub-agents, permission entries in the current repo and audits the portfolio. |
| `/claude-tool-audit:budget-planner` | Interactive scoping → recommends a **letter threshold per gate**, picks a vendoring strategy, optionally writes `budget.md` and `vendoring.md`. |

The `scoring-fundamentals` skill auto-triggers when you ask about scoring, gates, or risk evaluation.

## What's encoded

- `references/gates.md` — the four gates with A+..F per-letter rubrics, threshold mindset, fifth-gate guidance.
- `references/black-box-risks.md` — five black-box smells with **letter knocks** (the first is **install-time code execution** — runs before runtime surface or auth scope, since neither matters if the install already ran code you didn't see).
- `references/cost-risks.md` — context amplification, agent recursion, unbounded calls; **letter caps on Cost**.
- `references/vendoring.md` — Build / Buy / Wrap / Vendor / Defer; tactic-to-gate matrix.
- `examples/*.md` — 29+ worked audits using the canonical letter Scores table so `scripts/compare-scores.py` can parse them.

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

## Web view

The full corpus is published as a static site for QR-scanning during the talk:
[**mbrian23.github.io/claude-tool-audit**](https://mbrian23.github.io/claude-tool-audit/).
The page is regenerated by `scripts/build-site.py` from the `examples/` directory
and served from `docs/` via GitHub Pages.

## Reproducing the plugin

Built end-to-end via the `/plugin-dev:create-plugin` workflow against the
[meetup-27-may](https://github.com/mbrian23/meetup-27-may) talk repo. The rubric
is the talk's four-gate letter scale (Obs / Cost / Simp / Corr · A+..F) made
runnable.

See [`MILESTONES.md`](./MILESTONES.md) for the build sequence.

## License

MIT
