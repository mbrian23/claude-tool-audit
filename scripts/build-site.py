#!/usr/bin/env python3
"""Generate docs/index.html from examples/*.md.

The output is a self-contained HTML page (single file, inline CSS, no JS deps)
listing every reviewed tool with its four letter scores, use case, recommendation,
and a link to the source audit on GitHub.

The page is meant to be served from GitHub Pages at
https://mbrian23.github.io/claude-tool-audit/ — usable as a QR-target during the
talk.
"""

from __future__ import annotations

import html
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

GATES = ["Obs", "Cost", "Simp", "Corr"]
LETTERS = ["A+", "A", "B", "C", "D", "F"]
LETTER_RANK = {letter: rank for rank, letter in enumerate(LETTERS)}
LETTER_CLASS = {"A+": "pp", "A": "p", "B": "eq", "C": "eq", "D": "m", "F": "mm"}

SCORES_HEADING = re.compile(r"^##\s+Scores\s*$", re.MULTILINE)
USE_CASE = re.compile(r"^\*\*Use case:\*\*\s*(.+?)\s*$", re.MULTILINE)
ROW = re.compile(r"^\|\s*([A-Za-z][A-Za-z+ ]*?)\s*\|\s*(A\+|[ABCDF])\s*\|\s*([^|]*?)\s*\|\s*$")
SOURCE = re.compile(r"^\*\*Source:\*\*\s*(.+?)\s*$", re.MULTILINE)
TYPE = re.compile(r"^\*\*Type:\*\*\s*(.+?)\s*$", re.MULTILINE)
INSTALL = re.compile(r"^\*\*Install:\*\*\s*(.+?)\s*$", re.MULTILINE)
RECO = re.compile(r"^\*\*(Build|Buy|Wrap|Vendor|Defer|Reject)\*\*", re.MULTILINE)
HEADING = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
GITHUB_RAW_BASE = "https://github.com/mbrian23/claude-tool-audit/blob/main/examples"


@dataclass
class Audit:
    path: Path
    slug: str
    title: str = ""
    source: str = ""
    type_: str = ""
    install: str = ""
    use_case: str = ""
    scores: dict[str, str] = field(default_factory=dict)
    recommendation: str = ""

    @property
    def worst(self) -> str:
        if not self.scores:
            return ""
        return max(self.scores.items(), key=lambda kv: LETTER_RANK[kv[1]])[1]


def parse(path: Path) -> Audit:
    text = path.read_text(encoding="utf-8")
    a = Audit(path=path, slug=path.stem)

    h = HEADING.search(text)
    if h:
        a.title = h.group(1)

    s = SOURCE.search(text)
    if s:
        a.source = s.group(1).strip()

    t = TYPE.search(text)
    if t:
        a.type_ = t.group(1).strip()

    i = INSTALL.search(text)
    if i:
        a.install = i.group(1).strip()

    m = SCORES_HEADING.search(text)
    if not m:
        return a
    body = text[m.end():]

    uc = USE_CASE.search(body)
    if uc:
        a.use_case = uc.group(1)

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
        if gate in GATES:
            a.scores[gate] = letter

    r = RECO.search(text)
    if r:
        a.recommendation = r.group(1)

    return a


def linkify_source(src: str) -> str:
    m = re.match(r"^(https?://\S+)", src)
    if m:
        url = m.group(1)
        return f'<a href="{html.escape(url)}" target="_blank" rel="noopener">{html.escape(url)}</a>'
    return html.escape(src)


def render_install(install: str) -> str:
    """Render the install line with light markdown emphasis preserved."""
    if not install:
        return ""
    s = html.escape(install)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return s


