# C08 Eu no grupo da família: revisão de QA dos vídeos

Feita em 06/11/2026 pela nuvem (revisor de QA dos vídeos do C08).
**Vini, você não precisa fazer nada com este arquivo.** Ele é para a coordenação e o Montador.

**Resultado: aprovado, nota 9.** Os 3 vídeos, as capas, as legendas e o kit da M1 podem ser liberados.
Corrigi 1 defeito visual na V2 e na V3 (já re-renderizadas), 1 defeito no script (`--nome`) e 2 pontos do `roteiros-videos.md`.
Há **2 avisos para a coordenação**: o agendamento da V3 e o projeto do C08 no PC (ver "Riscos", itens 1 e 2).

---

## 1. O que eu conferi

### 1.1 Parte técnica (ffprobe e ffmpeg, depois da correção)

| Vídeo | Duração | Tamanho | Imagem | Som | Volume |
|---|---|---|---|---|---|
| C08-V1.mp4 | 10,0 s (300 quadros) | 2.799.320 bytes (2,67 MB) | 1080x1920, 30 fps, H.264 High, yuv420p, BT.709 | AAC estéreo 44,1 kHz | -13,4 LUFS · pico -0,8 dBFS · média -17,1 dB |
| C08-V2.mp4 | 13,0 s (390 quadros) | 3.066.368 bytes (2,92 MB) | igual | igual | -13,6 LUFS · pico -0,8 dBFS · média -17,2 dB |
| C08-V3.mp4 | 11,0 s (330 quadros) | 2.837.435 bytes (2,71 MB) | igual | igual | -11,8 LUFS · pico -0,9 dBFS · média -17,1 dB |

- Os 3 ficam entre 6 e 15 s e abaixo de 4 MB. **Pasta inteira: uns 11,4 milhões de bytes** (já com esta revisão), abaixo do limite de 12 MB.
- Som audível do começo ao fim: nenhum silêncio de mais de 0,3 s (abaixo de -45 dB). Pico abaixo de -0,5 dBFS em todos.
- MP4 com o índice no começo (sobe rápido no navegador).
- `kit-C08-M1/assinatura.wav`: 12,0 s, mono, 44,1 kHz, 16 bits, -14,9 LUFS, pico -1,5 dBFS.
- `gancho.png`: 1080x1920 transparente. O texto fica em x 155–921 e y 257–446 (dentro da zona). Só a sombra clara chega a x 957.
- `final.png` e as 4 capas: 1080x1920. Capas em JPG de 187 a 202 KB.

### 1.2 Quadros abertos e revisados (um por um)

Extraí **de 12 a 20 tempos de cada vídeo** (sempre com 0,0 s, 0,5 s, o 1º segundo e o último quadro), mais tiras da chegada do resultado e da entrada do cartão final, antes e depois da correção. Abri todas as pranchas.
Pranchas (no scratchpad da nuvem, pasta `qa-C08/`): `V1-a/b/c.png`, `V2-a/b/c.png`, `V3-a/b/c.png` (originais), `V2-novo.png` e `V3-novo.png` (corrigidos), `capas-kit.png`, `gancho-crop.png`, `foto-vs-cf.png` e `nomes-alternativos.png`.

| Ponto | V1 | V2 | V3 |
|---|---|---|---|
| Gancho no 1º quadro | ✅ "O filtro que te **expõe** no grupo" + carta 2 + 🤔 | ✅ "Cada um da família **tem o seu**" + MÃE + carta 1 | ✅ "Hoje o grupo da família vai **lotar** 🎄" + carta 13 + 🥳 |
| Palavras no gancho (máx. 7) | 6 | 6 | 7 |
| Quadro de 0,5 s serve de capa | ✅ | ✅ | ✅ |
| Resultado legível | 7 SOU ADM E NINGUÉM PEDIU, parado de 6,6 a ~8,05 s (~1,4 s, com a frase junto) | 4 VISUALIZO E NÃO RESPONDO, **era ~0,7 s; agora ~1,2 s** (9,6 a 10,8 s) | 9 SÓ APAREÇO PRA DAR PARABÉNS, **era ~0,6 s; agora ~1,15 s** (7,4 a 8,6 s) |
| Cartão final (CF) | 8,0–10,0 s: "Qual é o seu **papel** no grupo?" + símbolo + "Procura na lupa 🔎" + nome | 10,75–13,0 s, com "Manda no grupo da família 👀" | 8,55–11,0 s, com "Cada um no seu celular 📱" |
| Zona segura (topo 220, base 420, direita 140) | ✅ nenhum aviso | ✅ | ✅ |

