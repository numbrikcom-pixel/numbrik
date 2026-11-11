import json, os, shutil, html, re
from content import T, ORDER, BYID
import content2
import content3
import content4
import content5
import content6
import content7
import content8
import content9
import content10
import content11
import content12
import tweaks
import qa
import content13
import content14
import content15
from more import MORE
import extra
import cats
import days

DOMAIN = "https://numbrik.com"
TODAY = "2026-10-31"; TODAY_TXT = "October 31, 2026"
OUT = "dist"
E = html.escape
V = "15"  # asset version for cache busting

LOGO = '<svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="var(--accent)"/><rect x="5" y="5" width="22" height="22" rx="4" fill="none" stroke="var(--accent-ink)" stroke-opacity=".28" stroke-width="1.5"/><path d="M9.5 23V9h3l7 9.2V9h3v14h-3l-7-9.2V23z" fill="var(--accent-ink)"/></svg>'
FAVICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="8" fill="#2340C9"/><rect x="5" y="5" width="22" height="22" rx="4" fill="none" stroke="#fff" stroke-opacity=".28" stroke-width="1.5"/><path d="M9.5 23V9h3l7 9.2V9h3v14h-3l-7-9.2V23z" fill="#fff"/></svg>'

def head(title, desc, path, extra_ld=None, noindex=False):
    url = DOMAIN + path
    if not extra_ld and not noindex:
        extra_ld = {"@context": "https://schema.org", "@type": "WebPage", "name": title, "url": url, "description": desc,
                    "isPartOf": {"@type": "WebSite", "name": "Numbrik", "url": DOMAIN + "/"}}
    ld = f'<script type="application/ld+json">{json.dumps(extra_ld, ensure_ascii=False)}</script>' if extra_ld else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-K5H3XBXGMP"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('consent', 'default', {{ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', analytics_storage: 'denied', region: ['AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR','DE','GR','HU','IS','IE','IT','LV','LI','LT','LU','MT','NL','NO','PL','PT','RO','SK','SI','ES','SE','GB','CH']}});
  gtag('js', new Date());
  gtag('config', 'G-K5H3XBXGMP');
