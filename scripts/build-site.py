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
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

GATES = ["Obs", "Cost", "Simp", "Corr"]
LETTERS = ["A+", "A", "B", "C", "D", "F"]
LETTER_RANK = {letter: rank for rank, letter in enumerate(LETTERS)}
LETTER_CLASS = {"A+": "pp", "A": "p", "B": "eq", "C": "eq", "D": "m", "F": "mm"}

SCORES_HEADING = re.compile(r"^##\s+Scores\s*$", re.MULTILINE)
# Multi-line field capture: matches the value across lines until next blank line,
# next **Field:**, or markdown structure (#, |). Use re.DOTALL.
USE_CASE = re.compile(r"\*\*Use case:\*\*\s*(.+?)(?=\n\s*\n|\n\*\*[A-Z]|\n#|\n\|)", re.DOTALL)
PROJECT = re.compile(r"\*\*Project context assumed:\*\*\s*(.+?)(?=\n\s*\n|\n\*\*[A-Z]|\n#|\n\|)", re.DOTALL)
ROW = re.compile(r"^\|\s*([A-Za-z][A-Za-z+ ]*?)\s*\|\s*(A\+|[ABCDF])\s*\|\s*([^|]*?)\s*\|\s*$")
SOURCE = re.compile(r"^\*\*Source:\*\*\s*(.+?)\s*$", re.MULTILINE)
TYPE = re.compile(r"^\*\*Type:\*\*\s*(.+?)\s*$", re.MULTILINE)
INSTALL = re.compile(r"\*\*Install:\*\*\s*(.+?)(?=\n\s*\n|\n\*\*[A-Z]|\n#|\n\|)", re.DOTALL)
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
    project: str = ""
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
        a.install = collapse_ws(i.group(1))

    pr = PROJECT.search(text)
    if pr:
        a.project = collapse_ws(pr.group(1))

    m = SCORES_HEADING.search(text)
    if not m:
        return a
    body = text[m.end():]

    uc = USE_CASE.search(body)
    if uc:
        a.use_case = collapse_ws(uc.group(1))

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


def collapse_ws(s: str) -> str:
    """Collapse runs of whitespace (incl. newlines from multi-line markdown captures) to single spaces."""
    return re.sub(r"\s+", " ", s).strip()


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
  text-align: left;
  width: 220px;
  font-size: 12px;
  letter-spacing: 0.04em;
}
td.reco .verdict {
  display: block;
  font-weight: 700;
  font-size: 14px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}
td.reco .proj {
  display: block;
  color: var(--muted);
  font-weight: 400;
  font-size: 11px;
  letter-spacing: 0;
  text-transform: none;
  margin-top: 4px;
  font-style: italic;
}
td.reco.Buy    .verdict { color: var(--green); }
td.reco.Wrap   .verdict { color: var(--gold); }
td.reco.Vendor .verdict { color: var(--gold); }
td.reco.Build  .verdict { color: var(--accent); }
td.reco.Defer  .verdict { color: var(--muted); }
td.reco.Reject .verdict { color: var(--rival); }

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

.profile-bar {
  padding: 16px 18px;
  background: #11141b;
  border-radius: 6px;
  margin-bottom: 24px;
  border: 1px solid var(--line);
}
.profile-bar label {
  display: block;
  color: var(--muted);
  font-size: 13px;
  margin-bottom: 8px;
}
.profile-bar label strong { color: var(--fg); }
.profile-bar select {
  width: 100%;
  background: var(--bg);
  color: var(--fg);
  border: 1px solid var(--line);
  border-radius: 4px;
  padding: 10px 12px;
  font-family: inherit;
  font-size: 14px;
  cursor: pointer;
  appearance: none;
  background-image: linear-gradient(45deg, transparent 50%, var(--muted) 50%), linear-gradient(135deg, var(--muted) 50%, transparent 50%);
  background-position: calc(100% - 18px) 50%, calc(100% - 12px) 50%;
  background-size: 6px 6px;
  background-repeat: no-repeat;
}
.profile-bar select:focus { outline: 1px solid var(--accent); }
.profile-bar .thresholds {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--line);
  display: flex;
  flex-wrap: wrap;
  gap: 18px;
  font-size: 12px;
  color: var(--muted);
}
.profile-bar .thresholds .th-item strong { color: var(--fg); font-weight: 600; }
.profile-bar .thresholds .th-item .min { color: var(--gold); font-weight: 700; }
.profile-bar .summary {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--line);
  display: flex;
  flex-wrap: wrap;
  gap: 22px;
  font-size: 12px;
  color: var(--muted);
}
.profile-bar .summary .count { color: var(--fg); font-weight: 700; font-size: 14px; }
.profile-bar .summary .Buy    .count { color: var(--green); }
.profile-bar .summary .Wrap   .count { color: var(--gold); }
.profile-bar .summary .Vendor .count { color: var(--gold); }
.profile-bar .summary .Build  .count { color: var(--accent); }
.profile-bar .summary .Defer  .count { color: var(--muted); }
.profile-bar .summary .Reject .count { color: var(--rival); }

