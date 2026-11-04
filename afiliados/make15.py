# -*- coding: utf-8 -*-
"""Planner de Natal e Ano Novo — gera PDF imprimível A4 com reportlab."""
import math
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, KeepTogether, NextPageTemplate, CondPageBreak)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("DV", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("DV", normal="DV", bold="DVB", italic="DV", boldItalic="DVB")

RED = colors.HexColor("#b3262e")
GREEN = colors.HexColor("#1f5c45")
GOLD = colors.HexColor("#d9a441")
CREAM = colors.HexColor("#fdf6ea")
MINT = colors.HexColor("#eaf3ee")
ROSE = colors.HexColor("#fbeceb")
LINE = colors.HexColor("#c9c2b6")
DARK = colors.HexColor("#2b2b2b")
GREY = colors.HexColor("#6b6b6b")

PW, PH = A4
LM = RM = 45
TM = 45
BM = 58
W = PW - LM - RM  # 505.27
# A página de autor/copyright será inserida depois como página 2; por isso a numeração
# impressa no rodapé e no sumário já considera essa página (offset de 1).
PAGE_OFFSET = 1

# ---------------------------------------------------------------- estilos
def st(name, **kw):
    base = dict(fontName="DV", fontSize=10, leading=14, textColor=DARK)
    base.update(kw)
    return ParagraphStyle(name, **base)

H = st("H", fontName="DVB", fontSize=19, leading=24, textColor=colors.white)
HSUB = st("HSUB", fontSize=9.5, leading=13, textColor=colors.HexColor("#fff3dc"))
TAG = st("TAG", fontName="DVB", fontSize=8, leading=10, textColor=GOLD)
H2 = st("H2", fontName="DVB", fontSize=12.5, leading=16, textColor=GREEN, spaceBefore=8, spaceAfter=4)
H2R = st("H2R", fontName="DVB", fontSize=12.5, leading=16, textColor=RED, spaceBefore=8, spaceAfter=4)
H3 = st("H3", fontName="DVB", fontSize=10.5, leading=14, textColor=DARK, spaceBefore=4, spaceAfter=2)
P = st("P", fontSize=10, leading=14.2, spaceAfter=5)
PS = st("PS", fontSize=9, leading=12.4, spaceAfter=3)
SMALL = st("SMALL", fontSize=8, leading=10.5, textColor=GREY)
CELL = st("CELL", fontSize=8.8, leading=11.2)
CELLB = st("CELLB", fontName="DVB", fontSize=8.8, leading=11.2)
CELLH = st("CELLH", fontName="DVB", fontSize=8.8, leading=11.2, textColor=colors.white)
CELLC = st("CELLC", fontSize=8.8, leading=11.2, alignment=TA_CENTER)
CELLHC = st("CELLHC", fontName="DVB", fontSize=8.8, leading=11.2, textColor=colors.white, alignment=TA_CENTER)
BUL = st("BUL", fontSize=10, leading=14, leftIndent=12, bulletIndent=0, spaceAfter=3)
BULS = st("BULS", fontSize=9, leading=12.2, leftIndent=10, bulletIndent=0, spaceAfter=2)


def para(t, s=CELL):
    return t if not isinstance(t, str) else Paragraph(t, s)


def bullets(items, s=BUL, color="#b3262e"):
    return [Paragraph(i, s, bulletText="•") for i in items]


# ---------------------------------------------------------------- helpers
def banner(tag, title, sub=None, color=RED):
    rows = [[Paragraph(tag.upper(), TAG)], [Paragraph(title, H)]]
    if sub:
        rows.append([Paragraph(sub, HSUB)])
    t = Table(rows, colWidths=[W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("LEFTPADDING", (0, 0), (-1, -1), 14), ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, 0), 9), ("BOTTOMPADDING", (0, -1), (-1, -1), 10),
        ("TOPPADDING", (0, 1), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, -2), 1),
        ("LINEBELOW", (0, -1), (-1, -1), 3, GOLD),
    ]))
    return [t, Spacer(1, 10)]


def box(content, bg=CREAM, border=GOLD, title=None, width=W):
    inner = []
    if title:
        inner.append(Paragraph(title, H3))
    if isinstance(content, (list, tuple)):
        inner += list(content)
    else:
        inner.append(Paragraph(content, PS))
    t = Table([[inner]], colWidths=[width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg), ("BOX", (0, 0), (-1, -1), 0.8, border),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def checklist(items, width=W, s=PS, pad=3.5):
    rows = [[Paragraph("☐", st("bx", fontSize=11, leading=13, textColor=GREEN)), Paragraph(i, s)] for i in items]
    t = Table(rows, colWidths=[18, width - 18])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 2), ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), pad), ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
    ]))
    return t


def grid(header, rows, widths, head_bg=GREEN, rowh=None, zebra=True, center_cols=(), bold_first=False,
         font=CELL):
    hdr = [Paragraph(h, CELLHC if i in center_cols else CELLH) for i, h in enumerate(header)]
    data = [hdr]
    for r in rows:
        line = []
        for i, c in enumerate(r):
            if isinstance(c, str):
                s = CELLC if i in center_cols else (CELLB if (bold_first and i == 0) else font)
                line.append(Paragraph(c, s))
            else:
                line.append(c)
        data.append(line)
    rh = None
    if rowh:
        rh = [None] + [rowh] * len(rows)
    t = Table(data, colWidths=widths, rowHeights=rh, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), head_bg),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("BOX", (0, 0), (-1, -1), 0.8, head_bg),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]
    if zebra:
        for i in range(1, len(data)):
            if i % 2 == 0:
                style.append(("BACKGROUND", (0, i), (-1, i), CREAM))
    t.setStyle(TableStyle(style))
    return t


def lines(n, h=24, width=W, color=LINE):
    t = Table([[""] for _ in range(n)], colWidths=[width], rowHeights=[h] * n)
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.5, color)]))
    return t


def two_cols(left, right, gap=14):
    cw = (W - gap) / 2
    t = Table([[left, "", right]], colWidths=[cw, gap, cw])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                           ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return t


def recipe(title, yield_, time_, ingredients, steps, tip=None):
    cw = (W - 14) / 2
    ing = [Paragraph("Ingredientes", H3)] + [Paragraph(i, BULS, bulletText="•") for i in ingredients]
    stp = [Paragraph("Modo de preparo", H3)] + [Paragraph(f"{n}. {s}", PS) for n, s in enumerate(steps, 1)]
    head = Table([[Paragraph(title, st("rt", fontName="DVB", fontSize=13, leading=16, textColor=colors.white)),
                   Paragraph(f"Rende: {yield_}<br/>Tempo: {time_}", st("ry", fontSize=8.3, leading=10.5,
                                                                        textColor=colors.white, alignment=TA_RIGHT))]],
                 colWidths=[W * 0.62, W * 0.38])
    head.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), GREEN), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                              ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                              ("LINEBELOW", (0, 0), (-1, -1), 2, GOLD)]))
    body = Table([[ing, "", stp]], colWidths=[cw * 0.85, 14, cw * 1.15])
    body.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                              ("BACKGROUND", (0, 0), (0, 0), CREAM)]))
    out = [head, Spacer(1, 4), body]
    if tip:
        out += [Spacer(1, 3), Paragraph("<b>Dica:</b> " + tip, st("tp", fontSize=8.6, leading=11.5, textColor=GREEN))]
    return KeepTogether(out + [Spacer(1, 12)])


# ---------------------------------------------------------------- páginas (canvas)
def star(c, x, y, r, color):
    c.setFillColor(color)
    p = c.beginPath()
    for i in range(10):
        ang = math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        px, py = x + rr * math.cos(ang), y + rr * math.sin(ang)
        if i == 0:
            p.moveTo(px, py)
        else:
            p.lineTo(px, py)
    p.close()
    c.drawPath(p, fill=1, stroke=0)


def cover(c, doc):
    c.saveState()
    c.setFillColor(RED)
    c.rect(0, 0, PW, PH, fill=1, stroke=0)
    # faixa verde inferior
    c.setFillColor(GREEN)
    c.rect(0, 0, PW, 150, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, 150, PW, 5, fill=1, stroke=0)
    # moldura dourada
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.rect(22, 22, PW - 44, PH - 44, fill=0, stroke=1)
    c.setLineWidth(0.5)
    c.rect(28, 28, PW - 56, PH - 56, fill=0, stroke=1)
    # "neve" / pontos
    import random
    rnd = random.Random(7)
    for _ in range(70):
        x = rnd.uniform(40, PW - 40)
        y = rnd.uniform(170, PH - 40)
        r = rnd.uniform(0.8, 2.4)
        c.setFillColor(colors.Color(1, 1, 1, alpha=rnd.uniform(0.25, 0.6)))
        c.circle(x, y, r, fill=1, stroke=0)
    # árvore estilizada de triângulos
    cx, base = PW / 2, 200
    for i, (wd, hy) in enumerate([(150, 0), (118, 52), (86, 100), (54, 142)]):
        c.setFillColor(GREEN if i % 2 == 0 else colors.HexColor("#2a7558"))
        p = c.beginPath()
        p.moveTo(cx - wd / 2, base + hy)
        p.lineTo(cx + wd / 2, base + hy)
        p.lineTo(cx, base + hy + 78)
        p.close()
        c.drawPath(p, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#7a4a2a"))
    c.rect(cx - 10, base - 18, 20, 18, fill=1, stroke=0)
    star(c, cx, base + 232, 17, GOLD)
    for (dx, dy, col) in [(-40, 20, GOLD), (30, 38, colors.white), (-18, 72, colors.white), (22, 96, GOLD),
                          (-12, 130, GOLD), (8, 160, colors.white), (48, 12, colors.white), (-52, 52, GOLD)]:
        c.setFillColor(col)
        c.circle(cx + dx, base + dy + 8, 4.2, fill=1, stroke=0)
    for (x, y, r) in [(80, 700, 9), (510, 735, 7), (470, 640, 5), (120, 610, 5), (540, 520, 6), (60, 470, 6)]:
        star(c, x, y, r, GOLD)
    # textos inferiores
    c.setFillColor(colors.white)
    c.setFont("DVB", 11)
    c.drawCentredString(PW / 2, 108, "CEIA  •  PRESENTES  •  AMIGO SECRETO  •  RÉVEILLON  •  VIAGEM")
    c.setFont("DV", 10)
    c.setFillColor(colors.HexColor("#f4e3bf"))
    c.drawCentredString(PW / 2, 86, "Kit imprimível em A4 com checklists, tabelas, receitas e cronogramas")
    c.drawCentredString(PW / 2, 70, "Edição para as festas de 2026 e o planejamento de 2027")
    c.restoreState()


def footer(c, doc):
    c.saveState()
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.line(LM, 40, PW - RM, 40)
    c.setFont("DV", 8)
    c.setFillColor(GREY)
    c.drawString(LM, 28, "Planner de Natal e Ano Novo")
    c.setFont("DVB", 8.5)
    c.setFillColor(RED)
    c.drawRightString(PW - RM, 28, str(doc.page + PAGE_OFFSET))
    star(c, PW - RM - 24, 31.5, 4, GOLD)
    c.restoreState()


# ================================================================ CONTEÚDO
s = []

# ---------- Capa (página 1)
CT = st("CT", fontName="DVB", fontSize=36, leading=42, textColor=colors.white, alignment=TA_CENTER)
CS = st("CS", fontSize=14, leading=20, textColor=colors.HexColor("#fbe9c6"), alignment=TA_CENTER)
CK = st("CK", fontName="DVB", fontSize=10, leading=13, textColor=GOLD, alignment=TA_CENTER)
s += [Spacer(1, 50), Paragraph("✦  PLANNER IMPRIMÍVEL  ✦", CK), Spacer(1, 16),
      Paragraph("Planner de Natal<br/>e Ano Novo", CT), Spacer(1, 16),
      Paragraph("Organize as festas sem estresse<br/>e sem estourar o orçamento", CS),
      NextPageTemplate("normal"), PageBreak()]

# ---------- Sumário
sumario = [
    ("1", "Como usar o planner e calendário regressivo de 6 semanas", "4"),
    ("2", "Orçamento das festas e dicas para economizar", "7"),
    ("3", "Lista de presentes, ideias por perfil e presentes feitos em casa", "10"),
    ("4", "Amigo secreto: regras, sorteio sem papelzinho e lista de desejos", "16"),
    ("5", "Ceia de Natal: quantidades, calculadora, receitas, cronograma e compras", "19"),
    ("6", "Réveillon: cardápio leve, festa em casa e viagem de fim de ano", "30"),
    ("7", "Convidados e divisão de tarefas", "35"),
    ("8", "Decoração: checklist e ideias econômicas", "39"),
    ("9", "Encerramento do ano: retrospectiva, metas para 2027 e janeiro", "41"),
    ("10", "Páginas extras: contatos úteis e anotações", "47"),
]
s += banner("Bem-vindo", "Sumário", "Tudo o que você precisa para planejar dezembro em um só lugar")
rows = [[Paragraph(n, st("sn", fontName="DVB", fontSize=16, leading=19, textColor=RED, alignment=TA_CENTER)),
         Paragraph(t, st("stt", fontSize=11, leading=15)),
         Paragraph("p. " + p, st("sp", fontName="DVB", fontSize=10, leading=14, textColor=GREEN, alignment=TA_RIGHT))]
        for n, t, p in sumario]
t = Table(rows, colWidths=[44, W - 104, 60], rowHeights=[42] * len(rows))
t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LINEBELOW", (0, 0), (-1, -1), 0.5, LINE),
                       ("BACKGROUND", (0, 0), (0, -1), CREAM)]))
