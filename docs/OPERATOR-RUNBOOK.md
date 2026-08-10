# Manual do operador — do R0 ao Decision Gate

| Campo | Valor |
|---|---|
| Versão | 1.2 |
| Responsável | Proprietário do Radar de Perdas |
| Público | Operador que executará os pilotos |
| Dados reais no Git | Proibidos |
| Revisão jurídica externa | `EXTERNAL_LEGAL_REVIEW_NOT_OBTAINED` |

Este manual transforma os gates do projeto em ações executáveis. Ele não é
parecer jurídico e não libera dados por si só. Em caso de divergência, prevalecem
[`GATE-STATUS.md`](GATE-STATUS.md),
[`PRIVACY-PILOT.md`](PRIVACY-PILOT.md) e o instrumento aceito pelas partes.

## 1. Modelo mental e ordem obrigatória

Os nomes são marcos do projeto, não versões do software:

| Marco/gate | Significado | Resultado esperado |
|---|---|---|
| `R0` | Preparar documentos, computador e primeira oportunidade | Prontidão interna; ainda sem dados reais |
| `REAL_DATA_READY` | Conferir os controles de um piloto específico | Autoriza receber somente a amostra e o período aceitos |
| `R1A` | Executar uma auditoria humana preliminar, gratuita | Aprender se o relatório é útil e compreensível |
| `R1A.1` | Consolidar uma vez o que foi observado no `R1A` | Registrar problemas, gargalos, tempo, feedback e mudanças essenciais |
| `R1B` | Executar uma nova auditoria humana, paga por pelo menos R$ 500 | Demonstrar disposição real a pagar |
| `DECISION GATE` | Escolher `GO`, `PIVOT` ou `STOP` | Decidir se existe evidência para avaliar o backlog `R2+` |

Fluxo obrigatório:

```text
BitLocker verificado + oportunidade qualificada
                 |
                 v
             R0 completo
                 |
                 v
convite R1A + aceite do piloto + aceite do instrumento de dados
                 |
                 v
 REAL_DATA_READY completo para o R1A
                 |
                 v
 auditoria manual + relatório + feedback do R1A
                 |
                 v
 consolidação R1A.1 sem desenvolvimento técnico
                 |
                 v
 oferta e pagamento do R1B + novo REAL_DATA_READY
                 |
                 v
 auditoria manual paga + avaliação + pagamento total
                 |
                 v
 DECISION GATE: GO | PIVOT | STOP
                 |
                 v
 R2+ somente se GO e somente para gargalo comprovado
```

O parser, o frontend e a infraestrutura produtiva não fazem parte dessas
etapas. As auditorias `R1A` e `R1B` são serviços manuais. A demonstração
sintética não altera essa ordem nem fornece evidência para os gates.

### 1.1 Demonstração sintética antes do R1A

Para entender o fluxo sem empresa, contrato ou dados reais, execute na raiz do
repositório:

```powershell
python scripts/run_synthetic_demo.py --output-dir artifacts/synthetic-demo
Start-Process .\artifacts\synthetic-demo\index.html
```

Entram cinco TXT sintéticos e anotações humanas pré-revisadas. O script não
interpreta os chats: ele valida o pacote fixo e gera `index.html`, `result.json`
e `findings.csv`. A página mostra um caso de `LP-001`, um de `LP-002`, uma
resposta exatamente no SLA, uma mídia não verificável e um atendimento fora do
escopo.

O ganho demonstrado é transformar uma amostra em indicadores, evidências
revisadas, prioridades e recomendações. Não há estimativa financeira, dado real,
parser ou análise automática. A demonstração não altera nenhum gate e não
substitui o piloto manual `R1A`.

## 2. Antes de começar

É necessário:

- Windows 11 Pro, Enterprise ou Education com uma conta administradora;
- unidade `C:` protegida pelo BitLocker;
- uma mídia USB que possa ser dedicada ao piloto e protegida pelo BitLocker To
  Go;
