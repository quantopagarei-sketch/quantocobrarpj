# C08 "Eu no grupo da família" · roteiros dos vídeos

**Feito em:** 06/11/2026, pelo produtor de vídeo do C08 (nuvem).
**Base:** `videos/PLANO-DE-VIDEOS.md` (versão final, com a Revisão do crítico), `videos/lib/LEIA-ME.md`, `textos.md` e as artes de `assets/` (só lidas, nada mudou lá).
**Quem usa:** a coordenação (que passa as ordens ao Montador) e o Montador.
**O Vini não faz nada.** Ninguém aparece nos vídeos N. A M1 usa só rosto de banco de vídeos com licença.
**Revisado pela QA em 06/11/2026** (`revisao-qa-videos.md`): V2 e V3 re-renderizadas (resultado da roleta mais tempo na tela), agendamento da V3 e passo 0 da M1 corrigidos aqui.

---

## 1. Resumo

| Código | Tipo | Arquivo | Duração | Tamanho | Quem faz | Quando (alvo) |
|---|---|---|---|---|---|---|
| C08-V1 | N-video | `C08-V1.mp4` | 10,0 s | 2,67 MB | Nuvem (pronto) → Montador agenda | D1 do C08 · alvo **qui 12/11, 18h** |
| C08-V2 | N-video | `C08-V2.mp4` | 13,0 s | 2,92 MB | Nuvem (pronto) → Montador agenda | D4 a D6 · alvo **dom 15/11 (feriado), 19h** |
| C08-M1 | M-gravacao | `C08-M1.mp4` (o Montador gera) | 10 a 12 s | até 4 MB | Montador grava e edita com o `kit-C08-M1/` (pronto) | alvo **sex 20/11 (feriado), 19h**, se pronta |
| C08-V3 | N-video | `C08-V3.mp4` | 11,0 s | 2,71 MB | Nuvem (pronto) → Montador agenda na rodada de qui 17/12 | data fixa **sex 25/12, 15h** |

Os 3 mp4 já estão prontos e conferidos com ffprobe: 1080x1920, 30 fps, H.264 High yuv420p (BT.709), áudio AAC estéreo 44,1 kHz, de 6 a 15 s, menos de 4 MB cada. Zona segura sem nenhum aviso. Prévia: `previa-videos.png`.

**Arquivos desta pasta**

| Arquivo | Para quê |
|---|---|
| `C08-V1.mp4`, `C08-V2.mp4`, `C08-V3.mp4` | Os vídeos, já com o nosso som |
| `C08-V1-capa.jpg`, `C08-V2-capa.jpg`, `C08-V3-capa.jpg` | Capa (1080x1920, até 200 KB) para "Editar capa → Carregar" |
| `C08-V1-legenda.txt`, `C08-V2-legenda.txt`, `C08-V3-legenda.txt` | Legenda + 5 hashtags, numa linha, pronta para colar |
| `kit-C08-M1/` | `gancho.png`, `final.png`, `assinatura.wav`, `capa.jpg`, `legenda.txt` para a M1 |
| `previa-videos.png` | 6 quadros de cada vídeo (vermelho = interface do TikTok) |
| `render_videos.py` | Refaz tudo: `python3 render_videos.py` |

A coordenação copia cada peça para `videos/prontos/<código>/`, se for o caso.

---

## 2. Regras que valem para as 4 peças

**Quando postar (regra D1, seção 4.1 do plano)**
- **D0** = dia em que o efeito fica "Active". Nenhum post do C08 antes disso.
- **D1** = dia seguinte. A V1 sai no horário nobre do D1.
- Se o C01 e o C08 forem aprovados no mesmo dia: o C01-V1 sai no D1 e o C08-V1 no dia seguinte.
- **Se o C08 for aprovado sozinho** (C01 atrasado ou reprovado): a C08-V1 vira o 1º post da conta e leva o comentário fixado longo (seção 3).
- Horário nobre: 18h de terça a quinta, 19h de sexta a segunda. A C08-V1 da qui 12/11 sai às **18h** (decisão do gerente em 06/11: vale a regra geral, também na tabela do plano).
- No máximo 2 posts por dia na conta, com 3 h ou mais entre eles. Nunca 2 peças do C08 no mesmo dia.
- Sem post de efeito na sex 27/11 (Black Friday) e na qui 03/12.
- Aprovação mais cedo ou mais tarde: vale a seção 4.5 do plano. Ex.: aprovado no sáb 07/11 → V1 na seg 09/11, 19h; a V2 fica no dom 15/11.

