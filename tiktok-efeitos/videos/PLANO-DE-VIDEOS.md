# Plano de vídeos dos 7 efeitos (feito pela equipe, sem o Vini)

**Feito em:** 06/11/2026, pelo diretor de vídeo.
**Base:** pesquisas `videos/pesquisa/R1-postagem-pelo-pc.md`, `R2-direitos-e-regras.md`, `R3-formatos-sem-rosto.md`; a biblioteca `videos/lib/render.py` (`LEIA-ME.md`); os `lancamento.md` dos 7 efeitos (partes 3, 4 e 6); `plano-curto-prazo.md` (seções 1, 3, 3.1 e 5); `STATUS.md` e `PRONTO-PARA-MONTAR.md` (só leitura).
**Quem usa:** a coordenação. Ela transforma este plano em ordens para o Montador no `PRONTO-PARA-MONTAR.md`. Nós não editamos aquele arquivo.
**Este arquivo substitui:** a seção 3.1 do `plano-curto-prazo.md` e as tabelas de cronograma e as "listas de gravação do Vini" de cada `lancamento.md`. As boas ideias desses arquivos (ganchos, cartas, datas de futebol e de festa) foram aproveitadas aqui.
**Perfil (nome, foto, bio, link, fixados):** é do diretor de marca. Ver `videos/perfil/PERFIL.md`.
**Legenda:** (a confirmar) = ainda não visto na tela ou em fonte segura.
**Revisado pelo crítico em 06/11/2026.** As correções já estão no texto. O resumo do que mudou e por quê está na seção 10, no fim.
**Ajustes do gerente (06/11/2026, depois do estúdio de vídeo):** (1) as ordens ao Montador estão em `videos/ORDENS-VIDEOS-MONTADOR.md`; (2) as peças prontas ficaram em `efeito-*/videos/`, com capa `.jpg` (não há `videos/prontos/`); (3) quinta-feira = 18h em todo o calendário (C08-V1, C02-M1 e C06-V3 saíram de 19h); (4) "Montador agenda até [data]" virou "a partir de [data]": o Agendar só alcança 10 dias à frente (a confirmar), então a data é o 1º dia possível, não o prazo.

---

## Resumo em 9 linhas

1. O Vini não grava. A conta posta **vídeos-cartaz** pelo TikTok Studio no navegador: animações feitas pela nuvem com as nossas cartas e, quando der, gravações do preview do Effect House feitas pelo Montador.
2. Esses vídeos **não levam a etiqueta clicável do efeito e não contam como uso**. Servem para outras pessoas **procurarem o filtro pelo nome**. Os 1.000 vídeos vêm delas.
3. São **27 peças de efeito** (de 3 a 4 por efeito; no máximo 3 MP4 da nuvem por efeito) e **2 peças gerais** (tutorial "como achar nossos filtros").
4. **D1 = dia seguinte à aprovação.** O 1º vídeo sai sempre no D1, no horário nobre. Uma estreia por dia. **C01 e C08 já estão em análise e podem ser aprovados a qualquer dia: os V1 deles ficam prontos até sáb 07/11.**
5. **No máximo 2 posts por dia na conta** (loja conta), com 3 h ou mais entre eles. Nunca 2 do mesmo efeito no mesmo dia.
6. Horários: **18h de terça a quinta, 19h nos outros dias** (nobre); **15h** (tarde); **12h30** (loja). Dia de jogo grande: 2 a 3 h antes do jogo.
7. Som sempre **nosso**, sintetizado na nuvem, com uma "assinatura" por efeito. Sem música de terceiros. Biblioteca Comercial só em teste.
8. O Montador mede cada post (24 h e 72 h) e cada efeito (vídeos novos por dia). No **D3** e no **D7** a equipe decide o que muda.
9. **Novo (revisão):** quando outras pessoas postarem com o efeito, a conta **reposta e comenta** os melhores vídeos delas (seção 5.6). É o único jeito de mostrar aos 40 mil um vídeo **com** a etiqueta clicável, sem celular.

---

## 1. Princípios (o que dá, o que não dá e como compensamos)

1. **Dá para fazer sem o Vini:** vídeos-cartaz renderizados pela nuvem (nossas cartas, nossa arte, nosso som), gravações do preview do Effect House feitas pelo Montador e toda a postagem, o agendamento, os comentários e o perfil pelo navegador do PC.
2. **Não dá: vídeo gravado COM o efeito.** Isso só acontece na câmera do app do TikTok, num celular. Só esse vídeo ganha a etiqueta clicável e pode contar como uso. Site, app do Windows e LIVE Studio não têm os efeitos. Emulador e câmera virtual ficam fora: risco alto para a conta, a loja e o efeito (R1).
3. **Por isso os nossos vídeos são cartazes.** Eles não contam como uso. Quem gostar precisa **procurar o filtro pelo nome**, e muita gente se perde nesse passo (R3).
4. **Como compensamos:** nome exato do filtro em 3 lugares (tela, legenda, comentário fixado); "Procura na lupa 🔎" em todo vídeo; link do efeito da vez na bio; um vídeo-tutorial; prova do efeito funcionando num rosto de banco com licença; convites sem prêmio; e medição da conversão no dia seguinte a cada post.
5. **Regras de produção:** nenhuma pessoa inventada, nenhum rosto das amostras do Effect House em post público, nenhuma música de terceiros, nada da loja nos vídeos de efeito, nenhum QR code no vídeo e nada repetido (cada peça tem gancho, texto, ritmo e som próprios).

---

## 2. Formatos e quem faz

### 2.1 Os 4 tipos

| Tipo | O que é | Quem faz | Fonte de rosto | Quando usar |
|---|---|---|---|---|
| **N-video** | MP4 1080x1920 renderizado pela nuvem com `videos/lib/render.py`: roleta, "pausa e vê o seu", ranking, revelação de bolhas, POV de texto, card de resposta, tutorial | **Nuvem** renderiza; QA confere a prancha; **Montador** agenda e posta | **Nenhum rosto.** Só cartas, títulos e ícones dos efeitos, emoji (Noto) e a arte do perfil. No lugar da "cabeça", uma carinha emoji 🤔. Nunca silhueta humana nem rosto | Base de tudo. Máximo **3 por efeito** |
| **N-carrossel** | 3 a 5 JPG 1080x1920 (≤ 500 KB) tirados de uma linha do tempo já feita (`exportar_slides`) | Nuvem gera; Montador posta | Nenhum | **Reserva.** Só se o teste do Montador mostrar "modo Foto" no upload pela web (R1 diz que provavelmente não existe; R3 mostra vídeo com 5,6 vezes mais views). Nunca no lugar de um V1. Fora do calendário |
| **M-gravacao** | Gravação de tela do **preview do Effect House** com o efeito real funcionando | **Montador** grava e finaliza no PC com o kit da nuvem | **Só clipe de banco com licença:** 1º Pexels; 2º Mixkit com "Free License". **Nunca** os vídeos de amostra do Effect House (só servem para o demo do envio; R2). "Nenhum rosto" não serve aqui: o efeito precisa de rosto para aparecer | Prova de que o filtro existe e funciona. **Opcional:** se não estiver pronta na véspera, o horário fica vago |
| **Opcional do Vini** | Ver 2.6 | Vini, se quiser | O dele | **Nunca obrigatório.** Nenhuma data depende disso |

### 2.2 Molde de tela (vale para toda peça N e M)

- **Quadro 1 (0 a 2 s):** texto do gancho já visível (entrada `None`), com no máximo 7 palavras, e a carta mais engraçada na tela. A promessa se cumpre até os 2 s.
- **Meio:** sorteio, ranking ou bolhas. Algo muda na tela a cada 1 a 2 s.
- **Cartão final (CF), últimos 2 a 2,5 s:** "Procura na lupa 🔎" + **nome exato do filtro** em amarelo, numa linha só, + o símbolo do perfil (`videos/perfil/simbolo_transparente.png`, uns 220 px; desde a revisão ele tem a "mira" de câmera) + uma pergunta curta (varia por peça).
- **"No meu perfil" / "aba de efeitos"** só entra em tela, legenda ou comentário **depois** que o Montador abrir o perfil numa janela anônima e vir a aba de efeitos com o filtro (conta Pessoal: a confirmar). Até lá, só "Procura na lupa 🔎".
- **Luz piscante:** no máximo **3 trocas de carta por segundo** nos trechos rápidos ("pausa"), cartas em ordem de brilho parecido e nada de flash branco de tela cheia. Mais rápido que isso pode ativar o aviso de luz piscante do TikTok, que trava o vídeo antes de tocar (a confirmar). Se algum post receber esse aviso, a nuvem também desacelera o começo da roleta.
- **Na tela, "você"** (alcance nacional). "Tu", "bah" e "tchê" ficam para as respostas nos comentários.
- **Nunca:** "toca no nome do efeito" (exceção única: o G-V1, que manda tocar no nome **no vídeo de quem usou**, não no nosso), "o meu saiu…", "tem gente que tirou…", "carta rara", "só 1% tira", "comenta EU", "sigo quem usar", "marca 5 amigos", "concorra", "ganhe", "desafio" ou "prêmio", QR code, logo ou tela do app do TikTok, nome de app de mensagem, marca, time, carro reconhecível, "Pix", bebida, direção perigosa ou símbolo religioso.
- **Pode:** "Qual saiu pra você?", "Manda pra quem é assim", "Manda no grupo", "Faz o seu e me marca", "Duvido" (desafio sem prêmio).

### 2.3 Ficha técnica de toda peça N

- MP4 H.264 + AAC, 1080x1920, 30 fps, **6 a 15 s, até 4 MB**. Para caber: `renderizar(..., limite_mb_10s = 38 / duração)` (ex.: 12 s → 3,17).
- Tudo que importa dentro da zona segura da biblioteca (x de 60 a 940, y de 220 a 1500). Cartas na escala 1,6 no máximo.
- Entrega por peça (como ficou: na pasta `efeito-*/videos/`, com capa `.jpg` para caber em 12 MB; o plano original pedia `videos/prontos/<código>/`): `<código>.mp4`, `<código>-capa.png` (1080x1920, texto grande dentro do miolo 3:4, de y 240 a 1680), `<código>-legenda.txt` (legenda + hashtags, pronta para colar), `<código>-prancha.png`.
- **Prazo:** pronta e revisada **3 dias antes** do post. **C01-V1 e C08-V1: até sáb 07/11, 12h** (os dois estão em análise desde 06/11 e podem ser aprovados a qualquer dia). C02-V1 e C09-V1: até seg 09/11. G-V1: até sex 13/11. C06-V1: até 20/11. C05-V1 e C07-V1: até 04/12.
- **Se a aprovação chegar antes da peça ficar pronta:** a peça sai no 1º horário nobre livre depois de pronta (no máximo 48 h depois do D0). Nunca postar peça sem QA.
- **Nome publicado diferente do `textos.md`** (ex.: sem acento): a nuvem refaz tela, capa e legenda **no D0**, antes do D1.
- **Rótulo de IA: desligado** (é animação feita por código, sem pessoa e sem cena realista; R2). **Conteúdo comercial: desligado.**
- **QA antes de liberar:** nome igual ao publicado; gancho no 1º quadro; CF nos 2 s finais; sem pessoa; sem nada da lista "Nunca"; legenda com até 5 hashtags; duração de 6 a 15 s; até 4 MB (`render.py --info`); nada importante fora da zona segura (aviso `avisos_zona` vazio).
- **Capa:** se o TikTok Studio não tiver "Editar capa → Carregar" (a confirmar no passo 0), o Montador escolhe o quadro de 0,5 s. Por isso o quadro 0,5 s de toda peça N tem que funcionar sozinho como capa (gancho grande e carta inteira).

### 2.4 Som

- **Padrão: som nosso**, feito na nuvem com numpy (biblioteca: tique, plim, vush, pop, bip, toque, trilha rítmica; o resto a nuvem sintetiza). Vai **dentro do arquivo**. Nada de música famosa, acelerada, hino ou canto de torcida.
- **Assinatura sonora por efeito** (igual em todos os vídeos dele, com trilha e ritmo variando):

| Efeito | Assinatura | Trilha |
|---|---|---|
| C08 Eu no grupo da família | plim duplo de "mensagem nova" (genérico, sem imitar app nenhum) + pop | 104 bpm |
| C01 Torcedômetro | apito curto duplo + tique de roleta | 120 bpm |
| C05 Meu 2027 vai ser | estouro de bolha + brilho | 96 bpm |
| C02 Meu próximo carro | buzina curta "bi-bi" sintetizada + tique | 116 bpm |
| C09 Perrengue no volante | tic-tac de pisca-alerta + vush e pop por vaga | 100 bpm |
| C06 Meu amigo secreto | sininho + pop de caixa abrindo | 112 bpm |
| C07 Simpatia da Virada | bipes de contagem + estouro grave + brilho | 108 bpm |

