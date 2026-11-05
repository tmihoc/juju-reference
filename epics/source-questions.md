# Source questions and potential defects

Everything here was found while tracing the 4.1 code for the reference pages. Each item is a **question or a lead**, not a confirmed defect: source reads and synthetic probes only, no live controller, database or cloud. None is authorized for a code or prose change. Anchor commit `e5db99d585`.

## Found by the E83 test (2026-11-05)

- [ ] **Upgrade guide, section 18 "Backups are not available"** (`docs/howto/upgrade-your-juju-deployment-from-36-to-41.md:456-468`) says `juju create-backup` fails with a not-implemented error. At the anchor the backups facade (`apiserver/facades/controller/backups`) has no such error. Verify end to end and fix the guide, or the code.
- [ ] **Rendered anchor `#action-task-status`** on the action page is linked and has no target: the `ggarch` single-view HTML visitor writes the figure without the node IDs. Review the extension scope before any repair; preserve the other fragments.

## Potential defects and contract questions

- [ ] Investigate the storage `Import` change-block discrepancy: its comment
  mentions a change block, but the facade body directly checks model write and
  has no `ChangeAllowed` call (`apiserver/facades/client/storage/import.go:42-123`),
  unlike `AddToUnit` (`storage.go:1109-1117`). Check other layers and intended
  behavior before any assertion; no live RPC or block was exercised.

- [ ] Review `import-filesystem` help's provider-versus-pool terminology:
  its first argument is validated and passed as a pool, while help calls it a
  provider (`cmd/juju/storage/import.go:101-127,158-174`). Confirm relevant
  client and provider behavior before proposing a change.

- [ ] Investigate and resolve the `add-machine --disks` dropped-input defect:
  at the anchored 4.1 server v11/v12 the facade discards requested additional
  disks. A real-client/facade/service probe with synthetic provider/state saw
  successful machine results and identical service/state arguments with or
  without directives; separate root-disk constraints survived. No live RPC,
  persistent database or cloud ran. Trace intended fix and version/applicability
  before code or prose changes (`archive/work/add-machine-disks-127.md`).

- [ ] Investigate the DB REPL `.switch` same-name ambiguity before finalizing its contract: the controller schema permits two qualifiers for one model name; `.switch model-<name>` uses a name-only `QueryRow` and does not check ambiguity, while `.open <model-uuid>` uses a UUID. A synthetic SQLite query using actual schema returned one of two matches; no real REPL/controller ran. A wrong database selection matters because the REPL can modify state. Consider an isolated real worker/database exercise and source correction rather than merely adjusting prose (`archive/work/operational-boundaries-e64.md`).

- [ ] Review the plugin invocation contract when the structure is settled: on actual local CLI execution, separated `-m`/`-c` override inherited child environment, omitted flags retain it, and `--model=value` is forwarded but not extracted for the child environment. External plugins may parse their own arguments; no controller operation was exercised (`archive/work/operational-boundaries-e64.md`).

- [ ] Investigate E63's potential image-priority discrepancy: the traced provisioning service sorts numeric priorities ascending, and downstream conversion and EC2 filtering can preserve that order; a synthetic real-helper probe chose the first of equally matching candidates. `image-metadata.md:23,32` says highest priority wins. Trace and exercise the full relevant service-to-provider path before deciding whether this is an implementation/contract defect or a qualified documentation issue; do not claim a live cloud result or fix prose alone (`archive/work/boundary-rules-e63.md`).

- [ ] Investigate the annotation `Set` result shape: the traced facade appends per-entity errors but not successes, while `annotation.md:31,37` says one result per entity. Verify the real facade/RPC contract and client behavior; source trace only, not live, and no fix authorized (`archive/work/boundary-rules-e63.md`).

- [ ] Investigate the status-history kind mismatch before finalizing `status` and `show-status-log` contracts: CLI help and `HistoryKind.Valid()` include `filesystem`, `volume`, `task`, `saas`, `container` and `juju-container`, but the traced history filter skips these kinds and suppresses its default error. The real service with synthetic records returned workload=1 and filesystem=0 with no error. Do not present this as a live-controller result or merely document away a possible code defect; source and probe details are in `archive/work/structure-challenge-e62.md`.

- [ ] Investigate intended operation status for `aborted` tasks before finalizing the shared operation/task contract. The actual `operationStatus` helper returned an error for `{aborted}` and `completed` for `{aborted, completed}`. The real `GetOperationByID` service with synthetic state returned `pending` without error for an aborted task. Unit/machine finish facades authorize the receiver and pass `aborted` to the accepting service; a unit-runner path conditionally emits `aborted` after cancellation. No live controller/agent/RPC or cancellation ran; the separately known cancellation SQL issue may impede entry into `aborting`. Existing `action.md:209` already describes the all-aborted fallback: this is a possible implementation/contract defect, not a missing-doc claim or a prose-only fix (`archive/work/operation-task-boundary-121.md`).

