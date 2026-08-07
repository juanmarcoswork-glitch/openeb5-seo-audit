import re, json, sys, time
from collections import deque
from urllib.parse import urljoin, urlparse, urldefrag
import requests
from concurrent.futures import ThreadPoolExecutor

HOST = "openeb5.com"
UA = {"User-Agent": "Mozilla/5.0 (compatible; OpenEB5-SEO-Audit/1.0)"}
S = requests.Session()
S.headers.update(UA)

SKIP_EXT = re.compile(r"\.(jpg|jpeg|png|gif|webp|svg|ico|css|js|woff2?|ttf|eot|mp4|zip)(\?|$)", re.I)

pages = {}        # url -> {status, title, h1, canonical, meta_desc, robots, hreflang, lang, links}
seen = set()
queue = deque()

SEEDS = ["https://openeb5.com/", "https://openeb5.com/ES/"]
for s in SEEDS:
    queue.append(s); seen.add(s)

# also seed from sitemap
for line in open("all-urls.txt"):
    u = line.strip()
    if u and u not in seen:
        seen.add(u); queue.append(u)

def norm(u):
    u, _ = urldefrag(u)
    return u.rstrip()

def get_meta(html, name=None, prop=None):
    if name:
        m = re.search(r'<meta[^>]*name=["\']%s["\'][^>]*content=["\']([^"\']*)' % name, html, re.I)
        if not m:
            m = re.search(r'<meta[^>]*content=["\']([^"\']*)["\'][^>]*name=["\']%s["\']' % name, html, re.I)
        return m.group(1) if m else None
    return None

def fetch(url):
    try:
        r = S.get(url, timeout=30, allow_redirects=True)
    except Exception as e:
        return {"url": url, "status": "ERR", "error": str(e)[:120], "links": []}
    final = r.url
    rec = {"url": url, "final": final, "status": r.status_code,
           "redirected": final.rstrip('/') != url.rstrip('/'),
           "links": [], "ctype": r.headers.get("content-type", "")}
    if "text/html" not in rec["ctype"]:
        return rec
    html = r.text
    rec["bytes"] = len(html.encode("utf-8"))
    t = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    rec["title"] = re.sub(r"\s+", " ", t.group(1)).strip() if t else None
    h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
    rec["h1"] = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h)).strip() for h in h1s]
    c = re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']*)', html, re.I)
    rec["canonical"] = c.group(1) if c else None
    rec["meta_desc"] = get_meta(html, name="description")
    rec["robots"] = get_meta(html, name="robots")
    rec["hreflang"] = re.findall(r'<link[^>]*rel=["\']alternate["\'][^>]*hreflang=["\']([^"\']*)["\'][^>]*href=["\']([^"\']*)', html, re.I)
    lang = re.search(r'<html[^>]*lang=["\']([^"\']*)', html, re.I)
    rec["lang"] = lang.group(1) if lang else None
    rec["imgs_no_alt"] = len(re.findall(r"<img(?![^>]*\balt=)[^>]*>", html, re.I))
    rec["imgs_total"] = len(re.findall(r"<img", html, re.I))
    rec["h2"] = len(re.findall(r"<h2[^>]*>", html, re.I))
    rec["words"] = len(re.sub(r"<[^>]+>", " ", re.sub(r"(?is)<(script|style|nav|footer)[^>]*>.*?</\1>", " ", html)).split())
    for m in re.finditer(r'href=["\']([^"\']+)', html):
        href = m.group(1)
        if href.startswith(("mailto:", "tel:", "javascript:", "#", "data:")):
            continue
        absu = norm(urljoin(final, href))
        rec["links"].append(absu)
    return rec

MAX = 400
while queue and len(pages) < MAX:
    batch = []
    while queue and len(batch) < 12:
        batch.append(queue.popleft())
    with ThreadPoolExecutor(max_workers=12) as ex:
        for rec in ex.map(fetch, batch):
            pages[rec["url"]] = rec
            for l in rec.get("links", []):
                p = urlparse(l)
                if p.netloc.replace("www.", "") != HOST: continue
                if SKIP_EXT.search(l): continue
                if "/wp-json" in l or "/feed" in l or "?" in l or "/wp-admin" in l: continue
                if l not in seen and len(seen) < MAX:
                    seen.add(l); queue.append(l)
    print(f"crawled={len(pages)} queue={len(queue)}", file=sys.stderr)

json.dump(pages, open("crawl.json", "w"), indent=1)
print("DONE pages:", len(pages))
