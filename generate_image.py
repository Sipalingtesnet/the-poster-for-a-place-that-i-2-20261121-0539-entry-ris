#!/usr/bin/env python3
"""VELMARA - a vintage travel poster for a place that does not exist.

Floating terraced islands above an amber sea at sunset, a white lighthouse
on the highest terrace, a giant low sun, teal-to-amber sky, waterfalls,
birds, dark framing cliffs and a thin cream border. The only text is the
place name. 100% Pillow primitives, deterministic, no external images.
"""

import math
import random

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HORIZON = 650
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

CREAM = (244, 231, 200)
INK = (16, 40, 45)          # dark teal ink for outlines / birds / cliffs
SUN_CORE = (255, 220, 150)
SUN_EDGE = (250, 178, 88)
AMBER = (238, 158, 74)
ROCK_DARK = (24, 52, 56)
ROCK_MID = (38, 74, 74)
TERRACE_TOP = (122, 128, 82)     # sunlit olive tops
TERRACE_TOP_HI = (168, 158, 96)
TERRACE_SIDE = (52, 88, 82)
WATERFALL = (222, 236, 226)

rng = random.Random(42)  # fixed seed: fully deterministic


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def gradient(d, y0, y1, stops):
    """Per-row vertical gradient. stops = [(y, (r,g,b)), ...] sorted."""
    for y in range(y0, y1):
        for i in range(len(stops) - 1):
            ya, ca = stops[i]
            yb, cb = stops[i + 1]
            if ya <= y <= yb:
                t = 0.0 if yb == ya else (y - ya) / (yb - ya)
                d.line([(0, y), (W, y)], fill=lerp(ca, cb, t))
                break


def overlay(img):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    return ov, ImageDraw.Draw(ov)


def composite(img, ov):
    return Image.alpha_composite(img, ov)


def draw_sun(img, d):
    cx, cy, r = 512, 470, 170  # bottom edge sits just above the horizon
    ov, o = overlay(img)
    for i in range(14, 0, -1):  # soft concentric glow
        rr = r + i * 16
        a = int(10 + (14 - i) * 2.2)
        o.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                  fill=(252, 190, 100, a))
    img = composite(img, ov)
    d = ImageDraw.Draw(img)
    # banded disc: warm edge -> bright core, vintage flat-ish shading
    bands = 26
    for i in range(bands, 0, -1):
        rr = r * i / bands
        t = i / bands
        col = lerp(SUN_CORE, SUN_EDGE, t * t)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col)
    return img, d


def draw_sky(img, d):
    gradient(d, 0, HORIZON, [
        (0, (10, 52, 62)),
        (280, (24, 86, 88)),
        (500, (110, 118, 88)),
        (HORIZON, AMBER),
    ])
    # thin vintage cloud bands
    ov, o = overlay(img)
    bands = [
        (150, 300, 90, 7, (18, 70, 76, 90)),
        (330, 620, 130, 8, (26, 88, 90, 80)),
        (560, 240, 150, 7, (250, 190, 110, 70)),
        (600, 700, 170, 8, (252, 200, 120, 80)),
        (628, 420, 200, 6, (255, 214, 140, 90)),
    ]
    for x, y, half, thick, col in bands:
        o.ellipse([x - half, y - thick, x + half, y + thick], fill=col)
    return composite(img, ov), None


def draw_sea(img, d):
    gradient(d, HORIZON, H, [
        (HORIZON, (214, 142, 72)),
        (700, (44, 92, 90)),
        (860, (18, 58, 64)),
        (H, (8, 38, 46)),
    ])
    d.line([(0, HORIZON), (W, HORIZON)], fill=(255, 216, 150), width=2)
    # long amber sun reflection: tapering streaks down the water
    ov, o = overlay(img)
    y = HORIZON + 6
    while y < 980:
        depth = (y - HORIZON) / (980 - HORIZON)
        half = int(190 * (1.0 - depth * 0.78))
        jitter = int(14 * math.sin(y * 0.55) + rng.uniform(-8, 8))
        cx = 512 + jitter
        thick = max(2, int(6 - depth * 3))
        a = int(150 * (1.0 - depth * 0.72))
        col = lerp((255, 214, 140), (238, 158, 74), depth)
        o.ellipse([cx - half, y - thick, cx + half, y + thick],
                  fill=col + (a,))
        y += 9 + int(depth * 8)
    # a few quiet wave lines elsewhere on the sea
    for x, y, half in [(180, 730, 70), (880, 760, 80), (140, 850, 60),
                       (900, 880, 70), (320, 930, 80), (760, 960, 60)]:
        o.ellipse([x - half, y - 2, x + half, y + 2],
                  fill=(210, 220, 200, 46))
    return composite(img, ov), None


