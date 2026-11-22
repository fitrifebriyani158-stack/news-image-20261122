#!/usr/bin/env python3
"""Poster v4: newspaper front page, 1024x1024, 36 stories, illustrations."""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 244, 238)
INK = (24, 26, 30)
RED = (168, 30, 28)
GRAY = (110, 112, 116)
NAVY = (18, 30, 52)

SER_B = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
SER = '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
SAN = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def fb(s): return ImageFont.truetype(SER_B, s)
def fr(s): return ImageFont.truetype(SER, s)
def fs(s): return ImageFont.truetype(SAN, s)
def fc(s): return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s)

im = Image.new('RGB', (W, H), PAPER)
d = ImageDraw.Draw(im)

def ctext(x, y, s, f, fill, anchor='mm'):
    d.text((x, y), s, font=f, fill=fill, anchor=anchor)

def ltext(x, y, s, f, fill):
    d.text((x, y), s, font=f, fill=fill, anchor='la')

def rtext(x, y, s, f, fill):
    d.text((x, y), s, font=f, fill=fill, anchor='ra')

def fit(s, font_path, size, max_w):
    while size > 6:
        f = ImageFont.truetype(font_path, size)
        if d.textlength(s, font=f) <= max_w: return f
        size -= 1
    return ImageFont.truetype(font_path, 6)

M = 22  # margin
CW = W - 2 * M

# ---- masthead top bar
d.rectangle([0, 0, W, 22], fill=INK)
ltext(M, 4, 'THE WORLD IN ONE DAY', fs(11), (240, 238, 232))
rtext(W - M, 4, 'SUNDAY 22 NOVEMBER 2026  ·  ONE PAGE', fs(11), (240, 238, 232))

# ---- giant title
t = 'Sunday 22 November 2026'
f_title = fb(58)
while d.textlength(t, font=f_title) > CW:
    f_title = ImageFont.truetype(SER_B, f_title.size - 2)
