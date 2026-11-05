#!/usr/bin/env python3
"""Gera um pin vertical do Pinterest (1000x1500) a partir de uma imagem 4:3 do produto.

Uso:
  python3 pinterest/make_pin.py --src produto.jpg --out pin.jpg \
      --headline "Budget an irregular income in minutes" \
      --sub "Excel + Google Sheets template" \
      --bullets "Monthly dashboard & charts|Baseline paycheck system|Instant download" \
      [--accent "#2F5D50"] [--style 1|2|3]

Estilos (varie para o Pinterest não ver pins repetidos):
  1 = faixa colorida no topo com o título, imagem no meio, lista embaixo
  2 = título escuro sobre fundo claro, imagem grande, faixa colorida embaixo
  3 = imagem no topo, título e lista embaixo
"""
import argparse
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT_DIR = "/usr/share/fonts/truetype/google-fonts/"
W, H = 1000, 1500


def font(name, size):
    return ImageFont.truetype(FONT_DIR + f"Poppins-{name}.ttf", size)


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_text(draw, text, name, max_w, max_lines, start, minimum):
    size = start
    while size >= minimum:
        f = font(name, size)
        lines = wrap(draw, text, f, max_w)
        if len(lines) <= max_lines:
            return f, lines
        size -= 2
    f = font(name, minimum)
    return f, wrap(draw, text, f, max_w)[:max_lines]


def paste_card(canvas, src, box_w, x, y, radius=26):
    im = src.convert("RGB")
    ratio = box_w / im.width
    im = im.resize((box_w, int(im.height * ratio)), Image.LANCZOS)
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius, fill=255)
    shadow = Image.new("RGBA", (im.width + 60, im.height + 60), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle([30, 36, im.width + 30, im.height + 36], radius, fill=(0, 0, 0, 70))
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    canvas.paste(shadow, (x - 30, y - 30), shadow)
    canvas.paste(im, (x, y), mask)
    return im.height


def draw_lines(draw, lines, fnt, color, y, line_h, center=True, x=60):
    for ln in lines:
        if center:
            tw = draw.textlength(ln, font=fnt)
            draw.text(((W - tw) / 2, y), ln, font=fnt, fill=color)
        else:
            draw.text((x, y), ln, font=fnt, fill=color)
        y += line_h
    return y


def bullets_block(draw, items, accent, dark, y, size=36):
    f = font("Medium", size)
    for it in items:
        it = it.strip()
        if not it:
            continue
        cx, cy = 92, y + size * 0.72
        draw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=accent)
        draw.line([(cx - 9, cy), (cx - 2, cy + 8), (cx + 10, cy - 8)], fill=(255, 255, 255), width=5)
        lines = wrap(draw, it, f, W - 150 - 60)
        for ln in lines:
            draw.text((130, y), ln, font=f, fill=dark)
            y += int(size * 1.35)
        y += 14
    return y


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--headline", required=True)
    ap.add_argument("--sub", default="")
    ap.add_argument("--bullets", default="")
    ap.add_argument("--accent", default="#2F5D50")
    ap.add_argument("--style", type=int, default=1)
    ap.add_argument("--footer", default="Instant download  •  CellwiseSheets on Etsy")
    a = ap.parse_args()

    src = Image.open(a.src)
    accent = hex_rgb(a.accent)
    dark = (33, 37, 41)
    light = (247, 246, 242)
    canvas = Image.new("RGB", (W, H), light)
    d = ImageDraw.Draw(canvas)
    items = [b for b in a.bullets.split("|") if b.strip()][:3]

    if a.style == 1:
        d.rectangle([0, 0, W, 380], fill=accent)
        f, lines = fit_text(d, a.headline, "Bold", W - 120, 3, 78, 48)
        lh = int(f.size * 1.18)
        total = lh * len(lines) + (56 if a.sub else 0)
        y = (380 - total) // 2
        y = draw_lines(d, lines, f, (255, 255, 255), y, lh)
        if a.sub:
            fs = font("Medium", 34)
            draw_lines(d, wrap(d, a.sub, fs, W - 120)[:1], fs, (225, 238, 232), y + 6, 44)
        h = paste_card(canvas, src, 920, 40, 420)
        y = 420 + h + 50
        y = bullets_block(d, items, accent, dark, y)
    elif a.style == 2:
        f, lines = fit_text(d, a.headline, "Bold", W - 120, 3, 80, 50)
        lh = int(f.size * 1.16)
        y = draw_lines(d, lines, f, dark, 60, lh)
        if a.sub:
            fs = font("Medium", 34)
            y = draw_lines(d, wrap(d, a.sub, fs, W - 120)[:1], fs, accent, y + 8, 44)
        h = paste_card(canvas, src, 920, 40, y + 40)
        yb = y + 40 + h + 40
        d.rectangle([0, yb, W, H], fill=accent)
        fb = font("Medium", 36)
        ff2 = font("Regular", 28)
        rows = []
        for it in items[:3]:
            rows += wrap(d, "•  " + it.strip(), fb, W - 140)
        block = len(rows) * 52 + 70
        yy = yb + max(30, (H - yb - block) // 2)
        for r in rows:
            d.text((80, yy), r, font=fb, fill=(255, 255, 255))
            yy += 52
        tw2 = d.textlength(a.footer, font=ff2)
        d.text(((W - tw2) / 2, max(yy + 24, H - 70)), a.footer, font=ff2, fill=(235, 235, 235))
    else:
        h = paste_card(canvas, src, 920, 40, 50)
        y = 50 + h + 50
        f, lines = fit_text(d, a.headline, "Bold", W - 120, 3, 72, 46)
        lh = int(f.size * 1.16)
        y = draw_lines(d, lines, f, dark, y, lh)
        if a.sub:
            fs = font("Medium", 34)
            y = draw_lines(d, wrap(d, a.sub, fs, W - 120)[:1], fs, accent, y + 4, 44)
        y = bullets_block(d, items, accent, dark, y + 30)

    ff = font("Regular", 28)
    tw = d.textlength(a.footer, font=ff)
    if a.style != 2:
        d.text(((W - tw) / 2, H - 70), a.footer, font=ff, fill=(110, 115, 120))
    canvas.save(a.out, "JPEG", quality=90, optimize=True)
    print(a.out)


if __name__ == "__main__":
    main()
