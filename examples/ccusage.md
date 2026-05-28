# ccusage

**Source:** https://github.com/ryoppippi/ccusage
**Type:** Local CLI / cost analyzer
**Project context assumed:** Every Claude Code project.

## Surface

A local script that reads `~/.claude/projects/*.jsonl` and aggregates token use
and cost per session, per day, per project. Stateless. No network.

## Smells

None.

## Scores

**Use case:** Local cost analyzer — makes the Cost gate enforceable by surfacing
the actual token spend per session.

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | A+ | Reads local JSONL files; output is human-readable; full source on GitHub |
| Cost | A+ | Local CLI; zero per-call cost; itself helps reduce overall Cost |
| Simp | A+ | Single binary, one command, no config |
| Corr | A+ | Deterministic aggregation of authoritative local data |

## Recommendation

**Buy** — every project should have this on day one. No matrix row triggers a
stricter recommendation; this is the framework's "no-brainer" archetype.

The right move is **default-on**: alias it into the shell, run it weekly.
