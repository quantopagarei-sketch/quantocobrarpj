# Diário do Agente de SEO

- 2026-10-30: site ligado ao GitHub (deploy automático). Sitemap (23 URLs) reenviado no Search Console (propriedade de prefixo verificada também para quanto.pagarei). Indexação solicitada: /split-payment/, /mei-2027/, /clt-pj/, /clt-pj/5000/. /split-payment/ e /mei-2027/ já estavam no Google. Próximo: páginas novas de cauda longa.
- 2026-10-30 (tarde): site: no buscador = 0 resultados próprios (ainda não aparece na busca usada). Regras conferidas: split payment em testes desde 15/10 (sem adiamento oficial), CBS ~11,3% (TCU), LC 238/2026 ok, salário mínimo 2027 previsto R$ 1.741 (PLOA, não definitivo) — nada a corrigir. Melhoria técnica: schema WebApplication em /mei-2027/ e /split-payment/. Página nova: /mei-passou-do-limite/ (calculadora de excesso + prazo de comunicação, passo a passo, FAQ, fontes Receita). Links internos a partir de /mei-2027/ (card, calculadora, FAQ, rodapé). Sitemap: 24 URLs. Ideias amanhã: DAS MEI 2027 valor (quando o salário mínimo 2027 sair), páginas CLT 5500/6500/7500, fator R Anexo III x V, BreadcrumbList na home.

## PRIORIDADES DEFINIDAS PELO SÓCIO (30/10/2026) — fazer antes das ideias genéricas
1. [FEITO 30/10 pelo sócio] Página "Quem somos" completa (/sobre/): quem mantém o site, missão, como os cálculos são feitos, fontes oficiais, data da última revisão, contato, política de parceiros (comissão) — sinal de confiança (E-E-A-T). Link no rodapé de todas as páginas.
2. [FEITO 30/10: está em /sobre/#metodologia] Página "Metodologia" explicando cada fórmula (INSS, IR, DAS, Simples Anexo III/V, fator R, split payment) com links das fontes oficiais. Link a partir de cada calculadora.
3. Conversão: em cada página-guia, uma caixa "Precisa de contador?" levando ao formulário /#contador (sem pop-up).
4. [FEITO 30/10 pelo sócio — 31 salários no ar] Páginas de salário que faltam em /clt-pj/ (1500, 2200, 2800, 3200, 4200, 5500, 6500, 7500, 11000, 14000, 16000, 22000, 35000) — uma ou duas por dia junto com a página-guia, pois são rápidas e trazem buscas "salário X CLT ou PJ".
5. Nunca remover a tag do Google Analytics (gtag) quando ela existir no <head>.

- 2026-10-30 (sócio): criadas /sobre/ (quem somos + metodologia) e /incorporar/ (calculadora para outros sites via ?embed=pj ou ?embed=split no index.html — NÃO remover o bloco <style id="embed-css"> nem o script de embed do index.html). Corrigido rodapé quebrado de /mei-passou-do-limite/ (faltava fechar <footer>). Arquivo IndexNow na raiz (*.txt de 32 caracteres hex) — não apagar.

- 2026-10-30 (sócio): página inicial focada em dinheiro — seção de promessas de governo movida para /promessas/ (noindex, fora do sitemap; NÃO trazer de volta para a home nem linkar no menu). Caixas "Falar com um contador" (classe .ctabox, data-cta) depois dos resultados das calculadoras CLT x PJ e split; evento GA cta_contador. Replicar a .ctabox nas páginas de salário e guias quando fizer melhoria técnica.
- 2026-10-30 (sócio): +13 páginas de salário (1.500 a 35.000) e tabela atualizada; IndexNow automático via GitHub Actions a cada publicação (.github/workflows/indexnow.yml) — não precisa avisar o Bing manualmente.
- 2026-10-30 (sócio): botão "Mandar esse resultado no WhatsApp" (#pjshare) na calculadora da home, com ?s=salário e utm_source=whatsapp — não remover.
- 2026-10-30 (sócio): REGRA DE CRÉDITOS — cada publicação no Netlify gasta créditos. Faça no máximo UM push com mudanças no site por execução; commits só em seo/*.md terminam com "[skip netlify]".
