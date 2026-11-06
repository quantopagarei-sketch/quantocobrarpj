# C07 Simpatia da Virada: revisão de QA dos vídeos

Feita em 06/11/2026 pela nuvem (revisor de QA dos vídeos do C07).
**Vini, você não precisa fazer nada com este arquivo.** Ele é para a coordenação.

**Resultado: aprovado, nota 9 de 10.** Os 3 vídeos, as 3 capas, as legendas e o kit da M1 estão prontos para postar. Corrigi 1 erro de data no `roteiros-videos.md` (o prazo de agendar a V2 e a V3 não dava para cumprir) e 2 pontos pequenos. Nenhum vídeo precisou ser refeito.

---

## 1. O que eu conferi

### 1.1 Ficha técnica (ffprobe e ffmpeg)

| Arquivo | Tela | Quadros | Vídeo | Som | Duração | Tamanho | Volume médio / pico | LUFS / pico real |
|---|---|---|---|---|---|---|---|---|
| `C07-V1.mp4` | 1080x1920, 30 fps | 300 | H.264 High, yuv420p, BT.709 | AAC estéreo 44,1 kHz | 10,0 s | 2,49 MB | -18,8 / -2,0 dB | -17,5 / -2,0 dBTP |
| `C07-V2.mp4` | 1080x1920, 30 fps | 330 | igual | igual | 11,0 s | 2,63 MB | -18,8 / -2,3 dB | -17,3 / -2,3 dBTP |
| `C07-V3.mp4` | 1080x1920, 30 fps | 270 | igual | igual | 9,0 s | 2,39 MB | -19,8 / -1,7 dB | -17,5 / -1,7 dBTP |

- Todos entre 6 e 15 s, todos abaixo de 4 MB. Som presente e audível nos 3.
- Pasta inteira: 10,6 MB (com este arquivo). Limite: 12 MB. ✅
- Capas (`C07-V1-capa.jpg`, `C07-V2-capa.jpg`, `C07-V3-capa.jpg`, `kit-C07-M1/capa.jpg`): 1080x1920, até 263 KB.
- Kit da M1: `gancho.png` e `gancho-baixo.png` (1080x1920, transparentes), `final.png` (1080x1920), `assinatura.wav` (12,0 s, mono, 44,1 kHz, pico -1,5 dBFS, -18,6 LUFS). O toque aparece em 3,0 s e a assinatura em 9,5 s, como o roteiro diz.

### 1.2 Quadros abertos e olhados um por um

Tirei 15 quadros de cada vídeo (incluindo 0,0 s e o último quadro), com as faixas da interface do TikTok marcadas (topo 220 px, base 420 px, direita 140 px). Também olhei as 4 capas, o kit e a `previa-videos.png`. As pranchas ficaram no scratchpad da sessão (`qa-C07/V1-a.png` a `V3-c.png`, `capas.png`, `kit.png`, `detalhes-1.png`).

| Item | V1 | V2 | V3 |
|---|---|---|---|
| Gancho já no 1º quadro | ✅ "O filtro escolhe sua simpatia da virada" + carta 1 | ✅ "Não sabe qual simpatia fazer? 🤔" + 3 cartas | ✅ "Pausa e vê sua simpatia ⏸️" + título + "3" |
| Gancho com até 7 palavras | ✅ 7 | ✅ 5 | ✅ 5 |
| Textos legíveis, sem corte | ✅ | ✅ as 3 cartas do leque dão pra ler | ✅ "PAUSA AGORA" em 2 linhas grandes |
| Dentro da zona segura | ✅ (cartas até x 929; a borda é 940) | ✅ | ✅ |
| Acentos | ✅ É…, à, é | ✅ À MEIA-NOITE, ATÉ, você | ✅ vê, É… |
| Resultado da roleta | 14 VARRER O AZAR PRA FORA, parado de 6,8 a 8,2 s, e some até 8,5 s | 17 12 DESEJOS NUM PAPELZINHO, parado de 7,0 a 8,5 s | não tem roleta; 16 cartas, 0,35 s cada |
| Cartão final | ✅ 8,2–10 s | ✅ 8,5–11 s | ✅ 7–9 s |
| Nome no cartão final | ✅ **Simpatia da Virada**, igual ao `textos.md`, em amarelo, 1 linha | ✅ | ✅ |
| "Procura na lupa 🔎" | ✅ | ✅ | ✅ |
| Pergunta do cartão final | "Saiu, tem que cumprir 😅" | "Qual saiu pra você?" | "Grava cumprindo ✨" |

