# E77–E79: allocator, backup and migration boundaries

Research proposal, not an approved reference, figure, rule or tool edit. Source
anchor `/tmp/juju-41-tree` at `e5db99d5854803bd30ab9ea19bf6e16bab9bbcc5`;
docs worktree at `48ef1fca17`. E77, E78 and E79 were registered in
`structure-discovery-plan.md` before their new source traces. E63 and E55
already studied the same paths, and the existing database page mentioned
sequence migration before E79 registration: these are contaminated, not held
out or reader tests. Source establishes behavior within traced paths, not a
source-forced filename or reader benefit.

## E77: sequence allocation

The same `NextValue` inserts zero for a new namespace, otherwise increments it,
requires one affected row and reads the result in the supplied transaction;
preparation, update, row-count and read failures return errors
(`domain/sequence/state/sequence.go:21-62`). Machine creation calls it in the
creation transaction with `machine`, then formats a decimal machine name
(`domain/machine/state/state.go:93-102`, `placement.go:131-147,237-245`). On
the traced machine-model add-units path, storage-instance creation calls it
with `storage`, combining the number and storage name in a storage ID
(`domain/application/state/unit.go:467-513`, `unitstate.go:1399-1428`). The
add-units response returns unit names, not those storage IDs
(`apiserver/facades/client/application/addunit.go:120-136`). There are other
namespaces and batch allocation paths; neither gap-free IDs nor later provider
success follows from these two traces.

The model database has a sequence row keyed by namespace
(`domain/schema/model/sql/0029-sequence.sql:1-4`); a privileged controller
machine DB REPL can open a model and execute SQL (`cmd/jujuagentd/agent/dbrepl.go:74-103,140-150`,
`internal/worker/dbrepl/worker.go:237-268,320-335,781-785`). This is an
inspection surface, not proof of a general sequence-management API. The existing
`database` page already describes the shared operation and its namespaces
(`docs/reference/database.md:41-43,106-117`); no new page is implied.

**Outcome and judgment.** The registered behavioral criterion is met for these
paths. Shared transactional allocation is a substantive cross-subject mechanism;
the differences in namespace and output remain at the machine/storage
contracts. Provisionally explain the mechanism as a model-database leg, with an
inspector-relevant shared address on `database`, linked from those contracts.
Unlike a pool's directly selectable provider policy, its traced role is internal
number allocation for participant transactions, exposed here through database
inspection. This is a judgment about the supported role, not a rule requiring
characters to be independently managed or a universal negative about other
surfaces. Cross-subject abstraction and a database leg can coexist. Reopen if a
material independently meaningful sequence contract is found. The source does
not require a standalone page, and no reader comparison was run.

## E79: model migration of sequences

Legacy import registers the sequence operation before machine and storage
imports (`internal/migration/legacy/importoperations.go:71-97`). It reads a
model's sequence map, converts `task` to `operation`, `stores` to `storage`,
application names and matched container names, skips nonpositive values, and
inserts positive values minus one (`domain/sequence/modelmigration/import.go:93-139,142-153`).
The sequence state inserts the map in a transaction and reports a duplicate
namespace error on a primary-key conflict (`domain/sequence/state/state.go:61-94`).
The versioned model export separately selects sequence rows; the model import
inserts them, with a direct row conversion between the inspected export versions
(`domain/export/state/model/export.go:1018-1020,2007-2009`,
`domain/modelimport/transformer/transforms/to_v4_1_0/transform.go:1049-1052`,
`domain/modelimport/state/model/import.go:789-791,1924-1927`). These are
bounded code paths, not a completed end-to-end migration or proof of continuity
for all versions.

**Outcome.** The separately registered legacy import supports shared model-scope
sequence handling beyond a single participant; it does not establish an
independently administered allocator. It strengthens, rather than changes, the
E77 shared database-mechanism judgment. The direct modern row export/import is
additional source evidence, not proof of the routing or success of a live model
migration. Potential legacy-name collision remains queued: both matched LXD and
KVM names for one parent convert to the same namespace and the map assignment
can overwrite a value; whether both can occur in a supported legacy input and
its actual consequences are untraced.

