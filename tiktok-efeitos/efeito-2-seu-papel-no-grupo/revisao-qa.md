# Revisão de qualidade — Eu no grupo da família (C08)

**Nota final:** 8.5 · **Pronto para montar:** sim

## Problemas encontrados
- titulo.png: a borda branca externa do balão do título ia até a beirada do quadro de 512 px (alfa 147 nas colunas x=0 e x=511). O contorno e a sombra ficavam cortados em linha reta dos lados, o que pode aparecer na câmera como um corte duro ou um artefato de filtragem.
- Guia, Parte 12.2 (Challenge): mandava 'deixe vazio', mas o lancamento.md (seção 6) diz para selecionar um desafio ativo que combine. Os dois arquivos se contradiziam.
- Guia, Parte 15.2 (Plano B): apresentava como certo que 'From = To mostra só aquele quadro'. A documentação só confirma que os índices começam em 0. Faltava '(a confirmar)' e um plano alternativo.
- Guia, Parte 15.1: o caminho 'Hierarchy → + → Face Effects → Face Sticker' estava afirmado sem '(a confirmar)'. A pesquisa técnica trata o Face Sticker como componente, não como objeto.
- Guia, Parte 6: a documentação oficial descreve o TapToSpin de jeitos um pouco diferentes (a busca extended de hoje achou essa divergência). O guia não tinha um teste rápido para o caso de o comportamento vir invertido.
- Guia, Parte 4.2: o FPS de ~100 aparecia sem fonte. A busca de hoje confirmou: o tutorial oficial fala em 100 fps e num tempo de giro sorteado (±0,25 s). Agora está citado.
- lancamento.md 1.3: 'vídeo apagado não conta' estava marcado ✅, mas a pesquisa 02 (regras) diz explicitamente que isso não foi confirmado. Era uma contradição entre documentos.
- lancamento.md 1.4: dizia que não se sabe se os vídeos do próprio Vini contam, mas a pesquisa 02 resume os Termos do ECR dizendo que vídeos do próprio criador não contam para o pagamento.
- lancamento.md: o plano pedia o Vini em cerca de 9 dias de post (1 min cada) mais 2 momentos de gravação. Se o app não deixar agendar, isso vai contra o pedido dele de ser acionado só se MUITO necessário. Não havia um plano mínimo.
- lancamento.md 6.4: a sugestão de mandar o link no grupo da família real não tinha a ressalva sobre uso combinado ou incentivado, que é risco nos Termos do ECR.
- Bloqueio de logística: as pastas dos efeitos estão 'untracked' no git (não commitadas). O zip público do GitHub (repo público, link 302 OK) ainda NÃO contém este efeito, e o arquivo tiktok-efeitos/PRONTO-PARA-MONTAR.md não existe. O Montador fica parado até o coordenador publicar.
- Itens conferidos sem problema: os 33 arquivos citados no guia existem com as dimensões certas (título, 28 cartas e 3 reservas em 512×512 RGBA; ícones em 162×162 opacos). Todas as imagens têm menos de 121 KB, título + 28 cartas somam cerca de 2,95 MB (meta ≤ 5 MB). Os textos do JSON batem com os PNG e com a contagem de caracteres. O nome tem 22 caracteres e a bio tem 70. Não há texto cortado, erro de português, marca, time, celebridade ou visual de app de mensagem. O efeito não usa IA generativa nem segmentação. O formato (randomizer de 'papel no grupo') é um gênero comum, mas nome, frases e arte são originais.

## Correções feitas
- assets/gerar.py: o anel colorido e a borda externa do título ficaram mais finos (dilatação 20/30 → 12/20) para não encostar na beirada. Rodei o gerar.py de novo e todos os assets e a previa.png foram refeitos. Na beirada, o alfa do título caiu de 147 para cerca de 35, que é só sombra suave. Conferi visualmente o título, as cartas 02, 09, 13, 16, 20, 23, 24 e 27 e os 2 ícones.
- guia-montagem.md (v1.1): o campo Challenge agora diz para selecionar um desafio ativo de sorteio/humor, se houver, e anotar no relatório. Fica alinhado com o lancamento.md.
- guia-montagem.md: na Parte 15.2, a parte de 'From = To' ficou marcada (a confirmar), com a alternativa de usar a entrada Pause. Na Parte 15.1, o menu do Face Sticker ficou (a confirmar), com a alternativa Image 2D + Add Component → Face Sticker.
- guia-montagem.md, Parte 6: novo passo 8, um teste rápido do TapToSpin que manda inverter a marcação se o comportamento vier trocado e anotar no relatório.
- guia-montagem.md, Parte 4.2: o FPS de 100 e o tempo de giro sorteado (±0,25 s) agora citam o tutorial oficial. Na Parte 13, o prazo de revisão foi ajustado para '2 a 3 dias úteis; às vezes 1'.
- lancamento.md (v1.1): 'vídeo apagado não conta' passou de ✅ para ❓, mantendo a regra de nunca apagar. Vídeo privado continua ✅.
- lancamento.md: entrou um 'Plano mínimo' para o caso de não dar para agendar. O Vini passa a ter só 3 dias de post (D1, D3 e D6), e o Roteiro 2, as costuras e o Roteiro 1-B viram opcionais, decididos na Revisão 1.
- lancamento.md: entrou a ressalva de que no grupo da família real só se manda o link, sem pedir nem combinar quem posta. A nota sobre os vídeos do próprio criador foi corrigida com base nos Termos do ECR (pesquisa 02).
- Backup dos assets anteriores em /tmp/claude-0/-home-user-quantocobrarpj/97fcacc8-f478-5bbc-9659-8b19d0155dbf/scratchpad/assets_bak

## Pendências para o Vini
- Nenhuma nova para este efeito. O que já estava previsto continua igual: Effect House instalado e logado na conta Car Shop (download: https://effecthouse.tiktok.com/download ; login por QR com o scanner de dentro do app TikTok: https://effecthouse.tiktok.com/learn/guides/getting-started/introduction-to-effect-house/download-and-login).
- Depois da aprovação: 1 momento de gravação de uns 40 minutos com o efeito no celular (seção 2 do lancamento.md). Se o app deixar agendar, ele agenda tudo nesse mesmo momento. Se não deixar, vale o plano mínimo de 3 dias de post.
- Para a EQUIPE, não para o Vini: o coordenador precisa fazer commit e push da pasta tiktok-efeitos e criar o tiktok-efeitos/PRONTO-PARA-MONTAR.md. Sem isso, o zip https://github.com/quantopagarei-sketch/quantocobrarpj/archive/refs/heads/main.zip não traz este efeito e o Montador fica esperando.
