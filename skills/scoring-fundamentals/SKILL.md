---
name: scoring-fundamentals
description: This skill should be used when the user asks about "scoring a tool", "the four gates", "how to evaluate an MCP server", "black-box risk", "cost risk", "vendoring strategy", "Obs/Cost/Simp/Corr", or otherwise discusses how to judge a candidate tool for a Claude Code project. Loads the rubric so subsequent reasoning uses the encoded gates and letter scale.
version: 0.1.0
---

# Scoring fundamentals

Load the audit rubric into the conversation before any scoring or comparison work
begins. Trigger as soon as the user starts evaluating, comparing, or budgeting for
tools — never after.

## What the rubric encodes

**Four gates**, each scored on a **letter scale** (A+ · A · B · C · D · F).
Bigger is always better. **No summing, no averaging** — one failing gate drops the
tool. Scores are **per-use-case**, not per-tool: the same primitive scores
differently for different uses.

- `${CLAUDE_PLUGIN_ROOT}/references/gates.md` — the four gates (Obs, Cost, Simp, Corr), letter scale, per-gate rubrics, threshold mindset, optional fifth gate.
- `${CLAUDE_PLUGIN_ROOT}/references/black-box-risks.md` — four smells, letter knocks (each smell drops one letter on listed gates).
- `${CLAUDE_PLUGIN_ROOT}/references/cost-risks.md` — context amplification, agent recursion, unbounded calls; letter caps on Cost.
- `${CLAUDE_PLUGIN_ROOT}/references/vendoring.md` — Build / Buy / Wrap / Vendor / Defer; tactic-to-gate matrix.

## How to use the rubric in a conversation

1. **Read `gates.md` first.** Every other reference assumes its vocabulary.
2. **Establish the use case.** The same tool scores differently for "lint hook" vs
   "external-API gating hook." Name the use case before scoring.
3. **Walk the four gates in order**: Obs, Cost, Simp, Corr. Force a justification
   per gate even when the answer feels obvious — the act of justifying surfaces
   the disagreements.
4. **Apply black-box knocks** from `black-box-risks.md`. One letter down per smell.
5. **Apply Cost caps** from `cost-risks.md`. Strictest cap wins.
6. **Recommend** using the matrix in `vendoring.md`. Build / Buy / Wrap / Vendor /
   Defer. If two rows match and disagree, the stricter recommendation wins.

## Output shape

Every audit ends with the canonical Scores table from `gates.md`:

```markdown
## Scores

**Use case:** <one-line description — required>

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | A  | ... |
| Cost | C  | ... |
| Simp | A+ | ... |
| Corr | A  | ... |
```

Pin column names. Letters only — never numbers. Justifications stay to one
sentence each so the table is readable on a slide.

## Worked examples

Existing audits live in `${CLAUDE_PLUGIN_ROOT}/examples/`. Read one before scoring
a new tool — they show the depth of justification the rubric expects and how the
use case shapes each gate.

## When NOT to score

- The project hasn't been scoped yet. Run `budget-planner` first to fix the
  per-gate threshold, then come back.
- The candidate is so clearly disqualified on one gate that scoring the rest is
  theatre. Say so plainly and recommend Reject.

## Don't

- Don't sum or average the four letters into one verdict. The gates are not
  comparable to each other.
- Don't score "the tool" — score "the tool *for this use case*." A bare tool name
  in the audit file is a mistake.
- Don't use numbers in the Scores table. The compare script expects letters; the
  framework's whole point is that the scale is ordinal, not interval.
