"""Third batch, picked from the user's Google Trends export (top and rising "calculator" searches, Nov 7–8, 2026):
height, calorie deficit, BAC, bra size, numerology life path, loan and date calculators.
Gambling (parlay/odds/bet), game-specific and dosing (peptide) calculators were left out on purpose."""
import calendar
from datetime import date, timedelta
from content import tool, T, BYID

def tbl(head, rows):
    return ('<div class="tbl"><table><thead><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")
fi = lambda inch: f"{int(round(inch)) // 12} ft {int(round(inch)) % 12} in"

# ---------- Height ----------
tool(id="height", slug="height-calculator", cat="Health", name="Height Calculator",
 short="Height calculator", desc="Predict a child’s adult height from the parents’ heights.",
 title="Height Calculator – How Tall Will My Child Be? | Numbrik",
 meta="Predict how tall your child will be as an adult from both parents' heights (mid-parental method) or from their height as a toddler. Includes charts for boys and girls.",
 lede="How tall will your child be? Enter the mother's and father's heights to predict a boy's or girl's adult height with the mid-parental method doctors use, or use the toddler doubling rule.",
 steps=["Choose boy or girl and your units.", "Pick a method: parents' heights, or the child's height as a toddler.", "Enter the heights.", "Read the predicted adult height and the likely range."],
 how="""<p>The mid-parental height method averages the parents' heights and adjusts for sex: add 13 cm (5 inches) to the mother's height for a boy, or subtract 13 cm from the father's height for a girl, then average with the other parent. Paediatricians use it to see whether a child is growing along the expected path. About 95% of children end up within roughly 4 inches (10 cm) of the result.</p>
<p>The doubling rule is older and rougher: boys reach about twice their height at age 2, and girls about twice their height at 18 months. More accurate methods, such as Khamis-Roche, also use the child's current height and weight, and a bone-age X-ray is the most precise. Nutrition, sleep, health and puberty timing all play a part.</p>""",
 formula="Boy = (father + mother + 13 cm) ÷ 2\nGirl = (father + mother − 13 cm) ÷ 2\nIn inches: use 5 in instead of 13 cm\nLikely range: ± 10 cm (about 4 in)",
 example=f"<p>Father <strong>5 ft 10 in</strong> (70 in), mother <strong>5 ft 5 in</strong> (65 in). A son is predicted at (70 + 65 + 5) ÷ 2 = <strong>70 in (5 ft 10 in)</strong>, likely between 5 ft 6 in and 6 ft 2 in. A daughter: (70 + 65 − 5) ÷ 2 = <strong>65 in (5 ft 5 in)</strong>.</p>",
 extra="<h3>Predicted height for a boy (inches → feet)</h3>" + tbl(["Father \\ Mother"] + [fi(m) for m in (60, 62, 64, 66, 68)],
   [[fi(f)] + [fi((f + m + 5) / 2) for m in (60, 62, 64, 66, 68)] for f in (66, 68, 70, 72, 74, 76)]) +
 "<h3>Predicted height for a girl</h3>" + tbl(["Father \\ Mother"] + [fi(m) for m in (60, 62, 64, 66, 68)],
   [[fi(f)] + [fi((f + m - 5) / 2) for m in (60, 62, 64, 66, 68)] for f in (66, 68, 70, 72, 74, 76)]),
 faqs=[("How accurate is the height calculator?", "The mid-parental method puts most children within about 4 inches (10 cm) of the prediction. It can't account for nutrition, health problems or unusually early or late puberty."),
       ("When do boys and girls stop growing?", "Most girls reach adult height around 14 to 15, a couple of years after their first period. Most boys stop around 16 to 18, though some grow a little into their early 20s."),
       ("Can my child be taller than both parents?", "Yes. Height comes from many genes, and better nutrition means many children outgrow their parents. The prediction is only the most likely outcome."),
       ("Is the doubling rule reliable?", "It's a rough rule of thumb. It works best as a quick estimate; the parents' heights method is usually closer.")],
 related=["bmi", "age", "duedate", "convert"])

# ---------- Calorie deficit ----------
def msj(sex, kg, cm, age): return 10 * kg + 6.25 * cm - 5 * age + (5 if sex == "m" else -161)
ex_t = msj("f", 180 * 0.4536, 165.1, 35) * 1.375
tool(id="deficit", slug="calorie-deficit-calculator", cat="Health", name="Calorie Deficit Calculator",
 short="Calorie deficit", desc="Daily calories to reach a goal weight by a date.",
 title="Calorie Deficit Calculator – Lose Weight Safely | Numbrik",
 meta="Find how many calories to eat a day to lose weight at a safe pace, and when you'll reach your goal weight. Based on your TDEE and a 0.5–2 lb per week deficit.",
 lede="Find out how many calories to eat each day to lose weight, and roughly when you'll hit your goal. The calculator works out your maintenance calories, then subtracts a deficit for the pace you choose.",
 steps=["Enter your sex, age, height and current weight.", "Enter your goal weight and how active you are.", "Pick a pace: 1 lb a week is a good default.", "Read your daily calorie target and your estimated goal date."],
 how="""<p>First the calculator estimates your total daily energy expenditure (TDEE) from the Mifflin-St Jeor equation and your activity level. A pound of body fat stores roughly 3,500 calories, so a 500-calorie daily deficit adds up to about a pound a week. The target is your TDEE minus that deficit.</p>
<p>The CDC suggests losing 1 to 2 pounds a week for weight loss that lasts. The calculator won't set a target below 1,200 calories a day for women or 1,500 for men, because it gets hard to eat enough protein, vitamins and minerals below that without medical supervision. As you lose weight your TDEE falls, so recalculate every 10 pounds or so; the 3,500-calorie rule also tends to overestimate long-term loss.</p>""",
 formula="TDEE = BMR (Mifflin-St Jeor) × activity factor\nDaily deficit = pounds per week × 3,500 ÷ 7\nTarget calories = TDEE − deficit",
 example=f"<p>A 35-year-old woman, 5 ft 5 in and 180 lb, who exercises lightly has a TDEE of about <strong>{round(ex_t, -1):,.0f} calories</strong>. To lose 1 lb a week she'd eat about <strong>{round(ex_t - 500, -1):,.0f} calories a day</strong>. Losing 20 lb at that pace takes about 20 weeks.</p>",
 extra="<h3>Daily deficit by pace</h3>" + tbl(["Pace", "Daily deficit", "Weekly deficit", "Time to lose 10 lb"],
   [(f"{p} lb/week", f"{p * 500:,.0f} cal", f"{p * 3500:,.0f} cal", f"{10 / p:g} weeks") for p in (0.5, 1, 1.5, 2)]) +
 "<h3>Ways to create a 500-calorie deficit</h3><ul><li>Swap two sugary drinks for water or diet drinks (about 280 calories).</li><li>Take a brisk 45-minute walk (about 200 calories for a 160 lb person).</li><li>Fill half your plate with vegetables instead of rice or pasta at dinner.</li><li>Have a high-protein breakfast; protein keeps you full for longer.</li></ul>",
 faqs=[("How many calories should I eat to lose weight?", "About 500 below your maintenance calories to lose roughly 1 lb a week. For many women that's 1,400–1,800 a day and for many men 1,800–2,300, but it depends on your size and activity."),
       ("Is a 1,000-calorie deficit safe?", "It aims for about 2 lb a week, the top of the range the CDC suggests. It can work for people with a lot to lose, but it shouldn't take you below about 1,200 (women) or 1,500 (men) calories a day without medical advice."),
       ("Why have I stopped losing weight?", "As you lose weight you burn fewer calories, so the same intake becomes maintenance. Water retention can also hide fat loss for a week or two. Recalculate with your new weight."),
       ("Do I need to count calories forever?", "No. Many people count for a few months to learn portion sizes, then switch to habits like regular meals, more vegetables and weekly weigh-ins.")],
 related=["tdee", "calorie", "macro", "bmi"])

# ---------- BAC ----------
def bacv(drinks, lb, sex, hrs): return max(0, drinks * 14 / (lb * 453.592 * (0.68 if sex == "m" else 0.55)) * 100 - 0.015 * hrs)
tool(id="bac", slug="bac-calculator", cat="Health", name="BAC Calculator",
 short="BAC calculator", desc="Estimated blood alcohol content and time to sober up.",
 title="BAC Calculator – Blood Alcohol Content Estimate | Numbrik",
 meta="Estimate your blood alcohol content (BAC) from your drinks, weight and time with the Widmark formula, and how long until you're back to 0.00%. Never use it to decide to drive.",
 lede="Estimate your blood alcohol content (BAC) from what you've had to drink, your weight and how long you've been drinking, plus roughly how long until it's back to zero. It's a learning tool: never use it to decide whether you can drive.",
 steps=["Choose your sex and enter your body weight.", "Enter how many beers, glasses of wine and shots you've had.", "Enter the hours since your first drink.", "Read your estimated BAC and the time until it reaches 0.00%."],
 how="""<p>The calculator uses the Widmark formula. It converts your drinks to grams of alcohol (a US standard drink holds 14 g), divides by your body weight times a body-water constant (about 0.68 for men and 0.55 for women), and subtracts the alcohol your liver has cleared: on average about 0.015% BAC per hour. Coffee, cold showers and sleep don't speed that up.</p>
<p>Real BAC can be much higher than the estimate. Strong craft beers, large wine pours and mixed drinks often hold two or more standard drinks, and drinking on an empty stomach, medication, fatigue and health conditions all raise it. The only safe plan is not to drive after drinking.</p>""",
 formula="Alcohol (g) = standard drinks × 14\nBAC % = alcohol ÷ (body weight in g × r) × 100 − 0.015 × hours\nr ≈ 0.68 (men), 0.55 (women)",
 example=f"<p>A 170 lb man has three beers over two hours: 42 g of alcohol ÷ (77,111 g × 0.68) × 100 = 0.080%, minus 0.03% for two hours = about <strong>{bacv(3, 170, 'm', 2):.3f}%</strong>. A 140 lb woman drinking the same would be at about <strong>{bacv(3, 140, 'f', 2):.3f}%</strong>, over the 0.08% limit.</p>",
 extra="<h3>Estimated BAC one hour after drinking (men)</h3>" + tbl(["Drinks"] + [f"{w} lb" for w in (120, 140, 160, 180, 200, 240)],
   [[str(d)] + [f"{bacv(d, w, 'm', 1):.3f}%" for w in (120, 140, 160, 180, 200, 240)] for d in range(1, 7)]) +
 "<h3>Estimated BAC one hour after drinking (women)</h3>" + tbl(["Drinks"] + [f"{w} lb" for w in (100, 120, 140, 160, 180, 200)],
   [[str(d)] + [f"{bacv(d, w, 'f', 1):.3f}%" for w in (100, 120, 140, 160, 180, 200)] for d in range(1, 7)]) +
 "<h3>What counts as one standard drink (US)</h3>" + tbl(["Drink", "Size", "Alcohol"], [("Beer", "12 oz", "About 5%"), ("Malt liquor", "8–9 oz", "About 7%"), ("Wine", "5 oz", "About 12%"), ("Spirits (vodka, whiskey, rum)", "1.5 oz shot", "About 40%")]) +
 "<p><strong>Alcohol poisoning is an emergency.</strong> If someone is confused, vomiting while drowsy, breathing slowly or irregularly, has blue-tinged or pale skin, or can't be woken, call 911. Don't leave them to sleep it off.</p>",
 faqs=[("What is the legal BAC limit for driving?", "0.08% in every US state except Utah, where it's 0.05%. Commercial drivers are limited to 0.04%, and drivers under 21 face zero-tolerance limits of 0.00–0.02%."),
       ("How long does it take to get alcohol out of your system?", "BAC falls by about 0.015% an hour, so 0.08% takes over five hours to reach zero. Nothing speeds it up: not coffee, water, food after the fact or a cold shower."),
       ("How many drinks gets you to 0.08%?", "For many men around 170 lb it's three to four drinks in an hour or two; for many women around 140 lb it's two to three. It varies a lot, which is why no number of drinks is safe for driving."),
       ("Is this calculator accurate?", "It gives a rough average. Your real BAC depends on food, drink strength, medication, health and genetics. Only a breath or blood test measures it.")],
 related=["water", "calorie", "bmi", "sleep"])

# ---------- Bra size ----------
USC = ['AA', 'A', 'B', 'C', 'D', 'DD', 'DDD', 'G', 'H', 'I', 'J', 'K']; UKC = ['AA', 'A', 'B', 'C', 'D', 'DD', 'E', 'F', 'FF', 'G', 'GG', 'H']; EUC = ['AA', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
tool(id="bra", slug="bra-size-calculator", cat="Converters", name="Bra Size Calculator",
 short="Bra size calculator", desc="Band and cup size from two measurements.",
 title="Bra Size Calculator – Find Your Band & Cup Size | Numbrik",
 meta="Find your bra size from two measurements, in US, UK and EU sizes, plus sister sizes. Includes a step-by-step measuring guide and a bra size chart.",
 lede="Measure your underbust and bust with a soft tape, enter the numbers, and get your bra size in US, UK and EU sizing, plus sister sizes to try if the first doesn't fit perfectly.",
 steps=["Measure your underbust: wrap the tape snugly around your ribcage, right under your bust.", "Measure your bust: wrap the tape loosely around the fullest part, keeping it level.", "Enter both measurements.", "Read your size, and try sister sizes if the band or cups don't feel right."],
 how="""<p>Your band size is your underbust measurement rounded to the nearest even number of inches. Your cup size is the difference between your bust and your band: each inch is one cup size, so 1 inch is an A, 2 inches a B, 3 a C, 4 a D and 5 a DD. This is the modern method most fitters now use. The older “add 4 inches to the band” method gives bands that are often too loose.</p>
<p>Sister sizes hold the same cup volume on a different band: go down a band and up a cup (34C → 32D), or up a band and down a cup (34C → 36B). A good fit means the band sits level and does most of the support, the centre gore lies flat against your breastbone, and the cups don't gape or spill over.</p>""",
 formula="Band = underbust (in), rounded to the nearest even number\nCup = bust − band (1 in = A, 2 = B, 3 = C, 4 = D, 5 = DD…)\nEU band = 70 + (US band − 32) ÷ 2 × 5",
 example="<p>Underbust <strong>31.5 in</strong> rounds to a 32 band. Bust <strong>36 in</strong>: 36 − 32 = 4 inches = D cup. Your size is <strong>32D</strong> (UK 32D, EU 70D). Sister sizes: 30DD and 34C.</p>",
 extra="<h3>Cup size chart</h3>" + tbl(["Bust − band", "US", "UK", "EU"], [(f"{i} in" if i else "Under 1 in", USC[i], UKC[i], EUC[i]) for i in range(12)]) +
 "<h3>Band size conversion</h3>" + tbl(["US / UK band", "EU / Intl band", "FR / ES band", "AU band"], [(b, 70 + (b - 32) // 2 * 5, 85 + (b - 32) // 2 * 5, 10 + (b - 32)) for b in range(28, 46, 2)]),
 faqs=[("How do I measure my bra size at home?", "Use a soft tape measure. Measure snugly around your ribcage just under your bust, then loosely around the fullest part of your bust. Keep the tape level and breathe normally."),
       ("What are sister sizes?", "Sizes with the same cup volume on a different band. If 34C is tight in the band, try 36B; if it's loose, try 32D."),
       ("Is a D cup the same in every brand?", "No. Cups get bigger as the band grows, so a 38D holds more than a 32D, and brands and countries size differently. UK sizes use DD, E, F, FF; US brands often use DDD or G instead."),
       ("How often should I measure?", "Every six months to a year, and after weight changes, pregnancy or breastfeeding. Many people wear the wrong size because their body changed.")],
 related=["shoe", "convert", "bmi", "bodyfat"])

# ---------- Numerology ----------
def red(n, keep=True):
    while n > 9 and not (keep and n in (11, 22, 33)): n = sum(int(c) for c in str(n))
    return n
def lp(d): return red(red(d.month) + red(d.day) + red(d.year))
tool(id="numerology", slug="life-path-number-calculator", cat="Fun", name="Life Path Number Calculator",
 short="Life path number", desc="Your numerology life path and birthday numbers.",
 title="Life Path Number Calculator – Free Numerology | Numbrik",
 meta="Calculate your numerology life path number from your date of birth, with the working shown, master numbers 11, 22 and 33, plus your expression and soul urge numbers.",
 lede="Find your life path number, the best-known number in numerology, from your date of birth. Add your full birth name to get your expression (destiny) and soul urge numbers too. It's just for fun.",
 steps=["Enter your date of birth.", "Optional: enter your full name as it appears on your birth certificate.", "Read your life path number, what it's said to mean, and how it was worked out."],
 how="""<p>In Pythagorean numerology, your life path number comes from your birth date. Reduce the month, the day and the year separately to a single digit by adding their digits, then add the three results and reduce again. 11, 22 and 33 are “master numbers” and are not reduced further.</p>
<p>The expression number uses every letter of your birth name, with A = 1, B = 2 … I = 9, then J = 1 again, and the soul urge number uses only the vowels. Numerology has no scientific basis: enjoy it as a tradition and a conversation starter, not as advice.</p>""",
 formula="Reduce month, day and year to one digit each\nLife path = reduce(month + day + year)\nKeep 11, 22 and 33 as master numbers",
 example=f"<p>Born <strong>July 23, 1990</strong>: month 7 → 7; day 23 → 2 + 3 = 5; year 1990 → 1 + 9 + 9 + 0 = 19 → 1 + 9 = 10 → 1. Then 7 + 5 + 1 = 13 → 1 + 3 = <strong>{lp(date(1990, 7, 23))}</strong>.</p>",
 extra="<h3>Life path number meanings</h3>" + tbl(["Number", "Nickname", "Traits"], [("1", "The Leader", "Independent, driven, original"), ("2", "The Peacemaker", "Diplomatic, patient, caring"), ("3", "The Communicator", "Creative, expressive, social"), ("4", "The Builder", "Practical, loyal, hard-working"), ("5", "The Adventurer", "Curious, restless, freedom-loving"), ("6", "The Nurturer", "Responsible, warm, protective"), ("7", "The Seeker", "Thoughtful, analytical, spiritual"), ("8", "The Achiever", "Ambitious, confident, business-minded"), ("9", "The Humanitarian", "Generous, idealistic, compassionate"), ("11", "The Intuitive", "Inspired, sensitive, visionary"), ("22", "The Master Builder", "Turns big dreams into reality"), ("33", "The Master Teacher", "Devoted to helping others")]) +
 "<h3>Letter values</h3>" + tbl(["1", "2", "3", "4", "5", "6", "7", "8", "9"], [list("ABCDEFGHI"), list("JKLMNOPQR"), list("STUVWXYZ") + [""]]),
 faqs=[("How do I calculate my life path number?", "Reduce your birth month, day and year to single digits, add them, and reduce the total to one digit. Keep 11, 22 or 33 if you land on them."),
       ("What is a master number?", "11, 22 and 33 are treated as special in numerology and aren't added together into 2, 4 or 6."),
       ("Why do other sites give me a different number?", "Some add all the digits of the date in one go instead of reducing month, day and year first. That can skip a master number, so results sometimes differ."),
       ("Is numerology real?", "There's no scientific evidence that numbers shape personality or fate. Treat it as entertainment.")],
 related=["love", "age", "halfbday", "random"])

# ---------- Loan ----------
def pmt(P, apr, n): r = apr / 1200; return P * r / (1 - (1 + r) ** -n) if r else P / n
tool(id="gloan", slug="loan-calculator", cat="Money", name="Loan Calculator",
 short="Loan calculator", desc="Monthly payment, total interest and payoff schedule.",
 title="Loan Calculator – Monthly Payment & Interest | Numbrik",
 meta="Calculate the monthly payment, total interest and payoff schedule for a personal loan or any fixed-rate loan, and see how much extra payments save.",
 lede="Work out the monthly payment on a personal loan, debt consolidation loan or any fixed-rate loan. Enter the amount, APR and term to get the payment, the total interest, a year-by-year schedule, and how much you'd save by paying extra.",
 steps=["Enter the amount you want to borrow.", "Enter the interest rate (APR) you've been offered.", "Enter the term in years or months.", "Optional: add an extra monthly payment to see how much sooner you'd be debt-free."],
 how="""<p>Fixed-rate loans are repaid in equal monthly payments. Early on, most of each payment covers interest; later, most goes to the balance. The payment comes from the standard amortization formula, using the monthly rate (APR ÷ 12) and the number of payments.</p>
<p>Any extra payment goes straight to the principal, which cuts the interest charged in every later month, so even small extras shorten the loan. Check that your lender doesn't charge a prepayment penalty first. APR includes most fees, so compare offers by APR rather than the headline rate.</p>""",
 formula="Payment = P × r ÷ (1 − (1 + r)^−n)\nr = APR ÷ 12 ÷ 100,  n = number of monthly payments\nTotal interest = payment × n − P",
 example=f"<p>A <strong>$20,000</strong> loan at <strong>9.5% APR</strong> over <strong>5 years</strong> (60 payments) costs <strong>${pmt(20000, 9.5, 60):,.2f} a month</strong>. You'd pay ${pmt(20000, 9.5, 60) * 60 - 20000:,.0f} in interest, ${pmt(20000, 9.5, 60) * 60:,.0f} in total.</p>",
 extra="<h3>Monthly payment per $10,000 borrowed</h3>" + tbl(["APR", "2 years", "3 years", "4 years", "5 years", "7 years"],
   [[f"{a}%"] + [f"${pmt(10000, a, y * 12):,.2f}" for y in (2, 3, 4, 5, 7)] for a in (5, 7, 9, 11, 13, 15, 18, 22, 25)]) +
 "<h3>Total interest on $10,000</h3>" + tbl(["APR", "3 years", "5 years", "7 years"],
   [[f"{a}%"] + [f"${pmt(10000, a, y * 12) * y * 12 - 10000:,.0f}" for y in (3, 5, 7)] for a in (6, 10, 15, 20, 25)]),
 faqs=[("How is a loan payment calculated?", "With the amortization formula: payment = P × r ÷ (1 − (1 + r)^−n), where P is the amount, r the monthly rate and n the number of payments."),
       ("Is a longer loan term better?", "It lowers the monthly payment but raises the total interest. $10,000 at 10% costs about $2,748 in interest over 5 years, but $3,945 over 7."),
       ("What's a good APR for a personal loan?", "It depends on your credit score. Borrowers with excellent credit may be offered single-digit rates, while fair or poor credit can mean 20% or more. Compare several prequalified offers."),
       ("Do extra payments really help?", "Yes. Each extra dollar reduces the balance that's charged interest. On a $20,000, 5-year loan at 9.5%, an extra $100 a month pays it off about 13 months sooner.")],
 related=["loan", "autoloan", "simpleint", "compound"])

# ---------- Date ----------
def addm(d, m):
    t = d.month - 1 + m; y = d.year + t // 12; mo = t % 12 + 1
    return date(y, mo, min(d.day, calendar.monthrange(y, mo)[1]))
D0 = date(2026, 11, 8)
tool(id="datecalc", slug="date-calculator", cat="Dates & time", name="Date Calculator",
 short="Date calculator", desc="Add or subtract days, weeks, months or years from a date.",
 title="Date Calculator – Add or Subtract Days | Numbrik",
 meta="Add or subtract days, weeks, months and years from any date. Find the date 30, 60 or 90 days from a date, the day of the week, and weekdays in between.",
 lede="Add days, weeks, months or years to a date, or subtract them, and get the exact date and day of the week. Use it for deadlines, notice periods, contract dates, warranties and “90 days from” questions.",
 steps=["Pick the start date.", "Choose add or subtract.", "Enter any mix of years, months, weeks and days.", "Read the resulting date, the day of the week and the weekdays in between."],
 how="""<p>Years and months are added first as calendar units, then weeks and days. Adding a month keeps the same day of the month; if that day doesn't exist, the result moves to the last day of the month, so January 31 plus one month is February 28 (or 29 in a leap year). Days are counted as calendar days, including weekends.</p>
<p>For legal and contract deadlines, check whether the first day counts and what happens when the deadline lands on a weekend or holiday: many rules move it to the next business day. The weekday count shows Monday-to-Friday days but doesn't remove public holidays.</p>""",
 formula="Result = start date + years + months (calendar) + weeks × 7 + days\nIf the day doesn't exist in the new month, use the month's last day",
 example=f"<p>From <strong>November 8, 2026</strong>, adding 90 days gives <strong>{(D0 + timedelta(90)).strftime('%A, %B %-d, %Y')}</strong>. Adding 3 months instead gives {addm(D0, 3).strftime('%A, %B %-d, %Y')}, because months have different lengths.</p>",
 extra="<h3>Days from November 8, 2026</h3>" + tbl(["Add", "Date", "Day"], [(f"{n} days", (D0 + timedelta(n)).strftime("%B %-d, %Y"), (D0 + timedelta(n)).strftime("%A")) for n in (7, 10, 14, 30, 45, 60, 90, 100, 120, 180, 365)]) +
 "<h3>Months from November 8, 2026</h3>" + tbl(["Add", "Date", "Day"], [(f"{n} months", addm(D0, n).strftime("%B %-d, %Y"), addm(D0, n).strftime("%A")) for n in (1, 2, 3, 6, 9, 12, 18, 24)]),
 faqs=[("How do I add days to a date?", "Enter the start date and the number of days. The calculator counts forward calendar days, including weekends, and shows the date and day of the week."),
       ("Is 3 months the same as 90 days?", "Not quite. Three calendar months is 89 to 92 days depending on the months. From November 8, 2026, 90 days is February 6, 2027, but 3 months is February 8, 2027."),
       ("What is January 31 plus one month?", "February 28, or February 29 in a leap year. When the day doesn't exist, the result moves to the end of the month."),
       ("How do I count only business days?", "The result shows the weekdays (Monday to Friday) in between. To skip public holidays too, use the working days calculator.")],
 related=["days", "workdays", "age", "halfbday"])

BYID.update({t["id"]: t for t in T})
