#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_videos.py: vídeos do C09 "Perrengue no volante" (peças N), capas, legendas e prévia.

Usa a biblioteca da equipe: tiktok-efeitos/videos/lib/render.py (só importa; não altera nada nela).
Usa as artes de ../assets (só lê; não altera nada lá) e os textos de ../textos.json.
Tudo é determinístico: rodar de novo gera os mesmos arquivos (o x264 roda em 1 thread; ver render_det).

Rodar (de qualquer pasta):
    python3 render_videos.py                         # tudo: C09-V1, V2, V3, capas, legendas e prévia
    python3 render_videos.py --so C09-V2             # só uma peça (mp4 + capa + legenda)
    python3 render_videos.py --so previa             # só a prancha previa-videos.png
    python3 render_videos.py --rapido DIR            # pranchas rápidas da linha do tempo (sem mp4), em DIR
    python3 render_videos.py --nome "Ranking dos perrengues"   # se o nome publicado sair diferente
    python3 render_videos.py --so C09-V3 --resumo "Pneu furado sem estepe foi o 1 mais votado"
                                                     # V3 com o card do resumo dos comentários (ver abaixo)

C09-V3 e o resumo dos comentários:
    O Montador manda até qui 26/11 um resumo do que MUITA gente escreveu nos posts do C09 (ex.: qual perrengue
    mais gente pôs em 1º). A nuvem reescreve em palavras nossas (nunca o texto de alguém, nome, foto ou @) e roda
    com --resumo "...". Sem --resumo, sai a versão sem card (só o gancho), que é a versão "sem padrão claro".
    Nunca inventar o resumo.

Saída (nesta pasta):
    C09-V1.mp4  C09-V2.mp4  C09-V3.mp4
    C09-Vn-capa.jpg  C09-Vn-legenda.txt
    previa-videos.png

Não há peça N-carrossel nem M-gravacao no C09 (plano, seção 3), então não sai pasta carrossel-XX/ nem kit.
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
CARTAS = {n: os.path.join(ASSETS, "cartas", f"carta_{n:02d}.png") for n in range(1, 11)}
MARCADORES = {k: os.path.join(ASSETS, "marcadores", f"posicao_{k:02d}.png") for k in range(1, 11)}
TITULO_LARGO = os.path.join(ASSETS, "largo_512x256", "titulo.png")
ROT_PIOR = os.path.join(ASSETS, "interface", "rotulo_pior.png")
ROT_BOA = os.path.join(ASSETS, "interface", "rotulo_de_boa.png")

NOME_PADRAO = "Perrengue no volante"      # nome exato do textos.md
SR = r.SR

AMARELO = "#FFD43B"
LARANJA = "#FF7A1A"
ESCURO = "#1B1D24"
GRAFITE = "#262931"


def _itens():
    """Os 10 perrengues da versão padrão, com a quebra de linha oficial (linha1 / linha2 do textos.json)."""
    with open(TEXTOS_JSON, encoding="utf-8") as f:
        j = json.load(f)
    return {i + 1: (it["linha1"], it["linha2"]) for i, it in enumerate(j["resultados"][:10])}


ITENS = _itens()

# ============================================================================
# Layout (quadro 1080x1920; zona segura da biblioteca: x 60 a 940, y 220 a 1500)
#   faixa de cima (y 228 a 452): gancho, depois o título do efeito, e no fim o CF (lupa + nome)
#   coluna da esquerda (x 64 a 528, y 468 a 1496): o painel 1 a 10 (ranking() da biblioteca + marcadores)
#   coluna da direita (x 546 a 938): a carta "sobre a cabeça" e, no lugar da cabeça, uma carinha emoji
# ============================================================================
LISTA = (64, 468, 528, 1496)
NV = 10
X0, Y0, X1, Y1 = LISTA
HROW = (Y1 - Y0) / NV                  # mesma conta do ranking() da biblioteca
HV = HROW * 0.86
VX0 = X0 + HV * 1.05
VW = X1 - VX0
MARC_X = X0 + HV * 0.5
VAGA_CX = VX0 + VW / 2
TOPO_Y = 342                           # centro da faixa de cima
COL_X = 742                            # centro da coluna da direita
CARTA_C = (COL_X, 690)
ESC_CARTA = 0.76                       # carta 512 (507 px visíveis) -> 385 px: x 550 a 935
CABECA_C = (COL_X, 992)
CABECA_H = 168
BALAO_TOPO = 1094                      # o balão de fala sai da "cabeça" para baixo
BALAO_LARG = 390
DV = 0.40                              # duração do voo do item até a vaga


def slot_y(k):
    """Centro (y) da vaga k (1 a 10)."""
    return Y0 + (k - 1) * HROW + HROW / 2


# ============================================================================
# Som: assinatura do C09 = tic-tac de pisca-alerta + vush e pop por vaga (100 bpm)
# ============================================================================
@functools.lru_cache(maxsize=8)
def som_rele(tom=3000.0, grave=False):
    """Clique de relé do pisca-alerta, feito aqui com numpy: estalo curto + corpo agudo + caixinha.
    grave=False é o 'tic' (liga), grave=True é o 'tac' (desliga)."""
    dur = 0.075
    t = np.arange(int(dur * SR)) / SR
    rng = np.random.default_rng(91 if grave else 90)
    estalo = np.diff(rng.standard_normal(len(t)), prepend=0.0) * np.exp(-t / 0.0011)
    corpo = np.sin(2 * math.pi * tom * t) * np.exp(-t / 0.0042) + 0.45 * np.sin(2 * math.pi * tom * 1.53 * t) * np.exp(-t / 0.0028)
    caixa = 0.6 * np.sin(2 * math.pi * (380.0 if grave else 540.0) * t) * np.exp(-t / 0.011)
    s = 0.45 * estalo + 0.8 * corpo + caixa
    return (s / (np.max(np.abs(s)) + 1e-9) * 0.9).astype(np.float32)


