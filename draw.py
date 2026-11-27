#!/usr/bin/env python3
"""news-image entry — ATLAS layout (from the previous ATLAS edition, same
locked structure; story set + figures registry replaced for Thu Nov).

Zones: masthead (date + strap) · UTC timeline · THE DAY IN NUMBERS
horizontal strip, separate cells · heroes full width · map ribbon +
tally bar · cards with medallions · bottom two columns: left ALSO,
right DATE CHECK + HOW SURE + sources.
Every figure comes from figures.json (check_numbers.py gate)."""
import json, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FIG = {f["key"]: f["display"] for f in
       json.loads((HERE / "figures.json").read_text(encoding="utf-8"))["figures"]}
REGIONS = {"EUR": "Europe", "ASI": "Asia", "AME": "Americas", "MEA": "Middle East",
           "AFR": "Africa", "OCE": "Oceania", "GLO": "Global & Space"}
REG_COL = {"EUR": (31, 78, 140), "ASI": (176, 44, 34), "AME": (24, 106, 59),
           "MEA": (146, 96, 16), "AFR": (112, 54, 128), "OCE": (10, 110, 122),
           "GLO": (70, 70, 70)}
PAPER, INK, GREY, FAINT = (247, 243, 234), (26, 24, 20), (96, 90, 80), (216, 208, 194)
RED, NAVY, GOLD, CREAM = (176, 44, 34), (31, 51, 84), (196, 148, 38), (255, 252, 244)

im = Image.new("RGB", (1024, 1024), PAPER)
d = ImageDraw.Draw(im)


def F(name, size):
    return ImageFont.truetype(str(HERE / "fonts" / name), size)


SERIF, SERIF38, SERIF27 = F("PlayfairDisplay-Bold.ttf", 68), F("PlayfairDisplay-Bold.ttf", 38), F("PlayfairDisplay-Bold.ttf", 27)
SERIFN, SERIFC = F("PlayfairDisplay-Bold.ttf", 38), F("PlayfairDisplay-Bold.ttf", 17)
SANS, SANSB, SANSS, SANSBS = (F("Archivo.ttf", s) for s in (15, 15, 11, 11))
SANSM, SANSMB, SANSXL = F("Archivo.ttf", 13), F("Archivo.ttf", 13), F("Archivo.ttf", 22)
for _f in (SANSB, SANSBS, SANSMB):
    _f.set_variation_by_axes([700])
SANS.set_variation_by_axes([500]); SANSS.set_variation_by_axes([500]); SANSM.set_variation_by_axes([500])

TEXTS, LINES, OBSTACLES, FAILS = [], [], [], []


def _ink(x, y, s, fnt):
    b = d.textbbox((x, y), s, font=fnt)
    return (b[0], b[1], b[2], b[3])


def text(x, y, s, fnt, fill=INK, tag=""):
    d.text((x, y), s, font=fnt, fill=fill)
    TEXTS.append((*_ink(x, y, s, fnt), tag, s))


def text_c(cx, y, s, fnt, fill=INK, tag=""):
    w = d.textlength(s, font=fnt)
    text(cx - w / 2, y, s, fnt, fill, tag)


def text_r(rx, y, s, fnt, fill=INK, tag=""):
    w = d.textlength(s, font=fnt)
    text(rx - w, y, s, fnt, fill, tag)


def hcheck(x, y, s, fnt, limit, what):
    w = d.textlength(s, font=fnt)
    if w > limit:
        FAILS.append(f"H-FAIL {what}: '{s}' width {w:.0f} > {limit}")


def wrap(s, fnt, width, max_lines, what):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=fnt) <= width:
            cur = t
        else:
            lines.append(cur); cur = w_
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        FAILS.append(f"WRAP-FAIL {what}: '{s}' needs {len(lines)} lines > {max_lines}")
    return lines


def hline(y, x0=12, x1=1012, fill=INK, w=2, tag=""):
    d.line([(x0, y), (x1, y)], fill=fill, width=w)
    LINES.append((x0, y - w / 2, x1, y + w / 2, tag))


def vline(x, y0, y1, fill=INK, w=1, tag=""):
    d.line([(x, y0), (x, y1)], fill=fill, width=w)
    LINES.append((x - w / 2, y0, x + w / 2, y1, tag))


def obstacle(x0, y0, x1, y1, tag=""):
    OBSTACLES.append((x0, y0, x1, y1, tag))


def chip(x, y, sure, tag=""):
    lab = "CONFIRMED" if sure == "C" else "REPORTED"
    w = d.textlength(lab, font=SANSBS) + 12
    d.rounded_rectangle([x, y, x + w, y + 16], 4, fill=INK if sure == "C" else None,
                        outline=INK, width=1)
    text(x + 6, y + 1, lab, SANSBS, CREAM if sure == "C" else INK, tag)
    return w


