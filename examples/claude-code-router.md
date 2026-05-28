# claude-code-router

**Source:** https://github.com/musistudio/claude-code-router
**Type:** CLI wrapper — routes requests to DeepSeek / Gemini / Groq / etc.
**Install:** **`npm install` + config** ▸ wrapper code itself is small and readable; the routing destinations are the runtime risk, not install.
**Project context assumed:** Anything beyond a personal hobby account.

## Surface

Sits between the Claude Code CLI and the LLM provider. Intercepts requests and
re-routes to non-Anthropic models. Cost wins big; everything else loses.

## Smells

- **Vendor-controlled prompt/model.** The router decides which model your prompt
  hits. The model isn't pinned. **Knock: −1 Obs, −1 Cost.**
- **Hidden side effects** — you don't know which provider saw your prompt.
  **Knock: −1 Obs, −1 Corr.**

## Scores

**Use case:** Routing Claude Code requests to alternative LLM vendors to cut cost
on a personal/hobby account.

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | D  | Vendor-controlled routing, no provider pinning; two knocks bring from B to D |
| Cost | A+ | Massive cost reduction — the whole point of the tool |
| Simp | C  | Wrapper layer adds operational complexity; debugging requires understanding which provider ran |
| Corr | D  | Different model per call; outputs are not reproducible; knock applied |

## Recommendation

**Reject** for any client / sensitive / regulated work — `vendoring.md` row
"Regulated data → Obs D/F".

Two failing gates (Obs and Corr) simultaneously. **No averaging.** Cost A+ does
not buy back the failures.

For personal hobby on synthetic data: **Buy** is acceptable — the same scoring
on a different project profile would actually flip the recommendation.
This is a teaching example for "scores are circumstantial."
