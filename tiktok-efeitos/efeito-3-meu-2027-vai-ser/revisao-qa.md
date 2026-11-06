# Revisão de QA: Meu 2027 vai ser (C05)

**Data:** 06/11/2026 · **Revisor:** Controle de Qualidade · **Resultado:** o efeito está pronto para montar depois que a coordenação publicar os arquivos (push + `PRONTO-PARA-MONTAR.md`) e disser se ele é da situação A ou B. O envio só acontece em dezembro.

## O que foi conferido

| Item | Resultado |
|---|---|
| Arquivos citados no `guia-montagem.md` existem em `assets/` | OK: titulo, 4 rótulos, 30 respostas, 8 reservas, variantes com_sombra, quadrado_512, quadrado_512_com_sombra, bolha_inteira (com bolha_vazia), rotulos_sem_icone e 2 ícones |
| Dimensões | OK: título 1024×512, rótulos 512×256, respostas e reservas 512×128 (RGBA), quadradas 512×512, ícones 162×162 (opacos, desenho dentro da área de 144×144) |
| Peso | OK: 429 KB para as 4 bolhas na versão principal. Nenhum arquivo do efeito passa de 125 KB (limite de 1 MB) |
| Texto nas imagens (prévia, ícones, título, rótulos, amor_03, amor_06, grana_02, futebol_03, futebol_08, carro_02 e grana_02 com sombra) | Legível, sem corte, com acentos e Ç certos. O "º" de 13º sai como um "o" pequeno elevado, que é o desenho da fonte Inter, e lê-se bem |
| Português | Natural e atual, sem erro. Frases curtas, de humor leve, sem nada ofensivo |
| Marca, time, celebridade | Nada no efeito. A bola, a moeda com "$" e o carro de lado são desenhos genéricos. Não há par de cores de clube. "Pix" foi tirado |
| Regras do programa | A IA generativa do template (Pucker e Unhappy) é apagada na Parte 6, o que evita o nome com "AI", o problema de FPS e a regra "IA não é elegível". O lançamento não tem prêmio, cupom, conta extra nem grupo de troca |
| Originalidade | A base é o template oficial Future Life, que o TikTok oferece para isso. As 24 frases em português, o título, os rótulos e o ícone são próprios. Se der, a bolha própria (Parte 5.4) afasta ainda mais do visual padrão |
| Datas do lançamento | Conferidas no calendário de 2026: 12/12 é sábado, 18/12 é sexta (13º antecipado porque o dia 20 cai no domingo), 24/12 é quinta e 25/12 é sexta |
| Teste de sorteio (Parte 8.3) | A conta confere: em 24 rodadas saem em média 7,7 respostas diferentes. A chance de a 8ª não sair em 40 rodadas é de ~0,5%, ou seja, cerca de 1 em 200 |
| "Mouth Pout" (biquinho) | Confirmado na página oficial do nó Facial Movement Detection, que lista Mouth Pout entre as opções |
| Estrutura do template | Confirmada no tutorial oficial do Future Life: Bubble_Titles (Lover, Income, Kids), Generative Effects (Pucker e Unhappy), 3 nós Animated Texture Player no subgrafo Color_Picker & Randomizer, artes brancas |
| Script TS (Plano C) | A lógica está coerente e o guia já avisa que ele não foi rodado no Effect House |

## Correções feitas

1. **Guia, Parte 0.2 e Parte 12.4 (o mais importante):** o guia mandava enviar "entre 01/12 e 08/12" e o `lancamento.md` dizia que, na situação A, o envio só pode vir depois da admissão no programa. O Montador seguiria o guia e enviaria antes, e aí o efeito nunca renderia. Agora o guia tem a exceção: na situação A, só envia depois que a aba Rewards mostrar a inscrição aprovada. Se isso não sair até 15/12, ele avisa a equipe. A versão do guia passou para 1.1.
2. **Guia, Parte 4.2, passo 3:** "Import → Texture Sequence" estava como certo. O nome do menu não foi confirmado, e agora está marcado como (a confirmar), apontando para a solução da Parte 15.
3. **`textos.md` e `textos.json` (v1.1):** o arquivo do ícone era citado como `icone.png`, que não existe. Agora é `icone_162.png` (e `icone_alt_162.png`). O texto em inglês para quem revisa dizia "original art", mas a animação das bolhas vem do template. Agora ele fica igual ao do guia: título, rótulos e ícone são nossos, a animação é do template, e não há IA generativa. A contagem de caracteres foi atualizada. O `gerar.py` rodou de novo sem erro (as frases não mudaram).
4. **`lancamento.md`:** entrou a seção 2.0, "Plano mínimo". O plano completo pede ao Vini duas gravações (~35 min e ~15 min na véspera de Natal) e um toque em "Publicar" em vários dias, o que passa do que ele pediu. Agora a equipe pergunta uma vez só. Se ele não responder, vale o mínimo: ~10 min de gravação (Roteiros 1-A, 3-A e Reserva 1), agendados se der. A rodada da família, as respostas em vídeo e as costuras ficam canceladas.

## Riscos que continuam (baixos ou médios)

- **Médio: a revisão achar o efeito "igual ao template".** O Future Life é muito usado. O que protege são as frases em português, a arte própria e, se der, a bolha própria. O guia já tem a resposta pronta para um "Needs revision" desse tipo.
- **Médio: tirar a IA do template quebrar o estouro.** O tutorial oficial diz que os efeitos Pucker e Unhappy ficam numa pasta própria e ligados às expressões do rosto. O guia testa primeiro desligar, depois apagar, e proíbe enviar com a IA dentro (Parte 6.4).
- **Baixo: o ícone principal** usa um degradê roxo, rosa e laranja que lembra de longe o de uma rede social conhecida. Não tem câmera nem marca. Se a revisão implicar, o `icone_alt_162.png` (fundo escuro) resolve.
- **Baixo:** "LIMPA O NOME" fala de dívida e "SECA O RIVAL" é zoeira de torcida. As duas têm reserva pronta.
- Menus do Effect House a confirmar na versão instalada. O guia marca cada um.

## Pendências para a coordenação (não são do Vini)

1. Decidir se o C05 é da situação A ou B e escrever isso no `PRONTO-PARA-MONTAR.md`, junto com a data de envio.
2. O envio é em dezembro, mas a ordem do PC (`ORDEM-PC.md`, passo 4) manda montar **e enviar** em seguida. Alguém tem que garantir que o Montador volte ao C05 entre 01 e 08/12 (ou depois da admissão), por exemplo com uma tarefa agendada no PC.
3. Perguntar ao Vini uma vez só, com o aviso de aprovação, se ele topa o plano completo ou o mínimo (seção 2.0 do `lancamento.md`).
