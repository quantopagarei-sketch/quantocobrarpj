# Revisão de QA: Simpatia da Virada (C07)

**Data:** 06/11/2026 · **Revisor:** Controle de Qualidade · **Resultado:** pronto para montar quando a coordenação liberar o C07 na seção 2 do `PRONTO-PARA-MONTAR.md`. **Envio somente na qui 03/12/2026, junto com o C05.**

## O que foi conferido

| Item | Resultado |
|---|---|
| Arquivos citados no `guia-montagem.md` existem em `assets/` | OK: `titulo_toque.png`, `titulo.png`, `cartas/carta_01..26.png` (a pasta tem só as 26), `reservas/reserva_01..04.png`, `quadrado_512/` (título, título com toque, 26 cartas e 4 reservas), `icone_162.png`, `icone_alt_162.png`, `icone_512.png`, `icone_alt_512.png`, `previa.png`, `gerar.py`, `lista-de-arquivos.txt`, `LEIA-ME.md`, `script/prompt-effect-house-ai.md` |
| Dimensões | OK: título e cartas 512×256 RGBA, quadradas 512×512 RGBA, ícones 162×162 (e 512×512 de referência), opacos |
| Peso | OK: maior carta é a `carta_06.png`, com 110.015 bytes (≈107 KB; o limite é 1 MB). Título com toque + 26 cartas = 2,74 MB (2,62 MiB). O limite da equipe é 5 MB. A `previa.png` (2,7 MB) não entra no efeito |
| Contagem do CSV de conferência (Parte 0.5) | OK: 2 títulos + 26 cartas nas 2 versões = 56 linhas |
| `gerar.py` | Rodei de novo numa cópia (≈23 s) e as imagens saíram **idênticas byte a byte** às da pasta. Textos, cartas e reservas batem com o `textos.json` e com a tabela 0.7 do guia |
| Imagens abertas e lidas | `previa.png` inteira, os 2 ícones (162 px), título com e sem toque e as cartas 01, 02, 03, 04, 05, 06, 08, 09, 11, 12, 13, 15, 16, 18, 19, 20, 21, 22, 24 e 26, mais as reservas R1 e R3, em tamanho real. Nada cortado. Acentos certos (Ã, Á, À, Í, É, Ê, Ç, º e "…"). As mais apertadas (13 e 21, 43 px; 16, 44 px) leem bem. O dourado entre parênteses tem bom contraste nos 3 fundos. O selo ondulado é redondo e serve de régua |
| Português | Natural e atual: "pra", "tio do pavê", "crush", "o menor", "duvido". "À meia-noite" com crase certa e "1º" com ordinal. Nada ofensivo |
| Marcas, celebridades, times e carros | Nada no efeito: o "Pix" não aparece, e não há banco, app, montadora, modelo de carro, time ou pessoa real. Carro genérico, sem placa nem grade. Moeda só com estrela, sem cédula de real. O saquinho 💰 da carta 03 e da R3 tem um "$" genérico do emoji Noto, que não é marca nem moeda real (risco quase zero). Paleta sem par de cores de clube |
| Regras sensíveis | Nada religioso no desenho (sem flor no mar, vela, santo ou orixá). Sem bebida. Fogos só no céu. Roupa íntima não aparece (carta 12: carinha de "psiu" + coração). A cadeira da carta 04 está parada |
| Ícones | Cacho de uva com fogos, e uva com relógio na meia-noite (os dois ponteiros no 12). Sem texto, leem bem a 64 px. O formulário 5.16 usa o **Create icon**, e o guia já trata o PNG como plano de exceção |
| Data | O guia, o `textos.md`, o `textos.json`, o `lancamento.md` e o plano dizem **somente qui 03/12/2026, com o C05**. Conferi que 03/12/2026 é quinta. A Parte 13.1 trava o envio antes da data |
| Campos de envio | A Parte 13.4 tem os textos reais: nome `Simpatia da Virada` (18 caracteres) e as 2 alternativas (20 e 19), hint "Toque na tela" ou a opção de toque da lista, sem som, Challenge conforme a 13.2, Trend vazio e demo `C07-demo.mp4`. Para campos que podem aparecer, tem descrição (273 e 66 caracteres), categoria, tags e comentário para a revisão (EN + PT) |
| Seguível por agente | Caminhos, nomes de assets (`virada_titulo`, `cartas_simpatia`, `ANTIGO_*`), comandos PowerShell, ordem 01→26 com o 1º e o último quadro descritos, e os casos A/B e T/S. Guarda contra "Update/Replace" no envio e contra salvar por cima do C01. O fallback pelo C02 usa os nomes reais do guia dele (`carro_titulo`, `cartas_carro`) |
| Originalidade | Busca na web (06/11/2026): não achei nenhum efeito de "simpatia de ano novo" com sorteio. A mecânica de sorteio sobre a cabeça é comum, mas o tema, os 26 textos, o bilhete de desejo com pontas dobradas, o selo ondulado e a paleta são próprios e diferentes do C01 (ingresso), do C02 (asfalto), do C08 (balão) e do C05 (bolhas). A tiktok.com está bloqueada daqui: a busca na lupa do app fica (a confirmar), e o guia já manda fazer na Parte 12.4 |

