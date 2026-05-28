---
name: budget-planner
description: Helps the user set per-gate budgets for a new Claude Code project — Obs, Cost, Simp, Corr, and optionally a fifth gate — and recommends a vendoring strategy. Interactive scoping by default, optionally writes budget.md and vendoring.md into the project. Use when the user invokes "/claude-tool-audit:budget-planner", asks to "plan a Claude Code budget", "decide my tooling budget", "scope a new Claude Code project", or "figure out what to buy vs build vs vendor".
argument-hint: "[optional: project name or one-line description]"
allowed-tools: ["Read", "Write", "AskUserQuestion", "Bash"]
version: 0.1.0
---

# Plan the per-gate budget

Turn a project scope into a **letter threshold per gate** and a vendoring strategy
per category. **Interactive by default** — the conversation is the deliverable;
file output is optional.

## Inputs

- Optional one-line project description in `$ARGUMENTS`.
- The rubric in `${CLAUDE_PLUGIN_ROOT}/references/gates.md`.
- The vendoring matrix in `${CLAUDE_PLUGIN_ROOT}/references/vendoring.md`.

## Procedure

### 1. Scope the project

Use AskUserQuestion. Ask these in one batch:

1. **Horizon** — prototype (< 2 weeks), internal product (months), or public
   product (years)?
2. **Audience** — internal (1–10), team (10–500), or public (500+)?
3. **Data sensitivity** — synthetic / public, business, or regulated/PII?
4. **Latency profile** — interactive (sub-second), batch (minutes OK), or
   background (hours OK)?
5. **Fifth gate?** — Ethics, Privacy, Latency, or Compliance. Pick at most one
   that *changes a decision* the four gates don't already cover.

State the implied project-side budgets back to the user before continuing, so
they can correct mistakes.

### 2. Per-gate budget

For each of the four gates (plus any fifth), produce one paragraph with three
sentences:

1. **Threshold** — the minimum letter a candidate must score on this gate (e.g.
   "Obs ≥ A for any tool that touches customer data").
2. **Headroom** — how much budget to reserve for surprises. For Cost, use the
   60/20/20 rule from `${CLAUDE_PLUGIN_ROOT}/references/cost-risks.md`.
3. **Default tactic** — for tools below the threshold, the row from
   `vendoring.md` that applies (Build / Vendor / Wrap / Defer).

Don't expand on gates where the project's answer is permissive (e.g. Cost for a
small internal tool). One line is enough there.

### 3. Risk mitigations

Surface, by name, the mitigation patterns the project should already plan:

- **PreToolUse budget hook** — when Cost threshold is binding (≥ A).
- **Tool allowlist on MCP servers** — when Obs threshold is binding (≥ A).
- **Sub-agent isolation** — for any third-party tool that triggers a black-box
  smell from `black-box-risks.md`.
- **In-repo wrapper / vendored copy** — for any vendor tool the project wants to
  keep swappable.
- **Permission audit** — for any project with public audience or regulated data.
  Promote `ask` for any tool whose Obs falls below threshold.

For each surfaced mitigation, suggest *where it would live* (which hook event,
which plugin, which sub-agent file). Concrete > generic.

### 4. Write to disk (on request)

Ask: "Save the budget to the project? (writes `budget.md` and `vendoring.md`)"

If yes, write to the project root (or `./docs/` if that exists):

- `budget.md` — sections per gate with threshold / headroom / default-tactic.
- `vendoring.md` — recommended strategy per category and mitigations.

If no, present inline and stop.

## Output template (for budget.md)

```markdown
# <Project name> ▸ Tooling budget

Horizon: <prototype / internal / public>
Audience: <size>
Data sensitivity: <synthetic / business / regulated>
Latency profile: <interactive / batch / background>
Fifth gate: <Ethics / Privacy / Latency / Compliance / none>

## Per-gate budget

### Obs ▸ Observability & Ownership
- Threshold: any candidate must score ≥ <letter>
- Headroom: <one sentence>
- Default tactic if below: <Build / Vendor / Wrap / Defer>

### Cost
- Threshold: ≥ <letter>
- Headroom: 60% forecast / 20% amplification / 20% added tools
- Default tactic if below: <…>

### Simp ▸ Simplicity & Maintainability
- Threshold: ≥ <letter>
- Headroom: <…>
- Default tactic if below: <…>

### Corr ▸ Correctness of Output
- Threshold: ≥ <letter>
- Headroom: <…>
- Default tactic if below: <…>

<If fifth gate chosen, add a section with the same shape.>

## Risk mitigations to plan

- <mitigation 1, with location>
- <mitigation 2, with location>
- <mitigation 3, with location>
```

## Output template (for vendoring.md)

```markdown
# <Project name> ▸ Vendoring strategy

| Category | Strategy | Reason |
|----------|----------|--------|
| MCP servers | <Build / Buy / Wrap / Vendor / Defer> | <one sentence> |
| Sub-agents | ... | ... |
| Hooks | ... | ... |
| Skills | ... | ... |
| Third-party CLIs | ... | ... |
| Permission auto-allow | ... | ... |
```

## Don't

- Don't recommend a threshold you can't justify against the rubric. If the user
  pushes back, walk through the gate's per-letter rubric in `gates.md` rather
  than rounding.
- Don't produce a budget without mitigations. A threshold without a planned
  mitigation is a wish.
- Don't write files without explicit confirmation. The conversation is the
  default.
- Don't propose more than one fifth gate. The framework explicitly limits it to
  four "with optional 5th." Adding more dilutes the threshold mindset.
