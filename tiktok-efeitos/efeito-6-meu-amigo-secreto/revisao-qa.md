# Revisão de QA: Meu amigo secreto (C06)

**Data:** 06/11/2026 · **Revisor:** Controle de Qualidade · **Resultado:** pronto para montar, depois que a coordenação fizer duas coisas: (1) publicar os arquivos (as imagens do C06 ainda estão fora do git) e (2) pôr o C06 na tabela da seção 2 do `PRONTO-PARA-MONTAR.md`, com "enviar entre 20/11 e 24/11". **Enviar nunca antes de sex 20/11/2026.**

## O que foi conferido

| Item | Resultado |
|---|---|
| Arquivos citados no `guia-montagem.md` existem em `assets/` | OK: `titulo_toque.png`, `titulo.png`, `cartas/carta_01..26.png` (a pasta tem só as 26), `reservas/reserva_01..05.png`, `quadrado_512/` (título, 26 cartas, 5 reservas), `icone_162.png`, `icone_alt_162.png` e as versões em 512 |
| Dimensões | OK: título, cartas e reservas 512×256 RGBA; quadradas 512×512 RGBA; ícones 162×162 (opacos) e 512×512 de referência |
| Peso | OK: maior peça `carta_18.png`, 112.268 bytes (~110 KB; limite 1 MB). `titulo_toque` + 26 cartas = 2.716.391 bytes (2,59 MB em PNG; meta de 5 MB). A `previa.png` tem 3 MB, mas não entra no efeito |
| Corte | OK: área com desenho de x 5–506 e y 3–248 em todas as cartas e reservas (título: y 8–248). Nada encosta na borda |
| `gerar.py` reproduz os arquivos | OK: rodei uma cópia no scratchpad. Os 71 PNG saíram **idênticos, byte a byte**, e a `lista-de-arquivos.txt` também. As fontes por carta (41 a 54 px) batem com a tabela 0.7 do guia |
| Imagens abertas uma a uma | `previa.png`, os 2 ícones (com a área segura sobreposta), `titulo_toque` e as cartas 02, 04, 06, 07, 09, 10, 11, 12, 13, 15, 17, 21, 23, 25 e 26. Todas legíveis, sem corte, com acentos, °, º, aspas curvas e "…" certos. O espaço entre as palavras aparece ("PEGA DE UM LADO"). O texto creme com contorno marrom é legível nas etiquetas douradas |
| Ícones | OK: o desenho fica dentro de 144×144. No `icone_alt`, só um tracinho de movimento passa da linha, e cortá-lo não atrapalha. Pela ordem de 06/11, o ícone sai do Create icon; os PNG são o plano de exceção |
| Português | Natural e atual. "Dois números menor" é coloquial e correto. Nada ofensivo; a graça é a situação, não quem deu o presente |
| Marca, time, celebridade, modelo de carro | Nada, nem "Pix" (virou "TRANSFERÊNCIA DE 10 REAIS", sem losango e sem banco). Busquei Pix, bancos, marcas de panetone, chocolate, chinelo e celular, lojas, montadoras e times em todos os textos. Só aparecem dentro de regras do tipo "não pode". Aromatizante redondo, volante sem emblema, celular de tela apagada, fone com fio genérico, chocolate sem embalagem |
| Regras de conteúdo | Sem Papai Noel e sem figura humana (a única mão é o 👆 da pílula, como no C01, e a reserva `titulo.png` já está pronta). Nada religioso (brilhos de 4 pontas). Sem bebida. Sem link, CTA ou loja no efeito |
| Guia seguível por agente | Sim. Caminhos reais, comandos PowerShell conferidos (o CSV de hash dá 56 = 28 × 2), ordem 01→26 com 1º e último quadro descritos, régua do ilhós, casos A/B/T/S, plano alternativo com os nomes reais do C02 (`carro_titulo`, `cartas_carro`, conferidos no guia do C02) e campos do script iguais aos do `TorcedometroController.ts` |
| Data de envio | OK: sex 20/11 a ter 24/11/2026, "nunca antes de 20/11", na Parte 0.2, na 13.1, no resumo, no `textos.md`, no `lancamento.md` e no `plano-curto-prazo.md`. Conferi os dias da semana de todas as datas (20/11 sex, 24/11 ter, 29/11 dom, 30/11 seg, 17/12 qui, 19/12 sáb...) |
| Campos de envio | Preenchidos com os textos reais (nome de 17 caracteres, alternativas de 23 e 25, hint, sem som, trend vazio, demo; descrição de 259 caracteres e nota em inglês de 414 caracteres, se os campos aparecerem). Contagens conferidas |
| `lancamento.md` | Sem incentivo ("amigo secreto com os seguidores", brinde, cupom e "os melhores eu reposto" estão proibidos). Venda separada do vídeo do efeito, afiliados fora dos convites, divulgação comercial só no vídeo da loja. Links do Vini completos (lojas do app). Plano mínimo de ~5 min dentro de um momento que já existe |
| Originalidade | Busca na web (06/11) não achou efeito de amigo secreto famoso. "Sorteio do que você vai ganhar" é uma mecânica genérica de Natal. O nome, as 26 frases e a arte (etiqueta de presente com ilhós, paleta pinheiro, dourado, kraft e creme) são próprios e diferentes dos outros sorteios da conta |

