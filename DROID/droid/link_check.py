"""Module 3: dead-link and legacy-link checker for every Federation site and public repo.

Sites: crawls each configured site (same host only, up to max_pages) and checks every link and asset.
Repos: shallow-clones each public repo (read-only, no token needed) and checks every URL in its text files.
Flags: dead links, legacy Emergent hosts (never to be linked), http:// links, links to keywebco.github.io
(which redirects to next-xus.net). Big social sites that refuse robots count as "could not verify", not dead.

Files or updates ONE rolling issue (label droid-links). For legacy hosts whose replacement is confirmed in
DROID/config.yaml it drafts a pull request for this repo only; other repos get issue entries.
Usage: python3 DROID/droid/link_check.py [--sites-only] [--repos-only] [--repo NAME ...]
"""
import argparse
import concurrent.futures as cf
import html.parser
import os
import re
import subprocess
import sys
import tempfile
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CFG, LEGACY, GitHub, http, legacy_host_of, now_ct_str, write_out, redact, find_legacy, is_protected, is_history, propose_change, read, repo_files  # noqa: E402

LC = CFG.get("link_check", {})
SOFT = set(LC.get("soft_hosts", []))
IGNORE = set(LC.get("ignore_hosts", []))
URL_RE = re.compile(r"https?://[^\s\"'<>()\[\]{}`|\\^]+", re.I)
TRAIL = ".,;:!?*'\")]}>"

class LinkParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []
    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k in ("href", "src") and v:
                self.links.append(v.strip())

def clean(u):
    u = u.strip().rstrip(TRAIL)
    return u.split("#")[0]

def skip(u):
    if not u.lower().startswith(("http://", "https://")):
        return True
    host = (urllib.parse.urlsplit(u).hostname or "").lower()
    if not host or host in IGNORE or "${" in u or "{{" in u or "%7B%7B" in u:
        return True
    low = u.lower()
    if "\u2026" in u or "..." in u or low.endswith("/$") or "your_" in low or "your-" in low or "yourfile" in low or "&lt;" in low or "<" in u:
        return True     # placeholders and truncated examples, not real links
    if "." not in host:
        return True
    return False

def crawl(site):
    start, max_pages = site["url"], int(site.get("max_pages", 30))
    host = urllib.parse.urlsplit(start).hostname
    seen, queue, links, pages = set(), [start], [], 0
    while queue and pages < max_pages:
        page = queue.pop(0)
        if page in seen:
            continue
        seen.add(page)
        code, final, body, err = http(page, timeout=LC.get("timeout_seconds", 20))
        pages += 1
        if code != 200 or not body:
            links.append((site["name"] + " (crawl)", page, page))
            continue
        p = LinkParser()
        try:
            p.feed(body)
        except Exception:
            pass
        for raw in p.links:
            if raw.startswith(("mailto:", "tel:", "javascript:", "data:", "#")):
                continue
            u = clean(urllib.parse.urljoin(final, raw))
            if not u or skip(u):
                continue
            links.append((page, u, raw))
            uh = urllib.parse.urlsplit(u).hostname
            path = urllib.parse.urlsplit(u).path.lower()
            if uh == host and (path.endswith("/") or path.endswith(".html") or "." not in path.rsplit("/", 1)[-1]):
                if u not in seen and u not in queue:
                    queue.append(u)
    return links, pages