- **Quando trocar por som em alta:** só se o teste do Montador mostrar a **Biblioteca de Música Comercial** no upload pela web. A biblioteca geral não (a conta vende; R2). Nunca no V1. A partir do D7 de cada efeito, **1 peça por semana** (as marcadas "Teste de som: sim") pode levar uma faixa da Biblioteca Comercial em volume baixo, por baixo do nosso som. O Montador escolhe pelo print do Creative Center (Tendências → Músicas → Brasil) da segunda. Se o site não deixar manter o som do arquivo junto, não troca.

### 2.5 Como se faz uma M-gravacao

1. **Clipe:** o Montador baixa no PC (daqui da nuvem esses sites não abrem). Regras do R2: 1 pessoa adulta, de frente, parada, olhando para a câmera, camiseta lisa, fundo neutro. Rejeitar se tiver camisa ou escudo de time, logo, carro reconhecível, marca em roupa ou objeto, criança, famoso, bebida, símbolo religioso, direção ou clipe marcado como IA.
2. **Planilha de licença** (no PC, ao lado do `relatorio-montagem.md`): link do clipe, autor, data e print da página com a licença.
3. **Gravar:** no preview do Effect House, "+ Add media" → o clipe → botão de gravar do próprio preview (9:16) → clicar na tela para sortear. 8 a 12 s. Pode ser feito **já na montagem**, antes da aprovação (a gravação só vai ao ar no dia da peça). Se o preview não tiver botão de gravar (a confirmar), usar a gravação de tela da Ferramenta de Captura do Windows 11 (Win + Shift + R, a confirmar no PC), só na área do preview, sem menus, sem mouse e sem a interface do Effect House.
4. **Carta leve sobre rosto de banco.** Se sair carta que deixe a pessoa mal, grava de novo. Cada efeito tem a sua lista de "evitar" (seção 3).
5. **Acabamento no PC:** Clipchamp, que vem no Windows 11 (a confirmar no PC). Kit da nuvem por peça M: `gancho.png` (transparente, por cima de 0 a 3 s), `final.png` (CF, 2,5 s no fim), `assinatura.wav`, `capa.png` e `legenda.txt`. Som do clipe desligado. Exportar 1080p em MP4. **Conferir antes de postar:** de 6 a 15 s e até 4 MB (Propriedades do arquivo). Se passar de 4 MB, exportar de novo em 720p. Se o Clipchamp não existir ou travar, **a peça sai do calendário** e o horário fica vago. Nada de editor com marca d'água.
6. **Texto:** nunca "eu", "testei", "minha mãe" nem nome. Sempre "Funciona assim 👇". A pessoa nunca aparece perto de produto, preço ou loja.
7. **Rótulo de IA: desligado** (pessoa filmada de verdade, sem IA). **Conteúdo comercial: desligado.**

### 2.6 Opcional do Vini (nunca obrigatório)

As 3 gravações do `LEIA-PRIMEIRO.md` (22/11, 29/11 e 12/12) **saem do plano**. Nada no calendário depende do Vini. Se ele quiser, e só se quiser:

- **Mandar o link de um efeito** para amigos ou para a família (1 min). Só o link. Nada de pedir para cada um postar nem combinar quem posta quando (uso combinado não conta; R2).
- **1 minuto no app** para pôr o link na bio ou fixar vídeos, **se** a web não tiver esses campos (a coordenação pede no máximo uma vez).
- **Gravar 10 s com o efeito no celular**, qualquer um, sem roteiro. Esse é o único vídeo que ganha a etiqueta clicável. Se vier, entra num horário vago.

---

## 3. As peças, efeito por efeito

**Como ler:** código = efeito + tipo (V = N-video, M = M-gravacao). "CF" = cartão final da seção 2.2. Os números das cartas são os arquivos em `assets/cartas/` (C08: `assets/cartas/opcao_NN.png`). Datas "alvo" vêm do calendário da seção 4 e mudam se a aprovação mudar.

**Comentário fixado padrão** (o Montador publica logo depois do post; varia a 1ª frase de um post para outro; **até 150 caracteres**, limite a confirmar na tela; "ou no meu perfil" só depois da conferência da seção 2.2; se a web não tiver "Fixar" no comentário, só publicar):
> Nome do filtro: **[nome exato]** 🔎 Procura na lupa ou no meu perfil. [pergunta da peça]

**Resposta padrão para "onde compra?":** "Te chamo no direct 😉" (o produto só aparece na mensagem direta).

---

### C08 · Eu no grupo da família

Template Randomizer (sorteio sobre a cabeça, 1 rosto), 28 cartas. Fundo rosa → roxo, padrão bolinhas, balões 💬 flutuando. **Nada que lembre app de mensagem** (sem verde, sem tela de conversa, sem nome de app). Hashtag do efeito: `#eunogrupodafamilia`. Evitar sobre rosto de banco: SOU A FONTE DAS FOFOCAS (6).

#### C08-V1 · N-video · "O filtro que te expõe" · 10 s
- **Objetivo:** estreia. Mostrar em 3 s o que o filtro faz. Puxar compartilhamento para o grupo da família.
- **Gancho (0–2 s):** carta 2 MANDO ÁUDIO DE 4 MINUTOS + "O filtro que te expõe no grupo".

| Tempo | Na tela | Som |
|---|---|---|
| 0,0–1,8 | Gancho no topo. Carta 2 grande, balançando. 🤔 embaixo | trilha entra; plim duplo |
| 1,8–2,6 | Carta sai. Entra o título NO GRUPO DA FAMÍLIA, EU… e o dedo 👆 toca | vush, toque |
| 2,6–6,6 | Roleta das 28 cartas para na 7 SOU ADM E NINGUÉM PEDIU. Luz, confete, tremida | tiques, plim |
| 6,6–8,0 | "Alguém tem que manter a ordem 😌" | pop |
| 8,0–10,0 | CF com "Qual é o seu papel no grupo?" | assinatura |

- **Textos de tela:** "O filtro que te expõe no grupo" · "Alguém tem que manter a ordem 😌" · CF.
- **Legenda:** `Qual é o seu papel no grupo da família? Manda no grupo e vê quem concorda 😂 Filtro: Eu no grupo da família 🔎`
- **Hashtags:** `#eunogrupodafamilia #grupodafamilia #filtro #filtrotiktok #familia`
- **Chamada:** "Procura na lupa 🔎 Eu no grupo da família".
- **Som:** assinatura C08, trilha 104 bpm. Teste de som: não.
- **Capa:** "QUAL É O SEU PAPEL NO GRUPO?" com a carta 7.
- **Quando:** D1. Alvo **qui 12/11, 18h**.
- **Quem:** nuvem renderiza até 09/11; Montador agenda ou posta.

#### C08-V2 · N-video · "A família inteira" · 13 s
- **Objetivo:** identificação. Cada um lembra do parente que é assim e manda o vídeo para ele.
- **Gancho (0–2 s):** rótulo "MÃE" + carta 1 MANDO BOM DIA COM FLOR + "Cada um da família tem o seu".

| Tempo | Na tela | Som |
|---|---|---|
| 0,0–2,0 | Gancho. Rótulo MÃE + carta 1 | trilha; plim |
| 2,0–3,5 | Rótulo TIO + carta 21 FAÇO A PIADA DO PAVÊ | vush |
| 3,5–5,0 | Rótulo VÓ + carta 5 REPASSO TODA CORRENTE | vush |
| 5,0–6,5 | Rótulo PRIMO + carta 11 SÓ COMENTO KKKKKKK | vush |
| 6,5–7,3 | "E VOCÊ?" + dedo 👆 | toque |
| 7,3–10,5 | Roleta para na 4 VISUALIZO E NÃO RESPONDO | tiques, plim |
| 10,5–13,0 | CF com "Manda no grupo da família 👀" | assinatura |

- **Textos de tela:** "Cada um da família tem o seu" · MÃE · TIO · VÓ · PRIMO (só rótulos em texto, sem rosto nem emoji de pessoa) · "E VOCÊ?" · CF.
- **Legenda:** `Mãe, tio, vó, primo… cada um tem seu papel no grupo 😂 E você? Filtro: Eu no grupo da família 🔎 procura na lupa`
- **Hashtags:** `#eunogrupodafamilia #grupodafamilia #familiabrasileira #filtrotiktok #humor`
- **Chamada:** "Procura na lupa 🔎 Eu no grupo da família".
- **Som:** assinatura C08, trilha 110 bpm. **Teste de som: sim.**
- **Capa:** "CADA UM DA FAMÍLIA TEM O SEU 😂".
- **Quando:** D4 ou o domingo seguinte. Alvo **dom 15/11 (feriado), 19h**.
- **Quem:** nuvem até 12/11; Montador.

#### C08-M1 · M-gravacao · "Funciona assim" · 10–12 s
- **Objetivo:** provar que o filtro existe e funciona num rosto.
- **Fonte de rosto:** clipe do Pexels (ou Mixkit "Free License"), regras da 2.5. Cartas boas para rosto de banco: 26 AVISO QUE VAI CHOVER, 20 PASSO RECEITA QUE NINGUÉM FAZ, 25 ENCHO O GRUPO DE FOTO DO PET.
- **Gancho (0–3 s, `gancho.png`):** "Funciona assim 👇 qual é seu papel?"
- **Roteiro:** 0–3 s clipe com o título na cabeça e o gancho por cima · 3–7 s clique, as cartas giram e param · 7–9,5 s o resultado parado · 9,5–12 s `final.png` (CF com "Qual é o seu?").
- **Legenda:** `Funciona assim: toca na tela e o filtro mostra seu papel no grupo da família. Filtro: Eu no grupo da família 🔎`
- **Hashtags:** `#eunogrupodafamilia #grupodafamilia #filtro #filtrotiktok #feriado`
- **Som:** `assinatura.wav` por cima; som do clipe desligado. Teste de som: não.
- **Capa:** "FUNCIONA ASSIM 👇".
- **Quando:** alvo **sex 20/11 (feriado, família reunida), 19h**. Se não estiver pronta na véspera, o horário fica vago.
- **Quem:** Montador grava durante a montagem e finaliza; nuvem manda o kit até 17/11.

#### C08-V3 · N-video · "Natal no grupo" · 11 s
- **Objetivo:** 2ª onda no dia em que o grupo da família mais lota.
- **Gancho (0–2 s):** carta 13 SÓ ESCREVO EM CAPS LOCK + "Hoje o grupo da família vai lotar 🎄".

| Tempo | Na tela | Som |
|---|---|---|
| 0,0–2,0 | Gancho. Carta 13. Chuva de 💬 e 🎄 | trilha; plim duplo |
| 2,0–3,5 | "FELIZ NATAL × 200 💬" (o grupo enchendo) | plins seguidos |
| 3,5–4,2 | "E você, quem é hoje?" + dedo 👆 | toque |
| 4,2–8,0 | Roleta para na 9 SÓ APAREÇO PRA DAR PARABÉNS | tiques, plim |
| 8,0–11,0 | CF com "Cada um no seu celular 📱" | assinatura |

- **Legenda:** `Natal: hoje o grupo da família vai lotar 🎄 Qual é o seu papel nele? Filtro: Eu no grupo da família 🔎`
- **Hashtags:** `#eunogrupodafamilia #grupodafamilia #natal #filtrotiktok #familia`
- **Chamada:** "Procura na lupa 🔎 Eu no grupo da família".
- **Som:** assinatura C08 com sininho de fundo, trilha 100 bpm. Teste de som: não.
- **Capa:** "NATAL NO GRUPO DA FAMÍLIA 🎄".
- **Quando:** data fixa **sex 25/12, 15h**.
- **Quem:** nuvem até 21/12; Montador agenda a partir de 15/12 (rodada de qui 17/12).

---

### C01 · Torcedômetro

Template Randomizer2D, 26 cartas. **Serve pra qualquer time:** nada de nome, apelido, cor combinada ou escudo de clube. Fundo roxo → turquesa, padrão "mais". Hashtag do efeito: `#torcedometro`. Não usar nome de campeonato na tela (só "dia de final"). Evitar sobre rosto de banco: PÉ-FRIO CERTIFICADO (3) e SOFREDOR RAIZ (7). Preferir 26 TORCE ATÉ NA CHUVA, 6 NARRA MAIS QUE A TV, 12 CHORA NO HINO.

