"""Calculators added after the calculator.net gap analysis (October 31, 2026), plus upgrades to mortgage and GPA pages."""
import math
from datetime import date, timedelta
from content import tool, T, BYID, ORDER

if "Math" not in ORDER:
    ORDER.insert(ORDER.index("Students") + 1, "Math")

def bf(m, h, n, a, hp=0):
    return 86.010 * math.log10(a - n) - 70.041 * math.log10(h) + 36.76 if m else 163.205 * math.log10(a + hp - n) - 97.684 * math.log10(h) - 78.387
bf_m = bf(1, 69, 15.5, 34); bf_f = bf(0, 64, 13, 30, 40)
b = 10000.0
for _ in range(120): b = b * (1 + 0.07 / 12) + 200
ci_bal = b
ci_rows = ""
for P, r in [(10000, 5), (10000, 7), (10000, 10)]:
    vals = [P * (1 + r / 100) ** y for y in (10, 20, 30)]
    ci_rows += f"<tr><td>{r}%</td>" + "".join(f"<td>${x:,.0f}</td>" for x in vals) + "</tr>"
lmp = date(2026, 1, 1); due = lmp + timedelta(280)
def fmtd(d): return f"{d:%B} {d.day}, {d.year}"

tool(id="scientific", slug="scientific-calculator", cat="Math", name="Scientific Calculator",
 short="Scientific calculator", desc="An online calculator with trig, logs, powers and roots.",
 title="Scientific Calculator – Free Online Calculator | Numbrik",
 meta="Free online scientific calculator with sin, cos, tan, logs, powers, roots, factorials and memory of recent answers. Works with your keyboard and on phones.",
 lede="A free online calculator for everyday sums and scientific maths: trigonometry in degrees or radians, logarithms, powers, roots, percentages and factorials. Type on your keyboard or tap the keys.",
 steps=["Tap the keys or type with your keyboard. The answer previews as you type.",
        "Press = or Enter to finish. The last five answers appear in the result panel.",
        "Use Ans to reuse the previous answer, and switch between degrees and radians for sin, cos and tan."],
 how="""<p>The calculator follows the standard order of operations: brackets first, then powers and roots, then multiplication and division, then addition and subtraction. So 2 + 3 × 4 is 14, not 20. Multiplication can be implied, so 2π and 3(4 + 1) work as you would write them.</p>
<p>Trigonometry uses degrees by default, the usual choice for school geometry. Switch to radians for calculus and physics. A minus sign written before a power applies after it, so −3² is −9, while (−3)² is 9. Brackets you forget to close are closed for you.</p>""",
 formula="Order of operations: ( )  →  ^ √ !  →  × ÷  →  + −\nx% = x ÷ 100        EXP: 3E5 = 3 × 10⁵\nlog = base 10        ln = base e (2.71828…)",
 example="<p>sin(30) in degrees is <strong>0.5</strong>. 2^10 is <strong>1024</strong>, √(144) is 12, 5! is 120 and log(1000) is 3. To find 15% of 80, type 80 × 15% to get 12.</p>",
 extra="""<h3>Key guide</h3><div class="tbl"><table><thead><tr><th>Key</th><th>What it does</th><th>Example</th></tr></thead><tbody>
<tr><td>x²</td><td>Square</td><td>7² = 49</td></tr><tr><td>xʸ</td><td>Power</td><td>2^8 = 256</td></tr><tr><td>√</td><td>Square root</td><td>√(81) = 9</td></tr>
<tr><td>n!</td><td>Factorial</td><td>6! = 720</td></tr><tr><td>EXP</td><td>Times ten to the power</td><td>4E3 = 4,000</td></tr><tr><td>ln, log</td><td>Natural and base-10 logarithm</td><td>ln(e) = 1</td></tr>
<tr><td>Ans</td><td>Last answer</td><td>Ans × 2</td></tr></tbody></table></div>""",
 faqs=[("Does it use the right order of operations?", "Yes. Brackets come first, then powers and roots, then multiplication and division, then addition and subtraction, so 2 + 3 × 4 = 14."),
       ("How do I switch between degrees and radians?", "Use the Degrees and Radians buttons above the keypad. The choice applies to sin, cos and tan."),
       ("Can I use my keyboard?", "Yes. Type numbers and + − * / ^ ( ) %, press Enter for equals, Backspace to delete and Esc to clear."),
       ("Why does it say Error?", "The expression can't be worked out, for example dividing by zero, the square root of a negative number, or an unfinished expression such as 5 ×.")],
 related=["fraction", "percent", "stdev", "lcm"])

