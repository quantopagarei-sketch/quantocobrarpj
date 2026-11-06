#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C06 · Meu amigo secreto: gera TODAS as imagens do efeito.

Como rodar (de qualquer pasta):
    python3 gerar.py

Precisa de: Python 3 + Pillow + numpy. Nenhuma IA generativa: tudo é desenho
em código (formas simples) mais emoji Noto.
Fontes (as duas sob SIL Open Font License 1.1):
  - Inter Display Black/ExtraBold  -> /usr/share/fonts/opentype/inter/
  - Noto Color Emoji               -> /usr/share/fonts/truetype/noto/NotoColorEmoji.ttf
    (no Pillow só funciona com size=109 e embedded_color=True)

Os textos vêm de ../textos.json (linha1/linha2 de cada carta). Se o redator
trocar um texto, basta rodar de novo. O desenho de cada carta está no
dicionário ILUSTRA, pelo número (reservas = 100 + número).

Identidade visual (diferente do C01, C02, C08 e C09):
  - moldura = ETIQUETA DE PRESENTE: ponta chanfrada à esquerda com ilhós
    dourado (furo de verdade, transparente), borda dourada e pesponto tracejado;
  - em cima, a MESMA CAIXA DE PRESENTE em todas as peças: fechada com laço no
    título e aberta nas cartas, com o resultado saindo de dentro; um barbante
    dourado liga a etiqueta à caixa;
  - paleta: verde-pinheiro, dourado, papel kraft e creme; vermelho só no laço,
    na fita e na pílula "TOQUE PRA ABRIR".

Saída (nesta pasta):
  titulo.png, titulo_toque.png ............. 512x256 (título sobre a cabeça)
  cartas/carta_01..26.png .................. 512x256 (sequência do sorteio)
  reservas/reserva_01..05.png .............. 512x256
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
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
TEXTOS = os.path.join(AQUI, "..", "textos.json")

FONT_DIR = "/usr/share/fonts/opentype/inter"
F_BLACK = os.path.join(FONT_DIR, "InterDisplay-Black.otf")
F_XBOLD = os.path.join(FONT_DIR, "InterDisplay-ExtraBold.otf")
F_BOLD = os.path.join(FONT_DIR, "InterDisplay-Bold.otf")
F_SEMI = os.path.join(FONT_DIR, "InterDisplay-SemiBold.otf")
F_EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

S = 3            # desenha em 3x e reduz com LANCZOS (bordas lisas)
W, H = 512, 256  # tamanho final de título e cartas

# ---------------------------------------------------------------- cores
CREME = "#FFF6E0"
OURO = "#FFD45A"
VERDE_ESC = "#0B3A26"
VERDE = "#1E7A4C"
VERMELHO = "#D7263D"
VERMELHO_ESC = "#9E1426"
TINTA = "#1D2B22"      # texto da prévia

# Corpos da etiqueta (sem par de clube: nada de vermelho+branco, preto+branco, azul).
PALETAS = {
    "pinheiro": dict(top="#2E9A63", bot="#11563A", shade="#062A1B", txt=CREME,
                     contorno="#062A1B", listra=("#FFFFFF", 0.07), pesponto=(OURO, 0.75)),
    "dourado":  dict(top="#FFD666", bot="#E99A12", shade="#6B3A00", txt=CREME,
                     contorno="#5E3300", listra=("#FFFFFF", 0.16), pesponto=("#7A4300", 0.45)),
    "kraft":    dict(top="#D8A06A", bot="#A9672F", shade="#3F2108", txt=CREME,
                     contorno="#3F2108", listra=("#FFFFFF", 0.09), pesponto=("#FFE7B0", 0.70)),
    "creme":    dict(top="#FFF9EC", bot="#F1DDB4", shade="#7A5A26", txt="#0E4A31",
                     contorno="#FFFDF6", listra=("#D9B77A", 0.18), pesponto=("#C9973A", 0.80),
                     sombra_txt="#D2B47C"),
}
ORDEM_CORES = ["pinheiro", "dourado", "kraft", "creme"]

# ---------------------------------------------------------------- geometria (em 1x)
# Etiqueta: retângulo com a ponta da esquerda chanfrada (onde fica o ilhós).
TAG_P = [(54, 94), (494, 94), (494, 232), (54, 232), (18, 196), (18, 130)]
TAG_R = 14                  # raio dos cantos
BORDA = 6                   # borda dourada
FURO_C = (38, 163)          # ilhós
FURO_R = 7
ILHOS_R = 14
TEXT_AREA = (70, 104, 478, 224)  # x0, y0, x1, y1 onde o texto pode ficar (408 px úteis)
TAM_MAX = 54
TAM_MIN = 34
# Caixa de presente (igual em todas as peças)
BX = 274                    # centro x da caixa = centro da área de texto (e do retângulo da etiqueta)
CX0, CX1 = BX - 52, BX + 52  # frente da caixa
CY0, CY1 = 68, 100
ITEM_BOX = (124, 76)        # espaço máx. do resultado que sai da caixa (l x a, já com o contorno)
ITEM_BASE = 78              # y da base do resultado (10 px dentro da caixa); topo fica a ~6 px
ESPACO_EXTRA = 1.0          # espaço a mais entre palavras (x espessura do contorno)
SEC_DX = 86                 # distância dos adesivos ao centro da caixa


def rgb(h, a=255):
    if isinstance(h, tuple):
        return tuple(h[:3]) + (a if len(h) < 4 or a != 255 else h[3],)
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def mix(c1, c2, t):
    a, b = rgb(c1) if isinstance(c1, str) else c1, rgb(c2) if isinstance(c2, str) else c2
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(4))


def hexa(c):
    return "#%02X%02X%02X" % c[:3]


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


def gradiente_radial(w, h, c_in, c_out, cx=0.5, cy=0.5, raio=0.75):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dist = np.sqrt(((xx / w) - cx) ** 2 + ((yy / h) - cy) ** 2) / raio
    t = dist.clip(0, 1)[..., None]
    a, b = np.array(rgb(c_in), np.float32), np.array(rgb(c_out), np.float32)
    return Image.fromarray((a * (1 - t) + b * t).clip(0, 255).astype(np.uint8), "RGBA")


def camada_cor(size, cor, mascara, alpha_mult=1.0):
    c = rgb(cor) if isinstance(cor, str) else cor
    lay = Image.new("RGBA", size, c[:3] + (0,))
    a = mascara if alpha_mult == 1.0 else mascara.point(lambda v: int(v * alpha_mult))
    lay.putalpha(a)
    return lay


def preencher(im, m, paradas, direcao=(0.0, 1.0), alpha=1.0):
    """Pinta a máscara m com um gradiente calculado só no retângulo da forma."""
    if isinstance(paradas, str):
        paradas = [(0, paradas), (1, paradas)]
    bb = m.getbbox()
    if not bb:
        return
    g = gradiente(bb[2] - bb[0], bb[3] - bb[1], paradas, direcao)
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    lay.paste(g, bb[:2])
    a = m if alpha == 1.0 else m.point(lambda v: int(v * alpha))
    lay.putalpha(ImageChops.multiply(lay.split()[3], a))
    im.alpha_composite(lay)


def mascara(size):
    m = Image.new("L", size, 0)
    return m, ImageDraw.Draw(m)


def inter(*ms):
    out = ms[0]
    for m in ms[1:]:
        out = ImageChops.multiply(out, m)
    return out


def uniao(*ms):
    out = ms[0]
    for m in ms[1:]:
        out = ImageChops.lighter(out, m)
    return out


def menos(a, b):
    return ImageChops.subtract(a, b)


def deslocar(m, dx, dy):
    out = Image.new(m.mode, m.size, 0)
    out.paste(m, (dx, dy))
    return out


def estrela4(d, cx, cy, r, cor):
    """Brilho de 4 pontas."""
    k = r * 0.28
    pts = [(cx, cy - r), (cx + k, cy - k), (cx + r, cy), (cx + k, cy + k),
           (cx, cy + r), (cx - k, cy + k), (cx - r, cy), (cx - k, cy - k)]
    d.polygon(pts, fill=cor)


def brilho(img, cx, cy, r, cor=OURO, contorno="#5E3300"):
    """Brilho de 4 pontas com contorno escuro (lê em fundo claro e escuro)."""
    d = ImageDraw.Draw(img)
    estrela4(d, cx, cy, r * 1.32, rgb(contorno, 200))
    estrela4(d, cx, cy, r, rgb(cor))


def bezier(p0, p1, p2, p3, n=80):
    pts = []
    for i in range(n + 1):
        t = i / n
        a = (1 - t) ** 3
        b = 3 * (1 - t) ** 2 * t
        c = 3 * (1 - t) * t ** 2
        e = t ** 3
        pts.append((a * p0[0] + b * p1[0] + c * p2[0] + e * p3[0],
                    a * p0[1] + b * p1[1] + c * p2[1] + e * p3[1]))
    return pts


# ---------------------------------------------------------------- emoji
_EMOJI_FONT = None


def emoji(ch, tam):
    """Renderiza um emoji Noto (109 px) e redimensiona para caber em tam x tam."""
    global _EMOJI_FONT
    if _EMOJI_FONT is None:
        _EMOJI_FONT = ImageFont.truetype(F_EMOJI, 109)
    ch = ch.replace("️", "")
    im = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((100, 100), ch, font=_EMOJI_FONT, embedded_color=True, anchor="mm")
    bb = im.getbbox()
    if bb is None:
        raise SystemExit(f"emoji sem glifo: {ch!r}")
    im = im.crop(bb)
    k = tam / max(im.size)
    return im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)


def caber(im, w, h):
    k = min(w / im.width, h / im.height)
    return im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)


def com_contorno(im, px, cor=CREME):
    """Contorno de 'adesivo' em volta de uma imagem com alfa."""
    pad = px + 4
    a = Image.new("L", (im.width + 2 * pad, im.height + 2 * pad), 0)
    a.paste(im.split()[3], (pad, pad))
    blur = a.filter(ImageFilter.GaussianBlur(px / 2.0))
    dil = blur.point(lambda v: 255 if v > 14 else int(v * 18))
    out = camada_cor(a.size, cor, dil)
    out.alpha_composite(im, (pad, pad))
    return out


def com_sombra(im, dx, dy, raio, alpha=0.28, cor="#000000"):
    pad = int(raio * 3) + max(abs(dx), abs(dy))
    base = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    a = Image.new("L", base.size, 0)
    a.paste(im.split()[3], (pad + dx, pad + dy))
    a = a.filter(ImageFilter.GaussianBlur(raio))
    base.alpha_composite(camada_cor(base.size, cor, a, alpha))
    base.alpha_composite(im, (pad, pad))
    return base, pad


def colar_centro(dst, im, cx, cy):
    dst.alpha_composite(im, (int(round(cx - im.width / 2)), int(round(cy - im.height / 2))))


def recortar(im):
    bb = im.getbbox()
    return im.crop(bb) if bb else im


