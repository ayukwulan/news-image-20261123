#!/usr/bin/env python3
"""Draw 'THE WORLD TODAY' - Monday 23 November 2026.

A 1024x1024 newspaper front page: 35 verified world stories, a dotted
world map with 12 numbered pins, and a BY THE NUMBERS strip.
Pillow only, no network, fully deterministic.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (250, 248, 242)          # paper
INK = (24, 24, 24)            # near-black text
RULE = (24, 24, 24)
MUTED = (110, 108, 100)
MAP_DOT = (70, 70, 70)
PIN_RED = (192, 57, 43)

FONT_DIR = "/usr/share/fonts/truetype"
SERIF_B = os.path.join(FONT_DIR, "dejavu/DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "dejavu/DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "dejavu/DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- stories
# (number, region, beat, headline) -- every fact verified from Reuters /
# AP / AFP / Al Jazeera / ESA / Eurostat / Xinhua on 24 Nov 2026.
STORIES = [
    (1, "NORTH AMERICA", "MARKETS",
     "Nvidia reinstates Jensen Huang as CEO; shares jump about 31%"),
    (2, "NORTH AMERICA", "POLITICS",
     "Democrats clinch 258 House seats, largest majority since 1992"),
    (3, "NORTH AMERICA", "TECH",
     "CrowdStrike to buy Zscaler in $43.9bn all-stock deal"),
    (4, "NORTH AMERICA", "POLITICS",
     "US intel chief: Putin is \u2018not America\u2019s friend\u2019"),
    (5, "NORTH AMERICA", "HEALTH",
     "Pennsylvania measles deaths rise to 9; 1,638 cases recorded"),
    (6, "NORTH AMERICA", "LAW",
     "Massachusetts sues to block ICE courthouse arrests"),
    (7, "NORTH AMERICA", "ENERGY",
     "Alberta bill lets province fund gas pipelines itself"),
    (8, "NORTH AMERICA", "POLITICS",
     "Trump orders Army to pause Iowa lead-azide detonation"),
    (9, "NORTH AMERICA", "TRADE",
     "Mexico and China agree to set up trade working group"),
    (10, "SOUTH AMERICA", "ENERGY",
     "Argentina approves $50.8bn LNG project under RIGI"),
    (11, "SOUTH AMERICA", "SPORT",
     "Flamengo seal 10th Brazilian title with 1\u20131 draw"),
    (12, "SOUTH AMERICA", "ECONOMY",
     "Brazil central bank chief warns spending fuels inflation"),
    (13, "SOUTH AMERICA", "SPORT",
     "Boca Juniors win Copa Sudamericana, 2\u20130 in Barranquilla"),
    (14, "EUROPE", "CLIMATE",
     "COP31 ends with no deal after record-long talks"),
    (15, "EUROPE", "WAR",
     "Russian strikes kill at least 15 around Kyiv"),
    (16, "EUROPE", "POLITICS",
     "EU proposes 22nd sanctions package against Russia"),
    (17, "EUROPE", "POLITICS",
     "Spain court clears Puigdemont\u2019s return from exile"),
    (18, "EUROPE", "ECONOMY",
     "Euro area inflation hits 4.0%, highest since 2023"),
    (19, "EUROPE", "POLITICS",
     "UK and EU strike food-trade and youth-mobility deals"),
    (20, "EUROPE", "DEFENCE",
     "NATO meeting in Berlin warns Russia, pledges space defence"),
    (21, "AFRICA", "CONFLICT",
     "Ukraine drones sink Russian corvette off Benghazi"),
    (22, "AFRICA", "DISASTER",
     "Nigeria boat capsizes en route to funeral; at least 24 dead"),
    (23, "AFRICA", "CONFLICT",
     "Drones hit homes and a UN building in Khartoum"),
    (24, "ASIA", "DIPLOMACY",
     "Trump calls Putin \u2018my friend\u2019 after Shenzhen summit"),
    (25, "ASIA", "CONFLICT",
     "Iran vows \u2018all available means\u2019 against US blockade"),
    (26, "ASIA", "CONFLICT",
     "Iranian strike hits Bahrain civilian site; 2 hurt"),
    (27, "ASIA", "DISASTER",
     "Indonesia factory fire kills 24; about 30 missing"),
    (28, "ASIA", "AID",
     "India pledges $1.6bn aid to flood-hit Nepal"),
    (29, "ASIA", "POLITICS",
     "Bangladesh: Hasina to be jailed if she returns"),
    (30, "ASIA", "POLITICS",
     "Eisenkot calls settler arson \u2018Jewish terrorism\u2019"),
    (31, "ASIA", "TRADE",
     "EU and Indonesia sign trade deal covering 730m people"),
    (32, "ASIA", "SPACE",
     "BepiColombo reaches Mercury orbit after 8 years"),
    (33, "ASIA", "MARKETS",
     "Asian chip stocks slide; Kospi fell as much as 5.8%"),
    (34, "OCEANIA", "CLIMATE",
     "Albanese: COP31 failure shows \u2018difficult\u2019 times"),
    (35, "OCEANIA", "BUSINESS",
     "AustralianSuper backs $2.53bn Reliance takeover"),
]

REGION_COLOR = {
    "NORTH AMERICA": (31, 111, 191),
    "SOUTH AMERICA": (46, 139, 87),
    "EUROPE": (106, 79, 163),
    "AFRICA": (217, 123, 41),
    "ASIA": (192, 57, 43),
    "OCEANIA": (14, 138, 138),
}

LEAD_DECK = ("Wall Street rallies with it \u2014 Nasdaq +6.5%, S&P 500 +4.7% "
             "\u2014 after last week\u2019s AI sell-off. (Reuters)")

# (number, place, short label, lon, lat)
PINS = [
    (1, "Santa Clara", "Nvidia CEO returns", -122.0, 37.4),
    (2, "Washington", "Democrats 258 seats", -77.0, 38.9),
    (3, "Kyiv", "15 killed in strikes", 30.5, 50.5),
    (4, "Benghazi", "Russian corvette sunk", 20.1, 32.1),
    (5, "Antalya", "COP31 ends, no deal", 30.7, 36.9),
    (6, "Shenzhen", "Trump\u2013Xi\u2013Putin summit", 114.1, 22.5),
    (7, "Bahrain", "Iranian strike, 2 hurt", 50.6, 26.2),
    (8, "Cikande", "Factory fire, 24 dead", 106.3, -6.2),
    (9, "Kathmandu", "India pledges $1.6bn", 85.3, 27.7),
    (10, "Bayelsa", "Boat sinks, 24 dead", 6.3, 4.8),
    (11, "Khartoum", "Drones hit UN building", 32.5, 15.6),
    (12, "Sydney", "Albanese on COP31", 151.2, -33.9),
]

# (big number, label) -- all verified today.
NUMBERS = [
    ("31%", "Nvidia shares jump as Huang returns"),
    ("258", "House seats won by Democrats, most since 1992"),
    ("$43.9bn", "CrowdStrike\u2019s all-stock deal for Zscaler"),
    ("4.0%", "Euro area inflation in October, highest since 2023"),
]

# Landmass as coarse (lat_min, lat_max, lon_min, lon_max) rectangles.
LAND = [
    (-55, -35, -73, -62), (-35, -12, -73, -40), (-12, 0, -80, -35),
    (0, 12, -78, -50),                                    # South America
    (8, 18, -92, -77), (15, 32, -117, -87), (25, 45, -100, -67),
    (32, 49, -125, -100), (45, 62, -95, -55), (49, 70, -140, -95),
    (55, 71, -168, -140), (60, 83, -58, -20),             # N. America + Greenland
    (50, 59, -8, 2), (36, 44, -10, 3), (43, 55, -5, 15),
    (36, 45, 3, 30), (45, 60, 15, 40), (55, 71, 5, 30),   # Europe
    (4, 15, -18, 10), (15, 35, -10, 35), (-5, 5, 10, 30),
    (-12, 12, 30, 51), (-35, -12, 12, 35), (-25, -12, 43, 50),  # Africa
    (12, 42, 35, 63), (35, 55, 50, 90), (50, 75, 40, 180),
    (8, 35, 68, 89), (20, 53, 75, 135), (5, 28, 92, 110),
    (-11, 6, 95, 141), (31, 45, 130, 145), (34, 42, 126, 130),   # Asia
    (-25, -11, 130, 146), (-39, -25, 114, 153), (-47, -34, 166, 178),
]


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit `width`."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def is_land(lat, lon):
    for la0, la1, lo0, lo1 in LAND:
        if la0 <= lat <= la1 and lo0 <= lon <= lo1:
            return True
    return False


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    mx = 36
    right = W - 36
    content_w = right - mx

    # ---------------------------------------------------------- masthead
    f_title = font(SERIF_B, 52)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 20), title, font=f_title, fill=INK)
    d.line([(mx, 88), (right, 88)], fill=RULE, width=2)
    f_meta = font(SANS_B, 13)
    d.text((mx, 96), "MONDAY, 23 NOVEMBER 2026", font=f_meta, fill=INK)
    tagline_top = "35 STORIES \u00b7 6 CONTINENTS \u00b7 ONE DAY"
    tw2 = d.textlength(tagline_top, font=f_meta)
    d.text((right - tw2, 96), tagline_top, font=f_meta, fill=INK)
    d.line([(mx, 118), (right, 118)], fill=RULE, width=1)

    # ---------------------------------------------------------- lead story
    n, region, beat, headline = STORIES[0]
    col = REGION_COLOR[region]
    y = 128
    d.rectangle([mx, y, mx + 20, y + 20], fill=col)
    f_num = font(SANS_B, 13)
    t = str(n)
    d.text((mx + 10 - d.textlength(t, font=f_num) / 2, y + 3), t,
           font=f_num, fill=(255, 255, 255))
    f_tag = font(SANS_B, 11)
    d.text((mx + 28, y + 4), f"{region} \u00b7 {beat}", font=f_tag, fill=col)
    f_lead = font(SERIF_B, 21)
    d.text((mx, y + 26), headline, font=f_lead, fill=INK)
    f_deck = font(SANS, 12)
    d.text((mx, y + 54), LEAD_DECK, font=f_deck, fill=MUTED)
    d.line([(mx, 202), (right, 202)], fill=RULE, width=1)

    # ---------------------------------------------------------- story columns
    f_stag = font(SANS_B, 10)
    f_shead = font(SANS_B, 12)
    f_snum = font(SANS_B, 9)
    col_w = 300
    col_x = [mx, mx + 318, mx + 636]
    groups = [STORIES[1:13], STORIES[13:24], STORIES[24:35]]
    top = 212
    block_h = 43
    for ci, group in enumerate(groups):
        x = col_x[ci]
        yy = top
        for (num, reg, bt, head) in group:
            c = REGION_COLOR[reg]
            d.rectangle([x, yy, x + 15, yy + 15], fill=c)
            t = str(num)
            d.text((x + 7.5 - d.textlength(t, font=f_snum) / 2, yy + 2.5), t,
                   font=f_snum, fill=(255, 255, 255))
            d.text((x + 20, yy + 1), f"{reg} \u00b7 {bt}", font=f_stag, fill=c)
            lines = wrap(d, head, f_shead, col_w - 20)
            assert len(lines) <= 2, f"story {num} wraps to {len(lines)} lines"
            ly = yy + 15
            for ln in lines[:2]:
                d.text((x + 20, ly), ln, font=f_shead, fill=INK)
                ly += 14
            yy += block_h
    stories_bottom = top + 12 * block_h   # 728

    # ---------------------------------------------------------- map section
    f_sect = font(SANS_B, 14)
    map_title = "WHERE IT HAPPENED"
    my = stories_bottom + 8
    d.text((mx, my), map_title, font=f_sect, fill=INK)
    d.line([(mx + d.textlength(map_title, font=f_sect) + 10, my + 8),
            (right, my + 8)], fill=RULE, width=1)

    map_x = mx
    map_y = my + 24
    map_w = 470
    lat_top, lat_bot = 68.0, -50.0
    lat_span = lat_top - lat_bot
    map_h = int(map_w * lat_span / 360.0)

    def px(lon, lat):
        return (map_x + (lon + 180.0) / 360.0 * map_w,
                map_y + (lat_top - lat) / lat_span * map_h)

    step = 3.2
    lat = lat_top - step / 2
    while lat > lat_bot:
        lon = -180.0 + step / 2
        while lon < 180.0:
            if is_land(lat, lon):
                cx, cy = px(lon, lat)
                d.ellipse([cx - 1.6, cy - 1.6, cx + 1.6, cy + 1.6],
                          fill=MAP_DOT)
            lon += step
        lat -= step

    f_pin = font(SANS_B, 8)
    for (num, place, label, lon, lat) in PINS:
        cx, cy = px(lon, lat)
        r = 7
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PIN_RED,
                  outline=(255, 255, 255), width=1)
        t = str(num)
        d.text((cx - d.textlength(t, font=f_pin) / 2, cy - 4.5), t,
               font=f_pin, fill=(255, 255, 255))

    # legend (two columns of six, right of the map)
    f_leg = font(SANS, 11)
    f_leg_b = font(SANS_B, 11)
    lx0 = map_x + map_w + 22
    lx1 = lx0 + 208
    for i, (num, place, label, lon, lat) in enumerate(PINS):
        lx = lx0 if i < 6 else lx1
        ly = map_y + (i % 6) * 25
        d.ellipse([lx, ly, lx + 14, ly + 14], fill=PIN_RED)
        t = str(num)
        d.text((lx + 7 - d.textlength(t, font=f_pin) / 2, ly + 3), t,
               font=f_pin, fill=(255, 255, 255))
        d.text((lx + 19, ly - 1), place, font=f_leg_b, fill=INK)
        d.text((lx + 19, ly + 12), label, font=f_leg, fill=MUTED)
    map_bottom = map_y + map_h

    # ---------------------------------------------------------- by the numbers
    ny = map_bottom + 12
    d.line([(mx, ny), (right, ny)], fill=RULE, width=1)
    ny += 8
    f_big = font(SERIF_B, 30)
    f_lab = font(SANS, 11)
    box_w = content_w // 4
    for i, (big, lab) in enumerate(NUMBERS):
        bx = mx + i * box_w
        if i:
            d.line([(bx - 8, ny), (bx - 8, ny + 52)], fill=(200, 196, 188),
                   width=1)
        d.text((bx, ny), big, font=f_big, fill=PIN_RED)
        lab_lines = wrap(d, lab, f_lab, box_w - 16)
        ly = ny + 32
        for ln in lab_lines[:2]:
            d.text((bx, ly), ln, font=f_lab, fill=INK)
            ly += 12
    numbers_bottom = ny + 56

    # ---------------------------------------------------------- tagline + sources
    f_tag2 = font(SERIF_B, 12)
    tag2 = ("Everything on this page happened, or was first reported, "
            "on Monday 23 November 2026.")
    tw3 = d.textlength(tag2, font=f_tag2)
    d.text(((W - tw3) / 2, numbers_bottom + 6), tag2, font=f_tag2, fill=INK)
    f_src = font(SANS, 10)
    src = "Sources: Reuters, AP, AFP, BBC, Al Jazeera, ESA, Eurostat, Xinhua."
    tw4 = d.textlength(src, font=f_src)
    d.text(((W - tw4) / 2, numbers_bottom + 22), src, font=f_src, fill=MUTED)

    assert numbers_bottom + 34 <= H, "layout overflows bottom"
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("wrote", out, img.size, "map_bottom", map_bottom,
          "numbers_bottom", numbers_bottom)


if __name__ == "__main__":
    main()
