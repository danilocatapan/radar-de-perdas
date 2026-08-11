# Estado dos gates

| Campo | Valor |
|---|---|
| Versão | 3.0 |
| Responsável | Proprietário do Radar de Perdas |
| Última revisão | 2026-08-10 |

Estados pendentes ou bloqueados não autorizam a etapa seguinte. Atualize este
documento somente com evidência verificável e nunca converta fixture, intenção
ou elogio em validação de mercado.

## R0-PIVOT — preparação do novo discovery

| Gate | Estado | Evidência necessária |
|---|---|---|
| Pivot registrado sem apagar o histórico | COMPLETE | Decisões `R0-DEC-012` e `R0-DEC-013`; documentos antigos identificados como `SUPERSEDED` |
| Posicionamento e ICP atualizados | COMPLETE | README, produto e persona consistentes |
| Roteiro e convite do R1A disponíveis | COMPLETE | `R1A-DISCOVERY.md` e novo convite |
| `DISCOVERY_SESSION_READY` disponível | COMPLETE | Checklist simples sem cadeia de custódia |
| Registro pseudônimo vazio disponível | COMPLETE | CSV sem dados reais e com cabeçalho validado |
| Representação sintética mínima | COMPLETE | Quatro itens, formato vertical e sem códigos internos na experiência |
| `R1A_READY` | COMPLETE | Suíte documental integral verde; nenhuma evidência externa alegada |

`R1A_READY` autoriza somente abordar e executar discovery com um prestador
qualificado. Não é `GO` de produto, integração ou automação.

## Gate leve `DISCOVERY_SESSION_READY`

| Verificação | Estado inicial |
|---|---|
| Prestador compatível com o ICP | PENDING |
| Objetivo e limites explicados | PENDING |
| Prestador controla fisicamente o aparelho | PENDING |
| Sem fotografia, gravação ou captura | PENDING |
| Sem cópia ou exportação | PENDING |
| Sem retenção de mensagens ou nomes reais | PENDING |
| Conversas sensíveis ou incompatíveis serão ignoradas | PENDING |
| Registro limitado aos campos autorizados | PENDING |

O resultado é `READY` somente quando todos os itens forem confirmados para a
sessão concreta. Não criar manifesto, hash, ACL, USB ou cadeia de custódia para
esse fluxo sem arquivos.

## R1A — cinco prestadores

| Gate | Estado | Critério verificável |
|---|---|---|
| Cinco sessões concluídas | BLOCKED_EXTERNAL | Cinco códigos de sessão com dia 1 e follow-ups registrados |
| Problema existe | BLOCKED_EXTERNAL | Pelo menos 4 de 5 prestadores têm uma oportunidade candidata |
| Oportunidade relevante esquecida | BLOCKED_EXTERNAL | Pelo menos 3 de 5 confirmam ao menos uma |
| Ação executada | BLOCKED_EXTERNAL | Pelo menos 3 de 5 executam ao menos uma ação relevante |
| Interesse recorrente | BLOCKED_EXTERNAL | Pelo menos 3 de 5 querem receber novamente a lista ou revisão |
| Gate do R1A | BLOCKED_EXTERNAL | Todos os quatro critérios por prestador atendidos |

Métricas de taxas, reativação, serviço confirmado e tempo são diagnósticas e
não substituem os quatro critérios. O detalhe permanece fora do Git; somente
resultados agregados e não identificáveis podem ser registrados no repositório.

## Teste pago posterior

| Gate | Estado | Condição |
|---|---|---|
| Hipótese de R$ 149 por sete dias | HYPOTHESIS_ONLY | Não é oferta aprovada nem formato congelado |
| Preparação do teste pago | BLOCKED | Gate do R1A completo e decisão explícita do proprietário |
| Evidência comercial | BLOCKED_EXTERNAL | Pagamento real; manifestação verbal não basta |

O antigo `R1B` de auditoria por R$ 500 está `SUPERSEDED`. Nenhuma oferta nova
será finalizada neste marco.

## Backlog técnico

| Capacidade | Estado | Condição mínima futura |
|---|---|---|
| Contrato final de ingestão | BLOCKED | Corpus autorizado revisado e nova decisão |
| Parser | BLOCKED | Contrato final aprovado e problema de ingestão comprovado |
| Frontend, backend ou banco | BLOCKED | Teste pago e novo gate técnico |
| IA ou classificação automática | BLOCKED | Evidência, arquitetura, privacidade e segurança aprovadas |
| Integração WhatsApp | BLOCKED | Viabilidade técnica e jurídica decidida depois da validação |
| Infraestrutura produtiva | BLOCKED | Gate comercial, operacional e técnico posterior |

## Materiais históricos

- `PILOT-OFFER.md`: `SUPERSEDED` como oferta vigente.
- `PILOT-PRELIMINARY-INVITATION.md`: `SUPERSEDED` pelo convite de discovery.
- `PILOT-REPORT-TEMPLATE.md`: `SUPERSEDED` como experiência principal.
- `AUDIT-METHOD-v0.1.md`: método histórico e evidência auxiliar.
- `OPERATOR-RUNBOOK.md`: fluxo de auditoria com custódia, não aplicável ao R1A.
- `REAL_DATA_READY`: permanece bloqueado e não é substituído quando houver
  recebimento de arquivos; simplesmente não se aplica à sessão sem custódia.
