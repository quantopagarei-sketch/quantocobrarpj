# 03 — Guia técnico de referência: Effect House (2026)

**Para quem é:** agentes da equipe que vão escrever passo a passos de montagem e criar imagens/texturas. (Não é texto para o Vini.)
**Data da pesquisa:** 06/11/2026 · **Método:** ~30 buscas (boa parte em modo extended, várias restritas ao domínio effecthouse.tiktok.com). Os sites effecthouse.tiktok.com, community.effecthouse.com, formulae.brew.sh e uptodown.com **não abrem desta máquina**; o que está aqui saiu dos resumos que a busca traz dessas páginas. Por isso todo item tem fonte e etiqueta.

**Legenda:** ✅ = confirmado em página oficial (resumo da busca) · ⚠️ = confirmado, mas as páginas oficiais se contradizem ou são antigas · ❓ = a confirmar (só terceiros, dedução nossa ou não achado)

---

## 0. Resumo em 12 linhas (o que mais importa)

1. ✅ Download oficial: **https://effecthouse.tiktok.com/download** (Windows 10+ ou macOS; no Mac há build separada para **Apple (M1/M2…)** e **Intel**).
2. ✅ Login: o app mostra um **QR code**; escaneia-se com o **scanner do app TikTok** (não com a câmera do celular), logado na conta que vai publicar (Car Shop). Depois toca em **Confirmar** no celular.
3. ⚠️ Versão: release notes oficiais vão até **v5.14.0 (26/08/2026)**; site de terceiros lista **5.15.0 (22/09/2026)** e **5.16.0 (28/10/2026)**. Não existe 6.0. Usar sempre a mais nova da página de download.
4. ✅ Limite do pacote do efeito: **8 MB** (antes era 5 MB). Imagem: **≤ 1024×1024 px e < 1 MB cada**. Meta recomendada: texturas **512×512**, efeito total **≤ 5 MB** por segurança.
5. ✅ Ícone: **PNG, exportar 162×162 px, área segura central 144×144 px**; o app arredonda os cantos sozinho. Até **2 ícones**.
6. ✅ Formulário de envio: **Nome (obrigatório, máx. 25 caracteres, único)**, **Ícone (obrigatório)**, **Categoria (obrigatório)**, **Hint (opcional)**, **Tags (opcional, até 5, não públicas)**, **Vídeo demo (9:16, MP4/MOV, ≤ 32 MB, ≤ 15 s; opcional/obrigatório conflita — mandar sempre)**, **Challenge (opcional)**.
7. ✅ Teste no celular: botão **"Preview in TikTok"** gera QR → escanear no app TikTok (mesma conta). Dá para gravar a tela do celular durante o preview → vira o vídeo demo.
8. ✅ Antes de enviar: botão **"Test performance"** na barra de título → **Run test** (~30 s). Se falhar → **View suggestions**.
9. ✅ Status no **Manage Effects**: Draft · Under review · Needs revision (com motivo) · Active · Deactivated. Revisão: ~1 a 3 dias úteis.
10. ✅ Templates úteis confirmados: **Randomizer 2D / Randomizer 3D**, **Future Life** (previsão), **Big Head** (cabeção), **Face Stretch**, **3D Face Warp** (tem forma "Balloon"), **Face Mask**, **Segmentation**, **Green Screen TVs / Photo Slideshow** (foto da galeria), **Side Scroll Jelly Game** (jogo com boca/piscada), **Tap And Catch**, **Personality Quiz**, **Blind Rank**, **Face Inset**, **Face Morph**, **Wobbly Face**.
11. ✅ Visual Scripting: nós **Start**, **Update**, **Screen Tap**, **Face Detection**, **Facial Movement Detection** (Mouth Open, Blink…), **Set Visibility** (não "Set Visible"), **Random** (Math), **Index Generator** (Random/Shuffle), **Timer**, **Wait for Seconds**, **Delay Set**.
12. ✅ Existe scripting em **TypeScript** (API "APJS"): arquivos `.ts`, classe exportada com `@component()` que estende `APJS.BasicScriptComponent`, com `onStart / onUpdate / onDestroy`. Para iniciante e para os nossos efeitos, **Visual Scripting basta**.

---

## 1. Instalação e requisitos

### 1.1 Link direto (para mandar ao Vini)
| O quê | Link | Status |
|---|---|---|
| Página de download | **https://effecthouse.tiktok.com/download** | ✅ página existe e está indexada com o título "Create TikTok effects" (busca). Não consegui abrir daqui, então o botão exato não foi visto. |
| Guia oficial "Download and Login" | https://effecthouse.tiktok.com/learn/guides/getting-started/introduction-to-effect-house/download-and-login | ✅ |
| Home do Effect House | https://effecthouse.tiktok.com/ | ✅ |

### 1.2 Requisitos
- ✅ **Só desktop: Windows e macOS.** FAQ oficial: "currently only supported on Mac OS and Windows". Fonte: https://effecthouse.tiktok.com/learn/guides/support/faqs
- ✅ **Windows 10 ou superior.** Fonte: https://effecthouse.tiktok.com/latest/effect-house-for-windows
- ✅ **Mac: duas builds diferentes — chip Apple (M1 etc.) e chip Intel.** Baixar a errada é erro comum. Fonte: FAQ acima; página de desafio LIVE lista "Windows, Mac (M1), Mac (Intel)".
- ⚠️ macOS mínimo: Homebrew (build 5.5.1, dez/2025) indica **macOS 10.15 (Catalina)** ou superior. Fonte: https://formulae.brew.sh/cask/effect-house (resumo da busca).
- ❓ Hardware mínimo: só há dado de 2022 (Core i3 ou Apple M1, 4 GB RAM, tela 1280×768). Desatualizado. Recomendação prática da equipe: 8 GB de RAM ou mais e placa de vídeo com driver atualizado (dedução, não oficial).
- ✅ FAQ recomenda boa conexão de internet durante o download.

