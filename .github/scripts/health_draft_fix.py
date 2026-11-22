"""Health-check draft fix (EE-2026-11-20-002). Review branch only. Never merges. No AI model.

What it does, and nothing more:
  1. `plan`  reads LATTICE/reports/health.md and keeps only "missing:" problems on the allowed sites
     listed in ALLOWED below. A missing phrase is kept only if it is the exact title of a LIVE product in
     04-builds/products.yaml (Gumroad is the truth). Anything else is left for a person.
  2. `apply` adds those titles, with their exact Gumroad link and price, inside one marked block on the
     site's page. It only inserts. If the page would get shorter, or anything outside the block would
     change, it refuses.
The workflow then saves the change to a review branch and comments on the open health-check issue.
Roger says the merge word. Nothing goes live from here."""
import html, json, os, re, sys

import yaml  # installed by the workflow (pip install pyyaml)

# Allowed sites: health-check URL -> (repo, file to edit). Start with the Portal only.
ALLOWED = {
    "https://keywebco.github.io/": ("keywebco.github.io", "index.html"),
}
START = "<!-- nx-health-draft-fix:start (EE-002; edit by review branch only) -->"
END = "<!-- nx-health-draft-fix:end -->"
TMP = os.environ.get("RUNNER_TEMP", "/tmp")
PLAN = os.path.join(TMP, "draft_fix_plan.json")


def fail(msg):
    print("REFUSED:", msg)
    sys.exit(1)


def out(k, v):
    f = os.environ.get("GITHUB_OUTPUT")
    if f:
        with open(f, "a") as h:
            h.write("%s=%s\n" % (k, v))


def live_products(path):
    rows = yaml.safe_load(open(path, encoding="utf-8")) or []
    return {r["title"]: r for r in rows if isinstance(r, dict) and r.get("status") == "live"
            and str(r.get("url", "")).startswith("https://keywebster.gumroad.com/l/")}


def plan(report="LATTICE/reports/health.md", products="04-builds/products.yaml"):
    text = open(report, encoding="utf-8").read()
    probs = (text.split("## Problems")[1] if "## Problems" in text else "").split("## All checks")[0]
    live = live_products(products)
    todo, skipped = {}, []
    for line in probs.splitlines():
        m = re.match(r"- \*\*(.+?)\*\* \((\S+)\): (.*)$", line.strip())
        if not m:
            continue
        name, url, rest = m.groups()
        for p in [x.strip() for x in rest.split(";")]:
            if not p.startswith("missing: "):
                skipped.append("%s: %s (not a missing phrase)" % (name, p))
                continue
            phrase = p[len("missing: "):]
            if url not in ALLOWED:
                skipped.append("%s: %s (site not on the allowed list)" % (name, phrase))
            elif phrase not in live:
                skipped.append("%s: %s (not an exact live product title)" % (name, phrase))
            else:
                repo, fname = ALLOWED[url]
                todo.setdefault(repo, {"file": fname, "items": []})["items"].append(live[phrase])
    json.dump({"todo": todo, "skipped": skipped}, open(PLAN, "w"), indent=1)
    print(json.dumps({"todo": {k: [i["title"] for i in v["items"]] for k, v in todo.items()}, "skipped": skipped}, indent=1))
    repos = sorted(todo)
    if len(repos) > 1:
        fail("more than one repo in one run; this first version handles one at a time")
    out("repo", repos[0] if repos else "")


def block_for(items):
    lis = []
    for r in items:
        price = re.sub(r"\.00 USD$", "", str(r.get("price", ""))).replace(" USD", "")
        lis.append('<li><a href="%s">%s</a>%s</li>' % (html.escape(r["url"], quote=True), html.escape(r["title"], quote=False),
                                                         (' <span class="lp">%s</span>' % html.escape(price)) if price else ""))
    return "\n".join([START, '<div class="card">', "<h2>Books on Gumroad</h2>",
                      '<p>Roger Keyserling\'s books. Gumroad is the store; this page only links to it. <a href="store.html">See all books</a>.</p>',
                      "<ul>"] + lis + ["</ul>", "</div>", END])


def apply(target="target"):
    p = json.load(open(PLAN))
    if not p["todo"]:
        print("Nothing to draft.")
        return
    repo, job = next(iter(p["todo"].items()))
    path = os.path.join(target, job["file"])
    old = open(path, encoding="utf-8").read()
    items = list(job["items"])
    if START in old and END in old:
        a, rest = old.split(START, 1)
        inner, b = rest.split(END, 1)
        have = set(re.findall(r'<a href="([^"]+)">', inner))
        keep = [x for x in re.findall(r"<li>.*?</li>", inner)]
        add = [r for r in items if html.escape(r["url"], quote=True) not in have]
        if not add:
            print("Already drafted; nothing new.")
            return
        new_inner = block_for(add)
        # keep the existing rows, insert new ones before </ul>
        lis = "\n".join(keep + [l for l in new_inner.split("\n") if l.startswith("<li>")])
        new = a + block_for([]).replace("<ul>", "<ul>\n" + lis) + b
    else:
        blk = block_for(items)
        anchor = "</section>\n</main>"
        if anchor in old:
            new = old.replace(anchor, blk + "\n" + anchor, 1)
        elif "</main>" in old:
            new = old.replace("</main>", blk + "\n</main>", 1)
        elif "</body>" in old:
            new = old.replace("</body>", blk + "\n</body>", 1)
        else:
            fail("no place to insert the block")
    # Insert-only guard: everything that was there before must still be there, in order.
    if len(new) <= len(old):
        fail("the page would not grow; refusing")
    oi = 0
    for ch in new:
        if oi < len(old) and ch == old[oi]:
            oi += 1
    if oi != len(old):
        fail("the change would alter existing text; refusing")
    open(path, "w", encoding="utf-8").write(new)
    with open(os.path.join(TMP, "draft_fix_summary.txt"), "w") as h:
        h.write("Added to %s/%s: %s" % (repo, job["file"], "; ".join(r["title"] for r in items)))
    print("Drafted", repo, job["file"])


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "plan":
        plan()
    elif cmd == "apply":
        apply(sys.argv[2] if len(sys.argv) > 2 else "target")
    else:
        fail("use: plan | apply [target_dir]")
