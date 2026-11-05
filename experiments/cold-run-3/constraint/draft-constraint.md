---
myst:
  html_meta:
    description: "Juju constraints reference: the keys, values, and rules that state the architecture, size, network, and placement of the machines and containers that Juju provisions."
---

(constraint)=
# Constraint

A **constraint** is a key-value pair that states a requirement for a {ref}`compute resource <resource-compute>` that Juju provisions: a bare metal machine, a virtual machine, a system container, or a Kubernetes container. A constraint is set for a {ref}`model <model>`, an {ref}`application <application>`, a {ref}`machine <machine>`, or the {ref}`controller <controller>` machines. There are sixteen constraint keys, and each cloud supports some of them.

(constraint-syntax)=
## Constraint syntax

A set of constraints is written as `key=value` pairs separated by spaces, for example `arch=arm64 mem=8G tags=virtual,^dualnic`. A space inside a value is written as a backslash followed by a space. A key that takes a list takes comma-separated items.

A client writes a set of constraints in this form. For example, the `juju` client takes it in {ref}`command-juju-bootstrap`, {ref}`command-juju-deploy`, {ref}`command-juju-add-machine`, {ref}`command-juju-set-constraints`, and {ref}`command-juju-set-model-constraints`, and shows the stored sets with {ref}`command-juju-constraints` and {ref}`command-juju-model-constraints`.

Parsing a set of constraints fails with these errors:

- `malformed constraint "<pair>"`
  - Trigger: The pair has no `=`, or its key is empty.
  - Remediation: Write the pair as `key=value`.
- `unknown constraint "<key>"`
  - Trigger: The key is neither one of the constraint keys nor an alias.
  - Remediation: Use one of the {ref}`constraint keys <list-of-constraints>`.
- `bad "<key>" constraint: already set`
  - Trigger: The key appears twice in the set, or once under its name and once under its alias.
  - Remediation: Keep one of the pairs.

(constraint-levels)=
## Constraint levels and precedence

The constraints for a new machine are the model's constraints overlaid with the constraints of the level that provisions the machine:

- An application: The application's constraints overlay the model's constraints for the machines of its units.
- A machine that is added directly: The machine's constraints overlay the model's constraints.
- The controller machines: The bootstrap constraints overlay the model's constraints for the first controller machine, and they also apply to the controller machines added later for high availability.

The overlay works key by key. A key set at the more specific level replaces the same key of the model, and the keys that only the model sets stay.

Some keys of a cloud conflict, and which ones depends on the cloud. A key that the more specific level sets removes the keys of the model that conflict with it. For example, on EC2 an `instance-type` set on an application removes the model's `arch`, `cores`, `cpu-power`, and `mem`. Two conflicting keys in one set fail with `ambiguous constraints: "<key>" overlaps with "<other key>"`. Remove one of the two keys. On EC2 and Azure, `arch` may accompany `instance-type` when it names the architecture of that instance type.

When neither the application nor the model sets `arch`, the machines of the application get `amd64`.

(constraint-cloud-support)=
## Cloud support for constraints

A constraint that a cloud lists as unsupported does not fail the request. Juju logs the warning `unsupported constraints: <keys>` and continues.

A value that a cloud does not accept fails with `invalid constraint value: <key>=<value>`, followed by the line `valid values are: <the closest accepted values>`. Use one of the listed values.

The keys that a cloud supports are also listed in the constraints section of its page: {ref}`Amazon EC2 <ec2-machine-constraints>`, {ref}`Google GCE <gce-machine-constraints>`, {ref}`LXD <lxd-machine-constraints>`, {ref}`MAAS <maas-machine-constraints>`, {ref}`Microsoft Azure <azure-machine-constraints>`, {ref}`OpenStack <openstack-machine-constraints>`, {ref}`Oracle OCI <oci-machine-constraints>`, {ref}`unmanaged <unmanaged-machine-constraints>`, {ref}`VMware vSphere <vsphere-machine-constraints>`, and {ref}`Kubernetes <kubernetes-constraints>`.

(constraint-minimum-maximum)=
## Minimums and maximums

Four keys state a quantity: `cores`, `cpu-power`, `mem`, and `root-disk`. Each is defined as a minimum: the machine has at least that many cores, that much CPU power, that much memory, and that much root disk. The other keys select a value, a set, or an option, and none is a minimum or a maximum.

Two kinds of resource read a quantity differently:

- On LXD, for system containers and for virtual machines, `cores` and `mem` are limits, so they are maximums. `root-disk` sets the size of the root disk.
- On Kubernetes, `mem` and `cpu-power` are both the request and the limit of each workload container. `mem` is in MiB and `cpu-power` is in milli-CPU.

(list-of-constraints)=
## Constraint keys

The sixteen constraint keys, in alphabetical order, are:

(constraint-allocate-public-ip)=
### `allocate-public-ip`

`allocate-public-ip` states whether Juju gives each machine an address that is reachable from outside the cloud's virtual network. The valid values are `true` and `false`. Without the constraint, Azure, GCE, and OCI machines get a public address, and OpenStack machines get a floating IP only when the value is `true`. EC2 removes the public address from the first network interface of the machine when the value is `false`. EC2, Kubernetes, LXD, MAAS, unmanaged, and vSphere clouds list it as unsupported. A value other than a boolean fails with `bad "allocate-public-ip" constraint: must be 'true' or 'false'`.

(constraint-arch)=
### `arch`

`arch` is the CPU architecture of the machine. The valid values are `amd64`, `arm64`, `ppc64el`, `s390x`, and `riscv64`. A cloud accepts a subset of them: Azure, EC2, and OCI accept `amd64` and `arm64`, vSphere accepts `amd64`, LXD and MAAS accept the architectures that the server reports, and an unmanaged cloud accepts the architecture of its host. On Kubernetes, `arch` selects the nodes of that architecture. A value that is not one of the five fails with `bad "arch" constraint: "<value>" not recognized`.

(constraint-container)=
### `container`

`container` states the container type of the machine. The valid values are `lxd` and `none`, and an empty value is accepted. The constraints of a directly added machine do not use the key, and the `juju` client rejects it in {ref}`command-juju-add-machine` with `container constraint "<value>" not allowed when adding a machine`. Remove the key from the constraints of the added machine. Kubernetes, LXD, and OCI clouds list it as unsupported. A value that is not one of the two fails with `bad "container" constraint: invalid container type "<value>"`.

(constraint-cores)=
### `cores`

`cores` is the number of effective CPU cores, a non-negative integer. Its alias is `cpu-cores`, which is deprecated: the `juju` client warns that `cores` replaces it. Kubernetes clouds list `cores` as unsupported. A value that is not a non-negative integer fails with `bad "cores" constraint: must be a non-negative integer`.

(constraint-cpu-power)=
### `cpu-power`

`cpu-power` is an abstract amount of CPU power, a non-negative integer. A value of 100 equals one Amazon ECU, which is roughly a single 2007-era Xeon. On Kubernetes the unit is milli-CPU. Azure, LXD, MAAS, OpenStack, and unmanaged clouds list it as unsupported. On machine clouds `cores` is supported everywhere, so use `cores` for a requirement that moves between clouds.

(constraint-image-id)=
### `image-id`

`image-id` is the identifier of the image that the machine boots. Its form depends on the cloud. EC2, GCE, MAAS, and OpenStack support it; Azure, Kubernetes, LXD, OCI, unmanaged, and vSphere clouds list it as unsupported. When the application's constraints or the model's constraints set `image-id`, a deployment needs a base that is chosen explicitly: through the base option of the deploy or through the {ref}`default-base <model-config-default-base>` setting of the model. The base names the operating system that the image holds. Without an explicit base the deployment fails with `base must be explicitly provided when image-id constraint is used`.

(constraint-instance-role)=
### `instance-role`

`instance-role` is the role or profile that the machine takes in the cloud's identity system. EC2 supports it with an instance profile, Azure with a managed identity, and GCE with a service account. The valid values depend on the cloud.

(constraint-instance-type)=
### `instance-type`

`instance-type` is the name of an instance type of the cloud. The cloud supplies the names, so the valid values depend on the cloud and on the account. The conflicting keys depend on the cloud too: on EC2 they are `arch`, `cores`, `cpu-power`, and `mem`; on Azure they are `arch`, `cores`, and `mem`; on GCE they are `container`, `cores`, `cpu-power`, and `mem`; on OpenStack they are `cores` and `mem`. Kubernetes, MAAS, and unmanaged clouds list it as unsupported. For a requirement that moves between clouds, use `cores`, `mem`, and `root-disk` in its place.

(constraint-ip-family)=
### `ip-family`