### 1.3 Versão atual (2026)
- ✅ Release notes oficiais citam **v5.12.0 (28/06/2026)**, **v5.13.0 (29/07/2026)** e **v5.14.0 (26/08/2026)**. Fonte: https://effecthouse.tiktok.com/latest/release-notes-latest
  - v5.14.0: melhor redimensionamento de janela para usar lado a lado com apps de agente de IA.
  - v5.13.0: o antigo "Create with AI" (janela de prompt) foi **aposentado**; "Ask AI" foi renomeado para **"Effect House AI"** (agente de IA que monta cenas, escreve scripts e importa/gera assets dentro do editor).
  - v5.12.0: correções; **AI Graph Editor** (encadear modelos de IA, ex.: imagem→imagem→vídeo).
  - Outra pesquisa da equipe (02-monetizacao) achou entrada de **22/09/2026** nas release notes (vincular som da biblioteca do TikTok ao efeito).
- ❓ Uptodown (terceiro) lista **5.15.0 (22/09/2026)** e **5.16.0 (28/10/2026)** como mais recentes. Bate com a entrada de 22/09. **Tratar 5.16.x como provável versão atual (a confirmar ao abrir o download).**
- ⚠️ Menus mudam entre versões. Passo a passo deve dizer "na versão 5.1x" e usar nomes de painel genéricos quando possível.

### 1.4 Login
- ✅ Ao abrir o app, aparece um **QR code**. No app TikTok do celular: **Perfil → Adicionar amigos (ícone de pessoa) → ícone de scanner** (canto superior direito) → escanear → **Confirm/Confirmar** no celular. Fonte: guia Download and Login.
- ✅ Tem que ser o **scanner do TikTok**, não a câmera comum. ✅ Existe opção **"Log in with other methods"** (outro método; detalhes não vistos).
- ✅ QR é o login principal desde uma versão recente (release notes).
- ⚠️ A conta logada no Effect House é a "dona" do efeito e do dinheiro do Rewards. **Tem que ser a conta Car Shop do Vini.** (Elegibilidade do ECR depende da região de criação da conta — ver arquivo 02.)

### 1.5 O que depende do Vini (mínimo possível, num momento só)
1. Baixar e instalar o Effect House no computador dele (link acima; se Mac, escolher Apple ou Intel — no Mac: menu  → "Sobre este Mac" → se aparecer "Chip Apple M…" é Apple; se "Processador Intel" é Intel).
2. Abrir o app e escanear o QR com o app TikTok da conta Car Shop → Confirmar.
3. (Depois, por efeito) Escanear o QR do "Preview in TikTok" se a equipe não tiver acesso a um celular logado na conta — e apertar **Submit** / concluir o formulário web, se a equipe não estiver operando o computador dele.
> ❓ Como a equipe vai operar o computador dele (acesso remoto, ele mesmo clicando seguindo roteiro, ou arquivo de projeto enviado para ele) precisa ser decidido pelo coordenador. O Effect House salva projetos como arquivo/pasta de projeto que pode ser copiado (❓ extensão exata não confirmada nesta pesquisa).

---

## 2. Templates prontos relevantes

✅ Templates ficam na **Home do app → aba Templates**, filtráveis por categoria (ex.: **Face**, **Interactive**, **Screen**, **Game**). Fonte: https://effecthouse.tiktok.com/learn/guides/crash-course/effect-house-101/using-effect-templates-and-the-asset-library
✅ Há busca de templates e projetos na home (desde v3.0.0).

