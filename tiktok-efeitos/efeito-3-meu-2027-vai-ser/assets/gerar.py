#!/usr/bin/env python3
"""
Gera TODAS as imagens do efeito C05 "Meu 2027 vai ser" (Effect House, template Future Life).

Como rodar (de qualquer pasta):
    python3 /home/user/quantocobrarpj/tiktok-efeitos/efeito-3-meu-2027-vai-ser/assets/gerar.py
    # opcional: um conjunto extra de respostas num tamanho sob medida
    python3 .../gerar.py --resposta 512x256

Lê os textos de ../textos.json (do redator). Se uma frase mudar lá, é só rodar de novo.

REGRA DO TEMPLATE: o Future Life pinta as artes com uma cor sorteada, então tudo o que
entra no efeito é BRANCO PURO (#FFFFFF) com fundo transparente. Cada arte é, na prática,
uma máscara de alfa: o RGB é 255 em TODOS os pixels (até nos transparentes), para não
aparecer franja escura quando o app filtra/reduz a textura.

Grava, nesta pasta (assets/):
    titulo.png                         1024x512  "MEU 2027 / VAI SER…" (troca a textura do Effect_Title)
    bolha_amor|grana|futebol|carro.png  512x256  rótulos das bolhas (grupo Bubble_Titles), com ícone branco
    respostas_<bolha>/<bolha>_NN.png    512x128  respostas sorteadas (1 sequência por Animated Texture Player)
    reservas/reserva_<bolha>_NN.png     512x128  respostas de reserva (trocar 1 por 1 se alguma for vetada)
    icone_162.png / icone_alt_162.png   162x162  ícone do formulário de envio (área segura 144x144)
    icone_grande_512.png                512x512  mesmo ícone, grande (referência/divulgação)
    variantes/com_sombra/...            mesmas artes com sombra preta suave (usar só se o teste mostrar
                                                  que o template MULTIPLICA a cor; ver LEIA-ME.md)
    variantes/quadrado_512/...          mesmas artes em quadro 512x512 (se as texturas originais forem quadradas)
    variantes/quadrado_512_com_sombra/  idem, com sombra
    variantes/rotulos_sem_icone/        rótulos só com a palavra (512x256)
    variantes/bolha_inteira/            desenho próprio da bolha (512x512), com e sem rótulo
    previa.png                          folha de conferência (NÃO vai para o Effect House)

Tudo é desenhado em 2x (ou mais) e reduzido com LANCZOS. Fonte: Inter Display (licença OFL).
Ícones (coração, moeda, bola, carro, brilhos) são desenhos geométricos próprios: sem marca,
sem time, sem escudo, sem modelo de carro.
"""
import argparse
import json
import math
import os
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
EFEITO = os.path.dirname(AQUI)
with open(os.path.join(EFEITO, "textos.json"), encoding="utf-8") as _f:
    TEXTOS = json.load(_f)

F_BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
F_XBOLD = "/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf"
F_BOLD = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
F_MED = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"

S = 2                 # supersampling das artes brancas
LEAD = 1.10           # distância entre as linhas de base, em "em"
PAREN = 0.84          # linha que começa com "(" (a piada) sai 84% do tamanho
ORDEM_BOLHAS = ["amor", "grana", "futebol", "carro"]

# cores só para a prévia / ícone (as artes do efeito são brancas)
AMEIXA = (43, 15, 69)
ROXO = (122, 60, 255)
ROSA = (255, 62, 138)
LARANJA = (255, 140, 40)
AMARELO = (255, 214, 10)
CIANO = (40, 214, 255)
VERDE_LIMA = (120, 226, 80)

_fontes = {}


def fonte(caminho, px):
    k = (caminho, max(1, int(round(px))))
    if k not in _fontes:
        _fontes[k] = ImageFont.truetype(caminho, k[1])
    return _fontes[k]


# ------------------------------------------------------------------ utilidades
def para_branco(mascara_grande, tam):
    """Máscara L em 2x -> PNG branco puro (RGB 255 em todo pixel) com alfa reduzido em LANCZOS."""
    a = mascara_grande.resize(tam, Image.LANCZOS)
    out = Image.new("RGBA", tam, (255, 255, 255, 0))
    out.putalpha(a)
    return out


def para_branco_com_sombra(mascara_grande, tam, s=S, dil=3, blur=3.5, dy=2, forca=0.62):
    """Branco + sombra preta suave (dilatação + desfoque), em alfa pré-multiplicado."""
    g = mascara_grande
    tam_dil = 2 * int(round(dil * s)) + 1
    sombra = g.filter(ImageFilter.MaxFilter(tam_dil)).filter(ImageFilter.GaussianBlur(blur * s))
    sombra = ImageChops.offset(sombra, 0, int(round(dy * s)))
    sombra = sombra.point(lambda v: int(v * forca))
    base = Image.new("RGBA", g.size, (0, 0, 0, 0))
    base.putalpha(sombra)
    topo = Image.new("RGBA", g.size, (255, 255, 255, 0))
    topo.putalpha(g)
    comp = Image.alpha_composite(base, topo)
    return comp.convert("RGBa").resize(tam, Image.LANCZOS).convert("RGBA")


def reduzir(img, tam):
    return img.convert("RGBa").resize(tam, Image.LANCZOS).convert("RGBA")


def salvar(img, caminho):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    img.save(caminho, optimize=True)
    kb = os.path.getsize(caminho) / 1024
    assert kb < 1000, f"{caminho} passou de 1 MB ({kb:.0f} KB)"
    assert max(img.size) <= 1024, f"{caminho} passou de 1024 px"
    REGISTRO.append((os.path.relpath(caminho, AQUI), img.size, kb))
    return img


REGISTRO = []


def caixa_tinta(mascara, limiar=8):
    """bbox do que tem tinta (alfa > limiar)."""
    return mascara.point(lambda v: 255 if v > limiar else 0).getbbox()


def conferir_borda(img, nome, folga=1, limiar=8):
    """Garante que nada encosta/corta na borda (texto nunca cortado)."""
    bb = caixa_tinta(img.getchannel("A"), limiar)
    w, h = img.size
    if bb is None:
        raise SystemExit(f"ERRO: {nome} saiu vazio")
    if bb[0] < folga or bb[1] < folga or bb[2] > w - folga or bb[3] > h - folga:
        raise SystemExit(f"ERRO: {nome} encosta na borda {bb} (canvas {w}x{h})")


