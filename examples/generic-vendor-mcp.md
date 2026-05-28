# Generic vendor-API MCP

**Source:** Pattern — any hosted MCP server fronting a vendor's REST/GraphQL API
**Type:** MCP server (hosted)
**Install:** **Varies** ▸ if hosted: OAuth click-through. If local: typically `npm install` — **always read the postinstall script** before adopting. Often the actual supply-chain risk.
**Project context assumed:** Internal product moving toward production.

## Surface

A hosted MCP server that wraps some vendor's API (the pattern, not a specific
product). Tools list, auth tokens, side effects vary per vendor.

## Smells

- **Vendor-controlled retrieval / prompt** by default for any "smart" tools.
  **Knock: −1 Obs.**
- **Auth scopes ≫ used scopes** are routine for vendor APIs (broad-scope OAuth
  tokens). **Knock: −1 Obs.**
- **Hidden side effects** — most vendor APIs log queries on their side.

## Scores

**Use case:** Quick integration with a vendor service during development — to
be replaced by an in-house wrapper before any production rollout.

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | D  | Hosted by vendor; broad scopes; logs on vendor side; two knocks bring from B to D |
| Cost | C  | Per-call to vendor + the LLM call surrounding it |
| Simp | A  | OAuth click-through; immediate value |
| Corr | C  | Vendor API contract may shift; LLM still chooses what to call with what arguments |

## Recommendation

**Vendor (or replicate) before prod** — `vendoring.md` row "Multi-year product → Obs D/F".

The development-phase recommendation is **Buy** with eyes open: useful for
prototyping, **not for prod**. The production move is to write an in-house
wrapper around the vendor's API directly, dropping the hosted MCP layer. That
wrapper raises Obs from D to A+ and Simp typically holds.

This is the cautionary archetype every vendor MCP audit should anchor to.
