# Roadmap de conclusão e produção — Radar de Perdas

| Campo | Valor |
|---|---|
| Versão | 1.0 |
| Horizonte | 2026-08-03 a 2027-02-07 |
| Capacidade planejada | 10 horas por semana |
| Orçamento total | 260 horas |
| Responsável | Consultor do Radar de Perdas |
| Status | Em execução; `R0` aguardando aprovações |
| Última revisão | 2026-08-03 |

Este roadmap ordena a validação comercial, metodológica, técnica e operacional.
As datas são metas de planejamento. Somente os gates de
[`GATE-STATUS.md`](GATE-STATUS.md) autorizam o início da etapa seguinte.

## 1. Resultado pretendido

A produção v1 será uma ferramenta de uso interno do consultor com:

- análise exclusiva de `LP-001` e `LP-002`;
- interface hospedada e protegida no Cloudflare Pages;
- processamento integral das conversas no navegador;
- nenhum banco, backend, upload de conversas, telemetria ou integração;
- persistência por arquivo local criptografado;
- exportação experimental em HTML e CSV redigidos;
- PDF contratado produzido manualmente a partir do template aprovado;
- beta após o primeiro piloto pago e os gates técnicos;
- versão estável após um segundo piloto independente e o gate final.

Clientes não acessarão o software na v1. Neon, Supabase e outros bancos ficam
adiados até nova decisão arquitetural posterior à validação.

## 2. Princípios de execução

1. Gate prevalece sobre data.
2. Dados reais nunca entram no Git, em fixture, log, issue ou PR.
3. Holdout privado não é consultado durante a implementação.
4. Um marco atrasado desloca todos os marcos dependentes.
5. Cada marco de implementação usa branch e draft PR próprios.
6. Nenhum desenvolvimento personalizado entra no piloto.
7. Custo mensal de infraestrutura permanece igual a zero até nova autorização.
8. Não se declara ganho de produtividade sem baseline comparável.

## 3. Cronograma

| Marco | Período | Horas | Estado | Entrega e condição de saída |
|---|---:|---:|---|---|
| `R0` — Governança e preparação | 03–16/08/2026 | 20 | IN_PROGRESS | Documentos e roadmap revisados; BitLocker verificado; validação jurídica iniciada; aprovações registradas |
| `R1` — Piloto comercial manual | 17/08–13/09/2026 | 40 | BLOCKED | Oferta apresentada e aceita; instrumento de dados aprovado; R$ 500 recebidos; relatório e avaliação concluídos |
| `R2` — Corpus e contrato final | 14/09–04/10/2026 | 30 | BLOCKED | Corpus segregado; matriz coberta; holdout preservado; `radar.ingest/v1` final aprovado |
| `R3` — Parser CLI | 05/10–01/11/2026 | 40 | BLOCKED | CLI offline e relatório de qualidade aprovados no corpus e no holdout |
| `R4` — Vertical slice web | 02/11–13/12/2026 | 60 | BLOCKED | Workflow local-first, workspace criptografado e exportações aprovados em preview protegido |
| `R5` — Primeiro uso assistido e beta | 14/12/2026–10/01/2027 | 30 | BLOCKED | Medição assistida concluída; gate de continuidade aprovado; `v0.1.0-beta.1` publicada |
| `R6` — Segundo piloto e produção estável | 11/01–07/02/2027 | 40 | BLOCKED | Piloto independente e hardening concluídos; gate final aprovado; `v1.0.0` publicada |

Total planejado:

```text
20 + 40 + 30 + 40 + 60 + 30 + 40 = 260 horas
```

Horas de espera por cliente, jurídico ou revisão não consomem a capacidade de
execução, mas podem alterar as datas.

## 4. Marcos detalhados

### R0 — Governança e preparação

Entregas:

- revisar oferta, relatório, baseline, metodologia, privacidade e contrato draft;
- registrar aprovação ou mudanças requeridas para cada documento;
- verificar BitLocker em terminal administrativo;
- definir responsável jurídico e referência externa do instrumento de dados;
- identificar empresa e contato qualificados;
- manter este roadmap e `GATE-STATUS.md` coerentes.

Gate de saída:

