# Produto — Radar de Perdas

| Campo | Valor |
|---|---|
| Versão | 0.3 |
| Status | `INTERNAL_APPROVED` para `R1A` |
| Responsável pela decisão | Proprietário do Radar de Perdas |
| Revisão externa | `EXTERNAL_LEGAL_REVIEW_NOT_OBTAINED` |

## Visão

Ajudar pequenos negócios a identificar falhas verificáveis no atendimento
comercial por WhatsApp e priorizar melhorias, sem equiparar automaticamente uma
falha a uma venda perdida.

## Hipótese principal

Uma auditoria padronizada de LP-001 e LP-002:

- é comprável por pelo menos R$ 500;
- pode ser produzida com dados legitimamente fornecidos;
- gera recomendações compreensíveis;
- pode ter pelo menos 30% do tempo produtivo reduzido por ferramenta
  local-first, com processamento no navegador;
- pode operar com descarte automático inferior a 20% e proxy de achados não
  sugeridos inferior a 20%.

O piloto preliminar gratuito `R1A` valida operação, utilidade e compreensão. Ele
não valida disposição a pagar. A hipótese de compra por pelo menos R$ 500 só
pode ser considerada validada por um piloto pago posterior, em `R1B`.

## Usuário inicial

Consultor que vende, executa e apresenta auditorias. Clientes não acessam
software no primeiro estágio.

## Direção da v1

- Ferramenta de uso interno do consultor.
- Código, documentação e fixtures sintéticas em repositório público; previews e
  aplicação protegidos por controle de acesso.
- Análise exclusiva de LP-001 e LP-002.
- Interface estática hospedada e protegida no Cloudflare Pages.
- Conversas processadas somente no navegador.
- Nenhum banco, backend, upload de conversas ou telemetria.
- Estado persistido em arquivo local criptografado.
- HTML e CSV experimentais; PDF contratado produzido manualmente.
- Piloto preliminar gratuito antes do primeiro piloto pago.
- Beta somente após o piloto pago e os gates técnicos.
- Versão estável após segundo piloto independente e gate final.

O detalhamento e as dependências estão em [`ROADMAP.md`](ROADMAP.md).

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
- Analisar grupos, anexos, áudios ou mídia. Marcadores de mídia apenas bloqueiam
  conclusão automática até esclarecimento autorizado.
- Construir SaaS antes dos gates.

## Gates do produto

O parser e a vertical slice só podem ser iniciados depois de seus gates
específicos. Preview protegido pode usar apenas fixtures sintéticas. A beta
produtiva exige primeiro piloto pago, parser aprovado e gate de continuidade.
A versão estável exige um segundo piloto independente e todos os critérios de
`GATE-STATUS.md` documentados.

## Métricas de sucesso

- Piloto preliminar: custo zero, sem alegação de validação de preço.
- Piloto pago posterior: pagamento total ≥ R$ 500.
- Utilidade percebida ≥ 4/5.
- Compreensão ≥ 4 de 5 respostas corretas.
- Esclarecimento pós-leitura ≤ 15 minutos.
- Redução de `production_active_seconds` ≥ 30%.
- `total_service_active_seconds` não aumenta; minutos são apenas apresentação
  arredondada.
- Descarte automático < 20%.
- `manual_addition_rate` < 20%, tratado como proxy de achados não sugeridos e
  não como taxa absoluta de omissão.
