# C06 Meu amigo secreto: revisão de QA dos vídeos

Feita em 06/11/2026 pela nuvem (revisor de QA dos vídeos do C06).
**Vini, você não precisa fazer nada com este arquivo.** Ele é para a coordenação.

**Nota: 9 de 10. Pronto para liberar ao Montador.**
Corrigi dois problemas de tempo (V1 e V3) e um de som (V3). O resto passou como estava.

---

## Resumo

1. Os 3 MP4 seguem a ficha técnica: 1080x1920, 30 fps, H.264 High yuv420p, AAC estéreo, de 9 a 12 s, todos com menos de 4 MB.
2. **V1:** o cartão final tinha só 1,5 s. A regra 2.2 do plano pede de 2 a 2,5 s. **Agora tem 2,0 s**, e o vídeo continua com 10 s.
3. **V3:** o resultado da roleta ficava parado só 0,8 s antes do cartão final. Era pouco para ler "UM PRESENTÃO (FOI ENGANO)" e o "Durou pouco". **Agora fica 1,5 s**, e o vídeo continua com 12 s.
4. **Som do V3:** com os novos tempos, o pico real subiu para -0,7 dBTP. O script agora mede o pico depois do AAC e abaixa o ganho sozinho. **Ficou em -2,4 dBTP.**
5. O script roda de novo e gera os mesmos arquivos, byte a byte (16 arquivos, sha256 iguais em 2 rodadas).

---

## 1. O que conferi

### 1.1 Ficha técnica (ffprobe, volumedetect e loudnorm, nos arquivos finais)

| Arquivo | Duração | Tamanho | Vídeo | Áudio | Volume médio / máximo | Loudness | Pico real |
|---|---|---|---|---|---|---|---|
| C06-V1.mp4 | 10,0 s (300 quadros) | 2.683.722 B (2,56 MB) | H.264 High, yuv420p, 1080x1920, 30 fps | AAC LC, 44,1 kHz, estéreo | -18,7 / -2,2 dB | -15,9 LUFS | -2,0 dBTP |
| C06-V2.mp4 | 9,0 s (270 quadros) | 2.614.177 B (2,49 MB) | igual | igual | -18,7 / -2,1 dB | -14,9 LUFS | -2,0 dBTP |
| C06-V3.mp4 | 12,0 s (360 quadros) | 2.934.507 B (2,80 MB) | igual | igual | -19,5 / -2,4 dB | -16,7 LUFS | -2,4 dBTP |

- Os 3 MP4 somam 8.232.406 B (7,85 MB). O limite é 12 MB.
- A pasta `videos/` inteira, com script, roteiros, kit e prévia, tem 10,8 MB.
- Os 3 têm som audível do começo ao fim (trilha + efeitos). Nenhum clipa.

### 1.2 Quadros abertos e revisados

Tirei 15 quadros do V1, 14 do V2 e 16 do V3, sempre incluindo 0,0 s, 0,5 s, 1,0 s e o último quadro. Montei pranchas com as faixas da interface do TikTok (topo 220 px, base 420 px, direita 140 px) e abri cada uma.
Pranchas no scratchpad da sessão (`/tmp/claude-0/-home-user-quantocobrarpj/97fcacc8-f478-5bbc-9659-8b19d0155dbf/scratchpad/qa-C06/prancha_C06-V1_final.png`, `..._V2_final.png` e `..._V3_final.png`); elas não vão para o projeto.

| Item | V1 | V2 | V3 |
|---|---|---|---|
| Gancho no 1º quadro | ✅ "Todo ano é meia no amigo secreto?" (7 palavras) | ✅ "PAUSA AGORA ⏸️🎁 / e vê seu presente" (6) | ✅ "Amigo secreto da firma é sempre igual" (7) |
| Carta no 1º quadro | ✅ 1 MEIA (DE NOVO) | ✅ 1 MEIA (DE NOVO) | ✅ 14 SANDUICHEIRA (EU JÁ TENHO 2) |
| Quadro de 0,5 s serve de capa | ✅ | ✅ | ✅ |
| Texto dentro da zona segura | ✅ (`avisos_zona` vazio) | ✅ | ✅ |
| Acentos | ✅ | ✅ | ✅ |
| Nome do efeito | ✅ "Meu amigo secreto", igual ao `textos.md`, em amarelo, 1 linha | ✅ | ✅ |
| Resultado da roleta parado | 1,5 s (6,5 a 8,0 s) | não tem roleta | **1,5 s** (8,0 a 9,5 s; era 0,8 s) |
| Cartão final | **2,0 s** (8,0 a 10,0 s; era 1,5 s) | 2,0 s (7,0 a 9,0 s) | 2,5 s (9,5 a 12,0 s) |
| Trocas no "pausa" | — | 2,86 por segundo (limite: 3) | — |