## E78: backup

`create-backup` uses unscoped `POST /backup`; the route is controller-admin
protected (`api/client/backups/create.go:20-57`, `apiserver/apiserver.go:1087-1093`).
The creator exports controller data, enumerates model databases and exports each,
and derives an object inventory from those exports; it resolves the relevant
controller/model object stores to read inventoried objects
(`internal/worker/backupcreation/creator.go:193-233,284-315`). A model with no
inventoried objects does not need its store resolved on this path. A lease gates
archive generation, and a concurrent request can receive a not-yet-available
error; release is attempted and can itself fail
(`internal/worker/backupcreation/worker.go:166-177,212-233,303-307,348-351`).
Controller export and model exports occur separately, so the code does not
establish a cross-database snapshot. The HTTP handler streams the generated
archive and invokes cleanup even on transfer failure; cleanup itself ignores
removal errors (`apiserver/internal/handlers/backups/backups.go:95-105,127-137`,
`internal/worker/backupcreation/creator.go:371-373`). Do not promise successful
creation, transfer, cleanup, complete object-store copying or restore.

**Outcome and judgment.** The registered criterion is met: backup has a
controller-scoped trigger and a substantive cross-subject capture/transfer
contract, with consistency and error conditions not reducible to one database
or object-store operation. Both roles coexist; controller ownership does not
absorb the backup abstraction. Propose a stable backup address linked from
controller, database, model, object store, lease and `create-backup`; it need
not be a separate file. This does not establish an independently managed backup
character or restoration. A prior upgrade-guide conflict remains unverified at
runtime (`work/backup-subject-113.md`).

## Connected candidate and E71 reassessment

This artifact is an overlay to `work/storage-structure-124.md` and
`work/storage-machine-boundary-126.md`, not finished content or page edits.
Retain the pool-character proposal, the storage-instance/attachment split,
operation/task distinction, conditional causal order, provider limits and all
blocked family scopes. Revise only affected selected-page dispositions:

| Selected page | Evidence-driven proposal |
|---|---|
| database | Keep the existing model sequence and allocation address, explain shared transaction/inspection scope and link identifiers and model migration; link backup. |
| machine | Link its machine namespace and decimal name to the shared allocator; retain root-disk pool/provider distinction. Keep the separately exercised dropped additional-disk input as an unresolved source defect, not a promise that requested disks are created (`add-machine-disks-127.md`). |
| storage | Link its storage namespace and name/number instance IDs to the same mechanism; retain pool, instance and attachment distinctions. |
| model-migration | Link sequence import/conversion and its version-specific conditions; no blanket live-continuity guarantee. |
| controller | Link the controller-admin backup interaction and cross-subject backup contract. |
| object-store | Link only the inventory-selected backup reads, not all stored objects. |
| lease | Distinguish backup-generation coordination and attempted release from archive streaming. |

All other 28 selected rows retain their previous provisional dispositions; no
full-page audit or selected-counter change follows. The broader family index,
existing anchors and figure preservation obligations remain unchanged.

Reapply the 11 previously studied E71 cases to the corrected candidate as
extended here; pass means the **outline explicitly states** the discrimination,
not that pages, underlying defects or all source contracts are complete.

