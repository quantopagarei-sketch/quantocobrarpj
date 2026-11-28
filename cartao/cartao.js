// Cartão de oferta do Black Achadinhos (28/11/2026). Uso pelo Divulgador Facebook:
// 1) abra qualquer página do facebook.com na SUA aba; 2) rode este arquivo inteiro no javascript_tool,
//    trocando o objeto D no fim; 3) espere 2 s, tire screenshot (scale 1) e use o id no upload_image do post;
// 4) rode  document.getElementById('cartaoBA').remove(); document.documentElement.style.overflow='';
// Campos: nome, preco, preco_de (ou ''), parcelas (texto exato da página, ou ''), cupom (texto exato, ou ''), imagem (URL .jpg).
async function cartaoBA(D){
  document.getElementById('cartaoBA')?.remove();
  const f=v=>'R$ '+Number(v).toLocaleString('pt-BR',{minimumFractionDigits:Number(v)%1?2:0,maximumFractionDigits:2});
  const off=D.preco_de?Math.round((1-D.preco/D.preco_de)*100):0;
  const d=document.createElement('div');d.id='cartaoBA';
  d.style.cssText='position:fixed;inset:0;z-index:2147483647;background:#0b0b0b;display:flex;font-family:Arial,sans-serif;color:#fff;overflow:hidden';
  d.innerHTML=`
  <div style="width:46%;background:#fff;display:flex;align-items:center;justify-content:center;position:relative">
    <img id="cartaoImg" src="${D.imagem}" style="max-width:88%;max-height:88%;object-fit:contain">
    ${off?`<div style="position:absolute;top:28px;left:28px;background:#e8001c;color:#fff;font-weight:900;font-size:46px;padding:10px 22px;border-radius:14px">-${off}%</div>`:''}
  </div>
  <div style="flex:1;padding:48px 56px;display:flex;flex-direction:column;justify-content:center;gap:16px">
    <div style="font-size:22px;letter-spacing:6px;color:#FFD400;font-weight:900">BLACK ACHADINHOS · OFERTA DO DIA</div>
    <div style="font-size:40px;font-weight:700;line-height:1.15;max-height:140px;overflow:hidden">${D.nome}</div>
    ${D.preco_de?`<div style="font-size:30px;color:#aaa;text-decoration:line-through">${f(D.preco_de)}</div>`:''}
    <div style="font-size:96px;font-weight:900;color:#FFD400;line-height:1">${f(D.preco)}</div>
    ${D.parcelas?`<div style="font-size:32px;font-weight:700">💳 ${D.parcelas}</div>`:''}
    ${D.cupom?`<div style="font-size:30px;font-weight:700;background:#FFD400;color:#000;padding:10px 18px;border-radius:12px;align-self:flex-start">🎟️ ${D.cupom}</div>`:''}
    <div style="font-size:22px;color:#bbb;margin-top:8px">Preço conferido em ${new Date().toLocaleString('pt-BR',{day:'2-digit',month:'2-digit',hour:'2-digit',minute:'2-digit'})} · pode mudar a qualquer momento</div>
  </div>`;
  document.documentElement.style.overflow='hidden';document.body.appendChild(d);
  await new Promise(r=>{const i=document.getElementById('cartaoImg');if(i.complete)r();i.onload=r;i.onerror=r;setTimeout(r,4000)});
  return document.getElementById('cartaoImg').naturalWidth>0?'ok':'foto não carregou';
}
// Exemplo (troque pelos dados conferidos na página):
await cartaoBA({nome:'Kit com 5 carrinhos Hot Wheels', preco:49.90, preco_de:84.99, parcelas:'', cupom:'', imagem:'https://http2.mlstatic.com/D_NQ_NP_940549-MLA99850408707_112025-O.jpg'});