tool(id="fraction", slug="fraction-calculator", cat="Math", name="Fraction Calculator",
 short="Fraction calculator", desc="Add, subtract, multiply and divide fractions and mixed numbers.",
 title="Fraction Calculator with Steps & Mixed Numbers | Numbrik",
 meta="Add, subtract, multiply and divide fractions and mixed numbers. Shows the working, the simplified answer, the mixed number and the decimal.",
 lede="Add, subtract, multiply or divide two fractions or mixed numbers. The answer is simplified and shown as a fraction, a mixed number, a decimal and a percent, with the working.",
 steps=["Enter the first fraction. For a mixed number such as 1 ¾, put 1 in the small left box.",
        "Choose +, −, × or ÷.", "Enter the second fraction and read the answer and the working underneath."],
 how="""<p>To add or subtract, the fractions need a common denominator. The calculator uses the least common multiple of the two denominators, rewrites both fractions over it, then adds or subtracts the tops. To multiply, multiply the tops together and the bottoms together. To divide, flip the second fraction and multiply.</p>
<p>Every answer is reduced to lowest terms by dividing the top and bottom by their greatest common factor. Mixed numbers are converted to improper fractions first, so 1 ¾ becomes 7/4.</p>""",
 formula="a/b + c/d = (a×d + c×b) ÷ (b×d)\na/b × c/d = (a×c) ÷ (b×d)\na/b ÷ c/d = a/b × d/c",
 example="<p>3/4 + 5/6: the common denominator is 12, so it becomes 9/12 + 10/12 = <strong>19/12</strong>, which is <strong>1 7/12</strong> or 1.583333.</p>",
 extra="", faqs=[("How do I simplify a fraction?", "Divide the top and bottom by their greatest common factor. 18/24 has a GCF of 6, so it simplifies to 3/4."),
       ("How do I turn a mixed number into a fraction?", "Multiply the whole number by the denominator and add the numerator. 2 ⅓ is (2 × 3 + 1)/3 = 7/3."),
       ("How do I convert a fraction to a decimal?", "Divide the top by the bottom. 3/8 = 3 ÷ 8 = 0.375."),
       ("Can I use negative fractions?", "Yes. Put a minus sign on the whole number or the numerator.")],
 related=["lcm", "gcf", "scientific", "percent"])

tool(id="stdev", slug="standard-deviation-calculator", cat="Math", name="Standard Deviation Calculator",
 short="Standard deviation", desc="Standard deviation, variance, mean and median of a data set.",
 title="Standard Deviation Calculator & Variance | Numbrik",
 meta="Find the sample and population standard deviation, variance, mean, median and range of a list of numbers. Paste data separated by commas or spaces.",
 lede="Paste or type a list of numbers to get the sample and population standard deviation, the variance, mean, median, range and count.",
 steps=["Type or paste your numbers, separated by commas, spaces or new lines.", "Read the sample standard deviation and the other statistics.",
        "Use the population figures only when your list contains every value in the group."],
 how="""<p>Standard deviation measures how spread out the values are around the mean. The calculator finds the mean, subtracts it from each value, squares the differences, adds them up and divides. Taking the square root of that variance gives the standard deviation.</p>
<p>For a sample, the sum is divided by n − 1 rather than n. This correction, called Bessel's correction, makes the sample a better estimate of the whole population's spread. With large data sets the two results are very close.</p>""",
 formula="Mean  x̄ = Σx ÷ n\nPopulation SD  σ = √( Σ(x − x̄)² ÷ n )\nSample SD  s = √( Σ(x − x̄)² ÷ (n − 1) )",
 example="<p>For 10, 12, 23, 23, 16, 23, 21, 16 the mean is 18 and the squared differences add up to 192. The population standard deviation is √(192 ÷ 8) = <strong>4.899</strong> and the sample standard deviation is √(192 ÷ 7) = <strong>5.237</strong>.</p>",
 extra="", faqs=[("Should I use sample or population standard deviation?", "Use the sample version when your data is part of a bigger group, such as 30 students surveyed out of a whole school. Use population when you have every value."),
       ("What does a high standard deviation mean?", "The values are spread far from the mean. A low standard deviation means most values sit close to the average."),
       ("What is variance?", "Variance is the standard deviation squared. It is used in many formulas, but the standard deviation is easier to read because it uses the same units as the data."),
       ("How many numbers can I enter?", "As many as you like. The calculation runs in your browser.")],
 related=["percent", "scientific", "grade", "random"])

