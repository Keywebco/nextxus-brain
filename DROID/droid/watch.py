"""Module 6b: the Sentinel. The always-watching part, inside our own system (the Agent Zero pattern).

Runs on every push to main and every pull request. It reads only what changed and checks it against the
guardrails:
  * 00-immutable/ or the sealed Cathedral file touched -> loud alarm (issue or PR comment);
  * any file deleted -> Echo 64 alarm (never delete; archive first);
  * an existing file overwritten without an archive copy in the same change -> Echo 64 reminder;
  * new legacy Emergent links added -> flagged with the suggested current Next-Xus domain;
  * anything that looks like a secret added -> flagged by kind and place, never the value;
  * a changed YAML/JSON file that no longer parses;
  * the official directives copy changed -> re-check against the sealed Cathedral wording.
On a pull request it comments on that PR. On a push it files or updates ONE issue (label droid-watch).
It never reverts, edits or merges anything.
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yaml  # noqa: E402
from common import CFG, LEGACY, ROOT, GitHub, find_legacy, is_history, is_protected, now_ct_str, secret_kinds, write_out  # noqa: E402
from quality_check import directive_alignment  # noqa: E402

def git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True).stdout

def main():
    base = os.environ.get("DROID_BASE") or (sys.argv[1] if len(sys.argv) > 1 else "HEAD~1")
    head = os.environ.get("DROID_HEAD") or "HEAD"
    changes = [l.split("\t") for l in git("diff", "--name-status", "--no-renames", base, head).splitlines() if l.strip()]
    alarms, flags = [], []
    added_or_changed = [c[-1] for c in changes if c[0][0] in "AM"]
    archived_now = {c[-1] for c in changes if c[0][0] == "A" and c[-1].startswith("ARCHIVE/")}
    for c in changes:
        st, path = c[0][0], c[-1]
        if is_protected(path) and not path.startswith(".github/workflows/"):
            alarms.append("Protected path changed: `%s` (%s). 00-immutable and the sealed Cathedral file are never to be touched." % (path, {"A": "added", "M": "modified", "D": "deleted"}.get(st, st)))
        if st == "D":
            alarms.append("Echo 64: `%s` was deleted. Nothing is deleted; restore it or move it to ARCHIVE/." % path)
        if st == "M" and not any(a.endswith("/" + path) for a in archived_now) and not path.startswith(("LATTICE/reports/", "status/")):
            stat = git("diff", "--numstat", base, head, "--", path).split()
            if len(stat) >= 2 and stat[1].isdigit():
                removed_n = int(stat[1])
                old_n = len(git("show", "%s:%s" % (base, path)).splitlines()) or 1
                if removed_n >= 20 and removed_n / old_n > 0.3:
                    flags.append("`%s` lost %d of %d lines with no archive copy in the same change. Echo 64: archive before overwriting." % (path, removed_n, old_n))
    for path in added_or_changed:
        diff = git("diff", "-U0", base, head, "--", path)
        added = "\n".join(l[1:] for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++"))
        removed = "\n".join(l[1:] for l in diff.splitlines() if l.startswith("-") and not l.startswith("---"))
        new_legacy = len(find_legacy(added)) - len(find_legacy(removed))
        if new_legacy > 0 and not is_history(path) and path not in CFG.get("legacy_watch_files", []):
            hosts = sorted(set(find_legacy(added)))
            flags.append("`%s` adds %d legacy Emergent link(s): %s. Use %s instead." % (path, new_legacy, ", ".join(hosts),
                         ", ".join(LEGACY[h]["replacement"] for h in hosts if h in LEGACY)))
        kinds = secret_kinds(added)
        if kinds:
            alarms.append("`%s` adds something that looks like a secret (%s). The value is not shown. Remove it and rotate the key." % (path, ", ".join(kinds)))
        full = os.path.join(ROOT, path)
        if os.path.isfile(full):
            ext = os.path.splitext(path)[1].lower()
            try:
                if ext in (".yaml", ".yml"):
                    list(yaml.safe_load_all(open(full, encoding="utf-8")))
                elif ext == ".json":
                    json.load(open(full, encoding="utf-8"))
            except Exception as e:
                flags.append("`%s` no longer parses: %s" % (path, str(e).splitlines()[0][:120]))
        if path == CFG["directives"]["official"]:
            hard, notes = directive_alignment()
            (alarms if hard else flags).extend(hard or ["Official directives copy changed and still matches the sealed Cathedral wording."])
    md = ["# Sentinel watch", "", "Watched: " + now_ct_str() + " (%s..%s)" % (base[:12], head[:12]), "",
          "%d files changed. **%d alarms**, %d flags." % (len(changes), len(alarms), len(flags)), "",
          "## Alarms", ""] + (["- " + x for x in alarms] or ["None."]) + ["", "## Flags", ""] + (["- " + x for x in flags[:80]] or ["None."]) + ["",
          "The Sentinel only watches. It never reverts, edits or merges."]
    report = "\n".join(md)
    write_out("watch", report, {"alarms": alarms, "flags": flags})
    if "--no-issue" in sys.argv or not (alarms or flags):
        return
    gh = GitHub()
    pr = os.environ.get("DROID_PR")
    if pr:
        gh.comment(pr, report)
    elif alarms:
        gh.upsert_issue("droid-watch", "Sentinel: %d alarms on main (%s)" % (len(alarms), now_ct_str()[:10]), report)

if __name__ == "__main__":
    main()
