#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C01 · Torcedômetro: gera TODAS as imagens do efeito.

Como rodar (de qualquer pasta):
    python3 gerar.py

Precisa de: Python 3 + Pillow + numpy.
Fontes (as duas sob SIL Open Font License 1.1, conferido em /usr/share/doc):
  - Inter Display Black/ExtraBold  -> /usr/share/fonts/opentype/inter/
  - Noto Color Emoji               -> /usr/share/fonts/truetype/noto/NotoColorEmoji.ttf
    (no Pillow só funciona com size=109 e embedded_color=True)

Os textos vêm de ../textos.json (linha1/linha2 de cada carta). Se o redator
trocar um texto, basta rodar de novo. As ilustrações de cada carta (emoji
principal + emoji secundário) estão no dicionário ILUSTRA abaixo, pelo número.

Saída (nesta pasta):
  titulo.png, titulo_toque.png ............. 512x256 (título sobre a cabeça)
  cartas/carta_01..26.png .................. 512x256 (sequência do sorteio)
  reservas/reserva_01..04.png .............. 512x256
  quadrado_512/... ......................... os mesmos, centralizados em 512x512
  icone_162.png, icone_alt_162.png ......... ícone de envio (162x162)
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
W, H = 512, 256  # tamanho final de título e cartas

# ---------------------------------------------------------------- paleta
# Paleta neutra (sem par de cores de clube): laranja, violeta, ouro, rosa-magenta.
# Nada de vermelho+branco, verde+branco, preto+branco, nem azul (base colorada).
PALETAS = {
    "laranja": dict(top="#FFB21F", bot="#FF6400", shade="#8A2C00", tint="#FFEBD1"),
    "violeta": dict(top="#A97BFF", bot="#6A2BE0", shade="#2C1070", tint="#EEE5FF"),
    "ouro":    dict(top="#FFDA4A", bot="#FFA600", shade="#7A3A00", tint="#FFF5CC"),
    "magenta": dict(top="#FF6FB3", bot="#E3157A", shade="#7A0A42", tint="#FFE0EE"),
}
ORDEM_CORES = ["laranja", "violeta", "ouro", "magenta"]
GRAFITE = "#1F1A2E"
OURO_TXT = "#FFD84A"

# ---------------------------------------------------------------- ilustrações
# n -> (emoji principal, emoji secundário, extras)
# extras: {"tint_main": "#hex"} recolore o emoji principal; {"chip": "+5"} etiqueta de placar
ILUSTRA = {
    1: ("🛋", "📋", {}),            # técnico de sofá: sofá + prancheta
    2: ("📯", "🏅", {}),            # corneta oficial: corneta + medalha
    3: ("🦶", "🧊", {"tint_main": "#8FD8FF"}),  # pé-frio: pé gelado + gelo
    4: ("🧦", "🍀", {}),            # meia da sorte
    5: ("🌵", "⚽", {}),            # seca até amistoso
    6: ("🎙", "📺", {}),            # narra mais que a TV
    7: ("😭", "🌱", {}),            # sofredor raiz
    8: ("🏃", "⏱", {}),            # sai aos 40
    9: ("🙄", "🚩", {}),            # reclama até de lateral
    10: ("🎉", "⏳", {}),           # comemora antes do VAR
    11: ("📻", "⚽", {}),           # ouve no radinho
    12: ("🥲", "🎵", {}),           # chora no hino
    13: ("🙈", "⚽", {}),           # não olha o pênalti
    14: ("🙏", "🤞", {}),           # reza até no escanteio
    15: ("🤷", "🌿", {}),           # a culpa é do gramado
    16: ("☝", "💬", {}),           # jura que avisou
    17: ("👻", "📱", {}),           # some do grupo (celular genérico, sem app)
    18: ("🗣", "🔊", {"tint_main": "#FF8A1F"}),  # manda áudio (sem app); cabeça laranja (Noto é azul)
    19: ("💓", None, {"chip": "+5"}),  # cardíaco nos acréscimos
    20: ("📼", "⚽", {}),           # ainda fala daquele gol
    21: ("🧮", "📊", {}),           # calculadora da tabela
    22: ("🚗", "📣", {}),           # buzina quando sai gol (carro genérico)
    23: ("🚙", "🚗", {"tint_main": "#8B5CF6"}),  # carreata (carros genéricos); utilitário violeta (Noto é azul)
    24: ("🎮", "👑", {}),           # campeão no videogame (controle genérico)
    25: ("😴", "💤", {}),           # dorme no 1º tempo
    26: ("☔", "🌧", {}),           # torce até na chuva
    # reservas (chave = 100 + n)
    101: ("👕", "🍀", {"tint_main": "#FF8A1F"}),  # camisa lisa recolorida (sem azul)
    102: ("🔎", "⚽", {}),
    103: ("📋", "❌", {}),
    104: ("📺", "😤", {}),
}

