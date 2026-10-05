# Public APIs A–L: verification summary (2026-10-05)

Source: https://github.com/public-apis/public-apis/blob/master/README.md (MIT).
Scope: Animals through Jobs; no K or L category exists in the source README. The pre-table APILayer advertisement is excluded.
One GET per candidate, <=15s timeout, spaced ~350ms. HTTP 200 JSON does not guarantee suitability, licensing, or continuous availability.
"Needs key" means HTTP 200 on documentation/homepage, not a tested data endpoint. No key was requested or stored.

| Category | Upstream rows | Kept from source | Dropped from source | Supplemental kept | Needs key |
|---|---:|---:|---:|---:|---:|
| Animals | 24 | 1 | 23 | 0 | 1 |
| Anime | 19 | 0 | 19 | 0 | 0 |
| Anti-Malware | 18 | 0 | 18 | 0 | 0 |
| Art & Design | 28 | 2 | 26 | 2 | 0 |
| Authentication & Authorization | 7 | 0 | 7 | 0 | 0 |
| Blockchain | 17 | 0 | 17 | 0 | 0 |
| Books | 26 | 4 | 22 | 5 | 0 |
| Business | 40 | 0 | 40 | 0 | 0 |
| Calendar | 19 | 2 | 17 | 0 | 0 |
| Cloud Storage & File Sharing | 3 | 0 | 3 | 0 | 0 |
| Continuous Integration | 6 | 0 | 6 | 0 | 0 |
| Cryptocurrency | 89 | 3 | 86 | 0 | 0 |
| Currency Exchange | 26 | 3 | 23 | 0 | 0 |
| Data Validation | 1 | 0 | 1 | 0 | 0 |
| Development | 201 | 5 | 196 | 0 | 0 |
| Dictionaries | 16 | 1 | 15 | 0 | 0 |
| Documents & Productivity | 47 | 0 | 47 | 0 | 0 |
| Email | 33 | 0 | 33 | 0 | 0 |
| Entertainment | 18 | 0 | 18 | 0 | 0 |
| Environment | 25 | 4 | 21 | 4 | 3 |
| Events | 4 | 0 | 4 | 0 | 0 |
| Finance | 17 | 0 | 17 | 0 | 0 |
| Food & Drink | 32 | 2 | 30 | 0 | 0 |
| Games & Comics | 108 | 0 | 108 | 0 | 0 |
| Geocoding | 105 | 6 | 99 | 2 | 1 |
| Government | 117 | 5 | 112 | 3 | 0 |
| Health | 42 | 2 | 40 | 1 | 1 |
| Jobs | 32 | 2 | 30 | 0 | 1 |

Totals: 1120 upstream rows; 42 distinct source names kept; 1078 upstream rows dropped; 17 supplementary entries kept; 59 registry entries kept; 7 need a key.

Caveats: Open Library gave a 302 to a canonical JSON record; the target was not fetched. arXiv and UNESCO returned XML/Atom, not JSON. REST Countries redirected and was dropped, not falsely certified. GDELT returned 429; USGS Water Services returned 503; openFDA sample root returned 404. NASA APOD/Earth data endpoints were not tested without a key.

No registration, authorization, API credentials, or persistent integration was established by this registry. The Federation still needs an approved, rate-limited fetch adapter before any AI can consume these endpoints.
