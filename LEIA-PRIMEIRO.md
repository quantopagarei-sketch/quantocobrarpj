# TELEGRAM OFERTAS – "Achadinhos do Dia" (LEIA PRIMEIRO)

Projeto do Vini iniciado em 13/11/2026. Canal de ofertas no Telegram com links de afiliado do
**Mercado Livre, de TODAS as categorias** (decisão do Vini em 13/11: não focar em nicho; o Vini já é
afiliado do Mercado Livre). Shopee e Amazon ficam desligadas até ele mandar.
Tudo deste projeto mora NESTE ramo (`telegram`) do repositório quantocobrarpj. O ramo `main`
(site Quanto Eu Pago) só tem o arquivo `.github/workflows/telegram-ofertas.yml`. Nunca escreva
arquivos deste projeto no `main` (lá cada push pode publicar o site).

## Situação
- 13/11/2026: robô, fila e agentes criados e testados sem internet (modo de teste).
- FALTA o Vini (uma vez só): criar o bot no @BotFather, colar o token no GitHub
  (segredo `TELEGRAM_BOT_TOKEN`), criar o canal e colocar o bot como administrador.
- Depois disso o robô se liga sozinho: acha o canal, grava `estado.json` (chat_id), põe a
  descrição, fixa a mensagem de boas-vindas e começa a postar o que estiver em `fila/`.
- Como saber se está ligado: `estado.json` tem `chat_id` preenchido. Sem isso, os agentes param na hora.

## Peças
| Peça | O que faz | Onde roda | Gasta uso do Claude? |
|---|---|---|---|
| Robô postador (`bot.py`) | Posta 1 oferta da fila nos horários de `config.json` (9h, 12h, 15h, 18h, 20h, 21h), anota inscritos | GitHub Actions, de hora em hora | Não |
| Curador (tarefa agendada diária, 19h47) | Escolhe 6 a 8 ofertas no Mercado Livre, gera os links de afiliado e grava em `fila/` | Claude + Chrome do PC do Vini | Sim |
| Crescimento (seg e qui) | Traz inscritos sem spam; registra em `crescimento.md` | Claude (+ Chrome se houver) | Sim |
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
   seguinte. Ofertas vencem 24 h depois de `conferido_em`.

## Como escrever uma oferta na fila
Um arquivo por oferta em `fila/AAAAMMDD-NN.json` (o robô nunca edita esses arquivos):
```json
{"id": "20261114-01", "loja": "Mercado Livre", "nome": "Nome curto e claro do produto",
 "preco": 39.90, "preco_de": 69.90, "cupom": "", "motivo": "4,8★ · +5 mil vendidos · Full",
 "link": "https://mercadolivre.com/sec/XXXX", "imagem": "https://...jpg",
 "categoria": "Casa", "conferido_em": "2026-11-14T19:50", "prioridade": 0}
```
- Obrigatórios: `nome`, `preco`, `link` (link de AFILIADO, https, de domínio em `dominios_permitidos`).
- `preco_de` só se a página mostrar o preço riscado de verdade. Nunca invente preço "de".
- `prioridade` 1 para as 2 ofertas que devem sair ainda hoje (as que podem acabar antes).
- Resultado de cada oferta: `estado.json` > `itens` (postado, erro com motivo, vencido).

## Regras que não podem ser quebradas
1. Sem spam: nunca adicionar pessoas ao canal, nunca mandar mensagem em massa, nunca postar o link
   em grupos dos outros sem o dono permitir, nunca comprar inscritos. Isso derruba a conta do Telegram.
2. Preço e desconto reais, conferidos na hora. Nada de urgência falsa ("últimas unidades") inventada.
3. Transparência: a descrição e a mensagem fixada dizem que há links de afiliado. Não remover.
4. Regras do programa do Mercado Livre: não pagar anúncio em buscador, não clicar nem comprar pelos
   próprios links, não se passar por canal oficial (o nome do canal não usa "Mercado Livre"), divulgar
   só em canais permitidos. Se o painel pedir para cadastrar o canal do Telegram como canal de
   divulgação, o Curador anota em curador.md e o Diretor avisa o Vini.
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
- Confirmar no painel de afiliado se o canal do Telegram precisa estar cadastrado como canal de divulgação.
- Números de cliques e ganhos: o Curador lê no painel aos domingos e grava em `ml.csv`.
