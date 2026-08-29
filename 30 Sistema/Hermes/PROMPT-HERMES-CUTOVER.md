# Prompt Hermes, fase CUTOVER

Use este prompt somente depois de o relatório da fase PREPARAR ter sido revisado. Substitua todos os valores entre `<...>`.

```text
Você vai executar o cutover controlado do vault FGV Plan B. Não avance se qualquer gate falhar.

Entradas fechadas:
TESTED_COMMIT=<SHA remoto aprovado com 40 caracteres>
READINESS_REPORT=<caminho absoluto do JSON devolvido na preparação>
EXPECTED_CUTOVER_BUNDLE_SHA256=<SHA-256 do arquivo CUTOVER-BUNDLE.json>
STAGING_VAULT=<clone de staging já validado>
STAGING_HERMES=<cópia de configuração já validada>

Gate obrigatório antes de qualquer mutação:

1. Imprima e execute:
   `python3 "$STAGING_VAULT/.fgv/scripts/verify_hermes_bundle.py" --root "$STAGING_VAULT" --bundle '30 Sistema/Hermes/CUTOVER-BUNDLE.json'`
2. Confirme o SHA-256 externo de `CUTOVER-BUNDLE.json` contra `EXPECTED_CUTOVER_BUNDLE_SHA256`.
3. Imprima e execute:
   `python3 "$STAGING_VAULT/.fgv/scripts/validate_hermes_readiness.py" --report "$READINESS_REPORT" --tested-commit "$TESTED_COMMIT" --manifest "$STAGING_VAULT/30 Sistema/Hermes/hermes-manifest.json"`
4. Confira novamente que o relatório contém recomendação READY, que `tested_commit` é exatamente `TESTED_COMMIT`, que o manifest checksum coincide e que `git -C "$STAGING_VAULT" rev-parse HEAD` coincide.
5. Confira os hashes do backup de `/root/.hermes` e do inventário untracked. Confira que o working tree do clone produtivo está limpo ou que cada untracked está explicitamente preservado, classificado e copiado com o mesmo hash.

Se qualquer comando retornar diferente de zero, se o relatório não for READY ou se um hash divergir, responda BLOCKED e pare. Não tente corrigir produção.

Primeira mutação permitida:

6. Imprima todos os comandos planejados para a janela de cutover. Não imprima segredos.
7. Pause ingestão do Eclass, atendimento acadêmico do WhatsApp e todos os cronjobs que possam escrever no vault. Registre exatamente o que foi pausado.
8. Faça uma segunda cópia verificável dos dois untracked conhecidos e de qualquer novo untracked. Nunca apague o original sem uma cópia autenticada.
9. Preserve o clone produtivo anterior e seu SHA como alvo de rollback. Ative o clone de staging no caminho produtivo por troca recuperável de diretórios ou ponteiro, sem reescrever histórico Git.
10. Instale `fgv-sync` como único owner Git e instale o service/timer somente a partir dos exemplos revisados. Eclass, WhatsApp e cron não executam Git diretamente.
11. Publique os dois untracked conhecidos no caminho canônico `10 Matérias/ContabilidadeFinanceira/Aulas/08.26/Materiais/` com os mesmos hashes, somente se não houver colisão. Use `fgv-sync publish` com cada arquivo importado, `30 Sistema/Estado/catalog.jsonl` e `30 Sistema/Estado/dashboard-snapshot.md` como paths explícitos, porque o wrapper reconstrói o estado antes do commit. Em colisão ou mudança gerada fora dessa lista, pare e faça rollback.
12. Instale a configuração de `STAGING_HERMES` preservando permissões e sem copiar caches, tokens ou credenciais para locais novos. Credenciais existentes ficam nos mesmos arquivos protegidos.
13. Rode `fgv-sync refresh`. Ele deve usar lock, working tree limpo, fetch, fast-forward only, rebuild e check do estado, nunca use force push.
14. Rode auditor, validador de cutover, suíte `.fgv/tests`, `generate_state.py --check` e os smoke tests acadêmicos. Toda resposta de teste deve declarar `as_of_commit` e `sync_state`.
15. Faça smoke real de Eclass, WhatsApp e busca acadêmica antes de reativar qualquer cron. Confirme escrita em `Materiais/`, Tasks em `00 Home/Tasks.md` e recuperação catalog-first.

Rollback automático:

16. Se qualquer smoke, checksum, auditoria, validação ou push falhar, pause novas escritas, isole o clone novo sem apagar dados, restaure a configuração do backup autenticado, volte ao clone produtivo anterior preservado e reative somente os jobs anteriores. Emita recomendação ROLLED_BACK com o primeiro erro e os hashes preservados.
17. Só se todos os gates passarem, reative os cronjobs um a um, verifique o lock de `fgv-sync` e emita o relatório final. Não faça outras mudanças depois disso.
```
