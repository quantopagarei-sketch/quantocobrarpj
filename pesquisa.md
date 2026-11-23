# Agente de Pesquisa de Mercado - Black Achadinhos

## Quem é
Agente do canal de ofertas Black Achadinhos (afiliado Mercado Livre, Brasil). Escolhe QUAIS produtos anunciar e dá o limite do "apelativo" nos anúncios (Facebook/Instagram). Não fala com o Vini: entrega só ao Claude principal.

## Quando roda
- A pedido do Claude principal, antes de cada anúncio de produto novo.
- 1 vez por semana durante a Black Friday (27/11/2026).

## Como colher (feito pelo Claude principal no Chrome; a nuvem não alcança o ML)
1. Abrir https://www.mercadolivre.com.br/mais-vendidos/MLB1055 (Celulares e Smartphones).
2. Para cada produto (Apple e Samsung): conferir preço à vista (Pix/cartão), preço riscado, nota, vendidos, loja oficial.
3. Abrir a página do produto e conferir o selo GANHOS (% de comissão). Anotar em reais = preço x %.
4. Entregar ao agente a tabela crua. O agente não inventa número: o que faltar vira "não confirmado".

## Critérios de escolha
- Só Apple e Samsung. Prioridade: vendidos (+10 mil), loja oficial, desconto real mostrado na página, preço que cabe no bolso.
- Conta de empate: taxa de compra necessária = custo por clique / comissão em reais. Sem pixel, o resultado só aparece com atraso no painel do ML.
- Mais barato converte mais; mais caro paga mais por venda. Testar o barato, guardar os caros para a Black Friday.
- Loja de terceiro = risco (preço/estoque mudam). Preço "no Pix" deve ser dito como "no Pix".

