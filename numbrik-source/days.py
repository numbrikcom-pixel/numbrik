"""'X days / weeks from today' pages (added October 24, 2026). Dates are computed live in the browser; build-time values are the fallback."""
import html
from datetime import date, timedelta
from more import MORE
from extra import HOLS, hol_date

E = html.escape
DAYS = [7, 10, 14, 15, 20, 21, 30, 45, 60, 90, 100, 120, 150, 180, 200, 365]
WEEKS = [2, 3, 4, 6, 8, 10, 12, 16, 20, 26, 52]
def slug(n, unit): return f"/{n}-{'days' if unit == 'd' else 'weeks'}-from-today/"
def fmt(d): return f"{d:%A}, {d:%B} {d.day}, {d.year}"
def add_biz(d, n):
    while n:
        d += timedelta(1)
        if d.weekday() < 5: n -= 1
    return d
USES = {7: "a one-week deadline, a 7-day free trial or a short notice period",
        10: "a 10-day forecast, a short return window or shipping estimates",
        14: "a 14-day return policy, a two-week notice period or a quarantine",
        15: "a mid-month deadline or a 15-day payment term",
        20: "a 20-day response deadline or a short project sprint",
        21: "a three-week course, a habit challenge or a 21-day payment term",
        30: "30-day return windows, free trials, notice periods and net-30 invoices",
        45: "net-45 payment terms, a 45-day notice or a renewal reminder",
        60: "60-day notice periods, net-60 invoices and probation periods",
        90: "90-day probation periods, visa-free stays, warranties and net-90 terms",
        100: "a 100-day challenge, a school countdown or a product guarantee",
        120: "a four-month deadline, a passport renewal reminder or a lease notice",
        150: "a five-month project or a medical follow-up",
        180: "six-month reviews, the 90/180-day travel rule and medical follow-ups",
        200: "a long-term goal or project deadline",
        365: "a full year from today, an annual renewal or a one-year anniversary"}
MORE["days"] = MORE.get("days", "") + """<h2>Days from today</h2><p>Need the date a set number of days ahead? See <a href="/30-days-from-today/">30 days from today</a>, <a href="/60-days-from-today/">60 days</a>, <a href="/90-days-from-today/">90 days</a>, <a href="/180-days-from-today/">180 days</a> or <a href="/days-from-today/">any number of days</a>.</p>"""


def hol_list(today, target, days):
    items = []
    for k, slug, name, _ in HOLS:
        nd = hol_date(k, today.year)
        if nd <= today: nd = hol_date(k, today.year + 1)
        inside = nd <= target
        items.append((nd, f'<li data-hk="{k}"{"" if inside else " hidden"}><a href="/{slug}/">{E(name[0].upper()+name[1:])}</a> <span class="afd-hd">{nd:%b} {nd.day}</span></li>'))
    items.sort()
    return f'<h2>Holidays in the next {days} days</h2><ul class="afd-hols" data-add="{days}">' + "".join(x for _, x in items) + '</ul><p class="hint afd-none" hidden>No major holidays fall in this period.</p>'

