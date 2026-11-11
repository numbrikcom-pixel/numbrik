"""CalculatorSoup sitemap gap (Nov 11, 2026): tools where searchers click through because Google shows no built-in widget
(word counter, character counter, time to decimal, percent change), plus exact-answer tables on the sales tax page, which
already ranks 5–8 for long-tail queries like "8% sales tax on 35" (GSC, 28 days to Nov 9)."""
from content import tool, T, BYID

def tbl(head, rows):
    return ('<div class="tbl"><table><thead><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")
usd = lambda x: f"${x:,.2f}"

# ---------- Word counter ----------
tool(id="wordcount", slug="word-counter", cat="Students", name="Word Counter",
 short="Word counter", desc="Count words, characters, sentences and reading time.",
 title="Word Counter – Words, Characters & Reading Time | Numbrik",
 meta="Free word counter: paste your text to count words, characters, sentences and paragraphs, with reading time, speaking time and top keywords. Private: nothing is uploaded.",
 lede="Paste or type your text to count words, characters, sentences and paragraphs instantly. You also get the reading time, speaking time and most-used keywords, which helps with essays, blog posts, speeches and word limits.",
 steps=["Paste or type your text into the box.", "The counts update as you type.", "Check the word count, characters, sentences and paragraphs.", "Use the reading and speaking time to plan a talk, video or article."],
 how="""<p>A word is counted each time a run of letters or numbers starts after a space or punctuation mark, so “don't”, “well-known” and “2026” each count as one word. Characters are counted with and without spaces, and every emoji or accented letter counts as one character. Sentences end at a full stop, question mark, exclamation mark or ellipsis, and paragraphs are separated by a blank line.</p>
<p>Reading time uses 238 words per minute, the average silent reading speed for adults found in a 2019 review of 190 studies. Speaking time uses 140 words per minute, a comfortable pace for a presentation or video. Your text is counted in your browser and is never uploaded or stored.</p>""",
 formula="Reading time = words ÷ 238 per minute\nSpeaking time = words ÷ 140 per minute\nAverage word length = letters ÷ words",
 example="<p>A <strong>1,500-word</strong> blog post takes about 6 minutes 18 seconds to read (1,500 ÷ 238) and about 10 minutes 43 seconds to read aloud (1,500 ÷ 140).</p>",
 extra="<h3>How many pages is my word count?</h3><p>Approximate pages in 12-point Times New Roman or Arial with 1-inch margins.</p>" +
 tbl(["Words", "Single-spaced", "Double-spaced", "Reading time", "Speaking time"],
   [(f"{w:,}", f"{w / 500:g} page{'s' if w != 500 else ''}", f"{w / 250:g} pages", f"{w / 238:.0f} min" if w >= 238 else "Under 1 min", f"{w / 140:.0f} min") for w in (250, 500, 750, 1000, 1500, 2000, 2500, 3000, 5000)]) +
 "<h3>Typical word counts</h3>" + tbl(["Type of writing", "Usual length"],
   [("College application essay (Common App)", "Up to 650 words"), ("High school essay", "300–1,000 words"), ("Blog post", "1,000–2,500 words"), ("Cover letter", "250–400 words"),
    ("Short story", "1,000–7,500 words"), ("Novel", "70,000–100,000 words"), ("5-minute speech", "About 650–750 words")]),
 faqs=[("How many words is a 5-minute speech?", "About 650 to 750 words at a normal speaking pace of 130 to 150 words per minute."),
       ("How many pages is 1,000 words?", "About 2 pages single-spaced or 4 pages double-spaced, in a 12-point font with 1-inch margins."),
       ("Does the word counter count numbers and hyphenated words?", "Yes. Numbers like 2026 count as one word, and hyphenated words like “well-known” count as one word, as in Microsoft Word and Google Docs."),
       ("Is my text saved anywhere?", "No. The counting happens in your browser. Nothing you type is sent to Numbrik or stored.")],
 related=["charcount", "grade", "gpa", "average"])

# ---------- Character counter ----------
LIM = [("X (Twitter) post, standard account", "280"), ("SMS text message", "160 (70 if it contains emoji or non-Latin letters)"), ("Google search result title", "About 60 (cut off by pixel width)"),
       ("Meta description shown by Google", "About 150–160"), ("YouTube video title", "100"), ("Instagram caption", "2,200"), ("LinkedIn post", "3,000"), ("TikTok caption", "4,000")]
tool(id="charcount", slug="character-counter", cat="Students", name="Character Counter",
 short="Character counter", desc="Count characters with and without spaces, against common limits.",
 title="Character Counter – With & Without Spaces | Numbrik",
 meta="Count characters with and without spaces, letters and words as you type, and see how your text fits X, SMS, Instagram, YouTube and Google title limits.",
 lede="Type or paste text to count characters with and without spaces, letters and words. Bars show how much room you have left for X posts, text messages, Instagram captions, YouTube titles and Google titles and descriptions.",
 steps=["Paste or type your text.", "Read the character count with and without spaces.", "Check the bars to see if you're inside each platform's limit.", "Trim the text until the bar you need is no longer red."],
 how="""<p>Every letter, number, space, punctuation mark and line break counts as a character. The count without spaces leaves out spaces, tabs and line breaks. Each emoji and accented letter counts as a single character here, which matches what most people expect, although some platforms count certain emoji as two.</p>
<p>Text messages are the main exception: a standard SMS holds 160 characters, but if it includes any emoji or non-Latin letters the phone switches to a different encoding and each message holds only 70. Google cuts off titles and descriptions by pixel width rather than a fixed number, so the limits shown are typical rather than exact.</p>""",
 formula="Characters = every letter, digit, space and symbol\nWithout spaces = characters − spaces, tabs and line breaks",
 example="<p>“Hello, world!” has <strong>13 characters</strong>, 12 without the space, 10 letters and 2 words.</p>",
 extra="<h3>Character limits by platform</h3>" + tbl(["Where", "Character limit"], LIM),
 faqs=[("Do spaces count as characters?", "Yes. Spaces, punctuation and line breaks all count toward limits like X's 280 characters. Use the “without spaces” count only when a form specifically asks for it."),
       ("How many characters is a text message?", "160 for a standard SMS. If it contains emoji or letters outside the basic Latin alphabet, the limit drops to 70 per message, and longer texts are split into parts."),
       ("How many characters can a tweet have?", "280 for a standard X account. Paid subscribers can post longer texts, but only the first 280 characters show in the timeline before “Show more”."),
       ("How long should a meta description be?", "About 150 to 160 characters. Google cuts longer descriptions by pixel width, so put the most important words first.")],
 related=["wordcount", "password", "random", "convert"])

# ---------- Time to decimal ----------
tool(id="timedec", slug="time-to-decimal-calculator", cat="Work & pay", name="Time to Decimal Calculator",
 short="Time to decimal", desc="Convert hours and minutes to decimal hours and back.",
 title="Time to Decimal Calculator – Hours & Minutes | Numbrik",
 meta="Convert hours and minutes to decimal hours for payroll and timesheets, or decimal hours back to hours and minutes. 7:45 = 7.75 hours. Includes a full minutes chart.",
 lede="Convert time in hours and minutes to decimal hours for payroll, invoices and timesheets, or turn decimal hours back into hours and minutes. A chart of every minute from 1 to 59 is below.",
 steps=["Choose time → decimal or decimal → time.", "Enter the hours and minutes (and seconds if you need them), or the decimal hours.", "Read the result, plus the total minutes and a 2-decimal figure for payroll."],
 how="""<p>To convert minutes to a decimal, divide them by 60. 45 minutes is 45 ÷ 60 = 0.75 hours, so 7 hours 45 minutes is 7.75 hours. Seconds are divided by 3,600. To go the other way, multiply the decimal part by 60: 8.4 hours is 8 hours and 0.4 × 60 = 24 minutes.</p>
<p>Payroll systems usually round decimal hours to two places, and some employers round time to the nearest 5 or 15 minutes (0.08 or 0.25 hours). A common mistake is reading 7.30 as 7 hours 30 minutes: in decimal it's 7 hours 18 minutes, while 7 hours 30 minutes is 7.5.</p>""",
 formula="Decimal hours = hours + minutes ÷ 60 + seconds ÷ 3,600\nMinutes = (decimal hours − whole hours) × 60",
 example="<p>A shift of <strong>8 hours 20 minutes</strong> is 8 + 20 ÷ 60 = <strong>8.33 hours</strong> (8.333…). At $22 an hour that's 8.333 × $22 = $183.33.</p>",
 extra="<h3>Minutes to decimal hours chart</h3>" + tbl(["Minutes", "Decimal", "Minutes", "Decimal", "Minutes", "Decimal"],
   [sum(([str(m), f"{m / 60:.2f}"] for m in (r, r + 20, r + 40)), []) for r in range(1, 21)]) +
 "<h3>Common shift lengths</h3>" + tbl(["Hours and minutes", "Decimal hours"], [(f"{h} h {m:02d} min", f"{h + m / 60:.2f}") for h, m in ((4, 15), (4, 30), (6, 45), (7, 30), (7, 45), (8, 0), (8, 15), (8, 30), (9, 45), (10, 30), (12, 15))]),
 faqs=[("What is 7 hours and 45 minutes in decimal?", "7.75 hours, because 45 minutes ÷ 60 = 0.75."),
       ("What is 0.3 hours in minutes?", "18 minutes. Multiply the decimal by 60: 0.3 × 60 = 18."),
       ("Is 7.30 hours the same as 7 hours 30 minutes?", "No. 7.30 decimal hours is 7 hours 18 minutes. 7 hours 30 minutes is 7.5 hours."),
       ("How do I convert minutes to decimal for payroll?", "Divide the minutes by 60 and round to two places. 10 minutes is 0.17, 15 minutes is 0.25, 20 minutes is 0.33 and 50 minutes is 0.83.")],
 related=["timecard", "hours", "salary", "paycheck"])

# ---------- Percent change ----------
tool(id="pctchange", slug="percent-change-calculator", cat="Math", name="Percent Change Calculator",
 short="Percent change", desc="Percentage increase or decrease between two numbers.",
 title="Percent Change Calculator – % Increase & Decrease | Numbrik",
 meta="Find the percentage increase or decrease between two numbers, or increase or decrease a number by a percentage. Shows the formula, the change and the multiplier.",
 lede="Work out the percentage change between an old value and a new one, for prices, salaries, grades, sales or stock prices. You can also increase or decrease a number by a percentage, and see what it takes to get back to the start.",
 steps=["Choose percent change, increase by %, or decrease by %.", "Enter the old and new values, or the value and the percentage.", "Read the result: positive is an increase, negative a decrease."],
 how="""<p>Percent change compares the difference to the starting value: subtract the old value from the new one, divide by the old value, and multiply by 100. Going from 80 to 100 is (100 − 80) ÷ 80 × 100 = 25%. Going from 100 back to 80 is (80 − 100) ÷ 100 × 100 = −20%, which is why an increase and a decrease of the same size don't cancel out.</p>
<p>Percent difference is a different measure, used when neither value is the “starting” one: it divides the gap by the average of the two values. And when a rate itself changes, say from 4% to 5%, that's a rise of 1 percentage point but a 25% increase.</p>""",
 formula="Percent change = (new − old) ÷ |old| × 100\nIncrease by p% = value × (1 + p ÷ 100)\nDecrease by p% = value × (1 − p ÷ 100)",
 example="<p>A stock goes from <strong>$80 to $100</strong>: (100 − 80) ÷ 80 × 100 = <strong>+25%</strong>. If it then falls back to $80, that's (80 − 100) ÷ 100 × 100 = <strong>−20%</strong>, not −25%.</p>",
 extra="<h3>Increase and decrease don't cancel out</h3>" + tbl(["Change", "Then", "Net result"],
   [(f"+{a}%", f"−{a}%", f"{((1 + a / 100) * (1 - a / 100) - 1) * 100:+.2f}%") for a in (10, 20, 25, 50)]) +
 "<h3>Recovering from a loss</h3>" + tbl(["Drop", "Gain needed to get back"], [(f"−{d}%", f"+{d / (100 - d) * 100:.1f}%") for d in (10, 20, 25, 30, 40, 50, 75)]),
 faqs=[("How do I calculate percentage increase?", "Subtract the old number from the new number, divide by the old number and multiply by 100. From 50 to 65: (65 − 50) ÷ 50 × 100 = 30%."),
       ("How do I calculate percentage decrease?", "Use the same formula; the result is negative. From 200 to 150: (150 − 200) ÷ 200 × 100 = −25%, a 25% decrease."),
       ("What's the difference between percent change and percentage points?", "Percentage points are the simple difference between two percentages. A rate rising from 4% to 5% is up 1 percentage point, which is a 25% increase in the rate."),
       ("Why does a 50% loss need a 100% gain to recover?", "Because the gain is measured from the smaller number. $100 falls 50% to $50; getting back to $100 means adding $50, which is 100% of $50.")],
 related=["percent", "discount", "raise", "average"])

# ---------- Sales tax: exact-answer tables for long-tail queries ----------
st = BYID["salestax"]
RATES = (5, 6, 7, 8, 8.25, 8.875, 9, 9.5, 10)
AMTS = (10, 20, 30, 35, 40, 50, 70, 90, 100, 120, 140, 150, 170, 200, 250, 300, 450, 500, 1000, 1400, 1600, 1800, 2000, 4000, 5000)
st["extra"] = st.get("extra", "") + ("<h3>Sales tax on common amounts</h3><p>Tax to add at common US rates. The total is the amount plus the tax: "
  "8% sales tax on $35 is $2.80, so you pay $37.80. Most state and local combined rates fall between 5% and 10%.</p>" +
  tbl(["Amount"] + [f"{r:g}%" for r in RATES], [[usd(a)] + [usd(round(a * r / 100 + 1e-9, 2)) for r in RATES] for a in AMTS]) +
  "<h3>Total price including sales tax</h3>" +
  tbl(["Amount"] + [f"+{r:g}%" for r in RATES], [[usd(a)] + [usd(round(a * (1 + r / 100) + 1e-9, 2)) for r in RATES] for a in (10, 20, 35, 50, 100, 120, 200, 500, 1000)]))
st["faqs"] = st["faqs"] + [
  ("How much is 8% sales tax on $35?", "$2.80, for a total of $37.80. Multiply 35 × 0.08 = 2.80."),
  ("What is 120 plus 9.5% tax?", "$131.40. The tax is 120 × 0.095 = $11.40."),
  ("How do I work out sales tax on a price?", "Multiply the price by the tax rate as a decimal. For 7% tax on $140, 140 × 0.07 = $9.80, so the total is $149.80.")]

BYID.update({t["id"]: t for t in T})
