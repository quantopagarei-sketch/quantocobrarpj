#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_videos.py: vídeos do C05 "Meu 2027 vai ser" (peças N), capas, legendas e o kit da peça M.

Usa a biblioteca da equipe: tiktok-efeitos/videos/lib/render.py (não editar a biblioteca daqui).
Usa os PNGs do efeito sem mexer neles (assets/ só é lido). As artes do efeito são brancas (o template
pinta com cor sorteada); aqui elas são tingidas na memória.
Tudo é determinístico: rodar de novo gera os mesmos arquivos (x264 em 1 thread; ver renderizar_deterministico).

Rodar (da pasta que for):
    python3 render_videos.py                       # tudo: C05-V1, C05-V2, C05-V3, capas, legendas, kit M1, prévia
    python3 render_videos.py --so C05-V1           # só uma peça (mp4 + capa + legenda)
    python3 render_videos.py --so kit              # só o kit da C05-M1
    python3 render_videos.py --so previa           # só a prancha de prévia
    python3 render_videos.py --rapido DIR          # pranchas rápidas da linha do tempo (sem mp4), em DIR
    python3 render_videos.py --hint toque          # V1 com "Toca na tela 👆" (se o hint publicado for de toque)
    python3 render_videos.py --bolhas 4            # versão com a 4ª bolha CARRO (só se o efeito sair com 4)
    python3 render_videos.py --bolhas carro        # 3 bolhas com CARRO no lugar de FUTEBOL (guia, Parte 17.1)
    python3 render_videos.py --nome "Meu 2027 vai ser"   # nome publicado, se sair diferente

Saída (nesta pasta):
    C05-V1.mp4  C05-V2.mp4  C05-V3.mp4
    C05-Vn-capa.jpg  C05-Vn-legenda.txt
    kit-C05-M1/  (ganchos, final.png, assinatura.wav, capas e legendas: versão biquinho e versão toque)
    previa-videos.png
