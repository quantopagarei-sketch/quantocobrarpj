# C09 Perrengue no volante: roteiros e postagem dos vídeos

Feito em 06/11/2026 pela nuvem (produção de vídeo do C09). **Revisado pela QA em 06/11** (vídeos refeitos; ver `revisao-qa-videos.md`).
Base: `videos/PLANO-DE-VIDEOS.md` (versão final, com a revisão do crítico): seções 2.2 a 2.5, 3 (C09), 4, 5 e 7. Textos das cartas: `../textos.md` e `../textos.json`.
**Vini, você não precisa fazer nada com este arquivo.** Quem usa é o Montador (posta) e a coordenação.

---

## Resumo

| Código | Tipo | Quem faz | Quando (alvo) | Arquivo | Duração | Tamanho |
|---|---|---|---|---|---|---|
| C09-V1 | N-video | Nuvem fez. Montador agenda ou posta | D1 do C09. Alvo **ter 17/11, 18h** | `C09-V1.mp4` | 14,0 s | 3,41 MB |
| C09-V2 | N-video | Nuvem fez. Montador agenda ou posta | D4 a D6. Alvo **sáb 21/11, 15h** | `C09-V2.mp4` | 14,0 s | 3,41 MB |
| C09-V3 | N-video | Montador manda o resumo dos comentários até **qui 26/11**. Nuvem refaz (se houver padrão) até **sex 27/11**. Montador posta | Alvo **dom 29/11, 19h** | `C09-V3.mp4` | 12,0 s | 2,95 MB |

- Todos os MP4: 1080x1920, 30 fps, H.264 (High, yuv420p), som AAC estéreo 44,1 kHz, de 12 a 14 s, até 3,6 MB. Conferidos com ffprobe. Nenhum aviso de zona segura.
- Pasta inteira: uns 11,4 milhões de bytes (limite 12 MB).
- Prévia de todos (6 quadros de cada, com a interface do TikTok em vermelho): `previa-videos.png`.
- **Arquivos de cada peça:** `<código>.mp4`, `<código>-capa.jpg` (capa 1080x1920) e `<código>-legenda.txt` (legenda + hashtags, pronta para colar).
- **O C09 não tem M-gravação** (plano, seção 3): a carta 7 QUEM NÃO DÁ SETA sempre cai sobre o rosto, e o R2 manda evitar essa carta em rosto de banco. Ver "Se a QA liberar a C09-M1", no fim.
- **O C09 não tem carrossel.** Nenhuma pasta `carrossel-XX/`.
- **C09-V3 já está pronto na versão "sem padrão claro"** (só o gancho, sem card). Se o resumo dos comentários trouxer um padrão claro, a nuvem refaz o arquivo com o card. Se não trouxer, posta este mesmo.

---

## Regras que valem para todas as peças

1. **Nunca postar antes da aprovação** do C09 (status "Active" no Effect House).
2. **Nome do filtro: Perrengue no volante.** É igual na tela, na legenda e no comentário. Se o nome publicado sair outro (ex.: "Ranking dos perrengues"), a nuvem refaz tudo no D0 (ver "Para a nuvem", no fim). A hashtag do efeito muda junto.
3. **"Ou no meu perfil"** só entra na legenda e no comentário **depois** que o Montador abrir o perfil numa janela anônima e vir a aba de efeitos com o filtro (passo 6b do plano). Até lá, só "procura na lupa".
4. **Configurações da postagem (TikTok Studio, no navegador):**
   - Quem pode ver: **Todos**.
   - Comentários: **ligados**. Dueto: **ligado**. Costura: **ligada**.
   - Rótulo "Conteúdo gerado por IA": **desligado**. É animação feita por código, com as nossas cartas, sem pessoa e sem cena realista.
   - "Divulgar conteúdo comercial" (conteúdo de marca): **desligado**.
   - Som: **o do arquivo** (o nosso som já está dentro do MP4).
