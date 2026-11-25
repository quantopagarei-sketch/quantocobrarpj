# Reels – Agente especialista em Reels da página "Black Achadinhos" (manual e diário)

Pedido do Vini em 22/11/2026: "um agente especialista em Reels que leva pro Telegram, pra postar no Facebook da página; vídeo com as
promos, diário; vocês fazem tudo, da criação à postagem; pesquisem as melhores ofertas com as melhores comissões".
Objetivo: **1 Reel por dia** na página, com 3 ou 4 ofertas do dia, para levar gente ao canal do Telegram (2 inscritos em 22/11).
**Quem faz (desde 24/11): o Divulgador Facebook (tarefa das 20h31), dentro da própria sessão dele**: depois dos posts e stories da
página e antes dos grupos e do "terminei" (bloco REEL DO DIA no topo de `facebook.md`). O Reel sai por volta das 21h; PC ligado até ~21h45.
Por quê: a tarefa separada das 21h47 (`trig_01267ib4c8Y1G7Shb7r4FbBf`, criada em 22/11) NÃO consegue gravar no repositório: o push dá 403
("repositório fora da lista autorizada desta sessão") e, sem push, não há trava da Meta nem registro. Ela não postou em 22 nem em 23/11.
**Se você é essa tarefa das 21h47 ("Telegram Ofertas: Reels"): não faça nada e termine com a linha "O Reel é do Divulgador Facebook".**
Este agente NÃO fala com o Vini. Problema que depende dele: linha "PARA O DIRETOR (Reels): ..." em `diario.md` e fim.
Vale mais que este arquivo: `juridico.md` (capítulo REELS) e as seções TRAVA e REGISTRO do `LEIA-PRIMEIRO.md`.

## Portões (antes de qualquer coisa)
1. `git pull`. Escreva em `diario.md` "DD/MM HH:MM Reels: comecei" e dê push (regra REGISTRO).
2. Já existe Reel de HOJE em "Feito" (fim deste arquivo)? Então anote "Reels: já postado hoje" e termine. É 1 por dia.
3. Aviso do Facebook nos últimos 3 dias (`facebook.md` > Avisos, ou "Avisos" aqui embaixo)? Não poste: anote e termine.
4. Chrome do PC sem resposta, ou Facebook pedindo login, código ou captcha: anote "PARA O DIRETOR (Reels)" e termine.
   Nunca digite senha nem código, nunca resolva captcha.

## Passo 1 – Escolher 3 ou 4 ofertas (as que mais vendem e mais pagam)
**CINTA SEMPRE (ordem do Vini, 22/11/2026 20h35: "o Reels tem que ter a cinta sempre")**: todo Reel leva a Cinta Modeladora
Opta Corpus (MLB-4810647054, a que mais vende no projeto) como uma das 3 ou 4 ofertas. Ela não segue a regra dos 7 dias sem repetir.
- Fica em 1º lugar se tiver o maior desconto; senão, em 2º. As outras 2 ou 3 vagas seguem os critérios abaixo.
- Ela precisa estar no canal nas últimas 24 h (o Curador põe todo dia; ver `curador.md` > CINTA TODO DIA). Se não estiver, ou se na
  conferência (passo 2) sumir o riscado, acabar o estoque ou o desconto cair abaixo de 20%: use a reserva da "família da cinta" que
  estiver no canal (cinta shorts Shaper MLB-6171656788, macaquinho modelador MLB-5046520966) e anote no "Feito" "sem cinta: motivo".
  Se a cinta ainda não saiu no canal quando você chegar aqui (o Curador solta por volta das 20h40), espere até 10 min (`git pull` e
  `candidatas.py` de novo) antes de ir para a reserva.
- Texto e foto: só a foto do produto (sem corpo de modelo, sem antes e depois); nunca "emagrece", "perca X cm" ou promessa de corpo.
  Pode: "cinta modeladora", "com barbatanas", nota e vendidos da página.
`python3 reels/candidatas.py` lista as ofertas JÁ POSTADAS no canal nas últimas 24 h e ainda não usadas em Reel (7 dias).
Só entram ofertas que já estão no canal, porque o vídeo manda a pessoa procurar o link lá.
Escolha 4 (3 se faltar), nesta ordem de peso:
1. Desconto real com preço riscado na página (quanto maior, melhor; abaixo de 20% não entra).
2. Comissão: veja o selo "GANHOS" / "GANHOS EXTRAS" na página (passo 2) e a linha do dia em `curador.md`. Prefira 12% ou mais.
3. Compra por impulso e apelo amplo: até ~R$ 300, muita venda (+10 mil), nota 4,6+. No máximo 1 produto caro (celular) por vídeo.
4. Variedade: no máximo 2 da mesma categoria; misture casa, beleza, ferramentas, moda, eletrônicos.
A 1ª oferta do vídeo é a de MAIOR desconto (é ela que segura quem está rolando a tela).
Nenhuma candidata: sem Reel hoje; registre e termine (não invente oferta fora do canal).

