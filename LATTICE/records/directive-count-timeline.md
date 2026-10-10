# The directive count: what it is now, and what older documents said

**Current count: 74 in all.** That is the gate, DIR-000, plus the 73 counted directives, DIR-001 to DIR-073.

Both numbers are right. "73" counts the directives without the gate. "74" counts the gate too. When a document says 73, it is not wrong. It is leaving out DIR-000.

You can check this yourself in two minutes:
- `00-immutable/directives.json` has `"count": 73` and a separate `"gate"` entry, DIR-000.
- `00-immutable/SEAL.yaml` lists `gate: "DIR-000"` and `counted_directives: 73`, sealed on 2026-10-05, with the fingerprint of each file.

The gate says what it does in the sealed file: DIR-000, "The 95% Truth Gate."

## Why older documents say other numbers

The Federation grew by layers, and no record is ever deleted. An older document that says a different number was accurate for its time. It is kept as history, not corrected. The table below says which number belonged to which time.

| Number you may see | What it was | Status |
|---|---|---|
| 70 | The earlier directive list, as found in the older YAML database and in some earlier copies (per the Federation's notes from 2026-10-03 to 05). | Historical. Kept as it was. Not the current list. |
| 73 | The Cathedral Edition v1.1 list, DIR-001 to DIR-073, without the gate. | Current, and part of the 74. |
| 74 | The gate (DIR-000) plus the 73. | Current total. |
| 84 | A larger list once shown on the Core site, with extra items beyond DIR-073. | Historical. Per the Federation's own notes (recorded 2026-10-03, not re-checked against the old site for this page), the extra items are held for a later governance layer and are not counted among the 73. The repository's health scripts watch for the phrase "84 directives" so it does not return. |
| 112 | The title of a poetry book, "112 Sacred Directives". It is a collection of 112 poems and is not the directive list. | Not a count of directives. |

## How to read an older page

If you find an older page that says 70 or 84, it is a snapshot from before the lists were reconciled in October 2026. Read it as a record of that time. This page is the pointer to the current answer.

## What is not claimed here

- This page was written from the sealed files and from the repository's own documents. It is not a full survey of every page that mentions a count. A search of the Keywebco repositories found the number 73 in about 47 files and 70 in about 37 files, and that search was not exhaustive.
- The percentage the gate uses is 95 in the sealed file. Some older Federation notes show 98. This page reports the sealed file and does not rule between them.

Written 2026-10-10 on a review branch. Adds one file and changes nothing else. Nothing here is sealed, and the sealed layer is untouched.