## Correções feitas

1. **Guia, Parte 13.2 (desafio):** havia uma ambiguidade. A ordem de 06/11, 05:50, do `PRONTO-PARA-MONTAR.md` diz "não faça o Submit até sair a decisão do Vini", e o guia diz "se o PRONTO disser outra coisa, vale ele". Lido ao pé da letra, o Montador podia segurar o C06 para sempre e perder a gravação de 29/11. Entrou uma linha explicando que, para o C06, essa ordem é cumprida pela espera até 24/11, 12h. Só vale outra regra se o PRONTO tiver uma linha com o nome do C06. A versão do guia subiu para 1.1.
2. **`lancamento.md`, checklist 9:** o item "tem na loja… no vídeo do efeito" contradizia a resposta permitida "Tem na vitrine do perfil 😉" (seções 4.5 e 5.2). Agora diz onde a regra vale (fala, texto de tela, legenda e fixado) e que a exceção é só a resposta a quem perguntar, nunca no fixado.
3. **`lancamento.md`, 6.3:** "a janela de 30 dias do envio vai até ~24/12" estava errado: a janela conta da publicação, não do envio. Corrigido para "da aprovação, entre 24 e 27/12 (a confirmar)".
4. **`textos.md`:** dizia que a menor fonte era 44 px (medida no layout do C01). Na arte final, ela é 41 px (cartas 25 e 26). A nota foi acrescentada. Também entrou, no topo da seção 4, o aviso de que o formulário 5.16 não tem descrição, categoria e tags, e que vale a Parte 13.4 do guia.
5. **Imagens:** nada a corrigir. O `gerar.py` não foi rodado na pasta, porque a saída seria idêntica.

## Riscos que continuam

- **Duplicidade (o principal):** C01, C02, C06, C07 e C08 saem do mesmo template, na mesma conta. A arte do C06 é bem diferente, e o guia (12.2) manda **não enviar** se algum irmão voltar com "duplicado" ou "spam". Médio-baixo.
- **Cartas sensíveis, com reserva pronta:** 02 (transferência → R2), 10 ("milagre" → R4), 15 (desodorante, piada leve de corpo → R1), 03 (coach → R5). Nenhuma delas entra no demo nem no ícone. Baixo.
- **👆 na pílula do título:** é a mesma do C01. A troca para o `titulo.png` está no guia (Parte 16). Baixo.
- **"Tem na vitrine do perfil" nos comentários do vídeo do efeito:** é uma ponte leve para a loja. Está limitada a quem perguntar. Baixo.
- **Menus do Effect House:** a confirmar na versão instalada. O guia marca cada um.

## Pendências

- **Coordenação:** fazer commit e push das imagens do C06 (hoje estão como não rastreadas no git; sem isso, o zip do Montador vem sem `assets`). Pôr o C06 na seção 2 do `PRONTO-PARA-MONTAR.md`, com a janela 20–24/11 e, se possível, a regra do desafio escrita para o C06.
- **Vini:** a mesma decisão pendente do desafio "Nov Social Randomizer Sub Challenge" (aceitar ou não os termos). Se não decidir até 24/11, 12h, o C06 vai sem desafio. Nada mais depende dele até a gravação de 29/11.