CSS = """
:root {
  --bg: #0a0c10;
  --fg: #e6e8ee;
  --muted: #8a93a6;
  --line: #1c2230;
  --team: #2ff3c8;
  --rival: #ff2e74;
  --gold: #ffd166;
  --green: #9ce374;
  --accent: #6aa3ff;
}
* { box-sizing: border-box; }
body {
  background: var(--bg);
  color: var(--fg);
  font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  margin: 0;
  padding: 32px;
  font-size: 14px;
  line-height: 1.5;
}
header {
  max-width: 1400px;
  margin: 0 auto 28px;
}
header h1 {
  font-size: 28px;
  margin: 0 0 4px;
  letter-spacing: -0.01em;
}
header .sub {
  color: var(--muted);
}
header .meta {
  margin-top: 14px;
  color: var(--muted);
  font-size: 13px;
}
header a { color: var(--accent); text-decoration: none; }
header a:hover { text-decoration: underline; }

main {
  max-width: 1400px;
  margin: 0 auto;
}

table.audits {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 32px;
}
table.audits th, table.audits td {
  padding: 10px 8px;
  border-bottom: 1px solid var(--line);
  vertical-align: top;
  text-align: left;
}
table.audits th {
  background: #11141b;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-size: 11px;
  font-weight: 500;
}
table.audits td.gate {
  text-align: center;
  width: 48px;
  font-weight: 600;
  font-size: 16px;
}
table.audits td.gate.pp { color: var(--team); text-shadow: 0 0 10px rgba(47, 243, 200, 0.6); }
table.audits td.gate.p  { color: var(--green); }
table.audits td.gate.eq { color: var(--gold); }
table.audits td.gate.m  { color: var(--rival); text-shadow: 0 0 8px rgba(255, 46, 116, 0.5); }
table.audits td.gate.mm { color: var(--rival); background: rgba(255, 46, 116, 0.12); text-shadow: 0 0 10px rgba(255, 46, 116, 0.8); }

td.tool a {
  color: var(--fg);
  text-decoration: none;
  font-weight: 600;
}
td.tool a:hover { color: var(--accent); }
td.tool .type { color: var(--muted); font-size: 11px; display: block; margin-top: 2px; }
td.usecase { color: var(--fg); min-width: 380px; }
td.usecase .install { display: block; color: var(--gold); font-size: 11px; margin-top: 6px; }
td.usecase .install code { font-size: 10px; background: rgba(255,209,102,0.08); padding: 1px 4px; border-radius: 2px; }
td.usecase .src { display: block; color: var(--muted); font-size: 11px; margin-top: 4px; word-break: break-all; }
td.usecase .src a { color: var(--muted); text-decoration: none; }
td.usecase .src a:hover { color: var(--accent); }
table.audits { table-layout: auto; }
table.audits td, table.audits th { white-space: normal; }
td.reco {
  font-weight: 600;
  text-align: center;
  width: 80px;
  font-size: 12px;
  letter-spacing: 0.04em;
}
td.reco.Buy    { color: var(--green); }
td.reco.Wrap   { color: var(--gold); }
td.reco.Vendor { color: var(--gold); }
td.reco.Build  { color: var(--accent); }
td.reco.Defer  { color: var(--muted); }
td.reco.Reject { color: var(--rival); }

.section-head {
  margin: 32px 0 12px;
  color: var(--muted);
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  border-bottom: 1px solid var(--line);
  padding-bottom: 6px;
}

.footer {
  margin-top: 32px;
  color: var(--muted);
  font-size: 12px;
}
.footer a { color: var(--accent); }
.legend {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  padding: 14px;
  background: #11141b;
  border-radius: 6px;
  margin-bottom: 24px;
  font-size: 12px;
  color: var(--muted);
}
.legend strong { color: var(--fg); }
.legend .swatch {
  display: inline-block;
  width: 22px;
  text-align: center;
  font-weight: 600;
}
.legend .pp { color: var(--team); }
.legend .p { color: var(--green); }
.legend .eq { color: var(--gold); }
.legend .m { color: var(--rival); }
"""


CATEGORY_ORDER = [
    ("First-party primitives", ["permissions", "claude-md-tight", "claude-md-bloated", "hooks-lint", "hooks-chained", "skills-primitive", "subagents-isolation", "auto-memory"]),
    ("Slash commands", ["clear-command", "memory-command", "loop-command"]),
    ("Models", ["sonnet-model", "haiku-model"]),
    ("MCP servers", ["playwright-mcp", "context7-mcp", "slack-mcp", "vercel-mcp", "gmail-drive-mcp", "mermaid-mcp", "generic-vendor-mcp"]),
    ("Plugins & frameworks", ["pr-review-toolkit", "obra-superpowers", "superclaude-framework", "wshobson-agents", "claude-flow"]),
    ("Around Claude Code", ["ccusage", "claudia", "claude-code-router"]),
    ("This plugin (dogfood)", ["claude-tool-audit-self"]),
]


