# NextXus GitHub Operational Systems Manual

Version 1.0, 2026-10-09. Written by the Catalyst at Roger's direction. Lives in `nextxus-brain/framework/`.
Companion files: `Federation_Wide_Commands.md` (the command procedure, section 7 here summarizes it) and `04-builds/github-operations.yaml` (the same facts as machine-readable records).

## 0. How to read this manual

Every statement carries a label.

- **VERIFIED** (with a date): checked directly on the stated day. Re-check before relying on it later.
- **DECIDED**: Roger ruled on it.
- **PROPOSED**: the Catalyst's recommendation. Not Roger's ruling.
- **NOT BUILT**: described, but the tool does not exist.
- **OPEN**: undecided, Roger's to decide.
- **UNVERIFIED**: stated by a source but not tested, or two facts disagree and the cause is unknown.

Rule: never write a status without the check that backs it. A written procedure is not proof that its automation runs.

**Design rule (Roger, 2026-10-09): every single point of failure must have an alternative solution. A singularity with an alternative is far stronger than one without.**

A single point of failure can never be removed entirely; something always has to be the one thing. The test for each one is whether it has a second way to work. Section 10 is read against this rule. Working examples: the brain's daily GitHub check (runs with no Emergent and no Render) and the Living Library (runs in the browser from files, so no server failure takes it down). Weak examples, with no second way yet: the key copies, Roger's owner key, and the command page's dependence on Render.

## 1. The purpose, in plain words

Roger works from GitHub. Emergent is kept running for his lifetime (DECIDED, 2026-10-09), but nothing may depend on it to keep the Federation alive. The goal is that the Federation can be changed, repaired and grown from GitHub plus a cheap model, with no Emergent account. That goal is **partly met** (section 2).

## 2. What exists today (VERIFIED 2026-10-09)

### 2.1 GitHub

- Account `Keywebco`: 58 repositories. 47 have GitHub Pages sites; every one returned HTTP 200.
- The full list, with a one-line description of each and its address, is in the shared Google Doc "NextXus Federation: all GitHub sites, most important first" and in `04-builds/sites.yaml` and `05-wiring/`.
- **The front door is the Commons**: `https://keywebco.github.io/nextxus-humancodex/` (DECIDED). Every other site carries a slim "Commons bar" at the top that links back to it. 18 sites carry it (VERIFIED 2026-10-08).
- The free Living Library is at `.../nextxus-humancodex/library/`. The Core page is at `.../core/`. The command page is at `.../command/`.

### 2.2 The brain (`Keywebco/nextxus-brain`, public)

Layers: `00-immutable` (Cathedral v1.1, DIR-000 plus 73, 74 in all, sealed with SHA-256, never edited); `01-rings`; `02-senate` (policies and procedures); `03-minds`; `04-builds` (sites, tools, products, books, music); `05-wiring`; `06-apis`; `07-botbuilder` (spec only); `framework/` (this manual and the standards).

### 2.3 Render (the small servers)

14 services, all running, none suspended, all on the free plan or static (VERIFIED 2026-10-09):

- Web services (6): `ring-of-12-api` (the Ask and Council API, the library keys code, the command page backend), `nextxus-sim-api`, `roger-sim-api`, `nextxus-sim-telegram`, `plexus-relay-api`, `federation-gatekeeper`.
- Static sites (8): `federation-app-vault`, `nxs-emmy-board`, `nxs-staging`, `nxs-federation-hub`, `nxs-truth-gate-core`, `nxs-ai-course-hub`, `nxs-ai-minds-lab`, `nxs-unified-storefront`.

Free web services **fall asleep** when idle. The first request after a quiet time can take about a minute. This is normal, not a fault (VERIFIED: the first call to `ring-of-12-api` took about 22 seconds on 2026-10-08).

**Deploy behavior, UNVERIFIED.** Render's setting for `ring-of-12-api` is `autoDeploy: yes`, trigger `commit`, branch `main`. But on 2026-10-09 a push to `main` did **not** deploy; the server kept the old code until a deploy was triggered by hand, and every deploy in its history shows trigger `api`. The two facts disagree and the cause is unknown. **Rule until explained: after any change to a backend, trigger the deploy by hand and check the live behavior. Never assume a push deployed.**

### 2.4 Emergent

