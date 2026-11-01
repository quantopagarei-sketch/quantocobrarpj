"""Uso: python3 banners.py <pasta_saida> "<titulo>" "<subtitulo>" "<preco>" "<cor_hex>" "<b1|b2|b3>"
Gera capa.png (1080x1080) e os 6 banners de afiliado."""
import sys, os
from PIL import Image, ImageDraw, ImageFont

out, titulo, sub, preco, cor, bullets = sys.argv[1:7]
bullets = bullets.split("|")
B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F = lambda p, s: ImageFont.truetype(p, s)
base = tuple(int(cor[i:i+2], 16) for i in (1, 3, 5))
dark = tuple(max(0, int(c * 0.65)) for c in base)
YEL = (255, 205, 60)

def grad(w, h):
    im = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(im)
    for y in range(h):
        t = y / max(1, h - 1)
        d.line([(0, y), (w, y)], fill=tuple(int(base[i] * (1 - t) + dark[i] * t) for i in range(3)))
    return im

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def fit(d, text, path, maxw, maxh, start, minsize=8):
    s = start
    while s > minsize:
        f = F(path, s)
        ls = wrap(d, text, f, maxw)
        h = len(ls) * s * 1.18
        if h <= maxh and all(d.textlength(l, font=f) <= maxw for l in ls):
            return f, ls, s
        s -= 1
    f = F(path, minsize); return f, wrap(d, text, f, maxw), minsize

def block(d, x, y, text, path, maxw, maxh, start, fill=(255, 255, 255)):
    f, ls, s = fit(d, text, path, maxw, maxh, start)
    for l in ls:
        d.text((x, y), l, font=f, fill=fill); y += int(s * 1.18)
    return y

def button(d, x, y, w, h, label):
    d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=YEL)
    s = int(h * 0.45)
    while s > 7 and d.textlength(label, font=F(B, s)) > w - 16: s -= 1
    f = F(B, s); tw = d.textlength(label, font=f)
    d.text((x + (w - tw) / 2, y + (h - s) / 2 - 2), label, font=f, fill=(30, 30, 30))

# capa
W = 1080
im = grad(W, W); d = ImageDraw.Draw(im)
d.rounded_rectangle([60, 60, W - 60, W - 60], radius=40, outline=(255, 255, 255), width=4)
d.rounded_rectangle([110, 120, 140 + int(d.textlength(os.environ.get("TAG", "PDF / DIGITAL"), font=F(B, 30))) + 30, 180], radius=30, fill=YEL)
d.text((140, 133), os.environ.get("TAG", "PDF / DIGITAL"), font=F(B, 30), fill=(30, 30, 30))
y = block(d, 110, 230, titulo, B, W - 220, 300, 96)
y = block(d, 110, y + 15, sub, R, W - 220, 110, 40, fill=(235, 245, 240))
y += 30
for b in bullets:
    d.text((110, y), "✓ " + b, font=F(R, 36), fill=(255, 255, 255)); y += 52
d.text((110, W - 190), preco, font=F(B, 80), fill=YEL)
im.save(os.path.join(out, "capa.png"))

cta = "Garanta o seu"
for w, h in [(250, 250), (300, 250), (336, 280), (468, 60), (728, 90), (160, 600)]:
    im = grad(w, h); d = ImageDraw.Draw(im); p = max(6, int(min(w, h) * 0.06))
    if h <= 90:  # horizontais
        bw = int(w * 0.26) if w > 500 else int(w * 0.3)
        block(d, p, p - 2, titulo, B, int(w * 0.45), h - 2 * p, int(h * 0.42))
        f = F(B, int(h * 0.38)); pw = d.textlength(preco, font=f)
        d.text((w - bw - 2 * p - pw, (h - h * 0.38) / 2 - 3), preco, font=f, fill=YEL)
        button(d, w - bw - p, int(h * 0.2), bw, int(h * 0.6), cta)
    elif w <= 160:  # arranha-céu
        y = block(d, p * 2, p * 3, titulo, B, w - 4 * p, 180, 26)
        y = block(d, p * 2, y + 10, sub, R, w - 4 * p, 150, 16, fill=(235, 245, 240))
        y += 10
        for b in bullets[:3]:
            y = block(d, p * 2, y + 4, "✓ " + b, R, w - 4 * p, 60, 13)
        d.text((p * 2, h - 150), preco, font=F(B, 26), fill=YEL)
        button(d, p * 2, h - 90, w - 4 * p, 44, cta)
    else:
        y = block(d, p * 2, p * 2, titulo, B, w - 4 * p, int(h * 0.3), int(h * 0.12))
        block(d, p * 2, y + 6, sub, R, w - 4 * p, int(h * 0.62) - y - 6, int(h * 0.07), fill=(235, 245, 240))
        fp = F(B, int(h * 0.11))
        d.text((p * 2, h - int(h * 0.36)), preco, font=fp, fill=YEL)
        button(d, p * 2, h - int(h * 0.2), int(w * 0.6), int(h * 0.14), cta)
    im.save(os.path.join(out, f"banner-{w}x{h}.png"))
print("ok", out)
