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

# ---------------- Advanced SEO pass (Nov 13, 2026) ----------------
# Deeper topical coverage (cost basis, forms, 1099-DA, UK matching rules, India TDS and the Income-tax Act 2025),
# jump links, cited primary sources (WebPage.citation), about entities, contextual internal links and more FAQs.
# Sources checked: IRS broker-reporting guidance (1099-DA: gross proceeds from Jan 1 2025, basis from Jan 1 2026; Rev. Proc. 2024-28
# per-wallet basis from Jan 1 2025); GOV.UK CGT rates; India VDA rules (30% + cess, 1% TDS, ₹50,000/₹10,000; Income-tax Act 2025 from Apr 1 2026).
c = BYID["cryptotax"]
c["h1"] = "Crypto Tax Calculator 2026"
BR = {"Single": [12400, 50400, 105700, 201775, 256225, 640600], "Married filing jointly": [24800, 100800, 211400, 403550, 512450, 768700], "Head of household": [17700, 67450, 105700, 201750, 256200, 640600]}
def _rng(lo, hi): return f"${lo + 1:,} – ${hi:,}" if lo else f"Up to ${hi:,}"
c["extra"] = c["extra"].replace("<h3>2026 US long-term capital gains rates</h3>", '<h3 id="us-rates">2026 US long-term capital gains rates</h3>') \
                       .replace("<h3>What counts as a taxable crypto event?</h3>", '<h3 id="taxable">What counts as a taxable crypto event?</h3>')
c["extra"] = ('<h3 id="steps">How to calculate crypto taxes, step by step</h3><ol>'
  "<li><strong>List every disposal.</strong> Each sale, swap, purchase made with crypto and conversion to a stablecoin counts. Transfers between your own wallets don't.</li>"
  "<li><strong>Find the cost basis of what you sold.</strong> That's what you paid plus fees. Which coins you sold depends on the matching method (see below).</li>"
  "<li><strong>Work out the gain or loss.</strong> Sale value after fees minus cost basis. Check how long you held each lot: in the US, over one year is long-term.</li>"
  "<li><strong>Net your gains and losses</strong> for the year, short-term and long-term separately in the US.</li>"
  "<li><strong>Apply your country's rates</strong>, the step this calculator does for you, and add any staking, mining or airdrop income at your normal income tax rate.</li></ol>"
  + c["extra"] +
  '<h3 id="short-term">2026 US income tax brackets (for short-term gains)</h3><p>Crypto held one year or less is taxed at these ordinary rates, on taxable income after the standard deduction ($16,100 single, $32,200 married filing jointly, $24,150 head of household).</p>' +
  tbl(["Rate", "Single", "Married filing jointly", "Head of household"],
      [(f"{r}%", *[_rng(([0] + BR[k])[i], BR[k][i]) if i < 6 else f"Over ${BR[k][5]:,}" for k in BR]) for i, r in enumerate((10, 12, 22, 24, 32, 35, 37))]) +
  '<h3 id="cost-basis">Cost basis: which coins did you sell?</h3>'
  "<p>If you bought the same coin at different prices, the method you use to match sales to purchases changes your gain. In the US you can use <strong>FIFO</strong> (first in, first out, the default) or <strong>specific identification</strong>, choosing exact lots such as the most expensive first (HIFO), if you keep records that identify them. Since January 1, 2025, the IRS requires basis to be tracked <strong>wallet by wallet</strong> (or account by account) rather than across all your holdings, under the final broker regulations and Rev. Proc. 2024-28.</p>"
  "<p>The UK uses fixed matching rules instead: coins bought the <strong>same day</strong> are matched first, then coins bought in the <strong>next 30 days</strong> (the bed-and-breakfasting rule), and everything else comes from a <strong>Section 104 pool</strong> at its average cost. India allows only the cost of acquisition as a deduction.</p>" +
  '<h3 id="forms">Which tax forms do you need?</h3>' +
  tbl(["Country", "What to file"], [
    ("United States", "Form 8949 and Schedule D for sales and swaps; Schedule 1 for staking, mining and airdrop income; and answer the digital assets question on Form 1040."),
    ("US broker forms", "Form 1099-DA: exchanges report gross proceeds for sales from January 1, 2025, and cost basis for many sales from January 1, 2026. Check it against your own records."),
    ("United Kingdom", "Self Assessment capital gains pages (SA108). You must report if your total disposal proceeds exceed £50,000 in a tax year, even when gains are under the £3,000 allowance."),
    ("India", "Schedule VDA in ITR-2 (or ITR-3 with business income). TDS deducted under the 1% rule appears in Form 26AS and counts as tax paid.")]) +
  '<h3 id="uk">UK crypto tax at a glance</h3><ul>'
  "<li>Capital Gains Tax at <strong>18%</strong> within your remaining basic-rate band and <strong>24%</strong> above it, on gains over the £3,000 annual exempt amount.</li>"
  "<li>Staking, mining and crypto received as pay are generally taxed as income when received.</li>"
  "<li>Losses must be reported to HMRC (within four years) to be used against future gains.</li>"
  "<li>From 2026, UK exchanges collect user data under the international Cryptoasset Reporting Framework (CARF), so HMRC will increasingly see disposals.</li></ul>" +
  '<h3 id="india">India crypto tax at a glance</h3><ul>'
  "<li>Flat <strong>30%</strong> tax plus 4% cess (31.2%) on gains from virtual digital assets, whatever your income or holding period. Surcharge may apply on high incomes.</li>"
  "<li><strong>1% TDS</strong> on transfers above ₹50,000 a year (₹10,000 for most other payers), credited against your final tax.</li>"
  "<li>No deduction except the cost of acquisition, and losses can't be set off or carried forward.</li>"
  "<li>Crypto gifts from non-relatives above ₹50,000 a year are taxed as income for the receiver.</li>"
  "<li>The rules moved into the new Income-tax Act, 2025 from April 1, 2026 with the same 30% rate and 1% TDS, which Budget 2026 left unchanged.</li></ul>" +
  '<h3 id="lower">Legal ways to lower your crypto tax</h3><ul>'
  "<li><strong>Hold for more than a year</strong> (US): the long-term rate is often 15% instead of 22–24%. The table above shows how much that saves.</li>"
  "<li><strong>Harvest losses</strong>: selling coins at a loss offsets gains, and in the US up to $3,000 of other income a year. Use the <a href=\"/percent-change-calculator/\">percent change calculator</a> to see which holdings are down.</li>"
  "<li><strong>Use your UK allowance</strong>: spreading sales across tax years uses the £3,000 exemption more than once.</li>"
  "<li><strong>Keep records of every fee</strong>: fees add to your cost basis and cut the gain.</li>"
  "<li><strong>Plan for the bill</strong>: set aside tax from each profitable sale, and check how it affects your <a href=\"/take-home-pay-calculator/\">take-home pay</a> and <a href=\"/retirement-calculator/\">retirement savings</a>.</li></ul>"
  '<h3 id="sources">Sources</h3><ul class="sources">'
  '<li><a href="https://www.irs.gov/filing/digital-assets" rel="nofollow noopener" target="_blank">IRS: Digital assets</a></li>'
  '<li><a href="https://www.irs.gov/instructions/i1099da" rel="nofollow noopener" target="_blank">IRS: Instructions for Form 1099-DA</a></li>'
  '<li><a href="https://taxfoundation.org/data/all/federal/2026-tax-brackets/" rel="nofollow noopener" target="_blank">Tax Foundation: 2026 tax brackets (IRS Rev. Proc. 2025-32)</a></li>'
  '<li><a href="https://www.gov.uk/capital-gains-tax/rates" rel="nofollow noopener" target="_blank">GOV.UK: Capital Gains Tax rates and allowances</a></li>'
  '<li><a href="https://www.gov.uk/hmrc-internal-manuals/cryptoassets-manual" rel="nofollow noopener" target="_blank">HMRC: Cryptoassets Manual</a></li>'
  '<li><a href="https://www.incometax.gov.in/" rel="nofollow noopener" target="_blank">Income Tax Department, India</a></li></ul>'
  '<p>Last checked November 2026. This calculator gives estimates for general information, not tax advice; for complex situations talk to a tax professional.</p>')
