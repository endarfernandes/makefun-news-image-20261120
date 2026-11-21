#!/usr/bin/env python3
"""Render 'THE WORLD IN ONE DAY' — Friday 20 November 2026 — as 1024x1024 PNG.

Build-time renderer (Pillow + Liberation fonts, both present on the build
machine). Deterministic: no randomness, no timestamps, no network. Re-running
this script must produce byte-identical output (verified by SHA-256).

The grading entrypoint (main.py, pure stdlib) copies the rendered entry.png
to $MAKEFUN_OUTPUT_DIR/entry.png; see RULES.txt ("the simplest entry is a
repository holding the image and a one-line program that copies it there").

Layout (1024 x 1024, cream broadsheet):
  kicker + masthead + standfirst + region tabs
  numbers strip (6 cells)
  3 illustrated leads
  world map band ("WHERE IT HAPPENED")
  10 illustrated secondaries (2 rows x 5)
  "ALSO ON FRIDAY 20 NOVEMBER" brief tail (3 columns)
  DATE CHECK footer + sources
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
PAPER = (250, 246, 238)   # cream
INK = (16, 16, 16)        # near-black
RED = (178, 34, 34)       # accent red
NAVY = (11, 31, 75)       # map ocean
NAVY_D = (7, 20, 50)
GOLD = (201, 162, 39)
SKY = (126, 184, 228)
SKY_D = (70, 110, 170)
SAND = (214, 196, 148)    # map land
SAND_D = (180, 158, 105)
GREY = (120, 122, 128)
GREY_L = (225, 220, 210)  # hairlines
WHITE = (255, 255, 255)
GREEN = (46, 125, 50)
ORANGE = (230, 110, 30)
TEAL = (0, 121, 107)

# ---------------------------------------------------------------- fonts
FDIR = "/usr/share/fonts/truetype/liberation"
def font(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)

SERIF_B = "LiberationSerif-Bold.ttf"
SERIF = "LiberationSerif-Regular.ttf"
SERIF_I = "LiberationSerif-Italic.ttf"
SANS_B = "LiberationSans-Bold.ttf"
SANS = "LiberationSans-Regular.ttf"
SANS_I = "LiberationSans-Italic.ttf"

# ---------------------------------------------------------------- canvas
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def rect(x0, y0, x1, y1, fill=None, outline=None, width=1):
    d.rectangle([x0, y0, x1, y1], fill=fill, outline=outline, width=width)

def hline(x0, x1, y, fill=INK, width=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)

def vline(x, y0, y1, fill=INK, width=1):
    d.line([(x, y0), (x, y1)], fill=fill, width=width)

def text(x, y, s, f, fill=INK, anchor="la"):
    d.text((x, y), s, font=f, fill=fill, anchor=anchor)

def tw(s, f):
    """Pixel width of string s in font f."""
    return d.textlength(s, font=f)

def wrap(s, f, maxw):
    """Greedy word wrap; returns list of lines that fit maxw."""
    words = s.split()
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(t, f) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def para(x, y, s, f, maxw, fill=INK, leading=None):
    """Draw wrapped paragraph; returns y after last line."""
    if leading is None:
        leading = int(f.size * 1.22)
    for line in wrap(s, f, maxw):
        text(x, y, line, f, fill=fill)
        y += leading
    return y

def centre(x0, x1, y, s, f, fill=INK):
    text((x0 + x1) // 2, y, s, f, fill=fill, anchor="ma")

def kicker(x, y, s, size=13, fill=RED):
    text(x, y, s, font(SANS_B, size), fill=fill)

# ---------------------------------------------------------------- world map
# Hand-plotted coarse continent outlines (lon, lat). Schematic but
# geographically faithful in relative position and shape.
NORTH_AMERICA = [
    (-168, 66), (-161, 58), (-153, 58), (-146, 60), (-137, 58), (-131, 54),
    (-125, 49), (-124, 42), (-120, 34), (-114, 29), (-109, 23), (-105, 20),
    (-97, 16), (-92, 15), (-86, 12), (-83, 9), (-79, 9), (-81, 13),
    (-84, 16), (-87, 21), (-90, 21), (-91, 19), (-96, 19), (-97, 26),
    (-94, 29), (-89, 30), (-84, 30), (-81, 26), (-80, 32), (-76, 35),
    (-74, 40), (-70, 42), (-66, 44), (-60, 47), (-55, 47), (-53, 50),
    (-56, 53), (-60, 55), (-65, 58), (-70, 62), (-77, 62), (-85, 66),
    (-92, 66), (-96, 69), (-110, 68), (-125, 70), (-141, 70), (-155, 71),
    (-163, 70), (-168, 66),
]
GREENLAND = [
    (-44, 60), (-40, 64), (-32, 68), (-25, 70), (-22, 70), (-25, 74),
    (-32, 76), (-42, 77), (-52, 76), (-58, 74), (-55, 70), (-53, 66),
    (-48, 63), (-44, 60),
]
SOUTH_AMERICA = [
    (-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
    (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-74, -50), (-70, -54),
    (-66, -55), (-65, -50), (-62, -44), (-58, -38), (-52, -33), (-49, -28),
    (-41, -23), (-39, -17), (-35, -9), (-35, -6), (-41, -3), (-44, -2),
    (-50, 0), (-52, 4), (-55, 6), (-60, 8), (-62, 9), (-68, 11),
    (-72, 12), (-77, 11), (-79, 9),
]
AFRICA = [
    (-17, 15), (-17, 21), (-15, 27), (-10, 31), (-6, 34), (0, 36),
    (10, 37), (11, 34), (19, 32), (25, 32), (30, 31), (32, 31),
    (34, 28), (35, 23), (37, 18), (39, 15), (43, 12), (48, 11),
    (51, 12), (48, 4), (42, -2), (40, -8), (36, -14), (35, -20),
    (33, -26), (28, -33), (20, -35), (17, -32), (15, -27), (12, -18),
    (13, -12), (9, -4), (9, 4), (-8, 5), (-13, 8), (-17, 15),
]
EURASIA = [
    (-10, 36), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 50),
    (2, 51), (4, 53), (8, 57), (10, 59), (5, 60), (5, 62),
    (12, 64), (18, 69), (25, 71), (32, 70), (40, 68), (44, 68),
    (50, 69), (58, 69), (66, 70), (73, 71), (80, 73), (90, 75),
    (100, 76), (110, 74), (120, 73), (130, 72), (140, 72), (150, 70),
    (160, 70), (170, 67), (178, 65), (170, 60), (162, 56), (158, 53),
    (150, 59), (142, 54), (140, 48), (135, 43), (130, 42), (127, 40),
    (126, 38), (122, 39), (120, 35), (122, 31), (120, 28), (116, 23),
    (110, 21), (108, 18), (105, 10), (103, 8), (100, 7), (98, 10),
    (95, 16), (92, 21), (89, 22), (86, 20), (83, 18), (80, 15),
    (77, 8), (75, 12), (73, 17), (70, 20), (67, 23), (62, 25),
    (58, 25), (56, 27), (54, 26), (51, 28), (49, 30), (48, 30),
    (44, 29), (42, 27), (40, 25), (38, 21), (35, 29), (34, 31),
    (30, 36), (26, 38), (23, 36), (19, 40), (16, 38), (12, 44),
    (8, 44), (3, 43), (0, 40), (-2, 37), (-6, 36), (-10, 36),
]
AUSTRALIA = [
    (113, -22), (114, -30), (115, -35), (118, -35), (124, -33), (129, -32),
    (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
    (153, -32), (153, -27), (150, -23), (146, -19), (142, -15), (142, -11),
    (137, -12), (136, -15), (132, -12), (130, -13), (126, -14), (122, -17),
    (118, -20), (113, -22),
]
MADAGASCAR = [(44, -16), (47, -15), (50, -16), (49, -20), (46, -24), (44, -21), (43, -18), (44, -16)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51), (-3, 50), (-5, 50)]
JAPAN = [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (140, 38), (141, 41), (142, 44), (144, 44), (141, 40), (140, 37), (137, 37), (134, 36), (132, 34), (130, 31)]
NEW_ZEALAND = [(167, -45), (170, -43), (173, -41), (175, -38), (177, -38), (175, -40), (173, -42), (170, -44), (167, -45)]
INDONESIA = [(95, 5), (98, 3), (101, 0), (104, -3), (107, -6), (110, -7), (113, -8), (116, -9), (119, -9), (121, -7), (124, -6), (127, -4), (129, -2), (131, -1), (128, 1), (124, 1), (120, 0), (117, 1), (114, 3), (110, 1), (107, -1), (103, 1), (99, 4), (95, 5)]
PHILIPPINES = [(120, 14), (121, 16), (122, 18), (121, 16), (123, 14), (124, 11), (122, 9), (121, 12), (120, 14)]
CONTINENTS = [NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, AFRICA, EURASIA,
              AUSTRALIA, MADAGASCAR, UK, JAPAN, NEW_ZEALAND, INDONESIA, PHILIPPINES]

MAP_LON0, MAP_LON1 = -170, 190
MAP_LAT0, MAP_LAT1 = 84, -58   # top, bottom

# ---------------------------------------------------------------- story data
# Sources: research/RESEARCH.md (each story verified vs >=2 reliable sources).
# Briefs 09-13 and the tail are filled from research/BRIEFS.md when it lands.
LEADS = [
    dict(num=1, kicker="UKRAINE · POLAND — WAR", region="EUROPE",
         headline="MISSILES FALL ON NATO SOIL",
         deck="Russia's largest strike of the year: 110+ missiles, 400+ drones; at least 8 killed, 3 Kyiv bridges hit. A Kh-101 missile lands in Poland — NATO jets scrambled.",
         source="Reuters · AP", scene="missiles", tag="CONFIRMED"),
    dict(num=2, kicker="MARKETS — WALL STREET", region="AMERICAS",
         headline="NASDAQ ERASES ITS YEAR",
         deck="Nasdaq −5.28%, −1,261 points — the second-biggest one-day points drop ever. S&P 500 −3.7%, in correction. Anthropic −8.5% to $88.91 a day after its record IPO.",
         source="CNN · Reuters", scene="markets", tag="CONFIRMED"),
    dict(num=3, kicker="WASHINGTON — AFTER SHENZHEN", region="AMERICAS",
         headline="TRUMP: “VERY GOOD” TALKS",
         deck="A day after Shenzhen, the White House hails the Putin talks. US–China AI guardrails keep humans in military-AI decisions.",
         source="Reuters", scene="podium", tag="CONFIRMED"),
]

SECONDARIES = [
    dict(num=4, kicker="BRUSSELS — BREXIT RESET", region="EUROPE",
         headline="UK AND EU SEAL THE RESET",
         deck="Food checks scrapped; 100,000 youth visas a year.",
         source="Reuters", scene="handshake", tag="CONFIRMED"),
    dict(num=5, kicker="THE HAGUE — JUSTICE", region="EUROPE",
         headline="MYANMAR REJECTS 9–6 VERDICT",
         deck="Naypyitaw calls it “unfair”; UK expels attaché.",
         source="AP · Reuters", scene="gavel", tag="CONFIRMED"),
    dict(num=6, kicker="ANTALYA — CLIMATE", region="EUROPE",
         headline="COP31 DRAFT DROPS PHASE-OUT",
         deck="Fossil-fuel exit cut from the draft.",
         source="Reuters", scene="draft", tag="CONFIRMED"),
    dict(num=7, kicker="ODISHA — WEATHER", region="ASIA",
         headline="CYCLONE AKVAN MAKES LANDFALL",
         deck="300,000+ evacuated; no deaths in first hours.",
         source="IMD · Reuters", scene="cyclone", tag="CONFIRMED"),
    dict(num=8, kicker="NEW YORK — UNITED NATIONS", region="AMERICAS",
         headline="RACE FOR UN CHIEF STALLS",
         deck="Two veto powers reject Grynspan; poll 10 in favour, 4 against.",
         source="Reuters", scene="un", tag="REPORTED"),
    dict(num=9, kicker="BAGHDAD — IRAQ", region="MIDDLE EAST",
         headline="IRAQ MOVES ON KATAIB HEZBOLLAH",
         deck="Forces deploy in the militia stronghold of Jurf al-Sakhar.",
         source="Reuters", scene="raid", tag="CONFIRMED"),
    dict(num=10, kicker="THE GULF — EXPLAINED", region="MIDDLE EAST",
         headline="QESHM BLAST WAS MUNITIONS",
         deck="Blast was ordnance disposal, not a strike.",
         source="Tasnim · Reuters", scene="blast", tag="CONFIRMED"),
    dict(num=11, kicker="WASHINGTON — POLITICS", region="AMERICAS",
         headline="VANCE DUCKS IRAN QUESTION",
         deck="Declines to say he would have ordered the strikes.",
         source="Reuters", scene="split", tag="CONFIRMED"),
    dict(num=12, kicker="LUANDA — AFRICA · ECONOMY", region="AFRICA",
         headline="ANGOLA BUYS INTO DE BEERS",
         deck="$180m for a 10% stake in the diamond giant.",
         source="Reuters", scene="diamond", tag="CONFIRMED"),
    dict(num=13, kicker="PARIS — SECURITY COUNCIL", region="EUROPE",
         headline="FRANCE SEEKS UNSC MEETING",
         deck="Paris calls for an emergency session after the Kyiv strikes.",
         source="Reuters", scene="unsc", tag="CONFIRMED"),
]

# One-line briefs (place — what happened — region). All verified 20 Nov 2026
# (research/RESEARCH.md + research/BRIEFS.md). Somalia excluded: 19 Nov event.
BRIEFS = [
    ("LONDON", "Burnham hails EU reset as “win-win”.", "EUROPE"),
    ("WARSAW", "Tusk: incursions an “intentional provocation”.", "EUROPE"),
    ("BRUSSELS", "Rutte calls it a “grave violation”.", "EUROPE"),
    ("WASHINGTON", "Bessent: humans stay in military-AI calls.", "AMERICAS"),
    ("NEW YORK", "Dow and S&P both in correction territory.", "AMERICAS"),
    ("SAN FRANCISCO", "Anthropic closes $88.91, −8.5% after debut.", "AMERICAS"),
    ("ANTALYA", "Talks run on; no final COP31 deal yet.", "EUROPE"),
    ("NAYPYITAW", "Junta spokesperson: verdict “unfair”.", "ASIA"),
    ("THE HAGUE", "ICJ reading was 9–6; verdict final, binding.", "EUROPE"),
    ("WHITE HOUSE", "Trump threatens “tremendous tax” abroad.", "AMERICAS"),
    ("WASHINGTON", "Consumer sentiment rises to 51.5 in Nov.", "AMERICAS"),
    ("HAMBURG", "XFEL sets X-ray laser record: 0.04 nm.", "EUROPE"),
    ("NEW HAVEN", "Yale finds excitons in a single atomic layer.", "AMERICAS"),
    ("BOSTON", "Genesis unveils “Ruby” drug model.", "AMERICAS"),
    ("WASHINGTON", "US sanctions four Iranians over oil money.", "AMERICAS"),
    ("TEHRAN", "Araqchi: Iran wants diplomacy; Trump: terms no.", "MIDDLE EAST"),
    ("TALLINN", "Estonia to shut Russia border for six months.", "EUROPE"),
    ("LONDON", "UK admits offensive cyber ops on Russia, China.", "EUROPE"),
    ("TOKYO", "Japan core inflation hits year's high.", "ASIA"),
    ("WASHINGTON", "House AI caucus formed, 24+ members.", "AMERICAS"),
]

STRIP = [
    ("110+", "MISSILES FIRED"),
    ("−5.28%", "NASDAQ POINTS DROP"),
    ("$88.91", "ANTHROPIC CLOSE"),
    ("100,000", "YOUTH VISAS / YEAR"),
    ("9–6", "ICJ VOTE"),
    ("300,000+", "EVACUATED"),
]

# (number, lon, lat, label) — red pins for stories 1-13
PINS = [
    (1, 30.5, 50.45, "KYIV"), (1, 22.0, 50.5, "POLAND"),
    (2, -74.0, 40.7, "NEW YORK"), (3, -77.0, 38.9, "WASHINGTON"),
    (4, 4.35, 50.85, "BRUSSELS"), (5, 4.3, 52.1, "THE HAGUE"),
    (5, 96.1, 19.75, "NAYPYITAW"), (6, 30.7, 36.9, "ANTALYA"),
    (7, 84.9, 19.3, "ODISHA"), (8, -74.0, 40.7, "NEW YORK"),
    (9, 44.4, 33.3, "BAGHDAD"), (10, 56.3, 27.0, "QESHM"),
    (11, -77.0, 38.9, "WASHINGTON"), (12, 13.2, -8.8, "LUANDA"),
    (13, 2.35, 48.85, "PARIS"),
]
# Grey dots for brief locations (lon, lat)
DOTS = [(0.1, 51.5), (21.0, 52.25), (4.35, 50.85), (-77.0, 38.9), (-74.0, 40.7),
        (-122.4, 37.8), (30.7, 36.9), (96.1, 19.75), (4.3, 52.1), (10.0, 53.5),
        (-72.9, 41.3), (-71.1, 42.4), (51.4, 35.7), (24.7, 59.4), (139.7, 35.7)]

M = 28  # side margin
CW = W - 2 * M  # 968

# ---------------------------------------------------------------- header
def draw_header(y):
    text(M, y, "THE WORLD IN ONE DAY", font(SANS_B, 14), fill=RED)
    text(W - M, y, "FRIDAY · 20 NOVEMBER 2026", font(SANS_B, 14), fill=INK, anchor="ra")
    y += 22
    hline(M, W - M, y, fill=INK, width=3)
    y += 10
    centre(M, W - M, y, "THE WORLD IN ONE DAY", font(SERIF_B, 50), fill=INK)
    y += 60
    centre(M, W - M, y, "Russian missiles land in Poland. The Nasdaq erases its year. Britain and the EU strike a reset deal.",
           font(SERIF_I, 21), fill=RED)
    y += 28
    # region tabs, computed from the story data so the counts can never lie
    regions = ["ASIA", "EUROPE", "MIDDLE EAST", "AFRICA", "AMERICAS", "OCEANIA", "GLOBAL"]
    counts = {r: 0 for r in regions}
    for L in LEADS + SECONDARIES:
        counts[L["region"]] += 1
    for _, _, r in BRIEFS:
        counts[r] += 1
    total = sum(counts.values())
    covered = sum(1 for r in regions if counts[r] > 0)
    x = M
    for name in regions:
        if counts[name] == 0:
            continue
        s = f"{name} {counts[name]}"
        text(x, y, s, font(SANS_B, 13), fill=NAVY)
        x += int(tw(s, font(SANS_B, 13))) + 22
    s = f"{total} STORIES · {covered} REGIONS"
    text(W - M, y, s, font(SANS_B, 13), fill=RED, anchor="ra")
    y += 22
    hline(M, W - M, y, fill=INK, width=1)
    return y + 8

# ---------------------------------------------------------------- numbers strip
def draw_strip(y, h=54):
    rect(M, y, W - M, y + h, fill=(238, 232, 218))
    rect(M, y, W - M, y + h, outline=INK, width=1)
    cw = CW / len(STRIP)
    for i, (num, label) in enumerate(STRIP):
        x0 = M + i * cw
        if i:
            vline(int(x0), y + 8, y + h - 8, fill=GREY_L, width=1)
        centre(int(x0), int(x0 + cw), y + 6, num, font(SERIF_B, 24), fill=RED)
        centre(int(x0), int(x0 + cw), y + 33, label, font(SANS_B, 9), fill=INK)
    return y + h

# ---------------------------------------------------------------- map
def map_xy(lon, lat, x0, y0, x1, y1):
    x = x0 + (lon - MAP_LON0) / (MAP_LON1 - MAP_LON0) * (x1 - x0)
    yy = y0 + (MAP_LAT0 - lat) / (MAP_LAT0 - MAP_LAT1) * (y1 - y0)
    return x, yy

def draw_map(y, h=200):
    text(M, y, "WHERE IT HAPPENED", font(SANS_B, 13), fill=RED)
    text(W - M, y, "RED NUMBERS MARK STORIES 1–13 · GREY DOTS MARK THE BRIEFS · POSITIONS APPROXIMATE",
         font(SANS_B, 10), fill=GREY, anchor="ra")
    y += 18
    x0, y0, x1, y1 = M, y, W - M, y + h
    rect(x0, y0, x1, y1, fill=NAVY)
    # graticule
    for lon in range(-150, 181, 30):
        gx, _ = map_xy(lon, 0, x0, y0, x1, y1)
        d.line([(gx, y0), (gx, y1)], fill=(38, 62, 110), width=1)
    for lat in range(-40, 81, 20):
        _, gy = map_xy(0, lat, x0, y0, x1, y1)
        d.line([(x0, gy), (x1, gy)], fill=(38, 62, 110), width=1)
    # land
    for poly in CONTINENTS:
        pts = [map_xy(lon, lat, x0, y0, x1, y1) for lon, lat in poly]
        d.polygon(pts, fill=SAND, outline=SAND_D)
    # continent labels
    for label, lon, lat in [("NORTH AMERICA", -100, 48), ("SOUTH AMERICA", -60, -15),
                            ("AFRICA", 17, 5),
                            ("ASIA", 95, 50), ("AUSTRALIA", 134, -25),
                            ("ATLANTIC", -30, 20), ("PACIFIC", -150, -5),
                            ("INDIAN", 75, -30), ("GREENLAND", -42, 72)]:
        lx, ly = map_xy(lon, lat, x0, y0, x1, y1)
        f = font(SANS_B, 9)
        text(lx, ly, label, f, fill=(200, 205, 220) if "OCEAN" in label or label in ("ATLANTIC", "PACIFIC", "INDIAN") else (90, 80, 55), anchor="mm")
    # grey dots (briefs)
    for lon, lat in DOTS:
        dx, dy = map_xy(lon, lat, x0, y0, x1, y1)
        d.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=(200, 205, 220))
    # red pins — stagger colliding badges with leader lines.
    # Grouping is by true distance (<20px), not grid cells: Brussels, The
    # Hague and Paris are 2-6px apart in truth and straddle cell borders.
    import math as _math
    true_pts = [(num, lon, lat, label, map_xy(lon, lat, x0, y0, x1, y1)) for num, lon, lat, label in PINS]
    groups = []
    for item in true_pts:
        placed = False
        for g in groups:
            if any(_math.hypot(item[4][0] - m[4][0], item[4][1] - m[4][1]) < 20 for m in g):
                g.append(item)
                placed = True
                break
        if not placed:
            groups.append([item])
    offsets = [(0, 0), (28, -12), (-28, -12), (28, 12), (-28, 12)]
    # POLAND label + leader first (badges draw over the line, not under it).
    plx, ply = map_xy(22.0, 50.5, x0, y0, x1, y1)
    llx, lly = map_xy(-25, 57, x0, y0, x1, y1)
    d.line([(llx + 48, lly + 4), (plx, ply)], fill=(255, 255, 255), width=1)
    text(llx, lly, "POLAND", font(SANS_B, 9), fill=WHITE)
    for items in groups:
        for i, (num, lon, lat, label, (px, py)) in enumerate(items):
            ox, oy = offsets[i % len(offsets)]
            bx, by = px + ox, py + oy
            if ox or oy:
                d.line([(px, py), (bx, by)], fill=(255, 255, 255), width=1)
            d.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=RED, outline=WHITE, width=1)
            text(bx, by - 1, str(num), font(SANS_B, 9), fill=WHITE, anchor="mm")
    # pin labels (a few, placed to avoid collisions; POLAND is labelled
    # above, in the North Sea, with a leader line to its pin)
    for label, lon, lat, dx, dy in [
            ("KYIV", 30.5, 50.45, 14, -14),
            ("ODISHA", 84.9, 19.3, 12, 4), ("BAGHDAD", 44.4, 33.3, 12, 14),
            ("LUANDA", 13.2, -8.8, 10, 10)]:
        lx, ly = map_xy(lon, lat, x0, y0, x1, y1)
        text(lx + dx, ly + dy, label, font(SANS_B, 9), fill=WHITE)
    rect(x0, y0, x1, y1, outline=INK, width=1)
    return y1

# ---------------------------------------------------------------- scenes
# Flat vector illustrations, drawn in code. Each scene is deliberately simple:
# a few bold shapes that read at thumbnail size. (x0,y0,x1,y1) is the scene box.
def scene(name, x0, y0, x1, y1):
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if name == "missiles":
        rect(x0, y0, x1, y1, fill=NAVY_D)
        # night sky + stars
        for sx, sy in [(0.12, 0.2), (0.3, 0.12), (0.5, 0.25), (0.68, 0.1), (0.85, 0.22), (0.2, 0.45), (0.9, 0.4)]:
            d.ellipse([x0 + sx * w - 1, y0 + sy * h - 1, x0 + sx * w + 1, y0 + sy * h + 1], fill=WHITE)
        # missile trails (arcs) with warheads
        for fx, fy, tx in [(0.08, 0.75, 0.45), (0.2, 0.85, 0.62), (0.55, 0.9, 0.88)]:
            d.line([(x0 + fx * w, y0 + fy * h), (x0 + tx * w, y0 + 0.18 * h)], fill=GOLD, width=3)
            d.ellipse([x0 + tx * w - 3, y0 + 0.18 * h - 3, x0 + tx * w + 3, y0 + 0.18 * h + 3], fill=RED)
        # bridge, broken span, over a river
        d.line([(x0 + 0.05 * w, y0 + 0.82 * h), (x0 + 0.95 * w, y0 + 0.82 * h)], fill=WHITE, width=4)
        d.line([(x0 + 0.45 * w, y0 + 0.82 * h), (x0 + 0.45 * w, y0 + 0.55 * h)], fill=WHITE, width=3)
        d.line([(x0 + 0.62 * w, y0 + 0.82 * h), (x0 + 0.62 * w, y0 + 0.55 * h)], fill=WHITE, width=3)
        d.polygon([(x0 + 0.45 * w, y0 + 0.82 * h), (x0 + 0.53 * w, y0 + 0.68 * h),
                   (x0 + 0.62 * w, y0 + 0.82 * h)], outline=RED, width=3)
        rect(x0, y0 + 0.88 * h, x1, y1, fill=(70, 110, 170))
    elif name == "markets":
        rect(x0, y0, x1, y1, fill=(245, 240, 230))
        # bars
        bw = w / 9
        vals = [0.5, 0.55, 0.48, 0.6, 0.45, 0.5, 0.38, 0.3, 0.18]
        for i, v in enumerate(vals):
            bx = x0 + i * bw + 2
            bh = v * h
            rect(bx, y1 - bh - 6, bx + bw - 5, y1 - 6, fill=(120, 122, 128) if i < 6 else RED)
        # plunging line
        pts = [(x0 + i * bw + bw / 2, y0 + h * (0.25 + i * 0.07)) for i in range(9)]
        d.line(pts, fill=RED, width=4)
        d.ellipse([pts[-1][0] - 4, pts[-1][1] - 4, pts[-1][0] + 4, pts[-1][1] + 4], fill=RED)
        text(x1 - 6, y0 + 4, "−5.28%", font(SANS_B, 16), fill=RED, anchor="ra")
    elif name == "podium":
        rect(x0, y0, x1, y1, fill=(232, 226, 212))
        # White House: pediment + columns + two small flags, podium in front
        d.polygon([(cx - 0.22 * w, y0 + 0.52 * h), (cx, y0 + 0.34 * h), (cx + 0.22 * w, y0 + 0.52 * h)], fill=WHITE, outline=INK)
        rect(x0 + 0.12 * w, y0 + 0.52 * h, x1 - 0.12 * w, y0 + 0.82 * h, fill=WHITE, outline=INK, width=1)
        for i in range(5):
            rect(x0 + (0.17 + i * 0.12) * w, y0 + 0.58 * h, x0 + (0.23 + i * 0.12) * w, y0 + 0.8 * h, fill=NAVY)
        # small flags on poles
        d.line([(x0 + 0.07 * w, y0 + 0.18 * h), (x0 + 0.07 * w, y0 + 0.52 * h)], fill=INK, width=2)
        rect(x0 + 0.07 * w, y0 + 0.18 * h, x0 + 0.16 * w, y0 + 0.3 * h, fill=RED)
        d.line([(x1 - 0.07 * w, y0 + 0.18 * h), (x1 - 0.07 * w, y0 + 0.52 * h)], fill=INK, width=2)
        rect(x1 - 0.16 * w, y0 + 0.18 * h, x1 - 0.07 * w, y0 + 0.3 * h, fill=RED)
        # podium
        d.polygon([(cx - 0.13 * w, y0 + 0.82 * h), (cx + 0.13 * w, y0 + 0.82 * h),
                   (cx + 0.09 * w, y1), (cx - 0.09 * w, y1)], fill=NAVY)
        d.ellipse([cx - 5, y0 + 0.68 * h, cx + 5, y0 + 0.68 * h + 10], fill=INK)
    elif name == "handshake":
        rect(x0, y0, x1, y1, fill=(238, 232, 218))
        # UK flag (simplified) + EU flag, linked by a chain
        rect(x0 + 0.08 * w, y0 + 0.25 * h, x0 + 0.38 * w, y0 + 0.75 * h, fill=(0, 36, 125))
        d.line([(x0 + 0.08 * w, y0 + 0.25 * h), (x0 + 0.38 * w, y0 + 0.75 * h)], fill=WHITE, width=4)
        d.line([(x0 + 0.38 * w, y0 + 0.25 * h), (x0 + 0.08 * w, y0 + 0.75 * h)], fill=WHITE, width=4)
        d.line([(x0 + 0.23 * w, y0 + 0.25 * h), (x0 + 0.23 * w, y0 + 0.75 * h)], fill=RED, width=3)
        d.line([(x0 + 0.08 * w, y0 + 0.5 * h), (x0 + 0.38 * w, y0 + 0.5 * h)], fill=RED, width=3)
        rect(x0 + 0.62 * w, y0 + 0.25 * h, x0 + 0.92 * w, y0 + 0.75 * h, fill=(0, 51, 153))
        for k in range(8):
            import math
            a = k * math.pi / 4
            sx = x0 + 0.77 * w + 0.09 * w * math.cos(a)
            sy = y0 + 0.5 * h + 0.09 * h * math.sin(a)
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=GOLD)
        d.line([(x0 + 0.38 * w, y0 + 0.5 * h), (x0 + 0.62 * w, y0 + 0.5 * h)], fill=GOLD, width=4)
    elif name == "gavel":
        rect(x0, y0, x1, y1, fill=(232, 226, 212))
        # courtroom: gavel + block + 9-6 score bug
        rect(x0 + 0.1 * w, y0 + 0.62 * h, x0 + 0.9 * w, y0 + 0.8 * h, fill=(120, 84, 50))
        d.line([(x0 + 0.25 * w, y0 + 0.3 * h), (x0 + 0.7 * w, y0 + 0.55 * h)], fill=(90, 60, 30), width=8)
        rect(x0 + 0.2 * w, y0 + 0.22 * h, x0 + 0.38 * w, y0 + 0.38 * h, fill=(90, 60, 30))
        rect(x0 + 0.62 * w, y0 + 0.47 * h, x0 + 0.8 * w, y0 + 0.62 * h, fill=(90, 60, 30))
        rect(x1 - 0.32 * w, y0 + 0.08 * h, x1 - 0.06 * w, y0 + 0.38 * h, fill=RED)
        text((x1 - 0.19 * w), y0 + 0.23 * h, "9–6", font(SERIF_B, 18), fill=WHITE, anchor="mm")
    elif name == "draft":
        rect(x0, y0, x1, y1, fill=(245, 240, 230))
        rect(x0 + 0.15 * w, y0 + 0.1 * h, x0 + 0.85 * w, y0 + 0.9 * h, fill=WHITE, outline=INK, width=1)
        for i in range(4):
            d.line([(x0 + 0.22 * w, y0 + (0.24 + i * 0.14) * h), (x0 + 0.78 * w, y0 + (0.24 + i * 0.14) * h)], fill=GREY, width=2)
        d.line([(x0 + 0.22 * w, y0 + 0.38 * h), (x0 + 0.78 * w, y0 + 0.38 * h)], fill=RED, width=4)
        text(cx, y0 + 0.62 * h, "CUT", font(SANS_B, 20), fill=RED, anchor="mm")
        rect(x0 + 0.6 * w, y0 + 0.68 * h, x0 + 0.86 * w, y0 + 0.86 * h, outline=RED, width=2)
    elif name == "cyclone":
        rect(x0, y0, x1, y1, fill=SKY)
        import math
        for r in range(6, 46, 7):
            a0 = r * 0.35
            pts = []
            for k in range(25):
                a = a0 + k * 0.28
                rr = r * (1 - k * 0.012)
                pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a) * 0.8))
            d.line(pts, fill=WHITE, width=3)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=NAVY_D)
        rect(x0, y0 + 0.82 * h, x1, y1, fill=SAND)
    elif name == "un":
        rect(x0, y0, x1, y1, fill=(232, 226, 212))
        d.ellipse([cx - 0.22 * w, y0 + 0.12 * h, cx + 0.22 * w, y0 + 0.62 * h], fill=SKY, outline=NAVY, width=2)
        d.ellipse([cx - 0.22 * w, y0 + 0.12 * h, cx + 0.22 * w, y0 + 0.62 * h], outline=WHITE, width=1)
        for i in range(5):
            d.line([(cx - 0.16 * w, y0 + (0.2 + i * 0.07) * h), (cx + 0.16 * w, y0 + (0.2 + i * 0.07) * h)], fill=NAVY, width=1)
        for fx in [0.12, 0.3, 0.48, 0.66, 0.84]:
            rect(x0 + fx * w, y0 + 0.72 * h, x0 + (fx + 0.1) * w, y0 + 0.92 * h, fill=NAVY if fx < 0.5 else RED)
    elif name == "raid":
        rect(x0, y0, x1, y1, fill=NAVY_D)
        d.polygon([(x0 + 0.1 * w, y0 + 0.85 * h), (x0 + 0.1 * w, y0 + 0.45 * h),
                   (x0 + 0.9 * w, y0 + 0.45 * h), (x0 + 0.9 * w, y0 + 0.85 * h)], fill=(60, 60, 70))
        for i in range(4):
            rect(x0 + (0.18 + i * 0.18) * w, y0 + 0.55 * h, x0 + (0.28 + i * 0.18) * w, y0 + 0.7 * h, fill=GOLD)
        d.polygon([(cx - 0.3 * w, y0 + 0.85 * h), (cx, y0 + 0.1 * h), (cx + 0.3 * w, y0 + 0.85 * h)],
                  fill=(255, 240, 160))
        d.ellipse([cx - 5, y0 + 0.1 * h, cx + 5, y0 + 0.1 * h + 10], fill=WHITE)
    elif name == "blast":
        rect(x0, y0, x1, y1, fill=(245, 240, 230))
        # island + disposal burst
        rect(x0, y0 + 0.7 * h, x1, y1, fill=SKY_D)
        d.polygon([(x0 + 0.15 * w, y0 + 0.7 * h), (x0 + 0.4 * w, y0 + 0.55 * h),
                   (x0 + 0.7 * w, y0 + 0.62 * h), (x0 + 0.85 * w, y0 + 0.7 * h)], fill=SAND)
        import math
        for k in range(8):
            a = k * math.pi / 4
            px2 = cx + 0.28 * w * math.cos(a)
            py2 = cy - 0.1 * h + 0.28 * h * math.sin(a)
            d.line([(cx, cy - 0.1 * h), (px2, py2)], fill=ORANGE, width=4)
        d.ellipse([cx - 0.12 * w, cy - 0.28 * h, cx + 0.12 * w, cy - 0.04 * h], fill=GOLD)
        d.ellipse([cx - 0.06 * w, cy - 0.2 * h, cx + 0.06 * w, cy - 0.1 * h], fill=RED)
    elif name == "split":
        rect(x0, y0, x1, y1, fill=(232, 226, 212))
        d.line([(cx, y0 + 0.85 * h), (x0 + 0.15 * w, y0 + 0.2 * h)], fill=NAVY, width=4)
        d.line([(cx, y0 + 0.85 * h), (x1 - 0.15 * w, y0 + 0.2 * h)], fill=RED, width=4)
        d.ellipse([x0 + 0.15 * w - 6, y0 + 0.2 * h - 6, x0 + 0.15 * w + 6, y0 + 0.2 * h + 6], fill=NAVY)
        d.ellipse([x1 - 0.15 * w - 6, y0 + 0.2 * h - 6, x1 - 0.15 * w + 6, y0 + 0.2 * h + 6], fill=RED)
    elif name == "chip":
        rect(x0, y0, x1, y1, fill=(245, 240, 230))
        rect(cx - 0.2 * w, y0 + 0.25 * h, cx + 0.2 * w, y0 + 0.75 * h, fill=NAVY, outline=GOLD, width=2)
        rect(cx - 0.1 * w, y0 + 0.38 * h, cx + 0.1 * w, y0 + 0.62 * h, fill=GOLD)
        for i in range(3):
            d.line([(cx - 0.2 * w, y0 + (0.32 + i * 0.13) * h), (cx - 0.3 * w, y0 + (0.32 + i * 0.13) * h)], fill=INK, width=2)
            d.line([(cx + 0.2 * w, y0 + (0.32 + i * 0.13) * h), (cx + 0.3 * w, y0 + (0.32 + i * 0.13) * h)], fill=INK, width=2)
        d.line([(x1 - 0.35 * w, y0 + 0.2 * h), (x1 - 0.12 * w, y0 + 0.55 * h)], fill=RED, width=4)
        d.polygon([(x1 - 0.12 * w, y0 + 0.55 * h), (x1 - 0.2 * w, y0 + 0.45 * h), (x1 - 0.06 * w, y0 + 0.48 * h)], fill=RED)
    elif name == "diamond":
        rect(x0, y0, x1, y1, fill=(232, 226, 212))
        # faceted diamond
        top = y0 + 0.25 * h
        mid = y0 + 0.45 * h
        bot = y0 + 0.85 * h
        d.polygon([(cx - 0.3 * w, top), (cx + 0.3 * w, top), (cx + 0.18 * w, mid),
                   (cx, bot), (cx - 0.18 * w, mid)], fill=(200, 225, 240), outline=NAVY)
        d.line([(cx - 0.3 * w, top), (cx - 0.18 * w, mid)], fill=NAVY, width=1)
        d.line([(cx + 0.3 * w, top), (cx + 0.18 * w, mid)], fill=NAVY, width=1)
        d.line([(cx, top), (cx, bot)], fill=NAVY, width=1)
        d.line([(cx - 0.15 * w, top), (cx, bot)], fill=NAVY, width=1)
        d.line([(cx + 0.15 * w, top), (cx, bot)], fill=NAVY, width=1)
        d.line([(cx - 0.3 * w, top), (cx + 0.3 * w, top)], fill=NAVY, width=2)
        # sparkle (drawn, not a glyph — Liberation lacks ✦)
        sx, sy = cx + 0.34 * w, y0 + 0.18 * h
        d.line([(sx - 5, sy), (sx + 5, sy)], fill=GOLD, width=2)
        d.line([(sx, sy - 5), (sx, sy + 5)], fill=GOLD, width=2)
    elif name == "unsc":
        rect(x0, y0, x1, y1, fill=(232, 226, 212))
        # council table arc + flags
        d.arc([x0 + 0.1 * w, y0 + 0.1 * h, x1 - 0.1 * w, y0 + 0.95 * h], 180, 360, fill=NAVY, width=6)
        for fx in [0.18, 0.38, 0.58, 0.78]:
            rect(x0 + fx * w, y0 + 0.15 * h, x0 + (fx + 0.08) * w, y0 + 0.35 * h, fill=NAVY if fx < 0.5 else RED)
        rect(cx - 0.25 * w, y0 + 0.6 * h, cx + 0.25 * w, y0 + 0.8 * h, fill=WHITE, outline=INK, width=1)
        text(cx, y0 + 0.7 * h, "UNSC", font(SANS_B, 12), fill=NAVY, anchor="mm")

# ---------------------------------------------------------------- leads
def draw_leads(y, h=236):
    colw = (CW - 2 * 12) // 3
    for i, L in enumerate(LEADS):
        x0 = M + i * (colw + 12)
        x1 = x0 + colw
        scene(L["scene"], x0, y, x1, y + 96)
        rect(x0, y, x1, y + 96, outline=INK, width=1)
        yy = y + 104
        text(x0, yy, f"{L['num']:02d} · ", font(SANS_B, 12), fill=RED)
        text(x0 + int(tw(f"{L['num']:02d} · ", font(SANS_B, 12))), yy, L["kicker"], font(SANS_B, 12), fill=NAVY)
        yy += 16
        yy = para(x0, yy, L["headline"], font(SERIF_B, 24), colw, leading=26)
        yy += 2
        yy = para(x0, yy, L["deck"], font(SERIF, 13), colw, leading=15)
        yy += 3
        text(x0, yy, "— " + L["source"], font(SANS_I, 11), fill=GREY)
        text(x1, yy, L["tag"], font(SANS_B, 10), fill=GREEN if L["tag"] == "CONFIRMED" else ORANGE, anchor="ra")
    return y + h

# ---------------------------------------------------------------- secondaries
def draw_secondaries(y, h=236):
    colw = (CW - 4 * 10) // 5
    rowh = h // 2
    for i, S in enumerate(SECONDARIES):
        r, c = divmod(i, 5)
        x0 = M + c * (colw + 10)
        x1 = x0 + colw
        yy = y + r * rowh
        scene(S["scene"], x0, yy, x1, yy + 38)
        rect(x0, yy, x1, yy + 38, outline=INK, width=1)
        yy += 44
        text(x0, yy, f"{S['num']:02d} · ", font(SANS_B, 10), fill=RED)
        text(x0 + int(tw(f"{S['num']:02d} · ", font(SANS_B, 10))), yy, S["kicker"], font(SANS_B, 10), fill=NAVY)
        yy += 13
        yy = para(x0, yy, S["headline"], font(SERIF_B, 13), colw, leading=14)
        yy = para(x0, yy, S["deck"], font(SANS, 11), colw, leading=12)
        text(x0, yy + 1, "— " + S["source"], font(SANS_I, 9), fill=GREY)
    return y + h

# ---------------------------------------------------------------- tail + footer
def draw_tail(y, h=88):
    text(M, y, "ALSO ON FRIDAY 20 NOVEMBER", font(SANS_B, 13), fill=RED)
    text(W - M, y, f"{len(BRIEFS)} MORE STORIES", font(SANS_B, 13), fill=INK, anchor="ra")
    y += 18
    cols = 3
    per = (len(BRIEFS) + cols - 1) // cols
    colw = (CW - 2 * 14) // 3
    for ci in range(cols):
        x0 = M + ci * (colw + 14)
        for j, (place, txt, _reg) in enumerate(BRIEFS[ci * per:(ci + 1) * per]):
            yy = y + j * 11
            s = f"{place} — {txt}"
            # truncate to one line
            f = font(SANS, 10)
            while tw(s, f) > colw and len(s) > 20:
                s = s[:-4] + "…"
            text(x0, yy, s, f, fill=INK)
    return y + per * 11 + 6

def draw_footer(y):
    hline(M, W - M, y, fill=RED, width=2)
    y += 6
    text(M, y, "DATE CHECK", font(SANS_B, 11), fill=RED)
    para(M + 92, y, "Every story here happened, or was first reported, on Friday 20 November 2026. "
         "LEFT OUT AS OTHER DAYS' NEWS: Shenzhen summit + ICJ verdict (19 NOV) · "
         "Houthi PIF Tower strike (19 NOV) · Kenya Ebola discharge (11 NOV).",
         font(SANS, 10), CW - 92, leading=12)
    y += 22
    text(M, y, "SOURCES: REUTERS · AP · CNN · BBC · UN NEWS · IMD · AMNESTY INTERNATIONAL · TASNIM",
         font(SANS_B, 9), fill=GREY)
    text(W - M, y, "PICTURES AND MAP: ORIGINAL, DRAWN IN CODE · 20 NOVEMBER 2026",
         font(SANS_B, 9), fill=GREY, anchor="ra")
    return y + 14

# ---------------------------------------------------------------- compose
if __name__ == "__main__":
    y = 14
    y = draw_header(y)
    y = draw_strip(y)
    y += 8
    y = draw_leads(y)
    y += 5
    y = draw_map(y, h=144)
    y += 5
    y = draw_secondaries(y)
    y += 5
    y = draw_tail(y)
    y += 2
    y = draw_footer(y)
    print("bottom y:", y, "of", H)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("saved", out, os.path.getsize(out), "bytes")
