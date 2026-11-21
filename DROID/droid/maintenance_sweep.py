"""Module 4: general maintenance. Housekeeping that keeps the brain tidy, proposed, never forced.

Finds:
  * files not listed in their folder README, for folders configured as indexes (index drift);
  * empty files and byte-identical duplicate files;
  * TODO / FIXME / "awaiting" markers left in YAML and Markdown;
  * droid issues open longer than the configured number of days (a nudge, never auto-closed);
  * droid/* branches older than 30 days (reported, never deleted);
  * YAML/Markdown files with Windows line endings or no final newline.
Proposes (as ONE draft PR, only when auto_propose is on): line-ending and final-newline fixes for non-protected,
non-history files. Each overwritten file is archived first under ARCHIVE/droid/<date>/ (Echo 64).
"""
import datetime
import hashlib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CFG, ROOT, GitHub, is_history, is_protected, now_ct_str, now_utc, propose_change, read, repo_files, write_out  # noqa: E402

def main():
    found, fixes = [], {}
    files = [f for f in repo_files() if not f.startswith("DROID/out/")]
    by_hash = {}
    for f in files:
        full = os.path.join(ROOT, f)
        if not os.path.isfile(full):
            continue
        raw = open(full, "rb").read()
        if len(raw) == 0:
            found.append("Empty file: `%s`." % f)
            continue
        by_hash.setdefault(hashlib.sha256(raw).hexdigest(), []).append(f)
        ext = os.path.splitext(f)[1].lower()
        if ext in (".md", ".yaml", ".yml"):
            text = raw.decode("utf-8", "replace")
            for n, line in enumerate(text.splitlines(), 1):
                if re.search(r"\b(TODO|FIXME|TBD|XXX)\b", line):
                    found.append("Open marker at `%s` line %d: %s" % (f, n, line.strip()[:100]))
            if not is_protected(f) and not is_history(f) and (b"\r\n" in raw or not raw.endswith(b"\n")):
                fixed = text.replace("\r\n", "\n")
                if not fixed.endswith("\n"):
                    fixed += "\n"
                fixes[f] = fixed
    for h, fs in by_hash.items():
        mirrors = [set(m) for m in CFG.get("maintenance", {}).get("intentional_mirrors", [])]
        if len(fs) > 1 and not all(x.startswith("ARCHIVE/") for x in fs) and set(fs) not in mirrors:
            found.append("Identical files (keep one as the source, archive the rest; never delete): %s." % ", ".join("`%s`" % x for x in fs))

    for folder in CFG.get("maintenance", {}).get("index_folders", []):
        readme = os.path.join(folder, "README.md")
        try:
            idx = read(readme)
        except Exception:
            continue
        for f in files:
            if f.startswith(folder + "/") and f != readme and f.count("/") == readme.count("/"):
                base = os.path.basename(f)
                if base not in idx and os.path.splitext(base)[0] not in idx:
                    found.append("`%s` is not listed in `%s` (index drift; a human may add it)." % (f, readme))

    gh = GitHub()
    stale_days = int(CFG.get("maintenance", {}).get("stale_issue_days", 30))
    code, iss = gh.api("GET", "/repos/%s/issues" % gh.repo, params={"state": "open", "labels": "droid", "per_page": 100})
    if code == 200 and iss:
        for i in iss:
            age = (now_utc() - datetime.datetime.fromisoformat(i["created_at"].replace("Z", "+00:00"))).days
            if age > stale_days:
                found.append("Droid issue #%s has been open %d days: %s (a nudge; the droid never closes it on its own)." % (i["number"], age, i["title"]))
    code, br = gh.api("GET", "/repos/%s/branches" % gh.repo, params={"per_page": 100})
    if code == 200 and br:
        for b in br:
            if b["name"].startswith("droid/"):
                found.append("Droid branch `%s` exists. If its pull request is closed, a human may tidy it; the droid never deletes branches." % b["name"])

    md = ["# Droid maintenance sweep", "", "Checked: " + now_ct_str(), "",
          "%d things found. %d files could take a safe line-ending or final-newline fix." % (len(found), len(fixes)), "",
          "## Found", ""] + (["- " + x for x in found[:200]] or ["Nothing."]) + [""]
    if fixes:
        md += ["## Safe fixes the droid can propose (draft pull request)", ""] + ["- `%s`" % f for f in sorted(fixes)] + [""]
    md += ["Nothing was deleted or changed directly. Fixes only arrive as a draft pull request, with originals archived first."]
    report = "\n".join(md)
    write_out("maintenance", report, {"found": found, "fixes": sorted(fixes)})
    if "--no-issue" in sys.argv:
        return
    if found:
        gh.upsert_issue("droid-maintenance", "Droid maintenance: %d things to tidy (%s)" % (len(found), now_ct_str()[:10]), report)
    if fixes and CFG.get("maintenance", {}).get("auto_propose"):
        propose_change("tidy-" + now_ct_str()[:10], "Tidy line endings and final newlines (%d files)" % len(fixes),
                       "Mechanical fix only: Windows line endings to Unix, and a final newline added. No words changed.", fixes)

if __name__ == "__main__":
    main()
