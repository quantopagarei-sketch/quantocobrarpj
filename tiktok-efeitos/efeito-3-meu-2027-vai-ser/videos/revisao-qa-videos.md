# C05 Meu 2027 vai ser: revisão de QA dos vídeos

Feita em 06/11/2026 pela nuvem (revisor de QA dos vídeos do C05).
**Vini, você não precisa fazer nada com este arquivo.** Ele é para a coordenação e o Montador.

**Resultado: aprovado, nota 9.** Os 3 vídeos, as capas, as legendas e o kit da M1 podem ser liberados como estão. Nenhum MP4 precisou ser refeito.
Corrigi 1 falha do script: ele não fazia a versão com **CARRO no lugar de FUTEBOL**, que o guia de montagem permite. Também ajustei 6 pontos do `roteiros-videos.md`.
**Pedido para a coordenação:** no pedido do D0 do C05 no `PRONTO-PARA-MONTAR.md`, trocar "3 ou 4 bolhas" por "quais bolhas" (ver "Riscos", item 1).

---

## 1. O que eu conferi

### 1.1 Parte técnica (ffprobe e ffmpeg)

| Vídeo | Duração | Tamanho | Imagem | Som | Volume |
|---|---|---|---|---|---|
| C05-V1.mp4 | 12,0 s (360 quadros) | 2.849.821 bytes (2,72 MB) | 1080x1920, 30 fps, H.264 High, yuv420p, BT.709 | AAC estéreo 44,1 kHz, ~138 kbps | −17,2 LUFS · pico real −1,0 dBFS · média −19,1 dB |
| C05-V2.mp4 | 11,0 s (330 quadros) | 2.626.721 bytes (2,51 MB) | igual | AAC estéreo, ~135 kbps | −16,2 LUFS · pico real −1,5 dBFS · média −19,1 dB |
| C05-V3.mp4 | 12,0 s (360 quadros) | 2.842.149 bytes (2,71 MB) | igual | AAC estéreo, ~136 kbps | −16,6 LUFS · pico real −1,8 dBFS · média −19,0 dB |

- Os 3 ficam entre 6 e 15 s e abaixo de 4 MB. **Pasta inteira: ~11,2 MB**, já com esta revisão, abaixo do limite de 12 MB.
- Som audível do começo ao fim: nenhum silêncio de mais de 0,3 s (abaixo de −45 dB). Pico real abaixo de −1 dBFS nos 3. Os números batem com o relato do produtor.
- MP4 com o índice no começo (sobe rápido no navegador) e quadro-chave a cada 2 s.
- `kit-C05-M1/assinatura.wav`: 12,0 s, mono, 44,1 kHz, 16 bits. −20,5 LUFS e pico real −1,4 dBFS (ver "Riscos", item 5).
- Ganchos do kit: 1080x1920, fundo transparente. O de cima ocupa y 228–446; o de baixo, y 1283–1501 (só 1 px de sombra encosta na faixa de baixo; o texto fica acima). `final.png` e as 5 capas: 1080x1920.

### 1.2 Quadros abertos e revisados (um por um)

Extraí **10 tempos de cada vídeo** (sempre com 0,0 s, 0,5 s, o 1º segundo e o último quadro), com as faixas da interface do TikTok marcadas, e abri todas as pranchas. Também abri as 5 capas, o kit da M1, a `previa-videos.png`, um recorte das respostas em tamanho real e as pranchas das variantes (4 bolhas com toque; 3 bolhas com CARRO).
Pranchas no scratchpad da nuvem (pasta `qa-C05/`): `v1-a.png`, `v1-b.png`, `v2-a.png`, `v2-b.png`, `v3-a.png`, `v3-b.png`, `capas.png`, `kit.png`, `zoom-v1.png`, `carro-v1.png`, `carro-v2.png`, `carro-v3.png`, `carro-capas.png`, `rapido4/`.

