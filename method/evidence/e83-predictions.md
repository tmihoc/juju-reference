# E83 predictions (procedure v1, written before any case's docs diff was opened)

Registered in `archive/structure-discovery-plan.md` (E83). Inputs per case: the non-test Go diff and commit or PR message, and the docs tree at the parent commit. Chunks are file plus section. `[gen]` marks a generated file.

**Known gap of v1 recorded before comparison:** the procedure has no step for release notes, although `method/requirement-set.md` R23 says version facts belong there. Predictions follow v1 strictly. Any release-notes edit in the oracle counts as a P-miss and revises v1.

All paths are under `docs/`.

## C1: `3effaf8cb2`, `--show-command` for ssh and scp

Delta: a new CLI flag on `juju ssh` and `juju scp` (prints the OpenSSH command instead of running it); a client-side error when it is used without `--jump`.
Existing statements: none in hand-written docs (the parent has no hand-written text on `--jump` at all).

| # | Action | Chunk | Category | Req | Confidence |
|---|---|---|---|---|---|
| 1.1 | regenerate | `reference/juju-cli/list-of-juju-cli-commands/ssh.md`, `scp.md` [gen] | reference | R4 | Determined |
| 1.2 | add | `howto/manage-machines.md` > "Use the `juju ssh` command" (flag and the proxy context it needs) | how-to | R9, R27 | Open(Q1): the base feature (`--jump`) is itself undocumented by hand, so the gap is larger than this delta |

Examined and left unchanged: `reference/ssh-key.md` (about keys, not connection options).

## C2: `12a8237cfe`, `--jump` becomes the default

Delta: `juju ssh` and `juju scp` now proxy through the controller's SSH server by default (port 17022 by default must be reachable); `--jump` is removed; `--direct` is added for Juju 3 controllers; `--proxy` is now combined with `--direct`; nested containers are not supported in the new mode; new error text for `--show-command` with `--direct`; SSHClient facade v6.

| # | Action | Chunk | Category | Req | Confidence |
|---|---|---|---|---|---|
| 2.1 | regenerate | `ssh.md`, `scp.md` [gen] | reference | R4 | Determined |
| 2.2 | update (incomplete) | `howto/manage-machines.md` > the "two ways to connect" opening and "Use the `juju ssh` command": default path, port requirement, `--direct`, container limitation | how-to | R27 | Determined |
| 2.3 | update (incomplete) | `howto/manage-controllers.md` > the public-controller prerequisite that says the client must reach the API port: add the SSH server port | how-to | R27 | Open(Q1): unclear whether that statement's scope covers ssh |
| 2.4 | verify, then fix if false | `reference/ssh-key.md` > the sentence that says using `juju ssh` needs the key added to the model and admin access | reference | Quality | Determined (action is a source check) |

Examined and left unchanged: `explanation/juju-security.md` (no rationale or architecture picture is contradicted); `reference/configuration/list-of-controller-configuration-keys.md` > `ssh-server-port` (still true). No API reference for facade versions exists in the parent docs.

## C3: `5d37846068`, GCE `image-id` support

Delta: the `image-id` constraint is accepted on GCE (a short image name resolved in the base image project, or a full project/global/images path or URL); the image's architecture must equal the agent's, otherwise an error; EC2 and OpenStack keep their stubs.
Existing statements: the GCE constraints list has no `image-id`; `reference/constraint.md` > `image-id` says "Not supported by all providers".

| # | Action | Chunk | Category | Req | Confidence |
|---|---|---|---|---|---|
| 3.1 | add | `reference/cloud/list-of-supported-clouds/google-gce.md` > Machines > Constraints (`gce-machine-constraints`): `image-id`, valid values, architecture condition | reference | R7, R27 | Determined |
| 3.2 | update if the source trace confirms | same file > `base-image-path` entry: short names resolve against it | reference | Quality | Determined |

Examined and left unchanged: `reference/constraint.md` > `image-id` (adequate); `amazon-ec2.md` and `openstack.md` (observable behavior unchanged); `howto/manage-metadata.md`.

