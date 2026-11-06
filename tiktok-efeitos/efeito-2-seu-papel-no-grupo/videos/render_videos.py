#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vídeos do efeito C08 "Eu no grupo da família" (vídeos-cartaz, sem pessoa e sem rosto).

Gera nesta pasta (videos/):
  C08-V1.mp4, C08-V2.mp4, C08-V3.mp4   peças N: 1080x1920, 30 fps, H.264 + AAC, som nosso
  C08-Vx-capa.jpg                      capa para "Editar capa -> Carregar" (texto no miolo 3:4)
  C08-Vx-legenda.txt                   legenda + hashtags, pronta para colar
  kit-C08-M1/                          kit da gravação do Montador (gancho.png, final.png,
                                       assinatura.wav, capa.jpg, legenda.txt)
  previa-videos.png                    6 quadros de cada mp4 (vermelho = interface do TikTok)

Uso:
  python3 render_videos.py                      # tudo
  python3 render_videos.py --so C08-V2          # só uma peça (mp4 + capa + legenda)
  python3 render_videos.py --sem-mp4            # só capas, legendas, kit e prévia
  python3 render_videos.py --nome "Outro nome"  # se o nome publicado sair diferente (refaz tela, capa e legenda)

Usa a biblioteca ../../videos/lib/render.py (não altera nada nela) e as artes de ../assets (só lê).
Determinístico: cada peça tem semente fixa, e o mp4 sai igual byte a byte em duas rodadas
(ver renderizar_det: contorno do pipe com vários threads da biblioteca).
"""
from __future__ import annotations

import argparse
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

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.dont_write_bytecode = True       # não cria __pycache__ na pasta da biblioteca nem aqui
AQUI = os.path.dirname(os.path.abspath(__file__))
EFEITO = os.path.dirname(AQUI)                       # efeito-2-seu-papel-no-grupo
RAIZ = os.path.dirname(EFEITO)                       # tiktok-efeitos
sys.path.insert(0, os.path.join(RAIZ, "videos", "lib"))
import render as r  # noqa: E402

W, H = r.W, r.H
ASSETS = os.path.join(EFEITO, "assets")
SIMBOLO = os.path.join(RAIZ, "videos", "perfil", "simbolo_transparente.png")

with open(os.path.join(EFEITO, "textos.json"), encoding="utf-8") as _f:
    TEXTOS = json.load(_f)
NOME = TEXTOS["nome"]                                # "Eu no grupo da família" (pode trocar com --nome)

CARTAS = r.carregar_pasta(os.path.join(ASSETS, "cartas"), "opcao_*.png")
if len(CARTAS) != 28:
    raise SystemExit(f"Esperava 28 cartas em assets/cartas, achei {len(CARTAS)}")
TITULO = r.carregar(os.path.join(ASSETS, "titulo.png"))


def carta(n):
    """Carta pelo número do textos.md (1..28)."""
    return CARTAS[n - 1]


# ============================================================================
# Visual do C08
# ============================================================================
CONTORNO = "#26093F"          # roxo bem escuro (contorno do texto)
AMARELO = "#FFD43B"
ESC = 1.55                    # carta: 502 px visíveis -> 778 px (cabe nos 800 px da zona segura)
CX = 540
Y_GANCHO = 340
Y_CARTA = 800
Y_CABECA = 1290
POS_TOQUE = (800, 1170)
SOMBRA = (0, 8, 14, 150)
T_CORTINA = 0.30


def fundo_c08(neve=False):
    """Rosa -> roxo que flui devagar, com bolinhas. Nada de verde nem de tela de conversa."""
    grad = r.DegradeAnimado(["#D8338A", "#A22FC6", "#6228BA", "#A22FC6"], angulo=100, velocidade=0.045, giro=8)
    if neve:   # V3: bolinhas brancas caindo, como neve
        return r.Padrao("bolinhas", cor_forma=(255, 255, 255, 48), fundo=grad, tamanho=124, velocidade=(8, 120))
    return r.Padrao("bolinhas", cor_forma=(255, 255, 255, 30), fundo=grad, tamanho=150, velocidade=(12, -34))


class Baloes:
    """Balões 💬 subindo devagar pelas laterais (decoração, atrás de tudo)."""

    def __init__(self, semente, n=8, opac=(0.28, 0.48)):
        rng = random.Random(semente)
        self.itens = []
        for i in range(n):
            x = rng.uniform(18, 120) if i % 2 == 0 else rng.uniform(962, 1062)
            self.itens.append(dict(x=x, y0=(i + rng.uniform(0.1, 0.9)) * (H + 300) / n, alt=rng.choice([74, 92, 110, 128]),
                                   vel=rng.uniform(40, 75), fase=rng.uniform(0, 6.28), amp=rng.uniform(8, 20),
                                   ang=rng.uniform(-14, 14), op=rng.uniform(*opac)))

    def desenhar(self, canvas, t):
        per = H + 300
        for b in self.itens:
            y = (b["y0"] - b["vel"] * t) % per - 150
            x = b["x"] + b["amp"] * math.sin(1.3 * t + b["fase"])
            rot = b["ang"] + 5 * math.sin(0.9 * t + b["fase"])
            r.colar(canvas, r.emoji_img("💬", b["alt"]), (x, y), 1.0, rot, b["op"])


class Cenario:
    """Fundo + balões. Serve de fundo do vídeo e de 'cortina' antes do cartão final."""

    def __init__(self, semente, neve=False):
        self.fundo = fundo_c08(neve)
        self.baloes = Baloes(semente)

    def quadro(self, t):
        im = self.fundo.quadro(t)
        self.baloes.desenhar(im, t)
        return im


def emoji_cabeca(e, tam=290):
    return r.emoji_img(e, tam)


def cabeca(v, e, inicio, fim, entrada=None, saida=None, nome="cabeça"):
    """A 'cabeça' é uma carinha emoji (nunca pessoa). O balão da carta aponta para ela."""
    v.imagem(emoji_cabeca(e), inicio, fim, centro=(CX, Y_CABECA), entrada=entrada, saida=saida,
             dur_entrada=0.3, dur_saida=0.2, ocioso="flutuar", z=11, nome=nome)


def gancho(v, texto, fim, tamanho=96, saida="pop"):
    """Texto do gancho: já aparece no 1º quadro (entrada None)."""
    v.texto(texto, 0.0, fim, centro=(CX, Y_GANCHO), tamanho=tamanho, max_linhas=2, cor_contorno=CONTORNO,
            sombra=SOMBRA, entrada=None, saida=saida, dur_saida=0.2, ocioso="pulsar", z=20, nome="gancho")


def topo(v, texto, inicio, fim, tamanho=84, cor="#FFFFFF", saida="pop", z=20, nome="texto do topo", som=True):
    v.texto(texto, inicio, fim, centro=(CX, Y_GANCHO), tamanho=tamanho, max_linhas=2, cor=cor,
            cor_contorno=CONTORNO, sombra=SOMBRA, entrada="pop", saida=saida, dur_saida=0.2, som=som, z=z, nome=nome)


# ---------------------------------------------------------------- som
def assinatura(v, t, vol=1.0):
    """Assinatura do C08: plim duplo genérico ('mensagem nova', sem imitar app nenhum) + pop."""
    v.som(r.som_plim(nota=1396.91, duas=True, dur=0.8), t, 0.5 * vol)
    v.som(r.som_pop(f0=420.0, f1=1300.0, dur=0.11), t + 0.24, 0.55 * vol)


def som_sininho(semente=0, dur=0.24):
    """Sininho de Natal (guizo) sintetizado: parciais agudas + chiado curto, 3 batidas rápidas."""
    n = int(dur * r.SR)
    t = np.arange(n) / r.SR
    rng = np.random.default_rng(500 + semente)
    env = np.zeros(n)
    for k, off in enumerate((0.0, 0.017, 0.033)):
        i0 = int(off * r.SR)
        env[i0:] += (0.75 ** k) * np.exp(-t[: n - i0] / 0.035)
    s = np.zeros(n)
    for f, a in ((5300, 1.0), (6950, 0.7), (8700, 0.45), (10900, 0.3)):
        s += a * np.sin(2 * np.pi * f * rng.uniform(0.985, 1.015) * t + rng.uniform(0, 6.28))
    ruido = np.diff(rng.standard_normal(n), prepend=0.0)
    s = s * env * 0.6 + ruido * env * 0.35
    s *= np.minimum(1, t / 0.001)
    return (s / (np.max(np.abs(s)) + 1e-9) * 0.8).astype(np.float32)


# ---------------------------------------------------------------- cartão final
def avatar(diam=300):
    """Símbolo do perfil (com a mira) num círculo com o degradê da foto de perfil e anel branco."""
    S = 2
    D = diam * S
    yy, xx = np.mgrid[0:D, 0:D]
    p = np.clip((xx + yy) / (2 * D), 0, 1)
    cores = [r.rgb("#7B3BF0"), r.rgb("#D54BD8"), r.rgb("#F06BA8"), r.rgb("#FF9A4D")]
    pos = np.linspace(0, 1, len(cores))
    arr = np.stack([np.interp(p, pos, [c[i] for c in cores]) for i in range(3)], axis=-1).astype(np.uint8)
    grad = Image.fromarray(arr, "RGB").convert("RGBA")
    anel = 9 * S
    mask_total = Image.new("L", (D, D), 0)
    ImageDraw.Draw(mask_total).ellipse([0, 0, D - 1, D - 1], fill=255)
    mask_in = Image.new("L", (D, D), 0)
    ImageDraw.Draw(mask_in).ellipse([anel, anel, D - 1 - anel, D - 1 - anel], fill=255)
    im = Image.new("RGBA", (D, D), (255, 255, 255, 0))
    branco = Image.new("RGBA", (D, D), (255, 255, 255, 255))
    im.paste(branco, (0, 0), mask_total)
    im.paste(grad, (0, 0), mask_in)
    sim = r.carregar(SIMBOLO)
    bb = sim.getchannel("A").getbbox()
    sim = sim.crop(bb)
    alvo = (D - 2 * anel) * 0.80
    k = alvo / max(sim.size)
    sim = sim.resize((int(sim.width * k), int(sim.height * k)), Image.LANCZOS)
    camada = Image.new("RGBA", (D, D), (0, 0, 0, 0))
    camada.alpha_composite(sim, ((D - sim.width) // 2, (D - sim.height) // 2 + int(0.02 * D)))
    camada.putalpha(Image.composite(camada.getchannel("A"), Image.new("L", (D, D), 0), mask_in))
    im.alpha_composite(camada)
    im = im.resize((diam, diam), Image.LANCZOS)
    # sombra suave
    pad = 30
    out = Image.new("RGBA", (diam + 2 * pad, diam + 2 * pad), (0, 0, 0, 0))
    sa = Image.new("L", out.size, 0)
    sa.paste(im.getchannel("A"), (pad, pad + 10))
    sa = sa.filter(ImageFilter.GaussianBlur(12)).point(lambda a: int(a * 0.45))
    sombra = Image.new("RGBA", out.size, (20, 0, 40, 255))
    sombra.putalpha(sa)
    out.alpha_composite(sombra)
    out.alpha_composite(im, (pad, pad))
    return out


AVATAR = avatar(330)
Y_CF_PERGUNTA = 400
Y_CF_AVATAR = 790
Y_CF_LUPA = 1095
Y_CF_NOME = 1210


def cortina(v, cen, t0, dur=T_CORTINA, z=56):
    """O fundo sobe e cobre o que estava na tela (transição para o cartão final)."""
    v.som("vush", t0 - 0.03, 0.42)
    faixa = Image.new("RGBA", (W, 36), (0, 0, 0, 0))
    a = np.linspace(0, 70, 36).astype(np.uint8)[:, None].repeat(W, 1)
    faixa.putalpha(Image.fromarray(a, "L"))

    def f(canvas, tl, t):
        p = r.ease_out_cubic(min(1.0, tl / dur))
        y = int(round(H * (1 - p)))
        if y >= H:
            return
        bg = cen.quadro(t)
        if y > 0:
            canvas.paste(faixa, (0, y - 36), faixa)
            canvas.paste(bg.crop((0, y, W, H)), (0, y))
        else:
            canvas.paste(bg, (0, 0))
    v.adicionar(f, t0, None, z)


def tamanho_nome(contorno=11, largura=800):
    """Maior fonte em que o nome cabe numa linha só, dentro dos 800 px (a biblioteca encolhe em saltos de 7%)."""
    for s in range(110, 40, -1):
        im = r.texto_img(f"*{NOME}*", tamanho=s, fonte_nome="titulo", contorno=contorno, largura_max=largura, max_linhas=1)
        if im.info["tamanho_usado"] == s:
            return s
    return 40


def cartao_final(v, t0, pergunta, com_pergunta=True):
    """CF: pergunta + símbolo do perfil + 'Procura na lupa 🔎' + nome exato em amarelo, numa linha."""
    if com_pergunta:
        v.texto(pergunta, t0 + 0.04, None, centro=(CX, Y_CF_PERGUNTA), tamanho=82, max_linhas=2,
                cor_contorno=CONTORNO, sombra=SOMBRA, entrada="pop", saida=None, z=60, nome="CF pergunta")
    v.imagem(AVATAR, t0 + 0.10, None, centro=(CX, Y_CF_AVATAR), entrada="pop", som=False, ocioso="flutuar",
             z=58, nome="CF símbolo")
    v.texto("Procura na lupa 🔎", t0 + 0.18, None, centro=(CX, Y_CF_LUPA), tamanho=80, fonte="black",
            cor_contorno=CONTORNO, sombra=SOMBRA, entrada="deslizar_baixo", saida=None, som=False, z=60, nome="CF lupa")
    v.texto(f"*{NOME}*", t0 + 0.26, None, centro=(CX, Y_CF_NOME), tamanho=tamanho_nome(), fonte="titulo", max_linhas=1,
            contorno=11, cor_contorno=CONTORNO, sombra=SOMBRA, entrada="deslizar_baixo", saida=None, som=False,
            ocioso="pulsar", z=60, nome="CF nome")
    assinatura(v, t0 + 0.12)


def roleta(v, inicio, duracao, resultado, fim):
    """Roleta das 28 cartas (biblioteca), começo um pouco mais lento que o padrão (menos pisca-pisca)."""
    return v.roleta(CARTAS, resultado - 1, inicio=inicio, duracao=duracao, centro=(CX, Y_CARTA), escala=ESC,
                    fim=fim, intervalo_ini=0.09, intervalo_fim=0.5, curva=1.8, volume_tique=0.45, nome="roleta")


def video_base(dur, semente, bpm, progressao, neve=False, vol_trilha=0.26):
    v = r.Video(dur, semente=semente)
    cen = Cenario(semente, neve=neve)
    v.fundo(cen)
    v.trilha(volume=vol_trilha, bpm=bpm, progressao=progressao, ducking=0.5)
    return v, cen


# ============================================================================
# C08-V1 · "O filtro que te expõe" · 10 s
# ============================================================================
def peca_v1():
    v, cen = video_base(10.0, 8101, 104, [(48, ""), (43, ""), (45, "m"), (41, "")])
    assinatura(v, 0.05)
    # 0–1,8: gancho + carta 2 balançando + 🤔
    gancho(v, "O filtro que te *expõe* no grupo", fim=6.62)
    v.imagem(carta(2), 0.0, 1.95, centro=(CX, Y_CARTA), escala=ESC, entrada=None, saida="zoom", dur_saida=0.22,
             ocioso="balancar", z=12, nome="carta 2")
    cabeca(v, "🤔", 0.0, 6.6, saida=None)
    # 1,8–2,6: título + dedo
    v.som("vush", 1.72, 0.45)
    v.imagem(TITULO, 1.85, 2.6, centro=(CX, Y_CARTA), escala=ESC, entrada="pop", dur_entrada=0.3,
             ocioso="flutuar", z=12, nome="título")
    v.toque(2.12, centro=POS_TOQUE)
    # 2,6–6,6: roleta para na 7
    t_cf = 8.0
    t_res = roleta(v, 2.6, 4.0, 7, fim=t_cf + T_CORTINA + 0.05)
    cabeca(v, "😌", t_res, t_cf + T_CORTINA + 0.05, entrada="pop", nome="cabeça 2")
    # 6,6–8: frase
    topo(v, "Alguém tem que manter a *ordem* 😌", t_res + 0.1, t_cf + 0.02, saida="fade", nome="frase")
    # 8–10: cartão final
    cortina(v, cen, t_cf)
    cartao_final(v, t_cf, "Qual é o seu *papel* no grupo?")
    return v


# ============================================================================
# C08-V2 · "A família inteira" · 13 s
# ============================================================================
def rotulo_img(texto):
    """Rótulo em texto (MÃE, TIO…): pílula branca, letra roxa. Sem rosto e sem emoji de pessoa."""
    return r.texto_img(texto, tamanho=104, fonte_nome="titulo", cor="#4B1590", contorno=0, sombra=(0, 10, 16, 120),
                       largura_max=800, caixa="#FFFFFF", caixa_pad=(58, 30), caixa_raio=64)


def peca_v2():
    v, cen = video_base(13.0, 8202, 110, [(41, ""), (48, ""), (43, ""), (45, "m")])
    assinatura(v, 0.05)
    gancho(v, "Cada um da família *tem o seu*", fim=6.45)
    parentes = [("MÃE", 1), ("TIO", 21), ("VÓ", 5), ("PRIMO", 11)]
    tempos = [0.0, 2.0, 3.5, 5.0, 6.5]
    for i, (rot, n) in enumerate(parentes):
        ini, fim = tempos[i], tempos[i + 1]
        v.imagem(carta(n), ini if i == 0 else ini - 0.06, fim + 0.16, centro=(CX, Y_CARTA), escala=ESC,
                 entrada=None if i == 0 else "deslizar_dir", saida="deslizar_esq", dur_entrada=0.34, dur_saida=0.3,
                 som=(i > 0), z=12, nome=f"carta {n}")
        v.imagem(rotulo_img(rot), ini if i == 0 else ini + 0.08, fim, centro=(CX, Y_CABECA - 20),
                 entrada=None if i == 0 else "pop", saida="pop", dur_entrada=0.28, dur_saida=0.14,
                 som=(i > 0), z=13, nome=f"rótulo {rot}")
    # 6,5–7,3: E VOCÊ? + título + 🤔 + dedo
    # QA 06/11: roleta de 2,3 s (era 2,8) para o resultado ficar ~1,2 s parado antes da cortina (era ~0,7 s)
    t_cf = 10.75
    ini_rol, dur_rol = 7.3, 2.3
    t_res_prev = ini_rol + dur_rol                      # 9,6 s
    topo(v, "E *VOCÊ*?", 6.5, t_res_prev + 0.05, tamanho=128, nome="E VOCÊ")
    v.imagem(TITULO, 6.44, 7.3, centro=(CX, Y_CARTA), escala=ESC, entrada="deslizar_dir", dur_entrada=0.34,
             som=True, z=12, nome="título")
    cabeca(v, "🤔", 6.62, t_res_prev, entrada="pop")
    v.toque(6.86, centro=POS_TOQUE)
    # 7,3–9,6: roleta para na 4 (resultado parado de 9,6 a 10,75)
    t_res = roleta(v, ini_rol, dur_rol, 4, fim=t_cf + T_CORTINA + 0.05)
    assert abs(t_res - t_res_prev) < 1e-9
    cabeca(v, "🫣", t_res, t_cf + T_CORTINA + 0.05, entrada="pop", nome="cabeça 2")
    # 9,6–13: pergunta do CF já sobe com o resultado, depois o resto do CF
    topo(v, "Manda no grupo da família 👀", t_res + 0.1, None, tamanho=82, saida=None, z=60, nome="CF pergunta")
    cortina(v, cen, t_cf)
    cartao_final(v, t_cf, None, com_pergunta=False)
    return v


# ============================================================================
# C08-V3 · "Natal no grupo" · 11 s
# ============================================================================
class Chuva:
    """Chuva de 💬 e 🎄 caindo do topo (atrás da carta)."""

    def __init__(self, semente, n=24, fim_chuva=1.9):
        self.fim_chuva = fim_chuva
        rng = random.Random(semente)
        self.itens = []
        for i in range(n):
            self.itens.append(dict(e="🎄" if i % 3 == 1 else "💬", x=rng.uniform(40, 1040), y0=rng.uniform(-1300, 1500),
                                   vel=rng.uniform(420, 640), alt=rng.choice([70, 86, 100, 116]),
                                   fase=rng.uniform(0, 6.28), ang=rng.uniform(-18, 18), op=rng.uniform(0.75, 0.95)))

    def __call__(self, canvas, tl, t):
        fade = 1.0 - r.limitar((tl - self.fim_chuva) / 0.35)
        if fade <= 0:
            return
        for c in self.itens:
            y = c["y0"] + c["vel"] * tl
            if y < -80 or y > H + 80:
                continue
            x = c["x"] + 14 * math.sin(2.0 * tl + c["fase"])
            r.colar(canvas, r.emoji_img(c["e"], c["alt"]), (x, y), 1.0, c["ang"] + 8 * math.sin(1.6 * tl + c["fase"]),
                    c["op"] * fade)


def peca_v3():
    v, cen = video_base(11.0, 8303, 100, [(48, ""), (45, "m"), (41, ""), (43, "")], neve=True, vol_trilha=0.24)
    # sininho em colcheias, bem baixo, durante o vídeo todo
    beat = 60.0 / 100
    k = 0
    while k * beat / 2 < 10.4:
        v.som(som_sininho(k % 4), 0.02 + k * beat / 2, 0.11 if k % 2 == 0 else 0.07, 0.2)
        k += 1
    assinatura(v, 0.05)
    v.adicionar(Chuva(83031), 0.0, 2.4, z=3)
    # 0–2: gancho + carta 13
    gancho(v, "Hoje o grupo da família vai *lotar* 🎄", fim=3.45)
    v.imagem(carta(13), 0.0, 2.05, centro=(CX, Y_CARTA), escala=ESC, entrada=None, saida="zoom", dur_saida=0.22,
             ocioso="balancar", z=12, nome="carta 13")
    cabeca(v, "🥳", 0.0, 2.05, saida="pop")
    # 2–3,5: FELIZ NATAL × 200 💬 (o grupo enchendo), plins seguidos
    t_a, t_b = 2.0, 3.5
    feliz = r.texto_img("FELIZ NATAL", tamanho=124, fonte_nome="titulo", cor="#FFFFFF", contorno=12,
                        cor_contorno=CONTORNO, sombra=SOMBRA, largura_max=800, max_linhas=1)
    notas = [1046.5, 1174.66, 1318.51, 1396.91, 1567.98, 1760.0, 1975.53, 2093.0]
    for i, nota in enumerate(notas):
        v.som(r.som_plim(nota=nota, duas=False, dur=0.35), t_a + 0.08 + i * 0.14, 0.32 + 0.03 * i, 0.3 * (-1) ** i)
    v.som(r.som_pop(), t_a + 0.02, 0.6)

    def contador(canvas, tl, t):
        sai = 1.0 - r.limitar((tl - (t_b - t_a - 0.15)) / 0.15)
        p = r.limitar(tl / 0.25)
        s = (0.4 + 0.6 * r.ease_out_back(p, 2.0)) * (1 + 0.05 * math.sin(2 * math.pi * tl / 0.6))
        r.colar(canvas, feliz, (CX, 760), s, 0, r.limitar(p * 3) * sai)
        nn = 1 + int(round(199 * r.ease_out_cubic(r.limitar((tl - 0.08) / 1.1))))
        num = r.texto_img(f"× {nn} 💬", tamanho=150, fonte_nome="titulo", cor=AMARELO, contorno=13,
                          cor_contorno=CONTORNO, sombra=SOMBRA, largura_max=800, max_linhas=1)
        bate = 1 + 0.06 * math.exp(-((tl - 0.08) % 0.14) / 0.05) if tl < 1.2 else 1.0
        r.colar(canvas, num, (CX, 975), bate * min(1.0, 0.5 + p), 0, r.limitar((tl - 0.05) * 6) * sai)
        if v._registrando:   # checagem de zona segura do contador (posição de repouso)
            v._registrar("FELIZ NATAL", r.caixa_nominal(feliz, (CX, 760), 1.0, 0, "centro", feliz.info.get("caixa")), t)
            v._registrar("contador", r.caixa_nominal(num, (CX, 975), 1.0, 0, "centro", num.info.get("caixa")), t)
    v.adicionar(contador, t_a, t_b, z=22)

    # balões 💬 pipocando em volta (o grupo lotando)
    rng = random.Random(83032)
    pontos = [(150, 560), (930, 540), (250, 1180), (830, 1200), (110, 1360), (960, 1350), (420, 1320), (660, 1400),
              (300, 590), (770, 600), (540, 1230), (180, 860), (900, 880)]
    for i, (x, y) in enumerate(pontos):
        ti = t_a + 0.08 + i * 0.085
        alt = rng.choice([84, 100, 116, 132])
        v.imagem(r.emoji_img("💬", alt), ti, t_b, centro=(x + rng.uniform(-20, 20), y + rng.uniform(-20, 20)),
                 rotacao=rng.uniform(-16, 16), entrada="pop", saida="fade", dur_entrada=0.22, dur_saida=0.15,
                 som=False, z=15)
    # 3,5–4,2: E você, quem é hoje? + título + dedo
    # QA 06/11: roleta de 3,2 s (era 3,8) para o resultado ficar ~1,15 s parado antes da cortina (era ~0,55 s)
    t_cf = 8.55
    ini_rol, dur_rol = 4.2, 3.2
    t_res_prev = ini_rol + dur_rol                      # 7,4 s
    topo(v, "E você,\n*quem é hoje*?", t_b, t_res_prev + 0.05, nome="E você")
    v.imagem(TITULO, t_b, 4.2, centro=(CX, Y_CARTA), escala=ESC, entrada="pop", dur_entrada=0.3, z=12, nome="título")
    cabeca(v, "🤔", t_b + 0.05, t_res_prev, entrada="pop")
    v.toque(3.78, centro=POS_TOQUE)
    # 4,2–7,4: roleta para na 9 (resultado parado de 7,4 a 8,55)
    t_res = roleta(v, ini_rol, dur_rol, 9, fim=t_cf + T_CORTINA + 0.05)
    assert abs(t_res - t_res_prev) < 1e-9
    cabeca(v, "😅", t_res, t_cf + T_CORTINA + 0.05, entrada="pop", nome="cabeça 2")
    topo(v, "Cada um no seu celular 📱", t_res + 0.12, None, tamanho=82, saida=None, z=60, nome="CF pergunta")
    cortina(v, cen, t_cf)
    cartao_final(v, t_cf, None, com_pergunta=False)
    return v


# ============================================================================
# Fichas das peças
# ============================================================================
def hashtag_efeito():
    s = unicodedata.normalize("NFKD", NOME).encode("ascii", "ignore").decode().lower()
    return "#" + "".join(ch for ch in s if ch.isalnum())


def fichas():
    he = hashtag_efeito()
    return {
        "C08-V1": dict(func=peca_v1, alvo_mb=2.75, tempos_previa=[0.5, 2.2, 4.4, 7.0, 8.6, 9.8],
                       legenda=f"Qual é o seu papel no grupo da família? Manda no grupo e vê quem concorda 😂 Filtro: {NOME} 🔎",
                       hashtags=f"{he} #grupodafamilia #filtro #filtrotiktok #familia",
                       capa=dict(texto="QUAL É O SEU *PAPEL* NO GRUPO?", carta=7, cabeca="😌", rotulo=None)),
        "C08-V2": dict(func=peca_v2, alvo_mb=3.0, tempos_previa=[0.5, 2.8, 5.8, 7.0, 10.4, 12.6],
                       legenda=f"Mãe, tio, vó, primo… cada um tem seu papel no grupo 😂 E você? Filtro: {NOME} 🔎 procura na lupa",
                       hashtags=f"{he} #grupodafamilia #familiabrasileira #filtrotiktok #humor",
                       capa=dict(texto="CADA UM DA FAMÍLIA *TEM O SEU* 😂", carta=21, cabeca=None, rotulo="TIO")),
        "C08-V3": dict(func=peca_v3, alvo_mb=2.8, tempos_previa=[0.5, 2.9, 3.9, 6.0, 8.3, 10.6],
                       legenda=f"Natal: hoje o grupo da família vai lotar 🎄 Qual é o seu papel nele? Filtro: {NOME} 🔎",
                       hashtags=f"{he} #grupodafamilia #natal #filtrotiktok #familia",
                       capa=dict(texto="NATAL NO GRUPO DA FAMÍLIA 🎄", carta=9, cabeca="😅", rotulo=None, neve=True)),
    }


# QA 06/11: a legenda da M1 era montada na importação (f-string), e o --nome não chegava ao kit.
# Agora o nome entra na hora de gerar o kit, como nas outras legendas.
M1 = dict(legenda="Funciona assim: toca na tela e o filtro mostra seu papel no grupo da família. Filtro: {nome} 🔎",
          hashtags="{he} #grupodafamilia #filtro #filtrotiktok #feriado")


# ============================================================================
# Capas (1080x1920, texto grande no miolo 3:4 = y de 240 a 1680)
# ============================================================================
def salvar_jpg(img, caminho, max_kb=200):
    return r.salvar_jpg(img, caminho, max_kb=max_kb)


def capa_img(texto, carta_n=None, cabeca_e=None, rotulo=None, neve=False, semente=9000, titulo=False, dedo=False):
    v = r.Video(1.0, semente=semente)
    cen = Cenario(semente, neve=neve)
    v.fundo(cen)
    v.texto(texto, 0, None, centro=(CX, 470), tamanho=118, max_linhas=3, largura_max=820, contorno=13,
            cor_contorno=CONTORNO, sombra=(0, 10, 16, 160), entrada=None, saida=None, som=False)
    y_c = 1080
    if titulo:
        v.imagem(TITULO, 0, None, centro=(CX, y_c), escala=1.42, entrada=None, som=False, z=12)
    if carta_n:
        v.imagem(carta(carta_n), 0, None, centro=(CX, y_c), escala=1.42, entrada=None, som=False, z=12)
    if cabeca_e:
        v.imagem(r.emoji_img(cabeca_e, 250), 0, None, centro=(CX, y_c + 445), entrada=None, som=False, z=11)
    if rotulo:
        v.imagem(rotulo_img(rotulo), 0, None, centro=(CX, y_c + 430), entrada=None, som=False, z=13)
    if dedo:
        v.imagem(r.emoji_img("👆", 150), 0, None, centro=(790, y_c + 470), entrada=None, som=False, z=14)
    return v.quadro(0.0)


# ============================================================================
# Kit da C08-M1 (gravação do Montador no preview do Effect House)
# ============================================================================
def salvar_wav_mono(caminho, x):
    """WAV 16 bits, mono, 44,1 kHz (metade do tamanho do estéreo; o Clipchamp abre normal).
    Volume perto do dos mp4 (~ -14 LUFS), com o limitador suave da biblioteca."""
    m = np.asarray(x, dtype=np.float64).mean(axis=1)
    m = r.masterizar(np.stack([m, m], axis=1), rms_alvo_db=-12.5)[:, 0].astype(np.float64)
    with wave.open(caminho, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(r.SR)
        w.writeframes((m * 32767).astype("<i2").tobytes())


def kit_m1(pasta):
    os.makedirs(pasta, exist_ok=True)
    he = hashtag_efeito()
    # gancho.png: transparente, por cima de 0 a 3 s
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    t1 = r.texto_img("Funciona assim 👇\nQual é o seu *papel*?", tamanho=88, fonte_nome="titulo", contorno=12,
                     cor_contorno=CONTORNO, sombra=(0, 8, 16, 170), largura_max=800, max_linhas=2)
    r.colar(g, t1, (CX, 345))
    g.save(os.path.join(pasta, "gancho.png"), optimize=True)
    # final.png: cartão final parado (2,5 s no fim do vídeo)
    v = r.Video(3.0, semente=8404)
    cen = Cenario(8404)
    v.fundo(cen)
    cartao_final(v, 0.0, "Qual é o *seu*?")
    fim = v.quadro(1.5)
    fim.save(os.path.join(pasta, "final.png"), optimize=True)
    # assinatura.wav: 12 s de trilha nossa (104 bpm) com a assinatura no começo e no cartão final
    a = r.Video(12.0, semente=8404)
    a.trilha(volume=0.3, bpm=104, progressao=[(48, ""), (43, ""), (45, "m"), (41, "")], ducking=0.5)
    assinatura(a, 0.05)
    a.som("toque", 3.0, 0.5)
    assinatura(a, 9.55)
    salvar_wav_mono(os.path.join(pasta, "assinatura.wav"), a.audio())
    # capa
    salvar_jpg(capa_img("FUNCIONA ASSIM 👇", None, "🤔", None, semente=9404, titulo=True, dedo=True),
               os.path.join(pasta, "capa.jpg"))
    with open(os.path.join(pasta, "legenda.txt"), "w", encoding="utf-8") as f:
        f.write(M1["legenda"].format(nome=NOME) + " " + M1["hashtags"].format(he=he) + "\n")
    return sorted(os.listdir(pasta))


# ============================================================================
# Prévia: 6 quadros de cada mp4, com as faixas da interface
# ============================================================================
def extrair_quadro(mp4, t):
    res = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", mp4, "-frames:v", "1",
                          "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True, check=True)
    return Image.open(io.BytesIO(res.stdout)).convert("RGB")


def previa(pecas, saida, largura=210):
    alt = int(largura * H / W)
    m, topo_px, rot, cab = 10, 54, 28, 34
    cols = 6
    Wp = cols * largura + (cols + 1) * m
    Hp = topo_px + len(pecas) * (cab + alt + rot + m) + m
    pr = Image.new("RGB", (Wp, Hp), (24, 25, 30))
    d = ImageDraw.Draw(pr)
    d.text((m, 14), f"C08 · {NOME} · prévia dos vídeos (vermelho = interface do TikTok; amarelo = zona segura)",
           font=r.fonte("bold", 21), fill=(235, 235, 240))
    y = topo_px
    for cod, mp4, tempos in pecas:
        info = r.info_video(mp4)
        d.text((m, y + 4), f"{cod}  ·  {info['duracao_s']:.2f} s  ·  {info['tamanho_mb']} MB  ·  {info['codecs']}",
               font=r.fonte("semi", 20), fill=(255, 212, 59))
        y += cab
        for i, t in enumerate(tempos):
            q = extrair_quadro(mp4, t).resize((largura, alt), Image.LANCZOS)
            q = r.desenhar_zonas(q, cor=(255, 40, 40, 55), contorno=(255, 220, 0, 170))
            x = m + i * (largura + m)
            pr.paste(q, (x, y))
            d.text((x + 3, y + alt + 3), f"t = {t:.1f} s", font=r.fonte("semi", 18), fill=(200, 205, 215))
        y += alt + rot + m
    pr = pr.quantize(colors=256, method=Image.Quantize.FASTOCTREE)   # mantém as cores (o MEDIANCUT trocava o verde-água por azul)
    pr.save(saida, optimize=True)
    return saida


# ============================================================================
# Render determinístico (contorno de um defeito da biblioteca)
# ============================================================================
def renderizar_det(v, saida, alvo_mb):
    """Gera o mp4 sem usar Video.renderizar().

    Defeito contornado: o renderizar() da biblioteca manda os quadros por pipe para o x264 com vários
    threads, e o arquivo sai um pouco diferente a cada rodada (os quadros e o som são idênticos; conferido).
    Aqui: 1) quadros -> intermediário SEM PERDA (o que se decodifica é sempre igual);
          2) 2 passadas lendo do arquivo até o tamanho-alvo (x264 lendo de arquivo é determinístico).
    Mesmo formato da biblioteca: H.264 High 4.1, yuv420p, BT.709, 30 fps, AAC 128k estéreo, +faststart.
    Bônus: uma compressão só (a biblioteca fazia CRF 21 e depois mais 2 passadas)."""
    t0 = time.time()
    tmp = tempfile.mkdtemp(prefix="c08_")
    alvo = alvo_mb * 1024 * 1024
    kbps = int(alvo * 8 / v.duracao / 1000 * 0.96) - 136
    try:
        wav = os.path.join(tmp, "audio.wav")
        r.salvar_wav(wav, v.audio())
        sem_perda = os.path.join(tmp, "sem_perda.mkv")
        n = int(round(v.duracao * v.fps))
        cor = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
        cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
               "-r", str(v.fps), "-i", "-", "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
               "-c:v", "libx264", "-preset", "ultrafast", "-qp", "0"] + cor + [sem_perda]
        registra = hasattr(v, "_registrando") and hasattr(v, "_zonas")   # checagem de zona segura da biblioteca
        if registra:
            v._zonas = {}
            v._registrando = True
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        try:
            for i in range(n):
                p.stdin.write(v.quadro(i / v.fps).tobytes())
                if i % (v.fps * 3) == 0:
                    print(f"  {os.path.basename(saida)}: quadro {i}/{n} ({time.time() - t0:.0f} s)", file=sys.stderr)
        finally:
            if registra:
                v._registrando = False
            p.stdin.close()
            p.wait()
        if p.returncode != 0:
            raise RuntimeError("ffmpeg (intermediário sem perda) falhou")
        for _ in range(5):
            base = ["ffmpeg", "-y", "-v", "error", "-i", sem_perda, "-i", wav, "-map", "0:v", "-map", "1:a",
                    "-c:v", "libx264", "-preset", "medium", "-b:v", f"{kbps}k", "-profile:v", "high", "-level:v", "4.1",
                    "-pix_fmt", "yuv420p", "-g", str(v.fps * 2)] + cor + ["-passlogfile", os.path.join(tmp, "p")]
            subprocess.run(base + ["-pass", "1", "-an", "-f", "mp4", os.devnull], check=True)
            subprocess.run(base + ["-pass", "2", "-c:a", "aac", "-b:a", "128k", "-ar", str(r.SR), "-ac", "2",
                                   "-t", f"{v.duracao:.3f}", "-movflags", "+faststart", "-fflags", "+bitexact",
                                   "-flags:v", "+bitexact", "-flags:a", "+bitexact", "-map_metadata", "-1", saida],
                           check=True)
            if os.path.getsize(saida) <= alvo:
                break
            kbps = int(kbps * 0.94)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    info = r.info_video(saida)
    info["tempo_render_s"] = round(time.time() - t0, 1)
    info["kbps_video"] = kbps
    info["avisos_zona"] = v.relatorio_zonas()
    print(f"OK {saida}: {info['duracao_s']} s, {info['tamanho_mb']} MB, {info['codecs']}, "
          f"render {info['tempo_render_s']} s", file=sys.stderr)
    for aviso in info["avisos_zona"]:
        print("  AVISO zona segura:", aviso, file=sys.stderr)
    return info


# ============================================================================
# Principal
# ============================================================================
def main(argv=None):
    global NOME
    ap = argparse.ArgumentParser(description="Vídeos do C08 'Eu no grupo da família'.")
    ap.add_argument("--so", help="só esta peça (C08-V1, C08-V2 ou C08-V3)")
    ap.add_argument("--sem-mp4", action="store_true", help="não renderiza mp4 (só capas, legendas, kit e prévia)")
    ap.add_argument("--nome", help="nome publicado do filtro, se sair diferente do textos.json")
    ap.add_argument("--saida", default=AQUI, help="pasta de saída (padrão: esta pasta)")
    a = ap.parse_args(argv)
    if a.nome:
        NOME = a.nome
    out = a.saida
    os.makedirs(out, exist_ok=True)
    fs = fichas()
    cods = [a.so] if a.so else list(fs)
    resumo = []
    for cod in cods:
        f = fs[cod]
        mp4 = os.path.join(out, f"{cod}.mp4")
        if not a.sem_mp4:
            v = f["func"]()
            info = renderizar_det(v, mp4, f["alvo_mb"])
            resumo.append(dict(peca=cod, duracao_s=info["duracao_s"], tamanho_bytes=info["tamanho_bytes"],
                               codecs=info["codecs"], kbps_video=info["kbps_video"], avisos_zona=info["avisos_zona"]))
        c = f["capa"]
        salvar_jpg(capa_img(c["texto"], c["carta"], c["cabeca"], c["rotulo"], c.get("neve", False)),
                   os.path.join(out, f"{cod}-capa.jpg"))
        with open(os.path.join(out, f"{cod}-legenda.txt"), "w", encoding="utf-8") as fl:
            fl.write(f["legenda"] + " " + f["hashtags"] + "\n")
    if not a.so:
        kit_m1(os.path.join(out, "kit-C08-M1"))
    pecas = [(cod, os.path.join(out, f"{cod}.mp4"), fs[cod]["tempos_previa"]) for cod in fs
             if os.path.exists(os.path.join(out, f"{cod}.mp4"))]
    if pecas and not a.so:
        previa(pecas, os.path.join(out, "previa-videos.png"))
    print(json.dumps(resumo, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
