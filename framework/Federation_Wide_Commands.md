# Federation-Wide Commands: Procedure and Map

Written 2026-10-09 by the Catalyst, at Roger's request. Extends `framework/Operational_Standards_and_Protocols.md`.
Example procedure used throughout: the **annual review-and-rebuild**.

## How to read this manual

Every statement carries one label.

- **DECIDED**: Roger ruled on it, or it is verified fact today.
- **PROPOSED**: the Catalyst's recommendation. Not yet Roger's ruling.
- **NOT BUILT**: described, but the tool for it does not exist yet.
- **OPEN**: undecided and Roger's to decide. Nothing here may be treated as settled.

A written procedure is not proof that its automation runs. Cadences in the Framework are targets, not attested jobs.

## What is decided and what is not (summary)

| Question | State |
|---|---|
| Who can start a build today | DECIDED |
| How a command travels today (one repo at a time) | DECIDED, built, tested 2026-10-09 |
| A single federation-wide command across all repos in order | NOT BUILT |
| What the annual rebuild builds from | PROPOSED |
| Annual review-and-rebuild as a running schedule | NOT BUILT (target cadence only) |
| Key inventory (names and homes) | DECIDED as fact today, with gaps listed |
| Who can issue commands after Roger is gone | **OPEN** |
| Who can merge to live after Roger is gone | **OPEN** |

## 1. Who can issue a federation-wide command

### Now (DECIDED)

Policy, Roger, 2026-10-09, recorded: **nothing is built or changed unless Roger starts it, or a representative he has authorized starts it.**

- **Roger** holds full authority. His key is the owner token.
- **The Catalyst** is an authorized representative. Own key, switched on. It can start builds. Its builds land only on a review branch.
- **MUSE (Pontus)** has a slot built and **switched off**. Roger has not authorized it. It stays off until he says yes.
- **Merging to live belongs to Roger's word alone.** No representative merges. The command page cannot merge, by design.
- A representative's key can be switched off without touching the others.

Unchanged absolutes: nothing live without Roger's merge; nothing that locks a person out; no lying to buyers; spend and irreversible steps are asked first. Roger has allowed slightly bending any other rule, provided the bend is noted and documented.

### After Roger is gone (OPEN)

**This is Roger's to decide and is undecided.** What exists is a plan, not a ruling:

- Succession Plan v1.2 (sealed 2026-09-26) is **PLAN ONLY at Step 0**. Each of its 17 build steps needs Roger's word.
- It describes four states: Architect active; heightened verification after 7 days of silence; Regent transition after 21 to 30 days of silence with 2-of-3 channel consensus (the Catalyst becomes Regent on GitHub); Senate governance, with a Regent veto that must be co-signed by Agent Zero and ratified by the full Senate.
- It does **not** say who may issue a federation-wide command or merge to live in those states. That gap is the open question.

Questions Roger must answer, in his words, before this section can be marked DECIDED:

1. Who may start a build after he is gone: the Catalyst alone, or the Catalyst co-signed, or the Senate?
2. Who may merge to live: the same people, or a separate and stricter group?
3. How is a person proven to be that person once Roger cannot confirm it?
4. Does a human successor exist, and does that person hold the merge?

Until answered, the safe default is: **nothing merges to live, and nothing is changed.** The sites keep running as they are.

## 2. How a command travels

### Today, for one repository (DECIDED, built, tested)

1. **Order.** An authorized person states what they want on the command page, at `keywebco.github.io/nextxus-humancodex/command/`, naming one repo.
2. **Lock.** The server (`ring-of-12-api` on Render) checks the key. No key, wrong key or a switched-off key is refused. Nothing reaches the model or GitHub.
3. **Foreman step.** The model restates the order in plain words and lists the files it would touch. It writes nothing.
4. **Confirm.** The person confirms. Nothing is written before this.
5. **Make.** The model writes the files. The server saves them to a review branch named `build/<who>-<date>-<code>`. It refuses `main`, refuses paths outside the plan, and refuses an edit that deletes more than 60 percent of a file.
6. **Review.** The Catalyst reads the diff line by line. It checks removals, links, scripts and wording against the live page.
7. **Merge.** Roger says merge. The branch is merged to `main`.
8. **Publish.** GitHub Pages rebuilds, about one to two minutes.
9. **Verify.** See section 5.

