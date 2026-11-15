#!/usr/bin/env python3
"""Gera anuncio de produto (Black Achadinhos) em 1080x1350 e 1080x1080.
Uso: python3 gerar_anuncio_produto.py --foto F.png --nome "iPhone 17e" --linha2 "256 GB" \
     --preco "R$ 4.299" --sufixo "no Pix" --saida-prefixo anuncio/iphone17e
Gera <prefixo>-1080x1350.jpg e <prefixo>-1080x1080.jpg (JPEG q92)."""
import argparse
from PIL import Image, ImageDraw, ImageFont

BG = (12, 12, 14); AMARELO = (255, 212, 0); BRANCO = (255, 255, 255); CINZA = (170, 170, 175)
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
MAX_ZOOM = 1.5

def f(path, size): return ImageFont.truetype(path, size)

def fit(draw, text, path, size, maxw):
    while draw.textlength(text, font=f(path, size)) > maxw and size > 10: size -= 2
    return f(path, size)

def center(draw, cx, y, text, font, fill):
    w = draw.textlength(text, font=font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)

def left(draw, x, y, text, font, fill): draw.text((x, y), text, font=font, fill=fill)

def card(img, foto, box, pad):
    """Cartao branco arredondado com a foto centralizada (nunca ampliada alem de MAX_ZOOM)."""
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(box, radius=44, fill=BRANCO)
    aw, ah = x1 - x0 - 2 * pad, y1 - y0 - 2 * pad
    s = min(aw / foto.width, ah / foto.height, MAX_ZOOM)
    p = foto.resize((round(foto.width * s), round(foto.height * s)), Image.LANCZOS)
    img.paste(p, (x0 + (x1 - x0 - p.width) // 2, y0 + (y1 - y0 - p.height) // 2))

def rodape(d, W, H, my, canal):
    cx = W // 2
    center(d, cx, H - my - 68, canal, f(REG, 30), CINZA)
    center(d, cx, H - my - 28, "Publicidade · link de afiliado", f(REG, 24), CINZA)

def preco_pill(d, cx, y, w, h, preco, sufixo):
    d.rounded_rectangle((cx - w // 2, y, cx + w // 2, y + h), radius=h // 2, fill=AMARELO)
    txt = f"{preco} {sufixo}".strip()
    fnt = fit(d, txt, BOLD, 80, w - 80)
    bb = d.textbbox((0, 0), txt, font=fnt)
    d.text((cx - (bb[0] + bb[2]) / 2, y + h / 2 - (bb[1] + bb[3]) / 2), txt, font=fnt, fill=BG)

def retrato(foto, a):
    W, H = 1080, 1350; mx, my = 108, 135
    img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img); cx = W // 2
    center(d, cx, my, a.nome, fit(d, a.nome, BOLD, 120, W - 2 * mx), BRANCO)
    center(d, cx, my + 140, a.linha2, f(BOLD, 64), AMARELO)
    card(img, foto, (cx - 320, my + 237, cx + 320, my + 237 + 580), 26)
    preco_pill(d, cx, H - my - 68 - 40 - 120, W - 2 * mx, 120, a.preco, a.sufixo)
    rodape(d, W, H, my, a.canal)
    return img

def quadrado(foto, a):
    W, H = 1080, 1080; mx, my = 108, 108
    img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img)
    cy = 120; ch = 690
    card(img, foto, (mx, cy, mx + 440, cy + ch), 22)
    rx = mx + 440 + 44; rw = W - mx - rx; rcx = rx + rw // 2
    left(d, rx, cy + 40, a.nome, fit(d, a.nome, BOLD, 90, rw), BRANCO)
    left(d, rx, cy + 160, a.linha2, f(BOLD, 56), AMARELO)
    pw = rw; ph = 150; y = cy + ch - (ph + 90)
    d.rounded_rectangle((rx, y, rx + pw, y + ph + 90), radius=36, fill=AMARELO)
    fp = fit(d, a.preco, BOLD, 80, pw - 90); fs = f(BOLD, 46)
    bb = d.textbbox((0, 0), a.preco, font=fp)
    d.text((rx + (pw - (bb[2] - bb[0])) / 2 - bb[0], y + 48 - bb[1]), a.preco, font=fp, fill=BG)
    ws = d.textlength(a.sufixo, font=fs)
    d.text((rx + (pw - ws) / 2, y + 48 + (bb[3] - bb[1]) + 28), a.sufixo, font=fs, fill=BG)
    rodape(d, W, H, my, a.canal)
    return img

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--foto", required=True); p.add_argument("--nome", required=True)
    p.add_argument("--linha2", default=""); p.add_argument("--preco", required=True)
    p.add_argument("--sufixo", default="no Pix")
    p.add_argument("--canal", default="Vendido no Mercado Livre · Black Achadinhos")
    p.add_argument("--saida-prefixo", required=True)
    a = p.parse_args()
    foto = Image.open(a.foto).convert("RGB")
    retrato(foto, a).save(a.saida_prefixo + "-1080x1350.jpg", quality=92)
    quadrado(foto, a).save(a.saida_prefixo + "-1080x1080.jpg", quality=92)
