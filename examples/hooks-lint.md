# Hooks ▸ surgical (lint / secret-scan)

**Source:** https://code.claude.com/docs/en/hooks
**Type:** First-party primitive (PreToolUse / PostToolUse / Stop)
**Install:** N/A — a `hooks.json` and shell scripts in your own repo
**Project context assumed:** Any project that has a rule worth enforcing deterministically.

## Surface

A single shell command fires on a lifecycle event. Configured in
`hooks.json`. Exit code or stdout controls the LLM's next move.

## Smells

None — the hook is your code, in your repo.

## Scores

**Use case:** Surgical hook — one hook, one concern, fast. E.g. lint on file
write, secret-scan on bash, boundary-check on edit.

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | A+ | Hook is shell code in the repo; every invocation is loggable |
| Cost | A+ | Local shell — no LLM call, no token cost |
| Simp | A  | Setup cost is the one-time understanding of the events surface |
| Corr | A+ | Deterministic — the rule either fires or it doesn't |

## Recommendation

**Buy** — `vendoring.md` row "Every gate clears budget as-is".

This is the framework's preferred enforcement mechanism. If a rule needs to be
*enforced* rather than *suggested*, a hook is correct. If you can't reduce the
rule to a shell command, the rule is probably a skill, not a hook.

Compare to `hooks-chained.md` for the "wrong use" version of the same primitive.