def tic():
    return som_rele(3000.0, False)


def tac():
    return som_rele(2150.0, True)


def pisca_alerta(v, t0, n, bpm=100, vol=0.42):
    """n cliques alternados tic / tac, um por tempo da música."""
    beat = 60.0 / bpm
    for i in range(n):
        v.som(tic() if i % 2 == 0 else tac(), t0 + i * beat, vol, -0.2 if i % 2 == 0 else 0.2)


@functools.lru_cache(maxsize=2)
def som_decepcao():
    """'Ih...' de decepção: duas notas que descem (Lá# -> Fá, deslizando no fim), timbre suave."""
    partes = [(0.0, 0.15, 466.16, 466.16), (0.17, 0.42, 349.23, 300.0)]
    n = int(0.62 * SR)
    s = np.zeros(n)
    for t0, dur, f0, f1 in partes:
        m = int(dur * SR)
        t = np.arange(m) / SR
        f = f0 + (f1 - f0) * np.clip((t / dur - 0.45) / 0.55, 0, 1) ** 2
        fase = 2 * math.pi * np.cumsum(f) / SR
        x = np.sin(fase) + 0.32 * np.sin(3 * fase) + 0.12 * np.sin(5 * fase)
        env = np.minimum(1, t / 0.012) * np.clip((dur - t) / 0.06, 0, 1)
        i0 = int(t0 * SR)
        s[i0:i0 + m] += np.tanh(1.3 * x) * env
    return (s / (np.max(np.abs(s)) + 1e-9) * 0.8).astype(np.float32)


@functools.lru_cache(maxsize=2)
def som_cadeado():
    """Cadeado sacudindo: dois cliques metálicos curtos."""
    a = r.som_tique(3400, 0.04, 2)
    b = r.som_tique(2900, 0.04, 3)
    s = np.zeros(int(0.16 * SR), np.float32)
    s[:len(a)] += a
    i = int(0.075 * SR)
    s[i:i + len(b)] += b * 0.8
    return s


def pop_carta():
    return r.som_pop(300.0, 820.0, 0.1)


# ============================================================================
# Fundo: grafite com listras zebradas laranja (como fita de aviso), bem de leve
# ============================================================================
def fundo_c09(variante=0):
    cores = [
        ["#1A1C22", "#262931", "#3A2A20", "#262931"],     # V1
        ["#1B1C22", "#2A2A31", "#40291C", "#24272E"],     # V2
        ["#191B21", "#24272F", "#33281F", "#2A2D35"],     # V3
    ][variante % 3]
    vel = [(36, 0), (-40, 0), (30, 0)][variante % 3]
    return r.Padrao("listras", cor_forma=(255, 122, 26, 30), tamanho=230, velocidade=vel,
                    fundo=r.DegradeAnimado(cores, angulo=100, velocidade=0.04))


# ============================================================================
# Peças de tela
# ============================================================================
@functools.lru_cache(maxsize=1)
def sprites_itens():
    """Texto de cada perrengue em 2 linhas (quebra oficial) para a lista. Todos com a mesma altura de recorte:
    assim o ranking() da biblioteca reduz todos na mesma escala (e só reduz: nada fica borrado).
    QA 06/11: entrelinha 1,12 (era 0,93). Com 0,93 o acento e a cedilha encostavam na outra linha
    (POÇA / ERA CRATERA lia "ĆRATERA"; FILA ATRÁS e DÁ SETA marcavam o COM e o QUEM)."""
    imgs = {n: r.texto_img(f"{l1}\n{l2}", tamanho=52, fonte_nome="titulo", cor="#FFFFFF", cor_destaque=AMARELO,
                           contorno=6, cor_contorno=ESCURO, sombra=(0, 3, 4, 110), largura_max=None,
                           entrelinha=1.12, max_linhas=2)
            for n, (l1, l2) in ITENS.items()}
    caixas = {n: im.getchannel("A").getbbox() for n, im in imgs.items()}
    y0 = min(b[1] for b in caixas.values())
    y1 = max(b[3] for b in caixas.values())
    return {n: im.crop((caixas[n][0], y0, caixas[n][2], y1)) for n, im in imgs.items()}


def painel(v, pousos, fim=None):
    """Painel 1 a 10: vagas do ranking() da biblioteca (sem os números dela) + os marcadores do efeito
    (assets/marcadores). O marcador dá um pulo quando um item cai na vaga dele.
    Defeito contornado: no ranking() a camada começa 0,35 s antes de 'inicio'; por isso inicio = 0,35."""
    v.ranking([], 0.35, n_posicoes=NV, area=LISTA, cor_vaga=(255, 255, 255, 30), cor_borda=(255, 255, 255, 92),
              cor_numero=(0, 0, 0, 0), cor_numero_texto=(0, 0, 0, 0), som=False, z=8, nome="painel")
    imgs = {k: r.carregar(MARCADORES[k]) for k in range(1, 11)}
    esc = HV * 0.98 / 247.0                # parte visível do marcador: 247 px

    def f(canvas, tl, t):
        for k in range(1, 11):
            s = esc
            tp = pousos.get(k)
            if tp is not None and t >= tp:
                s = esc * (1 + r.quique(t - tp, 0.2, 2.4, 6.5))
            r.colar(canvas, imgs[k], (MARC_X, slot_y(k)), s)
            if v._registrando:
                v._registrar("marcadores", r.caixa_nominal(imgs[k], (MARC_X, slot_y(k)), esc), t)
    v.adicionar(f, 0.0, fim, z=9)