ctext(W // 2, 52, t, f_title, INK)

# ---- strapline
d.line([M, 86, W - M, 86], fill=RED, width=2)
strap = "186 drones over Ukraine in the night  ·  COP31's deal names no fossil fuels  ·  Iran's radar claim meets Bahrain's denial"
ctext(W // 2, 99, strap, fr(15), RED)

# ---- stat band
stats = [('186', 'drones fired at Ukraine overnight'),
         ('161', 'downed or suppressed by air defence'),
         ('35%', 'electricity lost for 2035, kept'),
         ('$120bn', 'adaptation target dropped'),
         ('720/9', "India's record Test total in NZ"),
         ('50', 'Wembanyama points, 19 rebounds')]
sy = 124
sw = CW // 6
for i, (n, cap) in enumerate(stats):
    x = M + i * sw
    ctext(x + sw // 2, sy, n, fb(26), RED)
    d.text((x + sw // 2, sy + 20), cap, font=fs(8.5), fill=GRAY, anchor='ma')

# ---- region band
d.line([M, 168, W - M, 168], fill=INK, width=1)
regions = [('EUROPE 8', (170, 40, 40)), ('MIDDLE EAST 4', (150, 80, 20)),
           ('AMERICAS 7', (30, 70, 140)), ('ASIA-PACIFIC 9', (90, 40, 120)),
           ('AFRICA 3', (30, 100, 50)), ('OCEANIA 3', (30, 90, 100)),
           ('WORLD 2', (60, 60, 60))]
by, bh = 170, 16
total = sum(int(r[0].split()[-1]) for r in regions)
x = M
for name, col in regions:
    seg = int((CW - 12) * int(name.split()[-1]) / total)
    d.rectangle([x, by, x + seg, by + bh], fill=col)
    ctext(x + seg // 2, by + bh // 2, name, fc(9), (255, 255, 255))
    x += seg + 2

# ---- timeline strip
ty = 196
ltext(M, ty, 'THE DAY IN UTC', fc(9), INK)
events = [('01:00', 'HK polls open'), ('03:30', 'COP31 objections close'),
          ('05:11', 'Hamas seeks talks'), ('05:30', 'Vertstappen wins Vegas'),
          ('06:00', 'COP31 approval due'), ('07:30', 'Approval slips again')]
x = M + 110
for tme, ev in events:
    ltext(x, ty, tme, fc(9), RED)
    ltext(x + 38, ty, ev, fs(9), GRAY)
    x += 150

d.line([M, 214, W - M, 214], fill=INK, width=2)

# ---- illustration helpers (all geometric)
def sky_scene(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(16, 24, 44))
    # buildings
    for bx, bh2, lit in [(20, 46, 1), (60, 60, 1), (100, 38, 0), (140, 52, 1), (180, 44, 1)]:
        d.rectangle([x0 + bx, y0 + h - bh2, x0 + bx + 28, y0 + h], fill=(40, 52, 80))
        for r in range(3):
            for c in range(3):
                if lit and (r + c) % 2 == 0:
                    d.rectangle([x0 + bx + 5 + c * 8, y0 + h - bh2 + 6 + r * 10,
                                 x0 + bx + 10 + c * 8, y0 + h - bh2 + 11 + r * 10], fill=(255, 210, 90))
    # drones
    for dx, dy in [(30, 20), (90, 12), (150, 26), (210, 15), (250, 22)]:
        cx, cy = x0 + dx, y0 + dy
        d.line([cx - 5, cy, cx + 5, cy], fill=(230, 230, 230), width=1)
        d.line([cx, cy - 5, cx, cy + 5], fill=(230, 230, 230), width=1)
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(255, 80, 60))
    # searchlight
    d.polygon([(x0 + 74, y0 + h - 60), (x0 + 200, y0), (x0 + 230, y0)], fill=(50, 62, 96))

def radar_scene(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(18, 40, 30))
    cx, cy, r = x0 + w // 2, y0 + h // 2 + 6, 34
    for rr in (12, 22, 32):
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], 180, 360, fill=(90, 190, 120), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(90, 190, 120), width=1)
    for a in ((cx - 18, cy - 20), (cx + 14, cy - 12)):
        d.ellipse([a[0] - 3, a[1] - 3, a[0] + 3, a[1] + 3], fill=(255, 60, 60))
    d.rectangle([x0 + w - 40, y0 + h - 18, x0 + w - 10, y0 + h - 8], fill=(30, 34, 40))

def globe_scene(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(24, 60, 110))
    cx, cy = x0 + w // 2, y0 + h // 2
    d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=(40, 90, 150), outline=(90, 140, 190), width=2)
    for gy in (-18, -6, 6, 18):
        d.arc([cx - 34, cy - 34, cx + 34, cy + 34], 0, 360, fill=(90, 140, 190), width=1)
    d.ellipse([cx - 34, cy + gy - 1, cx + 34, cy + gy + 1], outline=(90, 140, 190), width=1)
    # people row
    for i in range(6):
        px = x0 + 14 + i * (w - 40) // 5
        d.ellipse([px - 4, y0 + h - 26, px + 4, y0 + h - 18], fill=(200, 140, 90))
        d.rectangle([px - 5, y0 + h - 18, px + 5, y0 + h - 4], fill=(60, 44, 96))

def track_scene(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(26, 28, 34))
    for k in range(4):
        d.rectangle([x0 + 10 + k * 62, y0 + 8, x0 + 56 + k * 62, y0 + h - 8], outline=(90, 90, 96), width=2)
    d.rectangle([x0 + 16, y0 + 16, x0 + 50, y0 + h - 14], fill=(30, 110, 180))
    d.rectangle([x0 + 78, y0 + 16, x0 + 112, y0 + h - 14], fill=(180, 30, 30))
    d.rectangle([x0 + 140, y0 + 16, x0 + 174, y0 + h - 14], fill=(240, 150, 20))

def basket_scene(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(60, 36, 16))
    d.ellipse([x0 + w // 2 - 30, y0 + h - 34, x0 + w // 2 + 30, y0 + h + 8], outline=(240, 160, 40), width=4)
    d.line([x0 + w // 2 - 30, y0 + h - 14, x0 + w // 2 + 30, y0 + h - 14], fill=(240, 160, 40), width=2)
    d.line([x0 + w // 2, y0 + 6, x0 + w // 2 - 22, y0 + h - 18], fill=(240, 200, 120), width=2)
    d.ellipse([x0 + 20, y0 + 16, x0 + 40, y0 + 36], fill=(240, 150, 40))

def chart_scene(x0, y0, w, h, up=True):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(245, 243, 236))
    d.line([x0 + 8, y0 + h - 10, x0 + w - 8, y0 + h - 10], fill=GRAY, width=1)
    pts = [30, 24, 34, 20, 38, 26, 18, 40] if up else [40, 34, 38, 28, 30, 22, 24, 12]
    step = (w - 16) // (len(pts) - 1)
    for i, v in enumerate(pts):
        bx = x0 + 8 + i * step
        col = (40, 120, 60) if up else (190, 40, 40)
        d.rectangle([bx, y0 + h - 10 - v, bx + step - 6, y0 + h - 10], fill=col)

def pulse_scene(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(28, 44, 60))
    mid = y0 + h // 2
    pts = [(x0 + 6, mid), (x0 + 40, mid), (x0 + 48, mid - 14), (x0 + 56, mid + 14),
           (x0 + 64, mid - 10), (x0 + 72, mid), (x0 + w - 6, mid)]
    d.line(pts, fill=(255, 90, 90), width=2)

def icon_scene(x0, y0, w, h, kind):
    if kind == 0:  # flask / probe
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(30, 34, 44))
        d.line([x0 + 12, y0 + 10, x0 + w - 12, y0 + h - 10], fill=(255, 210, 90), width=3)
        d.ellipse([x0 + w - 26, y0 + 6, x0 + w - 6, y0 + 26], outline=(255, 210, 90), width=3)
    elif kind == 1:  # plane grounded
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(36, 40, 52))
        d.polygon([(x0 + 16, y0 + h - 14), (x0 + w - 16, y0 + h - 14), (x0 + w - 30, y0 + h - 26),
                   (x0 + 30, y0 + h - 26)], fill=(160, 164, 172))
        d.line([x0 + 10, y0 + h - 30, x0 + w - 10, y0 + h - 30], fill=(230, 230, 230), width=2)
    elif kind == 2:  # warning
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(24, 52, 90))
        d.polygon([(x0 + w // 2, y0 + 8), (x0 + w - 10, y0 + h - 10), (x0 + 10, y0 + h - 10)], outline=(255, 200, 60), width=3)
        d.line([x0 + w // 2, y0 + h // 2 - 4, x0 + w // 2, y0 + h // 2 + 6], fill=(255, 200, 60), width=3)
    elif kind == 3:  # fire
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(50, 26, 20))
        d.rectangle([x0 + 8, y0 + h - 26, x0 + w - 8, y0 + h - 6], fill=(80, 60, 50))
        d.polygon([(x0 + w // 2, y0 + 8), (x0 + w // 2 + 14, y0 + h - 26), (x0 + w // 2 - 14, y0 + h - 26)], fill=(250, 120, 30))
        d.polygon([(x0 + w // 2, y0 + 22), (x0 + w // 2 + 7, y0 + h - 26), (x0 + w // 2 - 7, y0 + h - 26)], fill=(255, 210, 80))
    else:  # quake mountain
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(30, 44, 36))
        d.polygon([(x0 + 8, y0 + h - 8), (x0 + w // 2, y0 + 12), (x0 + w - 8, y0 + h - 8)], fill=(70, 90, 78))
        d.polygon([(x0 + w // 2 - 8, y0 + 22), (x0 + w // 2, y0 + 12), (x0 + w // 2 + 8, y0 + 22)], fill=(240, 240, 240))
        d.line([x0 + 4, y0 + h - 4, x0 + w - 4, y0 + h - 4], fill=(200, 80, 60), width=2)

# ================= 3 big stories =================
big = [
    ('1', 'KYIV REGION, UKRAINE - WAR', 'REPORTED', sky_scene,
     'Russia fires 186 drones; a Kyiv-region block is destroyed',
     'Air defences downed or suppressed 161 of 186 strike drones (72 of them jet-powered) fired from eight directions. One destroyed a five-storey block in Dymer; up to seven people feared trapped, two injured. Ukrainian Air Force via (Reuters)'),
    ('2', 'ANTALYA, TURKIYE - CLIMATE', 'REPORTED', globe_scene,
     'Climate deal lands with no mention of fossil fuels',
     "The final text 'recalls' the Dubai pact whole, keeps the 35%-electricity-by-2035 goal, drops the $120bn adaptation target and is first to admit 1.5C will be overshoot. Hoekstra: 'a good deal or no deal'. (Reuters, BBC, The Guardian)"),
    ('3', 'MANAMA, BAHRAIN - IRAN', 'CLAIM', radar_scene,
     'Iran claims two US radars hit; Bahrain denies it',
     "The IRGC says it destroyed two Patriot radars on Saturday night; Bahrain's foreign ministry answered on Sunday: the target was a civilian industrial site - a fire, no injuries - and a violation of its sovereignty. (Khaleej Times, Al Jazeera)"),
]
by0 = 226
bw = (CW - 16) // 3
for i, (num, kicker, tag, scene, head, body) in enumerate(big):
    x0 = M + i * (bw + 8)
    scene(x0, by0, bw, 84)
    ltext(x0 + 4, by0 + 70, num, fc(11), (255, 255, 255))
    tagx = x0 + bw - d.textlength(tag, font=fc(8)) - 16
    d.rectangle([tagx, by0 + 68, tagx + d.textlength(tag, font=fc(8)) + 8, by0 + 80], fill=RED if tag == 'CLAIM' else (40, 110, 60))
    d.text((tagx + 4, by0 + 69), tag, font=fc(8), fill=(255, 255, 255))
    hy = by0 + 88
    ltext(x0, hy, f'{num}  {kicker}', fc(8.5), (110, 40, 30))
    hy += 13
    f_h = fit(head, SER_B, 16.5, bw)
    # wrap headline
    words, lines, cur = head.split(), [], ''
    for wd in words:
        t2 = (cur + ' ' + wd).strip()
        if d.textlength(t2, font=f_h) <= bw: cur = t2
        else: lines.append(cur); cur = wd
    lines.append(cur)
    for ln in lines[:3]:
        d.text((x0, hy), ln, font=f_h, fill=INK, anchor='la'); hy += f_h.size + 3
    hy += 2
    words, lines, cur = body.split(), [], ''
    for wd in words:
        t2 = (cur + ' ' + wd).strip()
        if d.textlength(t2, font=fs(8.5)) <= bw: cur = t2
        else: lines.append(cur); cur = wd
    lines.append(cur)
    for ln in lines[:6]:
        d.text((x0, hy), ln, font=fs(8.5), fill=(60, 62, 66), anchor='la'); hy += 10.5

# ================= 12 medium cards =================
med = [
    ('4', 'HONG KONG - ELECTION', 'chart_scene', False, '86 candidates', 'Hong Kong elects its Election Committee', '856 candidates, 773 seats, 5,700 voters; polls 09:00-18:00. (SCMP)'),
    ('5', 'WELLINGTON - CRICKET', 'chart_scene', True, '720/9 declared', 'India declare on 720/9, a record in New Zealand', 'Rahul 158, Pant 123; Gill 93*; hosts 119/1, trailing by 533. (ESPNCricinfo)'),
    ('6', 'LAS VEGAS - FORMULA 1', 'track_scene', False, 'Verstappen wins', 'Verstappen takes the Las Vegas Grand Prix', 'From pole in -1.27s;63+4. Norris +0.659; Piastri +1.529. (FIA)'),
    ('7', 'SAN ANTONIO - NBA', 'basket_scene', False, '50 points', "Wembanyama scores 50 as Spurs roll on", "50 pts, 19 rebounds, 5 blocks; 114-91 over New Orleans. (Reuters)"),
    ('8', 'GULF OF FINLAND - SHIP', 'radar_scene', False, 'Ship ablaze', 'Russian cargo ship Sparta II still burning', 'Hit by drones Saturday; Finland leads response. (Lloyd\u2019s list)'),
    ('9', 'THURAN, IRAN - ENERGY', 'icon_scene', 3, 'Power cuts', 'Iran begins rationing electricity', 'Rolling cuts on to two hours a day as war damage bites. (Wires)'),
    ('10', 'BRASILIA, BRAZIL - HEALTH', 'pulse_scene', False, 'In intensive care', 'Bolsonaro in intensive care in Brazil', 'Acute bowel obstruction, stable; surgery possible. (Reuters)'),
    ('11', 'WASHINGTON - CYBER', 'icon_scene', 0, 'FBI probe', 'FBI probes apparent hack of its crime database', 'Nationwide NCIC system paused; gun-dealer checks briefly ceased. (AP)'),
    ('12', 'BRUSSELS - TRAVEL', 'icon_scene', 1, 'Flights grounded', "Belgian controllers join Monday's national strike", 'Most flights grounded 07:00-21:00; controllers walk out. (Wires)'),
    ('13', 'MANIPUR, INDIA - POISONING', 'icon_scene', 2, 'Toll at 19', 'Toxic-liquor toll in Manipur climbs to 19', '600 in hospital; six held; toll up from 15 on Saturday. (Xinhua)'),
    ('14', 'CIANDE, INDONESIA - FIRE', 'icon_scene', 3, '3 dead, 36 missing', 'Candy-factory fire in Ciande: 3 dead, 36 missing', 'Blaze tore through the Barenti plant; search goes on. (Dellnews)'),
    ('15', 'LIMA, PERU - QUAKE TOLL', 'icon_scene', 4, '1 dead, 14 hurt', 'Peru quake toll updated: 1 dead, 16 hurt', '170 homes damaged in Lunna; the count is complete. (Reuters)'),
]
cy0 = by0 + 88 + 13 + 3 * 20 + 6 * 10.5 + 10  # below big-story text approx
cy0 = 452
ch_head, ch_ill = 96, 26
mw = (CW - 15) // 4
for i, (num, kicker, sk, karg, badge, head, body) in enumerate(med[:8]):
    col, row = i % 4, i // 4
    x0 = M + col * (mw + 5)
    y0 = cy0 + row * (ch_head + 10)
    sc = {'chart_scene': chart_scene, 'track_scene': track_scene, 'basket_scene': basket_scene,
          'radar_scene': radar_scene, 'pulse_scene': pulse_scene, 'icon_scene': icon_scene,
          'globe_scene': globe_scene, 'sky_scene': sky_scene}[sk]
    if sk == 'icon_scene':
        sc(x0, y0, mw, 34, karg)
    elif sk == 'chart_scene':
        sc(x0, y0, mw, 34, karg)
    else:
        sc(x0, y0, mw, 34)
    ltext(x0 + 3, y0 + 22, num, fc(10), (255, 255, 255))
    bx = x0 + mw - d.textlength(badge, font=fc(7.5)) - 10
    d.rectangle([bx, y0 + 2, bx + d.textlength(badge, font=fc(7.5)) + 6, y0 + 13], fill=(20, 22, 28))
    d.text((bx + 3, y0 + 3), badge, font=fc(7.5), fill=(255, 255, 255))
    ltext(x0, y0 + 38, f'{num}  {kicker}', fc(7.5), (110, 40, 30))
    f_h = fit(head, SER_B, 11.5, mw)
    words, lines, cur = head.split(), [], ''
    for wd in words:
        t2 = (cur + ' ' + wd).strip()
        if d.textlength(t2, font=f_h) <= mw: cur = t2
        else: lines.append(cur); cur = wd
    lines.append(cur)
    yy = y0 + 48
    for ln in lines[:2]:
        d.text((x0, yy), ln, font=f_h, fill=INK, anchor='la'); yy += f_h.size + 1
    words, lines, cur = body.split(), [], ''
    for wd in words:
        t2 = (cur + ' ' + wd).strip()
        if d.textlength(t2, font=fs(7)) <= mw: cur = t2
        else: lines.append(cur); cur = wd
    lines.append(cur)
    yy += 1
    for ln in lines[:2]:
        d.text((x0, yy), ln, font=fs(7), fill=(70, 72, 76), anchor='la'); yy += 8.5

# ================= map + briefs =================
my0 = 672
ltext(M, my0, 'WHERE IT HAPPENED', fc(9), INK)
ltext(M + 120, my0 + 1, 'pm=match story numbers', fs(7.5), GRAY)
# dot-matrix world (rough)
MAP = [
 "      ####    ####  ########   ####",
 " ##  ######## ########################",
 "  ################ #################",
 "   ##############   ######  ####",
 "    ##########      #######   ###",
 "     #######        #####    ###",
 "      #####          ###     ##",
 "       ###           ##    ####",
 "        ##            #    ####",
 "        ##                 ###",
 "        ##                  ##",
 "         #                ####",
 "        ####             ###",
 "        #####             #",
]
dot_x, dot_y, gap = M + 6, my0 + 16, 6
dnum = {(1,1):2,(0,2):3,(2,0):4,(1,3):5,(3,1):8,(4,2):9,(6,1):13,(5,0):10,(3,3):14,(7,1):15}
for r, row in enumerate(MAP):
    for c, ch in enumerate(row):
        if ch == '#':
            px, py = dot_x + c * gap, dot_y + r * gap
            d.ellipse([px, py, px + 2.5, py + 2.5], fill=(140, 150, 165))
for (r, c), n in dnum.items():
    px, py = dot_x + c * gap - 4, dot_y + r * gap - 4
    d.ellipse([px, py, px + 11, py + 11], fill=RED)
    d.text((px + 5.5, py + 5.5), str(n), font=fs(7), fill=(255, 255, 255), anchor='mm')

# briefs (2 columns right of map)
briefs = [
 ('9', 'Europe', "Estonia to shut five Russian border crossings: 1 Dec, after a sabotage (Reuters)"),
 ('10', 'Russia', 'Kremlin expels a Russian attaché over an alleged plot against an allied politician (Guardian)'),
 ('11', 'Ukraine', 'Ukrainian forces strike "Druzhba" pipeline and other targets overnight (Guardian)'),
 ('12', 'Asia-Pacific', 'Nepal PM Shah lands in Delhi on first visit; meets Modi Monday (AN)'),
 ('13', 'Asia-Pacific', 'Chinese bomber turns back: 170 km from Manila (AP)'),
 ('14', 'Asia-Pacific', 'Philippine MiG 29 quake: 899 km deep, off Palawan (RSMC)'),
 ('15', 'Asia-Pacific', 'Japan poll: record 92% feel friendly to South Korea (Nik)'),
 ('16', 'Asia-Pacific', 'Taiwan vice-FM chill on Xi junmen (CNA)'),
 ('17', 'Africa', 'Kenya charges its last Ebola patient (Wires)'),
 ('18', 'Africa', 'Sudan: RSF accused of killing civilians, incl. 5 children, in W. Kordofan (Guardian)'),
 ('19', 'Africa', 'Malawi rejects US report on UN/US visa bans (BBC)'),
 ('20', 'Oceania', 'Melbourne: 70 years since the 1956 Olympics opened (ABC)'),
 ('21', 'Oceania', 'Cummings keeps Australia\u2019s Test cap sojourn (Wires)'),
 ('22', 'Americas', "Trump says Permanent 'first deal' talks to mediate (H)"),
 ('23', 'World', 'Bitcoin back above $86,000 after Saturday: $2.5 trillion (Market data)'),
 ('24', 'World', 'Gold holds near $5,555 (Reuters)'),
 ('25', 'Europe', "FORECAST: ATP Finals final: Turin: 2 (see) v Alcaraz, 17:00 GMT (ATP)"),
 ('26', 'Europe', 'FORECAST: Liverpool host Manchester United, 16:30 GMT - Pochettino\u2019s United debut (Premier)'),
]
by1 = my0
for i, (num, reg, txt) in enumerate(briefs):
    col = i // 9
    row = i % 9
    x0 = M + 310 + col * 345
    y0 = by1 + 16 + row * 13.4
    d.text((x0, y0), num, font=fs(8), fill=RED, anchor='la')
    rlab = reg + ':'
    d.text((x0 + 18, y0), rlab, font=fc(8), fill=(50, 60, 120), anchor='la')
    tx0 = x0 + 22 + d.textlength(rlab, font=fc(8))
    avail = (M + 310 + 330) - tx0 if col == 0 else (W - M - 4) - tx0
    f_b = fs(8)
    while d.textlength(txt, font=f_b) > avail and f_b.size > 6:
        f_b = fs(f_b.size - 0.5)
    d.text((tx0, y0), txt, font=f_b, fill=(60, 62, 66), anchor='la')

# ---- certainty legend + date check
lg_y = 860
d.line([M, lg_y - 14, W - M, lg_y - 14], fill=(200, 196, 188), width=1)
d.text((M, lg_y), "CERTAINTY:  REPORTED = carried by the day's wires   ·   CLAIM = one side's account, labelled as such   ·   FORECAST = still to happen when drawn", font=fs(9), fill=(60, 62, 66), anchor='la')
dy0 = 900
d.rectangle([M, dy0, W - M, dy0 + 30], outline=RED, width=2)
ltext(M + 8, dy0 + 8, 'DATE CHECK', fc(10), RED)
dct = ("Left out as other days\u2019 news: the 400-drone barrage (Thu 19-20 Nov) - the 14-drone night and the Kryvyi Rih double-tap (Fri 20-21) - El Chapo Isidro captured (Fri) - Bayelsa boat, 24 dead (Fri)")
d.text((M + 92, dy0 + 4), dct, font=fs(8), fill=(60, 62, 66), anchor='la')

# footer
d.rectangle([0, 986, W, 1002], fill=INK)
d.text((M, 989), 'Sources: Reuters, BBC, AP, Al Jazeera, The Guardian, Hindustan Times, Fox Sports, SCMP, ESPNCricinfo, Orlando Sentinel and the wires named with each dispatch. Pictures and map original; drawn in code.', font=fs(7), fill=(200, 198, 192), anchor='la')
d.rectangle([0, 1002, W, H], fill=(240, 238, 232))
d.text((M, H - 18), 'THE WORLD IN ONE DAY', font=fc(9), fill=INK, anchor='lm')
d.text((W - M, H - 18), 'SUNDAY 22 NOVEMBER 2026  ·  ONE PAGE', font=fc(9), fill=INK, anchor='rm')

out = os.environ.get('MAKEFUN_OUTPUT_DIR') or '/tmp/newsout22'
os.makedirs(out, exist_ok=True)
im.save(os.path.join(out, 'entry.png'), optimize=True)
print('written', os.path.getsize(os.path.join(out, 'entry.png')))
