#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_videos.py: vídeos do C02 "Meu próximo carro" (peças N), capas, legendas, kit da peça M e prévia.

Usa a biblioteca da equipe: tiktok-efeitos/videos/lib/render.py (só importa; não altera nada nela).
Usa as artes de ../assets (só lê; não altera nada lá).
Tudo é determinístico: rodar de novo gera os mesmos arquivos (o x264 roda em 1 thread; ver render_det).

Rodar (de qualquer pasta):
    python3 render_videos.py                           # tudo: C02-V1, V2, V3, capas, legendas, kit M1, prévia
    python3 render_videos.py --so C02-V2               # só uma peça (mp4 + capa + legenda)
    python3 render_videos.py --so kit                  # só o kit da C02-M1
    python3 render_videos.py --so previa               # só a prancha previa-videos.png
    python3 render_videos.py --rapido DIR              # pranchas rápidas da linha do tempo (sem mp4), em DIR
    python3 render_videos.py --nome "Meu proximo carro"  # se o nome publicado sair diferente (ex.: sem acento)

Saída (nesta pasta):
    C02-V1.mp4  C02-V2.mp4  C02-V3.mp4
    C02-Vn-capa.jpg  C02-Vn-legenda.txt
    kit-C02-M1/  (gancho.png, gancho-baixo.png, final.png, assinatura.wav, capa.jpg, legenda.txt)
    previa-videos.png

Não há peça N-carrossel no C02 (plano, seção 3), então não sai nenhuma pasta carrossel-XX/.
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

NOME_PADRAO = "Meu próximo carro"      # nome exato do textos.md (sem reticências)

# Layout (quadro 1080x1920). A parte visível das cartas tem 500 px (x 6 a 506 do PNG). Na escala 1,6 dá
# 800 px: centrada em x = 540, vai de 140 a 940, exatamente dentro da zona segura (60 a 940).
CX = 540
ESC = 1.6
GANCHO_Y = 425        # texto de cima (gancho e reações)
CARTA_Y = 890         # carta "sobre a cabeça" (695 a 1085)
CABECA_Y = 1285       # carinha emoji no lugar da cabeça (nunca rosto ou silhueta humana)
CABECA_H = 210
AMARELO = "#FFD43B"
ESCURO = "#1B1D24"
SR = r.SR


def carta(n):
    return CARTAS[n - 1]


# ============================================================================
# Som: buzina curta "bi-bi" (assinatura do C02), feita aqui com numpy
# ============================================================================
@functools.lru_cache(maxsize=32)
def som_buzina(dur=0.11, f1=415.3, f2=523.25, semente=0):
    """Buzina curta sintetizada: dois tons (terça maior) com harmônicos e um 'formante' de corneta,
    leve subida no ataque e saturação suave. Original, sem gravar nem imitar marca nenhuma."""
    n = int(round(dur * SR))
    t = np.arange(n) / SR
    rng = np.random.default_rng(700 + int(semente))
    s = np.zeros(n)
    for f0, amp in ((f1, 1.0), (f2, 0.78)):
        inst = f0 * (1 - 0.04 * np.exp(-t / 0.010)) * (1 + 0.003 * np.sin(2 * math.pi * 29 * t + rng.uniform(0, 6.28)))
        fase = 2 * math.pi * np.cumsum(inst) / SR
        for k in range(1, 18):
            fk = k * f0
            if fk > 7500:
                break
            ganho = (1 / k ** 0.75) * (0.30 + np.exp(-((fk - 2000) / 850) ** 2) + 0.45 * np.exp(-((fk - 3400) / 650) ** 2))
            s += amp * ganho * np.sin(k * fase + rng.uniform(0, 0.3))
    s = np.tanh(1.7 * s / (np.max(np.abs(s)) + 1e-9))
    env = np.minimum(1, t / 0.006) * np.clip((dur - t) / 0.028, 0, 1)
    s = s * env
    return (s / (np.max(np.abs(s)) + 1e-9) * 0.85).astype(np.float32)


def _juntar(partes):
    """partes: lista de (atraso_s, array). Soma tudo num array mono."""
    n = max(int(round(a * SR)) + len(x) for a, x in partes)
    s = np.zeros(n, np.float32)
    for a, x in partes:
        i = int(round(a * SR))
        s[i:i + len(x)] += x
    return s


