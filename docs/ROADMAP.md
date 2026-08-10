# Roadmap de validação e backlog condicional — Radar de Perdas

| Campo | Valor |
|---|---|
| Versão | 2.0 |
| Prioridade | `R0 → R1A → R1A.1 → R1B → DECISION GATE → R2+ somente com GO` |
| Responsável | Proprietário do Radar de Perdas |
| Status | `R0` em execução; saída bloqueada exclusivamente por `OPP-2026-001` |
| Última revisão | 2026-08-10 |

Este roadmap prioriza a validação do serviço com clientes reais antes de novos
investimentos em software ou estrutura futura. Somente os gates de
[`GATE-STATUS.md`](GATE-STATUS.md) autorizam a etapa seguinte. Nenhuma data,
estimativa ou hipótese técnica substitui evidência comercial e operacional.

## 1. Resultado pretendido agora

O objetivo atual é comprovar que a auditoria manual de `LP-001` e `LP-002`:

- produz utilidade percebida pelo cliente;
- pode ser executada manualmente com segurança e operação viável;
- possui disposição real a pagar, demonstrada por pagamento total de pelo
  menos R$ 500;
- revela, em pilotos reais, algum gargalo repetitivo que justifique automação.

Parser, frontend, infraestrutura, banco de dados, IA, novos indicadores e
refinamentos estruturais não são entregas atuais. A demonstração sintética já
existente não é produto, não recebe dados arbitrários e não comprova utilidade,
operação ou disposição a pagar.

## 2. Princípios de execução

1. Validação comercial e operacional precede automação.
2. A próxima ação é qualificar `OPP-2026-001` sem solicitar ou receber dados
   reais, encerrando o bloqueio restante de `R0`.
3. Novas features, parser, frontend, infraestrutura e refinamentos estruturais
   ficam pausados durante `R1A`.
4. Depois de `R1A`, somente `R1A.1` e a preparação do teste comercial `R1B`
   podem avançar; o backlog técnico continua bloqueado até decisão `GO`.
5. Automação futura pode resolver somente gargalos repetitivos observados nos
   pilotos reais, nunca problemas hipotéticos.
6. Dados reais nunca entram no Git, em fixture, log, issue, PR ou ferramenta de
   IA. O holdout privado nunca entra no repositório.
7. `REAL_DATA_READY` é obrigatório e deve ser decidido novamente para cada
   piloto, escopo, período e amostra.
8. Nenhum resultado interno equivale a parecer jurídico externo.
9. Não se declara ganho de produtividade sem baseline comparável.
10. Mudança futura de produto, arquitetura relevante, segurança ou escopo deve
    ser registrada como pendência e submetida a nova decisão; não será
    implementada silenciosamente.

## 3. Sequência prioritária

| Ordem | Marco | Estado | Entrega e condição de saída |
|---:|---|---|---|
| 1 | `R0` — concluir preparação | IN_PROGRESS | Qualificar `OPP-2026-001`; BitLocker e decisões internas já possuem evidência |
| 2 | `R1A` — piloto manual real | BLOCKED | Executar um piloto gratuito com `REAL_DATA_READY`, medir operação e utilidade e não inferir disposição a pagar |
| 3 | `R1A.1` — consolidar aprendizados | BLOCKED | Registrar somente problemas reais, gargalos, tempo gasto, feedback e mudanças essenciais |
| 4 | `R1B` — piloto comercial pago | BLOCKED | Testar disposição a pagar e obter pagamento total de pelo menos R$ 500 |
| 5 | `DECISION GATE` | BLOCKED | Registrar exatamente uma decisão: `GO`, `PIVOT` ou `STOP` |
| 6 | `R2+` — backlog condicional | BLOCKED | Considerar somente após `GO`, sem datas, horas ou releases comprometidos |

A estimativa histórica de 300 horas até 07/03/2027 deixa de ser compromisso de
prazo, capacidade ou orçamento. Se houver `GO`, qualquer estimativa técnica será
refeita a partir dos gargalos comprovados e do menor escopo capaz de resolvê-los.

