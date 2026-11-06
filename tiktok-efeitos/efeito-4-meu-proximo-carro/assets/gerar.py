#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C02 · Meu próximo carro: gera TODAS as imagens do efeito.

Como rodar (de qualquer pasta):
    python3 gerar.py

Precisa de: Python 3 + Pillow + numpy.
Fontes (as duas sob SIL Open Font License 1.1, as mesmas do C01):
  - Inter Display Black/ExtraBold  -> /usr/share/fonts/opentype/inter/
  - Noto Color Emoji               -> /usr/share/fonts/truetype/noto/NotoColorEmoji.ttf
    (no Pillow só funciona com size=109 e embedded_color=True)

Os textos vêm de ../textos.json (linha1/linha2 de cada carta). Se o redator
trocar um texto, basta rodar de novo. O desenho de cada carta está na função
CENAS[n] (n = número da carta; reservas = 100 + n).

Identidade visual (diferente do Torcedômetro de propósito):
  - carta = etiqueta arredondada SEM recortes, com faixa de asfalto e tracejado
    amarelo embaixo (no C01 é um ingresso com recortes e medalha redonda);
  - desenho "estacionado" na borda de cima (no C01 fica dentro de uma medalha);
  - paleta: amarelo de faixa, turquesa, coral e grafite de asfalto;
  - carros desenhados aqui mesmo, em vetor simples: genéricos, de lado, parados,
    sem grade, sem logo, sem emblema, sem placa.

Saída (nesta pasta):
  titulo.png, titulo_toque.png ............. 512x256 (título sobre a cabeça)
  cartas/carta_01..26.png .................. 512x256 (sequência do sorteio)
  reservas/reserva_01..04.png .............. 512x256
  quadrado_512/... ......................... os mesmos, centralizados em 512x512
  icone_162.png, icone_alt_162.png ......... ícones de envio (162x162)
  icone_512.png, icone_alt_512.png ......... mesmos ícones em tamanho grande
  previa.png ............................... folha de conferência
  lista-de-arquivos.txt .................... lista com tamanhos e pesos
"""
import json
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
TEXTOS = os.path.join(AQUI, "..", "textos.json")

FONT_DIR = "/usr/share/fonts/opentype/inter"
F_BLACK = os.path.join(FONT_DIR, "InterDisplay-Black.otf")
F_XBOLD = os.path.join(FONT_DIR, "InterDisplay-ExtraBold.otf")
F_BOLD = os.path.join(FONT_DIR, "InterDisplay-Bold.otf")
F_SEMI = os.path.join(FONT_DIR, "InterDisplay-SemiBold.otf")
F_EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

S = 3            # desenha em 3x e reduz com LANCZOS (bordas lisas)
W, H = 512, 256  # tamanho final de título e cartas (igual ao C01: o template é o mesmo)

# ---------------------------------------------------------------- paleta
# Amarelo de faixa, turquesa, coral e grafite de asfalto.
# Evitados como cores principais: vermelho+branco, azul+preto+branco, verde+branco.
GRAFITE = "#22252C"      # contorno dos desenhos
ASFALTO = ("#33363F", "#1E2026")
AMARELO = "#FFD43B"      # tracejado e destaque de texto
CORAL = "#FF7A52"
TURQUESA = "#1FC8C0"
LILAS = "#9B7BFF"
PRATA = "#C6CED8"
CREME = "#F2E2BE"
CARRO_AMARELO = "#FFC93C"

PALETAS = {
    # top/bot = gradiente do corpo; shade = contorno do texto e sombra dura; dest = cor da linha "(…)"
    "amarelo":  dict(top="#FFE766", bot="#FFB61A", shade="#6A3A00", dest="#FFFFFF"),
    "turquesa": dict(top="#47EADB", bot="#0E9FB0", shade="#04404C", dest="#FFE03D"),
    "coral":    dict(top="#FFB07E", bot="#FF6F47", shade="#7A220E", dest="#FFE03D"),
    "grafite":  dict(top="#5D6576", bot="#353A46", shade="#121419", dest="#FFD43B"),
}

# ---------------------------------------------------------------- geometria (em 1x)
BODY = (16, 58, 496, 234)    # x0, y0, x1, y1 da etiqueta
R_BODY = 30
BORDA = 7                    # borda branca
FAIXA_Y = 209                # começo da faixa de asfalto (até BODY[3])
TEXT_AREA = (36, 96, 476, 204)
TAM_MAX = 54
TAM_MIN = 34
ILU_BASE = 92                # onde fica a base do desenho (ele "estaciona" na borda de cima)
ILU_MAX = (292, 78)          # tamanho do desenho (sem o contorno branco): ele é ampliado/reduzido para caber
MARGEM_TOPO = 3              # o contorno branco nunca pode encostar na borda de cima da imagem


def rgb(h, a=255):
    if isinstance(h, tuple):
        return h if len(h) == 4 else h + (a,)
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def mix(c1, c2, t):
    a, b = rgb(c1), rgb(c2)
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(4))


def escurecer(c, t):
    return mix(c, "#000000", t)


def clarear(c, t):
    return mix(c, "#FFFFFF", t)


# ---------------------------------------------------------------- utilidades de desenho
def gradiente(w, h, paradas, direcao=(0.15, 0.85)):
    """paradas = [(pos 0..1, '#hex'), ...]; direcao = peso de x e de y."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    t = (xx / max(w - 1, 1)) * direcao[0] + (yy / max(h - 1, 1)) * direcao[1]
    t = (t - t.min()) / max(t.max() - t.min(), 1e-6)
    out = np.zeros((h, w, 4), np.float32)
    pos = [p for p, _ in paradas]
    cores = [np.array(rgb(c), np.float32) for _, c in paradas]
    for ch in range(4):
        out[..., ch] = np.interp(t, pos, [c[ch] for c in cores])
    return Image.fromarray(out.clip(0, 255).astype(np.uint8), "RGBA")


def interseccao(*ms):
    out = np.array(ms[0])
    for m in ms[1:]:
        out = np.minimum(out, np.array(m))
    return Image.fromarray(out)


def uniao(*ms):
    out = np.array(ms[0])
    for m in ms[1:]:
        out = np.maximum(out, np.array(m))
    return Image.fromarray(out)


def menos(m1, m2):
    return Image.fromarray(np.clip(np.array(m1).astype(int) - np.array(m2).astype(int), 0, 255).astype(np.uint8))


def deslocar(m, dx, dy):
    out = Image.new(m.mode, m.size, 0)
    out.paste(m, (int(dx), int(dy)))
    return out


def camada_cor(size, cor, mascara, alpha_mult=1.0):
    c = rgb(cor)
    lay = Image.new("RGBA", size, c[:3] + (0,))
    a = mascara if alpha_mult == 1.0 else mascara.point(lambda v: int(v * alpha_mult))
    lay.putalpha(a)
    return lay


def recortar(lay, mascara):
    """Multiplica o alfa de uma camada RGBA por uma máscara."""
    a = np.array(lay.split()[3]).astype(np.float32) * np.array(mascara).astype(np.float32) / 255.0
    out = lay.copy()
    out.putalpha(Image.fromarray(a.clip(0, 255).astype(np.uint8)))
    return out


def estrela4(d, cx, cy, r, cor):
    """Brilho de 4 pontas."""
    k = r * 0.28
    pts = [(cx, cy - r), (cx + k, cy - k), (cx + r, cy), (cx + k, cy + k),
           (cx, cy + r), (cx - k, cy + k), (cx - r, cy), (cx - k, cy - k)]
    d.polygon(pts, fill=rgb(cor))


def caminho_arred(pts_r, passos=14):
    """Polígono com cantos arredondados. pts_r = [(x, y, raio), ...]."""
    out = []
    n = len(pts_r)
    for i in range(n):
        x0, y0, _ = pts_r[i - 1]
        x1, y1, r = pts_r[i]
        x2, y2, _ = pts_r[(i + 1) % n]
        d01 = math.hypot(x1 - x0, y1 - y0)
        d12 = math.hypot(x2 - x1, y2 - y1)
        r = min(r, d01 / 2, d12 / 2)
        if r <= 0.01:
            out.append((x1, y1))
            continue
        ax, ay = x1 + (x0 - x1) * r / d01, y1 + (y0 - y1) * r / d01
        bx, by = x1 + (x2 - x1) * r / d12, y1 + (y2 - y1) * r / d12
        for k in range(passos + 1):
            t = k / passos
            out.append(((1 - t) ** 2 * ax + 2 * (1 - t) * t * x1 + t ** 2 * bx,
                        (1 - t) ** 2 * ay + 2 * (1 - t) * t * y1 + t ** 2 * by))
    return out


def bezier(p0, p1, p2, p3, n=40):
    pts = []
    for i in range(n + 1):
        t = i / n
        a, b, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t ** 2, t ** 3
        pts.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return pts


def com_contorno(im, px, cor="#FFFFFF"):
    """Contorno em volta de uma imagem com alfa (adesivo branco ou traço escuro)."""
    px = max(1, int(round(px)))
    pad = px + 4
    a = Image.new("L", (im.width + 2 * pad, im.height + 2 * pad), 0)
    a.paste(im.split()[3], (pad, pad))
    blur = a.filter(ImageFilter.GaussianBlur(px / 2.0))
    dil = blur.point(lambda v: 255 if v > 14 else int(v * 18))
    out = camada_cor(a.size, cor, dil)
    out.alpha_composite(im, (pad, pad))
    return out


def com_sombra(im, dx, dy, raio, alpha=0.28, cor="#000000"):
    pad = int(raio * 3) + max(abs(int(dx)), abs(int(dy)))
    base = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    a = Image.new("L", base.size, 0)
    a.paste(im.split()[3], (pad + int(dx), pad + int(dy)))
    a = a.filter(ImageFilter.GaussianBlur(raio))
    base.alpha_composite(camada_cor(base.size, cor, a, alpha))
    base.alpha_composite(im, (pad, pad))
    return base, pad


def colar_centro(dst, im, cx, cy):
    dst.alpha_composite(im, (int(round(cx - im.width / 2)), int(round(cy - im.height / 2))))


def aparar(im):
    bb = im.getbbox()
    return im.crop(bb) if bb else im


