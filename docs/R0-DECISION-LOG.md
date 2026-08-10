# Registro de decisões do R0

| Campo | Valor |
|---|---|
| Versão | 1.1 |
| Marco | `R0` — Governança e prontidão interna |
| Responsável pelas decisões | Proprietário do Radar de Perdas |
| Data | 2026-08-10 |
| Revisão jurídica externa | `EXTERNAL_LEGAL_REVIEW_NOT_OBTAINED` |

Este registro contém somente decisões e evidências não sensíveis. Agentes
podem realizar revisão técnica, mas não recebem acesso a dados reais e não
substituem o proprietário nem um profissional jurídico externo como decisores.

## Vocabulário

- `INTERNAL_APPROVED`: aprovado pelo proprietário para o uso interno indicado;
- `INTERNAL_APPROVED_AS_DRAFT`: aprovado internamente apenas como rascunho e
  sujeito às condições registradas;
- `CHANGES_REQUIRED`: requer correção antes de nova decisão;
- `EXTERNAL_LEGAL_REVIEW_NOT_OBTAINED`: nenhum parecer jurídico externo foi
  obtido.

## Decisões documentais

| ID | Documento ou contrato | Versão | Decisão | Responsável | Data | Observações |
|---|---|---:|---|---|---|---|
| `R0-DEC-001` | `PILOT-OFFER.md` | 1.1 | INTERNAL_APPROVED | Proprietário | 2026-08-10 | Mantida para o futuro piloto pago de pelo menos R$ 500; não se aplica ao piloto preliminar gratuito |
| `R0-DEC-002` | `PILOT-REPORT-TEMPLATE.md` | 1.1 | INTERNAL_APPROVED | Proprietário | 2026-08-10 | Aprovado como template interno, sujeito aos dados e campos do piloto |
| `R0-DEC-003` | `PILOT-BASELINE.md` e `PILOT-TIME-LOG.csv` | 1.1 | INTERNAL_APPROVED | Proprietário | 2026-08-10 | Baseline comparável permanece obrigatório antes de alegar produtividade |
| `R0-DEC-004` | `AUDIT-METHOD-v0.1.md` | 0.1 | INTERNAL_APPROVED | Proprietário | 2026-08-10 | Uso restrito a `LP-001` e `LP-002` |
| `R0-DEC-005` | `PRIVACY-PILOT.md` | 1.2-draft | INTERNAL_APPROVED_AS_DRAFT | Proprietário | 2026-08-10 | Risco jurídico residual mantido; este estado não libera dados reais |
| `R0-DEC-006` | `INGEST-CONTRACT-v1-draft.md` | 1.0-draft | INTERNAL_APPROVED_AS_DRAFT | Proprietário | 2026-08-10 | Sujeito à revisão do corpus real; contrato final e parser continuam proibidos |
| `R0-DEC-007` | `ROADMAP.md` | 1.1 | INTERNAL_APPROVED | Proprietário | 2026-08-10 | Planejamento de 300 horas até 07/03/2027 |
| `R0-DEC-008` | Direção local-first em `PRODUCT.md` e `ROADMAP.md` | 0.3 / 1.1 | INTERNAL_APPROVED | Proprietário | 2026-08-10 | Código público sem dados; previews e aplicação protegidos; processamento no navegador |
| `R0-DEC-009` | `PILOT-PRELIMINARY-INVITATION.md` | 1.0 | INTERNAL_APPROVED | Proprietário | 2026-08-10 | Convite separado para o piloto preliminar gratuito; não valida disposição a pagar |
| `R0-DEC-010` | `PILOT-DATA-TERMS-v0.1-draft.md` | 0.1-draft | INTERNAL_APPROVED_AS_DRAFT | Proprietário | 2026-08-10 | Exige aceite contratual externo e todos os componentes de `REAL_DATA_READY` antes de dados reais |

## Decisão de risco do proprietário

| ID | Situação | Decisão | Limites obrigatórios |
|---|---|---|---|
| `R0-RISK-001` | `EXTERNAL_LEGAL_REVIEW_NOT_OBTAINED` | O proprietário aceita prosseguir apenas com preparação interna, contato comercial sem dados e coleta de aceite contratual externo | Não receber dados reais; não alegar parecer externo; manter `REAL_DATA_READY` bloqueado até todas as evidências |

Esta decisão é operacional e interna. Ela não transfere ao cliente riscos que
dependam de lei ou contrato, não confirma a legitimidade de um conjunto de dados
e não dispensa o aceite externo do instrumento de dados.

## Evidências operacionais

| Evidência | Estado | Registro permitido no Git | Condição para conclusão |
|---|---|---|---|
| Oportunidade `OPP-2026-001` | BLOCKED_EXTERNAL | Apenas código, data e resultado do checklist; nunca nome ou contato | Serviço de baixo risco; uma unidade/WhatsApp; 20–50 chats individuais; ao menos 10 solicitações estimadas; horário/SLA conhecidos; decisor operacional disponível; sem saúde, menores, grupos, anexos ou dados sensíveis |
| BitLocker da unidade `C:` | COMPLETE | `verification_date=2026-08-10`; `encryption_state=FULLY_ENCRYPTED`; `protection_state=ON` | Verificação confirmada pelo proprietário; nenhuma saída bruta, protetor ou chave de recuperação foi registrada |
| Instrumento de dados aceito | BLOCKED_EXTERNAL | Referência externa não sensível | Aceite contratual entre cliente e proprietário |
| `REAL_DATA_READY` | BLOCKED | Estado composto em [`GATE-STATUS.md`](GATE-STATUS.md) | Todos os componentes devem estar concluídos antes do recebimento de dados reais |

## Regras para novas entradas

- alterar uma decisão somente em nova linha, preservando o histórico;
- registrar o identificador da decisão substituída;
- não incluir PII, dados comerciais sensíveis, conversas, hashes reais,
  caminhos privados ou chaves de recuperação;
- manter documentos externos fora do Git e referenciá-los somente por código
  não sensível;
- nunca promover um gate externo ou administrativo sem evidência verificável.