</script>
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
<link rel="preload" href="/assets/fonts/bricolage-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/style.css?v={V}">
<script>try{{var t=JSON.parse(localStorage.getItem('nb_theme'));if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6519470736644184" crossorigin="anonymous"></script>
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
        cols += f"<div>{cats.cat_label(cat, 'h4')}<ul>{items}</ul></div>"
    return f"""<footer>
  <div class="wrap">
    {cols}
    <div><h4>Quick answers</h4><ul><li><a href="/salary-conversions/">Hourly wage to salary chart</a></li><li><a href="/25-an-hour-is-how-much-a-year/">$25 an hour per year</a></li><li><a href="/50000-a-year-is-how-much-an-hour/">$50,000 a year per hour</a></li><li><a href="/countdowns/">Holiday countdowns</a></li><li><a href="/days-until-christmas/">Days until Christmas</a></li><li><a href="/days-from-today/">Days from today</a></li></ul></div>
    <div><h4>Numbrik</h4><ul><li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li><li><a href="/privacy-policy/">Privacy policy</a></li><li><a href="/terms/">Terms of use</a></li><li><a href="/sitemap/">All pages</a></li></ul></div>
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
        out += f'<div class="group">{cats.cat_label(cat, "h3")}<ul>{items}</ul></div>'
    quick = [("/salary-conversions/", "Wage to salary chart"), ("/days-from-today/", "Days from today"), ("/countdowns/", "Holiday countdowns")]
    out += '<div class="group"><h3>Quick answers</h3><ul>' + "".join('<li><a href="%s"%s>%s</a></li>' % (u, ' aria-current="page"' if cur == u else "", n) for u, n in quick) + "</ul></div>"
    return out + "</aside>"

def write(path, s):
    full = os.path.join(OUT, path.strip("/"), "index.html") if not path.endswith((".xml", ".txt", ".html")) else os.path.join(OUT, path.strip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    # Give every content page the same layout as calculator pages: content plus the side menu.
    if '<main id="content" class="wrap page wide">' in s and s.count("</main>") == 1:
        s = s.replace('<main id="content" class="wrap page wide">', '<div class="wrap main"><main id="content" class="page">')
        s = s.replace("</main>", "</main>" + rail(path) + "</div>")
    # Each page loads only its own calculator's JavaScript (core + one tool), not every tool.
    m = re.search(r'id="toolBody" data-tool="([a-z0-9]+)"', s)
    s = s.replace(f'/assets/app.js?v={V}', f'/assets/js/{m.group(1) if m else "core"}.js?v={V}')
    open(full, "w").write(s)

def strip_tags(s): return re.sub(r"<[^>]+>", "", s)

# ---------------- tool pages ----------------

EMBED_H = json.load(open("embed_heights.json")) if os.path.exists("embed_heights.json") else {}
def embed_code(t):
    h = EMBED_H.get(t["id"], 620)
    return (f'<iframe src="{DOMAIN}/embed/{t["slug"]}/" title="{E(t["name"])}" width="100%" height="{h}" loading="lazy" '
            f'style="border:1px solid #d9dee6;border-radius:12px;max-width:680px"></iframe>\n'
            f'<p style="font-size:13px;margin:4px 0 0"><a href="{DOMAIN}/{t["slug"]}/">{E(t["name"])}</a> by Numbrik</p>')
def embed_box(t):
    return (f'<h2>Add this calculator to your website</h2><p>Free for blogs, schools and businesses. Copy the code and paste it into your page '
            f'(in WordPress, use a Custom HTML block). Please keep the credit link.</p>'
            f'<textarea class="embed-code" id="embedCode" readonly rows="4" aria-label="Embed code">{E(embed_code(t))}</textarea>'
            f'<p><button type="button" class="chip" data-copy="embedCode">Copy embed code</button></p>')

PUBLISHER = {"@type": "Organization", "name": "Numbrik", "url": DOMAIN + "/", "logo": {"@type": "ImageObject", "url": DOMAIN + "/apple-touch-icon.png"},
             "sameAs": ["https://github.com/numbrikcom-pixel/numbrik"]}
for t in T:
    path = f"/{t['slug']}/"
    url = DOMAIN + path
    qq, qa_a = qa.answer(t)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebApplication", "name": t["name"], "url": url, "description": t["meta"],
         "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
            *([{"@type": "ListItem", "position": 2, "name": cats.CATS[t["cat"]][1], "item": DOMAIN + cats.cat_url(t["cat"])}] if t["cat"] in cats.CATS else []),
            {"@type": "ListItem", "position": 3 if t["cat"] in cats.CATS else 2, "name": t["name"], "item": url}]},
        {"@type": "WebPage", "@id": url + "#webpage", "name": t["title"], "url": url, "description": t["meta"], "inLanguage": "en-US", "dateModified": TODAY,
         "author": {"@type": "Organization", "name": "Numbrik team", "url": DOMAIN + "/about/"}, "publisher": PUBLISHER,
         "isPartOf": {"@type": "WebSite", "name": "Numbrik", "url": DOMAIN + "/"},
         "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".quick-answer p", ".lede"]}},
        {"@type": "HowTo", "name": f"How to use the {t['name']}", "step": [{"@type": "HowToStep", "position": i + 1, "text": s_} for i, s_ in enumerate(t["steps"])]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in ([(qq, qa_a)] if qq else []) + t["faqs"]]}]}
    steps = "".join(f"<li>{E(s)}</li>" for s in t["steps"])
    faqs = "".join(f'<div class="qa"><h3>{E(q)}</h3><p>{E(a)}</p></div>' for q, a in t["faqs"])
    quick = f'<section class="quick-answer" aria-label="Quick answer"><h2>{E(qq)}</h2><p>{E(qa_a)}</p></section>' if qq else ""
    related = "".join(card(BYID[r]) for r in t["related"])
    page = head(t["title"], t["meta"], path, ld) + f"""
<nav class="wrap crumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li>{cats.cat_crumb(t["cat"])}<li aria-current="page">{E(t["name"])}</li></ol></nav>
<div class="wrap main">
  <main class="content" id="content">
    <h1>{E(t.get("h1", t["name"]))}</h1>
    <p class="byline">By the <a href="/about/">Numbrik team</a> · Tested against worked examples · Updated <time datetime="{TODAY}">{TODAY_TXT}</time></p>
    <p class="lede">{E(t["lede"])}</p>
    <div class="panel"><div class="panel-body" id="toolBody" data-tool="{t["id"]}"><p class="loading">Loading calculator…</p><noscript><p class="loading">Turn on JavaScript to use this calculator.</p></noscript></div></div>
    {quick}
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
      {embed_box(t)}
    </article>
    <section class="related" aria-label="Related calculators"><h2>Related calculators</h2><div class="cards">{related}</div></section>
  </main>
  {rail(t["id"])}
</div>
""" + footer()
    write(path, page)


# ---------------- embeddable widgets (noindex; their credit link points back to the full page) ----------------
for t in T:
    pg = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(t["name"])} | Numbrik</title><meta name="robots" content="noindex,follow"><link rel="canonical" href="{DOMAIN}/{t["slug"]}/">
<link rel="stylesheet" href="/assets/style.css?v={V}"><script>try{{var th=localStorage.getItem('nb_theme');if(th)document.documentElement.setAttribute('data-theme',JSON.parse(th))}}catch(e){{}}</script></head>
<body class="embed"><div class="panel"><div class="panel-body" id="toolBody" data-tool="{t["id"]}"><p class="loading">Loading calculator…</p></div></div>
<p class="embed-credit"><a href="{DOMAIN}/{t["slug"]}/" target="_blank" rel="noopener">{E(t["name"])}</a> by <a href="{DOMAIN}/" target="_blank" rel="noopener">Numbrik</a></p>
<script src="/assets/app.js?v={V}" defer></script></body></html>"""
    write(f"/embed/{t['slug']}/", pg)

# ---------------- home ----------------
home_ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebSite", "name": "Numbrik", "url": DOMAIN + "/"},
    {"@type": "Organization", "name": "Numbrik", "url": DOMAIN + "/", "logo": DOMAIN + "/apple-touch-icon.png"}]}
