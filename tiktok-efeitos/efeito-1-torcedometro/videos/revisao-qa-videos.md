# C01 Torcedômetro: revisão de QA dos vídeos

Feita em 06/11/2026 pela nuvem (revisor de QA dos vídeos do C01).
**Vini, você não precisa fazer nada com este arquivo.** Ele é para a coordenação e o Montador.

**Resultado: aprovado, nota 9.** Os 3 vídeos, as capas, as legendas e o kit da M1 podem ser liberados.
Corrigi 1 defeito visual nos vídeos V1 e V3 (já re-renderizados) e ajustei 3 pontos do `roteiros-videos.md`.
Há **1 risco urgente para a coordenação**: o projeto do C01 no PC vai ser reaproveitado para o C02 (ver "Riscos", item 1).

---

## 1. O que eu conferi

### 1.1 Parte técnica (ffprobe e ffmpeg, depois da correção)

| Vídeo | Duração | Tamanho | Imagem | Som | Volume |
|---|---|---|---|---|---|
| C01-V1.mp4 | 10,0 s (300 quadros) | 2.738.252 bytes (2,61 MB) | 1080x1920, 30 fps, H.264 High, yuv420p, BT.709 | AAC estéreo 44,1 kHz, ~137 kbps | -14,8 LUFS · pico -1,9 dBFS · média -18,2 dB |
| C01-V2.mp4 | 9,0 s (270 quadros) | 2.621.486 bytes (2,50 MB) | igual | AAC estéreo, ~143 kbps | -15,9 LUFS · pico -1,1 dBFS · média -18,2 dB |
| C01-V3.mp4 | 12,0 s (360 quadros) | 3.013.337 bytes (2,87 MB) | igual | AAC estéreo, ~140 kbps | -14,6 LUFS · pico -2,0 dBFS · média -18,1 dB |

- Os 3 ficam entre 6 e 15 s e abaixo de 4 MB. **Pasta inteira: 10,65 MB** (11.169.177 bytes, já com esta revisão), abaixo do limite de 12 MB.
- Som audível do começo ao fim: nenhum silêncio de mais de 0,3 s (abaixo de -45 dB). Pico abaixo de -1 dBFS em todos.
- MP4 com o índice no começo (sobe rápido no navegador) e quadro-chave a cada 2 s.
- `kit-C01-M1/assinatura.wav`: 12,0 s, mono, 44,1 kHz, 16 bits. Medi -14,3 LUFS e pico -1,5 dBFS (o produtor anotou -15,6 LUFS; a diferença é da medição em mono e não muda nada na prática).
- `gancho.png` e `gancho-baixo.png`: 1080x1920, fundo transparente. `final.png` e as 4 capas: 1080x1920.

### 1.2 Quadros abertos e revisados (um por um)

Extraí **18 tempos de cada vídeo** (sempre com 0,0 s, 0,5 s, o 1º segundo e o último quadro), mais recortes do resultado da roleta e tiras quadro a quadro da entrada do cartão final. Abri todas as pranchas.
Pranchas (no scratchpad da nuvem, pasta `qa-C01/`): `prancha-C01-V1-a.png`, `-b.png`, `prancha-C01-V2-a/b.png`, `prancha-C01-V3-a/b.png`, `rec-V1-res.png`, `rec-V3-res.png`, `tira-V1-corte-novo.png`, `tira-V3-corte-novo.png`, `capas.png`, `kit.png` e `nomes-alternativos.png`.

| Ponto | V1 | V2 | V3 |
|---|---|---|---|
| Gancho no 1º quadro | ✅ "Que tipo de **torcedor** você é?" + carta 8 + 🤔 + ⚽ | ✅ "**PAUSA AGORA** ⏸️ e vê o seu" + carta 2 + 🤔 | ✅ "Dia de final: **gira antes do jogo**" + carta 19 + 🤔 |
| Gancho com até 7 palavras | 6 | 6 | 7 |
| Quadro de 0,5 s serve de capa | ✅ | ✅ | ✅ |
| Resultado legível | 3 PÉ-FRIO CERTIFICADO, legível de ~6,7 a 8,05 s (~1,4 s, com a reação junto). O confete passa só pelo ícone da carta | 20 cartas de 0,35 s, todas legíveis, sem repetir, na ordem do roteiro | 13 NÃO OLHA O PÊNALTI, legível de ~8,1 a 10,05 s (~2 s) |
| Cartão final (CF) | 8,0–10,0 s: símbolo + "Procura na lupa 🔎" + **Torcedômetro** (amarelo, 1 linha) + "Serve pra qualquer time ⚽" | 7,0–9,0 s, com "Qual pegou? Conta aqui 👇" | 10,0–12,0 s, com "Serve pra qualquer time ⚽" |
| Zona segura (topo 220, base 420, direita 140) | ✅ nada fora; nenhum aviso | ✅ | ✅ |

