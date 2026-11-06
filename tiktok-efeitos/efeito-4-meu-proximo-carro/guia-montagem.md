# Guia de montagem: "Meu próximo carro" (C02)

**Para quem é:** para o Montador, o Claude que opera o PC do Vini. Também serve para qualquer pessoa que já tenha montado o Torcedômetro (C01).
**Versão do guia:** 1.1 · 06/11/2026 (revisado pela QA) · escrito para o Effect House **5.16** no Windows, a versão que o Montador encontrou no PC.
**Envio:** até **terça, 17/11/2026**. A data vale só se a decisão sobre o desafio já tiver saído (Parte 12.1).
**Tempo total:** cerca de **2 h** reaproveitando o projeto do C01. Se for preciso montar do zero (Parte 17), reserve 4 h.

> **Vini, se você estiver lendo:** não precisa fazer nada aqui. Você só será chamado nos casos da seção 0.7, sempre com o link direto.

### Como ler as marcas

- **(a confirmar na sua versão)**: a equipe não conseguiu ver essa tela, porque o site do Effect House não abre de onde pesquisamos. Se o botão ou o campo tiver outro nome, use o parecido e **anote no relatório** o nome real.
- Os nomes de botões e painéis estão **em inglês e em negrito**, como aparecem no programa.
- "Clique" é com o botão esquerdo. Quando for o direito, o passo diz "clique com o botão direito".
- **Você já montou o C08 e o C01.** Quando este guia diz "faça como no C01", vale o que você fez de verdade e anotou no `relatorio-montagem.md`, mesmo que seja diferente do guia do C01.

### O que vamos montar (resumo)

1. Sobre a cabeça aparece uma etiqueta grafite com a frase **"MEU PRÓXIMO / CARRO VAI SER…"**, um carro coberto com capa e um **"?"** num círculo amarelo em cima, e a pílula **"👆 TOQUE NA TELA"** na faixa de asfalto de baixo.
2. A pessoa toca na tela. O título some e as cartas giram por cerca de 2 segundos.
3. O giro para numa das **26 cartas**, por exemplo **"SÓ PEGA / NO TRANCO"** ou **"SUV EM 72 / PARCELAS"**. A carta fica presa na cabeça.
4. Quando a pessoa aperta **gravar** no TikTok, o efeito volta para o título.

**É o mesmo efeito do Torcedômetro, com outras imagens.** Usa o mesmo template (Randomizer 2D), o mesmo quadro de imagem (512×256) e as mesmas **26 cartas**, e a lógica é igual. Por isso o caminho principal deste guia é **copiar o projeto do C01 já pronto e trocar só o título, as cartas e o ícone**. A lógica, a posição e o tamanho continuam os do C01, que já foram testados. O efeito é para **1 pessoa** (1 rosto).

---

## Parte 0: Antes de começar

### 0.1 Pré-requisitos (confira todos)

| # | Pré-requisito | Como conferir |
|---|---|---|
| 1 | O C02 está liberado na tabela da seção 2 do `PRONTO-PARA-MONTAR.md` | Abra https://raw.githubusercontent.com/quantopagarei-sketch/quantocobrarpj/main/tiktok-efeitos/PRONTO-PARA-MONTAR.md. Se o C02 ainda estiver só em "Vem aí", **não comece**. |
| 2 | O projeto do C01 existe, abre e passou nos testes | No `relatorio-montagem.md`, seção do C01: nome do projeto, Caso A/B, plano usado (template ou script) e título usado |
| 3 | O Effect House está logado na conta **Car Shop** | Tela inicial (como no C01) |
| 4 | Você já sabe como o seu Effect House importa uma Texture Sequence (arquivos ou pasta) e como funciona o **Create icon** | Você fez isso no C01 e no C08. Anotações no relatório |
| 5 | O ffmpeg está instalado, se o vídeo do C01 precisou de corte | `ffmpeg -version` no PowerShell |

### 0.2 Links

| O quê | Link direto | Quem usa |
|---|---|---|
| Arquivos da equipe (zip com tudo) | https://github.com/quantopagarei-sketch/quantocobrarpj/archive/refs/heads/main.zip | Montador |
| Ordens da equipe (atualizadas todo dia) | https://raw.githubusercontent.com/quantopagarei-sketch/quantocobrarpj/main/tiktok-efeitos/PRONTO-PARA-MONTAR.md | Montador |
| Tutorial oficial do template (em inglês) | https://effecthouse.tiktok.com/learn/guides/tutorials/template-tutorials/randomizer-2d | Consulta |
| Guia oficial de envio (opções "new / update / replace") | https://effecthouse.tiktok.com/learn/guides/publishing/publish/submit-your-effect | Consulta |
| Guia oficial do ícone (Create icon) | https://effecthouse.tiktok.com/learn/guides/publishing/effect-icon-creation | Consulta |
| Preset de interação usado no Plano B2 | https://effecthouse.tiktok.com/learn/guides/visual-scripting/interactions/tap-screen-to-play-animation-sequence-then-delay-pause | Consulta |
| Guia do C01 (base deste) | `tiktok-efeitos\efeito-1-torcedometro\guia-montagem.md` | Consulta |

### 0.3 Pastas (vale para o guia inteiro)

Neste guia, **`<BASE>`** é a pasta "Efeitos" que você usa no PC. Pela última ordem da equipe, ela é `C:\Users\Pichau\Desktop\Efeitos`. Se essa pasta não existir, a pasta é `Documentos\Efeitos`.

| Apelido | Caminho |
|---|---|
| `<BASE>` | `C:\Users\Pichau\Desktop\Efeitos` (ou `Documentos\Efeitos`) |
| `<A>` (imagens do C02) | `<BASE>\tiktok-efeitos\efeito-4-meu-proximo-carro\assets` |
| Projeto novo | `<BASE>\projetos\C02-meu-proximo-carro` |
| Vídeo demo | `<BASE>\videos-demo\C02-demo.mp4` |
| Prints | `<BASE>\prints\C02-*.png` |
| Relatório | `<BASE>\relatorio-montagem.md`, nova seção "C02" |

### 0.4 Baixar e conferir os arquivos

1. Baixe o zip (link da 0.2) e extraia **só a pasta `tiktok-efeitos`** em `<BASE>`, por cima da antiga.
2. Rode no PowerShell:

```powershell
$BASE = if (Test-Path "C:\Users\Pichau\Desktop\Efeitos") { "C:\Users\Pichau\Desktop\Efeitos" } else { Join-Path ([Environment]::GetFolderPath('MyDocuments')) "Efeitos" }
$A = "$BASE\tiktok-efeitos\efeito-4-meu-proximo-carro\assets"
(Get-ChildItem "$A\cartas\carta_*.png").Count            # tem que dar 26
(Get-ChildItem "$A\cartas\*").Count                      # tem que dar 26 (a pasta só pode ter as cartas)
(Get-ChildItem "$A\reservas\reserva_*.png").Count        # tem que dar 4
Get-ChildItem "$A\titulo_toque.png","$A\titulo.png","$A\icone_162.png","$A\icone_alt_162.png" | Select Name, Length
(Get-ChildItem "$A\cartas\*.png" | Measure-Object Length -Maximum).Maximum   # tem que ser menor que 1048576 (1 MB); o esperado é ~105000
Get-ChildItem "$BASE\projetos" | Select Name, LastWriteTime                # ache aqui o projeto do C01
```

