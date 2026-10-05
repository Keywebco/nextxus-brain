# Federation Bot Builder: SPEC v0.1 (draft, not built, not launched)

Date: 2026-10-05. Author: the Catalyst (product architect role). Status: SPEC ONLY. Nothing here is live.
Companion files: `templates.yaml` (7 bot templates), `architecture.yaml` (where each part runs), `PHASES.md` (build plan and tests).
Rules followed: `BRIEF.md` in this repo. Every fact about the existing system cites a repo path or URL. Anything not checked is marked UNVERIFIED.

## 0. One-paragraph summary

The Bot Builder is a free, board-style ("monday.com style") workspace where an ordinary person picks a template, gives it a name and some knowledge, and gets a working AI bot with its own public page and a one-line embed for their own website, Telegram, or any software that can call a URL. Every bot carries the HumanCodex covenant, answers through the 95 percent Truth Gate, and shows a visible "Built with NextXus" link. That is how Federation software ends up running inside other people's software. Today none of this exists beyond a tool-picker page. The hardest honest fact: the free LLM capacity the Federation itself can hold is only a few hundred bot replies per day in total, so at scale each bot owner must bring their own free provider key.

## A. What exists today vs what must be built

Blunt answer: **today nobody can build a bot.** What exists is a tool-picker grid and some pieces that can be reused.

