"""Shared Save Our Homes model (used for page examples; JS mirrors it)."""
CAPS = {1995: 2.7, 1996: 2.5, 1997: 3.0, 1998: 1.7, 1999: 1.6, 2000: 2.7, 2001: 3.0, 2002: 1.6, 2003: 2.4, 2004: 1.9, 2005: 3.0, 2006: 3.0,
        2007: 2.5, 2008: 3.0, 2009: 0.1, 2010: 2.7, 2011: 1.5, 2012: 3.0, 2013: 1.7, 2014: 1.5, 2015: 0.8, 2016: 0.7, 2017: 2.1, 2018: 2.1,
        2019: 1.9, 2020: 2.3, 2021: 1.4, 2022: 3.0, 2023: 3.0, 2024: 3.0, 2025: 2.9, 2026: 2.7}
SECOND = {2025: 25722, 2026: 26411}
def second(y): return SECOND.get(y, 25000)
def taxes(assessed, year, school_mills, other_mills):
    sch = max(0, assessed - 25000)
    sec = min(max(0, assessed - 50000), second(year))
    oth = max(0, assessed - 25000 - sec)
    return sch * school_mills / 1000 + oth * other_mills / 1000
def run(base_year, base_value, now_value, now_year=2026, school=6.0, other=11.5):
    n = now_year - base_year
    g = (now_value / base_value) ** (1 / n) if n > 0 else 1
    a = base_value; rows = []
    for y in range(base_year, now_year + 1):
        j = base_value * g ** (y - base_year)
        if y > base_year: a = min(j, a * (1 + CAPS[y] / 100))
        rows.append((y, j, a, taxes(j, y, school, other) - taxes(a, y, school, other)))
    return rows