def reduzir(img):
    return img.resize((img.width // S, img.height // S), Image.LANCZOS)


# ---------------------------------------------------------------- emoji
_EMOJI_FONT = None


def emoji(ch, tam):
    """Renderiza um emoji Noto (109 px) e redimensiona para caber em tam x tam."""
    global _EMOJI_FONT
    if _EMOJI_FONT is None:
        _EMOJI_FONT = ImageFont.truetype(F_EMOJI, 109)
    ch = ch.replace("️", "")
    im = Image.new("RGBA", (180, 180), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((90, 90), ch, font=_EMOJI_FONT, embedded_color=True, anchor="mm")
    bb = im.getbbox()
    if bb is None:
        raise SystemExit(f"emoji sem glifo: {ch!r}")
    im = im.crop(bb)
    k = tam / max(im.size)
    return im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)


def adesivo(ch, tam, giro=0, borda=2.6):
    """Emoji com contorno branco de adesivo, levemente girado."""
    e = com_contorno(emoji(ch, tam), borda * S)
    if giro:
        e = e.rotate(giro, resample=Image.BICUBIC, expand=True)
    return e


# ---------------------------------------------------------------- carros (desenho próprio, genérico)
# Unidades: x de 0 (traseira) a 100 (frente, à direita); y para cima, chão em 0.
# Pontos do corpo: (x, y, raio do canto). Nada de grade, logo, emblema ou placa.
TIPOS = {
    "hatch": dict(
        corpo=[(3, 6, 3), (1, 23, 4), (5, 33, 8), (15, 46, 10), (52, 47.5, 10), (68, 32, 6),
               (94, 27.5, 9), (100, 18, 6), (99, 6, 3)],
        vidros=[[(10.5, 32.5, 2), (17.5, 43.3, 3), (34.5, 43.8, 1.5), (34.5, 32.5, 1)],
                [(38.5, 32.5, 1), (38.5, 44, 1.5), (50.5, 44.2, 3), (63.5, 32.5, 2)]],
        rodas=[(22, 10.5), (78, 10.5)], r_roda=10.5, folga=2.8,
        portas=[(37, 9, 31.5), (66, 9, 31.5)], macaneta=(41.5, 27.5),
        farol=(96.2, 21.5), lanterna=(1.6, 21), sombra_y=11.5, friso_y=30.5, topo=48,
    ),
    "suv": dict(
        corpo=[(2.5, 9, 3), (1, 40, 5), (5, 52, 8), (64, 53.5, 9), (77, 37, 6), (97, 33, 9),
               (100, 22, 6), (99, 9, 3)],
        vidros=[[(7.5, 38.5, 2), (9.5, 49.5, 3), (26, 49.8, 1.5), (26, 38.5, 1)],
                [(30, 38.5, 1), (30, 50, 1.5), (49, 50.2, 1.5), (49, 38.5, 1)],
                [(53, 38.5, 1), (53, 50.2, 1.5), (61.5, 50.4, 3), (72.5, 38.5, 2)]],
        rodas=[(21, 12.5), (79, 12.5)], r_roda=12.5, folga=3.0,
        portas=[(28, 11, 37), (51, 11, 37), (75, 11, 36)], macaneta=(33, 33),
        farol=(96.5, 27), lanterna=(1.6, 34), sombra_y=14, friso_y=36.5, topo=56,
        rack=(10, 58),
    ),
    "rebaixado": dict(
        corpo=[(3, 3.2, 2), (1, 19, 4), (5, 28, 8), (15, 40, 10), (52, 41.5, 10), (68, 27, 6),
               (94, 23, 9), (100, 14, 5), (99, 3.2, 2)],
        vidros=[[(10.5, 27.5, 2), (17.5, 37.5, 3), (34.5, 38, 1.5), (34.5, 27.5, 1)],
                [(38.5, 27.5, 1), (38.5, 38.2, 1.5), (50.5, 38.4, 3), (63.5, 27.5, 2)]],
        rodas=[(22, 8.0), (78, 8.0)], r_roda=8.0, folga=1.5,
        portas=[(37, 5, 26.5), (66, 5, 26.5)], macaneta=(41.5, 23),
        farol=(96.2, 17), lanterna=(1.6, 16.5), sombra_y=7.5, friso_y=25.5, topo=42,
    ),
    "antigo": dict(  # sedã de 3 volumes, genérico (sem silhueta de modelo famoso)
        corpo=[(1.5, 9, 3), (0, 23, 3), (4, 28, 3), (25, 30, 3), (32, 45, 7), (60, 46, 7), (70, 31, 4),
               (95, 28.5, 5), (100, 20, 4), (99, 9, 3)],
        vidros=[[(28.5, 31.5, 1.5), (34, 42.3, 3), (45, 42.6, 1.5), (45, 31.5, 1)],
                [(48.5, 31.5, 1), (48.5, 42.8, 1.5), (58, 43, 3), (66.5, 31.5, 1.5)]],
        rodas=[(20, 10), (80, 10)], r_roda=10, folga=3.2,
        portas=[(47, 9, 31), (68.5, 9, 30.5)], macaneta=(51, 27),
        farol=(97, 23), lanterna=(1.2, 20), sombra_y=12, friso_y=25, topo=47,
        cromado=True,
    ),
    "picape": dict(  # caminhonete com caçamba, genérica
        corpo=[(1.5, 11, 3), (0, 34, 2.5), (41, 34, 1), (42.5, 50, 5), (64, 51.5, 7), (77, 36, 5),
               (97, 32.5, 8), (100, 22, 5), (99, 11, 3)],
        vidros=[[(46, 36.5, 1), (46.3, 47.5, 2), (62.5, 48, 3), (73, 36.5, 2)]],
        rodas=[(19, 12.5), (80, 12.5)], r_roda=12.5, folga=3.2,
        portas=[(44, 11, 34), (75.5, 11, 34)], macaneta=(49, 31),
        farol=(96.5, 27), lanterna=(1.3, 29), sombra_y=14, friso_y=33, topo=53,
        cacamba=(2.5, 39.5, 33.5),
    ),
}

VIDRO_TOP, VIDRO_BOT = "#E4FAFF", "#8FD4EA"


def carro(tipo, cor, larg, porta_cor=None, lama=False, chapeu=False, ferrugem=False,
          capa=False, brilho_extra=False, traco=None):
    """Carro genérico de lado (frente para a direita), parado. larg = largura em px (já em escala S)."""
    t = TIPOS[tipo]
    k = larg / 104.0
    topo = t["topo"] + (13 if chapeu else 0) + (3 if t.get("rack") else 0)
    Wc, Hc = int(106 * k), int((topo + 3) * k)
    ox, oy = 3 * k, Hc - 1.5 * k
    P = lambda x, y: (ox + x * k, oy - y * k)  # noqa: E731
    size = (Wc, Hc)
    im = Image.new("RGBA", size, (0, 0, 0, 0))
    lw = max(2, int(1.25 * k))       # traço interno
    out_w = traco if traco else max(3, 1.9 * k)  # contorno externo

    corpo_pts = [P(x, y) for x, y in caminho_arred(t["corpo"])]
    mb = Image.new("L", size, 0)
    ImageDraw.Draw(mb).polygon(corpo_pts, fill=255)
    r = t["r_roda"]

    if capa:
        # carro coberto por uma capa: silhueta inflada, barra ondulada, só as rodas aparecem embaixo
        mb2 = mb.filter(ImageFilter.GaussianBlur(2.2 * k)).point(lambda v: 255 if v > 40 else 0)
        mb2 = mb2.filter(ImageFilter.GaussianBlur(0.6 * k)).point(lambda v: 255 if v > 128 else 0)
        corte = Image.new("L", size, 0)
        dc = ImageDraw.Draw(corte)
        pts = [P(-3, 9)]
        for i in range(0, 41):
            x = -3 + 106 * i / 40
            pts.append(P(x, 8.0 + 1.4 * math.sin(i * 1.15)))
        pts += [P(103, -5), P(-3, -5)]
        dc.polygon(pts, fill=255)
        mb2 = menos(mb2, corte)
        d = ImageDraw.Draw(im)
        for (x, _) in t["rodas"]:  # pneus por baixo da capa
            cx, cy = P(x, r)
            d.ellipse([cx - r * k, cy - r * k, cx + r * k, cy + r * k], fill=rgb("#2A2C33"))
        capa_img = gradiente(Wc, Hc, [(0, clarear(cor, 0.25)), (1, escurecer(cor, 0.12))], (0.2, 0.8))
        im.alpha_composite(recortar(capa_img, mb2))
        dobra = Image.new("RGBA", size, (0, 0, 0, 0))
        dd = ImageDraw.Draw(dobra)
        for (x0, x1, y0) in ((30, 36, 44), (55, 50, 45), (78, 84, 31)):
            dd.line(bezier(P(x0, y0), P(x0 + 1, y0 - 12), P(x1 - 3, 22), P(x1, 10)), fill=escurecer(cor, 0.30),
                    width=lw, joint="curve")
        im.alpha_composite(recortar(dobra, mb2))
        brilho = Image.new("L", size, 0)
        ImageDraw.Draw(brilho).ellipse([P(18, 51)[0], P(18, 51)[1], P(56, 40)[0], P(56, 40)[1]], fill=110)
        brilho = brilho.filter(ImageFilter.GaussianBlur(2.5 * k))
        im.alpha_composite(camada_cor(size, "#FFFFFF", interseccao(brilho, mb2)))
        return com_contorno(aparar(im), out_w, GRAFITE)

    # corpo
    im.alpha_composite(camada_cor(size, cor, mb))
    if porta_cor:
        x0p, x1p = t["portas"][0][0], t["portas"][1][0]
        mp = Image.new("L", size, 0)
        ImageDraw.Draw(mp).rectangle([P(x0p, 0)[0], 0, P(x1p, 0)[0], Hc], fill=255)
        im.alpha_composite(camada_cor(size, porta_cor, interseccao(mp, mb)))
    # parte de baixo mais escura
    ms = Image.new("L", size, 0)
    ImageDraw.Draw(ms).rectangle([0, P(0, t["sombra_y"])[1], Wc, Hc], fill=255)
    im.alpha_composite(camada_cor(size, "#000000", interseccao(ms, mb), 0.20))
    # brilho de pintura no teto
    br = Image.new("L", size, 0)
    ImageDraw.Draw(br).rectangle([0, 0, Wc, P(0, t["friso_y"] + 2)[1]], fill=60)
    br = br.filter(ImageFilter.GaussianBlur(2 * k))
    im.alpha_composite(camada_cor(size, "#FFFFFF", interseccao(br, mb)))
    if t.get("cacamba"):
        x0c, x1c, yc = t["cacamba"]
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([P(x0c, yc)[0], P(x0c, yc)[1], P(x1c, yc - 3.2)[0], P(x1c, yc - 3.2)[1]],
                            radius=1.2 * k, fill=escurecer(cor, 0.45))
    # caixas de roda (escuras), recortadas pelo corpo
    ma = Image.new("L", size, 0)
    da = ImageDraw.Draw(ma)
    for (x, _) in t["rodas"]:
        cx, cy = P(x, r)
        rr = (r + t["folga"]) * k
        da.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=255)
    im.alpha_composite(camada_cor(size, "#16181D", interseccao(ma, mb)))
    if ferrugem:
        mf = Image.new("L", size, 0)
        df = ImageDraw.Draw(mf)
        for (fx, fy, fr) in ((t["rodas"][0][0] + 9, 13.5, 2.6), (t["rodas"][0][0] + 12.5, 11.5, 1.6),
                             (t["rodas"][1][0] - 10, 14, 1.9)):
            cx, cy = P(fx, fy)
            df.ellipse([cx - fr * k, cy - fr * k * 0.8, cx + fr * k, cy + fr * k * 0.8], fill=255)
        im.alpha_composite(camada_cor(size, "#B4682E", interseccao(mf, mb, menos(mb, ma))))
    if lama:
        ml = Image.new("L", size, 0)
        dl = ImageDraw.Draw(ml)
        rnd = random.Random(7)
        for _ in range(26):
            fx, fy, fr = rnd.uniform(2, 98), rnd.uniform(4, 15), rnd.uniform(0.9, 2.6)
            cx, cy = P(fx, fy)
            dl.ellipse([cx - fr * k, cy - fr * k, cx + fr * k, cy + fr * k], fill=255)
        dl.rectangle([0, P(0, 8.5)[1], Wc, Hc], fill=255)
        im.alpha_composite(camada_cor(size, "#8A5A2B", interseccao(ml, mb, menos(mb, ma)), 0.92))
    d = ImageDraw.Draw(im)
    # friso (linha de luz na lateral)
    x_ini, x_fim = 4, 95
    d.line([P(x_ini, t["friso_y"]), P(x_fim, t["friso_y"] - 2.5)], fill=clarear(cor, 0.45), width=max(1, int(0.8 * k)))
    # vidros
    for v in t["vidros"]:
        pts = [P(x, y) for x, y in caminho_arred(v, 8)]
        mv = Image.new("L", size, 0)
        ImageDraw.Draw(mv).polygon(pts, fill=255)
        g = gradiente(Wc, Hc, [(0, VIDRO_TOP), (1, VIDRO_BOT)], (0.0, 1.0))
        im.alpha_composite(recortar(g, mv))
        # reflexo diagonal
        rf = Image.new("L", size, 0)
        x0v = min(p[0] for p in pts)
        x1v = max(p[0] for p in pts)
        y0v = min(p[1] for p in pts)
        y1v = max(p[1] for p in pts)
        cxv = x0v + (x1v - x0v) * 0.55
        ImageDraw.Draw(rf).polygon([(cxv - 1.5 * k, y1v), (cxv + 2.5 * k, y1v), (cxv + 8.5 * k, y0v), (cxv + 4.5 * k, y0v)],
                                   fill=200)
        im.alpha_composite(camada_cor(size, "#FFFFFF", interseccao(rf, mv), 0.85))
        d = ImageDraw.Draw(im)
        d.line(pts + [pts[0]], fill=rgb(GRAFITE), width=lw, joint="curve")
    if t.get("rack"):
        y_r, (x0r, x1r) = max(y for _, y, _ in t["corpo"]) + 1.6, t["rack"]
        for xp in (x0r + 3, x1r - 3):
            d.rectangle([P(xp - 1, y_r)[0], P(xp - 1, y_r)[1], P(xp + 1, y_r - 2.5)[0], P(xp + 1, y_r - 2.5)[1]],
                        fill=rgb(GRAFITE))
        d.rounded_rectangle([P(x0r, y_r + 2.2)[0], P(x0r, y_r + 2.2)[1], P(x1r, y_r)[0], P(x1r, y_r)[1]],
                            radius=1 * k, fill=rgb(GRAFITE))
    # portas e maçaneta
    for (x, y0, y1) in t["portas"]:
        lay = Image.new("RGBA", size, (0, 0, 0, 0))
        ImageDraw.Draw(lay).line([P(x, y0), P(x, y1)], fill=escurecer(cor, 0.55), width=lw)
        im.alpha_composite(recortar(lay, menos(mb, ma)))
    d = ImageDraw.Draw(im)
    mx, my = t["macaneta"]
    d.rounded_rectangle([P(mx, my + 1)[0], P(mx, my + 1)[1], P(mx + 5, my - 0.6)[0], P(mx + 5, my - 0.6)[1]],
                        radius=0.8 * k, fill=escurecer(cor, 0.45))
    # farol e lanterna (redondos/genéricos)
    fx, fy = t["farol"]
    cx, cy = P(fx, fy)
    d.ellipse([cx - 2.6 * k, cy - 2.2 * k, cx + 2.6 * k, cy + 2.2 * k], fill=rgb("#FFF4B8"), outline=rgb(GRAFITE),
              width=max(1, int(0.8 * k)))
    lx, ly = t["lanterna"]
    cx, cy = P(lx, ly)
    d.rounded_rectangle([cx - 1.6 * k, cy - 3.2 * k, cx + 1.6 * k, cy + 3.2 * k], radius=1.2 * k, fill=rgb("#FF5D4A"))
    if t.get("cromado"):
        for (x0b, x1b) in ((-1.5, 9), (91, 101.5)):
            d.rounded_rectangle([P(x0b, 12.5)[0], P(x0b, 12.5)[1], P(x1b, 8.5)[0], P(x1b, 8.5)[1]], radius=2 * k,
                                fill=rgb("#E9EDF2"), outline=rgb(GRAFITE), width=max(1, int(0.8 * k)))
    # rodas
    for (x, _) in t["rodas"]:
        cx, cy = P(x, r)
        rr = r * k
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=rgb("#2A2C33"))
        aro = rr * (0.58 if not t.get("cromado") else 0.66)
        if t.get("cromado"):  # faixa branca de pneu antigo
            d.ellipse([cx - aro, cy - aro, cx + aro, cy + aro], fill=rgb("#F4F4F2"))
            aro *= 0.74
        d.ellipse([cx - aro, cy - aro, cx + aro, cy + aro], fill=rgb("#D8DEE6"))
        d.ellipse([cx - aro * 0.78, cy - aro * 0.78, cx + aro * 0.78, cy + aro * 0.78], fill=rgb("#AEB7C3"))
        d.ellipse([cx - aro * 0.34, cy - aro * 0.34, cx + aro * 0.34, cy + aro * 0.34], fill=rgb("#E9EDF2"))
        d.arc([cx - rr * 0.86, cy - rr * 0.86, cx + rr * 0.86, cy + rr * 0.86], 200, 250, fill=rgb("#5A5E68"),
              width=max(1, int(0.9 * k)))
    if chapeu:  # chapéu de aba larga em cima da cabine (caminhonete do agro)
        topo_cab = max(y for _, y, _ in t["corpo"])
        xc = 54
        cx, cy = P(xc, topo_cab + 0.8)
        d.ellipse([cx - 15 * k, cy - 3.2 * k, cx + 15 * k, cy + 2.2 * k], fill=rgb("#B5793C"),
                  outline=rgb(GRAFITE), width=lw)
        copa = caminho_arred([(xc - 8.5, topo_cab + 1.5, 2), (xc - 7, topo_cab + 11.5, 4), (xc, topo_cab + 9.5, 2),
                              (xc + 7, topo_cab + 11.5, 4), (xc + 8.5, topo_cab + 1.5, 2)], 8)
        d.polygon([P(x, y) for x, y in copa], fill=rgb("#C98A47"), outline=rgb(GRAFITE), width=lw)
        d.rectangle([P(xc - 8.3, topo_cab + 4.6)[0], P(xc - 8.3, topo_cab + 4.6)[1],
                     P(xc + 8.3, topo_cab + 2.4)[0], P(xc + 8.3, topo_cab + 2.4)[1]], fill=rgb("#6B4220"))
    if brilho_extra:
        for (x, y, rr) in ((30, 40, 2.6), (84, 27, 2.0)):
            cx, cy = P(x, y)
            estrela4(d, cx, cy, rr * k, "#FFFFFF")
    return com_contorno(aparar(im), out_w, GRAFITE)