s += [t, Spacer(1, 16),
      box("Imprima em papel A4, escala 100% (ou “tamanho real”). As páginas de preenchimento podem ser impressas "
          "mais de uma vez. Se preferir reaproveitar, coloque-as em plástico transparente e escreva com caneta "
          "para quadro branco.", title="Antes de imprimir"),
      PageBreak()]

# ================================================================ 1. COMO USAR + CALENDÁRIO
s += banner("Parte 1 • Primeiros passos", "Como usar este planner",
            "Pequenas decisões tomadas cedo evitam correria, filas e compras por impulso em dezembro")
s += [Paragraph("Dezembro costuma juntar tudo ao mesmo tempo: confraternizações, compras, viagens, contas e a "
                "expectativa de uma ceia caprichada. Este planner divide o trabalho em etapas curtas, para que "
                "cada semana tenha poucas tarefas e nada importante fique para a última hora.", P),
      Paragraph("O caminho recomendado", H2)]
passos = [
    ("1. Faça a reunião de planejamento.", "Junte quem mora com você (ou quem vai organizar as festas junto) e "
     "decida: onde será a ceia, quantas pessoas, se haverá amigo secreto e se haverá viagem."),
    ("2. Defina o orçamento antes de comprar.", "Use a tabela da Parte 2. Primeiro o teto total, depois a "
     "divisão por categoria. Tudo o que vier depois precisa caber nesses números."),
    ("3. Monte as listas.", "Presentes, convidados, cardápio e compras. Listas evitam esquecimentos e "
     "idas repetidas ao mercado."),
    ("4. Siga o calendário regressivo.", "Cada semana tem um bloco de tarefas. Marque o que foi feito e "
     "passe adiante o que atrasou — sem acumular tudo para a última semana."),
    ("5. Divida tarefas.", "Festa boa é festa em que o anfitrião também aproveita. Use a folha de divisão de "
     "tarefas da Parte 7."),
    ("6. Feche o ano com calma.", "Na Parte 9 há uma retrospectiva, metas para 2027 e um lembrete das "
     "contas de janeiro, que costumam pesar logo depois das festas."),
]
for a, b in passos:
    s.append(Paragraph(f"<b>{a}</b> {b}", P))
s += [Paragraph("Legenda dos ícones usados nas páginas", H2),
      grid(["Símbolo", "Significado"],
           [["☐", "Caixa para marcar quando a tarefa estiver concluída"],
            ["Previsto / Real", "Quanto você planejou gastar e quanto gastou de fato"],
            ["D-3, D-2, D-1", "Três, dois e um dia antes da ceia"],
            ["Folha de preenchimento", "Página feita para escrever à mão; imprima quantas precisar"]],
           [130, W - 130], center_cols=(0,)),
      Spacer(1, 12),
      box("<b>Datas de referência para 2026:</b> a véspera de Natal (24/12) cai numa quinta-feira e a véspera de "
          "Ano Novo (31/12), também numa quinta-feira. O calendário a seguir começa em 12 de novembro, seis "
          "semanas antes da ceia. Se você começou depois, junte as semanas que já passaram e priorize os itens "
          "com prazo (reservas, viagens e encomendas).", bg=MINT, border=GREEN),
      PageBreak()]

semanas = [
    ("Semana 1 • 12 a 18 de novembro", "Decisões e orçamento", [
        "Reunir a família e decidir onde serão a ceia de Natal e o Réveillon",
        "Definir o número aproximado de convidados (adultos e crianças)",
        "Definir o orçamento total e por categoria (Parte 2)",
        "Decidir se haverá amigo secreto, o valor sugerido e a data do sorteio",
        "Se houver viagem: pesquisar e reservar transporte e hospedagem",
        "Verificar agenda de trabalho, férias e escala de quem vai participar"]),
    ("Semana 2 • 19 a 25 de novembro", "Listas e pesquisa", [
        "Fazer a lista de presentes com valor limite por pessoa",
        "Fazer o sorteio do amigo secreto e pedir as listas de desejos",
        "Rascunhar o cardápio da ceia e do Réveillon",
        "Enviar convites e pedir confirmação até uma data definida",
        "Perguntar sobre restrições alimentares e alergias",
        "Pesquisar preços dos presentes em mais de um lugar antes de comprar"]),
    ("Semana 3 • 26 de novembro a 2 de dezembro", "Compras que não estragam", [
        "Comprar a maior parte dos presentes (evita filas de dezembro)",
        "Separar e testar a decoração do ano anterior (luzes, enfeites)",
        "Comprar itens não perecíveis da ceia: farinha, arroz, enlatados, descartáveis",
        "Conferir louças, taças, travessas, toalhas e cadeiras; pedir emprestado o que faltar",
        "Encomendar carnes especiais, se o açougue trabalhar com reserva",
        "Revisar o carro se houver viagem (pneus, óleo, freios, documentação)"]),
]
semanas2 = [
    ("Semana 4 • 3 a 9 de dezembro", "Casa e decoração", [
        "Montar a árvore e a decoração (Parte 8)",
        "Fazer a faxina mais pesada da casa antes da correria",
        "Comprar o que faltar dos presentes e começar a embrulhar",
        "Liberar espaço na geladeira e no congelador",
        "Fechar o cardápio e dividir pratos com os convidados (Parte 7)"]),
    ("Semana 5 • 10 a 16 de dezembro", "Detalhes e bebidas", [
        "Comprar bebidas, gelo em estoque (se tiver onde guardar) e descartáveis",
        "Terminar de embrulhar e etiquetar os presentes",
        "Revisar a lista de compras por setor (Parte 5)",
        "Confirmar presença dos convidados e atualizar as quantidades",
        "Viagem: organizar quem cuidará de plantas, correspondência e pets"]),
    ("Semana 6 • 17 a 23 de dezembro", "Contagem final", [
        "Descongelar as carnes na geladeira (pernil grande leva de 2 a 3 dias)",
        "Comprar hortifrúti, frios e laticínios (do dia 21 em diante)",
        "Seguir o cronograma D-3, D-2 e D-1 da ceia",
        "Separar roupa, louça e travessas que serão usadas",
        "Deixar dinheiro trocado para gorjetas e caixinhas"]),
    ("24 e 25 de dezembro", "Natal", [
        "Seguir o cronograma do dia 24 hora a hora",
        "Guardar as sobras na geladeira em até 2 horas",
        "Anotar o que deu certo e o que mudar no próximo ano"]),
    ("26 a 31 de dezembro", "Réveillon", [
        "Fazer as compras do Réveillon aproveitando o que sobrou do Natal",
        "Confirmar convidados ou fazer o checklist de viagem (Parte 6)",
        "Reservar um tempo para a retrospectiva do ano e as metas de 2027"]),
]


def week_block(title, sub, items):
    head = Table([[Paragraph(title, st("wt", fontName="DVB", fontSize=10.5, leading=13, textColor=colors.white)),
                   Paragraph(sub, st("ws", fontName="DVB", fontSize=9, leading=12, textColor=GOLD, alignment=TA_RIGHT))]],
                 colWidths=[W * 0.62, W * 0.38])
    head.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), GREEN), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                              ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8)]))
    return KeepTogether([head, checklist(items, pad=3), Spacer(1, 9)])


s += banner("Parte 1 • Calendário regressivo", "Seis semanas até a ceia (1/2)",
            "Marque cada tarefa concluída. O que atrasar passa para a semana seguinte, nunca para a véspera")
for w in semanas:
    s.append(week_block(*w))
s += [Paragraph("Minhas tarefas extras destas semanas", H3), lines(4, 22), PageBreak()]
s += banner("Parte 1 • Calendário regressivo", "Seis semanas até a ceia (2/2)",
            "Da decoração ao Réveillon: as últimas semanas pedem foco em perecíveis e logística")
for w in semanas2:
    s.append(week_block(*w))
s.append(PageBreak())

# ================================================================ 2. ORÇAMENTO
s += banner("Parte 2 • Dinheiro", "Orçamento das festas",
            "Preencha a coluna Previsto antes de comprar e a coluna Real conforme os gastos acontecem", color=GREEN)
s += [Paragraph("Orçamento total disponível para as festas: R$ ______________", P),
      Paragraph("De onde vem o dinheiro (salário, 13º, reserva): ______________________________", P), Spacer(1, 4)]
cats = [
    ("Ceia de Natal", ["Carnes e pratos principais", "Acompanhamentos e saladas", "Sobremesas e panetones",
                       "Bebidas e gelo", "Descartáveis e guardanapos"]),
    ("Réveillon", ["Comidas", "Bebidas e gelo", "Outros"]),
    ("Presentes", ["Família próxima", "Crianças", "Outros presentes"]),
    ("Amigo secreto", ["Presente(s) do sorteio"]),
    ("Decoração", ["Enfeites, luzes e mesa"]),
    ("Roupas", ["Roupas e calçados das festas"]),
    ("Viagem", ["Transporte e pedágios", "Hospedagem", "Alimentação na viagem"]),
    ("Extras", ["Gorjetas, caixinhas e doações", "Imprevistos (reserve uma parte)"]),
]
rows = []
spans = []
r = 1
for cat, subs in cats:
    for i, sub in enumerate(subs):
        rows.append([cat if i == 0 else "", sub, "", "", ""])
    spans.append((r, r + len(subs) - 1))
    r += len(subs)
rows.append(["TOTAL", "", "", "", ""])
bt = grid(["Categoria", "Item", "Previsto (R$)", "Real (R$)", "Diferença (R$)"], rows,
          [92, 178, 78, 78, 79.27], rowh=24, zebra=False, bold_first=True)
extra = [("BACKGROUND", (0, len(rows)), (-1, len(rows)), MINT), ("FONT", (0, len(rows)), (-1, len(rows)), "DVB")]
for a, b in spans:
    extra.append(("SPAN", (0, a), (0, b)))
    extra.append(("BACKGROUND", (0, a), (0, b), CREAM))
    extra.append(("LINEABOVE", (0, a), (-1, a), 0.9, GREEN))