- **Nome do efeito:** "Eu no grupo da família", igual ao `textos.md`, na tela (amarelo, 1 linha, 73 px), nas 4 legendas e nos 5 comentários do roteiro.
- **Acentos conferidos na tela:** expõe, FAMÍLIA, ÁUDIO, NINGUÉM, Alguém, MÃE, VÓ, PAVÊ, VOCÊ, NÃO, você, é, APAREÇO, PARABÉNS, família. Nenhum erro.
- **Transições:** a carta que entra deslizando (V2) e o quique do resultado passam da linha da direita por menos de 0,3 s. Aceitável (a checagem da biblioteca não acusa).
- **Luz piscante:** sem flash branco de tela cheia. O começo da roleta troca a carta ~9 a 11 vezes por segundo, por menos de 1 s (ver "Riscos", item 4).
- **Capas:** texto grande dentro do miolo 3:4 (y 240 a 1680). V1 "QUAL É O SEU **PAPEL** NO GRUPO?" + carta 7 + 😌; V2 "CADA UM DA FAMÍLIA **TEM O SEU** 😂" + carta 21 + TIO; V3 "NATAL NO GRUPO DA FAMÍLIA 🎄" + carta 9 + 😅; M1 "FUNCIONA ASSIM 👇" + título + 🤔 + 👆.
- **Símbolo do CF = foto de perfil recomendada** (`videos/perfil/foto_recomendada.png`, carrinho turquesa na mira). Conferido lado a lado: mesmo desenho e mesmo degradê.
- **Kit da M1:** `gancho.png` "Funciona assim 👇 / Qual é o seu **papel**?" no topo; `final.png` igual ao CF, com "Qual é o **seu**?".

### 1.3 Regras fixas

Nenhuma pessoa, rosto ou silhueta: no lugar da cabeça, só carinhas emoji (🤔, 😌, 🫣, 🥳, 😅). Os parentes da V2 são só rótulos em texto (MÃE, TIO, VÓ, PRIMO).
Nada que lembre app de mensagem: fundo rosa → roxo, sem verde, sem tela de conversa, sem tiques de "lida". Os 💬 são o balão genérico do emoji.
Nenhuma marca, time, escudo, celebridade, "Pix", bebida, direção perigosa ou símbolo religioso. Nada de loja, link, preço ou cupom.
- As roletas passam de relance por cartas como 15 MANDO PROMOÇÃO DO MERCADO 🛒, 27 CARRO LAVADO 🚗 e 28 SECO O TIME DO MEU TIO ⚽. São cartas do próprio efeito, genéricas (sem marca, modelo ou time). OK.
- O carrinho do símbolo do perfil é um desenho genérico, sem marca nem modelo. Não é chamada para a loja.
- O 🎄 e o "Feliz Natal" são da data, sem símbolo religioso.

### 1.4 Legendas, hashtags e comentários

| Peça | Legenda sem hashtags | Total com hashtags | Hashtags |
|---|---|---|---|
| C08-V1 | 108 caracteres | 175 | 5 |
| C08-V2 | 110 | 186 | 5 |
| C08-V3 | 100 | 166 | 5 |
| C08-M1 | 110 | 177 | 5 |

- Todas muito abaixo do limite de legenda do TikTok. Texto igual ao `PLANO-DE-VIDEOS.md`, letra por letra.
- Comentários fixados do roteiro: de 77 a 124 caracteres (até 126 se o emoji contar 2), abaixo de 150.
- Nenhuma palavra proibida (prêmio, concorra, ganhe, desafio, loja, link, cupom, "o meu saiu").