# ---------------------------------------------------------------- outros desenhos próprios
def moeda_interrogacao(diam, cor="#FFD43B", cor_txt=GRAFITE, borda=None):
    """Círculo com '?' (é a 'régua' do título: tem que ficar redondo)."""
    t = int(diam)
    im = Image.new("RGBA", (t, t), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    b = borda if borda else max(2, int(t * 0.07))
    d.ellipse([0, 0, t - 1, t - 1], fill=rgb(GRAFITE))
    d.ellipse([b, b, t - 1 - b, t - 1 - b], fill=rgb(cor))
    # luz
    gl = Image.new("L", (t, t), 0)
    ImageDraw.Draw(gl).ellipse([t * 0.18, t * 0.12, t * 0.62, t * 0.42], fill=90)
    gl = gl.filter(ImageFilter.GaussianBlur(t * 0.05))
    m = Image.new("L", (t, t), 0)
    ImageDraw.Draw(m).ellipse([b, b, t - 1 - b, t - 1 - b], fill=255)
    im.alpha_composite(camada_cor((t, t), "#FFFFFF", interseccao(gl, m)))
    f = ImageFont.truetype(F_BLACK, int(t * 0.68))
    d.text((t / 2, t / 2 + t * 0.03), "?", font=f, anchor="mm", fill=rgb(cor_txt))
    return im


def chip(texto, alt, cor_txt=AMARELO, fundo=GRAFITE):
    """Etiqueta escura com texto (ex.: hodômetro '300.000')."""
    f = ImageFont.truetype(F_BLACK, int(alt * 0.62))
    tmp = ImageDraw.Draw(Image.new("L", (4, 4)))
    w = tmp.textlength(texto, font=f) + alt * 0.62
    b = max(2, int(alt * 0.09))
    im = Image.new("RGBA", (int(w + 2 * b), int(alt + 2 * b)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=int(alt * 0.32), fill=rgb("#FFFFFF"))
    d.rounded_rectangle([b, b, im.width - 1 - b, im.height - 1 - b], radius=int(alt * 0.26), fill=rgb(fundo))
    d.text((im.width / 2, im.height / 2 + alt * 0.03), texto, font=f, anchor="mm", fill=rgb(cor_txt))
    return im


def lombada(larg):
    """Lombada genérica (amarela e grafite)."""
    w, h = int(larg), int(larg * 0.30)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).chord([0, 0, w - 1, 2 * h], 180, 360, fill=255)
    lis = Image.new("RGBA", (w, h), rgb(AMARELO))
    d = ImageDraw.Draw(lis)
    passo = w / 6
    for i in range(-2, 9):
        x = i * passo
        d.polygon([(x, h), (x + passo / 2, h), (x + passo / 2 + h * 0.6, 0), (x + h * 0.6, 0)], fill=rgb(GRAFITE))
    im.alpha_composite(recortar(lis, m))
    return com_contorno(im, max(2, larg * 0.025), GRAFITE)


def faiscas(d, cx, cy, esc):
    for (dx, dy, r, c) in ((0, 0, 7, "#FFD43B"), (-11, -6, 4.5, "#FFFFFF"), (10, -8, 5, "#FF9F1C"),
                           (-4, 9, 3.5, "#FFD43B"), (14, 5, 3.5, "#FFFFFF")):
        estrela4(d, cx + dx * esc, cy + dy * esc, r * esc, c)


def vidro_familia(larg, cor):
    """Traseira (só a parte de cima) com vidro e adesivo de bonequinhos de palito. Sem placa."""
    k = larg / 100.0
    Wc, Hc = int(102 * k), int(60 * k)
    P = lambda x, y: (1 * k + x * k, Hc - 1 * k - y * k)  # noqa: E731
    im = Image.new("RGBA", (Wc, Hc), (0, 0, 0, 0))
    corpo = caminho_arred([(2, 0, 2), (1, 22, 8), (14, 26, 4), (22, 56, 10), (78, 56, 10), (86, 26, 4),
                           (99, 22, 8), (98, 0, 2)])
    mb = Image.new("L", (Wc, Hc), 0)
    ImageDraw.Draw(mb).polygon([P(x, y) for x, y in corpo], fill=255)
    im.alpha_composite(camada_cor((Wc, Hc), cor, mb))
    br = Image.new("L", (Wc, Hc), 0)
    ImageDraw.Draw(br).rectangle([0, 0, Wc, P(0, 40)[1]], fill=70)
    br = br.filter(ImageFilter.GaussianBlur(3 * k))
    im.alpha_composite(camada_cor((Wc, Hc), "#FFFFFF", interseccao(br, mb)))
    d = ImageDraw.Draw(im)
    # lanternas
    for x0 in (4, 84):
        d.rounded_rectangle([P(x0, 18)[0], P(x0, 18)[1], P(x0 + 12, 6)[0], P(x0 + 12, 6)[1]], radius=2.5 * k,
                            fill=rgb("#FF5D4A"), outline=rgb(GRAFITE), width=max(1, int(1.0 * k)))
        d.rounded_rectangle([P(x0 + 2, 16)[0], P(x0 + 2, 16)[1], P(x0 + 6, 12)[0], P(x0 + 6, 12)[1]], radius=1 * k,
                            fill=rgb("#FFB3A8"))
    # vidro
    vid = caminho_arred([(17, 24, 3), (24.5, 52, 6), (75.5, 52, 6), (83, 24, 3)], 8)
    pts = [P(x, y) for x, y in vid]
    mv = Image.new("L", (Wc, Hc), 0)
    ImageDraw.Draw(mv).polygon(pts, fill=255)
    im.alpha_composite(recortar(gradiente(Wc, Hc, [(0, "#4C6075"), (1, "#2C3846")], (0.2, 0.8)), mv))
    rf = Image.new("L", (Wc, Hc), 0)
    ImageDraw.Draw(rf).polygon([P(60, 24), P(66, 24), P(76, 52), P(70, 52)], fill=60)
    im.alpha_composite(camada_cor((Wc, Hc), "#FFFFFF", interseccao(rf, mv)))
    d = ImageDraw.Draw(im)
    d.line(pts + [pts[0]], fill=rgb(GRAFITE), width=max(2, int(1.3 * k)), joint="curve")
    # bonequinhos (pai, mãe, filho, cachorro), traço branco
    lw = max(2, int(1.9 * k))
    B = rgb("#FFFFFF")

    def pessoa(x, base, alt, vestido=False):
        cab = alt * 0.17
        cx, cy = P(x, base + alt - cab)
        d.ellipse([cx - cab * k, cy - cab * k, cx + cab * k, cy + cab * k], fill=B)
        pesc = base + alt - 2 * cab
        quad = base + alt * 0.42
        if vestido:
            d.polygon([P(x, pesc), P(x - alt * 0.2, quad - alt * 0.04), P(x + alt * 0.2, quad - alt * 0.04)], fill=B)
        else:
            d.line([P(x, pesc), P(x, quad)], fill=B, width=lw)
        d.line([P(x, quad), P(x - alt * 0.13, base)], fill=B, width=lw)
        d.line([P(x, quad), P(x + alt * 0.13, base)], fill=B, width=lw)
        ombro = pesc - alt * 0.08
        d.line([P(x - alt * 0.22, ombro - alt * 0.16), P(x, ombro), P(x + alt * 0.22, ombro - alt * 0.16)], fill=B,
               width=lw, joint="curve")

    pessoa(31, 28, 21)
    pessoa(43, 28, 19, vestido=True)
    pessoa(54, 28, 13)
    # cachorro
    d.line([P(62, 34), P(71, 34)], fill=B, width=lw)
    for x in (63, 70):
        d.line([P(x, 34), P(x, 28.5)], fill=B, width=lw)
    cx, cy = P(72.5, 37)
    d.ellipse([cx - 2.6 * k, cy - 2.4 * k, cx + 2.6 * k, cy + 2.4 * k], fill=B)
    d.line([P(62, 34), P(60, 38)], fill=B, width=lw)
    return com_contorno(aparar(im), max(3, 1.9 * k), GRAFITE)


def painel(larg):
    """Painel genérico com a luz da injeção (amarela) acesa."""
    w, h = int(larg), int(larg * 0.46)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=int(h * 0.30), fill=rgb("#4A505C"))
    b = int(h * 0.07)
    d.rounded_rectangle([b, b, w - 1 - b, h - 1 - b], radius=int(h * 0.25), fill=rgb("#1C1F25"))
    # mostrador
    c = (h * 0.52, h * 0.52)
    r = h * 0.33
    d.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], outline=rgb("#E9EDF2"), width=max(2, int(h * 0.035)))
    for i in range(7):
        a = math.radians(150 + 240 * i / 6)
        d.line([(c[0] + r * 0.72 * math.cos(a), c[1] + r * 0.72 * math.sin(a)),
                (c[0] + r * 0.88 * math.cos(a), c[1] + r * 0.88 * math.sin(a))], fill=rgb("#E9EDF2"),
               width=max(2, int(h * 0.03)))
    a = math.radians(165)
    d.line([c, (c[0] + r * 0.78 * math.cos(a), c[1] + r * 0.78 * math.sin(a))], fill=rgb("#FF7A52"),
           width=max(2, int(h * 0.05)))
    d.ellipse([c[0] - h * 0.05, c[1] - h * 0.05, c[0] + h * 0.05, c[1] + h * 0.05], fill=rgb("#E9EDF2"))
    # luz do motor (símbolo genérico de motor, em contorno) com brilho
    ex, ey, es = w * 0.66, h * 0.53, h * 0.046
    motor = [(-5, -3), (-3, -3), (-3, -5), (-1.2, -5), (-1.2, -6.6), (1.8, -6.6), (1.8, -5), (3.8, -5),
             (5.2, -3), (6.2, -3), (6.2, -1.2), (8.6, -3.2), (8.6, 4.6), (6.2, 2.6), (6.2, 4.8), (-2.8, 4.8),
             (-5, 2.6)]
    pts = [(ex + x * es, ey + y * es) for x, y in motor]
    glow = Image.new("L", (w, h), 0)
    ImageDraw.Draw(glow).ellipse([ex - 13 * es, ey - 12 * es, ex + 14 * es, ey + 12 * es], fill=200)
    glow = glow.filter(ImageFilter.GaussianBlur(h * 0.09))
    im.alpha_composite(camada_cor((w, h), "#FFB020", glow, 0.70))
    d = ImageDraw.Draw(im)
    lwm = max(3, int(es * 1.25))
    d.line(pts + [pts[0]], fill=rgb("#FFC21A"), width=lwm, joint="curve")
    # polia e ventoinha do lado esquerdo
    d.line([(ex - 5 * es, ey - 0.2 * es), (ex - 7.6 * es, ey - 0.2 * es)], fill=rgb("#FFC21A"), width=lwm)
    d.line([(ex - 7.6 * es, ey - 2.8 * es), (ex - 7.6 * es, ey + 2.6 * es)], fill=rgb("#FFC21A"), width=lwm)
    # luzinhas apagadas
    for i, xx in enumerate((0.86, 0.92)):
        d.ellipse([w * xx - h * 0.035, h * 0.30 - h * 0.035, w * xx + h * 0.035, h * 0.30 + h * 0.035],
                  fill=rgb("#3A3F49"))
    return com_contorno(im, max(3, h * 0.05), GRAFITE)


