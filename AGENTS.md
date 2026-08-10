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

## Qualidade de produto e comunicação comercial

Ao alterar material ou comportamento visível ao cliente, o agente deve:

- ler e aplicar obrigatoriamente a
  [`docs/AGENT-PERSONA-USUARIO.md`](docs/AGENT-PERSONA-USUARIO.md);
- separar códigos internos da linguagem comercial e não expor jargão como
  conceito principal sem necessidade;
- permitir que o cliente compreenda o problema encontrado, a evidência, a ação
  recomendada e os limites do resultado;
- consultar [`docs/CUSTOMER-FAQ.md`](docs/CUSTOMER-FAQ.md) como fonte canônica
  das respostas comerciais;
- não prometer integração, automação ou capacidade inexistente;
- não equiparar demora ou ausência de resposta a venda perdida, receita perdida,
  redução de conversão ou impacto financeiro;
- preservar integralmente os controles de segurança e privacidade.

### Gate interno da persona do usuário

Depois de gerar e renderizar o artefato cliente-facing final, o agente deve
executar explicitamente a revisão definida em
[`docs/AGENT-PERSONA-USUARIO.md`](docs/AGENT-PERSONA-USUARIO.md). A revisão deve
ocorrer sobre a experiência realmente inspecionada em desktop e mobile, não
apenas sobre o código-fonte ou os resultados dos testes.

O material somente recebe `APPROVE` interno quando:

- a nota total é maior ou igual a `9.0/10.0`;
- nenhum critério recebe zero;
- nenhuma falha crítica é encontrada;
- a revisão visual real foi concluída nos dois viewports.

Qualquer falha crítica bloqueia `APPROVE`, independentemente da nota. Se a
renderização ou a inspeção não puder ser concluída, registrar
`USER_VISUAL_REVIEW_REQUIRED` e não atribuir aprovação definitiva.

A entrega final deve informar nota, breakdown por critério, veredito, falhas
críticas e estado da revisão visual. Esse score é um gate interno de qualidade:
ele não substitui `mostrar -> ouvir`, não comprova utilidade com pessoas reais e
não valida disposição a pagar.

### Três invariantes comerciais

Toda apresentação a prospects deve responder claramente:

1. Dá para fazer isso no meu WhatsApp?
2. Você consegue descobrir quantos ficaram sem resposta?
3. Como você faria isso com minhas conversas?

A segunda resposta deve corrigir a premissa: o Radar conta solicitações
comerciais elegíveis sem resposta humana útil dentro da amostra analisada e dos
critérios definidos. Não cobre todos os clientes nem todo o WhatsApp, e mantém
casos inconclusivos separados.

### Cinco perguntas de avaliação de compreensão

As invariantes comerciais não substituem as cinco perguntas aplicadas ao
decisor depois da leitura do relatório, definidas em
[`docs/PILOT-BASELINE.md`](docs/PILOT-BASELINE.md):

1. Qual foi o objetivo da auditoria?
2. Quais foram os principais achados?
3. Qual ação possui maior prioridade?
4. Qual limitação impede interpretar os achados como vendas perdidas?
5. Qual é o próximo passo recomendado?

Essas perguntas medem compreensão do relatório e exigem pelo menos quatro
respostas corretas em cinco. Não devem ser apresentadas como FAQ comercial.

### Validação de produto

Antes da conclusão do `R1A`, a sequência é:

```text
rodar
  -> olhar
  -> mostrar
  -> ouvir
  -> conseguir R1A
  -> executar manualmente
```

Gerar e testar não substitui olhar a saída renderizada como cliente. Mostrar e
ouvir usam somente a demonstração sintética; conseguir `R1A` depende da
qualificação, dos aceites e dos controles aplicáveis. A execução continua
manual e não autoriza parser, frontend ou automação.

Depois de eventual `GO`, mudanças que alterem comportamento ou experiência
percebida pelo usuário seguem:

```text
implementar
  -> rodar
  -> revisar visualmente
  -> usar ou demonstrar
  -> ouvir
  -> medir
  -> manter | corrigir | reverter
```

Compilação, testes e code review não bastam para validar uma feature de produto.
A regra pós-`GO` não cria burocracia para mudanças puramente internas e não
antecipa qualquer gate.

## Entrega

Na resposta final, informe:

- branch e commit;
- URL do draft PR;
- arquivos e contratos alterados;
- validações executadas;
- gates e pendências externas;
- estado de mergeabilidade do PR.
