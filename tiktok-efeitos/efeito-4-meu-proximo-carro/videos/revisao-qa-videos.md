# C02 Meu próximo carro: revisão de QA dos vídeos

Feita em 06/11/2026 pelo revisor de QA dos vídeos.
**Resultado: aprovado, pronto para a coordenação. Nota 9 de 10.**
**Vini, você não precisa fazer nada com este arquivo.**

## Resumo

- Conferi os 3 MP4, as 3 capas, as legendas, o kit da C02-M1, a prévia e o `roteiros-videos.md`.
- Os vídeos não precisaram de correção. Nada foi renderizado de novo na pasta.
- Rodei o `render_videos.py` de novo numa cópia: os 16 arquivos saíram iguais, byte a byte.
- Corrigi só textos do `roteiros-videos.md` (lista na seção 6).

---

## 1. Ficha técnica (ffprobe, volumedetect e ebur128)

| Arquivo | Duração | Tamanho | Vídeo | Áudio | Volume médio | Volume integrado | Pico real |
|---|---|---|---|---|---|---|---|
| C02-V1.mp4 | 10,00 s | 2.735.160 bytes (2,61 MiB) | 1080x1920, 30 fps, H.264 High 4.1, yuv420p, 300 quadros | AAC estéreo 44,1 kHz | -18,2 dB | -14,8 LUFS | -1,7 dBTP |
| C02-V2.mp4 | 14,00 s | 3.392.515 bytes (3,24 MiB; limite da peça 3,78) | igual, 420 quadros | igual | -18,2 dB | -15,2 LUFS | -1,8 dBTP |
| C02-V3.mp4 | 11,00 s | 2.843.062 bytes (2,71 MiB) | igual, 330 quadros | igual | -18,3 dB | -15,1 LUFS | -1,8 dBTP |

- Os 3 estão de 6 a 15 s e abaixo de 4 MB.
- O índice do vídeo fica no começo do arquivo nos 3 (o vídeo começa a tocar mais rápido).
- Tem som desde o 1º quadro (-24,7 dB no primeiro meio segundo) e até o fim.
- Pasta `videos/` do C02: 11.679.142 bytes antes desta revisão. Com este arquivo, uns 11,69 milhões. Fica abaixo de 12 MB, mas com pouca folga.

## 2. Quadros conferidos

- Extraí 13 quadros do V1, 17 do V2 e 12 do V3, sempre com o 0,0 s e o último. Montei pranchas com a interface do TikTok marcada (topo 220 px, base 420 px, direita 140 px) e abri todas.
- Também recortei a carta do resultado de 0,1 em 0,1 s, para ver quando ela fica legível.

**O que vi:**

- **Gancho no 1º quadro** nos 3: "O filtro sorteia seu próximo carro", "Só paro quando sair ZERO KM" e "POV: perguntaram de novo do carro". Todos com até 7 palavras.
- **Nome do filtro:** "Meu próximo carro", igual ao `textos.md`, em amarelo e numa linha só, no cartão final dos 3, no `final.png`, nas capas e nas legendas.
- **Acentos certos** em tudo: próximo, você, então, Só, 1ª, 2ª, 3ª, CONSÓRCIO, ESPERANÇA, CÂMERA, VÔ.
- **Zona segura:** nada importante fora. O aviso de zona da biblioteca veio vazio no novo render. A única passagem é a linha "Procura na lupa 🔎", que encosta na faixa da direita durante a entrada do cartão final (uns 0,1 s) e depois volta. Não é problema.
- **Cartão final** nos 2 s finais (V1) e nos 2,5 s finais (V2 e V3), com símbolo do perfil, "Procura na lupa 🔎", nome e pergunta.
- **Algo muda na tela a cada 1 a 2 s** nos 3 vídeos.

**Quanto tempo o resultado da roleta fica legível:**

