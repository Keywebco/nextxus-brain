"""Module 7: the evolution proposer. Once a month it reads what the other modules found and what the
Federation looks like, and suggests new ideas and evolutions. Ideas only: it files ONE rolling issue
(label droid-idea) and, if asked with --pr, a draft pull request adding DROID/ideas/<date>.md.

Rules it uses (plain heuristics, no paid model):
  * a repo with GitHub Pages that no scanned site links to -> add it to a directory page or the link scan;
  * a live site with no sitemap.xml or robots.txt -> add one so search engines find the new structure;
  * a repo quiet for a long time -> revive, fold into another, or archive (never delete);
  * repeated failed workflow runs -> harden that workflow;
  * a directive number that no brain file ever mentions -> a gap between the canon and the builds;
  * a mind in 03-minds without a heartbeat or status field -> give each mind a visible pulse;
  * many legacy Emergent links -> finish the move and confirm replacements in DROID/config.yaml;
  * the watcher pattern: every new kind of finding becomes a rule in the Sentinel (droid-watch).
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CFG, GitHub, http, now_ct_str, propose_change, read, read_out, repo_files, today, write_out  # noqa: E402

def main():
    ideas = []
    gh = GitHub()
    repos = gh.owner_repos()
    links = read_out("links") or {}
    health = read_out("health") or {}
    quality = read_out("quality") or {}

    linked_text = " ".join(" ".join(map(str, x)) for x in (links.get("crawl") or []))
    for s in CFG.get("sites", []):
        if s.get("kind") != "site":
            continue
        for p in ("sitemap.xml", "robots.txt"):
            code, _, _, _ = http(s["url"].rstrip("/") + "/" + p, timeout=15, max_bytes=1024)
            if code != 200:
                what = "a sitemap listing every page" if p == "sitemap.xml" else "a robots.txt that points to the sitemap"
                ideas.append(("search", "%s has no %s. Add %s so search engines pick up the new structure." % (s["url"], p, what)))
    pages_repos = [r["name"] for r in repos if r.get("has_pages") and not r.get("archived")]
    brain_text = " ".join(read(f) for f in repo_files({".md", ".yaml", ".yml"}) if not f.startswith("DROID/"))
    for n in pages_repos:
        if n not in brain_text:
            ideas.append(("map", "Repo %s has a live GitHub Pages site but the brain never names it. Add it to 04-builds/sites.yaml and a directory page." % n))
    for x in health.get("ok", []):
        if "quiet for" in x:
            ideas.append(("tidy", x))
    for x in health.get("attention", []):
        if "failed workflow" in x:
            ideas.append(("harden", "Harden this workflow so it stops failing: " + x))
    practice_text = " ".join(read(f) for f in repo_files({".md", ".yaml", ".yml"})
                             if not f.startswith(("DROID/", "00-immutable/", "framework/DIRECTIVES/", "directives/")))
    for n in range(1, int(CFG["directives"]["counted"]) + 1):
        tag = "DIR-%03d" % n
        if not re.search(r"\b%s\b" % tag, practice_text):
            ideas.append(("canon", "%s is never referenced by a build, mind or ruling. Is there a practice that lives it out? A Senate proposal could name one." % tag))
    for f in repo_files({".yaml"}):
        if f.startswith("03-minds/") and f != "03-minds/index.yaml":
            t = read(f)
            if not re.search(r"^\s*(status|heartbeat|last_seen)\s*:", t, re.M):
                ideas.append(("pulse", "Mind `%s` has no status or heartbeat field. A one-line pulse would let the droid say which minds are awake." % f))
    if links.get("legacy"):
        ideas.append(("move", "%d legacy Emergent links remain across sites and repos. Confirm the replacement for each legacy host in DROID/config.yaml so the droid can draft the fix PRs." % len(links["legacy"])))
    if quality.get("hard"):
        ideas.append(("guard", "The quality check found %d hard problems. Add a pre-merge check (droid-watch already runs on pull requests) so they cannot come back." % len(quality["hard"])))
    ideas.append(("watch", "Always-watching, inside our own system: the Sentinel (droid-watch) reads every push and pull request. Next step: give it a short memory file of past findings so it can say 'this came back' and learn which rules matter most."))
    ideas.append(("senate", "Let the Senate vote on droid ideas: an idea issue labelled senate-vote could be read aloud at the weekly meeting, and a ruling turns it into a build order."))

    groups = {}
    for k, v in ideas:
        groups.setdefault(k, []).append(v)
    names = {"search": "Help search engines", "map": "Map what exists", "tidy": "Revive or archive", "harden": "Harden",
             "canon": "Canon gaps (directives with no living practice)", "pulse": "Give minds a pulse", "move": "Finish the move off Emergent",
             "guard": "Guard quality", "watch": "Always-watching evolution", "senate": "Governance"}
    md = ["# Droid ideas and evolutions", "", "Thought up: " + now_ct_str(), "",
          "%d ideas. These are suggestions only. Roger or the Senate chooses; nothing is built without a yes." % len(ideas), ""]
    for k, vs in groups.items():
        md += ["## " + names.get(k, k), ""] + ["- " + v for v in vs[:25]] + ([("- ...and %d more." % (len(vs) - 25))] if len(vs) > 25 else []) + [""]
    report = "\n".join(md)
    write_out("ideas", report, {"ideas": ideas})
    if "--no-issue" in sys.argv:
        return
    gh.upsert_issue("droid-idea", "Droid ideas for %s" % now_ct_str()[:7], report)
    if "--pr" in sys.argv:
        propose_change("ideas-" + today(), "Droid ideas %s" % today(), "A dated ideas file for the record.", {"DROID/ideas/%s.md" % today(): report + "\n"}, label="droid-idea")

if __name__ == "__main__":
    main()
