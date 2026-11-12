"""Crypto tax calculator (Nov 13, 2026). US: tax year 2026 brackets, standard deduction and LTCG thresholds from IRS Rev. Proc.
2025-32 (via Tax Foundation); NIIT 3.8% above $200k/$250k MAGI. UK: 18%/24% CGT, £3,000 annual exempt amount (2025/26 and
2026/27), basic-rate band to £50,270. India: 30% + 4% cess under s.115BBH, 1% TDS under s.194S, unchanged in Budget 2026."""
from content import tool, T, BYID

def tbl(head, rows):
    return ('<div class="tbl"><table><thead><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")
usd = lambda x: f"${x:,.0f}"
US = {"s": dict(sd=16100, b=[(12400, .10), (50400, .12), (105700, .22), (201775, .24), (256225, .32), (640600, .35), (float("inf"), .37)], lt=(49450, 545500), niit=200000),
      "m": dict(sd=32200, b=[(24800, .10), (100800, .12), (211400, .22), (403550, .24), (512450, .32), (768700, .35), (float("inf"), .37)], lt=(98900, 613700), niit=250000)}
def _tax(b, x):
    t = lo = 0
    for hi, r in b:
        if x > lo: t += (min(x, hi) - lo) * r
        lo = hi
    return t
def us_tax(gain, income, fs="s", long=True):
    T_ = US[fs]; ti = max(0, income - T_["sd"])
    if long:
        z, f = T_["lt"]; rem = gain; base = ti; t0 = max(0, min(rem, z - base)); rem -= t0; base += t0
        t15 = max(0, min(rem, f - max(base, z))); rem -= t15; tax = t15 * .15 + rem * .20
    else:
        tax = _tax(T_["b"], ti + gain) - _tax(T_["b"], ti)
    return tax + max(0, min(gain, income + gain - T_["niit"])) * .038

tool(id="cryptotax", slug="crypto-tax-calculator", cat="Money", name="Crypto Tax Calculator",
 short="Crypto tax calculator", desc="Tax on crypto gains for the US, UK and India.",
 title="Crypto Tax Calculator 2026 – US, UK & India | Numbrik",
 meta="Estimate tax on Bitcoin and other crypto gains: US short- and long-term capital gains for 2026, UK Capital Gains Tax and India's 30% VDA tax with 1% TDS.",
 lede="Estimate the tax on a crypto sale or trade. Pick your country, enter what you paid and what you sold for, and see the tax, the rate on your gain and what you keep. It covers US federal capital gains for 2026, UK Capital Gains Tax and India's 30% tax on virtual digital assets.",
 steps=["Choose the United States, United Kingdom or India.", "Enter your total cost (purchase price plus fees) and the sale value after fees.", "US: choose your filing status and whether you held the crypto more than a year, and enter your other income. UK: enter your income for the tax year.", "Read the estimated tax, the effective rate and what you keep."],
 how="""<p><strong>United States.</strong> The IRS treats crypto as property, so selling, swapping one coin for another or spending it is a taxable event. The gain is the sale value minus your cost basis. Coins held one year or less are taxed as ordinary income at your bracket (10% to 37%); held longer than a year, gains get the long-term rates of 0%, 15% or 20%, which depend on your total taxable income. Higher earners may also owe the 3.8% net investment income tax. The calculator stacks the gain on top of your other income after the standard deduction, the same way the tax return does. State income tax is not included.</p>
<p><strong>United Kingdom.</strong> HMRC treats crypto as an asset for Capital Gains Tax. The first £3,000 of gains each tax year is tax-free; above that, gains are taxed at 18% while they fit in your remaining basic-rate band and 24% beyond it. <strong>India.</strong> Gains on virtual digital assets are taxed at a flat 30% plus 4% cess (31.2%), with no deductions other than the cost of acquisition, and losses can't be set off or carried forward. A 1% TDS is deducted on sales above the threshold and counts towards the tax.</p>""",
 formula="Gain = sale value − cost (including fees)\nUS short-term: tax at your ordinary income brackets\nUS long-term: 0% / 15% / 20% by taxable income (+3.8% NIIT for high incomes)\nUK: (gain − £3,000) × 18% or 24%\nIndia: gain × 30% × 1.04 = 31.2%",
 example=f"<p>A single filer earning <strong>$75,000</strong> sells Bitcoin bought for $5,000 for <strong>$8,000</strong>, a $3,000 gain. Held over a year, the gain is taxed at 15%: about <strong>{usd(us_tax(3000, 75000))}</strong>. Sold within a year, it's taxed as ordinary income in the 22% bracket: about <strong>{usd(us_tax(3000, 75000, long=False))}</strong>. Holding for one more day past the one-year mark saves {usd(us_tax(3000, 75000, long=False) - us_tax(3000, 75000))}.</p>",
 extra="<h3>2026 US long-term capital gains rates</h3>" + tbl(["Rate", "Single (taxable income)", "Married filing jointly"],
   [("0%", "Up to $49,450", "Up to $98,900"), ("15%", "$49,451 – $545,500", "$98,901 – $613,700"), ("20%", "Over $545,500", "Over $613,700")]) +
 "<h3>US federal tax on a $10,000 crypto gain (single filer, 2026)</h3>" + tbl(["Other income", "Held ≤ 1 year", "Held > 1 year", "You save by holding"],
   [(usd(i), usd(us_tax(10000, i, long=False)), usd(us_tax(10000, i)), usd(us_tax(10000, i, long=False) - us_tax(10000, i))) for i in (30000, 50000, 75000, 100000, 150000, 250000)]) +
 "<h3>What counts as a taxable crypto event?</h3>" + tbl(["Action", "US", "UK", "India"],
   [("Selling crypto for cash", "Taxable", "Taxable", "Taxable"), ("Trading one coin for another", "Taxable", "Taxable", "Taxable"), ("Spending crypto on goods", "Taxable", "Taxable", "Taxable"),
    ("Buying and holding", "Not taxable", "Not taxable", "Not taxable"), ("Moving coins between your own wallets", "Not taxable", "Not taxable", "Not taxable"),
    ("Staking or mining rewards", "Income when received", "Income when received", "Generally income when received")]),
 faqs=[("How much tax do I pay on crypto in the US?", "It depends on how long you held it and your income. Gains on crypto held a year or less are taxed like wages, at 10% to 37%. Held longer, most people pay 15%, some pay 0%, and the highest earners pay 20%, plus 3.8% NIIT above $200,000 ($250,000 for couples)."),
       ("Do I pay tax on crypto if I don't sell?", "No. Simply buying and holding, or moving coins between your own wallets, isn't taxable. Tax is due when you sell, trade for another coin or spend it. Staking and mining rewards are taxed as income when you receive them."),
       ("Can crypto losses reduce my taxes?", "In the US, yes: losses offset gains, and up to $3,000 of net losses a year offset other income, with the rest carried forward. In the UK, reported losses offset gains. In India, crypto losses can't be set off against anything."),
       ("What is the crypto tax rate in India?", "A flat 30% plus 4% cess, 31.2% in total, on gains from virtual digital assets, regardless of how long you held them or your income. A 1% TDS is deducted on sales above the threshold and counts as tax already paid.")],
 related=["compound", "pctchange", "salary", "paycheck"])

BYID.update({t["id"]: t for t in T})
