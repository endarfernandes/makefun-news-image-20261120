#!/usr/bin/env python3
"""Render the V4 FINAL R3 PressPoint-reference magazine cover for
news-image-20261120 — edition: Friday, November 20, 2026.

Rebuilds v4-presspoint to match the LAYOUT of the reference image the
user uploaded (file_00000000ae1882078341f34fe57eba01.png) — layout and
style only, NOT its content (no 21 Nov date, no generic headlines,
no summit photo, no AFP/BBC source list).

Layout (1024x1024), adapted from the reference:
  header 0-76   : one row — big navy date | WORLD BRIEFING | red
                  BREAKING NEWS strip (label + arrow + headline);
                  thin navy divider below
  hero   76-470 : full-bleed Kyiv night photo, red category chip,
                  huge white headline + deck over a controlled dark
                  gradient, thin red accent line under the deck
  grid   482-968: 4x2 cards (235x237) — photo on top (cover crop),
                  coloured category chip overlaid bottom-left ON the
                  photo, bold headline + grey deck below on white
  footer 968-1024: dark navy bar — globe icon, date, sources,
                  photo-credit line, red diagonal accent at right

Exactly 9 stories (1 hero + 8 supporting) with the same headlines,
facts, figures, decks and sources as v4-presspoint, and the same
licensed photos (see PHOTOS.md). DROPPED vs v4-presspoint: the France
UNSC meeting story — it is a direct reaction to the hero story (the
Kyiv strikes), so the most duplicative of the 9; the user directed
8 supporting stories "sesuai gambar referensi". The reference look
REQUIRES cover-cropping the photos to fixed frames; the earlier
no-crop rule (R2) is set aside per the user's reference instruction
— R2 stays preserved as an alternative, and the 3x3 version of this
build is kept as entry-3x3.png. No timestamps, no randomness, no
network; two runs are byte-identical.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
MARGIN = 24
CW = W - 2 * MARGIN  # 976

# ---- palette ---------------------------------------------------------
NAVY = (14, 27, 46)        # deep navy: primary text / footer bar
INK = (11, 21, 38)         # near-black headlines
RED = (217, 43, 43)        # breaking red / hero chip
RED_DARK = (168, 30, 30)   # second footer slash
BLUE = (29, 95, 214)       # MARKETS
PURPLE = (104, 74, 186)    # WASHINGTON
TEAL = (14, 124, 123)      # WEATHER
GREEN = (34, 139, 74)      # CLIMATE
STEEL = (47, 111, 179)     # UNITED NATIONS
ORANGE = (214, 110, 28)    # AFRICA
IVORY = (250, 247, 241)    # page background
WHITE = (255, 255, 255)
HAIR = (231, 226, 214)     # card hairlines
GREY = (95, 107, 122)      # metadata grey
DECK = (58, 69, 86)        # card deck grey-navy
FOOT_TXT = (225, 232, 240) # footer main text
FOOT_DIM = (150, 168, 190) # footer credit line

# ---- fonts (Inter variable, OFL, bundled) -----------------------------
_cache = {}


def inter(size, weight=400):
    key = (size, weight)
    if key not in _cache:
        f = ImageFont.truetype(os.path.join(HERE, "fonts", "InterVariable.ttf"), size)
        f.set_variation_by_axes([min(32, max(14, size)), weight])
        _cache[key] = f
    return _cache[key]


def wrap(d, text, font, max_w):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def cover(img, tw, th, fy=0.5):
    """Scale image to cover (tw, th), cropping vertically at focus fy
    (0 = top of the excess, 1 = bottom), horizontally centred.
    This is the reference look: photos fill their frames."""
    w, h = img.size
    s = max(tw / w, th / h)
    nw, nh = round(w * s), round(h * s)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - tw) // 2
    y = int(round(fy * (nh - th)))
    y = max(0, min(nh - th, y))
    return img.crop((x, y, x + tw, y + th)).convert("RGB")


def chip(d, x, y, text, font, bg, fg=WHITE, pad_x=9, h=20):
    w = int(d.textlength(text, font=font)) + 2 * pad_x
    d.rectangle([x, y, x + w, y + h], fill=bg)
    d.text((x + pad_x, y + h // 2), text, font=font, fill=fg, anchor="lm")
    return w


# ---- content: exactly 10 stories, Friday 20 November 2026 -----------
# (same headlines / facts / decks / sources as v4-presspoint)
HERO = {
    "photo": "hero_kyiv.jpg", "fy": 0.42,
    "chip": "WAR — UKRAINE · POLAND",
    "headline": "MISSILES FALL ON NATO SOIL",
    "deck": ("Russia's largest strike of the year: 110+ missiles, 400+ drones, "
             "at least 8 killed, 3 Kyiv bridges hit. A Kh-101 missile lands in "
             "Poland — NATO jets scrambled."),
}

# (photo, fy, kicker, chip colour, headline, deck)
CARDS = [
    ("nyse_alt.jpg", 0.40, "MARKETS", BLUE,
     "NASDAQ ERASES ITS YEAR",
     "Nasdaq -5.28%, -1,261 points — the second-biggest one-day drop ever. "
     "Anthropic -8.5% to $88.91."),
    ("trump.jpg", 0.45, "WASHINGTON", PURPLE,
     "TRUMP: “VERY GOOD” TALKS",
     "A day after Shenzhen, the White House hails the talks. AI guardrails "
     "keep humans in military-AI decisions."),
    ("akvan.jpg", 0.50, "WEATHER", TEAL,
     "CYCLONE AKVAN MAKES LANDFALL",
     "300,000+ evacuated; no deaths in first hours. The storm crossed near "
     "Gopalpur with winds to 90 km/h."),
    ("berlaymont.jpg", 0.45, "BRUSSELS", NAVY,
     "UK AND EU SEAL THE RESET",
     "Food checks scrapped, emissions systems linked; 100,000 youth visas "
     "a year."),
    ("peace_palace.jpg", 0.45, "JUSTICE", RED,
     "MYANMAR REJECTS 9–6 VERDICT",
     "Naypyitaw calls the 9–6 genocide verdict “unfair”; UK expels "
     "attaché."),
    ("antalya.jpg", 0.50, "CLIMATE", GREEN,
     "COP31 SLIPS INTO OVERTIME",
     "No deal by Friday's deadline; talks run into the weekend. Fossil-fuel "
     "phase-out cut from the draft."),
    ("unhq.jpg", 0.50, "UNITED NATIONS", STEEL,
     "RACE FOR UN CHIEF STALLS",
     "Two veto powers reject Grynspan; poll 10 in favour, 4 against."),
    ("diamond.jpg", 0.50, "AFRICA", ORANGE,
     "ANGOLA BUYS INTO DE BEERS",
     "Angola's Endiama pays $180m for a 10% stake in the diamond giant."),
]

BREAKING = "Russian missiles land in Poland — NATO jets scrambled"
DATE = "Friday, November 20, 2026"
SOURCES_LINE = "Sources: Reuters · AP · CNN · IMD · Asia Today"


def main():
    img = Image.new("RGB", (W, H), IVORY)
    d = ImageDraw.Draw(img)

    # ---- header: one row (reference) ---------------------------------
    f_date = inter(32, 900)
    date_w = d.textlength(DATE, font=f_date)
    d.text((MARGIN, 16), DATE, font=f_date, fill=NAVY)
    div_x = MARGIN + int(date_w) + 14
    d.line([(div_x, 22), (div_x, 48)], fill=NAVY, width=2)
    f_wb = inter(11, 700)
    wb_x = div_x + 14
    wb_w = d.textlength("WORLD BRIEFING", font=f_wb)
    d.text((wb_x, 26), "WORLD BRIEFING", font=f_wb, fill=NAVY)

    # red breaking strip on the right of the same row
    strip_x = wb_x + int(wb_w) + 16
    strip_w = (W - MARGIN) - strip_x
    d.rectangle([strip_x, 14, W - MARGIN, 50], fill=RED)
    f_lab = inter(11, 800)
    f_brk = inter(10.5, 500)
    lab_w = d.textlength("BREAKING NEWS", font=f_lab)
    arr_w = d.textlength(" › ", font=inter(12, 800))
    brk_w = d.textlength(BREAKING, font=f_brk)
    need = 10 + lab_w + 6 + arr_w + 6 + brk_w + 10
    assert need <= strip_w, f"breaking strip overflow: need {need}, have {strip_w}"
    tx = strip_x + 10
    d.text((tx, 32), "BREAKING NEWS", font=f_lab, fill=WHITE, anchor="lm")
    tx += lab_w + 6
    d.text((tx, 32), "›", font=inter(12, 800), fill=WHITE, anchor="lm")
    tx += arr_w + 6
    d.text((tx, 32), BREAKING, font=f_brk, fill=WHITE, anchor="lm")

    # thin navy divider below the header row
    d.line([(MARGIN, 68), (W - MARGIN, 68)], fill=NAVY, width=2)

    # ---- hero: full-bleed photo, overlay text ------------------------
    HERO_Y0, HERO_Y1 = 76, 470
    hero = Image.open(os.path.join(HERE, "assets", HERO["photo"]))
    hero = cover(hero, W, HERO_Y1 - HERO_Y0, HERO["fy"])
    img.paste(hero, (0, HERO_Y0))
    # dark gradient over the lower part of the photo
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    gy0, gy1 = HERO_Y0 + 124, HERO_Y1
    for y in range(gy0, gy1):
        a = int(225 * (y - gy0) / (gy1 - gy0))
        od.line([(0, y), (W, y)], fill=(5, 10, 20, a))
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img)
    chip(d, MARGIN, 310, HERO["chip"], inter(12, 800), RED, h=24)
    f_hero = inter(46, 800)
    assert d.textlength(HERO["headline"], font=f_hero) <= CW, "hero headline too wide"
    d.text((MARGIN, 342), HERO["headline"], font=f_hero, fill=WHITE)
    f_deck = inter(15, 500)
    lines = wrap(d, HERO["deck"], f_deck, CW)
    assert len(lines) <= 2, f"hero deck wraps to {len(lines)} lines"
    y = 398
    for ln in lines:
        d.text((MARGIN, y), ln, font=f_deck, fill=(235, 238, 242))
        y += 20
    # thin red accent line under the deck (reference)
    d.rectangle([MARGIN, 450, MARGIN + 64, 453], fill=RED)

    # ---- 4x2 card grid (reference card style, 8 supporting stories) --
    grid_y0, gap, cw_, ch_, ph_ = 482, 12, 235, 237, 135
    f_head = inter(16, 800)
    f_cdeck = inter(11, 400)
    f_chip = inter(10, 800)
    for i, (photo, fy, kick, color, head, deck) in enumerate(CARDS):
        r, c = divmod(i, 4)
        cx = MARGIN + c * (cw_ + gap)
        cy = grid_y0 + r * (ch_ + gap)
        d.rectangle([cx, cy, cx + cw_, cy + ch_], fill=WHITE, outline=HAIR)
        ph = Image.open(os.path.join(HERE, "assets", photo))
        ph = cover(ph, cw_, ph_, fy)
        img.paste(ph, (cx, cy))
        # coloured category chip overlaid bottom-left ON the photo
        chip(d, cx + 8, cy + ph_ - 8 - 20, kick, f_chip, color, h=20)
        hlines = wrap(d, head, f_head, cw_ - 24)
        assert len(hlines) <= 2, f"headline wraps to {len(hlines)} lines: {head}"
        y = cy + 143
        for ln in hlines:
            d.text((cx + 12, y), ln, font=f_head, fill=INK)
            y += 18
        lines = wrap(d, deck, f_cdeck, cw_ - 24)
        assert len(lines) <= 3, f"deck wraps to {len(lines)} lines: {deck}"
        y = cy + 183
        for ln in lines:
            d.text((cx + 12, y), ln, font=f_cdeck, fill=DECK)
            y += 13
        assert y <= cy + ch_ - 8, f"card {i+1} text overflows"

    # ---- footer: dark navy bar (reference) ---------------------------
    d.rectangle([0, 968, W, H], fill=NAVY)
    # globe icon: circle + vertical ellipse + horizontal line
    d.ellipse([26, 984, 52, 1010], outline=WHITE, width=2)
    d.ellipse([33, 984, 45, 1010], outline=WHITE, width=1)
    d.line([(26, 997), (52, 997)], fill=WHITE, width=1)
    f_fdate = inter(13, 800)
    fdate_w = d.textlength(DATE, font=f_fdate)
    d.text((62, 990), DATE, font=f_fdate, fill=WHITE, anchor="lm")
    fdiv_x = 62 + int(fdate_w) + 12
    d.line([(fdiv_x, 984), (fdiv_x, 1000)], fill=(120, 140, 165), width=1)
    f_src = inter(12, 500)
    d.text((fdiv_x + 12, 990), SOURCES_LINE, font=f_src, fill=FOOT_TXT, anchor="lm")
    d.text((MARGIN, 1012), "PHOTOS: WIKIMEDIA COMMONS (CC BY / CC BY-SA / CC0) · "
           "NOAA · SMITHSONIAN · WHITE HOUSE — FULL CREDITS IN REPO",
           font=inter(9, 400), fill=FOOT_DIM)
    # red diagonal accent at the right edge (reference)
    d.polygon([(950, 968), (968, 968), (950, 1024), (932, 1024)], fill=RED)
    d.polygon([(976, 968), (994, 968), (976, 1024), (958, 1024)], fill=RED_DARK)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
