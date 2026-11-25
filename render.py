# render.py — draws entry.png for news-image-20261124 from scratch.
# One-day front page for Tuesday 24 November 2026: 35 stories, 6 regions.
# Run: python3 render.py  -> writes entry.png (1024x1024) next to this file.
# All facts below were checked against 2+ wire sources on 25 Nov 2026 (WIB);
# anything that could not be verified twice was dropped, never invented.

import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 24, 31)
NAVY = (15, 42, 74)
NAVY2 = (23, 58, 96)
GOLD = (201, 154, 44)
RED = (178, 38, 30)
TEAL = (14, 107, 107)
GREY = (108, 116, 128)
LINE = (190, 184, 172)
CARD = (255, 255, 255)
CREAM2 = (238, 232, 219)

REGION_COLORS = {
    "Europe": (43, 92, 168),
    "Middle East": (176, 92, 16),
    "Americas": (34, 120, 66),
    "Asia-Pacific": (112, 66, 150),
    "Africa": (198, 96, 26),
    "Global": (96, 104, 116),
}
TAG_COLORS = {
    "CONFIRMED": (34, 120, 66),
    "OFFICIAL": (43, 92, 168),
    "REPORTED": (120, 96, 20),
    "CLAIM": (178, 38, 30),
    "FORECAST": (96, 104, 116),
}

F_DIR = "fonts/"
def font(name, size):
    return ImageFont.truetype(F_DIR + name, size)

SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text(draw, xy, s, fnt, fill=INK, anchor="la"):
    draw.text(xy, s, font=fnt, fill=fill, anchor=anchor)