def conferir_glifos():
    """Confere se a fonte tem todos os caracteres usados (compara com a caixa de 'glifo faltando')."""
    usados = set()
    for r in TEXTOS["resultados"] + TEXTOS["reservas"]:
        usados |= set(r["linha1"] + r["linha2"])
    usados |= set(TEXTOS["titulo_topo"]["linha1"] + TEXTOS["titulo_topo"]["linha2"])
    for b in TEXTOS["bolhas"]:
        usados |= set(b["rotulo"])
    usados |= set(TEXTOS["regras_texto"]["glifos_necessarios_na_fonte"]) | set("$")
    usados.discard(" ")
    f = fonte(F_BLACK, 60)

    def desenho(c):
        im = Image.new("L", (120, 120), 0)
        ImageDraw.Draw(im).text((20, 90), c, font=f, fill=255, anchor="ls")
        return im.tobytes()

    faltando_ref = desenho(chr(0xE000))          # caixa de "glifo faltando" (área de uso privado)
    faltando = [c for c in sorted(usados) if desenho(c) == faltando_ref]
    if faltando:
        raise SystemExit(f"ERRO: a fonte não tem os glifos {faltando}")
    return "".join(sorted(usados))


# ------------------------------------------------------------------ desenhos brancos (máscaras L)
def poligono_suave(mask, pts, raio):
    """Desenha polígono com cantos arredondados (desfoque + limiar) e soma na máscara."""
    tmp = Image.new("L", mask.size, 0)
    ImageDraw.Draw(tmp).polygon(pts, fill=255)
    if raio > 0:
        tmp = tmp.filter(ImageFilter.GaussianBlur(raio)).point(lambda v: 255 if v >= 128 else 0)
    mask.paste(ImageChops.lighter(mask, tmp))


def coracao(mask, cx, cy, h):
    pts = []
    for i in range(400):
        t = 2 * math.pi * i / 400
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((x, y))
    ys = [p[1] for p in pts]
    xs = [p[0] for p in pts]
    esc = h / (max(ys) - min(ys))
    my = (max(ys) + min(ys)) / 2
    mx = (max(xs) + min(xs)) / 2
    pts = [(cx + (x - mx) * esc, cy + (y - my) * esc) for x, y in pts]
    ImageDraw.Draw(mask).polygon(pts, fill=255)


def moeda(mask, cx, cy, h):
    r = h / 2
    d = ImageDraw.Draw(mask)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
    ri, w = r * 0.80, r * 0.075
    d.ellipse((cx - ri, cy - ri, cx + ri, cy + ri), outline=0, width=max(1, int(w)))
    f = fonte(F_BLACK, r * 1.18)
    d.text((cx, cy), "$", font=f, fill=0, anchor="mm")


def pentagono(cx, cy, r, rot=-90):
    return [(cx + r * math.cos(math.radians(rot + 72 * k)), cy + r * math.sin(math.radians(rot + 72 * k)))
            for k in range(5)]


def bola(mask, cx, cy, h):
    r = h / 2
    tmp = Image.new("L", mask.size, 0)
    d = ImageDraw.Draw(tmp)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
    centro = pentagono(cx, cy, r * 0.34)
    d.polygon(centro, fill=0)
    lw = max(1, int(r * 0.075))
    for k in range(5):
        ang = math.radians(-90 + 72 * k)
        vx, vy = centro[k]
        ox, oy = cx + r * 0.62 * math.cos(ang), cy + r * 0.62 * math.sin(ang)
        d.line((vx, vy, ox, oy), fill=0, width=lw)
        px, py = cx + r * 0.98 * math.cos(ang), cy + r * 0.98 * math.sin(ang)
        d.polygon(pentagono(px, py, r * 0.36, rot=-90 + 72 * k + 180), fill=0)
    # aro externo para manter a silhueta redonda
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=255, width=max(1, int(r * 0.09)))
    mask.paste(ImageChops.lighter(mask, tmp))


def carro(mask, cx, cy, h):
    """Carro genérico (hatch de lado), sem marca nem modelo. h = altura total."""
    w = h / 0.56
    ox, oy = cx, cy - h / 2 + 0.20 * w      # oy = topo da carroceria (linha da cintura)

    def P(x, y):
        return (ox + x * w, oy + y * w)

    tmp = Image.new("L", mask.size, 0)
    d = ImageDraw.Draw(tmp)
    rr = 0.09 * w
    d.rounded_rectangle((*P(-0.5, 0.0), *P(0.5, 0.26)), radius=rr, fill=255)
    cab = Image.new("L", mask.size, 0)
    ImageDraw.Draw(cab).polygon([P(-0.36, 0.03), P(-0.24, -0.20), P(0.10, -0.20), P(0.30, 0.03)], fill=255)
    cab = cab.filter(ImageFilter.GaussianBlur(0.035 * w)).point(lambda v: 255 if v >= 110 else 0)
    tmp = ImageChops.lighter(tmp, cab)
    d = ImageDraw.Draw(tmp)
    janelas = Image.new("L", mask.size, 0)
    dj = ImageDraw.Draw(janelas)
    dj.polygon([P(-0.28, -0.005), P(-0.205, -0.15), P(-0.07, -0.15), P(-0.07, -0.005)], fill=255)
    dj.polygon([P(-0.025, -0.005), P(-0.025, -0.15), P(0.075, -0.15), P(0.205, -0.005)], fill=255)
    janelas = janelas.filter(ImageFilter.GaussianBlur(0.012 * w)).point(lambda v: 255 if v >= 128 else 0)
    tmp = ImageChops.subtract(tmp, janelas)
    d = ImageDraw.Draw(tmp)
    for sx in (-0.29, 0.29):
        wx, wy = P(sx, 0.26)
        rc = 0.135 * w
        d.ellipse((wx - rc, wy - rc, wx + rc, wy + rc), fill=0)          # caixa de roda
        rd = 0.105 * w
        d.ellipse((wx - rd, wy - rd, wx + rd, wy + rd), fill=255)        # pneu
        rh = 0.042 * w
        d.ellipse((wx - rh, wy - rh, wx + rh, wy + rh), fill=0)          # calota
    # farol (frente = direita) e lanterna
    d.rounded_rectangle((*P(0.42, 0.055), *P(0.485, 0.10)), radius=0.015 * w, fill=0)
    d.rounded_rectangle((*P(-0.485, 0.055), *P(-0.445, 0.11)), radius=0.012 * w, fill=0)
    mask.paste(ImageChops.lighter(mask, tmp))


ICONES = {"amor": coracao, "grana": moeda, "futebol": bola, "carro": carro}
# altura relativa de cada ícone (equilíbrio visual: o coração e o carro parecem menores)
ICONE_ESC = {"amor": 1.0, "grana": 1.0, "futebol": 1.0, "carro": 0.86}