#### C01-V1 · N-video · "Roleta do torcedor" · 10 s
- **Objetivo:** **1º post da conta depois do silêncio** (se o C01 for aprovado junto ou antes do C08). Falar com a base de futebol, sem time.
- **Gancho (0–2 s):** carta 8 SAI AOS 40 DO 2º TEMPO + "Que tipo de torcedor você é?".

| Tempo | Na tela | Som |
|---|---|---|
| 0,0–1,8 | Gancho no topo. Carta 8 balançando. ⚽ e 🤔 | trilha; apito curto |
| 1,8–2,6 | Título QUE TORCEDOR VOCÊ É? (`titulo_toque.png`) + dedo 👆 | toque |
| 2,6–6,6 | Roleta das 26 cartas para na 3 PÉ-FRIO CERTIFICADO. Confete, tremida | tiques, plim |
| 6,6–8,0 | "Isso explica muita coisa 🥶" | pop |
| 8,0–10,0 | CF com "Serve pra qualquer time ⚽" | apito duplo |

- **Legenda:** `Que torcedor você é? Gira e me conta qual saiu. Nome do filtro: Torcedômetro 🔎 procura na lupa`
- **Hashtags:** `#torcedometro #filtro #filtrotiktok #futebol #torcedor`
- **Chamada:** "Procura na lupa 🔎 Torcedômetro".
- **Comentário fixado (versão longa, só no 1º post da conta, seja do C01 ou do C08; 114 caracteres):** "Filtro: Torcedômetro 🔎 Procura na lupa. A conta agora faz filtros de torcida, carro e zoeira 😄 Qual saiu pra você?" (no C08: trocar o nome e a pergunta por "Qual é o seu papel?")
- **Som:** assinatura C01, trilha 120 bpm. Teste de som: não.
- **Capa:** "QUE TORCEDOR VOCÊ É?" com a carta 3.
- **Quando:** D1. Alvo **qua 11/11, 17h30** (antes dos jogos da noite).
- **Quem:** nuvem até 09/11; Montador.

#### C01-V2 · N-video · "Pausa e vê o seu" · 9 s
- **Objetivo:** retenção (a pessoa volta e pausa) e comentário ("qual pegou?").
- **Gancho (0–2 s):** cartas já passando no quadro 1 + "PAUSA AGORA ⏸️ e vê o seu" (texto único, 6 palavras, do 1º quadro até 7 s).

| Tempo | Na tela | Som |
|---|---|---|
| 0,0–7,0 | Texto fixo "PAUSA AGORA ⏸️ e vê o seu". **20 das 26 cartas** (a nuvem escolhe as mais engraçadas) trocando a cada **0,35 s** (`slides`, transição corte), sem repetir, em ordem de brilho parecido | tique a cada carta, trilha 132 bpm |
| 7,0–9,0 | CF com "Qual pegou? Conta aqui 👇" | apito duplo |

- **Legenda:** `Pausa o vídeo e vê que torcedor você é ⏸️ Qual pegou? Filtro: Torcedômetro 🔎 na lupa ou no meu perfil`
- **Hashtags:** `#torcedometro #filtrotiktok #futebol #torcedor #zoeira`
- **Chamada:** "Procura na lupa 🔎 Torcedômetro".
- **Som:** assinatura C01. **Teste de som: sim.**
- **Capa:** "PAUSA E VÊ O SEU ⏸️".
- **Quando:** D4. Alvo **sáb 14/11, 15h** (2 a 3 h antes dos jogos do dia; horários a confirmar).
- **Quem:** nuvem até 11/11; Montador.

#### C01-V3 · N-video · "Dia de final" · 12 s
- **Objetivo:** pegar o dia de maior interesse em futebol e criar o costume de "girar antes do jogo".
- **Gancho (0–2 s):** carta 19 CARDÍACO NOS ACRÉSCIMOS + "Dia de final: gira antes do jogo".

| Tempo | Na tela | Som |
|---|---|---|
| 0,0–2,0 | Gancho. Carta 19 | trilha 124 bpm |
| 2,0–4,0 | Contagem 3, 2, 1, "GIRA!" | bipes |
| 4,0–8,0 | Roleta para na 13 NÃO OLHA O PÊNALTI | tiques, apito longo |
| 8,0–10,0 | "Liberado pra assistir… de costas 🙈" | pop |
| 10,0–12,0 | CF com "Serve pra qualquer time ⚽" | apito duplo |

- **Legenda:** `Dia de final: gira antes do jogo e vê se pode assistir 😅 Serve pra qualquer time. Filtro: Torcedômetro 🔎`
- **Hashtags:** `#torcedometro #filtrotiktok #diadefinal #futebol #torcedor`
- **Chamada:** "Procura na lupa 🔎 Torcedômetro".
- **Som:** assinatura C01. Teste de som: não.
- **Capa:** "DIA DE FINAL: GIRA ANTES ⚽".
- **Quando:** data fixa **sáb 28/11, 14h** (final às 17h; nada postado das 16h às 20h).
- **Quem:** nuvem até 24/11; Montador agenda a partir de 18/11 (rodada de qui 19/11).

#### C01-M1 · M-gravacao · "Funciona assim" · 10–12 s
- **Objetivo:** prova do filtro num rosto, no dia de outra final.
- **Fonte de rosto:** clipe do Pexels (regras da 2.5), camiseta lisa. Cartas leves (26, 6, 12).
- **Gancho (`gancho.png`):** "Funciona assim 👇 serve pra qualquer time".
- **Roteiro:** 0–3 s clipe com QUE TORCEDOR VOCÊ É? na cabeça · 3–7 s clique, gira, para · 7–9,5 s resultado · 9,5–12 s CF com "Gira antes do jogo ⚽".
- **Legenda:** `Funciona assim: toca na tela e o filtro diz que torcedor você é. Serve pra qualquer time. Filtro: Torcedômetro 🔎`
- **Hashtags:** `#torcedometro #filtro #filtrotiktok #futebol #diadefinal`
- **Som:** `assinatura.wav`. Teste de som: não.
- **Capa:** "FUNCIONA ASSIM 👇 TORCEDÔMETRO".
- **Quando:** data fixa **dom 06/12, 2 a 3 h antes da final** (hora do jogo a confirmar). Se não estiver pronta, o dia fica sem post de efeito.
- **Quem:** Montador grava na montagem; nuvem manda o kit até 02/12.
- **Cuidado (C01, seção 7.5):** se a última rodada (~02/12) deixar a base de luto, o post de 06/12 fica leve ou sai.

---

### C05 · Meu 2027 vai ser

Template Future Life: bolhas que estouram quando a pessoa faz biquinho e sorteiam as previsões. Versão padrão com 3 bolhas (AMOR, GRANA, FUTEBOL); CARRO entra só se foi publicada com 4 (conferir no D0). A nuvem desenha as bolhas com `assets/variantes/bolha_inteira/` e usa as respostas de `respostas_*/`. Fundo azul-noite → roxo, padrão estrelas. Hashtag do efeito: `#meu2027vaiser`. Legenda nunca promete dinheiro. Evitar sobre rosto de banco: LIMPA O NOME (grana_07) e O EX VOLTA (amor_03). **Régua própria:** o pico vem de 26/12 a 03/01.

#### C05-V1 · N-video · "Estoura a bolha" · 12 s
- **Objetivo:** estreia e vitrine para o pico de fim de ano.
- **Gancho (0–2 s):** título MEU 2027 VAI SER… + as 3 bolhas flutuando + "Estoura a bolha e vê seu 2027".

| Tempo | Na tela | Som |
|---|---|---|
| 0,0–2,0 | Gancho. Título e 3 bolhas | trilha 96 bpm |
| 2,0–3,0 | "Faz biquinho 😗" (se o hint publicado for "Toque na tela": "Toca na tela 👆"; conferir no D0) | — |
| 3,0–4,5 | Bolha AMOR estoura → PAQUERA NO CHURRASCO (amor_02) | estouro, brilho |
| 4,5–6,0 | Bolha GRANA → O 13º DURA ATÉ O DIA 3 (grana_02) | estouro |
| 6,0–7,5 | Bolha FUTEBOL → TÍTULO VEM (CONFIA) (futebol_01) | estouro |
| 7,5–9,5 | "Resumindo: igual 2026 😂" | pop |
| 9,5–12,0 | CF com "Qual saiu pra você?" | assinatura |

- **Legenda:** `Estoura as bolhas e vê como vai ser seu 2027 ✨ Qual saiu pra você? Filtro: Meu 2027 vai ser 🔎 procura na lupa`
- **Hashtags:** `#meu2027vaiser #previsao2027 #2027 #filtro #filtrotiktok`
- **Chamada:** "Procura na lupa 🔎 Meu 2027 vai ser".
- **Som:** assinatura C05. Teste de som: não.
- **Capa:** "COMO VAI SER SEU 2027? ✨".
- **Quando:** D1. Alvo **qua 09/12, 18h**.
- **Quem:** nuvem até 04/12; Montador.

#### C05-V2 · N-video · "Ceia: cada um vê o seu" · 11 s
- **Objetivo:** levar o filtro para a ceia, com cada pessoa abrindo no próprio celular.
- **Gancho (0–2 s):** 🎄 + bolhas + "Ceia hoje: cada um vê seu 2027".

| Tempo | Na tela | Som |
|---|---|---|
| 0,0–2,0 | Gancho. Bolhas e enfeites desenhados | trilha 100 bpm, sininho |
| 2,0–5,0 | "Rodada 1": SOGRA TE ADORA (amor_07) · ENCHE O COFRINHO (grana_05) · GANHA O CLÁSSICO (futebol_02) | 3 estouros |
| 5,0–8,0 | "Rodada 2": CRUSH CHAMA PRIMEIRO (amor_05) · ACHA GRANA NA CALÇA (grana_08) · SEM CORNETAR (MENTIRA) (futebol_04) | 3 estouros |
| 8,0–11,0 | CF com "Cada um no seu celular 📱" | assinatura |

- **Legenda:** `Hoje tem ceia: cada um abre o filtro no seu celular e vê o 2027 🎄 Filtro: Meu 2027 vai ser 🔎 procura na lupa`
- **Hashtags:** `#meu2027vaiser #ceiadenatal #2027 #filtrotiktok #natal`
- **Chamada:** "Procura na lupa 🔎 Meu 2027 vai ser".
- **Som:** assinatura C05 + sininho. **Teste de som: sim.**
- **Capa:** "NA CEIA: CADA UM VÊ SEU 2027 🎄".
- **Quando:** data fixa **qui 24/12, 13h** (véspera: nada depois das 15h).
- **Quem:** nuvem até 18/12; Montador agenda a partir de 14/12, depois das 13h (rodada de seg 14/12 ou qui 17/12).

#### C05-M1 · M-gravacao · "Faz biquinho" · 10–12 s
- **Objetivo:** mostrar o gatilho (biquinho) funcionando.
- **Fonte de rosto:** clipe do Pexels de uma pessoa adulta mandando beijo ou fazendo biquinho. (a confirmar) se o preview dispara as bolhas com o biquinho do clipe. **Se não disparar, a peça não cai:** o Montador clica na tela (o template também estoura com toque) e o texto vira "toca na tela".
- **Gancho (`gancho.png`):** "Funciona assim 👇 faz biquinho" (ou "Funciona assim 👇 toca na tela", conforme o hint publicado e o que funcionou na gravação; a nuvem manda os dois PNGs).
- **Roteiro:** 0–3 s clipe com título e bolhas · 3–8 s biquinho (ou clique), as bolhas estouram · 8–9,5 s resultado · 9,5–12 s CF com "Faz hoje e na virada ✨".
- **Legenda:** `Funciona assim: faz biquinho e as bolhas estouram 😗 Filtro: Meu 2027 vai ser 🔎 procura na lupa` (versão toque: `Funciona assim: toca na tela e as bolhas estouram ✨ Filtro: Meu 2027 vai ser 🔎 procura na lupa`)
- **Hashtags:** `#meu2027vaiser #2027 #anonovo #filtro #filtrotiktok`
- **Som:** `assinatura.wav`. Teste de som: não.
- **Capa:** "FAZ BIQUINHO E VÊ SEU 2027 😗".
- **Quando:** alvo **dom 27/12, 19h** (pico). Se não estiver pronta, vago.
- **Quem:** Montador grava na montagem do C05 (antes de 03/12); nuvem manda o kit até 22/12.

#### C05-V3 · N-video · "Último dia de 2026" · 12 s
- **Objetivo:** o pico. Lembrar que no dia 1º dá para ver de novo, já em 2027. Convite simples, sem nada em troca.
- **Gancho (0–2 s):** relógio 🕛 + bolhas + "Último dia: vê seu 2027 agora".

