# Protocolo operacional de privacidade do piloto

| Campo | Valor |
|---|---|
| Versão | 1.1-draft |
| Escopo | Piloto manual e ferramenta local-first com dados reais |
| Status | Não aprovado juridicamente |
| Responsável operacional | Consultor do Radar de Perdas |

> Este protocolo descreve controles operacionais. Não substitui contrato,
> aditivo, parecer jurídico, definição de base legal ou avaliação de incidente.

## 1. Gates anteriores ao recebimento

Nenhum arquivo real pode ser recebido até existirem:

- controlador e operador definidos por escrito;
- finalidade e instruções documentadas;
- responsabilidade pelo fornecimento legítimo;
- período e prazo de retenção;
- procedimento de titulares;
- procedimento de incidente;
- lista de subprocessadores;
- aprovação jurídica registrada fora do repositório;
- `PILOT_ID` sem nome do cliente.

## 2. Identificador

Formato:

```text
PILOT-YYYYNN
```

Exemplo sintético:

```text
PILOT-202601
```

Não incluir nome, CNPJ, telefone ou segmento no identificador.

## 3. Diretório obrigatório

Raiz:

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

Finalidade:

- `00-contract`: referências operacionais ao instrumento, sem copiar documentos
  desnecessários.
- `10-raw`: exportações recebidas, sem alteração.
- `20-working`: cópias e resultados intermediários.
- `30-output`: relatório redigido e entregáveis.
- `90-disposal`: manifesto temporário anterior ao descarte.

Dados reais são proibidos dentro de:

```text
C:\Users\catap\Documents\Radar de Perdas\
```

## 4. Convenção de nomes

```text
<PILOT_ID>_<tipo>_<YYYYMMDD>_<sequencia>.<ext>
```

Tipos permitidos:

- `source`;
- `working`;
- `report`;
- `manifest`.

Exemplo:

```text
PILOT-202601_source_20260803_001.txt
```

Não usar dados identificáveis no nome.

## 5. Verificação de criptografia

Antes de criar o diretório, executar em terminal administrativo:

```powershell
manage-bde -status C:
```

O responsável deve confirmar e registrar:

```text
Conversion Status: Fully Encrypted
Protection Status: Protection On
```

Se a proteção estiver suspensa, desligada ou indeterminada:

1. não criar o diretório;
2. não baixar ou copiar arquivos;
3. corrigir a proteção;
4. repetir a verificação;
5. registrar somente o resultado, sem recovery key.

Nunca registrar ou enviar a chave de recuperação.

## 6. Acesso

- Único usuário autorizado: conta Windows `catap`.
- Não compartilhar sessão do Windows.
- Bloquear a tela ao se afastar.
- Não conceder acesso remoto durante o tratamento.
- Jurídico, cliente e terceiros recebem somente entregáveis adequadamente
  redigidos, salvo procedimento formal diferente.

Antes do piloto, verificar propriedades de segurança do diretório e confirmar
que apenas `catap`, `SYSTEM` e `Administrators` possuem acesso.

## 7. Recebimento

Canal de transferência deve ser definido no instrumento jurídico. O recebimento
não pode ocorrer por:

- WhatsApp;
- e-mail comum;
- clipboard compartilhado;
- repositório Git;
- formulário público;
- ferramenta de IA.

Ao receber:

1. mover o arquivo para `10-raw`;
2. renomear conforme a convenção;
3. calcular SHA-256;
4. registrar origem, data, responsável e hash em manifesto local;
5. confirmar que não existem grupos ou anexos fora do escopo;
6. remover a cópia do local de transferência conforme procedimento aprovado.

## 8. Regras de manuseio

É proibido:

- copiar conteúdo para clipboard fora da ferramenta;
- colar em e-mail, mensageiro, ticket ou nota em nuvem;
- enviar a modelos de IA;
- usar conteúdo em demonstrações;
- capturar telas contendo dados reais;
- incluir trechos em nomes de arquivos ou logs;
- habilitar telemetria que registre conteúdo;
- trabalhar em rede Wi-Fi pública.

Ferramentas manuais e o parser CLI devem operar offline. A ferramenta web
local-first obedece à fronteira de rede definida na seção seguinte.

## 9. Fronteira da ferramenta local-first

A aplicação web poderá ser carregada de um ambiente estático protegido. O
carregamento não autoriza transmitir conteúdo do piloto.

Cloudflare poderá receber somente:

- requisições de ativos estáticos;
- IP e metadados técnicos inerentes ao acesso;
- identidade usada para autenticação no Cloudflare Access.

É proibido transmitir:

- TXT ou anexos;
- mensagens brutas ou normalizadas;
- configuração de horário, SLA ou participantes;
- achados, classificações ou relatório;
- senha ou chave do workspace.

