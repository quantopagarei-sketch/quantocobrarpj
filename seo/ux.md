# Agente de UX — Quanto Eu Pago

Mantido pelo Agente de UX (quinta, 16h37). Objetivo: site curto, rápido e fácil no celular, focado nas calculadoras e no contador, sem perder SEO.

## ORÇAMENTO (375x800, medido ao carregar a página)
- Home: até 14 telas. Páginas com calculadora: até 16. Guias: até 20.
- Zero erro de JavaScript, zero rolagem horizontal, zero link interno quebrado.
- Home não ganha seções novas: página nova vira card em #ferramentas (8 a 12 cards).
- Botões e links soltos com 44px de altura (abaixo de 40px é problema); texto com 14px ou mais.
- Como medir: Playwright em 375x800 e 1280x800, com Analytics, AdSense, contador, /eventos.js, Clarity e cotações bloqueados; telas = scrollHeight/800 ao carregar; link dentro de frase não conta como alvo pequeno; das páginas /clt-pj/NNNN/ e /split-payment/pix-NNNN/ medir só 2 de cada.

## MEDIÇÃO 12/11/2026
| página | telas 375 | telas 1280 | KB | problemas |
|---|---|---|---|---|
| / | 10,8 | 8,6 | 78 | – |
| /impostos/ | 16,4 → 9,9 | 9,7 → 6,9 | 78 | link quebrado no topo e acima do orçamento (corrigido); % do supermercado com 13,6px |
| /clt-pj/ | 7,0 | 5,7 | 45 | 33 links de salário com 20px e coluna "Peça como PJ" escondida no celular (corrigido) |
| /split-payment/ | 13,2 | 8,5 | 56 | – |
| /mei-2027/ | 10,8 | 7,4 | 52 | – |
| /mei-passou-do-limite/ | 13,9 | 9,2 | 56 | selos de 12,5px |
| /privacidade/ | 4,7 | 3,1 | 37 | – |
| /clt-pj/5000/ e /2000/ | 6,2 e 6,0 | 4,1 | 42 | faixas da tabela com 13,1px |
| /sobre/ | 5,1 | 3,5 | 39 | – |
| /incorporar/ | 4,5 | 4,1 | 36 | crédito do exemplo com 13px (página protegida) |
| /guia-split-payment/ | 4,2 | 2,9 | 39 | – |
| /relatorio-mensal-mei/ | 7,5 | 5,5 | 48 | – |
| /quanto-cobrar-por-hora/ | 7,4 | 5,4 | 45 | – |
| /split-payment/como-calcular/ | 10,5 | 7,4 | 49 | 7 links de valores com 20–22px |
| /split-payment/quando-comeca/ | 8,5 | 5,5 | 47 | 3 links "Pix de R$" com 21px |
| /split-payment/simples-nacional/ | 8,7 | 5,6 | 50 | – |
| /split-payment/pix-1000/ e pix-5000 | 9,4 | 6,7 | 48 | – |
| /13-salario-pj/ | 10,3 | 7,3 | 49 | – |

Todas dentro do orçamento depois das correções. Nenhuma com erro de JavaScript, rolagem lateral, imagem sem width/height ou id repetido; 53 páginas do sitemap com zero link interno quebrado. Comum a todas (vem do tema.css): botão "Calcular agora" do topo com 38px e logo com 34px de altura; etiquetas .tag com 12,8px e texto do consentimento do formulário com 13,1px.

## Feito
- 12/11/2026 (UX): /impostos/ — o botão "Calcular agora" do topo apontava para #clt-mei, que só existe na home (link quebrado: o botão não fazia nada); agora vai para /#clt-mei, como nas outras páginas, e o logo vai para / (estava #top, copiado da home). Guia dos impostos: os 10 cartões e o do FGTS viraram <details> com o nome do imposto no <summary> (h3 mantido, nenhum texto apagado); CSS pequeno no bloco <style id="ux-css"> da página. FAQ e JSON-LD sem mudança. Telas: 16,4 → 9,9 no celular; 9,7 → 6,9 no computador.
- 12/11/2026 (UX): /clt-pj/ — na tabela, "Peça como PJ" (a resposta da página) virou a 2ª coluna: antes ficava escondida no celular, só aparecia arrastando a tabela. Números iguais, só mudou a ordem das colunas. O link do salário ocupa a célula inteira (20px → 48px de altura) e há um aviso só no celular ("Arraste a tabela para o lado para ver o ganho real e o regime"). Links pequenos: 36 → 5. Telas: 7,0 → 7,0.
- 10/11/2026 (pedido do Vini): visual novo em todas as páginas, tema "comprovante". Tudo fica em /tema.css (camada visual única; o <style> de cada página é só a base antiga, não mexer nele para mudar aparência). Topo verde-garrafa em bloco único, calculadora em cartão branco logo abaixo do título, resultado em bloco verde. Verde = o que é do usuário; amarelo (--gov) = parte do governo, só aí. Fontes no próprio site (/fontes/, Red Hat Display e Red Hat Text), sem Google Fonts. /visual.js desenha a barra que divide o pagamento nas 9 páginas com a calculadora de split. Campos com letra de 17px (o iPhone não dá zoom) e 50px de altura. Página nova: copiar o <head> de uma página atual (preload das fontes + /tema.css) e usar as classes existentes; não voltar para cantos retos, letras maiúsculas espaçadas ou fonte mono. Medição depois: home 10,7 telas, /split-payment/ 13,2.
- 08/11/2026 (sócio, pedido do Vini): home enxugada de 33,3 para 11,7 telas no celular. Ficaram: calculadoras CLT x PJ e split payment, grade "Mais calculadoras e guias" (#ferramentas), planilha, formulário do contador, 11 perguntas (CLT x PJ, MEI, split) e "Como calculamos" recolhido. Saíram para /impostos/: imposto no salário (janela #calc), supermercado, guia dos impostos, dólar e juros, contadores ao vivo e 9 perguntas. Explicação de split payment repetida saiu (está em /split-payment/). Links "/#guia" de 48 páginas agora apontam para /impostos/ (as protegidas continuam com /#guia, que cai no card). Script principal com $ seguro (elemento vazio se o id não existir).

## Fila
1. Topo de todas as páginas (tema.css): botão "Calcular agora" (38px) e logo (34px) com 44px de altura. Mexe no site inteiro: fazer sozinho numa execução, medindo antes e depois.
2. /split-payment/como-calcular/ e /split-payment/quando-comeca/: links de valores (20–22px) com a célula ou a linha inteira tocável, como em /clt-pj/ (são páginas com impressões no Google: só CSS, sem mexer em texto).
3. /split-payment/ (13,2 telas): ver o que dá para recolher abaixo da calculadora, sem mexer no topo (impressões no Google; título só depois de 22/11, e é do SEO).
4. /mei-passou-do-limite/ (13,9 telas): ver se o passo a passo e as fontes podem ir para <details>.
5. Textos abaixo de 14px que vêm do tema (etiquetas .tag, consentimento, % do supermercado, faixas das páginas de salário): avaliar junto com o visual, sem mudar a aparência do site por conta própria.

## Pedidos ao SEO
- (nenhum)
