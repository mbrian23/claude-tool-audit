# Haiku (Claude Haiku 4.5)

**Source:** Anthropic — first-party model
**Type:** Model selection
**Install:** N/A — model selection, no install step
**Project context assumed:** Sub-agent worker pools, cheap audit hooks.

## Surface

The cheapest, fastest Claude model. Used as a sub-agent worker or in cost-audit
hooks where the cheap pass is "good enough."

## Smells

None.

## Scores

**Use case:** Sub-agent workers and cheap-model audit hooks — Haiku is the floor;
use it when "good enough fast" beats "deep and slow."

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | A  | First-party, model ID pinnable |
| Cost | A+ | Cheapest in the family; ideal for hooks and per-call workers |
| Simp | A+ | Same switch surface as any other model |
| Corr | C  | Not for deep reasoning; for filter-and-flag work, correctness is acceptable |

## Recommendation

**Buy** — for cost-audit hooks, secret-scan, lint-classification, sub-agent
fan-out workers.

**Don't** use Haiku for the main session driver on non-trivial code. The Corr
gate is the binding constraint — pick Haiku for tasks where C is enough.
