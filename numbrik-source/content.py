"""Page content for every Numbrik calculator. Example numbers are computed here so the text always matches the tool."""
import math
from datetime import date, timedelta

def usd(x, d=2): return f"${x:,.{d}f}"
def pmt(P, annual, n):
    r = annual / 1200
    return P * r / (1 - (1 + r) ** -n) if r else P / n

# ---------- computed examples ----------
tc_days = [8, 8, 8.75, 8, 6.5, 4]; tc_total = sum(tc_days); tc_ot = tc_total - 40
tc_pay = 40 * 22.5 + tc_ot * 22.5 * 1.5
m350 = pmt(350000, 6.5, 360); m350_15 = pmt(350000, 6.5, 180)
car_tax = (34000 - 3000) * 0.07; car_P = 34000 - 4000 - 3000 + car_tax
car60 = pmt(car_P, 6.9, 60); car48 = pmt(car_P, 6.9, 48); car72 = pmt(car_P, 6.9, 72)
bmi_imp = 703 * 165 / 69 ** 2; bmi_met = 72 / 1.75 ** 2
kg = 150 * 0.45359237; cm = 66 * 2.54
bmr = 10 * kg + 6.25 * cm - 5 * 34 - 161; tdee = bmr * 1.375
gpa_pts = 3.7*3 + 3.3*4 + 4*3 + 3*1 + 3.7*3; gpa = gpa_pts / 14
cum = (3.40 * 45 + gpa_pts) / 59
d1, d2 = date(2026, 10, 20), date(2026, 12, 25)
ndays = (d2 - d1).days
wdays = sum(1 for i in range(1, ndays + 1) if (d1 + timedelta(i)).weekday() < 5)
def ymd(b, o):
    y = o.year - b.year; m = o.month - b.month; d = o.day - b.day
    if d < 0:
        m -= 1; d += (date(o.year, o.month, 1) - timedelta(1)).day
    if m < 0: y -= 1; m += 12
    return y, m, d
ay, am, ad = ymd(date(1994, 3, 17), date(2026, 10, 20))
adays = (date(2026, 10, 20) - date(1994, 3, 17)).days
two_d6 = {s: sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == s) for s in range(2, 13)}
f2c = lambda f: (f - 32) * 5 / 9

T = []
def tool(**k): T.append(k)

# ======================= WORK & PAY =======================
tool(id="timecard", slug="time-card-calculator", cat="Work & pay", name="Time Card Calculator",
 short="Time card", desc="Weekly hours, overtime and gross pay.",
 title="Time Card Calculator with Overtime & Pay | Numbrik",
 meta="Free weekly time card calculator. Enter start and end times and breaks to get total hours, overtime and gross pay. Works for US, Canada, Australia and UK.",
 lede="Enter start and end times for each day, take off unpaid breaks, and get total hours, overtime and gross pay for the week. Overtime rules follow the region you pick at the top of the page.",
 steps=["Type a start and end time for each day you worked. Leave days off empty.",
        "Enter the unpaid break for each shift in minutes, such as a 30-minute lunch.",
        "Add your hourly rate. The overtime threshold fills in for your region; change it if your contract is different.",
        "Read total hours, overtime and gross pay in the result panel. Your week stays saved in this browser for next time."],
 how="""<p>For each day the calculator subtracts the start time from the end time and then removes the break. If the end time is earlier than the start time, it treats the shift as overnight and adds 24 hours, so a 10:00 PM to 6:00 AM shift counts as 8 hours.</p>
<p>Hours above the weekly overtime threshold are paid at the overtime rate. In the United States the Fair Labor Standards Act sets that threshold at 40 hours in a workweek for non-exempt employees, paid at 1.5 times the regular rate. Some states add daily rules: California, for example, also pays overtime after 8 hours in a day. In Canada the threshold depends on the province, such as 44 hours a week in Ontario. Most Australian awards pay overtime after 38 ordinary hours. The UK and the Netherlands have no legal overtime premium, so it depends on your contract or collective agreement (CAO).</p>""",
 formula="Daily hours   = (end − start − break minutes) ÷ 60\nOvertime      = max(0, weekly hours − threshold)\nGross pay     = regular hours × rate + overtime × rate × multiplier",
 example=f"""<p>The calculator opens with an example week: five weekday shifts and a short Saturday, totalling <strong>{tc_total:g} hours</strong>. At {usd(22.5)} an hour with overtime after 40 hours at 1.5×, that is 40 regular hours ({usd(900)}) plus {tc_ot:g} overtime hours at {usd(33.75)} ({usd(tc_ot*33.75)}), for gross pay of <strong>{usd(tc_pay)}</strong>.</p>""",
 extra="""<h3>Minutes to decimal hours</h3><div class="tbl"><table><thead><tr><th>Minutes</th><th>Decimal</th><th>Minutes</th><th>Decimal</th></tr></thead><tbody>
<tr><td>5</td><td>0.08</td><td>35</td><td>0.58</td></tr><tr><td>10</td><td>0.17</td><td>40</td><td>0.67</td></tr><tr><td>15</td><td>0.25</td><td>45</td><td>0.75</td></tr>
<tr><td>20</td><td>0.33</td><td>50</td><td>0.83</td></tr><tr><td>25</td><td>0.42</td><td>55</td><td>0.92</td></tr><tr><td>30</td><td>0.50</td><td>60</td><td>1.00</td></tr></tbody></table></div>""",
 faqs=[("How do I convert minutes to decimal hours?","Divide the minutes by 60. 15 minutes is 0.25 hours, 30 minutes is 0.5 and 45 minutes is 0.75, so 7 hours 45 minutes is 7.75 hours. Payroll systems usually work in decimal hours, and the calculator shows both."),
       ("Does it work for overnight shifts?","Yes. When the end time is earlier than the start time, the shift is counted as running past midnight. A shift from 11:00 PM to 7:30 AM with a 30-minute break counts as 8 hours."),
       ("Is the result my take-home pay?","No. It is gross pay before income tax, Social Security, pension or other deductions, so your payslip will show a lower net amount."),
       ("Are my entries private?","Yes. Everything is calculated in your browser. Your week is saved only in this browser's local storage and is never sent to our servers.")],
 related=["hours","salary","tip","days"])