def bibi(grave=False):
    """'Bi-bi': dois toques curtos. grave=True é a versão 'decepção' (meio tom abaixo, mais lenta)."""
    if grave:
        a, b = som_buzina(0.10, 330.0, 415.3, 3), som_buzina(0.16, 311.1, 392.0, 4)
        return _juntar([(0.0, a), (0.17, b)])
    a, b = som_buzina(0.095, semente=1), som_buzina(0.125, semente=2)
    return _juntar([(0.0, a), (0.165, b)])


def bibi_duplo():
    """'Bi-bi bi-bi' de comemoração (o 2º par um tom acima)."""
    a, b = som_buzina(0.09, semente=5), som_buzina(0.11, semente=6)
    c, d = som_buzina(0.09, 466.2, 587.3, 7), som_buzina(0.16, 466.2, 587.3, 8)
    return _juntar([(0.0, a), (0.15, b), (0.40, c), (0.55, d)])


# ============================================================================
# Fundo, cabeça, textos e cartão final
# ============================================================================
def fundo_c02(variante=0):
    """Fundo grafite com tracejado amarelo de asfalto (igual à demo da biblioteca), com pequenas variações."""
    cores = [
        ["#1A1D24", "#2B303B", "#0F4A52", "#2B303B"],     # V1 (= demo)
        ["#1A1D24", "#2C2F3E", "#0E5560", "#2B303B"],     # V2
        ["#1A1D24", "#30333B", "#124650", "#262A33"],     # V3
    ][variante % 3]
    vel = [(0, 150), (0, 165), (0, 135)][variante % 3]
    return r.Padrao("tracejado", cor_forma=(255, 212, 59, 34), tamanho=200, velocidade=vel,
                    fundo=r.DegradeAnimado(cores, angulo=105, velocidade=0.05))


def cabeca(v, emoji, ini, fim, entrada=None, saida=None, nome=None):
    """No lugar da cabeça da pessoa, uma carinha emoji (nada de rosto ou silhueta humana)."""
    v.imagem(r.emoji_img(emoji, CABECA_H), ini, fim, centro=(CX, CABECA_Y), entrada=entrada, saida=saida,
             dur_saida=0.15, ocioso="flutuar", som=False, z=14, nome=nome)


def ao_lado(v, emoji, ini, fim, lado=1, tam=118, ritmo=0.9, giro=12, entrada="pop", saida="pop"):
    """Emoji pequeno ao lado da 'cabeça' (🤞, 💪, 🤏), mexendo no ritmo."""
    x = CX + lado * 218
    v.imagem(r.emoji_img(emoji, tam), ini, fim,
             centro=lambda tl: (x, CABECA_Y + 34 + 10 * math.sin(2 * math.pi * tl / ritmo)),
             rotacao=lambda tl: giro * math.sin(2 * math.pi * tl / ritmo), entrada=entrada, saida=saida,
             dur_saida=0.15, som=False, z=15, nome="emoji ao lado")


def topo(v, texto, ini, fim, entrada="pop", saida="pop", tamanho=96, max_linhas=2, ocioso=None, som=True,
         nome="topo", y=GANCHO_Y):
    """Texto de cima (gancho e reações). Gancho: entrada=None (já no 1º quadro)."""
    v.texto(texto, ini, fim, centro=(CX, y), tamanho=tamanho, max_linhas=max_linhas, entrada=entrada,
            saida=saida, dur_saida=0.16, ocioso=ocioso, som=som, z=51 if entrada else 22, nome=nome)


def pilula(v, texto, ini, fim, y, tamanho=56, nome="pílula", entrada="pop", saida="pop", z=51):
    v.texto(texto, ini, fim, centro=(CX, y), tamanho=tamanho, fonte="black", cor=ESCURO, contorno=0,
            max_linhas=1, caixa="#FFFFFF", sombra=(0, 6, 10, 110), entrada=entrada, saida=saida, dur_saida=0.15,
            som=False, z=z, nome=nome)


def cortina(v, bg, t0, fim, z=52):
    """O cartão final sobe de baixo para cima, cobrindo tudo (até o confete). A borda é um tracejado amarelo."""
    def f(canvas, tl, t):
        p = r.progresso(tl, 0, 0.32, "out_cubic")
        y0 = int(round(r.H * (1 - p)))
        if y0 >= r.H:
            return
        fundo = bg.quadro(t)
        canvas.paste(fundo.crop((0, y0, r.W, r.H)), (0, y0))
        if p < 1:
            d = ImageDraw.Draw(canvas)
            d.rectangle([0, max(0, y0 - 5), r.W, y0 + 5], fill=r.rgb("#2B303B"))
            for x in range(-40, r.W, 150):
                d.rounded_rectangle([x, max(0, y0 - 5), x + 90, y0 + 5], radius=5, fill=r.rgb(AMARELO))
    v.adicionar(f, t0, fim, z)


