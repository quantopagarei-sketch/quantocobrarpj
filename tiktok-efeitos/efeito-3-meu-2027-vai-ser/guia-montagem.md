# Guia de montagem: "Meu 2027 vai ser" (C05)

**Para quem é:** quem vai montar o efeito no Effect House. Pode ser o Montador (o Claude que roda no PC do Vini) ou o próprio Vini, mesmo sem nunca ter aberto o programa.
**Versão do guia:** 1.1 · 06/11/2026 · escrito para o Effect House 5.1x no Windows (no Mac, troque **Ctrl** por **Cmd** e "Explorador de Arquivos" por **Finder**).
**Tempo total:** cerca de 4 h sem imprevistos. Reserve 6 h.

> **Vini, se você estiver lendo:** não precisa fazer nada aqui. Este roteiro é para quem monta. Você só será chamado nos casos da seção 0.7, e sempre com o link direto.

### Como ler as marcas

- **(a confirmar na sua versão do programa)**: a equipe não conseguiu ver essa tela, porque o site do Effect House não abre de onde pesquisamos. Se o botão ou o objeto tiver outro nome, procure um parecido e **anote no relatório** o nome real.
- Os nomes de botões, painéis e objetos estão **em inglês e em negrito**, porque o programa é em inglês.
- Nos passos, "clique" é com o botão esquerdo. Quando for o direito, o passo diz "clique com o botão direito".
- `<DOCS>` é a pasta Documentos do PC (seção 0.3). `<PASTA>` é a pasta de imagens escolhida na Parte 3.

### O que vamos montar (resumo)

1. Na tela aparece o título **"MEU 2027 / VAI SER…"** e 3 bolhas de sabão: **AMOR**, **GRANA** e **FUTEBOL**.
2. A pessoa **faz biquinho** ou **toca na tela**.
3. As bolhas estouram. Cada uma mostra uma previsão sorteada entre 8, por exemplo "TÍTULO VEM / (CONFIA)" ou "O 13º DURA / ATÉ O DIA 3".
4. A cada abertura do efeito, o template sorteia uma cor e pinta título, rótulos e respostas. Por isso todas as nossas artes são **brancas**.

A base é o template pronto **Future Life**. Ele já tem a lógica (bolhas, estouro, sorteio de cor e de resposta), então **não é preciso programar**. O trabalho é trocar imagens, ajustar o número de respostas no sorteio e **desligar a IA generativa** que vem no template.

### Decisões já tomadas (não mude sem falar com a equipe da nuvem)

| Decisão | Por quê |
|---|---|
| **3 bolhas** (AMOR, GRANA, FUTEBOL) | Uma 4ª bolha exige duplicar objetos e lógica do template, e é aí que o projeto quebra. O tema carro já aparece nas respostas ("TANQUE CHEIO O ANO TODO", "BUZINAÇO DE CAMPEÃO"). A 4ª bolha fica como extra opcional (Parte 17). |
| **Desligar a IA do template** (Parte 6) | O template traz 2 efeitos de IA generativa (**Pucker** e **Unhappy**). A documentação oficial recomenda não usar mais de 1 efeito desse tipo, por causa da queda de FPS, que pode reprovar no teste técnico. Ela também recomenda pôr "AI" no nome de efeitos que mudam o rosto com IA. Além disso, o FAQ do programa de recompensas diz que efeito gerado por IA **não é elegível** (uma página mais antiga do TikTok diz o contrário; a equipe segue o FAQ). E a "cara triste" (Unhappy) não combina com previsões boas. |
| **Manter o sorteio de cor** do template | É o charme do formato. A leitura em fundo claro se resolve com a versão com sombra (Parte 3.2). |
| **Não tocar** na pasta **"DO NOT REMOVE!!! - Main Assets"** | O tutorial oficial proíbe mexer nela. Ela guarda as texturas da bolha e da varinha. |

---

## Parte 0: Antes de começar

### 0.1 Links

| O quê | Link direto | Quem usa |
|---|---|---|
| Baixar o Effect House (Windows 10 ou mais novo; no Mac há uma versão para chip Apple e outra para Intel) | https://effecthouse.tiktok.com/download | Montador. Só se o programa ainda não estiver instalado. |
| Guia oficial de instalação e login | https://effecthouse.tiktok.com/learn/guides/getting-started/introduction-to-effect-house/download-and-login | Consulta |
| Arquivos da equipe (zip com tudo) | https://github.com/quantopagarei-sketch/quantocobrarpj/archive/refs/heads/main.zip | Montador |
| Aviso de que a equipe terminou (erro 404 = ainda não terminou) | https://raw.githubusercontent.com/quantopagarei-sketch/quantocobrarpj/main/tiktok-efeitos/PRONTO-PARA-MONTAR.md | Montador |
| Tutorial oficial do template Future Life (em inglês) | https://effecthouse.tiktok.com/learn/library/template-tutorials/future-life | Consulta |
| O mesmo tutorial, endereço alternativo | https://effecthouse.tiktok.com/learn/guides/tutorials/template-tutorials/future-life | Consulta |
| Nó Animated Texture Player (em inglês) | https://effecthouse.tiktok.com/learn/guides/visual-scripting/nodes/utility/animated-texture-player | Consulta (Parte 7) |
| Nó Facial Movement Detection (biquinho = **Mouth Pout**) | https://effecthouse.tiktok.com/learn/guides/editor-panels/visual-scripting/nodes/head-and-face/facial-movement-detection | Consulta (Parte 7) |
| Regras para IA generativa em efeitos | https://effecthouse.tiktok.com/learn/guides/getting-started/best-practices/using-generative-ai-to-create-tiktok-effects | Consulta (Parte 6) |
| Guia oficial de envio | https://effecthouse.tiktok.com/learn/guides/publishing/publish/submit-your-effect | Consulta |

> O zip só traz este efeito **depois** que a equipe publicar os arquivos. Antes de baixar, confira se o link do "Aviso" abre.

### 0.2 Quando enviar (importante)

Este efeito é de **Réveillon**. Se ele entrar no ar cedo demais, a janela de 30 dias do programa de recompensas acaba antes do pico de uso (de 26/12 a 10/01).

- **Montar e testar:** pode e deve ser feito já.
- **Enviar (Parte 13):** na data indicada no `PRONTO-PARA-MONTAR.md` ou pela equipe da nuvem. Se ninguém indicar data, envie **entre 01/12 e 08/12/2026**, de preferência perto de 05/12. Assim ele entra no ar por volta de 08 a 12/12 e ainda sobra tempo para corrigir uma reprovação antes do Natal.
- **Exceção que vale mais que a data:** se a equipe disser que este efeito é da **"situação A"** (ver `lancamento.md`, seção 0), ele só pode ser enviado **depois** que a aba **Rewards** do Effect House mostrar a inscrição no programa de recompensas **aprovada**. Efeito publicado antes da admissão não rende ✅ (FAQ oficial). Nesse caso, se a aprovação não sair até 15/12, avise a equipe da nuvem e espere a decisão.
- **Não envie em novembro** sem ordem da equipe.
- Enquanto espera, deixe o projeto salvo e o vídeo demo pronto (Parte 10).

### 0.3 Copiar os arquivos para o computador

