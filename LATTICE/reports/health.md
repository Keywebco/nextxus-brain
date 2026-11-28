# Federation health report

Checked: 2026-11-28 17:00 UTC

40 of 42 checks passed.

## Problems

- **Music** (https://keywebco.github.io/nextxus-music/): missing: nx-commons-bar
- **Legacy hosted site: nextxus.tech** (https://nextxus.tech/): HTTP no answer (expected 200)

## All checks

| Check | Kind | Result | Seconds |
|---|---|---|---|
| Commons front door | site | OK | 0.3 |
| Living Library | site | OK | 0.3 |
| Library data (volume 1) | site | OK | 0.2 |
| Core page | site | OK | 0.1 |
| Command page | site | OK | 0.1 |
| Portal | site | OK | 0.2 |
| Agent Zero | site | OK | 0.2 |
| Research hub | site | OK | 0.2 |
| Recycler | site | OK | 0.2 |
| Archives | site | OK | 0.2 |
| Senate | site | OK | 0.1 |
| Chat | site | OK | 0.2 |
| Tools | site | OK | 0.2 |
| Blog | site | OK | 0.2 |
| Process | site | OK | 0.1 |
| YAML | site | OK | 0.2 |
| Music | site | PROBLEM | 0.1 |
| Build website | site | OK | 0.2 |
| Build Sim | site | OK | 0.2 |
| Build Nova | site | OK | 0.1 |
| Course hub | site | OK | 0.2 |
| Roger Keyserling | site | OK | 0.1 |
| Sovereign tools | site | OK | 0.2 |
| God's Eye | site | OK | 0.1 |
| Shared Mind (Sim) | site | OK | 0.1 |
| Ask and council server | server | OK | 0.1 |
| Command page server (the lock must answer 401 with no key) | server | OK | 0.1 |
| Sim server | server | OK | 11.2 |
| Roger Sim server | server | OK | 0.2 |
| Relay server | server | OK | 0.2 |
| Gatekeeper | server | OK | 0.2 |
| Gumroad: Support the Living Library | money | OK | 0.2 |
| Gumroad: Scholar's Ledger | money | OK | 0.2 |
| Gumroad: Ascendence | money | OK | 0.1 |
| Gumroad: Gravity of Us | money | OK | 0.1 |
| Gumroad: Sovereign Token | money | OK | 0.1 |
| Legacy hosted site: nextxus.org | watch only | OK | 0.9 |
| Legacy hosted site: nextxus.tech | watch only | PROBLEM | 0.1 |
| Legacy hosted site: nextxus.space | watch only | OK | 0.5 |
| Legacy hosted site: nextxus.studio | watch only | OK | 0.8 |
| Legacy hosted site: nextxus.help | watch only | OK | 0.5 |
| Legacy hosted site: next-xus.com | watch only | OK | 0.7 |

**What the kinds mean:** *site* is a web page that must answer and hold the words it should; *server* is a program that must answer (the command page's lock must answer 401 with no key); *money* is a Gumroad listing that must still be live; *watch only* is a site we monitor but never edit.

A free server that was asleep is retried before it counts as a problem. A page that answers 200 is also checked for a phrase it must contain and for known damage.
The legacy hosted sites (including nextxus.studio and next-xus.com) are watched only. nextxus.online was retired on 2026-11-20 and is no longer watched. They still appear to be served from Emergent infrastructure, are not part of the Federation stack, and need a move to GitHub Pages. They are never edited from this check.

**The receipt:** [what this costs, measured and estimated, dated](cost.md). **The seal check:** [the daily check of the sealed rules](latest.md). **The front door:** https://keywebco.github.io/nextxus-humancodex/
