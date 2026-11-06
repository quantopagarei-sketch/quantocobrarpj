# Guia de montagem: "Perrengue no volante" (C09)

**Para quem é:** para o Montador, o Claude que opera o PC do Vini. Também serve para qualquer pessoa que já tenha montado o C08 ou o C01.
**Versão do guia:** 1.1 · 06/11/2026 (revisada pelo QA) · escrito para o Effect House **5.16** no Windows, a versão que o Montador encontrou no PC.
**Envio:** até **terça, 17/11/2026**.
**Tempo total:** cerca de **4 h**. Reserve 5 h, porque o template é novo para a equipe.

> **Vini, se você estiver lendo:** não precisa fazer nada aqui. Você só será chamado no caso da seção 0.7, sempre com o link direto.

### Como ler as marcas

- **(a confirmar na sua versão)**: a equipe não conseguiu ver essa tela, porque o site do Effect House não abre de onde pesquisamos. Se o botão, o objeto ou o campo tiver outro nome, use o parecido e **anote no relatório** o nome real.
- Os nomes de botões, painéis e propriedades estão **em inglês e em negrito**, como aparecem no programa.
- "Clique" é com o botão esquerdo. Quando for o direito, o passo diz "clique com o botão direito".
- **Você já montou o C08 e o C01.** Quando este guia diz "como no C01", vale o que você fez de verdade e anotou no `relatorio-montagem.md`, mesmo que seja diferente do guia do C01.

### O que vamos montar (resumo)

1. No topo da tela aparece o título **"RANKING DOS / PERRENGUES / DO VOLANTE"**, com a pílula **"1 = PIOR · 10 = DE BOA"**. Na lateral da tela fica uma lista numerada de **1 a 10**.
2. Em cima da cabeça, as cartas giram e param num perrengue, por exemplo **"BALIZA COM / PLATEIA"**.
3. A pessoa toca no número da lista onde quer pôr aquele perrengue, **sem saber qual vem depois**. O perrengue vai para o lado do número e o próximo aparece em cima da cabeça.
4. Quando os 10 estão no lugar, o ranking fica pronto na tela. A graça é gastar o 1 cedo e depois vir um pior ainda.

**Este efeito NÃO reaproveita o projeto do C01.** A base é outro template pronto, o **Blind Rank** (Templates → aba **Interactive**). Ele já traz toda a lógica do ranking às cegas com comidas de exemplo. Você troca as comidas pelos 10 perrengues, põe o título e ajusta alguns valores. **Não é preciso programar.** O efeito é para **1 pessoa** (1 rosto).

**A diferença mais importante em relação ao C01:** aqui as cartas entram como **10 imagens soltas**, e **não** como Texture Sequence.

---

## Parte 0: Antes de começar

### 0.1 Pré-requisitos (confira todos)

| # | Pré-requisito | Como conferir |
|---|---|---|
| 1 | O C09 está liberado na tabela da seção 2 do `PRONTO-PARA-MONTAR.md` | Abra https://raw.githubusercontent.com/quantopagarei-sketch/quantocobrarpj/main/tiktok-efeitos/PRONTO-PARA-MONTAR.md. Se o C09 ainda estiver só em "Vem aí", **não comece**. |
| 2 | O Effect House está logado na conta **Car Shop** | Tela inicial, como no C01 |
| 3 | Você sabe o nome exato do template de ranking nesta versão | `reconhecimento.md`, item 2 (a equipe pediu para anotar "Blind Rank") |
| 4 | Você sabe se o **Effect House AI** funciona nesta conta | `reconhecimento.md`, item 3. Só importa se algo travar. |
| 5 | Você sabe gravar a tela do Preview e usar o **Create icon** | Você fez isso no C08 e no C01. Anotações no relatório. |
| 6 | O ffmpeg está instalado | `ffmpeg -version` no PowerShell. Se não estiver: `winget install --id Gyan.FFmpeg -e` e abra outro PowerShell. |

### 0.2 Links

| O quê | Link direto | Quem usa |
|---|---|---|
| Arquivos da equipe (zip com tudo) | https://github.com/quantopagarei-sketch/quantocobrarpj/archive/refs/heads/main.zip | Montador |
| Ordens da equipe (atualizadas todo dia) | https://raw.githubusercontent.com/quantopagarei-sketch/quantocobrarpj/main/tiktok-efeitos/PRONTO-PARA-MONTAR.md | Montador |
| Tutorial oficial do template Blind Rank (em inglês) | https://effecthouse.tiktok.com/learn/guides/tutorials/template-tutorials/blind-rank | Consulta |
| Outra cópia do mesmo tutorial | https://effecthouse.tiktok.com/learn/library/template-tutorials/blind-rank | Consulta |
| Relato no fórum: mais de 10 imagens bugam a lista | https://community.effecthouse.com/t/help-with-blind-rank-template/60530 | Consulta |
| Guia oficial de envio | https://effecthouse.tiktok.com/learn/guides/publishing/publish/submit-your-effect | Consulta |
| Guia oficial do ícone (Create icon) | https://effecthouse.tiktok.com/learn/guides/publishing/effect-icon-creation | Consulta |
| Nó de toque numa imagem (só no Plano B3) | https://effecthouse.tiktok.com/learn/guides/editor-panels/visual-scripting/nodes/utility/screen-image-tap | Consulta |
| Busca de marcas do INPI (Parte 12.2) | https://busca.inpi.gov.br/pePI/ | Montador |

### 0.3 Pastas (vale para o guia inteiro)

Neste guia, **`<BASE>`** é a pasta "Efeitos" que você usa no PC. Pela última ordem da equipe, ela é `C:\Users\Pichau\Desktop\Efeitos`. Se essa pasta não existir, a pasta é `Documentos\Efeitos`.

| Apelido | Caminho |
|---|---|
| `<BASE>` | `C:\Users\Pichau\Desktop\Efeitos` (ou `Documentos\Efeitos`) |
| `<A>` (imagens do C09) | `<BASE>\tiktok-efeitos\efeito-5-perrengue-no-volante\assets` |
| Projeto | `<BASE>\projetos\C09-perrengue-no-volante` |
| Vídeo demo | `<BASE>\videos-demo\C09-demo.mp4` |
| Prints | `<BASE>\prints\C09-*.png` |
| Relatório | `<BASE>\relatorio-montagem.md`, nova seção "C09" |

### 0.4 Baixar e conferir os arquivos

1. Baixe o zip (link da 0.2) e extraia **só a pasta `tiktok-efeitos`** em `<BASE>`, por cima da antiga.
2. Rode no PowerShell:

```powershell
$BASE = if (Test-Path "C:\Users\Pichau\Desktop\Efeitos") { "C:\Users\Pichau\Desktop\Efeitos" } else { Join-Path ([Environment]::GetFolderPath('MyDocuments')) "Efeitos" }
$A = "$BASE\tiktok-efeitos\efeito-5-perrengue-no-volante\assets"
(Get-ChildItem "$A\cartas\carta_*.png").Count                  # tem que dar 10
(Get-ChildItem "$A\cartas\*").Count                            # tem que dar 10 (a pasta só pode ter as cartas)
(Get-ChildItem "$A\largo_512x256\cartas\carta_*.png").Count    # tem que dar 10
(Get-ChildItem "$A\extras\carta_*.png").Count                  # tem que dar 4
(Get-ChildItem "$A\reservas\reserva_*.png").Count              # tem que dar 4
(Get-ChildItem "$A\marcadores\posicao_*.png").Count            # tem que dar 10
(Get-ChildItem "$A\interface\*.png").Count                     # tem que dar 4
Get-ChildItem "$A\titulo.png","$A\titulo_5_posicoes.png","$A\titulo_curto.png","$A\largo_512x256\titulo.png","$A\icone_162.png","$A\icone_alt_162.png" | Select FullName, Length
(Get-ChildItem "$A" -Recurse -Filter *.png | Where-Object Name -ne 'previa.png' | Measure-Object Length -Maximum).Maximum   # menor que 1048576 (1 MB); o esperado é ~149000
```

> **Em todo PowerShell novo**, rode antes a primeira linha acima (a que define `$BASE`). Os comandos das outras partes dependem dela.

3. Se faltar arquivo, baixe o zip de novo. Se continuar faltando, avise a nuvem. Não chame o Vini por isso.

### 0.5 O que entra no efeito e o que não entra

