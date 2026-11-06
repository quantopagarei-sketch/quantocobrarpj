/**
 * Meu 2027 vai ser (C05): script alternativo de sorteio das respostas
 * (PLANO C do guia-montagem.md, Parte 16.2).
 *
 * NÃO é o caminho principal. O caminho principal é o template Future Life,
 * sem código (Partes 1 a 8 do guia). Use este script só se o sorteio do
 * template ficar viciado, mostrar quadro vazio ou não aceitar as 8 respostas
 * e você não conseguir corrigir isso no Visual Scripting (Parte 7.3).
 *
 * O que ele faz (e só isso):
 *   - Sorteia 1 resposta para cada bolha e deixa a sequência de imagens
 *     parada nesse quadro.
 *   - Sorteia de novo no toque na tela, no biquinho e quando a pessoa aperta
 *     GRAVAR no TikTok (cada gatilho pode ser desligado no Inspector).
 *   - Nunca repete a mesma resposta duas vezes seguidas na mesma bolha.
 *
 * O que ele NÃO faz: não sobe bolha, não estoura bolha, não pinta cor, não
 * mostra nem esconde nada. Tudo isso continua com o template.
 *
 * De onde vieram os nomes da API (APJS):
 *   - Guia oficial "Scripting Capability Usage Guide" (classe com @component()
 *     que estende APJS.BasicScriptComponent; onStart/onUpdate/onDestroy).
 *   - Tutorial oficial "VFX: Tap Burst" (EventManager.getGlobalEmitter(),
 *     EventType.Touch, TouchPhase.Began).
 *   - Arquivos de tipos APJS.d.ts e OrionDecorators.d.ts de um projeto público
 *     do Effect House (github.com/christophusbeck/StatJack). Eles confirmam:
 *     EventType.RecordStart, Texture.getControl(), AnimatedTextureProvider
 *     (playFromTo/pause/play/getFrameCount), AlgorithmManager.getResult(),
 *     getFaceCount(), getFaceBaseInfo(i).hasAction(FaceAction.MouthPout)
 *     e o decorador @serializeProperty.
 *   - A técnica pause → playFromTo(i, i) → play para parar num quadro é a
 *     mesma do script do efeito C01 e do projeto público citado.
 *   - Este arquivo passou na checagem de tipos (tsc) contra esses dois .d.ts.
 *     Ainda NÃO foi rodado dentro do Effect House (a confirmar no Preview).
 *
 * Como ligar (detalhes na Parte 16.2 do guia):
 *   1. Crie um script TypeScript no projeto, cole este conteúdo e salve.
 *   2. Crie um objeto vazio "Sorteio" e adicione este script como componente.
 *   3. No Inspector, ligue as sequências:
 *        Respostas Bolha 1 → seq_amor    (pasta respostas_amor, bolha da esquerda)
 *        Respostas Bolha 2 → seq_grana   (pasta respostas_grana, bolha do meio)
 *        Respostas Bolha 3 → seq_futebol (pasta respostas_futebol, bolha da direita)
 *        Respostas Bolha 4 → seq_carro   (só se existir a 4ª bolha; senão, vazio)
 *   4. No Visual Scripting do template, impeça que os nós Animated Texture
 *      Player escolham o quadro (Parte 16.2, passo 3, do guia), senão os dois
 *      sorteios brigam.
 */

@component()
export class SorteioRespostas2027 extends APJS.BasicScriptComponent {
  // ---------- Campos que aparecem no Inspector ----------

  /** Sequência de respostas da bolha 1 (AMOR, esquerda). */
  @serializeProperty
  public respostasBolha1!: APJS.Texture;

  /** Sequência de respostas da bolha 2 (GRANA, meio). */
  @serializeProperty
  public respostasBolha2!: APJS.Texture;

  /** Sequência de respostas da bolha 3 (FUTEBOL, direita). */
  @serializeProperty
  public respostasBolha3!: APJS.Texture;

  /** Sequência da bolha 4 (CARRO). Deixe vazio na versão de 3 bolhas. */
  @serializeProperty
  public respostasBolha4!: APJS.Texture;

  /** Sorteia de novo quando a pessoa toca na tela. */
  @serializeProperty
  public sortearNoToque: boolean = true;

  /** Sorteia de novo quando a pessoa faz biquinho. */
  @serializeProperty
  public sortearNoBiquinho: boolean = true;

  /** Sorteia de novo quando a pessoa aperta GRAVAR no TikTok. */
  @serializeProperty
  public sortearAoGravar: boolean = true;

