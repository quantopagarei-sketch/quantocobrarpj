# Como ler seo/eventos.csv (uso do site por dia)

Cada número = quantas VISITAS fizeram aquilo no dia (conta 1 por visita, mesmo que a pessoa clique várias vezes). Anônimo, sem dados pessoais. Gravado às 20h17 pelo GitHub Actions (visitas.yml), a partir do script /eventos.js presente em todas as páginas.

Calculadoras usadas (pessoa mexeu em algum campo):
- c-cltpj: CLT x PJ (home) · c-split: split payment (home ou /split-payment/) · c-imposto: "Meu imposto" (home) · c-super: supermercado (home)
- c-mei2027: /mei-2027/ · c-meilimite: /mei-passou-do-limite/ · c-hora: /quanto-cobrar-por-hora/ · c-relmei: /relatorio-mensal-mei/ · c-tabela: /clt-pj/ · c-outra: outras

Cliques:
- k-whatsapp: compartilhar no WhatsApp · k-contador: botões "falar com um contador" · k-guia: chamadas para o e-book · k-pdf: baixou o PDF do e-book
- k-contabti: cliques no link da parceira Contabilidade TI
- k-produto: links de produtos (Hotmart) · k-externo: links para outros sites (gov.br etc.)

Formulários enviados: f-contador (pedido de contador) · f-guia (download do e-book com cadastro)

Antes de 01/11/2026 não havia medição (linhas começam em 01/11). Não remover /eventos.js nem a linha <script src="/eventos.js"> das páginas; toda página nova deve ter essa linha antes de </body>.