> **Em todo PowerShell novo**, rode antes a primeira linha acima (a que define `$BASE`). Os comandos das outras partes dependem dela.

3. Se faltar arquivo, baixe o zip de novo. Se continuar faltando, avise a nuvem. Não chame o Vini por isso.

### 0.5 O que entra no efeito e o que não entra

Todos os arquivos ficam dentro de `<A>` (a pasta `assets` do efeito 4).

| Arquivo | Entra? | Para quê |
|---|---|---|
| `titulo_toque.png` (512×256, fundo transparente) | **Sim (padrão)** | Título "MEU PRÓXIMO / CARRO VAI SER…" com a pílula "👆 TOQUE NA TELA". Vai no objeto **Title**. |
| `titulo.png` (512×256) | Só se o C01 usou o título sem etiqueta | O mesmo título, sem a pílula (Parte 3, passo 4). |
| `cartas\carta_01.png` … `carta_26.png` (512×256 cada) | **Sim** | Os 26 resultados. Entram juntos como **uma** Texture Sequence, na ordem 01→26. |
| `reservas\reserva_01.png` … `reserva_04.png` | Não | Só se uma carta for vetada (Parte 16) |
| `quadrado_512\` (as mesmas imagens em 512×512) | Só se o C01 usou as quadradas | Título e cartas têm que seguir o C01: as duas 512×256 ou as duas quadradas |
| `icone_162.png`, `icone_alt_162.png` | Só no plano de exceção da Parte 12.2 | Pela ordem de 06/11, o ícone sai do **Create icon** |
| `icone_512.png`, `icone_alt_512.png`, `previa.png`, `gerar.py`, `lista-de-arquivos.txt`, `LEIA-ME.md` | Não | Referência da equipe |

**Peso:** `titulo_toque.png` + 26 cartas = **2,43 MB** em PNG (no C01, as mesmas peças tinham 2,15 MB e viraram um pacote de 1,6 MB). O maior arquivo é a `carta_24.png`, com 103 KB.

**Réguas contra imagem esticada:** no título, o **círculo amarelo do "?"** tem que ficar redondo. Nas cartas, valem as **rodas** dos carros. Se virarem ovo, a imagem está esticada.

### 0.6 Ordem das cartas (quadro = posição na sequência)

O quadro 0 é a carta 01. Use a tabela para conferir a ordem (Parte 4) e para anotar o teste de sorteio (Parte 8.3).

| Quadro | Arquivo | Texto | Quadro | Arquivo | Texto |
|---:|---|---|---:|---|---|
| 0 | carta_01 | POPULAR 1.0 / COM 300 MIL KM | 13 | carta_14 | COM LUZ DA / INJEÇÃO ACESA |
| 1 | carta_02 | SUV EM 72 / PARCELAS | 14 | carta_15 | EMPRESTADO / DO CUNHADO |
| 2 | carta_03 | REBAIXADO QUE / RASPA EM TUDO | 15 | carta_16 | COM SOM MAIS / CARO QUE ELE |
| 3 | carta_04 | ZERO KM / (FINALMENTE) | 16 | carta_17 | AUTOMÁTICO E / COM AR GELADO |
| 4 | carta_05 | SÓ PEGA / NO TRANCO | 17 | carta_18 | MOVIDO A / ESPERANÇA |
| 5 | carta_06 | COM ADESIVO / DA FAMÍLIA | 18 | carta_19 | ESSE MESMO / SÓ QUE LAVADO |
| 6 | carta_07 | BICICLETA / (POR ENQUANTO) | 19 | carta_20 | CONSÓRCIO QUE / NUNCA SAI |
| 7 | carta_08 | CARRO DE APP / COM BALINHA | 20 | carta_21 | COM CÂMERA / DE RÉ (UFA) |
| 8 | carta_09 | HERDADO DO VÔ / (ZERADINHO) | 21 | carta_22 | COM TETO SOLAR / (É UM FURO) |
| 9 | carta_10 | COM PORTA DE / OUTRA COR | 22 | carta_23 | CARRINHO / DE MERCADO |
| 10 | carta_11 | CAMINHONETE / DO AGRO | 23 | carta_24 | USADO COM / CHEIRO DE NOVO |
| 11 | carta_12 | QUITADO E / NO MEU NOME | 24 | carta_25 | COMPLETINHO / (ATÉ O TAPETE) |
| 12 | carta_13 | O DOS SONHOS / (EM MINIATURA) | 25 | carta_26 | COM BARULHINHO / MISTERIOSO |

### 0.7 O que depende do Vini (o mínimo)

Nada, se tudo correr bem. Ele só é chamado se:

1. **O login do Effect House cair** ou se o programa estiver em outra conta. Mande para ele:
   > Abra o Effect House no computador. Vai aparecer um QR code. No celular, abra o **TikTok da conta Car Shop** → **Perfil** → ícone de pessoa (**Adicionar amigos**) → ícone de scanner no canto de cima → aponte para o QR → toque em **Confirmar**. Guia com imagens: https://effecthouse.tiktok.com/learn/guides/getting-started/introduction-to-effect-house/download-and-login
   >
   > Tem que ser o scanner **de dentro do TikTok**. A câmera comum do celular não funciona.
2. **A decisão sobre o desafio "Nov Social Randomizer Sub Challenge"** ainda não saiu. Quem pergunta é a nuvem, não você (Parte 12.1).

O teste no celular é **opcional** e fica de fora deste guia. Se a equipe quiser fazê-lo, junta com outros efeitos num momento só, como na Parte 10 do guia do C01.

### 0.8 Tempo estimado

| Etapa | Tempo |
|---|---|
| Parte 0: baixar e conferir | 10 min |
| Parte 1: copiar o projeto do C01 | 10 min |
| Parte 2: reconhecer o que veio do C01 | 10 min |
| Partes 3 a 5: importar, trocar e limpar | 20 min |
| Partes 6 e 7: posição e lógica (só conferir) | 10 min |
| Parte 8: testar no PC | 25 min |
| Partes 9 e 10: tamanho, desempenho e vídeo demo | 20 min |
| Partes 11 a 13: conferências, ícone, envio e status | 20 min |
| **Total** | **≈ 2 h** |

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

### 1.2 Abrir o C01 e salvar como C02

1. Abra o **Effect House**.
2. Confira a conta **Car Shop**, como no C01. Se for outra conta, **pare** e siga a seção 0.7.
3. Abra o projeto do C01 (lista de projetos recentes da tela inicial, ou **File → Open**; a confirmar na sua versão).
4. **Antes de mexer em qualquer coisa**, clique em **File → Save As**.
5. Vá até `<BASE>\projetos\`.
6. Dê o nome **`C02-meu-proximo-carro`**.
7. Clique em **Salvar**.
8. Confira na **barra de título** da janela se aparece `C02-meu-proximo-carro`. **Só siga em frente se o nome do C02 estiver lá.**

> **Regra deste guia:** antes de cada **Ctrl+S**, olhe a barra de título. Tem que estar escrito `C02-meu-proximo-carro`.

**Se não houver "Save As"** (a confirmar na sua versão):
1. Feche o Effect House.
2. No PowerShell: `Copy-Item -Recurse "$BASE\projetos\C01-torcedometro" "$BASE\projetos\C02-meu-proximo-carro"`. Se o projeto for um arquivo com extensão, copie o arquivo e dê ao novo o nome `C02-meu-proximo-carro` com a mesma extensão.
3. Abra a cópia no Effect House e confira a barra de título.

**Se o projeto do C01 não existir ou não abrir:** monte do zero, pela Parte 17 (Plano B1).

---

## Parte 2: Reconhecer o que veio do C01

Não mude nada nesta parte. Só anote no relatório, na seção do C02.

1. Na **Hierarchy**, clique em **Title**.
2. No **Inspector**, no componente **Image**, leia o nome que está no campo **Texture**. O esperado é `titulo_toque` (ou `titulo`, se no C01 você precisou trocar). **Anote o nome.**
3. Clique em **RandomAnimationSequence**.
4. Veja onde está a sequência das cartas e anote o caso:
   - **Caso A:** existe o componente **Animation Sequence**, e a sequência está no campo dele;
   - **Caso B:** a sequência está direto no campo **Texture** do componente **Image**.
5. Anote o nome da sequência. O esperado é `cartas_torcedor`.
6. Anote, nos dois objetos, os valores de **Position**, **Scale**, **Size** e **Stretch Mode**. Eles vão ficar iguais.
7. Na **Hierarchy**, veja se existe um objeto chamado `Controle` com o script **TorcedometroController**. Se existir, foi usado o Plano C no C01: este é o **Caso S**. Se não existir, a lógica é a do template: **Caso T**.
8. **Caso T:** abra o **Visual Scripting**, clique na caixa do randomizador e anote **TapToSpin**, **TimeToSpin**, **TitleDelay** e **TitleFadeOutTime**. O esperado é: ligado, `2`, o valor do template e `0.3`.
9. Veja no relatório do C01 se ele usou as imagens **512×256** ou as **quadradas** (`quadrado_512`). O C02 tem que usar a mesma versão.

---

## Parte 3: Marcar as imagens antigas e importar as novas

As imagens do C02 têm **os mesmos nomes de arquivo** das do C01 (`titulo_toque.png`, `carta_01.png`…). Para não confundir na hora de trocar, primeiro você muda o nome das antigas no projeto.

### 3.1 Marcar as antigas

No painel **Assets**:

1. Clique com o botão direito no título que você anotou na Parte 2, passo 2 (ex.: `titulo_toque`) → **Rename** → digite `ANTIGO_C01_titulo_toque`.
2. Se existir também `titulo`, faça o mesmo: `ANTIGO_C01_titulo`.
3. Clique com o botão direito na sequência anotada no passo 5 (ex.: `cartas_torcedor`) → **Rename** → digite `ANTIGO_C01_cartas`.

> Mudar o nome no painel Assets **não** muda o efeito: o objeto continua usando a mesma imagem. Os arquivos do C01 em `tiktok-efeitos\efeito-1-torcedometro\` também continuam intactos.

### 3.2 Importar o título

1. No painel **Assets**, clique em **+** (**Add**) → **Import** → **From Computer** (o mesmo caminho usado no C01).
2. Vá até `<A>` (`<BASE>\tiktok-efeitos\efeito-4-meu-proximo-carro\assets\`).
3. Selecione o título, conforme o que o C01 usou:
   - C01 com `titulo_toque` → selecione **`titulo_toque.png`**;
   - C01 com `titulo` (sem etiqueta) → selecione **`titulo.png`**;
   - C01 com as quadradas → use os mesmos nomes, mas dentro de `<A>\quadrado_512\`.
4. Clique em **Abrir**.
5. Renomeie o asset novo para **`carro_titulo`**.

### 3.3 Importar as 26 cartas (Texture Sequence)

1. No painel **Assets**, clique em **+** (**Add**) → **Import** → **Texture Sequence**.
2. Abra a pasta **`<A>\cartas\`** (ou `<A>\quadrado_512\cartas\`, se o C01 usou as quadradas).
3. Faça como no C01: se a janela pedir arquivos, **Ctrl+A** e **Abrir**; se pedir pasta, selecione a pasta `cartas` e confirme.
4. Confira se apareceu **uma** sequência nova e se ela tem **26 frames** no **Inspector**.
5. Renomeie a sequência nova para **`cartas_carro`**.
6. Confira a ordem: o primeiro quadro tem que ser **POPULAR 1.0 / COM 300 MIL KM** (etiqueta amarela, carro turquesa e o selo "300.000") e o último, **COM BARULHINHO / MISTERIOSO**. Se estiver fora de ordem, apague `cartas_carro` e importe de novo com **Ctrl+A**.

### 3.4 Compressão

1. Clique em `ANTIGO_C01_cartas` e veja a compressão no **Inspector**.
2. Ponha **a mesma** em `cartas_carro`. Se o C01 ficou em **Automatic** ou **Manual → 512 → High**, mantenha assim.
3. Faça o mesmo com `carro_titulo`, sempre em **High** (ou Automatic).

---

## Parte 4: Trocar as imagens

### 4.1 Título

1. Na **Hierarchy**, clique em **Title**.
2. No **Inspector**, componente **Image** → campo **Texture** → escolha **`carro_titulo`**. Também dá para arrastar do painel Assets para o campo.
3. Confira no **Preview** se aparece a etiqueta grafite "MEU PRÓXIMO / CARRO VAI SER…".

### 4.2 Cartas

1. Na **Hierarchy**, clique em **RandomAnimationSequence**.
2. Siga o caso que você anotou na Parte 2:
   - **Caso A:** componente **Animation Sequence** → campo da sequência → **`cartas_carro`**. Não mexa no **Texture** do **Image**, porque o Animation Sequence troca essa textura sozinho.
   - **Caso B:** componente **Image** → campo **Texture** → **`cartas_carro`**.
3. **Não mexa** no FPS nem no modo de reprodução (**Forward / Random / Shuffle**). Deixe como estavam no C01.
4. **Só no Caso S:** clique em `Controle` → componente **TorcedometroController** → campo **Sequencia Cartas** → **`cartas_carro`**. Os outros campos ficam como estão (Titulo = Title, Cartas = RandomAnimationSequence, Tempo Giro = 2, Tempo Some Titulo = 0.3, Girar De Novo No Toque = marcado). O nome do script continua "Torcedometro". Isso não aparece para ninguém e não precisa mudar.
5. **Só no Caso T:** abra o **Visual Scripting** e clique na caixa do randomizador. Se algum campo dela mostrar `ANTIGO_C01_cartas` ou `ANTIGO_C01_titulo_toque`, troque por `cartas_carro` ou `carro_titulo` (a confirmar na sua versão: o template pode não ter campo de imagem na caixa).
6. Aperte **Ctrl+S**, depois de conferir a barra de título.

---

## Parte 5: Apagar as imagens antigas

1. No painel **Assets**, clique com o botão direito em `ANTIGO_C01_cartas` → **Delete**.
2. Faça o mesmo com `ANTIGO_C01_titulo_toque` e, se existir, `ANTIGO_C01_titulo`.
3. **Se o programa avisar que o asset ainda está em uso, clique em Cancelar.** Algum lugar ainda aponta para a imagem antiga. Procure nesta ordem:
   1. **Title → Image → Texture**;
   2. **RandomAnimationSequence**: Animation Sequence e Image;
   3. `Controle` → **Sequencia Cartas** (Caso S);
   4. a caixa do randomizador no **Visual Scripting** (Caso T).
   Troque e tente apagar de novo.
4. Apague **só** o que começa com `ANTIGO_C01_`. Se aparecer outra imagem que você não reconhece, deixe como está e anote no relatório.
5. Aperte **Ctrl+S**.

> Se você quiser usar o `titulo.png` como reserva durante os testes, importe-o agora, renomeie para `carro_titulo_sem_toque` e apague antes do envio (Parte 9). Só importe se for usar.

---

## Parte 6: Proporção, posição e tamanho (só conferir)

O quadro do C02 é o mesmo do C01: **512×256**, e a peça ocupa praticamente o mesmo lugar dentro dele. A equipe mediu a área com desenho e deu 4 a 508 px na largura e 5 a 251 px na altura, contra 5 a 507 e 3 a 248 no C01. Por isso, **a posição e o tamanho do C01 devem servir sem mudança.**

1. Escolha no **Preview** o primeiro dos 3 rostos de exemplo.
2. Confira o título:
   - o **círculo amarelo do "?"** está redondo (se virou ovo, veja a Parte 15, linha "esticado");
   - o carro com capa e o "?" estão **inteiros na tela**, sem corte em cima;
   - a faixa de asfalto de baixo fica **logo acima do cabelo**, sem cobrir a testa nem os olhos.
3. Clique no Preview para sortear e espere a carta parar.
4. Confira a carta da mesma forma: **rodas redondas**, carro de cima inteiro, faixa de asfalto acima do cabelo.
5. Repita nos outros 2 rostos de exemplo.

**Só se algo não couber:** ajuste como na Parte 5.2 do guia do C01:
- mude **Scale** com **X e Y iguais** e **Position Y** no **RandomAnimationSequence**;
- copie o **2D Transform** (três pontinhos ⋮ → **Copy**) e cole no **Title** (⋮ → **Paste**);
- a largura da etiqueta fica em cerca de **1,6 vez a largura da cabeça** (entre 1,4 e 1,8).

Anote no relatório se mudou algo e os valores novos.

---

## Parte 7: A lógica (só conferir)

O C02 tem **26 cartas, igual ao C01**. Então a lógica não muda: nenhum campo de quantidade de quadros precisa ser alterado.

**Caso T (template):** no **Visual Scripting**, caixa do randomizador:

| Campo | Valor no C02 | Se estiver diferente |
|---|---|---|
| **TapToSpin** | **Ligado** | Ligue |
| **TimeToSpin** | **2** | Ponha `2` |
| **TitleFadeOutTime** | **0.3** | Ponha `0.3` |
| **TitleDelay** | o mesmo do C01 | Deixe como estava no C01 (se no C01 você precisou pôr `60`, mantenha) |
| Quantidade ou intervalo de quadros, se existir | **26** ou **0 a 25** | Ponha 26 ou 0–25 |
| Campos de objeto | **Title** e **RandomAnimationSequence** | Aponte para esses dois |

**Caso S (script):** confira os campos da Parte 4.2, passo 4.

Não crie nem apague nós. Se a lógica falhar nos testes, vá para a Parte 17.

Aperte **Ctrl+S**.

---

## Parte 8: Testar no PC

### 8.1 Como testar

Faça como no C01: escolha um rosto de exemplo **em vídeo**, se houver, e clique **dentro** da imagem do Preview para simular o toque.

### 8.2 Checklist (marque tudo antes de seguir)

- [ ] Ao abrir, aparece **só o título**, sem nenhuma carta por trás.
- [ ] O título **fica na tela até o clique**.
- [ ] A pílula **"👆 TOQUE NA TELA"** aparece inteira, sem corte, sobre a faixa de asfalto.
- [ ] O círculo amarelo do **"?"** e as **rodas** estão redondos (nada esticado).
- [ ] A peça está **inteira na tela**, inclusive o carro de cima, nos 3 rostos de exemplo.
- [ ] A faixa de asfalto fica **acima do cabelo**, sem cobrir os olhos.
- [ ] O título **acompanha a cabeça** quando o rosto se mexe.
- [ ] Ao clicar, o título **some** e as cartas **giram**.
- [ ] O giro dura **cerca de 2 s** e **para** numa carta.
- [ ] Nenhuma carta do **Torcedômetro** aparece no giro. Se aparecer qualquer ingresso com recortes nas laterais (roxo, laranja, dourado ou rosa), a troca da Parte 4.2 não pegou em algum lugar.
- [ ] Dá para **ler** a carta parada, inclusive as de letra menor: 09 (HERDADO DO VÔ / (ZERADINHO)), 21 (COM CÂMERA / DE RÉ (UFA)), 22 (COM TETO SOLAR / (É UM FURO)) e 26 (COM BARULHINHO / MISTERIOSO). Para conferir sem esperar o sorteio, abra a imagem em `<A>\cartas\` no visualizador do Windows ao lado do Preview e compare o tamanho do texto.
- [ ] O texto entre parênteses (amarelo) dá para ler nas etiquetas grafite, turquesa e coral.
- [ ] A carta continua **parada e presa na cabeça** quando o rosto se mexe.
- [ ] Não aparece **borda escura** nem quadrado em volta da etiqueta.
- [ ] Quando o rosto **sai** da imagem, a peça **some**.
- [ ] Clicar **de novo** depois do resultado faz o mesmo que no C01 (gira de novo ou nada). Anote.

### 8.3 Teste do sorteio

1. Faça **15 sorteios**, voltando ao título ou clicando de novo, como no C01.
2. Anote o texto de cada carta que saiu (use a tabela da 0.6).
3. Avalie:
   - **OK:** saíram **pelo menos 9 cartas diferentes** e **nenhuma saiu mais de 4 vezes**.
   - **Problema:** sempre as mesmas 2 ou 3, sempre a mesma, ou uma ordem fixa. Troque o modo da sequência para **Shuffle** (ou **Random**), como na Parte 7.3 do guia do C01, e repita. Se continuar, use o Plano C (Parte 17).

> Se o C01 passou neste teste, o C02 deve passar também: a lógica e a quantidade de cartas são as mesmas.

### 8.4 Salvar

Confira a barra de título e aperte **Ctrl+S**.

---

## Parte 9: Tamanho e desempenho

1. Se você importou `carro_titulo_sem_toque` e não usou, apague do painel **Assets**.
2. Na barra de cima, clique em **Click to update** no indicador de tamanho.
3. Anote o tamanho. O C01 deu **1,6 MB**. O C02 tem imagens um pouco mais pesadas, então o esperado é **perto de 2 MB** (estimativa, a confirmar na sua versão).
   - **Até 5 MB:** siga.
   - **Entre 5 e 8 MB:** sobrou alguma coisa do C01 ou do C08. Volte à Parte 5.
   - **Acima de 8 MB:** não dá para enviar. Apague o que sobrou e, se ainda passar, mude a compressão de `cartas_carro` para **Manual → 512 → Medium** e confira se o texto continua nítido.
4. Clique em **Test performance** → **Run test** e espere cerca de 30 s.
   - **Passou:** siga.
   - **Falhou:** clique em **View suggestions**, apague o que sobrou e teste de novo.
   - **Não rodou** (como aconteceu no C01): anote a mensagem e siga. O efeito é só 1 imagem e 1 sequência, sem IA e sem segmentação.

---

## Parte 10: Vídeo demo

O formulário 5.16 trata o demo como opcional, mas **mande sempre**. Só a revisão vê o vídeo. Regras: **9:16, MP4 ou MOV, até 15 s, até 32 MB**.

1. Grave como no C01 (Parte 9 do guia dele): aparelho 9:16 no Preview, rosto de exemplo em vídeo e **Screen record** (ou **Win+Shift+R**).
2. Siga o roteiro:

| Tempo | O que acontece |
|---|---|
| 0–2 s | Título parado sobre a cabeça, com "TOQUE NA TELA" |
| ≈ 2 s | Clique no Preview |
| 2–4,5 s | Título some e as cartas giram |
| 4,5–8 s | Resultado parado, com o rosto se mexendo um pouco |
| ≈ 8 s | Clique de novo, se o template girar de novo (se não girar, deixe o resultado até o fim) |
| 8–13 s | Segundo giro e segundo resultado |

3. Salve em `<BASE>\videos-demo\C02-demo-bruto.mp4`.
4. Confira em **Propriedades → Detalhes**: em pé, 9:16 (ex.: 1080×1920) e até 15 s.
5. Se não estiver em 9:16, rode:

```powershell
cd "$BASE\videos-demo"
ffmpeg -i C02-demo-bruto.mp4 -t 15 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" -c:v libx264 -pix_fmt yuv420p -an C02-demo.mp4
```

6. Se o bruto já estava em 9:16 e até 15 s, só renomeie para `C02-demo.mp4`.
7. Abra o `C02-demo.mp4` e confira se a peça continua inteira e se a carta final dá para ler.

---

## Parte 11: Conferências antes de enviar

### 11.1 Status do C01

1. Abra **Manage Effects** e veja o status do **Torcedômetro**.
   - **Active** ou **Under review:** siga.
   - **Needs revision por motivo técnico** (desempenho, tremor, tamanho): aplique a mesma correção no C02 antes de enviar. Avise a nuvem.
   - **Needs revision por conteúdo** (texto, carta, marca): não afeta o C02, que tem outras imagens. Siga, e corrija o C01 no projeto **dele**, não neste.

### 11.2 Nome

1. Em **Manage Effects**, confira se nenhum efeito da conta já se chama **Meu próximo carro**. Os nomes esperados lá são Eu no grupo da família, Torcedômetro e, se já tiver sido enviado, Perrengue no volante. (Meu 2027 vai ser só é enviado em 03/12.)
2. Veja no relatório se o formulário aceitou o acento em "Torcedômetro". Se não aceitou, use `Meu proximo carro` direto.

### 11.3 Conteúdo

1. Confira se nenhuma imagem do projeto tem marca, logo, placa, nome de loja, @ da conta, link ou chamada para comprar. As imagens da equipe já seguem essa regra. O risco é sobrar alguma do C01 ou do C08.
2. Confira se **não há som** ligado ao efeito.
3. Riscos conhecidos e aceitos pela equipe (não mude nada): o saquinho 💰 da carta 16 tem um "$" pequeno (símbolo genérico de moeda), e a bala da carta 08 é vermelha e branca. Se a revisão implicar, troque pela reserva (Parte 16).

### 11.4 Salvar e fazer backup

1. Confira a barra de título e aperte **Ctrl+S**.
2. Rode: `Copy-Item -Recurse -Force "$BASE\projetos\C02-meu-proximo-carro*" "$BASE\projetos\backup\"`

