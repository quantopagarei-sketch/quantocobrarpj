# Guia de montagem: "Eu no grupo da família" (C08)

**Para quem é:** para quem vai montar o efeito no Effect House. Pode ser o Montador (o Claude que roda no PC do Vini) ou o próprio Vini, mesmo que nunca tenha aberto o programa.
**Versão do guia:** 1.1 (revisada pelo QA) · 06/11/2026 · escrito para o Effect House 5.1x no Windows.
**Tempo total:** cerca de 3h30 sem imprevistos. Reserve 5 horas.

> **Vini, se você estiver lendo:** não precisa fazer nada aqui. Este roteiro é para quem monta. Você só será chamado em dois casos, explicados na seção 0.6.

### Como ler as marcas

- **(a confirmar na sua versão do programa)**: a equipe não conseguiu ver essa tela, porque o site do Effect House não abre de onde pesquisamos. Se o nome do botão for diferente, procure algo parecido e **anote no relatório** como ele se chama de verdade.
- Os nomes de botões e painéis estão **em inglês e em negrito**, porque o programa é em inglês.
- Nos passos, "clique" é com o botão esquerdo. Quando for o direito, o passo diz "clique com o botão direito".

### O que vamos montar (resumo)

1. Em cima da cabeça aparece o balão **"NO GRUPO DA / FAMÍLIA, EU…"**.
2. A pessoa toca na tela, os balões giram por uns 2,5 segundos e param em 1 das 28 frases.
3. Com 2 pessoas na câmera, cada uma ganha o seu título e a sua frase.

A base é o template pronto **Randomizer 2D**. Ele já tem toda a lógica, então **não precisamos programar nada**. Só vamos trocar imagens e ajustar 4 valores.

**Ordem de trabalho:** primeiro montamos e salvamos a versão de **1 rosto** (Partes 1 a 7). Depois, numa cópia, fazemos a de **2 rostos** (Parte 8). Só a de 2 rostos vai para aprovação se passar em todos os testes. Se não passar, enviamos a de 1 rosto.

---

## Parte 0: Antes de começar

### 0.1 Links

| O quê | Link direto | Quem usa |
|---|---|---|
| Baixar o Effect House (Windows 10 ou mais novo; Mac tem versão para chip Apple e outra para Intel) | https://effecthouse.tiktok.com/download | Montador. Só se o programa ainda não estiver instalado. |
| Guia oficial de instalação e login | https://effecthouse.tiktok.com/learn/guides/getting-started/introduction-to-effect-house/download-and-login | Consulta |
| Arquivos da equipe (zip com tudo) | https://github.com/quantopagarei-sketch/quantocobrarpj/archive/refs/heads/main.zip | Montador |
| Aviso de que a equipe terminou (se der erro 404, ainda não terminou) | https://raw.githubusercontent.com/quantopagarei-sketch/quantocobrarpj/main/tiktok-efeitos/PRONTO-PARA-MONTAR.md | Montador |
| Tutorial oficial do template (em inglês) | https://effecthouse.tiktok.com/learn/guides/tutorials/template-tutorials/randomizer-2d | Consulta |
| Guia oficial de envio | https://effecthouse.tiktok.com/learn/guides/publishing/publish/submit-your-effect | Consulta |

> O link do zip só traz este efeito **depois** que a equipe publicar os arquivos. Antes de baixar, confira se o link do "Aviso" abre.

### 0.2 Copiar os arquivos para o computador