  /**
   * Espera (segundos) entre o gatilho e o sorteio. Aumente (ex.: 0.3 ou 0.5)
   * se o template ainda trocar o quadro logo depois do gatilho.
   */
  @serializeProperty
  public atrasoSegundos: number = 0.1;

  /**
   * Tempo mínimo (segundos) entre dois sorteios. Evita que um biquinho
   * comprido ou dois toques seguidos troquem a resposta várias vezes.
   */
  @serializeProperty
  public intervaloMinimo: number = 1.5;

  // ---------- Estado interno ----------

  private providers: APJS.AnimatedTextureProvider[] = [];
  private totais: number[] = [];
  private atuais: number[] = [];
  private faltaParaSortear: number = -1; // -1 = nenhum sorteio agendado
  private desdeUltimoSorteio: number = 999;
  private biquinhoAntes: boolean = false;

  onStart(): void {
    const sequencias: APJS.Texture[] = [
      this.respostasBolha1,
      this.respostasBolha2,
      this.respostasBolha3,
      this.respostasBolha4,
    ];
    for (let i = 0; i < sequencias.length; i++) {
      const seq = sequencias[i];
      if (!seq) {
        continue;
      }
      const p = seq.getControl() as APJS.AnimatedTextureProvider;
      if (!p) {
        continue;
      }
      const total = p.getFrameCount();
      if (total < 1) {
        continue;
      }
      this.providers.push(p);
      this.totais.push(total);
      this.atuais.push(-1);
    }

    if (this.providers.length < 3 && typeof console !== "undefined") {
      // Se aparecer no painel de log, revise os campos do Inspector.
      console.log(
        "[Sorteio2027] Só " + this.providers.length + " sequência(s) ligada(s). O esperado é 3 (ou 4)."
      );
    }

    const emissor = APJS.EventManager.getGlobalEmitter();
    emissor.on(APJS.EventType.Touch, this.aoTocar);
    emissor.on(APJS.EventType.RecordStart, this.aoComecarGravacao);

    // Já deixa uma resposta válida parada em cada bolha desde o início.
    this.sortearTodas();
  }

  onUpdate(deltaTime: number): void {
    this.desdeUltimoSorteio += deltaTime;

    // Biquinho: só conta o momento em que ele começa (borda de subida).
    if (this.sortearNoBiquinho) {
      const biquinhoAgora = this.temBiquinho();
      if (biquinhoAgora && !this.biquinhoAntes) {
        this.agendarSorteio();
      }
      this.biquinhoAntes = biquinhoAgora;
    }

    // Sorteio agendado.
    if (this.faltaParaSortear >= 0) {
      this.faltaParaSortear -= deltaTime;
      if (this.faltaParaSortear < 0) {
        this.faltaParaSortear = -1;
        this.sortearTodas();
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
    if (!this.sortearNoToque) {
      return;
    }
    const toque = event.args[0] as APJS.TouchData;
    if (!toque || toque.phase !== APJS.TouchPhase.Began) {
      return;
    }
    this.agendarSorteio();
  };

  private aoComecarGravacao = (_event: APJS.IEvent): void => {
    if (this.sortearAoGravar) {
      this.faltaParaSortear = -1;
      this.sortearTodas();
    }
  };

  // ---------- Ações ----------

  private agendarSorteio(): void {
    if (this.desdeUltimoSorteio < this.intervaloMinimo) {
      return;
    }
    if (this.faltaParaSortear >= 0) {
      return; // já tem um sorteio agendado
    }
    this.faltaParaSortear = Math.max(this.atrasoSegundos, 0);
  }

  private temBiquinho(): boolean {
    const resultado = APJS.AlgorithmManager.getResult();
    if (!resultado || resultado.getFaceCount() < 1) {
      return false;
    }
    const rosto = resultado.getFaceBaseInfo(0);
    if (!rosto) {
      return false;
    }
    return rosto.hasAction(APJS.FaceAction.MouthPout);
  }

  private sortearTodas(): void {
    for (let i = 0; i < this.providers.length; i++) {
      const novo = this.sortearDiferente(this.totais[i], this.atuais[i]);
      this.atuais[i] = novo;
      this.pararNoQuadro(this.providers[i], novo);
    }
    this.desdeUltimoSorteio = 0;
  }

  /** Deixa a sequência parada no quadro "indice" (0 = arquivo _01). */
  private pararNoQuadro(p: APJS.AnimatedTextureProvider, indice: number): void {
    p.pause();
    p.playFromTo(indice, indice);
    p.play();
  }

  private sortearDiferente(total: number, atual: number): number {
    if (total <= 1) {
      return 0;
    }
    let n = Math.floor(Math.random() * total);
    while (n === atual) {
      n = Math.floor(Math.random() * total);
    }
    return n;
  }
}