cat_html = ""
for cat in ORDER:
    cat_html += f'<section>{cats.cat_label(cat, "h2")}<div class="cards">{"".join(card(t) for t in T if t["cat"] == cat)}</div></section>'
pop = "".join(f'<a href="/{BYID[i]["slug"]}/">{E(BYID[i]["short"])}</a>' for i in ["timecard", "gpa", "loan", "calorie", "hours", "age"])
home = head("Free Online Calculator & Everyday Calculators | Numbrik",
            "Free online calculator with scientific functions, plus calculators for pay, loans, grades, health, dates and conversions. Results update as you type.", "/", home_ld) + f"""
<main id="content">
  <section class="wrap hero">
    <h1>Free calculators that answer as you type</h1>
    <p class="lede">Hours and pay, loans, grades, health and everyday conversions. Results update live, units and currency follow your region, and nothing you enter leaves your browser.</p>
    <div class="pop"><span>Popular:</span>{pop}</div>
    <div class="panel"><div class="panel-body" id="toolBody" data-tool="scientific"><p class="loading">Loading calculator…</p><noscript><p class="loading">Turn on JavaScript to use the calculator.</p></noscript></div></div>
    <p class="hint">Need more? Open the full <a href="/scientific-calculator/">scientific calculator</a> page or pick a calculator below.</p>
  </section>
  <div class="wrap home-cats">{cat_html}</div>
  <section class="wrap home-cats" aria-label="Quick answers"><section><h2>Quick answers</h2><div class="cards">
<a class="card" href="/salary-conversions/"><small>Pay</small><b>Hourly wage to salary chart</b><span>$10 to $60 an hour and $30,000 to $150,000 a year, with take-home pay.</span></a>
<a class="card" href="/countdowns/"><small>Dates</small><b>Holiday countdowns</b><span>Live countdowns to Christmas, Thanksgiving, Memorial Day and 22 more.</span></a>
<a class="card" href="/days-from-today/"><small>Dates</small><b>Days from today</b><span>The date 30, 60, 90 or any number of days from today.</span></a>
</div></section></section>
  <section class="wrap why" aria-label="Why Numbrik">
    <div><h3>Live results</h3><p>No Calculate button. Change a number and the answer updates straight away.</p></div>
    <div><h3>Made for your region</h3><p>Choose the United States, Canada, Australia, the UK or the Netherlands to set currency, units and overtime defaults.</p></div>
    <div><h3>Private by design</h3><p>Calculations run on your device. Saved entries, like your time card or GPA courses, stay in your own browser. <a href="/about/">How we build our calculators</a>.</p></div>
  </section>
</main>
""" + footer()
write("/", home)

