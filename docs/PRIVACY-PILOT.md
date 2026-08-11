# Protocolo operacional de privacidade do piloto

> **Aplicabilidade no pivot:** o `REAL_DATA_READY` abaixo continua válido para
> qualquer piloto futuro que receba arquivos, mas não se aplica ao `R1A` sem
> custódia. Para o discovery atual, use
> [`DISCOVERY-SESSION-READY.md`](DISCOVERY-SESSION-READY.md). Não descreva a
> ausência de cópia ou retenção como ausência de tratamento de dados.

| Campo | Valor |
|---|---|
| Versão | 1.2-draft |
| Escopo | Pilotos manuais e ferramenta local-first com dados reais |
| Revisão | `INTERNAL_APPROVED_AS_DRAFT` — revisão operacional interna |
| Estado jurídico | `EXTERNAL_LEGAL_REVIEW_NOT_OBTAINED` |
| Responsável operacional | Proprietário do Radar de Perdas |

> Este protocolo descreve controles operacionais internos. Não é parecer
> jurídico, não atesta conformidade legal e não substitui a definição, pelo
> cliente, da hipótese legal, das informações aos titulares ou das obrigações
> regulatórias aplicáveis.

## 1. Papéis e premissas

Por padrão, e sujeito à confirmação no instrumento aceito por ambas as partes:

- o cliente é o **controlador** das conversas e decide finalidades, meios
  essenciais, hipótese legal, atendimento aos titulares e comunicações
  regulatórias;
- o proprietário do Radar de Perdas é o **operador** e trata os dados apenas em
  nome do controlador e segundo instruções documentadas;
- qualquer mudança de papel ou finalidade exige nova instrução e atualização do
  instrumento antes do tratamento.

O cliente declara que pode fornecer legitimamente o material, que cumpriu os
deveres de transparência aplicáveis e que as instruções são compatíveis com os
direitos dos titulares. O operador não escolhe a hipótese legal em nome do
cliente.

## 2. Gate composto `REAL_DATA_READY`

Nenhum conteúdo real pode ser recebido, copiado, aberto ou tratado até todos os
itens abaixo estarem comprovados. O gate é indivisível: um item pendente mantém
o estado `BLOCKED`.

- [ ] Instrumento de tratamento de dados aceito pelas duas partes.
- [ ] Papéis de controlador e operador confirmados no instrumento.
- [ ] Finalidade, instruções e legitimidade do fornecimento registradas.
- [ ] Escopo conferido e incompatibilidades excluídas.
- [ ] `PILOT_ID` não identificável criado.
- [ ] Retenção de 30 dias após a entrega registrada.
- [ ] Canal USB criptografado testado apenas com fixture sintética.
- [ ] Diretório local fora de sincronização criado e ACL conferida.
- [ ] BitLocker verificado como `FULLY_ENCRYPTED` e `ON`.
- [ ] Procedimentos de titulares, incidente e descarte conhecidos.
- [ ] Subprocessadores confirmados; por padrão, nenhum recebe dados reais.

Registrar o resultado sem dados pessoais:

```text
gate=REAL_DATA_READY
pilot_id=PILOT-YYYYNN
checked_at=YYYY-MM-DDTHH:MM:SS-03:00
state=COMPLETE | BLOCKED
pending_controls=
operator=
```

`COMPLETE` autoriza apenas o escopo e o período aceitos. Não equivale a aprovação
jurídica externa.

## 3. Escopo e minimização

O tratamento limita-se a conversas individuais necessárias à auditoria de
perdas comerciais e à elaboração do relatório redigido. A finalidade não inclui
treinamento de modelos, publicidade, enriquecimento cadastral, perfilamento,
revenda, reutilização para outro cliente ou desenvolvimento com dados reais.

Ficam fora do piloto:

- dados pessoais sensíveis, inclusive dados de saúde;
- dados de crianças ou adolescentes;
- grupos e arquivos ou conteúdo de anexos, áudio, vídeo e imagens;
- credenciais, dados financeiros e documentos de identidade;
- material sem origem ou autorização confirmada pelo controlador.

