# Divergence notes ▸ this rubric vs. `gates-scored-tools.md`

This file is **not** parsed by `compare-scores.py` (no `## Scores` section). It
documents where the plugin's methodology diverges from the talk's source-of-truth
file at `meetup-27-may/gates-scored-tools.md`, and which scoring is better in
each case.

## Scale mapping ▸ Fibonacci ↔ letters

The source file uses a **Fibonacci** scale (1 · 2 · 3 · 5 · 8 · 13). The
presentation slides and this plugin use **letters** (A+ · A · B · C · D · F).
Calibrating against tools that appear in both (Context7, Playwright):

| Fibonacci | Letter |
|-----------|--------|
| 13 | A+ |
| 8 | A |
| 5 | C |
| 3 | D |
| 2 | D or F (severity-dependent) |
| 1 | F |

**B is unused in Fibonacci** — the scale jumps from 5 (C) to 8 (A). The letter
scale fills the gap. Where this rubric uses B, the source file would have written
either 5 or 8 with a qualifier in the verdict column. The letter B is a genuine
refinement; the Fibonacci scale forces a snap to the nearest landmark
(intentionally) and the letter scale narrows the verdict (also intentionally).
Both are valid. The letter form is sharper to read on a slide.

## Where this rubric is better

### 1. Per-use-case framing is enforced

The source file gives **one row per tool**. The talk's slides already split
`CLAUDE.md` (tight vs. bloated) into two rows — this rubric extends the principle
to every tool. Concretely:

- `hooks-lint.md` (A+/A+/A/A+) vs. `hooks-chained.md` (C/D/D/C) — same primitive,
  different use, very different scores. Source file collapses into one row
  (`Hooks: 13/13/5/13`).
- `claude-md-tight.md` (A+/A/A+/A) vs. `claude-md-bloated.md` (C/D/C/D) — already
  in slides; rubric encodes the principle.
- `claude-code-router.md` flips Reject → Buy depending on whether the project
  is "client work" or "personal hobby." Source file recommends "personal/hobby
  only" in prose; rubric encodes the threshold mechanically.

**Why better**: the talk's central insight ("scores are circumstantial") becomes
mechanical, not aspirational. The Scores table requires a `Use case:` line; the
parser rejects files without it.

### 2. Knock mechanics are structured

Source file says things like "fans out tokens; correctness payoff is real" in
the verdict column. This rubric encodes the same observation as a **named smell
with a letter knock** in `references/black-box-risks.md` and `references/cost-risks.md`.

Concretely for `pr-review-toolkit`: source says Cost 5 (C) with prose "fans out
tokens." This rubric reaches the same C by applying the "agent recursion" Cost
cap, with the smell named. Result is the same; the reasoning is teachable.

### 3. B-letter resolves the Fibonacci gap

Source file scores Slack MCP and Vercel MCP at **Corr 8 (A)**. This rubric scores
them at **Corr B** — between C and A. Reason: sending Slack messages and
promoting Vercel deployments are reversible-but-noisy in different ways; the LLM
choice of recipient/deployment is the variable. A is too generous, C is too
harsh. The letter scale allows the verdict the Fibonacci scale skips.

**Caveat**: this is a one-letter divergence, not a category-changing one. Both
scales land on "wrap, don't buy raw" for these tools.

## Where the source file is better

### 1. Coverage

Source file scores ~35 tools across 7 categories (models, slash commands,
primitives, community plugins, frameworks, wrappers, MCPs). This rubric ships
19 examples. The source file is the **canonical** corpus; this plugin is the
**runnable** corpus.

### 2. Verdict column

Source file's "Verdict" column is one sentence per row. Easy to scan, easy to
fit on a slide. This rubric's Recommendation paragraphs are longer and slower.

### 3. Self-calibration

Source file was scored as a single pass — internal consistency is high. This
rubric's scores were assigned in batches; some may drift relative to others
until a calibration pass settles them.

## Specific deltas (where letters disagree with the Fibonacci→letter mapping)

| Tool | Source | This rubric | Delta | Reason |
|------|--------|-------------|-------|--------|
| Slack MCP | C/A/A/A | C/A/A/**B** | Corr A → B | LLM-chosen recipient is the variable; B is the honest verdict |
| Vercel MCP | C/A/A/A | C/A/A/**B** | Corr A → B | Deployment promotion is reversible-but-noisy; same logic |
| Gmail/Drive MCP | D/A/A+/A | **D**/A/A+/A | none (numerically) | Source already lands at D Obs via prose; rubric makes the knock explicit |
| Hooks (primitive) | A+/A+/C/A+ | **A+/A+/A/A+** (lint use) **/** **C/D/D/C** (chained use) | Simp depends on use | Per-use split is a refinement, not a disagreement |
| Subagents | A/C/C/A+ | A/C/C/A+ (PR review use) | none | Source row matches the PR review use case implicitly |
| Auto memory | C/C/A/C | C/C/A/C | none | Matches |

## Recommendation for the talk

1. **Keep the Fibonacci scale as historical reference** in `gates-scored-tools.md`
   for the broader corpus the slides can't fit. Note the letter mapping at the
   top of the file.
2. **The slides should use letters** — they already do; no change.
3. **Use this plugin's per-use-case files** as the canonical examples shown
   during the framework section of the talk. They're already parseable by the
   compare script and ship with the rubric.
4. **Add B-scoring tools** (Slack, Vercel) to the external-data slide to
   demonstrate that the letter scale resolves cases the Fibonacci scale couldn't.
5. **Run `python3 scripts/compare-scores.py`** live on stage as the "and here's
   the comparison matrix" reveal — it takes a second and renders the framework's
   judgments side by side.