def rotulos(v, voos, deslocar_pior=0.0):
    """'PIOR' na vaga 1 e 'DE BOA' na vaga 10 (assets/interface), enquanto estão vazias.
    voos: {vaga: tempo em que o item começa a voar}. O rótulo some logo que o item sai."""
    for k, arq in ((1, ROT_PIOR), (10, ROT_BOA)):
        x = VAGA_CX + (deslocar_pior if k == 1 else 0.0)
        fim = voos[k] + 0.14 if k in voos else None
        v.imagem(arq, 0.0, fim, centro=(x, slot_y(k)), escala=0.58, entrada=None, saida="fade",
                 dur_saida=0.14, som=False, z=9)


def colocar(v, n, vaga, t_voo, dur_voo=DV):
    """O item n voa para a vaga (ranking() da biblioteca, um item por chamada para ter tempos livres).
    Defeitos contornados: (1) a camada do ranking() começa 0,35 s antes de 'inicio', então passo t_voo + 0,35;
    (2) os sons do ranking() saíam 0,35 s atrasados em relação à imagem, então som=False e os sons vão aqui.
    Devolve o tempo em que o item pousa."""
    v.ranking([sprites_itens()[n]], t_voo + 0.35, posicoes=[vaga - 1], n_posicoes=NV, area=LISTA,
              dur_voo=dur_voo, cor_vaga=(0, 0, 0, 0), cor_borda=(0, 0, 0, 0), cor_numero=(0, 0, 0, 0),
              cor_numero_texto=(0, 0, 0, 0), som=False, z=16, nome=f"item {n}")
    v.som("vush", t_voo, 0.38)
    v.som("pop", t_voo + dur_voo * 0.8, 0.62)
    return t_voo + dur_voo


def carta_cabeca(v, img, t_ini, t_saida, entrada="pop", som=True):
    """Carta grande 'sobre a cabeça' (como no efeito). Sai encolhendo quando o item voa para a lista."""
    v.imagem(img, t_ini, t_saida + 0.16, centro=CARTA_C, escala=ESC_CARTA, entrada=entrada, saida="pop",
             dur_entrada=0.3, dur_saida=0.16, som=False, z=12, nome="carta")
    if som and entrada:
        v.som(pop_carta(), t_ini + 0.02, 0.45)


def cabeca(v, seq, fim):
    """No lugar da cabeça da pessoa, uma carinha emoji (nada de rosto real ou silhueta humana).
    seq: [(t, emoji), ...]. Flutua no tempo absoluto, para não pular quando a carinha troca."""
    for i, (t0, e) in enumerate(seq):
        t1 = seq[i + 1][0] if i + 1 < len(seq) else fim

        def centro(tl, t0=t0):
            return (COL_X, CABECA_C[1] + 8 * math.sin(2 * math.pi * (t0 + tl) / 2.6))
        v.imagem(r.emoji_img(e, CABECA_H), t0, t1, centro=centro, entrada=None if i == 0 else "pop",
                 dur_entrada=0.22, saida="pop" if i + 1 == len(seq) else None, dur_saida=0.16, som=False, z=12,
                 nome="cabeça")


def topo(v, texto, t0, t1, entrada="pop", tamanho=82, nome="topo", som=True):
    """Texto grande da faixa de cima (gancho e falas). Gancho: entrada=None (já no 1º quadro)."""
    v.texto(texto, t0, t1, centro=(540, TOPO_Y), tamanho=tamanho, max_linhas=2, largura_max=800, contorno=12,
            entrada=entrada, saida="pop", dur_saida=0.16, som=som and entrada is not None, z=25, nome=nome)


def placa_titulo(v, t0, t1):
    """Título do efeito (largo_512x256/titulo.png) no topo, como no próprio efeito."""
    v.imagem(TITULO_LARGO, t0, t1, centro=(540, TOPO_Y), escala=0.86, entrada="pop", saida="pop",
             dur_entrada=0.3, dur_saida=0.16, som=False, z=20, nome="título")


@functools.lru_cache(maxsize=32)
def balao_img(texto, tamanho=54, linhas=2):
    """Balão de fala branco com rabinho para cima (sai da carinha). Texto escuro, até BALAO_LARG px."""
    padx, pady, cauda = 28, 20, 24
    txt = r.texto_img(texto, tamanho=tamanho, fonte_nome="black", cor=ESCURO, cor_destaque="#D9480F", contorno=0,
                      sombra=None, largura_max=BALAO_LARG - 2 * padx, entrelinha=1.04, max_linhas=linhas)
    txt = txt.crop(txt.getchannel("A").getbbox())
    w, h = txt.width + 2 * padx, txt.height + 2 * pady
    S = 3
    forma = Image.new("L", ((w + 24) * S, (h + cauda + 24) * S), 0)
    d = ImageDraw.Draw(forma)
    ox, oy = 12 * S, 12 * S
    d.rounded_rectangle([ox, oy + cauda * S, ox + w * S, oy + (h + cauda) * S], radius=30 * S, fill=255)
    cx = ox + w * S / 2
    d.polygon([(cx - 22 * S, oy + cauda * S + 4 * S), (cx + 22 * S, oy + cauda * S + 4 * S), (cx, oy)], fill=255)
    forma = forma.resize((w + 24, h + cauda + 24), Image.LANCZOS)
    sombra = forma.filter(ImageFilter.GaussianBlur(7)).point(lambda a: int(a * 0.45))
    out = Image.new("RGBA", forma.size, (0, 0, 0, 0))
    som_img = Image.new("RGBA", forma.size, (0, 0, 0, 255))
    out.paste(som_img, (0, 6), sombra)
    branco = Image.new("RGBA", forma.size, (255, 255, 255, 255))
    out.paste(branco, (0, 0), forma)
    out.alpha_composite(txt, (12 + padx, 12 + cauda + pady))
    return out.crop((0, 12, out.width, out.height))     # topo da imagem = ponta do rabinho