| Ponto | V1 | V2 | V3 |
|---|---|---|---|
| Gancho no 1º quadro | ✅ "**Estoura a bolha** e vê seu 2027" + título + 3 bolhas + 🤔 | ✅ "Ceia hoje: cada um **vê seu 2027** 🎄" + título + bolhas + 🎄 + enfeites | ✅ "**Último dia:** vê seu 2027 agora" + título + bolhas + 🕛 |
| Gancho com até 7 palavras | 6 | 6 | 5 |
| Quadro de 0,5 s serve de capa | ✅ | ✅ | ✅ |
| Resultado legível | 3 respostas em faixas grandes; a última (TÍTULO VEM (CONFIA)) fica ~3,4 s na tela | Rodada 1 e Rodada 2 legíveis; a 3ª resposta de cada rodada fica ~1,2 a 1,3 s na tela (ver "Riscos", item 3) | 3 respostas; a última (GOL NOS ACRÉSCIMOS) fica ~3 s |
| Cartão final (CF) | 9,5–12 s: símbolo + "Procura na lupa 🔎" + **Meu 2027 vai ser** (amarelo, 1 linha) + "Qual saiu pra você?" | 8–11 s, com "Cada um no seu celular 📱" | 9,5–12 s, com "Qual saiu pra você?" |
| Zona segura (topo 220, base 420, direita 140) | ✅ nada importante fora; nenhum aviso da biblioteca | ✅ (só as bolas de Natal, que são enfeite, entram no topo e na direita) | ✅ |

- **Nome do efeito:** "Meu 2027 vai ser", igual ao `textos.md` (sem reticências), no CF dos 3 vídeos, nas 5 capas, nas 5 legendas e em todos os comentários do roteiro. O título na tela ("MEU 2027 VAI SER…") é a arte do próprio efeito.
- **Acentos conferidos na tela:** vê, Último, você, biquinho, amanhã, ATÉ, 13º, CLÁSSICO, CALÇA, ACRÉSCIMOS, TÍTULO. Nenhum erro. O "13º" vem do PNG do efeito e lê como ordinal.
- **Resultados iguais ao plano:** V1 amor_02, grana_02, futebol_01. V2 rodada 1 amor_07, grana_05, futebol_02; rodada 2 amor_05, grana_08, futebol_04. V3 amor_08, grana_03, futebol_06. Nenhuma das 2 respostas "a evitar" (grana_07, amor_03) aparece.
- **Luz piscante:** nada de flash de tela cheia. O clarão é só na faixa da resposta, por 0,35 s.
- **Capas:** texto grande dentro do miolo 3:4 (y 240 a 1680). O rodapé "Filtro: Meu 2027 vai ser 🔎" fica em y ~1545, dentro do 3:4. Textos iguais ao plano: "COMO VAI SER SEU 2027? ✨", "NA CEIA: CADA UM VÊ SEU 2027 🎄", "ÚLTIMO DIA: VÊ SEU 2027 ✨", "FAZ BIQUINHO E VÊ SEU 2027 😗" e "TOCA E VÊ SEU 2027 ✨".
- **Kit da M1:** "Funciona assim 👇 / faz biquinho 😗" e "… / toca na tela 👆", em cima e na altura do peito. `final.png` igual ao CF, com "Faz hoje e na virada ✨".

### 1.3 Regras fixas

Nenhum nome, escudo, cor combinada ou apelido de time ("GANHA O CLÁSSICO" e "TÍTULO VEM" servem para qualquer torcida). Nenhuma marca, celebridade, "Pix", bebida, direção perigosa ou religião. Nada de loja, link, preço, cupom ou prêmio.
- Nenhuma pessoa, rosto ou silhueta: no lugar da cabeça, só emoji (🤔, 😗, 🎄, 🕛).
- O símbolo do CF é o carrinho turquesa na mira de câmera (`videos/perfil/simbolo_transparente.png`), o mesmo dos outros efeitos. Carro genérico, sem marca nem modelo. Não é chamada para a loja.
- Na tela, sempre "você". Nenhuma palavra da lista "Nunca" do plano (2.2) na tela, nas legendas ou nos comentários.
- Nenhum arquivo cita nome ou versão de modelo de IA.

### 1.4 Legendas, hashtags e comentários