1. Baixe o zip pelo link da tabela.
2. Abra o zip.
3. Copie **só a pasta `tiktok-efeitos`** para `Documentos\Efeitos\`.
4. Confira se esta pasta existe:
   `Documentos\Efeitos\tiktok-efeitos\efeito-3-meu-2027-vai-ser\assets\`

> **Montador:** no Windows, "Documentos" fica em `%USERPROFILE%\Documents`. Com o OneDrive ativo, pode ser `%USERPROFILE%\OneDrive\Documentos`. Para descobrir, rode no PowerShell: `[Environment]::GetFolderPath('MyDocuments')`. Esse caminho é o `<DOCS>`.

### 0.4 Conferir os arquivos

Rode no PowerShell, trocando `<DOCS>` pelo caminho de Documentos:

```powershell
$a = "<DOCS>\Efeitos\tiktok-efeitos\efeito-3-meu-2027-vai-ser\assets"
foreach ($v in @("$a", "$a\variantes\com_sombra", "$a\variantes\quadrado_512", "$a\variantes\quadrado_512_com_sombra")) {
  $c = foreach ($b in "amor","grana","futebol","carro") { (Get-ChildItem "$v\respostas_$b").Count }
  "$v -> $($c -join ' ')"      # nas 4 linhas tem que dar: 8 8 8 6
}
Get-ChildItem "$a\titulo.png", "$a\bolha_*.png", "$a\icone_162.png", "$a\icone_alt_162.png", "$a\variantes\bolha_inteira\bolha_vazia.png" | Select Name, Length
(Get-ChildItem $a -Recurse -Filter *.png | Where-Object Name -ne "previa.png" | Measure-Object Length -Maximum).Maximum   # tem que ser menor que 1048576 (1 MB)
```

Se faltar arquivo, baixe o zip de novo. Se continuar faltando, avise a equipe da nuvem. Não chame o Vini por isso.

### 0.5 O que entra no efeito e o que não entra

Todas as artes do efeito são **brancas com fundo transparente**. No Explorador de Arquivos elas parecem "vazias" sobre fundo branco. Isso é normal. Para ver como ficam, abra `assets\previa.png`.

| Arquivo (dentro de `assets\`) | Entra? | Para quê |
|---|---|---|
| `titulo.png` (1024×512) | **Sim** | Título "MEU 2027 / VAI SER…". Troca o "My Future Life". |
| `bolha_amor.png`, `bolha_grana.png`, `bolha_futebol.png` (512×256) | **Sim** | Rótulos das bolhas, com palavra e ícone branco. Trocam Lover, Income e Kids. |
| `respostas_amor\amor_01…08.png`, `respostas_grana\grana_01…08.png`, `respostas_futebol\futebol_01…08.png` (512×128) | **Sim** | As 24 respostas. Cada pasta entra como **uma** sequência de imagens (**Texture Sequence**). |
| `variantes\com_sombra\` (mesmos nomes) | **Provável** | Mesmas artes com sombra preta suave. Decide-se na Parte 3.2. |
| `variantes\quadrado_512\` e `variantes\quadrado_512_com_sombra\` | Só se precisar | Tudo em 512×512, para o caso de as texturas do template serem quadradas (Parte 3.1). |
| `variantes\bolha_inteira\bolha_vazia.png` (512×512) | **Recomendado, se funcionar** | Nosso desenho de bolha, para o efeito não ficar igual a todos os outros feitos com o template (Parte 5.4). |
| `icone_162.png` | **No formulário de envio** | Ícone do efeito (obrigatório) |
| `icone_alt_162.png` | **No formulário de envio** | 2º ícone (opcional) |
| `bolha_carro.png` e `respostas_carro\carro_01…06.png` | Não (só na Parte 17) | 4ª bolha ou troca de FUTEBOL por CARRO |
| `reservas\reserva_<bolha>_01…02.png` | Não | Só se uma frase for vetada (Parte 15) |
| `variantes\rotulos_sem_icone\` | Não, salvo exceção | Rótulos só com a palavra, se o ícone ficar apertado na bolha |
| `variantes\bolha_inteira\bolha_inteira_<bolha>.png` | Não, salvo Plano B | Bolha com rótulo dentro, para montar do zero (Parte 16) |
| `icone_grande_512.png`, `previa.png`, `gerar.py`, `LEIA-ME.md` | Não | Referência da equipe |

A ordem e o texto de cada resposta estão em `textos.md`, seção 3. O quadro 0 de cada sequência é o arquivo `_01` e o quadro 7 é o `_08`.

### 0.6 Tempo estimado

| Etapa | Tempo |
|---|---|
| Parte 0: baixar e conferir | 10 min |
| Partes 1 e 2: abrir o template e anotar as peças | 25 min |
| Parte 3: testes de proporção e sombra | 15 min |
| Partes 4 e 5: importar, trocar imagens, proporção e tamanho | 50 min |
| Parte 6: desligar a IA do template | 20 min |
| Parte 7: ajustar a lógica | 30 min |
| Parte 8: testar no PC | 45 min |
| Partes 9 e 10: desempenho e vídeo demo | 35 min |
| Partes 12 a 14: conferências, envio e status | 20 min |
| **Total** | **≈ 4 h** (reserve 6 h) |

### 0.7 O que depende do Vini (o mínimo)

Pela ordem da equipe (`ORDEM-PC.md`), o Vini **já deixou o Effect House instalado e logado** na conta Car Shop. Ele só é chamado se:

1. **O login cair** ou o programa estiver logado em outra conta. Mande para ele, com o link:
   > Abra o Effect House no computador. Vai aparecer um QR code. No celular, abra o **TikTok da conta Car Shop** → **Perfil** → ícone de pessoa (**Adicionar amigos**) → ícone de scanner no canto de cima → aponte para o QR → toque em **Confirmar**. Guia com imagens: https://effecthouse.tiktok.com/learn/guides/getting-started/introduction-to-effect-house/download-and-login
   >
   > Tem que ser o scanner **de dentro do TikTok**. A câmera comum do celular não funciona.
2. **O programa não estiver instalado.** Mande: "Baixe e instale por este link: https://effecthouse.tiktok.com/download. Se o computador for Mac, escolha **Apple** (chip M1, M2…) ou **Intel** conforme o menu  → **Sobre este Mac**". Depois, o login do item 1.
3. **O teste no celular** (Parte 11). Ele é **opcional**. Se for feito, junte com os outros efeitos num único momento.

Todo o resto (montar, testar no PC, gravar o vídeo demo e enviar) é feito sem ele.

---

## Parte 1: Abrir o template

1. Abra o **Effect House**.
2. Confira a conta. A foto ou o nome da conta **Car Shop** deve aparecer na tela inicial (a confirmar na sua versão do programa: onde a conta aparece). Se for outra conta, **pare** e siga a seção 0.7.
3. Anote no relatório a versão do programa. Ela costuma estar em **Help → About** ou na tela inicial (a confirmar na sua versão do programa). O esperado é 5.15 ou 5.16.
4. Clique em **Templates**, no menu da esquerda da tela inicial.
5. Clique na aba **Community Creator**. O tutorial oficial diz que o Future Life fica nela. Em outra página da documentação a aba aparece como **Community Center**.
6. Clique no card **Future Life**.
7. Clique em **Create** ou **Open** (a confirmar na sua versão do programa: o nome do botão).
8. Espere o projeto carregar. O programa pode baixar o template, o que leva até 1 minuto.

**Se não achar "Future Life":**
- digite `Future Life` na busca de templates; depois tente `Future`, `Bubble` e `Prediction`;
- olhe nas abas e categorias **Community Creator**, **Community Center**, **Interactive** e **Face**;
- se não achar mesmo, vá para a Parte 16 (Plano B).

9. Clique em **File → Save As**.
10. Crie a pasta `Documentos\Efeitos\projetos\`, se ela não existir.
11. Dê o nome `C05-meu-2027`.
12. Clique em **Salvar**.

> A partir daqui, aperte **Ctrl+S** ao fim de cada parte.

---

## Parte 2: Reconhecer as peças do template

### 2.1 Os painéis

| Painel | Onde costuma ficar | Para quê |
|---|---|---|
| **Hierarchy** | à esquerda, em cima | lista os objetos da cena |
| **Assets** | à esquerda, embaixo | lista os arquivos importados |
| **Inspector** | à direita | mostra as propriedades do que estiver selecionado |
| **Preview** | à direita ou no centro | mostra o efeito num rosto de exemplo |
| **Visual Scripting** | embaixo | mostra a lógica (caixinhas ligadas por fios) |

Se algum painel sumir, procure no menu **Window** (a confirmar na sua versão do programa).

### 2.2 O que procurar na Hierarchy

O tutorial oficial descreve estes grupos. Os nomes dos objetos **dentro** de cada grupo não foram vistos (a confirmar na sua versão do programa).

| Grupo | O que tem dentro (segundo o tutorial) | O que vamos fazer |
|---|---|---|
| **2D Foreground Effects** | o grupo principal, com todas as imagens de tela | nada direto |
| ↳ **Main_Elements** | o título ("My Future Life") e a varinha de bolha | trocar a imagem do título |
| ↳ **Animations** | as 3 imagens animadas de resposta (esquerda, meio, direita) | trocar as sequências |
| ↳ **Bubble** | as 3 bolhas | (opcional) trocar o desenho da bolha |
| ↳ **Bubble_Titles** | os 3 rótulos: Lover, Income, Kids | trocar pelos nossos rótulos |
| **Generative Effects** | os efeitos de IA **Pucker** e **Unhappy** | desligar (Parte 6) |
| **TIPS** | instruções do template sobre como disparar o efeito sem toque | esconder, se aparecer na tela (Parte 5.5) |

1. Clique na setinha ao lado de cada grupo para abrir.
2. Anote no relatório o nome de cada objeto que aparecer dentro de **Main_Elements**, **Animations**, **Bubble**, **Bubble_Titles** e **Generative Effects**.
3. Clique no objeto do título (dentro de **Main_Elements**; pode se chamar **Effect_Title**, **Title** ou parecido).
4. Anote os componentes que aparecem no **Inspector**. O esperado é algo como **Screen Transform** (ou **2D Transform**) e **Image** (a confirmar na sua versão do programa).
5. Anote o **Size** (largura × altura) e o **Stretch Mode**, se existirem.
6. Clique no primeiro objeto de **Animations** e anote as mesmas coisas. Repare **onde está a sequência**: no campo **Texture** do componente **Image** ou num componente **Animation Sequence** (a confirmar na sua versão do programa).
7. Clique no primeiro objeto de **Bubble_Titles** e anote as mesmas coisas.

### 2.3 O que procurar no painel Assets

1. Ache a pasta **DO NOT REMOVE!!! - Main Assets**. **Não clique com o botão direito nela e não arraste nada para dentro ou para fora.**
2. Ache a pasta **Texture_Seq**. O tutorial diz que ela guarda as sequências de resposta de Lover, Income e Kids.
3. Clique em cada uma das 3 sequências originais.
4. Anote no relatório, para cada uma: o nome, o **tamanho** (largura × altura) e o **número de quadros** (frames) que o Inspector mostra.
5. Clique na textura original do título e anote o tamanho.
6. Clique na textura original de um rótulo (Lover, por exemplo) e anote o tamanho.

### 2.4 O que procurar no Visual Scripting

1. Abra o painel **Visual Scripting**.
2. Ache a caixa grande chamada **Color_Picker & Randomizer (Bubble_Input)**. É um **subgraph**, uma caixa que guarda vários nós dentro.
3. Repare no fio que sai do nó **Start** e entra na entrada **For_Colors** dessa caixa. É ele que liga o sorteio de cor. **Não apague esse fio.**
4. Dê **duplo clique** na caixa para ver o que tem dentro.
5. Ache os 3 nós **Animated Texture Player**, um por bolha. Eles podem estar dentro da caixa ou do lado de fora (a confirmar na sua versão do programa).
6. Ache o quadro de comentário **Change Color** (com as cores prontas) e o quadro **Remove these if you use images**.
7. Ache os nós de gatilho: **Screen Tap** (toque) e **Facial Movement Detection** com **Mouth Pout** (biquinho). Anote onde estão.
8. Volte para fora da caixa (botão de voltar ou o caminho no topo do painel; a confirmar na sua versão do programa).

> Se os nomes forem um pouco diferentes, siga com os nomes que existem e anote no relatório.

---

## Parte 3: Dois testes rápidos antes de importar

Eles decidem **qual pasta de imagens** você vai usar. Leva 15 minutos e evita refazer tudo depois.

### 3.1 Proporção das respostas

Use o tamanho das sequências originais que você anotou na Parte 2.3.

| Tamanho das respostas originais | Use |
|---|---|
| Larga, com a largura perto de 4 vezes a altura (ex.: 512×128, 1024×256) | as respostas de 512×128 (versão principal) |
| Quadrada (ex.: 512×512) | `variantes\quadrado_512\` (texto centralizado num quadrado) |
| Outra proporção (ex.: 2:1) | a versão principal, e depois ajuste o objeto na Parte 5.3. Se não der, peça à equipe da nuvem as respostas no tamanho certo (ela gera em minutos com `gerar.py --resposta LxA`). Não chame o Vini. |

O **título** e os **rótulos** seguem a pasta escolhida aqui. Os nossos são 2:1. Se os originais tiverem outra proporção, acerte no próprio objeto (Partes 5.1 e 5.2). Só se não der, importe o título e os rótulos de `variantes\quadrado_512\` (ou `quadrado_512_com_sombra\`, se a Parte 3.2 pedir sombra).

> **Uma regra que não pode ser quebrada:** as 8 respostas de uma mesma bolha têm que vir **da mesma pasta**. Todos os quadros de uma sequência precisam ter o mesmo tamanho.

### 3.2 Sombra (decide se a leitura em fundo claro fica boa)

O branco pintado de amarelo ou ciano some em fundo claro (veja o painel 3 de `previa.png`). A versão `com_sombra` resolve isso **se** o template pintar a imagem por multiplicação, que deixa o preto preto. Este teste mostra isso.

1. No painel **Assets**, clique no botão **+** (**Add**).
2. Clique em **Import**.
3. Clique em **From Computer** (a confirmar na sua versão do programa: pode aparecer como "Texture" ou "Image").
4. Abra `<DOCS>\Efeitos\tiktok-efeitos\efeito-3-meu-2027-vai-ser\assets\variantes\com_sombra\respostas_grana\`.
5. Selecione `grana_06.png`.
6. Clique em **Abrir**.
7. Na **Hierarchy**, clique no objeto do título (Parte 2.2, passo 3).
8. No **Inspector**, no componente **Image**, clique no campo **Texture**.
9. Escolha `grana_06`.
10. Olhe o **Preview**. A frase "TANQUE CHEIO / O ANO TODO" deve aparecer no lugar do título, pintada com uma cor.
11. Olhe a **sombra** em volta das letras e decida pela tabela:

| O que você vê | Conclusão | Use |
|---|---|---|
| Letras coloridas com sombra **escura** | o template multiplica a cor | as versões **com sombra** |
| Letras coloridas com um borrão **da mesma cor** em volta | o template troca a cor inteira | as versões **sem sombra** |
| Letras **brancas** (sem cor) com sombra escura | o título não é pintado. Repita os passos 7 a 11 num objeto de **Bubble_Titles** | decida pelo teste no rótulo |

12. Aperte **Ctrl+Z** até o título voltar à textura original.
13. No painel **Assets**, clique com o botão direito em `grana_06`.
14. Clique em **Delete**.

### 3.3 Escolha da pasta (`<PASTA>`)

| Proporção (3.1) | Com sombra (3.2) | Sem sombra (3.2) |
|---|---|---|
| Larga (4:1) | `assets\variantes\com_sombra\` | `assets\` (principal) |
| Quadrada | `assets\variantes\quadrado_512_com_sombra\` | `assets\variantes\quadrado_512\` |

As 4 pastas têm a mesma estrutura: `titulo.png`, `bolha_amor.png`, `bolha_grana.png`, `bolha_futebol.png`, `respostas_amor\`, `respostas_grana\`, `respostas_futebol\` (e as de carro e reservas).

Anote no relatório a pasta escolhida.

---

## Parte 4: Importar as imagens

### 4.1 Título e rótulos

1. No painel **Assets**, clique em **+** (**Add**).
2. Clique em **Import**.
3. Clique em **From Computer**.
4. Abra a `<PASTA>` escolhida na Parte 3.3.
5. Clique em `titulo.png`.
6. Segure **Ctrl** e clique em `bolha_amor.png`, `bolha_grana.png` e `bolha_futebol.png`.
7. Clique em **Abrir**.
8. Confira se `titulo`, `bolha_amor`, `bolha_grana` e `bolha_futebol` apareceram no painel **Assets**.

### 4.2 As 3 sequências de respostas

Cada bolha tem a sua sequência. As respostas **não** entram como imagens soltas.

1. No painel **Assets**, clique em **+** (**Add**).
2. Clique em **Import**.
3. Clique em **Texture Sequence** (a confirmar na sua versão do programa; se não existir, veja a primeira linha da Parte 15).
4. Abra a pasta `<PASTA>\respostas_amor\`.
5. Faça o que a janela pedir (a confirmar na sua versão do programa):
   - se ela pedir **arquivos**: aperte **Ctrl+A** para selecionar os 8 PNG e clique em **Abrir**;
   - se ela pedir **uma pasta**: selecione a pasta `respostas_amor` e clique em **Selecionar pasta**.
6. Confira se apareceu **uma** sequência nova no painel Assets.
7. Clique nela.
8. Confira no **Inspector** se ela tem **8 frames** (quadros).
9. Clique com o botão direito na sequência.
10. Clique em **Rename**.
11. Digite `seq_amor`.
12. Repita os passos 1 a 11 com a pasta `respostas_grana` (nome `seq_grana`) e com a pasta `respostas_futebol` (nome `seq_futebol`).

> **A ordem tem que estar certa.** Os nomes têm zero na frente (01, 02 … 08), então a ordem alfabética já é a certa. Se o Inspector mostrar outra ordem ou outro número de quadros, apague a sequência e importe de novo.

### 4.3 Compressão

1. Clique em `titulo` no painel Assets.
2. Confira a compressão no **Inspector**. Deixe **Automatic** ou **Manual → 512 → High**. Para o título, se houver a opção **1024 → High**, use-a: ele tem 1024 px de largura.
3. Faça o mesmo com os 3 rótulos e as 3 sequências (512 → High).

> **Não** use Medium nem Low. As artes deste efeito são leves (a versão com sombra inteira tem cerca de 1 MB).

---

## Parte 5: Trocar as imagens do template

### 5.1 Título

1. Na **Hierarchy**, clique no objeto do título (em **Main_Elements**).
2. No **Inspector**, no componente **Image**, clique no campo **Texture**.
3. Escolha `titulo`. Também dá para arrastar `titulo` do painel Assets para o campo.
4. Confira a **proporção**. O nosso título é 2:1 (largura = 2 × altura). As estrelinhas de 4 pontas têm que parecer simétricas, sem achatar:

| O que o Size do objeto mostra | O que fazer |
|---|---|
| Largura = 2 × altura | Nada. |
| Outra proporção | Mude a **altura** para metade da largura. Se houver **Stretch Mode**, use **Fit** em vez de mudar o Size. |

5. Confira no **Preview** se "MEU 2027 / VAI SER…" aparece inteiro, sem corte nas reticências.
6. **Não mexa** na posição do título. O template já o deixa no lugar certo. Só baixe um pouco o **Position Y** se ele ficar cortado no topo da tela.

### 5.2 Rótulos das bolhas

1. Na **Hierarchy**, abra **Bubble_Titles**.
2. Clique no rótulo **Lover** (bolha da esquerda).
3. No **Inspector**, troque a **Texture** do componente **Image** por `bolha_amor`.
4. Clique no rótulo **Income** (bolha do meio).
5. Troque a **Texture** por `bolha_grana`.
6. Clique no rótulo **Kids** (bolha da direita).
7. Troque a **Texture** por `bolha_futebol`.
8. Confira a proporção de cada um (2:1), como na Parte 5.1. **Régua:** a moeda de GRANA e a bola de FUTEBOL são círculos. Se parecerem ovos, a imagem está esticada.
9. Confira no **Preview** se as palavras AMOR, GRANA e FUTEBOL cabem dentro das bolhas. Se FUTEBOL encostar na borda da bolha, diminua o **Scale** dos 3 rótulos igualmente (X e Y juntos), por exemplo em 10%.

> Se o ícone deixar o rótulo apertado demais, use os rótulos de `variantes\rotulos_sem_icone\` (mesmo tamanho, só a palavra) e anote no relatório.

### 5.3 Objetos de resposta

1. Na **Hierarchy**, abra **Animations**.
2. Clique no objeto de resposta da **esquerda** (bolha Lover/AMOR).
3. Siga o que você anotou na Parte 2.2, passo 6:
   - se a sequência estiver no campo **Texture** do componente **Image**: troque por `seq_amor`;
   - se houver um componente **Animation Sequence**: troque o campo da sequência dele por `seq_amor` e **não mexa** no Texture do Image.
4. Repita com o objeto do **meio** (`seq_grana`) e o da **direita** (`seq_futebol`).
5. Confira a **proporção** das respostas: a nossa é **4:1** (largura = 4 × altura) na versão principal, ou 1:1 na quadrada.
   - Se o objeto tiver outra proporção, mude a altura para largura ÷ 4 (ou use **Stretch Mode → Fit**).
   - **Régua:** o "O" de "SOGRA TE ADORA" e o "º" de "13º" têm que ser redondos.
6. Confira o **tamanho**: a resposta deve ocupar cerca de 85% a 90% da largura de dentro da bolha. Se ficar maior, diminua o **Scale** (X e Y juntos). Se ficar bem menor, aumente.
7. Use o mesmo Scale nos 3 objetos de resposta.

> A troca definitiva da sequência é feita no nó **Animated Texture Player** (Parte 7.2). Fazer também aqui garante que nenhuma resposta antiga apareça em nenhum momento.
>
> **Para ver uma resposta parada durante o ajuste:** clique no Preview para estourar as bolhas (Parte 8) e ajuste com calma.

### 5.4 Nosso desenho de bolha (recomendado, se funcionar)

O Future Life é usado por muitos criadores. Trocar o desenho da bolha deixa o efeito com cara própria e diminui o risco de reprovação por "parecido com template". **Só vale se der para trocar sem mexer na pasta "DO NOT REMOVE!!! - Main Assets".** Aqui mudamos o objeto da cena, não a pasta.

1. Aperte **Ctrl+S** antes de começar.
2. Importe `assets\variantes\bolha_inteira\bolha_vazia.png` (como na Parte 4.1).
3. Na **Hierarchy**, abra o grupo **Bubble**.
4. Clique na bolha da esquerda.
5. Olhe o componente **Image**:
   - se o campo **Texture** mostrar uma **imagem parada** da bolha: troque por `bolha_vazia`;
   - se mostrar uma **sequência** ou um componente de animação: **pare aqui** e não troque. A animação de estouro do template depende dela.
6. Repita nas outras 2 bolhas.
7. Confira a proporção: a nossa bolha é **quadrada** (1:1). O aro tem que ser um círculo.
8. Teste no **Preview** (clique para estourar). Depois reinicie o Preview e estoure de novo, pelo menos 2 vezes. Confira se:
   - as bolhas aparecem com o nosso desenho e com a cor sorteada, também depois de reiniciar;
   - a bolha antiga não volta sozinha em nenhum momento;
   - o estouro continua acontecendo;
   - rótulo e resposta continuam legíveis dentro da bolha.
9. Se algo ficou estranho (bolha antiga aparecendo junto, estouro sumiu, bolha cortada), feche o projeto **sem salvar** e abra de novo. Anote no relatório "bolha própria: não deu".
10. Se deu certo, aperte **Ctrl+S** e anote no relatório "bolha própria: sim".

> **Não use** os arquivos `bolha_inteira_<bolha>.png` aqui. Eles já têm o rótulo dentro e duplicariam o texto dos rótulos.

### 5.5 Grupo TIPS

O tutorial diz que o grupo **TIPS** explica como disparar o efeito sem tocar na tela. É uma instrução para quem monta e não deve aparecer na câmera.

1. Na **Hierarchy**, clique no grupo **TIPS**.
2. Olhe o **Preview**. Se aparecer algum texto ou imagem em inglês que não seja do efeito, desmarque a **caixinha** ao lado do nome do grupo (desliga sem apagar).
3. Leia o que ele diz e anote no relatório. Ele pode ensinar a testar o biquinho no Preview (pela câmera do computador).

### 5.6 Limpar as imagens antigas do template

1. No painel **Assets**, ache o título original ("My Future Life"), os 3 rótulos originais (Lover, Income, Kids) e as 3 sequências originais (em **Texture_Seq**).
2. Clique com o botão direito em cada um.
3. Clique em **Delete**.
4. Se o programa avisar que o asset ainda está em uso, **cancele**: alguma troca das Partes 5.1 a 5.3 ou 7.2 não foi feita. Faça a Parte 7 primeiro e volte aqui depois.
5. **Nunca** apague nada de dentro de **DO NOT REMOVE!!! - Main Assets**.

---

## Parte 6: Desligar a IA do template (obrigatório)

O grupo **Generative Effects** tem dois efeitos de IA generativa: **Pucker** e **Unhappy**. Pelos nomes, o primeiro faz biquinho no rosto e o segundo deixa o rosto triste (a confirmar na Parte 6.1). Os motivos para desligar estão no começo do guia. Em resumo: peso, regra de "AI" no nome, programa de recompensas e tom das previsões.

O biquinho que **dispara** o efeito não depende deles. Quem detecta o biquinho é o nó **Facial Movement Detection** (opção **Mouth Pout**), que é rastreamento de rosto comum.

### 6.1 Ver o que eles fazem (2 min)

1. No **Preview**, clique para estourar as bolhas.
2. Observe o **rosto** de exemplo antes, durante e depois do estouro.
3. Anote no relatório se a boca vira biquinho sozinha e se o rosto fica triste no final.

### 6.2 Desligar sem apagar (primeira tentativa)

1. Aperte **Ctrl+S**.
2. Na **Hierarchy**, abra o grupo **Generative Effects**.
3. Clique no objeto **Pucker**.
4. No **Inspector**, ache o componente de IA (provavelmente **Generative Effects**; a confirmar na sua versão do programa).
5. Desmarque a **caixinha** no cabeçalho desse componente.
6. Desmarque também a **caixinha** ao lado do nome do objeto **Pucker**, na Hierarchy.
7. Repita os passos 3 a 6 com o objeto **Unhappy**.
8. No **Preview**, reinicie o efeito (a confirmar na sua versão do programa: botão de **reset/refresh** do Preview).
9. Clique para estourar as bolhas.
10. Confira:
    - [ ] as bolhas continuam subindo e estourando;
    - [ ] as respostas aparecem;
    - [ ] o rosto **não** muda (sem biquinho falso, sem cara triste).
11. Se as 3 caixas estão marcadas, siga para a 6.3.
12. Se o rosto **ainda muda**, a lógica do template está religando a IA. Vá para a 6.3 mesmo assim: apagar resolve.
13. Se as bolhas **pararam de funcionar**, aperte **Ctrl+Z** até voltar e vá para a 6.4.

### 6.3 Apagar de vez (para a IA não ir no pacote)

Desligado, o modelo de IA pode continuar dentro do pacote, pesando e marcando o efeito como "de IA". Por isso, se possível, apague.

1. Aperte **Ctrl+S**.
2. Na **Hierarchy**, clique com o botão direito em **Pucker**.
3. Clique em **Delete**.
4. Faça o mesmo com **Unhappy**.
5. Se o grupo **Generative Effects** ficar vazio, apague o grupo também.
6. Abra o painel **Visual Scripting** e procure nós com **aviso vermelho** ou campo **Target** vazio (a confirmar na sua versão do programa: como o programa mostra referência perdida). Olhe também dentro da caixa **Color_Picker & Randomizer (Bubble_Input)**.
7. Para cada nó com problema que só servia à IA (por exemplo, um **Set Visibility** com Target vazio):
   1. Ache o fio que **entra** nele (do nó anterior).
   2. Ache o fio que **sai** dele (para o nó seguinte).
   3. Arraste da saída do nó anterior até a entrada do nó seguinte, para pular o nó.
   4. Clique no nó com problema.
   5. Aperte **Delete**.
8. Abra o painel **Console** ou **Logger**, se existir (a confirmar na sua versão do programa), e veja se há erros em vermelho.
9. Repita o teste da 6.2 (passos 8 a 10).
10. Se tudo passou, aperte **Ctrl+S** e anote no relatório "IA apagada".
11. Se algo quebrou e você não conseguiu consertar em 15 minutos, feche **sem salvar**, abra de novo (fica a versão da 6.2) e anote "IA só desligada".

### 6.4 Se nada funcionar sem a IA

1. Tente o **Pedido 2** de `script\prompt-effect-house-ai.md` no assistente Effect House AI (Parte 16.3).
2. Se continuar sem jeito, **não envie** o efeito. Avise a equipe da nuvem: com IA, o nome teria que levar "AI", o efeito pode não render no programa de recompensas e pode reprovar por desempenho. Ela decide entre o Plano B (Parte 16.1) e seguir assim.

---

## Parte 7: A lógica (Visual Scripting)

**O template já faz quase tudo.** Não crie nós novos. Só troque as sequências e confira o número de respostas do sorteio.

### 7.1 Abrir a caixa do sorteio

1. Abra o painel **Visual Scripting**.
2. Dê **duplo clique** na caixa **Color_Picker & Randomizer (Bubble_Input)**.

### 7.2 Trocar as sequências nos 3 nós Animated Texture Player

O tutorial oficial manda trocar o campo **Animated Texture** de cada um dos 3 nós.

1. Clique no primeiro nó **Animated Texture Player**.
2. Veja qual sequência ele usa hoje (no próprio nó ou no Inspector). O nome indica a bolha: Lover, Income ou Kids.
3. Troque o campo **Animated Texture** pela nossa sequência da mesma bolha:

| Sequência original | Bolha | Troque por |
|---|---|---|
| Lover | esquerda | `seq_amor` |
| Income | meio | `seq_grana` |
| Kids | direita | `seq_futebol` |

4. Repita nos outros 2 nós.
5. Procure **outros nós** que ainda apontem para as sequências antigas, por exemplo **Set Animated Texture**, **Animated Texture Info** ou **Get Asset**. Troque também.

> Se o nome da sequência original não deixar claro qual é a bolha, siga o fio do nó até o objeto que ele controla (em **Animations**) e veja a posição do objeto: esquerda, meio ou direita.

### 7.3 Número de respostas no sorteio (o passo mais importante desta parte)

As sequências originais tinham um número de quadros (anotado na Parte 2.3). As nossas têm **8**. Se o sorteio ainda usar o número antigo, algumas respostas nunca aparecem, ou aparece um quadro vazio.

Para cada um dos 3 nós **Animated Texture Player**, veja o que chega nas entradas **From** e **To**:

| O que chega em From e To | O que fazer |
|---|---|
| Um nó **Animated Texture Info** (com o total de quadros, às vezes menos 1) | Nada. Ele lê sozinho os 8 quadros da nova sequência. Só confira se ele aponta para a nossa sequência (7.2, passo 5). |
| Um nó **Random** (ou **Generate Random Number**) com **Min** e **Max**, às vezes seguido de **Floor** ou **Round** | Use a **regra do original** logo abaixo. |
| Números fixos (ex.: From = 0, To = 4), com a ordem sorteada por um nó **Set Animated Texture** (Order = **Random** ou **Shuffle**) | Mude o **To** para **7** e deixe From = **0**. Não mexa em Order, FPS nem Loop. |
| Outra coisa | Anote no relatório e use o Pedido 1 de `script\prompt-effect-house-ai.md`. Se não resolver, Plano C (Parte 16.2). |

**Regra do original (para o nó Random):** compare o **Max** original com o número de quadros original.
- Se o **Max original = quadros − 1** (ex.: 5 quadros e Max 4), o Max conta o último quadro. Ponha **Max = 7**.
- Se o **Max original = quadros** (ex.: 5 quadros e Max 5), o Max fica de fora. Ponha **Max = 8**.
- **Min** fica **0** nos dois casos.

> Os quadros começam em 0: o quadro 0 é o arquivo `_01` e o quadro 7 é o `_08`.
>
> **Cuidado:** o nó **Random** sorteia um número **novo cada vez que é lido**. Se o mesmo Random estiver ligado direto em From **e** em To, pode dar 2 números diferentes. O template deve tratar isso. Se no teste (Parte 8.3) aparecerem respostas "andando" ou trocando sozinhas, anote no relatório e use o Plano C (Parte 16.2).

### 7.4 Cores

1. **Não apague** o fio **Start → For_Colors**: é ele que pinta as artes a cada abertura.
2. **Não apague** os nós do quadro **Remove these if you use images**. Esse quadro é para quem usa fotos coloridas. As nossas respostas são texto branco e precisam ser pintadas.
3. **Só se** você estiver usando a versão **sem sombra** e o teste de leitura (Parte 8.4) mostrar resposta ilegível com alguma cor clara (amarelo-claro, ciano, branco), troque **essa** cor no quadro **Change Color** por uma destas:

| Cor | Código |
|---|---|
| rosa forte | `#E0245E` |
| roxo | `#7B2FF7` |
| laranja | `#FF6B00` |
| azul | `#0077FF` |
| verde | `#00A86B` |

   Para trocar: clique no nó de cor dentro do quadro **Change Color**, clique no quadradinho de cor e digite o código (a confirmar na sua versão do programa: como o seletor de cor aceita o código).

