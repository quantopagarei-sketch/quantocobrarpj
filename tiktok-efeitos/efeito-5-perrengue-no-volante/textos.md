# Perrengue no volante: textos do efeito

Efeito C09 · versão dos textos 1.1 · 06/11/2026 · envio previsto até 17/11/2026 · Os mesmos dados estão em `textos.json` (para o designer).

**Vini, você não precisa fazer nada com este arquivo.** Ele está aqui só pra você ver o que vai aparecer no efeito. Quem usa é a equipe (designer e montador).

**Como funciona:** é um ranking às cegas. Aparece "RANKING DOS PERRENGUES DO VOLANTE" e, em cima da cabeça, surge um perrengue por vez, tipo "BALIZA COM PLATEIA". A pessoa toca no número de 1 (o pior) a 10 onde quer colocar aquele perrengue, sem saber qual vem depois. Quando os 10 estão no lugar, o ranking fica pronto na tela. A graça é gastar o 1 cedo e depois vir um pior ainda.

**Base técnica:** template **Blind Rank** (Templates > aba Interactive). Pela página oficial do template (resumo da busca, a confirmar no app), a escala vai de **1 a 10** e as imagens dos itens ficam em **Randomizer: Textures**. Num relato do fórum, com mais de 10 imagens o jogo passou da 10ª escolha e bugou a lista. Por isso a versão que vai pro envio tem **exatamente 10 itens**.

---

## 1. Nome do efeito

| | Nome | Caracteres | Por quê |
|---|---|---|---|
| **Escolhido** | **Perrengue no volante** | 20 | Fácil de lembrar e diz o assunto. Não achei efeito com esse nome na busca na web (ver "A confirmar"). |
| Alternativa 1 | Ranking dos perrengues | 22 | Mais fácil de achar pra quem procura "ranking". Usar se a equipe preferir um nome mais descritivo. |
| Alternativa 2 | Ranking do motorista | 20 | Reserva, se os outros dois já existirem. |

Nenhum dos três tem acento ou pontuação, então não dependem da regra de caracteres do formulário. O limite é 25.

## 2. O que aparece na tela

**Título** (em 3 linhas do mesmo tamanho):

> **RANKING DOS**
> **PERRENGUES**
> **DO VOLANTE**

**Subtítulo**, embaixo do título: **1 = PIOR · 10 = DE BOA**

- Se faltar espaço: só **1 = PIOR**.
- Se o template da versão instalada tiver só 5 posições (a busca indica 10): **1 = PIOR · 5 = DE BOA**.
- Onde o título entra (textura de título do template ou imagem 2D no topo da tela) fica a cargo do guia de montagem (a confirmar).

**Instrução (hint):** Toque no número

- Se o hint for de lista pronta (a confirmar): **Toque na tela**.
- Se o campo for texto livre e aceitar mais: **Escolha a posição**.
- O hint não aparece no teste pelo celular, só depois que o efeito é publicado. Isso é normal.

**Textos de interface:** só se o template mostrar algum texto em inglês. Se não mostrar, ignorar.

| Onde | Texto |
|---|---|
| Etiqueta de instrução | TOQUE NO NÚMERO |
| Botão ou aviso de reiniciar | JOGAR DE NOVO |
| Rótulo ao lado do 1 | PIOR |
| Rótulo ao lado do 10 | DE BOA |

## 3. Os perrengues

Todos cabem em 2 linhas curtas (no máximo 13 caracteres por linha e 24 no total), porque o item aparece em cima da cabeça e depois pequeno na lista. A barra ( / ) marca a quebra de linha. O emoji é só pra mostrar a ideia do desenho.

### Os 10 da versão padrão (a que vai pro envio)

| Nº | Perrengue | Emoji |
|---:|---|:-:|
| 1 | BALIZA COM / PLATEIA | 🚗👀 |
| 2 | PNEU FURADO / SEM ESTEPE | 🛞❌ |
| 3 | POÇA QUE / ERA CRATERA | 🕳️💦 |
| 4 | VAGA QUE / PARECIA MAIOR | 🚗📏 |
| 5 | LAVAR O CARRO / E CHOVER | 🧽🌧️ |
| 6 | BARULHINHO / NOVO NO CARRO | 👂🔧 |
| 7 | QUEM NÃO / DÁ SETA | 🤷💡 |
| 8 | SUBIDA COM / FILA ATRÁS | ⛰️😬 |
| 9 | ESQUECER ONDE / ESTACIONOU | 🤔🔑 |
| 10 | BATERIA / ARRIADA | 🪫😩 |

