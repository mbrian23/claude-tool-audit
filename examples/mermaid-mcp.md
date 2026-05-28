# Mermaid MCP

**Source:** Local Mermaid renderer exposed as an MCP server
**Type:** MCP server (local stdio)
**Install:** **Local install** ▸ stdlib renderer; no postinstall surprises if installed from the canonical repo. Pinnable.
**Project context assumed:** Any project that needs diagrams in the IDE.

## Surface

Two tools: render a Mermaid source string to PNG/SVG; preview live during
iteration. Local rendering; no network calls.

## Smells

None.

## Scores

**Use case:** Rendering Mermaid diagrams for documentation and presentations
without leaving Claude Code.

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | A+ | Local rendering; output is a file you can inspect |
| Cost | A+ | Free, no per-call cost |
| Simp | A+ | One install, two tools, no config |
| Corr | A+ | Mermaid's grammar is deterministic; output is what the spec says it is |

## Recommendation

**Buy** — every project that needs diagrams should have this. Pair with the
`claude-mermaid` plugin for the editing skill.

The framework's "no-brainer" archetype for local-execution MCPs — the same
class as `permissions.md`, `ccusage.md`, `clear-command.md`.