bt.setStyle(TableStyle(extra))
s += [bt, Spacer(1, 8),
      Paragraph("<b>Diferença</b> = Previsto − Real. Valor negativo indica que a categoria passou do limite: compense "
                "reduzindo outra categoria ainda não gasta, em vez de aumentar o total.", SMALL),
      PageBreak()]

s += banner("Parte 2 • Dinheiro", "Controle de gastos dia a dia",
            "Anote cada compra no momento em que ela acontece — inclusive as pequenas", color=GREEN)
s += [grid(["Data", "O que foi comprado", "Categoria", "Forma de pagamento", "Valor (R$)"],
           [["", "", "", "", ""] for _ in range(24)], [50, 190, 85, 100, 80.27], rowh=24),
      Spacer(1, 6),
      Paragraph("Total gasto até agora: R$ __________ &nbsp;&nbsp; Saldo do orçamento: R$ __________", P),
      PageBreak()]

s += banner("Parte 2 • Dinheiro", "Dicas práticas para economizar",
            "Medidas simples que ajudam a manter os gastos sob controle", color=GREEN)
dicas_l = [
    "<b>Decida o teto antes de ver vitrines.</b> Comprar sem limite definido é o caminho mais curto para o excesso.",
    "<b>Compre presentes cedo.</b> Em novembro há mais tempo para comparar preços e menos compra por impulso.",
    "<b>Compare em pelo menos três lugares</b> e considere o frete e o prazo de entrega no preço final.",
    "<b>Evite parcelas que vençam com as contas de janeiro.</b> Some as parcelas ao planejamento de início de ano.",
    "<b>Combine valores com a família.</b> Um amigo secreto para os adultos pode substituir vários presentes.",
    "<b>Ceia colaborativa:</b> cada núcleo familiar leva um prato. Use a folha de divisão de tarefas.",
    "<b>Calcule quantidades.</b> A tabela de quantidades por pessoa ajuda a evitar desperdício.",
]
dicas_r = [
    "<b>Aproveite ingredientes da estação:</b> manga, abacaxi, pêssego, cereja e uva costumam aparecer com mais oferta no fim do ano.",
    "<b>Monte o cardápio do Réveillon com as sobras</b> do Natal (salpicão, farofa, pernil desfiado em sanduíches).",
    "<b>Reaproveite a decoração</b> e invista em uma peça nova por ano, em vez de trocar tudo.",
    "<b>Embrulhe com o que tem em casa:</b> papel kraft, jornal, tecido, barbante e ramos secos.",
    "<b>Leve lista ao mercado e vá alimentado.</b> Fome e pressa aumentam as compras fora da lista.",
    "<b>Prefira marcas próprias e embalagens maiores</b> para itens que serão usados em grande quantidade, quando o preço por quilo ou litro compensar.",
    "<b>Separe uma reserva para imprevistos</b> dentro do orçamento, e não fora dele.",
]
s += [two_cols(bullets(dicas_l, BULS), bullets(dicas_r, BULS)), Spacer(1, 10)]
s += [Paragraph("Comparador de preços", H2),
      grid(["Produto", "Loja 1 (R$)", "Loja 2 (R$)", "Loja 3 (R$)", "Escolhido"],
           [["", "", "", "", "☐"] for _ in range(9)], [175, 80, 80, 80, 90.27], rowh=22, center_cols=(4,)),
      Spacer(1, 8),
      box("Economizar não significa cortar o que importa. Antes de cada compra, pergunte: “isso vai fazer "
          "diferença para quem vai estar na festa?”. Se a resposta for não, provavelmente dá para deixar de fora.",
          bg=MINT, border=GREEN),
      PageBreak()]

# ================================================================ 3. PRESENTES
for pg in (1, 2):
    s += banner("Parte 3 • Presentes", f"Lista de presentes ({pg}/2)",
                "Defina o valor limite antes de sair para comprar e marque o andamento de cada presente")
    s += [grid(["Pessoa", "Ideia de presente", "Valor limite (R$)", "Valor pago (R$)", "Comprado", "Embrulhado"],
               [["", "", "", "", "☐", "☐"] for _ in range(22)], [95, 140, 68, 62, 64, 76.27], rowh=27,
               center_cols=(4, 5), head_bg=RED),
          Spacer(1, 6),
          Paragraph("Subtotal desta página: valor limite R$ __________ &nbsp;&nbsp; valor pago R$ __________", P),
          PageBreak()]

s += banner("Parte 3 • Presentes", "Ideias de presentes por perfil",
            "Sugestões genéricas, sem marcas, organizadas em três faixas de preço que você mesmo define")
s += [box("Defina suas faixas: <b>Faixa 1 (lembrança)</b> até R$ ________ • <b>Faixa 2 (intermediária)</b> "
          "até R$ ________ • <b>Faixa 3 (especial)</b> até R$ ________", bg=ROSE, border=RED), Spacer(1, 8)]
perfis1 = [
    ("Quem gosta de cozinhar", "Pote de temperos caseiros, pano de prato, livro de receitas usado", "Avental, conjunto de utensílios de silicone, tábua de madeira", "Panela de ferro, faca de chef, curso de culinária"),
    ("Leitor(a)", "Marcador de páginas, caderno de anotações, livro de bolso", "Livro novo do gênero preferido, luminária de leitura", "Assinatura de clube de livros, leitor digital"),
    ("Quem pratica esportes", "Garrafa térmica, toalha de microfibra, meias esportivas", "Faixa elástica, corda de pular, bolsa de academia", "Tênis adequado à modalidade, relógio esportivo"),
    ("Bebês e crianças até 5 anos", "Livro de pano ou cartonado, massinha, giz de cera grosso", "Blocos de montar grandes, fantoches, quebra-cabeça simples", "Triciclo ou bicicleta de equilíbrio, cabaninha"),
    ("Crianças de 6 a 11 anos", "Kit de desenho, jogo de cartas, livro ilustrado", "Jogo de tabuleiro, kit de ciências, bola", "Patins com proteção, bicicleta, instrumento musical simples"),
    ("Adolescentes", "Capinha, chaveiro, caderno personalizado", "Fone de ouvido simples, mochila, livro de série", "Vale-experiência (show, curso, passeio), mochila de viagem"),
]
perfis2 = [
    ("Avós e idosos", "Álbum com fotos impressas, carta escrita à mão", "Manta, chinelo confortável, porta-retratos digital", "Dia de passeio com a família, cadeira confortável"),
    ("Quem trabalha em casa", "Planta pequena, caneca, bloco de notas", "Suporte para notebook, organizador de mesa", "Cadeira ergonômica, fone com microfone"),
    ("Amante de plantas", "Muda em vaso reaproveitado, sementes", "Kit de jardinagem, regador, vaso decorativo", "Horta vertical, suporte para vasos"),
    ("Quem gosta de viajar", "Etiqueta de mala, necessaire, travesseiro de pescoço", "Organizadores de mala, carregador portátil", "Mala de bordo, vale-hospedagem"),
    ("Quem tem pet", "Brinquedo de corda, petisco natural, plaquinha de identificação", "Caminha, comedouro elevado, coleira nova", "Casinha, sessão de banho e tosa, kit de passeio completo"),
    ("Quem “já tem tudo”", "Doce caseiro, playlist com bilhete", "Vale-experiência (cinema, jantar)", "Experiência compartilhada: viagem curta, aula, show"),
]
s += [grid(["Perfil", "Faixa 1", "Faixa 2", "Faixa 3"], [list(p) for p in perfis1 + perfis2],
           [100, 135, 135, 135.27], bold_first=True, head_bg=RED), Spacer(1, 10),
      box("Antes de escolher a faixa, pense no que a pessoa realmente usa no dia a dia. Um presente simples e "
          "útil costuma agradar mais do que um item caro que vai ficar guardado. Para crianças, considere também "
          "o espaço disponível em casa e se o brinquedo exige pilhas ou supervisão.", title="Como escolher",
          bg=MINT, border=GREEN), PageBreak()]
s += banner("Parte 3 • Presentes", "Boas práticas e ideias do ano",
            "Cuidados que evitam trocas e frustrações, e espaço para anotar ideias")
s += [Paragraph("Antes de comprar", H2)]
s += bullets([
    "Pergunte tamanhos de roupas e calçados com antecedência, de forma discreta, a alguém próximo da pessoa.",
    "Peça nota ou comprovante de troca e guarde-os junto da lista de presentes.",
    "Para brinquedos, confira a faixa etária indicada na embalagem e se há peças pequenas.",
    "Experiências (passeios, cursos, um dia juntos) ocupam pouco espaço e costumam ser lembradas por muito tempo.",
    "Presentes coletivos (vários familiares juntam o valor) permitem um item melhor sem pesar para ninguém.",
], BULS)
s += [Spacer(1, 6), Paragraph("Ideias que surgiram durante o ano", H2), lines(20, 24), PageBreak()]

s += banner("Parte 3 • Presentes", "Presentes feitos em casa",
            "Opções com carinho, baratas e que podem ser preparadas com antecedência")
caseiros = [
    ("Biscoitos amanteigados em pote de vidro", "Faça biscoitos simples (farinha, manteiga, açúcar e ovo), deixe esfriar bem e guarde em pote limpo e seco, com fita e etiqueta. Duram cerca de 1 semana bem fechados."),
    ("Granola caseira", "Misture 3 xícaras de aveia em flocos, 1/2 xícara de castanhas picadas, 3 colheres de sopa de mel e 2 de óleo. Asse a 160 °C por 20 a 25 minutos, mexendo a cada 8 minutos. Depois de fria, junte uvas-passas."),
    ("Sal de ervas", "Bata no liquidificador 1 xícara de sal grosso com folhas secas de alecrim, tomilho e orégano. Guarde em potinho com etiqueta e sugestões de uso (carnes, legumes, saladas)."),
    ("Kit chocolate quente em pote", "Em camadas: chocolate em pó, açúcar, leite em pó e minimarshmallows. Na etiqueta: “misture 3 colheres em 1 xícara de leite quente”."),
    ("Vale-experiência", "Cartões feitos à mão: “vale um almoço preparado por mim”, “vale uma tarde de jogos”, “vale um passeio no parque”. Combine depois a data."),
    ("Álbum de memórias", "Fotos impressas em álbum simples, com legendas escritas à mão e uma carta no final. Ótimo para avós e padrinhos."),
    ("Muda em vaso reaproveitado", "Plante uma muda de suculenta, temperos ou flores em lata ou pote pintado. Inclua um cartão com os cuidados (sol, rega)."),
    ("Pano de prato pintado", "Pano de prato branco, tinta para tecido e um carimbo feito de batata ou rolha. Deixe secar e fixe conforme a orientação da tinta."),
]
rows = [[Paragraph(f"<b>{a}</b>", CELL), Paragraph(b, CELL)] for a, b in caseiros]
t = Table(rows, colWidths=[140, W - 140])
t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE),
                       ("BACKGROUND", (0, 0), (0, -1), CREAM), ("TOPPADDING", (0, 0), (-1, -1), 6),
                       ("BOTTOMPADDING", (0, 0), (-1, -1), 6), ("LEFTPADDING", (0, 0), (-1, -1), 6),
                       ("BOX", (0, 0), (-1, -1), 0.8, GOLD)]))
s += [t, Spacer(1, 10),
      box("Alimentos caseiros: use potes limpos e bem secos, informe na etiqueta a data de preparo e os principais "
          "ingredientes (atenção a quem tem alergia a castanhas, leite, ovos ou glúten) e evite presentear itens "
          "que precisem de geladeira quando a entrega for demorada.", title="Cuidados", bg=MINT, border=GREEN),
      PageBreak()]

s += banner("Parte 3 • Presentes", "Embrulhos e etiquetas",
            "Planeje o material de embrulho e controle a entrega dos presentes")
