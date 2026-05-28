# Slack MCP

**Source:** Anthropic-hosted MCP server, OAuth-based
**Type:** MCP server (hosted, OAuth bearer)
**Install:** **Hosted, OAuth click-through** ▸ no local code. Runtime auth-scope smell does the damage, not install.
**Project context assumed:** Internal product, multi-month horizon, business data.

## Surface

Channel listing, message search, message send, thread reply, file upload, user
lookup, label management. Gated behind an OAuth flow (`authenticate`,
`complete_authentication`); the post-auth surface includes write operations.

Auth: full Slack OAuth scopes including `chat:write`, `channels:read`,
`groups:read`. Side effects: sending a message is **irreversible** and
**externally visible**.

## Smells

- **Auth scopes ≫ used scopes.** Read-only use cases inherit `chat:write`.
  **Knock: −1 Obs.**
- **Hidden side effects** in `label_thread`, `mark_thread_read`, etc. Documented,
  but easy to invoke accidentally. **Knock: −1 Obs, −1 Corr.**

## Scores

**Use case:** Ops/on-call automation — reading channel state and posting status
updates, scoped to one bot user.

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | C  | Third-party hosted; broad OAuth scopes inherited; two knocks bring from A to C |
| Cost | A  | Slack API is per-seat (already paid); MCP overhead flat |
| Simp | A  | Slack is daily-driver for almost every team; debugging well-understood |
| Corr | B  | API is well-specified, but the LLM decides recipient/channel; knock applied |

## Recommendation

**Wrap** — `vendoring.md` row "Public-facing → Corr below budget" (any
message-send tool is essentially public from the project's POV).

Concrete: split into two MCP configurations. A read-only one (always on,
`channels:read` + `search:read` only) and a write-enabled one (loaded only when
the user explicitly opts in for the session, with a `PreToolUse` hook that
requires confirmation and shows the rendered message preview).

For ops/on-call specifically, scope the bot's OAuth to one channel. The Obs knock
disappears with a narrow scope.