tool(id="hours", slug="hours-calculator", cat="Work & pay", name="Hours Calculator",
 short="Hours between times", desc="How long between two clock times.",
 title="Hours Calculator – Time Between Two Times | Numbrik",
 meta="Calculate the hours and minutes between two times, minus breaks. Shows hours, minutes and decimal hours. Handles shifts that cross midnight.",
 lede="Find the time between two clock times, minus any unpaid break. You get the answer in hours and minutes and in decimal hours.",
 steps=["Enter a start time and an end time.","Add an unpaid break in minutes, or leave it at 0.","Read the time worked in hours and minutes, decimal hours and total minutes."],
 how="""<p>The calculator turns both times into minutes after midnight, subtracts the start from the end and removes the break. When the end time is earlier than the start time, it assumes the period crosses midnight and adds 24 hours.</p>
<p>Decimal hours are the hours plus the minutes divided by 60. Timesheets and payroll software often ask for decimal hours, so 6 hours 20 minutes becomes 6.33.</p>""",
 formula="Minutes = end − start − break   (add 1,440 if end is before start)\nDecimal hours = minutes ÷ 60",
 example="<p>From 8:45 AM to 5:15 PM is 8 hours 30 minutes. Take off a 30-minute lunch and the time worked is <strong>8h 00m</strong>, or <strong>8.00</strong> decimal hours.</p>",
 extra="",
 faqs=[("How many hours is 9 to 5?","8 hours. With a 30-minute unpaid lunch it is 7.5 hours, and with a 1-hour lunch it is 7 hours."),
       ("How do I calculate hours across midnight?","Count from the start time to midnight, then add the time from midnight to the end. 10:00 PM to 6:00 AM is 2 hours plus 6 hours, or 8 hours. The calculator does this for you."),
       ("What is 8 hours 20 minutes as a decimal?","8.33 hours, because 20 ÷ 60 = 0.333."),
       ("Should I use this or the time card calculator?","Use this page for one period of time. For a whole week with overtime and pay, use the time card calculator.")],
 related=["timecard","salary","days","age"])

sal_rows = "".join(f"<tr><td>{usd(h,0)}</td><td>{usd(h*2080,0)}</td><td>{usd(h*2080/12)}</td><td>{usd(h*40)}</td></tr>" for h in [15,18,20,22,25,30,35,40,50])
tool(id="salary", slug="hourly-to-salary-calculator", cat="Work & pay", name="Hourly to Salary Calculator",
 short="Hourly ↔ salary", desc="Convert hourly wage to yearly, monthly and weekly pay.",
 title="Hourly to Salary Calculator – Wage Converter | Numbrik",
 meta="Convert an hourly wage to annual, monthly, biweekly and weekly pay, or a salary to an hourly rate. See what $20, $25 or $30 an hour is per year.",
 lede="Convert an hourly wage into yearly, monthly, biweekly and weekly pay, or work backwards from a salary to an hourly rate.",
 steps=["Choose whether you know your hourly rate or your annual salary.","Enter the amount, your hours per week and your paid weeks per year.","Read the hourly, daily, weekly, biweekly, monthly and yearly figures."],
 how="""<p>A full-time US work year is usually counted as 40 hours × 52 weeks = 2,080 paid hours. In Australia full-time is 38 hours a week, so the hours field starts at 38 when you choose Australia. Paid holidays and paid leave still count as paid weeks; lower the number only for unpaid time off.</p>
<p>Monthly pay divides the year by 12. Multiplying weekly pay by 4 understates it, because a month averages about 4.33 weeks.</p>""",
 formula="Annual pay  = hourly rate × hours per week × paid weeks\nHourly rate = annual pay ÷ (hours per week × paid weeks)",
 example=f"<p>{usd(25,0)} an hour at 40 hours a week for 52 weeks is <strong>{usd(52000,0)} a year</strong>, {usd(52000/12)} a month and {usd(2000,0)} every two weeks, before tax.</p>",
 extra=f"""<h3>Hourly wage to annual salary (40 hours, 52 weeks)</h3><div class="tbl"><table><thead><tr><th>Hourly</th><th>Yearly</th><th>Monthly</th><th>Weekly</th></tr></thead><tbody>{sal_rows}</tbody></table></div>""",
 faqs=[("$20 an hour is how much a year?","$41,600 before tax, at 40 hours a week for 52 weeks. That is about $3,467 a month."),
       ("How many working hours are in a year?","2,080 at 40 hours a week for 52 weeks. At 38 hours a week it is 1,976, and at 37.5 hours it is 1,950."),
       ("Is the result before or after tax?","Before tax. Income tax, social security and pension contributions all reduce what you take home."),
       ("How do I compare a salary job with an hourly job?","Convert both to the same unit. Remember that hourly jobs may pay overtime, while salaried roles may include paid leave and benefits that are not in the hourly rate.")],
 related=["timecard","hours","percent","loan"])

