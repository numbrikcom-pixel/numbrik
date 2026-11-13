"""German-language versions (/de/) of ten Numbrik calculators (Nov 13, 2026).
Each page reuses the English page's calculator (same JS, translated in the browser by the DE layer in app.js, EUR and de-DE
number format) with original German copy written for German searchers, hreflang-linked to its English twin."""
import html, math, statistics
from datetime import date

E = html.escape
def n(x, d=2, strip=True):  # German number format: 1.234,56
    s = f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s.rstrip("0").rstrip(",") if strip and d and "," in s else s
def eur(x): return n(x, 2, False) + " €"
def tbl(head, rows):
    return ('<div class="tbl"><table><thead><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")

def msj(sex, kg, cm, age): return 10 * kg + 6.25 * cm - 5 * age + (5 if sex == "m" else -161)
def cpd(K, p, y): return K * (1 + p / 100) ** y

PAGES = {
 "percent": dict(slug="prozentrechner", name="Prozentrechner", short="Prozentrechner",
  title="Prozentrechner – Prozente einfach berechnen | Numbrik",
  meta="Prozentrechner: Prozentwert, Prozentsatz und prozentuale Veränderung sofort berechnen. Mit Formeln, Beispielen, Prozenttabelle und Mehrwertsteuer.",
  lede="Berechnen Sie Prozentwert, Prozentsatz oder die prozentuale Veränderung zwischen zwei Zahlen – sofort und kostenlos. Unten finden Sie die Formeln, eine Prozenttabelle und wie Sie 19 % Mehrwertsteuer rechnen.",
  steps=["Wählen Sie, was Sie berechnen möchten: X % von Y, X ist wie viel % von Y, oder die Veränderung in %.", "Geben Sie die beiden Zahlen ein.", "Das Ergebnis erscheint sofort, inklusive Summe und Rest."],
  how="""<p>Die Prozentrechnung arbeitet mit drei Größen: dem <strong>Grundwert</strong> (G, das Ganze), dem <strong>Prozentwert</strong> (W, der Anteil) und dem <strong>Prozentsatz</strong> (p, der Anteil in Prozent). Kennen Sie zwei davon, lässt sich die dritte berechnen. 15 % von 240 sind 240 × 15 ÷ 100 = 36.</p>
<p>Für die prozentuale Veränderung teilen Sie die Differenz durch den Ausgangswert: Steigt ein Preis von 80 € auf 100 €, sind das (100 − 80) ÷ 80 × 100 = +25 %. Fällt er von 100 € zurück auf 80 €, sind es −20 % – Zunahme und Abnahme heben sich also nicht auf.</p>""",
  formula="Prozentwert W = G × p ÷ 100\nProzentsatz p = W ÷ G × 100\nGrundwert G = W × 100 ÷ p\nVeränderung = (neu − alt) ÷ alt × 100",
  example="<p><strong>Wie viel sind 15 % von 240?</strong> 240 × 15 ÷ 100 = <strong>36</strong>. Addiert ergibt das 276, abgezogen 204. <strong>Wie viel Prozent sind 45 von 180?</strong> 45 ÷ 180 × 100 = <strong>25 %</strong>.</p>",
  extra="<h3>Prozenttabelle</h3>" + tbl(["Prozent"] + [n(g, 0) for g in (50, 100, 250, 500, 1000)], [[f"{p} %"] + [n(g * p / 100) for g in (50, 100, 250, 500, 1000)] for p in (1, 3, 5, 7, 10, 15, 19, 20, 25, 30, 50, 75)]) +
   "<h3>Mehrwertsteuer berechnen (19 % und 7 %)</h3><p>Vom Netto- zum Bruttopreis: Netto × 1,19 (bzw. × 1,07 beim ermäßigten Satz). Die enthaltene Mehrwertsteuer aus einem Bruttobetrag: Brutto × 19 ÷ 119.</p>" +
   tbl(["Netto", "MwSt. 19 %", "Brutto (19 %)", "MwSt. 7 %", "Brutto (7 %)"], [(eur(x), eur(x * .19), eur(x * 1.19), eur(x * .07), eur(x * 1.07)) for x in (10, 50, 100, 250, 500, 1000)]),
  faqs=[("Wie berechnet man Prozent?", "Multiplizieren Sie den Grundwert mit dem Prozentsatz und teilen Sie durch 100. 20 % von 150 sind 150 × 20 ÷ 100 = 30."),
        ("Wie rechne ich aus, wie viel Prozent eine Zahl ist?", "Teilen Sie den Anteil durch das Ganze und multiplizieren Sie mit 100. 45 von 180 sind 45 ÷ 180 × 100 = 25 %."),
        ("Was ist der Unterschied zwischen Prozent und Prozentpunkten?", "Prozentpunkte sind die einfache Differenz zweier Prozentsätze. Steigt ein Zinssatz von 4 % auf 5 %, ist das ein Plus von 1 Prozentpunkt, aber eine Steigerung um 25 %."),
        ("Wie berechne ich 19 % Mehrwertsteuer?", "Netto × 0,19 ergibt die Steuer, Netto × 1,19 den Bruttopreis. Aus einem Bruttobetrag erhalten Sie die enthaltene Steuer mit Brutto × 19 ÷ 119: Bei 119 € sind das 19 €.")],
  qa=("Wie berechnet man Prozent?", "Prozentwert = Grundwert × Prozentsatz ÷ 100. 15 % von 240 sind 240 × 15 ÷ 100 = 36. Um herauszufinden, wie viel Prozent eine Zahl ist, teilen Sie den Anteil durch das Ganze und multiplizieren mit 100.")),

 "bmi": dict(slug="bmi-rechner", name="BMI-Rechner", short="BMI-Rechner",
  title="BMI-Rechner – Body-Mass-Index berechnen | Numbrik",
  meta="BMI-Rechner für Erwachsene: Body-Mass-Index aus Größe und Gewicht berechnen, mit WHO-Einteilung, Normalgewicht für Ihre Größe und BMI-Tabelle.",
  lede="Berechnen Sie Ihren Body-Mass-Index aus Körpergröße und Gewicht. Der Rechner zeigt Ihre Kategorie nach WHO und den Gewichtsbereich, der für Ihre Größe als Normalgewicht gilt.",
  steps=["Geben Sie Ihre Größe in Zentimetern ein.", "Geben Sie Ihr Gewicht in Kilogramm ein.", "Lesen Sie Ihren BMI, Ihre Kategorie und Ihr Normalgewicht ab."],
  how="""<p>Der BMI setzt das Körpergewicht ins Verhältnis zur Körpergröße: Gewicht in Kilogramm geteilt durch die Größe in Metern zum Quadrat. Die Weltgesundheitsorganisation (WHO) teilt Erwachsene so ein: unter 18,5 Untergewicht, 18,5 bis 24,9 Normalgewicht, 25 bis 29,9 Übergewicht (Präadipositas) und ab 30 Adipositas.</p>
<p>Der BMI ist ein schneller Richtwert, kein Diagnosewerkzeug. Er unterscheidet nicht zwischen Muskeln und Fett und berücksichtigt weder Alter noch Fettverteilung. Für Kinder und Jugendliche gelten Perzentilkurven statt fester Grenzen.</p>""",
  formula="BMI = Gewicht (kg) ÷ Größe (m)²\nNormalgewicht = 18,5 bis 24,9 × Größe (m)²",
  example=f"<p>Eine Person mit <strong>1,75 m</strong> und <strong>72 kg</strong>: 72 ÷ (1,75 × 1,75) = <strong>{n(72 / 1.75 ** 2, 1)}</strong>. Das ist Normalgewicht; bei 1,75 m reicht der Bereich von {n(18.5 * 1.75 ** 2, 1)} bis {n(24.9 * 1.75 ** 2, 1)} kg.</p>",
  extra="<h3>BMI-Einteilung nach WHO</h3>" + tbl(["BMI", "Kategorie"], [("unter 18,5", "Untergewicht"), ("18,5 – 24,9", "Normalgewicht"), ("25 – 29,9", "Übergewicht (Präadipositas)"), ("30 – 34,9", "Adipositas Grad I"), ("35 – 39,9", "Adipositas Grad II"), ("ab 40", "Adipositas Grad III")]) +
   "<h3>BMI-Tabelle: Normalgewicht nach Größe</h3>" + tbl(["Größe", "Normalgewicht (BMI 18,5–24,9)", "Übergewicht ab (BMI 25)"], [(f"{c} cm", f"{n(18.5 * (c / 100) ** 2, 1)} – {n(24.9 * (c / 100) ** 2, 1)} kg", f"{n(25 * (c / 100) ** 2, 1)} kg") for c in range(150, 201, 5)]),
  faqs=[("Welcher BMI ist normal?", "Bei Erwachsenen gilt ein BMI von 18,5 bis 24,9 als Normalgewicht. Für ältere Menschen halten manche Fachleute einen etwas höheren Wert für unbedenklich."),
        ("Ist der BMI für Frauen und Männer gleich?", "Ja, die WHO-Grenzen gelten für beide Geschlechter. Frauen haben im Durchschnitt mehr Körperfett bei gleichem BMI, was der BMI aber nicht abbildet."),
        ("Kann ich den BMI-Rechner für Kinder nutzen?", "Nein. Für Kinder und Jugendliche werden alters- und geschlechtsabhängige Perzentilkurven verwendet. Fragen Sie dazu die Kinderärztin oder den Kinderarzt."),
        ("Wie aussagekräftig ist der BMI?", "Er ist ein grober Richtwert. Sportliche Menschen mit viel Muskelmasse können einen hohen BMI haben, ohne zu viel Fett zu tragen. Bauchumfang oder Körperfettanteil sagen oft mehr aus.")],
  qa=("Wie berechnet man den BMI?", "Teilen Sie Ihr Gewicht in Kilogramm durch Ihre Größe in Metern zum Quadrat. Bei 72 kg und 1,75 m: 72 ÷ 3,0625 = 23,5. Ein BMI von 18,5 bis 24,9 gilt bei Erwachsenen als Normalgewicht.")),

 "calorie": dict(slug="kalorienrechner", name="Kalorienrechner", short="Kalorienrechner",
  title="Kalorienrechner – Kalorienbedarf pro Tag berechnen | Numbrik",
  meta="Kalorienrechner: Ihren täglichen Kalorienbedarf zum Halten, Abnehmen oder Zunehmen berechnen – aus Alter, Geschlecht, Größe, Gewicht und Aktivität.",
  lede="Wie viele Kalorien brauchen Sie am Tag? Geben Sie Alter, Geschlecht, Größe, Gewicht und Aktivität ein und erhalten Sie Ihren Grundumsatz, Ihren Gesamtbedarf und Zielwerte zum Abnehmen oder Zunehmen.",
  steps=["Wählen Sie Ihr Geschlecht und geben Sie Alter, Größe und Gewicht ein.", "Wählen Sie Ihr Aktivitätsniveau für eine normale Woche.", "Lesen Sie Ihren Bedarf zum Halten des Gewichts und die Werte zum Ab- oder Zunehmen ab."],
  how="""<p>Zuerst wird der <strong>Grundumsatz</strong> berechnet – die Energie, die Ihr Körper in völliger Ruhe verbraucht – mit der Mifflin-St-Jeor-Formel, die in Studien zu den genauesten Schätzformeln für Erwachsene gehört. Dieser Wert wird mit einem Aktivitätsfaktor (PAL) von 1,2 für überwiegend sitzende Tätigkeit bis 1,9 für körperliche Arbeit plus Training multipliziert. Das Ergebnis ist Ihr <strong>Gesamtumsatz</strong>.</p>
<p>Ein Kilogramm Körperfett entspricht grob 7.000 kcal. Ein Defizit von etwa 500 kcal pro Tag führt deshalb anfangs zu rund 0,5 kg Gewichtsverlust pro Woche. Mit sinkendem Gewicht sinkt auch der Bedarf – rechnen Sie nach einigen Kilo neu.</p>""",
  formula="Grundumsatz Männer = 10 × kg + 6,25 × cm − 5 × Alter + 5\nGrundumsatz Frauen = 10 × kg + 6,25 × cm − 5 × Alter − 161\nGesamtumsatz = Grundumsatz × Aktivitätsfaktor",
  example=f"<p>Eine <strong>30-jährige Frau</strong>, 165 cm und 65 kg, mit mäßigem Sport (Faktor 1,55): Grundumsatz = {n(msj('f', 65, 165, 30), 0)} kcal, Gesamtumsatz ≈ <strong>{n(round(msj('f', 65, 165, 30) * 1.55, -1), 0)} kcal</strong> pro Tag. Zum Abnehmen von rund 0,5 kg pro Woche wären es etwa {n(round(msj('f', 65, 165, 30) * 1.55 - 500, -1), 0)} kcal.</p>",
  extra="<h3>Kalorienbedarf: Beispiele nach Aktivität (30 Jahre)</h3>" + tbl(["Person", "Grundumsatz", "sitzend (1,2)", "mäßig aktiv (1,55)", "sehr aktiv (1,725)"],
     [(lab, *[n(round(msj(s, kg, cm, 30) * f, -1), 0) + " kcal" for f in (1, 1.2, 1.55, 1.725)]) for lab, s, kg, cm in (("Frau, 165 cm, 60 kg", "f", 60, 165), ("Frau, 170 cm, 75 kg", "f", 75, 170), ("Mann, 180 cm, 75 kg", "m", 75, 180), ("Mann, 185 cm, 90 kg", "m", 90, 185))]) +
   "<h3>Kalorien pro Gramm</h3>" + tbl(["Nährstoff", "kcal pro Gramm"], [("Eiweiß", "4"), ("Kohlenhydrate", "4"), ("Fett", "9"), ("Alkohol", "7")]),
  faqs=[("Wie viele Kalorien sollte ich am Tag essen, um abzunehmen?", "Etwa 300 bis 500 kcal weniger als Ihr Gesamtumsatz. Das entspricht anfangs rund 0,25 bis 0,5 kg pro Woche. Dauerhaft deutlich unter dem Grundumsatz zu essen, sollte nur ärztlich begleitet geschehen."),
        ("Was ist der Unterschied zwischen Grundumsatz und Gesamtumsatz?", "Der Grundumsatz ist der Energieverbrauch in völliger Ruhe. Der Gesamtumsatz enthält zusätzlich Alltag, Bewegung und Sport und liegt meist 20 bis 90 % darüber."),
        ("Wie viele Kalorien braucht eine Frau oder ein Mann pro Tag?", "Erwachsene Frauen brauchen meist etwa 1.800 bis 2.400 kcal, Männer etwa 2.200 bis 3.000 kcal – je nach Größe, Gewicht, Alter und Aktivität."),
        ("Wie genau ist der Kalorienrechner?", "Formeln liefern Schätzwerte, die im Einzelfall um einige Hundert Kalorien abweichen können. Beobachten Sie Ihr Gewicht über zwei bis drei Wochen und passen Sie die Menge an.")],
  qa=("Wie viele Kalorien brauche ich am Tag?", "Ihr Bedarf ist der Grundumsatz (nach Mifflin-St Jeor) mal einem Aktivitätsfaktor von 1,2 bis 1,9. Eine 30-jährige Frau mit 165 cm und 65 kg und mäßigem Sport braucht etwa 2.120 kcal; rund 500 kcal weniger führen zu etwa 0,5 kg Abnahme pro Woche.")),

 "compound": dict(slug="zinseszinsrechner", name="Zinseszinsrechner", short="Zinseszinsrechner",
  title="Zinseszinsrechner – Sparplan mit Zinseszins | Numbrik",
  meta="Zinseszinsrechner mit Sparrate: Berechnen Sie, wie Ihr Geld mit Zinseszins wächst – Startkapital, monatliche Einzahlung, Zinssatz und Laufzeit.",
  lede="Sehen Sie, wie Ihr Erspartes mit Zinseszins wächst. Geben Sie Startkapital, monatliche Sparrate, Zinssatz und Laufzeit ein und erhalten Sie Endkapital, Zinserträge und eine Übersicht pro Jahr.",
  steps=["Geben Sie Ihr Startkapital und die monatliche Sparrate ein.", "Tragen Sie den jährlichen Zinssatz und die Laufzeit in Jahren ein.", "Wählen Sie, wie oft die Zinsen gutgeschrieben werden (jährlich, vierteljährlich, monatlich oder täglich).", "Lesen Sie Endkapital, Einzahlungen und Zinserträge ab."],
  how="""<p>Beim Zinseszins werden die Zinsen dem Kapital gutgeschrieben und in den folgenden Perioden selbst mitverzinst. Deshalb wächst das Vermögen nicht gleichmäßig, sondern immer schneller. Je länger die Laufzeit und je häufiger die Zinsgutschrift, desto größer der Effekt.</p>
<p>In Deutschland sind Zinserträge oberhalb des <strong>Sparerpauschbetrags</strong> von 1.000 € pro Jahr (2.000 € für Verheiratete) steuerpflichtig: Die Abgeltungsteuer beträgt 25 % zuzüglich Solidaritätszuschlag, zusammen 26,375 %, plus gegebenenfalls Kirchensteuer. Der Rechner zeigt Werte vor Steuern.</p>""",
  formula="Endkapital Kₙ = K₀ × (1 + p ÷ 100)ⁿ\nK₀ = Startkapital, p = Zinssatz, n = Jahre\nVerdopplungszeit ≈ 72 ÷ Zinssatz",
  example=f"<p><strong>10.000 €</strong> zu <strong>3 %</strong> mit jährlicher Zinsgutschrift wachsen in 10 Jahren auf 10.000 × 1,03¹⁰ = <strong>{eur(cpd(10000, 3, 10))}</strong>. Ohne Zinseszins wären es nur 13.000 €.</p>",
  extra="<h3>Endkapital von 10.000 € (ohne Sparrate)</h3>" + tbl(["Zinssatz", "5 Jahre", "10 Jahre", "20 Jahre", "30 Jahre"], [(f"{n(p, 1)} %", *[eur(cpd(10000, p, y)) for y in (5, 10, 20, 30)]) for p in (1, 2, 3, 4, 5, 7)]) +
   "<h3>72er-Regel: Wann verdoppelt sich mein Geld?</h3>" + tbl(["Zinssatz", "Faustregel (72 ÷ p)", "Genau"], [(f"{p} %", f"{n(72 / p, 1)} Jahre", f"{n(math.log(2) / math.log(1 + p / 100), 1)} Jahre") for p in (1, 2, 3, 4, 6, 8)]),
  faqs=[("Was ist der Zinseszins?", "Zinsen auf bereits erhaltene Zinsen. Werden Zinsen nicht ausgezahlt, sondern dem Kapital gutgeschrieben, verzinsen sie sich im nächsten Jahr mit – das Kapital wächst exponentiell."),
        ("Wie lautet die Zinseszinsformel?", "Kₙ = K₀ × (1 + p/100)ⁿ. Bei unterjähriger Verzinsung teilen Sie den Zinssatz durch die Zahl der Perioden pro Jahr und erhöhen n entsprechend."),
        ("Wie lange dauert es, bis sich mein Geld verdoppelt?", "Mit der 72er-Regel: 72 geteilt durch den Zinssatz. Bei 3 % dauert es etwa 24 Jahre, bei 6 % etwa 12 Jahre."),
        ("Muss ich Zinsen versteuern?", "In Deutschland fallen auf Kapitalerträge über dem Sparerpauschbetrag (1.000 € bzw. 2.000 € für Verheiratete) 25 % Abgeltungsteuer plus Solidaritätszuschlag und gegebenenfalls Kirchensteuer an. Banken führen sie meist automatisch ab.")],
  qa=("Wie berechnet man den Zinseszins?", "Mit Kₙ = K₀ × (1 + p/100)ⁿ. 10.000 € zu 3 % wachsen in 10 Jahren auf 13.439,16 €. Mit einer monatlichen Sparrate wird jede Einzahlung ab ihrem Datum mitverzinst.")),

 "ratio": dict(slug="dreisatz-rechner", name="Dreisatz-Rechner", short="Dreisatz-Rechner",
  title="Dreisatz-Rechner – Dreisatz einfach lösen | Numbrik",
  meta="Dreisatz-Rechner: fehlenden Wert (A : B = C : D) sofort berechnen, Verhältnisse kürzen – mit Erklärung zu (anti)proportionalem Dreisatz.",
  lede="Lösen Sie den Dreisatz in Sekunden: Geben Sie drei Werte ein, und der Rechner bestimmt den vierten. Außerdem kürzt er Verhältnisse und zeigt sie als Bruch und Dezimalzahl.",
  steps=["Tragen Sie die zwei bekannten zusammengehörigen Werte als A und B ein.", "Tragen Sie den neuen Wert als C ein.", "Lesen Sie den gesuchten Wert D ab."],
  how="""<p>Beim <strong>proportionalen Dreisatz</strong> gilt: je mehr, desto mehr. Kosten 3 Brötchen 4 €, kosten 12 Brötchen 4 € ÷ 3 × 12 = 16 €. Allgemein gilt A : B = C : D, also D = B × C ÷ A. Genau das rechnet dieser Rechner.</p>
<p>Beim <strong>antiproportionalen Dreisatz</strong> gilt: je mehr, desto weniger. Brauchen 3 Personen 8 Stunden für eine Arbeit, brauchen 6 Personen 3 × 8 ÷ 6 = 4 Stunden. Hier wird multipliziert statt geteilt: D = A × B ÷ C.</p>""",
  formula="Proportional: D = B × C ÷ A\nAntiproportional: D = A × B ÷ C\nVerhältnis kürzen: beide Zahlen durch ihren größten gemeinsamen Teiler teilen",
  example="<p><strong>3 Kilo Äpfel kosten 4,50 €. Was kosten 5 Kilo?</strong> 4,50 € ÷ 3 = 1,50 € pro Kilo, × 5 = <strong>7,50 €</strong>. Im Rechner: A = 3, B = 4,5, C = 5 → D = 7,5.</p>",
  extra="<h3>Dreisatz in drei Schritten</h3><ol><li><strong>Bekanntes notieren:</strong> 3 kg ≙ 4,50 €</li><li><strong>Auf eins schließen:</strong> 1 kg ≙ 4,50 € ÷ 3 = 1,50 €</li><li><strong>Auf das Gesuchte schließen:</strong> 5 kg ≙ 1,50 € × 5 = 7,50 €</li></ol>" +
   "<h3>Typische Dreisatz-Aufgaben</h3>" + tbl(["Aufgabe", "Art", "Lösung"], [("4 Liter kosten 7,20 €. Was kosten 10 Liter?", "proportional", "18,00 €"), ("Ein Auto fährt 360 km mit 24 Litern. Wie weit mit 40 Litern?", "proportional", "600 km"),
     ("5 Maler brauchen 6 Tage. Wie lange brauchen 3 Maler?", "antiproportional", "10 Tage"), ("Bei 80 km/h dauert die Fahrt 3 h. Wie lange bei 120 km/h?", "antiproportional", "2 h")]),
  faqs=[("Wie funktioniert der Dreisatz?", "In drei Schritten: Notieren Sie das bekannte Verhältnis, rechnen Sie auf eine Einheit herunter und dann auf die gesuchte Menge hoch."),
        ("Woran erkenne ich, ob ein Dreisatz proportional oder antiproportional ist?", "Proportional: Wird eine Größe größer, wird auch die andere größer (Menge und Preis). Antiproportional: Wird eine größer, wird die andere kleiner (Arbeiter und Zeit)."),
        ("Wie rechne ich einen antiproportionalen Dreisatz?", "Multiplizieren Sie die bekannten Werte und teilen Sie durch den neuen Wert: D = A × B ÷ C. 3 Personen brauchen 8 Stunden, 6 Personen brauchen 3 × 8 ÷ 6 = 4 Stunden."),
        ("Wie kürze ich ein Verhältnis?", "Teilen Sie beide Zahlen durch ihren größten gemeinsamen Teiler. 12 : 16 wird mit 4 gekürzt zu 3 : 4.")],
  qa=("Wie rechnet man den Dreisatz?", "Schließen Sie zuerst auf eine Einheit und dann auf die gesuchte Menge. Kosten 3 kg 4,50 €, kostet 1 kg 1,50 € und 5 kg kosten 7,50 €. Als Formel: D = B × C ÷ A.")),

 "days": dict(slug="tage-zwischen-zwei-daten", name="Tage zwischen zwei Daten", short="Tage zählen",
  title="Tage zählen – Tage zwischen zwei Daten berechnen | Numbrik",
  meta="Tage zwischen zwei Daten berechnen: Kalendertage, Wochen, Werktage und Monate zwischen zwei Daten zählen – zum Beispiel bis Weihnachten oder zum Urlaub.",
  lede="Zählen Sie die Tage zwischen zwei Daten – für Fristen, Urlaub, Geburtstage oder einen Countdown. Der Rechner zeigt Kalendertage, Wochen, Werktage (Montag bis Freitag) und Monate.",
  steps=["Wählen Sie das Startdatum.", "Wählen Sie das Enddatum.", "Lesen Sie Tage, Wochen, Werktage und Monate ab."],
  how="""<p>Der Rechner zieht das Startdatum vom Enddatum ab. Üblicherweise wird der Starttag nicht mitgezählt, der Endtag schon: Von Montag bis Freitag derselben Woche sind es 4 Tage. Wenn Sie beide Tage mitzählen möchten – etwa bei einem Urlaub –, addieren Sie 1.</p>
<p>Werktage sind hier Montag bis Freitag. Gesetzliche Feiertage unterscheiden sich in Deutschland je nach Bundesland und werden nicht automatisch abgezogen. Schaltjahre mit dem 29. Februar sind berücksichtigt.</p>""",
  formula="Tage = Enddatum − Startdatum\nWochen = Tage ÷ 7\nInklusive beider Tage: Tage + 1",
  example="<p>Vom <strong>1. März 2026</strong> bis zum <strong>1. Juni 2026</strong> sind es 31 + 30 + 31 = <strong>92 Tage</strong> oder 13 Wochen und 1 Tag.</p>",
  extra="<h3>Tage pro Monat</h3>" + tbl(["Monat", "Tage", "Monat", "Tage"], [("Januar", "31", "Juli", "31"), ("Februar", "28 (Schaltjahr 29)", "August", "31"), ("März", "31", "September", "30"), ("April", "30", "Oktober", "31"), ("Mai", "31", "November", "30"), ("Juni", "30", "Dezember", "31")]) +
   "<h3>Schaltjahre</h3><p>Ein Jahr hat 365 Tage, ein Schaltjahr 366. Schaltjahre sind alle durch 4 teilbaren Jahre, außer volle Jahrhunderte, die nicht durch 400 teilbar sind. 2028 und 2032 sind Schaltjahre, 2026 und 2027 nicht.</p>",
  faqs=[("Wie viele Tage liegen zwischen zwei Daten?", "Ziehen Sie das frühere Datum vom späteren ab. Der Rechner erledigt das inklusive Monatslängen und Schaltjahren."),
        ("Wird der erste Tag mitgezählt?", "Standardmäßig nicht: Gezählt werden die Tage vom Start bis zum Ende. Möchten Sie beide Tage einschließen, rechnen Sie einen Tag dazu."),
        ("Wie viele Werktage hat ein Jahr in Deutschland?", "Ein Jahr hat 260 oder 261 Wochentage von Montag bis Freitag. Abzüglich der gesetzlichen Feiertage bleiben je nach Bundesland meist etwa 248 bis 252 Arbeitstage."),
        ("Wie viele Tage hat ein Jahr?", "365 Tage, in Schaltjahren 366. Das sind 52 Wochen und 1 Tag (bzw. 2 Tage).")],
  qa=("Wie berechnet man die Tage zwischen zwei Daten?", "Ziehen Sie das Startdatum vom Enddatum ab; der Starttag wird dabei nicht mitgezählt. Vom 1. März bis 1. Juni 2026 sind es 92 Tage. Für eine Zählung inklusive beider Tage addieren Sie 1.")),

 "age": dict(slug="altersrechner", name="Altersrechner", short="Altersrechner",
  title="Altersrechner – Alter genau berechnen | Numbrik",
  meta="Altersrechner: Ihr genaues Alter in Jahren, Monaten und Tagen berechnen, dazu Ihr Alter in Tagen und Wochen und die Tage bis zum nächsten Geburtstag.",
  lede="Wie alt sind Sie genau? Geben Sie Ihr Geburtsdatum ein und sehen Sie Ihr Alter in Jahren, Monaten und Tagen, insgesamt in Tagen und Wochen und wie viele Tage es bis zu Ihrem nächsten Geburtstag sind.",
  steps=["Geben Sie Ihr Geburtsdatum ein.", "Das zweite Datum ist heute – ändern Sie es, um Ihr Alter an einem anderen Tag zu berechnen.", "Lesen Sie Ihr genaues Alter und die Tage bis zum nächsten Geburtstag ab."],
  how="""<p>Das Alter in Jahren ergibt sich aus der Differenz der Jahreszahlen, minus ein Jahr, falls der Geburtstag im aktuellen Jahr noch nicht war. Für das genaue Alter zählt der Rechner anschließend die vollen Monate seit dem letzten Geburtstag und die restlichen Tage.</p>
<p>Wer am 29. Februar geboren ist, feiert in Nicht-Schaltjahren rechtlich am 1. März ein neues Lebensjahr; der Rechner zählt das Alter entsprechend weiter.</p>""",
  formula="Alter = aktuelles Jahr − Geburtsjahr\n(− 1, wenn der Geburtstag noch nicht war)\nAlter in Tagen = Datum − Geburtsdatum",
  example="<p>Geboren am <strong>17. März 1994</strong>, Stichtag 13. November 2026: <strong>32 Jahre, 7 Monate und 27 Tage</strong>. Der nächste Geburtstag ist in 124 Tagen.</p>",
  extra="<h3>Alter nach Geburtsjahr (am Geburtstag 2026)</h3>" + tbl(["Geburtsjahr", "Alter 2026", "Geburtsjahr", "Alter 2026"], [(y, 2026 - y, y + 30, 2026 - y - 30) for y in range(1950, 1981, 5)]),
  faqs=[("Wie berechne ich mein genaues Alter?", "Ziehen Sie Ihr Geburtsjahr vom aktuellen Jahr ab und ziehen Sie ein Jahr ab, wenn Ihr Geburtstag noch bevorsteht. Für Monate und Tage zählen Sie ab dem letzten Geburtstag weiter."),
        ("Wie alt bin ich in Tagen?", "Geben Sie Ihr Geburtsdatum ein – der Rechner zeigt Ihr Alter in Tagen und Wochen. 30 Jahre sind rund 10.957 Tage."),
        ("Wann werde ich 18?", "An Ihrem 18. Geburtstag. Geben Sie dieses Datum als zweites Datum ein, um zu sehen, wie viele Tage es noch sind."),
        ("Wie wird das Alter bei einem Geburtstag am 29. Februar gezählt?", "In Deutschland vollendet man das neue Lebensjahr in Nicht-Schaltjahren mit Ablauf des 28. Februar; der Geburtstag wird meist am 28. Februar oder 1. März gefeiert.")],
  qa=("Wie berechnet man das genaue Alter?", "Ziehen Sie das Geburtsjahr vom aktuellen Jahr ab und noch ein Jahr, wenn der Geburtstag im laufenden Jahr noch nicht war. Für das genaue Alter zählen Sie danach die vollen Monate und Tage seit dem letzten Geburtstag.")),

 "discount": dict(slug="rabattrechner", name="Rabattrechner", short="Rabattrechner",
  title="Rabattrechner – Preis nach Rabatt berechnen | Numbrik",
  meta="Rabattrechner: Preis nach Rabatt und Ersparnis berechnen – auch für kombinierte Rabatte wie „20 % + weitere 10 %“, ideal für Black Friday und Sale.",
  lede="Berechnen Sie den Preis nach Rabatt und wie viel Sie sparen. Auch kombinierte Rabatte wie „25 % und zusätzlich 10 %“ werden richtig gerechnet – wichtig für Black Friday, Sale und Gutscheine.",
  steps=["Geben Sie den ursprünglichen Preis ein.", "Geben Sie den Rabatt in Prozent ein, etwa 25.", "Optional: einen zusätzlichen Rabatt eintragen. Das Steuerfeld lassen Sie in Deutschland leer, da Preise die Mehrwertsteuer bereits enthalten.", "Lesen Sie den Endpreis, Ihre Ersparnis und den tatsächlichen Gesamtrabatt ab."],
  how="""<p>Der reduzierte Preis ist der Ausgangspreis mal (1 − Rabatt ÷ 100). Ein Artikel für 80 € mit 25 % Rabatt kostet 80 × 0,75 = 60 €; Sie sparen 20 €.</p>
<p>Mehrere Rabatte werden nacheinander berechnet, nicht addiert. „25 % und zusätzlich 10 %“ bedeutet: 10 % vom bereits reduzierten Preis. Aus 80 € werden erst 60 €, dann 54 €. Das sind insgesamt 32,5 % Rabatt, nicht 35 %.</p>""",
  formula="Preis nach Rabatt = Preis × (1 − Rabatt ÷ 100)\nZwei Rabatte: Preis × (1 − r₁ ÷ 100) × (1 − r₂ ÷ 100)\nErsparnis = Preis − Preis nach Rabatt",
  example="<p>Eine Jacke kostet <strong>80 €</strong>, im Sale gibt es <strong>25 %</strong> und an der Kasse <strong>weitere 10 %</strong>: 80 € × 0,75 = 60 €, dann 60 € × 0,90 = <strong>54 €</strong>. Sie sparen 26 €, also 32,5 %.</p>",
  extra="<h3>Rabatttabelle</h3>" + tbl(["Preis"] + [f"−{r} %" for r in (10, 15, 20, 25, 30, 40, 50)], [[eur(p)] + [eur(p * (1 - r / 100)) for r in (10, 15, 20, 25, 30, 40, 50)] for p in (10, 20, 50, 80, 100, 150, 200, 500)]) +
   "<h3>Kombinierte Rabatte: Was Sie wirklich sparen</h3>" + tbl(["Angebot", "Tatsächlicher Rabatt"], [(f"{a} % + weitere {b} %", n(100 - (100 - a) * (100 - b) / 100, 1) + " %") for a, b in ((20, 10), (25, 10), (30, 20), (40, 20), (50, 20), (50, 50))]),
  faqs=[("Wie berechne ich einen Rabatt?", "Multiplizieren Sie den Preis mit dem Rabatt in Prozent und teilen Sie durch 100 – das ist Ihre Ersparnis. 30 % von 45 € sind 13,50 €, der neue Preis ist 31,50 €."),
        ("Sind 20 % plus 20 % Rabatt gleich 40 %?", "Nein. Der zweite Rabatt gilt auf den bereits reduzierten Preis, insgesamt sind es 36 %. Aus 100 € werden 64 €, nicht 60 €."),
        ("Wie berechne ich den ursprünglichen Preis vor dem Rabatt?", "Teilen Sie den reduzierten Preis durch (1 − Rabatt). Kostet etwas nach 25 % Rabatt 60 €, war der Ausgangspreis 60 € ÷ 0,75 = 80 €."),
        ("Ist die Mehrwertsteuer im Preis enthalten?", "In Deutschland müssen Preise für Verbraucher inklusive Mehrwertsteuer angegeben werden. Der Rabatt bezieht sich also auf den Endpreis; ein Steuerfeld brauchen Sie nicht.")],
  qa=("Wie berechnet man den Preis nach Rabatt?", "Preis × (1 − Rabatt ÷ 100). 80 € mit 25 % Rabatt kosten 60 €. Mehrere Rabatte werden nacheinander gerechnet: 25 % plus weitere 10 % ergeben 54 €, also 32,5 % Rabatt.")),

 "wordcount": dict(slug="woerter-zaehlen", name="Wörter zählen", short="Wörter zählen",
  title="Wörter zählen – Wortzähler & Zeichenzähler | Numbrik",
  meta="Wörter zählen online: Wortanzahl, Zeichen mit und ohne Leerzeichen, Sätze, Absätze und Lesezeit Ihres Textes sofort zählen – kostenlos und privat.",
  lede="Fügen Sie Ihren Text ein und zählen Sie sofort Wörter, Zeichen mit und ohne Leerzeichen, Sätze und Absätze. Dazu gibt es Lese- und Sprechzeit sowie die häufigsten Wörter – ideal für Hausarbeiten, Bewerbungen und Blogartikel.",
  steps=["Text eingeben oder einfügen.", "Die Zählung aktualisiert sich beim Tippen.", "Lesen Sie Wörter, Zeichen, Sätze und Absätze ab."],
  how="""<p>Als Wort zählt jede zusammenhängende Folge von Buchstaben oder Ziffern; Wörter mit Bindestrich wie „E-Mail“ und Zahlen wie „2026“ zählen jeweils als ein Wort. Zeichen werden mit und ohne Leerzeichen gezählt, Umlaute und Emojis jeweils als ein Zeichen. Absätze werden durch eine Leerzeile getrennt.</p>
<p>Die Lesezeit basiert auf 238 Wörtern pro Minute, einem Durchschnittswert aus Studien zum stillen Lesen englischer Sachtexte; deutsche Texte mit längeren Wörtern werden oft etwas langsamer gelesen. Ihr Text wird ausschließlich in Ihrem Browser gezählt und nicht übertragen oder gespeichert.</p>""",
  formula="Lesezeit = Wörter ÷ 238 pro Minute\nSprechzeit = Wörter ÷ 140 pro Minute\nNormseiten = Zeichen inkl. Leerzeichen ÷ 1.800",
  example="<p>Ein Text mit <strong>1.500 Wörtern</strong> ist in etwa 6 Minuten gelesen und in rund 11 Minuten vorgetragen. Hat er 10.800 Zeichen inklusive Leerzeichen, entspricht das <strong>6 Normseiten</strong>.</p>",
  extra="<h3>Die Normseite</h3><p>Verlage, Übersetzer und Lektorate rechnen oft in Normseiten: 30 Zeilen mit je 60 Anschlägen, also 1.800 Zeichen inklusive Leerzeichen.</p>" +
   tbl(["Zeichen inkl. Leerzeichen", "Normseiten", "ca. Wörter (Deutsch)"], [(n(z, 0), n(z / 1800, 1), n(round(z / 7.2, -1), 0)) for z in (1800, 3600, 9000, 18000, 36000, 90000)]) +
   "<p>Die Wortzahl ist eine Schätzung mit durchschnittlich etwa 7 Zeichen pro Wort einschließlich Leerzeichen.</p>",
  faqs=[("Wie viele Wörter hat eine Seite?", "Bei 12 pt Schrift, 1,5-zeiligem Abstand und üblichen Rändern etwa 300 bis 350 Wörter. Einzeilig sind es etwa 500, eine Normseite hat 1.800 Zeichen, rund 250 Wörter."),
        ("Zählen Leerzeichen als Zeichen?", "Ja, bei „Zeichen inklusive Leerzeichen“. Viele Vorgaben – etwa für Bewerbungen oder Normseiten – verwenden diesen Wert; achten Sie darauf, welcher gemeint ist."),
        ("Wie zähle ich Wörter in Word oder Google Docs?", "In Word unter Überprüfen › Wörter zählen, in Google Docs unter Tools › Wortanzahl (Strg + Umschalt + C). Dieser Rechner liefert dieselben Werte ohne Programm."),
        ("Werden meine Texte gespeichert?", "Nein. Die Zählung läuft vollständig in Ihrem Browser. Nichts wird an Numbrik gesendet oder gespeichert.")],
  qa=("Wie zählt man Wörter in einem Text?", "Fügen Sie den Text in einen Wortzähler ein: Jede Folge von Buchstaben oder Ziffern zwischen Leerzeichen zählt als ein Wort. Eine Normseite hat 1.800 Zeichen inklusive Leerzeichen, das sind rund 250 Wörter.")),

 "average": dict(slug="durchschnitt-berechnen", name="Durchschnitt berechnen", short="Durchschnitt",
  title="Durchschnitt berechnen – Mittelwert, Median, Modus | Numbrik",
  meta="Durchschnitt berechnen: Mittelwert, Median, Modalwert und Spannweite sofort ermitteln – mit Beispiel zum Notendurchschnitt und Excel-Formeln.",
  lede="Geben Sie Ihre Zahlen ein und erhalten Sie sofort Durchschnitt (arithmetisches Mittel), Median, Modalwert, Spannweite, Summe und das geometrische Mittel – zum Beispiel für Ihren Notendurchschnitt.",
  steps=["Geben Sie Ihre Zahlen ein, getrennt durch Leerzeichen, Semikolon oder neue Zeilen. Dezimalzahlen schreiben Sie mit Komma, etwa 2,5.", "Die Ergebnisse erscheinen sofort.", "Vergleichen Sie Mittelwert und Median, um Ausreißer zu erkennen."],
  how="""<p>Der <strong>Durchschnitt</strong> (arithmetisches Mittel) ist die Summe aller Werte geteilt durch ihre Anzahl. Der <strong>Median</strong> ist der Wert in der Mitte der sortierten Reihe und wird von Ausreißern kaum beeinflusst. Der <strong>Modalwert</strong> ist der häufigste Wert.</p>
<p>Wenn einzelne Werte unterschiedlich zählen – etwa Klausuren doppelt –, brauchen Sie den <strong>gewichteten Durchschnitt</strong>: Jeden Wert mit seinem Gewicht multiplizieren, die Ergebnisse addieren und durch die Summe der Gewichte teilen.</p>""",
  formula="Durchschnitt = Summe aller Werte ÷ Anzahl\nGewichtet = Σ (Wert × Gewicht) ÷ Σ Gewichte\nMedian = mittlerer Wert der sortierten Reihe",
  example=f"<p><strong>Notendurchschnitt:</strong> Die Noten 2, 3, 1, 2 und 4 ergeben (2 + 3 + 1 + 2 + 4) ÷ 5 = <strong>{n(statistics.mean([2, 3, 1, 2, 4]), 1)}</strong>. Der Median ist {n(statistics.median([2, 3, 1, 2, 4]), 0)}, der häufigste Wert ebenfalls 2.</p>",
  extra="<h3>Gewichteter Notendurchschnitt</h3>" + tbl(["Leistung", "Note", "Gewicht", "Note × Gewicht"], [("Klausur 1", "2", "2", "4"), ("Klausur 2", "3", "2", "6"), ("Mündlich", "1", "1", "1"), ("<strong>Summe</strong>", "", "5", "<strong>11</strong>")]) +
   "<p>Gewichteter Durchschnitt: 11 ÷ 5 = <strong>2,2</strong> – ohne Gewichtung wären es 2,0.</p>" +
   "<h3>Durchschnitt in Excel und Google Tabellen</h3>" + tbl(["Was", "Formel"], [("Mittelwert", "<code>=MITTELWERT(A1:A10)</code>"), ("Median", "<code>=MEDIAN(A1:A10)</code>"), ("Modalwert", "<code>=MODUS.EINF(A1:A10)</code>"),
     ("Gewichteter Durchschnitt", "<code>=SUMMENPRODUKT(A1:A5;B1:B5)/SUMME(B1:B5)</code>"), ("Spannweite", "<code>=MAX(A1:A10)-MIN(A1:A10)</code>")]),
  faqs=[("Wie berechnet man den Durchschnitt?", "Addieren Sie alle Zahlen und teilen Sie durch ihre Anzahl. Der Durchschnitt von 4, 8 und 15 ist 27 ÷ 3 = 9."),
        ("Was ist der Unterschied zwischen Durchschnitt und Median?", "Der Durchschnitt nutzt alle Werte, der Median nur die Mitte der sortierten Reihe. Bei Ausreißern – etwa einem sehr hohen Gehalt – beschreibt der Median den typischen Wert besser."),
        ("Wie berechne ich meinen Notendurchschnitt?", "Addieren Sie alle Noten und teilen Sie durch ihre Anzahl. Zählen manche Noten doppelt, multiplizieren Sie sie mit ihrem Gewicht und teilen Sie durch die Summe der Gewichte."),
        ("Wie gebe ich Dezimalzahlen ein?", "Mit Komma, wie im Deutschen üblich, zum Beispiel 2,5 oder 1.234,5. Trennen Sie die Zahlen durch Leerzeichen, Semikolon oder neue Zeilen.")],
  qa=("Wie berechnet man den Durchschnitt?", "Addieren Sie alle Werte und teilen Sie durch ihre Anzahl. Die Noten 2, 3, 1, 2 und 4 ergeben 12 ÷ 5 = 2,4. Für einen gewichteten Durchschnitt multiplizieren Sie jeden Wert mit seinem Gewicht und teilen durch die Summe der Gewichte.")),
}

HUB = "/de/"
def url(i): return f"/de/{PAGES[i]['slug']}/"

def chrome_de(html_page, en_path):
    """Turn the English head/header into a German one."""
    h = html_page.replace('<html lang="en">', '<html lang="de">')
    h = h.replace('<a class="skip" href="#content">Skip to content</a>', '<a class="skip" href="#content">Zum Inhalt springen</a>')
    h = h.replace('placeholder="Search calculators: overtime, GPA, mortgage…" aria-label="Search calculators"', 'placeholder="Rechner suchen (Englisch) …" aria-label="Rechner suchen"')
    h = h.replace('<a class="brand" href="/" aria-label="Numbrik home">', f'<a class="brand" href="{HUB}" aria-label="Numbrik Startseite">')
    import re
    h = re.sub(r'<label class="region">.*?</label>', f'<a class="region" href="{en_path}" hreflang="en" lang="en">English</a>', h, flags=re.S)
    h = h.replace('aria-label="Switch between light and dark mode"', 'aria-label="Hell- und Dunkelmodus wechseln"').replace('<span id="themeLabel">Light</span>', '<span id="themeLabel">Hell</span>')
    return h

def side(cur):
    return ('<aside class="rail" aria-label="Rechner auf Deutsch"><p>Rechner auf Deutsch</p><div class="group"><ul>' +
            "".join(f'<li><a href="{url(i)}"{" aria-current=\"page\"" if i == cur else ""}>{E(p["short"])}</a></li>' for i, p in PAGES.items()) +
            f'</ul></div><div class="group"><h3>English</h3><ul><li><a href="/" hreflang="en" lang="en">All calculators (English)</a></li></ul></div></aside>')

def footer_de():
    items = "".join(f'<li><a href="{url(i)}">{E(p["name"])}</a></li>' for i, p in PAGES.items())
    return f"""<footer>
  <div class="wrap">
    <div><h4>Rechner auf Deutsch</h4><ul>{items}</ul></div>
    <div><h4>Numbrik</h4><ul><li><a href="{HUB}">Alle deutschen Rechner</a></li><li><a href="/" hreflang="en" lang="en">English version</a></li><li><a href="/about/" lang="en">Über uns (Englisch)</a></li><li><a href="/contact/" lang="en">Kontakt (Englisch)</a></li><li><a href="/privacy-policy/" lang="en">Datenschutz (Englisch)</a></li></ul></div>
    <p class="legal">© 2026 Numbrik. Alle Ergebnisse sind Schätzungen zur Orientierung und keine Finanz-, Medizin- oder Rechtsberatung.</p>
  </div>
</footer>
<script src="/assets/app.js?v={{V}}" defer></script>
</body>
</html>
"""

def card_de(i):
    p = PAGES[i]
    return f'<a class="card" href="{url(i)}"><small>Rechner</small><b>{E(p["name"])}</b><span>{E(p["lede"].split(". ")[0].rstrip("."))}.</span></a>'

def build(g):
    head, write, BYID, DOMAIN, V = g["head"], g["write"], g["BYID"], g["DOMAIN"], g["V"]
    TODAY = date.today().isoformat()
    d = date.fromisoformat(TODAY); months = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
    today_de = f"{d.day}. {months[d.month - 1]} {d.year}"
    out = []
    ids = list(PAGES)
    for k, (i, p) in enumerate(PAGES.items()):
        en = f"/{BYID[i]['slug']}/"; path = url(i); full = DOMAIN + path
        q, a = p["qa"]
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "WebApplication", "name": p["name"], "url": full, "description": p["meta"], "inLanguage": "de-DE", "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any",
             "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}},
            {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Rechner auf Deutsch", "item": DOMAIN + HUB}, {"@type": "ListItem", "position": 2, "name": p["name"], "item": full}]},
            {"@type": "WebPage", "name": p["title"], "url": full, "description": p["meta"], "inLanguage": "de-DE", "dateModified": TODAY,
             "author": {"@type": "Organization", "name": "Numbrik", "url": DOMAIN + "/about/"}, "isPartOf": {"@type": "WebSite", "name": "Numbrik", "url": DOMAIN + "/"},
             "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".quick-answer p", ".lede"]}},
            {"@type": "HowTo", "name": f"So nutzen Sie den {p['name']}" if not p["name"].startswith(("Tage", "Wörter", "Durchschnitt")) else p["name"], "step": [{"@type": "HowToStep", "position": j + 1, "text": s} for j, s in enumerate(p["steps"])]},
            {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": x, "acceptedAnswer": {"@type": "Answer", "text": y}} for x, y in [p["qa"]] + p["faqs"]]}]}
        steps = "".join(f"<li>{E(s)}</li>" for s in p["steps"])
        faqs = "".join(f'<div class="qa"><h3>{E(x)}</h3><p>{E(y)}</p></div>' for x, y in p["faqs"])
        rel = "".join(card_de(ids[(k + j) % len(ids)]) for j in (1, 2, 3))
        body = chrome_de(head(p["title"], p["meta"], path, ld), en) + f"""
<nav class="wrap crumbs" aria-label="Brotkrumen"><ol><li><a href="{HUB}">Rechner auf Deutsch</a></li><li aria-current="page">{E(p["name"])}</li></ol></nav>
<div class="wrap main">
  <main class="content" id="content">
    <h1>{E(p["name"])}</h1>
    <p class="byline">Vom <a href="/about/" lang="en">Numbrik-Team</a> · Mit Rechenbeispielen geprüft · Aktualisiert am <time datetime="{TODAY}">{today_de}</time> · <a href="{en}" hreflang="en" lang="en">English</a></p>
    <p class="lede">{E(p["lede"])}</p>
    <div class="panel"><div class="panel-body" id="toolBody" data-tool="{i}"><p class="loading">Rechner wird geladen …</p><noscript><p class="loading">Bitte aktivieren Sie JavaScript, um den Rechner zu nutzen.</p></noscript></div></div>
    <section class="quick-answer" aria-label="Kurze Antwort"><h2>{E(q)}</h2><p>{E(a)}</p></section>
    <article class="prose">
      <h2>So funktioniert's</h2>
      <ol>{steps}</ol>
      <h2>Erklärung</h2>
      {p["how"]}
      <h3>Formel</h3>
      <pre class="formula">{E(p["formula"])}</pre>
      <h2>Beispiel</h2>
      {p["example"]}
      {p["extra"]}
      <h2>Häufige Fragen</h2>
      <div class="faq">{faqs}</div>
      <p class="updated">Zuletzt geprüft am {today_de}. Fehler entdeckt? <a href="/contact/" lang="en">Schreiben Sie uns</a>.</p>
    </article>
    <section class="related" aria-label="Weitere Rechner"><h2>Weitere Rechner</h2><div class="cards">{rel}</div></section>
  </main>
  {side(i)}
</div>
""" + footer_de().replace("{V}", str(V))
        write(path, body); out.append(path)
    # hub
    hub_ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Kostenlose Online-Rechner auf Deutsch", "url": DOMAIN + HUB, "inLanguage": "de-DE",
              "hasPart": [{"@type": "WebApplication", "name": p["name"], "url": DOMAIN + url(i)} for i, p in PAGES.items()]}
    cards = "".join(f'<a class="card" href="{url(i)}"><small>Rechner</small><b>{E(p["name"])}</b><span>{E(p["lede"].split(". ")[0])}.</span></a>' for i, p in PAGES.items())
    hub = chrome_de(head("Online-Rechner kostenlos – Prozent, BMI, Kalorien | Numbrik", "Kostenlose Online-Rechner auf Deutsch: Prozent, BMI, Kalorien, Zinseszins, Dreisatz, Rabatt, Alter, Tage zählen, Wörter zählen und Durchschnitt.", HUB, hub_ld), "/") + f"""
<div class="wrap main"><main class="content" id="content">
<h1>Kostenlose Online-Rechner auf Deutsch</h1>
<p class="lede">Schnelle, kostenlose Rechner für Alltag, Schule, Gesundheit und Finanzen – ohne Anmeldung. Jeder Rechner erklärt die Formel und zeigt ein Rechenbeispiel. Zahlen erscheinen im deutschen Format mit Euro.</p>
<div class="cards">{cards}</div>
<p>Weitere Rechner finden Sie auf der <a href="/" hreflang="en" lang="en">englischen Startseite</a>. Wir übersetzen nach und nach weitere Rechner.</p>
</main>{side(None)}</div>""" + footer_de().replace("{V}", str(V))
    write(HUB, hub); out.append(HUB)
    return out