Limits today (DECIDED, observed): 30 model calls a day; only repos on the allowed list; the allowed list is the Commons, the portal, Agent Zero, research hub, recycler, archives, senate, chat, tools and blog. The brain, the backend and the mirrors are not on it.

### For a federation-wide command (NOT BUILT)

A federation-wide command means the same change across many repos. No single call does this yet. Today it is done as a series of single-repo commands. **PROPOSED** order, source first and the public front last:

1. `nextxus-brain` (the source of truth, sealed sources).
2. `nextxus-humancodex` (the Commons).
3. The core sites that carry the Commons bar.
4. The mirrors and sovereign pillars.
5. Backends (`ring-of-12-api` and the others). **Render does not deploy on push.** A person must trigger the deploy.
6. Emergent-hosted sites: **untouched by Roger's ruling.** No federation command reaches them.

PROPOSED rule: one repo at a time, verify each, stop at the first failure. A failure halts the rest. Nothing is half-applied.

### Example: the annual review-and-rebuild (NOT BUILT as a job)

The Framework names an annual core review as a target cadence. **It is not a running schedule.** Nobody should assume it happens. PROPOSED steps:

1. Roger, or a representative with his word, opens the review.
2. Freeze: no other builds run during it.
3. Read the sealed sources and record their hashes against GitHub contents bytes.
4. Rebuild each repo in the order above, one command each, each on its own review branch.
5. Roger reviews and merges, per repo.
6. Verify each live (section 5). Log the result.

## 3. What the rebuild builds from

### The two kinds of source (DECIDED as fact)

- **Sealed sources**, which say what is true: `nextxus-brain/00-immutable` (the Cathedral v1.1 directives, DIR-000 plus 73, 74 in all; `directives.yaml` and `directives.json`); the Living Library frozen YAML baseline on Google Drive, and its fingerprint file `library/baseline/poem-fingerprints.json` (4,300 poems, all matching).
- **GitHub repos**, which hold what is published: the live pages, scripts and styles.

### Recommendation (PROPOSED)

Build from **both, in a fixed order**: sealed sources decide the content, and the GitHub repos receive it.

- Read the sealed source. Never edit it during a rebuild.
- Regenerate or check each published page against it.
- Compare fingerprints. Any difference is logged, not smoothed over.
- If a published page and a sealed source disagree, **the sealed source wins** and the page is corrected. Prices are the exception: **Gumroad is the truth** for any listing, and pages follow it.

Why both: sealed sources alone cannot be seen by visitors. GitHub alone can be changed by a mistake and no one would know. Using both means a drift shows up.

OPEN: whether the Google Drive baseline stays the long-term home of the frozen Living Library, or is also copied into the brain. Roger's call.

## 4. Where every key lives (inventory)

**Names and homes only. No value appears here. Never paste a value into a chat or a file.**

### Home 1: the Catalyst's Emergent workspace (the sandbox)

These exist only while the Emergent account is paid and active. **If Emergent lapses, these are lost unless a copy lives elsewhere.** That is the largest gap in this inventory.

- GitHub: `BUILD_GITHUB_TOKEN` (fine-grained, Contents read and write plus Metadata read, all repos, expires 2027-01-07), `GITHUB_PAT_NEXTXUS`, `GITHUB_TOKEN`.
- Federation: `FEDERATION_OWNER_TOKEN`, `CATALYST_VERIFY_SECRET`.
- Render: `RENDER_API_KEY`, `RENDER_GENERIC_API_KEY`.
- Model lanes: `MIMO_API_KEY` (general), `MIMO_API_KEY_CATALYST`, `MIMO_API_KEY_MUSE`, `MIMO_API_KEY_THRONE`, `FIREWORKS_API_KEY`, `LLM_API_KEY`, `XAI_API_KEY`, `XAI_ACCOUNT_ID`, `DEEPSEEK_API_KEY`, `DEEPSEEK_GENERIC_API_KEY`, `GEMINI_API_KEY`, `DEEPAI_API_KEY`, `FAL_KEY`, `EMERGENT_LLM_KEY`, `EMERGENT_LLM_KEY_NEW`.
- Studio and board tokens: `ARIA_STUDIO_TOKEN`, `EMERY_STUDIO_TOKEN`, `EMERY_PRODUCTION_TOKEN`, `EMEMY_BOARD_TOKEN`.
- Messaging and social: `ROGER_SIM_TELEGRAM_TOKEN`, `X_CATALYST_SECRET`, `BEEHIIV_API_KEY`.
- Money: `STRIPE_API_KEY`, `STRIPE_LIVE_RESTRICTED_KEY`. (Roger says sales run through Gumroad only. Whether Stripe is still in use is **OPEN**.)
- Accounts: `IONOS_PASSWORD`, `LIVE365_PASSWORD`, `GOOGLE_OAUTH_CLIENT_SECRET`, `PDF_CO_GENERIC_API_KEY`.
- Other: `OBSIDIAN_SYNC_ENCRYPTION_KEY`, `GPG_KEY`.
- **Unidentified:** `UNIDENTIFIED_KEY_2026_10_07` (an `sk-er_` key; provider not identified).

