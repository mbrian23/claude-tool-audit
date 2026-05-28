# /loop ▸ recurring prompt

**Source:** https://code.claude.com/docs/en
**Type:** First-party slash command
**Install:** N/A — first-party CLI command, nothing to install
**Project context assumed:** Project where polling or recurring work is genuinely useful.

## Surface

Re-runs a prompt or slash command at a chosen interval (or self-paced). The
interval can be cron-style or dynamic. Each tick is a full LLM call.

## Smells

- **Per-call without a stop condition.** A long-interval loop runs forever
  unless the user cancels. **Cost capped at C** per `cost-risks.md`.

## Scores

**Use case:** Polling a CI run that takes ~8 minutes — short loop, clear stop
condition (the run completes), bounded total cost.

| Gate | Score | Justification |
|------|-------|---------------|
| Obs  | A+ | First-party, every tick is visible in the session |
| Cost | C  | Per-tick LLM call; cap applies; bounded only by user discipline |
| Simp | A  | One command, one interval; debugging is just reading the session log |
| Corr | A  | LLM-driven check; correctness depends on the checked-for condition being verifiable |

## Recommendation

**Buy** for the short-loop use case — `vendoring.md` row "Every gate clears budget."

For the *long-loop* use case (background monitoring, hours-to-days), this would
score Cost D and the recommendation flips to **Wrap** with a budget hook that
caps cost-per-loop. Set the cap before invoking; the framework's rule is "watch
the bill."