def brilho(mask, cx, cy, r, valor=255):
    """Brilho de 4 pontas (astroide)."""
    pts = []
    for i in range(240):
        t = 2 * math.pi * i / 240
        c, s_ = math.cos(t), math.sin(t)
        x = r * math.copysign(abs(c) ** 2.6, c)
        y = r * math.copysign(abs(s_) ** 2.6, s_)
        pts.append((cx + x, cy + y))
    ImageDraw.Draw(mask).polygon(pts, fill=valor)


def ponto(mask, cx, cy, r, valor=255):
    ImageDraw.Draw(mask).ellipse((cx - r, cy - r, cx + r, cy + r), fill=valor)


# ------------------------------------------------------------------ texto
def tam_linha(linha, s):
    return s * PAREN if linha.strip().startswith("(") else s


def cap_altura(s):
    return -fonte(F_BLACK, s).getbbox("H", anchor="ls")[1]


def linhas_encostam(l1, l2, s, folga=0.05):
    """Confere no pixel se um acento/cedilha/parêntese de uma linha encosta na outra
    (a caixa pode se sobrepor sem os desenhos se tocarem, ex.: Ç de BUZINAÇO x Ã de CAMPEÃO)."""
    W, H = int(s * 9), int(s * 3)
    y1 = s * 1.1
    a = Image.new("L", (W, H), 0)
    ImageDraw.Draw(a).text((W / 2, y1), l1, font=fonte(F_BLACK, tam_linha(l1, s)), fill=255, anchor="ms")
    b = Image.new("L", (W, H), 0)
    ImageDraw.Draw(b).text((W / 2, y1 + LEAD * s), l2, font=fonte(F_BLACK, tam_linha(l2, s)), fill=255, anchor="ms")
    k = 2 * max(1, int(s * folga)) + 1
    a = a.filter(ImageFilter.MaxFilter(k)).point(lambda v: 255 if v > 60 else 0)
    b = b.point(lambda v: 255 if v > 60 else 0)
    return ImageChops.multiply(a, b).getbbox() is not None


def layout_respostas(itens, W, H, mx, my, s_max):
    """Acha UM tamanho de fonte (igual para todas as respostas, para o sorteio não 'pular')
    em que todas cabem: largura e altura dentro das margens, sem encostar uma linha na outra.
    Devolve (s, y_base1)."""
    s = s_max
    while s > 10:
        cap = cap_altura(s)
        lead = LEAD * s
        y1 = H / 2 - (cap + lead) / 2 + cap          # bloco de caixa-alta centralizado
        topo, base, ok = 1e9, -1e9, True
        for l1, l2 in itens:
            b1 = fonte(F_BLACK, tam_linha(l1, s)).getbbox(l1, anchor="ms")
            b2 = fonte(F_BLACK, tam_linha(l2, s)).getbbox(l2, anchor="ms") if l2 else None
            larg = max(b1[2] - b1[0], (b2[2] - b2[0]) if b2 else 0)
            if larg > W - 2 * mx:
                ok = False
                break
            if b2 and (lead + b2[1]) - b1[3] < 0.06 * s and linhas_encostam(l1, l2, s):
                ok = False
                break
            topo = min(topo, y1 + b1[1], (y1 + lead + b2[1]) if b2 else 1e9)
            base = max(base, y1 + b1[3], (y1 + lead + b2[3]) if b2 else -1e9)
        if ok:
            if topo >= my and base <= H - my:
                return s, y1
            if base - topo <= H - 2 * my:                   # cabe, só precisa deslocar
                desl = (my - topo) if topo < my else (H - my - base)
                return s, y1 + desl
        s -= 1
    raise SystemExit("ERRO: não coube nenhuma resposta")


def mascara_resposta(l1, l2, W, H, s, y1):
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    d.text((W / 2, y1), l1, font=fonte(F_BLACK, tam_linha(l1, s)), fill=255, anchor="ms")
    if l2:
        d.text((W / 2, y1 + LEAD * s), l2, font=fonte(F_BLACK, tam_linha(l2, s)), fill=255, anchor="ms")
    return m


# ------------------------------------------------------------------ título
def mascara_titulo(W, H, margem):
    """'MEU 2027' grande + 'VAI SER…' menor, com brilhos. W,H já em 2x."""
    t = TEXTOS["titulo_topo"]
    l1, l2 = t["linha1"], t["linha2"]
    k2 = 0.80                      # linha 2 em 80%
    deco = 0.16                    # espaço lateral reservado para os brilhos (fração da largura útil)
    s = int(H)
    while s > 10:
        f1, f2 = fonte(F_BLACK, s), fonte(F_BLACK, s * k2)
        b1, b2 = f1.getbbox(l1, anchor="ms"), f2.getbbox(l2, anchor="ms")
        lead = 1.02 * s
        alt = (lead + b2[3]) - b1[1]
        larg = max(b1[2] - b1[0], b2[2] - b2[0])
        if larg <= (W - 2 * margem) * (1 - deco) and alt <= H - 2 * margem:
            break
        s -= 2
    y1 = H / 2 - alt / 2 - b1[1]
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    d.text((W / 2, y1), l1, font=f1, fill=255, anchor="ms")
    d.text((W / 2, y1 + lead), l2, font=f2, fill=255, anchor="ms")
    # brilhos: um grande no canto de cima à direita do "2027", um médio à esquerda do "VAI SER"
    x_dir = W / 2 + b1[2]
    x_esq = W / 2 + b2[0]
    cap = cap_altura(s)
    brilho(m, x_dir + 0.30 * cap, y1 - cap * 0.92, cap * 0.30)
    brilho(m, x_dir + 0.62 * cap, y1 - cap * 0.40, cap * 0.13)
    brilho(m, x_esq - 0.42 * cap, y1 + lead - cap * 0.55, cap * 0.22)
    ponto(m, x_esq - 0.22 * cap, y1 + lead - cap * 0.05, cap * 0.05)
    ponto(m, W / 2 + b1[0] - 0.28 * cap, y1 - cap * 0.75, cap * 0.06)
    return m


# ------------------------------------------------------------------ rótulo (ícone + palavra)
def tamanho_rotulos(W, H, mx, icone_rel, com_icone):
    """Um tamanho de fonte para os 4 rótulos (consistência)."""
    s = int(H)
    while s > 10:
        cap = cap_altura(s)
        ok = True
        for b in TEXTOS["bolhas"]:
            bb = fonte(F_BLACK, s).getbbox(b["rotulo"], anchor="ms")
            if bb[2] - bb[0] > W - 2 * mx:
                ok = False
            alt = cap + (cap * icone_rel + cap * 0.30 if com_icone else 0)
            if alt > H - 2 * mx * 0.6:
                ok = False
        if ok:
            return s
        s -= 1