def draw_island(img, cx, top_y, width, layers, layer_h=30):
    """Terraced floating island: sunlit top, stepped slabs, rocky keel."""
    ov, o = overlay(img)
    d = ImageDraw.Draw(img)
    rx = width // 2
    ry = max(10, int(width * 0.085))

    # rocky keel tapering to a point below the terraces
    keel_top = top_y + layers * layer_h
    keel_tip = keel_top + int(width * 0.55)
    kw = int(rx * 0.82)
    d.polygon([(cx - kw, keel_top), (cx + kw, keel_top),
               (cx + kw // 3, keel_top + (keel_tip - keel_top) // 2),
               (cx + 6, keel_tip), (cx - kw // 2, keel_top + 18)],
              fill=ROCK_DARK)
    d.polygon([(cx - kw, keel_top), (cx - kw // 2, keel_top + 18),
               (cx + 6, keel_tip), (cx - 4, keel_top + 10)],
              fill=ROCK_MID)

    # terrace slabs, bottom-up so upper steps overlap cleanly
    for i in range(layers - 1, -1, -1):
        t = i / max(1, layers - 1)
        sw = int(rx * (1.0 - 0.16 * i))       # each step narrower
        sy = top_y + i * layer_h
        sry = max(7, int(sw * 0.085))
        side = lerp(TERRACE_SIDE, ROCK_MID, t * 0.5)
        d.polygon([(cx - sw, sy), (cx + sw, sy),
                   (cx + sw - 6, sy + layer_h), (cx - sw + 6, sy + layer_h)],
                  fill=side)
        top_col = lerp(TERRACE_TOP, TERRACE_TOP_HI, 1.0 - t)
        d.ellipse([cx - sw, sy - sry, cx + sw, sy + sry], fill=top_col)
        d.arc([cx - sw, sy - sry, cx + sw, sy + sry], 180, 360,
              fill=(222, 208, 150), width=2)

    # sunlit top surface
    d.ellipse([cx - rx, top_y - ry, cx + rx, top_y + ry],
              fill=TERRACE_TOP_HI)
    d.arc([cx - rx, top_y - ry, cx + rx, top_y + ry], 180, 360,
          fill=(238, 222, 160), width=2)
    return img, ov, o


def draw_waterfall(img, x, y_top, y_sea, width=13):
    ov, o = overlay(img)
    spread = width + 8
    o.polygon([(x - width // 2, y_top), (x + width // 2, y_top),
               (x + spread // 2, y_sea), (x - spread // 2, y_sea)],
              fill=WATERFALL + (205,))
    for dx in (-width // 4, 0, width // 4):
        o.line([(x + dx, y_top + 4), (x + dx, y_sea - 3)],
               fill=(250, 252, 246, 150), width=2)
    # splash + mist where it meets the sea
    o.ellipse([x - 30, y_sea - 7, x + 30, y_sea + 7],
              fill=(235, 242, 232, 170))
    o.ellipse([x - 44, y_sea - 12, x + 44, y_sea + 10],
              fill=(235, 242, 232, 60))
    return composite(img, ov)


def draw_lighthouse(img, cx, base_y):
    d = ImageDraw.Draw(img)
    h = 118
    top_y = base_y - h
    bw, tw = 19, 12  # half widths at base / top
    # tower
    d.polygon([(cx - bw, base_y), (cx + bw, base_y),
               (cx + tw, top_y), (cx - tw, top_y)],
              fill=(246, 241, 228))
    d.polygon([(cx + 4, base_y), (cx + bw, base_y),
               (cx + tw, top_y), (cx + 4, top_y)],
              fill=(214, 208, 190))  # shaded side
    # one warm vintage band
    band_y = base_y - 46
    d.polygon([(cx - bw + 4, band_y + 14), (cx + bw - 4, band_y + 14),
               (cx + bw - 6, band_y), (cx - bw + 6, band_y)],
              fill=(206, 106, 74))
    # gallery deck
    d.rectangle([cx - tw - 5, top_y - 6, cx + tw + 5, top_y], fill=INK)
    # lamp room with warm light
    d.rectangle([cx - 9, top_y - 24, cx + 9, top_y - 6], fill=(255, 206, 116))
    d.rectangle([cx - 9, top_y - 24, cx + 9, top_y - 6], outline=INK, width=2)
    d.line([(cx, top_y - 24), (cx, top_y - 6)], fill=INK, width=2)
    # dome + finial
    d.pieslice([cx - 11, top_y - 36, cx + 11, top_y - 14], 180, 360, fill=INK)
    d.line([(cx, top_y - 36), (cx, top_y - 42)], fill=INK, width=3)
    # door
    d.rectangle([cx - 5, base_y - 16, cx + 5, base_y], fill=INK)
    return top_y - 15  # lamp centre y


def draw_beam(img, cx, cy):
    ov, o = overlay(img)
    for end_x, spread in ((cx - 330, 34), (cx + 250, 30)):
        o.polygon([(cx, cy), (end_x, cy - spread), (end_x, cy + spread)],
                  fill=(255, 210, 120, 60))
        o.polygon([(cx, cy), (end_x, cy - spread // 2),
                   (end_x, cy + spread // 2)],
                  fill=(255, 226, 150, 55))
    o.ellipse([cx - 22, cy - 22, cx + 22, cy + 22],
              fill=(255, 226, 150, 120))
    o.ellipse([cx - 10, cy - 10, cx + 10, cy + 10],
              fill=(255, 240, 190, 200))
    return composite(img, ov)


def draw_bird(d, x, y, s=1.0):
    r = int(13 * s)
    box_l = [x - 2 * r, y - r, x, y + r]
    box_r = [x, y - r, x + 2 * r, y + r]
    d.arc(box_l, 200, 340, fill=INK, width=3)
    d.arc(box_r, 200, 340, fill=INK, width=3)


def draw_cliffs(d):
    left = [(0, H), (0, 768), (46, 792), (84, 838), (128, 872),
            (176, 934), (238, H)]
    right = [(W, H), (W, 786), (966, 812), (924, 856), (886, 892),
             (838, 948), (790, H)]
    d.polygon(left, fill=(10, 30, 34))
    d.polygon(right, fill=(10, 30, 34))
    d.polygon([(0, 768), (46, 792), (84, 838), (30, 820), (0, 800)],
              fill=(20, 46, 50))
    d.polygon([(W, 786), (966, 812), (924, 856), (980, 838), (W, 820)],
              fill=(20, 46, 50))


def draw_title(img):
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(SERIF_BOLD, 147)  # ~110 pt
    word = "VELMARA"
    tracking = 24
    widths = [font.getlength(ch) for ch in word]
    total = sum(widths) + tracking * (len(word) - 1)
    x = (W - total) / 2
    baseline = 246  # centred across the upper third
    # soft drop shadow
    sx = x
    for ch, cw in zip(word, widths):
        d.text((sx + 5, baseline + 6), ch, font=font, fill=(12, 32, 36),
               anchor="ls")
        sx += cw + tracking
    # cream letters with a subtle dark outline
    sx = x
    for ch, cw in zip(word, widths):
        d.text((sx, baseline), ch, font=font, fill=CREAM, anchor="ls",
               stroke_width=4, stroke_fill=(20, 42, 46))
        sx += cw + tracking


def main(output_path="entry.png"):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    img, _ = draw_sky(img, d)
    d = ImageDraw.Draw(img)
    img, d = draw_sun(img, d)
    img, _ = draw_sea(img, d)
    d = ImageDraw.Draw(img)

    # small distant island silhouetted against the sun's reflection
    img, _, _ = draw_island(img, 430, 585, 110, 2, layer_h=22)
    img = draw_waterfall(img, 468, 600, 700, width=8)

    # left island
    img, _, _ = draw_island(img, 250, 500, 240, 3, layer_h=28)
    img = draw_waterfall(img, 352, 512, 726, width=13)

    # main island with the lighthouse on its highest terrace
    img, _, _ = draw_island(img, 740, 430, 300, 4, layer_h=30)
    img = draw_waterfall(img, 612, 444, 706, width=15)
    d = ImageDraw.Draw(img)
    lamp_y = draw_lighthouse(img, 740, 428)
    img = draw_beam(img, 740, lamp_y)
    d = ImageDraw.Draw(img)

    # birds crossing the sky
    for x, y, s in [(300, 342, 1.0), (352, 316, 0.8), (618, 356, 0.9),
                    (878, 372, 0.75), (180, 300, 0.7)]:
        draw_bird(d, x, y, s)

    draw_cliffs(d)

    # thin cream border frame inside the canvas edge
    d.rectangle([26, 26, W - 27, H - 27], outline=CREAM, width=3)
    d.rectangle([36, 36, W - 37, H - 37], outline=CREAM, width=1)

    draw_title(img)

    img.convert("RGB").save(output_path, "PNG", optimize=True)


if __name__ == "__main__":
    main()
