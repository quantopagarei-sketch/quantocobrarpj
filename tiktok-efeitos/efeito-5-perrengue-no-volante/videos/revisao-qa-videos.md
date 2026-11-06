# C09 Perrengue no volante: revisão de QA dos vídeos

Feita em 06/11/2026 pela QA dos vídeos (nuvem).
**Vini, você não precisa fazer nada com este arquivo.** É para a coordenação e para quem refizer os vídeos.

**Resultado: liberado para o Montador.** Nota **9,0 de 10**.
Achei 2 defeitos de tela e 1 defeito no script. Corrigi os 3 e renderizei os 3 vídeos de novo pelo `render_videos.py`. Também ajustei 3 pontos no `roteiros-videos.md`.

---

## 1. O que eu corrigi

| # | Problema | Onde | O que fiz |
|---|---|---|---|
| 1 | **Acento e cedilha encostando na outra linha** nos itens da lista. "POÇA QUE / ERA CRATERA" parecia "ĆRATERA". O acento de "ATRÁS" marcava o "COM" de cima. O de "DÁ SETA" marcava o "QUEM". Aparece nos 3 vídeos, a lista fica na tela quase o tempo todo | `render_videos.py`, `sprites_itens()` | Entrelinha de 0,93 para 1,12. Os acentos ficaram soltos. O texto da lista diminuiu uns 7% e continua legível (conferido em tamanho real) |
| 2 | **O nome do filtro estava fixo no código** no gancho do V1 e na capa do V1. Com `--nome` (nome publicado diferente), a tela mostrava o nome antigo no 1º segundo. Testei com "Ranking dos perrengues": o gancho continuava "perrengue no volante" | `render_videos.py`, `video_v1()` e `capa_v1()` | O gancho e a capa agora usam o nome passado. Criei `nome_em_2_linhas()` para quebrar o nome na capa. Testado de novo com "Ranking dos perrengues": gancho, capa, cartão final e legenda trocam juntos |
| 3 | **Gancho do V1 com "perrengue" minúsculo**, em amarelo, com cara de nome do filtro. O nome exato é **Perrengue no volante** | Gancho do V1 | Saiu junto com a correção 2: agora é "Ranking às cegas: **Perrengue no volante**" |
| 4 | Tamanhos dos MP4 desatualizados no roteiro | `roteiros-videos.md` | Atualizei os bytes (V1 3.572.458; V2 3.574.289; V3 3.089.439) |
| 5 | Resposta pronta "quero ver se tu **também** gasta o 1 cedo" dava a entender que a conta usou o filtro (o plano proíbe "o meu deu…") | `roteiros-videos.md`, respostas | Troquei por "quero ver se tu aguenta não gastar o 1 cedo 😂" |
| 6 | "Repostar quem usou" sem o caso de a web não ter o botão | `roteiros-videos.md`, "Depois de postar" | Incluí: só se a web tiver "Repostar" (a confirmar no passo 0); se não tiver, fica só o comentário (plano 5.6, item 7) |

A biblioteca `videos/lib/render.py` **não foi editada**. As capas e as legendas não mudaram (mesmo md5 de antes).

---

## 2. O que eu conferi

### 2.1 Ficha técnica (ffprobe e ffmpeg, depois da correção)

| Arquivo | Duração | Tamanho | Vídeo | Áudio | Volume |
|---|---|---|---|---|---|
| `C09-V1.mp4` | 14,0 s | 3.572.458 bytes (3,41 MB) | 1080x1920, 30 fps, H.264 High, yuv420p | AAC estéreo 44,1 kHz | -14,9 LUFS, pico -1,5 dB |
| `C09-V2.mp4` | 14,0 s | 3.574.289 bytes (3,41 MB) | igual | igual | -14,8 LUFS, pico -1,9 dB |
| `C09-V3.mp4` | 12,0 s | 3.089.439 bytes (2,95 MB) | igual | igual | -15,4 LUFS, pico -1,9 dB |

- Todos entre 6 e 15 s e abaixo de 4 MB. Os 3 MP4 somam 10,2 MB. A pasta `videos/` inteira fica em uns 11,4 milhões de bytes (abaixo de 12 MB).
- Som presente e audível: volume médio de -18 dB no vídeo todo e de -23 a -25 dB já no 1º segundo. Nenhum silêncio maior que 0,3 s.
- Aviso de zona segura do script: **vazio** nos 3.

