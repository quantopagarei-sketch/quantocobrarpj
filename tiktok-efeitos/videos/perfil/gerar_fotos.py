#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Foto de perfil da conta: gera as 3 opções, a prancha de conferência e a recomendada.

Como rodar (de qualquer pasta):
    python3 gerar_fotos.py

Precisa de: Python 3 + Pillow + numpy, e do gerador do C02 (Meu próximo carro),
porque o carrinho e as funções de desenho vêm de lá:
    ../../efeito-4-meu-proximo-carro/assets/gerar.py
Assim a foto usa o mesmo carro genérico que já passou pela revisão (sem grade,
sem logo, sem emblema e sem placa) e conversa com os ícones dos efeitos.

Fontes: Inter Display (SIL Open Font License 1.1), em /usr/share/fonts/opentype/inter/.

Regras seguidas:
  - nada de marca, logo, escudo, modelo de carro reconhecível ou rosto de pessoa;
  - sem as duplas de cor de clube: vermelho + branco, azul + preto + branco, verde + branco;
  - desenho no centro, longe dos cantos (a foto aparece em círculo);
  - legível num círculo de 40 px.

Saída (nesta pasta):
  foto_opcao_1.png ... carrinho na mira da câmera, com brilho (1080x1080; ajustada na revisão do crítico)
  foto_opcao_2.png ... dados da sorte no retrovisor (1080x1080)
  foto_opcao_3.png ... selo "CS" na faixa (1080x1080)
  foto_recomendada.png ... cópia da opção escolhida (RECOMENDADA, abaixo)
  prancha_fotos.png ... cada opção em círculo de 200, 80, 40 e 24 px, em fundo claro e escuro (+ a opção 1 antiga)
  simbolo_transparente.png ... carro + mira + brilho da opção 1, sem fundo (fim dos vídeos-cartaz)