Roger's Emergent account holds 35 jobs (March to August 2026), mostly rebuilds and renames of the same few things. The six public domains (`nextxus.online`, `.org`, `.tech`, `.space`, `.studio`, `.help`) run there and are indexed by Google. Roger has ruled: **no domain changes and no edits to them** (DECIDED, 2026-10-09). Gumroad is the only payment system; Emergent has none.

`nextxus.online` is **one single page** that answers every address with the same file (97,508 bytes, VERIFIED 2026-10-09). Its ticker figures are fixed in the code and must not be copied as live facts.

### 2.5 Money

All sales go through Gumroad (`keywebster.gumroad.com`). **Gumroad is the truth** for any listing: titles, prices and descriptions on Gumroad win, and every page adjusts to match (DECIDED). Sites link out and never take payment.

## 3. The two worlds of work

| | Emergent | GitHub plus Render plus a model |
|---|---|---|
| Who does the work | The Catalyst, a full AI with judgment | The command page, with a model writing the code |
| Cost | Credits, paid by Roger | Cents of model use; free hosting |
| Survives if Emergent lapses | No | Yes, once the keys are saved elsewhere |
| Quality | Highest | Good on small jobs; **reviewed by a person every time** |

Honest limit: the GitHub path has **more moving parts, not fewer** (Render, the model provider and GitHub, instead of one paid account). It is cheaper and the published pages last longer, but the build pipeline is more fragile. It is a trade, not a pure gain.

## 4. How a change is made (the command page)

Built and tested 2026-10-09 (VERIFIED). Address: `.../nextxus-humancodex/command/`. Backend: `ring-of-12-api` on Render.

Steps: order, lock, foreman restates, confirm, build onto a review branch, review, merge, publish, verify (full detail in `Federation_Wide_Commands.md`).

Built-in safeguards (VERIFIED in code and by test):
- Refuses any request without a valid key, a wrong key, or a switched-off representative's key. None of those reach the model or GitHub.
- Never writes to `main` or `master`. Branches are named `build/<who>-<date>-<code>`.
- Only the repos on the allowed list: the Commons, the portal, Agent Zero, research hub, recycler, archives, senate, chat, tools, blog.
- Refuses an edit that removes more than 60 percent of a file.
- A daily limit of 30 model calls.
- Merging to live is **not possible** from the page. That is Roger's word alone.

**Known weaknesses seen in use (VERIFIED 2026-10-09):**
1. The model sometimes "fixes" something nearby without being asked, in a way that hides the problem. It silently altered a broken Gumroad line and left an empty link.
2. It leaves the build summary blank.
3. It can invent wording if the order is not exact. It must be given the text to use.
4. It never checks that its own work is right.

Therefore: **a person or the Catalyst reads the diff before every merge**, and the live result is checked with a strict test (section 8).


## 4A. The GitHub command hub (Option B): built, NOT YET INSTALLED

State: the files are on the review branch `hub-command-build-2026-10-09`. They are **NOT BUILT as a running thing** until Roger merges them and two secrets are set. Nothing here has run on GitHub yet. What has been tested: the workflow passes `actionlint`, and the script was tested against a mock model (good order, wrong site, path escape, workflow-file touch, too many files, a model that deletes most of a page, junk output, an empty answer, no key). Every refusal worked. **It has not been run against the real model or the real GitHub.**

What it is: one workflow in the brain (`.github/workflows/command-build.yml`) that builds into the other sites. It is started by hand from the Actions tab, or by pushing a branch named `order/<anything>` that holds `.orders/order.json`. It checks that the starter is on the approved list, asks the model for the change, and saves it to a **review branch** of the target site named `build/<who>-<date>-<run>`. It never writes to `main`. Roger merges. A leftover summary file is no longer written into the site.

Why one hub: GitHub keeps secrets per repo. One hub means two secrets set once, one place to protect and one place to move.

Needs, before it can run:
1. Roger merges the hub files into the brain.
2. Secret `MIMO_API_KEY` in the brain's Actions secrets (the model key).
3. Secret `BUILD_GITHUB_TOKEN` in the brain's Actions secrets: the narrow key, Contents read and write. **It must be allowed to write to each site the hub builds into.** Today that token covers all repositories.
4. Variable `BUILD_APPROVED_ACTORS` (a plain setting, not a secret) listing who may start a build, comma separated. Start with `Keywebco`.

