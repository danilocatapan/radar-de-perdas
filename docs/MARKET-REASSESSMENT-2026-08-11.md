# Reavaliação de mercado — 2026-08-11

| Campo | Valor |
|---|---|
| Status | Decisão estratégica interna; validação externa pendente |
| Wedge em investigação | `MOBILE_FIELD_PROVIDER_NO_CRM` |
| Vertical | `VERTICAL_SELECTION=PENDING_OWNER_SELECTION` |
| Evidência externa do Radar | `PENDING_R1A` |

Este registro separa fatos observáveis, hipóteses, inferências, riscos e
decisões. Ele não constitui pesquisa exaustiva, recomendação de preço ou
evidência de demanda pelo Radar.

## Evidências consultadas

Páginas oficiais consultadas em 2026-08-11 mostram que já existem categorias
maduras com gestão de contatos, negócios, tarefas, funil, atendimento por
WhatsApp e automação:

- [HubSpot CRM](https://www.hubspot.com/products/crm?software=crm);
- [RD Station CRM para WhatsApp](https://materiales.rdstation.com/crm-de-vendas-para-whatsapp-extension);
- [RD Station Conversas](https://www.rdstation.com/produtos/conversas/atendimento-whatsapp/).

Essas páginas são evidência apenas da existência e amplitude das categorias.
Afirmações promocionais, estatísticas e preços publicados pelos fornecedores
não foram adotados como fatos sobre o mercado nem como evidência de demanda,
adequação ou disposição a pagar pelo Radar.

## Hipótese

O wedge `MOBILE_FIELD_PROVIDER_NO_CRM` descreve um prestador local que:

- passa a maior parte da operação em campo e usa primeiro o celular;
- vende pelo WhatsApp;
- não quer manter CRM, funil ou cadastro duplicado no dia a dia;
- pode valorizar uma lista assistida de no máximo cinco oportunidades, com
  prioridade, motivo e próxima ação.

A hipótese não afirma que todos os prestadores possuem esse comportamento nem
que a fricção é suficiente para gerar demanda.

## Inferência a investigar

Como CRMs e ferramentas ligadas ao WhatsApp cobrem conjuntos amplos de
funcionalidades, uma direção plausível para o Radar é diferenciar-se por baixo atrito
operacional em um nicho local e mobile-first, e não por paridade de features.
Essa é uma inferência estratégica a testar no `R1A`, não uma conclusão de
mercado.

## Riscos

- etiquetas, estrela, agenda, caderno, memória ou CRM podem resolver o problema
  suficientemente para a maioria;
- o wedge mobile/no-CRM pode não ser relevante na vertical selecionada;
- oportunidades paradas podem ocorrer de modo episódico demais;
- o serviço assistido pode exigir operação incompatível com o preço testado;
- `PAID_PILOT_PRICE=R$99.00` pode não produzir pagamentos reais.

## Decisões

- não posicionar o Radar como CRM horizontal, substituto de CRM ou concorrente
  por quantidade de funcionalidades;
- manter aquisição direta e relacional por amigos, conhecidos, indicações,
  bairro e cidade, sem mídia paga nesta fase;
- investigar explicitamente dispositivo principal, uso de WhatsApp Web,
  aceitação de ferramenta externa diária e experiência anterior com CRM;
- substituir a hipótese comercial vigente de R$ 49,90/mês por um piloto
  assistido pago, por 30 dias, com R$ 99 antecipados;
- manter o R1B `BLOCKED_UNTIL_R1A_PASS`, sujeito a nova autorização explícita e
  `OPERATIONAL_LIMIT=PENDING_OWNER_DECISION`;
- manter bloqueados produto, parser, frontend, backend, banco, IA/LLM,
  integração WhatsApp, notificações, automação, cobrança, infraestrutura e
  arquitetura produtiva.

A existência de concorrentes ou de uma categoria não valida o problema do
Radar. Somente as evidências pré-registradas do R1A e, depois, pagamentos reais
em R1B autorizado podem alterar os gates correspondentes.

Para evitar ambiguidade: `MONTHLY_PRICE=R$49.90` está `SUPERSEDED`;
`PAID_PILOT_PRICE=R$99.00` é a hipótese vigente, ainda `HYPOTHESIS_ONLY`.
