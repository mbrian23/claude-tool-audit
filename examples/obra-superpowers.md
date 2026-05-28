# obra/superpowers

**Source:** https://github.com/obra/superpowers
**Type:** Plugin (sub-agent methodology — TDD + brainstorming + 2-stage review)
**Install:** **`/plugin install`** ▸ markdown agents + commands. Readable. No code at install.
**Project context assumed:** Multi-month product where correctness justifies the bill.

## Surface

A bundle of slash commands, sub-agents, and skills. Implements a TDD-first
methodology: brainstorm → propose → implement → review (cheap-model) → review
(strong-model). Accepted into Anthropic's official marketplace.

## Smells

- **Cost amplification** — every iteration fans out into multiple sub-agent runs.
  **Cost capped at D** per `cost-risks.md`.
- **Simplicity erodes** — the methodology *is* the deliverable, so adopting it
  reshapes the team's flow. Brand-new contributors can't ramp in a day.

## Scores

**Use case:** Production code where correctness justifies the bill — adoption of
the methodology, not casual sampling.

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | A  | Open source, sub-agent runs are inspectable, prompts in the repo |
| Cost | D  | Fan-out into multiple cheap-and-strong reviews per change; cap applied |
| Simp | D  | Heavy methodology; you adopt the whole flow or you don't get the value |
| Corr | A+ | Best-in-class on Corr — that's the whole point of paying Cost & Simp |

## Recommendation

**Wrap** (adopt selectively) — `vendoring.md` row "Multi-year product → any gate at D".

Concrete: cherry-pick the 2-stage review sub-agent for critical PRs only. Don't
install the whole methodology unless the team commits. The "drop on a failing
gate" rule is suspended here only because the failing gates (Cost, Simp) are the
*price* of buying A+ Corr — accept the trade explicitly.

For prototypes: **Defer.** Two-week horizons don't justify the methodology.