## 4. Marcos de validação

### R0 — concluir preparação e qualificar a oportunidade

Ação prioritária:

- aplicar o checklist de qualificação de `OPP-2026-001`;
- manter nome, contato e informações comerciais fora do Git;
- não solicitar nem receber conversas durante a qualificação;
- registrar no repositório somente código, data e resultado permitido.

Condição de saída:

- oportunidade qualificada com evidência não sensível;
- nenhuma alteração nos controles já aprovados;
- `R0` continua sem autorizar dados reais, que dependem separadamente de
  `REAL_DATA_READY`.

### R1A — piloto manual de operação e utilidade

`R1A` é um experimento único de aprendizagem com serviço executado manualmente.
Ele não é software, demonstração automatizada ou teste de preço.

Entregas:

- obter os aceites externos aplicáveis;
- concluir todos os componentes de `REAL_DATA_READY` antes do recebimento;
- executar auditoria manual de 20 a 50 chats individuais;
- entregar relatório redigido e apresentação de até 60 minutos;
- medir tempo de execução, utilidade, compreensão e esclarecimento;
- registrar feedback e limitações sem perguntar faixa de preço.

Critérios de avaliação:

- utilidade mínima de 4/5;
- compreensão mínima de quatro respostas corretas em cinco;
- esclarecimento após leitura de no máximo 15 minutos;
- operação, tempo gasto, feedback e limitações registrados.

O resultado de `R1A` não valida disposição a pagar e não completa nenhum gate
comercial.

### R1A.1 — consolidar aprendizados observados

Após `R1A`, realizar uma consolidação curta, sem novo ciclo gratuito automático.
Registrar somente:

- problemas efetivamente encontrados;
- gargalos e atividades repetitivas observados;
- tempo ativo gasto por etapa;
- feedback recebido;
- mudanças essenciais para executar `R1B` com segurança e clareza.

Não criar features, parser, frontend, infraestrutura, banco, IA, novos LPs ou
refatorações estruturais. Itens que impliquem mudança de produto, arquitetura,
segurança ou escopo ficam registrados como pendências para decisão explícita.

### R1B — piloto comercial pago

`R1B` é o gate obrigatório de disposição a pagar. Interesse, elogio, intenção de
compra ou aceite sem pagamento não completam o gate.

Entregas:

- enviar a oferta de R$ 500 a uma empresa qualificada;
- obter aceite e primeira parcela;
- revalidar integralmente `REAL_DATA_READY` para o novo escopo e período;
- executar a auditoria manual e registrar o baseline de tempo;
- entregar relatório, apresentação e correções factuais;
- receber o saldo e comprovar fora do Git pagamento total de pelo menos R$ 500;
- reaplicar utilidade, compreensão e esclarecimento.

O término da tentativa comercial leva ao `DECISION GATE`. A conclusão positiva
de `R1B` é necessária para `GO`, mas não o produz automaticamente.

## 5. Decision Gate — GO, PIVOT ou STOP

A decisão deve usar evidências agregadas de `R1A`, `R1A.1` e da tentativa de
`R1B`. Exatamente um resultado deve ser registrado.

### GO

Somente quando todos os critérios estiverem comprovados:

- pagamento total de pelo menos R$ 500;
- utilidade conforme os critérios vigentes;
- execução manual operacionalmente viável;
- gargalo repetitivo observado que justifique automação.

`GO` autoriza apenas avaliar o menor item de `R2+` necessário para o gargalo
comprovado. Não autoriza todo o backlog, expansão de LPs ou a arquitetura
hipotética completa.

### PIVOT

Usar quando houver valor percebido, mas existir problema relevante em um ou mais
destes pontos:

- preço;
- segmento;
- adequação de `LP-001` ou `LP-002`;
- formato da entrega;
- obtenção dos dados;
- custo operacional.

O backlog técnico permanece bloqueado. A hipótese afetada deve ser revista e
revalidada antes de nova decisão.

### STOP

Usar quando não houver disposição real a pagar ou quando o custo operacional
tornar a oferta economicamente inviável. Nesse caso, `R2+` permanece sem
autorização e não existe compromisso de continuar o produto.

