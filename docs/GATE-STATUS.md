# Estado dos gates

| Campo | Valor |
|---|---|
| Versão | 2.0 |
| Responsável | Proprietário do Radar de Perdas |
| Última revisão | 2026-08-10 |

Atualize este documento somente com evidência verificável. Estados
`PENDING`, `BLOCKED`, `BLOCKED_ADMIN` ou `BLOCKED_EXTERNAL` não autorizam a
etapa seguinte. A decisão interna do proprietário não equivale a parecer
jurídico externo.

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
| Roadmap e direção local-first aprovados internamente | INTERNAL_APPROVED | Decisões `R0-DEC-007` e `R0-DEC-008` |
| Convite gratuito aprovado internamente | INTERNAL_APPROVED | Decisão `R0-DEC-009` |
| Instrumento de dados aprovado internamente como draft | INTERNAL_APPROVED_AS_DRAFT | Decisão `R0-DEC-010`; aceite externo continua pendente |
| Situação da revisão jurídica externa registrada | EXTERNAL_LEGAL_REVIEW_NOT_OBTAINED | Decisão `R0-RISK-001` |
| Decisão de risco do proprietário registrada | INTERNAL_APPROVED | Decisão `R0-RISK-001`; não libera dados reais |
| Oportunidade qualificada identificada | BLOCKED_EXTERNAL | Código reservado `OPP-2026-001`; checklist de qualificação ainda sem evidência |
| BitLocker verificado | BLOCKED_ADMIN | Registrar apenas data, `encryption_state=FULLY_ENCRYPTED` e `protection_state=ON` |
| Gate de saída do R0 | BLOCKED | Depende da oportunidade qualificada e do BitLocker verificado |

O gate de saída do `R0` comprova prontidão interna. Mesmo quando concluído,
ele não libera dados reais e não substitui `REAL_DATA_READY`.

## R1A — Piloto preliminar gratuito

| Gate | Estado | Evidência verificável |
|---|---|---|
| Convite gratuito criado e aprovado internamente | INTERNAL_APPROVED | Decisão `R0-DEC-009` |
| Instrumento de dados aprovado internamente como draft | INTERNAL_APPROVED_AS_DRAFT | Decisão `R0-DEC-010` |
| Empresa qualificada recebeu o convite | BLOCKED_EXTERNAL | Data e código da oportunidade, sem PII |
| Piloto gratuito aceito | BLOCKED_EXTERNAL | Aceite comercial externo referenciado sem dados sensíveis |
| Instrumento de dados contratualmente aceito | BLOCKED_EXTERNAL | Referência externa do aceite entre cliente e proprietário |
| `REAL_DATA_READY` | BLOCKED | Todos os componentes da tabela específica concluídos |
| Auditoria manual gratuita concluída | BLOCKED | Relatório, apresentação e feedback |
| Utilidade, compreensão e esclarecimento aprovados | BLOCKED | Utilidade ≥4/5; compreensão ≥4 de 5 respostas; esclarecimento ≤15 min |

O `R1A` não possui gate de disposição a pagar. Essa hipótese permanece exclusiva
do piloto pago `R1B`.

### Gate composto `REAL_DATA_READY`

| Componente | Estado | Evidência verificável |
|---|---|---|
| Instrumento de dados contratualmente aceito | BLOCKED_EXTERNAL | Referência externa não sensível |
| Escopo conferido | PENDING | Checklist excluindo grupos, anexos, saúde, menores e dados sensíveis |
| Retenção registrada | PENDING | Data limite de 30 dias após a entrega |
| Canal criptografado testado | PENDING | Mídia USB criptografada e senha transmitida separadamente |
| Diretório operacional e ACL aprovados | PENDING | Checklist operacional sem caminho privado no Git |
| BitLocker ativo | BLOCKED_ADMIN | Data e estados permitidos, sem saída bruta nem chave de recuperação |
| Resultado composto | BLOCKED | Somente `COMPLETE` quando todos os componentes estiverem concluídos |

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

`R2` depende do gate pago de `R1B`; a conclusão de `R1A` não o substitui.

## R2 — Corpus e contrato final

| Gate | Estado | Evidência verificável |
|---|---|---|
| Fixtures sintéticas iniciais criadas | COMPLETE | Expected outputs validados |
| Corpus real autorizado disponível | BLOCKED_EXTERNAL | Quatro exportações de desenvolvimento, duas de regressão e duas de holdout |
| Matriz obrigatória coberta | BLOCKED_EXTERNAL | Evidência do corpus sem conteúdo real no Git |
| Contrato de ingestão final aprovado | BLOCKED_EXTERNAL | Corpus revisado e gate pago concluído |

## R3 — Parser CLI

| Gate | Estado | Evidência verificável |
|---|---|---|
| Implementação do parser autorizada | BLOCKED | Contrato final aprovado |
| Parser aprovado no holdout | BLOCKED | Relatório do gate executado pelo revisor |

## R4 — Vertical slice web

| Gate | Estado | Evidência verificável |
|---|---|---|
| Implementação da vertical slice autorizada | BLOCKED | Parser aprovado no holdout |
| Vertical slice usada em piloto | BLOCKED | Medições manual e assistida |

## R5 — Primeiro uso assistido e beta

| Gate | Estado | Evidência verificável |
|---|---|---|
| Beta local-first aprovada | BLOCKED | Primeiro piloto pago e gate de continuidade |
| Publicação do alias produtivo autorizada | BLOCKED | Gate da beta aprovado |

## R6 — Segundo piloto e produção estável

| Gate | Estado | Evidência verificável |
|---|---|---|
| Segundo piloto independente concluído | BLOCKED | Relatório e medições do segundo piloto |
| Produção estável aprovada | BLOCKED | Relatório final do gate e release `v1.0.0` |

## Bloqueios obrigatórios

- Não criar `INGEST-CONTRACT-v1.md` antes da revisão do corpus real.
- Não implementar o parser antes do contrato final aprovado.
- Não implementar a vertical slice antes da aprovação do parser.
- Não criar infraestrutura produtiva antes do gate comercial e operacional.
- Não publicar o alias produtivo antes do gate da beta.
- Não adotar banco ou transmitir conversas sem nova decisão arquitetural,
  contratual e jurídica.
- Não receber arquivos reais enquanto `REAL_DATA_READY` estiver diferente de
  `COMPLETE`.
- Não considerar a decisão interna do proprietário como parecer jurídico
  externo.
