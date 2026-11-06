#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C09 · Perrengue no volante: gera TODAS as imagens do efeito (template Blind Rank).

Como rodar (de qualquer pasta):
    python3 gerar.py

Precisa de: Python 3 + Pillow + numpy.
Fontes (as duas sob SIL Open Font License 1.1, as mesmas do efeito-1):
  - Inter Display Black/ExtraBold  -> /usr/share/fonts/opentype/inter/
  - Noto Color Emoji               -> /usr/share/fonts/truetype/noto/NotoColorEmoji.ttf
    (no Pillow só funciona com size=109 e embedded_color=True; renderizado à parte e reduzido)

Os textos vêm de ../textos.json (linha1/linha2 de cada item, título e textos de
interface). Se o redator trocar um texto, basta rodar de novo.

Identidade visual (diferente do efeito-1): "sinalização de trânsito".
  - placas com borda de asfalto + aro branco, listras de advertência nos cantos;
  - cada carta tem uma "janela" com a cena desenhada (céu claro + asfalto com faixa amarela);
  - paleta: amarelo-sinalização, laranja-cone, asfalto e verde-limão refletivo, em rodízio.
    Nada de vermelho+branco, verde+branco, preto+branco nem azul como cor principal.
  - carros, pneu, bateria, volante, cone, mapa etc. são DESENHO PRÓPRIO (formas simples, carro
    genérico visto de lado, sem grade, emblema, placa ou silhueta de modelo real). O emoji Noto
    entra só como "adesivo" de reação (👀 😬 🤔 😩 ...).

Desenha tudo em 3x (S) e reduz com LANCZOS.

