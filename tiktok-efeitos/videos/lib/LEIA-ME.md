# render.py: vídeos 9:16 com os nossos PNGs

Biblioteca para a **nuvem** montar os vídeos do TikTok. O Vini não grava nada: o vídeo sai pronto daqui, com som, e o Montador só posta.

- **Precisa só de:** Python 3, Pillow, numpy e ffmpeg. Nada de `pip install`.
- **Saída:** MP4 1080x1920, 30 fps, H.264 (High, yuv420p, cor BT.709), `+faststart`, áudio AAC 128k estéreo.
- **Tamanho:** CRF 21 com teto de 2.600 kbps. Um vídeo de 10 s fica com uns 3,5 MB. Se passar de 4 MB a cada 10 s, ele recodifica sozinho em 2 passadas.
- **Som:** tudo feito aqui com numpy (tique, plim, vush, pop, bipe, tecla, toque e um fundo rítmico próprio). Nenhuma música de terceiros.
- **Determinístico:** a mesma semente gera o mesmo vídeo (conferido: mesmo hash de quadros e de áudio em duas rodadas).
- **Tempo:** a demo de 10 s leva uns 20 a 25 s nesta máquina (4 núcleos).

## Rodar

```bash
python3 render.py --demo saida.mp4                 # demo do C02 + prancha saida_prancha.png
python3 render.py --demo saida.mp4 --slides pasta  # + 3 slides JPG
python3 render.py --demo saida.mp4 --resultado 12 --sem-trilha
python3 render.py --info video.mp4                 # duração, tamanho, codecs (ffprobe)
python3 render.py --prancha video.mp4 -o prancha.png -n 12
```

A demo usa `efeito-4-meu-proximo-carro/assets`: título com pílula "toque na tela", dedo tocando, roleta de 4 s caindo na carta 05, confete, e o texto "Procure na lupa / Meu próximo carro". Para outra pasta, use `--assets`.

**Grave sempre fora da pasta do projeto** (ex.: no scratchpad). Os vídeos prontos vão para onde a coordenação mandar.

## Exemplo curto

```python
import sys; sys.path.insert(0, "/home/user/quantocobrarpj/tiktok-efeitos/videos/lib")
import render as r

A = "/home/user/quantocobrarpj/tiktok-efeitos/efeito-4-meu-proximo-carro/assets"
cartas = r.carregar_pasta(A + "/cartas", "carta_*.png")

v = r.Video(10)                                   # 10 segundos
v.fundo(r.Padrao("tracejado", cor_forma=(255, 212, 59, 34), velocidade=(0, 150),
                 fundo=r.DegradeAnimado(["#1A1D24", "#2B303B", "#0F4A52", "#2B303B"])))
v.trilha(volume=0.26)                             # fundo rítmico (opcional)
v.texto("Qual vai ser o teu *próximo carro*? 🤔", 0, 6, centro=(540, 375), tamanho=86,
        entrada=None, ocioso="pulsar", nome="gancho")      # texto já no 1º quadro
v.imagem(A + "/titulo_toque.png", 0, 1.9, centro=(540, 870), escala=1.6, nome="título")
t = v.roleta(cartas, 4, inicio=1.9, duracao=4.1, centro=(540, 870), escala=1.6)  # cai na carta 05
v.texto("*Meu próximo carro*", t + 0.8, None, centro=(540, 1315), tamanho=88, max_linhas=1,
        entrada="deslizar_baixo", z=60, nome="chamada")
info = v.renderizar("/caminho/fora/do/projeto/video.mp4")  # dict com duração, MB, codecs, avisos
r.prancha("/caminho/fora/do/projeto/video.mp4")            # prancha de 12 quadros para revisão
```

## API

### Linha do tempo: `Video(duracao, fundo="#22252C", fps=30, semente=2027)`