- uma empresa candidata de baixo risco e um decisor operacional;
- capacidade de trabalhar offline, sem IA, nuvem, sincronização ou acesso de
  terceiros aos dados;
- local seguro, fora do Git, para guardar contratos, registros confidenciais,
  senha e chave de recuperação.

Nunca coloque em prompt, chat com agente, issue, commit ou PR:

- nome da empresa, nome do decisor, telefone ou e-mail;
- conversas, trechos, screenshots ou nomes originais dos arquivos;
- hash de arquivo real, senha do USB ou chave de recuperação;
- caminho que revele identidade do cliente.

## 3. R0, passo 1 — verificar o BitLocker da unidade C:

### 3.1 O que significa “registrar”

Os valores `FULLY_ENCRYPTED` e `ON` não são declarações digitadas por escolha.
Eles são uma normalização do estado observado no Windows. Só registre esses
valores quando o comando administrativo comprovar simultaneamente:

- volume totalmente criptografado;
- percentual de criptografia igual a 100;
- proteção ativa.

### 3.2 Abrir o PowerShell administrativo

1. Abra o menu **Iniciar**.
2. Digite `PowerShell`.
3. Clique com o botão direito em **Windows PowerShell** ou **Terminal**.
4. Escolha **Executar como administrador**.
5. Confirme o aviso do Controle de Conta de Usuário.
6. Verifique que o título da janela contém `Administrador`.

Se não houver a opção ou a senha administrativa não estiver disponível, pare e
mantenha `BLOCKED_ADMIN`.

### 3.3 Executar e interpretar

Execute:

```powershell
manage-bde -status C:
```

Para uma leitura estruturada equivalente, execute também:

```powershell
Get-BitLockerVolume -MountPoint C: |
  Select-Object MountPoint, VolumeStatus, ProtectionStatus, EncryptionPercentage
```

Resultado aprovável no segundo comando:

```text
MountPoint           C:
VolumeStatus         FullyEncrypted
ProtectionStatus     On
EncryptionPercentage 100
```

No `manage-bde`, os rótulos podem aparecer em português ou inglês. Procure o
equivalente a `Conversion Status: Fully Encrypted`, `Percentage Encrypted:
100%` e `Protection Status: Protection On`.

| Resultado observado | Decisão |
|---|---|
| `FullyEncrypted`, `On`, `100` | Pode normalizar e registrar como aprovado |
| `EncryptionInProgress` | Aguardar terminar e executar novamente |
| `FullyDecrypted`, `Off` ou 0% | Ativar o BitLocker antes de continuar |
| `Suspended` ou proteção desativada | Retomar a proteção e verificar novamente |
| `Waiting for Activation` | Ainda não está protegido; concluir a ativação |
| Acesso negado, campo ausente ou estado duvidoso | `BLOCKED_ADMIN`; não inferir aprovação |

Não copie a saída completa, pois ela pode revelar informações sobre os
protetores. Não execute comandos que listem, exportem ou removam protetores para
produzir a evidência do projeto.

### 3.4 Se o BitLocker não estiver ativo

Use a interface do Windows, pois ela conduz a criação e o armazenamento seguro
da chave de recuperação:

1. Entre com uma conta administradora.
2. No Iniciar, procure **Gerenciar BitLocker**.
3. Na unidade do sistema operacional `C:`, escolha **Ativar BitLocker**. Se o
   estado estiver suspenso, escolha **Retomar proteção**.
4. Siga o assistente e guarde a chave de recuperação em local seguro separado
   do computador. Não a guarde no Git, neste projeto, no mesmo USB do piloto ou
   em chat com agente.
5. Em computador já usado, prefira a opção de criptografar a unidade inteira.
6. Conclua a verificação do sistema e reinicie, se solicitado.
7. Aguarde a criptografia chegar a 100% e repita os comandos da seção anterior.

