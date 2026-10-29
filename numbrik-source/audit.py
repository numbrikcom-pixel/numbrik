import os, re, json, html, collections, sys
D = sys.argv[1] if len(sys.argv) > 1 else "dist"
pages = {}
for root, _, files in os.walk(D):
    for f in files:
        if f == "index.html":
            p = "/" + os.path.relpath(root, D).replace(".", "").strip("/") + "/"
            pages[p.replace("//", "/")] = open(os.path.join(root, f)).read()
sm = set(re.findall(r"<loc>https://numbrik.com(.*?)</loc>", open(f"{D}/sitemap.xml").read()))
issues = collections.defaultdict(list)
titles = collections.defaultdict(list); metas = collections.defaultdict(list); inlinks = collections.Counter()
for p, h in pages.items():
    t = html.unescape(re.search(r"<title>(.*?)</title>", h).group(1))
    m = re.search(r'<meta name="description" content="(.*?)">', h); m = html.unescape(m.group(1)) if m else ""
    titles[t].append(p); metas[m].append(p)
    if len(t) > 60: issues["Title over 60 chars"].append(f"{p} ({len(t)})")
    if len(t) < 25: issues["Title under 25 chars"].append(f"{p} ({len(t)})")
    if len(m) > 160: issues["Meta description over 160 chars"].append(f"{p} ({len(m)})")
    if len(m) < 70: issues["Meta description under 70 chars"].append(f"{p} ({len(m)})")
    h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", h, re.S)
    if len(h1) != 1: issues["Not exactly one H1"].append(f"{p} ({len(h1)})")
    if not re.search(r"<h2", h): issues["No H2"].append(p)
    can = re.search(r'<link rel="canonical" href="(.*?)">', h)
    if p != "/404.html" and (not can or can.group(1) != "https://numbrik.com" + p): issues["Canonical missing/wrong"].append(p)
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try: json.loads(blk)
        except Exception as e: issues["Invalid JSON-LD"].append(p)
    if 'og:image' not in h: issues["No og:image"].append(p)
    main = re.search(r"<main.*?</main>", h, re.S).group(0) if "<main" in h else ""
    words = len(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", "", main, flags=re.S)).split())
    if words < 250 and p not in ("/contact/", "/countdowns/", "/terms/", "/about/"): issues["Thin main content (<250 words)"].append(f"{p} ({words})")
    for a in set(re.findall(r'href="(/[^"#?]*)"', main)):
        if a != p: inlinks[a] += 1
    for a in set(re.findall(r'href="(/[^"#?]*)"', h)):
        target = a if a.endswith("/") or "." in a.split("/")[-1] else a + "/"
        if not target.endswith((".svg", ".png", ".css", ".js", ".xml", ".txt", ".html", ".woff2")) and target not in pages: issues["Broken internal link"].append(f"{p} -> {a}")
    imgs = re.findall(r"<img(?![^>]*alt=)[^>]*>", h)
    if imgs: issues["Image without alt"].append(p)
    if '<html lang="en">' not in h: issues["Missing lang"].append(p)
for t, ps in titles.items():
    if len(ps) > 1: issues["Duplicate title"].append(f"{t} -> {ps}")
for m, ps in metas.items():
    if len(ps) > 1: issues["Duplicate meta description"].append(f"{m[:60]} -> {len(ps)} pages")
for p in pages:
    if p not in ("/",) and p in sm and inlinks[p] == 0: issues["Only linked from menu/footer (no in-content links)"].append(p)
missing = sm - set(pages); extra = set(pages) - sm - {"/404.html"}
if missing: issues["In sitemap but no page"] += sorted(missing)
if extra: issues["Page not in sitemap"] += sorted(extra)
css = os.path.getsize(f"{D}/assets/style.css"); js = os.path.getsize(f"{D}/assets/app.js")
print(f"{len(pages)} pages | CSS {css//1024} KB | JS {js//1024} KB | biggest HTML {max(len(h) for h in pages.values())//1024} KB")
for k, v in sorted(issues.items(), key=lambda x: -len(x[1])):
    print(f"\n## {k}: {len(v)}"); [print("  ", x) for x in v[:12]]; len(v) > 12 and print("   …")
