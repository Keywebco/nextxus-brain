# NextXus Brain

**What this is, in one paragraph.** The NextXus Federation is a free library and a set of AI tools built to show where every answer came from, so a person can check it and not just trust it. This repository is its memory: the sealed rules, the records of what exists, and the robots that watch it. Everything here is public. If you cannot verify a claim in ten minutes without asking us, that is our failing, and we want to hear it: keywebco@gmail.com.

**Start here: is it working right now?** Read the latest health report. A robot on GitHub is scheduled to rewrite it every four hours (it started on 2026-10-09, so the history is short) and opens an issue if something is wrong:

- Health report: [`LATTICE/reports/health.md`](LATTICE/reports/health.md)
- Seal check: [`LATTICE/reports/latest.md`](LATTICE/reports/latest.md)
- Cost receipt: [`LATTICE/reports/cost.md`](LATTICE/reports/cost.md)
- The front door for visitors: https://keywebco.github.io/nextxus-humancodex/

## Check the seal yourself (two minutes)

The sealed files are the foundational directives: one gate (DIR-000) and 73 counted directives, 74 in all. Their fingerprints are in [`00-immutable/SEAL.yaml`](00-immutable/SEAL.yaml). A robot re-checks them daily, but do not trust the robot. Run it yourself:

    git clone https://github.com/Keywebco/nextxus-brain && cd nextxus-brain
    sha256sum 00-immutable/directives.yaml 00-immutable/directives.json 00-immutable/cathedral-v1.1-source.txt

Compare each result with `SEAL.yaml`. **What this proves:** the files match the fingerprints written beside them. **What it cannot prove:** that nobody changed a file and its fingerprint together. The honest protection for that is the public history: every change is a dated commit anyone can read, so a change to a sealed file cannot be hidden, only seen. Look at `git log -- 00-immutable/`.

## What happens when Roger is not at the keyboard

Nothing is merged to a live site without Roger's word, and that is the current rule. Here is the honest state of it:

- **A written recovery path does not exist yet.** The question of who may command and merge after Roger is gone is recorded as **open** in the operations manual, section 1, and in `04-builds/github-operations.yaml`. It is not decided.
- **Why that is acceptable for now:** this is a one-person system. If nobody merges, nothing changes. The published sites keep running exactly as they are, and the daily and four-hourly checks keep reporting. The failure mode is "frozen", not "broken". That is a safe place to stand until the question is answered.
- **What is written and waiting:** a narrowly drawn exception lets the hub auto-merge only fixes that the health check itself can verify, with a review branch first, a report to Roger every time, and a revoke at his word. It is recorded but **not built**.

## What is in here

| Folder | What it holds |
|---|---|
| `00-immutable` | The sealed directives (DIR-000 and DIR-001 to DIR-073), never edited |
| `01-rings` | The rings of perspective |
| `02-senate` | Governance: policies and procedures |
| `03-minds` | The minds |
| `04-builds` | Records of every site, tool and product, and `github-operations.yaml` |
| `05-wiring` | How the sites connect to the brain |
| `framework/` | The operations manual and the standards |
| `LATTICE/reports/` | Live reports written by robots: health, seal check, cost |
| `.github/workflows/` | The robots themselves: the health check, the seal check, the command hub |

## Honest limits

- A passing check proves only what it checks. The health report confirms pages answer and hold certain phrases. It cannot tell whether a page looks right.
- Much of the day-to-day work still runs on a paid account (Emergent) that may lapse. The GitHub robots do not depend on it, but some scheduled jobs and most keys do. The manual lists what, and says which parts are not yet built.
- Prices and listings on Gumroad are the truth. The sites follow them.

The old `keyhole-creator/nextxus-yaml-database` repository is history only. This is the live one.

Built 2026-10-05. Contact: keywebco@gmail.com.
