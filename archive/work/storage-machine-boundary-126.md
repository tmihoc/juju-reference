# E75/E76: storage pools across machine and managed-storage paths

Research only; not an approved page, figure, rule or tool edit. Source anchor:
`/tmp/juju-41-tree` at `e5db99d5854803bd30ab9ea19bf6e16bab9bbcc5`.
E75 and E76 were registered in `structure-discovery-plan.md` before the
respective new traces. Previously studied storage paths make the comparison
contaminated, not held-out or reader testing. E44 did not establish reader
benefit; E59 failed its original threshold.

## E75: machine root-disk policy

**Result:** a pool can affect a supported non-charm machine boot-disk request,
not just charm storage-instance creation or adoption. This strengthens a
cross-subject pool character hypothesis and falsifies the strong claim that its
only effective use is charm storage. It does not rule out a storage-wide leg:
a machine's root disk is also storage. Neither classification is settled.

| Step | Bounded source evidence |
|---|---|
| Entry | `add-machine` takes `--constraints`; the client parses them and puts them in `AddMachineParams` (`cmd/juju/machine/add.go:190-195,282-285,341-353`). The facade checks model write and a change block for the whole call, then handles each machine separately and passes its constraints to the service (`apiserver/facades/client/machinemanager/machinemanager.go:116-134,215-225`). Local `juju help add-machine` ran; no controller ran. |
| Merging | The service merges machine and model constraints with the provider's validator, prechecks the instance, and saves the merged value on the machine (`domain/machine/service/provider.go:178-219,248-283`). Success here is a machine record, not provider completion. |
| Pool resolution | The provisioning read obtains the machine's constraints and looks up a pool by `root-disk-source` name with its attributes; no matching row returns nil (`domain/provisioner/state/model/state.go:91-107,130-134,644-690`). The service builds root-disk parameters containing provider and attributes (`domain/provisioner/service/service.go:251-266,570-587`); the compute provisioner adapter and task pass them with constraints to `StartInstance` (`internal/worker/computeprovisioner/provisioner_adapters.go:705-739`; `internal/provisionertask/provisioner_task.go:1027-1046,1641-1654,1499-1510`). These are source traces, not execution of that chain. |
| GCE provider | `StartInstance` calls `startInstance`, which passes root-disk parameters and constraints to `getDisks` before submitting `AddInstance` (`internal/provider/gce/environ_broker.go:30-45,229-237,284-312`). With a resolved pool and nonempty string `disk-type`, the helper validates and uses it; with no resolved pool it instead interprets the source as a GCE disk type. Local SSD and legacy-machine hyperdisk are rejected; unrecognized values produce different source-level errors for pool attribute versus direct source (`:351-417`). The GCE provider's pool `ValidateConfig` returns nil (`internal/provider/gce/disks.go:73-80`); this does not prove all requests reach provider allocation or succeed. |
| Comparator | On this same machine request GCE uses `instance-role` as a service-account choice and otherwise falls back to a project default, with a separate controller credential/bootstrap precedence (`environ_broker.go:166-205`). That choice concerns machine credentials rather than boot disk policy. The comparison shows different responsibilities and timing, not a mechanical character/leg rule. |

Example: a machine request with `root-disk-source=pool-fast` can resolve a
model pool with `disk-type=pd-ssd` and supply that attribute to the GCE boot
request. A source with no matching pool is instead interpreted as a GCE disk
type. Pool names and literal types can therefore collide; the lookup takes
precedence on this path. A present pool without a nonempty string disk type
skips that direct-source fallback. Provider-type compatibility on this route is
not established; do not infer universal fallback or cross-provider behavior.

## E76: distinct lifecycles and common policy

**Result:** the strong unified managed-storage-instance prediction is weakened
on these GCE traces. Boot disk configuration is inline in a machine instance
request (`environ_broker.go:365-375`); the separate managed-volume path uses
`CreateDisks`, then attaches to a running instance and returns a volume and
attachment (`disks.go:253-273,291-336`). `DetachStorage` instead selects a
Juju storage tag and, optionally, a unit and resolves their attachment
(`apiserver/facades/client/storage/detach.go:45-113,157-216`). This does not
prove root disks are invisible through every supported Juju inspection surface.

The registered end-to-end machine-deletion criterion is only partially met:
the worker/removal-service route to `StopInstances` was not traced. The provider
request comparison supports the narrower distinction above, not an observed
machine-deletion outcome.