# ---------------- static pages ----------------
def simple(path, title, desc, h1, body, noindex=False):
    write(path, head(title, desc, path, noindex=noindex) + f'<main id="content" class="wrap page"><h1>{E(h1)}</h1>{body}</main>' + footer())

simple("/about/", "About Numbrik – Free, Accurate Everyday Calculators", "Numbrik builds fast, free and accurate calculators for everyday work, money, health and school questions, with the method shown on every page.", "About Numbrik", f"""
<p class="lede">Numbrik is an independent website that makes free calculators for the questions people run into every day: how many hours they worked, what a loan will cost, what their GPA is, or how many millilitres are in a cup.</p>
<h2>What we care about</h2>
<ul><li><strong>Accuracy.</strong> Every calculator shows its formula and a worked example, so you can check the answer yourself.</li>
<li><strong>Speed.</strong> Pages are small and results update as you type, on phones as well as computers.</li>
<li><strong>Local defaults.</strong> Currency, units and overtime rules follow the region you choose: the United States, Canada, Australia, the United Kingdom or the Netherlands.</li>
<li><strong>Privacy.</strong> Calculations happen in your browser. We don't ask you to sign up.</li></ul>
<h2>Sources and methods</h2>
<p>Our calculators use standard, published methods. Examples include the US Fair Labor Standards Act overtime rule for the time card, the World Health Organization adult categories for BMI, the Mifflin-St Jeor equation for calorie needs, and the standard amortization formula for loans. Each page explains the method it uses and its limits.</p>
<h2>How we test every calculator</h2>
<p>Before a calculator goes live we check its results against worked examples by hand and against published reference values, such as the IRS 2026 federal tax brackets for take-home pay and the Pythagorean triples for the right triangle calculator. We test edge cases like overnight shifts, leap years, dividing by zero and empty fields, and check every page on a 375-pixel phone screen. The worked example on each page is calculated by the same code you use, so the numbers in the text always match the tool.</p>
<h2>Recent updates</h2>
<ul><li><strong>November 1, 2026:</strong> Removed thin conversion pages and expanded the salary chart, category guides and days-from-today answers.</li>
<li><strong>October 31, 2026:</strong> Added BMR, protein, macro, one rep max, pace, ratio, slope, average, right triangle, quadratic formula and CD calculators, plus scientific, fraction, standard deviation, compound interest, sales tax, due date, body fat and password tools.</li>
<li><strong>October 29, 2026:</strong> Added category pages and a full site map.</li>
<li><strong>October 26, 2026:</strong> Rewrote the final grade, car payment, salary, hours, tip and sleep pages based on the questions people search for.</li></ul>
<h2>Corrections</h2>
<p>If you find a mistake or a rule that has changed in your country, please <a href="/contact/">contact us</a>. We review every report and update the page.</p>
<p class="updated">Last updated {TODAY_TXT}.</p>""")

simple("/contact/", "Contact Numbrik – Report an Error or Suggest a Tool", "Contact Numbrik to report an error, suggest a new calculator or ask a question about how a result is worked out.", "Contact us", f"""
<p class="lede">Found an error, want a new calculator, or have a question about the site? Email us and we'll reply as soon as we can.</p>
<p class="copyline"><code id="mail">hello@numbrik.com</code><button class="btn" type="button" onclick="var b=this;navigator.clipboard&&navigator.clipboard.writeText('hello@numbrik.com').then(function(){{b.textContent='Copied'}})">Copy email</button></p>
<h2>When reporting an error</h2>
<ul><li>The page address, for example numbrik.com/gpa-calculator/</li><li>The numbers you entered</li><li>The result you expected and where the rule comes from</li></ul>
<p>We don't give personal financial, medical or legal advice by email. For decisions about your own situation, please speak to a qualified professional.</p>""")

