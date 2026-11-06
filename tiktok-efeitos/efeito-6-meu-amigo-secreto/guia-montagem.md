# Guia de montagem: "Meu amigo secreto" (C06)

**Para quem é:** para o Montador, o Claude que opera o PC do Vini. Também serve para qualquer pessoa que já tenha montado o Torcedômetro (C01).
**Versão do guia:** 1.1 · 06/11/2026 (revisada pela QA) · escrito para o Effect House **5.16** no Windows, a versão que o Montador encontrou no PC.
**Envio:** entre **sexta, 20/11** e **terça, 24/11/2026**. O dia preferido é a **sexta, 20/11** (Parte 0.2). **Nunca antes de 20/11.** Montar e testar pode (e deve) ser feito assim que o C06 for liberado.
**Tempo total:** cerca de **2 h** para montar, reaproveitando o projeto do C01, e mais **30 min** no dia do envio. Se for preciso montar do zero (Parte 18), reserve 4 h.

> **Vini, se você estiver lendo:** não precisa fazer nada aqui. Você só será chamado nos casos da seção 0.8, sempre com o link direto.

### Como ler as marcas

- **(a confirmar na sua versão)**: a equipe não conseguiu ver essa tela, porque o site do Effect House não abre de onde pesquisamos. Se o botão ou o campo tiver outro nome, use o parecido e **anote no relatório** o nome real.
- Os nomes de botões e painéis estão **em inglês e em negrito**, como aparecem no programa.
- "Clique" é com o botão esquerdo. Quando for o direito, o passo diz "clique com o botão direito".
- **Você já montou o C08 e o C01** (e, até lá, provavelmente o C02). Quando este guia diz "faça como no C01", vale o que você fez de verdade e anotou no `relatorio-montagem.md`, mesmo que seja diferente do guia do C01.

### O que vamos montar (resumo)

1. Sobre a cabeça aparece uma **etiqueta de presente verde-pinheiro**, com borda dourada, a ponta da esquerda chanfrada e um **furinho dourado (ilhós)** nela. Um barbante dourado sai do furinho e vai até uma **caixa de presente fechada, com laço vermelho e um "?"**, que fica em cima da etiqueta. O texto é **"NO AMIGO SECRETO / EU VOU GANHAR…"**, e embaixo vem a pílula vermelha **"👆 TOQUE PRA ABRIR"**.
2. A pessoa toca na tela. O título some e as cartas giram por cerca de 2 segundos.
3. O giro para numa das **26 cartas**, por exemplo **"MEIA / (DE NOVO)"** ou **"UM ABRAÇO E UM / “DEPOIS TE DOU”"**. Nas cartas, a mesma caixa aparece **aberta**, com o presente saindo de dentro. Por isso, no giro, parece que a caixa abre e o conteúdo vai trocando. A carta fica presa na cabeça.
4. Quando a pessoa aperta **gravar** no TikTok, o efeito volta para o título.

**É o mesmo efeito do Torcedômetro, com outras imagens.** Usa o mesmo template (**Randomizer 2D**), o mesmo quadro de imagem (512×256) e as mesmas **26 cartas**, e a lógica é igual. A etiqueta do C06 fica **dentro** da área que o ingresso do C01 ocupa no quadro. Por isso o caminho principal deste guia é **copiar o projeto do C01 já pronto e trocar só o título, as cartas e o ícone**. A lógica, a posição e o tamanho continuam os do C01, que já foram testados e enviados. O efeito é para **1 pessoa** (1 rosto).

> O conceito fala em "o presente chacoalha e gira". Quem faz esse papel é o giro rápido das cartas, com a caixa aberta sempre no mesmo lugar. **Não acrescente animação, som nem tremida.** O efeito fica igual ao C01, que já passou pelo envio.

---

## Parte 0: Antes de começar

### 0.1 Pré-requisitos (confira todos)

| # | Pré-requisito | Como conferir |
|---|---|---|
| 1 | O C06 está liberado na tabela da seção 2 do `PRONTO-PARA-MONTAR.md` | Abra https://raw.githubusercontent.com/quantopagarei-sketch/quantocobrarpj/main/tiktok-efeitos/PRONTO-PARA-MONTAR.md. Se o C06 ainda estiver só em "Vem aí", **não comece**. |
| 2 | O projeto do C01 existe, abre e passou nos testes | No `relatorio-montagem.md`, seção do C01: nome do projeto, Caso A/B, plano usado (template ou script) e título usado |
| 3 | O Effect House está logado na conta **Car Shop** | Tela inicial, como no C01 |
| 4 | Você já sabe como o seu Effect House importa uma Texture Sequence (arquivos ou pasta) e como funciona o **Create icon** | Você fez isso no C08 e no C01. Anotações no relatório |
| 5 | O ffmpeg está instalado | `ffmpeg -version` no PowerShell. Se não estiver: `winget install --id Gyan.FFmpeg -e` e abra outro PowerShell. |

### 0.2 Quando enviar (leia antes de tudo)

Este efeito é de **Natal**. A equipe escolheu a janela de 20 a 24/11 por dois motivos:
- **não antes de 20/11:** a janela de 30 dias que conta os vídeos do efeito precisa ir até o Natal;
- **não depois de 24/11:** o efeito tem que estar **Active** até sábado, 28/11, porque o Vini grava o vídeo de lançamento do C06 no **domingo, 29/11**.

A revisão leva de 1 a 3 dias úteis. Enviando na sexta, 20/11, o resultado sai até quarta, 25/11, e ainda sobra tempo para corrigir uma reprovação antes do dia 29.

| Situação | O que fazer |
|---|---|
| Antes de 20/11 | **Montar, testar, gravar o demo e parar** (Parte 11). **Não clique em Submit**, nem para "ver como fica". |
| **Sexta, 20/11/2026** | **Enviar** (Partes 12 e 13). É o dia preferido. |
| Não deu para enviar em 20/11 (PC desligado, limite de uso, login caído) | Envie no **primeiro dia possível até terça, 24/11**, sem esperar ordem nova. |
| Passou de 24/11 e o C06 não foi enviado | Envie no **primeiro dia possível** e avise a nuvem. Não espere ordem. |
| Você só recebeu o C06 depois de 20/11 | Monte e envie no mesmo dia: pule a Parte 11 e a 12.3. |
| O `PRONTO-PARA-MONTAR.md` mandar outra data para o C06 | **Vale o arquivo**, não este guia. |

### 0.3 Links

| O quê | Link direto | Quem usa |
|---|---|---|
| Arquivos da equipe (zip com tudo) | https://github.com/quantopagarei-sketch/quantocobrarpj/archive/refs/heads/main.zip | Montador |
| Ordens da equipe (atualizadas todo dia) | https://raw.githubusercontent.com/quantopagarei-sketch/quantocobrarpj/main/tiktok-efeitos/PRONTO-PARA-MONTAR.md | Montador |
| Tutorial oficial do template (em inglês) | https://effecthouse.tiktok.com/learn/guides/tutorials/template-tutorials/randomizer-2d | Consulta |
| Guia oficial de envio (opções "new / update / replace") | https://effecthouse.tiktok.com/learn/guides/publishing/publish/submit-your-effect | Consulta |
| Guia oficial do ícone (Create icon) | https://effecthouse.tiktok.com/learn/guides/publishing/effect-icon-creation | Consulta |
| Status dos efeitos (Manage Effects) | https://effecthouse.tiktok.com/learn/guides/management-and-growth/manage-your-effect | Consulta |
| Preset de interação usado no Plano B2 | https://effecthouse.tiktok.com/learn/guides/visual-scripting/interactions/tap-screen-to-play-animation-sequence-then-delay-pause | Consulta |
| Guia do C01 (base deste) | `tiktok-efeitos\efeito-1-torcedometro\guia-montagem.md` | Consulta |
| Pedidos prontos para o Effect House AI | `tiktok-efeitos\efeito-6-meu-amigo-secreto\script\prompt-effect-house-ai.md` | Montador, se travar |

### 0.4 Pastas (vale para o guia inteiro)

Neste guia, **`<BASE>`** é a pasta "Efeitos" que você usa no PC. Pela última ordem da equipe, ela é `C:\Users\Pichau\Desktop\Efeitos`. Se essa pasta não existir, a pasta é `Documentos\Efeitos`.

| Apelido | Caminho |
|---|---|
| `<BASE>` | `C:\Users\Pichau\Desktop\Efeitos` (ou `Documentos\Efeitos`) |
| `<A>` (imagens do C06) | `<BASE>\tiktok-efeitos\efeito-6-meu-amigo-secreto\assets` |
| Projeto novo | `<BASE>\projetos\C06-meu-amigo-secreto` |
| Vídeo demo | `<BASE>\videos-demo\C06-demo.mp4` |
| Prints | `<BASE>\prints\C06-*.png` |
| Conferência dos arquivos (Partes 0.5 e 12.3) | `<BASE>\C06-conferencia-arquivos.csv` |
| Relatório | `<BASE>\relatorio-montagem.md`, nova seção "C06" |

### 0.5 Baixar e conferir os arquivos

1. Baixe o zip (link da 0.3) e extraia **só a pasta `tiktok-efeitos`** em `<BASE>`, por cima da antiga.
2. Rode no PowerShell:

```powershell
$BASE = if (Test-Path "C:\Users\Pichau\Desktop\Efeitos") { "C:\Users\Pichau\Desktop\Efeitos" } else { Join-Path ([Environment]::GetFolderPath('MyDocuments')) "Efeitos" }
$A = "$BASE\tiktok-efeitos\efeito-6-meu-amigo-secreto\assets"
(Get-ChildItem "$A\cartas\carta_*.png").Count            # tem que dar 26
(Get-ChildItem "$A\cartas\*").Count                      # tem que dar 26 (a pasta só pode ter as cartas)
(Get-ChildItem "$A\reservas\reserva_*.png").Count        # tem que dar 5
Get-ChildItem "$A\titulo_toque.png","$A\titulo.png","$A\icone_162.png","$A\icone_alt_162.png" | Select Name, Length
(Get-ChildItem "$A\cartas\*.png" | Measure-Object Length -Maximum).Maximum   # tem que ser menor que 1048576 (1 MB); o esperado é ~112000 (carta_18)
Get-ChildItem "$BASE\projetos" | Select Name, LastWriteTime                # ache aqui o projeto do C01
```

> **Em todo PowerShell novo**, rode antes as duas primeiras linhas acima (as que definem `$BASE` e `$A`). Os comandos das outras partes dependem delas.