# ======================= MONEY =======================
tool(id="tip", slug="tip-calculator", cat="Money", name="Tip Calculator",
 short="Tip & split", desc="Tip amount and each person’s share.",
 title="Tip Calculator & Bill Splitter | Numbrik",
 meta="Work out the tip and split the bill between friends. Quick buttons for 15%, 18%, 20% and 25%, with tipping customs for the US, Canada, UK and Australia.",
 lede="Work out the tip and how much each person pays when you split the bill.",
 steps=["Enter the bill total.","Pick a tip percentage or type your own.","Enter how many people are paying and read each person's share."],
 how="""<p>The tip is the bill multiplied by the tip percentage. Add it to the bill and divide by the number of people to get each share.</p>
<p>Customs differ by country. In the US and Canada, 15–20% is usual at sit-down restaurants. In the UK a 12.5% service charge is often already on the bill, so check before adding more. In Australia and the Netherlands tipping is optional; rounding up or leaving around 5–10% for good service is common. In the US many people tip on the amount before sales tax.</p>""",
 formula="Tip = bill × tip % ÷ 100\nEach person = (bill + tip) ÷ people",
 example="<p>A $86.40 bill with an 18% tip is $15.55 in tip and $101.95 in total. Split three ways, each person pays <strong>$33.98</strong>.</p>",
 extra="",
 faqs=[("How much is a 20% tip on $50?","$10, for a total of $60. A quick way: move the decimal one place left to get 10% ($5), then double it."),
       ("Should I tip on the total before or after tax?","Etiquette guides in the US usually suggest tipping on the pre-tax amount, but many people tip on the full total. Either is accepted."),
       ("How do I split a bill unevenly?","Work out each person's share of the food and drinks, then apply the same tip percentage to each share."),
       ("Is a service charge the same as a tip?","A service charge is added by the restaurant. If one is already on the bill, you usually don't need to tip again unless you want to.")],
 related=["percent","salary","timecard","convert"])

tool(id="percent", slug="percentage-calculator", cat="Money", name="Percentage Calculator",
 short="Percentage", desc="Percent of, percent change, and what-percent.",
 title="Percentage Calculator – Percent Of, Change | Numbrik",
 meta="Three percentage calculators in one: X% of Y, X is what percent of Y, and percentage increase or decrease between two numbers. With formulas and examples.",
 lede="Three percentage calculators in one: find X% of a number, what percent one number is of another, and the percentage change between two values.",
 steps=["Choose the type of question at the top.","Enter the two numbers.","Read the answer and the extra results underneath."],
 how="""<p><strong>X% of Y</strong> multiplies Y by X and divides by 100. It also shows Y with that percentage added and taken away, which is handy for discounts and price rises.</p>
<p><strong>X is what percent of Y</strong> divides X by Y and multiplies by 100.</p>
<p><strong>Percent change</strong> divides the difference by the starting value. A change is not symmetrical: going from 80 to 100 is a 25% increase, but going from 100 back to 80 is a 20% decrease, because the starting value is different.</p>""",
 formula="X% of Y          = X ÷ 100 × Y\nX as % of Y      = X ÷ Y × 100\nPercent change   = (new − old) ÷ |old| × 100",
 example="<p>15% of 240 is <strong>36</strong>. 45 is <strong>25%</strong> of 180. A price that moves from 80 to 100 has risen by <strong>+25%</strong>.</p>",
 extra="",
 faqs=[("How do I calculate a discount?","Multiply the price by the discount rate. 30% off $70 is 0.30 × 70 = $21 off, so you pay $49."),
       ("How do I reverse a percentage increase?","Divide by 1 plus the rate. If a price is $120 after a 20% increase, the original was 120 ÷ 1.20 = $100."),
       ("What is the difference between percent change and percentage points?","Percentage points measure the gap between two percentages. A rate moving from 4% to 5% is a rise of 1 percentage point but a 25% increase."),
       ("Why doesn't +25% then −25% get back to the start?","The second change applies to a bigger number. 100 + 25% = 125, and 125 − 25% = 93.75.")],
 related=["tip","loan","salary","gcf"])

am_rows = ""
for P,r,y in [(250000,6.5,30),(350000,6.5,30),(350000,6.5,15),(350000,5.5,30),(500000,6.5,30)]:
    m = pmt(P,r,y*12); am_rows += f"<tr><td>{usd(P,0)}</td><td>{r}%</td><td>{y} yrs</td><td>{usd(m)}</td><td>{usd(m*y*12-P,0)}</td></tr>"
tool(id="loan", slug="mortgage-calculator", cat="Money", name="Mortgage & Loan Calculator",
 short="Mortgage & loan", desc="Monthly payment, total interest and payoff by year.",
 title="Mortgage & Loan Calculator with Amortization | Numbrik",
 meta="Calculate your monthly mortgage or loan payment, total interest and yearly amortization. Works for home loans, personal loans and any fixed-rate loan.",
 lede="Find the monthly payment for a mortgage or any fixed-rate loan, the total interest you will pay, and how each year's payments split between principal and interest.",
 steps=["Enter the loan amount (the price minus your down payment).","Enter the yearly interest rate and the term in years.","Read the monthly payment and total interest, then check the yearly chart to see the balance fall."],
 how="""<p>This is a standard amortizing loan: every monthly payment is the same, and each one pays the interest due that month plus some of the balance. Early payments are mostly interest because interest is charged on a large balance. As the balance falls, more of each payment goes to principal, which the yearly chart shows.</p>
<p>The payment covers principal and interest only. A US mortgage payment often also includes property tax, homeowners insurance and sometimes mortgage insurance (PMI), which are not added here. Canadian fixed-rate mortgages compound semi-annually, so a Canadian lender's quoted payment can be slightly lower than this monthly-compounding result.</p>""",
 formula="M = P × r(1 + r)ⁿ ÷ ((1 + r)ⁿ − 1)\nP = loan amount   r = yearly rate ÷ 12   n = number of monthly payments",
 example=f"<p>A {usd(350000,0)} loan at 6.5% over 30 years costs <strong>{usd(m350)} a month</strong>. Over 360 payments you pay {usd(m350*360,0)}, of which {usd(m350*360-350000,0)} is interest. The same loan over 15 years costs {usd(m350_15)} a month but only {usd(m350_15*180-350000,0)} in interest.</p>",
 extra=f"""<h3>Example payments</h3><div class="tbl"><table><thead><tr><th>Loan</th><th>Rate</th><th>Term</th><th>Monthly</th><th>Total interest</th></tr></thead><tbody>{am_rows}</tbody></table></div>""",
 faqs=[("How does a shorter term change the cost?","A shorter term raises the monthly payment but cuts total interest sharply, because the balance is paid down faster. The table above compares 30 and 15 years on the same loan."),
       ("Do extra payments help?","Yes. Extra money normally goes straight to principal, which lowers the interest charged every month after. Check that your lender has no prepayment penalty."),
       ("Does this include property tax and insurance?","No. It shows principal and interest only. Add your lender's estimates for tax, insurance and any HOA fees to get the full monthly cost."),
       ("Can I use it for personal or student loans?","Yes. It works for any fixed-rate loan with equal monthly payments. For a car purchase, the auto loan calculator also handles trade-in and sales tax.")],
 related=["autoloan","percent","salary","sqft"])

