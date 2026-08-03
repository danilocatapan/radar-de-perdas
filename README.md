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

## Testes automatizados

A fundação documental e as fixtures sintéticas podem ser validadas sem iniciar o
parser ou o frontend:

```text
python -m unittest discover -s tests -v
python scripts/validate_repository.py --report artifacts/quality/report.json
```

O workflow `Qualidade` executa a mesma passagem em pushes e pull requests. O
relatório contém somente contagens e estados agregados; mensagens, nomes de
fixtures e caminhos privados não entram no artefato.

O GitHub Pages, quando disponível para o plano da conta, publica apenas um painel
público dessa qualidade agregada após uma passagem verde na `main`. O painel não
é o produto, não recebe arquivos e não substitui o futuro preview protegido no
Cloudflare Pages.

## Roadmap

O plano de conclusão entre agosto de 2026 e fevereiro de 2027 está em
[`docs/ROADMAP.md`](docs/ROADMAP.md). Ele define:

- piloto comercial e auditoria manual antes do software;
- contrato final e parser antes da interface;
- vertical slice local-first sem banco de dados;
- beta após o primeiro piloto pago;
- produção estável após um segundo piloto independente;
- hospedagem estática protegida, sem transmitir conversas.

As datas do roadmap não substituem os gates do produto.

## Regra de dados

Dados reais, ainda que autorizados, nunca devem ser copiados para este
repositório. O diretório operacional do piloto fica fora dele:

```text
C:\Users\catap\RadarDePerdas-Pilotos\<PILOT_ID>\
```

Consulte [`docs/PRIVACY-PILOT.md`](docs/PRIVACY-PILOT.md) antes de receber
qualquer arquivo real.