| Método | O que faz |
|---|---|
| `fundo(f)` | Cor, Image (preenche a tela), `DegradeAnimado`, `Padrao` ou função `t -> Image`. |
| `imagem(img, inicio, fim, centro, escala, rotacao, opacidade, entrada, saida, ocioso, nome)` | Coloca um PNG. `centro`, `escala`, `rotacao` e `opacidade` aceitam número ou função do tempo. |
| `texto(texto, inicio, fim, centro, tamanho, fonte, cor, cor_destaque, contorno, sombra, largura_max, max_linhas, caixa, entrada, saida, ocioso, cps, nome)` | Texto animado (detalhes abaixo). |
| `roleta(imagens, resultado, inicio, duracao, centro, escala)` | Cartas trocando rápido e desacelerando até o resultado, com quique, tique a cada troca, plim, luz, raios, confete, brilhos e tremida. Nunca repete carta seguida. Devolve o tempo do resultado. |
| `revelar(img, inicio, centro, escala)` | Aparece com pop e mola, luz atrás, brilhos e plim. |
| `ranking(itens, inicio, posicoes, n_posicoes, intervalo, area)` | Vagas numeradas 1..N; cada item (texto ou imagem) entra voando para a sua vaga (vush + pop). Serve para o C09 (10 posições). |
| `slides(itens, inicio, dur_cada, transicao)` | Sequência de imagens ou textos. Transição `deslizar`, `zoom`, `fade` ou `corte`. |
| `contagem(inicio, de=3, final="JÁ!")` | 3, 2, 1, JÁ! grandes com bipe. Devolve o tempo em que termina. |
| `toque(t, centro)` | Dedo 👆 tocando a tela, com anel e som. |
| `confete(inicio, origem, quantidade, modo)` | `modo="explosao"` (sai de um ponto) ou `"chuva"` (cai do topo). |
| `brilhos(inicio, centro, raio)` | Estrelinhas piscando em volta de algo. |
| `luz(inicio, centro, raio)` / `raios(inicio, centro)` | Luz redonda atrás / raios de sol girando. |
| `tremida(inicio, duracao, intensidade)` | Tremida na tela inteira. |
| `som(nome_ou_array, t, volume, pan)` | Toca `tique`, `plim`, `vush`, `pop`, `bip`, `tecla`, `toque` ou um array numpy (44,1 kHz). |
| `trilha(volume=0.3, bpm=112, ducking=0.45)` | Liga o fundo rítmico. Os efeitos abaixam a trilha quando tocam. |
| `adicionar(func, inicio, fim, z)` | Camada própria: `func(canvas, t_local, t)` desenha no quadro (Image RGB). |
| `quadro(t)` | Devolve o quadro do tempo `t` (Image RGB). |
| `renderizar(saida, crf=21, preset="medium", limite_mb_10s=4.0)` | Gera o MP4. Devolve info do ffprobe, tempo de render e avisos de zona segura. |
| `prancha(saida, n=12)` | Prancha direto da linha do tempo, sem gerar MP4 (conferência rápida). |
| `exportar_slides(tempos, pasta, max_kb=500)` | Salva quadros como JPG 1080x1920 de até 500 KB (carrossel de fotos). |

**Ordem das camadas:** `z` maior fica por cima. Padrões: fundo de luz 4–5, imagens 10–12, texto 20, confete 50, brilhos 55, toque 40. Para texto ficar acima do confete, use `z=60`.

**Entradas:** `pop`, `fade`, `zoom`, `deslizar_baixo`, `deslizar_cima`, `deslizar_esq`, `deslizar_dir`, `girar`, `cair`, `digitar` (só texto, `cps` letras por segundo, com som de tecla) ou `None` (já aparece no 1º quadro).
**Saídas:** `fade`, `pop`, `zoom`, `deslizar_*` ou `None`. **Parado (`ocioso`):** `flutuar`, `pulsar`, `balancar`.
Entrada `pop` toca um pop; entrada `deslizar_*` toca um vush (desligue com `som=False`).

### Texto

`texto_img(texto, tamanho, fonte_nome, cor, cor_destaque, contorno, cor_contorno, sombra, largura_max, ...)` devolve a imagem RGBA (com cache). `Video.texto` usa a mesma função.

- Fonte Inter. Nomes: `titulo` (Inter Display Black), `display`, `black`, `extra`, `bold`, `semi`, `regular`.
- `*assim*` pinta com `cor_destaque` (amarelo `#FFD43B`). `\n` quebra a linha. `\*` é um asterisco de verdade.
- Quebra a linha sozinho em `largura_max` (padrão 800 px). Se uma palavra não couber, ou se passar de `max_linhas`, **diminui a fonte** até caber.
- Emoji colorido (Noto Color Emoji, desenhado em 109 e redimensionado). Emoji no fim não fica sozinho na linha: gruda na palavra de antes.
- Contorno (`contorno` em px), sombra `(dx, dy, desfoque, opacidade 0..255)`, `True` ou `None`, e `caixa="#FFFFFF"` para pílula atrás (estilo legenda).