tool(id="autoloan", slug="auto-loan-calculator", cat="Money", name="Auto Loan Calculator",
 short="Auto loan", desc="Monthly car payment with down payment, trade-in and tax.",
 title="Auto Loan Calculator – Car Payment with Tax | Numbrik",
 meta="Estimate your monthly car payment including down payment, trade-in, sales tax and interest. Compare 36 to 84 month terms and see total interest.",
 lede="Estimate your monthly car payment with the vehicle price, down payment, trade-in, sales tax and loan term all included.",
 steps=["Enter the vehicle price, your down payment and any trade-in value.","Enter the sales tax rate and the interest rate from your lender.","Pick a term and read the monthly payment, total interest and total cost."],
 how="""<p>The amount you borrow is the price, minus your down payment and trade-in, plus sales tax. In many US states sales tax is charged on the price after the trade-in is taken off, which is how this calculator works; a few states tax the full price, so check your state's rule. Dealer, title and registration fees are not included.</p>
<p>A longer term lowers the monthly payment but increases the total interest, and cars lose value quickly, so on long loans you can owe more than the car is worth for several years.</p>""",
 formula="Amount financed = price − down payment − trade-in + sales tax\nMonthly payment = A × r(1 + r)ⁿ ÷ ((1 + r)ⁿ − 1)",
 example=f"<p>A {usd(34000,0)} car with {usd(4000,0)} down, a {usd(3000,0)} trade-in and 7% sales tax ({usd(car_tax,0)}) leaves {usd(car_P,0)} to finance. At 6.9% for 60 months the payment is <strong>{usd(car60)}</strong>. Over 48 months it is {usd(car48)} with {usd(car48*48-car_P,0)} interest; over 72 months it is {usd(car72)} with {usd(car72*72-car_P,0)} interest.</p>",
 extra="",
 faqs=[("Is a 72-month car loan a good idea?","It lowers the payment but costs more interest and increases the time you may owe more than the car is worth. Compare the total cost, not just the monthly figure."),
       ("How much should I put down on a car?","Many guides suggest about 20% on a new car and 10% on a used car, which helps avoid owing more than the car's value."),
       ("Does my credit score change the rate?","Yes. Lenders set rates largely by credit history, so getting a pre-approval from a bank or credit union before visiting the dealer helps you compare offers."),
       ("Does this work for leasing?","No. Leases are priced on depreciation and a money factor, which work differently from a loan.")],
 related=["loan","percent","salary","tip"])

# ======================= HEALTH =======================
tool(id="bmi", slug="bmi-calculator", cat="Health", name="BMI Calculator",
 short="BMI", desc="Body mass index with the WHO category.",
 title="BMI Calculator – Imperial & Metric | Numbrik",
 meta="Calculate your body mass index in feet and pounds or centimetres and kilograms. See your WHO weight category and the healthy weight range for your height.",
 lede="Calculate body mass index from your height and weight in feet and pounds or centimetres and kilograms, and see the healthy weight range for your height.",
 steps=["Choose feet and pounds or centimetres and kilograms.","Enter your height and weight.","Read your BMI, its category and the healthy weight range for your height."],
 how="""<p>BMI divides your weight by the square of your height. It is a quick screening number used by doctors and public health bodies, but it does not measure body fat directly. Very muscular people can have a high BMI without excess fat, and BMI says nothing about where fat is stored.</p>
<p>The categories below are the World Health Organization's adult cut-offs. Some guidelines use lower cut-offs for people of South Asian, Chinese and other Asian backgrounds. Children and teenagers use age- and sex-specific percentiles instead, so this calculator is for adults aged 18 and over.</p>""",
 formula="BMI = weight (kg) ÷ height (m)²\nBMI = 703 × weight (lb) ÷ height (in)²",
 example=f"<p>Someone 5 ft 9 in tall weighing 165 lb has a BMI of <strong>{bmi_imp:.1f}</strong>. In metric, 175 cm and 72 kg gives <strong>{bmi_met:.1f}</strong>. Both fall in the healthy weight range.</p>",
 extra="""<h3>Adult BMI categories (WHO)</h3><div class="tbl"><table><thead><tr><th>BMI</th><th>Category</th></tr></thead><tbody>
<tr><td>Below 18.5</td><td>Underweight</td></tr><tr><td>18.5 – 24.9</td><td>Healthy weight</td></tr><tr><td>25.0 – 29.9</td><td>Overweight</td></tr><tr><td>30.0 and above</td><td>Obesity</td></tr></tbody></table></div>""",
 faqs=[("What is a healthy BMI?","For adults, 18.5 to 24.9 is the healthy weight range in the WHO classification."),
       ("Is BMI accurate for athletes?","Not very. Muscle is dense, so muscular people often score as overweight. Waist measurement or body-fat tests give a better picture."),
       ("Is BMI different for men and women?","The adult formula and categories are the same for both. Body fat at the same BMI tends to differ between men and women, which is one of the measure's limits."),
       ("Can children use this calculator?","No. Children and teens need BMI-for-age percentiles from a pediatric chart.")],
 related=["calorie","sleep","convert","age"])

