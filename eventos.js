/* Contagem anônima de uso (sem dados pessoais): conta 1 por visita para cada calculadora usada e cada tipo de link clicado.
   Os números são lidos todo dia pelo GitHub Actions (seo/eventos.csv) e entram no relatório do Gerente. NÃO remover. */
(function(){
var d=new Date(),p=function(n){return(n<10?"0":"")+n},dia=d.getFullYear()+p(d.getMonth()+1)+p(d.getDate());
function hit(k){var key=k+"-"+dia;try{if(sessionStorage.getItem("qe_"+key))return;sessionStorage.setItem("qe_"+key,"1");}catch(e){}
try{fetch("https://abacus.jasoncameron.dev/hit/quantoeupago-br/"+key,{mode:"cors",keepalive:true}).catch(function(){});}catch(e){}}
var seg=(location.pathname.split("/")[1]||"").toLowerCase();
var PAG={"split-payment":"split","mei-2027":"mei2027","mei-passou-do-limite":"meilimite","quanto-cobrar-por-hora":"hora","relatorio-mensal-mei":"relmei","clt-pj":"tabela"};
var SEC={"clt-mei":"cltpj","splitbox":"split","imposto":"imposto","super":"super"};
function calcKey(el){if(!seg){var s=el.closest&&el.closest("section[id]");return SEC[s&&s.id]||"outra";}return PAG[seg]||"outra";}
function noForm(el){var f=el.closest&&el.closest("form");return !(f&&(f.getAttribute("name")==="contador"||f.getAttribute("name")==="guia"));}
function onUse(e){var el=e.target;if(!el||!el.matches||!el.matches("input,select,textarea"))return;if(el.closest("footer")||!noForm(el))return;if(el.type==="hidden")return;hit("c-"+calcKey(el));}
document.addEventListener("input",onUse,true);document.addEventListener("change",onUse,true);
document.addEventListener("click",function(e){var t=e.target&&e.target.closest?e.target.closest("a,button"):null;if(!t)return;
var id=t.id||"",h=(t.getAttribute("href")||"").toLowerCase(),cta=t.getAttribute("data-cta")||"";
if(id==="pjshare"||id==="comp"||id==="gshare"||h.indexOf("wa.me")>-1||h.indexOf("whatsapp")>-1){hit("k-whatsapp");return;}
if(h.indexOf("contabilidadeti.com.br")>-1){hit("k-contabti");return;}
if(h.indexOf("hotmart")>-1){hit("k-produto");return;}
if(cta==="guia"||(h.indexOf("/guia-split-payment/")>-1&&h.indexOf(".pdf")<0)){hit("k-guia");return;}
if(h.indexOf(".pdf")>-1){hit("k-pdf");return;}
if(cta||h==="#contador"||h.indexOf("/#contador")>-1||h.indexOf("#contador")>-1){hit("k-contador");return;}
if(/^https?:\/\//.test(h)&&h.indexOf("quantocobrarpj.com.br")<0){hit("k-externo");}},true);
document.addEventListener("submit",function(e){var n=e.target&&e.target.getAttribute&&e.target.getAttribute("name");if(n==="contador"||n==="guia")hit("f-"+n);},true);
})();