### Fundos

- `fundo_cor(cor)`, `fundo_degrade(cores, angulo=90)` (90 = de cima para baixo).
- `DegradeAnimado(cores, angulo, velocidade)`: degradê que flui.
- `fundo_desfocado(img, raio, escurecer)`: foto/PNG preenchendo a tela, desfocada e escurecida.
- `Padrao(tipo, cor_forma, fundo, tamanho, velocidade)`: `bolinhas`, `listras`, `xadrez`, `estrelas`, `tracejado`, `mais` ou `emoji`. Desliza sem emenda. `fundo` pode ser cor ou `DegradeAnimado`.
- `cobrir(img)`: imagem preenchendo 1080x1920 sem distorcer.

### Imagens e suavização

- `carregar(caminho_ou_Image)`, `carregar_pasta(pasta, "carta_*.png")`, `ajustar(img, largura, altura)` (escala para caber).
- `transformar(img, escala, rotacao, opacidade)` e `colar(canvas, img, centro, escala, rotacao, opacidade, ancora)` (`ancora`: `centro`, `topo` ou `base`). Rotação em graus, sentido anti-horário.
- Ao ampliar mais de 15%, a imagem ganha uma leve nitidez.
- Suavização: `linear`, `ease_in/out_quad`, `ease_*_cubic`, `ease_out_quint`, `ease_out_expo`, `ease_in_back`, `ease_out_back`, `ease_out_elastic`, `ease_out_bounce`, `quique(t)` (mola), `progresso(t, inicio, duracao, "out_cubic")`, `lerp`, `misturar(cor1, cor2, p)`.

### Áudio

`som_tique`, `som_plim`, `som_vush` (estéreo, passa da esquerda para a direita), `som_pop`, `som_bip`, `som_tecla`, `som_toque`, `trilha_ritmica(duracao, bpm, semente, progressao)`, `mixar(duracao, eventos, trilha, volume_trilha, ducking)`, `masterizar(x)` (RMS alvo, limitador suave, pico em -1,5 dBFS) e `salvar_wav(caminho, x)`. A demo mede -13,9 LUFS, com pico real de -0,7 dBFS depois do AAC.

### Revisão e exportação

- `prancha(mp4, saida=None, n=12, zonas=True)`: N quadros do MP4 lado a lado, com a hora de cada um. Em vermelho, as faixas da interface do TikTok.
- `info_video(mp4)`: duração, bytes, MB, codecs, resolução, fps e áudio.
- `salvar_jpg(img, caminho, max_kb=500)`: JPG 1080x1920 que cabe no limite.

## Zona segura (interface do TikTok)

Valores conservadores, em px num quadro 1080x1920: **topo 220, base 420, direita 140, esquerda 60**. Área livre: x de 60 a 940, y de 220 a 1500. Esses valores são os pedidos pela coordenação; não confirmei com print do app (a confirmar).

- `zona_segura()` devolve o retângulo. `checar_zona_segura(caixa)` devolve `[]` ou frases como "passa 12 px na zona de direita".
- No render, todo elemento com `nome=` é checado. A checagem usa a posição de repouso (sem contar o pop, o pulso ou o quique). Se algo ficar fora por mais de 0,4 s, sai um aviso no terminal e em `info["avisos_zona"]`.
- Centralizado em x = 540, o que é importante cabe em **800 px de largura**. As cartas do C01/C02 têm 500 px visíveis (com a borda branca), então a escala máxima é **1,6**.

## Bom saber

- Os PNGs dos efeitos têm só 512 px. Na escala 1,6, eles ficam um pouco menos nítidos que o texto. Se a coordenação quiser mais nitidez, o caminho é gerar as cartas em 1024 px com o `gerar.py` de cada efeito.
- O texto na tela tem que estar no **1º quadro** (gancho). Use `entrada=None` no texto do gancho.
- O vídeo do efeito **não vende produto**: nada de loja, link ou cupom. O nome do efeito vai escrito igual na tela, na legenda e no comentário fixado.
- Carrossel de fotos pelo PC talvez não exista (ver `videos/pesquisa/R1`). Os JPGs ficam prontos para quando o Montador testar.
- Nada de música famosa: use só os sons daqui.