@functools.lru_cache(maxsize=8)
def tamanho_nome(nome, contorno=12, largura=800):
    """Maior fonte (até 128) em que o nome do filtro cabe numa linha só, dentro de 800 px."""
    for s in range(128, 40, -2):
        im = r.texto_img(f"*{nome}*", tamanho=s, fonte_nome="titulo", contorno=contorno, largura_max=largura,
                         max_linhas=1)
        bb = im.info["caixa"]
        if im.info["tamanho_usado"] == s and bb[2] - bb[0] <= largura:
            return s
    return 40


def cartao_final(v, bg, t0, fim, pergunta, nome, estatico=False):
    """CF: símbolo do perfil + 'Procura na lupa 🔎' + nome do filtro em amarelo (1 linha) + pergunta."""
    if not estatico:
        cortina(v, bg, t0, fim)
        v.som(bibi(), t0 + 0.06, 0.34)
    e = (lambda: None) if estatico else (lambda: "pop")
    dt = (lambda d: t0) if estatico else (lambda d: t0 + d)
    v.imagem(SIMBOLO, dt(0.12), fim, centro=(CX, 585), escala=0.32, entrada=e(), som=False,
             ocioso=None if estatico else "flutuar", z=61, nome="CF símbolo")
    v.texto("Procura na lupa 🔎", dt(0.22), fim, centro=(CX, 838), tamanho=86, fonte="black",
            entrada=e(), saida=None, som=False, z=62, nome="CF lupa")
    v.texto(f"*{nome}*", dt(0.32), fim, centro=(CX, 968), tamanho=tamanho_nome(nome), max_linhas=1, contorno=12,
            entrada=e(), saida=None, ocioso=None if estatico else "pulsar", som=not estatico, z=62,
            nome="CF nome do filtro")
    v.texto(pergunta, dt(0.50), fim, centro=(CX, 1140), tamanho=66, fonte="black", cor=ESCURO, contorno=0,
            max_linhas=2, largura_max=730, caixa="#FFFFFF", sombra=(0, 6, 10, 110), entrada=e(), saida=None,
            som=False, z=62, nome="CF pergunta")


# ============================================================================
# Roleta com ordem "vai e volta" por brilho (menos pisca-pisca)
# ============================================================================
@functools.lru_cache(maxsize=64)
def brilho(n):
    """Luminância média da parte visível da carta n."""
    a = np.asarray(Image.open(carta(n)).convert("RGBA"), dtype=np.float64)
    m = a[..., 3] > 128
    px = a[..., :3][m]
    return float((0.2126 * px[:, 0] + 0.7152 * px[:, 1] + 0.0722 * px[:, 2]).mean())