| Peça | Total com hashtags | Hashtags |
|---|---|---|
| C05-V1 | 167 caracteres | 5 · #meu2027vaiser #previsao2027 #2027 #filtro #filtrotiktok |
| C05-V2 | 164 | 5 · #meu2027vaiser #ceiadenatal #2027 #filtrotiktok #natal |
| C05-V3 | 157 | 5 · #meu2027vaiser #reveillon #anonovo #2027 #filtrotiktok |
| C05-M1 (biquinho e toque) | 147 cada | 5 · #meu2027vaiser #2027 #anonovo #filtro #filtrotiktok |

- Legendas iguais, letra por letra, às do `PLANO-DE-VIDEOS.md` (seção 3, C05). Todas muito abaixo do limite de legenda do TikTok.
- Contei os comentários fixados: 71, 88, 99, 116, 81, 95 e 112 caracteres, como está no roteiro. Todos abaixo de 150.

### 1.5 Roteiro, datas e instruções do Montador

- **Datas iguais à tabela 4.4 do plano:** V1 qua 09/12 18h (D1, com aprovação na ter 08/12) · V2 qui 24/12 13h · M1 dom 27/12 19h · V3 qui 31/12 14h (3 h depois do C07-V3 das 11h). Dias da semana conferidos no calendário de dez/2026.
- **Agendamento:** V2 na seg 14/12 (10 dias antes), M1 na qui 17/12 ou seg 21/12, V3 na seg 21/12 ou ter 22/12. Bate com "até 10 dias" (4.6) e com os prazos "Montador agenda até 14/12 / 22/12" do plano.
- Regras do D1, ordem C05 → C07, aprovação depois de 12/12 e depois de 24/12: iguais à 4.1 e à 4.5.
- Configurações: Todos; comentários, dueto e costura ligados; rótulo de IA desligado; conteúdo comercial desligado; som do arquivo. Coerente com o plano (2.3 e 2.5).
- Teste de som só na V2, só depois do D7 e só com a Biblioteca de Música Comercial. Coerente com 2.4.
- **Sem celular:** tudo é feito no PC (Effect House, Clipchamp, TikTok Studio no navegador). O que depende de botão da web está marcado "(a confirmar)" (Agendar, Carregar capa, Fixar comentário, Biblioteca Comercial).

### 1.6 O script roda de novo e dá o mesmo resultado

- Rodei o `render_videos.py` completo **3 vezes** numa pasta do scratchpad (`--pasta`): antes da minha mudança, durante e depois. Os 20 arquivos (3 MP4, 3 capas, 3 legendas, prévia e os 10 do kit) saíram **iguais byte a byte** aos entregues nas 3 rodadas. Nenhum aviso de zona segura.
- Testei também `--bolhas 4 --hint toque` (prancha rápida) e `--bolhas carro` (MP4 completos: 2,72 / 2,51 / 2,71 MB, sem aviso de zona segura).

---

## 2. O que eu corrigi

1. **`render_videos.py`: nova opção `--bolhas carro`.** O guia de montagem (Parte 17.1) e o `lancamento.md` (pendência 4) preveem 3 saídas: 3 bolhas, 4 bolhas, ou 3 bolhas com **CARRO no lugar de FUTEBOL**. O script só fazia as 2 primeiras. Se o efeito saísse com AMOR, GRANA e CARRO, os vídeos mostrariam uma bolha FUTEBOL que não existe no filtro. Agora `--bolhas carro` faz AMOR, GRANA e CARRO (CARRO à direita, como no guia), em vídeos, capas e kit, com as mesmas respostas de CARRO já usadas na opção de 4 bolhas. A versão padrão (3 bolhas) não mudou nada: conferido byte a byte.
2. **`roteiros-videos.md`:**
   - O pedido do D0 agora diz "**quais bolhas**" (padrão, 4 com CARRO, ou CARRO no lugar de FUTEBOL), e não só "3 ou 4". Mesma troca na lista "A confirmar".
   - Novo comando `--bolhas carro` em "Para a nuvem: como refazer".
   - M1, passo 1: o projeto a abrir é **o que foi enviado**. Pelo guia, ele pode ser `C05-meu-2027`, `C05-meu-2027-script` ou `C05-meu-2027-4bolhas`. Antes só citava o primeiro.
   - M1, passo 2: o guia manda **apagar ou desligar** os Generative Effects. Antes dizia só "desligado".
   - M1: faltava o comentário com "ou no meu perfil" (as outras peças tinham). Acrescentei as 2 versões, com 98 caracteres cada.
   - Regra 3: diz como pôr "ou no meu perfil" na legenda depois da conferência da aba.
   - Faixa de volume corrigida para "entre −16,2 e −17,2 LUFS" (a V1 tem −17,2).