c["toc"] = [("steps", "Step by step"), ("us-rates", "US long-term rates"), ("short-term", "US short-term brackets"), ("taxable", "Taxable events"),
            ("cost-basis", "Cost basis methods"), ("forms", "Tax forms and 1099-DA"), ("uk", "UK rules"), ("india", "India rules"), ("lower", "Lower your crypto tax"), ("sources", "Sources")]
c["cite"] = [("IRS: Digital assets", "https://www.irs.gov/filing/digital-assets"), ("IRS: Instructions for Form 1099-DA", "https://www.irs.gov/instructions/i1099da"),
             ("GOV.UK: Capital Gains Tax rates", "https://www.gov.uk/capital-gains-tax/rates"), ("HMRC Cryptoassets Manual", "https://www.gov.uk/hmrc-internal-manuals/cryptoassets-manual"),
             ("Income Tax Department, India", "https://www.incometax.gov.in/")]
c["about"] = [("Cryptocurrency", "https://en.wikipedia.org/wiki/Cryptocurrency"), ("Capital gains tax", "https://en.wikipedia.org/wiki/Capital_gains_tax"), ("Bitcoin", "https://en.wikipedia.org/wiki/Bitcoin")]
c["faqs"] = c["faqs"] + [
  ("Is trading one crypto for another taxable?", "Yes, in the US, UK and India. Swapping Bitcoin for Ethereum counts as selling the Bitcoin at its market value, so any gain since you bought it is taxable, even though no cash changed hands."),
  ("Do I have to report crypto if I lost money?", "In the US you report all disposals on Form 8949, and reporting losses is how you use them to cut your tax. In the UK, losses must be reported to HMRC within four years to be carried forward."),
  ("What is Form 1099-DA?", "A new IRS form crypto brokers send to you and the IRS. It reports gross proceeds for sales from January 1, 2025 and, for many sales from January 1, 2026, your cost basis. Compare it with your own records before filing."),
  ("How is crypto staking taxed?", "In the US and UK, staking rewards are generally taxed as income at their market value when you receive them. That value becomes your cost basis, so you may owe capital gains tax again when you later sell."),
  ("Do I pay state tax on crypto gains?", "In most US states, yes: states with an income tax generally tax capital gains as ordinary income. States with no income tax on wages, such as Florida and Texas, don't tax them. This calculator shows federal tax only."),
  ("Does the wash-sale rule apply to crypto?", "For US federal tax, the wash-sale rule has applied to stocks and securities, not to crypto, so selling at a loss and buying back soon after has generally been allowed. Congress has proposed changing this, so check the rules for the year you sell.")]
for _k in ("compound", "pctchange", "retire", "savings"):
    if "cryptotax" not in BYID[_k]["related"]: BYID[_k]["related"] = ["cryptotax"] + BYID[_k]["related"][:3]
