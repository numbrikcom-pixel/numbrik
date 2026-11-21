"""Insurance section (Nov 21, 2026): term life, car and home insurance calculators.
Data: MoneyGeek term life rates (updated Nov 20, 2026); NerdWallet car insurance state averages and driver-profile
averages (Nov 2026 analysis); Insurify home insurance state averages at $300k dwelling (Nov 17, 2026); Insurance.com
national averages by dwelling coverage and deductible (Sep 15, 2026); NerdWallet claim surcharge (10%); ABI UK motor
(£562, Q3 2026) and home (£389 combined, £310 buildings, £118 contents, Q3 2026) premium trackers."""
from content import tool, T, BYID, ORDER
import cats, qa

if "Insurance" not in ORDER: ORDER.insert(ORDER.index("Money") + 1, "Insurance")
cats.CATS["Insurance"] = ("insurance-calculators", "Insurance Calculators",
  "Estimate what insurance should cost and how much cover you need, before you ask for quotes. Work out how much term life insurance your family would need and what it may cost at your age, estimate car insurance by state, age and driving record, and estimate homeowners insurance from your state, rebuild cost and deductible. Every estimate shows the average it starts from and the source of the data.",
  [])

def tbl(head, rows):
    return ('<div class="tbl"><table><thead><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")
usd = lambda x: f"${x:,.0f}"
def sources(lst): return '<h3 id="sources">Sources</h3><ul class="sources">' + "".join(f'<li><a href="{u}" rel="noopener">{n}</a></li>' for n, u in lst) + "</ul>"
DISC = '<p class="hint"><strong>Not insurance advice.</strong> Numbrik is not an insurance company, agent or broker and doesn\'t sell policies. Figures are averages to help you plan; only an insurer can give you a real price.</p>'

# ---------------------------------------------------------------- data (same as src/tools18.js)
AG = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65]
T20 = {"f": [22, 23, 24, 29, 37, 54, 79, 127, 204, 336], "m": [28, 29, 30, 36, 44, 67, 103, 174, 293, 500]}
T10 = {"f": [17, 17, 17, 21, 25, 36, 52, 76, 112, 192], "m": [21, 21, 21, 25, 29, 43, 65, 102, 161, 281]}
T30 = {"f": [35, 35, 37, 46, 57, 89, 137, 211, None, None], "m": [44, 44, 46, 58, 73, 118, 189, 294, None, None]}
C250 = {"f": [15, 15, 16, 18, 22, 31, 44, 69, 110, 180], "m": [18, 18, 18, 22, 26, 38, 56, 94, 157, 260]}
C1M = {"f": [38, 38, 40, 51, 65, 97, 145, 236, 390, 657], "m": [51, 51, 52, 65, 80, 125, 195, 329, 561, 977]}
SMK = {"f": [65, 65, 71, 92, 119, 180, 271, 418, 646, 969], "m": [83, 83, 87, 116, 154, 241, 379, 592, 926, 1401]}
CAR = {"Alabama": (2259, 492), "Alaska": (1837, 383), "Arizona": (2942, 937), "Arkansas": (2644, 546), "California": (1884, 625), "Colorado": (3283, 742), "Connecticut": (2871, 1008), "Delaware": (2643, 1056), "Florida": (3151, 856), "Georgia": (3160, 1056), "Hawaii": (1975, 603), "Idaho": (1999, 434), "Illinois": (2520, 744), "Indiana": (1920, 512), "Iowa": (2250, 398), "Kansas": (2530, 625), "Kentucky": (3298, 836), "Louisiana": (4290, 1256), "Maine": (1711, 534), "Maryland": (3043, 1108), "Massachusetts": (1866, 628), "Michigan": (2952, 697), "Minnesota": (2508, 650), "Mississippi": (2502, 594), "Missouri": (2622, 699), "Montana": (2879, 453), "Nebraska": (2002, 424), "Nevada": (3497, 1033), "New Hampshire": (1578, 458), "New Jersey": (3718, 1608), "New Mexico": (2203, 505), "New York": (2679, 1022), "North Carolina": (1789, 598), "North Dakota": (2423, 507), "Ohio": (1795, 506), "Oklahoma": (2221, 496), "Oregon": (2207, 972), "Pennsylvania": (2208, 441), "Rhode Island": (3226, 873), "South Carolina": (2473, 695), "South Dakota": (2237, 377), "Tennessee": (2181, 538), "Texas": (3640, 1079), "Utah": (2435, 906), "Vermont": (1556, 429), "Virginia": (2163, 772), "Washington": (2323, 695), "Washington, D.C.": (2655, 892), "West Virginia": (2274, 680), "Wisconsin": (2335, 559), "Wyoming": (1148, 192)}
HOME = {"Alabama": 3408, "Alaska": 1308, "Arizona": 2172, "Arkansas": 3420, "California": 2040, "Colorado": 3120, "Connecticut": 2028, "Delaware": 1260, "Florida": 6324, "Georgia": 2496, "Hawaii": 1476, "Idaho": 1740, "Illinois": 2544, "Indiana": 2196, "Iowa": 2700, "Kansas": 3960, "Kentucky": 3240, "Louisiana": 4872, "Maine": 1224, "Maryland": 1932, "Massachusetts": 1968, "Michigan": 2196, "Minnesota": 2616, "Mississippi": 3264, "Missouri": 2844, "Montana": 2556, "Nebraska": 4020, "Nevada": 1296, "New Hampshire": 1176, "New Jersey": 1236, "New Mexico": 3168, "New York": 1404, "North Carolina": 3228, "North Dakota": 2592, "Ohio": 1692, "Oklahoma": 5424, "Oregon": 1332, "Pennsylvania": 1284, "Rhode Island": 2412, "South Carolina": 2736, "South Dakota": 2616, "Tennessee": 3060, "Texas": 4452, "Utah": 1524, "Vermont": 948, "Virginia": 1644, "Washington": 1392, "Washington, D.C.": 1152, "West Virginia": 1536, "Wisconsin": 1488, "Wyoming": 1692}

