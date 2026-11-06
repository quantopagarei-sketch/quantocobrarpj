# Revisão de QA: Perrengue no volante (C09)

**Data:** 06/11/2026 · **Revisor:** Controle de Qualidade · **Resultado:** pronto para montar depois que a coordenação liberar o C09 na seção 2 do `PRONTO-PARA-MONTAR.md` (hoje ele ainda está em "Vem aí") e publicar os arquivos (push).

## O que foi conferido

| Item | Resultado |
|---|---|
| Arquivos citados no `guia-montagem.md` existem em `assets/` | OK: 10 cartas (só elas em `cartas/`), 4 extras, 4 reservas, 10 marcadores, 4 de interface, 4 títulos, as versões em `largo_512x256/` com a mesma estrutura, 2 ícones de 162 e 2 de 512. As contagens do PowerShell da Parte 0.4 batem. |
| Dimensões | OK: cartas, extras, reservas e títulos quadrados 512×512 RGBA; versão larga 512×256 RGBA; marcadores 256×256; etiquetas 512×128 e rótulos 256×128; ícones 162×162 (e 512×512 de referência). |
| Peso | OK: a maior imagem é a `cartas/carta_08.png`, com 149.148 bytes (limite 1 MB). As 10 cartas + título somam 1,30 MB (quadrada) ou 0,93 MB (larga). O pacote estimado fica bem abaixo de 5 MB (limite real: 8 MB). |
| `gerar.py` | Rodado de novo numa cópia: as 61 imagens saíram idênticas, byte a byte. O `__pycache__/` dentro de `assets/` é ignorado pelo `.gitignore` e não vai no zip. |
| Imagens abertas | `previa.png`, os 2 ícones (162 e 512), título, cartas 01, 02, 03, 05, 06, 07, 08 e 09, larga 07 e 09, extras 12 e 13 e reserva 03. Nada cortado, tudo legível, acentos certos (POÇA, NÃO, DÁ, ATRÁS, À TOA). O visual de placa de trânsito está caprichado e é diferente do efeito-1. |
| Ícones | Volante genérico com centro liso (nada parecido com emblema), sem texto. Nada do desenho cai na margem de 9 px fora da área segura de 144. |
| Português | Natural e atual. "Ranking" em vez de "rankeie" no efeito; "rankeia/rankear" só nas legendas e nos comentários, o que é normal em rede social. Os textos gaúchos ("bah", "tu") aparecem só no lançamento e na medida certa. |
| Marca, celebridade, time, modelo de carro, "Pix" | Nada no efeito, nos textos de envio nem nas legendas. "GPS" é nome genérico, e o mapa da carta 13 não lembra nenhum aplicativo. Carros desenhados sem grade, emblema ou placa. A bomba da reserva 03 é grafite, sem cor de rede de postos. Os nomes de campeonato aparecem só no cronograma interno do `lancamento.md`, nunca em hashtag nem no efeito. |
| Regras de conteúdo | Nada de bebida, velocidade, radar, multa ou racha. Nenhum estereótipo: "flanelinha" saiu na redação, e "mulher no volante" vai para o filtro de comentários. O lançamento manda gravar com o carro parado, desligado e sem a chave na ignição, e não incentiva o uso com prêmio. Venda e efeito ficam em vídeos separados. |
| Nome | "Perrengue no volante" tem 20 caracteres (limite 25), sem acento. Alternativas com 22 e 20. Unicidade (a confirmar): o tiktok.com está bloqueado daqui, e o guia manda conferir no Manage Effects e no INPI. |
| Datas | Envio até ter 17/11/2026. Os dias da semana do guia e do lançamento conferem (17/11 ter, 22/11 dom, 25/11 qua, 01/12 ter, 08/12 ter etc.). |
| Campos de envio (Parte 13.3) | Preenchidos com os textos reais: nome, hint, som "nenhum", challenge, trend e demo, mais descrição, tags e comentários caso algum desses campos apareça. Tudo bate com a ordem de 06/11 05:50 (ícone pelo Create icon, sem tags nem categoria no formulário 5.16). |
| Originalidade | O ranking às cegas é um formato comum no TikTok e o template é oficial. O que é próprio: o tema (perrengue de motorista em PT-BR), os 10 textos, todos os desenhos, o título e o nome. Não copia nenhum efeito famoso. |

## Correções feitas

