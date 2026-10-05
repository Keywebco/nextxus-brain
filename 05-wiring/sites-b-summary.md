# GitHub hub and tool wiring, first-pass audit (2026-10-05)

**Scope:** 38 requested repos. GitHub Pages homes: 31 HTTP 200, 7 HTTP 404. One requested repo, `Keywebco/ring-of-six`, was not found via GitHub integration. The other six 404s are existing non-Pages backend/workflow repos, not necessarily dead services. This is **PARTIAL**, not an every-button acceptance test. Buttons and POST routes were read from source, not clicked or executed.

## Top problems

1. **HIGH, leaked Ring key:** `ring-of-12-api/server.js` explicitly states an `LLM_API_KEY` was committed to public git history. Revoke/rotate that key and verify deployed service uses the replacement. No key value was read into these deliverables. Health GET was 200 with `llmConfigured:true`; `/ask` and `/single` POST were not executed.
2. **Dead legacy Ring paths:** `nextxus-lasting-edition/ring-of-three.html` POSTs to a transient `trycloudflare.com` URL, curl returned 000. Its `ring-of-12.html` POSTs to an Emergent preview `/api/codex`, GET returned 404 (POST remains unverified). Its Zeus/Hera roster conflicts with the current Ring API's Mnemosyne/Themis roster; neither historical page is 01-rings canon.
3. **Unimplemented email route:** `ring-of-12/ask.html` calls `POST /subscribe`, but `ring-of-12-api/server.js` implements only `/ask`, `/single`, `/log`; GET `/subscribe` returned 404. No report form was submitted.
4. **Old YAML dependency:** eight `nextxus-free-satellites` files still reference `keyhole-creator/nextxus-yaml-database@main/loader.js` (jsDelivr HTTP 200). This is a live old source dependency, not the new brain. `data/directives.json` contains just 15 selected records, not 73 complete directives. `data/senate.json` hardcodes a 12-domain roster and names its chamber “Ring of 12”, mixing governance and reasoning concepts.
5. **State/roster drift:** `nextxus-sim-api` initializes five braid items in code and stores messages in memory, resetting on redeploy. `plexus-relay` has a separate `ROSTER` env default of Roger/Catalyst/Pontus/Aria and a GitHub mirror whose configuration needs independent check. Meeting-room boards read and write that relay. Brain 03-minds and 02-senate need distinct feeds.
6. **Source mismatch:** `federation-mind-mirror` Pages displays many generated HTML document links, while its main branch tree contains only `README.md` and `blueprint.html`. Publishing source/branch is unresolved.
7. **Unsafe conditional auth:** `federation-n8n/server.js` authorizes all requests when neither `FEDERATION_AUTH_CODE` nor legacy `FEDERATION_MASTER_AUTH_CODE` is configured. Deployment and current env configuration were not verified.
8. **Other stale public copy:** `nextxus-blog` links a historical “70 Sacred Directives” article. Do not treat that old headline as a current count. A free satellite references retired `nextxus.one`. `sovereign-knowledge-os` exposes a 64-item Echo Core roster, which is a duplicate index, not authoritative brain state.

## Ring of 12 exact wiring

`POST https://ring-of-12-api.onrender.com/ask` accepts JSON `{"question":"nonempty string <=2000 chars"}`. `server.js` sends system prompt plus user question to `https://integrations.emergentagent.com/llm/v1/chat/completions` with model `gpt-4o-mini`, `temperature:0.8`, `max_tokens:3000`; parses JSON, strips optional fences, checks at least 12 `seats` and `synthesis`, then returns `{seats:[{seat,name,zodiac,answer}],synthesis}`. `POST /single` accepts the same question, calls the same LLM model with a one-perspective prompt, `temperature:0.7`, `max_tokens:400`, returns `{answer:string}`. `POST /log` accepts question/rating/comment metadata and appends a local JSONL line, max 30 per minute per IP. `LLM_API_KEY` is required, `PORT` optional. The live root GET returned HTTP 200 and `llmConfigured:true`; actual LLM completion remains **UNVERIFIED**.

## Verification boundaries

All 38 Pages home statuses were checked with curl. 109 distinct sampled link targets were checked by curl in the local audit. The published YAML carries a subset of labeled link checks, not every link. All buttons/forms that mutate or spend money were **not** exercised. Nested pages in large repos, generated mirror docs, every song/blog/store link, workflows, and all server environment secrets remain **UNVERIFIED**. No other repo or live site was changed.

## Sampled broken link targets (curl, do not infer app action)

No 0/404/410 among sampled ordinary links, this does not mean all links work.

## Source pointers

- Ring API: `https://github.com/Keywebco/ring-of-12-api/blob/main/server.js`.
- Old satellite loader and copied data: `https://github.com/Keywebco/nextxus-free-satellites/`.
- Relay persistence: `https://github.com/Keywebco/plexus-relay/blob/main/github-store.js`.
- SIM backends: `https://github.com/Keywebco/nextxus-sim-api/blob/main/main.py` and `https://github.com/Keywebco/roger-sim-api/blob/main/server.js`.
- Each site entry in `sites-b.yaml` has its Pages HTTP status, purpose, brain layer, and selected page/control evidence. The file-wide source URL pattern and PARTIAL coverage warning apply to every entry.