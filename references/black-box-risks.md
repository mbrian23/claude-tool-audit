# Black-box risks ▸ knocks on the Obs gate

A "black box" is any tool whose behaviour you can't predict from reading its name
and docs. Most MCP servers, most third-party agents, and a lot of plugins are at
least partly black boxes. The risk isn't using them — it's *not knowing you're
using them*. Black-box smells primarily knock the **Obs** gate, sometimes Corr.

## The five smells

### 1. Install-time code execution

The tool runs code on your machine *before you've used it once*. `npm install`
runs `postinstall` scripts. `pip install` runs `setup.py`. MCP servers fetched
from GitHub may run a bootstrap step. A `curl | sh` is the extreme.

**Audit move**: trace exactly what happens between `install command typed` and
`tool ready`. Read the postinstall / setup script if there is one. If you can't,
treat the install path itself as a black box. This is the supply-chain smell;
auth-scope inspection and tool surface enumeration come *after* this one because
neither matters if the install already ran code you didn't see.

### 2. Tool surface ≫ documented behaviour

The MCP server exposes 25 tools. The README explains 4. The other 21 are
"discoverable" — Claude finds them at runtime and uses them without you having
read what they do.

**Audit move**: enumerate the actual tool names (most MCP servers expose
`tools/list`). If you can't enumerate them, this is a knock.

### 3. Side effects not in the name

A tool named `search_files` that also writes a query log. A `read_thread` that
marks threads as read. A `get_records` that triggers a re-sync. Side effects you
don't see are the ones that bite.

**Audit move**: for every tool you'll use, ask "what does this *change*?" If the
docs only describe what it *returns*, treat that as a smell, not as evidence.

### 4. Auth scopes ≫ used scopes

The MCP server asks for `repo`, `read:org`, `write:packages`, `admin:repo_hook`.
The plugin only needs to read PR descriptions.

**Audit move**: cross-check requested scopes against the documented tool list.
Any unjustified scope is a black box.

### 5. Vendor-controlled prompt or model

The tool returns model-generated text that re-enters your conversation. You can't
see the prompt the vendor used and can't pin the model.

**Audit move**: if the tool's output is *generated text* (not data), find out which
model and prompt produced it. If you can't, this is the most expensive kind of
black box.

## Letter knocks

When scoring a candidate that triggers a smell, downgrade by **one letter** on the
listed gates. Apply at most one knock per smell. Knocks compound by design.

| Smell | Knock |
|-------|-------|
| **Install-time code execution** (no audit possible) | **−2 letters on Obs** |
| Install-time code execution (postinstall script readable) | −1 letter on Obs |
| Tool surface ≫ docs | −1 letter on Obs |
| Hidden side effects | −1 letter on Obs, −1 letter on Corr |
| Excess auth scopes | −1 letter on Obs |
| Vendor-controlled prompt/model | −1 letter on Obs, −1 letter on Cost (context amplification) |

A tool that triggers two smells gets two knocks. A tool that started at A on Obs
and triggers a hidden-side-effects smell ends at B. Don't dampen the knocks; the
threshold mindset relies on them.

## Mitigations (in increasing strictness)

1. **Document the surface**: paste the actual `tools/list` output into the audit.
   Black boxes you've enumerated are at least *known*.
2. **Scope down**: most MCP configs accept `disabledTools` / `enabledTools`
   allowlists. Disable the ones you don't use.
3. **Wrap with a hook**: a `PreToolUse` hook that inspects the call and blocks
   destructive variants converts a black box into a constrained one. **+1 letter
   Obs** if the wrapper is in your repo.
4. **Cage in a sub-agent**: give the black-box tool only to a sub-agent with no
   write-to-disk and no network. Its blast radius drops to its return value.
5. **Vendor a copy**: pin a known-good version in your own infra. **+1 letter Obs
   and Simp**; usually **−1 Cost** to operate.
6. **Don't add it**: if mitigations 1–5 don't bring Obs above your project's
   threshold, the answer is "not yet."

See `vendoring.md` for which mitigation suits which project profile.
