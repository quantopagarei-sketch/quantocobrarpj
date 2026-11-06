# Guia de montagem: "Simpatia da Virada" (C07)

**Para quem é:** para o Montador, o Claude que opera o PC do Vini. Também serve para qualquer pessoa que já tenha montado o Torcedômetro (C01).
**Versão do guia:** 1.1 · 06/11/2026 (revisada pelo QA) · escrito para o Effect House **5.16** no Windows, a versão que o Montador encontrou no PC.
**Envio:** **somente na quinta, 03/12/2026**, no mesmo dia do C05 (Meu 2027 vai ser). **Nunca antes.** Montar e testar pode (e deve) ser feito assim que o C07 for liberado.
**Tempo total:** cerca de **2 h** para montar, reaproveitando o projeto do C01, e mais **30 min** no dia 03/12 para conferir e enviar. Se for preciso montar do zero (Parte 18), reserve 4 h.

> **Vini, se você estiver lendo:** não precisa fazer nada aqui. Você só será chamado nos casos da seção 0.8, sempre com o link direto.

### Como ler as marcas

- **(a confirmar na sua versão)**: a equipe não conseguiu ver essa tela, porque o site do Effect House não abre de onde pesquisamos. Se o botão ou o campo tiver outro nome, use o parecido e **anote no relatório** o nome real.
- Os nomes de botões e painéis estão **em inglês e em negrito**, como aparecem no programa.
- "Clique" é com o botão esquerdo. Quando for o direito, o passo diz "clique com o botão direito".
- **Você já montou o C08 e o C01** (e, até lá, provavelmente o C02 e o C06). Quando este guia diz "faça como no C01", vale o que você fez de verdade e anotou no `relatorio-montagem.md`, mesmo que seja diferente do guia do C01.

### O que vamos montar (resumo)

1. Sobre a cabeça aparece um **bilhete de desejo roxo**, com borda dourada, pontas dobradas e um **selo dourado ondulado com um cacho de uva** em cima. O texto é **"MINHA SIMPATIA / PRA 2027 É…"**, e embaixo vem a pílula dourada **"👆 TOQUE NA TELA"**.
2. A pessoa toca na tela. O título some e as cartas giram por cerca de 2 segundos.
3. O giro para numa das **26 simpatias**, por exemplo **"PULAR 7 ONDAS / (VALE NO BALDE)"** ou **"MOEDA NO SAPATO / (A NOITE TODA)"**. A carta fica presa na cabeça. A graça é a pessoa cumprir a simpatia no vídeo.
4. Quando a pessoa aperta **gravar** no TikTok, o efeito volta para o título.

**É o mesmo efeito do Torcedômetro, com outras imagens.** Usa o mesmo template (Randomizer 2D), o mesmo quadro de imagem (512×256) e as mesmas **26 cartas**, e a lógica é igual. O bilhete ocupa **exatamente** a mesma área do ingresso do C01 dentro do quadro. Por isso o caminho principal deste guia é **copiar o projeto do C01 já pronto e trocar só o título, as cartas e o ícone**. A lógica, a posição e o tamanho continuam os do C01, que já foram testados e enviados. O efeito é para **1 pessoa** (1 rosto).

---

## Parte 0: Antes de começar

### 0.1 Pré-requisitos (confira todos)

| # | Pré-requisito | Como conferir |
|---|---|---|
| 1 | O C07 está liberado na tabela da seção 2 do `PRONTO-PARA-MONTAR.md` | Abra https://raw.githubusercontent.com/quantopagarei-sketch/quantocobrarpj/main/tiktok-efeitos/PRONTO-PARA-MONTAR.md. Se o C07 ainda estiver só em "Vem aí", **não comece**. |
| 2 | O projeto do C01 existe, abre e passou nos testes | No `relatorio-montagem.md`, seção do C01: nome do projeto, Caso A/B, plano usado (template ou script) e título usado |
| 3 | O Effect House está logado na conta **Car Shop** | Tela inicial, como no C01 |
| 4 | Você já sabe como o seu Effect House importa uma Texture Sequence (arquivos ou pasta) e como funciona o **Create icon** | Você fez isso no C08 e no C01. Anotações no relatório |
| 5 | O ffmpeg está instalado | `ffmpeg -version` no PowerShell. Se não estiver: `winget install --id Gyan.FFmpeg -e` e abra outro PowerShell. |

### 0.2 Quando enviar (leia antes de tudo)

Este efeito é de **Réveillon**. A data foi escolhida para a aprovação sair por volta de 07 ou 08/12, o Vini gravar o C05 e o C07 juntos no sábado 12/12 e a janela de 30 dias do programa de recompensas cobrir o pico de uso, de 26/12 a 01/01.

| Situação | O que fazer |
|---|---|
| Antes de 03/12 | **Montar, testar, gravar o demo e parar** (Parte 11). **Não clique em Submit**, nem para "ver como fica". |
| Quinta, 03/12/2026 | Enviar (Partes 12 e 13), no mesmo dia do C05. **Não espere** a admissão no programa de recompensas: vale a **situação B**, igual ao C05. |
| Você não conseguiu enviar em 03/12 (PC desligado, limite de uso, login caído) | Envie no **primeiro dia possível depois**, sem esperar ordem nova, e avise a nuvem. O limite da equipe é o efeito **aprovado até sexta, 18/12**. |
| O `PRONTO-PARA-MONTAR.md` mandar outra data para o C07 | **Vale o arquivo**, não este guia. |

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
| Guia do C05 (enviado no mesmo dia) | `tiktok-efeitos\efeito-3-meu-2027-vai-ser\guia-montagem.md` | Montador, em 03/12 |

### 0.4 Pastas (vale para o guia inteiro)

Neste guia, **`<BASE>`** é a pasta "Efeitos" que você usa no PC. Pela última ordem da equipe, ela é `C:\Users\Pichau\Desktop\Efeitos`. Se essa pasta não existir, a pasta é `Documentos\Efeitos`.

| Apelido | Caminho |
|---|---|
| `<BASE>` | `C:\Users\Pichau\Desktop\Efeitos` (ou `Documentos\Efeitos`) |
| `<A>` (imagens do C07) | `<BASE>\tiktok-efeitos\efeito-7-simpatia-da-virada\assets` |
| Projeto novo | `<BASE>\projetos\C07-simpatia-da-virada` |
| Vídeo demo | `<BASE>\videos-demo\C07-demo.mp4` |
| Prints | `<BASE>\prints\C07-*.png` |
| Conferência dos arquivos (Parte 0.5 e 12.3) | `<BASE>\C07-conferencia-arquivos.csv` |
| Relatório | `<BASE>\relatorio-montagem.md`, nova seção "C07" |

### 0.5 Baixar e conferir os arquivos

1. Baixe o zip (link da 0.3) e extraia **só a pasta `tiktok-efeitos`** em `<BASE>`, por cima da antiga.
2. Rode no PowerShell:

```powershell
$BASE = if (Test-Path "C:\Users\Pichau\Desktop\Efeitos") { "C:\Users\Pichau\Desktop\Efeitos" } else { Join-Path ([Environment]::GetFolderPath('MyDocuments')) "Efeitos" }
$A = "$BASE\tiktok-efeitos\efeito-7-simpatia-da-virada\assets"
(Get-ChildItem "$A\cartas\carta_*.png").Count            # tem que dar 26
(Get-ChildItem "$A\cartas\*").Count                      # tem que dar 26 (a pasta só pode ter as cartas)
(Get-ChildItem "$A\reservas\reserva_*.png").Count        # tem que dar 4
Get-ChildItem "$A\titulo_toque.png","$A\titulo.png","$A\icone_162.png","$A\icone_alt_162.png" | Select Name, Length
(Get-ChildItem "$A\cartas\*.png" | Measure-Object Length -Maximum).Maximum   # tem que ser menor que 1048576 (1 MB); o esperado é ~110000 (carta_06)
Get-ChildItem "$BASE\projetos" | Select Name, LastWriteTime                # ache aqui o projeto do C01
```

> **Em todo PowerShell novo**, rode antes as duas primeiras linhas acima (as que definem `$BASE` e `$A`). Os comandos das outras partes dependem delas.