tr.changed td.reco {
  background: rgba(106, 163, 255, 0.06);
  border-left: 2px solid var(--accent);
}
"""


JS = r"""
// Project profiles ▸ per-gate letter threshold each tool must clear to be 'Buy'.
// Letters ranked: A+ best, F worst. clears(score, threshold) returns true when score is at-least the threshold.
const RANK = { "A+": 0, "A": 1, "B": 2, "C": 3, "D": 4, "F": 5 };
const GATES = ["Obs", "Cost", "Simp", "Corr"];

const PROFILES = {
  hobby: {
    name: "Personal / hobby",
    summary: "Synthetic or public data, throwaway code, single user.",
    thresholds: { Obs: "F", Cost: "D", Simp: "C", Corr: "D" },
    lenient: true,
  },
  prototype: {
    name: "Prototype",
    summary: "< 2 weeks horizon, internal audience, no production traffic.",
    thresholds: { Obs: "D", Cost: "D", Simp: "B", Corr: "C" },
    lenient: true,
  },
  internal: {
    name: "Internal product",
    summary: "Multi-month, business data, team-sized audience.",
    thresholds: { Obs: "B", Cost: "B", Simp: "B", Corr: "B" },
    lenient: false,
  },
  public: {
    name: "Public product",
    summary: "Multi-year, customer data, public audience.",
    thresholds: { Obs: "A", Cost: "A", Simp: "C", Corr: "A" },
    lenient: false,
  },
  regulated: {
    name: "Regulated / Compliance",
    summary: "Regulated/PII; correctness failures cost livelihoods; + Ethics gate.",
    thresholds: { Obs: "A+", Cost: "A", Simp: "D", Corr: "A+" },
    lenient: false,
  },
};

function clears(score, threshold) {
  if (!(score in RANK) || !(threshold in RANK)) return true;
  return RANK[score] <= RANK[threshold];
}

function letterGap(score, threshold) {
  return RANK[score] - RANK[threshold];
}

function verdictFor(scores, profile) {
  if (!profile) return null;
  const failing = GATES.filter(g => !clears(scores[g], profile.thresholds[g]));
  if (failing.length === 0) {
    return { verdict: "Buy", note: "clears all thresholds" };
  }
  // Any gate at F when the project's threshold is anything other than F is irrecoverable.
  for (const g of failing) {
    if (scores[g] === "F" && profile.thresholds[g] !== "F") {
      return { verdict: "Reject", note: g + " at F (irrecoverable)" };
    }
  }
  if (failing.length === 1) {
    const g = failing[0];
    const gap = letterGap(scores[g], profile.thresholds[g]);
    if (g === "Obs")  return { verdict: gap >= 2 ? "Vendor" : "Wrap", note: g + " below by " + gap };
    if (g === "Cost") return { verdict: "Wrap",   note: "budget hook for Cost" };
    if (g === "Simp") return { verdict: "Build",  note: "pick a different tool" };
    if (g === "Corr") return { verdict: gap >= 2 ? "Defer" : "Wrap", note: "confirmation hook for Corr" };
  }
  // 2+ failures
  if (profile.lenient) return { verdict: "Defer", note: failing.length + " gates fail: " + failing.join(", ") };
  return { verdict: "Reject", note: failing.length + " gates fail: " + failing.join(", ") };
}

