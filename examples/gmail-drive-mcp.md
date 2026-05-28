# Gmail / Drive MCP (claude.ai-hosted)

**Source:** Anthropic claude.ai built-in MCP
**Type:** MCP server (hosted, OAuth bearer)
**Project context assumed:** Personal use only — **forbidden for client / business data**.

## Surface

OAuth-gated. Post-auth surface: list/read/search messages, files, threads;
manage labels; create drafts. Substantial.

## Smells

- **Auth scopes ≫ used scopes** — Gmail OAuth scopes cover the entire mailbox by
  default. **Knock: −1 Obs.**
- **Vendor-controlled retrieval** — `search_threads` returns ranked results; the
  ranking is on Anthropic's side. **Knock: −1 Obs.**

## Scores

**Use case:** Personal email and document automation on a personal account — not
business / client data.

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | D  | Hosted on Anthropic's side; full mailbox scope; two knocks bring from B to D |
| Cost | A  | Free with claude.ai subscription; flat overhead |
| Simp | A+ | OAuth click-through; no install; works immediately |
| Corr | A  | Gmail/Drive APIs are precise; LLM choice of recipient/file is the variable |

## Recommendation

**Buy** for personal use; **Reject** for client / business data — `vendoring.md`
row "Regulated data → Obs D/F".

The Obs failure cannot be raised by wrapping (it's a hosted vendor surface, not
your code). The correct move on regulated data is to **not adopt** until either
the scopes can be narrowed or a self-hosted alternative exists.