# ---------------------------------------------------------------- geometria (em 1x)
BODY = (16, 50, 496, 232)   # x0, y0, x1, y1 do "ingresso"
R_BODY = 30
NOTCH_R = 15                # recortes laterais de ingresso
NOTCH_CY = 160
BORDA = 6                   # borda branca
BADGE_C = (256, 54)         # medalha da ilustração (centro)
BADGE_R = 44
TEXT_AREA = (44, 106, 468, 226)  # x0, y0, x1, y1 onde o texto pode ficar
TAM_MAX = 54                # fonte máxima das cartas (px em 512)
TAM_MIN = 34


def rgb(h, a=255):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def mix(c1, c2, t):
    a, b = rgb(c1) if isinstance(c1, str) else c1, rgb(c2) if isinstance(c2, str) else c2
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(4))


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


def mascara_ingresso(e=0, w=W, h=H, s=S):
    """Forma do ingresso (retângulo arredondado com recortes laterais), expandida em e px."""
    m = Image.new("L", (w * s, h * s), 0)
    d = ImageDraw.Draw(m)
    x0, y0, x1, y1 = BODY
    d.rounded_rectangle([(x0 - e) * s, (y0 - e) * s, (x1 + e) * s, (y1 + e) * s],
                        radius=max(1, R_BODY + e) * s, fill=255)
    rn = NOTCH_R - e
    if rn > 0:
        for cx in (x0, x1):
            d.ellipse([(cx - rn) * s, (NOTCH_CY - rn) * s, (cx + rn) * s, (NOTCH_CY + rn) * s], fill=0)
    return m


