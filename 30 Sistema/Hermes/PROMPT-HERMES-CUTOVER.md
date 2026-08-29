# Prompt Hermes, fase CUTOVER

Use este prompt somente depois de o relatório da fase PREPARAR ter sido revisado. Substitua todos os valores entre `<...>`.

```text
Você vai executar o cutover controlado do vault FGV Plan B. Não avance se qualquer gate falhar.

Entradas fechadas:
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
   `python3 "$STAGING_VAULT/.fgv/scripts/validate_hermes_readiness.py" --report "$READINESS_REPORT" --tested-commit "$TESTED_COMMIT" --manifest "$STAGING_VAULT/30 Sistema/Hermes/hermes-manifest.json" --production-vault /root/vault --hermes-home /root/.hermes --bundle "$STAGING_VAULT/30 Sistema/Hermes/PREPARAR-BUNDLE.json" --expected-report-sha256 "$EXPECTED_READINESS_REPORT_SHA256"`
4. Confira novamente que o relatório contém recomendação READY, que `tested_commit` é exatamente `TESTED_COMMIT`, que o manifest checksum coincide e que `git -C "$STAGING_VAULT" rev-parse HEAD` coincide.
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
13. Rode `fgv-sync refresh`. Ele deve usar lock, working tree limpa, fetch, validar o commit remoto numa worktree temporária com `generate_state.py --check` e `validate_vault.py`, e só depois fazer fast-forward, nunca use force push.
14. Rode auditor, validador de cutover, suíte `.fgv/tests`, `generate_state.py --check` e os smoke tests acadêmicos. Toda resposta de teste deve declarar `as_of_commit` e `sync_state`.
15. Faça smoke real de Eclass, WhatsApp e busca acadêmica antes de reativar qualquer cron. Confirme escrita em `Material/`, Tasks em `00 Home/Tasks.md` e recuperação catalog-first.

Rollback automático:

16. Se qualquer smoke, checksum, auditoria, validação ou push falhar, pause novas escritas, isole o clone novo sem apagar dados, restaure a configuração do backup autenticado, volte ao clone produtivo anterior preservado e reative somente os jobs anteriores. Emita recomendação ROLLED_BACK com o primeiro erro e os hashes preservados.
17. Só se todos os gates passarem, reative os cronjobs um a um, verifique o lock de `fgv-sync` e emita o relatório final. Não faça outras mudanças depois disso.
```