**Configurações em toda postagem (TikTok Studio, no navegador)**
- Quem pode ver: **Todos**.
- Comentários: **ligados**. Dueto: **ligado**. Costura: **ligada**.
- Conteúdo gerado por IA (rótulo de IA): **desligado**. Nas N, é animação feita por código, sem pessoa e sem cena realista. Na M1, é uma pessoa filmada de verdade, sem IA.
- Divulgar conteúdo comercial / conteúdo de marca: **desligado**.
- Som: **o do próprio arquivo**. Ele já está dentro do mp4 (som nosso, sem música de terceiros).
- Capa: **Editar capa → Carregar →** a capa da peça. Se não existir "Carregar", escolher o quadro de **0,5 s**. Ele foi feito para funcionar sozinho como capa.
- Colar a legenda inteira do `.txt`. Conferir: nome do filtro escrito igual e no máximo 5 hashtags.
- Agendar (se o botão existir) para a data e a hora. Sem o botão, postar na hora com o PC ligado (janela das 15h às 21h).

**Depois de postar**
- Publicar o comentário fixado da peça (seção 3) e fixar, se a web deixar. Até 150 caracteres. Todos os daqui têm menos de 130.
- "No meu perfil" só entra no comentário **depois** que o Montador vir a aba de efeitos do perfil numa janela anônima (seção 2.2 do plano). Até lá, só "Procura na lupa 🔎".
- Responder sempre que o PC estiver ligado. Sem link. Quando perguntarem o nome, repetir: **Eu no grupo da família**.
- "Onde compra?" → **Te chamo no direct 😉**
- Nunca escrever "o meu saiu…", "testei", desafio, prêmio, "concorra" ou "ganhe".

**Som em alta (Biblioteca de Música Comercial)**
- Só se o teste do passo 0 mostrar a Biblioteca **Comercial** no upload pela web. A biblioteca geral, não.
- Nunca na V1. Só na peça marcada "teste de som: sim" (aqui, só a V2), e só se ela sair **no D7 do C08 ou depois**.
- Faixa em volume baixo, **por baixo** do nosso som. Se o site não deixar manter o som do arquivo junto, não troca.

---

## 3. As peças

### C08-V1 · N-video · "O filtro que te expõe" · 10 s

- **Objetivo:** estreia. Mostrar em 3 s o que o filtro faz e puxar o compartilhamento para o grupo da família.
- **Quem faz:** nuvem (pronto e conferido). Montador agenda no D0, posta, fixa o comentário e responde.
- **Quando:** D1 do C08, horário nobre. Alvo **qui 12/11, 18h** (ver a nota do horário na seção 2). Prazo da peça: sáb 07/11, 12h → **pronta desde 06/11**.
- **Arquivo:** `C08-V1.mp4` (10,0 s · 2.799.320 bytes)

**O que aparece**

| Tempo | Na tela | Som |
|---|---|---|
| 0,0–1,85 | Gancho já no 1º quadro: "O filtro que te **expõe** no grupo". Carta 2 MANDO ÁUDIO DE 4 MINUTOS balançando. Embaixo, a carinha 🤔 no lugar da cabeça | trilha 104 bpm; assinatura (plim duplo + pop) |
| 1,85–2,6 | Título NO GRUPO DA FAMÍLIA, EU… e o dedo 👆 tocando | vush, pop, toque |
| 2,6–6,6 | Roleta das 28 cartas para na 7 SOU ADM E NINGUÉM PEDIU. Luz, raios, confete, tremida. A carinha vira 😌 | tiques, plim |
| 6,7–8,0 | "Alguém tem que manter a **ordem** 😌" | pop |
| 8,0–10,0 | CF: o fundo sobe e cobre a cena. "Qual é o seu **papel** no grupo?" + símbolo do perfil (com a mira) + "Procura na lupa 🔎" + **Eu no grupo da família** em amarelo, numa linha | vush; assinatura |

