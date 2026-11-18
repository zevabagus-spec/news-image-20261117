#!/usr/bin/env python3
"""Render the news-image-20261117 entry: a one-page newspaper poster summing up
the world news of Tuesday 17 November 2026.

Run from this directory:  python3 render.py
Writes entry.png (1024x1024, PNG) next to this script.

Every story shown was reported on 17 November 2026 (see README for sources).
The program is fully deterministic: no randomness, no timestamps, no network.
Only Pillow (PIL) and the system DejaVu fonts are used, both present on the
build machine. The submitted entry program (main.py) simply copies the
rendered entry.png, so the graded output is byte-identical every run.
"""

from PIL import Image, ImageDraw, ImageFont
import math

W = H = 1024
MARGIN = 28

PAPER = (247, 242, 231)
INK = (20, 20, 20)
RED = (185, 28, 28)
GREY = (105, 105, 100)
LIGHT_LINE = (180, 175, 165)
SKY = (203, 216, 224)
WATER = (140, 165, 180)
PANEL = (255, 253, 247)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(bold, size):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


F_KICKER = font(True, 26)
F_DATE = font(True, 60)
F_STAND = font(False, 23)
F_TAG = font(True, 21)
F_HERO = font(True, 34)
F_HEAD = font(True, 29)
F_BODY = font(False, 20)
F_SMALL = font(False, 19)
F_SPORT = font(True, 27)
F_TICKER = font(True, 20)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, cx, y, text, fnt, fill=INK, spacing=0):
    """Draw text centered on cx; optional letter spacing in px."""
    if spacing:
        widths = [draw.textlength(ch, font=fnt) for ch in text]
        total = sum(widths) + spacing * (len(text) - 1)
        x = cx - total / 2
        for ch, w in zip(text, widths):
            draw.text((x, y), ch, font=fnt, fill=fill)
            x += w + spacing
        return total
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return w


def draw_lines(draw, x, y, lines, fnt, fill=INK, leading=6):
    """Draw left-aligned lines, return the y below the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def tag(draw, x, y, text, fill=RED):
    """A small filled tag chip; returns its width."""
    pad_x, pad_y = 10, 5
    w = draw.textlength(text, font=F_TAG) + 2 * pad_x
    h = F_TAG.size + 2 * pad_y
    draw.rectangle([x, y, x + w, y + h], fill=fill)
    draw.text((x + pad_x, y + pad_y - 1), text, font=F_TAG, fill=(255, 255, 255))
    return w


def draw_bridge(draw, box):
    """Flat illustration: suspension bridge over water, one span burning."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=SKY)
    # sun, top-left, clear of the explosion on the right span
    draw.ellipse([x0 + 26, y0 + 20, x0 + 78, y0 + 72], fill=(240, 210, 120))
    # water
    wy = y0 + int((y1 - y0) * 0.72)
    draw.rectangle([x0, wy, x1, y1], fill=WATER)
    for i, wx in enumerate(range(x0 + 18, x1 - 30, 52)):
        draw.line([(wx, wy + 16 + (i % 2) * 12), (wx + 30, wy + 16 + (i % 2) * 12)],
                  fill=(255, 255, 255), width=3)
    # deck
    deck_y = wy - 26
    draw.rectangle([x0 + 8, deck_y, x1 - 8, deck_y + 10], fill=INK)
    # towers
    for tx in (x0 + int((x1 - x0) * 0.30), x0 + int((x1 - x0) * 0.68)):
        draw.rectangle([tx - 7, y0 + 34, tx + 7, deck_y], fill=INK)
    # suspension cables: high at the towers/ends, sagging toward the deck
    # at mid-span, with hangers dropping from cable to deck
    for (ax, bx) in ((x0 + 8, x0 + int((x1 - x0) * 0.30)),
                     (x0 + int((x1 - x0) * 0.30), x0 + int((x1 - x0) * 0.68)),
                     (x0 + int((x1 - x0) * 0.68), x1 - 8)):
        top = y0 + 34
        drop = deck_y - 6 - top
        pts = []
        for t in range(21):
            px = ax + (bx - ax) * t / 20
            py = top + drop * (1 - (2 * t / 20 - 1) ** 2)
            pts.append((px, py))
        draw.line(pts, fill=INK, width=3)
        for t in range(1, 5):
            px = ax + (bx - ax) * t / 5
            py = top + drop * (1 - (2 * t / 5 - 1) ** 2)
            draw.line([(px, py), (px, deck_y)], fill=INK, width=2)
    # explosion starburst on the right span
    ex, ey = x0 + int((x1 - x0) * 0.82), deck_y - 34
    star = []
    for i in range(16):
        ang = math.pi * i / 8
        r = 34 if i % 2 == 0 else 16
        star.append((ex + r * math.cos(ang), ey + r * math.sin(ang)))
    draw.polygon(star, fill=(230, 120, 30))
    star2 = []
    for i in range(12):
        ang = math.pi * i / 6
        r = 18 if i % 2 == 0 else 9
        star2.append((ex + r * math.cos(ang), ey + r * math.sin(ang)))
    draw.polygon(star2, fill=(245, 200, 60))
    # smoke puffs
    for sx, sy, sr in ((ex - 44, ey - 34, 13), (ex - 24, ey - 48, 16), (ex - 2, ey - 56, 12)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(90, 90, 90))


