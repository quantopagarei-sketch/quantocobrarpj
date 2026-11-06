#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render.py: biblioteca para fazer vídeos 9:16 do TikTok (1080x1920, 30 fps) com os nossos PNGs.

Só usa Python 3 + Pillow + numpy + ffmpeg. Os quadros vão crus para o ffmpeg pela entrada padrão.
O som é feito aqui mesmo, com numpy (nada de música de terceiros).
Tudo é determinístico: a mesma semente gera o mesmo vídeo.

Uso rápido (ver LEIA-ME.md):
    python3 render.py --demo saida.mp4
    python3 render.py --info video.mp4
    python3 render.py --prancha video.mp4 -o prancha.png
"""
from __future__ import annotations

import argparse
import bisect
import functools
import glob
import io
import json
import math
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata
import wave
from collections import OrderedDict

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ============================================================================
# Constantes
# ============================================================================
W, H = 1080, 1920          # tamanho do vídeo
FPS = 30
SR = 44100                 # taxa de amostragem do áudio
SEMENTE = 2027             # semente padrão (determinístico)

AQUI = os.path.dirname(os.path.abspath(__file__))
PASTA_FONTES = "/usr/share/fonts/opentype/inter"
EMOJI_TTF = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
FONTES = {
    "titulo": "InterDisplay-Black.otf",     # títulos grandes
    "display": "InterDisplay-ExtraBold.otf",
    "black": "Inter-Black.otf",
    "extra": "Inter-ExtraBold.otf",
    "bold": "Inter-Bold.otf",
    "semi": "Inter-SemiBold.otf",
    "regular": "Inter-Regular.otf",
}

# Zonas da interface do TikTok (valores conservadores, em px num quadro 1080x1920).
# Fora destas margens, o texto pode ficar embaixo do nome, da legenda, dos botões ou da busca.
# Valores sem fonte oficial confirmada: (a confirmar) com um print do app.
ZONA = {"topo": 220, "base": 420, "direita": 140, "esquerda": 60}

# Paleta do C02 (mesmas cores do gerar.py do efeito 4)
PALETA = {
    "grafite": "#22252C", "asfalto": "#1E2026", "amarelo": "#FFD43B", "coral": "#FF7A52",
    "turquesa": "#1FC8C0", "lilas": "#9B7BFF", "prata": "#C6CED8", "creme": "#F2E2BE",
    "branco": "#FFFFFF", "contorno": "#1B1D24",
}
CORES_CONFETE = ["#FFD43B", "#FF7A52", "#1FC8C0", "#9B7BFF", "#FFFFFF", "#47EADB", "#FFB61A"]


# ============================================================================
# Cores e números
# ============================================================================
def rgba(c, alpha=None):
    """'#RRGGBB', '#RRGGBBAA', (r,g,b) ou (r,g,b,a) -> (r,g,b,a). alpha (0..1) troca a opacidade."""
    if isinstance(c, str):
        s = c.lstrip("#")
        if len(s) == 3:
            s = "".join(ch * 2 for ch in s)
        r, g, b = int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)
        a = int(s[6:8], 16) if len(s) == 8 else 255
    else:
        r, g, b = c[0], c[1], c[2]
        a = c[3] if len(c) > 3 else 255
    if alpha is not None:
        a = int(round(255 * max(0.0, min(1.0, alpha))))
    return (int(r), int(g), int(b), int(a))


def rgb(c):
    return rgba(c)[:3]


def misturar(c1, c2, p):
    a, b = rgba(c1), rgba(c2)
    return tuple(int(round(a[i] + (b[i] - a[i]) * p)) for i in range(4))


def limitar(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def lerp(a, b, p):
    return a + (b - a) * p


# ============================================================================
# Suavização (easing). Todas recebem p em 0..1 e devolvem ~0..1.
# ============================================================================
def linear(p): return p
def ease_in_quad(p): return p * p
def ease_out_quad(p): return 1 - (1 - p) ** 2
def ease_in_out_quad(p): return 2 * p * p if p < 0.5 else 1 - (-2 * p + 2) ** 2 / 2
def ease_in_cubic(p): return p ** 3
def ease_out_cubic(p): return 1 - (1 - p) ** 3
def ease_in_out_cubic(p): return 4 * p ** 3 if p < 0.5 else 1 - (-2 * p + 2) ** 3 / 2
def ease_out_quint(p): return 1 - (1 - p) ** 5
def ease_out_expo(p): return 1.0 if p >= 1 else 1 - 2 ** (-10 * p)
def ease_in_back(p, s=1.70158): return (s + 1) * p ** 3 - s * p ** 2


def ease_out_back(p, s=1.70158):
    p -= 1
    return 1 + (s + 1) * p ** 3 + s * p ** 2


def ease_out_elastic(p):
    if p <= 0: return 0.0
    if p >= 1: return 1.0
    return 2 ** (-10 * p) * math.sin((p * 10 - 0.75) * (2 * math.pi / 3)) + 1


def ease_out_bounce(p):
    n1, d1 = 7.5625, 2.75
    if p < 1 / d1: return n1 * p * p
    if p < 2 / d1:
        p -= 1.5 / d1; return n1 * p * p + 0.75
    if p < 2.5 / d1:
        p -= 2.25 / d1; return n1 * p * p + 0.9375
    p -= 2.625 / d1
    return n1 * p * p + 0.984375


def quique(t, amplitude=0.16, freq=2.4, amortecimento=5.0):
    """Mola amortecida: começa em +amplitude e vai a 0 balançando. Use como 1 + quique(t) na escala."""
    if t < 0: return 0.0
    return amplitude * math.exp(-amortecimento * t) * math.cos(2 * math.pi * freq * t)


SUAVES = {
    "linear": linear, "in_quad": ease_in_quad, "out_quad": ease_out_quad, "in_out_quad": ease_in_out_quad,
    "in_cubic": ease_in_cubic, "out_cubic": ease_out_cubic, "in_out_cubic": ease_in_out_cubic,
    "out_quint": ease_out_quint, "out_expo": ease_out_expo, "in_back": ease_in_back,
    "out_back": ease_out_back, "out_elastic": ease_out_elastic, "out_bounce": ease_out_bounce,
}


def progresso(t, inicio, duracao, suave=linear):
    """0 antes de 'inicio', 1 depois de 'inicio+duracao', suavizado no meio."""
    if duracao <= 0:
        return 1.0 if t >= inicio else 0.0
    f = SUAVES[suave] if isinstance(suave, str) else suave
    return f(limitar((t - inicio) / duracao))


def _v(x, tl):
    """Valor fixo ou função do tempo local."""
    return x(tl) if callable(x) else x


# ============================================================================
# Zonas seguras
# ============================================================================
def zona_segura():
    """Retângulo (x0, y0, x1, y1) onde texto e coisas importantes ficam visíveis."""
    return (ZONA["esquerda"], ZONA["topo"], W - ZONA["direita"], H - ZONA["base"])


def checar_zona_segura(caixa, margem=0):
    """Recebe a caixa (x0,y0,x1,y1) de um elemento. Devolve [] se estiver dentro da zona segura,
    ou uma lista de frases dizendo quanto passou de cada lado."""
    if caixa is None:
        return []
    x0, y0, x1, y1 = caixa
    sx0, sy0, sx1, sy1 = zona_segura()
    sx0 += margem; sy0 += margem; sx1 -= margem; sy1 -= margem
    prob = []
    if y0 < sy0: prob.append(("topo", sy0 - y0))
    if y1 > sy1: prob.append(("base", y1 - sy1))
    if x1 > sx1: prob.append(("direita", x1 - sx1))
    if x0 < sx0: prob.append(("esquerda", sx0 - x0))
    return [f"passa {int(round(px))} px na zona de {lado}" for lado, px in prob]


def desenhar_zonas(img, cor=(255, 40, 40, 70), contorno=(255, 255, 0, 200)):
    """Pinta por cima as faixas da interface do TikTok (para revisão). Funciona em qualquer tamanho 9:16."""
    im = img.convert("RGBA")
    k = im.width / W
    cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(cam)
    d.rectangle([0, 0, im.width, ZONA["topo"] * k], fill=cor)
    d.rectangle([0, im.height - ZONA["base"] * k, im.width, im.height], fill=cor)
    d.rectangle([im.width - ZONA["direita"] * k, ZONA["topo"] * k, im.width, im.height - ZONA["base"] * k], fill=cor)
    d.rectangle([0, ZONA["topo"] * k, ZONA["esquerda"] * k, im.height - ZONA["base"] * k], fill=(cor[0], cor[1], cor[2], cor[3] // 2))
    x0, y0, x1, y1 = [v * k for v in zona_segura()]
    d.rectangle([x0, y0, x1, y1], outline=contorno, width=max(1, int(2 * k + 0.5)))
    return Image.alpha_composite(im, cam).convert("RGB")


# ============================================================================
# Imagens: carregar, transformar, colar
# ============================================================================
_IMGS = {}            # caminho -> Image RGBA
_REFS = {}            # id -> Image (mantém referência viva para o cache)
_CACHE_RED = OrderedDict()


def carregar(img):
    """Caminho ou Image -> Image RGBA (com cache)."""
    if isinstance(img, Image.Image):
        im = img if img.mode == "RGBA" else img.convert("RGBA")
        _REFS[id(im)] = im
        return im
    p = os.path.abspath(img)
    if p not in _IMGS:
        _IMGS[p] = Image.open(p).convert("RGBA")
        _REFS[id(_IMGS[p])] = _IMGS[p]
    return _IMGS[p]


def carregar_pasta(pasta, padrao="*.png"):
    """Lista ordenada de imagens de uma pasta (ex.: cartas/carta_01..26.png)."""
    return [carregar(p) for p in sorted(glob.glob(os.path.join(pasta, padrao)))]


def _redimensionar(img, tamanho):
    """Redimensiona com LANCZOS (cache LRU). Ao ampliar mais de 15%, dá uma leve nitidez no RGB."""
    chave = (id(img), tamanho)
    if chave in _CACHE_RED:
        _CACHE_RED.move_to_end(chave)
        return _CACHE_RED[chave]
    _REFS[id(img)] = img
    out = img.resize(tamanho, Image.LANCZOS)
    if tamanho[0] > img.width * 1.15 and out.mode == "RGBA":
        r, g, b, a = out.split()
        nit = Image.merge("RGB", (r, g, b)).filter(ImageFilter.UnsharpMask(radius=1.6, percent=55, threshold=2))
        out = Image.merge("RGBA", (*nit.split(), a))
    _CACHE_RED[chave] = out
    if len(_CACHE_RED) > 80:
        _CACHE_RED.popitem(last=False)
    return out


def transformar(img, escala=1.0, rotacao=0.0, opacidade=1.0):
    """Escala, gira (graus, sentido anti-horário) e aplica opacidade (0..1). Devolve RGBA novo."""
    img = carregar(img)
    if abs(escala - 1.0) > 1e-3:
        tam = (max(1, int(round(img.width * escala))), max(1, int(round(img.height * escala))))
        img = _redimensionar(img, tam)
    if abs(rotacao) > 0.05:
        img = img.rotate(rotacao, resample=Image.BICUBIC, expand=True)
    if opacidade < 0.999:
        a = img.getchannel("A").point(lambda v, o=max(0.0, opacidade): int(v * o))
        img = img.copy()
        img.putalpha(a)
    return img


def _pintar(canvas, im, x0, y0):
    """Põe 'im' (RGBA) sobre o canvas na posição (x0, y0). Corta o que sair da tela."""
    if canvas.mode == "RGB":
        canvas.paste(im, (int(x0), int(y0)), im)
        return
    # canvas RGBA: alpha_composite não aceita destino negativo, então recorta
    x0, y0 = int(x0), int(y0)
    sx, sy = max(0, -x0), max(0, -y0)
    dx, dy = max(0, x0), max(0, y0)
    w = min(im.width - sx, canvas.width - dx)
    h = min(im.height - sy, canvas.height - dy)
    if w > 0 and h > 0:
        canvas.alpha_composite(im, (dx, dy), (sx, sy, sx + w, sy + h))


def colar(canvas, img, centro=(W / 2, H / 2), escala=1.0, rotacao=0.0, opacidade=1.0, ancora="centro", tinta=False):
    """Cola um PNG com transparência. 'ancora': 'centro', 'topo' (centro é o meio da borda de cima) ou 'base'.
    Devolve a caixa (x0,y0,x1,y1) ocupada. Com tinta=True, devolve só a parte visível (sem área transparente)."""
    if opacidade <= 0.004 or escala <= 0.004:
        return None
    im = transformar(img, escala, rotacao, opacidade)
    x, y = centro
    x0 = int(round(x - im.width / 2))
    if ancora == "topo":
        y0 = int(round(y))
    elif ancora == "base":
        y0 = int(round(y - im.height))
    else:
        y0 = int(round(y - im.height / 2))
    _pintar(canvas, im, x0, y0)
    if tinta:
        bb = im.getchannel("A").point(lambda v: 255 if v > 40 else 0).getbbox()
        if bb is None:
            return None
        return (x0 + bb[0], y0 + bb[1], x0 + bb[2], y0 + bb[3])
    return (x0, y0, x0 + im.width, y0 + im.height)


_TINTA = {}


def caixa_tinta(img, limiar=40):
    """Caixa (x0,y0,x1,y1) da parte visível da imagem (alpha > limiar), com cache."""
    img = carregar(img)
    k = id(img)
    if k not in _TINTA:
        _TINTA[k] = img.getchannel("A").point(lambda v: 255 if v > limiar else 0).getbbox()
    return _TINTA[k]


def caixa_nominal(img, centro, escala=1.0, rotacao=0.0, ancora="centro", caixa_local=None):
    """Onde a parte visível da imagem fica na tela, sem contar animação de entrada, pulso ou quique.
    É o que a checagem de zona segura usa."""
    img = carregar(img)
    bb = caixa_local or caixa_tinta(img)
    if bb is None:
        return None
    w, h = img.size
    a = math.radians(rotacao)
    tw = abs(w * escala * math.cos(a)) + abs(h * escala * math.sin(a))
    th = abs(w * escala * math.sin(a)) + abs(h * escala * math.cos(a))
    x0 = centro[0] - tw / 2
    y0 = centro[1] if ancora == "topo" else centro[1] - th if ancora == "base" else centro[1] - th / 2
    return _caixa_transformada(bb, (w, h), escala, rotacao, x0, y0, (tw, th))


def _e_arquivo_imagem(x):
    return isinstance(x, str) and os.path.splitext(x)[1].lower() in (".png", ".jpg", ".jpeg", ".webp") and os.path.isfile(x)


def ajustar(img, largura, altura):
    """Escala para caber em largura x altura sem distorcer (devolve a escala)."""
    img = carregar(img)
    return min(largura / img.width, altura / img.height)


# ============================================================================
# Fundos
# ============================================================================
def fundo_cor(cor):
    return Image.new("RGB", (W, H), rgb(cor))


def _degrade_array(cores, angulo, w, h, deslocamento=0.0, ciclico=False, escala=1.0):
    """Array (h, w, 3) uint8 com degradê linear. angulo em graus: 90 = de cima para baixo."""
    a = math.radians(angulo)
    dx, dy = math.cos(a), math.sin(a)
    xs = (np.arange(w) + 0.5) / w * W - W / 2
    ys = (np.arange(h) + 0.5) / h * H - H / 2
    proj = xs[None, :] * dx + ys[:, None] * dy
    meia = (abs(dx) * W + abs(dy) * H) / 2
    v = proj / (2 * meia) + 0.5
    cs = [rgb(c) for c in cores]
    if ciclico:
        v = (v * escala + deslocamento) % 1.0
        cs = cs + [cs[0]]
    else:
        v = np.clip(v * escala + deslocamento, 0, 1)
    pos = np.linspace(0, 1, len(cs))
    out = np.empty((h, w, 3), np.uint8)
    for i in range(3):
        out[..., i] = np.interp(v, pos, [c[i] for c in cs]).round().astype(np.uint8)
    return out


def fundo_degrade(cores, angulo=90):
    """Degradê parado. cores: lista de 2 ou mais cores."""
    arr = _degrade_array(cores, angulo, W // 4, H // 4)
    return Image.fromarray(arr, "RGB").resize((W, H), Image.BICUBIC)


class DegradeAnimado:
    """Degradê que flui devagar. Calculado em 1/4 da resolução e ampliado (rápido e liso)."""

    def __init__(self, cores, angulo=100, velocidade=0.06, giro=10.0, periodo_giro=7.0, escala=0.8):
        self.cores, self.angulo, self.vel = list(cores), angulo, velocidade
        self.giro, self.periodo, self.escala = giro, periodo_giro, escala

    def quadro(self, t):
        ang = self.angulo + self.giro * math.sin(2 * math.pi * t / self.periodo)
        arr = _degrade_array(self.cores, ang, W // 4, H // 4, deslocamento=t * self.vel, ciclico=True, escala=self.escala)
        return Image.fromarray(arr, "RGB").resize((W, H), Image.BILINEAR)


def cobrir(img):
    """Imagem preenchendo 1080x1920 sem distorcer (corta as sobras no meio). Devolve RGB."""
    im = carregar(img).convert("RGB")
    if im.size == (W, H):
        return im.copy()
    k = max(W / im.width, H / im.height)
    im = im.resize((max(W, int(math.ceil(im.width * k))), max(H, int(math.ceil(im.height * k)))), Image.LANCZOS)
    x0, y0 = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x0, y0, x0 + W, y0 + H))


def fundo_desfocado(img, raio=40, escurecer=0.35, tinta=None, tinta_forca=0.25):
    """Imagem preenchendo a tela (corta as sobras), desfocada e escurecida. Bom atrás de um PNG."""
    im = cobrir(img)
    peq = im.resize((W // 4, H // 4), Image.BILINEAR).filter(ImageFilter.GaussianBlur(max(1, raio / 4)))
    im = peq.resize((W, H), Image.BICUBIC)
    if tinta is not None:
        im = Image.blend(im, Image.new("RGB", (W, H), rgb(tinta)), tinta_forca)
    if escurecer > 0:
        im = Image.blend(im, Image.new("RGB", (W, H), (0, 0, 0)), escurecer)
    return im


def _estrela4(d, cx, cy, r, cor, fino=0.28):
    """Estrela de 4 pontas (brilho)."""
    q = r * fino
    pts = [(cx, cy - r), (cx + q, cy - q), (cx + r, cy), (cx + q, cy + q),
           (cx, cy + r), (cx - q, cy + q), (cx - r, cy), (cx - q, cy - q)]
    d.polygon(pts, fill=cor)


class Padrao:
    """Padrão ilustrado simples que se repete e pode deslizar.
    tipo: 'bolinhas', 'listras', 'xadrez', 'estrelas', 'tracejado', 'mais', 'emoji'.
    fundo: cor, Image, ou objeto com .quadro(t) (ex.: DegradeAnimado).
    velocidade: (vx, vy) em px/s (vy > 0 desce)."""

    def __init__(self, tipo="bolinhas", cor_forma=(255, 255, 255, 30), fundo="#22252C", tamanho=160,
                 velocidade=(0, 40), emoji="✨"):
        self.T = int(tamanho)
        self.vel = velocidade
        tile = self._tile(tipo, rgba(cor_forma), emoji)
        nx, ny = W // self.T + 2, H // self.T + 2
        grande = Image.new("RGBA", (nx * self.T, ny * self.T), (0, 0, 0, 0))
        for i in range(nx):
            for j in range(ny):
                grande.paste(tile, (i * self.T, j * self.T))
        self.grande = grande
        self.fundo_anim = None
        if hasattr(fundo, "quadro") or callable(fundo):
            self.fundo_anim = fundo
        else:
            base = fundo if isinstance(fundo, Image.Image) else Image.new("RGBA", grande.size, rgba(fundo))
            if base.size != grande.size:
                b2 = Image.new("RGBA", grande.size, (0, 0, 0, 255))
                for i in range(0, grande.width, base.width):
                    for j in range(0, grande.height, base.height):
                        b2.paste(base.convert("RGBA"), (i, j))
                base = b2
            self.grande = Image.alpha_composite(base.convert("RGBA"), grande).convert("RGB")

    def _tile(self, tipo, cor, emoji):
        T, S = self.T, 3
        big = Image.new("RGBA", (T * S, T * S), (0, 0, 0, 0))
        d = ImageDraw.Draw(big)
        TT = T * S
        offs = [(ox, oy) for ox in (-TT, 0, TT) for oy in (-TT, 0, TT)]
        if tipo == "bolinhas":
            for ox, oy in offs:
                for (cx, cy, r) in ((0.25, 0.25, 0.10), (0.75, 0.75, 0.10)):
                    d.ellipse([ox + (cx - r) * TT, oy + (cy - r) * TT, ox + (cx + r) * TT, oy + (cy + r) * TT], fill=cor)
        elif tipo == "listras":
            bw = 0.22 * TT
            for a in (-2 * TT, -TT, 0, TT, 2 * TT):
                d.polygon([(a, 0), (a + bw, 0), (a + bw + TT, TT), (a + TT, TT)], fill=cor)
        elif tipo == "xadrez":
            d.rectangle([0, 0, TT / 2 - 1, TT / 2 - 1], fill=cor)
            d.rectangle([TT / 2, TT / 2, TT - 1, TT - 1], fill=cor)
        elif tipo == "estrelas":
            for ox, oy in offs:
                _estrela4(d, ox + 0.28 * TT, oy + 0.30 * TT, 0.13 * TT, cor)
                _estrela4(d, ox + 0.76 * TT, oy + 0.74 * TT, 0.07 * TT, cor)
        elif tipo == "tracejado":
            w, h = 0.07 * TT, 0.36 * TT
            for ox, oy in offs:
                for (cx, cy) in ((0.25, 0.30), (0.75, 0.80)):
                    d.rounded_rectangle([ox + cx * TT - w / 2, oy + cy * TT - h / 2, ox + cx * TT + w / 2, oy + cy * TT + h / 2],
                                        radius=w / 2, fill=cor)
        elif tipo == "mais":
            w, h = 0.05 * TT, 0.22 * TT
            for ox, oy in offs:
                for (cx, cy) in ((0.25, 0.25), (0.75, 0.75)):
                    X, Y = ox + cx * TT, oy + cy * TT
                    d.rounded_rectangle([X - w / 2, Y - h / 2, X + w / 2, Y + h / 2], radius=w / 2, fill=cor)
                    d.rounded_rectangle([X - h / 2, Y - w / 2, X + h / 2, Y + w / 2], radius=w / 2, fill=cor)
        elif tipo == "emoji":
            e = emoji_img(emoji, int(0.30 * TT))
            if cor[3] < 255:
                a = e.getchannel("A").point(lambda v: int(v * cor[3] / 255))
                e = e.copy(); e.putalpha(a)
            for (cx, cy, ang) in ((0.25, 0.27, 12), (0.75, 0.77, -12)):
                er = e.rotate(ang, resample=Image.BICUBIC, expand=True)
                for ox, oy in offs:
                    X, Y = int(ox + cx * TT - er.width / 2), int(oy + cy * TT - er.height / 2)
                    _pintar(big, er, X, Y)
        else:
            raise ValueError(f"tipo de padrão desconhecido: {tipo}")
        return big.resize((T, T), Image.LANCZOS)

    def quadro(self, t):
        vx, vy = self.vel
        ox = int(round((-vx * t) % self.T))
        oy = int(round((-vy * t) % self.T))
        corte = self.grande.crop((ox, oy, ox + W, oy + H))
        if self.fundo_anim is None:
            return corte
        base = self.fundo_anim.quadro(t) if hasattr(self.fundo_anim, "quadro") else self.fundo_anim(t)
        base = base.convert("RGB") if base.mode != "RGB" else base
        base.paste(corte, (0, 0), corte)
        return base


# ============================================================================
# Texto com fonte Inter, contorno, sombra, quebra automática e emoji colorido
# ============================================================================
@functools.lru_cache(maxsize=256)
def fonte(nome="titulo", tamanho=72):
    arq = FONTES.get(nome, nome)
    caminho = arq if os.path.isabs(arq) else os.path.join(PASTA_FONTES, arq)
    return ImageFont.truetype(caminho, int(tamanho))


@functools.lru_cache(maxsize=1)
def _fonte_emoji():
    return ImageFont.truetype(EMOJI_TTF, size=109)   # a Noto Color Emoji só funciona em 109


@functools.lru_cache(maxsize=256)
def _emoji_base(e):
    im = Image.new("RGBA", (136, 128), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((0, 0), e, font=_fonte_emoji(), embedded_color=True)
    return im


@functools.lru_cache(maxsize=512)
def emoji_img(e, altura):
    """Emoji colorido (Noto) desenhado em 109 e redimensionado para 'altura' px."""
    base = _emoji_base(e)
    altura = max(4, int(altura))
    return base.resize((max(4, int(round(altura * 136 / 128))), altura), Image.LANCZOS)


def _e_emoji_base(cp):
    return (0x1F000 <= cp <= 0x1FAFF or 0x2600 <= cp <= 0x27BF or 0x2300 <= cp <= 0x23FF
            or cp in (0x2B50, 0x2B55, 0x2B1B, 0x2B1C, 0x2B05, 0x2B06, 0x2B07, 0x3030, 0x303D, 0x3297, 0x3299))


def segmentar(texto):
    """Divide em pedaços (texto, é_emoji). Junta sequências com ZWJ, tons de pele, bandeiras e keycaps."""
    out = []
    i, n = 0, len(texto)
    while i < n:
        ch = texto[i]
        cp = ord(ch)
        prox = ord(texto[i + 1]) if i + 1 < n else 0
        keycap = ch in "0123456789#*" and prox == 0xFE0F and i + 2 < n and ord(texto[i + 2]) == 0x20E3
        if _e_emoji_base(cp) or prox == 0xFE0F or keycap:
            j = i + 1
            if 0x1F1E6 <= cp <= 0x1F1FF and j < n and 0x1F1E6 <= ord(texto[j]) <= 0x1F1FF:
                j += 1  # bandeira (par de letras regionais)
            while j < n:
                c2 = ord(texto[j])
                if c2 in (0xFE0F, 0xFE0E, 0x20E3) or 0x1F3FB <= c2 <= 0x1F3FF or 0xE0020 <= c2 <= 0xE007F:
                    j += 1
                elif c2 == 0x200D and j + 1 < n:
                    j += 2
                else:
                    break
            seq = texto[i:j]
            if keycap or _e_emoji_base(cp) or "️" in seq:
                out.append((seq, True))
            else:
                out.append((seq, False))
            i = j
        else:
            out.append((ch, False))
            i += 1
    return out


def _parse(texto):
    """'*palavra*' liga a cor de destaque. '\\*' é um asterisco de verdade. -> [(pedaço, emoji, destaque)]"""
    runs, buf, dest, i = [], "", False, 0
    while i < len(texto):
        ch = texto[i]
        if ch == "\\" and i + 1 < len(texto) and texto[i + 1] == "*":
            buf += "*"; i += 2; continue
        if ch == "*":
            if buf:
                runs.append((buf, dest)); buf = ""
            dest = not dest; i += 1; continue
        buf += ch; i += 1
    if buf:
        runs.append((buf, dest))
    out = []
    for s, d in runs:
        for cl, em in segmentar(s):
            out.append((cl, em, d))
    return out


def contar_letras(texto):
    """Quantas 'letras' (emoji conta 1, espaço conta 1) o texto tem. Usado pelo 'digitar'."""
    return sum(1 for cl, em, d in _parse(texto) if cl != "\n")


def _layout(texto, tam, nome_fonte, largura_max, contorno):
    f = fonte(nome_fonte, tam)
    eh = int(round(tam * 0.98))
    ew = int(round(eh * 136 / 128))
    esp = f.getlength(" ")
    toks, cur = [], []

    def fecha():
        nonlocal cur
        if cur:
            toks.append(("w", cur)); cur = []

    for cl, em, d in _parse(texto):
        if not em and cl == "\n":
            fecha(); toks.append(("n", None))
        elif not em and cl.isspace():
            fecha(); toks.append(("s", None))
        elif cur and not em and not cur[-1][1] and cur[-1][2] == d:
            cur[-1] = (cur[-1][0] + cl, False, d)
        else:
            cur.append((cl, em, d))
    fecha()
    # emoji sozinho não fica órfão: gruda na palavra de antes (espaço que não quebra)
    colado = []
    for tok in toks:
        if (tok[0] == "w" and all(r[1] for r in tok[1]) and len(colado) >= 2
                and colado[-1][0] == "s" and colado[-2][0] == "w"):
            colado.pop()
            ant = colado.pop()
            colado.append(("w", ant[1] + [(" ", False, ant[1][-1][2])] + tok[1]))
        else:
            colado.append(tok)
    toks = colado

    def larg_run(r):
        return ew if r[1] else f.getlength(r[0])

    linhas, linha, lw, maior_palavra = [], [], 0.0, 0.0
    lim = largura_max - 2 * contorno if largura_max else None
    pend_esp = False
    for tipo, val in toks:
        if tipo == "n":
            linhas.append((linha, lw)); linha, lw, pend_esp = [], 0.0, False
        elif tipo == "s":
            pend_esp = bool(linha)
        else:
            wl = sum(larg_run(r) for r in val)
            maior_palavra = max(maior_palavra, wl)
            if linha and lim and lw + (esp if pend_esp else 0) + wl > lim:
                linhas.append((linha, lw)); linha, lw, pend_esp = [], 0.0, False
            x = lw + (esp if (pend_esp and linha) else 0)
            pos = []
            for r in val:
                pos.append((x, r)); x += larg_run(r)
            linha.append(pos); lw = x; pend_esp = False
    linhas.append((linha, lw))
    return f, linhas, maior_palavra, eh, ew


@functools.lru_cache(maxsize=384)
def texto_img(texto, tamanho=72, fonte_nome="titulo", cor="#FFFFFF", cor_destaque="#FFD43B", contorno=10,
              cor_contorno="#1B1D24", sombra=(0, 8, 12, 150), largura_max=800, alinhamento="centro",
              entrelinha=1.08, max_linhas=None, encolher=True, caixa=None, caixa_pad=(30, 18), caixa_raio=28,
              visiveis=None):
    """Desenha um texto e devolve uma imagem RGBA recortada.
    - '*assim*' pinta com cor_destaque; '\\n' quebra a linha; emoji colorido funciona.
    - largura_max: quebra a linha sozinho; com encolher=True, diminui a fonte se uma palavra não couber
      ou se passar de max_linhas.
    - sombra: (dx, dy, desfoque, opacidade 0..255) ou None.
    - caixa: cor de uma pílula atrás do texto (estilo legenda) ou None.
    - visiveis: desenha só as N primeiras letras (para 'digitar'), sem mudar o tamanho da imagem.
    A caixa do texto (sem a sombra) fica em img.info['caixa']."""
    tam = int(tamanho)
    while True:
        f, linhas, maior, eh, ew = _layout(texto, tam, fonte_nome, largura_max, contorno)
        cabe = (not largura_max or maior <= largura_max - 2 * contorno) and (not max_linhas or len(linhas) <= max_linhas)
        if cabe or not encolher or tam <= 18:
            break
        tam = max(18, int(tam * 0.93))
    asc, desc = f.getmetrics()
    cap = -f.getbbox("H", anchor="ls")[1]
    lh = tam * entrelinha
    sdx, sdy, sblur, salpha = sombra if sombra else (0, 0, 0, 0)
    cpx, cpy = caixa_pad if caixa else (0, 0)
    pad = int(contorno + 2 * sblur + max(abs(sdx), abs(sdy)) + max(cpx, cpy) + 4)
    largura_txt = max([lw for _, lw in linhas] + [1])
    Wi = int(math.ceil(largura_txt + 2 * pad))
    Hi = int(math.ceil(pad * 2 + asc + desc + (len(linhas) - 1) * lh))
    camada = Image.new("RGBA", (Wi, Hi), (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)

    def x_linha(lw):
        if alinhamento in ("esquerda", "esq"):
            return pad
        if alinhamento in ("direita", "dir"):
            return pad + largura_txt - lw
        return pad + (largura_txt - lw) / 2

    # pílula atrás do texto
    if caixa:
        y_top = pad + asc - cap - cpy - tam * 0.06
        y_bot = pad + asc + (len(linhas) - 1) * lh + desc * 0.35 + cpy
        xs = [x_linha(lw) for _, lw in linhas]
        x0 = min(xs) - cpx
        x1 = max(x + lw for x, (_, lw) in zip(xs, linhas)) + cpx
        d.rounded_rectangle([x0, y_top, x1, y_bot], radius=caixa_raio, fill=rgba(caixa))

    restante = [10 ** 9 if visiveis is None else int(visiveis)]

    def passe(stroke):
        restante[0] = 10 ** 9 if visiveis is None else int(visiveis)
        for li, (linha, lw) in enumerate(linhas):
            base = pad + asc + li * lh
            x0 = x_linha(lw)
            for wi, palavra in enumerate(linha):
                if wi > 0:
                    restante[0] -= 1  # o espaço conta
                for x, (s, em, dest) in palavra:
                    if restante[0] <= 0:
                        return
                    if em:
                        restante[0] -= 1
                        e = emoji_img(s, eh)
                        ex, ey = int(round(x0 + x)), int(round(base - cap / 2 - eh / 2))
                        if stroke:
                            if contorno > 0:
                                k = min(2 * int(contorno * 0.8) + 1, 25)
                                pad_k = k // 2
                                sil2 = Image.new("L", (e.width + 2 * pad_k, e.height + 2 * pad_k), 0)
                                sil2.paste(e.getchannel("A"), (pad_k, pad_k))
                                sil2 = sil2.filter(ImageFilter.MaxFilter(k)) if k >= 3 else sil2
                                cc = Image.new("RGBA", sil2.size, rgba(cor_contorno))
                                camada.paste(cc, (ex - pad_k, ey - pad_k), sil2)
                        else:
                            camada.alpha_composite(e, (max(0, ex), max(0, ey)))
                    else:
                        parte = s[:restante[0]]
                        restante[0] -= len(s)
                        if stroke:
                            if contorno > 0:
                                d.text((x0 + x, base), parte, font=f, anchor="ls", fill=rgba(cor_contorno),
                                       stroke_width=int(contorno), stroke_fill=rgba(cor_contorno))
                        else:
                            d.text((x0 + x, base), parte, font=f, anchor="ls", fill=rgba(cor_destaque if dest else cor))
            restante[0] -= 1  # quebra de linha conta como espaço

    passe(True)
    passe(False)
    caixa_tinta = camada.getbbox()
    if sombra and salpha > 0:
        a = camada.getchannel("A")
        sa = Image.new("L", camada.size, 0)
        sa.paste(a, (int(sdx), int(sdy)))
        if sblur > 0:
            sa = sa.filter(ImageFilter.GaussianBlur(sblur))
        sa = sa.point(lambda v: int(v * salpha / 255))
        sombra_img = Image.new("RGBA", camada.size, (0, 0, 0, 255))
        sombra_img.putalpha(sa)
        camada = Image.alpha_composite(sombra_img, camada)
    camada.info["caixa"] = caixa_tinta
    camada.info["tamanho_usado"] = tam
    return camada


def _caixa_transformada(caixa_local, tam_img, escala, rot, x0, y0, tam_final):
    """Converte a caixa da tinta (coords da imagem original) para coords da tela, depois de escala/rotação."""
    if caixa_local is None:
        return None
    bx0, by0, bx1, by1 = caixa_local
    w, h = tam_img
    cx, cy = w / 2, h / 2
    a = math.radians(-rot)
    ca, sa = math.cos(a), math.sin(a)
    pts = []
    for (px, py) in ((bx0, by0), (bx1, by0), (bx0, by1), (bx1, by1)):
        X, Y = (px - cx) * escala, (py - cy) * escala
        pts.append((X * ca - Y * sa, X * sa + Y * ca))
    fx, fy = x0 + tam_final[0] / 2, y0 + tam_final[1] / 2
    xs = [p[0] + fx for p in pts]; ys = [p[1] + fy for p in pts]
    return (min(xs), min(ys), max(xs), max(ys))


# ============================================================================
# Sprites prontos (brilho, luz, anel)
# ============================================================================
@functools.lru_cache(maxsize=16)
def sprite_brilho(cor="#FFFFFF", tamanho=160):
    S = 4
    big = Image.new("RGBA", (tamanho * S, tamanho * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    c = tamanho * S / 2
    _estrela4(d, c, c, c * 0.92, rgba(cor), fino=0.16)
    im = big.resize((tamanho, tamanho), Image.LANCZOS)
    halo = im.getchannel("A").filter(ImageFilter.GaussianBlur(tamanho * 0.06)).point(lambda v: int(v * 0.8))
    glow = Image.new("RGBA", im.size, rgba(cor)); glow.putalpha(halo)
    return Image.alpha_composite(glow, im)


@functools.lru_cache(maxsize=16)
def sprite_luz(raio=420, cor="#FFFFFF", forca=1.0):
    """Luz redonda (degradê radial) com transparência."""
    n = 2 * raio
    y, x = np.mgrid[0:n, 0:n]
    r = np.sqrt((x - raio + 0.5) ** 2 + (y - raio + 0.5) ** 2) / raio
    a = np.clip(1 - r, 0, 1) ** 2.2 * 255 * forca
    im = Image.new("RGBA", (n, n), rgba(cor))
    im.putalpha(Image.fromarray(a.astype(np.uint8), "L"))
    return im


# ============================================================================
# Áudio original (numpy)
# ============================================================================
def _t(dur):
    return np.arange(int(round(dur * SR))) / SR


def _normal(x, pico=0.9):
    m = np.max(np.abs(x)) if len(x) else 0
    return x * (pico / m) if m > 0 else x


def _passa_baixa(x, fc):
    """Filtro passa-baixa de 1 polo. fc pode ser número ou array (variando no tempo)."""
    fc = np.broadcast_to(np.asarray(fc, dtype=float), x.shape)
    a = 1 - np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc += a[i] * (x[i] - acc)
        y[i] = acc
    return y


@functools.lru_cache(maxsize=256)
def som_tique(freq=2400, dur=0.045, semente=0):
    """Tique curto de roleta (madeira + clique)."""
    t = _t(dur)
    rng = np.random.default_rng(1000 + int(semente))
    corpo = np.sin(2 * np.pi * freq * t) * np.exp(-t / 0.0065)
    corpo2 = 0.45 * np.sin(2 * np.pi * freq * 1.52 * t) * np.exp(-t / 0.004)
    madeira = 0.7 * np.sin(2 * np.pi * freq * 0.36 * t) * np.exp(-t / 0.011)
    clique = np.diff(rng.standard_normal(len(t)) * np.exp(-t / 0.0012), prepend=0.0) * 0.35
    return _normal(corpo + corpo2 + madeira + clique, 0.9).astype(np.float32)


@functools.lru_cache(maxsize=16)
def som_plim(nota=1318.51, duas=True, dur=1.2):
    """'Plim' de sino no resultado (duas notas: a segunda uma quinta acima)."""
    def sino(f):
        t = _t(dur)
        parc = [(1.0, 1.0, 0.55), (2.0, 0.42, 0.30), (3.0, 0.22, 0.17), (4.16, 0.12, 0.09), (5.43, 0.06, 0.05)]
        s = sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t / tau) for m, a, tau in parc)
        return s * np.minimum(1, t / 0.002)
    s = sino(nota)
    if duas:
        b = sino(nota * 1.5) * 0.85
        off = int(0.085 * SR)
        s[off:] += b[: len(s) - off]
    return _normal(s, 0.9).astype(np.float32)


@functools.lru_cache(maxsize=16)
def som_vush(dur=0.42, sobe=True, semente=7):
    """'Vush' de transição (ruído filtrado que abre e fecha). Já vem em estéreo, passando da esquerda p/ direita."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    p = t / dur
    rng = np.random.default_rng(semente)
    ruido = rng.standard_normal(n)
    env = np.sin(np.pi * np.clip(p, 0, 1) ** (0.75 if sobe else 1.3)) ** 2
    fc = 300 + 5200 * env
    y = _passa_baixa(_passa_baixa(ruido, fc), fc)
    y = y - _passa_baixa(y, 180.0)
    y = _normal(y * env, 0.85)
    pan = np.linspace(-0.6, 0.6, n) if sobe else np.linspace(0.6, -0.6, n)
    ang = (pan + 1) * np.pi / 4
    return np.stack([y * np.cos(ang), y * np.sin(ang)], axis=1).astype(np.float32) * 1.3


