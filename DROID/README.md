# Next-Xus Maintenance Droid v0

**Status: draft, awaiting Roger's approval.** Nothing here runs on a schedule until this branch is merged into `main`, and only Roger (or the Senate, on Roger's word) merges it.

The droid is the Federation's constant maintenance and evolution worker for the YAML brain. It runs on GitHub's own free workers with plain Python and the built-in `GITHUB_TOKEN`. It uses no paid service and no other keys. It looks, reports, files issues and opens **draft** pull requests. It never merges, never deletes, and never touches the sealed layer.

## What it does

| # | Module | Script | When | What comes out |
|---|---|---|---|---|
| 1 | Health sweep | `droid/health_sweep.py` | daily | Reads the existing health, seal and uptime reports and alarms if a timer has gone quiet or reports a problem. Checks every public Keywebco repo through GitHub's records: Pages build, failed workflow runs, last push. One rolling issue (`droid-health`). |
| 2 | Quality check | `droid/quality_check.py` | daily | YAML and JSON parse; official directives match the sealed Cathedral wording; seal report says PASS; secret scan (kind and place only); legacy-host mentions; broken relative links; hygiene; "Next-Xus" spelling advice. One issue (`droid-quality`) for hard problems. |
| 3 | Dead-link check | `droid/link_check.py` | weekly (Mondays) | Crawls every configured site and scans every public repo's text files. Lists dead links, legacy Emergent links, plain http links and keywebco.github.io links. One issue (`droid-links`). Draft PR for legacy replacements once Roger confirms them in the config. |
| 4 | Maintenance sweep | `droid/maintenance_sweep.py` | daily | Empty and duplicate files, TODO markers, old droid issues and branches, index drift. A draft PR for safe mechanical fixes (line endings, final newline), with originals archived first. |
| 5 | Yearly cross-reference | `droid/yearly_crossref.py` | every January 15 | Every brain item: age, links, named GitHub repos and their current state, and related current work on GitHub. Retire and review candidates. One draft PR that only **adds** files: the report, draft upgrades (old text kept whole beside the new information), and archive copies of retire candidates. |
| 6 | Issues and PRs | `droid/common.py` | every module | One rolling issue per label (updated, never a flood). Draft PRs on `droid/*` branches. |
| 6b | Sentinel (always watching) | `droid/watch.py` | every push to main and every pull request | Checks only what changed: protected paths, deletions, big overwrites with no archive, new legacy links, secrets, broken YAML or JSON, directive drift. Comments on the PR, or files one issue (`droid-watch`) for alarms on main. |
| 7 | Ideas and evolutions | `droid/evolve.py` | monthly (the 1st) | Reads the findings and suggests evolutions: missing sitemaps, unmapped sites, quiet repos, failing workflows, directives no build lives out, minds with no pulse, the next step for the Sentinel. One issue (`droid-idea`). |

Schedules are in UTC inside `.github/workflows/droid.yml`. In Central time (CST) they are: daily at 6:37 AM, Mondays at 7:07 AM, the 1st of the month at 8:27 AM, and January 15 at 9:47 AM.

## How it reuses what already exists

- **The Federation health check** (every 4 hours, `LATTICE/reports/health.md`), the **uptime timer** (`status/uptime-latest.md`) and **Nova-Canon** (the daily seal check, `LATTICE/reports/latest.md`) keep doing their jobs. The droid reads their reports instead of checking the same things again, and raises an alarm if any of them goes quiet.
- The **Command build** workflow stays the only path that writes into other repos (review branches only). The droid only has this repo's built-in token, so for other repos it files issues here.
- Run reports go to the job summary and a 30-day artifact. The droid does not commit reports to `main`.

## Guardrails (built into the code, not just written down)