- [ ] `credential.md:106`: remove the assertion that an update checks model cloud reachability; distinguish cloud authentication-type validation from the currently unimplemented per-model connectivity check (`domain/credential/service/service.go:323-372`). Place with credential update; do not promise provider access.

- [ ] Review the credential schema model's primary-key flags before any approved figure/model changes: `domain/schema/controller/sql/0005-cloud.sql:183-191` defines `cloud_credential_attribute` primary key `(cloud_credential_uuid, "key")`, but both `archive/work/cr-schema.ggarch:39-44` and `docs/juju.ggarch:175-180` mark only `key` as `pk: true`. The current credential view sets `fields: hidden` (`docs/juju.ggarch:3792-3801`), so no visible incorrect primary-key label is established. `tools/build_page_schema.py:20-23` restores quoted fields with a hard-coded text primary-key marker; audit its broader consequences before changing it. No fix is authorized.

- [ ] Check the storage pool attribute model before approved figure changes:
  `domain/schema/model/4.0.15-model-release.ddl:446-454` defines composite PK
  `(storage_pool_uuid, "key")`, but `docs/juju.ggarch:2120-2125` flags only
  `key`. The current storage schema view hides fields (`:4837-4845`), so no
  visible wrong marker is established. Audit affected views/generator without
  resuming the stopped scratch cleanup. No fix is authorized.

## Code questions for the Juju developers (read from the code, none run)
Put these in the PR text under "Question for the Juju developers". All read from the 4.1 code, none run.
- `domain/operation/state/task.go:472-480` (cancel a task): the UPDATE uses `$taskStatus.status_id`, but `taskStatus` (`types.go:82-87`) has no such field. Preparing the statement should fail, so cancelling a non-final task would error. Only the not-found path has a test (`task_test.go:218`). The action page describes the evident intent (pending to cancelled, running to aborting).
- `apiserver/facades/client/machinemanager/machinemanager.go:179`: a placement directive is compared with the model UUID, so a normal provider directive such as `zone=x` would fail there. The machine page documents what the code does.
- `ImportKeys` (already in the PR text): a model admin can import keys for any existing user.
- Action facade: `WatchActionsProgress` has no access check (`action.go:274`); `EnqueueOperation` validation compares only the first two actions (`operation.go:140-170`); `FinishTask` sets the reported status whatever the current one is (`task.go:262-298`).
- Revoke (user and offer pages, read from the code, not run): a revoke sets the level just below the one named, whatever the user holds (`state/controller/offer.go: revokeOfferPermission`; same for other objects). Revoking admin from a user who has only read would set write (or consume for an offer). Intended?
- Offer: the how-to says destroying an offer needs offer admin, the code requires model admin or superuser (`applicationoffers.go:354-359, 1191`). A revoke suspends the user's relations before the permission lookup, so a failed revoke may already have suspended them (`service/offer.go:485-501`). The how-to says an offered application cannot be removed until its offers are removed, the code deletes the offers of a dead application (`domain/removal/state/model/application.go:405-459`).
- Secret: the how-to says only model admins write user secrets, the facade checks write access (`secrets.go:48`).
- Lease (session 88, read from the code, not run): the objectstore worker claims a lease in the namespace `object-store` (`internal/worker/objectstore/manifold.go:348`, `core/lease/interface.go:22`), but the `lease_type` table has no `object-store` row (`domain/schema/controller/sql/0002-lease.sql:9-13`, the same three rows in the 4.1 DDL). Either the claim fails on the foreign key at runtime, or something inserts the row outside the schema. The lease page documents the three types the schema has.
- Object store (session 88, from the draft agent, read from the code, not run): the zero-row insert is silent — `domain/lease/state/state.go:125-131` inserts a lease with `SELECT id FROM lease_type WHERE type = $type` and no error when no row matches, so the object-store claim (30 s, held while a write runs, `internal/worker/objectstore/manifold.go:348-352`) never persists and gives no cross-node exclusion. Either add the `object-store` lease type or drop the claim. The object-store page documents the claim without calling it a lease type.
- Container networking (session 90, from the link-layer device page review, read from the code, not run): `isValidBridgeCandidate` looks up a VLAN device's parent with `findParent(nic.ParentDeviceName, nics)` (`domain/network/service/container.go:432-443`), but `findParent` matches `nic.ParentDeviceName == parentName` (`:447-455`) — a device whose parent has that name, that is the VLAN itself or a sibling — never the parent, which would need `nic.Name == parentName`. The parent-type check (`:439`, Ethernet or bond) therefore never sees the VLAN's parent, so a VLAN device is effectively never bridged. Fix `findParent` to match the device name; the link-layer device page documents only the no-parent case until then.
