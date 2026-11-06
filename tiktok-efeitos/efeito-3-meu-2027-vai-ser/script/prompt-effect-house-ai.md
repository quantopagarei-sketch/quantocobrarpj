# Pedidos prontos para o assistente "Effect House AI" (C05, Meu 2027 vai ser)

**Para quem é:** o Montador ou quem estiver montando. Não é texto para o Vini.
**Quando usar:** só se algum passo do `guia-montagem.md` travar. O assistente existe a partir da versão 5.13 do Effect House. A disponibilidade por conta ou região **não foi confirmada**.
**Regra:** use o assistente para **destravar** um passo, sem mudar a ideia do efeito. Depois, confira tudo com os checklists da Parte 8 do guia.

O assistente entende inglês melhor, por isso os pedidos estão em inglês. Cole **um pedido por vez**. Antes de cada pedido, aperte **Ctrl+S**: se o assistente estragar algo, feche sem salvar e abra de novo.

---

## Pedido 1: configurar o template Future Life já aberto (Partes 5 e 7 do guia)

```text
This project is based on the "Future Life" template (soap bubbles with random answers). Please configure it without adding new features:

1. Do NOT delete, rename, move or edit anything inside the "DO NOT REMOVE!!! - Main Assets" folder.
2. The effect title object must use the texture "titulo" (white PNG, 2:1).
3. In the "Bubble_Titles" group: the Lover bubble title uses "bolha_amor", the Income one uses "bolha_grana", the Kids one uses "bolha_futebol" (white PNGs, 2:1). Keep the 2:1 ratio, no stretching.
4. The answers: the Lover bubble must use the texture sequence "seq_amor", Income uses "seq_grana", Kids uses "seq_futebol". Each sequence has 8 frames (indices 0 to 7), white text, 4:1 ratio (512x128). Update the three Animated Texture Player nodes and anything else that still points to the old sequences.
5. Make sure the random answer of each bubble can be any of the 8 frames (0 to 7) and never an empty frame. If a Random node or a constant still uses the old frame count, update it.
6. Keep the random color logic (Start -> For_Colors) and keep the nodes in the "Remove these if you use images" comment box, because my answers are white text.
7. Keep both triggers: screen tap and mouth pout.

Do not add sound, music, text objects, generative AI or segmentation. List every change you made.
```

## Pedido 2: tirar a IA generativa do template (Parte 6 do guia)

```text
This project is based on the "Future Life" template. It has a "Generative Effects" group with two generative effects (Pucker and Unhappy). I need the effect to use NO generative effects at all, because of performance and because the effect must not be an AI effect.

Please remove or fully disable the Pucker and Unhappy generative effects so they never run, and fix any Visual Scripting node that referenced them, so the rest of the logic keeps working exactly as before: bubbles appear, the tap or the mouth pout pops them, and each bubble shows a random answer.

Do not touch the "DO NOT REMOVE!!! - Main Assets" folder. Do not change the bubbles, titles, colors or answers. Tell me exactly what you removed or reconnected.
```

## Pedido 3: montar do zero (Plano B, se o template Future Life não existir)

```text
Build a simple 2D "my 2027 prediction" effect from scratch, for 1 person:

- Screen images (not following the face), for a 9:16 screen:
  "Titulo": texture "titulo" (2:1), top center.
  Three closed bubbles in a row under the title, left to right: "Bolha_Amor" (texture "bolha_inteira_amor"), "Bolha_Grana" ("bolha_inteira_grana"), "Bolha_Futebol" ("bolha_inteira_futebol"). All 512x512, same size.
  Three open bubbles in the same places: "Aberta_1", "Aberta_2", "Aberta_3" (texture "bolha_vazia").
  Three answers centered on the open bubbles: "Resposta_1" (texture sequence "seq_amor"), "Resposta_2" ("seq_grana"), "Resposta_3" ("seq_futebol"). Keep the 4:1 ratio of the answers, width about 90% of the bubble.
- Give each bubble a fixed color with the Image color: Amor #FF4F8B, Grana #FFB020, Futebol #2EC27E (the open bubble of each column uses the same color). Keep the title and the answers white.
- On effect start and on video record start: show the title and the three closed bubbles; hide the open bubbles and the answers.
- On screen tap OR mouth pout (begin): hide the closed bubbles; show the open bubbles and the answers. Each answer shows one random frame of its own sequence (0 to 7), chosen at that moment, and stays still.
- A new tap or pout after the result picks new random answers.
- Use Visual Scripting (Start, Screen Tap, Facial Movement Detection with Mouth Pout, Set Visibility) or a TypeScript component, whichever is more reliable in this version.

Do not add sound, generative AI or segmentation. Explain what you built and how to test it in the Preview panel.
```

## Pedido 4: adaptar o script pronto (Plano C)

Use se o script `SorteioRespostas2027.ts` (nesta mesma pasta) der erro ao compilar na sua versão.

```text
I have a TypeScript component script (APJS) that picks a random frame for 3 or 4 texture sequences and keeps each one still on that frame. It fails to compile or run in this Effect House version. Please fix it for the current APJS API, keeping the same behavior:
- On start, on screen tap (touch began), on mouth pout (only when the pout begins) and on video record start: for each sequence, pick a random frame different from the current one and keep the sequence paused on it.
- A delay (atrasoSegundos) between the trigger and the pick, and a minimum interval (intervaloMinimo) between two picks.
- It must not show, hide or recolor anything.
Inspector fields: respostasBolha1, respostasBolha2, respostasBolha3, respostasBolha4 (texture sequences; the 4th can be empty), sortearNoToque, sortearNoBiquinho, sortearAoGravar (booleans), atrasoSegundos, intervaloMinimo (numbers).
Here is the script and the error message:
[cole aqui o conteúdo do arquivo e a mensagem de erro]
```

## Pedido 5 (opcional): 4ª bolha CARRO (Parte 17.2 do guia)

Só numa **cópia** do projeto, depois que a versão de 3 bolhas passou em todos os testes.

```text
This project is based on the "Future Life" template and already works with 3 bubbles. In this copy, please add a 4th bubble that works exactly like the other three:
- label texture "bolha_carro" (2:1, white), answers from the texture sequence "seq_carro" (6 frames, indices 0 to 5, 4:1, white);
- the same rise, pop, random color and random answer logic as the other bubbles, triggered by the same tap or pout;
- rearrange the 4 bubbles so they fit on a 9:16 screen without overlapping each other or the title, and keep the answers readable.
Do NOT delete, rename or edit anything inside the "DO NOT REMOVE!!! - Main Assets" folder. Do not add generative AI, sound or segmentation. List every object and node you added or changed.
```

---

**Anote no relatório** (`relatorio-montagem.md`) qual pedido usou, o que o assistente mudou e se os checklists da Parte 8 do guia passaram depois.
