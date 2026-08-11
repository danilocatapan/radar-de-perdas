# Radar de Perdas

| Campo | Valor |
|---|---|
| Versão | 0.8 |
| Status | `R1A_READY=COMPLETE`; Discovery Concierge ainda não executado |
| Próximo gate | `VERTICAL_SELECTION=PENDING_OWNER_SELECTION` |

O Radar de Perdas está validando uma ideia simples para prestadores de serviço
locais: encontrar, nas conversas que eles já mantêm no WhatsApp, clientes que
ainda precisam de uma ação para o serviço não ficar pelo caminho.

> Continue usando seu WhatsApp normalmente. O Radar mostra quais clientes
> precisam de uma ação sua para o serviço não ficar pelo caminho.

## Para quem

O primeiro público é o prestador ou a microempresa de serviços que:

- vende principalmente pelo WhatsApp Business;
- passa boa parte do dia executando serviços em campo;
- trabalha em equipe de uma a cinco pessoas, sem vendedor dedicado;
- não usa CRM ou não consegue manter um funil atualizado;
- precisa resolver as pendências em poucos minutos pelo celular.

Os cinco participantes iniciais pertencerão à mesma vertical. A vertical
concreta ainda não foi escolhida: `VERTICAL_SELECTION=PENDING_OWNER_SELECTION`.
Exemplos como eletricistas, encanadores, ar-condicionado, assistência técnica e
manutenção residencial não são decisões. A escolha cabe ao proprietário e deve
priorizar onde seja possível recrutar cinco prestadores reais rapidamente.

## Aquisição inicial

O recrutamento começa por amigos e conhecidos compatíveis com o ICP,
indicações, prestadores do bairro e prestadores da cidade. A abordagem é direta
e relacional, sem mídia paga nesta fase.

Essa é uma decisão deliberada de atuar de forma pequena, próxima e simples. Não
é evidência de que “há clientes para todo mundo”, nem estratégia de competir em
funcionalidades, substituir CRMs ou buscar paridade com plataformas maiores.

A reavaliação de mercado registrou o wedge
`MOBILE_FIELD_PROVIDER_NO_CRM`: prestador em campo, mobile-first, que vende pelo
WhatsApp e não quer manter CRM, funil ou cadastro duplicado. A existência de
CRMs e ferramentas para WhatsApp comprova apenas uma categoria concorrida; não
valida demanda pelo Radar. Evidências, inferências e riscos estão separados em
[`docs/MARKET-REASSESSMENT-2026-08-11.md`](docs/MARKET-REASSESSMENT-2026-08-11.md).

## Hipótese atual

O trabalho a validar é: **“me diga quais clientes ainda podem virar serviço e
qual é a próxima coisa que preciso fazer.”**

O primeiro discovery observará quatro situações:

| Situação apresentada ao prestador | Código interno | Exemplo de próxima ação |
|---|---|---|
| Precisa responder | `NEEDS_RESPONSE` | Responder o pedido |
| Precisa orçar | `NEEDS_QUOTE` | Enviar o orçamento prometido |
| Follow-up pendente | `FOLLOWUP_DUE` | Retomar a proposta |
| Retorno prometido | `PROMISED_RETURN_DUE` | Cumprir o retorno combinado |

Padrões diferentes podem ser anotados como `OUT_OF_SCOPE_CANDIDATE`. Isso gera
aprendizado, não uma nova feature ou ampliação automática do produto.

## Próximo experimento: R1A

O `R1A` é um Discovery Concierge gratuito com cinco prestadores da mesma
vertical. `R1A_READY=COMPLETE` permanece como prontidão documental, mas
`FIRST_R1A_SESSION=BLOCKED` até que a vertical esteja `COMPLETE` e o checklist
da sessão concreta esteja `READY`. Em cada sessão:

1. o prestador mantém o próprio aparelho sob controle;
2. a revisão presencial dura de 20 a 30 minutos;
3. não há fotografia, gravação, cópia ou exportação de conversas;
4. o prestador confirma se a oportunidade importa, se a havia esquecido, por
   que ficou parada e qual ação faz sentido;
