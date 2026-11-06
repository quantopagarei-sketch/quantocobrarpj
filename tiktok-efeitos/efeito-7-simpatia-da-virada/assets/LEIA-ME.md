# Imagens do efeito C07 "Simpatia da Virada"

Para a equipe e o Montador. O Vini não precisa fazer nada aqui.

Para refazer tudo: `python3 gerar.py` (Python 3 + Pillow + numpy, leva uns 20 s). Os textos vêm de `../textos.json`. O desenho de cada carta está no dicionário `ILUSTRA` do script, pelo número da carta. Os campos `extras_desenho` do JSON (`tint_main` na carta 24 e `tint_secundario` na carta 5) são lidos e aplicados. Antes de desenhar, o script confere se a fonte tem todos os caracteres (À, º, …), e para com erro se faltar algum.

## O que entra no Effect House

É o mesmo template do C01 (Randomizer 2D), com o mesmo quadro de **512×256** (2:1) e o bilhete no mesmo lugar do ingresso do C01.

| Arquivo | Tamanho | Uso |
|---|---|---|
| `titulo_toque.png` | 512×256, PNG com transparência | **Padrão.** Título "MINHA SIMPATIA / PRA 2027 É…" com a pílula dourada "👆 TOQUE NA TELA". Vai no objeto **Title**. |
| `titulo.png` | 512×256 | Reserva: o mesmo título, sem a pílula e com letra maior. |
| `cartas/carta_01.png` … `carta_26.png` | 512×256 cada | Os 26 resultados, na ordem do `textos.json`. Entram juntos como **uma** sequência de imagens (Texture Sequence) no objeto **RandomAnimationSequence**, na ordem 01 → 26. |
| `icone_162.png` | 162×162, PNG opaco | Ícone do formulário de envio: cacho de uva com fogos dourados, rosa e verde-água, num fundo roxo-uva escuro. Não tem texto. O cacho fica entre 21 e 147 px, dentro da área segura (9 a 153). |
| `icone_alt_162.png` | 162×162, PNG opaco | 2º ícone (opcional): uva e relógio marcando meia-noite, num fundo ameixa. |

**Peso:** `titulo_toque.png` + 26 cartas = **2,62 MB**. Com o `titulo.png` de reserva, **2,72 MB**. O limite da equipe é 5 MB. A maior carta é a `carta_06.png`, com 107 KB (o limite é 1 MB), e nenhuma imagem passa de 1024 px. Os tamanhos de cada arquivo estão em `lista-de-arquivos.txt`.

## O que NÃO entra

| Arquivo | Uso |
|---|---|
| `reservas/reserva_01..04.png` (R1–R4) | Só se alguma carta for vetada (veja a tabela "entra no lugar de" no `textos.json`). **Troque pelo arquivo:** tire a carta vetada da pasta e renomeie a reserva com o número dela (ex.: `reserva_04.png` → `carta_01.png`). Não troque só o texto no JSON, porque o desenho fica preso ao número da carta. |
| `quadrado_512/` | As mesmas imagens centralizadas em 512×512. Só para o caso de o objeto do template não aceitar 2:1. Título e cartas têm que usar a **mesma** versão. |
| `icone_512.png`, `icone_alt_512.png` | Os ícones em tamanho grande, para referência e divulgação. |
| `previa.png` | Folha de conferência com todas as peças, os ícones em 162/96/64 px e a simulação sobre 4 fundos: sala clara, noite com fogos, praia de dia e confete. |
| `gerar.py`, `lista-de-arquivos.txt`, `LEIA-ME.md` | Referência da equipe. |

## Dicas de montagem

- **Régua contra imagem esticada:** o **selo dourado ondulado** no alto de cada peça tem que ficar redondo. Se virar ovo, a imagem está esticada; deixe o objeto em 2:1 (ex.: 512 × 256), como no C01.
- **Mesmo quadro em todas:** o bilhete ocupa o mesmo lugar no título e nas 26 cartas, então a troca não "pula".
- **Posição e tamanho:** iguais aos do C01. Largura do objeto ≈ **1,6 vez a largura da cabeça**. A borda de baixo do bilhete fica logo acima da testa. Na `previa.png`, a peça ocupa uns 2/3 da largura da tela.
- **Ordem da sequência:** os nomes têm zero à esquerda (01…26), então a ordem alfabética já é a certa. Se o Effect House ordena a sequência pelo nome é algo a confirmar na versão instalada, como no C01.

## Identidade visual (para a revisão de duplicidade)

A ideia foi não parecer nenhum dos outros sorteios da conta (C01 ingresso laranja/violeta, C02 etiqueta com asfalto, C08 balão de fala colorido) nem o C05 (bolhas brancas), que é enviado no mesmo dia:

- **Formato:** bilhete de desejo com borda dourada, **pontas dobradas** (canto de cima à esquerda e de baixo à direita), pontilhado dourado por dentro e **selo dourado ondulado** com o desenho.
- **Cores:** céu da meia-noite escuro, em 3 tons que se alternam no giro (uva, ameixa e anil). O texto é branco com contorno quase preto, e o **trecho entre parênteses (a piada) sai em dourado**. O confete é dourado, rosa e verde-água, com fogos pequenos nos cantos de cima. Nenhum par de cores de clube.
- **Desenhos:** a maioria é emoji Noto (licença OFL 1.1), com um adesivo secundário. Alguns são desenhos próprios:
  - **cacho de uva** do título e dos ícones;
  - **romã** da carta 9 (não existe emoji de romã);
  - **moeda dourada sem valor**, só com uma estrela, na carta 21;
  - **seta verde** da carta 19, porque a seta Noto é um botão cinza quadrado;
  - **estrela cadente** da carta 26, porque o emoji Noto vem num quadrado escuro;
  - **relógio da meia-noite** do ícone alternativo;
  - **montinho de lentilha** na tigela da carta 3 e **uva-passa** no arroz da carta 22.
- **Regras conferidas nos desenhos:**
  - nada religioso: sem flores no mar, vela, oferenda, guia ou santo;
  - nada de bebida nem rolha;
  - fogos só no céu, e ninguém segurando;
  - roupa íntima não aparece (a carta 12 usa só a carinha de "psiu" e um coração amarelo);
  - cadeira parada (carta 4);
  - carro genérico parado, sem placa nem logo (carta 18);
  - camiseta lisa recolorida em coral e tênis sem listra;
  - dinheiro só como saquinho e moeda genérica, sem cédula de real;
  - nenhuma marca.
