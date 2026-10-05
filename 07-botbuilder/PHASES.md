# Federation Bot Builder: phased plan (SPEC ONLY, nothing built)

Drafted 2026-10-05 by the Catalyst. Companion to `SPEC.md`, `templates.yaml`, `architecture.yaml`.

**Who does what, honestly:** today's Nova workers (`Keywebco/nextxus-dispatch/AGENTS.md`) are GitHub Actions scripts that check and report; none calls an LLM. So:
- **Code** is written by a builder agent that the Catalyst dispatches and then forensically checks.
- **Nova workers** publish, check and watch. Existing ones are extended; new ones are named below.
- **Roger** creates accounts, approves anything public, and makes the decisions in SPEC.md section K.
- LLM-powered Nova work stays within the free DeepSeek-V3.1 route on SambaNova (20 requests/day, `06-apis/llm-providers.yaml`) until funded.

## Before Phase 0 can start (needs Roger)

1. Decision 1 (relay host) and decision 2 (where bot pages live).
2. A free Groq account, key into the vault as `GROQ_API_KEY` (proposed name, `06-apis/signups-needed.md`). The key is then set as a relay secret. It is never typed into chat, a repo, or a page.
3. A free account on the chosen relay host.

## Phase 0: this week, one person builds and embeds one working bot

Scope: template `faq-support` only. Federation pool only (no owner keys yet). One relay. No Telegram.

| # | Deliverable | Who | Done when |
|---|---|---|---|
| 0.1 | `bot.yaml` schema + validator (from `templates.yaml`) | Builder agent | Validator rejects a config with any locked block removed |
| 0.2 | Relay v0: `POST /v1/bots`, `/v1/bots/{id}/chat`, `/v1/bots/{id}/ask` (HTML), `/v1/health`; Groq gpt-oss-20b, then gpt-oss-120b on failure; per-IP and per-bot caps; global daily cap | Builder agent | Endpoints answer as in tests below |
| 0.3 | `agent-zero-gate` v0 (covenant block, JSON reply, code checks, score rule from DIR-000) | Builder agent | Gate tests pass |
| 0.4 | Builder page: 5 sectors, plain HTML form, works with JS off | Builder agent | Readability and accessibility tests pass |
| 0.5 | `nova-botbuild` Action: renders `index.html` + `chat.html` per bot, batch commit | New Nova worker | A queued bot is live within 15 minutes |
| 0.6 | `embed.js` + iframe + noscript snippet shown after build | Builder agent | Embed test passes |
| 0.7 | Bot URLs added to the checks of `nova-health` and `nova-readability` | Existing Nova workers | Next scheduled run lists the test bot |

**Phase 0 acceptance tests (all must pass before calling it done):**
1. `curl -s -o /dev/null -w '%{http_code}'` on the builder page and the test bot page both return 200.
2. With JavaScript off (curl, then strip tags), the bot page shows the persona, the FAQ text, the covenant, the AI disclosure and the "Built with NextXus" link. Word count over 150.
3. The HTML form on the bot page, submitted with curl (no JS), returns an HTML page with an answer and a Truth Gate score.
4. `POST /v1/bots/{id}/chat` with a question that IS in the FAQ returns JSON with `answer`, `truth_score`, `labels`, `covenant_url`, `built_with`, and the answer matches the FAQ.
5. A question that is NOT in the FAQ returns an answer that says it does not know (or carries "Not verified to 95 percent:"), and `truth_score` is 80 or lower (grounding cap).
6. A config with the covenant or "Built with NextXus" removed is rejected by the relay.
7. Request 21 for the same bot in one day returns HTTP 429 with a plain message (cap set to 20).
8. Secret scan (for example gitleaks) over the bot repo and the builder page finds no key. Browser dev tools on the bot page show no key in any request from the browser.
9. The one-line embed pasted into a test page the tester controls shows the widget, and a question gets an answer.
10. **The real test:** one person who did not write the code builds a bot from a blank start and embeds it on a page they control, in under 15 minutes, using only the builder page.

