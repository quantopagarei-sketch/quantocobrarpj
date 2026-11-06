# Imagens do efeito C06 "Meu amigo secreto"

Este arquivo é para a equipe e para o Montador. O Vini não precisa fazer nada aqui.

Para refazer tudo, rode `python3 gerar.py` (precisa de Python 3, Pillow e numpy; leva cerca de 20 s). Os textos vêm de `../textos.json`. O desenho de cada carta fica no dicionário `ILUSTRA` do script, indexado pelo número da carta. As reservas usam o número 100 + n.

Nenhuma imagem foi feita com IA generativa: tudo é desenho em código mais emoji Noto Color Emoji. Por isso a frase "No generative AI" da nota em inglês do `textos.json` continua valendo.

## O que entra no Effect House

O template é o **Randomizer 2D**, o mesmo do C01. As imagens usam o mesmo quadro do C01, de **512×256** (proporção 2:1), em PNG com fundo transparente.

| Arquivo | Tamanho | Uso |
|---|---|---|
| `titulo_toque.png` | 512×256 | **Padrão.** Título "NO AMIGO SECRETO / EU VOU GANHAR…" com a pílula vermelha "👆 TOQUE PRA ABRIR". Vai no objeto **Title**. |
| `titulo.png` | 512×256 | Reserva: o mesmo título sem a pílula. |
| `cartas/carta_01.png` … `carta_26.png` | 512×256 cada | Os 26 resultados, na ordem do `textos.json`. Entram juntos como **uma** sequência de imagens (Texture Sequence) no objeto **RandomAnimationSequence**, na ordem 01 → 26. A pasta `cartas` contém **só** essas 26 imagens. |
| `icone_162.png` | 162×162, PNG opaco | Ícone do formulário de envio: caixa de presente dourada, laço vermelho e um "?" grande, sobre fundo verde-pinheiro. O desenho fica dentro da área segura de 144×144. |
| `icone_alt_162.png` | 162×162, PNG opaco | 2º ícone (opcional): a caixa aberta, com o "?" saindo e a tampa voando, sobre fundo dourado. |

**Peso:** `titulo_toque.png` mais as 26 cartas somam **2,59 MB** (2.653 KB). Com o `titulo.png` de reserva junto, dá 2,69 MB. A maior peça é a `carta_18.png`, com 110 KB, muito abaixo do limite de 1 MB. Nenhuma imagem passa de 1024 px. A meta da equipe é ficar abaixo de 5 MB, e o pacote cabe com folga.

## O que NÃO entra

| Arquivo | Uso |
|---|---|
| `reservas/reserva_01..05.png` (R1–R5) | Só se alguma carta for vetada. **Troque pelo arquivo:** tire a carta vetada da pasta `cartas` e renomeie a reserva com o número dela (ex.: `reserva_02.png` → `carta_02.png`). Não troque só o texto no `textos.json`, porque o desenho fica preso ao número da carta. |
| `quadrado_512/` | As mesmas peças centralizadas em 512×512. Só para quando o objeto do template não aceitar 2:1. Título e cartas têm que usar a **mesma** versão. |
| `icone_512.png`, `icone_alt_512.png` | Os ícones em tamanho grande, para referência e divulgação. |
| `previa.png` | Folha de conferência com todas as peças, os ícones em 162, 96 e 64 px e a simulação sobre 4 fundos. |
| `gerar.py`, `lista-de-arquivos.txt`, `LEIA-ME.md` | Referência da equipe. |

**Reservas** (o que cada uma substitui está no `textos.json`):

| Reserva | Texto | Entra no lugar de |
|---|---|---|
| R1 `reserva_01.png` | PORTA-RETRATO / SEM FOTO | qualquer carta vetada (1ª opção para a 3 ou a 15) |
| R2 `reserva_02.png` | 10 REAIS NUM / ENVELOPE | carta 2 (TRANSFERÊNCIA DE 10 REAIS) |
| R3 `reserva_03.png` | BOMBONS / (JÁ COMERAM 3) | carta 13 ou 5 |
| R4 `reserva_04.png` | O QUE EU PEDI / (NEM ACREDITO) | carta 10, se "MILAGRE" for vetado. Usa a mesma arte e a mesma cor da carta 10. |
| R5 `reserva_05.png` | CAPINHA QUE / NÃO SERVE | carta 3, 6, 17 ou outra |

A cor de cada reserva já combina com a vizinhança da carta que ela substitui. A única exceção: R5 no lugar da carta 6 deixa duas etiquetas kraft lado a lado (R5 e a carta 7). Isso é só estética e não afeta a revisão.

## Dicas de montagem