function applyProfile(key) {
  const profile = PROFILES[key] || null;
  const thresholdsEl = document.getElementById("profile-thresholds");
  const summaryEl = document.getElementById("profile-summary");
  const counts = { Buy: 0, Wrap: 0, Vendor: 0, Build: 0, Defer: 0, Reject: 0 };
  const rows = document.querySelectorAll("tr[data-slug]");

  for (const tr of rows) {
    const scores = JSON.parse(tr.getAttribute("data-scores"));
    const origVerdict = tr.getAttribute("data-orig-verdict");
    const origProject = tr.getAttribute("data-orig-project");
    const recoTd = tr.querySelector("td.reco");
    const verdictSpan = recoTd.querySelector(".verdict");
    const projSpan = recoTd.querySelector(".proj");

    // Reset reco class
    const origCls = recoTd.getAttribute("data-orig-cls") || "";
    recoTd.className = "reco " + origCls;

    if (profile) {
      const r = verdictFor(scores, profile);
      verdictSpan.textContent = r.verdict;
      if (projSpan) projSpan.textContent = "for: " + profile.name + " ▸ " + r.note;
      recoTd.className = "reco " + r.verdict;
      tr.classList.toggle("changed", r.verdict !== origVerdict);
      counts[r.verdict] = (counts[r.verdict] || 0) + 1;
    } else {
      verdictSpan.textContent = origVerdict || "—";
      if (projSpan) projSpan.textContent = origProject ? "for: " + origProject : "";
      tr.classList.remove("changed");
      counts[origVerdict] = (counts[origVerdict] || 0) + 1;
    }
  }

  if (profile) {
    thresholdsEl.style.display = "flex";
    thresholdsEl.innerHTML =
      '<div class="th-item"><strong>' + profile.name + ':</strong> <em>' + profile.summary + '</em></div>' +
      GATES.map(g => '<div class="th-item">' + g + ' ≥ <span class="min">' + profile.thresholds[g] + '</span></div>').join("");
  } else {
    thresholdsEl.style.display = "none";
    thresholdsEl.innerHTML = "";
  }

  const total = Object.values(counts).reduce((a, b) => a + b, 0);
  summaryEl.innerHTML =
    '<span><strong>' + total + '</strong> tools ▸ </span>' +
    ["Buy", "Wrap", "Vendor", "Build", "Defer", "Reject"]
      .filter(v => counts[v] > 0)
      .map(v => '<span class="' + v + '"><span class="count">' + counts[v] + '</span> ' + v + '</span>')
      .join("");
}

document.addEventListener("DOMContentLoaded", function() {
  const sel = document.getElementById("profile-select");
  sel.addEventListener("change", function() { applyProfile(sel.value); });
  applyProfile(sel.value);  // initial paint for original verdicts (computes counts)
});
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
    proj_html = (
        f'<span class="proj">for: {html.escape(a.project)}</span>'
        if a.project else ""
    )
    reco = (
        f'<td class="reco {reco_cls}" data-orig-cls="{reco_cls}">'
        f'<span class="verdict">{html.escape(a.recommendation or "—")}</span>'
        f'{proj_html}'
        f'</td>'
    )
    # data-* attributes drive the project-profile selector JS below
    scores_json = html.escape(json.dumps(a.scores), quote=True)
    data_attrs = (
        f'data-slug="{html.escape(a.slug)}" '
        f'data-scores=\'{scores_json}\' '
        f'data-orig-verdict="{html.escape(a.recommendation or "")}" '
        f'data-orig-project="{html.escape(a.project)}"'
    )
    return f"<tr {data_attrs}>{tool_cell}{''.join(cells)}{reco}{usecase}</tr>"


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

<div class="profile-bar">
  <label for="profile-select"><strong>Project profile</strong> ▸ re-verdict every tool for a specific project:</label>
  <select id="profile-select">
    <option value="original">▸ Original audit verdicts (per-file)</option>
    <option value="hobby">Personal / hobby ▸ synthetic data, throwaway</option>
    <option value="prototype">Prototype ▸ &lt; 2 weeks, internal</option>
    <option value="internal">Internal product ▸ months, business data</option>
    <option value="public">Public product ▸ years, customer data</option>
    <option value="regulated">Regulated ▸ PII / compliance / + Ethics</option>
  </select>
  <div id="profile-thresholds" class="thresholds" style="display:none;"></div>
  <div id="profile-summary" class="summary"></div>
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
The profile selector above re-verdicts every tool from the same letter scores against different project budgets — the scores don't change, the threshold does.
</p>
</main>
<script>
{JS}
</script>
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