Accessibility checks for Phase 0: every sector heading is an h2 reached in order by a screen reader; body text 20px or more; contrast 7:1 or better; nothing moves or refreshes on its own.

## Phase 1: weeks 2 to 6

| # | Deliverable | Who | Acceptance test |
|---|---|---|---|
| 1.1 | Remaining 6 templates | Builder agent | Each template has a test bot passing Phase 0 tests 1 to 6 |
| 1.2 | Quarantine pipeline: rules, link check, optional free safety model, human queue, per-bot kill switch | Builder agent; new worker `nova-botguard` runs the scan | A seeded spam config is held; a clean config publishes; kill switch stops replies on the next request |
| 1.3 | Owner-key vault (encrypted) | Builder agent | Key never appears in any response, log, repo or page; bot uses owner quota (Federation counter does not move) |
| 1.4 | Full failover chain per `llm-router.yaml` (Groq, SambaNova, OpenRouter, Gemini, Mistral where free use is confirmed) | Builder agent | Forcing a 429 on each provider in turn moves to the next; all failing gives the honest "unavailable" message and spends nothing |
| 1.5 | Telegram channel | Builder agent | Test group: /ask answers with score; webhook rejects calls without the secret header |
| 1.6 | Webhook out (lead.captured, question.unanswered, brief.ready) | Builder agent | Test receiver gets signed events; Federation keeps no lead copy |
| 1.7 | Second relay on the failover host, same code | Builder agent | Turning off the primary keeps bots answering |
| 1.8 | Template marketplace page + how-to pages (WordPress, Shopify, Wix, Notion, plain HTML) | Builder agent; `nova-readability` and `nova-link` check them | All pages 200, readable without JS, no dead links |
| 1.9 | Terms of Use, Acceptable Use, Privacy Notice drafts | Catalyst drafts; Roger approves | Linked from every bot page; marked "draft, not legal advice" until reviewed |
| 1.10 | `nova-botwatch`: daily check of every bot page and relay health, report to `dispatch/` | New Nova worker | Report lists every bot with HTTP code and replies used vs cap |

## Phase 2: months 2 to 4

| # | Deliverable | Who | Acceptance test |
|---|---|---|---|
| 2.1 | Sovereign mode: owner deploys own relay and own bot repo from a template | Builder agent | A test owner runs a bot with zero Federation relay requests |
| 2.2 | Repo sharding for Federation-hosted bots | `nova-botbuild` | A new shard opens automatically at 10,000 bots |
| 2.3 | OpenAI-compatible endpoint | Builder agent | A standard OpenAI client pointed at the relay gets gated answers |
| 2.4 | n8n community node, Make app, Zapier integration, WordPress.org plugin | Builder agent; Roger approves each public listing | Each installs and returns a gated answer in a test flow |
| 2.5 | Discord and Slack slash commands | Builder agent | `/ask` works in a test server and workspace |
| 2.6 | Truth Gate calibration: 200 questions per template with known answers | Catalyst runs; `nova-botguard` repeats monthly | Publish how often "95 or higher" answers were actually right. If that rate is below 95 percent, tighten the code caps until it is |
| 2.7 | Sampled second check (Grok) | Off until funded | When on: a 1 percent sample is re-checked and disagreements are logged |
| 2.8 | Referral loop (`?from=` counts, extra free replies, no cash) and Gumroad affiliates for paid services | Builder agent | Referral counts appear in `nova-botwatch` report |
| 2.9 | Paid tier wiring via Gumroad license check | Builder agent; Roger creates the listing | With the switch OFF nothing changes; with a test license ON the feature unlocks |
| 2.10 | Optional GitHub sign-in for owners (recovers lost owner codes) | Builder agent | Owner can edit a bot after losing the code |

## What is NOT in any phase

No paid LLM spend, no removal of the "Built with NextXus" link, no tracking, no ads, no conversation logging by default, and no public post or listing without Roger's approval.