### 7.5 Gatilhos

1. Confira se existe o nó **Screen Tap** ligado à lógica das bolhas. **Não mude.**
2. Confira se existe o nó **Facial Movement Detection** com **Facial Movement = Mouth Pout**. **Não mude.**
3. Anote no relatório os valores que aparecerem neles.
4. Volte para fora da caixa.
5. Aperte **Ctrl+S**.

### Sobre script em código

**Este efeito não precisa de código.** Mesmo assim, a equipe deixou um script em TypeScript (`script\SorteioRespostas2027.ts`) que só faz o sorteio das respostas, para o caso de a Parte 7.3 não dar certo. Ele passou na checagem de tipos, feita com os arquivos de tipos da API do Effect House tirados de um projeto público, e num teste de lógica fora do programa, mas **ainda não foi rodado dentro do programa** (a confirmar). Como usar: Parte 16.2.

---

## Parte 8: Testar no PC

### 8.1 Como testar no Preview

- Clicar com o mouse **dentro da imagem do Preview** simula o toque na tela.
- Para testar o **biquinho**, clique no botão de **câmera** do painel Preview (usa a webcam do PC) e faça biquinho para a câmera. É o que o grupo TIPS do template ensina. Se o PC não tiver webcam, pule o teste do biquinho e veja a Parte 13 (campo Hint).
- Para recomeçar do zero (bolhas fechadas e cor nova), reinicie o Preview (a confirmar na sua versão do programa: botão de **reset/refresh**).