tool(id="calorie", slug="calorie-calculator", cat="Health", name="Calorie Calculator",
 short="Calorie needs", desc="Daily calories to maintain, lose or gain weight.",
 title="Calorie Calculator – Daily Calories (TDEE) | Numbrik",
 meta="Estimate how many calories you burn a day (TDEE) using the Mifflin-St Jeor equation. Get daily calorie targets to maintain, lose or gain weight.",
 lede="Estimate how many calories you burn in a day and how many to eat to keep your weight steady, lose slowly or gain.",
 steps=["Choose your units and sex, then enter your age, height and weight.","Pick the activity level that matches a normal week.","Read your maintenance calories and the targets for gentle loss or gain."],
 how="""<p>The calculator first estimates your basal metabolic rate (BMR), the energy your body uses at rest, with the Mifflin-St Jeor equation. It then multiplies BMR by an activity factor to estimate total daily energy expenditure (TDEE), which is roughly the calories that keep your weight stable.</p>
<p>A deficit of about 500 kcal a day is commonly linked to losing around 0.5 kg (1 lb) a week, though real results vary as the body adapts. Targets never go below 1,200 kcal for women or 1,500 kcal for men, because eating less than that without medical supervision is generally not advised. The results are estimates for healthy adults; if you are pregnant, under 18 or managing a health condition, ask a doctor or registered dietitian.</p>""",
 formula="Men:    BMR = 10 × kg + 6.25 × cm − 5 × age + 5\nWomen:  BMR = 10 × kg + 6.25 × cm − 5 × age − 161\nTDEE   = BMR × activity factor",
 example=f"<p>A 34-year-old woman, 5 ft 6 in and 150 lb, has a BMR of about {bmr:,.0f} kcal. With light exercise (factor 1.375) her maintenance is about <strong>{round(tdee/10)*10:,} kcal a day</strong>.</p>",
 extra="""<h3>Activity factors</h3><div class="tbl"><table><thead><tr><th>Activity level</th><th>Factor</th></tr></thead><tbody>
<tr><td>Mostly sitting, little exercise</td><td>1.2</td></tr><tr><td>Light exercise 1–3 days a week</td><td>1.375</td></tr><tr><td>Moderate exercise 3–5 days a week</td><td>1.55</td></tr><tr><td>Hard exercise 6–7 days a week</td><td>1.725</td></tr><tr><td>Physical job plus training</td><td>1.9</td></tr></tbody></table></div>""",
 faqs=[("What is TDEE?","Total daily energy expenditure: the calories you burn in a day from resting metabolism, digestion and movement combined."),
       ("How accurate is this?","Mifflin-St Jeor is one of the better-performing formulas in studies, but individuals can differ from the estimate by 10% or more. Track your weight for a few weeks and adjust."),
       ("Which activity level should I pick?","Choose by your typical week, not your best one. Most office workers who exercise a few times a week fit 'light' or 'moderate'."),
       ("Can teenagers use it?","No. Teenagers are still growing and have different needs, so they should get advice from a doctor.")],
 related=["bmi","sleep","convert","percent"])

tool(id="sleep", slug="sleep-calculator", cat="Health", name="Sleep Calculator",
 short="Sleep time", desc="Bedtimes that line up with 90-minute sleep cycles.",
 title="Sleep Calculator – Best Bedtime & Wake Time | Numbrik",
 meta="Find the best time to go to bed or wake up based on 90-minute sleep cycles. Enter your wake-up time or bedtime and get times that help you wake refreshed.",
 lede="Find bedtimes and wake-up times that line up with 90-minute sleep cycles, so you are more likely to wake at the end of a cycle than in the middle of deep sleep.",
 steps=["Choose whether you know your wake-up time or your bedtime.","Enter the time and how long you usually take to fall asleep.","Pick one of the suggested times. Five or six cycles suit most adults."],
 how="""<p>Sleep runs in cycles of light sleep, deep sleep and REM sleep. A cycle lasts roughly 80 to 110 minutes, and 90 minutes is a common average. Waking at the end of a cycle, when sleep is lighter, usually feels easier than waking from deep sleep.</p>
<p>Health bodies including the American Academy of Sleep Medicine and the CDC recommend at least 7 hours a night for adults. Five cycles (7.5 hours) and six cycles (9 hours) fit that range, so those times are highlighted. Treat the times as a guide: your own cycles may be a little shorter or longer.</p>""",
 formula="Bedtime  = wake-up time − cycles × 90 min − time to fall asleep\nWake time = bedtime + time to fall asleep + cycles × 90 min",
 example="<p>To wake at 6:30 AM, taking 15 minutes to fall asleep, go to bed at <strong>10:45 PM</strong> for five cycles or 9:15 PM for six.</p>",
 extra="",
 faqs=[("What time should I go to bed to wake up at 7 AM?","Around 11:15 PM for five cycles (7.5 hours) or 9:45 PM for six cycles (9 hours), if you take about 15 minutes to fall asleep."),
       ("Is 6 hours of sleep enough?","For most adults, no. The recommendation is at least 7 hours. Regularly sleeping 6 hours or less is linked with poorer concentration and health."),
       ("Why do I feel groggy after a full night's sleep?","Waking from deep sleep can cause sleep inertia, a heavy feeling that usually fades within 15 to 30 minutes. Daylight and a regular schedule help."),
       ("Are sleep cycles always 90 minutes?","No. They vary between people and through the night, with more deep sleep early and more REM sleep towards morning.")],
 related=["age","calorie","bmi","hours"])

