# Instrumento de tratamento de dados do piloto — v0.1-draft

| Campo | Valor |
|---|---|
| Versão | 0.1-draft |
| Revisão | `INTERNAL_APPROVED_AS_DRAFT` — revisão operacional interna |
| Estado jurídico | `EXTERNAL_LEGAL_REVIEW_NOT_OBTAINED` |
| Uso | Minuta genérica para aceite externo antes de dados reais |

> **Minuta sem revisão jurídica externa.** Este documento não é parecer
> jurídico, não atesta conformidade com a LGPD e deve ser conferido e completado
> pelas partes antes do aceite. Nenhum dado real pode ser recebido enquanto o
> instrumento não estiver aceito e o gate `REAL_DATA_READY` não estiver
> integralmente liberado.

## 1. Partes e papéis

Para o piloto identificado somente pelo código `[PILOT_ID]`:

- **Cliente:** `[IDENTIFICAÇÃO FORA DO GIT]`, denominado **Controlador**;
- **Proprietário do Radar de Perdas:** `[IDENTIFICAÇÃO FORA DO GIT]`, denominado
  **Operador**.

Os papéis acima são a configuração padrão e dependem de confirmação expressa
das partes. O Controlador toma as decisões referentes ao tratamento; o Operador
trata os dados em nome do Controlador e conforme suas instruções documentadas.
Se a realidade do tratamento exigir papéis diferentes, as partes devem alterar
este instrumento antes de qualquer transferência.

## 2. Finalidade e instruções

O Operador poderá tratar somente as conversas individuais selecionadas pelo
Controlador para:

1. realizar auditoria de perdas comerciais do piloto;
2. classificar os casos segundo a metodologia acordada;
3. elaborar relatório redigido, prioridades e apresentação ao Controlador;
4. executar segurança, controle de qualidade e descarte vinculados ao piloto.

O Operador não poderá usar os dados para publicidade, enriquecimento cadastral,
perfilamento, revenda, outro cliente, treinamento de modelos de IA ou evolução
do produto. Nova finalidade ou instrução exige registro escrito e, quando
necessário, novo aceite.

## 3. Legitimidade do fornecimento e titulares

O Controlador declara e se responsabiliza por:

- possuir hipótese legal e autoridade para fornecer os dados e instruir o
  tratamento;
- cumprir os deveres de transparência e demais obrigações perante os titulares;
- enviar apenas o mínimo necessário e verificar o escopo antes da entrega;
- receber, avaliar e responder solicitações de titulares e autoridades;
- informar ao Operador instruções de acesso, correção, bloqueio, portabilidade
  ou eliminação aplicáveis aos dados sob tratamento.

O Operador apoiará o Controlador conforme instrução documentada, não responderá
diretamente ao titular sem autorização e avisará se identificar instrução
incompatível com este instrumento.

## 4. Dados permitidos e exclusões

O escopo permitido limita-se a 20–50 conversas individuais de uma unidade ou
número de WhatsApp, estritamente necessárias ao piloto.

Não podem ser fornecidos:

- dados pessoais sensíveis, inclusive dados de saúde;
- dados de crianças ou adolescentes;
- grupos e arquivos ou conteúdo de anexos, imagens, áudio ou vídeo;
- credenciais, documentos de identidade ou dados financeiros;
- conteúdo alheio à finalidade ou sem legitimidade confirmada.

Ao identificar material incompatível, o Operador suspenderá o tratamento,
isolará o arquivo e solicitará instrução ao Controlador sem reproduzir o
conteúdo em registros.

Marcadores textuais de mídia omitida no TXT não autorizam acesso ao conteúdo.
Eles são tratados somente como resposta não verificável, conforme a metodologia.

## 5. Segurança, transferência e acesso

A transferência padrão ocorrerá por mídia USB criptografada entregue
diretamente. A senha será transmitida por canal separado e apenas a pessoas
autorizadas. Integridade, leitura e descarte serão testados previamente com
fixture sintética.

