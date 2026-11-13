# TELEGRAM OFERTAS – "Black Achadinhos" (LEIA PRIMEIRO)

Nome do canal (escolha do Vini em 13/11, gatilho de Black Friday): **Black Achadinhos 🖤 Ofertas do Dia**.
Os textos das tarefas agendadas podem ainda dizer "Achadinhos do Dia" ou "Achadinhos da Casa": é o mesmo canal.
O nome vale o ano todo ("Black" como marca); não prometer "preço de Black Friday" fora da Black Friday (27/11/2026).

Projeto do Vini iniciado em 13/11/2026. Canal de ofertas no Telegram com links de afiliado do
**Mercado Livre, de TODAS as categorias** (decisão do Vini em 13/11: não focar em nicho; o Vini já é
afiliado do Mercado Livre). Shopee e Amazon ficam desligadas até ele mandar.
Tudo deste projeto mora NESTE ramo (`telegram`) do repositório quantocobrarpj. O ramo `main`
(site Quanto Eu Pago) só tem o arquivo `.github/workflows/telegram-ofertas.yml` (o agendamento de
hora em hora). Nunca escreva arquivos deste projeto no `main` (lá cada push pode publicar o site).
O que o robô faz em cada execução está em `rodar.sh` (os dois workflows só chamam esse arquivo).

## Situação
- 13/11/2026 14h35: **NO AR.** Canal público https://t.me/Blackachados (@Blackachados), bot
  @blackachados_bot como administrador, token no GitHub, boas-vindas fixada, descrição posta.
  `estado.json` tem `chat_id`. O robô posta o que estiver em `fila/` nos horários.
- O robô roda sozinho (a) de hora em hora e (b) em ~1 minuto sempre que um push muda `fila/` ou
  `disparar.txt` neste ramo (workflow `telegram-agora.yml`). Para forçar uma execução: mude
  `disparar.txt` e dê push. O resultado fica em `estado.json`.
- Horários: 1 oferta por horário de `config.json` > `horarios`. O agendamento do GitHub atrasa até ~1 h,
  então um horário pode ser cumprido com até `atraso_max_horas` de atraso, com pelo menos
  `intervalo_min_minutos` entre dois posts.
- `estado.json` > `erro` preenchido = o bot não consegue postar (perdeu o canal ou a permissão): o
  Diretor avisa o Vini. Falha de rede não queima a oferta: ela tenta de novo na execução seguinte.

## Peças
| Peça | O que faz | Onde roda | Gasta uso do Claude? |
|---|---|---|---|
| Robô postador (`bot.py`, chamado por `rodar.sh`) | Posta 1 oferta da fila em cada horário de `config.json` (9h, 12h, 15h, 18h, 20h, 21h), anota inscritos | GitHub Actions, de hora em hora e quando a fila muda | Não |
| Curador (tarefa agendada diária, 19h47) | Escolhe 6 a 8 ofertas no Mercado Livre, gera os links de afiliado e grava em `fila/` | Claude + Chrome do PC do Vini | Sim |
| Crescimento (seg e qui) | Traz inscritos sem spam; registra em `crescimento.md` | Claude (+ Chrome se houver) | Sim |
| Divulgador Facebook (diário, 20h31) | Posta as 2 campeãs do dia na página "Black Achadinhos" do Facebook e em grupos de ofertas que permitem; sempre chama para o canal. Regras em `facebook.md` | Claude + Chrome do PC do Vini | Sim |
| Divulgador X (diário, 21h17) | Posta as 2 campeãs do dia no X @titantuita (conta pessoal do Vini): 1 na hora, 1 programada para 12h15. Regras em `x.md` | Claude + Chrome do PC do Vini | Sim |
| Diretor (domingo) | Lê os números, ajusta e manda 1 aviso curto ao Vini | Claude | Sim |
| Coletor Shopee (`coletor_shopee.py`) | Desligado (só serve se um dia a Shopee voltar) | – | Não |

## Como o Curador trabalha (Mercado Livre)
1. Chrome do PC do Vini, logado no Mercado Livre com a conta de afiliado. Nunca digitar senha.
2. Fontes de oferta: https://www.mercadolivre.com.br/ofertas (ofertas do dia) e a Central de
   Afiliados e Criadores (produtos em destaque e comissões por categoria).
3. Rodízio de categorias (`config.json` > `mercadolivre.categorias_rodizio`): a cada dia, 6 a 8
   ofertas de pelo menos 4 categorias diferentes, puxando para as de comissão maior.
4. Critérios: desconto real de 15% ou mais, 500+ vendidos, nota 4,6+, R$ 20 a R$ 800, de preferência
   Full/frete grátis e loja oficial ou vendedor bem avaliado. Evitar oferta relâmpago com cronômetro
   que acaba antes do horário de postagem.
5. Link: SEMPRE pelo gerador do programa (barra de afiliado no topo da página do produto ou
   "Compartilhar" na Central de Afiliados). Link comum do produto NÃO paga comissão. Usar a etiqueta
   `telegram` se o gerador permitir.
6. A fila conferida às 19h47 é postada às 20h e 21h do mesmo dia e às 9h, 12h, 15h e 18h do dia
   seguinte. Ofertas vencem 24 h depois de `conferido_em`. O push da fila já dispara o robô na hora.
7. Só links do Mercado Livre são aceitos (`config.json` > `dominios_permitidos`: mercadolivre.com,
   mercadolivre.com.br, meli.la). O gerador hoje devolve links `https://meli.la/...`.

