# TELEGRAM OFERTAS – "Achadinhos da Casa" (LEIA PRIMEIRO)

Projeto do Vini iniciado em 13/11/2026. Canal de ofertas no Telegram com links de afiliado
(Shopee primeiro; Mercado Livre e Amazon depois). Mesmo nicho e nome da conta do TikTok
@casa.achadinhos.br ("Achadinhos da Casa"), que é a principal fonte de inscritos.
Tudo deste projeto mora NESTE ramo (`telegram`) do repositório quantocobrarpj. O ramo `main`
(site Quanto Eu Pago) só tem o arquivo `.github/workflows/telegram-ofertas.yml`. Nunca escreva
arquivos deste projeto no `main` (lá cada push pode publicar o site).

## Situação
- 13/11/2026: robô, fila, coletor e agentes criados e testados sem internet (modo de teste).
- FALTA o Vini (uma vez só): criar o bot no @BotFather, colar o token no GitHub
  (segredo `TELEGRAM_BOT_TOKEN`), criar o canal e colocar o bot como administrador.
- Depois disso o robô se liga sozinho: acha o canal, grava `estado.json` (chat_id), põe a
  descrição, fixa a mensagem de boas-vindas e começa a postar o que estiver em `fila/`.
- Como saber se está ligado: `estado.json` tem `chat_id` preenchido. Sem isso, os agentes param na hora.

## Peças
| Peça | O que faz | Onde roda | Gasta uso do Claude? |
|---|---|---|---|
| Robô postador (`bot.py`) | Posta 1 oferta da fila nos horários de `config.json` (9h, 12h, 15h, 18h, 20h, 21h), anota inscritos | GitHub Actions, de hora em hora | Não |
| Coletor Shopee (`coletor_shopee.py`) | Abastece a fila sozinho pela API oficial de afiliados | GitHub Actions | Não (desligado até existirem `SHOPEE_APP_ID` e `SHOPEE_APP_SECRET`) |
| Curador (tarefa agendada diária) | Escolhe 6 a 8 ofertas no painel de afiliado da Shopee e grava em `fila/` | Claude + Chrome do PC do Vini | Sim |
| Crescimento (seg e qui) | Traz inscritos sem spam; registra em `crescimento.md` | Claude (+ Chrome se houver) | Sim |
| Diretor (domingo) | Lê os números, ajusta e manda 1 aviso curto ao Vini | Claude | Sim |

## Como escrever uma oferta na fila
Um arquivo por oferta em `fila/AAAAMMDD-NN.json` (o robô nunca edita esses arquivos):
```json
{"id": "20261114-01", "loja": "Shopee", "nome": "Nome curto e claro do produto",
 "preco": 39.90, "preco_de": 69.90, "cupom": "", "motivo": "4,9★ · 12 mil vendidos",
 "link": "https://s.shopee.com.br/XXXX", "imagem": "https://...jpg",
 "conferido_em": "2026-11-14T19:50", "prioridade": 0}
```
- Obrigatórios: `nome`, `preco`, `link` (link de AFILIADO, https, de loja em `dominios_permitidos`).
- `preco_de` só se a loja mostrar o preço riscado de verdade. Nunca invente preço "de".
- Sem `valido_ate`, a oferta vence 48 h depois de `conferido_em` (o robô pula).
- Resultado de cada oferta: `estado.json` > `itens` (postado, erro com motivo, vencido).

## Regras que não podem ser quebradas
1. Sem spam: nunca adicionar pessoas ao canal, nunca mandar mensagem em massa, nunca postar o link
   em grupos dos outros sem o dono permitir, nunca comprar inscritos. Isso derruba a conta do Telegram.
2. Preço e desconto reais, conferidos na hora. Nada de urgência falsa ("últimas unidades") inventada.
3. Transparência: a descrição e a mensagem fixada dizem que há links de afiliado. Não remover.
4. Regras da Shopee Afiliados: não pagar anúncio com a marca Shopee, não clicar nos próprios links,
   não prometer cupom que não existe. Produto de saúde: sem promessa de cura.
5. Só casa, cozinha, organização, limpeza e utilidades. Nada de adulto, armas, remédio, aposta, cigarro.
6. Nunca digitar senha, token ou código em lugar nenhum. Token e segredos só o Vini coloca.
7. Gastar dinheiro, criar conta em serviço novo e mandar mensagem para terceiros em nome do Vini:
   só com o "sim" dele (o Diretor pergunta no aviso de domingo).

## Metas e ponto de decisão
- 30 dias (13/12/2026): 100 inscritos e a 1ª comissão. 90 dias: 500 inscritos.
- 13/12/2026: se houver menos de 50 inscritos e nenhuma comissão, o Diretor propõe mudar a
  fonte de inscritos ou encerrar. Canal de oferta só rende com gente dentro; o robô sozinho não traz ninguém.

## Pendências
- `config.json` > `shopee.affiliate_id`: o Curador lê no painel na 1ª execução e grava aqui.
- Open API da Shopee: o Curador confere se o painel já mostra "Open API". Se mostrar, o Diretor avisa
  o Vini (ele gera as credenciais e cola 2 segredos no GitHub); aí o coletor assume e o Curador vira revisão semanal.
- Mercado Livre (o Vini já é afiliado) e Amazon: entram depois dos primeiros 100 inscritos.