def scan_repo(name, workdir):
    exts = set(CFG["repos"].get("file_types", []))
    maxb = int(CFG["repos"].get("max_file_bytes", 400000))
    dest = os.path.join(workdir, name)
    url = "https://github.com/%s/%s.git" % (CFG["owner"], name)
    r = subprocess.run(["git", "clone", "-q", "--depth", "1", url, dest], capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        return [], "clone failed"
    out = []
    for d, dirs, fs in os.walk(dest):
        dirs[:] = [x for x in dirs if x not in (".git", "node_modules", "vendor", "dist", ".next")]
        for f in fs:
            if os.path.splitext(f)[1].lower() not in exts:
                continue
            full = os.path.join(d, f)
            if os.path.getsize(full) > maxb:
                continue
            rel = os.path.relpath(full, dest)
            if name == CFG["brain_repo"] and (is_history(rel) or rel.startswith("DROID/")):
                continue    # records of the past; their old links are history, not breakage
            try:
                text = open(full, encoding="utf-8", errors="replace").read()
            except Exception:
                continue
            for n, line in enumerate(text.splitlines(), 1):
                for m in URL_RE.finditer(line):
                    u = clean(m.group(0))
                    if not skip(u):
                        out.append(("%s:%s:%d" % (name, rel, n), u, m.group(0)))
                urls_in_line = " ".join(m.group(0).lower() for m in URL_RE.finditer(line))
                for h in set(find_legacy(line)):
                    if h not in urls_in_line:   # bare mention like "nextxus.online" with no https://
                        out.append(("%s:%s:%d" % (name, rel, n), "https://%s/" % h, "bare mention"))
    return out, ""

def check_url(u):
    tries = int(LC.get("tries", 2)); t = LC.get("timeout_seconds", 20)
    last = (0, u, "")
    for _ in range(tries):
        code, final, _, err = http(u, method="HEAD", timeout=t)
        if code in (405, 403, 400, 404, 501, 0) or code >= 500:
            code, final, _, err = http(u, method="GET", timeout=t, max_bytes=2048)
        last = (code, final, err)
        if 200 <= code < 400:
            break
    return u, last

def classify(u, res):
    """ok | dead | private | needs_key | unreachable | unverified"""
    code, final, err = res
    parts = urllib.parse.urlsplit(u)
    host = (parts.hostname or "").lower()
    if 200 <= code < 400:
        fh = (urllib.parse.urlsplit(final).hostname or "").lower()
        return "ok", ("redirects to " + fh) if fh and fh != host else ""
    if host in SOFT or any(host.endswith("." + s) for s in SOFT) or code in (403, 429):
        return "unverified", "HTTP %s" % code if code else err
    if code == 404 and any(host.endswith(x) for x in CFG.get("api_host_suffixes", [])) and parts.path not in ("", "/"):
        return "needs_key", "HTTP 404 on GET: a program route that may only take POST (the droid never sends one); confirm by hand"
    if code in (400, 401, 405, 406, 415, 422):
        return "needs_key", "HTTP %s: the address answers but wants a key, a POST, or parameters" % code
    segs = [x for x in parts.path.split("/") if x]
    if code == 404 and host == "github.com" and len(segs) >= 2 and segs[0].lower() == CFG["owner"].lower():
        return "private", "HTTP 404: the repo %s/%s is private, renamed, or gone" % (segs[0], segs[1])
    if code in (404, 410) or "Name or service not known" in err or "nodename nor servname" in err or "getaddrinfo" in err:
        return "dead", ("HTTP %s" % code) if code else "the name does not resolve"
    return "unreachable", ("HTTP %s" % code) if code else (err or "no answer")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sites-only", action="store_true")
    ap.add_argument("--repos-only", action="store_true")
    ap.add_argument("--repo", action="append", default=[])
    ap.add_argument("--max-repos", type=int, default=0)
    ap.add_argument("--no-issue", action="store_true")
    a = ap.parse_args()

    refs = []        # (where, url, raw)
    crawl_stats, repo_stats = [], []
    if not a.repos_only:
        for s in CFG.get("sites", []):
            links, pages = crawl(s)
            crawl_stats.append((s["name"], s.get("kind", "site"), pages, len(links)))
            refs += links
    if not a.sites_only:
        names = a.repo
        if not names and CFG["repos"].get("all_public_repos"):
            names = sorted(r["name"] for r in GitHub().owner_repos() if not r.get("archived"))
        names = [n for n in names if n not in set(CFG["repos"].get("exclude_repos", []))]
        if a.max_repos:
            names = names[: a.max_repos]
        with tempfile.TemporaryDirectory() as td:
            for n in names:
                found, err = scan_repo(n, td)
                repo_stats.append((n, len(found), err))
                refs += found

    # Legacy hosts first: never a network call needed.
    legacy, http_links, ghio = [], [], []
    for where, u, raw in refs:
        lh = legacy_host_of(u)
        if lh:
            legacy.append((where, u, lh))
        elif u.lower().startswith("http://"):
            http_links.append((where, u))
        elif (urllib.parse.urlsplit(u).hostname or "").lower() == "keywebco.github.io":
            ghio.append((where, u))

    EMERGENT = CFG.get("emergent_hosts", [])
    def is_emergent(u):
        h = (urllib.parse.urlsplit(u).hostname or "").lower()
        return any(h == e or h.endswith("." + e) for e in EMERGENT)
    emergent = [(w, u, "Emergent infrastructure; the Federation does not use Emergent") for w, u, _ in refs if is_emergent(u)]
    uniq = sorted({u for _, u, _ in refs if not legacy_host_of(u)})
    results = {}
    with cf.ThreadPoolExecutor(max_workers=int(LC.get("workers", 12))) as ex:
        for u, res in ex.map(check_url, uniq):
            results[u] = res
    status = {u: classify(u, r) for u, r in results.items()}
    def rows_of(kind):
        return [(w, u, status[u][1]) for w, u, _ in refs if u in status and status[u][0] == kind]
    dead = rows_of("dead")
    private = rows_of("private")
    unreachable = rows_of("unreachable")
    needs_key = sorted({u for u in status if status[u][0] == "needs_key"})
    unver = sorted({u for u in status if status[u][0] == "unverified"})

    def grouped(rows, limit=200):
        byurl = {}
        for w, u, why in rows:
            byurl.setdefault((u, why), []).append(w)
        lines = []
        for (u, why), ws in sorted(byurl.items())[:limit]:
            lines.append("- `%s` (%s), found in %d place(s): %s%s" % (u, why, len(ws), ", ".join("`%s`" % x for x in ws[:4]),
                                                                    " and more" if len(ws) > 4 else ""))
        if len(byurl) > limit:
            lines.append("- ...and %d more." % (len(byurl) - limit))
        return lines, len(byurl)

    dl, ndead = grouped(dead)
    pl, npriv = grouped(private, limit=80)
    ul, nunr = grouped(unreachable, limit=120)
    ll, nleg = grouped([(w, u, "legacy host " + h + ", suggest " + LEGACY[h]["replacement"] +
                         ("" if LEGACY[h].get("confirmed") else " (replacement not yet confirmed by Roger)")) for w, u, h in legacy])
    md = ["# Droid link check", "", "Checked: " + now_ct_str(), "",
          "%d references, %d unique URLs checked. **%d Emergent-hosted links or scripts**, **%d dead** (404, 410 or no such name), **%d legacy Emergent links**, %d links to private or missing Keywebco repos, %d unreachable this run (server error, timeout or TLS failure; retried next run), %d answer but want a key or a POST, %d could not be verified (sites that refuse robots), %d plain http links, %d links to keywebco.github.io (redirects to next-xus.net)." %
          (len(refs), len(uniq), len({u for _, u, _ in emergent}), ndead, nleg, npriv, nunr, len(needs_key), len(unver), len({u for _, u in http_links}), len({u for _, u in ghio})), ""]
    md += ["## Dead links", ""] + (dl or ["None."]) + [""]
    el, nem = grouped(emergent, limit=80)
    md += ["## Still loading from Emergent infrastructure (the Federation does not use Emergent)", ""] + (el or ["None."]) + [""]
    md += ["## Links to private, renamed or missing Keywebco repos", "", "Public pages should not point at private repos. Rename, make public, or remove the link (by pull request).", ""] + (pl or ["None."]) + [""]
    md += ["## Unreachable this run (retried next run before anyone acts)", ""] + (ul or ["None."]) + [""]
    md += ["## Legacy Emergent links (never link these; replace with a current Next-Xus domain)", "",
           "next-xus.com is a current domain but is still served by Emergent.", ""] + (ll or ["None."]) + [""]
    if http_links:
        hl, _ = grouped([(w, u, "use https") for w, u in http_links], limit=60)
        md += ["## Plain http links", ""] + hl + [""]
    if ghio:
        gl, _ = grouped([(w, u, "prefer next-xus.net") for w, u in ghio], limit=40)
        md += ["## keywebco.github.io links (work through a redirect; prefer the next-xus.net address)", ""] + gl + [""]
    if unver:
        md += ["## Could not verify (big sites often refuse robots; check by hand if it matters)", ""] + ["- `%s`" % u for u in unver[:60]] + [""]
    md += ["## What was scanned", "", "| Source | Kind | Pages or files | Links |", "|---|---|---|---|"]
    md += ["| %s | %s | %s pages | %s |" % s for s in crawl_stats]
    md += ["| %s | repo | %s | %s |" % (n, err or "scanned", c) for n, c, err in repo_stats]
    md += ["", "The droid only looked. It changed nothing. Fixes come as draft pull requests or issues for Roger's yes."]
    if needs_key:
        md.insert(md.index("## What was scanned"), "## Answer but want a key, a POST or parameters (not dead)\n\n" + "\n".join("- `%s`" % u for u in needs_key[:60]) + "\n")
    report = "\n".join(md)
    data = {"emergent": emergent, "dead": dead, "private": private, "unreachable": unreachable, "needs_key": needs_key, "legacy": legacy, "http": http_links, "ghio": ghio, "unverified": unver,
            "crawl": crawl_stats, "repos": repo_stats, "checked": len(uniq)}
    write_out("links", report, data)

    if a.no_issue:
        return
    if ndead or nleg or npriv:
        GitHub().upsert_issue("droid-links", "Droid: %d dead and %d legacy links (%s)" % (ndead, nleg, now_ct_str()[:10]), report)
    # Confirmed legacy replacements inside THIS repo become one draft PR.
    confirmed = {h: v["replacement"] for h, v in LEGACY.items() if v.get("confirmed")}
    if confirmed and CFG.get("maintenance", {}).get("auto_propose"):
        files = {}
        for f in repo_files({".md", ".yaml", ".yml", ".json", ".html", ".txt"}, include_protected=False):
            if is_history(f):
                continue
            text = read(f); new = text
            for h, rep in confirmed.items():
                new = re.sub(r"https?://(?:www\.)?%s/?" % re.escape(h), rep, new)
            if new != text:
                files[f] = new
        if files:
            propose_change("legacy-links-" + now_ct_str()[:10], "Replace confirmed legacy Emergent links (%d files)" % len(files),
                           "Replaces links to retired Emergent hosts with the confirmed Next-Xus addresses from DROID/config.yaml.", files)

if __name__ == "__main__":
    main()