def fig(key):
    return FIG[key]


# ---------------- story data (locked set, same as bagarte version) ----------
# (place, region, field, headline, deck, source, sure)
HEROES = [
    ("Kuwait City", "MEA", "Conflict", "Drone strike kills 2",
     "Kuwait, Italy blame Iran; Iran denies", "Reuters", "C"),
    ("New York", "AME", "Disaster", "Storm cuts power to 961k",
     "Parade put off to Saturday", "Reuters", "C"),
    ("Brussels", "EUR", "Economy", "De Cos to lead ECB",
     "First Spaniard to lead bank", "AP", "C"),
]
# card headlines shortened for the 130px medallion column; place rides the tab,
# detail rides the 1-line deck.
CARDS = [
    ("Washington", "AME", "Politics", "GDP 'fake' row", "Probe demanded", "AP", "C"),
    ("Gaza", "MEA", "Conflict", "Gaza: 9 killed", "9 killed overnight", "Reuters", "C"),
    ("Jazan", "MEA", "Conflict", "Refinery hit", "1 killed at refinery", "Reuters", "C"),
    ("Kyiv", "EUR", "Conflict", "Strike looms", "113 drones; 87 downed", "BBC", "C"),
    ("Brussels", "EUR", "Politics", "Budget talks fail", "€45bn loan stalls", "AP", "C"),
    ("Ituri", "AFR", "Health", "Ebola: 12,021", "5,904 deaths", "Reuters", "C"),
    ("São Paulo", "AME", "Economy", "Bovespa +6.07%", "STOXX up 1.8%", "Reuters", "C"),
    ("Pyongyang", "ASI", "Conflict", "Nuclear push", "Wider nuclear use", "Reuters", "C"),
    ("Beijing", "ASI", "Economy", "Tariff backlash", "Asia, EU hit back", "AP", "C"),
    ("Shanghai", "ASI", "Technology", "MiniMax named", ">50% of tests hit", "Reuters", "C"),
]
# (place, region, field, main, sub) — sub drawn only when the row has room
ALSO = [
    ("Buenos Aires", "AME", "Economy", "Printing ban", "141-0, 99 abstain · AP"),
    ("London", "EUR", "Migration", "Migration falls", "Down 62% to 77,000 · ONS"),
    ("Erbil", "MEA", "Politics", "Kurds protest", "Oilfields move · Reuters"),
    ("Caracas", "AME", "Politics", "Repeal law planned", "González plans return · La Nación"),
    ("Bangkok", "ASI", "Disaster", "Refinery blast", "9 hurt, 3 critical · AP"),
    ("Ibiza", "EUR", "Disaster", "Tanker capsizes", "17 rescued, 1 dies · Reuters"),
    ("Seoul", "ASI", "Economy", "Rate rise to 3.25%", "Highest in 2 years · BOK"),
    ("Oslo", "EUR", "Economy", "Airline halts flights", "Bankruptcy warning · Reuters"),
    ("Paris", "EUR", "Justice", "Depardieu trial ordered", "Alleged rape · Reuters"),
    ("Bissau", "AFR", "Politics", "Polls delayed to 2028", "Elections in Nov 2028 · Africanews"),
    ("Brasília", "AME", "Economy", "New finance chief", "Trabuco takes post · AFP"),
    ("Naypyidaw", "ASI", "Justice", "Rejects ICJ ruling", "Genocide measures · BBC"),
    ("Washington", "AME", "Justice", "Judge blocks curbs", "Birthright curbs cut · Al Jazeera"),
    ("Detroit", "AME", "Sport", "Bears win 39-35", "Eagles 39-38; Bills 13-10 · AP"),
    ("Melbourne", "OCE", "Sport", "Sinner out of AO", "Knee surgery · Reuters"),
    ("Nairobi", "AFR", "Justice", "Sex-case law signed", "Bars tribal settlements · AllAfrica"),
    ("Finland", "EUR", "Sport", "Wright wins biathlon", "First American winner · Guardian"),
    ("Hong Kong", "ASI", "Society", "Fire anniversary", "168 killed a year ago · BBC"),
    ("Flinders Island", "OCE", "Disaster", "Island burns", "Fire burns >10% · Guardian"),
    ("Bogor", "ASI", "Disaster", "Mine toll rises", "13 dead, 13 missing · BBC"),
    ("Hasakah", "MEA", "Conflict", "ISIL bomber strikes", "2 killed, 5 hurt · Anadolu"),
]
ALSO_SURE = ["C", "C", "C", "C", "C", "C", "C",
             "C", "C", "R", "C", "C", "C", "C",
             "C", "R", "R", "C", "R", "R", "R"]
STORIES_ALL = HEROES + CARDS + [(a[0], a[1], a[2], a[3], a[4], "", s)
                                for a, s in zip(ALSO, ALSO_SURE)]
