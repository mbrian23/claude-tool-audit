# /memory

**Source:** https://code.claude.com/docs/en
**Type:** First-party slash command
**Install:** N/A — first-party CLI command, nothing to install
**Project context assumed:** Long-running projects with persistent memory.

## Surface

Opens the memory directory for review and editing. Lists, edits, deletes
auto-saved memories. Pairs with the auto-memory primitive (`auto-memory.md`).

## Smells

None directly — this is the *hygiene* tool for the auto-memory primitive.

## Scores

**Use case:** Weekly audit of accumulated memories — trim stale ones, verify
project context is still accurate, remove obsolete user preferences.

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | A+ | First-party, opens the directory contents directly for review |
| Cost | A+ | Free, no LLM call |
| Simp | A+ | One command, one inspector view |
| Corr | A  | The inspector is deterministic; what to keep is a judgment call |

## Recommendation

**Buy** — pair with `auto-memory.md`. Run weekly. The auto-memory primitive is
useful but requires this hygiene step; without `/memory` audits, memory rot
silently undermines the Corr gate of the auto-memory primitive.
