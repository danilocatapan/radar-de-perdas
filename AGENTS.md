# Regras de trabalho para agentes

Estas regras são obrigatórias para toda nova demanda neste repositório.

## Fluxo Git obrigatório

1. Antes de editar, execute `git status -sb` e confirme que não existem
   alterações locais conflitantes ou fora do escopo.
2. Troque para `main`, execute `git fetch origin` e atualize com
   `git pull --ff-only origin main`.
3. Crie uma branch nova a partir da `main` atualizada, usando
   `codex/<slug-descritivo>`.
4. Nunca desenvolva diretamente na `main`.
5. Implemente somente o escopo autorizado pelos gates em
   `docs/GATE-STATUS.md`.
6. Execute validações proporcionais à alteração.
7. Imediatamente antes da validação final, execute `git fetch origin` e confirme
   que `origin/main` é ancestral da branch:

   ```text
   git merge-base --is-ancestor origin/main HEAD
   ```

   Se não for, incorpore `origin/main` por merge não destrutivo, resolva os
   conflitos preservando os dois escopos e reinicie a validação integral.
8. Antes de qualquer push ou abertura/atualização de PR, execute em uma única
   passagem todas as validações aplicáveis. Resultado parcial ou acumulado não
   substitui uma passagem integral verde.
9. Revise `git diff --check`, `git diff --stat`, `git status -sb` e o diff
   completo. Não publique alterações alheias ao escopo.
10. Use commits convencionais, descritivos e em português:
    - `docs:` documentação e contratos;
    - `test:` fixtures e contratos de teste;
    - `feat:` capacidade nova;
    - `fix:` correção;
    - `chore:` infraestrutura interna.
11. Publique a branch com tracking e abra draft PR para `main`.
12. Depois de cada push, consulte o estado real do PR. Estados
    `CONFLICTING`/`DIRTY` bloqueiam a conclusão; `UNKNOWN` deve ser consultado
    novamente.
13. Não faça merge, force-push, rebase destrutivo nem descarte alterações do
    usuário sem autorização explícita.

O commit vazio que cria a `main` é uma exceção única para o bootstrap do
repositório.

## Validação obrigatória no estágio documental

Enquanto não houver runtime configurado, a passagem integral deve verificar:

- todos os JSONs em `packages/test-fixtures` com parser real;
- correspondência entre `totalPhysicalLines`, arquivo e `lineLedger`;
- CSVs com cabeçalhos válidos;
- links locais Markdown;
- `git diff --check`;
- ausência de dados reais, segredos e diretórios privados no diff.

Quando `package.json` e scripts oficiais forem introduzidos, eles passam a fazer
parte da suíte integral, incluindo lint, typecheck, testes e build aplicáveis.

## Gates do produto

- Não criar `docs/INGEST-CONTRACT-v1.md` antes da revisão do corpus real.
- Não implementar parser antes da aprovação do contrato final.
- Não implementar vertical slice antes da aprovação do parser.
- Não criar infraestrutura produtiva antes do gate comercial e operacional.
- Não marcar um gate como concluído sem evidência verificável.

## Dados e privacidade

- Dados reais nunca entram neste repositório.
- O holdout privado nunca entra no Git.
- Não incluir nomes, telefones, e-mails, conversas ou hashes de arquivos reais em
  commits, logs, issues ou PRs.
- Fixtures versionadas devem ser sintéticas ou formalmente redigidas e aprovadas.
- Antes de receber dados reais, seguir `docs/PRIVACY-PILOT.md`.

## Entrega

Na resposta final, informe:

- branch e commit;
- URL do draft PR;
- arquivos e contratos alterados;
- validações executadas;
- gates e pendências externas;
- estado de mergeabilidade do PR.