3. Se faltar arquivo (por exemplo, se a pasta `assets` vier só com o `gerar.py`), a equipe ainda não publicou as imagens. Baixe o zip de novo mais tarde. Se continuar faltando, avise a nuvem. Não chame o Vini por isso.
4. **Guarde a "impressão digital" das imagens que você vai montar.** Entre a montagem e o envio podem passar dias, e a equipe pode retocar alguma carta nesse tempo. No dia do envio (Parte 12.3), este arquivo mostra se algo mudou:

```powershell
Get-ChildItem "$A\titulo_toque.png","$A\titulo.png","$A\cartas\*.png","$A\quadrado_512\titulo_toque.png","$A\quadrado_512\titulo.png","$A\quadrado_512\cartas\*.png" | Get-FileHash -Algorithm SHA256 | Select-Object @{n='Arquivo';e={$_.Path.Substring($A.Length + 1)}}, Hash | Export-Csv "$BASE\C06-conferencia-arquivos.csv" -NoTypeInformation -Encoding UTF8
(Import-Csv "$BASE\C06-conferencia-arquivos.csv").Count   # tem que dar 56 (2 títulos + 26 cartas, nas duas versões)
```

### 0.6 O que entra no efeito e o que não entra

Todos os arquivos ficam dentro de `<A>` (a pasta `assets` do efeito 6).

