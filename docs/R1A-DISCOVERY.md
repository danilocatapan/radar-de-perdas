# R1A — Discovery Concierge

| Campo | Valor |
|---|---|
| Versão | 1.0 |
| Participantes planejados | 5 prestadores |
| Estado | Preparação documental; nenhuma sessão concluída |
| Revisão jurídica externa | `EXTERNAL_LEGAL_REVIEW_NOT_OBTAINED` |

## Objetivo

Descobrir se prestadores compatíveis com o ICP possuem oportunidades comerciais
que consideram relevantes, poderiam ter esquecido e transformam em ação quando
recebem uma revisão curta e proativa.

O `R1A` não valida software, integração, automação, preço ou causalidade
financeira.

## Qualificação do prestador

O prestador deve:

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

1. Reservar um código como `R1A-2026-P01`, sem associá-lo publicamente ao nome.
2. Explicar o objetivo e enviar o
   [`convite de discovery`](R1A-DISCOVERY-INVITATION.md).
3. Conferir o checklist de uma página.
4. Abrir localmente uma cópia vazia de `R1A-DISCOVERY-LOG.csv` fora do Git.
5. Não solicitar exportação, screenshot, mensagem encaminhada ou lista de
   clientes.

## Dia 1 — sessão presencial de 20–30 minutos

O prestador mantém o aparelho nas mãos e navega nas próprias conversas.

1. Pedir que ele procure conversas comerciais recentes que possam ainda exigir
   alguma providência.
2. Ignorar imediatamente qualquer conversa incompatível.
3. Para cada possível oportunidade, criar apenas um código sequencial, como
   `R1A-2026-P01-O01`.
4. Classificar uma das quatro situações permitidas ou
   `OUT_OF_SCOPE_CANDIDATE`.
5. Perguntar:
   - Essa conversa ainda poderia virar serviço?
   - Você teria lembrado de procurar esse cliente sem esta revisão?
   - Qual é a próxima ação correta?
6. Registrar a prioridade acordada com o prestador e a ação em termos genéricos,
   sem copiar texto da conversa.
7. Pedir que ele execute somente as ações que considerar relevantes, no momento
   que julgar apropriado.
8. Encerrar o registro de tempo quando a participação ativa terminar.

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

## Métricas diagnósticas

Registrar numerador e denominador, sem tratar `n=5` como evidência estatística:

- `candidate_relevance_rate`;
- `false_positive_rate`;
- `actions_executed_rate`;
- `conversations_reactivated`;
- `services_confirmed`;
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
r1a_gate=PASS | FAIL | INCONCLUSIVE
external_evidence_reference=registro confidencial fora do Git
```

Não publicar linhas individuais, segmentos combinados com datas, conteúdo de
conversa ou qualquer informação que permita reidentificação.