| Peça | Carta | Na tela | Observação |
|---|---|---|---|
| V1 | 5 SÓ PEGA NO TRANCO | 6,6 a 8,05 s (uns 1,4 s) | O confete cobre um pouco nos primeiros 0,2 s. O "Bora empurrar 😅" reforça a piada |
| V2 | 7 BICICLETA (POR ENQUANTO) | 3,6 a 4,55 s (uns 0,95 s) | Giro do meio, com "Não. De novo." |
| V2 | 15 EMPRESTADO DO CUNHADO | 6,1 a 7,05 s (uns 0,95 s) | Giro do meio, com "Quase…" |
| V2 | 4 ZERO KM (FINALMENTE) | 8,8 a 11,6 s (uns 2,8 s) | Resultado principal |
| V3 | 18 MOVIDO A ESPERANÇA | 7,0 a 8,55 s (uns 1,5 s) | Com "Assunto encerrado ✅" |

Os tempos seguem o plano. O V1 é o mais curto. Se a leitura do D3 mostrar que muita gente sai no fim, dá para encurtar a roleta em meio segundo e deixar o resultado mais tempo (ver Riscos).

## 3. Luz piscante

- Medi a luminância de cada quadro, ponto a ponto (mudança de 0,1 ou mais, a régua usada para "3 flashes por segundo").
- Nenhuma troca de quadro mexe em 10% ou mais da tela.
- Mesmo contando trocas que mexem em só 5% da tela, o pior segundo tem 2 flashes no V1, 2 no V2 e 1 no V3. Fica abaixo de 3.
- A roleta troca de carta rápido no começo (até uns 13 por segundo), mas as cartas vêm em ordem de brilho, então isso não vira pisca-pisca. Se o TikTok vai ou não dar aviso continua (a confirmar).

## 4. Regras fixas

- Sem marca, logo, escudo, time, modelo de carro reconhecível, placa, celebridade, "Pix", bebida, direção perigosa ou religião. Os carros são os desenhos genéricos das cartas e o 🚗 da Noto. A carta 18 mostra uma bomba de combustível genérica e 🤞, sem marca.
- Sem loja, produto, preço, link, @ ou desafio na tela, nas legendas, nas capas e nos comentários fixados.
- Nenhuma pessoa nem rosto nas peças N. No lugar da cabeça há uma carinha emoji.
- "Bora empurrar 😅" fala de empurrar carro parado. Não é direção.

## 5. Capas, kit da M1 e prévia

- **Capas** (1080x1920): texto grande e carta dentro do miolo que aparece na grade do perfil (y 240 a 1680), com "Filtro: Meu próximo carro 🔎" no rodapé. A do V1 tem um leque de 3 cartas e os desenhos de cima se sobrepõem um pouco, mas "SÓ PEGA NO TRANCO" lê bem. Não mexi.
- **Quadro de 0,5 s** (capa reserva): nos 3, gancho grande e carta inteira. Serve de capa.
- **gancho.png:** pílula de y 221 a 454 e até x 935. Dentro da zona segura.
- **gancho-baixo.png:** pílula até y 1485 (só a sombra fraca passa disso). Dentro da zona segura.
- **final.png:** igual ao cartão final dos vídeos, com "Qual saiu pra você?".
- **assinatura.wav:** 12,0 s, mono, 44,1 kHz, pico -1,5 dBFS. O "bi-bi" no começo, o toque em 3,0 s e o "bi-bi" em 9,56 s aparecem no volume, nos tempos certos. Em mono mede -18,7 LUFS. Quando o editor copia o mono para os 2 lados, o volume fica perto do dos vídeos (uns -15,7 LUFS; a confirmar no Clipchamp).
- **capa.jpg da M1** e **legenda.txt** da M1: certos.
- **previa-videos.png:** legível, sem nada cortado.

## 6. Legendas e roteiros-videos.md