---

## 3. Riscos (o que continua aberto)

1. **Quais bolhas foram publicadas (a confirmar no D0).** O pedido ao Montador no `PRONTO-PARA-MONTAR.md` é da coordenação. Ele precisa perguntar "quais bolhas", e não só "3 ou 4". Com a resposta, a nuvem roda `--bolhas 4` ou `--bolhas carro` no mesmo dia.
2. **Respostas de CARRO escolhidas pela nuvem** (não estão no plano): V1 CARRO NOVO (DO VIZINHO); V2 VAGA NA PORTA e TIRA A CNH DE PRIMEIRA; V3 ZERO BURACO NO CAMINHO. Valem para `--bolhas 4` e `--bolhas carro`. Estão dentro das regras (sem marca, sem modelo, sem direção perigosa), mas a coordenação precisa aprovar.
3. **V2: a 3ª resposta de cada rodada fica pouco tempo na tela** (~1,3 s na rodada 1, até as respostas saírem; ~1,2 s na rodada 2, até o CF subir). São 3 palavras, dá para ler, e o tempo segue o plano (rodadas de 2 a 5 s e de 5 a 8 s). Se o D3 mostrar retenção baixa na V2, dá para adiantar a rodada 2 em ~0,3 s no script.
4. **V3: o confete passa por cima do título** "MEU 2027 VAI SER…" de ~4 a ~7,5 s, enquanto as bolhas estouram. O título continua legível. Não mexi.
5. **`assinatura.wav` (M1) é mais baixa que os vídeos N:** −20,5 LUFS, contra −16 a −17 nas N. A M1 vai sair um pouco mais baixa. O Montador **não deve subir o volume no Clipchamp** (o pico real já está em −1,4 dBFS; subir pode distorcer). Risco baixo.
6. **Cores das bolhas:** o template do efeito pinta as bolhas com cores sorteadas. Nos vídeos, elas são sempre rosa, amarela e azul. Quem abrir o filtro pode ver outras cores. É ilustração, não promete nada. Risco baixo.
7. **Versão toque da V1 não está na pasta** (a pasta passaria de 12 MB). Se o hint publicado for de toque, a nuvem roda `--so C05-V1 --hint toque` no D0 e substitui a `C05-V1.mp4`.
8. **Dependência da biblioteca:** o script usa funções internas de `videos/lib/render.py` (`_redimensionar`, `_pintar`, `_passa_baixa`, `_extrair_quadro`, `Video._registrar`). Se a biblioteca mudar, ele pode quebrar. Hoje roda e dá sempre o mesmo resultado.
9. **O C05 ainda não foi montado** (STATUS: "Não começado"). Se o efeito enviado mudar textos, cores ou bolhas, a M1 tem que ser gravada de novo e as N podem precisar das opções do script.
10. **(a confirmar)**, como o produtor já listou: nome, hint e bolhas publicados; data de aprovação; Agendar e "Editar capa → Carregar" na conta Pessoal pela web; "Fixar" comentário pela web; aba de efeitos no perfil; Biblioteca de Música Comercial no upload pela web; se o biquinho de um clipe dispara as bolhas no preview; botão de gravar do preview; Win+Shift+R; Clipchamp no PC.

---

## 4. Arquivos

- Revisados: `C05-V1.mp4`, `C05-V2.mp4`, `C05-V3.mp4`, as 3 capas e as 3 legendas, `kit-C05-M1/` (10 arquivos), `previa-videos.png`, `roteiros-videos.md` e `render_videos.py`.
- Alterados por mim: `render_videos.py` (opção `--bolhas carro`) e `roteiros-videos.md`. Criado: este arquivo.
- Não mexi em `PRONTO-PARA-MONTAR.md`, `STATUS.md`, na biblioteca nem em `assets/`.
