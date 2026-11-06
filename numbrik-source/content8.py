"""Florida Save Our Homes tax savings calculator (added November 6, 2026).
Caps and the indexed exemption come from the Florida Department of Revenue; Amendment 3 (approved Nov 3, 2026) is shown as a 2027 preview."""
from content import tool, T, BYID
import soh

def tbl(head, rows):
    return ('<div class="tbl"><table><thead><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")

r = soh.run(2015, 250000, 450000)
_, J, A, S = r[-1]
cum = sum(x[3] for x in r)
tw, two = soh.taxes(A, 2026, 6, 11.5), soh.taxes(J, 2026, 6, 11.5)
a3 = max(0, A - 150000) * 11.5 / 1000 + max(0, A - 25000) * 6 / 1000

tool(id="soh", slug="save-our-homes-calculator", cat="Money", name="Save Our Homes Calculator",
 short="Save Our Homes (Florida)", desc="Florida homestead assessment cap and tax savings.",
 title="Save Our Homes Calculator – Florida Tax Savings | Numbrik",
 meta="Estimate your Florida Save Our Homes savings: capped assessed value, tax saved this year and since you bought, portability, and a 2027 Amendment 3 preview.",
 lede="Florida's Save Our Homes cap limits how much the assessed value of a homestead can rise each year, to 3% or the inflation rate, whichever is lower. Enter the year you got your homestead exemption, its value then and its market value now to see your capped assessed value, how much tax the cap saves you, and how much benefit you could carry to a new home.",
 steps=["Enter the year your homestead exemption started and the home's market (just) value that year. The purchase price is a good estimate.",
        "Enter today's market value from your property appraiser or TRIM notice.",
        "Enter your school and non-school millage rates from your TRIM notice, or keep the Florida-average defaults.",
        "Read your 2026 assessed value, this year's tax savings, the total since you bought, and your portable benefit."],
 how=f"""<p>When you first qualify for a homestead exemption, your assessed value equals the market value. From the next January 1, the assessed value can rise by no more than 3% or the change in the Consumer Price Index, whichever is lower, and never above market value. The calculator applies the actual cap for every year since 1995 from the Florida Department of Revenue: 2.7% for 2026, 2.9% for 2025 and 3% for 2022–2024. Because it doesn't know your market value in each past year, it assumes the value grew evenly from your start year to today. Florida values jumped in some years, such as 2004–2006 and 2021–2023, so for an exact answer enter the assessed value from your TRIM notice.</p>
<p>Taxes are worked out on both values. The first $25,000 of assessed value is exempt from all property taxes. A second exemption, indexed to inflation since 2025 ($26,411 for 2026), applies to assessed value above $50,000 for non-school taxes only. Your savings is the tax on the uncapped market value minus the tax on your capped assessed value. Non-ad valorem charges such as trash and stormwater fees aren't affected by Save Our Homes and aren't included.</p>""",
 formula="Assessed(year) = min(market value, assessed(last year) × (1 + cap))\ncap = lower of 3% or CPI change (2.7% for 2026)\nSave Our Homes benefit = market value − assessed value\nTax = (assessed − exemptions) × millage ÷ 1,000",
 example=f"<p>A home that got its homestead exemption in 2015 at a value of $250,000 and is worth $450,000 in 2026 has a capped assessed value of about <strong>${A:,.0f}</strong>, so ${J-A:,.0f} of value isn't taxed. At 6 school mills and 11.5 other mills, the 2026 tax is about ${tw:,.0f} instead of ${two:,.0f}: a saving of <strong>${S:,.0f} this year</strong> and about <strong>${cum:,.0f}</strong> since 2015.</p>",
 extra="<h3>Save Our Homes cap by year</h3>" + tbl(["Year", "Cap", "Year", "Cap"], [(y, f"{soh.CAPS[y]}%", y - 16, f"{soh.CAPS[y-16]}%") for y in range(2026, 2010, -1)]) +
 "<p>Source: Florida Department of Revenue, Save Our Homes assessment limitation. The cap for each year is the lower of 3% or the change in CPI for the prior year.</p>"
 "<h3>Portability</h3><p>If you sell and buy another Florida homestead within three years, you can transfer your Save Our Homes benefit (the difference between market and assessed value) up to $500,000. Moving to a home of equal or higher value transfers the full benefit; moving to a cheaper home transfers a proportional share. You must apply for the new homestead exemption and portability with your county property appraiser.</p>"
 f"<h3>What Amendment 3 changes from 2027</h3><p>Florida voters approved Amendment 3 on November 3, 2026, with about 62% of the vote. From January 1, 2027, most homesteads won't pay non-school property taxes on the first $150,000 of assessed value, rising to $250,000 in 2028, with inflation adjustments later. The first $25,000 stays exempt from school taxes too, and the Save Our Homes cap and portability stay the same. Your November 2026 tax bill isn't affected. In the example above, the same assessed value would face roughly ${a3:,.0f} in taxes under the 2027 rules. The calculator shows this preview for your home; final figures depend on how your county applies the new law.</p>",
 faqs=[("What is the Save Our Homes cap for 2026?", "2.7%. The cap is the lower of 3% or the change in the Consumer Price Index; the CPI change used for 2026 assessments was 2.7%. It was 2.9% for 2025 and 3% for 2022 to 2024."),
       ("Does Save Our Homes lower my taxes or just my assessed value?", "It limits your assessed value. Your tax bill can still rise if millage rates go up or the assessed value catches up with market value, but it's usually much lower than it would be without the cap."),
       ("What happens to Save Our Homes when I sell?", "The cap resets for the buyer, whose assessed value starts at market value. You can carry up to $500,000 of your benefit to a new Florida homestead through portability if you buy within three years."),
       ("Does Save Our Homes apply to rental or second homes?", "No. It only applies to a homestead, your permanent Florida residence. Non-homestead property has a separate 10% cap on non-school taxes, which Amendment 3 lowers to 5% from 2027."),
       ("Did Amendment 3 change Save Our Homes?", "No. The cap and portability stay the same. Amendment 3 raises the homestead exemption for non-school taxes to $150,000 in 2027 and $250,000 in 2028.")],
 related=["loan", "compound", "percent", "salestax"])

BYID.update({t["id"]: t for t in T})