## Passo 2 – Conferir cada oferta AGORA (preço, riscado, nota, vendidos, comissão)
Abra a `pagina` da oferta (endereço normal; NUNCA o link de afiliado) no Chrome e rode este trecho com `javascript_tool`:
```js
(() => { const q=s=>document.querySelector(s); const t=s=>(q(s)?.innerText||'').replace(/\s+/g,' ').trim();
const b=document.body.innerText; const i=b.indexOf('GANHOS'); const pc=q('.ui-pdp-price__main-container')||q('.ui-pdp-price');
return JSON.stringify({titulo:t('h1.ui-pdp-title'), preco:t('.ui-pdp-price__main-container')||t('.ui-pdp-price'),
sub:t('.ui-pdp-subtitle'), nota:t('.ui-pdp-review__rating'), ganhos:i>=0?b.slice(i,i+40).replace(/\s+/g,' '):'',
meliplus:/meli\+|meliplus|loyalty/i.test(pc?.outerHTML||''), pix:/pix/i.test(pc?.innerText||''),
hora:new Date().toLocaleString('pt-BR')}) })()
```
O campo `preco` vem como "R$ 219 , 99 R$ 59 , 99 72% OFF ...": 1º = riscado ("de"), 2º = preço atual ("por").
- Preço mudou: use o de AGORA. Sumiu o riscado, ou o desconto caiu abaixo de 20%: troque de oferta.
- `pix` verdadeiro: ponha `"pix": true` no roteiro (o vídeo escreve "no Pix"). `meliplus` verdadeiro: esse preço é só de assinante;
  use o preço "em outros meios" da página ou troque de oferta.
- Oferta relâmpago com cronômetro, estoque acabando ou anúncio pausado: troque de oferta.
- Guarde a hora do PC (campo `hora`): ela vai no vídeo e na legenda ("22/11 às 13h41").
Lote do Chrome (`browser_batch`): só páginas do MESMO site por lote (`www.mercadolivre.com.br` e `produto.mercadolivre.com.br`
são sites diferentes). Não devolva endereço com "?" no resultado do trecho (o ambiente bloqueia).

## Passo 3 – Fotos (o servidor não baixa do Mercado Livre: a foto vem por print do Chrome)
Para cada oferta, na mesma aba: abra a `imagem` trocando "D_NQ_NP_" por "D_NQ_NP_2X_" e "-O.jpg" por "-F.jpg"; depois
`computer` > `hover` em (1562, 746) (tira o mouse de cima) e `computer` > `zoom` com `region [0, 0, 1568, 751]` e
`save_to_disk: true`, SEM `scale` (com `scale` o arquivo sai pequeno). O resultado mostra "Image source: /tmp/claude-tool-results/...png":
copie esse arquivo para a pasta de trabalho como `foto1.png`, `foto2.png`... As fotos são todas de `http2.mlstatic.com`: cabem num lote só.
O gerador recorta sozinho o fundo escuro do print. Use sempre a foto principal do anúncio, sem editar.

## Passo 4 – Roteiro (arquivo JSON na pasta de trabalho, ao lado das fotos; ex.: /home/claude/reel/roteiro.json)
```json
{"data": "2026-11-22", "conferido": "22/11 às 13h41", "ofertas": [
 {"id": "20261122-03", "nome": "Pisca-pisca cascata de Natal 400 LEDs", "nome_legenda": "Pisca-pisca cascata de Natal, 400 LEDs, 10 m",
  "preco": 59.99, "preco_de": 219.99, "info": "4,7★ · +10 mil vendidos", "foto": "foto1.png", "comissao": "20%"}]}
```
- `nome`: até ~45 letras, claro, sem MAIÚSCULAS gritadas (aparece em 2 linhas no vídeo). `nome_legenda`: versão um pouco mais completa.
- `preco` e `preco_de`: os da página agora. Sem riscado na página = sem `preco_de`. `info`: nota e vendidos da página.
- `comissao` é só para o registro (não aparece no vídeo). `"pix": true` quando o preço em destaque é só no Pix.
- 3 ou 4 ofertas. O "até X% OFF" da abertura e os "-X%" são calculados pelo gerador, arredondando para BAIXO (como o Mercado Livre).

