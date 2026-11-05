# E72: storage boundary and connected candidate, session 124

**Proposal, not an approved page, skeleton, figure, rule or tool change.** Source `/tmp/juju-41-tree` at `e5db99d5854803bd30ab9ea19bf6e16bab9bbcc5`; docs worktree `48ef1fca17`. Registered in `structure-discovery-plan.md` before new tracing. E57/E58 were already studied: this is neither held out nor evidence of reader benefit. E44 did not establish benefit and E59 failed its original four-of-four threshold. An outline is not finished content.

## Boundary result and one concrete arrangement

A **character** is a subject-level notion; a **leg** is a dependent aspect of a character. Neither the code nor the preregistered criteria give a numerical rule converting a dependency graph into conceptual granularity. Our strongest working classification is **pool: candidate character; storage instance: character; attachment: relationship leg of the storage instance, with the unit as a necessary co-participant**. A storage-wide cross-page abstraction is plausible, but no evidence here establishes it as a separate contract beyond the named notions. This is an informed proposed arrangement, not a source-forced theorem or a settled global structure. In particular we cannot rule out a pool section within an overarching storage character or an independently addressed relationship page solely from the observed behaviors. Equal expressive power does not decide the classification either.

Proposed page arrangement for review after the global gate: **storage pool page** for model-scoped reusable source configuration and pool calls; **storage page** for instance identity, backing, ownership, lifecycle and a linkable **storage attachment** relationship section; **unit** links to the same attachment contract and retains unit-specific conditions; **machine** links machine-side filesystem/volume attachment, removal and disk-inspection facets; **charm/application** link declarations and directives; provider/cloud entries describe evidenced provider branches. Keep existing `storage`, `storage-pool`, `storage-directive`, `storage-provider`, `storage-calls` and other existing anchors resolving through any approved move; enumerate actual inbound anchors before implementation. The pool page is proposed, not created. This is not an instruction to fold all storage into unit or machine.

| Prediction / alternative | Evidence, limitation and classification |
|---|---|
| Pool is more than one instance's field | A model-write caller creates a named pool against a model registry, validating provider and attributes; `ListPools` is read-authorized. Directive generation selects its pool, and count two generates two instance UUIDs referring to it (`pool.go:58-90,160-215`; `domain/storage/service/storagepool.go:110-164`; `domain/storageprovisioning/unitstorageargs.go:127-142,183-235`). A pool has its own reusable role before and across instances: supports candidate character, but the management operations and many-to-one reference do not prove it cannot be a storage leg. `UpdatePool` and `RemovePool` return `CodeNotYetAvailable` directly, so do not promise those lifecycle operations at this facade (`pool.go:217-228`). |
| Instance is not an attachment property | A client supplies an existing storage ID and a unit separately; attachment validates each, and the detachment job deletes the relationship without deleting the instance (`attach.go:38-75`; `domain/removal/state/model/storage.go:409-467`). Backing composition, life and explicit destroy apply to the instance; its relationship and owner can change. This supports a storage-instance character; it does not promise portable or persistent storage in every provider/removal path. |
| Attachment is not an instance-only or unit-only fact | Life of both participants, charm name and definition, kind, minimum size, count, sharing and machine ownership govern attachment (`domain/application/service/unit.go:390-445,470-584`); the transaction checks both sides and may set the instance's charm name (`domain/application/state/storage.go:1584-1634`). Detach checks the alive unit's minimum and schedules relationship and backing-attachment jobs (`domain/removal/service/storage.go:258-317,320-358`). This supports a two-participant relationship section and unit cross-link. Separate participant effects do not establish that the relationship itself needs a page. |

**Further discriminating comparison, using prior traces.** Cloud/region model defaults are selected by a model's cloud and region, yet are scoped outside any one model and feed configuration of multiple models (`domain/modeldefaults/service/service.go:416-481`; `skeleton-control-117.md:152-163`). Model command blocks are a per-model set whose checker governs interactions in that same model, including exec and machine removal (`model-command-blocks-113.md:18-24`). A pool resembles defaults in being reusable across multiple independently existing consumers; it differs from blocks, which are controls of their particular model. This strengthens the pool-character hypothesis by scope and use, not simply operation count, but does not logically refute a storage-domain leg encompassing multiple instances. Relation composition connects application endpoints, and relation-unit membership has its own guarded entry and settings (`domain/relation/state/relation.go:80-111,1797-1856`; `content-planning-slice-relation-120.md:21-59`). Storage attachment is more like that membership of an existing subject than the relation's endpoint composition: it binds one unit to one pre-existing storage instance, and detachment can leave the instance. This supports an instance relationship section with a unit link, without proving all relationship pages have the same level. Neither comparison rules out a different conceptual grouping, and both reuse studied paths.

