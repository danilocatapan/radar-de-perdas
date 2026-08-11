# Persona do usuário — prestador em campo

| Campo | Valor |
|---|---|
| Versão | 2.0 |
| Status | Hipótese para o `R1A` |
| Evidência externa | `PENDING` |

## Quem estamos tentando compreender

Prestador local ou dono de microempresa que vende pelo WhatsApp, executa os
serviços e não possui vendedor ou recepcionista dedicado. Ele usa o celular no
intervalo entre trabalhos, tem pouco tempo e baixa tolerância a cadastro,
configuração, relatório longo e método abstrato.

Ele não quer manter CRM nem aprender códigos internos. Quer saber rapidamente:

1. qual cliente merece atenção;
2. por que a conversa ainda pode importar;
3. qual é a próxima ação concreta.

## Como revisar material do R1A

Atue como esse prestador, em uma tela estreita e com poucos minutos disponíveis.
Procure primeiro o que está confuso, burocrático, genérico ou exige trabalho
administrativo.

Confirme que:

- a lista possui no máximo cinco itens;
- cada item mostra prioridade, cliente, motivo e próxima ação;
- a ação pode ser entendida sem conhecer a metodologia;
- códigos internos não aparecem na experiência do prestador;
- não existe promessa de integração, automação ou resultado financeiro;
- a apresentação não parece CRM, dashboard ou relatório de auditoria;
- limitações e privacidade são honestas sem dominar a tarefa principal.

## Falhas críticas

- sugerir que existe integração automática com WhatsApp;
- afirmar que oportunidade equivale a venda ou receita recuperada;
- expor nomes, telefones, mensagens ou qualquer dado real no Git;
- obrigar o usuário a cadastrar cliente, manter funil ou classificar códigos;
- apresentar fixture sintética como evidência de mercado;
- esconder a próxima ação ou não explicar o motivo da prioridade.

## Verificação proporcional ao estágio

Antes do primeiro `R1A`, realizar apenas uma conferência interna de que a lista
sintética é legível em largura de celular, possui próxima ação clara e não tem
falha crítica. Registrar:

```text
mobile_readability=PASS | CHANGES_REQUIRED | USER_VISUAL_REVIEW_REQUIRED
next_action_clarity=PASS | CHANGES_REQUIRED
internal_codes_hidden=PASS | CHANGES_REQUIRED
critical_failures=NONE | lista
external_validation=PENDING_R1A
```

Essa verificação não bloqueia o contato com o primeiro prestador por refinamento
estético. A antiga rubrica de dez pontos e nota mínima 9,0 fica `SUPERSEDED` para
o discovery inicial. Revisão visual completa volta a ser obrigatória antes de
material comercial reutilizável ou produto.

## Limite da revisão interna

Uma lista clara e legível não comprova que o problema existe. Somente observar
os prestadores, registrar seus julgamentos e acompanhar suas ações pode produzir
evidência para o gate do `R1A`.
