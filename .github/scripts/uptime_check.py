#!/usr/bin/env python3
"""Federation uptime timer.

Checks each Federation site and server over https, writes a short plain-words
status file a bot can read aloud (status/uptime-latest.md), and keeps one
GitHub issue per site that is not answering. When the site answers again the
issue gets a plain-words comment and is closed. It only reads the sites. It
never changes any site or server, and it uses no keys except the workflow's
own built-in GitHub token for issues.
"""
import json, os, sys, time, urllib.request, urllib.error
from datetime import datetime
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
TARGETS = json.load(open(os.path.join(HERE, "uptime_targets.json")))
CENTRAL = ZoneInfo("America/Chicago")
LABEL = "uptime"
REPO = os.environ.get("GITHUB_REPOSITORY", "")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
UA = "Next-Xus-Federation-uptime-timer/1.0 (GitHub Actions)"


def spoken_time(dt):
    h = dt.strftime("%I").lstrip("0")
    return f"{h}:{dt.strftime('%M %p')} Central on {dt.strftime('%A, %B')} {dt.day}"


def times_word(n):
    return {1: "once", 2: "twice"}.get(n, f"{n} times")


def check(t):
    tries = int(t.get("tries", 2))
    last = ""
    for i in range(1, tries + 1):
        try:
            req = urllib.request.Request(t["url"], headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=int(t.get("timeout", 30))) as r:
                if r.status < 400:
                    return True, i, ""
                last = f"it answered with error code {r.status}"
        except urllib.error.HTTPError as e:
            last = f"it answered with error code {e.code}"
        except Exception as e:  # timeout, DNS, TLS
            last = "it did not answer in time" if "timed out" in str(e).lower() else "it could not be reached"
        if i < tries:
            time.sleep(int(t.get("wait", 20)))
    return False, tries, last


def gh(method, path, body=None):
    if not (TOKEN and REPO):
        return None
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}{path}",
        method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json",
                 "User-Agent": UA, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            txt = r.read().decode()
            return json.loads(txt) if txt else {}
    except Exception as e:
        print(f"GitHub issue step did not work ({method} {path}): {e}", file=sys.stderr)
        return None


def title_for(name):
    return f"Not answering: {name}"


def main():
    now = datetime.now(CENTRAL)
    when = spoken_time(now)
    results = []
    for t in TARGETS:
        ok, n, why = check(t)
        results.append((t, ok, n, why))
        print(f"{t['name']}: {'up' if ok else 'DOWN'} ({t['url']})")

    open_issues = gh("GET", f"/issues?state=open&labels={LABEL}&per_page=100") or []
    by_title = {i["title"]: i for i in open_issues if "pull_request" not in i}

    for t, ok, n, why in results:
        title = title_for(t["name"])
        issue = by_title.get(title)
        if not ok:
            text = (f"{t['name']} did not answer at {when}. It was checked {times_word(n)}, "
                    f"and {why}.")
            if t.get("kind") == "server":
                text += (" This is a free server that can fall asleep, so it was given extra time "
                         "and extra tries before being called down.")
            text += " Nothing was changed automatically."
            if issue:
                gh("POST", f"/issues/{issue['number']}/comments", {"body": "Still not answering. " + text})
            else:
                gh("POST", "/issues", {"title": title, "labels": [LABEL],
                                        "body": text + f"\n\nAddress checked: {t['url']}"})
        elif issue:
            gh("POST", f"/issues/{issue['number']}/comments",
               {"body": f"{t['name']} is answering again as of {when}. Closing this issue."})
            gh("PATCH", f"/issues/{issue['number']}", {"state": "closed"})

    down = [r for r in results if not r[1]]
    total = len(results)
    lines = ["# Federation uptime, latest check", ""]
    lines.append(f"Checked at {when}.")
    lines.append("")
    if not down:
        lines.append(f"All {total} Federation sites and servers answered.")
    else:
        lines.append(f"{total - len(down)} of {total} Federation sites and servers answered. "
                     f"{len(down)} did not.")
        lines.append("")
        for t, ok, n, why in down:
            lines.append(f"- {t['name']} did not answer. It was checked {times_word(n)}, and {why}.")
    lines.append("")
    lines.append("## Everything checked")
    lines.append("")
    for t, ok, n, why in results:
        lines.append(f"- {t['name']}: {'answering' if ok else 'not answering'}.")
    lines.append("")
    lines.append("This timer runs on GitHub's free schedule about every four hours. It only looks. "
                 "It never changes a site or server.")
    os.makedirs("status", exist_ok=True)
    with open("status/uptime-latest.md", "w") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
