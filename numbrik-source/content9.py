"""Shoe size converter (added November 8, 2026). Formulas from foot length (Omni Calculator's published formulas):
US men = 3 × in − 22, US women = 3 × in − 21, UK = 3 × in − 23, EU = 1.27 × (UK + 23) + 2 (= 1.5 × cm + 2), US kids = 3 × in − 9.67, UK kids = 3 × in − 10."""
from content import tool, T, BYID

def tbl(head, rows):
    return ('<div class="tbl"><table><thead><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")
h = lambda x: f"{round(x * 2) / 2:g}"
def adult(inch):
    return dict(m=3 * inch - 22, w=3 * inch - 21, uk=3 * inch - 23, eu=1.27 * (3 * inch - 23 + 23) + 2, cm=inch * 2.54, inch=inch)
def kid(us):  # US kids size (toddler/little kid 0-13.5, then youth 1-7 = 14-20 on the kids scale)
    inch = (us + 9.67) / 3
    return dict(inch=inch, cm=inch * 2.54, uk=3 * inch - 10, eu=1.27 * (3 * inch - 23 + 23) + 2)

men = [adult((s + 22) / 3) for s in [x / 2 for x in range(12, 31)]]
women = [adult((s + 21) / 3) for s in [x / 2 for x in range(8, 27)]]
kids = [(f"{s:g}" if s < 14 else f"{s - 13:g}Y", kid(s)) for s in [x / 2 for x in range(4, 41)]]

tool(id="shoe", slug="shoe-size-converter", cat="Converters", name="Shoe Size Converter",
 short="Shoe size converter", desc="Convert shoe sizes between US, UK and EU.",
 title="Shoe Size Converter – US, UK, EU Size Charts | Numbrik",
 meta="Convert shoe sizes between US, UK and EU for men, women and kids, or find your size from foot length in inches or cm. Includes full size charts.",
 lede="Convert a shoe size between US, UK and European (EU) sizing for men, women and kids, or measure your foot and find your size in every system. Full conversion charts are below.",
 steps=["Choose what you know: a shoe size in one system, or your foot length.", "Pick men's, women's or kids' sizes and enter the size or length.",
        "Read your size in US, UK and EU, plus the matching foot length in inches and centimetres."],
 how="""<p>Shoe size systems all count length, but in different units and from different starting points. US and UK sizes go up by one size for every barleycorn (a third of an inch), while European sizes use the Paris point, two-thirds of a centimetre. The converter works from foot length, using these formulas: US men = 3 × foot length in inches − 22, US women = 3 × inches − 21, UK = 3 × inches − 23, and EU = 1.27 × (UK + 23) + 2. Results are rounded to the nearest half size.</p>
<p>Brands don't size identically. Nike, Adidas and New Balance can differ by half a size or more, and some EU sizes are sold in thirds. Treat the result as a starting point and check the brand's own chart, especially for running shoes, boots and sandals.</p>""",
 formula="US men = 3 × foot (in) − 22\nUS women = 3 × foot (in) − 21\nUK = 3 × foot (in) − 23\nEU = 1.27 × (UK + 23) + 2\nfoot (in) = foot (cm) ÷ 2.54",
 example="<p>A men's US 10 fits a foot of about 10.67 inches (27.1 cm). That's a UK 9, an EU 42.5 and a women's US 11. A women's US 8 is a UK 6 and an EU 39.</p>",
 extra="<h3>How to measure your foot</h3><ol><li>Stand on a sheet of paper with your heel against a wall, wearing the socks you'll wear with the shoes.</li><li>Mark the tip of your longest toe, then measure from the wall to the mark.</li><li>Measure both feet, in the evening when feet are largest, and use the longer one.</li></ol>"
 "<h3>Men's shoe size chart</h3>" + tbl(["US men", "UK", "EU", "US women", "Inches", "CM"], [(h(d["m"]), h(d["uk"]), h(d["eu"]), h(d["w"]), f'{d["inch"]:.2f}', f'{d["cm"]:.1f}') for d in men]) +
 "<h3>Women's shoe size chart</h3>" + tbl(["US women", "UK", "EU", "US men", "Inches", "CM"], [(h(d["w"]), h(d["uk"]), h(d["eu"]), h(d["m"]), f'{d["inch"]:.2f}', f'{d["cm"]:.1f}') for d in women]) +
 "<h3>Kids' shoe size chart</h3><p>US kids' sizes run from 0 to 13.5, then restart as youth sizes 1Y to 7Y.</p>" + tbl(["US kids", "UK kids", "EU", "Inches", "CM"], [(lab, h(d["uk"]) if d["uk"] < 13.75 else f'{h(d["uk"] - 13)} (youth)', h(d["eu"]), f'{d["inch"]:.2f}', f'{d["cm"]:.1f}') for lab, d in kids]),
 faqs=[("How do I convert women's to men's shoe sizes?", "Subtract 1 to 1.5 from the women's US size. A women's 9 is about a men's 7.5 to 8. This chart uses a difference of 1; some brands, such as Nike, use 1.5."),
       ("Is UK shoe size the same as US?", "No. A UK size is about one size smaller than US men's and two sizes smaller than US women's. A men's UK 9 is a US 10."),
       ("What is a size 42 in US shoes?", "EU 42 is about a men's US 9.5 or a women's US 10.5. Depending on the brand it can be half a size either way."),
       ("What's the difference between kids' and youth sizes?", "US kids' sizes go up to 13.5, then start again at 1Y for bigger kids. A 1Y is the next size up from a kids' 13.5."),
       ("Should I size up for running shoes?", "Many runners go up half a size, because feet swell during long runs. Leave about a thumb's width between your longest toe and the front of the shoe.")],
 related=["convert", "sqft", "bmi", "pace"])

BYID.update({t["id"]: t for t in T})
if "shoe" not in BYID["convert"]["related"]: BYID["convert"]["related"] = ["shoe"] + BYID["convert"]["related"][:3]
