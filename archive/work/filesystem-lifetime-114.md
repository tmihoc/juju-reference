# E58: filesystem storage under machine removal

Source: `/tmp/juju-41-tree` at Juju 4.1 commit `e5db99d5854803bd30ab9ea19bf6e16bab9bbcc5`. Paths are relative to that tree unless otherwise identified. The question and threshold were registered in `structure-discovery-plan.md` before this trace.

## Result

**The universal filesystem-lifetime claim fails as a source-level rule.** A real EBS provider can back filesystem storage with a model-scoped volume. In the traced machine-removal path, a unit-hosting machine requires `--force`; Juju schedules removal of that unit's storage attachments but does not select this model-owned instance and its backing resources for destruction. On the successful detachment path, the attachment records can be removed while the storage instance, filesystem record and volume remain. This is a conditional implementation trace, **not a live end-to-end demonstration**: forced removal can outrun provider detachment; cloud persistence, EC2 responses and later reattachment were not exercised.

The distinction is essential: the machine-local mount/attachment is not the storage instance, its filesystem record or its backing EBS volume. E57's rootfs case is machine-scoped; it cannot be generalized to all filesystem storage.

The reference says, unconditionally, “A filesystem storage lives on the machine that hosts the unit and dies with it” (`~/git/misc/juju-tutorial-diagrams/docs/reference/storage.md:14`). The traced EBS path contradicts that as a rule about the Juju filesystem **storage instance and backing volume**. It does not establish that the old mount remains usable on a removed machine. The adjacent claim that unit-owned storage always dies with its owner (`storage.md:75`) is also a candidate overstatement: the traced attachment deletion removes the owner relationship while leaving this instance; no separate unit-removal command audit was performed.

**Proposed replacement for the two lifetime sentences at line 14, not applied:**

> Filesystem storage is mounted on a machine; it can be backed by a volume. Whether a storage instance survives machine removal depends on its backing provider and the removal path.

This deliberately does not promise survival, persistence, cross-machine attachment or data integrity for every provider. The surrounding paragraph and the detailed scope/removal rules remain outside this proposal. Explicit approval is required before changing the page.

## Source trace

### EBS produces volume-backed filesystem storage

1. The EC2 registry returns `ebsProvider` for EBS and recommends its pool for either block or filesystem kind (`internal/provider/ec2/ebs.go:170-198`). Executable methods report support for block only, environment scope, and no filesystem source (`:313-320,360-362`).
2. For a requested filesystem, `CalculateStorageInstanceComposition` maps environment scope to model, then chooses a **machine-scoped filesystem plus model-scoped volume** when only block is supported. `CalculateStorageInstanceOwnershipScope` gives a backing volume precedence, yielding model ownership (`domain/storageprovisioning/provisioning.go:90-138,147-170`).
3. The unit argument path resolves the directive's provider and applies this composition to instance, filesystem and volume creation (`domain/storageprovisioning/unitstorageargs.go:183-265`). `MakeIAASUnitStorageArgs` adds filesystem/volume machine-owner entries only when the composition's overall ownership is machine (`:324-363`). Unit state inserts the provided machine-owner lists (`domain/application/state/unit.go:1439-1448`; `domain/application/state/unitstate.go:1239-1295`). Thus a new EBS filesystem instance from this path has neither machine-owner entry, even though its filesystem provisioning scope is machine.
4. EBS's successful volume-creation code calls EC2 `CreateVolume` and returns volume info marked `Persistent: true`; its description path qualifies persistence when an attachment has `DeleteOnTermination` set (`internal/provider/ec2/ebs.go:449-505,547-578`). This is code behavior, not observation of an actual cloud volume or a guarantee about externally changed cloud configuration.

### The actual machine-removal path