Todos os arquivos ficam dentro de `<A>`. Existem **duas versões das mesmas peças**: a quadrada (512×512, na raiz de `assets` e em `cartas\`) e a larga (512×256, em `largo_512x256\`). A Parte 2 diz qual usar. **Nunca importe as duas versões das cartas no mesmo projeto**: os nomes dos arquivos são iguais.

| Arquivo | Entra? | Para quê |
|---|---|---|
| `cartas\carta_01.png` … `carta_10.png` (512×512) **ou** `largo_512x256\cartas\carta_01.png` … `carta_10.png` (512×256) | **Sim, uma das duas versões** | Os 10 perrengues. Entram como **10 imagens soltas** na propriedade **Randomizer: Textures**. |
| `titulo.png` (512×512) **ou** `largo_512x256\titulo.png` (512×256) | **Sim, um dos dois** | Título com "1 = PIOR · 10 = DE BOA" (Parte 5.1). |
| `titulo_5_posicoes.png` | Só se o template tiver 5 posições | Título com "1 = PIOR · 5 = DE BOA" (Parte 4.4). Existe nas duas versões. |
| `titulo_curto.png` | Só se o template tiver outra quantidade de posições (nem 10, nem 5) | Título com "1 = PIOR" (Parte 4.4). Existe nas duas versões. |
| `titulo_sem_subtitulo.png` | Não, salvo exceção | Só as 3 linhas, sem a pílula. Use só se a lista ficar com "PIOR" e "DE BOA" ao lado dos números (fim da Parte 5.3). Existe nas duas versões. |
| `marcadores\posicao_01.png` … `posicao_10.png` (256×256) | Só no caso da Parte 5.2 | Números 1 a 10 no estilo do efeito, no lugar dos números do template. |
| `interface\etiqueta_toque.png`, `jogar_de_novo.png`, `rotulo_pior.png`, `rotulo_de_boa.png` | Só no caso da Parte 5.3 | Textos em português no lugar de textos em inglês do template. |
| `extras\carta_11.png` … `carta_14.png` | Só na versão com rodízio (Parte 9, opcional) | 4 perrengues a mais. |
| `reservas\reserva_01.png` … `reserva_04.png` | Não | Só se um item for vetado (Parte 17). |
| `icone_162.png`, `icone_alt_162.png` | Só no plano de exceção da Parte 13.2 | Pela ordem de 06/11, o ícone sai do **Create icon**. |
| `icone_512.png`, `icone_alt_512.png`, `previa.png`, `gerar.py`, `lista-de-arquivos.txt` | Não | Referência da equipe. |

**Peso:** as 10 cartas quadradas + `titulo.png` somam **1,30 MB** em PNG. Na versão larga, **0,93 MB**. A maior imagem é a `cartas\carta_08.png`, com 146 KB.

**Réguas contra imagem esticada:**
- nas cartas, as **rodas dos carros** (cartas 01 e 03 a 09) e o **pneu** da carta 02 têm que ficar **redondos**;
- no título, o **volante** dentro da placa amarela em losango tem que ficar **redondo**, e o losango, com os 4 lados iguais.

Se virar ovo, a imagem está esticada.

**Como é o visual:** placa de trânsito. Cada carta tem uma "janela" com a cena desenhada em cima e o texto em 2 linhas embaixo, numa moldura amarela, laranja, grafite ou verde-limão. A `previa.png` mostra uma simulação **aproximada** de como deve ficar na tela (lista à esquerda, título no topo).

### 0.6 Os 10 perrengues (para conferir)

| Nº | Arquivo | Texto | Cor da moldura |
|---:|---|---|---|
| 1 | carta_01 | BALIZA COM / PLATEIA | amarela |
| 2 | carta_02 | PNEU FURADO / SEM ESTEPE | laranja |
| 3 | carta_03 | POÇA QUE / ERA CRATERA | grafite |
| 4 | carta_04 | VAGA QUE / PARECIA MAIOR | verde-limão |
| 5 | carta_05 | LAVAR O CARRO / E CHOVER | amarela |
| 6 | carta_06 | BARULHINHO / NOVO NO CARRO | laranja |
| 7 | carta_07 | QUEM NÃO / DÁ SETA | grafite |
| 8 | carta_08 | SUBIDA COM / FILA ATRÁS | verde-limão |
| 9 | carta_09 | ESQUECER ONDE / ESTACIONOU | amarela |
| 10 | carta_10 | BATERIA / ARRIADA | laranja |

Extras (só no rodízio): 11 CARONA QUE / DÁ PITACO (grafite) · 12 ALARME QUE / DISPARA À TOA (verde) · 13 GPS / RECALCULANDO (amarela) · 14 TRANCAR A / CHAVE DENTRO (laranja).
Reservas (só se vetarem um item): R1 VOLANTE / PELANDO · R2 LIMPADOR QUE / SÓ ESPALHA · R3 RESERVA ACESA / NA ESTRADA · R4 GARAGEM / BLOQUEADA.

As cartas de **letra menor** (texto mais comprido) são a 09 (51 px), a 06 (52 px), a 04 e a 05 (54 px). São elas que você confere na leitura (Parte 8). **Na versão larga (512×256)** as de letra menor são outras: a **03** e a **07** (46 px, letra amarela na moldura grafite); as demais ficam com 52 px.

### 0.7 O que depende do Vini (o mínimo)

Nada, se tudo correr bem. Ele só é chamado se **o login do Effect House cair** ou se o programa estiver em outra conta. Mande para ele:

> Abra o Effect House no computador. Vai aparecer um QR code. No celular, abra o **TikTok da conta Car Shop** → **Perfil** → ícone de pessoa (**Adicionar amigos**) → ícone de scanner no canto de cima → aponte para o QR → toque em **Confirmar**. Guia com imagens: https://effecthouse.tiktok.com/learn/guides/getting-started/introduction-to-effect-house/download-and-login
>
> Tem que ser o scanner **de dentro do TikTok**. A câmera comum do celular não funciona.

O teste no celular é **opcional** e fica de fora deste guia. Se a equipe quiser fazê-lo, junta com outros efeitos num momento só, como na Parte 10 do guia do C01.

### 0.8 Tempo estimado

| Etapa | Tempo |
|---|---|
| Parte 0: baixar e conferir | 10 min |
| Partes 1 e 2: abrir o template e reconhecer as peças | 25 min |
| Partes 3 e 4: importar e trocar os itens | 25 min |
| Parte 5: título e textos | 25 min |
| Partes 6 e 7: lógica, posição e tamanho | 30 min |
| Parte 8: testar no PC | 40 min |
| Parte 9: rodízio (opcional) | 20 min |
| Partes 10 e 11: tamanho, desempenho e vídeo demo | 35 min |
| Partes 12 a 14: conferências, ícone, envio e status | 25 min |
| **Total** | **≈ 4 h** (reserve 5 h) |

---

## Parte 1: Abrir o template

1. Abra o **Effect House**.
2. Confira a conta **Car Shop**, como no C01. Se for outra conta, **pare** e siga a seção 0.7.
3. Na tela inicial, clique em **Templates**.
4. Clique na aba (ou filtro) **Interactive**.
5. Digite `Blind Rank` na busca.
6. Clique no card **Blind Rank**.
7. Clique em **Create** ou **Open** (o mesmo botão que você usou no C08 e no C01).
8. Espere o projeto carregar. O programa pode baixar o template, o que leva até 1 minuto.

**Se não achar "Blind Rank":** busque `Blind`, `Rank` e `Ranking`; olhe também nas abas **Game** e **Screen**. Se achar um template de ranking às cegas com outro nome, use-o (Parte 18, Plano B1). Se não houver nenhum, vá para a Parte 18, Plano B2.

9. Clique em **File → Save As**.
10. Vá até `<BASE>\projetos\`.
11. Dê o nome **`C09-perrengue-no-volante`**.
12. Clique em **Salvar**.
13. Confira na **barra de título** da janela se aparece `C09-perrengue-no-volante`.

> A partir daqui, aperte **Ctrl+S** ao fim de cada parte, sempre conferindo a barra de título.

---

## Parte 2: Reconhecer as peças do template

**Não mude nada nesta parte.** Só olhe e anote no relatório, na seção do C09. As decisões das partes seguintes dependem destas anotações.

### 2.1 Hierarchy

Pelo tutorial oficial, o template tem dois grupos principais (a confirmar na sua versão):
- **General**, com um **Head Tracker**: é o objeto que mostra, em cima da cabeça, o item que está girando;
- **2D Foreground**, com uma **2D Camera**: desenha a lista de 1 a 10 na tela.

O tutorial cita também um grupo **Tip**, com dicas para quem edita.

1. Abra cada grupo na **Hierarchy** (clique na setinha ao lado do nome).
2. Anote os nomes dos objetos que aparecem dentro de cada um.
3. Veja se existe algum objeto de **título** ou **cabeçalho** (nomes como `Title`, `Header`, `Logo`, `Banner` ou uma imagem com texto no topo da tela). Anote: **tem título** ou **não tem título**.
4. Veja o que há dentro de **Tip**. Anote se ele aparece no **Preview** (algum texto ou imagem de dica na tela).

### 2.2 Preview

1. Olhe o **Preview** com o primeiro rosto de exemplo.
2. Conte as posições da lista. Anote: **10**, **5** ou outro número.
3. Anote em que lado da tela a lista fica e em que altura começa e termina (ex.: "esquerda, de 20% a 85% da altura").
4. Anote **todo texto em inglês** que aparecer na tela (ex.: "Tap to rank", "Restart", "Best", "Worst").
5. Veja se os números da lista parecem **imagens** (com sombra, moldura ou fundo colorido) ou **texto simples**.

### 2.3 As imagens originais (comidas)

1. No painel **Assets**, ache as imagens de comida (podem estar numa pasta como `Textures`, `Food` ou `Images`).
2. Conte quantas são. Anote.
3. Clique na primeira. No **Inspector**, anote a **resolução** (largura × altura).
4. Calcule a proporção: **largura ÷ altura**. Exemplos: 512×512 dá 1; 512×256 dá 2; 512×384 dá 1,33.
5. Se os números da lista parecerem imagens (2.2, passo 5), procure-os no Assets também. Anote se são **10 imagens separadas** (uma por número) ou outra coisa.

### 2.4 Visual Scripting

1. Abra o painel **Visual Scripting**.
2. Ache a caixa grande do ranking. É um **subgraph** com várias propriedades. As propriedades podem aparecer na própria caixa ou no **Inspector** quando você clica nela (a confirmar na sua versão).
3. Anote o nome e o valor de **cada** propriedade. Pelo tutorial oficial, devem existir (a confirmar na sua versão):
   - **Randomizer: Textures**: a lista com as miniaturas das comidas;
   - **Randomizer: Wait Between Frames**: a velocidade da troca de imagens durante o giro;
   - **Randomizer: Shuffle Time** (mínimo e máximo): quanto tempo o item gira antes de parar;
   - **Randomizer: Tap To Stop Randomizer** (no tutorial aparece escrito "Tap To Shop", que é erro de digitação): se a pessoa precisa tocar para parar o giro;
   - **Layout: Space Between Each**: o espaço entre as linhas da lista;
   - **Layout: Objects Scale**: o tamanho das imagens na lista;
   - **Extra:** uma opção que põe sozinho o último item na última posição livre (o nome exato não foi confirmado);
   - **Extra: Hide Randomizer On Finish**: esconde o item de cima da cabeça ao terminar.
4. Procure também uma propriedade de **quantidade** de posições ou itens, e uma de **modo** (Loop, Random ou Shuffle). Anote se existem.
5. Procure um nó de evento de gravação (**Video Record Start**, **Record Start** ou a opção **Reset on Record**). Anote se existe. **Não crie** se não existir.

### 2.5 Jogar uma rodada com as comidas

Isso mostra como o template funciona antes de qualquer troca.

1. Clique **dentro** da imagem do Preview, num número da lista, quando o item de cima da cabeça parar.
2. Jogue até o fim. Anote:
   - se o item **para sozinho** ou se é preciso **tocar para parar**;
   - se o toque precisa ser **no número** ou se vale em qualquer lugar;
   - o que acontece quando você toca num número **já usado**;
   - se o **último** item vai sozinho para a última posição;
   - o que fica na tela no fim, e se o item de cima da cabeça some;
   - o que acontece se você clicar de novo depois do fim (nada, recomeça ou outra coisa).
3. Para recomeçar, use o botão de **reset/refresh** do Preview (a confirmar na sua versão) ou troque de rosto de exemplo e volte.

### 2.6 Decisão: versão quadrada ou larga

Use a proporção das comidas originais (2.3, passo 4):

| Proporção das comidas (largura ÷ altura) | Versão a usar no C09 | Pasta das cartas |
|---|---|---|
| menor que **1** (mais altas que largas) | **Quadrada (512×512)** | `<A>\cartas\` (e confira a régua na Parte 7.1) |
| de **1** até **1,4** (quadradas ou quase) | **Quadrada (512×512)** | `<A>\cartas\` |
| maior que **1,4** (mais largas que altas) | **Larga (512×256)** | `<A>\largo_512x256\cartas\` |

Anote a versão escolhida. **Ela vale para as cartas e, se o template tiver título próprio, para o título também.**

---

## Parte 3: Importar as imagens

### 3.1 As 10 cartas (imagens soltas)

1. No painel **Assets**, clique em **+** (**Add**) → **Import** → **From Computer** (o mesmo caminho do título no C01).
2. Abra a pasta da versão escolhida na 2.6: `<A>\cartas\` ou `<A>\largo_512x256\cartas\`.
3. Aperte **Ctrl+A** para selecionar os 10 PNG.
4. Clique em **Abrir**.
5. Confira se apareceram **10 imagens separadas** no Assets: `carta_01` … `carta_10`.

> **Não use Import → Texture Sequence aqui.** No Blind Rank, cada item é uma imagem solta. (A sequência só aparece no Plano B3.)

### 3.2 O título

Escolha o arquivo pela tabela:

| Caso (anotado na Parte 2) | Arquivo |
|---|---|
| O template **não tem** título (o título vai numa imagem nova no topo da tela) e a lista tem **10** posições | `<A>\largo_512x256\titulo.png` (sempre a larga: ocupa menos altura) |
| O template **tem** título e a lista tem **10** posições | `titulo.png` da versão escolhida na 2.6 (`<A>\titulo.png` ou `<A>\largo_512x256\titulo.png`) |
| A lista tem **5** posições | o mesmo raciocínio, com `titulo_5_posicoes.png` |
| A lista tem outra quantidade | o mesmo raciocínio, com `titulo_curto.png` ("1 = PIOR") |

1. **+** (**Add**) → **Import** → **From Computer**.
2. Selecione o arquivo da tabela e clique em **Abrir**.
3. Clique com o botão direito no asset novo → **Rename** → digite **`perrengue_titulo`**.

### 3.3 Números e textos (só se forem usados)

- **Números:** só se a Parte 2 mostrou que os números da lista são **10 imagens separadas**. Importe `<A>\marcadores\` com **Ctrl+A** (10 arquivos `posicao_01` … `posicao_10`).
- **Textos de interface:** só se a Parte 2 achou texto em inglês **feito de imagem**. Importe só os arquivos de `<A>\interface\` que forem usados (tabela da Parte 5.3).

### 3.4 Compressão

1. Clique em `carta_01` no Assets.
2. No **Inspector**, deixe a compressão em **Automatic** (512 px) ou **Manual → 512 → High**, como no C01.
3. Faça o mesmo nas outras 9 cartas e em `perrengue_titulo`. Se o Assets deixar selecionar várias com **Ctrl** e mudar todas juntas, faça assim (a confirmar na sua versão).
4. Números (`posicao_*`), se importados: **Manual → 256 → High** ou **Automatic**.

> **Não** use Medium nem Low agora. Isso só entra se o pacote passar do limite (Parte 10).

---

## Parte 4: Trocar as comidas pelos perrengues

### 4.1 Randomizer: Textures

O tutorial oficial manda trocar as imagens **arrastando do painel Assets para a miniatura no Visual Scripting**.

1. Abra o painel **Visual Scripting** e clique na caixa do ranking.
2. Ache a lista **Randomizer: Textures**, com as miniaturas das comidas.
3. Arraste `carta_01` do painel **Assets** e solte **em cima da 1ª miniatura** de comida.
4. Arraste `carta_02` para a 2ª miniatura, `carta_03` para a 3ª, e assim até `carta_10` na 10ª.
5. Se arrastar não funcionar: clique no campo do elemento e escolha a carta na lista que abrir (a confirmar na sua versão).

### 4.2 Exatamente 10 itens

**Regra:** a lista **Randomizer: Textures** tem que ter **exatamente 10** elementos, um para cada carta. Um usuário do fórum contou que, com mais de 10 imagens, o jogo passou da 10ª escolha e a lista de números bugou.

1. Conte os elementos da lista.
2. **Se houver mais de 10:** apague os que sobraram. Clique com o botão direito no elemento → **Remove** / **Delete**, ou use o botão **−** da lista (a confirmar na sua versão).
3. **Se houver menos de 10:** use o botão **+** da lista para criar os que faltam e ponha neles as cartas que faltaram.
4. Confira de novo: **10 elementos**, de `carta_01` a `carta_10`, **sem comida** e **sem carta repetida**.
5. Se existir a propriedade de **quantidade** de posições ou itens (Parte 2.4, passo 4), ponha **10**.
6. Aperte **Ctrl+S**.

### 4.3 Apagar as comidas

1. No painel **Assets**, clique com o botão direito numa imagem de comida → **Delete**.
2. **Se o programa avisar que o asset ainda está em uso, clique em Cancelar.** Algum lugar ainda aponta para ela. Procure:
   1. a lista **Randomizer: Textures** (sobrou uma comida?);
   2. o grupo **Tip** (pode usar uma comida como exemplo);
   3. algum objeto da **Hierarchy** com componente **Image** ou **Sprite** que mostre uma comida.
   Se for no **Tip**, deixe a comida lá e trate na Parte 5.3. Nos outros casos, troque pela carta certa e tente apagar de novo.
3. Repita para todas as comidas.
4. Apague **só** imagens de comida. Se aparecer outra imagem que você não reconhece (moldura, número, fundo), deixe como está e anote.
5. Aperte **Ctrl+S**.

### 4.4 Se a lista não tiver 10 posições

A pesquisa indica **10 posições**. Siga esta parte **só** se a Parte 2 contou outro número e não existe propriedade de quantidade (ou ela não aceitou 10).

**Lista com 5 posições:**
1. Deixe em **Randomizer: Textures** só **5 cartas**: `carta_01`, `carta_02`, `carta_07`, `carta_09` e `carta_10` (mistura de perrengue grande e pequeno). Mesma regra da Parte 4.2: **quantidade de cartas = quantidade de posições**. (Não envie com 10 cartas e 5 posições: pelos relatos do fórum, mais imagens que posições pode bugar a lista ou se comportar diferente no efeito publicado.)
2. Jogue **3 rodadas** no Preview. **Passou** se, nas 3 rodadas, o jogo **parou depois da 5ª escolha**, a lista não bugou e a ordem mudou entre as rodadas.
3. Se não passou, anote o que aconteceu e avise a nuvem antes de enviar.
4. Nos dois casos, o título é o `titulo_5_posicoes.png` (Parte 3.2).
5. Se o **Effect House AI** funcionar nesta conta, pode tentar o **Pedido 4** de `script\prompt-effect-house-ai.md`, com `[N]` = 10 e `[P]` = 5. Antes, salve uma cópia de segurança (`Copy-Item -Recurse -Force "$BASE\projetos\C09-perrengue-no-volante*" "$BASE\projetos\backup\"`). Use o resultado só se passar no teste do passo 2 **e** se a nuvem aprovar (mesmo risco do rodízio, Parte 9, passo 7); se não, restaure a cópia.
6. Anote no relatório e avise a nuvem.

**Lista com mais de 10 posições (ex.: 12):** a quantidade de cartas tem que ser igual à de posições. Complete com as extras, na ordem: `extras\carta_11.png`, `carta_12.png` … (importe da mesma versão, quadrada ou larga). Use o `titulo_curto.png` ("1 = PIOR"). Anote e avise a nuvem.

**Lista com 6 a 9 posições:** deixe o mesmo número de cartas, na ordem 01, 02, 03… e use o `titulo_curto.png`. Anote e avise a nuvem.

---

## Parte 5: Título, números e textos

### 5.1 Título

**Caso T1: o template tem título próprio** (Parte 2.1, passo 3)
1. Na **Hierarchy**, clique no objeto do título.
2. No **Inspector**, no componente **Image** (ou **Sprite**), troque o campo **Texture** por **`perrengue_titulo`**.
3. Confira no Preview se a régua do título (volante redondo) está certa. Se não, veja a Parte 7.1.

**Caso T2: o template não tem título** (o mais provável)
1. Na **Hierarchy**, abra **2D Foreground** e clique com o botão direito na **2D Camera**.
2. Clique em **Add** (ou **Create**) → **2D** → **Image**. Pode aparecer como **Screen Image** (a confirmar na sua versão). O objeto novo tem que ficar **dentro** da 2D Camera. Se ele for criado em outro lugar, arraste-o para dentro da **2D Camera** na Hierarchy.
3. Renomeie o objeto para **`Titulo`**.
4. No **Inspector**, componente **Image** → campo **Texture** → **`perrengue_titulo`**.
5. Proporção: deixe o tamanho do objeto em **2 de largura por 1 de altura** (ex.: **Size** 512 × 256). Se houver **Stretch Mode**, escolha **Fit** (a confirmar na sua versão).
6. Na Hierarchy, deixe `Titulo` como o **último** filho da 2D Camera, para ele ser desenhado por cima (a confirmar na sua versão: em alguns programas, quem fica embaixo na lista aparece na frente).
7. A posição e o tamanho finais você acerta na Parte 7.4. Por enquanto, basta o título aparecer inteiro no topo da tela.

> Se você não conseguir criar a imagem 2D, use o **Pedido 2** de `script\prompt-effect-house-ai.md`.

### 5.2 Números da lista (opcional)

Troque os números **só se** a Parte 2.3 mostrou que eles são **10 imagens separadas**, uma por número. Se forem texto, uma imagem única ou qualquer outra coisa, **deixe os números do template** e siga.

1. Ache onde cada número aparece: na **Hierarchy**, dentro de **2D Foreground**, ou numa lista de texturas no **Visual Scripting** (a confirmar na sua versão).
2. Troque a imagem do número 1 por `posicao_01`, a do 2 por `posicao_02`, e assim até o 10 com `posicao_10`.
3. Confira no Preview: os números aparecem **de 1 a 10 na ordem**, sem repetir, e redondinhos (os marcadores são quadrados, 256×256).
4. Se ficarem esticados ou fora do lugar, desfaça (**Ctrl+Z**) e volte aos números do template. A troca é só estética.
5. Apague do Assets os números antigos, se não estiverem mais em uso (mesma regra da Parte 4.3).

### 5.3 Textos em inglês e o grupo Tip

**Tip:** se o grupo **Tip** mostra alguma coisa no Preview, esconda o grupo inteiro: clique nele na Hierarchy e desmarque a caixinha de visível (ou **Set Active = off**; a confirmar na sua versão). **Não apague** o grupo, para não quebrar referência. Confira no Preview se a dica sumiu e se o jogo continua funcionando.

**Textos em inglês:** se a Parte 2.2 achou texto em inglês que **quem usa o efeito vê**, troque assim:

| Texto em inglês (exemplos) | Texto em português | Se for imagem, use |
|---|---|---|
| "Tap to rank", "Tap a number" (instrução) | **TOQUE NO NÚMERO** | `interface\etiqueta_toque.png` (512×128) |
| "Restart", "Play again" | **JOGAR DE NOVO** | `interface\jogar_de_novo.png` (512×128) |
| rótulo ao lado do 1 ("Best", "Worst" etc.) | **PIOR** | `interface\rotulo_pior.png` (256×128) |
| rótulo ao lado do último número | **DE BOA** | `interface\rotulo_de_boa.png` (256×128) |

- **Se o texto for um componente Text:** clique no objeto e troque o texto no campo **Text** do Inspector, em maiúsculas e com acento, exatamente como na tabela.
- **Se for imagem:** troque a **Texture** pela imagem da tabela e confira a proporção (as etiquetas são 4:1; os rótulos, 2:1).
- **Se o texto em inglês não estiver na tabela:** não invente. Esconda o objeto, se o jogo continuar funcionando sem ele. Se não der, deixe e anote no relatório com print.
- Se travar, use o **Pedido 5** de `script\prompt-effect-house-ai.md`.

Se não houver texto em inglês, **não use** nenhuma imagem de `interface\`.

**Se a lista ficou com "PIOR" e "DE BOA" ao lado dos números**, o subtítulo do título repete a mesma informação. Nesse caso, troque o título pelo `titulo_sem_subtitulo.png` da mesma versão (importe, renomeie para `perrengue_titulo_sem_sub`, ponha no objeto do título e apague o `perrengue_titulo` antigo).

Aperte **Ctrl+S**.

---

## Parte 6: A lógica (propriedades do template)

**O template já faz toda a lógica do ranking.** Não crie nós e não apague nós. Só mude os valores abaixo, na caixa do ranking do **Visual Scripting**.

| Propriedade (nome provável) | O que faz | Valor no C09 |
|---|---|---|
| **Randomizer: Textures** | Os itens do ranking | As **10 cartas**, de `carta_01` a `carta_10` (Parte 4) |
| Quantidade de posições/itens (se existir) | Quantas posições a lista tem | **10** |
| Modo (**Loop / Random / Shuffle**), se existir | Como os itens são sorteados | **Shuffle** (cada item aparece uma vez por rodada, em ordem aleatória) |
| **Randomizer: Tap To Stop Randomizer** | Ligado: a pessoa toca para parar o giro e depois toca no número | **Desligado**. O item para sozinho e a pessoa só toca no número. |
| **Randomizer: Wait Between Frames** | Velocidade da troca de imagens no giro | **Deixe o do template** e anote |
| **Randomizer: Shuffle Time** (Min / Max) | Quanto tempo o item gira antes de parar | **Deixe o do template** e anote. **Só se o máximo passar de 3 s:** Min = `1`, Max = `2`. |
| **Extra:** pôr o último item sozinho (nome a confirmar) | Quando sobra 1 posição, o último vai direto para ela | **Ligado** |
| **Extra: Hide Randomizer On Finish** | Esconde o item de cima da cabeça ao terminar | Veja a regra abaixo da tabela |
| **Layout: Space Between Each** e **Layout: Objects Scale** | Espaço e tamanho na lista | **Não mexa agora.** Só na Parte 7.3. |

**Regra do Hide Randomizer On Finish:** ligue e jogue uma rodada inteira.
- Se o item de cima da cabeça **some só no fim**, com a lista completa na tela: **deixe ligado**.
- Se ele some **depois de cada escolha** e o próximo item **não aparece**: **desligue**.
- Se ele some depois de cada escolha, mas o próximo aparece normalmente: **deixe ligado**.
Anote o que aconteceu.

**Se o Tap To Stop desligado travar o jogo** (o item gira sem parar, ou nenhum item aparece): ligue de novo, anote, e siga. Nesse caso, a pessoa toca uma vez para parar e outra no número. O hint do envio continua sendo o de tocar na tela.

Aperte **Ctrl+S**.

---

## Parte 7: Proporção, posição e tamanho

Use o Preview num aparelho com tela **9:16** (ex.: 1080×1920; como no vídeo demo do C01). Confira tudo nos **3 rostos de exemplo**.

Zonas da tela do TikTok que **não podem esconder nada importante** (a câmera do app põe botões nelas):
- **topo:** os primeiros **8%** da altura (botão de fechar e "Adicionar som");
- **direita:** os últimos **15%** da largura, da parte de cima até a metade da tela (botões de virar câmera, velocidade, filtros, timer);
- **baixo:** os últimos **20%** da altura (botão de gravar, efeitos, galeria).

Para medir, tire um print do Preview e compare as posições com a altura e a largura da imagem.

### 7.1 Réguas (nada esticado)

1. Jogue até um item parar em cima da cabeça.
2. Confira a régua da Parte 0.5: **rodas redondas** nas cartas e **volante redondo** no título.
3. Faça a mesma conferência nos itens **já colocados na lista**.
4. **Se esticou:**
   - confira se as cartas e o título são da versão certa (2.6). **Nunca** misture quadrada e larga nas cartas;
   - no objeto que mostra a imagem, procure **Stretch Mode** e escolha **Fit** (a confirmar na sua versão);
   - se não houver, ajuste o **Size** para a proporção da imagem (512×512 = quadrado; 512×256 = altura igual à metade da largura);
   - se nada resolver, troque para a outra versão: apague as 10 cartas do Assets, importe a outra pasta (Parte 3.1) e refaça a Parte 4.1. Anote.

### 7.2 O item em cima da cabeça

Regras:
- a borda de baixo do item fica **logo acima do cabelo**, sem cobrir a testa nem os olhos;
- o item fica **inteiro na tela**, sem corte em cima, nos 3 rostos;
- a largura do item fica entre **1,2 e 1,6 vez a largura da cabeça**;
- o texto do item dá para **ler**, inclusive nas cartas 09, 06, 04 e 05.

**Se algo não bater:** na **Hierarchy**, abra **General → Head Tracker** e clique no objeto que mostra o item. No **Transform**, ajuste:
- **Position Y**, para subir ou descer;
- **Scale**, com **X, Y e Z iguais**, para aumentar ou diminuir (a confirmar na sua versão: quais campos aparecem).

Não exagere na altura: quanto mais longe da cabeça, mais o item treme quando a pessoa se mexe.

### 7.3 A lista de 1 a 10

Regras:
- os **10 números** e os itens colocados ficam **inteiros na tela**;
- nada da lista entra na zona de **baixo** (últimos 20% da altura) nem na faixa da **direita**;
- a lista não cobre os **olhos** nos 3 rostos de exemplo (cobrir um pedaço do ombro ou do cabelo é normal);
- dá para **reconhecer** cada item colocado, pelo desenho ou pela 1ª linha do texto. Na lista, os itens ficam pequenos mesmo; isso é normal nesse formato. O que não pode é ficar cortado ou sumir.

**Se algo não bater**, mude **só** estas duas propriedades da Parte 6, um passo de cada vez, e jogue uma rodada inteira depois de cada mudança:
1. **Layout: Objects Scale**: **+10%** se os itens estiverem difíceis de reconhecer; **−10%** se a lista sair da tela.
2. **Layout: Space Between Each**: **−10%** se a lista passar da zona de baixo; **+10%** se as linhas estiverem encavaladas.

Anote os valores antigos e os novos. Se nada resolver, desfaça e deixe os valores do template.

### 7.4 O título

**Precisa:**
- ficar **inteiro** na tela, com a borda de cima a pelo menos **8%** da altura, contando de cima para baixo (fora da zona do topo);
- **não cobrir** nenhum número nem nenhum item da lista;
- ter a borda direita **antes dos 85%** da largura (fora da faixa dos botões);
- ter pelo menos **45% da largura** da tela, para dar para ler.

**De preferência:** centralizado, com cerca de **60% da largura** da tela, e a borda de cima em cerca de **10% da altura**.

**Passos (Caso T2):**
1. Clique em `Titulo` na Hierarchy.
2. No **Screen Transform** (ou **2D Transform**), ajuste **Position** e **Scale** até chegar na preferência acima. Mude **X e Y da Scale juntos, com o mesmo número**, para não esticar (a confirmar na sua versão: quais campos aparecem).
3. Jogue uma rodada inteira e veja se o título cobre algum número ou item.
4. Se cobrir, tente nesta ordem e pare quando resolver:
   1. suba o título até a borda de cima ficar nos **8%**;
   2. diminua até **50%** da largura;
   3. empurre para a direita até a borda direita chegar nos **85%**;
   4. diminua até **45%** da largura.
5. Se ainda assim cobrir, mande um print para a nuvem e siga com o melhor ajuste possível. Anote.
6. Com o rosto **perto** da câmera, o item de cima da cabeça pode passar por baixo do título. Isso é aceitável, desde que, numa distância normal de selfie (rosto ocupando cerca de 1/3 da largura da tela), os dois não se cubram.

**Caso T1:** use o lugar do título do template e só confira as regras "Precisa" acima.

Aperte **Ctrl+S**.

---

## Parte 8: Testar no PC

### 8.1 Como testar

1. No **Preview**, escolha um rosto de exemplo **em vídeo** (com movimento), se houver.
2. Clique **dentro** da imagem do Preview, **em cima do número** da lista, para simular o toque.
3. Para recomeçar uma rodada, use o **reset/refresh** do Preview, como na Parte 2.5.

### 8.2 Checklist (marque tudo antes de seguir)

- [ ] Ao abrir, aparecem o **título** no topo, a **lista vazia** de 1 a 10 e um **item** em cima da cabeça.
- [ ] **Nenhuma comida** do template aparece em momento nenhum.
- [ ] Nenhum texto em **inglês** e nenhuma **dica** de editor (grupo Tip) aparecem.
- [ ] O item gira e **para sozinho** (ou, se a Parte 6 precisou ligar o Tap To Stop, para com um toque).
- [ ] Ao tocar num número livre, o item vai para o lado **daquele número**.
- [ ] Tocar num número **já usado** não estraga a lista (não faz nada ou não troca o item que já estava lá).
- [ ] Cada item aparece **uma vez só** por rodada.
- [ ] O jogo **termina** depois do 10º item (ou do 9º, se o último vai sozinho), com a lista completa e **sem número trocado ou repetido**.
- [ ] No fim, o que fica na tela é o ranking. Anote se o item de cima da cabeça some ou fica.
- [ ] Rodas e volante **redondos** (nada esticado), em cima da cabeça, na lista e no título.
- [ ] Dá para **ler** o item parado em cima da cabeça, inclusive as cartas **09** (ESQUECER ONDE / ESTACIONOU), **06** (BARULHINHO / NOVO NO CARRO), **04** (VAGA QUE / PARECIA MAIOR) e **05** (LAVAR O CARRO / E CHOVER). **Se usou a versão larga**, confira no lugar delas as cartas **03** (POÇA QUE / ERA CRATERA) e **07** (QUEM NÃO / DÁ SETA). Para conferir sem esperar o sorteio, abra a imagem em `<A>\cartas\` (ou `<A>\largo_512x256\cartas\`) no visualizador do Windows ao lado do Preview e compare o tamanho do texto.
- [ ] Os acentos aparecem certos: POÇA, NÃO, DÁ, ATRÁS.
- [ ] O item **acompanha a cabeça** e fica preso nela quando o rosto se mexe.
- [ ] Quando o rosto **sai** da imagem, o item de cima da cabeça **some** (a lista pode continuar na tela).
- [ ] Não aparece **borda escura** nem quadrado em volta das cartas e do título. A transparência está OK.
- [ ] Título, lista e item respeitam as regras da Parte 7 nos **3 rostos**.
- [ ] Clicar **de novo** depois do fim faz o quê? Anote (nada, recomeça ou outra coisa). Só não pode bugar a lista.
- [ ] Clicar num número **enquanto o item ainda gira** faz o quê? Anote. Só não pode bugar a lista.

### 8.3 Teste do embaralhamento

1. Jogue **3 rodadas inteiras**, recomeçando o Preview entre elas.
2. Em cada rodada, anote a **ordem** em que os itens apareceram (use os números da tabela da 0.6, ex.: "07, 02, 10, …").
3. Avalie:
   - **OK:** em cada rodada, os **10 itens** apareceram, **sem repetir**; e as 3 ordens **não são iguais**, nem começam as 3 pelo mesmo item.
   - **Problema:** item repetido na mesma rodada, item que nunca aparece, ou a mesma ordem toda vez (ex.: sempre 01, 02, 03…).
4. **Se deu problema:**
   1. procure a propriedade de **modo** (Parte 2.4, passo 4) e ponha **Shuffle**; se não houver Shuffle, **Random**;
   2. confira se a lista **Randomizer: Textures** tem as 10 cartas **sem repetir** (Parte 4.2);
   3. jogue as 3 rodadas de novo;
   4. se continuar, use o **Pedido 1** de `script\prompt-effect-house-ai.md`, que pede "each item once per round, in random order";
   5. se ainda assim continuar, vá para o Plano B3 (Parte 18), que embaralha com o nó **Index Generator** em **Shuffle**.

> "Mesma ordem sempre" pode ser só o Preview recomeçando do mesmo jeito. Antes de mudar qualquer coisa, troque de rosto de exemplo entre as rodadas e teste de novo. Anote.

### 8.4 Salvar

1. Confira a barra de título (`C09-perrengue-no-volante`) e aperte **Ctrl+S**.

---

## Parte 9: Versão com rodízio (opcional, até 20 min)

A ideia: pôr os 4 extras (14 itens no total) para que cada rodada sorteie 10 dos 14, e a pessoa tenha motivo para jogar de novo. **Só faça se a versão padrão passou em toda a Parte 8 e se sobrar tempo antes de 17/11. Esta parte é só um teste: o primeiro envio é sempre a versão padrão (passo 7).** Se der qualquer problema, **fica a versão padrão. Não atrase o envio por isso.**

1. **File → Save As** → `C09-perrengue-rodizio`. Confira a barra de título: nesta parte, ela tem que mostrar `C09-perrengue-rodizio`. O projeto padrão fica intacto.
2. Importe `extras\carta_11.png` … `carta_14.png` **da mesma versão** das cartas (pasta `<A>\extras\` ou `<A>\largo_512x256\extras\`).
3. Em **Randomizer: Textures**, crie 4 elementos (botão **+**) e ponha neles `carta_11` a `carta_14`. Total: **14**.
4. **Não mude** a quantidade de posições: continua **10**.
5. Jogue **3 rodadas inteiras** e anote a ordem de cada uma.
6. **Passou** se:
   - nas 3 rodadas, o jogo **parou depois da 10ª escolha**, com a lista certinha (nada deslocado, repetido ou passando de 10);
   - **nenhum item repetiu** dentro de uma rodada;
   - somando as 3 rodadas, apareceram **pelo menos 2 dos extras** (11 a 14).
7. **Passou:** **mesmo assim, no primeiro envio vai o projeto padrão `C09-perrengue-no-volante`.** Motivo (revisão do QA): um relato de fevereiro de 2025 diz que um efeito com mais imagens que posições funcionou no editor, mas o efeito **publicado** só mostrava as mesmas 10 (fontes no fim do guia). O Preview não garante o comportamento no app, e um efeito publicado com a lista bugada atrasa o selo. Salve o projeto do rodízio, anote o resultado no relatório e avise a nuvem: ela decide se o rodízio entra depois, como atualização do efeito já aprovado. (Se um dia ele for enviado, os textos de comentário da Parte 13 trocam "e mais 8" por "e mais 12" e "10 original texts" por "14 original texts".)
8. **Não passou:** feche sem salvar e volte ao `C09-perrengue-no-volante`. Anote o que aconteceu (ex.: "continuou depois da 10ª", "extras nunca aparecem"). **Não tente consertar.** O Pedido 4 do `script\prompt-effect-house-ai.md` só pode ser tentado se a nuvem mandar.

---

## Parte 10: Tamanho e desempenho

1. Na barra de cima, clique em **Click to update** no indicador de tamanho.
2. Anote o tamanho. A estimativa da equipe é de **1,5 a 2,5 MB**: as 10 cartas e o título somam 1,30 MB em PNG (0,93 MB na versão larga), mais o que é do próprio template (a confirmar na sua versão).
   - **Até 5 MB:** siga.
   - **Entre 5 e 8 MB:** dá para enviar (o limite é 8 MB), mas provavelmente sobrou alguma coisa. Volte à Parte 4.3, confira se as comidas foram apagadas e clique em **Click to update** de novo. Se continuar entre 5 e 8 MB, siga e anote o tamanho no relatório.
   - **Acima de 8 MB:** não dá para enviar. Apague o que sobrou e, se ainda passar, mude a compressão das 10 cartas para **Manual → 512 → Medium**. Confira se o texto continua nítido. Deixe o **título** sempre em **High**.
3. Clique em **Test performance** → **Run test** e espere cerca de 30 s.
   - **Passou:** siga.
   - **Falhou:** clique em **View suggestions**, apague o que sobrou e teste de novo.
   - **Não rodou** (como aconteceu no C01): anote a mensagem e siga. O efeito usa só imagens, um Head Tracker e a camada 2D, sem IA e sem segmentação.

---

## Parte 11: Vídeo demo

O formulário 5.16 trata o demo como opcional, mas **mande sempre**. Só a revisão vê o vídeo. Regras: **9:16, MP4 ou MOV, até 15 s, até 32 MB**.

Uma rodada inteira de ranking pode passar de 15 s. Por isso, o plano é gravar a rodada inteira e, se passar de 15 s, juntar o começo e o fim.

### 11.1 Gravar

1. Grave como no C01: aparelho **9:16** no Preview, rosto de exemplo **em vídeo**, e **Screen record** (ou **Win+Shift+R** na Ferramenta de Captura).
2. Recomece o Preview, para começar com a lista vazia.
3. Siga o roteiro:

| Tempo (aprox.) | O que acontece |
|---|---|
| 0–1,5 s | Título no topo, lista vazia, primeiro item girando em cima da cabeça |
| a cada item | Assim que o item parar, clique num número. **Não comece pelo 1**: ponha o 1º item no **5** ou no **6**, para mostrar a graça de guardar posição |
| fim | Lista completa parada por **pelo menos 3 s** |

4. Pare a gravação **3 s depois** do fim da rodada.
5. Salve em `<BASE>\videos-demo\C09-demo-bruto.mp4`.

### 11.2 Cortar e acertar o formato

1. Confira a duração em **Propriedades → Detalhes**.
2. **Se tiver até 15 s:** só acerte o formato:

```powershell
cd "$BASE\videos-demo"
ffmpeg -y -i C09-demo-bruto.mp4 -t 15 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" -c:v libx264 -pix_fmt yuv420p -an C09-demo.mp4
```

3. **Se passar de 15 s:** junte os **primeiros 9 s** com os **últimos 5 s** (14 s no total):

```powershell
cd "$BASE\videos-demo"
ffmpeg -y -i C09-demo-bruto.mp4 -t 9 -c:v libx264 -pix_fmt yuv420p -an C09-parte1.mp4
ffmpeg -y -sseof -5 -i C09-demo-bruto.mp4 -c:v libx264 -pix_fmt yuv420p -an C09-parte2.mp4
ffmpeg -y -i C09-parte1.mp4 -i C09-parte2.mp4 -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[v]" -map "[v]" -c:v libx264 -pix_fmt yuv420p -an C09-demo.mp4
```

Os comandos cortam para 9:16 pelo centro e **tiram o áudio**, para não levar música junto.

4. Abra o `C09-demo.mp4` e confira:
   - em pé, 9:16 (ex.: 1080×1920) e até 15 s;
   - o título, a lista e o item aparecem **inteiros**;
   - o fim mostra a **lista completa**;
   - na emenda (se houve corte), não ficou um quadro preto.
5. Se o corte pelo centro cortar a lista da lateral, grave de novo com o Preview já num aparelho 9:16, para o ffmpeg não precisar cortar nada.

---

## Parte 12: Conferências antes de enviar

### 12.1 Nome

1. Abra **Manage Effects** e confira se nenhum efeito da conta já se chama **Perrengue no volante**.
2. O que pode estar lá: **Eu no grupo da família** (já enviado) e, se já tiverem sido enviados, **Torcedômetro** e **Meu próximo carro**. **Meu 2027 vai ser** só é enviado em 03/12, então ainda não aparece. Se não aparecer algum desses, não é erro: só anote quais estavam lá (isso serve de base para a conferência da Parte 14).

### 12.2 Marca no INPI (5 min; pule se o site não abrir)

1. Abra https://busca.inpi.gov.br/pePI/
2. Clique em **Continuar** (pesquisa sem login) e depois em **Marca** (a confirmar: os nomes dos botões do site).
3. Pesquise `perrengue no volante`.
4. Decida:
   - **Não apareceu nada** (ou só pedidos **arquivados** ou **extintos**): use **Perrengue no volante**.
   - **Apareceu marca ativa ou pedido em andamento** com esse nome: use **Ranking dos perrengues**.
   - **O site não abriu ou pediu login:** use **Perrengue no volante** e anote que a busca não foi feita.

### 12.3 Conteúdo

1. Confira se nenhuma imagem do projeto tem marca, logo, emblema, placa, nome de loja, @ da conta, link ou chamada para comprar. As imagens da equipe já seguem essa regra. O risco é sobrar alguma imagem do template.
2. Confira se **não há comida** em lugar nenhum do Preview.
3. Confira se **não há som** ligado ao efeito.

### 12.4 Salvar e fazer backup

1. Confira a barra de título e aperte **Ctrl+S**.
2. Rode: `Copy-Item -Recurse -Force "$BASE\projetos\C09-perrengue*" "$BASE\projetos\backup\"`
   O `*` leva junto o arquivo ou a pasta do projeto, qualquer que seja o formato (está no `reconhecimento.md`, item 6), e o projeto do rodízio, se existir.

---

## Parte 13: Ícone e envio

### 13.1 Antes: o desafio

O C09 é um **ranking**, não um sorteio. Ele **não está** na lista de efeitos que esperam a decisão do Vini sobre o desafio **"Nov Social Randomizer Sub Challenge"** (atualização de 06/11, 05:40 UTC, do `PRONTO-PARA-MONTAR.md`).

1. Abra o `PRONTO-PARA-MONTAR.md` mais novo (link da 0.2) e leia a seção **Atualizações**. **Se ela disser algo sobre o C09, vale ela, e não este guia.**
2. Veja no `reconhecimento.md` as regras do desafio (que tipo de efeito ou template ele aceita).
3. Decida:
   - **As regras não aceitam ranking** (ex.: só sorteio, só Randomizer): deixe **Challenge** vazio e envie.
   - **A decisão do Vini saiu e é entrar**, e as regras aceitam ranking: selecione o desafio no campo **Challenge**.
   - **A decisão saiu e é não entrar:** deixe **Challenge** vazio e envie.
   - **A decisão não saiu e as regras aceitam ranking:** monte, teste, grave o demo e **pare aqui**. Mande uma mensagem para a nuvem (`session_01XsQ8UziuLNch4tqqVVQfCw`) dizendo que o C09 está pronto e esperando. Se chegar **segunda, 16/11** sem decisão, avise a nuvem de novo. **Se chegar terça, 17/11, sem decisão e sem ordem nova sobre o C09 no `PRONTO-PARA-MONTAR.md`, envie com Challenge vazio** (o C09 não está na lista de espera do desafio, e o prazo de envio dele é 17/11). Anote no relatório.
4. **Nunca aceite os termos do desafio por conta própria.**

### 13.2 Ícone (Create icon)

Pela ordem da equipe, o ícone do formulário 5.16 sai do **Create icon**, com uma foto modelo, e não do `icone_162.png`.

1. Clique em **Create icon** na barra de cima (o mesmo caminho do C08 e do C01).
2. Escolha um modelo de rosto e espere o efeito aparecer nele.
3. **Ícone 1:** o rosto com um item **parado** em cima da cabeça. Prefira, nesta ordem, itens de frase curta e letra grande:
   1. **BATERIA / ARRIADA** (carta 10);
   2. **QUEM NÃO / DÁ SETA** (carta 07);
   3. **BALIZA COM / PLATEIA** (carta 01);
   4. **SUBIDA COM / FILA ATRÁS** (carta 08).
   Se o Create icon aceitar cliques, clique nos números até um desses itens aparecer em cima da cabeça. Se não aceitar, use o item que aparecer, desde que o texto dê para ler. Enquadre o rosto e o item inteiro, com o item ocupando a maior parte do quadrado.
4. **Ícone 2** (se der para ter 2): outro item da lista do passo 3, **de outra cor de moldura** (ex.: se o 1º foi a carta 10, laranja, o 2º pode ser a 07, grafite).
5. Confira na prévia pequena se o texto do ícone 1 dá para ler. Se não der, tente outro item da lista.
6. Clique em **Done** (ou **Submit**, conforme a versão).

**Plano de exceção:** se o Create icon não funcionar e o formulário tiver um botão de **Upload** de PNG, use `<A>\icone_162.png` (volante com gota de suor, fundo amarelo) e, como 2º, `<A>\icone_alt_162.png` (volante com lista 1-2-3, fundo escuro). Anote no relatório.

### 13.3 O formulário

1. Clique em **Submit**, no canto de cima à direita.
2. Se o formulário oferecer caminhos, escolha **Submit a new effect** (enviar um efeito novo). **Não use** **Update an existing effect** nem **Replace an existing effect**: eles trocariam outro efeito da conta pelo C09. Se o formulário vier com o nome ou o ícone de outro efeito preenchido, **pare**, volte e escolha **Submit a new effect**.
3. Preencha:

| Campo | O que colocar |
|---|---|
| **Effect name** | `Perrengue no volante` (20 caracteres; limite 25), ou o nome decidido na 12.2. Sem "AI" no nome (o efeito não usa IA generativa). Se recusar por nome repetido: `Ranking dos perrengues` (22); se recusar de novo: `Ranking do motorista` (20). |
| **Effect icon** | Os ícones do Create icon (13.2) |
| **Hint** (lista) | A opção de **tocar na tela**. Se houver opção em português, use ela (ex.: "Toque na tela"). Se a lista for só em inglês, a mesma que você usou no C01 (provavelmente "Tap the screen" ou parecido). Anote as opções que apareceram. |
| **Sound** (som) | **Nenhum.** Não ligue som. |
| **Challenge** | Conforme a 13.1. |
| **Trend** | Deixe **vazio**, a não ser que o `PRONTO-PARA-MONTAR.md` mande outra coisa. Anote as opções que apareceram (a confirmar na sua versão: o que o campo faz). |
| **Demo video** | `<BASE>\videos-demo\C09-demo.mp4` |

**Se aparecer algum campo que não está na tabela** (a versão pode ter mudado):

| Campo | O que colocar |
|---|---|
| **Description** (descrição) | `Ranking às cegas dos perrengues de quem dirige. Eles aparecem um de cada vez e você escolhe a posição de cada um, de 1 (o pior) a 10, sem saber qual vem depois. Tem baliza com plateia, pneu furado sem estepe e mais 8. Sem marca, modelo de carro, loja, bebida ou direção perigosa.` Se o campo for pequeno: `Monte o ranking dos perrengues do volante sem saber qual vem depois.` |
| **Category** | A mais próxima de **Game** (jogo); se não houver, **Funny** (engraçado); se não houver, **Interactive** |
| **Tags** | `ranking`, `carro`, `motorista`, `perrengue`, `humor`. Se tiver que ser em inglês: `blind ranking`, `car`, `driving`, `ranking`, `funny` |
| **Comentários para a revisão** ("Notes", "Additional comments") | O texto em inglês e, embaixo, o em português, que estão logo abaixo desta tabela |
| Qualquer outro | Deixe o padrão e anote |

**Texto para comentários** (só se o campo existir):

> Blind ranking of everyday driving struggles, in Brazilian Portuguese. Items appear one at a time above your head and you tap a slot from 1 (worst) to 10 without knowing what comes next. 10 original texts with simple drawings (parallel parking with an audience, flat tire with no spare, a puddle that was a pothole, etc.). Built on the Blind Rank template. No generative AI. No brands, car models, logos, store links, alcohol, speeding or dangerous driving.
>
> Ranking às cegas dos perrengues de quem dirige. Eles aparecem um de cada vez e você escolhe a posição de cada um, de 1 (o pior) a 10, sem saber qual vem depois. Tem baliza com plateia, pneu furado sem estepe e mais 8. Sem marca, modelo de carro, loja, bebida ou direção perigosa.

Se for enviar a versão com rodízio (Parte 9): no português, troque "e mais 8" por "e mais 12"; no inglês, "10 original texts" por "14 original texts". Se o template tiver ficado com 5 posições (Parte 4.4): troque "a 10" por "a 5", "e mais 8" por "e mais 3", "to 10" por "to 5" e "10 original texts" por "5 original texts".

### 13.4 Enviar

1. Revise o nome: "Perrengue no volante", com "P" maiúsculo e o resto em minúsculas, sem espaço sobrando.
2. Confira de novo se está no caminho **Submit a new effect**.
3. Clique em **Submit**.
4. Tire um print da confirmação e salve em `<BASE>\prints\C09-enviado.png`.
5. Mande para a nuvem: nome enviado, data e hora, status, tamanho do pacote, versão (quadrada ou larga; padrão, rodízio ou 5 posições), título no Caso T1 ou T2, e se entrou no desafio.

---

## Parte 14: Acompanhar o status

1. Abra **Manage Effects**.
2. **Confira se o C09 aparece como um efeito separado**, ao lado dos que já existiam (nenhum deles sumiu nem mudou de nome). Se algum sumiu, o envio caiu em "Update" ou "Replace": avise a nuvem na hora, com print, e não faça mais nada nesses efeitos.
3. Leia o status do C09:

| Status | O que fazer |
|---|---|
| **Draft** | Clique em **Finish submission** e termine. |
| **Under review** | Esperar (1 a 3 dias úteis). Conferir 1 vez por dia. |
| **Needs revision** | Leia o motivo, corrija (Partes 16 e 17) e reenvie **por este projeto**, com **Replace an existing effect** apontando para **Perrengue no volante** (a confirmar na sua versão: o nome da opção). É o único caso em que "Replace" é usado, e só no próprio C09. |
| **Active** | Anote a data e pegue o link (Manage Effects → menu ⋯ do efeito → **Share**). Mande para a nuvem: ele entra na gravação do Vini de dom 22/11. |
| **Deactivated** | Leia o motivo e avise a nuvem. |

> Para mudar algo enquanto o efeito está **Under review**, use **Withdraw from review**. Ele volta para Draft e precisa ser reenviado.

---

## Parte 15: Resumo de 1 tela

1. Templates → **Interactive** → **Blind Rank** → **Save As `C09-perrengue-no-volante`** → conferir a barra de título.
2. Reconhecer: grupos, quantas posições, proporção das comidas, propriedades do subgraph, texto em inglês, Tip. Jogar 1 rodada.
3. Decidir a versão: proporção até 1,4 → `cartas\` (512×512); acima → `largo_512x256\cartas\`.
4. Importar as 10 cartas **soltas** (não é Texture Sequence) e o título (→ `perrengue_titulo`).
5. **Randomizer: Textures** = exatamente `carta_01` … `carta_10`. Apagar as comidas.
6. Título: trocar a textura (T1) ou criar imagem 2D na 2D Camera (T2). Esconder o Tip. Trocar texto em inglês, se houver.
7. Lógica: Tap To Stop **desligado**, último item sozinho **ligado**, Hide Randomizer On Finish pela regra, Shuffle se existir, tempos do template.
8. Posição: réguas redondas, item acima do cabelo, lista inteira e fora das zonas do app, título sem cobrir a lista.
9. Checklist e 3 rodadas de embaralhamento. Rodízio só se sobrar tempo.
10. Tamanho, Test performance, demo `C09-demo.mp4` (cortar 9 s + 5 s se passar de 15 s).
11. Desafio (13.1) → **Create icon** → **Submit a new effect** → nome `Perrengue no volante`, hint de toque, sem som, trend vazio.

---

## Parte 16: Problemas comuns e soluções

| Problema | Causa provável | Solução |
|---|---|---|
| Não acho o template "Blind Rank" | Busca ou aba diferente | Busque `Blind`, `Rank`, `Ranking`; olhe Interactive, Game e Screen. Se não achar, Parte 18. |
| Não acho a lista **Randomizer: Textures** | Ela está no Inspector, não na caixa (ou o contrário) | Clique na caixa do ranking no Visual Scripting e olhe o Inspector. Se o template tiver outra estrutura, use o **Pedido 1** de `script\prompt-effect-house-ai.md`. |
| Arrastar a carta para a miniatura não troca nada | Soltou fora da miniatura | Solte **em cima** da miniatura da comida. Ou clique no campo do elemento e escolha a carta na lista. |
| Ainda aparece comida no jogo | Sobrou comida em **Randomizer: Textures**, ou o Tip mostra uma | Parte 4.2 (contar os 10) e Parte 5.3 (esconder o Tip). |
| O jogo passa da 10ª escolha, ou os números da lista mudam de lugar | Mais itens que posições | Deixe **exatamente 10** cartas em **Randomizer: Textures** (Parte 4.2). Se estiver no rodízio, volte à versão padrão (Parte 9, passo 8). |
| Item repetido na mesma rodada, ou sempre a mesma ordem | Modo de sorteio | Parte 8.3, passo 4. |
| Clicar no número não faz nada | O item ainda gira, o **Tap To Stop** está ligado, ou o clique foi fora do número | Espere o item parar. Confira a Parte 6. Clique **em cima** do número, dentro do Preview. |
| O jogo trava depois que desliguei o Tap To Stop | O template precisa do toque para parar | Ligue de novo (Parte 6, último parágrafo). |
| O item de cima da cabeça some e o próximo não aparece | **Hide Randomizer On Finish** age a cada escolha | Desligue (regra da Parte 6). |
| O último item não vai sozinho | A opção "Extra" de pôr o último não existe ou está desligada | Ligue, se existir. Se não existir, tudo bem: a pessoa toca no último número. Anote. |
| Carta ou título esticado (roda ou volante virou ovo) | Versão errada ou objeto com outra proporção | Parte 7.1. |
| Lista cortada embaixo ou no lado | Itens grandes ou espaço demais | Parte 7.3 (**Objects Scale** e **Space Between Each**, 10% por vez). |
| Título cobre a lista | Título grande ou baixo demais | Parte 7.4, passo 4. |
| O título não aparece | Ficou fora da 2D Camera, atrás de outra imagem ou fora da tela | Arraste `Titulo` para dentro da **2D Camera** e deixe-o como último filho. Confira **Position**. |
| Texto da carta borrado | Compressão baixa ou imagem esticada | Compressão **High** (Parte 3.4) e réguas (Parte 7.1). |
| Item de cima da cabeça treme ou se descola | Rastreamento, ou item longe demais da cabeça | Teste com mídia em vídeo e pouca luz. Baixe um pouco o **Position Y** (Parte 7.2). Efeito que treme é reprovado. |
| O item fica flutuando quando o rosto sai da imagem | O objeto do item saiu de dentro do **Head Tracker** | Na Hierarchy, confira se o objeto do item continua dentro de **General → Head Tracker**. Se o template original já se comportava assim (Parte 2.5), deixe e anote. |
| Pacote acima de 8 MB | Sobraram comidas ou outras imagens do template | Parte 10. |
| **Test performance** falhou | Algo pesado que sobrou do template | **View suggestions**. Apague o que não é usado. |
| "Asset em uso" ao apagar uma comida | Alguma referência ainda aponta para ela | Parte 4.3, passo 2. |
| Pediu login de novo ou está em outra conta | Login expirou | Seção 0.7, com o link. |
| O formulário veio com nome ou ícone de outro efeito | Caiu em Update ou Replace | Parte 13.3, passo 2: volte e escolha **Submit a new effect**. |
| O formulário recusa o nome | Nome repetido | `Ranking dos perrengues` → `Ranking do motorista`. |
| O formulário recusa o vídeo | Formato, duração ou tamanho | Parte 11.2. Confira 9:16, até 15 s e até 32 MB. |
| **Needs revision** por marca, modelo ou placa | O revisor viu semelhança com um carro ou rede de postos real | Avise a nuvem com o print do motivo e o número da carta. A equipe redesenha. Enquanto isso, troque a carta pela reserva (Parte 17). |
| **Needs revision** por um item específico | Item vetado | Parte 17. |
| **Needs revision** por "parecido demais com o template" ou "baixa qualidade" | O revisor achou pouca mudança | Avise a nuvem com o print. **Não** reenvie sem ordem. Se a nuvem mandar, troque os números pelos marcadores (Parte 5.2), se ainda não trocou. |
| **Needs revision** por desempenho ou tremor | QA técnico | Test performance, teste com movimento, Parte 10. |

---

## Parte 17: Trocar um item vetado

Aqui a troca é fácil, porque cada item é uma imagem solta: basta trocar **uma** imagem em **Randomizer: Textures**. Use as reservas **na ordem R1, R2, R3, R4**. Se a versão com rodízio **não** foi usada, os extras (11 a 14) também servem, depois das reservas.

| Ordem | Arquivo | Texto |
|---|---|---|
| 1ª troca | `reservas\reserva_01.png` (R1) | VOLANTE / PELANDO |
| 2ª troca | `reservas\reserva_02.png` (R2) | LIMPADOR QUE / SÓ ESPALHA |
| 3ª troca | `reservas\reserva_03.png` (R3) | RESERVA ACESA / NA ESTRADA |
| 4ª troca | `reservas\reserva_04.png` (R4) | GARAGEM / BLOQUEADA |
| depois | `extras\carta_11.png` … `carta_14.png` | CARONA QUE / DÁ PITACO, ALARME QUE / DISPARA À TOA, GPS / RECALCULANDO, TRANCAR A / CHAVE DENTRO |

Use **a mesma versão** das cartas do projeto: `<A>\reservas\` (512×512) ou `<A>\largo_512x256\reservas\` (512×256).

1. Abra o projeto do C09 e confira a barra de título.
2. Importe a reserva (**+** → **Import** → **From Computer**).
3. Em **Randomizer: Textures**, arraste a reserva para cima da miniatura da carta vetada.
4. Confira: continuam **10** elementos, sem repetir.
5. Apague a carta vetada do painel **Assets**.
6. Teste (Parte 8.2 e 8.3).
7. Reenvie com **Replace an existing effect** → **Perrengue no volante** (a confirmar na sua versão: o nome da opção).
8. Avise a nuvem qual item foi trocado, para atualizar o `textos.json`.

> **Plano B3 (sequência):** se o projeto foi montado pelo B3, a troca é pelo arquivo, como no C01. Tudo na versão **larga**: mova a carta vetada de `<A>\largo_512x256\cartas\` para a pasta nova `<A>\largo_512x256\cartas_trocadas\` (fora de `cartas\`); copie a reserva de `<A>\largo_512x256\reservas\` para `<A>\largo_512x256\cartas\` e renomeie a cópia com o nome da vetada (ex.: `reserva_01.png` vira `carta_07.png`); confira que `<A>\largo_512x256\cartas\` tem exatamente 10 arquivos e importe a sequência de novo (substituindo `itens_seq`).

---

## Parte 18: Planos B (se o template não der certo)

| Plano | Quando usar | Esforço |
|---|---|---|
| **B1: template parecido** | Não existe "Blind Rank", mas existe um template de ranking às cegas com outro nome | baixo |
| **B2: Effect House AI** | Não existe template de ranking, ou o Blind Rank não funciona, e o assistente funciona nesta conta | baixo a médio |
| **B3: Visual Scripting nó a nó** | Não há template e o assistente não ajudou | alto (≈ 3 h a mais) |

> **Não existe script TypeScript pronto para este efeito.** Se o B2 e o B3 falharem, pare, anote tudo e avise a nuvem com prints. Não envie um efeito que não passou na Parte 8.

### Plano B1: template parecido

1. Na busca de templates, use `Blind`, `Rank`, `Ranking`, `Tier` e `Top 10`.
2. Serve se o template fizer as 4 coisas: mostra **um item por vez**, a pessoa **escolhe a posição** tocando, **não dá para mudar** depois, e a lista final fica na tela.
3. Use-o seguindo **este guia inteiro**, a partir da Parte 1. Onde o guia diz um nome do Blind Rank (ex.: **Randomizer: Textures**), procure o equivalente no template novo e anote.
4. Não serve se for um sorteio (Randomizer), um quiz ou um ranking em que a pessoa vê todos os itens antes.

### Plano B2: Effect House AI

1. Crie um projeto vazio (**New Project** ou **Blank**; a confirmar na sua versão) e salve como `C09-perrengue-no-volante`.
2. Importe **sem** criar sequência: as 10 cartas de `<A>\largo_512x256\cartas\`, o título `<A>\largo_512x256\titulo.png` (→ `perrengue_titulo`) e os 10 números de `<A>\marcadores\`.
3. Importe **também** a pasta `<A>\largo_512x256\cartas\` como **Texture Sequence** e renomeie para `itens_seq` (o assistente pode preferir usar a sequência).
4. Abra o **Effect House AI** e cole o **Pedido 3** de `script\prompt-effect-house-ai.md`.
5. Depois que ele terminar, faça as Partes 7, 8, 10 e seguintes deste guia.
6. Anote no relatório o que o assistente fez.

### Plano B3: Visual Scripting nó a nó

Monta o ranking só com nós citados na documentação oficial. Os nomes de campo estão marcados "a confirmar". Use a versão **larga** (512×256) de tudo.

**Assets:**
1. Importe a pasta `<A>\largo_512x256\cartas\` como **Texture Sequence** (como no C01) e renomeie para `itens_seq`. Confira: **10 frames**, o quadro 0 é a carta 01 e o 9 é a carta 10.
2. Importe `<A>\largo_512x256\titulo.png` (→ `perrengue_titulo`) e os 10 arquivos de `<A>\marcadores\`.

**Objetos (Hierarchy):**
1. `ItemAtual`: **+** → **Face Effects** → **Face Sticker**. Adicione o componente **Animation Sequence** com a sequência `itens_seq`, **sem autoplay** (a confirmar na sua versão). Tamanho 2:1, acima do cabelo, como no C01.
2. Uma imagem 2D `Titulo` com `perrengue_titulo`, no topo (Partes 5.1 e 7.4).
3. 10 imagens 2D `Vaga_01` … `Vaga_10`, uma embaixo da outra, no lado **esquerdo**, entre **18% e 80%** da altura, cada uma com o marcador do seu número (`posicao_01` … `posicao_10`), quadradas, com cerca de **9% da largura** da tela.
4. 10 imagens 2D `Item_01` … `Item_10`, cada uma **à direita** da sua vaga, com proporção 2:1 e cerca de **30% da largura** da tela. Em cada uma, adicione **Animation Sequence** com `itens_seq`, sem autoplay. Deixe as 10 **invisíveis** no começo (desmarque a caixinha de visível na Hierarchy).

**Variáveis** (no painel de variáveis do Visual Scripting; a confirmar na sua versão: onde ficam):
- `itemAtual` (**Number**, valor inicial 0);
- `escolhas` (**Number**, valor inicial 0);
- `livre1` … `livre10` (**Boolean**, valor inicial **true**).

Adicione os nós com o botão direito no painel → buscar o nome.

**Ao abrir o efeito:**
1. **Start** → **Set Visibility** (Target `ItemAtual`, visível **ligado**).
2. → **Set Variable** `escolhas` = `0`.
3. → o bloco **"Próximo item"** (abaixo).

**Bloco "Próximo item"** (um bloco só, que recebe fios de vários lugares):
1. **Index Generator** no modo **Shuffle**, com **10** itens (ou intervalo 0 a 9; a confirmar na sua versão: nome dos campos e da entrada que pede o próximo número). No Shuffle, cada número sai uma vez antes de repetir.
2. → **Set Variable** `itemAtual` = saída do Index Generator.
3. → **Animation Sequence Controller** do `ItemAtual`, entrada **Play**: **From** = **Get Variable** `itemAtual`, **To** = **Get Variable** `itemAtual`, Loop **desligado**. Com From igual a To, aparece só aquele quadro.

> **Não use o nó Random direto em From e em To.** Ele gera um número novo a cada leitura. Por isso o valor passa pela variável `itemAtual`.

**Para cada vaga (faça a vaga 1, teste, e depois copie):**
1. **Screen Image Tap** com Image = `Vaga_01` (o nó antigo **Image Tap** foi substituído por este). Saída **On Image Tapped** →
2. **If** (ou **Branch**), Condition = **Get Variable** `livre1`. Saída **True** →
3. **Set Variable** `livre1` = **false** →
4. **Animation Sequence Controller** do `Item_01`, **Play**, From = To = **Get Variable** `itemAtual`, Loop desligado →
5. **Set Visibility** (`Item_01`, **ligado**) →
6. o **bloco "Fim de jogada"** (abaixo).

Teste a vaga 1 no Preview: ao clicar no 1, o item de cima da cabeça aparece ao lado do 1 e o próximo item aparece em cima da cabeça. Depois, selecione os nós da vaga 1, **Ctrl+C**, **Ctrl+V**, e troque na cópia: `Vaga_01` → `Vaga_02`, `livre1` → `livre2` (nos 2 lugares) e `Item_01` → `Item_02` (nos 2 lugares). Repita até a vaga 10.

**Bloco "Fim de jogada"** (um só, recebe os fios das 10 vagas):
1. **Set Variable** `escolhas` = **Add** (Get Variable `escolhas`, `1`) →
2. **If**, Condition = **Equal** (Get Variable `escolhas`, `10`):
   - **True** → **Set Visibility** (`ItemAtual`, **desligado**). A rodada acabou e a lista fica na tela.
   - **False** → bloco **"Próximo item"**.

**Limite:** este plano não recomeça quando a pessoa aperta gravar. Quem usa abre o efeito, aperta gravar e joga. Anote no relatório. Se o nó **Video Record Start** existir e você tiver tempo, ligue nele: as 10 **Set Variable** `livreN` = true, os 10 **Set Visibility** `Item_N` desligado e o mesmo caminho do "Ao abrir o efeito".

Depois, faça as Partes 7, 8, 10 e seguintes deste guia.

---

## Parte 19: O que anotar no relatório

Em `<BASE>\relatorio-montagem.md`, na seção do C09:

- Nome exato do template e onde estava (aba, busca).
- Nomes reais dos grupos e objetos da Hierarchy (General, Head Tracker, 2D Foreground, 2D Camera, Tip…).
- Quantas posições a lista tem, e quantas comidas e com que resolução vieram.
- Nomes e valores **originais** de todas as propriedades do subgraph, e os que você deixou.
- Versão usada (quadrada ou larga), título no Caso T1 ou T2 e arquivo do título.
- Se trocou os números (Parte 5.2) e os textos em inglês (Parte 5.3), e o que fez com o Tip.
- Resultado da Regra do Hide Randomizer On Finish e do Tap To Stop.
- As ordens das 3 rodadas do teste de embaralhamento (Parte 8.3).
- O que acontece ao tocar num número usado, ao tocar durante o giro e ao tocar depois do fim.
- Se existe evento de gravação (Video Record Start) no template.
- Rodízio: tentado ou não, e o resultado.
- Tamanho do pacote e resultado do Test performance (ou a mensagem, se não rodou).
- Plano usado: template, B1, B2 ou B3.
- Resultado do INPI, nome enviado, hint escolhido (e a lista de opções), opções do campo **Trend**, se entrou no desafio, itens usados no Create icon.
- Data e hora do envio, print e status.
- Qualquer "a confirmar" deste guia que você viu de verdade, e o que era.

---

## Fontes consultadas

Documentação oficial do Effect House (lida por resumos de busca, porque o site não abre daqui):
- Template Blind Rank: Templates → aba Interactive; escala de 1 a 10; grupo **General** com **Head Tracker** (item que gira) e **2D Foreground** com **2D Camera** (lista); grupo **Tip**; propriedades **Randomizer: Textures** (trocar arrastando do Assets para a miniatura; dá para selecionar várias com Ctrl), **Randomizer: Wait Between Frames**, **Randomizer: Shuffle Time (Min/Max)**, **Randomizer: Tap To Stop Randomizer** (escrito "Tap To Shop" na página), **Layout: Space Between Each**, **Layout: Objects Scale**, opção de pôr o último item sozinho e **Extra: Hide Randomizer On Finish**: https://effecthouse.tiktok.com/learn/guides/tutorials/template-tutorials/blind-rank · https://effecthouse.tiktok.com/learn/library/template-tutorials/blind-rank
- Nó **Screen Image Tap** (substitui o **Image Tap**, que ficou obsoleto na v2.1.0): https://effecthouse.tiktok.com/learn/guides/editor-panels/visual-scripting/nodes/utility/screen-image-tap · https://effecthouse.tiktok.com/learn/guides/editor-panels/visual-scripting/nodes/utility/image-tap
- Envio, com as opções "Submit a new effect", "Update an existing effect" e "Replace an existing effect": https://effecthouse.tiktok.com/learn/guides/publishing/publish/submit-your-effect
- Ícone (Create icon, até 2 ícones, PNG 162×162, área segura 144×144): https://effecthouse.tiktok.com/learn/guides/publishing/effect-icon-creation
- Status e retirada da revisão: https://effecthouse.tiktok.com/learn/guides/management-and-growth/manage-your-effect
- Nós **Index Generator** (Loop, Random, Shuffle), **Animation Sequence Controller**, **Set Visibility**, **Start** e limites técnicos: `tiktok-efeitos/pesquisa/03-tecnico-effect-house.md`.

Fórum e terceiros:
- Mais de 10 imagens em Randomizer: Textures fazem o jogo passar da 10ª escolha e bugar a lista (sem solução confirmada): https://community.effecthouse.com/t/help-with-blind-rank-template/60530
- Outro relato (fev/2025, sem resposta): com 26 imagens, o efeito publicado só mostrava as mesmas 10. Reforça a regra de exatamente 10 itens: https://community.sproutsocial.com/content-creation-67/effect-house-help-2424

Da própria equipe:
- Formulário do Effect House 5.16 (nome, ícone pelo Create icon, hint de lista, som, challenge, trend e demo) e a regra de esperar a decisão do desafio para os sorteios: `PRONTO-PARA-MONTAR.md`, atualizações de 06/11.
- Textos, nomes, hint, descrição e tags: `textos.md` e `textos.json` desta pasta.
- Medidas e pesos das imagens: conferidos pela equipe nos arquivos de `assets/` em 06/11/2026.
