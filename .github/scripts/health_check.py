"""Federation health check. Runs on GitHub's own workers, so it keeps working if Emergent or Render lapse.
Two rules so it tells the truth:
  1. A free server asleep is not "down": a slow answer is retried, and only a repeated failure counts.
  2. A page that answers 200 can still be broken, so each page is also checked for a phrase it must contain
     and for damage it must not contain.
It writes LATTICE/reports/health.md and exits 1 only when something is really wrong."""
import json, sys, time, urllib.request, urllib.error, datetime

UA = {"User-Agent": "NextXus-health-check/1.0"}

def fetch(url, timeout):
    req = urllib.request.Request(url, headers=UA)
    t = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(400000).decode("utf-8", "replace"), round(time.time() - t, 1)
    except urllib.error.HTTPError as e:
        return e.code, "", round(time.time() - t, 1)
    except Exception as e:
        return 0, "", round(time.time() - t, 1)

def check(item):
    url, must, forbid, timeout, tries = item["url"], item.get("must", []), item.get("forbid", []), item.get("timeout", 30), item.get("tries", 2)
    expect = item.get("expect", 200)
    last = None
    for i in range(tries):
        code, body, secs = fetch(url, timeout)
        problems = []
        if code != expect: problems.append("HTTP %s (expected %s)" % (code or "no answer", expect))
        for m in must:
            if code == expect and m not in body: problems.append("missing: " + m)
        for f in forbid:
            if code == expect and f in body: problems.append("found damage: " + f)
        last = {"name": item["name"], "url": url, "code": code, "secs": secs, "problems": problems, "kind": item.get("kind", "site")}
        if not problems: return last
        if i + 1 < tries: time.sleep(item.get("wait", 20))
    return last

def main():
    items = json.load(open(".github/scripts/health_targets.json", encoding="utf-8"))
    results = [check(i) for i in items]
    bad = [r for r in results if r["problems"]]
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    lines = ["# Federation health report", "", "Checked: " + now, "",
             "%d of %d checks passed." % (len(results) - len(bad), len(results)), ""]
    if bad:
        lines += ["## Problems", ""]
        for r in bad: lines.append("- **%s** (%s): %s" % (r["name"], r["url"], "; ".join(r["problems"])))
        lines.append("")
    lines += ["## All checks", "", "| Check | Kind | Result | Seconds |", "|---|---|---|---|"]
    for r in results:
        lines.append("| %s | %s | %s | %s |" % (r["name"], r["kind"], "OK" if not r["problems"] else "PROBLEM", r["secs"]))
    lines += ["", "A free server that was asleep is retried before it counts as a problem. A page that answers 200 is also checked for a phrase it must contain and for known damage.",
              "The Emergent-hosted domains are watched only. They are never edited."]
    open("LATTICE/reports/health.md", "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    sys.exit(1 if bad else 0)

main()