tool(id="compound", slug="compound-interest-calculator", cat="Money", name="Compound Interest Calculator",
 short="Compound interest", desc="How savings grow with compound interest and monthly deposits.",
 title="Compound Interest Calculator with Monthly Deposits | Numbrik",
 meta="See how savings grow with compound interest and monthly deposits. Choose yearly, quarterly, monthly or daily compounding and see a year-by-year table.",
 lede="See how a starting amount and regular monthly deposits grow with compound interest, with a year-by-year table of deposits, interest and balance.",
 steps=["Enter your starting amount and how much you'll add each month.", "Enter the yearly interest rate, the number of years and how often interest compounds.",
        "Read the final balance and check the table to see how interest takes over in later years."],
 how="""<p>With compound interest you earn interest on your interest. Each period the interest is added to the balance, so the next period's interest is a little larger. The calculator converts the yearly rate into a monthly rate for the chosen compounding, then adds each month's interest and deposit.</p>
<p>More frequent compounding earns slightly more. A 7% rate compounded monthly is an effective 7.23% a year. Real investments go up and down, so treat a fixed rate as a planning estimate. Taxes, fees and inflation are not included.</p>""",
 formula="Without deposits:  A = P × (1 + r/k)^(k×t)\nP = starting amount, r = yearly rate, k = compounding periods per year, t = years",
 example=f"<p>$10,000 at 7% compounded monthly, plus $200 a month for 10 years, grows to about <strong>${ci_bal:,.0f}</strong>. You put in $34,000, so about ${ci_bal-34000:,.0f} is interest.</p>",
 extra=f"""<h3>$10,000 with no deposits, compounded yearly</h3><div class="tbl"><table><thead><tr><th>Rate</th><th>10 years</th><th>20 years</th><th>30 years</th></tr></thead><tbody>{ci_rows}</tbody></table></div>
<p>The rule of 72 gives a quick estimate: divide 72 by the interest rate to find roughly how many years it takes money to double. At 8%, that's about 9 years.</p>""",
 faqs=[("What is the difference between simple and compound interest?", "Simple interest is paid only on the original amount. Compound interest is also paid on interest already earned, so the balance grows faster each year."),
       ("Does monthly compounding make a big difference?", "A little. At 7%, monthly compounding gives an effective 7.23% a year instead of 7%."),
       ("How long does it take to double my money?", "Use the rule of 72: divide 72 by the yearly rate. At 6% it takes about 12 years."),
       ("Are taxes included?", "No. Interest in a taxable account may be taxed each year, which lowers the final balance.")],
 related=["loan", "salary", "percent", "paycheck"])

