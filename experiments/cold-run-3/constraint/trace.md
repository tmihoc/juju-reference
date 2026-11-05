# Trace of the draft to the 4.1 source at 52e983a435

Paths are relative to the repository root at 52e983a435. "UP" is an upstream doc statement at the same commit. Verdict: T traced, TU traced to upstream doc only, U unverifiable (dropped or marked), P partial.

## Lede

| # | Statement | Source | Verdict |
|---|---|---|---|
| L1 | A constraint is a key-value pair stating a requirement for a compute resource | core/constraints/constraints.go:48-51 (Value), 134-136, 550-592 (name=value); UP docs/reference/constraint.md:10 | T |
| L2 | Compute resource kinds: bare metal, VM, system container, Kubernetes container | UP docs/reference/constraint.md:10; docs/reference/resource-compute.md (machines and Kubernetes containers) | TU |
| L3 | Set for a model, application, machine, or controller machines | domain/application/service/provider.go:964-971 (model+app); domain/machine/service/provider.go:253-267 (machine+model); cmd/juju/commands/bootstrap.go:938-942, 89-90 (controller) | T |
| L4 | Sixteen constraint keys | core/constraints/constraints.go:23-41 (16 key constants, `cpuCores` is an alias) | T |
| L5 | Each cloud supports some of them | the `unsupportedConstraints` lists (see key entries) | T |

## Constraint syntax

| # | Statement | Source | Verdict |
|---|---|---|---|
| S1 | key=value pairs separated by spaces | constraints.go:434-459 (split on spaces), 541-547 | T |
| S2 | Space inside a value is written backslash-space | constraints.go:439-443, 346-348 | T |
| S3 | List-valued keys take comma-separated items | constraints.go:886-894 (parseCommaDelimited) used by setTags/setSpaces/setZones 764-811 | T |
| S4 | Example `arch=arm64 mem=8G tags=virtual,^dualnic` parses | arch 697-706, mem 740-746 + 868-884, tags 764-770; example tags from UP constraint.md:102 | T |
| S5 | `juju` client takes constraints in bootstrap, deploy, add-machine, set-constraints, set-model-constraints | cmd/juju/commands/bootstrap.go:351-352; cmd/juju/application/deploy.go:647; cmd/juju/machine/add.go:194; cmd/juju/application/constraints.go:101-109,166-175 | T |
| S6 | `constraints` and `model-constraints` show the stored sets | cmd/juju/application/constraints.go:26-28, 54; cmd/juju/model/constraints.go:85 | T (application and model scope) |
| S7 | `malformed constraint "<pair>"`; trigger: no `=` or empty key | constraints.go:541-547 (`eq <= 0`) | T (message as raised; client wrapper not traced) |
| S8 | `unknown constraint "<key>"` | constraints.go:585-587 | T (same caveat) |
| S9 | `bad "<key>" constraint: already set`, repeated key or key plus alias | constraints.go:451-455 (alias resolved before setRaw), 591; setters e.g. 708-714, 22 occurrences of `already set` | T (same caveat) |
| S10 | Remediations (write key=value; use a key; keep one pair) | derived from the triggers; no source text | judgment, not a source claim |

## Levels and precedence

