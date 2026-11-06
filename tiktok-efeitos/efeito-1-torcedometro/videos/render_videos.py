#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_videos.py: vídeos do C01 "Torcedômetro" (peças N), capas, legendas e o kit da peça M.

Usa a biblioteca da equipe: tiktok-efeitos/videos/lib/render.py (não editar a biblioteca daqui).
Tudo é determinístico: rodar de novo gera os mesmos arquivos (o MP4 sai com o x264 em 1 thread; ver
renderizar_deterministico).

Rodar (da pasta que for):
    python3 render_videos.py                      # tudo: C01-V1, C01-V2, C01-V3, capas, legendas, kit M1, prévia
    python3 render_videos.py --so C01-V2          # só uma peça (mp4 + capa + legenda)
    python3 render_videos.py --rapido DIR         # pranchas rápidas da linha do tempo (sem mp4), em DIR
    python3 render_videos.py --nome Torcedometro  # se o nome publicado sair diferente (ex.: sem acento)

Saída (nesta pasta):
    C01-V1.mp4  C01-V2.mp4  C01-V3.mp4
    C01-Vn-capa.jpg  C01-Vn-legenda.txt
    kit-C01-M1/ (gancho.png, gancho-baixo.png, final.png, assinatura.wav, capa.jpg, legenda.txt)
    previa-videos.png