def roleta(v, resultado, inicio, duracao, fim=None, festa=True, intervalo_ini=0.075, intervalo_fim=0.44,
           curva=2.0, vol_tique=0.5, som_res=True, nome="roleta"):
    """Igual à roleta da biblioteca (mesma curva de tempo, mesmo quique, tique a cada troca, luz, raios,
    confete, brilhos e tremida), mas a ordem das cartas não é sorteada: as 25 cartas vão e voltam em ordem de
    brilho. Assim, na parte rápida, a carta troca quase sempre para outra da mesma cor, e a cor de fundo muda
    menos de 3 vezes por segundo (regra de luz piscante do plano, 2.2). Devolve o tempo do resultado."""
    imgs = {n: r.carregar(carta(n)) for n in range(1, 27)}
    res = imgs[resultado]
    N = 2
    while True:
        k = np.arange(N)
        d = intervalo_ini * (intervalo_fim / intervalo_ini) ** ((k / (N - 1)) ** curva)
        if d.sum() >= duracao or N > 800:
            break
        N += 1
    d = d * (duracao / d.sum())
    inicios = list(np.concatenate([[0.0], np.cumsum(d)[:-1]]))
    base = sorted([n for n in range(1, 27) if n != resultado], key=lambda n: (round(brilho(n), 3), n))
    vaivem = base + base[-2:0:-1]
    ini_k = v._rng().randrange(len(vaivem))
    ordem = [vaivem[(ini_k + i) % len(vaivem)] for i in range(N)]
    t_res = inicio + duracao
    for kk in range(N):
        v.som("tique", inicio + inicios[kk], vol_tique * (0.8 + 0.35 * kk / N), 0.0,
              freq=int(2500 - 700 * kk / N), semente=kk % 5)
    if som_res:
        v.som("pop", t_res, 0.5)
    if festa:
        if som_res:
            v.som("plim", t_res, 0.75)
        ink_w = res.width * ESC
        v.luz(t_res, (CX, CARTA_Y), fim=fim, raio=int(ink_w * 0.62), opacidade=0.55)
        v.raios(t_res, (CX, CARTA_Y), fim=fim)
        v.confete(t_res, origem=(CX, CARTA_Y), quantidade=110)
        v.brilhos(t_res + 0.05, (CX, CARTA_Y), raio=(ink_w * 0.55, res.height * ESC * 0.85), quantidade=12)
        v.tremida(t_res, 0.3, 9)

    def f(canvas, tl, t):
        if tl < duracao:
            k = max(0, min(N - 1, int(np.searchsorted(inicios, tl, side="right")) - 1))
            u = (tl - inicios[k]) / d[k]
            img = imgs[ordem[k]]
            e = 1 - r.ease_out_cubic(r.limitar(u * 2.2))
            s, dy, rot = ESC * (1 + 0.05 * e), -26 * e, (1.6 if k % 2 else -1.6) * e
        else:
            img, s, dy, rot = res, ESC * (1 + r.quique(tl - duracao, 0.16 if festa else 0.10, 2.4, 5.0)), 0.0, 0.0
        r.colar(canvas, img, (CX, CARTA_Y + dy), s, rot)
        if v._registrando:
            v._registrar(nome, r.caixa_nominal(img, (CX, CARTA_Y), ESC), t)
    v.adicionar(f, inicio, fim, 12)
    v.ordens = getattr(v, "ordens", []) + [ordem]
    return t_res


# ============================================================================
# As peças N
# ============================================================================
def video_v1(nome):
    """C02-V1 · 'Roleta do próximo carro' · 10 s · trilha 116 bpm."""
    v = r.Video(10.0, semente=201)
    bg = fundo_c02(0)
    v.fundo(bg)
    v.trilha(volume=0.26, bpm=116, progressao=[(45, "m"), (41, ""), (48, ""), (43, "")], ducking=0.5)
    # 0–1,9 s: gancho + carta 2 SUV EM 72 PARCELAS + 🤔 (tudo já no 1º quadro)
    topo(v, "O filtro\nsorteia seu\n*próximo carro*", 0.0, 6.6, entrada=None, saida="pop", ocioso="pulsar",
         tamanho=112, max_linhas=3, nome="gancho")
    v.imagem(carta(2), 0.0, 1.9, centro=(CX, CARTA_Y), escala=ESC, entrada=None, saida="pop", dur_saida=0.2,
             ocioso="balancar", nome="carta 2")
    cabeca(v, "🤔", 0.0, 6.6, nome="cabeça")
    ao_lado(v, "🚗", 0.0, 6.6, lado=-1, tam=124, ritmo=1.3, giro=2, entrada=None)
    # 1,9–2,6 s: título com "toque na tela" + dedo + bi-bi
    v.imagem(TITULO_TOQUE, 1.9, 2.6, centro=(CX, CARTA_Y), escala=ESC, entrada="pop", dur_entrada=0.3,
             ocioso="flutuar", nome="título")
    v.som(bibi(), 1.95, 0.34)
    v.toque(2.12, centro=(CX + 170, CARTA_Y + 70))
    v.som("vush", 2.45, 0.35)
    # 2,6–6,6 s: roleta para na 5 SÓ PEGA NO TRANCO (luz, raios, confete)
    t_res = roleta(v, 5, inicio=2.6, duracao=4.0, fim=8.35)
    # 6,6–8 s: "Bora empurrar 😅"
    cabeca(v, "😅", t_res, 8.35, entrada="pop")
    ao_lado(v, "💪", t_res + 0.1, 8.35, lado=1, ritmo=0.52, giro=14)
    topo(v, "Bora *empurrar* 😅", t_res + 0.12, 8.35, saida=None, tamanho=104, nome="reação")
    # 8–10 s: cartão final
    cartao_final(v, bg, 8.0, 10.0, "Qual saiu pra você?", nome)
    return v