def categorize(audits: list[Audit]) -> list[tuple[str, list[Audit]]]:
    by_slug = {a.slug: a for a in audits}
    out: list[tuple[str, list[Audit]]] = []
    seen: set[str] = set()
    for name, slugs in CATEGORY_ORDER:
        bucket = [by_slug[s] for s in slugs if s in by_slug]
        seen.update(a.slug for a in bucket)
        if bucket:
            out.append((name, bucket))
    rest = [a for a in audits if a.slug not in seen]
    if rest:
        out.append(("Other", sorted(rest, key=lambda a: a.slug)))
    return out


def render_row(a: Audit) -> str:
    raw_url = f"{GITHUB_RAW_BASE}/{a.path.name}"
    tool_cell = (
        f'<td class="tool">'
        f'<a href="{html.escape(raw_url)}" target="_blank" rel="noopener">{html.escape(a.title)}</a>'
        f'<span class="type">{html.escape(a.type_)}</span>'
        f'</td>'
    )
    cells = []
    for g in GATES:
        letter = a.scores.get(g, "—")
        cls = LETTER_CLASS.get(letter, "")
        cells.append(f'<td class="gate {cls}">{html.escape(letter)}</td>')
    install_html = (
        f'<span class="install">▸ install ▸ {render_install(a.install)}</span>'
        if a.install else ""
    )
    usecase = (
        f'<td class="usecase">{html.escape(a.use_case)}'
        f'{install_html}'
        f'<span class="src">{linkify_source(a.source)}</span>'
        f'</td>'
    )
    reco_cls = a.recommendation if a.recommendation else ""
    reco = f'<td class="reco {reco_cls}">{html.escape(a.recommendation or "—")}</td>'
    return f"<tr>{tool_cell}{''.join(cells)}{reco}{usecase}</tr>"


def render(audits: list[Audit]) -> str:
    sections = categorize(audits)
    body_parts = []
    for name, bucket in sections:
        rows = "\n".join(render_row(a) for a in bucket)
        body_parts.append(f"""
<div class="section-head">{html.escape(name)}</div>
<table class="audits">
  <thead>
    <tr>
      <th>Tool</th>
      <th>Obs</th>
      <th>Cost</th>
      <th>Simp</th>
      <th>Corr</th>
      <th>Verdict</th>
      <th>Use case &amp; source</th>
    </tr>
  </thead>
  <tbody>
{rows}
  </tbody>
</table>
""")

    legend = """
<div class="legend">
  <span><strong>Scale</strong></span>
  <span><span class="swatch pp">A+</span> exemplary</span>
  <span><span class="swatch p">A</span> good</span>
  <span><span class="swatch eq">B/C</span> acceptable / mediocre</span>
  <span><span class="swatch m">D</span> poor</span>
  <span><span class="swatch m">F</span> failure ▸ drop</span>
  <span style="margin-left: auto;"><strong>Rule</strong> ▸ one failing gate = drop. No averaging.</span>
</div>
"""

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>claude-tool-audit ▸ reviewed tools</title>
<style>{CSS}</style>
</head>
<body>
<header>
<h1>claude-tool-audit</h1>
<p class="sub">Tools reviewed against the four gates — Obs · Cost · Simp · Corr · letter scale A+..F</p>
<p class="meta">
Plugin repo ▸ <a href="https://github.com/mbrian23/claude-tool-audit">github.com/mbrian23/claude-tool-audit</a>
&nbsp;•&nbsp; Talk ▸ <a href="https://github.com/mbrian23/meetup-27-may">meetup-27-may</a>
&nbsp;•&nbsp; Built with <code>scripts/build-site.py</code>
</p>
</header>
<main>
{legend}
{''.join(body_parts)}
<p class="footer">
Generated from <code>examples/*.md</code>. The rubric lives in
<a href="https://github.com/mbrian23/claude-tool-audit/blob/main/references/gates.md">references/gates.md</a>
— the rule is <strong>no averaging, no summing</strong>: a single failing gate drops the tool, regardless of the others.
Scores are per-<em>use case</em>, not per-tool. Same primitive used wrong = different scores.
</p>
</main>
</body>
</html>
"""


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parent.parent
    examples = root / "examples"
    docs = root / "docs"
    docs.mkdir(exist_ok=True)

    audits: list[Audit] = []
    for p in sorted(examples.glob("*.md")):
        if p.name.startswith("_"):
            continue
        a = parse(p)
        if not a.scores:
            print(f"skip (no scores): {p.name}", file=sys.stderr)
            continue
        audits.append(a)

    out = docs / "index.html"
    out.write_text(render(audits), encoding="utf-8")
    print(f"wrote {out} ({len(audits)} audits)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