| Arquivo | Entra? | Para quê |
|---|---|---|
| `titulo_toque.png` (512×256, fundo transparente) | **Sim (padrão)** | Título "NO AMIGO SECRETO / EU VOU GANHAR…", com a caixa fechada e a pílula vermelha "👆 TOQUE PRA ABRIR". Vai no objeto **Title**. |
| `titulo.png` (512×256) | Só se o C01 usou o título sem etiqueta | O mesmo título, sem a pílula (Parte 3.2, passo 3). |
| `cartas\carta_01.png` … `carta_26.png` (512×256 cada) | **Sim** | Os 26 resultados. Entram juntos como **uma** Texture Sequence, na ordem 01→26. |
| `reservas\reserva_01.png` … `reserva_05.png` | Não | Só se uma carta for vetada (Parte 17) |
| `quadrado_512\` (as mesmas imagens em 512×512) | Só se o C01 usou as quadradas | Título e cartas têm que seguir o C01: as duas 512×256 ou as duas quadradas |
| `icone_162.png`, `icone_alt_162.png` | Só no plano de exceção da Parte 13.3 | Pela ordem de 06/11, o ícone sai do **Create icon** |
| `icone_512.png`, `icone_alt_512.png`, `previa.png`, `gerar.py`, `lista-de-arquivos.txt`, `LEIA-ME.md` | Não | Referência da equipe |

**Peso:** `titulo_toque.png` + 26 cartas = **2,59 MB** em PNG (no C01, as mesmas peças tinham 2,15 MB e viraram um pacote de 1,6 MB). O maior arquivo é a `carta_18.png`, com 110 KB. Nenhuma imagem passa de 1 MB nem de 1024 px.

**Régua contra imagem esticada:** o **ilhós**, o furinho dourado na ponta esquerda da etiqueta, tem que ficar **redondo** no título e em todas as cartas. Se virar ovo, a imagem está esticada. O miolo do furinho é **transparente de verdade**: o fundo do vídeo aparece por ele, e isso é de propósito.

**O conjunto não é simétrico, e isso é de propósito.** A ponta com o ilhós fica à esquerda, e a caixa e o texto ficam centrados no retângulo da etiqueta, uns 18 px à direita do centro da imagem. **Centralize a imagem** na cabeça, como no C01. Não empurre nada para compensar.

**Como reconhecer as cartas do C06 no giro:** etiqueta de presente com a ponta esquerda chanfrada e o ilhós, barbante dourado e, em cima, uma **caixa verde aberta com fita vermelha** de onde sai o desenho. O fundo da etiqueta alterna em **4 cores**, sem repetir a vizinha: verde-pinheiro, dourado, kraft (marrom de papel) e creme. O ingresso do C01 é **laranja, violeta, ouro ou magenta, com recortes redondos nas laterais e uma medalha redonda em cima**. Se ele aparecer, a troca não pegou.

### 0.7 Ordem das cartas (quadro = posição na sequência)

O quadro 0 é a carta 01. Use a tabela para conferir a ordem (Parte 3.3) e para anotar o teste de sorteio (Parte 8.3). A coluna "px" é o tamanho da letra: quanto menor, mais importante conferir a leitura.

| Quadro | Arquivo | Texto | px | Quadro | Arquivo | Texto | px |
|---:|---|---|---:|---:|---|---|---:|
| 0 | carta_01 | MEIA / (DE NOVO) | 54 | 13 | carta_14 | SANDUICHEIRA / (EU JÁ TENHO 2) | 48 |
| 1 | carta_02 | TRANSFERÊNCIA / DE 10 REAIS | 46 | 14 | carta_15 | DESODORANTE / (É INDIRETA?) | 52 |
| 2 | carta_03 | CANECA COM / FRASE DE COACH | 45 | 15 | carta_16 | O QUE EU DEI / NO ANO PASSADO | 43 |
| 3 | carta_04 | CHEIRINHO / PRO CARRO | 54 | 16 | carta_17 | CARREGADOR QUE / NÃO CARREGA | 42 |
| 4 | carta_05 | PANETONE QUE / NINGUÉM COME | 49 | 17 | carta_18 | PANO DE PRATO / COM CROCHÊ | 49 |
| 5 | carta_06 | FONE QUE SÓ / PEGA DE UM LADO | 42 | 18 | carta_19 | NADA (QUEM ME / TIROU FALTOU) | 47 |
| 6 | carta_07 | UM ABRAÇO E UM / “DEPOIS TE DOU” | 44 | 19 | carta_20 | PLANTINHA QUE / NÃO VAI DURAR | 48 |
| 7 | carta_08 | KIT SABONETE / (O 3º DO ANO) | 53 | 20 | carta_21 | CAPA DE / VOLANTE PELUDA | 44 |
| 8 | carta_09 | PANTUFA NUM / CALOR DE 40° | 54 | 21 | carta_22 | AGENDA QUE USO / ATÉ JANEIRO | 44 |
| 9 | carta_10 | O QUE EU PEDI / (MILAGRE) | 54 | 22 | carta_23 | UM PRESENTÃO / (FOI ENGANO) | 50 |
| 10 | carta_11 | PORTA-CELULAR / DE PAINEL | 47 | 23 | carta_24 | CHINELO DOIS / NÚMEROS MENOR | 44 |
| 11 | carta_12 | TOALHA COM MEU / NOME ERRADO | 42 | 24 | carta_25 | SQUEEZE QUE / VAZA NA MOCHILA | 41 |
| 12 | carta_13 | CHOCOLATE / DERRETIDO | 54 | 25 | carta_26 | PRESENTE SEM / NOTA PRA TROCAR | 41 |

### 0.8 O que depende do Vini (o mínimo)

Nada, se tudo correr bem. Ele só é chamado se:

1. **O login do Effect House cair** ou se o programa estiver em outra conta. Mande para ele:
   > Abra o Effect House no computador. Vai aparecer um QR code. No celular, abra o **TikTok da conta Car Shop** → **Perfil** → ícone de pessoa (**Adicionar amigos**) → ícone de scanner no canto de cima → aponte para o QR → toque em **Confirmar**. Guia com imagens: https://effecthouse.tiktok.com/learn/guides/getting-started/introduction-to-effect-house/download-and-login
   >
   > Tem que ser o scanner **de dentro do TikTok**. A câmera comum do celular não funciona.
2. **O formulário de envio abrir no navegador e pedir login no TikTok** (não está confirmado se isso acontece). Mande: "Abra https://www.tiktok.com/login/qrcode no computador e escaneie o QR com o scanner do TikTok da conta Car Shop, como no login do Effect House."
3. **A decisão sobre o desafio** ("Nov Social Randomizer Sub Challenge" ou outro) ainda não tiver saído no dia do envio. Quem pergunta é a nuvem, não você (Parte 13.2).

O teste no celular é **opcional** e fica de fora deste guia. Se a equipe quiser fazê-lo, junta com outros efeitos num momento só, como na Parte 10 do guia do C01.

### 0.9 Tempo estimado

| Etapa | Quando | Tempo |
|---|---|---|
| Parte 0: baixar e conferir | na montagem | 10 min |
| Parte 1: copiar o projeto do C01 | na montagem | 10 min |
| Parte 2: reconhecer o que veio do C01 | na montagem | 10 min |
| Partes 3 a 5: importar, trocar e limpar | na montagem | 20 min |
| Partes 6 e 7: posição e lógica (só conferir) | na montagem | 10 min |
| Parte 8: testar no PC | na montagem | 25 min |
| Partes 9 a 11: tamanho, desempenho, vídeo demo e pausa | na montagem | 25 min |
| Partes 12 e 13: conferências do dia, ícone e envio | **sex 20/11** (até ter 24/11) | 30 min |
| **Total** | | **≈ 2 h 20 min** |

---

## Parte 1: Copiar o projeto do C01 (sem estragar o original)

O projeto do C01 continua importante: se o Torcedômetro voltar com **Needs revision**, é nele que você corrige. Por isso a primeira coisa é guardar uma cópia, e depois **nunca mais salvar nada por cima dele** neste guia.

### 1.1 Backup do C01

1. Ache o nome real do projeto do C01 em `<BASE>\projetos\` (o guia do C01 sugeria `C01-torcedometro`; confira no relatório).
2. Feche o Effect House, se o projeto do C01 estiver aberto.
3. Rode no PowerShell, trocando `C01-torcedometro` pelo nome real, se for outro:

```powershell
$P = "$BASE\projetos"
New-Item -ItemType Directory -Force "$P\backup" | Out-Null
Copy-Item -Recurse -Force "$P\C01-torcedometro*" "$P\backup\"
Get-ChildItem "$P\backup" | Select Name, LastWriteTime
```

O `*` no fim do nome leva junto o arquivo de projeto, se ele for um arquivo solto com extensão, ou a pasta inteira, se o projeto for uma pasta. O formato real está no `reconhecimento.md`, item 6.

### 1.2 Abrir o C01 e salvar como C06

1. Abra o **Effect House**.
2. Confira a conta **Car Shop**, como no C01. Se for outra conta, **pare** e siga a seção 0.8.
3. Abra o projeto do C01 (lista de projetos recentes da tela inicial, ou **File → Open**; a confirmar na sua versão).
4. **Antes de mexer em qualquer coisa**, clique em **File → Save As**.
5. Vá até `<BASE>\projetos\`.
6. Dê o nome **`C06-meu-amigo-secreto`**.
7. Clique em **Salvar**.
8. Confira na **barra de título** da janela se aparece `C06-meu-amigo-secreto`. **Só siga em frente se o nome do C06 estiver lá.**

> **Regra deste guia:** antes de cada **Ctrl+S**, olhe a barra de título. Tem que estar escrito `C06-meu-amigo-secreto`.

**Se não houver "Save As"** (a confirmar na sua versão):
1. Feche o Effect House.
2. No PowerShell: `Copy-Item -Recurse "$BASE\projetos\C01-torcedometro" "$BASE\projetos\C06-meu-amigo-secreto"`. Se o projeto for um arquivo com extensão, copie o arquivo e dê ao novo o nome `C06-meu-amigo-secreto` com a mesma extensão.
3. Abra a cópia no Effect House e confira a barra de título.

**Se o projeto do C01 não existir ou não abrir:**
1. Use o projeto do C02 (`C02-meu-proximo-carro`), que é a mesma montagem com outras imagens. Faça o backup dele (1.1, com o nome do C02) e a Parte 1.2 a partir dele. Nas Partes 2 a 5, onde o guia diz "o que veio do C01", leia "o que veio do C02": o título esperado é `carro_titulo` e a sequência, `cartas_carro`. No giro, a carta antiga a evitar passa a ser a **etiqueta com faixa de asfalto embaixo e um carro em cima**. Anote no relatório.
2. Se nem o C02 servir, monte do zero pela Parte 18 (Plano B1).

---

## Parte 2: Reconhecer o que veio do C01

Não mude nada nesta parte. Só anote no relatório, na seção do C06.

1. Anote a versão do Effect House (**Help → About** ou tela inicial; a confirmar na sua versão). O esperado é 5.16.
2. Na **Hierarchy**, clique em **Title**.
3. No **Inspector**, no componente **Image**, leia o nome que está no campo **Texture**. O esperado é `titulo_toque` (ou `titulo`, se no C01 você precisou trocar). **Anote o nome.**
4. Clique em **RandomAnimationSequence**.
5. Veja onde está a sequência das cartas e anote o caso:
   - **Caso A:** existe o componente **Animation Sequence**, e a sequência está no campo dele;
   - **Caso B:** a sequência está direto no campo **Texture** do componente **Image**.
6. Anote o nome da sequência. O esperado é `cartas_torcedor`.
7. Anote, nos dois objetos, os valores de **Position**, **Scale**, **Size** e **Stretch Mode**. Eles vão ficar iguais.
8. Na **Hierarchy**, veja se existe um objeto chamado `Controle` com o script **TorcedometroController**. Se existir, foi usado o Plano C no C01: este é o **Caso S**. Se não existir, a lógica é a do template: **Caso T**.
9. **Caso T:** abra o **Visual Scripting**, clique na caixa do randomizador e anote **TapToSpin**, **TimeToSpin**, **TitleDelay** e **TitleFadeOutTime**. O esperado é: ligado, `2`, o valor do template e `0.3`.
10. Veja no relatório do C01 se ele usou as imagens **512×256** ou as **quadradas** (`quadrado_512`). O C06 tem que usar a mesma versão.

---

## Parte 3: Marcar as imagens antigas e importar as novas

As imagens do C06 têm **os mesmos nomes de arquivo** das do C01 (`titulo_toque.png`, `carta_01.png`…). Para não confundir na hora de trocar, primeiro você muda o nome das antigas no projeto.

### 3.1 Marcar as antigas

No painel **Assets**:

1. Clique com o botão direito no título que você anotou na Parte 2, passo 3 (ex.: `titulo_toque`) → **Rename** → digite `ANTIGO_titulo_toque`.
2. Se existir também `titulo`, faça o mesmo: `ANTIGO_titulo`.
3. Clique com o botão direito na sequência anotada no passo 6 (ex.: `cartas_torcedor`) → **Rename** → digite `ANTIGO_cartas`.

> Mudar o nome no painel Assets **não** muda o efeito: o objeto continua usando a mesma imagem. Os arquivos do C01 em `tiktok-efeitos\efeito-1-torcedometro\` também continuam intactos.

### 3.2 Importar o título

1. No painel **Assets**, clique em **+** (**Add**) → **Import** → **From Computer** (o mesmo caminho usado no C01).
2. Vá até `<A>` (`<BASE>\tiktok-efeitos\efeito-6-meu-amigo-secreto\assets\`).
3. Selecione o título, conforme o que o C01 usou:
   - C01 com `titulo_toque` → selecione **`titulo_toque.png`**;
   - C01 com `titulo` (sem etiqueta) → selecione **`titulo.png`**;
   - C01 com as quadradas → use os mesmos nomes, mas dentro de `<A>\quadrado_512\`.
4. Clique em **Abrir**.
5. Renomeie o asset novo para **`amigo_titulo`**.

### 3.3 Importar as 26 cartas (Texture Sequence)

1. No painel **Assets**, clique em **+** (**Add**) → **Import** → **Texture Sequence**.
2. Abra a pasta **`<A>\cartas\`** (ou `<A>\quadrado_512\cartas\`, se o C01 usou as quadradas).
3. Faça como no C01: se a janela pedir arquivos, **Ctrl+A** e **Abrir**; se pedir pasta, selecione a pasta `cartas` e confirme.
4. Confira se apareceu **uma** sequência nova e se ela tem **26 frames** no **Inspector**.
5. Renomeie a sequência nova para **`cartas_amigo`**.
6. Confira a ordem:
   - o **primeiro** quadro tem que ser **MEIA / (DE NOVO)**, com etiqueta **verde-pinheiro** e meias bege saindo da caixa;
   - o **último** tem que ser **PRESENTE SEM / NOTA PRA TROCAR**, com etiqueta **dourada**, um recibo saindo da caixa e um círculo vermelho cortado ao lado.
   Se estiver fora de ordem, apague `cartas_amigo` e importe de novo com **Ctrl+A**. A equipe não conseguiu confirmar se o programa ordena pelo nome do arquivo (a confirmar na sua versão); no C01 você já viu como ele se comporta.

### 3.4 Compressão

1. Clique em `ANTIGO_cartas` e veja a compressão no **Inspector**.
2. Ponha **a mesma** em `cartas_amigo`. Se o C01 ficou em **Automatic** ou **Manual → 512 → High**, mantenha assim.
3. Faça o mesmo com `amigo_titulo`, sempre em **High** (ou Automatic).

---

## Parte 4: Trocar as imagens

### 4.1 Título

1. Na **Hierarchy**, clique em **Title**.
2. No **Inspector**, componente **Image** → campo **Texture** → escolha **`amigo_titulo`**. Também dá para arrastar do painel Assets para o campo.
3. Confira no **Preview** se aparece a etiqueta verde com "NO AMIGO SECRETO / EU VOU GANHAR…" e, em cima, a caixa fechada com laço vermelho.

### 4.2 Cartas

1. Na **Hierarchy**, clique em **RandomAnimationSequence**.
2. Siga o caso que você anotou na Parte 2:
   - **Caso A:** componente **Animation Sequence** → campo da sequência → **`cartas_amigo`**. Não mexa no **Texture** do **Image**, porque o Animation Sequence troca essa textura sozinho.
   - **Caso B:** componente **Image** → campo **Texture** → **`cartas_amigo`**.
3. **Não mexa** no FPS nem no modo de reprodução (**Forward / Random / Shuffle**). Deixe como estavam no C01.
4. **Só no Caso S:** clique em `Controle` → componente **TorcedometroController** → campo **Sequencia Cartas** → **`cartas_amigo`**. Os outros campos ficam como estão (Titulo = Title, Cartas = RandomAnimationSequence, Tempo Giro = 2, Tempo Some Titulo = 0.3, Girar De Novo No Toque = marcado). O nome do script continua "Torcedometro". Isso não aparece para ninguém e não precisa mudar.
5. **Só no Caso T:** abra o **Visual Scripting** e clique na caixa do randomizador. Se algum campo dela mostrar `ANTIGO_cartas` ou `ANTIGO_titulo_toque`, troque por `cartas_amigo` ou `amigo_titulo` (a confirmar na sua versão: o template pode não ter campo de imagem na caixa).
6. Aperte **Ctrl+S**, depois de conferir a barra de título.

---

## Parte 5: Apagar as imagens antigas

1. No painel **Assets**, clique com o botão direito em `ANTIGO_cartas` → **Delete**.
2. Faça o mesmo com `ANTIGO_titulo_toque` e, se existir, `ANTIGO_titulo`.
3. **Se o programa avisar que o asset ainda está em uso, clique em Cancelar.** Algum lugar ainda aponta para a imagem antiga. Procure nesta ordem:
   1. **Title → Image → Texture**;
   2. **RandomAnimationSequence**: Animation Sequence e Image;
   3. `Controle` → **Sequencia Cartas** (Caso S);
   4. a caixa do randomizador no **Visual Scripting** (Caso T).
   Troque e tente apagar de novo.
4. Apague **só** o que começa com `ANTIGO_`. Se aparecer outra imagem que você não reconhece, deixe como está e anote no relatório.
5. Aperte **Ctrl+S**.

> Se você quiser usar o `titulo.png` como reserva durante os testes, importe-o agora, renomeie para `amigo_titulo_sem_toque` e apague antes da pausa (Parte 9). Só importe se for usar.

---

## Parte 6: Proporção, posição e tamanho (só conferir)

O quadro do C06 é o mesmo do C01: **512×256**. A equipe mediu a área com desenho, contando até a sombra mais fraca: nas 26 cartas, vai de **5 a 506 px na largura e de 3 a 248 px na altura**; no título, de 5 a 506 e de 8 a 248. Tudo isso fica **dentro** da área do ingresso do C01. Por isso, **a posição e o tamanho do C01 servem sem mudança.**

1. Escolha no **Preview** o primeiro dos 3 rostos de exemplo.
2. Confira o título:
   - o **ilhós** (furinho dourado da ponta esquerda) está **redondo** (se virou ovo, veja a Parte 16, linha "esticado");
   - a etiqueta está **inteira na tela**: a ponta esquerda com o barbante, a caixa de cima com o laço e as estrelinhas;
   - a pílula **"👆 TOQUE PRA ABRIR"** aparece inteira, e a borda de baixo da etiqueta fica **logo acima do cabelo**, sem cobrir a testa nem os olhos.
3. Clique no Preview para sortear e espere a carta parar.
4. Confira a carta da mesma forma: **ilhós redondo**, etiqueta inteira (com a caixa aberta e o desenho de cima), borda de baixo acima do cabelo.
5. Repita nos outros 2 rostos de exemplo.

> A caixa e o texto ficam um pouco à direita do centro da imagem (Parte 0.6). **Isso é normal.** Não mexa no **Position X** para compensar.

**Só se algo não couber:** ajuste como na Parte 5.2 do guia do C01:
- mude **Scale** com **X e Y iguais** e **Position Y** no **RandomAnimationSequence**;
- copie o **2D Transform** (três pontinhos ⋮ → **Copy**) e cole no **Title** (⋮ → **Paste**);
- a largura da etiqueta fica em cerca de **1,6 vez a largura da cabeça** (entre 1,4 e 1,8).

Anote no relatório se mudou algo e os valores novos.

---

## Parte 7: A lógica (só conferir)

O C06 tem **26 cartas, igual ao C01**. Então a lógica não muda: nenhum campo de quantidade de quadros precisa ser alterado.

**Caso T (template):** no **Visual Scripting**, caixa do randomizador:

| Campo | Valor no C06 | Se estiver diferente |
|---|---|---|
| **TapToSpin** | **Ligado** | Ligue |
| **TimeToSpin** | **2** | Ponha `2` |
| **TitleFadeOutTime** | **0.3** | Ponha `0.3` |
| **TitleDelay** | o mesmo do C01 | Deixe como estava no C01 (se no C01 você precisou pôr `60`, mantenha) |
| Quantidade ou intervalo de quadros, se existir | **26** ou **0 a 25** | Ponha 26 ou 0–25 |
| Campos de objeto | **Title** e **RandomAnimationSequence** | Aponte para esses dois |

**Caso S (script):** confira os campos da Parte 4.2, passo 4.

Não crie nem apague nós. Se a lógica falhar nos testes, vá para a Parte 18.

Aperte **Ctrl+S**.

---

## Parte 8: Testar no PC

### 8.1 Como testar

Faça como no C01: escolha um rosto de exemplo **em vídeo**, se houver, e clique **dentro** da imagem do Preview para simular o toque.

### 8.2 Checklist (marque tudo antes de seguir)

- [ ] Ao abrir, aparece **só o título** (etiqueta verde e caixa **fechada** com laço vermelho e "?"), sem nenhuma carta por trás.
- [ ] O título **fica na tela até o clique**.
- [ ] A pílula vermelha **"👆 TOQUE PRA ABRIR"** aparece inteira, sem corte.
- [ ] O **ilhós** está redondo no título e nas cartas (nada esticado).
- [ ] A etiqueta está **inteira na tela**, com a ponta esquerda, o barbante, a caixa de cima e as estrelinhas, nos 3 rostos de exemplo.
- [ ] A borda de baixo da etiqueta fica **acima do cabelo**, sem cobrir os olhos.
- [ ] O título **acompanha a cabeça** quando o rosto se mexe.
- [ ] Ao clicar, o título **some** e as cartas **giram**. No giro, a caixa aparece **aberta** e o fundo alterna entre verde-pinheiro, dourado, kraft e creme.
- [ ] O giro dura **cerca de 2 s** e **para** numa carta.
- [ ] Nenhuma carta do **Torcedômetro** aparece no giro. Se aparecer um ingresso **laranja, violeta, ouro ou magenta, com recortes redondos nas laterais**, a troca da Parte 4.2 não pegou em algum lugar. (Se a base foi o C02: nenhuma etiqueta com faixa de asfalto.)
- [ ] Dá para **ler** a carta parada, inclusive as de letra menor: 25 (SQUEEZE QUE / VAZA NA MOCHILA), 26 (PRESENTE SEM / NOTA PRA TROCAR), 06 (FONE QUE SÓ / PEGA DE UM LADO), 12 (TOALHA COM MEU / NOME ERRADO) e 17 (CARREGADOR QUE / NÃO CARREGA). Para conferir sem esperar o sorteio, abra a imagem em `<A>\cartas\` no visualizador do Windows ao lado do Preview e compare o tamanho do texto.
- [ ] As palavras **não grudam** (ex.: "PEGA DE UM LADO", na carta 06, com espaço visível entre as palavras).
- [ ] Nas cartas **creme** (04, 08, 12, 16, 20, 24), o texto verde-escuro dá para ler; nas **douradas** (02, 06, 10, 14, 18, 22, 26), o texto claro com contorno marrom também.
- [ ] A carta continua **parada e presa na cabeça** quando o rosto se mexe.
- [ ] Não aparece **borda escura** nem quadrado em volta da etiqueta. O único "buraco" esperado é o miolo do ilhós, por onde aparece o fundo.
- [ ] Quando o rosto **sai** da imagem, a etiqueta **some**.
- [ ] Clicar **de novo** depois do resultado faz o mesmo que no C01 (gira de novo ou nada). Anote.

### 8.3 Teste do sorteio

1. Faça **15 sorteios**, voltando ao título ou clicando de novo, como no C01.
2. Anote o texto de cada carta que saiu (use a tabela da 0.7).
3. Avalie:
   - **OK:** saíram **pelo menos 9 cartas diferentes** e **nenhuma saiu mais de 4 vezes**.
   - **Problema:** sempre as mesmas 2 ou 3, sempre a mesma, ou uma ordem fixa. Troque o modo da sequência para **Shuffle** (ou **Random**), como na Parte 7.3 do guia do C01, e repita. Se continuar, use o Plano C (Parte 18).

> Se o C01 passou neste teste, o C06 deve passar também: a lógica e a quantidade de cartas são as mesmas.

### 8.4 Salvar

Confira a barra de título e aperte **Ctrl+S**.

---

## Parte 9: Tamanho e desempenho

1. Se você importou `amigo_titulo_sem_toque` e não usou, apague do painel **Assets**.
2. Na barra de cima, clique em **Click to update** no indicador de tamanho.
3. Anote o tamanho. O C01 deu **1,6 MB**. As imagens do C06 pesam um pouco mais (2,59 MB contra 2,15 MB em PNG), então o esperado é **perto de 2 MB** (estimativa da equipe, a confirmar na sua versão).
   - **Até 5 MB:** siga.
   - **Entre 5 e 8 MB:** sobrou alguma coisa do C01 ou do C08. Volte à Parte 5.
   - **Acima de 8 MB:** não dá para enviar. Apague o que sobrou e, se ainda passar, mude a compressão de `cartas_amigo` para **Manual → 512 → Medium** e confira se o texto continua nítido, principalmente nas cartas 25 e 26.
4. Clique em **Test performance** → **Run test** e espere cerca de 30 s.
   - **Passou:** siga.
   - **Falhou:** clique em **View suggestions**, apague o que sobrou e teste de novo.
   - **Não rodou** (como aconteceu no C01): anote a mensagem e siga. O efeito é só 1 imagem e 1 sequência, sem IA e sem segmentação.

---

## Parte 10: Vídeo demo

O formulário 5.16 trata o demo como opcional, mas **mande sempre**. Só a revisão vê o vídeo. Regras: **9:16, MP4 ou MOV, até 15 s, até 32 MB**. Grave agora, na montagem, para o dia do envio ficar só com o envio.

1. Grave como no C01 (Parte 9 do guia dele): aparelho 9:16 no Preview, rosto de exemplo em vídeo e **Screen record** (ou **Win+Shift+R**). Use só os rostos de exemplo do programa: nada de webcam com enfeite de Natal, gorro de Papai Noel, mesa de ceia, garrafa ou taça ao fundo.
2. Siga o roteiro:

| Tempo | O que acontece |
|---|---|
| 0–2 s | Título parado sobre a cabeça, com a caixa fechada e "TOQUE PRA ABRIR" |
| ≈ 2 s | Clique no Preview |
| 2–4,5 s | Título some e as cartas giram |
| 4,5–8 s | Resultado parado, com o rosto se mexendo um pouco |
| ≈ 8 s | Clique de novo, se o template girar de novo (se não girar, deixe o resultado até o fim) |
| 8–13 s | Segundo giro e segundo resultado |

3. **Se algum resultado do vídeo for a carta 02 (TRANSFERÊNCIA DE 10 REAIS), 03 (CANECA COM FRASE DE COACH), 10 (O QUE EU PEDI (MILAGRE)) ou 15 (DESODORANTE (É INDIRETA?)), grave de novo.** São as cartas que a equipe marcou como as mais sensíveis para a revisão, e não vale a pena chamar atenção para elas no vídeo. Qualquer outra carta serve. O melhor resultado para o vídeo é o 01 (MEIA (DE NOVO)), mas não insista nele.
4. Salve em `<BASE>\videos-demo\C06-demo-bruto.mp4`.
5. Confira em **Propriedades → Detalhes**: em pé, 9:16 (ex.: 1080×1920) e até 15 s.
6. Se não estiver em 9:16, rode:

```powershell
cd "$BASE\videos-demo"
ffmpeg -i C06-demo-bruto.mp4 -t 15 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" -c:v libx264 -pix_fmt yuv420p -an C06-demo.mp4
```

7. Se o bruto já estava em 9:16 e até 15 s, só renomeie para `C06-demo.mp4`.
8. Abra o `C06-demo.mp4` e confira se a etiqueta continua inteira (com a ponta esquerda e a caixa de cima) e se a carta final dá para ler.

---

## Parte 11: Pausa até 20/11

Aqui termina a montagem. **Não clique em Submit.** (Se hoje já é 20/11 ou depois, pule esta parte e vá direto para a Parte 12.)

1. Confira a barra de título e aperte **Ctrl+S**.
2. Rode: `Copy-Item -Recurse -Force "$BASE\projetos\C06-meu-amigo-secreto*" "$BASE\projetos\backup\"`
3. Escreva no `relatorio-montagem.md`, seção do C06: **"C06 montado e testado, aguardando 20/11"**, com os itens da Parte 19 que já tiver.
4. Mande para a nuvem (`session_01XsQ8UziuLNch4tqqVVQfCw`) um resumo de 3 linhas: montado, resultado do teste de sorteio, tamanho do pacote.
5. Até 20/11, **não abra o projeto do C06 para mexer**, a não ser que o `PRONTO-PARA-MONTAR.md` mande. Se precisar corrigir o C01 ou outro sorteio nesse meio-tempo, faça no projeto **dele**.