simple("/privacy-policy/", "Privacy Policy – Numbrik Calculators", "How Numbrik handles your data, cookies, Google Analytics and Google AdSense advertising, and your privacy rights in the US, UK and EU.", "Privacy policy", f"""
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

simple("/terms/", "Terms of Use – Numbrik Calculators", "The terms for using Numbrik calculators: results are estimates for planning, not financial, medical or legal advice.", "Terms of use", f"""
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
EXTRA_URLS = cats.build_cats(globals()) + extra.build(globals()) + extra.build_countdowns(globals()) + days.build_days(globals())
urls = ["/"] + [f"/{t['slug']}/" for t in T] + EXTRA_URLS + ["/about/", "/contact/", "/privacy-policy/", "/terms/"]
# ---------------- HTML site map ----------------
def _ul(items): return '<ul class="linklist">' + "".join(f'<li><a href="{u}">{E(n)}</a></li>' for u, n in items) + "</ul>"
smap = ""
for cat in ORDER:
    tl = [t for t in T if t["cat"] == cat]
    if tl: smap += f"<h2>{E(cat)}</h2>" + _ul([(f"/{t['slug']}/", t["name"]) for t in tl])
smap += "<h2>Categories</h2>" + _ul([(f"/{s}/", h) for s, h, _, _ in cats.CATS.values()])
smap += "<h2>Hourly wage to salary</h2>" + _ul([(extra.hslug(h), f"${h} an hour") for h in extra.HOURLY] + [(extra.aslug(a), f"${a:,} a year") for a in extra.ANNUAL] + [("/salary-conversions/", "Wage to salary chart")])
smap += "<h2>Holiday countdowns</h2>" + _ul([(f"/{s}/", f"Days until {n}") for _, s, n, _ in extra.HOLS] + [("/countdowns/", "All countdowns")])
smap += "<h2>Days from today</h2>" + _ul([(days.slug(n, "d"), f"{n} days from today") for n in days.DAYS] + [(days.slug(n, "w"), f"{n} weeks from today") for n in days.WEEKS] + [("/days-from-today/", "Days from today calculator")])
smap += "<h2>About Numbrik</h2>" + _ul([("/about/", "About"), ("/contact/", "Contact"), ("/privacy-policy/", "Privacy policy"), ("/terms/", "Terms of use")])
write("/sitemap/", head("All Calculators & Pages – Site Map | Numbrik", "Every Numbrik page in one list: calculators by category, wage conversions, holiday countdowns and days-from-today pages.", "/sitemap/") +
      '<nav class="wrap crumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li><li aria-current="page">All pages</li></ol></nav>' +
      f'<main id="content" class="wrap page wide"><h1>All calculators and pages</h1><p class="lede">Every page on Numbrik, grouped by topic.</p>{smap}</main>' + footer())
urls.append("/sitemap/")
# Real per-page lastmod: a page's date changes only when its content changes (tracked in lastmod.json).
import hashlib, datetime
_LM_FILE = "lastmod.json"
_lm = json.load(open(_LM_FILE)) if os.path.exists(_LM_FILE) else {}
_SEED = {"2026-11-01": ["/half-birthday-calculator/", "/military-time-converter/", "/pay-raise-calculator/", "/water-intake-calculator/", "/mulch-calculator/",
                        "/working-days-calculator/", "/salary-conversions/", "/about/", "/tip-calculator/", "/days-between-dates/", "/home-project-calculators/",
                        "/date-and-time-calculators/", "/random-and-game-tools/", "/work-and-pay-calculators/", "/health-calculators/", "/math-calculators/"],
         "2026-11-02": ["/turkey-calculator/", "/hours-calculator/", "/days-until-thanksgiving/", "/days-until-christmas/", "/days-until-christmas-eve/"]}
_seed = {u: d for d, us in _SEED.items() for u in us}
def _norm(h):
    # Only the page's own content counts: drop the head, side menu, header and footer, which change site-wide
    m = re.search(r"<main.*?</main>", h, re.S)
    h = m.group(0) if m else h
    h = re.sub(r'<aside class="rail".*?</aside>', "", h, flags=re.S)
    h = re.sub(r'<section class="related".*?</section>', "", h, flags=re.S)
    h = re.sub(r"\?v=\d+", "", h)
    h = re.sub(r"/assets/js/[a-z0-9]+\.js", "", h)
    h = re.sub(r"(Last reviewed|Last updated|Effective) [A-Z][a-z]+ \d+, \d{4}", "", h)
    h = re.sub(r'"dateModified": "[0-9-]+"', "", h)
    h = re.sub(r'<time datetime="[0-9-]+">[^<]*</time>', "", h)
    return hashlib.sha1(h.encode()).hexdigest()
_today = datetime.date.today().isoformat()
LASTMOD = {}
for u in urls:
    f = os.path.join(OUT, u.strip("/"), "index.html") if u != "/" else os.path.join(OUT, "index.html")
    hv = _norm(open(f).read())
    if u in _lm and len(_lm[u]) == 2:  # one-time migration to the content-only hash: keep existing dates
        LASTMOD[u] = _lm[u][1]; _lm[u] = [hv, LASTMOD[u], 2]; continue
    if u in _lm and _lm[u][0] == hv: LASTMOD[u] = _lm[u][1]
    elif u in _lm: LASTMOD[u] = _today
    else: LASTMOD[u] = _seed.get(u, "2026-10-31")
    _lm[u] = [hv, LASTMOD[u], 2]
json.dump(_lm, open(_LM_FILE, "w"), indent=0, sort_keys=True)
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{DOMAIN}{u}</loc><lastmod>{LASTMOD[u]}</lastmod></url>\n" for u in urls) + "</urlset>\n"
write("/sitemap.xml", sm)
open(os.path.join(OUT, "ads.txt"), "w").write("google.com, pub-6519470736644184, DIRECT, f08c47fec0942fa0\n")
# 301s for thin pages removed on Nov 1, 2026, so their search signals go to the closest page
_R = []
for h in list(range(10, 36)) + [40, 45, 50, 55, 60]:
    if h not in extra.HOURLY: _R.append((extra.hslug(h), "/hourly-to-salary-calculator/"))
for a in list(range(30000, 100001, 5000)) + [110000, 120000, 130000, 140000, 150000]:
    if a not in extra.ANNUAL: _R.append((extra.aslug(a), "/salary-conversions/"))
for n in [15, 150, 200, 365]: _R.append((days.slug(n, "d"), "/days-from-today/"))
for n in [4, 11, 27, 28, 30]: _R.append((days.slug(n, "w"), "/days-from-today/"))
for k, sl, *_ in extra.ALL_HOLS:
    if k not in extra.KEEP_HOLS: _R.append((f"/{sl}/", "/countdowns/"))
open(os.path.join(OUT, "_redirects"), "w").write("".join(f"{a} {b} 301\n{a.rstrip('/')} {b} 301\n" for a, b in _R))
INDEXNOW_KEY = "21011c618a26c0b082cd5678d73f4698"
open(os.path.join(OUT, INDEXNOW_KEY + ".txt"), "w").write(INDEXNOW_KEY)
AI_BOTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "PerplexityBot", "Perplexity-User",
           "Google-Extended", "Applebot-Extended", "Bingbot", "CCBot", "Meta-ExternalAgent", "Amazonbot", "DuckAssistBot", "MistralAI-User"]