| Mecânica que queremos | Nome no Effect House | O que faz / como se mexe | Status | Fonte |
|---|---|---|---|---|
| **Sorteio / roleta em cima da cabeça** ("qual carro você seria", "qual posição no time") | **Randomizer 2D** (também **Randomizer 3D**) | Sequência de imagens (texture sequence) gira rápido em cima da cabeça e para num quadro aleatório. Subgrafo expõe **TapToSpin, TimeToSpin, TitleDelay, TitleFadeOutTime**. Título = imagem no objeto **Title**; imagens das opções vão no objeto **RandomAnimationSequence**. Segue a cabeça via componente **Face Sticker**. Versão para 2 pessoas: duplicar objetos e usar "Which Face". | ✅ | https://effecthouse.tiktok.com/learn/guides/tutorials/template-tutorials/randomizer-2d |
| **Previsão / futuro** (ideal p/ "previsão 2027") | **Future Life** | Bolhas de sabão com perguntas (padrão: Lover, Income, Kids) cujas respostas são sorteadas. Ativa com **toque na tela, biquinho (pout/pucker)**. Trocar assets de título, bolhas e texturas animadas; **fazer os assets em BRANCO** para o randomizador de cor funcionar. **Não mexer na pasta "DO NOT REMOVE!!! Main Assets"**. | ✅ | https://effecthouse.tiktok.com/learn/library/template-tutorials/future-life |
| Quiz de personalidade / "qual tipo de torcedor você é" | **Personality Quiz**, **One Person Quiz** | Quiz com resultado. | ✅ (nome) / ❓ detalhes | https://effecthouse.tiktok.com/learn/guides/tutorials/template-tutorials/personality-quiz |
| Ranking às cegas ("rankeie esses carros") | **Blind Rank** | Itens aparecem um a um e a pessoa posiciona. | ✅ (nome) / ❓ detalhes | https://effecthouse.tiktok.com/learn/guides/tutorials/template-tutorials/blind-rank |
| **Cabeção / cabecinha** | **Big Head** (aba Face) | Usa **Head Segmentation**; controla tamanho por **Scale 2D** do objeto da cabeça e posição por **Head Offset**. Escala < 1 = cabeça pequena. | ✅ | https://effecthouse.tiktok.com/learn/guides/tutorials/template-tutorials/big-head |
| **Deformar rosto / balão / cabeça redonda** | **3D Face Warp** (componente) | Sliders de formato de cabeça/rosto, olhos, nariz, boca, queixo (Face Width, Face Height, Head Curve…). Seção **Face Shape** tem opção **"Balloon"**. | ✅ (existe) / ❓ comportamento do Balloon | https://effecthouse.tiktok.com/learn/guides/workspace/components/face-effects/3d-face-warp |
| Esticar pontos do rosto | **Face Stretch** (objeto) | Template 2D de pontos do rosto; arrastar pontos; **Intensity** controla força; pode ser assimétrico. | ✅ | https://effecthouse.tiktok.com/learn/guides/technical-guides/objects/face-effects/face-stretch |
| Distorção por sliders | **Face Distortion** (template), **Wobbly Face**, **Face Morph**, **Face Fuse** | Variações de deformação/fusão. | ✅ (nomes) | https://effecthouse.tiktok.com/learn/library/template-tutorials/face-distortion |
| **Pintura no rosto** (ex.: faixas de torcedor em cores genéricas) | **Face Mask** (objeto) | Textura 2D sobre o rosto (ver specs na seção 4). | ✅ | https://effecthouse.tiktok.com/learn/guides/workspace/objects/face-effects/face-mask |
| Rosto dentro de outra coisa | **Face Inset** | Recorta o rosto e coloca em outro lugar (ex.: rosto num "adesivo"). | ✅ (nome) | https://effecthouse.tiktok.com/learn/guides/tutorials/template-tutorials/face-inset |
| **Troca de fundo / green screen** | **Portrait Segmentation** (objeto) + **Segmentation** (template) | Separa pessoa do fundo; fundo vira imagem nossa. | ✅ | https://effecthouse.tiktok.com/learn/guides/tutorials/template-tutorials/segmentation-2 |
| Fundo com **foto da galeria do usuário** | **Image Picker Texture** (antigo **User Media Texture**, renomeado na v4.9.0); templates **Green Screen TVs**, **Photo Slideshow**, **Photo Dump** | Placeholder quadriculado verde trocado pela foto do usuário. **Até 8 por projeto, só imagem (não vídeo)**. Pode usar segmentação Portrait/Subject/Head. | ✅ | https://effecthouse.tiktok.com/learn/guides/workspace/assets/texture/user-media-texture |
| Segmentações disponíveis | **Segmentation Texture** / objetos Portrait, Hair, Hand, Clothing, **Head Segmentation** | Tipos citados: Portrait, Hair, Head, Face, Hand, Clothing, Skin, Eye, Ear, Lip, Teeth, Pet, Subject, Sky, Ground, Building. **Hair Segmentation** permite pintar o cabelo (ex.: cabelo na cor do time genérico). | ✅ (lista varia por versão) | https://effecthouse.tiktok.com/learn/guides/technical-guides/assets/texture/segmentation-texture · https://effecthouse.tiktok.com/learn/guides/technical-guides/objects/segmentation/head-segmentation |
| **Filtro de cor (LUT)** | Objeto **Filter** (Post Effect) + **LUT Texture** | Padrão "Bright LUT Texture"; prontos: Black and White, Saturated, Warm, Cool; **Intensity 0–1**; importa LUT própria. | ✅ | https://effecthouse.tiktok.com/learn/library/assets/filter |
| **Jogo controlado pelo rosto** | **Side Scroll Jelly Game** (aba Interactive) | Força pode ser **Mouth Open** ou **Eye Blink** para começar e mover o jogador entre obstáculos. Melhor base para "desvie dos buracos da rua" (tema carro). | ✅ | https://effecthouse.tiktok.com/learn/guides/tutorials/template-tutorials/side-scroll-jelly-game |
| Jogo de toque / timing | **Tap And Catch** (aba Screen) | Tocar para parar objeto no alvo (ex.: "pare o ponteiro do conta-giros na faixa"). | ✅ | https://effecthouse.tiktok.com/learn/guides/tutorials/template-tutorials/tap-and-catch |
| Zoom interativo | **Interactive Zoom** | Mostra como trocar gatilho de gesto por **Facial Movement Detection**. | ✅ | https://effecthouse.tiktok.com/learn/guides/tutorials/template-tutorials/interactive-zoom |
| Voz/afinação | **Perfect Pitch** (aba Game) | Detecção de tom pelo microfone. | ✅ (nome) | https://effecthouse.tiktok.com/learn/guides/tutorials/template-tutorials/perfect-pitch |
| Boca falante em objeto | **Talking Potato** | Usa Head Tracker. | ✅ (nome) | https://effecthouse.tiktok.com/learn/guides/tutorials/template-tutorials/talking-potato |
| **IA generativa (rosto)** | componente **Generative Effects** | Estilos prontos (GAN): Smile, Pucker, Eyebrow Eraser, Shocked, Neutral, Wink, Slow Blink, Side Eye, Cartoon, Sad Face, **Hair Eraser**… **Impacto de performance muito alto: usar no máximo 1 e não misturar com muita coisa.** | ✅ | https://effecthouse.tiktok.com/learn/guides/technical-guides/components/utility/generative-effects |
| **IA generativa (estilo de imagem/vídeo)** | **AI Editor** (Image Model por prompt de texto; Video Model imagem→vídeo) e **AI Graph Editor** | Modelos disponíveis mudam com o tempo. **Video Model só para selos Platinum e Diamond.** Lip Sync foi removido. | ✅ | https://effecthouse.tiktok.com/learn/guides/ai-capabilities/ai-editor/ · https://effecthouse.tiktok.com/learn/guides/ai-capabilities/ai-editor/create-an-ai-effect-using-ai-editor |
| Agente de IA dentro do editor | **Effect House AI** (ex-"Ask AI") | Descreve em linguagem natural e o agente monta cena/scripts/assets. | ✅ (v5.13+) / ❓ disponibilidade por região/conta | https://effecthouse.tiktok.com/latest/release-notes-latest |

- ✅ Recomendação oficial: colocar **"AI"** no nome de efeitos que usam IA generativa (transparência). Fonte: https://effecthouse.tiktok.com/learn/guides/getting-started/best-practices/using-generative-ai-to-create-tiktok-effects
- ❓ Não achei template chamado literalmente "Green Screen" (o recurso existe via Segmentation/Image Picker), "Head Shrink", "Balloon Face" ou "Face Liquify".