s += [Paragraph("Material de embrulho", H2),
      two_cols(checklist(["Papel (kraft, estampado ou reaproveitado)", "Fita adesiva", "Tesoura", "Barbante ou fita de cetim",
                          "Etiquetas ou cartões", "Caneta permanente"], width=(W - 14) / 2),
               checklist(["Sacolas reaproveitadas", "Caixas de tamanhos variados", "Ramos secos ou pinhas para enfeitar",
                          "Papel de seda", "Laços prontos", "Sacos de tecido reutilizáveis"], width=(W - 14) / 2)),
      Spacer(1, 10),
      Paragraph("Controle de entrega", H2),
      grid(["Presente", "Para quem", "Onde está guardado", "Quando entregar", "Entregue"],
           [["", "", "", "", "☐"] for _ in range(14)], [120, 100, 120, 100, 65.27], rowh=25, center_cols=(4,),
           head_bg=RED),
      Spacer(1, 8),
      Paragraph("<b>Dica:</b> escreva o nome na etiqueta antes de embrulhar o próximo presente. Assim nenhum "
                "pacote fica sem identificação.", PS),
      PageBreak()]

# ================================================================ 4. AMIGO SECRETO
s += banner("Parte 4 • Amigo secreto", "Regras e sorteio sem papelzinho",
            "Combine tudo por escrito antes do sorteio para ninguém ter dúvidas no dia", color=GREEN)
s += [Paragraph("Regras que convém combinar", H2)]
s += bullets([
    "<b>Valor sugerido:</b> um valor mínimo e máximo ajuda a manter os presentes equilibrados.",
    "<b>Data, horário e local da troca</b>, e se a revelação será com pistas (“meu amigo secreto é uma pessoa que…”).",
    "<b>Lista de desejos:</b> cada participante indica pelo menos 3 opções, com tamanhos quando for roupa ou calçado.",
    "<b>Prazo para trocas:</b> o presente vai com comprovante de troca, sempre que possível.",
    "<b>Crianças:</b> decida se participam do mesmo sorteio ou se terão um sorteio separado.",
    "<b>Ausências:</b> quem não puder ir no dia deve combinar a entrega do presente com antecedência.",
], BULS)
s += [Paragraph("Três jeitos de sortear sem papelzinho", H2)]
metodos = [
    ("1. Aplicativo ou site de sorteio", "Há ferramentas gratuitas de amigo secreto: o organizador cadastra os nomes e cada pessoa recebe o resultado por mensagem ou e-mail. Ninguém, nem o organizador, precisa ver o resultado."),
    ("2. Corrente embaralhada", "Uma pessoa que não participa (ou um sorteio em planilha) embaralha a lista de nomes. Cada nome tira o seguinte da lista e o último tira o primeiro. Assim, ninguém tira a si mesmo. O organizador envia o resultado individualmente por mensagem."),
    ("3. Números secretos", "O organizador atribui a cada pessoa um número secreto e envia por mensagem. Depois, sorteia uma corrente de números (por exemplo, com um dado ou gerador de números) e informa a cada um apenas o número que tirou. Na revelação, cada pessoa diz seu número."),
]
for a, b in metodos:
    s.append(box([Paragraph(f"<b>{a}</b>", H3), Paragraph(b, PS)], bg=CREAM, border=GOLD))
    s.append(Spacer(1, 6))
s += [box("Para evitar que casais ou pessoas da mesma casa se tirem, na corrente embaralhada basta conferir se "
          "duas pessoas da mesma casa ficaram em sequência (inclusive o último e o primeiro da lista); se ficaram, embaralhe de novo.",
          title="Evitando pares indesejados", bg=MINT, border=GREEN),
      PageBreak()]

s += banner("Parte 4 • Amigo secreto", "Folha de sorteio e organização",
            "Para o organizador acompanhar participantes, listas de desejos e entregas", color=GREEN)
info = Table([[Paragraph("<b>Valor:</b> de R$ ______ a R$ ______", PS), Paragraph("<b>Data da troca:</b> ____/____", PS)],
              [Paragraph("<b>Local:</b> ______________________________", PS), Paragraph("<b>Horário:</b> ______", PS)],
              [Paragraph("<b>Tema (opcional):</b> ________________________", PS), Paragraph("<b>Prazo da lista de desejos:</b> ____/____", PS)]],
             colWidths=[W * 0.55, W * 0.45])
info.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), CREAM), ("BOX", (0, 0), (-1, -1), 0.8, GOLD),
                          ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
s += [info, Spacer(1, 10),
      grid(["Nº", "Participante", "Contato", "Lista enviada", "Presente comprado", "Presente entregue"],
           [[str(i), "", "", "☐", "☐", "☐"] for i in range(1, 21)],
           [28, 150, 120, 65, 70, 72.27], rowh=23.5, center_cols=(0, 3, 4, 5)),
      Spacer(1, 6),
      Paragraph("Use a coluna “Contato” para enviar o resultado do sorteio individualmente. Guarde o resultado em "
                "local que só o organizador acesse, para o caso de alguém esquecer quem tirou.", SMALL),
      PageBreak()]

s += banner("Parte 4 • Amigo secreto", "Lista de desejos para recortar",
            "Imprima, recorte na linha pontilhada e entregue um cartão para cada participante", color=GREEN)


def wish_card():
    cw = (W - 12) / 2
    inner = [Paragraph("✂  MINHA LISTA DE DESEJOS", st("wc", fontName="DVB", fontSize=10, leading=13, textColor=RED)),
             Spacer(1, 4),
             Paragraph("Nome: _________________________________", PS),
             Paragraph("1. ______________________________________", PS),
             Paragraph("2. ______________________________________", PS),
             Paragraph("3. ______________________________________", PS),
             Paragraph("Roupa: _______ Calçado: _______", PS),
             Paragraph("Cores que gosto: _______________________", PS),
             Paragraph("Não gosto de: __________________________", PS)]
    return inner


cards = [[wish_card(), wish_card()] for _ in range(3)]
t = Table(cards, colWidths=[(W) / 2, (W) / 2], rowHeights=[208] * 3)
t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.9, GREY, None, (3, 3)), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                       ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                       ("TOPPADDING", (0, 0), (-1, -1), 12)]))
s += [t, PageBreak()]

# ================================================================ 5. CEIA
s += banner("Parte 5 • Ceia de Natal", "Quantidades por pessoa",
            "Valores típicos de referência para um jantar completo. Ajuste ao apetite do seu grupo")
qt = [
    ["Entradas e petiscos", "100 a 150 g", "50 a 70 g", "Menos se a ceia for logo em seguida"],
    ["Carne principal (uma só, com osso, crua)", "400 a 500 g", "200 a 250 g", "Pernil, peru, costela: o osso pesa"],
    ["Carnes somadas (duas ou mais, cruas)", "300 a 400 g no total", "150 a 200 g", "Divida o total entre as carnes"],
    ["Carne sem osso (crua)", "250 a 300 g", "120 a 150 g", "Lombo, filé, peito de peru"],
    ["Tender ou presunto defumado (pronto)", "100 a 150 g", "50 a 80 g", "Quando há outra carne principal"],
    ["Arroz (cru)", "50 a 60 g", "25 a 30 g", "Arroz à grega rende um pouco mais"],
    ["Farofa (pronta)", "50 a 70 g", "30 g", "Cerca de 40 g de farinha por adulto"],
    ["Salpicão", "100 a 150 g", "60 a 80 g", "Se houver salada de maionese, use o menor valor"],
    ["Salada de maionese", "100 a 150 g", "60 a 80 g", "Idem"],
    ["Folhas e saladas cruas", "40 a 60 g", "20 a 30 g", "Folhas ocupam volume e pesam pouco"],
    ["Sobremesas (somadas)", "150 a 200 g", "100 a 150 g", "Ex.: 1 porção de pavê + 1 rabanada"],
    ["Panetone ou similar", "1 unidade de 500 g para 5 a 6 pessoas", "–", "Considere o café da manhã do dia 25"],
    ["Frutas (uvas, frutas da estação)", "150 a 200 g", "100 g", "Inclua frutas para decorar a mesa"],
    ["Castanhas e frutas secas", "30 a 50 g", "–", "Atenção a alergias"],
    ["Água", "500 ml a 1 litro", "500 ml", "Mais no calor"],
    ["Refrigerante e suco", "600 ml a 1 litro", "500 a 600 ml", "Quem não bebe álcool consome mais"],
    ["Cerveja (quem bebe)", "1 a 1,5 litro", "–", "Para cerca de 5 horas de festa"],
    ["Vinho (quem bebe)", "375 ml (meia garrafa)", "–", "Uma garrafa de 750 ml serve cerca de 5 taças"],
    ["Espumante para o brinde", "150 ml (1 taça)", "–", "1 garrafa de 750 ml para 5 a 6 brindes"],
    ["Gelo (verão)", "1 kg", "1 kg", "Só para bebidas; mais se usar caixas térmicas"],
]
s += [grid(["Item", "Por adulto", "Por criança", "Observação"], qt, [150, 100, 80, 175.27],
           bold_first=True, head_bg=RED),
      Spacer(1, 6),
      Paragraph("Quantidades aproximadas, pensadas para uma ceia com vários pratos. Crianças pequenas costumam comer "
                "cerca de metade da porção de um adulto. Se a festa for longa ou o grupo tiver bom apetite, "
                "acrescente de 10% a 15%.", SMALL),
      PageBreak()]

s += banner("Parte 5 • Ceia de Natal", "Calculadora de quantidades",
            "Multiplique a quantidade por pessoa pelo número de convidados e some adultos e crianças")
s += [box("<b>Exemplo:</b> 10 adultos e 4 crianças, com pernil como carne principal. "
          "Adultos: 10 × 450 g = 4.500 g. Crianças: 4 × 220 g = 880 g. Total = 5.380 g, ou seja, um pernil "
          "(ou dois menores) somando cerca de 5,4 kg cru, com osso.", bg=MINT, border=GREEN),
      Spacer(1, 6),
      Paragraph("Nº de adultos: ______ &nbsp;&nbsp;&nbsp; Nº de crianças: ______", P),
      grid(["Item", "Por adulto", "× adultos", "Por criança", "× crianças", "Total"],
           [[i, "", "", "", "", ""] for i in ["Carne 1:", "Carne 2:", "Arroz (cru)", "Farofa", "Salpicão",
                                               "Salada de maionese", "Outra salada:", "Entradas", "Sobremesa 1:",
                                               "Sobremesa 2:", "Panetone", "Frutas", "Água", "Refrigerante/suco",
                                               "Cerveja", "Vinho", "Espumante", "Gelo", "", ""]],
           [125, 70, 65, 70, 70, 105.27], rowh=24, bold_first=True),
      PageBreak()]

s += banner("Parte 5 • Receitas", "Arroz à grega e farofa de Natal",
            "Receitas clássicas, simples e testadas no formato caseiro", color=GREEN)
s.append(recipe("Arroz à grega", "8 porções", "35 minutos",
                ["2 xícaras (chá) de arroz", "4 xícaras (chá) de água quente", "3 colheres (sopa) de óleo ou manteiga",
                 "1 cebola picada", "2 dentes de alho picados", "1 cenoura em cubinhos",
                 "1/2 pimentão vermelho em cubinhos", "1/2 xícara (chá) de ervilha", "1/2 xícara (chá) de milho",
                 "1/2 xícara (chá) de uvas-passas (opcional)", "Sal e cheiro-verde a gosto"],
                ["Em uma panela, aqueça 1 colher de óleo, refogue metade da cebola e o alho por 2 minutos.",
                 "Junte o arroz, mexa por 1 minuto, acrescente a água quente e sal. Cozinhe tampado em fogo baixo por 15 a 18 minutos, até secar.",
                 "Em uma frigideira, aqueça o restante do óleo ou da manteiga e refogue o resto da cebola, a cenoura e o pimentão por 4 minutos.",
                 "Junte a ervilha e o milho e refogue por mais 2 minutos. Acerte o sal.",
                 "Misture os legumes ao arroz pronto com um garfo, para soltar os grãos. Finalize com passas e cheiro-verde."],
                "o arroz pode ser cozido no D-1 e guardado na geladeira; os legumes são refogados na hora e misturados ao arroz reaquecido."))
