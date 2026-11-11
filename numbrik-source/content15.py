"""Calculator.com sitemap gap (Nov 11, 2026): high-value personal-finance calculators Numbrik lacked — car lease, retirement,
savings, student loan and rent vs buy. Example figures are computed with the same formulas as the JavaScript tools."""
from content import tool, T, BYID

def tbl(head, rows):
    return ('<div class="tbl"><table><thead><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")
usd = lambda x, d=0: f"${x:,.{d}f}"
def pm(P, r, n): return P * r / (1 - (1 + r) ** -n) if r else P / n

# ---------- Car lease ----------
def lease(msrp, price, down, n, rp, apr, fees=995, tx=.07):
    cap = price + fees - down; res = msrp * rp / 100; mf = apr / 2400; base = (cap - res) / n + (cap + res) * mf; return base * (1 + tx)
tool(id="lease", slug="car-lease-calculator", cat="Money", name="Car Lease Calculator",
 short="Car lease calculator", desc="Monthly car lease payment from price, residual and money factor.",
 title="Car Lease Calculator – Monthly Lease Payment | Numbrik",
 meta="Calculate a car lease payment from the negotiated price, residual value, money factor or APR, down payment, fees and sales tax. See the full cost of the lease.",
 lede="Work out a monthly car lease payment the way dealers do: from the negotiated price, residual value, money factor, down payment, fees and sales tax. It shows each part of the payment so you can check a dealer's quote.",
 steps=["Enter the MSRP and the price you negotiated.", "Add your down payment and trade-in, and any fees rolled into the lease.", "Enter the term, the residual percentage and the APR (or money factor × 2,400).", "Read the monthly payment and the total cost of the lease."],
 how="""<p>A lease payment has two parts. The <strong>depreciation fee</strong> pays for the value the car loses while you drive it: the net capitalized cost (price plus fees, minus down payment and trade-in) minus the residual value, divided by the number of months. The <strong>finance or rent charge</strong> is (capitalized cost + residual) × money factor. Sales tax is then added to the payment in most US states.</p>
<p>The money factor is just an interest rate in disguise: multiply it by 2,400 to get the APR. Residual values for 36-month leases are often 50–60% of MSRP. Negotiating the price down lowers the payment just like it does when buying, and a large down payment is risky on a lease, because it's usually lost if the car is stolen or written off.</p>""",
 formula="Net cap cost = price + fees − down payment − trade-in\nResidual = MSRP × residual %\nDepreciation = (net cap cost − residual) ÷ months\nRent charge = (net cap cost + residual) × money factor\nMoney factor = APR ÷ 2,400",
 example=f"<p>A car with a <strong>$40,000 MSRP</strong> negotiated to <strong>$37,500</strong>, $995 in fees and $3,000 down, on a <strong>36-month</strong> lease with a 58% residual and 6% APR (money factor 0.0025): depreciation is $341.53 and the rent charge $146.74, so the payment is $488.27, or <strong>{usd(lease(40000, 37500, 3000, 36, 58, 6), 2)}</strong> with 7% sales tax.</p>",
 extra="<h3>Lease payment by price and residual (36 months, 6% APR, $3,000 down, 7% tax)</h3>" + tbl(["Car price (MSRP)", "50% residual", "55% residual", "60% residual"],
   [(usd(p), usd(lease(p, p * .95, 3000, 36, 50, 6)), usd(lease(p, p * .95, 3000, 36, 55, 6)), usd(lease(p, p * .95, 3000, 36, 60, 6))) for p in (25000, 30000, 35000, 40000, 50000, 60000)]) +
 "<p>Assumes the price is negotiated 5% below MSRP and $995 in fees.</p>" +
 "<h3>Money factor to APR</h3>" + tbl(["Money factor", "APR"], [(f"{m:.5f}", f"{m * 2400:.1f}%") for m in (0.0010, 0.0015, 0.0020, 0.0025, 0.0030, 0.0035, 0.0040)]),
 faqs=[("What is a good money factor?", "Multiply it by 2,400 to compare it with loan rates. 0.0025 is 6% APR. Anything close to the rate you'd get on a new-car loan is reasonable; ask the dealer for the buy rate, the lowest the lender allows."),
       ("Is it better to put money down on a lease?", "Usually as little as possible. A down payment just prepays the lease, and if the car is stolen or totaled early, gap coverage pays the lender but you typically don't get the down payment back."),
       ("What is the residual value?", "The car's predicted value at the end of the lease, set by the leasing company as a percentage of MSRP. A higher residual means a lower payment. It's also your buyout price."),
       ("Can I negotiate a lease?", "Yes. The price (capitalized cost) and often the money factor and fees can be negotiated, just as when buying. The residual is set by the lender.")],
 related=["autoloan", "gloan", "fuel", "salestax"])

# ---------- Retirement ----------
def retire(a, r, s, m, ret=.06, inc=.02):
    mr = (1 + ret) ** (1 / 12) - 1; b = s; c = m
    for y in range(r - a):
        for k in range(12): b = b * (1 + mr) + c
        c *= 1 + inc
    return b
tool(id="retire", slug="retirement-calculator", cat="Money", name="Retirement Calculator",
 short="Retirement calculator", desc="Projected retirement savings and income.",
 title="Retirement Calculator – How Much Will I Have? | Numbrik",
 meta="Project your retirement savings from your age, current balance, monthly contributions and expected return, in future and today's dollars, and the income it could pay.",
 lede="See how much you could have when you retire, from what you've saved so far, what you add each month and your expected return. The calculator shows the balance in future dollars and in today's money, plus the yearly income it could support.",
 steps=["Enter your age, the age you plan to retire and what you've saved.", "Enter your monthly contribution, including any employer match.", "Set an expected return and inflation; raise contributions each year if your pay rises.", "Read your projected balance and the income it could give you."],
 how="""<p>The calculator grows your savings month by month at the expected return, adds your contribution each month, and raises the contribution by the percentage you choose each year. It then divides by inflation to show the balance in today's money, which is what really matters for your lifestyle.</p>
<p>The income figure uses a withdrawal rate. The well-known 4% rule comes from research in the 1990s showing that withdrawing 4% of a balanced portfolio in the first year, then adjusting for inflation, lasted at least 30 years in most historical periods. Retiring early or wanting more certainty suggests a lower rate, around 3–3.5%.</p>""",
 formula="Each month: balance = balance × (1 + monthly return) + contribution\nMonthly return = (1 + annual return)^(1/12) − 1\nToday's money = future balance ÷ (1 + inflation)^years\nIncome = balance × withdrawal rate",
 example=f"<p>A 35-year-old with <strong>$50,000</strong> saved who invests <strong>$800 a month</strong> (raised 2% a year) at a 6% return could have about <strong>{usd(round(retire(35, 67, 50000, 800), -3))}</strong> at 67. With 2.5% inflation that's about {usd(round(retire(35, 67, 50000, 800) / 1.025 ** 32, -3))} in today's money, supporting roughly {usd(round(retire(35, 67, 50000, 800) * .04 / 1.025 ** 32, -2))} a year at 4%.</p>",
 extra="<h3>Balance at 67 by monthly saving (starting from $0, 6% return, no raises)</h3>" + tbl(["Monthly saving", "Start at 25", "Start at 35", "Start at 45", "Start at 55"],
   [(usd(m), *[usd(round(retire(a, 67, 0, m, inc=0), -3)) for a in (25, 35, 45, 55)]) for m in (200, 500, 800, 1000, 1500, 2000)]) +
 "<h3>How much savings for a given income (4% rule)</h3>" + tbl(["Yearly income from savings", "Savings needed"], [(usd(i), usd(i * 25)) for i in (20000, 30000, 40000, 50000, 60000, 80000, 100000)]),
 faqs=[("How much do I need to retire?", "A common rule of thumb is 25 times the yearly income you want from savings (the 4% rule), on top of Social Security or a pension. To draw $40,000 a year, aim for about $1,000,000."),
       ("What return should I assume?", "Many planners use 5–7% a year before inflation for a diversified portfolio of stocks and bonds. Use a lower figure if you hold mostly bonds or cash, or to be cautious."),
       ("Does this include Social Security?", "No. It only projects your own savings. Add your estimated Social Security benefit, which you can see in your my Social Security account at ssa.gov, to the income shown."),
       ("Should I count my employer's 401(k) match?", "Yes. Add the match to your monthly contribution; it's part of what goes into the account each month.")],
 related=["compound", "savings", "rmd", "salary"])

# ---------- Savings ----------
def sav(P, d, apy, y):
    r = (1 + apy) ** (1 / 12) - 1; b = P
    for k in range(y * 12): b = b * (1 + r) + d
    return b
tool(id="savings", slug="savings-calculator", cat="Money", name="Savings Calculator",
 short="Savings calculator", desc="How savings grow with deposits and interest, or what to save for a goal.",
 title="Savings Calculator – Growth & Savings Goal | Numbrik",
 meta="See how your savings grow with monthly deposits and interest, or find how much to save each month to reach a goal. Works with high-yield savings APYs.",
 lede="Find out how much your savings will grow with regular deposits and interest, or flip it around and see how much you need to save each month to reach a goal, such as an emergency fund, a down payment or a car.",
 steps=["Choose growth or goal.", "Enter your starting balance and either your monthly deposit or your goal.", "Enter the APY and how many years.", "Read the final balance and how much of it is interest, with a year-by-year table."],
 how="""<p>Savings accounts quote an annual percentage yield (APY), which already includes compounding. The calculator converts it to a monthly rate, (1 + APY)^(1/12) − 1, grows the balance each month and adds your deposit. In goal mode it solves the same formula backwards for the monthly deposit.</p>
<p>High-yield savings accounts and money market accounts change their rates with the market, so treat the APY as an estimate over long periods. Interest on savings is taxable as ordinary income in the US.</p>""",
 formula="Monthly rate r = (1 + APY)^(1/12) − 1\nFuture value = P(1 + r)^n + d × ((1 + r)^n − 1) ÷ r\nDeposit for a goal d = (goal − P(1 + r)^n) × r ÷ ((1 + r)^n − 1)",
 example=f"<p>Starting with <strong>$5,000</strong> and adding <strong>$300 a month</strong> at <strong>4.25% APY</strong> for 5 years gives about <strong>{usd(sav(5000, 300, .0425, 5))}</strong>. You deposit $23,000, so about {usd(sav(5000, 300, .0425, 5) - 23000)} is interest.</p>",
 extra="<h3>Monthly saving needed for a goal (starting from $0, 4% APY)</h3>" + tbl(["Goal", "1 year", "2 years", "3 years", "5 years"],
   [(usd(g), *[usd(g * ((1.04) ** (1 / 12) - 1) / ((1.04) ** (y) - 1)) for y in (1, 2, 3, 5)]) for g in (1000, 5000, 10000, 20000, 50000, 100000)]) +
 "<h3>Growth of $10,000 with no deposits</h3>" + tbl(["APY", "1 year", "5 years", "10 years"], [(f"{a}%", *[usd(10000 * (1 + a / 100) ** y) for y in (1, 5, 10)]) for a in (0.5, 2, 3, 4, 4.5, 5)]),
 faqs=[("How much should I keep in an emergency fund?", "A common guideline is three to six months of essential expenses, kept somewhere safe and easy to reach, like a high-yield savings account."),
       ("What's the difference between APR and APY?", "APY includes the effect of compounding and APR doesn't. Savings accounts quote APY, so you can compare them directly."),
       ("How often is savings interest compounded?", "Most US savings accounts compound daily and pay monthly. Because the APY already includes compounding, the calculator gives the same result either way."),
       ("Is interest on savings taxed?", "Yes, in the US it's taxed as ordinary income in the year it's paid. Your bank sends Form 1099-INT if you earn $10 or more.")],
 related=["compound", "cd", "simpleint", "retire"])

# ---------- Student loan ----------
tool(id="studentloan", slug="student-loan-calculator", cat="Money", name="Student Loan Calculator",
 short="Student loan calculator", desc="Student loan payment, total interest and payoff with extra payments.",
 title="Student Loan Calculator – Payment & Payoff | Numbrik",
 meta="Calculate your student loan payment and total interest, compare the 10-year standard plan with longer terms, and see how extra payments shorten your payoff.",
 lede="Work out your monthly student loan payment and the total interest you'll pay, compare the 10-year standard plan with 20- and 25-year terms, and see how much an extra payment each month saves.",
 steps=["Enter your loan balance and interest rate. For several loans, use the total and a weighted average rate.", "Enter the repayment term: 10 years is the federal standard plan.", "Optional: add an extra monthly payment.", "Read the payment, the total interest and how much sooner you'd be debt-free."],
 how="""<p>Fixed-rate student loans are repaid like other installment loans: equal monthly payments over the term, mostly interest at first and mostly principal later. The calculator uses the standard amortization formula and shows how the payment and total interest change with longer terms.</p>
<p>Longer terms lower the payment but can nearly triple the interest. Extra payments go straight to principal and cut the interest charged every month after. With federal loans, ask your servicer to apply extra payments to principal rather than to future payments. Income-driven repayment plans set the payment as a share of income instead, so use the official Loan Simulator at studentaid.gov for those.</p>""",
 formula="Payment = P × r ÷ (1 − (1 + r)^−n)\nr = annual rate ÷ 12,  n = months\nTotal interest = payment × n − P",
 example=f"<p>A <strong>$30,000</strong> balance at <strong>6.5%</strong> on the 10-year standard plan costs <strong>{usd(pm(30000, 6.5 / 1200, 120), 2)} a month</strong> and {usd(pm(30000, 6.5 / 1200, 120) * 120 - 30000)} in interest. Stretching it to 25 years drops the payment to {usd(pm(30000, 6.5 / 1200, 300), 2)} but the interest rises to {usd(pm(30000, 6.5 / 1200, 300) * 300 - 30000)}.</p>",
 extra="<h3>Monthly payment by balance (10-year term)</h3>" + tbl(["Balance", "4%", "5.5%", "6.5%", "8%"],
   [(usd(b), *[usd(pm(b, r / 1200, 120)) for r in (4, 5.5, 6.5, 8)]) for b in (10000, 20000, 30000, 40000, 60000, 80000, 100000)]),
 faqs=[("How long does it take to pay off student loans?", "The federal standard plan is 10 years. Extended plans run up to 25 years, and income-driven plans can last 20 to 25 years before any remaining balance is forgiven."),
       ("Should I pay off student loans early?", "If your rate is higher than what you'd reasonably earn investing, extra payments are a guaranteed return. Build an emergency fund and get any employer retirement match first."),
       ("How is student loan interest calculated?", "Most federal loans charge simple daily interest: balance × annual rate ÷ 365 each day. That works out to about balance × rate ÷ 12 a month, which is how this calculator models it."),
       ("Is student loan interest tax-deductible?", "In the US you may deduct up to $2,500 a year of student loan interest, subject to income limits. Check the current IRS rules for your filing status.")],
 related=["gloan", "loan", "gpa", "salary"])

# ---------- Rent vs buy ----------
def rb(H, rent, Y=7, dp=.2, rate=6.5, tx=.011, ins=2400, mt=.01, ap=.03, rg=.03, inv=.05):
    r = rate / 1200; down = H * dp; L = H - down; p = pm(L, r, 360); close = H * .03; bal = L; own = down + close; val = H; rt = 0; rr = rent
    for y in range(Y):
        for k in range(12): i = bal * r; bal -= p - i; own += p
        own += val * tx + ins + val * mt; val *= 1 + ap; rt += rr * 12; rr *= 1 + rg
    return own - (val * .94 - bal) + (down + close) * ((1 + inv) ** Y - 1), rt
_b, _r = rb(400000, 2200)
tool(id="rentbuy", slug="rent-vs-buy-calculator", cat="Money", name="Rent vs Buy Calculator",
 short="Rent vs buy", desc="Compare the true cost of renting and buying over time.",
 title="Rent vs Buy Calculator – Should I Rent or Buy? | Numbrik",
 meta="Should you rent or buy a home? Compare the full cost of each over the years you'll stay, including mortgage, taxes, upkeep, home value growth, rent increases and lost investment returns.",
 lede="Compare the true cost of buying a home with renting over the years you expect to stay. The calculator counts the mortgage, property tax, insurance, upkeep, closing and selling costs, home value growth, rent increases and the return your down payment could have earned.",
 steps=["Enter the home price, down payment, mortgage rate and how long you'll stay.", "Adjust property tax, insurance and HOA, maintenance and expected price growth.", "Enter the rent for a similar home and how fast rents rise.", "Read which option comes out ahead, and by how much."],
 how="""<p>Buying looks cheaper when you only compare the mortgage payment with rent, but owning has other costs: property tax, insurance, maintenance (often about 1% of the home's value a year), closing costs to buy (around 3%) and to sell (around 6%). Against that, you build equity and the home may rise in value. The calculator adds up everything you'd spend owning, subtracts what you'd walk away with after selling, and adds the investment return your down payment and closing costs would have earned if you'd rented instead.</p>
<p>The biggest factor is time. Buying and selling costs are large, so buying usually needs several years to beat renting. Higher rents, faster home price growth and lower mortgage rates all tip the balance toward buying.</p>""",
 formula="Net cost of buying = down payment + closing costs + mortgage payments + tax, insurance and upkeep\n  − (sale price − 6% selling costs − remaining loan)\n  + investment return lost on the down payment and closing costs\nCost of renting = total rent paid",
 example=f"<p>A <strong>$400,000</strong> home with 20% down at 6.5%, versus renting a similar home for <strong>$2,200 a month</strong>, over <strong>7 years</strong> with 3% yearly growth in prices and rents: buying costs about {usd(round(_b, -3))} net and renting about {usd(round(_r, -3))}, so renting comes out roughly {usd(round(abs(_b - _r), -3))} ahead. Stay longer, or find a higher rent, and buying wins.</p>",
 extra="<h3>Break-even: net cost of buying vs renting ($400,000 home, $2,200 rent)</h3>" + tbl(["Years you stay", "Net cost of buying", "Total rent", "Cheaper option"],
   [(y, usd(round(rb(400000, 2200, y)[0], -3)), usd(round(rb(400000, 2200, y)[1], -3)), "Buying" if rb(400000, 2200, y)[0] < rb(400000, 2200, y)[1] else "Renting") for y in (3, 5, 7, 10, 15, 20)]) +
 "<p>Assumes 20% down, a 6.5% 30-year mortgage, 1.1% property tax, $2,400 a year insurance and HOA, 1% maintenance, 3% yearly growth in prices and rents, and a 5% return on money not used for the down payment.</p>",
 faqs=[("Is it better to rent or buy a house?", "It depends mostly on how long you'll stay and how rents compare with prices where you live. Buying usually needs five years or more to beat renting, because of closing and selling costs."),
       ("What is the price-to-rent ratio?", "Home price divided by a year's rent. Below about 15 tends to favour buying; above about 20 tends to favour renting. A $400,000 home renting for $2,200 a month has a ratio of about 15."),
       ("Does the calculator include tax deductions?", "No. Since 2018 the higher standard deduction means most US homeowners don't itemize, so mortgage interest and property tax deductions often don't change the result."),
       ("Why does it count lost investment returns?", "Money put into a down payment can't be invested elsewhere. Counting what it might have earned makes the comparison with renting fair.")],
 related=["afford", "loan", "gloan", "compound"])

BYID.update({t["id"]: t for t in T})