Tem perrengue grande (pneu sem estepe, bateria) e pequeno (baliza, esquecer a vaga), pra dar briga na hora de escolher a posição.

### Extras para a versão com rodízio (opcional)

Só entram se, no teste, o template com 14 imagens parar certinho depois da 10ª escolha. Aí cada rodada sorteia 10 dos 14 (Index Generator em Shuffle), e a pessoa tem motivo pra jogar de novo. Se der qualquer problema, fica a versão padrão. **Não atrasar o envio por isso.** (a confirmar)

**Revisão do QA (06/11):** o primeiro envio é **sempre** a versão padrão de 10. O rodízio pode ser testado no PC, mas só entra depois, como atualização, se a equipe decidir. Motivo: um relato diz que o efeito publicado se comportou diferente do editor quando havia mais imagens que posições.

| Nº | Perrengue | Emoji |
|---:|---|:-:|
| 11 | CARONA QUE / DÁ PITACO | 🗣️🚗 |
| 12 | ALARME QUE / DISPARA À TOA | 🚨🌙 |
| 13 | GPS / RECALCULANDO | 🗺️📍 |
| 14 | TRANCAR A / CHAVE DENTRO | 🔑🔒 |

### Reservas

Só entram se algum item for vetado na revisão. A troca é de 1 por 1, na ordem R1, R2, R3, R4. Se a versão de rodízio não for usada, as extras 11 a 14 também servem de troca.

| Código | Perrengue | Emoji |
|---|---|:-:|
| R1 | VOLANTE / PELANDO | 🥵☀️ |
| R2 | LIMPADOR QUE / SÓ ESPALHA | 🪟🌧️ |
| R3 | RESERVA ACESA / NA ESTRADA | ⛽🛣️ |
| R4 | GARAGEM / BLOQUEADA | 🚧🚗 |

### O que mudou em relação à ideia original

- O título "RANKEIE OS PERRENGUES DO VOLANTE (1 = PIOR)" virou **RANKING DOS / PERRENGUES / DO VOLANTE**, com o subtítulo **1 = PIOR · 10 = DE BOA**. Fica em 3 linhas do mesmo tamanho. E "rankeie" é grafia de rede social (o dicionário registra "ranquear"), então o substantivo "ranking" evita a dúvida. A instrução vai no hint e na etiqueta.
- "BURACO NA CHUVA" virou **POÇA QUE ERA CRATERA** (mais engraçada: é a poça que esconde o buraco).
- "FLANELINHA COBRANDO ADIANTADO" saiu e entrou **LAVAR O CARRO E CHOVER**. A frase não cabia em 2 linhas e falava de uma ocupação, e a regra é não ofender profissões. A nova não fala de ninguém.
- "FILA DO POSTO" saiu e entrou **BARULHINHO NOVO NO CARRO**. Fila de posto costuma vir de aumento de combustível, assunto que puxa preço e política. A nova é mais engraçada e serve pra qualquer carro.
- "ALARME QUE DISPARA SOZINHO" virou **ALARME QUE DISPARA À TOA** e foi para as extras ("DISPARA SOZINHO" não cabia na linha). Na vaga dele entrou **SUBIDA COM FILA ATRÁS**, que dá mais discussão.
- "BATERIA ARRIADA NA SEGUNDA" virou **BATERIA ARRIADA** (não cabia, e "na segunda" pode ser lido como segunda marcha).
- Ficaram como estavam: PNEU FURADO SEM ESTEPE, VAGA QUE PARECIA MAIOR, QUEM NÃO DÁ SETA, BALIZA COM PLATEIA e ESQUECER ONDE ESTACIONOU.

### Itens que pedem atenção (risco baixo)

