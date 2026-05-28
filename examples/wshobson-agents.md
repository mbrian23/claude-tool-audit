# wshobson/agents

**Source:** https://github.com/wshobson/agents
**Type:** Marketplace (191 specialized sub-agents across 78 plugins)
**Install:** **`/plugin install` (per sub-agent)** ▸ markdown only; the risk is the **191-surface**, not install code.
**Project context assumed:** Any project with recurring specialist work.

## Surface

A marketplace of pre-built specialist sub-agents — security review, accessibility
audit, database migration helper, infra inspector, etc. Each is a sub-agent
markdown file. The bundle is large.

## Smells

- **Tool surface ≫ docs in detail.** 191 agents; the README explains a fraction.
  **Knock: −1 Obs.** Cherry-picking is the only sane install path.

## Scores

**Use case:** Cherry-picking 2–3 sub-agents that match recurring work in *this*
project — **not** installing the whole marketplace.

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | A  | Open source, agents are inspectable markdown; knock applied for the 191-surface |
| Cost | C  | Each agent run is a fan-out; cost adds up with broad adoption |
| Simp | C  | Composition of many specialists; cognitive load to choose between them |
| Corr | A  | Each specialist is bounded and falsifiable in its narrow domain |

## Recommendation

**Wrap** (cherry-pick) — `vendoring.md` row "Cost C–D → Wrap with budget hook".

Concrete: vendor the 2–3 agents you actually want into your own
`agents/` directory. **Don't install the whole marketplace.** A 191-surface
plugin in your config is a Simp F regardless of how good any individual agent
is.

This is the framework's "cherry-pick" archetype — the move that converts a
broad marketplace into a curated few.
