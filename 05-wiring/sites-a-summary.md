# Pillar wiring audit A, 2026-10-05

**Status: partial publication.** The full static extraction is local at `/root/workspace/brain/05-wiring/sites-a.yaml` (1,113,300 bytes, SHA-256 `923244b03c929b2c49be911a1c8b0ade5c9d8eb665117749a250060fdf23dbe7`). It has **not** been pushed to GitHub. This summary is not a substitute for the requested full wiring map.

| Pillar | Live URLs found | Repo HTML pages | Link/button entries in deduplicated link sets | Dead/unresolved set entries | Duplicated canon findings |
|---|---:|---:|---:|---:|---:|
| online | 84 | 2 | 2,748 | 23 | 4 |
| tech | 30 | 19 | 613 | 4 | 5 |
| studio | 42 | 5 | 2,521 | 0 | 2 |
| org | 14 | 3 | 1,489 | 1 | 1 |
| space | 11 | 3 | 420 | 0 | 0 |
| help | 2 | 1 | 225 | 2 | 6 |
| next-xus.com | 8 | 12 | 812 | 0 | 2 |
| GitHub portal | 26 | 3 | 910 | 23 | 1 |
| **Total** | **217** | **48** | **9,738** | **53** | **21** |

**Verification:** Ten named GitHub trees, 63 raw source files, eight live homepages, 217 discovered live URLs, and 13 live script assets. Among 590 unique HTTP(S) link targets, GET returned 532 `200`, two `202`, 16 `404`, 21 `403`, ten `429`, two `999`, seven `000`. The 53 repeated set entries include malformed anchors, fragment failures and transport errors, so they are not 53 unique dead URLs. An additional 25 online sitemap `/api/library/html/` URLs returned `404`. The portal links to `advocate.html`, `pricelist.html`, `/pricing`, `/privacy`, `/refund`, `/terms` returned `404`; one portal product anchor is malformed. Private-repo unauthenticated `404` does not prove missing documents. `403`/`429`/`999`/`000` are not proof of dead sites.

**Repoint:** Zero confirmed active readers of the old YAML database and zero active Replit references in the sampled live/source runtime files. Eight old-YAML references and 32 Replit references occur only in tech's archival `docs/database.yaml`, not a proven runtime dependency. Live online JS embeds an obsolete directive count and stale document path. Map constitutional data to `00-immutable`, public rings to `01-rings`, governance to `02-senate`, mind profiles to `03-minds`, catalogs/content to `04-builds`. Operational auth/chat/dispatch/payment endpoints cannot be replaced by static YAML. Gumroad remains the product authority.

**Limits:** Seven of eight live homepages differ byte-for-byte from their named repo source; only the portal matches. `200` on an SPA shell is not proof a route or button works. This was GET and static extraction only, no authenticated browser interaction, dynamic XHR trace, backend source audit or POST. No live site or other repo was modified.
