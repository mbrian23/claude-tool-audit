# claude-tool-audit ▸ itself

**Source:** https://github.com/mbrian23/claude-tool-audit
**Type:** Plugin (4 skills, 3 slash-command wrappers, 4 references, 2 scripts, 28+ examples)
**Install:** **`git clone` + `/plugin install`** ▸ nothing executes at install. Markdown skills + stdlib Python scripts. Fully readable.
**Project context assumed:** Any Claude Code project considering installing this plugin.

A plugin that scores tools should be willing to score itself. Here it is.

## Surface

- **Skills:** `audit-tool`, `audit-project`, `budget-planner`, `scoring-fundamentals`.
- **Slash commands:** wrappers under `commands/` for the three user-invokable skills.
- **References:** `gates.md`, `black-box-risks.md`, `cost-risks.md`, `vendoring.md`.
- **Scripts:** `compare-scores.py` (~120 lines, stdlib only), `build-site.py`
  (~250 lines, stdlib only). Neither has network or LLM calls.
- **Examples:** 28+ worked audits under `examples/`, all parseable.
- **Install path:** `git clone` + `/plugin install`. **Nothing executes during install.**

## Smells

None.

- Skills invoke LLM calls during interactive scoring — *by design*. The rubric
  needs human-and-LLM judgment per gate; that's the value proposition. Each skill
  is markdown anyone can read before adopting.
- Scripts are stdlib Python, deterministic, locally executed.
- No MCP server, no third-party vendor surface.

## Scores

**Use case:** Adopting this plugin to score other tools in a Claude Code project
— installing it and running the three skills.

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | A+ | All markdown and stdlib Python; no hidden behaviour; install runs no code |
| Cost | A  | LLM calls only when the user invokes a skill; rubric loads on demand; scripts are free |
| Simp | A  | One plugin, four skills, two scripts; standard plugin layout |
| Corr | A  | Interactive scoring is LLM-driven; the rubric (references/) is deterministic and falsifiable |

## Recommendation

**Buy** — the plugin clears every gate.

This is the dogfood test. A plugin that fails its own rubric shouldn't be
adopted; this one passes, with the honest caveat that the *output* of the
interactive scoring is LLM-driven and therefore Corr A, not A+. The rubric
itself (the four references) is A+ deterministic; the *application* of the
rubric uses LLM judgment.

If the project profile is "regulated data with zero LLM-in-the-loop scoring":
**Defer** until you've audited the four references manually. The rubric
encoded there is the durable artifact.
