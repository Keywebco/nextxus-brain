"""Command build hub. Two steps: `read` checks the order; `build` asks the model and writes the files.
Safe by design: only allowed repos, only the named files, paths checked, an edit that removes more than
60 percent of an existing file is refused, workflow files are never touched, secrets are never printed.
The summary goes to RUNNER_TEMP, never into the target repo."""
import json, os, re, sys, urllib.request

ALLOWED = ["nextxus-humancodex", "keywebco.github.io", "nextxus-agent-zero", "nextxus-research-hub",
           "nextxus-recycler", "nextxus-archives", "nextxus-senate", "nextxus-chat", "nextxus-tools", "nextxus-blog"]
TMP = os.environ.get("RUNNER_TEMP", "/tmp")
ORDER_FILE = os.path.join(TMP, "order.json")
TARGET = os.environ.get("TARGET_DIR", "target")

def fail(msg):
    print("REFUSED:", msg); sys.exit(1)

def safe(p):
    return (bool(re.fullmatch(r"[A-Za-z0-9._\-/]{1,160}", p)) and not p.startswith("/") and ".." not in p
            and not p.startswith(".git") and not p.startswith(".github"))

def out(k, v):
    f = os.environ.get("GITHUB_OUTPUT")
    if f:
        with open(f, "a") as h: h.write("%s=%s\n" % (k, v))

def read():
    ev = os.environ.get("EVENT_NAME", "")
    if ev == "workflow_dispatch":
        data = json.loads(os.environ.get("INPUTS_JSON") or "{}")
    elif ev == "push":
        try: data = json.load(open("hub/.orders/order.json", encoding="utf-8"))
        except Exception: fail("no readable .orders/order.json on the order branch")
    else:
        fail("unsupported trigger: " + ev)
    repo = str(data.get("repo", "")).strip()
    order = str(data.get("order", "")).strip()
    files = data.get("files", [])
    if isinstance(files, str): files = [f.strip() for f in files.split(",") if f.strip()]
    who = re.sub(r"[^a-z0-9\-]", "", str(data.get("who") or os.environ.get("ACTOR", "unknown")).lower())[:30] or "unknown"
    if repo not in ALLOWED: fail("that site is not on the allowed list")
    if len(order) < 5 or len(order) > 4000: fail("the order is empty or too long")
    if not files or len(files) > 8: fail("name between 1 and 8 files")
    for f in files:
        if not safe(f): fail("unsafe path: " + f)
    json.dump({"repo": repo, "order": order, "files": files, "who": who}, open(ORDER_FILE, "w", encoding="utf-8"))
    out("repo", repo); out("who", who)
    print("Order accepted for", repo, "by", who, "files:", ", ".join(files))

def build():
    key = os.environ.get("MIMO_API_KEY", "")
    if not key: fail("no model key is set")
    o = json.load(open(ORDER_FILE, encoding="utf-8"))
    order, files = o["order"], o["files"]
    base = os.environ.get("LLM_BASE", "https://api.xiaomimimo.com")
    model = os.environ.get("BUILD_MODEL", "mimo-v2.6-pro")
    root = os.path.realpath(TARGET)
    def full(p):
        q = os.path.realpath(os.path.join(root, p))
        if not q.startswith(root + os.sep): fail("path escapes the repo: " + p)
        return q
    current = {}
    for f in files:
        q = full(f)
        current[f] = open(q, encoding="utf-8").read() if os.path.exists(q) else None
    system = ('You write website files. Plain HTML, CSS and vanilla JS only, readable without JavaScript. '
              'Make ONLY the change that was ordered; keep everything else exactly as it is. '
              'Reply with ONLY a JSON object: {"files":[{"path":"...","content":"FULL new file content"}],"summary":"one plain sentence"}. '
              'Only paths from the allowed list. Never output secrets.')
    user = "ORDER:\n" + order + "\n\nALLOWED PATHS:\n" + "\n".join(files) + "\n\nCURRENT FILES:\n" + "\n\n".join(
        "=== %s%s ===\n%s" % (f, " (NEW FILE)" if c is None else "", c or "") for f, c in current.items())
    body = json.dumps({"model": model, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
                       "max_tokens": 12000, "temperature": 0.2}).encode()
    req = urllib.request.Request(base + "/v1/chat/completions", data=body,
                                 headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    try: reply = json.load(urllib.request.urlopen(req, timeout=240))["choices"][0]["message"]["content"]
    except Exception as e: fail("the model call failed: " + type(e).__name__)
    m = re.search(r"\{[\s\S]*\}", reply)
    if not m: fail("the model returned no JSON")
    try: res = json.loads(m.group(0))
    except Exception: fail("the model returned broken JSON")
    edits = [e for e in res.get("files", []) if isinstance(e, dict) and e.get("path") in files
             and isinstance(e.get("content"), str) and 0 < len(e["content"]) < 600000]
    if not edits: fail("the model returned nothing usable")
    for e in edits:
        old = current.get(e["path"])
        if old and len(e["content"]) < len(old) * 0.4: fail("the model tried to remove most of " + e["path"])
    for e in edits:
        q = full(e["path"]); os.makedirs(os.path.dirname(q), exist_ok=True)
        open(q, "w", encoding="utf-8").write(e["content"])
        print("wrote", e["path"], len(e["content"]), "bytes")
    open(os.path.join(TMP, "build_summary.txt"), "w", encoding="utf-8").write(str(res.get("summary", ""))[:300])

if __name__ == "__main__":
    {"read": read, "build": build}.get(sys.argv[1] if len(sys.argv) > 1 else "", lambda: fail("use: read | build"))()
