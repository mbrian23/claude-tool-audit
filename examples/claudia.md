# claudia

**Source:** https://github.com/getAsterisk/claudia
**Type:** Desktop GUI / session manager (Tauri)
**Project context assumed:** Teams that prefer a dashboard alongside the CLI.

## Surface

Local Tauri app. Reads the same session state Claude Code writes to disk. No
network calls beyond what the CLI itself makes. Provides visualisation for
sessions, agents, and MCP servers.

## Smells

None — local-first, observable, no hidden LLM calls.

## Scores

**Use case:** Visual dashboard for a team that wants to see all running sessions
and agent state at a glance, while keeping the CLI as the primary interface.

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | A  | Local app, reads local state; open source |
| Cost | A+ | Free, no runtime cost (just memory for the app) |
| Simp | A  | Standard desktop install; another piece of UI to keep in sync with the CLI |
| Corr | A  | Display layer only; correctness is bounded by what Claude Code writes to disk |

## Recommendation

**Buy** — `vendoring.md` row "Every gate clears budget as-is".

Useful for teams that prefer a dashboard. The CLI stays primary; claudia is the
inspection lens. For solo users, **Defer** — the CLI's own output is usually
sufficient.