s.append(recipe("Farofa de Natal", "10 porções", "25 minutos",
                ["500 g de farinha de mandioca torrada", "100 g de manteiga", "150 g de bacon em cubinhos",
                 "1 cebola picada", "2 ovos (opcional)", "1/2 xícara (chá) de uvas-passas",
                 "1/2 xícara (chá) de azeitonas picadas", "1/2 xícara (chá) de castanhas picadas",
                 "1/2 xícara (chá) de damascos secos picados", "Sal e salsinha a gosto"],
                ["Em uma panela grande, frite o bacon até dourar, sem adicionar óleo.",
                 "Junte a manteiga e a cebola e refogue até a cebola ficar transparente.",
                 "Se usar ovos, quebre-os na panela e mexa até ficarem cozidos e soltos.",
                 "Abaixe o fogo e acrescente a farinha aos poucos, mexendo sempre, por 5 a 8 minutos, até ficar levemente tostada.",
                 "Desligue o fogo, junte passas, azeitonas, castanhas e damascos. Acerte o sal e finalize com salsinha."],
                "a farofa pode ser feita no D-2 ou no D-1 sem as frutas e a salsinha; guarde em pote fechado e acrescente-as na hora de servir."))
s.append(PageBreak())

s += banner("Parte 5 • Receitas", "Salpicão e salada de maionese",
            "Saladas frias: prepare no dia 24 pela manhã e mantenha na geladeira até servir", color=GREEN)
s.append(recipe("Salpicão de frango", "10 porções", "50 minutos + geladeira",
                ["800 g de peito de frango", "1 cebola, 1 folha de louro e sal (para o cozimento)", "2 cenouras raladas",
                 "1 xícara (chá) de milho", "1 maçã em cubinhos", "1/2 xícara (chá) de uvas-passas",
                 "1 talo de salsão picado (opcional)", "1 xícara (chá) de maionese", "1/2 xícara (chá) de creme de leite",
                 "Sal, pimenta-do-reino e cheiro-verde", "Batata palha para servir"],
                ["Cozinhe o frango em água com cebola, louro e sal por 25 a 30 minutos, até ficar macio. Deixe amornar e desfie.",
                 "Coloque a maçã picada em um pouco de água com gotas de limão para não escurecer; escorra antes de usar.",
                 "Em uma tigela, misture o frango, a cenoura, o milho, a maçã, as passas e o salsão.",
                 "Junte a maionese e o creme de leite, tempere com sal e pimenta e misture bem.",
                 "Leve à geladeira por pelo menos 1 hora. Na hora de servir, cubra com batata palha e cheiro-verde."],
                "a batata palha só entra na hora de servir, para não murchar."))
s.append(recipe("Salada de maionese", "10 porções", "40 minutos + geladeira",
                ["1 kg de batatas em cubos médios", "2 cenouras em cubos", "3 ovos cozidos picados",
                 "1/2 xícara (chá) de ervilha", "1 xícara (chá) de maionese", "1 colher (sopa) de suco de limão ou vinagre",
                 "1/2 cebola bem picada (opcional)", "Sal, salsinha e cebolinha a gosto"],
                ["Cozinhe as batatas e as cenouras em água com sal até ficarem macias, mas firmes (cerca de 10 a 12 minutos depois da fervura).",
                 "Escorra e espalhe em uma assadeira para esfriar rápido.",
                 "Em uma tigela, misture a maionese, o limão, a cebola e o sal.",
                 "Junte batatas, cenouras, ovos e ervilha, misturando com cuidado para não desmanchar.",
                 "Finalize com salsinha e cebolinha e mantenha na geladeira até a hora de servir."],
                "prefira maionese industrializada; maionese caseira com ovo cru é mais arriscada no calor."))
s.append(PageBreak())

s += banner("Parte 5 • Receitas", "Pernil assado e tender glaceado",
            "Os pratos principais pedem planejamento: o pernil precisa marinar de um dia para o outro", color=GREEN)
s.append(recipe("Pernil assado", "10 a 12 porções", "3h30 + marinada (12–24 h)",
                ["1 pernil suíno com osso de 4 a 5 kg (descongelado)", "1 xícara (chá) de suco de laranja",
                 "1/2 xícara (chá) de vinho branco ou mais suco de laranja", "Suco de 2 limões", "8 dentes de alho amassados",
                 "1 cebola batida", "3 colheres (sopa) de azeite", "2 folhas de louro e 2 ramos de alecrim",
                 "Sal e pimenta-do-reino a gosto"],
                ["Faça furos profundos no pernil com uma faca. Bata os temperos (exceto louro e alecrim) e espalhe pela carne, inclusive nos furos.",
                 "Coloque em saco próprio ou travessa coberta, com louro e alecrim, e deixe na geladeira de 12 a 24 horas, virando uma vez.",
                 "Preaqueça o forno a 180 °C. Asse coberto com papel-alumínio, com a marinada, por cerca de 3 horas, regando a cada 40 minutos.",
                 "Retire o papel, aumente para 220 °C e asse por mais 30 a 40 minutos, até dourar.",
                 "Confira o ponto: ao espetar o garfo na parte mais grossa, o caldo deve sair claro, sem sinal rosado (com termômetro, cerca de 70 °C no centro). Descanse 15 minutos antes de fatiar."],
                "pernis de tamanhos diferentes pedem tempos diferentes; calcule cerca de 40 minutos de forno por quilo e confira sempre o ponto."))
s.append(recipe("Tender glaceado", "8 a 10 porções", "50 minutos",
                ["1 tender (presunto defumado) de cerca de 1,5 kg", "Cravos-da-índia para espetar",
                 "1/2 xícara (chá) de açúcar mascavo", "1/2 xícara (chá) de suco de laranja", "2 colheres (sopa) de mel",
                 "2 colheres (sopa) de mostarda", "Rodelas de abacaxi ou laranja para decorar (opcional)"],
                ["Retire a embalagem e, se houver, a rede. Faça cortes rasos em losango na superfície e espete um cravo em cada cruzamento.",
                 "Leve ao fogo o açúcar, o suco, o mel e a mostarda e cozinhe por 5 minutos, até engrossar levemente.",
                 "Coloque o tender em uma assadeira, pincele bem a calda e cubra com papel-alumínio.",
                 "Asse a 180 °C por 20 minutos. Retire o papel e asse mais 20 minutos, pincelando a calda a cada 10 minutos.",
                 "Decore com as frutas e sirva quente ou em temperatura ambiente."],
                "o tender já vem cozido; o forno serve para aquecer e caramelizar a calda."))
s.append(PageBreak())

s += banner("Parte 5 • Receitas", "Rabanada e pavê",
            "Sobremesas clássicas que podem ser adiantadas", color=GREEN)
s.append(recipe("Rabanada (frita ou assada)", "20 unidades", "40 minutos",
                ["4 pães franceses amanhecidos (ou 1 pão próprio para rabanada)", "2 xícaras (chá) de leite",
                 "1/2 lata de leite condensado (ou 4 colheres de sopa de açúcar)", "3 ovos batidos",
                 "1 colher (chá) de essência de baunilha (opcional)", "Óleo para fritar (versão frita)",
                 "1/2 xícara (chá) de açúcar e 1 colher (sopa) de canela em pó"],
                ["Corte os pães em fatias de cerca de 2 cm.",
                 "Misture o leite, o leite condensado e a baunilha. Em outro prato, deixe os ovos batidos.",
                 "Passe cada fatia rapidamente no leite e depois nos ovos.",
                 "<b>Frita:</b> frite em óleo quente até dourar dos dois lados e escorra em papel-toalha. <b>Assada:</b> arrume em assadeira untada e asse a 200 °C por 20 a 25 minutos, virando na metade do tempo.",
                 "Ainda mornas, passe as fatias na mistura de açúcar e canela."],
                "a versão assada usa menos óleo e libera o fogão durante a preparação da ceia."))
s.append(recipe("Pavê de chocolate", "12 porções", "40 minutos + 4 h de geladeira",
                ["1 pacote (cerca de 200 g) de biscoito tipo maisena", "1 xícara (chá) de leite para umedecer",
                 "<b>Creme:</b> 1 lata de leite condensado, a mesma medida de leite, 2 gemas, 2 colheres (sopa) de amido de milho e 1 colher (chá) de baunilha",
                 "<b>Cobertura:</b> 200 g de chocolate meio amargo picado e 1 caixa de creme de leite",
                 "Raspas de chocolate para decorar"],
                ["Em uma panela, misture os ingredientes do creme e cozinhe em fogo baixo, mexendo sempre, até engrossar (cerca de 10 minutos). Cubra com filme encostado no creme e deixe amornar.",
                 "Derreta o chocolate em banho-maria ou no micro-ondas em intervalos de 30 segundos e misture o creme de leite.",
                 "Em um refratário, faça camadas: biscoitos umedecidos rapidamente no leite, creme, biscoitos, creme.",
                 "Termine com a cobertura de chocolate e as raspas.",
                 "Leve à geladeira por pelo menos 4 horas antes de servir."],
                "pode ser feito no D-1 e fica ainda melhor de um dia para o outro."))
s.append(PageBreak())

s += banner("Parte 5 • Ceia de Natal", "Cronograma de preparo: D-3, D-2 e D-1",
            "Distribuir o trabalho nos dias anteriores deixa o dia 24 para finalizar, receber e aproveitar")


def phase(title, sub, items, color=GREEN):
    head = Table([[Paragraph(title, st("pt", fontName="DVB", fontSize=11, leading=14, textColor=colors.white)),
                   Paragraph(sub, st("pst", fontSize=8.8, leading=11, textColor=colors.white, alignment=TA_RIGHT))]],
                 colWidths=[W * 0.4, W * 0.6])
    head.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), color), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                              ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8)]))
    return KeepTogether([head, checklist(items, pad=3), Spacer(1, 10)])


s.append(phase("D-3 • 21 de dezembro", "Compras e descongelamento", [
    "Conferir se as carnes congeladas já estão na geladeira descongelando (pernil grande: desde o dia 19 ou 20)",
    "Comprar hortifrúti mais resistente (cebola, alho, batata, cenoura, laranja, limão)",
    "Comprar frios, laticínios e itens que faltaram da lista",
    "Conferir louças, travessas, talheres, taças e toalhas de mesa",
    "Lavar e guardar as taças e travessas que estavam no armário"]))
s.append(phase("D-2 • 22 de dezembro", "Bases, sobremesas e organização", [
    "Preparar o creme e a cobertura do pavê (ou o pavê inteiro, se a geladeira tiver espaço)",
    "Fazer a farofa sem as frutas e a salsinha",
    "Picar e guardar cebola, alho e legumes em potes fechados na geladeira",
    "Liberar espaço na geladeira para as travessas do dia 24",
    "Definir onde ficará a mesa, as bebidas e o lixo da festa"]))
s.append(phase("D-1 • 23 de dezembro", "Marinadas e pré-preparos", [
    "Temperar o pernil e deixar marinando na geladeira (de 12 a 24 horas)",
    "Cozinhar o arroz-base do arroz à grega e o frango do salpicão",
    "Cozinhar ovos, batatas e cenouras da salada de maionese (guardar separados)",
    "Montar o pavê, se ainda não estiver pronto",
    "Comprar pães para a rabanada (pães amanhecidos funcionam melhor)",
    "Arrumar a mesa, se o espaço não for usado antes da ceia",
    "Gelar bebidas e conferir o gelo"]))
