# Radar de Perdas

| Campo | Valor |
|---|---|
| Versão | 0.6 |
| Status | `R1A_READY`; Discovery Concierge ainda não executado |
| Próximo resultado | `R1A_READY` |

O Radar de Perdas está validando uma ideia simples para prestadores de serviço
locais: encontrar, nas conversas que eles já mantêm no WhatsApp, clientes que
ainda precisam de uma ação para o serviço não ficar pelo caminho.

> Continue usando seu WhatsApp normalmente. O Radar mostra quais clientes
> precisam de uma ação sua para o serviço não ficar pelo caminho.

## Para quem

O primeiro público é o prestador ou a microempresa de serviços que:

- vende principalmente pelo WhatsApp Business;
- passa boa parte do dia executando serviços em campo;
- trabalha em equipe de uma a cinco pessoas, sem vendedor dedicado;
- não usa CRM ou não consegue manter um funil atualizado;
- precisa resolver as pendências em poucos minutos pelo celular.

Eletricistas, encanadores, instaladores de ar-condicionado, assistência técnica
e manutenção residencial são segmentos prioritários. Oficina pequena permanece
como segmento secundário.

## Hipótese atual

O trabalho a validar é: **“me diga quais clientes ainda podem virar serviço e
qual é a próxima coisa que preciso fazer.”**

O primeiro discovery observará quatro situações:

| Situação apresentada ao prestador | Código interno | Exemplo de próxima ação |
|---|---|---|
| Precisa responder | `NEEDS_RESPONSE` | Responder o pedido |
| Precisa orçar | `NEEDS_QUOTE` | Enviar o orçamento prometido |
| Follow-up pendente | `FOLLOWUP_DUE` | Retomar a proposta |
| Retorno prometido | `PROMISED_RETURN_DUE` | Cumprir o retorno combinado |

Padrões diferentes podem ser anotados como `OUT_OF_SCOPE_CANDIDATE`. Isso gera
aprendizado, não uma nova feature ou ampliação automática do produto.

## Próximo experimento: R1A

O `R1A` é um Discovery Concierge com cinco prestadores. Em cada sessão:

1. o prestador mantém o próprio aparelho sob controle;
2. a revisão presencial dura de 20 a 30 minutos;
3. não há fotografia, gravação, cópia ou exportação de conversas;
4. o prestador confirma se a oportunidade importa, se a havia esquecido e qual
   ação faz sentido;
5. contatos curtos nos dias 4 e 7 registram ações e desfechos, sem nova revisão
   completa do WhatsApp.

O procedimento completo está em [`docs/R1A-DISCOVERY.md`](docs/R1A-DISCOVERY.md)
e o checklist de início em
[`docs/DISCOVERY-SESSION-READY.md`](docs/DISCOVERY-SESSION-READY.md).

O teste pago só poderá ser preparado se todos os critérios por prestador forem
atingidos: problema em pelo menos 4 de 5; oportunidade relevante esquecida,
ação executada e interesse recorrente em pelo menos 3 de 5.

## O que não está sendo construído

Não há produto, integração com WhatsApp, parser, IA, frontend, backend, banco,
notificação, automação, arquitetura definitiva ou infraestrutura produtiva em
desenvolvimento. A hipótese de um acompanhamento pago de R$ 149 por sete dias
continua apenas como hipótese e será revista depois do `R1A`.

A antiga auditoria de `LP-001`/`LP-002`, seu relatório longo e sua oferta de
R$ 500 foram substituídos como direção de produto. Os materiais continuam no
repositório como histórico e os detectores podem servir como evidência auxiliar.

## Representação sintética mínima

A [`lista sintética`](docs/R1A-SYNTHETIC-LIST.md) ilustra somente o formato que
será mostrado no discovery: no máximo cinco clientes, cada um com prioridade,
motivo e próxima ação. Ela não é produto, demo comercial refinada ou evidência
de mercado.

## Validação documental

```powershell
python -m unittest discover -s tests -v
python scripts/validate_repository.py --report artifacts/quality/report.json
```

Essas verificações cobrem fixtures sintéticas, contabilidade de linhas, CSVs,
links locais, privacidade, segredos e integridade do diff. Testes verdes não
validam o problema nem substituem as cinco conversas com prestadores.

## Dados e privacidade

Dados reais nunca entram neste Git. No `R1A`, a sessão é sem custódia, sem
cópia e sem retenção das conversas, mas isso não deve ser descrito como ausência
de tratamento de dados. Nomes, telefones, mensagens, mídias e informações
sensíveis não são registrados. A revisão jurídica externa não foi obtida.

Consulte [`docs/GATE-STATUS.md`](docs/GATE-STATUS.md) para os bloqueios vigentes
e [`docs/R0-DECISION-LOG.md`](docs/R0-DECISION-LOG.md) para o histórico.
