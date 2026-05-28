# CLAUDE.md ▸ bloated

**Source:** Same primitive as `claude-md-tight.md`. Same docs, same file.
**Type:** First-party primitive (always-on context file)
**Project context assumed:** Any project that has more than one contributor.

This file exists to demonstrate that **the same tool scores differently for
different use cases**. Same `CLAUDE.md`, different use, very different scores.

## Surface

A markdown file at the repo root, but: 500+ lines, conflicting rules, big
`@import` directives that pull in three more files, mixing project conventions
with imperative rules that need enforcement.

## Smells

- Effectively a black box from the LLM's POV — too much context, conflicting
  instructions, no single source of truth. **Knock: −1 Obs, −1 Corr.**

## Scores

**Use case:** Trying to use `CLAUDE.md` for *enforcement* — listing imperative
rules ("never run X", "always do Y") rather than just context.

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | C  | The file is still readable, but the LLM's reading of it is unpredictable; knock applied |
| Cost | D  | 500+ lines on every prompt is a Cost smell; context-amplification cap applies for the whole project |
| Simp | C  | Long file, conflicting rules, imports — debugging "why didn't Claude follow rule 47?" takes hours |
| Corr | D  | Claude reads `CLAUDE.md` as *context*, not enforcement; rules at this length are routinely violated; knock applied |

## Recommendation

**Replace** — `vendoring.md` row "Simp D or F → Build or pick a different tool."

Concrete: split the file. Keep `CLAUDE.md` as tight conventions under 200 lines.
Move enforcement rules to **hooks** (deterministic, falsifiable). Move longer
domain docs to **skills** (loaded on demand). Move ephemeral planning into the
session itself.

This is the canonical "same primitive, wrong use" pattern from the talk. The
remedy is never "make `CLAUDE.md` longer"; it's "pick the right primitive."
