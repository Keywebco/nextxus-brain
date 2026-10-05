# M-Z screened out, 2026-10-05

Source index: https://github.com/public-apis/public-apis/blob/master/README.md (MIT). From roughly 715 M-Z rows, 58 curated candidates were examined. Exactly one GET was made for each of 56 testable candidates, with a 15-second timeout and spacing. Two were excluded from source metadata without a request. An unsuccessful response was not retried. This is NOT an individual audit of all 715 rows.

## Failed one-time check, not admitted

- Solar System OpenData: HTTP 401.
- Open-Meteo Ensemble: HTTP 400 for tested example.
- US Weather (NWS): HTTP 400 for tested alerts query. This does not establish that the API itself is dead.
- GDELT: HTTP 429. No assertion that GDELT is dead; retry only in a later audit under provider policy.
- SpaceX API: HTTP 525.
- data.gov CKAN: HTTP 404 for tested catalog endpoint. Catalog may have moved.
- US Census API: HTTP 200 but body not parseable JSON under the test.
- USGS GeoNames GNIS: HTTP 200 HTML documentation, not a JSON API response.

## Excluded by source metadata

- Wikidata: README lists OAuth; the attempted keyless path was skipped. The source metadata might be overbroad.
- Open Notify: README lists HTTP-only; HTTPS test skipped.

## Reachable docs, excluded from free production routing

- NewsAPI and GNews: free plans appear restricted to development or testing, not dependable no-cost production feeds.
- Guardian Open Platform: docs reachable; free signup and production terms not confirmed in this audit.

## Other policy exclusions, not individually tested

Machine Learning and Music are assigned to the other agent. M-Z entries marked OAuth, HTTP-only, or requiring unsupported authentication were screened out, along with trivia, fake data, quote generators, URL shorteners, scraping and credential utilities, narrow commercial listings, and paywalled feeds. PatentsView legacy API retired and current service needs a key while new grants are suspended: https://patentsview.org/apis/api-faqs. Unchecked listings must never be represented as live.
