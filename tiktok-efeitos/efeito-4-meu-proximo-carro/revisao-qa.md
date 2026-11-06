# Revisão de QA: Meu próximo carro (C02)

**Data:** 06/11/2026 · **Revisor:** Controle de Qualidade · **Nota:** 9/10 · **Resultado:** pronto para montar. Antes, a coordenação precisa publicar os arquivos (push) e passar o C02 de "Vem aí" para a tabela da seção 2 do `PRONTO-PARA-MONTAR.md`. O envio continua travado até sair a decisão do desafio, como manda o guia na Parte 12.1.

## O que foi conferido

| Item | Resultado |
|---|---|
| Arquivos citados no `guia-montagem.md` existem em `assets/` | OK: `titulo_toque.png`, `titulo.png`, 26 cartas em `cartas/` (a pasta só tem as cartas), 4 reservas, `quadrado_512/` completa, os 2 ícones em 162 e em 512, `previa.png`, `LEIA-ME.md`, `lista-de-arquivos.txt`, `gerar.py` e `script/prompt-effect-house-ai.md` |
| Dimensões | OK: título e cartas em 512×256 RGBA, quadradas em 512×512, ícones em 162×162 RGB opaco, com o desenho dentro da área segura de 144 (conferido na `previa.png`) |
| Peso | OK: a maior carta é a `carta_24.png`, com 103 KB (limite de 1 MB). `titulo_toque` + 26 cartas = 2,43 MB em PNG. O C01 tinha 2,15 MB em PNG e virou um pacote de 1,6 MB, então o C02 deve ficar perto de 2 MB, longe do limite de 5 MB (a confirmar no Effect House) |
| Imagens abertas uma a uma | `previa.png`, `icone_162`, `icone_alt_162`, `titulo_toque` e as cartas 01, 02, 06, 08, 09, 11, 13, 16, 21, 22, 24 e 26 (as outras foram vistas na prévia). Nenhum texto cortado e nenhum erro de acento (Ó, Ã, Ç, Â, É, Í, Ô estão certos). A menor fonte é de 47 px, nas cartas 09, 21, 26 e na R3, acima do mínimo de 34 px. O amarelo dos parênteses dá para ler nas etiquetas grafite, turquesa e coral |
| Marca, modelo, celebridade, time, "Pix" | Nada nas imagens nem nos textos. Os carros são vetores próprios, sem grade, emblema ou placa. O aromatizante é uma gota, não um pinheirinho. O adesivo da família não tem peixinho nem time. A paleta não forma par de cores de clube. "SUV", "1.0", "app", "consórcio" e "agro" são palavras genéricas |
| Português | Natural e atual, sem gênero marcado. O título continua a frase em todas as cartas, menos na 16 (corrigida, veja abaixo) |
| Data de envio | Até ter 17/11/2026, que é mesmo terça. Seg 16/11, dom 22/11, qui 26/11 e qua 02/12 e 09/12 também conferem no calendário |
| Campos de envio | Batem com a regra do formulário 5.16 (atualização de 06/11, 05:50 UTC): nome, Create icon, hint de lista, sem som, Challenge conforme a decisão, Trend vazio e demo. O nome tem 17 caracteres e as alternativas, 21 e 19. Os textos opcionais (descrição e nota para a revisão) estão colados por inteiro no guia |
| Referências cruzadas do guia | Conferidas no guia do C01: Partes 5.1, 5.2, 7.3, 9 e 10, e Plano C nos passos 1 a 19. Os campos do script (Sequencia Cartas, Tempo Giro, Tempo Some Titulo, Girar De Novo No Toque) existem no `TorcedometroController.ts`. Os Pedidos 1 a 4 existem em `script/prompt-effect-house-ai.md` |
| `gerar.py` | É determinístico: rodado de novo sem mudança, gera as mesmas imagens. Depois da correção, o git mostra que só mudaram `carta_16` (as duas versões), `previa.png` e `lista-de-arquivos.txt` |
| Originalidade | O sorteio sobre a cabeça e o tema "que carro você vai ter" são formatos comuns. Os 26 textos, os desenhos, a moldura de etiqueta com asfalto e o ícone são próprios, e o visual é bem diferente do Torcedômetro. O nome é uma frase comum (busca no app a confirmar, já no guia) |

## Correções feitas

1. **Carta 16:** "SOM VALE MAIS / QUE O CARRO" virou **"COM SOM MAIS / CARO QUE ELE"**. Era a única carta que não continuava o título ("Meu próximo carro vai ser… som vale mais que o carro" não fecha a frase). Agora fica "Meu próximo carro vai ser… com som mais caro que ele". O desenho continua o mesmo. Atualizei `textos.json` (v1.1, registrado em `trocas_feitas_no_conceito`), `textos.md`, a tabela 0.6 do guia, o banco de reações do `lancamento.md` e o comentário da `cena_16` no `gerar.py`, e rodei o `gerar.py` de novo.
2. **Peso no guia e no `LEIA-ME.md`:** o maior arquivo passou a ser a `carta_24.png`, com 103 KB. O valor esperado no comando da 0.4 virou ~105000, e o total ficou em 2,43 MB (2.484 KB).
3. **Guia, 11.2:** a lista de nomes esperados em Manage Effects incluía "Meu 2027 vai ser", que só é enviado em 03/12. Corrigi. A versão do guia subiu para 1.1.
4. **`lancamento.md`, 4.4 e 5.2:** a resposta pronta "Tem na vitrine do perfil 😉", nos comentários do vídeo do efeito, contradizia a regra do próprio plano ("nada de 'tem na loja' no vídeo do efeito") e arriscava o vídeo ser lido como conteúdo comercial sem aviso. Ela virou "Te chamo no direct 😉", e o produto só é falado na mensagem direta. Se a mensagem direta não funcionar pela web, a equipe só curte o comentário.
5. **`lancamento.md`, seção 2:** o texto dizia que os 3 momentos do Vini têm ~10 min cada. No `LEIA-PRIMEIRO.md`, o de 29/11 tem ~5 min e é do Meu amigo secreto. Agora o texto diz isso e avisa que a fatia do C02 nesse dia depende do coordenador.

## Riscos que continuam (baixos, a não ser o primeiro)

- **Duplicidade, risco médio:** C08, C01 e C02 usam o mesmo template e a mesma lógica, e o guia trata o C02 como "o Torcedômetro com outras imagens". A pesquisa não achou regra explícita contra isso (pesquisa 02, linha "efeitos duplicados": ❓). O visual, os textos e o tema são outros. Se o efeito voltar com "duplicado", o guia (Parte 15) manda parar e avisar a nuvem, o que está certo.
- A **carta 16** tem um 💰 com "$", e a **carta 08** tem uma bala vermelha e branca. As reservas estão prontas (Parte 16).
- **CAMINHONETE DO AGRO** e **CARRO DE APP**: os desenhos estão genéricos. A R2 e a R1 servem de reserva.
- Os menus do Effect House e os nomes dos campos ainda estão "a confirmar na sua versão", e o guia marca cada um.
- Os convites a criadores (`lancamento.md`, seção 7) começam com "Aqui é o Vini, da Car Shop". É só o nome da conta, sem produto nem vantagem, então o risco é baixo.

## Pendências

- **Coordenação:** publicar os arquivos e liberar o C02 na seção 2 do `PRONTO-PARA-MONTAR.md`. O guia exige isso no pré-requisito 1.
- **Vini:** só a decisão que já está pendente sobre o desafio "Nov Social Randomizer Sub Challenge". A mesma decisão vale para C01, C02 e os outros sorteios. Fora isso, ninguém precisa chamá-lo para o C02.