1. `juju remove-machine` passes `force`, `keep`, `dryRun` and wait arguments to the API; `--no-wait` without `--force` is invalid (`cmd/juju/machine/remove.go:89-113,151-200`). The facade checks write access and the remove block, reports a dry run without scheduling removal, and otherwise calls `RemoveMachine` (`apiserver/facades/client/machinemanager/machinemanager.go:441-513`). It classifies affected storage with `destroyStorage=false` for the reported result (`:536-563`); this is reporting, not itself the removal operation.
2. In the state transaction, removal without force is refused if the machine has non-dead units or child machines (`domain/removal/state/model/machine.go:120-156`). With force, it marks the machine/cloud instance and its units not alive, calls the machine-owned storage selection, and cascades units with `destroyStorage=false` (`:158-225`). The machine-owned selection follows a `machine_volume` row when a storage instance has a volume; the filesystem-only branch explicitly excludes instances that also have a volume (`:246-299`). For the normal newly created EBS composition in the previous section, neither machine-owner list contains its backing resources, so this instance is not selected by that query.
3. Unit cascade advances its storage attachments to dying. It calls the owned-instance destruction cascade only when `destroyStorage` is true (`domain/removal/state/model/unit.go:78-112,130-177`). It returns the related filesystem/volume attachment IDs for scheduling (`:180-230`). `RemoveMachine` schedules removal jobs for the returned unit and attachment IDs, and separately schedules instance/filesystem/volume jobs only for resources returned by the respective cascades (`domain/removal/service/machine.go:90-144`). Those instance/backing-resource lists do not include the EBS instance under the stated conditions.
4. The storage-attachment job can make the attachment dead and cascade the backing **attachment** lives before deleting the storage attachment (`domain/removal/service/storage.go:385-475`; `domain/removal/state/model/storage.go:2179-2314`). Deleting the unit attachment also deletes the unit-owner relation when that unit was the owner, but neither statement deletes the storage instance (`domain/removal/state/model/storage.go:409-467`). The filesystem/volume attachment deletion functions delete their attachment rows, not the backing resource rows (`:1485-1512,1719-1746`). Machine deletion waits for the network node's remaining units and storage attachments to disappear even when forced (`domain/removal/state/model/machine.go:502-618,828-908`).
5. If the regular provisioner processes a provisioned dying volume attachment, it schedules a detach operation (`internal/worker/storageprovisioner/volume_events.go:394-430`); that operation calls the provider's `DetachVolumes` and removes the attachment after a successful result (`internal/worker/storageprovisioner/volume_ops.go:358-423`). EBS implements this by calling EC2 `DetachVolume`, not `DeleteVolume` (`internal/provider/ec2/ebs.go:1052-1091`). **Force caveat:** forced attachment jobs may delete a dying attachment without waiting for it to become dead (`domain/removal/service/storage.go:1093-1128,1158-1193`); therefore these code paths do not prove the provider detach runs before force cleanup or machine termination.

The storage instance may be explicitly destroyed in other paths: `RemoveUnit` takes a `destroyStorage` boolean and forwards it to the unit cascade (`domain/removal/service/unit.go:85-107`); the unit cascade then selects owned instances if true (`domain/removal/state/model/unit.go:104-112,261-290`). This does not turn the machine-removal path above into an unconditional survival guarantee.

## Direct real-code exercise

A temporary adapter in package `ec2` constructed the actual otherwise unexported `ebsProvider`; a temporary Go program invoked its real `Supports` and `Scope` methods, `CalculateStorageInstanceComposition`, `CalculateStorageInstanceOwnershipScope` and `MakeIAASUnitStorageArgs`. `go run` returned:

```text
ebs supports filesystem=false block=true scope=0
filesystem=true filesystem_scope=1 volume=true volume_scope=0 ownership_scope=0
machine_owned_filesystems=0 machine_owned_volumes=0
```

Here provisioning scope 0 is model and 1 is machine (`domain/storage/types.go:261-270`); ownership scope 0 is model (`domain/storageprovisioning/scope.go:8-17`). The UUID-like strings used in the last helper were inputs to the ownership-list calculation, not persisted entities. No AWS credentials, cloud API, controller or removal job were used. Both temporary files were removed after execution.

## Limits

The source establishes the conditional lifecycle decision and transition paths; actual cloud data survival, operation completion, ordering under forced removal, normal mount cleanup, provider availability-zone constraints, reattachment and data integrity remain unverified. No provider matrix, complete machine/unit/storage removal audit, permanent test, docs-tree edit or repository-rule edit was made. The physical page location and proposed wording remain unapproved.