**Remaining discriminator.** Investigate whether Juju exposes a storage-pool role or stable contract outside provisioning/storage consumers sufficiently different from model-local resource configuration to establish a character rather than the leg of a storage subject, and whether a documented cross-subject abstraction adds behavior not exhausted by its participant contracts. Register specific alternative predictions before any additional source paths. Do not call the structure locked merely because this proposal names pages.

## Contract to retain at proposed addresses

- **Pool create/list:** a model-write client submits each pool for provider/configuration validation; per-pool results can fail independently. A read caller lists pools; each filter has a result/error. Update/remove are whole-call not-yet-available responses on this facade. Provider support for a kind must be checked, not inferred from existence of a pool (`pool.go:58-90,160-228`; `domain/storageprovisioning/provisioning.go:71-138`).
- **Instance construction/provisioning:** a directive specifies pool, kind, requested size and count; on the traced new-unit path Juju computes provider-dependent composition, creates instance arguments, and later the storage provisioner invokes the provider for volume creation and publishes success (`unitstorageargs.go:127-142,183-265`; `internal/worker/storageprovisioner/volume_ops.go:19-101`). An accepted request or inserted record is not provider completion. E57's real rootfs helper probe produced filesystem support, machine scope, and block-kind refusal; not a live provision.
- **Attach:** model-write authorization and change-block checks are whole-call; each unit/storage pair has its own result (`attach.go:20-35`). Validate both subjects and charm compatibility, count, sharing and machine constraints before transactional rechecks. An attachment record is not proof that a provider mount has completed. Errors and retries must remain call-local.
- **Detach:** model-write authorization and negative `MaxWait` rejection precede processing. With a unit tag, select that pair; without one, process all attachments of the storage, stopping on the first failed attachment for that item. Results are per submitted storage ID and can be partial (`detach.go:45-113,157-274`). For an alive unit, minimum-count checks occur before job scheduling; force is passed to scheduling and does not remove that earlier guard (`domain/removal/service/storage.go:274-317,320-358`). The job normally waits for dead, whereas force can advance a dying attachment (`:385-475`); no completed provider detach follows merely from scheduling. Unit ownership is a distinct relationship; deletion also deletes the owner relationship if the detached unit is the owner (`domain/removal/state/model/storage.go:409-467`).
- **Machine removal / EBS:** a machine with live units requires force on the traced path; machine-owned storage is selected separately and unit cascade uses `destroyStorage=false` (`domain/removal/state/model/machine.go:142-155,193-220,246-299`). EBS-backed filesystem composition can be machine-scoped filesystem plus model-scoped volume, with model ownership; this specific new-unit path is not selected as machine-owned. Attachment cleanup is scheduled, but force can outrun normal provider detach. The source trace is not live AWS evidence of cloud survival, detach completion, reattachment, or integrity (`filesystem-lifetime-114.md:21-48`). Do not repeat the universal filesystem-dies-with-machine statement. Unit removal with `destroyStorage=true` is a different path. The owner sentence remains separately queued, not silently corrected.

Example: a directive for pool `fast` and count two generates two instance arguments with that pool; a permitted detach of one storage/unit pair schedules removal of that pair, not the other instance or the pool. The real local `go run ./cmd/juju help detach-storage` says the CLI selects one or more IDs, detaches each from all units, and warns of partial failures and force. That command exercised local help only, not a controller, provider or detachment.

## Separate epic preparation

**JUJU-10586 — per-call evidence, incomplete.** Store source revision, API or CLI entry, actor and guard, reachable path, whole-call versus per-item scope, exact returned template/code, trigger, remediation, supported version, and unknowns. Examples are source-level facade mappings, not proven CLI rendering or exhaustive inventories:

| Entry / condition | Observed source mapping | Remediation and remaining proof |
|---|---|---|
| `CreatePool`, invalid name | Per pool: `storage pool name is either not set or is not a valid name`, `CodeNotValid` (`pool.go:92-99`). | Supply a valid name after checking the actual naming rules; trace RPC/client rendering and test. |
| `CreatePool`, provider absent from model | Per pool: `no storage provider %q exists in the current model`, `CodeNotFound` (`pool.go:107-112`). | Select an available provider for that model; provider availability and exact client rendering remain untested. |
| `Attach`, unit missing | Per pair: `unit %q does not exist`, `CodeNotFound` (`attach.go:44-52`). | Select an existing unit; verify actual client rendering. Whole-call authorization/change-block errors are separate. |
| `Attach`, already attached | Per pair: `storage %q is already attached to unit %q`, `CodeAlreadyExists` (`unit.go:552-565`; `attach.go:146-150`). | Inspect the existing relationship and omit the redundant request; no runtime RPC run. |
| `DetachStorage`, negative max wait | Whole call: `max wait time cannot be a negative number`, `CodeNotValid` (`detach.go:57-61`). | Supply a non-negative value; CLI exposure and rendered code not established. |
| `UpdatePool`/`RemovePool` | Whole call: `not yet available in %s`, `CodeNotYetAvailable` (`pool.go:217-228`). | Do not promise a supported equivalent; establish version/client-specific alternatives before advising one. |