# ================================================================ desenhos próprios
# Cada função desenha num quadro N x N (coordenadas de 0 a 1) e devolve a imagem recortada.
N = 420


def _u(*v):
    return [x * N for x in v]


def _rr(box, r):
    m, d = mascara((N, N))
    d.rounded_rectangle(_u(*box), radius=r * N, fill=255)
    return m


def _el(box):
    m, d = mascara((N, N))
    d.ellipse(_u(*box), fill=255)
    return m


def _pol(pts):
    m, d = mascara((N, N))
    d.polygon([(x * N, y * N) for x, y in pts], fill=255)
    return m


def _brilho_luz(im, m, box, alpha=0.35):
    """Reflexo de luz (elipse branca suave) dentro da forma m."""
    luz = _el(box).filter(ImageFilter.GaussianBlur(N * 0.02))
    preencher(im, inter(luz, m), "#FFFFFF", alpha=alpha)


def nota10(n=N):
    """Nota verde genérica com '10' (não copia cédula real)."""
    w, h = n, int(n * 0.52)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    m, d = mascara((w, h))
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=n * 0.06, fill=255)
    lay = gradiente(w, h, [(0, "#7BD07E"), (1, "#2E8B57")], (0.6, 0.4))
    lay.putalpha(m)
    im.alpha_composite(lay)
    d = ImageDraw.Draw(im)
    e = n * 0.045
    d.rounded_rectangle([e, e, w - e, h - e], radius=n * 0.035, outline=rgb("#D8F5D2", 200), width=int(n * 0.014))
    d.ellipse([w * 0.12, h * 0.22, w * 0.12 + h * 0.56, h * 0.78], fill=rgb("#A8E6A0"))
    d.ellipse([w * 0.12 + h * 0.12, h * 0.34, w * 0.12 + h * 0.44, h * 0.66], fill=rgb("#5DBB63"))
    f = ImageFont.truetype(F_BLACK, int(n * 0.30))
    d.text((w * 0.70, h * 0.53), "10", font=f, anchor="mm", fill=rgb("#FFFFFF"),
           stroke_width=int(n * 0.016), stroke_fill=rgb("#1B5E37"))
    return im