def video_v2(nome):
    """C02-V2 · 'Só paro quando sair ZERO KM' · 14 s · trilha 120 bpm · 3 giros."""
    v = r.Video(14.0, semente=202)
    bg = fundo_c02(1)
    v.fundo(bg)
    v.trilha(volume=0.25, bpm=120, progressao=[(43, ""), (40, "m"), (45, "m"), (41, "")], ducking=0.5)
    # 0–2 s: gancho + carta 20 CONSÓRCIO QUE NUNCA SAI pequena + 😬 🤞
    topo(v, "Só paro quando\nsair *ZERO KM*", 0.0, 3.62, entrada=None, saida="pop", ocioso="pulsar", tamanho=100,
         nome="gancho")
    v.imagem(carta(20), 0.0, 2.05, centro=(CX, CARTA_Y + 10), escala=1.12, rotacao=-5, entrada=None, saida="pop",
             dur_saida=0.18, ocioso="flutuar", nome="carta 20")
    cabeca(v, "😬", 0.0, 3.6, nome="cabeça")
    ao_lado(v, "🤞", 0.0, 3.6, lado=1, ritmo=0.8, giro=10, entrada=None)
    # giro 1 (2–4,5 s) → 7 BICICLETA (POR ENQUANTO): "Não. De novo."
    pilula(v, "1ª tentativa", 1.95, 4.45, 612, nome="tentativa 1")
    v.toque(1.92, centro=(CX + 150, CARTA_Y + 40))
    t1 = roleta(v, 7, inicio=2.05, duracao=1.55, fim=4.55, festa=False, intervalo_ini=0.08, intervalo_fim=0.32)
    v.som(bibi(grave=True), t1 + 0.12, 0.30)
    cabeca(v, "😑", t1, 6.1, entrada="pop")
    topo(v, "Não. *De novo.*", t1 + 0.06, 6.1, tamanho=104, nome="não de novo")
    # giro 2 (4,5–7 s) → 15 EMPRESTADO DO CUNHADO: "Quase…"
    pilula(v, "2ª tentativa", 4.45, 6.95, 612, nome="tentativa 2")
    v.toque(4.42, centro=(CX - 150, CARTA_Y + 40))
    t2 = roleta(v, 15, inicio=4.55, duracao=1.55, fim=7.05, festa=False, intervalo_ini=0.08, intervalo_fim=0.32)
    cabeca(v, "😏", t2, 8.8, entrada="pop")
    ao_lado(v, "🤏", t2 + 0.08, 8.8, lado=1, ritmo=1.0, giro=8)
    topo(v, "*Quase…*", t2 + 0.06, 8.8, tamanho=112, max_linhas=1, nome="quase")
    # giro 3 (7–10 s) → 4 ZERO KM (FINALMENTE): confete, "SAIU! 🎉" + bi-bi duplo
    pilula(v, "3ª tentativa", 6.95, 10.0, 612, nome="tentativa 3")
    v.toque(6.92, centro=(CX + 150, CARTA_Y + 40))
    t3 = roleta(v, 4, inicio=7.05, duracao=1.75, fim=11.85, festa=True, intervalo_ini=0.08, intervalo_fim=0.36)
    v.som(bibi_duplo(), t3 + 0.18, 0.36)
    cabeca(v, "🤩", t3, 10.0, entrada="pop")
    topo(v, "*SAIU!* 🎉", t3 + 0.06, 10.0, tamanho=128, max_linhas=1, nome="saiu")
    # 10–11,5 s: "Agora só falta o dinheiro 😅"
    cabeca(v, "😅", 10.0, 11.85, entrada="pop")
    topo(v, "Agora só falta\no *dinheiro* 😅", 10.0, 11.85, saida=None, tamanho=96, nome="dinheiro")
    # 11,5–14 s: cartão final
    cartao_final(v, bg, 11.5, 14.0, "Quantas tentativas você precisou?", nome)
    return v


