# Auto memory

**Source:** Claude Code persistent file-based memory at `~/.claude/projects/.../memory/`
**Type:** First-party primitive
**Project context assumed:** Long-running projects with cross-session context.

## Surface

A directory of small markdown files indexed by `MEMORY.md`. The system writes
user-profile, feedback, project, and reference memories without prompting. Read
back in future sessions to seed context.

## Smells

- **Hidden side effects** — every conversation may write new memories. **Knock:
  −1 Corr.**
- **Stale memory bites** — saved facts can become wrong over time; future
  sessions may act on outdated information.

## Scores

**Use case:** Persistent cross-conversation context — user profile, feedback,
project history.

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | C  | Files are inspectable, but you have to run `/memory` to know what's there |
| Cost | C  | Memories are loaded into context for relevance; the more saved, the more tokens per session |
| Simp | A  | One markdown per memory; auditable directly |
| Corr | C  | Stale memories can mislead; knock applied for the silent-failure mode |

## Recommendation

**Wrap** — `vendoring.md` row "Corr C with silent-failure mode".

Concrete: run `/memory` weekly. Trim aggressively. Add a session-start hook that
flags memories older than 90 days for review. The primitive is useful but
requires hygiene; the wrap is the hygiene.
