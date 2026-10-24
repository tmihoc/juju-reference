# Storage page: the section split (session 88, derived from the 4.1 DDL and domain code)

Derivation rule (NEXT-PROMPT first move): split by shared owner and shared
lifecycle, not by size. Cited foreign keys are from `experiments/e11/model.ddl`
(line numbers below). The commit that lands the storage page records this
reason.

## The five sections of the Storage data model

1. **Storage directives** — `application_storage_directive` (:542),
   `unit_storage_directive` (:572).
   Owner: an application (`fk_application_storage_directive_application`,
   application_uuid -> application) or a unit
   (`fk_unit_storage_directive_unit`, unit_uuid -> unit); both also point at
   `storage_pool` and `(charm_uuid, storage_name) -> charm_storage`.
   Lifecycle: rows are replaced when the application's or unit's charm
   changes (both table comments, :538-541 and :565-571); a unit's charm may
   temporarily diverge from its application's (:569-571).

2. **Storage pools** — `storage_pool` (:465), `storage_pool_attribute`
   (:497), `model_storage_pool` (:526).
   Owner: the model. `storage_pool` has no FK to any entity: a pool exists
   for as long as the model does; `model_storage_pool` marks the model's
   default pool per storage kind
   (`fk_model_storage_pool_storage_kind`, `fk_model_storage_pool_storage_pool_uuid`).
   Lifecycle: created by an administrator or at model creation
   (`storage_pool_origin`: user, provider-default; :461-463).

3. **Storage instances** — `storage_instance` (:597), `storage_unit_owner`
   (:629), `storage_attachment` (:643).
   Owner: a unit, through `storage_unit_owner`
   (`fk_storage_owner_storage_instance`, `fk_storage_owner_unit`) and
   `storage_attachment` (`fk_storage_attachment_storage_instance`,
   `fk_storage_attachment_unit`).
   Lifecycle: alive/dying/dead (`life_id`, `fk_storage_instance_life`);
   this is the record a charm's named storage gets (`storage_id`).

4. **Volumes and filesystems** — `storage_volume` (:715),
   `storage_instance_volume` (:746), `storage_filesystem` (:832),
   `storage_instance_filesystem` (:860), `storage_volume_status` (:687),
   `storage_filesystem_status` (:815).
   Owner: a storage instance, at most one of either kind: both link tables
   key on `storage_instance_uuid` (PK) with a unique index on the
   volume/filesystem side (:757-758, :871-872). Standalone otherwise: no FK
   to an instance; they carry their own `life_id` and
   `provision_scope_id` (model | machine; :700-709) and
   `obliterate_on_cleanup`, CHECK-constrained to non-alive life
   (:726-727, :840-841). The two status tables mirror each other with the
   same eight values (:677-685, :805-813) — the volume and the filesystem
   are the same design twice, one for block devices, one for mounts.

5. **Attachments to machines** — `storage_volume_attachment` (:760),
   `storage_volume_attachment_plan` (:913),
   `storage_volume_attachment_plan_attr` (:941),
   `storage_filesystem_attachment` (:874), `machine_volume` (:2436),
   `machine_filesystem` (:2451).
   Owner: a net node (a machine or container), through
   `net_node_uuid -> net_node` (`fk_storage_volume_attachment_node`,
   `fk_storage_filesystem_attachment_node`); `machine_volume` and
   `machine_filesystem` link a volume or filesystem to the machine that
   hosts it (`machine_uuid -> machine`). A volume attachment also names
   the block device it brought (`block_device_uuid -> block_device`) and
   cannot share its volume with another node
   (idx_storage_volume_attachment_volume_uuid, :788-789). A filesystem
   attachment carries the mount point. An attachment plan is the planned
   form of a volume attachment (device type local or iSCSI, :909-911, with
   free-form attributes) before the volume exists on the machine.

2 + 3 + 3 + 6 + 6 = 20 tables, matching the manifest.

## Why this split (for the commit message)

The tables group by who owns a row and when it dies: a directive dies with
its application's or unit's charm; a pool dies with the model; an instance
dies when its owner destroys it; a volume or filesystem dies with its
instance (unless persistent); an attachment dies when it is detached or
its machine dies. The volume and the filesystem repeat one design (mirrored
status tables, mirrored link tables, mirrored attachments), so each is a
kind inside the sections, not a section of its own.
