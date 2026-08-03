# Metodologia de auditoria v0.1

| Campo | Valor |
|---|---|
| Versão | 0.1 |
| Escopo | LP-001 e LP-002 |
| Status | Aguardando aprovação |
| Responsável por aprovação | Consultor do Radar de Perdas |

## 1. Finalidade

Padronizar a identificação de demora e ausência de resposta sem confundir falha
de atendimento com venda perdida.

## 2. Papéis

- `PROSPECT`: contato confirmado como potencial cliente.
- `AGENT`: pessoa confirmada como representante do negócio.
- `SYSTEM`: automação ou evento do WhatsApp.
- `UNKNOWN`: papel ainda não confirmado.

Somente solicitações de `PROSPECT` entram nos indicadores. A existência do papel
`UNKNOWN` bloqueia a avaliação automática do ciclo.

## 3. Unidade de análise

### 3.1 Chat

Histórico textual entre o negócio e um contato, proveniente de um único arquivo
individual.

### 3.2 Ciclo

Parte do chat correspondente a um atendimento. Um novo ciclo começa depois de
sete dias corridos sem mensagens, salvo encerramento explícito anterior.

### 3.3 Solicitação

Bloco de uma ou mais mensagens consecutivas enviadas por um `PROSPECT`, encerrado
pela primeira resposta humana útil.

- Mensagens adicionais do prospect antes da resposta pertencem ao mesmo bloco.
- Uma resposta útil encerra o bloco.
- Um novo bloco posterior pode criar nova solicitação.
- Uma mensagem iniciada pelo negócio não cria solicitação.
- Após contato ativo do negócio, uma resposta do prospect só inicia solicitação
  se contiver dúvida, pedido ou interesse confirmado pelo consultor.

## 4. Elegibilidade

### 4.1 Incluído

- Prospect confirmado.
- Solicitação recebida dentro do período da auditoria.
- Conteúdo textual suficiente para avaliar pergunta e resposta.
- Participantes resolvidos.

### 4.2 `OUT_OF_SCOPE`

- Cliente existente tratando suporte ou pós-venda.
- Fornecedor.
- Contato interno.
- Spam.
- Chat em grupo.
- Conversa sem finalidade comercial.
- Arquivo incompatível.
- Ciclo anterior ao período sem nova solicitação elegível.

### 4.3 Avaliação manual obrigatória

- Áudio ou mídia potencialmente usados como resposta.
- Relação do contato desconhecida.
- Mensagem ambígua quanto a pedido ou interesse.
- Participante não resolvido.

## 5. Resposta humana útil

Mensagem de `AGENT` que satisfaz pelo menos uma condição:

1. responde à pergunta;
2. fornece orientação relevante; ou
3. solicita informação necessária para o atendimento avançar.

Não são respostas úteis:

- resposta automática;
- reação;
- figurinha;
- evento de sistema;
- marcador de chamada;
- marcador de mídia omitida;
- “aguarde”, “um momento” ou equivalente sem orientação adicional.

Um reconhecimento humano sem conteúdo útil pode preencher
`acknowledgement_at`, mas não `valid_response_at`.

Áudio ou mídia enviada pelo negócio é `UNVERIFIABLE_RESPONSE`: registra contato,
interrompe qualquer conclusão automática de LP-002 e exige revisão.

## 6. Relógios

Para cada solicitação registrar:

- `received_at`: primeira mensagem do bloco;
- `business_clock_start_at`: início efetivo do SLA;
- `acknowledgement_at`: primeiro reconhecimento humano, se houver;
- `valid_response_at`: primeira resposta útil, se houver;
- `elapsed_response_seconds`: tempo corrido;
- `business_response_seconds`: tempo útil.

### 6.1 Início do SLA

- Dentro do expediente: `business_clock_start_at = received_at`.
- Fora do expediente: próxima abertura configurada.
- Em intervalo fechado: próxima reabertura.

### 6.2 Tempo útil

Somar apenas interseções entre o intervalo da solicitação e os períodos abertos
da unidade. Fins de semana, intervalos e exceções fechadas não consomem SLA.

Persistir:

- fuso IANA;
- agenda semanal;
- exceções;
- versão da configuração;
- SLA em minutos.

