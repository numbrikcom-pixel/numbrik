"""Page improvements based on Search Console queries (October 26, 2026).
Applied on top of the content modules without editing them."""
from content import BYID

need = lambda c, w, t: (t - c * (1 - w)) / w
def cell(x):
    if x > 100: return "Not reachable"
    if x <= 0: return "Already passing"
    return f"{x:.0f}%"

# ---- Final grade: queries are "what do I need on my final (to pass)" in many wordings ----
fg = BYID["finalgrade"]
fg["title"] = "What Do I Need on My Final? Final Grade Calculator | Numbrik"
fg["meta"] = "What do you need on your final exam to pass or get an A, B or C? Enter your current grade and the final's weight to see the exact score you need."
rows60 = "".join(f"<tr><td>{c}%</td>" + "".join(f"<td>{cell(need(c, w, 60))}</td>" for w in (.2, .3, .4)) + "</tr>" for c in (45, 50, 55, 60, 65, 70))
rows70 = "".join(f"<tr><td>{c}%</td>" + "".join(f"<td>{cell(need(c, w, 70))}</td>" for w in (.2, .3, .4)) + "</tr>" for c in (55, 60, 65, 70, 75, 80))
fg["extra"] += f"""<h2>What do I need on my final to pass?</h2>
<p>It depends on your passing grade. Many US colleges pass you with a D (60%), while many high schools and some courses need a C (70%). The tables show the score needed on the final for common current grades and final exam weights.</p>
<h3>To finish with 60%</h3><div class="tbl"><table><thead><tr><th>Current grade</th><th>Final worth 20%</th><th>Final worth 30%</th><th>Final worth 40%</th></tr></thead><tbody>{rows60}</tbody></table></div>
<h3>To finish with 70%</h3><div class="tbl"><table><thead><tr><th>Current grade</th><th>Final worth 20%</th><th>Final worth 30%</th><th>Final worth 40%</th></tr></thead><tbody>{rows70}</tbody></table></div>
<p>A heavier final helps when you are behind: with 50% now, you need {need(50,.4,60):.0f}% on a final worth 40% to finish with 60%, but a final worth 20% would need a perfect {need(50,.2,60):.0f}%.</p>"""

# ---- Auto loan: queries are "car payment calculator with tax and fees" ----
al = BYID["autoloan"]
al["title"] = "Car Payment Calculator with Tax & Fees | Numbrik"
al["meta"] = "Car payment and auto loan calculator with sales tax, fees, down payment and trade-in. See your monthly payment, total interest and total cost from 36 to 84 months."
al["steps"] = ["Enter the vehicle price, your down payment and any trade-in value.",
               "Enter the sales tax rate, any fees you want to finance and the interest rate from your lender.",
               "Pick a term and read the monthly payment, total interest and total cost."]
al["how"] = al["how"].replace("Dealer, title and registration fees are not included.",
    "Fees such as the dealer documentation fee, title and registration can be added to the loan with the Fees box. Leave it at 0 if you will pay them up front. Some states also charge sales tax on the dealer fee.")
al["formula"] = "Amount financed = price − down payment − trade-in + sales tax + fees\nMonthly payment = A × r(1 + r)ⁿ ÷ ((1 + r)ⁿ − 1)"
al["faqs"] = al["faqs"] + [("What fees are added to a car loan?", "Common ones are the dealer documentation fee, title and registration fees, and sometimes add-ons such as an extended warranty. Rolling them into the loan raises the monthly payment and the interest you pay, so paying them in cash is usually cheaper.")]

# ---- Hourly to salary: queries are "calculate hourly rate", "salary to hourly" ----
sl = BYID["salary"]
sl["title"] = "Hourly to Salary Calculator – Salary to Hourly Rate | Numbrik"
sl["extra"] = """<h2>How to calculate your hourly rate from a salary</h2><ol>
<li>Take your yearly salary before tax, for example $60,000.</li>
<li>Multiply your usual hours per week by the weeks you are paid: 40 × 52 = 2,080 hours.</li>
<li>Divide the salary by the hours: $60,000 ÷ 2,080 = $28.85 an hour.</li></ol>
<p>A quick estimate: halve the salary and drop the last three zeros. $60,000 becomes about $30 an hour. This works because 2,080 hours is close to 2,000.</p>""" + sl["extra"]
sl["faqs"] = sl["faqs"] + [("How do I work out my hourly pay from my salary?", "Divide your yearly salary by the hours you work in a year. At 40 hours a week for 52 weeks that is 2,080 hours, so $50,000 a year is about $24.04 an hour.")]

