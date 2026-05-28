# Skills ▸ first-party primitive

**Source:** https://code.claude.com/docs/en
**Type:** First-party primitive
**Install:** N/A — markdown files; nothing executes at install
**Project context assumed:** Project with reusable domain knowledge that should
load on demand.

## Surface

A markdown file (`SKILL.md`) plus optional `references/`, `examples/`,
`scripts/`. Loaded by Claude Code when the description matches the user's intent.
Self-contained, sandboxable, distributable as part of a plugin.

## Smells

None individually. Skills are author-controlled markdown; the supply chain risk
is *whose* skill, not the primitive itself.

## Scores

**Use case:** Reusable playbook / domain knowledge — when none of Permissions,
Hooks, MCP, or Sub-agents fits the need.

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | A+ | Markdown in the repo, fully inspectable, no hidden behaviour |
| Cost | A  | On-demand loading — only pays for context when triggered |
| Simp | A  | One folder per skill; standard structure; debugging is reading the file |
| Corr | A  | LLM applies the skill at its discretion; correctness depends on the skill's clarity |

## Recommendation

**Buy** — the default primitive when the decision tree falls through everything
above it. The decision framework's rule: *reach for Skills last among the
six primitives — when none of the others fits.*

Don't reach for Skills when a Hook would do the job deterministically. Skills
are *context*, Hooks are *enforcement*.
