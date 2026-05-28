# pr-review-toolkit

**Source:** Anthropic-published plugin (in this marketplace)
**Type:** Plugin (6 specialized review sub-agents)
**Project context assumed:** Any project shipping PRs with non-trivial diffs.

## Surface

Six sub-agents that fan out in parallel: style, silent-failure, types, tests,
comments, simplicity. A driver command coordinates them. Each runs on a cheaper
model where reasonable.

## Smells

None individually — the sub-agents are documented and inspectable.
- **Cost amplification** — fan-out × 6 reviewers per PR. Pay attention.

## Scores

**Use case:** Pre-merge review for non-trivial PRs where catching silent failures
and type errors before they ship justifies the per-review bill.

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | A  | Anthropic-published; sub-agents are in the repo; per-agent logs visible |
| Cost | C  | Fan-out to 6 sub-agents; cheaper-model workers contain it; still non-trivial |
| Simp | C  | Composition of 6 specialists; debugging a missing finding requires understanding which agent had jurisdiction |
| Corr | A+ | Best-in-class on review correctness — six specialized perspectives is the value proposition |

## Recommendation

**Wrap** — `vendoring.md` row "Cost is C–D → Wrap with budget hook".

Concrete: gate `/review-pr` on PR size — small PRs skip half the agents; big PRs
run the full fan-out. The Cost and Simp failures are accepted in exchange for
A+ Corr, same trade as `obra/superpowers` but lighter.

For prototypes: **Defer** — manual review is fine when there's nothing to lose.