TOTAL = len(STORIES_ALL)
from collections import Counter
TALLY = Counter(s[1] for s in STORIES_ALL)
REGIONS_N = sum(1 for r in TALLY if r != "GLO")
FIELDS_N = len({s[2] for s in STORIES_ALL})
STRAP = f"{TOTAL} STORIES · {REGIONS_N} REGIONS · {FIELDS_N} FIELDS"


# ---------------- hero scenes (324x100 panels) ------------------------------
def scene_kuwait(x, y):
    # Air-defence station at night: radar tower, drone, blast.
    d.rectangle([x + 30, y + 58, x + 230, y + 96], fill=(60, 58, 52))
    d.polygon([(x + 60, y + 58), (x + 76, y + 14), (x + 92, y + 58)], fill=(120, 116, 108), outline=INK, width=2)
    d.ellipse([x + 66, y + 6, x + 86, y + 26], outline=CREAM, width=3)
    d.line([(x + 76, y + 16), (x + 76, y + 58)], fill=INK, width=2)
    d.rectangle([x + 150, y + 66, x + 226, y + 96], fill=(198, 202, 206), outline=INK, width=2)
    d.rectangle([x + 160, y + 72, x + 178, y + 84], fill=(170, 205, 225), outline=INK, width=1)
    d.rectangle([x + 190, y + 72, x + 208, y + 84], fill=(170, 205, 225), outline=INK, width=1)
    # drone above the station
    d.ellipse([x + 236, y + 18, x + 268, y + 30], fill=INK)
    d.line([(x + 228, y + 24), (x + 276, y + 24)], fill=INK, width=3)
    d.line([(x + 240, y + 14), (x + 264, y + 14)], fill=INK, width=2)
    # blast
    for fx, fh, col in ((x + 100, 26, RED), (x + 118, 36, GOLD), (x + 134, 28, RED)):
        d.polygon([(fx, y + 58), (fx + 9, y + 58 - fh), (fx + 18, y + 58)], fill=col)
    d.line([(x + 10, y + 98), (x + 280, y + 98)], fill=INK, width=2)
    obstacle(x + 58, y + 4, x + 268, y + 96, "hero1")


def scene_storm(x, y):
    # Thanksgiving storm: dark cloud, rain, leaning power pylon, house.
    d.ellipse([x + 30, y + 8, x + 130, y + 40], fill=(120, 116, 108))
    d.ellipse([x + 90, y + 2, x + 190, y + 34], fill=(88, 84, 78))
    d.ellipse([x + 170, y + 10, x + 250, y + 38], fill=(120, 116, 108))
    for rx in (x + 40, x + 80, x + 120, x + 160, x + 200, x + 240):
        d.line([(rx, y + 44), (rx - 8, y + 62)], fill=NAVY, width=2)
    # leaning pylon
    d.line([(x + 250, y + 96), (x + 268, y + 40)], fill=INK, width=4)
    d.line([(x + 244, y + 52), (x + 276, y + 46)], fill=INK, width=3)
    d.line([(x + 248, y + 66), (x + 272, y + 60)], fill=INK, width=3)
    d.line([(x + 268, y + 40), (x + 300, y + 52)], fill=INK, width=2)
    # house with dark windows
    d.rectangle([x + 30, y + 66, x + 110, y + 96], fill=CREAM, outline=INK, width=2)
    d.polygon([(x + 30, y + 66), (x + 70, y + 44), (x + 110, y + 66)], fill=RED, outline=INK, width=2)
    d.rectangle([x + 44, y + 74, x + 58, y + 86], fill=INK)
    d.rectangle([x + 82, y + 74, x + 96, y + 86], fill=INK)
    d.line([(x + 10, y + 98), (x + 280, y + 98)], fill=INK, width=2)
    obstacle(x + 28, y + 2, x + 302, y + 96, "hero2")


def scene_ecb(x, y):
    # ECB: bank front with columns, euro sign, EU stars.
    for sx, sy in ((x + 40, y + 14), (x + 290, y + 18), (x + 250, y + 66), (x + 70, y + 70), (x + 160, y + 10)):
        d.line([(sx - 4, sy), (sx + 4, sy)], fill=GOLD, width=1)
        d.line([(sx, sy - 4), (sx, sy + 4)], fill=GOLD, width=1)
    d.rectangle([x + 60, y + 34, x + 260, y + 96], fill=CREAM, outline=INK, width=2)
    d.polygon([(x + 60, y + 34), (x + 160, y + 10), (x + 260, y + 34)], fill=CREAM, outline=INK, width=2)
    d.ellipse([x + 150, y + 16, x + 170, y + 30], fill=GOLD, outline=INK, width=1)
    for colx in (x + 84, x + 124, x + 196, x + 236):
        d.rectangle([colx, y + 38, colx + 12, y + 96], fill=NAVY)
    d.text((x + 148, y + 52), "€", font=SERIFC, fill=NAVY)
    d.rectangle([x + 60, y + 90, x + 260, y + 96], fill=NAVY)
    obstacle(x + 58, y + 8, x + 262, y + 96, "hero3")


