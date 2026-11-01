// Rodar na página https://app.hotmart.com/products/manage/<ID>/affiliation-setup/promotional-materials
// Uso: window.__runKit('13').then(r=>window.__done=r)  (lê afiliados/<kit>/textos.json e banners deste repo)
(()=>{const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const setv=(el,v)=>{const p=el.tagName==='TEXTAREA'?HTMLTextAreaElement.prototype:HTMLInputElement.prototype;Object.getOwnPropertyDescriptor(p,'value').set.call(el,v);el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));};
const clickText=(sel,re)=>{const e=[...document.querySelectorAll(sel)].find(x=>re.test(x.textContent.trim()));if(!e)throw 'nf '+re;e.click();};
const count=l=>{const e=[...document.querySelectorAll('main *:not(:has(*))')].find(x=>x.textContent.trim()===l);return +(e.parentElement.textContent.replace(l,'').trim()||0);};
window.__runKit=async(kit)=>{const base='https://raw.githubusercontent.com/quantopagarei-sketch/quantocobrarpj/main/afiliados/'+kit+'/';
const T=await (await fetch(base+'textos.json?'+Date.now())).json();
for(const s of ['250x250','300x250','468x60','728x90','160x600','336x280']){if(count('Banner '+s)>0)continue;
clickText('main *:not(:has(*))',new RegExp('^Banner '+s+'$'));await sleep(1300);clickText('button,a',/^Adicionar novo banner$/);await sleep(1300);
setv(document.querySelector('input[placeholder="Título do banner"]'),'Banner '+s);setv([...document.querySelectorAll('input')].find(i=>/URL da imagem/.test(i.placeholder)),base+'banner-'+s+'.png');await sleep(300);
clickText('button',/^Adicionar banner$/);await sleep(2300);}
if(count('Modelo de Tweet')==0){for(const p of T.posts){clickText('main *:not(:has(*))',/^Modelo de Tweet$/);await sleep(1300);clickText('button,a',/^Adicionar novo modelo$/);await sleep(1300);
setv(document.querySelector('input[placeholder="Título do modelo de Tweet"]'),p.titulo);setv([...document.querySelectorAll('main textarea')].at(-1),p.texto);await sleep(300);clickText('button',/^Adicionar modelo$/);await sleep(2300);}}
if(count('Modelo de email')==0){const em=T.emails.map(e=>({a:e.assunto,c:e.corpo})).concat([{a:'Guia do afiliado: argumentos, objeções e o que não prometer',c:T.argumentos}]);
for(const e of em){clickText('main *:not(:has(*))',/^Modelo de email$/);await sleep(1300);clickText('button,a',/^Adicionar novo modelo$/);await sleep(1300);
setv(document.querySelector('input[placeholder="Assunto do e-mail"]'),e.a);setv(document.querySelector('textarea[placeholder="Corpo do e-mail"]'),e.c);await sleep(300);clickText('button',/^Adicionar modelo$/);await sleep(2300);}}
return 'done';};})();