### 1.3 Capas e kit da M1

- **Capas** (`C06-V1-capa.jpg`, `C06-V2-capa.jpg`, `C06-V3-capa.jpg` e `kit-C06-M1/capa.jpg`): 1080x1920, de 240 a 258 KB. Texto grande e carta dentro do miolo 3:4 (y de 240 a 1680). Acentos certos. Nome do filtro igual.
- **`gancho.png`**: transparente, 1080x1920. A pílula vai de y 243 a 424 (dentro da zona).
- **`gancho-baixo.png`**: a pílula vai até y 1478. Só a sombra fraca chega a 1501 (1 px além da faixa). Não precisa mudar.
- **`final.png`**: o mesmo cartão final dos vídeos, parado, com "O que você vai ganhar?".
- **`assinatura.wav`**: 12,0 s, mono, 44,1 kHz, -17,8 LUFS, pico real -1,2 dBTP. Pop de caixa em 3,0 s e assinatura em 9,5 s, como diz o roteiro.
- **`legenda.txt`**: igual à do plano, com 5 hashtags.

### 1.4 Regras fixas

- **Cartas fora dos vídeos:** 4, 11 e 21 (acessórios de carro, o que a loja vende) e 15 (desodorante) não aparecem em nenhum quadro. Conferi no código (`FORA_DOS_VIDEOS`) e nas pranchas. Concordo com a decisão do produtor.
- **As 22 cartas que aparecem:** abri todas em tamanho cheio. A 2 (TRANSFERÊNCIA DE 10 REAIS) mostra só notas, sem o losango do Pix e sem banco. A 10 (MILAGRE) tem alvo e brilhos, nada religioso. Nenhuma tem marca, logo, time, bebida ou direção.
- **Cartão final:** usa o símbolo do perfil (o carrinho turquesa na mira da câmera, de `videos/perfil/`), como manda a regra 2.2 do plano. É um desenho genérico, sem modelo reconhecível. Não tem loja, link, preço nem produto.
- **Sem pessoa:** nos vídeos N, a "cabeça" é sempre uma carinha emoji (🤔, 😅, 😳).
- **Palavras proibidas:** procurei Black Friday, prêmio, sorteio, concorra, ganhe, desafio, loja, link, cupom, preço e Pix nas 4 legendas e nos 8 comentários. Nenhuma aparece.

### 1.5 Roteiros e postagem (`roteiros-videos.md`)

- **Legendas:** de 154 a 190 caracteres, com 5 hashtags cada. O limite de legenda do TikTok é bem maior (o número exato na web: a confirmar).
- **Comentários fixados:** de 80 a 112 caracteres. O limite do plano é 150. Os números anotados no roteiro estão certos.
- **Datas:** conferi o dia da semana de todas (qua 25/11, sex 27/11, sáb 28/11, seg 30/11, ter 01/12, qua 02/12, qui 03/12, sex 04/12, seg 07/12, qui 10/12, sex 11/12, seg 14/12, qui 17/12, sex 18/12, seg 21/12). Estão iguais à tabela 4.4 do `PLANO-DE-VIDEOS.md`.
- **Agendar com até 10 dias:** 17/12 só cabe a partir de seg 07/12, e 21/12 a partir de sex 11/12. O roteiro está certo.
- **Configurações:** Todos; comentários, dueto e costura ligados; rótulo de IA desligado; conteúdo comercial desligado; som do arquivo. Igual às seções 2.3 e 2.5 do plano.
- **Sem celular:** todos os passos usam o TikTok Studio no navegador, o Effect House, a Ferramenta de Captura e o Clipchamp do PC. Nenhum passo pede o app.

### 1.6 Determinismo

- **Antes de mexer:** rodei o `render_videos.py` original numa pasta do scratchpad. Os 16 arquivos saíram com sha256 iguais aos que estavam na pasta.
- **Depois das correções:** rodei de novo na pasta do projeto e, ao mesmo tempo, numa pasta do scratchpad. Os 16 arquivos saíram iguais, byte a byte.

---

## 2. O que corrigi

Tudo pelo `render_videos.py`. Não mexi na biblioteca (`videos/lib/render.py`) nem nas artes (`../assets`).