Os dados serão tratados offline, em diretório local fora de sincronização, com
ACL restrita e em volume cuja criptografia BitLocker tenha os estados internos
`FULLY_ENCRYPTED` e `ON` comprovados.

É proibido colocar conteúdo real em Git, serviços de nuvem, ferramentas ou
agentes de IA, screenshots, gravações, logs, telemetria, clipboard compartilhado,
e-mail, mensageiro, tickets, demonstrações ou acesso remoto de terceiros.
Revisores e agentes técnicos usarão exclusivamente fixtures sintéticas.

## 6. Subprocessadores

Nenhum subprocessador está autorizado a acessar dados reais nesta versão. A
contratação futura exige autorização prévia e escrita do Controlador, descrição
de finalidade, dados, localidade, retenção e segurança, obrigação contratual
equivalente e nova verificação do gate `REAL_DATA_READY`.

## 7. Incidentes

O Operador adotará medidas de contenção, preservará os registros necessários e
informará o Controlador sobre incidente confirmado ou suspeito **em até 24
horas** de sua ciência, com as informações disponíveis e atualizações
posteriores. O Operador apoiará investigação, mitigação e comunicações, sem agir
em nome do Controlador salvo instrução escrita.

Cabe ao Controlador avaliar se o incidente pode acarretar risco ou dano
relevante e decidir as comunicações à ANPD e aos titulares. Quando aplicável, o
RCIS prevê prazo de três dias úteis contado do conhecimento pelo Controlador,
ressalvada legislação específica. O Controlador manterá registro de incidentes,
inclusive dos não comunicados, por no mínimo cinco anos.

Essas disposições operacionais tomam como referência os [arts. 46 a 48 da
LGPD](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm)
e as [orientações da ANPD sobre o
RCIS](https://www.gov.br/anpd/pt-br/canais_atendimento/agente-de-tratamento/comunicado-de-incidente-de-seguranca-cis).
Elas não substituem avaliação jurídica do caso concreto.

## 8. Retenção, término e descarte

Dados brutos, cópias de trabalho e saídas que contenham dados pessoais serão
eliminados em até **30 dias corridos após a entrega**. Prazo menor instruído pelo
Controlador prevalece. Qualquer ampliação exige instrução escrita e fundamento
registrado antes do vencimento.

O Operador realizará exclusão lógica do diretório validado em volume
criptografado, verificará a inexistência do caminho e emitirá recibo sem dados
pessoais. O recibo poderá conter código do piloto, datas, quantidade de arquivos,
hash do manifesto, confirmação da exclusão e estado da criptografia, mas não
nomes, contatos, conversas, nomes de arquivos ou hashes individuais.

Ao término, o Operador não conservará cópias, salvo obrigação legal documentada
e comunicada ao Controlador. O Controlador é responsável por conservar os
originais que devam permanecer sob seu controle.

## 9. Condições anteriores ao recebimento

O aceite deste instrumento é necessário, mas não suficiente. A transferência
somente poderá ocorrer após confirmação de todos os controles do
`REAL_DATA_READY` descritos no [protocolo operacional de
privacidade](PRIVACY-PILOT.md), incluindo escopo, retenção, canal, diretório,
ACL e BitLocker.

Se qualquer controle estiver ausente, indeterminado ou vencido, o estado será
`BLOCKED` e o Operador recusará os dados.

## 10. Aceite

Preencher e assinar fora do repositório. Não inserir nomes, contatos, documentos
ou assinaturas reais no Git.

```text
pilot_id:
controller_legal_name:
controller_representative:
controller_contact:
operator_legal_name:
purpose_confirmed: YES | NO
roles_confirmed: YES | NO
lawful_supply_confirmed: YES | NO
retention_days: 30
accepted_at:
controller_acceptance:
operator_acceptance:
notes:
```

O aceite não deve ser descrito como aprovação jurídica. Até que eventual revisão
externa seja obtida e registrada fora do Git, permanece:

```text
legal_status=EXTERNAL_LEGAL_REVIEW_NOT_OBTAINED
```