### 8.2 Checklist (marque tudo antes de seguir)

**Antes do toque**
- [ ] Aparece o título **"MEU 2027 / VAI SER…"**, inteiro, com as reticências. Nenhum "My Future Life".
- [ ] Aparecem 3 bolhas: **AMOR** (esquerda), **GRANA** (meio), **FUTEBOL** (direita). Nenhum "Lover", "Income" ou "Kids".
- [ ] Título e rótulos estão **pintados** com a cor sorteada (não branco puro), salvo decisão diferente na Parte 3.2.
- [ ] Moeda e bola dos rótulos estão **redondas** (nada esticado).
- [ ] Nada em inglês do template aparece na tela (grupo TIPS escondido, se for o caso).
- [ ] Não aparece **borda escura** nem quadrado em volta das artes.

**Depois do toque**
- [ ] As bolhas **estouram** e cada uma mostra **uma** resposta.
- [ ] Cada resposta é **do tema da bolha** (resposta de amor na bolha AMOR, de grana na GRANA, de futebol na FUTEBOL).
- [ ] As **2 linhas** da resposta aparecem inteiras, sem corte, com acentos visíveis (Ã, Ç, É, Í, Ú, º).
- [ ] Nenhuma resposta original do template aparece (por exemplo "No One", "$-10K" ou "0").
- [ ] A resposta fica **parada** (não fica trocando sozinha).
- [ ] O **rosto não muda** (IA desligada, Parte 6).
- [ ] Anote o que acontece num **segundo toque** depois do resultado (sorteia de novo, recomeça ou nada). Qualquer um é aceitável.