### 1.5 Datas e instruções do Montador

- Dias da semana conferidos: sáb 07/11, seg 09/11, ter 10/11, qui 12/11, dom 15/11, sex 20/11, ter 15/12, qui 17/12, seg 21/12, sex 25/12.
- Datas iguais ao `PLANO-DE-VIDEOS.md` (seções 3, 4.4 e 4.5): V1 no D1 (alvo qui 12/11, 19h; com C01 e C08 aprovados no mesmo dia, o C08-V1 sai no dia seguinte ao C01-V1), V2 do D4 ao D6 (alvo dom 15/11, 19h), M1 alvo sex 20/11, 19h, V3 data fixa sex 25/12, 15h.
- Configurações (rótulo de IA desligado, conteúdo comercial desligado, comentários/dueto/costura ligados, som do arquivo) iguais à ficha 2.3 do plano. Teste de som só na V2 e só a partir do D7, como manda a 2.4.
- **Tudo é feito no PC, sem celular:** TikTok Studio no navegador, preview do Effect House, Ferramenta de Captura do Windows e Clipchamp. O que não foi visto na tela está marcado (a confirmar).

### 1.6 O script refaz tudo igual

- Rodei o `render_videos.py` **original** numa pasta do scratchpad (`--saida`): os **15 arquivos saíram idênticos byte a byte** aos entregues pelo produtor.
- Depois da correção, renderizei V2 e V3 no scratchpad e de novo na pasta do efeito: **mesmo md5** nas duas rodadas. V1, capas, legendas e kit continuaram idênticos byte a byte ao original. Só mudaram `C08-V2.mp4`, `C08-V3.mp4` e `previa-videos.png`.
- Testei `--nome` com "Eu no grupo da familia" (sem acento) e "Meu papel no grupo": o nome cabe numa linha no CF, sem aviso de zona, e as 4 legendas mudam (a da M1 só depois da correção 2).
- O script não deixa `__pycache__` na pasta do efeito. O de `videos/lib/` é de 11:04 e não mudou.

---

## 2. O que eu corrigi

1. **Resultado da roleta rápido demais na V2 e na V3.** A carta sorteada ficava parada só ~0,7 s (V2) e ~0,55 s (V3) antes de a cortina do CF subir. Na V3, o confete ainda passava por cima nos primeiros 0,2 s. Dava para ver, mas não para ler com calma.
   - Correção em `render_videos.py`: a roleta da V2 ficou com 2,3 s (era 2,8; vai de 7,3 a 9,6 s) e a da V3 com 3,2 s (era 3,8; vai de 4,2 a 7,4 s). O CF não mudou de lugar (10,75 s e 8,55 s), então o nome segue na tela por ~2 s.
   - "E VOCÊ?", "E você, quem é hoje?" e a carinha 🤔 agora saem junto com a chegada do resultado (antes os tempos eram fixos no código).
   - A roleta continua com 12 (V2) e 17 (V3) cartas e o mesmo ritmo de desaceleração.
   - Re-renderizei `C08-V2.mp4`, `C08-V3.mp4` e `previa-videos.png` pelo script. Conferi quadro a quadro: resultado parado e legível, troca limpa para o CF.
2. **`--nome` não chegava à legenda da M1.** A legenda do kit era montada quando o script carregava, antes de ler o `--nome`. Se o nome publicado sair diferente, `kit-C08-M1/legenda.txt` ficaria com o nome antigo. Agora o nome entra na hora de gerar o kit. O arquivo atual não mudou.
3. **`roteiros-videos.md`:**
   - V3: o roteiro dizia "agenda até 15/12". Com o Agendar limitado a 10 dias (a confirmar), o 25/12 às 15h só abre a partir de **ter 15/12 às 15h**. Agora diz para agendar na rodada de **qui 17/12** (ou seg 21/12).
   - M1: novo **passo 0**. Conferir que o projeto do C08 no PC ainda é o C08 antes de gravar (ver "Riscos", item 2), e não salvar ao fechar.
   - V2 e V3: tempos e tamanhos novos nas tabelas. Seção 4: volume, determinismo e tempo do resultado. Seção 5: o `--nome` refaz também a legenda da M1.
   - Linha no topo apontando para esta revisão.