**Legenda pronta para colar** (igual ao `C08-V1-legenda.txt`):
```
Qual é o seu papel no grupo da família? Manda no grupo e vê quem concorda 😂 Filtro: Eu no grupo da família 🔎 #eunogrupodafamilia #grupodafamilia #filtro #filtrotiktok #familia
```
- **Hashtags:** `#eunogrupodafamilia #grupodafamilia #filtro #filtrotiktok #familia`
- **Capa:** `C08-V1-capa.jpg` → "QUAL É O SEU **PAPEL** NO GRUPO?" com a carta 7 e a carinha 😌. Sem "Carregar": quadro de **0,5 s** (gancho + carta 2 + 🤔).
- **Som:** assinatura do C08 + trilha 104 bpm, já no arquivo. Teste de som: **não**.
- **Postagem:** Todos · comentários, dueto e costura ligados · rótulo de IA **desligado** · conteúdo comercial **desligado**.
- **Comentário fixado:**
  - Se for o **1º post da conta** (C08 aprovado antes do C01):
    `Filtro: Eu no grupo da família 🔎 Procura na lupa. A conta agora faz filtros de torcida, carro e zoeira 😄 Qual é o seu papel?` (124 caracteres)
  - Se o C01-V1 já saiu:
    `Nome do filtro: Eu no grupo da família 🔎 Procura na lupa. Qual é o seu papel no grupo?` (86)

### C08-V2 · N-video · "A família inteira" · 13 s

- **Objetivo:** identificação. Cada um lembra do parente que é assim e manda o vídeo para ele.
- **Quem faz:** nuvem (pronto; o prazo era 12/11). Montador agenda ou posta.
- **Quando:** D4 a D6 do C08. Alvo **dom 15/11 (feriado), 19h**.
- **Arquivo:** `C08-V2.mp4` (13,0 s · 3.066.368 bytes)

**O que aparece**

| Tempo | Na tela | Som |
|---|---|---|
| 0,0–2,0 | Gancho já no 1º quadro: "Cada um da família **tem o seu**". Rótulo **MÃE** + carta 1 MANDO BOM DIA COM FLOR | trilha 110 bpm; assinatura |
| 2,0–3,5 | Rótulo **TIO** + carta 21 FAÇO A PIADA DO PAVÊ (as cartas deslizam) | vush, pop |
| 3,5–5,0 | Rótulo **VÓ** + carta 5 REPASSO TODA CORRENTE | vush, pop |
| 5,0–6,5 | Rótulo **PRIMO** + carta 11 SÓ COMENTO KKKKKKK | vush, pop |
| 6,5–7,3 | "E **VOCÊ**?" + título + carinha 🤔 + dedo 👆 | vush, pop, toque |
| 7,3–9,6 | Roleta para na 4 VISUALIZO E NÃO RESPONDO. A carinha vira 🫣. O resultado fica parado até 10,75 s (~1,2 s) | tiques, plim |
| 9,7–13,0 | "Manda no grupo da família 👀" no topo. Às 10,75 s o fundo cobre a cena e entra o CF (símbolo, "Procura na lupa 🔎", nome em amarelo) | vush; assinatura |

Os parentes são **só rótulos em texto**, sem rosto e sem emoji de pessoa. A carinha só aparece no "E VOCÊ?".

**Legenda pronta para colar** (igual ao `C08-V2-legenda.txt`):
```
Mãe, tio, vó, primo… cada um tem seu papel no grupo 😂 E você? Filtro: Eu no grupo da família 🔎 procura na lupa #eunogrupodafamilia #grupodafamilia #familiabrasileira #filtrotiktok #humor
```
- **Hashtags:** `#eunogrupodafamilia #grupodafamilia #familiabrasileira #filtrotiktok #humor`
- **Capa:** `C08-V2-capa.jpg` → "CADA UM DA FAMÍLIA **TEM O SEU** 😂" com a carta 21 e o rótulo TIO. Sem "Carregar": quadro de **0,5 s** (gancho + MÃE + carta 1).
- **Som:** assinatura do C08 + trilha 110 bpm, já no arquivo. **Teste de som: sim**, mas só se sair no D7 ou depois e se existir a Biblioteca Comercial (seção 2). No alvo de 15/11 (D5), vai só com o nosso som.
- **Postagem:** Todos · comentários, dueto e costura ligados · rótulo de IA **desligado** · conteúdo comercial **desligado**.
- **Comentário fixado:** `Pra achar: Eu no grupo da família 🔎 Procura na lupa. Qual parente seu é assim?` (78)

### C08-M1 · M-gravacao · "Funciona assim" · 10 a 12 s