| Tempo | Na tela | Som |
|---|---|---|
| 0,0–2,0 | Gancho. Bolhas e 🕛 | trilha 104 bpm |
| 2,0–4,0 | Contagem 3, 2, 1, "2027!" | bipes |
| 4,0–8,0 | Estouram: AMOR DA VIDA (DE NOVO) (amor_08) · SAI DO VERMELHO (grana_03) · GOL NOS ACRÉSCIMOS (futebol_06) | estouros, confete |
| 8,0–9,5 | "Faz hoje e de novo amanhã 👀" | pop |
| 9,5–12,0 | CF com "Qual saiu pra você?" | assinatura |

- **Legenda:** `Último dia de 2026: vê o seu 2027 agora e de novo amanhã 👀 Filtro: Meu 2027 vai ser 🔎 procura na lupa`
- **Hashtags:** `#meu2027vaiser #reveillon #anonovo #2027 #filtrotiktok`
- **Som:** assinatura C05. Teste de som: não.
- **Capa:** "ÚLTIMO DIA: VÊ SEU 2027 ✨".
- **Quando:** data fixa **qui 31/12, 14h**.
- **Quem:** nuvem até 26/12; Montador agenda a partir de 21/12, depois das 14h (rodada de seg 21/12).

---

### C02 · Meu próximo carro

Template Randomizer2D, 26 cartas. **Vinculado ao desafio.** Fundo grafite com tracejado amarelo de asfalto (como a demo testada da biblioteca). O carro aparece só como emoji 🚗 ou nas nossas cartas: nenhum modelo reconhecível. Hashtag do efeito: `#meuproximocarro`. Evitar sobre rosto de banco: SÓ PEGA NO TRANCO (5) e MOVIDO A ESPERANÇA (18). Preferir 12 QUITADO E NO MEU NOME, 17 AUTOMÁTICO E COM AR GELADO, 24 USADO COM CHEIRO DE NOVO.

#### C02-V1 · N-video · "Roleta do próximo carro" · 10 s
- **Objetivo:** estreia. Falar com quem dirige, sem vender nada e sem citar loja.
- **Gancho (0–2 s):** carta 2 SUV EM 72 PARCELAS + "O filtro sorteia seu próximo carro".

| Tempo | Na tela | Som |
|---|---|---|
| 0,0–1,9 | Gancho. Carta 2 | trilha 116 bpm |
| 1,9–2,6 | Título com "toque na tela" + dedo 👆 | bi-bi, toque |
| 2,6–6,6 | Roleta para na 5 SÓ PEGA NO TRANCO. Confete | tiques, plim |
| 6,6–8,0 | "Bora empurrar 😅" | pop |
| 8,0–10,0 | CF com "Qual saiu pra você?" | bi-bi |

- **Legenda:** `O filtro sorteia seu próximo carro 🚗 Qual saiu pra você? Filtro: Meu próximo carro 🔎 procura na lupa`
- **Hashtags:** `#meuproximocarro #filtro #filtrotiktok #carro #motorista`
- **Chamada:** "Procura na lupa 🔎 Meu próximo carro".
- **Som:** assinatura C02. Teste de som: não.
- **Capa:** "QUAL VAI SER SEU PRÓXIMO CARRO?".
- **Quando:** D1. Alvo **sex 13/11, 19h**.
- **Quem:** nuvem até 09/11 (a demo da biblioteca já é o rascunho); Montador.

#### C02-V2 · N-video · "Só paro quando sair ZERO KM" · 14 s
- **Objetivo:** mostrar que dá para girar de novo e de novo. Desafio sem prêmio.
- **Gancho (0–2 s):** carta 20 CONSÓRCIO QUE NUNCA SAI + 🤞 + "Só paro quando sair ZERO KM".

| Tempo | Na tela | Som |
|---|---|---|
| 0,0–2,0 | Gancho. Carta 20 pequena, 🤞 | trilha 120 bpm |
| 2,0–4,5 | Giro 1 → 7 BICICLETA (POR ENQUANTO). "Não. De novo." | tiques, bi-bi |
| 4,5–7,0 | Giro 2 → 15 EMPRESTADO DO CUNHADO. "Quase…" | tiques |
| 7,0–10,0 | Giro 3 → 4 ZERO KM (FINALMENTE). Confete, "SAIU! 🎉" | plim, bi-bi duplo |
| 10,0–11,5 | "Agora só falta o dinheiro 😅" | pop |
| 11,5–14,0 | CF com "Quantas tentativas você precisou?" | assinatura |

- **Legenda:** `Quantas tentativas até sair zero km? 😂 Filtro: Meu próximo carro 🔎 procura na lupa ou no meu perfil`
- **Hashtags:** `#meuproximocarro #zerokm #filtrotiktok #carro #humor`
- **Som:** assinatura C02. **Teste de som: sim.**
- **Capa:** "SÓ PARO QUANDO SAIR ZERO KM".
- **Quando:** D6. Alvo **qua 18/11, 18h**.
- **Quem:** nuvem até 15/11; Montador.

#### C02-V3 · N-video · "Quando perguntam do carro novo" · 11 s
- **Objetivo:** dar um alvo para mandar o vídeo (o parente do almoço de domingo).
- **Gancho (0–2 s):** carta 10 COM PORTA DE OUTRA COR + "POV: perguntaram de novo do carro".

| Tempo | Na tela | Som |
|---|---|---|
| 0,0–2,0 | Gancho. Carta 10 | trilha 112 bpm |
| 2,0–3,0 | "Pergunta pro filtro, então 🙄" + dedo 👆 | toque |
| 3,0–7,0 | Roleta para na 18 MOVIDO A ESPERANÇA | tiques, plim |
| 7,0–8,5 | "Assunto encerrado ✅" | pop |
| 8,5–11,0 | CF com "Manda pra quem sempre pergunta" | bi-bi |

- **Legenda:** `Pra quem vive perguntando quando você vai trocar de carro. Manda pra essa pessoa 😅 Filtro: Meu próximo carro 🔎`
- **Hashtags:** `#meuproximocarro #filtrotiktok #carro #almocodedomingo #humor`
- **Som:** assinatura C02. Teste de som: não.
- **Capa:** "QUANDO VOCÊ VAI TROCAR DE CARRO?".
- **Quando:** alvo **dom 22/11, 19h** (domingo de almoço em família).
- **Quem:** nuvem até 19/11; Montador.

#### C02-M1 · M-gravacao · "Funciona assim" · 10–12 s
- **Objetivo:** prova do filtro num rosto.
- **Fonte de rosto:** clipe do Pexels (2.5), fundo neutro, **fora de carro** (evita logo e modelo). Cartas leves (12, 17, 24).
- **Gancho (`gancho.png`):** "Funciona assim 👇 qual vai sair?"
- **Roteiro:** 0–3 s clipe com o título · 3–7 s clique, gira · 7–9,5 s resultado · 9,5–12 s CF com "Qual saiu pra você?".
- **Legenda:** `Funciona assim: toca na tela e o filtro sorteia seu próximo carro. Filtro: Meu próximo carro 🔎 procura na lupa`
- **Hashtags:** `#meuproximocarro #filtro #filtrotiktok #carro #motorista`
- **Som:** `assinatura.wav`. Teste de som: não.
- **Capa:** "FUNCIONA ASSIM 👇 MEU PRÓXIMO CARRO".
- **Quando:** alvo **qui 26/11, 18h** (véspera da Black Friday; o vídeo não fala de loja nem de compra). Se não estiver pronta, vago.
- **Quem:** Montador grava na montagem do C02; nuvem manda o kit até 22/11.

---

### C09 · Perrengue no volante

Template Blind Rank, versão padrão de 10 itens (`assets/cartas/carta_01` a `carta_10`), marcadores em `assets/marcadores/`. É o único que não é sorteio: a graça é o arrependimento. Fundo laranja e grafite, listras zebradas. Carro só nas nossas cartas, sempre parado. Hashtag do efeito: `#perrenguenovolante`. **Sem M-gravacao:** na versão de 10 itens, QUEM NÃO DÁ SETA (7) sempre aparece sobre o rosto, e o R2 manda evitar essa carta em rosto de banco. A QA pode liberar depois; aí entra uma C09-M1 num horário vago.

#### C09-V1 · N-video · "Gastei o 1 cedo demais" · 14 s
- **Objetivo:** estreia. Mostrar a regra (você não vê o próximo) e o arrependimento.
- **Gancho (0–2 s):** painel 1–10 + carta 1 BALIZA COM PLATEIA já voando para o 1 + "Ranking às cegas: perrengue no volante".

| Tempo | Na tela | Som |
|---|---|---|
| 0,0–2,0 | Gancho. Título RANKING DOS PERRENGUES. Carta 1 vai para a vaga 1. "Certeza: isso é o pior 😤" | trilha 100 bpm, pisca-alerta |
| 2,0–8,0 | Itens um por vez (`ranking`, ~0,9 s cada): 4 → vaga 5, 6 → vaga 7, 5 → vaga 9, 9 → vaga 8, 3 → vaga 4, 8 → vaga 6 | vush + pop |
| 8,0–10,0 | Aparece a 2 PNEU FURADO SEM ESTEPE. Tremida. "NÃO! Cadê o 1? 😩" → vai para a vaga 2 | tremida, pop |
| 10,0–12,0 | Últimos: 10 BATERIA ARRIADA → 3, 7 QUEM NÃO DÁ SETA → 10 | vush + pop |
| 12,0–14,0 | Lista completa + CF com "Qual você punha em 1º?" | assinatura |

- **Legenda:** `Ranking às cegas: você não vê o próximo perrengue. Qual você punha em 1º? Filtro: Perrengue no volante 🔎`
- **Hashtags:** `#perrenguenovolante #filtro #filtrotiktok #motorista #ranking`
- **Chamada:** "Procura na lupa 🔎 Perrengue no volante".
- **Som:** assinatura C09. Teste de som: não.
- **Capa:** "RANKING ÀS CEGAS: PERRENGUE NO VOLANTE".
- **Quando:** D1. Alvo **ter 17/11, 18h**.
- **Quem:** nuvem até 09/11; Montador.

#### C09-V2 · N-video · "O 1 só no último" · 14 s
- **Objetivo:** regra fácil de copiar ("duvido você aguentar"), sem prêmio.
- **Gancho (0–2 s):** vaga 1 com 🔒 piscando + "Regra: o 1 só no último".

| Tempo | Na tela | Som |
|---|---|---|
| 0,0–2,0 | Gancho. Vaga 1 trancada | trilha 104 bpm |
| 2,0–10,0 | 9 itens vão para as vagas 2 a 10. Na 10 BATERIA ARRIADA: "Ai… regra é regra" → vaga 2 | vush + pop, pisca-alerta |
| 10,0–12,0 | Último item, 5 LAVAR O CARRO E CHOVER, cai no 1. "Oficialmente o pior perrengue da vida 🤷" | plim |
| 12,0–14,0 | Lista + CF com "Duvido você aguentar" | assinatura |

- **Legenda:** `Regra: o 1 só no último. Duvido você aguentar 😂 Filtro: Perrengue no volante 🔎 procura na lupa`
- **Hashtags:** `#perrenguenovolante #filtrotiktok #ranking #carro #humor`
- **Som:** assinatura C09. **Teste de som: sim.**
- **Capa:** "REGRA: O 1 SÓ NO ÚLTIMO 🔒".
- **Quando:** D5. Alvo **sáb 21/11, 15h**.
- **Quem:** nuvem até 18/11; Montador.

#### C09-V3 · N-video · "Nos comentários é fácil" (card de resposta) · 12 s
- **Objetivo:** devolver a discussão dos comentários para o filtro.
- **Gancho (0–2,5 s):** card desenhado "O que mais apareceu nos comentários:" + **resumo em palavras nossas** do que muita gente escreveu nos posts do C09 (por exemplo, qual perrengue mais gente pôs em 1º). **Não copiar o texto de ninguém**, nem nome, foto ou @. + "Nos comentários é fácil 😏". O Montador manda o resumo até qui 26/11. Se não houver padrão claro, o card sai e fica só o texto (nunca inventar comentário).

| Tempo | Na tela | Som |
|---|---|---|
| 0,0–2,5 | Card do comentário + gancho | trilha 100 bpm |
| 2,5–4,0 | "Você já viu a lista toda 😏" | pop |
| 4,0–10,0 | Ranking rápido em que o próximo item aparece como "?" até entrar | vush + pop |
| 10,0–12,0 | CF com "No filtro você não vê o próximo" | assinatura |