Sites the hub may build into (the same list as the command page): nextxus-humancodex, keywebco.github.io, nextxus-agent-zero, nextxus-research-hub, nextxus-recycler, nextxus-archives, nextxus-senate, nextxus-chat, nextxus-tools, nextxus-blog.

Known limits: a workflow takes tens of seconds to start; it cannot serve live Ask or council tools (those still need a server); the model has the same weaknesses as on the command page, so **every diff is read before merge**.

## 5. Keys and secrets

See `Federation_Wide_Commands.md` section 4 for the full inventory. Summary:

- Names and homes only are ever written down. **A key value is never put in a chat, a repo or a document.**
- Most keys live **only** in the Catalyst's Emergent workspace. If the account lapses they are lost unless Roger keeps a private copy elsewhere. **OPEN: where.**
- Render holds its own copies for the services it runs.
- The command page's GitHub key expires **2027-01-07**. Renew before then.
- Roger's owner key for the command page: its location is **OPEN**.
- A tool once displayed key values in plain text (2026-10-09). Rotating those keys is recommended; Roger decides when.

## 6. Scheduled jobs (VERIFIED 2026-10-09)

20 jobs run on the Emergent side (not GitHub). 17 active, 2 auto-paused, 1 paused. They include the site health monitor (every 4 hours), the sentinel pulses, the daily briefing and pulse, the marrow and system-evolution jobs, and the social campaigns.

