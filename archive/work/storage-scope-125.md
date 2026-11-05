# E73/E74: storage pool scope, adoption and migration

Research proposal, not an approved page, figure, rule or tool change. Source is
`/tmp/juju-41-tree` at `e5db99d5854803bd30ab9ea19bf6e16bab9bbcc5`; documentation
worktree `48ef1fca17`. E73 was registered before its new traces. E74 was registered
before the subsequent reconciliation and coordinator traces, but the migration
import registration and operation excerpt had already appeared in E73 search
results and was read concurrently with registration. Its ordering evidence is
therefore contaminated: this is not a clean preregistered held-out test. E44 did
not demonstrate benefit; E59 failed its original threshold.

## Contracts and competing boundaries

A **character** is a subject-level notion; a **leg** is a dependent aspect of
another subject. The pool-character versus encompassing-storage-leg question
remains unresolved. The source supports a real model-scoped pool configuration
with distinct consumers; it does not supply a rule that converts those facts to
page level. The E72 proposal of pool and instance pages and an attachment section
remains a candidate, not a locked decision. Neither adoption nor migration
established a non-storage pool role or a separate storage-wide common contract.

| Path and participants | Source-established behavior and qualification |
|---|---|
| Model, provider and application | Model seeding obtains provider recommendations for filesystem and block kinds and stores the recommended mapping (`domain/model/service/modelservice.go:546-625,631-737`). Application directive generation uses an explicit override first, then the appropriate model pool if available; shared charm definitions are skipped on this path (`domain/application/service/storage/directive.go:93-125,136-180`). The override is separately checked against charm storage type (`:227-230,299-315`). The mapping is not itself an instance and a provider recommendation is not a promise that all kinds/providers work. |
| Directive and new unit storage | For each directive the unit-storage path retains count/name/pool/size, computes provider-specific filesystem/volume composition and creates distinct instance arguments; zero count returns no instance arguments (`domain/storageprovisioning/unitstorageargs.go:127-142,183-235`; `provisioning.go:71-138`). A pool can influence the backing shape before individual instances exist. This is still storage provisioning, not evidence of a non-storage consumer. |
| Adoption of an existing provider resource | The storage facade resolves the requested pool before calling filesystem adoption (`apiserver/facades/client/storage/import.go:44-104`). The service loads the pool's provider and attributes, calculates composition, rejects some machine-scoped cases, selects a volume or filesystem importer, and invokes it (`domain/storage/service/adopt.go:87-201,223-239`). This is a distinct, supported facade path from generating new unit storage and can start with an existing provider resource, but it is still about creating a storage instance; a pool is not proved to be a character by this independence. Provider support and completion are conditional. |
| Later add versus adoption | `AddToUnit` checks model write and a change block, then processes each request; an explicit pool is resolved per item and the service branches on model type (`apiserver/facades/client/storage/storage.go:1107-1206`). `Import` directly checks model write, resolves each pool and reports per-item results; its body does not explicitly call `ChangeAllowed` despite its comment (`import.go:42-123`). Whether another layer enforces the block, and intended behavior, require investigation: do not turn the discrepancy into a security or runtime claim. |
| Model migration | Legacy registration places pool import before application import and storage-instance import (`internal/migration/legacy/importoperations.go:76-97`); coordinator adds and executes operations in order (`core/modelmigration/coordinator.go:146-147,177-186`). On import, passed pool descriptions are assigned new UUIDs and retained with name, provider and attributes; provider default pools and recommended mappings are built from the model registry, with matching user-origin pool conflicts skipped (`domain/storage/service/storagepool.go:662-729,818-895`). Imported pools are validated against that registry (`:182-219,225-274`). Application directives resolve pool names and fail if absent (`domain/application/state/migration.go:209-249`). This weakens an independently portable/no-target-dependency prediction and a mere instance-property prediction. It establishes a migration cross-subject ordering contract, not a separate storage-wide abstraction. Source export, end-to-end migration and rollback remain untraced here. |

Example: an application directive may use a model-recommended pool, while an
operator can supply a pool for adoption of an existing filesystem. The first can
produce new instance arguments; the second selects a provider importer before
creating an instance. Neither demonstrates a successful cloud operation. A
candidate overarching storage subject can still encompass both; a separate pool
subject can describe the same cross-subject contracts. No observed fact excludes
both nuanced accounts, so no verdict or change to the 35 dispositions follows.
E71 remains ten previously studied outline passes and one unresolved, not
finished content or reader evidence (`work/storage-structure-124.md:96-114`).