SCENES = [scene_kuwait, scene_storm, scene_ecb]
PLATES = ["KUWAIT", "STORM", "ECB"]

# ---------------- card medallion pictograms (54x54, one subject) ------------
def pic_podium(cx, cy):
    d.rectangle([cx - 16, cy - 2, cx + 16, cy + 20], fill=NAVY, outline=INK, width=2)
    d.ellipse([cx - 9, cy - 18, cx + 9, cy + 0], fill=(198, 202, 206), outline=INK, width=2)
    d.line([(cx, cy - 18), (cx, cy - 2)], fill=INK, width=2)
    d.rectangle([cx - 12, cy + 8, cx + 12, cy + 14], fill=CREAM, outline=INK, width=1)


def pic_refinery(cx, cy):
    d.rectangle([cx - 20, cy - 2, cx - 4, cy + 20], fill=(198, 202, 206), outline=INK, width=2)
    d.rectangle([cx + 2, cy + 6, cx + 18, cy + 20], fill=(198, 202, 206), outline=INK, width=2)
    d.line([(cx + 12, cy - 20), (cx + 12, cy + 6)], fill=INK, width=3)
    d.polygon([(cx + 12, cy - 20), (cx + 6, cy - 8), (cx + 18, cy - 8)], fill=RED)
    d.polygon([(cx + 12, cy - 20), (cx + 9, cy - 12), (cx + 15, cy - 12)], fill=GOLD)


def pic_missile(cx, cy):
    d.line([(cx - 16, cy + 16), (cx + 12, cy - 12)], fill=INK, width=5)
    d.polygon([(cx + 12, cy - 12), (cx + 17, cy - 19), (cx + 19, cy - 10)], fill=RED)
    d.line([(cx - 16, cy + 16), (cx - 9, cy + 9)], fill=GOLD, width=3)
    d.rectangle([cx - 18, cy + 10, cx + 18, cy + 20], fill=(120, 116, 108))


def pic_euro(cx, cy):
    d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=GOLD, outline=INK, width=2)
    d.text((cx - 11, cy - 19), "€", font=SERIFC, fill=INK)


def pic_chart_up(cx, cy):
    d.line([(cx - 20, cy + 20), (cx + 20, cy + 20)], fill=INK, width=2)
    d.line([(cx - 20, cy - 20), (cx - 20, cy + 20)], fill=INK, width=2)
    d.line([(cx - 16, cy + 12), (cx - 4, cy + 2), (cx + 6, cy + 8), (cx + 16, cy - 12)], fill=(24, 106, 59), width=4)
    d.polygon([(cx + 16, cy - 12), (cx + 8, cy - 13), (cx + 15, cy - 5)], fill=(24, 106, 59))


def pic_cross(cx, cy):
    d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=CREAM, outline=INK, width=2)
    d.rectangle([cx - 5, cy - 14, cx + 5, cy + 14], fill=RED)
    d.rectangle([cx - 14, cy - 5, cx + 14, cy + 5], fill=RED)


def pic_building(cx, cy):
    d.rectangle([cx - 14, cy - 20, cx + 14, cy + 20], fill=(198, 202, 206), outline=INK, width=2)
    for wy in (cy - 13, cy - 3, cy + 7):
        for wx in (cx - 8, cx + 2):
            d.rectangle([wx, wy, wx + 6, wy + 6], fill=NAVY)


def pic_atom(cx, cy):
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED, outline=INK, width=2)
    d.ellipse([cx - 20, cy - 10, cx + 20, cy + 10], outline=NAVY, width=2)
    d.ellipse([cx - 10, cy - 20, cx + 10, cy + 20], outline=NAVY, width=2)


def pic_container(cx, cy):
    d.rectangle([cx - 20, cy - 16, cx - 2, cy - 2], fill=RED, outline=INK, width=2)
    d.rectangle([cx + 2, cy - 16, cx + 20, cy - 2], fill=NAVY, outline=INK, width=2)
    d.rectangle([cx - 11, cy + 2, cx + 11, cy + 16], fill=GOLD, outline=INK, width=2)
    d.line([(cx - 20, cy + 20), (cx + 20, cy + 20)], fill=INK, width=2)


