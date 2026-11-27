#!/usr/bin/env python3
"""news-image entry — map-column layout (replacement brief, Saturday).

Zones: masthead + UTC timeline · top zone split: LEFT three stacked
hero panels, RIGHT tall dot-map panel (numbered pins + tally bar) ·
numbers strip, four separate cells · eight cards in a four-by-two
grid with big medallions · bottom zone: ALSO in two big-type columns
+ DATE CHECK box + HOW SURE legend + sources footer.
Type floors: hero headlines largest, card headlines large, decks
mid-size, ALSO main and sub big, kickers and scene labels clear.
Every figure comes from figures.json (check_numbers.py gate)."""
import json
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
FDIR = HERE / "fonts"
REG = {f["key"]: f["display"] for f in
       json.loads((HERE / "figures.json").read_text(encoding="utf-8"))["figures"]}


def fig(key):
    return REG[key]


def F(name, size):
    return ImageFont.truetype(str(FDIR / name), size)


SERIF = "PlayfairDisplay-Bold.ttf"
SANSF = "Archivo.ttf"
SERIF46 = F(SERIF, 46)
SERIF40 = F(SERIF, 40)
SERIF30 = F(SERIF, 30)
SERIF28 = F(SERIF, 28)
SERIF36 = F(SERIF, 36)
SANSB15 = F(SANSF, 15)
SANSB14 = F(SANSF, 14)
SANSB13 = F(SANSF, 13)
SANSB12 = F(SANSF, 12)
SANS13 = F(SANSF, 13)
SANS12 = F(SANSF, 12)
SANS11 = F(SANSF, 11)
SANS16 = F(SANSF, 16)
SANSB18 = F(SANSF, 18)
SANS14 = F(SANSF, 14)

PAPER = (247, 243, 234)
CREAM = (238, 232, 218)
INK = (30, 28, 26)
GREY = (110, 106, 100)
RED = (176, 32, 40)
NAVY = (24, 42, 84)
GOLD = (196, 150, 44)

img = Image.new("RGB", (1024, 1024), PAPER)
d = ImageDraw.Draw(img)

TEXTS, LINES, GFX, FAILS = [], [], [], []


def text(x, y, s, font, fill=INK, tag=""):
    d.text((x, y), s, font=font, fill=fill)
    TEXTS.append((x, y, x + d.textlength(s, font=font),
                  y + font.getbbox("Ag")[3], s, tag))


def text_r(x, y, s, font, fill=INK, tag=""):
    text(x - d.textlength(s, font=font), y, s, font, fill, tag)


def text_c(x, y, s, font, fill=INK, tag=""):
    text(x - d.textlength(s, font=font) / 2, y, s, font, fill, tag)


def line(x0, y0, x1, y1, fill=INK, w=1, tag=""):
    d.line([(x0, y0), (x1, y1)], fill=fill, width=w)
    LINES.append((min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1), tag))


def obstacle(x0, y0, x1, y1, tag=""):
    GFX.append((x0, y0, x1, y1, tag))


def wrap(s, font, width):
    words, lines_, cur = s.split(), [], ""
    for w_ in words:
        t = f"{cur} {w_}".strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            lines_.append(cur)
            cur = w_
    if cur:
        lines_.append(cur)
    return lines_


def hcheck(x, y, s, font, limit, what):
    w_ = d.textlength(s, font=font)
    if w_ > limit:
        FAILS.append(f"H-FAIL {what}: '{s}' width {w_:.0f} > {limit:.0f}")


def chip(x_right, y, sure, tag):
    lab = "CONFIRMED" if sure == "C" else "REPORTED"
    w_ = d.textlength(lab, font=SANSB12) + 12
    col = NAVY if sure == "C" else RED
    d.rectangle([x_right - w_, y, x_right, y + 17], outline=col, width=1)
    text(x_right - w_ + 6, y + 2, lab, SANSB12, col, tag)
    return w_


