# Protocolo de baseline e produtividade

> **Status: `SUPERSEDED_FOR_CURRENT_R1A`.** Este baseline mede a produção de
> relatórios da auditoria anterior. O Discovery Concierge usa os critérios por
> prestador e os tempos definidos em [`R1A-DISCOVERY.md`](R1A-DISCOVERY.md).
> O conteúdo abaixo permanece como histórico e não bloqueia o `R1A` atual.

| Campo | Valor |
|---|---|
| Versão | 1.1 |
| Responsável pela decisão | Proprietário do Radar de Perdas |
| Status | `SUPERSEDED_FOR_CURRENT_R1A` |
| Registro primário | `PILOT-TIME-LOG.csv` |

## 1. Objetivo

Comparar a produção manual e assistida sem remover do cálculo configuração,
revisão ou retrabalho.

## 2. Modos

- `MANUAL`: nenhuma sugestão automática está disponível ao auditor.
- `ASSISTED`: parser e regras podem sugerir itens, mas a revisão integral
  continua obrigatória.

## 3. Categorias

| Categoria | Início | Fim |
|---|---|---|
| `PREPARATION` | Início da organização e conferência dos arquivos | Arquivos aptos para configurar |
| `CONFIGURATION` | Início do cadastro de período, horário, SLA e participantes | Critérios prontos para analisar |
| `READING` | Abertura do primeiro chat para compreensão | Fim da leitura prevista |
| `CLASSIFICATION` | Primeira marcação de solicitação, resultado ou achado | Fim das classificações |
| `REPORT_WRITING` | Início da redação/compilação do relatório | Relatório inicial completo |
| `REVIEW_REWORK` | Início da conferência ou correção | Versão pronta para entrega |
| `CLIENT_CLARIFICATION` | Início de atuação ativa para esclarecer contexto | Fim da atuação ativa; espera pela resposta não é registrada |
| `PRESENTATION` | Início da reunião de apresentação | Fim da reunião |

Uma atividade não pode sobrepor outra.

## 4. Pausas e arredondamento

- Interrupção superior a 60 segundos é registrada em
  `excluded_pause_seconds`.
- Interrupções de até 60 segundos permanecem no tempo ativo.
- Retrabalho e correções permanecem incluídos.
- Os segundos são somados antes do arredondamento.
- O arredondamento ocorre uma vez por categoria, para o minuto inteiro mais
  próximo.
- Linhas sem `started_at` e `ended_at` válidos invalidam a medição.
- Espera por resposta, agenda ou disponibilidade do cliente não é esforço
  ativo: encerrar a linha e abrir outra quando a atividade recomeçar.
- O esforço de esclarecimento inclui leitura da dúvida, formulação e envio da
  resposta e conversa síncrona; não inclui tempo corrido passivo.

## 5. Fórmulas

```text
active_seconds = elapsed_seconds - excluded_pause_seconds

production_active_seconds =
  PREPARATION +
  CONFIGURATION +
  READING +
  CLASSIFICATION +
  REPORT_WRITING +
  REVIEW_REWORK

client_interaction_active_seconds =
  CLIENT_CLARIFICATION +
  PRESENTATION

total_service_active_seconds =
  production_active_seconds +
  client_interaction_active_seconds

productivity_reduction =
  (manual_production_active_seconds - assisted_production_active_seconds)
  / manual_production_active_seconds
```

Todas as comparações usam segundos. Converter e arredondar somente os valores
apresentados no relatório, uma vez por categoria, sem reutilizar o valor
arredondado em fórmulas.

## 6. Procedimento comparativo

Preferência:

1. Usar amostra independente do mesmo segmento e perfil.
2. Estratificar por quantidade de chats, mensagens e período.

Para declarar as amostras comparáveis, elas devem usar o mesmo segmento, canal,
duração do período e regras de elegibilidade. A diferença absoluta entre os
modos deve ser de no máximo 20% para cada volume: chats analisados, mensagens e
solicitações elegíveis. Se qualquer condição falhar, registrar
`SAMPLES_INCOMPARABLE` e não calcular redução de produtividade conclusiva.

Fallback:

1. Repetir a mesma amostra após no mínimo 14 dias.
2. Ocultar relatório, classificações e expected outputs anteriores.
3. Registrar `LEARNING_EFFECT_RISK=true`.
4. Tratar o resultado como preliminar.
5. Exigir confirmação em segundo piloto antes de escalar.

## 7. Volumes obrigatórios