s += [Paragraph("Anotações do cronograma", H3), lines(6, 22), PageBreak()]

s += banner("Parte 5 • Ceia de Natal", "Dia 24 hora a hora",
            "Modelo para ceia servida por volta das 22h. Ajuste os horários à sua rotina na coluna “Meu horário”")
horas = [
    ("09h00", "Café da manhã reforçado e revisão do cronograma do dia", ""),
    ("10h00", "Retirar o pernil da geladeira 30 minutos antes de ir ao forno; preaquecer o forno", ""),
    ("11h00", "Pernil no forno, coberto (cerca de 3 horas + 30 a 40 minutos para dourar)", ""),
    ("11h30", "Montar o salpicão e a salada de maionese; levar à geladeira", ""),
    ("13h00", "Almoço leve e pausa", ""),
    ("14h00", "Retirar o papel do pernil, aumentar o forno e dourar (30 a 40 minutos)", ""),
    ("14h45", "Pernil pronto: conferir o ponto, descansar, cobrir; guardar para reaquecer", ""),
    ("15h00", "Preparar a rabanada (assada ou frita)", ""),
    ("16h00", "Arrumar a mesa, o espaço das bebidas e a decoração final", ""),
    ("16h30", "Tender no forno (cerca de 40 minutos pincelando a calda)", ""),
    ("17h30", "Banho e arrumação pessoal", ""),
    ("19h00", "Abastecer gelo e bebidas; montar as entradas", ""),
    ("20h00", "Chegada dos convidados; servir entradas", ""),
    ("21h00", "Refogar os legumes do arroz à grega e reaquecer o arroz", ""),
    ("21h20", "Reaquecer o pernil e o tender no forno; finalizar a farofa com frutas e salsinha", ""),
    ("21h45", "Tirar as saladas da geladeira, colocar a batata palha no salpicão", ""),
    ("22h00", "Ceia servida", ""),
    ("23h30", "Sobremesas, café e panetone", ""),
    ("00h00", "Brinde e troca de presentes", ""),
    ("00h30", "Guardar as sobras na geladeira (até 2 horas depois de servidas)", ""),
]
s += [grid(["Horário", "O que fazer", "Meu horário", "Feito"],
           [[a, b, c, "☐"] for a, b, c in horas], [55, 330, 70, 50.27], rowh=30.5, center_cols=(0, 3),
           head_bg=RED),
      PageBreak()]

s += banner("Parte 5 • Ceia de Natal", "Lista de compras por setor",
            "Base para uma ceia tradicional. Risque o que não vai usar e complete com o seu cardápio")
setores_l = [
    ("Hortifrúti", ["Cebola e alho", "Batata e cenoura", "Pimentão vermelho", "Maçã", "Laranja e limão",
                    "Abacaxi (tender)", "Folhas para salada", "Salsinha e cebolinha", "Uvas e frutas da estação"]),
    ("Açougue e frios", ["Pernil ou outra carne principal", "Tender ou presunto defumado", "Peito de frango (salpicão)",
                         "Bacon em cubos", "Queijos para entradas"]),
    ("Padaria", ["Pães franceses amanhecidos (rabanada)", "Pães e torradas para entradas", "Panetone"]),
]
setores_r = [
    ("Mercearia", ["Arroz", "Farinha de mandioca torrada", "Uvas-passas, damascos, castanhas", "Azeitonas",
                   "Milho e ervilha", "Maionese", "Mostarda e mel", "Açúcar, açúcar mascavo e canela",
                   "Biscoito tipo maisena", "Chocolate meio amargo", "Leite condensado e amido de milho",
                   "Azeite, óleo, sal e temperos secos", "Batata palha"]),
    ("Laticínios e refrigerados", ["Manteiga", "Leite", "Creme de leite", "Ovos"]),
    ("Bebidas", ["Água", "Refrigerantes e sucos", "Cerveja, vinho, espumante", "Gelo"]),
    ("Descartáveis e limpeza", ["Papel-alumínio e filme plástico", "Guardanapos", "Sacos de lixo",
                                "Detergente e esponjas", "Potes para sobras"]),
]


def setores(lst):
    out = []
    for nome, its in lst:
        out.append(Paragraph(nome, st("sx", fontName="DVB", fontSize=10, leading=13, textColor=RED, spaceBefore=4,
                                      spaceAfter=2)))
        out.append(checklist(its, width=(W - 14) / 2, pad=3.2, s=st("cs", fontSize=8.8, leading=11)))
    out.append(Spacer(1, 4))
    return out


left = setores(setores_l) + [Paragraph("Outros", st("sx2", fontName="DVB", fontSize=10, leading=13, textColor=RED, spaceBefore=4)),
                             checklist(["", "", "", "", "", ""], width=(W - 14) / 2, pad=4.5)]
s += [two_cols(left, setores(setores_r)), PageBreak()]

s += banner("Parte 5 • Ceia de Natal", "Minha lista de compras",
            "Folha em branco por setor, para o seu cardápio e para o Réveillon")
blk = lambda nome, n: [Paragraph(nome, st("bk", fontName="DVB", fontSize=10, leading=13, textColor=GREEN, spaceBefore=6, spaceAfter=2)),
                       checklist([""] * n, width=(W - 14) / 2, pad=4.5)]
L = blk("Hortifrúti", 11) + blk("Açougue e frios", 8) + blk("Padaria", 5)
R = blk("Mercearia", 11) + blk("Laticínios e refrigerados", 6) + blk("Bebidas e descartáveis", 7)
s += [two_cols(L, R), Spacer(1, 8), Paragraph("Previsão de gasto: R$ __________ &nbsp;&nbsp; Gasto real: R$ __________", P),
      PageBreak()]

s += banner("Parte 5 • Ceia de Natal", "Segurança dos alimentos no calor",
            "Dezembro no Brasil é quente: comida boa é comida bem conservada", color=GREEN)
s += [Paragraph("A regra das 2 horas", H2),
      Paragraph("Alimentos perecíveis (carnes, maioneses, saladas com creme, frios, laticínios e sobremesas com "
                "creme) não devem ficar mais de <b>2 horas</b> fora da geladeira. Em dias muito quentes (acima de "
                "32 °C), o limite cai para <b>1 hora</b>. Depois disso, o mais seguro é descartar.", P)]
temp = [["Geladeira", "Até 5 °C", "Não lote: o ar frio precisa circular entre os potes"],
        ["Congelador / freezer", "−18 °C ou menos", "Carnes congeladas por longos períodos perdem qualidade"],
        ["Comida quente servida", "Acima de 60 °C", "Mantenha tampada ou no forno baixo até servir"],
        ["Reaquecimento", "74 °C no centro", "Reaqueça só a porção que será consumida"],
        ["Zona de risco", "Entre 5 °C e 60 °C", "Faixa em que as bactérias se multiplicam mais rápido"]]
s += [grid(["Situação", "Temperatura", "Por quê"], temp, [140, 110, 255.27], bold_first=True), Spacer(1, 8),
      Paragraph("Boas práticas", H2)]
s += bullets([
    "<b>Descongele na geladeira</b>, nunca sobre a pia. Um pernil de 4 a 5 kg pode levar de 2 a 3 dias.",
    "<b>Não lave carnes cruas</b> na pia: os respingos espalham bactérias. Seque com papel-toalha se necessário.",
    "<b>Use tábuas e facas separadas</b> para carnes cruas e para alimentos prontos ou saladas.",
    "<b>Sirva saladas frias sobre gelo</b> (uma travessa dentro de outra com gelo) e reponha em pequenas porções.",
    "<b>Evite maionese caseira com ovo cru</b>; prefira a industrializada e mantenha-a refrigerada.",
    "<b>Gelo para bebidas e gelo para alimentos</b> devem ficar separados; gelo de caixa térmica com latas não vai para o copo.",
    "<b>Guarde as sobras</b> em potes rasos e fechados, em até 2 horas. Consuma em até 3 ou 4 dias.",
    "<b>Na dúvida, jogue fora.</b> Cheiro e aparência normais não garantem que o alimento esteja seguro.",
    "<b>Lave as mãos</b> antes de cozinhar e sempre depois de manusear carnes cruas e ovos.",
], BULS)
s += [Spacer(1, 6),
      box("Crianças pequenas, gestantes, idosos e pessoas com a imunidade baixa são mais sensíveis a intoxicações "
          "alimentares. Para elas, sirva as porções logo que os pratos saírem da geladeira ou do forno.",
          title="Atenção redobrada", bg=ROSE, border=RED),
      PageBreak()]

# ================================================================ 6. RÉVEILLON
s += banner("Parte 6 • Réveillon", "Cardápio leve para a virada",
            "Depois da ceia de Natal, um cardápio fresco, fácil de servir e que aproveita sobras")
menu = [
    ("Entradas", "Tábua de frutas, queijos e torradas • Bruschetta de tomate e manjericão • Palitos de legumes com pasta de grão-de-bico"),
    ("Saladas", "Salada de lentilha (tradicional na virada) • Salada verde com manga e castanhas • Salpicão que sobrou do Natal"),
    ("Pratos principais", "Peixe assado com legumes • Frango grelhado com ervas • Pernil desfiado do Natal em sanduíches"),
    ("Acompanhamentos", "Arroz com lentilha e cebola dourada • Batatas ao forno com alecrim"),
    ("Sobremesas", "Salada de frutas • Mousse de maracujá • Uvas, romã e frutas da estação"),
    ("Bebidas", "Água saborizada com frutas e hortelã • Sucos naturais • Ponche sem álcool • Espumante para o brinde"),
]
rows = [[Paragraph(f"<b>{a}</b>", CELL), Paragraph(b, CELL)] for a, b in menu]
t = Table(rows, colWidths=[110, W - 110])
t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE),
                       ("BACKGROUND", (0, 0), (0, -1), ROSE), ("BOX", (0, 0), (-1, -1), 0.8, RED),
                       ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
s += [t, Spacer(1, 10)]
s.append(recipe("Salada de lentilha", "8 porções", "40 minutos",
                ["2 xícaras (chá) de lentilha", "1 cebola roxa picada", "2 tomates sem sementes em cubos",
                 "1/2 pimentão amarelo em cubos", "Suco de 1 limão", "4 colheres (sopa) de azeite",
                 "Sal, pimenta-do-reino e salsinha a gosto"],
                ["Cozinhe a lentilha em água com sal por 15 a 20 minutos, até ficar macia mas inteira. Escorra e deixe esfriar.",
                 "Misture a cebola, o tomate e o pimentão.",
                 "Tempere com limão, azeite, sal e pimenta e finalize com salsinha. Mantenha na geladeira."]))
s.append(recipe("Peixe assado com legumes", "6 porções", "45 minutos",
                ["1 kg de filés de peixe firme", "Suco de 1 limão, 2 dentes de alho, sal e pimenta",
                 "3 batatas em rodelas finas", "1 cebola em rodelas", "2 tomates em rodelas", "1/2 pimentão em tiras",
                 "4 colheres (sopa) de azeite e cheiro-verde"],
                ["Tempere o peixe com limão, alho, sal e pimenta e reserve por 20 minutos na geladeira.",
                 "Em uma assadeira untada, faça uma camada de batatas e por cima cebola, tomate e pimentão.",
                 "Coloque o peixe, regue com azeite, cubra com papel-alumínio e asse a 200 °C por 25 minutos.",
                 "Retire o papel e asse mais 10 minutos. Finalize com cheiro-verde."]))
s.append(PageBreak())

s += banner("Parte 6 • Réveillon", "Checklist da festa em casa",
            "Do convite à arrumação do dia 1º: o essencial para receber bem e sem correria")
