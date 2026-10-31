"""Category hub pages (added October 29, 2026). Give breadcrumbs, menus and the homepage real category links."""
import html
from content import T

E = html.escape
# category -> (slug, H1, intro, extra links)
CATS = {
 "Work & pay": ("work-and-pay-calculators", "Work & Pay Calculators",
   "Calculators for hourly and salaried workers in the US, Canada, Australia, the UK and the Netherlands. Add up a week of shifts with overtime, find the hours between two clock times, convert an hourly wage to a yearly salary, and estimate take-home pay after 2026 US federal tax, Social Security and Medicare.",
   [("/salary-conversions/", "Hourly wage to salary chart"), ("/25-an-hour-is-how-much-a-year/", "$25 an hour is how much a year?"), ("/60000-a-year-is-how-much-an-hour/", "$60,000 a year is how much an hour?")]),
 "Money": ("money-calculators", "Money Calculators",
   "Everyday money maths: work out a tip and split the bill, find percentages, discounts and percent change, see the monthly payment and total interest on a mortgage or loan with a yearly amortization chart, and estimate a car payment including sales tax, fees and a trade-in.",
   []),
 "Health": ("health-calculators", "Health Calculators",
   "Health calculators for adults: body mass index with the World Health Organization categories, daily calorie needs from the Mifflin-St Jeor equation, and bedtimes that line up with 90-minute sleep cycles. Each page explains its method and limits. Results are estimates, not medical advice.",
   []),
 "Students": ("student-calculators", "Student Calculators",
   "Tools for students and teachers: semester and cumulative GPA on the 4.0 scale, weighted class grades with letter grades, the score you need on a final exam to pass or reach an A, and least common multiple and greatest common factor with prime factorization shown.",
   []),
 "Dates & time": ("date-and-time-calculators", "Date & Time Calculators",
   "Count the days and weekdays between two dates, find your exact age, see the date any number of days or weeks from today, and follow live countdowns to holidays in the US, Canada, the UK and Australia.",
   [("/days-from-today/", "Days from today calculator"), ("/countdowns/", "Holiday countdowns"), ("/90-days-from-today/", "90 days from today"), ("/days-until-christmas/", "Days until Christmas")]),
 "Home": ("home-project-calculators", "Home Project Calculators",
   "Plan a home project before you buy materials: measure square footage for flooring or carpet, work out cubic yards and bags of concrete for a slab or post holes, and find how much paint a room needs, in feet or metres.",
   []),
 "Math": ("math-calculators", "Math Calculators",
   "Maths tools for homework and work: a scientific calculator with trig, logs and powers, a fraction calculator that shows the working, and a standard deviation calculator for sample and population data.",
   [("/lcm-calculator/", "LCM calculator"), ("/gcf-calculator/", "GCF calculator"), ("/percentage-calculator/", "Percentage calculator")]),
 "Fun": ("random-and-game-tools", "Random & Game Tools",
   "Fair random tools for games, classrooms and quick decisions: roll dice from d4 to d100, pick random numbers with or without repeats, flip a coin up to 1,000 times, or create strong passwords. Every result comes from your browser's cryptographic random number generator.",
   []),
}

def cat_url(cat): return f"/{CATS[cat][0]}/" if cat in CATS else None
def cat_crumb(cat):
    u = cat_url(cat)
    return f'<li><a href="{u}">{E(cat)}</a></li>' if u else f"<li>{E(cat)}</li>"
def cat_label(cat, tag):
    u = cat_url(cat)
    return f'<{tag}><a href="{u}">{E(cat)}</a></{tag}>' if u else f"<{tag}>{E(cat)}</{tag}>"

def build_cats(g):
    head, footer, write, card, DOMAIN = g["head"], g["footer"], g["write"], g["card"], g["DOMAIN"]
    urls = []
    for cat, (slug, h1, intro, links) in CATS.items():
        tools = [t for t in T if t["cat"] == cat]
        path = f"/{slug}/"
        more = ""
        if links:
            more = '<h2>Quick answers</h2><ul class="linklist">' + "".join(f'<li><a href="{u}">{E(n)}</a></li>' for u, n in links) + "</ul>"
        guide = "".join('<div><dt><a href="/%s/">%s</a></dt><dd>%s</dd></div>' % (t["slug"], E(t["name"]), E(t["lede"])) for t in tools)
        others = "".join(f'<li><a href="/{CATS[c][0]}/">{E(CATS[c][1])}</a></li>' for c in CATS if c != cat)
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "CollectionPage", "name": h1, "url": DOMAIN + path, "description": intro,
             "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": t["name"], "url": f"{DOMAIN}/{t['slug']}/"} for i, t in enumerate(tools)]}},
            {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"}, {"@type": "ListItem", "position": 2, "name": h1, "item": DOMAIN + path}]}]}
        desc = (intro[:150].rsplit(" ", 1)[0] + "…") if len(intro) > 155 else intro
        write(path, head(f"{h1} – Free Online Tools | Numbrik", desc, path, ld) +
              f'<nav class="wrap crumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li><li aria-current="page">{E(h1)}</li></ol></nav>' +
              f'<main id="content" class="wrap page wide"><h1>{E(h1)}</h1><p class="lede">{E(intro)}</p>'
              f'<h2>All {E(h1.lower())}</h2><div class="cards">{"".join(card(t) for t in tools)}</div>'
              f'<h2>Which one do I need?</h2><dl class="guide">{guide}</dl>{more}'
              f'<h2>More categories</h2><ul class="linklist">{others}</ul></main>' + footer())
        urls.append(path)
    return urls
