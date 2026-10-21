"""Content for the five calculators added on October 21, 2026."""
import math
from content import tool, T, BYID, usd

# ---------- US take-home pay (2026) ----------
BR = {"single": [(12400, .10), (50400, .12), (105700, .22), (201775, .24), (256225, .32), (640600, .35), (math.inf, .37)],
      "mfj": [(24800, .10), (100800, .12), (211400, .22), (403550, .24), (512450, .32), (768700, .35), (math.inf, .37)]}
SD = {"single": 16100, "mfj": 32200}
def takehome(g, fs="single", pre=0, state=0):
    ti = max(0, g - pre - SD[fs]); fed = 0; lo = 0
    for hi, r in BR[fs]:
        if ti > lo: fed += (min(ti, hi) - lo) * r
        lo = hi
    ss = min(g, 184500) * .062; med = g * .0145 + max(0, g - (250000 if fs == "mfj" else 200000)) * .009
    st = (g - pre) * state / 100
    return dict(fed=fed, ss=ss, med=med, st=st, net=g - pre - fed - ss - med - st)
ex = takehome(65000); ex60 = takehome(60000); ex100 = takehome(100000, "mfj", 6000, 5)
th_rows = "".join(f"<tr><td>{usd(g,0)}</td><td>{usd(r['fed'],0)}</td><td>{usd(r['ss']+r['med'],0)}</td><td>{usd(r['net'],0)}</td><td>{usd(r['net']/26,0)}</td></tr>"
                  for g in [40000, 50000, 60000, 75000, 100000, 150000] for r in [takehome(g)])
br_rows = "".join(f"<tr><td>{int(r*100)}%</td><td>{s}</td><td>{m}</td></tr>" for r, s, m in [
    (.10, "$0 – $12,400", "$0 – $24,800"), (.12, "$12,401 – $50,400", "$24,801 – $100,800"), (.22, "$50,401 – $105,700", "$100,801 – $211,400"),
    (.24, "$105,701 – $201,775", "$211,401 – $403,550"), (.32, "$201,776 – $256,225", "$403,551 – $512,450"), (.35, "$256,226 – $640,600", "$512,451 – $768,700"), (.37, "Over $640,600", "Over $768,700")])
tool(id="paycheck", slug="take-home-pay-calculator", cat="Work & pay", name="Take-Home Pay Calculator",
 short="Take-home pay (US)", desc="2026 US paycheck after federal tax, FICA and state tax.",
 title="Take-Home Pay Calculator 2026 – US Paycheck | Numbrik",
 meta="Estimate your 2026 US take-home pay per paycheck after federal income tax, Social Security, Medicare, state tax and 401(k). Weekly, biweekly or monthly.",
 lede="Estimate your take-home pay per paycheck in the United States for 2026, after federal income tax, Social Security, Medicare, an estimated state tax and pre-tax deductions such as a 401(k).",
 steps=["Choose single or married filing jointly.","Enter your annual salary and how often you are paid.","Add pre-tax deductions per year, such as 401(k) contributions, and an estimated state income tax rate.","Read your take-home pay per paycheck and the breakdown of each tax."],
 how="""<p>Federal income tax is progressive: each slice of taxable income is taxed at its own rate. Taxable income is your salary minus pre-tax deductions and the 2026 standard deduction of $16,100 for single filers or $32,200 for married couples filing jointly.</p>
<p>Social Security tax is 6.2% of wages up to the 2026 wage base of $184,500. Medicare tax is 1.45% of all wages, plus an extra 0.9% on wages above $200,000 (single) or $250,000 (married filing jointly). Traditional 401(k) contributions lower your income tax but not Social Security or Medicare, and the calculator treats all pre-tax deductions that way.</p>
<p>State tax here is a simple flat estimate. Real state taxes use their own brackets and deductions, and some cities, such as New York City, add a local income tax. Tax credits, extra W-4 withholding and the new deductions for tips and overtime are not included, so your actual paycheck can differ.</p>""",
 formula="Taxable income = salary − pre-tax deductions − standard deduction\nFederal tax    = sum of each bracket slice × its rate\nSocial Security = 6.2% × min(salary, $184,500)\nMedicare       = 1.45% × salary (+0.9% above $200,000 single / $250,000 joint)\nTake-home      = salary − pre-tax − federal − Social Security − Medicare − state",
 example=f"""<p>A single filer earning {usd(65000,0)} with no pre-tax deductions in a state with no income tax pays about {usd(ex['fed'],0)} in federal income tax, {usd(ex['ss'],0)} in Social Security and {usd(ex['med'],0)} in Medicare. Take-home pay is about <strong>{usd(ex['net'],0)} a year</strong>, or <strong>{usd(ex['net']/26)}</strong> every two weeks.</p>
<p>A married couple earning {usd(100000,0)} together, putting {usd(6000,0)} into a 401(k) and paying an estimated 5% state tax, takes home about {usd(ex100['net'],0)} a year.</p>""",
 extra=f"""<h3>2026 federal tax brackets</h3><div class="tbl"><table><thead><tr><th>Rate</th><th>Single</th><th>Married filing jointly</th></tr></thead><tbody>{br_rows}</tbody></table></div>
<h3>Take-home pay by salary (single, no state tax, paid every 2 weeks)</h3><div class="tbl"><table><thead><tr><th>Salary</th><th>Federal tax</th><th>FICA</th><th>Take-home / yr</th><th>Per paycheck</th></tr></thead><tbody>{th_rows}</tbody></table></div>""",
 faqs=[("How much is $60,000 a year after taxes?", f"For a single filer in a state with no income tax, about {usd(ex60['net'],0)} a year, or {usd(ex60['net']/12,0)} a month, in 2026. State and local taxes lower that figure."),
       ("What is my tax bracket?","Your bracket is the rate on your last dollar of taxable income, after the standard deduction. Only the income inside each bracket is taxed at that rate, so your average (effective) rate is always lower than your top bracket."),
       ("Does a 401(k) reduce Social Security and Medicare tax?","No. Traditional 401(k) contributions reduce federal income tax and usually state tax, but Social Security and Medicare are still charged on that money."),
       ("Why is my real paycheck different?","Employers withhold based on your W-4, and paychecks can also include health insurance, local taxes, credits such as the child tax credit, and other deductions this estimate doesn't cover.")],
 related=["salary","timecard","percent","loan"])