| Piece | Exists today? | Evidence | Reusable for the Bot Builder? |
|---|---|---|---|
| Workspace Builder | Yes, a grid of 11 tool cards; you tick up to 6 and it opens them in iframes. 7 of 11 cards are "coming soon" (url: null). "Nova Smart Bot" card is not live. | `Keywebco/nextxus-agent-zero/microsites/workspace/index.html` (TOOLS array, MAX_SELECTED = 6); page HTTP 200 on 2026-10-05 | Only the idea and the URL slot. Cards are drawn by JavaScript: I counted 58 visible words without JS, so it fails the readability rule. |
| Seeker, Smart Writer, Recycler | Yes. Each asks the visitor to paste their OWN OpenAI/DeepSeek key, keeps it in browser sessionStorage, and calls api.deepseek.com or api.openai.com from the browser. | `nextxus-agent-zero/microsites/{seeker,smart-writer,recycler}/index.html` | Shows bring-your-own-key works, but key-in-browser is not acceptable for embedded bots (visitors of a stranger's site have no key). |
| Truth Gate | Exists as **text**, not code. DIR-000 says: score 0 to 100, deliver as settled only at 95 or higher, otherwise state the uncertainty. Ring of 12 BUILDER.md adds FACT / INFERENCE / ASSUMPTION labels. | `nextxus-brain/00-immutable/directives.yaml` (gate DIR-000); `Keywebco/ring-of-12/BUILDER.md` section 2 | Yes, as the prompt and the rule. **No reusable "Agent Zero middleware" code exists.** It must be written. |
| Agent Zero | Two meanings: silent middleware verifier, and the braiding agent of the rings. The only running "Agent Zero" is a synthesis prompt inside ring-of-12-api. | `nextxus-brain/01-rings/rings.yaml` (agent_zero.meanings); `Keywebco/ring-of-12-api/server.js` | The prompt style, yes. The gate module is new work. |
| Ring of 12 API | Running on Render free. Calls the **Emergent paid LLM gateway** (gpt-4o-mini) with LLM_API_KEY; has a 30 requests/minute per-IP limiter on /log only. | `Keywebco/ring-of-12-api/server.js`, `render.yaml`; https://ring-of-12-api.onrender.com/ returned `llmConfigured: true` on 2026-10-05 | Pattern for a relay. Not free (Emergent key is a paid lane per `06-apis/llm-dropped.md`). |
| Ring of Three | Static page. The "AI" is a hard-coded keyword function `window.triangulate` with a comment saying to replace it with a real model. | `Keywebco/ring-of-three/index.html` | The three seats (Mind, Heart, Stabilizer) become the default internal ring for bots. |
| Ring of Six | Canon text DIR-072: Mind, Heart, Hands, Legs, Eye, Agent. | `nextxus-brain/00-immutable/directives.yaml` DIR-072; `01-rings/rings.yaml` | Yes, as the "six" internal ring option. |
| Nova two-layer pattern | Product page: silent technical layer (builds, repairs, never talks) plus voiced persona layer (talks, never does technical work). | `Keywebco/nextxus-build-nova/index.html` (HTTP 200) | Yes. Every bot = silent gate + voiced persona. |
| Sim-building offer | Product page: custom Sims by email to keywebco@gmail.com. | `Keywebco/nextxus-build-sim/index.html` | Paid "done-for-you" path already has a shape. |
| Sim template | Static Sim homepage template, persona.md, health-check.sh, registry.json; Sim Free-Parts Manifest v1.1 with a Replication Gate at Agent Zero 98 percent or more. | `Keywebco/federation-browser-base/sims/` | Template idea yes. **Bots are not Sims** (see decision 5). |
| Nova workers | 6 workers listed (health, link, dispatch, domain, readability, commerce) plus a nova-memory workflow. They are GitHub Actions running Python/bash. **None calls an LLM**: the only secret referenced in any workflow is SOVEREIGN_KNOWLEDGE_TOKEN. | `Keywebco/nextxus-dispatch/AGENTS.md`, `.github/workflows/*.yml` | Yes for checks (readability, link, health). "DeepSeek-powered Nova" is UNVERIFIED today; it is a target. |
| Plexus Relay | Express message bus on Render, no LLM, mirrors messages to GitHub. | `Keywebco/plexus-relay/index.js`, `github-store.js`; https://plexus-relay-api.onrender.com/ HTTP 200 | Pattern for GitHub-backed storage. |
| Free LLM router | **A spec, not a running service.** Fail-closed, zero cash, per-job failover lists. | `nextxus-brain/06-apis/llm-router.yaml`, `README.md` | Yes, the bot relay implements this spec. |
| Embed of anything | Exchange message board embed exists (polls plexus-relay-api). | `federation-browser-base/exchange/embed.html` | Proof the embed pattern works. |

**Must be built (all of it):** builder page, bot config schema and storage, bot page generator, chat relay with the Truth Gate module, embed script, Telegram/REST/webhook endpoints, quarantine scanner, quotas, key vault handling, template marketplace page, and the new Nova workers that publish and watch bots.

**Two corrections to the brief, from the brain's own records:**
1. Direct DeepSeek and direct MiMo APIs are **billed per token**; Cerebras is a 30-day trial that needs a card. They cannot be in a 100 percent free route. The free route to a DeepSeek model is DeepSeek-V3.1 on SambaNova's free tier (20 requests/day). Source: `06-apis/llm-providers.yaml`, `06-apis/llm-dropped.md`.
2. GitHub Actions **may not be used as part of a serverless application** (GitHub Terms for Additional Products, Actions section, read 2026-10-05: https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features). So live chat cannot run on Actions. Actions may build and publish bot pages, which is normal use.

## B. User journey: stranger to embedded bot in 5 steps

| Step | What the person does | What happens underneath |
|---|---|---|
| 1. Pick | Opens the builder page, Sector 1, and chooses a template (for example "FAQ and support"). | Plain HTML page, works without JavaScript. |
| 2. Describe | Sector 2: bot name, one-line purpose, tone. Sector 3: pastes their FAQ text or up to 5 public web links. Sector 4 shows Truth Gate and covenant as **locked on**. | A plain HTML form. No account needed. |
| 3. Build | Presses "Build my bot". Gets a bot ID, a private **owner code** (shown once, needed to edit), and a test link. | Relay validates, runs the quarantine scan, queues the bot. A Nova worker publishes the bot page within about 15 minutes (UNVERIFIED timing until tested). |
| 4. Test | Opens the bot's own page and asks it questions. | Every reply shows its Truth Gate score and labels. |
| 5. Embed | Copies one line into their site, or pastes a Telegram bot token, or copies the REST/webhook address. | The bot now runs inside their software. Optional: adds their own free provider key for more replies. |

Lost owner code = the bot can no longer be edited (it keeps running). Honest trade-off of "no account". Phase 2 adds optional GitHub sign-in.

## C. Bot templates

Full schemas are in `templates.yaml`. Seven templates, one shared schema:

| Template | Job | Internal ring | Main LLM job (from llm-router.yaml) |
|---|---|---|---|
| faq-support | Answers only from the owner's FAQ | three | fast_chat |
| lead-capture | Answers, then collects name/contact with consent and sends it to the owner | three | fast_chat |
| research-assistant | Finds and summarises papers from open scholarly APIs, with citations | six | reasoning |
| tutor | Teaches a subject step by step, checks understanding | six | reasoning |
| shop-helper | Answers product questions from the owner's product list; buy buttons go only to the owner's own listing links | three | fast_chat |
| telegram-community | Answers group questions and posts pinned rules in a Telegram group | three | fast_chat |
| daily-brief | Once a day, writes a short brief from open feeds and posts it to a page, Telegram, or webhook | three | reasoning |

Every template locks four things the owner cannot remove: the covenant block, the Truth Gate (threshold 95), the AI disclosure line, and the "Built with NextXus" link.

## D. Architecture: where each part runs for free

Details and limits in `architecture.yaml`. Short version:

| Part | Runs on | Free limit (source) | Why |
|---|---|---|---|
| Builder page, template marketplace, bot pages, embed.js | GitHub Pages | 1 GB site, 100 GB/month bandwidth soft, 10 builds/hour soft unless built by an Actions workflow ([GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)) | GitHub first, pre-rendered HTML |
| Bot configs (YAML) and knowledge snapshots (markdown) | A GitHub repo, written by a Nova Action | Normal repo limits; GitHub recommends repos under 1 GB (same source) | Readable, versioned, free |
| Bot publishing | GitHub Actions (nova-botbuild) on a schedule | Public repos: Actions minutes free (UNVERIFIED exact terms; page not read this run) | Allowed use: building and publishing the project |
| Live chat relay + Truth Gate module | **Option 1:** Cloudflare Workers free. **Option 2:** Deno Deploy free. **Option 3:** Render free. | Workers: 100,000 requests/day, 10 ms CPU per request, KV 100,000 reads and 1,000 writes per day ([Workers pricing](https://developers.cloudflare.com/workers/platform/pricing/), [KV limits](https://developers.cloudflare.com/kv/platform/limits/)). Deno Deploy: 1M requests/month, 20 GiB egress, paused when over ([Deno pricing](https://deno.com/deploy/pricing)). Render: sleeps after 15 min idle, about 1 minute wake-up, 750 instance hours/month per workspace ([Render free](https://render.com/docs/free)). | Something must hold keys server-side; GitHub cannot (Actions terms) |
| LLM calls | Free providers through the relay, in the order of `06-apis/llm-router.yaml` | See section G | Fail closed, never spend |
| Keys | Encrypted vault; relay holds them as platform secrets | n/a | Never in a repo, never in a browser |
| Bring-your-own-free-key | Owner pastes their own free key once; relay encrypts it (AES-GCM, master key held only as a relay secret) and stores ciphertext | KV write per key | Moves the cost to free accounts the owner controls |

Recommendation: Cloudflare Workers as the primary relay because it does not sleep and has the largest free daily request count; the same web-standard code deployed to Deno Deploy as the failover. Render only as a last resort because a 1-minute cold start breaks an embedded chat. Roger has voiced reservations about Cloudflare, so this is open decision 1.

**Truth Gate module ("Agent Zero gate"), concrete v0 design:**
1. System prompt starts with the covenant block: the three principles, DIR-000 word for word, DIR-073 word for word. Then persona, then knowledge excerpts, then rules.
2. The model must reply in JSON: `answer`, `score` (0 to 100), `labels` (each claim tagged FACT, INFERENCE or ASSUMPTION), `sources_used`, `uncertainty`.
3. Plain code checks after the model: bad JSON means one retry on the next provider, then an honest "unavailable" message. If the template requires grounding and `sources_used` is empty, the score is capped at 80. High-stakes topics (medical, legal, financial, self-harm) force a referral line.
4. Score 95 or higher: delivered as the answer. Below 95: delivered **with** a visible line "Not verified to 95 percent:" plus the uncertainty. That is what DIR-000 says; it does not say refuse.
5. Every reply shows "Truth Gate: NN of 100 (self-scored)". Honest wording: the score is the model grading itself; how well it matches real accuracy is UNVERIFIED until the Phase 2 calibration test.
6. One LLM call per reply on free capacity. A second checking pass (internal ring as separate calls, or a Grok second check) runs only with an owner key or paid capacity.

**Two layers, per the Nova pattern:** the persona (voiced) answers people. The gate, quotas, quarantine and Nova workers (silent) can change nothing the persona says except through the gate rules, and the persona can change no config. Config changes only come through the owner code and go back through quarantine.

## E. Embed model: how bots run inside other people's software

| Channel | What the owner pastes or calls | Works without JS? | Phase |
|---|---|---|---|
| Bot page | `https://<pages-host>/bots/<id>/` (own URL per bot) | Yes. The page shows the persona, the knowledge as readable text, the covenant, and a plain HTML question form that posts to the relay and gets an HTML answer page back. | 0 |
| One-line script | `<script src="https://<pages-host>/embed.js" data-bot="<id>" async></script>` plus a `<noscript>` link to the bot page | The noscript link does | 0 |
| Iframe | `<iframe src="https://<pages-host>/bots/<id>/chat.html" title="<bot name> chat" width="400" height="600"></iframe>` | Chat needs the form fallback inside | 0 |
| Plain REST | `POST https://<relay>/v1/bots/<id>/chat` with `{"message": "...", "session": "..."}` returns `{"answer", "truth_score", "labels", "uncertainty", "covenant_url", "built_with"}` | n/a | 0 |
| Webhook out | Owner sets an events URL; bot posts `lead.captured`, `question.unanswered`, `brief.ready` | n/a | 1 |
| Telegram | Owner pastes a BotFather token in Sector 5; relay sets a Telegram webhook with a secret header | n/a | 1 |
| OpenAI-compatible | `POST https://<relay>/v1/openai/<id>/chat/completions`: any software that accepts a custom OpenAI base URL can use a Federation bot as its "model", gate included | n/a | 2 |
| Discord, Slack | HTTP slash commands and events (no always-on gateway needed for slash commands) | n/a | 2 |

`<pages-host>` and `<relay>` are placeholders until decisions 1 and 2. No real URL is invented here.

## F. Distribution: reaching large numbers

| Tactic | Free or paid | Effort | Phase | Notes |
|---|---|---|---|---|
| Every bot page is pre-rendered and readable by search engines and AI crawlers | Free | Built in | 0 | Each bot is a findable page |
| "Built with NextXus" link on every bot and reply widget, linking to the builder with `?from=<id>` | Free | S | 0 | The core loop |
| "Make a bot like this" remix button on every bot page | Free | S | 1 | Copies the template, not the owner's data |
| Template marketplace page (one pre-rendered page per template, plus owners' shared templates after review) | Free | M | 1 | |
| How-to pages: WordPress, Shopify, Wix, Notion, Squarespace, plain HTML | Free | S each | 1 | Shopify: theme code or custom liquid, no app review needed. Wix and Notion embed rules UNVERIFIED (may need a paid Wix plan) |
| WordPress.org plugin (shortcode wraps the script tag) | Free | M | 2 | Must be GPL; review time UNVERIFIED |
| n8n: works today through the HTTP Request node; later a community node | Free | S then M | 1 then 2 | |
| Make: HTTP module; later a custom app | Free plan limits UNVERIFIED | M | 2 | |
| Zapier: generic webhooks; later a Zapier integration | Webhooks by Zapier may need a paid Zapier plan (UNVERIFIED); building an integration is free | L | 2 | |
| Telegram bots | Free | M | 1 | |
| Discord, Slack apps | Free to build; directory listing review UNVERIFIED | M | 2 | |
| OpenAI-compatible endpoint (drop-in for other software) | Free | M | 2 | The strongest "inside other software" route |
| Directory submissions (Product Hunt, Show HN, AI tool directories) | Product Hunt and HN free; many AI directories charge (UNVERIFIED) | S each | 2 | Any public posting needs Roger's approval |
| Affiliate loop: Gumroad affiliates on paid services; free-tier referrals earn extra free replies, not cash | Free | S | 2 | Gumroad affiliate setup on this account UNVERIFIED |
| Social bursts on Roger's connected accounts | Free | S | 1 | Roger approves each post |

## G. Scaling truth: what breaks, with numbers

**Shared Federation LLM pool, free, per day** (figures from `06-apis/llm-providers.yaml` and the Groq rate-limit page read 2026-10-05):
- Groq gpt-oss-20b: 1,000 requests and 200,000 tokens per day. gpt-oss-120b: the same. Limits are organisation-wide.
- SambaNova: 20 requests per day per selected model.
- OpenRouter free models: 50 requests per day in total.
- Gemini and Mistral free quotas: UNVERIFIED.

A bot reply costs about 1,200 tokens (covenant and gate prompt about 500, knowledge excerpts about 400, question and answer about 300; estimate, UNVERIFIED until measured). The token cap binds first: 200,000 / 1,200 is about 166 replies per Groq model per day. **The whole shared pool is roughly 400 to 450 bot replies per day.** That is enough for a few dozen active bots, not for thousands.

| Scale | What breaks | Mitigation |
|---|---|---|
| 1,000 bots | Shared pool: under 1 reply per bot per day. KV: 1,000 writes/day means per-message counters cannot live in KV. Bot pages: fine (about 70 KB each, about 70 MB). Relay: 100,000 requests/day is fine. Abuse: one script can drain the pool in minutes. | Shared pool is a **trial** only (decision 3: 20 replies per bot per day, global cap). After that the bot asks the owner to add a free key. Quotas counted in memory per relay instance plus a daily roll-up, not per message in KV. Per-IP and per-bot limits. Owner keys spend the owner's quota, not the Federation's. |
| 100,000 bots | Relay: 100,000 requests/day is 1 per bot per day. Pages: 100,000 × 70 KB is about 7 GB, far past the 1 GB site limit. One repo with 100,000 folders makes slow builds and big clones. Moderation: thousands of new configs per day. Account risk: one wave of spam bots could get the hosting GitHub account flagged, and if that account is Keywebco, every Federation site goes with it. | **Sovereign mode:** the owner deploys their own copy of the relay (one-click template on their own free Workers or Deno account) and their own bot repo on their own Pages. The Federation keeps only the directory, templates and gate code. Shard Federation-hosted bots across repos of about 10,000 bots. Host user bots on a **separate** GitHub account or org, never Keywebco (decision 2). Paid relay plan wired in but off. |
| Any scale | Free provider terms change, quotas vanish. GitHub Pages terms forbid using Pages mainly for commercial SaaS ([Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)). | Failover order from llm-router.yaml; fail closed with an honest message. Keep the free core non-commercial; paid things are sold on Gumroad, never through Pages. |

No uptime promise is honest on free tiers. The bot page says so.

## H. Safety and legal

| Risk | Control |
|---|---|
| Spam or scam bots | Every new or edited config enters **quarantine**. Automatic scan: blocklist, link check, template rules, and a free safety model where available (Groq lists gpt-oss-safeguard-20b on its free plan, 1,000 requests/day; account access UNVERIFIED). Clean, template-standard configs publish automatically. Flagged ones wait for human review (the Catalyst, with Roger's final word). |
| Prompt injection through knowledge links | Knowledge is fetched once at build time, size-capped, stored as plain markdown, wrapped as "untrusted reference text" in the prompt. No live browsing from chat in v0. |
| Draining the free pool | Per-bot daily quota, per-IP limit, request size cap (2,000 characters, same as plexus-relay `MAX_TEXT_LEN`), global daily cap, kill switch per bot. |
| Leaked keys | Keys only in vault and relay secrets. Nova runs a secret scan on every bot repo commit. Relay never returns a stored key. Lesson on record: ring-of-12-api had a key committed to public history (`ring-of-12-api/server.js` header). |
| Privacy | No conversation logs by default; only counts. Leads go straight to the owner's webhook or Telegram, not stored by the Federation. No cookies, no tracking. Session IDs are random and expire. |
| Harmful advice | High-stakes topics get a referral line; self-harm questions get a crisis line message (US 988) and no other answer. |
| Honesty to visitors | Every bot says it is an AI in its first message, shows its Truth Gate score, and links to the covenant. |
| Children | Terms set a minimum age of 13 (COPPA); bots are not designed for children. UNVERIFIED legal sufficiency. |
| Copyright | Owner confirms they may use the knowledge they supply. DMCA and abuse contact: keywebco@gmail.com. |
| Terms | Need: Terms of Use, Acceptable Use Policy, Privacy Notice, AI disclosure. Drafts are Phase 1 work. **Not legal advice; a lawyer has not reviewed this.** |

## I. Revenue, consistent with "give without reward"

| Layer | What | Status |
|---|---|---|
| Free core, forever | Builder, all templates, bot page, embed, Truth Gate, Telegram, REST, webhook, sovereign mode, unlimited use with the owner's own free key | Planned |
| Shared-pool trial | A small number of free replies per bot per day on Federation capacity | Planned |
| Paid, wired in but OFF | (1) Done-for-you bot setup, the same shape as the existing Build Nova and Build Sim service pages. (2) Federation-hosted capacity packs, which can only be switched on once paid LLM capacity exists and is covered by revenue (never resold at a loss). (3) Possibly the $5 Sovereign Token as a redeemable unit. | OFF |
| Never | Removing the "Built with NextXus" link, ads, selling data, tracking | Rule |

Gumroad is the source of truth. **No Gumroad listing for the Bot Builder exists.** Roger creates each listing; the relay unlocks paid features only by checking a Gumroad license key against the listing he made. The $5 Sovereign Token's Gumroad listing is UNVERIFIED: its legacy Gumroad URL returned 404 and its JIM route returned 200 (`04-builds/summary.md`, `04-builds/dead.md`). No buy link is written in this spec.

## J. Phased plan

Full detail, workers and acceptance tests are in `PHASES.md`.
- **Phase 0 (this week):** one template (faq-support), one relay with the Truth Gate v0 and one free provider, plain HTML builder form, bot page generator, one-line embed, REST. Done when one real person builds one FAQ bot and it answers on a page they control.
- **Phase 1 (weeks 2 to 6):** all 7 templates, quarantine pipeline, owner-key vault, failover across providers, Telegram, webhook out, template marketplace, how-to pages, terms drafts, second relay.
- **Phase 2 (months 2 to 4):** sovereign mode, OpenAI-compatible endpoint, n8n/Make/Zapier/WordPress/Discord/Slack, Truth Gate calibration test, sampled second check, referral loop, paid tier wiring (off).

Honest note on "which Nova worker does it": Nova workers today are check-and-report scripts. Code is written by a Catalyst-dispatched builder; Nova workers publish, check and watch. LLM-powered Nova work stays within the 20 requests/day free DeepSeek route on SambaNova until funded.

## K. Open decisions for Roger (7)

| # | Decision | Recommendation |
|---|---|---|
| 1 | Relay host for live chat: Cloudflare Workers, Deno Deploy, or Render | Workers primary (no sleep, 100,000 requests/day), same code on Deno Deploy as failover. Render only last resort (1-minute cold start). |
| 2 | Where user bot pages live | A **separate** GitHub account or org just for user bots, so a spam wave can never take down Keywebco. This needs an exception to the 2026-10-02 "no new repos" order. Fallback: a `bots/` folder in `Keywebco/nextxus-agent-zero` for Phase 0 only. |
| 3 | Free shared-pool allowance | 20 replies per bot per day, global cap 400 per day, first 30 days; then "add your own free key" (always free). |
| 4 | Owner keys | Accept them, encrypted on the relay, never shown again, with a plain notice that the relay operator could technically decrypt them. Do not allow keys in visitors' browsers. |
| 5 | Bots vs Sims, and the covenant text | Call them Bots, not Sims (Sims need Aria's soul layer and the 98 percent Replication Gate per `federation-browser-base/sims/README.md`). Covenant block = the three principles + DIR-000 + DIR-073, word for word. |
| 6 | Phase 0 provider account | Roger creates a free Groq account and puts the key in the vault as GROQ_API_KEY (proposed name in `06-apis/signups-needed.md`); SambaNova second. |
| 7 | First paid item | A "Done-for-you bot setup" Gumroad listing (Roger sets title and price), kept OFF until Phase 1 passes. Decide whether the $5 token is redeemable once its Gumroad listing is confirmed. |