def pic_chip(cx, cy):
    d.rectangle([cx - 14, cy - 14, cx + 14, cy + 14], fill=NAVY, outline=INK, width=2)
    d.rectangle([cx - 6, cy - 6, cx + 6, cy + 6], fill=CREAM, outline=INK, width=1)
    for px in (cx - 10, cx - 3, cx + 4):
        d.line([(px, cy - 20), (px, cy - 14)], fill=INK, width=2)
        d.line([(px, cy + 14), (px, cy + 20)], fill=INK, width=2)
    for py in (cy - 10, cy - 3, cy + 4):
        d.line([(cx - 20, py), (cx - 14, py)], fill=INK, width=2)
        d.line([(cx + 14, py), (cx + 20, py)], fill=INK, width=2)


PICS = [pic_podium, pic_building, pic_refinery, pic_missile, pic_euro,
        pic_cross, pic_chart_up, pic_atom, pic_container, pic_chip]

# ---------------- map (continent-ellipse dot grid, ribbon 1000x100) --------
# Land dots are generated from rough continent ellipses in the SAME lon/lat
# projection the pins use, so every pin sits on land. (lon_c, lat_c, rx, ry)
CONTINENTS = [
    (-100, 48, 38, 16), (-85, 38, 22, 10), (-95, 65, 25, 8), (-102, 22, 10, 7),
    (-152, 65, 10, 6),                                    # North America + Alaska
    (-62, -12, 13, 16), (-70, -25, 8, 12), (-72, 8, 10, 7),   # South America
    (20, 8, 17, 14), (22, -12, 13, 12), (47, 5, 6, 5), (15, 27, 20, 8),  # Africa
    (15, 52, 18, 8), (10, 44, 10, 5), (15, 63, 10, 6),        # Europe
    (45, 32, 14, 9),                                          # Middle East
    (60, 50, 35, 13), (95, 35, 18, 12), (78, 21, 8, 9), (102, 15, 7, 8),
    (140, 62, 25, 9), (138, 37, 6, 5),                        # Asia + Japan
    (112, -4, 13, 6), (134, -25, 13, 7), (160, -9, 5, 3), (172, -42, 4, 4),
]
PIN_POS = {  # story no: (lon, lat, dx, dy) — nudges for the Europe/ME cluster
    1: (47.98, 29.38, 12, -14), 2: (-74.0, 40.7, 16, -12), 3: (4.35, 50.85, -18, -12),
    4: (-77.0, 38.9, -16, 12), 5: (34.35, 31.42, -18, 14), 6: (42.55, 16.89, 14, 10),
    7: (30.52, 50.45, 0, -13), 8: (4.35, 50.85, 18, 12), 9: (30.25, 1.57, 20, 8),
    10: (-46.63, -23.55, 0, 0), 11: (125.75, 39.04, 0, -12), 12: (116.4, 39.9, 0, -12),
    13: (121.47, 31.23, 0, 0),
}


# ============================ MASTHEAD =====================================
text(12, 2, "THE WORLD IN ONE PICTURE — ORIGINAL DRAWINGS", SANSMB, RED, "eyebrow")
text_r(1012, 2, STRAP, SANSMB, INK, "strap")
DATE_STR = "Thursday 26 November 2026"
date_w = d.textlength(DATE_STR, font=SERIF)
seg = (1000 - date_w) / 2 - 14
d.rectangle([12, 30, 12 + seg, 33], fill=RED)
d.rectangle([1012 - seg, 30, 1012, 33], fill=RED)
MAST_OBS = [(12, 30, 12 + seg, 33), (1012 - seg, 30, 1012, 33)]
text_c(512, 0, DATE_STR, SERIF, INK, "date")
hline(100, fill=INK, w=3, tag="masthead-rule")

# ============================ TIMELINE =====================================
TL = [("00:58", "BOK RAISES RATES"), ("05:28", "EBOLA SURGE"),
      ("07:45", "BANGKOK BLAST"), ("13:21", "UK MIGRATION FALLS"),
      ("15:36", "KUWAIT STRIKE"), ("16:55", "TRUMP GDP CLAIM"),
      ("23:49", "ZELENSKY INTERVIEW")]
d.rectangle([12, 104, 64, 124], fill=INK)
text(20, 107, "UTC", SANSBS, CREAM, "tl-label")
for i, (tm, cap) in enumerate(TL):
    tx = 76 + i * 134
    text(tx, 103, tm, SANSMB, RED, "tl-time")
    text(tx, 118, cap, SANSS, GREY, "tl-cap")
    hcheck(tx, 118, cap, SANSS, 128, f"tl cap {i}")
hline(133, fill=FAINT, w=1, tag="tl-rule")

# ==================== DAY IN NUMBERS — horizontal strip ====================
text(12, 135, "THE DAY IN NUMBERS", SANSBS, RED, "nums-head")
NUMS = [(fig("storm_outages"), "STORM — PEAK OUTAGES", "Parade postponed"),
        (fig("kuwait_killed"), "CONFLICT — KILLED IN KUWAIT", "Italy blames Iran; Iran denies"),
        (fig("ebola_cases"), "HEALTH — EBOLA", "5,904 deaths"),
        (fig("bovespa_rise"), "MARKETS — BOVESPA", "STOXX up 1.8%")]