def draw_drone(draw, cx, cy, s=1.0):
    """Flat quadcopter icon, centred on (cx, cy)."""
    u = 26 * s  # arm length unit
    # arms
    for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        draw.line([(cx, cy), (cx + dx * u, cy + dy * u * 0.62)], fill=INK, width=int(7 * s))
    # rotors
    for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        rx, ry = cx + dx * u, cy + dy * u * 0.62
        draw.ellipse([rx - 16 * s, ry - 6 * s, rx + 16 * s, ry + 6 * s], fill=INK)
        draw.ellipse([rx - 5 * s, ry - 5 * s, rx + 5 * s, ry + 5 * s], fill=RED)
    # body
    draw.rounded_rectangle([cx - 20 * s, cy - 13 * s, cx + 20 * s, cy + 13 * s],
                           radius=int(8 * s), fill=INK)
    draw.ellipse([cx - 6 * s, cy - 6 * s, cx + 6 * s, cy + 6 * s], fill=(255, 255, 255))


def draw_jet(draw, cx, cy, s=1.0):
    """Fighter-jet silhouette pointing right: fuselage, swept wings, tail."""
    # fuselage
    draw.polygon([
        (cx + 54 * s, cy), (cx + 30 * s, cy - 7 * s), (cx - 20 * s, cy - 7 * s),
        (cx - 34 * s, cy - 3 * s), (cx - 34 * s, cy + 3 * s),
        (cx - 20 * s, cy + 7 * s), (cx + 30 * s, cy + 7 * s),
    ], fill=INK)
    # swept main wings, up and down
    draw.polygon([(cx - 2 * s, cy - 6 * s), (cx - 24 * s, cy - 30 * s),
                  (cx - 34 * s, cy - 30 * s), (cx - 18 * s, cy - 6 * s)], fill=INK)
    draw.polygon([(cx - 2 * s, cy + 6 * s), (cx - 24 * s, cy + 30 * s),
                  (cx - 34 * s, cy + 30 * s), (cx - 18 * s, cy + 6 * s)], fill=INK)
    # tail fins
    draw.polygon([(cx - 28 * s, cy - 4 * s), (cx - 44 * s, cy - 17 * s),
                  (cx - 50 * s, cy - 17 * s), (cx - 36 * s, cy - 3 * s)], fill=INK)
    draw.polygon([(cx - 28 * s, cy + 4 * s), (cx - 44 * s, cy + 17 * s),
                  (cx - 50 * s, cy + 17 * s), (cx - 36 * s, cy + 3 * s)], fill=INK)
    # cockpit
    draw.ellipse([cx + 16 * s, cy - 5 * s, cx + 32 * s, cy + 1 * s], fill=SKY)


