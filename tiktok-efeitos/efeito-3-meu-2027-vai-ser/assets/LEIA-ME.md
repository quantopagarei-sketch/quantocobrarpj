# Imagens do efeito C05 "Meu 2027 vai ser"

Para a equipe e o Montador. O Vini não precisa fazer nada aqui.

Para refazer tudo, rode `python3 gerar.py`. O script lê os textos de `../textos.json`, então, se uma frase mudar lá, é só rodar de novo. Ele confere sozinho se a fonte tem todos os acentos, se algum texto encosta na borda, se algum arquivo passa de 1 MB ou de 1024 px.

**Por que tudo é branco:** o template **Future Life** pinta título, rótulos e respostas com uma cor sorteada, por isso as artes precisam ser brancas (tutorial oficial). Todas as artes principais são branco puro #FFFFFF, inclusive nos pixels transparentes, para não sair franja escura. No `previa.png` elas aparecem sobre xadrez escuro só para dar para ver.

## O que entra no efeito (versão principal)

| Arquivo | Tamanho | Onde vai no template |
|---|---|---|
| `titulo.png` | 1024×512 | Textura do grupo **Effect_Title** (substitui "My Future Life"). Texto: "MEU 2027 / VAI SER…", com brilhos. |
| `bolha_amor.png`, `bolha_grana.png`, `bolha_futebol.png` | 512×256 | Rótulos das bolhas, no grupo **Bubble_Titles** (substituem Lover / Income / Kids). Cada um tem a palavra e um ícone branco (coração, moeda, bola, carro). |
| `bolha_carro.png` | 512×256 | Rótulo da 4ª bolha, que é opcional. Também serve para o plano B: trocar FUTEBOL por CARRO. |
| `respostas_amor/amor_01…08.png` | 512×128 | Sequência do **Animated Texture Player** da bolha AMOR, no subgrafo *Color_Picker & Randomizer (Bubble_Input)*. São 3 nós, um por bolha. |
| `respostas_grana/grana_01…08.png` | 512×128 | Sequência da bolha GRANA. |
| `respostas_futebol/futebol_01…08.png` | 512×128 | Sequência da bolha FUTEBOL. |
| `respostas_carro/carro_01…06.png` | 512×128 | Sequência da bolha CARRO, só se entrar a 4ª bolha ou o plano B. |
| `icone_162.png` | 162×162, opaco | Ícone do formulário de envio (obrigatório). O desenho fica dentro da área segura de 144×144. |
| `icone_alt_162.png` | 162×162, opaco | 2º ícone (opcional, o formulário aceita até 2). É a mesma arte com fundo escuro. |

- Todas as respostas usam o mesmo tamanho de letra (49,5 px) e a mesma posição das linhas. Assim o texto não "pula" enquanto o sorteio gira. As linhas que começam com "(" saem em 84% do tamanho, porque o parêntese é a piada.
- Os nomes têm zero à esquerda (01, 02…), então a ordem alfabética é a ordem certa. A regra de nome na importação de sequência ainda está **(a confirmar)**.
- Peso: 3 bolhas = **348 KB**; 4 bolhas = **429 KB**. A meta da equipe é até 5 MB e o limite oficial é 8 MB. Nenhum arquivo passa de 40 KB, sem contar os ícones.

## Antes de importar: 2 testes rápidos no Effect House

**1) Tamanho das texturas originais (a confirmar).** Clique numa resposta original do template no painel Assets e veja o tamanho.
- Se for larga, com proporção perto de 4:1, use a versão principal (512×128).
- Se for quadrada, use `variantes/quadrado_512/` (mesma estrutura de pastas, texto centralizado dentro de um círculo).
- Se for outra proporção, há duas saídas: ajustar largura e altura do objeto para 4:1, ou gerar um tamanho sob medida com `python3 gerar.py --resposta 512x256`, que cria `variantes/sob_medida_512x256/`.
- Todos os quadros de uma sequência precisam ter o mesmo tamanho, senão a importação falha. Por isso não misture pastas.

**2) Sombra (vale fazer: melhora muito a leitura).** O branco puro tingido de amarelo ou ciano some em fundo claro (veja o painel 3 do `previa.png`). Por isso existe `variantes/com_sombra/`: as mesmas artes, com uma sombra preta suave.
- Importe `variantes/com_sombra/respostas_grana/grana_06.png` numa bolha e olhe o Preview.
- Se a sombra aparecer **escura**, o template multiplica a cor. Nesse caso use **com_sombra para tudo**: título, rótulos e respostas.
- Se a sombra aparecer **colorida, como um borrão** da mesma cor do texto, fique com a versão principal, branca pura.
- Para texturas quadradas: `variantes/quadrado_512_com_sombra/`.
- Na versão com sombra a letra das respostas é 47,5 px, 2 px menor, para a sombra caber sem cortar.

## O que NÃO entra (ou só entra se precisar)

| Arquivo | Uso |
|---|---|
| `reservas/reserva_<bolha>_01/02.png` (512×128) | Só se alguma frase for vetada. Troque 1 por 1, dentro da mesma bolha. O jeito certo é mudar a frase no `textos.json` e rodar `gerar.py`. Às pressas, renomeie a reserva com o nome do arquivo vetado (ex.: `reserva_grana_01.png` → `grana_07.png`). |
| `variantes/bolha_inteira/bolha_inteira_<bolha>.png` e `bolha_vazia.png` (512×512) | Nosso desenho de bolha: aro, brilho em meia-lua e 2 bolhinhas. Use só se o template deixar trocar a arte da bolha **fora** da pasta "DO NOT REMOVE!!! Main Assets" (a confirmar). Ajuda a fugir do visual padrão do template. **Nunca mexa nessa pasta.** |
| `variantes/rotulos_sem_icone/` (512×256) | Rótulos só com a palavra, caso o ícone fique apertado dentro da bolha. |
| `icone_grande_512.png` | O ícone em tamanho grande, só para referência e divulgação. |
| `previa.png` | Folha de conferência: todas as artes, simulação em 4 fundos e o ícone em 162, 96 e 64 px. |
| `gerar.py` | O script que gera tudo. |

## Originalidade e regras

- Fonte: **Inter Display Black**, licença OFL. O texto já vem desenhado no PNG.
- Ícones (coração, moeda com "$", bola, carro genérico de lado) e brilhos são desenhos geométricos próprios. Não têm marca, time, escudo, cor de torcida nem modelo de carro.
- Nada de "Pix", aposta, bebida, @ ou link nas artes.
- O vídeo demo 9:16 não é imagem gerada aqui. Ele é gravado na tela do celular durante o "Preview in TikTok".

## A confirmar no app

1. Tamanho e proporção das texturas originais de resposta, rótulo e título.
2. Se o template multiplica a cor (decide entre `com_sombra` e principal).
3. Se o rótulo continua aparecendo quando a bolha estoura. Na simulação do `previa.png` ele fica em cima da resposta.
4. Se dá para pôr a 4ª bolha (CARRO) sem quebrar o template.
5. Regra de nome e ordem dos arquivos na importação de sequência.