### 2.2 Quadros (abri cada prancha)

Tirei 12 quadros de cada vídeo, do 0,0 s ao último quadro, com a interface do TikTok marcada em vermelho (topo 220 px, base 420 px, direita 140 px). Também abri em tamanho real o quadro final do V1 e do V2 e o 1º quadro do V1.

- **Gancho no 1º quadro (0,0 s):** sim nos 3. "Ranking às cegas: Perrengue no volante" (6 palavras), "Regra: o 1 só no último 🔒" (6), "Nos comentários é fácil 😏" (4).
- **Quadro de 0,5 s como capa reserva:** funciona nos 3 (gancho grande, carta inteira, painel de 1 a 10).
- **Nome do filtro:** "Perrengue no volante", igual ao `textos.md`, no cartão final dos 3, numa linha, em amarelo. Igual também na capa, na legenda e no comentário fixado.
- **Cartão final:** nos 2 s finais dos 3, com "Procura na lupa 🔎", o símbolo do perfil e a pergunta da peça.
- **Zona segura:** tudo que importa fica entre x 60 e 940 e entre y 220 e 1500. A parte de baixo da tela fica só com o fundo.
- **Acentos:** certos em tudo (ÀS, SÓ, ÚLTIMO, COMENTÁRIOS, É FÁCIL, NÃO, DÁ, POÇA, ATRÁS, 1º, você, Cadê). Depois da correção, nenhum encosta na outra linha.
- **Resultado legível por tempo suficiente:** a lista completa fica na tela os 2 s finais, junto com o cartão final. O arrependimento do V1 (PNEU FURADO com a vaga 1 piscando em vermelho e "NÃO! Cadê o 1? 😩") fica 1,5 s. O "cai no 1" do V2 (🔓, brilho e "Oficialmente o pior perrengue da vida 🤷") fica 1,4 s.
- **Ordem do ranking igual ao plano:** V1: 1→1, 4→5, 6→7, 5→9, 9→8, 3→4, 8→6, 2→2, 10→3, 7→10. V2: a 10 BATERIA ARRIADA vai para a 2 com "Ai… regra é regra"; a 5 LAVAR O CARRO E CHOVER cai no 1. V3: o próximo item nunca aparece antes de sair da carta "?".
- **Luz piscante:** no máximo 1,7 troca por segundo (V3). O 🔒 pisca a 104 bpm e o contorno vermelho pulsa 2 vezes por segundo, os dois pequenos. Nenhum flash de tela cheia.

### 2.3 Regras fixas

- Nenhuma marca, logo, escudo, time, celebridade, "Pix", bebida ou religião. Carros só nas nossas cartas e no símbolo do perfil, desenhados, genéricos e parados. Nada de direção perigosa.
- Nenhuma pessoa nem rosto: no lugar da cabeça, carinha emoji.
- Nada de loja, produto, preço, link, cupom ou QR code nos vídeos, nas capas e nas legendas.
- Nenhuma palavra proibida pelo plano ("prêmio", "sorteio", "concorra", "ganhe", "desafio", "comenta EU" etc.) nos textos de tela, legendas e comentários fixados. "Duvido" é permitido (desafio sem prêmio).
- Nenhum nome de modelo de IA nos arquivos.

### 2.4 `roteiros-videos.md`

- **Legendas:** 168, 153 e 178 caracteres, muito abaixo do limite do TikTok. 5 hashtags em cada, iguais ao plano. Os `.txt` são iguais ao texto do roteiro.
- **Comentários fixados:** 78, 92 e 92 caracteres (o plano pede até 150).
- **Datas iguais ao `PLANO-DE-VIDEOS.md`:** V1 ter 17/11, 18h (D1, aprovação prevista seg 16/11). V2 sáb 21/11, 15h (D5). V3 dom 29/11, 19h. Resumo dos comentários até qui 26/11 e V3 refeito até sex 27/11. D3 qui 19/11 e D7 seg 23/11. Nada em 27/11 nem em 03/12.
- **Configurações:** Todos podem ver; comentários, dueto e costura ligados; rótulo de IA desligado; conteúdo comercial desligado; som do arquivo. Iguais ao plano (2.3).
- **Teste de som do V2:** o plano marca "sim", mas só permite a partir do D7. O roteiro resolve: na data-alvo (D5) fica o nosso som. Está coerente.
- **Montador sem celular:** tudo é feito pelo TikTok Studio no navegador. Cada passo que pode não existir na web (Agendar, Editar capa → Carregar, Fixar, Repostar, Biblioteca Comercial) tem um plano B escrito.
- **Sem M-gravação do C09:** igual ao plano.