tool(id="salestax", slug="sales-tax-calculator", cat="Money", name="Sales Tax Calculator",
 short="Sales tax / VAT", desc="Add or remove sales tax, VAT or GST from a price.",
 title="Sales Tax Calculator – Add or Remove Tax, VAT, GST | Numbrik",
 meta="Add sales tax to a price or work out the price before tax from a total. Works for US sales tax, UK VAT, Canadian GST and HST, and Australian GST.",
 lede="Add sales tax to a price, or remove it from a total to find the price before tax. Works for US sales tax, UK and Dutch VAT, Canadian GST and HST, and Australian GST.",
 steps=["Choose whether you're adding tax to a price or removing it from a total.", "Enter the amount and the tax rate. The rate starts at a typical value for your region.",
        "Read the total, the tax and the price before tax."],
 how="""<p>To add tax, multiply the price by the rate and add it on. To remove tax from a total, divide by 1 plus the rate. Subtracting the percentage from the total gives the wrong answer: removing 20% VAT from £120 gives £100, not £96.</p>
<p>In the US there is no national sales tax. States, counties and cities set their own rates, so the combined rate depends on where you buy. In Canada, some provinces charge GST plus a provincial sales tax, and others charge a single HST.</p>""",
 formula="Total = price × (1 + rate)\nPrice before tax = total ÷ (1 + rate)\nTax = total − price before tax",
 example="<p>A $100 item with 7% sales tax costs <strong>$107</strong>. Going the other way, a £120 total with 20% VAT has a price before tax of <strong>£100</strong> and £20 of VAT.</p>",
 extra="""<h3>Standard rates</h3><div class="tbl"><table><thead><tr><th>Country</th><th>Tax</th><th>Standard rate</th></tr></thead><tbody>
<tr><td>United Kingdom</td><td>VAT</td><td>20%</td></tr><tr><td>Netherlands</td><td>BTW (VAT)</td><td>21%</td></tr><tr><td>Australia</td><td>GST</td><td>10%</td></tr>
<tr><td>Canada</td><td>GST / HST</td><td>5% GST, or 13–15% HST in some provinces</td></tr><tr><td>United States</td><td>Sales tax</td><td>Set by each state and city</td></tr></tbody></table></div>
<p>Reduced rates apply to some goods, such as food and children's clothing, so check the rate for what you're buying.</p>""",
 faqs=[("How do I calculate sales tax?", "Multiply the price by the tax rate. 8% tax on $50 is $50 × 0.08 = $4, so you pay $54."),
       ("How do I work out the price before tax?", "Divide the total by 1 plus the rate. $54 ÷ 1.08 = $50."),
       ("Why can't I just subtract the percentage?", "Because the tax was worked out on the smaller, pre-tax price. Subtracting 20% from a total that includes 20% VAT takes off too much."),
       ("Is sales tax the same as VAT?", "Both are taxes on purchases. Sales tax is added at the till in the US, while VAT and GST are usually included in the shelf price.")],
 related=["percent", "tip", "autoloan", "compound"])

tool(id="duedate", slug="due-date-calculator", cat="Health", name="Due Date Calculator",
 short="Due date", desc="Estimated due date, how many weeks pregnant, and trimester dates.",
 title="Due Date Calculator – Pregnancy Weeks & Trimesters | Numbrik",
 meta="Estimate your due date from your last period, conception date or IVF transfer. See how many weeks pregnant you are and when each trimester ends.",
 lede="Estimate a baby's due date from the first day of your last period, the conception date or an IVF transfer date, and see how far along you are and when each trimester ends.",
 steps=["Choose what you know: your last period, the conception date or an IVF transfer date.", "Enter the date, and your usual cycle length or the embryo's age if asked.",
        "Read the due date, how many weeks pregnant you are today and the milestone dates."],
 how="""<p>Pregnancy is counted from the first day of the last menstrual period, about two weeks before conception. A full-term pregnancy is about 40 weeks, or 280 days, from that date. This is Naegele's rule, the standard first estimate. For cycles longer or shorter than 28 days, the calculator moves the date by the difference.</p>
<p>From a known conception date the due date is 266 days later. For IVF, it is 266 days from the egg retrieval, which is 263 days after a day-3 transfer or 261 days after a day-5 transfer. An early ultrasound is often more accurate, and only your doctor or midwife can confirm the date.</p>""",
 formula="From last period:  due date = first day of period + 280 days (+ cycle length − 28)\nFrom conception:  due date = conception + 266 days\nIVF day-5 transfer:  due date = transfer + 261 days",
 example=f"<p>If the first day of your last period was {fmtd(lmp)} and your cycle is 28 days, the estimated due date is <strong>{fmtd(due)}</strong>. The first trimester ends on {fmtd(lmp + timedelta(97))} and the second on {fmtd(lmp + timedelta(195))}.</p>",
 extra="", faqs=[("How accurate is a due date?", "It's an estimate. Only a small share of babies arrive on the exact day, and most are born within two weeks either side. An early ultrasound can adjust the date."),
       ("Why is pregnancy counted from my last period?", "Because the date of the last period is usually known and conception isn't. That's why you are considered about two weeks pregnant at conception."),
       ("What are the trimesters?", "The first trimester runs to the end of week 13, the second to the end of week 27, and the third until birth."),
       ("Is this medical advice?", "No. It's a general estimate. Talk to your doctor or midwife about your own pregnancy.")],
 related=["days", "age", "calorie", "bmi"])