def balao(v, texto, t0, t1, linhas=2, tamanho=54):
    v.imagem(balao_img(texto, tamanho, linhas), t0, t1, centro=(COL_X, BALAO_TOPO), ancora="topo", entrada="pop",
             saida="pop", dur_entrada=0.28, dur_saida=0.15, som=False, z=30, nome="balão")
    v.som("pop", t0 + 0.02, 0.4, 0.15, f0=520.0, f1=1300.0)


def destacar_vaga(v, k, t0, t1, cor=(255, 72, 60)):
    """Contorno vermelho pulsando (2 vezes por segundo) em volta da vaga k."""
    m = 7
    w, h = int(X1 - VX0 + 2 * m), int(HV + 2 * m)

    def f(canvas, tl, t):
        a = (0.55 + 0.45 * math.sin(2 * math.pi * tl / 0.5)) * min(1.0, tl / 0.12) * min(1.0, (t1 - t) / 0.15)
        ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(ov).rounded_rectangle([3, 3, w - 4, h - 4], radius=HV * 0.28 + m, outline=cor + (int(255 * a),),
                                             width=8)
        canvas.paste(ov, (int(VX0 - m), int(slot_y(k) - h / 2)), ov)
    v.adicionar(f, t0, t1, z=17)


@functools.lru_cache(maxsize=1)
def carta_misterio():
    """Carta '?' do C09-V3 (o próximo item que ninguém vê). Mesmo formato e borda das cartas do efeito."""
    S = 2
    n = 512 * S
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([3 * S, 9 * S, 509 * S, 511 * S], radius=46 * S, fill=(255, 255, 255, 255))
    d.rounded_rectangle([13 * S, 19 * S, 499 * S, 501 * S], radius=38 * S, fill=r.rgba(LARANJA))
    d.rounded_rectangle([22 * S, 28 * S, 490 * S, 492 * S], radius=32 * S, fill=r.rgba(GRAFITE))
    listras = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    dl = ImageDraw.Draw(listras)
    for x in range(-n, 2 * n, 64 * S):
        dl.polygon([(x, 0), (x + 22 * S, 0), (x + 22 * S + n, n), (x + n, n)], fill=(255, 255, 255, 16))
    masc = Image.new("L", (n, n), 0)
    ImageDraw.Draw(masc).rounded_rectangle([22 * S, 28 * S, 490 * S, 492 * S], radius=32 * S, fill=255)
    im.paste(listras, (0, 0), Image.fromarray(np.minimum(np.asarray(listras.getchannel("A")), np.asarray(masc))))
    im = im.resize((512, 512), Image.LANCZOS)
    q = r.texto_img("?", tamanho=300, fonte_nome="titulo", cor=AMARELO, contorno=14, cor_contorno=ESCURO,
                    sombra=(0, 10, 14, 150), largura_max=None)
    r.colar(im, q, (256, 232))
    t2 = r.texto_img("QUAL VEM?", tamanho=50, fonte_nome="titulo", cor="#FFFFFF", contorno=7, cor_contorno=ESCURO,
                     sombra=None, largura_max=None)
    r.colar(im, t2, (256, 432))
    return im


@functools.lru_cache(maxsize=8)
def tamanho_nome(nome, contorno=12, largura=800):
    """Maior fonte (até 104) em que o nome do filtro cabe numa linha só."""
    for s in range(104, 40, -2):
        im = r.texto_img(f"*{nome}*", tamanho=s, fonte_nome="titulo", contorno=contorno, largura_max=largura,
                         max_linhas=1)
        bb = im.info["caixa"]
        if im.info["tamanho_usado"] == s and bb[2] - bb[0] <= largura:
            return s
    return 40


def cartao_final(v, t0, fim, pergunta, nome, linhas=2, bpm=100):
    """CF (2 s finais): no topo 'Procura na lupa 🔎' + nome do filtro em amarelo (1 linha); na coluna da direita
    o símbolo do perfil + a pergunta da peça. A lista completa fica na tela (plano: 'lista completa + CF')."""
    v.texto("Procura na lupa 🔎", t0 + 0.05, fim, centro=(540, 284), tamanho=64, fonte="black", entrada="pop",
            saida=None, som=False, z=40, nome="CF lupa")
    v.texto(f"*{nome}*", t0 + 0.16, fim, centro=(540, 394), tamanho=tamanho_nome(nome), max_linhas=1, contorno=12,
            largura_max=800, entrada="pop", saida=None, ocioso="pulsar", som=False, z=41, nome="CF nome do filtro")
    v.imagem(SIMBOLO, t0 + 0.28, fim, centro=(COL_X, 712), escala=0.37, entrada="pop", som=False, ocioso="flutuar",
             z=40, nome="CF símbolo")
    # pílula de no máximo 390 px (texto 330 + 2 x 30 de margem), centrada em 738: de 543 a 933
    v.texto(pergunta, t0 + 0.42, fim, centro=(738, 1022), tamanho=56, fonte="black", cor=ESCURO, contorno=0,
            max_linhas=linhas, largura_max=330, caixa="#FFFFFF", sombra=(0, 6, 10, 110), entrada="pop", saida=None,
            som=False, z=40, nome="CF pergunta")
    v.som("vush", t0 - 0.05, 0.4)
    v.som("pop", t0 + 0.17, 0.55)
    pisca_alerta(v, t0 + 0.3, 3, bpm, 0.38)