fl = [("Planejamento", ["Lista de convidados fechada e confirmada", "Cardápio definido e dividido",
                        "Lista de compras pronta", "Combinado de horário de chegada e de saída",
                        "Avisar os vizinhos, se a festa tiver som"]),
      ("Espaço", ["Lugar para todos sentarem", "Mesa de comida e mesa de bebidas separadas",
                  "Área para crianças, se houver", "Lixeiras visíveis com sacos extras",
                  "Banheiro com papel, sabonete e toalhas de reserva"])]
fr = [("Comida e bebida", ["Gelo suficiente (cerca de 1 kg por pessoa)", "Caixas térmicas ou baldes",
                           "Taças para o brinde", "Água à vontade", "Opções sem álcool atraentes"]),
      ("Virada", ["Contagem regressiva combinada", "Playlist pronta", "Celular carregado para fotos",
                  "Pets em local fechado, silencioso e seguro (fogos assustam)",
                  "Plano de volta para casa dos convidados que beberam"])]


def blocks(lst):
    out = []
    for nome, its in lst:
        out.append(Paragraph(nome, st("fx", fontName="DVB", fontSize=10.5, leading=13, textColor=GREEN, spaceBefore=6, spaceAfter=2)))
        out.append(checklist(its, width=(W - 14) / 2, pad=3))
    return out


s += [two_cols(blocks(fl), blocks(fr)), Spacer(1, 10),
      Paragraph("Dia 1º de janeiro", H2),
      checklist(["Guardar as sobras assim que os convidados saírem (ou até 2 horas depois de servidas)",
                 "Separar recicláveis e retirar o lixo", "Devolver o que foi emprestado (cadeiras, travessas, caixas térmicas)",
                 "Anotar o que funcionou para o próximo ano"]),
      Spacer(1, 8),
      box("Fogos de artifício só devem ser manuseados por adultos, longe de crianças, animais e materiais "
          "inflamáveis, seguindo as instruções da embalagem e as regras da sua cidade. Se possível, prefira "
          "assistir a queimas organizadas.", title="Segurança com fogos", bg=ROSE, border=RED),
      PageBreak()]

s += banner("Parte 6 • Viagem de fim de ano", "Checklist da casa e da mala",
            "Viajar tranquilo começa por deixar a casa segura e a mala bem pensada", color=GREEN)
casa = ["Esvaziar a geladeira de perecíveis e retirar o lixo", "Desligar da tomada aparelhos que não precisam ficar ligados",
        "Fechar o registro de gás", "Fechar o registro de água, se for viajar por muitos dias",
        "Trancar portas e janelas, inclusive basculantes", "Pedir a alguém de confiança para recolher correspondências",
        "Combinar quem regará as plantas", "Deixar uma luz com temporizador, se tiver",
        "Avisar o síndico ou um vizinho de confiança", "Evitar anunciar a viagem em redes sociais enquanto estiver fora"]
mala = ["Documentos de todos (originais ou digitais aceitos)", "Cartões, um pouco de dinheiro e comprovantes de reserva",
        "Remédios de uso contínuo e receitas", "Kit de primeiros socorros básico", "Protetor solar, repelente e chapéu",
        "Carregadores e carregador portátil", "Roupas para calor e um agasalho leve", "Roupa para a virada",
        "Roupa de banho e chinelo", "Itens de higiene pessoal", "Garrafa de água reutilizável", "Lanches para a estrada",
        "Brinquedos e livros para as crianças", "Sacos para roupa suja"]
s += [two_cols([Paragraph("A casa", H2R), checklist(casa, width=(W - 14) / 2, pad=3)],
               [Paragraph("A mala", H2R), checklist(mala, width=(W - 14) / 2, pad=3)]),
      Spacer(1, 10),
      grid(["Item da viagem", "Detalhes"], [["Destino e endereço", ""], ["Data e horário de saída", ""],
                                           ["Data e horário de volta", ""], ["Reserva de hospedagem (código)", ""],
                                           ["Contato da hospedagem", ""]], [170, W - 170], rowh=24, bold_first=True),
      PageBreak()]

s += banner("Parte 6 • Viagem de fim de ano", "Checklist do carro e dos pets",
            "Estradas cheias pedem revisão em dia, paradas planejadas e atenção aos animais", color=GREEN)
carro = ["Revisão feita (óleo, freios, suspensão, luzes)", "Calibrar os pneus, incluindo o estepe",
         "Conferir macaco, chave de roda e triângulo", "Verificar água do radiador e do limpador",
         "Documento do veículo e habilitação válidos", "Planejar a rota, pedágios e postos de parada",
         "Sair cedo e evitar os horários de pico", "Parar para descansar a cada 2 horas, em média",
         "Cadeirinha ou assento de elevação adequado para cada criança", "Bagagem bem presa no porta-malas, sem objetos soltos",
         "Combinar motoristas para revezar em viagens longas", "Não dirigir após consumir bebida alcoólica"]
pets = ["Decidir se o pet viaja ou fica (hotel, cuidador ou vizinho)", "Vacinas em dia e carteira de vacinação",
        "Plaquinha de identificação com telefone na coleira", "Caixa de transporte ou cinto de segurança próprio",
        "Ração, potes, água e petiscos", "Remédios e contato de um veterinário no destino",
        "Tapete higiênico, saquinhos e areia (gatos)", "Nunca deixar o animal sozinho no carro",
        "No Réveillon: lugar fechado e tranquilo, longe do barulho dos fogos",
        "Se ficar com cuidador: deixar instruções escritas e contato do veterinário"]
s += [two_cols([Paragraph("O carro", H2R), checklist(carro, width=(W - 14) / 2, pad=3)],
               [Paragraph("Os pets", H2R), checklist(pets, width=(W - 14) / 2, pad=3)]),
      Spacer(1, 10),
      Paragraph("Paradas planejadas", H2),
      grid(["Parada", "Local / cidade", "Horário previsto", "Observação"],
           [[str(i), "", "", ""] for i in range(1, 6)], [50, 190, 100, 165.27], rowh=24, center_cols=(0,)),
      PageBreak()]

s += banner("Parte 6 • Réveillon", "Planejamento da virada",
            "Resumo da noite de 31 de dezembro, seja em casa, na casa de alguém ou em viagem")
s += [grid(["Item", "Definição"],
           [["Onde vamos passar a virada", ""], ["Quem vai estar", ""], ["Horário de chegada", ""],
            ["O que vamos levar / servir", ""], ["Como vamos chegar e voltar", ""], ["Roupa / cor escolhida", ""],
            ["Orçamento do Réveillon (R$)", ""]], [170, W - 170], rowh=28, bold_first=True, head_bg=RED),
      Spacer(1, 12),
      Paragraph("Desejos para a virada", H2),
      Paragraph("Escreva aqui o que você quer levar para o próximo ano e o que quer deixar para trás.", PS),
      two_cols([Paragraph("Levo para 2027", H3), lines(16, 22, width=(W - 14) / 2)],
               [Paragraph("Deixo em 2026", H3), lines(16, 22, width=(W - 14) / 2)]),
      PageBreak()]

# ================================================================ 7. CONVIDADOS E TAREFAS
for pg in (1, 2):
    s += banner("Parte 7 • Convidados", f"Lista de convidados ({pg}/2)",
                "Anote confirmação, quantas pessoas vêm e restrições alimentares de cada núcleo", color=GREEN)
    s += [Paragraph("Evento: ☐ Natal &nbsp;&nbsp; ☐ Réveillon &nbsp;&nbsp; ☐ Outro: ________________ "
                    "&nbsp;&nbsp; Confirmar até: ____/____", PS), Spacer(1, 4),
          grid(["Nome / família", "Adultos", "Crianças", "Confirmou", "Restrição alimentar", "Vai levar"],
               [["", "", "", "☐", "", ""] for _ in range(21)], [110, 50, 58, 64, 113, 110.27], rowh=27,
               center_cols=(1, 2, 3)),
          Spacer(1, 6),
          Paragraph("Total confirmado: ______ adultos e ______ crianças", P),
          PageBreak()]

s += banner("Parte 7 • Tarefas", "Divisão de tarefas entre família e convidados",
            "Ninguém precisa fazer tudo sozinho: distribua tarefas com prazo e responsável")
tarefas = ["Enviar convites e coletar confirmações", "Organizar o amigo secreto", "Comprar bebidas e gelo",
           "Comprar itens de mercearia", "Comprar hortifrúti e carnes", "Preparar o prato principal",
           "Preparar acompanhamentos", "Preparar saladas", "Preparar sobremesas", "Arrumar e decorar a mesa",
           "Cuidar da música", "Receber os convidados", "Organizar a brincadeira das crianças",
           "Repor bebidas e gelo durante a festa", "Lavar a louça", "Guardar as sobras", "Retirar o lixo",
           "Devolver itens emprestados", "", ""]
s += [grid(["Tarefa", "Responsável", "Prazo", "Feito"], [[x, "", "", "☐"] for x in tarefas],
           [235, 140, 75, 55.27], rowh=26, center_cols=(3,), head_bg=RED),
      PageBreak()]

s += banner("Parte 7 • Convidados", "Restrições alimentares: como adaptar",
            "Pequenas adaptações permitem que todos comam bem na mesma mesa")
restr = [
    ["Vegetariano", "Carnes, frango, peixe, bacon e caldos de carne", "Farofa sem bacon (use castanhas e ovos), arroz à grega, salada de lentilha, legumes assados"],
    ["Vegano", "Tudo de origem animal: carne, ovos, leite, manteiga, mel", "Farofa com azeite, arroz à grega com óleo, saladas sem maionese, frutas"],
    ["Sem glúten (doença celíaca)", "Trigo, cevada, centeio, pão, biscoitos, alguns embutidos", "Arroz, farofa de mandioca, carnes sem molho com farinha; use utensílios separados"],
    ["Sem lactose", "Leite, creme de leite, manteiga, queijos frescos", "Versões sem lactose dos laticínios; pratos com azeite"],
    ["Alergia a castanhas ou amendoim", "Castanhas, nozes, amendoim e farofas com esses itens", "Separe uma porção sem castanhas antes de finalizar e identifique as travessas"],
    ["Alergia a frutos do mar", "Camarão, lagosta, molhos com crustáceos", "Use utensílios separados e avise na mesa"],
    ["Diabetes ou restrição de açúcar", "Doces, refrigerantes, frutas secas em excesso", "Frutas frescas, sobremesas em porções menores, água e bebidas sem açúcar"],
]
s += [grid(["Restrição", "Evitar", "O que oferecer"], restr, [115, 170, 220.27], bold_first=True),
      Spacer(1, 8),
      box("Em caso de alergia, pergunte diretamente à pessoa (ou aos pais, no caso de crianças) quais ingredientes "
          "precisam ser evitados e identifique as travessas com plaquinhas. Contaminação cruzada (mesma colher, "
          "mesma tábua) também conta.", title="Alergias são assunto sério", bg=ROSE, border=RED),
      Spacer(1, 8),
      Paragraph("Restrições do meu grupo", H2),
      grid(["Nome", "Restrição", "Pratos que pode comer / adaptação"], [["", "", ""] for _ in range(9)],
           [130, 130, 245.27], rowh=24),
      PageBreak()]

# ================================================================ 8. DECORAÇÃO
s += banner("Parte 8 • Decoração", "Checklist de decoração",
            "Confira o que já existe antes de comprar e registre o que precisa ser reposto", color=GREEN)
dl = [("Árvore e enfeites", ["Árvore (montada e firme)", "Pisca-pisca testado", "Bolas e enfeites", "Ponteira",
                             "Saia ou base da árvore", "Presépio (se fizer parte da tradição)"]),
      ("Mesa da ceia", ["Toalha e caminho de mesa", "Guardanapos", "Centro de mesa", "Velas (com suporte seguro)",
                        "Pratos, talheres e taças contados", "Travessas e suportes para pratos quentes"])]
