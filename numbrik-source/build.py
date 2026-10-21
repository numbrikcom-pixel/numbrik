import json, os, shutil, html, re
from content import T, ORDER, BYID
import content2
from more import MORE

DOMAIN = "https://numbrik.com"
TODAY = "2026-10-21"; TODAY_TXT = "October 21, 2026"
OUT = "dist"
E = html.escape
V = "2"  # asset version for cache busting

LOGO = '<svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="var(--accent)"/><rect x="5" y="5" width="22" height="22" rx="4" fill="none" stroke="var(--accent-ink)" stroke-opacity=".28" stroke-width="1.5"/><path d="M9.5 23V9h3l7 9.2V9h3v14h-3l-7-9.2V23z" fill="var(--accent-ink)"/></svg>'
FAVICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="8" fill="#2340C9"/><rect x="5" y="5" width="22" height="22" rx="4" fill="none" stroke="#fff" stroke-opacity=".28" stroke-width="1.5"/><path d="M9.5 23V9h3l7 9.2V9h3v14h-3l-7-9.2V23z" fill="#fff"/></svg>'

def head(title, desc, path, extra_ld=None, noindex=False):
    url = DOMAIN + path
    ld = f'<script type="application/ld+json">{json.dumps(extra_ld, ensure_ascii=False)}</script>' if extra_ld else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
{'<meta name="robots" content="noindex">' if noindex else f'<link rel="canonical" href="{url}">'}
<meta name="theme-color" content="#2340C9">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Numbrik">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="/assets/fonts/plex-sans-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/bricolage-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/style.css?v={V}">
<script>try{{var t=JSON.parse(localStorage.getItem('nb_theme'));if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script>
<!-- Google AdSense: paste the AdSense <script> tag here after approval -->
<!-- Google Analytics: paste the gtag.js snippet here -->
{ld}
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<header class="bar">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Numbrik home">{LOGO}<b>Numbrik</b></a>
    <div class="search" role="search">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
      <input id="q" type="search" placeholder="Search calculators: overtime, GPA, mortgage…" aria-label="Search calculators" autocomplete="off">
      <div class="qres" id="qres" hidden></div>
    </div>
    <label class="region">Region
      <select id="region" aria-label="Region">
        <option value="US">United States</option>
        <option value="CA">Canada</option>
        <option value="AU">Australia</option>
        <option value="UK">United Kingdom</option>
        <option value="NL">Netherlands</option>
      </select>
    </label>
    <button type="button" class="theme" id="themeBtn" aria-label="Switch between light and dark mode">
      <svg class="sun" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
      <svg class="moon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
      <span id="themeLabel">Light</span>
    </button>
  </div>
</header>
"""

def footer():
    cols = ""
    for cat in ORDER:
        items = "".join(f'<li><a href="/{t["slug"]}/">{E(t["name"])}</a></li>' for t in T if t["cat"] == cat)
        cols += f"<div><h4>{E(cat)}</h4><ul>{items}</ul></div>"
    return f"""<footer>
  <div class="wrap">
    {cols}
    <div><h4>Numbrik</h4><ul><li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li><li><a href="/privacy-policy/">Privacy policy</a></li><li><a href="/terms/">Terms of use</a></li></ul></div>
    <p class="legal">© 2026 Numbrik. Results are estimates for planning and are not financial, medical or legal advice.</p>
  </div>
</footer>
<script src="/assets/app.js?v={V}" defer></script>
</body>
</html>
"""

def card(t):
    return f'<a class="card" href="/{t["slug"]}/"><small>{E(t["cat"])}</small><b>{E(t["name"])}</b><span>{E(t["desc"])}</span></a>'

def rail(cur):
    out = '<aside class="rail" aria-label="All calculators"><p>All calculators</p>'
    for cat in ORDER:
        items = "".join('<li><a href="/%s/"%s>%s</a></li>' % (t["slug"], ' aria-current="page"' if t["id"] == cur else "", E(t["short"])) for t in T if t["cat"] == cat)
        out += f'<div class="group"><h3>{E(cat)}</h3><ul>{items}</ul></div>'
    return out + "</aside>"

def write(path, s):
    full = os.path.join(OUT, path.strip("/"), "index.html") if not path.endswith((".xml", ".txt", ".html")) else os.path.join(OUT, path.strip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(s)

def strip_tags(s): return re.sub(r"<[^>]+>", "", s)

# ---------------- tool pages ----------------
for t in T:
    path = f"/{t['slug']}/"
    url = DOMAIN + path
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebApplication", "name": t["name"], "url": url, "description": t["meta"],
         "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
            {"@type": "ListItem", "position": 2, "name": t["name"], "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faqs"]]}]}
    steps = "".join(f"<li>{E(s)}</li>" for s in t["steps"])
    faqs = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in t["faqs"])
    related = "".join(card(BYID[r]) for r in t["related"])
    page = head(t["title"], t["meta"], path, ld) + f"""
<nav class="wrap crumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li><li>{E(t["cat"])}</li><li aria-current="page">{E(t["name"])}</li></ol></nav>
<div class="wrap main">
  <main class="content" id="content">
    <h1>{E(t["name"])}</h1>
    <p class="lede">{E(t["lede"])}</p>
    <div class="panel"><div class="panel-body" id="toolBody" data-tool="{t["id"]}"><p class="loading">Loading calculator…</p><noscript><p class="loading">Turn on JavaScript to use this calculator.</p></noscript></div></div>
    <!-- Ad slot: below calculator -->
    <article class="prose">
      <h2>How to use the {E(t["name"])}</h2>
      <ol>{steps}</ol>
      <h2>How it works</h2>
      {t["how"]}
      <h3>Formula</h3>
      <pre class="formula">{E(t["formula"])}</pre>
      <h2>Example</h2>
      {t["example"]}
      {t["extra"]}
      {MORE.get(t["id"], "")}
      <!-- Ad slot: in article -->
      <h2>Frequently asked questions</h2>
      <div class="faq">{faqs}</div>
      <p class="updated">Last reviewed {TODAY_TXT}. Spotted an error? <a href="/contact/">Tell us</a>.</p>
    </article>
    <section class="related" aria-label="Related calculators"><h2>Related calculators</h2><div class="cards">{related}</div></section>
  </main>
  {rail(t["id"])}
</div>
""" + footer()
    write(path, page)

# ---------------- home ----------------
home_ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebSite", "name": "Numbrik", "url": DOMAIN + "/"},
    {"@type": "Organization", "name": "Numbrik", "url": DOMAIN + "/", "logo": DOMAIN + "/apple-touch-icon.png"}]}
cats = ""
for cat in ORDER:
    cats += f'<section><h2>{E(cat)}</h2><div class="cards">{"".join(card(t) for t in T if t["cat"] == cat)}</div></section>'
pop = "".join(f'<a href="/{BYID[i]["slug"]}/">{E(BYID[i]["short"])}</a>' for i in ["timecard", "gpa", "loan", "calorie", "hours", "age"])
home = head("Numbrik – Free Online Calculators for Work, Money & Health",
            "Fast, free calculators for everyday life: time card and overtime, hourly to salary, mortgage, GPA, BMI, calories, dates and unit conversions.", "/", home_ld) + f"""
<main id="content">
  <section class="wrap hero">
    <h1>Free calculators that answer as you type</h1>
    <p class="lede">Hours and pay, loans, grades, health and everyday conversions. Results update live, units and currency follow your region, and nothing you enter leaves your browser.</p>
    <div class="pop"><span>Popular:</span>{pop}</div>
  </section>
  <div class="wrap home-cats">{cats}</div>
  <section class="wrap why" aria-label="Why Numbrik">
    <div><h3>Live results</h3><p>No Calculate button. Change a number and the answer updates straight away.</p></div>
    <div><h3>Made for your region</h3><p>Choose the United States, Canada, Australia, the UK or the Netherlands to set currency, units and overtime defaults.</p></div>
    <div><h3>Private by design</h3><p>Calculations run on your device. Saved entries, like your time card or GPA courses, stay in your own browser.</p></div>
  </section>
</main>
""" + footer()
write("/", home)

# ---------------- static pages ----------------
def simple(path, title, desc, h1, body, noindex=False):
    write(path, head(title, desc, path, noindex=noindex) + f'<main id="content" class="wrap page"><h1>{E(h1)}</h1>{body}</main>' + footer())

simple("/about/", "About Numbrik", "Numbrik builds fast, free and accurate calculators for everyday work, money, health and school questions.", "About Numbrik", f"""
<p class="lede">Numbrik is an independent website that makes free calculators for the questions people run into every day: how many hours they worked, what a loan will cost, what their GPA is, or how many millilitres are in a cup.</p>
<h2>What we care about</h2>
<ul><li><strong>Accuracy.</strong> Every calculator shows its formula and a worked example, so you can check the answer yourself.</li>
<li><strong>Speed.</strong> Pages are small and results update as you type, on phones as well as computers.</li>
<li><strong>Local defaults.</strong> Currency, units and overtime rules follow the region you choose: the United States, Canada, Australia, the United Kingdom or the Netherlands.</li>
<li><strong>Privacy.</strong> Calculations happen in your browser. We don't ask you to sign up.</li></ul>
<h2>Sources and methods</h2>
<p>Our calculators use standard, published methods. Examples include the US Fair Labor Standards Act overtime rule for the time card, the World Health Organization adult categories for BMI, the Mifflin-St Jeor equation for calorie needs, and the standard amortization formula for loans. Each page explains the method it uses and its limits.</p>
<h2>Corrections</h2>
<p>If you find a mistake or a rule that has changed in your country, please <a href="/contact/">contact us</a>. We review every report and update the page.</p>
<p class="updated">Last updated {TODAY_TXT}.</p>""")

simple("/contact/", "Contact Numbrik", "Contact Numbrik to report an error, suggest a calculator or ask a question.", "Contact us", f"""
<p class="lede">Found an error, want a new calculator, or have a question about the site? Email us and we'll reply as soon as we can.</p>
<p class="copyline"><code id="mail">hello@numbrik.com</code><button class="btn" type="button" onclick="var b=this;navigator.clipboard&&navigator.clipboard.writeText('hello@numbrik.com').then(function(){{b.textContent='Copied'}})">Copy email</button></p>
<h2>When reporting an error</h2>
<ul><li>The page address, for example numbrik.com/gpa-calculator/</li><li>The numbers you entered</li><li>The result you expected and where the rule comes from</li></ul>
<p>We don't give personal financial, medical or legal advice by email. For decisions about your own situation, please speak to a qualified professional.</p>""")

simple("/privacy-policy/", "Privacy Policy | Numbrik", "How Numbrik handles data, cookies, analytics and advertising.", "Privacy policy", f"""
<p class="updated">Effective {TODAY_TXT}</p>
<p>This policy explains what information Numbrik ("we", "us") collects when you use numbrik.com, and how it is used.</p>
<h2>Information you enter in calculators</h2>
<p>Calculations run in your web browser. The numbers you type are not sent to our servers. Some calculators, such as the time card and GPA calculator, save your entries and settings (region and light or dark mode) in your browser's local storage so they are there when you come back. You can delete this data at any time by clearing your browser's site data for numbrik.com.</p>
<h2>Analytics</h2>
<p>We may use Google Analytics to understand how many people visit, which pages they use and how they found the site. Google Analytics uses cookies and collects information such as your device type, browser, approximate location and pages viewed. We use this only in aggregate to improve the site. You can opt out with the <a href="https://tools.google.com/dlpage/gaoptout" rel="noopener">Google Analytics opt-out browser add-on</a>.</p>
<h2>Advertising</h2>
<p>We may show ads served by Google AdSense. Third-party vendors, including Google, use cookies to serve ads based on your previous visits to this and other websites. Google's use of advertising cookies enables it and its partners to serve ads based on your visits to this site and other sites on the internet. You can opt out of personalised advertising in <a href="https://adssettings.google.com" rel="noopener">Google Ads Settings</a>, and learn more at <a href="https://policies.google.com/technologies/partner-sites" rel="noopener">How Google uses information from sites that use its services</a>. You can also opt out of some third-party vendors' use of cookies at <a href="https://www.aboutads.info/choices/" rel="noopener">aboutads.info</a>.</p>
<h2>Visitors in the UK, EEA and Switzerland</h2>
<p>Where required, we ask for your consent before setting non-essential cookies, through a consent message shown on your first visit. You can change your choice at any time. Under the UK GDPR and EU GDPR you have the right to access, correct or delete personal data we hold about you, to object to processing and to complain to your local data protection authority.</p>
<h2>Visitors in the United States</h2>
<p>We do not sell personal information. Residents of states with privacy laws, such as California, may request access to or deletion of personal information by contacting us.</p>
<h2>Children</h2>
<p>Numbrik is a general-audience site and is not directed at children under 13. We do not knowingly collect personal information from children.</p>
<h2>Server logs</h2>
<p>Our hosting provider may keep standard server logs, such as IP address, browser type and the time of a request, for security and to keep the site running.</p>
<h2>Changes and contact</h2>
<p>We may update this policy and will change the date above when we do. Questions: <strong>hello@numbrik.com</strong>.</p>""")

simple("/terms/", "Terms of Use | Numbrik", "The terms for using Numbrik calculators.", "Terms of use", f"""
<p class="updated">Effective {TODAY_TXT}</p>
<p>By using numbrik.com you agree to these terms.</p>
<h2>Estimates, not advice</h2>
<p>Numbrik calculators give estimates for general information and planning. They are not financial, tax, medical, legal or professional advice. Rules such as overtime law, tax rates and lending terms vary by location and change over time. Check important results with a qualified professional or the official source before relying on them.</p>
<h2>No warranty</h2>
<p>We work to keep our calculators accurate, but the site is provided "as is" without warranties of any kind. We don't guarantee that results are complete, current or free of errors.</p>
<h2>Limitation of liability</h2>
<p>To the extent allowed by law, Numbrik is not liable for any loss or damage arising from your use of the site or reliance on its results.</p>
<h2>Acceptable use</h2>
<p>You may use the calculators for personal and business purposes. Don't copy the site in bulk, interfere with its operation, or use automated tools to overload it.</p>
<h2>Links</h2>
<p>We may link to other websites. We aren't responsible for their content or practices.</p>
<h2>Changes</h2>
<p>We may update these terms and will change the date above when we do. Questions: <strong>hello@numbrik.com</strong>.</p>""")

# 404
write("/404.html", head("Page not found | Numbrik", "This page doesn't exist.", "/404.html", noindex=True) + f"""
<main id="content" class="wrap page"><h1>We couldn't find that page</h1><p class="lede">The address may be mistyped, or the page may have moved. Try the search at the top, or pick a popular calculator:</p>
<div class="cards">{"".join(card(BYID[i]) for i in ["timecard","gpa","loan","calorie"])}</div><p><a href="/">Go to the homepage</a></p></main>""" + footer())

# sitemap & robots & headers
urls = ["/"] + [f"/{t['slug']}/" for t in T] + ["/about/", "/contact/", "/privacy-policy/", "/terms/"]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{DOMAIN}{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n"
write("/sitemap.xml", sm)
write("/robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
open(os.path.join(OUT, "_headers"), "w").write("""/assets/*
  Cache-Control: public, max-age=31536000, immutable
/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN
""")
open(os.path.join(OUT, "favicon.svg"), "w").write(FAVICON)

# assets
os.makedirs(os.path.join(OUT, "assets/fonts"), exist_ok=True)
shutil.copy("src/style.css", os.path.join(OUT, "assets/style.css"))
shutil.copy("src/app.js", os.path.join(OUT, "assets/app.js"))
F = "fontsrc/node_modules/@fontsource/"
for src, dst in [("bricolage-grotesque/files/bricolage-grotesque-latin-500-normal.woff2", "bricolage-500"),
                 ("bricolage-grotesque/files/bricolage-grotesque-latin-700-normal.woff2", "bricolage-700"),
                 ("ibm-plex-sans/files/ibm-plex-sans-latin-400-normal.woff2", "plex-sans-400"),
                 ("ibm-plex-sans/files/ibm-plex-sans-latin-500-normal.woff2", "plex-sans-500"),
                 ("ibm-plex-sans/files/ibm-plex-sans-latin-600-normal.woff2", "plex-sans-600"),
                 ("ibm-plex-mono/files/ibm-plex-mono-latin-500-normal.woff2", "plex-mono-500")]:
    shutil.copy(F + src, os.path.join(OUT, f"assets/fonts/{dst}.woff2"))
print("built", len(urls), "pages")

# Google Search Console verification file
open(os.path.join(OUT, "google3ac709f348cc4545.html"), "w").write("google-site-verification: google3ac709f348cc4545.html")