# ============================================================================
# C09-V1 · "Gastei o 1 cedo demais" · 14 s
# ============================================================================
def video_v1(nome, resumo=None):
    v = r.Video(14.0, semente=9101)
    v.fundo(fundo_c09(0))
    v.trilha(volume=0.22, bpm=100, progressao=[(45, "m"), (41, ""), (48, ""), (43, "")], ducking=0.5)
    v.luz(0.0, CARTA_C, fim=12.0, raio=300, cor="#FFB066", opacidade=0.22, z=5)

    # (carta, vaga, aparece, voa). Plano: 1->1 no gancho; 4->5, 6->7, 5->9, 9->8, 3->4, 8->6 (~1 s cada);
    # 2 PNEU FURADO -> 2 com tremida; 10->3 e 7->10; lista completa + CF.
    seq = [(1, 1, 0.0, 0.86),
           (4, 5, 2.0, 2.5), (6, 7, 3.0, 3.5), (5, 9, 4.0, 4.5), (9, 8, 5.0, 5.5), (3, 4, 6.0, 6.5), (8, 6, 7.0, 7.5),
           (2, 2, 8.0, 9.35),
           (10, 3, 10.0, 10.45), (7, 10, 10.95, 11.4)]
    pousos = {vaga: t_voo + DV for _, vaga, _, t_voo in seq}
    painel(v, pousos)
    rotulos(v, {vaga: t_voo for _, vaga, _, t_voo in seq})
    for n, vaga, t_ap, t_voo in seq:
        carta_cabeca(v, CARTAS[n], t_ap, t_voo, entrada=None if t_ap == 0.0 else "pop")
        colocar(v, n, vaga, t_voo)
    cabeca(v, [(0.0, "🤔"), (0.8, "😤"), (2.15, "🤔"), (8.05, "😩"), (9.9, "😬")], 12.0)

    # gancho (1º quadro) e título do efeito
    # QA 06/11: o nome vem de --nome (antes era fixo no código e não mudava com o nome publicado)
    topo(v, f"Ranking às cegas:\n*{nome}*", 0.0, 1.9, entrada=None, tamanho=80, nome="gancho")
    placa_titulo(v, 1.9, 12.0)
    v.toque(0.6, centro=(MARC_X, slot_y(1)))
    balao(v, "Certeza: isso\né o pior 😤", 0.8, 2.1)
    pisca_alerta(v, 0.05, 4)

    # o arrependimento: aparece o PNEU FURADO e o 1 já foi
    v.tremida(8.18, 0.45, 15)
    v.som(som_decepcao(), 8.2, 0.55)
    destacar_vaga(v, 1, 8.25, 9.55)
    balao(v, "NÃO!\nCadê o 1? 😩", 8.25, 9.7)
    pisca_alerta(v, 8.3, 2, vol=0.3)

    cartao_final(v, 12.0, None, "Qual você\npunha em 1º?", nome)
    v.ordem_cartas = [(n, vaga) for n, vaga, _, _ in seq]
    return v


# ============================================================================
# C09-V2 · "O 1 só no último" · 14 s · trilha 104 bpm
# ============================================================================
def cadeado(v, t0, t_abre, sacode=(), bpm=104):
    """🔒 piscando na vaga 1 no ritmo da trilha (104 bpm = 1,7 piscada por segundo); sacode quando a
    BATERIA ARRIADA aparece; abre (🔓) quando chega o último item."""
    beat = 60.0 / bpm
    fechado = r.emoji_img("🔒", 74)
    aberto = r.emoji_img("🔓", 74)
    pos = (VX0 + VW * 0.33, slot_y(1))

    def f(canvas, tl, t):
        if t < t_abre:
            k = int((t - t0) / beat)
            fase = ((t - t0) % beat) / beat
            s = 1 + 0.16 * math.exp(-fase * 6)
            op = 1.0 if k % 2 == 0 else 0.5
            rot = 0.0
            for a, b in sacode:
                if a <= t < b:
                    rot = 16 * math.sin(2 * math.pi * 7 * (t - a)) * (1 - (t - a) / (b - a))
                    op = 1.0
            r.colar(canvas, fechado, pos, s, rot, op)
        else:
            u = t - t_abre
            s = 1 + r.quique(u, 0.25, 2.4, 6)
            r.colar(canvas, aberto, pos, s, 0, 1 - r.limitar((u - 0.35) / 0.3))
    v.adicionar(f, t0, t_abre + 0.66, z=17)
    for a, b in sacode:
        v.som(som_cadeado(), a + 0.02, 0.5)


def video_v2(nome, resumo=None):
    v = r.Video(14.0, semente=9202)
    v.fundo(fundo_c09(1))
    bpm = 104
    v.trilha(volume=0.22, bpm=bpm, progressao=[(43, ""), (40, "m"), (45, "m"), (41, "")], ducking=0.5)
    v.luz(0.0, CARTA_C, fim=12.0, raio=300, cor="#FFB066", opacidade=0.22, z=5)

    # 9 itens nas vagas 2 a 10 (a BATERIA ARRIADA vai para a 2: "regra é regra"); o último, LAVAR O CARRO
    # E CHOVER, cai no 1.
    seq = [(4, 8, 0.0, 1.42), (2, 3, 1.92, 2.37), (9, 7, 2.82, 3.27), (6, 5, 3.72, 4.17),
           (10, 2, 4.62, 5.92),
           (3, 4, 6.37, 6.82), (8, 6, 7.27, 7.72), (7, 10, 8.17, 8.62), (1, 9, 9.07, 9.52),
           (5, 1, 9.97, 10.5)]
    pousos = {vaga: t_voo + DV for _, vaga, _, t_voo in seq}
    painel(v, pousos)
    rotulos(v, {vaga: t_voo for _, vaga, _, t_voo in seq}, deslocar_pior=VW * 0.2)
    for n, vaga, t_ap, t_voo in seq:
        carta_cabeca(v, CARTAS[n], t_ap, t_voo, entrada=None if t_ap == 0.0 else "pop")
        colocar(v, n, vaga, t_voo)
    v.som("plim", pousos[1], 0.42)
    v.brilhos(pousos[1], (VAGA_CX, slot_y(1)), raio=(200, 60), quantidade=10, duracao=1.2)
    cabeca(v, [(0.0, "🤔"), (4.75, "😬"), (6.3, "🤔"), (10.15, "😅")], 12.0)

    topo(v, "Regra: *o 1 só*\n*no último* 🔒", 0.0, 1.9, entrada=None, tamanho=84, nome="gancho")
    placa_titulo(v, 1.9, 12.0)
    cadeado(v, 0.0, 10.15, sacode=((4.85, 5.75),), bpm=bpm)
    pisca_alerta(v, 0.05, 4, bpm)
    v.toque(1.15, centro=(MARC_X, slot_y(8)))

    balao(v, "Ai…\nregra é regra", 4.85, 6.25)
    v.som(som_decepcao(), 4.88, 0.35)
    v.som(r.som_tique(3600, 0.05, 4), 10.15, 0.5)            # o cadeado abre
    balao(v, "Oficialmente\no *pior*\n*perrengue*\nda vida 🤷", 10.55, 11.95, linhas=4, tamanho=54)

    cartao_final(v, 12.0, None, "Duvido você\naguentar", nome, bpm=bpm)
    v.ordem_cartas = [(n, vaga) for n, vaga, _, _ in seq]
    return v