- **QUEM NÃO DÁ SETA:** reclama do outro motorista, mas sem xingamento e sem gesto no desenho.
- **CARONA QUE DÁ PITACO:** "carona" aqui é quem vai no banco do passageiro. A piada é com o amigo, não com ninguém de fora.
- **GPS RECALCULANDO:** GPS é nome genérico. Não desenhar tela nem ícone de aplicativo de mapa.
- **RESERVA ACESA NA ESTRADA:** bomba e posto genéricos, sem cor ou nome de rede de postos.
- **Todos os carros:** genéricos, sem grade, emblema, silhueta de modelo real ou placa.

## 4. Para o envio no Effect House

O formulário pode não ter descrição pública. Nos outros efeitos, a equipe só achou o campo de comentários para quem revisa (a confirmar). Colar o texto em inglês e, embaixo, o em português.

**Em português** (279 caracteres):

> Ranking às cegas dos perrengues de quem dirige. Eles aparecem um de cada vez e você escolhe a posição de cada um, de 1 (o pior) a 10, sem saber qual vem depois. Tem baliza com plateia, pneu furado sem estepe e mais 8. Sem marca, modelo de carro, loja, bebida ou direção perigosa.

**Em inglês** (456 caracteres):

> Blind ranking of everyday driving struggles, in Brazilian Portuguese. Items appear one at a time above your head and you tap a slot from 1 (worst) to 10 without knowing what comes next. 10 original texts with simple drawings (parallel parking with an audience, flat tire with no spare, a puddle that was a pothole, etc.). Built on the Blind Rank template. No generative AI. No brands, car models, logos, store links, alcohol, speeding or dangerous driving.

Se a versão com rodízio for usada: no português, trocar "e mais 8" por "e mais 12"; no inglês, "10 original texts" por "14 original texts".

**Versão curta** (68 caracteres), se o campo for pequeno:

> Monte o ranking dos perrengues do volante sem saber qual vem depois.

**Categoria:** a mais próxima de "Jogo" (Game). Se não houver, "Engraçado" (Funny). A lista ainda não foi vista (a confirmar).

**Tags** (até 5, não aparecem pro público):

- Principais: ranking, carro, motorista, perrengue, humor (já estão sem acento e sem espaço)
- Se as tags tiverem que ser em inglês: blind ranking, car, driving, ranking, funny
- Reserva: trânsito, dirigir, blind ranking
- Palavras extras, pra descrição ou legenda: baliza, pneu furado, blind rank

## 5. Para o vídeo de lançamento na conta

Isso vai só na legenda do vídeo, nunca dentro do efeito.

- Gastei o 1 cedo demais e depois veio a baliza com plateia. Faz o teu
- Qual é o teu número 1? Rankeia aí e me mostra
- Marca quem já passou por todos esses

Hashtags: #perrenguenovolante #blindranking #ranking #motorista #carro #perrengue

**Não pode** prometer prêmio, cupom ou sorteio pra quem usar o efeito. O TikTok trata isso como uso incentivado e para de contar os vídeos. A loja também não aparece no vídeo do efeito.

## 6. O que não pode aparecer no efeito

- Marca, logo, emblema ou modelo de carro; grade ou silhueta que lembre um modelo real; placa de verdade
- Nome ou cores de rede de postos, de aplicativo de mapa ou de qualquer outra marca
- @ da conta, link, nome da loja ou chamada pra comprar
- Bebida, velocidade, radar, multa, racha, blitz, celular na mão dirigindo
- Xingamento, gesto ofensivo, piada com profissão

## 7. A confirmar

- (a confirmar) Se o Blind Rank da versão instalada tem mesmo 10 posições. A busca na página oficial diz de 1 a 10.
- (a confirmar) Se o template aceita mais de 10 imagens sem bugar. O relato do fórum diz que não. Isso decide se a versão com rodízio é possível.
- (a confirmar) Tamanho e proporção das imagens originais do template (fotos de comida).
- (a confirmar) Se o template tem textura de título ou cabeçalho e se mostra algum texto de interface em inglês.
- (a confirmar) Se os itens giram antes de parar (a página cita "Tap To Stop Randomizer") e se o toque é no número da lista. Isso confirma o hint "Toque no número".
- (a confirmar) Se o hint é texto livre ou lista pronta.
- (a confirmar) Se as tags aceitam espaço e acento, e em que idioma funcionam melhor.
- (a confirmar) Se existe campo de descrição pública ou só o de comentários para a revisão.
- (a confirmar) Se já existe efeito famoso chamado "Perrengue no volante". A busca na web não achou nenhum, e o tiktok.com está bloqueado daqui. Existe uma série chamada "Perrengue", mas a palavra é comum e o nome completo é outro.
- (a confirmar) Registro de marca "Perrengue no Volante" no INPI, que não foi conferido daqui: https://busca.inpi.gov.br/pePI/

