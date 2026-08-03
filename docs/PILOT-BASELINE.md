# Protocolo de baseline e produtividade

| Campo | Valor |
|---|---|
| Versão | 1.0 |
| Responsável por aprovação | Consultor do Radar de Perdas |
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
| `CLIENT_CLARIFICATION` | Início de contato necessário para esclarecer contexto | Encerramento do esclarecimento |
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

## 5. Fórmulas

```text
active_seconds = elapsed_seconds - excluded_pause_seconds

production_active_minutes =
  PREPARATION +
  CONFIGURATION +
  READING +
  CLASSIFICATION +
  REPORT_WRITING +
  REVIEW_REWORK

client_interaction_minutes =
  CLIENT_CLARIFICATION +
  PRESENTATION

total_service_minutes =
  production_active_minutes +
  client_interaction_minutes

productivity_reduction =
  (manual_production_active - assisted_production_active)
  / manual_production_active
```

## 6. Procedimento comparativo

Preferência:

1. Usar amostra independente do mesmo segmento e perfil.
2. Estratificar por quantidade de chats, mensagens e período.

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
- Menos de dez sugestões automáticas torna descarte inconclusivo.
- Menos de dez achados confirmados torna omissão inconclusiva.

## 9. Gate

- Redução produtiva ≥ 30%.
- Tempo total do serviço não aumenta.
- Descarte < 20%.
- Achados manuais adicionais < 20%.

Todos os resultados inconclusivos exigem nova amostra.

## 10. Avaliação do comprador

Após ler o relatório, o comprador responde sem orientação prévia:

1. Qual foi o objetivo da auditoria?
2. Quais foram os principais achados?
3. Qual ação possui maior prioridade?
4. Qual limitação impede interpretar os achados como vendas perdidas?
5. Qual é o próximo passo recomendado?

Registrar:

```text
Nota de utilidade (1–5):
Respostas corretas (0–5):
Minutos de esclarecimento:
Intenção de contratar novamente:
Faixa de preço aceitável:
Comentários:
```
