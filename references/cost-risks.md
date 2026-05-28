# Cost risks ▸ knocks on the Cost gate

The Cost gate tracks **$/request + $/run + tokens**. Three patterns cause almost
every "we didn't expect that bill" incident with Claude Code adjacent tools.

## Pattern 1 ▸ Context amplification

The tool returns a large blob — a full page of search results, an entire file, a
sprawling JSON response. That blob enters the next LLM turn. Every subsequent turn
pays for those tokens.

**Examples**: web-search MCPs that dump full article text; database MCPs that
return unfiltered query results; documentation MCPs that paste full pages.

**Tell**: no `limit` or `excerpt` parameter, or the limit is in *items* rather than
*tokens*.

**Mitigation**: prefer tools with token/byte caps. If unavailable, wrap with a
sub-agent that summarises before returning to the main thread.

## Pattern 2 ▸ Agent recursion

An agent calls a tool that triggers another agent. A hook injects a prompt that
calls a tool that triggers a hook. Each hop costs an LLM call, and the call count
is not bounded by user intent.

**Examples**: MCP servers whose tools are themselves agents; hooks that fire on
every `PostToolUse` and use an LLM to decide whether to block.

**Tell**: docs mention "intelligent" anything — intelligent routing, smart
formatting. Intelligence usually means an unbudgeted LLM call.

**Mitigation**: turn off the "intelligence" if possible. If the tool *is* the
intelligence, see a representative trace before adopting.

## Pattern 3 ▸ Per-call without a stop condition

The tool can be called in a loop because the LLM doesn't know when to stop.
Search, retrieval, and "explore" tools are the usual suspects.

**Examples**: file-search tools the agent calls 12 times in a row; web-fetch the
agent calls on every URL it sees.

**Tell**: returns data the agent has no way to know is "enough." Pagination
without a total count. Search without relevance scores.

**Mitigation**: a `PreToolUse` hook that counts calls per turn and blocks beyond
a budget. Or replace with a tool that returns top-K with a relevance score.

## Letter caps

When the candidate exhibits a Cost smell, **cap the Cost letter** at the value
below. Use the strictest cap that applies.

| Tell | Cost cap |
|------|----------|
| Returns full-page blobs by default, no token cap | Cost capped at **C** |
| Spawns its own agent calls | Cost capped at **C** |
| Can be loop-called with no stop condition | Cost capped at **C** |
| Pricing is per-token of input to the *vendor's* model, not yours | Cost capped at **D** |
| Paid "fast" or "premium" mode | Cost capped at **D** for that mode |
| Flat-fee or local | Cost can be A or A+ |

## Budget-side guidance

The **budget-planner** skill produces a Cost budget per project. For a new
project, a common reservation:

- 60% baseline expected usage (your forecast × 1.5)
- 20% headroom for context-amplification surprises
- 20% headroom for tools you'll add later

If you can't reserve 40% headroom, defer the tool decision or wrap it behind a
budget-aware hook before adopting.

## Tokens are cost

When the slide says "Cost · tokens too," it means the Cost gate scores the full
LLM bill, not just the line-item invoice from the vendor. A free MCP that returns
8 KB of JSON per call is **not** a Cost A+ tool — its per-call bill arrives on
your Anthropic invoice, not the vendor's.