3. Se faltar arquivo, baixe o zip de novo. Se continuar faltando, avise a nuvem. Não chame o Vini por isso.
4. **Guarde a "impressão digital" das imagens que você vai montar.** Entre a montagem e o envio passam semanas, e a equipe pode retocar alguma carta nesse tempo. No dia 03/12 (Parte 12.3), este arquivo mostra se algo mudou:

```powershell
Get-ChildItem "$A\titulo_toque.png","$A\titulo.png","$A\cartas\*.png","$A\quadrado_512\titulo_toque.png","$A\quadrado_512\titulo.png","$A\quadrado_512\cartas\*.png" | Get-FileHash -Algorithm SHA256 | Select-Object @{n='Arquivo';e={$_.Path.Substring($A.Length + 1)}}, Hash | Export-Csv "$BASE\C07-conferencia-arquivos.csv" -NoTypeInformation -Encoding UTF8
(Import-Csv "$BASE\C07-conferencia-arquivos.csv").Count   # tem que dar 56 (2 títulos + 26 cartas, nas duas versões)
```

### 0.6 O que entra no efeito e o que não entra

Todos os arquivos ficam dentro de `<A>` (a pasta `assets` do efeito 7).

| Arquivo | Entra? | Para quê |
|---|---|---|
| `titulo_toque.png` (512×256, fundo transparente) | **Sim (padrão)** | Título "MINHA SIMPATIA / PRA 2027 É…" com a pílula dourada "👆 TOQUE NA TELA". Vai no objeto **Title**. |
| `titulo.png` (512×256) | Só se o C01 usou o título sem etiqueta | O mesmo título, sem a pílula e com letra um pouco maior (Parte 3, passo 3). |
| `cartas\carta_01.png` … `carta_26.png` (512×256 cada) | **Sim** | Os 26 resultados. Entram juntos como **uma** Texture Sequence, na ordem 01→26. |
| `reservas\reserva_01.png` … `reserva_04.png` | Não | Só se uma carta for vetada (Parte 17) |
| `quadrado_512\` (as mesmas imagens em 512×512) | Só se o C01 usou as quadradas | Título e cartas têm que seguir o C01: as duas 512×256 ou as duas quadradas |
| `icone_162.png`, `icone_alt_162.png` | Só no plano de exceção da Parte 13.3 | Pela ordem de 06/11, o ícone sai do **Create icon** |
| `icone_512.png`, `icone_alt_512.png`, `previa.png`, `gerar.py`, `lista-de-arquivos.txt`, `LEIA-ME.md` | Não | Referência da equipe |

**Peso:** `titulo_toque.png` + 26 cartas = **2,62 MB** em PNG (no C01, as mesmas peças tinham 2,15 MB e viraram um pacote de 1,6 MB). O maior arquivo é a `carta_06.png`, com 107 KB.

**Régua contra imagem esticada:** no alto de cada peça há um **selo dourado ondulado** (no título, com o cacho de uva; nas cartas, com o desenho da simpatia). Ele tem que ficar **redondo**. Se virar ovo, a imagem está esticada.

**Como reconhecer as cartas do C07 no giro:** bilhete com borda dourada e **pontas dobradas** (canto de cima à esquerda e de baixo à direita), confete e fogos pequenos nos cantos de cima. O fundo alterna em **3 tons**: roxo-uva, ameixa (vinho-arroxeado) e anil (azul-arroxeado). O trecho entre parênteses sai em **dourado**. O ingresso do C01 é **laranja ou violeta, com recortes redondos nas laterais**: se ele aparecer, a troca não pegou.

### 0.7 Ordem das cartas (quadro = posição na sequência)

O quadro 0 é a carta 01. Use a tabela para conferir a ordem (Parte 3.3) e para anotar o teste de sorteio (Parte 8.3). A coluna "px" é o tamanho da letra: quanto menor, mais importante conferir a leitura.

| Quadro | Arquivo | Texto | px | Quadro | Arquivo | Texto | px |
|---:|---|---|---:|---:|---|---|---:|
| 0 | carta_01 | PULAR 7 ONDAS / (VALE NO BALDE) | 48 | 13 | carta_14 | VARRER O AZAR / PRA FORA | 52 |
| 1 | carta_02 | NÃO MANDAR / OI PRO EX | 54 | 14 | carta_15 | FRANGO NÃO / (CISCA PRA TRÁS) | 45 |
| 2 | carta_03 | LENTILHA PRO / DINHEIRO VIR | 54 | 15 | carta_16 | ALGO VERMELHO / PRO CRUSH NOTAR | 44 |
| 3 | carta_04 | SUBIR NA VIDA / (E NA CADEIRA) | 53 | 16 | carta_17 | 12 DESEJOS / NUM PAPELZINHO | 46 |
| 4 | carta_05 | TUDO BRANCO / (ATÉ A MEIA) | 54 | 17 | carta_18 | CARRO LIMPINHO / PRA VIRADA | 48 |
| 5 | carta_06 | MADRUGAR NO / DIA 1º (DUVIDO) | 54 | 18 | carta_19 | ENTRAR COM O / PÉ DIREITO | 54 |
| 6 | carta_07 | COMER 12 UVAS / (SEM PRESSA) | 52 | 19 | carta_20 | VIRAR O ANO / SEM CELULAR | 54 |
| 7 | carta_08 | VOLTA NA RUA / COM MALA VAZIA | 46 | 20 | carta_21 | MOEDA NO SAPATO / (A NOITE TODA) | 43 |
| 8 | carta_09 | ROMÃ NA / CARTEIRA VAZIA | 49 | 21 | carta_22 | COMER ARROZ / COM UVA-PASSA | 48 |
| 9 | carta_10 | ABRAÇAR ATÉ / O TIO DO PAVÊ | 54 | 22 | carta_23 | ABRIR A PORTA / PRO ANO ENTRAR | 47 |
| 10 | carta_11 | 3 PULINHOS / À MEIA-NOITE | 54 | 23 | carta_24 | ROUPA NOVA / (SEM ETIQUETA) | 51 |
| 11 | carta_12 | ROUPA ÍNTIMA / AMARELA (PSIU) | 50 | 24 | carta_25 | LIGAR PRA VÓ / NA VIRADA | 54 |
| 12 | carta_13 | PAGAR UM / BOLETO (O MENOR) | 43 | 25 | carta_26 | PEDIDO NA HORA / DOS FOGOS | 48 |

### 0.8 O que depende do Vini (o mínimo)

Nada, se tudo correr bem. Ele só é chamado se:

1. **O login do Effect House cair** ou se o programa estiver em outra conta. Mande para ele:
   > Abra o Effect House no computador. Vai aparecer um QR code. No celular, abra o **TikTok da conta Car Shop** → **Perfil** → ícone de pessoa (**Adicionar amigos**) → ícone de scanner no canto de cima → aponte para o QR → toque em **Confirmar**. Guia com imagens: https://effecthouse.tiktok.com/learn/guides/getting-started/introduction-to-effect-house/download-and-login
   >
   > Tem que ser o scanner **de dentro do TikTok**. A câmera comum do celular não funciona.
2. **A decisão sobre o desafio** ("Nov Social Randomizer Sub Challenge" ou outro que aparecer) ainda não tiver saído em 03/12. Quem pergunta é a nuvem, não você (Parte 13.2).

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
| Partes 12 e 13: conferências do dia, ícone e envio | **qui 03/12** | 30 min |
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

### 1.2 Abrir o C01 e salvar como C07

1. Abra o **Effect House**.
2. Confira a conta **Car Shop**, como no C01. Se for outra conta, **pare** e siga a seção 0.8.
3. Abra o projeto do C01 (lista de projetos recentes da tela inicial, ou **File → Open**; a confirmar na sua versão).
4. **Antes de mexer em qualquer coisa**, clique em **File → Save As**.
5. Vá até `<BASE>\projetos\`.
6. Dê o nome **`C07-simpatia-da-virada`**.
7. Clique em **Salvar**.
8. Confira na **barra de título** da janela se aparece `C07-simpatia-da-virada`. **Só siga em frente se o nome do C07 estiver lá.**

> **Regra deste guia:** antes de cada **Ctrl+S**, olhe a barra de título. Tem que estar escrito `C07-simpatia-da-virada`. Isso vale principalmente em 03/12, quando o projeto do C05 também vai estar aberto no mesmo dia.

**Se não houver "Save As"** (a confirmar na sua versão):
1. Feche o Effect House.
2. No PowerShell: `Copy-Item -Recurse "$BASE\projetos\C01-torcedometro" "$BASE\projetos\C07-simpatia-da-virada"`. Se o projeto for um arquivo com extensão, copie o arquivo e dê ao novo o nome `C07-simpatia-da-virada` com a mesma extensão.
3. Abra a cópia no Effect House e confira a barra de título.

**Se o projeto do C01 não existir ou não abrir:**
1. Use o projeto do C02 (`C02-meu-proximo-carro`), que é a mesma montagem com outras imagens. Faça o backup dele (1.1, com o nome do C02) e a Parte 1.2 a partir dele. Nas Partes 2 a 5, onde o guia diz "o que veio do C01", leia "o que veio do C02" (o título esperado é `carro_titulo` e a sequência, `cartas_carro`). Anote no relatório.
2. Se nem o C02 servir, monte do zero pela Parte 18 (Plano B1).

---

## Parte 2: Reconhecer o que veio do C01

Não mude nada nesta parte. Só anote no relatório, na seção do C07.

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
9. Veja no relatório do C01 se ele usou as imagens **512×256** ou as **quadradas** (`quadrado_512`). O C07 tem que usar a mesma versão.

---

## Parte 3: Marcar as imagens antigas e importar as novas

As imagens do C07 têm **os mesmos nomes de arquivo** das do C01 (`titulo_toque.png`, `carta_01.png`…). Para não confundir na hora de trocar, primeiro você muda o nome das antigas no projeto.

### 3.1 Marcar as antigas

No painel **Assets**:

1. Clique com o botão direito no título que você anotou na Parte 2, passo 2 (ex.: `titulo_toque`) → **Rename** → digite `ANTIGO_titulo_toque`.
2. Se existir também `titulo`, faça o mesmo: `ANTIGO_titulo`.
3. Clique com o botão direito na sequência anotada no passo 5 (ex.: `cartas_torcedor`) → **Rename** → digite `ANTIGO_cartas`.

> Mudar o nome no painel Assets **não** muda o efeito: o objeto continua usando a mesma imagem. Os arquivos do C01 em `tiktok-efeitos\efeito-1-torcedometro\` também continuam intactos.

### 3.2 Importar o título

1. No painel **Assets**, clique em **+** (**Add**) → **Import** → **From Computer** (o mesmo caminho usado no C01).
2. Vá até `<A>` (`<BASE>\tiktok-efeitos\efeito-7-simpatia-da-virada\assets\`).
3. Selecione o título, conforme o que o C01 usou:
   - C01 com `titulo_toque` → selecione **`titulo_toque.png`**;
   - C01 com `titulo` (sem etiqueta) → selecione **`titulo.png`**;
   - C01 com as quadradas → use os mesmos nomes, mas dentro de `<A>\quadrado_512\`.
4. Clique em **Abrir**.
5. Renomeie o asset novo para **`virada_titulo`**.

### 3.3 Importar as 26 cartas (Texture Sequence)

1. No painel **Assets**, clique em **+** (**Add**) → **Import** → **Texture Sequence**.
2. Abra a pasta **`<A>\cartas\`** (ou `<A>\quadrado_512\cartas\`, se o C01 usou as quadradas).
3. Faça como no C01: se a janela pedir arquivos, **Ctrl+A** e **Abrir**; se pedir pasta, selecione a pasta `cartas` e confirme.
4. Confira se apareceu **uma** sequência nova e se ela tem **26 frames** no **Inspector**.
5. Renomeie a sequência nova para **`cartas_simpatia`**.
6. Confira a ordem:
   - o **primeiro** quadro tem que ser **PULAR 7 ONDAS / (VALE NO BALDE)**, com fundo roxo-uva e uma onda com um balde azul no selo;
   - o **último** tem que ser **PEDIDO NA HORA / DOS FOGOS**, com fundo ameixa e fogos com uma estrela cadente no selo.
   Se estiver fora de ordem, apague `cartas_simpatia` e importe de novo com **Ctrl+A**. A equipe não conseguiu confirmar se o programa ordena pelo nome do arquivo (a confirmar na sua versão); no C01 você já viu como ele se comporta.

### 3.4 Compressão

1. Clique em `ANTIGO_cartas` e veja a compressão no **Inspector**.
2. Ponha **a mesma** em `cartas_simpatia`. Se o C01 ficou em **Automatic** ou **Manual → 512 → High**, mantenha assim.
3. Faça o mesmo com `virada_titulo`, sempre em **High** (ou Automatic).

---

## Parte 4: Trocar as imagens

### 4.1 Título

1. Na **Hierarchy**, clique em **Title**.
2. No **Inspector**, componente **Image** → campo **Texture** → escolha **`virada_titulo`**. Também dá para arrastar do painel Assets para o campo.
3. Confira no **Preview** se aparece o bilhete roxo com "MINHA SIMPATIA / PRA 2027 É…" e o cacho de uva no selo.

### 4.2 Cartas

1. Na **Hierarchy**, clique em **RandomAnimationSequence**.
2. Siga o caso que você anotou na Parte 2:
   - **Caso A:** componente **Animation Sequence** → campo da sequência → **`cartas_simpatia`**. Não mexa no **Texture** do **Image**, porque o Animation Sequence troca essa textura sozinho.
   - **Caso B:** componente **Image** → campo **Texture** → **`cartas_simpatia`**.
3. **Não mexa** no FPS nem no modo de reprodução (**Forward / Random / Shuffle**). Deixe como estavam no C01.
4. **Só no Caso S:** clique em `Controle` → componente **TorcedometroController** → campo **Sequencia Cartas** → **`cartas_simpatia`**. Os outros campos ficam como estão (Titulo = Title, Cartas = RandomAnimationSequence, Tempo Giro = 2, Tempo Some Titulo = 0.3, Girar De Novo No Toque = marcado). O nome do script continua "Torcedometro". Isso não aparece para ninguém e não precisa mudar.
5. **Só no Caso T:** abra o **Visual Scripting** e clique na caixa do randomizador. Se algum campo dela mostrar `ANTIGO_cartas` ou `ANTIGO_titulo_toque`, troque por `cartas_simpatia` ou `virada_titulo` (a confirmar na sua versão: o template pode não ter campo de imagem na caixa).
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

> Se você quiser usar o `titulo.png` como reserva durante os testes, importe-o agora, renomeie para `virada_titulo_sem_toque` e apague antes da pausa (Parte 9). Só importe se for usar.

---

## Parte 6: Proporção, posição e tamanho (só conferir)

O quadro do C07 é o mesmo do C01: **512×256**. A equipe mediu a área com desenho em todas as 26 cartas, nas 4 reservas e no título: vai de **3 a 509 px na largura e de 2 a 250 px na altura**, exatamente a mesma do C01. Por isso, **a posição e o tamanho do C01 servem sem mudança.**

1. Escolha no **Preview** o primeiro dos 3 rostos de exemplo.
2. Confira o título:
   - o **selo dourado ondulado** (com o cacho de uva) está **redondo** (se virou ovo, veja a Parte 16, linha "esticado");
   - o bilhete está **inteiro na tela**, inclusive o selo de cima e as duas pontas dobradas;
   - a pílula **"👆 TOQUE NA TELA"** aparece inteira, e a borda de baixo do bilhete fica **logo acima do cabelo**, sem cobrir a testa nem os olhos.
3. Clique no Preview para sortear e espere a carta parar.
4. Confira a carta da mesma forma: **selo redondo**, bilhete inteiro, borda de baixo acima do cabelo.
5. Repita nos outros 2 rostos de exemplo.

**Só se algo não couber:** ajuste como na Parte 5.2 do guia do C01:
- mude **Scale** com **X e Y iguais** e **Position Y** no **RandomAnimationSequence**;
- copie o **2D Transform** (três pontinhos ⋮ → **Copy**) e cole no **Title** (⋮ → **Paste**);
- a largura do bilhete fica em cerca de **1,6 vez a largura da cabeça** (entre 1,4 e 1,8).

Anote no relatório se mudou algo e os valores novos.

---

## Parte 7: A lógica (só conferir)

O C07 tem **26 cartas, igual ao C01**. Então a lógica não muda: nenhum campo de quantidade de quadros precisa ser alterado.

**Caso T (template):** no **Visual Scripting**, caixa do randomizador:

| Campo | Valor no C07 | Se estiver diferente |
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

- [ ] Ao abrir, aparece **só o título**, sem nenhuma carta por trás.
- [ ] O título **fica na tela até o clique**.
- [ ] A pílula dourada **"👆 TOQUE NA TELA"** aparece inteira, sem corte.
- [ ] O **selo dourado ondulado** está redondo no título e nas cartas (nada esticado).
- [ ] O bilhete está **inteiro na tela**, com o selo de cima e as duas pontas dobradas, nos 3 rostos de exemplo.
- [ ] A borda de baixo do bilhete fica **acima do cabelo**, sem cobrir os olhos.
- [ ] O título **acompanha a cabeça** quando o rosto se mexe.
- [ ] Ao clicar, o título **some** e as cartas **giram**. No giro, o fundo alterna entre roxo-uva, ameixa e anil.
- [ ] O giro dura **cerca de 2 s** e **para** numa carta.
- [ ] Nenhuma carta do **Torcedômetro** aparece no giro. Se aparecer um ingresso **laranja ou violeta com recortes redondos nas laterais**, a troca da Parte 4.2 não pegou em algum lugar. (Se a base foi o C02: nenhuma etiqueta grafite com faixa de asfalto.)
- [ ] Dá para **ler** a carta parada, inclusive as de letra menor: 13 (PAGAR UM / BOLETO (O MENOR)), 21 (MOEDA NO SAPATO / (A NOITE TODA)), 16 (ALGO VERMELHO / PRO CRUSH NOTAR) e 15 (FRANGO NÃO / (CISCA PRA TRÁS)). Para conferir sem esperar o sorteio, abra a imagem em `<A>\cartas\` no visualizador do Windows ao lado do Preview e compare o tamanho do texto.
- [ ] O texto **dourado** entre parênteses dá para ler nos 3 fundos (uva, ameixa e anil).
- [ ] A carta continua **parada e presa na cabeça** quando o rosto se mexe.
- [ ] Não aparece **borda escura** nem quadrado em volta do bilhete.
- [ ] Quando o rosto **sai** da imagem, o bilhete **some**.
- [ ] Clicar **de novo** depois do resultado faz o mesmo que no C01 (gira de novo ou nada). Anote.

### 8.3 Teste do sorteio

1. Faça **15 sorteios**, voltando ao título ou clicando de novo, como no C01.
2. Anote o texto de cada carta que saiu (use a tabela da 0.7).
3. Avalie:
   - **OK:** saíram **pelo menos 9 cartas diferentes** e **nenhuma saiu mais de 4 vezes**.
   - **Problema:** sempre as mesmas 2 ou 3, sempre a mesma, ou uma ordem fixa. Troque o modo da sequência para **Shuffle** (ou **Random**), como na Parte 7.3 do guia do C01, e repita. Se continuar, use o Plano C (Parte 18).

> Se o C01 passou neste teste, o C07 deve passar também: a lógica e a quantidade de cartas são as mesmas.

### 8.4 Salvar

Confira a barra de título e aperte **Ctrl+S**.

---

## Parte 9: Tamanho e desempenho

1. Se você importou `virada_titulo_sem_toque` e não usou, apague do painel **Assets**.
2. Na barra de cima, clique em **Click to update** no indicador de tamanho.
3. Anote o tamanho. O C01 deu **1,6 MB**. As imagens do C07 pesam um pouco mais (2,62 MB contra 2,15 MB em PNG), então o esperado é **perto de 2 MB** (estimativa da equipe, a confirmar na sua versão).
   - **Até 5 MB:** siga.
   - **Entre 5 e 8 MB:** sobrou alguma coisa do C01 ou do C08. Volte à Parte 5.
   - **Acima de 8 MB:** não dá para enviar. Apague o que sobrou e, se ainda passar, mude a compressão de `cartas_simpatia` para **Manual → 512 → Medium** e confira se o texto continua nítido, principalmente o dourado entre parênteses.
4. Clique em **Test performance** → **Run test** e espere cerca de 30 s.
   - **Passou:** siga.
   - **Falhou:** clique em **View suggestions**, apague o que sobrou e teste de novo.
   - **Não rodou** (como aconteceu no C01): anote a mensagem e siga. O efeito é só 1 imagem e 1 sequência, sem IA e sem segmentação.

---

## Parte 10: Vídeo demo

O formulário 5.16 trata o demo como opcional, mas **mande sempre**. Só a revisão vê o vídeo. Regras: **9:16, MP4 ou MOV, até 15 s, até 32 MB**. Grave agora, na montagem, para o dia 03/12 ficar só com o envio.

1. Grave como no C01 (Parte 9 do guia dele): aparelho 9:16 no Preview, rosto de exemplo em vídeo e **Screen record** (ou **Win+Shift+R**). Use só os rostos de exemplo do programa: nada de webcam com mesa de festa, taça ou garrafa ao fundo.
2. Siga o roteiro:

| Tempo | O que acontece |
|---|---|
| 0–2 s | Título parado sobre a cabeça, com "TOQUE NA TELA" |
| ≈ 2 s | Clique no Preview |
| 2–4,5 s | Título some e as cartas giram |
| 4,5–8 s | Resultado parado, com o rosto se mexendo um pouco |
| ≈ 8 s | Clique de novo, se o template girar de novo (se não girar, deixe o resultado até o fim) |
| 8–13 s | Segundo giro e segundo resultado |

3. **Se algum resultado do vídeo for a carta 01 (PULAR 7 ONDAS), 05 (TUDO BRANCO) ou 12 (ROUPA ÍNTIMA AMARELA), grave de novo.** São as 3 cartas que a equipe marcou como as mais sensíveis para a revisão, e não vale a pena chamar atenção para elas no vídeo. Qualquer outra carta serve.
4. Salve em `<BASE>\videos-demo\C07-demo-bruto.mp4`.
5. Confira em **Propriedades → Detalhes**: em pé, 9:16 (ex.: 1080×1920) e até 15 s.
6. Se não estiver em 9:16, rode:

```powershell
cd "$BASE\videos-demo"
ffmpeg -i C07-demo-bruto.mp4 -t 15 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" -c:v libx264 -pix_fmt yuv420p -an C07-demo.mp4
```

7. Se o bruto já estava em 9:16 e até 15 s, só renomeie para `C07-demo.mp4`.
8. Abra o `C07-demo.mp4` e confira se o bilhete continua inteiro (com o selo) e se a carta final dá para ler.

---

## Parte 11: Pausa até 03/12

Aqui termina a montagem. **Não clique em Submit.**

1. Confira a barra de título e aperte **Ctrl+S**.
2. Rode: `Copy-Item -Recurse -Force "$BASE\projetos\C07-simpatia-da-virada*" "$BASE\projetos\backup\"`
3. Escreva no `relatorio-montagem.md`, seção do C07: **"C07 montado e testado, aguardando 03/12"**, com os itens da Parte 19 que já tiver.
4. Mande para a nuvem (`session_01XsQ8UziuLNch4tqqVVQfCw`) um resumo de 3 linhas: montado, resultado do teste de sorteio, tamanho do pacote.
5. Até 03/12, **não abra o projeto do C07 para mexer**, a não ser que o `PRONTO-PARA-MONTAR.md` mande. Se precisar corrigir o C01 ou outro sorteio nesse meio-tempo, faça no projeto **dele**.

