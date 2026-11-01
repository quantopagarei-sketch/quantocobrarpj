import json
from PIL import Image, ImageDraw, ImageFont
B="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; R="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F=lambda p,s: ImageFont.truetype(p,s)
cat=json.load(open('repo/afiliados/catalogo.json'))['produtos']
cores={"finan":"#2e6f9e","educa":"#c0662f","IA":"#5b3fd6","culin":"#b8452f","carreira":"#3d6b4f","concurso":"#7a4fa0","pets":"#8a5a2b","festa":"#d0447a","negócio":"#1f7a72","idioma":"#2f5fa8","MEI":"#20638f","casa":"#2f7d6b","casamento":"#b5546e"}
def cor(n):
    for k,v in cores.items():
        if k.lower() in n.lower(): return v
    return "#444466"
def wrap(d,t,f,w):
    out,cur=[],""
    for x in t.split():
        c=(cur+" "+x).strip()
        if d.textlength(c,font=f)<=w: cur=c
        else: out.append(cur); cur=x
    out.append(cur); return out
def sub(p):
    try:
        a=json.load(open(f"repo/afiliados/{p['id']}/textos.json"))['argumentos']; i=a.find('BENEFÍCIOS:')
        lines=[l.split(') ',1)[-1].split(':')[0].strip() for l in a[i:].split('\n')[1:4] if l.strip()]
        return [l for l in lines if 3<len(l)<60][:3]
    except Exception: return []
for p in cat:
    W,H=1000,1500; base=tuple(int(cor(p['nicho'])[i:i+2],16) for i in (1,3,5))
    im=Image.new("RGB",(W,H),base); d=ImageDraw.Draw(im)
    for y in range(H): t=y/H; d.line([(0,y),(W,y)],fill=tuple(int(c*(1-0.35*t)) for c in base))
    d.rounded_rectangle([60,60,W-60,H-60],radius=40,outline=(255,255,255),width=4)
    tag="PLANILHA" if "Planilha" in p['nome'] else "GUIA EM PDF"
    d.rounded_rectangle([110,120,110+d.textlength(tag,font=F(B,34))+50,190],radius=35,fill=(255,205,60)); d.text((135,135),tag,font=F(B,34),fill=(30,30,30))
    s=110
    while s>50:
        f=F(B,s); ls=wrap(d,p['nome'],f,W-220)
        if len(ls)*s*1.15<560 and max(d.textlength(l,font=f) for l in ls)<=W-220: break
        s-=4
    y=270
    for l in ls: d.text((110,y),l,font=f,fill="white"); y+=int(s*1.15)
    y+=40
    for b in sub(p):
        for l in wrap(d,"✓ "+b,F(R,46),W-220): d.text((110,y),l,font=F(R,46),fill=(240,240,240)); y+=60
        y+=12
    if p['preco']!='?': d.text((110,H-330),("R$ " if not p['preco'].startswith('US') else "")+p['preco'],font=F(B,90),fill=(255,205,60))
    d.rounded_rectangle([110,H-200,W-110,H-110],radius=45,fill="white")
    cta="Veja como funciona"; tw=d.textlength(cta,font=F(B,42)); d.text(((W-tw)/2,H-178),cta,font=F(B,42),fill=(30,30,30))
    im.save(f"pins/pin-{p['id']}.png")
