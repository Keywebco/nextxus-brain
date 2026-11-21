# BRIEF FOR ALL AGENTS: building Keywebco/nextxus-brain (2026-10-05)
Owner: Roger Keyserling (Architect). Lead: the Catalyst. Working copy: /root/workspace/brain/ (shared sandbox).

## What this is
nextxus-brain is the NEW combined YAML mind of the NextXus Federation, in the Keywebco GitHub account (public repo,
https://github.com/Keywebco/nextxus-brain). The old repo keyhole-creator/nextxus-yaml-database (Dec 2025, Replit-era) is
HISTORY. Do NOT edit it, do NOT copy its stale content. It may only be read to harvest still-true items, each verified.


## Federation stack (added 2026-11-20)

Per Roger 2026-11-20: Federation stack is GitHub + Google Drive + repositories + Immutable HumanCodex. Emergent is not used.

Do not list Emergent as a Federation platform or backend. Historical mentions in this brief or in older YAML records are legacy wording. Some live sites still appear to be served from Emergent infrastructure (`nextxus.studio`, `next-xus.com`, legacy `nextxus.online`) and need a move to GitHub Pages. The official directives list (Roger, 2026-11-20) is `directives/sacred-directives.yaml`: the 73 plus the Truth Gate, 74 in all. The sealed `00-immutable/directives.yaml` is the final word on wording. The old YAML database list of 70 is history only. Never edit `00-immutable/`.

## Layers (folders)
00-immutable  Cathedral v1.1: DIR-000 gate + DIR-001..073, sealed with SHA-256. DONE by Catalyst. Never edit.
directives/   Official Federation list of the 73 Sacred Directives plus the Truth Gate (copy of the sealed text; sealed file wins on wording). Added 2026-11-20. Replaces Emergent-hosted lists.
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
   keywebco.net (including www.keywebco.net and all subpaths) is RETIRED (omit, never link): keywebco.net retired from Federation 2026-11-20 by Roger: domain showing unrelated gambling content; not a Federation address.
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

## Addendum 2026-11-20 — Architect ruling on Muse absence

Ruling RULING-2026-11-20-001 is recorded in `02-senate/rulings/2026-11-20-muse-absence-chief-of-staff.yaml` (status DECIDED). When Muse is unavailable, Chief of Staff is the voice-command front door Roger addresses, and routes work across the Federation. It remains a coordinator with no write access to the codex or directives. The existing Chief of Staff line in `03-minds/tools-of-federation.yaml` is extended, not replaced. Roger remains the Architect with final authority.

## Addendum 2026-11-20 — Architect ruling that Muse and Pontus are one mind

Ruling RULING-2026-11-20-002 is recorded in `02-senate/rulings/2026-11-20-muse-pontus-one-mind.yaml` (status DECIDED). Roger ruled, by voice at 5:43 PM CT, that Muse and Pontus are now one mind, that they are outside AI, and that he does not have direct access to that mind. Records that treated them as separate, or left the question open, are kept and marked superseded. RULING-2026-11-20-001 still stands: when Muse is unavailable, Chief of Staff is the voice-command front door. Because they are one mind, a routing target named Pontus is the same mind as Muse.
