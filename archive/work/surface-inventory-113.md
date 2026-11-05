# Surface inventory -- session 113 E54

Registered in `structure-discovery-plan.md` as E54. Source paths are relative to
`/tmp/juju-41-tree` at `e5db99d585`; docs paths refer to the PR worktree at
`48ef1fca17`. This ledger reconciles generated command documentation with source-
constructed command registration. It does not assert backend behavior,
authorization, model-type support, live output or complete errors.

## Method and verification

- CLI docs inventory: filenames in `docs/reference/juju-cli/list-of-juju-cli-commands/*.md`, excluding `index.md`.
- CLI source-constructed inventory: `go run ./cmd/juju help commands` from `/tmp/juju-41-tree`; the supercommand is built by `cmd/juju/commands/main.go:215-266`, and commands are registered in `registerCommands` at `cmd/juju/commands/main.go:331-555`.
- Hook-command docs inventory: filenames in `docs/reference/hook-command/list-of-hook-commands/*.md`, excluding `index.md`.
- Hook-command source inventory: command maps in `internal/worker/uniter/runner/jujuc/server.go:38-107`, dispatched by `NewCommand` at `:192-203`.
- Verification run: the comparison script counted docs, source help output and hook maps from the files above. Counts reconcile below.

## Summary

| Surface | Docs count | Source non-alias count | Source alias count | Docs not in source | Source non-alias not in docs | Disposition |
|---|---:|---:|---:|---:|---:|---|
| `juju` CLI generated pages | 159 | 159 | 29 | 0 | 0 | Complete for non-alias source help at this anchor; aliases are help-visible but intentionally not generated as separate pages. |
| Hook-command generated pages | 38 | 38 | 0 | 0 | 0 | Exact filename-to-source-map match. Context success remains command-specific. |

## CLI command reconciliation

**Documented and source-visible non-alias commands (159):**

`actions`, `add-cloud`, `add-credential`, `add-k8s`, `add-machine`, `add-model`, `add-secret`, `add-secret-backend`, `add-space`, `add-ssh-key`, `add-storage`, `add-unit`, `add-user`, `attach-resource`, `attach-storage`, `autoload-credentials`, `bind`, `bootstrap`, `cancel-task`, `change-user-password`, `charm-resources`, `clouds`, `config`, `constraints`, `consume`, `controller-config`, `controllers`, `create-backup`, `create-storage-pool`, `credentials`, `dashboard`, `debug-code`, `debug-hooks`, `debug-log`, `default-credential`, `default-region`, `deploy`, `destroy-controller`, `destroy-model`, `detach-storage`, `diff-bundle`, `disable-command`, `disable-user`, `disabled-commands`, `documentation`, `download`, `enable-command`, `enable-destroy-controller`, `enable-user`, `exec`, `export-bundle`, `expose`, `find`, `find-offers`, `firewall-rules`, `grant`, `grant-cloud`, `grant-secret`, `help`, `help-action-commands`, `help-hook-commands`, `import-filesystem`, `import-ssh-key`, `info`, `integrate`, `kill-controller`, `login`, `logout`, `machines`, `migrate`, `model-config`, `model-constraints`, `model-defaults`, `model-secret-backend`, `models`, `move-to-space`, `offer`, `offers`, `operations`, `refresh`, `regions`, `register`, `reload-spaces`, `remove-application`, `remove-cloud`, `remove-credential`, `remove-k8s`, `remove-machine`, `remove-offer`, `remove-relation`, `remove-saas`, `remove-secret`, `remove-secret-backend`, `remove-space`, `remove-ssh-key`, `remove-storage`, `remove-storage-pool`, `remove-unit`, `remove-user`, `rename-space`, `reprovision-machine`, `resolved`, `resources`, `resume-relation`, `retry-provisioning`, `revoke`, `revoke-cloud`, `revoke-secret`, `run`, `scale-application`, `scp`, `secret-backends`, `secrets`, `set-constraints`, `set-credential`, `set-firewall-rule`, `set-model-constraints`, `show-action`, `show-application`, `show-cloud`, `show-controller`, `show-credential`, `show-machine`, `show-model`, `show-offer`, `show-operation`, `show-secret`, `show-secret-backend`, `show-space`, `show-status-log`, `show-storage`, `show-task`, `show-unit`, `show-user`, `spaces`, `ssh`, `ssh-keys`, `status`, `storage`, `storage-pools`, `subnets`, `suspend-relation`, `switch`, `sync-agent-binary`, `trust`, `unexpose`, `unregister`, `update-cloud`, `update-credential`, `update-k8s`, `update-public-clouds`, `update-secret`, `update-secret-backend`, `update-storage-pool`, `upgrade-controller`, `upgrade-model`, `users`, `version`, `whoami`