Saída (nesta pasta):
  titulo.png ............................ 512x512 título com "1 = PIOR · 10 = DE BOA" (padrão)
  titulo_curto.png ...................... 512x512 título com "1 = PIOR" (se faltar espaço)
  titulo_5_posicoes.png ................. 512x512 título com "1 = PIOR · 5 = DE BOA"
  titulo_sem_subtitulo.png .............. 512x512 só as 3 linhas
  cartas/carta_01..10.png ............... 512x512 os 10 itens da versão padrão (SÓ esses 10 na pasta)
  extras/carta_11..14.png ............... 512x512 itens extras da versão com rodízio (opcional)
  reservas/reserva_01..04.png ........... 512x512 reservas R1..R4
  largo_512x256/... ..................... as mesmas peças em 512x256 (mesma estrutura de pastas)
  marcadores/posicao_01..10.png ......... 256x256 números de posição (só se o template pedir)
  interface/*.png ....................... etiquetas em PT-BR (só se o template tiver texto em inglês)
  icone_162.png, icone_alt_162.png ...... ícones de envio (162x162, área segura 144)
  icone_512.png, icone_alt_512.png ...... os mesmos ícones grandes (referência)
  previa.png ............................ folha de conferência
  lista-de-arquivos.txt ................. lista com tamanhos e pesos
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

S = 3  # desenha em 3x e reduz com LANCZOS (bordas lisas)

# ---------------------------------------------------------------- cores
ASFALTO = "#24222B"     # contorno de tudo
ASFALTO_2 = "#3B3946"   # rua
AMARELO = "#FFD43B"     # faixa da rua / destaque
BRANCO = "#FFFFFF"
GRAFITE_TXT = "#1E1C24"

PALETAS = {
    "amarelo": dict(top="#FFE470", bot="#FFB300", shade="#6E4300", ceu=("#FFFFFF", "#FFF0BA"),
                    texto=BRANCO, listra=BRANCO),
    "laranja": dict(top="#FFAB57", bot="#FF6418", shade="#7A2600", ceu=("#FFFFFF", "#FFE0C8"),
                    texto=BRANCO, listra=BRANCO),
    "asfalto": dict(top="#4C4959", bot="#23212B", shade="#0D0C11", ceu=("#FFFFFF", "#ECE8F5"),
                    texto=AMARELO, listra=AMARELO),
    "lima":    dict(top="#DDF268", bot="#94CB22", shade="#365200", ceu=("#FFFFFF", "#EEF8C9"),
                    texto=BRANCO, listra=BRANCO),
}
ORDEM_CORES = ["amarelo", "laranja", "asfalto", "lima"]

# cor dos carrinhos (genéricos) por cena
VIOLETA = "#8B5CF6"
CORAL = "#FF5E57"
TURQUESA = "#16B8A6"
LARANJA_C = "#FF8A1F"
LILAS = "#B9A8E8"

# ---------------------------------------------------------------- geometria (em 1x)
RIM = 4        # aro branco em volta da borda escura
BORDA = 7      # borda escura (asfalto)
# carta quadrada 512x512
Q_CORPO = (20, 20, 492, 488)
Q_RAIO = 40
Q_PAINEL = (44, 44, 468, 292)
Q_PAINEL_R = 24
Q_TEXTO = (34, 300, 478, 474)
# carta larga 512x256
L_CORPO = (14, 60, 498, 240)
L_RAIO = 30
L_PAINEL = (148, 10, 364, 128)
L_PAINEL_R = 18
L_TEXTO = (28, 132, 484, 234)
PAINEL_BORDA = 4


def rgb(h, a=255):
    if isinstance(h, tuple):
        return h if len(h) == 4 else h + (a,)
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def mix(c1, c2, t):
    a, b = rgb(c1), rgb(c2)
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(4))


# ---------------------------------------------------------------- utilidades
def gradiente(w, h, paradas, direcao=(0.15, 0.85)):
    """paradas = [(pos 0..1, '#hex'), ...]; direcao = peso de x e de y."""
    w, h = int(w), int(h)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    t = (xx / max(w - 1, 1)) * direcao[0] + (yy / max(h - 1, 1)) * direcao[1]
    t = (t - t.min()) / max(t.max() - t.min(), 1e-6)
    out = np.zeros((h, w, 4), np.float32)
    pos = [p for p, _ in paradas]
    cores = [np.array(rgb(c), np.float32) for _, c in paradas]
    for ch in range(4):
        out[..., ch] = np.interp(t, pos, [c[ch] for c in cores])
    return Image.fromarray(out.clip(0, 255).astype(np.uint8), "RGBA")


def camada_cor(size, cor, mascara, alpha_mult=1.0):
    c = rgb(cor)
    lay = Image.new("RGBA", size, c[:3] + (0,))
    a = mascara if alpha_mult == 1.0 else mascara.point(lambda v: int(v * alpha_mult))
    lay.putalpha(a)
    return lay


def uniao(*ms):
    out = np.array(ms[0])
    for m in ms[1:]:
        out = np.maximum(out, np.array(m))
    return Image.fromarray(out)


def intersec(a, b):
    return Image.fromarray(np.minimum(np.array(a), np.array(b)))


def deslocar(m, dx, dy):
    out = Image.new(m.mode, m.size, 0)
    out.paste(m, (int(dx), int(dy)))
    return out


def dilatar(m, px):
    """Engrossa uma máscara em ~px (blur + limiar)."""
    if px <= 0:
        return m
    blur = m.filter(ImageFilter.GaussianBlur(px / 2.0))
    return blur.point(lambda v: 255 if v > 14 else int(v * 18))


def colar(dst, im, x, y):
    """alpha_composite que aceita posição negativa ou fora da borda (recorta)."""
    x, y = int(round(x)), int(round(y))
    sx0, sy0 = max(0, -x), max(0, -y)
    sx1, sy1 = min(im.width, dst.width - x), min(im.height, dst.height - y)
    if sx1 <= sx0 or sy1 <= sy0:
        return
    dst.alpha_composite(im.crop((sx0, sy0, sx1, sy1)), (x + sx0, y + sy0))


def colar_centro(dst, im, cx, cy):
    colar(dst, im, cx - im.width / 2, cy - im.height / 2)


def poli_arred(pts, r, passos=10):
    """Polígono com cantos arredondados (curva de Bézier quadrática em cada canto)."""
    out = []
    n = len(pts)
    for i in range(n):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        v1 = (p0[0] - p1[0], p0[1] - p1[1])
        v2 = (p2[0] - p1[0], p2[1] - p1[1])
        l1 = math.hypot(*v1) or 1
        l2 = math.hypot(*v2) or 1
        rr = min(r, l1 * 0.5, l2 * 0.5)
        a = (p1[0] + v1[0] / l1 * rr, p1[1] + v1[1] / l1 * rr)
        b = (p1[0] + v2[0] / l2 * rr, p1[1] + v2[1] / l2 * rr)
        for k in range(passos + 1):
            t = k / passos
            out.append(((1 - t) ** 2 * a[0] + 2 * (1 - t) * t * p1[0] + t * t * b[0],
                        (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * p1[1] + t * t * b[1]))
    return out


def estrela4(d, cx, cy, r, cor):
    k = r * 0.28
    pts = [(cx, cy - r), (cx + k, cy - k), (cx + r, cy), (cx + k, cy + k),
           (cx, cy + r), (cx - k, cy + k), (cx - r, cy), (cx - k, cy - k)]
    d.polygon(pts, fill=rgb(cor) if isinstance(cor, str) else cor)


def com_contorno(im, px, cor=BRANCO):
    """Contorno de 'adesivo' em volta de uma imagem com alfa."""
    px = max(1, int(px))
    pad = px + 4
    a = Image.new("L", (im.width + 2 * pad, im.height + 2 * pad), 0)
    a.paste(im.split()[3], (pad, pad))
    out = camada_cor(a.size, cor, dilatar(a, px))
    out.alpha_composite(im, (pad, pad))
    return out


def com_sombra(im, dx, dy, raio, alpha=0.28, cor="#000000"):
    pad = int(raio * 3) + int(max(abs(dx), abs(dy)))
    base = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    a = Image.new("L", base.size, 0)
    a.paste(im.split()[3], (pad + int(dx), pad + int(dy)))
    a = a.filter(ImageFilter.GaussianBlur(raio))
    base.alpha_composite(camada_cor(base.size, cor, a, alpha))
    base.alpha_composite(im, (pad, pad))
    return base


# ---------------------------------------------------------------- emoji
_EMOJI_FONT = None


def emoji(ch, tam):
    """Renderiza um emoji Noto (109 px) à parte e redimensiona para caber em tam x tam."""
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


def recolorir(im, cor):
    """Recolore mantendo luz e sombra (ex.: cabeça azul do 🗣 vira laranja)."""
    arr = np.array(im).astype(np.float32)
    lum = (0.299 * arr[..., 0] + 0.587 * arr[..., 1] + 0.114 * arr[..., 2]) / 255.0
    alvo = np.array(rgb(cor)[:3], np.float32)
    base = alvo[None, None, :] * (0.62 + 0.62 * lum[..., None])
    branco = np.clip((lum - 0.82) * 3.0, 0, 1)[..., None]
    novo = base * (1 - branco) + 255 * branco
    arr[..., :3] = np.clip(novo, 0, 255)
    return Image.fromarray(arr.astype(np.uint8), "RGBA")


def adesivo(im, px, girar=0):
    """Emoji/elemento com contorno branco + sombrinha (estilo adesivo)."""
    a = com_contorno(im, px, BRANCO)
    if girar:
        a = a.rotate(girar, resample=Image.BICUBIC, expand=True)
    return com_sombra(a, 0, px * 0.5, px * 0.6, 0.30)


def simbolo(txt, tam, cor=LARANJA_C, girar=0):
    """'?' ou '!!' desenhado em fonte grossa, com contorno escuro e aro branco."""
    tam = int(tam)
    f = ImageFont.truetype(F_BLACK, tam)
    sw = max(2, int(tam * 0.07))
    d0 = ImageDraw.Draw(Image.new("L", (4, 4)))
    bb = d0.textbbox((0, 0), txt, font=f, stroke_width=sw)
    im = Image.new("RGBA", (bb[2] - bb[0] + 8, bb[3] - bb[1] + 8), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((4 - bb[0], 4 - bb[1]), txt, font=f, fill=rgb(cor), stroke_width=sw,
                            stroke_fill=rgb(ASFALTO))
    im = com_contorno(im, max(2, tam * 0.06), BRANCO)
    if girar:
        im = im.rotate(girar, resample=Image.BICUBIC, expand=True)
    return im


# ---------------------------------------------------------------- desenhos próprios
def contorno_escuro(im, px, cor=ASFALTO):
    """Coloca contorno escuro (estilo cartoon) por baixo de uma imagem com alfa já com folga."""
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.alpha_composite(camada_cor(im.size, cor, dilatar(im.split()[3], px)))
    out.alpha_composite(im)
    return out


def carro(L, cor=VIOLETA, vidro="#D9F2FF", farol="#FFF3B0", virar=False, farol_aceso=False):
    """Carrinho genérico de lado (2 volumes, sem grade, sem emblema, sem placa). L = comprimento em px."""
    L = int(L)
    pad = max(4, int(L * 0.06))
    w, h = L + 2 * pad, int(L * 0.54) + 2 * pad

    def P(x, y):
        return (pad + x * L, pad + y * L)

    escuro = mix(cor, "#000000", 0.28)
    claro = mix(cor, "#FFFFFF", 0.40)
    cab = poli_arred([P(0.12, 0.22), P(0.25, 0.045), P(0.62, 0.045), P(0.82, 0.22)], 0.07 * L)
    corpo = [*P(0.02, 0.20), *P(0.98, 0.43)]
    rodas = [(0.25, 0.42), (0.76, 0.42)]
    rr = 0.105
    sil = Image.new("L", (w, h), 0)
    ds = ImageDraw.Draw(sil)
    ds.polygon(cab, fill=255)
    ds.rounded_rectangle(corpo, radius=0.08 * L, fill=255)
    for (x, y) in rodas:
        ds.ellipse([*P(x - rr, y - rr), *P(x + rr, y + rr)], fill=255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    if farol_aceso:  # brilho amarelo na frente e atrás (alarme)
        g = Image.new("L", (w, h), 0)
        gd = ImageDraw.Draw(g)
        for x in (0.97, 0.03):
            gd.ellipse([*P(x - 0.12, 0.15), *P(x + 0.12, 0.38)], fill=255)
        g = g.filter(ImageFilter.GaussianBlur(L * 0.04))
        im.alpha_composite(camada_cor((w, h), "#FFE14D", g, 0.9))
    im.alpha_composite(camada_cor((w, h), ASFALTO, dilatar(sil, max(2, L * 0.032))))
    d = ImageDraw.Draw(im)
    d.polygon(cab, fill=rgb(cor))
    d.rounded_rectangle(corpo, radius=0.08 * L, fill=rgb(cor))
    d.rounded_rectangle([*P(0.05, 0.215), *P(0.95, 0.243)], radius=0.014 * L, fill=claro)
    d.rounded_rectangle([*P(0.02, 0.355), *P(0.98, 0.43)], radius=0.035 * L, fill=escuro)
    d.rounded_rectangle([*P(0.004, 0.33), *P(0.09, 0.40)], radius=0.02 * L, fill=rgb("#4A4756"))
    d.rounded_rectangle([*P(0.91, 0.33), *P(0.996, 0.40)], radius=0.02 * L, fill=rgb("#4A4756"))
    for (x, y) in rodas:
        d.pieslice([*P(x - 0.13, y - 0.13), *P(x + 0.13, y + 0.13)], 180, 360, fill=rgb(ASFALTO_2))
    jt = poli_arred([P(0.185, 0.205), P(0.275, 0.085), P(0.43, 0.085), P(0.43, 0.205)], 0.02 * L)
    jf = poli_arred([P(0.465, 0.205), P(0.465, 0.085), P(0.605, 0.085), P(0.745, 0.205)], 0.02 * L)
    d.polygon(jt, fill=rgb(vidro))
    d.polygon(jf, fill=rgb(vidro))
    d.polygon([P(0.53, 0.195), P(0.59, 0.098), P(0.62, 0.098), P(0.56, 0.195)], fill=rgb(BRANCO))
    d.polygon([P(0.30, 0.195), P(0.345, 0.098), P(0.365, 0.098), P(0.32, 0.195)], fill=rgb(BRANCO, 170))
    d.line([P(0.447, 0.215), P(0.447, 0.355)], fill=escuro, width=max(1, int(L * 0.008)))
    d.rounded_rectangle([*P(0.50, 0.258), *P(0.56, 0.274)], radius=0.008 * L, fill=escuro)
    d.rounded_rectangle([*P(0.925, 0.245), *P(0.985, 0.29)], radius=0.015 * L,
                        fill=rgb("#FFF07A" if farol_aceso else farol))
    d.rounded_rectangle([*P(0.015, 0.245), *P(0.06, 0.29)], radius=0.012 * L,
                        fill=rgb("#FFC21A" if farol_aceso else "#FF8A3D"))
    for (x, y) in rodas:
        d.ellipse([*P(x - rr, y - rr), *P(x + rr, y + rr)], fill=rgb("#2A2832"))
        d.ellipse([*P(x - 0.056, y - 0.056), *P(x + 0.056, y + 0.056)], fill=rgb("#D3D1DC"))
        d.ellipse([*P(x - 0.022, y - 0.022), *P(x + 0.022, y + 0.022)], fill=rgb("#8D8A99"))
    if virar:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    return im


def cone(H):
    """Cone de trânsito laranja com faixas brancas."""
    H = int(H)
    pad = max(3, int(H * 0.08))
    w = int(H * 0.8) + 2 * pad
    im = Image.new("RGBA", (w, H + 2 * pad), (0, 0, 0, 0))

    def P(x, y):
        return (pad + x * H, pad + y * H)

    def borda(y):
        f = (y - 0.04) / 0.84
        return 0.31 + (0.11 - 0.31) * f, 0.49 + (0.69 - 0.49) * f

    corpo = poli_arred([P(0.31, 0.04), P(0.49, 0.04), P(0.69, 0.88), P(0.11, 0.88)], 0.05 * H)
    base = [*P(0.02, 0.85), *P(0.78, 0.99)]
    sil = Image.new("L", im.size, 0)
    ds = ImageDraw.Draw(sil)
    ds.polygon(corpo, fill=255)
    ds.rounded_rectangle(base, radius=0.04 * H, fill=255)
    im.alpha_composite(camada_cor(im.size, ASFALTO, dilatar(sil, max(2, H * 0.05))))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(base, radius=0.04 * H, fill=rgb("#4A4756"))
    d.polygon(corpo, fill=rgb("#FF7A1A"))
    for y0, y1 in ((0.30, 0.42), (0.58, 0.70)):
        a0, b0 = borda(y0)
        a1, b1 = borda(y1)
        d.polygon([P(a0, y0), P(b0, y0), P(b1, y1), P(a1, y1)], fill=rgb(BRANCO))
    a0, _ = borda(0.1)
    a1, _ = borda(0.8)
    d.line([P(a0 + 0.06, 0.1), P(a1 + 0.08, 0.8)], fill=rgb("#FFB070"), width=max(1, int(H * 0.03)))
    return im


def pneu_furado(D):
    """Pneu murcho (fundo achatado) com um prego espetado."""
    D = int(D)
    R = D / 2
    pad = int(D * 0.16)
    w, h = int(D * 1.2) + 2 * pad, D + 2 * pad
    cx, cy = w / 2, pad + R

    def forma(esc=1.0, dy=0.0):
        pts = []
        for k in range(200):
            t = 2 * math.pi * k / 200
            s = math.sin(t)
            x = cx + esc * R * math.cos(t) * (1 + 0.13 * max(0.0, s) ** 3)
            y = cy + dy + min(esc * R * s, 0.80 * R)
            pts.append((x, y))
        return pts

    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    # sombra no chão
    sh = Image.new("L", (w, h), 0)
    ImageDraw.Draw(sh).ellipse([cx - 0.75 * R, cy + 0.70 * R, cx + 0.75 * R, cy + 0.92 * R], fill=150)
    im.alpha_composite(camada_cor((w, h), "#000000", sh.filter(ImageFilter.GaussianBlur(R * 0.06)), 0.5))
    sil = Image.new("L", (w, h), 0)
    ImageDraw.Draw(sil).polygon(forma(), fill=255)
    # prego (cabeça fora do pneu, no alto à direita)
    ang = math.radians(-48)
    hx, hy = cx + 1.10 * R * math.cos(ang), cy + 1.10 * R * math.sin(ang)
    bx, by = cx + 0.90 * R * math.cos(ang), cy + 0.90 * R * math.sin(ang)
    prego = Image.new("L", (w, h), 0)
    pd = ImageDraw.Draw(prego)
    pd.line([(bx, by), (hx, hy)], fill=255, width=int(R * 0.07))
    perp = ang + math.pi / 2
    k = R * 0.13
    pd.line([(hx + k * math.cos(perp), hy + k * math.sin(perp)), (hx - k * math.cos(perp), hy - k * math.sin(perp))],
            fill=255, width=int(R * 0.08))
    im.alpha_composite(camada_cor((w, h), ASFALTO, dilatar(uniao(sil, prego), max(2, D * 0.03))))
    d = ImageDraw.Draw(im)
    d.polygon(forma(), fill=rgb("#2E2C36"))
    # brilho do pneu
    d.arc([cx - 0.88 * R, cy - 0.88 * R, cx + 0.88 * R, cy + 0.88 * R], 195, 275, fill=rgb("#55525F"),
          width=int(R * 0.08))
    # sulcos
    for i in range(26):
        t = 2 * math.pi * i / 26
        if math.sin(t) > 0.45:
            continue
        r1, r2 = 0.83 * R, 0.96 * R
        d.line([(cx + r1 * math.cos(t), cy + r1 * math.sin(t)), (cx + r2 * math.cos(t), cy + r2 * math.sin(t))],
               fill=rgb("#4A4756"), width=max(1, int(R * 0.05)))
    # roda (aro) — um pouco abaixada porque o pneu murchou
    rc = (cx, cy + 0.05 * R)
    rr = 0.50 * R
    d.ellipse([rc[0] - rr, rc[1] - rr, rc[0] + rr, rc[1] + rr], fill=rgb("#D7D5E0"))
    d.ellipse([rc[0] - rr * 0.78, rc[1] - rr * 0.78, rc[0] + rr * 0.78, rc[1] + rr * 0.78], fill=rgb("#B4B1C2"))
    for i in range(5):
        t = -math.pi / 2 + 2 * math.pi * i / 5
        px, py = rc[0] + rr * 0.45 * math.cos(t), rc[1] + rr * 0.45 * math.sin(t)
        d.ellipse([px - rr * 0.09, py - rr * 0.09, px + rr * 0.09, py + rr * 0.09], fill=rgb("#6E6B7C"))
    d.ellipse([rc[0] - rr * 0.2, rc[1] - rr * 0.2, rc[0] + rr * 0.2, rc[1] + rr * 0.2], fill=rgb("#8D8A99"))
    # prego por cima
    d.line([(bx, by), (hx, hy)], fill=rgb("#C9C6D3"), width=int(R * 0.05))
    d.line([(hx + k * math.cos(perp), hy + k * math.sin(perp)), (hx - k * math.cos(perp), hy - k * math.sin(perp))],
           fill=rgb("#DCDAE4"), width=int(R * 0.06))
    return im


def bateria(L):
    """Bateria de carro genérica, com o marcador de carga vazio."""
    L = int(L)
    pad = max(4, int(L * 0.07))
    top = pad + int(L * 0.10)
    w, h = L + 2 * pad, top + int(L * 0.66) + pad

    def P(x, y):
        return (pad + x * L, top + y * L)

    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sil = Image.new("L", (w, h), 0)
    ds = ImageDraw.Draw(sil)
    ds.rounded_rectangle([*P(0.0, 0.04), *P(1.0, 0.66)], radius=0.06 * L, fill=255)
    ds.rounded_rectangle([*P(-0.02, 0.0), *P(1.02, 0.15)], radius=0.04 * L, fill=255)
    for x0 in (0.15, 0.70):
        ds.rounded_rectangle([*P(x0, -0.08), *P(x0 + 0.15, 0.03)], radius=0.03 * L, fill=255)
    im.alpha_composite(camada_cor((w, h), ASFALTO, dilatar(sil, max(2, L * 0.03))))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([*P(0.0, 0.04), *P(1.0, 0.66)], radius=0.06 * L, fill=rgb("#45424F"))
    d.rounded_rectangle([*P(0.0, 0.50), *P(1.0, 0.66)], radius=0.06 * L, fill=rgb("#38353F"))
    d.rounded_rectangle([*P(-0.02, 0.0), *P(1.02, 0.15)], radius=0.04 * L, fill=rgb("#5E5B6A"))
    d.rounded_rectangle([*P(0.0, 0.01), *P(1.0, 0.045)], radius=0.02 * L, fill=rgb("#7A7787"))
    for x0, cor in ((0.15, "#FF5A4E"), (0.70, "#6A6777")):
        d.rounded_rectangle([*P(x0, -0.08), *P(x0 + 0.15, 0.03)], radius=0.03 * L, fill=rgb(cor))
        d.rounded_rectangle([*P(x0 + 0.02, -0.07), *P(x0 + 0.13, -0.035)], radius=0.015 * L,
                            fill=mix(cor, BRANCO, 0.4))
    # + e −
    lw = 0.035 * L
    cxp, cyp = P(0.225, 0.26)
    d.rectangle([cxp - 0.06 * L, cyp - lw / 2, cxp + 0.06 * L, cyp + lw / 2], fill=rgb(BRANCO))
    d.rectangle([cxp - lw / 2, cyp - 0.06 * L, cxp + lw / 2, cyp + 0.06 * L], fill=rgb(BRANCO))
    cxm, cym = P(0.775, 0.26)
    d.rectangle([cxm - 0.06 * L, cym - lw / 2, cxm + 0.06 * L, cym + lw / 2], fill=rgb(BRANCO))
    # etiqueta com marcador de carga vazio
    d.rounded_rectangle([*P(0.12, 0.36), *P(0.88, 0.58)], radius=0.04 * L, fill=rgb("#F4F2F8"))
    d.rounded_rectangle([*P(0.22, 0.40), *P(0.72, 0.54)], radius=0.02 * L, outline=rgb(ASFALTO),
                        width=max(2, int(L * 0.025)))
    d.rounded_rectangle([*P(0.72, 0.435), *P(0.77, 0.505)], radius=0.01 * L, fill=rgb(ASFALTO))
    d.rounded_rectangle([*P(0.245, 0.425), *P(0.30, 0.515)], radius=0.01 * L, fill=rgb("#FF3B30"))
    return im


def volante(D, aro="#2E2C37", miolo="#4D4A58", linha=ASFALTO, brilho=None):
    """Volante genérico: aro + 3 raios + centro LISO (nada que pareça emblema)."""
    D = int(D)
    R = D / 2
    pad = max(4, int(D * 0.06))
    w = D + 2 * pad
    c = w / 2

    def forma_raios(dd, fill):
        dd.polygon(poli_arred([(c - 0.30 * R, c - 0.10 * R), (c - 0.86 * R, c - 0.02 * R),
                               (c - 0.86 * R, c + 0.24 * R), (c - 0.30 * R, c + 0.30 * R)], 0.05 * R), fill=fill)
        dd.polygon(poli_arred([(c + 0.30 * R, c - 0.10 * R), (c + 0.86 * R, c - 0.02 * R),
                               (c + 0.86 * R, c + 0.24 * R), (c + 0.30 * R, c + 0.30 * R)], 0.05 * R), fill=fill)
        dd.polygon(poli_arred([(c - 0.17 * R, c + 0.22 * R), (c + 0.17 * R, c + 0.22 * R),
                               (c + 0.12 * R, c + 0.86 * R), (c - 0.12 * R, c + 0.86 * R)], 0.05 * R), fill=fill)

    sil = Image.new("L", (w, w), 0)
    ds = ImageDraw.Draw(sil)
    ds.ellipse([c - R, c - R, c + R, c + R], fill=255)
    ds.ellipse([c - 0.76 * R, c - 0.76 * R, c + 0.76 * R, c + 0.76 * R], fill=0)
    forma_raios(ds, 255)
    ds.rounded_rectangle([c - 0.36 * R, c - 0.27 * R, c + 0.36 * R, c + 0.37 * R], radius=0.2 * R, fill=255)
    im = Image.new("RGBA", (w, w), (0, 0, 0, 0))
    im.alpha_composite(camada_cor((w, w), linha, dilatar(sil, max(2, D * 0.035))))
    corpo = Image.new("RGBA", (w, w), rgb(aro))
    corpo.putalpha(sil)
    im.alpha_composite(corpo)
    d = ImageDraw.Draw(im)
    claro = mix(aro, BRANCO, 0.30)
    escuro = mix(aro, "#000000", 0.25)
    # volume do aro
    d.arc([c - 0.88 * R, c - 0.88 * R, c + 0.88 * R, c + 0.88 * R], 200, 300, fill=claro, width=int(0.07 * R))
    d.arc([c - 0.88 * R, c - 0.88 * R, c + 0.88 * R, c + 0.88 * R], 20, 120, fill=escuro, width=int(0.07 * R))
    # pegadas (texturinha nas posições 9h15)
    for a in (150, 160, 170, 10, 20, 30):
        t = math.radians(a + 180)
        d.line([(c + 0.80 * R * math.cos(t), c + 0.80 * R * math.sin(t)),
                (c + 0.96 * R * math.cos(t), c + 0.96 * R * math.sin(t))], fill=escuro, width=max(1, int(R * 0.03)))
    # centro liso
    d.rounded_rectangle([c - 0.36 * R, c - 0.27 * R, c + 0.36 * R, c + 0.37 * R], radius=0.2 * R, fill=rgb(miolo))
    d.rounded_rectangle([c - 0.30 * R, c - 0.22 * R, c + 0.30 * R, c - 0.12 * R], radius=0.05 * R,
                        fill=mix(miolo, BRANCO, 0.10))
    if brilho:
        estrela4(d, c - 0.55 * R, c - 0.58 * R, 0.12 * R, rgb(brilho))
    return im


def gota(H, c1="#A6EBFF", c2="#2F9BEA"):
    """Gota de suor (desenho próprio) com contorno escuro e brilho."""
    H = int(H)
    W = H * 0.70
    pad = max(4, int(H * 0.08))
    w, h = int(W) + 2 * pad, H + 2 * pad
    cx = w / 2
    r = W / 2
    cyc = pad + H - r
    dist = cyc - pad
    phi = math.acos(r / dist)
    a0 = math.atan2(-math.cos(phi), math.sin(phi))
    a1 = math.pi - a0
    pts = [(cx, pad)]
    for k in range(41):
        a = a0 + (a1 - a0) * k / 40
        pts.append((cx + r * math.cos(a), cyc + r * math.sin(a)))
    pts = poli_arred(pts, H * 0.03, 4)
    sil = Image.new("L", (w, h), 0)
    ImageDraw.Draw(sil).polygon(pts, fill=255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    im.alpha_composite(camada_cor((w, h), ASFALTO, dilatar(sil, max(2, H * 0.06))))
    g = gradiente(w, h, [(0, c1), (1, c2)], (0.25, 0.75))
    g.putalpha(sil)
    im.alpha_composite(g)
    d = ImageDraw.Draw(im)
    d.ellipse([cx - r * 0.55, cyc - r * 0.35, cx - r * 0.15, cyc + r * 0.35], fill=rgb(BRANCO, 230))
    d.ellipse([cx - r * 0.12, cyc - r * 0.62, cx + r * 0.04, cyc - r * 0.46], fill=rgb(BRANCO, 230))
    return im


def seta_pisca(L, fill="#E9E6EF", borda=LARANJA_C):
    """Setinha de pisca-pisca APAGADA (cinza claro com contorno laranja)."""
    L = int(L)
    H = L * 0.72
    pad = max(4, int(L * 0.08))
    w, h = L + 2 * pad, int(H) + 2 * pad

    def P(x, y):
        return (pad + x * L, pad + y * H)

    pts = poli_arred([P(0, 0.33), P(0.50, 0.33), P(0.50, 0.04), P(1, 0.5), P(0.50, 0.96), P(0.50, 0.67),
                      P(0, 0.67)], 0.05 * L)
    sil = Image.new("L", (w, h), 0)
    ImageDraw.Draw(sil).polygon(pts, fill=255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    im.alpha_composite(camada_cor((w, h), ASFALTO, dilatar(sil, max(3, L * 0.11))))
    im.alpha_composite(camada_cor((w, h), borda, dilatar(sil, max(2, L * 0.065))))
    lay = Image.new("RGBA", (w, h), rgb(fill))
    lay.putalpha(sil)
    im.alpha_composite(lay)
    return im


def balao(w, h, texto="!!", cor_txt=LARANJA_C):
    """Balão de fala com rabicho embaixo à esquerda."""
    w, h = int(w), int(h)
    pad = max(4, int(h * 0.1))
    W, H = w + 2 * pad, int(h * 1.35) + 2 * pad
    sil = Image.new("L", (W, H), 0)
    ds = ImageDraw.Draw(sil)
    ds.rounded_rectangle([pad, pad, pad + w, pad + h], radius=h * 0.45, fill=255)
    ds.polygon([(pad + w * 0.22, pad + h * 0.8), (pad + w * 0.42, pad + h * 0.8), (pad + w * 0.12, pad + h * 1.33)],
               fill=255)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    im.alpha_composite(camada_cor((W, H), ASFALTO, dilatar(sil, max(2, h * 0.08))))
    lay = Image.new("RGBA", (W, H), rgb(BRANCO))
    lay.putalpha(sil)
    im.alpha_composite(lay)
    f = ImageFont.truetype(F_BLACK, int(h * 0.72))
    ImageDraw.Draw(im).text((pad + w / 2, pad + h * 0.53), texto, font=f, anchor="mm", fill=rgb(cor_txt))
    return im


def seta_circular(D, cor=LARANJA_C, ini=40, fim=320):
    """Setinha dando a volta (recalculando)."""
    D = int(D)
    pad = max(4, int(D * 0.16))
    w = D + 2 * pad
    c = w / 2
    R = D / 2
    esp = D * 0.15
    sil = Image.new("L", (w, w), 0)
    ds = ImageDraw.Draw(sil)
    ds.arc([c - R + esp / 2, c - R + esp / 2, c + R - esp / 2, c + R - esp / 2], ini, fim, fill=255, width=int(esp))
    a = math.radians(fim)
    rm = R - esp / 2
    px, py = c + rm * math.cos(a), c + rm * math.sin(a)
    tx, ty = -math.sin(a), math.cos(a)  # tangente (sentido horário)
    nx, ny = math.cos(a), math.sin(a)
    k = esp * 1.25
    ds.polygon([(px + nx * k, py + ny * k), (px - nx * k, py - ny * k), (px + tx * k * 1.4, py + ty * k * 1.4)],
               fill=255)
    im = Image.new("RGBA", (w, w), (0, 0, 0, 0))
    im.alpha_composite(camada_cor((w, w), ASFALTO, dilatar(sil, max(2, D * 0.06))))
    lay = Image.new("RGBA", (w, w), rgb(cor))
    lay.putalpha(sil)
    im.alpha_composite(lay)
    return im


def mapa(L):
    """Mapa genérico dobrado em 4 (sem nome, sem marca, sem tela de aplicativo)."""
    L = int(L)
    H = L * 0.62
    pad = max(4, int(L * 0.05))
    w, h = L + 2 * pad, int(H) + 2 * pad

    def P(x, y):
        return (pad + x * L, pad + y * H)

    tops = [0.0, 0.08, 0.0, 0.08, 0.0]
    xs = [0.0, 0.25, 0.5, 0.75, 1.0]
    paineis = []
    for i in range(4):
        paineis.append([P(xs[i], tops[i]), P(xs[i + 1], tops[i + 1]), P(xs[i + 1], tops[i + 1] + 0.92),
                        P(xs[i], tops[i] + 0.92)])
    sil = Image.new("L", (w, h), 0)
    ds = ImageDraw.Draw(sil)
    for p in paineis:
        ds.polygon(p, fill=255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    im.alpha_composite(camada_cor((w, h), ASFALTO, dilatar(sil, max(2, L * 0.03))))
    base = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(base)
    for i, p in enumerate(paineis):
        d.polygon(p, fill=rgb("#FFF6DC" if i % 2 == 0 else "#EFE2BE"))
    # parque, rio e ruas genéricas
    d.ellipse([*P(0.05, 0.50), *P(0.30, 0.86)], fill=rgb("#BFE3A0"))
    d.line([P(0.0, 0.30), P(0.35, 0.36), P(0.62, 0.22), P(1.0, 0.30)], fill=rgb("#A9DDF2"), width=int(L * 0.035))
    for x in (0.18, 0.44, 0.70, 0.88):
        d.line([P(x, 0.0), P(x + 0.04, 1.0)], fill=rgb(BRANCO), width=int(L * 0.02))
    d.line([P(0.0, 0.66), P(1.0, 0.60)], fill=rgb(BRANCO), width=int(L * 0.02))
    # rota tracejada que dá voltas
    rota = []
    for k in range(60):
        t = k / 59
        x = 0.10 + 0.62 * t
        y = 0.75 - 0.35 * t + 0.13 * math.sin(t * 2 * math.pi * 1.6)
        rota.append(P(x, y))
    for k in range(0, len(rota) - 3, 5):
        d.line(rota[k:k + 3], fill=rgb("#FF4D3D"), width=int(L * 0.028))
    base.putalpha(intersec(base.split()[3], sil))
    im.alpha_composite(base)
    # sombras das dobras
    d = ImageDraw.Draw(im)
    for i in (1, 3):
        d.line([P(xs[i], tops[i]), P(xs[i], tops[i] + 0.92)], fill=rgb("#C9B98F"), width=max(1, int(L * 0.012)))
    return im


def placa_volante(D):
    """Placa de advertência (losango amarelo) com volante e gota de suor: emblema do título."""
    D = int(D)
    pad = int(D * 0.12)
    w = D + 2 * pad
    c = w / 2

    def losango(hd, r):
        return poli_arred([(c, c - hd), (c + hd, c), (c, c + hd), (c - hd, c)], r)

    hd = D / 2
    im = Image.new("RGBA", (w, w), (0, 0, 0, 0))
    m_rim = Image.new("L", (w, w), 0)
    ImageDraw.Draw(m_rim).polygon(losango(hd + RIM * S * 1.2, D * 0.10), fill=255)
    m_borda = Image.new("L", (w, w), 0)
    ImageDraw.Draw(m_borda).polygon(losango(hd, D * 0.09), fill=255)
    m_corpo = Image.new("L", (w, w), 0)
    ImageDraw.Draw(m_corpo).polygon(losango(hd - D * 0.045, D * 0.08), fill=255)
    m_linha = Image.new("L", (w, w), 0)
    dl = ImageDraw.Draw(m_linha)
    dl.polygon(losango(hd - D * 0.085, D * 0.065), fill=255)
    dl.polygon(losango(hd - D * 0.105, D * 0.06), fill=0)
    im.alpha_composite(camada_cor((w, w), "#000000", deslocar(m_rim, 0, D * 0.03).filter(
        ImageFilter.GaussianBlur(D * 0.03)), 0.35))
    im.alpha_composite(camada_cor((w, w), BRANCO, m_rim))
    im.alpha_composite(camada_cor((w, w), ASFALTO, m_borda))
    g = gradiente(w, w, [(0, "#FFE680"), (1, "#FFBE0B")], (0.3, 0.7))
    g.putalpha(m_corpo)
    im.alpha_composite(g)
    im.alpha_composite(camada_cor((w, w), ASFALTO, m_linha))
    v = volante(D * 0.50, aro=ASFALTO, miolo="#4D4A58", linha=ASFALTO).rotate(-10, resample=Image.BICUBIC)
    colar_centro(im, v, c, c + D * 0.03)
    gt = gota(D * 0.27)
    colar_centro(im, gt, c + D * 0.30, c - D * 0.19)
    return im


# ---------------------------------------------------------------- cenas
class Cena:
    """Canvas da cena. Unidade u = 1% da altura. x vai de -80 a +80 (seguro) a partir do centro."""

    def __init__(self, w, h):
        self.W, self.H = int(w), int(h)
        self.u = self.H / 100.0
        self.img = Image.new("RGBA", (self.W, self.H), (0, 0, 0, 0))

    @property
    def d(self):
        return ImageDraw.Draw(self.img)

    def X(self, x):
        return self.W / 2 + x * self.u

    def Y(self, y):
        return y * self.u

    def L(self, v):
        return v * self.u

    def P(self, x, y):
        return (self.X(x), self.Y(y))

    def colar(self, im, x, y):
        colar_centro(self.img, im, self.X(x), self.Y(y))

    def colar_base(self, im, x, yb):
        bb = im.split()[3].point(lambda v: 255 if v > 128 else 0).getbbox()
        colar(self.img, im, self.X(x) - (bb[0] + bb[2]) / 2, self.Y(yb) - bb[3])

    def adesivo(self, ch, x, y, tam, girar=0, cor=None):
        e = emoji(ch, self.L(tam))
        if cor:
            e = recolorir(e, cor)
        self.colar(adesivo(e, max(3, self.L(1.3)), girar), x, y)


def fundo_ceu(c, cores):
    c.img.alpha_composite(gradiente(c.W, c.H, [(0, cores[0]), (1, cores[1])], (0, 1)))


def fundo_rua(c, y0=78, cor=ASFALTO_2, faixa=AMARELO, meio_fio="#9C98AA"):
    d = c.d
    d.rectangle([0, c.Y(y0), c.W, c.H], fill=rgb(cor))
    d.rectangle([0, c.Y(y0), c.W, c.Y(y0) + c.L(2.4)], fill=rgb(meio_fio))
    ym = (y0 + 2.4 + 100) / 2
    x = -110
    while x < 110:
        d.rounded_rectangle([c.X(x), c.Y(ym) - c.L(1.4), c.X(x + 13), c.Y(ym) + c.L(1.4)], radius=c.L(1.3),
                            fill=rgb(faixa))
        x += 24


def chao_sombra(c, x, y, larg):
    sh = Image.new("L", (c.W, c.H), 0)
    ImageDraw.Draw(sh).ellipse([c.X(x - larg / 2), c.Y(y - 2.2), c.X(x + larg / 2), c.Y(y + 2.2)], fill=160)
    c.img.alpha_composite(camada_cor((c.W, c.H), "#000000", sh.filter(ImageFilter.GaussianBlur(c.L(1.2))), 0.45))


def brilhos(c, pts, cor=BRANCO):
    d = c.d
    for (x, y, r) in pts:
        estrela4(d, c.X(x), c.Y(y), c.L(r), rgb(ASFALTO))
        estrela4(d, c.X(x), c.Y(y), c.L(r * 0.72), rgb(cor))


def cena_baliza(c, pal):
    fundo_ceu(c, pal["ceu"])
    fundo_rua(c, 74)
    for x in (-64, 64):
        chao_sombra(c, x, 87, 18)
        c.colar_base(cone(c.L(28)), x, 88)
    chao_sombra(c, 0, 89, 66)
    c.colar_base(carro(c.L(82), VIOLETA), 0, 90)
    # plateia espiando de cima
    for x, y, s, g in ((-52, 15, 26, 6), (0, 11, 28, 0), (52, 15, 26, -6)):
        c.adesivo("👀", x, y, s, girar=g)


def cena_pneu(c, pal):
    fundo_ceu(c, pal["ceu"])
    fundo_rua(c, 80)
    c.colar_base(pneu_furado(c.L(66)), -8, 90)
    c.adesivo("💨", 46, 18, 20, girar=-10)
    c.adesivo("❌", 50, 62, 30)


def cena_poca(c, pal):
    fundo_ceu(c, pal["ceu"])
    d = c.d
    topo = 58
    # corte do chão: asfalto + terra
    d.rectangle([0, c.Y(topo), c.W, c.H], fill=rgb("#9A6B47"))
    d.rectangle([0, c.Y(topo), c.W, c.Y(topo + 10)], fill=rgb(ASFALTO_2))
    for x in (-74, -50, 44, 68):
        d.rounded_rectangle([c.X(x), c.Y(topo + 4) - c.L(1.1), c.X(x + 10), c.Y(topo + 4) + c.L(1.1)],
                            radius=c.L(1), fill=rgb(AMARELO))
    for (x, y, r) in ((-66, 80, 2.2), (-40, 92, 1.6), (52, 84, 2.4), (70, 94, 1.5), (-58, 95, 1.4)):
        d.ellipse([c.X(x - r), c.Y(y - r), c.X(x + r), c.Y(y + r)], fill=rgb("#7E5538"))
    # buraco fundo cheio d'água
    buraco = poli_arred([c.P(-34, topo), c.P(34, topo), c.P(30, 66), c.P(36, 74), c.P(27, 84), c.P(30, 92),
                         c.P(14, 99), c.P(-12, 98), c.P(-28, 92), c.P(-25, 82), c.P(-35, 73), c.P(-29, 65)],
                        c.L(4))
    m = Image.new("L", (c.W, c.H), 0)
    ImageDraw.Draw(m).polygon(buraco, fill=255)
    c.img.alpha_composite(camada_cor((c.W, c.H), ASFALTO, dilatar(m, c.L(1.6))))
    agua = gradiente(c.W, c.H, [(0, "#9FE2FF"), (0.55, "#3E9BE0"), (1, "#1D4E9E")], (0, 1))
    agua.putalpha(m)
    c.img.alpha_composite(agua)
    d = c.d
    for (x, y, r) in ((-8, 72, 2.2), (6, 82, 1.6), (-4, 91, 1.2), (12, 66, 1.3)):
        d.ellipse([c.X(x - r), c.Y(y - r), c.X(x + r), c.Y(y + r)], outline=rgb(BRANCO, 200),
                  width=max(1, int(c.L(0.6))))
    # espelho d'água (parecia rasinha)
    d.rounded_rectangle([c.X(-33), c.Y(topo) - c.L(1.6), c.X(33), c.Y(topo) + c.L(1.6)], radius=c.L(1.6),
                        fill=rgb("#CFF3FF"), outline=rgb(ASFALTO), width=max(1, int(c.L(0.7))))
    # carro chegando (nariz pra baixo) + respingo
    car = carro(c.L(58), CORAL).rotate(-13, resample=Image.BICUBIC, expand=True)
    c.colar_base(car, -50, topo + 3.2)
    c.adesivo("💦", 14, 30, 26, girar=-8)
    c.adesivo("😱", 52, 24, 26)


def cena_vaga(c, pal):
    fundo_ceu(c, pal["ceu"])
    fundo_rua(c, 76)
    chao_sombra(c, 0, 90, 150)
    c.colar_base(carro(c.L(62), LILAS), -58, 90)
    c.colar_base(carro(c.L(62), TURQUESA, virar=True), 58, 90)
    c.colar_base(carro(c.L(62), CORAL), 0, 91)
    # medida (setinhas de régua) acima do carro do meio
    d = c.d
    y = 40
    for cor, lw in ((ASFALTO, 3.4), (LARANJA_C, 1.6)):
        d.line([c.P(-28, y), c.P(28, y)], fill=rgb(cor), width=int(c.L(lw)))
        for sx in (-1, 1):
            d.polygon([c.P(sx * 31, y), c.P(sx * 24, y - 4.5), c.P(sx * 24, y + 4.5)], fill=rgb(cor))
            d.line([c.P(sx * 31.5, y - 6), c.P(sx * 31.5, y + 6)], fill=rgb(cor), width=int(c.L(lw)))
    c.adesivo("📏", 0, 18, 30, girar=-18)
    c.adesivo("😬", 54, 24, 24)


def cena_chuva(c, pal):
    fundo_ceu(c, ("#E9EBF2", "#D3D7E2"))
    fundo_rua(c, 76)
    d = c.d
    rnd = random.Random(5)
    for _ in range(26):
        x, y = rnd.uniform(-80, 80), rnd.uniform(30, 72)
        if -20 < x < 20 and y < 40:
            continue
        d.line([c.P(x, y), c.P(x - 1.5, y + 5)], fill=rgb("#6FB6E8"), width=max(2, int(c.L(1.1))))
    chao_sombra(c, 0, 89, 70)
    c.colar_base(carro(c.L(80), TURQUESA), 0, 90)
    brilhos(c, [(-42, 46, 7), (36, 42, 6), (8, 52, 4.2), (46, 64, 4)])
    c.adesivo("🌧", 0, 20, 46)
    c.adesivo("🧽", -58, 26, 24, girar=10)


def cena_barulho(c, pal):
    fundo_ceu(c, pal["ceu"])
    fundo_rua(c, 78)
    chao_sombra(c, -24, 89, 62)
    c.colar_base(carro(c.L(72), VIOLETA), -24, 90)
    d = c.d
    for k, (x0, y0) in enumerate(((16, 44), (20, 56), (16, 68))):
        pts = [c.P(x0 + i * 3.2, y0 + (2.8 if i % 2 else -2.8)) for i in range(5)]
        d.line(pts, fill=rgb(ASFALTO), width=int(c.L(3.4)), joint="curve")
        d.line(pts, fill=rgb(LARANJA_C), width=int(c.L(1.7)), joint="curve")
    c.adesivo("👂", 50, 44, 38)
    c.colar(simbolo("?", c.L(20), LARANJA_C, girar=12), 28, 22)
    c.colar(simbolo("?", c.L(15), LARANJA_C, girar=-10), 70, 14)
    c.adesivo("🔧", -60, 22, 24, girar=-15)


def cena_seta(c, pal):
    fundo_ceu(c, pal["ceu"])
    fundo_rua(c, 78)
    chao_sombra(c, -22, 89, 66)
    c.colar_base(carro(c.L(76), CORAL), -22, 90)
    c.colar(seta_pisca(c.L(34)), -22, 24)
    c.colar(simbolo("?", c.L(16), LARANJA_C, girar=10), 4, 14)
    c.adesivo("🤷", 52, 42, 40)


def cena_subida(c, pal):
    fundo_ceu(c, pal["ceu"])
    d = c.d
    y_esq, y_dir = 96, 46
    larg = c.W / c.u
    xe, xd = -larg / 2 - 2, larg / 2 + 2

    def ys(x):
        return y_esq + (x - xe) * (y_dir - y_esq) / (xd - xe)

    d.polygon([c.P(xe, ys(xe)), c.P(xd, ys(xd)), c.P(xd, 101), c.P(xe, 101)], fill=rgb(ASFALTO_2))
    d.line([c.P(xe, ys(xe)), c.P(xd, ys(xd))], fill=rgb("#9C98AA"), width=int(c.L(2.4)))
    ang = math.degrees(math.atan2(ys(xe) - ys(xd), (xd - xe)))
    tx, ty = math.cos(math.radians(ang)), -math.sin(math.radians(ang))
    nx, ny = -math.sin(math.radians(ang)), -math.cos(math.radians(ang))
    # faixa tracejada na ladeira
    x = xe
    while x < xd:
        p0 = (x, ys(x) + 9)
        p1 = (x + 9, ys(x + 9) + 9)
        d.line([c.P(*p0), c.P(*p1)], fill=rgb(AMARELO), width=int(c.L(2.4)))
        x += 20
    for (x, L, cor) in ((-60, 44, LILAS), (-14, 44, TURQUESA), (38, 54, CORAL)):
        car = carro(c.L(L), cor)
        bb = car.getbbox()
        hc = (bb[3] - bb[1]) / c.u
        car = car.crop(bb).rotate(ang, resample=Image.BICUBIC, expand=True)
        bx, by = x, ys(x) + 1.0
        c.colar(car, bx + nx * hc / 2, by + ny * hc / 2)
    c.adesivo("😬", 56, 18, 28)
    c.adesivo("💦", 30, 14, 16, girar=-15)


def cena_esquecer(c, pal):
    fundo_ceu(c, pal["ceu"])
    d = c.d
    d.rectangle([0, c.Y(62), c.W, c.H], fill=rgb(ASFALTO_2))
    for x in range(-100, 101, 40):
        d.line([c.P(x - 20 + 4, 64), c.P(x - 20 - 2, 100)], fill=rgb(BRANCO), width=int(c.L(1.6)))
    for x in (-60, -20, 20, 60):
        c.colar_base(carro(c.L(37), VIOLETA), x, 92)
    c.adesivo("🤔", -50, 26, 34)
    c.adesivo("🔑", 2, 28, 28, girar=20)
    c.colar(simbolo("?", c.L(22), LARANJA_C, girar=8), 40, 22)
    c.colar(simbolo("?", c.L(15), LARANJA_C, girar=-12), 64, 34)


def cena_bateria(c, pal):
    fundo_ceu(c, pal["ceu"])
    fundo_rua(c, 82)
    chao_sombra(c, -8, 91, 66)
    c.colar_base(bateria(c.L(70)), -8, 92)
    c.adesivo("😩", 52, 24, 32)


def cena_carona(c, pal):
    fundo_ceu(c, pal["ceu"])
    fundo_rua(c, 78)
    chao_sombra(c, -10, 89, 76)
    c.colar_base(carro(c.L(86), TURQUESA), -10, 90)
    c.colar(balao(c.L(42), c.L(26), "!!"), 28, 22)
    c.adesivo("🗣", -54, 24, 28, cor="#FF8A1F")


def cena_alarme(c, pal):
    fundo_ceu(c, ("#2C2546", "#4A3D70"))
    d = c.d
    rnd = random.Random(12)
    for _ in range(14):
        x, y = rnd.uniform(-80, 80), rnd.uniform(4, 50)
        r = rnd.uniform(0.6, 1.2)
        d.ellipse([c.X(x - r), c.Y(y - r), c.X(x + r), c.Y(y + r)], fill=rgb("#FFF3C4", 220))
    fundo_rua(c, 80, cor="#2A2833", meio_fio="#5E5A6E")
    cx, cy = 0, 66
    for k, r in enumerate((44, 54, 64)):
        for a0, a1 in ((150, 210), (-30, 30)):
            d.arc([c.X(cx - r), c.Y(cy - r * 0.62), c.X(cx + r), c.Y(cy + r * 0.62)], a0, a1,
                  fill=rgb(ASFALTO), width=int(c.L(4)))
            d.arc([c.X(cx - r), c.Y(cy - r * 0.62), c.X(cx + r), c.Y(cy + r * 0.62)], a0, a1,
                  fill=rgb("#FFB020" if k % 2 == 0 else AMARELO), width=int(c.L(2.2)))
    c.colar_base(carro(c.L(72), CORAL, farol_aceso=True), 0, 90)
    c.adesivo("🌙", -56, 18, 24)
    c.colar(simbolo("!", c.L(16), AMARELO, girar=-8), 40, 22)
    c.colar(simbolo("!", c.L(13), AMARELO, girar=8), 52, 30)


def cena_gps(c, pal):
    fundo_ceu(c, pal["ceu"])
    fundo_rua(c, 86)
    c.colar(com_sombra(mapa(c.L(104)), 0, c.L(1.2), c.L(1.4), 0.25), 4, 56)
    c.colar(seta_circular(c.L(26)), -60, 20)
    c.adesivo("📍", 30, 22, 30)


def cena_chave(c, pal):
    fundo_ceu(c, pal["ceu"])
    d = c.d
    # porta do carro (parte de baixo) + moldura da janela
    porta = "#FF7A57"
    d.rectangle([0, c.Y(74), c.W, c.H], fill=rgb(porta))
    d.rectangle([0, c.Y(74), c.W, c.Y(77)], fill=mix(porta, BRANCO, 0.35))
    d.rounded_rectangle([c.X(36), c.Y(84), c.X(58), c.Y(89)], radius=c.L(2), fill=mix(porta, "#000000", 0.3))
    jan = poli_arred([c.P(-66, 76), c.P(-44, 14), c.P(54, 14), c.P(70, 76)], c.L(8))
    m = Image.new("L", (c.W, c.H), 0)
    ImageDraw.Draw(m).polygon(jan, fill=255)
    c.img.alpha_composite(camada_cor((c.W, c.H), ASFALTO, dilatar(m, c.L(3.2))))
    vidro = gradiente(c.W, c.H, [(0, "#E6F7FF"), (1, "#B8E2F6")], (0.4, 0.6))
    vidro.putalpha(m)
    c.img.alpha_composite(vidro)
    # chave lá dentro (no banco), meio apagada pelo vidro
    k = emoji("🔑", c.L(30)).rotate(-25, resample=Image.BICUBIC, expand=True)
    k = com_contorno(k, c.L(0.8), ASFALTO)
    c.colar(k, -2, 48)
    refl = Image.new("L", (c.W, c.H), 0)
    rd = ImageDraw.Draw(refl)
    rd.polygon([c.P(-30, 14), c.P(-18, 14), c.P(-46, 76), c.P(-58, 76)], fill=150)
    rd.polygon([c.P(-12, 14), c.P(-6, 14), c.P(-34, 76), c.P(-40, 76)], fill=110)
    c.img.alpha_composite(camada_cor((c.W, c.H), BRANCO, intersec(refl, m)))
    c.adesivo("🔒", 56, 66, 30)
    c.colar(simbolo("!", c.L(15), LARANJA_C, girar=10), 34, 26)


def cena_volante(c, pal):
    fundo_ceu(c, ("#FFF4C2", "#FFC27A"))
    c.adesivo("☀", 58, 20, 34)
    d = c.d
    for x0 in (-34, -16, 2):
        pts = [c.P(x0 + 3.5 * math.sin(i * 0.9), 26 - i * 2.2) for i in range(10)]
        d.line(pts, fill=rgb(ASFALTO), width=int(c.L(3.4)), joint="curve")
        d.line(pts, fill=rgb("#FF6A1A"), width=int(c.L(1.8)), joint="curve")
    v = volante(c.L(62), aro="#3A3745", miolo="#55515F")
    v = com_sombra(v, 0, c.L(1.5), c.L(1.5), 0.25)
    c.colar(v, -14, 60)
    c.adesivo("🥵", 50, 66, 30)


def cena_limpador(c, pal):
    fundo_ceu(c, ("#E9EBF2", "#D3D7E2"))
    d = c.d
    pb = poli_arred([c.P(-74, 96), c.P(-56, 18), c.P(56, 18), c.P(74, 96)], c.L(10))
    m = Image.new("L", (c.W, c.H), 0)
    ImageDraw.Draw(m).polygon(pb, fill=255)
    c.img.alpha_composite(camada_cor((c.W, c.H), ASFALTO, dilatar(m, c.L(3.2))))
    vidro = gradiente(c.W, c.H, [(0, "#EAF8FF"), (1, "#B9E0F2")], (0.3, 0.7))
    vidro.putalpha(m)
    c.img.alpha_composite(vidro)
    # borrão em arco
    sm = Image.new("L", (c.W, c.H), 0)
    sd = ImageDraw.Draw(sm)
    px, py = 4, 96
    sd.pieslice([c.X(px - 64), c.Y(py - 64), c.X(px + 64), c.Y(py + 64)], 196, 344, fill=255)
    sd.pieslice([c.X(px - 40), c.Y(py - 40), c.X(px + 40), c.Y(py + 40)], 196, 344, fill=0)
    sm = intersec(sm.filter(ImageFilter.GaussianBlur(c.L(1.5))), m)
    c.img.alpha_composite(camada_cor((c.W, c.H), "#8C7A66", sm, 0.55))
    d = c.d
    rnd = random.Random(3)
    for _ in range(18):
        x, y = rnd.uniform(-50, 50), rnd.uniform(24, 90)
        r = rnd.uniform(1.0, 2.0)
        d.ellipse([c.X(x - r), c.Y(y - r * 1.2), c.X(x + r), c.Y(y + r * 1.2)], fill=rgb("#7CC4EE"))
    # palheta
    a = math.radians(300)
    bx, by = px + 66 * math.cos(a), py + 66 * math.sin(a)
    d.line([c.P(px, py), c.P(bx, by)], fill=rgb(ASFALTO), width=int(c.L(3.6)))
    off = math.radians(300 - 90)  # palheta ao lado do braço, paralela a ele
    ox, oy = 2.6 * math.cos(off), 2.6 * math.sin(off)
    d.line([c.P(px + 30 * math.cos(a) + ox, py + 30 * math.sin(a) + oy),
            c.P(px + 70 * math.cos(a) + ox, py + 70 * math.sin(a) + oy)], fill=rgb(ASFALTO), width=int(c.L(3.2)))
    d.ellipse([c.X(px - 4), c.Y(py - 4), c.X(px + 4), c.Y(py + 4)], fill=rgb(ASFALTO))
    c.adesivo("🌧", 58, 16, 28)


def marcador_combustivel(D):
    """Marcador de combustível (sem letras) com o ponteiro no vermelho."""
    D = int(D)
    pad = max(4, int(D * 0.06))
    w = D + 2 * pad
    cx = cy = w / 2
    R = D / 2
    im = Image.new("RGBA", (w, w), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=rgb(ASFALTO))
    d.ellipse([cx - R * 0.92, cy - R * 0.92, cx + R * 0.92, cy + R * 0.92], fill=rgb(BRANCO))
    d.ellipse([cx - R * 0.86, cy - R * 0.86, cx + R * 0.86, cy + R * 0.86], fill=rgb("#2E2C37"))
    ini, fim = 150, 390
    rr = R * 0.66
    d.arc([cx - rr, cy - rr, cx + rr, cy + rr], ini, ini + 40, fill=rgb("#FF3B30"), width=int(R * 0.14))
    for k in range(7):
        a = math.radians(ini + (fim - ini) * k / 6)
        r1, r2 = R * 0.52, R * (0.74 if k % 3 == 0 else 0.66)
        d.line([(cx + r1 * math.cos(a), cy + r1 * math.sin(a)), (cx + r2 * math.cos(a), cy + r2 * math.sin(a))],
               fill=rgb(BRANCO), width=max(2, int(R * 0.06)))
    # bombinha (pictograma) embaixo
    px, py = cx, cy + R * 0.45
    s = R * 0.20
    d.rounded_rectangle([px - s * 0.6, py - s * 0.8, px + s * 0.5, py + s * 0.8], radius=s * 0.12, fill=rgb("#FFB020"))
    d.rectangle([px - s * 0.4, py - s * 0.6, px + s * 0.3, py - s * 0.1], fill=rgb("#2E2C37"))
    d.line([(px + s * 0.5, py - s * 0.3), (px + s * 0.9, py - s * 0.1), (px + s * 0.9, py + s * 0.5)],
           fill=rgb("#FFB020"), width=max(2, int(s * 0.2)))
    # ponteiro no vermelho
    a = math.radians(ini + 16)
    comp = R * 0.72
    ponta = (cx + comp * math.cos(a), cy + comp * math.sin(a))
    perp = a + math.pi / 2
    b = R * 0.07
    d.polygon([ponta, (cx + b * math.cos(perp), cy + b * math.sin(perp)),
               (cx - R * 0.1 * math.cos(a), cy - R * 0.1 * math.sin(a)),
               (cx - b * math.cos(perp), cy - b * math.sin(perp))], fill=rgb("#FF5A1F"))
    d.ellipse([cx - R * 0.1, cy - R * 0.1, cx + R * 0.1, cy + R * 0.1], fill=rgb(BRANCO))
    return im


def cena_reserva(c, pal):
    fundo_ceu(c, ("#FFF6E0", "#FFD9A8"))
    d = c.d
    hz = 46
    d.rectangle([0, c.Y(hz), c.W, c.H], fill=rgb("#E7D29C"))
    d.polygon([c.P(-6, hz), c.P(6, hz), c.P(70, 101), c.P(-70, 101)], fill=rgb(ASFALTO_2))
    for k in range(6):
        t0, t1 = k / 6, k / 6 + 0.08
        y0, y1 = hz + (100 - hz) * t0 ** 1.4, hz + (100 - hz) * t1 ** 1.4
        w0, w1 = 0.4 + 2.2 * t0, 0.4 + 2.2 * t1
        d.polygon([c.P(-w0 / 2, y0), c.P(w0 / 2, y0), c.P(w1 / 2, y1), c.P(-w1 / 2, y1)], fill=rgb(AMARELO))
    g = marcador_combustivel(c.L(58))
    c.colar(com_sombra(g, 0, c.L(1.5), c.L(1.5), 0.3), -44, 56)
    c.adesivo("⛽", 50, 30, 30)


def cena_garagem(c, pal):
    fundo_ceu(c, pal["ceu"])
    d = c.d
    d.rectangle([c.X(-100), c.Y(12), c.X(100), c.Y(84)], fill=rgb("#F1E4CF"))
    d.rectangle([c.X(-100), c.Y(12), c.X(100), c.Y(16)], fill=rgb("#C9B596"))
    d.rectangle([c.X(-40), c.Y(26), c.X(40), c.Y(84)], fill=rgb(ASFALTO))
    d.rectangle([c.X(-37), c.Y(29), c.X(37), c.Y(84)], fill=rgb("#C2BFCD"))
    for y in range(33, 84, 7):
        d.line([c.P(-37, y), c.P(37, y)], fill=rgb("#8E8A9C"), width=max(1, int(c.L(1))))
    d.rectangle([0, c.Y(84), c.W, c.H], fill=rgb(ASFALTO_2))
    chao_sombra(c, 6, 95, 76)
    c.colar_base(carro(c.L(84), LARANJA_C), 6, 96)
    c.adesivo("😤", -62, 32, 26)
    c.adesivo("🚧", 62, 32, 26)


CENAS = {
    1: cena_baliza, 2: cena_pneu, 3: cena_poca, 4: cena_vaga, 5: cena_chuva,
    6: cena_barulho, 7: cena_seta, 8: cena_subida, 9: cena_esquecer, 10: cena_bateria,
    11: cena_carona, 12: cena_alarme, 13: cena_gps, 14: cena_chave,
    101: cena_volante, 102: cena_limpador, 103: cena_reserva, 104: cena_garagem,
}


# ---------------------------------------------------------------- texto
def medir_fonte(linhas, largura, tam_max, tam_min, arquivo=F_BLACK):
    d = ImageDraw.Draw(Image.new("L", (10, 10)))
    for tam in range(tam_max, tam_min - 1, -1):
        f = ImageFont.truetype(arquivo, tam * S)
        sw = max(3, round(tam * 0.085)) * S
        if max(d.textlength(l, font=f) for l in linhas) + 2 * sw <= largura * S:
            return tam, f, sw
    raise SystemExit(f"texto não coube nem com {tam_min}px: {linhas}")


def _layout_texto(linhas, fontes):
    """Posições de base (relativas ao topo da maiúscula da 1ª linha) e altura total do bloco, em px 3x."""
    caps = [-fo[1].getbbox("H", anchor="ls")[1] for fo in fontes]
    acento = [-fo[1].getbbox("ÊÁÉÍÃÀ", anchor="ls")[1] for fo in fontes]
    alt = caps[0]
    bases = [caps[0]]
    for i in range(1, len(linhas)):
        alt += caps[i] + (acento[i] - caps[i]) * 0.85 + fontes[i][2] * 1.0
        bases.append(alt)
    acima = (acento[0] - caps[0]) if any(ch in linhas[0] for ch in "ÁÃÉÊÍÓÔÕÚÇÀ") else 0
    sombra_px = max(3, round(fontes[0][0] * 0.07)) * S
    # descendente de Ç/Q/J na última linha + contorno + sombra
    desc = fontes[-1][1].getbbox(linhas[-1], anchor="ls")[3]
    total = acima + fontes[0][2] + alt + max(desc, 0) + fontes[-1][2] + sombra_px
    return bases, alt, acima, sombra_px, total


def desenhar_texto(img, linhas, area, cor_contorno=ASFALTO, cores_linha=None, tam_max=60, tam_min=30,
                   tamanhos=None, arquivo=F_BLACK, sombra=True, alinhar="centro"):
    """1 a 3 linhas com contorno e sombra dura. Reduz a fonte até caber na LARGURA e na ALTURA da área
    (contando acento, contorno e sombra), então nada encosta na borda nem corta."""
    x0, y0, x1, y1 = area
    cores_linha = cores_linha or [BRANCO] * len(linhas)
    d = ImageDraw.Draw(img)
    base_tams = list(tamanhos) if tamanhos else [tam_max] * len(linhas)
    reducao = 0
    while True:
        alvo = [max(tam_min, t - reducao) for t in base_tams]
        if tamanhos is None:
            tam, f, sw = medir_fonte(linhas, x1 - x0, alvo[0], tam_min, arquivo)
            fontes = [(tam, f, sw)] * len(linhas)
        else:
            fontes = [medir_fonte([l], x1 - x0, t, tam_min, arquivo) for l, t in zip(linhas, alvo)]
        bases, alt, acima, sombra_px, total = _layout_texto(linhas, fontes)
        if total <= (y1 - y0) * S or all(fo[0] <= tam_min for fo in fontes):
            break
        reducao += 1
    if total > (y1 - y0) * S:
        raise SystemExit(f"texto não coube na altura: {linhas}")
    # centraliza o bloco inteiro (acento + contorno + sombra incluídos)
    topo = (y0 + y1) / 2 * S - total / 2 + acima + fontes[0][2]
    cx = (x0 + x1) / 2 * S
    anchor = "ms"
    if alinhar == "esquerda":
        cx = x0 * S + fontes[0][2]
        anchor = "ls"
    if sombra:
        for i, l in enumerate(linhas):
            tam, f, sw = fontes[i]
            d.text((cx, topo + bases[i] + sombra_px), l, font=f, anchor=anchor, fill=rgb(cor_contorno),
                   stroke_width=sw, stroke_fill=rgb(cor_contorno))
    for i, l in enumerate(linhas):
        tam, f, sw = fontes[i]
        d.text((cx, topo + bases[i]), l, font=f, anchor=anchor, fill=rgb(cores_linha[i]),
               stroke_width=sw, stroke_fill=rgb(cor_contorno))
    return [fo[0] for fo in fontes], (topo - acima - fontes[0][2]) / S, (topo - acima - fontes[0][2] + total) / S


# ---------------------------------------------------------------- moldura (placa)
def mascara_rr(w, h, rect, r, e=0):
    m = Image.new("L", (w * S, h * S), 0)
    x0, y0, x1, y1 = rect
    ImageDraw.Draw(m).rounded_rectangle([(x0 - e) * S, (y0 - e) * S, (x1 + e) * S, (y1 + e) * S],
                                        radius=max(1, r + e) * S, fill=255)
    return m


def listras(size, m_corpo, cor, cantos, alcance, alpha=0.16):
    """Listras diagonais de advertência que somem a partir dos cantos."""
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    passo = 26 * S
    faixa = ((xx + yy) % passo) < (passo * 0.5)
    peso = np.zeros((h, w), np.float32)
    for (cx, cy) in cantos:
        dist = np.sqrt((xx - cx * S) ** 2 + (yy - cy * S) ** 2) / (alcance * S)
        peso = np.maximum(peso, np.clip(1 - dist, 0, 1))
    a = (faixa * peso * 255 * alpha * 2.2).clip(0, 255).astype(np.uint8)
    return camada_cor(size, cor, intersec(Image.fromarray(a), m_corpo))


def placa(w, h, corpo_rect, raio, pal, extras_rim=(), corpo_cores=None, listra_alpha=0.16):
    """Moldura: sombra, aro branco, borda de asfalto, corpo em gradiente, brilho e listras nos cantos."""
    size = (w * S, h * S)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    m_rim = uniao(mascara_rr(w, h, corpo_rect, raio, RIM), *extras_rim)
    sombra = deslocar(m_rim, 0, 6 * S).filter(ImageFilter.GaussianBlur(6 * S))
    img.alpha_composite(camada_cor(size, "#120A22", sombra, 0.45))
    img.alpha_composite(camada_cor(size, pal["shade"], deslocar(m_rim, 0, 5 * S)))
    img.alpha_composite(camada_cor(size, BRANCO, m_rim))
    img.alpha_composite(camada_cor(size, ASFALTO, mascara_rr(w, h, corpo_rect, raio, 0)))
    m_corpo = mascara_rr(w, h, corpo_rect, raio, -BORDA)
    cores = corpo_cores or [(0, pal["top"]), (1, pal["bot"])]
    corpo = gradiente(size[0], size[1], cores, (0.2, 0.8))
    corpo.putalpha(m_corpo)
    img.alpha_composite(corpo)
    x0, y0, x1, y1 = corpo_rect
    img.alpha_composite(listras(size, m_corpo, pal["listra"], [(x0, y0), (x1, y1)], 170, listra_alpha))
    # brilho no topo
    gl = Image.new("L", size, 0)
    gd = ImageDraw.Draw(gl)
    for i in range(50):
        yy = y0 + i * (y1 - y0) * 0.45 / 50
        gd.line([(0, yy * S), (w * S, yy * S)], fill=int(60 * (1 - i / 50)), width=S * 2)
    img.alpha_composite(camada_cor(size, BRANCO, intersec(gl, m_corpo)))
    # linha interna fina
    linha = Image.fromarray(np.clip(np.array(mascara_rr(w, h, corpo_rect, raio, -BORDA - 5)).astype(int)
                                    - np.array(mascara_rr(w, h, corpo_rect, raio, -BORDA - 7)).astype(int),
                                    0, 255).astype(np.uint8))
    img.alpha_composite(camada_cor(size, BRANCO, linha, 0.35))
    return img


def painel(img, w, h, rect, r, cena_fn, pal, shade):
    """Janela com a cena: sombrinha, borda de asfalto e a cena recortada."""
    size = img.size
    img.alpha_composite(camada_cor(size, shade, deslocar(mascara_rr(w, h, rect, r, 0), 0, 4 * S), 0.55))
    img.alpha_composite(camada_cor(size, ASFALTO, mascara_rr(w, h, rect, r, 0)))
    x0, y0, x1, y1 = rect
    b = PAINEL_BORDA
    c = Cena((x1 - x0 - 2 * b) * S, (y1 - y0 - 2 * b) * S)
    cena_fn(c, pal)
    lay = Image.new("RGBA", size, (0, 0, 0, 0))
    lay.paste(c.img, ((x0 + b) * S, (y0 + b) * S))
    lay.putalpha(intersec(lay.split()[3], mascara_rr(w, h, rect, r, -b)))
    img.alpha_composite(lay)
    # reflexo de vidro no canto do painel
    rf = Image.new("L", size, 0)
    ImageDraw.Draw(rf).polygon([((x0 + b) * S, (y0 + b) * S), ((x0 + b + 46) * S, (y0 + b) * S),
                                ((x0 + b) * S, (y0 + b + 46) * S)], fill=60)
    img.alpha_composite(camada_cor(size, BRANCO, intersec(rf, mascara_rr(w, h, rect, r, -b))))


def reduzir(img):
    return img.resize((img.width // S, img.height // S), Image.LANCZOS)


# ---------------------------------------------------------------- peças
def carta_quadrada(item, pal_nome, chave):
    pal = PALETAS[pal_nome]
    w = h = 512
    img = placa(w, h, Q_CORPO, Q_RAIO, pal)
    painel(img, w, h, Q_PAINEL, Q_PAINEL_R, CENAS[chave], pal, pal["shade"])
    tam, _, _ = desenhar_texto(img, [item["linha1"], item["linha2"]], Q_TEXTO, ASFALTO,
                               [pal["texto"]] * 2, tam_max=62, tam_min=36)
    return reduzir(img), tam[0]


def carta_larga(item, pal_nome, chave):
    pal = PALETAS[pal_nome]
    w, h = 512, 256
    img = placa(w, h, L_CORPO, L_RAIO, pal, extras_rim=[mascara_rr(w, h, L_PAINEL, L_PAINEL_R, RIM)])
    painel(img, w, h, L_PAINEL, L_PAINEL_R, CENAS[chave], pal, pal["shade"])
    tam, _, _ = desenhar_texto(img, [item["linha1"], item["linha2"]], L_TEXTO, ASFALTO,
                               [pal["texto"]] * 2, tam_max=56, tam_min=34)
    return reduzir(img), tam[0]


TITULO_CORES = [(0, "#55516A"), (0.6, "#2B2934"), (1, "#1C1A22")]


def pilula(img, texto, cx, cy, altura, cor_fundo=AMARELO, cor_txt=GRAFITE_TXT, fonte=F_BLACK, larg_max=None,
           icone=None):
    """Pílula com aro branco + borda escura (subtítulo, etiquetas). Coordenadas em 1x."""
    d = ImageDraw.Draw(img)
    tam = int(altura * 0.50)
    while True:
        f = ImageFont.truetype(fonte, tam * S)
        tw = d.textlength(texto, font=f)
        iw = (altura * 0.62 * S + 8 * S) if icone is not None else 0
        wtot = tw + iw + altura * 0.9 * S
        if larg_max is None or wtot <= larg_max * S or tam <= 12:
            break
        tam -= 1
    hh = altura * S
    box = [cx * S - wtot / 2, cy * S - hh / 2, cx * S + wtot / 2, cy * S + hh / 2]
    # sombra
    sm = Image.new("L", img.size, 0)
    ImageDraw.Draw(sm).rounded_rectangle([box[0], box[1] + 4 * S, box[2], box[3] + 4 * S], radius=hh / 2, fill=255)
    img.alpha_composite(camada_cor(img.size, "#000000", sm.filter(ImageFilter.GaussianBlur(3 * S)), 0.35))
    d.rounded_rectangle([box[0] - 3 * S, box[1] - 3 * S, box[2] + 3 * S, box[3] + 3 * S], radius=hh / 2 + 3 * S,
                        fill=rgb(BRANCO))
    d.rounded_rectangle(box, radius=hh / 2, fill=rgb(ASFALTO))
    d.rounded_rectangle([box[0] + 3 * S, box[1] + 3 * S, box[2] - 3 * S, box[3] - 3 * S], radius=hh / 2 - 3 * S,
                        fill=rgb(cor_fundo))
    x = box[0] + altura * 0.45 * S
    if icone is not None:
        ic = icone(int(altura * 0.62 * S))
        colar(img, ic, x, cy * S - ic.height / 2)
        x += ic.width + 8 * S
    d.text((x, cy * S + 1 * S), texto, font=f, anchor="lm", fill=rgb(cor_txt))
    return wtot / S


def titulo_quadrado(tx, subtitulo):
    w = h = 512
    pal = dict(PALETAS["asfalto"])
    corpo = (20, 100, 492, 488)
    hd = 90  # meia-diagonal do losango
    # aro do losango entra no aro branco geral
    pv = placa_volante(2 * hd * S)
    # o losango entra na sombra/aro geral da peça (só a parte opaca, sem a sombra suave dele)
    tmp = Image.new("L", (w * S, h * S), 0)
    tmp.paste(pv.split()[3].point(lambda v: 255 if v > 200 else 0),
              (int(256 * S - pv.width / 2), int(95 * S - pv.height / 2)))
    img = placa(w, h, corpo, Q_RAIO, pal, extras_rim=[tmp], corpo_cores=TITULO_CORES, listra_alpha=0.12)
    colar_centro(img, pv, 256 * S, 95 * S)
    linhas = [tx["titulo_topo"]["linha1"], tx["titulo_topo"]["linha2"], tx["titulo_topo"]["linha3"]]
    area = (40, 192, 472, 410) if subtitulo else (40, 192, 472, 470)
    desenhar_texto(img, linhas, area, "#121117", [BRANCO, AMARELO, BRANCO], tamanhos=(54, 68, 54), tam_min=30)
    if subtitulo:
        pilula(img, subtitulo, 256, 438, 50, larg_max=420)
    return reduzir(img)


def titulo_largo(tx, subtitulo):
    w, h = 512, 256
    pal = dict(PALETAS["asfalto"])
    corpo = (14, 14, 498, 242)
    img = placa(w, h, corpo, 30, pal, corpo_cores=TITULO_CORES, listra_alpha=0.12)
    pv = placa_volante(150 * S)
    colar_centro(img, pv, 102 * S, 128 * S)
    linhas = [tx["titulo_topo"]["linha1"], tx["titulo_topo"]["linha2"], tx["titulo_topo"]["linha3"]]
    if subtitulo:
        area = (186, 28, 484, 186)
    else:
        area = (186, 34, 484, 222)
    desenhar_texto(img, linhas, area, "#121117", [BRANCO, AMARELO, BRANCO], tamanhos=(46, 58, 46), tam_min=26)
    if subtitulo:
        pilula(img, subtitulo, 335, 210, 36, larg_max=296)
    return reduzir(img)


# ---------------------------------------------------------------- marcadores e interface
RAMPA_POSICAO = ["#FF4F1F", "#FF6418", "#FF7A12", "#FF900C", "#FFA507", "#FFBA04", "#F2C613", "#D9D126",
                 "#BCD72C", "#9ED22A"]


def marcador(n):
    w = h = 256
    cor = RAMPA_POSICAO[n - 1]
    pal = dict(shade=mix(cor, "#000000", 0.55), listra=BRANCO)
    img = placa(w, h, (22, 22, 234, 230), 42, pal, corpo_cores=[(0, mix(cor, BRANCO, 0.30)), (1, cor)],
                listra_alpha=0.12)
    desenhar_texto(img, [str(n)], (36, 40, 220, 214), ASFALTO, [BRANCO], tam_max=140, tam_min=60)
    return reduzir(img)


def mao_icone(px):
    return emoji("👆", px)


def seta_volta_icone(px):
    return seta_circular(px * 0.80, cor=GRAFITE_TXT, ini=60, fim=330)


def peca_interface(texto, w, h, cor_fundo, cor_txt, icone=None):
    img = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))
    pilula(img, texto, w / 2, h / 2 - 2, h * 0.70, cor_fundo, cor_txt, larg_max=w - 16, icone=icone)
    return reduzir(img)


# ---------------------------------------------------------------- ícones
def icone(tam_final=162, estilo="claro"):
    t = 648 if tam_final <= 162 else tam_final * 2
    if estilo == "claro":
        img = gradiente(t, t, [(0, "#FFE680"), (0.55, "#FFC21A"), (1, "#FF8A00")], (0.45, 0.55))
        # listras de advertência suaves no canto de baixo
        m = Image.new("L", (t, t), 255)
        yy, xx = np.mgrid[0:t, 0:t].astype(np.float32)
        faixa = ((xx + yy) % (t * 0.09)) < (t * 0.045)
        peso = np.clip(1 - np.sqrt((xx - t) ** 2 + (yy - t) ** 2) / (t * 0.55), 0, 1)
        a = Image.fromarray((faixa * peso * 70).astype(np.uint8))
        img.alpha_composite(camada_cor((t, t), ASFALTO, intersec(a, m)))
        v = volante(t * 0.66, aro="#2E2C37", miolo="#4D4A58").rotate(-10, resample=Image.BICUBIC)
        vs = com_sombra(v, 0, t * 0.018, t * 0.006, 0.30, "#7A3A00")
        colar_centro(img, vs, t * 0.47, t * 0.55)
        g = gota(t * 0.36)
        colar_centro(img, com_sombra(g, 0, t * 0.01, t * 0.005, 0.3, "#7A3A00"), t * 0.78, t * 0.27)
        d = ImageDraw.Draw(img)
        for (a0, r1, r2) in ((200, 0.37, 0.45), (222, 0.38, 0.47), (244, 0.37, 0.44)):
            ang = math.radians(a0)
            cx, cy = t * 0.47, t * 0.55
            p1 = (cx + t * r1 * math.cos(ang), cy + t * r1 * math.sin(ang))
            p2 = (cx + t * r2 * math.cos(ang), cy + t * r2 * math.sin(ang))
            d.line([p1, p2], fill=rgb(ASFALTO), width=int(t * 0.028))
    else:
        img = gradiente(t, t, [(0, "#45414F"), (1, "#1C1A22")], (0.3, 0.7))
        d = ImageDraw.Draw(img)
        # listinha 1, 2, 3 atrás
        f = ImageFont.truetype(F_BLACK, int(t * 0.11))
        for i, (cor, larg) in enumerate((("#FF6418", 0.50), ("#FFB300", 0.42), ("#9ED22A", 0.34))):
            y = t * (0.15 + i * 0.165)
            x0 = t * 0.10
            d.rounded_rectangle([x0 - t * 0.012, y - t * 0.012, x0 + t * larg + t * 0.012, y + t * 0.122 + t * 0.012],
                                radius=t * 0.07, fill=rgb(BRANCO))
            d.rounded_rectangle([x0, y, x0 + t * larg, y + t * 0.122], radius=t * 0.06, fill=rgb(cor))
            d.ellipse([x0 + t * 0.012, y + t * 0.012, x0 + t * 0.110, y + t * 0.110], fill=rgb(ASFALTO))
            d.text((x0 + t * 0.061, y + t * 0.063), str(i + 1), font=f, anchor="mm", fill=rgb(BRANCO))
            d.rounded_rectangle([x0 + t * 0.14, y + t * 0.045, x0 + t * (larg - 0.05), y + t * 0.077],
                                radius=t * 0.016, fill=rgb(BRANCO, 150))
        v = volante(t * 0.58, aro="#F2EFF8", miolo="#D6D1E2", linha=ASFALTO).rotate(-10, resample=Image.BICUBIC)
        vs = com_sombra(v, 0, t * 0.018, t * 0.008, 0.6)
        colar_centro(img, vs, t * 0.60, t * 0.64)
        g = gota(t * 0.30)
        colar_centro(img, com_sombra(g, 0, t * 0.01, t * 0.012, 0.4), t * 0.84, t * 0.32)
    return img.resize((tam_final, tam_final), Image.LANCZOS).convert("RGB")


# ---------------------------------------------------------------- prévia
def xadrez(w, h, q=12):
    im = Image.new("RGBA", (w, h), rgb("#FFFFFF"))
    d = ImageDraw.Draw(im)
    for y in range(0, h, q):
        for x in range(0, w, q):
            if (x // q + y // q) % 2:
                d.rectangle([x, y, x + q - 1, y + q - 1], fill=rgb("#D9D6E0"))
    return im


def foto_generica(w, h, tipo):
    rnd = random.Random(tipo)
    if tipo == "carro":  # dentro de um carro parado, de dia (genérico)
        im = gradiente(w, h, [(0, "#CFE6F2"), (0.5, "#F2EEE6"), (1, "#E5DED3")], (0, 1))
        d = ImageDraw.Draw(im)
        d.polygon([(0, 0), (w * 0.22, 0), (0, h * 0.55)], fill=rgb("#3A3844"))
        d.polygon([(w, 0), (w * 0.78, 0), (w, h * 0.55)], fill=rgb("#3A3844"))
        d.rectangle([0, h * 0.30, w, h * 0.36], fill=rgb("#9CB88A"))
        d.rectangle([0, h * 0.78, w, h], fill=rgb("#2E2C36"))
        d.rectangle([0, h * 0.74, w, h * 0.79], fill=rgb("#4A4756"))
    elif tipo == "noite":
        im = gradiente(w, h, [(0, "#0B0F1E"), (1, "#05060B")], (0, 1))
        d = ImageDraw.Draw(im)
        for _ in range(30):
            x, y, r = rnd.uniform(0, w), rnd.uniform(0, h * 0.7), rnd.uniform(10, 40)
            c = rnd.choice(["#FFB347", "#FFE08A", "#FF7A59", "#C9A0FF"])
            d.ellipse([x - r, y - r, x + r, y + r], fill=rgb(c, rnd.randint(40, 110)))
        im = im.filter(ImageFilter.GaussianBlur(6))
    elif tipo == "sala":
        im = gradiente(w, h, [(0, "#F4EEE6"), (1, "#D9CFC2")], (0, 1))
        d = ImageDraw.Draw(im)
        d.rectangle([w * 0.58, h * 0.08, w * 0.93, h * 0.40], fill=rgb("#CFE8F7"))
        d.rectangle([w * 0.58, h * 0.08, w * 0.93, h * 0.40], outline=rgb("#FFFFFF"), width=8)
        d.rectangle([0, h * 0.72, w, h], fill=rgb("#B9A58E"))
    else:  # fundo bem poluído
        im = Image.new("RGBA", (w, h), rgb("#FFF3D6"))
        d = ImageDraw.Draw(im)
        for _ in range(420):
            x, y = rnd.uniform(0, w), rnd.uniform(0, h)
            c = rnd.choice(["#FF6400", "#FFD43B", "#9ED22A", "#1F1A2E", "#FFFFFF", "#22C1C3", "#E3157A"])
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


def celular(tipo, cor_sil, topo_img=None, atual=None, lista=None, marcadores=None, modo_lista="largo"):
    """Simulação APROXIMADA do Blind Rank (layout real a confirmar no app):
    título em cima, item da vez sobre a cabeça, lista 1..10 à esquerda."""
    w, h = 405, 720
    im = foto_generica(w, h, tipo)
    topo_cab = int(h * 0.58)
    silhueta(im, w * 0.62, topo_cab, w * 0.62, cor_sil)
    if topo_img is not None:
        tw = int(w * (0.50 if topo_img.width == topo_img.height else 0.60))
        t = topo_img.resize((tw, int(topo_img.height * tw / topo_img.width)), Image.LANCZOS)
        im.alpha_composite(t, (int(w * 0.62 - tw / 2), 14))
    if atual is not None:
        aw = int(w * 0.40)
        a = atual.resize((aw, int(atual.height * aw / atual.width)), Image.LANCZOS)
        im.alpha_composite(a, (int(w * 0.62 - aw / 2), int(topo_cab - a.height + 6)))
    if marcadores:
        y0, rh = 150, 54
        for i in range(10):
            y = y0 + i * rh
            mk = marcadores[i].resize((40, 40), Image.LANCZOS)
            im.alpha_composite(mk, (8, y + (rh - 40) // 2))
            if lista and i < len(lista) and lista[i] is not None:
                th = lista[i]
                if modo_lista == "largo":
                    tw2 = 104
                else:
                    tw2 = 52
                t = th.resize((tw2, int(th.height * tw2 / th.width)), Image.LANCZOS)
                im.alpha_composite(t, (50, int(y + (rh - t.height) / 2)))
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


def previa(grupos, icones, sim):
    fundo = rgb("#F4F2F7")
    MARG, GX, GY = 40, 28, 58
    larg = 1760
    f_h1 = ImageFont.truetype(F_BLACK, 44)
    f_h2 = ImageFont.truetype(F_XBOLD, 28)
    f_lb = ImageFont.truetype(F_BOLD, 17)
    f_sm = ImageFont.truetype(F_SEMI, 15)
    # altura
    alt = 150
    for _, itens, tw, th, cols in grupos:
        alt += 50 + math.ceil(len(itens) / cols) * (th + GY) + 10
    alt += 320 + 60 + 720 + 120
    sheet = Image.new("RGBA", (larg, alt), fundo)
    d = ImageDraw.Draw(sheet)
    d.text((MARG, 36), "C09 · Perrengue no volante — prévia das imagens", font=f_h1, fill=rgb(GRAFITE_TXT))
    d.text((MARG, 94), "Xadrez = transparente. Itens e títulos em 512×512 (padrão) e 512×256 (largo_512x256/). "
                       "Ordem da grade = ordem dos arquivos. Ícone de envio: 162×162.",
           font=f_sm, fill=rgb("#5B5470"))
    y = 140
    for titulo_g, itens, tw, th, cols in grupos:
        d.text((MARG, y), titulo_g, font=f_h2, fill=rgb(GRAFITE_TXT))
        y += 50
        for i, (nome, im, legenda) in enumerate(itens):
            r, cc = divmod(i, cols)
            x = MARG + cc * (tw + GX)
            yy = y + r * (th + GY)
            cell = xadrez(tw, th)
            t = im.copy().convert("RGBA")
            t.thumbnail((tw, th), Image.LANCZOS)
            cell.alpha_composite(t, ((tw - t.width) // 2, (th - t.height) // 2))
            sheet.alpha_composite(cell, (x, yy))
            d.text((x, yy + th + 6), nome, font=f_lb, fill=rgb(GRAFITE_TXT))
            d.text((x, yy + th + 27), legenda, font=f_sm, fill=rgb("#6B6480"))
        y += math.ceil(len(itens) / cols) * (th + GY) + 10
    # ícones
    d.text((MARG, y), "Ícone como aparece no app (cantos arredondados pelo próprio app): 162, 96 e 64 px",
           font=f_h2, fill=rgb(GRAFITE_TXT))
    y += 50
    x = MARG
    for nome, ic in icones:
        x_ini = x
        for tam in (162, 96, 64):
            a = arredondar(ic.resize((tam, tam), Image.LANCZOS))
            sheet.alpha_composite(a, (x, y + (162 - tam)))
            x += tam + 18
        d.text((x_ini, y + 172), nome, font=f_lb, fill=rgb(GRAFITE_TXT))
        x += 50
    for nome, ic in icones:
        a = ic.resize((162, 162), Image.LANCZOS).convert("RGBA")
        dd = ImageDraw.Draw(a)
        dd.rectangle([9, 9, 152, 152], outline=rgb("#00B7FF"), width=1)
        sheet.alpha_composite(a, (x, y))
        d.text((x, y + 172), "área segura 144×144", font=f_sm, fill=rgb("#5B5470"))
        x += 162 + 30
    for nome, ic in icones:  # em fundo escuro (tema escuro do app)
        bg = Image.new("RGBA", (190, 190), rgb("#121212"))
        bg.alpha_composite(arredondar(ic.resize((96, 96), Image.LANCZOS)), (47, 30))
        sheet.alpha_composite(bg, (x, y - 14))
        x += 210
    d.text((x - 420, y + 172), "96 px sobre fundo escuro", font=f_sm, fill=rgb("#5B5470"))
    y += 260
    d.text((MARG, y), "Simulação APROXIMADA sobre fotos genéricas (layout do Blind Rank a confirmar no app; "
                      "lista 1–10 à esquerda)", font=f_h2, fill=rgb(GRAFITE_TXT))
    y += 50
    x = MARG
    for rot, cel in sim:
        sheet.alpha_composite(cel, (x, y))
        d.text((x, y + cel.height + 10), rot, font=f_lb, fill=rgb(GRAFITE_TXT))
        x += cel.width + 26
    return sheet.convert("RGB")


# ---------------------------------------------------------------- principal
def salvar(im, caminho):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    im.save(caminho, optimize=True)


def main():
    with open(TEXTOS, encoding="utf-8") as fh:
        tx = json.load(fh)
    LARGO = os.path.join(AQUI, "largo_512x256")
    grupos = []
    tam_fonte = {}

    # títulos
    tt = tx["titulo_topo"]
    variantes = [
        ("titulo.png", tt["subtitulo"], "padrão (10 posições)"),
        ("titulo_curto.png", tt["subtitulo_se_faltar_espaco"], "se faltar espaço"),
        ("titulo_5_posicoes.png", tt["subtitulo_se_o_template_tiver_so_5_posicoes"], "se o template tiver 5"),
        ("titulo_sem_subtitulo.png", None, "só o título"),
    ]
    g_tit, g_tit_l = [], []
    titulos = {}
    for nome, sub, leg in variantes:
        tq = titulo_quadrado(tx, sub)
        tl = titulo_largo(tx, sub)
        salvar(tq, os.path.join(AQUI, nome))
        salvar(tl, os.path.join(LARGO, nome))
        g_tit.append((nome, tq, leg))
        g_tit_l.append((nome, tl, leg))
        titulos[nome] = (tq, tl)
    grupos.append(("Título 512×512 (raiz de assets/)", g_tit, 300, 300, 5))
    grupos.append(("Título 512×256 (largo_512x256/)", g_tit_l, 400, 200, 4))

    # cartas
    todos = ([(it, "cartas", f"carta_{it['n']:02d}.png", it["n"]) for it in tx["resultados"]]
             + [(it, "extras", f"carta_{it['n']:02d}.png", it["n"]) for it in tx["extras_rodizio"]]
             + [(it, "reservas", f"reserva_{it['n']:02d}.png", 100 + it["n"]) for it in tx["reservas"]])
    g_cartas, g_extras, g_res, g_largo = [], [], [], []
    quad, larg = {}, {}
    for i, (it, pasta, nome, chave) in enumerate(todos):
        cor = ORDEM_CORES[i % len(ORDEM_CORES)]
        q, tq = carta_quadrada(it, cor, chave)
        l, tl = carta_larga(it, cor, chave)
        salvar(q, os.path.join(AQUI, pasta, nome))
        salvar(l, os.path.join(LARGO, pasta, nome))
        rot = f"{pasta}/{nome}"
        leg = f"{it.get('codigo', '')} {it['linha1']} / {it['linha2']} · {tq}px".strip()
        {"cartas": g_cartas, "extras": g_extras, "reservas": g_res}[pasta].append((rot, q, leg))
        g_largo.append((rot, l, f"{it['linha1']} / {it['linha2']} · {tl}px"))
        quad[chave], larg[chave] = q, l
        tam_fonte[rot] = (tq, tl)
    grupos.append(("Cartas da versão padrão (cartas/, só estas 10) · 512×512", g_cartas, 300, 300, 5))
    grupos.append(("Extras do rodízio (extras/) e reservas (reservas/) · 512×512", g_extras + g_res, 300, 300, 5))
    grupos.append(("As mesmas peças em 512×256 (largo_512x256/...)", g_largo, 320, 160, 5))

    # marcadores e interface
    mks = []
    g_mk = []
    for n in range(1, 11):
        m = marcador(n)
        salvar(m, os.path.join(AQUI, "marcadores", f"posicao_{n:02d}.png"))
        mks.append(m)
        g_mk.append((f"posicao_{n:02d}.png", m, "256×256"))
    ti = tx["textos_de_interface"]
    interface = [
        ("etiqueta_toque.png", peca_interface(ti["instrucao_toque"], 512, 128, ASFALTO, AMARELO, mao_icone)),
        ("jogar_de_novo.png", peca_interface(ti["reiniciar"], 512, 128, AMARELO, GRAFITE_TXT, seta_volta_icone)),
        ("rotulo_pior.png", peca_interface(ti["rotulo_posicao_1"], 256, 128, "#FF6418", BRANCO)),
        ("rotulo_de_boa.png", peca_interface(ti["rotulo_posicao_10"], 256, 128, "#9ED22A", GRAFITE_TXT)),
    ]
    g_if = []
    for nome, im in interface:
        salvar(im, os.path.join(AQUI, "interface", nome))
        g_if.append((f"interface/{nome}", im, f"{im.width}×{im.height}"))
    grupos.append(("Marcadores de posição (marcadores/) · só se o template pedir", g_mk, 140, 140, 10))
    grupos.append(("Textos de interface (interface/) · só se o template mostrar texto em inglês", g_if, 400, 100, 4))

    # ícones
    icones = []
    for estilo, suf in (("claro", ""), ("escuro", "_alt")):
        i162 = icone(162, estilo)
        i512 = icone(512, estilo)
        salvar(i162, os.path.join(AQUI, f"icone{suf}_162.png"))
        salvar(i512, os.path.join(AQUI, f"icone{suf}_512.png"))
        icones.append((f"icone{suf}_162.png", i512))

    # simulações
    ordem10 = [1, 4, 2, 10, 9, 5, 3, 8, 6, 7]
    sim = [
        ("início · carro parado de dia · 512×512",
         celular("carro", "#3C3A44", titulos["titulo.png"][0], quad[1], [], mks, "quadrado")),
        ("meio do jogo · noite · lista com 512×256",
         celular("noite", "#7A7488", titulos["titulo.png"][1], larg[6],
                 [larg[2], None, larg[10], None, larg[4], None, None, larg[9], None, None], mks, "largo")),
        ("fim · sala clara · lista com 512×256",
         celular("sala", "#3C3A44", titulos["titulo.png"][1], None, [larg[k] for k in ordem10], mks, "largo")),
        ("fim · fundo poluído · lista com 512×512",
         celular("confete", "#3C3A44", titulos["titulo.png"][0], None, [quad[k] for k in ordem10], mks,
                 "quadrado")),
    ]
    salvar(previa(grupos, icones, sim), os.path.join(AQUI, "previa.png"))

    # lista de arquivos
    linhas = []
    total = total_sem_previa = 0
    for raiz, dirs, arqs in sorted(os.walk(AQUI)):
        dirs.sort()
        for a in sorted(arqs):
            if a.endswith(".png"):
                p = os.path.join(raiz, a)
                tam = os.path.getsize(p)
                total += tam
                if a != "previa.png":
                    total_sem_previa += tam
                with Image.open(p) as im:
                    linhas.append(f"{os.path.relpath(p, AQUI):42s} {im.width}x{im.height}  {im.mode:5s} "
                                  f"{tam / 1024:7.1f} KB")
    linhas.append("")
    linhas.append(f"TOTAL de todos os PNGs: {total / 1024 / 1024:.2f} MB "
                  f"(sem a previa.png: {total_sem_previa / 1024 / 1024:.2f} MB)")
    with open(os.path.join(AQUI, "lista-de-arquivos.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(linhas) + "\n")
    print("\n".join(linhas))
    print("fonte usada (px, quadrada/larga):", tam_fonte)


if __name__ == "__main__":
    main()