`ip-family` is the IP address family of the machine's network interfaces. The valid values are `ipv4`, `ipv6`, and `dual`. Azure is the only cloud that acts on the key, and it accepts `ipv4` and `dual`. No cloud acts on `ipv6`. The other clouds are EC2, GCE, Kubernetes, LXD, MAAS, OCI, OpenStack, and vSphere, which list the key as unsupported, and the unmanaged cloud, which accepts the key and does not act on it.

On Azure, `dual` fails with `ip-family=dual requires load-balancer-sku-name=Standard on Azure; Basic SKU is not supported for this configuration` when the load balancer SKU is Basic. Set `load-balancer-sku-name` to `Standard`. `dual` also fails with `subnet "<name>" does not support ip-family=dual: no IPv6 /64 prefix found; add a /64 IPv6 prefix to the subnet or use ip-family=ipv4` when the machine's subnet has no IPv6 /64 prefix. Add the prefix to the subnet or use `ipv4`. A value outside the three fails with `bad "ip-family" constraint: "<value>" not recognized; valid values are "ipv4", "ipv6", "dual"`.

(constraint-mem)=
### `mem`

`mem` is the amount of memory in MiB. A suffix of `M`, `G`, `T`, or `P` multiplies the number by 1, 1024, 1024 times 1024, or 1024 times 1024 times 1024, so `8G` is 8192 MiB. The suffix is uppercase, and the number may have a fraction, which Juju rounds up to a whole MiB. A value that is negative or has another suffix fails with `bad "mem" constraint: must be a non-negative float with optional M/G/T/P suffix`.

(constraint-root-disk)=
### `root-disk`

`root-disk` is the size of the root disk in MiB, written like `mem`, with the same suffixes and the same error. Storage that is attached separately does not count towards it.

(constraint-root-disk-source)=
### `root-disk-source`

`root-disk-source` names where the root disk is allocated, and its meaning depends on the cloud. On LXD it is a storage pool, and the default pool is used when the key is absent. On OpenStack it is `local`, `volume`, or a storage pool name. On vSphere it is a datastore. On GCE it is a disk type. At bootstrap, a storage pool of the controller model that has this name supplies the root disk.

(constraint-spaces)=
### `spaces`

`spaces` is a comma-separated list of {ref}`network space <space>` names. A name states that the machine is connected to that space, and a name with the prefix `^` states that it is not. For example, `spaces=storage,db,^logging,^public` selects machines that are connected to the `storage` and `db` spaces and to neither the `logging` nor the `public` space. Kubernetes clouds list the key as unsupported. A name that is not a valid space name fails with `bad "spaces" constraint: "<name>" is not a valid space name`.

(constraint-tags)=
### `tags`

`tags` is a comma-separated list of tags. On MAAS, a tag states that the machine has it, and a tag with the prefix `^` states that it does not. For example, `tags=virtual,^dualnic`. On Kubernetes, each tag is a label in the form `key=value`, and Kubernetes schedules the pod by it. A tag without a prefix, or with the prefix `node.`, is a node affinity. The prefix `pod.` makes it a pod affinity and the prefix `anti-pod.` a pod anti-affinity, and a tag `topology-key=<label>` sets the topology key of those affinities. A prefix `^` before the tag excludes it. Azure, EC2, GCE, LXD, OCI, OpenStack, unmanaged, and vSphere clouds list `tags` as unsupported.

(constraint-virt-type)=
### `virt-type`

`virt-type` is the virtualization type of the machine. The valid values depend on the cloud: `container` and `virtual-machine` on {ref}`LXD <cloud-lxd>`, where the default is `container`; `virtual-machine` on MAAS, which composes a virtual machine from a pod; and `kvm` and `lxd` on {ref}`OpenStack <cloud-openstack>`. Azure, EC2, GCE, Kubernetes, OCI, unmanaged, and vSphere clouds list it as unsupported.

(constraint-zones)=
### `zones`

`zones` is a comma-separated list of availability zones. Juju creates the machine in one of the listed zones. The valid values depend on the cloud; for example, `zones=us-east-1a,us-east-1c` on EC2. At bootstrap, a list in which no zone is available fails with `no available zones (<the zones of the cloud>) matching bootstrap zone constraints (<the listed zones>)`. Name a zone that the cloud offers. A cloud without zones ignores the constraint. A zone can also be given as a {ref}`placement directive <placement-directive>` (for example, `juju deploy --to zone=<name of zone>`), and the placement directive takes precedence over the constraint.
