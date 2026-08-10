# Modelo de relatório do piloto — Radar de Perdas

| Campo | Valor |
|---|---|
| Versão do template | 1.1 |
| Código do piloto | `[PILOT_ID]` |
| Modalidade | `[R1A_GRATUITO | R1B_PAGO]` |
| Empresa/unidade | `[PREENCHER]` |
| Período analisado | `[INÍCIO]` a `[FIM]` |
| Regra do período | Início inclusivo; fim exclusivo |
| `evaluation_at` | `[TIMESTAMP ISO 8601 COM FUSO]` |
| Origem de `evaluation_at` | `[EXPORT_DECLARED | RECEIVED_AT_FALLBACK]` |
| Versão metodológica | `AUDIT-METHOD-v0.1` |
| Versão da configuração | `[CONFIG_VERSION]` |
| Data do relatório | `[PREENCHER]` |
| Revisor humano | `[PREENCHER]` |

> Classificação: relatório redigido ou pseudonimizado. A substituição de nomes
> não garante anonimização segundo a LGPD.

## 1. Resumo executivo

Descrever em linguagem não técnica:

- o que foi analisado;
- os dois ou três achados mais relevantes;
- o que merece ação imediata;
- as principais limitações.

Não afirmar que um achado corresponde a venda ou receita perdida.

## 2. Escopo, período e amostra

| Item | Quantidade/valor |
|---|---:|
| Chats recebidos | `[N]` |
| Chats aceitos | `[N]` |
| Chats excluídos | `[N]` |
| Solicitações elegíveis | `[N]` |
| Período | `[PREENCHER]` |
| Limites do período | Início inclusivo; fim exclusivo |
| Instante de corte (`evaluation_at`) | `[PREENCHER]` |
| Horário comercial | `[PREENCHER]` |
| Exceções de expediente | `[FERIADOS/FECHAMENTOS OU NENHUMA]` |
| SLA de resposta útil | `[N] minutos úteis` |
| Fuso | `[IANA]` |
| Versão da configuração | `[PREENCHER]` |
| Versão metodológica | `[PREENCHER]` |

Explicar todas as exclusões e seus motivos.

Usar como `evaluation_at` o instante declarado da exportação. Se a exportação
não o declarar, usar o instante de recebimento dos arquivos e registrar
`RECEIVED_AT_FALLBACK`; não inferir outro corte silenciosamente.

## 3. Metodologia e limitações

- Uma solicitação é um bloco de mensagens consecutivas do prospect.
- LP-001 considera a primeira resposta humana útil.
- LP-002 exige encerramento sem resposta humana útil.
- Resultados e elegibilidade são confirmados manualmente.

Configuração efetivamente aplicada:

```text
Versão da metodologia:
Versão da configuração:
Fuso:
Agenda semanal:
Exceções de expediente:
SLA configurado:
evaluation_at:
Origem de evaluation_at:
```

Limitações específicas da amostra:

```text
[PREENCHER]
```

## 4. Indicadores

| Indicador | Numerador | Denominador | Resultado | Observação |
|---|---:|---:|---:|---|
| Solicitações com LP-001 | `[N]` | `[SOLICITAÇÕES ELEGÍVEIS COM RESPOSTA ÚTIL E RELÓGIO CONFIGURADO]` | `[% OU INCONCLUSIVE]` | |
| Solicitações com LP-002 | `[N]` | `[SOLICITAÇÕES ELEGÍVEIS COM CICLO ENCERRADO E SEM RESPOSTA NÃO VERIFICÁVEL PENDENTE]` | `[% OU INCONCLUSIVE]` | Numerador exige ausência de resposta útil |
| Tempo útil médio de primeira resposta | — | `[N]` | `[min]` | |
| Tempo útil mediano de primeira resposta | — | `[N]` | `[min]` | |
| Solicitações pendentes | `[N]` | `[SOLICITAÇÕES ELEGÍVEIS]` | `[%]` | Não contam como LP-002 |
| Solicitações com resposta não verificável | `[N]` | `[SOLICITAÇÕES ELEGÍVEIS]` | `[%]` | Não geram LP-002 automático |
| Chats fora do escopo | `[CHATS EXCLUÍDOS]` | `[CHATS RECEBIDOS]` | `[%]` | Informar motivos de exclusão |

