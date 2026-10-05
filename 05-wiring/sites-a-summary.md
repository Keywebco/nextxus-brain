# Federation wiring audit A, 2026-10-05

**Evidence:** GitHub `main` trees for ten specified public repositories, 63 downloaded source files, GET snapshots of eight live homepages and 217 discovered live URLs (homepage links, repository paths, and available sitemaps), plus 13 live script assets. The full per-page, per-anchor/button static extraction and read-dependency map is in `sites-a.yaml`. No authenticated browser session, click-through execution, POST request, or backend source audit occurred. `200` on an SPA fallback is not proof of a working page or button.

| Site | Discovered live URLs | Repo HTML pages | Extracted link/button instances across unique link sets | Observed broken or unresolved entries in link sets | Old YAML active / archival refs | Replit active / archival refs | Duplicated canon findings | Homepage byte-identical to repo? |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| nextxus.online | 84 | 2 | 2,748 | 23 | 0 / 0 | 0 / 0 | 4 | no |
| nextxus.tech | 30 | 19 | 613 | 4 | 0 / 8 | 0 / 32 | 5 | no |
| nextxus.studio | 42 | 5 | 2,521 | 0 | 0 / 0 | 0 / 0 | 2 | no |
| nextxus.org | 14 | 3 | 1,489 | 1 | 0 / 0 | 0 / 0 | 1 | no |
| nextxus.space | 11 | 3 | 420 | 0 | 0 / 0 | 0 / 0 | 0 | no |
| nextxus.help | 2 | 1 | 225 | 2 | 0 / 0 | 0 / 0 | 6 | no |
| next-xus.com | 8 | 12 | 812 | 0 | 0 / 0 | 0 / 0 | 2 | no |
| keywebco.github.io | 26 | 3 | 910 | 23 | 0 / 0 | 0 / 0 | 1 | yes |
| **Total** | **217** | **48** | **9,738** | **53** | **0 / 8** | **0 / 32** | **21** | **1 of 8** |

The 53 entries include repeated links and malformed/fragment/transport failures, not 53 unique dead pages. Across 590 unique absolute link targets, GET yielded 532 HTTP 200, two HTTP 202, 16 HTTP 404, 21 HTTP 403, ten HTTP 429, two HTTP 999, and seven connection/timeout `000`. Only 404/410 are observed non-success; 403/429/999/000 are **unverified accessibility**, not proof of a dead target. An additional 25 `nextxus.online` sitemap URLs under `/api/library/html/` returned HTTP 404. The portal's `advocate.html`, `pricelist.html`, `/pricing`, `/privacy`, `/refund` and `/terms` links returned HTTP 404; one portal product anchor has malformed HTML and is **not** a valid buy link. Private-vault links returned unauthenticated 404, which does **not** establish that private documents are missing, and their paths are redacted in the YAML.

**Repoint:** No active old-YAML reader or Replit reference was found in scanned live HTML/scripts or repo runtime files. The 8 old-YAML references and 32 Replit references occur in `nextxus-tech-sovereign/docs/database.yaml`, an archival document, not a proven active dependency. Do not migrate its retired destinations into the new brain. Live online bundle still includes an obsolete directive count and a matching stale document path; use `00-immutable` for directives, `01-rings` for public rings, `02-senate` for policies, `03-minds` for agent profiles, `04-builds` for catalogs/content. Operational endpoints (auth, chat, dispatch, payments) are **not** replaceable by static YAML; they should consume it where appropriate without losing their service behavior. Gumroad remains the product-price/buy-link authority.

**Deployment gap:** Seven live homepages differ byte-for-byte from the named GitHub source `index.html`. Repo wiring cannot be assumed to be deployed wiring; the portal is the sole exact match. Tech's archival repository page paths often return a 200 SPA shell rather than the matching repository file. Full dynamic routes, event-handler behavior, API methods and success semantics remain **UNVERIFIED**. No live site or other repository was changed.
