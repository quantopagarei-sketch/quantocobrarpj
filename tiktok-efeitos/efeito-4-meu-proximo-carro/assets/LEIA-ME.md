# Imagens do efeito C02 "Meu próximo carro"

Para a equipe e o Montador. O Vini não precisa fazer nada aqui.

Para refazer tudo: `python3 gerar.py` (Python 3 + Pillow + numpy). Os textos vêm de `../textos.json`. O desenho de cada carta está no próprio script, na função `cena_NN` com o número da carta.

## O que entra no Effect House

O template é o mesmo do C01 (Randomizer 2D), e as imagens têm o mesmo quadro de **512×256** (2:1).

| Arquivo | Tamanho | Uso |
|---|---|---|
| `titulo_toque.png` | 512×256, PNG com transparência | **Padrão.** Título "MEU PRÓXIMO / CARRO VAI SER…" com a pílula "👆 TOQUE NA TELA". Vai no objeto **Title**. |
| `titulo.png` | 512×256 | Reserva: o mesmo título sem a pílula. |
| `cartas/carta_01.png` … `carta_26.png` | 512×256 cada | Os 26 resultados, na ordem do `textos.json`. Entram como **uma** sequência de imagens (Texture Sequence) no objeto **RandomAnimationSequence**, na ordem 01 → 26. |
| `icone_162.png` | 162×162, PNG opaco | Ícone do formulário de envio: carrinho turquesa com "?" coral, fundo amarelo e estrada. O desenho fica dentro da área segura 144×144. |
| `icone_alt_162.png` | 162×162, PNG opaco | 2º ícone (opcional): versão noite, com carrinho coral e "?" amarelo. |

**Peso:** `titulo_toque.png` + 26 cartas = **2,43 MB** (2.484 KB). Com o `titulo.png` de reserva junto, 2,52 MB. O maior arquivo é a `carta_24.png`, com 103 KB, bem abaixo do limite de 1 MB. Nenhuma imagem passa de 1024 px.

## O que NÃO entra

| Arquivo | Uso |
|---|---|
| `reservas/reserva_01..04.png` (R1–R4) | Só se alguma carta for vetada. **Troque pelo arquivo**: mova a carta vetada para fora e renomeie a reserva com o número dela (ex.: `reserva_01.png` → `carta_24.png`). Não troque só o texto no `textos.json`, porque o desenho fica preso ao número da carta e a carta nova sairia com o desenho antigo. |
| `quadrado_512/` | As mesmas imagens centralizadas em 512×512. Só se o objeto do template não aceitar 2:1. Título e cartas têm que usar a **mesma** versão. |
| `icone_512.png`, `icone_alt_512.png` | Os ícones em tamanho grande, para referência e divulgação. |
| `previa.png` | Folha de conferência: todas as peças, os ícones em 162/96/64 px e a simulação sobre 4 fundos. |
| `gerar.py`, `lista-de-arquivos.txt`, `LEIA-ME.md` | Referência da equipe. |

## Dicas de montagem

- **Régua contra imagem esticada:** no título, o **círculo amarelo do "?"** tem que ficar redondo. Nas cartas, valem as **rodas** dos carros. Se virarem ovo, a imagem está esticada: deixe o objeto em 2:1 (ex.: 512 × 256).
- **Mesmo quadro em todas:** a etiqueta ocupa o mesmo lugar no título e nas 26 cartas, então a troca não "pula". Só o desenho de cima muda de largura.
- **Posição:** a borda de baixo da etiqueta (a faixa de asfalto) fica logo acima da testa ou do cabelo. Largura do objeto ≈ **1,6 vez a largura da cabeça**, igual ao C01. Na simulação da `previa.png`, a peça ocupa uns 2/3 da tela.
- **Ordem da sequência:** os nomes têm zero à esquerda (01…26), então a ordem alfabética já é a certa.

## Identidade visual (para a revisão de duplicidade)

Pensada para não parecer o Torcedômetro (C01), que usa o mesmo template:

| | C01 Torcedômetro | C02 Meu próximo carro |
|---|---|---|
| Moldura | ingresso com recortes laterais | etiqueta arredondada lisa, com **faixa de asfalto e tracejado amarelo** embaixo |
| Desenho | emoji dentro de uma medalha redonda no topo | **desenho vetorial próprio "estacionado"** na borda de cima, com contorno branco de adesivo |
| Paleta | laranja, violeta, ouro, magenta | **amarelo de faixa, turquesa, coral e grafite** |
| Ícone | velocímetro com bola, fundo roxo e laranja | **carrinho com "?"** em fundo amarelo, com estrada |

As cores se alternam: nenhuma carta vizinha repete a cor, e as cartas com "(…)" nunca caem na etiqueta amarela, onde o destaque amarelo do parêntese não apareceria.

## Regras respeitadas nos desenhos

- **Os carros são desenhados no próprio script**, em vetor simples: hatch, SUV, rebaixado, sedã antigo de 3 volumes, caminhonete e carro coberto. Todos de lado e parados, **sem grade, logo, emblema nem placa**, e sem silhueta de modelo real. Os faróis são só uma bolinha.
- Nada sugere velocidade: sem chama, número de corrida, fumaça ou risco de movimento. As faíscas da carta 03 saem do carro raspando numa lombada.
- Carta 08 (carro de app): carro prata, sem logo, pino ou cores de app.
- Carta 24: o aromatizante é uma **gota**, nunca pinheirinho.
- Carta 06: os bonequinhos são pai, mãe, filho e cachorro, de palito e sem símbolo nenhum. O vidro é de **traseira sem placa**.
- Carta 20: usei o calendário 🗓 sem texto. O 📅 da Noto tem "July" escrito, por isso ficou de fora.
- Carta 16: o 💰 da Noto tem um "$" (símbolo genérico de moeda, sem banco nem marca). Se a revisão implicar, dá para trocar por outro emoji na `cena_16` e rodar de novo.
- Carta 12: documento genérico (📄), sem brasão nem placa.
- **Fontes:** Inter Display Black (OFL 1.1). **Emojis:** Noto Color Emoji (OFL 1.1), os mesmos do C01. Nada de IA generativa.
