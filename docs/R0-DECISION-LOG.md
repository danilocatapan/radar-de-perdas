# Registro de decisões do R0

| Campo | Valor |
|---|---|
| Versão | 1.5 |
| Marco | `R0` — Governança e prontidão interna |
| Responsável pelas decisões | Proprietário do Radar de Perdas |
| Última atualização | 2026-08-11 |
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
| `R0-DEC-011` | `ROADMAP.md` | 2.0 | INTERNAL_APPROVED | Proprietário | 2026-08-10 | Substitui `R0-DEC-007`: validação real precede automação; 300 horas e 07/03/2027 deixam de ser compromissos; `R2+` depende de `GO` |
| `R0-DEC-012` | Pivot para recuperação de oportunidades comerciais | 1.0 | INTERNAL_APPROVED | Proprietário | 2026-08-10 | Substitui a auditoria LP-001/LP-002 como proposta central; não representa evidência de mercado |
| `R0-DEC-013` | `R1A-DISCOVERY.md`, novo convite e `DISCOVERY_SESSION_READY` | 1.0 | INTERNAL_APPROVED | Proprietário | 2026-08-10 | Autoriza preparar cinco sessões sem custódia; não autoriza produto, teste pago ou dados no Git |
| `R0-DEC-014` | Aquisição local/relacional e mesma vertical no R1A | 1.0 | INTERNAL_APPROVED | Proprietário | 2026-08-11 | Cinco participantes da mesma vertical; seleção permanece `PENDING_OWNER_SELECTION`; aquisição por rede pessoal, indicações, bairro e cidade, sem mídia paga |
| `R0-DEC-015` | `R1B-COMMERCIAL-EXPERIMENT.md` e hipótese de R$ 49,90/mês | 1.0 | INTERNAL_APPROVED | Proprietário | 2026-08-11 | `HYPOTHESIS_ONLY`; até 30 dias gratuitos, sem cartão obrigatório ou cobrança automática; substitui a hipótese vigente de R$ 149 por sete dias; execução bloqueada até R1A PASS e nova decisão |
| `R0-DEC-016` | Gates comerciais, regras de STOP e bloqueios técnicos | 1.0 | INTERNAL_APPROVED | Proprietário | 2026-08-11 | `0=STOP`, `1=INSUFFICIENT_EVIDENCE`, `>=2=COMMERCIAL_SIGNAL_TO_INVESTIGATE`; STOP encerra a etapa atual; produto continua bloqueado |
| `R0-DEC-017` | Reavaliação competitiva e wedge `MOBILE_FIELD_PROVIDER_NO_CRM` | 1.0 | INTERNAL_APPROVED | Proprietário | 2026-08-11 | Não competir como CRM horizontal nem buscar paridade de features; R1A passa a diagnosticar dispositivo principal, WhatsApp Web e aceitação de ferramenta externa; categoria existente não valida demanda pelo Radar |
| `R0-DEC-018` | R1B como `PAID_ASSISTED_PILOT` de 30 dias por R$ 99 antecipados | 2.0 | INTERNAL_APPROVED | Proprietário | 2026-08-11 | `PAID_PILOT_PRICE=R$99.00` e `HYPOTHESIS_ONLY`; substitui a hipótese comercial de `R0-DEC-015` sem alterá-la retroativamente; sem período gratuito pós-R1A, cartão obrigatório ou renovação automática; execução continua bloqueada |

## Efeito do pivot sobre decisões anteriores

- `R0-DEC-001`, `R0-DEC-002`, `R0-DEC-003`, `R0-DEC-004` e `R0-DEC-009`
  permanecem preservadas como decisões históricas, mas seus materiais estão
  `SUPERSEDED` para o `R1A` atual.
- `R0-DEC-006` e `R0-DEC-008` não definem arquitetura vigente; ingestão,
  parser e direção técnica continuam bloqueados.
- `R0-DEC-005` e `R0-DEC-010` permanecem rascunhos condicionais para eventual
  recebimento futuro de arquivos. Eles não se aplicam à sessão sem custódia e
  não foram promovidos a parecer jurídico.
