# Roadmap de validação — Radar de Perdas

| Campo | Valor |
|---|---|
| Versão | 3.1 |
| Prioridade | `R1A_READY → VERTICAL_SELECTION → R1A → R1B bloqueado` |
| Status | `R1A_READY=COMPLETE`; primeira sessão bloqueada |
| Última revisão | 2026-08-11 |

## 1. R0-PIVOT — preparar o discovery

Objetivo: tornar inequívoco que o produto deixou de validar auditorias de
demora e ausência de resposta e passou a investigar oportunidades comerciais
que ainda merecem ação.

Entregas autorizadas:

- posicionamento, persona, gates e histórico atualizados;
- convite e roteiro concisos do Discovery Concierge;
- checklist simples para sessão sem custódia;
- registro pseudônimo vazio;
- representação sintética mínima da lista de ações;
- testes documentais proporcionais.

Condição de saída concluída: `R1A_READY=COMPLETE`. Esse estado registra
prontidão documental e não será reaberto pela seleção da vertical. Refinamento
da demo, oferta paga e arquitetura não pertencem a esta etapa.

## 2. R1A — Discovery Concierge

Executar cinco sessões gratuitas com prestadores compatíveis com o ICP e da
mesma vertical.

`VERTICAL_SELECTION=PENDING_OWNER_SELECTION` e
`FIRST_R1A_SESSION=BLOCKED`. O proprietário deve selecionar uma vertical na
qual consiga recrutar cinco prestadores reais por amigos, conhecidos,
indicações, bairro ou cidade. O Codex não faz essa escolha. Não haverá mídia
paga nesta fase.

A primeira sessão só pode ocorrer com `VERTICAL_SELECTION=COMPLETE` e o
`DISCOVERY_SESSION_READY` da sessão concreta em `READY`.

Fluxo por prestador:

1. confirmar a vertical selecionada e conferir `DISCOVERY_SESSION_READY`;
2. realizar uma sessão presencial de 20–30 minutos no aparelho controlado pelo
   prestador;
3. investigar como etiquetas, estrela, agenda, caderno, memória, CRM ou outros
   métodos evitam esquecimentos e onde falham;
4. registrar, quando legitimamente conhecidas, faixas de contatos/orçamentos
   semanais e ticket típico, sem identificar clientes ou alegar receita perdida;
5. classificar manualmente os quatro estados permitidos e registrar padrões
   externos apenas como `OUT_OF_SCOPE_CANDIDATE`;
6. confirmar relevância, esquecimento, causa da paralisação e próxima ação;
7. fazer contatos curtos nos dias 4 e 7, sem nova revisão completa do WhatsApp;
8. registrar ação, desfecho, interesse recorrente e custo operacional.

### Gate por prestador

Todos os critérios são obrigatórios:

| Pergunta | Critério |
|---|---|
| O problema existe? | Pelo menos 4 de 5 têm uma oportunidade candidata |
| A oportunidade foi esquecida e importa? | Pelo menos 3 de 5 confirmam uma oportunidade relevante esquecida |
| A lista leva à ação? | Pelo menos 3 de 5 executam alguma ação relevante |
| Existe interesse recorrente? | Pelo menos 3 de 5 querem receber novamente esse acompanhamento |

Taxas de relevância, falsos positivos e execução, além de reativações, serviços
confirmados e tempos, são diagnósticos. Devem mostrar numerador e denominador,
mas não representam evidência estatística com cinco participantes.

### Regras de parada do R1A

- Se todos os critérios forem atingidos e nenhuma condição de parada ocorrer,
  o proprietário pode decidir preparar o R1B.
- Se algum critério central falhar, o R1B permanece bloqueado.
- Se pelo menos três de cinco prestadores considerarem os substitutos atuais
  suficientes, registrar `STOP` para a hipótese atual.
- Se o problema for excessivamente episódico para acompanhamento recorrente, o
  R1B permanece bloqueado e o proprietário registra a decisão.

`STOP` encerra somente a hipótese ou etapa atual. Repetição, reformulação ou
pivot exigem nova decisão explícita; não arquivam automaticamente o repositório
nem geram feature.

## 3. R1B — experimento comercial posterior

O protocolo está em
[`R1B-COMMERCIAL-EXPERIMENT.md`](R1B-COMMERCIAL-EXPERIMENT.md), inicialmente
`BLOCKED_UNTIL_R1A_PASS`. Mesmo após o R1A, exige nova autorização explícita do
proprietário e `OPERATIONAL_LIMIT` definido.

A hipótese é oferecer até 30 dias gratuitos, sem cartão obrigatório ou cobrança
automática, e então apresentar pelo menos cinco ofertas explícitas de
continuidade por `MONTHLY_PRICE=R$49.90`, com estado `HYPOTHESIS_ONLY`.

| Pagamentos reais recebidos | Resultado |
|---:|---|
| `0` | `STOP` |
| `1` | `INSUFFICIENT_EVIDENCE` |
| `>=2` | `COMMERCIAL_SIGNAL_TO_INVESTIGATE` |

Um pagamento recebido já comprova o aceite daquele cliente. Intenção, elogio ou
promessa são apenas diagnóstico. `COMMERCIAL_SIGNAL_TO_INVESTIGATE` não é
`GO_PRODUCT`.

Medir tempo ativo por cliente, preparação, acompanhamento, deslocamento e
intervenções manuais. Evolução para produto permanece bloqueada até recorrência,
gargalo manual repetitivo, viabilidade operacional, decisão Produto/Negócios e
validações de Segurança/Privacidade aplicáveis.

A hipótese de R$ 149 por sete dias está `SUPERSEDED`. A auditoria por R$ 500
permanece histórica e `SUPERSEDED`.

## 4. Backlog bloqueado

Os itens abaixo não possuem cronograma, arquitetura escolhida ou autorização:

- estratégia de integração com WhatsApp, Coexistence ou Cloud API;
- ingestão, parser e classificação automática;
- frontend, backend, banco, IA e notificações;
- arquitetura produtiva, assinatura e onboarding;
- automação, multiusuário e novas verticais.

Mesmo um teste pago completo não autoriza automaticamente implementação. Uma
nova decisão deve definir o menor problema comprovado e os gates técnicos,
jurídicos, operacionais e de privacidade aplicáveis.

## 5. Invariáveis

- Dados reais e holdout privado nunca entram no Git.
- Hipótese, evidência, estimativa e decisão permanecem separadas.
- `OUT_OF_SCOPE_CANDIDATE` não expande o produto automaticamente.
- Ausência ou demora de resposta não prova venda ou receita perdida.
- A sessão sem custódia minimiza exposição, mas não é descrita como ausência de
  tratamento de dados.
- Decisões históricas permanecem preservadas como `SUPERSEDED` quando aplicável.
- Falha comercial bloqueia evolução para produto; qualquer repetição, mudança de
  hipótese ou pivot exige nova decisão explícita do proprietário.