tool(id="bodyfat", slug="body-fat-calculator", cat="Health", name="Body Fat Calculator",
 short="Body fat", desc="Body fat percentage with the US Navy tape method.",
 title="Body Fat Calculator – US Navy Method | Numbrik",
 meta="Estimate your body fat percentage with a tape measure using the US Navy method. Enter height, neck, waist and hips in inches or centimetres.",
 lede="Estimate your body fat percentage with a tape measure, using the US Navy method, and see your fat and lean mass and how the result compares with common ranges.",
 steps=["Choose units and sex.", "Measure your neck, waist and, for women, hips. Enter them with your height and weight.",
        "Read your body fat percentage, its category and your fat and lean mass."],
 how="""<p>The US Navy method estimates body fat from body circumferences and height. It was developed so that body fat could be checked without special equipment, and it is usually within a few percentage points of lab methods for most people. Measure in the morning, keep the tape level and take the average of two or three readings.</p>
<p>The categories come from the American Council on Exercise (ACE). Body fat is a better guide to health than weight alone, but it is still an estimate. Very muscular or very lean people may get less accurate results.</p>""",
 formula="Men:    BF% = 86.010 × log₁₀(waist − neck) − 70.041 × log₁₀(height) + 36.76\nWomen:  BF% = 163.205 × log₁₀(waist + hip − neck) − 97.684 × log₁₀(height) − 78.387\n(all measurements in inches)",
 example=f"<p>A man 69 in tall with a 15.5 in neck and a 34 in waist has about <strong>{bf_m:.1f}%</strong> body fat, in the fitness range. A woman 64 in tall with a 13 in neck, 30 in waist and 40 in hips has about <strong>{bf_f:.1f}%</strong>, in the average range.</p>",
 extra="""<h3>Body fat categories (ACE)</h3><div class="tbl"><table><thead><tr><th>Category</th><th>Women</th><th>Men</th></tr></thead><tbody>
<tr><td>Essential fat</td><td>10–13%</td><td>2–5%</td></tr><tr><td>Athletes</td><td>14–20%</td><td>6–13%</td></tr><tr><td>Fitness</td><td>21–24%</td><td>14–17%</td></tr>
<tr><td>Average</td><td>25–31%</td><td>18–24%</td></tr><tr><td>Obese</td><td>32% and above</td><td>25% and above</td></tr></tbody></table></div>""",
 faqs=[("How accurate is the Navy method?", "For most adults it lands within a few percentage points of lab tests, but tape placement matters. Take two or three readings and average them."),
       ("Where do I measure my waist?", "Men measure at the navel. Women measure at the narrowest point, usually just above the navel."),
       ("What is a healthy body fat percentage?", "The ACE fitness and average ranges are 14–24% for men and 21–31% for women."),
       ("Is body fat better than BMI?", "It gives more detail because it separates fat from muscle. BMI is quicker but can't tell the two apart.")],
 related=["bmi", "calorie", "duedate", "sleep"])

