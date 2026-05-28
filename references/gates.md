# The four gates

Score every candidate tool on **four gates**. Each gate gets a **letter** from
**A+ · A · B · C · D · F**. Bigger is always better, on every gate. A `Cost` of A+
means *cheap*; a `Cost` of F means *expensive*.

The four gates are intentionally not comparable to each other. Don't sum, don't
average. **One failing gate = drop the tool**, regardless of how it scores
elsewhere. Engineering lives in the threshold, not in the aggregate.

---

## The gates

- **Obs ▸ Observability & Ownership.** How it works *inside*. Scannable? Auditable
  supply chain? No black boxes, no unapproved external LLMs? *If you can't observe
  it, you don't own it.*
- **Cost.** $/request, $/run, **tokens too**. The fast modes are great and
  expensive. Cost includes context amplification.
- **Simp ▸ Simplicity & Maintainability.** Will it make sense in 3 months? Can a
  teammate run it without you in the room?
- **Corr ▸ Correctness of Output.** Deterministic-enough? Verifiable?
  **Falsifiable?** Or running on faith?

A project may legitimately add **one fifth gate** — Ethics, Privacy, Latency,
Compliance — when its profile demands it. Don't add a fifth lightly; each gate adds
friction to every audit. If the fifth dimension's mitigation is identical to an
existing gate's, fold it in instead.

---

## The letter scale

| Letter | Meaning |
|--------|---------|
| **A+** | Exemplary ▸ best-in-class on this gate |
| **A**  | Good ▸ a strong reason to pick it |
| **B**  | Acceptable ▸ within budget for most projects |
| **C**  | Mediocre ▸ wouldn't pick *for this reason* |
| **D**  | Poor ▸ noticeably weak |
| **F**  | Failure ▸ a clear miss; drop it for this use case |

**Can't decide A or B?** Pick B. **Can't decide D or F?** Pick F. The letter forces
a verdict; the *gap* between letters is the signal.

---

## Scores are per-use-case, not per-tool

The single most important thing about this rubric: **the same tool gets different
letters for different use cases**.

- `CLAUDE.md` tight (under 200 lines, conventions only) ▸ A+/A/A+/A.
- `CLAUDE.md` bloated (500+ lines, conflicting rules, big imports) ▸ C/D/C/D.

Same primitive. Same docs. Different use case → very different scores. When you
audit a tool, you are not auditing the tool in the abstract — you are auditing **a
tool for a specific use**. Name the use case in the audit file. If two use cases
apply, score them separately.

---

## Per-gate rubrics

### Obs ▸ Observability & Ownership

| Letter | Profile |
|--------|---------|
| A+ | Local, open source, fully scannable. Logs everything. No hidden LLM. |
| A | Mostly open. Logs available. External calls documented. |
| B | Closed but well-documented. Audit trail exists if you ask. |
| C | Closed; you can see *that* it ran but not *what* it did. |
| D | Black box. Vendor-controlled prompt or model. Logs only on vendor side. |
| F | Black box *and* trains on your inputs, *or* arbitrary external LLM with no opt-out. |

### Cost

| Letter | Profile |
|--------|---------|
| A+ | Free or flat-fee. No per-call charge. No context amplification. |
| A | Cheap per-call, predictable. Bounded context returned. |
| B | Per-call, bounded but non-trivial. Most projects can absorb. |
| C | Per-call with mild amplification (returns multi-KB blobs into context). |
| D | Per-call and **context-amplifying** without a cap, or a paid fast mode. |
| F | Per-call, unbounded recursion possible (agent calls agent), or per-token billed by vendor on their model. |

### Simp ▸ Simplicity & Maintainability

| Letter | Profile |
|--------|---------|
| A+ | One config line. Zero state. Anyone on the team can debug at 3am. |
| A | A handful of config lines. Standard surface. Documented well. |
| B | Some moving parts but they're in one place. A junior could learn in a day. |
| C | Multiple chained primitives. Behaviour depends on order. |
| D | Chained, undocumented, brittle. Breaks on version bumps. |
| F | Requires the original author present to operate or debug. |

### Corr ▸ Correctness of Output

| Letter | Profile |
|--------|---------|
| A+ | Deterministic. Same input → same output. Falsifiable by a test. |
| A | Probabilistic with schema validation and self-checks. Failures are loud. |
| B | LLM-generated with hard guardrails. Output is reviewable before it acts. |
| C | LLM-generated; correct enough; verification is manual and expensive. |
| D | LLM-generated; no verification; failures are silent. |
| F | LLM-generated; irreversible side effects on the first wrong answer. |

---

## Producing the Scores table

Every audit (and every example file) ends with this canonical table. The
`scripts/compare-scores.py` parser depends on the exact format.

```markdown
## Scores

**Use case:** <one-line description — required, scores are per-use-case>

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | A  | <one sentence> |
| Cost | C  | <one sentence> |
| Simp | A+ | <one sentence> |
| Corr | A  | <one sentence> |
```

Pin column names. Letters only — never numbers. Justifications stay to one sentence
each so the table is readable on a slide.

If a project has chosen to add a fifth gate, append it as the last row with the
same format. Document which fifth gate the project uses in `budget.md`.

---

## The threshold mindset

Set a **budget per gate**, project by project:

- A customer-data product: `Obs ≥ A`, `Corr ≥ A+` are mandatory; `Cost` looser.
- A 5-minute meetup demo: `Simp ≥ A`, `Cost ≥ B`; `Obs` and `Corr` looser.

Then audit each candidate. If it falls below budget on *any* gate, drop it. **One
failing gate = noise.**

This is the entire point of using letters rather than a number you can sum. The
gates measure different things; a great `Corr` does not buy back a failing `Obs`.
The right move is to *raise* the failing score with a tactic — vendor the tool,
wrap it in a hook, version-lock it — or to walk away.

See `vendoring.md` for the tactic-to-gate matrix.
