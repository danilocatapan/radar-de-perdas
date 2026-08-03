# Modelo de relatório do piloto — Radar de Perdas

| Campo | Valor |
|---|---|
| Versão do template | 1.0-draft |
| Código do piloto | `[PILOT_ID]` |
| Empresa/unidade | `[PREENCHER]` |
| Período analisado | `[INÍCIO]` a `[FIM]` |
| Metodologia | `AUDIT-METHOD-v0.1` |
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
| Horário comercial | `[PREENCHER]` |
| SLA de resposta útil | `[N] minutos úteis` |
| Fuso | `[IANA]` |

Explicar todas as exclusões e seus motivos.

## 3. Metodologia e limitações

- Uma solicitação é um bloco de mensagens consecutivas do prospect.
- LP-001 considera a primeira resposta humana útil.
- LP-002 exige encerramento sem resposta humana útil.
- Resultados e elegibilidade são confirmados manualmente.

Limitações específicas da amostra:

```text
[PREENCHER]
```

## 4. Indicadores

| Indicador | Numerador | Denominador | Resultado | Observação |
|---|---:|---:|---:|---|
| Solicitações com LP-001 | `[N]` | `[N]` | `[%]` | |
| Solicitações com LP-002 | `[N]` | `[N]` | `[%]` | |
| Tempo útil médio de primeira resposta | — | `[N]` | `[min]` | |
| Tempo útil mediano de primeira resposta | — | `[N]` | `[min]` | |
| Solicitações pendentes | `[N]` | `[N]` | `[%]` | Não contam como LP-002 |
| Itens fora do escopo | `[N]` | `[N]` | `[%]` | |

Apresentar sempre o denominador. Não calcular percentual quando o denominador
for zero.

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

## 12. Aceite e correções factuais

```text
Data de envio:
Data da apresentação:
Prazo para correções:
Correções recebidas:
Versão final:
Responsável pelo aceite:
```

## 13. Checklist do revisor

- [ ] Todos os achados foram confirmados manualmente.
- [ ] Numeradores e denominadores foram conferidos.
- [ ] Evidências usam o trecho mínimo.
- [ ] Não há promessa de venda ou receita perdida.
- [ ] Causas estão identificadas como hipóteses.
- [ ] O documento é descrito como redigido/pseudonimizado.
- [ ] Dados pessoais desnecessários foram removidos.
- [ ] Limitações estão visíveis no resumo e na metodologia.