def video_v3(nome):
    """C02-V3 · 'Quando perguntam do carro novo' · 11 s · trilha 112 bpm."""
    v = r.Video(11.0, semente=203)
    bg = fundo_c02(2)
    v.fundo(bg)
    v.trilha(volume=0.26, bpm=112, progressao=[(41, ""), (45, "m"), (43, ""), (48, "")], ducking=0.5)
    # 0–2 s: gancho POV + carta 10 COM PORTA DE OUTRA COR + 😑
    pilula(v, "POV:", 0.0, 2.0, 288, tamanho=66, nome="POV", entrada=None)
    topo(v, "perguntaram\n*de novo* do carro", 0.0, 2.0, entrada=None, saida="pop", ocioso="pulsar",
         tamanho=94, y=GANCHO_Y + 40, nome="gancho")
    v.imagem(carta(10), 0.0, 2.0, centro=(CX, CARTA_Y), escala=ESC, entrada=None, saida="pop", dur_saida=0.18,
             ocioso="balancar", nome="carta 10")
    cabeca(v, "😑", 0.0, 2.0, nome="cabeça")
    # 2–3 s: "Pergunta pro filtro, então 🙄" + título + dedo
    topo(v, "Pergunta pro\nfiltro, então 🙄", 2.0, 7.0, saida="pop", tamanho=96, nome="pergunta pro filtro")
    cabeca(v, "🙄", 2.0, 7.0, entrada="pop")
    v.imagem(TITULO_TOQUE, 2.0, 3.0, centro=(CX, CARTA_Y), escala=ESC, entrada="pop", dur_entrada=0.3,
             ocioso="flutuar", nome="título")
    v.toque(2.45, centro=(CX + 170, CARTA_Y + 70))
    v.som("vush", 2.85, 0.35)
    # 3–7 s: roleta para na 18 MOVIDO A ESPERANÇA
    t_res = roleta(v, 18, inicio=3.0, duracao=4.0, fim=8.85)
    # 7–8,5 s: "Assunto encerrado ✅"
    cabeca(v, "😌", t_res, 8.85, entrada="pop")
    topo(v, "Assunto\n*encerrado* ✅", t_res + 0.1, 8.85, saida=None, tamanho=104, nome="assunto encerrado")
    # 8,5–11 s: cartão final
    cartao_final(v, bg, 8.5, 11.0, "Manda pra quem sempre pergunta", nome)
    return v


# ============================================================================
# Capas, legendas e kit da M1
# ============================================================================
def _capa(texto, cartas, emoji, rodape, variante, tam=132):
    """Capa 1080x1920: texto grande e cartas dentro do miolo 3:4 (y 240 a 1680)."""
    v = r.Video(1.0, semente=210 + variante)
    v.fundo(fundo_c02(variante))
    v.texto(texto, 0, None, centro=(CX, 478), tamanho=tam, entrada=None, saida=None, contorno=14,
            largura_max=880, max_linhas=3)
    if len(cartas) == 1:
        v.imagem(cartas[0], 0, None, centro=(CX, 945), escala=ESC, entrada=None, som=False)
    else:   # leque de cartas
        for i, (c, rot, dx, dy) in enumerate(zip(cartas, (8, -6, 0), (-40, 38, 0), (-70, -36, 0))):
            v.imagem(c, 0, None, centro=(CX + dx, 975 + dy), escala=ESC * 0.94, rotacao=rot, entrada=None,
                     som=False, z=10 + i)
    v.imagem(r.emoji_img(emoji, 180), 0, None, centro=(CX, 1290), entrada=None, som=False)
    # rodapé acima de y 1520: na grade do perfil, o número de views cobre o pé do miolo 3:4
    if rodape:
        v.texto(rodape, 0, None, centro=(CX, 1462), tamanho=62, fonte="black", entrada=None, saida=None,
                largura_max=860, max_linhas=1)
    return v.quadro(0.0)


def capa_v1(nome):
    return _capa("QUAL VAI SER\nSEU *PRÓXIMO*\n*CARRO?*", [carta(4), carta(2), carta(5)], "🤔",
                 f"Filtro: *{nome}* 🔎", 0, tam=122)


def capa_v2(nome):
    return _capa("SÓ PARO\nQUANDO SAIR\n*ZERO KM*", [carta(4)], "🤞", f"Filtro: *{nome}* 🔎", 1, tam=122)


def capa_v3(nome):
    return _capa("QUANDO VOCÊ\nVAI *TROCAR*\n*DE CARRO?*", [carta(18)], "🙄", f"Filtro: *{nome}* 🔎", 2, tam=113)


def capa_m1(nome):
    return _capa("FUNCIONA\nASSIM 👇", [TITULO], "🤔", f"*{nome.upper()}* 🔎", 0)