**Biquinho (se houver webcam)**
- [ ] O biquinho dispara o efeito como o toque.
- [ ] Um biquinho comprido não fica trocando as respostas sem parar.

**Telas do TikTok**
- [ ] Título e bolhas não ficam escondidos atrás dos botões do TikTok (botão "Adicionar som" em cima, ferramentas à direita). Se o Preview tiver opção de mostrar a interface do TikTok, ligue para conferir (a confirmar na sua versão do programa). Se ficar escondido, baixe o título e as bolhas juntos, um pouco, pelo **Position Y**.

### 8.3 Teste do sorteio (importante)

Este teste mostra se as 8 respostas de cada bolha entram no sorteio.

1. Reinicie o Preview.
2. Clique para estourar.
3. Anote as 3 respostas (AMOR, GRANA, FUTEBOL).
4. Repita os passos 1 a 3 até ter **24 rodadas**. Se um segundo toque já sorteia de novo (Parte 8.2), basta clicar de novo, sem reiniciar.
5. Avalie **cada bolha**:
   - **OK** se: nunca apareceu bolha vazia; saíram **pelo menos 6 respostas diferentes** das 8; e a **8ª resposta** (a última, tabela abaixo) saiu pelo menos uma vez.
   - Se só faltou a 8ª: faça **mais 16 rodadas** (40 no total). Se ela sair, está OK.
   - **Problema** se: apareceu bolha vazia, saíram 5 ou menos respostas diferentes, ou a 8ª não saiu nem em 40 rodadas.

| Bolha | 8ª resposta (quadro 7, a última) |
|---|---|
| AMOR | AMOR DA VIDA / (DE NOVO) |
| GRANA | ACHA GRANA / NA CALÇA |
| FUTEBOL | BUZINAÇO / DE CAMPEÃO |

> Por que a última: se o sorteio ainda usar o número antigo de quadros, é ela que nunca aparece. Com um sorteio justo entre 8, em 24 rodadas saem em média 7 ou 8 respostas diferentes. A chance de reprovar por azar é de cerca de 1 em 200 por bolha.

**Se der problema:**
- **Bolha vazia** → o Max está alto demais. Diminua 1 no Max (Parte 7.3) e repita o teste.
- **A 8ª nunca sai** → o sorteio ainda usa o número antigo de quadros. Refaça a Parte 7.3.
- **Sai sempre a mesma** ou numa ordem fixa (01, 02, 03…) → procure um nó **Set Animated Texture** e confira se **Order** está em **Random** ou **Shuffle**. Se não resolver, Plano C (Parte 16.2).
- **De vez em quando volta para a 1ª resposta** sozinha → é um defeito relatado no fórum oficial com o Animated Texture Player. Use o Plano C (Parte 16.2).

6. Anote no relatório o resultado das rodadas.

### 8.4 Teste de leitura no pior caso

1. No **Preview**, escolha uma mídia de exemplo com **fundo claro**, se houver (a confirmar na sua versão do programa: quais mídias aparecem).
2. Reinicie o Preview várias vezes, até sair uma cor **clara** (amarela ou ciano), se o template tiver.
3. Estoure as bolhas.
4. Confira se dá para ler, na tela inteira do Preview, estas respostas (as mais longas): **SOFRE ATÉ A / ÚLTIMA RODADA**, **O EX VOLTA / (NÃO ATENDE)**, **NAMORO SÉRIO / (3 SEMANAS)** e **O 13º DURA / ATÉ O DIA 3**. Se não saírem por sorteio, confira as que saírem.
5. Se ficar ilegível:
   - na versão **sem sombra**: troque as cores claras (Parte 7.4, passo 3);
   - na versão **com sombra**: aumente o **Scale** das 3 respostas em 10% (X e Y juntos), se ainda couberem na bolha.
6. Aperte **Ctrl+S**.

---

## Parte 9: Desempenho e tamanho

1. Na barra de cima, ache o indicador de tamanho do efeito.
2. Clique em **Click to update** para atualizar o número.
3. Anote o tamanho no relatório. As nossas artes somam cerca de **0,4 MB** (sem sombra) ou **1 MB** (com sombra). O resto é do template e não foi medido (a confirmar).
   - **Até 5 MB:** ótimo.
   - **Entre 5 e 8 MB:** aceitável (o limite é 8 MB). Confira se a IA foi mesmo apagada (Parte 6.3) e se as texturas antigas foram apagadas (Parte 5.6).
   - **Acima de 8 MB:** não dá para enviar. Faça as conferências acima.
4. Na barra de cima, clique em **Test performance**.
5. Clique em **Run test**.
6. Espere cerca de 30 segundos.
7. Se passar, siga para a Parte 10.
8. Se falhar, clique em **View suggestions** e veja a Parte 15. A causa mais provável é a IA do template ainda ligada.

> Passar no Test performance **não garante** a aprovação, mas falhar nele quase garante a reprovação.

---

## Parte 10: Vídeo demo (sem precisar do Vini)

O formulário pede um vídeo curto mostrando o efeito. Só a equipe de revisão vê, ele não é público. Regras: **9:16 (em pé), MP4 ou MOV, até 15 segundos, até 32 MB.**

### 10.1 Gravar no próprio Effect House

1. No **Preview**, escolha um aparelho com tela **9:16** na lista de aparelhos (costuma ficar embaixo, à esquerda). Um exemplo é o iPhone 8 ou um aparelho de 1080×1920. Telas mais compridas, como as do iPhone X em diante, não são 9:16 (a confirmar na sua versão do programa: quais aparelhos aparecem).
2. Escolha o rosto de exemplo em que o efeito ficou melhor, de preferência em vídeo.
3. Reinicie o efeito, com as bolhas fechadas.
4. Clique em **Screen record** no painel Preview (a confirmar na sua versão do programa: o nome e o lugar do botão).
5. Siga o roteiro abaixo.
6. Pare a gravação antes de 15 segundos.
7. Salve em `Documentos\Efeitos\videos-demo\C05-demo-bruto.mp4`.

**Roteiro do vídeo (até 14 s):**

| Tempo | O que acontece |
|---|---|
| 0–2 s | Título e 3 bolhas fechadas |
| ≈ 2 s | Clique no Preview (ou biquinho na webcam) |
| 2–4 s | Bolhas estouram |
| 4–8 s | As 3 respostas paradas, com o rosto se mexendo um pouco |
| ≈ 8 s | Clique de novo, se o template sortear de novo. Se não, reinicie o Preview e clique |
| 8–14 s | Segunda rodada de respostas |

> Se der, faça a segunda rodada com uma resposta de futebol bem clara, como "TÍTULO VEM (CONFIA)". Não é obrigatório: o sorteio é sorteio.

### 10.2 Conferir o formato

1. No Explorador de Arquivos, clique com o botão direito no vídeo.
2. Clique em **Propriedades**.
3. Abra a aba **Detalhes**.
4. Confira **Largura** e **Altura**. O vídeo tem que estar em pé e em 9:16, por exemplo 1080×1920 ou 720×1280 (largura ÷ altura = 0,5625).
5. Confira a **Duração**: no máximo 15 s.

### 10.3 Se não estiver em 9:16 (só o Montador)