def mascara_rotulo(bolha, W, H, s, icone_rel=1.15, com_icone=True, deslocar_y=0):
    m = Image.new("L", (W, H), 0)
    cap = cap_altura(s)
    hi = cap * icone_rel * ICONE_ESC[bolha]
    gap = cap * 0.30
    alt_bloco = cap + (cap * icone_rel + gap if com_icone else 0)
    topo = H / 2 - alt_bloco / 2 + deslocar_y
    if com_icone:
        ICONES[bolha](m, W / 2, topo + cap * icone_rel / 2, hi)
        base = topo + cap * icone_rel + gap + cap
    else:
        base = topo + cap
    rot = next(b["rotulo"] for b in TEXTOS["bolhas"] if b["id"] == bolha)
    ImageDraw.Draw(m).text((W / 2, base), rot, font=fonte(F_BLACK, s), fill=255, anchor="ms")
    return m


# ------------------------------------------------------------------ bolha inteira (desenho próprio)
def mascara_bolha(N, com_rotulo=None, s_rotulo=None):
    """Bolha de sabão própria: aro, brilho em meia-lua, reflexo e 2 bolhinhas satélites.
    Tudo em tons de alfa (branco). N = lado em 2x."""
    m = Image.new("L", (N, N), 0)
    cx, cy, r = N * 0.47, N * 0.53, N * 0.415
    # preenchimento: mais forte perto do aro (efeito de película)
    prof = Image.radial_gradient("L").resize((int(2 * r), int(2 * r)))   # 0 no centro, 255 na borda
    prof = prof.point(lambda v: int(22 + 58 * (v / 255) ** 2.2) if v < 255 else 0)
    disco = Image.new("L", prof.size, 0)
    ImageDraw.Draw(disco).ellipse((0, 0, prof.size[0] - 1, prof.size[1] - 1), fill=255)
    m.paste(prof, (int(cx - r), int(cy - r)), disco)
    d = ImageDraw.Draw(m)
    aro = N * 0.022
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=255, width=int(aro))
    # meia-lua de brilho (cima-esquerda)
    rb = r * 0.80
    d.arc((cx - rb, cy - rb, cx + rb, cy + rb), start=200, end=252, fill=235, width=int(N * 0.03))
    for ang in (200, 252):
        a = math.radians(ang)
        ponto(m, cx + rb * math.cos(a), cy + rb * math.sin(a), N * 0.03 / 2 - 1, 235)
    ponto(m, cx + rb * math.cos(math.radians(266)), cy + rb * math.sin(math.radians(266)), N * 0.016, 235)
    # reflexo fraco embaixo-direita
    rr = r * 0.86
    d.arc((cx - rr, cy - rr, cx + rr, cy + rr), start=20, end=70, fill=120, width=int(N * 0.014))
    # bolhinhas satélites (cima-direita)
    for (bx, by, br) in ((0.885, 0.135, 0.062), (0.965, 0.255, 0.028)):
        bx, by, br = N * bx, N * by, N * br
        sub = Image.new("L", (N, N), 0)
        ds = ImageDraw.Draw(sub)
        ds.ellipse((bx - br, by - br, bx + br, by + br), fill=50)
        ds.ellipse((bx - br, by - br, bx + br, by + br), outline=255, width=max(2, int(N * 0.012)))
        ds.arc((bx - br * 0.62, by - br * 0.62, bx + br * 0.62, by + br * 0.62), 200, 250, fill=235,
               width=max(2, int(N * 0.01)))
        m.paste(ImageChops.lighter(m, sub))
    if com_rotulo:
        lab = mascara_rotulo(com_rotulo, int(2 * r * 0.66), int(2 * r * 0.66), s_rotulo, icone_rel=1.45)
        m.paste(ImageChops.lighter(m.crop((int(cx - lab.size[0] / 2), int(cy - lab.size[1] / 2),
                                            int(cx - lab.size[0] / 2) + lab.size[0],
                                            int(cy - lab.size[1] / 2) + lab.size[1])), lab),
                (int(cx - lab.size[0] / 2), int(cy - lab.size[1] / 2)))
    return m


# ------------------------------------------------------------------ conjuntos
def itens_respostas():
    return [(r["linha1"], r["linha2"]) for r in TEXTOS["resultados"] + TEXTOS["reservas"]]


def gerar_conjunto(destino, resp_tam, rot_tam, tit_tam, sombra, margens_resp, so_respostas=False):
    """Gera título, rótulos, respostas e reservas num formato. Devolve info do layout."""
    conv = para_branco_com_sombra if sombra else para_branco
    W, H = resp_tam[0] * S, resp_tam[1] * S
    mx, my = margens_resp[0] * S, margens_resp[1] * S
    s, y1 = layout_respostas(itens_respostas(), W, H, mx, my, s_max=int(H))
    info = {"fonte_resposta_px": round(s / S, 1)}
    for r in TEXTOS["resultados"]:
        img = conv(mascara_resposta(r["linha1"], r["linha2"], W, H, s, y1), resp_tam)
        conferir_borda(img, r["arquivo"])
        salvar(img, os.path.join(destino, r["arquivo"]))
    for r in TEXTOS["reservas"]:
        img = conv(mascara_resposta(r["linha1"], r["linha2"], W, H, s, y1), resp_tam)
        conferir_borda(img, r["arquivo"])
        salvar(img, os.path.join(destino, r["arquivo"]))
    if so_respostas:
        return info
    # rótulos
    RW, RH = rot_tam[0] * S, rot_tam[1] * S
    rmx = (36 if rot_tam[0] == rot_tam[1] else 22) * S
    sr = tamanho_rotulos(RW, RH, rmx, 1.15, True)
    info["fonte_rotulo_px"] = round(sr / S, 1)
    for b in TEXTOS["bolhas"]:
        img = conv(mascara_rotulo(b["id"], RW, RH, sr), rot_tam)
        conferir_borda(img, b["arquivo_rotulo"])
        salvar(img, os.path.join(destino, b["arquivo_rotulo"]))
    # título
    TW, TH = tit_tam[0] * S, tit_tam[1] * S
    img = conv(mascara_titulo(TW, TH, (24 if tit_tam[0] != tit_tam[1] else 40) * S), tit_tam)
    conferir_borda(img, "titulo.png")
    salvar(img, os.path.join(destino, "titulo.png"))
    return info


