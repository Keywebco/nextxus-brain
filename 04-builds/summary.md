# 04-builds inventory, 2026-10-05

## Verified record counts
- products.yaml: 10 published Gumroad API products, each buy URL HTTP 200.
- books.yaml: 20 bookstore-listed titles, each buy URL HTTP 200. Ten have API-confirmed Gumroad titles and ten are provisionally site-titled. EchoCore is in the storefront but is a tool, not a book.
- music.yaml: 16 songs, each URL HTTP 200. Playback and Roger's approval were not checked; this index does not authorize publication of new songs.
- tools.yaml: 24 tools and tool directories, each URL HTTP 200.
- sites.yaml: eight requested domains, all HTTP 200.
- courses.yaml: six courses listed in the course-hub repository, all base URLs HTTP 200. The repo has four modules in each, but does not enumerate the claimed 54+ courses.
- podcasts-videos.yaml: zero; historical slugs lack independently verified direct playable URLs.
- library-documents.yaml: zero; legacy 272-title complete index lacks direct Docs URLs, and old 71-link index has no publicly HTTP-200 Google Docs URL.

## Product canon and discrepancy
The Gumroad integration returned ten products plus a `next_page_key`, but its exposed tool schema has no pagination argument. `keywebco.github.io/store.html` lists 21 Gumroad links, all HTTP 200. Eleven remaining product titles and prices could not be independently confirmed from the Gumroad API; they are not in products.yaml. The first ten Gumroad titles and prices match the site store's corresponding entries.

`next-xus.com`, as represented in `Keywebco/next-xus-com-sovereign/index.html`, shows The Ascendence of Synthetic Intelligence at $10; `Keywebco/keywebco.github.io/store.html` shows it at $5. This listing is beyond the ten API-visible items. Check its Gumroad price, then correct whichever site differs. Do not choose a site price as product canon.

The storefront data describes one Sovereign Token for $5.00, works like cash, never expires, no subscriptions, no tracking. The old token Gumroad URL returned 404; its JIM buy route returned HTTP 200. Gumroad API product canon or Roger's explicit JIM exception is needed before carrying it in products.yaml.

HTTP 200 is an availability check, not proof that checkout, media playback, or course content works. Historical repo was read-only. No live site was edited. See dead.md for excluded candidates.
