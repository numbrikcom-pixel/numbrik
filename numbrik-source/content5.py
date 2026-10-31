"""Calculators added from the OpenRush keyword research (October 31, 2026).
Picked for high US search volume where Numbrik had no page: BMR, ratio, slope, protein,
one rep max, macro, pace, average, right triangle, quadratic formula and CD."""
import math
from content import tool, T, BYID

def tbl(head, rows):
    return ('<div class="tbl"><table><thead><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")

# ---------------- BMR ----------------
mif_m = 10 * 82 + 6.25 * 178 - 5 * 35 + 5
hb_m = 88.362 + 13.397 * 82 + 4.799 * 178 - 5.677 * 35
mif_f = 10 * 65 + 6.25 * 165 - 5 * 30 - 161
ACT = [("Sedentary (desk job, little exercise)", 1.2), ("Lightly active (exercise 1–3 days a week)", 1.375),
       ("Moderately active (3–5 days a week)", 1.55), ("Very active (6–7 days a week)", 1.725), ("Extra active (hard training or physical job)", 1.9)]
tool(id="bmr", slug="bmr-calculator", cat="Health", name="BMR Calculator",
 short="BMR calculator", desc="Calories your body burns at rest each day.",
 title="BMR Calculator – Basal Metabolic Rate | Numbrik",
 meta="Free BMR calculator. Find your basal metabolic rate with the Mifflin-St Jeor and Harris-Benedict equations, plus daily calories for five activity levels.",
 lede="Your basal metabolic rate (BMR) is the number of calories your body burns at complete rest to keep you alive: breathing, circulation, temperature and cell repair. Enter your sex, age, height and weight to see your BMR and the calories you burn each day at different activity levels.",
 steps=["Choose male or female, and US units or metric.", "Enter your age, height and weight.",
        "Read your BMR from the Mifflin-St Jeor equation, with the Harris-Benedict result for comparison, and your daily calories for each activity level."],
 how="""<p>The main result uses the Mifflin-St Jeor equation from 1990. Studies comparing prediction equations with measured metabolic rate found it the most accurate for most adults, usually within 10% of the measured value. It uses weight in kilograms, height in centimetres and age in years, with a constant that differs for men and women.</p>
<p>BMR is only the energy you'd burn lying still all day. To estimate the calories you actually burn, called total daily energy expenditure (TDEE), the calculator multiplies BMR by an activity factor from 1.2 for a desk job with no exercise to 1.9 for hard daily training or a physical job.</p>""",
 formula="Men:   BMR = 10 × weight(kg) + 6.25 × height(cm) − 5 × age + 5\nWomen: BMR = 10 × weight(kg) + 6.25 × height(cm) − 5 × age − 161\nTDEE = BMR × activity factor (1.2 to 1.9)",
 example=f"<p>A 35-year-old man who is 178 cm (5 ft 10 in) tall and weighs 82 kg (181 lb) has a BMR of 10 × 82 + 6.25 × 178 − 5 × 35 + 5 = <strong>{mif_m:,.0f} calories a day</strong>. The revised Harris-Benedict equation gives {hb_m:,.0f}. If he is moderately active, his daily burn is about {mif_m*1.55:,.0f} calories.</p><p>A 30-year-old woman who is 165 cm tall and weighs 65 kg has a BMR of about <strong>{mif_f:,.0f} calories</strong>.</p>",
 extra="<h3>Activity factors</h3>" + tbl(["Activity level", "Multiply BMR by", f"Example: BMR {mif_m:,.0f}"], [(a, f, f"{mif_m*f:,.0f} cal") for a, f in ACT]) +
 "<h3>BMR vs TDEE vs RMR</h3><p><strong>BMR</strong> is measured lying still after a night's sleep and a 12-hour fast. <strong>RMR</strong> (resting metabolic rate) is measured under looser conditions and runs slightly higher. <strong>TDEE</strong> adds everything else you do in a day, from walking and exercise to digesting food. To lose weight you eat below your TDEE, not below your BMR.</p>",
 faqs=[("What is a normal BMR?", "Most adult women have a BMR between about 1,200 and 1,500 calories a day and most adult men between about 1,500 and 1,900. Taller, heavier and younger people burn more."),
       ("Should I eat less than my BMR to lose weight?", "Generally no. Eating below your BMR for long periods can cost muscle and is hard to sustain. Aim for a moderate deficit below your TDEE instead, such as 300–500 calories a day."),
       ("Why does BMR go down with age?", "Adults tend to lose muscle as they age, and muscle burns more energy than fat. Strength training helps keep it up."),
       ("How accurate is a BMR calculator?", "For most people the Mifflin-St Jeor equation is within about 10% of a lab measurement. It is less accurate for very muscular people and people with obesity.")],
 related=["calorie", "macro", "protein", "bmi"])

# ---------------- Ratio ----------------
tool(id="ratio", slug="ratio-calculator", cat="Math", name="Ratio Calculator",
 short="Ratio calculator", desc="Solve proportions and simplify ratios.",
 title="Ratio & Proportion Calculator – Simplify Ratios | Numbrik",
 meta="Free ratio and proportion calculator. Solve A:B = C:D for the missing value, simplify a ratio to lowest terms and scale recipes, maps or screens.",
 lede="Find the missing number in a proportion such as 3:4 = 12:?, and simplify any ratio to its lowest terms. Useful for scaling recipes, mixing concrete or paint, map scales, screen sizes and homework.",
 steps=["Enter the first ratio as A and B, for example 3 and 4 for 3:4.", "Enter C, the number you want to scale to.",
        "Read D, the missing value, plus the simplified ratio, the ratio as 1:n, and as a fraction and decimal."],
 how="""<p>Two ratios are in proportion when they are equal fractions: A/B = C/D. Cross-multiplying gives A × D = B × C, so the missing value is D = B × C ÷ A. That's all a proportion calculator does, but it's easy to put a number on the wrong side, so the answer is shown in full.</p>
<p>To simplify a ratio, both sides are divided by their greatest common factor. 18:24 has a GCF of 6, so it simplifies to 3:4. Decimal ratios are first multiplied by a power of ten, so 1.5:2 becomes 15:20 and then 3:4.</p>""",
 formula="A : B = C : D   →   D = B × C ÷ A\nSimplify: divide A and B by GCF(A, B)",
 example="<p>A recipe uses 3 cups of flour to 4 cups of milk. With 12 cups of flour you need 4 × 12 ÷ 3 = <strong>16 cups of milk</strong>. The ratio 18:24 simplifies to <strong>3:4</strong>, which is also 1:1.333.</p>",
 extra="<h3>Common ratios</h3>" + tbl(["Use", "Ratio", "Means"], [("TV and monitor screens", "16:9", "16 units wide for every 9 tall"), ("Old TVs and iPads", "4:3", "4 wide for every 3 tall"),
  ("Photo prints", "3:2", "a 6 × 4 inch print"), ("Concrete mix", "1:2:3", "cement : sand : gravel"), ("Golden ratio", "1:1.618", "used in art and design"), ("Rice to water", "1:2", "1 cup rice, 2 cups water")]),
 faqs=[("How do you solve a proportion?", "Cross-multiply and divide. For 3:4 = 12:x, multiply 4 by 12 to get 48, then divide by 3 to get x = 16."),
       ("How do you simplify a ratio?", "Divide both numbers by their greatest common factor. 10:25 has a GCF of 5, so it becomes 2:5."),
       ("What is the difference between a ratio and a fraction?", "A ratio compares two quantities, part to part, such as 2 boys to 3 girls. A fraction compares a part to the whole, so the boys are 2/5 of the group."),
       ("How do I write a ratio as 1:n?", "Divide both sides by the first number. 4:10 becomes 1:2.5.")],
 related=["fraction", "percent", "gcf", "scientific"])

# ---------------- Slope ----------------
tool(id="slope", slug="slope-calculator", cat="Math", name="Slope Calculator",
 short="Slope calculator", desc="Slope, equation and distance from two points.",
 title="Slope Calculator – Find the Slope from Two Points | Numbrik",
 meta="Find the slope between two points, with the line equation in slope-intercept form, the y-intercept, angle, distance and midpoint. Shows the working.",
 lede="Enter two points to find the slope of the line through them, the equation in slope-intercept form (y = mx + b), the y-intercept, the angle of the line, the distance between the points and the midpoint.",
 steps=["Enter the first point as x₁ and y₁.", "Enter the second point as x₂ and y₂.",
        "Read the slope, the equation of the line and the working underneath."],
 how="""<p>Slope measures how steep a line is: how much y changes for each step in x, often called rise over run. Subtract the y-values, subtract the x-values in the same order, and divide. A positive slope rises from left to right, a negative slope falls, zero is flat and an undefined slope is a vertical line.</p>
<p>Once the slope m is known, the y-intercept b comes from putting one point into y = mx + b. The angle is the inverse tangent of the slope, and the distance between the points uses the Pythagorean theorem.</p>""",
 formula="m = (y₂ − y₁) ÷ (x₂ − x₁)\nb = y₁ − m × x₁        y = mx + b\nd = √((x₂ − x₁)² + (y₂ − y₁)²)\nangle = tan⁻¹(m)",
 example="<p>For the points (2, 3) and (6, 11), the slope is (11 − 3) ÷ (6 − 2) = 8 ÷ 4 = <strong>2</strong>. The intercept is 3 − 2 × 2 = −1, so the line is <strong>y = 2x − 1</strong>. The points are √(4² + 8²) ≈ 8.944 apart and the line rises at about 63.43°.</p>",
 extra="<h3>Reading a slope</h3>" + tbl(["Slope", "Line", "Grade"], [("0", "Flat", "0%"), ("0.05", "Gentle ramp", "5%"), ("1/12 ≈ 0.083", "Maximum US wheelchair ramp (ADA)", "8.3%"), ("1", "45° diagonal", "100%"), ("−2", "Falls 2 for every 1 across", "−200%"), ("Undefined", "Vertical", "—")]) +
 "<p>Road and ramp grades are slope written as a percent: multiply the slope by 100.</p>",
 faqs=[("What is the slope formula?", "m = (y₂ − y₁) ÷ (x₂ − x₁). It's the change in y divided by the change in x, or rise over run."),
       ("What does an undefined slope mean?", "The two points have the same x-value, so the line is vertical and the run is zero. You can't divide by zero."),
       ("How do I find the slope from an equation?", "Rearrange it to y = mx + b. The number in front of x is the slope. For 2y = 6x + 4, divide by 2 to get y = 3x + 2, so the slope is 3."),
       ("How do I convert slope to a percent grade?", "Multiply by 100. A slope of 0.06 is a 6% grade.")],
 related=["triangle", "quadratic", "scientific", "fraction"])

# ---------------- Protein ----------------
lb180 = 180 * 0.45359237
tool(id="protein", slug="protein-calculator", cat="Health", name="Protein Calculator",
 short="Protein calculator", desc="How much protein you need a day.",
 title="Protein Calculator – How Much Protein a Day? | Numbrik",
 meta="How much protein do you need a day? Enter your weight and goal for a daily target in grams, per meal, for general health, exercise, muscle gain or fat loss.",
 lede="Work out how many grams of protein to eat each day based on your weight and goal, from the minimum for general health to the higher amounts used for building muscle or keeping it while losing fat.",
 steps=["Enter your weight in pounds or kilograms.", "Choose the goal that fits you best.",
        "Read your daily protein range in grams, and how much that is per meal over three or four meals."],
 how="""<p>Protein needs are set per kilogram of body weight. The US and Canadian recommended dietary allowance (RDA) is 0.8 g per kg, the amount that covers the basic needs of almost all healthy adults. It is a minimum, not an ideal.</p>
<p>Position stands from sports nutrition groups, including the International Society of Sports Nutrition, suggest 1.4–2.0 g per kg for people who exercise regularly, and up to about 2.2 g per kg when building muscle or eating in a calorie deficit. Older adults are often advised to aim for 1.0–1.2 g per kg to slow muscle loss.</p>""",
 formula="Protein (g/day) = weight (kg) × grams per kg\nweight (kg) = weight (lb) × 0.4536",
 example=f"<p>A 180 lb (81.6 kg) person lifting weights to build muscle needs about 1.6–2.2 g per kg, which is <strong>{lb180*1.6:.0f}–{lb180*2.2:.0f} g of protein a day</strong>, or roughly {lb180*1.6/4:.0f}–{lb180*2.2/4:.0f} g at each of four meals. The RDA minimum for the same person is {lb180*0.8:.0f} g.</p>",
 extra="<h3>Protein targets by goal</h3>" + tbl(["Goal", "Grams per kg", "Grams per lb", "180 lb person"], [
   ("Minimum for health (RDA)", "0.8", "0.36", f"{lb180*.8:.0f} g"), ("Adults 65+", "1.0–1.2", "0.45–0.55", f"{lb180*1:.0f}–{lb180*1.2:.0f} g"),
   ("Regular exercise", "1.2–1.6", "0.55–0.73", f"{lb180*1.2:.0f}–{lb180*1.6:.0f} g"), ("Building muscle", "1.6–2.2", "0.73–1.0", f"{lb180*1.6:.0f}–{lb180*2.2:.0f} g"),
   ("Losing fat, keeping muscle", "1.8–2.4", "0.82–1.1", f"{lb180*1.8:.0f}–{lb180*2.4:.0f} g")]) +
 "<h3>Protein in common foods</h3>" + tbl(["Food", "Protein"], [("Chicken breast, 4 oz (113 g) cooked", "about 35 g"), ("Greek yogurt, 1 cup", "about 20 g"), ("Large egg", "about 6 g"), ("Lentils, 1 cup cooked", "about 18 g"), ("Tofu, firm, ½ cup", "about 20 g"), ("Whey protein, 1 scoop", "20–25 g")]),
 faqs=[("How much protein do I need a day?", "At least 0.8 g per kg of body weight (0.36 g per lb). If you exercise regularly, 1.2–1.6 g per kg is a common target, and 1.6–2.2 g per kg if you're trying to build muscle."),
       ("Can you eat too much protein?", "For healthy adults, intakes up to about 2 g per kg are considered safe. People with kidney disease should follow their doctor's advice."),
       ("Should I use my goal weight or current weight?", "If you have a lot of weight to lose, using your goal weight or a healthy weight gives a more sensible target."),
       ("Is it better to spread protein through the day?", "Yes. Research on muscle building suggests 20–40 g per meal across three or four meals works better than one large serving.")],
 related=["macro", "calorie", "bmr", "bodyfat"])

# ---------------- One rep max ----------------
e1 = 225 * (1 + 5 / 30); b1 = 225 * 36 / 32; l1 = 225 * 5 ** 0.1
PCT = [(100, 1), (95, 2), (93, 3), (90, 4), (87, 5), (85, 6), (83, 7), (80, 8), (77, 9), (75, 10), (70, 12)]
tool(id="onerm", slug="one-rep-max-calculator", cat="Health", name="One Rep Max Calculator",
 short="One rep max (1RM)", desc="Estimate your 1RM from a set of reps.",
 title="One Rep Max Calculator – Estimate Your 1RM | Numbrik",
 meta="Estimate your one rep max (1RM) for bench press, squat and deadlift from the weight and reps you lifted, with Epley, Brzycki and a percentage chart.",
 lede="Estimate the most weight you could lift for a single rep (your one rep max, or 1RM) from a set you've already done, without having to test a true max. Works for bench press, squat, deadlift and other lifts.",
 steps=["Enter the weight you lifted.", "Enter how many clean reps you did, from 1 to 12.",
        "Read your estimated 1RM and the training weights for each percentage of it."],
 how="""<p>The main estimate uses the Epley formula, the one most gym apps use. The Brzycki and Lombardi formulas are shown alongside so you can see the spread. All of them are most accurate between 2 and 10 reps. Above about 12 reps, endurance plays a bigger part and the estimates become unreliable.</p>
<p>Use a set taken close to failure with good form. The percentage chart turns your 1RM into training weights: strength programmes often work at 80–90% for 3–6 reps, and muscle-building programmes at 65–80% for 8–12 reps.</p>""",
 formula="Epley:    1RM = w × (1 + reps ÷ 30)\nBrzycki:  1RM = w × 36 ÷ (37 − reps)\nLombardi: 1RM = w × reps^0.10",
 example=f"<p>Bench pressing 225 lb for 5 reps gives an Epley estimate of 225 × (1 + 5/30) = <strong>{e1:.1f} lb</strong>. Brzycki gives {b1:.1f} lb and Lombardi {l1:.1f} lb. For sets of 8, about 80% of the Epley estimate, or roughly {e1*.8:.0f} lb, is a sensible working weight.</p>",
 extra="<h3>Percent of 1RM and typical reps</h3>" + tbl(["% of 1RM", "Approx. reps", "With a 1RM of 262.5"], [(f"{p}%", r, f"{e1*p/100:.1f}") for p, r in PCT]),
 faqs=[("How accurate is a 1RM calculator?", "Usually within a few percent for sets of 2–10 reps. Accuracy drops with higher reps and varies between people and lifts."),
       ("Which formula is best?", "Epley and Brzycki give almost the same answer at around 10 reps. Epley reads a little higher at low reps. Take the average if you're unsure."),
       ("Is it safe to test a true one rep max?", "It can be with good technique, a proper warm-up and a spotter or safety bars. Estimating from a set of 3–5 reps is safer for most people."),
       ("Can I use it for any exercise?", "It works best for big barbell lifts such as bench press, squat, deadlift and overhead press.")],
 related=["protein", "macro", "calorie", "bodyfat"])

# ---------------- Macro ----------------
SPL = [("Balanced", 50, 20, 30), ("High protein", 40, 30, 30), ("Low carb", 25, 35, 40), ("Keto", 5, 25, 70)]
tool(id="macro", slug="macro-calculator", cat="Health", name="Macro Calculator",
 short="Macro calculator", desc="Split daily calories into carbs, protein and fat.",
 title="Macro Calculator – Carbs, Protein & Fat in Grams | Numbrik",
 meta="Free macro calculator. Turn your daily calories into grams of carbs, protein and fat for a balanced, high-protein, low-carb or keto diet, or set your own split.",
 lede="Split your daily calorie target into grams of carbohydrate, protein and fat. Pick a balanced, high-protein, low-carb or keto split, or enter your own percentages.",
 steps=["Enter your daily calories. If you don't know them, use the calorie calculator first.",
        "Choose a split, or pick Custom and enter your own percentages.", "Read the grams of each macro per day and per meal."],
 how="""<p>Each macronutrient has a fixed energy value: protein and carbohydrate have 4 calories per gram and fat has 9. The calculator takes the share of calories for each macro and divides by its calories per gram.</p>
<p>The US Dietary Guidelines set acceptable ranges of 45–65% of calories from carbohydrate, 10–35% from protein and 20–35% from fat. Higher-protein splits are popular for weight loss because protein keeps you fuller and helps keep muscle, and keto diets cut carbohydrate to around 5% or less.</p>""",
 formula="Carbs (g) = calories × carb% ÷ 4\nProtein (g) = calories × protein% ÷ 4\nFat (g) = calories × fat% ÷ 9",
 example="<p>On 2,200 calories a day with a balanced 50/20/30 split you'd eat 2,200 × 0.50 ÷ 4 = <strong>275 g of carbs</strong>, 2,200 × 0.20 ÷ 4 = <strong>110 g of protein</strong> and 2,200 × 0.30 ÷ 9 ≈ <strong>73 g of fat</strong>.</p>",
 extra="<h3>Grams per day at 2,200 calories</h3>" + tbl(["Split", "Carbs / protein / fat", "Carbs", "Protein", "Fat"], [(n, f"{c}/{p}/{f}%", f"{2200*c/400:.0f} g", f"{2200*p/400:.0f} g", f"{2200*f/900:.0f} g") for n, c, p, f in SPL]),
 faqs=[("What should my macros be?", "There's no single best split. A balanced 50/20/30 fits the US guidelines. For fat loss, many people raise protein to 25–35% so they stay full and keep muscle."),
       ("How many calories are in a gram of each macro?", "Protein and carbohydrate have 4 calories per gram. Fat has 9. Alcohol has 7."),
       ("Do I need to count macros to lose weight?", "No. Total calories matter most for weight loss. Tracking macros helps make sure you eat enough protein while you cut."),
       ("What are keto macros?", "A typical keto split is about 70–75% fat, 20–25% protein and 5% carbohydrate, usually under 50 g of carbs a day.")],
 related=["calorie", "protein", "bmr", "bmi"])

# ---------------- Pace ----------------
RACES = [("5K", 5), ("10K", 10), ("Half marathon", 21.0975), ("Marathon", 42.195)]
def hms(sec):
    sec = round(sec); h, r = divmod(sec, 3600); m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"
tool(id="pace", slug="pace-calculator", cat="Health", name="Pace Calculator",
 short="Running pace", desc="Running pace per mile or km, speed and finish times.",
 title="Pace Calculator – Running Pace per Mile & km | Numbrik",
 meta="Enter distance and time to get your running pace per mile and per km, speed in mph and km/h, and finish times for a 5K, 10K, half and full marathon.",
 lede="Enter how far you ran and how long it took to get your pace per mile and per kilometre, your speed, and the finish time for a 5K, 10K, half marathon and marathon at the same pace.",
 steps=["Enter the distance and choose miles or kilometres, or tap a race distance.", "Enter your time in hours, minutes and seconds.",
        "Read your pace, speed and race finish times at that pace."],
 how="""<p>Pace is time divided by distance. It's the usual way runners measure effort, because it tells you directly how long each mile or kilometre takes. Speed is the opposite: distance divided by time.</p>
<p>The race table shows how long each distance takes if you hold the same pace. Most people slow down over longer races, so treat the half marathon and marathon times as best cases. A common rule of thumb, Riegel's formula, predicts a little more than double the time each time the distance doubles, about 4% extra.</p>""",
 formula="Pace = time ÷ distance\nSpeed = distance ÷ time\n1 mile = 1.609344 km",
 example="<p>A 5K (3.107 miles) in 28:00 is a pace of <strong>9:01 per mile</strong> or <strong>5:36 per km</strong>, a speed of about 6.66 mph (10.7 km/h). Held for a full marathon, that pace finishes in about 3:56:18.</p>",
 extra="<h3>Finish times by pace</h3>" + tbl(["Pace per mile", "Pace per km", "5K", "10K", "Half", "Marathon"],
   [(f"{p}:00", hms(p * 60 / 1.609344), *(hms(p * 60 / 1.609344 * d) for _, d in RACES)) for p in (7, 8, 9, 10, 11, 12)]),
 faqs=[("What is a good running pace?", "For recreational runners a pace of 9 to 12 minutes per mile (5:35 to 7:30 per km) is typical on easy runs. Racing pace is faster."),
       ("How do I convert pace per mile to pace per km?", "Divide the pace per mile by 1.609. A 10:00 mile is 6:13 per km."),
       ("How long is a half marathon?", "13.1 miles, or 21.0975 km. A full marathon is 26.2 miles, or 42.195 km."),
       ("Can I use it for walking or cycling?", "Yes. Pace and speed work the same way for any activity.")],
 related=["calorie", "bmr", "hours", "convert"])

# ---------------- Average ----------------
tool(id="average", slug="average-calculator", cat="Math", name="Average Calculator",
 short="Average calculator", desc="Mean, median, mode and range of a list of numbers.",
 title="Average Calculator – Mean, Median, Mode & Range | Numbrik",
 meta="Free average calculator. Paste a list of numbers to get the mean, median, mode, range, sum, count and geometric mean, with the working shown.",
 lede="Paste or type a list of numbers to find the average (mean), plus the median, mode, range, sum, count and geometric mean.",
 steps=["Type or paste your numbers. Separate them with commas, spaces or new lines.", "The mean, median and mode update as you type.",
        "Use the copy button to grab the result."],
 how="""<p>The mean is what most people call the average: add the numbers and divide by how many there are. The median is the middle value once the numbers are sorted, or the mean of the two middle values when there's an even count. The mode is the value that appears most often, and a list can have more than one mode or none.</p>
<p>The median is better than the mean when a few very large or very small values would pull the mean away from typical values, as with house prices or incomes. For a weighted average, such as a grade where tests count more than homework, use the grade calculator.</p>""",
 formula="Mean = sum ÷ count\nMedian = middle value of the sorted list\nMode = most frequent value\nRange = largest − smallest",
 example="<p>For 4, 8, 15, 16, 23 and 42, the sum is 108 and there are 6 numbers, so the mean is 108 ÷ 6 = <strong>18</strong>. The median is the mean of 15 and 16, which is <strong>15.5</strong>. No number repeats, so there is no mode. The range is 42 − 4 = 38.</p>",
 extra="<h3>Mean, median or mode?</h3>" + tbl(["Use", "When"], [("Mean", "Values are spread fairly evenly with no extreme outliers, such as test scores"), ("Median", "A few extreme values would distort the mean, such as incomes or home prices"), ("Mode", "You want the most common answer, such as shoe sizes or survey choices")]),
 faqs=[("How do I calculate an average?", "Add all the numbers together, then divide by how many numbers there are. The average of 2, 4 and 9 is 15 ÷ 3 = 5."),
       ("What's the difference between mean and median?", "The mean is the sum divided by the count. The median is the middle value. In 1, 2, 3, 4 and 100, the mean is 22 but the median is 3."),
       ("Can there be more than one mode?", "Yes. If two or more values tie for the most appearances, they are all modes."),
       ("How do I average percentages?", "If each percentage is based on the same total, average them normally. If not, add up the parts and the totals and divide.")],
 related=["stdev", "grade", "percent", "scientific"])

# ---------------- Right triangle ----------------
tool(id="triangle", slug="right-triangle-calculator", cat="Math", name="Right Triangle Calculator",
 short="Right triangle / Pythagorean", desc="Hypotenuse, sides, angles and area of a right triangle.",
 title="Right Triangle & Pythagorean Theorem Calculator | Numbrik",
 meta="Right triangle and Pythagorean theorem calculator. Enter any two sides to find the third side, the hypotenuse, both angles, the area and the perimeter.",
 lede="Enter any two sides of a right triangle to find the third side with the Pythagorean theorem, both acute angles, the area and the perimeter. Leave the side you want to find blank.",
 steps=["Enter two of the three sides: legs a and b, or the hypotenuse c (the longest side, opposite the right angle).",
        "Leave the side you want to find empty.", "Read the missing side, the angles, the area and the perimeter."],
 how="""<p>In a right triangle, the square of the hypotenuse equals the sum of the squares of the other two sides: a² + b² = c². Given both legs, take the square root of a² + b². Given a leg and the hypotenuse, the missing leg is the square root of c² − a².</p>
<p>The angles come from trigonometry. Angle A, opposite side a, is the inverse sine of a ÷ c, and angle B is 90° minus A. The area is half the product of the two legs.</p>""",
 formula="a² + b² = c²\nc = √(a² + b²)     a = √(c² − b²)\nA = sin⁻¹(a ÷ c)   B = 90° − A\nArea = a × b ÷ 2",
 example="<p>Legs of 5 and 12 give a hypotenuse of √(25 + 144) = √169 = <strong>13</strong>. The angles are about 22.62° and 67.38°, the area is 30 and the perimeter is 30.</p>",
 extra="<h3>Pythagorean triples</h3><p>These whole-number right triangles are handy for checking that a corner is square, for example measuring 3 ft and 4 ft from a corner and checking the diagonal is 5 ft.</p>" +
 tbl(["a", "b", "c"], [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (6, 8, 10), (9, 12, 15)]),
 faqs=[("What is the Pythagorean theorem?", "In any right triangle, a² + b² = c², where c is the hypotenuse, the side opposite the right angle."),
       ("How do I find the hypotenuse?", "Square both legs, add them and take the square root. For legs 6 and 8: 36 + 64 = 100, and √100 = 10."),
       ("How do I find a missing leg?", "Subtract the square of the known leg from the square of the hypotenuse and take the square root. With c = 10 and a = 6: 100 − 36 = 64, so b = 8."),
       ("Does it work for triangles without a right angle?", "No. For other triangles use the law of cosines: c² = a² + b² − 2ab·cos C.")],
 related=["slope", "scientific", "sqft", "quadratic"])

# ---------------- Quadratic ----------------
tool(id="quadratic", slug="quadratic-formula-calculator", cat="Math", name="Quadratic Formula Calculator",
 short="Quadratic formula", desc="Solve ax² + bx + c = 0 with steps.",
 title="Quadratic Formula Calculator with Steps | Numbrik",
 meta="Solve any quadratic equation with the quadratic formula. Shows the discriminant, real or complex roots, the vertex and the factored form, with the working.",
 lede="Solve a quadratic equation in the form ax² + bx + c = 0. Enter a, b and c to get both roots (real or complex), the discriminant, the vertex of the parabola and the working.",
 steps=["Write your equation as ax² + bx + c = 0, moving everything to one side.", "Enter a, b and c. Use negative numbers where the sign is minus.",
        "Read the roots, the discriminant and the vertex, and follow the working."],
 how="""<p>The quadratic formula solves any equation of the form ax² + bx + c = 0 where a is not zero. The discriminant, b² − 4ac, tells you what kind of answers to expect: positive means two different real roots, zero means one repeated root, and negative means two complex roots.</p>
<p>The roots are where the parabola y = ax² + bx + c crosses the x-axis. Its turning point, the vertex, is at x = −b ÷ 2a. When a is positive the parabola opens upward and the vertex is a minimum.</p>""",
 formula="x = (−b ± √(b² − 4ac)) ÷ 2a\nDiscriminant D = b² − 4ac\nVertex: x = −b ÷ 2a",
 example="<p>For x² − 5x + 6 = 0, a = 1, b = −5 and c = 6. The discriminant is 25 − 24 = 1, so x = (5 ± 1) ÷ 2, giving <strong>x = 3</strong> and <strong>x = 2</strong>. The factored form is (x − 3)(x − 2) = 0.</p><p>For 2x² + 4x − 6 = 0 the discriminant is 16 + 48 = 64, and the roots are x = 1 and x = −3.</p>",
 extra="<h3>What the discriminant tells you</h3>" + tbl(["Discriminant", "Roots", "Graph"], [("Positive", "Two different real roots", "Crosses the x-axis twice"), ("Zero", "One repeated real root", "Touches the x-axis at the vertex"), ("Negative", "Two complex roots", "Doesn't touch the x-axis")]),
 faqs=[("What is the quadratic formula?", "x = (−b ± √(b² − 4ac)) ÷ 2a. It gives both solutions of ax² + bx + c = 0."),
       ("What if a is zero?", "Then the equation is linear, bx + c = 0, and the single answer is x = −c ÷ b."),
       ("What are complex roots?", "When the discriminant is negative, the square root of a negative number is imaginary. The roots are written as p ± qi, where i = √−1."),
       ("Can I solve by factoring instead?", "If the roots are whole numbers or simple fractions, factoring is quicker. The formula always works.")],
 related=["slope", "scientific", "fraction", "triangle"])

# ---------------- CD ----------------
CDT = [(6, "6 months"), (12, "1 year"), (18, "18 months"), (24, "2 years"), (36, "3 years"), (60, "5 years")]
tool(id="cd", slug="cd-calculator", cat="Money", name="CD Calculator",
 short="CD calculator", desc="Interest earned on a certificate of deposit.",
 title="CD Calculator – CD Interest & APY | Numbrik",
 meta="Free CD calculator. Enter your deposit, APY and term to see the interest earned and the balance at maturity, with a comparison of 6-month to 5-year CDs.",
 lede="See how much a certificate of deposit (CD) will earn. Enter the deposit, the APY and the term to get the interest earned and the balance at maturity, plus the same deposit over other common terms.",
 steps=["Enter the amount you'll deposit.", "Enter the APY the bank quotes and the term in months.",
        "Read the interest earned and the balance when the CD matures."],
 how="""<p>Banks quote CD rates as an annual percentage yield (APY), which already includes the effect of compounding. That makes the maths simple: the balance grows by the APY each year, so after t years it is deposit × (1 + APY)ᵗ, whether the bank compounds daily or monthly.</p>
<p>Interest on a CD is usually taxable in the year it's credited, even if you can't withdraw it until maturity. Withdrawing early normally costs a penalty, often a few months of interest, so pick a term you won't need to break.</p>""",
 formula="Balance = deposit × (1 + APY)^(months ÷ 12)\nInterest = balance − deposit",
 example=f"<p>$10,000 in a 1-year CD at 4.50% APY earns <strong>$450</strong>. In an 18-month CD at the same APY it earns about <strong>${10000*1.045**1.5-10000:,.2f}</strong>.</p>",
 extra="<h3>$10,000 at 4.00% APY</h3>" + tbl(["Term", "Interest", "Balance"], [(n, f"${10000*1.04**(m/12)-10000:,.2f}", f"${10000*1.04**(m/12):,.2f}") for m, n in CDT]) +
 "<h3>CD vs high-yield savings</h3><p>A CD locks in a rate for the whole term, which helps if rates fall. A high-yield savings account lets you withdraw any time, but its rate can change. Many savers build a CD ladder, splitting money across several terms so part of it matures every year.</p>",
 faqs=[("What is APY?", "Annual percentage yield is the rate you earn in a year including compounding. A 4.50% APY means $10,000 grows to $10,450 after one year."),
       ("How is CD interest calculated?", "Balance = deposit × (1 + APY)^(years). Subtract the deposit to get the interest."),
       ("Are CDs safe?", "In the US, CDs at FDIC-insured banks and NCUA-insured credit unions are covered up to $250,000 per depositor, per institution, per ownership category."),
       ("What happens when a CD matures?", "You usually have a grace period of 7–10 days to withdraw or move the money. Otherwise many banks renew it automatically at the current rate.")],
 related=["compound", "percent", "loan", "salestax"])

BYID.update({t["id"]: t for t in T})