Se conteúdo incompatível for identificado, interromper o tratamento, isolar o
arquivo sem abri-lo novamente e solicitar instrução ao controlador. Não copiar o
conteúdo para registrar a ocorrência.

Marcadores textuais de mídia omitida já presentes no TXT podem permanecer. Eles
não autorizam receber ou abrir o conteúdo e são tratados como resposta não
verificável pela metodologia.

## 4. Identificador e diretório

Usar identificador sem nome, CNPJ, telefone ou segmento:

```text
PILOT-YYYYNN
```

Raiz operacional:

```text
C:\Users\catap\RadarDePerdas-Pilotos\<PILOT_ID>\
```

Subdiretórios:

```text
00-contract
10-raw
20-working
30-output
90-disposal
```

Dados reais são proibidos no repositório do projeto e em qualquer diretório
sincronizado. Antes do recebimento, confirmar que somente a conta Windows
autorizada, `SYSTEM` e `Administrators` têm acesso à raiz operacional.

Arquivos devem usar nomes não identificáveis:

```text
<PILOT_ID>_<tipo>_<YYYYMMDD>_<sequencia>.<ext>
```

## 5. Verificação do BitLocker

Antes de criar a raiz operacional, executar em PowerShell administrativo:

```powershell
manage-bde -status C:
```

Não copiar a saída completa. Registrar somente:

```text
verification_date=YYYY-MM-DD
encryption_state=FULLY_ENCRYPTED
protection_state=ON
```

Os valores acima são os estados canônicos internos. Se o comando não puder ser
executado como administrador, se a informação for indeterminada ou se qualquer
estado for diferente, registrar `BLOCKED_ADMIN`, manter `REAL_DATA_READY` como
`BLOCKED` e não receber dados reais.

Nunca registrar, fotografar, copiar ou enviar recovery key, senha, identificador
de protetor ou qualquer material de recuperação.

## 6. Transferência e recebimento

O canal padrão é mídia USB criptografada entregue diretamente. A senha deve ser
transmitida por canal separado da mídia e conhecida apenas pelas partes
autorizadas. Antes do primeiro uso real, testar leitura, integridade e remoção
com fixture exclusivamente sintética.

É proibido transferir conteúdo real por e-mail, mensageiro, formulário público,
Git, serviço de nuvem, ferramenta de IA, clipboard compartilhado ou acesso
remoto por agentes.

No recebimento:

1. confirmar `REAL_DATA_READY=COMPLETE`;
2. copiar diretamente da mídia para `10-raw`;
3. renomear conforme a convenção e calcular SHA-256 localmente;
4. registrar em manifesto local origem, data, responsável e hash;
5. confirmar que grupos, anexos e categorias excluídas não estão presentes;
6. ejetar a mídia e devolver ou eliminar a cópia conforme instrução do
   controlador.

## 7. Regras de acesso e manuseio

Somente o proprietário autorizado pode acessar conteúdo real. Agentes humanos
ou de IA, revisores, fornecedores, jurídico e outros terceiros não recebem
acesso às conversas. Revisões técnicas usam apenas fixtures sintéticas.

É proibido incluir conteúdo real, inclusive trechos, identificadores ou hashes
de arquivos reais, em:

- Git, issues, pull requests, CI ou diretórios do repositório;
- nuvem, backup, sincronização ou aplicação hospedada;
- prompts, modelos, ferramentas ou agentes de IA;
- screenshots, gravações de tela ou demonstrações;
- logs, telemetria, analytics, error tracking ou source maps;
- clipboard compartilhado, e-mail, mensageiro, ticket ou nota em nuvem.

O tratamento ocorre offline. A aplicação local-first pode carregar código
estático protegido, mas não pode transmitir dados, configurações do piloto,
achados ou relatórios. Controles de rede só podem ser testados com fixtures
sintéticas. Relatórios destinados ao cliente devem ser redigidos antes de sair
do ambiente local.

## 8. Titulares e instruções do controlador

O controlador recebe e decide solicitações de titulares. Ao ser instruído, o
operador deve localizar, corrigir, bloquear, exportar ou eliminar os dados sob
seu controle dentro do prazo informado pelo controlador, preservadas obrigações
legais documentadas.