# (place, region, field, headline, deck, source, sure)
HEROES = [
    ("Kuwait City", "MEA", "Conflict", "2 Italians killed",
     "Kuwait, Italy blame Iran; Iran denies", "Reuters", "C"),
    ("New York", "AME", "Disaster", "Power out for 961k",
     "Parade put off to Saturday", "Reuters", "C"),
    ("Brussels", "EUR", "Economy", "De Cos to lead ECB",
     "First Spaniard to lead bank", "AP", "C"),
]
# (place, region, field, headline, deck, source, sure) — stories 4-11
CARDS = [
    ("Washington", "AME", "Politics", "GDP 'fake' row", "Probe demanded", "AP", "C"),
    ("Gaza", "MEA", "Conflict", "Gaza: 9 killed", "9 killed overnight", "Reuters", "C"),
    ("Jazan", "MEA", "Conflict", "Refinery hit", "1 killed at refinery", "Reuters", "C"),
    ("Kyiv", "EUR", "Conflict", "Strike looms", "113 drones; 87 downed", "BBC", "C"),
    ("Brussels", "EUR", "Politics", "Budget talks fail", "€45bn loan stalls", "AP", "C"),
    ("Ituri", "AFR", "Health", "Ebola: 12,021", "5,904 deaths", "Reuters", "C"),
    ("São Paulo", "AME", "Economy", "Bovespa +6.07%", "STOXX up 1.8%", "Reuters", "C"),
    ("Pyongyang", "ASI", "Conflict", "Nuclear push", "Wider nuclear use", "Reuters", "C"),
]
# (place, region, field, main, sub, sure) — drawn in two columns, col-major
ALSO = [
    ("Beijing", "ASI", "Economy", "Tariff backlash", "Asia, EU · AP", "C"),
    ("Buenos Aires", "AME", "Economy", "Printing ban", "141-0 · AP", "C"),
    ("London", "EUR", "Migration", "Migration falls", "77,000 · ONS", "C"),
    ("Erbil", "MEA", "Politics", "Kurds protest", "Reuters", "C"),
    ("Caracas", "AME", "Politics", "Repeal law planned", "La Nación", "C"),
    ("Bangkok", "ASI", "Disaster", "Refinery blast", "9 hurt · AP", "C"),
    ("Ibiza", "EUR", "Disaster", "Tanker capsizes", "17 · Reuters", "C"),
    ("Seoul", "ASI", "Economy", "Rate rise to 3.25%", "BOK", "C"),
    ("Oslo", "EUR", "Economy", "Airline halts flights", "Reuters", "C"),
    ("Paris", "EUR", "Justice", "Depardieu trial", "Alleged · Reuters", "C"),
    ("Shanghai", "ASI", "Technology", "MiniMax named", ">50% · Reuters", "C"),
    ("Bissau", "AFR", "Politics", "Polls delayed", "Africanews", "R"),
    ("Brasília", "AME", "Economy", "Trabuco named", "AFP", "C"),
    ("Naypyidaw", "ASI", "Justice", "Rejects ICJ ruling", "BBC", "C"),
    ("Washington", "AME", "Justice", "Judge blocks", "Al Jazeera", "C"),
    ("Detroit", "AME", "Sport", "Bears win", "39-35 · AP", "C"),
    ("Melbourne", "OCE", "Sport", "Sinner out of AO", "Reuters", "C"),
    ("Hong Kong", "ASI", "Society", "Fire anniversary", "168 · BBC", "C"),
    ("Flinders Island", "OCE", "Disaster", ">10% burns", "Guardian", "R"),
    ("Bogor", "ASI", "Disaster", "Mine toll rises", "13 dead · BBC", "R"),
]
STORIES_ALL = HEROES + CARDS + ALSO
TOTAL = len(STORIES_ALL)
TALLY = Counter(s[1] for s in STORIES_ALL)
REGIONS_N = sum(1 for r in TALLY if r != "GLO")
FIELDS_N = len({s[2] for s in STORIES_ALL})
STRAP = f"{TOTAL} STORIES · {REGIONS_N} REGIONS · {FIELDS_N} FIELDS"
DATE_STR = "Thursday 26 November 2026"

# ---------------- masthead ----------------
text(12, 4, "THE WORLD IN ONE PICTURE — ORIGINAL DRAWINGS", SANSB12, RED, "mast")
text(12, 22, DATE_STR, SERIF46, INK, "mast")
text_r(1012, 32, STRAP, SANSB13, INK, "mast")
text_r(1012, 52, "All times UTC · One day only", SANS11, GREY, "mast")
line(12, 80, 1012, 80, RED, 3, "mast")

