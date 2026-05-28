---
name: audit-tool
description: Walks the user through auditing one candidate tool (MCP server, hook, sub-agent, skill, third-party CLI) against the four gates. Interactive by default. Produces a scored markdown file the compare-scores script can parse. Use when the user invokes "/claude-tool-audit:audit-tool", asks to "audit a tool", "score this MCP server", or "evaluate adding X to my Claude Code project".
argument-hint: "[tool-name or description]"
allowed-tools: ["Read", "Write", "Bash", "AskUserQuestion", "WebFetch"]
version: 0.1.0
---

# Audit one tool

Score a single candidate tool against the four gates in
`${CLAUDE_PLUGIN_ROOT}/references/gates.md`. **Interactive by default** — the
audit's value is the *per-gate justification*, not the final letters.

## Inputs

- A tool name or short description in `$ARGUMENTS`.
- Optionally, a link to the tool's docs / MCP server repo / vendor page.
- **The intended use case.** Required. The same tool scores differently for
  different uses; an audit without a named use case is invalid.

If `$ARGUMENTS` is empty, ask the user which tool to audit. Always ask the use
case if not provided.

## Procedure

### 1. Establish project context and use case

Use AskUserQuestion to anchor two things:

> What's the project this tool would go into?

Offer:
- "A prototype, < 2 weeks horizon"
- "An internal product, multi-month horizon"
- "A public-facing product, multi-year horizon"

Then:

> Which use case are we scoring? (Same tool, different use, different scores.)

Capture the use case in one sentence. Name it explicitly — e.g. "Playwright MCP
for nightly visual-regression in CI" is a different audit than "Playwright MCP for
interactive debugging in a dev session."

### 2. Enumerate the tool's surface

**First, the install-time check** (this comes before everything else):

- What command installs the tool? (`npm install`, `pip install`, `git clone +
  /plugin install`, a curl-pipe-shell, etc.)
- Does install run any code — a `postinstall` script, a `setup.py`, a bootstrap
  binary, a vendor's launcher?
- Is that code readable before it runs? Pinnable by version / SHA?
- If the install path itself is a black box, **stop scoring** and report it.
  The Obs gate cannot be A+ when install is opaque.

Capture as a one-line `**Install:**` field in the audit file.

**Then enumerate the runtime surface**:

If the candidate is an MCP server:

- Read its docs or `tools/list` if available.
- List the actual tool names exposed.
- Note any side effects in tool descriptions.
- Note any auth scopes requested.

If the candidate is a hook, skill, sub-agent, or CLI:

- Identify the events / triggers it fires on.
- Identify what it reads and writes.
- Identify whether it spawns LLM calls.

Black-box smells from `${CLAUDE_PLUGIN_ROOT}/references/black-box-risks.md` apply
here — including the **install-time** smell which knocks Obs by −1 (postinstall
readable) or −2 (no audit possible). Apply at most one knock per smell.

### 3. Score the four gates

Walk through them in order — **Obs, Cost, Simp, Corr**. For each gate:

1. Restate the gate's question from `gates.md`.
2. Pick a letter from A+ · A · B · C · D · F. Use the per-gate rubric in
   `gates.md`. Can't decide A or B? Pick B. Can't decide D or F? Pick F.
3. Write the justification in one sentence.

Then apply:

- **At most one knock per black-box smell** (per `black-box-risks.md`).
- **The strictest Cost cap** that applies (per `cost-risks.md`).

If the project has chosen to add a fifth gate (Ethics / Privacy / Latency /
Compliance), score it too with the same scale.

Use AskUserQuestion when the project context is non-obvious. Otherwise score and
explain reasoning inline, and ask only when a gate is genuinely ambiguous.

### 4. Produce the recommendation

Use the matrices in `${CLAUDE_PLUGIN_ROOT}/references/vendoring.md` to pick
**Build / Buy / Wrap / Vendor / Defer / Reject**.

State which row of the matrix matched. If two match and disagree, the stricter
recommendation wins: `Reject > Build > Vendor > Wrap > Defer > Buy`.

If the recommendation is **Wrap**, propose a concrete wrapping mechanism:
- a `PreToolUse` hook that filters,
- an MCP `disabledTools` allowlist,
- a sub-agent isolation,
- or a budget-aware hook that counts calls per turn.

If the recommendation is **Vendor**, propose where the vendored copy lives and
what its upgrade cadence will be.

### 5. Write the audit file (on request)

If the user agreed to persist the audit, write it to
`${CLAUDE_PLUGIN_ROOT}/examples/<tool-slug>__<use-case-slug>.md` (when shipping
as a plugin example) or a user-specified path (for project-local audits).

Otherwise present inline and stop.

## Output template

```markdown
# <Tool name>

**Source:** <link>
**Type:** <MCP server / hook / sub-agent / CLI / other>
**Install:** <one line — what runs at install time, is it readable, pinnable>
**Project context assumed:** <prototype / internal / public-facing>

## Surface

- <bulleted list of tools / events / IO>

## Smells

- <each triggered smell from black-box-risks.md, with the knock applied>

## Scores

**Use case:** <one-line description>

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | <A+/A/B/C/D/F> | <one sentence> |
| Cost | <A+/A/B/C/D/F> | <one sentence> |
| Simp | <A+/A/B/C/D/F> | <one sentence> |
| Corr | <A+/A/B/C/D/F> | <one sentence> |

## Recommendation

**<Build / Buy / Wrap / Vendor / Defer / Reject>** — <matrix row that matched>.

<If Wrap or Vendor: the concrete mechanism.>
```

Pin the table column names and order. Letters only.

## When to load other references

- `gates.md` is non-negotiable. It defines the scale.
- `black-box-risks.md` whenever step 2 surfaces > 5 undocumented tools, any
  unexplained scope, or any vendor-controlled prompt/model.
- `cost-risks.md` whenever the tool returns blobs, spawns LLM calls, or is priced
  per-call.
- `vendoring.md` at step 4 to look up the recommendation row and the tactic.

## Don't

- Don't fabricate scores when the surface is unknown. Score honestly — an F with
  the justification "could not enumerate the tool surface" is better than a
  fabricated A.
- Don't sum or average the four letters. The gates are not comparable.
- Don't audit "the tool" — audit "the tool *for this use case*." The use-case
  line in the Scores table is required.
- Don't skip the recommendation. A scored audit with no Build/Buy/Wrap/Vendor/
  Defer/Reject is half an answer.
