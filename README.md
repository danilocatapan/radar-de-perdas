# Radar de Perdas

| Campo | Valor |
|---|---|
| Versão | 0.2 |
| Responsável | Proprietário do Radar de Perdas |
| Status | `R0` em execução; pacote documental aprovado internamente; saída bloqueada |

Projeto para validar e, somente depois dos gates comerciais, metodológicos,
contratuais, operacionais e de privacidade, automatizar auditorias de
atendimento comercial por WhatsApp.

## Estado atual

O repositório está na etapa de preparação do piloto. Nesta etapa são permitidos:

- oferta comercial;
- convite para piloto preliminar gratuito;
- modelo de relatório manual;
- baseline e medição de produtividade;
- metodologia LP-001/LP-002;
- protocolo operacional de privacidade;
- instrumento de tratamento de dados em rascunho;
- contrato de ingestão em rascunho;
- registro não sensível de decisões internas;
- fixtures exclusivamente sintéticas.

O parser, a vertical slice e qualquer infraestrutura produtiva estão bloqueados
até o atendimento dos critérios registrados em
[`docs/GATE-STATUS.md`](docs/GATE-STATUS.md).

O pacote documental atual inclui o
[`convite do piloto preliminar`](docs/PILOT-PRELIMINARY-INVITATION.md), a
[`oferta comercial paga`](docs/PILOT-OFFER.md), o
[`instrumento de dados em rascunho`](docs/PILOT-DATA-TERMS-v0.1-draft.md) e o
[`registro de decisões do R0`](docs/R0-DECISION-LOG.md).

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

O GitHub Pages publica o
[painel público de qualidade](https://danilocatapan.github.io/radar-de-perdas/)
após uma passagem verde na `main`. O painel não é o produto, não recebe arquivos
e não substitui o futuro preview protegido no Cloudflare Pages.

O deploy usa GitHub Actions e depende da variável de repositório
`PAGES_ENABLED=true`. O repositório público contém somente código, documentos e
fixtures sintéticas; dados reais e o holdout privado continuam proibidos.

## Roadmap

O plano de conclusão entre agosto de 2026 e março de 2027 está em
[`docs/ROADMAP.md`](docs/ROADMAP.md). Ele define:

- piloto preliminar gratuito e, depois, piloto comercial pago antes do software;
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
qualquer arquivo real. O recebimento permanece proibido enquanto
`REAL_DATA_READY` estiver diferente de `COMPLETE`.