# Short label shown in the menu and search
BYID["sleep"]["short"] = "Sleep calculator"

# ---- October 28: Search Console round 2 ----
from more import MORE

def _t(s):
    h, m = s.split(" ")[0].split(":"); ap = s.split(" ")[1]
    h = int(h) % 12 + (12 if ap == "PM" else 0); return h * 60 + int(m)
def _hm(mins): return f"{mins // 60}h {mins % 60:02d}m"
SHIFTS = [("6:00 AM", "2:00 PM"), ("6:00 AM", "6:00 PM"), ("7:00 AM", "3:30 PM"), ("7:00 AM", "4:00 PM"), ("7:00 AM", "7:00 PM"),
          ("7:30 AM", "4:30 PM"), ("7:30 AM", "6:00 PM"), ("8:00 AM", "4:00 PM"), ("8:00 AM", "4:30 PM"), ("8:00 AM", "5:00 PM"),
          ("8:00 AM", "6:00 PM"), ("8:00 AM", "7:00 PM"), ("8:00 AM", "8:00 PM"), ("8:30 AM", "5:00 PM"), ("9:00 AM", "2:00 PM"),
          ("9:00 AM", "4:00 PM"), ("9:00 AM", "5:00 PM"), ("9:00 AM", "6:00 PM"), ("9:30 AM", "4:45 PM"), ("10:00 AM", "5:00 PM"),
          ("10:00 AM", "6:00 PM"), ("11:00 AM", "7:00 PM"), ("12:00 PM", "8:00 PM"), ("2:00 PM", "10:00 PM"), ("3:00 PM", "11:00 PM"),
          ("4:00 AM", "9:00 PM"), ("7:00 PM", "7:00 AM"), ("10:00 PM", "6:00 AM"), ("11:00 PM", "7:00 AM"),
          ("6:30 AM", "3:30 PM"), ("7:30 AM", "12:00 PM"), ("8:00 AM", "2:00 PM"), ("8:30 AM", "12:30 PM"), ("8:30 AM", "3:00 PM"), ("9:00 AM", "10:00 PM"),
          ("7:00 AM", "9:00 PM"), ("11:00 AM", "11:00 PM"), ("1:00 PM", "7:00 PM"), ("5:00 PM", "12:00 AM"), ("5:00 AM", "12:00 AM"), ("7:00 PM", "8:00 AM"),
          ("9:00 PM", "7:00 AM"), ("4:00 PM", "5:00 AM"), ("9:00 AM", "3:00 AM")]
SHIFTS.sort(key=lambda x: (_t(x[0]), (_t(x[1]) - _t(x[0])) % 1440))
rows = ""
for a, b in SHIFTS:
    m = (_t(b) - _t(a)) % 1440
    rows += f"<tr><td>{a} – {b}</td><td>{_hm(m)}</td><td>{m/60:.2f}</td><td>{_hm(m-30)}</td></tr>"
MORE["hours"] = f"""<h2>How many hours is it? Common shifts</h2><p>Time between common start and end times, with the time left after a 30-minute unpaid break.</p>
<div class="tbl"><table><thead><tr><th>From – to</th><th>Hours</th><th>Decimal</th><th>After 30-min break</th></tr></thead><tbody>{rows}</tbody></table></div>
<p>Breaks are often unpaid, but rules vary. US federal law does not require meal breaks, though several states do. In Canada, Australia, the UK and the Netherlands workers are entitled to rest breaks after a set number of hours, so check your contract or local rules.</p>"""
BYID["hours"]["title"] = "Hours Calculator – How Many Hours Between Two Times | Numbrik"