- **Capas:** o texto grande fica dentro do miolo 3:4 (y 240 a 1680) nas 4. Textos iguais aos do plano. O quadro de 0,5 s (capa reserva) funciona sozinho nos 3 vídeos.
- **Luz piscante:** medi a troca de brilho quadro a quadro. Não tem flash de tela cheia. A única queda grande de brilho é a entrada do cartão final (uma cortina de 0,3 s, uma vez só). No V3, as cartas trocam 2,86 vezes por segundo, abaixo do limite de 3 do plano. A roleta do V1 e do V2 começa rápida (como em todos os efeitos), mas as cartas têm o mesmo fundo roxo e o brilho da tela quase não muda.
- **Ordem das cartas do V3** no `roteiros-videos.md`: confere com a saída do script (1,40 s MOEDA… até 6,65 s LENTILHA…).

### 1.3 Regras fixas

- Nenhuma marca, logo, time, escudo, celebridade, "Pix", bebida, direção ou religião na tela, nas capas, nas legendas ou nos comentários. Sem mãos rezando. ✅
- Nada da loja, link, preço ou produto nos vídeos. ✅ As cartas 12 (roupa íntima) e 18 (carro limpinho) nunca aparecem nos vídeos N. ✅
- O único carro na tela é o símbolo do perfil no cartão final, que o plano (2.2) pede em todos os efeitos. Desenho genérico, sem marca. ✅
- Nada sobre desafio, prêmio ou sorteio em tela, legenda ou comentário. ✅
- Nenhum nome ou versão de modelo de IA nos arquivos. ✅

### 1.4 Legendas, hashtags e comentários

- As 4 legendas (V1, M1, V2, V3) são **iguais, letra por letra**, às do `PLANO-DE-VIDEOS.md`, seção 3 (conferido por script).
- Tamanho: de 178 a 185 caracteres com as hashtags. O limite do TikTok é muito maior. ✅
- 5 hashtags em cada uma (o plano pede até 5). ✅
- Comentários fixados: de 84 a 113 caracteres, todos abaixo de 150. Contagem do roteiro confere. ✅
- "Ou no meu perfil" só depois da conferência da aba de efeitos. ✅

### 1.5 Datas e instruções do Montador

- Datas iguais à tabela 4.4 do plano: V1 qui 10/12, 18h · M1 sáb 26/12, 15h · V2 ter 29/12, 19h · V3 qui 31/12, 11h (C05-V3 às 14h, 3 h depois). Dias da semana conferidos no calendário. ✅
- Nunca 2 peças do C07 no mesmo dia; nada depois das 15h em 31/12. ✅
- Configurações (Todos, comentários/dueto/costura ligados, rótulo de IA desligado, conteúdo comercial desligado, som do arquivo) iguais ao plano. ✅
- Tudo dá pra fazer **sem celular**: TikTok Studio no navegador, Effect House no PC, Clipchamp, janela anônima. ✅
- **Agendar da V2 e da V3: estava errado** (ver 2.1).

### 1.6 O script roda de novo e dá o mesmo resultado

- Rodei `render_videos.py --pasta <scratchpad>/qa-C07/run1` (71 s). **Os 16 arquivos saíram iguais byte a byte** (mesmo md5) aos da pasta: os 3 MP4, as capas, as legendas, o kit e a prévia.
- Nenhum aviso de zona segura. O volume e o pico do áudio saíram iguais aos do relatório do produtor.
- Testei `--rapido` com `--nome "Simpatia de Ano Novo" --troca 1=R4 --troca 5=R2`: o nome cabe numa linha, as reservas entram no lugar das cartas e a hashtag vira `#simpatiadeanonovo`.
- O script não altera a biblioteca (`videos/lib`) nem `../assets`.

---

## 2. O que eu corrigi

### 2.1 Datas de agendar da V2 e da V3 (`roteiros-videos.md`)