---

## Parte 12: Ícone e envio

### 12.1 Antes: a decisão do desafio

Pela ordem de 06/11 (05:50 UTC) do `PRONTO-PARA-MONTAR.md`, os sorteios **não podem ser enviados** até sair a decisão do Vini sobre o desafio **"Nov Social Randomizer Sub Challenge"**.

1. Abra o `PRONTO-PARA-MONTAR.md` mais novo (link da 0.2) e leia a seção **Atualizações**.
2. Decida:
   - **A decisão saiu e é entrar:** no envio, selecione o desafio no campo **Challenge** (12.3).
   - **A decisão saiu e é não entrar:** deixe **Challenge** vazio.
   - **Ainda não saiu:** monte, teste, grave o demo e **pare aqui**. Se chegar **segunda, 16/11** sem decisão, mande uma mensagem para a nuvem (`session_01XsQ8UziuLNch4tqqVVQfCw`) avisando que o C02 está pronto e esperando. **Nunca aceite os termos do desafio por conta própria.**

### 12.2 Ícone (Create icon)

Pela ordem da equipe, o ícone do formulário 5.16 sai do **Create icon**, com uma foto modelo, e não do `icone_162.png`.

1. Clique em **Create icon** na barra de cima (o mesmo caminho do C08 e do C01).
2. Escolha um modelo de rosto e espere o efeito aparecer nele.
3. **Ícone 1, o resultado:** clique para sortear até parar numa destas cartas, que têm frase curta e letra grande. Na ordem de preferência:
   1. **SÓ PEGA / NO TRANCO** (carta 05);
   2. **SUV EM 72 / PARCELAS** (carta 02);
   3. **EMPRESTADO / DO CUNHADO** (carta 15);
   4. **CARRINHO / DE MERCADO** (carta 23);
   5. **MOVIDO A / ESPERANÇA** (carta 18).
   Com 5 cartas boas em 26, devem bastar uns 5 cliques. Enquadre o rosto e a carta inteira, com a carta ocupando a maior parte do quadrado.