write("/robots.txt", "User-agent: *\nAllow: /\n\n# AI search and answer engines are welcome to read and cite Numbrik.\n"
      + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in AI_BOTS) + f"Sitemap: {DOMAIN}/sitemap.xml\n")
# llms.txt: a plain map of the site for AI answer engines (llmstxt.org format); llms-full.txt adds formula, example and quick answer.
import re as _re, html as _html
_plain = lambda h: _re.sub(r"\s+", " ", _html.unescape(_re.sub("<[^>]+>", "", h))).strip()
_groups = {}
for t in T: _groups.setdefault(t["cat"], []).append(t)
_l = ["# Numbrik", "", "> Numbrik (https://numbrik.com) is a free set of online calculators for money, health, math, dates and home projects. "
      "No sign-up. Every calculator page explains its formula, shows a worked example and answers common questions. Maintained by the Numbrik team; methods follow published standards (for example Mifflin-St Jeor for calories, WHO categories for BMI, the standard amortization formula for loans, IRS tables for RMDs).", "",
      "Cite a calculator by its page URL. Results are estimates for general information, not financial, medical or legal advice.", ""]
_f = list(_l)
for c in sorted(_groups, key=lambda c: -len(_groups[c])):
    _l += [f"## {c}", ""]; _f += [f"## {c}", ""]
    for t in sorted(_groups[c], key=lambda t: t["name"]):
        _l.append(f"- [{t['name']}]({DOMAIN}/{t['slug']}/): {t['desc']}")
        q_, a_ = qa.answer(t)
        _f += [f"### {t['name']}", f"URL: {DOMAIN}/{t['slug']}/", "", _plain(t["lede"]), ""] + ([f"Q: {q_}", f"A: {a_}", ""] if q_ else []) + \
              ["Formula:", "```", t["formula"], "```", "", "Example: " + _plain(t["example"]), ""]
    _l.append(""); 
