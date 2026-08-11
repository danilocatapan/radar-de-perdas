# R1A — Discovery Concierge

| Campo | Valor |
|---|---|
| Versão | 1.2 |
| Participantes planejados | 5 prestadores |
| Prontidão documental | `R1A_READY=COMPLETE` |
| Seleção de vertical | `VERTICAL_SELECTION=PENDING_OWNER_SELECTION` |
| Primeira sessão | `FIRST_R1A_SESSION=BLOCKED` |
| Revisão jurídica externa | `EXTERNAL_LEGAL_REVIEW_NOT_OBTAINED` |

## Objetivo

Descobrir se prestadores compatíveis com o ICP possuem oportunidades comerciais
que consideram relevantes, poderiam ter esquecido e transformam em ação quando
recebem uma revisão curta e proativa.

O `R1A` é gratuito e não valida software, integração, automação, IA, preço,
disposição a pagar ou causalidade financeira.

O wedge estratégico em investigação é `MOBILE_FIELD_PROVIDER_NO_CRM`: um
prestador em campo, mobile-first, que vende pelo WhatsApp e não aceita manter
CRM, funil ou cadastro duplicado no cotidiano. Ele é hipótese diagnóstica, não
critério isolado de aprovação do R1A.

## Aquisição e seleção da vertical

Os cinco participantes devem pertencer à mesma vertical. O proprietário escolhe
a vertical; o Codex não a define. A decisão deve priorizar onde seja possível
recrutar rapidamente cinco prestadores reais por:

- amigos e conhecidos compatíveis com o ICP;
- indicações da rede pessoal;
- prestadores do bairro;
- prestadores da cidade.

A abordagem é direta e relacional, sem mídia paga nesta fase. Exemplos de
verticais servem somente para orientar a decisão e não constituem escolha.

`R1A_READY=COMPLETE` permanece inalterado. A primeira sessão só pode ocorrer
quando `VERTICAL_SELECTION=COMPLETE` e o `DISCOVERY_SESSION_READY` da sessão
concreta estiver `READY`.

## Qualificação do prestador

O prestador deve:

- pertencer à vertical selecionada;
- vender serviços locais principalmente pelo WhatsApp Business;
- trabalhar sozinho ou em equipe de até cinco pessoas;
- não contar com vendedor ou recepcionista dedicado;
- passar parte relevante do dia executando serviços;
- possuir conversas comerciais recentes que possa revisar legitimamente;
- aceitar manter o aparelho sob seu controle durante toda a sessão;
- aceitar os limites do [`DISCOVERY_SESSION_READY`](DISCOVERY-SESSION-READY.md).

Não revisar saúde, menores, grupos, informações sensíveis, suporte sem finalidade
comercial ou qualquer conversa cuja visualização gere dúvida. Pular o caso é a
decisão padrão.

## Antes da sessão

1. Confirmar `VERTICAL_SELECTION=COMPLETE` e que o prestador pertence à vertical
   selecionada.
2. Reservar um código como `R1A-2026-P01`, sem associá-lo publicamente ao nome.
3. Explicar o objetivo e enviar o
   [`convite de discovery`](R1A-DISCOVERY-INVITATION.md).
4. Conferir o checklist de uma página e obter `DISCOVERY_SESSION_READY=READY`.
5. Abrir localmente uma cópia vazia de `R1A-DISCOVERY-LOG.csv` fora do Git.
6. Criar uma linha `SESSION` mesmo que nenhuma oportunidade seja encontrada.
7. Não solicitar exportação, screenshot, mensagem encaminhada ou lista de
   clientes.

## Dia 1 — sessão presencial de 20–30 minutos

O prestador mantém o aparelho nas mãos e navega nas próprias conversas.

1. Antes de revisar oportunidades, perguntar:
   - Qual é o dispositivo principal que você usa para vender: celular,
     computador ou ambos?
   - Você usa WhatsApp Web com regularidade?
   - Você aceitaria manter diariamente outro aplicativo, CRM ou funil além do
     WhatsApp?
   - Como você evita esquecer clientes hoje?
   - Quando foi a última vez que uma oportunidade ficou parada por falta de
     acompanhamento?
   - Você usa etiqueta, estrela, agenda, caderno, CRM ou outro método?
   - O que falha no método atual?
   - Já tentou algum CRM, extensão ou ferramenta semelhante? Se abandonou, por
     quê?
