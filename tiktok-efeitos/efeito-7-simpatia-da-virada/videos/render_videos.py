#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_videos.py: vídeos do C07 "Simpatia da Virada" (peças N), capas, legendas, kit da peça M e prévia.

Usa a biblioteca da equipe: tiktok-efeitos/videos/lib/render.py (só importa; não altera nada nela).
Usa as artes de ../assets (só lê; não altera nada lá).
Tudo é determinístico: rodar de novo gera os mesmos arquivos, byte a byte (o x264 roda em 1 thread;
ver renderizar_det).

Rodar (de qualquer pasta):
    python3 render_videos.py                          # tudo: C07-V1, V2, V3, capas, legendas, kit M1, prévia
    python3 render_videos.py --so C07-V2              # só uma peça (mp4 + capa + legenda)
    python3 render_videos.py --so kit                 # só o kit da C07-M1
    python3 render_videos.py --so previa              # só a prancha previa-videos.png
    python3 render_videos.py --rapido DIR             # pranchas rápidas da linha do tempo (sem mp4), em DIR
    python3 render_videos.py --nome "Simpatia de Ano Novo"   # se o nome publicado sair diferente
    python3 render_videos.py --troca 1=R4 --troca 5=R2       # se o efeito for publicado com carta reserva

Saída (nesta pasta):
    C07-V1.mp4  C07-V2.mp4  C07-V3.mp4
    C07-Vn-capa.jpg  C07-Vn-legenda.txt
    kit-C07-M1/  (gancho.png, gancho-baixo.png, final.png, assinatura.wav, capa.jpg, legenda.txt)
    previa-videos.png

