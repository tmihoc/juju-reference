# `add-machine --disks`: version and execution trace

Source anchor `/tmp/juju-41-tree` at `e5db99d5854803bd30ab9ea19bf6e16bab9bbcc5`.
This research is not an approved source or documentation fix. The source trace
and synthetic real-code exercise below establish a dropped-input defect at the
facade/service boundary for v11/v12, not a live cloud allocation result.

## Current path and version

The CLI accepts `--disks`, parses storage directives and places them into each
`AddMachineParams` (`cmd/juju/machine/add.go:190-195,341-353`, `flags.go:19-28`).
The client transmits them via `AddMachines` (`api/client/machinemanager/machinemanager.go:49-65`);
the JSON request has a `disks` field (`rpc/params/params.go:211-221`). The
client advertises versions 10, 11 and 12 (`api/facadeversions.go:65-68`); this
server registers 11 and 12, with v11 embedding the same implementation used by
v12 (`apiserver/facades/client/machinemanager/register.go:17-41`,
`machinemanager.go:42-46`).

The facade checks write access and a change block for the whole request before
processing each item; `addOneMachine` never reads `p.Disks` and constructs
`AddMachineArgs` without it (`machinemanager.go:116-134,139-230`). That type
has no disk field (`domain/machine/types.go:56-79`). The real provider service
merges and passes constraints to state after provider precheck
(`domain/machine/service/provider.go:178-219,248-283`); the discarded disk
requests cannot be recovered from those service arguments. Successful machine
acceptance is not provider completion. The manual/SSH CLI branch is separate
and its provisioning arguments also do not include `c.Disks`
(`cmd/juju/machine/add.go:310-315,396-431`); it was not exercised.

`root-disk` and `root-disk-source` are different constraint fields, not the
additional-disk directives. They survive the traced merge and can later feed
provider boot-disk allocation (`work/storage-machine-boundary-126.md`). Do not
conflate the two or assume the lost directives can be recovered by that path.

Version 10 is an older-server compatibility path, not a handler supplied by the
anchored server. In the inspected Juju 3.6.11 revision
[`17876b918429f0063380cdf07dc47f98a890778b`](https://github.com/juju/juju/blob/17876b918429f0063380cdf07dc47f98a890778b/apiserver/facades/client/machinemanager/machinemanager.go#L267-L319),
the v10 handler iterates `p.Disks`, rejects zero count and constructs host-volume
parameters for the machine template; state uses those volumes in host-storage
operations. This is source evidence for that revision, not an exercised v10
request or a claim about every 3.6 release.

## Executed probe

A throwaway program in a temporary source copy exercised the real directive
parser, version intersection, MachineManager client, v11/v12 facade and real
machine `ProviderService`. It manually JSON-round-tripped and dispatched
requests; authorization, block service, provider, state and status history were
synthetic. It did not use real RPC transport, a persistent database, a live
controller or cloud. The temporary source copy and probe were removed.

Both server-version sets `[11 12]` and `[11]` negotiated v12 and v11
respectively. For each, a four-item batch included a baseline without disks,
an `ebs` directive, a different synthetic `boguspool` directive and an invalid
parent/container input. The real client sent the directive variants. Selected
verbatim output for v12 was:

```text
server-versions=[11 12] client-negotiated=12
batch call-error=<nil> code="" result-count=4
  item[0] machine="0" error=<nil> code=""
  item[1] machine="1" error=<nil> code=""
  item[2] machine="2" error=<nil> code=""
  item[3] machine="" error="parent machine specified without container type" code=""
  wire[0] disks=[] root-disk=20480 root-source=pd-ssd
  wire[1] disks=[{Pool:ebs Size:1024 Count:2}] root-disk=20480 root-source=pd-ssd
  wire[2] disks=[{Pool:boguspool Size:2048 Count:1}] root-disk=20480 root-source=pd-ssd
  real-service calls=3 args-equal-baseline/ebs=true args-equal-baseline/bogus=true state-calls=3 state-args-equal=true provider-prechecks=3 history-calls=6
  state-boundary root-disk=20480 root-source=pd-ssd precheck root-disk=20480 root-source=pd-ssd
```

V11 produced the same item results and service/state comparisons. The synthetic
provider did not validate pool existence. Thus on this exercised successful
path, disk input was ignored at service and state boundaries despite an
accepted machine result. The separate root-disk constraints survived.

The probe also returned whole-call unauthorized and operation-blocked errors
for synthetic guard failures; a synthetic provider-precheck failure appeared in
one item result with an empty code. The local directive parser rejected two
sizes: `storage size is already set to 1024, new value 2048 not valid`. These
are bounded synthetic checks, not an exhaustive errors contract. No permanent
test was added.

## Consequences and limits

This is a concrete implementation/contract defect candidate, stronger than the
previous source-only suspicion. Do not document the requested disks as created,
or present a machine ID as proof of successful disk or machine provisioning.
Investigate intended behavior and an appropriate source fix before changing
reference prose; no fix is authorized here. The CLI's syntax and local parser
remain distinct from API authorization, per-item results and later provider
status. Existing global template checking cannot prove those associations.

No live controller, actual registry transport, database, manual/SSH execution,
provider or cloud was exercised. The synthetic `boguspool` name is not evidence
of a real missing pool; v10 was read, not executed. Provider/version differences,
the separate storage Import leads, all existing defects and four denied scopes
remain open. No page, source, diagram, rule, checker, selected counter or PR
was changed.