def chave_carro(larg):
    """Chave de carro genérica (sem logo): controle escuro + lâmina."""
    w, h = int(larg), int(larg * 0.42)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # argola
    rr = h * 0.22
    d.ellipse([w * 0.02, h * 0.5 - rr, w * 0.02 + 2 * rr, h * 0.5 + rr], outline=rgb("#C8CFD8"),
              width=max(3, int(h * 0.08)))
    # lâmina
    x0, x1 = w * 0.50, w * 0.98
    yb0, yb1 = h * 0.40, h * 0.62
    lam = [(x0, yb0), (x1 - h * 0.08, yb0), (x1, yb0 + h * 0.06), (x1, yb1)]
    dentes = []
    n = 5
    for i in range(n + 1):
        xx = x1 - (x1 - x0) * i / n
        dentes.append((xx, yb1 + (h * 0.07 if i % 2 else 0)))
    d.polygon(lam + dentes, fill=rgb("#D5DBE3"), outline=rgb("#7E8794"))
    d.line([(x0 + h * 0.05, (yb0 + yb1) / 2), (x1 - h * 0.12, (yb0 + yb1) / 2)], fill=rgb("#9AA3AF"),
           width=max(1, int(h * 0.03)))
    # controle
    d.rounded_rectangle([w * 0.13, h * 0.12, w * 0.56, h * 0.88], radius=int(h * 0.30), fill=rgb("#2E323B"))
    gl = Image.new("L", (w, h), 0)
    ImageDraw.Draw(gl).rounded_rectangle([w * 0.16, h * 0.16, w * 0.53, h * 0.40], radius=int(h * 0.15), fill=70)
    im.alpha_composite(camada_cor((w, h), "#FFFFFF", gl.filter(ImageFilter.GaussianBlur(h * 0.03))))
    d = ImageDraw.Draw(im)
    for i, cxx in enumerate((0.26, 0.42)):
        cx, cy = w * cxx, h * 0.5
        rb = h * 0.12
        d.ellipse([cx - rb, cy - rb, cx + rb, cy + rb], fill=rgb("#5A606C"))
        d.ellipse([cx - rb * 0.55, cy - rb * 0.55, cx + rb * 0.55, cy + rb * 0.55], fill=rgb("#7B8290"))
    return com_contorno(aparar(im), max(3, h * 0.06), GRAFITE)


def caixa_som(alt):
    """Caixa de som genérica (sem marca) com dois alto-falantes."""
    h = int(alt)
    w = int(alt * 1.45)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=int(h * 0.12), fill=rgb("#3A3E48"))
    d.rounded_rectangle([h * 0.05, h * 0.05, w - 1 - h * 0.05, h - 1 - h * 0.05], radius=int(h * 0.09),
                        fill=rgb("#2A2D34"))
    for cx in (w * 0.29, w * 0.71):
        cy = h * 0.52
        r = h * 0.34
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=rgb("#B9C1CC"))
        d.ellipse([cx - r * 0.86, cy - r * 0.86, cx + r * 0.86, cy + r * 0.86], fill=rgb("#16181C"))
        g = Image.new("RGBA", (int(2 * r), int(2 * r)), (0, 0, 0, 0))
        gg = gradiente(int(2 * r), int(2 * r), [(0, "#6A707C"), (1, "#24272E")], (0.5, 0.5))
        mm = Image.new("L", g.size, 0)
        ImageDraw.Draw(mm).ellipse([r * 0.30, r * 0.30, r * 1.70, r * 1.70], fill=255)
        im.alpha_composite(recortar(gg, mm), (int(cx - r), int(cy - r)))
        d = ImageDraw.Draw(im)
        d.ellipse([cx - r * 0.26, cy - r * 0.26, cx + r * 0.26, cy + r * 0.26], fill=rgb("#C9D0DA"))
        d.ellipse([cx - r * 0.12, cy - r * 0.18, cx + r * 0.02, cy - r * 0.06], fill=rgb("#FFFFFF"))
    for (sx, sy) in ((0.06, 0.08), (0.94, 0.08), (0.06, 0.92), (0.94, 0.92)):
        d.ellipse([w * sx - h * 0.025, h * sy - h * 0.025, w * sx + h * 0.025, h * sy + h * 0.025], fill=rgb("#8A919C"))
    return com_contorno(im, max(3, h * 0.045), GRAFITE)


def bolhas(larg, seed=3):
    """Bolhas de sabão desenhadas."""
    w, h = int(larg), int(larg * 0.75)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for (x, y, r) in ((0.25, 0.62, 0.20), (0.62, 0.35, 0.24), (0.80, 0.78, 0.13), (0.10, 0.22, 0.10)):
        cx, cy, rr = x * w, y * h, r * w
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(200, 245, 255, 150), outline=rgb("#FFFFFF"),
                  width=max(2, int(w * 0.022)))
        d.arc([cx - rr * 0.70, cy - rr * 0.70, cx + rr * 0.70, cy + rr * 0.70], 200, 260, fill=rgb("#FFFFFF"),
              width=max(2, int(w * 0.03)))
        d.ellipse([cx + rr * 0.25, cy + rr * 0.25, cx + rr * 0.45, cy + rr * 0.45], fill=(255, 255, 255, 200))
    return com_contorno(im, max(2, w * 0.018), "#2F8FB0")


def ondas_sensor(alt):
    """Arcos de sensor de ré (verde, amarelo, coral), atrás do carro."""
    h = int(alt)
    w = int(alt * 0.62)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, cor in enumerate(("#3DDC84", "#FFD43B", "#FF6F47")):
        r = h * (0.22 + 0.15 * i)
        cx, cy = w * 1.05, h * 0.5
        d.arc([cx - r, cy - r, cx + r, cy + r], 140, 220, fill=rgb(cor), width=max(3, int(h * 0.075)))
    return com_contorno(aparar(im), max(2, h * 0.04), GRAFITE)


def gota_aromatizante(alt, cor="#FF8FB1"):
    """Aromatizante em forma de GOTA (nada de pinheirinho), pendurado por um cordão."""
    h = int(alt)
    w = int(alt * 0.55)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx = w / 2
    # cordão
    d.line([(cx, 0), (cx, h * 0.30)], fill=rgb("#F2E2BE"), width=max(2, int(h * 0.035)))
    d.line([(cx, 0), (cx, h * 0.30)], fill=rgb(GRAFITE), width=max(1, int(h * 0.012)))
    # gota
    r = w * 0.40
    cy = h - r - h * 0.02
    topo = (cx, h * 0.26)
    m = Image.new("L", (w, h), 0)
    dm = ImageDraw.Draw(m)
    dm.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    a = math.asin(min(0.999, r / (cy - topo[1])))
    tx = r * math.cos(a)
    ty = r * math.sin(a)
    dm.polygon([topo, (cx - tx, cy - ty), (cx + tx, cy - ty)], fill=255)
    g = gradiente(w, h, [(0, clarear(cor, 0.35)), (1, escurecer(cor, 0.10))], (0.3, 0.7))
    im.alpha_composite(recortar(g, m))
    gl = Image.new("L", (w, h), 0)
    ImageDraw.Draw(gl).ellipse([cx - r * 0.65, cy - r * 0.75, cx - r * 0.15, cy - r * 0.05], fill=150)
    im.alpha_composite(camada_cor((w, h), "#FFFFFF", interseccao(gl.filter(ImageFilter.GaussianBlur(w * 0.03)), m)))
    d = ImageDraw.Draw(im)
    d.ellipse([cx - w * 0.06, h * 0.28, cx + w * 0.06, h * 0.28 + w * 0.12], outline=rgb(GRAFITE),
              width=max(1, int(h * 0.02)))
    return com_contorno(im, max(2, h * 0.035), GRAFITE)