bills = [20, 25, 30, 40, 50, 60, 75, 80, 100, 120, 150, 200]
trows = "".join(f"<tr><td>${b}</td>" + "".join(f"<td>${b*p/100:.2f}</td>" for p in (15, 18, 20, 25)) + "</tr>" for b in bills)
MORE["tip"] = f"""<h2>How to calculate a tip in your head</h2><ol>
<li>Find 10% by moving the decimal point one place left: 10% of $64.00 is $6.40.</li>
<li>For 20%, double it: $12.80.</li>
<li>For 15%, add half of the 10% figure: $6.40 + $3.20 = $9.60.</li>
<li>For 18%, take 20% and subtract a tenth of the 20% figure: $12.80 − $1.28 = $11.52.</li></ol>
<h3>Tip chart for common bills</h3><div class="tbl"><table><thead><tr><th>Bill</th><th>15%</th><th>18%</th><th>20%</th><th>25%</th></tr></thead><tbody>{trows}</tbody></table></div>
""" + MORE.get("tip", "")
BYID["tip"]["title"] = "Tip Calculator – Calculate Tip & Split the Bill | Numbrik"
BYID["tip"]["meta"] = "Free tip calculator: enter the bill, pick 15%, 18%, 20% or 25%, and see the tip and what each person pays. Plus how to work out a tip in your head."

# ---- October 29: on-page SEO audit fixes (titles 60 chars or less, metas 160 or less) ----
BYID["salary"]["title"] = "Hourly to Salary Calculator – Salary to Hourly | Numbrik"
BYID["hours"]["title"] = "Hours Calculator – Hours Between Two Times | Numbrik"
BYID["hours"]["faqs"] = BYID["hours"]["faqs"] + [
  ("How many hours is 8 to 5?", "8:00 AM to 5:00 PM is 9 hours, or 8.5 hours after a 30-minute unpaid lunch."),
  ("How many hours is 7 PM to 7 AM?", "7:00 PM to 7:00 AM is 12 hours. The calculator handles overnight shifts automatically.")]
BYID["autoloan"]["meta"] = "Car payment calculator with sales tax, fees, down payment and trade-in. See your monthly payment, total interest and total cost from 36 to 84 months."

# ---- Nov 5, 2026: target the queries Search Console shows for these pages ----
hr = BYID["hours"]
hr["lede"] = "Count the hours between two times, such as 8 AM to 5 PM or 7 PM to 8 AM, minus any unpaid break. This free hours calculator gives the answer in hours and minutes and in decimal hours, and handles overnight shifts."
hr["faqs"] = hr["faqs"] + [("How do I convert minutes to decimal hours?", "Divide the minutes by 60. 7 hours 45 minutes is 7 + 45 ÷ 60 = 7.75 hours, which is the number most payroll systems use."),
  ("How many hours is 7:30 to 4:30?", "7:30 AM to 4:30 PM is 9 hours, or 8.5 hours after a 30-minute unpaid lunch.")]
tp = BYID["tip"]
tp["lede"] = "A free tip calculator: enter the bill, pick a tip percentage, and see the tip amount, the total and what each person pays when you split the bill."
tp["faqs"] = [("How do you calculate a tip?", "Multiply the bill by the tip percentage. For an 18% tip on $60, multiply 60 × 0.18 = $10.80, then add it to the bill for a total of $70.80."),
  ("How do I work out a 15% or 20% tip quickly?", "For 20%, move the decimal point one place left and double it: on $45, 10% is $4.50, so 20% is $9.00. For 15%, add half of the 10% amount: $4.50 + $2.25 = $6.75.")] + tp["faqs"]
gc = BYID["gcf"]
gc["lede"] = "Find the greatest common factor (GCF) of 2 to 20 whole numbers. It's also called the greatest common divisor (GCD) or highest common factor (HCF). Each number's prime factorization is shown so you can check the answer."

# ---- Nov 7, 2026: Hours Calculator rebuilt from the page's own Search Console queries + competitor gap report ----
hr = BYID["hours"]
hr["title"] = "Hours Calculator: How Many Hours Between Two Times?"
hr["meta"] = "Count the hours between two times, like 8 AM to 5 PM or 7 PM to 8 AM. Subtracts breaks and shows hours, minutes and decimal hours for timesheets."
hr["h1"] = "Hours Calculator: How Many Hours Between Two Times"
hr["lede"] = ("Find how many hours are between two times. Enter a start and end time, such as 8 AM and 5 PM, and the hours calculator shows the total in "
              "hours and minutes, decimal hours and minutes, minus any unpaid break. It handles overnight shifts like 7 PM to 7 AM, counts hours between two "
              "dates, and adds hours to a time. The charts below answer the most common shifts at a glance.")