5. **Capa:** Editar capa → Carregar → o arquivo `-capa.jpg` da peça. Se não houver "Carregar", escolher o **quadro de 0,5 s**. Ele foi feito para funcionar sozinho como capa: gancho grande, carta inteira e o painel de 1 a 10.
6. **Comentário fixado:** publicar logo depois do post e fixar. Se a web não tiver "Fixar", só publicar. Até 150 caracteres (os daqui têm de 78 a 92).
7. **Respostas** (sempre que o PC estiver ligado; meta: nas 2 primeiras horas; nunca mais de 24 h sem responder quem pergunta o nome). Sem link. Varie as frases, nunca a mesma em sequência.
   - "Qual o nome?" → "Perrengue no volante 🔎 Digita na lupa!" / "É o Perrengue no volante, tá na lupa 🔎"
   - "Não achei" → "Digita Perrengue no volante na lupa 🔎 e abre a parte de efeitos" (caminho exato no app: a confirmar)
   - "Onde compra?" → **"Te chamo no direct 😉"** (o produto só aparece na mensagem direta). Sem link, sem fixar, sem puxar o assunto.
   - Discordou do ranking → "Nos comentários é fácil, você já viu a lista toda 😏 No filtro é um de cada vez" / "Pneu furado sem estepe no 5?? Bah, tu é forte 😂" / "Faz o teu e me marca, quero ver se tu aguenta não gastar o 1 cedo 😂"
   - "Faltou um perrengue" → "Qual tu colocaria no 1?" (não prometer que o item entra no filtro)
   - **Nunca** "o meu deu…" ou "eu tirei…" (a conta não usou o filtro). **Nunca** "toca no nome do efeito" (os nossos vídeos não têm a etiqueta).
   - Na tela é sempre "você". Nas respostas pode usar "tu", "bah", "tchê", sem forçar.
8. **Comentários que pedem cuidado** (do `lancamento.md`, seção 4.4):
   - Racha, grau, celular dirigindo, bebida, fugir de blitz, radar, multa: **não responder**. Ocultar se incentiva direção perigosa.
   - Estereótipo ("mulher no volante", idoso, gente de tal estado): **não responder e ocultar**.
   - Política (buraco e prefeito, preço de combustível): não responder.
   - Marca ou modelo de carro: responder sem repetir a marca ("Esse aí já viu de tudo 😂").
   - Futebol e time: resposta neutra, sem citar clube.
   - "Não funciona", "a lista bugou", "repetiu item": pedir um detalhe e avisar a nuvem na hora. Os posts do C09 param até a resposta.
9. **Nunca** escrever: prêmio, sorteio, concorra, ganhe, desafio, "comenta EU", "sigo quem usar", "marca 5 amigos", "Pix", marca ou modelo de carro, nome de loja, link ou cupom. **Não citar o desafio em lugar nenhum** (o C09 pode estar vinculado a ele).
10. **Loja separada:** nenhuma peça do C09 fala de produto, preço ou loja.
11. **Horários:** no máximo 2 posts por dia na conta (loja conta), com 3 h ou mais entre eles. Nunca 2 peças do C09 no mesmo dia. Sem post de efeito em **sex 27/11** (Black Friday) e **qui 03/12**. Nada durante jogo grande (sáb 28/11 das 16h às 20h; qua 02/12 à noite; dom 06/12 durante a final).
12. **Agendar** (se o botão existir, até 10 dias à frente): toda segunda e quinta. Antes, conferir que o relógio do Windows está no horário de Brasília. Sem Agendar: postar na hora (PC ligado; janela das 15h às 21h). **Não** mudar a conta para Empresa.
13. **Se a aprovação sair em outra data:** valem as regras 4.1 e 4.5 do plano. O V1 sai sempre no D1, no horário nobre (18h de terça a quinta; 19h de sexta a segunda). As outras peças andam junto.

---

## C09-V1 · "Gastei o 1 cedo demais" · N-video · 14 s

- **Quem faz:** a nuvem já fez (prancha conferida). O Montador agenda ou posta, fixa o comentário e responde.
- **Arquivos:** `C09-V1.mp4` (14,0 s; 3.572.458 bytes = 3,41 MB) · `C09-V1-capa.jpg` · `C09-V1-legenda.txt`
- **Objetivo:** estreia. Mostrar a regra (você não vê o próximo) e o arrependimento.

**Quando postar**
- **Regra D1:** dia seguinte à aprovação do C09, no horário nobre.
- **Alvo:** **ter 17/11, 18h** (aprovação prevista seg 16/11; a confirmar). Agendar no D0.
- No D1 o V1 vira o fixado 2 do perfil ("o mais novo"; plano 5.1).

**Legenda pronta para colar** (igual ao `C09-V1-legenda.txt`):
```
Ranking às cegas: você não vê o próximo perrengue. Qual você punha em 1º? Filtro: Perrengue no volante 🔎

#perrenguenovolante #filtro #filtrotiktok #motorista #ranking
```
- **Hashtags (5):** #perrenguenovolante #filtro #filtrotiktok #motorista #ranking