- documentos comerciais e metodológicos aprovados;
- protocolo encaminhado à validação jurídica;
- BitLocker com proteção ativa;
- oportunidade comercial identificada;
- nenhum bloqueio interno sem responsável.

### R1 — Piloto comercial manual

Entregas:

- enviar a oferta de R$ 500 a uma empresa qualificada;
- receber aceite, primeira parcela e insumos completos;
- executar auditoria manual de até 50 chats;
- registrar o baseline em `PILOT-TIME-LOG.csv`;
- entregar relatório manual em PDF;
- realizar apresentação e avaliação do comprador;
- concluir correções factuais e receber o pagamento restante.

Gate de saída:

- pagamento total de pelo menos R$ 500;
- utilidade mínima de 4/5;
- compreensão mínima de quatro respostas corretas em cinco;
- esclarecimento após leitura de no máximo 15 minutos;
- fornecimento legítimo e operação jurídica considerados viáveis.

### R2 — Corpus e contrato final

Entregas:

- manter dados reais exclusivamente na raiz operacional do piloto;
- separar quatro exportações de desenvolvimento, duas de regressão e duas de
  validação privada;
- revisar saídas esperadas linha a linha;
- completar a matriz obrigatória de formatos e casos;
- revisar o draft sem consultar o holdout durante a futura implementação;
- criar e aprovar `INGEST-CONTRACT-v1.md`.

Gate de saída:

- contrato final congelado;
- corpus de desenvolvimento e regressão utilizável sem dados reais no Git;
- holdout sob responsabilidade do revisor;
- schema `radar.ingest/v1` aprovado;
- implementação do parser formalmente autorizada.

### R3 — Parser CLI

Entregas:

- workspace pnpm com Node.js LTS e TypeScript estrito;
- pacote compartilhado de ingestão;
- CLI sem acesso à rede;
- saída JSON, livro de linhas, eventos, avisos, erros e proveniência;
- rejeição integral de variantes incompatíveis;
- scripts oficiais de lint, typecheck, testes e build.

Interface:

```text
radar ingest <arquivo.txt> \
  --timezone America/Sao_Paulo \
  --config <config.json> \
  --output <resultado.json>
```

Códigos de saída:

- `0`: compatível e processado integralmente;
- `2`: formato incompatível;
- `3`: erro ou ambiguidade de parsing;
- `4`: configuração inválida.

Gate de saída:

- contabilidade de linhas igual a 100%;
- precisão e recall iguais a 100%;
- parcialidade igual a zero;
- rejeição explícita igual a 100%;
- sucesso no holdout sem alterar o contrato durante o teste.

### R4 — Vertical slice web

Entregas:

- aplicação React/Vite compartilhando ingestão e regras com o CLI;
- importação de um TXT por vez, até 50 chats no workspace;
- parser executado em Web Worker;
- mapeamento manual de participantes;
- configuração de expediente, feriados, fuso e SLA;
- identificação assistida de solicitações, respostas úteis e `SLA_OVERDUE`;
- sugestões de `LP-001` e `LP-002`;
- revisão de todas as solicitações elegíveis;
- confirmação, rejeição e inclusão manual de achados;
- medição de produtividade;
- exportações HTML e CSV redigidas;
- workspace local criptografado.

Fluxo:

```text
importar
  -> revisar parsing
  -> mapear participantes
  -> configurar expediente e SLA
  -> revisar solicitações
  -> confirmar, rejeitar ou adicionar achados
  -> exportar
```

O preview pode usar apenas fixtures sintéticas e deve permanecer protegido. A
publicação no alias produtivo continua bloqueada até `R5`.

### R5 — Primeiro uso assistido e beta

Ordem de preferência da medição:

1. amostra independente com perfil equivalente;
2. mesma amostra após pelo menos 14 dias, sem exibir resultados anteriores;
3. registro explícito do efeito de aprendizagem;
4. confirmação posterior em um segundo piloto.

Gate de saída:

- parser aprovado;
- primeiro piloto pago;
- nenhuma perda silenciosa;
- `production_active_minutes` reduzido em pelo menos 30%;
- `total_service_minutes` sem aumento;
- descarte automático estritamente menor que 20%;
- achados manuais adicionais estritamente menores que 20%;
- denominadores conclusivos ou nova amostra requerida;
- revisão de segurança e privacidade aprovada.