**Next material discriminator:** compare the pool's actual role in an exposed
machine/root-disk or another non-charm resource allocation path, if one exists,
against a provider configuration that is clearly subordinate to its parent.
Preregister competing predictions, supported-surface criteria and falsifiers
before tracing; a mere call-site count or absence in a limited search cannot
settle the boundary. If no distinct supported use is found, explicitly state the
limit and continue with a different behavioral discriminator rather than infer
that the pool is only a storage leg.

## JUJU-10586 preparation, not completion

The facade exposes distinct per-item errors that cannot be joined merely because
they concern a pool. For `Import`, invalid pool name maps to `CodeNotValid` /
`storage pool name is not valid`; missing pool maps to `CodeNotFound` /
`storage pool not found`; missing provider entity maps to `CodeNotFound` /
`storage entity not found in pool`; block kind maps to `CodeNotSupported` /
`adopting block storage is not supported` (`import.go:57-103,109-123`). An
operator can check the model pool name, provider resource ID and kind, but exact
client rendering and provider-specific remediation remain to be proved. In
contrast, `AddToUnit` maps missing pool to `CodeNotFound` / `storage pool %q
does not exist`, with model-write and change-block whole-call guards before
individual results (`storage.go:1109-1125,1158-1175`). Error association, RPC
version negotiation and CLI-local validation must be verified before inclusion;
no live RPC ran. Version 6 of the import facade passes force=false, whereas
V2 parameters carry the caller's force (`import.go:128-143`). Existing checker
only verifies global template/vocabulary membership, not call reachability or
rendering. Preserve the proposed negative drift fixtures in E72.

Real `go run ./cmd/juju help import-filesystem` and `help add-storage` printed
local CLI help. Import help calls the first argument a storage provider, while
CLI `Init` stores and validates it as a pool and `Run` passes that pool to the
API (`cmd/juju/storage/import.go:101-127,158-174`). This is a terminology
review candidate, not evidence all provider names and pool names are equivalent.
Help is not evidence of runtime behavior or of Kubernetes-specific claims.

## JUJU-9635 preparation, not completion

The current `Storage database schema` figure selects pool, model pool mapping,
directives, instance and attachment records from `docs/juju.ggarch:4837-4845`;
`docs/reference/storage.md:16-24` supplies caption and alt text. It can answer a
record-relationship question, not adoption sequence, migration success or
provider state. A future dynamic view, if justified and approved, must separately
show the pool resolution/validation before importer invocation and distinguish
per-item failure from completed provider adoption; it is not a substitute for a
migration view or accessible prose. No new figure is prescribed now.

The model marks only `key` as primary in `docs/juju.ggarch:2120-2125` whereas
DDL `domain/schema/model/4.0.15-model-release.ddl:446-454` uses both pool UUID
and key; this view hides fields, so a visibly incorrect PK marker has not been
shown. The credential mismatch remains separately queued. `CONTRIBUTING.md:131-154`
instructs authors to edit the shared model and view, add caption/alt, inspect
light/dark, and run ggarch check; it references visual conventions and the PR
preview. This is a contributor path, not evidence that feedback occurred or all
views/grammar are correct. Existing review comments and actual acceptance text
still need reconciliation before epic closure.

## Verification and limits

CLI help was executed locally, not a facade, controller, migration, provider or
Kubernetes workload. The docs preview's cached dirhtml built and `/reference/storage/`
returned HTTP 200; fresh-output latex builder succeeded with cached doctrees, no
PDF. No page, diagram, production source, checker, rule, counter or PR changed.
`WorkloadModel`, `HookCommandPages`, `KubernetesCloudAttributes` and
`CrayonEvaluation` remain 402-denied and were not relaunched or worked around.
The 38 individual command derivations, five Kubernetes refinements and earlier
workload scope remain incomplete; user-directed resolution is needed for full
coverage. Jira issue APIs for all three epics returned 404/no permission; the
browser URL returned only a Jira shell, so actual acceptance text remains unknown.
