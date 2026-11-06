# Guia de montagem: "Torcedômetro" (C01)

**Para quem é:** quem vai montar o efeito no Effect House. Pode ser o Montador (o Claude que roda no PC do Vini) ou o próprio Vini, mesmo sem nunca ter aberto o programa.
**Versão do guia:** 1.1 · 06/11/2026 (1.1: revisão de QA) · escrito para o Effect House 5.1x no Windows (no Mac, troque **Ctrl** por **Cmd** e "Explorador de Arquivos" por **Finder**).
**Tempo total:** cerca de 3 h sem imprevistos. Como é o primeiro efeito da conta, reserve 5 h.

> **Vini, se você estiver lendo:** não precisa fazer nada aqui. Este roteiro é para quem monta. Você só será chamado nos casos da seção 0.6, e sempre com o link direto.

### Como ler as marcas

- **(a confirmar na sua versão do programa)**: a equipe não conseguiu ver essa tela, porque o site do Effect House não abre de onde pesquisamos. Se o botão tiver outro nome, procure um parecido e **anote no relatório** o nome real.
- Os nomes de botões e painéis estão **em inglês e em negrito**, porque o programa é em inglês.
- Nos passos, "clique" é com o botão esquerdo. Quando for o direito, o passo diz "clique com o botão direito".

### O que vamos montar (resumo)

1. Sobre a cabeça aparece um ingresso colorido com a pergunta **"QUE TORCEDOR / VOCÊ É?"** e a etiqueta **"👆 TOQUE NA TELA"**.
2. A pessoa toca na tela. O título some e as cartas giram por cerca de 2 segundos.
3. O giro para numa das **26 cartas**, por exemplo "PÉ-FRIO / CERTIFICADO". A carta fica presa na cabeça.
4. Quando a pessoa aperta **gravar** no TikTok, o efeito volta para o título. Assim, o sorteio sai dentro do vídeo.

A base é o template pronto **Randomizer 2D**. Ele já tem toda a lógica, então **não é preciso programar**: basta trocar as imagens e ajustar 3 valores. O efeito é para **1 pessoa** (1 rosto).

---

## Parte 0: Antes de começar

### 0.1 Links

| O quê | Link direto | Quem usa |
|---|---|---|
| Baixar o Effect House (Windows 10 ou mais novo; no Mac há uma versão para chip Apple e outra para Intel) | https://effecthouse.tiktok.com/download | Montador. Só se o programa ainda não estiver instalado. |
| Guia oficial de instalação e login | https://effecthouse.tiktok.com/learn/guides/getting-started/introduction-to-effect-house/download-and-login | Consulta |
| Arquivos da equipe (zip com tudo) | https://github.com/quantopagarei-sketch/quantocobrarpj/archive/refs/heads/main.zip | Montador |
| Aviso de que a equipe terminou (erro 404 = ainda não terminou) | https://raw.githubusercontent.com/quantopagarei-sketch/quantocobrarpj/main/tiktok-efeitos/PRONTO-PARA-MONTAR.md | Montador |
| Tutorial oficial do template (em inglês) | https://effecthouse.tiktok.com/learn/guides/tutorials/template-tutorials/randomizer-2d | Consulta |
| Modos de reprodução da sequência de imagens (em inglês) | https://effecthouse.tiktok.com/learn/guides/animation/animation-sequence/ | Consulta |
| Guia oficial de envio | https://effecthouse.tiktok.com/learn/guides/publishing/publish/submit-your-effect | Consulta |
| Busca de marcas do INPI (Parte 11) | https://busca.inpi.gov.br/pePI/ | Montador |

> O zip só traz este efeito **depois** que a equipe publicar os arquivos. Antes de baixar, confira se o link do "Aviso" abre.

### 0.2 Copiar os arquivos para o computador