The existing checker checks global raise-form/template vocabulary, not this call association, authorization, actual rendered code, trigger or remediation. Test wrong-call same message, modified/deleted message and code, missing evidence and explicitly unresolved paths after approval. Do not change the selected count.

**JUJU-9635 — figures, incomplete.** Existing `Storage database schema` view comes from shared `docs/juju.ggarch:4837-4845`; `storage.md:16-24` supplies caption and alternative text. It answers record relationships, not actual transition order, successful provider provisioning or force outcomes. A proposed relationship view could distinguish pool→instances, instance↔unit attachment and instance→filesystem/volume, while an optional separate dynamic view would need traced actors, guards and force branches; do not infer either is required or design the diagram before approval. Validate selection, DDL, shared editable model, visual grammar, accessible equivalent and light/dark rendering; trace the contributor guide and actual feedback process before asserting acceptance.

A second composite-key discrepancy was exposed by the required DDL check: `domain/schema/model/4.0.15-model-release.ddl:446-454` makes `storage_pool_attribute` primary key `(storage_pool_uuid, "key")`; `docs/juju.ggarch:2120-2125` marks only `key` as `pk: true`. The storage view sets `fields: hidden` (`:4837-4845`), so no visibly wrong field marker is established. Audit all affected model/views and generator only after approval; do not change the ten stopped scratch candidates. Credential's analogous discrepancy remains separate and open.

## Connected global candidate and 35 selected dispositions

The candidate in `structure-review-123.md:38-57` remains the global baseline except for the proposed storage arrangement above; it carries conditional roles in the user's causal order (definition/scope, records/invariants, streams, actors, interactions, configuration/failure index) only where relevant. Process, tool, provider and catalog pages retain their own forms. Shared operation/task is evidenced across action and administrative exec, with distinct guards/targets and pending/partial failures. Backup spans controller, all model exports and object stores and is more than the CLI or a database leg (`backup-subject-113.md`); whether it is a controller leg or cross-subject abstraction remains unresolved, not an equal-facts tie. Status/history and sequence allocator page-level classification remain unresolved. Cloud material is normally linked to the underlying model; source-checked common material may exceptionally be repeated for an isolated cloud-page reader. Existing `global-skeleton-119.md` blanket one-home and provider-only-intersection wording is superseded by this proposal, not edited.

Each selected row below is provisional; details and prior source leads remain in `application-disposition-115.md:9-45` and `structure-review-123.md`. “Retain” is not an audit or approval; all anchors and figures require an implementation-time link check.
**Session 126 delta:** `storage-machine-boundary-126.md` updates the connected
candidate and the constraint, machine, storage and cloud dispositions with the
GCE root-disk pool path. The pool participates in machine allocation as well as
managed storage, but the character-versus-storage-leg classification remains
unresolved. The other 31 rows below are unchanged by this bounded evidence.


