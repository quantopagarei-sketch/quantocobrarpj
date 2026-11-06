# Pedidos prontos para o assistente "Effect House AI" (C09, Perrengue no volante)

**Para quem é:** para o Montador ou para quem estiver montando. Não é texto para o Vini.
**Quando usar:** só se algum passo do `guia-montagem.md` travar, ou no Plano B2 (Parte 18 do guia). O assistente existe a partir da versão 5.13 do Effect House. Se ele funciona nesta conta, está anotado no `reconhecimento.md`, item 3.
**Regra:** use o assistente para **destravar** um passo. Ele não pode mudar a ideia, os textos nem as imagens. Depois, refaça os checklists da Parte 8 do guia.

O assistente entende inglês melhor, por isso os pedidos estão em inglês. Cole **um pedido por vez**. Os nomes de asset são os que o guia manda usar:

| Asset no painel Assets | Arquivo de origem (dentro de `assets\`) |
|---|---|
| `carta_01` … `carta_10` | `cartas\` (512×512) **ou** `largo_512x256\cartas\` (512×256), a versão escolhida na Parte 2 do guia |
| `perrengue_titulo` | `titulo.png` (512×512) ou `largo_512x256\titulo.png` (512×256) |
| `posicao_01` … `posicao_10` | `marcadores\` (256×256), só se forem usados |
| `itens_seq` | sequência de 10 quadros feita de `largo_512x256\cartas\` (só no Plano B3 ou no Pedido 3) |

Antes de colar, troque `512x512` por `512x256` nos pedidos se a versão escolhida for a larga.

---

## Pedido 1: configurar o template Blind Rank já aberto (Partes 4 e 6 do guia)

```text
This project is based on the "Blind Rank" template. Please configure it without adding new features:

1. In the Visual Scripting property "Randomizer: Textures", replace all the food images with exactly these 10 textures, in this order: carta_01, carta_02, carta_03, carta_04, carta_05, carta_06, carta_07, carta_08, carta_09, carta_10 (PNG, 512x512, transparent background). The list must have exactly 10 elements. Remove any extra element.
2. The ranking must have 10 positions (1 to 10). If there is a property for the number of positions or items, set it to 10.
3. Each item must appear only once per round, in random order. If there is a play mode (Loop / Random / Shuffle), use Shuffle.
4. "Randomizer: Tap To Stop Randomizer" = off. The item stops by itself and the user only taps a number.
5. Keep "Randomizer: Wait Between Frames" and "Randomizer: Shuffle Time" as they are, unless an item spins for more than 3 seconds; in that case set the shuffle time to min 1 and max 2.
6. If there is an option that places the last item automatically in the last free position, turn it on.
7. Keep the item above the head (Head Tracker, first face only) and the 1-10 list on the 2D layer. Do not move them unless something is off-screen.
8. Delete the food textures from the Assets panel only if nothing references them anymore.

Do not add sound, generative AI or segmentation. Tell me every change you made and the original value of every property you changed.
```

## Pedido 2: pôr o título no topo da tela (Parte 5 do guia)

Use só se o template **não** tiver um objeto de título próprio.

```text
Add a 2D image at the top of the screen showing the texture "perrengue_titulo" (512x256 PNG, transparent background, 2:1 ratio).
- It must be drawn by the existing 2D camera of the Blind Rank template (the "2D Foreground" group), above everything else.
- Centered horizontally, about 60% of the screen width, with its top edge at about 10% of the screen height.
- Keep the 2:1 ratio (no stretching).
- It must not cover any number or item of the 1-10 list. If it does, make it smaller (not less than 50% of the screen width) or move it to the right, but keep its right edge inside 85% of the screen width.
- It stays visible during the whole game and does not react to taps.
Do not change anything else. Tell me the object name, its parent, position and size.
```

## Pedido 3: montar o ranking às cegas do zero (Plano B2: não há template Blind Rank)

```text
Build a simple "blind ranking" game from scratch, for one person (first face only):

- A 2D title at the top of the screen with the texture "perrengue_titulo" (512x256, 2:1, no stretching), about 60% of the screen width.
- A vertical list on the left side of the screen with 10 slots, numbered 1 (top) to 10 (bottom). Each slot shows its number image (posicao_01 ... posicao_10, 256x256). The list must fit between 18% and 80% of the screen height and stay inside the left 45% of the screen width.
- Above the head (it must follow the head), one item at a time from these 10 textures: carta_01 ... carta_10 (512x256, 2:1). Each round shows each item exactly once, in a random order (no repeats). Store the random index in a variable before using it, so the same value is used everywhere.
- When the person taps a free slot, the current item is placed next to that slot number (small, 2:1, readable) and the next item appears above the head. Taps on a slot that is already used do nothing.
- After the 10th item is placed, hide the item above the head. The full ranking stays on screen.
- When video recording starts, reset everything (empty list, new random order) if this version supports a "video record start" event.
- Prefer Visual Scripting. Use a TypeScript component script only if that is more reliable in this version.

Do not add sound, generative AI, segmentation or any text object. Explain what you built and how to test it in the Preview panel by clicking on the numbers.
```

## Pedido 4: mais itens que posições (rodízio de 14, ou template com 5 posições)

Só com o caso previsto no guia (Parte 9, rodízio opcional; ou Parte 4.4, template com 5 posições). **Não atrase o envio por causa deste pedido.** Troque `[N]` pelo número de itens e `[P]` pelo número de posições: rodízio = 14 itens e 10 posições; template de 5 posições = 10 itens e 5 posições.

```text
This project is based on the "Blind Rank" template. "Randomizer: Textures" has [N] textures, but the ranking has [P] positions.
Change the logic so that each round:
- picks [P] different textures at random from the [N] (no repeats in the same round, Shuffle-like);
- shows them one at a time above the head, as the template already does;
- ends after the [P]th choice, with the list of positions 1 to [P] filled and nothing shifted or duplicated;
- a new round (new recording or reopening the effect) picks a new random set.
Keep everything else (layout, images, timing, title). Do not add sound, generative AI or segmentation. Tell me every change you made, and how I can undo it.
```

## Pedido 5: textos em inglês que aparecem para quem usa (Parte 5.3 do guia)

```text
In this Blind Rank project, replace every piece of English text that the end user can see with these Portuguese texts, keeping position, size and style:
- tap instruction (for example "Tap to rank" or "Tap a number") -> "TOQUE NO NÚMERO"
- restart button or message (for example "Restart" or "Play again") -> "JOGAR DE NOVO"
- label next to position 1 (for example "Worst" or "Best") -> "PIOR"
- label next to position 10 -> "DE BOA"
If a text is an image, use these textures instead: etiqueta_toque, jogar_de_novo, rotulo_pior, rotulo_de_boa.
Remove or hide any editor tip or helper text (for example in a "Tip" group) that would be visible in the published effect.
List every text you found, what you changed, and anything you did not change.
```

---

**Anote no relatório** (`relatorio-montagem.md`, seção do C09) qual pedido usou, o que o assistente mudou (com os valores antigos) e se os checklists da Parte 8 do guia passaram depois.
