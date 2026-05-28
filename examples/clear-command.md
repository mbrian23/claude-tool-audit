# /clear

**Source:** https://code.claude.com/docs/en
**Type:** First-party slash command
**Install:** N/A — first-party CLI command, nothing to install
**Project context assumed:** Every Claude Code session.

## Surface

Clears the conversation context. Zero side effects, no LLM call, no state
written.

## Smells

None.

## Scores

**Use case:** Resetting context when the conversation drifts off-task or when
context budget is about to bite — cheaper than scrolling, cheaper than
restarting.

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | A+ | First-party, instantaneous, no hidden behaviour |
| Cost | A+ | Free; actively reduces cost by trimming context |
| Simp | A+ | One command, one effect, no state |
| Corr | A+ | Deterministic — the conversation either resets or it doesn't |

## Recommendation

**Buy** — no-brainer. Use freely; reach for it whenever context drifts.

The framework's "no-brainer" archetype, alongside `permissions.md` and
`ccusage.md`. These three should be default reach-for-it tools in every project.
