# E57: storage pool, instance and attachment boundaries

Source anchor: `/tmp/juju-41-tree` at `e5db99d5854803bd30ab9ea19bf6e16bab9bbcc5` (Juju 4.1). Registered in `structure-discovery-plan.md` before tracing. References below are paths relative to that tree unless labeled otherwise. This is a bounded static source trace plus the explicitly identified direct-code probe, not a live controller, storage provider operation or documentation change.

## Decision and registered checks

**All three registered predictions are supported on the traced paths, with qualifications.** Keep separately addressable, linked contracts for (1) a model's reusable storage pool, (2) a storage instance and its backing resources, and (3) the storage-instance-to-unit attachment relationship. The attachment's consequences extend to filesystem/volume attachments on a machine's network node. A unit owner is a different relationship from an attachment, but detaching the owner also removes that ownership record. This is a semantic ownership decision, not a decision to create three files, add a page section or promise independent lifecycle under all conditions.

| Criterion registered before tracing | Result | Discriminating evidence |
|---|---|---|
| Pool managed separately from an instance and selected for provisioning | **Pass, qualified:** create/list are available, update/remove are not available at this API version. | Pool facade `apiserver/facades/client/storage/pool.go:58-90,160-215,217-228`; service `domain/storage/service/storagepool.go:110-164`; instance generation `domain/storageprovisioning/unitstorageargs.go:127-142,183-235`. |
| Instance identity/provisioning distinct from a particular attachment | **Pass for the traced path:** a storage ID resolves an instance; attach resolves that existing instance, and the removal job deletes an attachment without deleting that instance. It is not a universal survival guarantee for unit removal or storage destruction. | Identity `domain/application/state/unitstate.go:1399-1428`, lookup `domain/storage/state/instance.go:254-290`; attach `apiserver/facades/client/storage/attach.go:38-75`; detach `domain/removal/service/storage.go:258-317,385-475`, `domain/removal/state/model/storage.go:409-467`. |
| Attachment has its own relationship contract | **Pass:** one storage/unit pair is validated and inserted, and one or all of an instance's attachment relationships can be scheduled for removal. | `domain/application/service/unit.go:390-445,470-535,552-584`; `domain/application/state/storage.go:1567-1640`; `apiserver/facades/client/storage/detach.go:45-50,70-113,157-222,228-274`. |

**Competing placements.** One undifferentiated storage contract would conflate reusable configuration, individual identity and per-unit transitions. A pool plus instance-only organization still needs an address for attachment's unit-dependent checks, asynchronous removal and machine-side consequences; attaching those rules only to the instance or only to the unit hides the other participant. Three linked *semantic* addresses preserve those differences. The prior E52 map already proposes storage-pool and storage-instance anchors plus a storage-attachment anchor in `storage.md` and a unit link (`work/subject-map-112.md:41-42`); this trace strengthens and qualifies that map, but does not change its ownership or justify a separate delta file.

## Trace

### Pool: reusable model configuration

The client sends `ListPools`, `CreatePool`, `RemovePool`, and `UpdatePool` facade calls (`api/client/storage/client.go:73-139`). `CreatePool` checks model write access and processes each requested pool; it passes name, provider type and attributes to `CreateStoragePool` (`apiserver/facades/client/storage/pool.go:58-90`). That service validates the name, looks up the provider in the model's registry, validates its configuration, creates a pool UUID, and stores user-origin configuration (`domain/storage/service/storagepool.go:110-164,225-304`). Listing checks read access, selects a service listing path and returns name, provider and attributes (`apiserver/facades/client/storage/pool.go:160-215`).

**Important limit:** `UpdatePool` and `RemovePool` return `CodeNotYetAvailable` directly (`apiserver/facades/client/storage/pool.go:217-228`). Domain service methods to replace/delete pools exist (`domain/storage/service/storagepool.go:332-367,373-416`), but they are not the implementation of these facade calls. Do not infer client functionality from their existence, nor infer effects on already provisioned storage from a hypothetical update.

### Instance: identity and provider-backed provisioning

A unit storage directive carries a pool UUID and a desired count. The new-unit path generates that count of instance arguments, resolving the pool provider, calculating its required volume/filesystem composition, and assigning each instance its own UUID and the same selected pool UUID (`domain/storageprovisioning/unitstorageargs.go:127-142,183-235`). The state creation path allocates a sequence-based user-facing ID from the storage name, then persists that ID, UUID, kind, requested size and pool; it separately inserts and links any required filesystem and/or volume (`domain/application/state/unitstate.go:1035-1051,1070-1113,1129-1186,1399-1428`). The instance ID lookup is independent of any unit attachment lookup (`domain/storage/state/instance.go:254-290`).