| # | Statement | Source | Verdict |
|---|---|---|---|
| V1 | Application constraints overlay the model's constraints | domain/application/service/provider.go:964-971 (Merge(model, app)); cmd/juju/application/constraints.go:50-53 (help text) | T |
| V2 | Machine constraints overlay the model's | domain/machine/service/provider.go:248-267 | T |
| V3 | Bootstrap constraints overlay the model's for the first controller machine | cmd/juju/commands/bootstrap.go:938-942 (Merge(model, bootstrap)) | T |
| V4 | Bootstrap constraints also apply to controller machines added later for HA | cmd/juju/commands/bootstrap.go:89-90 (help text); the enable-ha code path was not traced | P (help text only) |
| V5 | Overlay works key by key; model-only keys stay | core/constraints/validation.go:336-346 (withFallbacks), 376-387 | T |
| V6 | A key of the specific level removes conflicting keys of the model | validation.go:375-384 (Merge, `without`) | T |
| V7 | Conflicts depend on the cloud | validation.go:82-89 (RegisterConflicts per validator); providers register different sets (see instance-type) | T |
| V8 | EC2: instance-type removes model's arch, cores, cpu-power, mem | internal/provider/ec2/environ.go:281-283 | T |
| V9 | Two conflicting keys in one set fail with `ambiguous constraints: "<key>" overlaps with "<other key>"` | validation.go:166-193 (lines 185, 189) | T (the application path swallows a Validate error when any unsupported key is present: domain/application/service/provider.go:992-998; see notes) |
| V10 | Remediation: remove one of the two keys | derived | judgment |
| V11 | EC2 and Azure allow arch with instance-type when the architecture matches | ec2/environ.go:296-320; azure/environ.go:487-511 | T |
| V12 | Neither application nor model sets arch: machines of the application get amd64 | domain/application/service/provider.go:974-979; core/arch/arches.go:16-18 | T |

## Cloud support