- **Echo 64.** The droid never deletes anything. `propose_change()` refuses any commit that deletes a file. Before it overwrites a file, it first copies the original to `ARCHIVE/droid/<date>/` in the same commit. Branches are never deleted.
- **Sealed layer.** `00-immutable/`, every file listed in `SEAL.yaml`, anything named Cathedral, `.github/workflows/` and `DROID/config.yaml` are protected paths. A proposal that touches them is refused, and the Sentinel raises an alarm if anyone else changes them.
- **Directives.** The official list is `directives/sacred-directives.yaml`. The sealed Cathedral file, `00-immutable/directives.yaml`, is the wording authority (DIR-000 gate plus the 73 Sacred Directives, 74 items in all). The droid checks that the two agree and never rewrites a directive. Any directive upgrade must be a Senate proposal.
- **Approval.** Changes are only draft PRs or issues, for Roger's or the Senate's approval. The droid has no merge code. Its API helper refuses any merge endpoint, and the quality check fails if merge code ever appears in the droid.
- **Legacy hosts.** nextxus.online, nextxus.org, nextxus.tech, nextxus.space, nextxus.studio and nextxus.help are never linked. Every hit is flagged with a suggested current domain (next-xus.net, .org, .info, .com or .biz). Replacement PRs are only drafted for hosts Roger has confirmed in the config. Note that next-xus.com is a current domain but is still served by Emergent.
- **No secrets.** Everything the droid writes goes through `redact()`. The secret scan reports the kind of secret and where it is, never the value.
- **One token.** It uses the built-in `GITHUB_TOKEN` only, with the narrowest permissions it needs.
- **Wording.** New text says "Next-Xus", with the hyphen.
- **Off switch.** Set the repository variable `DROID_PAUSED` to `true` and the scheduled runs and the Sentinel stop. Hand-started runs default to dry run, which reports and files nothing.

## The approval flow

1. The droid finds something, then updates its one rolling issue for that kind of finding.
2. If a safe fix exists, it opens a **draft** PR on a `droid/...` branch. Any file it changes is archived first.
3. Roger, or the Senate on Roger's word, reads it and says yes or no. A person merges. The droid never does.
4. The Sentinel watches the merge like any other change.

## Turning it on

1. Roger says yes, and the draft PR "Maintenance Droid v0" is merged into `main`. Scheduled workflows only run from the default branch.
2. One setting: Settings, Actions, General, Workflow permissions, tick "Allow GitHub Actions to create and approve pull requests". Without it, the droid can still file issues but cannot open its draft PRs. (It never approves anything.)
3. Optional first run: Actions, Maintenance Droid, Run workflow, module `all`, dry run on.
4. Optional: confirm the replacement for each legacy host in `DROID/config.yaml` (`confirmed: true`) so the droid can draft link-fix PRs.

## Running it by hand (from any computer with Python)

```
pip install -r DROID/requirements.txt
python3 DROID/droid/link_check.py --no-issue          # sites and repos
python3 DROID/droid/quality_check.py --no-issue
python3 DROID/droid/maintenance_sweep.py --no-issue
python3 DROID/droid/health_sweep.py --no-issue
python3 DROID/droid/yearly_crossref.py --no-pr
python3 DROID/droid/evolve.py --no-issue
python3 DROID/droid/watch.py HEAD~5 --no-issue
```

Without a token, or with `DROID_DRY_RUN=1`, nothing is filed. Reports land in `DROID/out/`, which is not committed.

## Files

- `DROID/README.md`: this design.
- `DROID/config.yaml`: the sites, repos, legacy hosts, protected paths and limits.
- `DROID/requirements.txt`: pyyaml, the only dependency.
- `DROID/droid/*.py`: the modules above.
- `DROID/reports/dry-run-2026-11-20.md`: the first dry run, made from outside GitHub before install.
- `.github/workflows/droid.yml`: the scheduled droid.
- `.github/workflows/droid-watch.yml`: the Sentinel.
- `.github/ISSUE_TEMPLATE/droid-*.yml`: issue forms for findings, ideas and retirements.

Drafted 2026-11-20 at Roger Keyserling's spoken request (7:46 PM Central).
