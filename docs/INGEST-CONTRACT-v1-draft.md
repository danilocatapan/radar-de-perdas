# Contrato de ingestão v1 — rascunho

| Campo | Valor |
|---|---|
| Versão do documento | 1.0-draft |
| Schema pretendido | `radar.ingest/v1` |
| Status | Hipóteses sintéticas; não implementar ainda |
| Responsáveis por aprovação | Consultor e desenvolvedor |

> Este rascunho organiza formatos conhecidos e fixtures sintéticas. O contrato
> final só poderá ser criado após a revisão do corpus real autorizado.

## 1. Interface pretendida

```text
radar ingest <arquivo.txt> \
  --timezone America/Sao_Paulo \
  --config <config.json> \
  --output <resultado.json>
```

Códigos de saída:

- `0`: arquivo compatível, sem erros de parsing.
- `2`: formato incompatível.
- `3`: erro ou ambiguidade de parsing.
- `4`: configuração inválida.

O CLI não acessará rede.

## 2. Escopo preliminar

### Suportado

- Exatamente um TXT.
- Chat individual.
- UTF-8 válido com ou sem BOM.
- LF ou CRLF.
- Marcas direcionais Unicode conhecidas ao redor de timestamp.
- Datas `DD/MM/AA` ou `DD/MM/AAAA`.
- Relógio de 24 horas.
- Segundos presentes ou ausentes.
- Mensagens multilinha.
- Eventos conhecidos representados explicitamente.

### Rejeitado

- Chat em grupo.
- ZIP, CSV ou múltiplos TXT.
- Conteúdo de anexos.
- Encoding diferente de UTF-8.
- Relógio de 12 horas.
- Formato mês/dia.
- Variante que não corresponda integralmente ao contrato final.

## 3. Padrões candidatos

Android:

```text
DD/MM/AAAA HH:mm - Remetente: texto
DD/MM/AA HH:mm:ss - Remetente: texto
```

iOS:

```text
[DD/MM/AAAA, HH:mm:ss] Remetente: texto
[DD/MM/AA, HH:mm] Remetente: texto
```

O contrato final deve registrar as expressões exatas observadas, incluindo
espaços, caracteres direcionais e delimitadores.

## 4. Definição de linha física

Linha física é a sequência terminada por LF, ou o conteúdo final depois do
último LF. CR pertencente a CRLF não faz parte do texto da linha.

Cada linha física recebe exatamente uma classificação:

- `MESSAGE_HEADER`;
- `MESSAGE_CONTINUATION`;
- `SYSTEM_EVENT`;
- `EMPTY_LINE`;
- `UNSUPPORTED_CONTENT`;
- `PARSE_ERROR`.

```text
classifiedPhysicalLines = totalPhysicalLines
```

Nenhuma linha pode ser removida antes do ledger.

## 5. Mensagens multilinha

- Uma linha com header válido inicia mensagem.
- Linhas subsequentes sem header pertencem à mensagem anterior como
  `MESSAGE_CONTINUATION`.
- Linha vazia dentro da mensagem é preservada no texto e classificada
  `EMPTY_LINE`, com vínculo à mensagem.
- Uma linha semelhante a timestamp que não satisfaz integralmente o header
  permanece continuação.
- Linha sem mensagem anterior e sem evento conhecido gera `PARSE_ERROR`.

## 6. Remetentes com dois-pontos

O formato textual pode ser ambíguo. O parser só separará nome e texto quando:

- o nome estiver fornecido explicitamente em configuração; ou
- uma análise em duas passagens encontrar uma interpretação única e consistente.

Caso contrário:

```text
code = AMBIGUOUS_SENDER_DELIMITER
exitCode = 3
```

O parser nunca escolherá silenciosamente o primeiro ou último dois-pontos.

## 7. Eventos preliminares

- `DELETED_MESSAGE`;
- `EDITED_MESSAGE`;
- `CALL_EVENT`;
- `MEDIA_OMITTED`;
- `SYSTEM_NOTICE`;
- `UNKNOWN_EVENT`.

Marcadores linguísticos exatos deverão ser obtidos do corpus. Evento desconhecido
não será tratado como mensagem comum sem aviso.

## 8. Timezone

- O arquivo não é presumido como UTC.
- `--timezone` é obrigatório.
- O valor deve ser um identificador IANA.
- O timestamp original permanece inalterado.
- Timestamp inexistente ou ambíguo no fuso gera erro.
- O resultado inclui horário local interpretado e UTC.

## 9. Modelo pretendido

