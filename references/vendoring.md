# Vendoring strategy ▸ raising scores or walking away

For every tool a project might depend on, there are five sane answers: **Build**,
**Buy**, **Wrap**, **Vendor**, **Defer**. The auditor recommends one based on
which gate is failing the project's budget.

This rubric distinguishes **Wrap** (constrain the live vendor tool) from
**Vendor** (mirror a known-good copy in your own infra). Both raise Obs; only
Vendor raises Simp.

## The five options

### Build

Write it yourself. A hook, a script, a small skill, an in-repo MCP server.

**When**: Simp budget is binding and the vendor tool is C or worse; or Obs budget
is binding and no available tool clears it; or the surface is small enough that
"build" is fewer lines than "configure."

**Cost**: engineering time up front, no recurring fee, no black box.

### Buy

Adopt the third-party tool as-is. Pay, integrate, accept the vendor's roadmap.

**When**: every gate clears budget as-is. Always the default for commodity work.

**Cost**: $$ ongoing.

### Wrap

Adopt the third-party tool *but constrain it*. Restrict its tool list with an
allowlist, put it behind a `PreToolUse` hook, only expose it inside a sub-agent.
The most common recommendation when the tool is useful but black-boxy.

**Raises**: Obs by 1 letter (if the wrapper is in your repo). Sometimes Corr.

**When**: Obs or Corr fails budget but the rest of the tool is strong; the surface
is small enough that the wrapper is maintainable.

### Vendor

Pin a known-good version of the tool in your own infra. Mirror the MCP server,
fork the plugin, version-lock the binary.

**Raises**: Obs by 1 letter. Simp by 1 letter (you control the upgrade cadence).
Cost typically drops 1 letter (you operate it).

**When**: Obs failure cannot be fixed by wrapping (vendor-controlled prompt/model
smell), or the project's horizon makes vendor-roadmap risk intolerable.

### Defer

Don't decide yet. Use a stub, a shell script, or no tool. Revisit when the project
has actual usage data.

**When**: project is < 1 week old, or you can't answer the project-side question
on any one of the four gates. Premature tool choice is more expensive than ten
extra `echo` statements.

**Cost**: opportunity cost only.

## Tactic ▸ gate matrix

Use this table to pick a tactic when a gate fails budget. The matrix is the
"how do I raise a failing score" lookup.

| Failing gate | Tactic | Effect |
|--------------|--------|--------|
| Obs is D or F | **Vendor** | +1 Obs, +1 Simp, −1 Cost |
| Obs is D or F (small surface) | **Wrap** with PreToolUse hook | +1 Obs |
| Cost is D or F | **Wrap** with budget hook (rate-limit, summarise) | +1 Cost |
| Cost is D or F (per-token vendor model) | **Build** alternative or **Defer** | replaces tool |
| Simp is D or F | **Build** or pick a different tool | replaces tool |
| Corr is D or F (irreversible side effects) | **Wrap** behind confirmation hook | +1 Corr |
| Corr is D or F (verification too expensive) | **Defer** until you have a test harness | — |

When two tactics could apply and disagree, the stricter wins:
`Reject > Build > Vendor > Wrap > Defer > Buy`.

## Decision matrix ▸ project signal × tool signal

The recommender combines the gate scores with the project's profile:

| Project signal | Tool signal | → Recommendation |
|----------------|-------------|------------------|
| Cost-sensitive budget (≥ A) | Cost D or F | **Wrap** (budget hook) or **Defer** |
| Public-facing (Corr ≥ A required) | Corr D or F | **Wrap** behind confirmation or **Build** |
| Regulated data (Obs ≥ A required) | Obs D or F | **Vendor** or reject |
| Prototype, < 2 weeks | Any | **Buy** if available, **Defer** otherwise |
| Multi-year product | Any gate at D or below | **Vendor** or **Build** |
| Can't fill scores on 3+ gates | Any | **Defer** until you can |

## How the budget planner uses this

Per gate, the planner produces a sentence like:

> Obs: project requires ≥ A. Any candidate scoring D or below must be **Vendored**
> before adoption. Allocate 15% of integration time per third-party tool for
> vendoring (mirror repo, version-lock, internal docs).

The percentage ("15%") is an estimate, not a forecast. Encoding it makes the
budget a *constraint*, not a wish.