- **"NextXus Social Campaign: Truth Over Noise"** is auto-paused: its Instagram access token expired 2026-10-02. It resumes only after Roger reconnects Instagram.
- **"Chronicle Ritual Pulse"** is auto-paused.
- **"Gumroad Daily 10-Task Feed"** is paused.
- **These jobs stop if the Emergent account lapses.** They are not a GitHub system.
- **GitHub health check, built 2026-10-09 (branch `health-check-2026-10-09`; runs only after Roger merges it).** 43 checks every 4 hours on GitHub's own workers: the Commons and 17 sites (each must still carry the Commons bar), the library data, the Core and command pages, the portal's two books, the Render servers (the command page's lock must answer 401 with no key), five Gumroad listings, and the seven Emergent domains (watched only, never edited). A free server that was asleep is retried before it counts. A page that answers 200 is also checked for a phrase it must hold and damage it must not. The report is `LATTICE/reports/health.md`; one issue opens on failure and is not duplicated. **Tested:** all 43 pass against the live Federation, and it correctly fails on a missing phrase, known damage, a dead address, a missing server and a wrong status. **It has not yet run on GitHub's workers.**
- There is **no scheduled annual review-and-rebuild** (PROPOSED cadence only).

## 7. Federation-wide commands

Detailed in `Federation_Wide_Commands.md`. In short:

- **Now (DECIDED):** only Roger, or a representative he authorizes, starts a build. The Catalyst is authorized, on a review branch only. MUSE's slot is built and off. Merging is Roger's alone.
- **After Roger is gone (OPEN):** nothing is decided. The safe default is that nothing merges and the sites keep running.
- **A single command across all repos: NOT BUILT.** Today it is a series of single-repo commands, source first, public front last, stopping at the first failure.

## 7A. The repair exception (auto-merge): DECIDED by delegation, NOT BUILT

**Provenance.** On 2026-10-09 Roger said every rule has exceptions written into it, and asked Pontus (MUSE) to decide the repair-authority question. Pontus decided yes, with the five terms below. Roger has not yet restated it in his own words, and he can overrule it. The Catalyst recorded it and agrees, with the extra safeguards in the second list, which are PROPOSED and not part of what was decided.

**Purpose.** An immune system that fights and also reports: when the health check finds a break, the hub prepares the fix by itself and tells Roger, and can keep working when he cannot be there.

**The exception to "nothing merges without Roger's word" (DECIDED, five terms):**

1. The hub may auto-merge ONLY fix classes the health check itself can verify: a required phrase restored, a link live again, a known damage pattern corrected and confirmed. The verifier decides.
2. Every fix goes through a review branch first, so there is full history and a one-command revert.
3. Every auto-merge is reported to Roger. Closing the notification gap is part of building this, not later.
4. Anything the check cannot verify waits for Roger's word. No exception.
5. Roger can revoke the whole exception with a word, at any time.

**State today (VERIFIED 2026-10-09):** nothing is built. The health check only detects and reports. No repair worker exists and nothing auto-merges. The notification gap is real: the check opens a GitHub issue, but whether Roger receives an email for it is UNVERIFIED (the brain repo shows no explicit watch subscription, HTTP 404).

**The Catalyst's proposed safeguards (PROPOSED, for Roger to accept or change):**

a. A written list of eligible fix classes lives in the repo. Anything not on it is not eligible. Classes are added one at a time, and each is tested with a deliberate failure before it is switched on.
b. The code that verifies a fix is separate from the code that writes it. It checks the review branch before the merge and the live page after.
c. If the live check fails after an auto-merge, the merge is reverted automatically and reported.
d. A fix may touch only the file the failing check names. It may not touch workflow files or secrets, and it refuses any edit that removes more than 60 percent of a file.
e. A daily limit on auto-merges, and a stop after two failures in a row, then wait for Roger.
f. The verifier compares the whole page with its state before the fix, not only the phrase. On 2026-10-09 the model "fixed" a broken Gumroad line in a way that hid it. A phrase-only check would have passed that.

**Honest limit.** A passing check proves only what it checks. This exception widens what a machine may change without a human reading it, so it should start with the narrowest class and grow slowly.

## 8. How to verify that a change worked

A check that a broken page cannot pass (VERIFIED as a lesson 2026-10-09).

1. Confirm `origin/main` holds the intended commit.
2. Read the diff before merging: removals, links, scripts, wording.
3. Fetch the live page with the cache off; retry up to about three minutes for GitHub Pages.
4. Test for the exact intended text **and** the absence of known damage.
5. Open it in a real browser: it renders, images load, a link opens.
6. Fingerprint check where one exists (Living Library: 4,300 poems, 0 differences).
7. Every outside link returns 200.
8. Any price matches the Gumroad listing. If it cannot be read, leave the price off and ask Roger.
9. Write down who ordered it, who merged it, the branch, the commit, the time and the result.

## 9. Recovery: what to do when something breaks

1. **A page looks wrong after a merge.** Revert the merge commit on `main`. GitHub Pages restores the old page in about two minutes. Nothing is lost; every old version is in the history.
2. **The command page says it cannot reach the server.** The Render server is probably asleep. Wait about a minute and retry. If it stays down, check Render's dashboard.
3. **The server answers "not authorized".** Wrong or missing key. Never share the key to fix it. Switch the representative's key off and issue a new one.
4. **A backend change did not take effect.** Trigger the deploy by hand (section 2.3).
5. **An Instagram or other token has expired.** The job pauses itself. Roger reconnects the account, then the job is resumed.
6. **Emergent stops.** The GitHub sites, the Render servers and the library keep running. The scheduled jobs and the Catalyst on Emergent stop. The command page keeps running on Render, but it can only be used by someone who holds a valid key, and the model key it needs is stored on Render itself. Whether Roger's own owner key survives depends on where he keeps it (OPEN, section 10). Without a person holding a key, nothing can be built; the published sites still stand.
7. **A rule must bend to get something done.** Allowed (DECIDED, Roger, 2026-10-09), if the bend is slight, noted and documented. Never bendable (with one written exception for verified repairs, section 7A): nothing live without Roger's merge; no lying to buyers; nothing that locks a person out; ask before spending money or taking an irreversible step.

## 10. Open items for Roger

1. **Who commands and merges after he is gone.** (OPEN)
2. **Where a private copy of the key names and recovery steps lives**, so an Emergent lapse does not lose them. (OPEN)
3. **Why Render did not auto-deploy on push.** (UNVERIFIED)
4. **Whether Stripe is still used.** (OPEN)
5. **Rotating the keys a tool displayed in plain text.** (his timing)
6. **Reconnecting Instagram**, so the social campaign can resume.
7. **Merge the GitHub health check**, so monitoring does not depend on Emergent. (built, waiting on his merge)
8. **MUSE's authorization** on the command page. (OPEN, switched off)
9. **Intent (Roger, 2026-10-09), not a ruling:** the Senate is meant to become a conversation of this kind: minds talking a matter through, one proposing, another reading it closely, and a person deciding. How seats, speech and decisions work in it is OPEN.

## 11. Revision log

- 2026-10-09: added section 7A, the repair exception (decided by Pontus at Roger's delegation; not built).
- 2026-10-09, v1.0: first complete version. Corrects the earlier statement in `Federation_Wide_Commands.md` that Render "does not deploy on push": the setting says it does, observation says it did not, cause UNVERIFIED.