Com o gate aprovado, publicar `v0.1.0-beta.1` para uso interno assistido.

### R6 — Segundo piloto e produção estável

Entregas:

- executar segundo piloto pago com empresa ou amostra independente;
- confirmar qualidade dos achados e produtividade;
- corrigir falhas sem ampliar LPs ou formatos;
- concluir smoke test do ambiente protegido;
- registrar limitações do free tier e procedimento de contingência;
- produzir relatório final do gate;
- reavaliar persistência remota sem presumir adoção ou custo.

Gate de saída:

- todos os critérios de `R5` confirmados;
- dois pilotos independentes concluídos;
- operação jurídica e de descarte comprovada;
- nenhum incidente crítico aberto;
- release `v1.0.0` aprovada.

## 5. Arquitetura local-first

### 5.1 Componentes

```text
Repositório privado no GitHub
  -> build e preview protegidos
  -> Cloudflare Pages + Access
  -> aplicação estática no navegador
  -> Web Worker para parsing e regras
  -> memória da sessão
  -> arquivo .radar criptografado
  -> HTML/CSV redigidos
```

Não existirão na v1:

- API de aplicação;
- banco de dados;
- função serverless;
- armazenamento de conversas em nuvem;
- autenticação implementada pelo produto;
- analytics, telemetria, IA ou error tracking;
- integração com WhatsApp, CRM ou agenda.

### 5.2 Fronteira de rede

Cloudflare poderá receber somente:

- requisições dos ativos estáticos;
- IP e metadados técnicos inerentes ao acesso;
- identidade usada pelo Cloudflare Access.

O navegador não poderá transmitir:

- TXT;
- mensagens normalizadas;
- configuração comercial;
- achados;
- relatório;
- senha ou chave do workspace.

A política de conteúdo deve incluir `connect-src 'none'`. Scripts, estilos,
fontes e Web Workers serão servidos pela própria aplicação. Não haverá ativos
externos nem source maps públicos de produção.

### 5.3 Hospedagem

- repositório GitHub privado;
- produção baseada na branch `main`;
- previews de PR protegidos;
- domínio gratuito `pages.dev`;
- Cloudflare Access limitado aos usuários aprovados;
- nenhum domínio pago obrigatório;
- nenhum recurso cobrado habilitado.

Referências oficiais:

- [limites do Cloudflare Pages](https://developers.cloudflare.com/pages/platform/limits/);
- [integração do Pages com GitHub](https://developers.cloudflare.com/pages/configuration/git-integration/github-integration/);
- [preço e limite do Cloudflare Access](https://www.cloudflare.com/plans/zero-trust-services/);
- [proteção do domínio pages.dev](https://developers.cloudflare.com/pages/platform/known-issues/).

O free tier não possui SLA. Essa limitação é aceita para a produção assistida e
deve ser reavaliada antes de tornar o produto crítico para a operação.

GitHub Pages fica excluído como hospedagem comercial devido às
[restrições documentadas de uso](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits).

Durante os marcos documentais, GitHub Pages pode publicar exclusivamente um
painel público de qualidade gerado por GitHub Actions. Esse painel:

- contém somente contagens e estados agregados da última validação verde;
- não recebe arquivos, não executa parsing e não contém conteúdo de conversa;
- não é preview, beta, produção nem interface do produto;
- depende de o plano da conta permitir Pages a partir do repositório privado;
- permanece desativado, mantendo somente a CI, se essa elegibilidade não existir.

Essa exceção documental não antecipa `R4` e não altera a hospedagem definida para
a aplicação, que continua sendo Cloudflare Pages com Access.

## 6. Contratos públicos

### 6.1 Ingestão

O parser implementará o schema versionado:

```text
radar.ingest/v1
```

Mudanças incompatíveis exigem novo schema e nova validação; expected outputs não
podem ser alterados sem revisão.

### 6.2 Workspace

O arquivo local terá:

```text
extensão: .radar
schema: radar.workspace/v1
cifra: AES-256-GCM
derivação: PBKDF2-HMAC-SHA-256
iterações: 600000
salt: 16 bytes aleatórios por arquivo
IV: 12 bytes aleatórios por gravação
tag de autenticação: 128 bits
senha mínima: 12 caracteres
```

O envelope não cifrado conterá somente versão, parâmetros criptográficos e
ciphertext. Empresa, participantes, mensagens, configuração e achados ficarão
dentro do conteúdo cifrado.

Regras:

- senha e chave existem somente na memória da sessão;
- conteúdo não é gravado em `localStorage`, IndexedDB ou cache remoto;
- senha incorreta ou arquivo adulterado deve falhar sem produzir estado parcial;
- perda da senha torna o arquivo irrecuperável;
- cada salvamento gera novo IV;
- o arquivo fica em `20-working` e segue a mesma retenção do piloto.

### 6.3 Exportações

- HTML e CSV incluem somente conteúdo redigido e confirmado;
- campos CSV iniciados por `=`, `+`, `-`, `@`, tab ou retorno de carro devem ser
  neutralizados;
- duplicatas não são contadas duas vezes;
- `OUT_OF_SCOPE` não entra nos denominadores;
- o PDF automático permanece fora da v1.

## 7. Qualidade

Quando o runtime existir, a passagem integral deverá executar:

```text
pnpm lint
pnpm typecheck
pnpm test
pnpm build
pnpm test:e2e
pnpm validate:fixtures
pnpm validate:docs
```

Até lá, permanecem obrigatórias as validações documentais de `AGENTS.md`.

Cobertura mínima:

- contrato e contabilidade de todas as linhas;
- expediente, feriados, virada de dia e SLA;
- timestamps iguais e mensagens idênticas consecutivas;
- multilinha, linha vazia e conteúdo semelhante a timestamp;
- Unicode direcional e remetente com dois-pontos;
- eventos, chamadas, mídia omitida, edição e exclusão;
- rejeição de grupo, ZIP, CSV, 12 horas e encoding incompatível;
- round-trip do `.radar`;
- senha incorreta, arquivo truncado, ciphertext adulterado e IV distinto;
- importação, revisão, achado manual, HTML e CSV;
- neutralização de fórmula em CSV e escaping de HTML;
- tentativa de rede bloqueada após o carregamento;
- smoke test com fixture sintética;
- Chrome e Edge atuais no Windows.

O holdout é executado somente pelo revisor no gate final do parser.

## 8. Atualização semanal

Toda revisão semanal deve registrar:

```text
data:
marco:
horas_planejadas:
horas_consumidas:
entregas_concluidas:
evidencias:
bloqueios:
responsavel_pelo_bloqueio:
proxima_acao:
nova_previsao:
```

Regras:

- atualizar o estado somente com evidência;
- não registrar PII, dados comerciais sensíveis ou hashes reais;
- registrar desvios acima de cinco horas;
- replanejar marcos dependentes quando um gate atrasar;
- preservar o orçamento total ou documentar a mudança de escopo.

## 9. Estratégia Git

1. Atualizar `main` com `fetch` e `pull --ff-only`.
2. Criar branch `codex/<slug-descritivo>`.
3. Implementar somente o escopo autorizado.
4. Executar a suíte integral aplicável.
5. Confirmar que `origin/main` é ancestral da branch.
6. Revisar diff, dados, segredos e arquivos fora do escopo.
7. Criar commit convencional e descritivo em português.
8. Fazer push com tracking.
9. Abrir draft PR para `main`.
10. Consultar checks e mergeabilidade após cada push.
11. Não fazer merge, force-push ou rebase destrutivo sem autorização explícita.

Cada marco terá PR própria. Aprovações externas permanecem registradas fora do
repositório, com somente a referência não sensível usada como evidência.

## 10. Decisões adiadas

Após o segundo piloto, uma nova decisão deverá avaliar:

- necessidade real de sincronização entre máquinas;
- banco remoto versus arquivo criptografado;
- região, DPA, subprocessadores, backup e restauração;
- autenticação do produto;
- custo aceitável;
- domínio próprio;
- PDF automático;
- novos indicadores.

O padrão até essa decisão permanece: sem banco e custo mensal de infraestrutura
igual a zero.