def build_days(g):
    head, footer, write, DOMAIN, TODAY_TXT = g["head"], g["footer"], g["write"], g["DOMAIN"], g["TODAY_TXT"]
    today = date.fromisoformat(g["TODAY"]); urls = []
    items = [(n, "d") for n in DAYS] + [(n, "w") for n in WEEKS]
    for idx, (n, unit) in enumerate(items):
        days = n if unit == "d" else n * 7
        label = f"{n} days" if unit == "d" else f"{n} weeks"
        target = today + timedelta(days); ago = today - timedelta(days); biz = add_biz(today, days)
        path = slug(n, unit)
        same = [x for x in items if x[1] == unit]; i = same.index((n, unit))
        prev = same[i - 1] if i else None; nxt = same[i + 1] if i + 1 < len(same) else None
        nav = " · ".join(x for x in [f'<a href="{slug(*prev)}">← {prev[0]} {"days" if unit=="d" else "weeks"}</a>' if prev else "", '<a href="/days-from-today/">Any number of days</a>', f'<a href="{slug(*nxt)}">{nxt[0]} {"days" if unit=="d" else "weeks"} →</a>' if nxt else ""] if x)
        weeks_line = f"{days // 7} weeks and {days % 7} {'day' if days % 7 == 1 else 'days'}" if days % 7 else f"exactly {days // 7} weeks"
        use = USES.get(n, f"a deadline {label} away") if unit == "d" else f"a {label} plan, pregnancy milestones, a training block or a project timeline"
        faqs = [(f"What date is {label} from today?", f"The box at the top of this page shows the exact date and updates automatically each day. Today is not counted: day 1 is tomorrow."),
                (f"How many {'weeks' if unit == 'd' else 'days'} is {label}?", f"{label.capitalize()} is {weeks_line}." if unit == "d" else f"{label.capitalize()} is {days} days."),
                (f"What is {days} business days from today?", f"Counting Monday to Friday only, {days} business days from today is shown in the box above. Public holidays are not removed, so a deadline can move later if a holiday falls in between.")]
        body = f"""<div class="answer afd" data-add="{days}"><span class="label">{E(label)} from today</span><div class="big"><em class="afd-date">{fmt(target)}</em></div>
<p class="hint afd-from">Counting from today, {fmt(today)}</p>
<dl class="kv"><div><dt>Short date</dt><dd class="afd-short">{target:%m/%d/%Y}</dd></div><div><dt>{days} business days from today</dt><dd class="afd-biz">{fmt(biz)}</dd></div><div><dt>{E(label)} ago</dt><dd class="afd-ago">{fmt(ago)}</dd></div><div><dt>In weeks</dt><dd>{weeks_line}</dd></div></dl></div>
{hol_list(today, target, days)}
<h2>How it's counted</h2><p>Today is day 0, tomorrow is day 1, and the date above is day {days}. That's how most deadlines, return windows and notice periods are counted. If a rule says to include today, take one day off the result. The business-day date skips Saturdays and Sundays but not public holidays.</p>
<p>People look up {E(label)} from today for {E(use)}. For legal, visa or contract deadlines, check how the rule counts days, since some count calendar days and others count working days.</p>
<p>To count between any two dates, use the <a href="/days-between-dates/">days between dates calculator</a>. For a different number of days, use the <a href="/days-from-today/">days from today calculator</a>.</p>
<p class="pager">{nav}</p>"""
        title = f"What Date Is {label.title()} From Today? | Numbrik"
        meta = f"Find the date {label} from today, updated daily. Also shows {days} business days from today and the date {label} ago."
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"}, {"@type": "ListItem", "position": 2, "name": "Days from today", "item": DOMAIN + "/days-from-today/"}, {"@type": "ListItem", "position": 3, "name": f"{label} from today", "item": DOMAIN + path}]},
            {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}]}
        write(path, head(title, meta, path, ld) +
              f'<nav class="wrap crumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li><li><a href="/days-from-today/">Days from today</a></li><li aria-current="page">{E(label)} from today</li></ol></nav>' +
              f'<main id="content" class="wrap page wide"><h1>What date is {E(label)} from today?</h1><p class="lede">The date {E(label)} after today, worked out live from your device\'s calendar.</p>{body}' +
              '<h2>Frequently asked questions</h2><div class="faq">' + "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in faqs) + f'</div><p class="updated">Last reviewed {TODAY_TXT}.</p></main>' + footer())
        urls.append(path)
    links_d = "".join(f'<a class="card" href="{slug(n,"d")}"><b>{n} days from today</b><span class="afd-mini" data-add="{n}">{fmt(today + timedelta(n))}</span></a>' for n in DAYS)
    links_w = "".join(f'<a class="card" href="{slug(n,"w")}"><b>{n} weeks from today</b><span class="afd-mini" data-add="{n*7}">{fmt(today + timedelta(n*7))}</span></a>' for n in WEEKS)
    write("/days-from-today/", head("Days From Today Calculator – Add Days to Today | Numbrik",
          "Add any number of days or weeks to today's date. See the date 30, 60, 90 or 180 days from today, business days and days ago.", "/days-from-today/") +
          '<nav class="wrap crumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li><li aria-current="page">Days from today</li></ol></nav>' +
          f"""<main id="content" class="wrap page wide"><h1>Days from today calculator</h1><p class="lede">Type a number of days to see the date that many days from today, the business-day date and the date that many days ago.</p>
<div class="answer" id="afdTool"><div class="row"><div class="field"><label for="afdN">Number of days</label><input id="afdN" type="number" value="30" step="1" inputmode="numeric"></div><div class="field"><label for="afdU">Unit</label><select id="afdU"><option value="1">Days</option><option value="7">Weeks</option></select></div></div>
<span class="label">Date</span><div class="big"><em id="afdOut">{fmt(today + timedelta(30))}</em></div><dl class="kv"><div><dt>Business days from today</dt><dd id="afdBiz">{fmt(add_biz(today, 30))}</dd></div><div><dt>Days ago</dt><dd id="afdAgo">{fmt(today - timedelta(30))}</dd></div></dl></div>
<h2>Days from today</h2><div class="cards">{links_d}</div><h2>Weeks from today</h2><div class="cards">{links_w}</div></main>""" + footer())
    urls.append("/days-from-today/")
    return urls