---

## Parte 12: No dia do envio: conferências antes de enviar

Faça na ordem. Leva uns 15 minutos.

### 12.1 Ordens novas

1. Abra o `PRONTO-PARA-MONTAR.md` mais novo (link da 0.3) e leia a seção **Atualizações**.
2. **Se ela disser algo sobre o C06 (data, desafio, carta trocada), vale ela, e não este guia.**

### 12.2 Status dos outros sorteios

1. Abra **Manage Effects**.
2. Veja o status de **Torcedômetro**, **Eu no grupo da família** e **Meu próximo carro** (os outros sorteios da conta, todos do mesmo template). Veja também **Perrengue no volante**.
3. Decida:
   - **Active** ou **Under review:** siga.
   - **Needs revision por "duplicado", "parecido com outro efeito" ou "spam"** em qualquer um deles: **não envie o C06.** Mande o print do motivo para a nuvem e espere ordem. O C06 sai do mesmo template, e mandar mais um agora pode piorar.
   - **Needs revision por motivo técnico** (desempenho, tremor, tamanho): aplique a mesma correção no C06 antes de enviar, refaça o checklist da Parte 8.2 e avise a nuvem.
   - **Needs revision por conteúdo** (uma carta, um texto, uma marca): não afeta o C06, que tem outras imagens. Siga.

