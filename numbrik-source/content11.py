"""Second batch from calculator.net's sitemap gap (November 8, 2026): gravel, stairs, period/ovulation, love, RMD,
rounding and time zones. RMD factors: IRS Uniform Lifetime Table (Pub. 590-B, Appendix B, Table III, in force since 2022).
RMD start ages per SECURE 2.0: 73 for people born 1951–1959, 75 for 1960 or later. Stair limits: IRC R311.7."""
import math
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from content import tool, T, BYID

def tbl(head, rows):
    return ('<div class="tbl"><table><thead><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")

# ---------- Gravel ----------
tool(id="gravel", slug="gravel-calculator", cat="Home", name="Gravel Calculator",
 short="Gravel calculator", desc="Cubic yards and tons of gravel, stone or sand.",
 title="Gravel Calculator – Cubic Yards & Tons Needed | Numbrik",
 meta="How much gravel do you need? Enter length, width and depth to get cubic yards, tons and bags of gravel, crushed stone, pea gravel, river rock or sand.",
 lede="Work out how much gravel, crushed stone or sand to order for a driveway, path or patio. Enter the area and depth, pick the material, and get the amount in cubic yards, tons and bags.",
 steps=["Measure the length and width of the area.", "Enter how deep you want the gravel.", "Pick the material so the weight is right.", "Order the cubic yards or tons shown. Suppliers sell by one or the other."],
 how="""<p>The volume is length × width × depth. With feet and inches, that's length (ft) × width (ft) × depth (in) ÷ 12 to get cubic feet, then ÷ 27 for cubic yards. To get the weight, multiply cubic yards by the material's density. Typical gravel weighs about 1.4 tons per cubic yard (2,800 lb), crushed stone a little less, and topsoil about 1.1 tons.</p>
<p>Gravel settles and spreads at the edges, so order 5–10% extra. For a driveway, lay 4–6 inches in layers: a base of larger crushed stone, then a top layer of smaller gravel. For paths, 2 inches over landscape fabric is usually enough.</p>""",
 formula="Cubic yards = length (ft) × width (ft) × depth (in) ÷ 12 ÷ 27\nTons = cubic yards × density (≈ 1.4 for gravel)\nCubic metres = length (m) × width (m) × depth (cm) ÷ 100",
 example="<p>A <strong>40 × 12 ft</strong> driveway, <strong>4 inches</strong> deep: 40 × 12 × 4 ÷ 12 = 160 cubic feet, ÷ 27 = <strong>5.93 cubic yards</strong>. At 1.4 tons per yard that's about <strong>8.3 tons</strong> of gravel.</p>",
 extra="<h3>Gravel needed per 100 square feet</h3>" + tbl(["Depth", "Cubic yards", "Tons (gravel, 1.4 t/yd³)", "50 lb bags"],
   [(f"{d} in", f"{100 * d / 12 / 27:.2f}", f"{100 * d / 12 / 27 * 1.4:.2f}", math.ceil(100 * d / 12 / 27 * 2800 / 50)) for d in (1, 2, 3, 4, 5, 6, 8, 12)]) +
 "<h3>Common gravel types</h3>" + tbl(["Material", "Size", "Good for"], [("Pea gravel", "3/8 in, rounded", "Paths, play areas, patios"), ("Crushed stone #57", "3/4–1 in, angular", "Driveway base, drainage"), ("Crushed stone #411 / crusher run", "Mixed with fines", "Compacted driveway and patio base"), ("River rock", "1–3 in, smooth", "Borders, dry creek beds"), ("Decomposed granite", "Fine, sandy", "Paths and xeriscaping")]),
 faqs=[("How many tons is a cubic yard of gravel?", "About 1.4 tons (2,800 lb) for typical gravel, but it ranges from about 1.3 to 1.7 tons depending on the stone and how wet it is. Ask your supplier for their figure."),
       ("How much area does a ton of gravel cover?", "At 2 inches deep, one ton covers roughly 115 square feet. At 4 inches deep it covers about 58 square feet."),
       ("How deep should gravel be for a driveway?", "4 to 6 inches for a new gravel driveway, laid in two or three compacted layers. Top up an existing driveway with 2 inches."),
       ("Is it cheaper to buy gravel in bags or in bulk?", "Bulk is much cheaper above about one cubic yard. Bags (usually 0.5 cu ft or 50 lb) are handy for small jobs and places a truck can't reach.")],
 related=["mulch", "concrete", "sqft", "tile"])

# ---------- Stairs ----------
def stair(rise, tread=10.5, mx=7.75):
    n = math.ceil(rise / mx - 1e-9); return n, rise / n, (n - 1) * tread
tool(id="stair", slug="stair-calculator", cat="Home", name="Stair Calculator",
 short="Stair calculator", desc="Number of steps, riser height, run and stringer length.",
 title="Stair Calculator – Steps, Rise, Run & Stringers | Numbrik",
 meta="Plan a staircase: enter the total rise to get the number of steps, riser height, total run, stringer length and angle, checked against US building code limits.",
 lede="Plan stairs for a deck, basement or loft. Enter the total rise from floor to floor and your tread depth, and the calculator works out how many steps you need, the exact riser height, the total run and the stringer length.",
 steps=["Measure the total rise: from the lower floor to the top of the upper floor, in one straight vertical line.", "Enter your tread depth and the maximum riser height allowed.", "Read the number of risers and treads, the riser height and the total run.", "Use the stringer length to buy lumber: add a foot or so for cuts."],
 how="""<p>The number of risers is the total rise divided by the maximum riser height, rounded up. Dividing the rise by that whole number gives the equal riser height every step needs. There is always one fewer tread than risers, because the top floor acts as the last step. The total run is treads × tread depth, and the stringer length follows from Pythagoras: √(rise² + run²).</p>
<p>The US International Residential Code (IRC) limits risers to 7¾ inches and requires treads of at least 10 inches, at least 6 ft 8 in of headroom, and risers within ⅜ inch of each other. A common comfort rule is 2 × riser + tread = 24 to 25 inches. Commercial stairs (IBC) are stricter: 7-inch maximum risers and 11-inch treads.</p>""",
 formula="Risers = ⌈total rise ÷ max riser⌉\nRiser height = total rise ÷ risers\nTreads = risers − 1\nTotal run = treads × tread depth\nStringer ≈ √(rise² + run²)",
 example=f"<p>A basement with a <strong>108-inch</strong> rise (9 ft): 108 ÷ 7.75 = 13.9, so <strong>14 risers</strong> of 108 ÷ 14 = <strong>7.71 in</strong>. That gives 13 treads; at 10.5 in each, the total run is 136.5 in (11 ft 4.5 in). The stringer is about {math.hypot(108, 136.5):.0f} in long.</p>",
 extra="<h3>Steps needed by total rise (7¾ in max riser, 10½ in treads)</h3>" + tbl(["Total rise", "Risers", "Riser height", "Treads", "Total run"],
   [(f"{r} in ({r // 12} ft {r % 12} in)", stair(r)[0], f"{stair(r)[1]:.2f} in", stair(r)[0] - 1, f"{stair(r)[2]:.1f} in") for r in (18, 24, 30, 36, 42, 48, 60, 72, 84, 96, 102, 108, 114, 120, 132, 144)]),
 faqs=[("How many steps do I need for 8 feet?", "A 96-inch rise needs 13 risers of about 7.38 inches, with 12 treads. At 10.5-inch treads the stairs run 126 inches (10.5 ft) horizontally."),
       ("What is the code for stair riser height?", "The IRC allows a maximum riser of 7¾ inches for homes, with risers in one flight varying by no more than ⅜ inch. Commercial buildings allow 7 inches."),
       ("How deep should stair treads be?", "At least 10 inches under the IRC, measured nose to nose. 10½ to 11 inches feels more comfortable, especially going down."),
       ("How do I measure total rise for deck stairs?", "Measure from the top of the deck surface straight down to the ground or landing where the stairs will end. If the ground slopes, measure at the point where the bottom step will land.")],
 related=["sqft", "concrete", "tile", "triangle"])

# ---------- Period ----------
tool(id="period", slug="period-calculator", cat="Health", name="Period & Ovulation Calculator",
 short="Period calculator", desc="Next period, ovulation day and fertile window.",
 title="Period Calculator – Next Period & Ovulation Date | Numbrik",
 meta="Predict your next period, ovulation day and fertile window from the date of your last period and your cycle length. See your next six cycles at a glance.",
 lede="Enter the first day of your last period and your usual cycle length to predict your next period, your ovulation day and your most fertile days, for the next six months.",
 steps=["Enter the first day of your last period (day 1 is the first day of real bleeding).", "Enter your average cycle length. Count from the first day of one period to the first day of the next.", "Enter how many days your period usually lasts.", "Read your next period date, ovulation estimate and fertile window."],
 how="""<p>Your next period is predicted by adding your cycle length to the start of your last period. Ovulation usually happens about 14 days before the next period starts, so in a 28-day cycle it falls around day 14, and in a 32-day cycle around day 18. The fertile window covers the five days before ovulation, the day itself and the day after, because sperm can survive up to five days.</p>
<p>Cycles change with stress, illness, travel, breastfeeding and age, so predictions get less reliable the further ahead they go. Ovulation tests, basal body temperature or cervical mucus give a more precise picture. This calculator must not be used as birth control.</p>""",
 formula="Next period = last period start + cycle length\nOvulation ≈ next period − 14 days\nFertile window = ovulation − 5 days to ovulation + 1 day",
 example="<p>Your last period started on <strong>November 1</strong> and your cycle is <strong>28 days</strong>. Your next period is due on <strong>November 29</strong>. Ovulation is around November 15, and your fertile window runs from November 10 to November 16.</p>",
 extra="<h3>Ovulation day by cycle length</h3>" + tbl(["Cycle length", "Ovulation (cycle day)", "Fertile window (cycle days)"],
   [(f"{c} days", f"Day {c - 14}", f"Days {c - 19}–{c - 13}") for c in range(21, 38)]) +
 "<h3>When to see a doctor</h3><p>Talk to a doctor or nurse if your cycles are often shorter than 21 days or longer than 35, your period lasts more than 7 days, it suddenly becomes irregular, you bleed between periods, or the pain stops you doing normal things. If you've been trying to get pregnant for a year (six months if you're 35 or older), it's also worth checking in.</p>",
 faqs=[("How do I calculate my next period?", "Add your cycle length to the first day of your last period. A 30-day cycle starting October 5 means your next period is due around November 4."),
       ("When am I most fertile?", "In the two to three days before ovulation and on ovulation day itself. For a 28-day cycle that's roughly days 12 to 14."),
       ("Is a 35-day cycle normal?", "Yes. Adult cycles between 21 and 35 days are considered normal. What matters more is a sudden change in your usual pattern."),
       ("Can I get pregnant on my period?", "It's unlikely but possible, especially with short cycles, because sperm can survive up to five days and you may ovulate soon after your period ends.")],
 related=["duedate", "water", "bmi", "days"])

# ---------- Love ----------
tool(id="love", slug="love-calculator", cat="Fun", name="Love Calculator",
 short="Love calculator", desc="A just-for-fun love percentage from two names.",
 title="Love Calculator – Test Your Love Percentage | Numbrik",
 meta="Enter two names to get a love compatibility percentage. A fun love test for you and your crush, partner or friends. Same names, same result every time.",
 lede="Type your name and your crush's name to get a love percentage. It's a party game, not science, but the same two names always get the same score, so you can't just keep pressing until you win.",
 steps=["Type your name.", "Type the other person's name.", "Read your love percentage and what it means.", "Copy the result to share it with friends."],
 how="""<p>The score comes from the letters of both names, sorted so it doesn't matter whose name goes first. The letters are fed through a hash, a formula that scrambles text into a number, and the number is turned into a percentage between 35% and 100%. Change one letter and the score changes completely, which is half the fun: try nicknames and full names.</p>
<p>Love calculators go back to the FLAMES game and to the “true love” test played with pen and paper in school, where you count the letters of TRUE and LOVE in both names. None of them can predict a relationship. Kindness, trust and shared values do that.</p>""",
 formula="score = 35 + (hash(sorted names) mod 66)\nSame two names → same score, in either order",
 example="<p>Type <strong>Alex</strong> and <strong>Sam</strong> and you'll always get the same score, whether Alex or Sam goes first. Try “Alexander” instead and the score changes.</p>",
 extra="<h3>What your score means</h3>" + tbl(["Score", "Verdict"], [("90–100%", "A match made in heaven"), ("75–89%", "Great chemistry"), ("60–74%", "Good potential"), ("45–59%", "Friends first"), ("35–44%", "Opposites attract… sometimes")]) +
 "<h3>Play the FLAMES game</h3><p>Write both names, cross out the letters they share, and count the letters left. Then count around the word FLAMES (Friends, Lovers, Affectionate, Marriage, Enemies, Siblings) by that number, crossing out the letter you land on, until one is left. That's your answer.</p>",
 faqs=[("Is the love calculator accurate?", "No. It's a game based on the letters in your names, so it can't know anything about a real relationship. Enjoy it, but don't take it seriously."),
       ("Why do I always get the same score?", "The result comes from the names themselves, so the same pair always gives the same percentage. It doesn't matter which name you type first."),
       ("Do you save the names I type?", "No. Everything happens in your browser. The names are never sent to us or stored."),
       ("What is the FLAMES game?", "A school game where you cancel the shared letters in two names and count the rest around the word FLAMES to find out if you'll be friends, lovers, married or enemies.")],
 related=["random", "coin", "dice", "age"])

# ---------- RMD ----------
U = {72: 27.4, 73: 26.5, 74: 25.5, 75: 24.6, 76: 23.7, 77: 22.9, 78: 22.0, 79: 21.1, 80: 20.2, 81: 19.4, 82: 18.5, 83: 17.7, 84: 16.8, 85: 16.0,
     86: 15.2, 87: 14.4, 88: 13.7, 89: 12.9, 90: 12.2, 91: 11.5, 92: 10.8, 93: 10.1, 94: 9.5, 95: 8.9, 96: 8.4, 97: 7.8, 98: 7.3, 99: 6.8, 100: 6.4}
tool(id="rmd", slug="rmd-calculator", cat="Money", name="RMD Calculator",
 short="RMD calculator", desc="Required minimum distribution from an IRA or 401(k).",
 title="Required Minimum Distribution (RMD) Calculator 2026",
 meta="Calculate your 2026 required minimum distribution (RMD) from an IRA or 401(k) with the IRS Uniform Lifetime Table, plus a 10-year projection.",
 lede="Work out how much you must withdraw from a traditional IRA, 401(k) or 403(b) this year. Enter your birth year and last year's December 31 balance to get your RMD, using the IRS Uniform Lifetime Table, and a 10-year projection.",
 steps=["Enter your year of birth.", "Enter the distribution year (this year).", "Enter the account balance on December 31 of last year: it's on your year-end statement.", "Read your RMD, the factor used and when it's due."],
 how="""<p>Your RMD is last year's December 31 balance divided by the distribution period for your age at the end of this year, from the IRS Uniform Lifetime Table. At 75 the factor is 24.6, so you withdraw about 4.07% of the balance. The factor shrinks every year, so the percentage rises.</p>
<p>Since the SECURE 2.0 Act, RMDs start at 73 if you were born from 1951 to 1959, and at 75 if you were born in 1960 or later. Your first RMD can wait until April 1 of the following year, but then you take two in one year. After that, each RMD is due by December 31. Missing one triggers a 25% excise tax on the shortfall, cut to 10% if you correct it within two years. Roth IRAs have no RMDs for the original owner, and Roth 401(k)s haven't needed them since 2024.</p>""",
 formula="RMD = balance on Dec 31 of the prior year ÷ distribution period\nDistribution period: IRS Uniform Lifetime Table, by age at year end",
 example=f"<p>You were born in <strong>1952</strong>, so you turn 74 in 2026. Your IRA held <strong>$500,000</strong> on December 31, 2025. The factor for age 74 is 25.5, so your 2026 RMD is 500,000 ÷ 25.5 = <strong>${500000 / 25.5:,.0f}</strong>, due by December 31, 2026.</p>",
 extra="<h3>IRS Uniform Lifetime Table</h3>" + tbl(["Age", "Factor", "% to withdraw", "Age", "Factor", "% to withdraw"],
   [(a, U[a], f"{100 / U[a]:.2f}%", a + 15, U[a + 15], f"{100 / U[a + 15]:.2f}%") for a in range(72, 87) if a + 15 <= 100]) +
 "<h3>When do RMDs start?</h3>" + tbl(["Born", "RMD age", "First RMD year"], [("1950 or earlier", "72 (or 70½ if born before July 1, 1949)", "Already started"), ("1951–1959", "73", "The year you turn 73"), ("1960 or later", "75", "The year you turn 75")]),
 faqs=[("At what age do I have to take an RMD?", "73 if you were born between 1951 and 1959, and 75 if you were born in 1960 or later."),
       ("What happens if I miss an RMD?", "The IRS charges a 25% excise tax on the amount you should have taken. It drops to 10% if you take the missed amount and file a corrected return within two years."),
       ("Do Roth IRAs have RMDs?", "Not for the original owner. Since 2024, Roth 401(k) and 403(b) accounts don't need RMDs during the owner's lifetime either. Inherited Roth accounts have their own rules."),
       ("Can I take my RMD from just one account?", "For IRAs, yes: work out each IRA's RMD, then withdraw the total from any of them. 401(k) RMDs must come from each 401(k) separately.")],
 related=["compound", "cd", "simpleint", "salary"])

# ---------- Rounding ----------
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
def rd(x, q, m=ROUND_HALF_UP): return str(Decimal(str(x)).quantize(Decimal(q), rounding=m))
tool(id="rounding", slug="rounding-calculator", cat="Math", name="Rounding Calculator",
 short="Rounding calculator", desc="Round a number to any place, any method.",
 title="Rounding Calculator – Nearest Tenth & Hundredth | Numbrik",
 meta="Round any number to the nearest whole number, ten, hundred, tenth, hundredth or thousandth. Choose half up, half to even (banker's), ceiling, floor or truncate.",
 lede="Round a number to the nearest whole number, ten, hundred, tenth, hundredth or thousandth, and see it rounded to every place at once. You can also pick the rounding rule: half up, banker's rounding, always up, always down or truncate.",
 steps=["Type the number to round.", "Choose the place to round to.", "Choose the rounding method (half up is what schools teach).", "Read the result, plus the number rounded to every other place."],
 how="""<p>To round, look at the digit just to the right of the place you're rounding to. If it's 5 or more, round up; if it's 4 or less, keep the digit and drop the rest. 3.14159 to the nearest hundredth: the hundredths digit is 4 and the next digit is 1, so it becomes 3.14. To the nearest tenth, the next digit is 4, so it's 3.1.</p>
<p>Half to even (banker's rounding) sends exact halves to the nearest even digit, so 2.5 becomes 2 and 3.5 becomes 4. It avoids an upward bias when you round lots of numbers, which is why accountants and many computer languages use it. Ceiling always rounds up, floor always rounds down, and truncating just chops off the extra digits.</p>""",
 formula="Look at the next digit to the right:\n0–4 → round down (keep the digit)\n5–9 → round up (add 1 to the digit)",
 example="<p><strong>2,746.385</strong> rounds to 2,746.39 (hundredths), 2,746.4 (tenths), 2,746 (whole number), 2,750 (tens) and 2,700 (hundreds). With banker's rounding, 2,746.385 to the hundredth still gives 2,746.38, because 8 is even.</p>",
 extra="<h3>Rounding examples</h3>" + tbl(["Number", "Nearest whole", "Tenth", "Hundredth", "Nearest ten"],
   [(x, rd(x, "1"), rd(x, "0.1"), rd(x, "0.01"), str(int(Decimal(str(x)).quantize(Decimal("1E1"), rounding=ROUND_HALF_UP)))) for x in (3.14159, 2.71828, 12.345, 0.666, 45.5, 99.951, 127.4949, 1.005, 68.75, 249.996)]) +
 "<h3>Half up vs half to even</h3>" + tbl(["Number", "Half up", "Half to even"], [(x, rd(x, "1"), rd(x, "1", ROUND_HALF_EVEN)) for x in (0.5, 1.5, 2.5, 3.5, 4.5, -2.5)]),
 faqs=[("How do you round to the nearest tenth?", "Look at the hundredths digit (the second after the decimal point). If it's 5 or more, add 1 to the tenths digit; otherwise leave it. 4.36 rounds to 4.4 and 4.34 rounds to 4.3."),
       ("What is 0.5 rounded to the nearest whole number?", "1 with the usual half-up rule. With banker's rounding it's 0, because 0 is the nearest even number."),
       ("How do you round negative numbers?", "Half up here means half away from zero, so −2.5 becomes −3. Floor always goes down, so −2.1 becomes −3; ceiling always goes up, so −2.9 becomes −2."),
       ("What's the difference between rounding and truncating?", "Rounding picks the nearest value; truncating simply cuts off the extra digits. 7.89 rounds to 7.9 but truncates to 7.8.")],
 related=["scientific", "fraction", "percent", "longdiv"])

# ---------- Time zones ----------
REF = datetime(2026, 11, 9, 17, 0, tzinfo=timezone.utc)  # 9 AM PST / 12 PM EST on a Monday, after US DST ends
ZN = [("America/Los_Angeles", "Pacific (PT)"), ("America/Denver", "Mountain (MT)"), ("America/Chicago", "Central (CT)"), ("America/New_York", "Eastern (ET)"),
      ("Europe/London", "London (GMT)"), ("Europe/Paris", "Paris / Berlin (CET)"), ("Asia/Dubai", "Dubai (GST)"), ("Asia/Kolkata", "India (IST)"), ("Asia/Tokyo", "Tokyo (JST)"), ("Australia/Sydney", "Sydney (AEDT)")]
def at(utc_hour, z):
    t = datetime(2026, 11, 9, utc_hour % 24, 0, tzinfo=timezone.utc).astimezone(ZoneInfo(z)); return t.strftime("%-I %p").replace("AM", "AM").lstrip("0")
tool(id="timezone", slug="time-zone-converter", cat="Dates & time", name="Time Zone Converter",
 short="Time zone converter", desc="Convert a time between US and world time zones.",
 title="Time Zone Converter – EST, PST, IST, GMT & More | Numbrik",
 meta="Convert a time between US and world time zones: EST, CST, PST, GMT, IST, CET, JST and more. Daylight saving time is applied automatically for the date.",
 lede="Convert a time from one time zone to another, for meetings, calls, flights and live events. Pick a date and time, choose the two zones, and get the converted time, the difference, and the time in eight major cities.",
 steps=["Pick the date and time you want to convert.", "Choose the time zone it's in (From).", "Choose the time zone to convert to (To).", "Read the converted time, the day, and the time difference."],
 how="""<p>Every time zone is an offset from Coordinated Universal Time (UTC). The converter turns your time into UTC using the first zone's offset on that date, then into the second zone. It uses your browser's time zone database, so daylight saving time is handled automatically, including the weeks in March and autumn when the US and Europe change clocks on different dates.</p>
<p>In 2026, US daylight saving time ran from March 8 to November 1; in 2027 it runs from March 14 to November 7. The UK and EU switch on the last Sundays of March and October. India, China, Japan, Arizona and Hawaii don't use daylight saving time, so their difference from New York changes by an hour twice a year.</p>""",
 formula="UTC time = local time − zone offset\nTarget time = UTC time + target offset\nExample offsets: EST = UTC−5, PST = UTC−8, IST = UTC+5:30",
 example="<p>A call at <strong>9:00 AM Pacific</strong> on Monday, November 9, 2026 is 12:00 PM Eastern, 5:00 PM in London and <strong>10:30 PM in India</strong>. In summer, while the US is on daylight time, the same 9:00 AM PDT call would be 9:30 PM in India.</p>",
 extra="<h3>Time zone chart (Monday, November 9, 2026)</h3>" + tbl([n for _, n in ZN[:4]] + ["London", "India", "Tokyo"],
   [[datetime(2026, 11, 9, h, 0, tzinfo=timezone.utc).astimezone(ZoneInfo(z)).strftime("%-I:%M %p") for z in [x[0] for x in ZN[:4]] + ["Europe/London", "Asia/Kolkata", "Asia/Tokyo"]] for h in range(12, 24, 1)] + [[datetime(2026, 11, 10, h, 0, tzinfo=timezone.utc).astimezone(ZoneInfo(z)).strftime("%-I:%M %p") for z in [x[0] for x in ZN[:4]] + ["Europe/London", "Asia/Kolkata", "Asia/Tokyo"]] for h in range(0, 4)]) +
 "<h3>Common conversions (standard time)</h3>" + tbl(["From", "To", "Difference"], [("EST", "PST", "PST is 3 hours behind"), ("EST", "CST", "CST is 1 hour behind"), ("EST", "GMT", "GMT is 5 hours ahead"), ("EST", "IST", "IST is 10½ hours ahead"), ("PST", "IST", "IST is 13½ hours ahead"), ("GMT", "CET", "CET is 1 hour ahead"), ("EST", "JST", "JST is 14 hours ahead"), ("PST", "AEDT", "AEDT is 19 hours ahead")]),
 faqs=[("What time is 12 PM EST in PST?", "9 AM PST. Pacific time is three hours behind Eastern time all year, because both switch to daylight time on the same dates."),
       ("How many hours ahead is India from the US?", "India (IST, UTC+5:30) is 10½ hours ahead of Eastern Standard Time and 13½ hours ahead of Pacific Standard Time. During US daylight time the gaps are 9½ and 12½ hours."),
       ("Is GMT the same as UTC?", "For everyday use, yes: both are UTC+0. UTC is the scientific standard; GMT is also the UK's winter time zone. In summer the UK uses BST (UTC+1)."),
       ("What's the difference between EST and EDT?", "EST (UTC−5) is Eastern Standard Time, used in winter. EDT (UTC−4) is Eastern Daylight Time, used from March to November. Many people just say ET.")],
 related=["military", "hours", "days", "age"])

BYID.update({t["id"]: t for t in T})
