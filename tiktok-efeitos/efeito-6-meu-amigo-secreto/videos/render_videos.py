#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_videos.py: vídeos do C06 "Meu amigo secreto" (peças N), capas, legendas, kit da peça M e prévia.

Usa a biblioteca da equipe: tiktok-efeitos/videos/lib/render.py (só importa; não altera nada nela).
Usa as artes de ../assets (só lê; não altera nada lá).
Tudo é determinístico: rodar de novo gera os mesmos arquivos (o x264 roda em 1 thread; ver renderizar_det).

Rodar (de qualquer pasta):
    python3 render_videos.py                         # tudo: C06-V1, V2, V3, capas, legendas, kit M1, prévia
    python3 render_videos.py --so C06-V2             # só uma peça (mp4 + capa + legenda)
    python3 render_videos.py --so kit                # só o kit da C06-M1
    python3 render_videos.py --so previa             # só a prancha previa-videos.png
    python3 render_videos.py --rapido DIR            # pranchas rápidas da linha do tempo (sem mp4), em DIR
    python3 render_videos.py --nome "Meu amigo secreto"   # se o nome publicado sair diferente

Saída (nesta pasta):
    C06-V1.mp4  C06-V2.mp4  C06-V3.mp4
    C06-Vn-capa.jpg  C06-Vn-legenda.txt
    kit-C06-M1/  (gancho.png, gancho-baixo.png, final.png, assinatura.wav, capa.jpg, legenda.txt)
    previa-videos.png

