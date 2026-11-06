#!/usr/bin/env python3
"""
Gera TODAS as imagens do efeito C08 "Eu no grupo da família" (Effect House).

Como rodar (de qualquer pasta):
    python3 /home/user/quantocobrarpj/tiktok-efeitos/efeito-2-seu-papel-no-grupo/assets/gerar.py

Lê os textos de ../textos.json (do redator) e grava, nesta pasta (assets/):
    titulo.png                 512x512  título que aparece sobre a cabeça antes do sorteio
    cartas/opcao_01..28.png    512x512  as 28 cartas do sorteio (texture sequence do Randomizer 2D)
    reservas/reserva_01..03    512x512  cartas de reserva (trocar 1 por 1 se alguma frase for vetada)
    icone_162.png              162x162  ícone para o formulário de envio (área segura 144x144)
    icone_alt_162.png          162x162  2º ícone opcional (o formulário aceita até 2)
    icone_grande_512.png       512x512  mesmo ícone em tamanho grande (só referência)
    previa.png                         folha de conferência (não vai para o Effect House)

Tudo é desenhado em 2x (ou mais) e reduzido com LANCZOS em alfa pré-multiplicado
(sem serrilhado e sem franja escura). Fontes: Inter / Inter Display (licença OFL).
Emojis: Noto Color Emoji (licença OFL). Nada de visual de aplicativo de mensagem:
sem verde, sem tiques de "lida", sem fundo bege de conversa, balão com rabicho
centralizado (estilo quadrinho), não no canto.
"""
import json
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
EFEITO = os.path.dirname(AQUI)
TEXTOS = json.load(open(os.path.join(EFEITO, "textos.json"), encoding="utf-8"))

F_BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
F_XBOLD = "/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf"
F_BOLD = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
F_REG = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
F_EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

# ---------------------------------------------------------------- paleta
# Rosa, roxo, laranja e azul-céu se alternando (nada de verde: evita lembrar app de mensagem).
# (topo do degradê, base do degradê, tinta escura p/ contorno do texto, tom claro p/ o selo)
PALETA = [
    ((255, 92, 160), (226, 20, 118), (78, 4, 44), (255, 226, 238)),    # rosa
    ((160, 104, 255), (104, 44, 226), (38, 8, 90), (236, 226, 255)),   # roxo
    ((255, 168, 48), (255, 98, 12), (96, 30, 0), (255, 236, 212)),     # laranja
    ((52, 196, 255), (22, 116, 236), (4, 34, 88), (218, 242, 255)),    # azul-céu
]
ROSA, ROXO = (255, 62, 138), (122, 60, 255)
AMEIXA = (43, 15, 69)          # texto escuro do título e sombras
SOMBRA = (30, 8, 50)

# ---------------------------------------------------------------- geometria (em 2x: 1024x1024)
S = 2
N = 512 * S
CORPO = (34, 262, 990, 808)          # retângulo do balão
RAIO = 112
RABICHO = [(440, 796), (584, 796), (512, 904)]   # ponta para baixo, no centro (aponta p/ a cabeça)
BORDA = 16                            # borda branca (sticker)
SELO_C, SELO_R, SELO_R_IN = (512, 262), 132, 115
EMOJI_PX = 180
AREA_TXT = (66, 404, 958, 780)        # onde o texto pode ficar (x0, y0, x1, y1)
TXT_MAX, TXT_MIN = 108, 60            # tamanho da fonte em 2x (54 px e 30 px no final)
CONTORNO = 11                         # contorno máximo do texto em 2x (proporcional: 0,1 em)
ENTRELINHA = 1.13                     # distância entre linhas de base, em "em"


# ---------------------------------------------------------------- utilidades
def reduzir(img, tam):
    """Redimensiona RGBA sem franja escura (alfa pré-multiplicado)."""
    return img.convert("RGBa").resize(tam, Image.LANCZOS).convert("RGBA")


def degrade_v(tam, c1, c2):
    w, h = tam
    col = Image.new("RGBA", (1, h))
    for y in range(h):
        t = y / max(1, h - 1)
        col.putpixel((0, y), tuple(round(c1[i] + (c2[i] - c1[i]) * t) for i in range(3)) + (255,))
    return col.resize((w, h))