def mascara_circulo(cx, cy, r, w=W, h=H, s=S):
    m = Image.new("L", (w * s, h * s), 0)
    ImageDraw.Draw(m).ellipse([(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s], fill=255)
    return m


def uniao(*ms):
    out = ms[0].copy()
    for m in ms[1:]:
        out = Image.fromarray(np.maximum(np.array(out), np.array(m)))
    return out


def deslocar(m, dx, dy):
    out = Image.new(m.mode, m.size, 0)
    out.paste(m, (dx, dy))
    return out


def camada_cor(size, cor, mascara, alpha_mult=1.0):
    c = rgb(cor) if isinstance(cor, str) else cor
    lay = Image.new("RGBA", size, c[:3] + (0,))
    a = mascara if alpha_mult == 1.0 else mascara.point(lambda v: int(v * alpha_mult))
    lay.putalpha(a)
    return lay


def estrela4(d, cx, cy, r, cor):
    """Brilho de 4 pontas."""
    k = r * 0.28
    pts = [(cx, cy - r), (cx + k, cy - k), (cx + r, cy), (cx + k, cy + k),
           (cx, cy + r), (cx - k, cy + k), (cx - r, cy), (cx - k, cy - k)]
    d.polygon(pts, fill=cor)


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


def recolorir(im, cor):
    """Recolore mantendo luz e sombra (usado no pé gelado e na camisa lisa)."""
    arr = np.array(im).astype(np.float32)
    lum = (0.299 * arr[..., 0] + 0.587 * arr[..., 1] + 0.114 * arr[..., 2]) / 255.0
    alvo = np.array(rgb(cor)[:3], np.float32)
    base = alvo[None, None, :] * (0.62 + 0.62 * lum[..., None])
    branco = np.clip((lum - 0.82) * 3.0, 0, 1)[..., None]
    novo = base * (1 - branco) + 255 * branco
    arr[..., :3] = np.clip(novo, 0, 255)
    return Image.fromarray(arr.astype(np.uint8), "RGBA")


def com_contorno(im, px, cor="#FFFFFF"):
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


# ---------------------------------------------------------------- bola e medidor (desenho próprio)
def bola(tam, linha=GRAFITE):
    """Bola de futebol simples, desenhada (sem emoji). tam = diâmetro em px."""
    r = tam / 2
    lay = Image.new("RGBA", (tam, tam), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.ellipse([0, 0, tam - 1, tam - 1], fill=rgb("#FFFFFF"))
    cx = cy = r
    ang0 = -90
    lw = max(1, int(r * 0.07))

    def pol(px, py, raio, giro):
        return [(px + raio * math.cos(math.radians(giro + 72 * k)),
                 py + raio * math.sin(math.radians(giro + 72 * k))) for k in range(5)]

    centro = pol(cx, cy, r * 0.33, ang0)               # pentágono do meio
    d.polygon(centro, fill=rgb(linha))
    fora = []
    for i in range(5):                                   # pentágonos cortados na borda
        a2 = ang0 + 36 + 72 * i
        ox, oy = cx + r * 1.04 * math.cos(math.radians(a2)), cy + r * 1.04 * math.sin(math.radians(a2))
        p = pol(ox, oy, r * 0.30, a2 + 180)
        fora.append(p)
        d.polygon(p, fill=rgb(linha))
    for i in range(5):                                   # costuras: vértice -> "Y" -> pentágonos vizinhos
        a = math.radians(ang0 + 72 * i)
        mx, my = cx + r * 0.60 * math.cos(a), cy + r * 0.60 * math.sin(a)
        d.line([centro[i], (mx, my)], fill=rgb(linha), width=lw)
        for viz in (fora[i], fora[(i - 1) % 5]):
            alvo = min(viz, key=lambda q: (q[0] - mx) ** 2 + (q[1] - my) ** 2)
            d.line([(mx, my), alvo], fill=rgb(linha), width=lw)
        d.ellipse([mx - lw / 2, my - lw / 2, mx + lw / 2, my + lw / 2], fill=rgb(linha))
    m = Image.new("L", (tam, tam), 0)
    ImageDraw.Draw(m).ellipse([0, 0, tam - 1, tam - 1], fill=255)
    lay.putalpha(Image.fromarray(np.minimum(np.array(lay.split()[3]), np.array(m))))
    d = ImageDraw.Draw(lay)
    d.ellipse([lw / 2, lw / 2, tam - 1 - lw / 2, tam - 1 - lw / 2], outline=rgb(linha), width=lw)
    # brilho
    br = Image.new("L", (tam, tam), 0)
    ImageDraw.Draw(br).ellipse([tam * 0.18, tam * 0.10, tam * 0.55, tam * 0.36], fill=70)
    br = br.filter(ImageFilter.GaussianBlur(tam * 0.04))
    lay.alpha_composite(camada_cor((tam, tam), "#FFFFFF", Image.fromarray(
        np.minimum(np.array(br), np.array(m)))))
    return lay


def medidor(tam, estilo="claro", ang_ponteiro=-28):
    """'Torcedômetro': mostrador tipo velocímetro com bola no centro (desenho próprio)."""
    t = tam
    lay = Image.new("RGBA", (t, t), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    if estilo == "claro":
        d.ellipse([0, 0, t - 1, t - 1], fill=rgb("#FFFFFF"))
        d.ellipse([t * 0.035, t * 0.035, t * 0.965, t * 0.965], fill=rgb("#FFF8EE"))
        cor_tick, cor_ponteiro = rgb("#3A3150"), rgb(GRAFITE)
    else:
        d.ellipse([0, 0, t - 1, t - 1], fill=rgb("#3B2F5C"))
        d.ellipse([t * 0.035, t * 0.035, t * 0.965, t * 0.965], fill=rgb("#17122A"))
        cor_tick, cor_ponteiro = rgb("#CFC6EA"), rgb("#FFFFFF")
    c = t / 2
    # arco colorido (gradiente ouro -> laranja -> magenta), abertura embaixo
    ini, fim = 140, 400
    rr, esp = t * 0.385, t * 0.11
    cores = ["#FFD43B", "#FF8A00", "#FF2E88"]
    passos = 90
    for i in range(passos):
        f = i / (passos - 1)
        cor = mix(cores[0], cores[1], f * 2) if f < 0.5 else mix(cores[1], cores[2], (f - 0.5) * 2)
        a0 = ini + (fim - ini) * i / passos
        a1 = ini + (fim - ini) * (i + 1.6) / passos
        d.arc([c - rr, c - rr, c + rr, c + rr], a0, min(a1, fim), fill=cor, width=int(esp))
    for ang, cor in ((ini, cores[0]), (fim, cores[2])):  # pontas arredondadas
        rm = rr - esp / 2
        px, py = c + rm * math.cos(math.radians(ang)), c + rm * math.sin(math.radians(ang))
        d.ellipse([px - esp / 2, py - esp / 2, px + esp / 2, py + esp / 2], fill=rgb(cor))
    if estilo != "claro":  # brilho neon
        glow = lay.filter(ImageFilter.GaussianBlur(t * 0.03))
        lay = Image.alpha_composite(glow, lay)
        d = ImageDraw.Draw(lay)
    # marquinhas
    for k in range(9):
        ang = math.radians(ini + (fim - ini) * k / 8)
        r1, r2 = t * 0.235, t * (0.275 if k % 2 == 0 else 0.258)
        d.line([(c + r1 * math.cos(ang), c + r1 * math.sin(ang)), (c + r2 * math.cos(ang), c + r2 * math.sin(ang))],
               fill=cor_tick, width=max(1, int(t * 0.022)))
    # ponteiro
    a = math.radians(ang_ponteiro)
    comp, base = t * 0.36, t * 0.045
    ponta = (c + comp * math.cos(a), c + comp * math.sin(a))
    perp = a + math.pi / 2
    p1 = (c + base * math.cos(perp), c + base * math.sin(perp))
    p2 = (c - base * math.cos(perp), c - base * math.sin(perp))
    traseira = (c - t * 0.06 * math.cos(a), c - t * 0.06 * math.sin(a))
    d.polygon([ponta, p1, traseira, p2], fill=cor_ponteiro)
    # bola no centro
    b = bola(int(t * 0.30), linha=GRAFITE)
    b = com_contorno(b, max(2, int(t * 0.018)), "#FFFFFF")
    colar_centro(lay, b, c, c)
    return lay


# ---------------------------------------------------------------- texto
def medir_fonte(linhas, largura, tam_max, tam_min, arquivo=F_BLACK):
    d = ImageDraw.Draw(Image.new("L", (10, 10)))
    for tam in range(tam_max, tam_min - 1, -1):
        f = ImageFont.truetype(arquivo, tam * S)
        sw = max(3, round(tam * 0.085)) * S
        if max(d.textlength(l, font=f) for l in linhas) + 2 * sw <= largura * S:
            return tam, f, sw
    raise SystemExit(f"texto não coube nem com {tam_min}px: {linhas}")


def desenhar_texto(img, linhas, area, cor_contorno, cores_linha=("#FFFFFF", "#FFFFFF"),
                   tam_max=TAM_MAX, tam_min=TAM_MIN, tamanhos=None, arquivo=F_BLACK):
    """Desenha 1 ou 2 linhas centralizadas, com contorno e sombra dura. Reduz a fonte se precisar."""
    x0, y0, x1, y1 = area
    d = ImageDraw.Draw(img)
    if tamanhos is None:
        tam, f, sw = medir_fonte(linhas, x1 - x0, tam_max, tam_min, arquivo)
        fontes = [(tam, f, sw)] * len(linhas)
    else:  # tamanhos diferentes por linha (título)
        fontes = [medir_fonte([l], x1 - x0, t, tam_min, arquivo) for l, t in zip(linhas, tamanhos)]
    caps = [-fo[1].getbbox("H", anchor="ls")[1] for fo in fontes]
    acento = [-fo[1].getbbox("ÊÁÉÍÃ", anchor="ls")[1] for fo in fontes]
    # entrelinha: altura da maiúscula + espaço do acento + contorno (acento nunca encosta na linha de cima)
    alt = caps[0]
    bases = [caps[0]]
    for i in range(1, len(linhas)):
        alt += caps[i] + (acento[i] - caps[i]) * 0.85 + fontes[i][2] * 1.0
        bases.append(alt)
    cy = (y0 + y1) / 2 * S
    topo = cy - alt / 2
    # garante espaço para acento da 1ª linha
    tem_acento_1 = any(ch in linhas[0] for ch in "ÁÃÉÊÍÓÔÕÚÇÀ")
    if tem_acento_1 and topo - (acento[0] - caps[0]) < y0 * S:
        topo = y0 * S + (acento[0] - caps[0])
    cx = (x0 + x1) / 2 * S
    sombra = max(3, round(fontes[0][0] * 0.07)) * S
    for i, l in enumerate(linhas):
        tam, f, sw = fontes[i]
        yb = topo + bases[i]
        d.text((cx, yb + sombra), l, font=f, anchor="ms", fill=rgb(cor_contorno),
               stroke_width=sw, stroke_fill=rgb(cor_contorno))
    for i, l in enumerate(linhas):
        tam, f, sw = fontes[i]
        yb = topo + bases[i]
        d.text((cx, yb), l, font=f, anchor="ms", fill=rgb(cores_linha[i]),
               stroke_width=sw, stroke_fill=rgb(cor_contorno))
    return [fo[0] for fo in fontes]


# ---------------------------------------------------------------- o "ingresso" (moldura própria)
def ingresso(corpo_rgba, shade, desenhar_medalha, extras_fundo=True, seed=0):
    """Monta a moldura: sombra, borda branca, corpo, brilho, pontilhado, medalha."""
    size = (W * S, H * S)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    cx, cy = BADGE_C
    m_borda = uniao(mascara_ingresso(BORDA), mascara_circulo(cx, cy, BADGE_R + BORDA))
    # sombra suave (para ler em qualquer fundo)
    sombra = deslocar(m_borda, 0, 5 * S).filter(ImageFilter.GaussianBlur(5 * S))
    img.alpha_composite(camada_cor(size, "#120A22", sombra, 0.55))
    # sombra dura (espessura de adesivo)
    img.alpha_composite(camada_cor(size, shade, deslocar(m_borda, 0, 5 * S)))
    # borda branca
    img.alpha_composite(camada_cor(size, "#FFFFFF", m_borda))
    # corpo
    m_corpo = mascara_ingresso(0)
    corpo = corpo_rgba.copy()
    corpo.putalpha(m_corpo)
    img.alpha_composite(corpo)
    # brilho no topo
    gl = Image.new("L", size, 0)
    gd = ImageDraw.Draw(gl)
    for i in range(60):
        yy = BODY[1] + i * (BODY[3] - BODY[1]) * 0.5 / 60
        gd.line([(0, yy * S), (W * S, yy * S)], fill=int(70 * (1 - i / 60)), width=S * 2)
    gl = Image.fromarray(np.minimum(np.array(gl), np.array(m_corpo)))
    img.alpha_composite(camada_cor(size, "#FFFFFF", gl))
    if extras_fundo:
        # meio-tom (bolinhas) nos cantos
        ht = Image.new("L", size, 0)
        hd = ImageDraw.Draw(ht)
        passo = 13
        for (ox, oy) in ((BODY[2], BODY[3]), (BODY[0], BODY[1])):
            for gx in range(BODY[0], BODY[2] + 1, passo):
                for gy in range(BODY[1], BODY[3] + 1, passo):
                    dist = math.hypot(gx - ox, gy - oy)
                    if dist < 150:
                        r = 3.6 * (1 - dist / 150)
                        if r > 0.5:
                            hd.ellipse([(gx - r) * S, (gy - r) * S, (gx + r) * S, (gy + r) * S], fill=46)
        ht = Image.fromarray(np.minimum(np.array(ht), np.array(m_corpo)))
        img.alpha_composite(camada_cor(size, "#FFFFFF", ht))
    # linha interna fina (acabamento de ingresso)
    linha = Image.fromarray(np.clip(np.array(mascara_ingresso(-7)).astype(int)
                                    - np.array(mascara_ingresso(-9)).astype(int), 0, 255).astype(np.uint8))
    img.alpha_composite(camada_cor(size, "#FFFFFF", linha, 0.40))
    # brilhos de 4 pontas dos lados da medalha
    d = ImageDraw.Draw(img)
    for (x, y, r, a) in ((176, 76, 9, 230), (156, 66, 5, 190), (336, 76, 9, 230), (356, 66, 5, 190)):
        estrela4(d, x * S, y * S, r * S, (255, 255, 255, a))
    # sombrinha da medalha sobre o corpo
    ms = deslocar(mascara_circulo(cx, cy, BADGE_R + BORDA), 0, 4 * S)
    ms = Image.fromarray(np.minimum(np.array(ms), np.array(m_corpo)))
    img.alpha_composite(camada_cor(size, shade, ms, 0.55))
    # medalha (aro branco + miolo)
    img.alpha_composite(camada_cor(size, "#FFFFFF", mascara_circulo(cx, cy, BADGE_R + BORDA)))
    desenhar_medalha(img)
    return img


def medalha_emoji(principal, secundario, tint, extras):
    def f(img):
        cx, cy = BADGE_C[0] * S, BADGE_C[1] * S
        r = BADGE_R * S
        # miolo com gradiente radial claro
        mi = Image.new("RGBA", (2 * r, 2 * r), (0, 0, 0, 0))
        yy, xx = np.mgrid[0:2 * r, 0:2 * r].astype(np.float32)
        dist = np.sqrt((xx - r * 0.8) ** 2 + (yy - r * 0.7) ** 2) / (r * 1.4)
        c1, c2 = np.array(rgb("#FFFFFF"), np.float32), np.array(rgb(tint), np.float32)
        arr = (c1[None, None, :] * (1 - dist[..., None].clip(0, 1)) + c2[None, None, :] * dist[..., None].clip(0, 1))
        mi = Image.fromarray(arr.clip(0, 255).astype(np.uint8), "RGBA")
        mm = Image.new("L", (2 * r, 2 * r), 0)
        ImageDraw.Draw(mm).ellipse([0, 0, 2 * r - 1, 2 * r - 1], fill=255)
        mi.putalpha(mm)
        img.alpha_composite(mi, (cx - r, cy - r))
        # emoji principal
        e1 = emoji(principal, int(r * 1.36))
        if extras.get("tint_main"):
            e1 = recolorir(e1, extras["tint_main"])
        e1s, pad = com_sombra(e1, 0, int(1.5 * S), 2 * S, 0.25)
        dx = -0.10 * r if (secundario or extras.get("chip")) else 0
        colar_centro(img, e1s, cx + dx, cy - 0.02 * r)
        # emoji secundário (adesivo inclinado, com contorno branco)
        if secundario:
            e2 = emoji(secundario, int(r * 0.88))
            e2 = com_contorno(e2, int(2.6 * S))
            e2 = e2.rotate(-12, resample=Image.BICUBIC, expand=True)
            e2s, _ = com_sombra(e2, 0, int(1.5 * S), 2 * S, 0.30)
            colar_centro(img, e2s, cx + 0.62 * r, cy + 0.50 * r)
        if extras.get("chip"):
            chip(img, extras["chip"], cx + 0.66 * r, cy + 0.52 * r)
    return f


def chip(img, texto, cx, cy):
    """Etiqueta de placar escura com número em amarelo (ex.: '+5' dos acréscimos)."""
    f = ImageFont.truetype(F_BLACK, 24 * S)
    d = ImageDraw.Draw(img)
    w = d.textlength(texto, font=f) + 16 * S
    h = 32 * S
    box = [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2]
    d.rounded_rectangle([box[0] - 3 * S, box[1] - 3 * S, box[2] + 3 * S, box[3] + 3 * S], radius=10 * S,
                        fill=rgb("#FFFFFF"))
    d.rounded_rectangle(box, radius=8 * S, fill=rgb(GRAFITE))
    d.text((cx, cy + 1 * S), texto, font=f, anchor="mm", fill=rgb(OURO_TXT))


def medalha_medidor(img):
    cx, cy = BADGE_C[0] * S, BADGE_C[1] * S
    r = BADGE_R * S
    m = medidor(2 * r, "claro")
    colar_centro(img, m, cx, cy)


def reduzir(img):
    return img.resize((img.width // S, img.height // S), Image.LANCZOS)


# ---------------------------------------------------------------- peças
def carta(item, paleta_nome, chave_ilustra):
    p = PALETAS[paleta_nome]
    corpo = gradiente(W * S, H * S, [(0, p["top"]), (1, p["bot"])], (0.18, 0.82))
    principal, secundario, extras = ILUSTRA[chave_ilustra]
    img = ingresso(corpo, p["shade"], medalha_emoji(principal, secundario, p["tint"], extras))
    tam = desenhar_texto(img, [item["linha1"], item["linha2"]], TEXT_AREA, p["shade"])
    return reduzir(img), tam[0]


def titulo(com_toque=False):
    corpo = gradiente(W * S, H * S, [(0, "#7A35F0"), (0.55, "#E9338C"), (1, "#FF8A00")], (0.85, 0.15))
    img = ingresso(corpo, "#2C1070", medalha_medidor)
    if com_toque:
        area = (44, 100, 468, 196)
        desenhar_texto(img, ["QUE TORCEDOR", "VOCÊ É?"], area, "#2C1070", ("#FFFFFF", OURO_TXT),
                       tamanhos=(42, 54), tam_min=28)
        pilula_toque(img)
    else:
        desenhar_texto(img, ["QUE TORCEDOR", "VOCÊ É?"], (44, 102, 468, 226), "#2C1070",
                       ("#FFFFFF", OURO_TXT), tamanhos=(46, 62), tam_min=30)
    return reduzir(img)


def pilula_toque(img):
    """Pílula 'TOQUE NA TELA' com mãozinha, presa na borda de baixo."""
    f = ImageFont.truetype(F_BLACK, 19 * S)
    d = ImageDraw.Draw(img)
    txt = "TOQUE NA TELA"
    tw = d.textlength(txt, font=f)
    mao = emoji("👆", 24 * S)
    w = tw + mao.width + 30 * S
    h = 34 * S
    cx, cy = 256 * S, 219 * S
    box = [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2]
    d.rounded_rectangle([box[0] - 3 * S, box[1] - 3 * S, box[2] + 3 * S, box[3] + 3 * S], radius=20 * S,
                        fill=rgb("#FFFFFF"))
    d.rounded_rectangle(box, radius=17 * S, fill=rgb(GRAFITE))
    x = box[0] + 12 * S
    img.alpha_composite(mao, (int(x), int(cy - mao.height / 2)))
    d.text((x + mao.width + 7 * S, cy + 1 * S), txt, font=f, anchor="lm", fill=rgb("#FFFFFF"))


def icone(tam_final=162, estilo="claro"):
    t = 648 if tam_final <= 162 else tam_final * 2   # desenha grande e reduz
    if estilo == "claro":
        img = gradiente(t, t, [(0, "#7A35F0"), (0.55, "#E9338C"), (1, "#FF8A00")], (0.5, 0.5))
    else:
        img = gradiente(t, t, [(0, "#2A1D4E"), (1, "#120C22")], (0.3, 0.7))
        glow = Image.new("L", (t, t), 0)
        ImageDraw.Draw(glow).ellipse([t * 0.12, t * 0.12, t * 0.88, t * 0.88], fill=150)
        glow = glow.filter(ImageFilter.GaussianBlur(t * 0.08))
        img.alpha_composite(camada_cor((t, t), "#8B3DFF", glow, 0.6))
    # brilhos no fundo
    d = ImageDraw.Draw(img)
    for (x, y, r, a) in ((0.15, 0.17, 0.045, 220), (0.86, 0.16, 0.03, 200), (0.88, 0.84, 0.04, 210),
                         (0.12, 0.85, 0.025, 180)):
        estrela4(d, x * t, y * t, r * t, (255, 255, 255, a))
    diam = int(t * 0.84)
    m = medidor(diam, estilo)
    ms, pad = com_sombra(m, 0, int(t * 0.02), int(t * 0.025), 0.40, "#12061F")
    colar_centro(img, ms, t / 2, t / 2 + t * 0.01)
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
    """Fundos falsos para testar a leitura (sala clara, noite, campo, confete)."""
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
    elif tipo == "campo":
        im = Image.new("RGBA", (w, h), rgb("#2E7D32"))
        d = ImageDraw.Draw(im)
        faixa = h // 10
        for i in range(10):
            if i % 2:
                d.rectangle([0, i * faixa, w, (i + 1) * faixa], fill=rgb("#388E3C"))
        d.rectangle([0, 0, w, h * 0.33], fill=rgb("#2B2A33"))
        for _ in range(260):
            x, y = rnd.uniform(0, w), rnd.uniform(0, h * 0.33)
            c = rnd.choice(["#F2F2F2", "#FFC857", "#9E9E9E", "#E57373", "#64B5F6", "#FFFFFF"])
            d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=rgb(c))
        d.line([(0, h * 0.62), (w, h * 0.58)], fill=rgb("#FFFFFF", 200), width=5)
    else:  # confete: fundo bem poluído
        im = Image.new("RGBA", (w, h), rgb("#FFF3D6"))
        d = ImageDraw.Draw(im)
        for _ in range(420):
            x, y = rnd.uniform(0, w), rnd.uniform(0, h)
            c = rnd.choice(["#FF6400", "#A97BFF", "#FFDA4A", "#E3157A", "#1F1A2E", "#FFFFFF", "#22C1C3"])
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
    return topo


def celular(peca, tipo, rotulo_cor="#222", largura_peca=0.66, cor_sil="#3C3A44"):
    w, h = 405, 720
    im = foto_generica(w, h, tipo)
    topo_cab = int(h * 0.40)
    silhueta(im, w / 2, topo_cab, w * 0.70, cor_sil)
    pw = int(w * largura_peca)
    ph = int(peca.height * pw / peca.width)
    p = peca.resize((pw, ph), Image.LANCZOS)
    im.alpha_composite(p, (int(w / 2 - pw / 2), int(topo_cab - ph - 8)))
    # cantos de celular
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


def previa(pecas, icones, cartas_longas):
    fundo = rgb("#F5F2FA")
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
    d.text((MARG, 36), "C01 · Torcedômetro — prévia das imagens", font=f_h1, fill=rgb(GRAFITE))
    d.text((MARG, 92), "Xadrez = transparente. Título e cartas: 512×256 (miniaturas aqui a 400×200). "
                       "Ordem da grade = ordem dos arquivos. Ícone de envio: 162×162.",
           font=f_sm, fill=rgb("#5B5470"))
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
        d.text((x, y + TH + 30), legenda, font=f_sm, fill=rgb("#6B6480"))
    # ícones como aparecem no app
    y = y0 + alt_grade + 10
    d.text((MARG, y), "Ícone como aparece no app (cantos arredondados pelo próprio app): 162, 96 e 64 px",
           font=f_h2, fill=rgb(GRAFITE))
    x = MARG
    y += 50
    for nome, ic in icones:
        for tam in (162, 96, 64):
            a = arredondar(ic.resize((tam, tam), Image.LANCZOS))
            sheet.alpha_composite(a, (x, y + (162 - tam)))
            x += tam + 18
        d.text((x - 3 * 18 - 162 - 96 - 64 + 18, y + 172), nome, font=f_lb, fill=rgb(GRAFITE))
        x += 60
    # área segura
    ic = icones[0][1].resize((162, 162), Image.LANCZOS).convert("RGBA")
    dd = ImageDraw.Draw(ic)
    dd.rectangle([9, 9, 152, 152], outline=rgb("#00E5FF"), width=1)
    sheet.alpha_composite(ic, (x, y))
    d.text((x, y + 172), "linha ciano = área segura 144×144", font=f_sm, fill=rgb("#5B5470"))
    # simulações
    y = y0 + alt_grade + alt_icones
    d.text((MARG, y), "Simulação sobre fotos genéricas (largura da peça ≈ 66% da tela)", font=f_h2,
           fill=rgb(GRAFITE))
    y += 50
    sims = [
        ("título · sala clara", pecas[0][1], "sala", "#3C3A44"),
        (f"{cartas_longas[0][0]} · fundo escuro", cartas_longas[0][1], "noite", "#7A7488"),
        (f"{cartas_longas[1][0]} · campo", cartas_longas[1][1], "campo", "#2A2830"),
        (f"{cartas_longas[2][0]} · fundo poluído", cartas_longas[2][1], "confete", "#3C3A44"),
    ]
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
    relatorio = []

    for com_toque, nome in ((False, "titulo.png"), (True, "titulo_toque.png")):
        t = titulo(com_toque)
        salvar(t, os.path.join(AQUI, nome))
        salvar(quadrado(t), os.path.join(AQUI, "quadrado_512", nome))
        pecas.append((nome, t, "título" + (" + aviso de toque (opcional)" if com_toque else " (antes do toque)")))

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
    for estilo, sufixo in (("claro", ""), ("escuro", "_alt")):
        ic162 = icone(162, estilo)
        ic512 = icone(512, estilo)
        salvar(ic162, os.path.join(AQUI, f"icone{sufixo}_162.png"))
        salvar(ic512, os.path.join(AQUI, f"icone{sufixo}_512.png"))
        icones.append((f"icone{sufixo}_162.png", ic512))
        pecas.append((f"icone{sufixo}_162.png", ic512.convert("RGBA"),
                      "ícone de envio" + (" (alternativo, escuro)" if sufixo else " (principal)")))

    # cartas com mais texto / menor fonte para a simulação
    ordem = sorted(imgs, key=lambda n: tamanhos[n])
    longas = [(n, imgs[n]) for n in ordem[:3]]
    salvar(previa(pecas, icones, longas), os.path.join(AQUI, "previa.png"))

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