def gerar_extras():
    # rótulos só com a palavra
    RW, RH = 512 * S, 256 * S
    sr = tamanho_rotulos(RW, RH, 22 * S, 0, False)
    for b in TEXTOS["bolhas"]:
        img = para_branco(mascara_rotulo(b["id"], RW, RH, sr, com_icone=False), (512, 256))
        conferir_borda(img, "rotulo sem icone")
        salvar(img, os.path.join(AQUI, "variantes", "rotulos_sem_icone", b["arquivo_rotulo"]))
    # bolha inteira (desenho próprio) com e sem rótulo
    N = 512 * S
    r_int = N * 0.415
    sr_b = tamanho_rotulos(int(2 * r_int * 0.66), int(2 * r_int * 0.66), 0, 1.45, True)
    vazia = para_branco(mascara_bolha(N), (512, 512))
    conferir_borda(vazia, "bolha_vazia")
    salvar(vazia, os.path.join(AQUI, "variantes", "bolha_inteira", "bolha_vazia.png"))
    for b in TEXTOS["bolhas"]:
        img = para_branco(mascara_bolha(N, b["id"], sr_b), (512, 512))
        conferir_borda(img, "bolha inteira")
        salvar(img, os.path.join(AQUI, "variantes", "bolha_inteira", f"bolha_inteira_{b['id']}.png"))