@functools.lru_cache(maxsize=16)
def som_pop(f0=380.0, f1=1150.0, dur=0.11):
    """'Pop' de bolha (o tom sobe rápido)."""
    t = _t(dur)
    f = f0 + (f1 - f0) * (1 - np.exp(-t / 0.018))
    fase = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(fase) * np.exp(-t / 0.032) * np.minimum(1, t / 0.0015)
    return _normal(s, 0.9).astype(np.float32)


@functools.lru_cache(maxsize=16)
def som_bip(freq=880.0, dur=0.16):
    """Bipe da contagem regressiva."""
    t = _t(dur)
    s = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(2 * np.pi * 2 * freq * t)
    s = np.tanh(2.2 * s) * np.minimum(1, t / 0.003) * np.exp(-t / 0.07)
    return _normal(s, 0.85).astype(np.float32)


@functools.lru_cache(maxsize=8)
def som_tecla(semente=0):
    """Clique de tecla (para texto sendo digitado)."""
    t = _t(0.03)
    rng = np.random.default_rng(300 + semente)
    s = np.diff(rng.standard_normal(len(t)), prepend=0.0) * np.exp(-t / 0.0025)
    s += 0.6 * np.sin(2 * np.pi * 1750 * t) * np.exp(-t / 0.004)
    return _normal(s, 0.8).astype(np.float32)