- A oportunidade `OPP-2026-001` poderá ser considerada no novo discovery apenas
  se atender ao ICP e ao checklist atuais. Os antigos requisitos de 20–50 chats,
  exportação e SLA não são critérios do `R1A` pivotado.
- `R0-DEC-014`, `R0-DEC-015` e `R0-DEC-016` evoluem incrementalmente o
  Discovery Concierge aprovado em `R0-DEC-012/013`; não repivotam o R1A.
- `R0-DEC-017` registra a reavaliação competitiva sem alegar evidência de
  demanda. `R0-DEC-018` substitui somente a hipótese comercial vigente de
  `R0-DEC-015`: R$ 49,90/mês e seu período gratuito tornam-se `SUPERSEDED`.
- R$ 149 por sete dias deixa de ser hipótese vigente. A oferta de R$ 500 e as
  decisões que a registraram permanecem preservadas como histórico
  `SUPERSEDED`, sem alteração retroativa.

## Decisão de risco do proprietário

| ID | Situação | Decisão | Limites obrigatórios |
|---|---|---|---|
| `R0-RISK-001` | `EXTERNAL_LEGAL_REVIEW_NOT_OBTAINED` | O proprietário aceita prosseguir apenas com preparação interna, contato comercial sem dados e coleta de aceite contratual externo | Não receber dados reais; não alegar parecer externo; manter `REAL_DATA_READY` bloqueado até todas as evidências |

Esta decisão é operacional e interna. Ela não transfere ao cliente riscos que
dependam de lei ou contrato, não confirma a legitimidade de um conjunto de dados
e não dispensa o aceite externo do instrumento de dados.

## Evidências operacionais do plano anterior

A tabela abaixo permanece sem alteração retroativa para preservar o histórico.
Ela não define a qualificação do `R1A` pivotado.

| Evidência | Estado | Registro permitido no Git | Condição para conclusão |
|---|---|---|---|
| Oportunidade `OPP-2026-001` | BLOCKED_EXTERNAL | Apenas código, data e resultado do checklist; nunca nome ou contato | Serviço de baixo risco; uma unidade/WhatsApp; 20–50 chats individuais; ao menos 10 solicitações estimadas; horário/SLA conhecidos; decisor operacional disponível; sem saúde, menores, grupos, anexos ou dados sensíveis |
| BitLocker da unidade `C:` | COMPLETE | `verification_date=2026-08-10`; `encryption_state=FULLY_ENCRYPTED`; `protection_state=ON` | Verificação confirmada pelo proprietário; nenhuma saída bruta, protetor ou chave de recuperação foi registrada |
| Instrumento de dados aceito | BLOCKED_EXTERNAL | Referência externa não sensível | Aceite contratual entre cliente e proprietário |
| `REAL_DATA_READY` | BLOCKED | Estado composto em [`GATE-STATUS.md`](GATE-STATUS.md) | Todos os componentes devem estar concluídos antes do recebimento de dados reais |

## Evidências vigentes do R0-PIVOT

| Evidência | Estado | Registro permitido no Git | Condição para conclusão |
|---|---|---|---|
| Kit documental do `R1A` | COMPLETE | Documentos, CSV vazio e resultado das validações | Suíte documental integral verde, sem alegar validação externa |
| Seleção da vertical | PENDING_OWNER_SELECTION | Estado e referência não identificável da decisão | Proprietário escolhe uma vertical com capacidade de recrutar cinco prestadores reais |
| Primeira sessão | BLOCKED | Apenas código, data e resultado de qualificação | `VERTICAL_SELECTION=COMPLETE`, prestador da vertical escolhida e `DISCOVERY_SESSION_READY=READY`; nenhum conteúdo de conversa |
| Cinco sessões | BLOCKED_EXTERNAL | Somente contagens agregadas e referência confidencial | Sessões e follow-ups concluídos sem dados reais no Git |

## Regras para novas entradas

- alterar uma decisão somente em nova linha, preservando o histórico;
- registrar o identificador da decisão substituída;
- não incluir PII, dados comerciais sensíveis, conversas, hashes reais,
  caminhos privados ou chaves de recuperação;
- manter documentos externos fora do Git e referenciá-los somente por código
  não sensível;
- nunca promover um gate externo ou administrativo sem evidência verificável.