## Passo 5 – Gerar e conferir
1. `python3 reels/fazer_reel.py --roteiro PASTA/roteiro.json --saida PASTA/saida --quadros` (1 segundo). Abra `saida/conferencia.jpg` (Read).
2. Conferência visual: nada cortado nem sobreposto; nome legível; preços, "de" riscado e "-X%" iguais ao roteiro; foto certa em cada
   produto; aviso "Publicidade · links de afiliado" no topo de todas as telas; tela final com "Blackachados" e a data e hora da conferência.
3. `python3 reels/fazer_reel.py --roteiro PASTA/roteiro.json --saida PASTA/saida` (uns 25 segundos). Tem que terminar com "OK reel.mp4"
   e menos de 3,6 MB (o envio de arquivo pelo Chrome aceita no máximo 3,8 MB; o gerador comprime sozinho se passar).
4. Saem prontos: `reel.mp4`, `legenda.txt` (copie como está) e `comentario.txt` (opcional; hoje não usamos).

## Passo 6 – Checklist jurídico (todos "sim", senão não posta; detalhes em juridico.md > REELS)
- A cinta (ou a reserva da família dela) está no vídeo, só com foto do produto e sem promessa de corpo ou de emagrecer?
1. Vídeo feito por nós hoje, com produtos e textos diferentes dos últimos dias? 2. Preços, riscado e % conferidos na página agora?
3. Aviso de publicidade no vídeo e na 1ª linha da legenda? 4. Data e hora da conferência e "podem mudar" na legenda?
5. "Canal independente (não oficial)" na legenda e na tela final? 6. Nenhum logo do Mercado Livre ou de marca desenhado à parte?
7. Foto só do anúncio, sem rosto de pessoa? 8. Só a trilha do gerador (nenhuma música comercial, nenhuma voz)?
9. Nada de "comente", "marque amigos", "só hoje", "últimas unidades", contagem regressiva? 10. Sem link e sem "@" na legenda?
11. Nenhum produto proibido (adulto, armas, remédio/suplemento, cigarro, álcool, apostas)?

## Passo 7 – Postar (TRAVA da Meta: 1 acesso por vez)
1. TRAVA: se você é o Divulgador Facebook e a sua linha "Facebook: comecei (Facebook em uso)" de hoje está aberta, a trava já é sua:
   pule este item. Qualquer outro caso: `git pull`; se houver "comecei (… em uso)" de HOJE sem "terminei", espere 10 min e confira de
   novo (até 3 vezes); continuou ocupado: anote "Reels adiado (Meta em uso)" e termine. Livre: escreva "DD/MM HH:MM Reels: comecei
   (Facebook em uso)" e dê push.
2. Abra https://www.facebook.com/blackachadinhos.ofertas . Se aparecer "Troque para a Página de Black Achadinhos" com o botão
   "Trocar agora", clique nele (`find` + ref) e espere 5 s. Confira que o Facebook está COMO A PÁGINA (foto do canto superior direito =
   logo preto e amarelo; o botão "Trocar agora" sumiu). O perfil pessoal do Vini NUNCA posta.
3. Abra https://www.facebook.com/reels/create . `find` "file input" (fica escondido) e envie `reel.mp4` com
   `mcp__claude-in-chrome__file_upload` (origin `https://www.facebook.com`; sozinho, fora de lote). Espere ~5 s: aparecem a prévia,
   "Mídia carregada" e, embaixo, "Você pode publicar seu reel!" (enquanto estiver "Verificando conteúdo protegido...", espere).
4. Legenda: clique na caixa "Descreva seu reel..." (perto de x=200, y=195) e digite SÓ a 1ª linha ("Publicidade · links de afiliado");
   confira com `javascript_tool` que ela entrou na caixa; então digite o resto linha por linha, com a tecla Enter entre as linhas
   (um lote só). Confira o texto inteiro no fim. Nunca escreva t.me/... nem "@" (ver "Links" abaixo).
5. Clique em "Avançar" (embaixo à esquerda). Na tela "Configurações": "Público do post" = Público; LIGUE "Adicionar rótulo de IA"
   (chave perto de x=457, y=283; confira que ficou azul); "Turbinar post" fica DESLIGADO (é pago: nunca ligue); não use
   "Compartilhar nos grupos" nem "Programar".