- **Nome do efeito:** "Torcedômetro", igual ao `textos.md`, na tela, nas 4 legendas, nas 4 capas e nos comentários do roteiro.
- **Acentos conferidos na tela:** você é, vê, Torcedômetro, PÉ-FRIO, TÉCNICO DE SOFÁ, NÃO OLHA O PÊNALTI, CARDÍACO NOS ACRÉSCIMOS, ATÉ, 2º TEMPO, assistir…, É. Nenhum erro.
- **Miolo em x = 520:** as cartas na escala 1,6 vão de x 110 a 930 (a zona livre vai até 940). A carta passa da borda só no quique de entrada do resultado (menos de 0,1 s), o que é aceitável.
- **Luz piscante:** o "pausa" do V2 troca a cada 0,35 s (2,9 por segundo), dentro do limite de 3. Sem flash branco de tela cheia.
- **Capas:** texto grande dentro do miolo 3:4 (y 240 a 1680). O rodapé "Filtro: Torcedômetro 🔎" fica em y ~1520, dentro do 3:4. A capa não aparece por baixo dos botões do feed, então a zona do vídeo não vale para ela.
- **Kit da M1:** pílula do `gancho.png` em x 92–948 e y 244–417 (só 8 px de branco passam da linha da direita; o texto fica em x 130–909). `gancho-baixo.png` em y 1299–1472, acima da base. `final.png` igual ao CF, com "Gira antes do jogo ⚽".

### 1.3 Regras fixas

Nenhum nome, escudo, cor combinada ou apelido de time. Nenhum nome de campeonato ("dia de final" só). Nenhuma marca, celebridade, "Pix", bebida, direção perigosa ou religião. Nada de loja, link, preço ou cupom.
- As roletas usam 24 das 26 cartas: ficaram fora a 14 (mãos de reza 🙏) e a 23 (carreata). Concordo: o vídeo pode ser pausado em qualquer quadro.
- A carta 22 BUZINA QUANDO SAI GOL aparece de relance nas roletas. O carro do desenho é genérico (sem marca nem modelo). OK.
- O símbolo do CF é o carrinho turquesa na mira de câmera (`videos/perfil/simbolo_transparente.png`), o mesmo desenho da foto de perfil recomendada (`PERFIL.md`). Não é chamada para a loja.
- Nenhuma pessoa, rosto ou silhueta: no lugar da cabeça, só emoji (🤔, 🥶, 🙈).

### 1.4 Legendas, hashtags e comentários

| Peça | Legenda sem hashtags | Total com hashtags | Hashtags |
|---|---|---|---|
| C01-V1 | 94 caracteres | 150 | 5 |
| C01-V2 | 84 | 140 | 5 |
| C01-V3 | 104 | 164 | 5 |
| C01-M1 | 112 | 170 | 5 |

- Todas muito abaixo do limite de legenda do TikTok. Texto igual ao `PLANO-DE-VIDEOS.md` (a V2 sai sem "ou no meu perfil" até a conferência da aba de efeitos, como manda a seção 2.2 do plano).
- Comentários fixados do roteiro: de 67 a 114 caracteres (até 116 se o emoji contar 2), abaixo de 150.
- Nenhuma palavra proibida (prêmio, sorteio, concorra, ganhe, desafio, time, loja, link, cupom).

### 1.5 Datas e instruções do Montador

- Dias da semana conferidos: qua 11/11, sáb 14/11, qua 18/11, qui 19/11, sex 20/11, sáb 28/11, qua 02/12, dom 06/12.
- Datas iguais ao `PLANO-DE-VIDEOS.md` (seções 3, 4.4 e 4.5): V1 no D1 (alvo qua 11/11, 17h30), V2 do D4 ao D6 (alvo sáb 14/11, 15h), V3 data fixa sáb 28/11, 14h, M1 data fixa dom 06/12. Exemplo de aprovação mais cedo (sáb 07/11 → V1 dom 08/11 19h, V2 qua 11/11 18h) igual ao plano.
- Configurações (rótulo de IA desligado, conteúdo comercial desligado, comentários/dueto/costura ligados, som do arquivo) iguais à ficha 2.3 do plano.
- **Tudo é feito no PC, sem celular:** TikTok Studio no navegador, preview do Effect House, Ferramenta de Captura do Windows e Clipchamp. O que não foi visto na tela está marcado (a confirmar).

### 1.6 O script refaz tudo igual

- Rodei o `render_videos.py` **original** numa pasta do scratchpad (`--pasta`): os **16 arquivos saíram idênticos byte a byte** aos entregues pelo produtor.
- Depois da correção, re-renderizei na pasta do efeito e rodei de novo no scratchpad: **idênticos byte a byte** outra vez.
- Testei também nomes publicados diferentes (`--nome Torcedometro`, "Que Torcedor Você É" e "Roleta do Torcedor"): o nome cabe numa linha no CF e não há aviso de zona.
- O script não deixa `__pycache__` na pasta do efeito.

---