# ---------------- UTC timeline ----------------
TL = [("00:58", "BOK RATE RISE"), ("05:28", "EBOLA SURGE"),
      ("07:45", "BANGKOK BLAST"), ("13:21", "UK MIGRATION"),
      ("15:36", "KUWAIT STRIKE"), ("16:55", "TRUMP GDP ROW"),
      ("23:49", "ZELENSKY TALKS")]
for i, (tm, cap) in enumerate(TL):
    tx = 12 + i * 142
    text(tx + 2, 88, tm, SANSB13, RED, "tl")
    text(tx + 42, 90, cap, SANS11, INK, "tl")
    hcheck(tx + 42, 90, cap, SANS11, 96, f"tl cap {i}")
    if i:
        line(tx - 6, 90, tx - 6, 103, GREY, 1, "tl")
line(12, 106, 1012, 106, INK, 1, "tl")

# ---------------- hero scenes (148x80) ----------------
def scene_kuwait(x, y):
    d.rectangle([x + 16, y + 40, x + 84, y + 72], fill=(198, 202, 206), outline=INK, width=2)
    d.rectangle([x + 100, y + 26, x + 107, y + 72], fill=(120, 116, 108), outline=INK, width=2)
    d.rectangle([x + 88, y + 18, x + 120, y + 26], fill=(88, 84, 78), outline=INK, width=1)
    d.line([(x + 94, y + 40), (x + 113, y + 40)], fill=INK, width=2)
    d.line([(x + 94, y + 52), (x + 113, y + 52)], fill=INK, width=2)
    d.rectangle([x + 26, y + 48, x + 40, y + 58], fill=(170, 205, 225), outline=INK, width=1)
    d.rectangle([x + 52, y + 48, x + 66, y + 58], fill=(170, 205, 225), outline=INK, width=1)
    d.ellipse([x + 118, y + 8, x + 140, y + 16], fill=INK)
    d.line([(x + 112, y + 12), (x + 146, y + 12)], fill=INK, width=2)
    for fx, fh, col in ((x + 30, 18, RED), (x + 44, 24, GOLD), (x + 58, 16, RED)):
        d.polygon([(fx, y + 40), (fx + 6, y + 40 - fh), (fx + 12, y + 40)], fill=col)
    obstacle(x + 14, y + 6, x + 148, y + 72, "hero1")


def scene_storm(x, y):
    d.ellipse([x + 14, y + 4, x + 74, y + 26], fill=(120, 116, 108))
    d.ellipse([x + 52, y + 0, x + 112, y + 22], fill=(88, 84, 78))
    d.ellipse([x + 96, y + 6, x + 140, y + 24], fill=(120, 116, 108))
    for rx in (x + 24, x + 52, x + 80, x + 108, x + 130):
        d.line([(rx, y + 28), (rx - 5, y + 42)], fill=NAVY, width=2)
    d.line([(x + 122, y + 72), (x + 134, y + 34)], fill=INK, width=3)
    d.line([(x + 116, y + 44), (x + 140, y + 40)], fill=INK, width=2)
    d.rectangle([x + 16, y + 50, x + 62, y + 72], fill=CREAM, outline=INK, width=2)
    d.polygon([(x + 16, y + 50), (x + 39, y + 36), (x + 62, y + 50)], fill=RED, outline=INK, width=2)
    d.rectangle([x + 26, y + 56, x + 34, y + 64], fill=INK)
    d.rectangle([x + 46, y + 56, x + 54, y + 64], fill=INK)
    obstacle(x + 12, y + 0, x + 142, y + 72, "hero2")


def scene_ecb(x, y):
    for sx, sy in ((x + 20, y + 8), (x + 132, y + 10), (x + 118, y + 30), (x + 34, y + 30)):
        d.line([(sx - 3, sy), (sx + 3, sy)], fill=GOLD, width=1)
        d.line([(sx, sy - 3), (sx, sy + 3)], fill=GOLD, width=1)
    d.rectangle([x + 30, y + 22, x + 118, y + 72], fill=CREAM, outline=INK, width=2)
    d.polygon([(x + 30, y + 22), (x + 74, y + 6), (x + 118, y + 22)], fill=CREAM, outline=INK, width=2)
    for colx in (x + 40, x + 58, x + 90, x + 108):
        d.rectangle([colx, y + 26, colx + 7, y + 72], fill=NAVY)
    d.text((x + 66, y + 34), "€", font=SERIF36, fill=NAVY)
    obstacle(x + 28, y + 4, x + 120, y + 72, "hero3")