**Capa:** `C09-V1-capa.jpg`, com o texto **"RANKING ÀS CEGAS: PERRENGUE NO VOLANTE"**, as cartas BALIZA COM PLATEIA (com o marcador 1) e PNEU FURADO SEM ESTEPE, e a carinha 😩. Sem "Carregar": **quadro de 0,5 s**.

**Comentário fixado** (78 caracteres):
> Nome do filtro: Perrengue no volante 🔎 Procura na lupa. Qual você punha em 1º?

Depois da conferência da aba de efeitos: "…Procura na lupa ou no meu perfil. Qual você punha em 1º?"

**Som:** assinatura do C09 (tic-tac de pisca-alerta + vush e pop a cada vaga), trilha nossa de 100 bpm, já no MP4. **Teste de som: não.** Nunca trocar o som do V1.

**O que aparece na tela**

| Tempo | Na tela | Som |
|---|---|---|
| 0,0–1,9 | Gancho "Ranking às cegas: *Perrengue no volante*" (nome exato do filtro, em amarelo). Painel de 1 a 10 (marcadores do efeito; "PIOR" no 1 e "DE BOA" no 10). Carta 1 BALIZA COM PLATEIA sobre a carinha 🤔. Dedo 👆 toca o 1 e a carta voa para a vaga 1. Balão "Certeza: isso é o pior 😤" | trilha 100 bpm, tic-tac do pisca-alerta, toque, vush + pop |
| 1,9–8,0 | Título do efeito no topo. Um item por segundo: 4 → vaga 5, 6 → 7, 5 → 9, 9 → 8, 3 → 4, 8 → 6 | vush + pop a cada vaga |
| 8,0–9,8 | Aparece a 2 PNEU FURADO SEM ESTEPE. Tremida. Carinha 😩. A vaga 1 pisca em vermelho. Balão "NÃO! Cadê o 1? 😩". Vai para a vaga 2 | "ih…" de decepção, tic-tac, vush + pop |
| 10,0–11,8 | 10 BATERIA ARRIADA → vaga 3; 7 QUEM NÃO DÁ SETA → vaga 10 | vush + pop |
| 12,0–14,0 | Lista completa na esquerda. CF: "Procura na lupa 🔎" + **Perrengue no volante** em amarelo (1 linha) + símbolo do perfil + "Qual você punha em 1º?" | vush, pop, tic-tac |

---

## C09-V2 · "O 1 só no último" · N-video · 14 s

- **Quem faz:** a nuvem já fez (prancha conferida). O Montador agenda ou posta, fixa o comentário e responde.
- **Arquivos:** `C09-V2.mp4` (14,0 s; 3.574.289 bytes = 3,41 MB) · `C09-V2-capa.jpg` · `C09-V2-legenda.txt`
- **Objetivo:** uma regra fácil de copiar ("duvido você aguentar"), sem prêmio.

**Quando postar**
- **Regra:** 2ª peça do efeito, entre o D4 e o D6.
- **Alvo:** **sáb 21/11, 15h** (D5). A final da Sul-Americana é às 19h30: não mexer no horário.

**Legenda pronta para colar** (igual ao `C09-V2-legenda.txt`):
```
Regra: o 1 só no último. Duvido você aguentar 😂 Filtro: Perrengue no volante 🔎 procura na lupa

#perrenguenovolante #filtrotiktok #ranking #carro #humor
```
- **Hashtags (5):** #perrenguenovolante #filtrotiktok #ranking #carro #humor

**Capa:** `C09-V2-capa.jpg`, com o texto **"REGRA: O 1 SÓ NO ÚLTIMO 🔒"**, a carta LAVAR O CARRO E CHOVER com o marcador 1 e a carinha 😅. Sem "Carregar": **quadro de 0,5 s**.

**Comentário fixado** (92 caracteres):
> O filtro é o Perrengue no volante 🔎 Procura na lupa. Aguenta deixar o 1 pro último? Duvido 😂

**Som:** assinatura do C09, trilha nossa de 104 bpm, já no MP4. **Teste de som: sim, com uma condição.** O plano só deixa testar som em alta **a partir do D7** do efeito. Na data-alvo (sáb 21/11 = D5) fica o nosso som. Se o V2 for postado no D7 ou depois, e se a Biblioteca de Música Comercial existir no upload pela web: o Montador escolhe uma faixa pelo print do Creative Center (Tendências → Músicas → Brasil) da segunda, em volume baixo, **por baixo** do nosso som. Se o site não deixar manter o som do arquivo junto, não troca. Nunca a biblioteca geral (a conta vende).