- **Régua contra imagem esticada:** o **ilhós** (o furinho dourado na ponta esquerda da etiqueta) tem que ficar redondo. Se virar ovo, a imagem foi esticada. Nesse caso deixe o objeto em 2:1 (ex.: 512 × 256).
- **Mesmo quadro em todas:** a etiqueta, a caixa e o barbante ficam no mesmo lugar no título e nas 26 cartas. No giro, parece que a mesma caixa abre e o conteúdo vai trocando. No título, a caixa aparece fechada com laço. Nas cartas, aberta.
- **Posição:** a borda de baixo da etiqueta fica logo acima da testa ou do cabelo. A largura do objeto deve ser de cerca de **1,6 vez a largura da cabeça**, igual ao C01. Na simulação da `previa.png`, a peça ocupa uns 2/3 da tela.
- **O conjunto não é simétrico, de propósito:** a ponta com o ilhós fica à esquerda, e a caixa e o texto ficam centrados no retângulo da etiqueta, uns 18 px à direita do centro da imagem. Centralize **a imagem** na cabeça, como no C01. A diferença de 18 px não aparece no celular.
- **Ordem da sequência:** os nomes têm zero à esquerda (01…26), então a ordem alfabética já é a certa.
- **Furo de verdade:** o furo do ilhós é transparente, e o fundo do vídeo aparece por ele. Isso não é defeito.

## Identidade visual (para a revisão de duplicidade)

Ela foi pensada para não parecer com os outros sorteios da conta:

| | C01 Torcedômetro | C02 Meu próximo carro | C08 Grupo da família | **C06 Meu amigo secreto** |
|---|---|---|---|---|
| Moldura | ingresso com recortes laterais | etiqueta lisa com faixa de asfalto | balão de fala | **etiqueta de presente**, com ponta chanfrada, ilhós dourado, borda dourada, pesponto tracejado e papel listrado |
| Desenho | emoji numa medalha redonda | carro desenhado "estacionado" | emoji num círculo | **caixa de presente aberta**, com o resultado saindo de dentro e um barbante dourado ligando a etiqueta à caixa |
| Paleta | laranja, violeta, ouro, magenta | amarelo, turquesa, coral, grafite | rosa, azul, roxo, laranja | **verde-pinheiro, dourado, kraft e creme**. O vermelho aparece só no laço, na fita e na pílula |
| Ícone | velocímetro com bola | carrinho com "?" | balões com bonequinhos | **presente com laço e "?"** |

As 4 cores de etiqueta se revezam (pinheiro → dourado → kraft → creme), então nenhuma carta fica ao lado de outra da mesma cor. Nenhuma cor dominante forma par de clube: não há vermelho+branco, verde+branco, preto+branco nem azul.

## Regras respeitadas nos desenhos

- **Nenhuma figura humana:** sem Papai Noel, duende, rosto, mão ou pé. Também não há emoji de carinha: o 🤨 e o 😳 do `textos.json` viraram objetos (cartas 15 e 23). A única mão da peça é o 👆 da pílula "TOQUE PRA ABRIR", igual ao C01.
- **Nada religioso:** os brilhos são estrelinhas de 4 pontas. Não há estrela-guia, anjo, presépio nem vela.
- **Nenhuma marca:** panetone sem caixa e sem embalagem, chocolate sem embalagem (não usei o 🍫 da Noto, que vem com papel vermelho) e celulares genéricos (sem câmera saliente e sem logo). O fone é o 🎧 genérico da Noto, e o chinelo é o 🩴 liso, sem bandeira na tira.
- **Carro:** o aromatizante (carta 4) é **redondo**, nunca de pinheirinho. O porta-celular (11) está preso numa saída de ar genérica, com a **tela apagada**. O volante (21) não tem emblema: o cubo é liso. O carro está sempre parado.
- **Dinheiro:** nota verde genérica com "10" (cartas 2 e R2). Não copia a cédula real e não tem o símbolo nem o nome do Pix.
- **Sem bebida:** os bombons (R3) são redondos e genéricos, sem formato de coração e sem licor.
- **Nenhum nome escrito:** o "bordado" da toalha (12) é um rabisco ilegível.
- As meias (1) foram desenhadas no próprio script, em bege com verde e dourado. O 🧦 da Noto tem listras vermelhas e brancas, que lembram uniforme.
- Emojis Noto usados: ☕ 📣 🕸 🎧 🎵 ❌ 📝 💗 🧼 ☀ 🎯 ✨ 🎁 ♻ 🔌 🪫 🧶 🪑 💨 🪴 🍂 📒 💎 🩴 📏 🎒 🧾 🚫 🌸 👆. Nenhum deles tem texto ou marca.

## Números conferidos (rodada de 06/11/2026)

- Todas as peças têm folga de pelo menos 3 px até a borda da imagem: nada é cortado. A sombra também não encosta na borda.
- Fonte das cartas (Inter Display Black, com 1× a espessura do contorno de espaço extra entre palavras, para não grudar "PEGA DE UM LADO"): **de 41 a 54 px**. As menores são a 25 (SQUEEZE QUE / VAZA NA MOCHILA) e a 26 (PRESENTE SEM / NOTA PRA TROCAR), as duas com 41 px. O mínimo aceito no C01 era 34 px. O tamanho de cada carta está no `previa.png`.
- Glifos conferidos na fonte: ° (grau, na carta 9), º (ordinal, na carta 8), “ ” (carta 7) e … (título). Nenhum faltou.

## A confirmar

- Se a importação da Texture Sequence respeita a ordem pelo nome (deve respeitar; foi assim no C01).
- Se o app mostra o 2º ícone (`icone_alt_162.png`). Se não mostrar, basta o principal.
