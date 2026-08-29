# Prompt Hermes, fase CUTOVER

Use este prompt somente depois de o relatório da fase PREPARAR ter sido revisado. Substitua todos os valores entre `<...>`.

```text
Você vai executar o cutover controlado do vault FGV Plan B. Não avance se qualquer gate falhar.

Entradas fechadas:
REMOTE_URL=https://github.com/ArthurMalucelli/fgv-vault.git
EXPECTED_UPSTREAM=origin/codex/vault-plan-b
EXPECTED_FETCH_REFSPEC=+refs/heads/codex/vault-plan-b:refs/remotes/origin/codex/vault-plan-b
OPERATIONAL_AS_OF=$(TZ=America/Sao_Paulo date +%F)
TESTED_COMMIT=<SHA remoto aprovado com 40 caracteres>
READINESS_REPORT=<caminho absoluto do JSON devolvido na preparação>
EXPECTED_READINESS_REPORT_SHA256=<SHA-256 exato do readiness report>
EXPECTED_CUTOVER_BUNDLE_SHA256=<SHA-256 do arquivo CUTOVER-BUNDLE.json>
STAGING_VAULT=<clone de staging já validado>
STAGING_HERMES=<cópia de configuração já validada>

Gate obrigatório antes de qualquer mutação:

1. Imprima e execute:
   `python3 "$STAGING_VAULT/.fgv/scripts/verify_hermes_bundle.py" --root "$STAGING_VAULT" --bundle '30 Sistema/Hermes/CUTOVER-BUNDLE.json'`
2. Confirme o SHA-256 externo de `CUTOVER-BUNDLE.json` contra `EXPECTED_CUTOVER_BUNDLE_SHA256`.
3. Imprima e execute:
   `python3 "$STAGING_VAULT/.fgv/scripts/validate_hermes_readiness.py" --report "$READINESS_REPORT" --tested-commit "$TESTED_COMMIT" --as-of "$OPERATIONAL_AS_OF" --manifest "$STAGING_VAULT/30 Sistema/Hermes/hermes-manifest.json" --production-vault /root/vault --hermes-home /root/.hermes --staging-hermes "$STAGING_HERMES" --bundle "$STAGING_VAULT/30 Sistema/Hermes/PREPARAR-BUNDLE.json" --expected-report-sha256 "$EXPECTED_READINESS_REPORT_SHA256"`
4. Confira novamente que o relatório contém recomendação READY, que `operational_as_of` coincide com a data atual de `America/Sao_Paulo`, que `tested_commit` é exatamente `TESTED_COMMIT`, que o manifest checksum coincide e que `git -C "$STAGING_VAULT" rev-parse HEAD` coincide. Exija branch local `codex/vault-plan-b`, `@{u}` igual a `EXPECTED_UPSTREAM`, `branch.codex/vault-plan-b.remote=origin`, `branch.codex/vault-plan-b.merge=refs/heads/codex/vault-plan-b` e somente `EXPECTED_FETCH_REFSPEC`. Exija uma única fetch URL e no máximo uma push URL, normalizadas para `REMOTE_URL`, e compare `git ls-remote --exit-code origin refs/heads/codex/vault-plan-b` com `TESTED_COMMIT`. Bloqueie rewrites, wildcard, refspec extra, push routing alternativo e listas múltiplas. Relatório do dia anterior, checkout detached ou outro remote bloqueia e exige nova fase PREPARAR com novo `TESTED_COMMIT` do dia.
5. Confira os hashes do backup integral de `/root/.hermes` e do inventário vazio de untracked. Exija working tree produtiva sem mudança tracked e sem qualquer untracked.

Se qualquer comando retornar diferente de zero, se o relatório não for READY ou se um hash divergir, responda BLOCKED e pare. Não tente corrigir produção.

Primeira mutação permitida:

6. Imprima todos os comandos planejados para a janela de cutover. Não imprima segredos.
7. Pause ingestão do Eclass, atendimento acadêmico do WhatsApp e todos os cronjobs que possam escrever no vault. Registre exatamente o que foi pausado.
8. Repita o preflight da produção. Qualquer untracked ou mudança tracked nova bloqueia o cutover. Não existe importação pendente fora do Git.
9. Preserve o clone produtivo anterior e seu SHA como alvo de rollback. Ative o clone de staging no caminho produtivo por troca recuperável de diretórios ou ponteiro, sem reescrever histórico Git.
10. Instale `fgv-sync` como único owner Git e instale o service/timer somente a partir dos exemplos revisados. Eclass, WhatsApp e cron não executam Git diretamente.
11. Confirme que todo material aprovado, inclusive os imports de 08.26, 08.28 e 09.04, já está tracked em `TESTED_COMMIT` sob `Material/` singular. Não crie commit de importação no cutover.
12. Instale a configuração de `STAGING_HERMES` preservando permissões e sem copiar caches, tokens ou credenciais para locais novos. Credenciais existentes ficam nos mesmos arquivos protegidos.
13. Antes de instalar o owner, confirme que o clone ativado preserva somente `EXPECTED_FETCH_REFSPEC`; não corrija silenciosamente um clone divergente. Rode `FGV_AS_OF_DATE="$OPERATIONAL_AS_OF" fgv-sync refresh`. Ele deve validar URL, branch source e refspec antes e depois de cada gate, fazer fetch explícito somente da branch canônica, validar o commit remoto numa worktree temporária com `generate_state.py --check` e `validate_vault.py`, e só depois fazer fast-forward, nunca use force push.
14. Rode auditor, `validate_hermes_cutover.py --as-of "$OPERATIONAL_AS_OF"`, suíte `.fgv/tests`, `generate_state.py --check` e os smoke tests acadêmicos com a mesma data. Toda resposta de teste deve declarar `as_of_commit`, `operational_as_of` e `sync_state`.
15. Faça smoke real de Eclass, WhatsApp e busca acadêmica antes de reativar qualquer cron. Confirme escrita em `Material/`, Tasks em `00 Home/Tasks.md` e recuperação com hash do catálogo pinado pelo snapshot, sem injetar o catálogo completo, com uma linha, no máximo 16 KiB e cinco candidatos. Rode `hermes_channel_smoke.py` contra os entrypoints instalados. O runner precisa aceitar o schema AST fechado e executar cada adapter com Python isolado `-I`. Eclass precisa provar `material-eclass`; WhatsApp precisa provar `ultima-aula-matematica`, ambos com challenge, stdout consumido, path selecionado e único arquivo aberto exatos. Preserve receipts e artefatos brutos. Probe morto, API reatribuída, branch não executada ou receipt separado do fluxo é falha.

Rollback automático:

16. Se qualquer smoke, checksum, auditoria, validação ou push falhar, pause novas escritas, isole o clone novo sem apagar dados, restaure a configuração do backup autenticado, volte ao clone produtivo anterior preservado e reative somente os jobs anteriores. Emita recomendação ROLLED_BACK com o primeiro erro e os hashes preservados.
17. Só se todos os gates passarem, reative os cronjobs um a um, verifique o lock de `fgv-sync` e emita o relatório final. Não faça outras mudanças depois disso.
```
