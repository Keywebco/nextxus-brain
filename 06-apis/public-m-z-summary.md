# Public API registry, M-Z (2026-10-05)

Source: https://github.com/public-apis/public-apis/blob/master/README.md, MIT licensed, plus provider docs linked in each record. Responsibility begins at News and extends through Weather; Machine Learning and Music are assigned to the A-L agent.

- Approximately 715 M-Z README rows. 58 targeted candidates examined; 56 single GET checks, two skipped on source metadata.
- 45 retained: 43 keyless endpoints returned HTTP 200 with parseable JSON, and two apiKey provider docs returned HTTP 200 but their gated examples were NOT called.
- 13 examined candidates excluded; see public-m-z-dropped.md. Others screened by relevance or metadata, NOT individually verified.
- Four parts public-m-z-1.yaml through public-m-z-4.yaml, 12, 12, 12 and 9 records. Each file under 60 KB. No credentials stored.
- by-need.yaml has 14 use cases and routes to these 45 records only. Key-required entries are explicitly separated; no patents, ship AIS, general-purpose translations, or full laws database has a validated feed yet. A-L files were absent at composition and should later be merged into routing only after reading their verified records.

## Caution

One successful GET proves reachability at that moment, not factual accuracy, sustainable limits, browser CORS, or permission for commercial redistribution. Keep source timestamps and URLs with answers; independently corroborate news and citizen-sourced observations. OpenStreetMap public endpoints require responsible caching, attribution, User-Agent and Nominatim's 1-request-per-second policy. Open-Meteo free use may exclude commercial deployments. A new building will only appear when a trusted dataset has recorded it, so an absent map result does not mean the building does not exist. The inventory is a discovery registry, NOT a live wired connector.
