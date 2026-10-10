# Cost receipt

Written 2026-10-09 from measured numbers. **Estimates are marked as estimates.**

## GitHub Actions minutes (measured)

This repository is public, so GitHub Actions on standard runners costs nothing. For the record, from the run history since 2026-10-08:

| Job | Runs | Billable minutes (rounded up per job) |
|---|---|---|
| Federation health check | 2 | about 3 |
| Command build (review branch only) | 1 | about 1 |
| Nova-Canon daily check | 1 | about 1 |
| **Total** | **4** | **about 5** |

The health check is scheduled every 4 hours (6 runs a day, each rounded up to a minute or two), so expect roughly 6 to 12 minutes a day. **That is a projection:** the schedule began on 2026-10-09 and there are only a few runs so far. **Cost to us: $0, because the repository is public.** If it were private, free plans include a monthly allowance and this would still fit; that is an estimate and not tested.

## Model calls (measured price, estimated use)

- **Published price, MiMo V2.6 Pro:** about $0.435 per million input tokens and $0.87 per million output tokens (source: the provider's pricing page, checked 2026-10-09).
- **One small build** (a page of a few thousand tokens in, a few thousand out) costs well under one cent at that price. **This is an estimate.** The exact tokens used per build were not logged.
- **One health check** makes no model calls. It costs nothing in model fees.
- **The "first 3 checks are free" tools** each use a model call. That is why the page says: each check costs us a few cents, so the first 3 are on us.

## What is not counted here

- Hosting on Render's free plan: $0.
- The Emergent subscription that runs the Catalyst and the scheduled jobs: paid by Roger. We do not have its exact cost.
- Domain names and Gumroad's sales fee.

This note is rewritten when the numbers change. A claim without a date is not a receipt.