hr["steps"] = ["Choose Between two times, Between two dates, or Add hours to a time.",
               "Enter the start and end times, or tap Now to use the current time. Add an unpaid break in minutes if you have one.",
               "Read the total in hours and minutes, the sentence answer you can copy, the decimal hours for a timesheet and the total minutes."]
hr["example"] = ("<p>From 8:00 AM to 5:00 PM is <strong>9 hours</strong> (540 minutes, 9.00 decimal hours). Take off a 30-minute unpaid lunch and the time worked is "
                 "<strong>8 hours 30 minutes</strong>, or 8.50 decimal hours. Overnight, 7:00 PM to 7:00 AM is 12 hours.</p>")

_EXTRA = [("8:00 AM", "10:00 PM"), ("7:00 PM", "11:00 PM"), ("1:30 AM", "8:00 PM"), ("6:00 PM", "8:00 AM"), ("7:00 AM", "6:00 PM"), ("6:00 AM", "9:00 PM"),
          ("5:00 AM", "10:00 PM"), ("10:00 AM", "4:00 PM"), ("6:00 AM", "12:00 PM"), ("10:00 AM", "8:00 PM"), ("7:00 PM", "10:00 PM"), ("8:00 PM", "8:00 AM"),
          ("10:00 AM", "10:00 PM"), ("6:00 AM", "11:00 AM"), ("8:00 PM", "12:00 AM"), ("5:00 PM", "9:00 PM"), ("8:00 AM", "3:00 PM"), ("2:00 PM", "12:00 AM"),
          ("8:00 PM", "7:00 AM"), ("8:00 PM", "4:00 AM"), ("11:00 PM", "3:00 AM"), ("4:00 PM", "10:00 AM"), ("10:00 PM", "7:00 AM"), ("6:00 PM", "1:00 AM"),
          ("6:00 PM", "9:00 AM"), ("5:00 PM", "9:00 AM"), ("5:00 PM", "7:00 AM"), ("9:00 AM", "4:30 PM"), ("8:30 AM", "4:30 PM"), ("7:30 AM", "3:30 PM"),
          ("6:30 AM", "2:30 PM"), ("6:30 AM", "4:30 PM"), ("8:30 AM", "5:30 PM"), ("9:30 AM", "5:00 PM"), ("6:00 AM", "4:00 PM"), ("4:00 AM", "4:00 PM"),
          ("3:00 AM", "9:00 AM"), ("11:00 AM", "4:00 PM"), ("10:00 AM", "2:00 PM"), ("10:00 AM", "1:00 PM"), ("1:00 PM", "5:00 PM"), ("3:00 PM", "7:00 PM"),
          ("6:00 PM", "9:00 PM"), ("7:30 PM", "12:00 AM"), ("9:30 AM", "4:00 PM"), ("8:00 AM", "12:00 PM"), ("8:00 AM", "11:00 AM"), ("7:00 AM", "10:00 AM"),
          ("8:30 AM", "3:30 PM"), ("8:00 AM", "3:30 PM"), ("10:00 AM", "5:00 PM"), ("6:00 PM", "6:00 AM"), ("6:00 AM", "6:00 PM"), ("4:00 PM", "5:00 AM")]
_all = []
for x in SHIFTS + _EXTRA:
    if x not in _all: _all.append(x)
def _row(a, b):
    m = (_t(b) - _t(a)) % 1440
    return f"<tr><td>{a} – {b}</td><td>{_hm(m)}</td><td>{m:,}</td><td>{m/60:.2f}</td><td>{_hm(max(0, m-30))}</td></tr>"
def _tbl(rows):
    return ('<div class="tbl"><table><thead><tr><th>From – to</th><th>Hours</th><th>Minutes</th><th>Decimal</th><th>After 30-min break</th></tr></thead><tbody>'
            + "".join(_row(a, b) for a, b in rows) + "</tbody></table></div>")
