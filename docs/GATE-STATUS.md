# Estado dos gates

| Campo | Valor |
|---|---|
| Versão | 3.2 |
| Responsável | Proprietário do Radar de Perdas |
| Última revisão | 2026-08-11 |

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

`R1A_READY=COMPLETE` permanece inalterado e comprova somente prontidão
documental. Autoriza recrutamento e qualificação, mas a primeira sessão depende
dos gates separados abaixo. Não é `GO` de produto, integração ou automação.

## Seleção da vertical e primeira sessão

| Gate | Estado | Condição para mudança |
|---|---|---|
| `VERTICAL_SELECTION` | `PENDING_OWNER_SELECTION` | Proprietário escolhe uma vertical com capacidade real de recrutar cinco prestadores pela rede pessoal, indicações, bairro ou cidade |
| `FIRST_R1A_SESSION` | `BLOCKED` | `VERTICAL_SELECTION=COMPLETE` e `DISCOVERY_SESSION_READY=READY` para a sessão concreta |

Os cinco participantes devem pertencer à mesma vertical. Exemplos de segmentos
não constituem decisão e o Codex não escolhe a vertical.

## Gate leve `DISCOVERY_SESSION_READY`

| Verificação | Estado inicial |
|---|---|
| `VERTICAL_SELECTION=COMPLETE` | PENDING |
| Prestador pertence à vertical selecionada | PENDING |
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
| Substitutos atuais avaliados | BLOCKED_EXTERNAL | Se pelo menos 3 de 5 os considerarem suficientes, resultado `STOP` para a hipótese atual |
| Frequência do problema avaliada | BLOCKED_EXTERNAL | Problema excessivamente episódico mantém R1B bloqueado e exige decisão explícita |
| Gate do R1A | BLOCKED_EXTERNAL | Todos os quatro critérios por prestador atendidos |

Métricas de taxas, reativação, serviço confirmado e tempo são diagnósticas e
não substituem os quatro critérios. O detalhe permanece fora do Git; somente
resultados agregados e não identificáveis podem ser registrados no repositório.
Dispositivo principal, uso de WhatsApp Web, aceitação de ferramenta externa e
origem da aquisição também são diagnósticos do wedge
`MOBILE_FIELD_PROVIDER_NO_CRM`; não formam gate autônomo.

Falha de qualquer gate central bloqueia o R1B. `STOP` encerra somente a hipótese
ou etapa atual; repetição, reformulação ou pivot exigem nova decisão explícita
do proprietário e não arquivam automaticamente o repositório.

## R1B — experimento comercial posterior

| Gate | Estado | Condição |
|---|---|---|
| Protocolo documental | COMPLETE | [`R1B-COMMERCIAL-EXPERIMENT.md`](R1B-COMMERCIAL-EXPERIMENT.md) |
| Estado do R1B | `BLOCKED_UNTIL_R1A_PASS` | Todos os gates centrais do R1A aprovados e nenhuma condição de STOP |
| Nova autorização do proprietário | PENDING_OWNER_DECISION | Decisão explícita posterior ao R1A PASS |
| Modelo | `PAID_ASSISTED_PILOT` | Piloto assistido manual por 30 dias; não é produto ou assinatura |
| `PAID_PILOT_PRICE=R$99.00` | `HYPOTHESIS_ONLY` | Pagamento `UPFRONT`; não é preço validado, recomendado ou economicamente sustentável |
| `OPERATIONAL_LIMIT` | `PENDING_OWNER_DECISION` | Limite definido pelo proprietário antes do R1B |
| Pelo menos cinco ofertas explícitas | BLOCKED_EXTERNAL | Contagem agregada e referência externa não identificável |
| Pagamentos reais recebidos | BLOCKED_EXTERNAL | Comprovantes fora do Git; intenção ou aceite verbal não substituem pagamento |
| Resultado comercial | BLOCKED | `0=STOP`; `1=INSUFFICIENT_EVIDENCE`; `>=2=COMMERCIAL_SIGNAL_TO_INVESTIGATE` |
| Evolução para produto | BLOCKED | Recorrência, gargalo repetitivo, viabilidade operacional, decisão Produto/Negócios e controles aplicáveis |

Um pagamento recebido já comprova o aceite de continuidade daquele cliente; não
existe gate redundante de aceitação. Uma revisão controlada da oferta depende de
nova decisão explícita e, persistindo resultado abaixo de dois pagamentos, a
hipótese recebe `STOP`. `COMMERCIAL_SIGNAL_TO_INVESTIGATE` não é `GO_PRODUCT`.

Não há período gratuito depois do R1A, cartão obrigatório ou renovação
automática. `MONTHLY_PRICE=R$49.90`, a hipótese de R$ 149 por sete dias e o
antigo `R1B` de auditoria por R$ 500 continuam históricos e `SUPERSEDED`.

## Backlog técnico

| Capacidade | Estado | Condição mínima futura |
|---|---|---|
| Contrato final de ingestão | BLOCKED | Corpus autorizado revisado e nova decisão |
| Parser | BLOCKED | Contrato final aprovado e problema de ingestão comprovado |
| Frontend, backend ou banco | BLOCKED | Teste pago e novo gate técnico |
| IA ou classificação automática | BLOCKED | Evidência, arquitetura, privacidade e segurança aprovadas |
| Integração WhatsApp | BLOCKED | Viabilidade técnica e jurídica decidida depois da validação |
| Automação, notificações ou cobrança | BLOCKED | Evidência recorrente, decisão Produto/Negócios e gates técnicos aplicáveis |
| Infraestrutura produtiva | BLOCKED | Gate comercial, operacional e técnico posterior |

## Materiais históricos

- `PILOT-OFFER.md`: `SUPERSEDED` como oferta vigente.
- `PILOT-PRELIMINARY-INVITATION.md`: `SUPERSEDED` pelo convite de discovery.
- `PILOT-REPORT-TEMPLATE.md`: `SUPERSEDED` como experiência principal.
- `AUDIT-METHOD-v0.1.md`: método histórico e evidência auxiliar.
- `OPERATOR-RUNBOOK.md`: fluxo de auditoria com custódia, não aplicável ao R1A.
- `REAL_DATA_READY`: permanece bloqueado e não é substituído quando houver
  recebimento de arquivos; simplesmente não se aplica à sessão sem custódia.