4. **Ícone 2, a pergunta:** se der para ter 2 ícones, faça o segundo com o **título** ("MEU PRÓXIMO / CARRO VAI SER…" com o "?"), voltando ao começo do efeito.
5. Confira na prévia pequena se o texto do ícone 1 dá para ler. Se não der, tente outra carta da lista.
6. Clique em **Done** (ou **Submit**, conforme a versão).

**Plano de exceção:** se o Create icon não funcionar e o formulário tiver um botão de **Upload** de PNG, use `<A>\icone_162.png` e, como 2º, `<A>\icone_alt_162.png`. Anote no relatório.

### 12.3 O formulário

1. Clique em **Submit**, no canto de cima à direita.
2. **Atenção, o passo mais importante do envio.** O formulário pode oferecer três caminhos:
   - **Submit a new effect** (enviar um efeito novo): **é este.**
   - **Update an existing effect**: aparece quando a conta tem efeitos **Active**. **Não use.** Ele trocaria o Torcedômetro ou o Eu no grupo da família pelo C02.
   - **Replace an existing effect**: aparece com efeitos em **Draft** ou **Needs revision**. **Não use**, pelo mesmo motivo.

   Como este projeto é uma cópia do C01, o formulário pode já vir com o nome **Torcedômetro** ou com o ícone do C01. **Se isso acontecer, pare**: volte e escolha **Submit a new effect**. Se a tela não oferecer essa opção, não envie: avise a nuvem com um print.

   > O C01 foi feito a partir do projeto do C08, e os dois entraram como efeitos separados. Então o caminho de "efeito novo" funciona nesta conta. Mesmo assim, confira sempre.