- **Legenda:** `Nos comentários é fácil, você já viu a lista. No filtro, não 😏 Filtro: Perrengue no volante 🔎 procura na lupa`
- **Hashtags:** `#perrenguenovolante #filtrotiktok #ranking #vidademotorista #humor`
- **Som:** assinatura C09. Teste de som: não.
- **Capa:** "NOS COMENTÁRIOS É FÁCIL 😏".
- **Quando:** alvo **dom 29/11, 19h**.
- **Quem:** Montador manda o resumo dos comentários até 26/11; nuvem renderiza até 27/11 (prazo de 3 dias vira 2 nesta peça, porque depende dos comentários); Montador.

---

### C06 · Meu amigo secreto

Template Randomizer2D, 26 cartas. **Vinculado ao desafio.** Pico de uso de 14 a 25/12; depois do Natal, ninguém usa. Fundo roxo com dourado, padrão estrelas, 🎁. Hashtag do efeito: `#meuamigosecreto`. Nunca citar Black Friday. Evitar sobre rosto de banco: DESODORANTE (É INDIRETA?) (15). Preferir 10 O QUE EU PEDI (MILAGRE), 20 PLANTINHA QUE NÃO VAI DURAR, 5 PANETONE QUE NINGUÉM COME.

#### C06-V1 · N-video · "Todo ano é meia?" · 10 s
- **Objetivo:** estreia na época do sorteio dos nomes.
- **Gancho (0–2 s):** carta 1 MEIA (DE NOVO) + "Todo ano é meia no amigo secreto?".

| Tempo | Na tela | Som |
|---|---|---|
| 0,0–2,0 | Gancho. Carta 1 | trilha 112 bpm, sininho |
| 2,0–3,0 | 🎁 treme + dedo 👆 | toque |
| 3,0–7,0 | Roleta para na 3 CANECA COM FRASE DE COACH | tiques, pop de caixa |
| 7,0–8,5 | "Pelo menos não é meia 😅" | pop |
| 8,5–10,0 | CF com "O que você vai ganhar? 🎁" | assinatura |

- **Legenda:** `Todo ano é meia? 🧦 Vê o que você vai ganhar no amigo secreto. Filtro: Meu amigo secreto 🔎 procura na lupa`
- **Hashtags:** `#meuamigosecreto #amigosecreto #amigooculto #filtro #filtrotiktok`
- **Chamada:** "Procura na lupa 🔎 Meu amigo secreto".
- **Som:** assinatura C06. Teste de som: não.
- **Capa:** "O QUE VOCÊ VAI GANHAR NO AMIGO SECRETO? 🎁".
- **Quando:** D1. Alvo **qua 25/11, 18h** (jogo às 20h).
- **Quem:** nuvem até 20/11; Montador.

#### C06-M1 · M-gravacao · "O presente abre" · 10–12 s
- **Objetivo:** prova do filtro num rosto.
- **Fonte de rosto:** clipe do Pexels (2.5). Cartas leves (10, 20, 5).
- **Gancho (`gancho.png`):** "Funciona assim 👇 o presente abre".
- **Roteiro:** 0–3 s clipe com o presente fechado na cabeça · 3–7 s clique, gira e abre · 7–9,5 s resultado · 9,5–12 s CF com "O que você vai ganhar?".
- **Legenda:** `Funciona assim: toca na tela e o presente abre 🎁 Filtro: Meu amigo secreto 🔎 procura na lupa`
- **Hashtags:** `#meuamigosecreto #amigosecreto #filtro #filtrotiktok #natal`
- **Som:** `assinatura.wav`. Teste de som: não.
- **Capa:** "FUNCIONA ASSIM 👇 MEU AMIGO SECRETO".
- **Quando:** alvo **ter 01/12, 18h**. Se não estiver pronta, vago.
- **Quem:** Montador grava na montagem do C06; nuvem manda o kit até 27/11.

#### C06-V3 · N-video · "Amigo secreto da firma" · 12 s
- **Objetivo:** dar o alvo "pessoal do setor", na véspera da sexta das confraternizações (estimativa da equipe; a confirmar).
- **Gancho (0–2 s):** carta 14 SANDUICHEIRA (EU JÁ TENHO 2) + "Amigo secreto da firma é sempre igual".

| Tempo | Na tela | Som |
|---|---|---|
| 0,0–2,0 | Gancho. Carta 14 | trilha 116 bpm |
| 2,0–5,0 | "Todo ano…" + cartas 3, 22, 25 e 13 passando (0,7 s cada) | vush |
| 5,0–5,7 | "Esse ano vai ser…" + dedo 👆 | toque |
| 5,7–9,5 | Roleta para na 23 UM PRESENTÃO (FOI ENGANO) | tiques, pop de caixa |
| 9,5–12,0 | CF com "Manda pro pessoal do setor" | assinatura |

- **Legenda:** `Amigo secreto da firma é sempre igual 😂 Manda pro pessoal do setor. Filtro: Meu amigo secreto 🔎 procura na lupa`
- **Hashtags:** `#meuamigosecreto #amigosecretodafirma #confraternizacao #filtrotiktok #humor`
- **Som:** assinatura C06. Teste de som: não.
- **Capa:** "AMIGO SECRETO DA FIRMA 🎁".
- **Quando:** data fixa **qui 17/12, 18h**.
- **Quem:** nuvem até 13/12; Montador agenda a partir de 07/12, depois das 18h (ou na rodada de qui 10/12).

#### C06-V2 · N-video · "Pausa e vê seu presente" · 9 s
- **Objetivo:** a semana da troca na família.
- **Gancho (0–2 s):** cartas já passando + "Pausa o vídeo e vê seu presente".
- **Roteiro:** 0–7 s texto fixo "PAUSA AGORA ⏸️🎁" e **20 das 26 cartas** (as mais engraçadas) a cada **0,35 s**, em ordem de brilho parecido · 7–9 s CF com "Qual pegou?".
- **Legenda:** `Semana da troca: pausa o vídeo e vê o seu presente 🎁 Qual pegou? Filtro: Meu amigo secreto 🔎 procura na lupa`
- **Hashtags:** `#meuamigosecreto #amigosecreto #amigooculto #natal #filtrotiktok`
- **Som:** tique a cada carta + sininho no fim, trilha 128 bpm. **Teste de som: sim.**
- **Capa:** "PAUSA E VÊ SEU PRESENTE ⏸️🎁".
- **Quando:** data fixa **seg 21/12, 19h**.
- **Quem:** nuvem até 17/12; Montador agenda a partir de 11/12 (rodada de seg 14/12).

---

### C07 · Simpatia da Virada

Template Randomizer2D, 26 cartas. **Vinculado ao desafio.** Pico de 26/12 a 01/01; depois de 03/01 quase ninguém procura. Fundo turquesa → amarelo, chuva de confete. Hashtag do efeito: `#simpatiadavirada`. Sem emoji de mãos rezando nem símbolo religioso. Evitar sobre rosto de banco: ROUPA ÍNTIMA AMARELA (PSIU) (12). Preferir 17 12 DESEJOS NUM PAPELZINHO, 19 ENTRAR COM O PÉ DIREITO, 25 LIGAR PRA VÓ NA VIRADA.

#### C07-V1 · N-video · "O filtro escolhe sua simpatia" · 10 s
- **Objetivo:** estreia. Ensinar a regra: saiu, tem que cumprir.
- **Gancho (0–2 s):** carta 1 PULAR 7 ONDAS (VALE NO BALDE) + "O filtro escolhe sua simpatia da virada".

| Tempo | Na tela | Som |
|---|---|---|
| 0,0–2,0 | Gancho. Carta 1 | trilha 108 bpm |
| 2,0–2,8 | Título com "toque na tela" + dedo 👆 | toque |
| 2,8–6,8 | Roleta para na 14 VARRER O AZAR PRA FORA. Confete | tiques, estouro |
| 6,8–8,2 | "Ordem é ordem 🧹" | pop |
| 8,2–10,0 | CF com "Saiu, tem que cumprir 😅" | assinatura |

- **Legenda:** `O filtro escolhe sua simpatia de Ano-Novo. Saiu, tem que cumprir 😅 Filtro: Simpatia da Virada 🔎 procura na lupa`
- **Hashtags:** `#simpatiadavirada #simpatiasdeanonovo #anonovo #filtro #filtrotiktok`
- **Chamada:** "Procura na lupa 🔎 Simpatia da Virada".
- **Som:** assinatura C07. Teste de som: não.
- **Capa:** "QUAL VAI SER SUA SIMPATIA? ✨".
- **Quando:** D1. Alvo **qui 10/12, 18h**.
- **Quem:** nuvem até 04/12; Montador.

#### C07-M1 · M-gravacao · "Saiu, cumpriu" · 10–12 s
- **Objetivo:** prova do filtro num rosto, no 1º dia do pico.
- **Fonte de rosto:** clipe do Pexels (2.5). Cartas leves (17, 19, 25).
- **Gancho (`gancho.png`):** "Funciona assim 👇 saiu, cumpriu".
- **Roteiro:** 0–3 s clipe com MINHA SIMPATIA PRA 2027 É… na cabeça · 3–7 s clique, gira · 7–9,5 s resultado · 9,5–12 s CF com "Faz e me conta em 2027".
- **Legenda:** `Funciona assim: toca na tela e sai a sua simpatia da virada ✨ Filtro: Simpatia da Virada 🔎 procura na lupa`
- **Hashtags:** `#simpatiadavirada #simpatiasdeanonovo #reveillon #filtro #filtrotiktok`
- **Som:** `assinatura.wav`. Teste de som: não.
- **Capa:** "FUNCIONA ASSIM 👇 SIMPATIA DA VIRADA".
- **Quando:** alvo **sáb 26/12, 15h**. Se não estiver pronta, vago.
- **Quem:** Montador grava na montagem do C07 (antes de 03/12); nuvem manda o kit até 21/12.

#### C07-V2 · N-video · "Não sabe qual simpatia fazer?" · 11 s
- **Objetivo:** pegar quem está procurando "simpatia de Ano-Novo" na semana do pico e deixar o filtro escolher. Tema só de virada (a versão antiga, "o carro nesse estado", foi trocada na revisão: puxava para o público da loja e fugia do tema).
- **Gancho (0–2 s):** cartas 7 COMER 12 UVAS (SEM PRESSA), 11 3 PULINHOS À MEIA-NOITE e 5 TUDO BRANCO (ATÉ A MEIA) em leque + "Não sabe qual simpatia fazer? 🤔".

| Tempo | Na tela | Som |
|---|---|---|
| 0,0–2,0 | Gancho. As 3 cartas em leque | trilha 108 bpm |
| 2,0–3,0 | "Deixa o filtro escolher 👆" + dedo | toque |
| 3,0–7,0 | Roleta para na 17 12 DESEJOS NUM PAPELZINHO. Confete | tiques, estouro |
| 7,0–8,5 | "Essa dá pra cumprir ✍️" | pop |
| 8,5–11,0 | CF com "Qual saiu pra você?" | assinatura |

- **Legenda:** `Não sabe qual simpatia de Ano-Novo fazer? Deixa o filtro escolher ✨ Filtro: Simpatia da Virada 🔎 procura na lupa`
- **Hashtags:** `#simpatiadavirada #simpatiasdeanonovo #anonovo #reveillon #filtrotiktok`
- **Chamada:** "Procura na lupa 🔎 Simpatia da Virada".
- **Som:** assinatura C07. **Teste de som: sim.**
- **Capa:** "NÃO SABE QUAL SIMPATIA FAZER? 🤔".
- **Quando:** data fixa **ter 29/12, 19h**.
- **Quem:** nuvem até 24/12; Montador agenda a partir de 19/12 (rodada de seg 21/12).

#### C07-V3 · N-video · "Último dia: pausa e vê a sua" · 9 s
- **Objetivo:** o dia de maior procura. Sortear e gravar cumprindo.
- **Gancho (0–2 s):** cartas já passando + "Pausa e vê sua simpatia ⏸️".
- **Roteiro:** 0–1,5 s contagem curta "3, 2, 1…" · 1,5–7 s texto fixo "PAUSA AGORA ⏸️✨" e **16 das 26 cartas** (as mais fáceis de cumprir) a cada **0,35 s** · 7–9 s CF com "Grava cumprindo ✨".
- **Legenda:** `Último dia de 2026: pausa o vídeo, vê sua simpatia e grava cumprindo ✨ Filtro: Simpatia da Virada 🔎`
- **Hashtags:** `#simpatiadavirada #simpatiasdeanonovo #reveillon #ultimodiadoano #filtrotiktok`
- **Som:** bipes + tique a cada carta + estouro no fim. Teste de som: não.
- **Capa:** "PAUSA E VÊ SUA SIMPATIA ⏸️".
- **Quando:** data fixa **qui 31/12, 11h** (simpatia se prepara de manhã; feriado só até 15h).
- **Quem:** nuvem até 26/12; Montador agenda a partir de 21/12, depois das 11h (rodada de seg 21/12).