# ------------------------------------------------------------------ ícone colorido (formulário)
def degrade_diag(N, cores):
    """Degradê diagonal (cima-esquerda -> baixo-direita) com várias paradas."""
    lin = Image.new("L", (256, 1))
    lin.putdata(list(range(256)))
    gx = lin.resize((N, N), Image.BILINEAR)                       # 0 à esquerda, 255 à direita
    gy = lin.transpose(Image.Transpose.TRANSPOSE).resize((N, N), Image.BILINEAR)   # 0 em cima
    t = ImageChops.add(gx.point(lambda v: v // 2), gy.point(lambda v: v // 2))
    n = len(cores) - 1
    lut = []
    for v in range(256):
        x = v / 255 * n
        i = min(int(x), n - 1)
        f = x - i
        lut.append(tuple(int(cores[i][c] + (cores[i + 1][c] - cores[i][c]) * f) for c in range(3)))
    return Image.merge("RGB", [t.point([lut[v][c] for v in range(256)]) for c in range(3)])


def bolha_colorida(N, cx, cy, r, base):
    """Bolha de sabão colorida (iridescente) para o ícone."""
    camada = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    # película: branco translúcido mais forte perto do aro
    prof = Image.radial_gradient("L").resize((int(2 * r), int(2 * r)))
    prof = prof.point(lambda v: int(30 + 90 * (v / 255) ** 2.4) if v < 255 else 0)
    disco = Image.new("L", prof.size, 0)
    ImageDraw.Draw(disco).ellipse((0, 0, prof.size[0] - 1, prof.size[1] - 1), fill=255)
    film = Image.new("RGBA", prof.size, (255, 255, 255, 0))
    film.putalpha(ImageChops.multiply(prof, disco))
    camada.alpha_composite(film, (int(cx - r), int(cy - r)))
    d = ImageDraw.Draw(camada)
    # aro iridescente: ciano -> amarelo -> rosa
    paradas = [CIANO, (160, 255, 200), AMARELO, (255, 150, 200), ROSA, (170, 120, 255), CIANO]
    passos = 180
    larg = int(r * 0.075)
    for i in range(passos):
        a0 = 360 * i / passos
        x = i / passos * (len(paradas) - 1)
        k = min(int(x), len(paradas) - 2)
        f = x - k
        cor = tuple(int(paradas[k][c] + (paradas[k + 1][c] - paradas[k][c]) * f) for c in range(3))
        d.arc((cx - r, cy - r, cx + r, cy + r), a0 - 0.6, a0 + 360 / passos + 0.6, fill=cor + (255,), width=larg)
    ri = r - larg * 0.55
    d.ellipse((cx - ri, cy - ri, cx + ri, cy + ri), outline=(255, 255, 255, 235), width=max(2, int(r * 0.03)))
    # brilho meia-lua
    rb = r * 0.78
    d.arc((cx - rb, cy - rb, cx + rb, cy + rb), 198, 250, fill=(255, 255, 255, 240), width=int(r * 0.075))
    for ang in (198, 250):
        a = math.radians(ang)
        e = r * 0.075 / 2
        d.ellipse((cx + rb * math.cos(a) - e, cy + rb * math.sin(a) - e,
                   cx + rb * math.cos(a) + e, cy + rb * math.sin(a) + e), fill=(255, 255, 255, 240))
    a = math.radians(266)
    e = r * 0.045
    d.ellipse((cx + rb * math.cos(a) - e, cy + rb * math.sin(a) - e,
               cx + rb * math.cos(a) + e, cy + rb * math.sin(a) + e), fill=(255, 255, 255, 240))
    return camada


def icone(N, fundo="claro"):
    if fundo == "claro":
        bg = degrade_diag(N, [ROXO, ROSA, LARANJA]).convert("RGBA")
        confete = [AMARELO, CIANO, (255, 255, 255)]
    else:
        bg = degrade_diag(N, [(24, 8, 54), (58, 18, 104), (96, 22, 112)]).convert("RGBA")
        confete = [ROSA, CIANO, AMARELO]
    d = ImageDraw.Draw(bg)
    # confete (fora da área central; pode ir até a borda)
    pts = [(0.12, 0.18, 0.022, 0), (0.86, 0.80, 0.020, 1), (0.10, 0.70, 0.016, 1), (0.30, 0.08, 0.014, 2),
           (0.92, 0.50, 0.015, 2), (0.70, 0.93, 0.016, 0), (0.18, 0.92, 0.013, 2), (0.55, 0.06, 0.012, 1)]
    for x, y, rr, c in pts:
        d.ellipse((x * N - rr * N, y * N - rr * N, x * N + rr * N, y * N + rr * N), fill=confete[c] + (255,))
    # bolhinhas
    for (x, y, rr) in ((0.83, 0.17, 0.075), (0.70, 0.075, 0.035), (0.16, 0.84, 0.045)):
        bg.alpha_composite(bolha_colorida(N, x * N, y * N, rr * N, None))
    # bolha principal
    cx, cy, r = 0.48 * N, 0.53 * N, 0.355 * N
    # sombra suave da bolha
    sh = Image.new("L", (N, N), 0)
    ImageDraw.Draw(sh).ellipse((cx - r, cy - r + 0.02 * N, cx + r, cy + r + 0.02 * N), fill=70)
    sh = sh.filter(ImageFilter.GaussianBlur(0.03 * N))
    sombra = Image.new("RGBA", (N, N), AMEIXA + (0,))
    sombra.putalpha(sh)
    bg.alpha_composite(sombra)
    bg.alpha_composite(bolha_colorida(N, cx, cy, r, None))
    # "2027"
    txt = "2027"
    s = int(N * 0.30)
    while fonte(F_BLACK, s).getbbox(txt, anchor="mm")[2] - fonte(F_BLACK, s).getbbox(txt, anchor="mm")[0] > 1.40 * r:
        s -= 2
    f = fonte(F_BLACK, s)
    ty = cy + 0.03 * N
    contorno = int(s * 0.10)
    txt_sh = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    ImageDraw.Draw(txt_sh).text((cx, ty + 0.018 * N), txt, font=f, fill=AMEIXA + (150,), anchor="mm",
                                stroke_width=contorno, stroke_fill=AMEIXA + (150,))
    bg.alpha_composite(txt_sh.filter(ImageFilter.GaussianBlur(0.012 * N)))
    d = ImageDraw.Draw(bg)
    d.text((cx, ty), txt, font=f, fill=(255, 255, 255, 255), anchor="mm", stroke_width=contorno,
           stroke_fill=AMEIXA + (255,))
    # brilho de 4 pontas amarelo perto do 7
    m = Image.new("L", (N, N), 0)
    brilho(m, cx + 0.58 * r, cy - 0.62 * r, 0.11 * N)
    estrela = Image.new("RGBA", (N, N), AMARELO + (0,))
    estrela.putalpha(m)
    contorno_m = m.filter(ImageFilter.MaxFilter(2 * int(0.008 * N) + 1))
    cont = Image.new("RGBA", (N, N), AMEIXA + (0,))
    cont.putalpha(contorno_m)
    bg.alpha_composite(cont)
    bg.alpha_composite(estrela)
    return bg.convert("RGB")


# ------------------------------------------------------------------ prévia (folha de conferência)
def xadrez(w, h, q=14, c1=(58, 50, 72), c2=(44, 37, 56)):
    img = Image.new("RGB", (w, h), c1)
    d = ImageDraw.Draw(img)
    for y in range(0, h, q):
        for x in range(0, w, q):
            if (x // q + y // q) % 2:
                d.rectangle((x, y, x + q - 1, y + q - 1), fill=c2)
    return img


def tingir(img, cor):
    """Simula o randomizador de cor do template (multiplica o RGB pela cor; alfa igual)."""
    rgb = ImageChops.multiply(img.convert("RGB"), Image.new("RGB", img.size, cor))
    out = rgb.convert("RGBA")
    out.putalpha(img.getchannel("A"))
    return out


def colar(base, img, xy):
    base.alpha_composite(img, (int(xy[0]), int(xy[1])))


def cartao(img, w, h, titulo, sub=None, q=14):
    """Miniatura sobre xadrez escuro + nome do arquivo."""
    c = Image.new("RGBA", (w, h + 46), (0, 0, 0, 0))
    x = xadrez(w, h, q).convert("RGBA")
    im = img if img.size == (w, h) else reduzir(img, (w, h))
    x.alpha_composite(im)
    c.paste(x, (0, 0))
    d = ImageDraw.Draw(c)
    d.text((0, h + 6), titulo, font=fonte(F_BOLD, 17), fill=AMEIXA + (255,))
    if sub:
        d.text((0, h + 27), sub, font=fonte(F_MED, 14), fill=(110, 96, 130, 255))
    return c


def foto_generica(w, h, tipo):
    img = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(img)
    if tipo == "clara":
        for y in range(h):
            t = y / h
            d.line((0, y, w, y), fill=(int(196 + 50 * t), int(226 + 20 * t), 255, 255))
        d.ellipse((w * 0.62, h * 0.06, w * 0.98, h * 0.26), fill=(255, 246, 200, 255))
        d.rectangle((0, h * 0.72, w, h), fill=(236, 236, 242, 255))
    elif tipo == "escura":
        for y in range(h):
            t = y / h
            d.line((0, y, w, y), fill=(int(14 + 20 * t), int(12 + 10 * t), int(34 + 30 * t), 255))
        import random
        rnd = random.Random(7)
        for _ in range(26):
            x, y, r = rnd.uniform(0, w), rnd.uniform(0, h * 0.6), rnd.uniform(10, 36)
            cor = rnd.choice([(255, 180, 80), (120, 160, 255), (255, 110, 170)])
            bk = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            ImageDraw.Draw(bk).ellipse((x - r, y - r, x + r, y + r), fill=cor + (70,))
            img.alpha_composite(bk.filter(ImageFilter.GaussianBlur(4)))
    elif tipo == "listrada":
        img.paste((255, 250, 235, 255), (0, 0, w, h))
        for k in range(-h, w + h, 56):
            d.polygon([(k, 0), (k + 28, 0), (k + 28 - h * 0.6, h), (k - h * 0.6, h)], fill=(255, 200, 70, 255))
    elif tipo == "sala":
        for y in range(h):
            t = y / h
            d.line((0, y, w, y), fill=(int(150 - 60 * t), int(110 - 50 * t), int(170 - 60 * t), 255))
        d.rectangle((w * 0.04, h * 0.46, w * 0.24, h * 0.70), fill=(255, 226, 170, 255))
        d.rectangle((w * 0.135, h * 0.46, w * 0.145, h * 0.70), fill=(150, 110, 170, 255))
        d.rectangle((0, h * 0.74, w, h), fill=(80, 56, 70, 255))
    return img


def silhueta(img, cx, cy, esc, cor):
    d = ImageDraw.Draw(img)
    hw, hh = 92 * esc, 118 * esc
    d.rounded_rectangle((cx - 175 * esc, cy + 140 * esc, cx + 175 * esc, cy + 420 * esc), radius=120 * esc,
                        fill=cor)
    d.rectangle((cx - 40 * esc, cy + 60 * esc, cx + 40 * esc, cy + 160 * esc), fill=cor)
    d.ellipse((cx - hw, cy - hh, cx + hw, cy + hh), fill=cor)


def cantos(img, r):
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, img.size[0] - 1, img.size[1] - 1), radius=r, fill=255)
    out = img.copy()
    out.putalpha(ImageChops.multiply(img.getchannel("A"), m))
    return out


def abrir(rel):
    return Image.open(os.path.join(AQUI, rel)).convert("RGBA")


def bolha_estourada(rotulo, resposta, cor, diam, vazia):
    """Simulação: bolha (anel) + rótulo pequeno em cima + resposta no meio, tudo na mesma cor."""
    out = Image.new("RGBA", (diam, diam), (0, 0, 0, 0))
    b = reduzir(tingir(vazia, cor), (diam, diam))
    b.putalpha(b.getchannel("A").point(lambda v: int(v * 0.55)))
    out.alpha_composite(b)
    cx, cy = diam * 0.47, diam * 0.53
    rw = int(diam * 0.42)
    rot = reduzir(tingir(rotulo, cor), (rw, rw // 2))
    colar(out, rot, (cx - rw / 2, cy - diam * 0.33))
    aw = int(diam * 0.80)
    resp = reduzir(tingir(resposta, cor), (aw, int(aw * resposta.size[1] / resposta.size[0])))
    colar(out, resp, (cx - aw / 2, cy - resp.size[1] / 2 + diam * 0.08))
    return out


def painel(w, h, tipo, conteudo):
    p = foto_generica(w, h, tipo)
    cor_sil = {"clara": (64, 62, 76, 255), "escura": (150, 146, 166, 255), "listrada": (64, 62, 76, 255),
               "sala": (52, 40, 58, 255)}[tipo]
    silhueta(p, w / 2, h * 0.64, w / 520, cor_sil)
    conteudo(p)
    return cantos(p, 26)


def gerar_previa():
    W = 2220
    M = 54
    blocos = []          # (imagem, y)
    y = 40
    folha = Image.new("RGBA", (W, 6000), (246, 243, 250, 255))
    d = ImageDraw.Draw(folha)
    d.text((M, y), "C05 · Meu 2027 vai ser — prévia dos assets", font=fonte(F_BLACK, 52), fill=AMEIXA)
    y += 70
    d.text((M, y), "Fundo xadrez ESCURO = transparente. As artes do efeito são BRANCAS de propósito: o template "
                   "Future Life pinta cada uma com uma cor sorteada.", font=fonte(F_MED, 20), fill=(90, 76, 110))
    y += 28
    d.text((M, y), "Respostas 512×128 mostradas em tamanho real. Todas usam o mesmo tamanho de letra, para o "
                   "sorteio não 'pular'.", font=fonte(F_MED, 20), fill=(90, 76, 110))
    y += 52

    def secao(txt):
        nonlocal y
        d.text((M, y), txt, font=fonte(F_BLACK, 30), fill=AMEIXA)
        y += 46

    # --- título + rótulos
    secao("Título e rótulos das bolhas (entram no efeito)")
    x = M
    c = cartao(abrir("titulo.png"), 640, 320, "titulo.png", "1024×512 · Effect_Title")
    folha.alpha_composite(c, (x, y))
    x += 640 + 30
    for i, b in enumerate(ORDEM_BOLHAS):
        c = cartao(abrir(f"bolha_{b}.png"), 330, 165, f"bolha_{b}.png",
                   "512×256 · Bubble_Titles" + (" · 4ª bolha" if b == "carro" else ""))
        folha.alpha_composite(c, (x + (i % 2) * 360, y + (i // 2) * 220))
    x2 = x + 2 * 360 + 10
    c = cartao(abrir("icone_162.png"), 162, 162, "icone_162.png", "162×162 · envio")
    folha.alpha_composite(c, (x2, y))
    c = cartao(abrir("icone_alt_162.png"), 162, 162, "icone_alt_162.png", "2º ícone (opcional)")
    folha.alpha_composite(c, (x2 + 190, y))
    y += 440

    # --- respostas
    for b in ORDEM_BOLHAS:
        rot = next(t["rotulo"] for t in TEXTOS["bolhas"] if t["id"] == b)
        extra = " — 4ª bolha opcional (ou troca com FUTEBOL)" if b == "carro" else ""
        secao(f"Respostas {rot}: respostas_{b}/{extra}")
        itens = [r for r in TEXTOS["resultados"] if r["bolha"] == b]
        for i, r in enumerate(itens):
            c = cartao(abrir(r["arquivo"]), 512, 128, os.path.basename(r["arquivo"]), r["texto"])
            folha.alpha_composite(c, (M + (i % 4) * (512 + 24), y + (i // 4) * 190))
        y += ((len(itens) + 3) // 4) * 190 + 6
    secao("Reservas: reservas/ (só se alguma frase for vetada; trocar dentro da mesma bolha)")
    for i, r in enumerate(TEXTOS["reservas"]):
        c = cartao(abrir(r["arquivo"]), 512, 128, os.path.basename(r["arquivo"]), r["codigo"] + " · " + r["texto"])
        folha.alpha_composite(c, (M + (i % 4) * (512 + 24), y + (i // 4) * 190))
    y += 2 * 190 + 6

    # --- variantes
    secao("Variantes (pasta variantes/): usar só se o teste no app pedir")
    x = M
    for rel, w_, h_, sub in (
        ("variantes/com_sombra/respostas_futebol/futebol_03.png", 512, 128, "com_sombra · 512×128"),
        ("variantes/quadrado_512/respostas_futebol/futebol_03.png", 200, 200, "quadrado_512 · 512×512"),
        ("variantes/rotulos_sem_icone/bolha_futebol.png", 256, 128, "rotulos_sem_icone · 512×256"),
        ("variantes/bolha_inteira/bolha_inteira_amor.png", 200, 200, "bolha_inteira · 512×512"),
        ("variantes/bolha_inteira/bolha_vazia.png", 200, 200, "bolha_inteira/bolha_vazia"),
    ):
        c = cartao(abrir(rel), w_, h_, os.path.basename(rel), sub)
        folha.alpha_composite(c, (x, y))
        x += w_ + 34
    c = cartao(abrir("variantes/com_sombra/titulo.png"), 360, 180, "titulo.png", "com_sombra")
    folha.alpha_composite(c, (x, y))
    y += 270

    # --- simulação
    secao("Simulação sobre fotos genéricas (cores sorteadas simuladas; a bolha real é a do template)")
    PW, PH = 500, 889
    vazia = abrir("variantes/bolha_inteira/bolha_vazia.png")
    tit = abrir("titulo.png")
    cores3 = [ROSA, AMARELO, CIANO]
    pos3 = [(0.20, 0.37), (0.50, 0.325), (0.80, 0.37)]

    def p1(p):
        colar(p, reduzir(tingir(tit, ROXO), (360, 180)), (PW / 2 - 180, 24))
        for (fx, fy), b, cor in zip(pos3, ORDEM_BOLHAS[:3], cores3):
            im = reduzir(tingir(abrir(f"variantes/bolha_inteira/bolha_inteira_{b}.png"), cor), (160, 160))
            colar(p, im, (fx * PW - 80, fy * PH - 80))

    def p2(p):
        colar(p, reduzir(tingir(tit, (255, 255, 255)), (360, 180)), (PW / 2 - 180, 24))
        escolhas = ["respostas_amor/amor_06.png", "respostas_grana/grana_02.png", "respostas_futebol/futebol_03.png"]
        for (fx, fy), b, cor, rel in zip(pos3, ORDEM_BOLHAS[:3], [ROSA, VERDE_LIMA, CIANO], escolhas):
            im = bolha_estourada(abrir(f"bolha_{b}.png"), abrir(rel), cor, 168, vazia)
            colar(p, im, (fx * PW - 84, fy * PH - 84))

    def p3(p):
        def faixa(caixa, alfa):
            ov = Image.new("RGBA", p.size, (0, 0, 0, 0))
            ImageDraw.Draw(ov).rounded_rectangle(caixa, radius=12, fill=(255, 255, 255, alfa))
            p.alpha_composite(ov)
        faixa((14, 14, PW - 14, 52), 215)
        d3 = ImageDraw.Draw(p)
        d3.text((26, 22), "leitura no pior caso: cor clara + fundo claro", font=fonte(F_BOLD, 18), fill=AMEIXA)
        a = abrir("respostas_grana/grana_06.png")
        bsh = abrir("variantes/com_sombra/respostas_grana/grana_06.png")
        for i, (img, txt) in enumerate(((a, "branco puro (principal), cor amarela"), (bsh, "com_sombra, cor amarela"))):
            yy = 78 + i * 160
            faixa((22, yy - 4, 26 + 11 * len(txt), yy + 24), 215)
            ImageDraw.Draw(p).text((30, yy), txt, font=fonte(F_BOLD, 17), fill=AMEIXA)
            colar(p, reduzir(tingir(img, AMARELO), (440, 110)), (30, yy + 30))
        for i, cor in enumerate([ROSA, CIANO]):
            colar(p, reduzir(tingir(a, cor), (300, 75)), (PW / 2 - 150, 410 + i * 70))

    def p4(p):
        colar(p, reduzir(tingir(tit, AMARELO), (340, 170)), (PW / 2 - 170, 26))
        pos4 = [(0.15, 0.36), (0.385, 0.30), (0.615, 0.30), (0.85, 0.36)]
        esc = ["respostas_amor/amor_04.png", "respostas_grana/grana_06.png",
               "respostas_futebol/futebol_08.png", "respostas_carro/carro_01.png"]
        for (fx, fy), b, cor, rel in zip(pos4, ORDEM_BOLHAS, [ROSA, AMARELO, CIANO, VERDE_LIMA], esc):
            im = bolha_estourada(abrir(f"bolha_{b}.png"), abrir(rel), cor, 128, vazia)
            colar(p, im, (fx * PW - 64, fy * PH - 64))

    paineis = [("clara", p1, "1) antes: título + 3 bolhas (bolha própria)"),
               ("escura", p2, "2) depois do biquinho: respostas"),
               ("listrada", p3, "3) pior caso: a sombra salva a leitura"),
               ("sala", p4, "4) versão 4 bolhas (com CARRO)")]
    for i, (tipo, fn, leg) in enumerate(paineis):
        pimg = painel(PW, PH, tipo, fn)
        xx = M + i * (PW + 22)
        folha.alpha_composite(pimg, (xx, y))
        d.text((xx, y + PH + 10), leg, font=fonte(F_BOLD, 19), fill=AMEIXA)
    y += PH + 60

    # --- ícone
    secao("Ícone como aparece no app (cantos arredondados pelo próprio app): 162, 96 e 64 px + versão grande")
    ic2 = abrir("icone_alt_162.png")
    x = M
    for base, nome in ((abrir("icone_162.png"), "principal"), (ic2, "alternativo")):
        for t in (162, 96, 64):
            im = base if t == 162 else reduzir(base, (t, t))
            im = cantos(im, int(t * 0.22))
            folha.alpha_composite(im, (x, y + (162 - t)))
            if t == 162 and nome == "principal":
                dd = ImageDraw.Draw(folha)
                dd.rectangle((x + 9, y + 9, x + 9 + 143, y + 9 + 143), outline=(40, 120, 255, 255), width=1)
            x += t + 22
        x += 40
    d.text((M, y + 176), "linha azul = área segura 144×144", font=fonte(F_MED, 17), fill=(40, 120, 255))
    folha.alpha_composite(cantos(reduzir(abrir("icone_grande_512.png"), (260, 260)), 56), (x + 20, y))
    d.text((x + 300, y + 120), "icone_grande_512.png (referência)", font=fonte(F_MED, 17), fill=(90, 76, 110))
    y += 260 + 50
    folha = folha.crop((0, 0, W, y))
    folha.convert("RGB").save(os.path.join(AQUI, "previa.png"), optimize=True)
    return folha.size


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--resposta", help="gera também respostas num tamanho sob medida, ex.: 512x256")
    ap.add_argument("--sem-previa", action="store_true")
    a = ap.parse_args()

    glifos = conferir_glifos()
    print("glifos conferidos:", glifos)

    info = gerar_conjunto(AQUI, (512, 128), (512, 256), (1024, 512), False, (16, 8))
    print("principal:", info)
    print("com_sombra:", gerar_conjunto(os.path.join(AQUI, "variantes", "com_sombra"),
                                        (512, 128), (512, 256), (1024, 512), True, (16, 10)))
    print("quadrado_512:", gerar_conjunto(os.path.join(AQUI, "variantes", "quadrado_512"),
                                          (512, 512), (512, 512), (512, 512), False, (56, 150)))
    print("quadrado_512_com_sombra:", gerar_conjunto(os.path.join(AQUI, "variantes", "quadrado_512_com_sombra"),
                                                     (512, 512), (512, 512), (512, 512), True, (56, 150)))
    gerar_extras()
    if a.resposta:
        rw, rh = (int(v) for v in a.resposta.lower().split("x"))
        dest = os.path.join(AQUI, "variantes", f"sob_medida_{rw}x{rh}")
        print("sob medida:", gerar_conjunto(dest, (rw, rh), None, None, False,
                                            (max(12, rw // 32), max(8, rh // 16)), so_respostas=True))

    # ícones
    mestre = icone(1024, "claro")
    salvar(mestre.resize((162, 162), Image.LANCZOS), os.path.join(AQUI, "icone_162.png"))
    salvar(mestre.resize((512, 512), Image.LANCZOS), os.path.join(AQUI, "icone_grande_512.png"))
    alt = icone(1024, "escuro")
    salvar(alt.resize((162, 162), Image.LANCZOS), os.path.join(AQUI, "icone_alt_162.png"))

    if not a.sem_previa:
        print("previa.png:", gerar_previa())

    total = sum(kb for rel, _, kb in REGISTRO if not rel.startswith("variantes") and not rel.startswith("icone")
                and not rel.startswith("reservas"))
    print(f"{len(REGISTRO)} arquivos gerados. Peso das artes que entram no efeito (principal, sem reservas): "
          f"{total:.0f} KB")
    maior = max(REGISTRO, key=lambda t: t[2])
    print(f"maior arquivo: {maior[0]} ({maior[2]:.0f} KB)")


if __name__ == "__main__":
    main()
