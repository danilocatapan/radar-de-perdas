# Radar de Perdas

| Campo | Valor |
|---|---|
| Versão | 0.1 |
| Responsável | Consultor do Radar de Perdas |
| Status | Preparação do piloto |

Projeto para validar e, somente depois dos gates comerciais, metodológicos e
jurídicos, automatizar auditorias de atendimento comercial por WhatsApp.

## Estado atual

O repositório está na etapa de preparação do piloto. Nesta etapa são permitidos:

- oferta comercial;
- modelo de relatório manual;
- baseline e medição de produtividade;
- metodologia LP-001/LP-002;
- protocolo operacional de privacidade;
- contrato de ingestão em rascunho;
- fixtures exclusivamente sintéticas.

O parser, a vertical slice e qualquer infraestrutura produtiva estão bloqueados
até o atendimento dos critérios registrados em
[`docs/GATE-STATUS.md`](docs/GATE-STATUS.md).

## Regra de dados

Dados reais, ainda que autorizados, nunca devem ser copiados para este
repositório. O diretório operacional do piloto fica fora dele:

```text
C:\Users\catap\RadarDePerdas-Pilotos\<PILOT_ID>\
```

Consulte [`docs/PRIVACY-PILOT.md`](docs/PRIVACY-PILOT.md) antes de receber
qualquer arquivo real.
