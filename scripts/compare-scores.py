#!/usr/bin/env python3
"""Compare letter Scores tables across every audit in examples/.

Reads every *.md file under examples/ (relative to the plugin root), extracts the
"## Scores" markdown table, and prints a comparison matrix.

The rubric uses **letters** (A+ A B C D F) across four gates (Obs Cost Simp Corr).
Letters are ordinal, not interval — the script does NOT sum, average, or rank.
It prints the per-gate letters side-by-side and flags each tool's worst gate so
the user can see "one failing gate = drop" at a glance.

Expected per-file table format (from references/gates.md):

    ## Scores

    **Use case:** <one-line description>

    | Gate | Score | Justification |
    |------|-------|---------------|
    | Obs  | A  | ... |
    | Cost | C  | ... |
    | Simp | A+ | ... |
    | Corr | A  | ... |

The parser is intentionally strict: a file that doesn't match the format is
reported, not silently skipped.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

GATES = ["Obs", "Cost", "Simp", "Corr"]
LETTERS = ["A+", "A", "B", "C", "D", "F"]  # best → worst
LETTER_RANK = {letter: rank for rank, letter in enumerate(LETTERS)}

SCORES_HEADING = re.compile(r"^##\s+Scores\s*$", re.MULTILINE)
USE_CASE = re.compile(r"^\*\*Use case:\*\*\s*(.+?)\s*$", re.MULTILINE)
ROW = re.compile(r"^\|\s*([A-Za-z][A-Za-z+ ]*?)\s*\|\s*(A\+|[ABCDF])\s*\|\s*([^|]*?)\s*\|\s*$")


@dataclass
class AuditFile:
    path: Path
    name: str
    use_case: str = ""
    scores: dict[str, str] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)

    @property
    def worst_gate(self) -> tuple[str, str] | None:
        if not self.scores:
            return None
        worst = max(self.scores.items(), key=lambda kv: LETTER_RANK[kv[1]])
        return worst


def parse(path: Path) -> AuditFile:
    text = path.read_text(encoding="utf-8")
    af = AuditFile(path=path, name=path.stem)

    m = SCORES_HEADING.search(text)
    if not m:
        af.errors.append("no '## Scores' heading")
        return af

    body = text[m.end():]

    uc = USE_CASE.search(body)
    if uc:
        af.use_case = uc.group(1)
    else:
        af.errors.append("missing '**Use case:**' line — scores are per-use-case, this is required")

    for line in body.splitlines():
        if line.startswith("##"):
            break
        row = ROW.match(line)
        if not row:
            continue
        gate, letter, _ = row.groups()
        gate = gate.strip()
        if gate in {"Gate", "------"}:
            continue
        if gate not in GATES:
            af.errors.append(f"unknown gate {gate!r}")
            continue
        af.scores[gate] = letter

    missing = [g for g in GATES if g not in af.scores]
    if missing:
        af.errors.append(f"missing gates: {', '.join(missing)}")
    return af


def render(files: list[AuditFile]) -> str:
    name_w = max((len(f.name) for f in files), default=4)
    name_w = max(name_w, len("Tool"))
    gate_w = 4
    header_cells = [f"{'Tool':<{name_w}}"] + [f"{g:>{gate_w}}" for g in GATES] + [f"{'Worst':>6}", "  Use case"]
    header = "  ".join(header_cells)
    sep = "-" * len(header)
    lines = [header, sep]
    for f in files:
        if f.errors:
            continue
        worst = f.worst_gate
        worst_str = f"{worst[1]} ({worst[0]})" if worst else ""
        row_cells = [f"{f.name:<{name_w}}"]
        for g in GATES:
            row_cells.append(f"{f.scores[g]:>{gate_w}}")
        row_cells.append(f"{worst_str:>6}")
        uc = (f.use_case[:60] + "…") if len(f.use_case) > 61 else f.use_case
        row_cells.append(f"  {uc}")
        lines.append("  ".join(row_cells))
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parent.parent
    examples = root / "examples"
    if not examples.is_dir():
        print(f"no examples/ directory at {examples}", file=sys.stderr)
        return 1

    files = [parse(p) for p in sorted(examples.glob("*.md")) if not p.name.startswith("_")]
    if not files:
        print(f"no example files found in {examples}", file=sys.stderr)
        return 1

    ok = [f for f in files if not f.errors]
    bad = [f for f in files if f.errors]

    print(render(ok))
    print()
    print(f"Parsed {len(ok)} / {len(files)} files cleanly.")
    print("Worst-gate column flags candidates for drop under a strict threshold (no averaging).")
    if bad:
        print("\nFiles with parse errors:")
        for f in bad:
            print(f"  {f.name}:")
            for err in f.errors:
                print(f"    - {err}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