Não há peça N-carrossel no C06 (plano, seção 3), então não sai nenhuma pasta carrossel-XX/.
"""
from __future__ import annotations

import argparse
import functools
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import time
import wave

sys.dont_write_bytecode = True        # não deixa __pycache__ na pasta da biblioteca

AQUI = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.normpath(os.path.join(AQUI, "..", "..", "videos", "lib"))
sys.path.insert(0, LIB)
import render as r  # noqa: E402

import numpy as np  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

# ============================================================================
# Caminhos e dados do efeito
# ============================================================================
ASSETS = os.path.normpath(os.path.join(AQUI, "..", "assets"))
SIMBOLO = os.path.normpath(os.path.join(AQUI, "..", "..", "videos", "perfil", "simbolo_transparente.png"))
TITULO_TOQUE = os.path.join(ASSETS, "titulo_toque.png")
TITULO = os.path.join(ASSETS, "titulo.png")
CARTAS = [os.path.join(ASSETS, "cartas", f"carta_{i:02d}.png") for i in range(1, 27)]


def carta(n):
    return CARTAS[n - 1]


NOME_PADRAO = "Meu amigo secreto"     # nome exato do textos.md

# Layout (quadro 1080x1920). A etiqueta visível ocupa x 5..507 do PNG de 512; na escala 1,6 dá 803 px.
# Centrada em x = 540 passaria 1 px da zona segura da direita (x 940). Por isso o miolo fica em x = 520
# (118 a 921), o que também afasta tudo da coluna de botões do TikTok.
CX = 520
ESC = 1.6
GANCHO_Y = 405
CARTA_Y = 845
CABECA_Y = 1300
CABECA_H = 200
CF_X = 510                     # cartão final: 10 px à esquerda do miolo, para o nome pulsando caber (94..936)
ANO_Y = 1120                   # pílula do ano (C06-V3)
AMARELO = "#FFD43B"
ESCURO = "#1B1D24"
CONFETE_C06 = ["#FFD43B", "#F2B632", "#E0393E", "#2F8F5B", "#FFF1D0", "#FFFFFF", "#C9A0FF"]

# Cartas que NUNCA aparecem nos vídeos N (mas seguem no efeito):
#   4 CHEIRINHO PRO CARRO, 11 PORTA-CELULAR DE PAINEL, 21 CAPA DE VOLANTE PELUDA -> são acessórios de carro,
#     o mesmo tipo de produto que a loja vende. O vídeo do efeito não pode parecer propaganda da loja.
#   15 DESODORANTE (É INDIRETA?) -> é a carta "evitar" do plano; o vídeo pode ser pausado em qualquer quadro.
FORA_DOS_VIDEOS = (4, 11, 15, 21)
ROLETA = [n for n in range(1, 27) if n not in FORA_DOS_VIDEOS]          # 22 cartas
CARTAS_ROLETA = [carta(n) for n in ROLETA]

# 20 das 26 cartas para o "pausa e vê seu presente" (as mais engraçadas).
# Fora: as 4 acima e as 25 e 26 (letra menor, 41 px no PNG, e piada mais fraca).
SELECAO_V2 = [1, 2, 3, 5, 6, 7, 8, 9, 10, 12, 13, 14, 16, 17, 18, 19, 20, 22, 23, 24]

SR = r.SR


# ============================================================================
# Som: a assinatura do C06 é "sininho + pop de caixa abrindo", tudo feito aqui com numpy
# ============================================================================
@functools.lru_cache(maxsize=8)
def som_sininho(semente=0):
    """Sininho: um sino pequeno e claro (sol, 1568 Hz) com guizos metálicos rápidos por cima.
    Nada de melodia conhecida: é um toque só."""
    rng = np.random.default_rng(6000 + int(semente))
    dur = 1.1
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.zeros(n)
    f0 = 1567.98
    for m, a, tau in ((1.0, 1.0, 0.42), (2.0, 0.34, 0.22), (2.76, 0.28, 0.15), (5.40, 0.11, 0.07), (8.93, 0.05, 0.04)):
        s += a * np.sin(2 * np.pi * f0 * m * t + rng.uniform(0, 2 * np.pi)) * np.exp(-t / tau)
    s *= np.minimum(1, t / 0.0015)
    for k, th in enumerate((0.0, 0.052, 0.098, 0.165, 0.25)):
        i0 = int(th * SR)
        tt = t[: n - i0]
        fb = rng.uniform(3500, 4500)
        g = np.zeros(len(tt))
        for m, a in ((1.0, 1.0), (1.49, 0.6), (2.11, 0.42), (2.63, 0.28)):
            g += a * np.sin(2 * np.pi * fb * m * tt + rng.uniform(0, 2 * np.pi))
        g *= np.exp(-tt / 0.035) * np.minimum(1, tt / 0.0008)
        clique = np.diff(rng.standard_normal(len(tt)) * np.exp(-tt / 0.004), prepend=0.0)
        s[i0:] += (0.5 * g + 0.22 * clique) * (0.9 - 0.12 * k)
    return r._normal(s, 0.9).astype(np.float32)


@functools.lru_cache(maxsize=4)
def som_pop_caixa():
    """Pop de caixa abrindo: baque grave da tampa + papel + 'pop' que sobe."""
    rng = np.random.default_rng(6100)
    dur = 0.34
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 68 + 120 * np.exp(-t / 0.03)
    baque = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.07) * np.minimum(1, t / 0.002)
    ruido = np.diff(rng.standard_normal(n), prepend=0.0)
    papel = r._passa_baixa(ruido, 4200.0) * np.exp(-t / 0.028)
    papel = papel / (np.max(np.abs(papel)) + 1e-9)
    pop = np.zeros(n)
    p = r.som_pop(300.0, 1250.0, 0.12)
    i0 = int(0.022 * SR)
    pop[i0:i0 + len(p)] = p[: n - i0]
    s = 0.95 * baque + 0.32 * papel + 0.7 * pop
    return r._normal(s, 0.9).astype(np.float32)


def som_assinatura():
    """Assinatura do C06: pop de caixa abrindo e, logo depois, o sininho."""
    a, b = som_pop_caixa(), som_sininho(3)
    off = int(0.07 * SR)
    s = np.zeros(off + len(b), np.float32)
    s[: len(a)] += a
    s[off:] += 0.85 * b
    return r._normal(s, 0.9).astype(np.float32)


def chacoalhar(v, t0, t1, volume=0.32):
    """Caixa chacoalhando (toc-toc de madeira) enquanto o presente treme."""
    k, t = 0, t0
    while t < t1:
        v.som("tique", t, volume * (0.8 + 0.2 * (k % 2)), 0.25 if k % 2 else -0.25, freq=760 + 90 * (k % 3), dur=0.05,
              semente=k % 5)
        k += 1
        t += 0.105
    return v


# ============================================================================
# Peças de tela
# ============================================================================
def fundo_c06(variante=0):
    """Fundo roxo com dourado: degradê roxo que flui, estrelinhas douradas de 4 pontas e 🎁 bem clarinhos."""
    cores = [
        ["#2A0E4A", "#46177A", "#5E2196", "#3A1266", "#46177A"],
        ["#300F55", "#251048", "#55208E", "#3E1470", "#251048"],
        ["#2A0E4A", "#3C1470", "#62249C", "#2F0F58", "#3C1470"],
    ][variante % 3]
    vel = [(0, 55), (30, 50), (0, -55)][variante % 3]
    base = r.DegradeAnimado(cores, angulo=100, velocidade=0.05)
    estrelas = r.Padrao("estrelas", cor_forma=(255, 206, 84, 58), tamanho=190, velocidade=vel, fundo=base)
    return r.Padrao("emoji", emoji="🎁", cor_forma=(255, 255, 255, 30), tamanho=330,
                    velocidade=(vel[0] * 0.5, vel[1] * 0.5), fundo=estrelas)


def cabeca(v, emoji, ini, fim, entrada=None, saida=None, nome=None):
    """No lugar da cabeça da pessoa, uma carinha emoji (nada de rosto ou silhueta humana)."""
    img = r.emoji_img(emoji, CABECA_H)
    v.imagem(img, ini, fim, centro=(CX, CABECA_Y), entrada=entrada, saida=saida, ocioso="flutuar",
             som=(entrada == "pop"), z=14, nome=nome)


def tempos_roleta(inicio, duracao, intervalo_ini=0.06, intervalo_fim=0.46, curva=2.0):
    """Os mesmos instantes de troca de carta que o Video.roleta da biblioteca calcula (cópia da conta),
    para pôr o nosso próprio som (tiques) com a roleta muda."""
    N = 2
    while True:
        k = np.arange(N)
        frac = (k / (N - 1)) ** curva
        d = intervalo_ini * (intervalo_fim / intervalo_ini) ** frac
        if d.sum() >= duracao or N > 800:
            break
        N += 1
    d = d * (duracao / d.sum())
    return [inicio + float(x) for x in np.concatenate([[0.0], np.cumsum(d)[:-1]])]


def roleta_c06(v, resultado, inicio, duracao, fim, intervalo_ini=0.085):
    """Roleta da biblioteca, mas com o som e a festa do C06 (confete vermelho, dourado e verde;
    pop de caixa + sininho no resultado). Devolve o tempo do resultado."""
    t_res = v.roleta(CARTAS_ROLETA, ROLETA.index(resultado), inicio=inicio, duracao=duracao,
                     centro=(CX, CARTA_Y), escala=ESC, fim=fim, intervalo_ini=intervalo_ini, som=False,
                     festa=False, raios=True, nome="roleta")
    ts = tempos_roleta(inicio, duracao, intervalo_ini)
    N = len(ts)
    for k, tk in enumerate(ts):
        v.som("tique", tk, 0.5 * (0.8 + 0.35 * k / N), 0.0, freq=int(2500 - 700 * k / N), semente=k % 5)
    v.som(som_pop_caixa(), t_res, 0.62)
    v.som(som_sininho(1), t_res + 0.05, 0.62)
    res = r.carregar(carta(resultado))
    ink_w = res.width * ESC
    v.luz(t_res, (CX, CARTA_Y), fim=fim, raio=int(ink_w * 0.62), opacidade=0.5, cor="#FFE9A8")
    v.confete(t_res, origem=(CX, CARTA_Y), quantidade=110, cores=CONFETE_C06)
    v.brilhos(t_res + 0.05, (CX, CARTA_Y), raio=(ink_w * 0.55, res.height * ESC * 0.85), quantidade=12, cor="#FFF4C2")
    v.tremida(t_res, 0.3, 9)
    return t_res


def presente_treme(v, ini, fim, t_toque, entrada="pop"):
    """O presente fechado (titulo_toque.png) entra, treme cada vez mais e leva um toque na pílula."""
    def rot(tl):
        return 4.5 * math.sin(2 * math.pi * 7.5 * tl) * min(1.0, tl / 0.45)

    def esc(tl):
        return ESC * (1 + 0.025 * math.sin(2 * math.pi * 5.0 * tl) * min(1.0, tl / 0.45))
    v.imagem(TITULO_TOQUE, ini, fim, centro=(CX, CARTA_Y), escala=esc, rotacao=rot, entrada=entrada, dur_entrada=0.25,
             z=12, nome="presente")
    chacoalhar(v, ini + 0.2, fim - 0.05)
    # pílula "👆 TOQUE PRA ABRIR": no PNG fica em x 175..372, y 196..225 -> centro (273, 210)
    v.toque(t_toque, centro=(CX + (273 - 256) * ESC, CARTA_Y + (210 - 128) * ESC))


def abre_presente(v, t):
    """O instante em que a caixa abre: pop de caixa, vush, brilhos saindo da caixa."""
    v.som(som_pop_caixa(), t, 0.78)
    v.som("vush", t + 0.02, 0.32)
    v.brilhos(t, (CX + 8, CARTA_Y - 150), raio=(150, 90), quantidade=9, duracao=0.9, cor="#FFE38A")


def cortina(v, bg, t0, fim, z=52):
    """O cartão final entra de baixo para cima, cobrindo tudo (inclusive o confete). Borda dourada."""
    def f(canvas, tl, t):
        p = r.progresso(tl, 0, 0.32, "out_cubic")
        y0 = int(round(r.H * (1 - p)))
        if y0 >= r.H:
            return
        fundo = bg.quadro(t)
        canvas.paste(fundo.crop((0, y0, r.W, r.H)), (0, y0))
        if p < 1:
            ImageDraw.Draw(canvas).rectangle([0, max(0, y0 - 7), r.W, y0 + 7], fill=r.rgb("#F2C14E"))
    v.adicionar(f, t0, fim, z)


def cartao_final(v, bg, t0, fim, pergunta, nome_filtro, estatico=False):
    """CF: símbolo do perfil + 'Procura na lupa 🔎' + nome do filtro em amarelo (1 linha) + pergunta."""
    if not estatico:
        cortina(v, bg, t0, fim)
        v.som(som_assinatura(), t0 + 0.04, 0.62)
    e = (lambda: None) if estatico else (lambda: "pop")
    dt = (lambda d: t0) if estatico else (lambda d: t0 + d)
    v.imagem(SIMBOLO, dt(0.10), fim, centro=(CF_X, 600), escala=0.31, entrada=e(), som=False,
             ocioso=None if estatico else "flutuar", z=61, nome="símbolo")
    v.texto("Procura na lupa 🔎", dt(0.18), fim, centro=(CF_X, 832), tamanho=84, fonte="black",
            entrada=e(), saida=None, som=False, z=62, nome="lupa")
    v.texto(f"*{nome_filtro}*", dt(0.28), fim, centro=(CF_X, 952), tamanho=120, max_linhas=1, contorno=11,
            largura_max=840, entrada=e(), saida=None, ocioso=None if estatico else "pulsar", som=not estatico,
            z=62, nome="nome do filtro")
    # largura_max 780: o Video.texto não desconta a margem da pílula (30 px de cada lado), então 780 + 60 = 840
    nl = pergunta.count("\n") + 1           # pergunta longa vai em 2 linhas (pílula mais alta)
    v.texto(pergunta, dt(0.46), fim, centro=(CF_X, 1092 + 36 * (nl - 1)), tamanho=62, fonte="black", cor=ESCURO,
            contorno=0, max_linhas=nl, largura_max=780, caixa="#FFFFFF", sombra=(0, 6, 10, 110),
            entrada=e(), saida=None, som=False, z=62, nome="pergunta")
    y_pres = 1290 + 50 * (nl - 1)
    # 🎁 pulando embaixo (dentro da zona segura)
    pres = r.emoji_img("🎁", 150)
    if estatico:
        v.imagem(pres, t0, fim, centro=(CF_X, y_pres), entrada=None, som=False, z=61, nome="presente final")
    else:
        v.imagem(pres, t0 + 0.55, fim,
                 centro=lambda tl: (CF_X, y_pres - 34 * abs(math.sin(math.pi * tl / 0.55))),
                 entrada="pop", som=False, z=61, nome="presente final")


def ordem_por_brilho(numeros):
    """Cartas em ordem de brilho (luminância média da parte visível), para trocas suaves no 'pausa'."""
    def lum(n):
        a = np.asarray(Image.open(carta(n)).convert("RGBA"), dtype=np.float64)
        m = a[..., 3] > 128
        rgb = a[..., :3][m]
        return float((0.2126 * rgb[:, 0] + 0.7152 * rgb[:, 1] + 0.0722 * rgb[:, 2]).mean())
    return sorted(numeros, key=lambda n: (round(lum(n), 3), n))


# ============================================================================
# As peças N
# ============================================================================
def video_v1(nome):
    """C06-V1 · 'Todo ano é meia?' · 10 s."""
    v = r.Video(10.0, semente=601)
    bg = fundo_c06(0)
    v.fundo(bg)
    v.trilha(volume=0.24, bpm=112, progressao=[(45, "m"), (41, ""), (48, ""), (43, "")], ducking=0.5)
    v.som(som_sininho(0), 0.05, 0.5)
    # Tempos (revisão de QA de 06/11): o CF tem 2,0 s (regra 2.2 do plano: últimos 2 a 2,5 s) e o resultado
    # fica parado 1,5 s antes dele. Para caber em 10 s, a roleta gira 3,5 s (era 4,0 s, com CF de só 1,5 s).
    T_RES, T_CF = 6.5, 8.0
    # 0–2 s: gancho + carta 1 MEIA (DE NOVO) balançando + 🤔 (tudo já no 1º quadro)
    v.texto("Todo ano é *meia*\nno amigo secreto?", 0.0, T_RES, centro=(CX, GANCHO_Y), tamanho=90, max_linhas=2,
            largura_max=840, entrada=None, saida="pop", ocioso="pulsar", nome="gancho")
    v.imagem(carta(1), 0.0, 2.0, centro=(CX, CARTA_Y), escala=ESC, entrada=None, saida="pop", dur_saida=0.2,
             ocioso="balancar", som=False, nome="carta 1")
    cabeca(v, "🤔", 0.0, T_RES)
    # 2–3 s: o presente fechado treme + dedo 👆
    presente_treme(v, 2.0, 3.0, t_toque=2.4)
    # 3–6,5 s: a caixa abre e a roleta para na 3 CANECA COM FRASE DE COACH
    abre_presente(v, 3.0)
    t_res = roleta_c06(v, 3, inicio=3.0, duracao=T_RES - 3.0, fim=T_CF + 0.35)
    cabeca(v, "😅", t_res, T_CF + 0.35, entrada="pop")
    # 6,5–8 s: reação
    v.texto("Pelo menos\n*não é meia* 😅", t_res + 0.1, T_CF + 0.35, centro=(CX, GANCHO_Y), tamanho=100,
            max_linhas=2, largura_max=840, entrada="pop", saida=None, z=51,
            nome="reação")   # z 51: acima do confete, abaixo do CF
    # 8–10 s: cartão final
    cartao_final(v, bg, T_CF, 10.0, "O que você vai ganhar? 🎁", nome)
    return v


def video_v2(nome):
    """C06-V2 · 'Pausa e vê seu presente' · 9 s."""
    v = r.Video(9.0, semente=602)
    bg = fundo_c06(1)
    v.fundo(bg)
    v.trilha(volume=0.2, bpm=128, progressao=[(43, ""), (40, "m"), (45, "m"), (41, "")], ducking=0.4)
    dur = 0.35                      # 2,86 trocas por segundo (limite do plano: 3)
    seq = ordem_por_brilho(SELECAO_V2)
    v.texto("*PAUSA AGORA* ⏸️🎁\ne vê seu presente", 0.0, 7.35, centro=(CX, GANCHO_Y), tamanho=86, max_linhas=2,
            largura_max=840, entrada=None, saida=None, ocioso="pulsar", nome="gancho")
    v.slides([carta(n) for n in seq], 0.0, dur_cada=dur, transicao="corte", centro=(CX, CARTA_Y),
             escala=ESC, fim=7.35, nome="cartas")
    for k in range(len(seq)):
        v.som("tique", k * dur, 0.55, 0.0, freq=2350 if k % 2 == 0 else 2150, semente=k % 5)
    cabeca(v, "🤔", 0.0, 7.35)
    cartao_final(v, bg, 7.0, 9.0, "Qual pegou? 🎁", nome)
    v.som(som_sininho(5), 8.25, 0.5)        # sininho no fim
    v.seq_cartas = seq
    return v


def esteira(v, itens, inicio, trocas, fim, dur_trans=0.3, nome="esteira"):
    """Cartas passando como numa esteira: na troca, a carta da vez sai pela esquerda e a próxima entra pela
    direita, as duas no mesmo passo (igual ao slides 'deslizar' da biblioteca, mas com trocas em tempos livres).
    itens: caminhos de PNG; itens[0] já está no lugar em 'inicio'. trocas: tempos absolutos das trocas."""
    imgs = [r.carregar(i) for i in itens]
    for tt in trocas:
        v.som("vush", tt - 0.04, 0.42)

    def f(canvas, tl, t):
        i = 0
        while i < len(trocas) and t >= trocas[i]:
            i += 1
        if i > 0 and t - trocas[i - 1] < dur_trans:
            p = r.ease_in_out_cubic((t - trocas[i - 1]) / dur_trans)
            r.colar(canvas, imgs[i - 1], (CX - p * r.W, CARTA_Y), ESC)
            r.colar(canvas, imgs[i], (CX + (1 - p) * r.W, CARTA_Y), ESC)
        else:
            r.colar(canvas, imgs[i], (CX, CARTA_Y), ESC)
            if v._registrando:
                v._registrar(nome, r.caixa_nominal(imgs[i], (CX, CARTA_Y), ESC), t)
    v.adicionar(f, inicio, fim, 12)


def video_v3(nome):
    """C06-V3 · 'Amigo secreto da firma' · 12 s."""
    v = r.Video(12.0, semente=603)
    bg = fundo_c06(2)
    v.fundo(bg)
    v.trilha(volume=0.24, bpm=116, progressao=[(41, ""), (43, ""), (45, "m"), (40, "m")], ducking=0.5)
    v.som(som_sininho(2), 0.05, 0.45)
    # 0–2 s: gancho + carta 14 SANDUICHEIRA (EU JÁ TENHO 2) balançando
    v.texto("Amigo secreto\nda *firma* é\nsempre igual", 0.0, 2.0, centro=(CX, GANCHO_Y - 10), tamanho=100,
            max_linhas=3, largura_max=840, entrada=None, saida="pop", ocioso="pulsar", nome="gancho")
    # o balanço termina em 1,1 s com a carta reta (meio período do 'balancar'), e a esteira assume dali
    v.imagem(carta(14), 0.0, 1.1, centro=(CX, CARTA_Y), escala=ESC, entrada=None, ocioso="balancar", som=False,
             nome="carta 14")
    # Revisão de QA de 06/11: a roleta gira 2,3 s (era 3,0 s) para o resultado ficar parado 1,5 s antes do CF
    # (antes ficava só 0,8 s, pouco para ler "UM PRESENTÃO (FOI ENGANO)" e o "Durou pouco").
    T_RES = 8.0                        # 5,7 + 2,3
    cabeca(v, "🤔", 0.0, T_RES)
    # 2–5 s: "Todo ano…" + cartas 3, 22, 25 e 13 passando (0,7 s cada), com o ano embaixo;
    # em 4,8 s a esteira traz o presente fechado (título com "toque pra abrir")
    trocas = [2.0, 2.7, 3.4, 4.1, 4.8]
    esteira(v, [carta(14), carta(3), carta(22), carta(25), carta(13), TITULO_TOQUE], 1.1, trocas, 5.1)
    v.texto("Todo ano…", 2.05, 4.95, centro=(CX, GANCHO_Y), tamanho=112, max_linhas=1, entrada="pop", saida="pop",
            nome="todo ano")
    for k, ano in enumerate((2022, 2023, 2024, 2025)):
        ti = trocas[k]
        v.texto(str(ano), ti + 0.16, trocas[k + 1] - 0.02, centro=(CX, ANO_Y), tamanho=62, fonte="black",
                contorno=0, cor=ESCURO, caixa="#FFFFFF", sombra=(0, 5, 8, 110), entrada="pop", saida=None,
                som=False, z=22, nome="ano")
    # 5–5,7 s: "Esse ano vai ser…" + 2026 + o presente treme + dedo 👆
    v.texto("Esse ano\n*vai ser…*", 4.95, T_RES + 0.05, centro=(CX, GANCHO_Y), tamanho=104, max_linhas=2,
            entrada="pop", saida="pop", nome="esse ano")
    v.texto("2026", 4.98, T_RES + 0.05, centro=(CX, ANO_Y), tamanho=62, fonte="black", contorno=0, cor=ESCURO,
            caixa=AMARELO, sombra=(0, 5, 8, 110), entrada="pop", saida="pop", som=False, z=22, nome="ano 2026")
    presente_treme(v, 5.1, 5.7, t_toque=5.2, entrada=None)
    # 5,7–9,5 s: a caixa abre, a roleta gira até 8,0 s e para na 23 UM PRESENTÃO (FOI ENGANO); parada até 9,5 s
    abre_presente(v, 5.7)
    t_res = roleta_c06(v, 23, inicio=5.7, duracao=T_RES - 5.7, fim=9.85)
    cabeca(v, "😳", t_res, 9.85, entrada="pop")
    v.texto("Durou pouco 😅", t_res + 0.08, 9.85, centro=(CX, GANCHO_Y), tamanho=104, max_linhas=1, entrada="pop",
            saida=None, z=51, nome="reação")   # z 51: acima do confete, abaixo do CF
    # 9,5–12 s: cartão final
    cartao_final(v, bg, 9.5, 12.0, "Manda pro pessoal\ndo setor", nome)
    return v


# ============================================================================
# Capas, legendas e kit da M1
# ============================================================================
def _capa(linhas, img, emoji, rodape, variante, img_y=1010, emoji_y=1350, topo=262, base=790):
    """Capa 1080x1920: texto grande e uma carta dentro do miolo 3:4 (y 240 a 1680).
    linhas: lista de (texto, tamanho). Cada bloco usa as quebras '\n' dele (se não couber, a fonte diminui;
    nunca quebra de novo) e os blocos ficam empilhados e centrados entre 'topo' e 'base'."""
    v = r.Video(1.0, semente=610 + variante)
    v.fundo(fundo_c06(variante))
    estilo = dict(contorno=14, largura_max=840)
    blocos = []
    for texto, tam in linhas:
        n = texto.count("\n") + 1
        im = r.texto_img(texto, tam, max_linhas=n, **estilo)
        bx0, by0, bx1, by1 = im.info["caixa"]
        blocos.append((texto, tam, n, by1 - by0, (by0 + by1) / 2 - im.height / 2))
    gap = 18
    total = sum(b[3] for b in blocos) + gap * (len(blocos) - 1)
    y = (topo + base) / 2 - total / 2
    for texto, tam, n, h, desloc in blocos:
        # centro da imagem = centro da tinta - deslocamento (a sombra deixa a imagem maior embaixo)
        v.texto(texto, 0, None, centro=(CX, y + h / 2 - desloc), tamanho=tam, entrada=None, saida=None,
                max_linhas=n, **estilo)
        y += h + gap
    v.luz(0, (CX, img_y), raio=520, opacidade=0.28, cor="#FFE9A8")
    v.imagem(img, 0, None, centro=(CX, img_y), escala=ESC, entrada=None, som=False)
    v.imagem(r.emoji_img(emoji, 190), 0, None, centro=(CX, emoji_y), entrada=None, som=False)
    if rodape:
        v.texto(rodape, 0, None, centro=(CX, 1560), tamanho=62, fonte="black", largura_max=840, max_linhas=1,
                entrada=None, saida=None)
    return v.quadro(0.0)


def capa_v1(nome):
    return _capa([("O QUE VOCÊ\nVAI GANHAR\nNO *AMIGO*\n*SECRETO?* 🎁", 122)], carta(1), "🤔",
                 f"Filtro: *{nome}* 🔎", 0, topo=250, base=785)


def capa_v2(nome):
    return _capa([("*PAUSA* E VÊ\nSEU PRESENTE\n⏸️🎁", 132)], carta(23), "🤔", f"Filtro: *{nome}* 🔎", 1)


def capa_v3(nome):
    return _capa([("AMIGO\nSECRETO\nDA *FIRMA* 🎁", 136)], carta(14), "🤔", f"Filtro: *{nome}* 🔎", 2)


def capa_m1(nome):
    return _capa([("FUNCIONA\nASSIM 👇", 132), (f"*{nome.upper()}*", 120)], TITULO_TOQUE, "🎁",
                 "Toca na tela e o presente abre", 0)


HASHTAGS = {
    "C06-V1": "#meuamigosecreto #amigosecreto #amigooculto #filtro #filtrotiktok",
    "C06-V2": "#meuamigosecreto #amigosecreto #amigooculto #natal #filtrotiktok",
    "C06-V3": "#meuamigosecreto #amigosecretodafirma #confraternizacao #filtrotiktok #humor",
    "C06-M1": "#meuamigosecreto #amigosecreto #filtro #filtrotiktok #natal",
}


def legendas(nome):
    """Legenda + hashtags (até 5), prontas para colar. 'ou no meu perfil' só depois da conferência da aba."""
    texto = {
        "C06-V1": f"Todo ano é meia? 🧦 Vê o que você vai ganhar no amigo secreto. Filtro: {nome} 🔎 procura na lupa",
        "C06-V2": f"Semana da troca: pausa o vídeo e vê o seu presente 🎁 Qual pegou? Filtro: {nome} 🔎 procura na lupa",
        "C06-V3": f"Amigo secreto da firma é sempre igual 😂 Manda pro pessoal do setor. Filtro: {nome} 🔎 procura na lupa",
        "C06-M1": f"Funciona assim: toca na tela e o presente abre 🎁 Filtro: {nome} 🔎 procura na lupa",
    }
    return {k: f"{t}\n\n{HASHTAGS[k]}" for k, t in texto.items()}


def _salvar_wav_mono(caminho, x):
    """WAV 16 bits, 44,1 kHz, mono (metade do tamanho; o Clipchamp aceita)."""
    m = np.asarray(x, dtype=np.float64)
    if m.ndim == 2:
        m = m.mean(axis=1)
    m = m / (np.max(np.abs(m)) + 1e-9) * 0.84
    x16 = (np.clip(m, -1, 1) * 32767).astype("<i2")
    with wave.open(caminho, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(np.ascontiguousarray(x16).tobytes())


def _png_transparente(texto_img, centro):
    tela = Image.new("RGBA", (r.W, r.H), (0, 0, 0, 0))
    r.colar(tela, texto_img, centro)
    return tela


def kit_m1(pasta, nome):
    """Kit da C06-M1 para o Montador finalizar no Clipchamp."""
    os.makedirs(pasta, exist_ok=True)
    estilo = dict(tamanho=68, fonte_nome="black", cor=ESCURO, cor_destaque="#B8860B", contorno=0,
                  sombra=(0, 6, 10, 120), largura_max=760, caixa="#FFFFFF", caixa_pad=(36, 22))
    g1 = r.texto_img("Funciona assim 👇\no *presente abre*", **estilo)
    g2 = r.texto_img("Funciona assim 👆\no *presente abre*", **estilo)
    _png_transparente(g1, (CX, 330)).save(os.path.join(pasta, "gancho.png"), optimize=True)
    _png_transparente(g2, (CX, 1385)).save(os.path.join(pasta, "gancho-baixo.png"), optimize=True)
    # final.png: o mesmo cartão final dos vídeos, parado, com a pergunta da M1
    v = r.Video(3.0, semente=620)
    bg = fundo_c06(0)
    v.fundo(bg)
    cartao_final(v, bg, 0.0, None, "O que você vai ganhar?", nome, estatico=True)
    v.quadro(1.0).save(os.path.join(pasta, "final.png"), optimize=True)
    # assinatura.wav (12 s): trilha 112 bpm + sininho no começo + pop de caixa em 3,0 s (o clique)
    # + assinatura (pop de caixa e sininho) em 9,5 s, quando entra o final
    a = r.Video(12.0, semente=621)
    a.trilha(volume=0.30, bpm=112, progressao=[(45, "m"), (41, ""), (48, ""), (43, "")], ducking=0.5)
    a.som(som_sininho(0), 0.10, 0.5)
    a.som(som_pop_caixa(), 3.0, 0.7)
    a.som(som_assinatura(), 9.5, 0.7)
    _salvar_wav_mono(os.path.join(pasta, "assinatura.wav"), a.audio())
    r.salvar_jpg(capa_m1(nome), os.path.join(pasta, "capa.jpg"), max_kb=260)
    with open(os.path.join(pasta, "legenda.txt"), "w", encoding="utf-8") as f:
        f.write(legendas(nome)["C06-M1"] + "\n")
    return sorted(os.listdir(pasta))


# ============================================================================
# Prévia (prancha de 6 quadros por vídeo)
# ============================================================================
TEMPOS_PREVIA = {
    "C06-V1": [0.0, 0.5, 2.5, 4.5, 7.2, 9.6],
    "C06-V2": [0.0, 0.5, 2.6, 5.4, 6.9, 8.6],
    "C06-V3": [0.0, 0.5, 3.1, 5.4, 8.8, 11.5],
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
PECAS = {"C06-V1": (video_v1, capa_v1, 1850), "C06-V2": (video_v2, capa_v2, 2000), "C06-V3": (video_v3, capa_v3, 1700)}
LIMITE_BYTES = int(3.8 * 1024 * 1024)      # plano 2.3: até 4 MB; deixamos folga para a pasta caber em 12 MB
GANHO_AUDIO = 0.84                         # -1,5 dB de folga antes do AAC (padrão)
TETO_PICO_REAL = -1.2                      # dBTP medido DEPOIS do AAC; acima disso o ganho desce (revisão de QA)


def pico_real_aac(wav, duracao):
    """Codifica só o áudio em AAC (mesmos parâmetros do MP4) e devolve o pico real (dBTP) do resultado,
    medido pelo loudnorm do ffmpeg (o mesmo número que a revisão de QA usa)."""
    m4a = wav[:-4] + "_teste.m4a"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", wav, "-c:a", "aac", "-b:a", "128k", "-ar", str(SR), "-ac", "2",
                    "-t", f"{duracao:.3f}", "-fflags", "+bitexact", "-flags:a", "+bitexact", m4a], check=True)
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", m4a, "-af", "loudnorm=print_format=json",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    dados = json.loads(err[err.rindex("{"): err.rindex("}") + 1])
    return float(dados["input_tp"])


def renderizar_det(v, saida, kbps, limite_bytes=LIMITE_BYTES):
    """Igual ao Video.renderizar da biblioteca (mesmos parâmetros do ffmpeg), com 3 diferenças:
    1) x264 em 1 thread: com várias threads e teto de bitrate (VBV), o x264 gera bytes diferentes a cada
       rodada, mesmo com quadros idênticos. Em 1 thread o MP4 sai igual byte a byte.
    2) áudio com -1,5 dB de folga antes do AAC (o pico da biblioteca fica em -1,5 dBFS, mas depois do AAC o pico
       real chegou a -0,3 dBFS no C06-V3 com -1 dB de folga). Depois da revisão de QA, o pico real é medido
       DEPOIS do AAC: se passar de TETO_PICO_REAL (-1,2 dBTP), o ganho desce até ficar abaixo (determinístico).
    3) se passar do limite, refaz com teto 15% menor (sem as 2 passadas da biblioteca, que usam várias threads)."""
    t0 = time.time()
    n = int(round(v.duracao * v.fps))
    tmp = tempfile.mkdtemp(prefix="c06_render_")
    try:
        wav = os.path.join(tmp, "audio.wav")
        mix = v.audio()
        ganho = GANHO_AUDIO
        r.salvar_wav(wav, mix * ganho)
        tp = pico_real_aac(wav, v.duracao)
        tentativas = 0
        while tp > TETO_PICO_REAL and tentativas < 6:
            ganho = round(ganho * 10 ** ((TETO_PICO_REAL - 0.3 - tp) / 20), 4)     # mira 0,3 dB abaixo do teto
            r.salvar_wav(wav, mix * ganho)
            tp = pico_real_aac(wav, v.duracao)
            tentativas += 1
        print(f"  áudio: ganho {ganho} · pico real depois do AAC {tp:.1f} dBTP", file=sys.stderr)
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
    info["ganho_audio"] = ganho
    info["pico_real_dbtp"] = tp
    info["avisos_zona"] = v.relatorio_zonas()
    print(f"OK {saida}: {info['duracao_s']} s, {info['tamanho_mb']} MB, {info['codecs']}, "
          f"render {info['tempo_render_s']} s", file=sys.stderr)
    for aviso in info["avisos_zona"]:
        print("  AVISO zona segura:", aviso, file=sys.stderr)
    return info


def renderizar_peca(cod, pasta, nome):
    fv, fc, kbps = PECAS[cod]
    v = fv(nome)
    mp4 = os.path.join(pasta, f"{cod}.mp4")
    info = renderizar_det(v, mp4, kbps)
    q, kb = r.salvar_jpg(fc(nome), os.path.join(pasta, f"{cod}-capa.jpg"), max_kb=260)
    with open(os.path.join(pasta, f"{cod}-legenda.txt"), "w", encoding="utf-8") as f:
        f.write(legendas(nome)[cod] + "\n")
    out = {"arquivo": os.path.basename(mp4), "duracao_s": info["duracao_s"], "tamanho_bytes": info["tamanho_bytes"],
           "codecs": info["codecs"], "video": info["video"], "audio": info["audio"],
           "avisos_zona": info["avisos_zona"], "teto_kbps": info["teto_kbps"], "capa_kb": round(kb, 1),
           "ganho_audio": info["ganho_audio"], "pico_real_dbtp": info["pico_real_dbtp"]}
    if hasattr(v, "seq_cartas"):
        out["ordem_cartas"] = v.seq_cartas
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Vídeos do C06 Meu amigo secreto")
    ap.add_argument("--so", choices=sorted(PECAS) + ["kit", "previa"], help="só uma peça (ou só o kit / a prévia)")
    ap.add_argument("--nome", default=NOME_PADRAO, help="nome publicado do filtro (padrão: Meu amigo secreto)")
    ap.add_argument("--pasta", default=AQUI, help="pasta de saída (padrão: a pasta deste arquivo)")
    ap.add_argument("--rapido", metavar="DIR", help="só pranchas rápidas da linha do tempo, sem mp4")
    a = ap.parse_args(argv)
    if a.rapido:
        os.makedirs(a.rapido, exist_ok=True)
        for cod, (fv, fc, _) in PECAS.items():
            v = fv(a.nome)
            v.prancha(os.path.join(a.rapido, f"{cod}_rapida.png"), n=12)
            fc(a.nome).save(os.path.join(a.rapido, f"{cod}_capa.png"))
        capa_m1(a.nome).save(os.path.join(a.rapido, "C06-M1_capa.png"))
        print("ok", a.rapido)
        return
    os.makedirs(a.pasta, exist_ok=True)
    res = {}
    cods = sorted(PECAS) if a.so is None else ([a.so] if a.so in PECAS else [])
    for cod in cods:
        res[cod] = renderizar_peca(cod, a.pasta, a.nome)
    if a.so in (None, "kit"):
        res["kit-C06-M1"] = kit_m1(os.path.join(a.pasta, "kit-C06-M1"), a.nome)
    if a.so in (None, "previa"):
        mp4s = [(c, os.path.join(a.pasta, f"{c}.mp4")) for c in sorted(PECAS)]
        if all(os.path.exists(p) for _, p in mp4s):
            res["previa"] = previa(mp4s, os.path.join(a.pasta, "previa-videos.png"))
    total = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(a.pasta) for f in fs)
    res["total_pasta_mb"] = round(total / 1024 / 1024, 2)
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