## Potencial de venda (pedido do Vini em 13/11: divulgar mais o que tem mais chance de vender)
O Curador dá a cada oferta o campo `"potencial"` de 1 a 5 (o robô ignora; quem usa é o Divulgador):
some 1 ponto para cada item verdadeiro: (a) +10 mil vendidos e nota 4,8+; (b) desconto real de 40% ou mais;
(c) preço entre R$ 40 e R$ 250 (compra por impulso); (d) marca conhecida ou loja oficial, com Full/frete grátis;
(e) categoria de comissão alta no painel de afiliado OU produto da época (Black Friday, Natal, volta às aulas).
As 2 de maior potencial do dia são as **campeãs**: recebem `"prioridade": 1` (saem primeiro no canal) e são as
que o Divulgador leva para o Facebook. Aos domingos o Curador lê no painel de afiliado quais links/categorias
tiveram mais clique e venda e anota em `ml.csv`; o Diretor puxa o rodízio para elas.

## Como escrever uma oferta na fila
Um arquivo por oferta em `fila/AAAAMMDD-NN.json` (o robô nunca edita esses arquivos):
```json
{"id": "20261114-01", "loja": "Mercado Livre", "nome": "Nome curto e claro do produto",
 "preco": 39.90, "preco_de": 69.90, "cupom": "", "motivo": "4,8★ · +5 mil vendidos · Full",
 "link": "https://meli.la/XXXX", "pagina": "https://www.mercadolivre.com.br/.../p/MLB000",
 "imagem": "https://http2.mlstatic.com/...-O.jpg", "categoria": "Casa",
 "conferido_em": "2026-11-14T19:50", "prioridade": 0, "potencial": 3}
```
- Obrigatórios: `nome`, `preco`, `link` (link de AFILIADO, https, de domínio em `dominios_permitidos`).
- `preco_de` só se a página mostrar o preço riscado de verdade. Nunca invente preço "de".
- `pagina` = endereço normal do produto (sem ser de afiliado). Serve para os outros agentes conferirem o
  preço depois sem clicar no link de afiliado.
- `imagem` = foto principal em **.jpg** (no Mercado Livre, troque o final `.webp` da foto por `.jpg`).
- `potencial` de 1 a 5: ver a seção "Potencial de venda".
- `prioridade`: 1 nas 2 campeãs do dia (maior potencial; saem primeiro, às 20h e 21h); 0 nas outras.
  Oferta relâmpago que acaba antes do dia seguinte: prioridade 2 só se ela puder sair ainda hoje; senão, não inclua.
- Resultado de cada oferta: `estado.json` > `itens` (postado, erro com motivo, vencido).

## Regras que não podem ser quebradas
1. Sem spam: nunca adicionar pessoas ao canal, nunca mandar mensagem em massa, nunca postar o link
   em grupos dos outros sem o dono permitir, nunca comprar inscritos. Isso derruba a conta do Telegram.
   Exceção (pedido do Vini em 13/11): grupos do FACEBOOK feitos para ofertas/promoções/divulgação, cujas
   regras permitem esse tipo de post; só pela página "Black Achadinhos", com os limites de `facebook.md`.
   No X: só posts na própria conta @titantuita, com os limites de `x.md` (nunca responder aos outros com link).
2. Preço e desconto reais, conferidos na hora. Nada de urgência falsa ("últimas unidades") inventada.
3. Transparência: a descrição e a mensagem fixada dizem que há links de afiliado. Não remover.
4. Regras do programa do Mercado Livre: não pagar anúncio em buscador, não clicar nem comprar pelos
   próprios links, não se passar por canal oficial (o nome do canal não usa "Mercado Livre"), divulgar
   só em canais permitidos. Se o painel pedir para cadastrar o canal do Telegram como canal de
   divulgação, o Curador anota em curador.md e o Diretor avisa o Vini. Para conferir preço, usar a
   `pagina` do produto, não o link de afiliado.
5. Todas as categorias, MENOS: adulto, armas e réplicas, remédios e suplementos com promessa de saúde,
   cigarro/vape, bebida alcoólica, apostas, produto falsificado ou de vendedor mal avaliado.
6. Nunca digitar senha, token ou código em lugar nenhum. Token e segredos só o Vini coloca.
7. Gastar dinheiro, criar conta em serviço novo e mandar mensagem para terceiros em nome do Vini:
   só com o "sim" dele (o Diretor pergunta no aviso de domingo).

## Metas e ponto de decisão
- 30 dias (13/12/2026): 100 inscritos e a 1ª comissão. 90 dias: 500 inscritos.
- 13/12/2026: se houver menos de 50 inscritos e nenhuma comissão, o Diretor propõe mudar a
  fonte de inscritos ou encerrar. Canal de oferta só rende com gente dentro; o robô sozinho não traz ninguém.
- Canal genérico concorre com canais gigantes: o Diretor acompanha quais categorias dão mais clique
  e venda e puxa o rodízio para elas.

## Pendências
- Diretor: leia também `x.md` (posts, aprendizados e avisos do X) e trate "Avisos do X" como os do Facebook.
- Confirmar no painel de afiliado se o canal do Telegram e a página do Facebook precisam estar cadastrados
  como canais de divulgação.
- Etiqueta: os links saem com a etiqueta padrão da conta ("viniciusmarrone"). Sem etiquetas separadas
  ("telegram", "facebook", "x") não dá para saber de onde veio cada venda; criar etiqueta depende do Vini.
- Limpeza: o Diretor apaga de `fila/` os arquivos com mais de 30 dias (o robô tira do `estado.json` sozinho).
- Números de cliques e ganhos: o Curador lê no painel aos domingos e grava em `ml.csv`.