"""
import importlib.util
import math
import os
import shutil
import sys

sys.dont_write_bytecode = True  # não deixa __pycache__ na pasta do C02

from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
C02_PY = os.path.normpath(os.path.join(AQUI, "..", "..", "efeito-4-meu-proximo-carro", "assets", "gerar.py"))
_spec = importlib.util.spec_from_file_location("gerar_c02", C02_PY)
c02 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(c02)

RECOMENDADA = 1   # número da opção copiada para foto_recomendada.png

S = 3             # desenha em 3x e reduz (bordas lisas)
N = 1080          # tamanho final
W = N * S

FONT_DIR = "/usr/share/fonts/opentype/inter"
F_BLACK = os.path.join(FONT_DIR, "InterDisplay-Black.otf")
F_XBOLD = os.path.join(FONT_DIR, "InterDisplay-ExtraBold.otf")
F_SEMI = os.path.join(FONT_DIR, "InterDisplay-SemiBold.otf")
F_MED = os.path.join(FONT_DIR, "InterDisplay-Medium.otf")

# ---------------------------------------------------------------- paleta da marca
GRAFITE = "#22252C"   # contorno (o mesmo dos efeitos)
ROXO = "#5B2EFF"
ROSA = "#E23CD8"
LARANJA = "#FF9A3C"
AMARELO = "#FFD43B"
TURQUESA = "#1FC8C0"
BRANCO = "#FFFFFF"

rgb = c02.rgb
camada_cor = c02.camada_cor
com_contorno = c02.com_contorno
colar_centro = c02.colar_centro


# ---------------------------------------------------------------- utilidades
def fundo(paradas, direcao=(0.35, 0.65)):
    return c02.gradiente(W, W, paradas, direcao)


def luz(img, cx, cy, r, alpha, cor=BRANCO):
    """Luz suave redonda (dá destaque ao desenho sem criar borda)."""
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).ellipse([cx - r, cy - r, cx + r, cy + r], fill=int(255 * alpha))
    m = m.filter(ImageFilter.GaussianBlur(r * 0.45))
    img.alpha_composite(camada_cor(img.size, cor, m))


def brilho(r, cor=AMARELO, traco=GRAFITE, borda=BRANCO):
    """Brilho de 4 pontas (o 'filtro'), com traço escuro e borda de figurinha."""
    tam = int(r * 2 + 8)
    im = Image.new("RGBA", (tam, tam), (0, 0, 0, 0))
    c02.estrela4(ImageDraw.Draw(im), tam / 2, tam / 2, r, cor)
    if traco:
        im = com_contorno(im, r * 0.11, traco)
    if borda:
        im = com_contorno(im, r * 0.11, borda)
    return im


def adesivo(im, borda_px, sombra=True):
    """Borda branca de figurinha + sombra curta (como nos ícones dos efeitos)."""
    im = com_contorno(im, borda_px, BRANCO)
    if sombra:
        im, _ = c02.com_sombra(im, 0, 5 * S, 9 * S, 0.30)
    return im


def sombra_chao(img, cx, cy, larg, alt, alpha=0.30):
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).ellipse([cx - larg / 2, cy - alt / 2, cx + larg / 2, cy + alt / 2], fill=int(255 * alpha))
    m = m.filter(ImageFilter.GaussianBlur(alt * 0.35))
    img.alpha_composite(camada_cor(img.size, "#14082E", m))


def finalizar(img):
    return img.convert("RGB").resize((N, N), Image.LANCZOS)


# ---------------------------------------------------------------- ajustes da revisão do crítico (06/11)
# 1) A lanterna do carro do C02 é vermelho-coral (#FF5D4A). Na foto ela vira laranja da marca,
#    para não sobrar nem um ponto de vermelho perto do branco da borda (cores do clube antigo).
# 2) "Mira" de câmera (4 cantos) em volta do carro: diz "filtro de câmera" e evita que
#    "Car Shop · Filtros" + carro com brilho seja lido como loja de filtro de óleo/ar ou lava-jato.
LANTERNA_C02 = (255, 93, 74)
EMOJI_FONT = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"


def sem_vermelho(im, alvo=LANTERNA_C02, novo=LARANJA, tol=60):
    """Troca a cor da lanterna (e a borda suavizada dela) pelo laranja da marca."""
    import numpy as np
    a = np.array(im.convert("RGBA")).astype(int)
    dist = np.sqrt((a[..., 0] - alvo[0]) ** 2 + (a[..., 1] - alvo[1]) ** 2 + (a[..., 2] - alvo[2]) ** 2)
    m = (dist < tol) & (a[..., 3] > 0)
    r, g, b = rgb(novo)[:3]
    a[m, 0], a[m, 1], a[m, 2] = r, g, b
    return Image.fromarray(a.astype("uint8"), "RGBA")


def mira(meia, braco, esp):
    """4 cantos de visor de câmera, brancos com traço escuro (estilo figurinha). Genérico, sem UI de app."""
    tam = int(2 * meia + esp * 4)
    im = Image.new("RGBA", (tam, tam), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = tam / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = c + sx * meia, c + sy * meia
            d.rounded_rectangle([min(x, x - sx * braco), y - esp / 2, max(x, x - sx * braco), y + esp / 2],
                                radius=esp / 2, fill=rgb(BRANCO))
            d.rounded_rectangle([x - esp / 2, min(y, y - sy * braco), x + esp / 2, max(y, y - sy * braco)],
                                radius=esp / 2, fill=rgb(BRANCO))
    return com_contorno(im, esp * 0.28, GRAFITE)


# ---------------------------------------------------------------- opção 1: carrinho na mira (recomendada)
def opcao_1(com_fundo=True):
    """Carro + mira + brilho. com_fundo=False devolve o símbolo em PNG transparente (fim dos vídeos)."""
    escala, cy = 0.64, 0.585
    if com_fundo:
        img = fundo([(0.0, ROXO), (0.55, ROSA), (1.0, LARANJA)], (0.30, 0.70))
        luz(img, W * 0.50, W * 0.55, W * 0.36, 0.30)
    else:
        img = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    carro = sem_vermelho(c02.carro("hatch", TURQUESA, int(W * escala)))
    carro = adesivo(carro, 11 * S)
    if com_fundo:
        sombra_chao(img, W * 0.50, W * (cy + 0.165), W * escala * 0.90, W * 0.05)
    colar_centro(img, mira(W * 0.305, W * 0.10, W * 0.044), W * 0.50, W * 0.50)
    colar_centro(img, carro, W * 0.50, W * cy)
    colar_centro(img, brilho(W * 0.088), W * 0.665, W * 0.345)
    if not com_fundo:
        return img.resize((N, N), Image.LANCZOS)
    colar_centro(img, brilho(W * 0.026, BRANCO, None, None), W * 0.36, W * 0.36)
    return finalizar(img)


# ---------------------------------------------------------------- opção 1 antiga (só para comparar na prancha)
def opcao_1_antiga(com_fundo=True):
    """Versão de antes da revisão do crítico (sem mira, lanterna vermelha). Não usar."""
    if com_fundo:
        img = fundo([(0.0, ROXO), (0.55, ROSA), (1.0, LARANJA)], (0.30, 0.70))
        luz(img, W * 0.50, W * 0.57, W * 0.38, 0.30)
    else:
        img = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    carro = c02.carro("hatch", TURQUESA, int(W * 0.76))
    carro = adesivo(carro, 11 * S)
    if com_fundo:
        sombra_chao(img, W * 0.50, W * 0.80, W * 0.70, W * 0.07)
    colar_centro(img, carro, W * 0.50, W * 0.605)
    colar_centro(img, brilho(W * 0.120), W * 0.715, W * 0.245)
    if not com_fundo:
        return img.resize((N, N), Image.LANCZOS)
    colar_centro(img, brilho(W * 0.040, BRANCO, None, None), W * 0.275, W * 0.300)
    colar_centro(img, brilho(W * 0.026, BRANCO, None, None), W * 0.505, W * 0.165)
    return finalizar(img)


# ---------------------------------------------------------------- opção 2: dados da sorte
PINTAS = {1: [(0.5, 0.5)], 2: [(0.27, 0.27), (0.73, 0.73)], 3: [(0.26, 0.26), (0.5, 0.5), (0.74, 0.74)],
          5: [(0.26, 0.26), (0.74, 0.26), (0.5, 0.5), (0.26, 0.74), (0.74, 0.74)],
          6: [(0.27, 0.24), (0.73, 0.24), (0.27, 0.5), (0.73, 0.5), (0.27, 0.76), (0.73, 0.76)]}


def dado(s, cor, cor_pinta, valor, giro, cor_lado=None):
    """Dado de pelúcia (enfeite de retrovisor), visto de frente com o topo e o lado direito."""
    dx, dy = 0.26 * s, -0.22 * s
    pad = int(0.18 * s)
    w = int(s + dx + 2 * pad)
    h = int(s - dy + 2 * pad)
    x0, y0 = pad, pad - dy
    x1, y1 = x0 + s, y0 + s
    r = 0.13 * s
    sil = [(x0, y1, r), (x0, y0, r), (x0 + dx, y0 + dy, r), (x1 + dx, y0 + dy, r), (x1 + dx, y1 + dy, r), (x1, y1, r)]
    contorno = c02.caminho_arred(sil, 12)
    m = Image.new("L", (w, h), 0)
    dm = ImageDraw.Draw(m)
    dm.polygon(contorno, fill=255)
    # pelúcia: bolinhas em volta da silhueta
    passo, rb = 0.055 * s, 0.040 * s
    pts = contorno + [contorno[0]]
    for i in range(len(pts) - 1):
        (ax, ay), (bx, by) = pts[i], pts[i + 1]
        seg = math.hypot(bx - ax, by - ay)
        n = max(1, int(seg / passo))
        for k in range(n):
            t = k / n
            cx, cy = ax + (bx - ax) * t, ay + (by - ay) * t
            dm.ellipse([cx - rb, cy - rb, cx + rb, cy + rb], fill=255)
    # regiões (frente, topo, lado)
    t_top = -y0 / dy
    topo = [(0, 0), (0, y0), (x1, y0), (x1 + t_top * dx, 0)]
    lado = [(x1, h), (x1, y0), (x1 + t_top * dx, 0), (w, 0), (w, h)]
    cores = Image.new("RGBA", (w, h), rgb(cor))
    dc = ImageDraw.Draw(cores)
    dc.polygon(topo, fill=c02.clarear(cor, 0.40))
    dc.polygon(lado, fill=rgb(cor_lado) if cor_lado else c02.escurecer(cor, 0.22))
    im = c02.recortar(cores, m)
    d = ImageDraw.Draw(im)
    lw = max(2, int(0.035 * s))
    d.rounded_rectangle([x0, y0, x1, y1], radius=r, outline=rgb(GRAFITE), width=lw)
    d.line([(x1 - r * 0.29, y0 + r * 0.29), (x1 + dx - r * 0.3, y0 + dy + r * 0.3)], fill=rgb(GRAFITE), width=lw)
    # pintas da frente
    rp = 0.092 * s
    for (px, py) in PINTAS[valor]:
        cx, cy = x0 + px * s, y0 + py * s
        d.ellipse([cx - rp, cy - rp, cx + rp, cy + rp], fill=rgb(cor_pinta))
    # 1 pinta no topo e 2 no lado (achatadas)
    cx, cy = x0 + s / 2 + dx / 2, y0 + dy / 2
    d.ellipse([cx - rp * 0.95, cy - rp * 0.42, cx + rp * 0.95, cy + rp * 0.42], fill=rgb(cor_pinta))
    for fy in (0.30, 0.70):  # 2 pintas no lado, achatadas na largura
        cx, cy = x1 + dx * 0.5, y0 + fy * s + dy * 0.5
        d.ellipse([cx - rp * 0.42, cy - rp * 0.80, cx + rp * 0.42, cy + rp * 0.80], fill=rgb(cor_pinta))
    im = com_contorno(im, 0.045 * s, GRAFITE)
    return im.rotate(giro, resample=Image.BICUBIC, expand=True)


def retrovisor(larg):
    alt = larg * 0.26
    pad = int(larg * 0.06)
    im = Image.new("RGBA", (int(larg + 2 * pad), int(alt + 2 * pad)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    caixa = [pad, pad, pad + larg, pad + alt]
    d.rounded_rectangle(caixa, radius=alt * 0.45, fill=rgb(GRAFITE))
    vidro = Image.new("L", im.size, 0)
    ins = larg * 0.045
    ImageDraw.Draw(vidro).rounded_rectangle([caixa[0] + ins, caixa[1] + ins, caixa[2] - ins, caixa[3] - ins],
                                            radius=alt * 0.32, fill=255)
    g = c02.gradiente(im.width, im.height, [(0, "#E9F7FF"), (1, "#A9C6F0")], (0.2, 0.8))
    im.alpha_composite(c02.recortar(g, vidro))
    ref = Image.new("L", im.size, 0)
    cx = caixa[0] + larg * 0.30
    ImageDraw.Draw(ref).polygon([(cx, caixa[3]), (cx + larg * 0.08, caixa[3]), (cx + larg * 0.20, caixa[1]),
                                 (cx + larg * 0.12, caixa[1])], fill=210)
    im.alpha_composite(camada_cor(im.size, BRANCO, c02.interseccao(ref, vidro)))
    return im


def opcao_2():
    img = fundo([(0.0, "#2A1680"), (0.5, ROXO), (1.0, "#B23CF0")], (0.25, 0.75))
    luz(img, W * 0.52, W * 0.62, W * 0.34, 0.22)
    d = ImageDraw.Draw(img)
    cx = W * 0.5
    # haste e cordões
    d.rounded_rectangle([cx - W * 0.022, -10, cx + W * 0.022, W * 0.17], radius=W * 0.02, fill=rgb(GRAFITE))
    origem = (cx, W * 0.25)
    pos_a, pos_b = (W * 0.385, W * 0.585), (W * 0.635, W * 0.665)
    for p in (pos_a, pos_b):
        d.line(c02.bezier(origem, (origem[0], origem[1] + W * 0.08), (p[0], p[1] - W * 0.18), p, 30),
               fill=rgb(BRANCO), width=int(W * 0.026), joint="curve")
    for p in (pos_a, pos_b):
        d.line(c02.bezier(origem, (origem[0], origem[1] + W * 0.08), (p[0], p[1] - W * 0.18), p, 30),
               fill=rgb(GRAFITE), width=int(W * 0.012), joint="curve")
    colar_centro(img, adesivo(retrovisor(W * 0.44), 8 * S), cx, W * 0.205)
    da = adesivo(dado(W * 0.27, AMARELO, GRAFITE, 5, 11, "#F2A516"), 9 * S)
    db = adesivo(dado(W * 0.25, TURQUESA, BRANCO, 3, -13, "#0E9FB0"), 9 * S)
    sombra_chao(img, W * 0.52, W * 0.87, W * 0.50, W * 0.05, 0.25)
    colar_centro(img, db, *pos_b)
    colar_centro(img, da, *pos_a)
    colar_centro(img, brilho(W * 0.075), W * 0.825, W * 0.40)
    colar_centro(img, brilho(W * 0.036, BRANCO, None, None), W * 0.19, W * 0.40)
    colar_centro(img, brilho(W * 0.026, BRANCO, None, None), W * 0.80, W * 0.80)
    return finalizar(img)


# ---------------------------------------------------------------- opção 3: selo "CS"
def letras(txt, tam_px, cor_top, cor_bot):
    f = ImageFont.truetype(F_BLACK, int(tam_px))
    bb = f.getbbox(txt)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    pad = int(tam_px * 0.1)
    m = Image.new("L", (w + 2 * pad, h + 2 * pad), 0)
    ImageDraw.Draw(m).text((pad - bb[0], pad - bb[1]), txt, font=f, fill=255)
    g = c02.gradiente(m.width, m.height, [(0, cor_top), (1, cor_bot)], (0.0, 1.0))
    return c02.recortar(g, m)


def faixa(larg, alt):
    im = Image.new("RGBA", (int(larg), int(alt)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, larg - 1, alt - 1], radius=alt * 0.5, fill=rgb("#33363F"))
    n = 5
    tw, th = larg * 0.11, alt * 0.16
    for i in range(n):
        x = larg * (0.12 + i * 0.19)
        d.rounded_rectangle([x, alt / 2 - th / 2, x + tw, alt / 2 + th / 2], radius=th / 2, fill=rgb(AMARELO))
    return im


def opcao_3():
    img = fundo([(0.0, "#FFE766"), (0.6, "#FFC23A"), (1.0, LARANJA)], (0.3, 0.7))
    luz(img, W * 0.5, W * 0.46, W * 0.30, 0.35)
    f = adesivo(com_contorno(faixa(W * 0.70, W * 0.13), 4 * S, GRAFITE), 8 * S)
    colar_centro(img, f, W * 0.5, W * 0.715)
    cs = letras("CS", W * 0.50, "#7B5CFF", "#4A22E0")
    cs = com_contorno(cs, 7 * S, GRAFITE)
    cs = adesivo(cs.rotate(5, resample=Image.BICUBIC, expand=True), 11 * S)
    colar_centro(img, cs, W * 0.49, W * 0.48)
    colar_centro(img, brilho(W * 0.085, TURQUESA), W * 0.79, W * 0.24)
    colar_centro(img, brilho(W * 0.034, BRANCO, None, None), W * 0.22, W * 0.27)
    return finalizar(img)


# ---------------------------------------------------------------- prancha
def circulo(img, d):
    peq = img.resize((d, d), Image.LANCZOS).convert("RGBA")
    m = Image.new("L", (d * 4, d * 4), 0)
    ImageDraw.Draw(m).ellipse([0, 0, d * 4 - 1, d * 4 - 1], fill=255)
    peq.putalpha(m.resize((d, d), Image.LANCZOS))
    return peq


def emoji_img(ch, px):
    """Emoji colorido (Noto) desenhado em 109 e reduzido para px."""
    f = ImageFont.truetype(EMOJI_FONT, size=109)
    im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
    bb = im.getbbox()
    im = im.crop(bb) if bb else im
    return im.resize((px, px), Image.LANCZOS)


NOME_EXIBICAO = ("Car Shop ", "✨", " Filtros e Efeitos")   # nome recomendado (PERFIL.md, revisão do crítico)


def nome_com_emoji(out, d, x, y, fonte, cor):
    a, e, b = NOME_EXIBICAO
    d.text((x, y), a, font=fonte, fill=cor)
    x += d.textlength(a, font=fonte)
    em = emoji_img(e, 15)
    out.paste(em, (int(x), y + 2), em)
    d.text((x + 15, y), b, font=fonte, fill=cor)


def prancha(fotos, nomes):
    LW = 1640
    ROW = 330
    TOP = 128
    out = Image.new("RGB", (LW, TOP + ROW * len(fotos) + 70), "#FFFFFF")
    d = ImageDraw.Draw(out)
    ft = ImageFont.truetype(F_BLACK, 34)
    fs = ImageFont.truetype(F_MED, 19)
    fl = ImageFont.truetype(F_XBOLD, 22)
    fn = ImageFont.truetype(F_SEMI, 15)
    fn2 = ImageFont.truetype(F_MED, 13)
    d.text((32, 26), "Foto de perfil: 3 opções (+ a opção 1 antiga, só para comparar)", font=ft, fill="#111111")
    d.text((32, 74), "Quadrado 1080 px · círculo de 200, 80 e 40 px · fundo claro e escuro · "
                     "40 px ≈ tamanho nos comentários e embaixo do efeito", font=fs, fill="#555555")
    for i, (foto, nome) in enumerate(zip(fotos, nomes)):
        y = TOP + i * ROW
        d.text((32, y + 6), nome, font=fl, fill="#111111")
        q = foto.resize((250, 250), Image.LANCZOS)
        out.paste(q, (32, y + 44))
        # linha do círculo por cima do quadrado (mostra o corte)
        d.ellipse([32, y + 44, 32 + 249, y + 44 + 249], outline="#FFFFFF", width=2)
        for j, (bg, txt, sub) in enumerate((("#F2F2F4", "#111111", "#777777"), ("#121212", "#F2F2F2", "#9A9A9A"))):
            x0 = 310 + j * 660
            d.rounded_rectangle([x0, y + 44, x0 + 640, y + 294], radius=18, fill=bg)
            out.paste(circulo(foto, 200), (x0 + 22, y + 69), circulo(foto, 200))
            out.paste(circulo(foto, 80), (x0 + 250, y + 129), circulo(foto, 80))
            c40 = circulo(foto, 40)
            out.paste(c40, (x0 + 360, y + 149), c40)
            nome_com_emoji(out, d, x0 + 410, y + 150, fn, txt)
            d.text((x0 + 410, y + 170), "@(o atual)", font=fn2, fill=sub)
            c24 = circulo(foto, 24)
            out.paste(c24, (x0 + 368, y + 215), c24)
            d.text((x0 + 400, y + 218), "24 px", font=fn2, fill=sub)
            d.text((x0 + 22, y + 272), "200 px", font=fn2, fill=sub)
            d.text((x0 + 268, y + 214), "80 px", font=fn2, fill=sub)
            d.text((x0 + 360, y + 194), "40 px", font=fn2, fill=sub)
    d.text((32, TOP + ROW * len(fotos) + 18),
           "Sem marca, escudo, modelo de carro reconhecível ou rosto. Cores sem dupla de clube "
           "(nada de vermelho + branco, azul + preto + branco ou verde + branco).", font=fs, fill="#555555")
    return out


def main():
    fotos = [opcao_1(), opcao_2(), opcao_3()]
    nomes = ["Opção 1 · Carrinho na mira da câmera", "Opção 2 · Dados da sorte no retrovisor",
             "Opção 3 · Selo CS na faixa"]
    nomes[RECOMENDADA - 1] += "  (recomendada)"
    for i, f in enumerate(fotos, 1):
        f.save(os.path.join(AQUI, f"foto_opcao_{i}.png"), optimize=True)
    shutil.copyfile(os.path.join(AQUI, f"foto_opcao_{RECOMENDADA}.png"), os.path.join(AQUI, "foto_recomendada.png"))
    antiga = opcao_1_antiga()
    prancha(fotos + [antiga], nomes + ["Opção 1 antiga · sem mira (trocada na revisão do crítico, não usar)"]).save(
        os.path.join(AQUI, "prancha_fotos.png"), optimize=True)
    opcao_1(com_fundo=False).save(os.path.join(AQUI, "simbolo_transparente.png"), optimize=True)
    for nome in ["foto_opcao_1.png", "foto_opcao_2.png", "foto_opcao_3.png", "foto_recomendada.png",
                 "prancha_fotos.png", "simbolo_transparente.png"]:
        p = os.path.join(AQUI, nome)
        im = Image.open(p)
        print(f"{nome}: {im.size[0]}x{im.size[1]}, {os.path.getsize(p) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
