"""Low-competition calculators picked from OpenRush SERP checks (November 1, 2026):
half birthday, military time, pay raise, water intake, mulch and working days in a year."""
import calendar
from datetime import date, timedelta
from content import tool, T, BYID

def tbl(head, rows):
    return ('<div class="tbl"><table><thead><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")

# ---------- US federal holidays (observed) ----------
def nth(y, m, dow, n):
    d = date(y, m, 1); return d + timedelta(((dow - d.weekday()) % 7) + 7 * (n - 1))
def last(y, m, dow):
    d = date(y, m, calendar.monthrange(y, m)[1]); return d - timedelta((d.weekday() - dow) % 7)
def obs(d):
    return d - timedelta(1) if d.weekday() == 5 else d + timedelta(1) if d.weekday() == 6 else d
def fed(y):
    hs = [obs(date(y, 1, 1)), nth(y, 1, 0, 3), nth(y, 2, 0, 3), last(y, 5, 0), obs(date(y, 6, 19)), obs(date(y, 7, 4)),
          nth(y, 9, 0, 1), nth(y, 10, 0, 2), obs(date(y, 11, 11)), nth(y, 11, 3, 4), obs(date(y, 12, 25)), obs(date(y + 1, 1, 1))]
    return sorted({d for d in hs if d.year == y and d.weekday() < 5})
def wdays(y, m=None):
    ms = [m] if m else range(1, 13)
    return sum(1 for mm in ms for dd in range(1, calendar.monthrange(y, mm)[1] + 1) if date(y, mm, dd).weekday() < 5)
def work(y, m=None):
    return wdays(y, m) - sum(1 for d in fed(y) if m is None or d.month == m)

# ---------- Half birthday ----------
def half(b):
    m = b.month + 6; y = b.year + (m > 12); m = m - 12 if m > 12 else m
    return date(y, m, min(b.day, calendar.monthrange(y, m)[1]))
tool(id="halfbday", slug="half-birthday-calculator", cat="Dates & time", name="Half Birthday Calculator",
 short="Half birthday", desc="Find your half birthday and days until it.",
 title="Half Birthday Calculator – When Is My Half Birthday?",
 meta="When is your half birthday? Enter your birthday to get the date exactly six months later, how many days until it, and how old you'll be.",
 lede="Your half birthday is the day exactly six months after your birthday. Enter your date of birth to see when your next half birthday is, how many days are left, and how old you'll be (and a half).",
 steps=["Enter your date of birth.", "Read your next half birthday and the countdown in days.", "See your half birthday every year in the list underneath."],
 how="""<p>The calculator adds six calendar months to your birthday. Someone born on March 10 has a half birthday on September 10. If the date doesn't exist six months later, it moves to the last day of that month: August 29, 30 and 31 birthdays have half birthdays on February 28, or February 29 in a leap year.</p>
<p>Some people count 182 or 183 days instead, which can land a day or two away from the calendar method. The six-month calendar date is the one most people use for parties and milestones.</p>""",
 formula="Half birthday = birthday + 6 calendar months\nIf that day doesn't exist, use the last day of the month",
 example=f"<p>Born on <strong>March 10</strong>, your half birthday is <strong>September 10</strong>. Born on August 31, your half birthday is February 28 (February 29 in a leap year such as 2028).</p>",
 extra="<h3>Half birthday by birth month</h3>" + tbl(["Birthday", "Half birthday"], [(f"{calendar.month_name[m]} {d}", f"{calendar.month_name[half(date(2025, m, d)).month]} {half(date(2025, m, d)).day}") for m, d in [(1, 15), (2, 14), (3, 10), (4, 1), (5, 20), (6, 30), (7, 4), (8, 31), (9, 9), (10, 31), (11, 15), (12, 25)]]) +
 "<h3>Ideas for celebrating</h3><p>Half birthdays are popular for babies (the six-month milestone photo), for children whose real birthday falls in the school holidays so they can celebrate with classmates, and for people born near Christmas who want a party in summer. A half cake, half a gift or a six-month photo are classic touches.</p>",
 faqs=[("When is my half birthday?", "Six calendar months after your birthday. A January 20 birthday has a half birthday on July 20."),
       ("What if I was born on August 31?", "There's no February 31, so your half birthday is the last day of February: the 28th, or the 29th in a leap year."),
       ("Is a half birthday 182 days?", "Half a year is about 182.6 days, but most people simply use the same date six months later."),
       ("Why do people celebrate half birthdays?", "Kids with summer or holiday birthdays often celebrate at school on their half birthday, and parents mark a baby's six-month milestone.")],
 related=["age", "days", "duedate", "workdays"])

# ---------- Military time ----------
def mil(h):
    s = f"{h % 12 or 12}:00 {'AM' if h < 12 else 'PM'}"
    return (s, f"{h:02d}00", f"{h:02d}:00")
tool(id="military", slug="military-time-converter", cat="Dates & time", name="Military Time Converter",
 short="Military time converter", desc="Convert 24-hour military time to AM/PM and back.",
 title="Military Time Converter & 24-Hour Chart | Numbrik",
 meta="Convert military time to standard AM/PM time and back. Type 1830 or 6:30 PM to convert instantly, with a full 24-hour military time chart.",
 lede="Convert military time (the 24-hour clock) to standard 12-hour time with AM and PM, or the other way round. Type a time in either box, or use the 24-hour chart below.",
 steps=["Type a military time such as 1830 or 0745 in the first box, or a standard time such as 6:30 PM in the second.",
        "Read the converted time underneath.", "Use the chart to look up any hour at a glance."],
 how="""<p>Military time numbers the hours of the day from 00 to 23, so there's no need for AM or PM. It's written as four digits without a colon, such as 0700 or 1930, and said as "oh seven hundred" or "nineteen thirty". It's used by the armed forces, hospitals, airlines, emergency services and most countries outside the US.</p>
<p>From 1:00 PM onwards, add 12 to the hour to get military time: 3:15 PM is 1515. To go back, subtract 12 from any hour of 13 or more: 2145 is 9:45 PM. Midnight is 0000 and noon is 1200.</p>""",
 formula="PM hours (1–11 PM):  military = hour + 12\nMilitary 1300–2359:   standard = hour − 12, PM\n12:00 AM = 0000      12:00 PM = 1200",
 example="<p>6:30 PM is 6 + 12 = 18, so it's <strong>1830</strong>. Military 0545 is <strong>5:45 AM</strong>, and 2215 is 22 − 12 = <strong>10:15 PM</strong>.</p>",
 extra="<h3>24-hour military time chart</h3>" + tbl(["Standard time", "Military time", "24-hour clock"], [mil(h) for h in range(24)]),
 faqs=[("What is 1700 in military time?", "1700 is 5:00 PM. Subtract 12 from 17 to get 5."),
       ("How do you say 0000 in military time?", "Midnight is \"zero hundred\" or \"twenty-four hundred\". Most systems use 0000 for the start of the day."),
       ("Is 2400 a valid military time?", "It's sometimes used for the end of a day, as in 0800–2400, but 0000 is the usual way to write midnight."),
       ("Do you use a colon in military time?", "Not usually. The military writes 1430. The 24-hour clock used in everyday life elsewhere often adds a colon: 14:30.")],
 related=["hours", "timecard", "workdays", "halfbday"])

# ---------- Pay raise ----------
tool(id="raise", slug="pay-raise-calculator", cat="Work & pay", name="Pay Raise Calculator",
 short="Pay raise", desc="New pay after a raise, or the raise percentage.",
 title="Pay Raise Calculator – Salary Increase % | Numbrik",
 meta="Enter your pay and a raise as a percent or dollar amount to see your new hourly, weekly, monthly and yearly pay, or find your raise percentage.",
 lede="See your new pay after a raise. Enter your current hourly wage or salary and the raise as a percentage or an amount, or enter your old and new pay to find the raise percentage.",
 steps=["Choose whether you know the raise percent, the raise amount, or your new pay.", "Enter your current pay and whether it's hourly or yearly.",
        "Read your new pay per hour, week, month and year, and how much more you'll earn."],
 how="""<p>A percentage raise multiplies your pay by one plus the percentage: a 4% raise on $50,000 is $50,000 × 1.04 = $52,000. A flat raise simply adds the amount. To find the raise percentage from old and new pay, divide the difference by the old pay.</p>
<p>Hourly and yearly figures assume 40 hours a week for 52 weeks (2,080 hours). The extra pay is before tax, so the increase in your paycheck will be smaller. Compare your raise with inflation: if prices rose 3% over the year, a 3% raise keeps your buying power level.</p>""",
 formula="New pay = old pay × (1 + raise% ÷ 100)\nRaise % = (new pay − old pay) ÷ old pay × 100\nYearly = hourly × 2,080",
 example="<p>A 5% raise on $24.00 an hour gives <strong>$25.20 an hour</strong>, which is $52,416 a year, or $2,496 more than before. Going from $50,000 to $53,000 is a raise of 3,000 ÷ 50,000 = <strong>6%</strong>.</p>",
 extra="<h3>What a raise is worth on $60,000</h3>" + tbl(["Raise", "New salary", "Extra per year", "Extra per month"], [(f"{p}%", f"${60000*(1+p/100):,.0f}", f"${600*p:,.0f}", f"${50*p:,.0f}") for p in (2, 3, 4, 5, 7, 10)]) +
 "<h3>How big is a typical raise?</h3><p>Surveys of US employers by consultancies such as WTW and Mercer have put typical salary increase budgets at around 3–4% in recent years. Promotions and job changes usually bring larger jumps, often 10% or more.</p>",
 faqs=[("How do I calculate a 3% raise?", "Multiply your pay by 1.03. On $45,000 that's $46,350, an extra $1,350 a year."),
       ("How do I work out my raise percentage?", "Subtract your old pay from your new pay, divide by your old pay and multiply by 100. From $20 to $21.50 an hour is a 7.5% raise."),
       ("Is a raise before or after tax?", "Raises are quoted on gross pay, before tax. Your take-home increase will be smaller."),
       ("What's a good raise?", "Anything above the inflation rate increases your buying power. Around 3–4% is common for a yearly raise; 10% or more is typical for a promotion.")],
 related=["salary", "paycheck", "percent", "timecard"])

# ---------- Water intake ----------
tool(id="water", slug="water-intake-calculator", cat="Health", name="Water Intake Calculator",
 short="Water intake", desc="How much water to drink a day.",
 title="Water Intake Calculator – How Much Water a Day? | Numbrik",
 meta="How much water should you drink a day? Estimate your daily water intake from your weight and exercise, in ounces, cups and litres.",
 lede="Estimate how much water to drink each day based on your body weight and how much you exercise. Results are shown in ounces, cups and litres, alongside the official adequate intake for adults.",
 steps=["Enter your weight in pounds or kilograms.", "Enter how many minutes you exercise on a typical day, and tick the box if it's hot where you are.",
        "Read your daily water target and how much that is in cups and bottles."],
 how="""<p>A common rule of thumb is to drink half an ounce of water for every pound you weigh (about 33 ml per kg), then add about 12 ounces (350 ml) for every 30 minutes of exercise. Hot or humid weather raises your needs further, so the calculator adds 16 ounces (about half a litre) when you tick that box.</p>
<p>For comparison, the US National Academies set an adequate intake of total water, from both drinks and food, of about 3.7 litres a day for men and 2.7 litres for women. Around 20% of that usually comes from food, which leaves roughly 13 cups of drinks for men and 9 for women. Thirst and pale yellow urine are good everyday guides.</p>""",
 formula="Base (oz) = weight (lb) × 0.5\nExercise: + 12 oz per 30 minutes\nHot weather: + 16 oz\n1 cup = 8 oz   1 litre = 33.8 oz",
 example="<p>A 160 lb person who exercises for 30 minutes a day needs about 160 × 0.5 + 12 = <strong>92 ounces</strong>, which is 11.5 cups or <strong>2.7 litres</strong> a day.</p>",
 extra="<h3>Daily water by body weight</h3>" + tbl(["Weight", "Base (no exercise)", "With 30 min exercise"], [(f"{w} lb ({w*0.4536:.0f} kg)", f"{w/2:.0f} oz · {w/2/33.814:.1f} L", f"{w/2+12:.0f} oz · {(w/2+12)/33.814:.1f} L") for w in (100, 120, 140, 160, 180, 200, 220, 250)]),
 faqs=[("How much water should I drink a day?", "A common estimate is half your body weight in pounds as ounces of water, so 80 ounces (about 2.4 litres) if you weigh 160 lb, plus more when you exercise or it's hot."),
       ("Do other drinks count?", "Yes. Milk, tea, coffee and juice all count toward your fluid intake, and so does water in food like fruit, vegetables and soup."),
       ("Can you drink too much water?", "It's rare, but drinking very large amounts in a short time can dilute the sodium in your blood. Spread drinks through the day and follow your thirst."),
       ("Is 8 glasses a day right?", "Eight 8-ounce glasses (about 1.9 litres) is a simple guide, but most adults need more once food and exercise are counted, and bigger people need more than smaller ones.")],
 related=["calorie", "protein", "bmi", "bmr"])

# ---------- Mulch ----------
tool(id="mulch", slug="mulch-calculator", cat="Home", name="Mulch Calculator",
 short="Mulch calculator", desc="Cubic yards and bags of mulch, soil or gravel.",
 title="Mulch Calculator – Cubic Yards & Bags Needed | Numbrik",
 meta="How much mulch do you need? Enter your bed size and depth to get cubic feet, cubic yards and the number of 2 or 3 cubic foot bags. Works for soil and gravel.",
 lede="Work out how much mulch, topsoil or gravel you need for a garden bed. Enter the size and depth to get cubic feet, cubic yards and the number of bags to buy.",
 steps=["Choose a rectangle or circle bed, and feet or metres.", "Enter the size and the depth you want. 2–3 inches is typical for mulch.",
        "Read the cubic yards to order in bulk, or the number of 2 and 3 cubic foot bags."],
 how="""<p>The calculator finds the bed area, multiplies it by the depth to get the volume in cubic feet, then divides by 27 to get cubic yards, the unit landscape suppliers sell in. Bagged mulch is usually sold in 2 or 3 cubic foot bags. For several beds, add up the results.</p>
<p>Spread mulch 2–3 inches deep on flower beds and 3–4 inches on paths and around trees, keeping it a few inches away from trunks and stems. Fresh mulch settles, so ordering 5–10% extra is sensible. The same maths works for topsoil, compost, sand and gravel.</p>""",
 formula="Volume (ft³) = length × width × depth (in) ÷ 12\nCircle: 3.1416 × radius² × depth ÷ 12\nCubic yards = ft³ ÷ 27",
 example="<p>A 20 ft × 10 ft bed at 3 inches deep needs 20 × 10 × 3 ÷ 12 = 50 cubic feet, which is <strong>1.85 cubic yards</strong>, or <strong>25 two-cubic-foot bags</strong> (17 three-cubic-foot bags).</p>",
 extra="<h3>How far one cubic yard goes</h3>" + tbl(["Depth", "Area covered by 1 cubic yard"], [(f"{d} in", f"{324/d:.0f} sq ft") for d in (1, 2, 3, 4, 6)]) +
 "<h3>Bags per cubic yard</h3><p>One cubic yard is 27 cubic feet: 13.5 bags of 2 cubic feet, or 9 bags of 3 cubic feet. Bulk delivery is usually cheaper once you need more than about 2–3 cubic yards.</p>",
 faqs=[("How much area does a yard of mulch cover?", "At 3 inches deep, one cubic yard covers about 108 square feet. At 2 inches it covers 162 square feet."),
       ("How many bags of mulch are in a yard?", "13.5 bags of 2 cubic feet, or 9 bags of 3 cubic feet."),
       ("How deep should mulch be?", "2–3 inches for beds, 3–4 inches for paths. More than 4 inches can stop water and air reaching the soil."),
       ("Can I use this for gravel or soil?", "Yes. The volume is the same for any loose material. Gravel is much heavier, so check the weight your vehicle can carry.")],
 related=["concrete", "sqft", "paint", "convert"])

# ---------- Working days ----------
yrs = (2026, 2027)
mrows = [(calendar.month_name[m], *(f"{work(y, m)}" for y in yrs)) for m in range(1, 13)]
tool(id="workdays", slug="working-days-calculator", cat="Dates & time", name="Working Days in a Year",
 short="Working days in a year", desc="Work days in any year and month, minus holidays.",
 title="How Many Working Days in 2026? Work Days | Numbrik",
 meta=f"There are {work(2026)} working days in 2026 in the US after federal holidays ({wdays(2026)} weekdays). See work days for any year and month, minus PTO.",
 lede=f"Count the working days in any year or month. There are {wdays(2026)} weekdays in 2026, and {work(2026)} working days after the 11 US federal holidays. Choose a year and add your own vacation days to see the days you'll actually work.",
 steps=["Pick a year.", "Choose whether to remove US federal holidays, and enter any vacation or PTO days.",
        "Read the working days and work hours for the year, with a month-by-month breakdown."],
 how="""<p>The calculator counts every Monday to Friday in the year, then removes the US federal holidays that fall on a weekday, using the observed date when a holiday lands on a weekend (Saturday holidays move to Friday, Sunday holidays to Monday). Your vacation days come off last.</p>
<p>A year has 52 weeks and one or two extra days, so it has 260, 261 or 262 weekdays. Private employers don't have to give federal holidays off, and many give fewer, so adjust the holiday setting to match your workplace. Work hours assume an 8-hour day.</p>""",
 formula="Working days = weekdays − weekday holidays − PTO days\nWork hours = working days × 8",
 example=f"<p>2026 has {wdays(2026)} weekdays. All 11 federal holidays fall on or are observed on a weekday, leaving <strong>{work(2026)} working days</strong>, or {work(2026)*8:,} hours at 8 hours a day. With 15 days of vacation you'd work {work(2026)-15} days. In 2027, New Year's Day 2028 falls on a Saturday and is observed on Friday, December 31, 2027, so 2027 has <strong>{work(2027)} working days</strong>.</p>",
 extra="<h3>Working days by month (US, after federal holidays)</h3>" + tbl(["Month", *map(str, yrs)], mrows + [("<strong>Total</strong>", *(f"<strong>{work(y)}</strong>" for y in yrs))]) +
 "<h3>US federal holidays</h3><p>New Year's Day, Martin Luther King Jr. Day, Washington's Birthday (Presidents' Day), Memorial Day, Juneteenth, Independence Day, Labor Day, Columbus Day, Veterans Day, Thanksgiving Day and Christmas Day.</p>",
 faqs=[("How many working days are in a year?", f"260 to 262 weekdays, depending on the year. After the 11 US federal holidays that's usually 249–251. In 2026 there are {work(2026)}."),
       ("How many working days are in a month?", "Usually 20 to 23 weekdays, about 21.7 on average. Holidays bring some months down to 19 or 20."),
       ("How many work hours are in a year?", f"At 40 hours a week, 2,080 hours before holidays and vacation. After federal holidays in 2026 that's {work(2026)*8:,} hours."),
       ("Does it include state holidays?", "No. It removes US federal holidays only. Enter extra days off in the PTO box to account for state or company holidays.")],
 related=["days", "hours", "timecard", "salary"])

BYID.update({t["id"]: t for t in T})