**O que aparece na tela**

| Tempo | Na tela | Som |
|---|---|---|
| 0,0–1,9 | Gancho "Regra: *o 1 só no último* 🔒". Vaga 1 com 🔒 piscando no ritmo (104 bpm). Carta 4 VAGA QUE PARECIA MAIOR sobre a 🤔. Dedo toca o 8 e ela voa para a vaga 8 | trilha, tic-tac, toque, vush + pop |
| 1,9–4,6 | Título no topo. 2 → vaga 3; 9 → 7; 6 → 5 | vush + pop |
| 4,6–6,3 | Aparece a 10 BATERIA ARRIADA. Carinha 😬. O 🔒 sacode. Balão "Ai… regra é regra". Vai para a vaga 2 | cadeado, "ih…", vush + pop |
| 6,4–9,9 | 3 → vaga 4; 8 → 6; 7 → 10; 1 → 9 | vush + pop |
| 10,0–11,9 | O 🔒 abre (🔓). A 5 LAVAR O CARRO E CHOVER cai no 1, com brilho. Carinha 😅. Balão "Oficialmente o *pior perrengue* da vida 🤷" | clique, vush + pop, plim |
| 12,0–14,0 | Lista completa. CF com "Duvido você aguentar" | vush, pop, tic-tac |

---

## C09-V3 · "Nos comentários é fácil" (card de resposta) · N-video · 12 s

- **Quem faz:** o Montador manda o resumo dos comentários; a nuvem refaz o vídeo se houver padrão claro; o Montador posta.
- **Arquivos:** `C09-V3.mp4` (12,0 s; 3.089.439 bytes = 2,95 MB) · `C09-V3-capa.jpg` · `C09-V3-legenda.txt`
- **Objetivo:** devolver a discussão dos comentários para o filtro.

**Tarefa do Montador: o resumo dos comentários (até qui 26/11)**
1. Ler os comentários dos posts do C09 (V1 e V2) no TikTok Studio.
2. Ver se existe um **padrão claro**: algo que **muita gente** escreveu. Exemplo: "a maioria pôs PNEU FURADO SEM ESTEPE no 1" ou "muita gente brigou por causa da BALIZA COM PLATEIA". Um comentário só não é padrão.
3. Escrever o padrão **em palavras suas**, numa frase curta (até umas 15 palavras). **Não copiar** o texto de ninguém. **Sem** nome, @, foto ou print de comentário.
4. Mandar para a nuvem junto com o resumo de quinta (26/11) e anotar em `C:\Users\Pichau\Desktop\Efeitos\metricas-videos.md`.
5. **Se não houver padrão claro**, escrever "sem padrão". Aí o vídeo que já está nesta pasta é o que vai ao ar. **Nunca inventar.**

**Tarefa da nuvem (até sex 27/11):** com padrão claro, reescrever o resumo em palavras nossas, sem nada que identifique alguém, e rodar
`python3 render_videos.py --so C09-V3 --resumo "<resumo>"`. Conferir a prancha. Mandar o arquivo novo para a coordenação. Sem padrão: nada muda.

**Quando postar**
- **Alvo:** **dom 29/11, 19h** (3ª peça, D8 em diante). Nada de post de efeito na sex 27/11 (Black Friday).

**Legenda pronta para colar** (igual ao `C09-V3-legenda.txt`):
```
Nos comentários é fácil, você já viu a lista. No filtro, não 😏 Filtro: Perrengue no volante 🔎 procura na lupa

#perrenguenovolante #filtrotiktok #ranking #vidademotorista #humor
```
- **Hashtags (5):** #perrenguenovolante #filtrotiktok #ranking #vidademotorista #humor

**Capa:** `C09-V3-capa.jpg`, com o texto **"NOS COMENTÁRIOS É FÁCIL 😏"**, a carta "?" (QUAL VEM?) e a carinha 🤔. Sem "Carregar": **quadro de 0,5 s**.

**Comentário fixado** (92 caracteres):
> Filtro: Perrengue no volante 🔎 Procura na lupa. Lá você não vê o próximo 😏 Qual foi o seu 1?

**Som:** assinatura do C09, trilha nossa de 100 bpm, já no MP4. **Teste de som: não.**

**O que aparece na tela**