---

## 3. Visual Scripting e Scripting

### 3.1 Visual Scripting (nós) — ✅ salvo indicação
Painel **Visual Scripting**; adicionar nó: **botão direito no painel → buscar o nome**. Fluxo: saídas de execução (Exec/Next) ligam na entrada (Enter) do próximo nó. Visão geral: https://effecthouse.tiktok.com/learn/guides/editor-panels/visual-scripting

| Precisamos de | Nó (nome real) | Detalhes | Fonte |
|---|---|---|---|
| Rodar ao abrir / a cada quadro | **Start** e **Update** (às vezes "On Start"/"On Update") | Start = quando o efeito começa; Update = todo quadro. | crash course VS módulo 4/5 |
| Toque na tela | **Screen Tap** (categoria Event) | Saída **Next** quando toca; saída **Position** (Vec2) do toque. | https://effecthouse.tiktok.com/learn/guides/visual-scripting/nodes/event/screen-tap |
| Rosto apareceu/sumiu | **Face Detection** | Até **5 rostos**; saídas **Begin, Stay, End, None** + **Face Count**. Um nó por rosto. | https://effecthouse.tiktok.com/learn/guides/editor-panels/visual-scripting/nodes/head-and-face/face-detection |
| Boca aberta / piscar / sobrancelha | **Facial Movement Detection** | Propriedade **Facial Movement** = **Mouth Open** (e outras, ex. piscada). Estados **begin / stay / end / none**. | https://effecthouse.tiktok.com/learn/guides/editor-panels/visual-scripting/nodes/head-and-face/facial-movement-detection |
| Mostrar/esconder objeto | **Set Visibility** (não "Set Visible") | Exec → **Enter**; objeto alvo na entrada **Target** (arrastar o objeto da Hierarchy para virar nó "Entity: Scene Object"). | Module 7 crash course |
| Número aleatório | **Random** (categoria Math) | Gera número dentro de um intervalo. **Gera um número NOVO cada vez que é lido** → para usar o mesmo sorteio em 2 lugares, guardar o valor (ex.: em variável ou ler uma vez via Timer). Fórum relata o "bug" de valores diferentes em duas entradas (2023). | https://effecthouse.tiktok.com/learn/guides/tutorials/template-tutorials/randomizer-2d · https://community.effecthouse.com/t/random-nodes-are-broken/58340 |
| Sortear índice sem repetir | **Index Generator** (Utility) | Modos **Loop**, **Random** (pode repetir), **Shuffle** (todos uma vez, ordem aleatória). Ótimo para "sorteio de 1 a N imagens". | https://effecthouse.tiktok.com/learn/guides/visual-scripting/nodes/utility/index-generator |
| Escolher entre valores | **Select** (Utility) | Seleciona valor por índice/condição. | https://effecthouse.tiktok.com/learn/guides/visual-scripting/nodes/utility/select |
| Cronômetro | **Timer** (Time) | Entradas **Start, Pause, Resume**, **Duration** (segundos); saídas **Started, Tick** (todo quadro), **Completed**; dados **Elapsed Time, Progress (%), Remaining**. | https://effecthouse.tiktok.com/learn/guides/visual-scripting/nodes/time/timer |
| Esperar X segundos | **Wait for Seconds** (Time) | Enter → espera N s → Exit. O "Delay" simples. | https://effecthouse.tiktok.com/learn/guides/visual-scripting/nodes/time/wait-for-seconds |
| Valor com atraso | **Delay Set** (Utility) | Define valor após **Delay Duration**; antes disso devolve 0/vazio. | https://effecthouse.tiktok.com/learn/guides/editor-panels/visual-scripting/nodes/utility/delay-set |
| Transição por tempo | **Transit by Time**, **Lerp** | Animações suaves de valor. | páginas de nós |
| Pegar asset por código | **Get Asset** (v3.0.0+) | Troca textura em tempo de execução. | release notes |
| Interações prontas (sem montar nó) | **Interactions** / "Triggers and responses" | Presets tipo "Tap Screen to Delay Show/Hide Object", "Tap Screen to Play Animation Sequence Then Delay Pause". Cycling: Loop/Random/Shuffle. | https://effecthouse.tiktok.com/learn/guides/editor-panels/visual-scripting/interactions/ |
| Reaproveitar | **Subgraph** | Salvar subgrafo na aba **Custom**. | release notes v3.0.0 |