## C4: `8e6af62c97`, OpenStack Cinder pool as root disk source

Delta: `root-disk-source` accepts a storage pool name besides `local` and `volume`; the cinder pool gains `tag` and `disk-bus` (root disk only) next to `volume-type`; a nova compute microversion is required for `volume-type` and `tag`; new validation messages; instance-type matching ignores root-disk size for any non-local source.

| # | Action | Chunk | Category | Req | Confidence |
|---|---|---|---|---|---|
| 4.1 | fix | `reference/cloud/list-of-supported-clouds/openstack.md` > Constraints: `root-disk-source` values line (now false: "local or volume") | reference | Quality | Determined |
| 4.2 | update | same file > the root-disk bullets in the bootstrap and machine resource lists | reference | R27 | Determined |
| 4.3 | add | same file > `storage-provider-cinder` attributes: `tag`, `disk-bus`, root-disk-only limit | reference | R27 | Determined |
| 4.4 | add | same file > Requirements: compute microversion for `volume-type` and `tag` | reference | R7 | Determined |

Examined and left unchanged: `reference/constraint.md` > `root-disk-source` ("different behaviour with each provider": adequate); `howto/manage-storage-pools.md` (generic).

## C5: `bd9cc89530`, charm revision implies resource revision

Delta: help text of `--revision` on `deploy` and `refresh` states that it implicitly selects the resource revisions released with that charm revision (overridable with `--resource`); a new informational message at run time. The underlying behavior existed before.

| # | Action | Chunk | Category | Req | Confidence |
|---|---|---|---|---|---|
| 5.1 | regenerate | `deploy.md`, `refresh.md` [gen] | reference | R4 | Determined |
| 5.2 | update | `howto/manage-charm-resources.md` > the bullets on specifying and updating a resource's revision | how-to | R27 | Determined |
| 5.3 | update | `howto/manage-charms.md` > where deploying or refreshing to a specific revision is described | how-to | R27 | Determined (contingent on the locate hit) |
| 5.4 | add or link | the owner of "resources are released alongside a charm revision" (`reference/charm.md` > revisions, or the resource entry) | reference | R17 | Open(Q1, Q2): owner unclear in the parent set |

## C6: `416d1b3a2a`, create-backup always returns the archive

Delta: `create-backup` always downloads the archive and verifies its checksum; `--no-download` and the `download-backup` command are removed; the controller copy is removed after delivery or after a 15-minute sweep; `backup-dir` is scratch space only; a new HTTP download endpoint; a new backup-sweeper worker.

| # | Action | Chunk | Category | Req | Confidence |
|---|---|---|---|---|---|
| 6.1 | regenerate; delete | `create-backup.md` [gen]; `download-backup.md` [gen, removed]; the CLI command index | reference | R4 | Determined |
| 6.2 | redirect | `redirects.txt`: the removed page needs a redirect | reference | R15 | Determined |
| 6.3 | fix | `howto/upgrade-your-juju-deployment-from-36-to-41.md` > "backups are not delivered; `create-backup` fails with not-implemented" (false at this commit) | how-to | Quality | Determined |
| 6.4 | add | `howto/manage-controllers.md`: a backup section (the lifecycle step has no how-to; always-downloaded archive, checksum, retention) | how-to | R9, R27 | Open(Q1): the gap predates this development |
| 6.5 | add | a home for the HTTP download endpoint | reference | R7 | Open(Q1): no route reference exists in the parent set |

Examined and left unchanged: `reference/configuration/list-of-model-configuration-keys.md` > `backup-dir` ("directory used to store the backup working directory" stays true); `explanation/juju-security.md` > Regular backups.

## Tally of the prediction

| Class | Count |
|---|---|
| Determined | 16 |
| Open(Qn) | 5 (1.2, 2.3, 5.4, 6.4, 6.5) |
| Total items | 21 |
| Determined share | 76 percent |

The first draft of this tally said 15 and 6; recounted before any diff was opened.
