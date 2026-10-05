#!/usr/bin/env python3
"""Nova-Canon: daily guard for the NextXus brain. Free (GitHub Actions). Reports; never edits canon.
1) Verifies the sealed immutable files against 00-immutable/SEAL.yaml (sha256 of file bytes).
2) Verifies framework/DIRECTIVES/directives.yaml equals the sealed canon.
3) Checks directive count (gate DIR-000 + DIR-001..073).
4) Scans live Federation site homepages for stale patterns (read-only GET).
Writes LATTICE/reports/latest.md. Exit code 1 if the seal or canon fails."""
import hashlib, re, sys, datetime, urllib.request, yaml, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def rd(p): return open(os.path.join(ROOT, p), 'rb').read()
fails, notes = [], []

seal = yaml.safe_load(rd('00-immutable/SEAL.yaml'))
for f in seal['files']:
    h = hashlib.sha256(rd(f['path'])).hexdigest()
    if h == f['sha256']: notes.append(f"PASS seal {f['path']}")
    else: fails.append(f"FAIL seal {f['path']}: expected {f['sha256'][:12]} got {h[:12]}")

canon_sha = [f for f in seal['files'] if f['path'].endswith('directives.yaml')][0]['sha256']
if hashlib.sha256(rd('framework/DIRECTIVES/directives.yaml')).hexdigest() == canon_sha:
    notes.append("PASS framework/DIRECTIVES mirrors sealed canon")
else:
    fails.append("FAIL framework/DIRECTIVES/directives.yaml differs from sealed canon")

d = yaml.safe_load(rd('00-immutable/directives.yaml'))
ids = [x['id'] for x in d['directives']]
want = [f'DIR-{n:03d}' for n in range(1, 74)]
if d['gate']['id'] == 'DIR-000' and ids == want: notes.append("PASS 1 gate + 73 directives, DIR-001..073 in order")
else: fails.append("FAIL directive ids are not DIR-000 + DIR-001..073")

STALE = {
  '70 directives': r'\b70\s+(?:sacred\s+)?directives',
  '84 directives': r'\b84\s+(?:sacred\s+)?directives',
  'replit.app': r'replit\.app',
  'dead email': r'keyhole@nextxus\.net',
  'retired .one': r'nextxus\.one\b',
  'retired .rip': r'nextxus\.rip\b',
}
SITES = ['https://nextxus.online/','https://nextxus.tech/','https://nextxus.studio/','https://nextxus.org/',
         'https://nextxus.space/','https://nextxus.help/','https://next-xus.com/','https://keywebco.github.io/']
scan = []
for u in SITES:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Nova-Canon/1.0'})
        r = urllib.request.urlopen(req, timeout=25); body = r.read().decode('utf8', 'ignore'); code = r.status
    except Exception as e:
        scan.append((u, 'ERR', str(e)[:60], {})); continue
    hits = {k: len(re.findall(p, body, re.I)) for k, p in STALE.items()}
    scan.append((u, code, '', {k: v for k, v in hits.items() if v}))

now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
out = [f"# Nova-Canon report ({now})", "", "Status: " + ("**FAIL**" if fails else "PASS"), "",
       "## Canon checks"] + [f"- {x}" for x in fails + notes] + ["", "## Live homepage scan (read-only; homepages only, not whole sites)",
       "| Site | HTTP | Stale patterns found |", "|---|---|---|"]
for u, c, e, h in scan:
    out.append(f"| {u} | {c} | {', '.join(f'{k} x{v}' for k, v in h.items()) or ('error: ' + e if e else 'none')} |")
out += ["", "Nova-Canon reports only. It never edits canon or live sites. Findings go to Roger."]
os.makedirs(os.path.join(ROOT, 'LATTICE/reports'), exist_ok=True)
open(os.path.join(ROOT, 'LATTICE/reports/latest.md'), 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))
sys.exit(1 if fails else 0)
