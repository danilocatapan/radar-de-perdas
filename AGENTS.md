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
5. Implemente somente o escopo autorizado em `docs/GATE-STATUS.md`.
6. Execute validações proporcionais à alteração.
7. Imediatamente antes da validação final, execute `git fetch origin` e confirme:

   ```text
   git merge-base --is-ancestor origin/main HEAD
   ```

   Se falhar, incorpore `origin/main` por merge não destrutivo, preserve os dois
   escopos e reinicie a validação integral.
8. Antes de push ou PR, execute todas as validações aplicáveis em uma única
   passagem verde.
9. Revise `git diff --check`, `git diff --stat`, `git status -sb` e o diff
   completo. Não publique alterações alheias ao escopo.
10. Use commits convencionais e descritivos em português.
11. Publique a branch com tracking e abra draft PR para `main`.
12. Depois de cada push, consulte o PR. `CONFLICTING` ou `DIRTY` bloqueia a
    conclusão; `UNKNOWN` deve ser consultado novamente.
13. Não faça merge, force-push, rebase destrutivo nem descarte alterações do
    usuário sem autorização explícita.

## Validação documental

Enquanto não houver runtime oficial, verificar:

- todos os JSONs sintéticos com parser real;
- `totalPhysicalLines`, arquivos e `lineLedger`;
- cabeçalhos e largura dos CSVs;
- links locais Markdown;
- `git diff --check`;
- ausência de dados reais, segredos e diretórios privados no diff.

## Gate atual do produto

`R1A_READY=COMPLETE` continua registrando a prontidão documental já
comprovada. A primeira sessão permanece separadamente bloqueada por:

- `VERTICAL_SELECTION=PENDING_OWNER_SELECTION`;
- `FIRST_R1A_SESSION=BLOCKED`.

`FIRST_R1A_SESSION` só pode mudar de estado quando a vertical estiver
`COMPLETE` e o `DISCOVERY_SESSION_READY` da sessão concreta estiver `READY`.
O agente não escolhe a vertical.

Permitido:

- documentação do pivot e do Discovery Concierge;
- estratégia de aquisição local e relacional;
- checklist simples `DISCOVERY_SESSION_READY`;
- registro pseudônimo vazio;
- representação sintética mínima de até cinco itens;
- protocolo documental do R1B, mantido `BLOCKED_UNTIL_R1A_PASS`;
- testes documentais estritamente necessários.

Bloqueado:

- execução ou oferta paga definitiva do R1B;
- demo comercial refinada;
- parser, frontend, backend, banco ou IA;
- integração com WhatsApp, notificações ou automação;
- arquitetura e infraestrutura produtivas.

Não criar `docs/INGEST-CONTRACT-v1.md`, parser ou vertical slice antes dos gates
futuros. Não marcar gate como concluído sem evidência verificável.

## Dados e privacidade

- Dados reais e holdout privado nunca entram no Git.
- Não incluir nomes, telefones, e-mails, conversas, screenshots, mídias ou hashes
  reais em commits, logs, issues ou PRs.
- Fixtures versionadas devem ser integralmente sintéticas.
- No `R1A`, usar a linguagem “sessão sem custódia, sem cópia e sem retenção das
  conversas”; não afirmar que não existe tratamento de dados.
- O prestador controla o aparelho. Não fotografar, gravar, copiar ou exportar.
- Pular conversas sensíveis e registrar apenas campos autorizados.
- Não criar manifesto, hash, ACL, mídia criptografada ou cadeia de custódia para
  a sessão sem arquivos.
- `EXTERNAL_LEGAL_REVIEW_NOT_OBTAINED` permanece explícito.

## Qualidade visível ao prestador

Aplicar `docs/AGENT-PERSONA-USUARIO.md` a qualquer material mostrado no `R1A`.
Antes do primeiro discovery, exigir somente legibilidade em celular, próxima
ação clara, ausência de códigos internos e nenhuma falha crítica. Refinamento
visual e nota 9,0 não bloqueiam o contato real neste estágio.

Não prometer integração, automação ou capacidade inexistente. Não equiparar
oportunidade, demora ou ausência de resposta a venda ou receita perdida.
Fixtures e testes não comprovam utilidade, mercado ou disposição a pagar.

## Contrato do R1A

- Cinco prestadores da mesma vertical; sessão inicial presencial de 20–30
  minutos.
- A vertical concreta depende do proprietário e deve privilegiar capacidade
  real de recrutamento pela rede pessoal, indicações, bairro e cidade.
- Follow-ups curtos nos dias 4 e 7, sem nova revisão completa do WhatsApp.
- Estados do gate: `NEEDS_RESPONSE`, `NEEDS_QUOTE`, `FOLLOWUP_DUE` e
  `PROMISED_RETURN_DUE`.
- `OUT_OF_SCOPE_CANDIDATE` registra aprendizado sem expandir o produto.
- Gate principal calculado por prestador, nunca por percentuais agregados de
  oportunidades.
- Taxas diagnósticas sempre exibem numerador e denominador e não são tratadas
  como evidência estatística com `n=5`.
- Investigar etiquetas, estrela, agenda, caderno, memória, CRM e outros métodos
  atuais, incluindo suas falhas e a causa da oportunidade parada.
- Se pelo menos três de cinco prestadores considerarem os substitutos atuais
  suficientes, o R1B permanece bloqueado.
- Pagamento real em teste futuro é a única evidência comercial; comentário sobre
  preço é apenas sinal.

## Hipótese comercial posterior

- `MONTHLY_PRICE=R$49.90` permanece `HYPOTHESIS_ONLY`.
- `R1B` permanece `BLOCKED_UNTIL_R1A_PASS` e depende de nova autorização
  explícita do proprietário.
- `OPERATIONAL_LIMIT=PENDING_OWNER_DECISION`; agentes não inventam o limite.
- Zero pagamentos reais produz `STOP`; um produz `INSUFFICIENT_EVIDENCE`; dois
  ou mais produzem `COMMERCIAL_SIGNAL_TO_INVESTIGATE`, nunca `GO_PRODUCT`.
- Aceite verbal, elogio, intenção ou promessa são apenas diagnóstico.
- `STOP` encerra a hipótese ou etapa atual. Repetição, reformulação ou pivot
  exigem nova decisão explícita; não arquivar o repositório nem criar feature
  automaticamente.

## Entrega

Na resposta final, informe branch e commit, URL do draft PR, arquivos e contratos
alterados, validações, gates e pendências externas e mergeabilidade do PR.