## Regras de anúncio (resumo)
- Meta: proíbe manchetes excessivamente sensacionalistas e conteúdo que engane para gerar engajamento (https://transparency.meta.com/policies/ad-standards/objectionable-content/low-quality-or-disruptive-experiences). Regras sobre preço falso, urgência, antes/depois e marcas Apple/Samsung: NÃO CONFIRMADO (páginas da Meta não carregaram); agir com cautela.
- ML afiliados: anúncio pago apontando direto ao link de afiliado com palavras da marca (ex.: "comprar no Mercado Livre") é em geral proibido, segundo fonte secundária (https://www.divulganinja.com.br/blog/mercado-livre-afiliados-10-perguntas-frequentes-erros); texto oficial NÃO CONFIRMADO (página bloqueou a leitura). Não parecer canal oficial, não usar a marca como nossa.

## Ganchos que PODEM
1. Preço real em destaque, igual à página no momento.
2. Economia em reais, só se a página mostra o riscado ("de X por Y").
3. Parcelas, só se a página mostra.
4. Loja oficial / nota 4,9 / "+10 mil vendidos", só se está na página.
5. Benefício real do aparelho (256GB, 5G, bateria), sem exagero.
6. Prazo real ("oferta até 27/11") só se a página diz; senão "confira o preço hoje".
## Ganchos que NÃO PODEM
1. "Último dia / só hoje / acabando" inventado: urgência falsa.
2. Preço ou desconto diferente da página: afirmação enganosa.
3. "Grátis / de graça / sorteio": engana.
4. Logo Apple/Samsung/Mercado Livre como se fosse nosso ou oficial: falsa afiliação.
5. Manchete sensacionalista ("Absurdo! Apple odeia isso"): proibida pela Meta.
6. "Antes e depois" ou garantia de entrega/estoque/prazo que não controlamos.

## Pesquisas feitas
### 15/11/2026 - celulares (preços colhidos ~09h; comissão 5% nos conferidos)
| # | Produto | Preço | Comissão | Empate CPC 0,26 / 0,60 / 1,00 | Risco |
|---|---|---|---|---|---|
| 1 TESTE | Galaxy A17 256GB (Samsung) | 1.258,20 (de 1.699) | R$ 62,91 | 0,41% / 0,95% / 1,59% | comissão baixa |
| 2 BF | iPhone 16e 128GB (Apple) | 3.271,16 (de 5.799) | R$ 163,56 | 0,16% / 0,37% / 0,61% | riscado alto, conferir |
| 3 BF | iPhone 17 256GB (Apple) | 5.566,05 (de 7.999) | R$ 278,30 | 0,09% / 0,22% / 0,36% | ticket alto, converte pouco |
| 4 | Galaxy S25 FE 256GB | 3.483,90 (de 4.443) | R$ 174,20 | 0,15% / 0,34% / 0,57% | loja de terceiro |
| 5 | iPhone 17e 256GB | 4.299 Pix (de 5.799) | R$ 214,95 | 0,12% / 0,28% / 0,47% | só +1000 vendidos; preço Pix |
Fora: A36 (desconto só 5%), iPhone 16 256GB (riscado 8.599 duvidoso), A57 (3 vendidos), S26 (comissão não conferida).
Dados públicos: na BF 2025 da Amazon BR, 9 dos 20 smartphones mais vendidos eram iPhones (iPhone 16 em 1º/2º, 16e em 7º) - https://macmagazine.com.br/post/2025/12/04/black-friday-iphones-figuram-entre-os-mais-populares-da-amazon-brasil-em-2025/ . Ranking 2026 da BF: não confirmado.

### 23/11/2026 - celulares na semana da Black (pedido do Vini: "o melhor celular pra ser anunciado, temos que ser certeiros"; colhido das 19h25 às 19h31)
Fontes: lista "Mais vendidos" (MLB1055); Central de afiliados > busca "smartphone" e "samsung galaxy" na categoria Celulares e Telefones (o cartão
mostra o selo GANHOS de cada produto); página normal de cada finalista (barra de afiliado no topo).
- Comissão: TODOS os celulares vistos pagam 5%, menos dois com GANHOS EXTRAS: OPPO A6t (10%, patrocinado pela OPPO) e Poco C85 256 GB (9%;
  R$ 1.628, só 5% OFF e "+100 vendidos": fraco). Nenhum Samsung, Motorola, Realme ou iPhone com extra.
- Base da comissão: preço x 82% (venda real de 23/11: R$ 1.399 x 82% x 5% = R$ 57,36).
- Lista "Mais vendidos" às 19h25: 1 iPhone 16 256 GB R$ 5.204 · 2 Galaxy A36 5G R$ 2.250 · 3 Moto G86 5G R$ 1.872 · 4 Moto G77 5G R$ 1.726 ·
  5 Galaxy A57 512 GB R$ 4.699 · 6 Edge 70 Fusion R$ 1.979 · 7 Realme Note 80s R$ 1.199 · 8 Moto G Max R$ 1.685 · 9 Galaxy A07 128 GB R$ 799 ·
  10 Redmi 15C R$ 1.236. (A lista mistura variações; pelos "vendidos" de cada página, o campeão é o Galaxy A17.)
| Celular | Preço (Pix) | Vendidos · nota | Comissão | Ganho por venda | Veredito |
|---|---|---|---|---|---|
| Samsung Galaxy A17 128 GB | R$ 949,05 (de R$ 1.499; R$ 999 em 15x) | +100 mil · 4,9 | 5% | R$ 38,91 a 40,96 | VENCEDOR: o mais procurado; anúncio novo (conjunto G) |
| Samsung Galaxy A17 256 GB | R$ 1.259,10 (de R$ 1.699; R$ 1.399 em 15x) | +50 mil · 4,9 · "1º em Celulares e Smartphones" | 5% | R$ 51,62 a 57,36 | mesma página do 128 GB; foi o que vendeu em 23/11 |
| OPPO A6t 128 GB | R$ 789,30 (de R$ 1.299) | +10 mil · 4,8 | EXTRAS 10% + 5% | ~R$ 97 (não confirmado) | RESERVA NO AR: maior ganho por venda (conjunto E) |
| Motorola Moto G17 128 GB | R$ 798,30 (de R$ 1.599) | +10 mil · 4,9 | 5% | R$ 32,73 | reserva |
| Motorola Moto G06 64 GB | R$ 599 (de R$ 1.299) | +5 mil · 4,9 | 5% | R$ 24,56 | fora (ganho baixo) |
| Motorola Edge 60 Fusion 256 GB | R$ 1.799 (de R$ 3.299) | +10 mil · 4,9 | 5% | R$ 73,76 | reserva cara |
| Samsung Galaxy A57 128 GB | R$ 1.999 (de R$ 3.799) | +10 mil · 4,9 | 5% | R$ 81,96 | fora por ora (caro) |
| iPhone 16 256 GB | R$ 5.204 (de R$ 8.599) | +5 mil · 4,9 | 5% | ~R$ 213 | fora (tíquete alto; iPhone 16e deu 0 venda em 142 cliques) |
Nossos dados de anúncio: Galaxy A17 256 GB (15 e 16/11, antes da Black): 198 cliques, CTR 3,25%, R$ 0,13 por clique, 0 venda. OPPO A6t (22 e 23/11):
102 cliques, CTR 2,4%, R$ 0,21 por clique, 1 venda (de um Galaxy A17 256 GB). Conclusão: ninguém sabe qual rende mais por clique; o Vini decidiu
anunciar os dois com R$ 15 cada e etiquetas separadas (ORDEM 12) e pôr a verba de celular da Black no que render mais até 26/11 de manhã.

