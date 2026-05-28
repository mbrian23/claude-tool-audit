# Permissions ▸ allow / ask / deny

**Source:** https://code.claude.com/docs/en/permissions
**Type:** First-party primitive (config layer, before any plugin)
**Project context assumed:** Every project.

## Surface

Three tiers, configured in `.claude/settings.json`:

- **allow** — read-only or low-risk; same outcome every time.
- **ask** — side effects you want to eyeball; the default.
- **deny** — destructive or unrecoverable; never under any circumstance.

No LLM calls of its own. Implemented in Claude Code itself.

## Smells

None — it's the lightest possible fix.

## Scores

**Use case:** The lightest fix in the decision framework — promoting a repeated
"yes" to `allow`, demoting a regret to `deny`, leaving everything else at `ask`.

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | A+ | All in `settings.json`, all in the repo, fully auditable |
| Cost | A+ | Zero runtime cost; cuts cost by removing approval round-trips |
| Simp | A+ | Three tiers, one config file, any teammate can read it |
| Corr | A+ | Deterministic — the rule either matches or it doesn't |

## Recommendation

**Buy** — there's no matrix row that triggers a stricter recommendation. This is
the framework's no-brainer: every project should use this primitive before
reaching for hooks, skills, or sub-agents.

The decision framework explicitly says: *settle approvals at the config layer
before reaching for a primitive.* Default everything to `ask`. Promote to
`allow` after the third "yes" in a row. Demote to `deny` after the first regret.