| Case | Result | Basis / unresolved limit |
|---|---|---|
| 1 Action/exec | Pass, outline | Shared operation/task; distinct targets, guards and partial outcomes (`structure-review-123.md:42-47`). |
| 2 Endpoint | Pass, outline | Charm declaration, application realization, relation composition and links (`structure-review-123.md:25,43`). |
| 3 Model/REPL | Pass, outline | Qualified identity vs name-only selection and UUID open; ambiguity remains (`structure-review-123.md:26,46`). |
| 4 Hook timing | Pass, outline | Conditional watcher path and timer-triggered update-status (`structure-review-123.md:27,49-51`). |
| 5 Storage lifetime | Pass, outline | EBS model-owned volume and force/cleanup qualification (`storage-structure-124.md:26-27`). |
| 6 Credential update | Pass, outline | Auth-type validation vs nil connectivity validator, with model/credential link (`structure-review-123.md:29,49-51`). |
| 7 Space refusals | Pass, outline | Alpha guard distinguished from constraint foreign-key refusal (`structure-review-123.md:30,44`). |
| 8 Credential figure | Pass, outline | Composite key in model; visible view hides fields (`structure-review-123.md:31,47`). |
| 9 Task status | Pass, outline | Synthetic aborted-only pending fallback is not an intent or live-cancellation claim (`structure-review-123.md:32,45`). |
| 10 Allocator / equal facts | Pass, outline | This overlay specifies shared mechanism, provisional database-leg judgment, participant links, inspection and migration limits; equal facts do not determine the level. This is an architectural inference, not proof no contrary surface exists. |
| 11 Blocked commands | Pass, outline | Command details remain blocked; hook metadata validity is not command availability (`storage-structure-124.md:118`). |

Thus **11 bounded outline passes, zero unresolved for the named E71 outline
criteria**, conditional on the explicitly provisional E77 classification. This
is a reassessment of the augmented candidate, not of the unmodified session-119
baseline: its one pass, one fail and nine unresolved remain historical. No case
is held out, a reader study or proof of content completeness. E44 did not
establish benefit; E59 failed its original threshold; E74 ordering is
contaminated.

## JUJU-10586 and JUJU-9635 preparation

Error evidence must attach to a specific entry/version and client, not a global
matching string. `AddMachines` has whole-call authorization/change-block guards
and per-machine results; allocation failures occur within its transactional
path, not automatically as a proven literal client code. Add-units returns unit
names, not newly allocated storage IDs. Backup errors before response headers
and failures after HTTP 200 are different: after `WriteHeader`, streaming errors
are logged, not returned as a fresh classified HTTP error
(`backups.go:99-137`). Client checksum and local-file errors are another stage.
Trace actual rendered messages/codes, reachability, remediation and version
before enforcing per-call drift; the existing checker cannot establish these.

For a concrete bounded error record, a backup generation lease claim denied or
already held produces `a backup is already being created` from the worker;
the request returns that error to the handler (`worker.go:120-152,212-233`,
`backups.go:99-103`). The classifier maps not-yet-available to HTTP 409 and the
JSON error writer serializes its message and code (`apiserver/errors/errors.go:103-146,152-163,234-237`,
`apiserver/internal/http/json.go:18-25`). A throwaway Go program exercised the
actual classifier with the same constructed error and JSON result: status 409,
message `a backup is already being created`, code `not yet available; try again
later`. Retry after the concurrent generation has ended is a conditional
remediation; no real contention, HTTP request or CLI rendering was exercised.
The same probe mapped a synthetic malformed-body error to HTTP 400 / code
`bad request`; the actual parser reason depends on input. This is not an
exhaustive error inventory or per-call drift enforcement.

The existing `Change log database schema` view depicts change-log records, not
sequence allocation (`docs/reference/database.md:16-24`). The existing `Object
store database schema` view has hidden fields and depicts records, not backup
capture or transfer (`docs/juju.ggarch:4699-4706`,
`docs/reference/object-store.md:12-20`). A proposed behavioral figure, if later
justified and approved, could separately show transaction-bound sequence
allocation or backup's authorizer, creator, individual exports, inventoried
object reads, streaming and attempted cleanup. Neither current schema proves
success or cross-database snapshot consistency. Existing contributor guidance
requires an editable shared model, caption and alt text, light/dark inspection
and `ggarch check` (`CONTRIBUTING.md:131-154`); actual feedback and full visual
grammar/acceptance remain open. Storage and credential composite-key model
issues remain hidden-field discrepancies, not proven visible wrong markers.

No controller, live database, backup, migration or provider ran in these traces.
Four 402-denied scopes, actual Jira acceptance text, structural approval and all
push/security gates remain open. Do not implement this proposal yet.