1. Baixe o zip pelo link da tabela.
2. Abra o zip.
3. Copie **só a pasta `tiktok-efeitos`** para `Documentos\Efeitos\`.
4. Confira se esta pasta existe:
   `Documentos\Efeitos\tiktok-efeitos\efeito-1-torcedometro\assets\`

> **Montador:** no Windows, "Documentos" fica em `%USERPROFILE%\Documents`. Com o OneDrive ativo, pode ser `%USERPROFILE%\OneDrive\Documentos`. Para descobrir, rode no PowerShell: `[Environment]::GetFolderPath('MyDocuments')`.

### 0.3 Conferir os arquivos

Rode no PowerShell, trocando `<DOCS>` pelo caminho de Documentos:

```powershell
$a = "<DOCS>\Efeitos\tiktok-efeitos\efeito-1-torcedometro\assets"
(Get-ChildItem "$a\cartas\carta_*.png").Count          # tem que dar 26
(Get-ChildItem "$a\cartas\*").Count                    # tem que dar 26 (a pasta só pode ter as cartas)
Get-ChildItem "$a\titulo.png", "$a\titulo_toque.png", "$a\icone_162.png", "$a\icone_alt_162.png" | Select Name, Length
(Get-ChildItem "$a\cartas\*.png" | Measure-Object Length -Maximum).Maximum   # tem que ser menor que 1048576 (1 MB)
```

Se faltar arquivo, baixe o zip de novo. Se continuar faltando, avise a equipe da nuvem. Não chame o Vini por isso.

### 0.4 O que entra no efeito e o que não entra

| Arquivo (dentro de `assets\`) | Entra? | Para quê |
|---|---|---|
| `titulo_toque.png` (512×256, fundo transparente) | **Sim (padrão)** | Título "QUE TORCEDOR / VOCÊ É?" com a etiqueta "👆 TOQUE NA TELA". Vai no objeto **Title**. |
| `titulo.png` (512×256) | Reserva | O mesmo título, sem a etiqueta. Só se o título sumir sozinho antes do toque (Parte 7.2). |
| `cartas\carta_01.png` … `carta_26.png` (512×256 cada) | **Sim** | Os 26 resultados. Entram juntos como **uma** sequência de imagens (**Texture Sequence**), na ordem 01→26. |
| `icone_162.png` (162×162) | **No formulário de envio** | Ícone do efeito (obrigatório) |
| `icone_alt_162.png` (162×162) | **No formulário de envio** | 2º ícone (opcional) |
| `reservas\reserva_01.png` … `reserva_04.png` | Não | Só se uma carta for vetada (Parte 14) |
| `quadrado_512\` (as mesmas imagens em 512×512) | Não, salvo exceção | Só se não der para deixar a imagem em 2:1 (Parte 5.1) |
| `icone_512.png`, `icone_alt_512.png`, `previa.png`, `gerar.py`, `lista-de-arquivos.txt` | Não | Referência da equipe |

**Por que o título com a etiqueta é o padrão:** a dica "Toque na tela" do formulário não aparece no teste pelo celular e, no app, some em poucos segundos. Com o TapToSpin ligado, o título fica parado até o toque, então a etiqueta avisa a pessoa o tempo todo.

**Como são as imagens:** todas têm o **mesmo quadro de 512×256** (2 de largura por 1 de altura), com o ingresso sempre no mesmo lugar. Por isso a troca do título para a carta não "pula". No topo de cada imagem há uma **medalha redonda** com o desenho. Ela serve de régua: se a medalha parecer um ovo, a imagem está esticada.

A ordem das cartas está em `textos.md`, seção 3. O quadro 0 da sequência é a carta 01 (TÉCNICO DE SOFÁ) e o quadro 25 é a carta 26 (TORCE ATÉ NA CHUVA).

### 0.5 Tempo estimado

| Etapa | Tempo |
|---|---|
| Parte 0: baixar e conferir | 10 min |
| Partes 1 e 2: abrir o template e reconhecer as peças | 15 min |
| Partes 3 e 4: importar e trocar as imagens | 20 min |
| Parte 5: proporção, posição e tamanho | 25 min |
| Parte 6: ajustar a lógica | 10 min |
| Parte 7: testar no PC | 30 min |
| Partes 8 e 9: desempenho e vídeo demo | 30 min |
| Partes 11 a 13: conferências, envio e status | 25 min |
| **Total** | **≈ 3 h** (reserve 5 h) |

### 0.6 O que depende do Vini (o mínimo)

Pela ordem da equipe (`ORDEM-PC.md`), o Vini **já deixou o Effect House instalado e logado** na conta Car Shop. Ele só é chamado se:

1. **O login cair** ou o programa estiver logado em outra conta. Mande para ele, com o link:
   > Abra o Effect House no computador. Vai aparecer um QR code. No celular, abra o **TikTok da conta Car Shop** → **Perfil** → ícone de pessoa (**Adicionar amigos**) → ícone de scanner no canto de cima → aponte para o QR → toque em **Confirmar**. Guia com imagens: https://effecthouse.tiktok.com/learn/guides/getting-started/introduction-to-effect-house/download-and-login
   >
   > Tem que ser o scanner **de dentro do TikTok**. A câmera comum do celular não funciona.
2. **O programa não estiver instalado.** Mande: "Baixe e instale por este link: <https://effecthouse.tiktok.com/download>. Se o computador for Mac, escolha **Apple** (chip M1, M2…) ou **Intel** conforme o menu  → **Sobre este Mac**". Depois, o login do item 1.
3. **O teste no celular** (Parte 10). Ele é **opcional**. Se for feito, junte com os outros efeitos num único momento.

Todo o resto (montar, testar no PC, gravar o vídeo demo e enviar) é feito sem ele.

---

## Parte 1: Abrir o template

1. Abra o **Effect House**.
2. Confira a conta. A foto ou o nome da conta **Car Shop** deve aparecer na tela inicial (a confirmar na sua versão do programa: onde a conta aparece). Se for outra conta, **pare** e siga a seção 0.6.
3. Anote no relatório a versão do programa. Ela costuma estar em **Help → About** ou na tela inicial (a confirmar na sua versão do programa). O esperado é 5.15 ou 5.16.
4. Clique em **Templates**, no menu da esquerda da tela inicial.
5. Digite `Randomizer` na busca.
6. Clique no card **Randomizer 2D**. Atenção: **2D**, não 3D.
7. Clique em **Create** ou **Open** (a confirmar na sua versão do programa: o nome do botão).
8. Espere o projeto carregar. O programa pode baixar o template, o que leva até 1 minuto.

**Se não achar "Randomizer 2D":**
- busque `Random`, `Randomizer` ou `Random Image`;
- olhe nas categorias **Interactive**, **Face** e **Game**;
- se não achar mesmo, vá para a Parte 15 (Plano B ou C).

9. Clique em **File → Save As**.
10. Crie a pasta `Documentos\Efeitos\projetos\`, se ela não existir.
11. Dê o nome `C01-torcedometro`.
12. Clique em **Salvar**.

> A partir daqui, aperte **Ctrl+S** ao fim de cada parte.

---

## Parte 2: Reconhecer as peças do template

O programa é dividido em painéis. Os que vamos usar:

| Painel | Onde costuma ficar | Para quê |
|---|---|---|
| **Hierarchy** | à esquerda, em cima | lista os objetos da cena |
| **Assets** | à esquerda, embaixo | lista os arquivos importados |
| **Inspector** | à direita | mostra as propriedades do objeto selecionado |
| **Preview** | à direita ou no centro | mostra o efeito num rosto de exemplo |
| **Visual Scripting** | embaixo | mostra a lógica (caixinhas ligadas por fios) |

Se algum painel sumir, procure no menu **Window** (a confirmar na sua versão do programa).

1. Olhe o painel **Hierarchy**.
2. Ache o objeto **Title**. É nele que fica a imagem do título.
3. Ache o objeto **RandomAnimationSequence**. É nele que fica a sequência de imagens que gira.
4. Clique em **Title**.
5. Anote no relatório os componentes que aparecem no **Inspector**. O esperado é algo como **2D Transform** (ou **Screen Transform**), **Image** e **Face Sticker** (a confirmar na sua versão do programa).
6. Anote o tamanho da imagem: o campo **Size** (largura × altura), que pode estar no componente **Image** ou no **Transform**. Anote também o campo **Stretch Mode**, se existir.
7. Clique em **RandomAnimationSequence**.
8. Anote os componentes. Repare em **onde a sequência de imagens está ligada**. Há dois casos possíveis (a confirmar na sua versão do programa):
   - **Caso A:** existe um componente **Animation Sequence**, com um campo de sequência e um campo **FPS**;
   - **Caso B:** não existe esse componente, e a sequência fica direto no campo **Texture** do componente **Image**.
9. Anote **Size** e **Stretch Mode** deste objeto também.
10. Abra o painel **Visual Scripting**.
11. Ache a caixa grande do randomizador. É um **subgraph**, uma caixa que guarda vários nós dentro.
12. Clique nela e anote os valores de **TapToSpin**, **TimeToSpin**, **TitleDelay** e **TitleFadeOutTime**. Eles podem aparecer na própria caixa ou no Inspector.

> Se os nomes forem um pouco diferentes (por exemplo, "Title_A" ou "Randomizer"), siga com os nomes que existem e anote no relatório.

---

## Parte 3: Importar as imagens

### 3.1 Títulos

1. No painel **Assets**, clique no botão **+** (**Add**).
2. Clique em **Import**.
3. Clique em **From Computer** (a confirmar na sua versão do programa: pode aparecer como "Texture" ou "Image").
4. Vá até `Documentos\Efeitos\tiktok-efeitos\efeito-1-torcedometro\assets\`.
5. Selecione `titulo_toque.png`.
6. Segure **Ctrl** e clique em `titulo.png`, para levar os dois.
7. Clique em **Abrir**.
8. Confira se `titulo_toque` e `titulo` apareceram no painel **Assets**.

### 3.2 As 26 cartas (sequência)

As cartas **não** entram uma a uma como imagens soltas. Elas entram juntas como **Texture Sequence**. O tutorial oficial do template manda importar só as respostas, sem o título.

1. No painel **Assets**, clique em **+** (**Add**).
2. Clique em **Import**.
3. Clique em **Texture Sequence**.
4. Abra a pasta `assets\cartas\`.
5. Faça o que a janela pedir (a confirmar na sua versão do programa):
   - se ela pedir **arquivos**: aperte **Ctrl+A** para selecionar os 26 PNG e clique em **Abrir**;
   - se ela pedir **uma pasta**: selecione a pasta `cartas` e clique em **Selecionar pasta**.
6. Confira se apareceu **uma** sequência no painel Assets (provavelmente chamada `cartas` ou `carta`).
7. Clique nela.
8. Confira no **Inspector** se ela tem **26 frames** (quadros).
9. Clique com o botão direito na sequência e escolha **Rename**.
10. Digite `cartas_torcedor` (opcional, só para organizar).

> **A ordem tem que estar certa.** Os nomes têm zero na frente (01, 02 … 26), então a ordem alfabética já é a certa. Se o Inspector mostrar outra ordem, apague a sequência e importe de novo.

### 3.3 Compressão das imagens

1. Clique em `titulo_toque` no painel Assets.
2. Confira a compressão no **Inspector**. Deixe **Automatic** (512 px) ou **Manual → 512 → High**. As imagens já têm 512 px de largura, então não há perda.
3. Faça o mesmo com `titulo`.
4. Faça o mesmo com a sequência `cartas_torcedor`.

> **Não** use Medium nem Low agora. Isso só entra se o tamanho do pacote passar do limite (Parte 8).

---

## Parte 4: Trocar as imagens do template

### 4.1 Título

1. Na **Hierarchy**, clique em **Title**.
2. No **Inspector**, ache o componente **Image**.
3. Clique no campo **Texture**.
4. Escolha `titulo_toque` na lista. Também dá para arrastar `titulo_toque` do painel Assets para o campo.
5. Confira no **Preview** se o título apareceu sobre a cabeça. Se parecer esticado, não se preocupe: isso se resolve na Parte 5.

### 4.2 Cartas

1. Na **Hierarchy**, clique em **RandomAnimationSequence**.
2. Siga o caso que você anotou na Parte 2, passo 8:
   - **Caso A (existe Animation Sequence):** no componente **Animation Sequence**, clique no campo da sequência (pode se chamar **Texture Sequence**, **Texture** ou **Animated Texture**; a confirmar na sua versão do programa) e escolha `cartas_torcedor`. **Não mexa** no campo Texture do componente Image: a documentação oficial diz que o Animation Sequence troca essa textura sozinho a cada quadro, então o que for colocado ali é apagado.
   - **Caso B (só existe Image):** no componente **Image**, clique no campo **Texture** e escolha `cartas_torcedor`.
3. **Não mexa** no **FPS** (velocidade) da sequência. O giro rápido é de propósito: é ele que deixa o sorteio imprevisível. Anote o valor no relatório.

### 4.3 Limpar as imagens antigas do template

Isso deixa o pacote mais leve.

1. No painel **Assets**, ache o título e a sequência originais do template (os que vieram com ele).
2. Clique com o botão direito em cada um.
3. Clique em **Delete**.
4. Se o programa avisar que o asset ainda está em uso, **cancele**: alguma troca da Parte 4.1 ou 4.2 não foi feita. Volte e confira.

> Deixe `titulo` (a reserva sem etiqueta) no projeto até a Parte 7. Se ele não for usado, apague-o antes do envio (Parte 8).

---

## Parte 5: Proporção, posição e tamanho sobre a cabeça

O componente **Face Sticker** já faz a imagem seguir a cabeça. Aqui só ajustamos a proporção, o lugar e o tamanho.

### 5.1 Proporção 2:1 (o mais importante desta parte)

As imagens deste efeito são **2 de largura por 1 de altura** (512×256). Se o objeto do template for quadrado, o ingresso fica esticado. O teste é olhar a **medalha redonda** no topo: ela tem que parecer **um círculo, não um ovo**.

1. Na **Hierarchy**, clique em **RandomAnimationSequence**.
2. Olhe o **Size** que você anotou na Parte 2.
3. Decida pela tabela:

| O que o Size mostra | O que fazer |
|---|---|
| Largura = 2 × altura (ex.: 512 × 256) | Nada. Siga para a 5.2. |
| Quadrado ou outra proporção (ex.: 512 × 512) | Mude a **altura** para metade da largura (ex.: **512 × 256**). |
| Não há campo Size, ou ele não aceita mudança | Mude **Stretch Mode** para **Fit** (mantém a proporção). Se também não houver, use o plano de exceção abaixo. |

4. Confira no **Preview** se a medalha ficou redonda.
5. Faça a mesma coisa no objeto **Title**.

**Plano de exceção (só se nada acima funcionar):** use as imagens quadradas, que têm o ingresso centralizado numa tela transparente de 512×512.
1. Importe `assets\quadrado_512\titulo_toque.png` e a pasta `assets\quadrado_512\cartas\` como Texture Sequence, como na Parte 3.
2. Troque o título e as cartas pelas versões quadradas, como na Parte 4.
3. Apague as versões 512×256 do painel Assets.
4. Anote no relatório que usou as quadradas.

> Título e cartas têm que usar **a mesma** versão: as duas 512×256 ou as duas quadradas.

### 5.2 Posição e tamanho

**Regras:**
- **Title** e **RandomAnimationSequence** precisam ter **exatamente a mesma posição e o mesmo tamanho**.
- **Posição:** a borda de baixo do ingresso fica **logo acima do cabelo**, sem cobrir a testa nem os olhos.
- **Largura:** o ingresso deve ter **cerca de 1,6 vez a largura da cabeça** (aceitável entre 1,4 e 1,8). Na simulação do designer (`previa.png`), ele ocupa uns 2/3 da largura da tela.
- O ingresso inteiro, **inclusive a medalha de cima**, tem que caber na tela nos 3 rostos de exemplo.
- Não exagere na altura: quanto mais longe da cabeça, mais o adesivo treme quando a pessoa se mexe.

**Passos:**
1. Na **Hierarchy**, clique em **RandomAnimationSequence**.
2. No **Inspector**, abra o componente **2D Transform** (ou **Screen Transform**).
3. Anote os valores atuais de **Position**, **Scale** e **Size**, se existirem (a confirmar na sua versão do programa: quais campos aparecem).
4. Ajuste **Scale** até o ingresso ter cerca de 1,6 cabeça de largura. Mude **X e Y juntos, com o mesmo número**, para não estragar a proporção da 5.1.
5. Ajuste **Position Y** até a borda de baixo do ingresso ficar logo acima do cabelo.
6. Deixe **Position X** no centro (normalmente 0).
7. Troque o rosto do Preview: abra a lista de mídias do painel **Preview** e escolha outro rosto de exemplo.
8. Confira nos **3 rostos de exemplo** e escolha um meio-termo que sirva para todos.
9. Clique nos **três pontinhos** (⋮) do componente **2D Transform**.
10. Clique em **Copy**.
11. Na **Hierarchy**, clique em **Title**.
12. Clique nos **três pontinhos** do **2D Transform** do Title.
13. Clique em **Paste** (pode aparecer como **Paste Component Values**; a confirmar na sua versão do programa).
14. Confira no **Preview** se o título e as cartas ocupam o mesmo lugar.

> Se **Title** e **RandomAnimationSequence** estiverem dentro de um mesmo objeto "pai" (por exemplo, um objeto Face Sticker com os dois dentro), ajuste posição e tamanho **no pai**, e os dois mudam juntos (a confirmar na sua versão do programa).
>
> **Para ver uma carta parada durante o ajuste:** clique no Preview para sortear (Parte 7). Depois do giro, a carta fica parada e dá para ajustar com calma.

---

## Parte 6: A lógica (Visual Scripting)

**O template já faz toda a lógica.** Não crie nós e não apague nós. Só mude os valores abaixo, na caixa do randomizador (o subgraph).

| Campo | O que faz | Valor para o C01 | Por quê |
|---|---|---|---|
| **TapToSpin** | Ligado: o giro só começa quando a pessoa toca na tela. Desligado: começa sozinho ao abrir o efeito e de novo ao apertar gravar. | **Ligado (marcado)** | O título mostra "TOQUE NA TELA" e a pessoa escolhe a hora de sortear, por exemplo depois de dizer "vamos ver que torcedor eu sou". |
| **TimeToSpin** | Quanto tempo as cartas giram antes de parar (segundos) | **2** | É o tempo do conceito: dá suspense e cabe com folga num vídeo curto. |
| **TitleFadeOutTime** | Quanto tempo o título leva para sumir (segundos) | **0.3** | Troca rápida e limpa. |
| **TitleDelay** | Espera do título antes do giro. Pesa mais quando TapToSpin está desligado. | **Deixe o valor do template** e anote | Com TapToSpin ligado, quem decide a hora é o toque. |

### Passos

1. Abra o painel **Visual Scripting**.
2. Clique na caixa do randomizador.
3. Marque **TapToSpin**.
4. Digite `2` em **TimeToSpin**.
5. Digite `0.3` em **TitleFadeOutTime**.
6. Confira se a caixa aponta para os objetos certos: nos campos de objeto deve aparecer **Title** e **RandomAnimationSequence**.
7. Procure algum campo de **quantidade ou intervalo de quadros** (por exemplo "Count", "Frames" ou "Random 0–9"). Se existir, ponha **26** (quantidade) ou **0 a 25** (intervalo) (a confirmar na sua versão do programa). Se não existir, o template lê sozinho os 26 quadros.
8. Aperte **Ctrl+S**.

### Como a lógica funciona (só para entender)

- **Ao abrir o efeito** e **ao apertar gravar no TikTok**, o template volta ao começo: o título aparece e as cartas ficam escondidas. A documentação oficial confirma que os eventos "Effect Start" e "Video Record Start" reiniciam o randomizador.
- **No toque**, o título some em 0,3 s, as cartas giram por 2 s e a animação para numa carta.
- **Se TapToSpin estiver desmarcado**, o giro começa sozinho e o toque não faz nada. Por isso ele tem que estar marcado.

### Sobre script em código

**Este efeito não precisa de código.** Mesmo assim, a equipe deixou um script alternativo em TypeScript (`script\TorcedometroController.ts`) para o caso de a lógica do template falhar. Ele passou na checagem de tipos, feita com os arquivos de tipos da API do Effect House tirados de um projeto público, mas **ainda não foi rodado dentro do programa** (a confirmar). Como usar: Parte 15, Plano C.

---

## Parte 7: Testar no PC

### 7.1 Como testar no Preview

Clicar com o mouse **dentro da imagem do Preview** simula o toque na tela.

1. No painel **Preview**, abra a lista de mídias (o menu de cima).
2. Escolha um rosto de exemplo **em vídeo** (com movimento), se houver.
3. Clique dentro da imagem do Preview.
4. Veja o giro e a carta final.

> Dá para testar com a webcam pelo botão de câmera ao lado do menu de mídias. É opcional.

### 7.2 Checklist (marque tudo antes de seguir)

- [ ] Ao abrir, aparece **só o título**, sem nenhuma carta por trás.
- [ ] O título **fica na tela até o clique**. Se ele sumir sozinho antes, veja a Parte 14 (linha "O título some sozinho").
- [ ] A etiqueta **"TOQUE NA TELA"** aparece inteira, sem corte.
- [ ] O ingresso está **inteiro na tela**, sem corte em cima, nos 3 rostos de exemplo.
- [ ] A medalha está **redonda** (nada esticado), no título e nas cartas.
- [ ] A borda de baixo fica **acima do cabelo**, sem cobrir os olhos.
- [ ] O título **acompanha a cabeça** quando o rosto se mexe.
- [ ] Ao clicar, o título **some** e as cartas **giram**.
- [ ] O giro dura **cerca de 2 s** e **para** numa carta.
- [ ] A carta parada **dá para ler**, inclusive as de letra menor ou texto mais longo: 17 (SOME DO GRUPO / NA DERROTA), 18 (MANDA ÁUDIO / NO INTERVALO) e 22 (BUZINA QUANDO / SAI GOL).
- [ ] A carta continua **parada e presa na cabeça** quando o rosto se mexe.
- [ ] Não aparece **borda escura** nem quadrado em volta do ingresso. A transparência tem que estar OK.
- [ ] Quando o rosto **sai** da imagem, o ingresso **some**, sem ficar flutuando na tela.
- [ ] Clicar **de novo** depois do resultado faz o quê? Anote no relatório (gira de novo ou nada). As duas coisas são aceitáveis.

### 7.3 Teste do sorteio (importante)

Este teste mostra se o sorteio é aleatório de verdade.

1. Clique no Preview.
2. Anote o texto da carta que saiu.
3. Volte ao título: reinicie o Preview (a confirmar na sua versão do programa: botão de **reset/refresh** do Preview) ou clique de novo, se o template girar de novo.
4. Repita até ter **15 sorteios**.
5. Avalie:
   - **OK:** saíram **pelo menos 9 cartas diferentes** e **nenhuma carta saiu mais de 4 vezes**. (Com 26 cartas, um sorteio justo dá em média 11 ou 12 diferentes em 15 giros. A chance de um sorteio justo reprovar por azar é de pouco mais de 1%, pela simulação da equipe de QA.)
   - **Problema:** saem sempre as mesmas 2 ou 3 cartas, sempre a mesma, ou uma ordem fixa (01, 02, 03…). Aplique a correção abaixo.

**Correção se o sorteio estiver viciado:**
1. Clique em **RandomAnimationSequence** (Caso A) ou na sequência `cartas_torcedor` no painel Assets (Caso B).
2. Ache o modo de reprodução. Ele pode se chamar **Play Mode**, **Mode** ou **Order** (a confirmar na sua versão do programa).
3. Troque **Forward** (ou **Loop**) por **Shuffle**. Se não houver Shuffle, use **Random** (ou **Randomize**). A documentação oficial explica que Random sorteia a ordem dos quadros (pode repetir) e Shuffle embaralha sem repetir o quadro anterior.
4. Faça os 15 sorteios de novo.
5. Anote o resultado no relatório.
6. Se continuar viciado, use o Plano C (Parte 15), em que o sorteio é feito pelo script.

### 7.4 Salvar

1. Aperte **Ctrl+S**.

---

## Parte 8: Desempenho e tamanho

1. Apague `titulo` (a reserva sem etiqueta) do painel **Assets**, se ele não estiver em uso.
2. Na barra de cima, ache o indicador de tamanho do efeito.
3. Clique em **Click to update** para atualizar o número.
4. Anote o tamanho no relatório. A estimativa da equipe é de **perto de 3 MB**, porque as 26 cartas somam cerca de 2,1 MB.
   - **Até 5 MB:** ótimo, siga em frente.
   - **Entre 5 e 8 MB:** aceitável, já que o limite é 8 MB. Mesmo assim, tente diminuir com os passos abaixo.
   - **Acima de 8 MB:** não dá para enviar. Diminua com os passos abaixo.
5. Na barra de cima, clique em **Test performance**.
6. Clique em **Run test**.
7. Espere cerca de 30 segundos.
8. Se passar, siga para a Parte 9.
9. Se falhar, clique em **View suggestions** e veja a Parte 14.

**Para diminuir o tamanho, nesta ordem:**
1. Apague do painel Assets tudo o que sobrou do template e não é usado (Parte 4.3).
2. Mude a compressão da sequência `cartas_torcedor` para **Manual → 512 → Medium**.
3. Confira no Preview se o texto das cartas continua nítido. Se borrou, volte para **High**.
4. Deixe o **título** sempre em **High**.

> Passar no Test performance **não garante** a aprovação, mas falhar nele quase garante a reprovação.

---

## Parte 9: Vídeo demo (sem precisar do Vini)

O formulário pede um vídeo curto mostrando o efeito. Só a equipe de revisão vê, ele não é público. Regras: **9:16 (em pé), MP4 ou MOV, até 15 segundos, até 32 MB.**

### 9.1 Gravar no próprio Effect House

1. No **Preview**, escolha um aparelho com tela **9:16** na lista de aparelhos (costuma ficar embaixo, à esquerda). Um exemplo é o iPhone 8 ou um aparelho de 1080×1920. Telas mais compridas, como as do iPhone X em diante, não são 9:16 (a confirmar na sua versão do programa: quais aparelhos aparecem).
2. Escolha o rosto de exemplo em que o ingresso ficou melhor, de preferência em vídeo.
3. Volte o efeito para o começo, com o título aparecendo.
4. Clique em **Screen record** no painel Preview (a confirmar na sua versão do programa: o nome e o lugar do botão).
5. Siga o roteiro abaixo.
6. Pare a gravação antes de 15 segundos.
7. Salve em `Documentos\Efeitos\videos-demo\C01-demo-bruto.mp4`.

**Roteiro do vídeo (até 14 s):**

| Tempo | O que acontece |
|---|---|
| 0–2 s | Título parado sobre a cabeça, com "TOQUE NA TELA" |
| ≈ 2 s | Clique no Preview |
| 2–4,5 s | Título some e as cartas giram |
| 4,5–8 s | Resultado parado, com o rosto se mexendo um pouco |
| ≈ 8 s | Clique de novo, se o template girar de novo (se não girar, deixe o resultado até o fim) |
| 8–13 s | Segundo giro e segundo resultado |

### 9.2 Conferir o formato

1. No Explorador de Arquivos, clique com o botão direito no vídeo.
2. Clique em **Propriedades**.
3. Abra a aba **Detalhes**.
4. Confira **Largura** e **Altura**. O vídeo tem que estar em pé e em 9:16, por exemplo 1080×1920 ou 720×1280 (largura ÷ altura = 0,5625).
5. Confira a **Duração**: no máximo 15 s.

### 9.3 Se não estiver em 9:16 (só o Montador)

1. Instale o ffmpeg pelo PowerShell: `winget install --id Gyan.FFmpeg -e`
   (sem winget, baixe em https://www.gyan.dev/ffmpeg/builds/ e use o `ffmpeg.exe` da pasta `bin`).
2. Feche e abra o PowerShell de novo.
3. Rode, na pasta do vídeo:

```powershell
ffmpeg -i C01-demo-bruto.mp4 -t 15 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" -c:v libx264 -pix_fmt yuv420p -an C01-demo.mp4
```

O comando corta para 9:16 pelo centro, limita a 15 s e **tira o áudio**, para não levar música junto.

4. Abra o `C01-demo.mp4`.
5. Confira se o ingresso continua inteiro na imagem.

> Se o Preview não tiver **Screen record**, grave a janela do Preview com a Ferramenta de Captura do Windows (**Win+Shift+R**; a confirmar se existe na versão do Windows do PC) e passe o vídeo pelo comando acima.

---

## Parte 10: Teste no celular (opcional, depende do Vini)

É o teste mais fiel, mas precisa de um celular logado na conta **Car Shop**. **Pule esta parte** se o Vini não estiver disponível: os testes da Parte 7 bastam para enviar.

Se for fazer, junte com os outros efeitos num único momento com o Vini.

1. No Effect House, clique em **Preview in TikTok**, na barra de cima (a confirmar na sua versão do programa: o lugar do botão).
2. Espere o QR code aparecer.
3. O Vini abre o **TikTok da conta Car Shop** no celular.
4. Ele toca em **Perfil**.
5. Ele toca no ícone de pessoa (**Adicionar amigos**).
6. Ele toca no ícone de **scanner**, no canto de cima.
7. Ele aponta para o QR da tela.
8. O efeito abre na câmera do TikTok.

> A dica ("Toque na tela") do formulário **não aparece** no teste pelo celular. Isso é normal; por isso o título já traz a etiqueta.
> Uma versão do guia oficial diz que o QR vale 14 dias ou até 30 contas. Se for verdade, outra conta também pode testar (a confirmar).

**Checklist no celular:**
- [ ] O título aparece e segue a cabeça.
- [ ] O toque faz girar. Em alguns Android o toque falha no teste; se falhar, tente outro aparelho antes de mexer no efeito.
- [ ] Dá para ler a carta na tela do celular, com o braço esticado.
- [ ] Ao apertar **gravar**, o efeito volta para o título.
- [ ] Com pouca luz e mexendo a cabeça, o ingresso não treme nem se descola.
- [ ] Os botões do TikTok (como "Adicionar som", em cima) não escondem a parte importante do ingresso com o rosto numa distância normal de selfie.

---

## Parte 11: Conferências antes de enviar

Faça estas 4 conferências **antes** de abrir o formulário.

### 11.1 Nome (INPI)

A equipe não achou nenhuma marca "Torcedômetro", mas achou "Torcidômetro" (com **i**), usado pelo Lance! por volta de 2012. Falta conferir no INPI.

1. Abra https://busca.inpi.gov.br/pePI/
2. Clique em **Continuar**, para pesquisar sem login (a confirmar: alguns guias dizem que a busca abre sem login, outros mandam entrar).
3. Clique em **Marca** (a confirmar: os nomes dos botões do site).
4. Digite `torcedometro` na busca por marca e pesquise.
5. Repita com `torcedômetro`, `torcidometro` e `torcidômetro` (com e sem acento, porque a busca pode diferenciar).
6. Decida:
   - **Não apareceu nada** (ou só pedidos **arquivados** ou **extintos**): use o nome **Torcedômetro**.
   - **Apareceu marca ativa ou pedido em andamento** com qualquer um dos dois nomes: use o nome **Que Torcedor Você É**.
   - **O site não abriu ou pediu login:** use **Torcedômetro** e anote no relatório que a busca não foi feita.
7. Anote no relatório o que apareceu (um print basta).

### 11.2 Conta

1. Confira de novo se o Effect House está logado na conta **Car Shop**. O efeito e o dinheiro do programa de recompensas ficam com a conta que envia.

### 11.3 Conteúdo

1. Confira se nenhuma imagem do projeto tem nome de time, escudo, marca, @ da conta, link ou chamada para comprar. As imagens da equipe já seguem essa regra. O risco é sobrar alguma imagem do template.
2. Confira se **não há som** ligado ao efeito.

### 11.4 Projeto salvo

1. Aperte **Ctrl+S**.
2. Copie a pasta do projeto `C01-torcedometro` para `Documentos\Efeitos\projetos\backup\`, como garantia.

---

## Parte 12: Enviar para aprovação

### 12.1 Abrir o formulário

1. Clique em **Submit**, no canto de cima à direita.
2. Espere abrir o formulário de envio. Ele é uma página web dentro de uma janela.

> Se o formulário abrir no navegador e pedir login no TikTok, chame o Vini (seção 0.6). A página de login por QR é <https://www.tiktok.com/login/qrcode>, e ele escaneia com o scanner do TikTok, como na seção 0.6. Não está confirmado se isso acontece.

### 12.2 O que preencher

| Campo | Obrigatório? | O que colocar |
|---|---|---|
| **Effect name** (nome) | Sim | `Torcedômetro` (12 caracteres; o limite é 25), ou o nome decidido na Parte 11.1. Se recusar o acento, use `Torcedometro`. Se recusar por nome repetido, use `Que Torcedor Você É` (19); se recusar de novo, `Roleta do Torcedor` (18). **Não** coloque "AI" no nome: o efeito não usa IA generativa. |
| **Effect icon** (ícone) | Sim | `assets\icone_162.png`. Se houver espaço para um 2º ícone, `assets\icone_alt_162.png`. |
| **Category** (categoria) | Sim | Escolha nesta ordem: uma opção parecida com **Randomizer** (sorteio); se não houver, **Funny** (engraçado); se não houver, **Interactive**. Anote no relatório a lista que apareceu. |
| **Hint** (dica) | Não, mas preencha | Se for texto livre: `Toque na tela`. Se for **lista pronta**, escolha a opção de tocar na tela (provavelmente **Tap screen**; a confirmar). |
| **Description** (descrição), se existir | — | `Toque na tela e a roleta mostra que torcedor você é: técnico de sofá, pé-frio, corneta oficial e mais 23 tipos. Serve pra qualquer time.` (136 caracteres). Se não couber: `Toque na tela e descubra que torcedor você é. Serve pra qualquer time.` (70 caracteres). |
| **Tags** | Não, mas preencha | `futebol`, `torcedor`, `sorteio`, `roleta`, `humor`. Se o campo só aceitar inglês: `football`, `fan`, `randomizer`, `roulette`, `funny`. Máximo de 5. |
| **Demo video** | Mande sempre | `Documentos\Efeitos\videos-demo\C01-demo.mp4` (ou o bruto, se ele já estava em 9:16) |
| **Challenge** (desafio) | Não | Deixe vazio. Se aparecer um desafio ativo de randomizer ou de futebol, anote o nome no relatório para a equipe avaliar depois. |
| **Comentários para a revisão** (pode se chamar "Additional comments" ou "Notes"; a confirmar) | Se existir | Cole o texto abaixo. |
| **Som / música** (se aparecer opção de ligar um som ao efeito) | Não | **Não ligue nenhum som.** |
| Qualquer outro campo que não esteja aqui | — | Deixe o padrão e anote no relatório. |

**Texto para os comentários.** Cole os dois, primeiro o inglês:

> Head randomizer. Tap the screen and a card above your head shows a funny type of football fan (couch coach, jinx, lucky socks, etc.). 26 original Portuguese texts and simple drawings. No teams, crests, kits, players, brands, betting or real people.
>
> Sorteio sobre a cabeça. A pessoa toca na tela e uma carta mostra que tipo de torcedor ela é (técnico de sofá, pé-frio, meia da sorte etc.). São 26 textos originais em português, com desenhos simples. Não há time, escudo, uniforme, jogador, marca, aposta nem pessoa real.

### 12.3 Enviar

1. Revise o nome: acento em "Torcedômetro" e nenhum espaço sobrando.
2. Confira se o ícone aparece com os cantos arredondados (o site faz isso sozinho).
3. Clique em **Submit** (ou **Enviar**).
4. Tire um print da tela de confirmação.
5. Salve o print em `Documentos\Efeitos\prints\C01-enviado.png`.

---

## Parte 13: Acompanhar o status

1. Abra a área **Manage Effects**, no Effect House ou no site https://effecthouse.tiktok.com/ com a conta logada (a confirmar na sua versão do programa: o caminho exato).
2. Ache o efeito pelo nome enviado.
3. Leia o status:

| Status | O que significa | O que fazer |
|---|---|---|
| **Draft** | Rascunho; o envio não terminou | Clique em **Finish submission** e termine. |
| **Under review** | Em análise (de 1 a 3 dias úteis) | Esperar. Conferir 1 vez por dia. |
| **Needs revision** | Reprovado, com motivo | Clique no status, leia o motivo, corrija (Parte 14) e reenvie. |
| **Active** | Aprovado e no ar | Anote a data no relatório e avise a equipe da nuvem para o vídeo de lançamento (legendas prontas em `textos.md`, seção 5). |
| **Deactivated** | Fora do ar | Leia o motivo e avise a equipe. |

> Para mudar algo enquanto o efeito está **Under review**, use **Withdraw from review**. Ele volta para Draft e precisa ser reenviado.

---

## Parte 14: Problemas comuns e soluções

| Problema | Causa provável | Solução |
|---|---|---|
| Não acho o template "Randomizer 2D" | Busca ou categoria diferente | Busque `Random`; olhe em Interactive, Face e Game. Se não achar, use a Parte 15. |
| Não existe **Import → Texture Sequence** | O menu mudou | Arraste a **pasta `cartas`** inteira do Explorador de Arquivos para o painel Assets. Ou importe as 26 imagens e procure uma opção de criar sequência com o botão direito (a confirmar). Anote o caminho certo no relatório. |
| A sequência veio com menos de 26 quadros | Arquivos não selecionados | Apague a sequência e importe de novo com **Ctrl+A**. |
| Cartas fora de ordem | Seleção fora de ordem | Apague e importe de novo, selecionando com **Ctrl+A** (fica em ordem de nome). |
| Troquei a imagem, mas continua a carta antiga do template | No Caso A, a troca foi feita no **Image**, não no **Animation Sequence** | Refaça a Parte 4.2 no componente certo. |
| Ingresso esticado (medalha virou ovo) | Proporção diferente de 2:1 | Parte 5.1: Size com altura = metade da largura, ou Stretch Mode = Fit. Ao mudar Scale, mude X e Y juntos. |
| Título e carta em lugares diferentes | Transform diferente nos dois objetos | Copie o **2D Transform** de um e cole no outro (Parte 5.2, passos 9 a 13). |
| Clicar no Preview não faz girar | **TapToSpin** desmarcado, ou clique fora da imagem | Marque **TapToSpin**. Clique **dentro** da imagem do Preview. |
| O título some sozinho antes do clique | TitleDelay curto, ou TapToSpin desmarcado | 1) Confira TapToSpin. 2) Aumente **TitleDelay** para `60` e teste (a confirmar: o efeito exato desse campo não está documentado). 3) Se continuar, troque a textura do Title para `titulo` (sem a etiqueta "TOQUE NA TELA") e anote no relatório. 4) Se o efeito ficar sem nada na tela até o toque, use o Plano C (Parte 15), que mantém o título até o toque. |
| O título não some | A caixa do randomizador aponta para outro objeto | Parte 6, passo 6: o campo de título tem que apontar para **Title**. |
| Sai sempre a mesma carta (ou só 2 ou 3) | O sorteio depende só do tempo | Parte 7.3: modo de reprodução **Shuffle** ou **Random**. Se não resolver, Plano C. |
| Texto da carta borrado | Compressão baixa ou imagem esticada | Volte a compressão para **High** (Parte 3.3) e confira a proporção (Parte 5.1). |
| Carta difícil de ler no celular | Ingresso pequeno demais | Aumente a **Scale** de Title e RandomAnimationSequence em 10% (X e Y juntos) e confira de novo se o ingresso inteiro cabe na tela. |
| Ingresso treme ou se descola do rosto | Rastreamento | Teste com mídia em vídeo e pouca luz. Baixe um pouco o **Position Y**: quanto mais longe da cabeça, mais treme. Efeito que treme é reprovado. |
| Pacote acima de 8 MB | Restos do template ou compressão | Parte 8: apagar o que sobrou e usar Medium só nas cartas. |
| **Test performance** falhou | Algo pesado no projeto | Clique em **View suggestions**. Este efeito não usa nada pesado (sem IA, sem segmentação), então o problema deve ser algo que sobrou do template. Apague o que não é usado. |
| Pediu login de novo ou está na conta errada | Login expirou | Chame o Vini (seção 0.6), com o link. |
| O programa pede atualização | Versão antiga | Baixe a mais nova em https://effecthouse.tiktok.com/download e instale por cima. |
| **Needs revision** por "propriedade intelectual", "marca" ou time | O revisor viu semelhança com clube ou marca | Responda ou reenvie explicando nos comentários que não há time, escudo nem marca, e que as cores (laranja, violeta, ouro e rosa) não são de nenhum clube. Se insistir, peça à equipe da nuvem para mudar as cores e gerar as imagens de novo. |
| **Needs revision** por causa do nome | Nome parecido com marca ou produto | Reenvie com o nome `Que Torcedor Você É`. |
| **Needs revision** por causa de uma carta | Carta vetada | Troque pela reserva, como explicado logo abaixo. |
| **Needs revision** por desempenho ou tremor | QA técnico | Rode o Test performance; teste com movimento; reduza o tamanho (Parte 8). |
| O formulário recusa o vídeo | Formato, duração ou tamanho | Parte 9.3 (ffmpeg); confira 9:16, até 15 s e até 32 MB. |

### Como trocar uma carta vetada pela reserva

As reservas já estão prontas, no mesmo formato:

| Se vetarem… | Use | Texto da reserva |
|---|---|---|
| carta 14 (REZA ATÉ NO ESCANTEIO) | `reserva_01.png` (R1) | CAMISA DA SORTE FURADA |
| carta 23 (FAZ CARREATA POR EMPATE) | `reserva_02.png` (R2) | CONHECE ATÉ O SUB-17 |
| qualquer outra carta | `reserva_03.png` (R3) e depois `reserva_04.png` (R4) | QUER DEMITIR O TÉCNICO · GRITA COM A TV |

1. Crie a pasta `assets\cartas_trocadas\`, **fora** da pasta `cartas`.
2. Mova a carta vetada (ex.: `cartas\carta_14.png`) para `cartas_trocadas\`.
3. Copie a reserva (ex.: `reservas\reserva_01.png`) para a pasta `cartas\`.
4. Renomeie a cópia com o nome da carta vetada (ex.: `carta_14.png`).
5. Confira se a pasta `cartas` continua com **exatamente 26** imagens.
6. No Effect House, apague a sequência `cartas_torcedor` do painel Assets.
7. Importe a pasta `cartas` de novo (Parte 3.2).
8. Ligue a nova sequência de novo (Parte 4.2). Se usar o Plano C, ligue também no campo **Sequencia Cartas** do script.
9. Teste (Parte 7) e reenvie.
10. Avise a equipe da nuvem qual carta foi trocada, para atualizar `textos.json`.

---

## Parte 15: Planos B e C (se o template falhar)

Use **só** se o template Randomizer 2D não existir, não abrir ou não passar nos testes da Parte 7.

| Plano | Quando usar | Esforço |
|---|---|---|
| **B: Visual Scripting do zero** | Não existe o template, mas os nós citados abaixo existem | médio |
| **C: script pronto em TypeScript** | O template existe, mas a lógica dele falha (título some sozinho, sorteio viciado, não gira) | baixo (é colar e ligar 3 campos) |
| **Assistente Effect House AI** | Travou em qualquer passo | baixo; pedidos prontos em `script\prompt-effect-house-ai.md` |

> **Montador:** para quem opera o programa por cliques remotos, o Plano C deve ser mais fácil que o B, porque não exige ligar fios entre caixinhas.

### Plano B: lógica do zero com Visual Scripting

Usa só nós citados na documentação oficial. Alguns nomes de campo estão marcados "a confirmar".

**Objetos:**
1. Crie um projeto vazio: na tela inicial, clique em **New Project** ou **Blank** (a confirmar).
2. Na **Hierarchy**, clique em **+** (**Add**).
3. Clique em **Face Effects**.
4. Clique em **Face Sticker**. Isso cria um objeto que segue o rosto, com uma imagem dentro.
5. Renomeie o objeto para `Titulo`.
6. Na imagem dele, ponha a textura `titulo_toque` (componente **Image → Texture**).
7. Repita os passos 2 a 4 para criar outro Face Sticker.
8. Renomeie para `Cartas`.
9. Na imagem de `Cartas`, ponha a sequência `cartas_torcedor` (Caso B da Parte 4.2), ou adicione o componente **Animation Sequence** e ponha a sequência nele (Caso A).
10. Acerte proporção, posição e tamanho dos dois (Parte 5).

**Ao abrir o efeito:**
1. Clique com o botão direito no painel **Visual Scripting** e adicione o nó **Start**.
2. Ligue **Start → Set Visibility**, com Target = `Titulo` e visível = **ligado**.
3. Ligue depois outro **Set Visibility**, com Target = `Cartas` e visível = **desligado**.

**Ao tocar:**
1. Adicione o nó **Screen Tap**.
2. Ligue **Screen Tap (Next) → Set Visibility**, com `Titulo` = **desligado**.
3. Ligue depois **Set Visibility**, com `Cartas` = **ligado**.
4. Ligue depois **Animation Sequence Controller**, entrada **Play**, com From = `0`, To = `25` e Loop = **ligado** (a confirmar na sua versão do programa: o nó pode ter outro nome, como **Set Animation Sequence**).
5. Ligue depois **Wait for Seconds**, com `2`.
6. Ligue depois **Index Generator**, no modo **Random**, com intervalo de **0 a 25** (a confirmar: os nomes dos campos de intervalo).
7. Ligue depois outro **Animation Sequence Controller**, entrada **Play**, com **From** e **To** ligados **na mesma saída** do Index Generator e Loop = **desligado**. Com From igual a To, a animação mostra só aquele quadro. Os quadros começam em 0: o 0 é a carta 01 e o 25 é a carta 26.

> **Cuidado:** o nó **Random** sorteia um número **novo cada vez que é lido**. Ligado em From e em To, ele daria 2 números diferentes. Se usar Random, guarde antes o número numa variável (**Set Variable**) e leia a variável nos dois campos.

**Ao gravar:**
1. Ache a opção **Reset on Record** no painel Visual Scripting (a confirmar).
2. Escolha **On**. Assim, ao apertar gravar, o efeito volta para o título.

### Plano C: script pronto (TypeScript)

**O que é:** o arquivo `script\TorcedometroController.ts` faz o mesmo que o template: título até o toque; no toque, título some em 0,3 s; cartas giram 2 s, desacelerando no fim; para numa carta sorteada; novo toque gira de novo; ao apertar gravar, volta ao título.
**O que foi conferido:** os nomes da API vieram do guia oficial de scripting, do tutorial oficial "VFX: Tap Burst" e dos arquivos de tipos do Effect House de um projeto público. O script passou na checagem de tipos e num teste de lógica fora do programa. **Ainda não foi rodado dentro do Effect House** (a confirmar no Preview).

1. Clique em **File → Save As**.
2. Dê o nome `C01-torcedometro-script`. Assim, o projeto original fica intacto.
3. No painel **Visual Scripting**, clique na caixa do randomizador.
4. Aperte **Delete**. Só nesta cópia: as duas lógicas não podem rodar juntas.
5. Se **RandomAnimationSequence** tiver o componente **Animation Sequence** (Caso A), desmarque esse componente no Inspector. Senão, ele troca a imagem sozinho a cada quadro e briga com o script.
6. No painel **Assets**, clique em **+** (**Add**).
7. Crie um script **TypeScript** (a confirmar na sua versão do programa: pode aparecer como **Script**, **Create → Script** ou **Script Component**).
8. Dê o nome `TorcedometroController`.
9. Abra o script (clique duplo; o programa abre um editor).
10. Apague todo o conteúdo.
11. Cole o conteúdo de `efeito-1-torcedometro\script\TorcedometroController.ts`.
12. Salve o script.
13. Na **Hierarchy**, clique em **+** (**Add**) e crie um objeto vazio (**Empty Object** ou parecido; a confirmar).
14. Renomeie o objeto para `Controle`.
    > Não ponha o script no Title nem no RandomAnimationSequence: o script esconde esses objetos e, escondido, ele mesmo pararia de rodar.
15. Com `Controle` selecionado, clique em **Add Component** no Inspector.
16. Escolha **TorcedometroController** (pode estar dentro de **Script**; a confirmar).
17. Preencha os campos do script no Inspector:
    - **Titulo**: arraste **Title** da Hierarchy;
    - **Cartas**: arraste **RandomAnimationSequence**;
    - **Sequencia Cartas**: arraste `cartas_torcedor` do painel Assets;
    - **Tempo Giro**: `2`;
    - **Tempo Some Titulo**: `0.3`;
    - **Girar De Novo No Toque**: marcado.
18. Aperte **Ctrl+S**.
19. Faça todos os testes da Parte 7.

**Se der erro:**
- Erro ao salvar ou compilar o script: use o **Pedido 3** de `script\prompt-effect-house-ai.md` no assistente Effect House AI.
- A carta pisca ou continua andando depois do giro: anote no relatório e use o **Pedido 1** ou o **Pedido 2** do mesmo arquivo.

### Assistente Effect House AI

A partir da versão 5.13 existe o assistente **Effect House AI**, que monta cenas e lógica a partir de um pedido escrito. A disponibilidade por conta ou região não foi confirmada. Os pedidos prontos, em inglês, estão em `efeito-1-torcedometro\script\prompt-effect-house-ai.md`.

Use o assistente para **destravar** um passo, não para mudar a ideia do efeito. Depois, confira tudo com os checklists da Parte 7.

---

## Parte 16: O que anotar no relatório

Em `Documentos\Efeitos\relatorio-montagem.md`, na seção do C01:

- Versão do Effect House instalada.
- Nomes reais dos objetos, componentes e campos que estavam diferentes deste guia (o que cada "a confirmar" virou).
- Caso A ou B da Parte 2 (onde a sequência fica).
- Size e Stretch Mode originais e os que você deixou. Se usou as imagens quadradas.
- Valores originais do template (FPS, TitleDelay, posição e escala) e os que você colocou.
- Se o título ficou até o toque, e qual título foi usado (`titulo_toque` ou `titulo`).
- Resultado do teste de sorteio (Parte 7.3): quantas cartas diferentes e a que mais repetiu.
- Plano usado: template, B ou C.
- Tamanho do pacote e resultado do Test performance.
- Resultado da busca no INPI e nome enviado.
- Lista de categorias e tipo de campo de hint (texto livre ou lista) que apareceram no formulário.
- Data e hora do envio, print da confirmação e status (Under review, Needs revision ou Active).

---

## Fontes consultadas

Documentação oficial do Effect House (lida por resumos de busca, porque o site não abre daqui):
- Tutorial do template Randomizer 2D: <https://effecthouse.tiktok.com/learn/guides/tutorials/template-tutorials/randomizer-2d>. Base para: Import → Texture Sequence (só as respostas, sem o título), objetos Title e RandomAnimationSequence, TapToSpin, TimeToSpin, TitleDelay e TitleFadeOutTime, reinício em Effect Start e Video Record Start, e Face Sticker.
- Animated Texture / Animation Sequence (modos Forward, Random, Ping-pong e Shuffle; FPS; o componente sobrescreve a textura do Image): https://effecthouse.tiktok.com/learn/guides/animation/animation-sequence/
- Nó Animation Sequence Controller (Play, From/To, Loop): https://effecthouse.tiktok.com/learn/3.8.0/guides/visual-scripting/nodes/utility/animation-sequence-controller
- Preparação de sequência de imagens (PNG/JPG, até 200 quadros, até 1024 px, menos de 1 MB cada, mesmo tamanho): https://effecthouse.tiktok.com/learn/guides/technical-guides/assets/asset-preparation/2d-texture-sequence
- Scripting em TypeScript (APJS): https://effecthouse.tiktok.com/learn/guides/api-reference/scripting-capability-usage-guide e o tutorial "VFX: Tap Burst" (toque pelo emissor global, `APJS.TouchPhase.Began`).
- Preview no programa: https://effecthouse.tiktok.com/learn/guides/publishing/preview-in-effect-house · Preview no celular: https://effecthouse.tiktok.com/learn/guides/publishing/preview-in-tiktok
- Vídeo demo: https://effecthouse.tiktok.com/learn/guides/publishing/demo-video-creation
- Teste de desempenho: https://effecthouse.tiktok.com/learn/guides/publishing/publish/test-effect-performance
- Envio: https://effecthouse.tiktok.com/learn/guides/publishing/publish/submit-your-effect · Ícone: https://effecthouse.tiktok.com/learn/guides/publishing/effect-icon-creation
- Status (Manage Effects): https://effecthouse.tiktok.com/learn/guides/management-and-growth/manage-your-effect

Outras:
- Tipos da API do Effect House (`APJS.d.ts` e `OrionDecorators.d.ts`) e exemplo de sequência com 1 quadro sorteado (`GameManager.ts`): projeto público https://github.com/christophusbeck/StatJack (pasta `StatJack_EH`). Versão do Effect House usada nele: não informada.
- Busca de marcas do INPI: https://busca.inpi.gov.br/pePI/ (acesso sem login citado por guias de terceiros; a confirmar).
- Pesquisa técnica da equipe: `tiktok-efeitos/pesquisa/03-tecnico-effect-house.md`.