- **Objetivo:** provar que o filtro existe e funciona num rosto.
- **Quem faz:** o **Montador** grava no PC e finaliza no Clipchamp. A nuvem já mandou o kit: `kit-C08-M1/` (o prazo era 17/11).
- **Quando:** alvo **sex 20/11 (feriado, família reunida), 19h**. Se ficar pronta antes, pode subir de data e virar a 2ª peça do C08 (seção 4.5 do plano), sem tirar a V2 do dia 15/11 e sem 2 peças do C08 no mesmo dia. Se não estiver pronta na véspera, o horário **fica vago** (não troca por outra peça).
- **Arquivo final:** `C08-M1.mp4`, feito pelo Montador.

**1. Fonte de rosto (o Montador baixa no PC; daqui da nuvem esses sites não abrem)**
- 1º **Pexels**. 2º **Mixkit**, só com "Free License".
- **Nunca** os vídeos de amostra do Effect House (só servem para o demo do envio).
- O clipe precisa ter: 1 pessoa adulta, de frente, parada, olhando para a câmera, camiseta lisa, fundo neutro. De preferência em pé (vertical).
- Rejeitar se tiver: camisa ou escudo de time, logo, marca em roupa ou objeto, carro reconhecível, criança, famoso, bebida, símbolo religioso, direção, ou clipe marcado como IA.
- Sugestão de busca (em inglês costuma achar mais): `man looking at camera plain background`, `woman looking at camera neutral background`, filtro "Vertical".
- **Planilha de licença** (no PC, ao lado do `relatorio-montagem.md`): link do clipe, autor, data e print da página com a licença.
- **Antes de postar:** conferir no print das regras do desafio se pedem autorização por escrito de quem aparece no vídeo (seção 5.4 do plano). Se pedirem, **não postar a M1** e avisar a nuvem.