2. Registrar a origem do recrutamento como categoria genérica, sem nome de quem
   indicou ou qualquer contato identificável.
3. Quando o prestador souber responder legitimamente, registrar somente a faixa
   aproximada de contatos ou orçamentos comerciais por semana e a faixa de
   ticket típico. Não registrar faturamento, valor exato identificável ou dados
   de clientes.
4. Pedir que ele procure conversas comerciais recentes que possam ainda exigir
   alguma providência.
5. Ignorar imediatamente qualquer conversa incompatível.
6. Para cada possível oportunidade, criar apenas um código sequencial, como
   `R1A-2026-P01-O01`.
7. Classificar uma das quatro situações permitidas ou
   `OUT_OF_SCOPE_CANDIDATE`.
8. Perguntar:
   - Essa conversa ainda poderia virar serviço?
   - Você teria lembrado de procurar esse cliente sem esta revisão?
   - Qual é a próxima ação correta?
   - Por que esta oportunidade específica ficou parada?
9. Registrar a prioridade acordada com o prestador e a ação em termos genéricos,
   sem copiar texto da conversa.
10. Pedir que ele execute somente as ações que considerar relevantes, no momento
   que julgar apropriado.
11. Perguntar se o método atual resolve suficientemente o problema e registrar
    `YES`, `NO` ou `UNKNOWN` como diagnóstico, nunca como resposta presumida.
12. Encerrar o registro de tempo quando a participação ativa terminar.

Prioridade é julgamento manual e contextual. Não existe mapeamento automático
entre estado e prioridade.

## Estados permitidos

| Código interno | Uso no discovery |
|---|---|
| `NEEDS_RESPONSE` | Solicitação comercial relevante sem resposta útil do prestador |
| `NEEDS_QUOTE` | Prestador indicou que enviaria preço ou orçamento, mas ainda não enviou |
| `FOLLOWUP_DUE` | Orçamento ou proposta enviada com oportunidade razoável de retomada |
| `PROMISED_RETURN_DUE` | Retorno, confirmação ou verificação prometida e ainda não cumprida |
| `OUT_OF_SCOPE_CANDIDATE` | Padrão possivelmente relevante que não cabe nos quatro estados |

Para `OUT_OF_SCOPE_CANDIDATE`, registrar somente:

- `candidate_type`: rótulo genérico, como `NEEDS_SCHEDULING`;
- `provider_confirmed_relevant`: `YES`, `NO` ou `UNKNOWN`;
- `frequency`: contagem observada na sessão;
- `notes`: aprendizado categórico, sem nome, mensagem ou detalhe identificável.

O registro não cria feature, estado oficial ou gate. Padrões recorrentes serão
avaliados somente depois das cinco sessões.

## Contrato do registro pseudônimo

Cada cópia externa de `R1A-DISCOVERY-LOG.csv` usa dois tipos de linha:

- `SESSION`: uma linha obrigatória por prestador, com `session_code`, método
  atual, falha do método, experiência e eventual abandono de CRM, suficiência
  do substituto, frequência do problema, faixa da última oportunidade parada,
  faixas econômicas, dispositivo principal de vendas, uso de WhatsApp Web,
  aceitação de ferramenta externa diária, origem da aquisição, interesse
  recorrente e tempos; campos de oportunidade ficam vazios;
- `OPPORTUNITY`: uma linha por oportunidade codificada, com `session_code`,
  `opportunity_code`, estado, prioridade, confirmações, próxima ação, desfechos,
  causa genérica da paralisação e eventual candidato fora do escopo; campos de
  contexto da sessão ficam vazios.

Campos `YES | NO | UNKNOWN` nunca recebem resposta presumida. Métodos, falhas,
motivos e causas usam rótulos genéricos; `notes` não recebe nomes, mensagens,
datas exatas ou detalhes que permitam reidentificação. As faixas econômicas são
aproximadas, opcionais e permanecem somente na cópia confidencial fora do Git.

Os campos diagnósticos usam somente estes valores:

| Campo | Valores permitidos |
|---|---|
| `primary_sales_device` | `MOBILE_ONLY \| MOBILE_MOSTLY \| BALANCED \| DESKTOP_MOSTLY \| UNKNOWN` |
| `whatsapp_web_usage` | `YES \| NO \| UNKNOWN` |
| `daily_external_tool_acceptance` | `YES \| NO \| UNKNOWN` |
| `acquisition_source` | `FRIEND \| REFERRAL \| NEIGHBORHOOD \| CITY_OTHER \| UNKNOWN` |

