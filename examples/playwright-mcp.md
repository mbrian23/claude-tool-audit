# Playwright MCP

**Source:** https://github.com/microsoft/playwright-mcp
**Type:** MCP server (stdio, runs locally)
**Install:** **npm install + npx** ▸ Playwright binary install runs setup scripts (Microsoft-signed, pinnable by version, readable). Not a smell; the runtime surface is the issue.
**Project context assumed:** Internal product, multi-month horizon, business data.

## Surface

About two dozen tools, roughly:

- Navigation: `browser_navigate`, `browser_navigate_back`, `browser_close`, `browser_tabs`
- Interaction: `browser_click`, `browser_type`, `browser_press_key`, `browser_hover`, `browser_drag`, `browser_drop`, `browser_select_option`, `browser_fill_form`, `browser_file_upload`
- Inspection: `browser_snapshot`, `browser_take_screenshot`, `browser_console_messages`, `browser_network_requests`, `browser_network_request`
- Execution: `browser_evaluate`, `browser_run_code_unsafe`
- Lifecycle: `browser_resize`, `browser_wait_for`, `browser_handle_dialog`

Auth: none (local process). Side effects: opens a real browser, can fill any form,
can run arbitrary JS in the page.

## Smells

- **Tool surface ≫ docs in detail.** The names are clear, but the unsafe variant
  (`browser_run_code_unsafe`) ships in the default surface. **Knock: −1 Obs.**

## Scores

**Use case:** UI verification on internal product — real browser checks during
development, no live customer data.

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | A  | Local execution, full source available; knock applied to bring from A+ to A |
| Cost | A  | Free per-call, but `browser_snapshot` returns DOM trees so context isn't free |
| Simp | A  | Local install but real browser dependency adds operational moving parts |
| Corr | A+ | Real browser is the ground truth — no hallucination of selectors or layout |

## Recommendation

**Wrap** — `vendoring.md` row "Public-facing → Corr D/F" does not match; the
binding row here is the unsafe surface, not a failing gate.

Concrete wrapping: disable `browser_run_code_unsafe` via the MCP `disabledTools`
allowlist; confine the server to a sub-agent that has no shell access. A
`PreToolUse` hook that requires user confirmation for any `browser_navigate` to an
external domain is a strong second layer for any public-facing project.

For a prototype, **Buy** (use as-is, allowlist trimmed) is acceptable — the Obs
knock matters less when the horizon is < 2 weeks.