# ---------- concrete ----------
slab = 10 * 10 * 4 / 12; slab_w = slab * 1.1
hole = math.pi * (5 / 12) ** 2 * 3; holes8 = hole * 8 * 1.1
tool(id="concrete", slug="concrete-calculator", cat="Home", name="Concrete Calculator",
 short="Concrete", desc="Cubic yards or m³ and bags for slabs and post holes.",
 title="Concrete Calculator – Cubic Yards & Bags | Numbrik",
 meta="Work out how much concrete you need for a slab, patio or post holes in cubic yards, cubic feet or m³, and how many 40, 60 or 80 lb bags to buy.",
 lede="Work out how much concrete you need for a slab, patio, path or post holes, in cubic yards, cubic feet or cubic metres, and how many bags to buy.",
 steps=["Choose a slab or post holes, and feet or metres.","Enter the size and thickness, or the hole diameter and depth, and how many you need.","Keep about 10% extra for waste and uneven ground.","Read the volume and the number of bags for each bag size."],
 how="""<p>Concrete is ordered by volume. For a slab, multiply length by width by thickness. Because slab thickness is usually measured in inches, divide it by 12 to turn it into feet. One cubic yard is 27 cubic feet, and ready-mix concrete in the US is sold by the cubic yard. In Canada, Australia, the UK and the Netherlands it is sold by the cubic metre.</p>
<p>For post holes the calculator uses the volume of a cylinder. It ignores the post itself, which gives a little extra. Typical thickness is 4 inches (10 cm) for patios and paths and 5 to 6 inches (12–15 cm) for driveways. For jobs above about one cubic yard, ready-mix delivery is usually easier than mixing bags by hand.</p>""",
 formula="Slab (cu ft)   = length (ft) × width (ft) × thickness (in) ÷ 12\nCubic yards    = cubic feet ÷ 27\nPost hole      = π × (diameter ÷ 2)² × depth\nBags           = volume ÷ bag yield, rounded up",
 example=f"""<p>A 10 × 10 ft patio, 4 inches thick, needs {slab:.2f} cubic feet, or {slab/27:.2f} cubic yards. With 10% extra that is <strong>{slab_w/27:.2f} cubic yards</strong>, or <strong>{math.ceil(slab_w/0.6)} bags of 80 lb</strong> premix.</p>
<p>Eight fence post holes, each 10 inches wide and 36 inches deep, need {holes8:.1f} cubic feet with 10% extra, which is {math.ceil(holes8/0.6)} bags of 80 lb concrete.</p>""",
 extra="""<h3>Bag yields</h3><div class="tbl"><table><thead><tr><th>Bag</th><th>Makes about</th><th>Bags per cubic yard</th></tr></thead><tbody>
<tr><td>80 lb</td><td>0.60 cu ft</td><td>45</td></tr><tr><td>60 lb</td><td>0.45 cu ft</td><td>60</td></tr><tr><td>40 lb</td><td>0.30 cu ft</td><td>90</td></tr><tr><td>20 kg</td><td>0.01 m³ (10 litres)</td><td>100 per m³</td></tr></tbody></table></div>
<p>Yields differ slightly between brands, so check the bag.</p>""",
 faqs=[("How many 80 lb bags of concrete are in a yard?","About 45. Each 80 lb bag makes roughly 0.6 cubic feet, and a cubic yard is 27 cubic feet."),
       ("How thick should a concrete slab be?","About 4 inches (10 cm) for patios, paths and shed bases, and 5 to 6 inches (12–15 cm) for driveways that carry cars. Heavier loads need more, and local building codes may set a minimum."),
       ("How much does a cubic yard of concrete weigh?","Roughly 4,000 lb, or about 2 US tons. A cubic metre weighs about 2,400 kg."),
       ("How do I convert cubic metres to cubic yards?","Multiply by 1.308. One cubic metre is about 1.31 cubic yards.")],
 related=["sqft","paint","convert","percent"])