---

### Peças gerais (fora do limite por efeito)

#### G-V1 · N-video · "Como achar nossos filtros" · 10 s
- **Objetivo:** tirar o atrito da busca. Vai fixado no lugar 3 do perfil enquanto não houver um bom vídeo da loja (PERFIL.md, seção 6).
- **Gancho (0–2 s):** "Não achou o filtro? É fácil" + 🔎 grande.
- **Roteiro:** 0–2 s gancho · 2–4 s "1. Toca na lupa 🔎" · 4–6 s "2. Digita o nome do filtro ⌨️" · 6–8 s "Ou entra no meu perfil, na aba de efeitos ✨" (**só se** a aba já apareceu na conferência da seção 2.2; senão: "Ou toca no nome do filtro no vídeo de quem usou ✨"; texto trocado em 06/11 para deixar claro que é o vídeo de outra pessoa, porque o nosso não tem a etiqueta) · 8–10 s os nomes dos filtros já aprovados, um embaixo do outro, + símbolo do perfil. Ícones nossos; **nada que imite a tela ou o logo do TikTok**. O caminho exato dentro do app é (a confirmar); por isso o vídeo só diz "lupa" e "perfil".
- **Legenda:** `Viu um filtro nosso e não achou? Procura o nome na lupa 🔎 ou entra no meu perfil, na aba de efeitos ✨` (sem a aba: `Viu um filtro nosso e não achou? Procura o nome na lupa 🔎 ou toca no nome dele no vídeo de quem usou ✨`)
- **Hashtags:** `#filtro #filtrotiktok #efeitostiktok`
- **Som:** tecla (digitar) + plim, trilha 100 bpm.
- **Capa:** "COMO ACHAR NOSSOS FILTROS 🔎".
- **Quando:** alvo **seg 16/11, 19h** (com 2 ou 3 efeitos no ar). Saiu da qui 19/11 na revisão: a busca é onde mais se perde gente (R3), então o tutorial vem cedo.
- **Quem:** nuvem até sex 13/11, com os nomes já publicados; Montador.

#### G-V2 · N-video · "3 filtros pro fim de ano" · 10 s
- **Gancho:** "3 filtros pro fim de ano" + os 3 títulos (C06, C05, C07).
- **Roteiro:** 0–2 s gancho · 2–8 s um título por vez com 1 carta de cada (`slides`, zoom) · 8–10 s "Procura na lupa 🔎" + os 3 nomes.
- **Legenda:** `Filtros pro fim de ano: Meu amigo secreto, Meu 2027 vai ser e Simpatia da Virada 🎄 Procura na lupa 🔎`
- **Hashtags:** `#filtrotiktok #amigosecreto #natal #anonovo #2027`
- **Som:** sininho + estouro + plim.
- **Capa:** "3 FILTROS PRO FIM DE ANO 🎄".
- **Quando:** alvo **sáb 12/12, 19h** (só se C05 e C07 estiverem aprovados; senão, sai só com os aprovados).
- **Quem:** nuvem até 09/12; Montador.
- **Entregue (06/11):** G-V1 (`G-V1.mp4` sem a aba e `G-V1-aba.mp4` com a aba) e G-V2 prontos em `videos/gerais/`, com capas, legendas, prévia e `roteiros-videos.md`; `render_gerais.py` refaz com os nomes aprovados reais.

---

## 4. Calendário único (substitui a seção 3.1 do `plano-curto-prazo.md`)

### 4.1 A regra (vale para qualquer data de aprovação)

| Momento | O que acontece |
|---|---|
| **D0 = dia da aprovação** (status "Active") | Montador: Effect House → Manage → Share, salva o QR e o link e manda para a nuvem com o nome publicado. Perfil, bio e link conforme `PERFIL.md`. Agenda o V1 para o D1. Nuvem: se o nome publicado for diferente, refaz o V1 no mesmo dia. **Nenhum post de efeito antes da aprovação.** **PC desligado no D0** (o Montador só trabalha com o PC do Vini ligado): tudo isso na próxima vez que o PC ligar, e o V1 vai para o 1º horário nobre livre depois disso. |
| **D1 = dia seguinte à aprovação** | V1 no horário nobre. Comentário fixado. Respostas sempre que o PC estiver ligado (meta: nas 2 primeiras horas; nunca mais de 24 h sem responder quem pergunta o nome) |
| **D3** | 1ª leitura (seção 6) |
| **D4 a D6** | 2ª peça do efeito |
| **D7** | Revisão (seção 6) |
| **D8 em diante** | 3ª e 4ª peças, ou nas datas fixas |

**Ordem quando dois efeitos são aprovados no mesmo dia:** em novembro, C01 → C08 → C02 → C09 (futebol primeiro, para a base antiga). Em dezembro, C05 → C07. O segundo estreia no dia seguinte ao primeiro. **Se só o C08 sair** (C01 atrasado ou reprovado), o C08 vira o 1º post da conta e leva o comentário fixado longo.

**Quando dois posts disputam o mesmo horário, fica com o nobre:** (1) a estreia; (2) a peça presa a uma data fixa; (3) o efeito vinculado ao desafio, enquanto o desafio estiver aberto; (4) o efeito com mais vídeos novos nos últimos 7 dias. O outro vai para as 15h do mesmo dia (se respeitar as regras abaixo) ou para o próximo dia livre.

**Regras que não mudam:**
- No máximo **2 posts por dia na conta** (loja conta), com **3 h ou mais** entre eles.
- **Uma estreia por dia.** Nunca 2 peças do mesmo efeito no mesmo dia.
- **Sem post de efeito:** sex 27/11 (Black Friday, dia da loja) e qui 03/12 (dia seguinte à última rodada).
- **Nada durante jogo grande:** sáb 28/11 das 16h às 20h; qua 02/12 à noite (última rodada); dom 06/12 durante a final.
- Peça M que não estiver pronta na véspera **não é trocada**: o horário fica vago ou vai para a loja.

### 4.2 Horários (Brasília)

| Faixa | Horário | Uso |
|---|---|---|
| **N (nobre)** | **18h** de terça a quinta · **19h** de sexta a segunda | V1 e peças principais |
| **T (tarde)** | **15h** | 2º post de efeito no dia, sábado de jogo, feriados |
| **L (loja)** | **12h30** | Vídeos da loja |
| Dia de jogo grande | 2 a 3 h antes do jogo | Peças do C01 |
| 24/12 e 31/12 | até 15h · 25/12 e 01/01: de 14h a 18h | Festas (opinião da equipe) |

Base: R1 (terça a quinta, das 15h às 21h; 10h–12h fraco) e os planos de lançamento. **Depois de 2 semanas (~25/11)**, o Montador olha TikTok Studio → Análises → Seguidores e a equipe troca N e T pelos 2 horários mais ativos.

### 4.3 Datas fixas

Feriado 15/11 (dom) · feriado 20/11 (sex) · final da Sul-Americana 21/11 (19h30) ✅ · Black Friday 27/11 · final da Libertadores 28/11 (17h) ✅ · última rodada ~02/12 ⚠️ · final da Copa do Brasil 06/12 (hora a confirmar) ✅ · 2ª parcela do 13º 18/12 ✅ · véspera de Natal 24/12 · Natal 25/12 · Réveillon 31/12 · 01/01. (Fonte das datas de futebol: `plano-curto-prazo.md`, seção 3.)

### 4.4 Tabela-alvo, de 06/11/2026 a 03/01/2027

Aprovações prováveis (a confirmar): **C01 e C08 ter 10/11** · **C02 qui 12/11** (envio provável 07 a 09/11) · **C09 seg 16/11** (envio provável 09 a 13/11; prazo 17/11) · **C06 ter 24/11** (envio 20/11) · **C05 e C07 ter 08/12** (envio 03/12). Se uma aprovação mudar, valem as regras da 4.1 e da 4.5.

**Toda célula "Loja" = só se houver vídeo da loja pronto.** Hoje ninguém produz esses vídeos (seção 5.3). Sem vídeo, o horário fica vazio. Eles não fazem parte da meta dos efeitos.

| Data | Post 1 | Post 2 | Notas |
|---|---|---|---|
| sex 06 a seg 09/11 | — | — | Montador: teste do TikTok Studio **sem publicar** (seção 7, passo 0) e gravações M durante a montagem. Nuvem: **C01-V1 e C08-V1 prontos até sáb 07/11, 12h**; C02-V1 e C09-V1 até seg 09/11; G-V1 até sex 13/11. Se C01 ou C08 forem aprovados antes de 10/11, vale a regra 4.5 "mais cedo" |
| ter 10/11 | — | — | **D0 de C01 e C08** (alvo). Perfil trocado (`PERFIL.md`) antes do 1º vídeo |
| qua 11/11 | **C01-V1** 17h30 (estreia) | — | 1º post da conta depois do silêncio: futebol |
| qui 12/11 | **C08-V1** 18h (estreia) | — | D0 do C02 (alvo) |
| sex 13/11 | **C02-V1** 19h (estreia) | — | D3 do C01 |
| sáb 14/11 | C01-V2 15h | — | Antes dos jogos do dia (a confirmar) |
| dom 15/11 | C08-V2 19h | — | Feriado |
| seg 16/11 | Loja 12h30 | **G-V1 19h** (tutorial) | D0 do C09 (alvo) |
| ter 17/11 | **C09-V1** 18h (estreia) | — | D7 do C01 |
| qua 18/11 | C02-V2 18h | — | D7 do C08 |
| qui 19/11 | Loja 12h30 | — | D7 do C02 |
| sex 20/11 | C08-M1 19h (se pronta) | — | Feriado. Montador envia o C06 |
| sáb 21/11 | C09-V2 15h | — | Final da Sul-Americana 19h30 |
| dom 22/11 | C02-V3 19h | — | |
| seg 23/11 | Loja 12h30 | — | Semana da Black Friday. D7 do C09. Revisão de 2 semanas (formatos e horários) |
| ter 24/11 | — | — | D0 do C06 (alvo) |
| qua 25/11 | Loja 12h30 | **C06-V1** 18h (estreia) | Jogo às 20h |
| qui 26/11 | C02-M1 18h (se pronta) | — | |
| sex 27/11 | Loja 12h30 | Loja 19h | **Black Friday: nenhum post de efeito** |
| sáb 28/11 | C01-V3 14h | — | Final às 17h. Nada das 16h às 20h |
| dom 29/11 | C09-V3 19h | — | |
| seg 30/11 | Loja 12h30 | — | |
| ter 01/12 | C06-M1 18h (se pronta) | — | D7 do C06 |
| qua 02/12 | — | — | Última rodada ⚠️. Tom cuidadoso nos comentários |
| qui 03/12 | — | — | **Nenhum post de efeito.** Montador envia C05 e C07 |
| sex 04/12 | Loja 12h30 | — | |
| sáb 05/12 | — | — | |
| dom 06/12 | C01-M1 2–3 h antes da final (se pronta) | — | Final da Copa do Brasil |
| seg 07/12 | Loja 12h30 | — | |
| ter 08/12 | — | — | D0 de C05 e C07 (alvo) |
| qua 09/12 | **C05-V1** 18h (estreia) | — | |
| qui 10/12 | **C07-V1** 18h (estreia) | — | |
| sex 11/12 | Loja 12h30 | — | |
| sáb 12/12 | G-V2 19h | — | |
| seg 14/12 | Loja 12h30 | — | Começa o pico do amigo secreto |
| ter 15/12 | — | — | D7 do C05 |
| qua 16/12 | Loja 12h30 | — | D7 do C07 |
| qui 17/12 | C06-V3 18h | — | Véspera das confraternizações |
| sex 18/12 | Loja 12h30 | Loja 19h | 2ª parcela do 13º: dia da loja |
| seg 21/12 | C06-V2 19h | — | Semana da troca |
| ter 22/12 | Loja 12h30 | — | |
| qui 24/12 | C05-V2 13h | — | Véspera: nada depois das 15h |
| sex 25/12 | C08-V3 15h | — | Natal |
| sáb 26/12 | C07-M1 15h (se pronta) | — | Começa o pico da virada |
| dom 27/12 | C05-M1 19h (se pronta) | — | |
| seg 28/12 | Loja 12h30 | — | |
| ter 29/12 | C07-V2 19h | — | |
| qui 31/12 | C07-V3 11h | C05-V3 14h | Réveillon |
| sex 01/01 | — | — | Só comentários (a partir das 14h) |
| sáb 02/01 | Loja 15h | — | Volta da praia |
| dom 03/01 | — | — | Fim do plano. Balanço do selo |