| # | Statement | Source | Verdict |
|---|---|---|---|
| C1 | Unsupported constraint does not fail the request; Juju logs `unsupported constraints: <keys>` | domain/application/service/provider.go:992-996; domain/machine/service/provider.go:272-281; cmd/juju/commands/bootstrap.go:947-954 | T |
| C2 | Value not accepted fails with `invalid constraint value: <key>=<value>` plus line `valid values are: ...` | validation.go:234-246 | T |
| C3 | Remediation: use a listed value | derived | judgment |
| C4 | Cloud pages list the supported keys; anchors | UP docs/reference/cloud/list-of-supported-clouds/*.md (ec2-machine-constraints amazon-ec2.md:243, gce google-gce.md:188, lxd lxd.md:190, maas maas.md:140, azure microsoft-azure.md:198, openstack openstack.md:215, oci oracle-oci.md:153, unmanaged unmanaged.md:177, vsphere vmware-vsphere.md:282, kubernetes reuse/k8s/constraints.md:7) | TU |

## Minimums and maximums

| # | Statement | Source | Verdict |
|---|---|---|---|
| M1 | Four keys state a quantity: cores, cpu-power, mem, root-disk | constraints.go:61-79 (uint64 quantities), 52-132 (all other keys are string, list, bool, enum) | T |
| M2 | Each is defined as a minimum | constraints.go:61-79 ("at least"); internal/provider/maas/constraints.go:54-59 (MinCPUCount, MinMemory) | T (definition; per-cloud implementation traced for MAAS only) |
| M3 | Other keys select a value, set, or option; none is a min or max | constraints.go:52-132 | T |
| M4 | LXD, containers and VMs: cores and mem are limits | internal/container/lxd/container.go:58-63 (limits.cpu, limits.memory); internal/provider/lxd/environ_broker.go:205-214 (same spec for VMs) ; UP lxd.md:185 | T |
| M5 | LXD: root-disk sets the root disk size | container.go:68-89 | T |
| M6 | Kubernetes: mem and cpu-power are request and limit of each workload container | internal/provider/kubernetes/application/constraints.go:33-42, 331-374 (V2 excludes the charm container) | T |
| M7 | Units: mem in MiB, cpu-power in milli-CPU | kubernetes/application/constraints.go:34, 39 (`%dMi`, `%dm`) | T |

## Key entries

| # | Statement | Source | Verdict |
|---|---|---|---|
| K1 | allocate-public-ip: addresses reachable from outside the cloud's virtual network | constraints.go:115-119; UP constraint.md:30 | T |
| K2 | Valid values true, false | constraints.go:844-854 (ParseBool; empty ignored 813-816); UP :30 | T (strconv accepts more spellings; page lists the canonical two) |
| K3 | Azure, GCE, OCI public address without the constraint | azure/environ.go:762-767; gce/environ_broker.go:239-242; oci/environ.go:569-572 | T |
| K4 | OpenStack floating IP only when true | openstack/provider.go:1381-1386 (`withPublicIP` false by default) | T |
| K5 | EC2 removes the public address from the first NIC when false | ec2/environ.go:750-765 | T |
| K6 | Unsupported: EC2, Kubernetes, LXD, MAAS, unmanaged, vSphere | ec2/environ.go:270; kubernetes/constraints.go:18; lxd/environ_policy.go:33; maas/constraints.go:22; unmanaged/environ.go:331; vsphere/environ_policy.go:82 | T |
| K7 | Non-boolean fails `must be 'true' or 'false'` | constraints.go:849 (message) wrapped by 591 | T |
| K8 | arch: valid values five | core/arch/arches.go:53-68; constraints.go:697-706 | T |
| K9 | Azure, EC2, OCI accept amd64, arm64 | azure/environ.go:471-474; ec2/environ.go:277-280; oci/environ.go:326 | T |
| K10 | vSphere amd64 | vsphere/environ_policy.go:92-94 | T |
| K11 | LXD and MAAS: architectures the server reports (intersection with Juju's five) | lxd/environ_policy.go:46-51; maas/constraints.go:35-40 | T |
| K12 | Unmanaged: architecture of the host | unmanaged/environ.go:339-349 | T |
| K13 | Kubernetes arch selects nodes | kubernetes/application/constraints.go:44-68 | T |
| K14 | Non-listed arch fails `bad "arch" constraint: "<value>" not recognized` | constraints.go:701-703, 591 | T |
| K15 | container: states container type | constraints.go:58-59 | T (intent comment; no 4.1 code was found that acts on it: grep of `HasContainer`, `.Container` shows no reader outside core/constraints, state, and add-machine) |
| K16 | Valid values lxd, none, empty accepted | core/instance/container.go:13-15, 25-30; constraints.go:675-690 | T |
| K17 | juju client rejects it in add-machine with the quoted message | cmd/juju/machine/add.go:200-203 | T |
| K18 | Machine-level constraints do not use the key | domain/machine/service/provider.go:248-252, 286-296 | T |
| K19 | Unsupported: Kubernetes, LXD, OCI | kubernetes/constraints.go:15; lxd/environ_policy.go:32; oci/environ.go:315 | T |
| K20 | Bad value: `invalid container type "<value>"` | core/instance/container.go:40; constraints.go:591 | T |
| K21 | cores: number of effective CPU cores, non-negative integer | constraints.go:61-63, 856-866 | T |
| K22 | Alias cpu-cores | constraints.go:26-27, 134-136 | T |
| K23 | Alias deprecated; client warns | cmd/juju/common/flags.go:158-163 (`Warning: constraint "cpu-cores" is deprecated in favor of "cores".`) | T |
| K24 | Kubernetes lists cores unsupported | kubernetes/constraints.go:13 | T |
| K25 | Bad cores: `must be a non-negative integer` | constraints.go:861 | T |
| K26 | cpu-power: abstract, non-negative integer, 100 = one Amazon ECU, roughly a 2007-era Xeon | constraints.go:65-68, 716-722 | T |
| K27 | Kubernetes unit milli-CPU | kubernetes/application/constraints.go:38-39 | T |
| K28 | Unsupported: Azure, LXD, MAAS, OpenStack, unmanaged | azure/environ.go:451; lxd/environ_policy.go:30; maas/constraints.go:20; openstack/provider.go:598; unmanaged/environ.go:327 | T |
| K29 | cores unsupported only on Kubernetes, so supported on every machine cloud | grep of all `unsupportedConstraints` lists (10 providers): `constraints.Cores` appears only in kubernetes/constraints.go:13 | T |
| K30 | image-id: identifier of the image the machine boots | constraints.go:121-124 | T |
| K31 | Supported by EC2, GCE, MAAS, OpenStack | not in their unsupported lists; read at ec2/environ.go:634, gce/environ_broker.go:83, maas/environ.go:1020, openstack/provider.go:1120 | T |
| K32 | Unsupported: Azure, Kubernetes, LXD, OCI, unmanaged, vSphere | azure/environ.go:454; kubernetes/constraints.go:19; lxd/environ_policy.go:34; oci/environ.go:318; unmanaged/environ.go:332; vsphere/environ_policy.go:83 | T |
| K33 | Application or model constraints with image-id need an explicit base (deploy base option or model default-base); error text | core/charm/baseselector.go:46-49, 94-101, 147-152; cmd/juju/application/deployer/deployer.go:315 (application or model constraints); environs/config/config.go:303 (`default-base`); UP configuration/list-of-model-configuration-keys.md:366 (anchor) | T |
| K34 | The base names the OS of the image | UP constraint.md:56 | TU |
| K35 | instance-role: EC2 instance profile, Azure managed identity, GCE service account | ec2/environ.go:250-251, 205-223, 811-823; azure/identity.go:23-27, 251-258; gce/identity.go:15-19, gce/environ_broker.go:171-189 | T |
| K36 | instance-type: names come from the cloud, depend on cloud and account | ec2/environ.go:286-295; azure/environ.go:458-478; gce/environ_policy.go:91-99; openstack/provider.go:612-621 | T |
| K37 | Conflicts per cloud (EC2, Azure, GCE, OpenStack lists) | ec2/environ.go:281-283; azure/environ.go:479-486; gce/environ_policy.go:66-85; openstack/provider.go:605-608 | T |
| K38 | Unsupported: Kubernetes, MAAS, unmanaged | kubernetes/constraints.go:16; maas/constraints.go:21; unmanaged/environ.go:328 | T |
| K39 | Use cores, mem, root-disk for portability | UP constraint.md:66 | TU |
| K40 | ip-family: IP family of the machine's NICs; values ipv4, ipv6, dual | constraints.go:126-131; core/network/ipfamily/ipfamily.go:12-21 | T |
| K41 | Azure is the only cloud that acts on it; accepts ipv4, dual | grep of `IPFamily` in internal/provider: only azure/environ.go (299, 512-515, 522-531, 574-610) outside unsupported lists | T (by grep) |
| K42 | No cloud acts on ipv6 | azure/environ.go:512-515 (vocabulary excludes ipv6); all others unsupported or not acting | T |
| K43 | Unsupported: EC2, GCE, Kubernetes, LXD, MAAS, OCI, OpenStack, vSphere; unmanaged accepts without acting | ec2/environ.go:271; gce/environ_policy.go:63; kubernetes/constraints.go:20; lxd/environ_policy.go:35; maas/constraints.go:23; oci/environ.go:319; openstack/provider.go:599; vsphere/environ_policy.go:84; unmanaged/environ.go:326-333 (absent) | T |
| K44 | Azure dual with Basic SKU fails with the quoted message | azure/environ.go:522-531, 588-592 | T |
| K45 | Azure dual fails when subnet has no IPv6 /64 prefix; message | azure/environ.go:598-609 | T |
| K46 | Remediations for K44 and K45 | message texts at azure/environ.go:527, 601 | T |
| K47 | Bad ip-family value message | ipfamily.go:44; constraints.go:832-841 | T |
| K48 | mem: MiB | constraints.go:70-72 ("megabytes"), 912-917 (M = 1), kubernetes `%dMi`, lxd `%dMiB` (container.go:62) | T |
| K49 | Suffix multipliers 1, 1024, 1024^2, 1024^3; `8G` = 8192 | constraints.go:912-917 | T |
| K50 | Suffix uppercase; fraction allowed and rounded up | constraints.go:868-884 (keys of mbSuffixes are uppercase; ParseFloat; math.Ceil) | T |
| K51 | Bad value message | constraints.go:878 | T |
| K52 | root-disk: MiB, same suffixes and error | constraints.go:74-79, 748-754 (parseSize) | T |
| K53 | Separately attached storage does not count | UP constraint.md:87; constraints.go:74-78 (space "in the root disk") | TU |
| K54 | root-disk-source: where root disk is allocated, cloud-dependent | constraints.go:81-85; UP constraint.md:92 | T |
| K55 | LXD: storage pool; default pool when absent | internal/container/lxd/container.go:68-74 | T |
| K56 | OpenStack: local, volume, or storage pool name | openstack/init.go:22-24; openstack/provider.go:729-738 | T |
| K57 | vSphere: datastore | vsphere/environ_broker.go:131-146; constraints.go:81-84 | T |
| K58 | GCE: disk type | gce/environ_broker.go:398-412 | T |
| K59 | Bootstrap: a controller-model storage pool with this name supplies the root disk | internal/provider/common/bootstrap.go:216-228 | T |
| K60 | spaces: comma-separated space names | constraints.go:101-105, 772-782 | T |
| K61 | Plain name = connected; `^` name = not connected | constraints.go:101-104 ("available (or not)"); domain/provisioner/service/service.go:307-308; maas/constraints.go:92-115 | T |
| K62 | Example `spaces=storage,db,^logging,^public` | UP constraint.md:97 | TU |
| K63 | Kubernetes lists spaces unsupported | kubernetes/constraints.go:17 | T |
| K64 | Invalid name message | constraints.go:784-795 | T |
| K65 | tags on MAAS: has / not has | maas/constraints.go:60-67, 101-115 | T |
| K66 | tags on Kubernetes: key=value labels, node affinity default or `node.`, `pod.`, `anti-pod.`, `topology-key`, `^` excludes | kubernetes/application/constraints.go:70-92, 174-179, 181-235, 237-329 | T |
| K67 | Unsupported: Azure, EC2, GCE, LXD, OCI, OpenStack, unmanaged, vSphere | azure/environ.go:452; ec2/environ.go:266; gce/environ_policy.go:61; lxd/environ_policy.go:31; oci/environ.go:317; openstack/provider.go:597; unmanaged/environ.go:329; vsphere/environ_policy.go:80 | T |
| K68 | virt-type: LXD container, virtual-machine; default container | lxd/environ_policy.go:44; core/instance/virttype.go:43-46; lxd/environ_broker.go:207-214 | T |
| K69 | MAAS virtual-machine composes a VM from a pod | maas/constraints.go:41-42; maas/environ.go:631-644 | T |
| K70 | OpenStack kvm, lxd | openstack/provider.go:622 | T |
| K71 | Unsupported: Azure, EC2, GCE, Kubernetes, OCI, unmanaged, vSphere | azure/environ.go:453; ec2/environ.go:269; gce/environ_policy.go:62; kubernetes/constraints.go:14; oci/environ.go:316; unmanaged/environ.go:330; vsphere/environ_policy.go:81 | T |
| K72 | zones: list of availability zones; machine created in one of them | internal/provisionertask/provisioner_task.go:1064-1071 | T |
| K73 | Valid values depend on the cloud; example `us-east-1a,us-east-1c` | UP constraint.md:110-113 | TU |
| K74 | Bootstrap with no matching zone fails; message | internal/provider/common/bootstrap.go:240-255 | T |
| K75 | Cloud without zones ignores the constraint | common/bootstrap.go:231-237; provisioner_task.go:1073-1075 | T |
| K76 | Zone also a placement directive; directive takes precedence | UP docs/reference/placement-directive.md:57; UP docs/reference/zone.md:14 | TU |

## Statements not traced

None of the draft's statements is left Unverifiable. The effect of the `container` constraint at provisioning is not stated, because no 4.1 code was found that acts on it (K15).
