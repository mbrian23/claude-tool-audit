# Context7 MCP

**Source:** https://github.com/upstash/context7
**Type:** MCP server (hosted, HTTP)
**Install:** **Hosted, OAuth click-through** ▸ no local code execution at adoption. Obs unaffected by install path; runtime opacity is the issue.
**Project context assumed:** Internal product, multi-month horizon, business data.

## Surface

Two tools:

- `resolve-library-id` — maps a human library name to a Context7-internal ID.
- `query-docs` — returns documentation snippets for a given library ID and topic.

Auth: a Context7 API key (optional for low-volume use). Side effects: query is
logged on Context7's side for rate-limiting / analytics.

## Smells

- **Vendor-controlled retrieval.** The "current docs" claim is plausible but not
  audited per-call — the user can't see *which* doc version Context7 returned.
  **Knock: −1 Obs, −1 Cost.**
- **Context amplification.** `query-docs` returns multi-KB snippets with no
  token cap parameter. **Cost capped at C** per `cost-risks.md`.

## Scores

**Use case:** Live library docs for fast-moving APIs during development — better
than training-data memory; vendored copy planned for prod.

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | D  | Vendor chooses doc version; queries logged on their side; knock applied |
| Cost | C  | Free tier but returns multi-KB blobs with no cap; amplification cap |
| Simp | A+ | One config line, two tools, no operational complexity |
| Corr | A  | Doc content itself is from the actual source; correctness depends on Context7's indexing freshness |

## Recommendation

**Vendor** — `vendoring.md` row "Multi-year product → Obs D/F".

Concrete: mirror the Context7 index for production use, or replace with an
in-repo `docs/` grep for libraries the project actually depends on. The hosted
service is acceptable for development; in prod the Obs failure has to be raised
either by vendoring (pin a Context7 snapshot) or replacing with a deterministic
local docs cache.

For a prototype, **Buy** — the Obs failure is acceptable on a 2-week horizon.