_key = lambda x: (_t(x[0]), (_t(x[1]) - _t(x[0])) % 1440)
_over = sorted([x for x in _all if _t(x[1]) <= _t(x[0])], key=_key)
_short = sorted([x for x in _all if _t(x[1]) > _t(x[0]) and _t(x[1]) - _t(x[0]) < 360], key=_key)
_day = sorted([x for x in _all if _t(x[1]) > _t(x[0]) and _t(x[1]) - _t(x[0]) >= 360], key=_key)
_dec = "".join(f"<tr><td>{m} min</td><td>{m/60:.2f}</td><td>{m+30} min</td><td>{(m+30)/60:.2f}</td></tr>" for m in range(0, 30, 5)) + "<tr><td>30 min</td><td>0.50</td><td>60 min</td><td>1.00</td></tr>"
_adds = [("8:15 AM", 8 * 60), ("9:15 AM", 510), ("7:30 AM", 9 * 60), ("7:00 PM", 12 * 60), ("10:00 PM", 8 * 60), ("2:00 PM", -3 * 60)]
def _clock(mins):
    mins %= 1440; h, m = divmod(mins, 60)
    return f"{h % 12 or 12}:{m:02d} {'AM' if h < 12 else 'PM'}"
def _addrow(a, d):
    e = _t(a) + d; day = " (next day)" if e >= 1440 else (" (previous day)" if e < 0 else "")
    sign = f"{abs(d)//60}h {abs(d)%60:02d}m {'after' if d >= 0 else 'before'}"
    return f"<tr><td>{sign} {a}</td><td>{_clock(e)}{day}</td></tr>"
MORE["hours"] = f"""<h2>How many hours is it? Common work shifts</h2>
<p>The time between common start and end times, in hours and minutes, total minutes and decimal hours, plus the time left after a 30-minute unpaid break. For any other times, use the calculator above.</p>
<h3>Daytime shifts (6 hours or more)</h3>{_tbl(_day)}
<h3>Overnight shifts</h3><p>When the end time is earlier than the start time, the shift runs past midnight, so 24 hours are added.</p>{_tbl(_over)}
<h3>Short spans (under 6 hours)</h3>{_tbl(_short)}
<p>Breaks are often unpaid, but rules vary. US federal law does not require meal breaks, though several states do. In Canada, Australia, the UK and the Netherlands workers are entitled to rest breaks after a set number of hours, so check your contract or local rules. For a whole week of shifts with overtime, use the <a href="/time-card-calculator/">time card calculator</a>.</p>

<h2>How to calculate hours between two times</h2>
<h3>Step 1: Convert both times to 24-hour time</h3><p>Add 12 to any PM hour except 12 PM: 4:30 PM becomes 16:30. 12 AM (midnight) becomes 0:00. The <a href="/military-time-converter/">military time converter</a> does this for you.</p>
<h3>Step 2: Subtract the start time from the end time</h3><p>Subtract the hours and the minutes separately: 16:30 − 7:30 = 9 hours 0 minutes. If the minutes go negative, borrow 60 minutes from the hours. If the end time is earlier than the start, the shift crosses midnight, so add 24 hours.</p>
<h3>Step 3: Subtract unpaid breaks</h3><p>Take off any unpaid lunch or rest break: 9 hours − 30 minutes = 8 hours 30 minutes.</p>
<h3>Step 4: Convert the minutes to decimal hours</h3><p>Divide the minutes by 60 for a timesheet: 30 ÷ 60 = 0.5, so 8 hours 30 minutes is 8.5 hours. <strong>Worked example:</strong> 7:30 AM to 4:30 PM with a 30-minute lunch is 9 hours − 30 minutes = <strong>8.5 hours</strong>.</p>

<h2>Minutes to decimal hours chart</h2>
<p>Payroll systems usually want hours as a decimal. Divide the minutes by 60, or use this chart.</p>
<div class="tbl"><table><thead><tr><th>Minutes</th><th>Decimal</th><th>Minutes</th><th>Decimal</th></tr></thead><tbody>{_dec}</tbody></table></div>
<p>Many employers round to the nearest quarter hour (0.25). Under US federal rules, rounding is allowed if it averages out over time so that employees are fully paid for the time they work.</p>

<h2>Add or subtract hours from a time</h2>
<p>To find when a shift ends, add the hours to the start time. Choose <strong>Add hours to a time</strong> in the calculator, or use these examples.</p>
<div class="tbl"><table><thead><tr><th>Calculation</th><th>Result</th></tr></thead><tbody>{"".join(_addrow(a, d) for a, d in _adds)}</tbody></table></div>

<h2>How many hours are in a day, week, month and year?</h2>
<div class="tbl"><table><thead><tr><th>Period</th><th>Hours</th></tr></thead><tbody>
<tr><td>Day</td><td>24</td></tr><tr><td>Week</td><td>168</td></tr><tr><td>2 weeks</td><td>336</td></tr>
<tr><td>Month (28 / 30 / 31 days)</td><td>672 / 720 / 744</td></tr><tr><td>Average month</td><td>730.5</td></tr>
<tr><td>Year (365 / 366 days)</td><td>8,760 / 8,784</td></tr>
<tr><td>Full-time work year (40 hours × 52 weeks)</td><td>2,080</td></tr></tbody></table></div>
<p>To count the working days in a particular year, use the <a href="/working-days-calculator/">working days calculator</a>. To turn hours into pay, use the <a href="/hourly-to-salary-calculator/">hourly to salary calculator</a>.</p>

<h2>AM, PM, noon and midnight</h2>
<h3>Is 12 PM noon or midnight?</h3><p>12 PM is noon and 12 AM is midnight, the start of the day. So 12 AM to 8 AM is 8 hours, and 8 PM to 12 AM is 4 hours. If you mean the very end of a day, enter 12:00 AM; the calculator treats it as the following midnight.</p>
<h3>12-hour vs 24-hour (military) time</h3><p>The 24-hour clock numbers the hours from 0 to 23, so there's no AM or PM: 2:00 PM is 14:00 and 11:30 PM is 23:30. It's used by the military, hospitals and most countries outside the US. The <a href="/military-time-converter/">military time converter</a> switches between the two.</p>"""
hr["faqs"] = hr["faqs"] + [
  ("How many hours is a full-time shift?", "There's no legal definition of full-time in US federal law, according to the U.S. Department of Labor, so employers set their own. A common full-time day is 8 hours, such as 9 AM to 5 PM, or 8 AM to 4:30 PM with a 30-minute unpaid lunch: 40 hours over a 5-day week."),
  ("How many hours is 8 AM to 4:30 PM with a 30-minute lunch?", "8 hours. 8:00 AM to 4:30 PM is 8 hours 30 minutes, and taking off the 30-minute lunch leaves 8 hours, or 8.00 decimal hours.")]