Não há peça N-carrossel no C07 (plano, seção 3), então não sai nenhuma pasta carrossel-XX/.
"""
from __future__ import annotations

import argparse
import functools
import json
import math
import os
import random
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
CARTAS = {i: os.path.join(ASSETS, "cartas", f"carta_{i:02d}.png") for i in range(1, 27)}
RESERVAS = {f"R{i}": os.path.join(ASSETS, "reservas", f"reserva_{i:02d}.png") for i in range(1, 5)}
TROCAS = {}                     # número da carta -> caminho da reserva (opção --troca, ex.: 1=R4)


def carta(n):
    """Caminho da carta n (1..26). Se o efeito foi publicado com uma reserva no lugar dela, usa a reserva."""
    return TROCAS.get(n, CARTAS[n])


NOME_PADRAO = "Simpatia da Virada"     # nome exato do textos.md

# Layout (quadro 1080x1920). A parte visível das cartas ocupa x 7..505 do PNG de 512; na escala 1,6 dá 797 px.
# Centrada em x = 540, ela iria até x 938,4 (a zona segura acaba em 940). Com o miolo em x = 530 fica de
# 131 a 929, com folga para o balanço e mais longe da coluna de botões do TikTok.
CX = 530
ESC = 1.6
GANCHO_Y = 400
CARTA_Y = 850
CABECA_Y = 1290
CABECA_H = 190
CF_X = 520                     # cartão final: o nome pulsando (até +2,5 %) cabe de 110 a 930
PILULA = (255.5, 225.0)        # centro da pílula "👆 TOQUE NA TELA" dentro do titulo_toque.png (512x256)
ESCURO = "#1B1D24"
ROXO = "#5B23B0"               # destaque de texto sobre pílula branca (kit da M1)
CORES_FUNDO = [
    ["#0B9CA8", "#36C8BC", "#BFEFC7", "#FFE066", "#FFC93C"],     # V1: turquesa -> menta -> amarelo
    ["#0A93A6", "#2FC1BF", "#B5ECC9", "#FFE36E", "#FFC23A"],     # V2
    ["#0D9FAE", "#3ACBBB", "#C8F0C4", "#FFE15E", "#FFCB45"],     # V3
]
CONFETE_C07 = ["#FFFFFF", "#FF4F9A", "#7B3FE4", "#F5B800", "#FF8A3D", "#FFE14D"]
CONFETE_FESTA = ["#FFD43B", "#F5B800", "#FF4F9A", "#2EE6C8", "#FFFFFF", "#9B6BFF"]   # dourado, rosa, verde-água

# Cartas que NUNCA aparecem nos vídeos N (mas seguem no efeito):
#   12 ROUPA ÍNTIMA AMARELA (PSIU) -> é a carta "evitar" do plano; o vídeo pode ser pausado em qualquer quadro.
#   18 CARRO LIMPINHO PRA VIRADA   -> puxa o assunto de carro, o mesmo da loja. O vídeo do efeito não pode
#      parecer propaganda da loja (plano, seções 5.3 e 10, item 3).
FORA_DOS_VIDEOS = (12, 18)
ROLETA = [n for n in range(1, 27) if n not in FORA_DOS_VIDEOS]          # 24 cartas

# 16 das 26 cartas para o "pausa e vê a sua" (V3): as mais fáceis de cumprir em casa, na virada.
# Fora, além das 2 acima: 1 (7 ondas: precisa de praia ou balde; "ondas, só na beirinha"), 4 (cadeira: não
# incentivar subir em cadeira gravando), 6 (madrugar no dia 1º: a piada é que ninguém cumpre), 13 (boleto:
# mostra conta e banco), 15 (frango não: "não fazer" não rende vídeo), 20 (sem celular: não dá pra gravar),
# 24 (roupa nova: precisa comprar) e 26 (fogos: melhor não incentivar gravar perto de fogos).
SELECAO_V3 = [2, 3, 5, 7, 8, 9, 10, 11, 14, 16, 17, 19, 21, 22, 23, 25]

SR = r.SR


# ============================================================================
# Som: a assinatura do C07 é "bipes de contagem + estouro grave + brilho", tudo feito aqui com numpy
# ============================================================================
def _t(dur):
    return np.arange(int(round(dur * SR))) / SR


@functools.lru_cache(maxsize=8)
def som_estouro(semente=0):
    """Estouro grave de fogos lá no céu: baque grave que desce, sopro abafado e estalinhos que somem.
    (Só o som; nada de rojão na mão.)"""
    rng = np.random.default_rng(7100 + int(semente))
    t = _t(1.3)
    n = len(t)
    f = 36 + 95 * np.exp(-t / 0.045)
    baque = np.tanh(1.8 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.26) * np.minimum(1, t / 0.004))
    sopro = r._passa_baixa(rng.standard_normal(n) * np.exp(-t / 0.10), 650.0)
    sopro /= np.max(np.abs(sopro)) + 1e-9
    est = np.zeros(n)
    L = int(0.012 * SR)
    tt = np.arange(L) / SR
    for _ in range(42):
        t0 = 0.10 + 0.9 * rng.uniform(0, 1) ** 1.4
        i0 = int(t0 * SR)
        m = max(0, min(L, n - i0))
        a = rng.uniform(0.3, 1.0) * math.exp(-(t0 - 0.1) / 0.45)
        est[i0:i0 + m] += (rng.standard_normal(L) * np.exp(-tt / 0.0018))[:m] * a
    est = est - r._passa_baixa(est, 1800.0)
    est /= np.max(np.abs(est)) + 1e-9
    return r._normal(1.0 * baque + 0.45 * sopro + 0.30 * est, 0.9).astype(np.float32)


@functools.lru_cache(maxsize=8)
def som_brilho(semente=0, dur=0.9, n_pings=16):
    """Brilho: chuva de 'plins' agudos e curtos, espalhados da esquerda para a direita (estéreo)."""
    rng = np.random.default_rng(7200 + int(semente))
    n = int(dur * SR)
    E, D = np.zeros(n), np.zeros(n)
    for _ in range(n_pings):
        t0 = rng.uniform(0, dur * 0.55)
        f = rng.uniform(2600, 6400)
        tau = rng.uniform(0.06, 0.16)
        a = rng.uniform(0.35, 1.0) * (1 - 0.5 * t0 / dur)
        i0 = int(t0 * SR)
        tt = np.arange(n - i0) / SR
        p = a * (np.sin(2 * np.pi * f * tt) * np.exp(-tt / tau) +
                 0.3 * np.sin(2 * np.pi * 2.76 * f * tt) * np.exp(-tt / (tau * 0.5))) * np.minimum(1, tt / 0.001)
        ang = (rng.uniform(-0.7, 0.7) + 1) * np.pi / 4
        E[i0:] += p * math.cos(ang)
        D[i0:] += p * math.sin(ang)
    return r._normal(np.stack([E, D], axis=1), 0.85).astype(np.float32)


@functools.lru_cache(maxsize=2)
def som_bipes():
    """Três bipes de contagem pra meia-noite: bi, bi, BIIP (o último mais agudo e mais longo)."""
    a, b = r.som_bip(988.0, 0.11), r.som_bip(1480.0, 0.24)
    s = np.zeros(int(0.30 * SR) + len(b), np.float32)
    for t0 in (0.0, 0.15):
        i0 = int(t0 * SR)
        s[i0:i0 + len(a)] += a
    s[int(0.30 * SR):] += b
    return s


def _mix_estereo(partes, dur):
    """partes: lista de (t, array mono ou (n,2), volume). Devolve array (n,2) normalizado."""
    out = np.zeros((int(dur * SR), 2))
    for t0, x, vol in partes:
        x = np.asarray(x, dtype=np.float64)
        if x.ndim == 1:
            x = np.stack([x, x], axis=1) * 0.7071
        i0 = int(t0 * SR)
        m = min(len(x), len(out) - i0)
        out[i0:i0 + m] += x[:m] * vol
    return r._normal(out, 0.9).astype(np.float32)


@functools.lru_cache(maxsize=4)
def som_assinatura(com_bipes=True):
    """Assinatura do C07: bipes de contagem, estouro grave e brilho. Sem os bipes no V3 (lá eles abrem o vídeo)."""
    if com_bipes:
        return _mix_estereo([(0.0, som_bipes(), 0.75), (0.42, som_estouro(0), 1.0), (0.50, som_brilho(0), 0.6)], 1.85)
    return _mix_estereo([(0.0, som_estouro(3), 1.0), (0.08, som_brilho(3), 0.6)], 1.45)


# ============================================================================
# Fundo: turquesa -> amarelo, estrelinhas e chuva de confete
# ============================================================================
@functools.lru_cache(maxsize=4)
def _degrade(variante):
    return r.fundo_degrade(CORES_FUNDO[variante % 3], 90)


@functools.lru_cache(maxsize=4)
def fundo_c07(variante=0):
    """Degradê turquesa (em cima) -> menta -> amarelo (embaixo), com estrelinhas brancas deslizando."""
    grad = _degrade(variante)
    vel = [(0, 45), (25, 40), (0, -40)][variante % 3]
    return r.Padrao("estrelas", cor_forma=(255, 255, 255, 52), tamanho=210, velocidade=vel,
                    fundo=lambda t, g=grad: g.copy())


@functools.lru_cache(maxsize=2)
def fundo_cf():
    """Fundo do cartão final: céu da meia-noite (roxo-uva, como as cartas) com estrelinhas douradas."""
    grad = r.fundo_degrade(["#24104C", "#43187A", "#5A2096", "#2E1160"], 90)
    return r.Padrao("estrelas", cor_forma=(255, 206, 84, 72), tamanho=170, velocidade=(0, 35),
                    fundo=lambda t, g=grad: g.copy())


def chuva_confete(v, semente, quantidade=56, z=2):
    """Chuva de confete contínua no fundo (laço sem emenda: o que sai embaixo volta em cima)."""
    rng = random.Random(9000 + semente)
    cores = [r.rgb(c) for c in CONFETE_C07]
    ps = [dict(x=rng.uniform(0, r.W), y=rng.uniform(0, r.H + 120), vy=rng.uniform(110, 230),
               tam=rng.uniform(12, 21), rot0=rng.uniform(0, 360), vrot=rng.uniform(-220, 220),
               fase=rng.uniform(0, 6.28), vflip=rng.uniform(3, 8), osc=rng.uniform(8, 26),
               cor=rng.choice(cores)) for _ in range(quantidade)]

    def f(canvas, tl, t):
        d = ImageDraw.Draw(canvas)
        for p in ps:
            y = (p["y"] + p["vy"] * t) % (r.H + 120) - 60
            x = p["x"] + p["osc"] * math.sin(1.6 * t + p["fase"])
            flip = math.cos(p["fase"] + p["vflip"] * t)
            w2, h2 = p["tam"] / 2 * max(0.15, abs(flip)), p["tam"] * 0.3
            a = math.radians(p["rot0"] + p["vrot"] * t)
            ca, sa = math.cos(a), math.sin(a)
            pts = [(x + px * ca - py * sa, y + px * sa + py * ca) for px, py in ((-w2, -h2), (w2, -h2), (w2, h2), (-w2, h2))]
            d.polygon(pts, fill=p["cor"] if flip > 0 else tuple(int(c * 0.75) for c in p["cor"]))
    v.adicionar(f, 0.0, None, z)


def base_video(dur, semente, variante, trilha_bpm, progressao, volume_trilha=0.24):
    v = r.Video(dur, semente=semente)
    v.fundo(fundo_c07(variante))
    chuva_confete(v, variante)
    v.trilha(volume=volume_trilha, bpm=trilha_bpm, progressao=progressao, ducking=0.5)
    return v


# ============================================================================
# Peças de tela
# ============================================================================
def cabeca(v, emoji, ini, fim, entrada=None, saida=None, nome=None, y=CABECA_Y, altura=CABECA_H):
    """No lugar da cabeça da pessoa, uma carinha emoji (nada de rosto ou silhueta humana)."""
    v.imagem(r.emoji_img(emoji, altura), ini, fim, centro=(CX, y), entrada=entrada, saida=saida, ocioso="flutuar",
             som=(entrada == "pop"), z=14, nome=nome)


def ponto_pilula(cx=CX, cy=CARTA_Y, esc=ESC):
    return (cx + (PILULA[0] - 256) * esc, cy + (PILULA[1] - 128) * esc)


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


def roleta_c07(v, resultado, inicio, duracao, fim, intervalo_ini=0.09):
    """Roleta da biblioteca, mas com o som e a festa do C07 (estouro grave + brilho; confete dourado, rosa e
    verde-água). Começo um pouco mais lento que o padrão (0,09 s por carta). Devolve o tempo do resultado."""
    cartas = [carta(n) for n in ROLETA]
    t_res = v.roleta(cartas, ROLETA.index(resultado), inicio=inicio, duracao=duracao, centro=(CX, CARTA_Y),
                     escala=ESC, fim=fim, intervalo_ini=intervalo_ini, som=False, festa=False, raios=True,
                     nome="roleta")
    ts = tempos_roleta(inicio, duracao, intervalo_ini)
    N = len(ts)
    for k, tk in enumerate(ts):
        v.som("tique", tk, 0.5 * (0.8 + 0.35 * k / N), 0.0, freq=int(2500 - 700 * k / N), semente=k % 5)
    v.som(som_estouro(1), t_res, 0.8)
    v.som(som_brilho(2), t_res + 0.06, 0.5)
    v.som("pop", t_res, 0.35)
    res = r.carregar(carta(resultado))
    ink_w = res.width * ESC
    v.luz(t_res, (CX, CARTA_Y), fim=fim, raio=int(ink_w * 0.62), opacidade=0.5, cor="#FFF6C8")
    v.confete(t_res, origem=(CX, CARTA_Y), quantidade=110, cores=CONFETE_FESTA)
    v.brilhos(t_res + 0.05, (CX, CARTA_Y), raio=(ink_w * 0.55, res.height * ESC * 0.85), quantidade=12, cor="#FFF4C2")
    v.tremida(t_res, 0.3, 9)
    return t_res


def titulo_com_toque(v, ini, fim, t_toque, entrada="pop"):
    """Título MINHA SIMPATIA PRA 2027 É… com a pílula 'toque na tela', e o dedo tocando a pílula."""
    v.imagem(TITULO_TOQUE, ini, fim, centro=(CX, CARTA_Y), escala=ESC, entrada=entrada, dur_entrada=0.25,
             ocioso="flutuar", z=12, nome="título")
    v.som("vush", ini - 0.08, 0.35)
    v.toque(t_toque, centro=ponto_pilula())


def cortina(v, bg, t0, fim, z=52):
    """O cartão final sobe de baixo para cima, cobrindo tudo (inclusive o confete). Borda dourada."""
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


def cartao_final(v, t0, fim, pergunta, nome_filtro, estatico=False, com_bipes=True):
    """CF: símbolo do perfil + 'Procura na lupa 🔎' + nome do filtro em amarelo (1 linha) + pergunta + 🍇."""
    bg = fundo_cf()
    if not estatico:
        cortina(v, bg, t0, fim)
        v.som(som_assinatura(com_bipes), t0 + 0.04, 0.62)
    e = (lambda: None) if estatico else (lambda: "pop")
    dt = (lambda d: t0) if estatico else (lambda d: t0 + d)
    v.imagem(SIMBOLO, dt(0.10), fim, centro=(CF_X, 600), escala=0.31, entrada=e(), som=False,
             ocioso=None if estatico else "flutuar", z=61, nome="símbolo")
    v.texto("Procura na lupa 🔎", dt(0.18), fim, centro=(CF_X, 832), tamanho=84, fonte="black",
            entrada=e(), saida=None, som=False, z=62, nome="lupa")
    v.texto(f"*{nome_filtro}*", dt(0.28), fim, centro=(CF_X, 952), tamanho=120, max_linhas=1, contorno=11,
            largura_max=800, entrada=e(), saida=None, ocioso=None if estatico else "pulsar", som=not estatico,
            z=62, nome="nome do filtro")
    # largura_max 760: o Video.texto não desconta a margem da pílula (30 px de cada lado), então 760 + 60 = 820
    nl = pergunta.count("\n") + 1
    v.texto(pergunta, dt(0.46), fim, centro=(CF_X, 1092 + 36 * (nl - 1)), tamanho=62, fonte="black", cor=ESCURO,
            contorno=0, max_linhas=nl, largura_max=760, caixa="#FFFFFF", sombra=(0, 6, 10, 110),
            entrada=e(), saida=None, som=False, z=62, nome="pergunta")
    y_uva = 1290 + 50 * (nl - 1)
    uva = r.emoji_img("🍇", 150)
    if estatico:
        v.imagem(uva, t0, fim, centro=(CF_X, y_uva), entrada=None, som=False, z=61, nome="uva")
    else:
        v.imagem(uva, t0 + 0.55, fim, centro=lambda tl: (CF_X, y_uva - 34 * abs(math.sin(math.pi * tl / 0.55))),
                 entrada="pop", som=False, z=61, nome="uva")


@functools.lru_cache(maxsize=64)
def _luminancia(caminho):
    a = np.asarray(Image.open(caminho).convert("RGBA"), dtype=np.float64)
    m = a[..., 3] > 128
    rgb = a[..., :3][m]
    return float((0.2126 * rgb[:, 0] + 0.7152 * rgb[:, 1] + 0.0722 * rgb[:, 2]).mean())


def ordem_por_brilho(numeros):
    """Cartas em ordem de brilho (luminância média da parte visível), para trocas suaves no 'pausa'."""
    return sorted(numeros, key=lambda n: (round(_luminancia(carta(n)), 3), n))


# Leque do V2: as 3 cartas empilhadas de cima para baixo, a de cima na frente (cobre só o selo da de baixo,
# nunca o texto). (número, dx, y, rotação em graus)
LEQUE = [(7, -16, 680, 3.0), (11, 20, 875, -2.5), (5, -8, 1070, 2.0)]
LEQUE_ESC = 1.15


# ============================================================================
# As peças N
# ============================================================================
def video_v1(nome):
    """C07-V1 · 'O filtro escolhe sua simpatia' · 10 s."""
    v = base_video(10.0, 701, 0, 108, [(45, "m"), (41, ""), (48, ""), (43, "")])
    v.som(som_brilho(5), 0.05, 0.4)
    # 0–2 s: gancho + carta 1 PULAR 7 ONDAS (VALE NO BALDE) balançando + 🤔 (tudo já no 1º quadro)
    # Se o nome publicado for outro (--nome), o gancho não pinta "simpatia da virada" de amarelo: em amarelo,
    # a frase parece o nome do filtro e a pessoa procuraria o nome errado na lupa (revisão de QA, 06/11).
    gancho = ("O filtro escolhe sua\n*simpatia da virada*" if nome == NOME_PADRAO
              else "O filtro escolhe sua\n*simpatia* de Ano-Novo")
    v.texto(gancho, 0.0, 6.8, centro=(CX, GANCHO_Y), tamanho=96, max_linhas=2,
            largura_max=820, entrada=None, saida="pop", ocioso="pulsar", nome="gancho")
    v.imagem(carta(1), 0.0, 2.0, centro=(CX, CARTA_Y), escala=ESC, entrada=None, saida="pop", dur_saida=0.2,
             ocioso="balancar", som=False, nome="carta 1")
    cabeca(v, "🤔", 0.0, 6.8)
    # 2–2,8 s: título com "toque na tela" + dedo 👆
    titulo_com_toque(v, 2.0, 2.8, t_toque=2.3)
    # 2,8–6,8 s: roleta para na 14 VARRER O AZAR PRA FORA
    t_res = roleta_c07(v, 14, inicio=2.8, duracao=4.0, fim=8.55)
    cabeca(v, "🫡", t_res, 8.55, entrada="pop")
    # 6,8–8,2 s: reação
    v.texto("Ordem é *ordem* 🧹", t_res + 0.1, 8.55, centro=(CX, GANCHO_Y), tamanho=112, max_linhas=1,
            largura_max=820, entrada="pop", saida=None, z=51, nome="reação")   # z 51: acima do confete, abaixo do CF
    # 8,2–10 s: cartão final
    cartao_final(v, 8.2, 10.0, "Saiu, tem que cumprir 😅", nome)
    return v


def leque(v, ini, t_junta, dur_junta=0.32):
    """As 3 cartas do gancho do V2. Em t_junta elas voam para o centro, encolhem e somem (o título entra)."""
    for k, (n, dx, y, rot) in enumerate(LEQUE):
        x0, y0 = CX + dx, y

        def prog(tl, k=k):
            return r.ease_in_cubic(r.limitar((tl - (t_junta - ini) - 0.03 * k) / dur_junta))

        v.imagem(carta(n), ini, t_junta + dur_junta + 0.1,
                 centro=lambda tl, x0=x0, y0=y0, prog=prog: (r.lerp(x0, CX, prog(tl)), r.lerp(y0, CARTA_Y, prog(tl))),
                 escala=lambda tl, prog=prog: r.lerp(LEQUE_ESC, 1.25, prog(tl)),
                 rotacao=lambda tl, rot=rot, prog=prog: rot * (1 - prog(tl)),
                 opacidade=lambda tl, prog=prog: 1 - prog(tl),
                 entrada=None, ocioso="flutuar", som=False, z=13 - k, nome=f"leque {k + 1}")
    v.som("vush", t_junta, 0.45)


def video_v2(nome):
    """C07-V2 · 'Não sabe qual simpatia fazer?' · 11 s."""
    v = base_video(11.0, 702, 1, 108, [(43, ""), (40, "m"), (45, "m"), (41, "")])
    v.som(som_brilho(6), 0.05, 0.4)
    # 0–2 s: gancho + cartas 7, 11 e 5 em leque (já no 1º quadro)
    v.texto("Não sabe qual\n*simpatia* fazer? 🤔", 0.0, 2.0, centro=(CX, GANCHO_Y - 10), tamanho=100, max_linhas=2,
            largura_max=820, entrada=None, saida="pop", ocioso="pulsar", nome="gancho")
    leque(v, 0.0, 1.95)
    # 2–3 s: "Deixa o filtro escolher 👆" + título + dedo
    v.texto("Deixa o filtro\n*escolher* 👆", 2.0, 7.0, centro=(CX, GANCHO_Y - 10), tamanho=100, max_linhas=2,
            largura_max=820, entrada="pop", saida="pop", nome="deixa")
    titulo_com_toque(v, 2.2, 3.0, t_toque=2.55)
    cabeca(v, "🤔", 2.0, 7.0, entrada="pop")
    # 3–7 s: roleta para na 17 12 DESEJOS NUM PAPELZINHO
    t_res = roleta_c07(v, 17, inicio=3.0, duracao=4.0, fim=8.85)
    cabeca(v, "😌", t_res, 8.85, entrada="pop")
    # 7–8,5 s: reação
    v.texto("Essa dá pra\n*cumprir* ✍️", t_res + 0.1, 8.85, centro=(CX, GANCHO_Y - 10), tamanho=108, max_linhas=2,
            largura_max=820, entrada="pop", saida=None, z=51, nome="reação")
    # 8,5–11 s: cartão final
    cartao_final(v, 8.5, 11.0, "Qual saiu pra você?", nome)
    return v


def video_v3(nome):
    """C07-V3 · 'Último dia: pausa e vê a sua' · 9 s."""
    v = base_video(9.0, 703, 2, 116, [(41, ""), (43, ""), (45, "m"), (40, "m")], volume_trilha=0.2)
    # 0–1,4 s: gancho + título do efeito (o "baralho") + contagem curta 3, 2, 1… com bipes
    v.texto("Pausa e vê sua\n*simpatia* ⏸️", 0.0, 1.4, centro=(CX, GANCHO_Y - 10), tamanho=104, max_linhas=2,
            largura_max=820, entrada=None, saida="pop", dur_saida=0.15, nome="gancho")
    v.imagem(TITULO, 0.0, 1.4, centro=(CX, CARTA_Y), escala=ESC, entrada=None, ocioso="flutuar", som=False,
             nome="título")
    contagem = [("3", 0.0, 0.47), ("2", 0.47, 0.94), ("1…", 0.94, 1.4)]
    for k, (s, a, b) in enumerate(contagem):
        v.texto(s, a, b, centro=(CX, CABECA_Y), tamanho=230, contorno=14, max_linhas=1,
                entrada=None if k == 0 else "pop", dur_entrada=0.14, saida=None, som=False, z=30, nome="contagem")
        v.som("bip", a + 0.02, 0.6, 0.0, freq=1320.0 if k == 2 else 988.0, dur=0.22 if k == 2 else 0.13)
    # 1,4–7 s: texto fixo + 16 cartas a cada 0,35 s (2,86 trocas por segundo; limite do plano: 3)
    dur = 0.35
    seq = ordem_por_brilho(SELECAO_V3)
    v.texto("*PAUSA*\n*AGORA* ⏸️✨", 1.4, 7.35, centro=(CX, GANCHO_Y - 10), tamanho=124, max_linhas=2,
            largura_max=820, entrada="pop", dur_entrada=0.2, saida=None, ocioso="pulsar", nome="pausa agora")
    v.slides([carta(n) for n in seq], 1.4, dur_cada=dur, transicao="corte", centro=(CX, CARTA_Y),
             escala=ESC, fim=7.35, nome="cartas")
    for k in range(len(seq)):
        v.som("tique", 1.4 + k * dur, 0.55, 0.0, freq=2350 if k % 2 == 0 else 2150, semente=k % 5)
    cabeca(v, "🤔", 1.4, 7.35, entrada="pop")
    # 7–9 s: cartão final com estouro no fim (sem os bipes: eles já abriram o vídeo)
    cartao_final(v, 7.0, 9.0, "Grava cumprindo ✨", nome, com_bipes=False)
    v.seq_cartas = seq
    v.seq_inicio, v.seq_dur = 1.4, dur
    return v


# ============================================================================
# Capas, legendas e kit da M1
# ============================================================================
@functools.lru_cache(maxsize=2)
def leque_img(esc=1.0, gap=172):
    """O leque do V2 como uma imagem só (para a capa)."""
    ims = []
    for n, dx, y, rot in LEQUE:
        ims.append((r.transformar(carta(n), esc, rot), dx * esc / LEQUE_ESC))
    w = max(im.width for im, _ in ims) + 60
    h = ims[0][0].height + gap * (len(ims) - 1) + 20
    tela = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))
    for k in reversed(range(len(ims))):        # de baixo para cima: a de cima fica na frente
        im, dx = ims[k]
        r.colar(tela, im, (w / 2 + dx, ims[0][0].height / 2 + 10 + k * gap))
    return tela


def _capa(linhas, img, emoji, rodape, variante, img_y=1010, emoji_y=1350, topo=262, base=790, img_esc=ESC):
    """Capa 1080x1920: texto grande e uma carta dentro do miolo 3:4 (y 240 a 1680).
    linhas: lista de (texto, tamanho). Cada bloco usa as quebras '\n' dele e os blocos ficam empilhados
    e centrados entre 'topo' e 'base'."""
    v = r.Video(1.0, semente=710 + variante)
    v.fundo(fundo_c07(variante))
    chuva_confete(v, 20 + variante)
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
        v.texto(texto, 0, None, centro=(CX, y + h / 2 - desloc), tamanho=tam, entrada=None, saida=None,
                max_linhas=n, **estilo)
        y += h + gap
    v.luz(0, (CX, img_y), raio=520, opacidade=0.30, cor="#FFF6C8")
    v.imagem(img, 0, None, centro=(CX, img_y), escala=img_esc, entrada=None, som=False)
    if emoji:
        v.imagem(r.emoji_img(emoji, 190), 0, None, centro=(CX, emoji_y), entrada=None, som=False)
    if rodape:
        v.texto(rodape, 0, None, centro=(CX, 1560), tamanho=62, fonte="black", largura_max=840, max_linhas=1,
                entrada=None, saida=None)
    return v.quadro(0.3)


def capa_v1(nome):
    return _capa([("QUAL VAI\nSER SUA\n*SIMPATIA*? ✨", 140)], carta(1), "🤔", f"Filtro: *{nome}* 🔎", 0,
                 topo=250, base=785)


def capa_v2(nome):
    return _capa([("NÃO SABE QUAL\n*SIMPATIA*\nFAZER? 🤔", 126)], leque_img(1.0), None, f"Filtro: *{nome}* 🔎", 1,
                  img_y=1095, topo=250, base=700, img_esc=1.0)


def capa_v3(nome):
    return _capa([("*PAUSA* E VÊ\nSUA SIMPATIA ⏸️", 128)], TITULO, "🤔", f"Filtro: *{nome}* 🔎", 2)


def capa_m1(nome):
    return _capa([("FUNCIONA\nASSIM 👇", 132), (f"*{nome.upper()}*", 112)], TITULO_TOQUE, "🍇",
                  "Toca na tela e sai a sua", 0, topo=250, base=800)


HASHTAGS = {        # a 1ª é a do efeito; ela sai do nome publicado (ver hashtag_efeito)
    "C07-V1": "{h} #simpatiasdeanonovo #anonovo #filtro #filtrotiktok",
    "C07-V2": "{h} #simpatiasdeanonovo #anonovo #reveillon #filtrotiktok",
    "C07-V3": "{h} #simpatiasdeanonovo #reveillon #ultimodiadoano #filtrotiktok",
    "C07-M1": "{h} #simpatiasdeanonovo #reveillon #filtro #filtrotiktok",
}


def hashtag_efeito(nome):
    """'Simpatia da Virada' -> '#simpatiadavirada' (sem acento, sem espaço, minúsculas)."""
    import unicodedata
    s = unicodedata.normalize("NFKD", nome)
    return "#" + "".join(c for c in s if c.isascii() and c.isalnum()).lower()


def legendas(nome):
    """Legenda + hashtags (até 5), prontas para colar. Textos do plano (seção 3, C07)."""
    tags = {k: v.format(h=hashtag_efeito(nome)) for k, v in HASHTAGS.items()}
    texto = {
        "C07-V1": f"O filtro escolhe sua simpatia de Ano-Novo. Saiu, tem que cumprir 😅 Filtro: {nome} 🔎 procura na lupa",
        "C07-V2": f"Não sabe qual simpatia de Ano-Novo fazer? Deixa o filtro escolher ✨ Filtro: {nome} 🔎 procura na lupa",
        "C07-V3": f"Último dia de 2026: pausa o vídeo, vê sua simpatia e grava cumprindo ✨ Filtro: {nome} 🔎",
        "C07-M1": f"Funciona assim: toca na tela e sai a sua simpatia da virada ✨ Filtro: {nome} 🔎 procura na lupa",
    }
    return {k: f"{t}\n\n{tags[k]}" for k, t in texto.items()}


def _salvar_wav_mono(caminho, x):
    """WAV 16 bits, 44,1 kHz, mono (metade do tamanho)."""
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


def _png_transparente(img, centro):
    tela = Image.new("RGBA", (r.W, r.H), (0, 0, 0, 0))
    r.colar(tela, img, centro)
    return tela


def kit_m1(pasta, nome):
    """Kit da C07-M1 para o Montador finalizar no Clipchamp."""
    os.makedirs(pasta, exist_ok=True)
    estilo = dict(tamanho=68, fonte_nome="black", cor=ESCURO, cor_destaque=ROXO, contorno=0,
                  sombra=(0, 6, 10, 120), largura_max=760, caixa="#FFFFFF", caixa_pad=(36, 22))
    g1 = r.texto_img("Funciona assim 👇\n*saiu, cumpriu*", **estilo)
    g2 = r.texto_img("Funciona assim 👆\n*saiu, cumpriu*", **estilo)
    _png_transparente(g1, (CX, 330)).save(os.path.join(pasta, "gancho.png"), optimize=True)
    _png_transparente(g2, (CX, 1370)).save(os.path.join(pasta, "gancho-baixo.png"), optimize=True)
    # final.png: o mesmo cartão final dos vídeos, parado, com a pergunta da M1
    v = r.Video(3.0, semente=720)
    v.fundo(fundo_cf())
    cartao_final(v, 0.0, None, "Faz e me conta em 2027", nome, estatico=True)
    v.quadro(1.0).save(os.path.join(pasta, "final.png"), optimize=True)
    # assinatura.wav (12 s): trilha 108 bpm + brilho no começo + toque em 3,0 s (o clique)
    # + assinatura (bipes, estouro e brilho) em 9,5 s, quando entra o final
    a = r.Video(12.0, semente=721)
    a.trilha(volume=0.30, bpm=108, progressao=[(45, "m"), (41, ""), (48, ""), (43, "")], ducking=0.5)
    a.som(som_brilho(5), 0.10, 0.45)
    a.som("toque", 3.0, 0.7)
    a.som(som_assinatura(True), 9.5, 0.7)
    _salvar_wav_mono(os.path.join(pasta, "assinatura.wav"), a.audio())
    r.salvar_jpg(capa_m1(nome), os.path.join(pasta, "capa.jpg"), max_kb=260)
    with open(os.path.join(pasta, "legenda.txt"), "w", encoding="utf-8") as f:
        f.write(legendas(nome)["C07-M1"] + "\n")
    return sorted(os.listdir(pasta))


# ============================================================================
# Prévia (prancha de 6 quadros por vídeo)
# ============================================================================
TEMPOS_PREVIA = {
    "C07-V1": [0.0, 0.5, 2.4, 4.6, 7.5, 9.6],
    "C07-V2": [0.0, 0.5, 2.6, 5.0, 7.8, 10.6],
    "C07-V3": [0.0, 0.5, 1.2, 3.2, 6.0, 8.6],
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
PECAS = {"C07-V1": (video_v1, capa_v1, 1850), "C07-V2": (video_v2, capa_v2, 1800), "C07-V3": (video_v3, capa_v3, 2000)}
LIMITE_BYTES = int(3.8 * 1024 * 1024)      # plano 2.3: até 4 MB; com folga para a pasta caber em 12 MB


def medir_audio(mp4):
    """Volume integrado (LUFS) e pico real (dBTP) do áudio já em AAC, medidos pelo ffmpeg (ebur128)."""
    p = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", mp4, "-map", "0:a", "-af", "ebur128=peak=true",
                        "-f", "null", "-"], capture_output=True, text=True)
    txt = p.stderr[p.stderr.rfind("Summary:"):]
    lufs = re.search(r"I:\s+(-?[\d.]+) LUFS", txt)
    pico = re.search(r"Peak:\s+(-?[\d.]+) dBFS", txt)
    return {"lufs": float(lufs.group(1)) if lufs else None, "pico_real_dbtp": float(pico.group(1)) if pico else None}


def renderizar_det(v, saida, kbps, limite_bytes=LIMITE_BYTES):
    """Igual ao Video.renderizar da biblioteca (mesmos parâmetros do ffmpeg), com 3 diferenças:
    1) x264 em 1 thread: com várias threads e teto de bitrate (VBV), o x264 da biblioteca gera bytes (e até
       quadros decodificados) diferentes a cada rodada. Em 1 thread o MP4 sai igual byte a byte.
    2) áudio com folga antes do AAC: a biblioteca deixa o pico em -1,5 dBFS, mas depois do AAC o pico real passou
       de 0 dBTP no V3 (tiques). Aqui o áudio é codificado num teste, o pico real é medido e o ganho baixa até
       ficar em -1 dBTP ou menos.
    3) se passar do limite, refaz com teto 15% menor (sem as 2 passadas da biblioteca, que usam várias threads)."""
    t0 = time.time()
    n = int(round(v.duracao * v.fps))
    tmp = tempfile.mkdtemp(prefix="c07_render_")
    try:
        wav = os.path.join(tmp, "audio.wav")
        audio = v.audio()
        ganho = 0.84
        for _ in range(12):     # mede o pico real já em AAC e baixa o ganho (0,5 dB por vez) até -1 dBTP ou menos
            r.salvar_wav(wav, audio * ganho)
            m4a = os.path.join(tmp, "teste.m4a")
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", wav, "-c:a", "aac", "-b:a", "128k", "-ar", str(SR),
                            "-ac", "2", "-flags:a", "+bitexact", m4a], check=True)
            pico = medir_audio(m4a)["pico_real_dbtp"]
            if pico is None or pico <= -1.0:
                break
            ganho *= 10 ** (-0.5 / 20)      # passo fixo: o pico do AAC não cai em linha reta com o ganho
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
    info["audio_medido"] = medir_audio(saida)
    info["ganho_audio"] = round(ganho, 3)
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
           "audio_medido": info["audio_medido"], "ganho_audio": info["ganho_audio"], "avisos_zona": info["avisos_zona"], "teto_kbps": info["teto_kbps"],
           "capa_kb": round(kb, 1)}
    if hasattr(v, "seq_cartas"):
        out["ordem_cartas"] = [(round(v.seq_inicio + k * v.seq_dur, 2), n) for k, n in enumerate(v.seq_cartas)]
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Vídeos do C07 Simpatia da Virada")
    ap.add_argument("--so", choices=sorted(PECAS) + ["kit", "previa"], help="só uma peça (ou só o kit / a prévia)")
    ap.add_argument("--nome", default=NOME_PADRAO, help="nome publicado do filtro (padrão: Simpatia da Virada)")
    ap.add_argument("--pasta", default=AQUI, help="pasta de saída (padrão: a pasta deste arquivo)")
    ap.add_argument("--rapido", metavar="DIR", help="só pranchas rápidas da linha do tempo, sem mp4")
    ap.add_argument("--troca", action="append", default=[], metavar="N=Rk",
                    help="carta N publicada com a reserva Rk no lugar (ex.: 1=R4). Pode repetir.")
    a = ap.parse_args(argv)
    for tr in a.troca:
        n, rk = tr.split("=")
        TROCAS[int(n)] = RESERVAS[rk.strip().upper()]
    if a.rapido:
        os.makedirs(a.rapido, exist_ok=True)
        for cod, (fv, fc, _) in PECAS.items():
            v = fv(a.nome)
            v.prancha(os.path.join(a.rapido, f"{cod}_rapida.png"), n=12)
            fc(a.nome).save(os.path.join(a.rapido, f"{cod}_capa.png"))
        capa_m1(a.nome).save(os.path.join(a.rapido, "C07-M1_capa.png"))
        print("ok", a.rapido)
        return
    os.makedirs(a.pasta, exist_ok=True)
    res = {}
    cods = sorted(PECAS) if a.so is None else ([a.so] if a.so in PECAS else [])
    for cod in cods:
        res[cod] = renderizar_peca(cod, a.pasta, a.nome)
    if a.so in (None, "kit"):
        res["kit-C07-M1"] = kit_m1(os.path.join(a.pasta, "kit-C07-M1"), a.nome)
    if a.so in (None, "previa"):
        mp4s = [(c, os.path.join(a.pasta, f"{c}.mp4")) for c in sorted(PECAS)]
        if all(os.path.exists(p) for _, p in mp4s):
            res["previa"] = previa(mp4s, os.path.join(a.pasta, "previa-videos.png"))
    total = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(a.pasta) for f in fs)
    res["total_pasta_bytes"] = total
    res["total_pasta_mb"] = round(total / 1024 / 1024, 2)
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
