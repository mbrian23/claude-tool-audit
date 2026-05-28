# ruvnet/claude-flow

**Source:** https://github.com/ruvnet/claude-flow
**Type:** Multi-agent swarm orchestration (314 MCP tools)
**Project context assumed:** Anything beyond a research demo.

## Surface

A swarm orchestrator that exposes ~314 MCP tools. Agents call agents call agents.
Heavy. Opinionated. Vendor-controlled prompts inside the swarm.

## Smells

- **Tool surface ≫ docs.** 314 tools, README explains a handful. **Knock: −1 Obs.**
- **Agent recursion.** Swarm-of-swarms — call count is not bounded by user
  intent. **Cost capped at F** per `cost-risks.md`.
- **Vendor-controlled prompt/model.** The orchestrator's internal prompts shape
  every sub-agent. **Knock: −1 Obs, −1 Cost.**

## Scores

**Use case:** Multi-agent swarm orchestration for an exploratory research demo.

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | D  | 314-tool surface, vendor-controlled internal prompts; two knocks bring from B to D |
| Cost | F  | Swarm-of-swarms recursion with no stop condition; cap and knock both apply |
| Simp | D  | Heavy install, opinionated config, debugging requires understanding the orchestrator |
| Corr | D  | LLM-generated all the way down; no verification layer surfaced |

## Recommendation

**Reject** — `vendoring.md` row "Failing gate threshold cannot be raised by Wrap or Vendor".

Two failing gates simultaneously (Obs and Cost). **No averaging.** The "drop"
rule fires. This is the framework's canonical "no, don't add it" example.

For research-only demos where the goal *is* the swarm: **Defer** any production
adoption decision until a representative trace exists and the call-count is
bounded.
