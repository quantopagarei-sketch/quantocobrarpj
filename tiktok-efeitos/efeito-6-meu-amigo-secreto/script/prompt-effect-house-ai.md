# Pedidos prontos para o assistente "Effect House AI" (C06, Meu amigo secreto)

**Para quem é:** para o Montador ou para quem estiver montando. Não é texto para o Vini.
**Quando usar:** só se algum passo do `guia-montagem.md` travar. O assistente existe a partir da versão 5.13 do Effect House. Se ele funciona nesta conta, o `reconhecimento.md` (item 3) diz.
**Regra:** use o assistente para **destravar** um passo. Ele não pode mudar a ideia, os textos, as imagens, a posição já testada nem o tamanho. Depois, refaça os checklists da Parte 8 do guia.
**Atenção:** nenhum pedido manda enviar o efeito. O envio do C06 é **entre sexta, 20/11, e terça, 24/11/2026**, pelas Partes 12 e 13 do guia. Se o assistente oferecer "Submit" ou "Publish", recuse.

O assistente entende inglês melhor, por isso os pedidos estão em inglês. Cole **um pedido por vez**. Os nomes de asset usados aqui são os que o guia manda criar: `amigo_titulo` (título) e `cartas_amigo` (sequência de 26 quadros). As imagens antigas do C01 ficam com o prefixo `ANTIGO_` (Parte 3.1 do guia).

Dois detalhes do desenho que o assistente precisa saber (estão nos pedidos):
- a **régua** contra imagem esticada é o **ilhós**, o furinho dourado na ponta esquerda da etiqueta. Ele tem que continuar redondo. O miolo dele é transparente de propósito;
- a peça **não é simétrica**: a caixa e o texto ficam uns 18 px à direita do centro da imagem. A imagem é que fica centralizada na cabeça, e ninguém deve "corrigir" isso.

---

## Pedido 1: trocar as imagens na cópia do projeto do C01 (Partes 3 a 5 do guia)

```text
This project is a copy of a working "Randomizer 2D" head randomizer. I only need to swap its images. Do not change positions, scales, sizes, the randomizer logic, the play mode or the frame rate.

1. The object "Title" must show the texture "amigo_titulo" (512x256 PNG, transparent background).
2. The object "RandomAnimationSequence" must play the texture sequence "cartas_amigo" (26 frames, 512x256 each, carta_01 to carta_26, in this order). Put it wherever the old sequence was assigned (Animation Sequence component or the Image texture). If there is a script component "TorcedometroController", set its "sequenciaCartas" field to "cartas_amigo" too.
3. Find every remaining reference to the old assets whose names start with "ANTIGO_" (in components, scripts and Visual Scripting subgraphs), replace it with the matching new asset, and then delete the "ANTIGO_" assets.
4. Keep TapToSpin = on, TimeToSpin = 2, TitleFadeOutTime = 0.3, and the frame count at 26.

The new images are gift tags with a small round gold eyelet on the left tip. The eyelet has a transparent hole on purpose, and the drawing sits about 18 px to the right of the image center on purpose. Do not move or re-center anything because of that.

Do not add sound, text objects, animations, generative AI or segmentation. Do not submit or publish the effect. Tell me every change you made and anything you could not find.
```

## Pedido 2: configurar o template Randomizer 2D do zero (Plano B1)

```text
This project is based on the "Randomizer 2D" template. Please configure it, without adding new features:

1. The object "Title" must show the texture "amigo_titulo" (512x256 PNG, transparent background).
2. The object "RandomAnimationSequence" must play the texture sequence "cartas_amigo" (26 frames, 512x256 each, carta_01 to carta_26, in this order). Make sure the sequence is assigned in the right place (Animation Sequence component or the Image texture, whichever this version uses) and that all 26 frames are used.
3. Both images are 2:1 (width = 2 x height). Set the image size of both objects to a 2:1 ratio so nothing is stretched (the small round gold eyelet on the left tip of the gift tag must stay a circle, not an oval), and give both objects exactly the same position and size. The width should be about 1.6 times the width of the head. Center the image on the head; the drawing is about 18 px to the right of the image center on purpose.
4. Both objects must follow the head (Face Sticker, Face 0 only) and sit just above the hair, without covering the eyes. The whole image, including the gift box on top and the eyelet on the left tip, must stay inside the screen.
5. In the randomizer subgraph: TapToSpin = on, TimeToSpin = 2, TitleFadeOutTime = 0.3. Keep TitleDelay and the frame rate as they are.
6. The effect must reset to the title when the effect starts and when video recording starts.
7. The final card must be random among all 26 frames. If it is not, set the sequence play mode to Shuffle.

Do not add sound, text objects, animations, generative AI or segmentation. Do not submit or publish the effect. Tell me every change you made.
```

## Pedido 3: montar tudo do zero (se não houver template; Planos B2 e B3)

```text
Build a simple 2D head randomizer from scratch:

- Two Face Sticker objects that follow the head (Face 0), placed just above the hair:
  "Titulo" shows the texture "amigo_titulo" (512x256, 2:1);
  "Cartas" shows the texture sequence "cartas_amigo" (26 frames, 512x256, 2:1, carta_01 to carta_26 in this order).
  Same position and size for both; keep the 2:1 ratio (no stretching: the small round gold eyelet on the left tip of the gift tag must stay a circle); about 1.6 times the head width; image centered on the head; fully inside the screen, including the gift box on top.
- On effect start and on video record start: show "Titulo", hide "Cartas".
- On screen tap (only when no spin is running): hide "Titulo" (fade out in 0.3 s if possible), show "Cartas" and cycle random frames for 2 seconds, then stop on one random frame (index 0 to 25, uniform). Store the random index in a variable before using it, so the same value is used everywhere. The stopped card must stay still and keep following the head.
- A new tap after the result spins again. Taps during the spin are ignored.
- Prefer the built-in Interactions (for example "Tap Screen to Play Animation Sequence Then Delay Pause" and "Tap Screen to Delay Show/Hide Object") or Visual Scripting. Use a TypeScript component script only if that is more reliable in this version.

Do not add sound, text objects, animations, generative AI or segmentation. Do not submit or publish the effect. Explain what you built and how to test it in the Preview panel.
```

## Pedido 4: consertar o script do Plano C

Use se o script `TorcedometroController.ts` (copiado de `efeito-1-torcedometro\script\`, sem mexer no original) der erro ao compilar ou rodar nesta versão.

```text
I have a TypeScript component script (APJS) for a head randomizer. It fails to compile or run in this Effect House version. Please fix it to work with the current APJS API, keeping the same behavior:
title visible at start and on record start; on tap, fade the title in 0.3 s, then cycle random frames of a texture sequence for 2 s (slowing down) and stop on a random frame; a new tap after the result spins again; taps during the spin are ignored.
Inspector fields: titulo (SceneObject with Image), cartas (SceneObject with Image), sequenciaCartas (Texture sequence, here "cartas_amigo" with 26 frames), tempoGiro (number), tempoSomeTitulo (number), girarDeNovoNoToque (boolean).
Do not submit or publish the effect.
Here is the script and the error message:
[cole aqui o conteúdo do arquivo e a mensagem de erro]
```

---

**Anote no relatório** (`relatorio-montagem.md`, seção do C06) qual pedido usou, o que o assistente mudou e se os checklists da Parte 8 do guia passaram depois.
