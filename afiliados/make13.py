from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("DV", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
GREEN = colors.HexColor("#2f7d6b")
LIGHT = colors.HexColor("#e8f3f0")

T = ParagraphStyle("T", fontName="DVB", fontSize=26, leading=32, textColor=GREEN, spaceAfter=10)
H = ParagraphStyle("H", fontName="DVB", fontSize=17, leading=22, textColor=GREEN, spaceAfter=8)
H2 = ParagraphStyle("H2", fontName="DVB", fontSize=12, leading=16, spaceBefore=10, spaceAfter=4)
P = ParagraphStyle("P", fontName="DV", fontSize=10.5, leading=15, spaceAfter=5)
S = ParagraphStyle("S", fontName="DV", fontSize=9, leading=12, textColor=colors.grey)

def checklist(items, title=None):
    rows = [["☐", Paragraph(i, P)] for i in items]
    t = Table(rows, colWidths=[22, 460])
    t.setStyle(TableStyle([("FONT", (0, 0), (0, -1), "DV", 13), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LINEBELOW", (0, 0), (-1, -1), 0.3, colors.lightgrey),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return t

def grid(header, rows, widths):
    data = [header] + rows
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "DV", 9), ("FONT", (0, 0), (-1, 0), "DVB", 9),
                           ("BACKGROUND", (0, 0), (-1, 0), LIGHT), ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 7),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    return t

s = []
s += [Spacer(1, 120), Paragraph("Kit Organização da Casa", T),
      Paragraph("Rotina de limpeza em 15 minutos por dia — checklists, planners e tabelas para imprimir", P),
      Spacer(1, 10), Paragraph("Autor: Vinicius Marrone", H2),
      Spacer(1, 20),
      Paragraph("Como imprimir: tamanho A4, escala 100%. Se quiser reutilizar, imprima e coloque em uma pasta plástica ou capa transparente, e use caneta para quadro branco.", S),
      PageBreak()]

s += [Paragraph("Por onde começar", H),
      Paragraph("Casa organizada não depende de faxinas gigantes: depende de pequenas tarefas repetidas no mesmo dia. "
                "Este kit divide a limpeza em três ritmos: <b>diário</b> (15 minutos), <b>semanal</b> (um foco por dia) e <b>mensal</b> (itens que ninguém lembra).", P),
      Paragraph("Passo a passo para usar", H2),
      Paragraph("1. Imprima as páginas de checklist diário, semanal e mensal.", P),
      Paragraph("2. Preencha a tabela de divisão de tarefas com quem mora na casa.", P),
      Paragraph("3. Escolha um horário fixo para os 15 minutos diários (por exemplo, logo depois do jantar).", P),
      Paragraph("4. Marque cada tarefa feita. Se um dia falhar, não tente compensar: retome no dia seguinte.", P),
      Paragraph("Regra dos 2 minutos", H2),
      Paragraph("Se uma tarefa leva menos de 2 minutos (guardar um copo, jogar uma embalagem fora, pendurar uma toalha), faça na hora. Isso evita acúmulo.", P),
      Paragraph("Material básico de limpeza", H2),
      checklist(["Detergente neutro", "Desinfetante ou álcool 70%", "Água sanitária (nunca misturar com outros produtos)",
                 "Desengordurante para cozinha", "Esponjas e panos de microfibra", "Rodo, vassoura e pá",
                 "Balde e luvas", "Sacos de lixo"]),
      PageBreak()]

s += [Paragraph("Rotina diária de 15 minutos", H),
      Paragraph("Faça na ordem. Use um cronômetro: quando acabar o tempo, pare.", P),
      Paragraph("Manhã (5 minutos)", H2),
      checklist(["Arrumar a cama", "Abrir janelas para ventilar", "Guardar o que ficou fora do lugar na sala", "Passar pano no pia do banheiro"]),
      Paragraph("Tarde / noite (10 minutos)", H2),
      checklist(["Lavar a louça ou colocar na máquina", "Limpar fogão e bancada da cozinha", "Varrer cozinha e sala (só o essencial)",
                 "Tirar o lixo", "Deixar a roupa suja no cesto", "Separar roupa do dia seguinte"]),
      Spacer(1, 10),
      Paragraph("Acompanhamento da semana", H2),
      grid(["Tarefa", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"],
           [[t, "", "", "", "", "", "", ""] for t in ["Cama arrumada", "Louça feita", "Bancada limpa", "Lixo retirado", "Chão varrido"]],
           [150, 45, 45, 45, 45, 45, 45, 45]),
      PageBreak()]

dias = [("Segunda — Banheiro", ["Lavar o vaso e a pia", "Limpar box e azulejos", "Trocar toalhas", "Lavar tapete do banheiro", "Repor papel e sabonete"]),
        ("Terça — Cozinha", ["Limpar por fora a geladeira e o micro-ondas", "Desengordurar fogão e coifa", "Lavar a lixeira", "Conferir validade dos alimentos", "Limpar pia e ralo"]),
        ("Quarta — Quartos", ["Trocar roupa de cama", "Tirar o pó de móveis", "Passar aspirador ou vassoura", "Organizar guarda-roupa por 5 minutos", "Arejar colchão"]),
        ("Quinta — Sala", ["Tirar o pó de estantes e TV", "Passar aspirador no sofá", "Lavar capas de almofada, se tiver", "Passar pano no chão", "Organizar controles e revistas"]),
        ("Sexta — Roupas", ["Lavar roupas acumuladas", "Passar o essencial", "Guardar roupas limpas", "Limpar filtro da máquina, se tiver", "Separar doações"]),
        ("Sábado — Área externa", ["Varrer varanda ou quintal", "Lavar capacho", "Regar plantas", "Separar recicláveis", "Limpar tampa da lixeira externa"]),
        ("Domingo — Descanso e planejamento", ["Planejar refeições da semana", "Fazer lista de compras", "Ver compromissos da semana", "Ler a tabela de tarefas", "Descansar"])]
s += [Paragraph("Rotina semanal: um foco por dia", H),
      Paragraph("Cada dia tem um cômodo ou assunto principal. Some isso aos 15 minutos diários.", P)]
for i, (d, it) in enumerate(dias):
    s += [Paragraph(d, H2), checklist(it)]
    if i == 3:
        s.append(PageBreak())
s.append(PageBreak())

s += [Paragraph("Checklist mensal", H),
      Paragraph("Tarefas que parecem pequenas, mas fazem diferença quando ficam esquecidas.", P),
      checklist(["Limpar o interior da geladeira e do congelador", "Limpar o forno e o micro-ondas por dentro", "Lavar cortinas ou limpá-las com pano úmido",
                 "Limpar ventiladores e saídas de ar", "Virar ou rodar o colchão (se o modelo permitir)", "Limpar atrás e embaixo dos móveis leves",
                 "Lavar lixeiras e cestos", "Limpar vidros e janelas", "Lavar tapetes", "Conferir produtos de limpeza e repor o que acabou",
                 "Revisar documentos e contas (rápido)", "Separar itens para doação"]),
      Spacer(1, 10),
      Paragraph("Checklist de faxina pesada (a cada 3 ou 6 meses)", H2),
      checklist(["Lavar sofá e estofados (conforme a etiqueta)", "Limpar o topo dos armários", "Limpar rodapés e interruptores", "Esvaziar e limpar armários da cozinha",
                 "Limpar a máquina de lavar por dentro", "Revisar a despensa e descartar itens vencidos"]),
      PageBreak()]

s += [Paragraph("Divisão de tarefas da casa", H),
      Paragraph("Preencha com quem mora com você. Troque as tarefas a cada mês para ficar justo.", P),
      grid(["Tarefa", "Responsável", "Dias", "Feito?"],
           [[t, "", "", "☐"] for t in ["Louça", "Lixo", "Banheiro", "Cozinha", "Roupas", "Compras", "Quarto", "Sala", "Pets / plantas", "Outra:"]],
           [190, 120, 110, 60]),
      Spacer(1, 14),
      Paragraph("Planner de limpeza por cômodo", H2),
      grid(["Cômodo", "Tarefa", "Frequência", "Última vez"],
           [["", "", "", ""] for _ in range(10)], [100, 190, 100, 90]),
      PageBreak()]

s += [Paragraph("Organização de armários e gavetas em 5 passos", H),
      Paragraph("1. <b>Tire tudo</b> de dentro e limpe o espaço vazio.", P),
      Paragraph("2. <b>Separe</b> em três montes: ficar, doar, descartar.", P),
      Paragraph("3. <b>Agrupe</b> por tipo (por exemplo, camisetas com camisetas).", P),
      Paragraph("4. <b>Guarde</b> o que usa mais ao alcance da mão e o que usa menos no alto.", P),
      Paragraph("5. <b>Etiquete</b> caixas e prateleiras para manter o hábito.", P),
      Spacer(1, 10),
      Paragraph("Meta de organização por semana", H2),
      grid(["Semana", "Local para organizar", "Feito"], [["1", "", "☐"], ["2", "", "☐"], ["3", "", "☐"], ["4", "", "☐"]], [60, 330, 60]),
      Spacer(1, 12),
      Paragraph("Lista de compras de limpeza", H2),
      checklist(["", "", "", "", "", ""]),
      PageBreak()]

s += [Paragraph("Dicas rápidas de segurança", H),
      Paragraph("• Nunca misture água sanitária com outros produtos de limpeza.", P),
      Paragraph("• Use luvas e mantenha o ambiente ventilado ao usar produtos fortes.", P),
      Paragraph("• Guarde produtos de limpeza longe de crianças e animais.", P),
      Paragraph("• Leia o rótulo de cada produto antes de usar.", P),
      Spacer(1, 12),
      Paragraph("Uso do material", H2),
      Paragraph("Autoria: Vinicius Marrone. Este material é de uso pessoal. Não é permitido revender ou redistribuir os arquivos. Este kit traz orientações gerais de organização e não substitui recomendações do fabricante de cada produto.", P)]

SimpleDocTemplate("/tmp/claude-0/-home-claude/f004c82e-06d5-5323-b435-46473cd83ab1/scratchpad/p13/kit-organizacao-da-casa.pdf", pagesize=A4,
                  leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50, title="Kit Organização da Casa").build(s)
print("ok")
