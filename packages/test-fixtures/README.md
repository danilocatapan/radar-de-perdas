# Fixtures de ingestão

| Campo | Valor |
|---|---|
| Versão | 1.0-draft |
| Responsável | Proprietário do Radar de Perdas |
| Status | Corpus exclusivamente sintético; contrato apenas aprovado como draft |

## Regra fundamental

Este diretório aceita apenas conteúdo sintético ou conteúdo real previamente
redigido, revisado e formalmente aprovado para entrar no repositório.

Arquivos originais, ainda que autorizados, permanecem fora do Git.

## Estrutura

```text
development/       exemplos visíveis usados para elaboração
regression/        casos congelados executados continuamente
rejected/          formatos que devem ser rejeitados
expected/          classificação linha a linha e mensagens esperadas
configs/           configurações sintéticas sem dados pessoais
validation-private/ proibido no Git; mantido pelo revisor
coverage-matrix.csv cobertura dos casos do contrato
```

`validation-private/` está no `.gitignore` e não deve ser criado por Codex.

## Divisão futura do corpus real autorizado

Mínimo:

- Desenvolvimento: quatro exportações, duas Android e duas iOS.
- Regressão: duas exportações, uma Android e uma iOS.
- Validação privada: duas exportações, uma Android e uma iOS.

Quantidade não substitui cobertura. O gate depende de todos os casos obrigatórios
da matriz.

## Processo para admitir uma fixture derivada de dado real

1. Confirmar instrumento e instrução que permitam o uso.
2. Manter o original no diretório operacional externo.
3. Criar uma versão redigida.
4. Trocar nomes, telefones, e-mails, endereços, produtos e valores.
5. Preservar somente a característica sintática necessária.
6. Revisar risco de reidentificação.
7. Fazer revisão linha a linha da saída esperada.
8. Registrar aprovação na matriz sem citar cliente ou hash do original.

## Expected outputs

Cada manifesto deve declarar:

- fixture;
- conjunto;
- compatibilidade esperada;
- variante;
- total de linhas;
- classificação de cada linha;
- mensagens e intervalos esperados;
- avisos ou erros esperados.

Não ajustar expected output apenas para fazer um teste passar. Mudanças exigem
revisão do contrato e aprovação.

## Casos pendentes de geração

Os arquivos textuais versionados podem ser normalizados pelo Git. Casos que
dependem dos bytes CRLF ou BOM deverão ser materializados por um gerador
determinístico somente depois da aprovação do contrato final. Até lá, a matriz
os marca como pendentes.

ZIP, CSV, relógio de 12 horas e encoding incompatível também permanecem como
casos sintéticos pendentes. A existência das linhas na matriz não antecipa o
parser nem comprova cobertura pelo corpus real.
