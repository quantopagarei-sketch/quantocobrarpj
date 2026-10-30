// Guardião do site: confere se o que gera dinheiro está funcionando.
const {chromium}=require('playwright');const fs=require('fs');
const BASE='https://quantocobrarpj.com.br';
(async()=>{
  const prob=[];const ok=[];
  const sm=fs.readFileSync('sitemap.xml','utf8');const urls=[...sm.matchAll(/<loc>([^<]+)<\/loc>/g)].map(m=>m[1]);
  for(const u of urls){try{const r=await fetch(u,{redirect:'follow'});if(r.status!==200)prob.push(`Página fora do ar (${r.status}): ${u}`);}catch(e){prob.push(`Página não abriu: ${u}`);}}
  ok.push(`${urls.length} páginas do sitemap verificadas`);
  const b=await chromium.launch();const p=await b.newPage({viewport:{width:375,height:800}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
  await p.goto(BASE+'/?s=5000',{waitUntil:'networkidle'});await p.waitForTimeout(1500);
  const h=await p.evaluate(()=>({mk:(document.getElementById('mk')||{}).textContent||'',form:!!document.querySelector('form[name=contador][data-netlify]'),area:!!document.querySelector('form[name=contador] [name=area]'),ga:!!document.querySelector('script[src*="G-CYDV58698D"]'),share:((document.getElementById('pjshare')||{}).href||'').includes('wa.me/?text='),cta:document.querySelectorAll('.ctabox').length,sw:document.documentElement.scrollWidth}));
  if(!/R\$\s?8\.000/.test(h.mk))prob.push(`Calculadora CLT x PJ com resultado estranho para R$ 5.000: "${h.mk}"`);else ok.push('Calculadora CLT x PJ ok');
  if(!h.form||!h.area)prob.push('Formulário de contador sumiu ou está sem o campo "area" na home');else ok.push('Formulário de contador ok');
  if(!h.ga)prob.push('Tag do Google Analytics sumiu da home');
  if(!h.share)prob.push('Botão de WhatsApp quebrado');
  if(h.cta<2)prob.push('Caixas "Falar com um contador" sumiram da home');
  if(h.sw>380)prob.push(`Home com rolagem para o lado no celular (${h.sw}px)`);
  if(errs.length)prob.push('Erro de JavaScript na home: '+errs[0]);
  const p2=await b.newPage({viewport:{width:375,height:800}});const e2=[];p2.on('pageerror',e=>e2.push(e.message));
  for(const path of ['/clt-pj/5000/','/mei-2027/','/split-payment/','/incorporar/']){await p2.goto(BASE+path,{waitUntil:'domcontentloaded'});await p2.waitForTimeout(600);
    const r=await p2.evaluate(()=>({ga:!!document.querySelector('script[src*="G-CYDV58698D"]'),foot:!!document.querySelector('footer'),sw:document.documentElement.scrollWidth}));
    if(!r.ga)prob.push('Sem Google Analytics: '+path);if(!r.foot)prob.push('Sem rodapé: '+path);if(r.sw>380)prob.push(`Rolagem para o lado: ${path}`);}
  if(e2.length)prob.push('Erro de JavaScript nas páginas internas: '+e2[0]);
  await b.close();
  const st={verificado_em:new Date().toLocaleString('pt-BR',{timeZone:'America/Sao_Paulo'}),status:prob.length?'PROBLEMA':'OK',problemas:prob,ok};
  fs.writeFileSync('seo/saude.json',JSON.stringify(st,null,1)+'\n');
  console.log(JSON.stringify(st,null,1));
  if(prob.length)process.exitCode=1;
})();