Dias que não aparecem: sem post. Ficam para comentários, convites e, se a loja quiser, mais um vídeo dela (sempre dentro das regras da 4.1).

**Totais:** 29 posts de efeito (27 peças + 2 gerais; 6 deles são M e podem cair) e até 17 da loja em 8 semanas (só se existirem). Nunca mais de 2 por dia. Conferido na revisão: nenhum dia passa de 2 posts, todos os pares do mesmo dia têm 3 h ou mais, e nenhum efeito tem 2 peças no mesmo dia.

### 4.5 Se a aprovação sair em outra data

- **Mais cedo:** o V1 sai no dia seguinte, desde que não caia em 27/11 ou 03/12 e não bata com outra estreia. As outras peças andam junto (D4 a D6, depois D8 em diante), sem tirar as datas fixas de ninguém. Exemplo: C01 e C08 aprovados no sáb 07/11 → C01-V1 dom 08/11 19h, C08-V1 seg 09/11 19h, C01-V2 qua 11/11 18h, C08-V2 dom 15/11 19h (feriado, fica).
- **Mais tarde:** o V1 sai no dia seguinte à aprovação. Se a 2ª ou a 3ª peça já tinha passado, ela vai para o próximo dia livre. Peça presa a data fixa que ficou antes da aprovação **cai** (não se posta "dia de final" depois da final).
- **Reprovação:** o Montador corrige e reenvia no mesmo dia. O efeito entra na regra de "mais tarde".
- **C06:** se o envio só sair em 24/11, a estreia fica para depois de 27/11 (nunca na Black Friday).
- **C05 e C07:** se aprovados depois de 12/12, os V1 saem no dia seguinte e as peças de 24/12 a 31/12 ficam como estão. Se a aprovação sair só depois de 24/12, o V1 vira a peça daquele dia (não se somam 2 peças do mesmo efeito no dia).
- **Peça M "Funciona assim" pode subir de data** e virar a 2ª peça do efeito, se a gravação ficar pronta antes da N prevista. Ela mostra o efeito de verdade, então converte melhor (R3; a confirmar com os números do D3).
- A nuvem mantém esta tabela atualizada a cada aprovação e manda a nova versão para a coordenação.

### 4.6 Agendamento

- Se o botão **Agendar** existir (até 10 dias à frente; conta Pessoal a confirmar): o Montador agenda **toda segunda e quinta** as peças dos próximos 10 dias que já estão prontas. O V1 é agendado no D0.
- Antes de agendar, conferir que o relógio do Windows está no horário de Brasília (a confirmar se o agendador usa o fuso do PC).
- Se o botão não existir: **não mudar a conta para Empresa** (ela sairia do programa de recompensas e perderia a biblioteca geral). O Montador posta na hora, **e isso exige o PC do Vini ligado no horário**. Janela aceita: das 15h às 21h. Se o PC só ligar fora dela, a peça vai para o próximo dia livre e a nuvem é avisada. Peça de data fixa (24/12, 25/12, 31/12) sem Agendar: a coordenação combina com o Vini o PC ligado nesses dias (a confirmar).
- Post agendado sai mesmo com o PC desligado (fica no servidor do TikTok). Por isso o Agendar é o recurso mais importante do passo 0.

---

## 5. Fixados, reaquecimento da base, loja e desafio

### 5.1 Vídeos fixados (até 3)

O critério é o do `PERFIL.md`, seção 6. Em resumo:
1. **O que mais cresce:** o vídeo-cartaz do efeito com mais vídeos novos nos últimos 7 dias. Troca toda segunda.
2. **O mais novo:** o V1 do último efeito aprovado. Troca a cada D1.
3. **A loja:** o vídeo da loja com mais views em 30 dias. Até existir um bom, fica o **G-V1** (tutorial).

Nunca fixar vídeo com pessoa de banco perto de produto, nem vídeo de efeito com produto. Se "Fixar" não existir na web (a confirmar), fica sem fixados. O Vini só entra se quiser (2.6).

### 5.2 Primeira semana de reaquecimento da base antiga (alvo: 10 a 17/11)

| Dia | O que sai | Por quê |
|---|---|---|
| D0 (ter 10/11) | Perfil novo, bio, link do efeito | A pessoa que chega já entende a conta. Sem vídeo de "voltamos" (R3) |
| D1 (qua 11/11) | C01-V1, com o comentário fixado longo ("a conta mudou…") | Futebol é o assunto que trouxe essa base |
| D2 (qui 12/11) | C08-V1 | O tema mais amplo (todo mundo tem grupo da família) |
| D3 (sex 13/11) | C02-V1 | A ponte "torcedor que dirige" para o carro |
| D4 (sáb 14/11) | C01-V2 | Volta ao futebol no sábado de rodada |
| D5 (dom 15/11) | C08-V2 | Domingo de família |
| D6 (seg 16/11) | G-V1 (tutorial) e loja, se houver vídeo | Tirar o atrito da busca cedo; a loja só se existir vídeo pronto |
| D7 (ter 17/11) | C09-V1 + 1ª revisão da conta | — |

**Medir na semana:** views de seguidores e de não seguidores (se o Studio mostrar), seguidores perdidos e comentários do tipo "cadê o conteúdo antigo". **Alerta: perda acima de 1% da base numa semana (~400 seguidores).** Nesse caso, a próxima peça de efeito vira uma do C01 (a mais próxima na tabela sobe de data).
**Não fazer:** desarquivar vídeos antigos do clube; apagar ou esconder os 3 vídeos de IA da loja (só conferir se têm o rótulo de IA; R2).

### 5.3 Posts da loja (separados dos vídeos de efeito)

- **Frequência sugerida:** 2 por semana no normal; 4 na semana da Black Friday (23, 25 e 27/11 duas vezes); 2 no dia 18/12 (13º); 1 em 02/01. Sempre no horário L (12h30) ou em dia sem efeito. A loja conta no limite de 2 posts por dia.
- **Quem faz:** ninguém, hoje (a confirmar com a coordenação). A nuvem não faz vídeo de produto: o TikTok Shop proíbe vídeo de produto feito de imagem parada ou slideshow e pede produto físico em movimento (R2). O Vini não grava. **Sem vídeo, o horário da loja fica vazio** e não é preenchido com vídeo de efeito.
- **Regras:** "Divulgar conteúdo comercial" ligado em **"Sua marca"**; "publi" na legenda; música só da Biblioteca Comercial ou som nosso; rótulo de IA se tiver pessoa ou cena realista feita por IA.
- **Nunca:** nome do filtro, hashtag de efeito, pedido para usar efeito, pessoa dos clipes de banco, cupom ou brinde ligado a efeito.
- **Nenhum gancho, frase, carta, cor ou arte de efeito em vídeo da loja** (a versão anterior sugeria ecoar cartas do C02; saiu na revisão). Ligar a loja às cartas faz o efeito parecer propaganda. A loja e os efeitos só se encontram no perfil.
- **"Onde compra?" nos vídeos de efeito:** "Te chamo no direct 😉".

### 5.4 Convivência com o desafio "Nov Social Randomizer Sub Challenge"

- **Vinculados (no envio):** C02, C06 e C07; C09 e C05 se o template for aceito; C01 e C08 só se der para vincular depois (situação no `relatorio-montagem.md`).
- **Os nossos vídeos não mudam o desafio.** O que conta é o uso de outras pessoas (como o prêmio é decidido: a confirmar no `reconhecimento.md`).
- **Nunca** citar desafio, prêmio, dinheiro, "concorra" ou "ganhe" em tela, legenda, comentário ou convite. Nada em troca de uso.
- **Hashtag do desafio:** só se as regras pedirem (a confirmar). Ela entra no limite de 5.
- **Prioridade de horário:** enquanto o desafio estiver aberto (data final a confirmar; ~51 dias), os efeitos vinculados ganham o desempate da regra 4.1.
- **Guardar print das regras** aceitas em 06/11 e conferir se pedem autorização por escrito de quem aparece no vídeo (afeta só as peças M, com rosto de banco).

### 5.5 Semeadura (todo dia, pelo navegador)

- **Até 5 convites por dia na 1ª semana e até 10 depois**, por mensagem direta, espalhados no dia (a conta voltou agora de um longo silêncio e quem digita é o Montador; subir aos poucos é mais seguro), para criadores de 1 mil a 50 mil seguidores que já postam o tema. Texto pessoal, citando um vídeo da pessoa. Modelo: "Oi! Vi seu vídeo sobre [tema] e ri muito. Fiz um filtro grátis que [o que faz]. Chama **[nome]**, tá na lupa. Se curtir, usa à vontade 😊". Nunca prêmio, cupom, "sigo de volta" ou insistência. Aviso de spam: para tudo e avisa a nuvem.
- Comentários: responder sempre que o PC estiver ligado (meta: nas 2 primeiras horas); nunca link; repetir o nome do filtro quando perguntarem. Textos variados, nunca a mesma frase colada em série.

### 5.6 Amplificar quem usou (novo na revisão: alto impacto, baixo risco, zero produção)

Os vídeos de outras pessoas com o efeito são os **únicos** que têm a etiqueta clicável (R1, R3). A conta pode empurrar esses vídeos para os 40 mil seguidores sem celular:

1. **Achar:** pela página do efeito (o link do Share, aberto no navegador) ou pela hashtag do efeito. Se a página do efeito não listar vídeos na web (a confirmar), usar a busca do site com o nome do filtro.
2. **Repostar** (botão "Repostar" do compartilhar, se existir na web; a confirmar no passo 0): **até 1 por dia**, a partir do D3 de cada efeito, só nos dias com 0 ou 1 post nosso. Escolher o vídeo mais engraçado.
3. **Só repostar se:** público; pessoa que parece adulta (na dúvida, não); sem camisa ou escudo de time, marca, carro reconhecível, bebida, direção ou símbolo religioso; o resultado não deixa a pessoa mal; nada de produto ou loja no vídeo.
4. **Comentar** nos vídeos de quem usou: até 10 por dia, frase curta e diferente em cada um (ex.: "Esse resultado é muito você 😂", "Rindo até agora"). Nunca "o meu deu…" (a conta não usou o efeito). Nunca link, loja, pedido para seguir, nem pedido de nada.
5. **Nada em troca**, nunca. Não pedir para a pessoa postar de novo. Não combinar repost com ninguém.
6. **Medir:** vídeos novos do efeito nas 24 h depois do repost (como na seção 6.1). Se não mexer em 2 reposts seguidos, para e a equipe revê no D7.
7. Se a web não tiver Repostar, fica só o comentário (item 4). Não é motivo para chamar o Vini.

---

## 6. Métricas e decisões no D3 e no D7

### 6.1 O que o Montador anota

Num arquivo no PC (sugestão: `C:\Users\Pichau\Desktop\Efeitos\metricas-videos.md`), com resumo para a nuvem **toda segunda e quinta**.

**Por post (em 24 h e em 72 h; TikTok Studio → Análises do post):**
código da peça · data e hora · agendado ou na mão · views · tempo médio assistido · % que viu até o fim (se aparecer) · curtidas · comentários · compartilhamentos · salvamentos · seguidores ganhos pelo post (se aparecer) · de onde vieram as views (Para Você, Seguindo, Perfil, Busca; se aparecer) · quantos comentários pedem o nome ou dizem "não achei".

**Por efeito (Effect House → Manage → análise do efeito; todo dia do D0 ao D7, depois segunda e quinta):**
vídeos publicados com o efeito (total e novos desde a última leitura) · views · aberturas ou usos na bandeja (o nome exato na tela: a confirmar) · compartilhamentos · posição entre os efeitos (se aparecer) · status · vínculo com o desafio.
**Conversão de cada post nosso** = vídeos novos do efeito nas 24 h depois do post, menos a média das 24 h anteriores.

**Da conta (toda segunda):** seguidores ganhos e perdidos · visitas ao perfil · horários mais ativos (Análises → Seguidores) · print do Creative Center, Brasil (10 músicas e 10 hashtags) · se o link da bio está clicável.

### 6.2 Régua (vídeos de outras pessoas, contando do D1; `plano-curto-prazo.md` 5.2)