1. Instale o ffmpeg pelo PowerShell: `winget install --id Gyan.FFmpeg -e`
   (sem winget, baixe em https://www.gyan.dev/ffmpeg/builds/ e use o `ffmpeg.exe` da pasta `bin`).
2. Feche e abra o PowerShell de novo.
3. Rode, na pasta do vídeo:

```powershell
ffmpeg -i C05-demo-bruto.mp4 -t 15 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" -c:v libx264 -pix_fmt yuv420p -an C05-demo.mp4
```

O comando corta para 9:16 pelo centro, limita a 15 s e **tira o áudio**, para não levar música junto.

4. Abra o `C05-demo.mp4`.
5. Confira se o título e as 3 bolhas continuam inteiros na imagem. As bolhas laterais ficam perto das bordas: se o corte pegar uma delas, grave de novo com um aparelho 9:16 no Preview.

> Se o Preview não tiver **Screen record**, grave a janela do Preview com a Ferramenta de Captura do Windows (**Win+Shift+R**; a confirmar se existe na versão do Windows do PC) e passe o vídeo pelo comando acima.

---

## Parte 11: Teste no celular (opcional, depende do Vini)

É o teste mais fiel, e o único que confirma o **biquinho** quando o PC não tem webcam. Precisa de um celular logado na conta **Car Shop**. **Pule esta parte** se o Vini não estiver disponível.

Se for fazer, junte com os outros efeitos num único momento com o Vini.

1. No Effect House, clique em **Preview in TikTok**, na barra de cima (a confirmar na sua versão do programa: o lugar do botão).
2. Espere o QR code aparecer.
3. O Vini abre o **TikTok da conta Car Shop** no celular.
4. Ele toca em **Perfil**.
5. Ele toca no ícone de pessoa (**Adicionar amigos**).
6. Ele toca no ícone de **scanner**, no canto de cima.
7. Ele aponta para o QR da tela.
8. O efeito abre na câmera do TikTok.

> A dica ("Faça biquinho") do formulário **não aparece** no teste pelo celular. Isso é normal.
> Uma versão do guia oficial diz que o QR vale 14 dias ou até 30 contas. Se for verdade, outra conta também pode testar (a confirmar).

**Checklist no celular:**
- [ ] O biquinho dispara o efeito.
- [ ] O toque também dispara. Em alguns Android o toque falha no teste; se falhar, tente outro aparelho antes de mexer no efeito.
- [ ] Dá para ler as respostas com o braço esticado.
- [ ] Os botões do TikTok não escondem o título nem as bolhas.
- [ ] O rosto não muda sozinho (nada de IA).
- [ ] Anote o que acontece ao apertar **gravar**: o efeito recomeça ou continua.

---

## Parte 12: Conferências antes de enviar

### 12.1 Conta

1. Confira de novo se o Effect House está logado na conta **Car Shop**. O efeito e o dinheiro do programa de recompensas ficam com a conta que envia.

### 12.2 Conteúdo

1. Confira se nada do template em inglês sobrou na tela: "My Future Life", "Lover", "Income", "Kids" e as respostas originais.
2. Confira se o grupo **Generative Effects** foi apagado (ou, no mínimo, desligado). Anote qual dos dois.
3. Confira se nenhuma imagem tem nome de time, escudo, marca, @ da conta, link ou chamada para comprar. As imagens da equipe já seguem essa regra.
4. **Não adicione** música nem som da biblioteca do TikTok. Se o template já tiver um som próprio curto (por exemplo, de bolha estourando), pode manter (a confirmar se existe) e anote no relatório.

### 12.3 Projeto salvo

1. Aperte **Ctrl+S**.
2. Copie a pasta do projeto `C05-meu-2027` para `Documentos\Efeitos\projetos\backup\`, como garantia.

### 12.4 Data

1. Confira a data de envio (Parte 0.2). Se ainda não for a hora, pare aqui e anote no relatório "C05 pronto, aguardando data".
2. Se a equipe marcou o C05 como **situação A**, abra a aba **Rewards** do Effect House e confira se a inscrição no programa aparece aprovada. Se não aparecer, **não envie**: anote "C05 aguardando admissão" e avise a equipe da nuvem.

---

## Parte 13: Enviar para aprovação

### 13.1 Abrir o formulário

1. Clique em **Submit**, no canto de cima à direita.
2. Espere abrir o formulário de envio. Ele é uma página web dentro de uma janela.

> Se o formulário abrir no navegador e pedir login no TikTok, chame o Vini (seção 0.7). A página de login por QR é https://www.tiktok.com/login/qrcode, e ele escaneia com o scanner do TikTok, como na seção 0.7. Não está confirmado se isso acontece.

### 13.2 O que preencher

| Campo | Obrigatório? | O que colocar |
|---|---|---|
| **Effect name** (nome) | Sim | `Meu 2027 vai ser` (16 caracteres; o limite é 25). **Sem reticências.** Se recusar por nome repetido, use `Estoura meu 2027` (16); se recusar de novo, `Bolhas de 2027` (14). **Não** coloque "AI" no nome: a IA do template foi tirada (Parte 6). |
| **Effect icon** (ícone) | Sim | `assets\icone_162.png`. Se houver espaço para um 2º ícone, `assets\icone_alt_162.png`. |
| **Category** (categoria) | Sim | Escolha nesta ordem: uma opção parecida com **Funny** (engraçado); se não houver, **Randomizer** (sorteio); se não houver, **Interactive**. Anote no relatório a lista que apareceu. |
| **Hint** (dica) | Não, mas preencha | Veja a regra logo abaixo da tabela. |
| **Description** (descrição), se existir | — | `Faça biquinho e veja como vai ser o seu 2027 no amor, na grana e no futebol.` (76 caracteres). Se couber texto maior, use o texto em português dos comentários abaixo. |
| **Tags** | Não, mas preencha | `2027`, `previsão`, `ano novo`, `réveillon`, `sorteio`. Se não aceitar acento ou espaço: `2027`, `previsao`, `anonovo`, `reveillon`, `sorteio`. Se só aceitar inglês: `2027`, `prediction`, `new year`, `randomizer`, `funny`. Máximo de 5. |
| **Demo video** | Mande sempre | `Documentos\Efeitos\videos-demo\C05-demo.mp4` (ou o bruto, se ele já estava em 9:16) |
| **Challenge** (desafio) | Não | Deixe vazio. Se aparecer um desafio ativo de Ano Novo, 2027 ou previsão, anote o nome no relatório para a equipe avaliar. |
| **Comentários para a revisão** (pode se chamar "Additional comments" ou "Notes"; a confirmar) | Se existir | Cole o texto abaixo. |
| **Som / música** (se aparecer opção de ligar um som ao efeito) | Não | **Não ligue nenhum som.** |
| Qualquer outro campo que não esteja aqui | — | Deixe o padrão e anote no relatório. |

**Regra do Hint:**
- Se o biquinho foi testado e funcionou (webcam na Parte 8 ou celular na Parte 11) e o campo for **texto livre**: `Faça biquinho`. Se aceitar frase maior: `Faça biquinho ou toque`.
- Se o campo for **lista pronta**: escolha a opção de biquinho, se existir (algo como **Pout**); se não existir, a de tocar na tela (algo como **Tap screen**).
- Se o biquinho **não** foi testado ou falhou: `Toque na tela` (ou a opção de tocar, na lista). O toque foi testado no Preview.

**Texto para os comentários.** Cole os dois, primeiro o inglês. O texto é o do `textos.md`, com um ajuste: a animação das bolhas vem do template, então não dá para dizer que toda a arte é nossa.

> 2027 New Year prediction with bubbles. Tap the screen or pout, and the LOVE, MONEY and FOOTBALL bubbles pop with a random prediction in Brazilian Portuguese, such as "the title is coming (trust me)" or "my year-end bonus lasts until the 3rd". 24 original, light-humor texts, with our own title, label and icon art; the bubble animation comes from the Future Life template. No generative AI. No teams, crests, kits, brands, betting or real people.
>
> Previsão de 2027 em bolhas. A pessoa toca na tela ou faz biquinho e as bolhas de amor, grana e futebol estouram com uma previsão sorteada, tipo "título vem (confia)" ou "o 13º dura até o dia 3". São 24 frases originais de humor leve, com título, rótulos e ícone feitos por nós; a animação das bolhas é do template Future Life. Sem IA generativa, time, marca, aposta ou pessoa real.

> Se a IA ficou **só desligada** (Parte 6.3, passo 11), troque "No generative AI." por "The template's generative effects are disabled and never run." e "Sem IA generativa, time, marca…" por "Os efeitos de IA do template estão desligados. Sem time, marca…".
> Se a IA do template **não** pôde ser tirada (Parte 6.4), **não envie**: avise a equipe da nuvem.
> Se usou a 4ª bolha ou a troca por CARRO (Parte 17), use os textos ajustados de lá.

### 13.3 Enviar

1. Revise o nome: sem reticências e sem espaço sobrando no começo ou no fim.
2. Confira se o ícone aparece com os cantos arredondados (o site faz isso sozinho).
3. Clique em **Submit** (ou **Enviar**).
4. Tire um print da tela de confirmação.
5. Salve o print em `Documentos\Efeitos\prints\C05-enviado.png`.

---

## Parte 14: Acompanhar o status

1. Abra a área **Manage Effects**, no Effect House ou no site https://effecthouse.tiktok.com/ com a conta logada (a confirmar na sua versão do programa: o caminho exato).
2. Ache o efeito pelo nome enviado.
3. Leia o status:

| Status | O que significa | O que fazer |
|---|---|---|
| **Draft** | Rascunho; o envio não terminou | Clique em **Finish submission** e termine. |
| **Under review** | Em análise (de 1 a 3 dias úteis) | Esperar. Conferir 1 vez por dia. |
| **Needs revision** | Reprovado, com motivo | Clique no status, leia o motivo, corrija (Parte 15) e reenvie. |
| **Active** | Aprovado e no ar | Anote a data no relatório e avise a equipe da nuvem para o vídeo de lançamento (legendas prontas em `textos.md`, seção 5). |
| **Deactivated** | Fora do ar | Leia o motivo e avise a equipe. |

> Para mudar algo enquanto o efeito está **Under review**, use **Withdraw from review**. Ele volta para Draft e precisa ser reenviado.

---

## Parte 15: Problemas comuns e soluções

| Problema | Causa provável | Solução |
|---|---|---|
| Não acho o template "Future Life" | Aba ou nome diferente | Parte 1: busque `Future`, `Bubble`; olhe Community Creator, Community Center, Interactive e Face. Se não achar, Parte 16.1 (Plano B). |
| Não existe **Import → Texture Sequence** | O menu mudou | Arraste a **pasta** `respostas_amor` inteira do Explorador de Arquivos para o painel Assets. Ou importe os 8 PNG e procure, com o botão direito, uma opção de criar sequência (a confirmar). Anote o caminho certo no relatório. |
| A sequência veio com menos de 8 quadros | Arquivos não selecionados | Apague a sequência e importe de novo com **Ctrl+A**. |
| Aparece "My Future Life", "Lover", "Income" ou "Kids" | Troca não feita | Refaça a Parte 5.1 ou 5.2. Confira também se não há uma segunda cópia do objeto (por exemplo, um título "pai" e um "filho"). |
| Aparece resposta original em inglês | Animated Texture Player ou objeto ainda com a sequência antiga | Refaça a Parte 7.2 (passos 1 a 5) e a Parte 5.3. |
| Bolha fica **vazia** depois do estouro | Max do sorteio alto demais, ou sequência não ligada | Parte 7.3 (diminua 1 no Max) e Parte 7.2. |
| Algumas respostas nunca aparecem | Sorteio ainda com o número antigo de quadros | Parte 7.3. |
| A resposta fica trocando sozinha ou volta para a 1ª | Random lido duas vezes, ou defeito do Animated Texture Player | Plano C (Parte 16.2). |
| Arte **branca** (sem cor) | O fio **Start → For_Colors** foi apagado | Ligue de novo: arraste da saída do **Start** até a entrada **For_Colors** da caixa Color_Picker & Randomizer. |
| Resposta ilegível em fundo claro | Cor clara sobre fundo claro | Parte 8.4: com sombra, ou trocar as cores claras (Parte 7.4). |
| Sombra virou borrão colorido | Você usou com_sombra, mas o template troca a cor inteira | Troque para a versão sem sombra (Parte 3.3) e importe de novo. |
| Texto esticado (moeda ou bola viraram ovo) | Proporção diferente | Parte 5.1 a 5.3: Size com a proporção certa, ou Stretch Mode = Fit. Ao mudar Scale, mude X e Y juntos. |
| Resposta grande demais para a bolha | Scale alto | Diminua o **Scale** dos 3 objetos de resposta (Parte 5.3, passo 6). |
| O rosto muda sozinho (biquinho ou cara triste) | IA do template ainda ligada | Parte 6.3 (apagar). |
| O biquinho não dispara nada | Nó Mouth Pout desligado, ou rosto mal enquadrado na webcam | Parte 7.5. Teste com boa luz e rosto de frente. Se continuar, use o hint `Toque na tela` (Parte 13). |
| Clicar no Preview não faz nada | Clique fora da imagem, ou fio do **Screen Tap** solto | Clique **dentro** da imagem do Preview. Confira a Parte 7.5. |
| Bolhas ou título escondidos atrás dos botões do TikTok | Posição alta demais | Baixe juntos o título e as bolhas pelo **Position Y** (Parte 8.2). |
| Pacote acima de 8 MB | IA ou texturas antigas ainda no projeto | Parte 6.3 e Parte 5.6. |
| **Test performance** falhou | Quase sempre a IA do template | Parte 6.3. Depois clique em **View suggestions**. |
| Pediu login de novo ou está na conta errada | Login expirou | Chame o Vini (seção 0.7), com o link. |
| O programa pede atualização | Versão antiga | Baixe a mais nova em https://effecthouse.tiktok.com/download e instale por cima. |
| **Needs revision** por "parecido com template" ou "falta de originalidade" | Visual padrão do Future Life | Faça a Parte 5.4 (bolha própria), se ainda não fez. Nos comentários, destaque as 24 frases originais em português e as artes próprias. Avise a equipe da nuvem. |
| **Needs revision** por IA ou por falta de "AI" no nome | A revisão achou IA no efeito | Confira a Parte 6.3 (apagar, não só desligar) e reenvie explicando nos comentários que não há IA generativa. |
| **Needs revision** por causa de uma frase | Frase vetada | Troque pela reserva, como explicado logo abaixo. |
| **Needs revision** por texto na tela / "parece anúncio" | O revisor achou o título dispensável | Responda nos comentários que o título "MEU 2027 VAI SER…" é a pergunta do efeito, sem marca nem chamada. Avise a equipe. |
| **Needs revision** por desempenho | QA técnico | Rode o Test performance; confira a Parte 6.3; reduza o tamanho (Parte 9). |
| O formulário recusa o vídeo | Formato, duração ou tamanho | Parte 10.3 (ffmpeg); confira 9:16, até 15 s e até 32 MB. |

### Como trocar uma frase vetada pela reserva

As reservas já estão prontas, no mesmo formato, em cada pasta de variante (`<PASTA>\reservas\`). A troca é **dentro da mesma bolha**.

| Bolha | Reserva 1 | Reserva 2 |
|---|---|---|
| AMOR | `reserva_amor_01.png`: AMOR NA FILA DO PÃO | `reserva_amor_02.png`: DATE QUE DÁ CERTO |
| GRANA | `reserva_grana_01.png`: SALÁRIO DURA O MÊS TODO | `reserva_grana_02.png`: FATURA SEM SUSTO |
| FUTEBOL | `reserva_futebol_01.png`: TÉCNICO NOVO EM MARÇO | `reserva_futebol_02.png`: PÉ-QUENTE OFICIAL |

> Se vetarem **LIMPA O NOME** (grana_07), use **SALÁRIO DURA O MÊS TODO** (`reserva_grana_01.png`), como pede o `textos.md`.

1. Crie a pasta `<PASTA>\respostas_trocadas\`, **fora** das pastas de resposta.
2. Mova a frase vetada (ex.: `respostas_grana\grana_07.png`) para `respostas_trocadas\`.
3. Copie a reserva (ex.: `reservas\reserva_grana_01.png`) para a pasta `respostas_grana\`.
4. Renomeie a cópia com o nome da frase vetada (ex.: `grana_07.png`).
5. Confira se a pasta continua com **exatamente 8** imagens.
6. No Effect House, apague a sequência `seq_grana` do painel Assets.
7. Importe a pasta de novo (Parte 4.2) com o nome `seq_grana`.
8. Ligue a nova sequência de novo (Partes 5.3 e 7.2). Se usar o Plano C, ligue também no campo do script.
9. Teste (Parte 8) e reenvie.
10. Avise a equipe da nuvem qual frase foi trocada, para atualizar `textos.json`.

---

## Parte 16: Planos B e C e o assistente

| Plano | Quando usar | Esforço |
|---|---|---|
| **B: montar do zero** | O template Future Life não existe ou não abre | alto (perde a animação de subir e estourar) |
| **C: script de sorteio** | O template funciona, mas o sorteio das respostas falha (vazio, viciado, volta para a 1ª) e a Parte 7.3 não resolveu | baixo (colar o script e ligar 3 campos) |
| **Assistente Effect House AI** | Travou em qualquer passo | baixo; pedidos prontos em `script\prompt-effect-house-ai.md` |

### 16.1 Plano B: montar do zero

Use o **Pedido 3** de `script\prompt-effect-house-ai.md`. Se o assistente não existir, monte à mão:

1. Crie um projeto vazio: na tela inicial, clique em **New Project** ou **Blank** (a confirmar).
2. Importe `assets\variantes\com_sombra\titulo.png`, os 3 arquivos `assets\variantes\bolha_inteira\bolha_inteira_<bolha>.png` (amor, grana, futebol) e `bolha_vazia.png`.
3. Importe as 3 sequências de `assets\variantes\com_sombra\respostas_<bolha>\` (Parte 4.2). Aqui não há sorteio de cor, então as respostas ficam brancas e a sombra garante a leitura.
4. Na **Hierarchy**, crie 10 imagens de tela (**+** → **2D** → **Image** ou **Screen Image**; a confirmar): `Titulo`, `Bolha_Amor`, `Bolha_Grana`, `Bolha_Futebol`, `Aberta_1`, `Aberta_2`, `Aberta_3`, `Resposta_1`, `Resposta_2`, `Resposta_3`.
5. Ponha as texturas: título no `Titulo`; `bolha_inteira_amor`, `_grana` e `_futebol` nas 3 bolhas; `bolha_vazia` nas 3 abertas; `seq_amor`, `seq_grana` e `seq_futebol` nas 3 respostas.
6. Posicione: título no alto, ao centro; as 3 bolhas em fila logo abaixo (esquerda, meio, direita); cada `Aberta` no mesmo lugar da bolha da coluna; cada `Resposta` no centro da sua `Aberta`, com cerca de 90% da largura dela e proporção 4:1.
7. Pinte as bolhas pelo campo **Color** do componente Image: AMOR `#FF4F8B`, GRANA `#FFB020`, FUTEBOL `#2EC27E`. A `Aberta` de cada coluna leva a mesma cor da bolha. Título e respostas ficam brancos.
8. No **Visual Scripting**, adicione o nó **Start** e ligue em sequência nós **Set Visibility**: `Titulo` e as 3 bolhas = **ligado**; as 3 abertas e as 3 respostas = **desligado**.
9. Adicione o nó **Screen Tap** e ligue a saída **Next** numa sequência de **Set Visibility**: as 3 bolhas = **desligado**; as 3 abertas e as 3 respostas = **ligado**.
10. Adicione o nó **Facial Movement Detection**, escolha **Mouth Pout** e ligue a saída **Begin** no **primeiro** Set Visibility da sequência do passo 9.
11. Para voltar ao começo quando a pessoa aperta gravar, ligue o evento de início de gravação (algo como **Video Record Start**; a confirmar) no **primeiro** Set Visibility da sequência do passo 8.
12. Faça o sorteio com o script do Plano C (16.2, passos 5 a 15), com **Atraso Segundos** = `0`. Aqui não há Animated Texture Player para desligar.
13. Teste tudo da Parte 8 e siga para a Parte 9.

### 16.2 Plano C: script de sorteio (TypeScript)

**O que é:** o arquivo `script\SorteioRespostas2027.ts` sorteia 1 resposta por bolha e deixa a sequência parada nela. Sorteia de novo no toque, no biquinho (só quando o biquinho começa) e ao apertar gravar, e nunca repete a mesma resposta duas vezes seguidas. Ele **não** mostra, esconde nem pinta nada: isso continua com o template.
**O que foi conferido:** os nomes da API vieram do guia oficial de scripting, do tutorial oficial "VFX: Tap Burst" e dos arquivos de tipos do Effect House de um projeto público. O script passou na checagem de tipos e num teste de lógica fora do programa (toque, biquinho comprido, intervalo mínimo, sem repetição, sorteio uniforme). **Ainda não foi rodado dentro do Effect House** (a confirmar no Preview).

1. Clique em **File → Save As**.
2. Dê o nome `C05-meu-2027-script`. Assim, o projeto original fica intacto.
3. Impeça que o template escolha o quadro, senão os dois sorteios brigam. Em cada um dos 3 nós **Animated Texture Player**:
   - se **não sai nenhum fio** das saídas dele (**On Begin**, **On Pause**, **On Resume**, **On Play End**): clique no fio que entra em **Play From To** e aperte **Delete**;
   - se **sai algum fio** das saídas: **não apague nada** nesse nó. No passo 14, use **Atraso Segundos** maior (veja lá).
4. Aperte **Ctrl+S**.
5. No painel **Assets**, clique em **+** (**Add**).
6. Crie um script **TypeScript** (a confirmar na sua versão do programa: pode aparecer como **Script**, **Create → Script** ou **Script Component**).
7. Dê o nome `SorteioRespostas2027`.
8. Abra o script (clique duplo; o programa abre um editor).
9. Apague todo o conteúdo.
10. Cole o conteúdo de `efeito-3-meu-2027-vai-ser\script\SorteioRespostas2027.ts`.
11. Salve o script.
12. Na **Hierarchy**, clique em **+** (**Add**) e crie um objeto vazio (**Empty Object** ou parecido; a confirmar), **fora** dos grupos do template.
13. Renomeie o objeto para `Sorteio`.
14. Com `Sorteio` selecionado, clique em **Add Component** no Inspector e escolha **SorteioRespostas2027** (pode estar dentro de **Script**; a confirmar). Preencha:
    - **Respostas Bolha 1**: arraste `seq_amor` do painel Assets;
    - **Respostas Bolha 2**: `seq_grana`;
    - **Respostas Bolha 3**: `seq_futebol`;
    - **Respostas Bolha 4**: deixe vazio;
    - **Sortear No Toque**, **Sortear No Biquinho** e **Sortear Ao Gravar**: marcados;
    - **Atraso Segundos**: `0.1`. Se no passo 3 você **não** pôde apagar o fio, use o tempo que a resposta leva para aparecer depois do toque, mais um pouco (comece com `1` e ajuste);
    - **Intervalo Minimo**: `1.5`.
15. Aperte **Ctrl+S**.
16. Faça todos os testes da Parte 8, principalmente o 8.3.

**Se der erro:**
- Erro ao salvar ou compilar o script: use o **Pedido 4** de `script\prompt-effect-house-ai.md`.
- A resposta aparece e logo troca por outra: aumente **Atraso Segundos** (o template ainda escolhe o quadro antes do script).

### 16.3 Assistente Effect House AI

A partir da versão 5.13 existe o assistente **Effect House AI**, que monta cenas e lógica a partir de um pedido escrito. A disponibilidade por conta ou região não foi confirmada. Os pedidos prontos, em inglês, estão em `efeito-3-meu-2027-vai-ser\script\prompt-effect-house-ai.md`.

Use o assistente para **destravar** um passo, não para mudar a ideia do efeito. Peça sempre "sem IA generativa". Depois, confira tudo com os checklists da Parte 8.

---

## Parte 17: Extras opcionais (só com ordem da equipe da nuvem)

### 17.1 Trocar FUTEBOL por CARRO (continua com 3 bolhas)

É uma troca simples de imagens, sem risco para o template.

1. Na Parte 4.1, importe `bolha_carro.png` no lugar de `bolha_futebol.png`.
2. Na Parte 4.2, importe a pasta `respostas_carro` (**6** quadros) com o nome `seq_carro`.
3. Nas Partes 5.2, 5.3 e 7.2, use `bolha_carro` e `seq_carro` na bolha da direita (Kids).
4. Na Parte 7.3, use **6** quadros: Max = **5** (se o Max original contava o último quadro) ou **6** (se não contava); To = **5** no caso de números fixos.
5. Na Parte 8.3, a bolha CARRO passa se não houver bolha vazia, se saírem **pelo menos 5** respostas diferentes e se a última, **CARRO SEMPRE / CHEIROSO** (quadro 5), sair pelo menos uma vez.
6. No envio, troque "futebol" por "carro" e "24" por "22" nos textos, e use exemplos de carro. Comentários em inglês: "LOVE, MONEY and CAR bubbles", "22 original". Descrição curta: `Faça biquinho e veja como vai ser o seu 2027 no amor, na grana e no carro.`

### 17.2 4ª bolha CARRO (experimental)

**Recomendação da equipe: não fazer no primeiro envio.** Exige duplicar objetos e a lógica de uma bolha inteira, perto da pasta "DO NOT REMOVE!!!", e 4 bolhas numa tela 9:16 deixam as respostas menores.

Se a equipe pedir:

1. Termine e teste a versão de 3 bolhas primeiro (até a Parte 10).
2. Clique em **File → Save As** e dê o nome `C05-meu-2027-4bolhas`.
3. Marque no relógio: **45 minutos**. Se não funcionar nesse tempo, desista e envie a de 3 bolhas.
4. Use o **Pedido 5** de `script\prompt-effect-house-ai.md`. Sem o assistente, à mão:
   1. Importe `bolha_carro.png` e a pasta `respostas_carro` como `seq_carro` (6 quadros).
   2. Na **Hierarchy**, clique com o botão direito no objeto da direita de **Animations** e escolha **Duplicate**. Faça o mesmo em **Bubble** e em **Bubble_Titles**.
   3. Ponha `bolha_carro` no rótulo duplicado e `seq_carro` na resposta duplicada.
   4. No **Visual Scripting**, ache tudo o que controla a bolha da direita (siga os fios a partir do nó **Animated Texture Player** dela e dos nós que citam os objetos dela).
   5. Selecione esses nós, copie (**Ctrl+C**) e cole (**Ctrl+V**).
   6. Troque, nos nós colados, os objetos da direita pelos duplicados e a sequência por `seq_carro`, com Max ou To para **6 quadros** (Parte 17.1, passo 4).
   7. Ligue o gatilho (o mesmo fio de toque e biquinho que dispara as outras bolhas) nos nós colados.
   8. Reposicione as 4 bolhas para caberem na tela sem encostar umas nas outras nem no título.
5. Faça a Parte 8 inteira, nas **4** bolhas.
6. Se qualquer item falhar, ou se as respostas ficarem pequenas demais para ler, **descarte a cópia** e envie a de 3 bolhas.
7. Se passar, use no envio os textos de 4 bolhas: "amor, grana, futebol e carro" e "30 frases" em português; "LOVE, MONEY, FOOTBALL and CAR" e "30 original" em inglês (estão no `textos.json`, campo `descricao_envio`).

---

## Parte 18: O que anotar no relatório

Em `Documentos\Efeitos\relatorio-montagem.md`, na seção do C05:

- Versão do Effect House instalada.
- Nomes reais de abas, grupos, objetos, componentes e nós que estavam diferentes deste guia (o que cada "a confirmar" virou).
- Tamanho e número de quadros das sequências originais, do título e dos rótulos (Parte 2.3).
- Resultado do teste da sombra e a `<PASTA>` escolhida (Parte 3).
- Se a bolha própria entrou (Parte 5.4) e o que o grupo TIPS mostrava (Parte 5.5).
- O que a IA fazia no rosto, e se ela foi **apagada** ou só **desligada** (Parte 6).
- O que chegava em From e To dos Animated Texture Player, Min e Max originais e os valores que você colocou (Parte 7.3).
- Resultado das rodadas (Parte 8.3): quantas rodadas, quantas respostas diferentes por bolha e se saiu a 8ª.
- Se o biquinho foi testado (webcam ou celular) e se funcionou.
- Plano usado: template, B ou C. Se usou o assistente, qual pedido.
- Tamanho do pacote e resultado do Test performance.
- Lista de categorias e tipo de campo de hint (texto livre ou lista) que apareceram no formulário.
- Nome enviado, data e hora do envio, print da confirmação e status (Under review, Needs revision ou Active).

---

## Fontes consultadas

Documentação oficial do Effect House (lida por resumos de busca, porque o site não abre daqui):
- Tutorial do template Future Life: https://effecthouse.tiktok.com/learn/library/template-tutorials/future-life e https://effecthouse.tiktok.com/learn/guides/tutorials/template-tutorials/future-life. Base para: aba Community Creator; gatilho por toque ou biquinho; grupos 2D Foreground Effects, Main_Elements, Animations, Bubble, Bubble_Titles, Effect_Title, Generative Effects (Pucker e Unhappy) e TIPS; pastas DO NOT REMOVE!!! - Main Assets e Texture_Seq; artes brancas; 3 nós Animated Texture Player; subgraph Color_Picker & Randomizer (Bubble_Input); fio Start → For_Colors; quadros Change Color e "Remove these if you use images"; respostas originais "No One", "$-10K" e "0".
- Nó Animated Texture Player (Play From To, Pause, Resume; From e To começam em 0 e vão até o total − 1; From = To mostra 1 quadro; saídas On Begin, On Pause, On Resume, On Play End): https://effecthouse.tiktok.com/learn/guides/visual-scripting/nodes/utility/animated-texture-player
- Nó Set Animated Texture (Order: Forward, Random, Ping-pong, Shuffle; FPS; Loop Count): https://effecthouse.tiktok.com/learn/guides/visual-scripting/nodes/utility/set-animated-texture
- Nó Facial Movement Detection (Mouth Pout; saídas Begin, Stay, End, None): https://effecthouse.tiktok.com/learn/guides/editor-panels/visual-scripting/nodes/head-and-face/facial-movement-detection
- Regras de IA generativa (pôr "AI" no nome; no máximo 1 Generative Effect por causa do FPS e do QA): https://effecthouse.tiktok.com/learn/guides/getting-started/best-practices/using-generative-ai-to-create-tiktok-effects · https://effecthouse.tiktok.com/learn/guides/technical-guides/components/utility/generative-effects
- FAQ do programa de recompensas (efeito de IA generativa não elegível; pesquisa da equipe em `pesquisa/02-monetizacao-e-regras.md`): https://effecthouse.tiktok.com/learn/guides/support/faq-effect-creator-rewards
- Preparação de sequência de imagens (PNG/JPG, até 1024 px, menos de 1 MB cada, mesmo tamanho): https://effecthouse.tiktok.com/learn/guides/technical-guides/assets/asset-preparation/2d-texture-sequence
- Scripting em TypeScript (APJS): https://effecthouse.tiktok.com/learn/guides/api-reference/scripting-capability-usage-guide
- Preview no celular: https://effecthouse.tiktok.com/learn/guides/publishing/preview-in-tiktok · Vídeo demo: https://effecthouse.tiktok.com/learn/guides/publishing/demo-video-creation
- Teste de desempenho: https://effecthouse.tiktok.com/learn/guides/publishing/publish/test-effect-performance
- Envio: https://effecthouse.tiktok.com/learn/guides/publishing/publish/submit-your-effect · Ícone: https://effecthouse.tiktok.com/learn/guides/publishing/effect-icon-creation
- Status (Manage Effects): https://effecthouse.tiktok.com/learn/guides/management-and-growth/manage-your-effect

Fórum e outras:
- Animated Texture Player voltando para o 1º quadro de vez em quando: https://community.effecthouse.com/t/animated-texture-sequences-keep-flickering-when-trying-to-stop-on-a-frame-via-screen-tap/71157
- Tipos da API do Effect House (`APJS.d.ts` e `OrionDecorators.d.ts`): projeto público https://github.com/christophusbeck/StatJack (pasta `StatJack_EH`). Versão do Effect House usada nele: não informada.
- Pesquisa técnica da equipe: `tiktok-efeitos/pesquisa/03-tecnico-effect-house.md`. Artes e testes do designer: `efeito-3-meu-2027-vai-ser/assets/LEIA-ME.md`.
