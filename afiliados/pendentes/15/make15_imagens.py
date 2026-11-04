import math, random, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = "/home/claude/quantocobrarpj/afiliados/15"
GF = "/usr/share/fonts/truetype/google-fonts/"
PB, PM, PR, PSB = GF + "Poppins-Bold.ttf", GF + "Poppins-Medium.ttf", GF + "Poppins-Regular.ttf", GF + "Poppins-Bold.ttf"
F = lambda p, s: ImageFont.truetype(p, int(s))

RED = (179, 38, 46); DARK = (110, 18, 26); GOLD = (217, 164, 65); GOLD_L = (240, 200, 110)
GREEN = (31, 92, 64); CREAM = (255, 246, 232); WHITE = (255, 255, 255)

TITLE = "Planner de Natal e Ano Novo"
SUB = "Organize as festas sem estresse e sem estourar o orçamento"
BUL = ["Orçamento e lista de presentes", "Ceia: quantidades por pessoa e receitas", "Cronograma de 6 semanas e Réveillon"]
PRICE = "R$ 17,90"
CTA = "Quero o meu"


def radial_bg(w, h):
    im = Image.new("RGB", (w, h))
    px = im.load()
    cx, cy = w * 0.5, h * 0.35
    md = math.hypot(max(cx, w - cx), max(cy, h - cy))
    for y in range(h):
        for x in range(w):
            t = min(1, math.hypot(x - cx, y - cy) / md) ** 1.3
            px[x, y] = tuple(int(RED[i] * (1 - t) + DARK[i] * t) for i in range(3))
    return im


def star(d, cx, cy, r, fill, points=5, inner=0.45, rot=-90):
    pts = []
    for i in range(points * 2):
        rr = r if i % 2 == 0 else r * inner
        a = math.radians(rot + i * 180 / points)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill)


def sparkle(d, cx, cy, r, fill):
    star(d, cx, cy, r, fill, points=4, inner=0.22, rot=-90)


def ornament(im, cx, top, cy, r, color, cap=GOLD):
    """bolinha pendurada: fio do topo até cy-r"""
    d = ImageDraw.Draw(im)
    d.line([(cx, top), (cx, cy - r - r * 0.25)], fill=GOLD_L, width=max(1, int(r * 0.06)))
    # gancho
    d.ellipse([cx - r * 0.12, cy - r - r * 0.42, cx + r * 0.12, cy - r - r * 0.18], outline=GOLD_L, width=max(1, int(r * 0.05)))
    # sombra suave
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    sd.ellipse([cx - r + r * 0.12, cy - r + r * 0.18, cx + r + r * 0.12, cy + r + r * 0.18], fill=(0, 0, 0, 90))
    sh = sh.filter(ImageFilter.GaussianBlur(r * 0.15))
    im.paste(sh, (0, 0), sh)
    d = ImageDraw.Draw(im)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    # faixa decorativa
    dk = tuple(int(c * 0.75) for c in color)
    d.arc([cx - r, cy - r * 0.35, cx + r, cy + r * 0.35], 0, 180, fill=cap, width=max(2, int(r * 0.09)))
    for k in (-0.5, 0, 0.5):
        d.ellipse([cx + k * r - r * 0.07, cy + r * 0.28 - r * 0.07 - abs(k) * r * 0.12, cx + k * r + r * 0.07, cy + r * 0.28 + r * 0.07 - abs(k) * r * 0.12], fill=cap)
    # brilho
    hl = Image.new("RGBA", im.size, (0, 0, 0, 0)); hd = ImageDraw.Draw(hl)
    hd.ellipse([cx - r * 0.62, cy - r * 0.7, cx - r * 0.12, cy - r * 0.3], fill=(255, 255, 255, 120))
    hl = hl.filter(ImageFilter.GaussianBlur(r * 0.08))
    im.paste(hl, (0, 0), hl)
    d = ImageDraw.Draw(im)
    # tampinha
    d.rounded_rectangle([cx - r * 0.28, cy - r - r * 0.2, cx + r * 0.28, cy - r + r * 0.08], radius=max(1, int(r * 0.06)), fill=cap)


def snow(d, w, h, n, seed, rmax, alpha_fill=(255, 255, 255)):
    rnd = random.Random(seed)
    for _ in range(n):
        x, y = rnd.uniform(0, w), rnd.uniform(0, h)
        r = rnd.uniform(rmax * 0.3, rmax)
        c = tuple(int(alpha_fill[i] * 0.22 + RED[i] * 0.78) for i in range(3))
        d.ellipse([x - r, y - r, x + r, y + r], fill=c)