# ======================= STUDENTS =======================
tool(id="gpa", slug="gpa-calculator", cat="Students", name="GPA Calculator",
 short="GPA", desc="Semester GPA on the US 4.0 scale, plus cumulative.",
 title="GPA Calculator – Semester & Cumulative GPA | Numbrik",
 meta="Calculate your semester and cumulative GPA on the 4.0 scale. Add courses, letter grades and credit hours. Your courses are saved in your browser.",
 lede="Add your courses, letter grades and credits to get your semester GPA on the 4.0 scale. Add your current GPA and credits to see your new cumulative GPA.",
 steps=["Enter each course with its letter grade and credit hours. Use Add course for more rows.","Remove example rows you don't need with ✕.","To see your cumulative GPA, enter your current GPA and the credits you have already earned."],
 how="""<p>Each letter grade has a grade-point value. The calculator multiplies each grade's points by the course credits, adds them up and divides by the total credits, so a 4-credit course counts more than a 1-credit lab.</p>
<p>This is an unweighted GPA. A+ counts as 4.0, which is the most common practice, though some schools give 4.3. High schools that add points for honors or AP classes report a weighted GPA, which can go above 4.0. Pass/fail courses usually don't count toward GPA, so leave them out.</p>""",
 formula="GPA = Σ(grade points × credits) ÷ Σ credits\nCumulative = (current GPA × earned credits + new grade points) ÷ (earned + new credits)",
 example=f"<p>The example term has five courses worth 14 credits and {gpa_pts:.1f} grade points, a semester GPA of <strong>{gpa:.2f}</strong>. A student who already had a 3.40 GPA over 45 credits would move to a cumulative <strong>{cum:.2f}</strong>.</p>",
 extra="""<h3>Grade points</h3><div class="tbl"><table><thead><tr><th>Grade</th><th>Points</th><th>Grade</th><th>Points</th></tr></thead><tbody>
<tr><td>A+ / A</td><td>4.0</td><td>C+</td><td>2.3</td></tr><tr><td>A−</td><td>3.7</td><td>C</td><td>2.0</td></tr><tr><td>B+</td><td>3.3</td><td>C−</td><td>1.7</td></tr>
<tr><td>B</td><td>3.0</td><td>D+</td><td>1.3</td></tr><tr><td>B−</td><td>2.7</td><td>D</td><td>1.0</td></tr><tr><td></td><td></td><td>F</td><td>0.0</td></tr></tbody></table></div>""",
 faqs=[("What is a good GPA?","A 3.0 is a B average. Many competitive programs and scholarships look for 3.5 or higher, but requirements differ by school."),
       ("How can I raise my GPA fastest?","Higher grades in courses with more credits move your GPA the most. The more credits you have already earned, the slower your cumulative GPA changes."),
       ("Does a withdrawn or pass/fail course count?","Usually not. A W or a pass grade normally carries no grade points, so leave it out. Check your school's policy."),
       ("Do Australian or UK universities use this scale?","Not usually. Most Australian universities use a 7-point GPA, and UK degrees use classifications such as First or 2:1. This calculator uses the US 4.0 scale.")],
 related=["grade","finalgrade","percent","lcm"])

tool(id="lcm", slug="lcm-calculator", cat="Students", name="LCM Calculator",
 short="LCM", desc="Least common multiple of two or more whole numbers.",
 title="LCM Calculator – Least Common Multiple | Numbrik",
 meta="Find the least common multiple of 2 to 20 numbers with prime factorization shown. Use it to find common denominators for fractions.",
 lede="Find the least common multiple of 2 to 20 whole numbers, with the prime factorization of each number shown.",
 steps=["Type your numbers separated by commas or spaces.","Read the LCM, the GCF of the same numbers and the prime factors."],
 how="""<p>The least common multiple is the smallest positive number that every number in your list divides into evenly. One way to find it is prime factorization: write each number as a product of primes and multiply together the highest power of every prime that appears.</p>
<p>Another way uses the greatest common factor: for two numbers, LCM(a, b) = a × b ÷ GCF(a, b). For more numbers the calculator repeats this one pair at a time. The LCM is what you need to find a common denominator when adding fractions.</p>""",
 formula="LCM(a, b) = a × b ÷ GCF(a, b)\nLCM(a, b, c) = LCM(LCM(a, b), c)",
 example="<p>12 = 2² × 3, 18 = 2 × 3² and 30 = 2 × 3 × 5. Taking the highest power of each prime gives 2² × 3² × 5 = <strong>180</strong>.</p>",
 extra="",
 faqs=[("What is the LCM of 4 and 6?","12. Multiples of 4 are 4, 8, 12… and multiples of 6 are 6, 12…, so 12 is the first one they share."),
       ("What is the difference between LCM and LCD?","The least common denominator is the LCM of the denominators of a set of fractions. To add 1/4 and 1/6, use 12 as the denominator."),
       ("Can the LCM be smaller than the numbers?","No. The LCM is always at least as large as the biggest number in the list."),
       ("Where is the LCM used in real life?","Repeating schedules. If one bus comes every 12 minutes and another every 18, they arrive together every 36 minutes.")],
 related=["gcf","percent","gpa","dice"])

tool(id="gcf", slug="gcf-calculator", cat="Students", name="GCF Calculator",
 short="GCF", desc="Greatest common factor of two or more whole numbers.",
 title="GCF Calculator – Greatest Common Factor | Numbrik",
 meta="Find the greatest common factor (GCD or HCF) of 2 to 20 numbers with prime factorization. Use it to simplify fractions and split things into equal groups.",
 lede="Find the greatest common factor, also called the GCD or HCF, of 2 to 20 whole numbers, with each number's prime factorization.",
 steps=["Type your numbers separated by commas or spaces.","Read the GCF, the LCM of the same numbers and the prime factors."],
 how="""<p>The greatest common factor is the largest number that divides every number in the list without a remainder. With prime factorization, multiply the primes the numbers share, each at its lowest power.</p>
<p>The calculator uses Euclid's algorithm, which is fast even for large numbers: replace the larger number with the remainder after dividing by the smaller one, and repeat until the remainder is 0. The last non-zero number is the GCF.</p>""",
 formula="GCF(a, b) = GCF(b, a mod b), until the remainder is 0",
 example="<p>48 = 2⁴ × 3, 180 = 2² × 3² × 5 and 72 = 2³ × 3². The shared primes at their lowest powers are 2² × 3 = <strong>12</strong>. With Euclid: 180 mod 48 = 36, 48 mod 36 = 12, 36 mod 12 = 0, so GCF(180, 48) = 12.</p>",
 extra="",
 faqs=[("What is the GCF of 12 and 18?","6. The factors of 12 are 1, 2, 3, 4, 6, 12 and the factors of 18 are 1, 2, 3, 6, 9, 18; the largest shared one is 6."),
       ("How do I simplify a fraction with the GCF?","Divide the top and bottom by their GCF. For 48/180 the GCF is 12, so it simplifies to 4/15."),
       ("What does it mean if the GCF is 1?","The numbers are coprime: they share no factor except 1, so a fraction made from them is already in lowest terms."),
       ("Is GCF the same as GCD and HCF?","Yes. Greatest common factor, greatest common divisor and highest common factor are three names for the same thing.")],
 related=["lcm","percent","gpa","dice"])