@functools.lru_cache(maxsize=4)
def som_toque():
    """Toque na tela (um 'toc' suave)."""
    t = _t(0.06)
    s = np.sin(2 * np.pi * 950 * t) * np.exp(-t / 0.012) + 0.4 * np.sin(2 * np.pi * 2300 * t) * np.exp(-t / 0.005)
    return _normal(s, 0.8).astype(np.float32)


SONS = {"tique": som_tique, "plim": som_plim, "vush": som_vush, "pop": som_pop, "bip": som_bip,
        "tecla": som_tecla, "toque": som_toque}


def _midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def _bumbo():
    t = _t(0.34)
    f = 46 + 100 * np.exp(-t / 0.038)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.17)
    s[: int(0.003 * SR)] += np.linspace(0.6, 0, int(0.003 * SR))
    return np.tanh(1.6 * s)


def _palma(rng):
    t = _t(0.22)
    r = np.diff(rng.standard_normal(len(t)), prepend=0.0)
    env = np.exp(-t / 0.045)
    for k in (0.0, 0.011, 0.022):
        env += 0.8 * np.exp(-np.maximum(0, t - k) / 0.004) * (t >= k)
    s = _passa_baixa(r * env, 3200.0)
    return _normal(s, 0.8)


def _chimbal(rng, aberto=False):
    t = _t(0.16 if aberto else 0.05)
    r = np.diff(np.diff(rng.standard_normal(len(t)), prepend=0.0), prepend=0.0)
    return _normal(r * np.exp(-t / (0.05 if aberto else 0.014)), 0.6)