```text
Chats recebidos:
Chats analisados:
Chats excluídos:
Mensagens:
Solicitações elegíveis:
Achados LP-001:
Achados LP-002:
Sugestões automáticas:
Sugestões rejeitadas:
Achados manuais adicionais:
Achados confirmados:
```

## 8. Métricas dos achados

```text
auto_discard_rate =
  automatic_suggestions_rejected /
  total_automatic_suggestions_reviewed

manual_addition_rate =
  additional_manual_findings_confirmed /
  total_confirmed_findings
```

- Cálculos limitados a LP-001 e LP-002.
- Revisar todas as solicitações elegíveis, não apenas as sugeridas.
- `OUT_OF_SCOPE` não entra nos denominadores.
- Duplicatas confirmadas contam uma vez.
- Denominador zero torna a métrica correspondente inconclusiva.
- Menos de dez sugestões automáticas torna descarte inconclusivo.
- Menos de dez achados confirmados torna `manual_addition_rate` inconclusiva.
- `manual_addition_rate` é uma proxy de achados confirmados que não foram
  sugeridos automaticamente. Ela não mede omissão absoluta e não demonstra que
  todos os achados possíveis foram encontrados.

## 9. Gate

- Redução produtiva ≥ 30%.
- Tempo total do serviço não aumenta.
- Descarte < 20%.
- `manual_addition_rate` < 20%, apresentado como proxy de achados não sugeridos.

Todos os resultados inconclusivos exigem nova amostra.

## 10. Avaliação do decisor

Após ler o relatório, o decisor responde sem orientação prévia:

1. Qual foi o objetivo da auditoria?
2. Quais foram os principais achados?
3. Qual ação possui maior prioridade?
4. Qual limitação impede interpretar os achados como vendas perdidas?
5. Qual é o próximo passo recomendado?

Registrar:

```text
Nota de utilidade (1–5):
Respostas corretas (0–5):
Esforço ativo de esclarecimento em segundos:
Minutos apresentados após arredondamento:
Intenção de contratar novamente:
Faixa de preço aceitável:
Comentários:
```

### 10.1 Rubrica de utilidade

O decisor escolhe uma afirmação antes da apresentação:

| Nota | Âncora |
|---:|---|
| 1 | Não identifica uso prático para o relatório. |
| 2 | Percebe informação interessante, mas sem ação clara. |
| 3 | Identifica ao menos uma ação possível, ainda com dúvidas relevantes. |
| 4 | Considera o relatório útil e identifica uma ação prioritária aplicável. |
| 5 | Considera o relatório muito útil, claro e suficiente para orientar próximos passos. |

O critério de utilidade é atingido com nota maior ou igual a 4/5.

### 10.2 Rubrica de compreensão

Cada uma das cinco perguntas vale um ponto. A resposta é correta quando contém
o elemento mínimo abaixo, sem exigir reprodução literal:

| Pergunta | Elemento mínimo para um ponto |
|---|---|
| Objetivo | Identificar demora e ausência de resposta na amostra, sem afirmar venda perdida. |
| Principais achados | Relatar corretamente os achados prioritários apresentados. |
| Prioridade | Identificar a ação classificada como prioridade mais alta. |
| Limitação | Reconhecer que a amostra e os indicadores não provam perda de venda ou receita. |
| Próximo passo | Identificar o próximo passo recomendado no relatório. |

O critério de compreensão é atingido com pelo menos quatro respostas corretas
em cinco. Pergunta não respondida ou resposta ambígua vale zero; registrar a
justificativa da correção.

### 10.3 Esclarecimento e modalidade

- Somar os `active_seconds` de `CLIENT_CLARIFICATION` ocorridos após a leitura e
  antes do encerramento da avaliação.
- O critério é atingido com no máximo 900 segundos ativos, apresentados como até
  15 minutos.
- Denominador ausente, avaliação não respondida ou medição inválida produz
  `INCONCLUSIVE`, nunca aprovação presumida.
- No `R1A` gratuito, registrar feedback de utilidade e compreensão, mas não
  solicitar nem inferir intenção de recompra ou faixa de preço.
- A disposição a pagar só pode ser validada no `R1B` mediante pagamento total
  de pelo menos R$ 500; feedback do `R1A` não completa esse gate.

## 11. Aprovação interna

```text
Responsável: Proprietário do Radar de Perdas
Decisão: INTERNAL_APPROVED
Escopo da decisão: protocolo de baseline e avaliação dos pilotos R1A e R1B
Revisão jurídica externa: não aplicável a esta aprovação metodológica interna
```
