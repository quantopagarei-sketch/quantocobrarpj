# Agente de UX — Quanto Eu Pago

Mantido pelo Agente de UX (quinta, 16h37). Objetivo: site curto, rápido e fácil no celular, focado nas calculadoras e no contador, sem perder SEO.

## ORÇAMENTO (375x800, medido ao carregar a página)
- Home: até 14 telas. Páginas com calculadora: até 16. Guias: até 20.
- Zero erro de JavaScript, zero rolagem horizontal, zero link interno quebrado.
- Home não ganha seções novas: página nova vira card em #ferramentas (8 a 12 cards).
- Botões e links soltos com 44px de altura (abaixo de 40px é problema); texto com 14px ou mais.
- Extra (desde 19/11): nenhuma página rola para o lado em 320px (iPhone SE e celular com zoom de tela).
- Como medir: Playwright em 375x800 e 1280x800, com Analytics, AdSense, contador, /eventos.js, Clarity e cotações bloqueados; telas = scrollHeight/800 ao carregar; link dentro de frase não conta como alvo pequeno; das páginas /clt-pj/NNNN/ e /split-payment/pix-NNNN/ medir só 2 de cada.

## MEDIÇÃO 19/11/2026
| página | telas 375 | telas 1280 | KB | problemas |
|---|---|---|---|---|
| / | 11,1 | 8,6 | 78 | – |
| /impostos/ | 9,9 | 6,9 | 78 | % do supermercado com 13,6px; "Dólar agora" com 12,8px |
| /clt-pj/ | 10,3 | 8,0 | 51 | – |
| /split-payment/ | 13,3 | 8,5 | 57 | – |
| /mei-2027/ | 10,9 | 7,5 | 53 | – |
| /mei-passou-do-limite/ | 13,9 | 9,2 | 56 | selos de 12,5px |
| /privacidade/ | 4,7 | 3,1 | 37 | – |
| /sobre/ | 5,1 | 3,5 | 39 | – |
| /incorporar/ | 4,5 | 4,1 | 36 | crédito do exemplo com 13px (página protegida) |
| /guia-split-payment/ | 4,3 | 2,9 | 39 | – |
| /relatorio-mensal-mei/ | 7,8 | 5,7 | 48 | – |
| /quanto-cobrar-por-hora/ | 9,7 | 6,8 | 49 | – |
| /13-salario-pj/ | 10,6 | 7,6 | 49 | – |
| /split-payment/como-calcular/ | 10,6 | 7,5 | 49 | 7 links de valores com 20–22px |
| /split-payment/quando-comeca/ | 10,0 | 6,1 | 49 | 3 links "Pix de R$" com 21px |
| /split-payment/simples-nacional/ | 8,7 | 5,7 | 50 | – |
| /split-payment/mei/ | 9,1 | 5,8 | 50 | – |
| /split-payment/cartao/ (nova) | 9,5 | 6,0 | 51 | – |
| /split-payment/tabela-pix-2027/ (nova) | 9,5 | 6,7 | 51 | – |
| /split-payment/pix-1000/ e pix-2000 | 9,4 | 6,8 | 48 | – |
| /clt-pj/4000/ e /5000/ | 6,3 | 4,1 | 42 | faixas da tabela com 13,1px |

Números depois da correção de hoje. Todas dentro do orçamento; nenhuma com erro de JavaScript, rolagem lateral (375, 1280 e 320px), imagem sem width/height ou id repetido; 56 páginas do sitemap com zero link interno quebrado (âncoras conferidas). Antes da correção: as 56 páginas rolavam para o lado em 320px (o botão "Calcular agora" saía cortado) e todas tinham 3 ou 4 alvos pequenos no topo e no rodapé. Comum a todas (tema.css): etiquetas .tag com 12,8px e texto do consentimento do formulário com 13,1px.