| Marco | Vai bem | Atenção | Não pegou |
|---|---|---|---|
| D3 | ≥ 50 | 20 a 49 | < 20 |
| D7 | ≥ 300 | 50 a 299 | < 50 |

C05 e C07 usam a régua dos planos deles: o pico vem depois do D14.

### 6.3 O que muda no D3

- **≥ 50:** segue a tabela.
- **20 a 49:** reforço sem vídeo novo: comentário fixado mais claro, 10 convites a mais no dia, bio com o nome do efeito.
- **< 20, com poucas views** (V1 com menos de 1.000 em 72 h): problema de alcance. A próxima peça do efeito ganha gancho novo (outra carta no quadro 1, texto mais curto, vídeo de 8 a 9 s) e vai para o outro horário (N ↔ T).
- **< 20, com views boas** (2.000 ou mais) e poucos usos: problema de conversão. Antecipar o G-V1 (se ainda não saiu), deixar o link da bio no efeito, responder todo comentário com o nome e focar os convites no tema.
- **Comentários de "não funciona", "não acho" ou "não dá pra ler":** avisar a nuvem na hora. O Montador confere o efeito. Os posts do efeito param até a resposta.

### 6.4 O que muda no D7

- **≥ 300:** o efeito ganha o fixado 1 e o desempate do horário nobre. A nuvem pode trocar a peça seguinte dele por uma variante do formato que mais converteu (dentro do limite de 3 por efeito).
- **50 a 299:** a próxima peça usa o formato campeão da conta. Mais 20 convites na semana.
- **< 50:** diagnóstico em 1 h (alcance ou conversão; `plano-curto-prazo.md` 5.3). As peças que faltam vão para o horário T ou caem, e o nobre passa ao próximo efeito. **Nada é apagado.** Nunca reenviar o efeito com outro nome.
- **Revisão de 2 semanas (~25/11):** comparar a conversão por formato (roleta, pausa, POV, ranking, M, tutorial). Ficar com **os 2 melhores** nas peças de dezembro: a nuvem troca o formato de C06-V2/V3, C05-V2/V3 e C07-V2/V3, mantendo data, nome e legenda base. Trocar N e T pelos horários da aba Seguidores.
- **Som:** se a Biblioteca Comercial existir, comparar as peças "Teste de som: sim" com a média do formato. Se não ganharem, volta ao som nosso.

---

## 7. O que o Montador faz no TikTok Studio (passos curtos)

0. **Uma vez, sem publicar:** abrir Carregar com um vídeo de teste e anotar se existem: Agendar; Editar capa → Carregar; Sons / Biblioteca de Música Comercial; modo Foto; "Conteúdo gerado por IA"; "Divulgar conteúdo comercial". Ver também: se o tiktok.com já está **logado** no navegador (se pedir login ou código, juntar no pedido único ao Vini); "Fixar" no menu de um vídeo; "Fixar" no menu de um comentário; "Repostar" no menu de compartilhar de um vídeo de outra pessoa; mensagens diretas pela web; o campo "Site" em Editar perfil; tipo de conta **Pessoal**; relógio do Windows em Brasília. Sair sem postar e mandar o resultado para a nuvem.
1. **Pegar a peça** na pasta `efeito-*/videos/` do zip (MP4, capa `.jpg`, legenda; a M fica em `Efeitos\prontos\<código>\` no PC). Nunca postar peça sem prancha aprovada pela QA.
2. **Carregar o MP4** e colar a legenda inteira (com as hashtags). Conferir: nome do filtro igual ao publicado e no máximo 5 hashtags.
3. **Capa:** Editar capa → Carregar → a capa da peça.
4. **Opções:** Quem pode ver = Todos. Comentários ligados. Dueto e costura ligados. Rótulo de IA desligado. Conteúdo comercial desligado (**na loja: ligado, "Sua marca"**). Som: o do arquivo, a não ser que a peça diga "Teste de som: sim".
5. **Agendar** para a data e a hora da tabela. Sem botão: postar na hora.
6. **Depois do post:** publicar e fixar o comentário padrão da peça (até 150 caracteres); responder comentários sempre que o PC estiver ligado (sem link; "onde compra?" → "Te chamo no direct 😉"); trocar fixados, bio e link conforme o `PERFIL.md`.
6b. **No D0 de cada efeito, depois do perfil:** abrir o perfil numa janela anônima e ver se a aba de efeitos mostra o filtro. Mandar o print para a nuvem (decide se "no meu perfil" entra nos textos, seção 2.2).
7. **Anotar as métricas** em 24 h e 72 h (seção 6) e mandar o resumo segunda e quinta.
8. **No D0 de cada efeito:** Share no Effect House (QR e link), nome publicado para a nuvem, perfil e agendamento do V1.
9. **Nunca:** apagar, deixar privado ou repostar o mesmo arquivo; usar emulador, câmera virtual ou ferramenta de postagem automática; pôr QR code no vídeo; aceitar "mudar para conta comercial"; ligar a conta como Conta Oficial da loja.

---

## 8. Pendências (a confirmar)

1. Datas reais de aprovação de cada efeito (a tabela 4.4 é alvo).
2. Botão Agendar na conta Pessoal; fuso do agendador.
3. Biblioteca de Música Comercial e modo Foto no upload pela web.
4. "Fixar" vídeo e campo "Site" pela web.
5. Clipchamp no PC (para as peças M).
6. Se o preview do Effect House grava sozinho em 9:16 com clipe do "+ Add media"; se o biquinho de um clipe dispara as bolhas do C05.
7. Caminho exato para achar um efeito pelo nome no app de hoje (lupa, aba Efeitos).
8. Regras do desafio: data final, como o prêmio é decidido, hashtag obrigatória, autorização de quem aparece.
9. Horários dos jogos de 14/11, 25/11 e 06/12 e a data da última rodada.
10. Quem produz os vídeos da loja e o catálogo atual.
11. Se o rótulo de IA aparece nos 3 vídeos antigos da loja.
12. Se o tiktok.com está logado no PC (sem isso, nada do plano anda).
13. "Fixar" comentário, "Repostar" e mensagens diretas pela web; limite de caracteres do comentário (o plano usa até 150).
14. Se a aba de efeitos aparece no perfil de conta Pessoal.
15. Se o preview do Effect House tem botão de gravar; senão, a gravação de tela do Windows 11.
16. Data final do desafio (~51 dias a partir de 06/11 dá ~27/12; a confirmar). O pico do C07 (26/12 a 01/01) pode cair quase todo depois do fim do desafio.

## 9. Arquivos relacionados

- Pesquisas: `videos/pesquisa/R1-postagem-pelo-pc.md`, `R2-direitos-e-regras.md`, `R3-formatos-sem-rosto.md`
- Biblioteca de render: `videos/lib/render.py` e `videos/lib/LEIA-ME.md`
- Perfil: `videos/perfil/PERFIL.md`
- Cartas e títulos: `efeito-*/assets/`
- Metas, régua e riscos: `plano-curto-prazo.md` (seções 1 e 5)

---

## 10. Revisão do crítico (06/11/2026)

**O que foi conferido:** este plano contra R1, R2, R3 e R5, as regras fixas, os `textos.md` e `textos.json` dos 7 efeitos (nome exato e o texto de cada carta citada), o `STATUS.md` e o `PRONTO-PARA-MONTAR.md` (só leitura). Os dias da semana de todas as datas foram conferidos. As legendas e os comentários foram contados com Python, também no "pior caso", em que o emoji conta 2 ou 3. **Não houve busca nova na web:** o limite de buscas da rodada acabou. Por isso, Agendar, Fixar comentário, Repostar e o limite do comentário seguem (a confirmar) no passo 0.

**Estava certo e ficou:** os 7 nomes estão iguais aos `textos.md`. Todas as cartas citadas existem, com o número e o texto certos. Todas as peças têm de 9 a 14 s e até 3 MP4 por efeito. Os ganchos têm até 7 palavras. As legendas têm de 92 a 112 caracteres e no máximo 5 hashtags. Nenhum dia passa de 2 posts. O "nunca" das chamadas, o rótulo de IA desligado e o som próprio estão certos.

### O que mudou e por quê

1. **Prazo dos V1 de C01 e C08: de seg 09/11 para sáb 07/11, 12h.** Os dois estão em análise desde 06/11. Se forem aprovados no fim de semana, o V1 do D1 não estaria pronto. A regra "mais cedo" (4.5) ganhou um exemplo de datas.
2. **PC desligado.** O Montador só trabalha com o PC do Vini ligado. Por isso: o D0 vale "na próxima vez que o PC ligar"; as respostas viraram "sempre que o PC estiver ligado"; e, sem o botão Agendar, a postagem tem uma janela das 15h às 21h. O Agendar virou o item mais importante do passo 0.
3. **C07-V2 trocado.** "O carro nesse estado" mirava "o cliente da loja" e puxava a virada para o carro. Isso é mistura de loja com efeito e foge da busca do pico. Entrou "Não sabe qual simpatia fazer?", na mesma data e com o mesmo limite de 3 MP4.
4. **Loja separada de verdade.** Saíram os ganchos da loja que ecoavam cartas do C02. O objetivo do C02-V1 não fala mais em "público da loja". As células "Loja" do calendário só valem se houver vídeo: hoje ninguém produz vídeo da loja, e o Vini não grava.
5. **C09-V3 sem copiar comentário de ninguém.** Em vez de reproduzir o texto de uma pessoa (direito e privacidade dela), o card resume em palavras nossas o que mais apareceu nos comentários. Se não houver padrão, o card sai.
6. **C05 com toque.** O template estoura as bolhas com biquinho **ou** toque (`textos.md` do C05). A M1 não cai mais se o biquinho do clipe não disparar: o Montador clica. O texto da V1 segue o hint publicado.
7. **Comentários com até 150 caracteres.** O comentário longo do 1º post tinha 147 (149 no pior caso), no limite. Agora tem 114. E vai no 1º post da conta, seja do C01 ou do C08.
8. **"No meu perfil, na aba de efeitos" só depois de conferir.** A aba de efeitos em conta Pessoal é (a confirmar). Prometer na tela algo que a pessoa não acha queima a confiança. O G-V1 ganhou uma versão sem a aba.
9. **G-V1 (tutorial) de qui 19/11 para seg 16/11.** A busca é onde mais se perde gente (R3, risco "Alta"). O tutorial vem assim que houver 2 ou 3 efeitos no ar.
10. **Luz piscante.** As 3 peças "pausa" trocavam a carta a cada 0,2 ou 0,25 s (4 a 5 por segundo). Agora são 3 por segundo, no máximo, em ordem de brilho parecido. Custa zero e evita o aviso que trava o vídeo (a confirmar).
11. **Gancho do C01-V2** encurtado para 6 palavras ("PAUSA AGORA ⏸️ e vê o seu").
12. **M-gravação:** reserva para gravar a tela (Windows 11), conferência de 6 a 15 s e de até 4 MB, e saída em 720p se passar.
13. **C05:** os objetivos não falam mais em "contar 2 vezes" nem em "cada uma conta como uso". O convite fica igual, mas o plano não registra intenção de inflar a contagem.
14. **Novo: seção 5.6, "Amplificar quem usou".** A conta reposta (se a web deixar) e comenta os vídeos de quem usou o efeito. São os únicos vídeos com a etiqueta clicável, e o repost leva esses vídeos aos 40 mil, sem celular e sem produção. Até 1 repost por dia e nada em troca.
15. **Convites por mensagem:** até 5 por dia na 1ª semana e até 10 depois. A conta volta de um longo silêncio, e quem digita é o Montador.
16. **Capa:** se não der para carregar a capa pela web, vale o quadro de 0,5 s. Por isso, esse quadro precisa funcionar sozinho.
17. **Passo 0 e pendências:** login no tiktok.com, Fixar comentário, Repostar, mensagem direta pela web, aba de efeitos e data final do desafio.

### O que continua em risco (não dá para resolver daqui)

- **Conversão baixa do vídeo-cartaz** (sem etiqueta). É o maior risco do plano. As respostas são a 5.6, o G-V1 cedo, as M e a medição no D3.
- **Sem Agendar e com o PC desligado**, os horários nobres e as datas fixas (24, 25 e 31/12) dependem do Vini ligar o PC.
- **Datas de aprovação.** O calendário é alvo. As regras 4.1 e 4.5 cobrem atraso e adiantamento. Uma reprovação por "duplicidade" de sorteio para a fila de envios (ordem do PRONTO de 07:10).
- **O desafio deve acabar por volta de 27/12** (a confirmar). O pico do C07 cai quase todo depois disso.
- **Datas e horários de futebol** vêm do `plano-curto-prazo.md` e não foram conferidos de novo (sem busca).
