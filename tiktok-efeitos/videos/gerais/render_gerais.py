#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_gerais.py: as 2 peças gerais do plano de vídeos (PLANO-DE-VIDEOS.md, "Peças gerais").

    G-V1 · "Como achar nossos filtros" · 10 s  (tutorial: lupa → digita o nome → 3º passo → nomes aprovados)
    G-V2 · "3 filtros pro fim de ano"  · 10 s  (C06, C05 e C07: título + 1 carta de cada)

Usa a biblioteca da equipe (videos/lib/render.py; só importa, não altera nada nela) e as artes dos efeitos
(efeito-*/assets; só lê). Tudo é determinístico: o x264 roda em 1 thread (ver render_det), então rodar de novo
gera os mesmos bytes.

Rodar (de qualquer pasta):
    python3 render_gerais.py --aba ambas                  # tudo: G-V1, G-V1-aba, G-V2, capas, legendas, prévia
    python3 render_gerais.py                              # G-V1 (sem a aba, padrão) + G-V2 + capas + prévia
    python3 render_gerais.py --so G-V1 --aba sim          # só G-V1-aba.mp4 (3º passo = "aba de efeitos")
    python3 render_gerais.py --so G-V1 --nomes "Eu no grupo da família" "Torcedômetro"
    python3 render_gerais.py --so G-V2 --nomes-v2 "Meu amigo secreto" "Simpatia da Virada"
    python3 render_gerais.py --so previa                  # só a prancha previa-videos.png (dos MP4 que existem)
    python3 render_gerais.py --rapido DIR                 # pranchas rápidas da linha do tempo (sem MP4), em DIR

Parâmetros:
    --nomes   nomes dos filtros JÁ APROVADOS, na ordem em que aparecem no fim do G-V1 (8–10 s). O 1º também é
              o nome digitado no passo 2. Padrão: "Eu no grupo da família" "Torcedômetro" "Meu próximo carro".
    --aba     nao  → 3º passo "Ou toca no nome do filtro no vídeo de quem usou ✨" (G-V1.mp4, padrão)
              sim  → 3º passo "Ou entra no meu perfil, na aba de efeitos ✨"        (G-V1-aba.mp4)
              ambas → as duas versões.
    --nomes-v2 os filtros de fim de ano aprovados (padrão: os 3). Tira o que não foi aprovado; o gancho, a capa
              e a legenda mudam sozinhos ("2 filtros pro fim de ano").
Os nomes valem como foram publicados (se sair sem acento, passe sem acento). O ícone e a arte de cada efeito
são achados pelo nome, mesmo com outra grafia (ex.: "Torcedometro").