SCENES = [scene_kuwait, scene_storm, scene_ecb]
PLATES = ["KUWAIT", "STORM", "ECB"]

# ---------------- top zone: heroes left ----------------
TOP = 112
HH = 92
for i, (place, reg, field, head, deck, src, sure) in enumerate(HEROES):
    hy = TOP + i * HH
    if i:
        line(12, hy, 575, hy, GREY, 1, f"hero{i + 1}")
    bg = NAVY if i == 2 else CREAM
    d.rectangle([12, hy + 5, 575, hy + HH - 4], fill=bg)
    sx, sy = 20, hy + 6
    d.rectangle([sx, sy, sx + 148, sy + 80], fill=(24, 26, 34) if i != 1 else (210, 208, 198))
    if i == 2:
        d.rectangle([sx, sy, sx + 148, sy + 80], fill=NAVY)
    SCENES[i](sx, sy)
    d.rectangle([sx, sy + 64, sx + 148, sy + 80], fill=INK)
    text_c(sx + 74, sy + 65, PLATES[i], SANSB14, (255, 255, 255), f"hero{i + 1}")
    tx = 180
    kick = f"{place.upper()} — {field.upper()}"
    text(tx, hy + 6, kick, SANSB14, RED if i != 2 else GOLD, f"hero{i + 1}")
    hcheck(tx, hy + 6, kick, SANSB14, 250, f"hero{i + 1} kicker")
    chip(567, hy + 5, sure, f"hero{i + 1}")
    text_r(567, hy + 26, src, SANS11, GREY if i != 2 else CREAM, f"hero{i + 1}")
    text(tx, hy + 24, head, SERIF40, INK if i != 2 else (255, 255, 255), f"hero{i + 1}")
    hcheck(tx, hy + 24, head, SERIF40, 387, f"hero{i + 1} headline")
    text(tx, hy + 68, deck, SANS16, INK if i != 2 else CREAM, f"hero{i + 1}")
    hcheck(tx, hy + 68, deck, SANS16, 387, f"hero{i + 1} deck")

# ---------------- top zone: map panel right ----------------
MX0, MY0, MX1, MY1 = 587, 112, 1012, 390
d.rectangle([MX0, MY0, MX1, MY1], fill=NAVY)
text(MX0 + 10, MY0 + 6, "WHERE IT HAPPENED", SANSB14, GOLD, "map")
MAPX, MAPY, MAPW, MAPH = 597, 140, 405, 188
CONTINENTS = [(-100, 48, 55, 16), (-85, 38, 25, 9), (-95, 62, 30, 8), (-155, 64, 14, 5),
              (-40, 74, 12, 5), (-62, -12, 14, 14), (-70, -25, 8, 12), (-48, -20, 9, 8),
              (15, 50, 22, 7), (28, 55, 14, 6), (10, 62, 16, 6), (5, 44, 10, 4),
              (20, 8, 24, 14), (22, -12, 16, 10), (47, 5, 8, 5),
              (45, 27, 12, 6), (36, 33, 10, 6), (43, 20, 9, 7),
              (60, 50, 35, 10), (95, 48, 25, 9), (78, 22, 10, 8), (108, 32, 16, 9),
              (100, 14, 7, 6), (135, 35, 8, 4), (127, 39, 6, 4),
              (113, -2, 16, 3), (95, 3, 8, 3), (134, -25, 14, 7), (122, -24, 8, 5),
              (172, -42, 5, 4)]


def proj(lon, lat):
    return (MAPX + (lon + 168) / 360 * MAPW,
            MAPY + (80 - lat) / 135 * MAPH)


for gy in range(0, MAPH, 9):
    for gx in range(0, MAPW, 9):
        lon = -168 + gx / MAPW * 360
        lat = 80 - gy / MAPH * 135
        for clon, clat, rx, ry in CONTINENTS:
            if ((lon - clon) / rx) ** 2 + ((lat - clat) / ry) ** 2 <= 1:
                d.ellipse([MAPX + gx - 1, MAPY + gy - 1, MAPX + gx + 1, MAPY + gy + 1],
                          fill=(150, 160, 190))
                break