def desenho_celular(tela="apagada", n=N):
    """Celular genérico de pé (sem câmera saliente, sem marca)."""
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    k = n / N
    corpo = _rr((0.25, 0.02, 0.75, 0.98), 0.08)
    preencher(im, corpo, [(0, "#3A3D48"), (1, "#16181E")], (0.5, 0.5))
    tl = _rr((0.28, 0.06, 0.72, 0.94), 0.05)
    if tela == "apagada":
        preencher(im, tl, [(0, "#3A404D"), (1, "#14161C")], (0.3, 0.7))
        refl = _pol([(0.28, 0.42), (0.72, 0.18), (0.72, 0.34), (0.28, 0.58)])
        preencher(im, inter(refl, tl), "#FFFFFF", alpha=0.10)
    else:
        preencher(im, tl, [(0, "#E9FBEF"), (1, "#BDEBCB")], (0.3, 0.7))
        d = ImageDraw.Draw(im)
        # setinha de "enviar" (círculo + seta)
        d.ellipse(_u(0.36, 0.14, 0.64, 0.42), fill=rgb("#2E8B57"))
        d.line(_u(0.43, 0.28, 0.57, 0.28), fill=rgb("#FFFFFF"), width=int(N * 0.035))
        d.polygon([(0.55 * N, 0.21 * N), (0.62 * N, 0.28 * N), (0.55 * N, 0.35 * N)], fill=rgb("#FFFFFF"))
        nt = nota10(int(N * 0.38))
        im.alpha_composite(nt, (int(0.31 * N), int(0.52 * N)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(_u(0.44, 0.075, 0.56, 0.095), radius=N * 0.01, fill=rgb("#0E0F13"))
    if k != 1:
        im = im.resize((n, n), Image.LANCZOS)
    return recortar(im)


def d_transferencia():
    cel = desenho_celular("nota")
    cel = cel.rotate(8, resample=Image.BICUBIC, expand=True)
    nt = nota10(int(N * 0.62)).rotate(-14, resample=Image.BICUBIC, expand=True)
    tela_ = Image.new("RGBA", (int(N * 1.5), N), (0, 0, 0, 0))
    tela_.alpha_composite(caber(cel, int(N * 0.62), int(N * 0.98)), (int(N * 0.10), 0))
    nt_s, _ = com_sombra(nt, 0, 6, 8, 0.25)
    tela_.alpha_composite(nt_s, (int(N * 0.62), int(N * 0.30)))
    # rastro de movimento
    d = ImageDraw.Draw(tela_)
    for i, y in enumerate((0.42, 0.56, 0.70)):
        d.line([(N * (0.56 + 0.02 * i), N * y), (N * (0.68 + 0.02 * i), N * (y - 0.03))],
               fill=rgb("#2E8B57"), width=int(N * 0.03))
    return recortar(tela_)


def _meia():
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    perna = _rr((0.32, 0.04, 0.62, 0.68), 0.05)
    pe = _rr((0.32, 0.50, 0.96, 0.84), 0.17)
    m = uniao(perna, pe)
    preencher(im, m, [(0, "#F3EBDD"), (1, "#D8C9AE")], (0.4, 0.6))
    cano = inter(m, _rr((0.0, 0.0, 1.0, 0.16), 0.0))
    preencher(im, cano, [(0, "#2E9A63"), (1, "#17643F")])
    for y in (0.22, 0.31):
        preencher(im, inter(m, _rr((0.0, y, 1.0, y + 0.045), 0.0)), "#E3A92B")
    calc = inter(m, _el((0.22, 0.60, 0.50, 0.92)))
    preencher(im, calc, [(0, "#2E9A63"), (1, "#17643F")])
    bico = inter(m, _rr((0.80, 0.0, 1.0, 1.0), 0.0))
    preencher(im, bico, [(0, "#2E9A63"), (1, "#17643F")])
    # costura do cano e brilho
    d = ImageDraw.Draw(im)
    for x in np.arange(0.35, 0.60, 0.035):
        d.line([(x * N, 0.05 * N), (x * N, 0.14 * N)], fill=rgb("#0F4A30", 45), width=int(N * 0.006))
    _brilho_luz(im, m, (0.34, 0.18, 0.44, 0.60), 0.35)
    return recortar(im)


def d_meias():
    meia = _meia()
    tela_ = Image.new("RGBA", (int(N * 1.7), int(N * 1.2)), (0, 0, 0, 0))
    atras = meia.copy()
    arr = np.array(atras).astype(np.float32)
    arr[..., :3] *= 0.86
    atras = Image.fromarray(arr.clip(0, 255).astype(np.uint8), "RGBA")
    for ang, dx, dy in ((22, 0.05, 0.02), (-18, 0.62, 0.0)):
        r = atras.rotate(ang, resample=Image.BICUBIC, expand=True)
        rs, _ = com_sombra(r, 0, 4, 6, 0.18)
        tela_.alpha_composite(rs, (int(N * dx), int(N * dy)))
    f = meia.rotate(-4, resample=Image.BICUBIC, expand=True)
    fs, _ = com_sombra(f, 0, 6, 8, 0.28)
    tela_.alpha_composite(fs, (int(N * 0.30), int(N * 0.14)))
    return recortar(tela_)


def d_aromatizante():
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # cordão
    d.line(_u(0.42, 0.30, 0.42, 0.02), fill=rgb("#C99A2E"), width=int(N * 0.025))
    d.ellipse(_u(0.385, 0.0, 0.455, 0.06), outline=rgb("#C99A2E"), width=int(N * 0.02))
    # disco redondo (não é pinheirinho)
    disco = _el((0.12, 0.26, 0.72, 0.86))
    preencher(im, _el((0.10, 0.24, 0.74, 0.88)), "#FFFFFF")
    preencher(im, disco, [(0, "#FFB8D6"), (1, "#E25C9C")], (0.3, 0.7))
    _brilho_luz(im, disco, (0.18, 0.30, 0.46, 0.46), 0.35)
    d.ellipse(_u(0.40, 0.29, 0.44, 0.33), fill=rgb("#7A1F4A"))
    fl = emoji("🌸", int(N * 0.40))
    colar_centro(im, fl, 0.42 * N, 0.58 * N)
    # ondinhas de cheiro
    for i, (x0, y0) in enumerate(((0.74, 0.30), (0.80, 0.46), (0.74, 0.62))):
        pts = [((x0 + 0.20 * t) * N, (y0 + 0.035 * math.sin(t * math.pi * 3)) * N) for t in np.linspace(0, 1, 30)]
        d.line(pts, fill=rgb("#B455E0"), width=int(N * 0.03), joint="curve")
    return recortar(im)


def d_panetone():
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    miolo = _rr((0.18, 0.34, 0.82, 0.96), 0.07)
    preencher(im, miolo, [(0, "#FFE08A"), (1, "#EBB54A")], (0.3, 0.7))
    rnd = random.Random(5)
    d = ImageDraw.Draw(im)
    cores = ["#E53935", "#43A047", "#FB8C00", "#E53935", "#2E7D32", "#F4511E"]
    for i in range(16):
        x, y = rnd.uniform(0.24, 0.76), rnd.uniform(0.54, 0.80)
        s = rnd.uniform(0.035, 0.055)
        d.rounded_rectangle(_u(x - s / 2, y - s / 2, x + s / 2, y + s / 2), radius=N * 0.012,
                            fill=rgb(cores[i % len(cores)]))
    copa = _el((0.13, 0.08, 0.87, 0.50))
    preencher(im, copa, [(0, "#D07A2C"), (1, "#8A4210")], (0.2, 0.8))
    _brilho_luz(im, copa, (0.22, 0.11, 0.56, 0.24), 0.30)
    faixa = inter(miolo, _rr((0, 0.84, 1, 1), 0))
    preencher(im, faixa, [(0, "#F7E7C4"), (1, "#E5CC98")])
    d.line(_u(0.18, 0.845, 0.82, 0.845), fill=rgb("#C9A468"), width=int(N * 0.012))
    for i in range(7):
        x, y = rnd.uniform(0.24, 0.76), rnd.uniform(0.20, 0.40)
        s = rnd.uniform(0.03, 0.045)
        d.rounded_rectangle(_u(x - s / 2, y - s / 2, x + s / 2, y + s / 2), radius=N * 0.01,
                            fill=rgb(cores[(i + 2) % len(cores)]))
    return recortar(im)


def _pantufa(cor=("#D9C8FF", "#9C7BE6"), sola="#6A4BB8"):
    """Pantufa de lado (bico à esquerda), com gola felpuda branca na abertura."""
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    sola_m = _rr((0.03, 0.74, 0.97, 0.88), 0.07)
    preencher(im, sola_m, [(0, mix(sola, "#FFFFFF", 0.15)), (1, sola)])
    bico = inter(_el((0.03, 0.36, 0.70, 1.10)), _rr((0, 0, 1, 0.80), 0))
    calcanhar = _rr((0.40, 0.52, 0.97, 0.80), 0.10)
    corpo = uniao(bico, calcanhar)
    preencher(im, corpo, [(0, cor[0]), (1, cor[1])], (0.3, 0.7))
    _brilho_luz(im, corpo, (0.10, 0.42, 0.40, 0.56), 0.35)
    abertura = _el((0.50, 0.47, 0.95, 0.63))
    preencher(im, abertura, [(0, "#4E3394"), (1, "#7E5CCF")])
    # gola felpuda em volta da abertura
    d = ImageDraw.Draw(im)
    rnd = random.Random(9)
    for t in np.linspace(math.pi * 0.95, math.pi * 2.05, 16):
        x, y = 0.725 + 0.235 * math.cos(t), 0.55 + 0.085 * math.sin(t)
        r = rnd.uniform(0.038, 0.050)
        d.ellipse(_u(x - r, y - r, x + r, y + r), fill=rgb("#FFFFFF"))
    for t in np.linspace(math.pi * 0.05, math.pi * 0.95, 9):
        x, y = 0.725 + 0.235 * math.cos(t), 0.55 + 0.085 * math.sin(t)
        r = rnd.uniform(0.030, 0.040)
        d.ellipse(_u(x - r, y - r, x + r, y + r), fill=rgb("#EEE8F6"))
    # pompom no bico
    pom, pd = mascara((N, N))
    for (x, y, r) in ((0.24, 0.40, 0.075), (0.18, 0.44, 0.05), (0.30, 0.45, 0.05), (0.24, 0.34, 0.05)):
        pd.ellipse(_u(x - r, y - r, x + r, y + r), fill=255)
    preencher(im, pom, [(0, "#FFFFFF"), (1, "#E4DCF0")])
    return recortar(im)


def d_pantufa():
    """Pantufa felpuda (uma só: lê melhor em tamanho pequeno)."""
    return _pantufa()


def d_porta_celular():
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # saída de ar genérica do painel
    saida = _rr((0.06, 0.66, 0.94, 0.98), 0.06)
    preencher(im, saida, [(0, "#4A4E59"), (1, "#25272E")])
    for y in (0.74, 0.82, 0.90):
        d.rounded_rectangle(_u(0.12, y - 0.018, 0.88, y + 0.018), radius=N * 0.015, fill=rgb("#6B717E"))
    # braço e berço
    d.rounded_rectangle(_u(0.44, 0.52, 0.56, 0.72), radius=N * 0.02, fill=rgb("#8A909C"))
    d.rounded_rectangle(_u(0.16, 0.48, 0.84, 0.58), radius=N * 0.03, fill=rgb("#9AA0AC"))
    # celular deitado, tela apagada
    corpo = _rr((0.08, 0.06, 0.92, 0.54), 0.06)
    preencher(im, corpo, [(0, "#3A3D48"), (1, "#16181E")])
    tl = _rr((0.13, 0.10, 0.87, 0.50), 0.035)
    preencher(im, tl, [(0, "#3A404D"), (1, "#121419")], (0.3, 0.7))
    refl = _pol([(0.13, 0.36), (0.50, 0.10), (0.66, 0.10), (0.24, 0.50), (0.13, 0.50)])
    preencher(im, inter(refl, tl), "#FFFFFF", alpha=0.12)
    # garras laterais
    for x0 in (0.03, 0.87):
        d.rounded_rectangle(_u(x0, 0.14, x0 + 0.10, 0.48), radius=N * 0.03, fill=rgb("#9AA0AC"))
        d.rounded_rectangle(_u(x0 + 0.025, 0.18, x0 + 0.075, 0.44), radius=N * 0.02, fill=rgb("#B9BEC8"))
    return recortar(im)


def d_toalha():
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    baixo = _rr((0.04, 0.54, 0.96, 0.92), 0.08)
    preencher(im, baixo, [(0, "#FFD666"), (1, "#E39C1A")])
    d = ImageDraw.Draw(im)
    for y in (0.80, 0.85):
        d.line(_u(0.04, y, 0.96, y), fill=rgb("#17643F"), width=int(N * 0.025))
    cima = _rr((0.10, 0.16, 0.90, 0.60), 0.08)
    preencher(im, cima, [(0, "#FFFCF3"), (1, "#E9DCC4")])
    preencher(im, inter(cima, _rr((0.0, 0.47, 1.0, 0.53), 0.0)), "#2E9A63")
    # "bordado" = rabisco ilegível (nenhum nome de verdade)
    pts = []
    for i, t in enumerate(np.linspace(0, 1, 160)):
        x = 0.22 + 0.56 * t + 0.025 * math.sin(t * math.pi * 14)
        y = 0.31 - 0.05 * math.sin(t * math.pi * 14 + 0.6) * (0.6 + 0.4 * math.sin(t * 9))
        pts.append((x * N, y * N))
    d.line(pts, fill=rgb("#C2185B"), width=int(N * 0.022), joint="curve")
    return recortar(im)


def d_chocolate():
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    choc = [(0, "#8E4E2B"), (1, "#5A2C14")]
    barra = _rr((0.10, 0.06, 0.90, 0.60), 0.05)
    pingos, pd = mascara((N, N))
    for x, comp in ((0.22, 0.22), (0.40, 0.34), (0.60, 0.16), (0.78, 0.28)):
        pd.rectangle(_u(x - 0.045, 0.50, x + 0.045, 0.56 + comp), fill=255)
        pd.ellipse(_u(x - 0.045, 0.51 + comp, x + 0.045, 0.60 + comp), fill=255)
    poca = _el((0.12, 0.84, 0.88, 0.98))
    preencher(im, uniao(barra, pingos, poca), choc, (0.3, 0.7))
    d = ImageDraw.Draw(im)
    for c in range(3):
        for r in range(2):
            x0, y0 = 0.15 + c * 0.25, 0.11 + r * 0.235
            d.rounded_rectangle(_u(x0, y0, x0 + 0.21, y0 + 0.20), radius=N * 0.02, fill=rgb("#6B3519"))
            d.rounded_rectangle(_u(x0 + 0.02, y0 + 0.02, x0 + 0.19, y0 + 0.17), radius=N * 0.015, fill=rgb("#8A4A26"))
    _brilho_luz(im, barra, (0.14, 0.08, 0.50, 0.18), 0.25)
    return recortar(im)


def d_sanduicheira():
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for x in (0.16, 0.76):
        d.rounded_rectangle(_u(x, 0.82, x + 0.08, 0.90), radius=N * 0.02, fill=rgb("#2A2C33"))
    base = _rr((0.06, 0.54, 0.94, 0.86), 0.08)
    preencher(im, base, [(0, "#E3E6EB"), (1, "#A9AFB9")])
    tampa = _rr((0.08, 0.20, 0.92, 0.62), 0.20)
    preencher(im, tampa, [(0, "#4A4E59"), (1, "#22242B")])
    _brilho_luz(im, tampa, (0.18, 0.24, 0.62, 0.36), 0.25)
    d.line(_u(0.10, 0.60, 0.90, 0.60), fill=rgb("#15161A"), width=int(N * 0.015))
    d.rounded_rectangle(_u(0.36, 0.52, 0.64, 0.66), radius=N * 0.03, fill=rgb("#15161A"))
    d.ellipse(_u(0.80, 0.68, 0.86, 0.74), fill=rgb("#5BE37F"))
    return recortar(im)


def d_desodorante():
    """Desodorante spray liso (sem rótulo), com névoa saindo do bico."""
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    corpo = uniao(_rr((0.30, 0.34, 0.66, 0.96), 0.05), _el((0.30, 0.22, 0.66, 0.46)))
    preencher(im, corpo, [(0, "#B9A2F0"), (1, "#6B4FC4")], (1.0, 0.0))
    d.rounded_rectangle(_u(0.35, 0.36, 0.40, 0.90), radius=N * 0.025, fill=rgb("#FFFFFF", 110))
    tampa = _el((0.37, 0.10, 0.59, 0.30))
    preencher(im, tampa, [(0, "#FFFFFF"), (1, "#C5CAD3")], (1.0, 0.0))
    d.rounded_rectangle(_u(0.44, 0.06, 0.53, 0.14), radius=N * 0.02, fill=rgb("#8A909C"))
    d.rounded_rectangle(_u(0.52, 0.075, 0.58, 0.105), radius=N * 0.01, fill=rgb("#5E6370"))
    rnd = random.Random(15)
    for _ in range(26):
        a = rnd.uniform(-0.45, 0.35)
        r = rnd.uniform(0.06, 0.34)
        x, y = 0.60 + r * math.cos(a), 0.09 + r * math.sin(a)
        rr_ = 0.008 + 0.018 * r
        d.ellipse(_u(x - rr_, y - rr_, x + rr_, y + rr_), fill=rgb("#9FD8F5", 220))
    return recortar(im)


def d_pano():
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    pano = _rr((0.10, 0.06, 0.90, 0.74), 0.03)
    preencher(im, pano, [(0, "#FFFDF7"), (1, "#EADFCC")])
    preencher(im, inter(pano, _rr((0, 0.50, 1, 0.555), 0)), "#2E9A63")
    preencher(im, inter(pano, _rr((0, 0.58, 1, 0.61), 0)), "#E3A92B")
    d = ImageDraw.Draw(im)
    # quadriculado leve do pano
    for x in np.arange(0.18, 0.9, 0.08):
        d.line(_u(x, 0.08, x, 0.46), fill=rgb("#D9CBB2", 120), width=int(N * 0.008))
    # barradinho de crochê (leques com furinhos)
    n_leq = 6
    larg = 0.80 / n_leq
    for i in range(n_leq):
        cx = 0.10 + larg * (i + 0.5)
        d.pieslice(_u(cx - larg / 2, 0.64, cx + larg / 2, 0.64 + larg * 1.6), 0, 180, fill=rgb("#F2B33D"))
        for k, ang in enumerate((25, 65, 115, 155)):
            r = larg * 0.55
            px = cx + r * math.cos(math.radians(ang)) * 0.9
            py = 0.64 + larg * 0.8 + r * math.sin(math.radians(ang)) * 0.9
            d.ellipse(_u(px - 0.012, py - 0.012, px + 0.012, py + 0.012), fill=rgb("#B9771A"))
    d.rectangle(_u(0.10, 0.73, 0.90, 0.755), fill=rgb("#E39C1A"))
    # virado de cabeça pra baixo: o barradinho de crochê fica em cima, fora da caixa
    return recortar(im.transpose(Image.FLIP_TOP_BOTTOM))


def d_volante():
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # raios e cubo (sem emblema)
    d.rounded_rectangle(_u(0.16, 0.45, 0.84, 0.57), radius=N * 0.04, fill=rgb("#3A3D46"))
    d.rounded_rectangle(_u(0.44, 0.50, 0.56, 0.82), radius=N * 0.04, fill=rgb("#3A3D46"))
    cubo = _el((0.36, 0.37, 0.64, 0.65))
    preencher(im, cubo, [(0, "#4C505B"), (1, "#24262D")])
    d.ellipse(_u(0.41, 0.42, 0.59, 0.60), outline=rgb("#5E6370"), width=int(N * 0.012))
    # aro de pelúcia
    aro = menos(_el((0.04, 0.04, 0.96, 0.96)), _el((0.22, 0.22, 0.78, 0.78)))
    preencher(im, aro, "#E86FA8")
    rnd = random.Random(21)
    for _ in range(170):
        t = rnd.uniform(0, 2 * math.pi)
        rr_ = rnd.uniform(0.29, 0.44)
        x, y = 0.5 + rr_ * math.cos(t), 0.5 + rr_ * math.sin(t)
        r = rnd.uniform(0.035, 0.06)
        c = rnd.choice(["#F48FBF", "#FFB3D4", "#E86FA8", "#FFC7DF", "#D9558F"])
        d.ellipse(_u(x - r, y - r, x + r, y + r), fill=rgb(c))
    return recortar(im)


def d_squeeze():
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(_u(0.45, 0.02, 0.55, 0.14), radius=N * 0.03, fill=rgb("#2D3038"))
    tampa = _rr((0.33, 0.11, 0.67, 0.27), 0.05)
    preencher(im, tampa, [(0, "#4A4E59"), (1, "#22242B")])
    corpo = _rr((0.30, 0.25, 0.70, 0.94), 0.11)
    preencher(im, corpo, [(0, "#FFB25C"), (1, "#EE6A1A")], (1.0, 0.0))
    preencher(im, inter(corpo, _rr((0, 0.52, 1, 0.62), 0)), "#FFFFFF", alpha=0.35)
    d.rounded_rectangle(_u(0.36, 0.32, 0.41, 0.86), radius=N * 0.025, fill=rgb("#FFFFFF", 100))

    def gota(cx, cy, r):
        d.ellipse(_u(cx - r, cy - r, cx + r, cy + r), fill=rgb("#38B6F0"))
        d.polygon([(cx * N, (cy - r * 2.1) * N), ((cx - r * 0.92) * N, (cy - r * 0.4) * N),
                   ((cx + r * 0.92) * N, (cy - r * 0.4) * N)], fill=rgb("#38B6F0"))
        d.ellipse(_u(cx - r * 0.45, cy - r * 0.35, cx - r * 0.05, cy + r * 0.05), fill=rgb("#FFFFFF", 180))
    gota(0.80, 0.70, 0.06)
    gota(0.88, 0.90, 0.045)
    gota(0.18, 0.84, 0.05)
    return recortar(im)


def d_porta_retrato():
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    mold = _rr((0.04, 0.16, 0.96, 0.84), 0.04)
    preencher(im, mold, [(0, "#D89A5C"), (1, "#8D5524")], (0.4, 0.6))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(_u(0.08, 0.20, 0.92, 0.80), radius=N * 0.03, outline=rgb("#F1C38C", 160), width=int(N * 0.012))
    d.rectangle(_u(0.14, 0.26, 0.86, 0.74), fill=rgb("#FFF6E6"))
    vazio = _rr((0.20, 0.32, 0.80, 0.68), 0.0)
    preencher(im, vazio, [(0, "#D3D6DC"), (1, "#A9AEB7")])
    return recortar(im)


def d_envelope():
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    aba = _pol([(0.06, 0.42), (0.94, 0.42), (0.50, 0.12)])
    preencher(im, aba, [(0, "#E8D3A8"), (1, "#D9BE8A")])
    nt = nota10(int(N * 0.62)).rotate(10, resample=Image.BICUBIC, expand=True)
    im.alpha_composite(nt, (int(N * 0.17), int(N * 0.14)))
    frente = _pol([(0.06, 0.42), (0.50, 0.70), (0.94, 0.42), (0.94, 0.94), (0.06, 0.94)])
    preencher(im, frente, [(0, "#FFF4DC"), (1, "#EEDBB4")])
    d = ImageDraw.Draw(im)
    d.line([(0.06 * N, 0.94 * N), (0.44 * N, 0.66 * N)], fill=rgb("#D2B27A"), width=int(N * 0.012))
    d.line([(0.94 * N, 0.94 * N), (0.56 * N, 0.66 * N)], fill=rgb("#D2B27A"), width=int(N * 0.012))
    d.line([(0.06 * N, 0.42 * N), (0.50 * N, 0.70 * N), (0.94 * N, 0.42 * N)], fill=rgb("#C9A468"),
           width=int(N * 0.014), joint="curve")
    return recortar(im)


def d_bombons():
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    caixa = _rr((0.02, 0.24, 0.98, 0.84), 0.06)
    preencher(im, caixa, [(0, "#FFD666"), (1, "#D9901A")])
    bandeja = _rr((0.06, 0.29, 0.94, 0.79), 0.04)
    preencher(im, bandeja, [(0, "#5A2C14"), (1, "#3A1A0A")])
    d = ImageDraw.Draw(im)
    vazios = {1, 4, 6}
    k = 0
    for row, y in enumerate((0.42, 0.66)):
        for x in (0.17, 0.39, 0.61, 0.83):
            d.ellipse(_u(x - 0.10, y - 0.10, x + 0.10, y + 0.10), fill=rgb("#7A4524"))
            if k in vazios:
                d.ellipse(_u(x - 0.075, y - 0.075, x + 0.075, y + 0.075), fill=rgb("#2A1206"))
            else:
                b = _el((x - 0.085, y - 0.085, x + 0.085, y + 0.085))
                preencher(im, b, [(0, "#9A5A33"), (1, "#4E2310")], (0.3, 0.7))
                d.arc(_u(x - 0.05, y - 0.03, x + 0.05, y + 0.03), 200, 340, fill=rgb("#C88B5E"), width=int(N * 0.014))
            k += 1
    return recortar(im)


def d_capinha():
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    capa = _rr((0.25, 0.03, 0.75, 0.97), 0.10)
    preencher(im, capa, [(0, "#FFA8A0"), (1, "#F0627E")], (0.4, 0.6))
    furo = _rr((0.31, 0.09, 0.50, 0.30), 0.05)
    preencher(im, furo, "#2B2D33")
    d = ImageDraw.Draw(im)
    rnd = random.Random(3)
    for _ in range(22):
        x, y = rnd.uniform(0.30, 0.70), rnd.uniform(0.36, 0.92)
        r = rnd.uniform(0.006, 0.014)
        d.ellipse(_u(x - r, y - r, x + r, y + r), fill=rgb("#FFFFFF", 200))
    d.rounded_rectangle(_u(0.73, 0.22, 0.77, 0.34), radius=N * 0.015, fill=rgb("#E0566F"))
    return recortar(im)


# ---------------------------------------------------------------- ilustrações por carta
# main: emoji (str) ou função de desenho; sec: adesivo à direita; sec_esq: adesivo à esquerda;
# chip: etiqueta escura com texto dourado; escala: tamanho do resultado (1 = máximo).
ILUSTRA = {
    1: dict(main=d_meias),                                   # meia (de novo): 3 meias iguais
    2: dict(main=d_transferencia),                           # transferência: celular + nota "10"
    3: dict(main="☕", sec="📣"),                             # caneca + megafone (coach)
    4: dict(main=d_aromatizante),                            # cheirinho redondo (não é pinheirinho)
    5: dict(main=d_panetone, sec="🕸"),                       # panetone sem caixa + teia
    6: dict(main="🎧", sec="❌", sec_esq="🎵"),                 # fone: só um lado toca
    7: dict(main="📝", sec="💗"),                             # bilhete "depois te dou" + coração
    8: dict(main="🧼", chip="3º"),                            # kit sabonete, o 3º
    9: dict(main=d_pantufa, sec="☀", chip="40°"),           # pantufa felpuda no calor
    10: dict(main="🎯", sec="✨"),                            # o que eu pedi: na mosca
    11: dict(main=d_porta_celular),                          # porta-celular de painel, tela apagada
    12: dict(main=d_toalha, chip="?"),                       # toalha com bordado errado
    13: dict(main=d_chocolate, sec="☀"),                     # chocolate derretido
    14: dict(main=d_sanduicheira, chip="+2"),                # sanduicheira
    15: dict(main=d_desodorante, chip="?", giro=-16),        # desodorante liso (spray)
    16: dict(main="🎁", sec="♻"),                            # presente reciclado
    17: dict(main="🔌", sec="🪫"),                            # carregador + bateria vazia
    18: dict(main=d_pano, sec="🧶", giro=8),                  # pano de prato (crochê pra cima)
    19: dict(main="🪑", sec="💨"),                            # cadeira vazia: quem tirou faltou
    20: dict(main="🪴", sec="🍂"),                            # plantinha + folha caindo
    21: dict(main=d_volante),                                # capa de volante peluda (sem emblema)
    22: dict(main="📒", chip="JAN", giro=12),                # agenda até janeiro
    23: dict(main="💎", sec="❌"),                            # presentão (foi engano)
    24: dict(main="🩴", sec="📏", giro=58),                  # chinelo (deitado) + régua
    25: dict(main=d_squeeze, sec="🎒", giro=-14),             # squeeze vazando + mochila
    26: dict(main="🧾", sec="🚫", giro=-10),                  # sem nota pra trocar
    # reservas
    101: dict(main=d_porta_retrato, giro=6),                 # porta-retrato (deitado) sem foto
    102: dict(main=d_envelope),                              # 10 reais num envelope
    103: dict(main=d_bombons),                               # bombons (já comeram 3)
    104: dict(main="🎯", sec="✨"),                           # mesma arte da carta 10
    105: dict(main=d_capinha, sec="❌", giro=-24),            # capinha que não serve
}


# ================================================================ moldura: etiqueta de presente
def inset_poligono(P, dist):
    """Desloca cada lado de um polígono convexo (horário na tela) para dentro e recalcula os vértices."""
    n = len(P)
    linhas = []
    for i in range(n):
        (x0, y0), (x1, y1) = P[i], P[(i + 1) % n]
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy)
        nx, ny = -dy / L, dx / L
        linhas.append(((x0 + nx * dist, y0 + ny * dist), (dx, dy)))
    out = []
    for i in range(n):
        (p, r), (q, s) = linhas[i - 1], linhas[i]
        cr = r[0] * s[1] - r[1] * s[0]
        t = ((q[0] - p[0]) * s[1] - (q[1] - p[1]) * s[0]) / cr
        out.append((p[0] + r[0] * t, p[1] + r[1] * t))
    return out


def mascara_tag(e=0, furo=True):
    """Forma da etiqueta (cantos redondos), expandida em e px, com o furo do ilhós."""
    m, d = mascara((W * S, H * S))
    nucleo = inset_poligono(TAG_P, TAG_R)
    pts = [(x * S, y * S) for x, y in nucleo]
    raio = (TAG_R + e) * S
    d.polygon(pts, fill=255)
    d.line(pts + [pts[0]], fill=255, width=int(2 * raio), joint="curve")
    for x, y in pts:
        d.ellipse([x - raio, y - raio, x + raio, y + raio], fill=255)
    if furo:
        cx, cy = FURO_C
        d.ellipse([(cx - FURO_R) * S, (cy - FURO_R) * S, (cx + FURO_R) * S, (cy + FURO_R) * S], fill=0)
    return m


def mascara_circulo(cx, cy, r):
    m, d = mascara((W * S, H * S))
    d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=255)
    return m