- **Legendas** (com hashtags): V1 159 caracteres, V2 137 (153 com "ou no meu perfil"), V3 174 e M1 169. Muito abaixo do limite de legenda do TikTok (número exato a confirmar na tela). Cada uma tem 5 hashtags e o nome exato do filtro. Iguais às do plano.
- **Comentários fixados:** de 72 a 110 caracteres (limite do plano: 150).
- **Datas:** batem com a tabela 4.4 do plano. V1 sex 13/11 19h, V2 qua 18/11 18h, V3 dom 22/11 19h, M1 qui 26/11 19h. Dias da semana conferidos. Nada em 27/11 e 03/12.
- **Configurações:** Todos; comentários, dueto e costura ligados; rótulo de IA desligado; conteúdo comercial desligado; som do arquivo. Iguais ao plano (2.3, 2.5 e seção 7, passo 4).
- **Sem celular:** todo passo é feito no PC (TikTok Studio no navegador, Effect House, Clipchamp, Pexels ou Mixkit, janela anônima).
- **"Onde compra?"** → "Te chamo no direct 😉". Certo.

**Correções que fiz no `roteiros-videos.md`:**

1. Regra 8: a hashtag do desafio só entra se as regras pedirem (plano 5.4) e fica no lugar da última hashtag, para continuar com 5.
2. C02-M1, "Quando postar": nota de que a tabela do plano diz 19h, mas a regra de horários diz 18h às quintas. Vale a tabela até a coordenação decidir.
3. C02-M1, gravação (passo 5): o giro leva uns 2 s, segundo o `guia-montagem.md` (a confirmar). Dica para a seta do mouse da Ferramenta de Captura não cair no rosto nem na carta.
4. "A confirmar": tempo do giro com a estimativa do guia.
5. Tamanho da pasta atualizado com este arquivo.

## 7. Script

- Rodei `python3 render_videos.py --pasta <cópia no scratchpad>` (1 min 40 s). Os 16 arquivos saíram com o mesmo md5 dos da pasta. Aviso de zona vazio nas 3 peças.
- Testei também `--rapido` e `--so kit` com o nome reserva "Qual carro eu vou ter": funciona e o nome cabe numa linha no cartão final.
- Não mexi no script, na biblioteca, em `assets/`, em outras pastas, no `PRONTO-PARA-MONTAR.md` nem no `STATUS.md`. Sem commit e sem push.

## 8. Riscos que ficam

- **Aviso de luz piscante** do TikTok (a confirmar). A medição deu baixo risco. Se vier aviso, desacelerar o começo da roleta no script.
- **V1 com o resultado por uns 1,4 s.** Segue o plano. Se a retenção do fim for baixa no D3, encurtar a roleta (2,6 a 6,1 s) e deixar o resultado até 8,0 s.
- **Pasta perto de 12 MB** (uns 11,69 milhões de bytes). Se a coordenação somar arquivos aqui, mover o kit da M1 para outra pasta.
- **Horário da M1** (19h ou 18h numa quinta): a coordenação decide.
- **Volume da M1:** depende de como o Clipchamp trata o WAV mono (a confirmar). Se a M1 sair bem mais baixa que os outros vídeos, subir o volume da faixa no Clipchamp.
- **Seta do mouse** na gravação pela Ferramenta de Captura (a confirmar).
- Continuam a confirmar (fora do alcance da nuvem): data de aprovação do C02; Agendar e "Editar capa → Carregar" pela web; Fixar comentário; aba de efeitos no perfil; Biblioteca de Música Comercial; botão de gravar no preview; Clipchamp no PC; se o desafio pede autorização escrita de quem aparece na M1; se a busca acha o nome sem acento.
- **Perfil:** os vídeos do C02 não citam o nome da conta, então trocar o nome não obriga a refazer nada. O símbolo do cartão final é o mesmo da foto recomendada no `PERFIL.md` (carrinho turquesa na mira). Se a foto escolhida for outra, trocar o `simbolo_transparente.png` e rodar o script de novo.
