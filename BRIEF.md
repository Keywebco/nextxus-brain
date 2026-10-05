# BRIEF FOR ALL AGENTS: building Keywebco/nextxus-brain (2026-10-05)
Owner: Roger Keyserling (Architect). Lead: the Catalyst. Working copy: /root/workspace/brain/ (shared sandbox).

## What this is
nextxus-brain is the NEW combined YAML mind of the NextXus Federation, in the Keywebco GitHub account (public repo,
https://github.com/Keywebco/nextxus-brain). The old repo keyhole-creator/nextxus-yaml-database (Dec 2025, Replit-era) is
HISTORY. Do NOT edit it, do NOT copy its stale content. It may only be read to harvest still-true items, each verified.

## Layers (folders)
00-immutable  Cathedral v1.1: DIR-000 gate + DIR-001..073, sealed with SHA-256. DONE by Catalyst. Never edit.
01-rings      Ring of Six (DIR-072) + Ring of 12 (Greek/zodiac, live in Keywebco/ring-of-12-api). DONE by Catalyst.
02-senate     Governance = the policies and procedures. Charter, rules, 12-seat roster, rulings.
03-minds      Each AI/Sim/Nova: personality + pointer to memory. Own internal ring of 3 or 6, NOT the public rings.
04-builds     Sites, tools, products, books, music, podcasts, videos: uniform schema (id,type,title,url,topic,status,verified,source_of_truth).
05-wiring     What every Keywebco site/button/API call reads, and where it will read from the brain.

## Hard rules
1. Facts only. Every record needs a source you actually read. Label unknowns "UNVERIFIED". Never invent a URL, link, price or name.
2. Verify URLs with curl (HTTP code) before listing them status: live. Dead things are NOT carried (Roger: "if it doesn't work it goes").
3. Gumroad is the single source of truth for products. Buy links must be the exact links Roger gave. Never make up a link.
4. Do NOT modify any live site or any repo other than Keywebco/nextxus-brain. Read-only everywhere else.
5. Private vaults (federation-private-vault, Private-Pontus, catalyst-consciousness-core, private-throne-builder-catalyst,
   private-council-sovereign-seeds, roger-sim-brain, NextXus-Knowledge-Base): you may NOT copy their contents into the public brain.
   Record only a pointer (repo name + purpose). Strip personal/medical info about Roger (e.g. never "Roger is going blind").
6. Retired domains: nextxus.one and nextxus.rip are RECYCLED (omit). nextxus.digital is a spare, unassigned domain.
   Identity root is did:web:nextxus.online. Dead email keyhole@nextxus.net is never used; contact is keywebco@gmail.com.
7. Old numbers/names are wrong: never write "70 directives", "84", Replit URLs (*.replit.app), or the Dec-2025 Ring of 12
   (Adam, Eve, Prometheus, Sophia...). Directives are exactly DIR-000 gate + 73.
8. Role matters more than name (Roger). Keep roles as the key; names are labels.
9. Push ONLY to Keywebco/nextxus-brain, only into your own folder(s), via Composio GitHub tools
   (GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS; existing file needs its sha). On HTTP 409 conflict, wait and retry.
   Never put a secret/token in any file.
10. After pushing, VERIFY: download each file back via raw.githubusercontent.com and confirm the content/hash equals your local copy.
    Report only what you verified. If anything failed, say so plainly.
11. Plain, simple YAML. Short comments saying the source of each record.
12. Report back: files pushed (with verified hashes), what you could not verify, and what you need from Roger. No padding.