- **Problema:** o roteiro (copiado do plano) dizia "agenda **até** 19/12" (V2, post em 29/12) e "agenda **até** 22/12" (V3, post em 31/12). Mas o Agendar só aceita até **10 dias à frente**. Então 29/12, 19h, só aparece no Agendar a partir de sáb 19/12, 19h, e 31/12, 11h, a partir de seg 21/12, 11h. Do jeito que estava, o Montador tentaria agendar antes e não ia conseguir, ou ia achar que o prazo já tinha passado.
- **Correção:** V2 → agendar na **seg 21/12** (rotina de segunda; se não der, qui 24/12; último dia seg 28/12). V3 → agendar na **seg 21/12, depois das 11h** (se não der, qui 24/12; último dia qua 30/12). Mudei a tabela do resumo, as duas peças e a regra 10 (que agora explica: "agenda até [data]" no plano é o 1º dia possível, não o último).
- **M1:** acrescentei quando agendar (rotina de qui 17/12 ou seg 21/12, se já estiver pronta e conferida).

### 2.2 Gancho do V1 se o nome publicado mudar (`render_videos.py`)

- **Problema:** com `--nome "Simpatia de Ano Novo"`, o gancho continuava "O filtro escolhe sua **simpatia da virada**", com "simpatia da virada" em amarelo. Em amarelo, parece o nome do filtro, e a pessoa iria procurar o nome errado na lupa.
- **Correção:** com outro nome, o gancho vira "O filtro escolhe sua **simpatia** de Ano-Novo". Com o nome padrão, nada muda (re-renderizei o V1: mesmo md5 de antes). Anotei isso na parte "Para a nuvem" do roteiro.

### 2.3 Carro no cartão final (`roteiros-videos.md`, regra 11)

- A regra dizia "o C07 não fala da loja, nem de carro", mas o símbolo do perfil (um carro com a mira de câmera) aparece no cartão final. Acrescentei que esse é o único carro, igual em todos os efeitos, e que não é problema. Assim o Montador não trava na conferência.

### Não precisei mexer

Vídeos, capas, legendas, kit e prévia ficaram como o produtor entregou.

---

## 3. Riscos que continuam

1. **O mesmo erro de "agenda até" está no plano para outras peças** (C08-V3, C05-V2, C05-V3, C06-V2, C06-V3 e a C07 da tarefa do produtor: "schedule by 19/12"). Se o `PRONTO-PARA-MONTAR.md` copiar essas datas, o Montador vai tentar agendar cedo demais. A coordenação precisa trocar "até" por "a partir de" (ou pela data da rotina de segunda e quinta). A regra dos 10 dias ainda é (a confirmar) para conta Pessoal; algumas contas veem 30 dias.
2. **Começo rápido da roleta (V1 e V2):** cerca de 11 trocas por segundo no primeiro segundo, como em todos os efeitos. O limite de 3 por segundo do plano vale para o trecho "pausa" (cumprido no V3). Se algum post do C07 receber o aviso de luz piscante (a confirmar), a nuvem desacelera o começo da roleta.
3. **Cartas 1 (7 ondas) e 5 (tudo branco)** vêm de tradição religiosa, hoje costume popular. A 1 está no gancho e na capa do V1; a 5, no leque do V2. Risco baixo. Se o efeito for publicado com reserva: `--troca 1=R4 --troca 5=R2`.
4. **Cartas 14 e 17** (resultados do V1 e do V2) não têm reserva. Se uma delas sair do efeito, a reação na tela ("Ordem é ordem 🧹", "Essa dá pra cumprir ✍️") precisa ser refeita à mão.
5. **Desafio termina por volta de 27/12** (a confirmar). V2 (29/12) e V3 (31/12) saem depois. Não muda nenhum texto: o desafio nunca é citado.
6. **M1 depende de coisas que a nuvem não vê:** botão de gravar no preview, Win+Shift+R, Clipchamp no PC, se o clipe no preview altera o projeto salvo, e se as regras do desafio pedem autorização por escrito de quem aparece no clipe (tudo a confirmar).
7. **`assinatura.wav`** sai com pico de -1,5 dBFS. Depois de exportado no Clipchamp, o pico pode subir um pouco. Risco baixo: o TikTok ajusta o volume.
8. **Foto do perfil:** o cartão final usa `videos/perfil/simbolo_transparente.png`. Se a equipe trocar a foto do perfil, basta rodar `python3 render_videos.py` de novo para os vídeos acompanharem.
9. **Hashtag com outro nome:** com `--nome`, a 1ª hashtag sai do nome (ex.: `#simpatiadeanonovo`). A coordenação confirma se é essa.
10. Agendar, "Editar capa → Carregar", "Fixar" comentário e a Biblioteca de Música Comercial pela web continuam (a confirmar) na conta Pessoal.
