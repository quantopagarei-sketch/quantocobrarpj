# Imagens do efeito C08 "Eu no grupo da família"

Para a equipe e o Montador. O Vini não precisa fazer nada aqui.

Para refazer tudo: `python3 gerar.py`. O script lê os textos de `../textos.json`; se uma frase mudar lá, é só rodar de novo.

## O que entra no Effect House

| Arquivo | Tamanho | Uso |
|---|---|---|
| `titulo.png` | 512×512, PNG com transparência | Textura do objeto **Title** do Randomizer 2D ("NO GRUPO DA / FAMÍLIA, EU…"). |
| `cartas/opcao_01.png` … `opcao_28.png` | 512×512 cada, PNG com transparência | As 28 cartas do sorteio. Vão como **texture sequence** no objeto **RandomAnimationSequence**, na ordem 01 → 28. |
| `icone_162.png` | 162×162, PNG opaco | Ícone do formulário de envio (campo obrigatório). O desenho fica dentro da área segura 144×144. |
| `icone_alt_162.png` | 162×162, PNG opaco | 2º ícone (opcional; o formulário aceita até 2). É a mesma arte com fundo escuro. |

## O que NÃO entra

| Arquivo | Uso |
|---|---|
| `reservas/reserva_01..03.png` (512×512) | Só se alguma frase for vetada. O jeito certo é trocar a frase no `textos.json` e rodar `python3 gerar.py`, que mantém a alternância de cores. Às pressas, dá para renomear a reserva com o número da carta vetada (ex.: `reserva_02.png` → `opcao_15.png`). |
| `icone_grande_512.png` | O mesmo ícone em tamanho grande, só para referência e divulgação. |
| `previa.png` | Folha de conferência (contato + simulação sobre fotos). |
| `gerar.py` | Script que gera tudo. |

## Dicas de montagem

- **O título e as cartas usam o mesmo quadro de 512×512.** O balão ocupa o mesmo lugar em todos, então a troca entre título e resultado não "pula". Mantenha o objeto com proporção 1:1, sem esticar.
- **O rabicho do balão aponta para a cabeça.** A ponta fica a cerca de 90% da altura da imagem (y ≈ 459 de 512) e o resto embaixo é margem transparente. Posicione o objeto para a ponta ficar logo acima da testa ou do cabelo.
- **Tamanho sugerido:** largura do objeto ≈ 1,5 vez a largura da cabeça (ajustar olhando nos 3 rostos do Preview).
- **Versão de 2 rostos:** usa as mesmas imagens. Duplique Title e RandomAnimationSequence e aponte o 2º Face Sticker para o rosto 1 (Which Face). Na simulação da `previa.png`, com 2 rostos, cada carta tem cerca de 70% do tamanho da versão de 1 rosto e as duas não se encostam.
- **Peso:** título + 28 cartas somam cerca de 3,0 MB em PNG (cada um tem menos de 120 KB). A meta da equipe é ≤ 5 MB no efeito; conferir o número real no indicador de tamanho da barra de título (a confirmar). Se passar, a primeira opção é compressão Manual 512 + Medium só nas cartas.
- **Ordem da sequência:** os nomes têm zero à esquerda (01…28), então a ordem alfabética é a ordem certa. Ainda falta confirmar no app se o import aceita a pasta inteira ou se é preciso selecionar os 28 arquivos (a confirmar).

## Regras de originalidade respeitadas

- Os balões têm rabicho centralizado, no estilo de quadrinho, e nenhum tem cor ou formato de app de mensagem (nada de verde, tique de "lida", fundo bege ou logo).
- Paleta: rosa, roxo, laranja e azul-céu, em ordem alternada, para o giro ficar colorido.
- Fonte: Inter Display Black (licença OFL). Emojis: Noto Color Emoji (licença OFL). O pictograma de família do título e do ícone é um desenho próprio.
