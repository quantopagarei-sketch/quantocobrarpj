#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C07 · Simpatia da Virada: gera TODAS as imagens do efeito.

Como rodar (de qualquer pasta):
    python3 gerar.py

Precisa de: Python 3 + Pillow + numpy.
Fontes (as duas sob SIL Open Font License 1.1):
  - Inter Display Black/ExtraBold  -> /usr/share/fonts/opentype/inter/
  - Noto Color Emoji               -> /usr/share/fonts/truetype/noto/NotoColorEmoji.ttf
    (no Pillow só funciona com size=109 e embedded_color=True)

Mesmo template e mesmo enquadramento do C01 (Randomizer 2D, peças 512x256),
mas com identidade própria: "bilhete de desejo" de Réveillon. O corpo é
roxo-uva escuro (céu da meia-noite), a borda é dourada, há confete, fogos
pequenos no céu, pontas dobradas e um selo dourado ondulado com o desenho.

Os textos vêm de ../textos.json (linha1/linha2 de cada carta). Se o redator
trocar um texto, basta rodar de novo. O desenho de cada carta está no
dicionário ILUSTRA, pelo número. Os campos "extras_desenho" do JSON
(tint_main, tint_secundario) também são lidos.

Desenhos próprios (sem emoji): cacho de uva, romã, moeda sem valor, seta,
estrela cadente, relógio da meia-noite e fogos. Motivo: não existe emoji de
romã; os emojis Noto de fogos e estrela cadente vêm num quadrado escuro; a
seta Noto é um botão cinza; a moeda Noto tem um prédio gravado.

Saída (nesta pasta):
  titulo_toque.png, titulo.png ............. 512x256 (título sobre a cabeça)
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
W, H = 512, 256  # tamanho final de título e cartas (igual ao C01)

# ---------------------------------------------------------------- paleta
# Céu da meia-noite em 3 tons (alternam no giro) + dourado + confete.
# Nada de vermelho+branco, verde+branco, preto+branco ou azul+preto+branco.
PALETAS = {
    "uva":    dict(top="#5E2DAE", bot="#2A0D66", shade="#150432", tint="#EFE6FF"),
    "ameixa": dict(top="#912C8A", bot="#4A0E55", shade="#21052A", tint="#FFE4F5"),
    "anil":   dict(top="#4A36BE", bot="#1E166E", shade="#0D0A3B", tint="#E6E6FF"),
}
ORDEM_CORES = ["uva", "ameixa", "anil"]
NOITE = "#150432"
OURO_TXT = "#FFD84A"
OURO_CLARO, OURO, OURO_ESCURO, OURO_SOMBRA = "#FFF3B0", "#FFCF3F", "#D9920F", "#6B4200"
CONFETE = ["#FFD24A", "#FF6FB5", "#3FE0D0", "#FFFFFF", "#FFB23F", "#C9A2FF"]

# ---------------------------------------------------------------- ilustrações
# n -> (emoji principal, secundário, extras)
#   principal/secundário: emoji, ou "@nome" para desenho próprio (roma, moeda, seta, estrela_cadente, uvas)
#   extras:
#     tint_main / tint_secundario: recolore o principal / o secundário (#hex)
#     terceiro: (emoji, dx, dy, escala, giro) adesivo extra, posição em frações do raio do selo
#     pontos: (cor, cx, cy, rx, ry, n, raio) pontinhos sobre o principal (lentilha, uva-passa), em frações
#     interior: (cor1, cor2) fundo do selo diferente (quando o desenho é branco)
#     interior_emoji: emoji que preenche o selo inteiro, recortado em círculo
GOTAS_LENTILHA = ("#A3561F", 0.47, 0.30, 0.30, 0.075, 26, 0.050)
GOTAS_PASSA = ("#4B1F3D", 0.50, 0.25, 0.30, 0.15, 11, 0.050)
ILUSTRA = {
    1: ("🌊", "🪣", {}),                      # 7 ondas no balde
    2: ("🙅", "💔", {}),                      # não mandar oi pro ex
    3: ("🥣", "💰", {"pontos": GOTAS_LENTILHA}),  # tigela de lentilha + saquinho
    4: ("🪑", "📈", {}),                      # cadeira PARADA + gráfico subindo
    5: ("🤍", "🧦", {"interior": ("#C8B3F7", "#8E6FE0")}),  # tudo branco; meia recolorida (JSON)
    6: ("⏰", "😴", {}),                      # madrugar no dia 1º
    7: ("🍇", "🗓", {}),                      # 12 uvas + calendário
    8: ("🧳", "✈", {}),                       # volta com mala vazia
    9: ("👛", "@roma", {"terceiro": ("🕸", -0.62, -0.42, 0.50, 10)}),  # romã + carteira vazia (teia)
    10: ("🤗", "🍮", {}),                     # abraço + sobremesa genérica
    11: ("🦘", "🕛", {}),                     # 3 pulinhos à meia-noite
    12: ("🤫", "💛", {}),                     # psiu + coração amarelo (sem roupa íntima)
    13: ("🧾", "😅", {}),                     # conta genérica + suor
    14: ("🧹", "💨", {}),                     # varrer o azar
    15: ("🐔", "🚫", {}),                     # frango não
    16: ("❤", "👀", {}),                      # algo vermelho pro crush
    17: ("📝", "✨", {}),                     # 12 desejos no papel (nada de queimar)
    18: ("🚗", "🧽", {"terceiro": ("✨", -0.66, -0.46, 0.46, 0)}),  # carro genérico parado, limpinho
    19: ("👟", "@seta", {}),                  # pé direito: tênis liso + seta
    20: ("📵", "🙌", {}),                     # sem celular
    21: ("👞", "@moeda", {}),                 # moeda dourada sem valor no sapato
    22: ("🍚", "🤔", {"pontos": GOTAS_PASSA}),  # arroz com uva-passa
    23: ("🚪", "🌟", {}),                     # porta aberta pro ano entrar
    24: ("👕", "🏷", {}),                     # camiseta lisa recolorida (JSON) + etiqueta
    25: ("👵", "📞", {}),                     # ligar pra vó
    26: (None, "@estrela_cadente", {"interior_emoji": "🎆"}),  # fogos no céu + estrela cadente
    # reservas (chave = 100 + n)
    101: ("👛", "🍃", {}),                    # R1 folha de louro na carteira
    102: ("💚", "🍀", {}),                    # R2 peça verde pra saúde
    103: ("👖", "💰", {}),                    # R3 grana no bolso
    104: ("🏖", "☀", {}),                     # R4 banho de mar no dia 1º
}

# ---------------------------------------------------------------- geometria (em 1x)
BODY = (16, 50, 496, 232)   # x0, y0, x1, y1 do bilhete (mesmo lugar do ingresso do C01)
R_BODY = 18
DOBRA = 22                  # pontas dobradas (canto sup. esquerdo e inf. direito)
BORDA = 6                   # borda dourada
SELO_C = (256, 54)          # selo dourado com o desenho (centro)
SELO_R = 42                 # miolo do selo
SELO_ARO = 7                # aro dourado
SELO_ONDAS, SELO_AMP = 18, 2.4
TEXT_AREA = (44, 106, 468, 226)  # onde o texto pode ficar (424 px, igual ao C01)
TAM_MAX = 54
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


