"""Module 2: quality and lint checks on the brain repo itself.

  * every YAML and JSON file parses;
  * the official directives copy (directives/sacred-directives.yaml) still matches the sealed Cathedral
    wording (00-immutable/directives.yaml): DIR-000 gate plus DIR-001..073, same ids, same text, same titles;
  * the Nova-Canon seal report says PASS (reused, not re-hashed here);
  * no secrets in tracked files (reported by kind and place only, never the value);
  * legacy Emergent host mentions outside history folders;
  * broken relative links between files in this repo;
  * hygiene: CRLF endings, tabs in YAML, missing final newline, files over 1 MB;
  * "NextXus" written without the hyphen in prose (advice only);
  * the droid's own code holds no merge call (self-check of the never-auto-merge rule).
Exit code 1 only for hard failures (unparseable files, directive drift, secrets, failed seal).
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yaml  # noqa: E402
from common import CFG, ROOT, find_legacy, is_history, is_protected, now_ct_str, read, repo_files, secret_kinds, write_out, GitHub  # noqa: E402

def norm_title(t):
    return " ".join(t.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"').lower().split())

def directive_alignment():
    d = CFG["directives"]
    hard, notes = [], []
    try:
        off = yaml.safe_load(read(d["official"]))
        sea = yaml.safe_load(read(d["sealed"]))
    except Exception as e:
        return ["Could not read the directive files: %s" % e], notes
    def items(doc, textkey):
        g = doc.get("gate") or {}
        rows = [(g.get("id"), (g.get("title") or "").strip(), (g.get(textkey) or g.get("text") or g.get("content") or "").strip())]
        for x in doc.get("directives", []):
            rows.append((x.get("id"), (x.get("title") or "").strip(), (x.get(textkey) or x.get("text") or x.get("content") or "").strip()))
        return rows
    o, s = items(off, "text"), items(sea, "content")
    want = [d["gate"]] + ["DIR-%03d" % n for n in range(1, int(d["counted"]) + 1)]
    if [r[0] for r in s] != want:
        hard.append("The sealed file does not hold %s plus DIR-001..%03d in order." % (d["gate"], d["counted"]))
    if [r[0] for r in o] != want:
        hard.append("The official copy does not hold %s plus DIR-001..%03d in order (it has %d items)." % (d["gate"], d["counted"], len(o)))
    sd = {r[0]: r for r in s}
    for i, t, x in o:
        if i not in sd:
            continue
        if " ".join(x.split()) != " ".join(sd[i][2].split()):
            hard.append("%s text differs from the sealed Cathedral wording." % i)
        if norm_title(t) != norm_title(sd[i][1]):
            hard.append("%s title differs from the sealed file ('%s' vs '%s')." % (i, t, sd[i][1]))
    if not hard:
        notes.append("Official directives copy matches the sealed Cathedral wording: %s + %d directives." % (d["gate"], d["counted"]))
    return hard, notes

def seal_report():
    p = CFG["existing_reports"]["seal"]["path"]
    try:
        t = read(p)
    except Exception:
        return ["The Nova-Canon seal report %s is missing." % p], []
    if "**FAIL**" in t:
        return ["Nova-Canon reports the seal FAILED (see %s)." % p], []
    return [], ["Nova-Canon seal report says PASS (reused from %s)." % p]

def main():
    hard, warn, notes = [], [], []
    legacy_files = {}
    files = repo_files()
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        full = os.path.join(ROOT, f)
        if not os.path.isfile(full) or f.startswith("DROID/out/"):
            continue
        size = os.path.getsize(full)
        if size > 1_000_000:
            warn.append("`%s` is over 1 MB (%d bytes)." % (f, size))
            continue
        raw = open(full, "rb").read()
        if b"\0" in raw[:4096]:
            continue
        text = raw.decode("utf-8", "replace")
        if ext in (".yaml", ".yml"):
            try:
                list(yaml.safe_load_all(text))
            except Exception as e:
                hard.append("`%s` is not valid YAML: %s" % (f, str(e).splitlines()[0][:120]))
            if "\t" in text:
                warn.append("`%s` has tab characters (YAML wants spaces)." % f)
        elif ext == ".json":
            try:
                json.loads(text)
            except Exception as e:
                hard.append("`%s` is not valid JSON: %s" % (f, str(e)[:120]))
        if ext in (".yaml", ".yml", ".md", ".json", ".py", ".txt") and not is_protected(f):
            if b"\r\n" in raw:
                warn.append("`%s` has Windows line endings." % f)
            if raw and not raw.endswith(b"\n"):
                warn.append("`%s` has no final newline." % f)
        if secret_kinds(text):
            for n, line in enumerate(text.splitlines(), 1):
                kinds = secret_kinds(line)
                if kinds:
                    hard.append("Possible secret (%s) at `%s` line %d. The value is not shown. Rotate it if real." % (", ".join(kinds), f, n))
        if not is_history(f) and not is_protected(f) and f not in CFG.get("legacy_watch_files", []):
            hits = find_legacy(text)
            if hits:
                per = {}
                for h in hits:
                    per[h] = per.get(h, 0) + 1
                legacy_files[f] = per
        if ext == ".md":
            for m in re.finditer(r"\]\((?!https?:|mailto:|#)([^)\s]+)\)", text):
                target = m.group(1).split("#")[0]
                if target and not os.path.exists(os.path.normpath(os.path.join(ROOT, os.path.dirname(f), target))):
                    warn.append("Broken relative link in `%s`: `%s`." % (f, target))
        if ext == ".md" and not is_history(f) and not is_protected(f):
            n_bad = len(re.findall(r"\bNext[Xx]us\b(?![-/\w.])", text))
            if n_bad:
                notes.append("`%s` writes NextXus without the hyphen %d time(s); new text should say Next-Xus." % (f, n_bad))
    if legacy_files:
        total = sum(sum(v.values()) for v in legacy_files.values())
        top = ["Legacy Emergent hosts are mentioned %d times in %d files (outside history folders). Each needs review: replace with a current Next-Xus domain or mark as history." % (total, len(legacy_files))]
        for f, per in sorted(legacy_files.items(), key=lambda kv: -sum(kv[1].values()))[:60]:
            top.append("Legacy hosts in `%s`: %s." % (f, ", ".join("%s x%d" % kv for kv in sorted(per.items()))))
        warn[:0] = top
    h, n = directive_alignment(); hard += h; notes += n
    h, n = seal_report(); hard += h; notes += n
    # Self-check: the droid itself must never contain merge calls.
    for f in repo_files({".py", ".yml", ".yaml"}):
        if f.startswith("DROID/droid/") or f.startswith(".github/workflows/droid"):
            t = read(f)
            if re.search(r"merge_pull_request|pulls/\S+/merge|gh pr merge|--auto", t) and "never" not in t[:0]:
                if f != "DROID/droid/quality_check.py":
                    hard.append("Self-check: `%s` contains merge code. The droid must never merge." % f)
    md = ["# Droid quality check", "", "Checked: " + now_ct_str(), "",
          "%d files looked at. **%d hard problems**, %d warnings, %d notes." % (len(files), len(hard), len(warn), len(notes)), ""]
    md += ["## Hard problems", ""] + (["- " + x for x in hard] or ["None."]) + [""]
    md += ["## Warnings", ""] + (["- " + x for x in warn[:150]] or ["None."]) + ([("- ...and %d more." % (len(warn) - 150))] if len(warn) > 150 else []) + [""]
    md += ["## Notes", ""] + (["- " + x for x in notes[:80]] or ["None."]) + [""]
    md += ["Nothing was changed. 00-immutable and the sealed Cathedral file are read, never written."]
    report = "\n".join(md)
    write_out("quality", report, {"hard": hard, "warn": warn, "notes": notes})
    if hard and "--no-issue" not in sys.argv:
        GitHub().upsert_issue("droid-quality", "Droid quality: %d hard problems (%s)" % (len(hard), now_ct_str()[:10]), report)
    sys.exit(1 if hard else 0)

if __name__ == "__main__":
    main()