"""
from __future__ import annotations

import argparse
import functools
import json
import math
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time
import wave

sys.dont_write_bytecode = True   # não deixa __pycache__ na pasta da biblioteca

AQUI = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.normpath(os.path.join(AQUI, "..", "..", "videos", "lib"))
sys.path.insert(0, LIB)
import render as r  # noqa: E402

import numpy as np  # noqa: E402
from PIL import Image, ImageDraw, ImageFilter  # noqa: E402

# ============================================================================
# Caminhos e dados do efeito
# ============================================================================
ASSETS = os.path.normpath(os.path.join(AQUI, "..", "assets"))
TEXTOS_JSON = os.path.normpath(os.path.join(AQUI, "..", "textos.json"))
SIMBOLO = os.path.normpath(os.path.join(AQUI, "..", "..", "videos", "perfil", "simbolo_transparente.png"))
TITULO = os.path.join(ASSETS, "titulo.png")
BOLHA_DIR = os.path.join(ASSETS, "variantes", "bolha_inteira")

NOME_PADRAO = "Meu 2027 vai ser"     # nome exato do textos.md (sem reticências)

CX = 520                 # miolo um pouco à esquerda: longe da coluna de botões do TikTok (x > 940)
AMARELO = "#FFD43B"
ESCURO = "#1B1D24"
COR = {"amor": "#FF6FB1", "grana": "#FFD43B", "futebol": "#4FE3F0", "carro": "#B794FF"}
CATS3 = ["amor", "grana", "futebol"]
CATS3_CARRO = ["amor", "grana", "carro"]     # guia de montagem, Parte 17.1 (CARRO no lugar de FUTEBOL)
CATS4 = ["amor", "grana", "futebol", "carro"]


def categorias(nb):
    """Bolhas da versão publicada: 3 (padrão), 4 (com CARRO) ou "carro" (3, com CARRO no lugar de FUTEBOL)."""
    return {3: CATS3, 4: CATS4, "carro": CATS3_CARRO}[nb]

# Resultados de cada peça (arquivo respostas_<bolha>/<bolha>_NN.png). CARRO só entra com --bolhas 4 ou carro.
RES_V1 = {"amor": 2, "grana": 2, "futebol": 1, "carro": 1}
RES_V2_R1 = {"amor": 7, "grana": 5, "futebol": 2, "carro": 5}
RES_V2_R2 = {"amor": 5, "grana": 8, "futebol": 4, "carro": 2}
RES_V3 = {"amor": 8, "grana": 3, "futebol": 6, "carro": 3}


def resposta_png(cat, n):
    return os.path.join(ASSETS, f"respostas_{cat}", f"{cat}_{n:02d}.png")


@functools.lru_cache(maxsize=1)
def textos():
    with open(TEXTOS_JSON, encoding="utf-8") as f:
        j = json.load(f)
    return {os.path.basename(x["arquivo"]): (x["texto"], x["emoji"]) for x in j["resultados"]}


def texto_resposta(cat, n):
    return textos()[f"{cat}_{n:02d}.png"][0]


def emoji_resposta(cat, n):
    return textos()[f"{cat}_{n:02d}.png"][1]


# ============================================================================
# Arte: tingir as artes brancas (na memória), bolha, linha de resultado, ícones
# ============================================================================
_ARTE = {}     # cache próprio (as imagens criadas aqui ficam vivas: a biblioteca guarda referência por id)


def _guardar(chave, img):
    _ARTE[chave] = img
    return img


def tingir(img, cor):
    """Arte branca -> mesma arte na cor dada (mantém a transparência)."""
    im = r.carregar(img)
    c = r.rgb(cor)
    a = np.asarray(im, dtype=np.float32)
    out = np.empty_like(a)
    for i in range(3):
        out[..., i] = a[..., i] / 255.0 * c[i]
    out[..., 3] = a[..., 3]
    return Image.fromarray(out.round().astype(np.uint8), "RGBA")


def bolha(cat):
    """Bolha do efeito (variantes/bolha_inteira) tingida: aro e brilho na cor da bolha, rótulo em branco.
    O rótulo é separado comparando bolha_inteira_<cat> com bolha_vazia (mesmo desenho, sem rótulo)."""
    k = ("bolha", cat)
    if k in _ARTE:
        return _ARTE[k]
    cheia = np.asarray(r.carregar(os.path.join(BOLHA_DIR, f"bolha_inteira_{cat}.png")), dtype=np.float32)
    vazia = np.asarray(r.carregar(os.path.join(BOLHA_DIR, "bolha_vazia.png")), dtype=np.float32)
    a_rot = np.clip(cheia[..., 3] - vazia[..., 3], 0, 255)
    base = tingir(Image.fromarray(vazia.astype(np.uint8), "RGBA"), COR[cat])
    # deixa o "vidro" da bolha um pouco mais cheio de cor (fica bonito no fundo escuro)
    b = np.asarray(base, dtype=np.float32).copy()
    b[..., 3] = np.clip(b[..., 3] * 1.25, 0, 255)
    base = Image.fromarray(b.round().astype(np.uint8), "RGBA")
    rot = np.zeros_like(cheia)
    rot[..., :3] = 255
    rot[..., 3] = a_rot
    rot_img = Image.fromarray(rot.round().astype(np.uint8), "RGBA")
    # contorno escuro fininho no rótulo, para ler bem sobre o vidro colorido
    sombra = Image.new("RGBA", rot_img.size, (20, 16, 50, 0))
    sa = rot_img.getchannel("A").filter(ImageFilter.MaxFilter(5))
    sombra.putalpha(sa.point(lambda v: int(v * 0.55)))
    out = Image.alpha_composite(base, sombra)
    out = Image.alpha_composite(out, rot_img)
    return _guardar(k, out)


def bolha_fantasma(cat):
    """Bolha vazia tingida (sem rótulo): a 'próxima bolha' se formando depois do estouro."""
    k = ("fantasma", cat)
    if k in _ARTE:
        return _ARTE[k]
    return _guardar(k, tingir(os.path.join(BOLHA_DIR, "bolha_vazia.png"), COR[cat]))


@functools.lru_cache(maxsize=1)
def geometria_bolha():
    """Centro e raio do aro da bolha dentro do PNG de 512 px (medido no alfa de bolha_vazia)."""
    a = np.asarray(r.carregar(os.path.join(BOLHA_DIR, "bolha_vazia.png")))[..., 3]
    # o aro principal ocupa quase todo o PNG; as bolhinhas ficam no canto de cima à direita.
    # Linha do meio (y = 256): pega a extensão do aro; depois a coluna do centro dá a altura.
    xs_m = np.nonzero(a[256] > 200)[0]
    cx = 0.5 * (xs_m.min() + xs_m.max())
    raio = 0.5 * (xs_m.max() - xs_m.min())
    ys_c = np.nonzero(a[:, int(cx)] > 200)[0]
    cy = 0.5 * (ys_c.min() + ys_c.max())
    return float(cx), float(cy), float(raio)


def icone(cat):
    """Só o ícone (coração, moeda, bola, carro) do rótulo bolha_<cat>.png, em azul-noite."""
    k = ("icone", cat)
    if k in _ARTE:
        return _ARTE[k]
    im = r.carregar(os.path.join(ASSETS, f"bolha_{cat}.png"))
    a = np.asarray(im)[..., 3]
    linhas = np.nonzero((a > 30).any(axis=1))[0]
    y0 = linhas.min()
    y = y0
    while y < a.shape[0] and (a[y] > 30).any():   # primeiro bloco de cima = ícone
        y += 1
    sub = im.crop((0, y0, im.width, y))
    bb = sub.getchannel("A").getbbox()
    ic = sub.crop(bb)
    return _guardar(k, tingir(ic, "#1A1440"))


def linha_resultado(cat, n, largura, altura):
    """Pílula de resultado: disco colorido com o ícone + a resposta do efeito (PNG) tingida na cor da bolha."""
    k = ("linha", cat, n, largura, altura)
    if k in _ARTE:
        return _ARTE[k]
    S = 2
    W_, H_ = largura * S, altura * S
    pil = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
    d = ImageDraw.Draw(pil)
    cor = r.rgba(COR[cat])
    d.rounded_rectangle([3 * S, 3 * S, W_ - 3 * S, H_ - 3 * S], radius=int(altura * 0.5 * S),
                        fill=(16, 14, 46, 236), outline=cor, width=5 * S)
    pil = pil.resize((largura, altura), Image.LANCZOS)
    # disco + ícone
    dd = int(altura * 0.74)
    disco = Image.new("RGBA", (dd * S, dd * S), (0, 0, 0, 0))
    ImageDraw.Draw(disco).ellipse([0, 0, dd * S - 1, dd * S - 1], fill=cor)
    disco = disco.resize((dd, dd), Image.LANCZOS)
    ic = icone(cat)
    k_ic = (dd * 0.56) / max(ic.width, ic.height)
    ic2 = ic.resize((max(1, int(ic.width * k_ic)), max(1, int(ic.height * k_ic))), Image.LANCZOS)
    disco.alpha_composite(ic2, ((dd - ic2.width) // 2, (dd - ic2.height) // 2))
    x_disco = int(altura * 0.13)
    pil.alpha_composite(disco, (x_disco, (altura - dd) // 2))
    # resposta (PNG 512x128 do efeito), recortada na tinta e ampliada
    resp = r.carregar(resposta_png(cat, n))
    bb = resp.getchannel("A").getbbox()
    resp = resp.crop(bb)
    # emoji da resposta (o mesmo do textos.json), na ponta direita
    em = r.emoji_img(emoji_resposta(cat, n), int(altura * 0.50))
    x_em = largura - int(altura * 0.16) - em.width
    pil.alpha_composite(em, (x_em, (altura - em.height) // 2))
    area_x0 = x_disco + dd + int(altura * 0.10)
    area_w = x_em - int(altura * 0.10) - area_x0
    area_h = int(altura * 0.80)
    esc = min(area_w / resp.width, area_h / resp.height)
    rw, rh = int(round(resp.width * esc)), int(round(resp.height * esc))
    resp2 = r._redimensionar(resp, (rw, rh)) if esc > 1 else resp.resize((rw, rh), Image.LANCZOS)
    resp2 = tingir(resp2, r.misturar(COR[cat], "#FFFFFF", 0.18)[:3])
    pil.alpha_composite(resp2, (area_x0 + (area_w - rw) // 2, (altura - rh) // 2))
    return _guardar(k, pil)


def titulo_img():
    k = ("titulo",)
    if k in _ARTE:
        return _ARTE[k]
    t = r.carregar(TITULO)
    # brilho amarelo bem leve nas estrelinhas não dá para separar; título branco com sombra suave
    sombra = Image.new("RGBA", t.size, (10, 8, 40, 0))
    sa = t.getchannel("A").filter(ImageFilter.GaussianBlur(6))
    sombra.putalpha(sa.point(lambda v: int(v * 0.7)))
    out = Image.alpha_composite(sombra, t)
    return _guardar(k, out)


# ============================================================================
# Layout (quadro 1080x1920; zona segura x 60–940, y 220–1500)
# ============================================================================
LEGENDA_Y = 338          # faixa de texto de cima (gancho, instrução, "Resumindo")
TITULO_Y = 570
TITULO_ESC = 0.56
MEIO_Y = 1165            # carinha / árvore / relógio / contagem antes das respostas


def layout(nb):
    """Posições das bolhas (centro do PNG), escala, fileiras de resultado e a vaga de baixo (carinha)."""
    if nb == 4:
        esc = 0.36
        bol = [(210, 815), (400, 778), (640, 778), (830, 815)]
        lh, gap, y1 = 124, 10, 988
    else:
        esc = 0.46
        bol = [(270, 815), (520, 778), (770, 815)]
        lh, gap, y1 = 156, 12, 1012
    filas = [y1 + i * (lh + gap) for i in range(len(categorias(nb)))]
    return dict(esc=esc, bolhas=bol, lh=lh, filas=filas, lw=800)


def centro_aro(pos, esc):
    gx, gy, raio = geometria_bolha()
    return pos[0] + (gx - 256) * esc, pos[1] + (gy - 256) * esc, raio * esc


# ============================================================================
# Som (assinatura do C05: estouro de bolha + brilho), feito aqui com numpy
# ============================================================================
SR = r.SR


@functools.lru_cache(maxsize=16)
def som_estouro(semente=0, tom=1.0):
    """Estouro de bolha: 'plop' que sobe de tom + estalo curto + borrifo."""
    dur = 0.2
    t = np.arange(int(dur * SR)) / SR
    rng = np.random.default_rng(700 + semente)
    f = (240 + 900 * (1 - np.exp(-t / 0.010))) * tom
    plop = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.040) * np.minimum(1, t / 0.0008)
    ruido = rng.standard_normal(len(t))
    estalo = r._passa_baixa(np.diff(ruido, prepend=0.0) * np.exp(-t / 0.0016), 7000.0) * 1.1   # sem pico entre amostras
    agudo = ruido - r._passa_baixa(ruido, 2500.0)
    borrifo = agudo * np.exp(-np.maximum(0, t - 0.004) / 0.028) * (t >= 0.004) * 0.28
    s = plop + estalo + borrifo
    return (s / (np.max(np.abs(s)) + 1e-9) * 0.9).astype(np.float32)


@functools.lru_cache(maxsize=16)
def som_brilho(semente=0, notas=6, base=1568.0, passo=0.045, decaimento=0.22):
    """Brilho: notas curtas e agudas subindo (escala pentatônica), indo de um lado para o outro. Estéreo."""
    escala = [1.0, 9 / 8, 5 / 4, 3 / 2, 5 / 3, 2.0, 9 / 4, 5 / 2]
    dur = passo * notas + decaimento * 3
    n = int(dur * SR)
    out = np.zeros((n, 2))
    rng = np.random.default_rng(900 + semente)
    for k in range(notas):
        f = base * escala[k % len(escala)] * (2 if k >= len(escala) else 1) * (1 + rng.uniform(-0.004, 0.004))
        t = np.arange(int(decaimento * 3 * SR)) / SR
        s = (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / 0.03))
        s *= np.exp(-t / decaimento) * np.minimum(1, t / 0.002) * (0.75 + 0.25 * k / notas)
        i0 = int(k * passo * SR)
        m = min(len(s), n - i0)
        pan = -0.6 + 1.2 * k / max(1, notas - 1)
        a = (pan + 1) * np.pi / 4
        out[i0:i0 + m, 0] += s[:m] * math.cos(a)
        out[i0:i0 + m, 1] += s[:m] * math.sin(a)
    return (out / (np.max(np.abs(out)) + 1e-9) * 0.8).astype(np.float32)


@functools.lru_cache(maxsize=8)
def som_sininho(semente=0, batidas=5):
    """Sininhos de Natal (guizos): batidas metálicas curtas e um pouco desencontradas. Estéreo."""
    rng = np.random.default_rng(1200 + semente)
    dur = 0.55
    n = int(dur * SR)
    out = np.zeros((n, 2))
    parciais = [(1.0, 1.0), (1.47, 0.6), (2.09, 0.42), (2.56, 0.3), (3.12, 0.22)]
    for k in range(batidas):
        t0 = k * 0.075 + rng.uniform(0, 0.02)
        f0 = rng.uniform(2700, 3400)
        t = np.arange(int(0.3 * SR)) / SR
        s = sum(a * np.sin(2 * np.pi * f0 * m * t + rng.uniform(0, 6.28)) * np.exp(-t / (0.09 / m ** 0.5))
                for m, a in parciais)
        s += 0.2 * rng.standard_normal(len(t)) * np.exp(-t / 0.006)
        s *= np.minimum(1, t / 0.001) * (1 - 0.12 * k)
        i0 = int(t0 * SR)
        m = min(len(s), n - i0)
        pan = rng.uniform(-0.5, 0.5)
        a = (pan + 1) * np.pi / 4
        out[i0:i0 + m, 0] += s[:m] * math.cos(a)
        out[i0:i0 + m, 1] += s[:m] * math.sin(a)
    return (out / (np.max(np.abs(out)) + 1e-9) * 0.8).astype(np.float32)


def assinatura(v, t, volume=1.0, semente=0):
    """Assinatura sonora do C05: estouro + brilho."""
    v.som(som_estouro(semente, 0.9), t, 0.55 * volume)
    v.som(som_brilho(semente, 7, 1760.0), t + 0.07, 0.30 * volume)


def estouro(v, t, semente=0, tom=1.0):
    v.som(som_estouro(semente % 6, tom), t, 0.6)
    v.som(som_brilho(semente % 6, 5, 1568.0 * tom, 0.04, 0.18), t + 0.06, 0.20)


# ============================================================================
# Fundo: azul-noite -> roxo, padrão de estrelas e estrelinhas piscando
# ============================================================================
class FundoC05:
    def __init__(self, variante=0, n_pisca=34, cor_estrela=(255, 255, 255, 24)):
        cores = [
            ["#0A0F2E", "#151B4C", "#2A1A63", "#43207A", "#2A1A63", "#151B4C"],
            ["#0B0F2C", "#1A1A4E", "#331B66", "#4A1F74", "#331B66", "#1A1A4E"],
            ["#0A0D2A", "#1B1550", "#3A1A6C", "#5A1F7C", "#3A1A6C", "#1B1550"],
        ][variante % 3]
        vel = [(6, 24), (-8, 22), (0, 30)][variante % 3]
        self.pad = r.Padrao("estrelas", cor_forma=cor_estrela, tamanho=210, velocidade=vel,
                            fundo=r.DegradeAnimado(cores, angulo=100, velocidade=0.035, giro=8.0))
        rng = random.Random(2027 + variante)
        self.sp = {tam: r._redimensionar(r.sprite_brilho("#FFFFFF", 160), (tam, tam)) for tam in (14, 20, 28)}
        self.estrelas = [(rng.uniform(20, 1060), rng.uniform(20, 1900), rng.choice((14, 14, 20, 20, 28)),
                          rng.uniform(0.25, 0.7), rng.uniform(0, 1)) for _ in range(n_pisca)]

    def quadro(self, t):
        im = self.pad.quadro(t)
        for x, y, tam, f, fase in self.estrelas:
            a = max(0.0, math.sin(2 * math.pi * (t * f + fase))) ** 2
            if a < 0.05:
                continue
            sp = self.sp[tam]
            r.colar(im, sp, (x, y), 1.0, 0, 0.25 + 0.75 * a)
        return im


# ============================================================================
# Peças de tela
# ============================================================================
def cabeca(v, trocas, ini, fim, de, para=None, t_mov=None, dur_mov=0.5, entrada=True, z=13, nome="carinha"):
    """No lugar da cabeça da pessoa, uma carinha emoji (nada de rosto ou silhueta humana).
    trocas: [(t, emoji)]. de/para: (x, y, altura). Se 'para', ela desce e diminui a partir de t_mov."""
    tam0 = de[2]
    imgs = {e: r.emoji_img(e, tam0) for _, e in trocas}
    tempos = [t for t, _ in trocas]

    def f(canvas, tl, t):
        k = max(0, sum(1 for tt in tempos if tt <= t) - 1)
        e = trocas[k][1]
        t_troca = trocas[k][0]
        x, y, h = de
        if para and t_mov is not None:
            p = r.progresso(t, t_mov, dur_mov, "in_out_cubic")
            x, y, h = r.lerp(de[0], para[0], p), r.lerp(de[1], para[1], p), r.lerp(de[2], para[2], p)
        s = h / tam0
        if entrada and tl < 0.3 and ini > 0:
            s *= 0.25 + 0.75 * r.ease_out_back(r.limitar(tl / 0.3), 2.0)
        if k > 0:
            s *= 1 + r.quique(t - t_troca, 0.20, 2.4, 6.0)
        if fim is not None and t > fim - 0.2:
            s *= max(0.01, (fim - t) / 0.2)
        dy = 8 * math.sin(2 * math.pi * t / 2.4)
        r.colar(canvas, imgs[e], (x, y + dy), s)
        if v._registrando:
            v._registrar(nome, r.caixa_nominal(imgs[e], (x, y), h / tam0), t)
    for t, _ in trocas[1:]:
        v.som("pop", t + 0.01, 0.35)
    v.adicionar(f, ini, fim, z)


def titulo(v, ini, fim, entrada=None):
    img = titulo_img()
    v.imagem(img, ini, fim, centro=(CX, TITULO_Y), escala=TITULO_ESC, entrada=entrada, saida="fade", ocioso="flutuar",
             som=False, z=10, nome="título MEU 2027 VAI SER…")


def gancho(v, texto, ini, fim, tamanho=88, saida="pop", entrada=None, nome="gancho", y=LEGENDA_Y, som=True):
    v.texto(texto, ini, fim, centro=(CX, y), tamanho=tamanho, max_linhas=2, largura_max=840, entrada=entrada,
            saida=saida, ocioso="pulsar", som=som, z=60, nome=nome)


def montar_bolhas(v, cats, lay, rodadas, fim_filas):
    """Bolhas flutuando, estouro e as fileiras de resultado.
    rodadas: lista de dicts {"aparece": t ou None, "estouros": {cat: (n_resposta, t_estouro)}, "sai": t ou None}."""
    esc = lay["esc"]
    pos = {c: lay["bolhas"][i] for i, c in enumerate(cats)}
    fase = {c: i * 0.37 for i, c in enumerate(cats)}
    luz = {c: r.sprite_luz(int(170 * esc / 0.42), COR[c]) for c in cats}
    for ri, rod in enumerate(rodadas):
        ap = rod.get("aparece")
        for i, c in enumerate(cats):
            n, tp = rod["estouros"][c]
            img = bolha(c)
            x0, y0 = pos[c]

            def fb(canvas, tl, t, c=c, img=img, x0=x0, y0=y0, tp=tp, ap=ap):
                ph = fase[c]
                dy = 11 * math.sin(2 * math.pi * (t / 2.5 + ph))
                dx = 4 * math.sin(2 * math.pi * (t / 3.3 + ph))
                s = esc * (1 + 0.02 * math.sin(2 * math.pi * (t / 1.7 + ph)))
                if ap is not None and t - ap < 0.35:
                    s *= max(0.02, r.ease_out_back(r.limitar((t - ap) / 0.35), 2.0))
                u = (t - (tp - 0.26)) / 0.26
                if 0 <= u <= 1:      # treme e incha antes de estourar
                    s *= 1 + 0.13 * u ** 1.5 + 0.035 * math.sin(2 * math.pi * 3.5 * u)
                gx, gy, _ = centro_aro((x0 + dx, y0 + dy), s)
                r.colar(canvas, luz[c], (gx, gy), 1.0 * s / esc, 0, 0.30)
                r.colar(canvas, img, (x0 + dx, y0 + dy), s)
                if v._registrando:
                    v._registrar(f"bolha {c}", r.caixa_nominal(img, (x0, y0), esc), t)
            v.adicionar(fb, ap if ap is not None else 0.0, tp, 11)
            # estouro
            gx, gy, raio = centro_aro((x0, y0), esc)
            estouro(v, tp, semente=3 * ri + i, tom=[1.0, 1.12, 0.9, 1.05][i % 4])
            v.adicionar(_desenho_estouro(c, (gx, gy), raio, 31 * ri + i), tp, tp + 0.6, 16)
            v.brilhos(tp + 0.03, (gx, gy), raio=(raio * 1.1, raio * 1.0), quantidade=7, duracao=0.9,
                      tamanho=(22, 46), z=17)
            # fantasma: a bolha se formando de novo, bem clarinha, até a próxima rodada (ou o fim)
            prox = rodadas[ri + 1].get("aparece") if ri + 1 < len(rodadas) else None
            fim_f = prox if prox is not None else fim_filas
            if fim_f - (tp + 0.45) > 0.3:
                v.adicionar(_desenho_fantasma(c, (x0, y0), esc, fase[c], tp + 0.45, fim_f), tp + 0.45, fim_f, 9)
            # fileira de resultado: aparece na sua vaga (pop + clarão), sem cruzar as outras
            fila = linha_resultado(c, n, lay["lw"], lay["lh"])
            yf = lay["filas"][i]
            sai = rod.get("sai")
            fim = (sai + 0.3) if sai is not None else fim_filas
            v.som("pop", tp + 0.10, 0.35)
            v.adicionar(_desenho_fila(fila, (CX, yf), sai, f"resultado {c} {n:02d}"), tp + 0.06, fim, 14)


def _desenho_estouro(cat, centro, raio, semente):
    """Anel que se abre + gotinhas que voam (desenhado em 2x e reduzido, para ficar liso)."""
    rng = random.Random(4000 + semente)
    cor = r.rgb(COR[cat])
    gotas = []
    for k in range(16):
        ang = 2 * math.pi * k / 16 + rng.uniform(-0.15, 0.15)
        gotas.append((ang, rng.uniform(1.25, 1.9), rng.uniform(5, 11), k % 3 == 0))
    R = int(raio * 2.2)
    S = 2

    def f(canvas, tl, t):
        if tl > 0.6:
            return
        ov = Image.new("RGBA", (2 * R * S, 2 * R * S), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        c0 = R * S
        u = r.limitar(tl / 0.32)
        if u < 1:
            rr = raio * (1.0 + 0.6 * r.ease_out_cubic(u)) * S
            w = max(2, int((10 - 8 * u) * S))
            a = int(255 * (1 - u) ** 1.3)
            d.ellipse([c0 - rr, c0 - rr, c0 + rr, c0 + rr], outline=cor + (a,), width=w)
        p = r.limitar(tl / 0.55)
        dist = r.ease_out_cubic(p)
        a = int(255 * (1 - r.limitar((p - 0.45) / 0.55)))
        for ang, alcance, tam, branca in gotas:
            dd = raio * (0.85 + (alcance - 0.85) * dist) * S
            x, y = c0 + math.cos(ang) * dd, c0 + math.sin(ang) * dd + 60 * p * p * S
            tt = tam * (1 - 0.6 * p) * S
            d.ellipse([x - tt, y - tt, x + tt, y + tt], fill=((255, 255, 255) if branca else cor) + (a,))
        ov = ov.resize((2 * R, 2 * R), Image.LANCZOS)
        r._pintar(canvas, ov, int(centro[0] - R), int(centro[1] - R))
    return f


def _desenho_fila(fila, pos, sai, nome):
    flash = Image.new("RGBA", fila.size, (255, 255, 255, 0))
    flash.putalpha(fila.getchannel("A"))

    def f(canvas, tl, t):
        p = r.limitar(tl / 0.30)
        x, y = pos
        s = 0.55 + 0.45 * r.ease_out_back(p, 2.0) if p < 1 else 1 + r.quique(tl - 0.30, 0.04, 2.6, 7.0)
        op = r.limitar(tl / 0.08)
        if sai is not None and t > sai:
            q = r.limitar((t - sai) / 0.28)
            x -= r.W * r.ease_in_cubic(q)
            op *= 1 - q
        r.colar(canvas, fila, (x, y), s, 0, op)
        if 0.05 < tl < 0.40:       # clarão rápido na pílula quando ela chega
            a = 0.55 * (1 - (tl - 0.05) / 0.35)
            r.colar(canvas, flash, (x, y), s, 0, a)
        if p >= 1 and (sai is None or t < sai) and _VID[0] is not None and _VID[0]._registrando:
            _VID[0]._registrar(nome, r.caixa_nominal(fila, pos, 1.0), t)
    return f


def _desenho_fantasma(cat, pos, esc, fase, t0, t1):
    img = bolha_fantasma(cat)

    def f(canvas, tl, t):
        a = 0.20 * r.limitar(tl / 0.8) * r.limitar((t1 - t) / 0.2)
        if a <= 0.01:
            return
        dy = 11 * math.sin(2 * math.pi * (t / 2.5 + fase))
        s = esc * (0.55 + 0.30 * r.ease_out_cubic(r.limitar(tl / 1.2)))
        r.colar(canvas, img, (pos[0], pos[1] + dy), s, 0, a)
    return f


_VID = [None]     # vídeo em montagem (para a checagem de zona segura das fileiras)


def cortina(v, bg, t0, fim, z=52):
    """O cartão final sobe de baixo para cima, cobrindo tudo (inclusive o confete)."""
    def f(canvas, tl, t):
        p = r.progresso(tl, 0, 0.32, "out_cubic")
        y0 = int(round(r.H * (1 - p)))
        if y0 >= r.H:
            return
        fundo = bg.quadro(t)
        canvas.paste(fundo.crop((0, y0, r.W, r.H)), (0, y0))
        if p < 1:
            ImageDraw.Draw(canvas).rectangle([0, max(0, y0 - 6), r.W, y0 + 6], fill=r.rgb(AMARELO))
    v.adicionar(f, t0, fim, z)


def cartao_final(v, bg, t0, fim, pergunta, nome_filtro, estatico=False, som=True):
    """CF: símbolo do perfil + 'Procura na lupa 🔎' + nome do filtro em amarelo (1 linha) + pergunta."""
    if not estatico:
        cortina(v, bg, t0, fim)
        if som:
            assinatura(v, t0 + 0.08, 1.0, semente=5)
    e = (lambda d: None) if estatico else (lambda d: "pop")
    dt = (lambda d: t0) if estatico else (lambda d: t0 + d)
    v.imagem(SIMBOLO, dt(0.12), fim, centro=(CX, 600), escala=0.40, entrada=e(0), som=False,
             ocioso="flutuar", z=61, nome="símbolo")
    v.texto("Procura na lupa 🔎", dt(0.22), fim, centro=(CX, 878), tamanho=80, fonte="black",
            entrada=e(0), saida=None, som=False, z=62, nome="lupa")
    v.texto(f"*{nome_filtro}*", dt(0.32), fim, centro=(CX, 1005), tamanho=124, max_linhas=1, largura_max=820,
            contorno=12, entrada=e(0), saida=None, ocioso=None if estatico else "pulsar", som=False, z=62,
            nome="nome do filtro")
    v.texto(pergunta, dt(0.50), fim, centro=(CX, 1170), tamanho=64, fonte="black", cor=ESCURO, contorno=0,
            max_linhas=1, largura_max=820, caixa="#FFFFFF", sombra=(0, 6, 10, 110), entrada=e(0), saida=None,
            som=False, z=62, nome="pergunta")


# --- enfeites de Natal desenhados (C05-V2)
@functools.lru_cache(maxsize=8)
def _sprite_enfeite(cor, comprimento, raio):
    S = 3
    w, h = int(2 * raio + 20), int(comprimento + 2 * raio + 30)
    im = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx = w * S / 2
    d.line([cx, 0, cx, comprimento * S], fill=(235, 225, 200, 170), width=3 * S)
    cy = (comprimento + 12 + raio) * S
    d.rounded_rectangle([cx - 0.32 * raio * S, (comprimento - 2) * S, cx + 0.32 * raio * S, (comprimento + 16) * S],
                        radius=3 * S, fill=(225, 190, 90, 255))
    c = r.rgb(cor)
    d.ellipse([cx - raio * S, cy - raio * S, cx + raio * S, cy + raio * S], fill=c + (255,))
    esc = tuple(int(v * 0.72) for v in c)
    d.arc([cx - raio * S, cy - raio * S, cx + raio * S, cy + raio * S], 20, 160, fill=esc + (255,), width=int(raio * 0.35 * S))
    d.ellipse([cx - raio * 0.55 * S, cy - raio * 0.62 * S, cx - raio * 0.15 * S, cy - raio * 0.22 * S],
              fill=(255, 255, 255, 170))
    d.line([cx - raio * S * 0.95, cy + raio * 0.12 * S, cx + raio * S * 0.95, cy + raio * 0.12 * S],
           fill=(255, 255, 255, 120), width=int(4 * S))
    return im.resize((w, h), Image.LANCZOS)


ENFEITES = [(92, 120, "#E63946", 46), (238, 40, AMARELO, 34), (842, 60, "#4FE3F0", 36), (990, 150, "#FF6FB1", 48)]


def enfeites(v, ini, fim, z=8):
    sps = [(x, _sprite_enfeite(c, comp, raio), i) for i, (x, comp, c, raio) in enumerate(ENFEITES)]

    def f(canvas, tl, t):
        for x, sp, i in sps:
            ang = 5 * math.sin(2 * math.pi * (t / (2.2 + 0.3 * i) + 0.2 * i))
            im = sp.rotate(ang, resample=Image.BICUBIC, expand=True, center=(sp.width / 2, 0))
            r._pintar(canvas, im, int(x - im.width / 2), -4)
    v.adicionar(f, ini, fim, z)


def tic_tac(v, ini, fim, passo=0.5, volume=0.42):
    k = 0
    t = ini
    while t < fim - 1e-6:
        v.som("tique", t, volume, 0.0, freq=2100 if k % 2 == 0 else 1550, semente=k % 5)
        t += passo
        k += 1


# ============================================================================
# As peças N
# ============================================================================
def video_v1(nome, hint="biquinho", nb=3):
    """C05-V1 · 'Estoura a bolha' · 12 s."""
    v = r.Video(12.0, semente=501)
    _VID[0] = v
    cats = categorias(nb)
    lay = layout(nb)
    bg = FundoC05(0)
    v.fundo(bg)
    v.trilha(volume=0.24, bpm=96, progressao=[(41, ""), (45, "m"), (43, ""), (48, "")], ducking=0.5)
    v.som(som_brilho(1, 7, 1318.5), 0.04, 0.22)
    # 0–2 s: gancho + título + bolhas + carinha (tudo no 1º quadro)
    gancho(v, "*Estoura a bolha*\ne vê seu 2027", 0.0, 2.0)
    titulo(v, 0.0, 9.6)
    if nb == 4:
        tps = [3.0, 4.15, 5.3, 6.45]
    else:
        tps = [3.0, 4.5, 6.0]
    est = {c: (RES_V1[c], tps[i]) for i, c in enumerate(cats)}
    montar_bolhas(v, cats, lay, [{"aparece": None, "estouros": est, "sai": None}], 9.6)
    # 2–3 s: instrução (segue o hint publicado)
    if hint == "toque":
        gancho(v, "Toca na *tela* 👆", 2.0, 7.5, tamanho=96, entrada="pop", saida="pop", nome="instrução")
        mid = lay["bolhas"][1]
        v.toque(2.45, centro=(mid[0] + 30, mid[1] + 20))
        trocas = [(0.0, "🤔"), (2.0, "😮")]
    else:
        gancho(v, "Faz *biquinho* 😗", 2.0, 7.5, tamanho=96, entrada="pop", saida="pop", nome="instrução")
        trocas = [(0.0, "🤔"), (2.0, "😗")]
    cabeca(v, trocas, 0.0, tps[0] + 0.02, de=(CX, MEIO_Y, 270))
    # 7,5–9,5 s: "Resumindo"
    gancho(v, "Resumindo:\n*igual 2026* 😂", 7.5, 9.6, tamanho=88, entrada="pop", saida=None, nome="resumindo")
    # 9,5–12 s: cartão final
    cartao_final(v, bg, 9.5, 12.0, "Qual saiu pra você?", nome)
    return v


def video_v2(nome, nb=3):
    """C05-V2 · 'Ceia: cada um vê o seu' · 11 s."""
    v = r.Video(11.0, semente=502)
    _VID[0] = v
    cats = categorias(nb)
    lay = layout(nb)
    bg = FundoC05(1, cor_estrela=(255, 222, 120, 26))
    v.fundo(bg)
    v.trilha(volume=0.24, bpm=100, progressao=[(48, ""), (45, "m"), (41, ""), (43, "")], ducking=0.5)
    v.som(som_sininho(0, 6), 0.03, 0.42)
    enfeites(v, 0.0, 8.3)
    # 0–2 s: gancho + 🎄 + bolhas + enfeites
    gancho(v, "Ceia hoje: cada um\n*vê seu 2027* 🎄", 0.0, 2.0, tamanho=88)
    titulo(v, 0.0, 8.1)
    passo = 0.7 if len(cats) == 3 else 0.55
    r1 = {c: (RES_V2_R1[c], 2.15 + i * passo) for i, c in enumerate(cats)}
    r2 = {c: (RES_V2_R2[c], 5.35 + i * passo) for i, c in enumerate(cats)}
    montar_bolhas(v, cats, lay, [
        {"aparece": None, "estouros": r1, "sai": 4.92},
        {"aparece": 4.98, "estouros": r2, "sai": None},
    ], 8.1)
    cabeca(v, [(0.0, "🎄")], 0.0, 2.17, de=(CX, MEIO_Y, 270), nome="árvore")
    # rodadas
    v.som(som_sininho(1, 4), 2.0, 0.30)
    gancho(v, "*Rodada 1*", 2.0, 4.95, tamanho=104, entrada="pop", saida="pop", nome="rodada 1")
    v.som(som_sininho(2, 4), 5.0, 0.30)
    gancho(v, "*Rodada 2*", 5.0, 8.1, tamanho=104, entrada="pop", saida=None, nome="rodada 2")
    # 8–11 s: cartão final
    v.som(som_sininho(3, 5), 8.05, 0.32)
    cartao_final(v, bg, 8.0, 11.0, "Cada um no seu celular 📱", nome)
    return v


def video_v3(nome, nb=3):
    """C05-V3 · 'Último dia de 2026' · 12 s."""
    v = r.Video(12.0, semente=503)
    _VID[0] = v
    cats = categorias(nb)
    lay = layout(nb)
    bg = FundoC05(2)
    v.fundo(bg)
    v.trilha(volume=0.24, bpm=104, progressao=[(45, "m"), (41, ""), (48, ""), (43, "")], ducking=0.5)
    # 0–2 s: gancho + bolhas + 🕛 (tic-tac)
    gancho(v, "*Último dia:*\nvê seu 2027 agora", 0.0, 8.0, tamanho=88)
    titulo(v, 0.0, 9.6)
    tic_tac(v, 0.0, 2.0)
    v.imagem(r.emoji_img("🕛", 270), 0.0, 2.0, centro=(CX, MEIO_Y), entrada=None, saida="pop", ocioso="balancar",
             som=False, z=13, nome="relógio")
    # 2–4 s: 3, 2, 1, 2027!
    v.contagem(2.0, de=3, dur_cada=0.5, centro=(CX, MEIO_Y), tamanho=330, final="2027!")
    # 4–8 s: estouros com confete
    if nb == 4:
        tps = [4.1, 5.0, 5.9, 6.8]
    else:
        tps = [4.1, 5.3, 6.5]
    est = {c: (RES_V3[c], tps[i]) for i, c in enumerate(cats)}
    montar_bolhas(v, cats, lay, [{"aparece": None, "estouros": est, "sai": None}], 9.6)
    gx_list = [centro_aro(p, lay["esc"]) for p in lay["bolhas"]]
    for i, tp in enumerate(tps):
        gx, gy, _ = gx_list[i]
        v.confete(tp + 0.02, origem=(gx, gy), quantidade=55, duracao=2.6, forca=0.75, z=13)   # atrás das respostas
    # 8–9,5 s
    gancho(v, "Faz hoje e de novo\n*amanhã* 👀", 8.0, 9.6, tamanho=88, entrada="pop", saida=None, nome="convite")
    # 9,5–12 s: cartão final
    cartao_final(v, bg, 9.5, 12.0, "Qual saiu pra você?", nome)
    return v


# ============================================================================
# Capas, legendas e kit da M1
# ============================================================================
def _capa(texto, emoji, rodape, variante, nb=3, natal=False, bolhas_cats=None, tamanho=128):
    """Capa 1080x1920: texto grande, título e bolhas dentro do miolo 3:4 (y 240 a 1680)."""
    v = r.Video(1.0, semente=510 + variante)
    _VID[0] = None
    bg = FundoC05(variante, cor_estrela=(255, 222, 120, 26) if natal else (255, 255, 255, 24))
    v.fundo(bg)
    if natal:
        enfeites(v, 0, None)
    v.texto(texto, 0, None, centro=(CX, 420), tamanho=tamanho, entrada=None, saida=None, contorno=14,
            largura_max=860, max_linhas=2)      # 2 linhas: a biblioteca diminui a letra até caber
    v.imagem(titulo_img(), 0, None, centro=(CX, 760), escala=0.70, entrada=None, som=False)
    cats = bolhas_cats or categorias(nb)
    if len(cats) == 4:
        pos, esc = [(205, 1030), (405, 985), (635, 985), (835, 1030)], 0.38
    else:
        pos, esc = [(270, 1030), (520, 990), (770, 1030)], 0.48
    for c, p in zip(cats, pos):
        gx, gy, _ = centro_aro(p, esc)
        v.imagem(r.sprite_luz(int(170 * esc / 0.42), COR[c]), 0, None, centro=(gx, gy), opacidade=0.3, entrada=None,
                 som=False, z=9)
        v.imagem(bolha(c), 0, None, centro=p, escala=esc, entrada=None, som=False, z=11)
    v.imagem(r.emoji_img(emoji, 200), 0, None, centro=(CX, 1330), entrada=None, som=False)
    if rodape:
        v.texto(rodape, 0, None, centro=(CX, 1545), tamanho=62, fonte="black", entrada=None, saida=None,
                largura_max=860, max_linhas=1)
    return v.quadro(0.0)


def capa_v1(nome, nb=3):
    return _capa("COMO VAI SER\n*SEU 2027?* ✨", "🤔", f"Filtro: *{nome}* 🔎", 0, nb)


def capa_v2(nome, nb=3):
    return _capa("NA CEIA: CADA UM\n*VÊ SEU 2027* 🎄", "🎄", f"Filtro: *{nome}* 🔎", 1, nb, natal=True, tamanho=112)


def capa_v3(nome, nb=3):
    return _capa("ÚLTIMO DIA:\n*VÊ SEU 2027* ✨", "🕛", f"Filtro: *{nome}* 🔎", 2, nb)


def capa_m1(nome, versao, nb=3):
    if versao == "toque":
        return _capa("TOCA E\n*VÊ SEU 2027* ✨", "👆", f"Filtro: *{nome}* 🔎", 0, nb)
    return _capa("FAZ BIQUINHO E\n*VÊ SEU 2027* 😗", "😗", f"Filtro: *{nome}* 🔎", 0, nb, tamanho=120)


HASHTAGS = {
    "C05-V1": "#meu2027vaiser #previsao2027 #2027 #filtro #filtrotiktok",
    "C05-V2": "#meu2027vaiser #ceiadenatal #2027 #filtrotiktok #natal",
    "C05-V3": "#meu2027vaiser #reveillon #anonovo #2027 #filtrotiktok",
    "C05-M1": "#meu2027vaiser #2027 #anonovo #filtro #filtrotiktok",
}


def legendas(nome):
    """Legenda + hashtags (até 5), prontas para colar. 'ou no meu perfil' só depois da conferência da aba."""
    return {
        "C05-V1": f"Estoura as bolhas e vê como vai ser seu 2027 ✨ Qual saiu pra você? Filtro: {nome} 🔎 procura na lupa"
                  f"\n\n{HASHTAGS['C05-V1']}",
        "C05-V2": f"Hoje tem ceia: cada um abre o filtro no seu celular e vê o 2027 🎄 Filtro: {nome} 🔎 procura na lupa"
                  f"\n\n{HASHTAGS['C05-V2']}",
        "C05-V3": f"Último dia de 2026: vê o seu 2027 agora e de novo amanhã 👀 Filtro: {nome} 🔎 procura na lupa"
                  f"\n\n{HASHTAGS['C05-V3']}",
        "C05-M1-biquinho": f"Funciona assim: faz biquinho e as bolhas estouram 😗 Filtro: {nome} 🔎 procura na lupa"
                           f"\n\n{HASHTAGS['C05-M1']}",
        "C05-M1-toque": f"Funciona assim: toca na tela e as bolhas estouram ✨ Filtro: {nome} 🔎 procura na lupa"
                        f"\n\n{HASHTAGS['C05-M1']}",
    }


def _salvar_wav_mono(caminho, x):
    """WAV 16 bits, 44,1 kHz, mono (metade do tamanho; o Clipchamp aceita)."""
    m = np.asarray(x, dtype=np.float64)
    if m.ndim == 2:
        m = m.mean(axis=1)
    m = m / (np.max(np.abs(m)) + 1e-9) * 0.70      # -3 dBFS de pico: folga para o pico entre amostras
    x16 = (np.clip(m, -1, 1) * 32767).astype("<i2")
    with wave.open(caminho, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(np.ascontiguousarray(x16).tobytes())


def _png_transparente(img, centro):
    tela = Image.new("RGBA", (r.W, r.H), (0, 0, 0, 0))
    r.colar(tela, img, centro)
    return tela


def kit_m1(pasta, nome, nb=3):
    """Kit da C05-M1 para o Montador finalizar no Clipchamp (versão biquinho e versão toque)."""
    os.makedirs(pasta, exist_ok=True)
    estilo = dict(tamanho=66, fonte_nome="black", cor=ESCURO, cor_destaque="#C2185B", contorno=0,
                  sombra=(0, 6, 10, 120), largura_max=820, caixa="#FFFFFF", caixa_pad=(36, 22))
    textos_g = {"biquinho": "Funciona assim 👇\n*faz biquinho* 😗", "toque": "Funciona assim 👇\n*toca na tela* 👆"}
    for versao, txt in textos_g.items():
        g = r.texto_img(txt, **estilo)
        # em cima: no lugar do título do efeito pode haver conflito; por isso há a versão de baixo (peito)
        _png_transparente(g, (CX, 330)).save(os.path.join(pasta, f"gancho-{versao}.png"), optimize=True)
        _png_transparente(g, (CX, 1385)).save(os.path.join(pasta, f"gancho-{versao}-baixo.png"), optimize=True)
        r.salvar_jpg(capa_m1(nome, versao, nb), os.path.join(pasta, f"capa-{versao}.jpg"), max_kb=240)
        with open(os.path.join(pasta, f"legenda-{versao}.txt"), "w", encoding="utf-8") as f:
            f.write(legendas(nome)[f"C05-M1-{versao}"] + "\n")
    # final.png: o mesmo cartão final dos vídeos, parado, com a pergunta da M1
    v = r.Video(3.0, semente=520)
    _VID[0] = None
    bg = FundoC05(0)
    v.fundo(bg)
    cartao_final(v, bg, 0.0, None, "Faz hoje e na virada ✨", nome, estatico=True)
    q = v.quadro(1.0).quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
    q.save(os.path.join(pasta, "final.png"), optimize=True)
    # assinatura.wav: trilha 96 bpm + brilho no começo + assinatura (estouro + brilho) quando entra o final (9,5 s)
    a = r.Video(12.0, semente=521)
    a.trilha(volume=0.30, bpm=96, progressao=[(41, ""), (45, "m"), (43, ""), (48, "")], ducking=0.5)
    a.som(som_brilho(1, 7, 1318.5), 0.10, 0.24)
    assinatura(a, 9.5, 1.1, semente=5)
    _salvar_wav_mono(os.path.join(pasta, "assinatura.wav"), a.audio())
    return sorted(os.listdir(pasta))


# ============================================================================
# Prévia (prancha de 6 quadros por vídeo)
# ============================================================================
TEMPOS_PREVIA = {
    "C05-V1": [0.0, 0.5, 2.6, 5.3, 8.4, 11.2],
    "C05-V2": [0.0, 0.5, 3.0, 4.7, 7.7, 10.2],
    "C05-V3": [0.0, 0.5, 3.2, 7.4, 8.9, 11.2],
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
# Render determinístico
# ============================================================================
def renderizar_deterministico(v, saida, kbps, limite_bytes):
    """Igual ao Video.renderizar da biblioteca (mesmos parâmetros do ffmpeg), mas com o x264 em 1 thread.
    Motivo: com várias threads + teto de bitrate (VBV), o x264 gera bytes diferentes a cada rodada, mesmo com os
    quadros idênticos. Em 1 thread o MP4 sai igual byte a byte. Se passar do limite de tamanho, refaz com teto
    15% menor (sem as 2 passadas da biblioteca, que também usam várias threads)."""
    t0 = time.time()
    n = int(round(v.duracao * v.fps))
    tmp = tempfile.mkdtemp(prefix="c05_render_")
    try:
        wav = os.path.join(tmp, "audio.wav")
        # -2 dB de folga: a masterização da biblioteca deixa o pico da amostra em -1,5 dBFS, mas depois do AAC
        # o pico real chegou a -0,2 dBFS aqui (estouros curtos). Com -2 dB fica em -1 dBFS ou menos.
        r.salvar_wav(wav, v.audio() * 0.794)
        while True:
            cmd = ["ffmpeg", "-y", "-v", "error",
                   "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{r.W}x{r.H}", "-r", str(v.fps), "-i", "-",
                   "-i", wav, "-map", "0:v", "-map", "1:a",
                   "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
                   "-c:v", "libx264", "-threads", "1", "-preset", "medium", "-crf", "21",
                   "-maxrate", f"{kbps}k", "-bufsize", f"{2 * kbps}k",
                   "-profile:v", "high", "-level:v", "4.1", "-pix_fmt", "yuv420p", "-g", str(v.fps * 2),
                   "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                   "-c:a", "aac", "-b:a", "128k", "-ar", str(SR), "-ac", "2",
                   "-t", f"{v.duracao:.3f}", "-movflags", "+faststart",
                   "-fflags", "+bitexact", "-flags:v", "+bitexact", "-flags:a", "+bitexact", "-map_metadata", "-1",
                   saida]
            v._zonas = {}            # checagem de zona segura da biblioteca (mesma regra do renderizar)
            v._registrando = True
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
            kbps = int(kbps * 0.85)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    info = r.info_video(saida)
    info["tempo_render_s"] = round(time.time() - t0, 1)
    info["teto_kbps"] = kbps
    info["avisos_zona"] = v.relatorio_zonas()
    print(f"OK {saida}: {info['duracao_s']} s, {info['tamanho_mb']} MB, {info['codecs']}, "
          f"render {info['tempo_render_s']} s", file=sys.stderr)
    for aviso in info["avisos_zona"]:
        print("  AVISO zona segura:", aviso, file=sys.stderr)
    return info


# ============================================================================
# Principal
# ============================================================================
def _video(cod, nome, hint, nb):
    if cod == "C05-V1":
        return video_v1(nome, hint, nb)
    if cod == "C05-V2":
        return video_v2(nome, nb)
    return video_v3(nome, nb)


CAPAS = {"C05-V1": capa_v1, "C05-V2": capa_v2, "C05-V3": capa_v3}
TETO_KBPS = {"C05-V1": 1650, "C05-V2": 1650, "C05-V3": 1650}
LIMITE_BYTES = int(3.0 * 1024 * 1024)    # 4 MB é o limite da ficha; 3 MB deixa a pasta toda abaixo de 12 MB


def renderizar_peca(cod, pasta, nome, hint, nb):
    v = _video(cod, nome, hint, nb)
    mp4 = os.path.join(pasta, f"{cod}.mp4")
    info = renderizar_deterministico(v, mp4, TETO_KBPS[cod], LIMITE_BYTES)
    q, kb = r.salvar_jpg(CAPAS[cod](nome, nb), os.path.join(pasta, f"{cod}-capa.jpg"), max_kb=240)
    with open(os.path.join(pasta, f"{cod}-legenda.txt"), "w", encoding="utf-8") as f:
        f.write(legendas(nome)[cod] + "\n")
    return {"arquivo": os.path.basename(mp4), "duracao_s": info["duracao_s"], "tamanho_bytes": info["tamanho_bytes"],
            "codecs": info["codecs"], "video": info["video"], "audio": info["audio"],
            "avisos_zona": info["avisos_zona"], "teto_kbps": info["teto_kbps"], "capa_kb": round(kb, 1)}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Vídeos do C05 Meu 2027 vai ser")
    pecas = ["C05-V1", "C05-V2", "C05-V3"]
    ap.add_argument("--so", choices=pecas + ["kit", "previa"], help="só uma peça (ou só o kit / a prévia)")
    ap.add_argument("--nome", default=NOME_PADRAO, help="nome publicado do filtro (padrão: Meu 2027 vai ser)")
    ap.add_argument("--hint", choices=["biquinho", "toque"], default="biquinho",
                    help="instrução da V1 (siga o hint publicado; padrão: biquinho)")
    ap.add_argument("--bolhas", choices=["3", "4", "carro"], default="3",
                    help="3 (padrão: AMOR, GRANA, FUTEBOL), 4 (com CARRO) ou carro (3 bolhas, CARRO no lugar de FUTEBOL)")
    ap.add_argument("--pasta", default=AQUI, help="pasta de saída (padrão: a pasta deste arquivo)")
    ap.add_argument("--rapido", metavar="DIR", help="só pranchas rápidas da linha do tempo, sem mp4")
    a = ap.parse_args(argv)
    a.bolhas = int(a.bolhas) if a.bolhas in ("3", "4") else a.bolhas
    if a.rapido:
        os.makedirs(a.rapido, exist_ok=True)
        for cod in ([a.so] if a.so in pecas else pecas):
            v = _video(cod, a.nome, a.hint, a.bolhas)
            v.prancha(os.path.join(a.rapido, f"{cod}_rapida.png"), n=12)
            CAPAS[cod](a.nome, a.bolhas).save(os.path.join(a.rapido, f"{cod}_capa.png"))
        print("ok", a.rapido)
        return
    os.makedirs(a.pasta, exist_ok=True)
    res = {}
    cods = pecas if a.so is None else ([a.so] if a.so in pecas else [])
    for cod in cods:
        res[cod] = renderizar_peca(cod, a.pasta, a.nome, a.hint, a.bolhas)
    if a.so in (None, "kit"):
        res["kit-C05-M1"] = kit_m1(os.path.join(a.pasta, "kit-C05-M1"), a.nome, a.bolhas)
    if a.so in (None, "previa"):
        mp4s = [(c, os.path.join(a.pasta, f"{c}.mp4")) for c in pecas]
        if all(os.path.exists(p) for _, p in mp4s):
            res["previa"] = previa(mp4s, os.path.join(a.pasta, "previa-videos.png"))
    total = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(a.pasta) for f in fs)
    res["total_pasta_mb"] = round(total / 1024 / 1024, 2)
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