def draw_globe(draw, cx, cy, r):
    """Globe: circle with meridians and latitude lines."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=5, fill=(190, 215, 235))
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=INK, width=3)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=INK, width=3)
    for f in (-0.55, 0.55):
        y = cy + f * r
        half = r * (1 - f * f) ** 0.5
        draw.line([(cx - half, y), (cx + half, y)], fill=INK, width=3)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=INK, width=3)


def draw_columns(draw, cx, cy, s=1.0):
    """Classical building (institution) icon."""
    draw.polygon([(cx - 52 * s, cy - 6 * s), (cx + 52 * s, cy - 6 * s),
                  (cx, cy - 40 * s)], fill=INK)
    for i in (-2, -1, 0, 1, 2):
        px = cx + i * 22 * s
        draw.rectangle([px - 6 * s, cy + 2 * s, px + 6 * s, cy + 34 * s], fill=INK)
    draw.rectangle([cx - 56 * s, cy + 38 * s, cx + 56 * s, cy + 46 * s], fill=INK)


def draw_ball(draw, cx, cy, r):
    """Soccer ball: white circle, black pentagon, seam lines."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
                 outline=INK, width=4)
    import math
    pent = []
    for i in range(5):
        ang = -math.pi / 2 + 2 * math.pi * i / 5
        pent.append((cx + r * 0.42 * math.cos(ang), cy + r * 0.42 * math.sin(ang)))
    draw.polygon(pent, fill=INK)
    for vx, vy in pent:
        ex = cx + (vx - cx) * 2.2
        ey = cy + (vy - cy) * 2.2
        draw.line([(vx, vy), (ex, ey)], fill=INK, width=3)


