"""Module 1: health of all Federation systems and files, built ON TOP of the existing machinery.

It does not re-check the sites (the 4-hourly health check and uptime timer already do that) and it does not
re-hash the seal (Nova-Canon does that daily). Instead it:
  * reads LATTICE/reports/health.md, LATTICE/reports/latest.md and status/uptime-latest.md, and alarms if any
    of those timers has gone quiet (report older than its limit) or reports problems;
  * checks every public Keywebco repo through the GitHub API with the built-in token: archived or not, last push,
    latest GitHub Pages build, and failed workflow runs in the last 7 days;
  * counts open health, uptime and droid issues so nothing is forgotten.
Writes DROID/out/health.md and updates ONE rolling issue (label droid-health) when something needs attention.
"""
import datetime
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CFG, GitHub, now_ct_str, now_utc, read, write_out  # noqa: E402

def report_age(path):
    try:
        t = read(path)
    except Exception:
        return None, "missing"
    m = re.search(r"(\d{4}-\d{2}-\d{2})[ T](\d{2}):(\d{2})\s*UTC", t)
    if m:
        dt = datetime.datetime.strptime("%s %s:%s" % m.groups(), "%Y-%m-%d %H:%M").replace(tzinfo=datetime.timezone.utc)
        return (now_utc() - dt).total_seconds() / 3600, t
    m = re.search(r"(\d{4}-\d{2}-\d{2}) (\d{1,2}):(\d{2}) ([AP]M)", t)
    if m:
        from zoneinfo import ZoneInfo
        dt = datetime.datetime.strptime("%s %s:%s %s" % m.groups(), "%Y-%m-%d %I:%M %p").replace(tzinfo=ZoneInfo("America/Chicago"))
        return (now_utc() - dt).total_seconds() / 3600, t
    m = re.search(r"(\d{1,2}):(\d{2}) ([AP]M) Central on \w+, (\w+) (\d{1,2})", t)
    if m:
        from zoneinfo import ZoneInfo
        hh, mm, ap, mon, day = m.groups()
        year = now_utc().year
        dt = datetime.datetime.strptime("%s %s %s %s:%s %s" % (year, mon, day, hh, mm, ap), "%Y %B %d %I:%M %p").replace(tzinfo=ZoneInfo("America/Chicago"))
        if dt > now_utc() + datetime.timedelta(days=1):
            dt = dt.replace(year=year - 1)
        return (now_utc() - dt).total_seconds() / 3600, t
    return None, t

def main():
    attention, ok = [], []
    for key, r in CFG.get("existing_reports", {}).items():
        age, text = report_age(r["path"])
        if text == "missing":
            attention.append("The %s report (%s) is missing. Its timer, %s, may be off." % (key, r["path"], r["made_by"])); continue
        if age is None:
            attention.append("Could not read a time in the %s report (%s)." % (key, r["path"]))
        elif age > r["max_age_hours"]:
            attention.append("The %s timer (%s) looks stalled: last report is %.0f hours old (limit %s)." % (key, r["made_by"], age, r["max_age_hours"]))
        else:
            ok.append("%s report is fresh (%.1f hours old)." % (key, age))
        if key == "health":
            m = re.search(r"(\d+) of (\d+) checks passed", text or "")
            if m and m.group(1) != m.group(2):
                probs = (text.split("## Problems")[1].split("## All checks")[0].strip().splitlines() if "## Problems" in text else [])
                attention.append("Health check: %s of %s passed. %s" % (m.group(1), m.group(2), " ".join(p.strip() for p in probs[:6])))
            elif m:
                ok.append("Health check: all %s checks passed." % m.group(2))
        if key == "seal" and "**FAIL**" in (text or ""):
            attention.append("Nova-Canon says the seal FAILED. Roger decides; nothing is auto-fixed.")
        if key == "uptime":
            low = (text or "").lower()
            if re.search(r"\b(not answering|down|failed)\b", low):
                attention.append("The uptime status mentions a site or server not answering (see %s)." % r["path"])

    gh = GitHub()
    repos = gh.owner_repos()
    since = now_utc() - datetime.timedelta(days=7)
    quiet_days = int(CFG.get("maintenance", {}).get("quiet_repo_days", 180))
    rows = []
    for r in sorted(repos, key=lambda x: x["name"].lower()):
        name = r["name"]
        pushed = datetime.datetime.fromisoformat(r["pushed_at"].replace("Z", "+00:00")) if r.get("pushed_at") else None
        pages, failed = "-", 0
        if r.get("has_pages") and gh.token:
            code, b = gh.api("GET", "/repos/%s/%s/pages/builds/latest" % (CFG["owner"], name))
            if code == 200 and b:
                pages = b.get("status", "?")
                if pages == "errored":
                    attention.append("GitHub Pages build for %s errored: %s" % (name, ((b.get("error") or {}).get("message") or "")[:120]))
        code, runs = gh.api("GET", "/repos/%s/%s/actions/runs" % (CFG["owner"], name), params={"per_page": 30, "created": ">=" + since.strftime("%Y-%m-%d")})
        if code == 200 and runs:
            bad = [x for x in runs.get("workflow_runs", []) if x.get("conclusion") in ("failure", "timed_out", "startup_failure")]
            failed = len(bad)
            names = sorted({x.get("name", "?") for x in bad})
            if failed:
                attention.append("%s: %d failed workflow run(s) in 7 days (%s)." % (name, failed, ", ".join(names[:4])))
        age_days = (now_utc() - pushed).days if pushed else None
        rows.append("| %s | %s | %s | %s | %s |" % (name, "archived" if r.get("archived") else "active",
                                                   "%s days ago" % age_days if age_days is not None else "?", pages, failed))
        if age_days is not None and age_days > quiet_days and not r.get("archived"):
            ok.append("%s has been quiet for %d days (idea: revive or archive; never delete)." % (name, age_days))

    open_counts = []
    for label in ("health-check", "droid-links", "droid-quality", "droid-maintenance", "droid-idea", "droid-proposal"):
        code, iss = gh.api("GET", "/repos/%s/issues" % gh.repo, params={"state": "open", "labels": label, "per_page": 50})
        if code == 200 and iss:
            open_counts.append("%s: %d open" % (label, len(iss)))

    md = ["# Droid health sweep", "", "Checked: " + now_ct_str(), "",
          "**%d items need attention.** %d public repos looked at." % (len(attention), len(repos)), "",
          "## Needs attention", ""] + (["- " + x for x in attention] or ["Nothing."]) + ["",
          "## Fine", ""] + ["- " + x for x in ok] + ["",
          "## Open issues by label", ""] + (["- " + x for x in open_counts] or ["None open."]) + ["",
          "## Every public repo", "", "| Repo | State | Last push | Pages build | Failed runs (7 days) |", "|---|---|---|---|---|"] + rows + ["",
          "This sweep reads the existing health, seal and uptime reports and GitHub's own records. It changed nothing."]
    report = "\n".join(md)
    write_out("health", report, {"attention": attention, "ok": ok})
    if attention and "--no-issue" not in sys.argv:
        gh.upsert_issue("droid-health", "Droid health: %d items need attention (%s)" % (len(attention), now_ct_str()[:10]), report)

if __name__ == "__main__":
    main()
