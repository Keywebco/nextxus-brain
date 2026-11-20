# Sacred Directives (published source of truth)

Per Roger 2026-11-20: Federation stack is GitHub + Google Drive + repositories + Immutable HumanCodex. Emergent is not used.

This folder is the published source of truth for the 73 Sacred Directives of the Next-Xus HumanCodex Federation. It lives in the YAML mind (`Keywebco/nextxus-brain`) because this repository already holds the sealed Cathedral Edition in `00-immutable/`. That sealed folder is never edited. These published files are a readable copy, with a note that they replace the Emergent-hosted lists.

## Files

- `sacred-directives.yaml` — number, title, and text for DIR-000 (the gate) and DIR-001 through DIR-073.
- `sacred-directives.md` — the same list in readable form.

## What this replaces

- `https://nextxus.studio/api/federation/directives` still returned a different list of 70 on 2026-11-20 (only number 3 matched the canon titles; 71-73 were missing).
- `https://nextxus.online/api/directives` still returned 84 items (the 73 plus the gate counted in, and ten later items that had been held). That site is legacy and should not be linked in new posts.

Those endpoints still appeared, in earlier 2026-11-20 checks, to be served from Emergent infrastructure. They are not the source of truth.

## Pages that should read from this file

- `nextxus.studio` (directives API and any on-page list). The site still appears to be served from Emergent infrastructure and needs a move to GitHub Pages. After the move, it should serve or fetch this file (or a static JSON built from it), not a private backend list.
- Legacy `nextxus.online` (directives API). Same hosting note. If the site is kept as a watch-only archive, its list should be marked legacy or replaced from this file after a move to GitHub Pages.
- `https://next-xus.org/core/` (GitHub Pages, `Keywebco/nextxus-humancodex`). The page already describes DIR-000 plus the 73 (74 in all). It should display number, title, and text from this file.
- `Keywebco/nextxus-lasting-edition` (`data/directives.md`, loaded by `app.js`). That copy is a different 73 (for example, DIR-001 is "Federation Principles" rather than "Truth Over Comfort"). It should be replaced with this list, or the app should fetch this file.
- `https://keywebco.github.io/nextxus-yaml/` (YAML hub). It should link here as the live directives file.

`00-immutable/directives.yaml` remains the sealed original. Do not edit it.