3. Preencha:

| Campo | O que colocar |
|---|---|
| **Effect name** | `Meu próximo carro` (17 caracteres; limite 25). Sem reticências, sem "AI" (não usa IA generativa). Se recusar o acento: `Meu proximo carro`. Se recusar por nome repetido: `Qual carro eu vou ter` (21); se recusar de novo: `Roleta do meu carro` (19). |
| **Effect icon** | Os ícones do Create icon (12.2): 1º o resultado, 2º o título |
| **Hint** (lista) | A opção de **tocar na tela**. Se houver opção em português, use ela (ex.: "Toque na tela"). Se a lista for só em inglês, a mesma que você usou no C01 (provavelmente "Tap the screen" ou parecido). |
| **Sound** (som) | **Nenhum.** Não ligue som. |
| **Challenge** | Conforme a 12.1. Sem decisão escrita, **não envie**. |
| **Trend** | Deixe **vazio**, a não ser que o `PRONTO-PARA-MONTAR.md` mande outra coisa. Anote no relatório as opções que apareceram (a confirmar na sua versão: o que o campo faz). |
| **Demo video** | `<BASE>\videos-demo\C02-demo.mp4` |

**Se aparecer algum campo que não está na tabela** (a versão pode ter mudado):

| Campo | O que colocar |
|---|---|
| **Description** (descrição) | `Sorteio sobre a cabeça. A pessoa toca na tela e descobre como vai ser o seu próximo carro: popular 1.0 com 300 mil km, SUV em 72 parcelas, esse mesmo só que lavado e mais 23 resultados. Os desenhos de carro são genéricos, sem marca, modelo ou placa.` Se o campo for pequeno: `Toque na tela e descubra como vai ser o seu próximo carro.` |
| **Category** | A mais próxima de **Funny**; senão, **Randomizer**; senão, **Interactive** |
| **Tags** | `carro`, `sorteio`, `humor`, `roleta`, `motorista`. Se tiver que ser em inglês: `car`, `randomizer`, `funny`, `roulette`, `driver` |
| **Comentários para a revisão** ("Notes", "Additional comments") | O texto em inglês e, embaixo, o em português, que estão logo abaixo desta tabela |
| Qualquer outro | Deixe o padrão e anote |