O BitLocker manual está disponível nas edições Pro, Enterprise e Education. Se
**Gerenciar BitLocker** não existir, confirme a edição do Windows antes de
prosseguir.

### 3.5 Evidência mínima permitida

Depois da verificação aprovada, envie ao responsável pelo repositório ou use na
atualização de `GATE-STATUS.md` somente:

```text
verification_date=YYYY-MM-DD
encryption_state=FULLY_ENCRYPTED
protection_state=ON
```

Exemplo de entrada válida, sem copiar a saída do comando:

```text
verification_date=2026-08-10
encryption_state=FULLY_ENCRYPTED
protection_state=ON
```

Se qualquer campo não puder ser confirmado, a entrada correta é:

```text
state=BLOCKED_ADMIN
reason=estado não confirmado
```

## 4. R0, passo 2 — qualificar `OPP-2026-001`

`OPP-2026-001` é um apelido público e não identificável para uma oportunidade.
Ele permite atualizar o Git sem revelar qual empresa está sendo abordada.

### 4.1 O que fazer primeiro

Converse com uma empresa da sua rede sem solicitar conversas ainda. Explique o
piloto gratuito usando
[`PILOT-PRELIMINARY-INVITATION.md`](PILOT-PRELIMINARY-INVITATION.md) e faça a
triagem abaixo.

| Pergunta | Resposta necessária |
|---|---|
| É serviço de baixo risco? | Sim |
| É uma única empresa, unidade e WhatsApp? | Sim |
| Existem entre 20 e 50 chats individuais exportáveis? | Sim |
| A estimativa contém ao menos 10 solicitações comerciais? | Sim |
| O período proposto tem no máximo 30 dias? | Sim |
| Horário, fuso, intervalos, feriados e SLA são conhecidos? | Sim |
| Há decisor operacional disponível para contexto e feedback? | Sim |
| A empresa confirma legitimidade para fornecer as conversas? | Sim |
| Saúde, menores e dados sensíveis estão ausentes? | Sim |
| Grupos e conteúdo de anexos estão excluídos? | Sim |

Uma resposta `não` nas exclusões torna a oportunidade `NOT_QUALIFIED`. Uma
pendência corrigível, como horário ainda não informado, produz
`CHANGES_REQUIRED`. Somente todas as respostas necessárias confirmadas produzem
`QUALIFIED`.

### 4.2 Registro confidencial

Nome e contato ficam em registro local protegido, nunca no Git. Depois de o
BitLocker estar aprovado, use um arquivo local fora de pastas sincronizadas ou
um registro físico seguro com este conteúdo:

```text
opportunity_code=OPP-2026-001
company=[PREENCHER FORA DO GIT]
unit=[PREENCHER FORA DO GIT]
decision_maker=[PREENCHER FORA DO GIT]
contact_channel=[PREENCHER FORA DO GIT]
qualified_at=[TIMESTAMP COM FUSO]
qualified_by=[RESPONSÁVEL]
low_risk_service=YES | NO
single_unit_and_whatsapp=YES | NO
individual_chats_20_to_50=YES | NO
estimated_requests_at_least_10=YES | NO
period_up_to_30_days=YES | NO
schedule_timezone_exceptions_sla_known=YES | NO
operational_decision_maker_available=YES | NO
lawful_supply_declared=YES | NO
no_health_minors_or_sensitive_data=YES | NO
no_groups_or_attachment_content=YES | NO
result=QUALIFIED | CHANGES_REQUIRED | NOT_QUALIFIED
notes=
```

### 4.3 Evidência permitida no Git

Quando o resultado for `QUALIFIED`, registre publicamente apenas:

```text
opportunity_code=OPP-2026-001
qualification_date=YYYY-MM-DD
result=QUALIFIED
evidence_reference=registro confidencial mantido fora do Git
```

Não envie a identidade da empresa ao agente para que ele atualize o gate.

## 5. Preparar um piloto e criar o `PILOT_ID`

