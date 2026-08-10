# Estado dos gates

| Campo | Valor |
|---|---|
| Versão | 2.2 |
| Responsável | Proprietário do Radar de Perdas |
| Última revisão | 2026-08-10 |

Atualize este documento somente com evidência verificável. Estados `PENDING`,
`BLOCKED`, `BLOCKED_ADMIN` ou `BLOCKED_EXTERNAL` não autorizam a etapa seguinte.
A decisão interna do proprietário não equivale a parecer jurídico externo.

Estados de decisão documental:

- `INTERNAL_APPROVED`: aprovado pelo proprietário para o uso interno indicado;
- `INTERNAL_APPROVED_AS_DRAFT`: aprovado internamente apenas como rascunho,
  sujeito às condições registradas;
- `CHANGES_REQUIRED`: requer correção antes de nova decisão;
- `EXTERNAL_LEGAL_REVIEW_NOT_OBTAINED`: nenhum parecer jurídico externo foi
  obtido; o risco residual e seus limites devem permanecer explícitos.

## R0 — Governança e prontidão interna

| Gate | Estado | Evidência verificável |
|---|---|---|
| Registro de decisões do R0 criado | COMPLETE | [`R0-DECISION-LOG.md`](R0-DECISION-LOG.md) |
| Oferta comercial revisada internamente | INTERNAL_APPROVED | Decisão `R0-DEC-001` |
| Relatório e baseline revisados internamente | INTERNAL_APPROVED | Decisões `R0-DEC-002` e `R0-DEC-003` |
| Metodologia v0.1 aprovada internamente | INTERNAL_APPROVED | Decisão `R0-DEC-004` |
| Protocolo de privacidade revisado internamente | INTERNAL_APPROVED_AS_DRAFT | Decisão `R0-DEC-005` |
| Contrato de ingestão draft aprovado internamente | INTERNAL_APPROVED_AS_DRAFT | Decisão `R0-DEC-006`; sujeito ao corpus real |
| Roadmap e direção local-first aprovados internamente | INTERNAL_APPROVED | Decisões `R0-DEC-007`, `R0-DEC-008` e `R0-DEC-011` |
| Convite gratuito aprovado internamente | INTERNAL_APPROVED | Decisão `R0-DEC-009` |
| Instrumento de dados aprovado internamente como draft | INTERNAL_APPROVED_AS_DRAFT | Decisão `R0-DEC-010`; aceite externo continua pendente |
| Situação da revisão jurídica externa registrada | EXTERNAL_LEGAL_REVIEW_NOT_OBTAINED | Decisão `R0-RISK-001` |
| Decisão de risco do proprietário registrada | INTERNAL_APPROVED | Decisão `R0-RISK-001`; não libera dados reais |
| Oportunidade qualificada identificada | BLOCKED_EXTERNAL | Código reservado `OPP-2026-001`; checklist de qualificação ainda sem evidência |
| BitLocker verificado | COMPLETE | Verificação do proprietário em 2026-08-10: `encryption_state=FULLY_ENCRYPTED`; `protection_state=ON`; sem saída bruta ou chave de recuperação |
| Gate de saída do R0 | BLOCKED | Depende exclusivamente da oportunidade qualificada `OPP-2026-001` |

A próxima ação obrigatória é qualificar `OPP-2026-001` sem solicitar ou receber
dados reais. O encerramento de `R0` comprova prontidão interna, mas não libera
dados reais e não substitui `REAL_DATA_READY`.

## R1A — Piloto manual de operação e utilidade