for i, (num, role, ctx) in enumerate(NUMS):
    cx = 12 + i * 250
    if i:
        vline(cx - 6, 138, 190, fill=FAINT, w=1, tag=f"numsep{i}")
    text(cx + 2, 144, num, SERIFN, INK, f"num{i}")
    nw = d.textlength(num, font=SERIFN)
    rx = cx + nw + 16
    text(rx, 148, role, SANSBS, RED, f"numrole{i}")
    text(rx, 163, ctx, SANSS, GREY, f"numctx{i}")
    hcheck(rx, 148, role, SANSBS, cx + 244 - rx, f"num role {i}")
    hcheck(rx, 163, ctx, SANSS, cx + 244 - rx, f"num ctx {i}")
hline(197, fill=INK, w=2, tag="nums-rule")

# ============================ HEROES =======================================
HY = 198
for i, (place, reg, field, head, deck, src, sure) in enumerate(HEROES):
    x = 12 + i * 338
    w = 324
    d.rectangle([x, HY, x + w, HY + 92], fill=NAVY if i == 2 else (238, 232, 218))
    SCENES[i](x, HY)
    d.rectangle([x, HY + 92, x + w, HY + 114], fill=INK)
    text(x + 7, HY + 95, PLATES[i], SANSBS, CREAM, f"hero{i + 1}")
    cw = chip(x + w - 76, HY + 95, sure, f"hero{i + 1}")
    d.ellipse([x, HY + 118, x + 18, HY + 136], fill=REG_COL[reg])
    text_c(x + 9, HY + 120, str(i + 1), SANSBS, CREAM, f"hero{i + 1}")
    text(x + 24, HY + 120, f"{place.upper()} — {field.upper()}", SANSBS, REG_COL[reg], f"hero{i + 1}")
    text_r(x + w, HY + 120, src, SANSS, GREY, f"hero{i + 1}")
    for j, ln in enumerate(wrap(head, SERIF38, w - 2, 2, f"hero{i + 1} headline")):
        text(x, HY + 136 + j * 39, ln, SERIF38, INK, f"hero{i + 1}h")
    text(x, HY + 228, deck, SANS, INK, f"hero{i + 1}")
    hcheck(x, HY + 228, deck, SANS, w - 2, f"hero{i + 1} deck")

# ============================ MAP RIBBON ===================================
MY = 444
d.rectangle([12, MY, 1012, MY + 100], fill=NAVY)
for r in range(16):
    for c in range(110):
        px = 12 + (c + 0.5) / 110 * 1000
        py = MY + (r + 0.5) / 16 * 100
        lon = (px - 12) / 1000 * 360 - 168
        lat = 78 - (py - MY) / 100 * 134
        if any(((lon - cx) / rx) ** 2 + ((lat - cy) / ry) ** 2 <= 1
               for cx, cy, rx, ry in CONTINENTS):
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(214, 205, 188))
d.rectangle([12, MY, 168, MY + 20], fill=INK)
text(19, MY + 3, "WHERE IT HAPPENED", SANSBS, CREAM, "map-head")
STORY_LONLAT = [(1, 47.98, 29.38), (2, -74.0, 40.7), (3, 4.35, 50.85), (4, -77.0, 38.9),
                (5, 34.35, 31.42), (6, 42.55, 16.89), (7, 30.52, 50.45), (8, 4.35, 50.85),
                (9, 30.25, 1.57), (10, -46.63, -23.55), (11, 125.75, 39.04), (12, 116.4, 39.9),
                (13, 121.47, 31.23)]
for n, lon, lat in STORY_LONLAT:
    _, _, dx, dy = PIN_POS[n]
    px = 12 + (lon + 168) / 360 * 1000 + dx
    py = MY + (78 - lat) / 134 * 100 + dy
    d.ellipse([px - 10, py - 10, px + 10, py + 10], fill=CREAM, outline=INK, width=2)
    text_c(px, py - 7, str(n), SANSBS, INK, "pin")
# tally bar
TY = MY + 106
tx = 12
for reg in ("EUR", "ASI", "AME", "MEA", "AFR", "OCE", "GLO"):
    if not TALLY[reg]:
        continue
    segw = TALLY[reg] / TOTAL * 1000
    d.rectangle([tx, TY, tx + segw, TY + 14], fill=REG_COL[reg])
    lab = "MIDDLE EAST" if reg == "MEA" else REGIONS[reg].split(' ')[0].upper()
    text(tx + 2, TY + 17, f"{lab} {TALLY[reg]}", SANSS, INK, "tally")
    tx += segw
hline(MY + 140, fill=FAINT, w=1, tag="map-rule")

