"""Five tools from the Nov 18, 2026 keyword review (Google Trends + Semrush): VA disability, time, invoice generator, EMI, SIP.
VA rates: 2026 compensation rates effective Dec 1, 2025 (2.8% COLA), as published by VA and reproduced by CCK Law."""
from content import tool, T, BYID
import qa

def tbl(head, rows):
    return ('<div class="tbl"><table><thead><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")
usd = lambda x: f"${x:,.2f}"
def inr(x):  # Indian grouping: 12,34,567
    x = round(x); s = str(abs(x)); h, t = s[:-3], s[-3:]
    while len(h) > 2: t = h[-2:] + "," + t; h = h[:-2]
    return "₹" + (h + "," + t if h else t)

A = [180.42, 356.66, 552.47, 795.84, 1132.90, 1435.02, 1808.45, 2102.15, 2362.30, 3938.58]
S = [617.47, 882.84, 1241.90, 1566.02, 1961.45, 2277.15, 2559.30, 4158.17]
SC = [666.47, 947.84, 1322.90, 1663.02, 2074.45, 2406.15, 2704.30, 4318.99]
C = [596.47, 853.84, 1205.90, 1523.02, 1910.45, 2219.15, 2494.30, 4085.43]
K = [32, 43, 54, 65, 76, 87, 98, 109.11]; SCH = [105, 140, 176, 211, 246, 281, 317, 352.45]; AA = [61, 81, 101, 121, 141, 161, 181, 201.41]
def va(rs):
    e = 0
    for r in sorted(rs, reverse=True): e = int(e + (100 - e) * r / 100 + .5)
    return e, min(100, int(e / 10 + .5) * 10)

def emi(P, rate, n):
    r = rate / 1200; return P * r * (1 + r) ** n / ((1 + r) ** n - 1)
def sip(m, rate, y, step=0):
    i = rate / 1200; v = inv = 0; a = m
    for _ in range(y):
        for _ in range(12): v = (v + a) * (1 + i); inv += a
        a *= 1 + step / 100
    return v, inv

# ----------------------------------------------------------------- VA disability
e1, c1 = va([50, 30, 10]); e2, c2 = va([70, 20]); e3, c3 = va([40, 40, 20, 10])
tool(id="vadisab", slug="va-disability-calculator", cat="Money", name="VA Disability Calculator",
 short="VA disability", desc="Combined VA rating and monthly pay for 2026.",
 title="VA Disability Calculator 2026 – Combined Rating & Pay | Numbrik",
 meta="Free VA disability calculator: combine your ratings with VA math, see your rounded combined rating and 2026 monthly pay with spouse and children.",
 lede="Enter your individual VA disability ratings to see how VA combines them, the rating it rounds to, and your 2026 monthly compensation, including extra pay for a spouse and children. VA doesn't add ratings together, which is why 50% and 30% don't make 80%.",
 steps=["Type each of your service-connected ratings, separated by commas, such as 50, 30, 10.", "Choose whether you're married and, if so, whether your spouse needs Aid and Attendance.", "Enter how many children you have under 18 and how many aged 18 to 23 are in school.", "Read your combined rating, monthly and yearly pay, and the VA math step by step."],
 how=f"""<p>VA uses a "whole person" method. You start as 100% able. Your highest rating takes its percentage of that whole; each next rating then takes its percentage of what is left, not of 100%. VA rounds each step to a whole number, the same as its combined ratings table, and then rounds the final value to the nearest 10 (a value ending in 5 rounds up).</p>
<p>For ratings of 50%, 30% and 10%: 50% of 100 leaves 50; 30% of the remaining 50 is 15, so you're at 65; 10% of the remaining 35 is 3.5, giving 68.5, which the table shows as 69 and VA rounds to <strong>{c1}%</strong>. Monthly pay then comes from VA's rate table for that combined rating. At 30% and above, VA pays more for a spouse, children and dependent parents.</p>""",
 formula="Remaining = 100\nFor each rating, highest first:\n  combined = combined + remaining × rating ÷ 100\n  remaining = 100 − combined\nFinal rating = combined rounded to the nearest 10",
 example=f"<p><strong>Ratings of 50%, 30% and 10%</strong> combine to {e1}%, which VA rounds to <strong>{c1}%</strong>. A single veteran with no dependents at {c1}% receives <strong>{usd(A[c1 // 10 - 1])} a month</strong> in 2026. Married with one child, the same veteran receives {usd(SC[c1 // 10 - 3])}.</p>",
 extra='<h3 id="rates">2026 VA disability pay chart (monthly)</h3><p>Rates effective December 1, 2025, after the 2.8% cost-of-living adjustment. At 10% and 20%, pay is the same with or without dependents.</p>' +
   tbl(["Rating", "Veteran alone", "With spouse", "Spouse + 1 child", "1 child, no spouse"],
       [(f"{(i + 1) * 10}%", usd(A[i]), *( [usd(S[i - 2]), usd(SC[i - 2]), usd(C[i - 2])] if i >= 2 else ["—", "—", "—"])) for i in range(10)]) +
   '<h3 id="added">Added amounts for more dependents (monthly)</h3>' +
   tbl(["Rating", "Each additional child under 18", "Each child 18–23 in school", "Spouse needs Aid & Attendance"], [(f"{(i + 3) * 10}%", usd(K[i]), usd(SCH[i]), usd(AA[i])) for i in range(8)]) +
   '<h3 id="examples">VA math examples</h3>' +
   tbl(["Individual ratings", "Exact combined", "Rounded rating", "Monthly pay (alone)"],
       [(", ".join(f"{r}%" for r in rs), f"{e}%", f"{c}%", usd(A[c // 10 - 1])) for rs in ([50, 30, 10], [70, 20], [40, 40, 20, 10], [30, 20, 10, 10], [60, 50], [90, 50]) for e, c in [va(rs)]]) +
   '<h3 id="notes">What this calculator doesn\'t include</h3><ul><li><strong>Bilateral factor:</strong> when both arms or both legs (or paired organs) are rated, VA adds 10% of their combined value before combining with other ratings, so your result may be slightly higher.</li>'
   "<li><strong>Dependent parents</strong> and <strong>special monthly compensation (SMC)</strong> for things like loss of use or housebound status are paid on top and aren't included.</li>"
   "<li>A new cost-of-living adjustment takes effect each December 1. We update this page when VA publishes the new table.</li></ul>",
 faqs=[("How does VA calculate combined disability ratings?", "VA applies your ratings one at a time, highest first, each to the part of you that isn't already disabled. 50% and 30% make 65% (30% of the remaining 50 is 15), which rounds to 70%. The exact value is rounded to the nearest 10."),
       ("Why doesn't 50% plus 30% equal 80%?", "Because VA doesn't add ratings. After a 50% rating, only 50% of you is considered able, so a 30% rating takes 30% of that 50, which is 15 points, for 65% combined, rounded to 70%."),
       ("How much is 100% VA disability in 2026?", "A veteran alone at 100% receives $3,938.58 a month from December 1, 2025, about $47,263 a year, tax-free. With a spouse it's $4,158.17, and with a spouse and one child $4,318.99."),
       ("Is VA disability pay taxable?", "No. VA disability compensation isn't taxed by the federal government or by states, and it doesn't count as income on your federal return."),
       ("When do dependents increase VA pay?", "Only at a combined rating of 30% or higher. You need to add dependents with VA (for example on VA Form 21-686c) before the extra amount is paid.")],
 related=["salary", "retire", "paycheck", "compound"])

# ----------------------------------------------------------------- Time calculator
tool(id="timecalc", slug="time-calculator", cat="Dates & time", name="Time Calculator",
 short="Time calculator", desc="Add or subtract hours, minutes and seconds.",
 title="Time Calculator – Add & Subtract Hours and Minutes | Numbrik",
 meta="Free time calculator: add or subtract hours, minutes and seconds, total up a list of times, or find what time it will be after a number of hours.",
 lede="Add up a list of times like 2:45 + 1:30 + 0:50, subtract time, or find the clock time a number of hours and minutes from now. Results come as hours:minutes, decimal hours and total minutes.",
 steps=["Choose Add up durations to total a list of times, or Time of day ± hours to move a clock time forward or back.", "For durations, type one time per line as 2:45, 1:30:20 or 1h 15m. Put a minus sign in front of any time to subtract it.", "For a clock time, pick the start time, choose add or subtract, and enter the hours and minutes.", "Read the total, or the resulting time and whether it lands on another day."],
 how="""<p>Time is base 60, not base 10, so you can't add 2:45 and 1:30 like decimals. The calculator turns every time into seconds, adds or subtracts them, and turns the total back into hours, minutes and seconds. 2:45 + 1:30 is 165 + 90 = 255 minutes, which is 4 hours 15 minutes, not 3:75.</p>
<p>For a clock time, the calculator adds the duration to the start time and wraps past midnight, telling you if the result falls on the next day or the day before. 9:30 PM plus 4 hours 45 minutes is 2:15 AM the next day.</p>""",
 formula="Seconds = hours × 3,600 + minutes × 60 + seconds\nTotal = sum of all times in seconds\nHours = total ÷ 3,600 (whole part)\nMinutes = (remainder) ÷ 60",
 example="<p><strong>2:45 + 1:30 + 0:50 − 0:20</strong> = 165 + 90 + 50 − 20 = 285 minutes = <strong>4 hours 45 minutes</strong> (4.75 hours). <strong>9:30 AM + 8 h 45 min</strong> = <strong>6:15 PM</strong>.</p>",
 extra="<h3>Minutes to decimal hours</h3>" + tbl(["Minutes", "Decimal hours", "Minutes", "Decimal hours"], [(f"{m}", f"{m / 60:.2f}".rstrip("0").rstrip("."), f"{m + 30}", f"{(m + 30) / 60:.2f}".rstrip("0").rstrip(".")) for m in (5, 10, 15, 20, 25, 30)]) +
   "<h3>Common time additions</h3>" + tbl(["Calculation", "Result"], [("1:45 + 2:30", "4:15"), ("3:50 + 0:25", "4:15"), ("8:00 − 0:45", "7:15"), ("12:00 PM + 9 h 30 min", "9:30 PM"), ("10:00 PM + 8 h", "6:00 AM next day"), ("7:15 AM − 1 h 30 min", "5:45 AM")]),
 faqs=[("How do I add hours and minutes together?", "Add the minutes, and for every 60 minutes carry 1 hour. 2:45 + 1:30: 45 + 30 = 75 minutes, which is 1 hour 15 minutes; 2 + 1 + 1 = 4 hours, so the total is 4:15."),
       ("How do I subtract time?", "Subtract the minutes first. If you don't have enough, borrow 1 hour as 60 minutes. 5:10 − 2:40: borrow so 5:10 becomes 4:70, then 4:70 − 2:40 = 2:30."),
       ("What time will it be in 8 hours?", "Add 8 hours to the current time and subtract 12 (or 24) if you pass noon or midnight. Use Time of day ± hours above with your start time to get the exact answer."),
       ("How do I convert minutes to decimal hours?", "Divide the minutes by 60. 45 minutes is 0.75 hours, so 3 hours 45 minutes is 3.75 hours.")],
 related=["hours", "timecard", "timedec", "days"])

# ----------------------------------------------------------------- Invoice generator
tool(id="invoice", slug="invoice-generator", cat="Work & pay", name="Invoice Generator",
 short="Invoice generator", desc="Make a professional invoice and save it as a PDF.",
 title="Free Invoice Generator – Create a PDF Invoice | Numbrik",
 meta="Free invoice generator: add your details, client, items, tax and discount, then download a clean PDF invoice. No sign-up, nothing uploaded.",
 lede="Create a clean, professional invoice in a minute. Fill in your details and your client's, add line items, tax and discount, and download it as a PDF. It's free, needs no account, and everything stays in your browser.",
 steps=["Enter your name or business and contact details under From, and your client's under Bill to.", "Set the invoice number, date, due date and currency.", "Add each item or service with its quantity and price. Use + Add item for more lines.", "Add tax or a discount if needed, plus payment terms in the notes.", "Click Download PDF / Print and choose Save as PDF."],
 how="""<p>Each line amount is quantity × price. The subtotal is the sum of the lines; a discount comes off the subtotal, and tax is charged on the amount after the discount. The total due is subtotal − discount + tax.</p>
<p>The invoice is built in your browser and never sent to a server, so client details stay private. Your last invoice is remembered on this device, which makes the next one quicker: change the number and items, and you're done.</p>""",
 formula="Line amount = quantity × price\nSubtotal = sum of line amounts\nDiscount = subtotal × discount %\nTax = (subtotal − discount) × tax %\nTotal due = subtotal − discount + tax",
 example="<p>A freelancer bills <strong>10 hours of design at $50</strong> and <strong>1 month of hosting at $20</strong>: subtotal $520. With a 10% discount ($52) and 8% sales tax on the rest ($37.44), the total due is <strong>$505.44</strong>.</p>",
 extra="<h3>What to put on an invoice</h3>" + tbl(["Item", "Why it matters"], [("Your name or business, and contact details", "So the client knows who to pay and how to reach you"), ("Client name and address", "Shows who owes the money"), ("Unique invoice number", "Needed for your records and the client's accounts team; number invoices in order, like INV-001"),
     ("Invoice date and due date", "Sets when payment is expected, such as 14 or 30 days"), ("Description, quantity and price of each item", "Makes the total easy to check and reduces disputes"), ("Tax, if you charge it", "Show the rate and amount separately (sales tax, VAT or GST)"), ("Payment details and terms", "Bank details, PayPal or other methods, and any late-fee terms")]) +
   "<h3>Common payment terms</h3>" + tbl(["Term", "Meaning"], [("Due on receipt", "Payment expected right away"), ("Net 15 / Net 30", "Payment due 15 or 30 days after the invoice date"), ("2/10 Net 30", "2% discount if paid within 10 days, otherwise full amount in 30 days"), ("50% upfront", "Half paid before work starts, the rest on delivery")]),
 faqs=[("How do I make an invoice for free?", "Fill in your details, your client's, and the items above, then click Download PDF / Print and choose Save as PDF. There's no sign-up, watermark or limit."),
       ("Is my information saved or uploaded?", "No. The invoice is created entirely in your browser. Your last invoice is remembered only on your own device so you can reuse it."),
       ("What should an invoice number look like?", "Any unique, sequential code works, such as INV-001, INV-002 or 2026-014. Never reuse a number; it helps you and your client keep clean records."),
       ("Do I need to charge tax on my invoice?", "It depends on where you are and what you sell. In the US, many services aren't subject to sales tax, but some states tax them. In the UK and EU, VAT applies once you're registered. Check your local rules or an accountant.")],
 related=["salary", "paycheck", "discount", "pctchange"])

# ----------------------------------------------------------------- EMI
tool(id="emi", slug="emi-calculator", cat="Money", name="EMI Calculator",
 short="EMI calculator", desc="Monthly EMI, total interest and repayment schedule.",
 title="EMI Calculator – Home, Car & Personal Loan EMI | Numbrik",
 meta="Free EMI calculator: find the monthly EMI for a home, car or personal loan, total interest and a year-by-year repayment schedule in rupees.",
 lede="Work out the EMI (equated monthly instalment) on any loan: home, car, personal or education. Enter the amount, interest rate and tenure to see your EMI, the total interest and how the balance falls each year.",
 steps=["Enter the loan amount in rupees.", "Enter the annual interest rate your lender quoted.", "Enter the tenure in years or months.", "Read your monthly EMI, total interest and the yearly repayment schedule."],
 how="""<p>An EMI is a fixed monthly payment that covers that month's interest and repays a little of the principal. Early on, most of each EMI is interest, because the balance is high; as the balance falls, more of each EMI goes to principal. The formula below gives the one payment that clears the loan exactly in the chosen number of months.</p>
<p>Banks in India calculate interest on the reducing balance each month, which is what this calculator does. Processing fees, insurance and GST on fees are not included. Prepaying part of the loan early cuts the total interest sharply, because it removes principal while interest is at its highest.</p>""",
 formula="EMI = P × r × (1 + r)ⁿ ÷ ((1 + r)ⁿ − 1)\nP = loan amount, r = annual rate ÷ 12 ÷ 100, n = months\nTotal interest = EMI × n − P",
 example=f"<p>A <strong>₹25,00,000 home loan</strong> at <strong>8.5%</strong> for <strong>20 years</strong> (240 months) has an EMI of <strong>{inr(emi(2500000, 8.5, 240))}</strong>. Over 20 years you pay {inr(emi(2500000, 8.5, 240) * 240)}, of which {inr(emi(2500000, 8.5, 240) * 240 - 2500000)} is interest.</p>",
 extra="<h3>EMI per ₹1 lakh borrowed</h3>" + tbl(["Rate", "5 years", "10 years", "15 years", "20 years", "30 years"], [(f"{r}%", *[inr(emi(100000, r, y * 12)) for y in (5, 10, 15, 20, 30)]) for r in (7.5, 8, 8.5, 9, 10, 11, 12, 14)]) +
   "<p>Multiply by the number of lakhs you're borrowing: a ₹30 lakh loan at 8.5% for 20 years is about 30 × " + inr(emi(100000, 8.5, 240)) + " = " + inr(emi(3000000, 8.5, 240)) + " a month.</p>" +
   "<h3>Typical EMIs by loan type</h3>" + tbl(["Loan", "Amount", "Rate", "Tenure", "EMI", "Total interest"], [(n, inr(P), f"{r}%", f"{y} years", inr(emi(P, r, y * 12)), inr(emi(P, r, y * 12) * y * 12 - P)) for n, P, r, y in (("Home loan", 5000000, 8.5, 20), ("Car loan", 800000, 9.5, 5), ("Personal loan", 300000, 13, 3), ("Education loan", 1000000, 10, 7))]),
 faqs=[("How is EMI calculated?", "With the formula EMI = P × r × (1 + r)ⁿ ÷ ((1 + r)ⁿ − 1), where P is the loan, r is the monthly rate (annual rate ÷ 12 ÷ 100) and n is the number of months. ₹10 lakh at 9% for 10 years gives an EMI of about ₹12,668."),
       ("Does a longer tenure reduce EMI?", "Yes, but you pay much more interest. ₹25 lakh at 8.5% costs about ₹24,618 a month over 15 years, or ₹21,696 over 20 years, but the 20-year loan costs over ₹7.7 lakh more in interest."),
       ("Is it better to prepay a loan or invest?", "Prepaying saves interest at your loan rate with no risk. If your investments are unlikely to beat the loan rate after tax, prepaying usually wins. Check for prepayment charges first; floating-rate home loans in India have none for individuals."),
       ("Does the EMI include processing fees and insurance?", "No. Processing fees, GST on fees and loan insurance are charged separately, so the total cost of the loan is a little higher.")],
 related=["loan", "autoloan", "gloan", "sip"])

# ----------------------------------------------------------------- SIP
v1, i1 = sip(10000, 12, 15); v2, i2 = sip(10000, 12, 15, 10)
tool(id="sip", slug="sip-calculator", cat="Money", name="SIP Calculator",
 short="SIP calculator", desc="What a monthly SIP grows to, with optional step-up.",
 title="SIP Calculator – Mutual Fund SIP Returns & Step-Up | Numbrik",
 meta="Free SIP calculator: see what your monthly mutual fund SIP could grow to, with total invested, estimated returns and an optional yearly step-up.",
 lede="See what a monthly SIP (systematic investment plan) in a mutual fund could grow to. Enter your monthly amount, expected return and time period, and optionally raise the SIP each year, to see total invested, estimated returns and the final value.",
 steps=["Enter how much you'll invest each month.", "Enter the return you expect per year, such as 12% for an equity fund.", "Enter the number of years.", "Optionally add a yearly step-up, the percentage by which you'll raise your SIP each year.", "Read the estimated final value, the amount you invested and the year-by-year growth."],
 how="""<p>Each monthly instalment is invested and grows at the monthly rate (annual return ÷ 12) until the end of the period. Instalments made early compound for longer, which is why the gains grow faster in the later years. This calculator assumes each SIP is invested at the start of the month, the same convention most fund houses' calculators use.</p>
<p>A step-up SIP raises the monthly amount once a year, typically in line with your salary. Even a 10% yearly step-up makes a large difference over 15–20 years. Real mutual fund returns vary from year to year and can be negative; the result is an estimate, not a guarantee.</p>""",
 formula="FV = P × [((1 + i)ⁿ − 1) ÷ i] × (1 + i)\nP = monthly SIP, i = annual return ÷ 12 ÷ 100, n = months\nReturns = FV − total invested",
 example=f"<p>A <strong>₹10,000 SIP</strong> for <strong>15 years</strong> at <strong>12%</strong> a year grows to about <strong>{inr(v1)}</strong>: {inr(i1)} invested and {inr(v1 - i1)} in returns. With a <strong>10% yearly step-up</strong>, it grows to about {inr(v2)} on {inr(i2)} invested.</p>",
 extra="<h3>What a ₹5,000 monthly SIP can become</h3>" + tbl(["Years", "Invested", "At 8%", "At 10%", "At 12%", "At 15%"], [(f"{y}", inr(5000 * 12 * y), *[inr(sip(5000, r, y)[0]) for r in (8, 10, 12, 15)]) for y in (5, 10, 15, 20, 25, 30)]) +
   "<h3>Monthly SIP needed for ₹1 crore</h3>" + tbl(["Years", "At 10%", "At 12%", "At 15%"], [(f"{y}", *[inr(10000000 / sip(1, r, y)[0]) for r in (10, 12, 15)]) for y in (10, 15, 20, 25, 30)]),
 faqs=[("How is SIP return calculated?", "With FV = P × [((1 + i)ⁿ − 1) ÷ i] × (1 + i), where P is the monthly SIP, i is the monthly return and n the number of months. ₹10,000 a month for 15 years at 12% gives about ₹50.5 lakh."),
       ("What is a good SIP return?", "Indian equity mutual funds have historically returned around 10–14% a year over long periods, but returns vary and past performance doesn't guarantee future results. Debt funds have typically returned 6–8%."),
       ("What is a step-up SIP?", "A SIP where you raise the monthly amount each year by a fixed percentage or amount, usually as your income grows. It can greatly increase your final corpus."),
       ("Is SIP better than a lump sum?", "A SIP spreads your investment over time, so you buy at different prices and don't need a large amount upfront. A lump sum invested early can earn more if markets rise, but carries more timing risk.")],
 related=["compound", "emi", "savings", "retire"])

BYID.update({t["id"]: t for t in T})
qa.QA.update({
 "vadisab": ("How is a combined VA disability rating calculated?", f"VA combines ratings highest first, each applied to the remaining able percentage, then rounds to the nearest 10. 50%, 30% and 10% make {e1}%, rounded to {c1}%, which pays {usd(A[c1 // 10 - 1])} a month for a veteran alone in 2026."),
 "timecalc": ("How do you add hours and minutes?", "Convert to minutes, add, and convert back: 2:45 + 1:30 = 165 + 90 = 255 minutes = 4 hours 15 minutes. For every 60 minutes, carry 1 hour."),
 "invoice": ("How do I create an invoice for free?", "Enter your details, your client's, an invoice number, dates and each item with quantity and price, then add tax or a discount. Numbrik's invoice generator totals it and saves it as a PDF, free and without sign-up."),
 "emi": ("How is EMI calculated?", f"EMI = P × r × (1 + r)ⁿ ÷ ((1 + r)ⁿ − 1), with r the monthly rate and n the months. A ₹25 lakh loan at 8.5% for 20 years has an EMI of {inr(emi(2500000, 8.5, 240))}."),
 "sip": ("How much will my SIP grow?", f"At 12% a year, ₹10,000 a month for 15 years grows to about {inr(v1)} on {inr(i1)} invested. The formula is FV = P × [((1 + i)ⁿ − 1) ÷ i] × (1 + i)."),
})
for _k in ("hours", "timecard", "timedec"):
    if _k in BYID and "timecalc" not in BYID[_k]["related"]: BYID[_k]["related"] = ["timecalc"] + BYID[_k]["related"][:3]
for _k in ("loan", "autoloan", "gloan"):
    if _k in BYID and "emi" not in BYID[_k]["related"]: BYID[_k]["related"] = BYID[_k]["related"][:3] + ["emi"]
for _k in ("compound", "savings"):
    if _k in BYID and "sip" not in BYID[_k]["related"]: BYID[_k]["related"] = BYID[_k]["related"][:3] + ["sip"]
