/**
 * Torcedômetro (C01): script alternativo (PLANO C do guia-montagem.md, Parte 15)
 *
 * NÃO é o caminho principal. O caminho principal é o template Randomizer 2D
 * sem código (Partes 1 a 7 do guia). Use este script só se a lógica do template
 * não funcionar ou não existir na sua versão do Effect House.
 *
 * O que ele faz:
 *   1. Ao abrir o efeito e ao apertar GRAVAR: mostra só o título.
 *   2. No toque: o título some em 0,3 s, as cartas giram por 2 s
 *      (desacelerando no fim) e param numa carta sorteada.
 *   3. Novo toque depois do resultado: gira de novo (dá para desligar).
 *
 * De onde vieram os nomes da API (APJS):
 *   - Guia oficial "Scripting Capability Usage Guide" (classe com @component()
 *     que estende APJS.BasicScriptComponent; onStart/onUpdate/onDestroy).
 *   - Tutorial oficial "VFX: Tap Burst" (APJS.EventManager.getGlobalEmitter()
 *     .on(APJS.EventType.Touch, ...) e APJS.TouchPhase.Began).
 *   - Arquivo de tipos APJS.d.ts e OrionDecorators.d.ts de um projeto público
 *     do Effect House no GitHub (christophusbeck/StatJack). Ele confirma:
 *     EventType.RecordStart, Image.texture, Image.opacity, Texture.getControl(),
 *     AnimatedTextureProvider.playFromTo/pause/play/getFrameCount e o
 *     decorador @serializeProperty. O mesmo projeto usa exatamente esta técnica
 *     (pause → playFromTo(i, i) → play) para mostrar 1 quadro de uma sequência.
 *   - Este arquivo passou na checagem de tipos (tsc) contra esses dois .d.ts.
 *     Ainda NÃO foi rodado dentro do Effect House (a confirmar no Preview).
 *
 * Como ligar (detalhes na Parte 15 do guia):
 *   - Crie um script TypeScript no projeto, cole este conteúdo e salve.
 *   - Adicione o script como componente num objeto da cena.
 *   - No Inspector do script, preencha:
 *       Titulo           → o objeto que mostra o título (ex.: Title)
 *       Cartas           → o objeto que mostra as cartas (ex.: RandomAnimationSequence)
 *       Sequencia Cartas → a Texture Sequence com carta_01 … carta_26
 *   - Desligue a lógica do template (a caixa do randomizador no Visual
 *     Scripting) para as duas lógicas não brigarem.
 */

@component()
export class TorcedometroController extends APJS.BasicScriptComponent {
  // ---------- Campos que aparecem no Inspector ----------

  /** Objeto que tem o componente Image do título ("QUE TORCEDOR VOCÊ É?"). */
  @serializeProperty
  public titulo!: APJS.SceneObject;

  /** Objeto que tem o componente Image onde as cartas aparecem. */
  @serializeProperty
  public cartas!: APJS.SceneObject;

  /** A Texture Sequence importada da pasta cartas (26 quadros, índice 0 a 25). */
  @serializeProperty
  public sequenciaCartas!: APJS.Texture;

  /** Quanto tempo as cartas giram, em segundos. */
  @serializeProperty
  public tempoGiro: number = 2.0;

  /** Quanto tempo o título leva para sumir, em segundos. */
  @serializeProperty
  public tempoSomeTitulo: number = 0.3;

  /** Ligado: tocar de novo depois do resultado faz girar outra vez. */
  @serializeProperty
  public girarDeNovoNoToque: boolean = true;

  // ---------- Estado interno ----------

  // 0 = título na tela · 1 = título sumindo · 2 = cartas girando · 3 = resultado parado
  private estado: number = 0;
  private imgTitulo: APJS.Image | null = null;
  private imgCartas: APJS.Image | null = null;
  private provider: APJS.AnimatedTextureProvider | null = null;
  private totalCartas: number = 0;
  private relogio: number = 0;
  private desdeUltimaTroca: number = 0;
  private cartaAtual: number = -1;

  // Intervalo entre trocas de carta durante o giro (segundos).
  // Começa rápido e vai desacelerando até parar.
  private readonly intervaloInicial: number = 0.05;
  private readonly intervaloFinal: number = 0.22;