**Texto para comentários** (só se o campo existir):

> Head randomizer. Tap the screen to find out what your next car will be, such as "1.0 economy car with 300,000 km", "SUV in 72 installments" or "this same one, but washed". 26 original light-humor texts in Brazilian Portuguese, with simple generic car drawings. No brands, logos, car models, license plates, speed or racing, and no real people. No generative AI.
>
> Sorteio sobre a cabeça. A pessoa toca na tela e descobre como vai ser o seu próximo carro: popular 1.0 com 300 mil km, SUV em 72 parcelas, esse mesmo só que lavado e mais 23 resultados. Os desenhos de carro são genéricos, sem marca, modelo ou placa.

### 12.4 Enviar

1. Revise o nome: "Meu próximo carro", com acento no "ó", "M" maiúsculo e o resto em minúsculas, sem espaço sobrando.
2. Confira de novo se está no caminho **Submit a new effect**.
3. Clique em **Submit**.
4. Tire um print da confirmação e salve em `<BASE>\prints\C02-enviado.png`.
5. Mande para a nuvem: nome enviado, data e hora, status, tamanho do pacote, caso (A/B, T/S) e se entrou no desafio.

---

## Parte 13: Acompanhar o status

1. Abra **Manage Effects**.
2. **Confira se aparecem os dois, separados: "Torcedômetro" e "Meu próximo carro".** Se o Torcedômetro sumiu ou mudou de nome, o envio caiu em "Update" ou "Replace". Avise a nuvem na hora, com print, e não faça mais nada nesses dois efeitos.
3. Leia o status do C02:

| Status | O que fazer |
|---|---|
| **Draft** | Clique em **Finish submission** e termine. |
| **Under review** | Esperar (1 a 3 dias úteis). Conferir 1 vez por dia. |
| **Needs revision** | Leia o motivo, corrija (Partes 15 e 16) e reenvie **por este projeto**, com **Replace an existing effect** apontando para **Meu próximo carro** (a confirmar na sua versão: o nome da opção). É o único caso em que "Replace" é usado, e só no próprio C02. |
| **Active** | Anote a data e pegue o link (Manage Effects → menu ⋯ do efeito → **Share**). Mande para a nuvem: ele entra na gravação do Vini de dom 22/11. |
| **Deactivated** | Leia o motivo e avise a nuvem. |

---

## Parte 14: Resumo de 1 tela (para quem já fez o C01)