Esses campos ajudam a avaliar o wedge `MOBILE_FIELD_PROVIDER_NO_CRM`, mas não
substituem nenhum dos quatro gates centrais, não criam um gate autônomo e não
validam demanda ou disposição a pagar.

## Dias 4 e 7 — follow-ups curtos

Não repetir a revisão do WhatsApp. Perguntar somente, para as oportunidades já
codificadas:

- A ação foi executada?
- A conversa foi reativada?
- Algum serviço foi confirmado?

No dia 7, perguntar também se o prestador gostaria de receber novamente uma
lista ou revisão desse tipo. Registrar `YES`, `NO` ou `UNKNOWN`.

Ausência de confirmação não vira resultado positivo. Valor de serviço pode ser
registrado em controle confidencial somente se confirmado espontaneamente pelo
prestador, sempre separado de qualquer alegação causal e fora do Git.

## Tempos

Registrar em segundos:

- `provider_active_seconds`: tempo de participação ativa do prestador;
- `operator_active_seconds`: preparação, sessão, registro e follow-up ativos;
- `operator_travel_seconds`: deslocamento dedicado à sessão.

Espera passiva não entra em tempo ativo. Esses dados diagnosticam o custo do
concierge e não são gate estatístico.

## Gate por prestador

Após cinco sessões, contar cada prestador no máximo uma vez por critério:

| Critério | Aprovação |
|---|---|
| Problema existe | Pelo menos 4 de 5 têm uma oportunidade candidata |
| Oportunidade relevante esquecida | Pelo menos 3 de 5 confirmam pelo menos uma |
| Ação executada | Pelo menos 3 de 5 executam pelo menos uma ação relevante |
| Interesse recorrente | Pelo menos 3 de 5 querem receber novamente o acompanhamento |

Todos os quatro critérios devem ser atendidos para preparar o teste pago.

## Análise de substitutos e regras de parada

Depois das cinco sessões, contar cada prestador no máximo uma vez:

- se pelo menos três de cinco considerarem que etiquetas, estrela, agenda,
  caderno, memória, CRM ou outra rotina já resolvem suficientemente o problema,
  registrar `STOP` para a hipótese atual e manter o R1B bloqueado;
- se a evidência mostrar que o problema é excessivamente episódico para um
  acompanhamento recorrente, o proprietário registra `STOP` ou outra decisão
  explícita e o R1B permanece bloqueado;
- se qualquer um dos quatro gates centrais falhar, o R1B permanece bloqueado.

`STOP` encerra somente a hipótese ou etapa atual. Repetir o R1A, reformular a
hipótese ou pivotar exige nova decisão explícita do proprietário. A falha não
cria feature, não inicia uma sequência automática de pivots e não arquiva o
repositório.

## Métricas diagnósticas

Registrar numerador e denominador, sem tratar `n=5` como evidência estatística:

- `candidate_relevance_rate`;
- `false_positive_rate`;
- `actions_executed_rate`;
- `conversations_reactivated`;
- `services_confirmed`;
- `providers_with_sufficient_substitute`;
- `reported_problem_frequency`;
- `provider_active_time`;
- `operator_active_time`, incluindo deslocamento separado.

Essas taxas descrevem a amostra observada e não representam evidência
estatística.

Manifestação espontânea de disposição a pagar é sinal qualitativo. Somente
pagamento real em experimento posterior é evidência comercial.

## Registro agregado permitido no Git

Depois das cinco sessões, o repositório pode receber somente:

```text
sessions_completed=<0-5>
providers_with_candidate=<0-5>
providers_with_forgotten_relevant_opportunity=<0-5>
providers_who_executed_action=<0-5>
providers_with_recurring_interest=<0-5>
providers_with_sufficient_substitute=<0-5>
problem_frequency_summary=<agregado não identificável>
r1a_gate=PASS | FAIL | INCONCLUSIVE
stage_decision=CONTINUE_TO_R1B_PREPARATION | STOP | OWNER_DECISION_REQUIRED
external_evidence_reference=registro confidencial fora do Git
```

Não publicar linhas individuais, segmentos combinados com datas, conteúdo de
conversa ou qualquer informação que permita reidentificação.