Apresentar sempre o denominador. Não calcular percentual quando o denominador
for zero ou insuficiente para o critério avaliado; nesses casos, exibir
`INCONCLUSIVE`, informar a quantidade observada e explicar a insuficiência.

Registro dos denominadores:

```text
Denominador de LP-001:
Exclusões do denominador de LP-001:
Denominador de LP-002:
Exclusões do denominador de LP-002:
Denominador de tempos de resposta:
Critério mínimo aplicável:
Conclusão sobre suficiência:
```

## 5. LP-001 confirmados

Para cada achado:

```text
Código:
Chat pseudonimizado:
Solicitação:
Recebimento:
Início do relógio útil:
Primeira resposta útil:
Tempo útil:
SLA:
Versão da metodologia:
Versão da configuração:
Evidência redigida:
Confirmação humana:
Observação:
```

## 6. LP-002 confirmados

Para cada achado:

```text
Código:
Chat pseudonimizado:
Solicitação:
Recebimento:
Encerramento:
Motivo do encerramento:
evaluation_at:
Versão da metodologia:
Versão da configuração:
Evidência redigida:
Confirmação humana:
Observação:
```

## 7. Exemplos redigidos

Usar somente o trecho mínimo necessário. Remover ou substituir:

- nomes;
- telefones;
- e-mails;
- documentos;
- endereços;
- datas ou produtos que não sejam necessários à conclusão.

Marcar qualquer contexto ainda potencialmente reidentificável.

## 8. Causas prováveis

Esta seção contém hipóteses, não fatos comprovados.

| Hipótese | Evidência que a sustenta | Como validar |
|---|---|---|
| `[PREENCHER]` | `[PREENCHER]` | `[PREENCHER]` |

## 9. Recomendações

| Recomendação | Achado relacionado | Responsável sugerido | Resultado esperado |
|---|---|---|---|
| `[PREENCHER]` | `[LP-...]` | `[PREENCHER]` | `[PREENCHER]` |

## 10. Prioridades

Classificar cada recomendação como:

- `CORRIGIR_AGORA`;
- `CORRIGIR_DEPOIS`;
- `NAO_PRIORIZAR`.

Justificar a prioridade sem estimar ganho financeiro não demonstrado.

## 11. Próximos passos

- Ação imediata.
- Responsável.
- Data de revisão sugerida.
- Indicador a acompanhar.
- Condição para uma auditoria futura.

## 12. Avaliação de utilidade e compreensão

Aplicar a rubrica definida em [`PILOT-BASELINE.md`](PILOT-BASELINE.md) depois
que o decisor ler o relatório, antes de qualquer orientação sobre as respostas.

```text
Nota de utilidade (1–5):
Respostas corretas de compreensão (0–5):
Esforço ativo de esclarecimento em segundos:
Esforço ativo de esclarecimento apresentado em minutos:
Utilidade >= 4/5: YES | NO | INCONCLUSIVE
Compreensão >= 4/5: YES | NO | INCONCLUSIVE
Esclarecimento <= 15 minutos: YES | NO | INCONCLUSIVE
Feedback livre:
```

No `R1A`, não solicitar nem inferir disposição a pagar. O piloto gratuito não
completa o gate comercial pago.

## 13. Aceite e correções factuais

```text
Data de envio:
Data da apresentação:
Prazo para correções:
Correções recebidas:
Versão final:
Responsável pelo aceite:
```

## 14. Aprovação interna e checklist do revisor

```text
Responsável: Proprietário do Radar de Perdas
Decisão: INTERNAL_APPROVED
Escopo da decisão: uso como template dos pilotos R1A e R1B
```

- [ ] Todos os achados foram confirmados manualmente.
- [ ] Numeradores e denominadores foram conferidos.
- [ ] `evaluation_at`, sua origem e as versões aplicadas foram registradas.
- [ ] Agenda e exceções de expediente foram registradas.
- [ ] Evidências usam o trecho mínimo.
- [ ] Não há promessa de venda ou receita perdida.
- [ ] Causas estão identificadas como hipóteses.
- [ ] O documento é descrito como redigido/pseudonimizado.
- [ ] Dados pessoais desnecessários foram removidos.
- [ ] Limitações estão visíveis no resumo e na metodologia.