| Selected page | Disposition, link or unresolved check |
|---|---|
| action | Keep action initiation; link shared script/task and distinguish machine exec, write/admin guards and partial results. |
| agent-version | Keep version contract; link agents/upgrade; rollout untraced. |
| annotation | Shared target metadata; target eligibility and result-shape defect remain open. |
| application | Keep realized bindings and directives; link charm, relation and storage pool/instance; refresh direction open. |
| charm | Keep declarations including storage and endpoint; link application realization. |
| resource-charm | Keep charm content/fetch distinct from storage and compute; link object store. |
| cloud | Keep cloud/region and provider distinctions; link credential, model and provider storage. |
| constraint | Shared request/merge semantics; link machine allocation and space restrictions; provider limits. |
| controller | Keep actor/model links; link backup, database, object store and HA; backup classification open. |
| controller-upgrade | Keep process and agent-version links; no completion guarantee. |
| credential | Keep separately from model credential reference; correct proposed update connectivity claim only after approval; downstream provider effects open. |
| database | Keep inspection, link DB REPL, object store and backup; do not assert dump-db works. |
| external-controller | Keep remote connection; link offer/migration; remote failures untraced. |
| high-availability | Keep controller mechanism; scope unsupported methods, no blanket unavailability. |
| image-metadata | Keep image selection link to machine; priority discrepancy open. |
| lease | Keep coordination contract, link relevant mechanisms; no blanket guarantee. |
| link-layer-device | Keep network observation distinct from disk; link machine/subnet. |
| machine | Keep lifecycle/provisioning and inspector-only disk facet; link storage attachment/removal and provider; no general client disk inventory claimed. |
| model | Keep identity `(name, qualifier)`, credential and command-block aspects; link pools, access and defaults. |
| model-defaults | Keep cloud/region defaults distinct from a model; precedence untraced. |
| model-migration | Keep process and phase-specific links/errors; migration coverage incomplete. |
| object-store | Keep artifact/backend contract; link backup, resource, task output and migration; backend untraced. |
| offer | Keep offered endpoint and consumer distinction; link relation/external controller. |
| relation | Keep composition and participant settings; link charm/application, hook and partial command context. |
| secret | Keep secret/revision and shared selector vocabulary; call-local selector precedence; preserve anchors. |
| secret-backend | Keep backend separate; link model/secret; drain/removal limits open. |
| space | Keep space; distinguish alpha rename guard from constraint-name FK refusal; link constraint. |
| ssh-key | Keep key grants separate from server; retain named-user caveat. |
| ssh-server | Keep connection mechanism and links to key/target; scope provider and Kubernetes behavior. |
| storage | Proposed instance page with attachment, backing and directive addresses; candidate pool page, preserve old pool anchor and links. Qualified EBS/force path; unit-owner wording open. |
| subnet | Keep subnet/space distinction; provider and exposure limits. |
| telemetry | Keep observation mechanisms; collector behavior untraced. |
| unit | Keep unit lifecycle; link two-participant attachment; action tasks are not all unit-targeted. |
| user | Keep identity and target-specific grants; blocks are separate. |
| zone | Keep location link to subnet/placement; cloud placement provider-dependent. |

Broader scope includes direct pages, authored nested, generated CLI and keys, process/mechanism/tool pages, and machine/cloud provider families (`reference-skeletons-117.md:33-46`); existing counts are accounting only. The 38 individual hook/action command derivations, five Kubernetes refinements and earlier workload scope are 402-denied; do not relaunch, replace or route around them. `CrayonEvaluation` is also denied. Provider/model type/version, UI, migrations, watcher inventories, backend and recovery paths, and generated publication remain untraced in part. Full epic completion requires user-directed blocker resolution and actual Jira acceptance text; no silent narrowing.

## E71 regression reapplied to this candidate

Pass means only that this research candidate explicitly specifies the listed boundary, qualified facts and links; it does not mean rendered pages or underlying defects are fixed. These cases were studied earlier, not held out.

| Case | Result on candidate | Evidence / remaining limit |
|---|---|---|
| 1 Action/exec | Pass, outline | Corrected global candidate records target, guards, partial failures and pending; no live execution. |
| 2 Endpoint | Pass, outline | Charm declaration → application binding → relation composition; not all endpoint behavior audited. |
| 3 Model/REPL | Pass, outline | Qualified model identity versus name-only `.switch` and UUID `.open`; ambiguity still open. |
| 4 Hook timing | Pass, outline | Unit agent timer can initiate update-status, not all hooks begin with DB change; other triggers untraced. |
| 5 Storage lifetime | Pass, outline | EBS model-owned volume, force and conditional attachment cleanup captured above; no cloud survival claim. |
| 6 Credential update | Pass, outline | Auth type vs nil connectivity validator and model/credential links; provider aftermath open. |
| 7 Space refusals | Pass, outline | Alpha facade guard distinct from constraint FK refusal; requires page/link implementation. |
| 8 Credential diagram | Pass, outline | Both composite key fields required; current view hides fields; model defect remains. |
| 9 Task status | Pass, outline | Synthetic aborted-only fallback is pending; intended contract and real cancellation open. |
| 10 Equal-facts / allocator | Unresolved | The incorrect general tie is rejected; actual shared allocator's page-versus-leg classification is still unproved. Storage classification is also qualified above. |
| 11 Blocked commands | Pass, outline | Command details blocked, metadata validation differs from command availability; not individual completeness. |

Thus **10 bounded outline passes, one unresolved**, not 10 finished pages or evidence of accuracy beyond the cited traces. Earlier E71 baseline remains one pass, one fail, nine unresolved, and its independent reuse-policy conflict remains recorded. No reference, figure, checker, rules, PR or production-source edit is authorized by these results.