| Tempo | Na tela | Som |
|---|---|---|
| 0,0–2,5 | Gancho "Nos comentários é fácil 😏". Painel de 1 a 10 vazio. Carta "?" (QUAL VEM?) sobre a 🤔. **Com padrão claro:** no meio da tela, o card branco "💬 O que mais apareceu nos comentários:" + o resumo em palavras nossas (a carta "?" entra aos 2,5 s) | trilha 100 bpm, tic-tac |
| 2,5–4,0 | "Você já viu a lista toda 😏". Carinha 😏 | pop |
| 4,0–9,9 | Título no topo. Ranking rápido: um item a cada 0,58 s sai da carta "?" e voa para a vaga. A carta "?" nunca mostra o próximo (e não troca de imagem: nada de pisca-pisca) | vush + pop a cada vaga |
| 10,0–12,0 | Lista completa. CF com "No filtro você não vê o próximo" | vush, pop, tic-tac |

---

## Se a QA liberar a C09-M1 (hoje: não existe)

O plano tirou a M-gravação do C09. Só entra se a QA liberar a carta 7 sobre rosto de banco, e aí num horário vago. Se isso acontecer, a nuvem manda o kit (gancho, cartão final, som, capa e legenda), como nos outros efeitos. Até lá, o Montador **não grava nada do C09**.
Se for liberada, o resumo é:
- **O que gravar:** o preview do Effect House com o C09 montado. "+ Add media" → o clipe → botão de gravar do próprio preview (9:16). Clicar nos números para montar o ranking. Se o preview não tiver botão de gravar (a confirmar), usar a gravação de tela do Windows 11 (Ferramenta de Captura, Win + Shift + R, a confirmar), só na área do preview, sem menus e sem o mouse.
- **Fonte de rosto:** só clipe de banco com licença (1º Pexels; 2º Mixkit "Free License"), com 1 pessoa adulta, de frente, parada, camiseta lisa e fundo neutro. **Nunca** os vídeos de amostra do Effect House. Anotar link, autor, data e print da licença na planilha ao lado do `relatorio-montagem.md`.
- **Duração:** de 10 a 12 s (o arquivo final, de 6 a 15 s).
- **Exportar:** Clipchamp, 1080p, MP4, com o kit por cima e o som do clipe desligado. Conferir: até 4 MB (Propriedades do arquivo). Se passar, exportar de novo em 720p. Sem Clipchamp, a peça sai do calendário.
- **Onde salvar:** `C:\Users\Pichau\Desktop\Efeitos\prontos\C09-M1\` (mesma regra das outras M; a confirmar).
- **Configurações:** rótulo de IA desligado (pessoa filmada de verdade); conteúdo comercial desligado.

---

## Depois de postar (vale para as 3 peças)

- **Medir** em 24 h e 72 h (plano, seção 6.1): views, tempo médio, % até o fim, curtidas, comentários, compartilhamentos, salvamentos, seguidores ganhos, de onde vieram as views e quantos comentários pedem o nome ou dizem "não achei". No Effect House: vídeos novos com o efeito por dia, do D0 ao D7.
- **D3 e D7 do C09** (alvo qui 19/11 e seg 23/11): a equipe decide o que muda (plano, seções 6.3 e 6.4).
- **Repostar quem usou** (plano, 5.6; só se a web tiver "Repostar", a confirmar no passo 0; se não tiver, fica só o comentário): a partir do D3, até 1 por dia, nos dias com 0 ou 1 post nosso. Só vídeo público, de pessoa que parece adulta, sem marca, time, carro reconhecível, bebida ou direção, e que não deixa a pessoa mal. Comentar até 10 por dia, frases curtas e diferentes ("baliza no 10?? tu é outro nível 😂"). Nada em troca.

---

## Para a nuvem

- **Rodar tudo de novo** (sai igual, byte a byte): `python3 render_videos.py` nesta pasta (uns 100 s).
- **Nome publicado diferente** (no D0): `python3 render_videos.py --nome "Ranking dos perrengues"`. A tela, a capa e a legenda mudam juntas, e a hashtag do efeito sai do nome (ex.: #rankingdosperrengues). Depois, trocar o nome também nos comentários fixados deste arquivo.
- **C09-V3 com o resumo:** `python3 render_videos.py --so C09-V3 --resumo "<resumo em palavras nossas>"` e depois `python3 render_videos.py --so previa`.
- **Pranchas rápidas** (sem MP4): `python3 render_videos.py --rapido <pasta fora do projeto>`.
- O script só importa `videos/lib/render.py` e só lê `../assets` e `../textos.json`. Nada lá é alterado.
