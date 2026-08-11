# Produto — Radar de Perdas

| Campo | Valor |
|---|---|
| Versão | 0.5 |
| Status | `PRODUCT_PIVOT`; hipótese sem validação externa |
| Responsável pela decisão | Proprietário do Radar de Perdas |

## Direção atual

O Radar de Perdas pretende ajudar prestadores locais a identificar oportunidades
comerciais paradas no WhatsApp e decidir a próxima ação, sem exigir CRM, cadastro
duplicado ou manutenção manual de funil.

Esta direção é uma hipótese. Nenhum contato real foi registrado como evidência
deste pivot e nenhuma capacidade técnica está autorizada.

## Trabalho a ser validado

> Me diga quais clientes ainda podem virar serviço e qual é a próxima coisa que
> preciso fazer.

O usuário continua trabalhando e conversando normalmente. A experiência
pretendida é uma lista curta, mobile-first, que explique por que cada cliente
merece atenção e qual ação deve ser tomada.

## Usuário inicial

Prestador local ou microempresa de uma a cinco pessoas, sem vendedor dedicado,
que vende serviços principalmente pelo WhatsApp Business e passa grande parte
do dia em campo.

Os cinco participantes do `R1A` devem pertencer à mesma vertical. A vertical
concreta não está decidida: `VERTICAL_SELECTION=PENDING_OWNER_SELECTION`. A
seleção cabe ao proprietário e prioriza capacidade real de recrutamento pela
rede pessoal, indicações, bairro e cidade.

## Entrada no mercado

A aquisição inicial é direta e relacional: amigos e conhecidos compatíveis com
o ICP, indicações e prestadores do bairro e da cidade, sem mídia paga nesta
fase. O Radar pretende ganhar aprendizado e clientes pela simplicidade,
proximidade, baixo atrito e utilidade concreta para um nicho pequeno.

Essa escolha não significa confronto competitivo, substituição de CRM ou busca
de paridade funcional. A frase “há clientes para todo mundo” não constitui
evidência de mercado e não será usada como tal.

## Estados do primeiro discovery

- `NEEDS_RESPONSE`: solicitação comercial relevante sem resposta útil.
- `NEEDS_QUOTE`: orçamento ou preço prometido ainda não enviado.
- `FOLLOWUP_DUE`: proposta enviada com oportunidade razoável de retomada.
- `PROMISED_RETURN_DUE`: retorno, confirmação ou verificação prometida e não
  cumprida.
- `OUT_OF_SCOPE_CANDIDATE`: padrão observado fora dos quatro estados; serve
  somente para aprendizagem e decisão futura.

## Princípios

- Zero trabalho administrativo sempre que possível.
- Nenhum cadastro duplicado ou funil para o usuário manter.
- Lista curta, motivo explícito e próxima ação clara.
- Uso pensado primeiro para celular e inferior a dois minutos por dia.
- Códigos internos não aparecem como linguagem principal para o prestador.
- Privacidade e operação ficam predominantemente sob responsabilidade do Radar.

## Não objetivos

CRM, caixa de entrada, chatbot, helpdesk, ERP, financeiro, agenda completa,
campanhas, analytics complexo, automação de mensagens e substituição do
WhatsApp não pertencem ao escopo.

## Situação da direção anterior

A auditoria de `LP-001` e `LP-002`, o relatório retrospectivo e a oferta de
R$ 500 estão `SUPERSEDED` como proposta principal. As definições continuam
preservadas historicamente e podem fornecer detectores ou evidências auxiliares,
sem representar venda ou receita perdida.

A versão 0.3 deste documento descrevia uma ferramenta interna local-first e
metas de parser. Essas escolhas não são arquitetura vigente e permanecem
bloqueadas até evidência real e uma decisão posterior.

## Hipótese comercial posterior

`MONTHLY_PRICE=R$49.90` está `HYPOTHESIS_ONLY`. Não é preço validado,
recomendação de mercado ou comprovação de sustentabilidade econômica. A
hipótese anterior de R$ 149 por sete dias está `SUPERSEDED`; a oferta histórica
de auditoria por R$ 500 continua preservada como `SUPERSEDED`.

Um eventual R1B prevê período gratuito de até 30 dias, sem cartão obrigatório
ou cobrança automática, seguido de oferta explícita de continuidade. Somente
pagamento efetivamente recebido constitui evidência comercial.

## Próxima decisão

O único trabalho externo autorizado é selecionar a vertical e executar o `R1A`
definido em [`R1A-DISCOVERY.md`](R1A-DISCOVERY.md). O protocolo posterior está
em [`R1B-COMMERCIAL-EXPERIMENT.md`](R1B-COMMERCIAL-EXPERIMENT.md), com estado
`BLOCKED_UNTIL_R1A_PASS` e nova autorização do proprietário obrigatória. Nenhum
resultado autoriza desenvolvimento automático do produto.