def ctext(d, cx, y, text, font, fill, anchor="mt"):
    d.text((cx, y), text, font=font, fill=fill, anchor=anchor)


def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines


def fit(d, text, path, maxw, maxh, start, lh=1.12, minsize=7, maxlines=99):
    s = start
    while s > minsize:
        f = F(path, s); ls = wrap(d, text, f, maxw)
        if len(ls) <= maxlines and len(ls) * s * lh <= maxh and all(d.textlength(l, font=f) <= maxw for l in ls):
            return f, ls, s
        s -= 1
    f = F(path, minsize); return f, wrap(d, text, f, maxw), minsize


def check(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD)
    w = max(2, int(r * 0.32))
    d.line([(cx - r * 0.45, cy + r * 0.02), (cx - r * 0.1, cy + r * 0.38), (cx + r * 0.5, cy - r * 0.35)], fill=DARK, width=w, joint="curve")


def button(d, x, y, w, h, label, font_path=PB):
    d.rounded_rectangle([x, y + max(2, h * 0.07), x + w, y + h + max(2, h * 0.07)], radius=h // 2, fill=(120, 80, 20))
    d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=GOLD)
    s = int(h * 0.46)
    while s > 7 and d.textlength(label, font=F(font_path, s)) > w - h * 0.6: s -= 1
    d.text((x + w / 2, y + h / 2), label, font=F(font_path, s), fill=DARK, anchor="mm")


def gold_band(im, y0, y1, text, size):
    d = ImageDraw.Draw(im); w = im.width
    d.rectangle([0, y0, w, y1], fill=GOLD)
    d.line([(0, y0 + 6), (w, y0 + 6)], fill=GOLD_L, width=2)
    d.line([(0, y1 - 6), (w, y1 - 6)], fill=(170, 120, 40), width=2)
    d.text((w / 2, (y0 + y1) / 2), text, font=F(PB, size), fill=DARK, anchor="mm")


# ---------------- CAPA 1200 ----------------
W = 1200
im = radial_bg(W, W)
d = ImageDraw.Draw(im)
snow(d, W, W, 140, 7, 6)
rnd = random.Random(3)
for _ in range(22):
    x = rnd.choice([rnd.uniform(70, 230), rnd.uniform(W - 230, W - 70)])
    y = rnd.uniform(290, 600) if rnd.random() < 0.6 else rnd.uniform(720, 1000)
    if 170 < x < 1030 and y > 700: continue
    sparkle(d, x, y, rnd.uniform(5, 11), tuple(int(GOLD_L[i] * 0.55 + RED[i] * 0.45) for i in range(3)))
# moldura dourada dupla
d.rounded_rectangle([34, 34, W - 34, W - 34], radius=34, outline=GOLD, width=5)
d.rounded_rectangle([50, 50, W - 50, W - 50], radius=24, outline=(200, 140, 60), width=2)

# bolinhas penduradas no topo
orn = [(160, 215, 50, GREEN), (285, 148, 34, GOLD), (W - 285, 148, 34, CREAM), (W - 160, 215, 50, GREEN)]
for cx, cy, r, c in orn:
    ornament(im, cx, 50, cy, r, c, cap=GOLD if c != GOLD else CREAM)
d = ImageDraw.Draw(im)
star(d, W / 2, 128, 46, GOLD)
star(d, W / 2, 128, 22, GOLD_L)
sparkle(d, W / 2 - 92, 108, 14, GOLD_L); sparkle(d, W / 2 + 92, 108, 14, GOLD_L)

# etiqueta
tag = "KIT IMPRIMÍVEL  •  PDF  •  44+ PÁGINAS"
ft = F(PB, 30); tw = d.textlength(tag, font=ft)
d.rounded_rectangle([W / 2 - tw / 2 - 30, 205, W / 2 + tw / 2 + 30, 257], radius=26, fill=CREAM)
d.text((W / 2, 231), tag, font=ft, fill=RED, anchor="mm")

# titulo
f1 = F(PB, 100)
ctext(d, W / 2, 272, "Planner de", f1, WHITE)
f2 = F(PB, 116)
# "Natal & Ano Novo" em duas linhas para impacto
ctext(d, W / 2, 368, "Natal e", f2, GOLD_L)
ctext(d, W / 2, 478, "Ano Novo", f2, GOLD_L)