dr = [("Casa", ["Guirlanda na porta", "Luzes na janela ou varanda", "Almofadas ou mantas temáticas",
                "Arranjos com ramos e pinhas", "Enfeites no banheiro (toalha, sabonete)"]),
      ("Segurança", ["Luzes com selo de certificação e fios sem emendas", "Não sobrecarregar tomadas e extensões",
                     "Desligar as luzes ao dormir ou sair", "Enfeites pequenos e frágeis fora do alcance de crianças e pets",
                     "Velas longe de cortinas e da árvore"])]
s += [two_cols(blocks(dl), blocks(dr)), Spacer(1, 10),
      Paragraph("Inventário da decoração", H2),
      grid(["Item", "Quantidade", "Estado", "Repor?"], [["", "", "", "☐"] for _ in range(12)],
           [210, 80, 150, 65.27], rowh=24, center_cols=(3,)),
      PageBreak()]

s += banner("Parte 8 • Decoração", "Ideias econômicas e faça você mesmo",
            "Decoração bonita com material reaproveitado e pouco gasto", color=GREEN)
diy = [
    ("Árvore de galhos secos", "Galhos firmes em um vaso ou balde com pedras, decorados com luzes e enfeites leves. Boa para espaços pequenos."),
    ("Pinhas pintadas", "Pinhas recolhidas e limpas, pintadas com tinta branca ou dourada nas pontas. Servem para árvore, mesa e guirlanda."),
    ("Laranjas com cravos", "Espete cravos-da-índia em laranjas formando desenhos. Perfumam o ambiente e enfeitam o centro de mesa."),
    ("Rodelas de laranja secas", "Rodelas finas no forno baixo (cerca de 100 °C) por 2 a 3 horas, virando de vez em quando. Viram enfeites com barbante."),
    ("Potes de vidro iluminados", "Potes reaproveitados com pisca-pisca a pilha dentro. Use apenas luzes de LED, nunca velas acesas em pote fechado."),
    ("Estrelas de papel", "Estrelas dobradas com papel kraft, jornal ou páginas de revista, penduradas com linha na janela ou na árvore."),
    ("Guirlanda de bambolê ou cabide", "Arame do cabide em círculo ou bambolê forrado com ramos, fitas e pinhas."),
    ("Guardanapo em formato de árvore", "Dobre o guardanapo em triângulos sobrepostos sobre o prato e finalize com uma estrelinha de papel."),
    ("Etiquetas recicladas", "Recorte etiquetas de presente de caixas de cereal ou cartões antigos, faça um furo e passe um barbante."),
    ("Centro de mesa com frutas", "Bandeja com uvas, romãs, maçãs vermelhas e ramos verdes. Decora e depois vira sobremesa."),
]
rows = [[Paragraph(f"<b>{a}</b>", CELL), Paragraph(b, CELL)] for a, b in diy]
t = Table(rows, colWidths=[150, W - 150])
t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE),
                       ("BACKGROUND", (0, 0), (0, -1), MINT), ("BOX", (0, 0), (-1, -1), 0.8, GREEN),
                       ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                       ("LEFTPADDING", (0, 0), (-1, -1), 6)]))
s += [t, Spacer(1, 10),
      box("Defina uma paleta de duas ou três cores (por exemplo, vermelho, verde e dourado, ou branco e madeira) e "
          "use-a em tudo: enfeites, mesa e embrulhos. Com uma paleta definida, poucos itens já criam um visual "
          "harmonioso e fica mais fácil resistir a compras por impulso.", title="Uma regra que ajuda", bg=CREAM),
      PageBreak()]

# ================================================================ 9. ENCERRAMENTO DO ANO
s += banner("Parte 9 • Encerramento do ano", "Retrospectiva de 2026 (1/2)",
            "Reserve uma hora tranquila. Responda com sinceridade: ninguém precisa ler além de você")
perguntas1 = ["Quais foram os três momentos mais felizes do meu ano?",
              "Do que eu mais me orgulho de ter feito ou enfrentado?",
              "O que aprendi de mais importante neste ano?",
              "Quais pessoas fizeram diferença na minha vida e eu quero agradecer?"]
for q in perguntas1:
    s += [Paragraph(q, H3), lines(5, 21), Spacer(1, 4)]
s.append(PageBreak())
s += banner("Parte 9 • Encerramento do ano", "Retrospectiva de 2026 (2/2)",
            "Olhe também para o que não saiu como esperado: é daí que nascem as boas metas")
perguntas2 = ["O que não saiu como eu queria? O que estava sob meu controle?",
              "Que hábito quero deixar para trás?",
              "Como cuidei da minha saúde, do meu dinheiro e das minhas relações?",
              "Se eu resumisse 2026 em uma palavra, qual seria? Por quê?"]
for q in perguntas2:
    s += [Paragraph(q, H3), lines(6, 21), Spacer(1, 4)]
s.append(PageBreak())

s += banner("Parte 9 • Metas", "Metas para 2027 por área da vida",
            "Escolha poucas metas, escreva de forma concreta e defina o primeiro passo", color=GREEN)
areas = ["Saúde e bem-estar", "Finanças", "Carreira e estudos", "Família e relacionamentos", "Casa",
         "Lazer e viagens", "Desenvolvimento pessoal", "Comunidade e solidariedade"]
s += [grid(["Área", "Meta para 2027", "Primeiro passo", "Prazo"], [[a, "", "", ""] for a in areas],
           [115, 170, 155, 65.27], rowh=70, bold_first=True),
      Spacer(1, 8),
      Paragraph("Uma meta bem escrita diz <b>o quê</b>, <b>quanto</b> e <b>até quando</b>. Em vez de “ler mais”, "
                "experimente “ler um livro por mês até dezembro”.", PS),
      PageBreak()]

s += banner("Parte 9 • Metas", "Plano de ação trimestral",
            "Transforme as metas em etapas menores, distribuídas ao longo do ano", color=GREEN)
for tri, meses in [("1º trimestre", "janeiro a março"), ("2º trimestre", "abril a junho"),
                   ("3º trimestre", "julho a setembro"), ("4º trimestre", "outubro a dezembro")]:
    s += [Paragraph(f"{tri} <font color='#6b6b6b' size='9'>({meses})</font>", H2),
          grid(["Etapa", "Meta relacionada", "Feito"], [["", "", "☐"] for _ in range(5)],
               [260, 185, 60.27], rowh=21, center_cols=(2,))]
s.append(PageBreak())

s += banner("Parte 9 • Janeiro", "Contas e compromissos de início de ano",
            "Janeiro concentra despesas que chegam logo depois das festas. Anote para não ser pego de surpresa", color=RED)
s += [Paragraph("Confira as datas e as condições no seu estado, prefeitura, escola ou banco. Muitas cobranças "
                "oferecem desconto para pagamento à vista ou opção de parcelamento: vale comparar com calma.", PS),
      Spacer(1, 4)]
contas = ["IPVA (cota única ou parcelas, conforme o calendário do seu estado)", "Licenciamento do veículo",
          "IPTU (carnê da prefeitura)", "Material escolar e uniformes", "Matrícula ou rematrícula escolar",
          "Fatura do cartão com as compras de dezembro", "Parcelas de compras de fim de ano", "Seguros (carro, casa, vida)",
          "Anuidades e assinaturas renovadas", "Reajustes de mensalidades (escola, academia, planos)",
          "Consultas e exames de rotina", "Revisão do carro depois da viagem", "", "", "", ""]
s += [grid(["Conta / compromisso", "Vencimento", "Valor (R$)", "Forma", "Pago"], [[c, "", "", "", "☐"] for c in contas],
           [215, 70, 75, 85, 60.27], rowh=28, center_cols=(4,), head_bg=RED),
      Spacer(1, 6),
      box("Comece a separar, desde já, os comprovantes que costumam ser pedidos na declaração anual de imposto de "
          "renda (despesas médicas, de educação, informes de rendimentos). Uma pasta física ou digital resolve.",
          title="Para não esquecer", bg=MINT, border=GREEN),
      PageBreak()]

# Calendário janeiro 2027 (1/1/2027 = sexta-feira)
s += banner("Parte 9 • Janeiro", "Calendário de janeiro de 2027",
            "Marque vencimentos, volta às aulas, retorno ao trabalho e compromissos", color=RED)
dias = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
start = 5  # sexta
cells = [""] * start + [str(d) for d in range(1, 32)]
while len(cells) % 7:
    cells.append("")
weeks = [cells[i:i + 7] for i in range(0, len(cells), 7)]
dnum = st("dn", fontName="DVB", fontSize=10, leading=12, textColor=GREEN)
data = [[Paragraph(d, CELLHC) for d in dias]] + [[Paragraph(c, dnum) for c in w] for w in weeks]
t = Table(data, colWidths=[W / 7] * 7, rowHeights=[20] + [80] * len(weeks))
t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), RED), ("GRID", (0, 0), (-1, -1), 0.5, LINE),
                       ("BOX", (0, 0), (-1, -1), 0.9, RED), ("VALIGN", (0, 1), (-1, -1), "TOP"),
                       ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),
                       ("BACKGROUND", (0, 1), (0, -1), CREAM), ("BACKGROUND", (6, 1), (6, -1), CREAM)]))
s += [t, Spacer(1, 8), Paragraph("Prioridades do mês", H3), lines(3, 22), PageBreak()]

# ================================================================ 10. EXTRAS
s += banner("Parte 10 • Páginas extras", "Contatos úteis",
            "Tenha à mão os telefones que podem ser necessários durante as festas e as viagens", color=GREEN)
s += [grid(["Serviço", "Telefone"], [["SAMU", "192"], ["Bombeiros", "193"], ["Polícia Militar", "190"],
                                     ["Defesa Civil", "199"]], [200, W - 200], bold_first=True, head_bg=RED),
      Spacer(1, 10)]
contatos = ["Médico ou clínica da família", "Pediatra", "Farmácia de plantão", "Veterinário", "Hotel ou cuidador do pet",
            "Açougue / encomendas", "Padaria / encomendas", "Mercado com entrega", "Gás", "Chaveiro",
            "Eletricista", "Encanador", "Vizinho de confiança", "Síndico / portaria", "Hospedagem da viagem",
            "Seguro do carro / guincho", "Táxi ou transporte", "", ""]
s += [grid(["Contato", "Nome", "Telefone", "Observação"], [[c, "", "", ""] for c in contatos],
           [150, 120, 100, 135.27], rowh=24.5, bold_first=True),
      PageBreak()]

for i in range(1, 4):
    s += banner("Parte 10 • Páginas extras", f"Anotações ({i}/3)", None, color=GREEN if i % 2 else RED)
    s += [lines(27 if i < 3 else 25, 24.3)]
    if i < 3:
        s.append(PageBreak())

s += [Spacer(1, 10),
      Paragraph("Boas festas e um ótimo 2027!", st("end", fontName="DVB", fontSize=12, leading=15, textColor=RED,
                                                    alignment=TA_CENTER))]


# ---------------------------------------------------------------- build
class Doc(BaseDocTemplate):
    pass


doc = Doc("/home/claude/work15/planner-natal-original.pdf", pagesize=A4, leftMargin=LM, rightMargin=RM,
          topMargin=TM, bottomMargin=BM, title="Planner de Natal e Ano Novo",
          subject="Organize as festas sem estresse e sem estourar o orçamento")
frame_c = Frame(LM, 160, W, PH - 160 - 60, id="cover", showBoundary=0)
frame_n = Frame(LM, BM, W, PH - TM - BM, id="normal", showBoundary=0)
doc.addPageTemplates([PageTemplate(id="cover", frames=[frame_c], onPage=cover),
                      PageTemplate(id="normal", frames=[frame_n], onPage=footer)])
doc.build(s)
print("ok")
