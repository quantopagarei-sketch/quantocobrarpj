#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador do Reel diário do Black Achadinhos (regras e roteiro: ver reels.md).

  python3 reels/fazer_reel.py --roteiro PASTA/roteiro.json --saida PASTA --quadros   (só a folha de conferência)
  python3 reels/fazer_reel.py --roteiro PASTA/roteiro.json --saida PASTA             (vídeo completo)

Sai em PASTA: reel.mp4 (1080x1920, 30 fps, H.264 + AAC, abaixo de 3,6 MB), legenda.txt, comentario.txt,
conferencia.jpg (um quadro de cada cena, para conferir com os olhos antes de postar).
Tudo é desenhado por código: nenhuma imagem, voz ou música de terceiros além da foto do anúncio.
"""
import argparse
import json
import math
import os
import subprocess
import sys
import wave
from decimal import Decimal, ROUND_HALF_UP
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
PRETO, AMARELO, BRANCO = (12, 12, 14), (255, 212, 0), (255, 255, 255)
CINZA, CINZA_ESC = (170, 170, 175), (58, 58, 64)
AQUI = Path(__file__).resolve().parent
BATIDA = 0.5                      # 120 BPM: 1 batida = 15 quadros
SEG_ABRE, SEG_FECHA = 2.0, 4.0    # abertura (4 batidas) e chamada final (8 batidas)
LIMITE_BYTES = 3_600_000          # o envio de arquivo pelo Chrome aceita no máximo 3,8 MB
CANAL = 'Blackachados'


# ------------------------------------------------------------------ texto e formas
@lru_cache(maxsize=None)
def fonte(tam, bold=True):
    nome = 'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'
    for p in (AQUI / 'fonts' / nome, Path('/usr/share/fonts/truetype/dejavu') / nome):
        if p.exists():
            return ImageFont.truetype(str(p), tam)
    raise SystemExit('Fonte DejaVu não encontrada (reels/fonts).')


def linha(partes, tam, bold=True):
    """Uma linha de texto com trechos de cores diferentes. partes = [(texto, cor), ...]"""
    f = fonte(tam, bold)
    asc, desc = f.getmetrics()
    larg = sum(f.getlength(t) for t, _ in partes)
    im = Image.new('RGBA', (int(math.ceil(larg)) + 8, asc + desc + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = 4.0
    for t, cor in partes:
        d.text((x, 4), t, font=f, fill=cor + (255,))
        x += f.getlength(t)
    return im


def txt(texto, tam, cor=BRANCO, bold=True):
    return linha([(texto, cor)], tam, bold)


def quebra(texto, tam, max_w, max_linhas=2, tam_min=42):
    """Quebra em até max_linhas; diminui a fonte se preciso; no limite, corta com reticências."""
    while True:
        f = fonte(tam, True)
        linhas, atual = [], ''
        for p in texto.split():
            t = (atual + ' ' + p).strip()
            if f.getlength(t) <= max_w or not atual:
                atual = t
            else:
                linhas.append(atual)
                atual = p
        if atual:
            linhas.append(atual)
        if len(linhas) <= max_linhas and all(f.getlength(l) <= max_w for l in linhas):
            return linhas, tam
        if tam <= tam_min:
            linhas = linhas[:max_linhas]
            while f.getlength(linhas[-1] + '…') > max_w and len(linhas[-1]) > 1:
                linhas[-1] = linhas[-1][:-1]
            linhas[-1] = linhas[-1].rstrip() + '…'
            return linhas, tam
        tam -= 2


def brl(v):
    d = Decimal(str(v)).quantize(Decimal('0.01'), ROUND_HALF_UP)
    inteiro = int(d)
    cent = int((d - inteiro) * 100)
    return 'R$ ' + f'{inteiro:,}'.replace(',', '.') + f',{cent:02d}'


def pct(preco, de):
    """Desconto arredondado para BAIXO (como a página do Mercado Livre mostra)."""
    return int(math.floor((1 - float(preco) / float(de)) * 100 + 1e-9))


def caixa(w, h, raio, cor):
    s = 3
    im = Image.new('RGBA', (w * s, h * s), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w * s - 1, h * s - 1), raio * s, fill=cor + (255,))
    return im.resize((w, h), Image.LANCZOS)


def faixa_texto(texto, tam, alt, pad=60, cor=AMARELO, cor_txt=PRETO, max_w=840, sufixo=None):
    """Faixa arredondada com texto (o preço). Diminui a fonte até caber em max_w."""
    while True:
        t = txt(texto, tam, cor_txt)
        suf = txt(sufixo, int(tam * 0.38), cor_txt) if sufixo else None
        larg = t.width + 2 * pad + (suf.width + 10 if suf else 0)
        if larg <= max_w or tam <= 60:
            break
        tam -= 4
    im = caixa(larg, alt, alt // 3, cor)
    im.alpha_composite(t, (pad, (alt - t.height) // 2))
    if suf:
        im.alpha_composite(suf, (pad + t.width + 6, (alt - t.height) // 2 + t.height - suf.height - int(tam * 0.13)))
    return im


def etiqueta(larg):
    """O símbolo do logo (etiqueta amarela com %), desenhado como no logo.jpg."""
    s = 4
    esc = larg * s / 549.0
    alt = int(round(510 * esc / s))
    im = Image.new('RGBA', (larg * s, alt * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = [(262, 300), (600, 215), (811, 380), (811, 560), (600, 725), (262, 640)]
    d.polygon([((x - 262) * esc, (y - 215) * esc) for x, y in pts], fill=AMARELO + (255,))
    cx, cy, r = (335 - 262) * esc, (470 - 215) * esc, 35 * esc
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=PRETO + (255,))
    d.text(((580 - 262) * esc, (470 - 215) * esc), '%', font=fonte(int(250 * esc)), fill=PRETO + (255,), anchor='mm')
    return im.resize((larg, alt), Image.LANCZOS)


# ------------------------------------------------------------------ foto do produto
def _maior_trecho(v):
    melhor, ini = (0, 0), None
    for i, ok in enumerate(list(v) + [False]):
        if ok and ini is None:
            ini = i
        elif not ok and ini is not None:
            if i - ini > melhor[1] - melhor[0]:
                melhor = (ini, i)
            ini = None
    return melhor


def carrega_foto(caminho):
    """Abre a foto. Se for print da aba de imagem do Chrome (fundo quase preto em volta), recorta só a foto."""
    im = Image.open(caminho).convert('RGB')
    a = np.asarray(im).astype(np.int16)
    canto = a[:6, :6].reshape(-1, 3)
    if np.abs(canto - 14).max() <= 5:                       # fundo do visualizador do Chrome: rgb(14,14,14)
        dif = (np.abs(a - 14) > 8).any(axis=2)
        c0, c1 = _maior_trecho(dif.any(axis=0))               # ignora o cursor do mouse no canto (trecho pequeno)
        l0, l1 = _maior_trecho(dif[:, c0:c1].any(axis=1))
        if c1 - c0 > 80 and l1 - l0 > 80:
            im = im.crop((c0 + 1, l0 + 1, c1 - 1, l1 - 1))
    return im


def monta_tela(foto, cw, ch):
    """Coloca a foto no cartão branco. Fundo branco: cabe inteira. Foto de ambiente: preenche o cartão."""
    a = np.asarray(foto).astype(np.float32)
    borda = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    tela = Image.new('RGB', (cw, ch), BRANCO)
    cobre = max(cw / foto.width, ch / foto.height)
    if borda.mean() > 232 or cobre > 1.5:                    # produto em fundo branco (ou foto pequena demais)
        m = 46
        esc = min((cw - 2 * m) / foto.width, (ch - 2 * m) / foto.height, 1.5)
    else:
        esc = cobre
    f = foto.resize((max(1, int(round(foto.width * esc))), max(1, int(round(foto.height * esc)))), Image.LANCZOS)
    tela.paste(f, ((cw - f.width) // 2, (ch - f.height) // 2))
    return tela


def zoom(tela, s):
    cw, ch = tela.size
    return tela.transform((cw, ch), Image.AFFINE, (1 / s, 0, cw / 2 * (1 - 1 / s), 0, 1 / s, ch / 2 * (1 - 1 / s)),
                          resample=Image.BICUBIC, fillcolor=BRANCO)


# ------------------------------------------------------------------ animação
def clamp(x):
    return 0.0 if x < 0 else 1.0 if x > 1 else x


def p(t, t0, d):
    return clamp((t - t0) / d)


def suave(x):
    return 1 - (1 - x) ** 3


def pulo(x):
    c1 = 1.70158
    return 1 + (c1 + 1) * (x - 1) ** 3 + c1 * (x - 1) ** 2


def cola(base, camada, cx, cy, escala=1.0, alpha=1.0):
    if alpha <= 0.004 or escala <= 0.01:
        return
    im = camada
    if abs(escala - 1.0) > 0.002:
        im = im.resize((max(1, int(im.width * escala)), max(1, int(im.height * escala))), Image.BICUBIC)
    if alpha < 0.996:
        im = im.copy()
        im.putalpha(im.getchannel('A').point(lambda v: int(v * alpha)))
    base.paste(im, (int(round(cx - im.width / 2)), int(round(cy - im.height / 2))), im)


def com_brilho(faixa, q):
    w, h = faixa.size
    ov = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    x = -140 + q * (w + 280)
    ImageDraw.Draw(ov).polygon([(x, 0), (x + 80, 0), (x + 20, h), (x - 60, h)], fill=(255, 255, 255, 120))
    ov.putalpha(ImageChops.multiply(ov.getchannel('A'), faixa.getchannel('A')))
    out = faixa.copy()
    out.alpha_composite(ov)
    return out


def barra(d, n, atual, frac):
    x0, x1, y, gap = 70, 1010, 284, 12
    seg = (x1 - x0 - gap * (n - 1)) / n
    for i in range(n):
        a = x0 + i * (seg + gap)
        d.rounded_rectangle((a, y, a + seg, y + 8), 4, fill=CINZA_ESC)
        f = 1.0 if i < atual else clamp(frac) if i == atual else 0.0
        if f > 0.01:
            d.rounded_rectangle((a, y, a + max(8, seg * f), y + 8), 4, fill=AMARELO)


# ------------------------------------------------------------------ cenas
class Reel:
    def __init__(self, roteiro, base):
        self.r = roteiro
        self.ofertas = roteiro['ofertas']
        self.n = len(self.ofertas)
        self.anuncio = roteiro.get('modo') == 'anuncio'   # vídeo de 1 produto para anúncio pago (o clique vai direto ao produto)
        self.seg_prod = float(roteiro.get('segundos_por_produto', 6.0 if self.anuncio else 4.0))
        self.fundo = Image.new('RGB', (W, H), PRETO)
        self.conferido = roteiro['conferido']
        descontos = [pct(o['preco'], o['preco_de']) for o in self.ofertas if o.get('preco_de')]
        self.max_desc = max(descontos) if descontos else 0
        # cabeçalho fixo (marca + aviso de publicidade, visível do primeiro ao último quadro)
        cab = Image.new('RGBA', (W, 300), (0, 0, 0, 0))
        tag = etiqueta(84)
        cab.alpha_composite(tag, (70, 168))
        cab.alpha_composite(linha([('BLACK ', BRANCO), ('ACHADINHOS', AMARELO)], 38), (170, 162))
        cab.alpha_composite(txt('Publicidade · links de afiliado', 29, CINZA, bold=False), (170, 213))
        self.cab = cab
        self.aviso_centro = txt('Publicidade · links de afiliado', 30, CINZA, bold=False)
        self._abre()
        self.prod = [self._produto(o, base) for o in self.ofertas]
        self._fecha()

    # ---- abertura
    def _abre(self):
        n = self.n
        self.a_black = txt('BLACK', 104)
        self.a_tag = etiqueta(330)
        self.a_ach = txt('ACHADINHOS', 96, AMARELO)
        self.a_sub = txt('OFERTAS DO DIA', 40)
        self.a_tit = txt('ACHADO DE HOJE' if n == 1 else f'{n} ACHADOS DE HOJE', 78)
        if self.max_desc >= 15:
            self.a_faixa = faixa_texto(f'ATÉ {self.max_desc}% OFF', 92, 150, pad=56)
        else:
            self.a_faixa = faixa_texto('PREÇOS CONFERIDOS', 64, 130, pad=50)
        self.a_rod = txt(f'no Mercado Livre · conferidos em {self.conferido.split(" às ")[0]}', 37, CINZA, bold=False)

    def quadro_abre(self, t):
        """O 1º quadro já sai completo: é ele que vira a capa do Reel e segura quem está rolando a tela."""
        im = self.fundo.copy()
        cola(im, self.aviso_centro, W / 2, 205)
        for cam, y in ((self.a_black, 470), (self.a_tag, 690), (self.a_ach, 912), (self.a_sub, 992)):
            cola(im, cam, W / 2, y)
        cola(im, self.a_tit, W / 2, 1150)
        fx = self.a_faixa
        q = p(t, 0.15, 0.6)
        if 0 < q < 1:
            fx = com_brilho(fx, q)
        cola(im, fx, W / 2, 1300, escala=1.0 + 0.10 * math.sin(math.pi * p(t, 0.88, 0.34)))   # pulso na 3ª batida
        cola(im, self.a_rod, W / 2, 1432)
        return im

    # ---- produto
    def _produto(self, o, base):
        cw, ch = 900, 700
        L = {'tela': monta_tela(carrega_foto(base / o['foto']), cw, ch)}
        L['mask'] = caixa(cw, ch, 46, BRANCO).getchannel('A')
        linhas, tam = quebra(o['nome'], 58, 900)
        L['nome'] = [txt(l, tam) for l in linhas]
        L['passo'] = int(tam * 1.24)
        if o.get('preco_de'):
            d = pct(o['preco'], o['preco_de'])
            L['de'] = linha([('de ', CINZA), (brl(o['preco_de']), CINZA)], 46, bold=False)
            L['de_risco'] = fonte(46, False).getlength('de ')
            selo = caixa(204, 204, 102, AMARELO)
            t = txt(f'-{d}%', 68, PRETO)
            selo.alpha_composite(t, ((204 - t.width) // 2, (204 - t.height) // 2 - 2))
            L['selo'] = selo.rotate(12, resample=Image.BICUBIC, expand=True)
        else:
            L['de'] = L['selo'] = None
        L['faixa'] = faixa_texto(brl(o['preco']), 112, 144, sufixo='no Pix' if o.get('pix') else None)
        L['info'] = txt(o['info'], 36, CINZA, bold=False) if o.get('info') else None
        return L

    def quadro_produto(self, t, i):
        L, dur = self.prod[i], self.seg_prod
        im = self.fundo.copy()
        im.paste(self.cab, (0, 0), self.cab)
        d = ImageDraw.Draw(im)
        barra(d, self.n, i, t / dur)
        # cartão com a foto entra da direita e segue com um zoom bem lento
        e = suave(p(t, 0.0, 0.36))
        x = int(round(90 + (1 - e) * (W - 50)))
        im.paste(zoom(L['tela'], 1.0 + 0.05 * t / dur), (x, 330), L['mask'])
        # nome
        n = len(L['nome'])
        y0 = 1122 - (n - 1) * L['passo'] / 2
        for k, cam in enumerate(L['nome']):
            a = suave(p(t, 0.20 + 0.08 * k, 0.3))
            cola(im, cam, W / 2, y0 + k * L['passo'] + (1 - a) * 26, alpha=a)
        # preço "de", com o risco
        if L['de'] is not None:
            a = suave(p(t, 0.48, 0.25))
            cola(im, L['de'], W / 2, 1240, alpha=a)
            q = p(t, 0.70, 0.2)
            if q > 0:
                xa = W / 2 - L['de'].width / 2 + 4 + L['de_risco'] - 4
                xb = W / 2 + L['de'].width / 2 - 2
                d.line((xa, 1243, xa + (xb - xa) * q, 1243), fill=CINZA, width=4)
        # preço "por" (o estalo cai na 3ª batida da cena: 1,0 s)
        a = p(t, 0.86, 0.3)
        if a > 0:
            fx = L['faixa']
            q = p(t, 2.0, 0.55)
            if 0 < q < 1:
                fx = com_brilho(fx, q)
            cola(im, fx, W / 2, 1362, escala=0.55 + 0.45 * pulo(a), alpha=min(1, a * 3))
        # selo de desconto
        if L['selo'] is not None:
            a = p(t, 1.36, 0.3)
            if a > 0:
                cola(im, L['selo'], 905, 420, escala=0.4 + 0.6 * pulo(a), alpha=min(1, a * 3))
        # nota e vendidos
        if L['info'] is not None:
            a = suave(p(t, 1.15, 0.3))
            cola(im, L['info'], W / 2, 1480 + (1 - a) * 14, alpha=a)
        return im

    # ---- chamada para o canal
    def _fecha(self):
        self.f_t1 = txt('Os links estão', 80)
        self.f_t2 = linha([('no nosso ', BRANCO), ('Telegram', AMARELO)], 80)
        pil = caixa(860, 140, 70, BRANCO)
        d = ImageDraw.Draw(pil)
        d.ellipse((52, 40, 104, 92), outline=(120, 120, 126), width=9)
        d.line((97, 86, 122, 111), fill=(120, 120, 126), width=10)
        self.f_pil = pil
        f = fonte(66)
        self.f_digita = [txt(CANAL[:k], 66, PRETO) if k else None for k in range(len(CANAL) + 1)]
        self.f_larg = [f.getlength(CANAL[:k]) for k in range(len(CANAL) + 1)]
        self.f_dica = txt('Procure assim no Telegram', 38, CINZA, bold=False)
        self.f_gratis = faixa_texto('Canal grátis · ofertas todo dia', 44, 100, pad=44, max_w=900)
        self.f_saiba = txt('Ou toque em “Saiba mais” na nossa página', 38, BRANCO, bold=False)
        self.f_rod1 = txt('Canal independente (não oficial) · links de afiliado', 27, CINZA, bold=False)
        self.f_rod2 = txt(f'Preços conferidos em {self.conferido} · podem mudar', 27, CINZA, bold=False)

    def quadro_fecha(self, t):
        if self.anuncio:
            return self.quadro_fecha_anuncio(t)
        im = self.fundo.copy()
        im.paste(self.cab, (0, 0), self.cab)
        d = ImageDraw.Draw(im)
        barra(d, self.n, self.n, 1)
        a = suave(p(t, 0.0, 0.32))
        cola(im, self.f_t1, W / 2, 500 + (1 - a) * 30, alpha=a)
        a = suave(p(t, 0.10, 0.32))
        cola(im, self.f_t2, W / 2, 604 + (1 - a) * 30, alpha=a)
        a = p(t, 0.40, 0.32)
        if a > 0:
            cola(im, self.f_pil, W / 2, 800, escala=0.6 + 0.4 * pulo(a), alpha=min(1, a * 3))
        if t >= 0.9:
            k = min(len(CANAL), int((t - 1.0) / 0.075) + 1) if t >= 1.0 else 0
            xt = 250
            if k:
                cam = self.f_digita[k]
                im.paste(cam, (xt - 4, 800 - cam.height // 2), cam)
            if int(t * 2) % 2 == 0 or t < 1.0 + 0.075 * len(CANAL):
                xc = xt + self.f_larg[k] + 4
                d.rectangle((xc, 768, xc + 5, 832), fill=(40, 40, 44))
        a = suave(p(t, 2.0, 0.3))
        cola(im, self.f_dica, W / 2, 918, alpha=a)
        a = p(t, 2.36, 0.3)
        if a > 0:
            cola(im, self.f_gratis, W / 2, 1050, escala=0.6 + 0.4 * pulo(a), alpha=min(1, a * 3))
        a = suave(p(t, 2.85, 0.3))
        cola(im, self.f_saiba, W / 2, 1176 + (1 - a) * 14, alpha=a)
        a = suave(p(t, 0.2, 0.4))
        cola(im, self.f_rod1, W / 2, 1300, alpha=a)
        cola(im, self.f_rod2, W / 2, 1344, alpha=a)
        return im

    def quadro_fecha_anuncio(self, t):
        if not hasattr(self, 'g_t1'):
            self.g_t1 = txt('Gostou?', 96)
            self.g_t2 = txt('Toque no botão', 80)
            self.g_t3 = linha([('abaixo do ', BRANCO), ('vídeo', AMARELO)], 80)
            self.g_faixa = faixa_texto('Preço conferido hoje', 56, 116, pad=48, max_w=900)
        im = self.fundo.copy()
        im.paste(self.cab, (0, 0), self.cab)
        d = ImageDraw.Draw(im)
        barra(d, self.n, self.n, 1)
        for cam, y, t0 in ((self.g_t1, 560, 0.0), (self.g_t2, 720, 0.25), (self.g_t3, 824, 0.4)):
            a = suave(p(t, t0, 0.32))
            cola(im, cam, W / 2, y + (1 - a) * 30, alpha=a)
        a = p(t, 1.0, 0.32)
        if a > 0:
            cola(im, self.g_faixa, W / 2, 1000, escala=0.6 + 0.4 * pulo(a), alpha=min(1, a * 3))
        a = suave(p(t, 0.2, 0.4))
        cola(im, self.f_rod1, W / 2, 1300, alpha=a)
        cola(im, self.f_rod2, W / 2, 1344, alpha=a)
        return im

    # ---- lista de cenas: (nome, duração, função do quadro)
    def cenas(self):
        cs = [('abre', SEG_ABRE, self.quadro_abre)]
        for i in range(self.n):
            cs.append((f'produto{i + 1}', self.seg_prod, lambda t, i=i: self.quadro_produto(t, i)))
        cs.append(('fecha', SEG_FECHA, self.quadro_fecha))
        return cs


# ------------------------------------------------------------------ som (trilha original, feita por código)
SR = 48000


def _ruido(n, lo, hi, semente):
    x = np.random.default_rng(semente).standard_normal(n)
    X = np.fft.rfft(x)
    f = np.maximum(np.fft.rfftfreq(n, 1 / SR), 1.0)
    y = np.fft.irfft(X / (1 + (lo / f) ** 8) / (1 + (f / hi) ** 8), n)
    return y / (np.abs(y).max() + 1e-9)


def _nota(freq, dur, tau, harm=((1, 1.0), (2, 0.35), (3, 0.12)), ataque=0.004):
    n = int(dur * SR)
    t = np.arange(n) / SR
    y = sum(a * np.sin(2 * np.pi * freq * h * t) for h, a in harm)
    return y * np.exp(-t / tau) * np.minimum(1, t / ataque) * np.minimum(1, (dur - t) / 0.012)


def _poe(buf, y, t0, ganho=1.0, pan=0.0):
    i = int(round(t0 * SR))
    if i < 0:
        y, i = y[-i:], 0
    n = min(len(y), len(buf) - i)
    if n <= 0:
        return
    ang = (pan + 1) * math.pi / 4
    buf[i:i + n, 0] += y[:n] * ganho * math.cos(ang) * 1.414
    buf[i:i + n, 1] += y[:n] * ganho * math.sin(ang) * 1.414


def faz_som(dur, cortes, precos, estalos, teclas, destino):
    """cortes = inícios de cena; precos = instantes do preço; estalos = outros destaques; teclas = digitação."""
    N = int(dur * SR)
    bat, mus, fx = np.zeros((N, 2)), np.zeros((N, 2)), np.zeros((N, 2))
    compassos = int(math.ceil(dur / (4 * BATIDA)))
    acordes = {
        'C': dict(baixo=65.41, pad=(261.63, 329.63, 392.00), arp=(523.25, 659.25, 783.99, 1046.50)),
        'G': dict(baixo=98.00, pad=(246.94, 293.66, 392.00), arp=(493.88, 587.33, 783.99, 987.77)),
        'Am': dict(baixo=110.00, pad=(220.00, 261.63, 329.63), arp=(440.00, 523.25, 659.25, 880.00)),
        'F': dict(baixo=87.31, pad=(220.00, 261.63, 349.23), arp=(440.00, 523.25, 698.46, 880.00)),
    }
    ordem = ['C', 'G', 'Am', 'F']
    t = np.arange(int(0.30 * SR)) / SR
    bumbo = np.sin(2 * np.pi * (55 * t + 110 * 0.030 * (1 - np.exp(-t / 0.030)))) * np.exp(-t / 0.085)
    bumbo[:int(0.006 * SR)] += 0.35 * _ruido(int(0.006 * SR), 1500, 5000, 6) * np.linspace(1, 0, int(0.006 * SR))
    palma = _ruido(int(0.20 * SR), 900, 4200, 1)
    tp = np.arange(len(palma)) / SR
    palma = palma * (np.exp(-tp / 0.07) + 0.6 * np.exp(-np.abs(tp - 0.012) / 0.004) + 0.5 * np.exp(-np.abs(tp - 0.024) / 0.004))
    chim = _ruido(int(0.08 * SR), 7000, 15000, 2)
    chim = chim * np.exp(-np.arange(len(chim)) / SR / 0.022)
    duck = np.ones(N)
    fim_bateria = dur - 2 * BATIDA                      # as 2 últimas batidas ficam só com o acorde soando
    for c in range(compassos):
        t0 = c * 4 * BATIDA
        nome = 'C' if c == compassos - 1 else ordem[c % 4]
        ac = acordes[nome]
        cheio = c >= 1                                   # compasso 0 (abertura) sem bateria
        # base suave
        n = int(4 * BATIDA * SR)
        tt = np.arange(n) / SR
        env = np.minimum(1, tt / 0.25) * np.minimum(1, (4 * BATIDA - tt) / 0.30)
        for f in ac['pad']:
            y = (np.sin(2 * np.pi * f * tt) + np.sin(2 * np.pi * f * 1.003 * tt)) * env
            _poe(mus, y, t0, 0.050)
        for k in range(8):                                # colcheias
            tk = t0 + k * BATIDA / 2
            if tk >= dur - 0.05:
                break
            f = ac['arp'][(0, 1, 2, 3, 2, 1, 2, 3)[k]]
            y = _nota(f, 0.42, 0.16, harm=((1, 1.0), (2, 0.42), (3, 0.22), (4, 0.11), (5, 0.05)))
            pan = 0.35 if k % 2 else -0.35
            _poe(mus, y, tk, 0.200, pan)
            _poe(mus, y, tk + 0.1875, 0.062, -pan)
            _poe(mus, y, tk + 0.375, 0.026, pan)
            if cheio and tk < fim_bateria:
                if k % 2 == 0:
                    _poe(bat, bumbo, tk, 0.36)
                    i = int(tk * SR)
                    m = min(N - i, int(0.35 * SR))
                    duck[i:i + m] *= 1 - 0.42 * np.exp(-np.arange(m) / SR / 0.10)
                    if k in (2, 6):
                        _poe(bat, palma, tk, 0.34)
                else:
                    _poe(bat, chim, tk, 0.240, 0.2)
                    _poe(mus, _nota(ac['baixo'], 0.24, 0.20, harm=((1, 0.6), (2, 0.75), (3, 0.5), (4, 0.3))), tk, 0.15)
        if c == 0:                                        # sobe-som da abertura até a 1ª batida cheia
            n = int(1.2 * SR)
            r = _ruido(n, 2500, 12000, 3) * (np.arange(n) / n) ** 2.2
            _poe(fx, r, 4 * BATIDA - 1.2, 0.10)
    # acorde final soando
    for f in acordes['C']['pad'] + (523.25,):
        _poe(mus, _nota(f, 1.6, 0.7, harm=((1, 1.0), (2, 0.2))), fim_bateria, 0.07)
    _poe(bat, bumbo, fim_bateria, 0.36)
    # passagens de cena
    n = int(0.46 * SR)
    sopro = _ruido(n, 700, 6000, 4) * np.sin(np.pi * np.arange(n) / n) ** 2
    for tc in cortes:
        if tc > 0.1:
            _poe(fx, sopro, tc - 0.20, 0.12)
    # preço: duas notas de sino (si e mi), em tom com a trilha
    for tpz in precos:
        _poe(fx, _nota(987.77, 0.45, 0.16, harm=((1, 1.0), (2, 0.25))), tpz, 0.17)
        _poe(fx, _nota(1318.51, 0.70, 0.26, harm=((1, 1.0), (2, 0.25))), tpz + 0.075, 0.19)
    for te in estalos:
        _poe(fx, _nota(783.99, 0.5, 0.20, harm=((1, 1.0), (2, 0.3))), te, 0.15)
        _poe(fx, _nota(1046.50, 0.6, 0.24, harm=((1, 1.0), (2, 0.3))), te + 0.07, 0.15)
    tique = _ruido(int(0.012 * SR), 1800, 7000, 5) * np.exp(-np.arange(int(0.012 * SR)) / SR / 0.003)
    for tk in teclas:
        _poe(fx, tique, tk, 0.08)
    mix = bat + mus * duck[:, None] + fx
    mix = np.tanh(mix * 1.25) / math.tanh(1.25)
    n = int(0.9 * SR)
    mix[-n:] *= np.linspace(1, 0, n)[:, None] ** 1.5
    mix[:int(0.02 * SR)] *= np.linspace(0, 1, int(0.02 * SR))[:, None]
    mix *= 0.80 / (np.abs(mix).max() + 1e-9)
    with wave.open(str(destino), 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((mix * 32767).astype('<i2').tobytes())


def ganho_som(wav, alvo=-14.0):
    """Quanto aumentar ou baixar (em dB) para a trilha ficar em -14 LUFS, sem passar de -1 dB de pico."""
    r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(wav), '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE).stderr.decode('utf-8', 'ignore')
    try:
        fim = r[r.rindex('Summary:'):]
        lufs = float(fim.split('I:')[1].split('LUFS')[0])
        pico = float(fim.split('Peak:')[1].split('dBFS')[0])
    except (ValueError, IndexError):
        return -3.0
    return max(-12.0, min(alvo - lufs, -1.0 - pico, 12.0))


# ------------------------------------------------------------------ renderização
COR709 = ['-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-colorspace', 'bt709',
          '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv']


def roda(cmd, **kw):
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kw)
    if r.returncode != 0:
        sys.stderr.write(r.stderr.decode('utf-8', 'ignore')[-1500:])
        raise SystemExit(f'ffmpeg falhou: {" ".join(str(c) for c in cmd[:6])} ...')
    return r


def grava_cena(arq, dur, fn, crf):
    tmp = arq.with_name(arq.stem + '.parcial.mp4')
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
           '-i', '-', *COR709, '-c:v', 'libx264', '-preset', 'slow', '-crf', str(crf), '-profile:v', 'high',
           '-g', '60', '-r', str(FPS), '-an', str(tmp)]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    for k in range(int(round(dur * FPS))):
        pr.stdin.write(fn(k / FPS).tobytes())
    pr.stdin.close()
    err = pr.stderr.read()
    if pr.wait() != 0:
        sys.stderr.write(err.decode('utf-8', 'ignore')[-1500:])
        raise SystemExit('ffmpeg falhou ao gravar a cena ' + arq.name)
    os.replace(tmp, arq)


def folha(reel, destino):
    """Um quadro de cada cena, no instante em que tudo está na tela."""
    qs = []
    for nome, dur, fn in reel.cenas():
        qs.append(fn(dur - 0.15 if nome != 'abre' else dur - 0.1))
    cols = 3
    lin = int(math.ceil(len(qs) / cols))
    tw, th = 432, 768
    sh = Image.new('RGB', (cols * tw + (cols + 1) * 12, lin * th + (lin + 1) * 12), (40, 40, 44))
    for i, q in enumerate(qs):
        sh.paste(q.resize((tw, th), Image.LANCZOS), (12 + (i % cols) * (tw + 12), 12 + (i // cols) * (th + 12)))
    sh.save(destino, quality=88)
    return qs


def textos(r, saida):
    ofs = r['ofertas']
    if r.get('modo') == 'anuncio':
        o = ofs[0]
        nome = o.get('nome_legenda') or o['nome']
        pix = ' no Pix' if o.get('pix') else ''
        preco = f'de {brl(o["preco_de"])} por {brl(o["preco"])}{pix}' if o.get('preco_de') else f'{brl(o["preco"])}{pix}'
        L = ['Publicidade · link de afiliado', f'{nome}: {preco} 👇', '',
             f'Preço conferido em {r["conferido"]}; pode mudar. Canal independente (não oficial).', 'Vídeo criado com IA.']
        (saida / 'legenda.txt').write_text('\n'.join(L) + '\n', encoding='utf-8')
        return
    descontos = [pct(o['preco'], o['preco_de']) for o in ofs if o.get('preco_de')]
    ate = f', com até {max(descontos)}% OFF' if descontos and max(descontos) >= 15 else ''
    L = ['Publicidade · links de afiliado', f'{len(ofs)} achados de hoje no Mercado Livre{ate} 👇', '']
    for i, o in enumerate(ofs, 1):
        nome = o.get('nome_legenda') or o['nome']
        pix = ' no Pix' if o.get('pix') else ''
        if o.get('preco_de'):
            L.append(f'{i}) {nome}: de {brl(o["preco_de"])} por {brl(o["preco"])}{pix}')
        else:
            L.append(f'{i}) {nome}: {brl(o["preco"])}{pix}')
    L += ['', f'🔎 Os links estão no nosso canal do Telegram: procure por {CANAL} (ou toque em "Saiba mais" na nossa página).',
          f'Preços conferidos em {r["conferido"]}; podem mudar. Canal independente (não oficial).',
          'Vídeo criado com IA.', '', '#ofertas #achadinhos #promoção']
    (saida / 'legenda.txt').write_text('\n'.join(L) + '\n', encoding='utf-8')
    (saida / 'comentario.txt').write_text(
        f'Os links destas ofertas estão no nosso canal do Telegram: procure por {CANAL}. '
        'Lá entram ofertas conferidas o dia todo. (Publicidade · links de afiliado)\n', encoding='utf-8')


def valida(r, base):
    erros = []
    ofs = r.get('ofertas', [])
    if r.get('modo') == 'anuncio':
        if len(ofs) != 1:
            erros.append('no modo "anuncio" o roteiro precisa de exatamente 1 oferta')
    elif not 3 <= len(ofs) <= 4:
        erros.append('o roteiro precisa de 3 ou 4 ofertas')
    if ' às ' not in r.get('conferido', ''):
        erros.append('falta "conferido" no formato "22/11 às 13h41"')
    for i, o in enumerate(ofs, 1):
        if not o.get('nome') or len(o['nome']) > 60:
            erros.append(f'oferta {i}: nome ausente ou com mais de 60 letras')
        if not o.get('preco') or float(o['preco']) <= 0:
            erros.append(f'oferta {i}: preço ausente')
        if o.get('preco_de') and float(o['preco_de']) <= float(o.get('preco', 0)):
            erros.append(f'oferta {i}: preco_de precisa ser maior que o preço (ou tire o preco_de)')
        if not o.get('foto') or not (base / o['foto']).exists():
            erros.append(f'oferta {i}: foto não encontrada ({o.get("foto")})')
    if erros:
        raise SystemExit('ROTEIRO INVÁLIDO:\n- ' + '\n- '.join(erros))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--roteiro', required=True)
    ap.add_argument('--saida', required=True)
    ap.add_argument('--quadros', action='store_true', help='só gera conferencia.jpg e os textos (rápido)')
    a = ap.parse_args()
    rot = Path(a.roteiro).resolve()
    saida = Path(a.saida).resolve()
    saida.mkdir(parents=True, exist_ok=True)
    r = json.loads(rot.read_text(encoding='utf-8'))
    valida(r, rot.parent)
    reel = Reel(r, rot.parent)
    textos(r, saida)
    qs = folha(reel, saida / 'conferencia.jpg')
    if a.quadros:
        for i, q in enumerate(qs):
            q.save(saida / f'quadro{i}.jpg', quality=90)
        print('OK quadros:', saida / 'conferencia.jpg')
        return
    cenas = reel.cenas()
    total = sum(d for _, d, _ in cenas)
    # instantes para o som
    cortes, precos, estalos, t0 = [], [], [1.0], 0.0
    for nome, dur, _ in cenas:
        cortes.append(t0)
        if nome.startswith('produto'):
            precos.append(t0 + 1.0)
        if nome == 'fecha':
            estalos.append(t0 + 2.5)
            teclas = [t0 + 1.0 + 0.075 * k for k in range(len(CANAL))]
        t0 += dur
    faz_som(total, cortes, precos, estalos, teclas, saida / 'som.wav')
    ganho = ganho_som(saida / 'som.wav')
    crf = 21
    while True:
        arqs = []
        for nome, dur, fn in cenas:
            arq = saida / f'cena-{nome}.mp4'
            grava_cena(arq, dur, fn, crf)
            arqs.append(arq)
        (saida / 'cenas.txt').write_text(''.join(f"file '{x.name}'\n" for x in arqs), encoding='utf-8')
        roda(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', 'cenas.txt', '-c', 'copy', 'mudo.mp4'],
             cwd=saida)
        roda(['ffmpeg', '-y', '-loglevel', 'error', '-i', 'mudo.mp4', '-i', 'som.wav', '-map', '0:v', '-map', '1:a',
              '-c:v', 'copy', '-af', f'volume={ganho:.1f}dB', '-c:a', 'aac', '-b:a', '128k', '-ar', '48000',
              '-movflags', '+faststart', '-shortest', 'reel.parcial.mp4'], cwd=saida)
        os.replace(saida / 'reel.parcial.mp4', saida / 'reel.mp4')
        tam = (saida / 'reel.mp4').stat().st_size
        if tam <= LIMITE_BYTES or crf >= 31:
            break
        crf += 3                                           # passou do limite de envio: comprime um pouco mais
    for x in arqs + [saida / 'cenas.txt', saida / 'mudo.mp4', saida / 'som.wav']:
        x.unlink(missing_ok=True)
    print(f'OK reel.mp4: {total:.1f} s, {tam / 1e6:.2f} MB (crf {crf}) em {saida}')
    if tam > LIMITE_BYTES:
        raise SystemExit('ATENÇÃO: o vídeo passou de 3,6 MB; use 3 ofertas ou fotos mais simples.')


if __name__ == '__main__':
    main()