O operador deve:

- manter registro local das operações e instruções, sem reproduzir conversas;
- avisar se uma instrução parecer incompatível com este protocolo;
- suspender o tratamento até receber instrução corrigida quando houver risco;
- não responder ao titular em nome do controlador sem autorização escrita.

## 9. Subprocessadores e fronteira externa

O padrão do piloto manual é **nenhum subprocessador com acesso a dados reais**.
Sistemas operacionais e código estático que não recebem conteúdo não são
autorização para transferência de dados.

Qualquer subprocessador futuro exige, antes do acesso:

1. autorização prévia e escrita do controlador;
2. finalidade, dados, localidade, retenção e segurança documentadas;
3. obrigação contratual equivalente;
4. atualização do instrumento e nova decisão de `REAL_DATA_READY`.

## 10. Retenção e descarte

O prazo padrão para `10-raw`, `20-working` e qualquer saída que ainda contenha
dados pessoais é de **30 dias corridos após a entrega**. Prazo menor prevalece
quando instruído pelo controlador. Ampliação exige instrução documentada e
fundamento registrado antes do vencimento.

Registrar localmente:

```text
delivered_at=
retention_days=30
deletion_due_at=
instruction_reference=
```

Antes da exclusão, resolver o caminho absoluto e confirmar que ele começa
exatamente com `C:\Users\catap\RadarDePerdas-Pilotos\`, termina em um
`PILOT_ID` válido e não contém curinga ou variável não resolvida. Recusar a raiz
do volume, a pasta de usuário, o repositório e a raiz de pilotos sem um
identificador.

Excluir com PowerShell de ponta a ponta e `-LiteralPath`, verificar
`Test-Path=False` e criar recibo não sensível fora da raiz apagada. O recibo
registra apenas `pilotId`, responsável, datas, caminho validado, quantidade de
arquivos, hash do manifesto, confirmação da exclusão e estado de criptografia;
não inclui nomes, conversas, contatos ou hashes individuais.

Em SSD, a evidência é de remoção lógica sobre volume criptografado, não de
apagamento físico comprovado.

## 11. Incidentes

Ao tomar conhecimento de incidente confirmado ou suspeito, o operador deve:

1. conter o evento sem destruir evidências;
2. suspender novos tratamentos;
3. registrar data, circunstâncias, categorias e volume estimado sem copiar
   conversas;
4. informar o controlador **em até 24 horas**, fornecendo as informações
   disponíveis e atualizações relevantes;
5. preservar os registros necessários e apoiar a análise e a mitigação;
6. revogar credenciais ou sessões afetadas e confirmar o estado conhecido da
   criptografia;
7. retomar somente mediante instrução documentada do controlador.

Cabe ao controlador avaliar risco ou dano relevante e decidir as comunicações à
ANPD e aos titulares. Quando aplicável, o Regulamento de Comunicação de
Incidente de Segurança (RCIS) estabelece prazo de três dias úteis, contado do
conhecimento pelo controlador, ressalvado prazo específico. O controlador deve
manter registro dos incidentes, inclusive dos não comunicados, por no mínimo
cinco anos. A obrigação contratual de 24 horas do operador é interna entre as
partes e não altera os prazos regulatórios.

A criptografia é um controle relevante, mas não elimina automaticamente o risco
nem dispensa a avaliação do controlador.

Referências oficiais, consultadas em 10/08/2026:

- [LGPD, arts. 46 a 48](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm);
- [ANPD — Comunicação de Incidente de Segurança e RCIS](https://www.gov.br/anpd/pt-br/canais_atendimento/agente-de-tratamento/comunicado-de-incidente-de-seguranca-cis).

## 12. Registro de revisão interna

```text
document=PRIVACY-PILOT.md
version=1.2-draft
review=INTERNAL_APPROVED_AS_DRAFT | CHANGES_REQUIRED
legal_status=EXTERNAL_LEGAL_REVIEW_NOT_OBTAINED
owner=
reviewed_at=
notes=
```

O preenchimento deste registro comprova apenas revisão operacional interna. Não
deve ser descrito como aprovação jurídica, validação jurídica ou parecer.
