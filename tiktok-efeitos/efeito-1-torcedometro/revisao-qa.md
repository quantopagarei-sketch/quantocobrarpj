# Revisão de QA: Torcedômetro (C01)

**Data:** 06/11/2026 · **Revisor:** Controle de Qualidade · **Resultado:** pronto para montar, depois que a coordenação publicar os arquivos (push + `PRONTO-PARA-MONTAR.md`).

## O que foi conferido

| Item | Resultado |
|---|---|
| Arquivos citados no `guia-montagem.md` existem em `assets/` | OK: titulo, titulo_toque, 26 cartas, 4 reservas, versões quadradas, 2 ícones |
| Dimensões | OK: título e cartas 512×256 RGBA, quadradas 512×512, ícones 162×162 (e 512×512 de referência) |
| Peso | OK: maior carta ~93 KB (limite 1 MB); 26 cartas ≈ 2,1 MB |
| Texto nas imagens (prévia, ícones, título, cartas 03, 08, 17, 19, 22, 23, 25) | Legível, sem corte, acentos e º certos |
| Fontes | Inter Display e Noto Color Emoji, as duas com licença OFL 1.1 |
| Marca, time, celebridade | Nada. Carros e celular genéricos (emoji Noto). Paleta sem par de cores de clube |
| Originalidade | O sorteio sobre a cabeça é uma mecânica comum. Os textos, os desenhos e o nome são próprios |
| Teste de sorteio da Parte 7.3 | Conta conferida por simulação: média de 11,6 cartas diferentes e chance de reprovar por azar de ~1,3% |
| Script TS (Plano C) | A lógica está coerente. Ainda não foi rodado no Effect House, e o guia já avisa isso |

## Correções feitas

1. **Carta 17:** "SOME DO GRUPO / SE PERDE" virou **"SOME DO GRUPO / NA DERROTA"**, porque "se perde" era ambíguo. Atualizei `textos.json` (v1.1, registro em `trocas_feitas_no_conceito`), `textos.md` e o checklist do guia (Parte 7.2), e rodei `assets/gerar.py` de novo. Só mudaram `carta_17.png`, `quadrado_512/cartas/carta_17.png` e `previa.png`; as outras imagens ficaram idênticas, pixel por pixel.
2. **Guia, Parte 7.3:** a chance de reprovar por azar passou de "cerca de 1,5%" para "pouco mais de 1%", que é o valor da simulação. A versão do guia subiu para 1.1.
3. **`lancamento.md`:** entrou a seção 2.0, "Plano mínimo". Gravar o próprio rosto com o pai, em 2 momentos e com 8 dias de postagem, passa do que o Vini pediu. Agora a equipe pergunta uma vez só. Se ele não responder, vale o mínimo: Roteiros 1-A e 3-A, ~5 min, agendados. O Roteiro 2 virou sempre opcional. Também ficou anotado que o login do TikTok na web, se for preciso, entra no mesmo momento.

## Riscos que continuam (baixos)

- Hashtags com nome de campeonato (#libertadores, #copadobrasil, #brasileirao) só aparecem nas legendas, nunca no efeito. O risco é baixo.
- As cartas 14 (reza) e 23 (carreata) podem implicar com a revisão. As reservas R1 e R2 já estão prontas.
- Menus do Effect House a confirmar na versão instalada. O guia marca cada um.