**Help-visible aliases not generated as separate pages (29):**

`debug-hook` -> `debug-hooks`, `list-actions` -> `actions`, `list-charm-resources` -> `charm-resources`, `list-clouds` -> `clouds`, `list-controllers` -> `controllers`, `list-credentials` -> `credentials`, `list-disabled-commands` -> `disabled-commands`, `list-firewall-rules` -> `firewall-rules`, `list-machines` -> `machines`, `list-models` -> `models`, `list-offers` -> `offers`, `list-operations` -> `operations`, `list-regions` -> `regions`, `list-resources` -> `resources`, `list-secret-backends` -> `secret-backends`, `list-secrets` -> `secrets`, `list-spaces` -> `spaces`, `list-ssh-keys` -> `ssh-keys`, `list-storage` -> `storage`, `list-storage-pools` -> `storage-pools`, `list-subnets` -> `subnets`, `list-users` -> `users`, `model-default` -> `model-defaults`, `relate` -> `integrate`, `resolve` -> `resolved`, `set-default-credentials` -> `default-credential`, `set-default-region` -> `default-region`, `show-credentials` -> `show-credential`, `update-credentials` -> `update-credential`

**Mismatches:** none for non-alias commands. `doc_not_help = []`; `nonalias_not_doc = []`.

**Registration caveats:**

- The source help list is constructed from the command registry, not from executing each command. `registerCommands` includes conditional developer-mode registrations for `dump` and `dump-db` at `cmd/juju/commands/main.go:431-434`; with developer mode off in the verification run they are not in help output and no generated pages exist for them.
- Missing commands can fall through to plugin lookup when the supercommand is not embedded (`cmd/juju/commands/main.go:226-242`). Plugin names are dynamic local behavior and are not part of the generated built-in command inventory.
- Embedded command use can whitelist/exclude commands before registration (`cmd/juju/commands/main.go:303-319`). The generated docs and this inventory describe the ordinary built-in CLI, not every embedded-client subset.
- Command registration is not proof of controller-side support. Example leads already in E52/E53 still need source or live tracing where behavior matters: `create-backup`, `exec`, `run`, `set-firewall-rule`, storage commands, provider-specific commands and migration commands.

## Hook-command reconciliation

**Documented and source-registered hook commands (38):**

`action-fail`, `action-get`, `action-log`, `action-set`, `application-version-set`, `close-port`, `config-get`, `credential-get`, `goal-state`, `is-leader`, `juju-log`, `juju-reboot`, `network-get`, `open-port`, `opened-ports`, `relation-get`, `relation-ids`, `relation-list`, `relation-model-get`, `relation-set`, `resource-get`, `secret-add`, `secret-get`, `secret-grant`, `secret-ids`, `secret-info-get`, `secret-remove`, `secret-revoke`, `secret-set`, `state-delete`, `state-get`, `state-set`, `status-get`, `status-set`, `storage-add`, `storage-get`, `storage-list`, `unit-get`

**Mismatches:** none. `hook_src_not_doc = []`; `hook_doc_not_src = []`.

**Registration caveats:**

- `allEnabledCommands` merges base, storage, leader, resource, secret and action command maps (`internal/worker/uniter/runner/jujuc/server.go:97-107`), and `NewCommand` errors only when a name is absent from the merged map (`:192-203`). That establishes command-name registration, not command success.
- Hook data is context-dependent: relation hooks require relation remote fields, storage hooks require a storage ID, workload hooks require workload/check/notice fields, and secret hooks require a secret URI and sometimes a revision (`internal/worker/uniter/hook/hook.go:81-143`).
- Some commands have additional runtime conditions; for example `relation-set --app` requires leadership before writing application relation settings (`internal/worker/uniter/runner/jujuc/relation-set.go:163-200`). A full hook-command/context matrix remains open.

## Subject-map effect

1. Generated CLI command pages can be treated as a closed inventory of ordinary, non-alias built-in CLI command surfaces at the 4.1 anchor. Aliases are help-visible redirects, not independent command subjects.
2. Generated hook-command pages exactly match the source command-name maps. They are a closed name inventory, not a closed behavior matrix.
3. E52/E53 should keep using command lists as coverage checklists under the owning subjects. They do not imply page-per-command subjects or backend behavior.
