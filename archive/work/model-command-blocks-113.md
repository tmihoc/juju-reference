# Model command block trace -- session 113 E56

Registered in `structure-discovery-plan.md` as E56. Source paths are relative to
`/tmp/juju-41-tree` at `e5db99d585`; docs paths refer to the PR worktree at
`48ef1fca17`. This is a bounded source/docs trace only. No live controller was
exercised and no complete command/facade audit was performed.

## Question

Given E52 identified model command blocks as a shared contract with only how-to
links, what can the subject map say about their owner, behavior and limits
without auditing every blocked command?

## Trace

| Step | Evidence | Reading |
|---|---|---|
| CLI surface and command-set names | `cmd/juju/block/protection.go:20-43` maps CLI command sets `all`, `destroy-model`, `remove-object` to API values `BlockChange`, `BlockDestroy`, `BlockRemove`. Generated docs for `disable-command`, `enable-command` and `disabled-commands` expose those names and lists (`docs/reference/juju-cli/list-of-juju-cli-commands/disable-command.md:34-103`; `enable-command.md:34-103`; `disabled-commands.md:24-87`). | The user-visible surface is command-set based, not one block per command. |
| CLI behavior | `cmd/juju/block/disable.go:35-47` validates the command set and optional message; `:50-61` names `disable-command`; `:69-78` calls `SwitchBlockOn`. `cmd/juju/block/enable.go:34-45` validates the command set; `:48-59` names `enable-command`; `:68-77` calls `SwitchBlockOff`. `cmd/juju/block/list.go:52-68` names `disabled-commands`, with alias `list-disabled-commands`; `:82-129` lists either the current model or all models for admin users. | The commands operate on the selected model by default; listing has a controller-wide administrative view. |
| Client API | `api/client/block/client.go:28-31` creates the `Block` facade client; `:34-50` calls `List`; `:53-69` calls `SwitchBlockOn`; `:71-86` calls `SwitchBlockOff`. | The CLI talks to the client `Block` facade, not to the access/user API. |
| Facade permissions and scope | `apiserver/facades/client/block/client.go:37-43` stores the current model tag, service and authorizer. `:45-52` checks read/write permission on the model tag. `:55-70` lists blocks with read access; `:83-110` switches blocks on/off with write access. `:113-123` accepts only `BlockDestroy`, `BlockRemove`, `BlockChange`. | A block is model-scoped. Read/write access to the model controls listing and switching; this is distinct from user grants. |
| Stored subject | `domain/schema/model/sql/0025-command-block.sql:1-24` defines seeded block types `destroy`, `remove`, `change` and a model-database `block_command` table with one row per block type. `domain/blockcommand/state/state.go:34-79` inserts a block; `:81-113` removes one; `:141-177` lists all; `:179-208` gets a block message. `domain/blockcommand/service/service.go:55-69` enforces message length and idempotent already-exists behavior; `:71-80` lists and removes blocks. | The persisted state is a per-model set of up to three block types with optional messages. |
| Checker contract | `apiserver/common/block.go:51-56` checks a change block. `:58-67` checks remove then change for removal. `:69-80` checks destroy, then remove, then change for destruction. `:83-94` returns an operation-blocked error carrying the configured message. | The shared rule is ordered and cumulative: change blocks are broadest; remove includes change; destroy includes remove and change. |
| Representative affected calls | `apiserver/facades/client/modelconfig/modelconfig.go:158-167` refuses model config set when `ChangeAllowed` fails. `apiserver/facades/client/action/operation.go:241-261` refuses arbitrary `juju exec` operation creation when `ChangeAllowed` fails. `apiserver/facades/client/machinemanager/machinemanager.go:450-456` refuses machine destruction when `RemoveAllowed` fails. `apiserver/facades/client/modelmanager/modelmanager.go:883-907` refuses model destruction when `DestroyAllowed` fails. | Blocks are applied by affected API paths. The command-set list is not itself enforcement; individual API paths call the checker. |
| Existing reference/how-to links | `docs/reference/model.md:142-145` says a change block refuses model configuration changes and links the how-to. `model.md:240-254` says destroy, remove or change blocks refuse model destroy. `docs/howto/manage-models.md:330-340` owns the how-to anchor `restrict-commands-on-a-model`. | Current docs have call-specific mentions and a how-to, but no stable model-reference contract anchor for the shared block semantics. |
| Command-set list accuracy | A mechanical comparison of the source `commandSets` list with E54's ordinary non-alias CLI inventory found 41 listed names; `set-application-base` and `sync-agents` are not ordinary non-alias commands at this anchor. The list also omits many ordinary commands because only some operations are blocked. | The generated command docs' textual command-set list is a surface artifact to verify before treating as exact coverage. The source checker/calls are the stronger evidence. |

## Subject ownership decision

Model command blocks are model-owned controls, not access grants and not a new
page-per-command subject. The owner should be a stable model reference anchor
such as `[model command blocks]`, with affected command/call sections linking to
it and adding call-specific behavior. User/access pages should link only for the
read/write permission needed to view or switch blocks.

## What the map may predict

- A model can carry up to three command block types: destroy, remove and change.
- Listing blocks requires read access to the model; switching blocks requires
  write access to the model.
- `disable-command` and `enable-command` switch block types on the current model.
- Removal checks the remove block before the change block.
- Destruction checks destroy, then remove, then change.
- A configured block message is returned as an operation-blocked error message
  on paths that use the common checker.
- Affected calls must still be checked individually; the checker contract does
  not prove every generated CLI command is blocked.

## What remains unproved

- Full inventory of every command/facade path that checks each block type.
- Live controller behavior and exact client rendering for every command.
- Whether every name in the generated command-set prose is current.
- Whether force options bypass blocks on any particular path.
- The final physical docs heading or whether model.md is the best location.