1. Baixe o zip pelo link da tabela.
2. Abra o zip.
3. Copie **só a pasta `tiktok-efeitos`** para `Documentos\Efeitos\`.
4. Confira se esta pasta existe:
   `Documentos\Efeitos\tiktok-efeitos\efeito-2-seu-papel-no-grupo\assets\`

> **Montador:** no Windows, "Documentos" fica em `%USERPROFILE%\Documents`. Se o OneDrive estiver ativo, pode ser `%USERPROFILE%\OneDrive\Documentos`. Para descobrir, rode no PowerShell: `[Environment]::GetFolderPath('MyDocuments')`.

### 0.3 Conferir os arquivos

Rode no PowerShell, trocando `<DOCS>` pelo caminho de Documentos:

```powershell
$a = "<DOCS>\Efeitos\tiktok-efeitos\efeito-2-seu-papel-no-grupo\assets"
(Get-ChildItem "$a\cartas\opcao_*.png").Count            # tem que dar 28
Get-ChildItem "$a\titulo.png", "$a\icone_162.png", "$a\icone_alt_162.png" | Select Name, Length
(Get-ChildItem "$a\cartas\*.png" | Measure-Object Length -Maximum).Maximum   # tem que ser menor que 1048576 (1 MB)
```

Se faltar arquivo, baixe o zip de novo. Se continuar faltando, avise a equipe da nuvem. Não chame o Vini por isso.

### 0.4 O que entra no efeito e o que não entra

| Arquivo (dentro de `assets\`) | Entra? | Para quê |
|---|---|---|
| `titulo.png` (512×512, fundo transparente) | **Sim** | Balão do título, "NO GRUPO DA / FAMÍLIA, EU…" |
| `cartas\opcao_01.png` … `opcao_28.png` (512×512 cada) | **Sim** | As 28 frases. Entram juntas como uma sequência de imagens (**Texture Sequence**), na ordem 01→28. |
| `icone_162.png` (162×162) | **No formulário de envio** | Ícone do efeito (obrigatório) |
| `icone_alt_162.png` (162×162) | **No formulário de envio** | 2º ícone (opcional) |
| `reservas\reserva_01..03.png` | Não | Só se uma frase for vetada (ver Parte 14) |
| `icone_grande_512.png`, `previa.png`, `gerar.py`, `LEIA-ME.md` | Não | Referência da equipe |

Todas as imagens do efeito têm o **mesmo quadro de 512×512**, com o balão sempre no mesmo lugar. Por isso a troca do título para a frase não "pula". A ponta do rabicho do balão fica a cerca de 90% da altura da imagem (y ≈ 459 de 512). Embaixo dela só tem margem transparente.

### 0.5 Tempo estimado

| Etapa | Tempo |
|---|---|
| Parte 0: baixar e conferir | 10 min |
| Partes 1 e 2: abrir o template e reconhecer as peças | 15 min |
| Partes 3 e 4: importar e trocar as imagens | 20 min |
| Parte 5: posição e tamanho | 20 min |
| Parte 6: ajustar a lógica | 15 min |
| Parte 7: testar 1 rosto no PC | 20 min |
| Parte 8: versão de 2 rostos e testes | 45 min |
| Partes 9 e 10: desempenho e vídeo demo | 30 min |
| Parte 12: envio | 15 min |
| **Total** | **≈ 3h30** (reserve 5 h) |

### 0.6 O que depende do Vini (o mínimo)

Pela ordem da equipe, o Vini **já deixou o Effect House instalado e logado** na conta Car Shop. Ele só é chamado se:

1. **O login cair**, ou se o programa estiver logado em outra conta. Mande para ele este passo, com o link: abrir o Effect House → aparece um QR code → no celular, abrir o **TikTok da conta Car Shop** → **Perfil** → ícone de pessoa (**Adicionar amigos**) → ícone de scanner no canto de cima → apontar para o QR → tocar em **Confirmar**. Guia com imagens: https://effecthouse.tiktok.com/learn/guides/getting-started/introduction-to-effect-house/download-and-login
   Tem que ser o scanner **de dentro do TikTok**. A câmera comum do celular não funciona.
2. **O teste no celular** (Parte 11). Ele é **opcional**. Se for feito, junte num único momento com os outros efeitos.

Todo o resto (montar, testar no PC, gravar o vídeo demo e enviar) é feito sem ele.

---

## Parte 1: Abrir o template

1. Abra o **Effect House**.
2. Confira a conta: no canto da tela inicial deve aparecer a foto ou o nome da conta **Car Shop**. Se for outra conta, **pare** e veja a seção 0.6 (a confirmar na sua versão do programa: onde a conta aparece).
3. Anote no relatório a versão do programa. Ela costuma estar no menu **Help → About** ou na tela inicial (a confirmar na sua versão do programa). A esperada é a 5.15 ou a 5.16.
4. Clique em **Templates**, no menu da esquerda da tela inicial.
5. Digite `Randomizer` na busca da tela inicial.
6. Clique no card **Randomizer 2D**. Atenção: **2D**, não 3D.
7. Clique em **Create** ou **Open** para abrir o template (a confirmar na sua versão do programa: o nome do botão).
8. Espere o projeto carregar. O programa pode baixar o template, o que leva até 1 minuto.

**Se não achar "Randomizer 2D":**
- procure por `Random`, `Randomizer` ou `Random Image`;
- olhe nas categorias **Interactive**, **Face** e **Game**;
- se não achar mesmo, use o **Plano B** (Parte 15).

9. Salve logo: menu **File → Save As**.
10. Crie a pasta `Documentos\Efeitos\projetos\` se ela não existir.
11. Dê o nome `C08-grupo-familia-1rosto`.
12. Clique em **Salvar**.

> A partir daqui, aperte **Ctrl+S** a cada parte terminada.

---

## Parte 2: Reconhecer as peças do template

O programa tem painéis. Os que vamos usar:

| Painel | Onde fica (costuma) | Para quê |
|---|---|---|
| **Hierarchy** | à esquerda, em cima | lista os objetos da cena |
| **Assets** | à esquerda, embaixo | lista os arquivos importados |
| **Inspector** | à direita | mostra as propriedades do objeto selecionado |
| **Preview** | à direita ou no centro | mostra o efeito num rosto de exemplo |
| **Visual Scripting** | embaixo | mostra a lógica, com caixinhas ligadas por fios |

Se algum painel sumir, procure no menu **Window** (a confirmar na sua versão do programa).

1. Olhe o painel **Hierarchy**.
2. Ache o objeto **Title**. É onde fica a imagem do título.
3. Ache o objeto **RandomAnimationSequence**. É onde fica a sequência de imagens que gira.
4. Clique em **Title**.
5. Olhe o **Inspector** e anote no relatório os componentes que aparecem. O esperado é algo como **2D Transform**, **Image** e **Face Sticker** (a confirmar na sua versão do programa).
6. Clique em **RandomAnimationSequence**.
7. Anote os componentes. O esperado é **2D Transform**, **Image**, **Animation Sequence** e **Face Sticker**.
8. Abra o painel **Visual Scripting**.
9. Ache a caixinha grande do randomizador. É um **subgraph**, uma caixa que guarda vários nós dentro.
10. Clique nela e anote os valores dos campos **TapToSpin**, **TimeToSpin**, **TitleDelay** e **TitleFadeOutTime**. Eles podem aparecer na própria caixa ou no Inspector.

> Se os nomes forem um pouco diferentes (por exemplo, "Title_A" ou "Randomizer"), siga com os nomes que existem e anote no relatório.

---

## Parte 3: Importar as imagens

### 3.1 Título

1. No painel **Assets**, clique no botão **+** (**Add**).
2. Clique em **Import**.
3. Clique em **From Computer** (a confirmar na sua versão do programa: pode aparecer como "Texture" ou "Image").
4. Vá até `Documentos\Efeitos\tiktok-efeitos\efeito-2-seu-papel-no-grupo\assets\`.
5. Selecione `titulo.png`.
6. Clique em **Abrir**.
7. Confira se `titulo` apareceu no painel Assets.

### 3.2 As 28 cartas (sequência)

As cartas **não** são importadas uma a uma como imagens soltas. Elas entram juntas como **Texture Sequence**.

1. No painel **Assets**, clique em **+** (**Add**).
2. Clique em **Import**.
3. Clique em **Texture Sequence**.
4. Vá até a pasta `assets\cartas\`.
5. Faça uma das duas coisas, conforme o que a janela pedir (a confirmar na sua versão do programa):
   - se a janela pedir **arquivos**, aperte **Ctrl+A** para selecionar os 28 PNG e clique em **Abrir**;
   - se a janela pedir **uma pasta**, selecione a pasta `cartas` e clique em **Selecionar pasta**.
6. Confira se apareceu no painel Assets **uma** sequência (provavelmente chamada `cartas` ou `opcao`).
7. Clique nela e confira no **Inspector** se tem **28 frames** (quadros).
8. Renomeie a sequência para `cartas_grupo`: clique com o botão direito → **Rename** (opcional, só para organizar).

> **A ordem importa pouco para o sorteio, mas deve estar certa.** Os nomes têm zero na frente (01, 02 … 28), então a ordem alfabética já é a certa. Se o Inspector mostrar outra ordem, apague a sequência e importe de novo.

### 3.3 Compressão das imagens

1. Clique em `titulo` no painel Assets.
2. No **Inspector**, confira a compressão. Deixe **Automatic** (512 px) ou **Manual 512 + High**. As imagens já têm 512 px, então não há perda.
3. Faça o mesmo com a sequência `cartas_grupo`.

> **Não** use Medium nem Low agora. Isso só entra se o tamanho do pacote passar do limite (Parte 9).

---

## Parte 4: Trocar as imagens do template

### 4.1 Título

1. Na **Hierarchy**, clique em **Title**.
2. No **Inspector**, ache o componente **Image**.
3. Clique no campo **Texture**.
4. Escolha `titulo` na lista. Também dá para arrastar `titulo` do painel Assets para o campo.
5. Confira no **Preview** se o balão "NO GRUPO DA / FAMÍLIA, EU…" apareceu sobre a cabeça.

### 4.2 Cartas

1. Na **Hierarchy**, clique em **RandomAnimationSequence**.
2. No **Inspector**, ache o componente **Animation Sequence**. Atenção: **não** é o componente Image.
3. Clique no campo da sequência. Ele pode se chamar **Texture Sequence**, **Texture** ou **Animated Texture** (a confirmar na sua versão do programa).
4. Escolha `cartas_grupo` na lista.
5. **Não mexa** no campo **FPS**. Pelo tutorial oficial, o template gira a animação a 100 quadros por segundo e sorteia o tempo do giro (cerca de 0,25 s para mais ou para menos do TimeToSpin), de propósito: é isso que deixa o sorteio aleatório. Anote no relatório o valor que aparece.
6. **Não mexa** na textura do componente **Image** desse objeto. O Animation Sequence troca essa textura sozinho a cada quadro, então qualquer coisa colocada ali é apagada.

### 4.3 Limpar as imagens antigas do template

Isso deixa o pacote mais leve.

1. No painel **Assets**, ache o título e a sequência originais do template (os que vieram com ele).
2. Clique com o botão direito em cada um.
3. Clique em **Delete**.
4. Se o programa avisar que o asset ainda está em uso, **cancele**: alguma troca da Parte 4.1 ou 4.2 não foi feita. Volte e confira.

---

## Parte 5: Posição e tamanho sobre a cabeça

O componente **Face Sticker** já faz o balão seguir a cabeça. Aqui só ajustamos onde ele fica e o tamanho.

**Regras:**
- **Title** e **RandomAnimationSequence** precisam ter **exatamente a mesma posição e o mesmo tamanho**, porque as imagens usam o mesmo quadro.
- O objeto tem que ficar **quadrado** (proporção 1:1). O teste é olhar o círculo branco com o desenho, em cima do balão: ele tem que parecer **um círculo, não um ovo**.
- **Posição:** a ponta do rabicho deve ficar **logo acima do cabelo**, sem cobrir a testa nem os olhos.
- **Largura:** o balão deve ter **cerca de 1,5 vez a largura da cabeça**.

### Passos

1. Na **Hierarchy**, clique em **RandomAnimationSequence**.
2. No **Inspector**, abra o componente **2D Transform**.
3. Anote os valores atuais de **Position**, **Scale** e **Size**, se existir (a confirmar na sua versão do programa: quais campos aparecem).
4. Confira a proporção:
   - se houver **Size** (largura e altura), deixe os dois números iguais;
   - se houver só **Scale X / Y**, deixe X igual a Y.
5. Olhe o **Preview** e confira se o círculo branco está redondo.
6. Ajuste **Scale** (ou **Size**) até o balão ter cerca de 1,5 cabeça de largura. Mude sempre os dois valores juntos.
7. Ajuste **Position Y** até a ponta do rabicho ficar logo acima do cabelo.
8. Deixe **Position X** no centro (normalmente 0).
9. Troque o rosto do Preview: abra a lista de mídias do painel **Preview** e escolha outro rosto de exemplo.
10. Repita a conferência nos **3 rostos de exemplo** e escolha um meio-termo que sirva para todos.
11. Clique nos **três pontinhos** (⋮) do componente **2D Transform**.
12. Clique em **Copy**.
13. Na **Hierarchy**, clique em **Title**.
14. Clique nos **três pontinhos** do **2D Transform** do Title.
15. Clique em **Paste** (pode aparecer como **Paste Component Values**; a confirmar na sua versão do programa).
16. Confira no **Preview** se o título e as cartas ocupam o mesmo lugar.

> **Para ver uma carta parada durante o ajuste:** clique no Preview para sortear (Parte 7). Depois do giro, a carta fica parada e dá para ajustar com calma.

---

## Parte 6: A lógica (Visual Scripting)

**O template já faz toda a lógica.** Não crie nós e não apague nós. Só mude os 4 valores abaixo, que ficam na caixa do randomizador (o subgraph).

| Campo | O que faz | Valor para o C08 | Por quê |
|---|---|---|---|
| **TapToSpin** | Ligado: o giro só começa quando a pessoa toca na tela. Desligado: começa sozinho ao abrir o efeito e de novo ao apertar o botão de gravar. | **Ligado (marcado)** | A dica do efeito é "Toque na tela", e a pessoa escolhe a hora, por exemplo depois de chamar a mãe para o vídeo. |
| **TimeToSpin** | Quanto tempo as cartas giram antes de parar (segundos) | **2.5** | Dá suspense sem cansar e cabe bem num vídeo de 15 s. |
| **TitleFadeOutTime** | Quanto tempo o título leva para sumir (segundos) | **0.3** | Troca rápida e limpa. |
| **TitleDelay** | Tempo de espera do título antes de girar. Pesa mais quando TapToSpin está desligado. | **Deixe o valor do template** e anote no relatório | Com TapToSpin ligado, o tempo é decidido pelo toque. |

### Passos

1. Abra o painel **Visual Scripting**.
2. Clique na caixa do randomizador.
3. Marque **TapToSpin**.
4. Digite `2.5` em **TimeToSpin**.
5. Digite `0.3` em **TitleFadeOutTime**.
6. Confira se a caixa do randomizador aponta para os objetos certos: nos campos de objeto deve aparecer **Title** e **RandomAnimationSequence**.
7. Aperte **Ctrl+S**.
8. Teste rápido: clique no Preview. Se com **TapToSpin** marcado o giro começar **sozinho** (sem clique) ou o clique **não** girar, a caixa está com o comportamento invertido nesta versão (as páginas oficiais descrevem esse campo de jeitos um pouco diferentes). Nesse caso, inverta a marcação, teste de novo e anote no relatório qual posição deixou o giro "só no toque".

### Como a lógica funciona (só para entender)

- **Ao abrir o efeito** e **ao apertar o botão de gravar no TikTok**, o template volta ao começo: o título aparece e as cartas ficam escondidas. A documentação oficial confirma que os eventos "Effect Start" e "Video Record Start" reiniciam o randomizador.
- **No toque**, o título some em 0,3 s e as cartas giram por 2,5 s. Depois a animação para numa carta.
- **Se o TapToSpin estiver desligado,** o toque não faz nada. Por isso ele tem que estar marcado.
- Se a caixa tiver algum campo com **intervalo de números** (por exemplo "Random 0–9", "Count" ou "Frames"), mude para **0 a 27**, ou para **28** se o campo pedir a quantidade (a confirmar na sua versão do programa). A pesquisa indica que a versão oficial lê sozinha a quantidade de quadros, mas um fork da comunidade tinha esse número fixo.

### Sobre script em código (TypeScript)

O Effect House aceita scripts em TypeScript, mas **este efeito não precisa de código**. A equipe também não conseguiu confirmar os comandos da API para trocar quadro de sequência e ler toque, e um script não testado seria mais arriscado que o template. Por isso **não incluímos script em código**. Se o template der problema, use o **Plano B** (Parte 15, montagem do zero só com nós confirmados) ou o prompt para o assistente **Effect House AI** que está em `script/prompt-effect-house-ai.md`.

---

## Parte 7: Testar no PC (versão de 1 rosto)

### 7.1 Como testar no Preview

O clique do mouse **dentro da janela do Preview** simula o toque na tela.

1. No painel **Preview**, abra a lista de mídias (o menu de cima).
2. Escolha um rosto de exemplo com **1 pessoa**.
3. Clique dentro da imagem do Preview.
4. Veja o giro e a carta final.

> Também dá para testar com a webcam: há um botão de câmera ao lado do menu de mídias. Isso é opcional.

### 7.2 Checklist (marque tudo antes de seguir)

- [ ] Ao abrir, aparece **só o título**, sem nenhuma carta por trás.
- [ ] O título está **inteiro na tela**, não cortado em cima, nos 3 rostos de exemplo.
- [ ] O círculo do emoji está **redondo** (nada esticado).
- [ ] A ponta do rabicho fica **acima do cabelo**, sem cobrir os olhos.
- [ ] O título **acompanha a cabeça** quando o rosto se mexe. Use uma mídia de vídeo, não só foto.
- [ ] Ao clicar, o título **some** e as cartas **giram**.
- [ ] O giro dura **cerca de 2,5 s** e **para** numa carta.
- [ ] A carta parada **dá para ler** (texto nítido, sem borrão).
- [ ] A carta continua **parada e presa na cabeça** enquanto o rosto se mexe.
- [ ] Não aparece **borda escura** nem quadrado em volta do balão. A transparência tem que estar OK.
- [ ] Quando o rosto **sai** da imagem, o balão **some**, sem ficar flutuando na tela.
- [ ] Clicar **de novo** depois do resultado faz o quê? Anote no relatório (gira de novo, ou nada). As duas coisas são aceitáveis.

### 7.3 Teste do sorteio (importante)

Esse teste mostra se o sorteio é aleatório de verdade.

1. Clique no Preview e anote o número da carta que saiu. O número está no nome do arquivo (veja a tabela em `textos.md`, seção 3).
2. Para voltar ao título, reinicie o preview (a confirmar na sua versão do programa: botão de **reset/refresh** do Preview) ou clique de novo, se o template permitir girar de novo.
3. Repita até ter **15 sorteios**.
4. Avalie:
   - **OK:** saíram **pelo menos 9 cartas diferentes** e não há padrão (não é sempre a mesma, nem uma sequência fixa).
   - **Problema:** saem sempre as mesmas 2 ou 3 cartas, ou sempre a mesma. Aplique a correção abaixo.

**Correção se o sorteio estiver viciado:**
1. Clique em **RandomAnimationSequence**.
2. No componente **Animation Sequence**, ache o modo de reprodução. Ele pode se chamar **Play Mode**, **Mode** ou **Order** (a confirmar na sua versão do programa).
3. Troque de **Loop** para **Shuffle**. Se não tiver Shuffle, use **Random**. A documentação oficial descreve Random como quadros em ordem aleatória e Shuffle como ordem embaralhada sem repetir o quadro anterior.
4. Repita os 15 sorteios.
5. Anote o resultado no relatório.

### 7.4 Salvar a versão de 1 rosto

1. Aperte **Ctrl+S**. O projeto `C08-grupo-familia-1rosto` fica guardado como reserva.

---

## Parte 8: Versão de 2 rostos

### 8.1 Criar a cópia do projeto

1. Clique em **File → Save As**.
2. Dê o nome `C08-grupo-familia-2rostos`.
3. Clique em **Salvar**. Agora você está trabalhando na cópia, e a versão de 1 rosto fica intacta.

### 8.2 Duplicar os objetos

1. Na **Hierarchy**, clique com o botão direito em **Title**.
2. Clique em **Duplicate** (ou aperte **Ctrl+D**; a confirmar na sua versão do programa).
3. Renomeie a cópia para `Title_B`: botão direito → **Rename**.
4. Clique com o botão direito em **RandomAnimationSequence**.
5. Clique em **Duplicate**.
6. Renomeie a cópia para `RandomAnimationSequence_B`.
7. Confira se as cópias ficaram **no mesmo nível** dos originais na Hierarchy, e não dentro deles.

> Se o objeto original estiver dentro de um "pai" (por exemplo, um objeto Face Sticker com os dois filhos), duplique o **pai** inteiro e renomeie os filhos com `_B`.

### 8.3 Ligar cada cópia ao 2º rosto

1. Clique em **Title_B**.
2. No **Inspector**, ache o componente **Face Sticker**.
3. Clique no campo **Which Face**.
4. **Desmarque Face 0** e **marque Face 1**. Esse campo aceita mais de uma escolha, então confira se **só** a Face 1 ficou marcada.
5. Clique em **RandomAnimationSequence_B**.
6. Repita: **Which Face** = só **Face 1**.
7. Clique em **Title** (o original).
8. Confira **Which Face** = só **Face 0**.
9. Clique em **RandomAnimationSequence** (o original).
10. Confira **Which Face** = só **Face 0**.

> Se o **Which Face** estiver no objeto "pai" e não nos filhos, faça a troca no pai duplicado (a confirmar na sua versão do programa).

### 8.4 Duplicar a lógica

O tutorial oficial faz assim: ele duplica os nós do randomizador e aponta as cópias para os objetos `_B`. No tutorial, esses nós aparecem marcados em rosa.

1. Abra o painel **Visual Scripting**.
2. Selecione a caixa do randomizador (o subgraph). Se houver nós de objeto ligados a ela (Title e RandomAnimationSequence), segure **Ctrl** e clique neles também.
3. Aperte **Ctrl+C**.
4. Clique num espaço vazio do painel.
5. Aperte **Ctrl+V**.
6. Na cópia, troque o objeto **Title** por **Title_B**: arraste `Title_B` da Hierarchy para o campo.
7. Na cópia, troque **RandomAnimationSequence** por **RandomAnimationSequence_B**.
8. Ligue na cópia os **mesmos fios de entrada** que chegam na caixa original (por exemplo, o fio de início e o de toque). Puxe o fio da saída do nó de evento até a entrada da cópia.
9. Na cópia, use os mesmos valores da Parte 6: **TapToSpin** marcado, **TimeToSpin** `2.5`, **TitleFadeOutTime** `0.3`.
10. Aperte **Ctrl+S**.

Com isso, **um toque gira os dois**. Cada pessoa ganha o seu resultado.

> **Se o template já vier com um exemplo pronto de "2 answers"** (dois randomizadores), use esse exemplo em vez de duplicar (a confirmar na sua versão do programa).

### 8.5 Testar com 1, 2 e 3 rostos

1. No **Preview**, abra a lista de mídias.
2. Escolha uma mídia de **duas pessoas** (deve ter o nome "Two Person" ou parecido; a documentação oficial cita essa mídia em outros templates). Se não houver, use **+ Add media** e escolha um vídeo seu com 2 pessoas.
3. Clique no Preview.

**Checklist de 2 rostos:**
- [ ] Com **2 rostos**, aparecem **2 títulos**, um em cada cabeça.
- [ ] Um clique gira **os dois**.
- [ ] Cada cabeça fica com **a sua** carta, e cada carta segue a cabeça certa.
- [ ] Os dois balões **não se encostam** quando as pessoas estão lado a lado. Se encostarem, reduza a **Scale** dos 4 objetos (A e B) em 10% e teste de novo, no máximo 2 vezes.
- [ ] Com **1 rosto** (volte para uma mídia de 1 pessoa), **não aparece** nenhum segundo balão flutuando nem preso no canto da tela.
- [ ] Com **3 rostos** (se houver mídia assim), a 3ª pessoa fica **sem balão** e nada quebra.
- [ ] Quando a 2ª pessoa sai e volta, o balão dela some e volta junto com ela.

**Teste de independência (importante):**
1. Faça **10 sorteios** com 2 rostos.
2. Anote o par de cartas de cada sorteio (A e B).
3. Avalie:
   - **OK:** os pares variam e só às vezes saem iguais. Pela conta, iguais deve ser raro, perto de 1 em 28.
   - **Problema:** as duas cartas saem **sempre iguais**, ou sempre com a mesma distância (por exemplo, B é sempre a carta seguinte de A). Isso acontece porque as duas animações começam juntas e param no mesmo instante.

**Correção se A e B estiverem "grudados":**
1. Clique em **RandomAnimationSequence_B**.
2. No componente **Animation Sequence**, troque o modo de reprodução para **Shuffle** ou **Random** (Parte 7.3).
3. Faça o mesmo em **RandomAnimationSequence**.
4. Se ainda estiver grudado, mude **TimeToSpin** só da cópia B para `2.8`.
5. Repita os 10 sorteios.

### 8.6 Decidir qual versão vai para aprovação

| Situação | O que enviar |
|---|---|
| Todos os itens da 8.5 passaram | **2 rostos** (`C08-grupo-familia-2rostos`) |
| O 2º balão aparece sem 2º rosto, ou o teste de independência falhou mesmo depois da correção | **1 rosto** (`C08-grupo-familia-1rosto`). Anote no relatório o que falhou. |

> Não gaste mais de 1 hora tentando consertar a versão de 2 rostos. A de 1 rosto é um efeito completo.

---

## Parte 9: Desempenho e tamanho

1. Abra o projeto escolhido na 8.6.
2. Na barra de cima, ache o indicador de tamanho do efeito.
3. Clique em **Click to update** para atualizar o número.
4. Anote o tamanho no relatório.
   - **Até 5 MB:** ótimo, siga em frente.
   - **Entre 5 e 8 MB:** aceitável. O limite é 8 MB, mas tente diminuir com os passos abaixo.
   - **Acima de 8 MB:** não dá para enviar. Diminua com os passos abaixo.
5. Na barra de cima, clique em **Test performance**.
6. Clique em **Run test**.
7. Espere cerca de 30 segundos.
8. Se passar, siga para a Parte 10.
9. Se falhar, clique em **View suggestions** e veja a Parte 14.

**Para diminuir o tamanho, nesta ordem:**
1. Apague do painel Assets tudo que sobrou do template e não é usado (Parte 4.3).
2. Clique na sequência `cartas_grupo` e mude a compressão para **Manual → 512 → Medium**.
3. Confira no Preview se o texto das cartas continua nítido. Se borrou, volte para **High**.
4. Deixe o **título** sempre em **High**.

> Passar no Test performance **não garante** a aprovação, mas falhar nele quase garante a reprovação.

---

## Parte 10: Vídeo demo (sem precisar do Vini)

O formulário pede um vídeo curto mostrando o efeito. Ele não é público, só a equipe de revisão vê. Regras: **9:16 (em pé), MP4 ou MOV, até 15 segundos, até 32 MB.**

### 10.1 Gravar no próprio Effect House

1. No **Preview**, escolha um aparelho com tela **9:16** na lista de aparelhos do canto de baixo à esquerda. Um exemplo é um iPhone 8 ou um aparelho de 1080×1920. Telas mais compridas, como a do iPhone X em diante, não são 9:16 (a confirmar na sua versão do programa: quais aparelhos aparecem).
2. Escolha a mídia:
   - versão de 2 rostos: a mídia de **duas pessoas**;
   - versão de 1 rosto: o rosto de exemplo onde o balão ficou melhor.
3. Volte o efeito para o começo, com o título aparecendo.
4. Clique em **Screen record** no painel Preview (a confirmar na sua versão do programa: o nome e o lugar do botão).
5. Siga o roteiro abaixo.
6. Pare a gravação antes de 15 segundos.
7. Salve em `Documentos\Efeitos\videos-demo\C08-demo-bruto.mp4`.

**Roteiro do vídeo (até 14 s):**

| Tempo | O que acontece |
|---|---|
| 0–2 s | Título parado sobre a cabeça |
| ≈ 2 s | Clique no Preview |
| 2–5 s | Giro |
| 5–9 s | Resultado parado, com o rosto se mexendo um pouco |
| ≈ 9 s | Clique de novo, se o template girar de novo (se não girar, deixe o resultado até o fim) |
| 9–14 s | Segundo giro e segundo resultado |

### 10.2 Conferir o formato

1. No Explorador de Arquivos, clique com o botão direito no vídeo.
2. Clique em **Propriedades**.
3. Abra a aba **Detalhes**.
4. Confira a **Largura** e a **Altura**. Tem que ser em pé e 9:16, por exemplo 1080×1920 ou 720×1280. A conta largura ÷ altura deve dar 0,5625.
5. Confira a **Duração**: no máximo 15 s.

### 10.3 Se não estiver em 9:16 (só o Montador)

1. Instale o ffmpeg pelo PowerShell: `winget install --id Gyan.FFmpeg -e`
2. Feche e abra o PowerShell de novo.
3. Rode, na pasta do vídeo:

```powershell
ffmpeg -i C08-demo-bruto.mp4 -t 15 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" -c:v libx264 -pix_fmt yuv420p -an C08-demo.mp4
```

O comando corta para 9:16 pelo centro, limita a 15 s e **tira o áudio**, para não levar nenhuma música junto.

4. Abra o `C08-demo.mp4` e confira se o balão continua inteiro na imagem.

> Se o Preview não tiver **Screen record**, grave a janela do Preview com a Ferramenta de Captura do Windows (**Win+Shift+R**; a confirmar se está disponível na versão do Windows do PC) e passe pelo comando acima.

---

## Parte 11: Teste no celular (opcional, depende do Vini)

Este teste é o mais fiel, mas precisa de um celular logado na conta **Car Shop**. **Pule esta parte** se o Vini não estiver disponível: os testes das Partes 7 e 8 são suficientes para enviar.

Se for fazer, junte com os outros efeitos num único momento com o Vini.

1. No Effect House, clique em **Preview in TikTok** (na barra de cima; a confirmar na sua versão do programa: o lugar do botão).
2. Espere o QR code aparecer.
3. O Vini abre o **TikTok da conta Car Shop** no celular.
4. Ele toca em **Perfil**.
5. Ele toca no ícone de pessoa (**Adicionar amigos**).
6. Ele toca no ícone de **scanner**, no canto de cima.
7. Ele aponta para o QR da tela.
8. O efeito abre na câmera do TikTok.

> A dica ("Toque na tela") **não aparece** no teste do celular. Isso é normal.
> Uma versão do guia oficial diz que o QR vale 14 dias ou até 30 contas. Se for verdade, outra conta também pode testar (a confirmar).

**Checklist no celular:**
- [ ] O título aparece e segue a cabeça.
- [ ] O toque faz girar. Em alguns Android o toque falha no teste; se falhar, tente em outro aparelho antes de mudar o efeito.
- [ ] A carta é legível na tela do celular.
- [ ] Ao apertar **gravar**, o efeito volta para o título.
- [ ] Com pouca luz e mexendo a cabeça, o balão não treme nem descola.
- [ ] (2 rostos) Com 2 pessoas, cada uma ganha a sua carta.

---

## Parte 12: Enviar para aprovação

### 12.1 Abrir o formulário

1. Abra o projeto escolhido na Parte 8.6.
2. Aperte **Ctrl+S**.
3. Clique em **Submit**, no canto de cima à direita.
4. Espere abrir o formulário de envio. Ele é uma página web dentro de uma janela.

> Se o formulário abrir no navegador e pedir login no TikTok, é um caso de "chamar o Vini" (seção 0.6). A página de login por QR é <https://www.tiktok.com/login/qrcode> e ele escaneia com o scanner do TikTok, como no passo 0.6. Não está confirmado se isso acontece.

### 12.2 O que preencher

| Campo | Obrigatório? | O que colocar |
|---|---|---|
| **Effect name** (nome) | Sim | `Eu no grupo da família` (22 caracteres; o limite é 25). Se recusar por nome repetido, use `Meu papel no grupo`; se recusar de novo, `Grupo da família`. **Não** coloque "AI" no nome: o efeito não usa IA generativa. |
| **Effect icon** (ícone) | Sim | `assets\icone_162.png`. Se houver espaço para um 2º ícone, `assets\icone_alt_162.png`. |
| **Category** (categoria) | Sim | A mais próxima de **Funny** (engraçado). Se não houver, **Interactive**. Anote no relatório a lista que apareceu. |
| **Hint** (dica) | Não, mas preencha | Texto livre: `Toque na tela`. Se for a versão de 2 rostos e couber, `Toque e chame alguém`. Se o campo for uma **lista pronta**, escolha a opção de tocar na tela ("Tap the screen" ou parecido). |
| **Tags** | Não, mas preencha | `grupo da família`, `família`, `sorteio`, `humor`, `randomizer`. Se não aceitar espaço ou acento: `grupodafamilia`, `familia`, `sorteio`, `humor`, `randomizer`. Reservas: `meme`, `brasil`, `dupla`. |
| **Demo video** | Mande sempre | `Documentos\Efeitos\videos-demo\C08-demo.mp4` (ou o bruto, se já estava em 9:16) |
| **Challenge** (desafio) | Não | Se a lista mostrar um desafio **ativo** de sorteio/randomizer (ou de humor) que combine com o efeito, selecione: não atrapalha o Rewards e pode dar prêmio extra. Se não houver nenhum que combine, deixe vazio. Anote no relatório os desafios que apareceram. |
| **Comentários para a revisão** (pode se chamar "Additional comments" ou "Notes"; a confirmar) | Se existir | Cole o texto abaixo. |
| **Som / música** (se aparecer opção de ligar um som ao efeito) | Não | **Não ligue nenhum som.** |
| Qualquer outro campo que não esteja aqui | — | Deixe o padrão e anote no relatório. |

**Texto para os comentários.** Cole os dois, primeiro o inglês:

> Head randomizer. Tap the screen to find out your role in the family group chat. There are 28 light-humor results in Brazilian Portuguese, such as "I send 4-minute voice messages" and "I only show up to say happy birthday". No app names, logos or app-like visuals are used.
>
> Sorteio sobre a cabeça. A pessoa toca na tela e descobre qual é o seu papel no grupo da família. São 28 resultados de humor leve, como "mando áudio de 4 minutos" e "só apareço pra dar parabéns". O efeito não usa nome, logo nem visual de nenhum aplicativo de mensagem.

**Só se a versão enviada for a de 2 rostos**, acrescente no fim:

> With two people on camera, each person gets their own result.
> Com duas pessoas na câmera, cada uma ganha o seu resultado.

### 12.3 Enviar

1. Revise o nome: acento em "família" e sem espaço sobrando.
2. Confira se o ícone aparece com os cantos arredondados (o site faz isso sozinho).
3. Clique em **Submit** (ou **Enviar**).
4. Tire um print da tela de confirmação.
5. Salve o print em `Documentos\Efeitos\prints\C08-enviado.png`.

---

## Parte 13: Acompanhar o status

1. Abra a área **Manage Effects** (no Effect House ou no site https://effecthouse.tiktok.com/ logado; a confirmar na sua versão do programa: o caminho exato do menu).
2. Ache **Eu no grupo da família**.
3. Leia o status:

| Status | O que significa | O que fazer |
|---|---|---|
| **Draft** | Rascunho, envio não terminado | Clique em **Finish submission** e termine. |
| **Under review** | Em análise (normalmente 2 a 3 dias úteis; às vezes 1) | Esperar. Conferir 1 vez por dia. |
| **Needs revision** | Reprovado, com motivo | Clique no status, leia o motivo, corrija (Parte 14) e reenvie. |
| **Active** | Aprovado e no ar | Anotar a data no relatório e avisar a equipe da nuvem para o vídeo de lançamento (legendas prontas em `textos.md`, seção 7). |
| **Deactivated** | Fora do ar | Ver o motivo e avisar a equipe. |

> Para mudar algo enquanto está em **Under review**, use **Withdraw from review**. O efeito volta para Draft e precisa ser reenviado.

---

## Parte 14: Problemas comuns e soluções

| Problema | Causa provável | Solução |
|---|---|---|
| Não acho o template "Randomizer 2D" | Busca ou categoria diferente | Busque `Random`; olhe em Interactive, Face e Game. Se não achar, use o Plano B (Parte 15). |
| Não existe **Import → Texture Sequence** | Menu mudou | Tente arrastar a **pasta `cartas`** inteira do Explorador de Arquivos para o painel Assets. Ou importe as 28 imagens e procure uma opção de criar sequência com o botão direito (a confirmar). Anote o caminho certo no relatório. |
| A sequência veio com menos de 28 quadros | Arquivos não selecionados | Apague a sequência e importe de novo com **Ctrl+A**. |
| As cartas fora de ordem | Seleção fora de ordem | Apague e importe de novo, selecionando com **Ctrl+A** (vai em ordem de nome). |
| Troquei a imagem mas continua a carta antiga do template | Trocou no componente **Image**, não no **Animation Sequence** | Faça a Parte 4.2 de novo, no componente **Animation Sequence**. |
| Balão esticado (círculo do emoji virou ovo) | Proporção diferente de 1:1 | No **2D Transform**, deixe largura igual à altura (ou Scale X igual a Y). |
| Título e carta em lugares diferentes | Transform diferente nos dois objetos | Copie o **2D Transform** de um e cole no outro (Parte 5, passos 11 a 15). |
| Clique no Preview não faz girar | **TapToSpin** desmarcado, ou clique fora da imagem | Marque **TapToSpin**. Clique **dentro** da imagem do Preview. |
| O título não some | Caixa do randomizador aponta para outro objeto | Na Parte 6, confira se o campo de título aponta para **Title**. |
| Sai sempre a mesma carta (ou só 2 ou 3) | Sorteio depende só do tempo | Parte 7.3: modo de reprodução **Shuffle** ou **Random**. |
| Com 2 rostos, as duas cartas saem sempre iguais | As duas animações param juntas | Parte 8.5: Shuffle/Random nas duas e **TimeToSpin** `2.8` na B. |
| 2º balão aparece com só 1 pessoa | Which Face errado | Parte 8.3: B só com **Face 1**, A só com **Face 0**. Se continuar, envie a versão de 1 rosto. |
| Balão treme ou descola do rosto | Rastreamento | Teste com mídia de vídeo e pouca luz. Não ponha o balão muito longe da cabeça: com Position Y exagerado, o tremor aumenta. Efeito que treme é reprovado. |
| Texto da carta borrado | Compressão baixa | Volte a compressão para **High** (Parte 3.3). |
| Pacote acima de 8 MB | Restos do template ou compressão | Parte 9: apagar o que sobrou e usar Medium só nas cartas. |
| **Test performance** falhou | Algo pesado no projeto | Clique em **View suggestions**. Este efeito não usa nada pesado (sem IA, sem segmentação), então o problema deve estar em algo que sobrou do template. Apague o que não é usado. |
| Pediu login de novo / conta errada | Login expirou | Chamar o Vini (seção 0.6), com o link. |
| Programa pede atualização | Versão velha | Baixe a mais nova em https://effecthouse.tiktok.com/download e instale por cima. |
| **Needs revision** por "propriedade intelectual" ou "marca" | O revisor achou parecido com app de mensagem | Responder/reenviar explicando nos comentários que o balão é genérico (sem verde, sem tiques, sem logo). Se insistir, peça à equipe da nuvem para mudar cores e formato do balão e gerar as imagens de novo. |
| **Needs revision** por causa de uma frase | Frase vetada | Peça à equipe da nuvem para trocar a frase no `textos.json` e rodar `gerar.py` de novo. **Às pressas:** renomeie uma reserva (`assets\reservas\reserva_01.png`) com o número da carta vetada (ex.: `opcao_15.png`), substitua na pasta `cartas` e importe a sequência de novo. |
| **Needs revision** por desempenho ou tremor | QA técnico | Rode o Test performance; teste com movimento; reduza o tamanho (Parte 9). |
| O formulário recusa o vídeo | Formato, duração ou tamanho | Parte 10.3 (ffmpeg); confira 9:16, ≤ 15 s e ≤ 32 MB. |

---

## Parte 15: Plano B (montar do zero, sem o template)

Use **só** se o template Randomizer 2D não existir ou não funcionar. Ele usa nós que estão na documentação oficial. Os nomes de alguns campos estão marcados como "a confirmar".

### 15.1 Objetos

1. Crie um projeto vazio: na tela inicial, clique em **New Project** ou **Blank** (a confirmar).
2. Na **Hierarchy**, clique em **+** (**Add**).
3. Clique em **Face Effects**.
4. Clique em **Face Sticker**. Ele cria um objeto que segue o rosto, com uma imagem dentro (a confirmar na sua versão do programa: o menu pode chamar "2D" ou "Face" em vez de "Face Effects"; se não houver objeto Face Sticker, crie uma **Image** 2D e adicione o componente **Face Sticker** pelo **Add Component**).
5. Renomeie para `Titulo`.
6. Na imagem filha, coloque a textura `titulo` (componente **Image → Texture**).
7. Repita os passos 2 a 4 para criar outro Face Sticker.
8. Renomeie para `Cartas`.
9. Na imagem filha de `Cartas`, clique em **Add Component**.
10. Escolha **Animation Sequence**.
11. No campo da sequência, escolha `cartas_grupo`.
12. Ajuste posição e tamanho como na Parte 5.

### 15.2 Lógica (Visual Scripting)

Para adicionar um nó: clique com o botão direito no painel **Visual Scripting** e digite o nome do nó. Para ligar: puxe da saída **Next** ou **Exec** de um nó até a entrada **Enter** do próximo.

**Ao abrir:**
1. Adicione o nó **Start**.
2. Ligue **Start → Set Visibility** com Target = `Titulo` e visível = **ligado**.
3. Ligue em seguida outro **Set Visibility**, com Target = imagem de `Cartas` e visível = **desligado**.

**Ao tocar:**
1. Adicione o nó **Screen Tap**.
2. Ligue **Screen Tap (Next) → Set Visibility** com `Titulo` = **desligado**.
3. Ligue em seguida **Set Visibility** com `Cartas` = **ligado**.
4. Ligue em seguida **Animation Sequence Controller**, entrada **Play**, com:
   - Animation Sequence = o componente de `Cartas`;
   - **From** = `0`, **To** = `27`;
   - **Loop** = ligado.
5. Ligue em seguida **Wait for Seconds** com `2.5`.
6. Ligue em seguida **Index Generator**, modo **Shuffle** (sem repetir) e intervalo de **0 a 27** (a confirmar na sua versão do programa: os nomes dos campos de intervalo).
7. Ligue em seguida outro **Animation Sequence Controller**, entrada **Play**, com:
   - **From** = saída do Index Generator;
   - **To** = **a mesma** saída do Index Generator;
   - **Loop** = desligado.
   A ideia é que, com From igual a To, a animação mostre **só aquele quadro** (a confirmar na sua versão do programa: teste no Preview; se não parar num quadro só, use a entrada **Pause** do mesmo nó logo depois do Play). A documentação oficial confirma que os índices começam em 0, então 0 = opcao_01 e 27 = opcao_28.

> **Cuidado:** se usar o nó **Random** em vez de Index Generator, ele **sorteia um número novo cada vez que é lido**. Ligado em From e em To, ele daria 2 números diferentes. Nesse caso, guarde o número antes numa variável (**Set Variable**) e leia a variável nos dois campos.

**Ao gravar:**
1. No painel **Visual Scripting**, ache a opção **Reset on Record**.
2. Escolha **On**. Assim, ao apertar o botão de gravar, o efeito volta para o título.

**Versão de 2 rostos no Plano B:**
1. Duplique `Titulo` e `Cartas` como `Titulo_B` e `Cartas_B`.
2. Em **Which Face**, deixe só **Face 1** nas cópias.
3. Duplique a cadeia "Ao tocar", apontando para os objetos `_B`. Cada cadeia tem o seu próprio Index Generator, então os resultados saem independentes.

### 15.3 Ajuda do assistente de IA do programa

Nas versões 5.13 em diante existe o assistente **Effect House AI**. Ele monta cenas e lógica a partir de um pedido escrito. A disponibilidade por conta ou região não foi confirmada. O pedido pronto, em inglês, está em:
`efeito-2-seu-papel-no-grupo\script\prompt-effect-house-ai.md`

Use o assistente para **destravar** um passo, não para mudar a ideia do efeito. Depois, confira tudo com os checklists das Partes 7 e 8.

---

## Parte 16: O que anotar no relatório

Em `Documentos\Efeitos\relatorio-montagem.md`, na seção do C08:

- Versão do Effect House instalada.
- Nomes reais dos objetos, componentes e campos que estavam diferentes deste guia (o "a confirmar" virou o quê).
- Valores originais do template (FPS, TitleDelay, posição e escala) e os que você colocou.
- Resultado do teste de sorteio (7.3) e do teste de independência (8.5).
- Versão enviada (1 ou 2 rostos) e por quê.
- Tamanho do pacote e resultado do Test performance.
- Lista de categorias e tipo de campo de hint que apareceram no formulário.
- Data e hora do envio, print da confirmação e status (Under review / Needs revision / Active).

---

## Fontes consultadas (documentação oficial do Effect House)

- Tutorial do template Randomizer 2D: <https://effecthouse.tiktok.com/learn/guides/tutorials/template-tutorials/randomizer-2d> (fonte para: Import → Texture Sequence, Title e RandomAnimationSequence, o componente Animation Sequence que sobrescreve o Image, TapToSpin, TimeToSpin, o reinício em Effect Start e Video Record Start, a duplicação para 2 pessoas com Which Face 0/1 e a cópia do 2D Transform pelos três pontinhos).
- Preparação de sequência de imagens (PNG/JPG, até 200 quadros, ≤ 1024 px, < 1 MB cada, mesmo tamanho): https://effecthouse.tiktok.com/learn/guides/technical-guides/assets/asset-preparation/2d-texture-sequence
- Modos de reprodução Random e Shuffle: https://effecthouse.tiktok.com/learn/guides/animation/animation-sequence/
- Nó Animation Sequence Controller (Play, Pause, From/To, Loop): https://effecthouse.tiktok.com/learn/3.8.0/guides/visual-scripting/nodes/utility/animation-sequence-controller
- Preview (mídias de exemplo, + Add media, webcam, clique simula toque, escolha de aparelho): https://effecthouse.tiktok.com/learn/guides/publishing/preview-in-effect-house
- Vídeo demo (9:16, MP4/MOV, ≤ 32 MB, ≤ 15 s; gravação pelo Preview): https://effecthouse.tiktok.com/learn/guides/publishing/demo-video-creation
- Preview no celular: https://effecthouse.tiktok.com/learn/guides/publishing/preview-in-tiktok
- Teste de desempenho: https://effecthouse.tiktok.com/learn/guides/publishing/publish/test-effect-performance
- Envio: https://effecthouse.tiktok.com/learn/guides/publishing/publish/submit-your-effect
- Ícone: https://effecthouse.tiktok.com/learn/guides/publishing/effect-icon-creation
- Status (Manage Effects): https://effecthouse.tiktok.com/learn/guides/management-and-growth/manage-your-effect
- Nós Face Detection, Screen Tap, Index Generator, Wait for Seconds: ver `tiktok-efeitos/pesquisa/03-tecnico-effect-house.md`, seção 3.