```text
IngestResult
  schemaVersion
  parserVersion
  source
  compatibility
  messages[]
  events[]
  lineLedger[]
  errors[]
  warnings[]
  qualityMetrics
```

`source`:

```text
fileName
sha256
byteLength
encoding
lineEnding
hasBom
totalPhysicalLines
```

`NormalizedMessage`:

```text
sourceMessageId
sourceFileName
sourceFileSha256
sourceLineStart
sourceLineEnd
rawTimestampText
parsedTimestampLocal
assumedTimezone
timestampUtc
detectedVariant
rawSenderText
rawText
normalizedText
messageKind
editedMarker
parseWarnings[]
canonicalFingerprint
```

`LineLedgerEntry`:

```text
lineNumber
classification
messageSourceId
eventSourceId
errorCode
```

`ParseError`:

```text
code
severity
sourceFileName
sourceFileSha256
lineStart
lineEnd
detectedVariant
reason
recoverable
rawExcerpt
```

O texto bruto e `rawExcerpt` obedecem à retenção.

## 10. Normalização

Permitido:

- remover BOM da primeira linha após registrá-lo;
- remover caracteres direcionais conhecidos somente para interpretar timestamp;
- converter CRLF para LF em `normalizedText`;
- normalizar fingerprint em Unicode NFC.

Proibido:

- `trim` destrutivo do texto bruto;
- compactar espaços no conteúdo;
- remover linhas vazias;
- alterar pontuação;
- trocar caracteres antes de conservar `rawText`.

## 11. Identidade e deduplicação

Identidade dentro do arquivo:

```text
sourceMessageId =
  sourceFileSha256 + ":" + sourceLineStart + ":" + sourceLineEnd
```

Fingerprint candidato:

```text
chatScope +
normalizedSender +
resolvedTimestamp +
messageKind +
NFC(normalizedText) +
occurrenceOrdinal
```

Política:

- timestamps iguais são permitidos;
- mensagens idênticas consecutivas recebem ordinais distintos;
- o CLI calcula fingerprints, mas não remove mensagens;
- colapso futuro exige fingerprint e contexto anterior/posterior inequívocos;
- incerteza gera `POSSIBLE_DUPLICATE`;
- conteúdo divergente no mesmo alinhamento gera `CONTENT_CONFLICT`;
- conflitos preservam todas as proveniências e bloqueiam métricas.

## 12. Métricas

```text
precision =
  expectedMessagesCorrectlyDetected /
  detectedMessages

recall =
  expectedMessagesDetected /
  expectedMessages

partialRate =
  partiallyInterpretedMessages /
  expectedMessages

lineAccountability =
  classifiedPhysicalLines /
  totalPhysicalLines

explicitRejectionRate =
  incompatibleInputsRejected /
  incompatibleInputs
```

Critérios pretendidos para o contrato suportado:

- precisão = 100%;
- recall = 100%;
- parcialidade = 0%;
- contabilidade = 100%;
- rejeição explícita = 100%.

## 13. Corpus e prevenção de overfitting

- Desenvolvimento: 4 exportações, 2 Android e 2 iOS.
- Regressão: 2 exportações, 1 Android e 1 iOS.
- Validação privada: 2 exportações, 1 Android e 1 iOS.

O conjunto privado não entra no repositório nem é consultado durante a
implementação. O expected output fica com o revisor.

As oito exportações são mínimo; a aprovação depende da matriz de cobertura.

## 14. Matriz mínima

- [ ] Ano curto.
- [ ] Ano longo.
- [ ] Segundos presentes.
- [ ] Segundos ausentes.
- [ ] LF.
- [ ] CRLF.
- [ ] BOM.
- [ ] Multilinha.
- [ ] Linha vazia.
- [ ] Unicode direcional.
- [ ] Nome com dois-pontos.
- [ ] Conteúdo semelhante a timestamp.
- [ ] Evento de sistema.
- [ ] Mensagem editada.
- [ ] Mensagem apagada.
- [ ] Chamada.
- [ ] Mídia omitida.
- [ ] Timestamps iguais.
- [ ] Mensagens idênticas consecutivas.

## 15. Processo de finalização

1. Aprovar este draft.
2. Receber corpus autorizado fora do repositório.
3. Criar versões redigidas de desenvolvimento e regressão.
4. Revisar linha a linha.
5. Atualizar padrões e eventos observados.
6. Criar `INGEST-CONTRACT-v1.md`.
7. Congelar schema, exemplos e expected outputs.
8. Somente então implementar o parser.

## 16. Aprovação do draft

```text
Consultor:
Desenvolvedor:
Data:
Decisão: APPROVED | CHANGES_REQUIRED
Observações:
```