def tapete(alt):
    """Tapete de carro genérico visto de cima: borracha com pinos e apoio de calcanhar."""
    h = int(alt)
    w = int(alt * 0.80)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # contorno típico de tapete: topo inclinado e um lado mais curvo
    fora = caminho_arred([(0, h * 0.16, w * 0.14), (w, 0, w * 0.14), (w * 0.96, h, w * 0.18), (w * 0.04, h, w * 0.18)])
    d.polygon(fora, fill=rgb("#3D424C"))
    m = w * 0.10
    dentro = caminho_arred([(m, h * 0.16 + m * 0.6, w * 0.08), (w - m, m * 0.9, w * 0.08),
                            (w * 0.96 - m, h - m, w * 0.10), (w * 0.04 + m, h - m, w * 0.10)])
    d.polygon(dentro, fill=rgb("#262930"))
    # pinos de borracha
    rp = w * 0.035
    for iy in range(5):
        for ix in range(5):
            x = w * (0.24 + 0.13 * ix)
            y = h * (0.30 + 0.095 * iy) - (x / w) * h * 0.08
            d.ellipse([x - rp, y - rp, x + rp, y + rp], fill=rgb("#5E6572"))
    # apoio de calcanhar (frisos curtos embaixo)
    d.rounded_rectangle([w * 0.24, h * 0.76, w * 0.76, h * 0.88], radius=w * 0.04, fill=rgb("#4A505C"))
    for i in range(6):
        x = w * (0.29 + 0.085 * i)
        d.line([(x, h * 0.78), (x, h * 0.86)], fill=rgb("#262930"), width=max(2, int(w * 0.025)))
    return com_contorno(im, max(2, h * 0.04), GRAFITE)


def tapete_chao(larg):
    """Tapetinho de borracha deitado no chão (em perspectiva), com frisos e borda clara."""
    w = int(larg)
    h = int(larg * 0.36)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    fora = caminho_arred([(w * 0.16, 0, h * 0.18), (w * 0.84, 0, h * 0.18), (w, h, h * 0.22), (0, h, h * 0.22)])
    d.polygon(fora, fill=rgb("#6A717E"))
    dentro = caminho_arred([(w * 0.21, h * 0.16, h * 0.12), (w * 0.79, h * 0.16, h * 0.12), (w * 0.91, h * 0.84, h * 0.14),
                            (w * 0.09, h * 0.84, h * 0.14)])
    d.polygon(dentro, fill=rgb("#30343C"))
    for i in range(4):
        f = (i + 1) / 5
        y = h * (0.16 + 0.68 * f)
        xa = w * (0.21 - 0.12 * f) + w * 0.05
        xb = w * (0.79 + 0.12 * f) - w * 0.05
        d.line([(xa, y), (xb, y)], fill=rgb("#5A606C"), width=max(2, int(h * 0.07)))
    return com_contorno(im, max(2, h * 0.07), GRAFITE)


def manivela(alt):
    """Manivela de vidro (base redonda + braço + pegador)."""
    h = int(alt)
    w = int(alt * 1.1)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    bx, by, br_ = w * 0.28, h * 0.62, h * 0.22
    d.line([(bx, by), (w * 0.80, h * 0.30)], fill=rgb("#C8CFD8"), width=int(h * 0.14))
    d.ellipse([bx - br_, by - br_, bx + br_, by + br_], fill=rgb("#AEB7C3"))
    d.ellipse([bx - br_ * 0.5, by - br_ * 0.5, bx + br_ * 0.5, by + br_ * 0.5], fill=rgb("#E9EDF2"))
    px, py = w * 0.80, h * 0.30
    d.rounded_rectangle([px - h * 0.11, py - h * 0.30, px + h * 0.11, py + h * 0.10], radius=int(h * 0.10),
                        fill=rgb("#2E323B"))
    d.ellipse([px - h * 0.06, py - h * 0.24, px - h * 0.01, py - h * 0.10], fill=rgb("#6A707C"))
    return com_contorno(aparar(im), max(3, h * 0.05), GRAFITE)


def marcador_combustivel(larg):
    """Marcador de combustível com o ponteiro encostado no vazio."""
    w = int(larg)
    h = int(larg * 0.62)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy, r = w / 2, h * 0.92, w * 0.48
    d.pieslice([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=rgb("#4A505C"))
    r2 = r * 0.90
    d.pieslice([cx - r2, cy - r2, cx + r2, cy + r2], 180, 360, fill=rgb("#1C1F25"))
    d.rectangle([cx - r, cy - h * 0.02, cx + r, cy + h * 0.10], fill=(0, 0, 0, 0))
    # faixa de reserva (coral)
    d.arc([cx - r * 0.78, cy - r * 0.78, cx + r * 0.78, cy + r * 0.78], 182, 212, fill=rgb("#FF6F47"),
          width=int(r * 0.13))
    for i in range(5):
        a = math.radians(185 + 170 * i / 4)
        d.line([(cx + r * 0.55 * math.cos(a), cy + r * 0.55 * math.sin(a)),
                (cx + r * 0.70 * math.cos(a), cy + r * 0.70 * math.sin(a))], fill=rgb("#E9EDF2"),
               width=max(2, int(r * 0.05)))
    f = ImageFont.truetype(F_BLACK, int(r * 0.26))
    d.text((cx - r * 0.36, cy - r * 0.22), "E", font=f, anchor="mm", fill=rgb("#FF8A66"))
    d.text((cx + r * 0.36, cy - r * 0.22), "F", font=f, anchor="mm", fill=rgb("#E9EDF2"))
    a = math.radians(190)
    d.line([(cx, cy - h * 0.02), (cx + r * 0.72 * math.cos(a), cy + r * 0.72 * math.sin(a))], fill=rgb("#FFD43B"),
           width=max(3, int(r * 0.07)))
    d.ellipse([cx - r * 0.10, cy - r * 0.12, cx + r * 0.10, cy + r * 0.08], fill=rgb("#E9EDF2"))
    # bombinha acesa
    gl = Image.new("L", (w, h), 0)
    ImageDraw.Draw(gl).ellipse([cx - r * 0.18, cy - r * 0.62, cx + r * 0.18, cy - r * 0.26], fill=200)
    im.alpha_composite(camada_cor((w, h), "#FFB020", gl.filter(ImageFilter.GaussianBlur(r * 0.06)), 0.8))
    d = ImageDraw.Draw(im)
    bx, by, bs = cx, cy - r * 0.44, r * 0.10
    d.rounded_rectangle([bx - bs * 0.8, by - bs, bx + bs * 0.5, by + bs], radius=bs * 0.2, fill=rgb("#FFC21A"))
    d.line([(bx + bs * 0.5, by - bs * 0.4), (bx + bs * 1.1, by), (bx + bs * 1.1, by + bs * 0.8)], fill=rgb("#FFC21A"),
           width=max(1, int(bs * 0.35)))
    return com_contorno(aparar(im), max(3, w * 0.025), GRAFITE)


def cabo(w, h, pts_rel, larg_linha):
    im = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))
    pts = bezier(*[(x * w, y * h) for x, y in pts_rel])
    d = ImageDraw.Draw(im)
    d.line(pts, fill=rgb(GRAFITE), width=int(larg_linha * 1.8), joint="curve")
    d.line(pts, fill=rgb("#3D414B"), width=int(larg_linha), joint="curve")
    return im


def raios_sol(w, h):
    im = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(w * 0.35, 0), (w * 0.65, 0), (w * 0.95, h), (w * 0.05, h)], fill=(255, 220, 90, 110))
    return im


def ondinhas(alt):
    """Marquinhas de barulho (três tracinhos curvos)."""
    h = int(alt)
    w = int(alt * 0.7)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i in range(3):
        r = h * (0.22 + 0.16 * i)
        d.arc([-r + w * 0.05, h / 2 - r, r + w * 0.05, h / 2 + r], -40, 40, fill=rgb(GRAFITE),
              width=max(3, int(h * 0.09)))
    return aparar(im)


# ---------------------------------------------------------------- cenas (uma por carta)
class Cena:
    """Monta o desenho de cada carta. Coordenadas em 1x (o chão fica em y=100)."""

    def __init__(self):
        self.im = Image.new("RGBA", (360 * S, 150 * S), (0, 0, 0, 0))

    def base(self, img, cx, base_y):
        """Cola com o centro de baixo em (cx, base_y)."""
        self.im.alpha_composite(img, (int(cx * S - img.width / 2), int(base_y * S - img.height)))
        return self

    def centro(self, img, cx, cy):
        colar_centro(self.im, img, cx * S, cy * S)
        return self

    def draw(self):
        return ImageDraw.Draw(self.im)


CX = 180      # centro da cena (1x)
CHAO = 100    # chão da cena (1x)


def cena_01():  # POPULAR 1.0 COM 300 MIL KM
    c = Cena().base(carro("hatch", "#7CCFC6", 150 * S, ferrugem=True), CX, CHAO)
    return c.centro(chip("300.000", 28 * S), CX + 70, CHAO - 60)


def cena_02():  # SUV EM 72 PARCELAS
    c = Cena().base(adesivo("🧾", 48 * S, 14), CX - 80, CHAO - 10)
    c.base(carro("suv", CORAL, 150 * S), CX + 6, CHAO)
    return c.centro(chip("72×", 28 * S), CX + 74, CHAO - 62)


def cena_03():  # REBAIXADO QUE RASPA EM TUDO
    c = Cena().base(carro("rebaixado", LILAS, 162 * S), CX, CHAO - 1)
    c.base(lombada(58 * S), CX, CHAO + 4)
    d = c.draw()
    faiscas(d, (CX - 26) * S, (CHAO - 8) * S, 1.15 * S)
    faiscas(d, (CX + 26) * S, (CHAO - 6) * S, 0.9 * S)
    return c


def cena_04():  # ZERO KM (FINALMENTE)
    c = Cena().base(carro("hatch", TURQUESA, 150 * S, brilho_extra=True), CX, CHAO)
    c.base(adesivo("🎀", 40 * S, -6), CX - 10, CHAO - 50)
    c.centro(adesivo("✨", 30 * S, 0), CX + 86, CHAO - 50)
    return c.centro(adesivo("✨", 22 * S, 0), CX - 88, CHAO - 44)


def cena_05():  # SÓ PEGA NO TRANCO
    c = Cena().base(adesivo("💪", 50 * S, -20), CX - 84, CHAO - 4)
    c.base(carro("hatch", PRATA, 150 * S, ferrugem=True), CX + 12, CHAO)
    return c.centro(adesivo("💦", 26 * S, 0), CX - 112, CHAO - 56)


def cena_06():  # COM ADESIVO DA FAMÍLIA
    return Cena().base(vidro_familia(170 * S, CORAL), CX, CHAO)


def cena_07():  # BICICLETA (POR ENQUANTO)
    c = Cena().base(emoji("🚲", 98 * S), CX - 10, CHAO)
    return c.centro(adesivo("⏳", 36 * S, 12), CX + 62, CHAO - 44)


def cena_08():  # CARRO DE APP COM BALINHA (sem logo, pino ou cores de app)
    c = Cena().base(carro("hatch", PRATA, 150 * S), CX - 6, CHAO)
    c.centro(adesivo("🍬", 34 * S, -18), CX + 78, CHAO - 50)
    return c.centro(adesivo("🍬", 26 * S, 22), CX + 50, CHAO - 62)


def cena_09():  # HERDADO DO VÔ (ZERADINHO)
    c = Cena().base(carro("antigo", CREME, 158 * S, brilho_extra=True), CX + 10, CHAO)
    c.centro(adesivo("👴", 38 * S, -8), CX - 76, CHAO - 46)
    return c.centro(adesivo("✨", 26 * S, 0), CX + 92, CHAO - 50)


def cena_10():  # COM PORTA DE OUTRA COR
    return Cena().base(carro("hatch", TURQUESA, 156 * S, porta_cor=CORAL), CX, CHAO)


