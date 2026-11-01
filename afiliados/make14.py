"""Planilha de Orçamento do Casamento (xlsx com fórmulas)."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.chart import PieChart, Reference

ROSE = "B5546E"; LIGHT = "F8E8EC"; GREY = "F3F3F3"
H = Font(bold=True, color="FFFFFF", size=11); HF = PatternFill("solid", fgColor=ROSE)
IN = PatternFill("solid", fgColor="FFF9E6")
thin = Side(style="thin", color="DDDDDD"); B = Border(left=thin, right=thin, top=thin, bottom=thin)
BRL = '"R$" #,##0.00'

wb = Workbook()

def head(ws, row, cols):
    for i, c in enumerate(cols, 1):
        x = ws.cell(row, i, c); x.font = H; x.fill = HF; x.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True); x.border = B
    ws.row_dimensions[row].height = 30

def title(ws, t, sub):
    ws["A1"] = t; ws["A1"].font = Font(bold=True, size=18, color=ROSE)
    ws["A2"] = sub; ws["A2"].font = Font(italic=True, size=10, color="666666")

# 1. Início
ws = wb.active; ws.title = "Início"
title(ws, "Planilha de Orçamento do Casamento", "Autor: Vinicius Marrone · Preencha só as células amarelas. O resto calcula sozinho.")
ws.column_dimensions["A"].width = 34; ws.column_dimensions["B"].width = 26
dados = [("Nome do casal", ""), ("Data do casamento", None), ("Número de convidados (estimado)", 100),
         ("Orçamento total disponível", 45000), ("Quanto já temos guardado", 0), ("Quanto conseguimos guardar por mês", 1000)]
for i, (k, v) in enumerate(dados, 4):
    ws.cell(i, 1, k).font = Font(bold=True)
    c = ws.cell(i, 2, v); c.fill = IN; c.border = B
ws["B5"].number_format = "DD/MM/YYYY"
for r in (7, 8, 9): ws.cell(r, 2).number_format = BRL
ws["A11"] = "RESUMO"; ws["A11"].font = Font(bold=True, size=13, color=ROSE)
res = [("Dias até o casamento", '=IF(B5="","",B5-TODAY())', "0"),
       ("Meses até o casamento", '=IF(B5="","",MAX(0,ROUND((B5-TODAY())/30.4,1)))', "0.0"),
       ("Total previsto (aba Orçamento)", "=Orçamento!D42", BRL),
       ("Total já pago", "=Orçamento!F42", BRL),
       ("Falta pagar", "=B14-B15", BRL),
       ("Sobra ou falta no orçamento", "=B7-B14", BRL),
       ("Custo por convidado", '=IF(B6>0,B14/B6,"")', BRL),
       ("Dinheiro previsto até a data", '=IF(B5="","",B8+B9*MAX(0,(B5-TODAY())/30.4))', BRL),
       ("Situação", '=IF(B5="","Preencha a data",IF(B19>=B16,"No caminho certo","Atenção: o dinheiro previsto não cobre o que falta pagar"))', "@")]
for i, (k, f, fmt) in enumerate(res, 12):
    ws.cell(i, 1, k); c = ws.cell(i, 2, f); c.number_format = fmt; c.border = B; c.fill = PatternFill("solid", fgColor=GREY)
ws.conditional_formatting.add("B17", CellIsRule(operator="lessThan", formula=["0"], font=Font(color="C00000", bold=True)))
ws.conditional_formatting.add("B17", CellIsRule(operator="greaterThanOrEqual", formula=["0"], font=Font(color="2E7D32", bold=True)))
ws["A22"] = "Como usar"; ws["A22"].font = Font(bold=True, size=13, color=ROSE)
passos = ["1. Preencha os dados acima (células amarelas).",
          "2. Na aba Orçamento, ajuste o valor previsto de cada item e marque o que já foi pago.",
          "3. Na aba Fornecedores, anote contatos, orçamentos recebidos e datas de pagamento.",
          "4. Na aba Convidados, liste os convidados e a confirmação de presença.",
          "5. Na aba Pagamentos, registre cada parcela paga com a data.",
          "6. A aba Checklist mostra as tarefas por prazo antes do casamento.",
          "Os valores de exemplo são só sugestões para começar: troque pelos orçamentos reais da sua região."]
for i, p in enumerate(passos, 23): ws.cell(i, 1, p)

# 2. Orçamento
ws = wb.create_sheet("Orçamento")
title(ws, "Orçamento por categoria", "Valores de exemplo são apenas ponto de partida. Troque pelos seus orçamentos.")
head(ws, 4, ["Categoria", "Item", "Prioridade", "Previsto", "Contratado", "Pago", "Falta pagar", "Status"])
for col, w in zip("ABCDEFGH", [20, 34, 12, 15, 15, 15, 15, 14]): ws.column_dimensions[col].width = w
itens = [("Cerimônia", "Local da cerimônia", 1500), ("Cerimônia", "Celebrante / taxas", 600), ("Cerimônia", "Decoração da cerimônia", 1200),
         ("Recepção", "Local da festa", 5000), ("Recepção", "Buffet (comida)", 7000), ("Recepção", "Bebidas", 2500), ("Recepção", "Bolo e doces", 1500),
         ("Recepção", "Decoração e flores", 2500), ("Recepção", "Mobiliário e louças", 800),
         ("Música", "DJ ou banda", 2000), ("Música", "Som e iluminação", 800),
         ("Foto e vídeo", "Fotógrafo", 2500), ("Foto e vídeo", "Filmagem", 2000),
         ("Noiva/Noivo", "Vestido ou traje 1", 2000), ("Noiva/Noivo", "Traje 2", 800), ("Noiva/Noivo", "Cabelo e maquiagem", 600), ("Noiva/Noivo", "Calçados e acessórios", 400),
         ("Noiva/Noivo", "Alianças", 1500),
         ("Papelaria", "Convites", 400), ("Papelaria", "Lembrancinhas", 600),
         ("Documentos", "Cartório (civil)", 500),
         ("Transporte", "Carro dos noivos / convidados", 400),
         ("Lua de mel", "Passagens", 2000), ("Lua de mel", "Hospedagem", 2000),
         ("Outros", "Assessoria / cerimonial", 1500), ("Outros", "Reserva para imprevistos", 1000)]
dv = DataValidation(type="list", formula1='"Alta,Média,Baixa"', allow_blank=True); ws.add_data_validation(dv)
for r in range(5, 42):
    i = r - 5
    if i < len(itens):
        cat, it, v = itens[i]; ws.cell(r, 1, cat); ws.cell(r, 2, it); ws.cell(r, 3, "Alta" if v >= 1500 else "Média"); ws.cell(r, 4, v)
    for c in (1, 2, 3, 4, 5, 6): ws.cell(r, c).fill = IN
    ws.cell(r, 7, f'=IF(D{r}="","",MAX(0,IF(E{r}>0,E{r},D{r})-F{r}))')
    ws.cell(r, 8, f'=IF(B{r}="","",IF(AND(F{r}>0,G{r}=0),"Pago",IF(F{r}>0,"Parcial",IF(E{r}>0,"Contratado","Pesquisando"))))')
    for c in range(1, 9): ws.cell(r, c).border = B
    for c in (4, 5, 6, 7): ws.cell(r, c).number_format = BRL
    dv.add(f"C{r}")
ws.cell(42, 1, "TOTAL").font = Font(bold=True)

ws["D42"] = "=SUM(D5:D41)-SUMPRODUCT((E5:E41>0)*D5:D41)+SUM(E5:E41)"
ws["E42"] = "=SUM(E5:E41)"; ws["F42"] = "=SUM(F5:F41)"; ws["G42"] = "=SUM(G5:G41)"
for c in "DEFG": ws[f"{c}42"].number_format = BRL; ws[f"{c}42"].font = Font(bold=True)
ws["A43"] = "O total usa o valor contratado quando houver; se não, o previsto."; ws["A43"].font = Font(italic=True, size=9, color="666666")
ws.conditional_formatting.add("H5:H41", CellIsRule(operator="equal", formula=['"Pago"'], fill=PatternFill("solid", fgColor="D9F2DD")))
ws.conditional_formatting.add("H5:H41", CellIsRule(operator="equal", formula=['"Parcial"'], fill=PatternFill("solid", fgColor="FFF2CC")))
ws.freeze_panes = "A5"
# resumo por categoria
ws["J4"] = "Categoria"; ws["K4"] = "Total"
for c in ("J4", "K4"): ws[c].font = H; ws[c].fill = HF
cats = ["Cerimônia", "Recepção", "Música", "Foto e vídeo", "Noiva/Noivo", "Papelaria", "Documentos", "Transporte", "Lua de mel", "Outros"]
for i, c in enumerate(cats, 5):
    ws.cell(i, 10, c); ws.cell(i, 11, f'=SUMIF(A$5:A$41,J{i},D$5:D$41)').number_format = BRL
ws.column_dimensions["J"].width = 16; ws.column_dimensions["K"].width = 15
pie = PieChart(); pie.title = "Previsto por categoria"
pie.add_data(Reference(ws, min_col=11, min_row=4, max_row=14), titles_from_data=True)
pie.set_categories(Reference(ws, min_col=10, min_row=5, max_row=14)); pie.height = 9; pie.width = 13
ws.add_chart(pie, "J17")

# 3. Fornecedores
ws = wb.create_sheet("Fornecedores")
title(ws, "Fornecedores e orçamentos", "Compare até 3 orçamentos por serviço antes de fechar.")
head(ws, 4, ["Serviço", "Fornecedor", "Contato", "Orçamento 1", "Orçamento 2", "Orçamento 3", "Menor orçamento", "Escolhido?", "Observações"])
for col, w in zip("ABCDEFGHI", [18, 22, 20, 14, 14, 14, 16, 12, 30]): ws.column_dimensions[col].width = w
dv2 = DataValidation(type="list", formula1='"Sim,Não,Talvez"', allow_blank=True); ws.add_data_validation(dv2)
for r in range(5, 35):
    for c in range(1, 10):
        x = ws.cell(r, c); x.border = B
        if c != 7: x.fill = IN
    ws.cell(r, 7, f'=IF(COUNT(D{r}:F{r})=0,"",MIN(D{r}:F{r}))')
    for c in (4, 5, 6, 7): ws.cell(r, c).number_format = BRL
    dv2.add(f"H{r}")
ws.freeze_panes = "A5"

# 4. Convidados
ws = wb.create_sheet("Convidados")
title(ws, "Lista de convidados", "Marque a confirmação para ver o total de pessoas.")
head(ws, 4, ["Nome", "Lado", "Grupo", "Adultos", "Crianças", "Convite enviado?", "Confirmou?", "Mesa", "Observações"])
for col, w in zip("ABCDEFGHI", [28, 12, 16, 9, 9, 14, 12, 8, 24]): ws.column_dimensions[col].width = w
dvl = DataValidation(type="list", formula1='"Noivo(a) 1,Noivo(a) 2,Ambos"', allow_blank=True)
dvs = DataValidation(type="list", formula1='"Sim,Não"', allow_blank=True)
dvc = DataValidation(type="list", formula1='"Sim,Não,Aguardando"', allow_blank=True)
for d in (dvl, dvs, dvc): ws.add_data_validation(d)
for r in range(5, 255):
    for c in range(1, 10): ws.cell(r, c).border = B; ws.cell(r, c).fill = IN
    dvl.add(f"B{r}"); dvs.add(f"F{r}"); dvc.add(f"G{r}")
ws["K4"] = "Resumo"; ws["K4"].font = Font(bold=True, color=ROSE, size=12)
for i, (k, f) in enumerate([("Convites na lista", '=COUNTA(A5:A254)'), ("Pessoas convidadas", "=SUM(D5:E254)"),
                            ("Pessoas confirmadas", '=SUMIF(G5:G254,"Sim",D5:D254)+SUMIF(G5:G254,"Sim",E5:E254)'),
                            ("Aguardando resposta", '=COUNTIF(G5:G254,"Aguardando")+COUNTBLANK(G5:G254)-COUNTBLANK(A5:A254)'),
                            ("Não vão", '=COUNTIF(G5:G254,"Não")')], 5):
    ws.cell(i, 11, k); ws.cell(i, 12, f).font = Font(bold=True)
ws.column_dimensions["K"].width = 22
ws.freeze_panes = "A5"

# 5. Pagamentos
ws = wb.create_sheet("Pagamentos")
title(ws, "Controle de pagamentos e parcelas", "Registre cada pagamento. Some com a coluna Pago da aba Orçamento.")
head(ws, 4, ["Data de vencimento", "Fornecedor / item", "Valor", "Forma de pagamento", "Pago?", "Data do pagamento", "Situação"])
for col, w in zip("ABCDEFG", [16, 30, 14, 18, 9, 16, 14]): ws.column_dimensions[col].width = w
dvp = DataValidation(type="list", formula1='"Sim,Não"', allow_blank=True); ws.add_data_validation(dvp)
dvf = DataValidation(type="list", formula1='"Pix,Boleto,Cartão,Dinheiro,Transferência"', allow_blank=True); ws.add_data_validation(dvf)
for r in range(5, 85):
    for c in range(1, 8):
        ws.cell(r, c).border = B
        if c < 7: ws.cell(r, c).fill = IN
    ws.cell(r, 1).number_format = "DD/MM/YYYY"; ws.cell(r, 6).number_format = "DD/MM/YYYY"; ws.cell(r, 3).number_format = BRL
    ws.cell(r, 7, f'=IF(A{r}="","",IF(E{r}="Sim","Pago",IF(A{r}<TODAY(),"Atrasado",IF(A{r}-TODAY()<=7,"Vence em breve","A vencer"))))')
    dvp.add(f"E{r}"); dvf.add(f"D{r}")
ws.conditional_formatting.add("G5:G84", CellIsRule(operator="equal", formula=['"Atrasado"'], fill=PatternFill("solid", fgColor="F8D7DA")))
ws.conditional_formatting.add("G5:G84", CellIsRule(operator="equal", formula=['"Vence em breve"'], fill=PatternFill("solid", fgColor="FFF2CC")))
ws.conditional_formatting.add("G5:G84", CellIsRule(operator="equal", formula=['"Pago"'], fill=PatternFill("solid", fgColor="D9F2DD")))
ws["I4"] = "Total pago"; ws["J4"] = '=SUMIF(E5:E84,"Sim",C5:C84)'
ws["I5"] = "Total a pagar"; ws["J5"] = '=SUMIF(E5:E84,"<>Sim",C5:C84)'
for c in ("J4", "J5"): ws[c].number_format = BRL; ws[c].font = Font(bold=True)
ws.column_dimensions["I"].width = 14; ws.column_dimensions["J"].width = 15
ws.freeze_panes = "A5"

# 6. Checklist
ws = wb.create_sheet("Checklist")
title(ws, "Checklist por prazo", "A coluna Prazo calcula a data a partir da data do casamento (aba Início).")
head(ws, 4, ["Quando", "Tarefa", "Prazo", "Feito?"])
for col, w in zip("ABCD", [18, 52, 14, 9]): ws.column_dimensions[col].width = w
tarefas = [(365, "12 meses antes", ["Definir orçamento total e estilo da festa", "Fazer a lista prévia de convidados", "Pesquisar e reservar local da cerimônia e da festa", "Escolher a data"]),
           (270, "9 meses antes", ["Contratar buffet", "Contratar fotógrafo e filmagem", "Contratar DJ ou banda", "Contratar assessoria, se for usar"]),
           (180, "6 meses antes", ["Escolher vestido / trajes", "Contratar decoração e flores", "Planejar a lua de mel", "Enviar save the date"]),
           (120, "4 meses antes", ["Encomendar convites", "Comprar alianças", "Contratar bolo e doces", "Dar entrada na documentação do cartório"]),
           (60, "2 meses antes", ["Enviar convites", "Definir cardápio e bebidas", "Fazer prova de cabelo e maquiagem", "Comprar lembrancinhas"]),
           (30, "1 mês antes", ["Confirmar presenças", "Montar mapa de mesas", "Fazer a última prova do traje", "Confirmar horários com todos os fornecedores"]),
           (7, "1 semana antes", ["Passar números finais ao buffet", "Separar pagamentos finais", "Preparar a mala da lua de mel", "Descansar"])]
dvk = DataValidation(type="list", formula1='"Sim,Não"', allow_blank=True); ws.add_data_validation(dvk)
r = 5
for dias, quando, ts in tarefas:
    for t in ts:
        ws.cell(r, 1, quando); ws.cell(r, 2, t)
        c = ws.cell(r, 3, f'=IF(Início!$B$5="","",Início!$B$5-{dias})'); c.number_format = "DD/MM/YYYY"
        ws.cell(r, 4).fill = IN; dvk.add(f"D{r}")
        for cc in range(1, 5): ws.cell(r, cc).border = B
        r += 1
ws.conditional_formatting.add(f"A5:D{r-1}", FormulaRule(formula=['$D5="Sim"'], fill=PatternFill("solid", fgColor="D9F2DD")))
ws.conditional_formatting.add(f"A5:D{r-1}", FormulaRule(formula=['AND($D5<>"Sim",$C5<>"",$C5<TODAY())'], fill=PatternFill("solid", fgColor="F8D7DA")))
ws.cell(r + 1, 1, "Concluídas:"); ws.cell(r + 1, 2, f'=COUNTIF(D5:D{r-1},"Sim")&" de "&COUNTA(B5:B{r-1})').font = Font(bold=True)

for s in wb.worksheets:
    s.sheet_view.showGridLines = False
wb.save("/tmp/claude-0/-home-claude/f004c82e-06d5-5323-b435-46473cd83ab1/scratchpad/p14/planilha-orcamento-casamento.xlsx")
print("ok")
