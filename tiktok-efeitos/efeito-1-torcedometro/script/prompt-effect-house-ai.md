# Pedido pronto para o assistente "Effect House AI" (C01, Torcedômetro)

**Para quem é:** para o Montador ou para quem estiver montando. Não é texto para o Vini.
**Quando usar:** só se algum passo do `guia-montagem.md` travar (Partes 4 a 6, ou o Plano B/C da Parte 15). O assistente existe a partir da versão 5.13 do Effect House. A disponibilidade por conta ou região **não foi confirmada**.
**Regra:** use o assistente para **destravar** um passo, sem mudar a ideia do efeito. Depois, confira tudo com os checklists da Parte 7 do guia.

O assistente entende inglês melhor, por isso os pedidos estão em inglês. Cole **um pedido por vez**.

---

## Pedido 1: ajustar o template Randomizer 2D já aberto

```text
This project is based on the "Randomizer 2D" template. Please help me configure it, without adding new features:

1. The object "Title" must show the texture "titulo_toque" (512x256 PNG, transparent background).
2. The object "RandomAnimationSequence" must play the texture sequence "cartas" (26 frames, 512x256 each, carta_01 to carta_26). Make sure the sequence is assigned in the right place (Animation Sequence component or the Image texture, whichever this version uses) and that all 26 frames are used.
3. Both images are 2:1 (width = 2 x height). Set the image size of both objects to a 2:1 ratio so nothing is stretched, and give both objects exactly the same position and size.
4. Both objects must follow the head (Face Sticker, Face 0 only) and sit just above the hair, without covering the eyes.
5. In the randomizer subgraph: TapToSpin = on, TimeToSpin = 2, TitleFadeOutTime = 0.3. Keep TitleDelay and the frame rate as they are.
6. The effect must reset to the title when the effect starts and when video recording starts.
7. The final card must be random among all 26 frames. If it is not, set the sequence play mode to Shuffle.

Do not add sound, text objects, generative AI or segmentation. Tell me every change you made.
```

## Pedido 2: montar do zero (se o template não existir ou estiver quebrado)

```text
Build a simple 2D head randomizer from scratch:

- Two Face Sticker objects that follow the head (Face 0), placed just above the hair:
  "Titulo" shows the texture "titulo_toque" (512x256, 2:1);
  "Cartas" shows the texture sequence "cartas" (26 frames, 512x256, 2:1).
  Same position and size for both; keep the 2:1 ratio (no stretching).
- On effect start and on video record start: show "Titulo", hide "Cartas".
- On screen tap (only when the title is visible): fade "Titulo" out in 0.3 s, then show "Cartas" and cycle random frames for 2 seconds, slowing down at the end, then stop on one random frame (index 0 to 25, uniform). The stopped card must stay still and keep following the head.
- A new tap after the result spins again. Taps during the spin are ignored.
- Use Visual Scripting or a TypeScript component script, whichever is more reliable in this version.

Do not add sound, text objects, generative AI or segmentation. Explain what you built and how to test it in the Preview panel.
```

## Pedido 3: adaptar o script pronto (Plano C)

Use se o script `TorcedometroController.ts` (nesta mesma pasta) der erro ao compilar na sua versão.

```text
I have a TypeScript component script (APJS) for a head randomizer. It fails to compile or run in this Effect House version. Please fix it to work with the current APJS API, keeping the same behavior:
title visible at start and on record start; on tap, fade the title in 0.3 s, then cycle random frames of a texture sequence for 2 s (slowing down) and stop on a random frame; a new tap after the result spins again; taps during the spin are ignored.
Inspector fields: titulo (SceneObject with Image), cartas (SceneObject with Image), sequenciaCartas (Texture sequence), tempoGiro (number), tempoSomeTitulo (number), girarDeNovoNoToque (boolean).
Here is the script and the error message:
[cole aqui o conteúdo do arquivo e a mensagem de erro]
```

---

**Anote no relatório** (`relatorio-montagem.md`) qual pedido usou, o que o assistente mudou e se os checklists da Parte 7 do guia passaram depois.
