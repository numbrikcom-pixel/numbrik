"""Long-tail keyword pages: wage conversions and holiday countdowns (added October 22, 2026)."""
import json, html
from datetime import date, timedelta
from content2 import takehome
from more import MORE

E = html.escape
HOURLY = list(range(10, 36)) + [40, 45, 50, 55, 60]
ANNUAL = list(range(30000, 100001, 5000)) + [110000, 120000, 130000, 140000, 150000]
def hslug(h): return f"/{h}-an-hour-is-how-much-a-year/"
def aslug(a): return f"/{a}-a-year-is-how-much-an-hour/"
def usd(x, d=2): return f"${x:,.{d}f}"
def usd0(x): return f"${x:,.0f}"
def amt(h): return f"${h:g}"

HOLS = [  # key, slug, name, short rule text
 ("christmas", "days-until-christmas", "Christmas", "Christmas Day is always on December 25."),
 ("halloween", "days-until-halloween", "Halloween", "Halloween is always on October 31."),
 ("thanksgiving", "days-until-thanksgiving", "Thanksgiving", "US Thanksgiving is the fourth Thursday of November. Canadian Thanksgiving is earlier, on the second Monday of October."),
 ("blackfriday", "days-until-black-friday", "Black Friday", "Black Friday is the day after US Thanksgiving, so it always falls between November 23 and November 29."),
 ("newyear", "days-until-new-year", "New Year's Day", "New Year's Day is always on January 1."),
 ("valentines", "days-until-valentines-day", "Valentine's Day", "Valentine's Day is always on February 14."),
 ("easter", "days-until-easter", "Easter", "Easter Sunday moves every year. In Western churches it is the first Sunday after the first full moon on or after March 21, so it falls between March 22 and April 25."),
 ("mothers", "days-until-mothers-day", "Mother's Day", "In the US, Canada and Australia, Mother's Day is the second Sunday of May. The UK's Mothering Sunday is different: three weeks before Easter Sunday."),
 ("fathers", "days-until-fathers-day", "Father's Day", "In the US, Canada and the UK, Father's Day is the third Sunday of June. Australia celebrates it on the first Sunday of September."),
 ("july4", "days-until-4th-of-july", "the 4th of July", "Independence Day in the United States is always on July 4."),
 ("christmaseve", "days-until-christmas-eve", "Christmas Eve", "Christmas Eve is always on December 24, the day before Christmas."),
 ("newyearseve", "days-until-new-years-eve", "New Year's Eve", "New Year's Eve is always on December 31."),
 ("mlk", "days-until-mlk-day", "Martin Luther King Jr. Day", "Martin Luther King Jr. Day is a US federal holiday on the third Monday of January."),
 ("presidents", "days-until-presidents-day", "Presidents' Day", "Presidents' Day, officially Washington's Birthday, is a US federal holiday on the third Monday of February."),
 ("stpatricks", "days-until-st-patricks-day", "St. Patrick's Day", "St. Patrick's Day is always on March 17."),
 ("memorial", "days-until-memorial-day", "Memorial Day", "Memorial Day is a US federal holiday on the last Monday of May. Many people treat the long weekend as the start of summer."),
 ("juneteenth", "days-until-juneteenth", "Juneteenth", "Juneteenth is a US federal holiday on June 19. When it falls on a Saturday the federal day off is the Friday before, and when it falls on a Sunday it is the Monday after."),
 ("laborday", "days-until-labor-day", "Labor Day", "In the US and Canada, Labor Day (Labour Day in Canada) is the first Monday of September."),
 ("veterans", "days-until-veterans-day", "Veterans Day", "Veterans Day in the US is always on November 11. Canada, the UK and Australia mark Remembrance Day on the same date."),
 ("canadaday", "days-until-canada-day", "Canada Day", "Canada Day is always on July 1. When July 1 is a Sunday, the holiday is observed on Monday, July 2."),
 ("cathanksgiving", "days-until-canadian-thanksgiving", "Canadian Thanksgiving", "Thanksgiving in Canada is the second Monday of October, about six weeks before US Thanksgiving."),
 ("boxingday", "days-until-boxing-day", "Boxing Day", "Boxing Day is December 26 in the UK, Canada, Australia and other Commonwealth countries. When it falls on a weekend, the public holiday moves to the next weekday."),
 ("australiaday", "days-until-australia-day", "Australia Day", "Australia Day is on January 26. When it falls on a weekend, the public holiday moves to the following Monday."),
 ("dstend", "days-until-daylight-saving-ends", "the end of daylight saving time", "In the US and most of Canada, daylight saving time ends at 2:00 a.m. on the first Sunday of November, when clocks go back one hour. The UK and the EU change on the last Sunday of October, and Australia's southern states on the first Sunday of April."),
 ("dststart", "days-until-daylight-saving-starts", "the start of daylight saving time", "In the US and most of Canada, daylight saving time starts at 2:00 a.m. on the second Sunday of March, when clocks go forward one hour. The UK and the EU change on the last Sunday of March, and Australia's southern states on the first Sunday of October."),
]
COUNTRY = {"thanksgiving": "US", "blackfriday": "US", "july4": "US", "mlk": "US", "presidents": "US", "memorial": "US", "juneteenth": "US", "veterans": "US", "laborday": "US · Canada",
           "canadaday": "Canada", "cathanksgiving": "Canada", "boxingday": "UK · Canada · Australia", "australiaday": "Australia", "dstend": "US · Canada", "dststart": "US · Canada"}