---

## Parte 12: No dia 03/12: conferências antes de enviar

Faça na ordem. Leva uns 15 minutos.

### 12.1 Ordens novas

1. Abra o `PRONTO-PARA-MONTAR.md` mais novo (link da 0.3) e leia a seção **Atualizações**.
2. **Se ela disser algo sobre o C07 (data, desafio, carta trocada), vale ela, e não este guia.**
3. Ordem do dia: envie primeiro o **C05**, pelo guia dele (`efeito-3-meu-2027-vai-ser\guia-montagem.md`), e depois o **C07**, por este guia. **Se o C05 travar, envie o C07 mesmo assim**, no mesmo dia. Os dois são independentes.

### 12.2 Status dos outros sorteios

1. Abra **Manage Effects**.
2. Veja o status de **Torcedômetro**, **Eu no grupo da família**, **Meu próximo carro** e **Meu amigo secreto** (os outros sorteios da conta, todos do mesmo template). Se algum foi publicado com um nome alternativo, procure pelo nome que está no `relatorio-montagem.md`.
3. Decida:
   - **Active** ou **Under review:** siga.
   - **Needs revision por "duplicado", "parecido com outro efeito" ou "spam"** em qualquer um deles: **não envie o C07.** Mande o print do motivo para a nuvem e espere ordem. O C07 sai do mesmo template, e mandar mais um agora pode piorar.
   - **Needs revision por motivo técnico** (desempenho, tremor, tamanho): aplique a mesma correção no C07 antes de enviar, refaça o checklist da Parte 8 e avise a nuvem.
   - **Needs revision por conteúdo** (uma carta, um texto, uma marca): não afeta o C07, que tem outras imagens. Siga.

