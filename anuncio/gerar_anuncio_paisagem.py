"""Anúncio em paisagem (1920x919) para subir no Gerenciador pelo print da tela (ver design.md)."""
import argparse
from PIL import Image, ImageDraw, ImageFont
BG=(12,12,14); AM=(255,212,0); BR=(255,255,255); CZ=(170,170,175)
B="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; R="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
f=lambda p,s: ImageFont.truetype(p,s)
def fit(d,txt,path,size,maxw):
    while d.textlength(txt,font=f(path,size))>maxw and size>20: size-=2
    return f(path,size)
p=argparse.ArgumentParser()
for a in ("foto","nome","linha2","preco","sufixo","extra","saida"): p.add_argument("--"+a,default="")
a=p.parse_args()
W,H=1920,919
im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
# cartão branco com a foto (esquerda)
cx0,cy0,cw,ch=150,90,640,739
d.rounded_rectangle((cx0,cy0,cx0+cw,cy0+ch),radius=48,fill=BR)
ft=Image.open(a.foto).convert("RGB"); s=min((cw-70)/ft.width,(ch-70)/ft.height,1.5)
ft=ft.resize((int(ft.width*s),int(ft.height*s)),Image.LANCZOS)
im.paste(ft,(cx0+(cw-ft.width)//2,cy0+(ch-ft.height)//2))
# texto (direita)
x=880; mw=W-x-150
fn=fit(d,a.nome,B,150,mw); d.text((x,110),a.nome,font=fn,fill=BR)
fl=fit(d,a.linha2,B,70,mw); d.text((x,290),a.linha2,font=fl,fill=AM)
pt=f"{a.preco} {a.sufixo}".strip(); fp=fit(d,pt,B,92,mw-90)
pw=d.textlength(pt,font=fp)+90; d.rounded_rectangle((x,430,x+pw,430+150),radius=75,fill=AM)
bb=d.textbbox((0,0),pt,font=fp); d.text((x+45,430+(150-(bb[3]-bb[1]))/2-bb[1]),pt,font=fp,fill=BG)
if a.extra: d.text((x,615),a.extra,font=fit(d,a.extra,R,44,mw),fill=BR)
d.text((x,740),"Vendido no Mercado Livre · Black Achadinhos",font=f(R,34),fill=CZ)
d.text((x,790),"Publicidade · link de afiliado",font=f(R,28),fill=CZ)
im.save(a.saida,quality=93)