For the **volume** path specifically, provisioning parameters join the volume to its instance and the selected pool and retrieve the pool's provider type and attributes (`domain/storageprovisioning/state/volume.go:1289-1392`). The agent facade obtains those parameters (`apiserver/facades/agent/storageprovisioner/storageprovisioner.go:1527-1577`); the storage provisioner validates the parameters, calls the provider's `CreateVolumes`, and publishes successful volume information (`internal/worker/storageprovisioner/volume_ops.go:19-101`). This is a static trace of a path, not evidence that a cloud volume was actually created.

### Attachment: relationship and lifecycle, not the instance itself

`Attach` checks model write access and the model change block (`apiserver/facades/client/storage/attach.go:20-35`). It resolves the unit and existing storage ID separately before calling the application service (`:38-75`). The service checks life, charm identity, storage kind, minimum size, count, sharing and machine compatibility (`domain/application/service/unit.go:390-445,470-535,538-584`). Its transaction rechecks the instance and attachment expectations, then inserts unit storage attachments and may set the instance's charm name (`domain/application/state/storage.go:1567-1640`). Thus the relationship has independent conditions, but attaching is not necessarily a write to the relationship alone.

`DetachStorage` checks model write access and resolves either one storage/unit pair or all attachments when no unit tag is supplied (`apiserver/facades/client/storage/detach.go:45-50,70-113,157-222,228-274`). Removal checks the charm's required minimum for an alive unit, makes the storage attachment non-alive and schedules a removal job; corresponding filesystem/volume attachment or attachment-plan jobs may also be scheduled (`domain/removal/service/storage.go:258-317,320-358`; `domain/removal/state/model/storage.go:2399-2495`). The job waits for a dead attachment unless forced, then deletes the attachment (`domain/removal/service/storage.go:385-475`). The deletion transaction also deletes the unit-owner record **if the detached unit is the owner**, but does not delete the storage instance (`domain/removal/state/model/storage.go:409-467`). A successful request schedules work; it is not proof the physical detach has completed. Force, asynchronous failures and multi-attachment behavior were not exercised live.

**Example, deduced from source:** if a directive selects pool `fast` and requests two stores, the argument-generation loop makes two distinct instance UUIDs with the same pool UUID. A later valid detach request for one of those instances and one unit schedules removal of that relationship; it does not request deletion of the pool or the other instance. Whether the request is allowed, and whether the backing storage can later be used elsewhere, depends on the charm, instance, machine and provider conditions above; no live example was run.

### One concrete provider limit: rootfs

The real `rootfs` provider supports filesystems but not block storage and reports machine scope (`internal/storage/provider/rootfs.go:69-95`). Composition rejects a provider that cannot support the requested kind (`domain/storageprovisioning/provisioning.go:71-138`); this is why pool selection cannot imply that every kind works. For unit-removal classification the code uses a backing volume's scope in preference to filesystem scope, if both exist; it classifies storage as detached only when the calculated ownership scope is model and destruction was not requested (`domain/storageprovisioning/provisioning.go:147-170`; `domain/storage/service/instance.go:128-167,215-245`). This is classification source, not a demonstrated successful reattachment or a complete description of unit removal.

A possible documentation issue is the unconditional statement that filesystem storage dies with its host machine (`~/git/misc/juju-tutorial-diagrams/docs/reference/storage.md:14`): the composition/classification code distinguishes backing-volume scope rather than simply filesystem versus block. This is a **candidate for a separate provider-specific trace**, not a proven live counterexample or authorization to edit the page.

## Executed direct-code probe

A temporary Go program in the source worktree called the real `provider.NewRootfsProvider(nil)` and `CalculateStorageInstanceComposition`, then directly called `UpdatePool` and `RemovePool` on a nil `*StorageAPI` receiver; these methods do not dereference the receiver. `go run` printed:

```text
rootfs kind=filesystem composition={FilesystemProvisionScope:1 FilesystemRequired:true VolumeProvisionScope:0 VolumeRequired:false} error=<nil>
rootfs kind=block composition={FilesystemProvisionScope:0 FilesystemRequired:false VolumeProvisionScope:0 VolumeRequired:false} error=provider does not support storage kind
update error=not yet available in 4.1-beta3
remove error=not yet available in 4.1-beta3
```

`ProvisionScopeMachine` is 1 (`domain/storage/types.go:261-270`). The probe exercised composition and the facade methods directly, not RPC routing, permissions, a controller, filesystem creation or live provider infrastructure. The temporary program was removed after the run.

## Limits and next discriminating question

No full provider matrix, full command/error audit, live controller, provider, charm hook, physical mount or removal job was exercised. Pool update/remove were checked only at the traced facade; no universal claim about every internal service caller follows. The trace does not prove that all detached instances survive all unit or model removals, that all provider resources are portable, or that attachments can always be shared. It does not establish reader findability, a unique physical file split or full subject-map coverage.

A useful next bounded investigation is the candidate filesystem-lifecycle claim: trace a real model-scoped volume-only provider through filesystem composition and the actual machine-removal path, distinguishing a mount's lifetime from its backing storage's lifetime. Register that probe before tracing; do not generalize from the rootfs case.