# ---------- paint ----------
def paint(l, w, h, d=1, win=2, coats=2, cov=350):
    walls = 2 * (l + w) * h - d * 20 - win * 15
    return walls, walls * coats / cov
pw, pg = paint(14, 12, 8)
mw = 2 * (4.2 + 3.6) * 2.4 - 1.9 - 2.8
p_rows = "".join(f"<tr><td>{l} × {w} ft</td><td>{paint(l,w,8)[0]:.0f} sq ft</td><td>{paint(l,w,8)[1]:.1f} gal</td><td>{math.ceil(paint(l,w,8)[1])} gal</td></tr>" for l, w in [(10,10),(12,12),(14,12),(16,14),(20,15)])
tool(id="paint", slug="paint-calculator", cat="Home", name="Paint Calculator",
 short="Paint", desc="How much paint a room needs, in gallons or litres.",
 title="Paint Calculator – How Much Paint for a Room | Numbrik",
 meta="Find out how many gallons or litres of paint you need for a room. Includes doors, windows, ceiling and number of coats, with a quick room-size chart.",
 lede="Find out how much paint a room needs in gallons or litres, allowing for doors, windows, the ceiling and the number of coats.",
 steps=["Choose feet and gallons or metres and litres.","Enter the room's length, width and wall height.","Add the number of doors, windows and coats, and choose whether to paint the ceiling.","Read how much paint you need and how many whole cans to buy."],
 how="""<p>The wall area is the distance around the room multiplied by the wall height. The calculator then takes off a typical door and window, multiplies by the number of coats and divides by the paint's coverage.</p>
<p>Most interior wall paint covers about 350 to 400 square feet per gallon, or roughly 10 m² per litre, on smooth walls. Textured walls, bare plaster and new drywall soak up more, so expect lower coverage or use a primer first. Two coats are normal, especially when changing colour. A US gallon is 3.785 litres, and a quart is a quarter of a gallon.</p>""",
 formula="Wall area   = 2 × (length + width) × height − doors − windows\nPaint       = (wall area + ceiling) × coats ÷ coverage",
 example=f"""<p>A 14 × 12 ft bedroom with 8 ft walls, one door and two windows has about {pw:.0f} sq ft of wall. Two coats at 350 sq ft per gallon need <strong>{pg:.2f} gallons</strong>, so buy 2 gallons and a quart, or 3 gallons. In metric, a 4.2 × 3.6 m room with 2.4 m walls has about {mw:.1f} m² of wall and needs about <strong>{mw*2/10:.1f} litres</strong> for two coats.</p>""",
 extra=f"""<h3>Paint for common room sizes</h3><p>Walls only, 8 ft ceilings, one door, two windows, two coats at 350 sq ft per gallon.</p><div class="tbl"><table><thead><tr><th>Room</th><th>Wall area</th><th>Paint</th><th>Buy</th></tr></thead><tbody>{p_rows}</tbody></table></div>""",
 faqs=[("How much paint do I need for a 12 × 12 room?", f"About {paint(12,12,8)[1]:.1f} gallons for two coats on 8 ft walls with one door and two windows, so buy 3 gallons, or 2 gallons and a quart."),
       ("How many coats of paint do I need?","Two coats for most walls. One coat can be enough when repainting the same colour, while bright or dark colours over a light wall may need three, or a tinted primer."),
       ("How much paint do I need per square foot?","About 1 gallon for every 350 to 400 square feet per coat. Divide your wall area by the coverage on the can."),
       ("Should I buy extra paint?","Keep a little left over for touch-ups. Buying from one batch also avoids slight colour differences between cans.")],
 related=["sqft","concrete","convert","percent"])

