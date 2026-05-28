# Sub-agents ▸ verbose-task isolation

**Source:** https://code.claude.com/docs/en
**Type:** First-party primitive
**Install:** N/A — markdown files defining the sub-agent
**Project context assumed:** Project with verbose, parallelizable work that
would otherwise pollute the main context.

## Surface

Markdown file with a name, description, and tool allowlist. Spawned by the
parent session; gets its own context window; returns only a summary. The
parent never sees the sub-agent's verbose output.

## Smells

None per se. Cost is sensitive to use case:
- **Cost amplification.** Many sub-agents in parallel multiply per-turn cost.

## Scores

**Use case:** Isolating verbose research / multi-file refactoring / exploration
into a sub-agent so the main context stays clean — *not* the PR-review use case
(see `pr-review-toolkit.md` for that scoring).

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | A  | First-party; the sub-agent definition is in the repo; its actions are visible while it runs |
| Cost | A  | Bounded work scope; cost is one fan-out, not a swarm |
| Simp | B  | An extra layer to debug; "did the agent or its parent decide X?" is a real question |
| Corr | A+ | Bounded jobs with summary returns are highly verifiable |

## Recommendation

**Buy** for isolated verbose work; **Wrap** if your sub-agent itself uses tools
that need gating (apply the same hook/allowlist treatment as for MCP servers).

This is the *non-PR-review* use case. The fan-out PR review use scores
A/C/C/A+ (see `pr-review-toolkit.md`) because Cost and Simp degrade with parallel
specialists. Same primitive, different use, different scores.
