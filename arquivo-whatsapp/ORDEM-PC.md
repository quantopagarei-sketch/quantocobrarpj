# Ordem para o Claude no PC do Vini: extrair o WhatsApp Business do S22

Cole tudo abaixo da linha numa sessão do **Claude Code rodando no PC** (app Claude no computador › Claude Code), numa pasta nova `Documentos\WhatsApp-S22`.

---

Você vai extrair e guardar o histórico do WhatsApp Business do Samsung S22 do Vini, que já está ligado neste PC pelo cabo USB. O Vini autorizou você a fazer tudo sozinho neste PC: rodar comandos, instalar o que precisar, usar o navegador e o controle do computador. Só chame o Vini quando for impossível sem ele (tocar no celular ou digitar a chave). Nesse caso diga exatamente o que ele precisa tocar, em uma frase.

São conversas reais de clientes. Regras:
- Nunca apague, mova ou renomeie nada no celular. Só copie.
- Não envie esses arquivos para nenhum lugar (nuvem, git, e-mail, sites). A única exceção é o pacote final no iCloud Drive/Google Drive do próprio Vini.
- Não leia as conversas além do necessário para conferir que deu certo.
- Não grave a chave de 64 dígitos em arquivo nenhum.

Passos:

1. **Ferramenta adb.** Baixe https://dl.google.com/android/repository/platform-tools-latest-windows.zip, extraia em `Documentos\WhatsApp-S22\platform-tools` e rode `adb devices`.
   - Se o S22 não aparecer ou aparecer `unauthorized`, peça ao Vini: "No S22, toque em PERMITIR depuração USB".
   - Se a depuração não estiver ligada, peça: "Configurações > Sobre o telefone > Informações do software > toque 7x em Número da versão; depois Opções do desenvolvedor > Depuração USB".
2. **Cópia de segurança imediata.** Rode `adb pull "/sdcard/Android/media/com.whatsapp.w4b/WhatsApp Business" copia-1`. Confira se vieram `Databases` e `Media`, e anote quantos arquivos e quantos MB.
3. **Backup que abre com chave.** Veja o que há em `copia-1\WhatsApp Business\Databases`.
   - Se já houver `msgstore.db.crypt15` de hoje e o Vini tiver a chave de 64 dígitos, pule para o passo 4.
   - Senão, peça ao Vini, numa única mensagem: "No S22, abra o WhatsApp Business (confirme o número se pedir; o código chega no iPhone) › ⋮ › Configurações › Conversas › Backup de conversas › Backup criptografado de ponta a ponta › Ativar › Usar chave de criptografia de 64 dígitos. Tire print da chave. Volte e toque em Fazer backup. Me avise quando terminar."
   - Antes disso, lembre o Vini de fazer o backup do WhatsApp Business do iPhone no iCloud: "iPhone: WhatsApp Business › Configurações › Conversas › Backup de conversas › Fazer backup agora".
   - Quando ele avisar, rode o `adb pull` de novo para `copia-2` e confira se `Databases\msgstore.db.crypt15` tem data e hora de agora.
4. **Importar.** Abra no Chrome ou no Edge: https://claude.ai/artifact/4dNonxgka9iN13sG1NZbQX
   - Vá em Importar › Backup completo do S22.
   - Item 1: o `msgstore.db.crypt15` da cópia mais nova.
   - Item 3: a pasta `Media` da mesma cópia.
   - Peça ao Vini que digite a chave no item 2 (ou cole, se ele mandar a chave para você no chat só para isso) e clique em **Abrir backup e importar**.
   - Espere o "Pronto". Se aparecerem arquivos sem ligação, use "Ligar PDFs e fotos que faltaram" com a pasta `Media`.
5. **Nomes.** Com o adb, gere ou peça um .vcf dos contatos. O mais fácil é pedir ao Vini: "No S22: Contatos › Gerenciar contatos › Exportar". Depois puxe o .vcf com `adb pull` (procure em `/sdcard` por `*.vcf`) e importe em Nomes dos contatos.
6. **Pacote.** Vá em Backup › Gerar e salvar pacote.
   - Salve em `Documentos\WhatsApp-S22\`.
   - Se o iCloud Drive para Windows estiver instalado, copie também para ele. Se não, deixe o pacote no Google Drive do Vini pelo navegador, onde ele já estiver logado.
7. **Devolver o WhatsApp ao iPhone.** Diga ao Vini: "Pode abrir o WhatsApp Business no iPhone, confirmar o número e tocar em Restaurar".
8. **Relatório.** Escreva `Documentos\WhatsApp-S22\relatorio.md` com:
   - quantas conversas, mensagens e documentos o app mostrou;
   - o nome e o tamanho do pacote e onde ele foi salvo;
   - o que deu errado, se algo deu.

   Mande esse resumo ao Vini em 3 linhas.
