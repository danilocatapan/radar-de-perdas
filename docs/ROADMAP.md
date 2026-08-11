# Roadmap de validação — Radar de Perdas

| Campo | Valor |
|---|---|
| Versão | 3.0 |
| Prioridade | `R0-PIVOT → R1A → decisão sobre teste pago` |
| Status | Preparação de `R1A_READY` |
| Última revisão | 2026-08-10 |

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

Condição de saída: os instrumentos mínimos estão consistentes e o próximo passo
é conversar com um prestador qualificado. Refinamento da demo, oferta paga e
arquitetura não pertencem a esta etapa.

## 2. R1A — Discovery Concierge

Executar cinco sessões com prestadores compatíveis com o ICP.

Fluxo por prestador:

1. conferir `DISCOVERY_SESSION_READY`;
2. realizar uma sessão presencial de 20–30 minutos no aparelho controlado pelo
   prestador;
3. classificar manualmente os quatro estados permitidos e registrar padrões
   externos apenas como `OUT_OF_SCOPE_CANDIDATE`;
4. confirmar relevância, esquecimento e próxima ação com o prestador;
5. fazer contatos curtos nos dias 4 e 7, sem nova revisão completa do WhatsApp;
6. registrar ação, desfecho, interesse recorrente e custo operacional.

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

## 3. Decisão após R1A

- Se todos os critérios forem atingidos, preparar um teste pago manual com base
  no comportamento observado.
- Se algum critério falhar, o teste pago permanece bloqueado e o proprietário
  registra `PIVOT`, `REPEAT_WITH_CHANGES` ou `STOP`, sem transformar sinais
  isolados em aprovação.

R$ 149 por sete dias é somente uma hipótese comercial. Formato, frequência,
entregáveis e custo aceitável serão decididos depois do `R1A`. Manifestação
espontânea de preço pode ser registrada, mas apenas pagamento real será
evidência comercial.

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