1. Backup do C01 → abrir o C01 → **Save As `C02-meu-proximo-carro`** → conferir a barra de título.
2. Assets: renomear os antigos para `ANTIGO_C01_…`.
3. Importar `<A>\titulo_toque.png` (→ `carro_titulo`) e a sequência `<A>\cartas\` (→ `cartas_carro`, 26 frames).
4. Title → Texture = `carro_titulo`. RandomAnimationSequence → sequência = `cartas_carro` (Caso A no Animation Sequence, Caso B no Image, Caso S também no script).
5. Apagar os `ANTIGO_C01_…`. Se der "em uso", achar a referência.
6. Conferir posição, lógica (TapToSpin ligado, 2, 0.3) e checklist; fazer 15 sorteios.
7. Tamanho, Test performance, demo `C02-demo.mp4`.
8. Decisão do desafio → **Create icon** → **Submit a new effect** → nome `Meu próximo carro`, hint de toque, sem som, trend vazio.
9. Manage Effects: os dois efeitos aparecem separados.

---

## Parte 15: Problemas comuns e soluções

| Problema | Causa provável | Solução |
|---|---|---|
| A barra de título ainda diz C01 | O Save As não foi feito ou não pegou | **Não salve.** Feche sem salvar, reabra o C01 e faça a Parte 1.2 de novo. Se já salvou por cima, restaure de `projetos\backup\`. |
| Não acho o projeto do C01 | Nome diferente ou outra pasta | Veja o `relatorio-montagem.md` e o `reconhecimento.md`. Se não existir, use o Plano B1 (Parte 17). |
| Os assets novos vieram com "1" ou "(2)" no nome | Os antigos não foram renomeados antes | Siga mesmo assim: identifique os novos pela miniatura (etiqueta grafite com "?" e cartas com faixa de asfalto) e renomeie para `carro_titulo` e `cartas_carro`. |
| No giro aparece um ingresso do C01 (com recortes nas laterais) | A sequência antiga continua ligada em algum lugar | Parte 4.2: confira Animation Sequence, Image, o script (Caso S) e a caixa do randomizador. |
| "Asset em uso" ao apagar o antigo | Idem | Parte 5, passo 3. |
| A sequência veio com menos de 26 quadros ou fora de ordem | Seleção incompleta | Apague `cartas_carro` e importe de novo com **Ctrl+A**. |
| Esticado (o "?" ou as rodas viraram ovo) | Size ou Stretch Mode diferente do C01, ou mistura de versão quadrada com 2:1 | Confira se o título e as cartas são da **mesma** versão do C01 (512×256 ou `quadrado_512`). Depois, Parte 5.1 do guia do C01. |
| O carro de cima sai cortado no topo da tela | Peça alta demais para aquele rosto | Baixe um pouco o **Position Y** dos dois objetos (copie o 2D Transform de um para o outro) ou reduza a **Scale** em 5% (X e Y juntos). |
| Texto difícil de ler | Compressão baixa ou peça pequena | Compressão **High** e, se preciso, Scale +10% (X e Y juntos), conferindo se tudo cabe. |
| Clicar não gira | TapToSpin desligado ou clique fora da imagem | Parte 7. Clique **dentro** do Preview. |
| O título some sozinho antes do toque | Igual ao C01 | Use a mesma solução que você usou no C01 (TitleDelay, título sem etiqueta ou Plano C). |
| Sai sempre a mesma carta | Modo de reprodução | Parte 8.3: **Shuffle** ou **Random**. Se não resolver, Plano C. |
| Pacote acima de 8 MB | Sobrou coisa do C01 ou do C08 | Parte 9. |
| O formulário veio com "Torcedômetro" preenchido | Caiu em Update ou Replace | Parte 12.3, passo 2: volte e escolha **Submit a new effect**. |
| O formulário recusa o nome | Acento ou nome repetido | `Meu proximo carro` → `Qual carro eu vou ter` → `Roleta do meu carro`. |
| O formulário recusa o vídeo | Formato, duração ou tamanho | Parte 10, passo 5 (ffmpeg). |
| **Needs revision** por marca, modelo ou placa | O revisor viu semelhança com um carro real | Avise a nuvem com o print do motivo e o número da carta. A equipe redesenha. Enquanto isso, se for uma carta só, troque pela reserva (Parte 16). |
| **Needs revision** por "duplicado" ou "parecido com outro efeito" | Mesmo template do C01 | Avise a nuvem com o print. **Não** reenvie sem ordem: a equipe decide se muda o visual. |
| **Needs revision** por uma carta | Carta vetada | Parte 16. |
| **Needs revision** por desempenho ou tremor | QA técnico | Test performance, teste com movimento, Parte 9. |
| Pediu login de novo ou está em outra conta | Login expirou | Seção 0.7, com o link. |

---

## Parte 16: Trocar uma carta vetada pela reserva

**A troca é sempre pelo arquivo.** Não adianta mudar só o texto no `textos.json`: o desenho de cada carta está preso ao número dela no `gerar.py`, e a carta nova sairia com o desenho antigo.

| Se vetarem… | Use | Texto da reserva |
|---|---|---|
| carta 08 (CARRO DE APP / COM BALINHA) | `reserva_01.png` (R1) | COM VIDRO DE / MANIVELA |
| carta 11 (CAMINHONETE / DO AGRO) | `reserva_02.png` (R2) | TANQUE SEMPRE / NA RESERVA |
| carta 20 (CONSÓRCIO QUE / NUNCA SAI) | `reserva_03.png` (R3) | ELÉTRICO / (SEM TOMADA) |
| qualquer outra (ex.: 16, pelo "$") | `reserva_04.png` (R4) e depois as que sobrarem | CHOVE DENTRO / MAIS QUE FORA |

Exemplo com a carta 08 (troque os números para o seu caso):

```powershell
$A = "$BASE\tiktok-efeitos\efeito-4-meu-proximo-carro\assets"
New-Item -ItemType Directory -Force "$A\cartas_trocadas" | Out-Null
Move-Item "$A\cartas\carta_08.png" "$A\cartas_trocadas\carta_08.png"
Copy-Item "$A\reservas\reserva_01.png" "$A\cartas\carta_08.png"
(Get-ChildItem "$A\cartas\*").Count    # tem que continuar 26
```

Se o projeto usa as quadradas, faça o mesmo dentro de `$A\quadrado_512\` (`cartas` e `reservas`).

No Effect House:
1. Apague `cartas_carro` do painel **Assets**.
2. Importe a pasta `cartas` de novo (Parte 3.3) e renomeie para `cartas_carro`.
3. Ligue a sequência de novo (Parte 4.2, inclusive no script, se for Caso S).
4. Teste (Parte 8) e reenvie com **Replace an existing effect** → **Meu próximo carro** (a confirmar na sua versão: o nome da opção).
5. Avise a nuvem qual carta foi trocada, para atualizar o `textos.json`.

> A reserva pode ficar com a mesma cor de etiqueta da carta vizinha. É só estética, pode ignorar.

---

## Parte 17: Planos B e C (se a cópia do C01 não der certo)

| Plano | Quando usar | Esforço |
|---|---|---|
| **B1: template do zero** | O projeto do C01 não existe, não abre ou ficou estragado | médio (≈ 3 h) |
| **B2: preset de Interactions** | Não há template, mas o preset existe | baixo a médio |
| **B3: Visual Scripting nó a nó** | Não há template nem preset | médio |
| **C: script TypeScript** | A lógica do template falha (título some, sorteio viciado, não gira) | baixo |
| **Effect House AI** | Travou em qualquer passo | baixo. Pedidos prontos em `script\prompt-effect-house-ai.md` |

### Plano B1: template Randomizer 2D do zero

Siga as **Partes 1 a 9 do guia do C01** (`efeito-1-torcedometro\guia-montagem.md`), trocando:

| No guia do C01 | No C02 |
|---|---|
| pasta `efeito-1-torcedometro\assets\` | `efeito-4-meu-proximo-carro\assets\` |
| projeto `C01-torcedometro` | `C02-meu-proximo-carro` |
| sequência `cartas_torcedor` | `cartas_carro` |
| "QUE TORCEDOR / VOCÊ É?" | "MEU PRÓXIMO / CARRO VAI SER…" |
| régua: medalha redonda | régua: círculo do "?" (título) e rodas (cartas) |
| cartas de leitura difícil 17, 18, 22 | 09, 21, 22, 26 |
| demo `C01-demo.mp4` | `C02-demo.mp4` |

Os valores são os mesmos: **TapToSpin ligado, TimeToSpin 2, TitleFadeOutTime 0.3, 26 quadros**, largura de cerca de 1,6 cabeça. Depois, volte para as Partes 11 a 13 **deste** guia, porque o envio do 5.16 é diferente do guia do C01.

### Plano B2: preset de Interactions (sem ligar fios)

O preset oficial **"Tap Screen to Play Animation Sequence Then Delay Pause"** toca a sequência ao tocar na tela e pausa depois de N segundos. Com o modo **Random** ou **Shuffle**, ela para numa carta qualquer. Exige o componente **Animation Sequence** no objeto.

1. Num projeto vazio (**New Project**/**Blank**; a confirmar na sua versão), crie dois **Face Sticker** (**Hierarchy → + → Face Effects → Face Sticker**) e renomeie para `Titulo` e `Cartas`.
2. `Titulo`: **Image → Texture** = `carro_titulo`.
3. `Cartas`: **Add Component → Animation Sequence**, com a sequência `cartas_carro` e o modo **Shuffle** (ou **Random**). Desmarque o **autoplay**, se existir (a confirmar na sua versão).
4. Acerte proporção (2:1), posição e tamanho dos dois, iguais (Parte 5 do guia do C01).
5. Com `Cartas` selecionado, clique em **+ Add interaction** (no Inspector ou no Visual Scripting; a confirmar na sua versão) e escolha **Tap Screen to Play Animation Sequence Then Delay Pause**. Em **Target**, `Cartas`. Em **Delay Pause Seconds**, `2`.
6. Para o título sumir e as cartas aparecerem no toque, adicione o preset **Tap Screen to Delay Show/Hide Object** duas vezes (a confirmar na sua versão: nome exato):
   - Target `Titulo`, ação **Hide**, atraso `0`;
   - Target `Cartas`, ação **Show**, atraso `0`.
7. Deixe `Cartas` **invisível no começo**: desmarque a caixinha do objeto na Hierarchy ou ligue **Start → Set Visibility** (Target `Cartas`, desligado).

**Limite:** este plano não volta ao título quando a pessoa aperta gravar. Se der, ligue o evento de início de gravação (**Video Record Start** ou **Record Start**; a confirmar na sua versão) em dois **Set Visibility**: `Titulo` ligado e `Cartas` desligado. Se não der, envie assim mesmo e anote: a pessoa toca de novo durante a gravação e o giro acontece no vídeo.

### Plano B3: Visual Scripting nó a nó

Mesmos objetos do B2 (passos 1 a 4, mas **sem** o modo Shuffle/autoplay se você for usar o nó de controle). Crie duas **variáveis** no painel de variáveis do Visual Scripting (a confirmar na sua versão: onde ficam):
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
- **Se não é:** siga a Parte 15, Plano C, do guia do C01, passos 1 a 19, com estas trocas: projeto `C02-meu-proximo-carro-script`; no campo **Sequencia Cartas**, `cartas_carro`.
- O script **ainda não foi rodado** dentro do Effect House pela equipe. Se der erro, use o **Pedido 4** de `script\prompt-effect-house-ai.md` (desta pasta).

### Effect House AI

Veja no `reconhecimento.md` (item 3) se o assistente funcionou nesta conta. Os pedidos prontos, em inglês, estão em `efeito-4-meu-proximo-carro\script\prompt-effect-house-ai.md`:

| Pedido | Quando |
|---|---|
| 1 | A troca de imagens na cópia do C01 travou (Partes 3 a 5) |
| 2 | Precisa configurar o template Randomizer 2D do zero (Plano B1) |
| 3 | Não há template: montar tudo do zero (Planos B2 e B3) |
| 4 | O script do Plano C deu erro |

Use o assistente para **destravar** um passo, sem mudar a ideia, os textos ou as imagens. Depois, refaça os checklists da Parte 8.

---

## Parte 18: O que anotar no relatório

Em `<BASE>\relatorio-montagem.md`, na seção do C02:

- Nome real do projeto do C01 usado como base e se o backup foi feito.
- Caso A ou B, Caso T ou S, versão 512×256 ou quadrada, título com ou sem etiqueta.
- Se mudou posição ou escala, com os valores antigos e os novos.
- Valores da lógica conferidos (TapToSpin, TimeToSpin, TitleDelay, TitleFadeOutTime).
- Resultado do teste de sorteio: quantas cartas diferentes e a que mais repetiu.
- Tamanho do pacote e resultado do Test performance (ou a mensagem, se não rodou).
- Plano usado: cópia do C01, B1, B2, B3 ou C.
- Cartas usadas nos ícones do Create icon.
- Caminho escolhido no Submit (tem que ser **Submit a new effect**), nome enviado, hint escolhido, se entrou no desafio, opções do campo **Trend**.
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
- Nós e limites técnicos: `tiktok-efeitos/pesquisa/03-tecnico-effect-house.md`.

Da própria equipe:
- Formulário do Effect House 5.16 (nome, ícone pelo Create icon, hint de lista, som, challenge, trend e demo) e a ordem de esperar a decisão do desafio: `PRONTO-PARA-MONTAR.md`, atualizações de 06/11.
- C08 e C01 enviados como efeitos separados, C01 com 26 cartas e 1,6 MB: `STATUS.md`.
- Medidas das imagens (área com desenho, pesos): conferidas pela equipe nos arquivos de `assets/` em 06/11/2026.