RULES = {"christmaseve": ("f", 12, 24), "newyearseve": ("f", 12, 31), "stpatricks": ("f", 3, 17), "juneteenth": ("f", 6, 19), "veterans": ("f", 11, 11),
         "canadaday": ("f", 7, 1), "boxingday": ("f", 12, 26), "australiaday": ("f", 1, 26),
         "mlk": ("n", 1, 0, 3), "presidents": ("n", 2, 0, 3), "laborday": ("n", 9, 0, 1), "cathanksgiving": ("n", 10, 0, 2),
         "dstend": ("n", 11, 6, 1), "dststart": ("n", 3, 6, 2), "memorial": ("l", 5, 0)}
def last_dow(y, m, dow):
    d = (date(y, m + 1, 1) if m < 12 else date(y + 1, 1, 1)) - timedelta(1)
    return d - timedelta((d.weekday() - dow) % 7)
def nth_dow(y, m, dow, n):  # dow: Monday=0 … Sunday=6
    d = date(y, m, 1); return d + timedelta((dow - d.weekday()) % 7 + 7 * (n - 1))
def easter(y):
    a, b, c = y % 19, y // 100, y % 100; d, e = b // 4, b % 4; f = (b + 8) // 25; g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30; i, k = c // 4, c % 4; l = (32 + 2 * e + 2 * i - h - k) % 7; m = (a + 11 * h + 22 * l) // 451
    return date(y, (h + l - 7 * m + 114) // 31, (h + l - 7 * m + 114) % 31 + 1)
def hol_date(k, y):
    fixed = {"christmas": (12, 25), "halloween": (10, 31), "newyear": (1, 1), "valentines": (2, 14), "july4": (7, 4)}
    if k in fixed: return date(y, *fixed[k])
    if k == "thanksgiving": return nth_dow(y, 11, 3, 4)
    if k == "blackfriday": return nth_dow(y, 11, 3, 4) + timedelta(1)
    if k == "mothers": return nth_dow(y, 5, 6, 2)
    if k == "fathers": return nth_dow(y, 6, 6, 3)
    if k == "easter": return easter(y)
    r = RULES.get(k)
    if r and r[0] == "f": return date(y, r[1], r[2])
    if r and r[0] == "n": return nth_dow(y, r[1], r[2], r[3])
    if r and r[0] == "l": return last_dow(y, r[1], r[2])
def fmt(d): return f"{d:%A}, {d:%B} {d.day}, {d.year}"

# links from existing tool pages
MORE["salary"] = MORE.get("salary", "") + """<h2>Quick wage conversions</h2><p>See the yearly, monthly and after-tax figures for a specific wage: <a href="/20-an-hour-is-how-much-a-year/">$20 an hour</a>, <a href="/25-an-hour-is-how-much-a-year/">$25 an hour</a>, <a href="/30-an-hour-is-how-much-a-year/">$30 an hour</a>, <a href="/50000-a-year-is-how-much-an-hour/">$50,000 a year</a> or <a href="/salary-conversions/">all wage conversions</a>.</p>"""
MORE["days"] = MORE.get("days", "") + """<h2>Holiday countdowns</h2><p>Live countdowns for <a href="/days-until-christmas/">Christmas</a>, <a href="/days-until-halloween/">Halloween</a>, <a href="/days-until-thanksgiving/">Thanksgiving</a>, <a href="/days-until-easter/">Easter</a> and <a href="/countdowns/">more holidays</a>.</p>"""

def build(g):
    head, footer, write, DOMAIN, TODAY_TXT = g["head"], g["footer"], g["write"], g["DOMAIN"], g["TODAY_TXT"]
    today = date.fromisoformat(g["TODAY"])
    urls = []
    def crumbs(items):
        lis = "".join(f'<li><a href="{u}">{E(n)}</a></li>' if u else f'<li aria-current="page">{E(n)}</li>' for n, u in items)
        return f'<nav class="wrap crumbs" aria-label="Breadcrumb"><ol>{lis}</ol></nav>'
    def ld(path, name, faqs, parent=None):
        items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"}]
        if parent: items.append({"@type": "ListItem", "position": 2, "name": parent[0], "item": DOMAIN + parent[1]})
        items.append({"@type": "ListItem", "position": len(items) + 1, "name": name, "item": DOMAIN + path})
        graph = [{"@type": "BreadcrumbList", "itemListElement": items}]
        if faqs: graph.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]})
        return {"@context": "https://schema.org", "@graph": graph}
    def faq_html(faqs): return '<h2>Frequently asked questions</h2><div class="faq">' + "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in faqs) + "</div>"
    def page(path, title, meta, h1, lede, body, faqs, parent):
        write(path, head(title, meta, path, ld(path, h1, faqs, parent)) + crumbs([("Home", "/"), parent, (h1, None)]) +
              f'<main id="content" class="wrap page wide"><h1>{E(h1)}</h1><p class="lede">{lede}</p>{body}{faq_html(faqs) if faqs else ""}<p class="updated">Last reviewed {TODAY_TXT}.</p></main>' + footer())
        urls.append(path)
    HUB_W = ("Salary conversions", "/salary-conversions/")
    HUB_C = ("Holiday countdowns", "/countdowns/")

    # ---------- hourly → yearly ----------
    for idx, h in enumerate(HOURLY):
        y = h * 2080; t = takehome(y)
        rows = "".join(f"<tr><td>{hw:g} hours</td><td>{usd(h*hw)}</td><td>{usd0(h*hw*52)}</td><td>{usd(h*hw*52/12)}</td></tr>" for hw in [20, 25, 30, 35, 37.5, 38, 40, 45])
        prev = HOURLY[idx - 1] if idx else None; nxt = HOURLY[idx + 1] if idx + 1 < len(HOURLY) else None
        nav = " · ".join(x for x in [f'<a href="{hslug(prev)}">← {amt(prev)} an hour</a>' if prev else "", f'<a href="/salary-conversions/">All wages</a>', f'<a href="{hslug(nxt)}">{amt(nxt)} an hour →</a>' if nxt else ""] if x)
        faqs = [(f"How much is {amt(h)} an hour every two weeks?", f"{usd(h*80)} before tax, at 40 hours a week. After estimated 2026 US federal tax and FICA for a single filer with no state tax, it is about {usd(t['net']/26)}."),
                (f"How much is {amt(h)} an hour after taxes?", f"About {usd0(t['net'])} a year, or {usd(t['net']/12)} a month, for a single filer in a state with no income tax in 2026. State and local taxes, retirement contributions and benefits lower this."),
                (f"How much is {amt(h)} an hour part-time?", f"At 20 hours a week it is {usd(h*20)} a week, or {usd0(h*20*52)} a year before tax. At 30 hours a week it is {usd0(h*30*52)} a year.")]
        body = f"""<div class="answer"><span class="label">{amt(h)} an hour, full time (40 hours × 52 weeks)</span><div class="big"><em>{usd0(y)}</em> a year</div>
<dl class="kv"><div><dt>Monthly</dt><dd>{usd(y/12)}</dd></div><div><dt>Every 2 weeks</dt><dd>{usd(h*80)}</dd></div><div><dt>Weekly</dt><dd>{usd(h*40)}</dd></div><div><dt>Daily (8 hours)</dt><dd>{usd(h*8)}</dd></div><div><dt>After US tax (estimate)</dt><dd>{usd0(t['net'])} a year</dd></div></dl></div>
<h2>How it's calculated</h2><p>A full-time year is usually counted as 40 hours a week for 52 weeks, which is 2,080 paid hours. {amt(h)} × 2,080 = {usd0(y)}. Paid holidays and paid vacation still count. If you take two weeks of unpaid leave, you work 50 weeks and earn {usd0(h*2000)}.</p>
<p>A raise of $1 an hour adds $2,080 a year at full time. {amt(h)} an hour is {h/7.25:.1f} times the US federal minimum wage of $7.25. Many states and cities set a higher minimum.</p>
<h2>{amt(h)} an hour by hours per week</h2><div class="tbl"><table><thead><tr><th>Hours a week</th><th>Weekly</th><th>Yearly</th><th>Monthly</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="hint">Overtime isn't included. Hours over 40 a week are usually paid at 1.5× for non-exempt US workers.</p>
<h2>{amt(h)} an hour after taxes</h2><p>For a single filer in 2026 with no state income tax, {usd0(y)} a year means about {usd0(t['fed'])} in federal income tax, {usd0(t['ss'])} in Social Security and {usd0(t['med'])} in Medicare. That leaves roughly <strong>{usd0(t['net'])} a year</strong>, {usd(t['net']/12)} a month or {usd(t['net']/26)} every two weeks. Use the <a href="/take-home-pay-calculator/">take-home pay calculator</a> to add state tax and 401(k) contributions. The pre-tax figures above apply to any currency paid by the hour, such as Canadian or Australian dollars; the after-tax estimate uses US rules.</p>
<p>To change the hours or weeks, use the <a href="/hourly-to-salary-calculator/">hourly to salary calculator</a>. To track the hours you actually work, use the <a href="/time-card-calculator/">time card calculator</a>.</p>
<p class="pager">{nav}</p>"""
        page(hslug(h), f"{amt(h)} an Hour Is How Much a Year? ({usd0(y)}) | Numbrik",
             f"{amt(h)} an hour is {usd0(y)} a year at 40 hours a week. See monthly, biweekly and weekly pay, part-time figures and take-home pay after 2026 taxes.",
             f"{amt(h)} an hour is how much a year?",
             f"At 40 hours a week, {amt(h)} an hour is <strong>{usd0(y)} a year</strong> before tax, or {usd(y/12)} a month.", body, faqs, HUB_W)

    # ---------- yearly → hourly ----------
    for idx, a in enumerate(ANNUAL):
        h = a / 2080; t = takehome(a)
        rows = "".join(f"<tr><td>{hw:g} hours</td><td>{usd(a/(hw*52))}</td></tr>" for hw in [30, 35, 37.5, 38, 40, 45, 50])
        prev = ANNUAL[idx - 1] if idx else None; nxt = ANNUAL[idx + 1] if idx + 1 < len(ANNUAL) else None
        nav = " · ".join(x for x in [f'<a href="{aslug(prev)}">← {usd0(prev)} a year</a>' if prev else "", f'<a href="/salary-conversions/">All wages</a>', f'<a href="{aslug(nxt)}">{usd0(nxt)} a year →</a>' if nxt else ""] if x)
        faqs = [(f"How much is {usd0(a)} a year per month?", f"{usd(a/12)} before tax. After estimated 2026 US federal tax and FICA for a single filer with no state tax, about {usd(t['net']/12)}."),
                (f"How much is {usd0(a)} a year every two weeks?", f"{usd(a/26)} before tax, or about {usd(t['net']/26)} after estimated federal tax and FICA."),
                (f"How much is {usd0(a)} a year after taxes?", f"About {usd0(t['net'])} for a single filer in a state with no income tax in 2026. State tax, 401(k) contributions and benefits lower this.")]
        body = f"""<div class="answer"><span class="label">{usd0(a)} a year, full time (40 hours × 52 weeks)</span><div class="big"><em>{usd(h)}</em> an hour</div>
<dl class="kv"><div><dt>Monthly</dt><dd>{usd(a/12)}</dd></div><div><dt>Every 2 weeks</dt><dd>{usd(a/26)}</dd></div><div><dt>Twice a month</dt><dd>{usd(a/24)}</dd></div><div><dt>Weekly</dt><dd>{usd(a/52)}</dd></div><div><dt>After US tax (estimate)</dt><dd>{usd0(t['net'])} a year</dd></div></dl></div>
<h2>How it's calculated</h2><p>Divide the salary by the number of paid hours in a year. Full time is usually 40 hours a week for 52 weeks, or 2,080 hours, so {usd0(a)} ÷ 2,080 = {usd(h)} an hour. If you regularly work more than 40 hours on a fixed salary, your real hourly rate is lower, as the table shows.</p>
<h2>{usd0(a)} a year by hours per week</h2><div class="tbl"><table><thead><tr><th>Hours a week</th><th>Hourly rate</th></tr></thead><tbody>{rows}</tbody></table></div>
<h2>{usd0(a)} a year after taxes</h2><p>For a single filer in 2026 with no state income tax, expect about {usd0(t['fed'])} in federal income tax, {usd0(t['ss'])} in Social Security and {usd0(t['med'])} in Medicare, leaving roughly <strong>{usd0(t['net'])} a year</strong> or {usd(t['net']/12)} a month. Add your state's tax and retirement contributions in the <a href="/take-home-pay-calculator/">take-home pay calculator</a>. The pre-tax figures apply to any currency; the after-tax estimate uses US rules.</p>
<p>For other salaries or hours, use the <a href="/hourly-to-salary-calculator/">hourly to salary calculator</a>.</p>
<p class="pager">{nav}</p>"""
        page(aslug(a), f"{usd0(a)} a Year Is How Much an Hour? ({usd(h)}) | Numbrik",
             f"{usd0(a)} a year is {usd(h)} an hour at 40 hours a week. See monthly and biweekly pay and take-home pay after 2026 taxes.",
             f"{usd0(a)} a year is how much an hour?",
             f"At 40 hours a week, {usd0(a)} a year works out to <strong>{usd(h)} an hour</strong> before tax, or {usd(a/12)} a month.", body, faqs, HUB_W)

    # ---------- wage hub ----------
    hrows = "".join(f'<tr><td><a href="{hslug(h)}">{amt(h)} an hour</a></td><td>{usd0(h*2080)}</td><td>{usd(h*2080/12)}</td></tr>' for h in HOURLY)
    arows = "".join(f'<tr><td><a href="{aslug(a)}">{usd0(a)} a year</a></td><td>{usd(a/2080)}</td><td>{usd(a/12)}</td></tr>' for a in ANNUAL)
    write("/salary-conversions/", head("Hourly Wage to Salary Conversion Chart | Numbrik", "Chart of hourly wages from $10 to $60 an hour as yearly salaries, and salaries from $30,000 to $150,000 as hourly rates. Full time, 40 hours a week.", "/salary-conversions/", ld("/salary-conversions/", "Salary conversions", None)) +
          crumbs([("Home", "/"), ("Salary conversions", None)]) + f"""<main id="content" class="wrap page wide"><h1>Hourly wage to salary chart</h1>
<p class="lede">Full-time figures at 40 hours a week for 52 weeks (2,080 hours), before tax. Pick a wage for monthly, biweekly and after-tax figures, or use the <a href="/hourly-to-salary-calculator/">hourly to salary calculator</a> for any amount.</p>
<div class="twocol"><div><h2>Hourly to yearly</h2><div class="tbl"><table><thead><tr><th>Hourly</th><th>Yearly</th><th>Monthly</th></tr></thead><tbody>{hrows}</tbody></table></div></div>
<div><h2>Yearly to hourly</h2><div class="tbl"><table><thead><tr><th>Salary</th><th>Hourly</th><th>Monthly</th></tr></thead><tbody>{arows}</tbody></table></div></div></div></main>""" + footer())
    urls.append("/salary-conversions/")
    return urls