  onStart(): void {
    if (this.titulo) {
      this.imgTitulo = this.titulo.getComponent("Image") as APJS.Image;
    }
    if (this.cartas) {
      this.imgCartas = this.cartas.getComponent("Image") as APJS.Image;
    }
    if (this.imgCartas && this.sequenciaCartas) {
      this.imgCartas.texture = this.sequenciaCartas;
    }
    if (this.sequenciaCartas) {
      this.provider = this.sequenciaCartas.getControl() as APJS.AnimatedTextureProvider;
    }
    if (this.provider) {
      this.totalCartas = this.provider.getFrameCount();
    }
    if (!this.imgTitulo || !this.imgCartas || !this.provider || this.totalCartas < 2) {
      // Aviso no painel de log (se existir). Se aparecer, revise o Inspector.
      if (typeof console !== "undefined") {
        console.log(
          "[Torcedometro] Falta ligar algo no Inspector (Titulo, Cartas ou Sequencia Cartas). Quadros: " +
            this.totalCartas
        );
      }
    }

    const emissor = APJS.EventManager.getGlobalEmitter();
    emissor.on(APJS.EventType.Touch, this.aoTocar);
    emissor.on(APJS.EventType.RecordStart, this.aoComecarGravacao);

    this.voltarAoTitulo();
  }

  onUpdate(deltaTime: number): void {
    if (this.estado === 1) {
      // Título sumindo
      this.relogio += deltaTime;
      const p = this.tempoSomeTitulo > 0 ? Math.min(this.relogio / this.tempoSomeTitulo, 1) : 1;
      if (this.imgTitulo) {
        this.imgTitulo.opacity = 1 - p;
      }
      if (p >= 1) {
        if (this.titulo) {
          this.titulo.enabled = false;
        }
        this.comecarGiro();
      }
      return;
    }

    if (this.estado === 2) {
      // Cartas girando
      this.relogio += deltaTime;
      this.desdeUltimaTroca += deltaTime;
      const p = Math.min(this.relogio / Math.max(this.tempoGiro, 0.1), 1);
      const intervalo =
        this.intervaloInicial + (this.intervaloFinal - this.intervaloInicial) * p * p;

      if (this.desdeUltimaTroca >= intervalo) {
        this.desdeUltimaTroca = 0;
        this.mostrarCarta(this.sortearDiferenteDaAtual());
      }

      if (this.relogio >= this.tempoGiro) {
        // Resultado final: sorteio uniforme entre as 26 cartas.
        this.mostrarCarta(this.sortear());
        this.estado = 3;
      }
    }
  }

  onDestroy(): void {
    const emissor = APJS.EventManager.getGlobalEmitter();
    emissor.off(APJS.EventType.Touch, this.aoTocar);
    emissor.off(APJS.EventType.RecordStart, this.aoComecarGravacao);
  }

  // ---------- Eventos ----------

  private aoTocar = (event: APJS.IEvent): void => {
    const toque = event.args[0] as APJS.TouchData;
    if (!toque || toque.phase !== APJS.TouchPhase.Began) {
      return;
    }
    if (this.estado === 0) {
      // Primeiro toque: some o título e depois gira.
      this.relogio = 0;
      this.estado = 1;
    } else if (this.estado === 3 && this.girarDeNovoNoToque) {
      // Toque depois do resultado: gira de novo.
      this.comecarGiro();
    }
    // Durante o sumiço do título ou o giro, o toque é ignorado.
  };

  private aoComecarGravacao = (_event: APJS.IEvent): void => {
    // Ao apertar GRAVAR no TikTok, volta para o título (igual ao template).
    this.voltarAoTitulo();
  };

  // ---------- Ações ----------

  private voltarAoTitulo(): void {
    this.estado = 0;
    this.relogio = 0;
    this.desdeUltimaTroca = 0;
    if (this.titulo) {
      this.titulo.enabled = true;
    }
    if (this.imgTitulo) {
      this.imgTitulo.opacity = 1;
    }
    if (this.cartas) {
      this.cartas.enabled = false;
    }
  }

  private comecarGiro(): void {
    if (!this.provider || this.totalCartas < 2) {
      return;
    }
    this.relogio = 0;
    this.desdeUltimaTroca = 0;
    if (this.cartas) {
      this.cartas.enabled = true;
    }
    this.mostrarCarta(this.sortearDiferenteDaAtual());
    this.estado = 2;
  }

  /** Mostra só o quadro "indice" da sequência (0 = carta_01 … 25 = carta_26). */
  private mostrarCarta(indice: number): void {
    if (!this.provider) {
      return;
    }
    this.cartaAtual = indice;
    this.provider.pause();
    this.provider.playFromTo(indice, indice);
    this.provider.play();
  }

  private sortear(): number {
    return Math.floor(Math.random() * this.totalCartas);
  }

  private sortearDiferenteDaAtual(): number {
    let n = this.sortear();
    if (this.totalCartas > 1) {
      while (n === this.cartaAtual) {
        n = this.sortear();
      }
    }
    return n;
  }
}
