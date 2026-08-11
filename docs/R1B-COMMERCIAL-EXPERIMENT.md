# R1B — Piloto assistido pago

| Campo | Valor |
|---|---|
| Versão | 2.0 |
| Estado | `BLOCKED_UNTIL_R1A_PASS` |
| Modelo | `PAID_ASSISTED_PILOT` |
| Duração | 30 dias |
| Preço do piloto | `PAID_PILOT_PRICE=R$99.00` |
| Estado do preço | `HYPOTHESIS_ONLY` |
| Pagamento | `UPFRONT` |
| Limite operacional | `OPERATIONAL_LIMIT=PENDING_OWNER_DECISION` |
| Autorização de execução | `PENDING_OWNER_DECISION` |

Este documento pré-registra um experimento comercial possível depois do R1A.
Não é oferta vigente, autorização de cobrança ou `GO_PRODUCT`. A execução exige
simultaneamente `R1A PASS`, limite operacional definido e nova autorização
explícita do proprietário.

## Hipótese

Prestadores da vertical validada no R1A podem pagar antecipadamente R$ 99 por
30 dias de acompanhamento assistido e manual de oportunidades comerciais
paradas, apresentado como lista de no máximo cinco prioridades, seus motivos e
próximas ações.

A aquisição inicial continua direta e relacional, por rede pessoal, indicações,
bairro e cidade, sem mídia paga. O Radar investiga o wedge
`MOBILE_FIELD_PROVIDER_NO_CRM`: não pretende substituir CRM, exigir funil
mantido pelo prestador nem competir por quantidade de funcionalidades.

## Formato a testar

- piloto assistido pago com duração de 30 dias;
- pagamento antecipado de R$ 99;
- sem período gratuito depois do R1A;
- sem cartão obrigatório;
- sem cobrança ou renovação automática;
- acompanhamento manual, com operação e controles definidos antes do início;
- pelo menos cinco ofertas explícitas do piloto.

`PAID_PILOT_PRICE=R$99.00` é `HYPOTHESIS_ONLY`: não é preço validado,
recomendado pelo mercado ou comprovadamente sustentável. A hipótese de
`MONTHLY_PRICE=R$49.90` está `SUPERSEDED`, assim como a hipótese de R$ 149 por
sete dias. A oferta de auditoria por R$ 500 permanece histórica e `SUPERSEDED`.

## Evidência comercial

Pagamento efetivamente recebido é a evidência comercial. Aceite verbal, elogio,
intenção, promessa, “eu pagaria” ou resposta positiva podem ser registrados
somente como diagnóstico e nunca substituem pagamento.

Um pagamento recebido já comprova o aceite daquele cliente; não existe gate
separado ou redundante de aceitação.

Depois de pelo menos cinco ofertas explícitas, aplicar exatamente:

| Pagamentos reais recebidos | Resultado |
|---:|---|
| `0` | `STOP` |
| `1` | `INSUFFICIENT_EVIDENCE` |
| `>=2` | `COMMERCIAL_SIGNAL_TO_INVESTIGATE` |

`COMMERCIAL_SIGNAL_TO_INVESTIGATE` não é `GO_PRODUCT`, não autoriza automação e
não comprova recorrência ou sustentabilidade econômica.

## Gate operacional

Antes do início, o proprietário deve definir um limite mensurável para
`OPERATIONAL_LIMIT`. O Codex e a Engenharia não inventam esse número.

Medir por cliente:

- tempo ativo total do operador;
- tempo de preparação;
- tempo de acompanhamento;
- tempo de deslocamento;
- número de intervenções manuais.

O objetivo é impedir que R$ 99 por 30 dias esconda um serviço manual
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
