"""Module 5: the yearly cross-reference. Once a year (and by hand any time).

For every YAML/Markdown item in the scanned folders it gathers:
  * when the file last changed (git history; the workflow checks out full history);
  * every URL inside, and whether it still answers;
  * every github.com/<owner>/<repo> it names, and that repo's current state (exists, archived, last push,
    latest release, description) from the GitHub API;
  * a few current GitHub repositories on the same subject (free GitHub search API) as "new information".
Then it sorts items into:
  * RETIRE candidates: unchanged for over stale_days AND leaning on dead links or archived/missing repos;
  * REVIEW candidates: unchanged for over stale_days but still sound;
  * CURRENT.
Directives are never retired by the droid. It re-checks that the official copy matches the sealed Cathedral
wording, and any directive upgrade can only be drafted as a Senate proposal.

Output is ONE draft pull request that ADDS files only:
  DROID/yearly/<year>/crossref.md                 the full report;
  DROID/yearly/<year>/upgrades/<item>.md          a draft upgrade per candidate: the old text kept whole,
                                                  side by side with the new information, and a suggested merge;
  ARCHIVE/retired/<year>/<original path>          a copy of each retire candidate (Echo 64: archive first).
Originals are not changed or removed. Roger or the Senate decides; a human then marks items retired.
"""
import datetime
import os
import re
import subprocess
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CFG, ROOT, GitHub, is_history, http, legacy_host_of, now_ct_str, now_utc, propose_change, read, repo_files, write_out  # noqa: E402
from quality_check import directive_alignment  # noqa: E402

URL_RE = re.compile(r"https?://[^\s\"'<>()\[\]{}`|\\^]+")
GH_RE = re.compile(r"github\.com/([A-Za-z0-9_.\-]+)/([A-Za-z0-9_.\-]+)")

def last_changed(path):
    r = subprocess.run(["git", "log", "-1", "--format=%cI", "--", path], cwd=ROOT, capture_output=True, text=True)
    s = r.stdout.strip()
    return datetime.datetime.fromisoformat(s) if s else None

def topic_of(path, text):
    m = re.search(r"^(?:title|name):\s*['\"]?(.+?)['\"]?\s*$", text, re.M)
    if m:
        return m.group(1)[:60]
    m = re.search(r"^#\s+(.+)$", text, re.M)
    if m:
        return m.group(1)[:60]
    return os.path.splitext(os.path.basename(path))[0].replace("-", " ")