# ---- Nov 8, 2026: stronger title tags (keyword first, a clear benefit, year where freshness matters) ----
import datetime as _dt
_Y = _dt.date.today().year
_TT = {
 "bmi": "BMI Calculator – Check Your Body Mass Index | Numbrik",
 "bmr": "BMR Calculator – Calories You Burn at Rest | Numbrik",
 "bodyfat": "Body Fat Calculator – US Navy Tape Method | Numbrik",
 "cd": "CD Calculator – How Much Will My CD Earn? | Numbrik",
 "coin": "Flip a Coin – Heads or Tails Online, Free | Numbrik",
 "days": "Days Between Dates Calculator – Count Days | Numbrik",
 "gcf": "GCF Calculator – Greatest Common Factor (GCD) | Numbrik",
 "gpa": "GPA Calculator – Semester & Cumulative (4.0 Scale) | Numbrik",
 "grade": "Grade Calculator – Weighted Grade & Letter | Numbrik",
 "lcm": "LCM Calculator – Least Common Multiple, Steps | Numbrik",
 "military": "Military Time Converter & 24-Hour Clock Chart | Numbrik",
 "raise": "Pay Raise Calculator – New Salary After a Raise | Numbrik",
 "percent": "Percentage Calculator – Percent Of, Off & Change | Numbrik",
 "random": "Random Number Generator (RNG) – 1 to 100 & More | Numbrik",
 "sqft": "Square Footage Calculator – Room Area & Flooring | Numbrik",
 "stdev": "Standard Deviation Calculator with Steps | Numbrik",
 "workdays": f"Working Days Calculator – Work Days in {_Y} & {_Y+1} | Numbrik",
 "turkey": f"Turkey Calculator {_Y} – Size, Thaw & Cooking Time | Numbrik",
 "soh": f"Save Our Homes Calculator {_Y} – Florida Tax Savings",
 "salary": "Hourly to Salary Calculator (and Salary to Hourly) | Numbrik",
 "paycheck": f"Take-Home Pay Calculator {_Y} – US Paycheck | Numbrik",
}
for _k, _v in _TT.items():
    assert len(_v) <= 60, (_k, len(_v))
    BYID[_k]["title"] = _v