# ---------- random number ----------
tool(id="random", slug="random-number-generator", cat="Fun", name="Random Number Generator",
 short="Random number", desc="Random whole numbers in any range, with or without repeats.",
 title="Random Number Generator – Pick a Number | Numbrik",
 meta="Generate random numbers between any two values. Pick one number or up to 1,000, with or without repeats, sorted or as drawn. Fair and unbiased.",
 lede="Pick one random number or up to 1,000 in any range, with or without repeats. Use it for raffles, games, classroom draws or choosing a winner.",
 steps=["Enter the lowest and highest number.","Choose how many numbers you want and whether repeats are allowed.","Press Generate. Change any setting or press it again for a new draw."],
 how="""<p>Numbers come from your browser's cryptographic random number generator. The calculator also uses rejection sampling, which throws away the few raw values that would make some numbers slightly more likely, so every number in the range has exactly the same chance.</p>
<p>With "No repeats" each number can come up only once, like drawing tickets from a hat. With repeats allowed, every draw is independent, like rolling a die again and again. Negative numbers work too.</p>""",
 formula="Chance of a given number = 1 ÷ (highest − lowest + 1)\nWays to draw k of n without repeats = n! ÷ (k! × (n − k)!)",
 example=f"<p>Picking one number from 1 to 100 gives each number a 1% chance. Drawing 6 numbers from 1 to 49 with no repeats can produce {math.comb(49,6):,} different sets, so the chance of matching all six is 1 in {math.comb(49,6):,}.</p>",
 extra="""<h2>Ways to use it</h2><ul>
<li><strong>Pick a winner:</strong> number your entries, then generate one number from 1 to the number of entries.</li>
<li><strong>Classroom:</strong> choose students to answer by their number on the register, with no repeats so nobody is picked twice.</li>
<li><strong>Games:</strong> replace lost dice or spinners, or decide who goes first.</li>
<li><strong>Sampling:</strong> choose random rows or items to check from a list.</li></ul>
<p>For official lotteries and prize draws, local laws may require a specific, audited process.</p>""",
 faqs=[("Is this random number generator truly random?","It uses the browser's cryptographic generator, which is designed to be unpredictable, plus a method that removes bias. Each number in your range is equally likely."),
       ("How do I pick a random winner from a list?","Give each entry a number from 1 upward, then generate one number from 1 to the total. The entry with that number wins."),
       ("Can I generate negative numbers?","Yes. Enter a negative lowest number, for example −50 to 50."),
       ("How many numbers can I generate at once?","Up to 1,000. With no repeats, you can't ask for more numbers than the range contains.")],
 related=["coin","dice","lcm","percent"])

# ---------- coin flip ----------
tool(id="coin", slug="coin-flip", cat="Fun", name="Coin Flip",
 short="Coin flip", desc="Flip a coin once or up to 1,000 times.",
 title="Coin Flip – Heads or Tails Online | Numbrik",
 meta="Flip a coin online: heads or tails with a fair 50/50 result. Flip once or up to 1,000 times and see the totals, percentages and longest streak.",
 lede="Flip a virtual coin for a quick heads-or-tails decision, or flip it up to 1,000 times and see the totals and the longest streak.",
 steps=["Leave flips at 1 for a single heads-or-tails answer, or enter more.","Press Flip coin.","Read the result, the heads and tails count and the longest run."],
 how="""<p>Each flip takes one random value from your browser's cryptographic generator and turns it into heads or tails, so both sides have exactly a 50% chance and earlier flips never affect the next one.</p>
<p>Real coins are very close to fair but not perfect. A large 2023 study of more than 350,000 hand-tossed flips found coins landed on the same side they started on about 51% of the time. A virtual coin has no such bias.</p>
<p>Streaks are normal. Over 100 flips, a run of six or seven of the same side in a row is common. Believing tails is "due" after several heads is the gambler's fallacy: the next flip is still 50/50.</p>""",
 formula="Chance of heads = 1 ÷ 2\nChance of k heads in a row = (1 ÷ 2)ᵏ",
 example="<p>The chance of three heads in a row is ½ × ½ × ½ = 12.5%. Ten heads in a row is 1 in 1,024, or about 0.1%.</p>",
 extra="""<h3>Chance of a streak</h3><div class="tbl"><table><thead><tr><th>Same side in a row</th><th>Chance from a fresh start</th></tr></thead><tbody>
<tr><td>2</td><td>25%</td></tr><tr><td>3</td><td>12.5%</td></tr><tr><td>4</td><td>6.25%</td></tr><tr><td>5</td><td>3.13%</td></tr><tr><td>10</td><td>0.098% (1 in 1,024)</td></tr></tbody></table></div>""",
 faqs=[("Is an online coin flip 50/50?","Yes. Each flip here has exactly a 50% chance of heads and 50% of tails, and flips are independent."),
       ("What are the odds of 10 heads in a row?","1 in 1,024, about 0.1%."),
       ("How does best of three work?","Flip until one side has won twice. It takes two or three flips and gives each side an equal chance overall."),
       ("Is it fair to use a coin flip to decide?","For two equal options, yes. Some people find that their reaction to the result shows which option they really wanted.")],
 related=["dice","random","percent","gcf"])

BYID.update({t["id"]: t for t in T})
