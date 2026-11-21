"""Shared pieces for the Next-Xus Maintenance Droid.

Guardrails live here so every module obeys them the same way:
  * Echo 64: never delete; archive before overwriting.
  * Never touch 00-immutable/ or the sealed Cathedral file (or workflow files).
  * Changes are only ever draft pull requests or issues. The droid has no merge code at all.
  * Never write a legacy Emergent host link. Flag them for replacement.
  * No secrets in output: everything written is passed through redact().
  * Only the built-in GITHUB_TOKEN is used.
"""
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

try:
    import yaml
except ImportError:  # pragma: no cover
    print("pyyaml is needed: pip install -r DROID/requirements.txt")
    raise

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "DROID", "out")          # run output (uploaded as an artifact, never committed by the droid)
UA = "Next-Xus-Maintenance-Droid/0.1 (+https://github.com/Keywebco/nextxus-brain)"

# ---------------------------------------------------------------- config

def load_config():
    with open(os.path.join(ROOT, "DROID", "config.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)

CFG = load_config()
LEGACY = {h.lower(): v for h, v in (CFG.get("legacy_hosts") or {}).items()}

def dry_run():
    """Dry run unless a token is present AND DROID_DRY_RUN is not '1'."""
    return os.environ.get("DROID_DRY_RUN", "1") == "1" or not os.environ.get("GITHUB_TOKEN")

# ---------------------------------------------------------------- guardrails

def sealed_paths():
    out = set()
    try:
        seal = yaml.safe_load(open(os.path.join(ROOT, "00-immutable", "SEAL.yaml"), encoding="utf-8"))
        for f in seal.get("files", []):
            out.add(f["path"])
    except Exception:
        pass
    return out

def is_protected(path):
    p = path.replace("\\", "/").removeprefix("./")
    if p in sealed_paths():
        return True
    if "cathedral" in p.lower():
        return True
    return any(p == x.rstrip("/") or p.startswith(x) for x in CFG.get("protected_paths", []))

def is_history(path):
    p = path.replace("\\", "/").removeprefix("./")
    return any(p.startswith(x) for x in CFG.get("history_paths", []))

class GuardrailError(RuntimeError):
    pass

SECRET_PATTERNS = {
    "openai-style key": r"\bsk-[A-Za-z0-9_\-]{16,}",
    "google api key": r"\bAIza[0-9A-Za-z_\-]{30,}",
    "github token": r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}|\bgithub_pat_[A-Za-z0-9_]{30,}",
    "slack token": r"\bxox[abprs]-[A-Za-z0-9\-]{10,}",
    "aws access key": r"\bAKIA[0-9A-Z]{16}\b",
    "private key block": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "stripe live key": r"\b[rs]k_live_[A-Za-z0-9]{16,}",
}
_SECRET_RE = re.compile("|".join("(?:%s)" % p for p in SECRET_PATTERNS.values()))

def secret_kinds(text):
    return [k for k, p in SECRET_PATTERNS.items() if re.search(p, text)]

def redact(text):
    """Every byte the droid writes to an issue, PR, summary or file goes through here."""
    return _SECRET_RE.sub("[secret hidden]", text or "")

def legacy_host_of(url_or_host):
    host = url_or_host
    if "://" in url_or_host:
        host = urllib.parse.urlsplit(url_or_host).hostname or ""
    host = host.lower().rstrip(".")
    for h in LEGACY:
        if host == h or host.endswith("." + h):
            return h
    return None

LEGACY_RE = re.compile(r"(?<![A-Za-z0-9\-])(?:https?://)?(?:[a-z0-9\-]+\.)*(%s)(?![A-Za-z0-9\-])" %
                       "|".join(re.escape(h) for h in LEGACY), re.I) if LEGACY else None

def find_legacy(text):
    return [m.group(1).lower() for m in LEGACY_RE.finditer(text)] if LEGACY_RE else []

# ---------------------------------------------------------------- time

def now_utc():
    return datetime.datetime.now(datetime.timezone.utc)

def now_ct_str():
    try:
        from zoneinfo import ZoneInfo
        return now_utc().astimezone(ZoneInfo("America/Chicago")).strftime("%Y-%m-%d %I:%M %p Central")
    except Exception:
        return now_utc().strftime("%Y-%m-%d %H:%M UTC")

def today():
    return now_utc().strftime("%Y-%m-%d")

# ---------------------------------------------------------------- http

class _UpgradeRedirect(urllib.request.HTTPRedirectHandler):
    """GitHub Pages sends keywebco.github.io/<repo> to http://next-xus.net/<repo>. Follow it over https."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parts = urllib.parse.urlsplit(newurl)
        if parts.scheme == "http" and (parts.hostname or "") in set(CFG.get("current_domains", [])) | {"keywebco.github.io"}:
            newurl = urllib.parse.urlunsplit(("https",) + tuple(parts[1:]))
        return super().redirect_request(req, fp, code, msg, headers, newurl)

_OPENER = urllib.request.build_opener(_UpgradeRedirect)

def safe_url(url):
    """Percent-encode anything outside ASCII so odd characters cannot crash a check."""
    p = urllib.parse.urlsplit(url)
    host = (p.hostname or "")
    try:
        host_enc = host.encode("idna").decode("ascii")
    except Exception:
        host_enc = host
    netloc = host_enc + (":%d" % p.port if p.port else "")
    return urllib.parse.urlunsplit((p.scheme, netloc, urllib.parse.quote(p.path, safe="/%:@!$&'()*+,;=-._~"),
                                    urllib.parse.quote(p.query, safe="=&%+/:,;@!$'()*-._~?"), ""))

def http(url, method="GET", timeout=20, max_bytes=600000, headers=None):
    """Returns (status, final_url, body_text, error). status 0 means no answer."""
    try:
        url = safe_url(url)
    except Exception:
        return 0, url, "", "bad url"
    h = {"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8"}
    h.update(headers or {})
    req = urllib.request.Request(url, method=method, headers=h)
    try:
        with _OPENER.open(req, timeout=timeout) as r:
            body = r.read(max_bytes).decode("utf-8", "replace") if method != "HEAD" else ""
            return r.status, r.geturl(), body, ""
    except urllib.error.HTTPError as e:
        return e.code, url, "", "HTTP %s" % e.code
    except Exception as e:
        return 0, url, "", type(e).__name__ + ": " + str(e)[:120]

# ---------------------------------------------------------------- GitHub (built-in GITHUB_TOKEN only)

class GitHub:
    def __init__(self):
        self.token = os.environ.get("GITHUB_TOKEN", "")
        self.repo = os.environ.get("GITHUB_REPOSITORY", "%s/%s" % (CFG["owner"], CFG["brain_repo"]))
        self.api_base = os.environ.get("GITHUB_API_URL", "https://api.github.com")

    def api(self, method, path, body=None, params=None):
        url = self.api_base + path
        if params:
            url += "?" + urllib.parse.urlencode(params)
        if "/merge" in path:
            raise GuardrailError("The droid never merges. Refused: " + path)
        data = json.dumps(body).encode() if body is not None else None
        h = {"User-Agent": UA, "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
        if self.token:
            h["Authorization"] = "Bearer " + self.token
        if data:
            h["Content-Type"] = "application/json"
        for attempt in range(3):
            req = urllib.request.Request(url, data=data, method=method, headers=h)
            try:
                with urllib.request.urlopen(req, timeout=30) as r:
                    txt = r.read().decode("utf-8", "replace")
                    return r.status, (json.loads(txt) if txt else None)
            except urllib.error.HTTPError as e:
                if e.code in (502, 503, 504) and attempt < 2:
                    time.sleep(5); continue
                try:
                    return e.code, json.loads(e.read().decode("utf-8", "replace"))
                except Exception:
                    return e.code, None
            except Exception as e:
                if attempt < 2:
                    time.sleep(5); continue
                return 0, {"error": str(e)[:200]}

    def owner_repos(self):
        repos, page = [], 1
        while True:
            code, data = self.api("GET", "/users/%s/repos" % CFG["owner"], params={"per_page": 100, "page": page, "type": "owner"})
            if code != 200 or not data:
                break
            repos += data
            if len(data) < 100:
                break
            page += 1
        return [r for r in repos if not r.get("private")]

    # ---- issues: one rolling issue per label, never a flood
    def upsert_issue(self, label, title, body):
        body = redact(body)
        if dry_run():
            print("[dry run] would file or update issue [%s] %s" % (label, title))
            return None
        self.api("POST", "/repos/%s/labels" % self.repo, {"name": label, "color": "5319e7",
                                                         "description": "Filed by the Next-Xus Maintenance Droid"})
        code, open_ = self.api("GET", "/repos/%s/issues" % self.repo, params={"state": "open", "labels": label, "per_page": 5})
        marker = "<!-- droid-hash:%s -->" % hashlib.sha256(body.encode()).hexdigest()[:16]
        if code == 200 and open_:
            issue = open_[0]
            if marker in (issue.get("body") or ""):
                print("No change for issue #%s" % issue["number"])
                return issue["number"]
            self.api("PATCH", "/repos/%s/issues/%s" % (self.repo, issue["number"]), {"title": title, "body": body + "\n\n" + marker})
            self.api("POST", "/repos/%s/issues/%s/comments" % (self.repo, issue["number"]),
                     {"body": "The droid updated this issue at %s with new findings." % now_ct_str()})
            return issue["number"]
        code, issue = self.api("POST", "/repos/%s/issues" % self.repo, {"title": title, "body": body + "\n\n" + marker, "labels": [label, "droid"]})
        return (issue or {}).get("number")

    def comment(self, number, body):
        if dry_run():
            print("[dry run] would comment on #%s" % number); return
        self.api("POST", "/repos/%s/issues/%s/comments" % (self.repo, number), {"body": redact(body)})

# ---------------------------------------------------------------- proposing changes (draft PRs only)

def _git(*args, check=True):
    return subprocess.run(["git", *args], cwd=ROOT, check=check, capture_output=True, text=True)

def propose_change(branch, title, body, files, label="droid-proposal"):
    """Write `files` ({path: new_text}) on a fresh branch and open a DRAFT pull request.

    Guardrails enforced here, not just promised:
      - protected paths (00-immutable, Cathedral, workflows, droid config) are refused outright;
      - any existing file that is overwritten is first copied to ARCHIVE/droid/<date>/<path> in the same commit (Echo 64);
      - the commit may not delete any file;
      - no new legacy Emergent links and no secrets may be added;
      - the pull request is always a draft and the droid has no merge code.
    """
    for p, text in files.items():
        if is_protected(p):
            raise GuardrailError("Refused to propose a change to protected path: " + p)
        if secret_kinds(text):
            raise GuardrailError("Refused: proposed text for %s looks like it holds a secret." % p)
        old = open(os.path.join(ROOT, p), encoding="utf-8", errors="replace").read() if os.path.exists(os.path.join(ROOT, p)) else ""
        if len(find_legacy(text)) > len(find_legacy(old)) and not is_history(p):   # records may quote old text
            raise GuardrailError("Refused: proposed text for %s adds a legacy Emergent link." % p)
    branch = "droid/" + re.sub(r"[^a-z0-9\-]+", "-", branch.lower()).strip("-")
    if dry_run():
        print("[dry run] would open DRAFT PR '%s' on %s with: %s" % (title, branch, ", ".join(sorted(files))))
        return None
    gh = GitHub()
    code, _ = gh.api("GET", "/repos/%s/branches/%s" % (gh.repo, branch))
    if code == 200:
        print("Branch %s already exists; not opening a second proposal." % branch)
        return None
    _git("config", "user.name", "Next-Xus Maintenance Droid")
    _git("config", "user.email", "keywebco@users.noreply.github.com")
    base = _git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    _git("checkout", "-B", branch)
    try:
        stamp = today()
        for p, text in files.items():
            full = os.path.join(ROOT, p)
            if os.path.exists(full):
                arch = os.path.join(ROOT, "ARCHIVE", "droid", stamp, p)
                os.makedirs(os.path.dirname(arch), exist_ok=True)
                shutil.copy2(full, arch)
            os.makedirs(os.path.dirname(full) or ROOT, exist_ok=True)
            with open(full, "w", encoding="utf-8") as f:
                f.write(redact(text))
        _git("add", "-A", "--", *files.keys(), "ARCHIVE") if os.path.isdir(os.path.join(ROOT, "ARCHIVE")) else _git("add", "-A", "--", *files.keys())
        staged = _git("diff", "--cached", "--name-status").stdout.splitlines()
        if any(line.startswith("D") for line in staged):
            raise GuardrailError("Refused: the commit would delete a file (Echo 64).")
        if any(is_protected(line.split("\t")[-1]) for line in staged):
            raise GuardrailError("Refused: the commit touches a protected path.")
        if not staged:
            print("Nothing changed; no proposal."); return None
        _git("commit", "-m", "Droid proposal: " + title)
        _git("push", "origin", branch)
        note = ("\n\n---\n**Draft from the Next-Xus Maintenance Droid.** Nothing is live. "
                "Any file this changes was first copied to `ARCHIVE/droid/%s/` (Echo 64). "
                "The droid never merges; Roger or the Senate decides." % stamp)
        code, pr = gh.api("POST", "/repos/%s/pulls" % gh.repo, {"title": title, "head": branch, "base": base,
                                                                "body": redact(body + note), "draft": True})
        if pr and pr.get("number"):
            gh.api("POST", "/repos/%s/issues/%s/labels" % (gh.repo, pr["number"]), {"labels": [label, "droid"]})
        return (pr or {}).get("html_url")
    finally:
        _git("checkout", base, check=False)

# ---------------------------------------------------------------- output

def write_out(name, markdown, data=None):
    os.makedirs(OUT, exist_ok=True)
    md = redact(markdown)
    with open(os.path.join(OUT, name + ".md"), "w", encoding="utf-8") as f:
        f.write(md)
    if data is not None:
        with open(os.path.join(OUT, name + ".json"), "w", encoding="utf-8") as f:
            f.write(redact(json.dumps(data, indent=1, default=str)))
    summ = os.environ.get("GITHUB_STEP_SUMMARY")
    if summ:
        with open(summ, "a", encoding="utf-8") as f:
            f.write(md + "\n\n")
    print(md)

def read_out(name):
    try:
        return json.load(open(os.path.join(OUT, name + ".json"), encoding="utf-8"))
    except Exception:
        return None

def repo_files(exts=None, include_protected=True):
    """Tracked files in the brain repo (git ls-files), optionally filtered by extension."""
    try:
        files = _git("ls-files").stdout.splitlines()
    except Exception:
        files = []
        for d, _, fs in os.walk(ROOT):
            if "/.git" in d or "/DROID/out" in d:
                continue
            files += [os.path.relpath(os.path.join(d, f), ROOT) for f in fs]
    if exts:
        files = [f for f in files if os.path.splitext(f)[1].lower() in exts]
    if not include_protected:
        files = [f for f in files if not is_protected(f)]
    return files

def read(path):
    return open(os.path.join(ROOT, path), encoding="utf-8", errors="replace").read()
