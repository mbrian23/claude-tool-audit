# Sonnet (Claude Sonnet 4.6)

**Source:** Anthropic — first-party model
**Type:** Model selection
**Project context assumed:** Any project; Sonnet vs Opus is the decision.

## Surface

A faster, cheaper Claude model. Same Claude Code interface; different model ID
under the hood. Switchable per-session.

## Smells

None — first-party, fully documented, pinnable by ID.

## Scores

**Use case:** Default for high-volume / context-heavy work — Sonnet is plenty for
most coding tasks, Opus is overkill when the task isn't deep-reasoning.

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | A  | First-party, model ID pinnable, behaviour documented |
| Cost | A  | Cheaper per token than Opus; substantially cheaper for routine work |
| Simp | A+ | Switch with one config line; no operational change |
| Corr | A  | Strong on coding tasks; not Opus-level for hardest reasoning steps |

## Recommendation

**Buy** — every project should have a Sonnet/Opus split policy.

The usual policy: Sonnet by default; Opus for plan-mode, hard refactors, and
production-bound code. **Don't average models** — Sonnet is the right tool for
its use case, Opus for its.