def legendas(nome):
    """Legenda + hashtags (5), prontas para colar. 'ou no meu perfil' só depois da conferência da aba."""
    return {
        "C02-V1": f"O filtro sorteia seu próximo carro 🚗 Qual saiu pra você? Filtro: {nome} 🔎 procura na lupa\n\n"
                  "#meuproximocarro #filtro #filtrotiktok #carro #motorista",
        "C02-V2": f"Quantas tentativas até sair zero km? 😂 Filtro: {nome} 🔎 procura na lupa\n\n"
                  "#meuproximocarro #zerokm #filtrotiktok #carro #humor",
        "C02-V3": f"Pra quem vive perguntando quando você vai trocar de carro. Manda pra essa pessoa 😅 "
                  f"Filtro: {nome} 🔎\n\n#meuproximocarro #filtrotiktok #carro #almocodedomingo #humor",
        "C02-M1": f"Funciona assim: toca na tela e o filtro sorteia seu próximo carro. Filtro: {nome} 🔎 "
                  "procura na lupa\n\n#meuproximocarro #filtro #filtrotiktok #carro #motorista",
    }


def _salvar_wav_mono(caminho, x):
    """WAV 16 bits, 44,1 kHz, mono (metade do tamanho do estéreo; o Clipchamp aceita)."""
    m = np.asarray(x, dtype=np.float64)
    if m.ndim == 2:
        m = m.mean(axis=1)
    m = m / (np.max(np.abs(m)) + 1e-9) * 0.84
    x16 = (np.clip(m, -1, 1) * 32767).astype("<i2")
    with wave.open(caminho, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(np.ascontiguousarray(x16).tobytes())


def _png_transparente(img, centro):
    tela = Image.new("RGBA", (r.W, r.H), (0, 0, 0, 0))
    r.colar(tela, img, centro)
    return tela


def kit_m1(pasta, nome):
    """Kit da C02-M1 para o Montador finalizar no Clipchamp (gravação do preview do Effect House)."""
    os.makedirs(pasta, exist_ok=True)
    estilo = dict(tamanho=74, fonte_nome="black", cor=ESCURO, cor_destaque="#C77800", contorno=0,
                  sombra=(0, 6, 10, 120), largura_max=820, caixa="#FFFFFF", caixa_pad=(36, 22))
    g1 = r.texto_img("Funciona assim 👇\n*qual vai sair?*", **estilo)
    g2 = r.texto_img("Funciona assim 👆\n*qual vai sair?*", **estilo)
    _png_transparente(g1, (CX, 330)).save(os.path.join(pasta, "gancho.png"), optimize=True)
    _png_transparente(g2, (CX, 1390)).save(os.path.join(pasta, "gancho-baixo.png"), optimize=True)
    # final.png: o mesmo cartão final dos vídeos, parado, com a pergunta da M1
    v = r.Video(3.0, semente=220)
    bg = fundo_c02(0)
    v.fundo(bg)
    cartao_final(v, bg, 0.0, None, "Qual saiu pra você?", nome, estatico=True)
    q = v.quadro(1.0).quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    q.save(os.path.join(pasta, "final.png"), optimize=True)
    # assinatura.wav (12 s): trilha 116 bpm + bi-bi no começo + toque no clique (3,0 s) + bi-bi quando entra o
    # final (9,5 s). Sem som no resultado: o tempo do giro do template não foi medido (a confirmar).
    a = r.Video(12.0, semente=221)
    a.trilha(volume=0.30, bpm=116, progressao=[(45, "m"), (41, ""), (48, ""), (43, "")], ducking=0.5)
    a.som(bibi(), 0.12, 0.34)
    a.som("toque", 3.0, 0.55)
    a.som(bibi(), 9.56, 0.36)
    _salvar_wav_mono(os.path.join(pasta, "assinatura.wav"), a.audio())
    r.salvar_jpg(capa_m1(nome), os.path.join(pasta, "capa.jpg"), max_kb=260)
    with open(os.path.join(pasta, "legenda.txt"), "w", encoding="utf-8") as f:
        f.write(legendas(nome)["C02-M1"] + "\n")
    return sorted(os.listdir(pasta))


# ============================================================================
# Prévia (prancha de 6 quadros por vídeo)
# ============================================================================
TEMPOS_PREVIA = {
    "C02-V1": [0.0, 0.5, 2.2, 6.9, 7.6, 9.6],
    "C02-V2": [0.5, 3.9, 6.4, 9.2, 10.8, 13.6],
    "C02-V3": [0.0, 0.5, 2.5, 7.4, 8.2, 10.6],
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
# Render determinístico (precaução contra um defeito relatado na biblioteca)
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
    AAC 128k estéreo 44,1 kHz, +faststart, bitexact), com duas diferenças:
    1) x264 em 1 thread, por precaução: os produtores do C01 e do C08 relataram MP4 com bytes diferentes a cada
       rodada com várias threads + teto de bitrate (VBV). Num teste curto aqui (3 s), a biblioteca saiu igual;
       não confirmei. Em 1 thread o MP4 sai igual byte a byte (conferido nas 3 peças).
    2) Se passar do limite, refaz com teto 12% menor (a biblioteca recodificava em 2 passadas, também com
       várias threads e sem -level, -g e bitexact).
    O áudio sai 1 dB mais baixo (ganho_audio): a masterização da biblioteca deixa o pico em -1,5 dBFS, mas o
    pico real depois do AAC pode passar disso."""
    t0 = time.time()
    n = int(round(v.duracao * v.fps))
    tmp = tempfile.mkdtemp(prefix="c02_render_")
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
# Limites: ficha 2.3 (até 4 MB); V2 com 14 s usa limite_mb_10s = 2,7 (3,78 MB). Os tetos deixam a pasta
# inteira (3 MP4 + capas + kit + prévia) abaixo de 12 MB.
PECAS = {
    "C02-V1": (video_v1, capa_v1, 1900, 4.0),
    "C02-V2": (video_v2, capa_v2, 1700, 2.7 * 1.4),
    "C02-V3": (video_v3, capa_v3, 1800, 4.0),
}


def renderizar_peca(cod, pasta, nome):
    fv, fc, kbps, limite_mb = PECAS[cod]
    v = fv(nome)
    mp4 = os.path.join(pasta, f"{cod}.mp4")
    info = render_det(v, mp4, kbps, int(limite_mb * 1024 * 1024))
    q, kb = r.salvar_jpg(fc(nome), os.path.join(pasta, f"{cod}-capa.jpg"), max_kb=260)
    with open(os.path.join(pasta, f"{cod}-legenda.txt"), "w", encoding="utf-8") as f:
        f.write(legendas(nome)[cod] + "\n")
    return {"arquivo": os.path.basename(mp4), "duracao_s": info["duracao_s"],
            "tamanho_bytes": info["tamanho_bytes"], "tamanho_mb": info["tamanho_mb"], "codecs": info["codecs"],
            "video": info["video"], "audio": info["audio"], "lufs": info["lufs"], "pico_dbtp": info["pico_dbtp"],
            "avisos_zona": info["avisos_zona"], "teto_kbps": info["teto_kbps"], "md5": info["md5"],
            "capa_kb": round(kb, 1), "ordem_cartas_roleta": getattr(v, "ordens", [])}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Vídeos do C02 Meu próximo carro")
    ap.add_argument("--so", choices=sorted(PECAS) + ["kit", "previa"], help="só uma peça (ou só o kit / a prévia)")
    ap.add_argument("--nome", default=NOME_PADRAO, help="nome publicado do filtro (padrão: Meu próximo carro)")
    ap.add_argument("--pasta", default=AQUI, help="pasta de saída (padrão: a pasta deste arquivo)")
    ap.add_argument("--rapido", metavar="DIR", help="só pranchas rápidas da linha do tempo, sem mp4")
    a = ap.parse_args(argv)
    if a.rapido:
        os.makedirs(a.rapido, exist_ok=True)
        for cod, (fv, fc, _, _) in PECAS.items():
            fv(a.nome).prancha(os.path.join(a.rapido, f"{cod}_rapida.png"), n=12)
            fc(a.nome).save(os.path.join(a.rapido, f"{cod}_capa.png"))
        print("ok", a.rapido)
        return
    os.makedirs(a.pasta, exist_ok=True)
    res = {}
    cods = sorted(PECAS) if a.so is None else ([a.so] if a.so in PECAS else [])
    for cod in cods:
        res[cod] = renderizar_peca(cod, a.pasta, a.nome)
    if a.so in (None, "kit"):
        res["kit-C02-M1"] = kit_m1(os.path.join(a.pasta, "kit-C02-M1"), a.nome)
    if a.so in (None, "previa"):
        mp4s = [(c, os.path.join(a.pasta, f"{c}.mp4")) for c in sorted(PECAS)]
        if all(os.path.exists(p) for _, p in mp4s):
            res["previa"] = previa(mp4s, os.path.join(a.pasta, "previa-videos.png"))
    total = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(a.pasta) for f in fs)
    res["total_pasta_mb"] = round(total / 1024 / 1024, 2)
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