def para(draw, x, y, s, fnt, max_w, fill=INK, leading=None):
    lines = wrap(draw, s, fnt, max_w)
    lh = leading or int(fnt.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y

def tag_chip(draw, x, y, tag):
    f = SANS_B(8)
    w = int(draw.textlength(tag, font=f) + 10)
    draw.rounded_rectangle([x, y, x + w, y + 13], radius=3, fill=TAG_COLORS[tag])
    draw.text((x + 5, y + 2), tag, font=f, fill=(255, 255, 255))
    return w

# ---------------------------------------------------------------- data
# (n, region, headline, one-liner, tag, source)
LEADS = [
    (1, "Middle East", "FOURTH TANKER HITS A MINE IN HORMUZ",
     "Iran's Guard says a tanker hit a mine at dawn east of the strait and caught fire; two more turned back.",
     ["4 tankers hit mines — IRGC claim", "Brent $91.40, +2.3% Tue"], "CLAIM", "IRNA / Tasnim"),
    (2, "Middle East", "RIYADH TOWER HIT IN 'TERRORIST ATTACK'",
     "The Saudi-led coalition says a skyscraper in the finance district was targeted. No culprit named.",
     ["Tower in KAFD finance district", "Houthis 60 km from Aden"], "OFFICIAL", "Reuters"),
    (3, "Americas", "HUANG'S FIRST DAY BACK — AND THE RALLY FADES",
     "Cheered at HQ a day after his reinstatement, Huang watched Nvidia fall 5.9% as the Nasdaq slid.",
     ["NVDA -5.9% Tue, after +31% Mon", "Dow +0.9% to 50,018.70"], "CONFIRMED", "Reuters / Investopedia"),
]

MIDS = [
    (4, "Europe", "FLY WITH ME TO MOSCOW, LUKASHENKO TELLS ZELENSKYY",
     "Belarus leader proposes the two fly together for Kremlin talks — and says Russia is winning the war.", "REPORTED", "Reuters"),
    (5, "Middle East", "EISENKOT SIGNS FIRST COALITION DEAL",
     "Yashar (21 seats) agrees a pact with Lieberman's party (7) in the race to form a government by 6 Dec.", "CONFIRMED", "Reuters"),
    (6, "Asia-Pacific", "CHINA PROBES A POLITBURO MEMBER",
     "Shanghai chief Chen Jining is under investigation — the fourth top leader probed since 2025.", "OFFICIAL", "Xinhua / Reuters"),
    (7, "Americas", "NEW US TARIFFS DUE AFTER CAPACITY PROBE",
     "Findings on excess factory capacity in 16 trading partners expected Tue–Wed; new duties to follow.", "REPORTED", "Reuters"),
    (8, "Middle East", "SIX KILLED IN GAZA STRIKES",
     "Three die at a police post in Khan Younis, three more near the Netzarim corridor, medics say.", "REPORTED", "Reuters"),
    (9, "Europe", "KYIV DEFENDS LIBYA STRIKE AS SELF-DEFENCE",
     "FM Sybiha: hitting Russian ships in Libyan waters was lawful. Zelenskyy confirms a separate hit on the Sparta II.", "OFFICIAL", "Reuters"),
    (10, "Europe", "REAL HIT FIVE IN CHAMPIONS LEAGUE COMEBACK",
     "Real Madrid 5–1 PSV; Arsenal 1–1 Dortmund; Man City 2–2 Napoli on matchday 5.", "CONFIRMED", "UEFA / Reuters"),
    (11, "Asia-Pacific", "GARMENT WORKERS CLASH WITH POLICE",
     "Pay protests shut factories in Gazipur; workers want the minimum wage doubled to 30,000 taka.", "CONFIRMED", "Reuters"),
    (12, "Africa", "ABOUT 175 MIGRANTS MISSING OFF SENEGAL",
     "Contact lost with a Europe-bound boat that left Dakar about two weeks ago, officials say.", "REPORTED", "Reuters"),
    (13, "Europe", "UK OPENS NUCLEAR-TESTS INQUIRY",
     "A panel will examine the impact of weapons testing on veterans and their families, PM Burnham says.", "OFFICIAL", "Reuters"),
]

BRIEFS = [
    (14, "Middle East", "Houthis 60 km from Aden; army: they “won't seize” it.", "REPORTED", "Reuters"),
    (15, "Middle East", "UK sanctions the Houthis and four officials.", "OFFICIAL", "Anadolu / UK"),
    (16, "Europe", "Putin: Ukraine still hits Russian oil plants; vows reply.", "OFFICIAL", "Reuters"),
    (17, "Europe", "Norway, Ukraine expand anti-drone defence cooperation.", "OFFICIAL", "Reuters"),
    (18, "Europe", "UK, MI5 warn Ukraine suppliers of Russian sabotage risk.", "OFFICIAL", "Reuters"),
    (19, "Europe", "Kragujevac school shooting: teen held; two hurt, none killed.", "CONFIRMED", "AP"),
    (20, "Americas", "“El Chapo Isidro” to be tried in Mexico, not extradited.", "REPORTED", "Reuters"),
    (21, "Americas", "Abrego Garcia to leave the US voluntarily for Europe.", "REPORTED", "CBS / Reuters"),
    (22, "Americas", "US court lets army detonate toxic explosives in Iowa.", "REPORTED", "Reuters"),
    (23, "Americas", "Schumer: Huang broke chip-export law; Alibaba to fight listing.", "REPORTED", "Reuters"),
    (24, "Asia-Pacific", "UK sanctions five Myanmar generals after ICJ ruling.", "CONFIRMED", "BBC / TBS"),
    (25, "Asia-Pacific", "Bangladesh rejects Hasina's plea for help returning.", "REPORTED", "Anadolu"),
    (26, "Africa", "RSF group defects to the army in Khartoum.", "REPORTED", "Anadolu"),
    (27, "Asia-Pacific", "Wong: US–China rivalry strains conflict safeguards.", "REPORTED", "Anadolu"),
    (28, "Global", "Gold −2.7% to $3,554; Bitcoin below $60,000.", "REPORTED", "Markets"),
    (29, "Europe", "EU leaders meet 26–27 Nov on budget, Ukraine funding.", "FORECAST", "Reuters / EU"),
    (30, "Middle East", "Qatar working to revive US–Iran talks as Hormuz stays shut.", "REPORTED", "Reuters"),
    (31, "Middle East", "Iran army chief: Hormuz shut, curbs “tightening day by day”.", "OFFICIAL", "IRNA"),
    (32, "Europe", "Moscow: Estonia's acts “on verge of triggering open war”.", "CLAIM", "Reuters"),
    (33, "Middle East", "US weighing military training for Syrian forces.", "REPORTED", "Reuters"),
    (34, "Americas", "Huang faces Congress: House 1 Dec, Senate 3 Dec.", "FORECAST", "Reuters"),
    (35, "Americas", "Next: US GDP, PCE Wed; markets shut Thu (Thanksgiving).", "FORECAST", "Markets"),
]

STATS = [
    ("4", "tankers hit mines\nin Hormuz (IRGC claim)"),
    ("$91.40", "Brent crude Tue\n+2.3% on Hormuz fears"),
    ("−5.9%", "Nvidia Tue, after\n+31% on Monday"),
    ("50,018.70", "Dow close Tue\n+0.9%, above 50,000"),
    ("6", "killed in Gaza\nstrikes Tue (medics)"),
    ("~175", "migrants missing\noff Senegal"),
]

UTC_STRIP = [
    ("DAWN", "4th tanker hits mine, Hormuz"),
    ("07:00 UTC", "School shooting, Kragujevac"),
    ("08:13 UTC", "6 killed in Gaza (Reuters)"),
    ("15:23 UTC", "Riyadh tower attack"),
    ("EVENING", "UCL: Real 5–1 PSV"),
    ("21:00 UTC", "US close: Nasdaq −1.5%"),
    ("22:33 UTC", "UK nuclear inquiry"),
]

DATE_CHECK = [
    ("COP31 collapse — Sun 22 Nov, Antalya; EU + 130 nations refused a no-fossil-fuel text.", "NOT TODAY"),
    ("Libya warship sunk — Sun 22 Nov dawn; claimed Mon 23 Nov.", "NOT TODAY"),
    ("Huang reinstated — Mon 23 Nov; shares +31% Mon.", "NOT TODAY"),
    ("Kerch Bridge strikes — 16–19 Nov (Reuters, 21 Nov).", "NOT TODAY"),
    ("ICJ Myanmar ruling — Thu 19 Nov, 9–6.", "NOT TODAY"),
    ("“El Chapo Isidro” captured — Fri 20 Nov; announced Sat 21 Nov.", "NOT TODAY"),
    ("Dymer strike, 11 killed — Sun 22–Mon 23 Nov.", "NOT TODAY"),
    ("Indonesia ship seizure disclosed — Fri 20 Nov.", "NOT TODAY"),
    ("US blacklist: Megaspeed + Alibaba unit — Mon 23 Nov.", "NOT TODAY"),
    ("Not yet: EU council 26–27 Nov; Huang in Congress 1 + 3 Dec.", "NOT YET"),
]

REGIONS = [("Europe", 10), ("Middle East", 9), ("Americas", 8),
           ("Asia-Pacific", 5), ("Africa", 2), ("Global", 1)]

# Map pins: (number, label, lon, lat)
PINS = [
    (1, "Hormuz", 57, 26), (2, "Riyadh", 47, 25), (3, "Aden", 45, 13),
    (4, "Gaza", 34, 31), (5, "Benghazi", 20, 32), (6, "Minsk", 27, 54),
    (7, "Jerusalem", 35, 32), (8, "Shanghai", 121, 31), (9, "Dhaka", 90, 24),
    (10, "Dakar", -17, 15), (11, "Kragujevac", 21, 44),
    (12, "Santa Clara", -122, 37), (13, "London", 0, 51),
]

# Rough continent outlines (lon, lat) — schematic, drawn by hand.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-80, 73), (-70, 62),
     (-55, 47), (-60, 46), (-70, 42), (-75, 35), (-80, 26), (-84, 30), (-90, 21),
     (-97, 26), (-105, 20), (-110, 23), (-117, 33), (-125, 40), (-125, 49), (-135, 58),
     (-155, 58), (-168, 66)],
    # South America
    [(-79, 9), (-72, 12), (-62, 9), (-52, 5), (-44, -3), (-35, -8), (-40, -20),
     (-48, -28), (-58, -38), (-65, -45), (-70, -54), (-73, -37), (-70, -20),
     (-77, -12), (-81, -5), (-79, 9)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 49), (0, 51), (5, 53), (8, 57), (12, 55), (18, 56),
     (21, 55), (24, 59), (30, 60), (30, 70), (40, 68), (45, 68), (50, 69), (44, 62),
     (40, 55), (35, 47), (30, 46), (28, 44), (23, 40), (19, 42), (13, 45), (8, 44),
     (3, 43), (-2, 37), (-10, 36)],
    # Africa
    [(-6, 35), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12), (51, 11), (48, 2),
     (41, -2), (40, -10), (36, -18), (33, -26), (27, -33), (19, -35), (15, -27),
     (12, -18), (9, -1), (9, 4), (-8, 5), (-13, 8), (-17, 15), (-16, 25), (-10, 31),
     (-6, 35)],
    # Asia (simplified)
    [(30, 36), (36, 36), (43, 40), (48, 39), (50, 30), (54, 26), (57, 25), (61, 25),
     (66, 25), (70, 22), (72, 20), (76, 10), (80, 8), (80, 14), (85, 19), (89, 22),
     (92, 21), (94, 17), (98, 10), (100, 7), (104, 2), (104, 9), (109, 13), (110, 20),
     (114, 22), (118, 25), (122, 30), (121, 38), (126, 40), (130, 42), (135, 44),
     (140, 46), (142, 52), (142, 59), (158, 60), (162, 66), (178, 65), (170, 60),
     (160, 55), (150, 60), (140, 72), (130, 72), (120, 73), (110, 74), (100, 76),
     (90, 75), (80, 73), (70, 72), (60, 69), (55, 68), (50, 69), (44, 68), (40, 67),
     (35, 66), (32, 70), (30, 62), (28, 58), (30, 55), (35, 50), (40, 47), (45, 44),
     (40, 42), (35, 40), (30, 36)],
    # Australia
    [(114, -22), (114, -32), (118, -35), (124, -33), (130, -32), (136, -35),
     (140, -38), (147, -39), (150, -37), (153, -27), (146, -19), (142, -11),
     (136, -12), (132, -12), (126, -14), (122, -17), (118, -20), (114, -22)],
]