### 12.3 As imagens da equipe mudaram desde a montagem?

1. Baixe o zip de novo e extraia **só a pasta `tiktok-efeitos`** em `<BASE>`, por cima da antiga.
2. Rode no PowerShell (depois das duas linhas da 0.5 que definem `$BASE` e `$A`):

```powershell
$antes = Import-Csv "$BASE\C06-conferencia-arquivos.csv"
$agora = Get-ChildItem "$A\titulo_toque.png","$A\titulo.png","$A\cartas\*.png","$A\quadrado_512\titulo_toque.png","$A\quadrado_512\titulo.png","$A\quadrado_512\cartas\*.png" | Get-FileHash -Algorithm SHA256 | Select-Object @{n='Arquivo';e={$_.Path.Substring($A.Length + 1)}}, Hash
Compare-Object $antes $agora -Property Arquivo, Hash
```

3. Leia o resultado:
   - **Não apareceu nada:** as imagens são as mesmas que você montou. Siga para a 12.4.
   - **Apareceram linhas:** a equipe mudou essas imagens. Olhe só as linhas da versão que você usa (512×256, sem `quadrado_512\`, ou só as `quadrado_512\`):
     - **mudou alguma `cartas\carta_XX.png`:** troque a sequência inteira, como na Parte 17, passos 1 a 4 do bloco "No Effect House" (sem o reenvio), e refaça o checklist da Parte 8.2;
     - **mudou o título que você usa:** importe o novo (Parte 3.2), ponha no **Title** (Parte 4.1), apague o `amigo_titulo` antigo, renomeie o novo para `amigo_titulo`, refaça a Parte 8.2 e **grave o demo de novo** (Parte 10).
   - Em qualquer caso, a versão certa é a da pasta da equipe: refaça o que está acima e conte para a nuvem quais arquivos mudaram.

### 12.4 Nome

1. Em **Manage Effects**, confira se nenhum efeito da conta já se chama **Meu amigo secreto**. Os nomes esperados lá são: Eu no grupo da família, Torcedômetro, Meu próximo carro e Perrengue no volante.
2. **Opcional, 3 min (a confirmar se funciona sem login):** no navegador do PC, abra https://www.google.com/search?q=site%3Atiktok.com%2Fsticker+%22Meu+amigo+secreto%22. Se aparecer um efeito **famoso** com exatamente esse nome, use o 1º nome alternativo da Parte 13.4 e anote. Se a busca não abrir ou não achar nada, siga com **Meu amigo secreto**.

### 12.5 Conteúdo

1. Confira se nenhuma imagem do projeto tem marca, logo, nome de loja, @ da conta, link ou chamada para comprar. As imagens da equipe já seguem essa regra. O risco é sobrar alguma do C01 ou do C08 no painel **Assets**.
2. Confira se **não há som** ligado ao efeito.
3. Riscos conhecidos e aceitos pela equipe (não mude nada):
   - carta **02 (TRANSFERÊNCIA DE 10 REAIS)**: nota verde genérica com "10", sem a palavra nem o símbolo do Pix e sem banco;
   - carta **10 (O QUE EU PEDI (MILAGRE))**: "milagre" como expressão do dia a dia; o desenho só tem brilhos de 4 pontas, nada religioso;
   - carta **15 (DESODORANTE (É INDIRETA?))**: frasco liso, sem rótulo; a piada é com a própria pessoa, sem falar de corpo;
   - cartas de carro **04, 11 e 21**: aromatizante redondo (não é pinheirinho), celular com a tela apagada e carro parado, volante sem emblema.
   Se a revisão implicar com alguma delas, troque pela reserva (Parte 17).

### 12.6 Salvar e fazer backup

1. Confira a barra de título (`C06-meu-amigo-secreto`) e aperte **Ctrl+S**.
2. Rode: `Copy-Item -Recurse -Force "$BASE\projetos\C06-meu-amigo-secreto*" "$BASE\projetos\backup\"`

---

## Parte 13: Ícone e envio (de 20/11 a 24/11/2026)

### 13.1 A data

**Hoje é sexta, 20/11/2026, ou depois?** Se ainda não chegou 20/11, **pare**: volte à Parte 11. Se 24/11 já passou e o C06 não foi enviado, envie hoje e avise a nuvem (Parte 0.2).

### 13.2 O desafio

1. Veja no `PRONTO-PARA-MONTAR.md` (12.1) a decisão do Vini sobre o desafio **"Nov Social Randomizer Sub Challenge"** e, se aparecer, sobre qualquer desafio novo de fim de ano.
2. Decida:
   - **A ordem manda entrar num desafio, com o nome dele:** no formulário, selecione **esse** desafio no campo **Challenge**. Se ele não aparecer na lista (por exemplo, porque o prazo acabou ou porque não aceita efeito novo), deixe **Challenge** vazio, envie e anote.
   - **A ordem manda não entrar**, ou não fala de desafio nenhum mas a decisão já saiu: deixe **Challenge** vazio.
   - **A decisão ainda não saiu:** mande uma mensagem para a nuvem dizendo que o C06 está pronto e esperando só o desafio, e espere até **terça, 24/11, 12h**. Sem resposta até lá, **envie com Challenge vazio** e avise. Se esse horário já passou quando você chegar aqui, envie na hora com Challenge vazio e avise. Este efeito é de data: cada dia de espera come a folga para corrigir uma reprovação antes da gravação do dia 29/11. (Regra proposta pela equipe que escreveu este guia; se o `PRONTO-PARA-MONTAR.md` disser outra coisa, vale ele.)
   - **Como ler a ordem de 06/11, 05:50** ("C01 e os outros sorteios: NÃO faça o Submit até sair a decisão do Vini"): para o C06, ela é cumprida pela espera até **24/11, 12h** descrita acima. Ela **não** manda segurar o C06 depois desse horário. Só vale outra regra se o `PRONTO-PARA-MONTAR.md` tiver uma linha **com o nome do C06** (por exemplo, na tabela da seção 2 ou numa atualização datada depois de 06/11).
3. **Nunca aceite os termos de um desafio por conta própria.** Se aparecer outro desafio na lista que não esteja na ordem (por exemplo, um de Natal), anote o nome e o prazo no relatório e conte para a nuvem, mas não selecione.

### 13.3 Ícone (Create icon)

Pela ordem da equipe, o ícone do formulário 5.16 sai do **Create icon**, com uma foto modelo, e não do `icone_162.png`.

1. Clique em **Create icon** na barra de cima (o mesmo caminho do C08 e do C01).
2. Escolha um modelo de rosto e espere o efeito aparecer nele.
3. **Ícone 1, o resultado:** clique para sortear até parar numa destas cartas, que têm frase curta, letra grande e nenhum risco de revisão. Na ordem de preferência:
   1. **MEIA / (DE NOVO)** (carta 01; o presente mais clássico do amigo secreto);
   2. **PANETONE QUE / NINGUÉM COME** (carta 05);
   3. **CHOCOLATE / DERRETIDO** (carta 13);
   4. **PANTUFA NUM / CALOR DE 40°** (carta 09);
   5. **KIT SABONETE / (O 3º DO ANO)** (carta 08).
   Com 5 cartas boas em 26, devem bastar uns 5 cliques. **Não use** no ícone as cartas 02, 03, 10 e 15. Enquadre o rosto e a etiqueta inteira, com a etiqueta ocupando a maior parte do quadrado.
4. **Ícone 2, a pergunta:** se der para ter 2 ícones, faça o segundo com o **título** ("NO AMIGO SECRETO / EU VOU GANHAR…" com a caixa fechada e o "?"), voltando ao começo do efeito.
5. Confira na prévia pequena se o texto do ícone 1 dá para ler. Se não der, tente outra carta da lista.
6. Clique em **Done** (ou **Submit**, conforme a versão).

**Plano de exceção:** se o Create icon não funcionar e o formulário tiver um botão de **Upload** de PNG, use `<A>\icone_162.png` (caixa dourada com laço vermelho e um "?" grande, fundo verde-pinheiro) e, como 2º, `<A>\icone_alt_162.png` (caixa verde aberta com o "?" saindo e a tampa voando, fundo dourado). Os dois têm 162×162 e o desenho dentro da área segura de 144×144. Anote no relatório.

### 13.4 O formulário

1. Clique em **Submit**, no canto de cima à direita.
2. **Atenção, o passo mais importante do envio.** O formulário pode oferecer três caminhos:
   - **Submit a new effect** (enviar um efeito novo): **é este.**
   - **Update an existing effect**: aparece quando a conta tem efeitos **Active**. **Não use.** Ele trocaria o Torcedômetro (ou outro efeito) pelo C06.
   - **Replace an existing effect**: aparece com efeitos em **Draft** ou **Needs revision**. **Não use**, pelo mesmo motivo.

   Como este projeto é uma cópia do C01, o formulário pode já vir com o nome **Torcedômetro** ou com o ícone do C01. **Se isso acontecer, pare**: volte e escolha **Submit a new effect**. Se a tela não oferecer essa opção, não envie: avise a nuvem com um print.

   > O C01 foi feito a partir do projeto do C08, e os dois entraram como efeitos separados. Então o caminho de "efeito novo" funciona nesta conta. Mesmo assim, confira sempre.

3. Preencha:

| Campo | O que colocar |
|---|---|
| **Effect name** | `Meu amigo secreto` (17 caracteres; limite 25), com **M** maiúsculo e o resto em minúsculas. Sem reticências, sem "AI" (as imagens não usam IA generativa). O nome não tem acento, então não há versão "sem acento". Se recusar por nome repetido: `Roleta do amigo secreto` (23). Se recusar de novo: `Presente do amigo secreto` (25, exatamente no limite; só serve se o campo aceitar 25 contando os espaços, a confirmar). |
| **Effect icon** | Os ícones do Create icon (13.3): 1º o resultado, 2º o título |
| **Hint** (lista) | A opção de **tocar na tela**. Se houver opção em português, use ela (ex.: "Toque na tela"). Se a lista for só em inglês, a mesma que você usou no C01 (provavelmente "Tap the screen" ou parecido). Se o campo for **texto livre**: `Toque pra abrir`. |
| **Sound** (som) | **Nenhum.** Não ligue som nem música. |
| **Challenge** | Conforme a 13.2. |
| **Trend** | Deixe **vazio**, a não ser que o `PRONTO-PARA-MONTAR.md` mande outra coisa. Se aparecer uma trend de Natal, amigo secreto ou fim de ano, anote o nome no relatório e conte para a nuvem, mas **não segure o envio** por isso (a confirmar na sua versão: o que o campo faz). |
| **Demo video** | `<BASE>\videos-demo\C06-demo.mp4` |

**Se aparecer algum campo que não está na tabela** (a versão pode ter mudado):

| Campo | O que colocar |
|---|---|
| **Description** (descrição) | `Sorteio sobre a cabeça para o amigo secreto de Natal. A pessoa toca na tela, o presente abre e mostra o que ela vai ganhar: meia (de novo), panetone que ninguém come, um abraço e um “depois te dou” e mais 23 resultados. Sem marca, loja, bebida ou pessoa real.` (259 caracteres). Se o campo for pequeno: `Toque na tela e descubra o que você vai ganhar no amigo secreto.` (64) |
| **Category** | A mais próxima de **Funny** (engraçado); senão, **Randomizer** (sorteio); senão, **Interactive** |
| **Tags** | `amigo secreto`, `amigo oculto`, `natal`, `presente`, `sorteio`. Se não aceitar espaço nem acento: `amigosecreto`, `amigooculto`, `natal`, `presente`, `sorteio`. Se tiver que ser em inglês: `secret santa`, `christmas`, `gift`, `randomizer`, `funny`. Reserva, se alguma for recusada: `humor`, `fim de ano`, `roleta`. |
| **Comentários para a revisão** ("Notes", "Additional comments") | O texto em inglês e, embaixo, o em português, que estão logo abaixo desta tabela |
| Qualquer outro | Deixe o padrão e anote |

**Texto para comentários** (só se o campo existir):

> Head randomizer for Christmas Secret Santa ("amigo secreto" in Brazil). Tap the screen, the gift opens and shows what you will get, such as "socks (again)", "a panettone nobody eats" or "a hug and an 'I'll give it to you later'". 26 original light-humor texts in Brazilian Portuguese, with simple generic drawings. No brands, logos, stores, alcohol, religious symbols, Santa Claus or real people. No generative AI.
>
> Sorteio sobre a cabeça para o amigo secreto de Natal. A pessoa toca na tela, o presente abre e mostra o que ela vai ganhar: meia (de novo), panetone que ninguém come, um abraço e um “depois te dou” e mais 23 resultados. Sem marca, loja, bebida ou pessoa real.

**Se a carta 05 (PANETONE QUE NINGUÉM COME) tiver sido trocada pela reserva R3** (Parte 17), troque nos dois textos acima e na descrição: em português, "panetone que ninguém come" por "pano de prato com crochê"; em inglês, "a panettone nobody eats" por "a crochet-trimmed dish towel". As outras trocas não mexem nos textos.

### 13.5 Enviar

1. Revise o nome: "Meu amigo secreto", sem espaço sobrando no começo ou no fim.
2. Confira de novo se está no caminho **Submit a new effect**.
3. Clique em **Submit**.
4. Tire um print da confirmação e salve em `<BASE>\prints\C06-enviado.png`.
5. Mande para a nuvem: nome enviado, data e hora, status, tamanho do pacote, caso (A/B, T/S), versão (512×256 ou quadrada), cartas usadas nos ícones e se entrou em algum desafio.

---

## Parte 14: Acompanhar o status

1. Abra **Manage Effects**.
2. **Confira se o C06 aparece separado dos outros**, com o nome "Meu amigo secreto", e se o **Torcedômetro** continua lá com o nome dele. Se o Torcedômetro sumiu ou mudou de nome, o envio caiu em "Update" ou "Replace". Avise a nuvem na hora, com print, e não faça mais nada nesses dois efeitos.
3. Confira o status uma vez por dia, de manhã, até sair o resultado:

| Status | O que fazer |
|---|---|
| **Draft** | Clique em **Finish submission** e termine. |
| **Under review** | Esperar (1 a 3 dias úteis; enviando em 20/11, a equipe conta com o resultado até qua 25/11). |
| **Needs revision** | Leia o motivo, corrija (Partes 16 e 17) e **reenvie no mesmo dia**, por este projeto, com **Replace an existing effect** apontando para **Meu amigo secreto** (a confirmar na sua versão: o nome da opção). É o único caso em que "Replace" é usado, e só no próprio C06. Avise a nuvem. A meta é estar **Active até sábado, 28/11**. |
| **Active** | Anote a data e pegue o link (Manage Effects → menu ⋯ do efeito → **Share**). Mande para a nuvem na hora: ele entra na gravação do Vini de **domingo, 29/11**. |
| **Deactivated** | Leia o motivo e avise a nuvem. |

---

## Parte 15: Resumo de 1 tela (para quem já fez o C01)

**Na montagem (assim que o C06 for liberado):**
1. Conferir os arquivos e salvar `C06-conferencia-arquivos.csv` (0.5).
2. Backup do C01 → abrir o C01 → **Save As `C06-meu-amigo-secreto`** → conferir a barra de título.
3. Assets: renomear os antigos para `ANTIGO_…`.
4. Importar `<A>\titulo_toque.png` (→ `amigo_titulo`) e a sequência `<A>\cartas\` (→ `cartas_amigo`, 26 frames, 1º MEIA (DE NOVO), último PRESENTE SEM NOTA PRA TROCAR).
5. Title → Texture = `amigo_titulo`. RandomAnimationSequence → sequência = `cartas_amigo` (Caso A no Animation Sequence, Caso B no Image, Caso S também no script).
6. Apagar os `ANTIGO_…`. Se der "em uso", achar a referência.
7. Conferir posição (ilhós redondo, peça inteira), lógica (TapToSpin ligado, 2, 0.3) e checklist; fazer 15 sorteios.
8. Tamanho, Test performance, demo `C06-demo.mp4` (sem as cartas 02, 03, 10 e 15 no vídeo).
9. Backup, relatório "aguardando 20/11", resumo para a nuvem. **Sem Submit.**

**Na sexta, 20/11/2026 (ou no primeiro dia possível até 24/11):**
1. Ler o `PRONTO-PARA-MONTAR.md`.
2. Status dos outros sorteios (duplicidade = parar); conferir se as imagens mudaram (CSV); nome; conteúdo; backup.
3. Desafio conforme a ordem → **Create icon** (carta 01, 05, 13, 09 ou 08 + título) → **Submit a new effect** → `Meu amigo secreto`, hint de toque, sem som, trend vazio, demo.
4. Manage Effects: o C06 aparece separado. Status 1 vez por dia; Active → link para a nuvem (gravação de 29/11).

---

## Parte 16: Problemas comuns e soluções

| Problema | Causa provável | Solução |
|---|---|---|
| A barra de título ainda diz C01 | O Save As não foi feito ou não pegou | **Não salve.** Feche sem salvar, reabra o C01 e faça a Parte 1.2 de novo. Se já salvou por cima, restaure de `projetos\backup\`. |
| Não acho o projeto do C01 | Nome diferente ou outra pasta | Veja o `relatorio-montagem.md` e o `reconhecimento.md`. Se não existir, use o do C02 (Parte 1.2, último bloco) ou o Plano B1 (Parte 18). |
| A pasta `assets` veio só com o `gerar.py`, sem imagens | A equipe ainda não publicou as imagens | Baixe o zip de novo mais tarde. Se continuar, avise a nuvem (Parte 0.5, passo 3). |
| Os assets novos vieram com "1" ou "(2)" no nome | Os antigos não foram renomeados antes | Siga mesmo assim: identifique os novos pela miniatura (etiqueta de presente com o ilhós e a caixa verde em cima) e renomeie para `amigo_titulo` e `cartas_amigo`. |
| No giro aparece um ingresso do C01 (com recortes nas laterais) | A sequência antiga continua ligada em algum lugar | Parte 4.2: confira Animation Sequence, Image, o script (Caso S) e a caixa do randomizador. |
| "Asset em uso" ao apagar o antigo | Idem | Parte 5, passo 3. |
| A sequência veio com menos de 26 quadros ou fora de ordem | Seleção incompleta | Apague `cartas_amigo` e importe de novo com **Ctrl+A**. |
| Esticado (o ilhós virou ovo) | Size ou Stretch Mode diferente do C01, ou mistura de versão quadrada com 2:1 | Confira se o título e as cartas são da **mesma** versão do C01 (512×256 ou `quadrado_512`). Depois, Parte 5.1 do guia do C01. |
| Dá para ver o fundo pelo furinho da etiqueta | É de propósito: o miolo do ilhós é transparente | Nada a fazer. |
| A etiqueta parece puxada para a direita | É de propósito: a ponta do ilhós fica à esquerda | Nada a fazer. Não mude o **Position X** (Parte 6). |
| A caixa de cima ou as estrelinhas saem cortadas no topo da tela | Peça alta demais para aquele rosto | Baixe um pouco o **Position Y** dos dois objetos (copie o 2D Transform de um para o outro) ou reduza a **Scale** em 5% (X e Y juntos). |
| A ponta esquerda (ilhós e barbante) sai cortada na lateral da tela | Peça larga demais | Reduza a **Scale** em 5% (X e Y juntos) nos dois objetos e confira de novo nos 3 rostos. |
| Texto difícil de ler (principalmente as cartas 25 e 26) | Compressão baixa ou peça pequena | Compressão **High** e, se preciso, Scale +10% (X e Y juntos), conferindo se tudo cabe. |
| Clicar não gira | TapToSpin desligado ou clique fora da imagem | Parte 7. Clique **dentro** do Preview. |
| O título some sozinho antes do toque | Igual ao C01 | Use a mesma solução que você usou no C01 (TitleDelay, título sem etiqueta ou Plano C). |
| Sai sempre a mesma carta | Modo de reprodução | Parte 8.3: **Shuffle** ou **Random**. Se não resolver, Plano C. |
| Pacote acima de 8 MB | Sobrou coisa do C01 ou do C08 | Parte 9. |
| O programa pede atualização no dia do envio | Saiu versão nova | Se der para enviar sem atualizar, envie e atualize depois. Se o envio exigir a atualização: atualize (https://effecthouse.tiktok.com/download), reabra o projeto, refaça o checklist da Parte 8.2 com 5 sorteios e envie. Anote a versão nova. |
| O formulário veio com "Torcedômetro" preenchido | Caiu em Update ou Replace | Parte 13.4, passo 2: volte e escolha **Submit a new effect**. |
| O formulário recusa o nome | Nome repetido | `Roleta do amigo secreto` → `Presente do amigo secreto`. |
| O formulário recusa o vídeo | Formato, duração ou tamanho | Parte 10, passo 6 (ffmpeg). |
| O formulário abre no navegador e pede login | Sessão web do TikTok | Seção 0.8, item 2, com o link. |
| O desafio da ordem não aparece no campo Challenge | Prazo acabou ou não aceita efeito novo | Deixe vazio, envie e anote (Parte 13.2). |
| **Needs revision** por dinheiro, banco ou "Pix" | Carta 02 | Troque a 02 pela R2 (Parte 17) e reenvie. |
| **Needs revision** por religião | Carta 10 ("milagre") | Troque a 10 pela R4 e reenvie. Se o motivo falar do Natal em geral, sem citar carta, **não reenvie**: mande o print para a nuvem e espere ordem. |
| **Needs revision** por direção perigosa ou celular no carro | Cartas 11 (porta-celular) ou 21 (capa de volante) | Troque só a carta citada pela reserva livre (Parte 17) e reenvie. Se não citar carta, troque as duas e avise a nuvem. |
| **Needs revision** por marca de comida | Cartas 05 (panetone) ou 13 (chocolate) | Troque a carta citada pela R3 (Parte 17). Se citar as duas: a 13 pela R3 e a 05 pela R1. Se a 05 for trocada, ajuste os textos (Parte 13.4, último parágrafo). |
| **Needs revision** por ofensa ou "corpo" | Carta 15 (desodorante) | Troque a 15 pela R1 e reenvie. |
| **Needs revision** citando a mão 👆 ou "figura humana" | A única mão da peça é o 👆 da pílula do título | Importe `<A>\titulo.png` (sem a pílula), renomeie para `amigo_titulo_sem_toque`, ponha no **Title** (Parte 4.1), apague o `amigo_titulo`, refaça a Parte 8.2 e reenvie. Avise a nuvem. |
| **Needs revision** por "duplicado" ou "parecido com outro efeito" | Mesmo template do C01 | Mande o print para a nuvem. **Não** reenvie sem ordem: a equipe decide se muda o visual. |
| **Needs revision** por marca, logo ou outro motivo com número de carta | O revisor viu semelhança com algo real | Mande o print do motivo e o número da carta para a nuvem. Enquanto isso, se for uma carta só, troque pela reserva (Parte 17). |
| **Needs revision** por desempenho ou tremor | QA técnico | Test performance, teste com movimento, Parte 9. |
| Pediu login de novo ou está em outra conta | Login expirou | Seção 0.8, com o link. |

---

## Parte 17: Trocar uma carta vetada pela reserva

**A troca é sempre pelo arquivo.** Não adianta mudar só o texto no `textos.json`: o desenho de cada carta está preso ao número dela no `gerar.py`, e a carta nova sairia com o desenho antigo.

As 5 reservas (em `<A>\reservas\`):

| Código | Arquivo | Texto |
|---|---|---|
| R1 | `reserva_01.png` | PORTA-RETRATO / SEM FOTO (a coringa) |
| R2 | `reserva_02.png` | 10 REAIS NUM / ENVELOPE |
| R3 | `reserva_03.png` | BOMBONS / (JÁ COMERAM 3) |
| R4 | `reserva_04.png` | O QUE EU PEDI / (NEM ACREDITO) |
| R5 | `reserva_05.png` | CAPINHA QUE / NÃO SERVE |

| Se vetarem… | Use (nesta ordem, a primeira que ainda estiver livre) |
|---|---|
| carta 02 (TRANSFERÊNCIA / DE 10 REAIS) | R2 → R1 |
| carta 03 (CANECA COM / FRASE DE COACH) | R5 → R1 |
| carta 05 (PANETONE QUE / NINGUÉM COME) | R3 → R1 |
| carta 06 (FONE QUE SÓ / PEGA DE UM LADO) ou 17 (CARREGADOR QUE / NÃO CARREGA) | R5 → R1 |
| carta 10 (O QUE EU PEDI / (MILAGRE)) | R4 → R1 |
| carta 13 (CHOCOLATE / DERRETIDO) | R3 → R1 |
| carta 15 (DESODORANTE / (É INDIRETA?)) | R1 → R5 |
| qualquer outra (ex.: 04, cheirinho; 11, porta-celular; 21, volante) | R1 → R5 → R3 |

**Cada reserva entra uma vez só.** Se a da lista já foi usada, passe para a próxima. A R2 não serve no lugar de outra carta enquanto a 02 estiver no efeito (as duas falam de 10 reais), e a R4 só serve no lugar da 10 (é a mesma arte, sem a palavra "milagre"). Se acabarem as reservas, avise a nuvem e espere: a equipe gera cartas novas.

Exemplo com a carta 02 (troque os números para o seu caso):

```powershell
$A = "$BASE\tiktok-efeitos\efeito-6-meu-amigo-secreto\assets"
New-Item -ItemType Directory -Force "$A\cartas_trocadas" | Out-Null
Move-Item "$A\cartas\carta_02.png" "$A\cartas_trocadas\carta_02.png"
Copy-Item "$A\reservas\reserva_02.png" "$A\cartas\carta_02.png"
(Get-ChildItem "$A\cartas\*").Count    # tem que continuar 26
```

Se o projeto usa as quadradas, faça o mesmo dentro de `$A\quadrado_512\` (`cartas` e `reservas`).

> **Cuidado com o zip:** se depois da troca você extrair o zip da equipe por cima de novo, a carta vetada volta para a pasta `cartas`. Refaça a troca antes de importar, até a nuvem avisar que atualizou os arquivos.

No Effect House:
1. Apague `cartas_amigo` do painel **Assets**. Se der "em uso", tire a sequência do objeto primeiro (Parte 5, passo 3) e tente de novo.
2. Importe a pasta `cartas` de novo (Parte 3.3) e renomeie para `cartas_amigo`.
3. Ligue a sequência de novo (Parte 4.2, inclusive no script, se for Caso S).
4. Teste (Parte 8.2) e faça 5 sorteios.
5. Reenvie com **Replace an existing effect** → **Meu amigo secreto** (a confirmar na sua versão: o nome da opção). Se a carta trocada foi a 05, ajuste os textos (Parte 13.4, último parágrafo).
6. Avise a nuvem qual carta foi trocada e por qual reserva, para atualizar o `textos.json`.

> A cor de cada reserva já combina com a vizinhança da carta que ela substitui. A única exceção: a R5 no lugar da carta 06 deixa duas etiquetas kraft lado a lado no giro (R5 e a carta 07). É só estética, pode ignorar.

---

## Parte 18: Planos B e C (se a cópia do C01 não der certo)

| Plano | Quando usar | Esforço |
|---|---|---|
| **B1: template do zero** | Os projetos do C01 e do C02 não existem, não abrem ou ficaram estragados | médio (≈ 3 h) |
| **B2: preset de Interactions** | Não há template, mas o preset existe | baixo a médio |
| **B3: Visual Scripting nó a nó** | Não há template nem preset | médio |
| **C: script TypeScript** | A lógica do template falha (título some, sorteio viciado, não gira) | baixo |
| **Effect House AI** | Travou em qualquer passo | baixo. Pedidos prontos em `efeito-6-meu-amigo-secreto\script\prompt-effect-house-ai.md` |

### Plano B1: template Randomizer 2D do zero

1. Na tela inicial do Effect House, clique em **Templates** (menu da esquerda).
2. Digite `Randomizer` na busca.
3. Clique no card **Randomizer 2D**. Atenção: **2D**, não 3D.
4. Clique em **Create** ou **Open** (a confirmar na sua versão: o nome do botão) e espere o projeto carregar.
   - **Se não achar "Randomizer 2D":** busque `Random` e `Random Image`, e olhe nas categorias **Interactive**, **Face** e **Game**. Se aparecer um template de sorteio com outro nome, que tenha um objeto de título e uma sequência de imagens sobre a cabeça, use-o e anote o nome real. Se não houver nenhum, vá para o Plano B2.
5. Clique em **File → Save As**, vá até `<BASE>\projetos\` e salve como `C06-meu-amigo-secreto`.
6. Importe o título e as cartas pelas Partes **3.2** e **3.3** deste guia (pule a 3.1: não há imagens antigas do C01). Renomeie para `amigo_titulo` e `cartas_amigo`. Deixe a compressão dos dois em **Automatic** ou **Manual → 512 → High** (Parte 3.3 do guia do C01).
7. Siga as **Partes 2, 4 e 5 do guia do C01** (`efeito-1-torcedometro\guia-montagem.md`), com estas trocas:

| No guia do C01 | No C06 |
|---|---|
| pasta `efeito-1-torcedometro\assets\` | `efeito-6-meu-amigo-secreto\assets\` |
| projeto `C01-torcedometro` | `C06-meu-amigo-secreto` |
| título `titulo_toque` | `amigo_titulo` |
| sequência `cartas_torcedor` | `cartas_amigo` |
| "QUE TORCEDOR / VOCÊ É?" | "NO AMIGO SECRETO / EU VOU GANHAR…" |
| régua: medalha redonda | régua: ilhós redondo |
| cartas de leitura difícil 17, 18, 22 | 25, 26, 06, 12, 17 |

8. Ponha os valores da Parte 7 deste guia: **TapToSpin ligado, TimeToSpin 2, TitleFadeOutTime 0.3**, TitleDelay do template, **26 quadros**. A largura fica em cerca de 1,6 cabeça.
9. Volte para a Parte 8 **deste** guia e siga até o fim. O envio do 5.16 é diferente do guia do C01, e a data do C06 é fixa.

### Plano B2: preset de Interactions (sem ligar fios)

O preset oficial **"Tap Screen to Play Animation Sequence Then Delay Pause"** toca a sequência ao tocar na tela e pausa depois de N segundos. Com o modo **Random** ou **Shuffle**, ela para numa carta qualquer. Exige o componente **Animation Sequence** no objeto.

1. Num projeto vazio (**New Project**/**Blank**; a confirmar na sua versão), salve como `C06-meu-amigo-secreto`. Crie dois **Face Sticker** (**Hierarchy → + → Face Effects → Face Sticker**) e renomeie para `Titulo` e `Cartas`.
2. Importe o título e as cartas (Partes 3.2 e 3.3).
3. `Titulo`: **Image → Texture** = `amigo_titulo`.
4. `Cartas`: **Add Component → Animation Sequence**, com a sequência `cartas_amigo` e o modo **Shuffle** (ou **Random**). Desmarque o **autoplay**, se existir (a confirmar na sua versão).
5. Acerte proporção (2:1), posição e tamanho dos dois, iguais (Parte 5 do guia do C01). O ilhós tem que ficar redondo.
6. Com `Cartas` selecionado, clique em **+ Add interaction** (no Inspector ou no Visual Scripting; a confirmar na sua versão) e escolha **Tap Screen to Play Animation Sequence Then Delay Pause**. Em **Target**, `Cartas`. Em **Delay Pause Seconds**, `2`.
7. Para o título sumir e as cartas aparecerem no toque, adicione o preset **Tap Screen to Delay Show/Hide Object** duas vezes (a confirmar na sua versão: nome exato):
   - Target `Titulo`, ação **Hide**, atraso `0`;
   - Target `Cartas`, ação **Show**, atraso `0`.
8. Deixe `Cartas` **invisível no começo**: desmarque a caixinha do objeto na Hierarchy ou ligue **Start → Set Visibility** (Target `Cartas`, desligado).

**Limite:** este plano não volta ao título quando a pessoa aperta gravar. Se der, ligue o evento de início de gravação (**Video Record Start** ou **Record Start**; a confirmar na sua versão) em dois **Set Visibility**: `Titulo` ligado e `Cartas` desligado. Se não der, envie assim mesmo e anote: a pessoa toca de novo durante a gravação e o giro acontece no vídeo.

### Plano B3: Visual Scripting nó a nó

Mesmos objetos do B2 (passos 1 a 5, mas **sem** o modo Shuffle/autoplay, porque quem controla a sequência é o nó). Crie duas **variáveis** no painel de variáveis do Visual Scripting (a confirmar na sua versão: onde ficam):
- `podeTocar` (**Boolean**, valor inicial **true**);
- `sorteio` (**Number**, valor inicial **0**).

Adicione os nós com o botão direito no painel → buscar o nome.

**Ao abrir o efeito:**
1. **Start** → **Set Visibility** (Target `Titulo`, visível **ligado**).
2. → **Set Visibility** (Target `Cartas`, visível **desligado**).
3. → **Set Variable** `podeTocar` = **true**.

**Ao tocar:**
1. **Screen Tap** (saída **Next**) → **If** (Condition = **Get Variable** `podeTocar`). O nó pode se chamar **Branch** (a confirmar na sua versão).
2. Saída **True** → **Set Variable** `podeTocar` = **false** (ignora toques durante o giro).
3. → **Set Visibility** (`Titulo`, **desligado**).
4. → **Set Visibility** (`Cartas`, **ligado**).
5. → **Animation Sequence Controller**, entrada **Play**: From `0`, To `25`, Loop **ligado** (pode se chamar **Set Animation Sequence**; a confirmar na sua versão).
6. → **Wait for Seconds** = `2`.
7. → **Index Generator** no modo **Random**, com **26** itens (ou intervalo 0 a 25; a confirmar na sua versão: nome dos campos) → **Set Variable** `sorteio` = saída do Index Generator.
8. → **Animation Sequence Controller**, entrada **Play**: **From** = **Get Variable** `sorteio`, **To** = **Get Variable** `sorteio`, Loop **desligado**. Com From igual a To, a sequência mostra só aquele quadro (0 = carta 01, 25 = carta 26).
9. → **Set Variable** `podeTocar` = **true** (um novo toque gira de novo).

> **Não ligue o nó Random direto em From e em To.** Ele gera um número novo a cada leitura e daria 2 números diferentes. Por isso o valor passa pela variável `sorteio`.

**Ao gravar:** ligue o evento **Video Record Start** (ou a opção **Reset on Record = On**; a confirmar na sua versão) na mesma sequência do "Ao abrir o efeito".

### Plano C: script pronto (TypeScript)

O script do C01 serve sem mudança, porque lê a quantidade de quadros da própria sequência: `tiktok-efeitos\efeito-1-torcedometro\script\TorcedometroController.ts`. **Não mexa no arquivo da pasta do efeito 1.** Só copie o conteúdo.

- **Se o projeto já é Caso S:** o script já está nele. Basta a Parte 4.2, passo 4.
- **Se não é:** siga a Parte 15, Plano C, do guia do C01, passos 1 a 19, com estas trocas: projeto `C06-meu-amigo-secreto-script`; no campo **Sequencia Cartas**, `cartas_amigo`. Se este plano der certo, é **esta** cópia que vai ser enviada: anote no relatório e use o nome dela no lugar de `C06-meu-amigo-secreto` nas Partes 11 a 14.
- O script **ainda não foi rodado** dentro do Effect House pela equipe (a confirmar). Se der erro, use o **Pedido 4** de `efeito-6-meu-amigo-secreto\script\prompt-effect-house-ai.md`.

### Effect House AI

Veja no `reconhecimento.md` (item 3) se o assistente funcionou nesta conta. Os pedidos prontos, em inglês, estão em `efeito-6-meu-amigo-secreto\script\prompt-effect-house-ai.md`:

| Pedido | Quando |
|---|---|
| 1 | A troca de imagens na cópia do C01 travou (Partes 3 a 5) |
| 2 | Precisa configurar o template Randomizer 2D do zero (Plano B1) |
| 3 | Não há template: montar tudo do zero (Planos B2 e B3) |
| 4 | O script do Plano C deu erro |

Use o assistente para **destravar** um passo, sem mudar a ideia, os textos ou as imagens. Se ele oferecer "Submit" ou "Publish", recuse: o envio é pela Parte 13. Depois, refaça os checklists da Parte 8.

---

## Parte 19: O que anotar no relatório

Em `<BASE>\relatorio-montagem.md`, na seção do C06:

**Na montagem:**
- Versão do Effect House.
- Nome real do projeto usado como base (C01 ou C02) e se o backup foi feito.
- Caso A ou B, Caso T ou S, versão 512×256 ou quadrada, título com ou sem etiqueta.
- Se o programa pôs a sequência na ordem certa sozinho (1º MEIA (DE NOVO), último PRESENTE SEM NOTA PRA TROCAR).
- Se mudou posição ou escala, com os valores antigos e os novos.
- Valores da lógica conferidos (TapToSpin, TimeToSpin, TitleDelay, TitleFadeOutTime).
- Resultado do teste de sorteio: quantas cartas diferentes e a que mais repetiu.
- Tamanho do pacote e resultado do Test performance (ou a mensagem, se não rodou).
- Plano usado: cópia do C01, cópia do C02, B1, B2, B3 ou C.
- "C06 montado e testado, aguardando 20/11", com data e hora.

**No dia do envio:**
- O que o `PRONTO-PARA-MONTAR.md` dizia sobre o C06 e o desafio.
- Status dos outros sorteios em Manage Effects.
- Resultado da conferência dos arquivos (12.3): nada mudou, ou o que mudou e o que você refez.
- Cartas usadas nos ícones do Create icon.
- Caminho escolhido no Submit (tem que ser **Submit a new effect**), nome enviado, hint escolhido, desafio (qual ou nenhum), opções do campo **Trend**.
- Data e hora do envio, print e status. Confirmação de que o Torcedômetro continua separado em Manage Effects.
- Qualquer "a confirmar" deste guia que você viu de verdade, e o que era.

---

## Fontes consultadas

Documentação oficial do Effect House (lida por resumos de busca, porque o site não abre daqui):
- Envio, com as opções "Submit a new effect", "Update an existing effect" (efeitos Active) e "Replace an existing effect" (Draft ou Needs revision), e o limite de 10 reenvios: https://effecthouse.tiktok.com/learn/guides/publishing/publish/submit-your-effect
- Ícone: botão **Create icon** na barra de título, que abre o Effect Icon Creator, com modelos de rosto prontos, até 2 ícones, PNG 162×162 e área segura 144×144: https://effecthouse.tiktok.com/learn/guides/publishing/effect-icon-creation
- Status e retirada da revisão: https://effecthouse.tiktok.com/learn/guides/management-and-growth/manage-your-effect
- Template Randomizer 2D (Title, RandomAnimationSequence, TapToSpin, TimeToSpin, TitleDelay, TitleFadeOutTime, reinício em Effect Start e Video Record Start): https://effecthouse.tiktok.com/learn/guides/tutorials/template-tutorials/randomizer-2d
- Preset "Tap Screen to Play Animation Sequence Then Delay Pause" (Target e Delay Pause Seconds; exige Animation Sequence): https://effecthouse.tiktok.com/learn/guides/visual-scripting/interactions/tap-screen-to-play-animation-sequence-then-delay-pause · visão geral: https://effecthouse.tiktok.com/learn/guides/visual-scripting/interactions
- Nós (Random gera número novo a cada leitura; Index Generator com Loop/Random/Shuffle), limites de imagem e de pacote, vídeo demo: `tiktok-efeitos/pesquisa/03-tecnico-effect-house.md`.

Da própria equipe:
- Formulário do Effect House 5.16 (nome, ícone pelo Create icon, hint de lista, som, challenge, trend e demo), pasta `C:\Users\Pichau\Desktop\Efeitos` e a regra de esperar a decisão do desafio: `PRONTO-PARA-MONTAR.md`, atualizações de 06/11.
- Janela de envio (20 a 24/11, não antes por causa da janela de 30 dias), gravação do Vini em dom 29/11 e estreia em 30/11 ou 01/12: `plano-curto-prazo.md`, cronograma S2 a S4.
- C08 e C01 enviados como efeitos separados, C01 com 26 cartas e 1,6 MB: `STATUS.md`.
- Caminho de cópia do projeto do C01: `efeito-4-meu-proximo-carro/guia-montagem.md` (C02) e `efeito-7-simpatia-da-virada/guia-montagem.md` (C07), que usam o mesmo método.
- Textos, nome, alternativas, hint, tags, comentários, reservas e cartas sensíveis: `efeito-6-meu-amigo-secreto/textos.md` e `textos.json`.
- Imagens, identidade visual, régua do ilhós, assimetria de 18 px e cores das reservas: `efeito-6-meu-amigo-secreto/assets/LEIA-ME.md` e `gerar.py`.
- Medidas conferidas pela equipe nos arquivos de `assets/` em 06/11/2026: área com desenho de 5 a 506 × 3 a 248 px nas cartas (dentro da área do C01), peso de 2,59 MB para título + 26 cartas, maior arquivo `carta_18.png` com 110 KB e fonte de 41 a 54 px por carta (tabela da 0.7, tirada de uma cópia do `gerar.py` rodada fora da pasta, com saída idêntica aos arquivos).