# ======================= DATES & TIME =======================
tool(id="age", slug="age-calculator", cat="Dates & time", name="Age Calculator",
 short="Age", desc="Exact age and days until your next birthday.",
 title="Age Calculator – Exact Age in Years, Months, Days | Numbrik",
 meta="Calculate your exact age in years, months and days, plus your age in days and weeks and the days until your next birthday. Find age on any date.",
 lede="Find your exact age in years, months and days, your age in total days and weeks, and how long until your next birthday.",
 steps=["Enter a date of birth.","Leave 'Age on' as today, or pick another date to find an age in the past or future.","Read the exact age, total days and weeks, and the countdown to the next birthday."],
 how="""<p>The calculator counts full years first, then full months, then the remaining days. If the birth day hasn't come yet in the current month, it borrows the days of the previous month, the same way you would count on a calendar.</p>
<p>For people born on February 29, the next-birthday countdown uses March 1 in years that are not leap years. Legal rules for this differ between countries.</p>""",
 formula="Age = full years + full months + remaining days between the two dates",
 example=f"<p>Someone born on March 17, 1994 is <strong>{ay} years, {am} months and {ad} days</strong> old on October 20, 2026. That is {adays:,} days, or about {adays//7:,} weeks.</p>",
 extra="",
 faqs=[("How do I work out my age in months?","Multiply your full years by 12 and add the extra months. At 32 years and 7 months you are 391 months old."),
       ("Can I find someone's age on a past date?","Yes. Change the 'Age on' date to any day after the birth date."),
       ("How many days old am I?","Enter your birth date and read 'In days'. It counts every day from your birth date up to the 'Age on' date."),
       ("How is a February 29 birthday handled?","In non-leap years the next-birthday countdown uses March 1.")],
 related=["days","sleep","hours","gpa"])

tool(id="days", slug="days-between-dates", cat="Dates & time", name="Days Between Dates",
 short="Days between dates", desc="Calendar days and weekdays between two dates.",
 title="Days Between Dates Calculator & Countdown | Numbrik",
 meta="Count the days, weeks and weekdays between two dates, or count down to Christmas, a holiday, deadline or trip. Free date difference calculator.",
 lede="Count the days, weeks and weekdays between two dates, or count down to a holiday, deadline or trip.",
 steps=["Pick a start date and an end date.","Read the number of days, weekdays, weeks and approximate months."],
 how="""<p>The start date is not counted and the end date is, so Monday to Friday of the same week is 4 days. If you want to include both dates, add 1.</p>
<p>Weekdays are Monday to Friday. Public holidays are not removed, because they differ by country, state and employer; subtract them yourself for an exact working-day count.</p>""",
 formula="Days = end date − start date\nWeeks = days ÷ 7",
 example=f"<p>From October 20, 2026 to Christmas Day is <strong>{ndays} days</strong>, which includes {wdays} weekdays and is about {ndays/7:.1f} weeks.</p>",
 extra="",
 faqs=[("How many days until Christmas?","The calculator opens with today's date and December 25 filled in, so the answer is on screen as soon as the page loads."),
       ("Does it include the end date?","Yes, the end date is counted and the start date is not. Add 1 to include both."),
       ("How many weeks is 90 days?","12 weeks and 6 days, or about 12.9 weeks."),
       ("Does it skip public holidays?","No. It counts Monday to Friday. Subtract the public holidays that apply to you.")],
 related=["age","hours","timecard","sleep"])

# ======================= HOME =======================
tool(id="sqft", slug="square-footage-calculator", cat="Home", name="Square Footage Calculator",
 short="Square footage", desc="Area of rooms and shapes, with material cost.",
 title="Square Footage Calculator – Area & Cost | Numbrik",
 meta="Calculate square feet or square metres for rooms, circles and triangles. Add waste for flooring or tile and estimate material cost. Includes conversions.",
 lede="Measure the area of rooms and shapes in square feet or square metres, add a waste allowance and estimate material cost for flooring, tile, carpet or turf.",
 steps=["Choose a shape and feet or metres.","Enter the measurements and how many identical areas you have.","Add the material price and a waste percentage to see how much to buy and what it costs."],
 how="""<p>Area is length times width for a rectangle, π times the radius squared for a circle, and half the base times the height for a triangle. For an L-shaped or irregular room, split it into rectangles, work out each one and add them up.</p>
<p>Buy more than the exact area to allow for cuts and mistakes. About 10% extra is usual for straight layouts and 15% for diagonal or patterned tile. Measurements in inches can be divided by 12 to get feet.</p>""",
 formula="Rectangle = length × width\nCircle    = π × (diameter ÷ 2)²\nTriangle  = base × height ÷ 2\n1 m² = 10.764 sq ft     1 sq yd = 9 sq ft",
 example="<p>A 14 × 12 ft room is <strong>168 sq ft</strong> (15.6 m²). With 10% waste you need 184.8 sq ft, and at $4.50 per sq ft the flooring costs about <strong>$831.60</strong>.</p>",
 extra="",
 faqs=[("How do I measure an L-shaped room?","Split it into two rectangles, measure each, calculate both areas and add them together."),
       ("How many square feet is a 12 × 12 room?","144 square feet, or about 13.4 square metres."),
       ("How do I convert square feet to square metres?","Divide by 10.764. 200 sq ft is about 18.6 m²."),
       ("How much flooring should I buy?","Take the area with waste and round up to whole boxes. Keep a spare box for future repairs.")],
 related=["convert","loan","percent","autoloan"])