| Gate | Estado | Evidência verificável |
|---|---|---|
| Convite gratuito criado e aprovado internamente | INTERNAL_APPROVED | Decisão `R0-DEC-009` |
| Instrumento de dados aprovado internamente como draft | INTERNAL_APPROVED_AS_DRAFT | Decisão `R0-DEC-010` |
| Empresa qualificada recebeu o convite | BLOCKED_EXTERNAL | Data e código da oportunidade, sem PII |
| Piloto gratuito aceito | BLOCKED_EXTERNAL | Aceite comercial externo referenciado sem dados sensíveis |
| Instrumento de dados contratualmente aceito | BLOCKED_EXTERNAL | Referência externa do aceite entre cliente e proprietário |
| `REAL_DATA_READY` | BLOCKED | Todos os componentes da tabela específica concluídos |
| Auditoria manual gratuita concluída | BLOCKED | Relatório, apresentação, tempo gasto, feedback e limitações |
| Utilidade, compreensão e esclarecimento aprovados | BLOCKED | Utilidade ≥4/5; compreensão ≥4 de 5 respostas; esclarecimento ≤15 min |

`R1A` é um experimento manual único de validação operacional e de utilidade. Não
possui gate de preço ou disposição a pagar, não autoriza automação e não deve ser
seguido por nova amostra gratuita automática. A disposição a pagar permanece
exclusiva de `R1B`.

### Gate composto `REAL_DATA_READY`

| Componente | Estado | Evidência verificável |
|---|---|---|
| Instrumento de dados contratualmente aceito | BLOCKED_EXTERNAL | Referência externa não sensível |
| Escopo conferido | PENDING | Checklist excluindo grupos, anexos, saúde, menores e dados sensíveis |
| Retenção registrada | PENDING | Data limite de 30 dias após a entrega |
| Canal criptografado testado | PENDING | Mídia USB criptografada e senha transmitida separadamente |
| Diretório operacional e ACL aprovados | PENDING | Checklist operacional sem caminho privado no Git |
| BitLocker ativo | PENDING | Evidência do R0 existe; revalidar `FULLY_ENCRYPTED` e `ON` para o piloto concreto, sem reutilização automática |
| Resultado composto | BLOCKED | Somente `COMPLETE` quando todos os componentes estiverem concluídos |

## R1A.1 — Consolidação de aprendizados observados

| Checkpoint | Estado | Evidência verificável |
|---|---|---|
| Problemas reais registrados | BLOCKED | Lista agregada, sem PII ou conteúdo de conversa |
| Gargalos e tempo gasto registrados | BLOCKED | Atividades observadas e baseline manual |
| Feedback e limitações consolidados | BLOCKED | Síntese não sensível do piloto |
| Mudanças essenciais identificadas | BLOCKED | Somente ajustes necessários ao serviço manual, oferta, metodologia ou operação segura |
| Consolidação concluída | BLOCKED | Todos os itens anteriores registrados sem criar novo escopo técnico |

`R1A.1` não é feature, novo piloto ou autorização técnica. Parser, frontend,
infraestrutura, banco, IA, novos LPs e refinamentos estruturais permanecem
pausados.

## R1B — Piloto comercial pago

| Gate | Estado | Evidência verificável |
|---|---|---|
| Oferta de R$ 500 enviada | BLOCKED_EXTERNAL | Data e código da oportunidade |
| Piloto pago aceito | BLOCKED_EXTERNAL | Aceite comercial |
| `REAL_DATA_READY` revalidado para o escopo e período de `R1B` | BLOCKED | Nova decisão composta; o estado de `R1A` não é reutilizado |
| Primeira parcela recebida | BLOCKED_EXTERNAL | Comprovante mantido fora do repositório |
| Pagamento total de pelo menos R$ 500 | BLOCKED_EXTERNAL | Referência não sensível |
| Relatório e avaliação concluídos | BLOCKED | Relatório redigido e medições aprovadas |
| Gate comercial e operacional pago completo | BLOCKED | Todos os critérios de `R1B` atendidos |

`R1B` é obrigatório para comprovar disposição a pagar. Sua conclusão positiva é
necessária para `GO`, mas não libera `R2+` automaticamente. A tentativa de
`R1B` pode fornecer evidência para `PIVOT` ou `STOP` mesmo sem pagamento total.

## Decision Gate — GO, PIVOT ou STOP

