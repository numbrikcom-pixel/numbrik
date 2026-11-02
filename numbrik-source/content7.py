"""Seasonal: Thanksgiving turkey calculator (added November 2, 2026). Times follow the USDA Food Safety and Inspection Service charts."""
from content import tool, T, BYID

def tbl(head, rows):
    return ('<div class="tbl"><table><thead><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")

ROAST = [("4 to 8 lb (breast)", "1½ to 3¼ hours", "Not recommended"), ("8 to 12 lb", "2¾ to 3 hours", "3 to 3½ hours"), ("12 to 14 lb", "3 to 3¾ hours", "3½ to 4 hours"),
         ("14 to 18 lb", "3¾ to 4¼ hours", "4 to 4¼ hours"), ("18 to 20 lb", "4¼ to 4½ hours", "4¼ to 4¾ hours"), ("20 to 24 lb", "4½ to 5 hours", "4¾ to 5¼ hours")]
THAW = [(f"{w} lb", (lambda a, b: f"{a} days" if a == b else f"{a}–{b} days")(max(1, round(w/5)), round(w/4 + 0.49)), f"{w*0.5:g} hours") for w in (8, 12, 16, 20, 24)]

tool(id="turkey", slug="turkey-calculator", cat="Home", name="Turkey Calculator",
 short="Turkey calculator", desc="Turkey size, thawing and roasting time.",
 title="Turkey Calculator – Size, Thawing & Cooking Time | Numbrik",
 meta="Plan your Thanksgiving turkey: how big a turkey to buy per person, how long to thaw it, how long to roast it at 325°F, and when to start for your dinner time.",
 lede="Plan your Thanksgiving or Christmas turkey. Enter the number of guests or the turkey's weight and your dinner time to see how big a bird to buy, when to start thawing it, how long to roast it, and when it needs to go in the oven.",
 steps=["Enter how many people you're feeding, or the weight of the turkey you already have.",
        "Choose stuffed or unstuffed, and fridge or cold-water thawing.",
        "Enter when you want to eat. The timeline shows when to start thawing and when the turkey goes in the oven."],
 how="""<p>Roasting times follow the USDA Food Safety and Inspection Service chart for a fully thawed turkey in a 325°F (163°C) oven. They're a guide: ovens vary, so start checking an hour before the shortest time. The turkey is done when a food thermometer reads 165°F (74°C) in the thickest part of the breast, the innermost part of the thigh and the innermost part of the wing, and in the centre of any stuffing.</p>
<p>For thawing, the USDA allows about 24 hours in the fridge for every 4 to 5 pounds, or 30 minutes per pound in cold water, changing the water every 30 minutes and cooking the turkey straight away afterwards. Never thaw a turkey on the counter. Plan on 1 to 1½ pounds of whole turkey per person; the larger amount leaves leftovers. The timeline adds 30 minutes for the turkey to rest before carving.</p>""",
 formula="Size: guests × 1–1.5 lb\nFridge thaw: 1 day per 4–5 lb\nCold-water thaw: 30 min per lb\nDone at 165°F (74°C) · rest 20–30 min",
 example="<p>For 12 guests with leftovers, buy a turkey of about 12 × 1.5 = <strong>18 lb</strong>. Thawing it in the fridge takes 4 to 5 days, so for Thursday dinner put it in the fridge by Saturday or Sunday. Unstuffed, an 18 lb turkey roasts for about <strong>4¼ to 4½ hours</strong> at 325°F, so for dinner at 5:00 PM it goes in the oven at about 12:00 PM.</p>",
 extra="<h3>Roasting times at 325°F (USDA)</h3>" + tbl(["Turkey weight", "Unstuffed", "Stuffed"], ROAST) +
 "<h3>Thawing times</h3>" + tbl(["Weight", "In the fridge", "In cold water"], THAW) +
 "<h3>How big a turkey for how many people?</h3>" + tbl(["Guests", "Just dinner (1 lb each)", "With leftovers (1.5 lb each)"], [(n, f"{n} lb", f"{n*1.5:g} lb") for n in (4, 6, 8, 10, 12, 16, 20)]) +
 "<p>For a boneless turkey breast, allow about half a pound per person.</p>",
 faqs=[("How long does it take to cook a turkey?", "At 325°F an unstuffed turkey takes roughly 13–15 minutes per pound: about 3 hours for 12 lb and 4¼–4½ hours for 18–20 lb. Always check it reaches 165°F."),
       ("How long does a turkey take to thaw?", "About 1 day in the fridge for every 4–5 lb, so 4–5 days for a 20 lb bird. In cold water, 30 minutes per pound."),
       ("What temperature should a turkey be cooked to?", "165°F (74°C), measured in the thickest part of the breast, the inner thigh and the wing, and in the centre of the stuffing."),
       ("Can I cook a turkey that's still frozen?", "Yes, it's safe, but it takes about 50% longer, and you can't remove the giblets until it has partly cooked."),
       ("How big a turkey do I need?", "About 1 lb per person for one meal, or 1½ lb per person if you want leftovers.")],
 related=["days", "hours", "convert", "calorie"])

BYID.update({t["id"]: t for t in T})