def _baixo(f, dur=0.32):
    t = _t(dur)
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) + 0.12 * np.sin(2 * np.pi * 3 * f * t)
    return np.tanh(1.4 * s) * np.minimum(1, t / 0.004) * np.exp(-t / 0.2)


def _dedilhado(f, dur=0.28):
    t = _t(dur)
    s = np.sin(2 * np.pi * f * t) + 0.22 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t / 0.02)
    return s * np.minimum(1, t / 0.002) * np.exp(-t / 0.09)


def trilha_ritmica(duracao, bpm=112, semente=SEMENTE, progressao=None):
    """Fundo rítmico simples e original: bumbo, palma, chimbal, baixo e um dedilhado.
    progressao: lista de (nota_midi_do_baixo, 'm' ou '') por compasso. Devolve array (n, 2)."""
    rng = np.random.default_rng(semente)
    n = int(round(duracao * SR)) + 1
    L = np.zeros(n); R = np.zeros(n)
    prog = progressao or [(45, "m"), (41, ""), (48, ""), (43, "")]
    beat = 60.0 / bpm
    bumbo = _bumbo()
    palmas = [_palma(rng) for _ in range(2)]
    chimbais = [_chimbal(rng) for _ in range(3)]
    chimbal_ab = _chimbal(rng, True)

    def add(sinal, t0, vol, pan=0.0):
        i0 = int(round(t0 * SR))
        if i0 >= n:
            return
        m = min(len(sinal), n - i0)
        a = (pan + 1) * np.pi / 4
        L[i0:i0 + m] += sinal[:m] * vol * math.cos(a) * 1.4142
        R[i0:i0 + m] += sinal[:m] * vol * math.sin(a) * 1.4142

    arp = [0, 1, 2, 1, 3, 2, 1, 2, 0, 1, 2, 3, 2, 1, 2, 1]
    toca_arp = [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0]
    baixo_8 = [1, 0, 1, 1, 0, 1, 1, 0]
    ncomp = int(math.ceil(duracao / (4 * beat))) + 1
    for c in range(ncomp):
        raiz, q = prog[c % len(prog)]
        tri = [0, 3, 7, 12] if q == "m" else [0, 4, 7, 12]
        t_c = c * 4 * beat
        for b in range(4):
            tb = t_c + b * beat
            if b in (0, 2):
                add(bumbo, tb, 0.9)
            if b == 3 and c % 2 == 1:
                add(bumbo, tb + beat / 2, 0.55)
            if b in (1, 3):
                add(palmas[(c + b) % 2], tb, 0.30, 0.05)
            add(chimbais[(c + b) % 3], tb, 0.16, 0.35)
            if b == 3:
                add(chimbal_ab, tb + beat / 2, 0.14, 0.35)
            else:
                add(chimbais[(c + b + 1) % 3], tb + beat / 2, 0.24, 0.35)
        for k in range(8):
            if baixo_8[k]:
                add(_baixo(_midi(raiz)), t_c + k * beat / 2, 0.5, -0.05)
        for k in range(16):
            if toca_arp[k]:
                nota = raiz + 24 + tri[arp[k]]
                add(_dedilhado(_midi(nota)), t_c + k * beat / 4, 0.16 + 0.04 * (k % 4 == 0), -0.35)
    s = np.stack([L, R], axis=1)[: int(round(duracao * SR))]
    s = np.tanh(s * 0.9)
    fade_in, fade_out = int(0.25 * SR), int(0.8 * SR)
    s[:fade_in] *= np.linspace(0, 1, fade_in)[:, None]
    s[-fade_out:] *= np.linspace(1, 0, fade_out)[:, None]
    return _normal(s, 0.9).astype(np.float32)


def _estereo(arr, pan=0.0):
    if arr.ndim == 2:
        return arr
    a = (pan + 1) * np.pi / 4
    return np.stack([arr * math.cos(a), arr * math.sin(a)], axis=1) * 1.4142