| # | Problema | Correção | Arquivos |
|---|---|---|---|
| 1 | **V1:** o cartão final tinha 1,5 s (8,5 a 10 s). A regra 2.2 e a conferência da 2.3 pedem de 2 a 2,5 s no fim, e é ali que entra o nome do filtro. | A roleta gira 3,5 s (era 4,0 s). O resultado continua parado 1,5 s (6,5 a 8,0 s). O cartão final vai de 8,0 a 10,0 s. | `C06-V1.mp4` |
| 2 | **V3:** o resultado (23 UM PRESENTÃO (FOI ENGANO)) ficava só 0,8 s na tela (8,7 a 9,5 s), com o "Durou pouco 😅" por cima. | A roleta gira 2,3 s (era 3,0 s). O resultado fica parado 1,5 s (8,0 a 9,5 s). O "Esse ano vai ser…", o "2026" e o 🤔 saem junto com o resultado. Cartão final igual (9,5 a 12 s). | `C06-V3.mp4` |
| 3 | **Som do V3:** depois da correção 2, o pico real do V3 subiu para -0,7 dBTP (os sons do resultado caíram em outro ponto da trilha). O ganho fixo de 0,84 não garante folga depois do AAC. | Função nova `pico_real_aac`: o script codifica só o áudio, mede o pico real e, se passar de -1,2 dBTP, abaixa o ganho daquela peça. O V3 ficou com ganho 0,7652 e pico de -2,4 dBTP. V1 e V2 não mudaram (o V2 saiu com os mesmos bytes). | `render_videos.py`, `C06-V3.mp4` |
| 4 | A prancha `previa-videos.png` mostrava os tempos antigos. | Novos tempos da prévia (V1: 4,5 s e 7,2 s; V3: 8,8 s). Regerada e revisada. | `previa-videos.png` |
| 5 | Faltava um caso de data no V1: aprovação em ter 01/12 põe o D1 na qua 02/12, noite da última rodada (regra 4.1). | Linha nova no roteiro: nesse dia, o V1 sai às 15h. Vale o mesmo para dom 06/12 se a final for à noite (hora a confirmar). | `roteiros-videos.md` |
| 6 | O roteiro trazia os tempos antigos do V1 e do V3 e o pico de -1,2 dBFS. | Tabelas do V1 e do V3, linha do som e "Para a nuvem" atualizadas. Pus um aviso no topo apontando para esta revisão. | `roteiros-videos.md` |

**Não mudaram:** `C06-V2.mp4`, as 3 capas, as 3 legendas e todo o `kit-C06-M1/`. Os sha256 deles são os mesmos de antes.
**Limpeza:** apaguei uma pasta `__pycache__` que o meu teste de importação criou em `videos/`. A do `videos/lib/` já existia e ficou.

---

## 3. Para a coordenação (eu não edito PRONTO-PARA-MONTAR.md nem STATUS.md)

- **As durações não mudaram** (V1 10 s, V2 9 s, V3 12 s). As tarefas do Montador continuam valendo como estão.
- **Repasso o aviso do produtor:** no plano, "Montador agenda até 07/12" (V3) e "até 11/12" (V2) são o **primeiro** dia possível, por causa do limite de 10 dias do Agendar. Não são prazo. No PRONTO-PARA-MONTAR, o certo é "a partir de".
- **Caso novo para o Montador:** se o D1 do C06 cair na qua 02/12, o V1 sai às 15h (nada na noite da última rodada).
- **Foto e nome do perfil:** ficam com o diretor de marca (`PERFIL.md`). O cartão final usa `videos/perfil/simbolo_transparente.png`. Se o símbolo mudar, basta rodar `python3 render_videos.py` de novo (uns 100 s). Os vídeos se refazem sozinhos.

---

## 4. Riscos que ficam

1. **Luz piscante (a confirmar):** nos primeiros segundos, a roleta troca de carta de 9 a 11 vezes por segundo (é o padrão das roletas de todos os efeitos). O "pausa" do V2 está dentro do limite de 3 por segundo. Se algum post receber o aviso de luz piscante, a nuvem aumenta o `intervalo_ini` da `roleta_c06` (hoje 0,085 s) e roda de novo.
2. **Nome publicado diferente no D0:** a nuvem roda `render_videos.py --nome "Nome Publicado"` antes do D1.
3. **Recursos da web (a confirmar):** Agendar, "Editar capa → Carregar", "Fixar" comentário e a Biblioteca de Música Comercial (só para o teste de som do V2).
4. **M1 depende do Montador:** clipe do Pexels ou do Mixkit com licença, botão de gravar do preview, Win + Shift + R e Clipchamp (tudo a confirmar no PC). Se não ficar pronta, o horário fica vago.
5. **Desafio (a confirmar):** se as regras pedem autorização por escrito de quem aparece na M1 (pessoa de banco de imagem).
6. **Data do V3:** a "sexta das confraternizações" em 18/12 é estimativa (a confirmar). Se o C06 só for aprovado depois de 16/12, vale a regra do roteiro.
7. **`assinatura.wav` da M1:** está em -17,8 LUFS, um pouco abaixo dos vídeos N (cerca de -16). O TikTok iguala o volume. Risco baixo; não mexi para não mudar o kit já entregue.
8. **Cartas de acessório de carro fora dos vídeos:** é decisão do produtor, e eu concordo. Se a coordenação desfizer, basta tirar o número de `FORA_DOS_VIDEOS` e rodar de novo.
