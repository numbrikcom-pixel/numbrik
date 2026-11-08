"""Calculators chosen from calculator.net's sitemap gap (November 8, 2026): discount, TDEE, ideal weight, Roman numerals,
simple interest, tile, long division, z-score, margin and gas cost."""
import math
from content import tool, T, BYID

def tbl(head, rows):
    return ('<div class="tbl"><table><thead><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")
usd = lambda x: f"${x:,.2f}"

# ---------- Discount ----------
tool(id="discount", slug="discount-calculator", cat="Money", name="Discount Calculator",
 short="Discount calculator", desc="Sale price and savings after a percent off.",
 title="Discount Calculator – Sale Price After % Off | Numbrik",
 meta="Work out the sale price and how much you save after a percent-off discount, including stacked “extra % off” deals and sales tax. Free, instant, with a chart.",
 lede="Enter the original price and the percent off to see the sale price and how much you save. Add an extra discount for stacked deals like “25% off plus an extra 10%”, and sales tax for the total at the register.",
 steps=["Enter the original (tag) price.", "Enter the discount, such as 25 for 25% off.",
        "Optional: add an extra discount and your sales tax rate.", "Read the sale price, your savings and the effective discount."],
 how="""<p>The sale price is the original price multiplied by (1 − discount ÷ 100). A $80 item at 25% off costs $80 × 0.75 = $60, so you save $20.</p>
<p>Stacked discounts multiply rather than add. “25% off, then an extra 10% off” takes 10% off the $60 sale price, not the original $80, giving $54. That's 32.5% off in total, not 35%. Sales tax is charged on the price after discounts in most US states.</p>""",
 formula="Sale price = price × (1 − discount ÷ 100)\nStacked: price × (1 − d1 ÷ 100) × (1 − d2 ÷ 100)\nYou save = price − sale price",
 example="<p>A jacket tagged <strong>$80</strong> is 25% off, with an extra 10% off at checkout. First discount: $80 × 0.75 = $60. Extra discount: $60 × 0.90 = <strong>$54</strong>. You save $26, which is 32.5% off.</p>",
 extra="<h3>Percent off chart</h3>" + tbl(["Price"] + [f"{d}% off" for d in (10, 15, 20, 25, 30, 40, 50)],
   [[usd(p)] + [usd(p * (1 - d / 100)) for d in (10, 15, 20, 25, 30, 40, 50)] for p in (10, 20, 25, 50, 75, 100, 150, 200, 250, 500)]) +
 "<h3>Stacked discounts: what you really get</h3>" + tbl(["Deal", "Total discount"],
   [(f"{a}% + extra {b}% off", f"{100 - (100 - a) * (100 - b) / 100:g}%") for a, b in ((20, 10), (25, 10), (30, 20), (40, 20), (50, 20), (50, 50))]),
 faqs=[("How do I calculate a discount?", "Multiply the price by the discount percentage and divide by 100 to get the savings, then subtract it. 30% off $45 is $45 × 0.30 = $13.50 off, so you pay $31.50."),
       ("Is 20% off plus an extra 20% off the same as 40% off?", "No. The second 20% comes off the already-reduced price, so the total is 36% off. On $100 you'd pay $64, not $60."),
       ("How do I find the original price from a sale price?", "Divide the sale price by (1 − discount). If something costs $60 after 25% off, the original price was $60 ÷ 0.75 = $80."),
       ("Is sales tax calculated before or after the discount?", "For store discounts and coupons, sales tax is usually charged on the discounted price. Manufacturer coupons can be taxed on the full price in some states.")],
 related=["percent", "salestax", "tip", "margin"])

# ---------- TDEE ----------
def tdee(sex, kg, cm, age, f):
    return (10 * kg + 6.25 * cm - 5 * age + (5 if sex == "m" else -161)) * f
tool(id="tdee", slug="tdee-calculator", cat="Health", name="TDEE Calculator",
 short="TDEE calculator", desc="Maintenance calories from your activity level.",
 title="TDEE Calculator – Maintenance Calories Per Day | Numbrik",
 meta="Calculate your TDEE (total daily energy expenditure): the calories you burn a day with exercise. Get maintenance, weight loss and lean bulk calories.",
 lede="Your TDEE (total daily energy expenditure) is how many calories you burn in a day, including exercise. Eat that many to keep your weight steady, fewer to lose weight, or more to gain. Enter your details and activity level to get yours.",
 steps=["Choose male or female and your units.", "Enter your age, height and weight.", "Pick the activity level that matches a normal week.",
        "Read your maintenance calories plus targets for losing or gaining weight."],
 how="""<p>The calculator first estimates your basal metabolic rate (BMR), the energy you'd use resting all day, with the Mifflin-St Jeor equation. Studies have found it the most accurate of the common BMR formulas for most adults. It then multiplies BMR by an activity factor: 1.2 for a desk job with little exercise, 1.375 for light exercise, 1.55 for moderate, 1.725 for hard exercise most days and 1.9 for very hard training or physical work.</p>
<p>A pound of body fat holds roughly 3,500 calories, so eating about 500 calories below TDEE each day leads to roughly a pound a week of weight loss at first. Real results vary, and the loss slows as your weight drops, so recalculate every 10 pounds or so.</p>""",
 formula="BMR (men) = 10 × kg + 6.25 × cm − 5 × age + 5\nBMR (women) = 10 × kg + 6.25 × cm − 5 × age − 161\nTDEE = BMR × activity factor",
 example=f"<p>A 30-year-old man, 5 ft 10 in (178 cm) and 180 lb (81.6 kg), who exercises 3–5 days a week: BMR = {tdee('m', 81.65, 177.8, 30, 1):,.0f} calories. TDEE = {tdee('m', 81.65, 177.8, 30, 1):,.0f} × 1.55 = <strong>{tdee('m', 81.65, 177.8, 30, 1.55):,.0f} calories a day</strong>. To lose about a pound a week he'd aim for around {tdee('m', 81.65, 177.8, 30, 1.55) - 500:,.0f}.</p>",
 extra="<h3>Activity levels</h3>" + tbl(["Level", "What it means", "Multiplier"], [("Desk job", "Little or no exercise", "1.2"), ("Light", "Exercise 1–3 days a week", "1.375"), ("Moderate", "Exercise 3–5 days a week", "1.55"), ("Active", "Hard exercise 6–7 days a week", "1.725"), ("Very active", "Twice-daily training or a physical job", "1.9")]) +
 "<h3>TDEE examples by weight (age 30, moderate activity)</h3>" + tbl(["Weight", "Men, 5 ft 10 in", "Women, 5 ft 5 in"],
   [(f"{lb} lb", f"{tdee('m', lb * 0.4536, 177.8, 30, 1.55):,.0f}", f"{tdee('f', lb * 0.4536, 165.1, 30, 1.55):,.0f}") for lb in (120, 140, 160, 180, 200, 220, 250)]),
 faqs=[("What is TDEE?", "Total daily energy expenditure: all the calories you burn in a day, from your resting metabolism, digesting food, everyday movement and exercise."),
       ("What's the difference between BMR and TDEE?", "BMR is the energy you'd burn lying still all day. TDEE adds everything else you do, so it's always higher, usually 1.2 to 1.9 times BMR."),
       ("How many calories should I eat to lose weight?", "A common starting point is 300–500 calories below your TDEE, which aims for about 0.5–1 lb a week. Avoid going below about 1,500 calories a day for men or 1,200 for women without medical advice."),
       ("Why am I not losing weight at my TDEE deficit?", "Activity levels are often overestimated, food tracking misses calories, and water weight can hide fat loss for a week or two. Try the next activity level down and track for three to four weeks.")],
 related=["bmr", "calorie", "macro", "protein"])

# ---------- Ideal weight ----------
def iw(sex, inch):
    o = max(0, inch - 60); m = sex == "m"
    return [m and 52 + 1.9 * o or 49 + 1.7 * o, m and 56.2 + 1.41 * o or 53.1 + 1.36 * o, m and 50 + 2.3 * o or 45.5 + 2.3 * o, m and 48 + 2.7 * o or 45.5 + 2.2 * o]
lb = lambda kg: kg / 0.45359237
def iwrow(sex, inch):
    v = iw(sex, inch); hm = inch * 0.0254
    return (f"{inch // 12} ft {inch % 12} in", f"{lb(min(v)):.0f}–{lb(max(v)):.0f} lb", f"{lb(18.5 * hm * hm):.0f}–{lb(24.9 * hm * hm):.0f} lb")
tool(id="idealweight", slug="ideal-weight-calculator", cat="Health", name="Ideal Weight Calculator",
 short="Ideal weight calculator", desc="Ideal body weight for your height, four formulas.",
 title="Ideal Weight Calculator – What Should I Weigh? | Numbrik",
 meta="How much should you weigh for your height? Get your ideal body weight from the Devine, Robinson, Miller and Hamwi formulas plus the healthy BMI weight range.",
 lede="Find a healthy target weight for your height. The calculator gives your ideal body weight from four medical formulas and the weight range that puts you in the healthy BMI band of 18.5 to 24.9.",
 steps=["Choose male or female and your units.", "Enter your height.", "Read the ideal weight range from the four formulas and your healthy BMI range."],
 how="""<p>Ideal body weight (IBW) formulas start from a base weight at 5 feet tall and add a fixed amount for each inch above that. The Devine formula (1974) was written to dose medicines and is still used in hospitals. Robinson and Miller (both 1983) refined it with population data, and the Hamwi formula (1964) is common in nutrition. They give slightly different answers, so the calculator shows the range.</p>
<p>The healthy BMI range is wider and more practical: any weight that gives a BMI from 18.5 to 24.9 is classed as a healthy weight by the World Health Organization. Neither method knows how much muscle you carry, so athletes can be healthy above both, and older adults may be better off slightly higher.</p>""",
 formula="Devine (men) = 50 kg + 2.3 kg per inch over 5 ft\nDevine (women) = 45.5 kg + 2.3 kg per inch over 5 ft\nHealthy BMI weight = 18.5 to 24.9 × height (m)²",
 example=f"<p>A man who is 5 ft 10 in has 10 inches over 5 feet. Devine: 50 + 2.3 × 10 = 73 kg (<strong>161 lb</strong>). Robinson gives 71 kg (157 lb), Miller 70.3 kg (155 lb) and Hamwi 75 kg (165 lb). His healthy BMI range is {iwrow('m', 70)[2]}.</p>",
 extra="<h3>Ideal weight chart for men</h3>" + tbl(["Height", "Ideal weight (4 formulas)", "Healthy BMI range"], [iwrow("m", i) for i in range(62, 78)]) +
 "<h3>Ideal weight chart for women</h3>" + tbl(["Height", "Ideal weight (4 formulas)", "Healthy BMI range"], [iwrow("f", i) for i in range(58, 74)]),
 faqs=[("How much should I weigh for my height?", "For most adults, any weight in the healthy BMI range of 18.5 to 24.9 is a reasonable target. For someone 5 ft 6 in tall that's about 115 to 154 lb."),
       ("Which ideal weight formula is most accurate?", "None is accurate for everyone. Robinson and Miller are based on more recent data; Devine is the hospital standard for drug dosing. Use the range as a guide, not a single number."),
       ("Does age change my ideal weight?", "The formulas don't use age. Some research suggests a BMI slightly above 25 carries little extra risk for adults over 65, so ask your doctor what suits you."),
       ("Why is my ideal weight lower than I expected?", "These formulas ignore muscle mass and frame size. Muscular people often weigh more than the formula suggests and are still healthy. A body fat measurement tells you more.")],
 related=["bmi", "bodyfat", "tdee", "calorie"])

# ---------- Roman numerals ----------
RV = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
def rom(n):
    o = ""
    for a, r in RV:
        while n >= a: o += r; n -= a
    return o
tool(id="roman", slug="roman-numeral-converter", cat="Converters", name="Roman Numeral Converter",
 short="Roman numeral converter", desc="Numbers to Roman numerals and back.",
 title="Roman Numeral Converter – Numbers, Years & Dates | Numbrik",
 meta="Convert numbers to Roman numerals and Roman numerals to numbers, from 1 to 3,999. Works for years and dates (2026 = MMXXVI), with full charts.",
 lede="Type a number to get it in Roman numerals, or type Roman numerals to get the number. It also converts years and full dates, which is handy for tattoos, clock faces, film credits and Super Bowl numbers.",
 steps=["Type a number (1 to 3,999), Roman numerals, or a date like 11/08/2026.", "The converter detects which way to convert.", "Read the result and the breakdown of each part."],
 how="""<p>Roman numerals use seven letters: I = 1, V = 5, X = 10, L = 50, C = 100, D = 500 and M = 1,000. You add letters from largest to smallest, so VIII = 5 + 1 + 1 + 1 = 8. When a smaller letter comes before a larger one, you subtract it: IV = 4, IX = 9, XL = 40, XC = 90, CD = 400 and CM = 900.</p>
<p>Standard numerals never repeat a letter more than three times in a row, which is why 4 is IV, not IIII (though many clock faces use IIII). Only I, X and C are used for subtraction. Without extra symbols, the largest number is 3,999 (MMMCMXCIX).</p>""",
 formula="I = 1   V = 5   X = 10   L = 50\nC = 100   D = 500   M = 1000\nIV = 4  IX = 9  XL = 40  XC = 90  CD = 400  CM = 900",
 example="<p>To write <strong>2026</strong>: 2000 = MM, 20 = XX, 6 = VI, so 2026 = <strong>MMXXVI</strong>. To read <strong>MCMXCIV</strong>: M (1000) + CM (900) + XC (90) + IV (4) = 1994.</p>",
 extra="<h3>Roman numerals 1 to 100</h3>" + tbl(["Number", "Roman", "Number", "Roman", "Number", "Roman", "Number", "Roman"],
   [sum(([str(n), rom(n)] for n in (r, r + 25, r + 50, r + 75)), []) for r in range(1, 26)]) +
 "<h3>Years in Roman numerals</h3>" + tbl(["Year", "Roman numerals"], [(y, rom(y)) for y in list(range(1990, 2001, 5)) + list(range(2010, 2031))]),
 faqs=[("What is 2026 in Roman numerals?", "MMXXVI: MM (2000) + XX (20) + VI (6)."),
       ("How do you write 4 in Roman numerals?", "IV, meaning one less than five. Some clocks show IIII, but IV is the standard form."),
       ("Is there a zero in Roman numerals?", "No. The Romans had no numeral for zero. Medieval writers sometimes used N (for nulla) instead."),
       ("How do I write a date in Roman numerals?", "Convert the month, day and year separately and join them with dots or dashes. November 8, 2026 is XI.VIII.MMXXVI in month-day-year order.")],
 related=["convert", "military", "scientific", "random"])

# ---------- Simple interest ----------
tool(id="simpleint", slug="simple-interest-calculator", cat="Money", name="Simple Interest Calculator",
 short="Simple interest", desc="Interest and total with I = P × r × t.",
 title="Simple Interest Calculator – I = Prt Formula | Numbrik",
 meta="Calculate simple interest with I = P × r × t. Enter principal, rate and time in years, months or days to get the interest, total and the compound comparison.",
 lede="Work out simple interest on a loan or savings with the formula I = P × r × t. Enter the principal, annual rate and time to get the interest, the total amount, and how it compares with compound interest.",
 steps=["Enter the principal (the amount borrowed or saved).", "Enter the annual interest rate.", "Enter the time and choose years, months or days.", "Read the interest, the total and the interest per year, month and day."],
 how="""<p>Simple interest is paid only on the original principal, never on interest already earned. Multiply the principal by the annual rate (as a decimal) and by the time in years. For months, divide by 12; for days, divide by 365.</p>
<p>Car loans, some personal loans, bonds and short-term notes often use simple interest. Most savings accounts and credit cards compound, so they grow faster. The calculator shows the compound figure for comparison.</p>""",
 formula="I = P × r × t\nTotal (A) = P × (1 + r × t)\nr = annual rate ÷ 100,  t = years",
 example="<p><strong>$10,000</strong> at <strong>5%</strong> for <strong>3 years</strong>: I = 10,000 × 0.05 × 3 = <strong>$1,500</strong>. The total is $11,500. Compounded yearly, the same deposit would earn $1,576.25.</p>",
 extra="<h3>Simple interest on $10,000</h3>" + tbl(["Rate", "1 year", "2 years", "3 years", "5 years", "10 years"],
   [[f"{r}%"] + [usd(10000 * r / 100 * t) for t in (1, 2, 3, 5, 10)] for r in (2, 3, 4, 5, 6, 7, 8, 10)]) +
 "<h3>Simple vs compound interest on $10,000 at 5%</h3>" + tbl(["Years", "Simple interest", "Compound (yearly)", "Difference"],
   [(t, usd(500 * t), usd(10000 * (1.05 ** t - 1)), usd(10000 * (1.05 ** t - 1) - 500 * t)) for t in (1, 3, 5, 10, 20, 30)]),
 faqs=[("What is the simple interest formula?", "I = P × r × t: principal times the annual rate (as a decimal) times the time in years."),
       ("How do I calculate simple interest for months?", "Divide the months by 12 to get years. $5,000 at 6% for 8 months is 5,000 × 0.06 × 8/12 = $200."),
       ("How do I find the rate or time?", "Rearrange the formula: r = I ÷ (P × t) and t = I ÷ (P × r). Earning $300 on $2,000 in 3 years means r = 300 ÷ 6,000 = 5%."),
       ("Is simple or compound interest better?", "Simple interest is better when you borrow, because you pay less. Compound interest is better when you save or invest, because your interest earns interest.")],
 related=["compound", "cd", "loan", "autoloan"])

# ---------- Tile ----------
def tiles(sqft, a, b, waste=10):
    return math.ceil(sqft / (a * b / 144) * (1 + waste / 100))
tool(id="tile", slug="tile-calculator", cat="Home", name="Tile Calculator",
 short="Tile calculator", desc="Number of tiles and boxes for a floor or wall.",
 title="Tile Calculator – How Many Tiles Do I Need? | Numbrik",
 meta="Find out how many tiles and boxes you need for a floor, wall or backsplash. Enter the area, tile size, grout gap and waste to get an exact count.",
 lede="Work out how many tiles you need for a floor, wall, shower or backsplash. Enter the area, your tile size and grout gap, and the calculator adds a waste allowance and tells you how many boxes to buy.",
 steps=["Measure the length and width of the area.", "Enter the tile size and grout joint.", "Set the waste allowance: 10% for straight layouts, 15% for diagonal or herringbone.", "Enter the tiles per box to get the number of boxes."],
 how="""<p>The calculator divides the area by the space one tile covers, including half a grout joint on each side, and rounds up. It then adds the waste allowance for cuts, breakages and mistakes.</p>
<p>Buy all your tile at once from the same batch (lot number), because shades vary between batches. Keep a few spare tiles after the job for future repairs. For rooms with lots of corners or a feature pattern, use 15–20% waste.</p>""",
 formula="Tile area = (length + grout) × (width + grout)\nTiles = room area ÷ tile area × (1 + waste ÷ 100)\nBoxes = tiles ÷ tiles per box, rounded up",
 example=f"<p>A <strong>12 × 10 ft</strong> floor (120 sq ft) with <strong>12 × 24 in</strong> tiles: each tile covers 2 sq ft, so you need 60 tiles. With 10% waste that's <strong>66 tiles</strong>, or 9 boxes of 8. With 1/8-inch grout joints each tile covers slightly more floor, so the calculator shows 65.</p>",
 extra="<h3>Tiles needed per 100 square feet</h3>" + tbl(["Tile size", "Tiles (no waste)", "With 10% waste", "With 15% waste"],
   [(f"{a} × {b} in", math.ceil(100 / (a * b / 144)), tiles(100, a, b, 10), tiles(100, a, b, 15)) for a, b in ((4, 4), (6, 6), (3, 6), (4, 12), (6, 24), (8, 8), (12, 12), (12, 24), (16, 16), (18, 18), (24, 24), (24, 48))]),
 faqs=[("How many 12x24 tiles do I need for 100 square feet?", "Each 12 × 24 tile covers 2 square feet, so 50 tiles, or 55 with 10% waste."),
       ("How much extra tile should I buy?", "10% for a straight layout in a simple room, 15% for diagonal, herringbone or rooms with many cuts, and up to 20% for large-format tiles that break easily."),
       ("How do I measure an L-shaped room?", "Split it into rectangles, work out each area, and add them together before entering the total."),
       ("Do I need to include grout lines?", "For small tiles, yes. Grout joints add up: 1/8-inch joints on 4-inch tiles reduce the count by about 6%. For large tiles the difference is tiny.")],
 related=["sqft", "paint", "concrete", "mulch"])

# ---------- Long division ----------
tool(id="longdiv", slug="long-division-calculator", cat="Math", name="Long Division Calculator",
 short="Long division", desc="Quotient and remainder with every step shown.",
 title="Long Division Calculator with Steps & Remainders | Numbrik",
 meta="Divide any two numbers with long division and see every step: divide, multiply, subtract, bring down. Get the quotient, remainder, decimal and mixed number.",
 lede="Enter a dividend and divisor to get the quotient and remainder, with every long-division step written out. Great for checking homework: you also get the decimal answer and the mixed number.",
 steps=["Enter the dividend (the number being divided).", "Enter the divisor (the number you divide by).", "Read the quotient and remainder, then follow the step table: divide, multiply, subtract, bring down."],
 how="""<p>Long division breaks a big division into small ones, working left to right through the digits of the dividend. At each step you divide the current number by the divisor, write the whole-number result in the quotient, multiply it back, subtract, and bring down the next digit. Whatever is left at the end is the remainder.</p>
<p>A handy memory aid is “Does McDonald's Sell Cheese Burgers”: Divide, Multiply, Subtract, Check, Bring down. To check your answer, multiply the quotient by the divisor and add the remainder: you should get the dividend.</p>""",
 formula="Dividend = divisor × quotient + remainder\n0 ≤ remainder < divisor",
 example="<p><strong>1,764 ÷ 13</strong>: 17 ÷ 13 = 1, remainder 4. Bring down 6: 46 ÷ 13 = 3, remainder 7. Bring down 4: 74 ÷ 13 = 5, remainder 9. The answer is <strong>135 R 9</strong>, or 135 9/13 ≈ 135.692. Check: 13 × 135 + 9 = 1,764.</p>",
 extra="<h3>Division facts to know</h3>" + tbl(["Divisor", "Divisibility rule"],
   [("2", "The last digit is even"), ("3", "The digits add up to a multiple of 3"), ("4", "The last two digits make a multiple of 4"), ("5", "The last digit is 0 or 5"), ("6", "It divides by both 2 and 3"), ("8", "The last three digits make a multiple of 8"), ("9", "The digits add up to a multiple of 9"), ("10", "The last digit is 0")]) +
 "<h3>Common divisions with remainders</h3>" + tbl(["Division", "Quotient R remainder", "Decimal"], [(f"{a} ÷ {b}", f"{a // b} R {a % b}", f"{a / b:.4f}".rstrip("0").rstrip(".")) for a, b in ((100, 7), (250, 12), (365, 7), (500, 9), (1000, 3), (1000, 6), (1000, 7), (1440, 60), (2026, 4), (5280, 12))]),
 faqs=[("How do you do long division step by step?", "Divide, multiply, subtract, bring down, and repeat until there are no digits left. The number you end with is the remainder."),
       ("How do I turn a remainder into a decimal?", "Add a decimal point and zeros to the dividend and keep dividing. Or divide the remainder by the divisor: 9 ÷ 13 ≈ 0.692, so 135 R 9 is 135.692."),
       ("How do I write a remainder as a fraction?", "Put the remainder over the divisor. 135 R 9 when dividing by 13 is 135 9/13."),
       ("What do I do when the divisor is bigger than the first digit?", "Use the first two digits instead (or more). In 1,764 ÷ 13, 1 is too small, so start with 17.")],
 related=["fraction", "scientific", "gcf", "lcm"])

# ---------- Z-score ----------
def phi(z): return 0.5 * (1 + math.erf(z / math.sqrt(2)))
tool(id="zscore", slug="z-score-calculator", cat="Math", name="Z-Score Calculator",
 short="Z-score calculator", desc="Z-score, percentile and probability from a raw score.",
 title="Z-Score Calculator – Percentile & Probability | Numbrik",
 meta="Calculate a z-score from a raw score, mean and standard deviation, and get the percentile, left and right tail probabilities and two-tailed p-value.",
 lede="Enter a raw score, the mean and the standard deviation to get the z-score, plus the percentile and probabilities from the normal distribution. No z-table needed.",
 steps=["Enter the raw score (x).", "Enter the mean (μ) and standard deviation (σ) of the data.", "Read the z-score, the percentile and the tail probabilities."],
 how="""<p>A z-score says how many standard deviations a value is from the mean. A z-score of 0 is exactly average, +1 is one standard deviation above, and −2 is two below. Because it removes the units, you can compare scores from different tests, such as an SAT score and an ACT score.</p>
<p>If the data follow a normal distribution, the z-score converts to a percentile: about 68% of values fall within ±1, 95% within ±1.96 and 99.7% within ±3. The calculator uses the standard normal cumulative distribution to find the area to the left of your z-score.</p>""",
 formula="z = (x − μ) ÷ σ\nPercentile = Φ(z) × 100\nTwo-tailed p = 2 × (1 − Φ(|z|))",
 example=f"<p>A test has a mean of <strong>70</strong> and a standard deviation of <strong>10</strong>. A score of <strong>85</strong> has z = (85 − 70) ÷ 10 = <strong>1.5</strong>. That's higher than about {phi(1.5) * 100:.2f}% of test takers (the 93rd percentile).</p>",
 extra="<h3>Z-score to percentile table</h3>" + tbl(["z", "Percentile", "z", "Percentile"],
   [(f"{-z:.1f}", f"{phi(-z) * 100:.2f}%", f"{z:.1f}", f"{phi(z) * 100:.2f}%") for z in [x / 10 for x in range(0, 31, 2)]]) +
 "<h3>Critical z-values</h3>" + tbl(["Confidence level", "Two-tailed z", "One-tailed z"], [("80%", "1.282", "0.842"), ("90%", "1.645", "1.282"), ("95%", "1.960", "1.645"), ("98%", "2.326", "2.054"), ("99%", "2.576", "2.326"), ("99.9%", "3.291", "3.090")]),
 faqs=[("What is a good z-score?", "It depends on the context. Above +1 is better than about 84% of values, above +2 better than about 98%. In quality control, a z-score beyond ±3 usually flags an outlier."),
       ("Can a z-score be negative?", "Yes. A negative z-score means the value is below the mean. z = −1 is lower than about 84% of values (the 16th percentile)."),
       ("What's the z-score for 95% confidence?", "1.96 for a two-tailed interval and 1.645 for one-tailed."),
       ("How do I convert a z-score to a percentile?", "Find the area under the normal curve to the left of z. This calculator does it for you; z = 1 is the 84th percentile and z = 2 is the 98th.")],
 related=["stdev", "average", "scientific", "grade"])

# ---------- Margin ----------
tool(id="margin", slug="margin-calculator", cat="Money", name="Margin Calculator",
 short="Margin calculator", desc="Profit margin, markup and selling price.",
 title="Margin Calculator – Profit Margin & Markup | Numbrik",
 meta="Calculate gross profit margin and markup from cost and price, or find the selling price for a target margin. Includes a margin vs markup chart.",
 lede="Enter your cost and selling price to see the profit, gross margin and markup. Or enter the cost and the margin (or markup) you want, and get the price to charge.",
 steps=["Choose what you know: cost and price, cost and margin, or cost and markup.", "Enter the numbers.", "Read the selling price, profit, margin and markup."],
 how="""<p>Margin and markup both describe profit, but against different bases. Gross margin is profit as a percentage of the selling price. Markup is profit as a percentage of the cost. Buy at $40 and sell at $60 and you make $20: a 33.3% margin but a 50% markup.</p>
<p>Mixing them up is a common pricing mistake. If you want a 30% margin and add 30% to the cost, you only get a 23% margin. To hit a target margin, divide the cost by (1 − margin). Margin can never reach 100%, but markup can be any size.</p>""",
 formula="Profit = price − cost\nMargin = profit ÷ price × 100\nMarkup = profit ÷ cost × 100\nPrice for a target margin = cost ÷ (1 − margin)",
 example="<p>A product costs <strong>$40</strong> and you want a <strong>30% margin</strong>. Price = 40 ÷ (1 − 0.30) = <strong>$57.14</strong>. Profit is $17.14, which is a 42.9% markup.</p>",
 extra="<h3>Margin vs markup chart</h3>" + tbl(["Markup", "Equals margin", "Margin", "Needs markup"],
   [(f"{k}%", f"{k / (100 + k) * 100:.1f}%", f"{m}%", f"{m / (100 - m) * 100:.1f}%") for k, m in ((10, 10), (20, 20), (25, 25), (30, 30), (40, 35), (50, 40), (75, 50), (100, 60), (150, 70), (200, 75))]),
 faqs=[("What's the difference between margin and markup?", "Margin is profit divided by price; markup is profit divided by cost. The same sale always has a higher markup than margin."),
       ("How do I calculate selling price from cost and margin?", "Divide the cost by (1 − margin as a decimal). For a $25 cost and a 40% margin: 25 ÷ 0.6 = $41.67."),
       ("What is a good profit margin?", "It varies widely by industry. Grocery stores often run on gross margins of 25–30%, while software and jewellery can exceed 50%. Compare with businesses like yours."),
       ("Is this gross or net margin?", "Gross margin: it only counts the cost of the product. Net margin also subtracts rent, wages, marketing and taxes, so it's lower.")],
 related=["discount", "percent", "salestax", "raise"])

# ---------- Gas cost ----------
tool(id="fuel", slug="gas-cost-calculator", cat="Money", name="Gas Cost Calculator",
 short="Gas cost calculator", desc="Fuel cost of a trip from distance and mileage.",
 title="Gas Cost Calculator – Trip Fuel Cost & Split | Numbrik",
 meta="How much will gas cost for your trip? Enter the distance, your car's MPG and the gas price to get the fuel cost, cost per mile and each person's share.",
 lede="Estimate how much gas a road trip will cost. Enter the distance, your car's fuel economy and the price per gallon, choose one way or round trip, and split the cost between passengers.",
 steps=["Enter the trip distance (check a map app for the miles).", "Enter your car's fuel economy in MPG.", "Enter the gas price per gallon.", "Choose round trip if you're coming back, and the number of people sharing."],
 how="""<p>Fuel used is the distance divided by your miles per gallon. Multiply that by the price per gallon to get the cost. In metric, multiply the distance by your litres per 100 km and divide by 100.</p>
<p>Real-world mileage is usually lower than the sticker figure: highway driving at 75–80 mph, a loaded car, roof boxes, cold weather and air conditioning can all cut MPG by 10–25%. For a safe budget, knock a few MPG off your car's rating.</p>""",
 formula="Gallons = miles ÷ MPG\nCost = gallons × price per gallon\nMetric: litres = km × L/100 km ÷ 100",
 example="<p>A <strong>300-mile</strong> trip in a car that gets <strong>28 MPG</strong>, with gas at <strong>$3.10</strong> a gallon: 300 ÷ 28 = 10.7 gallons × $3.10 = <strong>$33.21</strong> one way, or $66.43 for the round trip. Split between 3 people, that's $22.14 each.</p>",
 extra="<h3>Gas cost per 100 miles</h3>" + tbl(["MPG"] + [f"${p:.2f}/gal" for p in (2.75, 3.00, 3.25, 3.50, 4.00, 4.50)],
   [[str(m)] + [usd(100 / m * p) for p in (2.75, 3.00, 3.25, 3.50, 4.00, 4.50)] for m in (15, 20, 25, 30, 35, 40, 50)]),
 faqs=[("How do I calculate gas cost for a trip?", "Divide the miles by your car's MPG to get gallons, then multiply by the price per gallon. 450 miles at 30 MPG and $3.20 a gallon is 15 × $3.20 = $48."),
       ("How do I find my car's real MPG?", "Fill the tank, reset the trip meter, drive normally, then fill up again. Divide the miles driven by the gallons it took to refill."),
       ("How much is gas money for a ride?", "A fair share is the trip's fuel cost divided by everyone in the car, including the driver. Some people add a little extra for wear and tear on the car."),
       ("Does driving faster use more gas?", "Yes. Most cars are most efficient at around 50 mph or lower. Above that, air resistance rises quickly and fuel economy falls, so slowing from 80 to 65 mph on the highway can noticeably cut your gas bill.")],
 related=["autoloan", "convert", "pace", "salestax"])

BYID.update({t["id"]: t for t in T})