def radial(w, h, cx, cy, r, paradas):
    """Gradiente radial: paradas = [(pos 0..1, '#hex'), ...] a partir de (cx, cy)."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    t = np.clip(np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / max(r, 1e-6), 0, 1)
    out = np.zeros((h, w, 4), np.float32)
    pos = [p for p, _ in paradas]
    cores = [np.array(rgb(c), np.float32) for _, c in paradas]
    for ch in range(4):
        out[..., ch] = np.interp(t, pos, [c[ch] for c in cores])
    return Image.fromarray(out.clip(0, 255).astype(np.uint8), "RGBA")


def mascara_bilhete(e=0, s=S):
    """Bilhete: retângulo arredondado com as pontas sup. esq. e inf. dir. cortadas (dobradas)."""
    m = Image.new("L", (W * s, H * s), 0)
    d = ImageDraw.Draw(m)
    x0, y0, x1, y1 = BODY
    d.rounded_rectangle([(x0 - e) * s, (y0 - e) * s, (x1 + e) * s, (y1 + e) * s],
                        radius=max(1, R_BODY + e) * s, fill=255)
    r2 = math.sqrt(2)
    k_tl = x0 + y0 + DOBRA - e * r2          # linha x + y = k
    k_br = x1 + y1 - DOBRA + e * r2
    xs, ys = x0 - e - 10, y0 - e - 10
    d.polygon([((k_tl - ys) * s, ys * s), (xs * s, (k_tl - xs) * s), (xs * s, ys * s)], fill=0)
    xb, yb = x1 + e + 10, y1 + e + 10
    d.polygon([((k_br - yb) * s, yb * s), (xb * s, (k_br - xb) * s), (xb * s, yb * s)], fill=0)
    return m


def pontos_selo(cx, cy, r, amp, ondas, s=S, n=720):
    return [((cx + (r + amp * math.cos(ondas * 2 * math.pi * i / n)) * math.cos(2 * math.pi * i / n)) * s,
             (cy + (r + amp * math.cos(ondas * 2 * math.pi * i / n)) * math.sin(2 * math.pi * i / n)) * s)
            for i in range(n)]


def mascara_selo(e=0, s=S):
    """Selo ondulado (borda de 'rosácea')."""
    m = Image.new("L", (W * s, H * s), 0)
    cx, cy = SELO_C
    ImageDraw.Draw(m).polygon(pontos_selo(cx, cy, SELO_R + SELO_ARO + e, SELO_AMP, SELO_ONDAS, s), fill=255)
    return m


def mascara_circulo(cx, cy, r, w=W, h=H, s=S):
    m = Image.new("L", (w * s, h * s), 0)
    ImageDraw.Draw(m).ellipse([(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s], fill=255)
    return m


def uniao(*ms):
    out = np.array(ms[0])
    for m in ms[1:]:
        out = np.maximum(out, np.array(m))
    return Image.fromarray(out)


def intersecao(a, b):
    return Image.fromarray(np.minimum(np.array(a), np.array(b)))


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


def com_mascara(im, mascara):
    """Aplica uma máscara L sobre o alfa de uma imagem RGBA."""
    out = im.copy()
    out.putalpha(intersecao(im.split()[3], mascara))
    return out


def estrela4(d, cx, cy, r, cor):
    """Brilho de 4 pontas."""
    k = r * 0.28
    pts = [(cx, cy - r), (cx + k, cy - k), (cx + r, cy), (cx + k, cy + k),
           (cx, cy + r), (cx - k, cy + k), (cx - r, cy), (cx - k, cy - k)]
    d.polygon(pts, fill=cor)


def estrela5(cx, cy, r_ext, r_int, giro=-90):
    return [(cx + (r_ext if i % 2 == 0 else r_int) * math.cos(math.radians(giro + 36 * i)),
             cy + (r_ext if i % 2 == 0 else r_int) * math.sin(math.radians(giro + 36 * i))) for i in range(10)]


def explosao(d, cx, cy, r, cor, n=12, giro=0.0, larg=None):
    """Fogos no céu: raios com pontinha redonda e um miolo (coordenadas já na escala final)."""
    c = rgb(cor) if isinstance(cor, str) else cor
    w = larg or max(1, r * 0.085)
    for k in range(n):
        a = math.radians(giro + 360 * k / n)
        r0, r1 = r * 0.36, r * (1.0 if k % 2 == 0 else 0.76)
        p0 = (cx + r0 * math.cos(a), cy + r0 * math.sin(a))
        p1 = (cx + r1 * math.cos(a), cy + r1 * math.sin(a))
        d.line([p0, p1], fill=c, width=max(1, int(round(w))))
        rr = w * 0.85
        d.ellipse([p1[0] - rr, p1[1] - rr, p1[0] + rr, p1[1] + rr], fill=c)
    rc = r * 0.12
    d.ellipse([cx - rc, cy - rc, cx + rc, cy + rc], fill=c)


def confete(d, rnd, x0, y0, x1, y1, n, s=S, tam=(3.0, 6.5)):
    """Confete em retângulos girados, bolinhas e estrelinhas (em 1x; multiplica por s)."""
    for _ in range(n):
        x, y = rnd.uniform(x0, x1) * s, rnd.uniform(y0, y1) * s
        cor = rgb(rnd.choice(CONFETE), rnd.randint(170, 240))
        tipo = rnd.random()
        t = rnd.uniform(*tam) * s
        if tipo < 0.55:
            a = rnd.uniform(0, math.pi)
            hw, hh = t * 0.5, t * 0.22
            ca, sa = math.cos(a), math.sin(a)
            pts = [(x + px * ca - py * sa, y + px * sa + py * ca)
                   for px, py in ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh))]
            d.polygon(pts, fill=cor)
        elif tipo < 0.85:
            r = t * 0.26
            d.ellipse([x - r, y - r, x + r, y + r], fill=cor)
        else:
            estrela4(d, x, y, t * 0.55, cor)


# ---------------------------------------------------------------- emoji
_EMOJI_FONT = None
_EMOJI_CACHE = {}


def emoji_base(ch):
    global _EMOJI_FONT
    if _EMOJI_FONT is None:
        _EMOJI_FONT = ImageFont.truetype(F_EMOJI, 109)
    ch = ch.replace("️", "")
    if ch not in _EMOJI_CACHE:
        im = Image.new("RGBA", (180, 180), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((90, 90), ch, font=_EMOJI_FONT, embedded_color=True, anchor="mm")
        bb = im.getbbox()
        if bb is None:
            raise SystemExit(f"emoji sem glifo: {ch!r}")
        _EMOJI_CACHE[ch] = im.crop(bb)
    return _EMOJI_CACHE[ch]


def emoji(ch, tam):
    """Renderiza um emoji Noto (109 px) e redimensiona para caber em tam x tam."""
    im = emoji_base(ch)
    k = tam / max(im.size)
    return im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)


def recolorir(im, cor):
    """Recolore mantendo luz e sombra (camiseta lisa, meia branca)."""
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


def com_pontinhos(im, cor, fcx, fcy, frx, fry, n, fr, seed):
    """Pontinhos (lentilha, uva-passa) num elipse relativo ao tamanho do emoji."""
    out = im.copy()
    d = ImageDraw.Draw(out)
    rnd = random.Random(seed)
    w, h = out.size
    alfa = np.array(out.split()[3])
    r = fr * w
    base, luz = rgb(cor), mix(cor, "#FFFFFF", 0.45)
    feitos = 0
    tent = 0
    while feitos < n and tent < 2000:
        tent += 1
        a, rr = rnd.uniform(0, 2 * math.pi), math.sqrt(rnd.random())
        x = (fcx + frx * rr * math.cos(a)) * w
        y = (fcy + fry * rr * math.sin(a)) * h
        if not (0 <= int(x) < w and 0 <= int(y) < h) or alfa[int(y), int(x)] < 250:
            continue
        rx, ry = r * rnd.uniform(0.9, 1.15), r * rnd.uniform(0.65, 0.85)
        d.ellipse([x - rx, y - ry, x + rx, y + ry], fill=base)
        d.ellipse([x - rx * 0.45, y - ry * 0.65, x + rx * 0.05, y - ry * 0.1], fill=luz)
        feitos += 1
    return out


# ---------------------------------------------------------------- desenhos próprios
def uvas(tam, folha=True):
    """Cacho de uva (desenho próprio). tam = altura aproximada do cacho em px."""
    g = tam / 9.4                      # raio de cada uva
    ww, hh = int(g * 9.2), int(g * 10.2)
    lay = Image.new("RGBA", (ww, hh), (0, 0, 0, 0))
    cx, topo = ww * 0.47, g * 2.5
    # cabinho e gavinha
    d = ImageDraw.Draw(lay)
    lw = max(2, int(g * 0.42))
    d.line([(cx + g * 0.1, topo + g * 0.2), (cx + g * 0.35, topo - g * 1.25), (cx + g * 0.9, topo - g * 2.05)],
           fill=rgb("#6B3F1D"), width=lw, joint="curve")
    d.arc([cx - g * 1.9, topo - g * 2.3, cx - g * 0.2, topo - g * 0.7], 200, 20, fill=rgb("#6B3F1D"),
          width=max(1, int(g * 0.22)))
    if folha:
        fl = Image.new("RGBA", (int(g * 4.2), int(g * 3.0)), (0, 0, 0, 0))
        fd = ImageDraw.Draw(fl)
        fw, fh = fl.size
        fd.ellipse([0, fh * 0.12, fw * 0.98, fh * 0.92], fill=rgb("#3FAE4E"))
        fd.ellipse([fw * 0.05, fh * 0.12, fw * 0.95, fh * 0.6], fill=rgb("#5CC963"))
        fd.line([(fw * 0.06, fh * 0.55), (fw * 0.92, fh * 0.48)], fill=rgb("#2C7E39"), width=max(1, int(g * 0.2)))
        fl = fl.rotate(28, resample=Image.BICUBIC, expand=True)
        lay.alpha_composite(fl, (int(cx + g * 0.3), int(topo - g * 2.55)))
    linhas = [(0.0, (-1.7, 0, 1.7)), (1.45, (-2.55, -0.85, 0.85, 2.55)), (2.9, (-1.7, 0, 1.7)),
              (4.35, (-0.85, 0.85)), (5.8, (0,))]
    for yy, xs in linhas:
        for xx in xs:
            gx, gy = cx + xx * g, topo + yy * g + g * 0.9
            uva = Image.new("RGBA", (int(g * 2.4) + 2, int(g * 2.4) + 2), (0, 0, 0, 0))
            ud = ImageDraw.Draw(uva)
            c = uva.width / 2
            ud.ellipse([c - g * 1.08, c - g * 1.08, c + g * 1.08, c + g * 1.08], fill=rgb("#2B0C52"))
            gr = radial(uva.width, uva.height, c - g * 0.35, c - g * 0.4, g * 1.45,
                        [(0, "#C58BFF"), (0.45, "#8A45E6"), (1, "#4A1898")])
            mm = Image.new("L", uva.size, 0)
            ImageDraw.Draw(mm).ellipse([c - g * 0.95, c - g * 0.95, c + g * 0.95, c + g * 0.95], fill=255)
            uva.alpha_composite(com_mascara(gr, mm))
            ud = ImageDraw.Draw(uva)
            ud.ellipse([c - g * 0.62, c - g * 0.66, c - g * 0.12, c - g * 0.26], fill=(255, 255, 255, 190))
            lay.alpha_composite(uva, (int(gx - c), int(gy - c)))
    return lay.crop(lay.getbbox())


def roma(tam):
    """Romã (não existe emoji): fruta vermelho-escura, coroinha e um corte com sementes."""
    t = int(tam)
    lay = Image.new("RGBA", (t, t), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    cx, cy, r = t * 0.5, t * 0.57, t * 0.39
    # coroinha
    coroa = [(cx - t * 0.13, cy - r * 0.86), (cx - t * 0.16, cy - r - t * 0.17), (cx - t * 0.06, cy - r - t * 0.07),
             (cx, cy - r - t * 0.19), (cx + t * 0.06, cy - r - t * 0.07), (cx + t * 0.16, cy - r - t * 0.17),
             (cx + t * 0.13, cy - r * 0.86)]
    d.polygon(coroa, fill=rgb("#8E1430"))
    # fruta
    fr = radial(t, t, cx - r * 0.35, cy - r * 0.4, r * 1.55, [(0, "#FF5A73"), (0.45, "#D11A44"), (1, "#6E0A24")])
    m = Image.new("L", (t, t), 0)
    ImageDraw.Draw(m).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    lay.alpha_composite(com_mascara(fr, m))
    d = ImageDraw.Draw(lay)
    # corte com sementes (embaixo, à direita)
    ex, ey, erx, ery = cx + r * 0.22, cy + r * 0.22, r * 0.55, r * 0.45
    d.ellipse([ex - erx, ey - ery, ex + erx, ey + ery], fill=rgb("#FFE3C4"))
    rnd = random.Random(9)
    for i in range(13):
        a, rr = rnd.uniform(0, 2 * math.pi), math.sqrt(rnd.random()) * 0.78
        sx, sy = ex + erx * rr * math.cos(a), ey + ery * rr * math.sin(a)
        sr = r * 0.12
        d.ellipse([sx - sr, sy - sr * 0.85, sx + sr, sy + sr * 0.85], fill=rgb("#C3123D"))
        d.ellipse([sx - sr * 0.5, sy - sr * 0.55, sx - sr * 0.05, sy - sr * 0.1], fill=(255, 220, 230, 230))
    # brilho
    d.ellipse([cx - r * 0.62, cy - r * 0.7, cx - r * 0.25, cy - r * 0.38], fill=(255, 255, 255, 140))
    return lay.crop(lay.getbbox())


def moeda(tam):
    """Moeda dourada genérica, sem valor: só uma estrela no meio."""
    t = int(tam)
    lay = Image.new("RGBA", (t, t), (0, 0, 0, 0))
    c, r = t / 2, t * 0.48
    d = ImageDraw.Draw(lay)
    d.ellipse([c - r, c - r, c + r, c + r], fill=rgb("#B07205"))
    fr = radial(t, t, c - r * 0.3, c - r * 0.35, r * 1.5, [(0, "#FFF4B5"), (0.45, "#FFCF3F"), (1, "#D48A08")])
    m = Image.new("L", (t, t), 0)
    ImageDraw.Draw(m).ellipse([c - r * 0.9, c - r * 0.9, c + r * 0.9, c + r * 0.9], fill=255)
    lay.alpha_composite(com_mascara(fr, m))
    d = ImageDraw.Draw(lay)
    d.ellipse([c - r * 0.68, c - r * 0.68, c + r * 0.68, c + r * 0.68], outline=rgb("#C58A0C"),
              width=max(1, int(r * 0.07)))
    d.polygon(estrela5(c, c + r * 0.03, r * 0.42, r * 0.18), fill=rgb("#D99410"))
    d.ellipse([c - r * 0.62, c - r * 0.66, c - r * 0.22, c - r * 0.36], fill=(255, 255, 255, 150))
    return lay


def seta(tam):
    """Seta grossa para a direita (verde), com contorno escuro."""
    t = int(tam)
    lay = Image.new("RGBA", (t, t), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    y = t / 2
    pts = [(t * 0.10, y - t * 0.13), (t * 0.52, y - t * 0.13), (t * 0.52, y - t * 0.32), (t * 0.92, y),
           (t * 0.52, y + t * 0.32), (t * 0.52, y + t * 0.13), (t * 0.10, y + t * 0.13)]
    d.polygon(pts, fill=rgb("#2FBF71"))
    d.polygon([(t * 0.10, y - t * 0.13), (t * 0.52, y - t * 0.13), (t * 0.52, y - t * 0.32), (t * 0.92, y),
               (t * 0.52, y)], fill=rgb("#55D98E"))
    lay = com_contorno(lay.crop(lay.getbbox()), max(2, int(t * 0.05)), "#126B3C")
    return lay


def estrela_cadente(tam):
    """Estrela dourada com rastro colorido (no lugar do emoji, que vem num quadrado escuro)."""
    t = int(tam)
    lay = Image.new("RGBA", (t, t), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    sx, sy = t * 0.68, t * 0.34
    for i, cor in enumerate(("#FF6FB5", "#FFD24A", "#3FE0D0")):
        off = (i - 1) * t * 0.085
        x0, y0 = t * 0.06 + off * 0.6, t * 0.80 + off
        x1, y1 = sx - t * 0.05 + off * 0.3, sy + t * 0.08 + off * 0.6
        w = int(t * 0.075)
        d.line([(x0, y0), (x1, y1)], fill=rgb(cor, 235), width=w)
        for (px, py) in ((x0, y0), (x1, y1)):
            d.ellipse([px - w / 2, py - w / 2, px + w / 2, py + w / 2], fill=rgb(cor, 235))
    est = Image.new("RGBA", (t, t), (0, 0, 0, 0))
    ImageDraw.Draw(est).polygon(estrela5(sx, sy, t * 0.30, t * 0.13, -90 + 12), fill=rgb("#FFCF3F"))
    est = com_contorno(est, max(2, int(t * 0.035)), "#C27A00")
    lay.alpha_composite(est, (-(est.width - t) // 2, -(est.height - t) // 2))
    d = ImageDraw.Draw(lay)
    d.ellipse([sx - t * 0.10, sy - t * 0.12, sx - t * 0.02, sy - t * 0.05], fill=(255, 255, 255, 200))
    return lay.crop(lay.getbbox())


def relogio(tam):
    """Relógio de parede marcando meia-noite (ícone alternativo)."""
    t = int(tam)
    lay = Image.new("RGBA", (t, t), (0, 0, 0, 0))
    c, r = t / 2, t * 0.48
    aro = radial(t, t, c - r * 0.4, c - r * 0.5, r * 1.8, [(0, OURO_CLARO), (0.4, OURO), (1, "#B57405")])
    m = Image.new("L", (t, t), 0)
    ImageDraw.Draw(m).ellipse([c - r, c - r, c + r, c + r], fill=255)
    lay.alpha_composite(com_mascara(aro, m))
    d = ImageDraw.Draw(lay)
    rf = r * 0.82
    d.ellipse([c - rf, c - rf, c + rf, c + rf], fill=rgb("#FFF8E8"))
    d.ellipse([c - rf, c - rf, c + rf, c + rf], outline=rgb("#E7B54A"), width=max(1, int(r * 0.03)))
    for k in range(12):
        a = math.radians(-90 + 30 * k)
        grande = k % 3 == 0
        r1, r2 = rf * (0.74 if grande else 0.80), rf * 0.92
        d.line([(c + r1 * math.cos(a), c + r1 * math.sin(a)), (c + r2 * math.cos(a), c + r2 * math.sin(a))],
               fill=rgb("#3A1C6E"), width=max(1, int(r * (0.075 if grande else 0.04))))
    # ponteiros juntos no 12 (meia-noite): hora grossa e curta, minuto fino e longo
    wh, wm = r * 0.13, r * 0.075
    d.rounded_rectangle([c - wh / 2, c - rf * 0.50, c + wh / 2, c + wh * 0.4], radius=int(wh / 2), fill=rgb("#2A0D55"))
    d.rounded_rectangle([c - wm / 2, c - rf * 0.70, c + wm / 2, c + wm], radius=int(wm / 2), fill=rgb("#2A0D55"))
    d.ellipse([c - r * 0.10, c - r * 0.10, c + r * 0.10, c + r * 0.10], fill=rgb("#FF4FA3"))
    # brilho no vidro
    br = Image.new("L", (t, t), 0)
    ImageDraw.Draw(br).pieslice([c - rf * 0.9, c - rf * 0.9, c + rf * 0.9, c + rf * 0.9], 190, 260, fill=60)
    lay.alpha_composite(camada_cor((t, t), "#FFFFFF", br.filter(ImageFilter.GaussianBlur(t * 0.01))))
    return lay


DESENHOS = {"roma": roma, "moeda": moeda, "seta": seta, "estrela_cadente": estrela_cadente}


def figura(nome, tam):
    """Emoji Noto ou desenho próprio ('@nome'), cabendo em tam x tam."""
    if nome.startswith("@"):
        im = DESENHOS[nome[1:]](tam * 2)
        k = tam / max(im.size)
        return im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
    return emoji(nome, tam)


# ---------------------------------------------------------------- texto
def medir_fonte(linhas, largura, tam_max, tam_min, arquivo=F_BLACK):
    d = ImageDraw.Draw(Image.new("L", (10, 10)))
    for tam in range(tam_max, tam_min - 1, -1):
        f = ImageFont.truetype(arquivo, tam * S)
        sw = max(3, round(tam * 0.085)) * S
        if max(d.textlength(l, font=f) for l in linhas) + 2 * sw <= largura * S:
            return tam, f, sw
    raise SystemExit(f"texto não coube nem com {tam_min}px: {linhas}")


def segmentos(linha, cor, destaque):
    """Separa a parte entre parênteses (a piada) para pintar de dourado."""
    if destaque and "(" in linha:
        i = linha.index("(")
        return [(p, c) for p, c in ((linha[:i], cor), (linha[i:], OURO_TXT)) if p]
    return [(linha, cor)]


def desenhar_texto(img, linhas, area, cor_contorno, cores_linha=("#FFFFFF", "#FFFFFF"),
                   tam_max=TAM_MAX, tam_min=TAM_MIN, tamanhos=None, arquivo=F_BLACK, destaque=True):
    """1 ou 2 linhas centralizadas, com contorno e sombra dura. Reduz a fonte se precisar.
    O trecho entre parênteses sai em dourado (destaque=True)."""
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
    tem_acento_1 = any(ch in linhas[0] for ch in "ÁÃÉÊÍÓÔÕÚÇÀ")
    if tem_acento_1 and topo - (acento[0] - caps[0]) < y0 * S:
        topo = y0 * S + (acento[0] - caps[0])
    cx = (x0 + x1) / 2 * S
    sombra = max(3, round(fontes[0][0] * 0.07)) * S
    contorno = rgb(cor_contorno)
    # 1) sombra dura  2) contorno  3) miolo colorido por trecho
    for i, l in enumerate(linhas):
        tam, f, sw = fontes[i]
        xs = cx - d.textlength(l, font=f) / 2
        yb = topo + bases[i]
        d.text((xs, yb + sombra), l, font=f, anchor="ls", fill=contorno, stroke_width=sw, stroke_fill=contorno)
    for i, l in enumerate(linhas):
        tam, f, sw = fontes[i]
        xs = cx - d.textlength(l, font=f) / 2
        yb = topo + bases[i]
        d.text((xs, yb), l, font=f, anchor="ls", fill=contorno, stroke_width=sw, stroke_fill=contorno)
    for i, l in enumerate(linhas):
        tam, f, sw = fontes[i]
        x = cx - d.textlength(l, font=f) / 2
        yb = topo + bases[i]
        for trecho, cor in segmentos(l, cores_linha[i], destaque):
            d.text((x, yb), trecho, font=f, anchor="ls", fill=rgb(cor))
            x += d.textlength(trecho, font=f)
    return [fo[0] for fo in fontes]


def checar_glifos(texto, arquivo=F_BLACK):
    """Falha se algum caractere cair no 'quadradinho' (glifo que a fonte não tem)."""
    f = ImageFont.truetype(arquivo, 60)

    def desenho(ch):
        im = Image.new("L", (120, 120), 0)
        ImageDraw.Draw(im).text((10, 10), ch, font=f, fill=255)
        return np.array(im)

    vazio = desenho("")
    faltando = [ch for ch in sorted(set(texto)) if ch.strip() and np.array_equal(desenho(ch), vazio)]
    if faltando:
        raise SystemExit(f"a fonte não tem: {faltando}")


# ---------------------------------------------------------------- o "bilhete" (moldura própria)
def linha_pontilhada(img, inset, passo, raio, cor, alpha):
    """Pontinhos dourados acompanhando a borda por dentro (acabamento de bilhete)."""
    x0, y0, x1, y1 = BODY
    a0, b0, a1, b1 = x0 + inset, y0 + inset, x1 - inset, y1 - inset
    r2 = math.sqrt(2)
    k_tl = x0 + y0 + DOBRA + inset * r2
    k_br = x1 + y1 - DOBRA - inset * r2
    rc = max(1.0, R_BODY - inset)
    caminho = [(k_tl - b0, b0)]
    for k in range(9):  # canto sup. direito (arco)
        a = math.radians(-90 + 90 * k / 8)
        caminho.append((a1 - rc + rc * math.cos(a), b0 + rc + rc * math.sin(a)))
    caminho += [(a1, k_br - a1), (k_br - b1, b1)]
    for k in range(9):  # canto inf. esquerdo (arco)
        a = math.radians(90 + 90 * k / 8)
        caminho.append((a0 + rc + rc * math.cos(a), b1 - rc + rc * math.sin(a)))
    caminho += [(a0, k_tl - a0), (k_tl - b0, b0)]
    camada = Image.new("L", img.size, 0)
    d = ImageDraw.Draw(camada)
    sobra = 0.0
    for (p, q) in zip(caminho, caminho[1:]):
        seg = math.hypot(q[0] - p[0], q[1] - p[1])
        t = sobra
        while t <= seg:
            x, y = p[0] + (q[0] - p[0]) * t / seg, p[1] + (q[1] - p[1]) * t / seg
            d.ellipse([(x - raio) * S, (y - raio) * S, (x + raio) * S, (y + raio) * S], fill=255)
            t += passo
        sobra = t - seg
    img.alpha_composite(camada_cor(img.size, cor, camada, alpha))


def ponta_dobrada(img, canto, m_corpo):
    """Desenha a ponta dobrada (verso do papel em dourado claro) com sombrinha."""
    x0, y0, x1, y1 = BODY
    f = DOBRA
    if canto == "tl":
        tri = [(x0 + f, y0), (x0, y0 + f), (x0 + f, y0 + f)]
        sdx, sdy = 2, 3
    else:
        tri = [(x1 - f, y1), (x1, y1 - f), (x1 - f, y1 - f)]
        sdx, sdy = -2, -3
    size = img.size
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).polygon([(x * S, y * S) for x, y in tri], fill=255)
    sombra = deslocar(m, sdx * S, sdy * S).filter(ImageFilter.GaussianBlur(2.5 * S))
    img.alpha_composite(camada_cor(size, "#070113", intersecao(sombra, m_corpo), 0.65))
    xs = [p[0] for p in tri]
    ys = [p[1] for p in tri]
    bx0, by0, bx1, by1 = int(min(xs) * S), int(min(ys) * S), int(max(xs) * S) + 1, int(max(ys) * S) + 1
    gr = gradiente(bx1 - bx0, by1 - by0, [(0, "#FFF6CF"), (1, "#F0B93A")],
                   (0.5, 0.5) if canto == "tl" else (-0.5, -0.5))
    lay = Image.new("RGBA", size, (0, 0, 0, 0))
    lay.paste(gr, (bx0, by0))
    img.alpha_composite(com_mascara(lay, m))
    d = ImageDraw.Draw(img)
    d.line([(x * S, y * S) for x, y in tri + [tri[0]]], fill=rgb("#B97A0A"), width=int(1.2 * S), joint="curve")


def bilhete(corpo_rgba, shade, desenhar_selo, seed=0):
    """Monta a moldura: sombras, borda dourada, corpo de céu noturno, confete, fogos, pontas, selo."""
    size = (W * S, H * S)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    rnd = random.Random(1000 + seed)
    m_borda = uniao(mascara_bilhete(BORDA), mascara_selo(0))
    # sombra suave (para ler em qualquer fundo) e espessura de adesivo
    sombra = deslocar(m_borda, 0, 5 * S).filter(ImageFilter.GaussianBlur(5 * S))
    img.alpha_composite(camada_cor(size, "#0A0418", sombra, 0.55))
    img.alpha_composite(camada_cor(size, OURO_SOMBRA, deslocar(m_borda, 0, 5 * S)))
    # borda dourada (gradiente de cima para baixo, com reflexo diagonal)
    ouro = gradiente(W * S, H * S, [(0, OURO_CLARO), (0.35, OURO), (0.75, "#F2B12A"), (1, OURO_ESCURO)], (0.25, 0.75))
    img.alpha_composite(com_mascara(ouro, m_borda))
    # corpo
    m_corpo = mascara_bilhete(0)
    img.alpha_composite(com_mascara(corpo_rgba, m_corpo))
    # brilho de luz no alto (como se os fogos iluminassem)
    gl = Image.new("L", size, 0)
    ImageDraw.Draw(gl).ellipse([150 * S, -40 * S, 362 * S, 150 * S], fill=120)
    gl = gl.filter(ImageFilter.GaussianBlur(28 * S))
    img.alpha_composite(camada_cor(size, "#FF9AD5", intersecao(gl, m_corpo), 0.35))
    gl2 = Image.new("L", size, 0)
    gd = ImageDraw.Draw(gl2)
    for i in range(60):
        yy = BODY[1] + i * (BODY[3] - BODY[1]) * 0.5 / 60
        gd.line([(0, yy * S), (W * S, yy * S)], fill=int(48 * (1 - i / 60)), width=S * 2)
    img.alpha_composite(camada_cor(size, "#FFFFFF", intersecao(gl2, m_corpo)))
    # estrelinhas do céu (bem fracas)
    st = Image.new("RGBA", size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(st)
    for _ in range(46):
        x, y = rnd.uniform(BODY[0] + 6, BODY[2] - 6) * S, rnd.uniform(BODY[1] + 6, BODY[3] - 6) * S
        r = rnd.uniform(0.5, 1.3) * S
        sd.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, rnd.randint(50, 120)))
    img.alpha_composite(com_mascara(st, m_corpo))
    # fogos pequenos no céu (cantos de cima) + confete
    fx = Image.new("RGBA", size, (0, 0, 0, 0))
    fd = ImageDraw.Draw(fx)
    explosao(fd, 72 * S, 84 * S, 19 * S, rgb(OURO, 235), n=12, giro=rnd.uniform(0, 30))
    explosao(fd, 124 * S, 66 * S, 9 * S, rgb("#3FE0D0", 220), n=10, giro=rnd.uniform(0, 30))
    explosao(fd, 442 * S, 82 * S, 18 * S, rgb("#FF6FB5", 235), n=12, giro=rnd.uniform(0, 30))
    explosao(fd, 390 * S, 66 * S, 9 * S, rgb(OURO, 220), n=10, giro=rnd.uniform(0, 30))
    confete(fd, rnd, 42, 60, 196, 100, 9)
    confete(fd, rnd, 318, 60, 476, 100, 9)
    for (x, y, r, a) in ((186, 80, 7.5, 235), (170, 66, 4, 200), (326, 80, 7.5, 235), (342, 66, 4, 200)):
        estrela4(fd, x * S, y * S, r * S, (255, 255, 255, a))
    img.alpha_composite(com_mascara(fx, m_corpo))
    # pontilhado dourado por dentro da borda
    linha_pontilhada(img, 8.5, 8.0, 1.25, OURO, 0.75)
    # pontas dobradas
    ponta_dobrada(img, "tl", m_corpo)
    ponta_dobrada(img, "br", m_corpo)
    # selo: sombra no corpo, aro dourado ondulado, miolo
    ms = deslocar(mascara_selo(0), 0, 4 * S).filter(ImageFilter.GaussianBlur(2 * S))
    img.alpha_composite(camada_cor(size, "#070113", intersecao(ms, m_corpo), 0.7))
    cx, cy = SELO_C
    aro = radial(W * S, H * S, (cx - 18) * S, (cy - 22) * S, 70 * S,
                 [(0, OURO_CLARO), (0.45, OURO), (0.8, "#F0AE22"), (1, OURO_ESCURO)])
    img.alpha_composite(com_mascara(aro, mascara_selo(0)))
    d = ImageDraw.Draw(img)
    d.line(pontos_selo(cx, cy, SELO_R + SELO_ARO - 0.6, SELO_AMP, SELO_ONDAS) +
           pontos_selo(cx, cy, SELO_R + SELO_ARO - 0.6, SELO_AMP, SELO_ONDAS)[:1],
           fill=rgb("#C98608", 160), width=int(0.9 * S))
    rr = SELO_R + 1.3
    d.ellipse([(cx - rr) * S, (cy - rr) * S, (cx + rr) * S, (cy + rr) * S], fill=rgb("#B97A0A"))
    desenhar_selo(img)
    return img


def miolo(img, c1, c2):
    """Miolo do selo: gradiente radial (c1 no centro-alto, c2 na borda)."""
    cx, cy = SELO_C[0] * S, SELO_C[1] * S
    r = SELO_R * S
    mi = radial(2 * r, 2 * r, r * 0.8, r * 0.7, r * 1.4, [(0, c1), (1, c2)])
    mm = Image.new("L", (2 * r, 2 * r), 0)
    ImageDraw.Draw(mm).ellipse([0, 0, 2 * r - 1, 2 * r - 1], fill=255)
    img.alpha_composite(com_mascara(mi, mm), (cx - r, cy - r))
    return mm


def selo_ilustracao(principal, secundario, tint, extras, seed):
    def f(img):
        cx, cy = SELO_C[0] * S, SELO_C[1] * S
        r = SELO_R * S
        c1, c2 = extras.get("interior", ("#FFFFFF", tint))
        mm = miolo(img, c1, c2)
        if extras.get("interior_emoji"):
            ce = emoji_base(extras["interior_emoji"])
            ce = ce.resize((2 * r + 2, 2 * r + 2), Image.LANCZOS).crop((1, 1, 2 * r + 1, 2 * r + 1))
            img.alpha_composite(com_mascara(ce, mm), (cx - r, cy - r))
        tem_lado = bool(secundario)
        if principal:
            e1 = figura(principal, int(r * 1.36))
            if extras.get("tint_main"):
                e1 = recolorir(e1, extras["tint_main"])
            if extras.get("pontos"):
                cor, fcx, fcy, frx, fry, n, fr = extras["pontos"]
                e1 = com_pontinhos(e1, cor, fcx, fcy, frx, fry, n, fr, seed)
            e1s, _ = com_sombra(e1, 0, int(1.5 * S), 2 * S, 0.25)
            dx = -0.10 * r if tem_lado else 0
            colar_centro(img, e1s, cx + dx, cy - 0.02 * r)
        if extras.get("terceiro"):
            ch, fx, fy, esc, giro = extras["terceiro"]
            e3 = com_contorno(figura(ch, int(r * esc)), int(2.2 * S))
            if giro:
                e3 = e3.rotate(giro, resample=Image.BICUBIC, expand=True)
            e3s, _ = com_sombra(e3, 0, int(1.2 * S), 2 * S, 0.25)
            colar_centro(img, e3s, cx + fx * r, cy + fy * r)
        if secundario:
            grande = principal is None
            e2 = figura(secundario, int(r * (1.25 if grande else 0.88)))
            if extras.get("tint_secundario"):
                e2 = recolorir(e2, extras["tint_secundario"])
            e2 = com_contorno(e2, int(2.6 * S))
            if not grande:
                e2 = e2.rotate(-12, resample=Image.BICUBIC, expand=True)
            e2s, _ = com_sombra(e2, 0, int(1.5 * S), 2 * S, 0.30)
            if grande:
                colar_centro(img, e2s, cx + 0.05 * r, cy + 0.02 * r)
            else:
                colar_centro(img, e2s, cx + 0.62 * r, cy + 0.50 * r)
    return f


def selo_titulo(img):
    """Selo do título: miolo de céu noturno com fogos e o cacho de uva (motivo do ícone)."""
    cx, cy = SELO_C[0] * S, SELO_C[1] * S
    r = SELO_R * S
    mm = miolo(img, "#5A2AB0", "#1B0745")
    fx = Image.new("RGBA", (2 * r, 2 * r), (0, 0, 0, 0))
    fd = ImageDraw.Draw(fx)
    explosao(fd, r * 0.55, r * 0.55, r * 0.5, rgb(OURO, 240), n=14)
    explosao(fd, r * 1.5, r * 0.62, r * 0.38, rgb("#FF6FB5", 235), n=12, giro=8)
    explosao(fd, r * 1.55, r * 1.45, r * 0.26, rgb("#3FE0D0", 220), n=10)
    img.alpha_composite(com_mascara(fx, mm), (cx - r, cy - r))
    u = uvas(int(r * 1.32))
    u = com_contorno(u, int(2.4 * S))
    us, _ = com_sombra(u, 0, int(1.5 * S), 2 * S, 0.35)
    colar_centro(img, us, cx - 0.04 * r, cy + 0.04 * r)


def reduzir(img):
    return img.resize((img.width // S, img.height // S), Image.LANCZOS)


# ---------------------------------------------------------------- peças
def ilustracao_de(item, chave):
    principal, secundario, extras = ILUSTRA[chave]
    extras = dict(extras)
    extras.update(item.get("extras_desenho", {}) or {})   # tint_main / tint_secundario do JSON
    return principal, secundario, extras


def carta(item, paleta_nome, chave):
    p = PALETAS[paleta_nome]
    corpo = gradiente(W * S, H * S, [(0, p["top"]), (1, p["bot"])], (0.18, 0.82))
    principal, secundario, extras = ilustracao_de(item, chave)
    img = bilhete(corpo, p["shade"], selo_ilustracao(principal, secundario, p["tint"], extras, chave), seed=chave)
    tam = desenhar_texto(img, [item["linha1"], item["linha2"]], TEXT_AREA, p["shade"])
    return reduzir(img), tam[0]


TITULO_GRAD = [(0, "#2C0D72"), (0.5, "#6A1C8E"), (1, "#A3236E")]


def titulo(l1, l2, com_toque=False):
    corpo = gradiente(W * S, H * S, TITULO_GRAD, (0.85, 0.15))
    img = bilhete(corpo, NOITE, selo_titulo, seed=7)
    if com_toque:
        tams = desenhar_texto(img, [l1, l2], (44, 100, 468, 194), NOITE, ("#FFFFFF", OURO_TXT),
                              tamanhos=(46, 50), tam_min=28, destaque=False)
        pilula_toque(img)
    else:
        tams = desenhar_texto(img, [l1, l2], (44, 104, 468, 226), NOITE, ("#FFFFFF", OURO_TXT),
                              tamanhos=(50, 56), tam_min=30, destaque=False)
    return reduzir(img), tams


def pilula_toque(img):
    """Pílula dourada 'TOQUE NA TELA' com mãozinha, presa na borda de baixo."""
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
                        fill=rgb(NOITE))
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle(box, radius=17 * S, fill=255)
    gp = gradiente(int(w) + 2, int(h) + 2, [(0, "#FFF3B0"), (0.55, OURO), (1, "#F2A81E")], (0, 1))
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    lay.paste(gp, (int(box[0]), int(box[1])))
    img.alpha_composite(com_mascara(lay, m))
    x = box[0] + 12 * S
    img.alpha_composite(mao, (int(x), int(cy - mao.height / 2)))
    d = ImageDraw.Draw(img)
    d.text((x + mao.width + 7 * S, cy + 1 * S), txt, font=f, anchor="lm", fill=rgb(NOITE))


def icone(tam_final=162, estilo="principal"):
    t = 648 if tam_final <= 162 else tam_final * 2   # desenha grande e reduz
    rnd = random.Random(estilo)
    if estilo == "principal":
        img = gradiente(t, t, [(0, "#3B137E"), (0.55, "#220A52"), (1, "#11052B")], (0.3, 0.7))
        glow = Image.new("L", (t, t), 0)
        ImageDraw.Draw(glow).ellipse([t * 0.2, t * 0.22, t * 0.8, t * 0.9], fill=170)
        img.alpha_composite(camada_cor((t, t), "#8B3DFF", glow.filter(ImageFilter.GaussianBlur(t * 0.09)), 0.55))
    else:
        img = gradiente(t, t, [(0, "#8A1F6C"), (0.6, "#4A0D45"), (1, "#24062A")], (0.3, 0.7))
        glow = Image.new("L", (t, t), 0)
        ImageDraw.Draw(glow).ellipse([t * 0.3, t * 0.1, t * 0.9, t * 0.7], fill=160)
        img.alpha_composite(camada_cor((t, t), "#FF5FB0", glow.filter(ImageFilter.GaussianBlur(t * 0.1)), 0.45))
    d = ImageDraw.Draw(img)
    for _ in range(60):  # estrelinhas
        x, y, r = rnd.uniform(0, t), rnd.uniform(0, t), rnd.uniform(0.6, 2.0) * t / 648
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, rnd.randint(70, 170)))
    fx = Image.new("RGBA", (t, t), (0, 0, 0, 0))
    fd = ImageDraw.Draw(fx)
    if estilo == "principal":
        explosao(fd, t * 0.30, t * 0.30, t * 0.25, rgb(OURO), n=16, larg=t * 0.016)
        explosao(fd, t * 0.74, t * 0.25, t * 0.19, rgb("#FF6FB5"), n=14, giro=6, larg=t * 0.014)
        explosao(fd, t * 0.83, t * 0.66, t * 0.11, rgb("#3FE0D0"), n=12, larg=t * 0.011)
        explosao(fd, t * 0.15, t * 0.70, t * 0.08, rgb("#FFB23F"), n=10, larg=t * 0.009)
    else:
        explosao(fd, t * 0.22, t * 0.22, t * 0.16, rgb(OURO), n=14, larg=t * 0.013)
        explosao(fd, t * 0.84, t * 0.84, t * 0.10, rgb("#3FE0D0"), n=12, larg=t * 0.010)
    glow_f = fx.filter(ImageFilter.GaussianBlur(t * 0.012))
    img.alpha_composite(glow_f)
    img.alpha_composite(fx)
    d = ImageDraw.Draw(img)
    for (x, y, r) in ((0.12, 0.13, 0.035), (0.90, 0.48, 0.028), (0.10, 0.88, 0.03)):
        estrela4(d, x * t, y * t, r * t, (255, 255, 255, 230))
    if estilo == "principal":
        u = uvas(int(t * 0.60))
        u = com_contorno(u, int(t * 0.022))
        us, _ = com_sombra(u, 0, int(t * 0.018), int(t * 0.022), 0.45, "#0B0320")
        colar_centro(img, us, t * 0.49, t * 0.53)
    else:
        rl = relogio(int(t * 0.58))
        rl = com_contorno(rl, int(t * 0.018))
        rs, _ = com_sombra(rl, 0, int(t * 0.016), int(t * 0.02), 0.45, "#12020F")
        colar_centro(img, rs, t * 0.585, t * 0.43)
        u = uvas(int(t * 0.44))
        u = com_contorno(u, int(t * 0.02))
        us, _ = com_sombra(u, 0, int(t * 0.016), int(t * 0.02), 0.45, "#12020F")
        colar_centro(img, us, t * 0.33, t * 0.63)
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
    """Fundos falsos para testar a leitura (sala clara, noite com fogos, praia de dia, confete)."""
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
        for _ in range(22):
            x, y, r = rnd.uniform(0, w), rnd.uniform(0, h * 0.7), rnd.uniform(10, 36)
            c = rnd.choice(["#FFB347", "#FFE08A", "#FF7A59", "#C9A0FF"])
            d.ellipse([x - r, y - r, x + r, y + r], fill=rgb(c, rnd.randint(40, 110)))
        im = im.filter(ImageFilter.GaussianBlur(6))
        d = ImageDraw.Draw(im)
        for (x, y, r, c) in ((0.2, 0.12, 60, "#FFD24A"), (0.8, 0.2, 70, "#FF6FB5"), (0.55, 0.06, 40, "#3FE0D0")):
            explosao(d, x * w, y * h, r, rgb(c, 200), n=18, larg=2.5)
    elif tipo == "praia":
        im = gradiente(w, h, [(0, "#8FD3FF"), (0.5, "#DDF3FF"), (1, "#DDF3FF")], (0, 1))
        d = ImageDraw.Draw(im)
        d.ellipse([w * 0.70, h * 0.06, w * 0.92, h * 0.18], fill=rgb("#FFF1A6"))
        d.rectangle([0, h * 0.50, w, h * 0.66], fill=rgb("#2E9BD6"))
        for i in range(6):
            yy = h * (0.52 + i * 0.024)
            d.line([(0, yy), (w, yy + 4)], fill=rgb("#FFFFFF", 120), width=3)
        d.rectangle([0, h * 0.66, w, h], fill=rgb("#F1D9A8"))
    else:  # confete: fundo bem poluído
        im = Image.new("RGBA", (w, h), rgb("#FFF3D6"))
        d = ImageDraw.Draw(im)
        for _ in range(420):
            x, y = rnd.uniform(0, w), rnd.uniform(0, h)
            c = rnd.choice(["#FF6400", "#A97BFF", "#FFDA4A", "#E3157A", "#1F1A2E", "#FFFFFF", "#22C1C3", "#4A1898"])
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


def celular(peca, tipo, largura_peca=0.66, cor_sil="#3C3A44"):
    w, h = 405, 720
    im = foto_generica(w, h, tipo)
    topo_cab = int(h * 0.40)
    silhueta(im, w / 2, topo_cab, w * 0.70, cor_sil)
    pw = int(w * largura_peca)
    ph = int(peca.height * pw / peca.width)
    p = peca.resize((pw, ph), Image.LANCZOS)
    im.alpha_composite(p, (int(w / 2 - pw / 2), int(topo_cab - ph - 8)))
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
    d.text((MARG, 36), "C07 · Simpatia da Virada — prévia das imagens", font=f_h1, fill=rgb("#1F1A2E"))
    d.text((MARG, 92), "Xadrez = transparente. Título e cartas: 512×256 (miniaturas aqui a 400×200). "
                       "Ordem da grade = ordem dos arquivos. Trecho entre parênteses em dourado. Ícone de envio: 162×162.",
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
        d.text((x, y + TH + 8), nome, font=f_lb, fill=rgb("#1F1A2E"))
        d.text((x, y + TH + 30), legenda, font=f_sm, fill=rgb("#6B6480"))
    y = y0 + alt_grade + 10
    d.text((MARG, y), "Ícone como aparece no app (cantos arredondados pelo próprio app): 162, 96 e 64 px",
           font=f_h2, fill=rgb("#1F1A2E"))
    x = MARG
    y += 50
    for nome, ic in icones:
        x_ini = x
        for tam in (162, 96, 64):
            a = arredondar(ic.resize((tam, tam), Image.LANCZOS))
            sheet.alpha_composite(a, (x, y + (162 - tam)))
            x += tam + 18
        d.text((x_ini, y + 172), nome, font=f_lb, fill=rgb("#1F1A2E"))
        x += 50
    for nome, ic in icones:  # área segura
        ic2 = ic.resize((162, 162), Image.LANCZOS).convert("RGBA")
        ImageDraw.Draw(ic2).rectangle([9, 9, 152, 152], outline=rgb("#00E5FF"), width=1)
        sheet.alpha_composite(ic2, (x, y))
        x += 162 + 18
    d.text((x - 2 * 180, y + 172), "linha ciano = área segura 144×144", font=f_sm, fill=rgb("#5B5470"))
    y = y0 + alt_grade + alt_icones
    d.text((MARG, y), "Simulação sobre fotos genéricas (largura da peça ≈ 66% da tela)", font=f_h2,
           fill=rgb("#1F1A2E"))
    y += 50
    x = MARG
    for rot, peca, tipo, cs in sims:
        cel = celular(peca, tipo, cor_sil=cs)
        sheet.alpha_composite(cel, (x, y))
        d.text((x, y + cel.height + 10), rot, font=f_lb, fill=rgb("#1F1A2E"))
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
    todos = [tx["titulo_topo"]["linha1"], tx["titulo_topo"]["linha2"], "TOQUE NA TELA"]
    for it in tx["resultados"] + tx["reservas"]:
        todos += [it["linha1"], it["linha2"]]
    checar_glifos("".join(todos))
    pecas = []
    l1, l2 = tx["titulo_topo"]["linha1"], tx["titulo_topo"]["linha2"]
    for com_toque, nome in ((True, "titulo_toque.png"), (False, "titulo.png")):
        t, tams = titulo(l1, l2, com_toque)
        salvar(t, os.path.join(AQUI, nome))
        salvar(quadrado(t), os.path.join(AQUI, "quadrado_512", nome))
        pecas.append((nome, t, ("título + aviso de toque (padrão)" if com_toque else "título sem aviso (reserva)")
                      + f" · {tams[0]}/{tams[1]}px"))

    tamanhos, imgs = {}, {}
    for i, item in enumerate(tx["resultados"]):
        cor = ORDEM_CORES[i % len(ORDEM_CORES)]
        im, tam = carta(item, cor, item["n"])
        nome = f"carta_{item['n']:02d}.png"
        salvar(im, os.path.join(AQUI, "cartas", nome))
        salvar(quadrado(im), os.path.join(AQUI, "quadrado_512", "cartas", nome))
        pecas.append((nome, im, f"{item['linha1']} / {item['linha2']} · {tam}px"))
        tamanhos[nome], imgs[nome] = tam, im
        esperado = item.get("fonte_px_no_layout_c01")
        if esperado and esperado != tam:
            print(f"aviso: {nome} saiu com {tam}px (redator mediu {esperado}px)")
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
        ic162 = icone(162, estilo)
        ic512 = icone(512, estilo)
        salvar(ic162, os.path.join(AQUI, f"icone{sufixo}_162.png"))
        salvar(ic512, os.path.join(AQUI, f"icone{sufixo}_512.png"))
        icones.append((f"icone{sufixo}_162.png", ic512))
        pecas.append((f"icone{sufixo}_162.png", ic512.convert("RGBA"),
                      "ícone de envio" + (" (alternativo: uva + meia-noite)" if sufixo else " (principal: uva + fogos)")))

    ordem = sorted(imgs, key=lambda n: tamanhos[n])
    sims = [
        ("titulo_toque.png · sala clara", pecas[0][1], "sala", "#3C3A44"),
        (f"{ordem[0]} · noite com fogos", imgs[ordem[0]], "noite", "#7A7488"),
        (f"{ordem[1]} · praia de dia", imgs[ordem[1]], "praia", "#3C3A44"),
        (f"{ordem[2]} · fundo poluído", imgs[ordem[2]], "confete", "#3C3A44"),
    ]
    salvar(previa(pecas, icones, sims), os.path.join(AQUI, "previa.png"))

    # lista de arquivos + somas
    linhas, total, efeito = [], 0, 0
    for raiz, _, arqs in sorted(os.walk(AQUI)):
        for a in sorted(arqs):
            if a.endswith(".png"):
                p = os.path.join(raiz, a)
                rel = os.path.relpath(p, AQUI)
                tb = os.path.getsize(p)
                total += tb
                if rel == "titulo_toque.png" or rel.startswith("cartas" + os.sep):
                    efeito += tb
                with Image.open(p) as im:
                    linhas.append(f"{rel:42s} {im.width}x{im.height}  {im.mode:5s} {tb / 1024:7.1f} KB")
                if tb >= 1024 * 1024:
                    print(f"ATENÇÃO: {rel} passou de 1 MB")
    linhas.append("")
    linhas.append(f"Entram no efeito (titulo_toque.png + cartas/*.png): {efeito / 1024 / 1024:.2f} MB")
    linhas.append(f"Todos os PNG desta pasta (inclui previa.png, quadrados e reservas): {total / 1024 / 1024:.2f} MB")
    with open(os.path.join(AQUI, "lista-de-arquivos.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(linhas) + "\n")
    print("\n".join(linhas))
    print("fonte usada por carta (px):", tamanhos)


if __name__ == "__main__":
    main()
