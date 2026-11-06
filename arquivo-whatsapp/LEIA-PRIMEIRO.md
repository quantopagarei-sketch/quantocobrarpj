# Histórico do WhatsApp Business: como não perder nada

**Vini, esta é a única página que você precisa ler.**

**Resumo:** o WhatsApp **não transfere** o WhatsApp Business de Android para iPhone. Nem o app "Migrar para iOS", nem resetando o iPhone (o próprio WhatsApp diz isso na ajuda dele). Por isso, a saída é tirar o histórico do S22 e guardar no **Arquivo de Clientes**, um app que a equipe fez para você. Nele você:

- acha qualquer cliente digitando **qualquer pedaço do número** (com ou sem o 9);
- lê a conversa inteira;
- abre e reenvia os **PDFs das propostas**;
- anota a situação de cada cliente (proposta enviada, negociando, fechado…).

Tudo fica guardado **só no seu aparelho**. Nada é enviado para a internet.

**Abrir o app:** https://claude.ai/artifact/4dNonxgka9iN13sG1NZbQX

---

## Antes de tudo (1 minuto)

1. **Não desinstale** o WhatsApp Business do S22, **não limpe os dados** dele e **não restaure o S22 de fábrica**. O histórico está lá dentro.
2. **Não resete o iPhone**: não traz o WhatsApp Business e você perderia o que já tem nele.
3. Deixe o S22 carregando.

## Passo 1: salvar já uma cópia dos PDFs (5 min, sem mexer no WhatsApp)

No S22:

1. Abra o app **Meus Arquivos** › **Armazenamento interno** › **Android** › **media** › **com.whatsapp.w4b**.
2. Segure a pasta **WhatsApp Business** › **Compactar**.
3. Mande o .zip para o **Google Drive** (ou ligue o S22 no PC e copie essa pasta).

Isso já guarda todos os PDFs, fotos e áudios. Se o .zip ficar grande demais, compacte só as pastas **Databases** e **Media › WhatsApp Business Documents**.

## Passo 2: proteger as conversas novas do iPhone (2 min)

No iPhone: **WhatsApp Business › Configurações › Conversas › Backup de conversas › Fazer backup agora**.

## Passo 3: gerar no S22 um backup que o app consegue abrir (15 min)

1. Abra o WhatsApp Business **no S22** e confirme seu número. O código chega por SMS no iPhone. Enquanto o S22 estiver ativo, o WhatsApp Business do iPhone fica desconectado. É normal e temporário. Se aparecer **Restaurar**, toque em Restaurar.
2. No S22: **⋮ › Configurações › Conversas › Backup de conversas › Backup criptografado de ponta a ponta › Ativar**.
3. Escolha **Usar chave de criptografia de 64 dígitos**. Não escolha senha nem chave de acesso.
4. **Tire um print da chave** e guarde. Quem tiver essa chave e o arquivo consegue ler as conversas, então não mande para ninguém.
5. Volte em **Backup de conversas** e toque em **Fazer backup**. Espere terminar.
6. Repita o **Passo 1** (Compactar a pasta e mandar para o Drive). Agora o .zip tem o backup novo.

Se o backup criptografado já estava ligado com senha, desative (vai pedir a senha) e ative de novo escolhendo a chave de 64 dígitos.

## Passo 4: devolver o WhatsApp Business para o iPhone (3 min)

No iPhone: abra o WhatsApp Business, confirme o número e toque em **Restaurar** (é o backup do Passo 2). Pronto, o iPhone volta a ser o principal.

Não fique trocando entre os dois celulares: o WhatsApp pode bloquear a confirmação do número por algumas horas.

## Passo 5: importar no Arquivo de Clientes (10 min)

No computador fica mais rápido, mas funciona no iPhone também.

1. Abra o app › **Importar** › **Backup completo do S22**.
2. Escolha o **.zip** do Passo 3 (ou o arquivo `msgstore.db.crypt15`, se copiou pelo PC).
3. Digite a **chave de 64 dígitos** (pode colar com espaços) › **Abrir backup e importar**.
4. **Nomes (opcional):** o backup traz só os números. Para ver os nomes, exporte os contatos e escolha em **Nomes dos contatos (.vcf)**.
   - No S22: **Contatos › Gerenciar contatos › Exportar**.
   - No iPhone: **Contatos › Listas**, segure **Todos os contatos** › **Exportar**.
5. Aba **Backup** › **Gerar e salvar pacote** › guarde no **iCloud Drive**.

Esse pacote é a sua cópia definitiva:

- abre direto no app **Arquivos** do iPhone, com uma pasta por cliente (nome e número), a conversa em texto e os PDFs;
- volta inteiro para o app em qualquer aparelho, em **Importar › Restaurar um pacote salvo**.

## Plano B: sem a chave, conversa por conversa

Com o WhatsApp Business ativo no S22 (Passo 3, item 1):

1. Abra a conversa › **⋮ › Mais › Exportar conversa › Incluir mídia** › salve no Google Drive.
2. No app: **Importar › Conversas exportadas**. Pode escolher várias de uma vez.

Limites do WhatsApp: até 10 mil mensagens por conversa com mídia, e nas conversas longas os PDFs mais antigos podem não vir. Para esses, use **Importar › Ligar PDFs e fotos que faltaram** com o .zip do Passo 1.

## Se você quiser o histórico DENTRO do WhatsApp do iPhone

Só com programa pago de computador, sem apoio do WhatsApp. O mais indicado é o **Tenorshare iCareFone Transfer**, no modo "transferir e mesclar" (cerca de US$ 40 por ano).

- **Riscos:** o programa é fechado e lê todas as conversas dos clientes, pode apagar o que já está no WhatsApp do iPhone e pode falhar.
- **Se for usar:** faça antes os Passos 2 e 5 (pacote salvo) e não apague nada do S22.

## Dúvidas rápidas

- **Os dados vão para algum lugar?** Não. Ficam no navegador do aparelho. A cópia segura é o pacote que você guarda no iCloud Drive.
- **Como busco?** Digite qualquer pedaço do número (ex.: `4321` ou `11 98765`). Também acha por nome, anotação ou, com o botão "Procurar dentro das conversas", por palavra.
- **O cliente apareceu duas vezes** (uma pelo nome, outra pelo número)? Abra o que está pelo nome › aba **Anotações** › coloque o número › **Salvar**. Os dois viram um só.
- **Como reenvio uma proposta antiga?** Abra o PDF › **Enviar…** (ou **Salvar**) › escolha o WhatsApp.
- **Troquei de aparelho?** Abra o app no novo e importe o pacote.
- **A lista apareceu vazia** (navegador limpo, aparelho novo)? Importe o pacote do iCloud Drive e está tudo de volta. Por isso, gere um pacote novo sempre que importar algo.