| Decisão | Estado | Evidência verificável |
|---|---|---|
| `GO` | BLOCKED | Pagamento total ≥R$ 500; utilidade aprovada; operação manual viável; gargalo repetitivo observado que justifique automação |
| `PIVOT` | BLOCKED | Valor percebido com problema relevante de preço, segmento, `LP-001`/`LP-002`, formato, obtenção dos dados ou custo operacional |
| `STOP` | BLOCKED | Ausência de disposição real a pagar ou inviabilidade econômica da operação manual |
| Decisão única registrada | BLOCKED | Exatamente uma decisão fundamentada em evidências agregadas de `R1A`, `R1A.1` e da tentativa de `R1B` |

Nenhuma decisão foi tomada. `GO` exige todos os seus critérios; pagamento parcial,
intenção de compra ou utilidade isolada não o autorizam. `PIVOT` mantém o backlog
técnico bloqueado até revalidação. `STOP` encerra o compromisso de continuidade.

## R2+ — backlog técnico condicional

Os estados existentes abaixo permanecem inalterados. Eles não formam cronograma,
não possuem datas ou releases comprometidos e somente podem ser considerados
depois de `GO`.

### R2 — Corpus e contrato final

| Gate | Estado | Evidência verificável |
|---|---|---|
| Fixtures sintéticas iniciais criadas | COMPLETE | Expected outputs validados |
| Corpus real autorizado disponível | BLOCKED_EXTERNAL | `GO` registrado e corpus autorizado, segregado e mantido fora do Git |
| Matriz obrigatória coberta | BLOCKED_EXTERNAL | Evidência do corpus sem conteúdo real no Git |
| Contrato de ingestão final aprovado | BLOCKED_EXTERNAL | `GO`, corpus revisado e gate específico concluído |

### R3 — Parser CLI

| Gate | Estado | Evidência verificável |
|---|---|---|
| Implementação do parser autorizada | BLOCKED | `GO`, contrato final aprovado e gargalo de ingestão comprovado |
| Parser aprovado no holdout | BLOCKED | Relatório do gate executado pelo revisor |

### R4 — Vertical slice web

| Gate | Estado | Evidência verificável |
|---|---|---|
| Implementação da vertical slice autorizada | BLOCKED | Parser aprovado no holdout e gargalo de fluxo comprovado |
| Vertical slice usada em piloto | BLOCKED | Medições manual e assistida |

### R5 — Uso assistido condicional

| Gate | Estado | Evidência verificável |
|---|---|---|
| Uso assistido local-first aprovado | BLOCKED | Solução mínima, segurança, privacidade e medição aprovadas |
| Eventual publicação protegida autorizada | BLOCKED | Nova decisão após o gate de uso assistido |

### R6 — Validação independente condicional

| Gate | Estado | Evidência verificável |
|---|---|---|
| Segundo piloto independente concluído | BLOCKED | Relatório e medições do segundo piloto |
| Continuidade técnica aprovada | BLOCKED | Relatório final e nova decisão explícita, sem release previamente comprometido |

## Bloqueios obrigatórios

- Não implementar novas features, parser, frontend, infraestrutura, banco, IA ou
  refinamentos estruturais durante `R1A`.
- Depois de `R1A`, executar somente `R1A.1` e a preparação de `R1B`; `R2+`
  continua bloqueado até `GO`.
- Não criar `INGEST-CONTRACT-v1.md` antes de `GO` e da revisão do corpus real.
- Não implementar o parser antes de `GO` e do contrato final aprovado.
- Não implementar a vertical slice antes da aprovação do parser.
- Não criar infraestrutura produtiva antes de `GO` e dos gates técnicos
  posteriores.
- Não adotar banco, IA ou transmitir conversas sem nova decisão arquitetural,
  contratual, de privacidade e segurança.
- Não receber arquivos reais enquanto `REAL_DATA_READY` estiver diferente de
  `COMPLETE` para o piloto concreto.
- Não considerar a decisão interna do proprietário como parecer jurídico
  externo.
- Automação futura deve resolver somente gargalos repetitivos comprovados em
  pilotos reais.