_l += ["## About", "", f"- [About Numbrik]({DOMAIN}/about/): who maintains the site and how calculators are tested", f"- [Sitemap]({DOMAIN}/sitemap.xml)", ""]
import shutil as _sh; _sh.copy("BingSiteAuth.xml", "dist/BingSiteAuth.xml")  # Bing Webmaster Tools verification (Nov 10, 2026)
open("dist/llms.txt", "w").write("\n".join(_l)); open("dist/llms-full.txt", "w").write("\n".join(_f))
open(os.path.join(OUT, "_headers"), "w").write("""/assets/*
  Cache-Control: public, max-age=31536000, immutable
/*
  X-Content-Type-Options: nosniff
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()
  X-Frame-Options: SAMEORIGIN
/embed/*
  ! X-Frame-Options
  Content-Security-Policy: frame-ancestors *
""")
open(os.path.join(OUT, "favicon.svg"), "w").write(FAVICON)

# assets
os.makedirs(os.path.join(OUT, "assets/fonts"), exist_ok=True)
shutil.copy("src/style.css", os.path.join(OUT, "assets/style.css"))
import subprocess
subprocess.run(["node", "tools/bundle.js", "src/app.js", os.path.join(OUT, "assets/js")], check=True)
F = "fontsrc/node_modules/@fontsource/"
for src, dst in [("bricolage-grotesque/files/bricolage-grotesque-latin-700-normal.woff2", "bricolage-700")]:
    shutil.copy(F + src, os.path.join(OUT, f"assets/fonts/{dst}.woff2"))
print("built", len(urls), "pages")

# Google Search Console verification file
open(os.path.join(OUT, "google3ac709f348cc4545.html"), "w").write("google-site-verification: google3ac709f348cc4545.html")

# Cache-busting by content: every page points at ?v=<hash of the exact file>, so browsers fetch a new
# bundle the moment it changes (assets are cached for a year as immutable).
import hashlib as _hl, glob as _gl
def _h(p): return _hl.sha1(open(p, "rb").read()).hexdigest()[:10]
_css = _h(os.path.join(OUT, "assets/style.css"))
_js = {os.path.basename(p)[:-3]: _h(p) for p in _gl.glob(os.path.join(OUT, "assets/js/*.js"))}
for f in _gl.glob(os.path.join(OUT, "**/*.html"), recursive=True):
    s = open(f).read()
    s2 = s.replace(f"/assets/style.css?v={V}", f"/assets/style.css?v={_css}")
    s2 = re.sub(r"/assets/js/([a-z0-9]+)\.js\?v=" + re.escape(V), lambda m: f"/assets/js/{m.group(1)}.js?v={_js[m.group(1)]}", s2)
    if s2 != s: open(f, "w").write(s2)

# Put each page's real last-updated date into its visible byline, review note and WebPage schema
for u in urls:
    f = os.path.join(OUT, u.strip("/"), "index.html") if u != "/" else os.path.join(OUT, "index.html")
    d = LASTMOD[u]; dt = datetime.date.fromisoformat(d); txt = dt.strftime("%B ") + str(dt.day) + dt.strftime(", %Y")
    h = open(f).read()
    h2 = re.sub(r'<time datetime="[0-9-]+">[^<]*</time>', f'<time datetime="{d}">{txt}</time>', h)
    h2 = re.sub(r'"dateModified": "[0-9-]+"', f'"dateModified": "{d}"', h2)
    h2 = re.sub(r"Last reviewed [A-Z][a-z]+ \d+, \d{4}\.", f"Last reviewed {txt}.", h2)
    if h2 != h: open(f, "w").write(h2)
