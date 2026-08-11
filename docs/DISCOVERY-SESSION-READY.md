# DISCOVERY_SESSION_READY

Checklist de uma página para cada sessão presencial do `R1A`.

```text
session_code=
checked_at=

[ ] VERTICAL_SELECTION=COMPLETE.
[ ] Prestador pertence à vertical selecionada.
[ ] Prestador compatível com o ICP.
[ ] Objetivo e limites da sessão explicados.
[ ] Prestador controla fisicamente o aparelho.
[ ] Nenhuma fotografia, gravação ou captura será feita.
[ ] Nenhuma mensagem será copiada.
[ ] Nenhuma conversa será exportada.
[ ] Nenhuma mensagem ou nome real será retido.
[ ] Conversas sensíveis ou incompatíveis serão ignoradas.
[ ] Registro limitado aos campos autorizados.

state=READY | BLOCKED
confidential_reference=
```

Use `READY` somente com todos os itens confirmados. Qualquer dúvida produz
`BLOCKED` e a conversa não é visualizada.

`R1A_READY=COMPLETE` continua significando prontidão documental. A primeira
sessão permanece `FIRST_R1A_SESSION=BLOCKED` enquanto a vertical estiver
pendente ou este checklist concreto não estiver `READY`.

Esta é uma sessão sem custódia, sem cópia e sem retenção das conversas. A
minimização não deve ser descrita como ausência de tratamento de dados. A
revisão jurídica externa permanece `EXTERNAL_LEGAL_REVIEW_NOT_OBTAINED`.

Não criar manifesto, hash, ACL, USB, diretório de dados ou cadeia de custódia
para este fluxo, pois nenhum arquivo será recebido.