6. Clique em "Postar". O Facebook volta para a página inicial.
7. Confirme em https://www.facebook.com/blackachadinhos.ofertas/reels/ ("Seus reels": o 1º cartão é o de hoje) e copie o endereço
   (`a[href*="/reel/"]`, sem o que vem depois de "?").
8. Feche a aba do Reel. Escreva "DD/MM HH:MM Reels: publicado (<endereço>)" em `diario.md` e dê push. A trava fecha com o "terminei" de
   quem a abriu: o do Divulgador, no fim do trabalho dele (ou "Reels: terminei", se foi você que abriu). Nunca clique em "Turbinar reel".
As posições (x, y) valem para a tela do PC do Vini (quadro 1568x751). Se a tela mudar, ache os botões com `find` ou com um print.

## Passo 8 – Registro (na hora, com push)
- Copie o roteiro para `reels/roteiros/AAAAMMDD.json` (é o que evita repetir produto).
- Acrescente 1 linha em "Feito" (data | ofertas com preço e comissão | endereço do Reel | observações).
- NÃO grave vídeo nem foto no repositório (pesam). Commit: "Reels DD/MM: ... [skip netlify]".

## Regras do vídeo (o gerador já cumpre; não mude sem motivo)
- 1080x1920, 30 fps, 18 a 22 s: abertura (2 s) + 4 s por produto + chamada final (4 s). Trilha original feita pelo próprio gerador.
- Identidade do `design.md`: fundo preto, amarelo #FFD400, fonte DejaVu Sans Bold, foto em cartão branco, preço em faixa amarela.
- O 1º quadro já sai completo (logo + "N ACHADOS DE HOJE" + "ATÉ X% OFF"): é a capa do Reel.
- Nada importante nos ~400 px de baixo nem nos ~150 px de cima (o Facebook cobre com botões e legenda).
- Tela final: "Os links estão no nosso Telegram" + caixa de busca com "Blackachados" + 'Ou toque em "Saiba mais" na nossa página'.
- Pode: nome, "de R$ X" riscado (só com riscado na página), "R$ Y", "-Z%", nota e vendidos, "no Mercado Livre".
- Não pode: logo do Mercado Livre, do Telegram ou de marca desenhado à parte, "oficial", "só hoje", "últimas unidades",
  contagem regressiva, botão falso, rosto ou nome de pessoa, voz sintética, música de terceiros.

## Links (regra da Meta descoberta em 16/11; ver facebook.md > LIMITE DE LINKS)
A página tem cota de 8 links por mês em reels, posts e comentários, e a de novembro acabou (a tela do Reel mostra "Restam 0 links").
Até 30/11: nenhum link na legenda nem em comentário. Chame assim: "procure por Blackachados no Telegram" ou 'toque em "Saiba mais"
na nossa página'. De 1/12 em diante: confira "Restam N links" na tela do Reel; se houver cota, o Diretor decide onde gastar.

## Avisos (aviso do Facebook sobre Reel: anote aqui com data e pare 3 dias)
(nenhum até 22/11)

## Números (o Diretor lê aos domingos)
Em https://www.facebook.com/blackachadinhos.ofertas/reels/ cada cartão mostra as visualizações. Anote aos domingos:
semana | Reels postados | visualizações somadas | inscritos do canal (metricas.csv). A meta é o canal crescer; se em 14 dias
os Reels tiverem visualização e o canal não crescer, o Diretor propõe ao Vini pôr também os links de afiliado no 1º comentário.

## VÍDEO DE ANÚNCIO DA CINTA (pedido do Vini em 22/11; fazer em 23/11, depois do Reel do dia; ORDEM 8 de trafego.md)
Uma vez só (refazer apenas se o Gestor pedir no diario.md porque o preço mudou). Usa a mesma foto e os mesmos preços conferidos da cinta do Reel.
1. Roteiro com `"modo": "anuncio"` e SÓ a cinta (1 oferta), na mesma pasta da foto. O gerador faz 12 s: abertura, cinta (6 s) e tela final
   "Toque no botão abaixo do vídeo" (o clique do anúncio vai direto ao produto, sem Telegram).
2. `python3 reels/fazer_reel.py --roteiro PASTA/anuncio.json --saida PASTA/anuncio --quadros`, conferir `conferencia.jpg`, depois sem `--quadros`.
3. Copiar `reel.mp4` para `anuncio/cinta-video.mp4` e `legenda.txt` para `anuncio/cinta-video-legenda.txt`; commit e push.
4. Anotar em "Feito": "vídeo de anúncio da cinta gravado em anuncio/". Não posta esse vídeo na página: quem usa é o Gestor.