# ---------------------------------------------------------------- scenes
def scene_hormuz(d, x, y, w, h):
    # Night sea, tanker silhouette, mine blast, smoke — all inside the scene.
    d.rectangle([x, y, x + w, y + h], fill=(13, 52, 66))
    d.rectangle([x, y, x + w, y + 26], fill=(18, 36, 52))
    for sx in range(x + 8, x + w - 8, 26):
        d.ellipse([sx, y + 6, sx + 3, y + 9], fill=(220, 200, 130))
    d.rectangle([x, y + 26, x + w, y + h], fill=(10, 74, 92))
    for i in range(4):
        wy = y + 34 + i * 10
        d.line([x + 6, wy, x + w - 6, wy], fill=(28, 110, 128), width=2)
    # tanker: hull in the sea, deck cargo above the waterline
    hx, hy = x + 16, y + 36
    d.polygon([(hx, hy + 20), (hx + 150, hy + 20), (hx + 166, hy + 6),
               (hx + 148, hy), (hx, hy)], fill=(24, 28, 34))
    d.rectangle([hx + 16, hy - 12, hx + 54, hy], fill=(40, 46, 54))
    for cx in range(hx + 62, hx + 140, 14):
        d.rectangle([cx, hy - 8, cx + 9, hy - 1], fill=(201, 154, 44))
    # explosion burst on the far side, kept inside the scene
    bx, by = x + w - 62, y + 20
    for r, col in ((16, (240, 120, 30)), (11, (250, 180, 60)), (6, (255, 230, 150))):
        pts = []
        for k in range(12):
            ang = math.pi * k / 6
            rr = r * (1.25 if k % 2 == 0 else 0.8)
            pts.append((bx + rr * math.cos(ang), by + rr * math.sin(ang)))
        d.polygon(pts, fill=col)
    d.ellipse([bx - 30, by - 12, bx - 10, by + 2], fill=(70, 74, 80))
    d.ellipse([bx + 8, by - 14, bx + 28, by], fill=(90, 94, 100))
    # mines
    for mx, my in ((x + 30, y + 68), (x + w - 34, y + 72)):
        d.ellipse([mx - 5, my - 5, mx + 5, my + 5], fill=(20, 20, 24))
        for ang in range(0, 360, 45):
            a = math.radians(ang)
            d.line([mx, my, mx + 8 * math.cos(a), my + 8 * math.sin(a)], fill=(20, 20, 24), width=1)

