"""Gera o 'Manual de Instruções e Autoria' em PDF exigido pela Hotmart (Código Fonte)."""
import sys
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("DV", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

out, titulo, zipname, itens, passos = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
h = ParagraphStyle("h", fontName="DVB", fontSize=18, leading=24, spaceAfter=12)
h2 = ParagraphStyle("h2", fontName="DVB", fontSize=13, leading=18, spaceBefore=12, spaceAfter=6)
p = ParagraphStyle("p", fontName="DV", fontSize=11, leading=16)

s = [Paragraph(f"Manual de Instruções e Autoria — {titulo}", h)]
s.append(Paragraph("O que vem no arquivo", h2))
s.append(Paragraph(f"Ao comprar, você baixa o arquivo <b>{zipname}</b>. Dentro dele:", p))
for i in itens.split("|"):
    s.append(Paragraph(f"• {i}", p))
s.append(Paragraph("Como usar", h2))
for n, i in enumerate(passos.split("|"), 1):
    s.append(Paragraph(f"{n}. {i}", p))
s.append(Paragraph("Autoria e direitos", h2))
s.append(Paragraph(
    f"O conteúdo de “{titulo}” é original e de autoria do produtor responsável por este produto na Hotmart. "
    "A compra dá direito ao uso pessoal (ou em sala de aula, no caso de materiais educativos). "
    "Não é permitido revender, redistribuir ou compartilhar os arquivos.", p))
s.append(Paragraph("Suporte", h2))
s.append(Paragraph("Dúvidas? Fale com o produtor pela própria Hotmart, na área “Minhas compras”. "
                   "Garantia de 7 dias: se não gostar, peça reembolso direto pela Hotmart.", p))
SimpleDocTemplate(out, pagesize=A4, leftMargin=56, rightMargin=56, topMargin=56, bottomMargin=56).build(s)
print("ok", out)