- ✅ **Texto dinâmico:** existe componente **Text** e objeto **2D Text**; há tópico no fórum sobre setar valor do Text via VS (https://community.effecthouse.com/t/set-value-for-text-component/42442). ❓ Nome exato do nó para mudar o texto (provavelmente um "Set" de propriedade do componente Text) — conferir no app.
- ✅ Cada nó tem ícone de info no painel com a documentação; usar para checar nomes na versão instalada.

### 3.2 Scripting em TypeScript (APJS) — ✅
- ✅ Existe. Guia: **Scripting Capability Usage Guide** — https://effecthouse.tiktok.com/learn/guides/api-reference/scripting-capability-usage-guide
- ✅ Regras: arquivo **`.ts`**, **exportar uma classe** com o decorator **`@component()`** que estende **`APJS.BasicScriptComponent`**; ciclo de vida **`onStart()`, `onUpdate(dt)`, `onDestroy()`**; propriedades serializadas aparecem no **Inspector**; **não usar `require`** (usar `import`); evitar nomes de script duplicados (o app renomeia). Só **Component Scripts** podem ser anexados a objetos.
- ✅ Exemplo oficial "TapCounter": pega o componente Text no `onStart`, assina o evento global de Touch e remove no `onDestroy`.
- ✅ Há referência de API (ex.: SceneObject, Ray): https://effecthouse.tiktok.com/learn/guides/api-reference/scene/sceneobject
- ❓ Caminho exato do menu para criar o script (provável: Assets → Add/+ → Script). Conferir.
- **Recomendação da equipe:** nossos efeitos (sorteio, previsão, filtro de cor, cabeção, jogo simples) dão para fazer **só com templates + Visual Scripting**. TypeScript só se precisar de lógica que os nós não cobrem. O agente "Effect House AI" pode escrever scripts, mas exige o Vini/operador logado no app.

---

## 4. Especificações de arquivos

### 4.1 Limites gerais
| Item | Valor | Status | Fonte |
|---|---|---|---|
| **Pacote total do efeito** | **≤ 8 MB** (subiu de 5 MB) | ✅ release notes + QA no "Technical Optimization" ⚠️ páginas antigas (Face Mask) ainda dizem 5 MB | https://effecthouse.tiktok.com/learn/guides/getting-started/technical-guidelines/technical-optimization |
| **Meta da equipe** | **≤ 5 MB** (cabe nas duas regras e carrega rápido em celular fraco) | recomendação | — |
| Imagem individual | **< 1 MB** (QA cita "no more than 1025 KB") | ✅ | idem + https://effecthouse.tiktok.com/learn/guides/technical-guides/assets/asset-preparation/screen-image |
| Resolução de imagem | **máx. 1024×1024 px**; **recomendado 512×512** | ✅ | idem |
| Importação acima de 1024 | é redimensionada (lado maior = 1024); se ainda > 1 MB, a importação para | ✅ | 2D asset preparation |
| Compressão no app | **Automatic** (lado máx. 512 px, mantém proporção) ou **Manual** (1024/512/256/128; qualidade High/Medium/Low — **só High é sem perda**) | ✅ | Screen Image Preparation |
| Vídeo individual | ≤ 8 MB | ✅ | Video Asset Preparation |
| Sequência de texturas (animação 2D) | PNG ou JPG; **até 200 quadros** (versão antiga dizia < 20); **12 FPS** sugerido | ⚠️ | https://effecthouse.tiktok.com/learn/guides/technical-guides/assets/asset-preparation/2d-texture-sequence |
| Prefabs | até 25 MB | ✅ | release notes |
| Image Picker (foto do usuário) | até 8 por projeto; só imagem | ✅ | User Media Texture |
| Potência de 2 (256/512/1024) | não exigido nas fontes achadas | ❓ (usar 512 ou 1024 mesmo assim — é boa prática) | — |

### 4.2 Texturas PNG com transparência (para os agentes de imagem)
- ✅ Formatos aceitos: **PNG ou JPG**. Para transparência: **PNG-24 com canal alfa** (Photoshop: exportar só conteúdo da prancheta, sem fundo, PNG-24). Fonte: Face Mask guide.
- Recomendações práticas (dedução nossa a partir dos limites acima):
  - Elementos sobre a cabeça (randomizer, título): **512×512** ou **512×256**, fundo transparente, margem de ~8% vazia nas bordas.
  - Telas cheias/fundos: proporção 9:16, ex. **576×1024** (cabe no limite de 1024), JPG se não precisar de transparência (menor).
  - Sequência do randomizer: **todas as imagens com o mesmo tamanho** (ex.: 512×512) e mesmo enquadramento; nomear em ordem (`opcao_01.png`, `opcao_02.png`…). ❓ Regra de nomenclatura exata da importação de sequência não confirmada.
  - **Future Life:** assets **brancos** (o template colore).
  - Otimizar PNG (pngquant/oxipng) para ficar bem abaixo de 1 MB.
- ✅ **Face Mask:** máx. **1024×1024**, PNG/JPG, < 1 MB; usar o **template oficial de rosto** (para v2.1+: `face_mask_2.1+.zip`; antigo: `face_mask.psd`) que mostra rosto inteiro, olhos, cílios, lábios e dentes; testar nos **3 modelos de rosto** do Preview (tons de pele diferentes). Fontes: https://effecthouse.tiktok.com/learn/guides/workspace/objects/face-effects/face-mask · https://effecthouse.tiktok.com/learn/guides/workspace/assets/downloadable-assets/2d-face-mask
- ✅ 3D Face: `face_uv.png` é outro asset (UV da malha 3D), não confundir com o template 2D.

### 4.3 LUT (filtro de cor) — atenção
- ✅ Fluxo oficial: baixar na página **Filter** os arquivos **`color_card.zip`** (LUTs de exemplo) e **`color_card_template.zip`** (PSD com camada **DEFAULT COLORCARD** + foto de exemplo). Esconder a camada DEFAULT COLORCARD, aplicar **camadas de ajuste** sobre a foto; quando gostar, esconder a foto e mostrar a DEFAULT COLORCARD (**abaixo** das camadas de ajuste); salvar **PNG**. Fonte: https://effecthouse.tiktok.com/learn/library/assets/filter
- ✅ Importar: **Assets → Add (+) → Import → From Computer**. Aplicar: selecionar objeto **Filter** na Hierarchy → no Inspector trocar **"Bright LUT Texture"** pela nossa → ajustar **Intensity (0–1)**.
- ✅ v4.6.0: Post Effects ganhou **AI Filter** que também aceita importar LUT textures.
- ❓ **Dimensões/layout exatos da LUT do Effect House NÃO foram confirmados** em página oficial. O padrão de mercado para "color card" é **512×512 px, grade 8×8 de blocos 64×64 (LUT 64³)** — muito provável, mas **a confirmar**. Outras convenções (256×16, 1024×32) existem em outros programas e **não** devem ser usadas sem teste.
- ❓ Não há confirmação de suporte a arquivo **.cube** (usar PNG).
- **Procedimento seguro para a equipe:** (1) usar o PNG neutro de dentro do `color_card.zip` como base e **manter exatamente as mesmas dimensões e orientação**; (2) aplicar os ajustes de cor por cima (Photoshop, GIMP, Photopea ou script Python aplicando a transformação de cor pixel a pixel na imagem neutra); (3) **teste de sanidade:** importar a LUT neutra sem alteração com Intensity 1 — a imagem do preview não pode mudar nada; se mudar, o layout está errado. (4) Nunca redimensionar nem comprimir com perda (sem JPG, sem compressão Medium/Low) — estraga a LUT.

### 4.4 Ícone do efeito (envio)
- ✅ **PNG**, **exportar 162×162 px**, **área segura 144×144 px** no centro. O Effect House **corta e arredonda os cantos** e cria uma borda de transição transparente. Não precisa preencher tudo. Imagem sem fundo recebe **fundo padrão**. Pode-se criar **até 2 ícones**. Tem que respeitar propriedade intelectual (nada de escudo/logo/marca). Fonte: https://effecthouse.tiktok.com/learn/guides/publishing/effect-icon-creation
- ⚠️ Versão antiga (3.7.0) do guia cita limite de importação de **2 MB / 1024×1024**. Nosso ícone de 162×162 fica muito abaixo disso.
- Dica: desenhar em 648×648 (4×) e reduzir para 162×162; elemento principal grande, alto contraste, legível em tamanho pequeno; pouco ou nenhum texto.

### 4.5 Fontes de texto
- ✅ Componente **Text** / objeto **2D Text** com propriedade **Font** (opções de fonte desde **v3.7.0, 22/01/2024**). Preenchimento por cor sólida, **gradiente** ou **textura** (via **Text Art**). Fontes: https://effecthouse.tiktok.com/learn/guides/technical-guides/components/2d/text · https://effecthouse.tiktok.com/learn/guides/workspace/objects/2d/2d-text · https://effecthouse.tiktok.com/learn/guides/technical-guides/assets/texture/text-art
- ❓ **Importar fonte própria (.ttf/.otf) NÃO confirmado.** Alternativa garantida: **escrever o texto direto na imagem PNG** (texto "assado" na textura). Para os efeitos de sorteio/previsão, isso é o caminho mais seguro — e permite usar qualquer fonte de licença livre (ex.: Google Fonts, licença OFL) nas imagens.
- ✅ Texto do efeito também passa pelas regras (nada de marca, time, celebridade).

### 4.6 Vídeo de demonstração
- ✅ **9:16 (vertical)**, **MP4 ou MOV**, **≤ 32 MB**, **≤ 15 s**. Não é público; só a equipe de revisão vê. Deve mostrar fielmente o que o efeito faz. ⚠️ Uma página diz opcional, outra obrigatório → **mandar sempre**. Fonte: https://effecthouse.tiktok.com/learn/guides/publishing/demo-video-creation
- ✅ Jeito fácil: **gravar a tela do celular durante o "Preview in TikTok"**.

---

## 5. Teste e envio

### 5.1 Preview no computador
- ✅ Painel **Preview** com vídeos/rostos de teste (3 modelos de rosto com tons de pele diferentes, citados no guia de Face Mask) e **Profiler** (FPS e memória em tempo real). Fonte: https://effecthouse.tiktok.com/learn/guides/workspace/panels/preview-panel · https://effecthouse.tiktok.com/learn/guides/publishing/preview/preview-in-effect-house
- ❓ Nomes exatos dos vídeos de teste na versão atual — conferir.

### 5.2 Preview no celular ("Preview in TikTok")
- ✅ Botão **"Preview in TikTok"** gera **QR code único** do efeito aberto. Fonte: https://effecthouse.tiktok.com/learn/guides/publishing/preview-in-tiktok
- ✅ Escanear com o **scanner do app TikTok** (aba Descobrir/Discover → ícone de scanner no canto superior direito, **ou** Amigos/Perfil → Adicionar amigos → scanner). ✅ O guia diz para estar logado **com a mesma conta** do Effect House. ⚠️ Página de outra versão diz que o QR expira em **14 dias ou após 30 contas**, o que sugere que outras contas também podem abrir o preview (a confirmar) — isso permitiria a equipe testar num celular próprio sem acionar o Vini.
- ✅ **Hints não aparecem** no preview do TikTok.
- ✅ Preview no celular é necessário para testar **câmera AR/traseira e gestos de tela**.
- ❓ Fórum (antigo): em alguns Android/Samsung o toque no preview é interpretado como foco/trocar filtro. Testar em mais de um aparelho. https://community.effecthouse.com/t/bug-in-preview-in-tiktok/43191

### 5.3 Teste de desempenho (obrigatório na prática)
- ✅ Barra de título → **Test performance** → **Run test** (~30 s). Passou → pode enviar. Falhou → **View suggestions** (abre o guia de otimização). Mede **frame rate**; falhas vêm de modelos com muitos polígonos, shaders complexos, sombras, pós-processamento, física, texturas grandes e **mais de um Generative Effect**. **Segmentation** e **Body Avatar Drive** derrubam FPS. Passar no teste **não garante** aprovação. Fonte: https://effecthouse.tiktok.com/learn/guides/publishing/publish/test-effect-performance
- ✅ Indicador de tamanho do efeito na barra de título (**"Click to update"** atualiza o tamanho do pacote).

### 5.4 Envio (Submit)
- ✅ Botão **Submit** no Effect House → janela do app → **formulário web** → revisar a página de detalhes → enviar. Fonte: https://effecthouse.tiktok.com/learn/guides/publishing/publish/submit-your-effect
- Campos ✅:

| Campo | Obrigatório? | Regra |
|---|---|---|
| **Effect name** | Sim | Máx. **25 caracteres**, **único** entre seus efeitos, segue as Effect Guidelines. Se usar IA generativa, incluir "AI" (recomendação). |
| **Effect icon** | Sim | Ver 4.4. |
| **Category** | Sim | Ajuda na descoberta. ❓ Lista de categorias não obtida — escolher no formulário. |
| **Hint** | Não | Aparece toda vez que alguém abre o efeito. ⚠️ Guia antigo diz que se **escolhe de uma lista** de hints prontos (não texto livre) — a confirmar no formulário. |
| **Tags** | Não | Até **5**, não públicas, seguem as regras. |
| **Demo video** | ⚠️ conflito | 9:16, MP4/MOV, ≤ 32 MB, ≤ 15 s. Mandar sempre. |
| **Challenge** | Não | Selecionar desafio ativo, se houver (ex.: desafios temáticos). |
| Comentários p/ revisão | ⚠️ só em guia antigo | Texto não público para a equipe de revisão. |

- ✅ Duas revisões: **QA técnico** e **moderação de conteúdo**.
- ⚠️ Prazo: "até 1 dia útil" (uma página) / "~2–3 dias úteis" (Quickstart) / "1–3 dias úteis". Planejar **3 dias úteis**.

### 5.5 Onde ver o status
- ✅ Botão **Manage Effects** (página de gerenciamento). Fonte: https://effecthouse.tiktok.com/learn/guides/management-and-growth/manage-your-effect

| Status | Significado | Ação |
|---|---|---|
| **Draft** | Enviado pelo app mas formulário web não concluído | Menu de ações → **Finish submission** |
| **Under review** | Em revisão | Pode **Withdraw from review** (volta a Draft) |
| **Needs revision** | Reprovado | Abrir detalhe → motivo em **Status** → corrigir no app → reenviar |
| **Active** | No ar no TikTok | Apagar tira do ar, mas vídeos já feitos continuam |
| **Deactivated** | Fora do ar sem apagar | Pode reativar (versão antiga do guia) |

- ⚠️ Limites de edição conflitam: "Active/Deactivated criados nos últimos 6 meses podem ser editados" (até 5 vezes em 6 meses, segundo uma versão) / "até 10 reenvios antes de precisar de arquivo novo".
- ✅ Analytics do efeito: https://effecthouse.tiktok.com/learn/guides/publishing/manage/effect-analytics · Rewards Center: aba **Rewards** na home do app (ver arquivo 02).

---

## 6. Limitações e armadilhas de iniciante

1. ✅ **Baixar a build errada no Mac** (Intel × Apple). Conferir o chip antes.
2. ✅ **Escanear o QR com a câmera do celular** em vez do scanner do TikTok → não funciona.
3. ⚠️ **Conta errada logada** (efeito e recompensas ficam na conta logada). Tem que ser a Car Shop.
4. ✅ **Estourar tamanho:** imagem > 1 MB ou > 1024 px, pacote > 8 MB. Manter tudo 512 px quando der e o pacote ≤ 5 MB.
5. ✅ **Comprimir a LUT** (Medium/Low ou JPG) ou redimensioná-la → cores erradas. LUT sempre PNG sem perda, nas dimensões do color card oficial.
6. ✅ **Empilhar recursos pesados** (Generative Effect + Segmentation + Body Avatar etc.) → reprovação por FPS/"segurança". Fórum relata rejeição instantânea por "security requirements" nessa combinação. Regra da equipe: **no máximo 1 recurso pesado por efeito**. https://community.effecthouse.com/t/review-instantly-rejected/44509
7. ✅ **Random gera valor novo a cada leitura** → resultado mostrado ≠ resultado usado. Guardar o valor ou usar Index Generator.
8. ✅ **Apagar a pasta "DO NOT REMOVE!!!"** em templates (ex.: Future Life) quebra o efeito.
9. ✅ **Assets coloridos no Future Life** — o template espera branco.
10. ✅ **Hint não aparece no preview do celular** → não achar que está quebrado.
11. ❓ **Toque não funciona no preview em alguns Android** (fórum antigo) → testar em outro aparelho.
12. ✅ **Efeito que treme/descola do rosto** é reprovado com frequência (pesquisa 02). Testar com movimento rápido de cabeça e pouca luz.
13. ✅ **Testar nos 3 rostos-modelo** (tons de pele) — inclusão é critério de qualidade.
14. ✅ **Nome > 25 caracteres ou repetido** → não envia.
15. ✅ **Conteúdo proibido:** marca, logo, time, escudo, celebridade, link/CTA, efeito de marca → reprovação (ver arquivo 02). Isso inclui **ícone, nome, tags e vídeo demo**.
16. ✅ **Docs desatualizadas:** muitas páginas oficiais são de 2022–2023 (v1–v3) e se contradizem (5 MB × 8 MB; demo opcional × obrigatório). Sempre preferir o que o app mostra na versão instalada.
17. ✅ **Passou no Test performance ≠ aprovado.** Ainda pode cair na revisão por performance em celular fraco.
18. ❓ **Fonte própria** não confirmada → texto em PNG.
19. ✅ **Image Picker só aceita imagem** (não vídeo), até 8 por projeto.
20. ✅ **Video Model do AI Editor** só para Platinum/Diamond → conta nova não tem.

---

## 7. Pendências (a confirmar quando o app estiver aberto no computador do Vini)
1. ❓ Versão instalada (esperado 5.16.x).
2. ❓ Dimensões do PNG neutro dentro de `color_card.zip` (esperado 512×512, grade 8×8).
3. ❓ Lista de **categorias** e se o **hint** é texto livre ou lista.
4. ❓ Se o QR do "Preview in TikTok" abre em outra conta (permitiria a equipe testar sem o Vini).
5. ❓ Se dá para importar .ttf/.otf.
6. ❓ Nome do nó para alterar texto do componente Text pelo Visual Scripting.
7. ❓ Menu exato para criar script TypeScript e formato/extensão do arquivo de projeto (para levar projetos prontos ao computador dele).
8. ❓ Disponibilidade do "Effect House AI" (agente) para a conta/região.

---

## 8. Fontes principais (oficiais, salvo indicação)
- Download: https://effecthouse.tiktok.com/download
- Download and Login: https://effecthouse.tiktok.com/learn/guides/getting-started/introduction-to-effect-house/download-and-login
- Windows: https://effecthouse.tiktok.com/latest/effect-house-for-windows
- FAQ: https://effecthouse.tiktok.com/learn/guides/support/faqs
- Release notes: https://effecthouse.tiktok.com/latest/release-notes-latest
- Templates e Asset Library: https://effecthouse.tiktok.com/learn/guides/crash-course/effect-house-101/using-effect-templates-and-the-asset-library
- Randomizer 2D: https://effecthouse.tiktok.com/learn/guides/tutorials/template-tutorials/randomizer-2d
- Future Life: https://effecthouse.tiktok.com/learn/library/template-tutorials/future-life
- Big Head: https://effecthouse.tiktok.com/learn/guides/tutorials/template-tutorials/big-head
- 3D Face Warp: https://effecthouse.tiktok.com/learn/guides/workspace/components/face-effects/3d-face-warp
- Face Stretch: https://effecthouse.tiktok.com/learn/guides/technical-guides/objects/face-effects/face-stretch
- Face Mask: https://effecthouse.tiktok.com/learn/guides/workspace/objects/face-effects/face-mask · 2D Face Mask Reference: https://effecthouse.tiktok.com/learn/guides/workspace/assets/downloadable-assets/2d-face-mask
- Segmentation (template): https://effecthouse.tiktok.com/learn/guides/tutorials/template-tutorials/segmentation-2 · Segmentation Texture: https://effecthouse.tiktok.com/learn/guides/technical-guides/assets/texture/segmentation-texture · Head Segmentation: https://effecthouse.tiktok.com/learn/guides/technical-guides/objects/segmentation/head-segmentation
- Image Picker / User Media Texture: https://effecthouse.tiktok.com/learn/guides/workspace/assets/texture/user-media-texture
- Side Scroll Jelly Game: https://effecthouse.tiktok.com/learn/guides/tutorials/template-tutorials/side-scroll-jelly-game · Tap And Catch: https://effecthouse.tiktok.com/learn/guides/tutorials/template-tutorials/tap-and-catch
- Generative Effects: https://effecthouse.tiktok.com/learn/guides/technical-guides/components/utility/generative-effects · IA generativa (boas práticas): https://effecthouse.tiktok.com/learn/guides/getting-started/best-practices/using-generative-ai-to-create-tiktok-effects
- AI Editor: https://effecthouse.tiktok.com/learn/guides/ai-capabilities/ai-editor/ · Create With AI: https://effecthouse.tiktok.com/learn/guides/ai-capabilities/create-with-ai
- Filter (LUT/color card): https://effecthouse.tiktok.com/learn/library/assets/filter · LUT Texture: https://effecthouse.tiktok.com/learn/guides/workspace/assets/texture/lut-texture
- Visual Scripting: https://effecthouse.tiktok.com/learn/guides/editor-panels/visual-scripting · Screen Tap: https://effecthouse.tiktok.com/learn/guides/visual-scripting/nodes/event/screen-tap · Face Detection: https://effecthouse.tiktok.com/learn/guides/editor-panels/visual-scripting/nodes/head-and-face/face-detection · Facial Movement Detection: https://effecthouse.tiktok.com/learn/guides/editor-panels/visual-scripting/nodes/head-and-face/facial-movement-detection · Timer: https://effecthouse.tiktok.com/learn/guides/visual-scripting/nodes/time/timer · Wait for Seconds: https://effecthouse.tiktok.com/learn/guides/visual-scripting/nodes/time/wait-for-seconds · Delay Set: https://effecthouse.tiktok.com/learn/guides/editor-panels/visual-scripting/nodes/utility/delay-set · Index Generator: https://effecthouse.tiktok.com/learn/guides/visual-scripting/nodes/utility/index-generator · Module 7 (Set Visibility): https://effecthouse.tiktok.com/learn/guides/crash-course/effect-house-101/creating-tiktok-effects-using-visual-scripting · Interactions: https://effecthouse.tiktok.com/learn/guides/editor-panels/visual-scripting/interactions/
- TypeScript/APJS: https://effecthouse.tiktok.com/learn/guides/api-reference/scripting-capability-usage-guide
- Text: https://effecthouse.tiktok.com/learn/guides/technical-guides/components/2d/text · 2D Text: https://effecthouse.tiktok.com/learn/guides/workspace/objects/2d/2d-text · Text Art: https://effecthouse.tiktok.com/learn/guides/technical-guides/assets/texture/text-art
- Technical Optimization: https://effecthouse.tiktok.com/learn/guides/getting-started/technical-guidelines/technical-optimization · Screen Image Preparation: https://effecthouse.tiktok.com/learn/guides/technical-guides/assets/asset-preparation/screen-image · 2D Texture Sequence: https://effecthouse.tiktok.com/learn/guides/technical-guides/assets/asset-preparation/2d-texture-sequence
- Test Effect Performance: https://effecthouse.tiktok.com/learn/guides/publishing/publish/test-effect-performance · Preview Panel: https://effecthouse.tiktok.com/learn/guides/workspace/panels/preview-panel
- Preview in TikTok: https://effecthouse.tiktok.com/learn/guides/publishing/preview-in-tiktok
- Submit Your Effect: https://effecthouse.tiktok.com/learn/guides/publishing/publish/submit-your-effect · Effect Icon Creation: https://effecthouse.tiktok.com/learn/guides/publishing/effect-icon-creation · Demo Video Creation: https://effecthouse.tiktok.com/learn/guides/publishing/demo-video-creation
- Manage Your Effect: https://effecthouse.tiktok.com/learn/guides/management-and-growth/manage-your-effect · Effect Analytics: https://effecthouse.tiktok.com/learn/guides/publishing/manage/effect-analytics
- Terceiros/fórum: Homebrew cask https://formulae.brew.sh/cask/effect-house · Uptodown https://effect-house.en.uptodown.com/mac · Fórum: https://community.effecthouse.com/t/random-nodes-are-broken/58340 · https://community.effecthouse.com/t/bug-in-preview-in-tiktok/43191 · https://community.effecthouse.com/t/review-instantly-rejected/44509 · https://community.effecthouse.com/t/set-value-for-text-component/42442