**2. O que gravar no preview do Effect House**
0. **Antes de tudo: o projeto do C08 ainda é o C08?** Uma ordem de 06/11 mandou montar o C01 reaproveitando o projeto do C08. Abrir `projetos\C08-grupo-familia-1rosto` (nome do guia, parte 7.4; conferir no `relatorio-montagem.md`) e ver se o título é NO GRUPO DA FAMÍLIA, EU… e as cartas são as do grupo da família.
   - Se virou o Torcedômetro (salvo por cima): procurar uma cópia em `projetos\backup\` ou a versão `C08-grupo-familia-2rostos` (com 1 rosto no clipe, deve sortear igual; a confirmar no preview). Se não houver nenhuma, **não montar de novo só para a M1**: avisar a nuvem; a M1 sai do calendário e o horário fica vago.
1. Abrir o projeto do C08 salvo em `projetos\` (o mesmo que foi enviado). Não mudar nada nele. Ao fechar, se perguntar se quer salvar, escolher **não salvar** (a confirmar se o clipe no preview altera o projeto).
2. No Preview, escolher um aparelho 9:16 (ex.: 1080x1920).
3. "+ Add media" → o clipe baixado.
4. Voltar o efeito para o começo, com o título NO GRUPO DA FAMÍLIA, EU… sobre a cabeça.
5. Gravar com o botão de gravar do próprio Preview ("Screen record"; nome e lugar a confirmar). Se não houver, usar a Ferramenta de Captura do Windows 11 (Win + Shift + R, a confirmar), **só a área do Preview**: sem menus, sem mouse e sem a interface do Effect House.
6. Roteiro da gravação (uns 10 s):
   - 0 a 3 s: título parado sobre a cabeça. Não clicar.
   - perto de 3 s: **um clique** no Preview. As cartas giram e param.
   - do resultado até uns 9,5 s: resultado parado.
7. **Regravar se sair a carta 6** SOU A FONTE DAS FOFOCAS. As melhores para rosto de banco: **26** AVISO QUE VAI CHOVER, **20** PASSO RECEITA QUE NINGUÉM FAZ, **25** ENCHO O GRUPO DE FOTO DO PET. Pode gravar algumas vezes e ficar com a melhor.
8. Salvar a gravação bruta em `Efeitos\prontos\C08-M1\C08-M1-bruto.mp4` (pasta `Efeitos` = a mesma do `relatorio-montagem.md`; criar se não existir). Pode ser feito já na montagem, antes da aprovação. Só vai ao ar no dia da peça.

**3. Edição no Clipchamp (vem no Windows 11; a confirmar no PC)**
1. Projeto novo em **9:16**.
2. Importar: a gravação bruta, `gancho.png`, `final.png` e `assinatura.wav` (pasta `kit-C08-M1`).
3. Linha do tempo:

| Tempo | Vídeo | Por cima | Som |
|---|---|---|---|
| 0 a 3 s | gravação (título sobre a cabeça) | `gancho.png` ("Funciona assim 👇 / Qual é o seu papel?", no topo) | `assinatura.wav` do começo ao fim |
| 3 s até ~9,5 s | gravação (clique, cartas girando, resultado parado) | nada | (continua) |
| 9,5 a 12 s | `final.png` (CF com "Qual é o seu?", símbolo, "Procura na lupa 🔎" e o nome) | nada | (continua) |

4. **Som da gravação: desligado** (mudo). Só o `assinatura.wav`. Ele tem a trilha nossa de 104 bpm, a assinatura no começo, um toque leve aos 3 s (a hora do clique) e a assinatura de novo aos 9,5 s (entrada do final).
5. Se o `gancho.png` cobrir o balão sobre a cabeça, arrastar o gancho um pouco para cima ou diminuir o clipe. O gancho fica sempre por inteiro na tela.
6. Duração total: de 10 a 12 s.
7. Exportar em **1080p**, MP4. Salvar como `Efeitos\prontos\C08-M1\C08-M1.mp4`.
8. **Conferir antes de postar** (botão direito → Propriedades → Detalhes): de 6 a 15 s e **até 4 MB**. Se passar de 4 MB, exportar de novo em **720p**.
9. Se o Clipchamp não existir ou travar, a peça **sai do calendário** e o horário fica vago. Nada de editor com marca d'água.

**Textos:** nunca "eu", "testei", "minha mãe" ou nome de alguém. Sempre "Funciona assim 👇". A pessoa do clipe nunca aparece perto de produto, preço ou loja.

**Legenda pronta para colar** (igual ao `kit-C08-M1/legenda.txt`):
```
Funciona assim: toca na tela e o filtro mostra seu papel no grupo da família. Filtro: Eu no grupo da família 🔎 #eunogrupodafamilia #grupodafamilia #filtro #filtrotiktok #feriado
```
- **Hashtags:** `#eunogrupodafamilia #grupodafamilia #filtro #filtrotiktok #feriado`
- **Capa:** `kit-C08-M1/capa.jpg` → "FUNCIONA ASSIM 👇" com o título do efeito, a carinha 🤔 e o dedo. Sem "Carregar": um quadro perto de **1 s** (título sobre a cabeça + gancho).
- **Som:** só o `assinatura.wav` (nosso). Teste de som: **não**.
- **Postagem:** Todos · comentários, dueto e costura ligados · rótulo de IA **desligado** (pessoa filmada de verdade, sem IA) · conteúdo comercial **desligado**.
- **Comentário fixado:** `Esse é o filtro Eu no grupo da família 🔎 Procura na lupa. Qual saiu pra você?` (77)
- **Nunca fixar no perfil** um vídeo com pessoa de banco perto de produto (aqui não tem produto; só não misturar com a loja).

### C08-V3 · N-video · "Natal no grupo" · 11 s

- **Objetivo:** 2ª onda no dia em que o grupo da família mais lota.
- **Quem faz:** nuvem (pronto; o prazo era 21/12). Montador agenda.
- **Quando agendar:** o Agendar vai só até 10 dias à frente (a confirmar). Então **não dá antes de ter 15/12 às 15h**. Na rotina do plano (segunda e quinta), é a rodada de **qui 17/12**; a de seg 21/12 também serve. Não deixar para depois de qua 23/12.
- **Quando sai:** data fixa **sex 25/12, 15h**. Sem o botão Agendar, a coordenação combina com o Vini o PC ligado nesse dia (a confirmar).
- **Arquivo:** `C08-V3.mp4` (11,0 s · 2.837.435 bytes)

**O que aparece**