def build_countdowns(g):
    head, footer, write, DOMAIN, TODAY_TXT = g["head"], g["footer"], g["write"], g["DOMAIN"], g["TODAY_TXT"]
    today = date.fromisoformat(g["TODAY"]); urls = []
    for k, slug, name, rule in HOLS:
        nd = hol_date(k, today.year)
        if nd < today: nd = hol_date(k, today.year + 1)
        n = (nd - today).days
        yrs = "".join(f"<tr><td>{y}</td><td>{fmt(hol_date(k, y))}</td></tr>" for y in range(today.year, today.year + 6))
        disp = name[0].upper() + name[1:]
        path = f"/{slug}/"
        faqs = [(f"What day is {name} {nd.year}?", f"{disp} {nd.year} is on {fmt(nd)}."),
                (f"How many weeks until {name}?", f"Divide the days by 7. The countdown at the top of this page shows the exact number of weeks and days, and updates every day."),
                (f"How many sleeps until {name}?", f"The number of sleeps is the same as the number of days shown in the countdown, because you sleep once each night before the day arrives.")]
        def nxt(kk):
            d = hol_date(kk, today.year)
            return d if d >= today else hol_date(kk, today.year + 1)
        soon = sorted((x for x in HOLS if x[0] != k), key=lambda x: nxt(x[0]))[:6]
        others = "".join(f'<a class="card" href="/{s}/"><small>{COUNTRY.get(kk, "")}</small><b>{E(nm[0].upper()+nm[1:])}</b><span><span class="cd-mini" data-countdown="{kk}">{(nxt(kk)-today).days}</span> days</span></a>' for kk, s, nm, _ in soon) + '<a class="card" href="/countdowns/"><b>All countdowns</b><span>{} holidays</span></a>'.format(len(HOLS))
        body = f"""<div class="answer cd" data-countdown="{k}"><span class="label">Days until {E(name)}</span><div class="big"><em class="cd-days">{n}</em> <span class="cd-unit">days</span></div>
<p class="cd-live hint">{n} days to go</p><dl class="kv"><div><dt>Date</dt><dd class="cd-date">{fmt(nd)}</dd></div><div><dt>Weeks</dt><dd class="cd-weeks">{n//7} {"week" if n//7==1 else "weeks"}, {n%7} {"day" if n%7==1 else "days"}</dd></div><div><dt>Weekdays (Mon–Fri)</dt><dd class="cd-wd">—</dd></div></dl></div>
<h2>When is {E(name)}?</h2><p>{E(rule)}</p>
<h2>{E(disp)} dates</h2><div class="tbl"><table><thead><tr><th>Year</th><th>Date</th></tr></thead><tbody>{yrs}</tbody></table></div>
<p>To count the days between any two dates, use the <a href="/days-between-dates/">days between dates calculator</a>.</p>
<h2>Other countdowns</h2><div class="cards">{others}</div>"""
        write(path, head(f"How Many Days Until {disp}? Live Countdown | Numbrik", f"Live countdown to {name}: how many days, weeks and hours are left, what day it falls on, and {disp} dates for the next six years.", path,
              {"@context": "https://schema.org", "@graph": [{"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"}, {"@type": "ListItem", "position": 2, "name": "Holiday countdowns", "item": DOMAIN + "/countdowns/"}, {"@type": "ListItem", "position": 3, "name": f"Days until {name}", "item": DOMAIN + path}]},
               {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}]}) +
              f'<nav class="wrap crumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li><li><a href="/countdowns/">Holiday countdowns</a></li><li aria-current="page">Days until {E(name)}</li></ol></nav>' +
              f'<main id="content" class="wrap page wide"><h1>How many days until {E(name)}?</h1><p class="lede">A live countdown that updates every second. {E(disp)} {nd.year} falls on {fmt(nd)}.</p>{body}' +
              '<h2>Frequently asked questions</h2><div class="faq">' + "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in faqs) + f'</div><p class="updated">Last reviewed {TODAY_TXT}.</p></main>' + footer())
        urls.append(path)
    cards = ""
    for k, slug, name, _ in sorted(HOLS, key=lambda x: ((hol_date(x[0], today.year) if hol_date(x[0], today.year) >= today else hol_date(x[0], today.year + 1)) - today).days):
        nd = hol_date(k, today.year)
        if nd < today: nd = hol_date(k, today.year + 1)
        cards += f'<a class="card" href="/{slug}/"><small>{nd:%b} {nd.day}{" · " + COUNTRY[k] if k in COUNTRY else ""}</small><b>{E(name[0].upper()+name[1:])}</b><span><span class="cd-mini" data-countdown="{k}">{(nd-today).days}</span> days to go</span></a>'
    write("/countdowns/", head("Holiday Countdowns – Days Until Christmas & More | Numbrik", "Live countdowns to Christmas, Halloween, Thanksgiving, New Year's Eve, Memorial Day, Labor Day, Canada Day, Boxing Day, Australia Day, daylight saving time and more.", "/countdowns/") +
          '<nav class="wrap crumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li><li aria-current="page">Holiday countdowns</li></ol></nav>' +
          f'<main id="content" class="wrap page wide"><h1>Holiday countdowns</h1><p class="lede">How many days until the next big day, soonest first. Each countdown updates live.</p><div class="cards">{cards}</div></main>' + footer())
    urls.append("/countdowns/")
    return urls