Controles obrigatórios antes da beta:

- `connect-src 'none'` na política de conteúdo;
- scripts, estilos, fontes e Web Workers servidos pela própria aplicação;
- nenhum analytics, telemetria, IA, error tracking ou fonte externa;
- source maps de produção não publicados;
- previews e domínio produtivo protegidos pelo Cloudflare Access;
- lista de usuários permitidos revisada;
- Cloudflare registrado na lista contratual de subprocessadores aplicável;
- teste de rede executado somente com fixtures sintéticas.

O conteúdo permanece em memória durante a sessão. Para persistência, o usuário
exporta um arquivo `.radar` criptografado para `20-working`. Conteúdo do piloto
não pode ser gravado em `localStorage`, IndexedDB ou cache remoto. O arquivo
criptografado segue a mesma retenção de `20-working`.

Fechar a aba encerra o estado não exportado. Perda da senha do `.radar` implica
perda irrecuperável do workspace.

## 10. Sincronização e backup

- A raiz operacional não pode estar dentro de OneDrive, Google Drive, Dropbox ou
  diretório sincronizado.
- Não criar backup de `10-raw` ou `20-working`.
- O cliente é responsável por conservar o original.
- Não usar histórico de arquivos do Windows para esses diretórios.
- O relatório redigido em `30-output` segue o prazo definido no contrato.

## 11. Retenção

Prazo padrão:

- `10-raw` e `20-working`: até 90 dias após a entrega;
- prazo menor prevalece quando definido em contrato ou solicitação válida;
- nenhum prazo pode ser ampliado sem instrução documentada do controlador.

Registrar:

```text
delivered_at:
retention_days:
deletion_due_at:
legal_or_contract_reference:
```

## 12. Preparação do descarte

Antes da exclusão:

1. resolver o caminho absoluto;
2. confirmar que ele começa exatamente com
   `C:\Users\catap\RadarDePerdas-Pilotos\`;
3. confirmar que o último segmento corresponde ao `PILOT_ID`;
4. contar arquivos;
5. calcular SHA-256 de cada arquivo;
6. gerar um hash do manifesto;
7. registrar somente metadados necessários.

O procedimento deve recusar:

- `C:\`;
- `C:\Users\catap`;
- diretório do repositório;
- raiz `RadarDePerdas-Pilotos` sem um `PILOT_ID`;
- caminhos com curingas ou variáveis não resolvidas.

## 13. Exclusão

A exclusão deve ser executada em PowerShell, do início ao fim, usando
`-LiteralPath` e somente após as validações da seção anterior.

Procedimento operacional:

1. fechar todas as ferramentas;
2. excluir a raiz validada do piloto;
3. verificar `Test-Path -LiteralPath <caminho>` igual a `False`;
4. criar recibo fora da raiz apagada.

Destino do recibo:

```text
C:\Users\catap\RadarDePerdas-Receipts\<PILOT_ID>-disposal.json
```

Campos:

```text
pilotId
operator
startedAt
completedAt
validatedAbsolutePath
fileCount
manifestSha256
pathExistsAfterDeletion
encryptionWasVerified
notes
```

O recibo não contém nomes de arquivos, textos, contatos ou hashes individuais.

Em SSD, a evidência é de remoção lógica sobre volume criptografado, não de
apagamento físico comprovado.

## 14. Perda ou roubo

Ao tomar ciência:

1. registrar horário e circunstâncias;
2. informar o controlador em até 24 horas;
3. confirmar estado conhecido do BitLocker;
4. revogar credenciais e sessões acessíveis;
5. preservar logs sem copiar conversas;
6. suspender novos tratamentos;
7. listar categorias e volume possivelmente afetados;
8. solicitar avaliação jurídica sobre ANPD e titulares;
9. documentar contenção, avaliação e retomada.

Não prometer ao cliente que criptografia elimina automaticamente o risco.

## 15. Checklist anterior ao arquivo real

- [ ] Instrumento jurídico aprovado.
- [ ] Papéis LGPD definidos.
- [ ] `PILOT_ID` criado.
- [ ] BitLocker totalmente ativo.
- [ ] Diretório fora de sincronização.
- [ ] Permissões conferidas.
- [ ] Canal de transferência aprovado.
- [ ] Retenção registrada.
- [ ] Procedimento de incidente conhecido.
- [ ] Oferta proíbe escopo incompatível.
- [ ] Subprocessadores e fronteira de rede aprovados antes da beta.

## 16. Aprovação

```text
Responsável operacional:
Responsável jurídico:
Data:
Decisão: APPROVED | CHANGES_REQUIRED
Referência do instrumento:
Observações:
```