1. **Rodízio fora do primeiro envio** (guia, Parte 9; `textos.md`; `textos.json`). Antes, se o teste com 14 imagens passasse no Preview, o guia mandava enviar o rodízio. Mas o próprio guia cita um relato em que o efeito **publicado** só mostrava as mesmas 10 imagens, mesmo funcionando no editor, e o Montador não consegue testar o efeito publicado. Agora o primeiro envio é **sempre** a versão padrão de 10. O rodízio pode ser testado e guardado, e a nuvem decide depois se ele entra como atualização.
2. **Template com 5 posições** (guia, Parte 4.4; `textos.json`). O plano A antigo era enviar com 10 cartas e 5 posições, que tem o mesmo risco de "mais imagens que posições". Agora são 5 cartas direto (01, 02, 07, 09 e 10), e o Pedido 4 do assistente só entra se a nuvem aprovar. Os textos de comentário passam a trocar também "e mais 8" → "e mais 3" e "10 original texts" → "5 original texts".
3. **Parte 13.1, desafio sem decisão:** o guia mandava parar e esperar, mas não dizia o que fazer no prazo final. Agora diz: se chegar ter 17/11 sem decisão e sem ordem nova sobre o C09, enviar com Challenge vazio (o C09 não está na lista de espera do desafio, que é de sorteios).
4. **Parte 12.1, nomes no Manage Effects:** o guia dava como "esperado" o Meu 2027 vai ser, que só é enviado em 03/12, e o Torcedômetro, que está parado esperando a decisão do desafio. Isso podia confundir a conferência da Parte 14. Agora o guia diz o que **pode** estar lá e manda só anotar.
5. **Parte 10, pacote entre 5 e 8 MB:** o guia não dizia se dava para enviar. Agora diz: dá, porque o limite é 8 MB. Antes, limpar e atualizar o número; se continuar entre 5 e 8, seguir e anotar (igual ao C01).
6. **Partes 0.6 e 8.2, versão larga:** as cartas de letra menor da versão 512×256 são outras, a 03 e a 07 (46 px). Antes, o guia só citava as da quadrada (09, 06, 04 e 05). Agora o checklist de leitura cobre as duas versões.
7. **Parte 11.2:** faltava o `-y` no primeiro comando do ffmpeg. Sem ele, se o `C09-demo.mp4` já existir, o ffmpeg para e pergunta se pode sobrescrever, e o Montador fica travado.
8. **Parte 17, troca no Plano B3:** os caminhos estavam ambíguos ("copie a reserva para `cartas\`"). Agora tudo está com caminho completo na pasta `largo_512x256`, inclusive a origem da reserva e a pasta `cartas_trocadas`.
9. **`lancamento.md`, 2.2:** dizia que a dica "Toque no número" aparece no efeito publicado. Mas o hint do formulário 5.16 é de lista, então o texto provável é "Toque na tela". O texto agora é genérico.
10. O guia subiu para a versão 1.1, e os textos para a 1.1.

As imagens não mudaram, então não foi preciso rodar o `gerar.py` no original. Rodei só para conferir.

## Riscos que continuam

- **Template sem confirmação (médio):** o Blind Rank, o número de posições, os nomes das propriedades, o Tap To Stop e o comportamento com 10 itens só foram vistos em resumos de busca. O guia marca cada um "(a confirmar na sua versão)" e tem planos B1, B2 e B3.
- **"Parecido demais com o template" (baixo a médio, a confirmar):** não achei regra oficial que reprove efeito de template com troca só de imagens. Aqui a troca é grande (10 cartas próprias e um título). A Parte 16 já diz o que fazer se vier esse motivo. Também fica a confirmar se efeito feito de template conta para o selo e para o programa.
- **Carro vermelho nas cartas 03 e 07 (com céu claro), 08 e 12 (baixo):** isso **não** é o par de cores de clube dominante. A moldura é grafite ou verde, e o texto é amarelo ou branco. Fica anotado porque o público vem da torcida do Inter. Se algum comentário ligar o desenho a um time, troca-se a cor do carro no `gerar.py`.
- **Carta 03 (baixo):** o carro aparece "pulando" a cratera. É desenho cômico, sem velocidade, mas pode implicar com a revisão de direção perigosa. A reserva R1 está pronta.
- **Rodada longa (baixo):** uma rodada leva de 30 a 40 s e a demo tem até 15 s. A Parte 11.2 junta os primeiros 9 s com os últimos 5 s.
- **Unicidade do nome e INPI (a confirmar):** o Montador confere nas Partes 12.1 e 12.2.

## Pendências que dependem do Vini

Nenhuma para montar ou enviar. Ele só é chamado se o login do Effect House cair (seção 0.7 do guia, com link direto) e, no lançamento, nos momentos de gravação que ele já tem (dom 22/11 e dom 29/11).