| Tempo | Na tela | Som |
|---|---|---|
| 0,0–2,0 | Gancho já no 1º quadro: "Hoje o grupo da família vai **lotar** 🎄". Carta 13 SÓ ESCREVO EM CAPS LOCK + carinha 🥳. Chuva de 💬 e 🎄. Fundo com bolinhas caindo, como neve | trilha 100 bpm + sininho baixinho; assinatura |
| 2,0–3,5 | "FELIZ NATAL" + "× 1 … × 200 💬" contando, com balões 💬 pipocando (o grupo enchendo) | 8 plins seguidos |
| 3,5–4,2 | "E você, **quem é hoje**?" + título + carinha 🤔 + dedo 👆 | pop, toque |
| 4,2–7,4 | Roleta para na 9 SÓ APAREÇO PRA DAR PARABÉNS. A carinha vira 😅. O resultado fica parado até 8,55 s (~1,15 s) | tiques, plim |
| 7,5–11,0 | "Cada um no seu celular 📱" no topo. Às 8,55 s o fundo cobre a cena e entra o CF (símbolo, "Procura na lupa 🔎", nome em amarelo) | vush; assinatura |

**Legenda pronta para colar** (igual ao `C08-V3-legenda.txt`):
```
Natal: hoje o grupo da família vai lotar 🎄 Qual é o seu papel nele? Filtro: Eu no grupo da família 🔎 #eunogrupodafamilia #grupodafamilia #natal #filtrotiktok #familia
```
- **Hashtags:** `#eunogrupodafamilia #grupodafamilia #natal #filtrotiktok #familia`
- **Capa:** `C08-V3-capa.jpg` → "NATAL NO GRUPO DA FAMÍLIA 🎄" com a carta 9 e a carinha 😅. Sem "Carregar": quadro de **0,5 s** (gancho + carta 13 + 🥳).
- **Som:** assinatura do C08 + sininho + trilha 100 bpm, já no arquivo. Teste de som: **não**.
- **Postagem:** Todos · comentários, dueto e costura ligados · rótulo de IA **desligado** · conteúdo comercial **desligado**.
- **Comentário fixado:** `Feliz Natal! 🎄 O filtro é Eu no grupo da família 🔎 Procura na lupa. Qual é o seu papel hoje?` (92)

---

## 4. Conferência feita (QA da nuvem)

- Nome igual ao `textos.md` (**Eu no grupo da família**) na tela, na legenda e no comentário.
- Gancho no 1º quadro (t = 0) nas 3 peças N. O quadro de 0,5 s serve de capa.
- CF nos 2 a 2,5 s finais, com o nome em amarelo numa linha só e o símbolo do perfil (com a mira).
- Sem pessoa, sem rosto, sem emoji de pessoa nos parentes. Só carinhas emoji no lugar da cabeça.
- Nada que lembre app de mensagem: sem verde, sem tela de conversa, sem tiques de "lida", sem nome de app. Os 💬 são o balão genérico do emoji.
- Nada da lista "Nunca" do plano: sem loja, link, QR code, marca, time, carro reconhecível, "Pix", bebida, direção, religião, desafio ou prêmio.
- Duração de 6 a 15 s e até 4 MB (ffprobe). Legendas com 5 hashtags. Comentários com menos de 130 caracteres.
- Zona segura da biblioteca (x de 60 a 940, y de 220 a 1500): nenhum aviso. A prévia foi aberta e conferida.
- Som: picos em −0,8 dBFS ou menos e volume de −11,8 a −13,6 LUFS nos mp4; −14,9 LUFS no `assinatura.wav`.
- Mesmo resultado em duas rodadas: os 15 arquivos saem iguais byte a byte (conferido pela QA nas 3 peças, nas capas, nas legendas e no kit).
- Resultado da roleta parado antes do CF: V1 ~1,4 s, V2 ~1,2 s, V3 ~1,15 s (correção da QA).

## 5. Se precisar refazer

- **Nome publicado diferente** (ex.: sem acento), no D0: `python3 render_videos.py --nome "Nome publicado"`. Refaz tela, legendas e kit (a legenda da M1 também, desde a correção da QA). A capa não tem o nome, então não muda. Depois, trocar o nome nos comentários desta página.
- **Aviso de luz piscante** num post: a roleta começa com umas 11 trocas de carta por segundo (a regra de 3 por segundo do plano vale para os trechos de "pausa"). Para desacelerar, aumentar `intervalo_ini` na função `roleta()` do script (ex.: 0,33 = 3 por segundo) e rodar de novo.
- **Outra foto de perfil** (não a opção 1): trocar o degradê da função `avatar()` para bater com a foto escolhida.
- **"No meu perfil"** só entra nos textos depois da conferência da aba de efeitos (seção 2.2 do plano).
- Tempo para refazer tudo: uns 3 minutos nesta máquina.