PIN_POS = {  # story no: (lon, lat, dx, dy)
    1: (47.98, 29.38, 10, -8), 2: (-74.0, 40.7, 14, -12), 3: (4.35, 50.85, 0, 0),
    4: (-77.0, 38.9, -14, 12), 5: (34.35, 31.42, -16, 10), 6: (42.55, 16.89, 0, 0),
    7: (30.52, 50.45, 0, 0), 8: (4.35, 50.85, -16, 18), 9: (30.25, 1.57, 0, 0),
    10: (-46.63, -23.55, 0, 0), 11: (125.75, 39.04, 0, 0),
}
PINS = {}
for n, (lon, lat, dx, dy) in PIN_POS.items():
    px, py = proj(lon, lat)
    px, py = px + dx, py + dy
    PINS[n] = (px, py)
    d.ellipse([px - 10, py - 10, px + 10, py + 10], fill=CREAM, outline=INK, width=2)
    text_c(px, py - 7, str(n), SANSB12, INK, f"pin{n}")
    obstacle(px - 10, py - 10, px + 10, py + 10, f"pin{n}")

# tally bar inside the map panel
TB_Y = 350
text(MX0 + 10, TB_Y - 16, "STORIES BY REGION — COUNTED FROM THE TABLE", SANS11, CREAM, "map")
tx = MAPX
for reg in ("EUR", "ASI", "AME", "MEA", "AFR", "OCE"):
    if not TALLY[reg]:
        continue
    segw = TALLY[reg] / TOTAL * MAPW
    d.rectangle([tx, TB_Y, tx + segw, TB_Y + 14], fill=GOLD if reg in ("EUR", "ASI") else CREAM,
                outline=NAVY, width=1)
    tx += segw
regs_drawn = [r for r in ("EUR", "ASI", "AME", "MEA", "AFR", "OCE") if TALLY[r]]
for idx, reg in enumerate(regs_drawn):
    text_c(MAPX + (idx + 0.5) * MAPW / len(regs_drawn), TB_Y + 17,
           f"{reg} {TALLY[reg]}", SANS11, CREAM, "map")

# ---------------- numbers strip ----------------
SY = 396
NUMS = [(fig("storm_outages"), "STORM — PEAK OUTAGES", "Parade postponed"),
        (fig("kuwait_killed"), "CONFLICT — KILLED IN KUWAIT", "Italy blames Iran; Iran denies"),
        (fig("ebola_cases"), "HEALTH — EBOLA", "5,904 deaths"),
        (fig("bovespa_rise"), "MARKETS — BOVESPA", "STOXX up 1.8%")]
line(12, SY, 1012, SY, INK, 2, "strip")
for i, (num, role, ctx) in enumerate(NUMS):
    cx = 12 + i * 250
    if i:
        line(cx, SY + 4, cx, SY + 34, GREY, 1, "strip")
    text(cx + 2, SY + 6, num, SERIF28, RED, "strip")
    nw = d.textlength(num, font=SERIF28)
    rx = cx + nw + 16
    text(rx, SY + 5, role, SANSB12, INK, "strip")
    hcheck(rx, SY + 5, role, SANSB12, cx + 244 - rx, f"strip role {i}")
    text(rx, SY + 24, ctx, SANS11, GREY, "strip")
    hcheck(rx, SY + 24, ctx, SANS11, cx + 244 - rx, f"strip ctx {i}")
line(12, SY + 40, 1012, SY + 40, INK, 1, "strip")

# ---------------- card pictograms (72px medallions) ----------------
def pic_podium(cx, cy):
    d.rectangle([cx - 22, cy - 2, cx + 22, cy + 27], fill=NAVY, outline=INK, width=2)
    d.ellipse([cx - 12, cy - 24, cx + 12, cy + 0], fill=(198, 202, 206), outline=INK, width=2)
    d.line([(cx, cy - 24), (cx, cy - 2)], fill=INK, width=3)
    d.rectangle([cx - 16, cy + 10, cx + 16, cy + 18], fill=CREAM, outline=INK, width=1)