Uma tentativa de `R1B` sem pagamento completo pode resultar em `PIVOT` ou
`STOP`; nunca em `GO`.

## 6. R2+ — backlog técnico condicional

Os antigos marcos `R2` a `R6` deixam de ser cronograma e passam a representar
hipóteses condicionais:

| Item | Hipótese condicional | Pré-condição adicional |
|---|---|---|
| `R2` | Revisar corpus autorizado e contrato final de ingestão | `GO` registrado; corpus real revisado sem entrar no Git |
| `R3` | Implementar o menor parser necessário | Contrato final aprovado e gargalo de ingestão comprovado |
| `R4` | Avaliar uma vertical slice local-first | Parser aprovado e gargalo de fluxo comprovado |
| `R5` | Medir uso assistido | Solução mínima aprovada em segurança, privacidade e qualidade |
| `R6` | Confirmar resultado em piloto independente | Evidência suficiente para nova decisão de continuidade |

Nenhum item possui data, orçamento, release ou compromisso de execução. Cada
item depende dos gates anteriores e de nova autorização verificável. Se o
gargalo observado puder ser resolvido manualmente ou por mudança simples de
processo, a automação não se justifica.

## 7. Controles invariáveis de dados, privacidade e segurança

O replanejamento não simplifica os controles necessários para receber dados
reais. Permanecem obrigatórios:

- aceite contratual externo do instrumento de dados;
- escopo que exclua grupos, anexos, saúde, menores e dados sensíveis;
- retenção de 30 dias após a entrega e descarte registrado;
- transferência por mídia USB criptografada, com senha em canal separado;
- diretório operacional fora do Git e de pastas sincronizadas, com ACL restrita;
- BitLocker ativo e revalidado para cada piloto concreto;
- trabalho offline e sem agentes de IA sobre dados reais;
- dados reais e holdout privado sempre fora do Git;
- relatórios e exportações redigidos, com conteúdo mínimo necessário;
- ausência explícita de parecer jurídico externo, sem inferir validação legal.

Se `GO` autorizar uma proposta técnica futura, a direção local-first continua
como limite mínimo até nova decisão arquitetural, contratual e de privacidade:

- processamento integral no navegador, sem upload de conversas;
- nenhuma API, banco, função serverless, telemetria ou integração com dados
  reais;
- workspace local criptografado, com senha e chave somente em memória;
- HTML e CSV apenas com conteúdo redigido e confirmado;
- neutralização de fórmulas em CSV e escaping de HTML;
- `connect-src 'none'`, ativos próprios e ausência de source maps públicos;
- preview e aplicação protegidos, sem confundir o painel documental do GitHub
  Pages com produto ou produção.

Qualquer relaxamento desses controles exige nova decisão explícita e não pode
ser inferido de `GO`.

## 8. Qualidade e governança

Até existir runtime oficial, permanecem obrigatórias as validações documentais
de `AGENTS.md`: JSONs, contabilidade de linhas e `lineLedger`, CSVs, links locais,
privacidade, segredos e `git diff --check`.

Regras de atualização:

- alterar estados somente com evidência verificável;
- registrar apenas estados agregados e referências não sensíveis;
- não publicar PII, dados comerciais sensíveis, conversas ou hashes reais;
- usar branch e draft PR por alteração;
- não fazer merge, force-push ou rebase destrutivo sem autorização explícita.

## 9. Estado operacional atual

```text
data: 2026-08-10
marco: R0
entregas_concluidas: decisões internas; BitLocker verificado; demonstração sintética disponível
bloqueio: qualificação da oportunidade OPP-2026-001
responsavel_pelo_bloqueio: proprietário
proxima_acao: aplicar o checklist de qualificação sem solicitar ou receber dados reais
```

Nenhuma decisão `GO`, `PIVOT` ou `STOP` foi tomada. `R1A`, `R1A.1`, `R1B`, o
`DECISION GATE` e todo o backlog `R2+` permanecem bloqueados.