The boot request sets `AutoDelete: true`; GCE `StopInstances` requests deletion
of instances and the connector waits on the delete operation
(`environ_broker.go:365-375,489-499`; `internal/provider/gce/internal/google/instance.go:125-149,157-184`).
Managed volume destruction instead resolves a volume ID and calls `RemoveDisk`
(`disks.go:339-340,361-384`). This is request-level source evidence, not a
claim of completed removal, cloud retention, force behavior or that every
machine-removal route invokes `StopInstances`.

Both GCE paths interpret the pool's `disk-type`, reject local SSD, and disallow
hyperdisk on legacy series (`environ_broker.go:383-395`; `disks.go:232-249,275-288`).
This is an actual shared provider policy across different allocation paths, not
merely a repeated name. Conditions and errors differ: root-disk validation is
inside machine start, whereas volume creation processes per-volume errors and
may return a whole-call credential failure (`disks.go:165-209`). This supports a
pool contract shared across machine and managed storage; it does not establish
a provider-independent shared rule or prove whether a storage umbrella can
adequately encompass both. Classification remains unresolved. Next investigate
a supported pool interaction that changes an existing policy's effects or
binding across consumers, if one exists; preregister first and do not infer
absence from an unsupported operation or limited search.

## Connected candidate and selected-page delta

The connected candidate and all other dispositions remain as in
`storage-structure-124.md:50-94`. Update only these proposed relationships:

| Selected page | Evidence-driven delta, not completed content |
|---|---|
| constraint | Link `root-disk-source` to pool policy and machine/provider behavior; preserve provider-specific literal-source alternatives and precedence, rather than saying every value denotes a pool. |
| machine | Link the root-disk allocation request to the pool and GCE provider policy, distinct from managed storage attachment; no assumption of live provision or removal. |
| storage | Pool policy participates both in root-disk allocation and managed storage; link machine and constraint alongside application/unit. Keep the pool-character versus storage-leg classification unresolved. |
| cloud | GCE-specific pool attribute validation, literal fallback and boot request can be described only with the traced conditions; other providers remain untraced here. |

E71 remains ten previously studied outline passes and one unresolved, not
finished pages or held-out evidence. No new page arrangement is settled.

## Error and figure preparation

**JUJU-10586.** `AddMachines` can return whole-call authorization/change-block
errors before per-machine results, while the later machine provisioning path
may record a provider start error as machine status rather than return it in
that earlier call (`machinemanager.go:116-134`; `provisioner_task.go:1460-1468,1499-1510`).
GCE `getDisks` generates `NotValidf` for local SSD, an invalid pool attribute
or unrecognized direct source, and `NotSupportedf` for a legacy-series
hyperdisk; exact final status rendering, client-visible code, version negotiation
and actionable provider-specific remediation are not established. Do not file
these as synchronous AddMachines API errors. Existing global message checking
cannot prove the association; the call/status transition and negative drift
fixtures remain approval-gated.

**JUJU-9635.** The existing storage schema view selects storage pools,
instances and attachments (`docs/juju.ggarch:4837-4845`), not the GCE boot
request; the machine schema selects machine and related records, not pool
resolution (`docs/juju.ggarch:3661-3664`, `docs/reference/machine.md:16-24`).
A future, approved behavioral view could distinguish request, persisted
constraints, pool-or-literal choice, provider validation and asynchronous
status; neither schema alone proves these steps or cloud success. Examine the
existing provisioning behavior and contributor process before deciding whether
any new view is warranted. The storage and credential composite-key model
mismatches remain hidden-field issues, not demonstrated visible wrong markers.

## Pending source questions

`add-machine --disks` is supplied by the CLI and sent by the API client, but
`addOneMachine` as traced does not pass `p.Disks` to `AddMachineArgs`
(`cmd/juju/machine/add.go:341-353`; `api/client/machinemanager/machinemanager.go:49-56`;
`apiserver/facades/client/machinemanager/machinemanager.go:139-230`). This is a
potential ignored-input discrepancy, not a live failure or proof no other path
handles it; trace the full facade/version and exercise it before any proposed
correction. It is separate from the root-disk constraint path above.

## Verification and limits

`go run ./cmd/juju help add-machine` exercised local help. An attempted CLI
`add-machine` with duplicate source constraints stopped at `No controllers
registered` before reaching the intended parser; it did not exercise allocation.
A throwaway Go program invoked the real `constraints.Parse`: one source was
accepted and duplicate sources returned `bad "root-disk-source" constraint:
already set`. It did not exercise the machine facade or GCE provider. The
program was removed. No live controller, API, agent, provider, deletion or cloud
ran; no reference page, diagram, checker, rule, PR or production source changed.
Four 402-denied scopes remain blocked and were not replaced or relaunched.