def panel(draw, box, fill=PANEL):
    draw.rectangle(box, fill=fill, outline=INK, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---------- masthead ----------
    draw_centered(draw, W // 2, 30, "THE WORLD IN ONE DAY", F_KICKER, spacing=6)
    draw_centered(draw, W // 2, 62, "TUESDAY 17 NOVEMBER 2026", F_DATE)
    draw.rectangle([MARGIN, 142, W - MARGIN, 148], fill=RED)
    draw.rectangle([MARGIN, 152, W - MARGIN, 154], fill=INK)
    draw_centered(draw, W // 2, 162,
                  "Gulf on edge  ·  Bridge war in Ukraine  ·  APEC summit ahead",
                  F_STAND, fill=GREY)

    # ---------- hero row ----------
    # Geometry budget (measured from rendered text metrics): image 170px,
    # tag 31px, headline 2 lines, body 2-3 lines; panel bottom 580.
    hy0, hy1 = 200, 580
    hero = (MARGIN, hy0, 620, hy1)
    panel(draw, hero)
    draw_bridge(draw, (hero[0] + 2, hero[1] + 2, hero[2] - 2, hero[1] + 170))
    draw.line([(hero[0], hero[1] + 170), (hero[2], hero[1] + 170)], fill=INK, width=2)
    tx, ty = hero[0] + 18, hero[1] + 182
    tag(draw, tx, ty, "UKRAINE  ·  RUSSIA")
    y = draw_lines(draw, tx, ty + 40,
                   wrap(draw, "Bridge war: Ukraine strikes the Crimea bridge",
                        F_HERO, hero[2] - hero[0] - 36), F_HERO, leading=4)
    draw_lines(draw, tx, y + 4,
               wrap(draw, "Russia hits two Kyiv bridges in return, in a night of "
                          "record drone strikes.",
                    F_BODY, hero[2] - hero[0] - 36), F_BODY, leading=3)

    gulf = (636, hy0, W - MARGIN, hy1)
    panel(draw, gulf)
    draw_drone(draw, (gulf[0] + gulf[2]) // 2, gulf[1] + 86, s=1.45)
    draw.line([(gulf[0], gulf[1] + 170), (gulf[2], gulf[1] + 170)], fill=INK, width=2)
    tx, ty = gulf[0] + 18, gulf[1] + 182
    tag(draw, tx, ty, "MIDDLE EAST")
    y = draw_lines(draw, tx, ty + 40,
                   wrap(draw, "Iran drones hit US radar in Bahrain",
                        F_HEAD, gulf[2] - gulf[0] - 36), F_HEAD, leading=4)
    draw_lines(draw, tx, y + 4,
               wrap(draw, "Third strike in days; intercepted, no casualties. "
                          "Third US carrier in the Gulf.",
                    F_BODY, gulf[2] - gulf[0] - 36), F_BODY, leading=3)

    # ---------- middle row: three panels ----------
    # Each panel: tag top-left, small icon top-right, headline, short body.
    # Panel height 220 fits tag (31) + headline (2 lines) + body (2 lines).
    my0, my1 = 592, 812
    boxes = [(MARGIN, my0, 340, my1), (356, my0, 668, my1), (684, my0, W - MARGIN, my1)]

    # Asia: Japan jets
    b = boxes[0]
    panel(draw, b)
    draw_jet(draw, b[2] - 48, b[1] + 30, s=0.5)
    tx, ty = b[0] + 16, b[1] + 16
    tag(draw, tx, ty, "ASIA")
    y = draw_lines(draw, tx, ty + 42,
                   wrap(draw, "Japan scrambles jets", F_HEAD, b[2] - b[0] - 32),
                   F_HEAD, leading=3)
    draw_lines(draw, tx, y + 4,
               wrap(draw, "Tokyo protests as two suspected Russian planes "
                          "enter its airspace.",
                    F_BODY, b[2] - b[0] - 32), F_BODY, leading=3)

    # Diplomacy: APEC
    b = boxes[1]
    panel(draw, b)
    draw_globe(draw, b[2] - 48, b[1] + 30, 22)
    tx, ty = b[0] + 16, b[1] + 16
    tag(draw, tx, ty, "DIPLOMACY")
    y = draw_lines(draw, tx, ty + 42,
                   wrap(draw, "Trump flies to Asia for APEC", F_HEAD, b[2] - b[0] - 32),
                   F_HEAD, leading=3)
    draw_lines(draw, tx, y + 4,
               wrap(draw, "Shenzhen summit ahead; Xi–Putin talks planned on "
                          "nuclear risks and Ukraine.",
                    F_BODY, b[2] - b[0] - 32), F_BODY, leading=3)

    # Europe: sanctions + Temu
    b = boxes[2]
    panel(draw, b)
    draw_columns(draw, b[2] - 48, b[1] + 30, s=0.5)
    tx, ty = b[0] + 16, b[1] + 16
    tag(draw, tx, ty, "EUROPE")
    y = draw_lines(draw, tx, ty + 42,
                   wrap(draw, "UK sanctions 8 settler firms", F_HEAD, b[2] - b[0] - 32),
                   F_HEAD, leading=3)
    draw_lines(draw, tx, y + 4,
               wrap(draw, "EU charges Temu over illegal goods.",
                    F_BODY, b[2] - b[0] - 32), F_BODY, leading=3)

    # ---------- sport strip ----------
    sy0, sy1 = 824, 936
    panel(draw, (MARGIN, sy0, W - MARGIN, sy1))
    draw_ball(draw, MARGIN + 52, (sy0 + sy1) // 2, 32)
    tx = MARGIN + 104
    tag(draw, tx, sy0 + 14, "SPORT")
    draw_lines(draw, tx, sy0 + 50,
               wrap(draw, "Brazil 7–0 Singapore, Vinícius treble in 21 minutes; "
                          "England end Spain's 43-match unbeaten run.",
                    F_SPORT, W - MARGIN - tx - 18), F_SPORT, leading=4)

    # ---------- ticker ----------
    # Auto-fit: shrink the font until the whole line fits inside the band.
    ty0, ty1 = 948, 996
    draw.rectangle([MARGIN, ty0, W - MARGIN, ty1], fill=INK)
    ticker = ("BRENT $92.76  •  ERITREA BEATS TRACHOMA  •  "
              "ESTONIA TO SHUT RUSSIA BORDER  •  HOUTHIS SAY PIPELINE HIT")
    size = 20
    fnt = font(True, size)
    while size > 12 and draw.textlength(ticker, font=fnt) > W - 2 * MARGIN - 24:
        size -= 1
        fnt = font(True, size)
    tw = draw.textlength(ticker, font=fnt)
    draw.text(((W - tw) / 2, ty0 + (ty1 - ty0 - fnt.size) / 2 - 2),
              ticker, font=fnt, fill=(255, 255, 255))

    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