"""
from __future__ import annotations

import argparse
import json
import math
import os
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
from PIL import Image, ImageDraw  # noqa: E402

# ============================================================================
# Caminhos e dados do efeito
# ============================================================================
ASSETS = os.path.normpath(os.path.join(AQUI, "..", "assets"))
SIMBOLO = os.path.normpath(os.path.join(AQUI, "..", "..", "videos", "perfil", "simbolo_transparente.png"))
TITULO_TOQUE = os.path.join(ASSETS, "titulo_toque.png")
TITULO = os.path.join(ASSETS, "titulo.png")
CARTAS = [os.path.join(ASSETS, "cartas", f"carta_{i:02d}.png") for i in range(1, 27)]

NOME_PADRAO = "Torcedômetro"     # nome exato do textos.md

# Layout (quadro 1080x1920). As cartas ocupam os 512 px inteiros do PNG; na escala 1,6 dão 819 px.
# Centradas em x = 540 passariam 10 px da zona segura da direita (x 940). Por isso o miolo fica em x = 520
# (110 a 930), o que também afasta tudo da coluna de botões do TikTok.
CX = 520
ESC = 1.6
GANCHO_Y = 390
CARTA_Y = 830
CABECA_Y = 1255
CABECA_H = 220
AMARELO = "#FFD43B"
ESCURO = "#1B1D24"

# 20 das 26 cartas para o "pausa e vê o seu" (as mais engraçadas).
# Fora: 11 radinho, 14 reza (tema religioso), 21 calculadora, 22 buzina e 23 carreata (carro e carreata
# ficam fora para não puxar loja nem política) e 24 videogame.
SELECAO_V2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 15, 16, 17, 18, 19, 20, 25, 26]

# Roletas dos vídeos: 24 das 26 cartas. Ficam fora a 14 (REZA ATÉ NO ESCANTEIO, mãos de reza 🙏) e a 23
# (FAZ CARREATA POR EMPATE, lembra campanha política). As duas estão no efeito (risco baixo), mas o vídeo
# pode ser pausado em qualquer quadro e a lista "Nunca" do plano veta símbolo religioso.
ROLETA = [n for n in range(1, 27) if n not in (14, 23)]
CARTAS_ROLETA = [CARTAS[n - 1] for n in ROLETA]


# ============================================================================
# Som: apito (assinatura do C01), feito aqui com numpy
# ============================================================================
SR = r.SR


def som_apito(dur=0.13, f=2500.0, trinado=31.0, profundidade=0.03, semente=0, queda=0.0):
    """Apito de juiz sintetizado: tom ~2,5 kHz com o 'trinado' da bolinha (FM + AM) e um pouco de sopro."""
    n = int(round(dur * SR))
    t = np.arange(n) / SR
    rng = np.random.default_rng(500 + int(semente))
    fase0 = rng.uniform(0, 2 * math.pi)
    trem = np.sin(2 * math.pi * trinado * t + fase0)
    freq = f * (1 + profundidade * trem) * (1 - queda * (t / dur) ** 2)
    fase = 2 * math.pi * np.cumsum(freq) / SR
    tom = np.sin(fase) + 0.16 * np.sin(2 * fase) + 0.04 * np.sin(3 * fase)
    am = 0.74 + 0.26 * (0.5 + 0.5 * trem)
    ruido = rng.standard_normal(n)
    esp = np.fft.rfft(ruido)
    fr = np.fft.rfftfreq(n, 1 / SR)
    esp *= np.exp(-((fr - f) / (f * 0.35)) ** 2)
    sopro = np.fft.irfft(esp, n)
    sopro /= (np.max(np.abs(sopro)) + 1e-9)
    env = np.minimum(1, t / 0.010) * np.clip((dur - t) / 0.035, 0, 1)
    s = (tom * am + 0.14 * sopro) * env
    return (s / (np.max(np.abs(s)) + 1e-9) * 0.85).astype(np.float32)


def apito_curto():
    return som_apito(0.14, semente=1)


def apito_duplo():
    """Dois apitos curtos (o 2º um pouco mais longo): a assinatura do C01."""
    a, b = som_apito(0.12, semente=2), som_apito(0.17, semente=3)
    n = int(0.21 * SR) + len(b)
    s = np.zeros(n, np.float32)
    s[:len(a)] += a
    s[int(0.21 * SR):int(0.21 * SR) + len(b)] += b
    return s


def apito_longo():
    return som_apito(0.85, f=2450.0, semente=4, queda=0.04)


# ============================================================================
# Peças de tela
# ============================================================================
def fundo_c01(variante=0):
    """Fundo roxo -> turquesa com o padrão 'mais' (igual nas 3 peças, com pequenas variações)."""
    cores = [
        ["#2A1563", "#3D1F8A", "#0F5C66", "#157F7B", "#3D1F8A"],
        ["#311870", "#22146A", "#0E6670", "#18908A", "#22146A"],
        ["#2A1563", "#46229A", "#0F5C66", "#11706C", "#46229A"],
    ][variante % 3]
    vel = [(0, 70), (40, 60), (0, -70)][variante % 3]
    return r.Padrao("mais", cor_forma=(255, 255, 255, 30), tamanho=180, velocidade=vel,
                    fundo=r.DegradeAnimado(cores, angulo=100, velocidade=0.05))


def cabeca(v, emoji, ini, fim, entrada=None, saida=None, nome=None):
    """No lugar da cabeça da pessoa, uma carinha emoji (nada de rosto ou silhueta humana)."""
    img = r.emoji_img(emoji, CABECA_H)
    v.imagem(img, ini, fim, centro=(CX, CABECA_Y), entrada=entrada, saida=saida, ocioso="flutuar",
             som=(entrada == "pop"), z=14, nome=nome)


def bola(v, ini, fim):
    """⚽ quicando ao lado da 'cabeça'."""
    img = r.emoji_img("⚽", 104)
    v.imagem(img, ini, fim, centro=lambda tl: (CX + 215, CABECA_Y + 70 - 80 * abs(math.sin(math.pi * tl / 0.6))),
             rotacao=lambda tl: -160 * tl, entrada=None, saida="pop", som=False, z=15, nome="bola")


def cortina(v, bg, t0, fim, z=52):
    """O cartão final entra de baixo para cima, cobrindo tudo (inclusive o confete)."""
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


def cartao_final(v, bg, t0, fim, pergunta, nome_filtro, estatico=False):
    """CF: símbolo do perfil + 'Procura na lupa 🔎' + nome do filtro em amarelo (1 linha) + pergunta."""
    if not estatico:
        cortina(v, bg, t0, fim)
        v.som(apito_duplo(), t0 + 0.05, 0.24)
    e = (lambda d: None) if estatico else (lambda d: "pop")
    dt = (lambda d: t0) if estatico else (lambda d: t0 + d)
    v.imagem(SIMBOLO, dt(0.12), fim, centro=(CX, 590), escala=0.40, entrada=e(0), som=False,
             ocioso="flutuar", z=61, nome="símbolo")
    v.texto("Procura na lupa 🔎", dt(0.22), fim, centro=(CX, 868), tamanho=80, fonte="black",
            entrada=e(0), saida=None, som=False, z=62, nome="lupa")
    v.texto(f"*{nome_filtro}*", dt(0.32), fim, centro=(CX, 995), tamanho=132, max_linhas=1, contorno=12,
            entrada=e(0), saida=None, ocioso=None if estatico else "pulsar", som=not estatico, z=62,
            nome="nome do filtro")
    v.texto(pergunta, dt(0.50), fim, centro=(CX, 1160), tamanho=64, fonte="black", cor=ESCURO, contorno=0, max_linhas=1,
            caixa="#FFFFFF", sombra=(0, 6, 10, 110), entrada=e(0), saida=None, som=False,
            z=62, nome="pergunta")


def ordem_por_brilho(numeros):
    """Cartas em ordem de brilho (luminância média), para trocas suaves no 'pausa' (luz piscante)."""
    def lum(n):
        im = Image.open(CARTAS[n - 1]).convert("RGBA")
        a = np.asarray(im, dtype=np.float64)
        m = a[..., 3] > 128
        rgb = a[..., :3][m]
        return float((0.2126 * rgb[:, 0] + 0.7152 * rgb[:, 1] + 0.0722 * rgb[:, 2]).mean())
    return sorted(numeros, key=lambda n: (round(lum(n), 3), n))


# ============================================================================
# As peças N
# ============================================================================
def video_v1(nome):
    """C01-V1 · 'Roleta do torcedor' · 10 s."""
    v = r.Video(10.0, semente=101)
    bg = fundo_c01(0)
    v.fundo(bg)
    v.trilha(volume=0.26, bpm=120, progressao=[(43, ""), (48, ""), (45, "m"), (41, "")], ducking=0.5)
    v.som(apito_curto(), 0.06, 0.20)
    # 0–1,8 s: gancho + carta 8 balançando + ⚽ 🤔 (tudo no 1º quadro)
    v.texto("Que tipo de *torcedor* você é?", 0.0, 6.6, centro=(CX, GANCHO_Y), tamanho=96, max_linhas=2,
            entrada=None, saida="pop", ocioso="pulsar", nome="gancho")
    v.imagem(CARTAS[7], 0.0, 1.8, centro=(CX, CARTA_Y), escala=ESC, entrada=None, saida="pop", dur_saida=0.2,
             ocioso="balancar", nome="carta 8")
    cabeca(v, "🤔", 0.0, 6.6)
    bola(v, 0.0, 2.6)
    # 1,8–2,6 s: título com "toque na tela" + dedo
    v.imagem(TITULO_TOQUE, 1.8, 2.6, centro=(CX, CARTA_Y), escala=ESC, entrada="pop", dur_entrada=0.3,
             ocioso="flutuar", nome="título")
    v.toque(2.05, centro=(CX + 205, CARTA_Y + 150))
    v.som("vush", 2.42, 0.35)
    # 2,6–6,6 s: roleta das 26 cartas, para na 3 PÉ-FRIO CERTIFICADO
    t_res = v.roleta(CARTAS_ROLETA, ROLETA.index(3), inicio=2.6, duracao=4.0, centro=(CX, CARTA_Y), escala=ESC, fim=8.35,
                     intervalo_ini=0.075, nome="roleta")
    cabeca(v, "🥶", t_res, 8.35, entrada="pop")
    # 6,6–8 s: reação. z=51: acima do confete (50) e abaixo da cortina do cartão final (52). Com z=60 (QA 06/11)
    # o texto ficava por cima do cartão final de 8,0 a 8,35 s e encostava no símbolo.
    v.texto("Isso explica\n*muita coisa* 🥶", t_res + 0.12, 8.35, centro=(CX, GANCHO_Y), tamanho=96, max_linhas=2,
            entrada="pop", saida=None, z=51, nome="reação")
    # 8–10 s: cartão final
    cartao_final(v, bg, 8.0, 10.0, "Serve pra qualquer time ⚽", nome)
    return v


def video_v2(nome):
    """C01-V2 · 'Pausa e vê o seu' · 9 s."""
    v = r.Video(9.0, semente=102)
    bg = fundo_c01(1)
    v.fundo(bg)
    v.trilha(volume=0.20, bpm=132, progressao=[(45, "m"), (43, ""), (41, ""), (43, "")], ducking=0.4)
    dur = 0.35                      # 2,86 trocas por segundo (limite do plano: 3)
    seq = ordem_por_brilho(SELECAO_V2)
    v.texto("*PAUSA AGORA* ⏸️\ne vê o seu", 0.0, 7.35, centro=(CX, GANCHO_Y), tamanho=104, max_linhas=2,
            entrada=None, saida=None, ocioso="pulsar", nome="gancho")
    v.slides([CARTAS[n - 1] for n in seq], 0.0, dur_cada=dur, transicao="corte", centro=(CX, CARTA_Y),
             escala=ESC, fim=7.35, nome="cartas")
    for k in range(len(seq)):
        v.som("tique", k * dur, 0.55, 0.0, freq=2350 if k % 2 == 0 else 2150, semente=k % 5)
    cabeca(v, "🤔", 0.0, 7.35)
    cartao_final(v, bg, 7.0, 9.0, "Qual pegou? Conta aqui 👇", nome)
    v.seq_cartas = seq
    return v


def video_v3(nome):
    """C01-V3 · 'Dia de final' · 12 s."""
    v = r.Video(12.0, semente=103)
    bg = fundo_c01(2)
    v.fundo(bg)
    v.trilha(volume=0.26, bpm=124, progressao=[(41, ""), (43, ""), (45, "m"), (40, "m")], ducking=0.5)
    v.som(apito_curto(), 0.06, 0.19)
    # 0–2 s: gancho + carta 19
    v.texto("Dia de final:\n*gira antes do jogo*", 0.0, 8.0, centro=(CX, GANCHO_Y), tamanho=96, max_linhas=2,
            entrada=None, saida="pop", ocioso="pulsar", nome="gancho")
    v.imagem(CARTAS[18], 0.0, 2.0, centro=(CX, CARTA_Y), escala=ESC, entrada=None, saida="pop", dur_saida=0.22,
             ocioso="balancar", nome="carta 19")
    cabeca(v, "🤔", 0.0, 8.0)
    # 2–4 s: 3, 2, 1, GIRA!
    v.contagem(2.0, de=3, dur_cada=0.5, centro=(CX, CARTA_Y), tamanho=360, final="GIRA!")
    v.toque(3.5, centro=(CX + 150, CARTA_Y + 120))
    # 4–8 s: roleta para na 13 NÃO OLHA O PÊNALTI + apito longo
    t_res = v.roleta(CARTAS_ROLETA, ROLETA.index(13), inicio=4.0, duracao=4.0, centro=(CX, CARTA_Y), escala=ESC, fim=10.35,
                     intervalo_ini=0.075, nome="roleta")
    v.som(apito_longo(), t_res + 0.03, 0.18)
    cabeca(v, "🙈", t_res, 10.35, entrada="pop")
    # 8–10 s: reação (z=51: a cortina do cartão final cobre o texto; ver video_v1)
    v.texto("Liberado pra\nassistir…\n*de costas* 🙈", t_res + 0.15, 10.35, centro=(CX, GANCHO_Y + 10), tamanho=92,
            max_linhas=3, entrada="pop", saida=None, z=51, nome="reação")
    # 10–12 s: cartão final
    cartao_final(v, bg, 10.0, 12.0, "Serve pra qualquer time ⚽", nome)
    return v


# ============================================================================
# Capas, legendas e kit da M1
# ============================================================================
def _capa(texto, cartas, emoji, rodape, variante):
    """Capa 1080x1920: texto grande e cartas dentro do miolo 3:4 (y 240 a 1680)."""
    v = r.Video(1.0, semente=110 + variante)
    v.fundo(fundo_c01(variante))
    v.texto(texto, 0, None, centro=(CX, 450), tamanho=138, entrada=None, saida=None, contorno=14,
            largura_max=860, max_linhas=2)
    if len(cartas) == 1:
        v.imagem(cartas[0], 0, None, centro=(CX, 905), escala=ESC, entrada=None, som=False)
    else:   # leque de cartas
        for i, (c, rot, dx, dy) in enumerate(zip(cartas, (10, -8, 0), (-48, 44, 0), (-96, -52, 0))):
            v.imagem(c, 0, None, centro=(CX + dx, 925 + dy), escala=ESC * 0.96, rotacao=rot, entrada=None,
                     som=False, z=10 + i)
    v.imagem(r.emoji_img(emoji, 210), 0, None, centro=(CX, 1305), entrada=None, som=False)
    if rodape:   # 1 linha só: com nome publicado mais longo (--nome), a fonte diminui em vez de quebrar a linha
        v.texto(rodape, 0, None, centro=(CX, 1520), tamanho=64, fonte="black", entrada=None, saida=None,
                max_linhas=1)
    return v.quadro(0.0)


def capa_v1(nome):
    return _capa("QUE TORCEDOR\n*VOCÊ É?*", [CARTAS[2]], "🥶", f"Filtro: *{nome}* 🔎", 0)


def capa_v2(nome):
    return _capa("*PAUSA* E\nVÊ O SEU ⏸️", [CARTAS[25], CARTAS[5], CARTAS[0]], "🤔", f"Filtro: *{nome}* 🔎", 1)


def capa_v3(nome):
    return _capa("DIA DE FINAL:\n*GIRA ANTES* ⚽", [CARTAS[18]], "🤔", f"Filtro: *{nome}* 🔎", 2)


def capa_m1(nome):
    return _capa("FUNCIONA\nASSIM 👇", [TITULO], "🤔", f"*{nome.upper()}* 🔎", 0)


def legendas(nome):
    """Legenda + hashtags (até 5), prontas para colar. 'ou no meu perfil' só depois da conferência da aba."""
    return {
        "C01-V1": f"Que torcedor você é? Gira e me conta qual saiu. Nome do filtro: {nome} 🔎 procura na lupa\n\n"
                  "#torcedometro #filtro #filtrotiktok #futebol #torcedor",
        "C01-V2": f"Pausa o vídeo e vê que torcedor você é ⏸️ Qual pegou? Filtro: {nome} 🔎 na lupa\n\n"
                  "#torcedometro #filtrotiktok #futebol #torcedor #zoeira",
        "C01-V3": f"Dia de final: gira antes do jogo e vê se pode assistir 😅 Serve pra qualquer time. "
                  f"Filtro: {nome} 🔎\n\n#torcedometro #filtrotiktok #diadefinal #futebol #torcedor",
        "C01-M1": f"Funciona assim: toca na tela e o filtro diz que torcedor você é. Serve pra qualquer time. "
                  f"Filtro: {nome} 🔎\n\n#torcedometro #filtro #filtrotiktok #futebol #diadefinal",
    }


def _salvar_wav_mono(caminho, x):
    """WAV 16 bits, 44,1 kHz, mono (metade do tamanho; o Clipchamp aceita)."""
    m = np.asarray(x, dtype=np.float64)
    if m.ndim == 2:
        m = m.mean(axis=1)
    m = m / (np.max(np.abs(m)) + 1e-9) * 0.84
    x16 = (np.clip(m, -1, 1) * 32767).astype("<i2")
    with wave.open(caminho, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(np.ascontiguousarray(x16).tobytes())


def _png_transparente(texto_img, centro):
    tela = Image.new("RGBA", (r.W, r.H), (0, 0, 0, 0))
    r.colar(tela, texto_img, centro)
    return tela


def kit_m1(pasta, nome):
    """Kit da C01-M1 para o Montador finalizar no Clipchamp."""
    os.makedirs(pasta, exist_ok=True)
    estilo = dict(tamanho=66, fonte_nome="black", cor=ESCURO, cor_destaque="#B8860B", contorno=0,
                  sombra=(0, 6, 10, 120), largura_max=820, caixa="#FFFFFF", caixa_pad=(36, 22))
    g1 = r.texto_img("Funciona assim 👇\nserve pra qualquer time", **estilo)
    g2 = r.texto_img("Funciona assim 👆\nserve pra qualquer time", **estilo)
    _png_transparente(g1, (CX, 330)).save(os.path.join(pasta, "gancho.png"), optimize=True)
    _png_transparente(g2, (CX, 1385)).save(os.path.join(pasta, "gancho-baixo.png"), optimize=True)
    # final.png: o mesmo cartão final dos vídeos, parado, com a pergunta da M1
    v = r.Video(3.0, semente=120)
    bg = fundo_c01(0)
    v.fundo(bg)
    cartao_final(v, bg, 0.0, None, "Gira antes do jogo ⚽", nome, estatico=True)
    v.quadro(1.0).save(os.path.join(pasta, "final.png"), optimize=True)
    # assinatura.wav: trilha 120 bpm + apito curto no começo + apito duplo quando entra o final (9,5 s)
    a = r.Video(12.0, semente=121)
    a.trilha(volume=0.30, bpm=120, progressao=[(45, "m"), (41, ""), (48, ""), (43, "")], ducking=0.5)
    a.som(apito_curto(), 0.10, 0.22)
    a.som(apito_duplo(), 9.50, 0.26)
    _salvar_wav_mono(os.path.join(pasta, "assinatura.wav"), a.audio())
    r.salvar_jpg(capa_m1(nome), os.path.join(pasta, "capa.jpg"), max_kb=260)
    with open(os.path.join(pasta, "legenda.txt"), "w", encoding="utf-8") as f:
        f.write(legendas(nome)["C01-M1"] + "\n")
    return sorted(os.listdir(pasta))


# ============================================================================
# Prévia (prancha de 6 quadros por vídeo)
# ============================================================================
TEMPOS_PREVIA = {
    "C01-V1": [0.0, 0.5, 2.2, 6.9, 7.6, 9.5],
    "C01-V2": [0.0, 0.5, 2.6, 5.4, 6.9, 8.6],
    "C01-V3": [0.0, 0.5, 3.6, 8.5, 9.6, 11.5],
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
PECAS = {"C01-V1": (video_v1, capa_v1, 1900), "C01-V2": (video_v2, capa_v2, 2000), "C01-V3": (video_v3, capa_v3, 1750)}


def renderizar_deterministico(v, saida, kbps, limite_bytes):
    """Igual ao Video.renderizar da biblioteca (mesmos parâmetros do ffmpeg), mas com o x264 em 1 thread.
    Motivo: com várias threads + teto de bitrate (VBV), o x264 gera bytes diferentes a cada rodada, mesmo com os
    quadros idênticos (conferido aqui). Em 1 thread o MP4 sai igual byte a byte. Se passar do limite de tamanho,
    refaz com teto 15% menor (sem as 2 passadas da biblioteca, que também usam várias threads)."""
    t0 = time.time()
    n = int(round(v.duracao * v.fps))
    tmp = tempfile.mkdtemp(prefix="c01_render_")
    try:
        wav = os.path.join(tmp, "audio.wav")
        # -1 dB de folga: a masterização da biblioteca deixa o pico em -1,5 dBFS, mas depois do AAC o pico real
        # chegou a -0,1 dBFS no C01-V2 (risco de estalo). Com -1 dB fica perto de -1 dBFS.
        r.salvar_wav(wav, v.audio() * 0.891)
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


def renderizar_peca(cod, pasta, nome):
    fv, fc, kbps = PECAS[cod]
    v = fv(nome)
    mp4 = os.path.join(pasta, f"{cod}.mp4")
    # 4 MB no máximo (ficha 2.3); o teto de bitrate deixa folga para a pasta inteira caber em 12 MB
    info = renderizar_deterministico(v, mp4, kbps, int(4.0 * 1024 * 1024))
    q, kb = r.salvar_jpg(fc(nome), os.path.join(pasta, f"{cod}-capa.jpg"), max_kb=260)
    with open(os.path.join(pasta, f"{cod}-legenda.txt"), "w", encoding="utf-8") as f:
        f.write(legendas(nome)[cod] + "\n")
    out = {"arquivo": os.path.basename(mp4), "duracao_s": info["duracao_s"], "tamanho_bytes": info["tamanho_bytes"],
           "codecs": info["codecs"], "video": info["video"], "audio": info["audio"],
           "avisos_zona": info["avisos_zona"], "teto_kbps": info["teto_kbps"],
           "capa_kb": round(kb, 1)}
    if hasattr(v, "seq_cartas"):
        out["ordem_cartas"] = v.seq_cartas
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Vídeos do C01 Torcedômetro")
    ap.add_argument("--so", choices=sorted(PECAS) + ["kit", "previa"], help="só uma peça (ou só o kit / a prévia)")
    ap.add_argument("--nome", default=NOME_PADRAO, help="nome publicado do filtro (padrão: Torcedômetro)")
    ap.add_argument("--pasta", default=AQUI, help="pasta de saída (padrão: a pasta deste arquivo)")
    ap.add_argument("--rapido", metavar="DIR", help="só pranchas rápidas da linha do tempo, sem mp4")
    a = ap.parse_args(argv)
    if a.rapido:
        os.makedirs(a.rapido, exist_ok=True)
        for cod, (fv, fc, _) in PECAS.items():
            v = fv(a.nome)
            v.prancha(os.path.join(a.rapido, f"{cod}_rapida.png"), n=12)
            fc(a.nome).save(os.path.join(a.rapido, f"{cod}_capa.png"))
        print("ok", a.rapido)
        return
    os.makedirs(a.pasta, exist_ok=True)
    res = {}
    cods = sorted(PECAS) if a.so in (None,) else ([a.so] if a.so in PECAS else [])
    for cod in cods:
        res[cod] = renderizar_peca(cod, a.pasta, a.nome)
    if a.so in (None, "kit"):
        res["kit-C01-M1"] = kit_m1(os.path.join(a.pasta, "kit-C01-M1"), a.nome)
    if a.so in (None, "previa"):
        mp4s = [(c, os.path.join(a.pasta, f"{c}.mp4")) for c in sorted(PECAS)]
        if all(os.path.exists(p) for _, p in mp4s):
            res["previa"] = previa(mp4s, os.path.join(a.pasta, "previa-videos.png"))
    total = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(a.pasta) for f in fs)
    res["total_pasta_mb"] = round(total / 1024 / 1024, 2)
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