Depois de encerrar o `R0` e obter o aceite inicial da empresa, crie um código
sequencial não identificável:

```text
PILOT-YYYYNN
```

Exemplo: `PILOT-202601` identifica o primeiro piloto de 2026, mas não identifica
a empresa. O código é diferente de `OPP-2026-001`: `OPP` acompanha a
oportunidade comercial; `PILOT` acompanha uma execução concreta.

## 6. `REAL_DATA_READY` — como liberar dados reais

`REAL_DATA_READY` é um checklist composto e específico para cada piloto. Um
único item pendente mantém tudo bloqueado. O estado do `R1A` não pode ser
reutilizado automaticamente no `R1B`.

### 6.1 Instrumento de dados aceito

Copie o conteúdo de
[`PILOT-DATA-TERMS-v0.1-draft.md`](PILOT-DATA-TERMS-v0.1-draft.md) para um
documento confidencial fora do Git. Complete e obtenha aceite das duas partes:

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

Os campos identificáveis e as assinaturas permanecem fora do Git. O gate só
passa quando as duas partes aceitaram e todos os três campos de confirmação são
`YES`. Isso é aceite contratual, não aprovação jurídica externa.

### 6.2 Conferir o escopo sem receber arquivos

O cliente deve declarar, antes da transferência:

```text
pilot_id=
single_company_unit_whatsapp=YES | NO
period_start=
period_end=
expected_individual_chats=
expected_commercial_requests=
media_files_excluded=YES | NO
group_chats_excluded=YES | NO
health_data_excluded=YES | NO
minors_excluded=YES | NO
sensitive_financial_identity_data_excluded=YES | NO
business_timezone=
business_hours=
breaks=
holidays_or_closures=
useful_response_sla_minutes=
scope_result=COMPLETE | BLOCKED
```

Não peça exemplos reais para conferir o escopo. A conferência prévia usa a
declaração do controlador. Se o arquivo recebido posteriormente contrariar a
declaração, interrompa o tratamento e isole o arquivo.

### 6.3 Registrar retenção de 30 dias

Antes do recebimento, registre a regra e quem fará a eliminação:

```text
pilot_id=
retention_days=30
retention_starts_at=FINAL_REPORT_DELIVERY
deletion_owner=
planned_delivery_at=
planned_deletion_due_at=
```

Na entrega real do relatório, substitua as datas planejadas pelas datas
efetivas. Para calcular exatamente 30 dias corridos no PowerShell, informe o
timestamp real de entrega:

```powershell
$deliveredAt = [datetimeoffset]'2026-09-04T17:00:00-03:00'
$deletionDueAt = $deliveredAt.AddDays(30)
$deletionDueAt.ToString('o')
```

O resultado esperado para o exemplo é `2026-10-04T17:00:00.0000000-03:00`.
Substitua o timestamp do exemplo pelo real. Guarde o registro fora do Git.

### 6.4 Preparar e testar o USB criptografado

Use uma mídia dedicada. Não use o mesmo USB que guarda a chave de recuperação.

1. Conecte o USB vazio e confirme sua letra no Explorador, por exemplo `E:`.
2. Procure **Gerenciar BitLocker** no Iniciar.
3. Em **Unidades de dados removíveis — BitLocker To Go**, selecione o USB e
   escolha **Ativar BitLocker**.
4. Defina uma senha forte. Não a coloque no repositório, histórico de comando ou
   chat.
5. Guarde a chave de recuperação em local seguro separado do USB e do
   computador.
6. Conclua a criptografia e aguarde 100%.
7. Transmita a senha ao cliente por canal diferente da entrega física do USB,
   preferencialmente em conversa de voz ou presencialmente.

Teste somente com uma fixture sintética do repositório. Ajuste `$usbDrive` para
a letra observada:

```powershell
$usbDrive = 'E:'
$source = Resolve-Path '.\packages\test-fixtures\development\android-multiline-lf.txt'
$testDirectory = Join-Path $usbDrive 'RADAR-USB-TEST'
$testFile = Join-Path $testDirectory 'synthetic-fixture.txt'

New-Item -ItemType Directory -Path $testDirectory -ErrorAction Stop
$sourceHash = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash
Copy-Item -LiteralPath $source -Destination $testFile -ErrorAction Stop
$usbHash = (Get-FileHash -LiteralPath $testFile -Algorithm SHA256).Hash
$sourceHash -eq $usbHash
```

Resultado esperado: `True`. Depois:

1. ejete o USB pelo Windows;
2. reconecte e confirme que ele exige desbloqueio;
3. desbloqueie com a senha;
4. repita o hash e confirme `True`;
5. apague apenas a pasta sintética `RADAR-USB-TEST`;
6. ejete novamente.

Registre fora do Git apenas o código do piloto, data, `hash_match=YES`,
`unlock_test=PASS` e `synthetic_test_removed=YES`. Não registre senha, chave de
recuperação, número de série da mídia ou hash de arquivo real.

### 6.5 Criar o diretório operacional e restringir a ACL

Execute em PowerShell administrativo. Substitua somente o valor de `$pilotId`:

```powershell
$pilotId = 'PILOT-202601'
$pilotsBase = 'C:\Users\catap\RadarDePerdas-Pilotos'

if ($pilotId -notmatch '^PILOT-\d{6}$') {
  throw 'PILOT_ID inválido.'
}

$pilotRoot = Join-Path $pilotsBase $pilotId
if (Test-Path -LiteralPath $pilotRoot) {
  throw 'O diretório do piloto já existe; não sobrescreva.'
}

New-Item -ItemType Directory -Path $pilotRoot -ErrorAction Stop | Out-Null

$currentSid = ([System.Security.Principal.WindowsIdentity]::GetCurrent()).User.Value
$currentTrustee = "*$currentSid"

& icacls.exe $pilotRoot /inheritancelevel:r
if ($LASTEXITCODE -ne 0) { throw 'Falha ao remover herança da ACL.' }

& icacls.exe $pilotRoot /grant:r `
  "${currentTrustee}:(OI)(CI)F" `
  '*S-1-5-18:(OI)(CI)F' `
  '*S-1-5-32-544:(OI)(CI)F'
if ($LASTEXITCODE -ne 0) { throw 'Falha ao definir a ACL.' }

'00-contract','10-raw','20-working','30-output','90-disposal' |
  ForEach-Object {
    New-Item -ItemType Directory -Path (Join-Path $pilotRoot $_) -ErrorAction Stop
  } | Out-Null
```

Os SIDs representam a conta atual, `SYSTEM` e o grupo local de administradores,
sem depender do idioma do Windows. `(OI)(CI)F` concede controle total ao
diretório, aos arquivos e aos subdiretórios.

Verifique:

```powershell
icacls.exe $pilotRoot

(Get-Acl -LiteralPath $pilotRoot).Access |
  Select-Object IdentityReference, FileSystemRights, IsInherited