def _media_movel(x, janela):
    c = np.cumsum(np.concatenate([[0.0], x]))
    m = (c[janela:] - c[:-janela]) / janela
    return np.concatenate([np.full(janela // 2, m[0]), m, np.full(len(x) - len(m) - janela // 2, m[-1])])


def masterizar(x, rms_alvo_db=-15.5, pico_db=-1.5, ganho_max_db=12.0):
    """Normaliza o volume (RMS alvo), passa num limitador suave e deixa o pico em -1,5 dBFS (folga para o AAC)."""
    x = x.astype(np.float64)
    rms = float(np.sqrt(np.mean(x ** 2))) if len(x) else 0.0
    if rms > 1e-7:
        x *= min(10 ** (rms_alvo_db / 20) / rms, 10 ** (ganho_max_db / 20))
    limiar = 0.7
    ax = np.abs(x)
    acima = ax > limiar
    x[acima] = np.sign(x[acima]) * (limiar + (1 - limiar) * np.tanh((ax[acima] - limiar) / (1 - limiar)))
    pico = np.max(np.abs(x)) if len(x) else 0
    alvo = 10 ** (pico_db / 20)
    if pico > 0:
        x *= alvo / pico
    f = int(0.004 * SR)
    if len(x) > 2 * f:
        x[:f] *= np.linspace(0, 1, f)[:, None]
        x[-f:] *= np.linspace(1, 0, f)[:, None]
    return x.astype(np.float32)


def mixar(duracao, eventos, trilha=None, volume_trilha=0.32, ducking=0.45):
    """eventos: lista de (t, array, volume, pan). trilha: array (n,2) ou None.
    Os efeitos abaixam a trilha um pouco quando tocam (ducking 0..1)."""
    n = int(round(duracao * SR))
    sfx = np.zeros((n, 2), np.float64)
    for t, arr, vol, pan in eventos:
        a = _estereo(np.asarray(arr, dtype=np.float64), pan)
        i0 = int(round(t * SR))
        if i0 < 0:
            a = a[-i0:]; i0 = 0
        if i0 >= n or len(a) == 0:
            continue
        m = min(len(a), n - i0)
        sfx[i0:i0 + m] += a[:m] * vol
    mix = sfx
    if trilha is not None and volume_trilha > 0:
        tr = np.zeros((n, 2)); m = min(n, len(trilha)); tr[:m] = trilha[:m]
        if ducking > 0 and np.any(sfx):
            env = _media_movel(np.abs(sfx).mean(axis=1), int(0.06 * SR))
            env = env / (np.max(env) + 1e-9)
            ganho = 1 - ducking * np.clip(env * 2.5, 0, 1)
            tr *= ganho[:, None]
        mix = sfx + tr * volume_trilha
    return masterizar(mix)


def salvar_wav(caminho, x):
    """Salva array (n,2) float -1..1 como WAV 16 bits estéreo 44,1 kHz."""
    x16 = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(caminho, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(np.ascontiguousarray(x16).tobytes())


# ============================================================================
# Exportar: JPG de slide, info do vídeo, prancha de quadros
# ============================================================================
def salvar_jpg(img, caminho, max_kb=500):
    """Salva 1080x1920 em JPG com no máximo max_kb. Baixa a qualidade até caber. Devolve (qualidade, KB)."""
    im = img.convert("RGB")
    if im.size != (W, H):
        im = im.resize((W, H), Image.LANCZOS)
    for sub in (0, 2):
        for q in range(94, 40, -4):
            b = io.BytesIO()
            im.save(b, "JPEG", quality=q, optimize=True, progressive=True, subsampling=sub)
            if b.tell() <= max_kb * 1024:
                with open(caminho, "wb") as f:
                    f.write(b.getvalue())
                return q, b.tell() / 1024
    with open(caminho, "wb") as f:
        f.write(b.getvalue())
    return q, b.tell() / 1024


def info_video(mp4):
    """Lê o mp4 com ffprobe. Devolve dict com duração, tamanho, codecs, resolução, fps e áudio."""
    r = subprocess.run(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", mp4],
                       capture_output=True, text=True, check=True)
    j = json.loads(r.stdout)
    fmt = j["format"]
    v = next((s for s in j["streams"] if s["codec_type"] == "video"), {})
    a = next((s for s in j["streams"] if s["codec_type"] == "audio"), None)
    num, den = (v.get("r_frame_rate", "0/1").split("/") + ["1"])[:2]
    info = {
        "arquivo": mp4,
        "duracao_s": round(float(fmt.get("duration", 0)), 3),
        "tamanho_bytes": int(fmt.get("size", os.path.getsize(mp4))),
        "tamanho_mb": round(int(fmt.get("size", 0)) / 1024 / 1024, 2),
        "bitrate_kbps": round(int(fmt.get("bit_rate", 0)) / 1000),
        "video": {"codec": v.get("codec_name"), "perfil": v.get("profile"), "pix_fmt": v.get("pix_fmt"),
                  "largura": v.get("width"), "altura": v.get("height"),
                  "fps": round(float(num) / float(den or 1), 3), "quadros": int(v.get("nb_frames", 0) or 0),
                  "cor": v.get("color_space")},
        "audio": None if a is None else {"codec": a.get("codec_name"), "canais": a.get("channels"),
                                         "taxa": int(a.get("sample_rate", 0)),
                                         "bitrate_kbps": round(int(a.get("bit_rate", 0) or 0) / 1000)},
    }
    info["codecs"] = f"{info['video']['codec']} ({info['video']['perfil']}, {info['video']['pix_fmt']})" + (
        f" + {info['audio']['codec']} {info['audio']['bitrate_kbps']}k" if a else " + SEM ÁUDIO")
    return info


def _extrair_quadro(mp4, t):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", mp4, "-frames:v", "1",
                        "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True, check=True)
    return Image.open(io.BytesIO(r.stdout)).convert("RGB")


def _montar_prancha(quadros, tempos, saida, colunas=4, largura=270, zonas=True, cabecalho=""):
    alt = int(largura * H / W)
    linhas = int(math.ceil(len(quadros) / colunas))
    m, topo, rot = 12, 64, 34
    Wp = colunas * largura + (colunas + 1) * m
    Hp = topo + linhas * (alt + rot + m) + m
    pr = Image.new("RGB", (Wp, Hp), (24, 25, 30))
    d = ImageDraw.Draw(pr)
    tf = 24
    while tf > 12 and fonte("bold", tf).getlength(cabecalho) > Wp - 2 * m:
        tf -= 1
    d.text((m, 18), cabecalho, font=fonte("bold", tf), fill=(235, 235, 240))
    for i, (q, t) in enumerate(zip(quadros, tempos)):
        th = q.resize((largura, alt), Image.LANCZOS)
        if zonas:
            th = desenhar_zonas(th, cor=(255, 40, 40, 55), contorno=(255, 220, 0, 170))
        c, l = i % colunas, i // colunas
        x = m + c * (largura + m)
        y = topo + l * (alt + rot + m)
        pr.paste(th, (x, y))
        d.text((x + 4, y + alt + 4), f"{i + 1:02d}  ·  t = {t:.2f} s", font=fonte("semi", 22), fill=(200, 205, 215))
    pr.save(saida)
    return saida


def prancha(mp4, saida=None, n=12, colunas=4, largura=270, zonas=True):
    """Prancha de prévia: N quadros do mp4 lado a lado, com a hora de cada um.
    zonas=True pinta de vermelho as faixas da interface do TikTok (para revisão)."""
    info = info_video(mp4)
    dur = info["duracao_s"]
    saida = saida or os.path.splitext(mp4)[0] + "_prancha.png"
    tempos = [dur * (i + 0.5) / n for i in range(n)]
    quadros = [_extrair_quadro(mp4, t) for t in tempos]
    cab = (f"{os.path.basename(mp4)}  ·  {dur:.2f} s  ·  {info['tamanho_mb']} MB  ·  {info['codecs']}"
           + ("  ·  vermelho = interface" if zonas else ""))
    return _montar_prancha(quadros, tempos, saida, colunas, largura, zonas, cab)


# ============================================================================
# Linha do tempo: a classe Video
# ============================================================================
class _Camada:
    __slots__ = ("inicio", "fim", "z", "ordem", "func")

    def __init__(self, inicio, fim, z, ordem, func):
        self.inicio, self.fim, self.z, self.ordem, self.func = inicio, fim, z, ordem, func


def _anim_es(tl, total, entrada, saida, de, ds):
    """Entrada e saída prontas. Devolve (dx, dy, escala, opacidade, rotação)."""
    dx = dy = rot = 0.0
    s = op = 1.0
    if entrada and entrada != "digitar" and tl < de:
        p = limitar(tl / de)
        if entrada == "pop":
            s *= 0.25 + 0.75 * ease_out_back(p, 2.2); op *= limitar(p * 4)
        elif entrada == "fade":
            op *= ease_out_quad(p)
        elif entrada == "zoom":
            s *= 1.6 - 0.6 * ease_out_cubic(p); op *= ease_out_quad(p)
        elif entrada == "deslizar_baixo":
            dy += 260 * (1 - ease_out_cubic(p)); op *= limitar(p * 2.5)
        elif entrada == "deslizar_cima":
            dy -= 260 * (1 - ease_out_cubic(p)); op *= limitar(p * 2.5)
        elif entrada == "deslizar_esq":
            dx -= W * (1 - ease_out_cubic(p))
        elif entrada == "deslizar_dir":
            dx += W * (1 - ease_out_cubic(p))
        elif entrada == "girar":
            rot += -200 * (1 - ease_out_back(p)); s *= max(0.01, ease_out_back(p)); op *= limitar(p * 3)
        elif entrada == "cair":
            dy -= 700 * (1 - ease_out_bounce(p)); op *= limitar(p * 5)
    if saida and total is not None and tl > total - ds:
        q = limitar((total - tl) / ds)   # 1 -> 0
        if saida == "pop":
            s *= 0.2 + 0.8 * ease_out_cubic(q); op *= limitar(q * 3)
        elif saida == "fade":
            op *= q
        elif saida == "zoom":
            s *= 1 + 0.5 * (1 - q); op *= q
        elif saida == "deslizar_baixo":
            dy += 300 * ease_in_cubic(1 - q); op *= q
        elif saida == "deslizar_cima":
            dy -= 300 * ease_in_cubic(1 - q); op *= q
        elif saida == "deslizar_esq":
            dx -= W * ease_in_cubic(1 - q)
        elif saida == "deslizar_dir":
            dx += W * ease_in_cubic(1 - q)
    return dx, dy, s, op, rot


def _ocioso(tl, ocioso):
    """Movimento parado: 'flutuar', 'pulsar' ou 'balancar'. Devolve (dy, escala, rotação)."""
    if ocioso == "flutuar":
        return 9 * math.sin(2 * math.pi * tl / 2.6), 1.0, 0.0
    if ocioso == "pulsar":
        return 0.0, 1 + 0.025 * math.sin(2 * math.pi * tl / 1.1), 0.0
    if ocioso == "balancar":
        return 0.0, 1.0, 2.5 * math.sin(2 * math.pi * tl / 2.2)
    return 0.0, 1.0, 0.0


class Video:
    """Linha do tempo de um vídeo 1080x1920 a 30 fps.

    v = Video(10)                          # 10 segundos
    v.fundo(DegradeAnimado([...]))         # fundo
    v.texto('Oi *você*', 0, 3, centro=(540, 400))
    v.imagem('titulo.png', 0, 2, escala=1.6)
    v.roleta(cartas, 4, inicio=2, duracao=4)
    v.renderizar('saida.mp4')
    """

    def __init__(self, duracao, fundo="#22252C", fps=FPS, semente=SEMENTE):
        self.duracao = float(duracao)
        self.fps = int(fps)
        self.semente = int(semente)
        self.camadas = []
        self.pos = []                   # efeitos no quadro inteiro (tremida)
        self.eventos = []               # (t, array, volume, pan)
        self.trilha_cfg = None
        self._n = 0
        self._rng_n = 0
        self._zonas = {}
        self._registrando = False
        self.fundo(fundo)

    # ---------------------------------------------------------------- básico
    def _rng(self):
        self._rng_n += 1
        return random.Random(self.semente * 7919 + self._rng_n)

    def fundo(self, f):
        """Cor, Image, ou objeto com .quadro(t) (DegradeAnimado, Padrao) ou função t -> Image."""
        if isinstance(f, (str, tuple)):
            self._fundo = fundo_cor(f)
        elif isinstance(f, Image.Image):
            self._fundo = cobrir(f)
        else:
            self._fundo = f
        return self

    def adicionar(self, func, inicio=0.0, fim=None, z=0):
        """Camada própria: func(canvas, t_local, t). Desenha no canvas (Image RGB 1080x1920)."""
        self._n += 1
        self.camadas.append(_Camada(float(inicio), None if fim is None else float(fim), z, self._n, func))
        return self

    def som(self, som, t, volume=1.0, pan=0.0, **params):
        """Toca um som em t segundos. som: nome ('tique', 'plim', 'vush', 'pop', 'bip', 'tecla', 'toque')
        ou um array numpy (mono ou (n,2)) a 44,1 kHz."""
        if isinstance(som, str):
            arr = SONS[som](**params)
        else:
            arr = np.asarray(som, dtype=np.float32)
        self.eventos.append((float(t), arr, float(volume), float(pan)))
        return self

    def trilha(self, volume=0.3, bpm=112, progressao=None, ducking=0.45):
        """Liga o fundo rítmico original (volume 0..1 em relação aos efeitos)."""
        self.trilha_cfg = dict(volume=volume, bpm=bpm, progressao=progressao, ducking=ducking)
        return self

    def _registrar(self, nome, caixa, t):
        if not self._registrando or not nome or caixa is None:
            return
        probs = checar_zona_segura(caixa)
        r = self._zonas.setdefault(nome, {"quadros_fora": 0, "pior": "", "pior_px": 0, "t": None})
        if probs:
            r["quadros_fora"] += 1
            px = max(int(p.split()[1]) for p in probs)
            if px > r["pior_px"]:
                r["pior_px"], r["pior"], r["t"] = px, "; ".join(probs), round(t, 2)

    def relatorio_zonas(self, tolerancia_s=0.4):
        """Elementos que ficaram fora da zona segura por mais de 'tolerancia_s' segundos."""
        out = []
        for nome, r in self._zonas.items():
            if r["quadros_fora"] > tolerancia_s * self.fps:
                out.append(f"'{nome}': {r['pior']} (pior em t={r['t']} s; {r['quadros_fora']} quadros fora)")
        return out

    # ---------------------------------------------------------------- imagem e texto
    def imagem(self, img, inicio=0.0, fim=None, centro=(540, 900), escala=1.0, rotacao=0.0, opacidade=1.0,
               entrada="pop", saida=None, dur_entrada=0.35, dur_saida=0.28, ocioso=None, som=True,
               ancora="centro", z=10, nome=None):
        """Coloca um PNG. centro/escala/rotacao/opacidade aceitam número ou função do tempo local."""
        im = carregar(img)
        total = None if fim is None else fim - inicio
        if som and entrada == "pop":
            self.som("pop", inicio + 0.02, 0.6)
        elif som and entrada and entrada.startswith("deslizar"):
            self.som("vush", inicio, 0.5)

        def f(canvas, tl, t):
            dx, dy, s, op, rot = _anim_es(tl, total, entrada, saida, dur_entrada, dur_saida)
            ody, os_, orot = _ocioso(tl, ocioso)
            cx, cy = _v(centro, tl)
            colar(canvas, im, (cx + dx, cy + dy + ody), _v(escala, tl) * s * os_, _v(rotacao, tl) + rot + orot,
                  _v(opacidade, tl) * op, ancora)
            if nome and self._registrando and op > 0.5:
                self._registrar(nome, caixa_nominal(im, (cx, cy), _v(escala, tl), _v(rotacao, tl), ancora), t)
        return self.adicionar(f, inicio, fim, z)

    def texto(self, texto, inicio=0.0, fim=None, centro=(540, 400), tamanho=72, fonte="titulo", cor="#FFFFFF",
              cor_destaque="#FFD43B", contorno=10, cor_contorno="#1B1D24", sombra=(0, 8, 12, 150),
              largura_max=800, alinhamento="centro", entrelinha=1.08, max_linhas=None, caixa=None,
              entrada="pop", saida="fade", dur_entrada=0.35, dur_saida=0.25, ocioso=None, cps=24,
              som=True, escala=1.0, rotacao=0.0, opacidade=1.0, ancora="centro", z=20, nome=None):
        """Texto animado. entrada: 'pop', 'fade', 'zoom', 'deslizar_baixo|cima|esq|dir', 'girar', 'cair',
        'digitar' (letra por letra, cps letras/s) ou None. saida: 'fade', 'pop', 'zoom', 'deslizar_*' ou None.
        nome: se der um nome, o texto entra na checagem de zona segura."""
        if sombra is True:
            sombra = (0, 8, 12, 150)
        elif not sombra:
            sombra = None
        args = (texto, int(tamanho), fonte, cor, cor_destaque, contorno, cor_contorno, tuple(sombra) if sombra else None, largura_max,
                alinhamento, entrelinha, max_linhas, True, caixa)
        total = None if fim is None else fim - inicio
        n_letras = contar_letras(texto)
        if som and entrada == "pop":
            self.som("pop", inicio + 0.02, 0.55)
        elif som and entrada and entrada.startswith("deslizar"):
            self.som("vush", inicio, 0.5)
        elif som and entrada == "digitar":
            letras = [cl for cl, em, d in _parse(texto) if cl != "\n"]
            for i, cl in enumerate(letras):
                if not cl.isspace():
                    self.som("tecla", inicio + i / cps, 0.22, 0.0, semente=i % 4)
        cheio = texto_img(*args)

        def f(canvas, tl, t):
            if entrada == "digitar":
                k = int(tl * cps) + 1
                img = cheio if k >= n_letras else texto_img(*args, visiveis=k)
            else:
                img = cheio
            dx, dy, s, op, rot = _anim_es(tl, total, entrada, saida, dur_entrada, dur_saida)
            ody, os_, orot = _ocioso(tl, ocioso)
            cx, cy = _v(centro, tl)
            esc = _v(escala, tl) * s * os_
            r = _v(rotacao, tl) + rot + orot
            colar(canvas, img, (cx + dx, cy + dy + ody), esc, r, _v(opacidade, tl) * op, ancora)
            if nome and self._registrando and op > 0.5:
                self._registrar(nome, caixa_nominal(cheio, (cx, cy), _v(escala, tl), _v(rotacao, tl), ancora,
                                                    cheio.info.get("caixa")), t)
        return self.adicionar(f, inicio, fim, z)

    # ---------------------------------------------------------------- animações prontas
    def revelar(self, img, inicio, centro=(540, 900), escala=1.0, fim=None, brilho=True, luz=True, som=True, z=12, nome=None):
        """Aparece com 'pop' (escala com mola), luz atrás e brilhos em volta."""
        im = carregar(img)
        if luz:
            self.luz(inicio, centro, fim=fim, raio=int(max(im.width, im.height) * escala * 0.75))
        if som:
            self.som("pop", inicio, 0.7)
            self.som("plim", inicio + 0.05, 0.45)
        if brilho:
            self.brilhos(inicio + 0.05, centro, raio=(im.width * escala * 0.6, im.height * escala * 0.75))

        def f(canvas, tl, t):
            p = limitar(tl / 0.18)
            s = escala * (0.3 + 0.7 * ease_out_quad(p)) if tl < 0.18 else escala * (1 + quique(tl - 0.18, 0.12, 2.2, 5.5))
            colar(canvas, im, centro, s, 0, limitar(tl / 0.08))
            if nome and self._registrando:
                self._registrar(nome, caixa_nominal(im, centro, escala), t)
        return self.adicionar(f, inicio, fim, z)

    def roleta(self, imagens, resultado, inicio, duracao=4.0, centro=(540, 900), escala=1.65, fim=None,
               intervalo_ini=0.06, intervalo_fim=0.46, curva=2.0, som=True, volume_tique=0.5, festa=True,
               raios=True, z=12, nome="roleta"):
        """Cartas trocando rápido e desacelerando até cair no 'resultado' (índice na lista ou imagem),
        com quique, 'plim', confete, brilhos e raios. As cartas nunca repetem em seguida.
        Devolve o tempo (s) em que o resultado aparece."""
        imgs = [carregar(i) for i in imagens]
        if isinstance(resultado, int):
            ri, res = resultado, imgs[resultado]
        else:
            res = carregar(resultado)
            ri = next((i for i, im in enumerate(imgs) if im is res), None)
        rng = self._rng()
        N = 2
        while True:
            k = np.arange(N)
            frac = (k / (N - 1)) ** curva
            d = intervalo_ini * (intervalo_fim / intervalo_ini) ** frac
            if d.sum() >= duracao or N > 800:
                break
            N += 1
        d = d * (duracao / d.sum())
        inicios = list(np.concatenate([[0.0], np.cumsum(d)[:-1]]))
        pool = [i for i in range(len(imgs)) if i != ri] or [0]
        ordem, ultimo = [], None
        while len(ordem) < N:
            emb = pool[:]
            rng.shuffle(emb)
            for i in emb:
                if i != ultimo or len(pool) == 1:
                    ordem.append(i); ultimo = i
                if len(ordem) == N:
                    break
        t_res = inicio + duracao
        if som:
            for kk in range(N):
                self.som("tique", inicio + inicios[kk], volume_tique * (0.8 + 0.35 * kk / N), 0.0,
                         freq=int(2500 - 700 * kk / N), semente=kk % 5)
            self.som("plim", t_res, 0.8)
            self.som("pop", t_res, 0.5)
        if festa:
            ink_w = res.width * escala
            self.luz(t_res, centro, fim=fim, raio=int(ink_w * 0.62), opacidade=0.55)
            self.confete(t_res, origem=(centro[0], centro[1]), quantidade=110)
            self.brilhos(t_res + 0.05, centro, raio=(ink_w * 0.55, res.height * escala * 0.85), quantidade=12)
            self.tremida(t_res, 0.3, 9)
        if raios:
            self.raios(t_res, centro, fim=fim)

        def f(canvas, tl, t):
            if tl < duracao:
                k = max(0, bisect.bisect_right(inicios, tl) - 1)
                u = (tl - inicios[k]) / d[k]
                img = imgs[ordem[k]]
                e = 1 - ease_out_cubic(limitar(u * 2.2))
                s = escala * (1 + 0.05 * e)
                dy = -26 * e
                rot = (1.6 if k % 2 else -1.6) * e
            else:
                tau = tl - duracao
                img, s, dy, rot = res, escala * (1 + quique(tau, 0.16, 2.4, 5.0)), 0.0, 0.0
            colar(canvas, img, (centro[0], centro[1] + dy), s, rot)
            if self._registrando:
                self._registrar(nome, caixa_nominal(img, centro, escala), t)
        self.adicionar(f, inicio, fim, z)
        return t_res

    def ranking(self, itens, inicio, posicoes=None, n_posicoes=None, intervalo=0.8, dur_voo=0.5, area=None,
                fim=None, cor_vaga=(255, 255, 255, 40), cor_borda=(255, 255, 255, 110), cor_numero="#FFD43B",
                cor_numero_texto="#1B1D24", fonte_item="titulo", som=True, z=15, nome="ranking"):
        """Ranking: N vagas numeradas (1..N) e os itens entrando um a um na sua posição.
        itens: textos ou imagens. posicoes[i] = vaga (0 = primeira) do item i. area: (x0,y0,x1,y1)."""
        N = n_posicoes or len(itens)
        posicoes = list(posicoes) if posicoes is not None else list(range(len(itens)))
        x0, y0, x1, y1 = area or zona_segura()
        hrow = (y1 - y0) / N
        hv = hrow * 0.86
        bd = hv * 0.86
        vx0 = x0 + hv * 1.05
        vw = x1 - vx0
        # vagas (pré-desenhadas)
        S = 2
        vagas = Image.new("RGBA", (int((x1 - x0) * S), int((y1 - y0) * S)), (0, 0, 0, 0))
        dv = ImageDraw.Draw(vagas)
        fn = fonte("titulo", int(bd * 0.62 * S))
        for i in range(N):
            yy = (i * hrow + (hrow - hv) / 2) * S
            dv.rounded_rectangle([(vx0 - x0) * S, yy, (x1 - x0) * S - 2, yy + hv * S], radius=hv * 0.28 * S,
                                 fill=rgba(cor_vaga), outline=rgba(cor_borda), width=int(3 * S))
            cx, cy = hv * 0.5 * S, yy + hv * S / 2
            dv.ellipse([cx - bd * S / 2, cy - bd * S / 2, cx + bd * S / 2, cy + bd * S / 2], fill=rgba(cor_numero),
                       outline=rgba(cor_numero_texto), width=int(4 * S))
            dv.text((cx, cy + bd * 0.04 * S), str(i + 1), font=fn, anchor="mm", fill=rgba(cor_numero_texto))
        vagas = vagas.resize((int(x1 - x0), int(y1 - y0)), Image.LANCZOS)
        # sprites dos itens
        sprites = []
        for it in itens:
            if isinstance(it, str) and not _e_arquivo_imagem(it):
                sp = texto_img(it, int(hv * 0.5), fonte_item, "#FFFFFF", "#FFD43B", 7, "#1B1D24", (0, 4, 6, 120),
                               int(vw * 0.94), "centro", 1.0, 2, True, None)
            else:
                sp = carregar(it)
                sp = transformar(sp, ajustar(sp, vw * 0.96, hv * 0.96))
            sprites.append(sp)
        if som:
            for i in range(len(itens)):
                ti = inicio + i * intervalo
                self.som("vush", ti, 0.45)
                self.som("pop", ti + dur_voo * 0.8, 0.6)

        def f(canvas, tl, t):
            op = limitar((tl + 0.35) / 0.35)
            colar(canvas, vagas, ((x0 + x1) / 2, (y0 + y1) / 2), 1.0, 0, op)
            for i, sp in enumerate(sprites):
                ti = i * intervalo
                if tl < ti:
                    continue
                vaga = posicoes[i]
                cy = y0 + vaga * hrow + hrow / 2
                cx_dest = vx0 + vw / 2
                p = limitar((tl - ti) / dur_voo)
                x = lerp(W + sp.width / 2 + 40, cx_dest, ease_out_back(p, 1.2))
                s = 1 + quique(tl - ti - dur_voo, 0.12, 2.6, 7) if p >= 1 else 1.0
                if 0 <= tl - ti - dur_voo < 0.35:   # brilho na vaga quando o item chega
                    a = 1 - (tl - ti - dur_voo) / 0.35
                    fl = Image.new("RGBA", (int(vw), int(hv)), (255, 255, 255, int(90 * a)))
                    canvas.paste(fl, (int(vx0), int(cy - hv / 2)), fl)
                colar(canvas, sp, (x, cy), s)
            self._registrar(nome, (x0, y0, x1, y1), t)
        return self.adicionar(f, inicio - 0.35, fim, z)

    def slides(self, itens, inicio, dur_cada=1.6, transicao="deslizar", dur_trans=0.35, centro=(540, 900),
               escala=1.0, fim=None, som=True, z=10, nome="slides"):
        """Sequência de slides (imagens, caminhos de PNG/JPG ou textos). transicao: 'deslizar', 'zoom',
        'fade' ou 'corte'. O último fica até 'fim' (ou até inicio + len*dur_cada)."""
        sprites = []
        for it in itens:
            texto_puro = isinstance(it, str) and not _e_arquivo_imagem(it)
            sprites.append(texto_img(it, 84) if texto_puro else carregar(it))
        n = len(sprites)
        fim = fim if fim is not None else inicio + n * dur_cada
        if som and transicao != "corte":
            for i in range(1, n):
                self.som("vush", inicio + i * dur_cada - dur_trans * 0.5, 0.5)

        def f(canvas, tl, t):
            i = min(n - 1, int(tl // dur_cada))
            u = tl - i * dur_cada
            if i > 0 and u < dur_trans and transicao != "corte":
                p = ease_in_out_cubic(u / dur_trans)
                a, b = sprites[i - 1], sprites[i]
                if transicao == "deslizar":
                    colar(canvas, a, (centro[0] - p * W, centro[1]), escala)
                    colar(canvas, b, (centro[0] + (1 - p) * W, centro[1]), escala)
                elif transicao == "zoom":
                    colar(canvas, a, centro, escala * (1 + 0.4 * p), 0, 1 - p)
                    colar(canvas, b, centro, escala * (0.7 + 0.3 * p), 0, p)
                else:
                    colar(canvas, a, centro, escala, 0, 1 - p)
                    colar(canvas, b, centro, escala, 0, p)
            else:
                colar(canvas, sprites[i], centro, escala)
                if self._registrando:
                    self._registrar(nome, caixa_nominal(sprites[i], centro, escala), t)
        return self.adicionar(f, inicio, fim, z)

    def contagem(self, inicio, de=3, dur_cada=0.7, centro=(540, 860), tamanho=380, cor="#FFFFFF",
                 cor_contorno="#1B1D24", final="JÁ!", som=True, z=30):
        """Contagem regressiva grande (3, 2, 1, JÁ!) com bipe. Devolve o tempo em que termina."""
        nums = [str(k) for k in range(de, 0, -1)] + ([final] if final else [])
        for i, s in enumerate(nums):
            ti = inicio + i * dur_cada
            img = texto_img(s, tamanho if s != final else int(tamanho * 0.6), "titulo", cor, "#FFD43B", 16,
                            cor_contorno, (0, 12, 16, 160), 900, "centro", 1.0, 1, True, None)
            if som:
                ultimo = final and i == len(nums) - 1
                self.som("bip", ti, 0.6, 0.0, freq=1320.0 if ultimo else 880.0, dur=0.3 if ultimo else 0.16)

            def f(canvas, tl, t, img=img):
                p = limitar(tl / 0.25)
                s = 1.5 - 0.5 * ease_out_back(p, 2.0)
                q = limitar((tl - dur_cada * 0.7) / (dur_cada * 0.3))
                colar(canvas, img, centro, s * (1 + 0.25 * q), 0, limitar(p * 3) * (1 - q))
            self.adicionar(f, ti, ti + dur_cada, z)
        return inicio + len(nums) * dur_cada

    def toque(self, t, centro=(540, 1100), som=True, z=40):
        """Simula um dedo tocando na tela: anel que se espalha + 👆."""
        if som:
            self.som("toque", t + 0.12, 0.7)
        dedo = emoji_img("👆", 120)

        def f(canvas, tl, tt):
            p = limitar(tl / 0.12)
            dy = 40 * (1 - ease_out_cubic(p))
            if tl > 0.12:
                u = limitar((tl - 0.12) / 0.45)
                r = 30 + 110 * ease_out_cubic(u)
                a = int(220 * (1 - u))
                sz = int(2 * r + 16)
                anel = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
                ImageDraw.Draw(anel).ellipse([8, 8, sz - 8, sz - 8], outline=(255, 255, 255, a), width=8)
                _pintar(canvas, anel, centro[0] - sz // 2, centro[1] - sz // 2)
            op = limitar(tl / 0.08) * (1 - limitar((tl - 0.45) / 0.15))
            colar(canvas, dedo, (centro[0] + 18, centro[1] + 62 + dy), 1.0, 0, op)
        return self.adicionar(f, t, t + 0.62, z)

    def confete(self, inicio, origem=(540, 900), quantidade=110, duracao=2.8, cores=None, forca=1.0,
                modo="explosao", z=50):
        """Confete. modo 'explosao' (sai de 'origem' para cima) ou 'chuva' (cai do topo)."""
        rng = self._rng()
        cores = [rgb(c) for c in (cores or CORES_CONFETE)]
        g, k = 1100.0, 3.0
        ps = []
        for _ in range(quantidade):
            if modo == "chuva":
                x0, y0 = rng.uniform(0, W), rng.uniform(-300, -20)
                vx, vy = rng.uniform(-60, 60), rng.uniform(0, 200)
                atraso = rng.uniform(0, duracao * 0.5)
            else:
                ang = math.radians(rng.uniform(-165, -15))
                v = rng.uniform(700, 2000) * forca
                x0, y0 = origem[0] + rng.uniform(-60, 60), origem[1] + rng.uniform(-30, 30)
                vx, vy = v * math.cos(ang), v * math.sin(ang)
                atraso = rng.uniform(0, 0.06)
            ps.append(dict(x0=x0, y0=y0, vx=vx, vy=vy, atraso=atraso, tam=rng.uniform(14, 26),
                           rot0=rng.uniform(0, 360), vrot=rng.uniform(-420, 420), fase=rng.uniform(0, 6.28),
                           vflip=rng.uniform(4, 11), cor=rng.choice(cores), osc=rng.uniform(10, 40)))

        def f(canvas, tl, t):
            d = ImageDraw.Draw(canvas)
            for p in ps:
                tt = tl - p["atraso"]
                if tt < 0:
                    continue
                e = math.exp(-k * tt)
                x = p["x0"] + p["vx"] / k * (1 - e) + p["osc"] * math.sin(2.2 * tt + p["fase"])
                y = p["y0"] + (g / k) * tt + (p["vy"] - g / k) * (1 - e) / k
                if y > H + 40 or x < -40 or x > W + 40:
                    continue
                s = p["tam"] * (1 - limitar((tl - duracao + 0.5) / 0.5))
                if s < 1:
                    continue
                flip = math.cos(p["fase"] + p["vflip"] * tt)
                w2, h2 = s / 2 * max(0.15, abs(flip)), s * 0.3
                a = math.radians(p["rot0"] + p["vrot"] * tt)
                ca, sa = math.cos(a), math.sin(a)
                pts = [(x + px * ca - py * sa, y + px * sa + py * ca) for px, py in ((-w2, -h2), (w2, -h2), (w2, h2), (-w2, h2))]
                c = p["cor"] if flip > 0 else tuple(int(v * 0.72) for v in p["cor"])
                d.polygon(pts, fill=c)
        return self.adicionar(f, inicio, inicio + duracao, z)

    def brilhos(self, inicio, centro=(540, 900), raio=(420, 260), quantidade=14, duracao=1.6, cor="#FFFFFF",
                tamanho=(26, 64), z=55):
        """Brilhos (estrelinhas de 4 pontas) piscando em volta de 'centro', numa elipse de raios 'raio'."""
        rng = self._rng()
        sp = sprite_brilho(cor, 160)
        bs = []
        for i in range(quantidade):
            ang = rng.uniform(0, 2 * math.pi)
            rr = rng.uniform(0.75, 1.1)
            bs.append((centro[0] + math.cos(ang) * raio[0] * rr, centro[1] + math.sin(ang) * raio[1] * rr,
                       rng.uniform(0, duracao * 0.55), rng.uniform(0.45, 0.8), rng.uniform(*tamanho) / 160,
                       rng.uniform(-30, 30)))

        def f(canvas, tl, t):
            for x, y, nasce, vida, esc, rot in bs:
                u = (tl - nasce) / vida
                if 0 <= u <= 1:
                    s = esc * math.sin(math.pi * u)
                    colar(canvas, sp, (x, y), s, rot + 40 * u)
        return self.adicionar(f, inicio, inicio + duracao, z)

    def luz(self, inicio, centro=(540, 900), fim=None, raio=420, cor="#FFFFFF", opacidade=0.5, z=5):
        """Luz redonda atrás de algo: acende forte e fica suave."""
        sp = sprite_luz(int(raio), cor)

        def f(canvas, tl, t):
            op = opacidade * (0.55 + 0.45 * math.exp(-tl * 4)) * limitar(tl / 0.08)
            colar(canvas, sp, centro, 1.0, 0, op)
        return self.adicionar(f, inicio, fim, z)

    def raios(self, inicio, centro=(540, 900), fim=None, n=14, cor="#FFFFFF", opacidade=0.16, velocidade=14,
              raio=1100, z=4):
        """Raios de sol girando devagar atrás do resultado."""
        q = 4
        w, h = W // q, H // q
        ys, xs = np.mgrid[0:h, 0:w]
        dx, dy = xs * q - centro[0], ys * q - centro[1]
        theta = np.arctan2(dy, dx)
        r = np.sqrt(dx ** 2 + dy ** 2)
        queda = np.clip(1 - r / raio, 0, 1) ** 1.2 * np.clip(r / 160, 0, 1)
        cor_img = Image.new("RGB", (W, H), rgb(cor))

        def f(canvas, tl, t):
            rot = math.radians(velocidade * tl)
            v = 0.5 + 0.5 * np.cos(n * (theta - rot))
            v = np.clip((v - 0.45) * 4, 0, 1)
            a = v * queda * 255 * opacidade * limitar(tl / 0.4)
            m = Image.fromarray(a.astype(np.uint8), "L").resize((W, H), Image.BILINEAR)
            canvas.paste(cor_img, (0, 0), m)
        return self.adicionar(f, inicio, fim, z)

    def tremida(self, inicio, duracao=0.35, intensidade=12, frequencia=24):
        """Tremida na tela inteira (some aos poucos)."""
        rng = self._rng()
        f1, f2 = rng.uniform(0, 6.28), rng.uniform(0, 6.28)

        def efeito(img, tl):
            a = intensidade * (1 - tl / duracao) ** 2
            dx = a * math.sin(2 * math.pi * frequencia * tl + f1)
            dy = a * math.sin(2 * math.pi * frequencia * 1.31 * tl + f2)
            zz = 1 + (2 * a + 4) / W * 2
            cx, cy = W / 2, H / 2
            return img.transform(img.size, Image.AFFINE,
                                 (1 / zz, 0, cx - (cx + dx) / zz, 0, 1 / zz, cy - (cy + dy) / zz), resample=Image.BILINEAR)
        self.pos.append((float(inicio), float(inicio + duracao), efeito))
        return self

    # ---------------------------------------------------------------- render
    def quadro(self, t):
        """Desenha o quadro do tempo t (s). Devolve Image RGB 1080x1920."""
        f = self._fundo
        if isinstance(f, Image.Image):
            canvas = f.copy()
        elif hasattr(f, "quadro"):
            canvas = f.quadro(t)
        else:
            canvas = f(t)
        if canvas.mode != "RGB":
            canvas = canvas.convert("RGB")
        for c in sorted(self.camadas, key=lambda c: (c.z, c.ordem)):
            if t >= c.inicio and (c.fim is None or t < c.fim):
                c.func(canvas, t - c.inicio, t)
        for ini, fim, ef in self.pos:
            if ini <= t < fim:
                canvas = ef(canvas, t - ini)
        return canvas

    def audio(self):
        """Mixa tudo e devolve array (n, 2) float32 já masterizado."""
        trilha = None
        vol = 0.0
        duck = 0.45
        if self.trilha_cfg:
            c = self.trilha_cfg
            trilha = trilha_ritmica(self.duracao, c["bpm"], self.semente, c["progressao"])
            vol, duck = c["volume"], c["ducking"]
        return mixar(self.duracao, self.eventos, trilha, vol, duck)

    def renderizar(self, saida, crf=21, preset="medium", maxrate="2600k", bufsize="5200k", limite_mb_10s=4.0,
                   wav=None, mostrar=True):
        """Gera o mp4 (H.264 high, yuv420p, 30 fps, AAC 128k, faststart). Devolve dict com info e tempo.
        Se passar de 'limite_mb_10s' MB por 10 s, recodifica com bitrate menor (2 passadas)."""
        t0 = time.time()
        os.makedirs(os.path.dirname(os.path.abspath(saida)) or ".", exist_ok=True)
        n = int(round(self.duracao * self.fps))
        tmp = tempfile.mkdtemp(prefix="render_")
        wav_path = wav or os.path.join(tmp, "audio.wav")
        salvar_wav(wav_path, self.audio())
        cmd = ["ffmpeg", "-y", "-v", "error",
               "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(self.fps), "-i", "-",
               "-i", wav_path, "-map", "0:v", "-map", "1:a",
               "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
               "-c:v", "libx264", "-preset", preset, "-crf", str(crf), "-maxrate", maxrate, "-bufsize", bufsize,
               "-profile:v", "high", "-level:v", "4.1", "-pix_fmt", "yuv420p", "-g", str(self.fps * 2),
               "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
               "-c:a", "aac", "-b:a", "128k", "-ar", str(SR), "-ac", "2",
               "-t", f"{self.duracao:.3f}", "-movflags", "+faststart",
               "-fflags", "+bitexact", "-flags:v", "+bitexact", "-flags:a", "+bitexact", "-map_metadata", "-1",
               saida]
        self._zonas = {}
        self._registrando = True
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        try:
            for i in range(n):
                q = self.quadro(i / self.fps)
                p.stdin.write(q.tobytes())
                if mostrar and (i % (self.fps * 2) == 0):
                    print(f"  quadro {i}/{n}  ({time.time() - t0:.1f} s)", file=sys.stderr)
        finally:
            self._registrando = False
            p.stdin.close()
            p.wait()
        if p.returncode != 0:
            raise RuntimeError("ffmpeg falhou")
        limite = limite_mb_10s * 1024 * 1024 * self.duracao / 10.0
        recod = False
        if os.path.getsize(saida) > limite:
            self._recodificar(saida, limite, tmp)
            recod = True
        shutil.rmtree(tmp, ignore_errors=True)
        info = info_video(saida)
        info["tempo_render_s"] = round(time.time() - t0, 1)
        info["recodificado"] = recod
        info["avisos_zona"] = self.relatorio_zonas()
        if mostrar:
            print(f"OK {saida}: {info['duracao_s']} s, {info['tamanho_mb']} MB, {info['codecs']}, "
                  f"render {info['tempo_render_s']} s", file=sys.stderr)
            for a in info["avisos_zona"]:
                print("  AVISO zona segura:", a, file=sys.stderr)
        return info

    def _recodificar(self, saida, limite_bytes, tmp):
        kbps = int(limite_bytes * 8 / self.duracao / 1000 * 0.93) - 128
        orig = os.path.join(tmp, "orig.mp4")
        shutil.move(saida, orig)
        base = ["ffmpeg", "-y", "-v", "error", "-i", orig, "-c:v", "libx264", "-preset", "medium",
                "-b:v", f"{kbps}k", "-profile:v", "high", "-pix_fmt", "yuv420p", "-passlogfile", os.path.join(tmp, "p")]
        subprocess.run(base + ["-pass", "1", "-an", "-f", "mp4", os.devnull], check=True)
        subprocess.run(base + ["-pass", "2", "-c:a", "copy", "-colorspace", "bt709", "-color_primaries", "bt709",
                               "-color_trc", "bt709", "-movflags", "+faststart", "-fflags", "+bitexact",
                               "-map_metadata", "-1", saida], check=True)

    def prancha(self, saida, n=12, colunas=4, largura=270, zonas=True):
        """Prancha direto da linha do tempo (sem gerar mp4). Bom para conferir antes do render."""
        tempos = [self.duracao * (i + 0.5) / n for i in range(n)]
        quadros = [self.quadro(t) for t in tempos]
        return _montar_prancha(quadros, tempos, saida, colunas, largura, zonas, f"prévia · {self.duracao:.1f} s")

    def exportar_slides(self, tempos, pasta, prefixo="slide", max_kb=500):
        """Salva os quadros dos tempos dados como JPG 1080x1920 (até max_kb cada), para carrossel de fotos."""
        os.makedirs(pasta, exist_ok=True)
        out = []
        for i, t in enumerate(tempos, 1):
            caminho = os.path.join(pasta, f"{prefixo}_{i:02d}.jpg")
            q, kb = salvar_jpg(self.quadro(t), caminho, max_kb)
            out.append((caminho, q, round(kb, 1)))
        return out


# ============================================================================
# Demo (C02 "Meu próximo carro")
# ============================================================================
def demo(saida, pasta_assets=None, resultado=5, trilha=True, semente=SEMENTE):
    """Demo de 10 s: título, toque, roleta caindo numa carta e texto de chamada."""
    pasta = pasta_assets or os.path.normpath(os.path.join(AQUI, "..", "..", "efeito-4-meu-proximo-carro", "assets"))
    titulo = os.path.join(pasta, "titulo_toque.png")
    cartas = sorted(glob.glob(os.path.join(pasta, "cartas", "carta_*.png")))
    if not cartas or not os.path.exists(titulo):
        raise SystemExit(f"Não achei titulo_toque.png e cartas/carta_*.png em {pasta}")
    v = Video(10.0, semente=semente)
    v.fundo(Padrao("tracejado", cor_forma=(255, 212, 59, 34), tamanho=200, velocidade=(0, 150),
                   fundo=DegradeAnimado(["#1A1D24", "#2B303B", "#0F4A52", "#2B303B"], angulo=105, velocidade=0.05)))
    if trilha:
        v.trilha(volume=0.26, ducking=0.55)
    cx, cy, esc = 540, 870, 1.6     # carta visível = 500 px de largura -> 800 px, cabe na zona segura
    v.texto("Qual vai ser o teu *próximo carro*? 🤔", 0.0, 6.0, centro=(540, 375), tamanho=86,
            entrada=None, saida="pop", ocioso="pulsar", nome="gancho")
    v.imagem(titulo, 0.0, 1.9, centro=(cx, cy), escala=esc, entrada="pop", dur_entrada=0.4, ocioso="flutuar",
             nome="título")
    v.toque(1.25, centro=(cx, cy + 250))
    v.som("vush", 1.75, 0.45)
    t_res = v.roleta(cartas, resultado - 1, inicio=1.9, duracao=4.1, centro=(cx, cy), escala=esc, nome="roleta")
    v.texto("Saiu *esse aqui* 😂", t_res + 0.15, None, centro=(540, 375), tamanho=92, entrada="pop",
            saida=None, nome="resultado")
    v.texto("Procure na lupa 🔎", t_res + 0.7, None, centro=(540, 1205), tamanho=60, fonte="black",
            entrada="deslizar_baixo", saida=None, z=60, nome="chamada 1")
    v.texto("*Meu próximo carro*", t_res + 0.85, None, centro=(540, 1315), tamanho=88, max_linhas=1,
            entrada="deslizar_baixo", saida=None, ocioso="pulsar", som=False, z=60, nome="chamada 2")
    return v


def main(argv=None):
    ap = argparse.ArgumentParser(description="Render de vídeos 9:16 do TikTok (1080x1920, 30 fps).")
    ap.add_argument("--demo", metavar="SAIDA.mp4", help="gera a demo do C02 'Meu próximo carro'")
    ap.add_argument("--assets", help="pasta de assets (padrão: efeito-4-meu-proximo-carro/assets)")
    ap.add_argument("--resultado", type=int, default=5, help="número da carta sorteada na demo (1..26)")
    ap.add_argument("--sem-trilha", action="store_true", help="sem o fundo rítmico")
    ap.add_argument("--semente", type=int, default=SEMENTE)
    ap.add_argument("--slides", metavar="PASTA", help="na demo, exporta 3 slides JPG nesta pasta")
    ap.add_argument("--sem-prancha", action="store_true", help="na demo, não gera a prancha de quadros")
    ap.add_argument("--info", metavar="MP4", help="mostra duração, tamanho e codecs de um mp4")
    ap.add_argument("--prancha", metavar="MP4", help="gera a prancha de quadros de um mp4")
    ap.add_argument("-o", "--saida", help="arquivo de saída da prancha")
    ap.add_argument("-n", type=int, default=12, help="quantos quadros na prancha")
    a = ap.parse_args(argv)
    if a.info:
        print(json.dumps(info_video(a.info), ensure_ascii=False, indent=2))
    elif a.prancha:
        print(prancha(a.prancha, a.saida, a.n))
    elif a.demo:
        v = demo(a.demo, a.assets, a.resultado, not a.sem_trilha, a.semente)
        info = v.renderizar(a.demo)
        if not a.sem_prancha:
            info["prancha"] = prancha(a.demo, None, a.n)
        if a.slides:
            info["slides"] = v.exportar_slides([1.0, 6.9, 9.5], a.slides)
        print(json.dumps(info, ensure_ascii=False, indent=2))
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