def etiqueta(p):
    """Sombra, borda dourada, corpo com papel listrado, brilho, pesponto e ilhós."""
    size = (W * S, H * S)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    m_borda = mascara_tag(BORDA)
    sombra = deslocar(m_borda, 0, 4 * S).filter(ImageFilter.GaussianBlur(3 * S))
    img.alpha_composite(camada_cor(size, "#0A1A10", sombra, 0.50))
    img.alpha_composite(camada_cor(size, p["shade"], deslocar(m_borda, 0, 4 * S)))
    preencher(img, m_borda, [(0, "#FFF0B8"), (0.45, "#F5C84C"), (1, "#C98A12")], (0.1, 0.9))
    m_corpo = mascara_tag(0)
    corpo = gradiente(W * S, H * S, [(0, p["top"]), (1, p["bot"])], (0.18, 0.82))
    corpo.putalpha(m_corpo)
    img.alpha_composite(corpo)
    # papel de presente: listras diagonais bem leves
    lst, ld = mascara(size)
    for x in range(-H, W + H, 26):
        ld.line([(x * S, 0), ((x + H) * S, H * S)], fill=255, width=9 * S)
    img.alpha_composite(camada_cor(size, p["listra"][0], inter(lst, m_corpo), p["listra"][1]))
    # brilho no topo
    gl, gd = mascara(size)
    y0, y1 = TAG_P[0][1], TAG_P[2][1]
    for i in range(50):
        yy = y0 + i * (y1 - y0) * 0.5 / 50
        gd.line([(0, yy * S), (W * S, yy * S)], fill=int(60 * (1 - i / 50)), width=S * 2)
    img.alpha_composite(camada_cor(size, "#FFFFFF", inter(gl, m_corpo)))
    # pesponto tracejado (costura da etiqueta), sem passar no ilhós
    d = ImageDraw.Draw(img)
    caminho = inset_poligono(TAG_P, 10)
    cor_p = rgb(p["pesponto"][0], int(255 * p["pesponto"][1]))
    traco, vao = 9, 6
    for i in range(len(caminho)):
        (x0, y0_), (x1, y1_) = caminho[i], caminho[(i + 1) % len(caminho)]
        L = math.hypot(x1 - x0, y1_ - y0_)
        nt = int((L - 8) // (traco + vao))
        sobra = (L - nt * (traco + vao) + vao) / 2
        for k in range(nt):
            a = (sobra + k * (traco + vao)) / L
            b = (sobra + k * (traco + vao) + traco) / L
            pa = (x0 + (x1 - x0) * a, y0_ + (y1_ - y0_) * a)
            pb = (x0 + (x1 - x0) * b, y0_ + (y1_ - y0_) * b)
            mx, my = (pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2
            if math.hypot(mx - FURO_C[0], my - FURO_C[1]) < ILHOS_R + 7:
                continue
            d.line([(pa[0] * S, pa[1] * S), (pb[0] * S, pb[1] * S)], fill=cor_p, width=int(2.2 * S))
    # ilhós dourado
    cx, cy = FURO_C
    anel = menos(mascara_circulo(cx, cy, ILHOS_R), mascara_circulo(cx, cy, FURO_R))
    img.alpha_composite(camada_cor(size, p["shade"], deslocar(anel, 0, 2 * S), 0.6))
    preencher(img, anel, [(0, "#FFF3C4"), (0.5, "#F2C443"), (1, "#B57A0E")], (0.3, 0.7))
    d.ellipse([(cx - FURO_R - 1) * S, (cy - FURO_R - 1) * S, (cx + FURO_R + 1) * S, (cy + FURO_R + 1) * S],
              outline=rgb("#8A5A08"), width=int(1.4 * S))
    furo = mascara_circulo(cx, cy, FURO_R - 0.5)
    img.putalpha(ImageChops.subtract(img.split()[3], furo))
    return img


def barbante(img):
    """Barbante dourado: sai do ilhós, passa por fora da ponta e vai até a caixa."""
    cx, cy = FURO_C
    pts = bezier((cx + 2, cy - 3), (cx - 34, cy - 54), (CX0 - 150, CY0 - 30), (CX0 + 2, CY0 + 22))
    pts = [(x * S, y * S) for x, y in pts]
    d = ImageDraw.Draw(img)
    d.line(pts, fill=rgb("#4A2E08"), width=int(6.5 * S), joint="curve")
    d.line(pts, fill=rgb("#E8BC4A"), width=int(3.6 * S), joint="curve")
    # torcido do barbante
    for i in range(3, len(pts) - 3, 4):
        x, y = pts[i]
        d.line([(x - 1.2 * S, y - 1.2 * S), (x + 1.2 * S, y + 1.2 * S)], fill=rgb("#B8861C"), width=int(1.0 * S))
    # nó na caixa
    kx, ky = (CX0 + 2) * S, (CY0 + 22) * S
    d.ellipse([kx - 5 * S, ky - 5 * S, kx + 5 * S, ky + 5 * S], fill=rgb("#4A2E08"))
    d.ellipse([kx - 3.4 * S, ky - 3.4 * S, kx + 3.4 * S, ky + 3.4 * S], fill=rgb("#E8BC4A"))


# ---------------------------------------------------------------- caixa de presente
def caixa_fundo(img):
    """Parte de trás da caixa aberta (o 'dentro'), desenhada antes do resultado."""
    d = ImageDraw.Draw(img)
    pts = [(CX0 - 1, CY0 + 2), (CX1 + 1, CY0 + 2), (CX1 - 9, CY0 - 10), (CX0 + 9, CY0 - 10)]
    d.polygon([(x * S, y * S) for x, y in pts], fill=rgb("#4A2E08"))
    pts = [(CX0 + 1.5, CY0 + 1), (CX1 - 1.5, CY0 + 1), (CX1 - 10, CY0 - 8), (CX0 + 10, CY0 - 8)]
    d.polygon([(x * S, y * S) for x, y in pts], fill=rgb("#0A2F1F"))
    # fita vermelha subindo por dentro
    d.polygon([((BX - 7) * S, (CY0 + 1) * S), ((BX + 7) * S, (CY0 + 1) * S),
               ((BX + 6) * S, (CY0 - 8) * S), ((BX - 6) * S, (CY0 - 8) * S)], fill=rgb(VERMELHO_ESC))


def caixa_frente(img, fechada=False):
    size = img.size
    m, md = mascara(size)
    md.rounded_rectangle([CX0 * S, CY0 * S, CX1 * S, CY1 * S], radius=5 * S, fill=255)
    # contorno escuro + sombra no corpo da etiqueta
    cont, cd = mascara(size)
    cd.rounded_rectangle([(CX0 - 2.5) * S, (CY0 - 2.5) * S, (CX1 + 2.5) * S, (CY1 + 2.5) * S], radius=7 * S, fill=255)
    img.alpha_composite(camada_cor(size, "#000000", deslocar(cont, 0, 3 * S).filter(ImageFilter.GaussianBlur(3 * S)), 0.35))
    img.alpha_composite(camada_cor(size, "#4A2E08", cont))
    preencher(img, m, [(0, "#2FA068"), (1, "#14603F")], (0.25, 0.75))
    d = ImageDraw.Draw(img)
    # listras do papel da caixa
    lst, ld = mascara(size)
    for x in range(CX0 - 60, CX1 + 60, 14):
        ld.line([(x * S, CY0 * S), ((x + 40) * S, CY1 * S)], fill=255, width=4 * S)
    img.alpha_composite(camada_cor(size, "#FFFFFF", inter(lst, m), 0.10))
    # fita vertical
    fita, fd = mascara(size)
    fd.rectangle([(BX - 8) * S, CY0 * S, (BX + 8) * S, CY1 * S], fill=255)
    preencher(img, inter(fita, m), [(0, "#F0414F"), (1, "#B3172A")], (1.0, 0.0))
    d.line([((BX - 8) * S, CY0 * S), ((BX - 8) * S, CY1 * S)], fill=rgb("#7E0E1E"), width=int(1.2 * S))
    d.line([((BX + 8) * S, CY0 * S), ((BX + 8) * S, CY1 * S)], fill=rgb("#7E0E1E"), width=int(1.2 * S))
    if not fechada:
        # borda de cima da caixa (luz)
        d.rounded_rectangle([CX0 * S, CY0 * S, CX1 * S, (CY0 + 4) * S], radius=2 * S, fill=rgb("#5CC48E"))
        d.rectangle([(BX - 8) * S, CY0 * S, (BX + 8) * S, (CY0 + 4) * S], fill=rgb("#FF6B78"))


def tampa_e_laco(img):
    """Tampa por cima da caixa e laço grande vermelho (só no título)."""
    size = img.size
    tx0, tx1, ty0, ty1 = CX0 - 6, CX1 + 6, CY0 - 12, CY0 + 6
    cont, cd = mascara(size)
    cd.rounded_rectangle([(tx0 - 2.5) * S, (ty0 - 2.5) * S, (tx1 + 2.5) * S, (ty1 + 2.5) * S], radius=6 * S, fill=255)
    img.alpha_composite(camada_cor(size, "#4A2E08", cont))
    m, md = mascara(size)
    md.rounded_rectangle([tx0 * S, ty0 * S, tx1 * S, ty1 * S], radius=4 * S, fill=255)
    preencher(img, m, [(0, "#4DBB82"), (1, "#1B7049")])
    fita, fd = mascara(size)
    fd.rectangle([(BX - 9) * S, ty0 * S, (BX + 9) * S, ty1 * S], fill=255)
    preencher(img, inter(fita, m), [(0, "#FF5361"), (1, "#C21A2E")], (1.0, 0.0))
    # laço: duas alças, nó e pontas
    lay = Image.new("RGBA", size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    cx, cy = BX, ty0 - 2
    for lado in (-1, 1):
        ponta = [((cx + lado * 4) * S, (cy + 2) * S), ((cx + lado * 18) * S, (cy + 22) * S),
                 ((cx + lado * 10) * S, (cy + 24) * S), ((cx + lado * 1) * S, (cy + 4) * S)]
        ld.polygon(ponta, fill=rgb("#B3172A"))
    alcas, ad = mascara(size)
    for lado in (-1, 1):
        a = Image.new("L", (64 * S, 40 * S), 0)
        ImageDraw.Draw(a).ellipse([2 * S, 4 * S, 60 * S, 36 * S], fill=255)
        a = a.rotate(lado * 24, resample=Image.BICUBIC, expand=True)
        alcas.paste(255, (int((cx + lado * 23) * S - a.width / 2), int((cy - 13) * S - a.height / 2)), a)
    contorno = alcas.filter(ImageFilter.MaxFilter(7))
    img.alpha_composite(lay)
    img.alpha_composite(camada_cor(size, "#5E0A16", contorno))
    preencher(img, alcas, [(0, "#FF6B78"), (1, "#C21A2E")], (0.2, 0.8))
    # miolo das alças (sombra interna)
    d = ImageDraw.Draw(img)
    for lado in (-1, 1):
        a = Image.new("L", (34 * S, 18 * S), 0)
        ImageDraw.Draw(a).ellipse([1 * S, 1 * S, 33 * S, 17 * S], fill=255)
        a = a.rotate(lado * 24, resample=Image.BICUBIC, expand=True)
        cam = Image.new("L", size, 0)
        cam.paste(a, (int((cx + lado * 21) * S - a.width / 2), int((cy - 12) * S - a.height / 2)))
        img.alpha_composite(camada_cor(size, "#8E0F22", cam, 0.85))
    d.ellipse([(cx - 9) * S, (cy - 10) * S, (cx + 9) * S, (cy + 6) * S], fill=rgb("#5E0A16"))
    d.ellipse([(cx - 7) * S, (cy - 8) * S, (cx + 7) * S, (cy + 4) * S], fill=rgb("#E8303F"))
    d.ellipse([(cx - 4) * S, (cy - 6) * S, (cx + 1) * S, (cy - 2) * S], fill=rgb("#FF8A94"))


def selo_interrogacao(img, cx, cy, r):
    d = ImageDraw.Draw(img)
    d.ellipse([(cx - r - 2) * S, (cy - r - 2) * S, (cx + r + 2) * S, (cy + r + 2) * S], fill=rgb("#4A2E08"))
    d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=rgb(CREME))
    f = ImageFont.truetype(F_BLACK, int(r * 1.5 * S))
    d.text((cx * S, (cy + 1) * S), "?", font=f, anchor="mm", fill=rgb("#0E4A31"))


def chip(img, texto, cx, cy):
    """Etiqueta escura com texto dourado (ex.: '3º', '40°', '+2')."""
    f = ImageFont.truetype(F_BLACK, 21 * S)
    d = ImageDraw.Draw(img)
    w = max(d.textlength(texto, font=f) + 16 * S, 32 * S)
    h = 30 * S
    box = [cx * S - w / 2, (cy - 15) * S, cx * S + w / 2, (cy + 15) * S]
    d.rounded_rectangle([box[0] - 3 * S, box[1] - 3 * S, box[2] + 3 * S, box[3] + 3 * S], radius=11 * S,
                        fill=rgb(CREME))
    d.rounded_rectangle(box, radius=8 * S, fill=rgb(VERDE_ESC))
    d.text((cx * S, (cy + 1) * S), texto, font=f, anchor="mm", fill=rgb(OURO))


def adesivo(img, ch, cx, cy, tam, ang):
    e = emoji(ch, int(tam * S))
    e = com_contorno(e, int(2.6 * S))
    e = e.rotate(ang, resample=Image.BICUBIC, expand=True)
    es, _ = com_sombra(e, 0, int(1.5 * S), 2 * S, 0.30)
    colar_centro(img, es, cx * S, cy * S)


def resultado(img, spec):
    """O que sai da caixa: desenho/emoji com contorno creme e sombra, base dentro da caixa."""
    main = spec["main"]
    esc = spec.get("escala", 1.0)
    cpad = int(2.6 * S) + 4                      # folga que o contorno creme acrescenta de cada lado
    lw, lh = ITEM_BOX[0] * esc * S - 2 * cpad, ITEM_BOX[1] * esc * S - 2 * cpad
    if callable(main):
        im = main()
    else:
        im = emoji(main, 300)
    if spec.get("giro"):
        im = recortar(im.rotate(spec["giro"], resample=Image.BICUBIC, expand=True))
    im = caber(im, int(lw), int(lh))
    im = com_contorno(im, int(2.6 * S))
    ims, pad = com_sombra(im, 0, int(1.5 * S), 2 * S, 0.30)
    x = BX * S - ims.width / 2
    pad += cpad - int(1.0 * S)                   # base visível do contorno fica ~1 px dentro da caixa
    y = ITEM_BASE * S - (ims.height - pad)
    img.alpha_composite(ims, (int(round(x)), int(round(y))))


# ---------------------------------------------------------------- texto
_DM = ImageDraw.Draw(Image.new("L", (10, 10)))


def espaco(f, sw):
    return _DM.textlength(" ", font=f) + ESPACO_EXTRA * sw


def largura_linha(l, f, sw):
    """Largura com contorno, contando o espaço extra entre palavras."""
    pal = l.split(" ")
    return sum(_DM.textlength(p, font=f) for p in pal) + espaco(f, sw) * (len(pal) - 1) + 2 * sw


def medir_fonte(linhas, largura, tam_max, tam_min, arquivo=F_BLACK):
    for tam in range(tam_max, tam_min - 1, -1):
        f = ImageFont.truetype(arquivo, tam * S)
        sw = max(3, round(tam * 0.085)) * S
        if max(largura_linha(l, f, sw) for l in linhas) <= largura * S:
            return tam, f, sw
    raise SystemExit(f"texto não coube nem com {tam_min}px: {linhas}")


def texto_palavras(d, cx, yb, l, f, sw, fill, stroke):
    pal = l.split(" ")
    x = cx - (largura_linha(l, f, sw) - 2 * sw) / 2
    for p in pal:
        d.text((x, yb), p, font=f, anchor="ls", fill=fill, stroke_width=sw, stroke_fill=stroke)
        x += _DM.textlength(p, font=f) + espaco(f, sw)


def desenhar_texto(img, linhas, area, cor_contorno, cores_linha, cor_sombra=None,
                   tam_max=TAM_MAX, tam_min=TAM_MIN, tamanhos=None, arquivo=F_BLACK):
    """1 ou 2 linhas centralizadas, com contorno e sombra dura. Reduz a fonte se precisar.
    Confere se nada passa da área (acento em cima, parêntese/cedilha embaixo)."""
    x0, y0, x1, y1 = area
    d = ImageDraw.Draw(img)
    if tamanhos is None:
        tam, f, sw = medir_fonte(linhas, x1 - x0, tam_max, tam_min, arquivo)
        fontes = [(tam, f, sw)] * len(linhas)
    else:
        fontes = [medir_fonte([l], x1 - x0, t, tam_min, arquivo) for l, t in zip(linhas, tamanhos)]
    caps = [-fo[1].getbbox("H", anchor="ls")[1] for fo in fontes]
    acento = [-fo[1].getbbox("ÊÁÉÍÃ", anchor="ls")[1] for fo in fontes]
    alt = caps[0]
    bases = [caps[0]]
    for i in range(1, len(linhas)):
        alt += caps[i] + (acento[i] - caps[i]) * 0.85 + fontes[i][2] * 1.0
        bases.append(alt)
    cy = (y0 + y1) / 2 * S
    topo = cy - alt / 2
    tem_acento_1 = any(ch in linhas[0] for ch in "ÁÃÉÊÍÓÔÕÚÇÀ")
    if tem_acento_1 and topo - (acento[0] - caps[0]) < y0 * S:
        topo = y0 * S + (acento[0] - caps[0])
    cx = (x0 + x1) / 2 * S
    sombra = max(3, round(fontes[0][0] * 0.07)) * S
    cs = cor_sombra or cor_contorno
    # conferência: caixa real de cada linha (com contorno e sombra) dentro da área
    for i, l in enumerate(linhas):
        tam, f, sw = fontes[i]
        bb = d.textbbox((cx, topo + bases[i]), l, font=f, anchor="ms", stroke_width=sw)
        lx = largura_linha(l, f, sw)
        if (cx - lx / 2 < x0 * S - 1 or cx + lx / 2 > x1 * S + 1 or bb[1] < (y0 - 6) * S
                or bb[3] + sombra > (y1 + 6) * S):
            raise SystemExit(f"texto fora da área: {l!r} {[round(v / S) for v in bb]}")
    for i, l in enumerate(linhas):
        tam, f, sw = fontes[i]
        texto_palavras(d, cx, topo + bases[i] + sombra, l, f, sw, rgb(cs), rgb(cs))
    for i, l in enumerate(linhas):
        tam, f, sw = fontes[i]
        texto_palavras(d, cx, topo + bases[i], l, f, sw, rgb(cores_linha[i]), rgb(cor_contorno))
    return [fo[0] for fo in fontes]


def reduzir(img):
    return img.resize((img.width // S, img.height // S), Image.LANCZOS)


# ---------------------------------------------------------------- peças
def carta(item, paleta_nome, chave_ilustra):
    p = PALETAS[paleta_nome]
    spec = ILUSTRA[chave_ilustra]
    img = etiqueta(p)
    barbante(img)
    caixa_fundo(img)
    # brilhos atrás do resultado
    for (x, y, r) in ((BX - 78, 16, 7), (BX - 66, 50, 4), (BX + 70, 12, 5)):
        brilho(img, x * S, y * S, r * S)
    resultado(img, spec)
    caixa_frente(img)
    if spec.get("sec_esq"):
        adesivo(img, spec["sec_esq"], BX - SEC_DX, 38, 38, 12)
    if spec.get("sec"):
        adesivo(img, spec["sec"], BX + SEC_DX, 36, 42, -12)
    if spec.get("chip"):
        cy = 74 if spec.get("sec") else 50
        chip(img, spec["chip"], BX + SEC_DX + 6, cy)
    tam = desenhar_texto(img, [item["linha1"], item["linha2"]], TEXT_AREA, p["contorno"],
                         (p["txt"], p["txt"]), p.get("sombra_txt"))
    return reduzir(img), tam[0]


def titulo(com_toque=False):
    p = PALETAS["pinheiro"]
    img = etiqueta(p)
    barbante(img)
    caixa_frente(img, fechada=True)
    tampa_e_laco(img)
    selo_interrogacao(img, BX, 82, 12)
    for (x, y, r) in ((BX - 70, 22, 8), (BX - 56, 48, 4), (BX + 66, 16, 6), (BX + 76, 44, 4)):
        brilho(img, x * S, y * S, r * S)
    linhas = [item.strip() for item in ("NO AMIGO SECRETO", "EU VOU GANHAR…")]
    if com_toque:
        desenhar_texto(img, linhas, (70, 98, 478, 190), p["contorno"], (CREME, OURO),
                       tamanhos=(40, 50), tam_min=28)
        pilula_toque(img)
    else:
        desenhar_texto(img, linhas, (70, 102, 478, 224), p["contorno"], (CREME, OURO),
                       tamanhos=(46, 58), tam_min=30)
    return reduzir(img)


def pilula_toque(img):
    """Pílula vermelha (a 'fita') com mãozinha e 'TOQUE PRA ABRIR', presa embaixo."""
    f = ImageFont.truetype(F_BLACK, 17 * S)
    d = ImageDraw.Draw(img)
    txt = "TOQUE PRA ABRIR"
    tw = d.textlength(txt, font=f)
    mao = emoji("👆", 22 * S)
    w = tw + mao.width + 28 * S
    h = 30 * S
    cx, cy = BX * S, 211 * S
    box = [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2]
    d.rounded_rectangle([box[0] - 3 * S, box[1] - 3 * S, box[2] + 3 * S, box[3] + 3 * S], radius=18 * S,
                        fill=rgb("#F5C84C"))
    m, md = mascara(img.size)
    md.rounded_rectangle(box, radius=15 * S, fill=255)
    preencher(img, m, [(0, "#F0414F"), (1, "#B3172A")])
    x = box[0] + 11 * S
    img.alpha_composite(mao, (int(x), int(cy - mao.height / 2)))
    d.text((x + mao.width + 6 * S, cy + 1 * S), txt, font=f, anchor="lm", fill=rgb(CREME))


# ---------------------------------------------------------------- ícones
def _caixa_icone(t, aberta=False, cor_caixa=("#FFD666", "#E3940F"), cor_listra="#FFFFFF"):
    """Caixa de presente grande para o ícone (desenhada em t x t)."""
    img = Image.new("RGBA", (t, t), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x0, x1, y0, y1 = 0.20 * t, 0.80 * t, 0.50 * t, 0.88 * t
    cont = t * 0.016
    d.rounded_rectangle([x0 - cont, y0 - cont, x1 + cont, y1 + cont], radius=t * 0.04, fill=rgb("#3A2406"))
    m, md = mascara((t, t))
    md.rounded_rectangle([x0, y0, x1, y1], radius=t * 0.03, fill=255)
    preencher(img, m, [(0, cor_caixa[0]), (1, cor_caixa[1])], (0.3, 0.7))
    lst, ld = mascara((t, t))
    for k in range(-6, 14):
        xx = x0 + k * t * 0.06
        ld.line([(xx, y0), (xx + t * 0.25, y1)], fill=255, width=int(t * 0.018))
    img.alpha_composite(camada_cor((t, t), cor_listra, inter(lst, m), 0.16))
    fita, fd = mascara((t, t))
    fd.rectangle([0.455 * t, y0, 0.545 * t, y1], fill=255)
    preencher(img, inter(fita, m), [(0, "#FF5361"), (1, "#B3172A")], (1.0, 0.0))
    # tampa
    tx0, tx1, ty0, ty1 = 0.16 * t, 0.84 * t, 0.39 * t, 0.52 * t
    if aberta:
        tampa = Image.new("RGBA", (t, t), (0, 0, 0, 0))
        tdd = ImageDraw.Draw(tampa)
        tdd.rounded_rectangle([tx0 - cont, ty0 - cont, tx1 + cont, ty1 + cont], radius=t * 0.035, fill=rgb("#3A2406"))
        mt, mtd = mascara((t, t))
        mtd.rounded_rectangle([tx0, ty0, tx1, ty1], radius=t * 0.025, fill=255)
        preencher(tampa, mt, [(0, mix(cor_caixa[0], "#FFFFFF", 0.25)), (1, cor_caixa[1])])
        ft, ftd = mascara((t, t))
        ftd.rectangle([0.455 * t, ty0, 0.545 * t, ty1], fill=255)
        preencher(tampa, inter(ft, mt), [(0, "#FF5361"), (1, "#B3172A")], (1.0, 0.0))
        return img, tampa
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([tx0 - cont, ty0 - cont, tx1 + cont, ty1 + cont], radius=t * 0.035, fill=rgb("#3A2406"))
    mt, mtd = mascara((t, t))
    mtd.rounded_rectangle([tx0, ty0, tx1, ty1], radius=t * 0.025, fill=255)
    preencher(img, mt, [(0, mix(cor_caixa[0], "#FFFFFF", 0.25)), (1, cor_caixa[1])])
    ft, ftd = mascara((t, t))
    ftd.rectangle([0.45 * t, ty0, 0.55 * t, ty1], fill=255)
    preencher(img, inter(ft, mt), [(0, "#FF5361"), (1, "#B3172A")], (1.0, 0.0))
    return img, None


def _laco_icone(t, cx, cy, esc=1.0):
    img = Image.new("RGBA", (t, t), (0, 0, 0, 0))
    s = t * esc
    pontas = Image.new("RGBA", (t, t), (0, 0, 0, 0))
    pd = ImageDraw.Draw(pontas)
    for lado in (-1, 1):
        pd.polygon([(cx + lado * 0.02 * s, cy + 0.01 * s), (cx + lado * 0.12 * s, cy + 0.12 * s),
                    (cx + lado * 0.07 * s, cy + 0.14 * s), (cx, cy + 0.03 * s)], fill=rgb("#B3172A"))
    img.alpha_composite(pontas)
    alcas, _ = mascara((t, t))
    for lado in (-1, 1):
        a = Image.new("L", (int(0.30 * s), int(0.19 * s)), 0)
        ImageDraw.Draw(a).ellipse([0, 0, a.width - 1, a.height - 1], fill=255)
        a = a.rotate(lado * 22, resample=Image.BICUBIC, expand=True)
        alcas.paste(255, (int(cx + lado * 0.125 * s - a.width / 2), int(cy - 0.06 * s - a.height / 2)), a)
    cont = alcas.filter(ImageFilter.MaxFilter(int(t * 0.022) | 1))
    img.alpha_composite(camada_cor((t, t), "#4A0812", cont))
    preencher(img, alcas, [(0, "#FF6B78"), (1, "#C21A2E")], (0.2, 0.8))
    for lado in (-1, 1):
        a = Image.new("L", (int(0.15 * s), int(0.08 * s)), 0)
        ImageDraw.Draw(a).ellipse([0, 0, a.width - 1, a.height - 1], fill=255)
        a = a.rotate(lado * 22, resample=Image.BICUBIC, expand=True)
        cam = Image.new("L", (t, t), 0)
        cam.paste(a, (int(cx + lado * 0.115 * s - a.width / 2), int(cy - 0.055 * s - a.height / 2)))
        img.alpha_composite(camada_cor((t, t), "#8E0F22", cam, 0.85))
    d = ImageDraw.Draw(img)
    r = 0.045 * s
    d.ellipse([cx - r - t * 0.01, cy - r - t * 0.04, cx + r + t * 0.01, cy + r - t * 0.02 + t * 0.01], fill=rgb("#4A0812"))
    d.ellipse([cx - r, cy - r - t * 0.03, cx + r, cy + r - t * 0.03], fill=rgb("#E8303F"))
    return img


def _interrogacao(t, tam, fill, stroke, sw):
    lay = Image.new("RGBA", (t, t), (0, 0, 0, 0))
    f = ImageFont.truetype(F_BLACK, int(tam))
    ImageDraw.Draw(lay).text((t / 2, t / 2), "?", font=f, anchor="mm", fill=rgb(fill),
                             stroke_width=int(sw), stroke_fill=rgb(stroke))
    return recortar(lay)


def icone(tam_final=162, estilo="principal"):
    t = 648
    if estilo == "principal":
        img = gradiente_radial(t, t, "#2FA068", "#0A3A24", 0.5, 0.42, 0.80)
        cor_lst = ("#FFFFFF", 0.05)
    else:
        img = gradiente_radial(t, t, "#FFE69A", "#E08A0C", 0.5, 0.40, 0.80)
        cor_lst = ("#FFFFFF", 0.14)
    lst, ld = mascara((t, t))
    for x in range(-t, 2 * t, 54):
        ld.line([(x, 0), (x + t, t)], fill=255, width=20)
    img.alpha_composite(camada_cor((t, t), cor_lst[0], lst, cor_lst[1]))
    d = ImageDraw.Draw(img)
    cont_brilho = "#5E3300" if estilo != "principal" else "#062A1B"
    for (x, y, r) in ((0.15, 0.16, 0.045), (0.86, 0.15, 0.032), (0.87, 0.80, 0.04), (0.12, 0.78, 0.028)):
        brilho(img, x * t, y * t, r * t, OURO if estilo == "principal" else "#FFFFFF", cont_brilho)
    if estilo == "principal":
        cx_, sombra_cor = t / 2, "#021A0F"
        caixa, _ = _caixa_icone(t)
        cs, pad = com_sombra(caixa, 0, int(t * 0.02), int(t * 0.025), 0.45, sombra_cor)
        img.alpha_composite(cs, (-pad, -pad))
        laco = _laco_icone(t, cx_, 0.36 * t, 1.25)
        img.alpha_composite(laco)
        # "?" grande na frente, num selo creme
        d = ImageDraw.Draw(img)
        r = 0.150 * t
        cy = 0.69 * t
        d.ellipse([cx_ - r - t * 0.016, cy - r - t * 0.016, cx_ + r + t * 0.016, cy + r + t * 0.016], fill=rgb("#3A2406"))
        d.ellipse([cx_ - r, cy - r, cx_ + r, cy + r], fill=rgb(CREME))
        q = _interrogacao(t, t * 0.30, "#0E4A31", "#0E4A31", 2)
        colar_centro(img, q, cx_, cy + t * 0.005)
    else:
        # caixa aberta, "?" inteiro saindo de dentro e tampa voando à esquerda (tudo dentro da área segura)
        caixa, tampa = _caixa_icone(t, aberta=True, cor_caixa=("#3FB27A", "#10583A"))
        desloc = int(0.03 * t)                   # caixa um pouco mais baixa que no ícone principal
        cs, pad = com_sombra(caixa, 0, int(t * 0.02), int(t * 0.025), 0.40, "#5E3300")
        rd = ImageDraw.Draw(img)
        qx, qbase = 0.57 * t, 0.505 * t
        # raios de "surpresa" (lado direito; a tampa ocupa o esquerdo)
        for ang in (-58, -30, -2):
            a = math.radians(ang)
            r1, r2 = 0.23 * t, 0.31 * t
            ocx, ocy = qx, 0.31 * t
            p1 = (ocx + r1 * math.cos(a), ocy + r1 * math.sin(a))
            p2 = (ocx + r2 * math.cos(a), ocy + r2 * math.sin(a))
            rd.line([p1, p2], fill=rgb("#5E3300"), width=int(t * 0.040))
            rd.line([p1, p2], fill=rgb("#FFFFFF"), width=int(t * 0.022))
        # boca da caixa (interior)
        yb = 0.50 * t + desloc
        rd.polygon([(0.20 * t, yb), (0.80 * t, yb), (0.74 * t, yb - 0.06 * t), (0.26 * t, yb - 0.06 * t)],
                   fill=rgb("#3A2406"))
        rd.polygon([(0.215 * t, yb - 0.005 * t), (0.785 * t, yb - 0.005 * t), (0.735 * t, yb - 0.048 * t),
                    (0.265 * t, yb - 0.048 * t)], fill=rgb("#0A2F1F"))
        q = _interrogacao(t, t * 0.44, CREME, "#0B3A26", t * 0.022)
        qs, qpad = com_sombra(q, 0, int(t * 0.012), int(t * 0.015), 0.35, "#3A2406")
        img.alpha_composite(qs, (int(qx - qs.width / 2), int(qbase - qs.height + qpad)))
        img.alpha_composite(cs, (-pad, -pad + desloc))
        tb = recortar(tampa)
        tb = tb.resize((int(tb.width * 0.52), int(tb.height * 0.52)), Image.LANCZOS)
        tb = tb.rotate(26, resample=Image.BICUBIC, expand=True)
        tbs, tpad = com_sombra(tb, 0, int(t * 0.015), int(t * 0.02), 0.35, "#5E3300")
        img.alpha_composite(tbs, (int(0.255 * t - tbs.width / 2), int(0.27 * t - tbs.height / 2)))
    out = img.resize((tam_final, tam_final), Image.LANCZOS) if tam_final != t else img
    return out.convert("RGB")


# ---------------------------------------------------------------- prévia
def xadrez(w, h, q=12):
    im = Image.new("RGBA", (w, h), rgb("#FFFFFF"))
    d = ImageDraw.Draw(im)
    for y in range(0, h, q):
        for x in range(0, w, q):
            if (x // q + y // q) % 2:
                d.rectangle([x, y, x + q - 1, y + q - 1], fill=rgb("#DCD9D2"))
    return im


def foto_generica(w, h, tipo):
    """Fundos falsos para testar a leitura."""
    rnd = random.Random(tipo)
    if tipo == "sala":
        im = gradiente(w, h, [(0, "#F4EEE6"), (1, "#D9CFC2")], (0, 1))
        d = ImageDraw.Draw(im)
        d.rectangle([w * 0.58, h * 0.08, w * 0.93, h * 0.40], fill=rgb("#CFE8F7"))
        d.rectangle([w * 0.58, h * 0.08, w * 0.93, h * 0.40], outline=rgb("#FFFFFF"), width=8)
        d.line([(w * 0.755, h * 0.08), (w * 0.755, h * 0.40)], fill=rgb("#FFFFFF"), width=6)
        d.rectangle([0, h * 0.72, w, h], fill=rgb("#B9A58E"))
        d.ellipse([w * 0.05, h * 0.18, w * 0.30, h * 0.40], fill=rgb("#7BAF6A"))
    elif tipo == "noite":
        im = gradiente(w, h, [(0, "#0B0F1E"), (1, "#05060B")], (0, 1))
        d = ImageDraw.Draw(im)
        for _ in range(28):
            x, y, r = rnd.uniform(0, w), rnd.uniform(0, h * 0.7), rnd.uniform(10, 40)
            c = rnd.choice(["#FFB347", "#FFE08A", "#FF7A59", "#C9A0FF"])
            d.ellipse([x - r, y - r, x + r, y + r], fill=rgb(c, rnd.randint(40, 110)))
        im = im.filter(ImageFilter.GaussianBlur(6))
    elif tipo == "pisca":
        # parede escura com pisca-pisca colorido (festa de fim de ano)
        im = gradiente(w, h, [(0, "#2B2420"), (1, "#15110E")], (0, 1))
        d = ImageDraw.Draw(im)
        for fio in range(4):
            y0 = h * (0.08 + 0.17 * fio)
            pts = [(x, y0 + 26 * math.sin(x / w * math.pi * 2 + fio)) for x in range(0, w + 10, 10)]
            d.line(pts, fill=rgb("#3D3A33"), width=3)
            for k, (x, y) in enumerate(pts[::4]):
                c = ["#FFD45A", "#FF5A5F", "#5AD17A", "#59B7FF", "#FF9F43"][(k + fio) % 5]
                d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=rgb(c, 70))
                d.ellipse([x - 6, y - 3, x + 6, y + 13], fill=rgb(c))
        im = im.filter(ImageFilter.GaussianBlur(1.5))
    else:  # papel de presente: fundo bem poluído
        im = Image.new("RGBA", (w, h), rgb("#C8102E"))
        d = ImageDraw.Draw(im)
        for y in range(-40, h + 40, 60):
            for x in range(-40, w + 40, 60):
                off = 30 if (y // 60) % 2 else 0
                estrela4(d, x + off, y, 14, rgb("#FFE08A"))
                d.ellipse([x + off + 22, y + 22, x + off + 32, y + 32], fill=rgb("#FFFFFF"))
        for x in range(0, w, 90):
            d.line([(x, 0), (x + 200, h)], fill=rgb("#1E7A4C", 160), width=14)
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
    im.alpha_composite(p, (int(w / 2 - pw / 2), int(topo_cab - ph - 2)))
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
    fundo = rgb("#F6F3EC")
    COLS, TW, TH = 4, 400, 200
    GX, GY = 36, 64
    MARG = 40
    linhas = math.ceil(len(pecas) / COLS)
    larg = MARG * 2 + COLS * TW + (COLS - 1) * GX
    alt_grade = linhas * (TH + GY)
    alt_icones = 300
    alt_sim = 900
    alt = 140 + alt_grade + alt_icones + alt_sim + 60
    sheet = Image.new("RGBA", (larg, alt), fundo)
    d = ImageDraw.Draw(sheet)
    f_h1 = ImageFont.truetype(F_BLACK, 44)
    f_h2 = ImageFont.truetype(F_XBOLD, 28)
    f_lb = ImageFont.truetype(F_BOLD, 17)
    f_sm = ImageFont.truetype(F_SEMI, 15)
    d.text((MARG, 36), "C06 · Meu amigo secreto — prévia das imagens", font=f_h1, fill=rgb(TINTA))
    d.text((MARG, 92), "Xadrez = transparente. Título e cartas: 512×256 (miniaturas aqui a 400×200). "
                       "Ordem da grade = ordem dos arquivos. Ícone de envio: 162×162.",
           font=f_sm, fill=rgb("#5E5A50"))
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
        d.text((x, y + TH + 8), nome, font=f_lb, fill=rgb(TINTA))
        d.text((x, y + TH + 30), legenda, font=f_sm, fill=rgb("#6E695E"))
    y = y0 + alt_grade + 10
    d.text((MARG, y), "Ícone como aparece no app (cantos arredondados pelo próprio app): 162, 96 e 64 px",
           font=f_h2, fill=rgb(TINTA))
    x = MARG
    y += 50
    for nome, ic in icones:
        x_ini = x
        for tam in (162, 96, 64):
            a = arredondar(ic.resize((tam, tam), Image.LANCZOS))
            sheet.alpha_composite(a, (x, y + (162 - tam)))
            x += tam + 18
        d.text((x_ini, y + 172), nome, font=f_lb, fill=rgb(TINTA))
        x += 60
    for nome, ic in icones:
        ic2 = ic.resize((162, 162), Image.LANCZOS).convert("RGBA")
        dd = ImageDraw.Draw(ic2)
        dd.rectangle([9, 9, 152, 152], outline=rgb("#00E5FF"), width=1)
        sheet.alpha_composite(ic2, (x, y))
        x += 162 + 18
    d.text((x - 2 * 180, y + 172), "linha ciano = área segura 144×144", font=f_sm, fill=rgb("#5E5A50"))
    y = y0 + alt_grade + alt_icones
    d.text((MARG, y), "Simulação sobre fotos genéricas (largura da peça ≈ 66% da tela)", font=f_h2,
           fill=rgb(TINTA))
    y += 50
    x = MARG
    for rot, peca, tipo, cs in sims:
        cel = celular(peca, tipo, cor_sil=cs)
        sheet.alpha_composite(cel, (x, y))
        d.text((x, y + cel.height + 10), rot, font=f_lb, fill=rgb(TINTA))
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

    titulos = {}
    for com_toque, nome in ((False, "titulo.png"), (True, "titulo_toque.png")):
        t = titulo(com_toque)
        titulos[nome] = t
        salvar(t, os.path.join(AQUI, nome))
        salvar(quadrado(t), os.path.join(AQUI, "quadrado_512", nome))
        pecas.append((nome, t, "título" + (" + aviso de toque (padrão)" if com_toque else " (reserva, sem aviso)")))

    tamanhos = {}
    imgs = {}
    for i, item in enumerate(tx["resultados"]):
        cor = ORDEM_CORES[i % len(ORDEM_CORES)]
        im, tam = carta(item, cor, item["n"])
        nome = f"carta_{item['n']:02d}.png"
        salvar(im, os.path.join(AQUI, "cartas", nome))
        salvar(quadrado(im), os.path.join(AQUI, "quadrado_512", "cartas", nome))
        pecas.append((nome, im, f"{item['linha1']} / {item['linha2']} · {tam}px"))
        tamanhos[nome] = tam
        imgs[nome] = im
    n_res = len(tx["resultados"])
    for j, item in enumerate(tx["reservas"]):
        cor = ORDEM_CORES[(n_res + j) % len(ORDEM_CORES)]
        im, tam = carta(item, cor, 100 + item["n"])
        nome = f"reserva_{item['n']:02d}.png"
        salvar(im, os.path.join(AQUI, "reservas", nome))
        salvar(quadrado(im), os.path.join(AQUI, "quadrado_512", "reservas", nome))
        pecas.append((nome, im, f"{item['codigo']} · {item['linha1']} / {item['linha2']} · {tam}px"))
        tamanhos[nome] = tam

    icones = []
    for estilo, sufixo in (("principal", ""), ("alt", "_alt")):
        ic512 = icone(512, estilo)
        ic162 = icone(162, estilo)
        salvar(ic162, os.path.join(AQUI, f"icone{sufixo}_162.png"))
        salvar(ic512, os.path.join(AQUI, f"icone{sufixo}_512.png"))
        icones.append((f"icone{sufixo}_162.png", ic512))
        pecas.append((f"icone{sufixo}_162.png", ic512.convert("RGBA"),
                      "ícone de envio" + (" (alternativo, caixa aberta)" if sufixo else " (principal)")))

    # simulação: título + as cartas de letra menor, em fundos diferentes
    ordem = sorted(imgs, key=lambda n: (tamanhos[n], n))
    sims = [
        ("titulo_toque.png · sala clara", titulos["titulo_toque.png"], "sala", "#3C3A44"),
        (f"{ordem[0]} · fundo escuro", imgs[ordem[0]], "noite", "#7A7488"),
        (f"{ordem[1]} · pisca-pisca", imgs[ordem[1]], "pisca", "#4A4540"),
        ("carta_02.png · papel de presente", imgs["carta_02.png"], "papel", "#2A2830"),
    ]
    salvar(previa(pecas, icones, sims), os.path.join(AQUI, "previa.png"))

    # lista de arquivos
    linhas = []
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


if __name__ == "__main__":
    main()
