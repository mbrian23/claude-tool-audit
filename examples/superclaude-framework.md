# SuperClaude_Framework

**Source:** https://github.com/SuperClaude-Org/SuperClaude_Framework
**Type:** Plugin (cognitive personas + structured workflows)
**Install:** **`/plugin install`** + framework config ▸ heavier setup; review the persona files before adopting.
**Project context assumed:** Team committing to a unified house style.

## Surface

A bundle of personas (Architect, Reviewer, Refactorer, etc.), each invoking
custom prompts and workflows. The framework reshapes how the team interacts
with Claude. Heavy.

## Smells

- **Vendor-controlled prompt/model** in each persona. **Knock: −1 Obs, −1 Cost.**
- **Cost amplification** — persona workflows often chain into multiple
  reviewers per task. **Cost capped at D.**

## Scores

**Use case:** Teams adopting a unified cognitive style across all Claude Code
sessions — house style is the deliverable.

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | A  | Open source, personas in the repo; knock applied |
| Cost | D  | Multi-persona chains compound; cap and amplification both apply |
| Simp | D  | Heavy methodology; persona naming and selection has its own learning curve |
| Corr | C  | Persona outputs vary; not stronger than the underlying model's reasoning |

## Recommendation

**Defer** for most projects — `vendoring.md` row "Multi-year product → any gate at D".

This is `obra/superpowers` *without* the A+ Corr payoff. Superpowers pays Cost
& Simp to buy A+ Corr; SuperClaude pays Cost & Simp for the same Corr you'd
get without it. The trade is harder to justify.

**Buy** is acceptable for a team that explicitly values house style above raw
output quality — but that team should know the trade-off they're making.