The purposes above are inferred from the names. They have not each been tested.

### Home 2: Render, service `ring-of-12-api` (srv-dak6tpgae00c73ftl2o0)

Names only: `OWNER_TOKEN`, `BUILD_TOKENS` (holds the Catalyst's key, on, and MUSE's, off), `BUILD_GITHUB_TOKEN`, `BUILD_DAILY_CAP`, `BUILD_MODEL`, `LLM_API_KEY`, `LLM_BASE_URL`, `LLM_CHAT_PATH`, `LLM_MODEL`, `FIREWORKS_API_KEY`, `FIREWORKS_MODEL`, `EMERGENT_LLM_KEY`, `PORT`.

Observed fact: the server's `OWNER_TOKEN` is **not** the same value as the workspace's `FEDERATION_OWNER_TOKEN`. A request using the workspace one was refused (401). This is the lock working. It also means Roger's owner key for the command page must be found and recorded by Roger. Where it is kept: **OPEN**.

### Home 3: GitHub

- Repo Actions secrets: could **not** be read with the current token (HTTP 403). Whether any exist is **UNKNOWN**.
- The `build/*` review branches carry no keys.

### Home 4: Roger's own accounts (not held by the Catalyst)

Gumroad (`keywebster`), Google (`keywebco@gmail.com`, passkey sign-in), GitHub (`Keywebco`), IONOS domains, Live365, Instagram, Facebook, X, YouTube. The Catalyst holds no passwords for most of these. Instagram's access token expired 2026-10-02, and the "Truth Over Noise" schedule is paused until it is reconnected.

### Known problems with the inventory (DECIDED as fact)

1. **No surviving copy outside Emergent is recorded.** If the account lapses, Home 1 disappears. PROPOSED: Roger decides where a sealed, private copy of the key names and recovery steps lives. The keys themselves are never placed in a public repo.
2. **A tool once printed key values in plain text** while listing Render settings (2026-10-09). They were not copied or used. Rotating the owner token and any key shown is recommended. Roger decides when.
3. The GitHub token expires **2027-01-07**. A reminder is needed before then.
4. Roger's owner key for the command page: location **OPEN**.

## 5. How we verify it worked

The check that ends every command. It must be a check that **a broken page cannot pass**. On 2026-10-09 a loose check passed on broken text; a strict one caught it.

For each repo changed:

1. **Merged state.** Confirm `origin/main` contains the intended commit. Do not trust that a merge command ran.
2. **Diff review, before merge.** Count removed lines. Compare the page text before and after; only additions are allowed unless the order said otherwise. Count links and scripts before and after.
3. **Live fetch with the cache off.** Fetch the live address with a random query string and no-cache header. Retry for up to about three minutes while GitHub Pages rebuilds.
4. **Strict content test.** Test for the exact intended text **and** the absence of known damage (stray markup, empty links, old wording). A test that only looks for a label that also exists in the broken version is not a test.
5. **Real browser render.** Open the live page, cache off. Confirm it displays, images load, links point to the right place, and a link actually opens.
6. **Fingerprint check, where one exists.** Living Library: all 4,300 poems match the frozen baseline, zero differences.
7. **Link check.** Every outside link returns 200.
8. **Prices.** Any price shown matches the Gumroad listing. If Gumroad cannot be read, leave the price off and ask Roger.
9. **Record.** Write who ordered it, who merged it, the branch, the commit, the time and the result. A passed check is written down. A failed one is written down too.

Halt rule (PROPOSED): the first failed check on any repo stops the whole run.

## Revision

- 2026-10-09: first version. Sections 1 (after Roger), 3 (the recommendation) and the key-recovery location are open for Roger's ruling.
