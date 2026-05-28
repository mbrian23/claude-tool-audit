---
name: audit-project
description: Scans the current repo's Claude Code setup — .claude/, plugin configs, .mcp.json, hooks.json, sub-agents, skills — and audits the portfolio against the four gates. Use when the user invokes "/claude-tool-audit:audit-project", asks to "audit my project's tools", "review my Claude setup", "check what's in .claude/", or "score everything we've added".
argument-hint: "[optional: path to project root, defaults to cwd]"
allowed-tools: ["Read", "Bash", "Glob", "Grep", "AskUserQuestion", "Write"]
version: 0.1.0
---

# Audit the whole project's tools

Audit the *portfolio* of tools a project has wired into Claude Code, not a single
candidate. Output: per-tool letter scores against the four gates plus a
portfolio-level view (redundancies, gaps, concentration risk).

## Inputs

- Project root in `$ARGUMENTS` (defaults to current working directory).
- The rubric in `${CLAUDE_PLUGIN_ROOT}/references/gates.md`.

## Procedure

### 1. Enumerate the surface

Discover what tools the project has wired in. Run in parallel:

```bash
# MCP servers
find <root> -name ".mcp.json" -not -path "*/node_modules/*" 2>/dev/null
# Plugin configs
find <root> -name "plugin.json" -path "*/.claude-plugin/*" 2>/dev/null
# Hooks
find <root> -name "hooks.json" -not -path "*/node_modules/*" 2>/dev/null
# Skills and sub-agents
find <root> -type d \( -name "skills" -o -name "agents" \) -not -path "*/node_modules/*" 2>/dev/null
# Permissions (auto-allow lists, the lightest fix in the decision framework)
find <root> -path "*/.claude/settings*.json" 2>/dev/null
# CLAUDE.md instructions that imply tool usage
find <root> -name "CLAUDE.md" -not -path "*/node_modules/*" 2>/dev/null
```

Read each file. Build a list of distinct tools/primitives the project depends on.

### 2. Classify and group

For each item discovered:

- **Type**: MCP server, hook, skill, sub-agent, slash command, third-party CLI,
  permission entry.
- **Trust origin**: this repo, an internal plugin, a marketplace plugin, a
  third-party MCP, an unknown OSS project.
- **Use case in this repo**: derive from where it's wired in. A hook with a
  `Bash(npm test:*)` matcher is "lint/test gating", not "all bash".

Flag anything in the auto-allow list — those bypass the user's approval, so they
need the strictest scoring.

### 3. Establish project context

Ask once:

> What's the project — prototype, internal product, or public-facing? Any
> regulated data? Latency-critical?

This sets the per-gate budget. Optionally surface the project's *fifth gate* if
one has been declared (Ethics / Privacy / Latency / Compliance).

### 4. Score each tool

For each distinct (tool, use case) pair, run the same procedure as `audit-tool`:

- Enumerate its surface.
- Apply black-box and cost-risk knocks.
- Produce the Scores table — Obs / Cost / Simp / Corr (+ fifth gate if any).

If the project has > 8 distinct tools, batch by category (MCPs first, then hooks,
then skills) and ask the user whether to score everything or only the high-risk
subset (third-party origin, in auto-allow list, or writes externally).

### 5. Portfolio view

After per-tool scoring, produce a portfolio summary:

- **Failing gates** — per-tool list of which gate fell below project budget. **One
  failing gate per tool = candidate for drop.** No averaging.
- **Redundancies** — two tools doing the same job. Recommend keeping the one with
  the better worst-gate score.
- **Concentration risk** — if > 50% of tools are from one vendor, flag it. Note
  the Lock-in implication even though Lock-in isn't a gate.
- **Black-box concentration** — count tools where any smell from
  `${CLAUDE_PLUGIN_ROOT}/references/black-box-risks.md` fired.
- **Auto-allow surprises** — permission entries that allowlist a tool whose Obs
  or Corr scores below project budget.

### 6. Recommendations

Per tool, use the matrices in `${CLAUDE_PLUGIN_ROOT}/references/vendoring.md`:
**keep / wrap / vendor / replace / drop**.

For the portfolio:

- At most three actions, ordered by leverage.
- Concrete, not aspirational ("remove the slack-mcp auto-allow entry" beats
  "improve governance posture").

## Output

Single markdown report. If the user wants it persisted, write it to
`<root>/.claude/audit-report.md` and ensure that path is gitignored. Otherwise,
present inline.

Sections:

1. Surface (the enumerated list with types and trust origins)
2. Per-tool scores (one canonical Scores table per (tool, use case) — same letter
   format as `audit-tool` so `compare-scores.py` can parse it)
3. Portfolio findings
4. Top three actions

## Don't

- Don't score internal hooks/skills the same way as third-party MCPs. The trust
  origin matters: an internal hook with `Bash` access is normal, a vendor MCP with
  the same access is a smell.
- Don't recommend "remove all third-party tools." The point is calibrated trust,
  not abstention.
- Don't merge use cases. A hook used for lint *and* for cost-auditing scores
  twice, not once.
