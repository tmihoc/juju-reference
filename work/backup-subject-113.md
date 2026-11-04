# Backup subject trace -- session 113 E55

Registered in `structure-discovery-plan.md` as E55. Source paths are relative to
`/tmp/juju-41-tree` at `e5db99d585`; docs paths refer to the PR worktree at
`48ef1fca17`. This is a source trace only. No live controller, backup creation,
restore or recovery was exercised.

## Question

Given E54 established `create-backup` as an ordinary built-in CLI command
surface, what can the subject map say about backup as a reference subject
without overclaiming live success, restore behavior or consistency guarantees?

## Trace

| Step | Evidence | Reading |
|---|---|---|
| Generated CLI surface | `docs/reference/juju-cli/list-of-juju-cli-commands/create-backup.md:1-55` documents `juju create-backup`, local download, checksum verification, scratch `backup-dir`, one creation at a time and non-snapshot consistency limits. | Backup is a user-visible CLI surface, not merely an internal worker. |
| Built-in command registration | E54 verified the generated CLI docs match source help. `cmd/juju/commands/main.go:390-391` registers `backups.NewCreateCommand()`. | `create-backup` is part of the ordinary built-in CLI inventory at the anchor. |
| CLI command behavior | `cmd/juju/backups/create.go:25-56` is the generated help text; `:63-85` names the command; `:112-145` calls the backup client, receives metadata and archive stream, verifies the checksum, writes the local archive, then prints metadata. `:156-183` removes incomplete archives and keeps checksum mismatches under `.corrupt`. | The command creates a fresh remote archive and streams it to the local client. Local success depends on checksum verification and local file I/O. |
| Client API | `api/client/backups/create.go:20-23` defines `POST /backup`; `:25-57` calls an unscoped HTTP client, sends notes, reads backup metadata from response headers and returns the response body as the archive stream. | This is an HTTP transfer surface, not an RPC facade method. |
| HTTP route and auth | `apiserver/apiserver.go:1087-1093` registers `POST /backup` with `controllerAdminAuthorizer` and tracked request handling. `:1095-1108` registers old GET `/backups` paths only so old clients receive a clear upgrade error. | Backup creation is controller-admin HTTP behavior. Old download-by-id flow is explicitly not the current creation path. |
| Handler | `apiserver/internal/handlers/backups/backups.go:34-42` states create-and-stream semantics and no staging after the request; `:64-92` dispatches POST create and rejects GET old-client flow; `:95-138` creates the archive, writes metadata headers, streams bytes and cleans up on return or transfer failure. | The server does not keep the archive after handling the request. The client must create again after interrupted transfer. |
| Controller-machine worker injection | `cmd/jujuagentd/agent/machine/manifolds.go:773-806` wires the `backupcreation` manifold only through `ifController` and passes `BackupCreator` to the API server manifold. | The creator is a controller-machine capability consumed by the API server, not a model worker. |
| Creator construction | `internal/worker/backupcreation/manifold.go:77-125` outputs a `corebackups.BackupCreator`; `:150-194` resolves controller services, per-model services, controller object store and per-model object stores, then creates the archive creator. | Backup spans controller services, model services and object stores. |
| Lease / concurrency | `internal/worker/backupcreation/worker.go:120-153` accepts creation requests; `:166-177` queues requests but gates them on a lease; `:212-223` returns not-yet-available when a backup is already being created. | The one-at-a-time rule is source-backed through a controller-wide lease, not just CLI wording. |
| Archive contents and consistency | `internal/worker/backupcreation/creator.go:137-152` states the archive contains controller export, one export per model and data-dir files, with no cross-database snapshot. `:178-205` exports controller data and controller object inventory; `:207-233` exports every model namespace and model object inventory; `:284-315` streams referenced objects from namespace object stores. `:344-373` writes the archive in a per-request temp directory and returns a cleanup. | Backup is a controller/database/object-store mechanism. It produces an inspectable archive, but not a single point-in-time controller-wide snapshot. |
| Existing conflict | `docs/howto/upgrade-your-juju-deployment-from-36-to-41.md:456-468` says `juju create-backup` fails with a not-implemented error in 4.0 and 4.1. | This conflicts with the 4.1 source path and generated CLI docs. It is a candidate docs correction, not an authorized edit and not a live success proof. |
| Restore/recovery | A source search found recovery/archive code but no `restore-backup` command or ordinary backup restore CLI/API path in the traced command tree. `cmd/juju/backups/doc.go:29-30` says recovery tooling for bootstrapping a fresh replacement controller is planned and bootstrap does not yet support it. | Creation is implemented; ordinary restore flow remains unestablished by this trace. |

## Subject ownership decision

Backup is not merely a CLI command page and not solely a database page. It is a
controller-admin backup mechanism with a CLI/HTTP surface, a controller-machine
creator, controller and model database exports, and object-store archive
content. Candidate stable address: a controller or database reference anchor
such as `[controller backup]`, linked from `create-backup`, `database`,
`object-store` and recovery/upgrade material. A separate top-level page is a
navigation decision, not decided by source evidence alone.

## What the map may predict

- `juju create-backup` is an ordinary built-in command at the 4.1 anchor.
- The command sends `POST /backup` and receives a streamed archive plus metadata.
- The route requires controller-admin authorization.
- Creation runs through a controller-machine backup creator.
- The archive includes controller export, every model namespace export and
  referenced object-store content.
- Only one creation can proceed at a time through the backup-creation lease.
- The archive is cleaned up on the controller when the request ends.
- The archive is not a single point-in-time snapshot across all controller and
  model databases.

## What remains unproved

- A live backup succeeds on a real controller.
- Restore or recovery is available through an ordinary user-facing command.
- Every platform/provider/model state supports successful creation.
- Exact archive schema is complete and stable for user documentation.
- The best physical docs address or navigation label.
