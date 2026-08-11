# R1B — Experimento comercial posterior

| Campo | Valor |
|---|---|
| Versão | 1.0 |
| Estado | `BLOCKED_UNTIL_R1A_PASS` |
| Preço mensal | `MONTHLY_PRICE=R$49.90` |
| Estado do preço | `HYPOTHESIS_ONLY` |
| Limite operacional | `OPERATIONAL_LIMIT=PENDING_OWNER_DECISION` |
| Autorização de execução | `PENDING_OWNER_DECISION` |

Este documento pré-registra um experimento comercial possível depois do R1A.
Não é oferta vigente, autorização de cobrança ou `GO_PRODUCT`. A execução exige
simultaneamente `R1A PASS`, limite operacional definido e nova autorização
explícita do proprietário.

## Hipótese

Prestadores da vertical validada no R1A podem perceber valor recorrente em um
acompanhamento simples das oportunidades comerciais paradas, apresentado como
lista curta de próximas ações.

A aquisição inicial continua direta e relacional, por rede pessoal, indicações,
bairro e cidade, sem mídia paga. O Radar não pretende substituir CRM, competir
por quantidade de funcionalidades ou exigir funil mantido pelo prestador.

## Formato a testar

- período gratuito de no máximo 30 dias;
- sem cartão obrigatório;
- sem cobrança automática ao final;
- acompanhamento ainda manual, com operação e controles definidos antes do
  início;
- oferta explícita para continuar por R$ 49,90 por mês ao término;
- pelo menos cinco ofertas explícitas de continuidade.

R$ 49,90 não é preço validado, recomendado pelo mercado ou comprovadamente
sustentável. A hipótese de R$ 149 por sete dias está `SUPERSEDED`. A oferta de
auditoria por R$ 500 permanece histórica e `SUPERSEDED`.

## Evidência comercial

Pagamento efetivamente recebido é a evidência comercial. Aceite verbal, elogio,
intenção, promessa, “eu pagaria” ou resposta positiva podem ser registrados
somente como diagnóstico e nunca substituem pagamento.

Um pagamento recebido já comprova o aceite de continuidade daquele cliente;
não existe gate separado ou redundante de aceitação.

Depois de pelo menos cinco ofertas explícitas, aplicar exatamente:

| Pagamentos reais recebidos | Resultado |
|---:|---|
| `0` | `STOP` |
| `1` | `INSUFFICIENT_EVIDENCE` |
| `>=2` | `COMMERCIAL_SIGNAL_TO_INVESTIGATE` |

`COMMERCIAL_SIGNAL_TO_INVESTIGATE` não é `GO_PRODUCT`, não autoriza automação e
não comprova sustentabilidade econômica.

## Gate operacional

Antes do início, o proprietário deve definir um limite mensurável para
`OPERATIONAL_LIMIT`. O Codex e a Engenharia não inventam esse número.

Medir por cliente:

- tempo ativo total do operador;
- tempo de preparação;
- tempo de acompanhamento;
- tempo de deslocamento;
- número de intervenções manuais.

O objetivo é impedir que R$ 49,90 por mês esconda um serviço manual
economicamente inviável. Mesmo com dois ou mais pagamentos, automação permanece
bloqueada até haver evidência de recorrência, gargalo manual repetitivo,
viabilidade operacional analisada, decisão explícita de Produto/Negócios e
validações de Segurança/Privacidade aplicáveis.

## STOP, revisão e continuidade

`STOP` encerra a hipótese ou etapa comercial atual e bloqueia evolução para
produto. Não arquiva automaticamente o repositório, não cria uma feature e não
autoriza novo pivot.

Uma única revisão controlada da oferta pode ser considerada somente mediante
nova decisão explícita do proprietário. Se, depois dessa revisão, o resultado
continuar abaixo de dois pagamentos reais, registrar `STOP` para a hipótese.
Qualquer repetição, reformulação ou pivot posterior também exige nova decisão
explícita.

## Registros permitidos

Comprovantes, identidades, contatos, detalhes individuais e registros fiscais
permanecem fora do Git. O repositório pode receber somente contagens agregadas,
estados de gate e referência externa não identificável:

```text
explicit_paid_offers=<inteiro>
real_payments_received=<inteiro>
commercial_result=STOP | INSUFFICIENT_EVIDENCE | COMMERCIAL_SIGNAL_TO_INVESTIGATE
operational_limit_state=PENDING_OWNER_DECISION | DEFINED
operational_viability=PENDING | VIABLE | NOT_VIABLE | INCONCLUSIVE
external_evidence_reference=registro confidencial fora do Git
```

Dados reais nunca entram no Git. Nenhum modelo operacional futuro pode relaxar
os controles de privacidade ou alegar ausência de tratamento de dados sem nova
decisão aplicável.
