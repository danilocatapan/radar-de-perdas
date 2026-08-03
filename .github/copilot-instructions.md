# Instruções para GitHub Copilot — Radar de Perdas

## Fluxo Git obrigatório

1. Verifique `git status -sb`.
2. Atualize `main` com `git fetch origin` e
   `git pull --ff-only origin main`.
3. Crie `codex/<slug-descritivo>`.
4. Nunca edite diretamente na `main`.
5. Respeite os gates de `docs/GATE-STATUS.md`.
6. Execute a validação integral aplicável.
7. Revise o diff e use commit convencional em português.
8. Faça push da branch e abra draft PR para `main`.
9. Confirme que o PR está mergeável e sem conflitos.
10. Não faça merge, force-push ou rebase destrutivo sem autorização.

As regras canônicas estão em `AGENTS.md`.

## Privacidade

- Dados reais e holdout privado nunca entram no repositório.
- Não copie conversas para logs, testes, PRs ou ferramentas de IA.
- Use apenas fixtures sintéticas nesta fase.
- Não implemente parser, vertical slice ou produção antes dos respectivos gates.

## Conclusão

Informar branch, commit, PR, validações e pendências externas.
