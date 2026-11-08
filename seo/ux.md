# Agente de UX — Quanto Eu Pago

Mantido pelo Agente de UX (quinta, 16h37). Objetivo: site curto, rápido e fácil no celular, focado nas calculadoras e no contador, sem perder SEO.

## ORÇAMENTO (375x800, medido ao carregar a página)
- Home: até 14 telas. Páginas com calculadora: até 16. Guias: até 20.
- Zero erro de JavaScript, zero rolagem horizontal, zero link interno quebrado.
- Home não ganha seções novas: página nova vira card em #ferramentas (8 a 12 cards).

## MEDIÇÃO 08/11/2026 (sócio)
| página | telas 375 | telas 1280 | KB |
|---|---|---|---|
| / (antes) | 33,3 | 20,5 | 107 |
| / (depois) | 11,7 | 8,9 | 77 |
| /impostos/ (nova) | 18,1 | 10,5 | 78 |
| /split-payment/ | 14,1 | – | 54 |
| /mei-2027/ | 11,4 | – | 49 |
| /clt-pj/ | 7,7 | – | 45 |

## Feito
- 08/11/2026 (sócio, pedido do Vini): home enxugada de 33,3 para 11,7 telas no celular. Ficaram: calculadoras CLT x PJ e split payment, grade "Mais calculadoras e guias" (#ferramentas), planilha, formulário do contador, 11 perguntas (CLT x PJ, MEI, split) e "Como calculamos" recolhido. Saíram para /impostos/: imposto no salário (janela #calc), supermercado, guia dos impostos, dólar e juros, contadores ao vivo e 9 perguntas. Explicação de split payment repetida saiu (está em /split-payment/). Links "/#guia" de 48 páginas agora apontam para /impostos/ (as protegidas continuam com /#guia, que cai no card). Script principal com $ seguro (elemento vazio se o id não existir).

## Fila
1. /impostos/ (18,1 telas): recolher os cards do "Guia dos impostos" em <details> por imposto.
2. /split-payment/ (14,1 telas): ver o que dá para recolher sem mexer no topo, que tem impressões no Google.

## Pedidos ao SEO
- (nenhum)
