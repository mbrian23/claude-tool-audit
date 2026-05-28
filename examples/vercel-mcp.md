# Vercel MCP

**Source:** Vercel-hosted MCP server, OAuth-based
**Type:** MCP server (hosted, OAuth bearer)
**Project context assumed:** Internal product on Vercel, multi-month horizon, business data.

## Surface

OAuth-gated (`authenticate`, `complete_authentication`). Post-auth, the Vercel MCP
exposes deployment management, environment variable read/write, log queries,
domain listing, project metadata.

Auth: Vercel account scopes including team-level read and project-level write.
Side effects: env var changes propagate to deployments; deployment promotions
affect production traffic.

## Smells

- **Auth scopes ≫ used scopes.** Read-only use cases inherit project-level write.
  **Knock: −1 Obs.**
- **Hidden side effects.** Promoting a deployment is a single call that affects
  production traffic — documented, but agent-invokable. **Knock: −1 Corr.**

## Scores

**Use case:** Deploy automation in a Vercel-hosted project — log queries,
deployment promotion, env var management.

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | C  | Third-party hosted, broad scopes by default; knock applied |
| Cost | A  | Included with Vercel plan; MCP overhead flat |
| Simp | A  | Vercel API is well-documented; team already operates Vercel |
| Corr | B  | Vercel API is precise, but agent-driven deployment promotion is reversible-but-noisy; knock applied |

## Recommendation

**Wrap** — `vendoring.md` row "Multi-year product → Lock-in 1–2" (the tool *is*
the platform, lock-in is by choice).

The wrap here is about gating the write surface, not avoiding Vercel. Concrete:
two MCP configurations — read-only always on, write-enabled opt-in per session.
A `PreToolUse` hook that requires confirmation for any tool that mutates
production env or promotes a deployment.

For prototype projects on Vercel, **Buy** (use as-is) is acceptable. The Corr
knock matters less when there's no production traffic to disrupt.