5. contatos curtos nos dias 4 e 7 registram ações e desfechos, sem nova revisão
   completa do WhatsApp.

O discovery também investiga como o prestador evita esquecimentos hoje, o que
falha em etiquetas, estrela, agenda, caderno, memória, CRM ou outros métodos e
se essas alternativas já resolvem suficientemente o problema. Também registra,
em categorias, o dispositivo principal de vendas, uso regular de WhatsApp Web,
aceitação de outra ferramenta diária e origem do recrutamento. Faixas de volume
semanal e ticket típico só são registradas quando legitimamente conhecidas, sem
identificar clientes ou alegar receita perdida. Esses dados são diagnósticos e
não criam gates isolados.

O procedimento completo está em [`docs/R1A-DISCOVERY.md`](docs/R1A-DISCOVERY.md)
e o checklist de início em
[`docs/DISCOVERY-SESSION-READY.md`](docs/DISCOVERY-SESSION-READY.md).

O R1B só poderá ser preparado se todos os critérios por prestador forem
atingidos: problema em pelo menos 4 de 5; oportunidade relevante esquecida,
ação executada e interesse recorrente em pelo menos 3 de 5. Se pelo menos três
participantes considerarem os substitutos atuais suficientes, ou se o problema
for excessivamente episódico, o R1B permanece bloqueado.

## O que não está sendo construído

Não há produto, integração com WhatsApp, parser, IA, frontend, backend, banco,
notificação, automação, cobrança, arquitetura definitiva ou infraestrutura
produtiva em desenvolvimento. A hipótese vigente para um experimento posterior
é um `PAID_ASSISTED_PILOT` de 30 dias, pago antecipadamente por
`PAID_PILOT_PRICE=R$99.00`, com estado `HYPOTHESIS_ONLY`, sem período gratuito
depois do R1A e sem renovação automática.

O protocolo está pré-registrado em
[`docs/R1B-COMMERCIAL-EXPERIMENT.md`](docs/R1B-COMMERCIAL-EXPERIMENT.md), mas
permanece `BLOCKED_UNTIL_R1A_PASS`, depende de nova autorização explícita e não
é uma oferta vigente. A hipótese anterior de R$ 149 por sete dias está
`SUPERSEDED`. `MONTHLY_PRICE=R$49.90` também está `SUPERSEDED` e permanece
somente como histórico da decisão anterior.

A antiga auditoria de `LP-001`/`LP-002`, seu relatório longo e sua oferta de
R$ 500 foram substituídos como direção de produto. Os materiais continuam no
repositório como histórico e os detectores podem servir como evidência auxiliar.

## Representação sintética mínima

A [`lista sintética`](docs/R1A-SYNTHETIC-LIST.md) ilustra somente o formato que
será mostrado no discovery: no máximo cinco clientes, cada um com prioridade,
motivo e próxima ação. Ela não é produto, demo comercial refinada ou evidência
de mercado.

## Validação documental

```powershell
python -m unittest discover -s tests -v
python scripts/validate_repository.py --report artifacts/quality/report.json
```

Essas verificações cobrem fixtures sintéticas, contabilidade de linhas, CSVs,
links locais, privacidade, segredos e integridade do diff. Testes verdes não
validam o problema nem substituem as cinco conversas com prestadores.

## Dados e privacidade

Dados reais nunca entram neste Git. No `R1A`, a sessão é sem custódia, sem
cópia e sem retenção das conversas, mas isso não deve ser descrito como ausência
de tratamento de dados. Nomes, telefones, mensagens, mídias e informações
sensíveis não são registrados. A revisão jurídica externa não foi obtida.

Consulte [`docs/GATE-STATUS.md`](docs/GATE-STATUS.md) para os bloqueios vigentes
e [`docs/R0-DECISION-LOG.md`](docs/R0-DECISION-LOG.md) para o histórico.