```

Resultado esperado:

- somente a conta Windows autorizada, `SYSTEM` e `Administrators` possuem
  acesso;
- `IsInherited` aparece como `False`;
- os cinco subdiretórios existem;
- o caminho não está dentro de OneDrive, Dropbox, Google Drive, Git ou outra
  pasta sincronizada.

Se aparecer outra conta ou grupo, não copie dados. Corrija a ACL e verifique
novamente. Não publique o caminho privado ou a saída da ACL no Git.

### 6.6 Decisão composta

Complete fora do Git:

```text
gate=REAL_DATA_READY
pilot_id=PILOT-YYYYNN
checked_at=YYYY-MM-DDTHH:MM:SS-03:00
data_terms_accepted=COMPLETE | BLOCKED
scope_checked=COMPLETE | BLOCKED
retention_registered=COMPLETE | BLOCKED
encrypted_usb_tested=COMPLETE | BLOCKED
directory_acl_approved=COMPLETE | BLOCKED
bitlocker_active=COMPLETE | BLOCKED
incident_and_disposal_procedures_known=COMPLETE | BLOCKED
subprocessors_with_real_data=NONE | BLOCKED
state=COMPLETE | BLOCKED
pending_controls=
operator=
```

`state=COMPLETE` somente quando todos os componentes estão completos e não há
pendência. Em qualquer outro caso, use `BLOCKED` e não receba dados.

## 7. Executar o `R1A` gratuito

`R1A` significa “primeiro piloto de aprendizagem”. Não é software e não é uma
demonstração automatizada. Você presta manualmente o serviço descrito no
convite, sem cobrar, para descobrir se o resultado é útil e compreensível.

### 7.1 Entradas necessárias

Somente após `REAL_DATA_READY=COMPLETE`, receba:

- 20 a 50 exportações `.txt` de chats individuais, sem mídia;
- período de análise com início inclusivo e fim exclusivo;
- data/hora declarada da exportação; se ausente, registre o recebimento como
  `evaluation_at`;
- fuso, horário semanal, intervalos, feriados e fechamentos;
- SLA em minutos úteis;
- identificação local de atendentes e do decisor, mantida fora do Git;
- explicações necessárias para excluir suporte, pós-venda e contatos que não
  sejam prospects.

O cliente não envia anexos. Marcadores textuais como “áudio omitido” podem
existir no TXT, mas o conteúdo não é solicitado nem analisado.

### 7.2 Recebimento

1. Confirme novamente `REAL_DATA_READY=COMPLETE`.
2. Receba fisicamente o USB e desbloqueie localmente.
3. Copie diretamente para `10-raw`.
4. Renomeie com `PILOT_ID`, tipo, data e sequência, sem nomes reais.
5. Calcule SHA-256 local e registre em manifesto dentro de `00-contract` ou
   `20-working`; nunca publique o hash.
6. Confirme quantidade, formato `.txt` e ausência das categorias excluídas.
7. Ejete e proteja ou devolva o USB conforme o instrumento aceito.

Exemplo local de hash para um arquivo já renomeado:

```powershell
Get-FileHash -LiteralPath 'C:\Users\catap\RadarDePerdas-Pilotos\PILOT-202601\10-raw\PILOT-202601_chat_20260820_001.txt' -Algorithm SHA256
```

A saída desse comando é confidencial e permanece somente no manifesto local.

### 7.3 Auditoria humana

Trabalhe offline e sem agentes de IA:

1. Inicie o registro de tempo copiando o cabeçalho de
   [`PILOT-TIME-LOG.csv`](PILOT-TIME-LOG.csv) para um CSV local em `20-working`.
2. Registre `PREPARATION` e `CONFIGURATION`.
3. Leia cada chat e identifique blocos de solicitações comerciais do prospect.
4. Para cada solicitação, determine a primeira resposta humana útil segundo
   [`AUDIT-METHOD-v0.1.md`](AUDIT-METHOD-v0.1.md).
5. Marque `LP-001` quando a resposta útil exceder o SLA em tempo de expediente.
6. Marque `LP-002` somente quando o ciclo encerrar sem resposta humana útil e
   não houver resposta de mídia não verificável pendente.
7. Trate marcador de mídia como `UNVERIFIABLE_RESPONSE`; não abra nem transcreva
   o conteúdo e não gere `LP-002` automaticamente.
8. Faça revisão humana de todos os achados e denominadores.
9. Redija exemplos mínimos, removendo nomes, telefones, e-mails e contexto
   desnecessário.
10. Preencha uma cópia local de
    [`PILOT-REPORT-TEMPLATE.md`](PILOT-REPORT-TEMPLATE.md).

O relatório deve informar amostra, exclusões, período, corte, configuração,
numeradores, denominadores, achados confirmados, limitações, prioridades e
recomendações. Não estime receita perdida.

### 7.4 Entrega e feedback

1. Entregue relatório redigido em até sete dias úteis após todos os insumos
   válidos.
2. Peça que o decisor leia o relatório antes da apresentação.
3. Antes de explicar as respostas, obtenha nota de utilidade de 1 a 5 e aplique
   as cinco perguntas de compreensão de
   [`PILOT-BASELINE.md`](PILOT-BASELINE.md).
4. Some somente o esforço ativo de esclarecimento; espera passiva não conta.
5. Faça a apresentação de até 60 minutos.
6. Receba uma rodada consolidada de correções factuais.
7. Registre a data efetiva de entrega e calcule o descarte em 30 dias.

O `R1A` atinge suas metas quando:

- utilidade é pelo menos 4/5;
- pelo menos quatro de cinco respostas de compreensão estão corretas;
- esclarecimento ativo é no máximo 900 segundos;
- relatório, apresentação, feedback e limitações estão registrados.

Resultado baixo ou inconclusivo não deve ser convertido em aprovação nem gerar
nova amostra gratuita automática. Ele segue para a consolidação única `R1A.1`.
No `R1A`, não pergunte faixa de preço nem declare disposição a pagar validada.

### 7.5 Consolidar o `R1A.1`

Depois da entrega e do feedback de `R1A`, registre fora do Git os detalhes
confidenciais e compartilhe com o repositório somente uma síntese não sensível:

```text
problemas_reais=
gargalos_observados=
tempo_ativo_por_etapa=
feedback_agregado=
mudancas_essenciais_para_R1B=
pendencias_de_produto_arquitetura_seguranca_ou_escopo=
```

Não implemente as pendências. `R1A.1` permite somente ajustes essenciais ao
serviço manual, à oferta, à metodologia ou à operação segura necessários para
executar `R1B`. Parser, frontend, infraestrutura, banco, IA, novos LPs e
refinamentos estruturais continuam bloqueados.

## 8. Executar o `R1B` pago de R$ 500

`R1B` é o primeiro teste comercial. O trabalho continua sendo uma auditoria
manual, mas agora uma empresa aceita a oferta e paga pelo menos R$ 500. O
pagamento real é a evidência que o piloto gratuito não consegue fornecer.

Passos:

1. Concluir e aprender com o `R1A`.
2. Selecionar uma empresa qualificada; pode ser a mesma, desde que exista novo
   escopo, aceite e decisão de dados.
3. Emitir a [`PILOT-OFFER.md`](PILOT-OFFER.md) fora do Git com identificação,
   datas e condições fiscais reais.
4. Obter aceite comercial e a primeira parcela prevista.
5. Revalidar todo o `REAL_DATA_READY` para o novo período e amostra. Não copiar
   automaticamente o estado do `R1A`.
6. Receber até 50 chats e repetir a auditoria humana.
7. Registrar integralmente o baseline de tempo em modo `MANUAL`.
8. Entregar relatório, apresentação e correções factuais.
9. Receber o saldo e comprovar pagamento total de pelo menos R$ 500 fora do Git.
10. Reaplicar utilidade, compreensão e esclarecimento.

O `R1B` só completa quando o pagamento total e as metas operacionais estiverem
comprovados. “Gostei”, intenção de compra ou aceite sem pagamento não completam
o gate. O término da tentativa comercial leva ao `DECISION GATE`; `R1B` não
libera `R2+` automaticamente.

### 8.1 Aplicar o `DECISION GATE`

Registre exatamente uma decisão, com referência apenas a evidências agregadas:

- `GO`: pagamento total de pelo menos R$ 500, utilidade aprovada, operação
  manual viável e gargalo repetitivo observado que justifique automação;
- `PIVOT`: valor percebido com problema relevante de preço, segmento,
  `LP-001`/`LP-002`, formato, obtenção dos dados ou custo operacional;
- `STOP`: ausência de disposição real a pagar ou custo operacional que torne a
  oferta economicamente inviável.

Uma tentativa sem pagamento completo pode resultar em `PIVOT` ou `STOP`, nunca
em `GO`. Somente `GO` permite avaliar o menor item de `R2+` necessário para um
gargalo comprovado; não autoriza automaticamente todo o backlog.

## 9. Descarte após a entrega

Na data de eliminação, feche os aplicativos que usam o piloto e valide o alvo
antes de qualquer remoção. Exemplo para `PILOT-202601`:

```powershell
$pilotId = 'PILOT-202601'
$pilotsBase = 'C:\Users\catap\RadarDePerdas-Pilotos'