## Feito
- 19/11/2026 (UX): tema.css (vale para todas as páginas; nenhum HTML mudou) — logo e botão "Calcular agora" do topo com 44px de altura (eram 34 e 38px; o topo continua com 60px no celular e 70px no computador, porque o respiro do .hd caiu de 12/10 para 8/8px), logo do rodapé com 44px e link solto (a.lk sem .btn: home, /clt-pj/, /mei-2027/) com 44px (era 24px). Celular pequeno (até 359px): logo com 28px e respiro lateral de 12px no topo (antes o botão saía cortado e as 56 páginas rolavam para o lado em 320px) e legenda da barra do split em uma coluna (o cartão da calculadora ficava maior que a tela em /, /split-payment/, pix-10000 e pix-20000). Alvos pequenos: 3–4 → 0 por página (ficam só os de como-calcular e quando-comeca, item 1 da fila). Rolagem em 320px: 56 → 0 páginas. Telas: iguais (+0,1 no máximo, pelo rodapé).
- 12/11/2026 (UX): /impostos/ — o botão "Calcular agora" do topo apontava para #clt-mei, que só existe na home (link quebrado: o botão não fazia nada); agora vai para /#clt-mei, como nas outras páginas, e o logo vai para / (estava #top, copiado da home). Guia dos impostos: os 10 cartões e o do FGTS viraram <details> com o nome do imposto no <summary> (h3 mantido, nenhum texto apagado); CSS pequeno no bloco <style id="ux-css"> da página. FAQ e JSON-LD sem mudança. Telas: 16,4 → 9,9 no celular; 9,7 → 6,9 no computador.
- 12/11/2026 (UX): /clt-pj/ — na tabela, "Peça como PJ" (a resposta da página) virou a 2ª coluna: antes ficava escondida no celular, só aparecia arrastando a tabela. Números iguais, só mudou a ordem das colunas. O link do salário ocupa a célula inteira (20px → 48px de altura) e há um aviso só no celular ("Arraste a tabela para o lado para ver o ganho real e o regime"). Links pequenos: 36 → 5. Telas: 7,0 → 7,0.
- 10/11/2026 (pedido do Vini): visual novo em todas as páginas, tema "comprovante". Tudo fica em /tema.css (camada visual única; o <style> de cada página é só a base antiga, não mexer nele para mudar aparência). Topo verde-garrafa em bloco único, calculadora em cartão branco logo abaixo do título, resultado em bloco verde. Verde = o que é do usuário; amarelo (--gov) = parte do governo, só aí. Fontes no próprio site (/fontes/, Red Hat Display e Red Hat Text), sem Google Fonts. /visual.js desenha a barra que divide o pagamento nas 9 páginas com a calculadora de split. Campos com letra de 17px (o iPhone não dá zoom) e 50px de altura. Página nova: copiar o <head> de uma página atual (preload das fontes + /tema.css) e usar as classes existentes; não voltar para cantos retos, letras maiúsculas espaçadas ou fonte mono. Medição depois: home 10,7 telas, /split-payment/ 13,2.
- 08/11/2026 (sócio, pedido do Vini): home enxugada de 33,3 para 11,7 telas no celular. Ficaram: calculadoras CLT x PJ e split payment, grade "Mais calculadoras e guias" (#ferramentas), planilha, formulário do contador, 11 perguntas (CLT x PJ, MEI, split) e "Como calculamos" recolhido. Saíram para /impostos/: imposto no salário (janela #calc), supermercado, guia dos impostos, dólar e juros, contadores ao vivo e 9 perguntas. Explicação de split payment repetida saiu (está em /split-payment/). Links "/#guia" de 48 páginas agora apontam para /impostos/ (as protegidas continuam com /#guia, que cai no card). Script principal com $ seguro (elemento vazio se o id não existir).

## Fila
1. /split-payment/como-calcular/ e /split-payment/quando-comeca/: links de valores (20–22px) com a célula ou a linha inteira tocável, como em /clt-pj/ (páginas com impressões no Google: só CSS, sem mexer em texto).
2. /split-payment/ (13,3 telas): ver o que dá para recolher abaixo da calculadora, sem mexer no topo — só depois de 22/11 (teste de título do SEO) e sem tirar texto que responde busca.
3. /mei-passou-do-limite/ (13,9 telas): ver se o passo a passo e as fontes podem ir para <details>.
4. Textos abaixo de 14px que vêm do tema ou da base (etiquetas .tag 12,8px, consentimento 13,1px, % do supermercado 13,6px, faixas das páginas de salário 13,1px, selos 12,5px, avisos de 13,6–13,8px): avaliar junto com o visual, sem mudar a aparência do site por conta própria.
5. Toda medição: conferir também 320px nas páginas novas (rolagem lateral).

## Pedidos ao SEO
- (nenhum)