## Correções feitas

1. **Guia, Parte 13.2 (desafio):** havia uma contradição. O guia mandava enviar com o Challenge vazio se a decisão do Vini não saísse até sáb 05/12, 12h. Já a ordem em vigor no `PRONTO-PARA-MONTAR.md` (06/11, 05:50) proíbe o Submit dos sorteios antes dessa decisão. Um agente que segue o texto ao pé da letra ficaria entre as duas. Agora o guia diz que a ordem do `PRONTO-PARA-MONTAR.md` vale para o C07: o Montador avisa a nuvem, não envia e relê as ordens 2 vezes por dia até sair a decisão ou a liberação.
2. **Guia, Parte 12.2:** se algum sorteio tiver sido publicado com nome alternativo, o Montador procura pelo nome anotado no relatório.
3. Versão do guia: 1.1 (revisada pelo QA). Nenhuma imagem precisou mudar. O `gerar.py` não foi rodado na pasta, porque a saída seria idêntica.

## Riscos que continuam (baixos, todos com plano)

- **5 sorteios do mesmo template na conta (C01, C02, C06, C07, C08):** a regra de duplicidade está (a confirmar). O visual é bem diferente, e a Parte 12.2 manda parar se algum voltar como "duplicado/spam".
- **Simpatia × religião:** as cartas 01 (7 ondas) e 05 (tudo branco) vêm de tradição religiosa, mas o texto e o desenho são laicos. A carta 12 (roupa íntima) e a 04 (cadeira) também são sensíveis. As 4 reservas e a tabela da Parte 17 cobrem esses casos. O demo e os ícones evitam as cartas 01, 05 e 12.
- **"Lentilha pro dinheiro vir", "romã" e "moeda":** é humor, sem promessa. O `lancamento.md` proíbe dizer que "funciona".
- **`lancamento.md`:** está limpo quanto a incentivo (nada de cupom, sorteio ou "os melhores eu reposto"), bebida, fogos, carro andando e marca. Ficam 2 pontos de atenção leves, que deixei como estão porque seguem a regra dos outros planos:
  - responder "tem na vitrine do perfil 😉" nos comentários do vídeo do efeito (só quando perguntarem);
  - os convites a criadores assinados "Vini, da Car Shop" (só falam do efeito).
  Se a equipe quiser risco zero, troque por "Vini aqui".
- **Data:** pela ordem atual, o envio depende da decisão do desafio. Se ela atrasar além de 03/12, o efeito de data perde folga. Ver as pendências.

## Pendências

- **Coordenação (não é com o Vini):**
  - ao pôr o C07 na seção 2 do `PRONTO-PARA-MONTAR.md`, escreva "montar já, enviar somente em 03/12";
  - diga também, de forma explícita, o que fazer com o desafio em 03/12 (entrar, não entrar, ou enviar sem desafio se a decisão não tiver saído).
- **Vini:** só a decisão do desafio, que já está na lista de pendências do `STATUS.md`. Nada novo para o C07.