# faixa dourada
gold_band(im, 625, 690, "ORGANIZE  •  PLANEJE  •  CELEBRE", 34)
d = ImageDraw.Draw(im)
sparkle(d, 110, 657, 16, DARK); sparkle(d, W - 110, 657, 16, DARK)

# subtitulo
fs = F(PM, 38)
ls = ["Organize as festas sem estresse", "e sem estourar o orçamento"]
y = 712
for l in ls:
    ctext(d, W / 2, y, l, fs, CREAM); y += 46

# bullets
fb = F(PR, 33)
bw = max(d.textlength(b, font=fb) for b in BUL) + 60
bx = W / 2 - bw / 2
y += 14
for b in BUL:
    check(d, bx + 18, y + 22, 18)
    d.text((bx + 56, y + 22), b, font=fb, fill=WHITE, anchor="lm"); y += 52

# preço
fp = F(PB, 54)
pw = d.textlength(PRICE, font=fp)
px0 = W - 90 - pw - 60
d.rounded_rectangle([px0, W - 175, W - 90, W - 95], radius=40, fill=GOLD)
d.text(((px0 + W - 90) / 2, W - 135), PRICE, font=fp, fill=DARK, anchor="mm")
# selo canto esquerdo
fl = F(PB, 26); lab = "PRONTO PARA IMPRIMIR"; lw = d.textlength(lab, font=fl)
d.rounded_rectangle([90, W - 165, 90 + lw + 50, W - 105], radius=30, outline=GOLD_L, width=3)
d.text((115 + lw / 2, W - 135), lab, font=fl, fill=CREAM, anchor="mm")
assert y < W - 190, y
im.save(os.path.join(OUT, "capa.png"))
im.resize((600, 600), Image.LANCZOS).save("/home/claude/work15/capa-600.png")


# ---------------- BANNERS ----------------
def base(w, h):
    im = radial_bg(w, h); d = ImageDraw.Draw(im)
    snow(d, w, h, int(w * h / 2500) + 6, w + h, max(2, min(w, h) * 0.018))
    bw = max(2, int(min(w, h) * 0.025))
    d.rectangle([0, 0, w - 1, h - 1], outline=GOLD, width=bw)
    return im


def mini_ornaments(im, specs):
    for cx, top, cy, r, c in specs:
        ornament(im, cx, top, cy, r, c, cap=GOLD if c != GOLD else CREAM)


def square(w, h):
    im = base(w, h); d = ImageDraw.Draw(im)
    s = min(w, h) / 250
    mini_ornaments(im, [(w - 30 * s, 0, 28 * s, 12 * s, GREEN), (w - 56 * s, 0, 19 * s, 8 * s, GOLD)])
    d = ImageDraw.Draw(im)
    p = int(16 * s)
    # tag
    ft = F(PB, 10.5 * s); tag = "PDF • 44+ PÁGINAS"
    tw = d.textlength(tag, font=ft)
    d.rounded_rectangle([p, p, p + tw + 16 * s, p + 20 * s], radius=int(10 * s), fill=CREAM)
    d.text((p + 8 * s + tw / 2, p + 10 * s), tag, font=ft, fill=RED, anchor="mm")
    y = p + 28 * s
    ls = ["Planner de Natal", "e Ano Novo"]
    sz = int(32 * s)
    while d.textlength(ls[0], font=F(PB, sz)) > w - 2 * p - 30 * s: sz -= 1
    f = F(PB, sz)
    for i, l in enumerate(ls):
        d.text((p, y), l, font=f, fill=GOLD_L if i else WHITE, anchor="lt"); y += sz * 1.12
    y += 6 * s
    d.rectangle([p, y, p + 46 * s, y + 3 * s], fill=GOLD); y += 9 * s
    avail = h - 82 * s - y
    f, ls, sz = fit(d, SUB, PR, w - 2 * p, avail, int(14 * s), lh=1.2)
    if sz < 12:
        f, ls, sz = fit(d, "Organize as festas sem estresse", PR, w - 2 * p, avail, int(14 * s), lh=1.2)
    for l in ls:
        d.text((p, y), l, font=f, fill=CREAM); y += sz * 1.2
    # rodapé: preço + botão
    by = h - p - 34 * s
    fp = F(PB, 25 * s)
    d.text((p, by + 17 * s), PRICE, font=fp, fill=GOLD_L, anchor="lm")
    pw = d.textlength(PRICE, font=fp)
    bx = p + pw + 12 * s
    button(d, bx, by, w - p - bx, 34 * s, CTA)
    assert y <= by - 2, (w, h, y, by)
    return im


