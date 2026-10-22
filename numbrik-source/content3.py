"""Grade and final grade calculators (added October 22, 2026)."""
from content import tool, T, BYID

rows = [("Homework", 92, 20), ("Quizzes", 85, 15), ("Midterm exam", 78, 25), ("Project", 88, 15), ("Participation", 100, 5)]
sw = sum(s * w for _, s, w in rows); ws = sum(w for *_, w in rows); g = sw / ws
def letter(x):
    for cut, l in [(97,"A+"),(93,"A"),(90,"A−"),(87,"B+"),(83,"B"),(80,"B−"),(77,"C+"),(73,"C"),(70,"C−"),(67,"D+"),(63,"D"),(60,"D−")]:
        if x >= cut: return l
    return "F"
need = lambda c, w, t: (t - c * (1 - w)) / w
LETTER = """<h3>Common US letter grade scale</h3><div class="tbl"><table><thead><tr><th>Letter</th><th>Percent</th><th>Letter</th><th>Percent</th></tr></thead><tbody>
<tr><td>A+</td><td>97–100</td><td>C+</td><td>77–79</td></tr><tr><td>A</td><td>93–96</td><td>C</td><td>73–76</td></tr><tr><td>A−</td><td>90–92</td><td>C−</td><td>70–72</td></tr>
<tr><td>B+</td><td>87–89</td><td>D+</td><td>67–69</td></tr><tr><td>B</td><td>83–86</td><td>D</td><td>63–66</td></tr><tr><td>B−</td><td>80–82</td><td>D−</td><td>60–62</td></tr>
<tr><td></td><td></td><td>F</td><td>Below 60</td></tr></tbody></table></div><p>Schools set their own cut-offs, so check your syllabus. Some use 90/80/70/60 with no plus or minus grades.</p>"""

tool(id="grade", slug="grade-calculator", cat="Students", name="Grade Calculator",
 short="Grade", desc="Weighted class grade from your assignments and categories.",
 title="Grade Calculator – Weighted Class Grade | Numbrik",
 meta="Calculate your weighted class grade from assignments, tests and categories. See your percentage, letter grade and how much of the course is still to come.",
 lede="Work out your current grade in a class from weighted assignments and categories, such as homework, quizzes, exams and projects. See your percentage and letter grade straight away.",
 steps=["Add a row for each assignment or category in your syllabus.","Enter your score as a percentage and the weight of that item.","Read your current grade and letter grade. Use 'What do I need on the final?' to plan ahead."],
 how="""<p>Most classes give each category a weight, such as homework 20% and exams 50%. Your grade is a weighted average: each score is multiplied by its weight, the results are added up, and the total is divided by the sum of the weights.</p>
<p>The weights you enter don't need to reach 100%. If only 75% of the course has been graded, the calculator divides by 75, which gives your grade on the work marked so far. That is the same number most online gradebooks show. Change any score to see how a better or worse result would move your grade.</p>
<p>If your class uses points instead of weights, divide your total points by the total points possible and multiply by 100. For example, 412 out of 450 points is 91.6%.</p>""",
 formula="Grade = Σ(score × weight) ÷ Σ weight\nScore % = points earned ÷ points possible × 100",
 example=f"<p>The example class has homework at 92% (weight 20), quizzes at 85% (15), a midterm at 78% (25), a project at 88% (15) and participation at 100% (5). That adds up to {sw:,} weighted points over {ws} weight, a current grade of <strong>{g:.1f}%</strong>, which is a <strong>{letter(g)}</strong>. The final exam, worth the remaining {100-ws}%, is still to come.</p>",
 extra=LETTER,
 faqs=[("How do I calculate my grade with weights?","Multiply each score by its weight, add the results and divide by the total weight. With homework 90% at 40% weight and tests 80% at 60%, the grade is (90 × 40 + 80 × 60) ÷ 100 = 84%."),
       ("What if the weights don't add up to 100?","Then part of the course hasn't been graded yet. Dividing by the weights entered gives your current grade on the work done so far."),
       ("How do I turn points into a percentage?","Divide the points you earned by the points possible and multiply by 100. 45 out of 50 is 90%."),
       ("What grade do I need on my final?","Use the final grade calculator. Enter your current grade, the final's weight and the grade you want.")],
 related=["finalgrade","gpa","percent","lcm"])

ex1 = need(84, .25, 85); ex2 = need(84, .25, 90)
fg_rows = "".join(f"<tr><td>{c}%</td><td>{'Not reachable' if need(c,.3,90)>100 else f'{need(c,.3,90):.1f}%'}</td><td>{need(c,.3,80):.1f}%</td><td>{max(0,need(c,.3,70)):.1f}%</td></tr>" for c in [95, 90, 85, 80, 75, 70])
tool(id="finalgrade", slug="final-grade-calculator", cat="Students", name="Final Grade Calculator",
 short="Final grade", desc="The score you need on the final exam to reach your target grade.",
 title="Final Grade Calculator – What Do I Need on My Final? | Numbrik",
 meta="Find out what score you need on your final exam to get an A, B, C or pass the class. Enter your current grade, the final's weight and your target grade.",
 lede="Find out what score you need on your final exam to reach the grade you want, whether that's keeping an A or making sure you pass.",
 steps=["Enter your current grade in the class.","Enter how much the final exam is worth, from your syllabus.","Enter the grade you want, or tap A, B, C or D. Read the score you need, and the table for every letter."],
 how="""<p>Your final grade is a weighted mix of your current grade and the final exam. If the final is worth 25%, your current grade counts for the other 75%. The calculator solves for the exam score that brings the mix up to your target.</p>
<p>If the answer is above 100%, the target can't be reached even with a perfect exam, unless there is extra credit. If it is 0% or less, you already have that grade secured. The result also shows what your grade would be with 100%, 70% or 0% on the final, which helps you plan how much to study.</p>""",
 formula="Needed on final = (target − current × (1 − final weight)) ÷ final weight",
 example=f"<p>With a current grade of 84% and a final worth 25%, you need <strong>{ex1:.0f}%</strong> on the final to finish with 85%. To get a 90% (an A), you would need {ex2:.0f}%, which isn't possible without extra credit.</p>",
 extra=f"""<h3>Score needed on a final worth 30%</h3><div class="tbl"><table><thead><tr><th>Current grade</th><th>For 90% (A)</th><th>For 80% (B)</th><th>For 70% (C)</th></tr></thead><tbody>{fg_rows}</tbody></table></div>""",
 faqs=[("What do I need on my final to get an A?", f"It depends on your current grade and the final's weight. With 88% now and a final worth 20%, you need {need(88,.2,90):.0f}% to reach 90%."),
       ("What do I need on my final to pass?",f"Set the target to your school's passing grade, often 60% or 70%. With 65% now and a final worth 30%, you need about {need(65,.3,60):.0f}% to finish on 60%."),
       ("How much is my final exam worth?","Check the course syllabus or ask your teacher. Finals are often worth between 15% and 40% of the grade."),
       ("What does 'Not reachable' mean?","Even 100% on the final wouldn't bring your grade up to the target. Look for extra credit, or aim for the next grade down.")],
 related=["grade","gpa","percent","age"])

BYID.update({t["id"]: t for t in T})
