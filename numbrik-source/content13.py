"""Semrush keyword overview for "calculator" (US, November 2026) showed two easy wins:
"calorie calculator" (4.1M searches, KD 5) and "how much house can I afford calculator" (49.5K, KD 11).
This module strengthens the calorie page and adds a house affordability calculator. Imported after tweaks.
Calorie needs table: Dietary Guidelines for Americans 2020–2025, Appendix 2 (estimated calorie needs)."""
from content import tool, T, BYID

def tbl(head, rows):
    return ('<div class="tbl"><table><thead><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")

# ---------------- Calorie calculator upgrade ----------------
c = BYID["calorie"]
c["title"] = "Calorie Calculator – How Many Calories Do I Need? | Numbrik"
c["h1"] = "Calorie Calculator"
c["meta"] = "Free calorie calculator: find how many calories you need a day to maintain, lose or gain weight, based on your age, sex, height, weight and activity. With charts."
c["lede"] = ("How many calories should you eat a day? Enter your age, sex, height, weight and activity level to get your maintenance calories, "
             "plus daily targets to lose or gain ½, 1 or 2 pounds a week. Charts below show typical needs by age and how many calories common activities burn.")
F = [("19–25", 2000, 2200, 2400), ("26–30", 1800, 2000, 2400), ("31–50", 1800, 2000, 2200), ("51–60", 1600, 1800, 2200), ("61 and over", 1600, 1800, 2000)]
M = [("19–20", 2600, 2800, 3000), ("21–25", 2400, 2800, 3000), ("26–35", 2400, 2600, 3000), ("36–40", 2400, 2600, 2800), ("41–45", 2200, 2600, 2800),
     ("46–55", 2200, 2400, 2800), ("56–60", 2200, 2400, 2600), ("61–65", 2000, 2400, 2600), ("66–75", 2000, 2200, 2600), ("76 and over", 2000, 2200, 2400)]
f = lambda rows: tbl(["Age", "Sedentary", "Moderately active", "Active"], [(a, f"{x:,}", f"{y:,}", f"{z:,}") for a, x, y, z in rows])
# Calories burned in 30 minutes = MET × kg × 0.5 h, MET values from the 2011 Compendium of Physical Activities.
MET = [("Walking, 3.5 mph", 4.3), ("Walking, 4 mph (brisk)", 5.0), ("Cycling, 12–13.9 mph", 8.0), ("Running, 5 mph (12 min/mile)", 8.3),
       ("Running, 6 mph (10 min/mile)", 9.8), ("Swimming laps, light to moderate", 5.8), ("Weight lifting, moderate", 3.5), ("Yoga (hatha)", 2.5), ("Gardening, general", 3.8), ("Elliptical, moderate", 5.0)]
B = [(a_, *[round(m * lb * 0.4536 * 0.5) for lb in (125, 155, 185)]) for a_, m in MET]
c["extra"] += ("<h3>How many calories do I need a day by age?</h3><p>Typical daily needs from the US Dietary Guidelines, for a reference-size adult. "
  "Sedentary means only everyday activity; moderately active is about the equivalent of walking 1.5–3 miles a day; active is more than 3 miles a day. Your own number can be a few hundred calories higher or lower.</p>"
  "<h3>Women</h3>" + f(F) + "<h3>Men</h3>" + f(M) +
  "<h3>Calories burned in 30 minutes</h3><p>Estimated from MET values in the Compendium of Physical Activities (calories = MET × weight in kg × hours).</p>" + tbl(["Activity", "125 lb person", "155 lb person", "185 lb person"], [(a, x, y, z) for a, x, y, z in B]) +
  "<h3>Calories in each macronutrient</h3>" + tbl(["Nutrient", "Calories per gram"], [("Protein", "4"), ("Carbohydrate", "4"), ("Fat", "9"), ("Alcohol", "7"), ("Fibre", "About 2")]) +
  "<h3>Tips for hitting your calorie target</h3><ul><li>Weigh foods for a week or two; portion sizes are where most estimates go wrong.</li>"
  "<li>Prioritise protein and vegetables: they fill you up for fewer calories.</li><li>Count drinks: a large latte or a soda can be 200–300 calories.</li>"
  "<li>Weigh yourself at the same time several days a week and look at the weekly average, not single days.</li><li>Recalculate after every 10 lb (4–5 kg) of change.</li></ul>")
c["faqs"] = c["faqs"] + [
  ("How many calories should I eat to lose weight?", "About 500 fewer than your maintenance calories a day to lose roughly 1 lb a week. Use the “Weight loss” line in the result. Don't go below 1,200 calories a day (women) or 1,500 (men) without medical supervision."),
  ("How many calories should a woman eat a day?", "Most adult women need about 1,600 to 2,400 calories a day, depending on age, size and activity. A moderately active woman of 31 to 50 needs about 2,000."),
  ("How many calories should a man eat a day?", "Most adult men need about 2,000 to 3,000 calories a day. A moderately active man of 26 to 35 needs about 2,600."),
  ("Do I eat back the calories I burn exercising?", "Not separately: the activity level you choose already includes your usual exercise. Fitness trackers often overestimate calories burned, so be careful adding them on top.")]
c["related"] = ["tdee", "deficit", "macro", "bmr"]

# ---------------- House affordability ----------------
def afford(inc, debt, down, rate, yrs=30, tax=1.1, ins=1800, hoa=0, front=.28, back=.36):
    r = rate / 1200; n = yrs * 12; k = r / (1 - (1 + r) ** -n)
    Mx = min(inc / 12 * front, inc / 12 * back - debt); fixed = ins / 12 + hoa; pm = 0.005 / 12
    H = (Mx - fixed + down * (k + pm)) / (k + tax / 1200 + pm)
    if down >= 0.2 * H: H = (Mx - fixed + down * k) / (k + tax / 1200)
    return H
def p10(inc, debt=300, rate=6.5, tax=1.1, ins=1800):
    r = rate / 1200; k = r / (1 - (1 + r) ** -360); pm = 0.005 / 12
    Mx = min(inc / 12 * .28, inc / 12 * .36 - debt)
    return (Mx - ins / 12) / (0.9 * (k + pm) + tax / 1200)
e = afford(100000, 500, 40000, 6.5)
tool(id="afford", slug="house-affordability-calculator", cat="Money", name="House Affordability Calculator",
 short="How much house can I afford", desc="How much house you can afford on your income.",
 title="How Much House Can I Afford? Affordability Calculator",
 h1="How Much House Can I Afford?",
 meta="Find out how much house you can afford from your income, debts, down payment and mortgage rate, using the 28/36 rule lenders use. Includes taxes, insurance and PMI.",
 lede="Find a realistic home price for your budget. Enter your income, monthly debts, down payment and mortgage rate, and the calculator applies the debt-to-income rules lenders use, including property tax, insurance, HOA fees and PMI.",
 steps=["Enter your yearly household income before tax.", "Add your monthly debt payments, such as car, student loan and credit card minimums.", "Enter your down payment, mortgage rate and term.", "Adjust property tax, insurance and HOA for the area you're looking in, then read your maximum home price."],
 how="""<p>Lenders look at two debt-to-income (DTI) ratios. The 28/36 rule says your housing costs (mortgage principal and interest, property tax, insurance, HOA and PMI) shouldn't be more than 28% of your gross monthly income, and all your debts together shouldn't be more than 36%. FHA loans and many lenders allow more, often around 31/43, and sometimes higher with strong credit or savings.</p>
<p>The calculator takes the lower of the two limits as your maximum monthly payment, then works backwards to the home price that payment supports. With less than 20% down it adds an estimate for private mortgage insurance (PMI). Just because a lender will approve an amount doesn't mean it's comfortable: leave room for repairs, savings and closing costs, which are typically 2–5% of the price.</p>""",
 formula="Max housing payment = lower of\n  28% × monthly income\n  36% × monthly income − other debts\nHome price = down payment + loan the payment supports\n(after property tax, insurance, HOA and PMI)",
 example=f"<p>A household earning <strong>$100,000</strong> a year with <strong>$500</strong> of monthly debts and <strong>$40,000</strong> down, at a <strong>6.5%</strong> 30-year rate: 28% of $8,333 is $2,333 and 36% minus debts is $2,500, so the limit is $2,333 a month. After taxes, insurance and PMI that supports a home of about <strong>${round(e, -3):,.0f}</strong>.</p>",
 extra="<h3>How much house can I afford by income?</h3><p>Home price under the 28/36 rule with $300 a month of other debts, 10% down, a 6.5% 30-year mortgage, 1.1% property tax and $1,800 a year insurance.</p>" +
 tbl(["Annual income", "Max housing payment", "Home price (approx.)", "Down payment (10%)"],
   [(f"${i:,}", f"${min(i / 12 * .28, i / 12 * .36 - 300):,.0f}/mo", f"${round(p10(i), -3):,.0f}", f"${round(p10(i) * .1, -3):,.0f}") for i in (40000, 50000, 60000, 75000, 90000, 100000, 120000, 150000, 175000, 200000, 250000)]),
 faqs=[("How much house can I afford on a $100,000 salary?", f"Roughly ${round(p10(100000), -3):,.0f} with 10% down, a 6.5% rate and $300 of other monthly debts, using the 28/36 rule. More debt or higher taxes lower that; a bigger down payment raises it."),
       ("What is the 28/36 rule?", "Spend no more than 28% of your gross monthly income on housing and no more than 36% on all debts combined, including housing."),
       ("How much should I put down on a house?", "20% avoids PMI on a conventional loan, but many buyers put down 3–10%. FHA loans need as little as 3.5% with a credit score of 580 or higher."),
       ("Does the calculator include closing costs?", "No. Budget another 2–5% of the price for closing costs, plus moving costs and an emergency fund.")],
 related=["loan", "gloan", "salary", "compound"])

BYID.update({t["id"]: t for t in T})