def sky(w, h):
    im = base(w, h); d = ImageDraw.Draw(im)
    mini_ornaments(im, [(40, 0, 50, 17, GREEN), (80, 0, 34, 12, GOLD), (120, 0, 56, 17, CREAM)])
    d = ImageDraw.Draw(im)
    p = 14
    y = 84
    ft = F(PB, 11); tag = "PDF • 44+ PÁGINAS"
    d.rounded_rectangle([p, y, w - p, y + 22], radius=11, fill=CREAM)
    d.text((w / 2, y + 11), tag, font=ft, fill=RED, anchor="mm"); y += 34
    for i, l in enumerate(["Planner", "de Natal", "e Ano", "Novo"]):
        f = F(PB, 26)
        d.text((w / 2, y), l, font=f, fill=WHITE if i == 0 else GOLD_L, anchor="mt"); y += 29
    y += 8
    d.rectangle([w / 2 - 25, y, w / 2 + 25, y + 3], fill=GOLD); y += 14
    f, ls, sz = fit(d, SUB, PM, w - 2 * p, 100, 13, lh=1.2)
    for l in ls:
        d.text((w / 2, y), l, font=f, fill=CREAM, anchor="mt"); y += sz * 1.2
    y += 8
    fb = F(PR, 11.5)
    for b in BUL:
        ls = wrap(d, b, fb, w - 2 * p - 22)
        check(d, p + 7, y + 8, 7)
        for l in ls:
            d.text((p + 20, y), l, font=fb, fill=WHITE); y += 15
        y += 5
    fp = F(PB, 28)
    d.text((w / 2, h - 108), PRICE, font=fp, fill=GOLD_L, anchor="mm")
    button(d, p, h - 78, w - 2 * p, 40, CTA)
    star(d, w / 2, h - 18, 7, GOLD)
    assert y < h - 128, y
    return im


def leader(w, h):
    im = base(w, h); d = ImageDraw.Draw(im)
    big = w > 600
    p = int(h * 0.14)
    # ornamentos à esquerda
    if big:
        mini_ornaments(im, [(26, 0, 50, 15, GREEN), (58, 0, 36, 11, GOLD)])
        x0 = 82
    else:
        mini_ornaments(im, [(22, 0, 34, 11, GREEN)])
        x0 = 42
    d = ImageDraw.Draw(im)
    bw = int(w * 0.2) if big else int(w * 0.24)
    bh = int(h * 0.56)
    bx = w - bw - p
    button(d, bx, (h - bh) / 2 - 1, bw, bh, CTA)
    fp = F(PB, h * (0.34 if big else 0.36))
    pw = d.textlength(PRICE, font=fp)
    px = bx - 12 - pw
    d.text((px, h / 2), PRICE, font=fp, fill=GOLD_L, anchor="lm")
    maxw = px - x0 - 12
    if big:
        f = F(PB, 30)
        while d.textlength(TITLE, font=f) > maxw: f = F(PB, f.size - 1)
        d.text((x0, h * 0.36), TITLE, font=f, fill=WHITE, anchor="lm")
        f2 = F(PR, 15)
        sub = "Orçamento, presentes, ceia e Réveillon • PDF 44+ págs."
        while d.textlength(sub, font=f2) > maxw: f2 = F(PR, f2.size - 1)
        d.text((x0, h * 0.70), sub, font=f2, fill=CREAM, anchor="lm")
    else:
        f = F(PB, 20)
        while d.textlength("Planner de Natal", font=f) > maxw: f = F(PB, f.size - 1)
        d.text((x0, h * 0.30), "Planner de Natal", font=f, fill=WHITE, anchor="lm")
        f2 = f
        d.text((x0, h * 0.70), "e Ano Novo", font=f, fill=GOLD_L, anchor="lm")
    print(w, h, "title size", f.size, "sub", f2.size)
    return im


for w, h in [(250, 250), (300, 250), (336, 280), (468, 60), (728, 90), (160, 600)]:
    if h <= 90: im = leader(w, h)
    elif w <= 160: im = sky(w, h)
    else: im = square(w, h)
    im.save(os.path.join(OUT, f"banner-{w}x{h}.png"))

for fn in sorted(x for x in os.listdir(OUT) if x.endswith(".png")) + ["/home/claude/work15/capa-600.png"]:
    pth = fn if fn.startswith("/") else os.path.join(OUT, fn)
    print(pth, Image.open(pth).size)