Fuso padrão do piloto: `America/Sao_Paulo`.

## 7. LP-001 — demora na primeira resposta

Pré-condições:

- solicitação elegível;
- resposta humana útil disponível;
- relógio comercial configurado.

Regra:

```text
LP-001 =
  business_response_seconds >
  configured_sla_seconds
```

O limite é estrito: resposta exatamente no SLA não gera LP-001.

Evidência mínima:

- trecho redigido da solicitação;
- trecho redigido da resposta;
- timestamps;
- tempo útil;
- SLA;
- versão da metodologia.

Sem resposta útil, LP-001 não é criado.

## 8. LP-002 — ausência de resposta

Antes do encerramento, uma solicitação que ultrapassou o SLA sem resposta recebe
somente `SLA_OVERDUE`.

LP-002 exige:

- solicitação elegível;
- ciclo encerrado;
- nenhuma resposta humana útil;
- nenhuma resposta não verificável pendente de revisão.

Regra:

```text
LP-002 =
  cycle_is_closed
  AND valid_response_at IS NULL
  AND unverifiable_response_count = 0
```

## 9. Encerramento do ciclo

O ciclo encerra quando:

- o consultor confirma um resultado final; ou
- passam sete dias corridos sem novas mensagens.

Se o corte da auditoria ocorrer antes dos sete dias, o ciclo permanece
`PENDING`, ainda que o SLA esteja vencido.

## 10. Resultado comercial

- `CONVERTED`: ação comercial desejada confirmada.
- `LOST`: encerramento negativo confirmado com evidência.
- `PENDING`: ciclo ainda aberto.
- `NOT_QUALIFIED`: contato não atendia aos critérios.
- `OUT_OF_SCOPE`: conversa não pertence à auditoria.
- `UNKNOWN`: dados insuficientes.

O sistema pode sugerir apenas `PENDING` ou `UNKNOWN`. Todos os demais resultados
dependem de confirmação humana.

LP-001 ou LP-002 não determina automaticamente `LOST`.

## 11. Exemplos positivos, negativos e de fronteira

| Cenário | Classificação |
|---|---|
| Prospect pergunta às 09:00; resposta útil às 09:20; SLA 15 min | LP-001 |
| Resposta útil ocorre exatamente aos 15 min | Sem LP-001 |
| Mensagem às 22:00; abertura 08:00; resposta útil 08:10 | 10 min úteis |
| Bot responde imediatamente; humano responde em 30 min; SLA 15 | LP-001 |
| “Aguarde” em 5 min; resposta útil em 25 min; SLA 15 | Acknowledgement 5; LP-001 |
| Áudio enviado pelo negócio sem transcrição | Revisão manual; sem LP-002 automático |
| Solicitação sem resposta e sete dias de inatividade | LP-002 |
| Solicitação sem resposta há dois dias no corte | PENDING + SLA_OVERDUE |
| Negócio envia promoção; contato responde “obrigado” | Sem solicitação automática |
| Prospect envia três mensagens antes da resposta | Uma solicitação |
| Prospect faz nova pergunta após resposta útil | Nova solicitação |
| Conversa de suporte de cliente existente | OUT_OF_SCOPE |
| Papel do contato não confirmado | Bloqueado para revisão |

## 12. Revisão e métricas de qualidade

Todo achado automático recebe:

- `SUGGESTED`;
- `CONFIRMED`; ou
- `REJECTED`.

O consultor deve revisar também solicitações sem sugestão, registrando achados
manuais adicionais.

```text
auto_discard_rate =
  automatic_suggestions_rejected /
  total_automatic_suggestions_reviewed

manual_addition_rate =
  additional_manual_findings_confirmed /
  total_confirmed_findings
```

Menos de dez itens no denominador torna a métrica inconclusiva.

## 13. Controle de versão

- Mudanças após o primeiro uso produzem v0.2.
- Uma auditoria registra a versão usada.
- Não alterar exemplos ou definições retroativamente para ajustar resultados.

## 14. Aprovação

```text
Responsável:
Data:
Decisão: APPROVED | CHANGES_REQUIRED
Observações:
```