Fontes da parte técnica (resumos da busca, porque os sites não abrem daqui): https://effecthouse.tiktok.com/learn/guides/tutorials/template-tutorials/blind-rank · https://effecthouse.tiktok.com/learn/library/template-tutorials/blind-rank · https://community.effecthouse.com/t/help-with-blind-rank-template/60530

---

## Para o designer

- Os dados estruturados estão em `textos.json`. Use `linha1` e `linha2` exatamente como estão, sem quebrar de outro jeito.
- **Título:** `titulo.png`, fundo transparente, em 3 linhas (`linha1`, `linha2`, `linha3`) e o subtítulo menor embaixo. Faça também a versão sem subtítulo e a de 5 posições, pra não atrasar se o template for diferente.
- **Itens:** `cartas/carta_01.png` até `carta_10.png` (versão padrão). A pasta `cartas/` só pode ter essas 10 imagens. Extras: `extras/carta_11.png` até `carta_14.png`. Reservas: `reservas/reserva_01.png` até `reserva_04.png`. Todas do mesmo tamanho e com o mesmo enquadramento.
- **Tamanho:** o mesmo das imagens de comida do template (a confirmar ao abrir o projeto). O conceito estimou uns 512×128. Se não der pra saber antes, sugestão: 512×512 (desenho em cima, 2 linhas embaixo) e uma cópia em 512×256, como no efeito-1.
- **Legibilidade:** o item aparece grande em cima da cabeça e depois pequeno na lista de 1 a 10. Letra bem grossa, contorno escuro e desenho simples. O maior item tem 24 caracteres (BARULHINHO / NOVO NO CARRO).
- **Interface (opcional):** `etiqueta_toque.png` (TOQUE NO NÚMERO), `jogar_de_novo.png` (JOGAR DE NOVO), `rotulo_pior.png` (PIOR) e `rotulo_de_boa.png` (DE BOA). Só são usadas se o template tiver texto em inglês nesses lugares.
- Tudo em MAIÚSCULAS, com acento. Máximo de 24 caracteres por item e 13 por linha.
- A fonte precisa ter todos estes glifos: `015=ABCDEFGHIJKLMNOPQRSTUVZ·ÀÁÃÇÓÚ`. Atenção principalmente a À (em "À TOA"), Á, Ã, Ç, Ó, Ú, "=" e "·". A Inter Display do efeito-1 tem todos (conferido). Se trocar algum texto, confira de novo os limites.
- **Emoji:** é só referência (principal + secundário, como no `ILUSTRA` do `gerar.py` do efeito-1). Se usar emoji pronto, use o Noto Color Emoji (OFL 1.1). Todos os da tabela existem nessa fonte (conferido). No Noto, a cabeça do 🗣️ e o 🚙 vêm azuis, e as setas (⬅️ etc.) vêm num quadrado azul. Recolorir ou trocar, seguindo a regra de paleta do efeito-1.
- **Ícone:** `icone_162.png` (2º ícone opcional: `icone_alt_162.png`), 162×162 px, área segura de 144×144. Um volante genérico (aro com 3 raios e centro liso, sem nada que pareça emblema) com uma gota de suor grande. Sem texto. Não existe emoji de volante, então é preciso desenhar. Ideia para o ícone alternativo: o mesmo volante na frente de uma listinha numerada 1, 2, 3.
- **Desenhos:** cada item tem uma descrição no campo `ilustracao` do JSON. Carro, chave, bateria, bomba de combustível e mapa sempre genéricos.
- **Paleta:** a mesma regra do efeito-1, sem par de cores de clube (vermelho+branco, verde+branco, preto+branco) e sem azul como cor principal.