def pic_building(cx, cy):
    d.rectangle([cx - 24, cy - 26, cx + 10, cy + 27], fill=(198, 202, 206), outline=INK, width=2)
    for wy in (cy - 18, cy - 4, cy + 10):
        for wx in (cx - 18, cx - 6):
            d.rectangle([wx, wy, wx + 8, wy + 9], fill=NAVY)
    d.rectangle([cx + 10, cy + 2, cx + 26, cy + 27], fill=(120, 116, 108), outline=INK, width=2)
    d.line([(cx + 10, cy + 2), (cx + 26, cy + 16)], fill=INK, width=2)


def pic_refinery(cx, cy):
    d.rectangle([cx - 26, cy + 14, cx + 26, cy + 27], fill=(198, 202, 206), outline=INK, width=2)
    d.rectangle([cx - 20, cy - 20, cx - 8, cy + 14], fill=GREY, outline=INK, width=2)
    d.rectangle([cx + 8, cy - 26, cx + 18, cy + 14], fill=GREY, outline=INK, width=2)
    d.polygon([(cx + 13, cy - 26), (cx + 17, cy - 34), (cx + 21, cy - 26)], fill=RED)
    d.line([(cx - 8, cy - 6), (cx + 8, cy - 6)], fill=INK, width=3)


def pic_missile(cx, cy):
    d.polygon([(cx - 6, cy - 27), (cx + 14, cy - 7), (cx + 6, cy + 1), (cx - 14, cy - 19)],
              fill=(198, 202, 206), outline=INK, width=2)
    d.polygon([(cx - 14, cy - 19), (cx - 24, cy - 9), (cx - 16, cy - 3)], fill=RED)
    d.polygon([(cx - 20, cy + 8), (cx - 8, cy + 20), (cx - 26, cy + 22)], fill=GOLD)
    d.polygon([(cx - 12, cy + 16), (cx - 2, cy + 26), (cx - 18, cy + 27)], fill=RED)


def pic_euro(cx, cy):
    d.ellipse([cx - 27, cy - 27, cx + 27, cy + 27], fill=GOLD, outline=INK, width=2)
    d.text((cx - 15, cy - 26), "€", font=SERIF36, fill=INK)


def pic_cross(cx, cy):
    d.ellipse([cx - 27, cy - 27, cx + 27, cy + 27], fill=CREAM, outline=INK, width=2)
    d.rectangle([cx - 7, cy - 19, cx + 7, cy + 19], fill=RED)
    d.rectangle([cx - 19, cy - 7, cx + 19, cy + 7], fill=RED)


def pic_chart_up(cx, cy):
    d.line([(cx - 27, cy + 27), (cx + 27, cy + 27)], fill=INK, width=2)
    d.line([(cx - 27, cy - 27), (cx - 27, cy + 27)], fill=INK, width=2)
    d.line([(cx - 21, cy + 16), (cx - 6, cy + 2), (cx + 6, cy + 10), (cx + 21, cy - 16)],
           fill=RED, width=5)
    d.polygon([(cx + 21, cy - 16), (cx + 10, cy - 15), (cx + 20, cy - 5)], fill=RED)


def pic_atom(cx, cy):
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=RED, outline=INK, width=2)
    d.ellipse([cx - 27, cy - 13, cx + 27, cy + 13], outline=NAVY, width=3)
    d.ellipse([cx - 13, cy - 27, cx + 13, cy + 27], outline=NAVY, width=3)


PICS = [pic_podium, pic_building, pic_refinery, pic_missile, pic_euro,
        pic_cross, pic_chart_up, pic_atom]

