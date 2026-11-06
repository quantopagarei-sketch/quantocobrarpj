# Ordem para a sessão do Claude no PC do Vini (copiar o WhatsApp Business do S22)

Cole o texto abaixo numa sessão do Claude Code rodando NO PC (não na nuvem), numa pasta nova `Documentos\WhatsApp-S22`.

---

Você vai ajudar o Vini a guardar o histórico do WhatsApp Business do Samsung S22 Ultra antigo dele. São conversas reais de clientes: trate tudo como confidencial.

**Regras:**

- Nunca apague, mova ou renomeie nada no celular. Só copie.
- Não envie esses arquivos para nenhum lugar: nada de nuvem, git, e-mail ou sites. Exceção: o pacote final, que o Vini guarda no iCloud Drive dele.
- Não abra nem leia as conversas, a não ser que o Vini peça.
- A chave de 64 dígitos é do Vini. Ele mesmo digita no app. Não grave a chave em arquivo nenhum.

**Passos:**

1. Peça ao Vini para ligar o S22 no PC pelo cabo USB e escolher **Transferindo arquivos** na notificação do celular.
2. No Explorador de Arquivos: **Este Computador › Galaxy S22 Ultra › Armazenamento interno › Android › media › com.whatsapp.w4b**. Copie a pasta **WhatsApp Business** inteira para `Documentos\WhatsApp-S22\copia-1`. Pode demorar. Confira se a cópia tem as subpastas `Databases` e `Media` e se o tamanho bate com o do celular.
3. Avise o Vini que a cópia 1 terminou. Ele vai seguir o Passo 3 do guia (ativar o backup com chave de 64 dígitos no S22 e tocar em Fazer backup). Guia: https://github.com/quantopagarei-sketch/quantocobrarpj/blob/claude/nifty-babbage-xiu79b/arquivo-whatsapp/LEIA-PRIMEIRO.md
4. Quando ele disser que o backup novo terminou: desconecte e reconecte o cabo (o Windows às vezes mostra a lista antiga). Copie de novo a pasta para `Documentos\WhatsApp-S22\copia-2`. Confira se `copia-2\WhatsApp Business\Databases\msgstore.db.crypt15` existe e tem data de hoje.
5. Abra no Chrome ou no Edge o **Arquivo de Clientes**: https://claude.ai/artifact/4dNonxgka9iN13sG1NZbQX
6. No app: **Importar › Backup completo do S22**.
   - Item 1: escolha `copia-2\WhatsApp Business\Databases\msgstore.db.crypt15`.
   - Item 3: escolha a pasta `copia-2\WhatsApp Business\Media`.
   - Peça ao Vini para digitar a chave no item 2 e clicar em **Abrir backup e importar**.
   - Espere o "Pronto" e mande um print do resultado para o Vini.
7. Se o Vini tiver um arquivo de contatos (.vcf), importe em **Nomes dos contatos**.
8. No app: **Backup › Gerar e salvar pacote**. Salve em `Documentos\WhatsApp-S22\` e também no iCloud Drive, se estiver instalado no PC. Se não estiver, avise o Vini para mandar o pacote para o iCloud Drive pelo iPhone.
9. Escreva em `Documentos\WhatsApp-S22\relatorio.md`:
   - quantas conversas, mensagens e documentos o app mostrou;
   - o nome e o tamanho do pacote;
   - qualquer erro que apareceu.
