# Radar de Perdas

| Campo | Valor |
|---|---|
| Versão | 0.4 |
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

## Comece aqui

O passo a passo operacional está no
[`manual do operador`](docs/OPERATOR-RUNBOOK.md). Ele explica, com entradas,
comandos e resultados esperados:

1. como verificar e registrar o BitLocker sem expor a chave de recuperação;
2. como qualificar `OPP-2026-001` sem colocar a identidade da empresa no Git;
3. como preparar e liberar cada componente de `REAL_DATA_READY`;
4. como executar o piloto manual gratuito `R1A`;
5. por que o piloto pago `R1B` é separado e o que ele precisa comprovar.

No estado atual, a ordem é: verificar BitLocker, qualificar uma oportunidade,
encerrar `R0`, obter os aceites de `R1A` e somente então preparar
`REAL_DATA_READY`. Não solicite nem receba conversas durante a qualificação ou o
convite inicial.

## Demonstração sintética executável

É possível conhecer o fluxo e visualizar resultados agora, sem parser e sem
dados reais:

```powershell
python scripts/run_synthetic_demo.py --output-dir artifacts/synthetic-demo
Start-Process .\artifacts\synthetic-demo\index.html
```

O que entra: cinco chats TXT inteiramente sintéticos e classificações humanas
pré-revisadas. O que acontece: o script valida a consistência dessas anotações,
sem interpretar automaticamente as conversas. O que sai:

- `index.html`, com indicadores, casos, prioridades e limitações;
- `result.json`, usando o schema exclusivo `radar.demo/v1`;
- `findings.csv`, com os dois achados demonstrativos.

A demonstração mostra como o serviço identifica demora (`LP-001`), ausência de
resposta (`LP-002`), casos inconclusivos e itens fora do escopo. Ela não aceita
arquivo arbitrário, não antecipa o parser e não comprova venda ou receita
perdida.

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