# ======================= CONVERTERS =======================
oven = "".join(f"<tr><td>{f}°F</td><td>{f2c(f):.0f}°C</td><td>{g}</td></tr>" for f,g in [(300,2),(325,3),(350,4),(375,5),(400,6),(425,7),(450,8)])
tool(id="convert", slug="unit-converter", cat="Converters", name="Unit Converter",
 short="Unit converter", desc="Kitchen, length, weight and temperature.",
 title="Unit Converter – Cups, ml, °F to °C, Inches | Numbrik",
 meta="Convert cups to ml, Fahrenheit to Celsius, inches to cm, pounds to kg and more. Includes US and metric cups and an oven temperature chart.",
 lede="Convert kitchen measures, length, weight and temperature, including US cups, metric cups, tablespoons, feet, metres, pounds, kilograms, °F, °C and kelvin.",
 steps=["Choose kitchen, length, weight or temperature.","Enter a value and pick the units to convert from and to.","Read the answer and the same value in other common units. Use Swap to reverse."],
 how="""<p>A US cup is 236.6 ml. Australia, New Zealand and Canada commonly use a 250 ml metric cup, so the same '1 cup' differs by about 5%; choose 'metric cup' for those recipes. Tablespoons differ too: a US tablespoon is about 14.8 ml, while an Australian tablespoon is 20 ml.</p>
<p>Cups measure volume and grams measure weight, so converting between them depends on the ingredient. One US cup of all-purpose flour weighs about 120–125 g, granulated sugar about 200 g and butter about 227 g.</p>""",
 formula="°C = (°F − 32) × 5 ÷ 9\n°F = °C × 9 ÷ 5 + 32\nK  = °C + 273.15",
 example=f"<p>1.5 US cups is <strong>354.9 ml</strong>. An oven at 350°F is <strong>{f2c(350):.1f}°C</strong>, which recipes usually round to 180°C (gas mark 4).</p>",
 extra=f"""<h3>Oven temperatures</h3><div class="tbl"><table><thead><tr><th>Fahrenheit</th><th>Celsius</th><th>Gas mark</th></tr></thead><tbody>{oven}</tbody></table></div>""",
 faqs=[("How many ml are in a cup?","236.6 ml in a US cup and 250 ml in a metric cup used in Australia, New Zealand and Canada."),
       ("How many tablespoons are in a cup?","16 US tablespoons make a US cup. In Australia, with 20 ml tablespoons, a 250 ml cup is 12.5 tablespoons."),
       ("What is 180°C in Fahrenheit?","356°F. Recipes usually treat it as 350°F."),
       ("How many centimetres are in an inch?","Exactly 2.54 cm. A foot is 30.48 cm.")],
 related=["sqft","bmi","calorie","percent"])

# ======================= FUN =======================
d6rows = "".join(f"<tr><td>{s}</td><td>{c}/36</td><td>{c/36*100:.1f}%</td></tr>" for s,c in two_d6.items())
tool(id="dice", slug="dice-roller", cat="Fun", name="Dice Roller",
 short="Dice roller", desc="Roll any number of dice, from d4 to d100.",
 title="Dice Roller – Roll d4, d6, d8, d10, d12, d20 | Numbrik",
 meta="Roll virtual dice online for board games and tabletop RPGs. Choose d4, d6, d8, d10, d12, d20 or d100, roll up to 50 dice and add a modifier.",
 lede="Roll virtual dice for board games, tabletop role-playing games and classroom games. Choose d4 to d100, roll up to 50 dice at once and add a modifier.",
 steps=["Choose the type of die.","Set how many dice to roll and any modifier, such as +3.","Press Roll dice. The highest possible faces are outlined."],
 how="""<p>Each roll uses your browser's cryptographic random number generator, so every face has an equal chance and results can't be predicted from earlier rolls.</p>
<p>Dice notation describes a roll: 3d6+2 means roll three six-sided dice, add them and add 2. One die gives every face the same chance, but sums of several dice cluster in the middle. With two six-sided dice, 7 is the most likely total.</p>""",
 formula="Chance of one face on a die = 1 ÷ number of sides\nRange of NdS + M = (N + M) to (N × S + M)",
 example="<p>2d6 + 3 can land anywhere from 5 to 15. A single d20 gives each number, including a natural 20, a 5% chance.</p>",
 extra=f"""<h3>Two six-sided dice: chance of each total</h3><div class="tbl"><table><thead><tr><th>Total</th><th>Ways</th><th>Chance</th></tr></thead><tbody>{d6rows}</tbody></table></div>""",
 faqs=[("What does 3d6 mean?","Roll three six-sided dice and add the results. The total ranges from 3 to 18."),
       ("Are the rolls truly random?","They come from the browser's cryptographic random generator, the same source used for security keys, so they are unpredictable and fair."),
       ("What is the most common total with two dice?","7, with a 1 in 6 chance (16.7%)."),
       ("What is the chance of at least one 20 when rolling two d20s?","9.75%. The chance of no 20 on both dice is 0.95 × 0.95 = 90.25%, so at least one 20 is 100% − 90.25%.")],
 related=["lcm","gcf","percent","age"])

ORDER = ["Work & pay", "Money", "Health", "Students", "Dates & time", "Home", "Converters", "Fun"]
BYID = {t["id"]: t for t in T}
