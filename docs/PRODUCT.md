# Produto — Radar de Perdas

| Campo | Valor |
|---|---|
| Versão | 0.1 |
| Status | Validação do serviço |
| Responsável por aprovação | Consultor do Radar de Perdas |

## Visão

Ajudar pequenos negócios a identificar falhas verificáveis no atendimento
comercial por WhatsApp e priorizar melhorias, sem equiparar automaticamente uma
falha a uma venda perdida.

## Hipótese principal

Uma auditoria padronizada de LP-001 e LP-002:

- é comprável por pelo menos R$ 500;
- pode ser produzida com dados legitimamente fornecidos;
- gera recomendações compreensíveis;
- pode ter pelo menos 30% do tempo produtivo reduzido por ferramenta local;
- pode operar com taxas de descarte e omissão inferiores a 20%.

## Usuário inicial

Consultor que vende, executa e apresenta auditorias. Clientes não acessam
software no primeiro estágio.

## Unidade de análise

- Empresa: uma por piloto.
- Unidade: uma por piloto.
- Canal: um WhatsApp.
- Amostra: até 50 chats individuais.
- Período: até 30 dias.
- Solicitação: bloco consecutivo de mensagens do prospect até uma resposta
  humana útil.

## Resultado entregue

Relatório manual redigido ou pseudonimizado com:

- escopo e limitações;
- indicadores LP-001/LP-002;
- evidências mínimas;
- hipóteses de causa;
- recomendações e prioridades.

## Não objetivos

- Estimar receita perdida.
- Provar causalidade entre atendimento e venda.
- Substituir revisão humana.
- Criar software personalizado por cliente.
- Analisar grupos, anexos ou áudios.
- Construir SaaS antes dos gates.

## Gates do produto

A aplicação produtiva só pode ser iniciada quando todos os critérios de
`GATE-STATUS.md` estiverem atendidos e documentados.

## Métricas de sucesso

- Pagamento total ≥ R$ 500.
- Utilidade percebida ≥ 4/5.
- Compreensão ≥ 4/5 respostas.
- Esclarecimento pós-leitura ≤ 15 minutos.
- Redução de `production_active_minutes` ≥ 30%.
- `total_service_minutes` não aumenta.
- Descarte automático < 20%.
- Achados manuais adicionais < 20%.