## Aprendizados técnicos (22/11, 1º Reel)
- 23/11: tarefa agendada nova, criada numa conversa que só ganhou o repositório por `add_repo`, nasce SEM permissão de gravar (push 403
  em toda execução; a execução não pode adicionar o repositório sozinha). Por isso o Reel foi para dentro do Divulgador Facebook, que grava.
- `file_upload` do Chrome aceita arquivo criado nesta sessão, até 3,8 MB por envio. `upload_image` só serve para print (não para vídeo).
- Para trocar o vídeo sem perder a legenda: novo `find` do "file input" e outro `file_upload` (é o "Substituir mídia").
- O servidor não alcança `mlstatic.com` (403): foto só por print. O print com `zoom` da tela inteira sai em 1568x751.
- O Facebook pode estar no perfil pessoal (o Vini usa o Gerenciador): sempre confira e troque para a página antes de postar.
- O Reel publicado mostra "Conteúdo de IA" ao lado do nome da página (é o rótulo ligado no passo 7.5) e a legenda corta em
  "Publicidade · links de afiliado… Ver mais": o aviso fica visível sem abrir, como o jurídico pede.
- 24/11 (1º Reel do Divulgador): (1) `zoom` com `save_to_disk` grava o print em /tmp/claude-chrome-screenshots-*/ (o caminho vem no resultado), não em
  /tmp/claude-tool-results. (2) O `file_upload` só aceita arquivo da pasta de saída da sessão: copie o reel.mp4 para /mnt/user-data/outputs/ e envie de lá.
  (3) Confira os preços DEPOIS da virada da hora (o Mercado Livre troca preço e riscado na hora cheia) e poste em seguida. (4) Na página do produto, 'Encerra em'
  junto de 'Oferta relâmpago' = cronômetro: troque de oferta. (5) Com a janela minimizada, ponha o pontinho animado (facebook.md > PRINT QUE NÃO SAI) na cor do
  fundo, rgb(14,14,14), também na aba da foto: o gerador ignora. (6) Foto de peça vestida: aumente a foto com CSS (height:140vh, centrada) antes do print e
  recorte só a peça com o PIL; o arquivo sem borda escura entra direto no cartão.

## Feito (data | ofertas | endereço do Reel | observações)
- 22/11 13h56 | pisca-pisca cascata 400 LEDs R$ 59,99 de R$ 219,99 (-72%, ganhos extras 20%); tênis Kappa Zenit R$ 99,99 de R$ 229,99
  (-56%, ganhos extras 20%); parafusadeira The Black Tools 21V R$ 139,90 de R$ 259,90 (-46%, comissão não vista); Cicaplast Baume B5+
  R$ 64,37 de R$ 109,90 (-41%, ganhos 16%) | https://www.facebook.com/reel/1554465049846732/ | 1º Reel, feito pelo Claude principal;
  preços conferidos às 13h38-13h41; 22 s; 3,36 MB; rótulo de IA ligado; página com 3 seguidores e canal com 2 inscritos nesse dia.
- 24/11 21h04 | air fryer Midea Widemax 5,5 L R$ 237,91 no Pix de R$ 739,68 (-67%, ganhos extras 13%); CINTA Opta Corpus R$ 113,90 no Pix de R$ 179,90
  (-36%, ganhos extras 27%; 2º lugar, porque não tinha o maior desconto); carrinho de controle remoto Kizumba R$ 58,56 no Pix de R$ 149 (-60%, ganhos extras 20%);
  tapete de atividades Maxi Baby R$ 58,41 no Pix de R$ 129,90 (-55%, ganhos 12%) | https://www.facebook.com/reel/2575264492994414/ | 1º Reel feito pelo Divulgador
  Facebook; preços conferidos às 21h00-21h01, DEPOIS da virada da hora (às 21h o Kizumba, a Midea e o Taiff mudaram de preço); 22 s; 3,11 MB; rótulo de IA ligado;
  Turbinar desligado; legenda do gerador sem link. Trocas: secador Taiff saiu (o riscado caiu de R$ 613,74 para R$ 401: 26% OFF) e jogo de chaves Black Tools saiu
  (virou oferta relâmpago com cronômetro). FOTO DA CINTA: o anúncio só tem fotos da peça vestida em modelo (nenhuma só do produto); usei a foto principal
  recortada só na peça (colchetes e etiqueta, sem busto, quadril, mão ou braço). PARA O CLAUDE PRINCIPAL: confirmar se esse recorte atende ao 'sem corpo de modelo'.