# ============================ CARDS ========================================
CY0 = 588
MEDALS = []
for i, (place, reg, field, head, deck, src, sure) in enumerate(CARDS):
    cx, cy = 12 + (i % 5) * 200, CY0 + (i // 5) * 104
    n = i + 4
    d.ellipse([cx, cy, cx + 17, cy + 17], fill=REG_COL[reg])
    text_c(cx + 8.5, cy + 2, str(n), SANSBS, CREAM, f"card{n}")
    text(cx + 22, cy + 2, place.upper(), SANSBS, REG_COL[reg], f"card{n}")
    lab = "CONFIRMED" if sure == "C" else "REPORTED"
    chipw = d.textlength(lab, font=SANSBS) + 12
    chip(cx + 192 - chipw, cy, sure, f"card{n}")
    d.rounded_rectangle([cx, cy + 22, cx + 54, cy + 76], 6, fill=CREAM, outline=INK, width=2)
    PICS[i](cx + 27, cy + 49)
    MEDALS.append((cx, cy + 22, cx + 54, cy + 76, n))
    for j, ln in enumerate(wrap(head, SERIF27, 132, 2, f"card{n} headline")):
        text(cx + 62, cy + 22 + j * 29, ln, SERIF27, INK, f"card{n}h")
    sw = d.textlength(src, font=SANSS)
    text(cx, cy + 86, deck, SANS, INK, f"card{n}")
    hcheck(cx, cy + 86, deck, SANS, 192 - sw - 8, f"card{n} deck")
    text_r(cx + 192, cy + 88, src, SANSS, GREY, f"card{n}")

# ============================ BOTTOM =======================================
BY = 796
text(12, BY, "ALSO ON THURSDAY 26 NOVEMBER", SANSB, RED, "also-head")
for col in range(3):
    items = ALSO[col * 7:(col + 1) * 7]
    ax = 12 + col * 224
    for j, (place, reg, field, main, sub) in enumerate(items):
        yy = BY + 22 + j * 32
        text(ax, yy, f"{place} — ", SANSMB, INK, "alsoP")
        off = d.textlength(f"{place} — ", font=SANSMB)
        text(ax + off, yy, main, SANSM, INK, "alsoM")
        hcheck(ax, yy, f"{place} — {main}", SANSMB, 216, f"also {col * 7 + j + 14}")
        if j < 6:
            text(ax + 2, yy + 19, sub, SANSS, GREY, "alsoS")
# DATE CHECK (right column) — the deliberate trap list
DX, DY = 684, BY - 1
DC_TEXT = ("All stories: Thu 26 Nov 2026. "
           "Wed 25 Nov — NOT Thu news: tariff proposals; Cairo tanker fire; "
           "Shenzhou-24 launch; Cartagena siege; US GDP revision; "
           "Miss Universe; Solomon treaty. "
           "Tue 24 Nov: Senegal AFCON title; Huawei verdict. "
           "NOT YET: Macy's parade Sat 28 Nov; ECB appointment Dec; "
           "EU budget talks 17-18 Dec; Spain vote Sun 29 Nov; "
           "González return 5 Dec.")
d.rectangle([DX, DY, DX + 118, DY + 22], fill=INK)
text(DX + 7, DY + 4, "DATE CHECK", SANSBS, CREAM, "dc-tab")
d.rectangle([DX, DY, 1012, DY + 158], outline=INK, width=2)
dc_texts = []
yy = DY + 30
for ln in wrap(DC_TEXT, SANSM, 304, 8, "date check"):
    dc_texts.append((*_ink(DX + 12, yy, ln, SANSM), "dc", ln))
    text(DX + 12, yy, ln, SANSM, INK, "dc")
    yy += 15
# HOW SURE + sources footer (right column, below the box)
HY2 = DY + 166
text(DX, HY2, "HOW SURE", SANSBS, RED, "howsure")
cw1 = chip(DX + 72, HY2 - 2, "C", "howsure")
text(DX + 72 + cw1 + 6, HY2, "2+ outlets agree", SANSS, INK, "howsure")
cw2 = chip(DX + 72, HY2 + 18, "R", "howsure")
text(DX + 72 + cw2 + 6, HY2 + 20, "one outlet or a claim", SANSS, INK, "howsure")
srcs = []
for s in STORIES_ALL:
    if s[5] and s[5] not in srcs:
        srcs.append(s[5])
FOOT = (f"Sources: {' · '.join(srcs[:5])} + {len(srcs) - 5} more"
        if len(srcs) > 5 else f"Sources: {' · '.join(srcs)}")
text(DX, HY2 + 44, FOOT, SANSS, GREY, "footer")
hcheck(DX, HY2 + 44, FOOT, SANSS, 328, "footer sources")

# ============================ AUDITS =======================================
def overlap(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def gap(a, b):
    dx = max(b[0] - a[2], a[0] - b[2], 0)
    dy = max(b[1] - a[3], a[1] - b[3], 0)
    return math.hypot(dx, dy)


findings = []
# 1. TEXT-AUDIT
for i in range(len(TEXTS)):
    for j in range(i + 1, len(TEXTS)):
        a, b = TEXTS[i], TEXTS[j]
        if {a[4], b[4]} == {"alsoP", "alsoM"} and abs(a[1] - b[1]) < 3:
            continue  # one composed ALSO line: bold place + regular main
        if a[4] == b[4] and (a[4] == "dc" or a[4].endswith("h")):
            continue  # wrapped lines of one headline / one date-check block
        if overlap(a, b):
            findings.append(f"TEXT overlap: '{a[5]}' <> '{b[5]}'")
        elif gap(a, b) < 3:
            findings.append(f"TEXT gap<3: '{a[5]}' <> '{b[5]}' ({gap(a, b):.1f}px)")
print(f"TEXT-AUDIT: {len(findings)} finding(s)")
for f_ in findings:
    print("  ", f_)
# 2. LINE-AUDIT
lf = []
for t in TEXTS:
    for ln in LINES:
        if overlap(t, ln):
            lf.append(f"LINE overlap: '{t[5]}' x {ln[4]}")
        elif gap(t, ln) < 3:
            lf.append(f"LINE gap<3: '{t[5]}' x {ln[4]} ({gap(t, ln):.1f}px)")
print(f"LINE-AUDIT: {len(lf)} finding(s)")
for f_ in lf:
    print("  ", f_)
findings += lf
# 3. GFX-AUDIT (hero scenes exempt vs their own texts)
gf = []
for t in TEXTS:
    for ob in OBSTACLES:
        if t[4].startswith("hero") and ob[4] == f"hero{t[4][4]}":
            continue
        if overlap(t, ob):
            gf.append(f"GFX overlap: '{t[5]}' x obstacle {ob[4]}")
        elif gap(t, ob) < 3:
            gf.append(f"GFX gap<3: '{t[5]}' x obstacle {ob[4]} ({gap(t, ob):.1f}px)")
print(f"GFX-AUDIT: {len(gf)} finding(s)")
for f_ in gf:
    print("  ", f_)
findings += gf
# 4. MEDAL-AUDIT (pixel scan: pictogram ink must stay >=4px inside the frame)
mf = []
arr = im.load()
for (x0, y0, x1, y1, n) in MEDALS:
    bad = 0
    for px in range(x0 + 4, x1 - 3):
        for py in range(y0 + 4, y1 - 3):
            if px in (x0 + 4, x1 - 4) or py in (y0 + 4, y1 - 4):
                if arr[px, py] != CREAM:
                    bad += 1
    ring = [(px, py) for px in range(x0 + 3, x1 - 2) for py in (y0 + 3, y1 - 3)]
    ring += [(px, py) for py in range(y0 + 3, y1 - 2) for px in (x0 + 3, x1 - 3)]
    edge = sum(1 for (px, py) in ring if arr[px, py] != CREAM)
    if bad or edge:
        mf.append(f"MEDAL card{n}: ink within 4px of frame (ring {bad}, edge {edge})")
print(f"MEDAL-AUDIT: {len(mf)} finding(s)")
for f_ in mf:
    print("  ", f_)
findings += mf
# 5. MASTHEAD-AUDIT (date vs red segments + rule)
mastf = []
date_box = [t for t in TEXTS if t[4] == "date"][0]
for ob in MAST_OBS:
    if overlap(date_box, ob) or gap(date_box, ob) < 3:
        mastf.append("MASTHEAD: date too close to red segment")
print(f"MASTHEAD-AUDIT: {len(mastf)} finding(s)")
for f_ in mastf:
    print("  ", f_)
findings += mastf
# 6. DC-AUDIT
dcf = [f"DC: '{t[5]}' escapes box" for t in dc_texts
       if t[0] < DX + 9 or t[2] > 1009 or t[1] < DY + 25 or t[3] > DY + 155]
print(f"DC-AUDIT: {len(dcf)} finding(s)")
for f_ in dcf:
    print("  ", f_)
findings += dcf
# 7. FIG-SELFCHECK (WARN only)
joined = " ".join(t[5] for t in TEXTS)
figw = [f"FIG-WARN: display '{v}' (key) not drawn"
        for k, v in FIG.items() if v not in joined]
print(f"FIG-SELFCHECK (WARN only): {len(figw)} finding(s)")
for f_ in figw:
    print("  ", f_)

for f_ in FAILS:
    print(f_)
print(f"TOTAL AUDIT FINDINGS: {len(findings)} | FAIL: {len(FAILS)}")
im.save(HERE / "entry.png")
print("saved", HERE / "entry.png", im.size)