# ---------------- cards 4x2 ----------------
CY0 = 444
CH = 124
MEDALS = []
for i, (place, reg, field, head, deck, src, sure) in enumerate(CARDS):
    n = i + 4
    cx = 12 + (i % 4) * 250
    cy = CY0 + (i // 4) * CH
    if i % 4:
        line(cx - 6, cy + 8, cx - 6, cy + CH - 8, GREY, 1, f"card{n}")
    if i // 4:
        line(cx, cy - 4, cx + 238, cy - 4, GREY, 1, f"card{n}")
    mx, my = cx + 8, cy + 10
    d.rectangle([mx, my, mx + 72, my + 72], fill=CREAM, outline=INK, width=2)
    PICS[i](mx + 36, my + 36)
    MEDALS.append((mx, my, mx + 72, my + 72, n))
    obstacle(mx, my, mx + 72, my + 72, f"card{n}")
    d.ellipse([mx - 2, my - 2, mx + 20, my + 20], fill=INK)
    text_c(mx + 9, my + 2, str(n), SANSB12, (255, 255, 255), f"card{n}")
    text(cx + 88, cy + 10, place.upper(), SANSB13, RED, f"card{n}")
    sq_col = NAVY if sure == "C" else RED
    d.rectangle([cx + 219, cy + 8, cx + 238, cy + 27], fill=sq_col)
    text_c(cx + 228, cy + 11, sure, SANSB12, (255, 255, 255), f"card{n}")
    hl = wrap(head, SERIF30, 150)
    if len(hl) > 2:
        FAILS.append(f"WRAP-FAIL card{n} headline: '{head}' needs {len(hl)} lines > 2")
    for j, ln in enumerate(hl[:2]):
        text(cx + 88, cy + 32 + j * 34, ln, SERIF30, INK, f"card{n}h")
    text(cx + 8, cy + 102, deck, SANS16, INK, f"card{n}")
    hcheck(cx + 8, cy + 102, deck, SANS16, 190, f"card{n} deck")
    text_r(cx + 238, cy + 104, src, SANS11, GREY, f"card{n}")

# ---------------- bottom zone ----------------
BY = 700
text(12, BY, "ALSO ON THURSDAY 26 NOVEMBER", SANSB15, RED, "also-head")
ALSO_COLS = [(12, ALSO[:10]), (362, ALSO[10:])]
for colx, items in ALSO_COLS:
    for j, (place, reg, field, main, sub, sure) in enumerate(items):
        yy = BY + 24 + j * 30
        main_s = f"{place} — {main}"
        text(colx, yy, main_s, SANSB18, INK, "also")
        mw = d.textlength(main_s, font=SANSB18)
        text(colx + mw + 8, yy + 4, sub, SANS14, GREY, "also")
        tot = mw + 8 + d.textlength(sub, font=SANS14)
        if tot > 348:
            FAILS.append(f"H-FAIL also row {place}: combined width {tot:.0f} over limit")
        if sure == "R":
            text_r(colx + 348, yy + 4, "R", SANSB12, RED, "also")

DC_TEXT = ("All stories: Thu 26 Nov 2026. "
           "Wed 25 Nov — NOT Thu news: tariff proposals; Cairo tanker fire; "
           "Shenzhou-24 launch; US GDP revision; "
           "Miss Universe; Solomon treaty. "
           "Tue 24 Nov: Senegal AFCON title; Huawei verdict. "
           "NOT YET: Macy's parade Sat 28 Nov; ECB appointment Dec; "
           "EU budget talks 17-18 Dec; Spain vote Sun 29 Nov; "
           "González return 5 Dec.")
DX, DY = 712, 698
d.rectangle([DX, DY, 1012, 892], outline=INK, width=2)
text(DX + 12, DY + 10, "DATE CHECK", SANSB13, RED, "dc")
dl = wrap(DC_TEXT, SANS13, 276)
if len(dl) > 9:
    FAILS.append(f"WRAP-FAIL date check: needs {len(dl)} lines > 9")
for j, ln in enumerate(dl[:9]):
    text(DX + 12, DY + 32 + j * 18, ln, SANS13, INK, "dc")
text(DX + 12, 904, "HOW SURE", SANSB13, RED, "how")
text(DX + 12, 924, "CONFIRMED", SANSB12, NAVY, "how")
text(DX + 96, 924, "— 2+ outlets agree", SANS12, INK, "how")
text(DX + 12, 944, "REPORTED", SANSB12, RED, "how")
text(DX + 96, 944, "— one outlet or a claim", SANS12, INK, "how")
srcs = []
for s in HEROES + CARDS:
    if s[5] and s[5] not in srcs:
        srcs.append(s[5])
FOOT = (f"Sources: {' · '.join(srcs[:5])} + {len(srcs) - 5} more"
        if len(srcs) > 5 else f"Sources: {' · '.join(srcs)}")
text(DX + 12, 968, FOOT, SANS11, GREY, "foot")
text(DX + 12, 986, "Figures: figures.json registry", SANS11, GREY, "foot")

# ---------------- audits ----------------
def overlap(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def gap(a, b):
    dx = max(b[0] - a[2], a[0] - b[2], 0)
    dy = max(b[1] - a[3], a[1] - b[3], 0)
    return max(dx, dy) if (dx or dy) else -1


findings = []
for i, a in enumerate(TEXTS):
    for b in TEXTS[i + 1:]:
        if a[5].rstrip("h") == b[5].rstrip("h") and a[5].endswith("h"):
            continue
        if a[5] == b[5] and a[5].startswith(("hero", "pin", "card")):
            continue
        if overlap(a, b):
            findings.append(f"TEXT overlap: '{a[4]}' <> '{b[4]}'")
        elif 0 <= gap(a, b) < 3:
            findings.append(f"TEXT gap<3: '{a[4]}' <> '{b[4]}' ({gap(a, b):.1f}px)")
print(f"TEXT-AUDIT: {len(findings)} finding(s)")
for f_ in findings:
    print("  ", f_)

findings = []
for t in TEXTS:
    for ln in LINES:
        if ln[4] == t[5]:
            continue
        box = (ln[0], ln[1], ln[2], ln[3])
        if overlap(t, box):
            findings.append(f"LINE overlap: '{t[4]}' x {ln[4]}")
        elif 0 <= gap(t, box) < 3:
            findings.append(f"LINE gap<3: '{t[4]}' x {ln[4]} ({gap(t, box):.1f}px)")
print(f"LINE-AUDIT: {len(findings)} finding(s)")
for f_ in findings:
    print("  ", f_)

findings = []
for t in TEXTS:
    for g in GFX:
        if g[4] == t[5] or (t[5].startswith("pin") and g[4] == t[5]):
            continue
        if t[5].startswith("pin") and g[4].startswith("pin"):
            continue
        box = (g[0], g[1], g[2], g[3])
        if overlap(t, box):
            findings.append(f"GFX overlap: '{t[4]}' x obstacle {g[4]}")
        elif 0 <= gap(t, box) < 3:
            findings.append(f"GFX gap<3: '{t[4]}' x obstacle {g[4]} ({gap(t, box):.1f}px)")
print(f"GFX-AUDIT: {len(findings)} finding(s)")
for f_ in findings:
    print("  ", f_)

findings = []
for (x0, y0, x1, y1, n) in MEDALS:
    px = img.load()
    ink = 0
    for yy in range(y0 + 4, y1 - 4):
        for xx in range(x0 + 4, x1 - 4):
            r, g, b = px[xx, yy]
            if r < 90 and g < 90 and b < 90:
                ink += 1
    if ink < 60:
        findings.append(f"MEDAL {n}: only {ink} dark px inside frame")
print(f"MEDAL-AUDIT: {len(findings)} finding(s)")
for f_ in findings:
    print("  ", f_)

findings = []
pns = list(PINS.items())
for i, (n1, (x1, y1)) in enumerate(pns):
    for n2, (x2, y2) in pns[i + 1:]:
        dist = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        if dist < 23:
            findings.append(f"PIN {n1}<>PIN {n2}: centre distance {dist:.1f} < 23")
    if not (MAPX <= x1 <= MAPX + MAPW and MAPY <= y1 <= MAPY + MAPH):
        findings.append(f"PIN {n1}: outside map area")
print(f"PIN-AUDIT: {len(findings)} finding(s)")
for f_ in findings:
    print("  ", f_)

findings = []
for t in TEXTS:
    if t[5] in ("mast", "tl") and (t[0] < 12 or t[2] > 1012):
        findings.append(f"MASTHEAD: '{t[4]}' escapes page")
for t in TEXTS:
    if t[5] == "dc" and not (DX <= t[0] and t[2] <= 1012 and DY <= t[1] and t[3] <= 892):
        findings.append(f"DC: '{t[4]}' escapes box")
print(f"BOX-AUDIT: {len(findings)} finding(s)")
for f_ in findings:
    print("  ", f_)

warn = []
img_texts = " ".join(t[4] for t in TEXTS)
for k, disp in REG.items():
    if disp not in img_texts:
        warn.append(f"FIG not drawn: {k} display '{disp}'")
print(f"FIG-SELFCHECK (WARN only): {len(warn)} finding(s)")
for f_ in warn:
    print("  ", f_)

total = 0
print(f"TOTAL FAIL: {len(FAILS)}")
for f_ in FAILS:
    print("  ", f_)

img.save(HERE / "entry.png")
print("saved", HERE / "entry.png", img.size)