def scene_riyadh(d, x, y, w, h):
    # Night skyline, tallest tower with a flash at its crown — inside the scene.
    d.rectangle([x, y, x + w, y + h], fill=(16, 22, 40))
    for sx in range(x + 10, x + w - 6, 22):
        d.ellipse([sx, y + 8, sx + 2, y + 10], fill=(230, 220, 170))
    base = y + h
    towers = [(0, 42, 34), (40, 30, 30), (76, 62, 40), (122, 34, 32),
              (160, 48, 36), (202, 32, 30), (238, 42, 34), (278, 26, 28)]
    for tx, th, tw in towers:
        d.rectangle([x + tx, base - th, x + tx + tw, base], fill=(38, 48, 66))
        for wy in range(base - th + 8, base - 6, 12):
            for wx in range(x + tx + 6, x + tx + tw - 6, 12):
                if (wx + wy) % 3 == 0:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(240, 200, 90))
    # tallest tower, crown flash
    tx, th, tw = 76, 62, 40
    d.rectangle([x + tx, base - th - 8, x + tx + tw, base - th], fill=(52, 64, 88))
    fx, fy = x + tx + tw // 2, base - th - 8
    for r, col in ((11, (240, 110, 30)), (7, (250, 180, 60)), (4, (255, 235, 160))):
        pts = []
        for k in range(10):
            ang = math.pi * k / 5
            rr = r * (1.3 if k % 2 == 0 else 0.75)
            pts.append((fx + rr * math.cos(ang), fy + rr * math.sin(ang)))
        d.polygon(pts, fill=col)
    d.ellipse([fx - 22, fy - 8, fx - 4, fy + 4], fill=(70, 74, 82))
    d.ellipse([fx + 4, fy - 10, fx + 22, fy + 2], fill=(88, 92, 100))