def main():
    Y = CFG.get("yearly", {})
    stale_days = int(Y.get("stale_days", 365))
    gh = GitHub()
    year = now_utc().strftime("%Y")
    items = [f for f in repo_files({".yaml", ".yml", ".md"}, include_protected=False)
             if any(f.startswith(d + "/") for d in Y.get("scan_folders", [])) and not is_history(f)]
    repo_cache = {}
    # Check every URL once, in parallel, before walking the items.
    import concurrent.futures as cf
    all_urls = set()
    for f in items:
        all_urls |= {u.rstrip(".,;:)'\"") for u in URL_RE.findall(read(f))[:40]}
    all_urls = sorted(u for u in all_urls if not legacy_host_of(u))
    def probe(u):
        return u, http(u, method="GET", timeout=15, max_bytes=2048)[0]
    with cf.ThreadPoolExecutor(max_workers=12) as ex:
        url_cache = dict(ex.map(probe, all_urls))
    rows, retire, review, upgrades = [], [], [], {}
    searched = 0
    for f in sorted(items):
        text = read(f)
        changed = last_changed(f)
        age = (now_utc() - changed).days if changed else 0
        urls = sorted({u.rstrip(".,;:)'\"") for u in URL_RE.findall(text)})
        dead, legacy = [], []
        for u in urls[:40]:
            if legacy_host_of(u):
                legacy.append(u); continue
            if u not in url_cache:
                url_cache[u] = http(u, method="GET", timeout=15, max_bytes=2048)[0]
            if url_cache[u] in (404, 410):
                dead.append(u)
        repos_state = []
        for o, r in sorted(set(GH_RE.findall(text)))[:15]:
            r = re.sub(r"\.git$", "", r)
            key = (o, r)
            if key not in repo_cache:
                code, d = gh.api("GET", "/repos/%s/%s" % (o, r))
                rel = None
                if code == 200:
                    c2, rr = gh.api("GET", "/repos/%s/%s/releases/latest" % (o, r))
                    rel = (rr or {}).get("tag_name") if c2 == 200 else None
                repo_cache[key] = {"code": code, "archived": (d or {}).get("archived"), "pushed": (d or {}).get("pushed_at"),
                                   "desc": (d or {}).get("description"), "release": rel}
            repos_state.append(("%s/%s" % key, repo_cache[key]))
        broken_repos = [n for n, s in repos_state if s["code"] == 404 or s.get("archived")]
        status = "current"
        if age > stale_days:
            status = "retire" if (dead or broken_repos) else "review"
        rows.append((f, age, len(urls), len(dead), len(legacy), len(broken_repos), status))
        if status == "current" and not legacy:
            continue
        new_info = []
        if searched < int(Y.get("max_items_searched", 25)) and status != "current":
            searched += 1
            q = topic_of(f, text)
            code, s = gh.api("GET", "/search/repositories", params={"q": q, "sort": "stars", "per_page": int(Y.get("github_search_per_item", 3))})
            for it in ((s or {}).get("items") or []):
                new_info.append("- %s: %s (stars %s, last push %s)" % (it["full_name"], (it.get("description") or "")[:120], it.get("stargazers_count"), (it.get("pushed_at") or "")[:10]))
        doc = ["# Draft upgrade: `%s`" % f, "", "Year %s cross-reference. Status: **%s**. Last changed %s days ago." % (year, status, age), "",
               "## What changed out in the world", ""]
        doc += ["- Dead link: %s" % u for u in dead] + ["- Legacy Emergent link (replace with a current Next-Xus domain): %s" % u for u in legacy]
        for n, s in repos_state:
            doc.append("- Repo %s: %s, last push %s, latest release %s. %s" % (
                n, "missing" if s["code"] == 404 else ("archived" if s.get("archived") else "active"),
                (s.get("pushed") or "?")[:10], s.get("release") or "none", s.get("desc") or ""))
        if new_info:
            doc += ["", "## Current related work on GitHub (new information to weigh)", ""] + new_info
        doc += ["", "## Suggested upgrade (old + new combined)", "",
                "Keep the original meaning. Replace dead and legacy links with their current homes, add a line naming the "
                "current state of each repo above, and fold in any new related work the Senate finds worthy. "
                "If the item is no longer needed, retire it: the original stays, a copy is kept in ARCHIVE/retired/%s/, and its status is marked retired by a human." % year,
                "", "## The original, kept whole", "", "```", text[:12000], "```"]
        upgrades["DROID/yearly/%s/upgrades/%s.md" % (year, f.replace("/", "__"))] = "\n".join(doc) + "\n"
        if status == "retire":
            retire.append(f)
        elif status == "review":
            review.append(f)

    hard, notes = directive_alignment()
    md = ["# Yearly cross-reference %s" % year, "", "Run: " + now_ct_str(), "",
          "%d items looked at. **%d retire candidates**, %d to review, %d draft upgrades written." % (len(rows), len(retire), len(review), len(upgrades)), "",
          "## Directives", "", "The official list is `directives/sacred-directives.yaml`; the sealed Cathedral file `00-immutable/directives.yaml` is the wording authority. The droid never retires or rewrites a directive."]
    md += ["- " + x for x in hard + notes] + ["",
           "## Retire candidates (archive copy proposed; nothing removed)", ""] + (["- `%s`" % x for x in retire] or ["None."]) + ["",
           "## Review candidates", ""] + (["- `%s`" % x for x in review] or ["None."]) + ["",
           "## Every item", "", "| Item | Days since change | URLs | Dead | Legacy | Missing or archived repos | Status |", "|---|---|---|---|---|---|---|"]
    md += ["| %s | %s | %s | %s | %s | %s | %s |" % r for r in rows]
    report = "\n".join(md)
    write_out("yearly", report, {"retire": retire, "review": review, "rows": rows})
    if "--no-pr" in sys.argv:
        return
    files = {"DROID/yearly/%s/crossref.md" % year: report + "\n"}
    files.update(upgrades)
    for f in retire:
        files["ARCHIVE/retired/%s/%s" % (year, f)] = read(f)
    propose_change("yearly-%s" % year, "Yearly cross-reference %s: %d retire candidates, %d draft upgrades" % (year, len(retire), len(upgrades)),
                   "The yearly cross-reference. This pull request only ADDS files: the report, draft upgrades that keep the old text "
                   "whole beside the new information, and archive copies of retire candidates. No original is changed or removed.\n\n"
                   "Roger or the Senate decides each item. Directive changes, if any, go through a Senate proposal; "
                   "the sealed Cathedral file is never touched.", files, label="droid-yearly")

if __name__ == "__main__":
    main()