Não editei a biblioteca (`videos/lib/render.py`), o `PRONTO-PARA-MONTAR.md` nem o `STATUS.md`. Não apaguei nada.

---

## 3. Riscos que ficam (para a coordenação)

1. **Ordem do Montador para a V3.** A lista de tarefas do produtor diz "C08-V3: agendar até 15/12". Isso não funciona se o limite for 10 dias: antes de 15/12 às 15h o agendador não alcança o 25/12. Pedido: na ordem para o Montador, usar "agendar na rodada de qui 17/12 (ou seg 21/12)". O plano (seção 3, C08-V3) tem a mesma frase "agenda até 15/12".
2. **Projeto do C08 pode ter virado o C01.** A atualização das 05:40 UTC de 06/11 do `PRONTO-PARA-MONTAR.md` mandou montar o C01 "reaproveitando o projeto do C08". O STATUS diz que o C01 ficou em `projetos\C01-torcedometro`, o que sugere um "Salvar como", mas não confirma que o do C08 ficou intacto. Se foi salvo por cima, o PC não tem mais o C08 e a **M1 não tem como ser gravada**. O roteiro agora manda conferir (passo 0). Pedido: na próxima atualização, perguntar ao Montador se `projetos\C08-grupo-familia-1rosto` ainda abre como C08.
3. **Horário da V1:** a tabela 4.4 do plano dá qui 12/11 às **19h**, mas a regra 4.2 dá **18h** de terça a quinta. A própria tabela mistura os dois nas quintas. A coordenação decide (a confirmar).
4. **Luz piscante na roleta.** O começo troca a carta ~9 a 11 vezes por segundo, por menos de 1 s. O plano só limita a 3 por segundo o trecho "pausa" e já prevê desacelerar se algum post receber o aviso (a confirmar). Se acontecer: aumentar `intervalo_ini` em `roleta()` no script e rodar de novo (uns 3 minutos).
5. **Volume da V3 um pouco mais alto** (-11,8 LUFS, contra -13,4 e -13,6). É o trecho dos 8 plins seguidos (FELIZ NATAL × 200), que é a ideia da cena. Pico em -0,9 dBFS, sem estouro. Deixei como está.
6. **Símbolo do CF = foto recomendada.** Se a coordenação escolher outra foto de perfil (`PERFIL.md`), o CF fica diferente da foto. Aí é ajustar `avatar()` no script e rodar de novo.
7. **Formato de entrega diferente da ficha 2.3:** capas em JPG (não PNG), arquivos na pasta do efeito (não em `videos/prontos/<código>/`) e uma prancha só (`previa-videos.png`). Motivo: o limite de 12 MB. Aceitar JPG em "Editar capa → Carregar" fica para o passo 0 do Montador (a confirmar).
8. **Biblioteca (aviso para os outros produtores):** o `Video.renderizar` manda os quadros por pipe para o x264 com várias threads e não sai igual byte a byte. O C08 contorna com `renderizar_det()` (intermediário sem perda + 2 passadas lendo do arquivo). O script também usa atributos internos da biblioteca para checar a zona segura das camadas próprias (com proteção se eles mudarem de nome).
9. **M1 depende do Montador:** sincronia do `assinatura.wav` com o clique (~3 s) e o final (9,5 s); clipe com licença anotada; regras do desafio sobre autorização de quem aparece (se pedirem, a M1 não sai).
10. **(a confirmar) no PC e no site:** Agendar e o limite de 10 dias; "Editar capa → Carregar"; "Fixar" comentário; aba de efeitos no perfil; botão de gravar do preview do Effect House; Win + Shift + R; Clipchamp e WAV mono; Biblioteca Comercial.