def degrade_h(tam, c1, c2):
    w, h = tam
    lin = Image.new("RGBA", (w, 1))
    for x in range(w):
        t = x / max(1, w - 1)
        lin.putpixel((x, 0), tuple(round(c1[i] + (c2[i] - c1[i]) * t) for i in range(3)) + (255,))
    return lin.resize((w, h))


def degrade_diag(tam, c1, c2):
    w, h = tam
    g = degrade_h((w * 2, 1), c1, c2).resize((w * 2, h * 2))
    return g.rotate(-35, resample=Image.BICUBIC).crop((w // 2, h // 2, w // 2 + w, h // 2 + h))


def cor(c, a=255):
    return tuple(c[:3]) + (a,)


def suavizar(mask, r=3):
    """Arredonda cantos vivos (ponta do rabicho) com desfoque + limiar."""
    return mask.filter(ImageFilter.GaussianBlur(r)).point(lambda v: 255 if v >= 128 else (0 if v < 100 else (v - 100) * 9))


def dilatar(mask, px):
    """Engorda a máscara 'px' pixels (borda arredondada)."""
    m = mask.filter(ImageFilter.GaussianBlur(px / 2))
    return m.point(lambda v: 255 if v > 8 else v * 30)


def mascara_balao(tam=(N, N), corpo=CORPO, raio=RAIO, rabicho=RABICHO):
    m = Image.new("L", tam, 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle(corpo, raio, fill=255)
    d.polygon(rabicho, fill=255)
    return suavizar(m)


def circulo(tam, c, r):
    m = Image.new("L", tam, 0)
    ImageDraw.Draw(m).ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), fill=255)
    return m


def sombra(mask, desloc=(0, 16), blur=14, c=SOMBRA, alfa=120):
    s = Image.new("RGBA", mask.size, cor(c, 0))
    a = mask.point(lambda v: v * alfa // 255)
    a = a.transform(a.size, Image.AFFINE, (1, 0, -desloc[0], 0, 1, -desloc[1]))
    s.putalpha(a.filter(ImageFilter.GaussianBlur(blur)))
    return s


def pintar(base, mask, fonte_cor):
    """Pinta 'fonte_cor' (cor RGBA ou imagem) sobre 'base' usando 'mask'."""
    if isinstance(fonte_cor, tuple):
        fonte_cor = Image.new("RGBA", base.size, fonte_cor)
    camada = fonte_cor.copy()
    a = Image.composite(camada.getchannel("A"), Image.new("L", base.size, 0), mask)
    camada.putalpha(a)
    base.alpha_composite(camada)


_cache_emoji = {}


def emoji(ch, px):
    """Renderiza o emoji colorido no tamanho nativo (109) e reduz para 'px'."""
    if ch not in _cache_emoji:
        f = ImageFont.truetype(F_EMOJI, 109, layout_engine=ImageFont.Layout.RAQM)
        im = Image.new("RGBA", (400, 200), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((10, 20), ch, font=f, embedded_color=True)
        _cache_emoji[ch] = im.crop(im.getchannel("A").getbbox())
    im = _cache_emoji[ch]
    k = px / max(im.size)
    return reduzir(im, (max(1, round(im.width * k)), max(1, round(im.height * k))))


def contorno_para(tam):
    return min(CONTORNO, max(6, round(tam * 0.1)))


def ajustar_fonte(linhas, largura_max, maxi, mini, caminho=F_BLACK, contorno=None):
    for t in range(maxi, mini - 1, -2):
        f = ImageFont.truetype(caminho, t)
        c = contorno_para(t) if contorno is None else contorno
        if all(f.getlength(l) + 2 * c <= largura_max for l in linhas):
            return f
    raise SystemExit(f"Texto não cabe nem com fonte {mini}: {linhas}")


def posicoes_linhas(f, linhas, area):
    """Linhas de base para centralizar o bloco (pela altura das maiúsculas) na área."""
    x0, y0, x1, y1 = area
    tam = f.size
    cap = -f.getbbox("H", anchor="ls")[1]
    passo = tam * ENTRELINHA
    altura = cap + passo * (len(linhas) - 1)
    topo = (y0 + y1) / 2 - altura / 2
    return [(x0 + x1) / 2, [topo + cap + i * passo for i in range(len(linhas))]]


def texto_mascara(tam, linhas, f, cx, bases, contorno=0):
    m = Image.new("L", tam, 0)
    d = ImageDraw.Draw(m)
    for l, b in zip(linhas, bases):
        d.text((cx, b), l, font=f, anchor="ms", fill=255, stroke_width=contorno, stroke_fill=255)
    return m


def conferir_dentro(mask_txt, area, nome):
    bb = mask_txt.getbbox()
    x0, y0, x1, y1 = area
    folga = 6
    if bb[0] < x0 - folga or bb[2] > x1 + folga or bb[1] < y0 - 40 or bb[3] > y1 + folga:
        raise SystemExit(f"{nome}: texto saiu da área {bb} vs {area}")


def familia(px, cores=(ROSA, ROXO, (255, 140, 20)), contorno_branco=True):
    """Pictograma próprio de família: 3 bonequinhos (pai, mãe e criança). Desenho original."""
    k = 4
    W = px * k
    im = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    # (centro x, centro da cabeça y, raio da cabeça, largura do corpo, cor)
    pessoas = [
        (0.27, 0.36, 0.13, 0.36, cores[1]),
        (0.73, 0.36, 0.13, 0.36, cores[0]),
        (0.50, 0.55, 0.105, 0.30, cores[2]),
    ]
    for cx, cy, r, lw, c in pessoas:
        m = Image.new("L", (W, W), 0)
        d = ImageDraw.Draw(m)
        X, Y, R = cx * W, cy * W, r * W
        d.ellipse((X - R, Y - R, X + R, Y + R), fill=255)
        top = Y + R * 1.25
        d.rounded_rectangle((X - lw * W / 2, top, X + lw * W / 2, top + 0.62 * W), radius=lw * W / 2, fill=255)
        m = Image.composite(m, Image.new("L", (W, W), 0), circulo((W, W), (W / 2, W * 0.45), W * 0.52))
        corte = Image.new("L", (W, W), 0)
        ImageDraw.Draw(corte).rectangle((0, 0, W, W * 0.93), fill=255)
        m = Image.composite(m, Image.new("L", (W, W), 0), corte)
        if contorno_branco:
            pintar(im, dilatar(m, W * 0.035), (255, 255, 255, 255))
        pintar(im, m, cor(c))
    return reduzir(im, (px, px))


# ---------------------------------------------------------------- carta (resultado)
def desenhar_carta(linha1, linha2, ch, pal, nome):
    topo, base, escura, clara = pal
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    corpo = mascara_balao()
    borda = dilatar(corpo, BORDA)
    selo = circulo((N, N), SELO_C, SELO_R)
    uniao = Image.composite(Image.new("L", (N, N), 255), borda, selo)

    im.alpha_composite(sombra(uniao))
    pintar(im, borda, (255, 255, 255, 255))
    pintar(im, corpo, degrade_v((N, N), topo, base))
    # brilho suave na metade de cima do balão
    brilho = Image.new("L", (N, N), 0)
    ImageDraw.Draw(brilho).rounded_rectangle((CORPO[0] + 26, CORPO[1] + 22, CORPO[2] - 26, CORPO[1] + 210), 90, fill=40)
    pintar(im, Image.composite(brilho.filter(ImageFilter.GaussianBlur(18)), Image.new("L", (N, N), 0), corpo), (255, 255, 255, 255))
    # confete discreto (sempre no mesmo lugar, para a sequência não "piscar")
    rnd = random.Random(8)
    conf = Image.new("L", (N, N), 0)
    dc = ImageDraw.Draw(conf)
    for _ in range(14):
        x = rnd.choice([rnd.uniform(70, 330), rnd.uniform(694, 950)])
        y = rnd.uniform(300, 380)
        rr = rnd.uniform(5, 9)
        dc.ellipse((x - rr, y - rr, x + rr, y + rr), fill=70)
    pintar(im, Image.composite(conf, Image.new("L", (N, N), 0), corpo), (255, 255, 255, 255))

    # selo do emoji
    pintar(im, selo, (255, 255, 255, 255))
    pintar(im, circulo((N, N), SELO_C, SELO_R_IN), cor(clara))
    e = emoji(ch, EMOJI_PX)
    im.alpha_composite(e, (SELO_C[0] - e.width // 2, SELO_C[1] - e.height // 2))

    # texto: branco com contorno escuro + sombra
    linhas = [linha1, linha2]
    f = ajustar_fonte(linhas, AREA_TXT[2] - AREA_TXT[0], TXT_MAX, TXT_MIN)
    cx, bases = posicoes_linhas(f, linhas, AREA_TXT)
    m_cont = texto_mascara((N, N), linhas, f, cx, bases, contorno_para(f.size))
    conferir_dentro(m_cont, AREA_TXT, nome)
    im.alpha_composite(sombra(m_cont, (0, 8), 6, escura, 150))
    pintar(im, m_cont, cor(escura))
    pintar(im, texto_mascara((N, N), linhas, f, cx, bases), (255, 255, 255, 255))
    return reduzir(im, (512, 512)), f.size / S


# ---------------------------------------------------------------- título
def desenhar_titulo():
    t = TEXTOS["titulo_topo"]
    linhas = [t["linha1"], t["linha2"]]
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    corpo = mascara_balao()
    # anel e borda externa mais finos que antes (20/30) para o contorno branco
    # não encostar na beirada do quadro de 512 (antes ficava cortado em x=0 e x=511)
    anel = dilatar(corpo, 12)
    externo = dilatar(corpo, 20)
    selo = circulo((N, N), SELO_C, SELO_R + 6)
    uniao = Image.composite(Image.new("L", (N, N), 255), externo, selo)
    im.alpha_composite(sombra(uniao))
    pintar(im, externo, (255, 255, 255, 255))
    pintar(im, anel, degrade_h((N, N), ROSA, ROXO))
    pintar(im, corpo, (255, 255, 255, 255))
    # selo com o pictograma de família
    pintar(im, selo, (255, 255, 255, 255))
    pintar(im, circulo((N, N), SELO_C, SELO_R_IN), (240, 230, 255, 255))
    fam = familia(196)
    im.alpha_composite(fam, (SELO_C[0] - 98, SELO_C[1] - 96))
    # texto: linha 1 em ameixa, linha 2 em degradê rosa->roxo
    try:
        f = ajustar_fonte(linhas, AREA_TXT[2] - AREA_TXT[0], 116, 70, contorno=0)
    except SystemExit:
        linhas = [linhas[0], linhas[1].replace("…", "...")]
        f = ajustar_fonte(linhas, AREA_TXT[2] - AREA_TXT[0], 116, 70, contorno=0)
    cx, bases = posicoes_linhas(f, linhas, AREA_TXT)
    m1 = texto_mascara((N, N), linhas[:1], f, cx, bases[:1])
    m2 = texto_mascara((N, N), linhas[1:], f, cx, bases[1:])
    conferir_dentro(Image.composite(m1, m2, m1), AREA_TXT, "titulo")
    pintar(im, m1, cor(AMEIXA))
    bb = m2.getbbox()
    g = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    g.paste(degrade_h((bb[2] - bb[0], N), ROSA, ROXO), (bb[0], 0))
    pintar(im, m2, g)
    return reduzir(im, (512, 512)), f.size / S


# ---------------------------------------------------------------- ícone
def balao_icone(w, h, r, tail):
    m = Image.new("L", (w, h + tail), 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle((0, 0, w - 1, h - 1), r, fill=255)
    d.polygon([(w / 2 - tail * 0.75, h - 8), (w / 2 + tail * 0.75, h - 8), (w / 2, h + tail - 1)], fill=255)
    return suavizar(m, 4)


def desenhar_icone(variante="claro"):
    T = 1024
    if variante == "claro":
        im = degrade_diag((T, T), ROSA, ROXO)
    else:
        im = degrade_diag((T, T), (40, 12, 70), (18, 6, 40))
    # brilho radial no centro
    g = circulo((T, T), (T / 2, T * 0.46), T * 0.36).filter(ImageFilter.GaussianBlur(120))
    pintar(im, g.point(lambda v: v * 70 // 255), (255, 255, 255, 255))

    def colar_balao(m, fill, ang, cx, cy, borda=0, sombra_on=True):
        lay = Image.new("RGBA", (T, T), (0, 0, 0, 0))
        mm = Image.new("L", (T, T), 0)
        mm.paste(m, (int(cx - m.width / 2), int(cy - m.height / 2)))
        mm = mm.rotate(ang, resample=Image.BICUBIC, center=(cx, cy))
        if sombra_on:
            lay.alpha_composite(sombra(mm, (0, 18), 22, SOMBRA, 120))
        if borda:
            pintar(lay, dilatar(mm, borda), (255, 255, 255, 255))
        pintar(lay, mm, fill)
        im.alpha_composite(lay)
        return mm

    # dois balões coloridos inteiros (com rabicho) espiando atrás = "cartas" do sorteio
    # (assimétrico de propósito: parece movimento de sorteio e não forma "orelhas")
    colar_balao(balao_icone(330, 230, 78, 64), degrade_v((T, T), PALETA[2][0], PALETA[2][1]), 12, 300, 280, borda=18)
    colar_balao(balao_icone(300, 210, 72, 58), degrade_v((T, T), PALETA[3][0], PALETA[3][1]), -10, 742, 390, borda=18)
    # balão branco da frente com a família
    frente = balao_icone(640, 450, 130, 110)
    colar_balao(frente, (255, 255, 255, 255), 0, 486, 620, borda=0)
    fam = familia(420)
    im.alpha_composite(fam, (486 - 210, 620 - 55 - 210 + 10))
    return im


# ---------------------------------------------------------------- prévia (folha de conferência)
def xadrez(w, h, q=16, c1=(200, 200, 200), c2=(150, 150, 150)):
    im = Image.new("RGBA", (w, h), cor(c1))
    d = ImageDraw.Draw(im)
    for y in range(0, h, q):
        for x in range(0, w, q):
            if (x // q + y // q) % 2:
                d.rectangle((x, y, x + q - 1, y + q - 1), fill=cor(c2))
    return im


def foto_generica(w, h, tipo):
    if tipo == "clara":
        im = degrade_v((w, h), (186, 226, 255), (250, 252, 255))
        d = ImageDraw.Draw(im)
        d.ellipse((w * 0.62, h * 0.06, w * 0.92, h * 0.23), fill=(255, 245, 200, 255))
        d.rectangle((0, h * 0.72, w, h), fill=(235, 238, 242, 255))
    elif tipo == "escura":
        im = degrade_v((w, h), (14, 18, 40), (2, 2, 8))
        rnd = random.Random(3)
        lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for _ in range(26):
            x, y, r = rnd.uniform(0, w), rnd.uniform(0, h * 0.7), rnd.uniform(10, 34)
            d.ellipse((x - r, y - r, x + r, y + r), fill=rnd.choice([(255, 190, 90, 90), (120, 160, 255, 80), (255, 255, 255, 60)]))
        im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(4)))
    elif tipo == "listrada":
        im = Image.new("RGBA", (w, h), (250, 250, 250, 255))
        d = ImageDraw.Draw(im)
        for i in range(-h, w + h, 60):
            d.polygon([(i, 0), (i + 30, 0), (i + 30 - h, h), (i - h, h)], fill=(255, 120, 160, 255))
    else:  # sala
        im = degrade_v((w, h), (120, 96, 150), (60, 44, 80))
        d = ImageDraw.Draw(im)
        d.rectangle((w * 0.08, h * 0.08, w * 0.42, h * 0.38), fill=(255, 220, 160, 255))
        d.rectangle((w * 0.24, h * 0.08, w * 0.26, h * 0.38), fill=(90, 70, 110, 255))
        d.rectangle((0, h * 0.74, w, h), fill=(70, 50, 60, 255))
    return im


def silhueta(im, cx, topo, larg, tom):
    d = ImageDraw.Draw(im)
    hw, hh = larg / 2, larg * 0.62
    d.rounded_rectangle((cx - larg * 0.95, topo + hh * 2.05, cx + larg * 0.95, topo + hh * 3.6), radius=larg * 0.5, fill=tom)
    d.rectangle((cx - larg * 0.18, topo + hh * 1.7, cx + larg * 0.18, topo + hh * 2.2), fill=tom)
    d.ellipse((cx - hw, topo, cx + hw, topo + hh * 2), fill=tom)


def tela(img_over, tipo, rostos=1, W=480, H=853, escala=0.62):
    im = foto_generica(W, H, tipo)
    tom = (70, 70, 80, 255) if tipo != "escura" else (150, 150, 165, 255)
    if rostos == 1:
        centros, larg, esc = [W / 2], W * 0.36, escala
    else:
        centros, larg, esc = [W * 0.27, W * 0.73], W * 0.27, escala * 0.70
    for i, cx in enumerate(centros):
        topo = H * 0.43
        silhueta(im, cx, topo, larg, tom)
        ov = img_over[i] if isinstance(img_over, list) else img_over
        dw = round(W * esc)
        o = reduzir(ov, (dw, dw))
        ponta = round((RABICHO[2][1] + BORDA) / N * dw)
        im.alpha_composite(o, (round(cx - dw / 2), round(topo - 10 - ponta)))
    return im


def borda_tela(im, raio=36):
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), raio, fill=255)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.paste(im, (0, 0), m)
    return out


def montar_previa(itens, titulo_img, cartas, icone, icone_alt):
    W = 2100
    COLS, TW, TH, GAP = 8, 230, 230, 22
    linhas_grade = math.ceil(len(itens) / COLS)
    TOPO_GRADE = 150
    alt_grade = linhas_grade * (TH + 70)
    TOPO_SIM = TOPO_GRADE + alt_grade + 90
    H = TOPO_SIM + 853 + 340
    im = Image.new("RGBA", (W, H), (246, 244, 250, 255))
    d = ImageDraw.Draw(im)
    fT = ImageFont.truetype(F_BLACK, 46)
    fS = ImageFont.truetype(F_BOLD, 26)
    fL = ImageFont.truetype(F_BOLD, 17)
    fl = ImageFont.truetype(F_REG, 15)
    d.text((60, 40), "C08 · Eu no grupo da família — prévia dos assets", font=fT, fill=cor(AMEIXA))
    d.text((60, 100), "Fundo xadrez = transparente. Todas as cartas e o título têm 512x512 (mesmo enquadramento). Ícone: 162x162.", font=fl, fill=(90, 80, 110, 255))
    x0 = (W - (COLS * TW + (COLS - 1) * GAP)) // 2
    for i, (nome, img, legenda) in enumerate(itens):
        cx = x0 + (i % COLS) * (TW + GAP)
        cy = TOPO_GRADE + (i // COLS) * (TH + 70)
        tile = xadrez(TW, TH)
        k = min(TW / img.width, TH / img.height, 1.0 if img.width < TW else 99)
        th = reduzir(img, (round(img.width * k), round(img.height * k)))
        tile.alpha_composite(th, ((TW - th.width) // 2, (TH - th.height) // 2))
        im.alpha_composite(tile, (cx, cy))
        d.text((cx, cy + TH + 8), nome, font=fL, fill=cor(AMEIXA))
        while fl.getlength(legenda) > TW + GAP - 6:
            legenda = legenda[:-2] + "…" if not legenda.endswith("…") else legenda[:-2] + "…"
        d.text((cx, cy + TH + 30), legenda, font=fl, fill=(100, 90, 120, 255))
    d.text((60, TOPO_SIM - 56), "Simulação sobre fotos genéricas (clara, escura, listrada, sala) e versão de 2 rostos", font=fS, fill=cor(AMEIXA))
    telas = [
        tela(titulo_img, "clara"),
        tela(cartas[1], "escura"),
        tela(cartas[8], "listrada"),
        tela([cartas[6], cartas[20]], "sala", rostos=2),
    ]
    tx = (W - (4 * 480 + 3 * 40)) // 2
    rot = ["título (antes do toque)", "opção 02 · fundo escuro", "opção 09 · maior linha (16)", "2 rostos · opções 07 e 21"]
    for i, t in enumerate(telas):
        im.alpha_composite(borda_tela(t), (tx + i * 520, TOPO_SIM))
        d.text((tx + i * 520, TOPO_SIM + 863), rot[i], font=fL, fill=cor(AMEIXA))
    # ícone como o app mostra (cantos arredondados), em tamanho real e pequeno
    yI = TOPO_SIM + 853 + 70
    d.text((tx, yI), "Ícone como aparece no app (cantos arredondados pelo próprio app): 162 px, 96 px e 64 px", font=fS, fill=cor(AMEIXA))
    xx = tx
    for ic in (icone, icone_alt):
        for tam in (162, 96, 64):
            r = reduzir(ic, (tam, tam)) if tam != 162 else ic
            im.alpha_composite(borda_tela(r, raio=round(tam * 0.22)), (xx, yI + 50 + (162 - tam)))
            xx += tam + 24
        xx += 60
    # guia da área segura 144x144 no primeiro ícone
    g = (162 - 144) // 2
    d.rectangle((tx + g, yI + 50 + g, tx + g + 144, yI + 50 + g + 144), outline=(0, 200, 255, 255), width=1)
    d.text((xx, yI + 120), "linha azul = área segura 144x144", font=fl, fill=(0, 140, 200, 255))
    return im


# ---------------------------------------------------------------- execução
def salvar(img, caminho):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    img.save(caminho, optimize=True)
    kb = os.path.getsize(caminho) / 1024
    if kb >= 1000:
        raise SystemExit(f"{caminho} passou de 1 MB ({kb:.0f} KB)")
    return kb


def main():
    relatorio = []
    itens = []
    tit, ft = desenhar_titulo()
    kb = salvar(tit, os.path.join(AQUI, "titulo.png"))
    relatorio.append(("titulo.png", tit.size, kb, f"fonte {ft:.0f}px"))
    itens.append(("titulo.png", tit, "título"))

    cartas = []
    for i, r in enumerate(TEXTOS["resultados"]):
        img, fs = desenhar_carta(r["linha1"], r["linha2"], r["emoji"], PALETA[i % len(PALETA)], r["arquivo"])
        kb = salvar(img, os.path.join(AQUI, "cartas", r["arquivo"]))
        relatorio.append(("cartas/" + r["arquivo"], img.size, kb, f"fonte {fs:.0f}px · {r['texto']}"))
        itens.append((r["arquivo"], img, f"{r['linha1']} / {r['linha2']}"))
        cartas.append(img)

    for i, r in enumerate(TEXTOS["resultados_reserva"]):
        img, fs = desenhar_carta(r["linha1"], r["linha2"], r["emoji"], PALETA[(i + 1) % len(PALETA)], r["arquivo"])
        kb = salvar(img, os.path.join(AQUI, "reservas", r["arquivo"]))
        relatorio.append(("reservas/" + r["arquivo"], img.size, kb, f"fonte {fs:.0f}px · {r['texto']}"))
        itens.append((r["arquivo"], img, "reserva · " + r["texto"]))

    ic = desenhar_icone("claro")
    ic162 = reduzir(ic, (162, 162))
    ic512 = reduzir(ic, (512, 512))
    ica = reduzir(desenhar_icone("escuro"), (162, 162))
    for nome, img in (("icone_162.png", ic162), ("icone_alt_162.png", ica), ("icone_grande_512.png", ic512)):
        kb = salvar(img, os.path.join(AQUI, nome))
        relatorio.append((nome, img.size, kb, ""))
    itens.append(("icone_162.png", ic162, "ícone (envio)"))
    itens.append(("icone_alt_162.png", ica, "ícone alternativo"))

    prev = montar_previa(itens, tit, cartas, ic162, ica)
    prev.convert("RGB").save(os.path.join(AQUI, "previa.png"), optimize=True)
    relatorio.append(("previa.png", prev.size, os.path.getsize(os.path.join(AQUI, "previa.png")) / 1024, "conferência"))

    total_efeito = 0
    for nome, tam, kb, obs in relatorio:
        if nome != "previa.png" and not nome.startswith("reservas") and nome != "icone_grande_512.png" and not nome.startswith("icone"):
            total_efeito += kb
        print(f"{nome:28s} {tam[0]}x{tam[1]:<5d} {kb:7.1f} KB  {obs}")
    print(f"\nTotal das texturas que entram no efeito (título + 28 cartas): {total_efeito/1024:.2f} MB")


if __name__ == "__main__":
    main()
