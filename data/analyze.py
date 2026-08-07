import json, re, collections
from urllib.parse import urlparse
p = json.load(open("crawl.json"))

def is_es(u): return "/ES/" in u or u.rstrip("/").endswith("/ES")

en = {u: r for u, r in p.items() if not is_es(u)}
es = {u: r for u, r in p.items() if is_es(u)}
print(f"TOTAL {len(p)} | EN {len(en)} | ES {len(es)}\n")

print("=== STATUS CODES ===")
for lang, d in (("EN", en), ("ES", es)):
    c = collections.Counter(r["status"] for r in d.values())
    print(f"  {lang}: {dict(c)}")

print("\n=== 404 / ERRORES ===")
bad = {u: r for u, r in p.items() if r["status"] not in (200, 301, 302)}
for u, r in sorted(bad.items()):
    print(f"  {r['status']}  {u}")
if not bad: print("  (ninguno)")

print("\n=== REDIRECCIONES (301/302) ===")
for u, r in sorted(p.items()):
    if r["status"] in (301, 302) or r.get("redirected"):
        if r.get("final") and r["final"].rstrip("/") != u.rstrip("/"):
            print(f"  {u}\n      -> {r['final']}")

# inbound links to broken targets
print("\n=== ENLACES ROTOS: quien apunta a que ===")
inbound = collections.defaultdict(set)
for u, r in p.items():
    for l in r.get("links", []):
        inbound[l.rstrip("/")].add(u)
for u, r in sorted(bad.items()):
    src = inbound.get(u.rstrip("/"), set())
    print(f"  [{r['status']}] {u}  <- {len(src)} paginas")
    for s in sorted(src)[:6]: print(f"        {s}")

print("\n=== TITLES: faltantes / duplicados / longitud ===")
titles = collections.defaultdict(list)
for u, r in p.items():
    if r["status"] != 200 or "title" not in r: continue
    titles[(r.get("title") or "").strip()].append(u)
for t, us in sorted(titles.items(), key=lambda x: -len(x[1])):
    if len(us) > 1:
        print(f"  DUP x{len(us)}: {t[:90]!r}")
        for u in us[:8]: print(f"        {u}")
print("  -- longitud fuera de rango (>60 o <30) --")
for u, r in sorted(p.items()):
    t = r.get("title")
    if r["status"] == 200 and t and (len(t) > 60 or len(t) < 30):
        print(f"    {len(t):3d}  {u}\n         {t[:110]}")

print("\n=== META DESCRIPTION faltante o mala ===")
for u, r in sorted(p.items()):
    if r["status"] != 200 or "title" not in r: continue
    md = r.get("meta_desc")
    if not md:
        print(f"  FALTA        {u}")
    elif len(md) > 160 or len(md) < 70:
        print(f"  LEN {len(md):3d}      {u}")

print("\n=== H1: faltante o multiple ===")
for u, r in sorted(p.items()):
    if r["status"] != 200 or "h1" not in r: continue
    h = r.get("h1") or []
    if len(h) == 0: print(f"  SIN H1       {u}")
    elif len(h) > 1: print(f"  {len(h)} H1s       {u}  | {[x[:40] for x in h]}")

print("\n=== HREFLANG ===")
nohl = [u for u, r in p.items() if r["status"] == 200 and "title" in r and not r.get("hreflang")]
print(f"  Paginas SIN hreflang: {len(nohl)} de {len([1 for r in p.values() if r['status']==200 and 'title' in r])}")
for u in sorted(nohl)[:25]: print(f"      {u}")
print("  -- ejemplos CON hreflang --")
n = 0
for u, r in sorted(p.items()):
    if r.get("hreflang") and n < 6:
        print(f"      {u}")
        for hl, href in r["hreflang"]: print(f"           {hl:8s} {href}")
        n += 1

print("\n=== LANG attr ===")
print("  ", dict(collections.Counter((r.get("lang") or "NONE") for r in p.values() if r["status"] == 200 and "title" in r)))
print("  -- ES con lang incorrecto --")
for u, r in sorted(es.items()):
    if r["status"] == 200 and "title" in r and (r.get("lang") or "").lower() not in ("es", "es-es", "es-mx"):
        print(f"      lang={r.get('lang')}  {u}")

print("\n=== CANONICAL problemas ===")
for u, r in sorted(p.items()):
    if r["status"] != 200 or "title" not in r: continue
    c = r.get("canonical")
    if not c: print(f"  SIN CANONICAL  {u}")
    elif c.rstrip("/") != (r.get("final") or u).rstrip("/"):
        print(f"  MISMATCH  {u}\n            canonical -> {c}")

print("\n=== NOINDEX ===")
for u, r in sorted(p.items()):
    if r.get("robots") and "noindex" in r["robots"].lower():
        print(f"  {r['robots'][:40]:40s} {u}")

print("\n=== CONTENIDO THIN (<300 palabras) ===")
for u, r in sorted(p.items(), key=lambda x: x[1].get("words", 9999)):
    if r["status"] == 200 and "words" in r and r["words"] < 300:
        print(f"  {r['words']:5d} palabras  {u}")

print("\n=== IMAGENES SIN ALT ===")
tot = sum(r.get("imgs_no_alt", 0) for r in p.values())
print(f"  Total img sin alt: {tot}")
for u, r in sorted(p.items(), key=lambda x: -x[1].get("imgs_no_alt", 0))[:15]:
    if r.get("imgs_no_alt", 0) > 0:
        print(f"  {r['imgs_no_alt']:3d}/{r.get('imgs_total',0):3d}  {u}")