### 12.3 As imagens da equipe mudaram desde a montagem?

1. Baixe o zip de novo e extraia **só a pasta `tiktok-efeitos`** em `<BASE>`, por cima da antiga.
2. Rode no PowerShell (depois das duas linhas da 0.5 que definem `$BASE` e `$A`):

```powershell
$antes = Import-Csv "$BASE\C07-conferencia-arquivos.csv"
$agora = Get-ChildItem "$A\titulo_toque.png","$A\titulo.png","$A\cartas\*.png","$A\quadrado_512\titulo_toque.png","$A\quadrado_512\titulo.png","$A\quadrado_512\cartas\*.png" | Get-FileHash -Algorithm SHA256 | Select-Object @{n='Arquivo';e={$_.Path.Substring($A.Length + 1)}}, Hash
Compare-Object $antes $agora -Property Arquivo, Hash
```

3. Leia o resultado:
   - **Não apareceu nada:** as imagens são as mesmas que você montou. Siga para a 12.4.
   - **Apareceram linhas:** a equipe mudou essas imagens. Olhe só as linhas da versão que você usa (512×256 sem `quadrado_512\`, ou só as `quadrado_512\`):
     - **mudou alguma `cartas\carta_XX.png`:** troque a sequência inteira, como na Parte 17, passos 1 a 4 do bloco "No Effect House" (sem a parte de reenvio), e refaça o checklist da Parte 8.2;
     - **mudou o título que você usa:** importe o novo (Parte 3.2), ponha no **Title** (Parte 4.1), apague o `virada_titulo` antigo, renomeie o novo para `virada_titulo`, refaça a Parte 8.2 e **grave o demo de novo** (Parte 10).
   - Em qualquer caso, a versão certa é a da pasta da equipe: refaça o que está acima e conte para a nuvem quais arquivos mudaram.

### 12.4 Nome

1. Em **Manage Effects**, confira se nenhum efeito da conta já se chama **Simpatia da Virada**. Os nomes esperados lá são: Eu no grupo da família, Torcedômetro, Meu próximo carro, Perrengue no volante, Meu amigo secreto e Meu 2027 vai ser.
2. **Opcional, 3 min (a confirmar se funciona sem login):** no navegador do PC, abra https://www.google.com/search?q=site%3Atiktok.com%2Fsticker+%22Simpatia+da+Virada%22. Se aparecer um efeito **famoso** com exatamente esse nome, use o nome alternativo da Parte 13.4 e anote. Se a busca não abrir ou não achar nada, siga com **Simpatia da Virada**.

### 12.5 Conteúdo

1. Confira se nenhuma imagem do projeto tem marca, logo, nome de loja, @ da conta, link ou chamada para comprar. As imagens da equipe já seguem essa regra. O risco é sobrar alguma do C01 ou do C08 no painel **Assets**.
2. Confira se **não há som** ligado ao efeito.
3. Riscos conhecidos e aceitos pela equipe (não mude nada):
   - cartas **01 (PULAR 7 ONDAS)** e **05 (TUDO BRANCO)**: nasceram de tradição religiosa, mas hoje são costume popular de Réveillon. Texto e desenho não têm nada religioso;
   - carta **12 (ROUPA ÍNTIMA AMARELA)**: o desenho é só uma carinha de "psiu" e um coração amarelo, sem roupa íntima.
   Se a revisão implicar com alguma delas, troque pela reserva (Parte 17).

### 12.6 Salvar e fazer backup

1. Confira a barra de título (`C07-simpatia-da-virada`) e aperte **Ctrl+S**.
2. Rode: `Copy-Item -Recurse -Force "$BASE\projetos\C07-simpatia-da-virada*" "$BASE\projetos\backup\"`

---

## Parte 13: Ícone e envio (somente em 03/12/2026)

### 13.1 A data

**Hoje é quinta, 03/12/2026, ou um dia depois?** Se ainda não chegou 03/12, **pare**: volte à Parte 11. Se 03/12 já passou e o C07 não foi enviado, envie hoje e avise a nuvem (Parte 0.2).

### 13.2 O desafio

1. Veja no `PRONTO-PARA-MONTAR.md` (12.1) a decisão do Vini sobre o desafio **"Nov Social Randomizer Sub Challenge"** e, se aparecer, sobre qualquer desafio novo de fim de ano.
2. Decida:
   - **A ordem manda entrar num desafio, com o nome dele:** no formulário, selecione **esse** desafio no campo **Challenge**. Se ele não aparecer na lista (por exemplo, porque o prazo acabou ou porque não aceita efeito novo), deixe **Challenge** vazio, envie e anote.
   - **A ordem manda não entrar**, ou não fala de desafio nenhum mas a decisão já saiu: deixe **Challenge** vazio.
   - **A decisão ainda não saiu:** a ordem de 06/11 (05:50) no `PRONTO-PARA-MONTAR.md` diz "não faça o Submit dos sorteios até sair a decisão do Vini sobre o desafio", e ela **vale também para o C07**. Então: mande uma mensagem para a nuvem dizendo que o C07 está pronto e esperando só o desafio, e **não envie**. Releia o `PRONTO-PARA-MONTAR.md` todo dia às 9h e às 15h. Envie assim que sair (a) a decisão ou (b) uma atualização liberando o envio do C07 sem desafio. Se essa ordem antiga tiver sido apagada ou trocada por outra regra, vale a regra nova. Este efeito é de data: cada dia de espera come a folga para corrigir uma reprovação antes de 18/12, então diga isso na mensagem para a nuvem.
3. **Nunca aceite os termos de um desafio por conta própria.** Se aparecer outro desafio na lista que não esteja na ordem, anote o nome e o prazo no relatório e conte para a nuvem, mas não selecione.

### 13.3 Ícone (Create icon)

Pela ordem da equipe, o ícone do formulário 5.16 sai do **Create icon**, com uma foto modelo, e não do `icone_162.png`.

1. Clique em **Create icon** na barra de cima (o mesmo caminho do C08 e do C01).
2. Escolha um modelo de rosto e espere o efeito aparecer nele.
3. **Ícone 1, o resultado:** clique para sortear até parar numa destas cartas, que têm frase curta, letra grande e nenhum risco de revisão. Na ordem de preferência:
   1. **COMER 12 UVAS / (SEM PRESSA)** (carta 07; tem uva, como o título);
   2. **3 PULINHOS / À MEIA-NOITE** (carta 11);
   3. **LENTILHA PRO / DINHEIRO VIR** (carta 03);
   4. **ENTRAR COM O / PÉ DIREITO** (carta 19);
   5. **NÃO MANDAR / OI PRO EX** (carta 02).
   Com 5 cartas boas em 26, devem bastar uns 5 cliques. **Não use** as cartas 01, 05 e 12 no ícone. Enquadre o rosto e o bilhete inteiro, com o bilhete ocupando a maior parte do quadrado.
4. **Ícone 2, a pergunta:** se der para ter 2 ícones, faça o segundo com o **título** ("MINHA SIMPATIA / PRA 2027 É…" com o cacho de uva), voltando ao começo do efeito.
5. Confira na prévia pequena se o texto do ícone 1 dá para ler. Se não der, tente outra carta da lista.
6. Clique em **Done** (ou **Submit**, conforme a versão).

**Plano de exceção:** se o Create icon não funcionar e o formulário tiver um botão de **Upload** de PNG, use `<A>\icone_162.png` (cacho de uva com fogos, fundo roxo-uva) e, como 2º, `<A>\icone_alt_162.png` (uva com relógio marcando meia-noite, fundo ameixa). Os dois têm 162×162 e o desenho dentro da área segura. Anote no relatório.

### 13.4 O formulário

1. Clique em **Submit**, no canto de cima à direita.
2. **Atenção, o passo mais importante do envio.** O formulário pode oferecer três caminhos:
   - **Submit a new effect** (enviar um efeito novo): **é este.**
   - **Update an existing effect**: aparece quando a conta tem efeitos **Active**. **Não use.** Ele trocaria o Torcedômetro (ou outro efeito) pelo C07.
   - **Replace an existing effect**: aparece com efeitos em **Draft** ou **Needs revision**. **Não use**, pelo mesmo motivo.

   Como este projeto é uma cópia do C01, o formulário pode já vir com o nome **Torcedômetro** ou com o ícone do C01. **Se isso acontecer, pare**: volte e escolha **Submit a new effect**. Se a tela não oferecer essa opção, não envie: avise a nuvem com um print.

   > O C01 foi feito a partir do projeto do C08, e os dois entraram como efeitos separados. Então o caminho de "efeito novo" funciona nesta conta. Mesmo assim, confira sempre.

3. Preencha:

| Campo | O que colocar |
|---|---|
| **Effect name** | `Simpatia da Virada` (18 caracteres; limite 25), com **S** e **V** maiúsculos. Sem reticências, sem "AI" (não usa IA generativa). Se recusar por nome repetido: `Simpatia de Ano Novo` (20); se recusar de novo: `Minha Simpatia 2027` (19). O nome não tem acento, então não há versão "sem acento". |
| **Effect icon** | Os ícones do Create icon (13.3): 1º o resultado, 2º o título |
| **Hint** (lista) | A opção de **tocar na tela**. Se houver opção em português, use ela (ex.: "Toque na tela"). Se a lista for só em inglês, a mesma que você usou no C01 (provavelmente "Tap the screen" ou parecido). Se o campo for **texto livre**: `Toque na tela`. |
| **Sound** (som) | **Nenhum.** Não ligue som nem música. |
| **Challenge** | Conforme a 13.2. |
| **Trend** | Deixe **vazio**, a não ser que o `PRONTO-PARA-MONTAR.md` mande outra coisa. Se aparecer uma trend de Ano Novo, Réveillon ou 2027, anote o nome no relatório e conte para a nuvem, mas **não segure o envio** por isso (a confirmar na sua versão: o que o campo faz). |
| **Demo video** | `<BASE>\videos-demo\C07-demo.mp4` |

**Se aparecer algum campo que não está na tabela** (a versão pode ter mudado):

| Campo | O que colocar |
|---|---|
| **Description** (descrição) | `Sorteio de Réveillon sobre a cabeça. Toque na tela e descubra a simpatia que você vai ter que cumprir pra 2027: pular 7 ondas (vale no balde), comer 12 uvas sem pressa, lentilha pro dinheiro vir e mais 23. Só simpatias populares e humor leve, sem religião, bebida ou marca.` (273 caracteres). Se o campo for pequeno: `Toque na tela e descubra a simpatia que você vai cumprir pra 2027.` (66) |
| **Category** | A mais próxima de **Funny** (engraçado); senão, **Randomizer** (sorteio); senão, **Interactive** |
| **Tags** | `simpatia`, `reveillon`, `anonovo`, `sorteio`, `2027`. Se aceitar acento e espaço: `simpatia`, `réveillon`, `ano novo`, `sorteio`, `2027`. Se tiver que ser em inglês: `new year`, `superstition`, `randomizer`, `funny`, `2027`. Reserva, se alguma for recusada: `virada`, `humor`, `simpatias`. |
| **Comentários para a revisão** ("Notes", "Additional comments") | O texto em inglês e, embaixo, o em português, que estão logo abaixo desta tabela |
| Qualquer outro | Deixe o padrão e anote |

**Texto para comentários** (só se o campo existir):

> New Year's Eve head randomizer. Tap the screen and a card above your head shows a popular Brazilian New Year's superstition to act out in the video, such as "jump 7 waves (a bucket counts)", "eat 12 grapes (slowly)" or "lentils so money comes". 26 original light-humor texts in Brazilian Portuguese with simple drawings. Only secular folk customs: no religious symbols or offerings, no alcohol, no handling of fireworks, no brands, logos or real people. No generative AI.
>
> Sorteio de Réveillon sobre a cabeça. Toque na tela e descubra a simpatia que você vai ter que cumprir pra 2027: pular 7 ondas (vale no balde), comer 12 uvas sem pressa, lentilha pro dinheiro vir e mais 23. Só simpatias populares e humor leve, sem religião, bebida ou marca.

**Se a carta 01 (PULAR 7 ONDAS) tiver sido trocada pela reserva R4** (Parte 17), troque nos dois textos acima e na descrição: em português, "pular 7 ondas (vale no balde)" por "moeda no sapato a noite toda"; em inglês, "jump 7 waves (a bucket counts)" por "a coin in your shoe all night long". As outras trocas não mexem nos textos.

### 13.5 Enviar

1. Revise o nome: "Simpatia da Virada", sem espaço sobrando no começo ou no fim.
2. Confira de novo se está no caminho **Submit a new effect**.
3. Clique em **Submit**.
4. Tire um print da confirmação e salve em `<BASE>\prints\C07-enviado.png`.
5. Mande para a nuvem: nome enviado, data e hora, status, tamanho do pacote, caso (A/B, T/S), versão (512×256 ou quadrada), cartas usadas nos ícones e se entrou em algum desafio.

---

## Parte 14: Acompanhar o status

1. Abra **Manage Effects**.
2. **Confira se o C07 aparece separado dos outros**, com o nome "Simpatia da Virada", e se o **Torcedômetro** continua lá com o nome dele. Se o Torcedômetro sumiu ou mudou de nome, o envio caiu em "Update" ou "Replace". Avise a nuvem na hora, com print, e não faça mais nada nesses dois efeitos.
3. Confira o status uma vez por dia, de manhã, até sair o resultado:

| Status | O que fazer |
|---|---|
| **Draft** | Clique em **Finish submission** e termine. |
| **Under review** | Esperar (1 a 3 dias úteis; a equipe conta com o resultado em seg 07 ou ter 08/12). |
| **Needs revision** | Leia o motivo, corrija (Partes 16 e 17) e **reenvie no mesmo dia**, por este projeto, com **Replace an existing effect** apontando para **Simpatia da Virada** (a confirmar na sua versão: o nome da opção). É o único caso em que "Replace" é usado, e só no próprio C07. Avise a nuvem. O limite da equipe é estar **aprovado até sex 18/12**. |
| **Active** | Anote a data e pegue o link (Manage Effects → menu ⋯ do efeito → **Share**). Mande para a nuvem na hora: ele entra na gravação do Vini de **sábado, 12/12**, junto com o C05. |
| **Deactivated** | Leia o motivo e avise a nuvem. |

---

## Parte 15: Resumo de 1 tela (para quem já fez o C01)

**Na montagem (assim que o C07 for liberado):**
1. Conferir os arquivos e salvar `C07-conferencia-arquivos.csv` (0.5).
2. Backup do C01 → abrir o C01 → **Save As `C07-simpatia-da-virada`** → conferir a barra de título.
3. Assets: renomear os antigos para `ANTIGO_…`.
4. Importar `<A>\titulo_toque.png` (→ `virada_titulo`) e a sequência `<A>\cartas\` (→ `cartas_simpatia`, 26 frames, 1º PULAR 7 ONDAS, último PEDIDO NA HORA DOS FOGOS).
5. Title → Texture = `virada_titulo`. RandomAnimationSequence → sequência = `cartas_simpatia` (Caso A no Animation Sequence, Caso B no Image, Caso S também no script).
6. Apagar os `ANTIGO_…`. Se der "em uso", achar a referência.
7. Conferir posição (selo redondo), lógica (TapToSpin ligado, 2, 0.3) e checklist; fazer 15 sorteios.
8. Tamanho, Test performance, demo `C07-demo.mp4` (sem as cartas 01, 05 e 12 no vídeo).
9. Backup, relatório "aguardando 03/12", resumo para a nuvem. **Sem Submit.**

**Na quinta, 03/12/2026:**
1. Ler o `PRONTO-PARA-MONTAR.md`; enviar o C05 primeiro.
2. Status dos outros sorteios (duplicidade = parar); conferir se as imagens mudaram (CSV); nome; conteúdo; backup.
3. Desafio conforme a ordem → **Create icon** (carta 07, 11, 03, 19 ou 02 + título) → **Submit a new effect** → `Simpatia da Virada`, hint de toque, sem som, trend vazio, demo.
4. Manage Effects: o C07 aparece separado. Status 1 vez por dia; Active → link para a nuvem.

---

## Parte 16: Problemas comuns e soluções

| Problema | Causa provável | Solução |
|---|---|---|
| A barra de título ainda diz C01 | O Save As não foi feito ou não pegou | **Não salve.** Feche sem salvar, reabra o C01 e faça a Parte 1.2 de novo. Se já salvou por cima, restaure de `projetos\backup\`. |
| A barra de título diz C05 (em 03/12) | Projeto errado aberto | Feche sem salvar e abra `C07-simpatia-da-virada`. |
| Não acho o projeto do C01 | Nome diferente ou outra pasta | Veja o `relatorio-montagem.md` e o `reconhecimento.md`. Se não existir, use o do C02 (Parte 1.2, último bloco) ou o Plano B1 (Parte 18). |
| Os assets novos vieram com "1" ou "(2)" no nome | Os antigos não foram renomeados antes | Siga mesmo assim: identifique os novos pela miniatura (bilhete roxo com borda dourada e selo ondulado) e renomeie para `virada_titulo` e `cartas_simpatia`. |
| No giro aparece um ingresso do C01 (laranja ou violeta, com recortes nas laterais) | A sequência antiga continua ligada em algum lugar | Parte 4.2: confira Animation Sequence, Image, o script (Caso S) e a caixa do randomizador. |
| "Asset em uso" ao apagar o antigo | Idem | Parte 5, passo 3. |
| A sequência veio com menos de 26 quadros ou fora de ordem | Seleção incompleta | Apague `cartas_simpatia` e importe de novo com **Ctrl+A**. |
| Esticado (o selo dourado virou ovo) | Size ou Stretch Mode diferente do C01, ou mistura de versão quadrada com 2:1 | Confira se o título e as cartas são da **mesma** versão do C01 (512×256 ou `quadrado_512`). Depois, Parte 5.1 do guia do C01. |
| O selo de cima sai cortado no topo da tela | Bilhete alto demais para aquele rosto | Baixe um pouco o **Position Y** dos dois objetos (copie o 2D Transform de um para o outro) ou reduza a **Scale** em 5% (X e Y juntos). |
| Texto difícil de ler (principalmente o dourado entre parênteses) | Compressão baixa ou bilhete pequeno | Compressão **High** e, se preciso, Scale +10% (X e Y juntos), conferindo se tudo cabe. |
| Clicar não gira | TapToSpin desligado ou clique fora da imagem | Parte 7. Clique **dentro** do Preview. |
| O título some sozinho antes do toque | Igual ao C01 | Use a mesma solução que você usou no C01 (TitleDelay, título sem etiqueta ou Plano C). |
| Sai sempre a mesma carta | Modo de reprodução | Parte 8.3: **Shuffle** ou **Random**. Se não resolver, Plano C. |
| Pacote acima de 8 MB | Sobrou coisa do C01 ou do C08 | Parte 9. |
| O programa pede atualização em 03/12 | Saiu versão nova | Se der para enviar sem atualizar, envie e atualize depois. Se o envio exigir a atualização: atualize (https://effecthouse.tiktok.com/download), reabra o projeto, refaça o checklist da Parte 8.2 com 5 sorteios e envie. Anote a versão nova. |
| O formulário veio com "Torcedômetro" preenchido | Caiu em Update ou Replace | Parte 13.4, passo 2: volte e escolha **Submit a new effect**. |
| O formulário recusa o nome | Nome repetido | `Simpatia de Ano Novo` → `Minha Simpatia 2027`. |
| O formulário recusa o vídeo | Formato, duração ou tamanho | Parte 10, passo 6 (ffmpeg). |
| O desafio da ordem não aparece no campo Challenge | Prazo acabou ou não aceita efeito novo | Deixe vazio, envie e anote (Parte 13.2). |
| **Needs revision** por religião, crença ou "superstição" | O revisor ligou alguma simpatia a religião | Se o motivo citar uma carta, troque só ela (Parte 17). Se for genérico, troque as 3 sensíveis de uma vez: 01 → R4, 05 → R2, 12 → R1. Reenvie e avise a nuvem. Se reprovar de novo pelo mesmo motivo, **pare** e espere ordem. |
| **Needs revision** por conteúdo sexual ou roupa íntima | Carta 12 | Troque a 12 pela R1 (Parte 17) e reenvie. |
| **Needs revision** por desafio perigoso | Cartas 04 (cadeira), 07 (uvas) ou 26 (fogos) | Troque a carta citada pela reserva livre (Parte 17) e reenvie. Se não citar carta, mande o print para a nuvem. |
| **Needs revision** por "duplicado" ou "parecido com outro efeito" | Mesmo template do C01 | Mande o print para a nuvem. **Não** reenvie sem ordem: a equipe decide se muda o visual. |
| **Needs revision** por marca, logo ou dinheiro | O revisor viu semelhança com marca ou moeda real | Mande o print do motivo e o número da carta para a nuvem. Enquanto isso, se for uma carta só, troque pela reserva (Parte 17). |
| **Needs revision** por desempenho ou tremor | QA técnico | Test performance, teste com movimento, Parte 9. |
| Pediu login de novo ou está em outra conta | Login expirou | Seção 0.8, com o link. |

---

## Parte 17: Trocar uma carta vetada pela reserva

**A troca é sempre pelo arquivo.** Não adianta mudar só o texto no `textos.json`: o desenho de cada carta está preso ao número dela no `gerar.py`, e a carta nova sairia com o desenho antigo.

As 4 reservas (em `<A>\reservas\`):

| Código | Arquivo | Texto |
|---|---|---|
| R1 | `reserva_01.png` | FOLHA DE LOURO / NA CARTEIRA |
| R2 | `reserva_02.png` | UMA PEÇA VERDE / PRA SAÚDE |
| R3 | `reserva_03.png` | GRANA NO BOLSO / NA VIRADA (a coringa) |
| R4 | `reserva_04.png` | BANHO DE MAR / NO DIA 1º |

| Se vetarem… | Use (nesta ordem, a primeira que ainda estiver livre) |
|---|---|
| carta 01 (PULAR 7 ONDAS / (VALE NO BALDE)) | R4 → R3 |
| carta 05 (TUDO BRANCO / (ATÉ A MEIA)) | R2 → R3 |
| carta 12 (ROUPA ÍNTIMA / AMARELA (PSIU)) | R1 → R2 → R3 |
| carta 09 (ROMÃ NA / CARTEIRA VAZIA) | R1 → R3 |
| qualquer outra (ex.: 04, cadeira; 13, boleto; 18, carro) | R3 → R4 → R2 → R1 |

**Cada reserva entra uma vez só.** Se a da lista já foi usada, passe para a próxima. Se acabarem as reservas, avise a nuvem e espere: a equipe gera cartas novas.

Exemplo com a carta 12 (troque os números para o seu caso):

```powershell
$A = "$BASE\tiktok-efeitos\efeito-7-simpatia-da-virada\assets"
New-Item -ItemType Directory -Force "$A\cartas_trocadas" | Out-Null
Move-Item "$A\cartas\carta_12.png" "$A\cartas_trocadas\carta_12.png"
Copy-Item "$A\reservas\reserva_01.png" "$A\cartas\carta_12.png"
(Get-ChildItem "$A\cartas\*").Count    # tem que continuar 26
```

Se o projeto usa as quadradas, faça o mesmo dentro de `$A\quadrado_512\` (`cartas` e `reservas`).

No Effect House:
1. Apague `cartas_simpatia` do painel **Assets**. Se der "em uso", tire a sequência do objeto primeiro (Parte 5, passo 3) e tente de novo.
2. Importe a pasta `cartas` de novo (Parte 3.3) e renomeie para `cartas_simpatia`.
3. Ligue a sequência de novo (Parte 4.2, inclusive no script, se for Caso S).
4. Teste (Parte 8.2) e faça 5 sorteios.
5. Reenvie com **Replace an existing effect** → **Simpatia da Virada** (a confirmar na sua versão: o nome da opção). Se a carta trocada foi a 01, ajuste os textos (Parte 13.4, último parágrafo).
6. Avise a nuvem qual carta foi trocada e por qual reserva, para atualizar o `textos.json`.

> Cada reserva já vem com um dos 3 tons de fundo (uva, ameixa ou anil), e pode acabar com o mesmo tom da carta vizinha no giro. É só estética, pode ignorar.

---

## Parte 18: Planos B e C (se a cópia do C01 não der certo)

| Plano | Quando usar | Esforço |
|---|---|---|
| **B1: template do zero** | Os projetos do C01 e do C02 não existem, não abrem ou ficaram estragados | médio (≈ 3 h) |
| **B2: preset de Interactions** | Não há template, mas o preset existe | baixo a médio |
| **B3: Visual Scripting nó a nó** | Não há template nem preset | médio |
| **C: script TypeScript** | A lógica do template falha (título some, sorteio viciado, não gira) | baixo |
| **Effect House AI** | Travou em qualquer passo | baixo. Pedidos prontos em `efeito-7-simpatia-da-virada\script\prompt-effect-house-ai.md` |

### Plano B1: template Randomizer 2D do zero

Siga as **Partes 1 a 9 do guia do C01** (`efeito-1-torcedometro\guia-montagem.md`), trocando:

| No guia do C01 | No C07 |
|---|---|
| pasta `efeito-1-torcedometro\assets\` | `efeito-7-simpatia-da-virada\assets\` |
| projeto `C01-torcedometro` | `C07-simpatia-da-virada` |
| título `titulo_toque` | `virada_titulo` (renomeie depois de importar) |
| sequência `cartas_torcedor` | `cartas_simpatia` |
| "QUE TORCEDOR / VOCÊ É?" | "MINHA SIMPATIA / PRA 2027 É…" |
| régua: medalha redonda | régua: selo dourado ondulado |
| cartas de leitura difícil 17, 18, 22 | 13, 21, 16, 15 |
| demo `C01-demo.mp4` | `C07-demo.mp4` |

Os valores são os mesmos: **TapToSpin ligado, TimeToSpin 2, TitleFadeOutTime 0.3, 26 quadros**, largura de cerca de 1,6 cabeça. Depois, volte para as Partes 10 a 14 **deste** guia, porque o envio do 5.16 é diferente do guia do C01 e a data do C07 é fixa.

### Plano B2: preset de Interactions (sem ligar fios)

O preset oficial **"Tap Screen to Play Animation Sequence Then Delay Pause"** toca a sequência ao tocar na tela e pausa depois de N segundos. Com o modo **Random** ou **Shuffle**, ela para numa carta qualquer. Exige o componente **Animation Sequence** no objeto.

1. Num projeto vazio (**New Project**/**Blank**; a confirmar na sua versão), salve como `C07-simpatia-da-virada`. Crie dois **Face Sticker** (**Hierarchy → + → Face Effects → Face Sticker**) e renomeie para `Titulo` e `Cartas`.
2. Importe o título e as cartas (Partes 3.2 e 3.3).
3. `Titulo`: **Image → Texture** = `virada_titulo`.
4. `Cartas`: **Add Component → Animation Sequence**, com a sequência `cartas_simpatia` e o modo **Shuffle** (ou **Random**). Desmarque o **autoplay**, se existir (a confirmar na sua versão).
5. Acerte proporção (2:1), posição e tamanho dos dois, iguais (Parte 5 do guia do C01). O selo dourado tem que ficar redondo.
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
- **Se não é:** siga a Parte 15, Plano C, do guia do C01, passos 1 a 19, com estas trocas: projeto `C07-simpatia-da-virada-script`; no campo **Sequencia Cartas**, `cartas_simpatia`. Se este plano der certo, é **esta** cópia que vai ser enviada em 03/12: anote no relatório e use o nome dela no lugar de `C07-simpatia-da-virada` nas Partes 11 a 14.
- O script **ainda não foi rodado** dentro do Effect House pela equipe (a confirmar). Se der erro, use o **Pedido 4** de `efeito-7-simpatia-da-virada\script\prompt-effect-house-ai.md`.

### Effect House AI

Veja no `reconhecimento.md` (item 3) se o assistente funcionou nesta conta. Os pedidos prontos, em inglês, estão em `efeito-7-simpatia-da-virada\script\prompt-effect-house-ai.md`:

| Pedido | Quando |
|---|---|
| 1 | A troca de imagens na cópia do C01 travou (Partes 3 a 5) |
| 2 | Precisa configurar o template Randomizer 2D do zero (Plano B1) |
| 3 | Não há template: montar tudo do zero (Planos B2 e B3) |
| 4 | O script do Plano C deu erro |

Use o assistente para **destravar** um passo, sem mudar a ideia, os textos ou as imagens. Depois, refaça os checklists da Parte 8.

---

## Parte 19: O que anotar no relatório

Em `<BASE>\relatorio-montagem.md`, na seção do C07:

**Na montagem:**
- Nome real do projeto usado como base (C01 ou C02) e se o backup foi feito.
- Caso A ou B, Caso T ou S, versão 512×256 ou quadrada, título com ou sem etiqueta.
- Se o programa pôs a sequência na ordem certa sozinho (1º PULAR 7 ONDAS, último PEDIDO NA HORA DOS FOGOS).
- Se mudou posição ou escala, com os valores antigos e os novos.
- Valores da lógica conferidos (TapToSpin, TimeToSpin, TitleDelay, TitleFadeOutTime).
- Resultado do teste de sorteio: quantas cartas diferentes e a que mais repetiu.
- Tamanho do pacote e resultado do Test performance (ou a mensagem, se não rodou).
- Plano usado: cópia do C01, cópia do C02, B1, B2, B3 ou C.
- "C07 montado e testado, aguardando 03/12", com data e hora.

**Em 03/12:**
- O que o `PRONTO-PARA-MONTAR.md` dizia sobre o C07 e o desafio.
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
- Nós (Random gera número novo a cada leitura; Index Generator com Loop/Random/Shuffle) e limites técnicos: `tiktok-efeitos/pesquisa/03-tecnico-effect-house.md`.

Da própria equipe:
- Formulário do Effect House 5.16 (nome, ícone pelo Create icon, hint de lista, som, challenge, trend e demo), pasta `C:\Users\Pichau\Desktop\Efeitos` e a regra de esperar a decisão do desafio: `PRONTO-PARA-MONTAR.md`, atualizações de 06/11.
- Data de envio (qui 03/12, situação B, junto com o C05), aprovação esperada em 07 ou 08/12, gravação do Vini em sáb 12/12 e limite de aprovação em 18/12: `plano-curto-prazo.md`, seções do cronograma e da fila.
- C08 e C01 enviados como efeitos separados, C01 com 26 cartas e 1,6 MB: `STATUS.md`.
- Caminho de cópia do projeto do C01: `efeito-4-meu-proximo-carro/guia-montagem.md` (C02), que usa o mesmo método.
- Textos, nome, alternativas, hint, tags, comentários, reservas e cartas sensíveis: `efeito-7-simpatia-da-virada/textos.md` e `textos.json`.
- Medidas das imagens (área com desenho de 3 a 509 × 2 a 250 px, igual à do C01; pesos; tons de fundo em rodízio uva/ameixa/anil): conferidas pela equipe nos arquivos de `assets/` em 06/11/2026.