if ($pilotId -notmatch '^PILOT-\d{6}$') {
  throw 'PILOT_ID inválido.'
}

$pilotRoot = [System.IO.Path]::GetFullPath((Join-Path $pilotsBase $pilotId))
$expectedRoot = [System.IO.Path]::GetFullPath("C:\Users\catap\RadarDePerdas-Pilotos\$pilotId")

if ($pilotRoot -ne $expectedRoot) {
  throw 'Caminho divergente; exclusão recusada.'
}
if (-not (Test-Path -LiteralPath $pilotRoot -PathType Container)) {
  throw 'Diretório do piloto não encontrado.'
}

$pilotRoot
(Get-ChildItem -LiteralPath $pilotRoot -Recurse -Force | Measure-Object).Count
```

Confira visualmente que o caminho termina exatamente no `PILOT_ID` pretendido.
Não prossiga se aparecer a raiz do volume, a pasta do usuário, a raiz geral de
pilotos ou qualquer caminho inesperado. Depois de gerar e guardar fora da pasta
o recibo não sensível previsto no protocolo:

```powershell
Remove-Item -LiteralPath $pilotRoot -Recurse -Force -ErrorAction Stop
Test-Path -LiteralPath $pilotRoot
```

Resultado esperado do último comando: `False`. Em SSD criptografado, isso
comprova remoção lógica, não destruição física pericial.

## 10. O que atualizar no Git

O Git contém apenas estados agregados e evidências não sensíveis. Após cada
passo, forneça ao responsável pelo repositório somente os campos permitidos:

| Evento | Pode informar | Não pode informar |
|---|---|---|
| BitLocker | Data, `FULLY_ENCRYPTED`, `ON` | Saída bruta, protetores, recovery key |
| Oportunidade | Código, data, `QUALIFIED` | Empresa, decisor, contato |
| Aceite | Código, data e referência externa genérica | Contrato assinado, nomes, assinaturas |
| USB | Data e `PASS` de teste sintético | Senha, chave, serial, hash real |
| ACL | Data e `COMPLETE` | Caminho privado e identidades |
| Piloto | Código, modalidade e estados agregados | Conversas, trechos, hashes e relatório identificável |

Um pedido seguro de atualização pode ter este formato:

```text
Atualize os gates com evidência não sensível:
bitlocker_checked_at=YYYY-MM-DD
encryption_state=FULLY_ENCRYPTED
protection_state=ON
opportunity_code=OPP-2026-001
opportunity_result=QUALIFIED
qualification_date=YYYY-MM-DD
```

Antes de enviar, confirme que não há nome, telefone, e-mail, conversa, senha,
chave ou hash real no texto.

## 11. Referências oficiais do Windows

- [Microsoft Learn — `manage-bde -status`](https://learn.microsoft.com/windows-server/administration/windows-commands/manage-bde-status)
- [Microsoft Learn — operações do BitLocker](https://learn.microsoft.com/windows/security/operating-system-security/data-protection/bitlocker/operations-guide)
- [Microsoft Support — criptografia de unidade BitLocker](https://support.microsoft.com/windows/security/encryption/bitlocker-drive-encryption)
- [Microsoft Learn — `icacls`](https://learn.microsoft.com/windows-server/administration/windows-commands/icacls)
