/* Barra que divide o pagamento no resultado do split payment (verde = cai na sua conta, amarelo = governo).
   Só desenha: lê os valores que a calculadora da página já escreveu. */
(function(){
var g=function(i){return document.getElementById(i)},pago=g("sp1"),ret=g("sp2"),seu=g("sp3"),big=g("spo1");
if(!pago||!ret||!seu||!big||!big.parentNode)return;
var box=big.parentNode,bar=document.createElement("div"),leg=document.createElement("div");
bar.className="splitbar";bar.setAttribute("role","img");bar.innerHTML='<i class="sua"></i><i class="gov"></i>';
leg.className="splitleg";leg.innerHTML='<span class="sua">Cai na sua conta<b></b></span><span class="gov">Vai para o governo<b></b></span>';
box.appendChild(bar);box.appendChild(leg);
function n(t){return parseFloat(String(t).replace(/[^\d,]/g,"").replace(",","."))||0}
function draw(){var p=n(pago.textContent),r=n(ret.textContent),pc=p>0?Math.min(100,r/p*100):0;
bar.lastChild.style.flexBasis=pc+"%";bar.lastChild.style.display=pc>0?"":"none";
leg.firstChild.lastChild.textContent=seu.textContent;leg.lastChild.lastChild.textContent=ret.textContent.replace(/^[−-]\s*/,"");
leg.lastChild.style.display=pc>0?"":"none";
bar.setAttribute("aria-label","De cada pagamento, "+(100-pc).toFixed(1).replace(".",",")+"% cai na sua conta e "+pc.toFixed(1).replace(".",",")+"% vai para o governo");}
draw();
if(window.MutationObserver)new MutationObserver(draw).observe(ret,{childList:true,characterData:true,subtree:true});
})();