def cena_11():  # CAMINHONETE DO AGRO
    c = Cena().base(carro("picape", "#5C6372", 162 * S, lama=True, chapeu=True), CX + 4, CHAO)
    return c.centro(adesivo("🌾", 46 * S, -10), CX - 82, CHAO - 46)


def cena_12():  # QUITADO E NO MEU NOME (documento genérico, sem brasão, sem placa)
    c = Cena().base(emoji("📄", 70 * S), CX - 8, CHAO)
    c.centro(adesivo("✅", 34 * S, 10), CX + 28, CHAO - 12)
    return c.centro(adesivo("🔑", 30 * S, -20), CX - 52, CHAO - 18)


def cena_13():  # O DOS SONHOS (EM MINIATURA)
    c = Cena().base(emoji("🤏", 72 * S), CX + 16, CHAO)
    c.centro(carro("hatch", CARRO_AMARELO, 46 * S, traco=1.4 * S), CX - 26, CHAO - 44)
    c.centro(adesivo("✨", 24 * S, 0), CX - 62, CHAO - 64)
    return c


def cena_14():  # COM LUZ DA INJEÇÃO ACESA
    return Cena().base(painel(150 * S), CX, CHAO)


def cena_15():  # EMPRESTADO DO CUNHADO
    c = Cena().base(chave_carro(140 * S).rotate(10, resample=Image.BICUBIC, expand=True), CX - 18, CHAO)
    return c.centro(adesivo("🤝", 40 * S, 8), CX + 66, CHAO - 44)


def cena_16():  # COM SOM MAIS CARO QUE ELE
    c = Cena().base(caixa_som(72 * S), CX - 52, CHAO)
    c.base(carro("hatch", CARRO_AMARELO, 92 * S), CX + 52, CHAO)
    return c.centro(adesivo("💰", 32 * S, 12), CX + 92, CHAO - 46)


def cena_17():  # AUTOMÁTICO E COM AR GELADO
    c = Cena().base(carro("suv", TURQUESA, 150 * S), CX, CHAO)
    c.centro(adesivo("❄️", 30 * S, 10), CX + 80, CHAO - 56)
    return c.centro(adesivo("❄️", 22 * S, -10), CX + 50, CHAO - 70)


def cena_18():  # MOVIDO A ESPERANÇA (dedos cruzados, não mãos de reza)
    c = Cena().base(emoji("⛽", 70 * S), CX - 20, CHAO)
    return c.centro(adesivo("🤞", 44 * S, 10), CX + 34, CHAO - 26)


def cena_19():  # ESSE MESMO SÓ QUE LAVADO
    c = Cena().base(carro("hatch", LILAS, 150 * S), CX + 6, CHAO)
    c.centro(bolhas(58 * S), CX - 4, CHAO - 56)
    return c.centro(adesivo("🧽", 34 * S, -14), CX - 84, CHAO - 26)


def cena_20():  # CONSÓRCIO QUE NUNCA SAI (calendário sem texto, sem nome de empresa)
    c = Cena().base(emoji("🗓", 70 * S), CX - 10, CHAO)
    return c.centro(adesivo("⏳", 36 * S, 12), CX + 42, CHAO - 20)


def cena_21():  # COM CÂMERA DE RÉ (UFA)
    c = Cena().base(ondas_sensor(56 * S), CX - 92, CHAO - 6)
    c.base(carro("hatch", CORAL, 150 * S), CX + 6, CHAO)
    return c.centro(adesivo("📷", 34 * S, -10), CX - 50, CHAO - 62)


def cena_22():  # COM TETO SOLAR (É UM FURO)
    car = carro("hatch", CARRO_AMARELO, 150 * S)
    c = Cena()
    c.base(car, CX, CHAO)
    raio = raios_sol(44 * S, 40 * S).rotate(38, resample=Image.BICUBIC, expand=True)
    c.centro(raio, CX - 38, CHAO - 62)
    furo = emoji("🕳", 48 * S)
    c.centro(furo.resize((furo.width, int(furo.height * 0.75)), Image.LANCZOS), CX - 12, CHAO - 49)
    return c.centro(adesivo("☀️", 40 * S, 0), CX - 74, CHAO - 66)


def cena_23():  # CARRINHO DE MERCADO (sem nome de loja)
    c = Cena().base(emoji("🛒", 74 * S), CX - 6, CHAO)
    return c.centro(adesivo("🔑", 30 * S, 18), CX + 46, CHAO - 54)


def cena_24():  # USADO COM CHEIRO DE NOVO (aromatizante em GOTA, nunca pinheirinho)
    c = Cena().base(carro("hatch", TURQUESA, 140 * S), CX - 22, CHAO)
    c.base(gota_aromatizante(66 * S), CX + 72, CHAO - 4)
    return c.centro(adesivo("🌸", 26 * S, 0), CX + 92, CHAO - 54)


def cena_25():  # COMPLETINHO (ATÉ O TAPETE)
    c = Cena().base(carro("suv", CORAL, 140 * S), CX - 26, CHAO)
    c.base(tapete_chao(78 * S), CX + 74, CHAO + 3)
    c.centro(adesivo("⭐", 28 * S, 0), CX + 88, CHAO - 44)
    return c.centro(adesivo("⭐", 20 * S, 12), CX + 58, CHAO - 58)


def cena_26():  # COM BARULHINHO MISTERIOSO
    c = Cena().base(carro("hatch", PRATA, 146 * S, ferrugem=True), CX - 6, CHAO)
    c.centro(ondinhas(26 * S), CX + 80, CHAO - 36)
    c.centro(com_contorno(moeda_interrogacao(34 * S), 2.6 * S), CX + 46, CHAO - 58)
    return c.centro(adesivo("🔧", 30 * S, -30), CX - 82, CHAO - 44)


def cena_r1():  # COM VIDRO DE MANIVELA
    c = Cena().base(carro("hatch", CREME, 146 * S), CX - 22, CHAO)
    return c.centro(com_contorno(manivela(62 * S), 2.6 * S), CX + 82, CHAO - 40)


def cena_r2():  # TANQUE SEMPRE NA RESERVA
    c = Cena().base(marcador_combustivel(126 * S), CX - 6, CHAO)
    return c.centro(adesivo("😬", 34 * S, 10), CX + 70, CHAO - 50)


def cena_r3():  # ELÉTRICO (SEM TOMADA)
    c = Cena()
    c.base(cabo(70 * S, 34 * S, [(1.0, 0.15), (0.6, -0.1), (0.35, 1.1), (0.05, 0.85)], 3.2 * S), CX - 74, CHAO - 2)
    c.base(carro("hatch", TURQUESA, 140 * S), CX + 22, CHAO)
    return c.centro(adesivo("🔌", 32 * S, -30), CX - 104, CHAO - 10)


def cena_r4():  # CHOVE DENTRO MAIS QUE FORA
    c = Cena().base(carro("hatch", LILAS, 146 * S), CX - 8, CHAO)
    c.centro(adesivo("🌧", 40 * S, 0), CX - 12, CHAO - 50)
    return c.centro(adesivo("☂️", 32 * S, 14), CX + 78, CHAO - 48)


CENAS = {1: cena_01, 2: cena_02, 3: cena_03, 4: cena_04, 5: cena_05, 6: cena_06, 7: cena_07, 8: cena_08,
         9: cena_09, 10: cena_10, 11: cena_11, 12: cena_12, 13: cena_13, 14: cena_14, 15: cena_15, 16: cena_16,
         17: cena_17, 18: cena_18, 19: cena_19, 20: cena_20, 21: cena_21, 22: cena_22, 23: cena_23, 24: cena_24,
         25: cena_25, 26: cena_26, 101: cena_r1, 102: cena_r2, 103: cena_r3, 104: cena_r4}

# cor da etiqueta de cada carta (sem duas iguais em sequência; as de "(…)" nunca no amarelo)
COR_CARTA = {1: "amarelo", 2: "turquesa", 3: "coral", 4: "grafite", 5: "amarelo", 6: "turquesa", 7: "coral",
             8: "grafite", 9: "turquesa", 10: "amarelo", 11: "coral", 12: "turquesa", 13: "grafite", 14: "amarelo",
             15: "coral", 16: "turquesa", 17: "grafite", 18: "amarelo", 19: "coral", 20: "turquesa", 21: "grafite",
             22: "turquesa", 23: "amarelo", 24: "coral", 25: "grafite", 26: "amarelo",
             101: "turquesa", 102: "coral", 103: "grafite", 104: "amarelo"}


def finalizar_desenho(cena):
    """Apara, garante o tamanho máximo, põe contorno branco de adesivo e sombra."""
    im = aparar(cena.im)
    mw, mh = ILU_MAX[0] * S, ILU_MAX[1] * S
    k = min(1.3, mw / im.width, mh / im.height)
    if abs(k - 1.0) > 0.01:
        im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    im = com_contorno(im, 4.2 * S, "#FFFFFF")
    ims, pad = com_sombra(im, 0, int(2.5 * S), int(2.5 * S), 0.35, "#0E1014")
    return ims, pad, k


# ---------------------------------------------------------------- texto
def _fontes(linhas, tam, escalas, arquivo):
    out = []
    for l, e in zip(linhas, escalas):
        t = max(10, int(round(tam * e)))
        f = ImageFont.truetype(arquivo, t * S)
        sw = max(3, round(t * 0.085)) * S
        out.append((t, f, sw))
    return out


