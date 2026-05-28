# Hooks ▸ chained external (the wrong use)

**Source:** Same primitive as `hooks-lint.md`. Same docs.
**Type:** First-party primitive (PreToolUse / PostToolUse / Stop)
**Install:** N/A — `hooks.json` + shell scripts; supply chain risk lives in *what your scripts call out to*
**Project context assumed:** Any project that's reached for hooks for the wrong job.

This file demonstrates **same tool, different use, very different scores** — the
sibling of `claude-md-tight.md` vs `claude-md-bloated.md`.

## Surface

Five hooks chained on `PostToolUse`. Each calls an external API. One uses an LLM
to "decide" whether to block. Every Claude action stalls behind the slowest
hook.

## Smells

- **Agent recursion.** A hook that itself calls an LLM. **Cost capped at C.**
- **Hidden side effects** — external API calls from every tool invocation.
  **Knock: −1 Obs, −1 Corr.**

## Scores

**Use case:** "Smart" hook stack — 5 chained, external API calls, LLM in the
decision path. Over-engineered, stalls every action.

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | C  | Hooks are in the repo, but the external API calls are not auditable; knock applied |
| Cost | D  | LLM in the decision path; cap and amplification both apply |
| Simp | D  | 5 chained hooks, debugging order matters; behaviour changes with config order |
| Corr | C  | The LLM "decider" is non-deterministic; knock applied |

## Recommendation

**Replace** — `vendoring.md` row "Simp D → Build or pick a different tool".

Concrete: split into one hook per concern. Drop the external API calls (move
them to scheduled jobs, not lifecycle hooks). Replace any "LLM decider" with a
deterministic shell check.

The framework's rule is **one hook, one concern, fast.** Five chained hooks is
five tools, not one.