## 2. O que eu corrigi

1. **Reação por cima do cartão final (V1 e V3).** O texto "Isso explica muita coisa 🥶" (V1) e "Liberado pra assistir… de costas 🙈" (V3) ficava por cima do cartão final de 8,0 a 8,35 s (V1) e de 10,0 a 10,35 s (V3). Nos últimos quadros, ele encostava no símbolo do perfil.
   - Correção em `render_videos.py`: a reação passou para a camada 51 (acima do confete, abaixo da cortina do CF). Agora a cortina amarela sobe e cobre o texto junto com a carta.
   - Re-renderizei `C01-V1.mp4`, `C01-V3.mp4` e `previa-videos.png`. Conferi quadro a quadro: a transição ficou limpa. O resto ficou igual (C01-V2, capas, legendas e kit, byte a byte).
2. **Rodapé da capa em 1 linha** (`render_videos.py`, função `_capa`). Com um nome publicado mais longo (ex.: "Que Torcedor Você É"), o rodapé quebrava em 2 linhas e deixava "É 🔎" sozinho na capa da M1. Agora a fonte diminui e fica em 1 linha. As capas atuais não mudaram.
3. **`roteiros-videos.md`:**
   - V3: com o Agendar limitado a 10 dias (a confirmar), o 28/11 só abre a partir de qua 18/11. O roteiro agora diz para agendar na rodada de **qui 19/11** (a de seg 16/11 não alcança).
   - M1: novo **passo 0**. Conferir que `projetos\C01-torcedometro` ainda é o Torcedômetro antes de gravar; gravar a M1 antes de reaproveitar o projeto para o C02, ou reaproveitar com "Salvar como".
   - V1: a tabela diz que a roleta usa 24 das 26 cartas (sem a 14 e a 23). Antes isso só aparecia na V2.
   - Linha no topo apontando para esta revisão.

Não editei a biblioteca (`videos/lib/render.py`), o `PRONTO-PARA-MONTAR.md` nem o `STATUS.md`. Não apaguei nada.

---

## 3. Riscos que ficam (para a coordenação)

1. **URGENTE: o projeto do C01 vai ser reaproveitado para o C02.** A atualização de 10:00 UTC do `PRONTO-PARA-MONTAR.md` manda montar o C02 "reaproveitando o projeto `projetos\C01-torcedometro`". E o C02 é a próxima tarefa do Montador quando o PC ligar. Se ele editar por cima, o PC fica sem o Torcedômetro e a **M1 (06/12) não tem como ser gravada**. Pedido: na próxima atualização, mandar o Montador (a) gravar o bruto da M1 antes do C02, ou (b) reaproveitar com "Salvar como". O mesmo vale para C06 e C07, que também reaproveitam esse projeto.
2. **Luz piscante na roleta.** O começo da roleta troca a carta a cada 0,075 s (~13 por segundo) por cerca de 1 s. O plano só limita a 3 por segundo o trecho "pausa", e já prevê desacelerar a roleta se algum post receber o aviso (a confirmar). Se o aviso aparecer no C01-V1, a nuvem refaz V1 e V3 com `intervalo_ini` maior em `render_videos.py`.
3. **Tempo do resultado no V1:** ~1,4 s com a reação junto. Segue o roteiro do plano (6,6–8,0 s). Se no D3 a retenção do V1 vier baixa, uma versão com +0,5 s de resultado é fácil de fazer.
4. **Símbolo do CF = foto de perfil recomendada.** Se a coordenação escolher outra foto (opção 2 ou 3 do `PERFIL.md`), o CF fica diferente da foto. Aí é trocar `SIMBOLO` no script e re-renderizar (uns 90 s).
5. **Formato de entrega diferente da ficha 2.3:** capas em JPG (não PNG), arquivos na pasta do efeito (não em `videos/prontos/<código>/`) e uma prancha só. Motivo: o limite de 12 MB. A coordenação copia para `videos/prontos/` se quiser.
6. **V2 "Teste de som: sim" no D4,** mas o plano (2.4) só deixa testar a partir do D7. O roteiro resolve (sai com o nosso som no D4). A coordenação confirma.
7. **Biblioteca (aviso para os outros produtores):** o `Video.renderizar` com várias threads não sai igual byte a byte, e o pico depois do AAC pode chegar a -0,1 dBFS. O C01 contorna os dois (1 thread e mix 1 dB mais baixo).
8. **`__pycache__` em `videos/lib/`** (criado às 11:04 UTC). Não fui eu e não apaguei. O git já ignora.
9. **(a confirmar) no PC e no site:** Agendar e o limite de 10 dias; "Editar capa → Carregar"; "Fixar" comentário; aba de efeitos no perfil; botão de gravar do preview do Effect House; Win + Shift + R; Clipchamp aceitar WAV mono; horários dos jogos de 14/11 e 06/12. As datas de futebol vêm do `plano-curto-prazo.md` e não foram reconferidas aqui.