def bloco_texto(linhas, tam, escalas, cores, cor_contorno, arquivo=F_BLACK):
    """Renderiza o bloco de texto (contorno + sombra dura). Devolve imagem e a altura das maiúsculas."""
    fontes = _fontes(linhas, tam, escalas, arquivo)
    d0 = ImageDraw.Draw(Image.new("L", (4, 4)))
    larg = max(d0.textlength(l, font=f) + 2 * sw for l, (_, f, sw) in zip(linhas, fontes))
    caps = [-f.getbbox("H", anchor="ls")[1] for _, f, _ in fontes]
    acento = [-f.getbbox("ÊÁÉÍÃÓ", anchor="ls")[1] for _, f, _ in fontes]
    bases = [0.0]
    for i in range(1, len(linhas)):
        bases.append(bases[-1] + caps[i] + (acento[i] - caps[i]) * 0.85 + fontes[i][2] * 1.0)
    sombra = max(3, round(fontes[0][0] * 0.07)) * S
    margem = int(fontes[0][0] * S * 0.8)
    Wb = int(larg + 2 * margem)
    Hb = int(bases[-1] + caps[0] + 2 * margem + sombra)
    im = Image.new("RGBA", (Wb, Hb), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    y_cap0 = margem + caps[0]  # linha de base da 1ª linha
    for i, l in enumerate(linhas):
        _, f, sw = fontes[i]
        d.text((Wb / 2, y_cap0 + bases[i] + sombra), l, font=f, anchor="ms", fill=rgb(cor_contorno),
               stroke_width=sw, stroke_fill=rgb(cor_contorno))
    for i, l in enumerate(linhas):
        _, f, sw = fontes[i]
        d.text((Wb / 2, y_cap0 + bases[i]), l, font=f, anchor="ms", fill=rgb(cores[i]),
               stroke_width=sw, stroke_fill=rgb(cor_contorno))
    # centro óptico = meio entre o topo das maiúsculas da 1ª linha e a base da última
    centro_y = (margem + y_cap0 + bases[-1]) / 2
    bb = im.getbbox()
    return im, bb, centro_y


def desenhar_texto(img, linhas, area, cor_contorno, cores=("#FFFFFF", "#FFFFFF"), tam_max=TAM_MAX,
                   tam_min=TAM_MIN, escalas=None, arquivo=F_BLACK):
    """Escolhe o maior tamanho em que o bloco cabe INTEIRO (largura e altura) na área e desenha."""
    x0, y0, x1, y1 = [v * S for v in area]
    escalas = escalas or [1.0] * len(linhas)
    for tam in range(tam_max, tam_min - 1, -1):
        bloco, bb, centro_y = bloco_texto(linhas, tam, escalas, cores, cor_contorno, arquivo)
        bw, bh = bb[2] - bb[0], bb[3] - bb[1]
        if bw > x1 - x0 or bh > y1 - y0:
            continue
        cx = (x0 + x1) / 2
        dx = cx - bloco.width / 2
        dy = (y0 + y1) / 2 - centro_y
        # ajusta para o bloco inteiro (acento, parêntese e sombra) ficar dentro da área
        topo, fundo = bb[1] + dy, bb[3] + dy
        if topo < y0:
            dy += y0 - topo
        elif fundo > y1:
            dy -= fundo - y1
        img.alpha_composite(bloco, (int(round(dx)), int(round(dy))))
        return tam
    raise SystemExit(f"texto não coube nem com {tam_min}px: {linhas}")


# ---------------------------------------------------------------- a etiqueta (moldura própria)
def mascara_corpo(e=0, w=W, h=H, s=S):
    m = Image.new("L", (w * s, h * s), 0)
    x0, y0, x1, y1 = BODY
    ImageDraw.Draw(m).rounded_rectangle([(x0 - e) * s, (y0 - e) * s, (x1 + e) * s, (y1 + e) * s],
                                        radius=max(1, R_BODY + e) * s, fill=255)
    return m


def etiqueta(pal, desenho=None, titulo_mode=False):
    """Sombra, borda branca, corpo com gradiente, brilho de pintura, faixa de asfalto e desenho."""
    size = (W * S, H * S)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    m_borda = mascara_corpo(BORDA)
    sombra = deslocar(m_borda, 0, 5 * S).filter(ImageFilter.GaussianBlur(5 * S))
    img.alpha_composite(camada_cor(size, "#0E1014", sombra, 0.55))
    img.alpha_composite(camada_cor(size, pal["shade"], deslocar(m_borda, 0, 5 * S)))
    img.alpha_composite(camada_cor(size, "#FFFFFF", m_borda))
    m_corpo = mascara_corpo(0)
    corpo = gradiente(W * S, H * S, [(0, pal["top"]), (1, pal["bot"])], (0.20, 0.80))
    img.alpha_composite(recortar(corpo, m_corpo))
    # brilho no topo
    gl = Image.new("L", size, 0)
    gd = ImageDraw.Draw(gl)
    for i in range(50):
        yy = BODY[1] + i * 1.6
        gd.line([(0, yy * S), (W * S, yy * S)], fill=int(66 * (1 - i / 50)), width=S * 2)
    img.alpha_composite(camada_cor(size, "#FFFFFF", interseccao(gl, m_corpo)))
    # reflexo diagonal de pintura (duas faixas suaves)
    rf = Image.new("L", size, 0)
    rd = ImageDraw.Draw(rf)
    for (xa, larg_f, a) in ((92, 46, 34), (150, 16, 28)):
        rd.polygon([((xa) * S, BODY[1] * S), ((xa + larg_f) * S, BODY[1] * S),
                    ((xa + larg_f - 70) * S, FAIXA_Y * S), ((xa - 70) * S, FAIXA_Y * S)], fill=a)
    rf = rf.filter(ImageFilter.GaussianBlur(3 * S))
    img.alpha_composite(camada_cor(size, "#FFFFFF", interseccao(rf, m_corpo)))
    # faixa de asfalto + tracejado amarelo
    mf = Image.new("L", size, 0)
    ImageDraw.Draw(mf).rectangle([0, FAIXA_Y * S, W * S, H * S], fill=255)
    mf = interseccao(mf, m_corpo)
    asf = gradiente(W * S, H * S, [(0, ASFALTO[0]), (1, ASFALTO[1])], (0, 1))
    img.alpha_composite(recortar(asf, mf))
    # granulado do asfalto
    rnd = random.Random(11)
    gr = Image.new("L", size, 0)
    grd = ImageDraw.Draw(gr)
    for _ in range(420):
        x, y = rnd.uniform(BODY[0], BODY[2]), rnd.uniform(FAIXA_Y + 1, BODY[3])
        r = rnd.uniform(0.4, 1.0)
        grd.ellipse([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], fill=rnd.randint(30, 70))
    img.alpha_composite(camada_cor(size, "#FFFFFF", interseccao(gr, mf)))
    d = ImageDraw.Draw(img)
    # meio-fio (linha clara no começo da faixa)
    lay = Image.new("RGBA", size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).rectangle([0, FAIXA_Y * S, W * S, (FAIXA_Y + 2.2) * S], fill=(255, 255, 255, 150))
    img.alpha_composite(recortar(lay, m_corpo))
    if not titulo_mode:
        lay = Image.new("RGBA", size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        yc = (FAIXA_Y + BODY[3]) / 2 + 1
        comp, gap = 26, 17
        x = 256 - comp / 2 - 5 * (comp + gap)
        while x < BODY[2]:
            ld.rounded_rectangle([x * S, (yc - 2.6) * S, (x + comp) * S, (yc + 2.6) * S], radius=2.6 * S,
                                 fill=rgb(AMARELO))
            x += comp + gap
        img.alpha_composite(recortar(lay, m_corpo))
    # desenho estacionado na borda de cima
    if desenho is not None:
        ims, pad, _ = desenho
        x = 256 * S - ims.width / 2
        y = ILU_BASE * S - (ims.height - pad) + int(2.5 * S)
        if y + pad < MARGEM_TOPO * S:
            raise SystemExit(f"desenho cortado em cima ({(y + pad) / S:.1f}px): reduzir ILU_MAX ou descer ILU_BASE")
        img.alpha_composite(ims, (int(x), int(y)))
    return img


def carta(item, chave):
    pal = PALETAS[COR_CARTA[chave]]
    des = finalizar_desenho(CENAS[chave]())
    img = etiqueta(pal, des)
    l1, l2 = item["linha1"], item["linha2"]
    cores = ("#FFFFFF", pal["dest"] if l2.startswith("(") else "#FFFFFF")
    tam = desenhar_texto(img, [l1, l2], TEXT_AREA, pal["shade"], cores)
    return reduzir(img), tam, des[2]


# ---------------------------------------------------------------- título
def desenho_titulo():
    c = Cena()
    c.base(carro("hatch", "#AEB6C4", 168 * S, capa=True), CX, CHAO)
    c.centro(com_contorno(moeda_interrogacao(66 * S), 3 * S), CX - 4, CHAO - 50)
    d = c.draw()
    for (x, y, r) in ((CX - 60, CHAO - 66, 8), (CX + 66, CHAO - 70, 6), (CX - 78, CHAO - 50, 4.5),
                      (CX + 82, CHAO - 54, 4.5)):
        estrela4(d, x * S, y * S, r * S, "#FFFFFF")
    return c


def pilula_toque(img):
    """Pílula 'TOQUE NA TELA' com mãozinha, em cima da faixa de asfalto."""
    f = ImageFont.truetype(F_BLACK, 19 * S)
    d = ImageDraw.Draw(img)
    txt = "TOQUE NA TELA"
    tw = d.textlength(txt, font=f)
    mao = emoji("👆", 24 * S)
    w = tw + mao.width + 30 * S
    h = 32 * S
    cx, cy = 256 * S, ((FAIXA_Y + BODY[3]) / 2 + 1) * S
    box = [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2]
    d.rounded_rectangle([box[0] - 3 * S, box[1] - 3 * S, box[2] + 3 * S, box[3] + 3 * S], radius=19 * S,
                        fill=rgb("#FFFFFF"))
    d.rounded_rectangle(box, radius=16 * S, fill=rgb(AMARELO))
    x = box[0] + 12 * S
    img.alpha_composite(mao, (int(x), int(cy - mao.height / 2)))
    d.text((x + mao.width + 7 * S, cy + 1 * S), txt, font=f, anchor="lm", fill=rgb(GRAFITE))


def titulo(com_toque=False):
    pal = dict(top="#5D6576", bot="#2E333E", shade="#121419")
    des = finalizar_desenho(desenho_titulo())
    img = etiqueta(pal, des, titulo_mode=com_toque)
    linhas = ["MEU PRÓXIMO", "CARRO VAI SER…"]
    cores = ("#FFFFFF", AMARELO)
    if com_toque:
        desenhar_texto(img, linhas, (36, 96, 476, 194), "#121419", cores, tam_max=52, tam_min=30, escalas=(0.86, 1.0))
        pilula_toque(img)
    else:
        desenhar_texto(img, linhas, TEXT_AREA, "#121419", cores, tam_max=58, tam_min=30, escalas=(0.86, 1.0))
    return reduzir(img)


# ---------------------------------------------------------------- ícone
def icone(tam_final=162, estilo="claro"):
    t = 648 if tam_final <= 162 else tam_final * 2   # desenha grande e reduz
    if estilo == "claro":
        img = gradiente(t, t, [(0, "#FFE766"), (0.6, "#FFC21A"), (1, "#FF9F1C")], (0.35, 0.65))
        cor_carro, cor_moeda, cor_q = TURQUESA, CORAL, "#FFFFFF"
    else:
        img = gradiente(t, t, [(0, "#3A4152"), (1, "#15171C")], (0.3, 0.7))
        glow = Image.new("L", (t, t), 0)
        ImageDraw.Draw(glow).ellipse([t * 0.10, t * 0.05, t * 0.90, t * 0.75], fill=150)
        glow = glow.filter(ImageFilter.GaussianBlur(t * 0.09))
        img.alpha_composite(camada_cor((t, t), "#1FC8C0", glow, 0.45))
        cor_carro, cor_moeda, cor_q = CORAL, AMARELO, GRAFITE
    d = ImageDraw.Draw(img)
    # estrada
    y_rua = t * 0.74
    d.rectangle([0, y_rua, t, t], fill=rgb("#2A2D35"))
    d.rectangle([0, y_rua, t, y_rua + t * 0.012], fill=(255, 255, 255, 140))
    yc = y_rua + (t - y_rua) * 0.55
    for x in np.arange(-t * 0.02, t, t * 0.22):
        d.rounded_rectangle([x, yc - t * 0.016, x + t * 0.13, yc + t * 0.016], radius=t * 0.016, fill=rgb(AMARELO))
    # brilhos
    for (x, y, r, a) in ((0.14, 0.16, 0.045, 230), (0.88, 0.13, 0.032, 210), (0.86, 0.50, 0.03, 200),
                         (0.10, 0.52, 0.025, 190)):
        estrela4(d, x * t, y * t, r * t, (255, 255, 255, a))
    # carro (área segura: 144/162 = 89% do quadro)
    car = carro("hatch", cor_carro, int(t * 0.74), traco=t * 0.016)
    car = com_contorno(car, t * 0.018, "#FFFFFF")
    cs, pad = com_sombra(car, 0, int(t * 0.012), int(t * 0.015), 0.35, "#0E1014")
    img.alpha_composite(cs, (int(t / 2 - cs.width / 2), int(y_rua + t * 0.045 - (cs.height - pad))))
    # ponto de interrogação grande
    q = moeda_interrogacao(int(t * 0.38), cor=cor_moeda, cor_txt=cor_q, borda=int(t * 0.022))
    q = com_contorno(q, t * 0.018, "#FFFFFF")
    qs, _ = com_sombra(q, 0, int(t * 0.012), int(t * 0.015), 0.35, "#0E1014")
    colar_centro(img, qs, t * 0.50, t * 0.255)
    return img.resize((tam_final, tam_final), Image.LANCZOS).convert("RGB")


# ---------------------------------------------------------------- prévia
def xadrez(w, h, q=12):
    im = Image.new("RGBA", (w, h), rgb("#FFFFFF"))
    d = ImageDraw.Draw(im)
    for y in range(0, h, q):
        for x in range(0, w, q):
            if (x // q + y // q) % 2:
                d.rectangle([x, y, x + q - 1, y + q - 1], fill=rgb("#D9DCE2"))
    return im


def foto_generica(w, h, tipo):
    """Fundos falsos para testar a leitura (rua de dia, dentro do carro, noite, fundo poluído)."""
    rnd = random.Random(tipo)
    if tipo == "rua":
        im = gradiente(w, h, [(0, "#9ED8F5"), (0.55, "#DDF1FA"), (1, "#DDF1FA")], (0, 1))
        d = ImageDraw.Draw(im)
        for i in range(6):
            x = i * w / 5 - 20
            bh = rnd.uniform(0.25, 0.45) * h
            d.rectangle([x, h * 0.62 - bh, x + w / 5 - 8, h * 0.62], fill=rgb(rnd.choice(["#E9DCC9", "#CFC4B5",
                                                                                          "#F2E6D8", "#BFB3A3"])))
            for jy in range(int(h * 0.62 - bh + 14), int(h * 0.62 - 20), 34):
                for jx in range(int(x + 10), int(x + w / 5 - 20), 26):
                    d.rectangle([jx, jy, jx + 12, jy + 16], fill=rgb("#8FB4C9"))
        d.rectangle([0, h * 0.62, w, h], fill=rgb("#55595F"))
        d.rectangle([0, h * 0.60, w, h * 0.63], fill=rgb("#C9C2B8"))
    elif tipo == "carro":
        im = gradiente(w, h, [(0, "#3A3D44"), (1, "#1C1D21")], (0, 1))
        d = ImageDraw.Draw(im)
        d.polygon([(w * 0.55, h * 0.06), (w * 1.0, h * 0.04), (w * 1.0, h * 0.36), (w * 0.62, h * 0.40)],
                  fill=rgb("#BFD9E6"))
        d.rounded_rectangle([w * 0.18, h * 0.36, w * 0.82, h * 1.1], radius=60, fill=rgb("#2A2B30"))
        d.rounded_rectangle([w * 0.30, h * 0.30, w * 0.70, h * 0.48], radius=40, fill=rgb("#33353B"))
        im = im.filter(ImageFilter.GaussianBlur(3))
    elif tipo == "noite":
        im = gradiente(w, h, [(0, "#0B0F1E"), (1, "#05060B")], (0, 1))
        d = ImageDraw.Draw(im)
        for _ in range(30):
            x, y, r = rnd.uniform(0, w), rnd.uniform(0, h * 0.7), rnd.uniform(10, 40)
            c = rnd.choice(["#FFB347", "#FFE08A", "#FF7A59", "#9FE7FF"])
            d.ellipse([x - r, y - r, x + r, y + r], fill=rgb(c, rnd.randint(40, 110)))
        im = im.filter(ImageFilter.GaussianBlur(6))
    else:  # poluído: fundo bem colorido
        im = Image.new("RGBA", (w, h), rgb("#FFF3D6"))
        d = ImageDraw.Draw(im)
        for _ in range(420):
            x, y = rnd.uniform(0, w), rnd.uniform(0, h)
            c = rnd.choice(["#FF7A52", "#1FC8C0", "#FFD43B", "#22252C", "#FFFFFF", "#9B7BFF"])
            s = rnd.uniform(6, 22)
            d.rectangle([x, y, x + s, y + s * 0.5], fill=rgb(c))
    return im


def silhueta(im, cx, topo, larg, cor):
    d = ImageDraw.Draw(im)
    w, h = im.size
    cab_w, cab_h = larg * 0.42, larg * 0.54
    d.ellipse([cx - cab_w / 2, topo, cx + cab_w / 2, topo + cab_h], fill=rgb(cor))
    d.rectangle([cx - cab_w * 0.22, topo + cab_h * 0.85, cx + cab_w * 0.22, topo + cab_h * 1.12], fill=rgb(cor))
    d.rounded_rectangle([cx - larg / 2, topo + cab_h * 1.05, cx + larg / 2, h + 60], radius=int(larg * 0.25),
                        fill=rgb(cor))


def celular(peca, tipo, largura_peca=0.66, cor_sil="#3C3A44"):
    w, h = 405, 720
    im = foto_generica(w, h, tipo)
    topo_cab = int(h * 0.40)
    silhueta(im, w / 2, topo_cab, w * 0.70, cor_sil)
    pw = int(w * largura_peca)
    ph = int(peca.height * pw / peca.width)
    p = peca.resize((pw, ph), Image.LANCZOS)
    im.alpha_composite(p, (int(w / 2 - pw / 2), int(topo_cab - ph + 6)))
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=36, fill=255)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(im, (0, 0), m)
    return out


def arredondar(icon, raio_frac=0.22):
    icon = icon.convert("RGBA")
    m = Image.new("L", icon.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, icon.width - 1, icon.height - 1],
                                        radius=int(icon.width * raio_frac), fill=255)
    icon.putalpha(m)
    return icon


def previa(pecas, icones, sims):
    fundo = rgb("#F3F4F7")
    COLS, TW, TH = 4, 400, 200
    GX, GY = 36, 64
    MARG = 40
    linhas = math.ceil(len(pecas) / COLS)
    larg = MARG * 2 + COLS * TW + (COLS - 1) * GX
    alt_grade = linhas * (TH + GY)
    alt_icones = 300
    alt_sim = 900
    alt = 140 + alt_grade + alt_icones + alt_sim + 40
    sheet = Image.new("RGBA", (larg, alt), fundo)
    d = ImageDraw.Draw(sheet)
    f_h1 = ImageFont.truetype(F_BLACK, 44)
    f_h2 = ImageFont.truetype(F_XBOLD, 28)
    f_lb = ImageFont.truetype(F_BOLD, 17)
    f_sm = ImageFont.truetype(F_SEMI, 15)
    d.text((MARG, 36), "C02 · Meu próximo carro — prévia das imagens", font=f_h1, fill=rgb(GRAFITE))
    d.text((MARG, 92), "Xadrez = transparente. Título e cartas: 512×256 (miniaturas aqui a 400×200). "
                       "Ordem da grade = ordem dos arquivos. Ícone de envio: 162×162.",
           font=f_sm, fill=rgb("#5B6070"))
    y0 = 140
    for i, (nome, im, legenda) in enumerate(pecas):
        r, c = divmod(i, COLS)
        x = MARG + c * (TW + GX)
        y = y0 + r * (TH + GY)
        cell = xadrez(TW, TH)
        th = im.copy()
        th.thumbnail((TW, TH), Image.LANCZOS)
        cell.alpha_composite(th, ((TW - th.width) // 2, (TH - th.height) // 2))
        sheet.alpha_composite(cell, (x, y))
        d.text((x, y + TH + 8), nome, font=f_lb, fill=rgb(GRAFITE))
        d.text((x, y + TH + 30), legenda, font=f_sm, fill=rgb("#6B7080"))
    y = y0 + alt_grade + 10
    d.text((MARG, y), "Ícone como aparece no app (cantos arredondados pelo próprio app): 162, 96 e 64 px",
           font=f_h2, fill=rgb(GRAFITE))
    x = MARG
    y += 50
    for nome, ic in icones:
        x_ini = x
        for tam in (162, 96, 64):
            a = arredondar(ic.resize((tam, tam), Image.LANCZOS))
            sheet.alpha_composite(a, (x, y + (162 - tam)))
            x += tam + 18
        d.text((x_ini, y + 172), nome, font=f_lb, fill=rgb(GRAFITE))
        x += 60
    for nome, ic in icones:
        ic2 = ic.resize((162, 162), Image.LANCZOS).convert("RGBA")
        dd = ImageDraw.Draw(ic2)
        dd.rectangle([9, 9, 152, 152], outline=rgb("#FF2BD6"), width=1)
        sheet.alpha_composite(ic2, (x, y))
        x += 162 + 18
    d.text((x - 2 * 180, y + 172), "linha rosa = área segura 144×144", font=f_sm, fill=rgb("#5B6070"))
    y = y0 + alt_grade + alt_icones
    d.text((MARG, y), "Simulação sobre fotos genéricas (largura da peça ≈ 66% da tela)", font=f_h2,
           fill=rgb(GRAFITE))
    y += 50
    x = MARG
    for rot, peca, tipo, cs in sims:
        cel = celular(peca, tipo, cor_sil=cs)
        sheet.alpha_composite(cel, (x, y))
        d.text((x, y + cel.height + 10), rot, font=f_lb, fill=rgb(GRAFITE))
        x += cel.width + GX
    return sheet.convert("RGB")


# ---------------------------------------------------------------- principal
def salvar(im, caminho):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    im.save(caminho, optimize=True)


def quadrado(im):
    q = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    q.alpha_composite(im, (0, (512 - im.height) // 2))
    return q


def main():
    with open(TEXTOS, encoding="utf-8") as fh:
        tx = json.load(fh)
    pecas = []
    imgs = {}
    tamanhos = {}
    escalas_des = {}

    for com_toque, nome in ((False, "titulo.png"), (True, "titulo_toque.png")):
        t = titulo(com_toque)
        salvar(t, os.path.join(AQUI, nome))
        salvar(quadrado(t), os.path.join(AQUI, "quadrado_512", nome))
        pecas.append((nome, t, "título" + (" + aviso de toque (padrão)" if com_toque else " (sem aviso)")))
        imgs[nome] = t

    for item in tx["resultados"]:
        im, tam, kd = carta(item, item["n"])
        nome = f"carta_{item['n']:02d}.png"
        salvar(im, os.path.join(AQUI, "cartas", nome))
        salvar(quadrado(im), os.path.join(AQUI, "quadrado_512", "cartas", nome))
        pecas.append((nome, im, f"{item['linha1']} / {item['linha2']} · {tam}px"))
        imgs[nome] = im
        tamanhos[nome] = tam
        escalas_des[nome] = round(kd, 2)
    for item in tx["reservas"]:
        im, tam, kd = carta(item, 100 + item["n"])
        nome = f"reserva_{item['n']:02d}.png"
        salvar(im, os.path.join(AQUI, "reservas", nome))
        salvar(quadrado(im), os.path.join(AQUI, "quadrado_512", "reservas", nome))
        pecas.append((nome, im, f"{item['codigo']} · {item['linha1']} / {item['linha2']} · {tam}px"))
        imgs[nome] = im
        tamanhos[nome] = tam
        escalas_des[nome] = round(kd, 2)

    icones = []
    for estilo, sufixo in (("claro", ""), ("escuro", "_alt")):
        ic162 = icone(162, estilo)
        ic512 = icone(512, estilo)
        salvar(ic162, os.path.join(AQUI, f"icone{sufixo}_162.png"))
        salvar(ic512, os.path.join(AQUI, f"icone{sufixo}_512.png"))
        icones.append((f"icone{sufixo}_162.png", ic512))
        pecas.append((f"icone{sufixo}_162.png", ic512.convert("RGBA"),
                      "ícone de envio" + (" (alternativo, noite)" if sufixo else " (principal)")))

    so_cartas = [n for n in tamanhos if n.startswith("carta_")]
    menor = sorted(so_cartas, key=lambda n: (tamanhos[n], n))
    sims = [
        ("titulo_toque.png · rua de dia", imgs["titulo_toque.png"], "rua", "#3C3A44"),
        (f"{menor[0]} · dentro do carro", imgs[menor[0]], "carro", "#6E6A78"),
        (f"{menor[1]} · fundo escuro", imgs[menor[1]], "noite", "#7A7488"),
        ("carta_06.png · fundo poluído", imgs["carta_06.png"], "poluido", "#3C3A44"),
    ]
    salvar(previa(pecas, icones, sims), os.path.join(AQUI, "previa.png"))

    linhas = []
    total_efeito = 0
    for raiz, _, arqs in sorted(os.walk(AQUI)):
        for a in sorted(arqs):
            if a.endswith(".png"):
                p = os.path.join(raiz, a)
                with Image.open(p) as im:
                    linhas.append(f"{os.path.relpath(p, AQUI):42s} {im.width}x{im.height}  {im.mode:5s} "
                                  f"{os.path.getsize(p) / 1024:7.1f} KB")
    with open(os.path.join(AQUI, "lista-de-arquivos.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(linhas) + "\n")
    print("\n".join(linhas))
    print("fonte usada por carta (px):", tamanhos)
    print("redução aplicada ao desenho (1.0 = sem redução):", {k: v for k, v in escalas_des.items() if v < 1})


if __name__ == "__main__":
    main()