### 2.5 O script roda de novo e dá o mesmo resultado

- Antes da correção: rodei `render_videos.py --pasta <pasta de teste>`. Os 10 arquivos saíram com o mesmo md5 dos entregues.
- Depois da correção: rodei na pasta do efeito e numa pasta de teste ao mesmo tempo. Os 10 arquivos saíram iguais nas 2 rodadas (md5 abaixo). Cada vídeo leva uns 30 s.
- Testei `--resumo` (V3 com o card) e `--nome` no modo `--rapido`, fora do projeto. O card fica legível e dentro da zona segura. Com `--nome`, tudo troca junto.

| Arquivo | md5 |
|---|---|
| C09-V1.mp4 | d04e7fe9575761b200175762f7a5ac1b |
| C09-V2.mp4 | bfb008ceeeb5c7e49f1e23c8c1f030d3 |
| C09-V3.mp4 | 66088cdcecda9b06aed261263f03e910 |
| C09-V1-capa.jpg | b37995cb33e8b541c793d3868ae47684 |
| C09-V2-capa.jpg | 6b15d754a16a78ab18c0a0834aba2e2e |
| C09-V3-capa.jpg | 21546fa5b89933597d0877bdc1578e58 |
| previa-videos.png | abcaac6e2b292167d31dfd26545d52a0 |

---

## 3. Riscos que ficam

1. **Zona segura sem print do app.** Os valores (topo 220, base 420, direita 140) são os da biblioteca e não foram vistos na tela (a confirmar).
2. **Texto da lista é o menor do vídeo** (letra de uns 32 px num quadro de 1080). Fica legível em tamanho real, mas num celular pequeno pede atenção. O gancho, o nome do filtro e as falas são grandes.
3. **C09-V3 sem card.** O arquivo de agora é a versão "sem padrão claro". Sozinho, o gancho "Nos comentários é fácil 😏" é menos claro para quem não viu os outros posts. Se o Montador mandar um padrão até 26/11, a nuvem refaz com `--resumo` até 27/11. Se o resumo atrasar, vai este arquivo. Nunca inventar o resumo.
4. **Teste de som do V2:** fica o nosso som na data-alvo. Só a coordenação pode mudar isso (a confirmar).
5. **Onde estão os arquivos:** o plano pede `videos/prontos/<código>/` e capa em PNG. Aqui ficaram na pasta do efeito, com capa JPG de até 260 KB, como nos outros efeitos. A coordenação move.
6. **A confirmar no passo 0 do Montador:** Agendar, "Editar capa → Carregar", "Fixar" (vídeo e comentário), "Repostar" e Biblioteca Comercial pela web, na conta Pessoal.
7. **Data de aprovação:** o alvo é seg 16/11. Se mudar, valem as regras 4.1 e 4.5 do plano. Se o nome publicado sair diferente, rodar `python3 render_videos.py --nome "<nome publicado>"` no D0 e trocar o nome nos comentários fixados.
8. **Perfil:** o Vini autorizou trocar foto e nome do perfil. Os vídeos do C09 não mostram o nome do perfil. O cartão final usa `videos/perfil/simbolo_transparente.png`. Se esse arquivo mudar, rodar `python3 render_videos.py` de novo antes do D0 para o símbolo novo entrar nos vídeos.
9. **Capa do V1:** as cartas ficam em leque, e a BALIZA COM PLATEIA (com o marcador 1) fica meio coberta pela PNEU FURADO. É de propósito e o título grande é legível. Se a coordenação preferir, dá para afastar as cartas.
10. **Biblioteca `render.py`:** os defeitos do `ranking()` relatados pelo produtor (camada 0,35 s antes do som; fade do painel que não acontece) foram contornados no script, não consertados na biblioteca. Avisar quem cuida dela antes de outro efeito usar o `ranking()`.
