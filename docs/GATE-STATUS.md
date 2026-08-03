# Estado dos gates

| Campo | Valor |
|---|---|
| Versão | 1.1 |
| Responsável | Consultor do Radar de Perdas |
| Última revisão | 2026-08-03 |

Atualize este documento somente com evidência verificável. `PENDING` não
autoriza a etapa seguinte.

| Gate | Estado | Evidência necessária |
|---|---|---|
| `ROADMAP.md` criado | READY_FOR_REVIEW | Documento presente |
| `PILOT-OFFER.md` criado | READY_FOR_REVIEW | Documento presente |
| `PILOT-REPORT-TEMPLATE.md` criado | READY_FOR_REVIEW | Documento presente |
| Baseline e time log criados | READY_FOR_REVIEW | Documentos presentes |
| Metodologia v0.1 criada | READY_FOR_REVIEW | Documento presente |
| Protocolo de privacidade criado | READY_FOR_LEGAL_REVIEW | Documento presente |
| Contrato de ingestão draft criado | READY_FOR_REVIEW | Documento presente |
| Fixtures sintéticas iniciais criadas | COMPLETE | Expected outputs validados |
| Oferta comercial revisada | PENDING | Aprovação registrada |
| Empresa qualificada recebeu a oferta | PENDING | Data e código da oportunidade |
| Piloto aceito | PENDING | Aceite comercial |
| Primeira parcela recebida | PENDING | Comprovante sem dados sensíveis no repositório |
| Instrumento de dados validado | PENDING | Referência externa e aprovação jurídica |
| Relatório e baseline revisados | PENDING | Aprovação registrada |
| Metodologia v0.1 aprovada | PENDING | Responsável e data |
| Contrato de ingestão draft aprovado | PENDING | Responsável e data |
| Roadmap e direção local-first aprovados | PENDING | Responsável e data |
| Corpus real autorizado disponível | BLOCKED_EXTERNAL | Oito exportações e matriz |
| Contrato de ingestão final aprovado | BLOCKED_EXTERNAL | Corpus revisado |
| Parser aprovado no holdout | BLOCKED | Relatório do gate |
| Vertical slice usada em piloto | BLOCKED | Medições manual/assistida |
| Beta local-first aprovada | BLOCKED | Primeiro piloto e gate de continuidade |
| Segundo piloto independente concluído | BLOCKED | Relatório e medições do segundo piloto |
| Produção estável aprovada | BLOCKED | Relatório final do gate e release `v1.0.0` |
| Gate comercial e operacional completo | BLOCKED | Todos os critérios atendidos |
| BitLocker verificado | BLOCKED_ADMIN | Executar `manage-bde -status C:` em terminal administrativo |

## Bloqueios

- Não criar `INGEST-CONTRACT-v1.md` antes da revisão do corpus real.
- Não implementar o parser antes do contrato final aprovado.
- Não implementar a vertical slice antes da aprovação do parser.
- Não criar infraestrutura produtiva antes do gate comercial e operacional.
- Não publicar o alias produtivo antes do gate da beta.
- Não adotar banco ou transmitir conversas sem nova decisão arquitetural,
  contratual e jurídica.
- Não receber arquivos reais enquanto a verificação do BitLocker estiver
  `BLOCKED_ADMIN`.