def need(inc, yrs, mort, debt, kids, edu, fin, sav):
    n = inc * yrs + mort + debt + kids * edu + fin; net = max(0, n - sav)
    return n, net, -(-net // 50000) * 50000
N1, NET1, COV1 = need(75000, 15, 220000, 15000, 2, 60000, 15000, 40000)

# ---------------------------------------------------------------- Term life
tool(id="lifeins", slug="life-insurance-calculator", cat="Insurance", name="Life Insurance Calculator",
 short="Life insurance", desc="How much term life cover you need, and what it may cost.",
 h1="Life Insurance Calculator: How Much Term Life Do You Need?",
 title="Life Insurance Calculator – How Much Do I Need? | Numbrik",
 meta="Free term life insurance calculator: find how much cover your family needs, the right term length, and 2026 average monthly costs by age.",
 lede="Work out how much term life insurance would protect your family if you died, and which term length fits. Add your income, debts and what your children will need, subtract what you already have, and see a coverage amount, a suggested term and, in the US, what that policy typically costs at your age.",
 steps=["Choose your currency: US, UK or Canadian dollars.", "Enter your yearly income and how many years your family would rely on it, usually until your youngest child is independent.", "Add your mortgage balance, other debts, college costs and final expenses.", "Subtract savings and any life insurance you already have, such as cover through work.", "In the US, add your age, sex and smoking status to see a typical monthly cost."],
 how="""<p>A life insurance payout has one job: to let the people who depend on you carry on without your income. This calculator uses a needs-based method, a version of what planners call the DIME method (Debt, Income, Mortgage, Education). It adds up <strong>your income for the years your family would need it</strong>, the <strong>mortgage</strong> and <strong>other debts</strong> they'd want to clear, <strong>education</strong> for each child and <strong>final expenses</strong> such as a funeral. It then subtracts savings, investments and existing life cover, and rounds up to the nearest $50,000, since policies are sold in round amounts.</p>
<p>The term should last as long as the need does. If your youngest child is 5 and you want cover until they're 22, a 20-year term fits; if your mortgage has 25 years left, consider 25 or 30. Term life is the simplest and cheapest kind: you pay a fixed premium for the term, and the policy pays out only if you die during it. Permanent policies (whole and universal life) cost several times more for the same cover.</p>
<p>The cost estimate uses average 2026 monthly rates for nonsmokers in good health, by age and sex, for $250,000, $500,000 and $1 million policies over 10, 20 and 30 years, and fills in amounts and ages in between. It shows a range of ±15% because insurers price your exact health class after a medical questionnaire or exam. Smoking multiplies the price about three times.</p>""",
 formula="Need = income × years + mortgage + other debts + (children × college cost) + final expenses\nCover = need − savings − existing life insurance (rounded up to $50,000)\nTerm = shortest of 10/15/20/25/30 years that covers the years needed",
 example=f"<p>A 35-year-old earning <strong>$75,000</strong> wants to support the family for <strong>15 years</strong>, has a $220,000 mortgage, $15,000 of other debt, two children ($60,000 each for college) and $15,000 for final costs. That's {usd(N1)}. Minus $40,000 of savings and existing cover, the need is {usd(NET1)}, so a <strong>{usd(COV1)}, 15-year term policy</strong> fits. For a healthy nonsmoking man, a 20-year, $1 million policy averages about <strong>$65 a month</strong> at 35.</p>",
 extra='<h3 id="cost-by-age">Average monthly cost of a $500,000, 20-year term policy (2026)</h3><p>Nonsmokers in good health. Prices roughly double every 8–10 years after 40, so buying younger locks in a lower rate for the whole term.</p>' +
   tbl(["Age", "Women", "Men", "Men who smoke"], [(a, f"${T20['f'][i]}", f"${T20['m'][i]}", f"${SMK['m'][i]}") for i, a in enumerate(AG)]) +
   '<h3 id="by-term">How term length and cover change the price (men, nonsmoker)</h3>' +
   tbl(["Age", "$250k, 20 yr", "$500k, 10 yr", "$500k, 30 yr", "$1M, 20 yr"], [(a, f"${C250['m'][i]}", f"${T10['m'][i]}", f"${T30['m'][i]}" if T30['m'][i] else "—", f"${C1M['m'][i]}") for i, a in enumerate(AG) if a >= 25]) +
   '<h3 id="rules">Quick rules of thumb, and why they fall short</h3><ul><li><strong>10× your income</strong> is a common shortcut. It ignores your mortgage, savings and how long your family needs support, so it can be far too much or too little.</li>'
   "<li><strong>Stay-at-home parents need cover too.</strong> Replacing childcare and household work can cost $30,000 or more a year; enter that as income.</li>"
   "<li><strong>Cover through work is usually 1–2× salary</strong> and ends if you leave the job, so count it, but don't rely on it alone.</li></ul>"
   '<h3 id="uk-canada">In the UK and Canada</h3><p>The coverage method works the same way: use the £ or C$ setting. In the UK, consider a decreasing term policy if the main need is a repayment mortgage, and ask for the policy to be written in trust so the payout can avoid inheritance tax and probate delays. In Canada, term life payouts to a named beneficiary are generally tax-free.</p>' + DISC +
   sources([("MoneyGeek: Average life insurance cost in 2026 (updated Nov 20, 2026)", "https://www.moneygeek.com/insurance/life/rates/")]),
 faqs=[("How much life insurance do I need?", f"Enough to replace your income for the years your family depends on it, clear your mortgage and debts, fund education and pay final costs, minus your savings and existing cover. For a typical family with a $75,000 income that's often $1 million to $1.5 million."),
       ("How much does term life insurance cost?", "A healthy 35-year-old nonsmoker pays about $29–$36 a month for a $500,000, 20-year policy in 2026. At 50 it's about $79–$103, and smokers pay about three times as much."),
       ("How long should my term be?", "Long enough to cover your longest money commitment: until your youngest child finishes school or your mortgage is paid off. Most families choose 20 or 30 years."),
       ("Is term or whole life insurance better?", "For most families, term. It costs a fraction of whole life for the same cover. Whole life adds lifelong cover and a cash value, which mainly suits estate planning or special needs."),
       ("Is a life insurance payout taxable?", "In the US and Canada, a death benefit paid to a named beneficiary is generally not income tax. In the UK, it can count toward inheritance tax unless the policy is written in trust.")],
 related=["carins", "homeins", "retire", "savings"],
 cite=[("MoneyGeek: Average life insurance cost in 2026", "https://www.moneygeek.com/insurance/life/rates/")],
 about=[("Term life insurance", "https://en.wikipedia.org/wiki/Term_life_insurance")])

# ---------------------------------------------------------------- Car
_c = sorted(CAR.items(), key=lambda x: x[1][0])
tool(id="carins", slug="car-insurance-calculator", cat="Insurance", name="Car Insurance Calculator",
 short="Car insurance", desc="Estimate your car insurance cost by state and driver profile.",
 h1="Car Insurance Calculator: Estimate Your Premium",
 title="Car Insurance Calculator 2026 – Cost by State | Numbrik",
 meta="Free car insurance calculator: estimate your 2026 premium by state, age, coverage, driving record and credit, with average costs for every state.",
 lede="Estimate what car insurance should cost you before you shop. Pick your state, age, coverage level, driving record and credit, and see an estimated yearly and monthly premium, how each factor moves it, and the state average it starts from. UK drivers see the latest national average price paid.",
 steps=["Choose the United States or the United Kingdom.", "Pick your state and enter the driver's age.", "Choose full coverage (liability plus collision and comprehensive) or your state's minimum.", "Set your credit and your driving record for the last 3–5 years.", "Read your estimated premium, the monthly cost and the typical range of quotes."],
 how="""<p>The estimate starts from the <strong>average premium in your state</strong> for a 35-year-old driver with a clean record and good credit, from a November 2026 rate analysis. It then applies the average effect of each factor in that analysis. Age matters most for young drivers: a 20-year-old pays about twice as much as a 35-year-old, and prices ease slowly into your 60s before rising a little again. One <strong>speeding ticket</strong> adds about 28%, an <strong>at-fault accident</strong> about 49% and a <strong>DUI</strong> about 88% to a full-coverage premium.</p>
<p><strong>Credit</strong> is a big factor in most states: drivers with poor credit pay about 67% more for full coverage than drivers with good credit, even with a clean record. California, Hawaii, Massachusetts and Michigan don't allow insurers to use credit for car insurance, so the calculator ignores it there.</p>
<p><strong>Full coverage</strong> adds collision and comprehensive to liability, so it repairs or replaces your own car, and lenders require it on a financed or leased car. <strong>Minimum coverage</strong> is the legal minimum liability in your state; it's far cheaper but pays nothing toward your own car. Your real quote also depends on your car's make and model, your ZIP code, how far you drive and the insurer, which is why the result shows a ±20% range.</p>""",
 formula="Estimate = state average × age factor × driving record factor × credit factor\nRecord (full coverage): ticket ×1.28, accident ×1.49, DUI ×1.88\nPoor credit: ×1.67 (not used in CA, HI, MA, MI)",
 example=f"<p>A <strong>35-year-old in Texas</strong> with a clean record and good credit pays about <strong>{usd(CAR['Texas'][0])} a year</strong> for full coverage, or {usd(CAR['Texas'][0] / 12)} a month. After one at-fault accident, that rises to about {usd(CAR['Texas'][0] * 1.491)}; at age 20 with a clean record, about {usd(CAR['Texas'][0] * 2)}.</p>",
 extra='<h3 id="by-state">Average car insurance cost by state (2026)</h3><p>35-year-old driver, clean record, good credit, yearly premium.</p>' +
   tbl(["State", "Full coverage", "Minimum coverage", "Full, per month"], [(s, usd(f), usd(m), usd(f / 12)) for s, (f, m) in _c]) +
   '<h3 id="factors">What raises or lowers your premium</h3>' +
   tbl(["Factor", "Full coverage", "Minimum coverage"], [("Good driver, age 35 (baseline)", "$2,357", "$650"), ("Age 20", "$4,712", "$1,340"), ("Age 60", "$2,024", "$590"), ("One speeding ticket", "$3,022", "$843"), ("One at-fault accident", "$3,514", "$952"), ("One DUI", "$4,424", "$1,230"), ("Poor credit", "$3,939", "$1,032")]) +
   '<h3 id="save">Six ways to pay less</h3><ol><li>Get at least three quotes at every renewal; prices for the same driver vary by hundreds of dollars between insurers.</li><li>Raise your collision and comprehensive deductible from $500 to $1,000 if you can afford it after an accident.</li><li>Bundle car and home or renters insurance with one company.</li><li>Ask about good-driver, good-student, low-mileage and safety-course discounts.</li><li>Drop collision and comprehensive on an old car worth less than about ten times the yearly cost of that cover.</li><li>Keep your credit healthy, in states where insurers use it.</li></ol>' +
   '<h3 id="uk-canada">UK and Canada</h3><p>In the UK, the average price paid for comprehensive car insurance was <strong>£562 a year</strong> in July–September 2026, according to the Association of British Insurers, which tracks about 28 million policies. Building a no-claims bonus and comparing quotes about three weeks before renewal usually lowers the price. In Canada, rules differ by province: British Columbia, Saskatchewan and Manitoba have public basic insurance, Quebec covers injuries through a public plan, and Ontario and Alberta have some of the highest private premiums.</p>' + DISC +
   sources([("NerdWallet: Average cost of car insurance (Nov 2026 rate analysis)", "https://www.nerdwallet.com/insurance/auto/average-car-insurance-cost"), ("ABI: Motor insurance premium tracker, Q3 2026", "https://www.abi.org.uk/media-hub/news-post/motor-insurance-payouts-remain-at-32-billion-for-second-consecutive-quarter")]),
 faqs=[("How much is car insurance per month?", "About $196 a month for full coverage and $54 for minimum coverage for a 35-year-old with a clean record in 2026, but state matters a lot: from about $96 a month in Wyoming to $358 in Louisiana."),
       ("Why is car insurance so expensive for young drivers?", "Drivers under 25 have far more crashes per mile driven, so insurers charge them more. A 20-year-old pays about twice what a 35-year-old pays; staying on a parent's policy is usually cheaper."),
       ("How much does an accident raise car insurance?", "One at-fault accident raises a full-coverage premium by about 49% on average, and the surcharge usually lasts three to five years."),
       ("What's the difference between full and minimum coverage?", "Minimum coverage is only the liability insurance your state requires, which pays for damage you cause to others. Full coverage adds collision and comprehensive, which pay to repair or replace your own car."),
       ("Is this calculator a quote?", "No. It's an estimate from average rates. Your actual price depends on your car, ZIP code, mileage, claims history and the insurer, so compare quotes before you buy.")],
 related=["lifeins", "homeins", "autoloan", "lease"],
 cite=[("NerdWallet: Average cost of car insurance", "https://www.nerdwallet.com/insurance/auto/average-car-insurance-cost"), ("Association of British Insurers: Motor insurance premium tracker", "https://www.abi.org.uk/media-hub/news-post/motor-insurance-payouts-remain-at-32-billion-for-second-consecutive-quarter")],
 about=[("Vehicle insurance", "https://en.wikipedia.org/wiki/Vehicle_insurance")])

# ---------------------------------------------------------------- Home
_h = sorted(HOME.items(), key=lambda x: x[1])
CV = [(200000, .751), (300000, 1), (400000, 1.246), (600000, 1.727), (1000000, 2.68)]
tool(id="homeins", slug="home-insurance-calculator", cat="Insurance", name="Home Insurance Calculator",
 short="Home insurance", desc="Estimate homeowners insurance by state, coverage and deductible.",
 h1="Home Insurance Calculator: Estimate Your Homeowners Premium",
 title="Home Insurance Calculator 2026 – Cost by State | Numbrik",
 meta="Free home insurance calculator: estimate your 2026 homeowners premium from your state, rebuild cost, deductible and claims, with averages by state.",
 lede="Estimate what homeowners insurance should cost before you get quotes. Choose your state, enter the cost to rebuild your home, pick a deductible and your claims history, and see an estimated yearly and monthly premium. UK homeowners see the latest average prices for buildings and contents cover.",
 steps=["Choose the United States or the United Kingdom.", "Pick your state and enter your dwelling coverage, the cost to rebuild your home, or enter its size and a rebuild cost per square foot.", "Choose your deductible: the amount you pay toward each claim.", "Say how many claims you've made in the last five years.", "Read your estimated premium, monthly cost and cost per $1,000 of coverage."],
 how="""<p>The estimate starts from the <strong>average premium in your state</strong> for $300,000 of dwelling coverage with a $1,000 deductible, no recent claims and good credit, from November 2026 rate data. It then scales for your <strong>coverage amount</strong>: premiums rise more slowly than coverage, so $600,000 of cover costs about 1.7 times as much as $300,000, not twice as much. A <strong>$500 deductible</strong> adds about 7%; raising it to <strong>$2,500</strong> saves about 9%, and $5,000 about 20%. One recent claim adds about 10%.</p>
<p><strong>Dwelling coverage</strong> should equal the cost to rebuild your home from the ground up at today's labour and material prices, not its market value, which includes land. Ask your insurer for a replacement-cost estimate, or multiply the floor area by a local rebuild cost per square foot from a builder. Being underinsured is risky: many policies pay less on every claim if your cover is well below the rebuild cost.</p>
<p>Where you live matters most. Hurricanes, hail, tornadoes and wildfires push premiums in Florida, Oklahoma, Louisiana, Texas and the Plains far above average, while Vermont and New Hampshire pay a fraction as much. Standard policies don't cover <strong>flood</strong> or <strong>earthquake</strong> damage; those need separate cover. Your real quote also depends on the age of your roof, construction type, distance to a fire station, credit (in most states) and the insurer, so the result shows a ±25% range.</p>""",
 formula="Estimate = state average ($300k) × coverage factor × deductible factor × claims factor\nCoverage factor: $200k ×0.75, $400k ×1.25, $600k ×1.73, $1M ×2.68\nDeductible: $500 ×1.07, $2,500 ×0.91, $5,000 ×0.80 · One claim ×1.10",
 example=f"<p>A home in <strong>Texas</strong> with <strong>$400,000</strong> of dwelling coverage and a $1,000 deductible costs about {usd(4452)} × 1.25 = <strong>{usd(4452 * 1.246)} a year</strong>, or {usd(4452 * 1.246 / 12)} a month. Raising the deductible to $2,500 cuts that to about {usd(4452 * 1.246 * .91)}.</p>",
 extra='<h3 id="by-state">Average homeowners insurance cost by state (2026)</h3><p>$300,000 dwelling coverage, $1,000 deductible, no claims, good credit, yearly premium.</p>' +
   tbl(["State", "Per year", "Per month"], [(s, usd(v), usd(v / 12)) for s, v in _h]) +
   '<h3 id="by-coverage">National average by coverage amount</h3>' +
   tbl(["Dwelling coverage", "$1,000 deductible", "$2,500 deductible"], [("$200,000", "$2,156", "$1,933"), ("$300,000", "$2,872", "$2,621"), ("$400,000", "$3,579", "$3,279"), ("$600,000", "$4,960", "$4,577")]) +
   '<h3 id="coverages">What a standard policy covers</h3>' +
   tbl(["Part", "Covers", "Typical limit"], [("Dwelling (A)", "The house and attached structures", "Your rebuild cost"), ("Other structures (B)", "Fences, sheds, detached garage", "10% of dwelling"), ("Personal property (C)", "Furniture, clothes, electronics", "50–70% of dwelling"), ("Loss of use (D)", "Hotel and extra living costs while you can't live at home", "20–30% of dwelling"), ("Liability (E)", "Injuries to others and damage you cause", "$100,000–$500,000"), ("Medical payments (F)", "Guests' minor medical bills", "$1,000–$5,000")]) +
   '<h3 id="uk-canada">UK and Canada</h3><p>In the UK, the average combined buildings and contents policy cost <strong>£389 a year</strong> in July–September 2026, buildings-only cover £310 and contents-only cover £118, according to the Association of British Insurers. Mortgage lenders require buildings insurance; insure for the rebuild cost, which you can estimate with the BCIS calculator. In Canada, premiums vary widely by province and city, and overland flood and sewer backup are usually optional add-ons worth checking.</p>' + DISC +
   sources([("Insurify: Average home insurance rates by state (Nov 17, 2026)", "https://insurify.com/homeowners-insurance/states/"), ("Insurance.com: Average homeowners insurance rates (Sep 15, 2026)", "https://www.insurance.com/home-and-renters-insurance/home-insurance-basics/average-homeowners-insurance-rates-by-state"), ("NerdWallet: What is a home insurance deductible?", "https://www.nerdwallet.com/article/insurance/homeowners-insurance-deductible"), ("Which?: ABI home insurance premiums, Q3 2026", "https://www.which.co.uk/news/article/whats-happening-to-home-insurance-premiums-a3EjJ5O6GVvP")]),
 faqs=[("How much is homeowners insurance per month?", "About $231 a month on average in the US for $300,000 of dwelling coverage in 2026, from about $79 in Vermont to $527 in Florida."),
       ("How much homeowners insurance do I need?", "Enough dwelling coverage to rebuild your home completely at today's costs, plus liability of at least $300,000. Market value doesn't matter, because it includes the land, which can't burn down."),
       ("Does a higher deductible save money?", "Yes. Moving from $1,000 to $2,500 saves about 9% on average. Choose a deductible you could pay from savings the week after a loss."),
       ("Does homeowners insurance cover floods?", "No. Standard policies exclude flooding. In the US, flood cover comes from the National Flood Insurance Program or private flood insurers, usually with a 30-day wait."),
       ("Is this calculator a quote?", "No. It's an estimate from state averages. Roof age, construction, local risks, credit and the insurer all change the price, so compare quotes before you buy.")],
 related=["lifeins", "carins", "afford", "loan"],
 cite=[("Insurify: Average home insurance rates by state", "https://insurify.com/homeowners-insurance/states/"), ("Insurance.com: Average homeowners insurance rates by state", "https://www.insurance.com/home-and-renters-insurance/home-insurance-basics/average-homeowners-insurance-rates-by-state")],
 about=[("Home insurance", "https://en.wikipedia.org/wiki/Home_insurance")])

BYID.update({t["id"]: t for t in T})
qa.QA.update({
 "lifeins": ("How much life insurance do I need?", "Add your income for the years your family would need it, your mortgage and debts, children's education and final costs, then subtract savings and existing cover. A $75,000 earner supporting a family for 15 years with a $220,000 mortgage often needs about $1.5 million."),
 "carins": ("How much is car insurance?", "The US average for a 35-year-old with a clean record and good credit is about $2,357 a year for full coverage and $650 for minimum coverage in 2026. An at-fault accident adds about 49%, and a 20-year-old pays about twice as much."),
 "homeins": ("How much is homeowners insurance?", "About $2,772 a year on average in the US for $300,000 of dwelling coverage with a $1,000 deductible in 2026, from $948 in Vermont to $6,324 in Florida. In the UK, combined buildings and contents averaged £389 a year."),
})
for _k, _r in (("autoloan", "carins"), ("lease", "carins"), ("afford", "homeins"), ("loan", "homeins"), ("retire", "lifeins")):
    if _k in BYID and _r not in BYID[_k]["related"]: BYID[_k]["related"] = BYID[_k]["related"][:3] + [_r]
