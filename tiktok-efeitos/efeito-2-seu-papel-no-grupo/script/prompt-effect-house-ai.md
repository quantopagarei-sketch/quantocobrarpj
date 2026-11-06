# Pedido pronto para o assistente "Effect House AI" (C08)

**Para quem é:** o Montador. O Vini não precisa usar.
**Quando usar:** só se o template Randomizer 2D não existir, não funcionar, ou se um passo do `guia-montagem.md` travar. O caminho principal continua sendo o guia.
**Onde fica o assistente:** dentro do Effect House 5.13 ou mais novo, com o nome "Effect House AI" (antes se chamava "Ask AI"). O lugar exato do botão e a disponibilidade por conta ou região ainda precisam ser confirmados.

## Por que não há script em TypeScript aqui

O Effect House aceita scripts `.ts` (classe com `@component()` que estende `APJS.BasicScriptComponent`). A equipe, porém, não conseguiu confirmar na documentação os comandos para ler o toque na tela, trocar o quadro de uma sequência e saber qual rosto está na tela. Um script escrito no escuro poderia não compilar e tomaria mais tempo do Montador do que o template. Este efeito funciona só com o template e o Visual Scripting.

## Como usar

1. Abra o assistente Effect House AI.
2. Cole **um bloco por vez**, começando pelo Bloco 1.
3. Antes de passar ao bloco seguinte, confira o resultado no Preview.
4. No fim, confira tudo com os checklists das Partes 7 e 8 do guia.
5. Se o assistente propuser algo fora da ideia (outras frases, música, IA generativa, logo), **recuse**.

Os pedidos estão em inglês porque o programa é em inglês.

---

### Bloco 1: cena e imagens

```
I am building a head randomizer effect. Please set it up step by step and tell me what you changed.

Assets already imported in this project:
- "titulo" : a 512x512 transparent PNG (title speech bubble).
- "cartas_grupo" : a Texture Sequence with 28 frames, 512x512 each (the 28 possible results, frame 0 to frame 27).

Scene I need:
1. A Face Sticker object named "Titulo" that follows face 0, showing the "titulo" texture above the head.
2. A Face Sticker object named "Cartas" that follows face 0, with an Animation Sequence component using "cartas_grupo".
3. Both objects must have exactly the same 2D Transform, keep a 1:1 aspect ratio (no stretching), be horizontally centered on the head, and sit just above the hair. The bubble tail tip is at about 90% of the image height, so the bottom 10% of each image is transparent margin. Width about 1.5x the head width.
Do not add music, generative AI, segmentation or any other heavy feature.
```

### Bloco 2: lógica

```
Now create the Visual Scripting logic, using only standard nodes:
1. On Start: "Titulo" visible, "Cartas" hidden.
2. On Screen Tap: hide "Titulo", show "Cartas", play the "Cartas" Animation Sequence looping through all frames (From 0 To 27) for 2.5 seconds, then stop on ONE random frame between 0 and 27 and keep showing only that frame.
3. The random frame must be generated once and reused (the Random node returns a new value every time it is read), so prefer an Index Generator in Shuffle mode, or store the value in a variable before using it for both From and To.
4. Ignore taps while it is spinning.
5. Turn "Reset on Record" On, so pressing the TikTok record button brings the title back.
```

### Bloco 3: versão de 2 pessoas (só depois que a de 1 pessoa funcionar)

```
Now add a second, independent randomizer for a second person:
1. Duplicate "Titulo" and "Cartas" as "Titulo_B" and "Cartas_B". Set their Which Face to face 1 ONLY (face 0 unchecked). Keep the originals on face 0 ONLY.
2. Duplicate the tap logic for the _B objects, with its own random index, so both people usually get different results. One tap must spin both.
3. When only one face is visible, nothing of the _B objects may appear on screen.
Tell me how to test this with the two-person preview media.
```

---

## O que conferir depois do assistente

- 28 quadros na sequência, nenhum esticado (o círculo do emoji tem que estar redondo).
- Toque faz girar; para em carta aleatória (teste de 15 sorteios, Parte 7.3 do guia).
- Com 2 rostos, cada um ganha a sua carta e os resultados não andam "grudados" (Parte 8.5).
- Com 1 rosto, não aparece balão flutuando.
- Tamanho do pacote ≤ 5 MB e **Test performance** aprovado (Parte 9).