# ============================================================================
# C09-V3 · "Nos comentários é fácil" (card de resposta) · 12 s
# ============================================================================
@functools.lru_cache(maxsize=4)
def card_resumo_img(texto):
    """Card desenhado com o resumo, em palavras nossas, do que mais apareceu nos comentários.
    Nunca o texto de alguém, nome, foto ou @. Só entra se o Montador mandar um padrão claro."""
    larg = 780                           # centrado em x = 540: de 150 a 930 (zona segura vai até 940)
    cab = r.texto_img("💬 O que mais apareceu nos comentários:", tamanho=38, fonte_nome="bold", cor="#5A5F6B",
                      contorno=0, sombra=None, largura_max=larg - 80, max_linhas=1)
    corpo = r.texto_img(texto, tamanho=60, fonte_nome="black", cor=ESCURO, cor_destaque="#D9480F", contorno=0,
                        sombra=None, largura_max=larg - 80, max_linhas=4)
    cab = cab.crop(cab.getchannel("A").getbbox())
    corpo = corpo.crop(corpo.getchannel("A").getbbox())
    h = 44 + cab.height + 26 + corpo.height + 48
    S = 2
    forma = Image.new("L", ((larg + 40) * S, (h + 40) * S), 0)
    ImageDraw.Draw(forma).rounded_rectangle([20 * S, 20 * S, (20 + larg) * S, (20 + h) * S], radius=40 * S, fill=255)
    forma = forma.resize((larg + 40, h + 40), Image.LANCZOS)
    sombra = forma.filter(ImageFilter.GaussianBlur(10)).point(lambda a: int(a * 0.5))
    out = Image.new("RGBA", forma.size, (0, 0, 0, 0))
    out.paste(Image.new("RGBA", forma.size, (0, 0, 0, 255)), (0, 8), sombra)
    out.paste(Image.new("RGBA", forma.size, (255, 255, 255, 255)), (0, 0), forma)
    out.alpha_composite(cab, (20 + 40, 20 + 44))
    out.alpha_composite(corpo, (20 + (larg - corpo.width) // 2, 20 + 44 + cab.height + 26))
    return out


def video_v3(nome, resumo=None):
    v = r.Video(12.0, semente=9303)
    v.fundo(fundo_c09(2))
    v.trilha(volume=0.22, bpm=100, progressao=[(40, "m"), (45, "m"), (43, ""), (38, "")], ducking=0.5)
    v.luz(0.0, CARTA_C, fim=10.0, raio=300, cor="#FFB066", opacidade=0.22, z=5)

    # ranking rápido (ranking() da biblioteca, um só chamado, intervalo fixo): o próximo é sempre "?"
    ordem = [(3, 4), (8, 7), (1, 9), (6, 6), (10, 2), (4, 10), (7, 8), (2, 1), (9, 5), (5, 3)]
    t1, intervalo, dvoo = 4.15, 0.58, 0.30
    voos = [t1 + i * intervalo for i in range(len(ordem))]
    pousos = {vaga: tv + dvoo for (_, vaga), tv in zip(ordem, voos)}
    painel(v, pousos)
    rotulos(v, {vaga: tv for (_, vaga), tv in zip(ordem, voos)})
    v.ranking([sprites_itens()[n] for n, _ in ordem], t1 + 0.35, posicoes=[vaga - 1 for _, vaga in ordem],
              n_posicoes=NV, area=LISTA, intervalo=intervalo, dur_voo=dvoo, cor_vaga=(0, 0, 0, 0),
              cor_borda=(0, 0, 0, 0), cor_numero=(0, 0, 0, 0), cor_numero_texto=(0, 0, 0, 0), som=False, z=16,
              nome="ranking")
    for tv in voos:
        v.som("vush", tv, 0.34)
        v.som("pop", tv + dvoo * 0.8, 0.58)

    # carta "?" sobre a cabeça: pula a cada item que sai dela (sem trocar de carta: nada de pisca-pisca)
    t_carta = 2.5 if resumo else 0.0
    misterio = carta_misterio()

    def f(canvas, tl, t):
        s = 1.0
        for tv in voos:
            if t >= tv:
                s = 1 + r.quique(t - tv, 0.09, 2.6, 7.5)
        if tl < 0.3 and t_carta > 0:
            s *= 0.25 + 0.75 * r.ease_out_back(tl / 0.3, 2.2)
        if t > 9.85:
            s *= max(0.0, 1 - (t - 9.85) / 0.15)
        r.colar(canvas, misterio, CARTA_C, ESC_CARTA * s, 2.0 * math.sin(2 * math.pi * t / 2.2))
        if v._registrando:
            v._registrar("carta ?", r.caixa_nominal(misterio, CARTA_C, ESC_CARTA), t)
    v.adicionar(f, t_carta, 10.0, z=12)
    if t_carta > 0:
        v.som(pop_carta(), t_carta + 0.02, 0.45)
    cabeca(v, [(t_carta, "🤔"), (2.55, "😏"), (4.1, "🤔"), (7.0, "😬")] if not resumo else
           [(2.5, "😏"), (4.1, "🤔"), (7.0, "😬")], 10.0)

    topo(v, "Nos comentários\né fácil 😏", 0.0, 2.45, entrada=None, tamanho=84, nome="gancho")
    if resumo:
        v.imagem(card_resumo_img(resumo), 0.0, 2.45, centro=(540, 930), entrada=None, saida="pop", dur_saida=0.16,
                 som=False, z=35, nome="card do resumo")
    topo(v, "Você já viu\na lista toda 😏", 2.5, 4.05, tamanho=84, nome="fala")
    placa_titulo(v, 4.05, 10.0)
    pisca_alerta(v, 0.05, 4)

    cartao_final(v, 10.0, None, "No filtro\nvocê não vê\no próximo", nome, linhas=3)
    v.ordem_cartas = ordem
    return v


# ============================================================================
# Capas, legendas
# ============================================================================
def _capa(texto, cartas, emoji, nome, variante, tam=124, marcador=None, texto_y=500):
    """Capa 1080x1920: texto grande e carta dentro do miolo 3:4 (y 240 a 1680). Rodapé acima de y 1520
    (na grade do perfil, o número de views cobre o pé do miolo 3:4)."""
    v = r.Video(1.0, semente=9400 + variante)
    v.fundo(fundo_c09(variante))
    v.texto(texto, 0, None, centro=(540, texto_y), tamanho=tam, entrada=None, saida=None, contorno=14,
            largura_max=900, max_linhas=4)
    if len(cartas) == 1:
        v.imagem(cartas[0], 0, None, centro=(540, 1030), escala=0.88, entrada=None, som=False, z=10)
    else:
        for i, (c, rot, dx, dy) in enumerate(zip(cartas, (9, -7), (-118, 118), (-18, 18))):
            v.imagem(c, 0, None, centro=(540 + dx, 1040 + dy), escala=0.76, rotacao=rot, entrada=None, som=False,
                     z=10 + i)
    if marcador:
        img, pos, esc = marcador
        v.imagem(img, 0, None, centro=pos, escala=esc, entrada=None, som=False, z=20)
    v.imagem(r.emoji_img(emoji, 150), 0, None, centro=(540, 1335), entrada=None, som=False, z=21)
    v.texto(f"Filtro: *{nome}* 🔎", 0, None, centro=(540, 1462), tamanho=58, fonte="black", entrada=None, saida=None,
            largura_max=880, max_linhas=1)
    return v.quadro(0.0)


def nome_em_2_linhas(nome):
    """'Perrengue no volante' -> ('PERRENGUE', 'NO VOLANTE'): quebra onde as 2 linhas ficam mais parecidas."""
    p = nome.upper().split()
    if len(p) < 2:
        return (nome.upper(),)
    k = min(range(1, len(p)), key=lambda i: (abs(len(" ".join(p[:i])) - len(" ".join(p[i:]))), i))
    return (" ".join(p[:k]), " ".join(p[k:]))


def capa_v1(nome):
    # QA 06/11: o nome da capa vem de --nome (antes era fixo; com outro nome publicado a capa ficava errada)
    linhas = "\n".join(f"*{l}*" for l in nome_em_2_linhas(nome))
    return _capa(f"RANKING\nÀS CEGAS:\n{linhas}", [CARTAS[1], CARTAS[2]], "😩", nome, 0, tam=112,
                 marcador=(MARCADORES[1], (262, 838), 0.4), texto_y=478)


def capa_v2(nome):
    return _capa("REGRA:\n*O 1 SÓ NO*\n*ÚLTIMO* 🔒", [CARTAS[5]], "😅", nome, 1, tam=136,
                 marcador=(MARCADORES[1], (300, 830), 0.42))


def capa_v3(nome):
    return _capa("NOS\nCOMENTÁRIOS\n*É FÁCIL* 😏", [carta_misterio()], "🤔", nome, 2, tam=136)


def hashtag_do_nome(nome):
    """'Perrengue no volante' -> '#perrenguenovolante' (sem acento, sem espaço, minúsculas)."""
    s = unicodedata.normalize("NFD", nome)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return "#" + re.sub(r"[^a-z0-9]", "", s.lower())


def legendas(nome):
    """Legenda + hashtags (até 5), prontas para colar. Textos do plano, com o nome publicado."""
    h = hashtag_do_nome(nome)
    return {
        "C09-V1": f"Ranking às cegas: você não vê o próximo perrengue. Qual você punha em 1º? Filtro: {nome} 🔎\n\n"
                  f"{h} #filtro #filtrotiktok #motorista #ranking",
        "C09-V2": f"Regra: o 1 só no último. Duvido você aguentar 😂 Filtro: {nome} 🔎 procura na lupa\n\n"
                  f"{h} #filtrotiktok #ranking #carro #humor",
        "C09-V3": f"Nos comentários é fácil, você já viu a lista. No filtro, não 😏 Filtro: {nome} 🔎 procura na lupa\n\n"
                  f"{h} #filtrotiktok #ranking #vidademotorista #humor",
    }


# ============================================================================
# Prévia (prancha de 6 quadros por vídeo)
# ============================================================================
TEMPOS_PREVIA = {
    "C09-V1": [0.5, 1.5, 5.0, 8.7, 11.9, 13.6],
    "C09-V2": [0.5, 2.6, 5.4, 9.4, 11.3, 13.6],
    "C09-V3": [0.5, 3.2, 6.0, 8.6, 9.9, 11.6],
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
    pr = pr.quantize(colors=256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.FLOYDSTEINBERG)
    pr.save(saida, optimize=True)
    return saida


# ============================================================================
# Render determinístico
# ============================================================================
def medir_audio(mp4):
    """Volume integrado (LUFS) e pico real (dBTP) do áudio do mp4, pelo filtro ebur128 do ffmpeg."""
    p = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", mp4, "-map", "0:a", "-af",
                        "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    txt = p.stderr[p.stderr.rfind("Summary:"):]
    lufs = re.search(r"I:\s+(-?[\d.]+) LUFS", txt)
    pico = re.search(r"Peak:\s+(-?[\d.]+) dBFS", txt)
    return (float(lufs.group(1)) if lufs else None, float(pico.group(1)) if pico else None)


def render_det(v, saida, kbps, limite_bytes, ganho_audio=0.891):
    """Mesmo formato do Video.renderizar da biblioteca (H.264 High 4.1, yuv420p, BT.709, 30 fps, GOP 2 s,
    AAC 128k estéreo 44,1 kHz, +faststart, bitexact), com duas diferenças, por precaução:
    1) x264 em 1 thread: outros produtores relataram MP4 com bytes diferentes a cada rodada com várias threads
       + teto de bitrate. Em 1 thread o MP4 sai igual byte a byte.
    2) Se passar do limite, refaz com teto 12% menor (em vez das 2 passadas da biblioteca).
    O áudio sai 1 dB mais baixo (ganho_audio): o pico real depois do AAC pode passar dos -1,5 dBFS da master."""
    t0 = time.time()
    n = int(round(v.duracao * v.fps))
    tmp = tempfile.mkdtemp(prefix="c09_render_")
    try:
        wav = os.path.join(tmp, "audio.wav")
        r.salvar_wav(wav, v.audio() * ganho_audio)
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
# Principal
# ============================================================================
# código: (função do vídeo, função da capa, teto de bitrate em kbps, limite em MB)
# Limites: ficha 2.3 do plano (até 4 MB); peças de 14 s com limite_mb_10s = 2,7 (3,78 MB). Os tetos deixam a
# pasta inteira (3 MP4 + capas + prévia + script + roteiros) abaixo de 12 MB.
PECAS = {
    "C09-V1": (video_v1, capa_v1, 1800, 2.7 * 1.4),
    "C09-V2": (video_v2, capa_v2, 1800, 2.7 * 1.4),
    "C09-V3": (video_v3, capa_v3, 1800, 3.2),
}


def renderizar_peca(cod, pasta, nome, resumo=None):
    fv, fc, kbps, limite_mb = PECAS[cod]
    v = fv(nome, resumo)
    mp4 = os.path.join(pasta, f"{cod}.mp4")
    info = render_det(v, mp4, kbps, int(limite_mb * 1024 * 1024))
    q, kb = r.salvar_jpg(fc(nome), os.path.join(pasta, f"{cod}-capa.jpg"), max_kb=260)
    with open(os.path.join(pasta, f"{cod}-legenda.txt"), "w", encoding="utf-8") as f:
        f.write(legendas(nome)[cod] + "\n")
    return {"arquivo": os.path.basename(mp4), "duracao_s": info["duracao_s"],
            "tamanho_bytes": info["tamanho_bytes"], "tamanho_mb": info["tamanho_mb"], "codecs": info["codecs"],
            "video": info["video"], "audio": info["audio"], "lufs": info["lufs"], "pico_dbtp": info["pico_dbtp"],
            "avisos_zona": info["avisos_zona"], "teto_kbps": info["teto_kbps"], "md5": info["md5"],
            "capa_kb": round(kb, 1), "ordem_cartas": getattr(v, "ordem_cartas", [])}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Vídeos do C09 Perrengue no volante")
    ap.add_argument("--so", choices=sorted(PECAS) + ["previa"], help="só uma peça (ou só a prévia)")
    ap.add_argument("--nome", default=NOME_PADRAO, help="nome publicado do filtro (padrão: Perrengue no volante)")
    ap.add_argument("--resumo", default=None,
                    help="C09-V3: resumo, em palavras nossas, do que mais apareceu nos comentários (sem nome/@)")
    ap.add_argument("--pasta", default=AQUI, help="pasta de saída (padrão: a pasta deste arquivo)")
    ap.add_argument("--rapido", metavar="DIR", help="só pranchas rápidas da linha do tempo, sem mp4")
    a = ap.parse_args(argv)
    if a.rapido:
        os.makedirs(a.rapido, exist_ok=True)
        for cod, (fv, fc, _, _) in PECAS.items():
            if a.so in PECAS and cod != a.so:
                continue
            fv(a.nome, a.resumo).prancha(os.path.join(a.rapido, f"{cod}_rapida.png"), n=12)
            fc(a.nome).save(os.path.join(a.rapido, f"{cod}_capa.png"))
        print("ok", a.rapido)
        return
    os.makedirs(a.pasta, exist_ok=True)
    res = {}
    cods = sorted(PECAS) if a.so is None else ([a.so] if a.so in PECAS else [])
    for cod in cods:
        res[cod] = renderizar_peca(cod, a.pasta, a.nome, a.resumo if cod == "C09-V3" else None)
    if a.so in (None, "previa"):
        mp4s = [(c, os.path.join(a.pasta, f"{c}.mp4")) for c in sorted(PECAS)]
        if all(os.path.exists(p) for _, p in mp4s):
            res["previa"] = previa(mp4s, os.path.join(a.pasta, "previa-videos.png"))
    total = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(a.pasta) for f in fs)
    res["total_pasta_mb"] = round(total / 1024 / 1024, 2)
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