tool(id="password", slug="password-generator", cat="Fun", name="Password Generator",
 short="Password generator", desc="Strong random passwords, made in your browser.",
 title="Password Generator – Strong Random Passwords | Numbrik",
 meta="Generate strong, random passwords in your browser. Choose the length and character types, avoid look-alike characters and see the strength in bits.",
 lede="Create strong, random passwords with your chosen length and character types. Passwords are made in your browser and are never sent anywhere.",
 steps=["Set the length. 16 characters or more is a good default.", "Choose uppercase, lowercase, numbers and symbols. Tick \"avoid look-alikes\" if you'll type it by hand.",
        "Copy the password, or press Generate new for a fresh set."],
 how="""<p>Each character is picked with your browser's cryptographic random number generator, the same source used to create encryption keys. The generator makes sure every character type you chose appears at least once, then shuffles the result.</p>
<p>Strength is measured in bits of entropy: the length multiplied by log₂ of the number of possible characters. Every extra bit doubles the number of guesses needed. Use a different password for every account, and a password manager to remember them.</p>""",
 formula="Entropy (bits) = length × log₂(number of possible characters)",
 example="<p>A 16-character password using uppercase, lowercase, numbers and 24 symbols draws from 86 characters, giving about <strong>103 bits</strong> of entropy. That rates as very strong.</p>",
 extra="""<h3>How strength is rated</h3><div class="tbl"><table><thead><tr><th>Entropy</th><th>Rating</th></tr></thead><tbody>
<tr><td>Under 40 bits</td><td>Weak</td></tr><tr><td>40–59 bits</td><td>Fair</td></tr><tr><td>60–79 bits</td><td>Strong</td></tr><tr><td>80 bits and above</td><td>Very strong</td></tr></tbody></table></div>""",
 faqs=[("Is it safe to generate passwords online here?", "The passwords are made inside your browser and are never sent over the internet or saved by Numbrik."),
       ("How long should a password be?", "At least 12 characters, and 16 or more for important accounts such as email and banking."),
       ("Should I use symbols?", "They help, but length matters more. A longer password with letters and numbers can be stronger than a short one with symbols."),
       ("What are look-alike characters?", "Characters that are easy to confuse, such as 0 and O or 1, l and I. Leaving them out makes a password easier to type.")],
 related=["random", "coin", "dice", "scientific"])

# ---- upgrades to existing pages ----
ln = BYID["loan"]
ln["title"] = "Mortgage Calculator with Taxes, Insurance & PMI | Numbrik"
ln["meta"] = "Mortgage calculator with property tax, insurance, PMI, HOA and extra payments. See your total monthly payment, payoff date and full amortization schedule."
ln["lede"] = "Find the monthly payment for a mortgage or any fixed-rate loan, with optional property tax, home insurance, PMI, HOA fees and extra payments. See the payoff date, the interest you'll pay and a yearly or monthly amortization schedule."
ln["steps"] = ["Enter the loan amount (the price minus your down payment), the interest rate and the term.",
               "Open \"Taxes, insurance and extra payments\" to add property tax, insurance, PMI, HOA fees or an extra monthly payment.",
               "Read the total monthly payment and payoff date, then switch the schedule between yearly and monthly."]
ln["faqs"] = [f for f in ln["faqs"] if not f[0].startswith("Does this include property tax")] + [
    ("Does this include property tax and insurance?", "Yes, if you add them. Open \"Taxes, insurance and extra payments\" and enter your yearly property tax and insurance, plus any monthly PMI and HOA fees."),
    ("How much do extra payments save?", "Extra payments go straight to principal. On a $350,000 loan at 6.5% for 30 years, an extra $200 a month saves tens of thousands in interest and pays the loan off years early. The calculator shows the exact amount.")]
gp = BYID["gpa"]
gp["steps"] = gp["steps"] + ["To plan ahead, enter a target GPA and the credits you'll take next to see the GPA you need in those classes."]
gp["faqs"] = gp["faqs"] + [("What GPA do I need to reach my goal?", "Enter your current GPA, credits earned, your target and the credits you'll take next. The calculator shows the GPA those new credits must average. For example, going from 3.0 over 60 credits to 3.2 with 30 more credits needs a 3.6.")]

BYID.update({t["id"]: t for t in T})