Saída (nesta pasta): G-V1.mp4, G-V1-aba.mp4, G-V2.mp4, G-V1-capa.jpg, G-V2-capa.jpg, G-V1-legenda.txt,
G-V1-aba-legenda.txt, G-V2-legenda.txt, previa-videos.png.
"""
from __future__ import annotations

import argparse
import functools
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata

sys.dont_write_bytecode = True        # não deixa __pycache__ na pasta da biblioteca

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, "..", ".."))          # tiktok-efeitos/
LIB = os.path.join(RAIZ, "videos", "lib")
sys.path.insert(0, LIB)
import render as r  # noqa: E402

import numpy as np  # noqa: E402
from PIL import Image, ImageDraw, ImageFilter  # noqa: E402

SR = r.SR
CX = 540
SIMBOLO = os.path.join(RAIZ, "videos", "perfil", "simbolo_transparente.png")

# Cores do perfil (PERFIL.md, seção 5): roxo, rosa, laranja, turquesa, amarelo, contorno grafite.
ROXO, ROSA, LARANJA, TURQUESA, AMARELO, CONTORNO = "#5B2EFF", "#E23CD8", "#FF9A3C", "#1FC8C0", "#FFD43B", "#22252C"
ESCURO = "#1B1D24"
BRANCO = "#FFFFFF"

# ============================================================================
# Os efeitos: pasta, ícone, nome padrão e pedaços do nome que identificam o efeito (sem acento, minúsculo)
# ============================================================================
EFEITOS = {
    "C08": dict(pasta="efeito-2-seu-papel-no-grupo", icone="icone_grande_512.png", nome="Eu no grupo da família",
                chaves=("grupodafamilia", "familia")),
    "C01": dict(pasta="efeito-1-torcedometro", icone="icone_512.png", nome="Torcedômetro", chaves=("torced",)),
    "C02": dict(pasta="efeito-4-meu-proximo-carro", icone="icone_512.png", nome="Meu próximo carro",
                chaves=("proximocarro",)),
    "C09": dict(pasta="efeito-5-perrengue-no-volante", icone="icone_512.png", nome="Perrengue no volante",
                chaves=("perrengue",)),
    "C06": dict(pasta="efeito-6-meu-amigo-secreto", icone="icone_512.png", nome="Meu amigo secreto",
                chaves=("amigosecreto", "amigooculto")),
    "C05": dict(pasta="efeito-3-meu-2027-vai-ser", icone="icone_grande_512.png", nome="Meu 2027 vai ser",
                chaves=("2027",)),
    "C07": dict(pasta="efeito-7-simpatia-da-virada", icone="icone_512.png", nome="Simpatia da Virada",
                chaves=("simpatia",)),
}
NOMES_V1 = ["Eu no grupo da família", "Torcedômetro", "Meu próximo carro"]
NOMES_V2 = ["Meu amigo secreto", "Meu 2027 vai ser", "Simpatia da Virada"]
ORDEM_V2 = ["C06", "C05", "C07"]


def _norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]", "", s)


def efeito_do_nome(nome):
    n = _norm(nome)
    for cod, e in EFEITOS.items():
        if any(k in n for k in e["chaves"]):
            return cod
    return None


def asset(cod, *partes):
    return os.path.join(RAIZ, EFEITOS[cod]["pasta"], "assets", *partes)


def juntar(nomes):
    """['A', 'B', 'C'] -> 'A, B e C'."""
    if len(nomes) == 1:
        return nomes[0]
    return ", ".join(nomes[:-1]) + " e " + nomes[-1]


# ============================================================================
# Desenhos nossos (lupa, teclado, vídeo, avatar). Nada imita tela, ícone ou logo do TikTok.
# ============================================================================
S = 3                     # superamostragem dos desenhos
_ARTE = {}                # mantém vivas as imagens criadas aqui (a biblioteca faz cache por id)


def _guardar(chave, img):
    _ARTE[chave] = img
    return img


def _reduzir(im, tam):
    return im.resize(tam, Image.LANCZOS)


def _estrela(d, cx, cy, raio, cor, contorno=None, ol=0.0, fino=0.30):
    if contorno:
        r._estrela4(d, cx, cy, raio + ol * 1.6, r.rgba(contorno), fino=fino + 0.04)
    r._estrela4(d, cx, cy, raio, r.rgba(cor), fino=fino)


def lupa(tam=480, estrela=True):
    """Lupa nossa: aro branco com contorno grafite (estilo figurinha), lente turquesa clara com reflexo, cabo amarelo
    e uma estrelinha amarela dentro (o 'filtro'). Desenho simples e genérico, sem imitar ícone de app."""
    k = ("lupa", tam, estrela)
    if k in _ARTE:
        return _ARTE[k]
    T = tam * S
    im = Image.new("RGBA", (T, T), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx = cy = T * 0.40
    R = T * 0.31
    ol = T * 0.022
    ux = uy = math.cos(math.radians(45))
    px, py = -uy, ux

    def faixa(l0, l1, w):
        return [(cx + ux * l0 + px * w / 2, cy + uy * l0 + py * w / 2), (cx + ux * l1 + px * w / 2, cy + uy * l1 + py * w / 2),
                (cx + ux * l1 - px * w / 2, cy + uy * l1 - py * w / 2), (cx + ux * l0 - px * w / 2, cy + uy * l0 - py * w / 2)]
    L0, L1, wc = R * 0.85, R * 1.78, R * 0.44
    ex, ey = cx + ux * L1, cy + uy * L1
    d.polygon(faixa(L0, L1, wc + 2 * ol), fill=r.rgba(CONTORNO))
    d.ellipse([ex - wc / 2 - ol, ey - wc / 2 - ol, ex + wc / 2 + ol, ey + wc / 2 + ol], fill=r.rgba(CONTORNO))
    d.polygon(faixa(L0, L1, wc), fill=r.rgba(AMARELO))
    d.ellipse([ex - wc / 2, ey - wc / 2, ex + wc / 2, ey + wc / 2], fill=r.rgba(AMARELO))
    # frisos do cabo (laranja)
    for l in (R * 1.22, R * 1.42):
        d.line([(cx + ux * l + px * wc * 0.36, cy + uy * l + py * wc * 0.36),
                (cx + ux * l - px * wc * 0.36, cy + uy * l - py * wc * 0.36)], fill=r.rgba(LARANJA), width=int(ol * 1.3))
    # aro
    Ra = R + ol
    d.ellipse([cx - Ra, cy - Ra, cx + Ra, cy + Ra], fill=r.rgba(CONTORNO))
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=r.rgba(BRANCO))
    Rl = R * 0.76
    d.ellipse([cx - Rl - ol, cy - Rl - ol, cx + Rl + ol, cy + Rl + ol], fill=r.rgba(CONTORNO))
    d.ellipse([cx - Rl, cy - Rl, cx + Rl, cy + Rl], fill=r.rgba("#BDF4EF"))
    # reflexo
    Rr = Rl * 0.72
    d.arc([cx - Rr, cy - Rr, cx + Rr, cy + Rr], 200, 255, fill=r.rgba(BRANCO), width=int(Rl * 0.13))
    d.ellipse([cx - Rr * 0.18 - Rl * 0.06, cy - Rr * 0.98 - Rl * 0.06, cx - Rr * 0.18 + Rl * 0.06,
               cy - Rr * 0.98 + Rl * 0.06], fill=r.rgba(BRANCO))
    if estrela:
        _estrela(d, cx + Rl * 0.06, cy + Rl * 0.08, Rl * 0.50, AMARELO, CONTORNO, ol)
        _estrela(d, cx + Rl * 0.55, cy - Rl * 0.40, Rl * 0.16, BRANCO)
    return _guardar(k, _reduzir(im, (tam, tam)))


def botao_lupa(tam=420):
    """Botão redondo (branco, contorno grafite, anel turquesa) com a nossa lupa dentro."""
    k = ("botao", tam)
    if k in _ARTE:
        return _ARTE[k]
    T = tam * S
    im = Image.new("RGBA", (T, T), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    ol = T * 0.025
    d.ellipse([0, 0, T - 1, T - 1], fill=r.rgba(CONTORNO))
    d.ellipse([ol, ol, T - ol, T - ol], fill=r.rgba(TURQUESA))
    e = T * 0.075
    d.ellipse([e, e, T - e, T - e], fill=r.rgba(CONTORNO))
    d.ellipse([e + ol, e + ol, T - e - ol, T - e - ol], fill=r.rgba(BRANCO))
    im = _reduzir(im, (tam, tam))
    lp = lupa(int(tam * 0.74), estrela=False)
    im.alpha_composite(lp, ((tam - lp.width) // 2 + int(tam * 0.04), (tam - lp.height) // 2 + int(tam * 0.04)))
    return _guardar(k, im)


def teclado(larg=660):
    """Teclado nosso (genérico): corpo branco, teclas lilás em 3 fileiras + barra de espaço.
    Devolve (imagem, lista de caixas das teclas em px da imagem)."""
    k = ("teclado", larg)
    if k in _ARTE:
        return _ARTE[k]
    alt = int(larg * 0.47)
    Wt, Ht = larg * S, alt * S
    im = Image.new("RGBA", (Wt, Ht), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    ol = Wt * 0.012
    d.rounded_rectangle([0, 0, Wt - 1, Ht - 1], radius=Ht * 0.10, fill=r.rgba(CONTORNO))
    d.rounded_rectangle([ol, ol, Wt - ol, Ht - ol], radius=Ht * 0.10 - ol, fill=r.rgba(BRANCO))
    m = Wt * 0.045
    gap = Wt * 0.014
    kw = (Wt - 2 * m - 9 * gap) / 10
    kh = (Ht - 2 * m - 3 * gap) / 4
    caixas = []
    fileiras = [(10, 0.0), (9, 0.5), (7, 1.5)]
    for fi, (n, desl) in enumerate(fileiras):
        y0 = m + fi * (kh + gap)
        for i in range(n):
            x0 = m + (desl + i) * (kw + gap)
            caixas.append((x0, y0, x0 + kw, y0 + kh))
    y0 = m + 3 * (kh + gap)
    caixas.append((m + 2.5 * (kw + gap), y0, m + 7.5 * (kw + gap) - gap, y0 + kh))       # espaço
    for (x0, y0, x1, y1) in caixas:
        d.rounded_rectangle([x0, y0, x1, y1], radius=kh * 0.22, fill=r.rgba(CONTORNO))
        d.rounded_rectangle([x0 + ol * 0.7, y0 + ol * 0.7, x1 - ol * 0.7, y1 - ol * 1.6], radius=kh * 0.2,
                            fill=r.rgba("#E6DEFF"))
    # 2 teclas laterais da última fileira (turquesa) e a tecla de apagar (laranja)
    for (x0, y0, x1, y1), cor in ((caixas[19], TURQUESA), (caixas[25], LARANJA)):
        d.rounded_rectangle([x0 + ol * 0.7, y0 + ol * 0.7, x1 - ol * 0.7, y1 - ol * 1.6], radius=kh * 0.2, fill=r.rgba(cor))
    im = _reduzir(im, (larg, alt))
    cx_ = [(x0 / S, y0 / S, x1 / S, y1 / S) for x0, y0, x1, y1 in caixas]
    return _guardar(k, (im, cx_))


@functools.lru_cache(maxsize=8)
def tecla_acesa(w, h):
    T = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(T)
    d.rounded_rectangle([0, 0, w * S - 1, h * S - 1], radius=h * S * 0.22, fill=r.rgba(CONTORNO))
    d.rounded_rectangle([S * 2, S * 2, w * S - S * 2, h * S - S * 4], radius=h * S * 0.2, fill=r.rgba(AMARELO))
    return _guardar(("tecla", w, h), _reduzir(T, (w, h)))


def campo_texto(larg=840, alt=150):
    """Campo branco de texto (borda amarela grossa e contorno grafite). Genérico: sem botão, sem ícone de app."""
    k = ("campo", larg, alt)
    if k in _ARTE:
        return _ARTE[k]
    Wc, Hc = larg * S, alt * S
    im = Image.new("RGBA", (Wc, Hc), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    ol = 4 * S
    rad = Hc * 0.5
    d.rounded_rectangle([0, 0, Wc - 1, Hc - 1], radius=rad, fill=r.rgba(CONTORNO))
    d.rounded_rectangle([ol, ol, Wc - ol, Hc - ol], radius=rad - ol, fill=r.rgba(AMARELO))
    b = ol + 9 * S
    d.rounded_rectangle([b, b, Wc - b, Hc - b], radius=rad - b, fill=r.rgba(BRANCO))
    return _guardar(k, _reduzir(im, (larg, alt)))


def _degrade_vertical(w, h, c1, c2):
    a = np.linspace(0, 1, h)[:, None, None]
    c1, c2 = np.array(r.rgb(c1), float), np.array(r.rgb(c2), float)
    arr = (c1 * (1 - a) + c2 * a).repeat(w, axis=1)
    return Image.fromarray(arr.round().astype(np.uint8), "RGB")


def card_video(larg=460, alt=720):
    """'Um vídeo com o filtro', desenhado de forma esquemática: retângulo em pé com borda branca, play no meio e a
    etiqueta branca '✨ nome do filtro' embaixo. Sem coluna de botões, sem @, sem disco de música: não imita tela."""
    k = ("card", larg, alt)
    if k in _ARTE:
        return _ARTE[k]
    Wc, Hc = larg * S, alt * S
    rad = 46 * S
    ol = 5 * S
    borda = 14 * S
    im = Image.new("RGBA", (Wc, Hc), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, Wc - 1, Hc - 1], radius=rad, fill=r.rgba(CONTORNO))
    d.rounded_rectangle([ol, ol, Wc - ol, Hc - ol], radius=rad - ol, fill=r.rgba(BRANCO))
    dentro = _degrade_vertical(Wc - 2 * (ol + borda), Hc - 2 * (ol + borda), "#7B4BFF", ROSA)
    mask = Image.new("L", dentro.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, dentro.width - 1, dentro.height - 1], radius=rad - ol - borda, fill=255)
    im.paste(dentro, (ol + borda, ol + borda), mask)
    d = ImageDraw.Draw(im)
    # estrelinhas no fundo
    for (fx, fy, fr) in ((0.22, 0.16, 0.05), (0.78, 0.28, 0.035), (0.30, 0.62, 0.03), (0.80, 0.70, 0.045)):
        _estrela(d, Wc * fx, Hc * fy, Wc * fr, (255, 255, 255, 150))
    # play
    pr = Wc * 0.17
    pcx, pcy = Wc * 0.5, Hc * 0.40
    tri = [(pcx - pr * 0.55, pcy - pr * 0.75), (pcx + pr * 0.85, pcy), (pcx - pr * 0.55, pcy + pr * 0.75)]
    d.ellipse([pcx - pr * 1.25, pcy - pr * 1.25, pcx + pr * 1.25, pcy + pr * 1.25], fill=(255, 255, 255, 70))
    d.polygon([(x + 0 * S, y) for x, y in tri], fill=r.rgba(BRANCO), outline=r.rgba(CONTORNO), width=int(ol * 0.8))
    im = _reduzir(im, (larg, alt))
    # etiqueta: o texto encolhe até a pílula (texto + 2 x 24 px) caber dentro do card, com folga de 40 px
    eti = r.texto_img("✨ nome do filtro", 48, "black", ESCURO, AMARELO, 0, CONTORNO, None, larg - 2 * 40 - 48,
                      "centro", 1.08, 1, True, BRANCO, (24, 14), 30)
    im.alpha_composite(eti, ((larg - eti.width) // 2, int(alt * 0.80 - eti.height / 2)))
    return _guardar(k, im)


def card_video_etiqueta_y(alt=720):
    return alt * 0.80


def icone_efeito(cod, tam=120):
    """Ícone do efeito (o mesmo do Effect House) com cantos redondos, borda branca e contorno grafite.
    cod None = estrelinha nossa (nome sem ícone conhecido)."""
    k = ("icone", cod, tam)
    if k in _ARTE:
        return _ARTE[k]
    T = tam * S
    im = Image.new("RGBA", (T, T), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rad = T * 0.24
    ol = T * 0.025
    b = T * 0.06
    d.rounded_rectangle([0, 0, T - 1, T - 1], radius=rad, fill=r.rgba(CONTORNO))
    d.rounded_rectangle([ol, ol, T - ol, T - ol], radius=rad - ol, fill=r.rgba(BRANCO))
    tam_in = int(T - 2 * b)
    if cod:
        ic = Image.open(asset(cod, EFEITOS[cod]["icone"])).convert("RGBA").resize((tam_in, tam_in), Image.LANCZOS)
    else:
        ic = _degrade_vertical(tam_in, tam_in, ROXO, ROSA).convert("RGBA")
        _estrela(ImageDraw.Draw(ic), tam_in / 2, tam_in / 2, tam_in * 0.36, AMARELO, CONTORNO, ol)
    mask = Image.new("L", (tam_in, tam_in), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, tam_in - 1, tam_in - 1], radius=rad - b, fill=255)
    im.paste(ic, (int(b), int(b)), mask)
    return _guardar(k, _reduzir(im, (tam, tam)))


def avatar(tam=280):
    """Foto do perfil (o nosso símbolo) num círculo com anel branco e contorno grafite."""
    k = ("avatar", tam)
    if k in _ARTE:
        return _ARTE[k]
    T = tam * S
    im = Image.new("RGBA", (T, T), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    ol = T * 0.02
    d.ellipse([0, 0, T - 1, T - 1], fill=r.rgba(CONTORNO))
    d.ellipse([ol, ol, T - ol, T - ol], fill=r.rgba(BRANCO))
    b = T * 0.06
    fundo = _degrade_vertical(int(T - 2 * b), int(T - 2 * b), "#FFE58A", AMARELO)
    mask = Image.new("L", fundo.size, 0)
    ImageDraw.Draw(mask).ellipse([0, 0, fundo.width - 1, fundo.height - 1], fill=255)
    im.paste(fundo, (int(b), int(b)), mask)
    im = _reduzir(im, (tam, tam))
    sim = Image.open(SIMBOLO).convert("RGBA")
    lado = int(tam * 0.90)            # o desenho ocupa ~69% do PNG: fica com ~62% do círculo
    sim = sim.resize((lado, lado), Image.LANCZOS)
    im.alpha_composite(sim, ((tam - lado) // 2, (tam - lado) // 2))
    return _guardar(k, im)


def aba_efeitos(cods, larg=800):
    """'✨ Efeitos' com sublinhado amarelo + grade com os ícones dos efeitos aprovados (até 6)."""
    k = ("aba", tuple(cods), larg)
    if k in _ARTE:
        return _ARTE[k]
    rot = r.texto_img("✨ Efeitos", 76, "titulo", BRANCO, AMARELO, 10, CONTORNO, (0, 6, 10, 130), 2000)
    caixa_rot = rot.info["caixa"]
    rot = rot.crop(rot.getbbox())                 # sem a folga transparente (a sombra fica)
    n = max(1, min(6, len(cods)))
    por_linha = 3 if n > 2 else n
    linhas = int(math.ceil(n / por_linha))
    tam_ic = 215 if linhas == 1 else 120
    gap = 26
    grade_w = por_linha * tam_ic + (por_linha - 1) * gap
    grade_h = linhas * tam_ic + (linhas - 1) * gap
    W_ = max(rot.width, grade_w) + 20
    sub_y = rot.height + 8
    H_ = sub_y + 14 + 34 + grade_h + 10
    im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
    im.alpha_composite(rot, ((W_ - rot.width) // 2, 0))
    d = ImageDraw.Draw(im)
    x0 = (W_ - rot.width) // 2 + 4
    x1 = x0 + (caixa_rot[2] - caixa_rot[0]) - 4
    d.rounded_rectangle([x0, sub_y, x1, sub_y + 14], radius=7, fill=r.rgba(AMARELO), outline=r.rgba(CONTORNO), width=3)
    gy = sub_y + 14 + 34
    for i, cod in enumerate(cods[:6]):
        li, co = divmod(i, por_linha)
        na_linha = min(por_linha, n - li * por_linha)
        lw = na_linha * tam_ic + (na_linha - 1) * gap
        ic = icone_efeito(cod, tam_ic)
        im.alpha_composite(ic, ((W_ - lw) // 2 + co * (tam_ic + gap), gy + li * (tam_ic + gap)))
    centro_aba = ((W_) / 2, rot.height / 2)
    return _guardar(k, (im, centro_aba))


# ============================================================================
# Artes do G-V2 (títulos e cartas dos efeitos; a do C05 é montada aqui com as artes do efeito)
# ============================================================================
CARTA_V2 = {"C06": ("cartas", "carta_01.png"),      # MEIA (DE NOVO)
            "C07": ("cartas", "carta_07.png")}      # COMER 12 UVAS (SEM PRESSA)
REACAO_V2 = {"C06": "😑", "C05": "😬", "C07": "😋"}
C05_RESPOSTA = ("respostas_grana", "grana_02.png", "😅")     # O 13º DURA ATÉ O DIA 3
COR_GRANA = "#FFD43B"


def tingir(img, cor):
    im = r.carregar(img)
    c = r.rgb(cor)
    a = np.asarray(im, dtype=np.float32)
    out = np.empty_like(a)
    for i in range(3):
        out[..., i] = a[..., i] / 255.0 * c[i]
    out[..., 3] = a[..., 3]
    return Image.fromarray(out.round().astype(np.uint8), "RGBA")


def com_sombra(img, cor=(12, 8, 40), raio=7, forca=0.75):
    sombra = Image.new("RGBA", img.size, cor + (0,))
    sa = img.getchannel("A").filter(ImageFilter.GaussianBlur(raio))
    sombra.putalpha(sa.point(lambda v: int(min(255, v * forca * 1.4))))
    return Image.alpha_composite(sombra, img)


def titulo_v2(cod):
    k = ("titulo", cod)
    if k in _ARTE:
        return _ARTE[k]
    im = Image.open(asset(cod, "titulo.png")).convert("RGBA")
    im = im.crop(im.getchannel("A").getbbox())
    if cod == "C05":                       # título branco sem fundo: ganha uma sombra escura para ler bem
        pad = 24
        big = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
        big.alpha_composite(im, (pad, pad))
        im = com_sombra(big, raio=9, forca=0.8)
    return _guardar(k, im)


def bolha_c05():
    """Bolha GRANA do C05 (variantes/bolha_inteira) tingida de amarelo, com o rótulo em branco."""
    k = ("bolha",)
    if k in _ARTE:
        return _ARTE[k]
    d = asset("C05", "variantes", "bolha_inteira")
    cheia = np.asarray(Image.open(os.path.join(d, "bolha_inteira_grana.png")).convert("RGBA"), dtype=np.float32)
    vazia = np.asarray(Image.open(os.path.join(d, "bolha_vazia.png")).convert("RGBA"), dtype=np.float32)
    a_rot = np.clip(cheia[..., 3] - vazia[..., 3], 0, 255)
    base = np.asarray(tingir(Image.fromarray(vazia.astype(np.uint8), "RGBA"), COR_GRANA), dtype=np.float32).copy()
    base[..., 3] = np.clip(base[..., 3] * 1.25, 0, 255)
    base = Image.fromarray(base.round().astype(np.uint8), "RGBA")
    rot = np.zeros_like(cheia)
    rot[..., :3] = 255
    rot[..., 3] = a_rot
    rot = Image.fromarray(rot.round().astype(np.uint8), "RGBA")
    sombra = Image.new("RGBA", rot.size, (20, 16, 50, 0))
    sombra.putalpha(rot.getchannel("A").filter(ImageFilter.MaxFilter(5)).point(lambda v: int(v * 0.6)))
    out = Image.alpha_composite(Image.alpha_composite(base, sombra), rot)
    out = out.crop(out.getchannel("A").getbbox())
    return _guardar(k, out)


def pilula_c05(larg=760, alt=168):
    """Resultado do C05 no estilo do efeito: pílula azul-noite com borda amarela, disco com a moeda, a resposta
    (PNG do efeito, tingida) e o emoji da resposta (textos.json)."""
    k = ("pilula", larg, alt)
    if k in _ARTE:
        return _ARTE[k]
    Wp, Hp = larg * S, alt * S
    im = Image.new("RGBA", (Wp, Hp), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([3 * S, 3 * S, Wp - 3 * S, Hp - 3 * S], radius=Hp * 0.5, fill=(16, 14, 46, 240),
                        outline=r.rgba(COR_GRANA), width=6 * S)
    im = _reduzir(im, (larg, alt))
    dd = int(alt * 0.74)
    disco = Image.new("RGBA", (dd * S, dd * S), (0, 0, 0, 0))
    ImageDraw.Draw(disco).ellipse([0, 0, dd * S - 1, dd * S - 1], fill=r.rgba(COR_GRANA))
    disco = _reduzir(disco, (dd, dd))
    lab = Image.open(asset("C05", "bolha_grana.png")).convert("RGBA")
    a = np.asarray(lab)[..., 3]
    linhas = np.nonzero((a > 30).any(axis=1))[0]
    y0 = y = int(linhas.min())
    while y < a.shape[0] and (a[y] > 30).any():
        y += 1
    ic = lab.crop((0, y0, lab.width, y))
    ic = tingir(ic.crop(ic.getchannel("A").getbbox()), "#1A1440")
    kk = dd * 0.58 / max(ic.size)
    ic = ic.resize((max(1, int(ic.width * kk)), max(1, int(ic.height * kk))), Image.LANCZOS)
    disco.alpha_composite(ic, ((dd - ic.width) // 2, (dd - ic.height) // 2))
    xd = int(alt * 0.13)
    im.alpha_composite(disco, (xd, (alt - dd) // 2))
    em = r.emoji_img(C05_RESPOSTA[2], int(alt * 0.5))
    xe = larg - int(alt * 0.18) - em.width
    im.alpha_composite(em, (xe, (alt - em.height) // 2))
    resp = Image.open(asset("C05", C05_RESPOSTA[0], C05_RESPOSTA[1])).convert("RGBA")
    resp = resp.crop(resp.getchannel("A").getbbox())
    ax0 = xd + dd + int(alt * 0.10)
    aw = xe - int(alt * 0.10) - ax0
    ah = int(alt * 0.78)
    esc = min(aw / resp.width, ah / resp.height)
    rw, rh = int(round(resp.width * esc)), int(round(resp.height * esc))
    resp = tingir(resp.resize((rw, rh), Image.LANCZOS), r.misturar(COR_GRANA, BRANCO, 0.25)[:3])
    im.alpha_composite(resp, (ax0 + (aw - rw) // 2, (alt - rh) // 2))
    return _guardar(k, im)


def empilhar(partes, gap=26, larg_max=800):
    """partes: [(imagem, escala, dx)] de cima para baixo -> uma imagem RGBA (largura até larg_max)."""
    ims = [(r.transformar(im, esc), dx) for im, esc, dx in partes]
    Wc = max(i.width + 2 * abs(dx) for i, dx in ims)
    Hc = sum(i.height for i, _ in ims) + gap * (len(ims) - 1)
    out = Image.new("RGBA", (Wc, Hc), (0, 0, 0, 0))
    y = 0
    for i, dx in ims:
        out.alpha_composite(i, ((Wc - i.width) // 2 + dx, y))
        y += i.height + gap
    return out


def slide_v2(cod):
    """Título + 1 carta do efeito, numa imagem só (até 800 px de largura: cabe na zona segura)."""
    k = ("slide", cod)
    if k in _ARTE:
        return _ARTE[k]
    t = titulo_v2(cod)
    if cod == "C05":
        b = bolha_c05()
        p = pilula_c05()
        im = empilhar([(t, 680 / t.width, 0), (b, 285 / b.height, 0), (p, 1.0, 0)], gap=18)
    else:
        c = Image.open(asset(cod, *CARTA_V2[cod])).convert("RGBA")
        c = c.crop(c.getchannel("A").getbbox())
        im = empilhar([(t, 600 / t.width, 0), (c, 770 / c.width, 0)], gap=30)
    return _guardar(k, im)


def pilha_titulos(cods):
    """Gancho do G-V2: os títulos empilhados, levemente girados para os lados."""
    k = ("pilha", tuple(cods))
    if k in _ARTE:
        return _ARTE[k]
    larg = {1: 760, 2: 700, 3: 640}[len(cods)]
    rots = [-3.0, 2.5, -2.0]
    partes = []
    for i, cod in enumerate(cods):
        t = titulo_v2(cod)
        alvo = larg * (1.06 if cod == "C05" else 1.0)
        partes.append(r.transformar(t, alvo / t.width, rots[i % 3]))
    gap = 26
    Wc = max(p.width for p in partes)
    Hc = sum(p.height for p in partes) + gap * (len(partes) - 1)
    out = Image.new("RGBA", (Wc, Hc), (0, 0, 0, 0))
    y = 0
    for p in partes:
        out.alpha_composite(p, ((Wc - p.width) // 2, y))
        y += p.height + gap
    esc = min(1.0, 900 / out.height, 800 / out.width)        # cabe entre o gancho e a base da zona segura
    if esc < 1.0:
        out = out.resize((int(round(out.width * esc)), int(round(out.height * esc))), Image.LANCZOS)
    return _guardar(k, out)


# ============================================================================
# Som (tudo feito aqui ou na biblioteca, com numpy)
# ============================================================================
@functools.lru_cache(maxsize=8)
def som_sininho(semente=0):
    """Sininho pequeno (ré, 2349 Hz) com parciais de sino e 4 guizos rápidos por cima. Um toque só, sem melodia."""
    rng = np.random.default_rng(4400 + int(semente))
    dur = 1.0
    n = int(dur * SR)
    t = np.arange(n) / SR
    f0 = 2349.3 * (1 + 0.004 * (semente % 3))
    s = np.zeros(n)
    for m, a, tau in ((1.0, 1.0, 0.36), (2.0, 0.30, 0.20), (2.92, 0.26, 0.13), (4.13, 0.10, 0.07), (5.40, 0.05, 0.04)):
        s += a * np.sin(2 * np.pi * f0 * m * t + rng.uniform(0, 6.28)) * np.exp(-t / tau)
    s *= np.minimum(1, t / 0.0015)
    for kk, th in enumerate((0.0, 0.058, 0.121, 0.19)):
        i0 = int(th * SR)
        tt = t[: n - i0]
        fb = rng.uniform(3900, 5100)
        g = sum(a * np.sin(2 * np.pi * fb * m * tt + rng.uniform(0, 6.28)) for m, a in ((1.0, 1.0), (1.51, 0.55), (2.17, 0.35)))
        g = g * np.exp(-tt / 0.03) * np.minimum(1, tt / 0.0008)
        cl = r._passa_baixa(np.diff(rng.standard_normal(len(tt)) * np.exp(-tt / 0.004), prepend=0.0), 6500.0)
        s[i0:] += (0.45 * g + 0.5 * cl) * (0.9 - 0.15 * kk)
    return r._normal(s, 0.9).astype(np.float32)


@functools.lru_cache(maxsize=8)
def som_estouro(semente=0):
    """Estouro de bolha: 'plop' que sobe de tom + estalo filtrado + borrifo."""
    rng = np.random.default_rng(5500 + int(semente))
    dur = 0.22
    t = np.arange(int(dur * SR)) / SR
    f = 230 + 950 * (1 - np.exp(-t / 0.011))
    plop = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.045) * np.minimum(1, t / 0.0008)
    ru = rng.standard_normal(len(t))
    estalo = r._passa_baixa(np.diff(ru, prepend=0.0) * np.exp(-t / 0.0018), 6500.0)
    borrifo = (ru - r._passa_baixa(ru, 2500.0)) * np.exp(-np.maximum(0, t - 0.005) / 0.03) * (t >= 0.005) * 0.25
    s = plop + estalo + borrifo
    return r._normal(s, 0.9).astype(np.float32)


@functools.lru_cache(maxsize=8)
def som_brilho(notas=6, base=1568.0, passo=0.045):
    """Brilho: notas agudas subindo (pentatônica), passando de um lado para o outro. Estéreo."""
    esc = [1.0, 9 / 8, 5 / 4, 3 / 2, 5 / 3, 2.0, 9 / 4, 5 / 2]
    dec = 0.2
    n = int((passo * notas + dec * 3) * SR)
    out = np.zeros((n, 2))
    for kk in range(notas):
        f = base * esc[kk % len(esc)]
        t = np.arange(int(dec * 3 * SR)) / SR
        s = (np.sin(2 * np.pi * f * t) + 0.22 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / 0.03))
        s *= np.exp(-t / dec) * np.minimum(1, t / 0.002) * (0.75 + 0.25 * kk / notas)
        i0 = int(kk * passo * SR)
        m = min(len(s), n - i0)
        a = (-0.6 + 1.2 * kk / max(1, notas - 1) + 1) * np.pi / 4
        out[i0:i0 + m, 0] += s[:m] * math.cos(a)
        out[i0:i0 + m, 1] += s[:m] * math.sin(a)
    return (out / (np.max(np.abs(out)) + 1e-9) * 0.8).astype(np.float32)


def teclas_rapidas(v, t0, n=3, passo=0.085, volume=0.5):
    for i in range(n):
        v.som("tecla", t0 + i * passo, volume * (1 - 0.08 * i), 0.15 * (-1) ** i, semente=i % 4)


# ============================================================================
# Fundos
# ============================================================================
def fundo_v1():
    """Roxo do perfil com lupinhas 🔎 bem clarinhas descendo devagar."""
    base = r.DegradeAnimado(["#24106A", "#3A1CB0", "#5B2EFF", "#7A2BD8", "#3A1CB0"], angulo=100, velocidade=0.045)
    return r.Padrao("emoji", emoji="🔎", cor_forma=(255, 255, 255, 34), tamanho=300, velocidade=(14, 46), fundo=base)


def fundo_v2():
    """Noite de fim de ano: azul-noite → roxo → magenta, estrelinhas douradas caindo devagar."""
    base = r.DegradeAnimado(["#0E1240", "#1F1764", "#3C1A7C", "#6A1E86", "#3C1A7C", "#1F1764"], angulo=100,
                            velocidade=0.04, giro=8.0)
    return r.Padrao("estrelas", cor_forma=(255, 206, 84, 60), tamanho=200, velocidade=(10, 60), fundo=base)


def fundo_cf():
    """Fundo do cartão final (igual nas 2 peças): roxo escuro com estrelinhas amarelas."""
    base = r.DegradeAnimado(["#1C1050", "#2E1B86", "#4422B4", "#2E1B86"], angulo=100, velocidade=0.05)
    return r.Padrao("estrelas", cor_forma=(255, 212, 59, 64), tamanho=170, velocidade=(0, 36), fundo=base)


# ============================================================================
# Peças de tela comuns
# ============================================================================
def cortina(v, bg, t0, fim, z=52):
    """O cartão final sobe de baixo para cima, cobrindo tudo. A borda é uma faixa amarela."""
    def f(canvas, tl, t):
        p = r.progresso(tl, 0, 0.32, "out_cubic")
        y0 = int(round(r.H * (1 - p)))
        if y0 >= r.H:
            return
        fundo = bg.quadro(t)
        canvas.paste(fundo.crop((0, y0, r.W, r.H)), (0, y0))
        if p < 1:
            ImageDraw.Draw(canvas).rectangle([0, max(0, y0 - 7), r.W, y0 + 7], fill=r.rgb(AMARELO))
    v.adicionar(f, t0, fim, z)


@functools.lru_cache(maxsize=64)
def cabe_em(texto, largura, maximo, fonte="titulo", contorno=10, minimo=30):
    """Maior fonte (até 'maximo') em que o texto cabe numa linha só dentro de 'largura' px (tinta)."""
    for s in range(int(maximo), minimo - 1, -2):
        im = r.texto_img(texto, s, fonte, BRANCO, AMARELO, contorno, CONTORNO, (0, 6, 10, 130), 4000, "centro", 1.08,
                         1, False, None)
        bb = im.info["caixa"]
        if bb[2] - bb[0] <= largura:
            return s
    return minimo


def lista_nomes(v, nomes, t0, fim, y0, y1, estatico=False, larg=850, cx=505):
    """Nomes dos filtros, um embaixo do outro, cada um com o ícone do efeito ao lado (o mesmo ícone que aparece
    na busca). Todos com a mesma fonte, em amarelo."""
    n = len(nomes)
    altura = y1 - y0
    linha_h = min(176.0, altura / n)
    tam_ic = int(min(116, linha_h * 0.74))
    gap = 24
    maximo = min(96, int(linha_h * 0.60))
    tam = min(cabe_em(f"*{nm}*", larg - tam_ic - gap, maximo) for nm in nomes)
    linhas = []
    for nm in nomes:
        cheio = r.texto_img(f"*{nm}*", tam, "titulo", BRANCO, AMARELO, 10, CONTORNO, (0, 6, 10, 130), 4000, "centro",
                            1.08, 1, False, None)
        bb = cheio.info["caixa"]
        txt = cheio.crop((bb[0], 0, bb[2] + 14, cheio.height))     # sem a folga da esquerda (alinha pelo ícone)
        cy_t = (bb[1] + bb[3]) / 2                                   # meio da tinta do texto
        ic = icone_efeito(efeito_do_nome(nm), tam_ic)
        Hl = int(math.ceil(max(tam_ic, 2 * cy_t, 2 * (txt.height - cy_t))))
        lin = Image.new("RGBA", (tam_ic + gap + txt.width, Hl), (0, 0, 0, 0))
        lin.alpha_composite(ic, (0, (Hl - tam_ic) // 2))
        lin.alpha_composite(txt, (tam_ic + gap, int(round(Hl / 2 - cy_t))))   # tinta centrada no ícone
        linhas.append(_guardar(("linha", nm, tam, tam_ic), lin))
    larg_bloco = max(l.width for l in linhas)
    x_esq = cx - larg_bloco / 2
    alt_bloco = linha_h * n
    yc0 = (y0 + y1) / 2 - alt_bloco / 2 + linha_h / 2
    for i, lin in enumerate(linhas):
        c = (x_esq + lin.width / 2, yc0 + i * linha_h)
        ti = t0 if estatico else t0 + 0.30 + 0.12 * i
        v.imagem(lin, ti, fim, centro=c, entrada=None if estatico else "pop", som=not estatico and i == 0,
                 z=62, nome=f"CF nome {i + 1}")
    return tam


def cartao_final(v, t0, fim, nomes, pergunta, estatico=False, som_extra=None):
    """CF: símbolo do perfil + 'Procura na lupa 🔎' + nomes dos filtros (amarelo, 1 linha cada) + pergunta."""
    bg = fundo_cf()
    if not estatico:
        cortina(v, bg, t0, fim)
        v.som("plim", t0 + 0.05, 0.62)
        if som_extra:
            som_extra(t0)
    e = None if estatico else "pop"
    dt = (lambda d: t0) if estatico else (lambda d: t0 + d)
    v.imagem(SIMBOLO, dt(0.10), fim, centro=(CX, 412), escala=0.29, entrada=e, som=False,
             ocioso=None if estatico else "flutuar", z=61, nome="CF símbolo")
    v.texto("Procura na lupa 🔎", dt(0.18), fim, centro=(CX, 622), tamanho=86, fonte="black", max_linhas=1,
            entrada=e, saida=None, som=False, z=62, nome="CF lupa")
    lista_nomes(v, nomes, t0, fim, 690, 1338, estatico=estatico)
    v.texto(pergunta, dt(0.62 + 0.1 * len(nomes)), fim, centro=(CX, 1424), tamanho=58, fonte="black", cor=ESCURO,
            contorno=0, max_linhas=1, largura_max=740, caixa=BRANCO, sombra=(0, 6, 10, 110), entrada=e, saida=None,
            som=False, z=62, nome="CF pergunta")
    if not estatico:
        v.brilhos(t0 + 0.2, (CX, 412), raio=(150, 120), quantidade=8, duracao=1.4)


def topo(v, texto, ini, fim, tamanho=104, max_linhas=2, entrada="pop", saida="pop", ocioso=None, som=True,
         y=410, nome="topo", z=22, largura_max=820, x=530):
    """Texto de cima. Até 820 px centrado em x = 530: fica de 120 a 940 (zona segura: 60 a 940)."""
    v.texto(texto, ini, fim, centro=(x, y), tamanho=tamanho, max_linhas=max_linhas, largura_max=largura_max,
            entrada=entrada, saida=saida, dur_saida=0.16, ocioso=ocioso, som=som, z=z, nome=nome)


def pontos(v, tempos, fim, y=1440):
    """3 pontinhos de passo (o atual em amarelo e mais largo). Simples, sem número."""
    def f(canvas, tl, t):
        d = ImageDraw.Draw(canvas)
        op = r.limitar(tl / 0.2) * r.limitar((fim - t) / 0.15)
        if op <= 0.01:
            return
        ativo = max(i for i in range(len(tempos)) if tempos[i] <= t + 1e-9)
        larg = [92 if i == ativo else 30 for i in range(3)]
        tot = sum(larg) + 2 * 22
        x = CX - tot / 2
        for i in range(3):
            cor = r.rgb(AMARELO) if i == ativo else (255, 255, 255)
            a = op if i == ativo else op * 0.55
            fundo = canvas.getpixel((int(x + larg[i] / 2), y))
            c = tuple(int(round(fundo[k] * (1 - a) + cor[k] * a)) for k in range(3))
            cc = tuple(int(round(fundo[k] * (1 - a) + r.rgb(CONTORNO)[k] * a)) for k in range(3))
            d.rounded_rectangle([x - 4, y - 19, x + larg[i] + 4, y + 19], radius=19, fill=cc)
            d.rounded_rectangle([x, y - 15, x + larg[i], y + 15], radius=15, fill=c)
            x += larg[i] + 22
    v.adicionar(f, tempos[0], fim, 30)


# ============================================================================
# G-V1 · "Como achar nossos filtros" · 10 s · trilha 100 bpm · tecla + plim
# ============================================================================
T1, T2, T3, TCF, DUR = 1.9, 3.85, 5.85, 7.9, 10.0     # inícios: passo 1, passo 2, passo 3, cartão final


def video_v1(nomes, aba=False):
    v = r.Video(DUR, semente=1101 if not aba else 1102)
    v.fundo(fundo_v1())
    v.trilha(volume=0.27, bpm=100, progressao=[(45, "m"), (41, ""), (43, ""), (40, "m")], ducking=0.5)

    # 0–1,9 s: gancho (já no 1º quadro) + lupa grande
    teclas_rapidas(v, 0.0, n=3, volume=0.55)
    v.som("plim", 0.32, 0.30, duas=False)
    topo(v, "Não achou o filtro?\n*É fácil*", 0.0, T1, tamanho=118, entrada=None, ocioso="pulsar", som=False,
         y=420, nome="gancho")
    v.imagem(lupa(560), 0.0, T1, centro=(CX - 12, 985), entrada=None, saida="zoom", ocioso="balancar", som=False,
             nome="lupa grande")
    v.brilhos(0.15, (CX - 50, 930), raio=(250, 230), quantidade=10, duracao=1.6)

    # 1,9–3,85 s: 1. Toca na lupa 🔎
    v.som("vush", T1 - 0.12, 0.35)
    topo(v, "1. Toca na *lupa* 🔎", T1, T2, tamanho=108, max_linhas=1, nome="passo 1")
    v.imagem(botao_lupa(430), T1 + 0.06, T2, centro=(CX, 940), entrada="pop", saida="pop", som=False,
             ocioso="flutuar", nome="botão lupa")
    v.toque(T1 + 0.62, centro=(CX + 30, 960))
    v.som("plim", T1 + 0.80, 0.40, duas=False)
    v.brilhos(T1 + 0.78, (CX, 940), raio=(250, 250), quantidade=10, duracao=1.0)
    pontos(v, [T1, T2, T3], TCF)

    # 3,85–5,85 s: 2. Digita o nome do filtro ⌨️ (o 1º nome, letra por letra, com tecla)
    v.som("vush", T2 - 0.12, 0.35)
    topo(v, "2. Digita o\n*nome do filtro* ⌨️", T2, T3, tamanho=100, nome="passo 2")
    nome = nomes[0]
    campo = campo_texto(820, 150)
    x_campo, y_campo = 530, 800            # 120 a 940: dentro da zona segura
    v.imagem(campo, T2 + 0.04, T3, centro=(x_campo, y_campo), entrada="pop", saida="pop", som=False, nome="campo")
    t_dig = T2 + 0.25
    L = r.contar_letras(nome)
    cps = max(14.0, L / 1.0)                # termina ~0,7 s antes do passo 3 (nome inteiro na tela)
    tam_nome = cabe_em(nome, 700, 68, "black", 0)
    v.texto(nome, t_dig, T3, centro=(x_campo, y_campo), tamanho=tam_nome, fonte="black", cor=ESCURO, contorno=0,
            sombra=None, max_linhas=1, largura_max=4000, entrada="digitar", saida="pop", dur_saida=0.16, cps=cps,
            z=24, nome="nome digitado")
    t_fim_dig = t_dig + L / cps
    cheio = r.texto_img(nome, tam_nome, "black", ESCURO, AMARELO, 0, CONTORNO, None, 4000, "centro", 1.08, 1, True, None)
    fonte_n = r.fonte("black", cheio.info["tamanho_usado"])
    letras = [cl for cl, em, dd in r._parse(nome) if cl != "\n"]
    x_ini = x_campo - cheio.width / 2 + cheio.info["caixa"][0]

    def cursor(canvas, tl, t):
        k = min(len(letras), int(tl * cps) + 1) if tl >= 0 else 0
        pref = "".join(letras[:k])
        x = x_ini + fonte_n.getlength(pref) + 6
        piscando = t > t_fim_dig + 0.05 and ((t - t_fim_dig) * 2.4) % 1 > 0.55
        if not piscando:
            ImageDraw.Draw(canvas).rounded_rectangle([x, y_campo - 38, x + 7, y_campo + 38], radius=3,
                                                     fill=r.rgb(ROXO))
    v.adicionar(cursor, t_dig, T3 - 0.16, 25)
    tec, caixas = teclado(680)
    y_tec = 1150
    v.imagem(tec, T2 + 0.12, T3, centro=(CX, y_tec), entrada="pop", saida="pop", som=False, nome="teclado")
    ordem_teclas = [3, 12, 22, 7, 15, 1, 18, 9, 20, 5, 14, 24, 0, 11, 17, 6, 21, 2, 13, 8, 19, 4, 16, 10, 23]
    x0_t, y0_t = CX - tec.width / 2, y_tec - tec.height / 2

    def acende(canvas, tl, t):
        k = int((t - t_dig) * cps)
        if t < t_dig or k >= L:
            return
        idx = 26 if letras[k] == " " else ordem_teclas[k % len(ordem_teclas)]
        bx0, by0, bx1, by1 = caixas[idx]
        sp = tecla_acesa(int(round(bx1 - bx0)), int(round(by1 - by0)))
        r._pintar(canvas, sp, int(round(x0_t + bx0)), int(round(y0_t + by0)))
    v.adicionar(acende, t_dig, T3, 13)
    v.som("plim", t_fim_dig + 0.08, 0.50)
    v.brilhos(t_fim_dig + 0.05, (x_campo, y_campo), raio=(410, 110), quantidade=10, duracao=1.0)

    # 5,85–7,9 s: passo 3 (sem a aba: toca no nome no vídeo de quem usou; com a aba: perfil → aba de efeitos)
    v.som("vush", T3 - 0.12, 0.35)
    if not aba:
        topo(v, "Ou toca no nome do filtro *no vídeo de quem usou* ✨", T3, TCF, tamanho=90, max_linhas=3,
             y=395, nome="passo 3")
        cv = card_video(460, 720)
        y_cv = 1010
        v.imagem(cv, T3 + 0.06, TCF, centro=(CX, y_cv), entrada="pop", som=False, ocioso="flutuar", nome="vídeo")
        y_eti = y_cv - 720 / 2 + card_video_etiqueta_y(720)
        v.toque(T3 + 0.80, centro=(CX + 20, y_eti))
        v.som("plim", T3 + 0.98, 0.42, duas=False)
        v.brilhos(T3 + 0.95, (CX, y_eti), raio=(220, 70), quantidade=9, duracao=1.0)
    else:
        topo(v, "Ou entra no *meu perfil*, na *aba de efeitos* ✨", T3, TCF, tamanho=96, max_linhas=3,
             y=395, nome="passo 3 (aba)")
        cods = [efeito_do_nome(nm) for nm in nomes]
        av = avatar(280)
        v.imagem(av, T3 + 0.04, TCF, centro=(CX, 745), entrada="pop", som=False, nome="perfil")
        aba_img, c_aba = aba_efeitos(cods)
        y_aba = 950 + aba_img.height / 2          # topo fixo; a base fica acima dos pontinhos (y 1420)
        v.imagem(aba_img, T3 + 0.20, TCF, centro=(CX, y_aba), entrada="pop", som=False, nome="aba de efeitos")
        y_rot = y_aba - aba_img.height / 2 + c_aba[1]
        v.toque(T3 + 0.82, centro=(CX + 40, y_rot))
        v.som("plim", T3 + 1.0, 0.42, duas=False)
        v.brilhos(T3 + 0.98, (CX, y_rot), raio=(200, 60), quantidade=8, duracao=1.0)

    # 7,9–10 s: cartão final com os nomes aprovados
    cartao_final(v, TCF, None, nomes, "Qual você vai usar primeiro?",
                 som_extra=lambda t0: teclas_rapidas(v, t0 + 0.32, n=4, passo=0.07, volume=0.38))
    return v


# ============================================================================
# G-V2 · "3 filtros pro fim de ano" · 10 s · sininho + estouro + plim
# ============================================================================
NUM = {1: "Um", 2: "2", 3: "3"}


def gancho_v2(n):
    return f"{NUM[n]} {'filtro' if n == 1 else 'filtros'} pro\n*fim de ano* 🎄"


def slides_zoom(v, sprites, tempos, centros, fim, dur_trans=0.35, z=12, nome="slides"):
    """Um sprite por vez (o i-ésimo a partir de tempos[i]) com transição 'zoom' (a mesma do Video.slides da
    biblioteca, mas aceita tempos diferentes) e um leve flutuar."""
    def f(canvas, tl, t):
        i = max(k for k in range(len(tempos)) if tempos[k] <= t + 1e-9)
        u = t - tempos[i]
        dy = 9 * math.sin(2 * math.pi * t / 2.6)
        c = (centros[i][0], centros[i][1] + dy)
        if i > 0 and u < dur_trans:
            p = r.ease_in_out_cubic(u / dur_trans)
            r.colar(canvas, sprites[i - 1], (centros[i - 1][0], centros[i - 1][1] + dy), 1 + 0.4 * p, 0, 1 - p)
            r.colar(canvas, sprites[i], c, 0.7 + 0.3 * p, 0, p)
        else:
            r.colar(canvas, sprites[i], c, 1.0)
            if v._registrando:
                v._registrar(f"{nome} {i}", r.caixa_nominal(sprites[i], centros[i], 1.0), t)
    v.adicionar(f, tempos[0], fim, z)


def video_v2(nomes):
    cods = [efeito_do_nome(nm) for nm in nomes]
    n = len(cods)
    v = r.Video(DUR, semente=1201)
    v.fundo(fundo_v2())
    v.trilha(volume=0.25, bpm=110, progressao=[(43, ""), (47, "m"), (45, "m"), (38, "")], ducking=0.5)
    t_fim_slides = 8.0
    cada = (t_fim_slides - 2.0) / n
    tempos = [0.0] + [2.0 + i * cada for i in range(n)]
    sprites = [pilha_titulos(cods)] + [slide_v2(c) for c in cods]
    y_slide = 950

    # 0–2 s: gancho + os títulos (tudo já no 1º quadro), sininho logo no começo
    v.som(som_sininho(0), 0.0, 0.55)
    v.som("pop", 0.0, 0.35)
    topo(v, gancho_v2(n), 0.0, 2.0, tamanho=112, entrada=None, ocioso="pulsar", som=False, y=372, nome="gancho")
    centros = [(CX, 1005)] + [(CX, y_slide)] * n
    slides_zoom(v, sprites, tempos, centros, t_fim_slides + 0.4)
    v.brilhos(0.2, (CX, 1005), raio=(400, 440), quantidade=12, duracao=1.7)

    # 2–8 s: um efeito por vez: nome exato em amarelo, título + 1 carta, carinha embaixo
    for i, (cod, nm) in enumerate(zip(cods, nomes)):
        ti = tempos[i + 1]
        tf = ti + cada
        v.som("vush", ti - 0.16, 0.32)
        tam = cabe_em(f"*{nm}*", 800, 104)
        v.texto(f"*{nm}*", ti + 0.05, tf if i < n - 1 else t_fim_slides + 0.4, centro=(CX, 372), tamanho=tam,
                max_linhas=1, largura_max=4000, entrada="pop", saida="pop", dur_saida=0.16, som=False, z=22,
                nome=f"nome {cod}")
        v.imagem(r.emoji_img(REACAO_V2[cod], 150), ti + 0.45, tf if i < n - 1 else t_fim_slides + 0.4,
                 centro=(CX, 1408), entrada="pop", saida="pop", dur_saida=0.15, som=False, ocioso="flutuar", z=14,
                 nome=f"carinha {cod}")
        if cod == "C06":            # sininho + pop de caixa
            v.som("pop", ti + 0.02, 0.55, f0=260.0, f1=900.0, dur=0.14)
            v.som(som_sininho(1), ti + 0.08, 0.52)
        elif cod == "C05":          # estouro de bolha + brilho
            v.som(som_estouro(0), ti + 0.02, 0.62)
            v.som(som_brilho(6, 1760.0, 0.045), ti + 0.09, 0.30)
            v.som(som_estouro(1), ti + 0.45, 0.40)
        else:                       # plim + brilho
            v.som("plim", ti + 0.04, 0.55)
            v.som(som_brilho(5, 1568.0, 0.05), ti + 0.12, 0.22)
        v.som("pop", ti + 0.47, 0.32)
        v.brilhos(ti + 0.12, (CX, y_slide), raio=(420, 380), quantidade=10, duracao=1.3)

    # 8–10 s: cartão final com os nomes
    cartao_final(v, t_fim_slides, None, nomes, "Qual combina com você? 🎄",
                 som_extra=lambda t0: v.som(som_sininho(2), t0 + 0.30, 0.42))
    return v


# ============================================================================
# Capas (1080x1920, texto dentro do miolo 3:4: y 240 a 1680; rodapé acima de 1520)
# ============================================================================
def capa_v1():
    v = r.Video(1.0, semente=1111)
    v.fundo(fundo_v1())
    v.texto("COMO ACHAR\nNOSSOS\n*FILTROS* 🔎", 0, None, centro=(CX, 500), tamanho=136, entrada=None, saida=None,
            contorno=14, largura_max=900, max_linhas=3)
    v.imagem(lupa(520), 0, None, centro=(CX - 10, 1090), entrada=None, som=False)
    v.texto("Passo a passo em *10 segundos*", 0, None, centro=(CX, 1462), tamanho=58, fonte="black", entrada=None,
            saida=None, largura_max=880, max_linhas=1)
    return v.quadro(0.0)


def capa_v2(nomes):
    cods = [efeito_do_nome(nm) for nm in nomes]
    n = len(cods)
    v = r.Video(1.0, semente=1211)
    v.fundo(fundo_v2())
    txt = f"{NUM[n].upper()} {'FILTRO' if n == 1 else 'FILTROS'}\nPRO *FIM*\n*DE ANO* 🎄"
    v.texto(txt, 0, None, centro=(CX, 505), tamanho=136, entrada=None, saida=None, contorno=14, largura_max=900,
            max_linhas=3)
    pil = pilha_titulos(cods)
    k = min(1.0, 700 / pil.height, 860 / pil.width)
    v.imagem(pil, 0, None, centro=(CX, 1075), escala=k, entrada=None, som=False)
    v.texto("Procura na *lupa* 🔎", 0, None, centro=(CX, 1462), tamanho=62, fonte="black", entrada=None,
            saida=None, largura_max=880, max_linhas=1)
    return v.quadro(0.0)


# ============================================================================
# Legendas (legenda + hashtags numa linha só, como no plano) e comentário fixado (vai no roteiro)
# ============================================================================
def legenda_v1(aba):
    if aba:
        txt = "Viu um filtro nosso e não achou? Procura o nome na lupa 🔎 ou entra no meu perfil, na aba de efeitos ✨"
    else:
        txt = "Viu um filtro nosso e não achou? Procura o nome na lupa 🔎 ou toca no nome dele no vídeo de quem usou ✨"
    return txt + " #filtro #filtrotiktok #efeitostiktok"


def legenda_v2(nomes):
    cods = [efeito_do_nome(nm) for nm in nomes]
    filtros = "Filtro" if len(nomes) == 1 else "Filtros"
    tags = ["#filtrotiktok", "#amigosecreto" if "C06" in cods else "#fimdeano", "#natal", "#anonovo", "#2027"]
    return f"{filtros} pro fim de ano: {juntar(nomes)} 🎄 Procura na lupa 🔎 " + " ".join(tags)


def comentario(nomes, aba, pergunta):
    rot = "Nome do filtro" if len(nomes) == 1 else "Nomes dos filtros"
    onde = "Procura na lupa ou no meu perfil." if aba else "Procura na lupa."
    return f"{rot}: {juntar(nomes)} 🔎 {onde} {pergunta}"


# ============================================================================
# Render determinístico e medição do som
# ============================================================================
def medir_audio(arq):
    """Volume integrado (LUFS) e pico real (dBTP) pelo filtro ebur128 do ffmpeg."""
    p = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-map", "0:a", "-af",
                        "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    txt = p.stderr[p.stderr.rfind("Summary:"):]
    lufs = re.search(r"I:\s+(-?[\d.]+) LUFS", txt)
    pico = re.search(r"Peak:\s+(-?[\d.]+) dBFS", txt)
    return (float(lufs.group(1)) if lufs else None, float(pico.group(1)) if pico else None)


AAC = ["-c:a", "aac", "-b:a", "128k", "-ar", str(SR), "-ac", "2"]


def ajustar_ganho(audio, tmp, ganho_db=-1.8, teto_dbtp=-1.3):
    """Abaixa o áudio 'ganho_db' (folga para o AAC) e confere o pico real num AAC só do som (mesmo codificador e
    mesmos parâmetros do MP4). Se passar do teto, abaixa mais e confere de novo. Devolve (ganho_db, wav)."""
    wav = os.path.join(tmp, "audio.wav")
    for _ in range(6):
        r.salvar_wav(wav, audio * 10 ** (ganho_db / 20))
        m4a = os.path.join(tmp, "teste.m4a")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", wav] + AAC + ["-fflags", "+bitexact", "-flags:a",
                       "+bitexact", m4a], check=True)
        _, pico = medir_audio(m4a)
        if pico is None or pico <= teto_dbtp:
            break
        ganho_db -= (pico - teto_dbtp) + 0.2
    return ganho_db, wav


def render_det(v, saida, kbps=2000, limite_bytes=int(3.9 * 1024 * 1024)):
    """Mesmo formato do Video.renderizar da biblioteca (H.264 High 4.1, yuv420p, BT.709, 30 fps, GOP 2 s,
    AAC 128k estéreo 44,1 kHz, +faststart, bitexact), com duas diferenças conhecidas da equipe:
    1) x264 em 1 thread: com várias threads + teto de bitrate o MP4 sai com bytes diferentes a cada rodada;
    2) som com folga de ~1,8 dB antes do AAC (o pico real passava de -1 dBTP depois do AAC), conferida antes.
    Se passar do limite de tamanho, refaz com teto 12% menor."""
    t0 = time.time()
    n = int(round(v.duracao * v.fps))
    tmp = tempfile.mkdtemp(prefix="gerais_render_")
    try:
        ganho_db, wav = ajustar_ganho(v.audio(), tmp)
        while True:
            cmd = ["ffmpeg", "-y", "-v", "error",
                   "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{r.W}x{r.H}", "-r", str(v.fps), "-i", "-",
                   "-i", wav, "-map", "0:v", "-map", "1:a",
                   "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
                   "-c:v", "libx264", "-threads", "1", "-preset", "medium", "-crf", "21",
                   "-maxrate", f"{kbps}k", "-bufsize", f"{2 * kbps}k",
                   "-profile:v", "high", "-level:v", "4.1", "-pix_fmt", "yuv420p", "-g", str(v.fps * 2),
                   "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"] + AAC + [
                   "-t", f"{v.duracao:.3f}", "-movflags", "+faststart",
                   "-fflags", "+bitexact", "-flags:v", "+bitexact", "-flags:a", "+bitexact", "-map_metadata", "-1",
                   saida]
            v._zonas = {}
            v._registrando = True            # checagem de zona segura da biblioteca (mesma regra do renderizar)
            p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
            try:
                for i in range(n):
                    p.stdin.write(v.quadro(i / v.fps).tobytes())
            finally:
                v._registrando = False
                p.stdin.close()
                p.wait()
            if p.returncode != 0:
                raise RuntimeError("ffmpeg falhou")
            if os.path.getsize(saida) <= limite_bytes or kbps < 800:
                break
            kbps = int(kbps * 0.88)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    info = r.info_video(saida)
    info["tempo_render_s"] = round(time.time() - t0, 1)
    info["teto_kbps"] = kbps
    info["ganho_audio_db"] = round(ganho_db, 2)
    info["avisos_zona"] = v.relatorio_zonas()
    info["lufs"], info["pico_dbtp"] = medir_audio(saida)
    with open(saida, "rb") as f:
        info["md5"] = hashlib.md5(f.read()).hexdigest()
    print(f"OK {saida}: {info['duracao_s']} s, {info['tamanho_mb']} MB, {info['codecs']}, "
          f"{info['lufs']} LUFS, pico {info['pico_dbtp']} dBTP, render {info['tempo_render_s']} s", file=sys.stderr)
    for aviso in info["avisos_zona"]:
        print("  AVISO zona segura:", aviso, file=sys.stderr)
    return info


# ============================================================================
# Prévia (prancha de 6 quadros por vídeo, com as faixas da interface do TikTok em vermelho)
# ============================================================================
TEMPOS_PREVIA = {
    "G-V1": [0.0, 0.5, 2.9, 5.5, 7.2, 9.6],
    "G-V1-aba": [0.0, 2.9, 4.6, 5.5, 7.2, 9.6],
    "G-V2": [0.0, 0.5, 3.0, 5.0, 7.0, 9.6],
}


def previa(mp4s, saida, largura=250):
    alt = int(largura * r.H / r.W)
    m, cab, rot = 14, 46, 30
    cols = 6
    Wp = cols * largura + (cols + 1) * m
    Hp = m + len(mp4s) * (cab + alt + rot + m)
    pr = Image.new("RGB", (Wp, Hp), (24, 25, 30))
    d = ImageDraw.Draw(pr)
    y = m
    for cod, mp4 in mp4s:
        info = r.info_video(mp4)
        d.text((m, y + 8), f"{cod}.mp4 · {info['duracao_s']:.2f} s · {info['tamanho_mb']} MB · {info['codecs']}"
               f" · vermelho = interface do TikTok", font=r.fonte("bold", 21), fill=(235, 235, 240))
        y += cab
        for i, t in enumerate(TEMPOS_PREVIA[cod]):
            q = r._extrair_quadro(mp4, min(t, info["duracao_s"] - 0.05))
            th = r.desenhar_zonas(q.resize((largura, alt), Image.LANCZOS), cor=(255, 40, 40, 55),
                                  contorno=(255, 220, 0, 170))
            x = m + i * (largura + m)
            pr.paste(th, (x, y))
            d.text((x + 4, y + alt + 4), f"t = {t:.1f} s", font=r.fonte("semi", 20), fill=(200, 205, 215))
        y += alt + rot + m
    pr = pr.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
    pr.save(saida, optimize=True)
    return saida


# ============================================================================
# Principal
# ============================================================================
def conferir_nomes(nomes, permitidos=None):
    out = []
    for nm in nomes:
        nm = " ".join(nm.split())
        cod = efeito_do_nome(nm)
        if permitidos is not None and cod not in permitidos:
            raise SystemExit(f"--nomes-v2: '{nm}' não é C06, C05 nem C07 (Meu amigo secreto, Meu 2027 vai ser, "
                             "Simpatia da Virada)")
        if cod is None:
            print(f"  aviso: não reconheci o efeito de '{nm}'; vai sem ícone (estrelinha no lugar)", file=sys.stderr)
        out.append(nm)
    if not out:
        raise SystemExit("precisa de pelo menos 1 nome")
    if len(set(out)) != len(out):
        raise SystemExit("nome repetido")
    return out


def salvar_txt(caminho, texto):
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(texto + "\n")


def renderizar_v1(pasta, nomes, aba):
    cod = "G-V1-aba" if aba else "G-V1"
    v = video_v1(nomes, aba)
    info = render_det(v, os.path.join(pasta, f"{cod}.mp4"))
    q, kb = r.salvar_jpg(capa_v1(), os.path.join(pasta, "G-V1-capa.jpg"), max_kb=300)
    salvar_txt(os.path.join(pasta, f"{cod}-legenda.txt"), legenda_v1(aba))
    return cod, info, kb


def renderizar_v2(pasta, nomes):
    v = video_v2(nomes)
    info = render_det(v, os.path.join(pasta, "G-V2.mp4"))
    q, kb = r.salvar_jpg(capa_v2(nomes), os.path.join(pasta, "G-V2-capa.jpg"), max_kb=300)
    salvar_txt(os.path.join(pasta, "G-V2-legenda.txt"), legenda_v2(nomes))
    return "G-V2", info, kb


def resumo(info, kb):
    return {k: info[k] for k in ("duracao_s", "tamanho_bytes", "tamanho_mb", "codecs", "lufs", "pico_dbtp",
                                 "ganho_audio_db", "teto_kbps", "avisos_zona", "md5", "tempo_render_s")} | {
        "video": info["video"], "audio": info["audio"], "capa_kb": round(kb, 1)}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Peças gerais G-V1 (tutorial) e G-V2 (fim de ano)")
    ap.add_argument("--nomes", nargs="+", default=NOMES_V1, metavar="NOME",
                    help="filtros já aprovados, na ordem do fim do G-V1 (padrão: %(default)s)")
    ap.add_argument("--aba", choices=["nao", "sim", "ambas"], default="nao",
                    help="3º passo do G-V1: nao = 'toca no nome no vídeo de quem usou' (G-V1.mp4), sim = 'aba de efeitos' "
                         "(G-V1-aba.mp4), ambas = as duas (padrão: nao)")
    ap.add_argument("--nomes-v2", nargs="+", default=NOMES_V2, metavar="NOME",
                    help="filtros de fim de ano aprovados (C06, C05, C07; padrão: os 3)")
    ap.add_argument("--so", choices=["G-V1", "G-V2", "previa"], help="só uma peça (ou só a prévia)")
    ap.add_argument("--pasta", default=AQUI, help="pasta de saída (padrão: a pasta deste arquivo)")
    ap.add_argument("--rapido", metavar="DIR", help="só pranchas rápidas da linha do tempo, sem MP4")
    a = ap.parse_args(argv)
    nomes = conferir_nomes(a.nomes)
    nomes_v2 = conferir_nomes(a.nomes_v2, permitidos=set(ORDEM_V2))
    # a ordem do G-V2 segue o calendário (C06, C05, C07), seja qual for a ordem passada
    nomes_v2 = sorted(nomes_v2, key=lambda nm: ORDEM_V2.index(efeito_do_nome(nm)))
    abas = {"nao": [False], "sim": [True], "ambas": [False, True]}[a.aba]
    if a.rapido:
        os.makedirs(a.rapido, exist_ok=True)
        for aba in abas:
            video_v1(nomes, aba).prancha(os.path.join(a.rapido, f"G-V1{'-aba' if aba else ''}_rapida.png"), n=20,
                                         colunas=5)
        video_v2(nomes_v2).prancha(os.path.join(a.rapido, "G-V2_rapida.png"), n=20, colunas=5)
        capa_v1().save(os.path.join(a.rapido, "G-V1_capa.png"))
        capa_v2(nomes_v2).save(os.path.join(a.rapido, "G-V2_capa.png"))
        print("ok", a.rapido)
        return
    os.makedirs(a.pasta, exist_ok=True)
    res = {}
    if a.so in (None, "G-V1"):
        for aba in abas:
            cod, info, kb = renderizar_v1(a.pasta, nomes, aba)
            res[cod] = resumo(info, kb)
    if a.so in (None, "G-V2"):
        cod, info, kb = renderizar_v2(a.pasta, nomes_v2)
        res[cod] = resumo(info, kb)
    if a.so in (None, "previa"):
        mp4s = [(c, os.path.join(a.pasta, f"{c}.mp4")) for c in ("G-V1", "G-V1-aba", "G-V2")]
        mp4s = [(c, p) for c, p in mp4s if os.path.exists(p)]
        if mp4s:
            res["previa"] = previa(mp4s, os.path.join(a.pasta, "previa-videos.png"))
    res["comentarios"] = {"G-V1": comentario(nomes, False, "Qual você vai usar primeiro?"),
                          "G-V1-aba": comentario(nomes, True, "Qual você vai usar primeiro?"),
                          "G-V2": comentario(nomes_v2, False, "Qual combina com você?")}
    res["comentarios_caracteres"] = {k: len(t) for k, t in res["comentarios"].items()}
    total = sum(os.path.getsize(os.path.join(a.pasta, f)) for f in os.listdir(a.pasta)
                if os.path.isfile(os.path.join(a.pasta, f)))
    res["total_pasta_mb"] = round(total / 1024 / 1024, 2)
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
