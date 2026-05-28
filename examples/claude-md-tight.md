# CLAUDE.md ▸ tight

**Source:** https://code.claude.com/docs/en/memory
**Type:** First-party primitive (always-on context file)
**Install:** N/A — a markdown file you author; no install step
**Project context assumed:** Any project that has more than one contributor.

## Surface

A single markdown file at the repo root. Always loaded by Claude Code into every
prompt for that project. No side effects, no LLM calls of its own.

## Smells

None — it's a first-party primitive with full source visibility.

## Scores

**Use case:** Project conventions and always-on facts — under 200 lines, only
conventions and links to longer docs, no imperative rules that need enforcement.

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | A+ | One markdown file in the repo; fully scannable; no hidden behaviour |
| Cost | A  | Loaded into every prompt — context cost is non-zero but bounded if file stays small |
| Simp | A+ | A markdown file. A teammate at 3am can read and edit it. |
| Corr | A  | Conventions land reliably; not deterministic enforcement (that's what hooks are for) |

## Recommendation

**Buy** — every project should run `/init` and curate a tight `CLAUDE.md`. No
matrix row triggers a stricter recommendation.

Pair with hooks for any rule that needs *enforcement* rather than *context*. The
talk's framework is explicit: `CLAUDE.md` is context, hooks are enforcement.