def scene_nvidia(d, x, y, w, h):
    # Green chip + candlestick chart: Monday spike, Tuesday dip — inside the scene.
    d.rectangle([x, y, x + w, y + h], fill=(12, 40, 26))
    cx, cy, s = x + 14, y + 8, 54
    d.rectangle([cx - 6, cy - 6, cx + s + 6, cy + s + 6], fill=(24, 90, 50))
    d.rectangle([cx, cy, cx + s, cy + s], fill=(16, 130, 66))
    d.rectangle([cx + 10, cy + 10, cx + s - 10, cy + s - 10], outline=(200, 240, 210), width=2)
    d.text((cx + s // 2, cy + s // 2 - 4), "NVDA", font=SANS_B(12),
           fill=(255, 255, 255), anchor="mm")
    for k in range(5):
        d.line([cx - 12, cy + 8 + k * 9, cx - 6, cy + 8 + k * 9], fill=(120, 200, 150), width=2)
        d.line([cx + s + 6, cy + 8 + k * 9, cx + s + 12, cy + 8 + k * 9], fill=(120, 200, 150), width=2)
    # chart
    gx, gy, gw, gh = x + 92, y + 8, w - 108, 50
    d.rectangle([gx, gy, gx + gw, gy + gh], fill=(255, 255, 255))
    pts = [(gx + 8, gy + 34), (gx + 52, gy + 36), (gx + 96, gy + 10),
           (gx + 140, gy + 40), (gx + gw - 8, gy + 30)]
    d.line(pts, fill=(178, 38, 30), width=3, joint="curve")
    d.ellipse([pts[2][0] - 4, pts[2][1] - 4, pts[2][0] + 4, pts[2][1] + 4], fill=(34, 120, 66))
    d.ellipse([pts[3][0] - 4, pts[3][1] - 4, pts[3][0] + 4, pts[3][1] + 4], fill=(178, 38, 30))
    d.text((x + 16, y + h - 14), "MON +31%  →  TUE −5.9% — the rally faded in a day",
           font=SANS_B(10), fill=(200, 220, 200))

SCENES = [scene_hormuz, scene_riyadh, scene_nvidia]

# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([0, 0, W, 96], fill=NAVY)
    d.rectangle([0, 94, W, 96], fill=GOLD)
    text(d, (18, 12), "THE WORLD IN ONE DAY", SANS_B(12), fill=GOLD)
    text(d, (W - 18, 12), "35 STORIES  •  6 REGIONS", SANS_B(11), fill=(180, 200, 225), anchor="ra")
    text(d, (18, 30), "TUESDAY 24 NOVEMBER 2026", SERIF_B(36), fill=(255, 255, 255))
    text(d, (18, 72), "Hormuz mines  •  Riyadh tower hit  •  Huang's first day back",
         SANS(12), fill=(205, 216, 232))
    text(d, (W - 18, 72), "Wires read up to 25 Nov 00:00 UTC", SANS(11),
         fill=(180, 200, 225), anchor="ra")

    # ---- UTC strip
    y = 104
    text(d, (18, y), "THE DAY IN UTC", SANS_B(10), fill=RED)
    x = 132
    seg_w = (W - 132 - 18) / len(UTC_STRIP)
    for i, (t, label) in enumerate(UTC_STRIP):
        cx = x + i * seg_w
        d.ellipse([cx, y + 1, cx + 7, y + 8], fill=NAVY)
        text(d, (cx + 11, y), t, SANS_B(9), fill=NAVY)
        text(d, (cx + 11, y + 11), label, SANS(8), fill=(60, 66, 76))
        if i < len(UTC_STRIP) - 1:
            d.line([cx + seg_w - 4, y + 4, cx + seg_w + 2, y + 4], fill=LINE, width=1)

    # ---- stat row
    y = 128
    bw = int((W - 36 - 5 * 6) / 6)
    for i, (num, lab) in enumerate(STATS):
        bx = 18 + i * (bw + 6)
        d.rectangle([bx, y, bx + bw, y + 40], fill=CARD, outline=LINE, width=1)
        d.rectangle([bx, y, bx + bw, y + 3], fill=NAVY)
        text(d, (bx + bw / 2, y + 6), num, SANS_B(15), fill=RED, anchor="ma")
        for j, ln in enumerate(lab.split("\n")):
            text(d, (bx + bw / 2, y + 23 + j * 9), ln, SANS(7.5), fill=(60, 66, 76), anchor="ma")

    # ---- leads
    y = 176
    lw = int((W - 36 - 2 * 10) / 3)
    lh = 216
    for i, (n, region, head, line, chips, tag, src) in enumerate(LEADS):
        lx = 18 + i * (lw + 10)
        d.rectangle([lx, y, lx + lw, y + lh], fill=CARD, outline=LINE, width=1)
        d.rectangle([lx, y, lx + lw, y + 4], fill=REGION_COLORS[region])
        # number badge + region
        d.ellipse([lx + 8, y + 12, lx + 30, y + 34], fill=RED)
        text(d, (lx + 19, y + 16), str(n), SANS_B(13), fill=(255, 255, 255), anchor="ma")
        text(d, (lx + 36, y + 16), region.upper(), SANS_B(9), fill=GREY)
        # scene
        SCENES[i](d, lx + 8, y + 40, lw - 16, 84)
        hy = y + 128
        hy = para(d, lx + 10, hy, head, SANS_B(13.5), lw - 20, leading=15)
        hy = para(d, lx + 10, hy + 2, line, SANS(10), lw - 20, leading=11)
        # two data chips, stacked; source sits right of the second chip
        f = SANS_B(9)
        for ci, chip in enumerate(chips):
            cyy = y + lh - 30 + ci * 15
            cw = d.textlength(chip, font=f) + 12
            d.rounded_rectangle([lx + 10, cyy, lx + 10 + cw, cyy + 13], radius=7,
                                fill=CREAM2, outline=GOLD, width=1)
            d.text((lx + 16, cyy + 2), chip, font=f, fill=INK)
        # tag + source, top right / bottom right
        tag_chip(d, lx + lw - 92, y + 12, tag)
        text(d, (lx + lw - 10, y + lh - 17), "Src: " + src, SANS(8), fill=GREY, anchor="ra")

    # ---- mid grid header
    y = 400
    text(d, (18, y), "MORE OF THE DAY — 10 STORIES", SANS_B(11), fill=NAVY)
    text(d, (W - 18, y), "each tagged: how sure are we?", SANS(9), fill=GREY, anchor="ra")
    y = 418
    mw = int((W - 36 - 10) / 2)
    mh = 40
    for i, (n, region, head, line, tag, src) in enumerate(MIDS):
        col, row = i % 2, i // 2
        mx = 18 + col * (mw + 10)
        my = y + row * (mh + 2)
        d.rectangle([mx, my, mx + mw, my + mh], fill=CARD, outline=LINE, width=1)
        d.rectangle([mx, my, mx + 4, my + mh], fill=REGION_COLORS[region])
        text(d, (mx + 10, my + 5), f"{n}.", SANS_B(12), fill=RED)
        text(d, (mx + 34, my + 4), head, SANS_B(11), fill=INK)
        blines = wrap(d, line, SANS(9.5), mw - 140)[:2]
        for bi, bl in enumerate(blines):
            text(d, (mx + 34, my + 19 + bi * 11), bl, SANS(9.5), fill=(52, 58, 68))
        tag_chip(d, mx + mw - 96, my + 4, tag)
        text(d, (mx + mw - 6, my + 27), src, SANS(8), fill=GREY, anchor="ra")

    # ---- briefs header
    y = 632
    text(d, (18, y), "BRIEFS 14–35 — THE REST OF TUESDAY", SANS_B(11), fill=NAVY)
    text(d, (W - 18, y), "one line each, source at the end", SANS(9), fill=GREY, anchor="ra")
    y = 648
    bw2 = int((W - 36 - 10) / 2)
    for i, (n, region, line, tag, src) in enumerate(BRIEFS):
        col, row = i % 2, i // 2
        bx = 18 + col * (bw2 + 10)
        by = y + row * 14.5
        d.ellipse([bx, by + 2, bx + 7, by + 9], fill=REGION_COLORS[region])
        text(d, (bx + 11, by), f"{n}.", SANS_B(9.5), fill=RED)
        text(d, (bx + 34, by), line, SANS(9.5), fill=INK)
        tw = d.textlength("[" + tag + " · " + src + "]", font=SANS(8))
        text(d, (bx + bw2 - tw, by), f"[{tag} · {src}]", SANS(8), fill=GREY)

    # ---- region bar
    y = 814
    text(d, (18, y), "WHERE THE STORIES CAME FROM", SANS_B(10), fill=NAVY)
    x = 18
    total = sum(v for _, v in REGIONS)
    for name, v in REGIONS:
        seg = (W - 36) * v / total
        d.rectangle([x, y + 13, x + seg - 2, y + 24], fill=REGION_COLORS[name])
        lab = f"{name} {v}"
        text(d, (x + seg / 2, y + 27), lab, SANS(8), fill=INK, anchor="ma")
        x += seg

    # ---- map
    y = 854
    text(d, (18, y), "WHERE IT HAPPENED", SANS_B(11), fill=NAVY)
    text(d, (W - 18, y), "pins 1–13 match the story numbers", SANS(9), fill=GREY, anchor="ra")
    mx0, my0, mw2, mh2 = 18, y + 17, W - 36, 68
    d.rectangle([mx0, my0, mx0 + mw2, my0 + mh2], fill=(222, 233, 240), outline=LINE, width=1)
    def proj(lon, lat):
        px = mx0 + (lon + 170) / 360 * mw2
        py = my0 + (75 - lat) / 130 * mh2
        return (px, py)
    for poly in CONTINENTS:
        d.polygon([proj(lo, la) for lo, la in poly], fill=(150, 168, 182))
    PIN_OFF = {1: (8, -4), 2: (8, -10), 3: (8, 12), 4: (-34, -12), 5: (-52, -4),
               6: (8, -4), 7: (8, 12), 8: (8, -4), 9: (8, -4), 10: (-34, -4),
               11: (-30, 10), 12: (-72, -4), 13: (8, -12)}
    for n, label, lon, lat in PINS:
        px, py = proj(lon, lat)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255), width=1)
        text(d, (px, py - 5), str(n), SANS_B(7), fill=(255, 255, 255), anchor="ma")
        ox, oy = PIN_OFF[n]
        text(d, (px + ox, py + oy), label, SANS_B(7.5), fill=INK)

    # ---- date check (two columns, all 10 items)
    y = 946
    d.rectangle([18, y, W - 18, y + 56], fill=(253, 240, 236), outline=(220, 160, 150), width=1)
    text(d, (26, y + 4), "DATE CHECK — left out on purpose:", SANS_B(10), fill=RED)
    for col_i in range(2):
        for j in range(5):
            item, kind = DATE_CHECK[col_i * 5 + j]
            ix = 26 + col_i * 490
            iy = y + 18 + j * 8
            text(d, (ix, iy), "• " + item, SANS(7.5), fill=(80, 40, 36))

    # ---- footer: one-day assertion + legend + sources
    text(d, (18, 1006), "Every story here happened, or was first reported, on Tuesday 24 November 2026.",
         SANS_B(9), fill=NAVY)
    text(d, (18, 1016), "CONFIRMED = 2+ major outlets · OFFICIAL = on the record · REPORTED = one outlet · CLAIM = one side's claim · FORECAST = scheduled — Sources: Reuters, AP, AFP, Xinhua, IRNA, Tasnim, Anadolu, UEFA, Investopedia, IBD, CBS, BBC.",
         SANS(8), fill=(60, 66, 76))

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)

if __name__ == "__main__":
    main()
