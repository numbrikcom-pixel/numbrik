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
          ("4:00 AM", "9:00 PM"), ("7:00 PM", "7:00 AM"), ("10:00 PM", "6:00 AM"), ("11:00 PM", "7:00 AM")]
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
BYID["autoloan"]["meta"] = "Car payment calculator with sales tax, fees, down payment and trade-in. See your monthly payment, total interest and total cost from 36 to 84 months."
