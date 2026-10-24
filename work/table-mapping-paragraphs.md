# The record-to-table closing paragraphs (dropped from the pages, session 92)

Provenance: extracted verbatim from commit `a0ff626ad789` (the pushed state
before `8c034d49ed` dropped them, 2026-10-21). These are the closing
paragraphs of the database schema sections of the 33 entity pages, per the
old page-recipe rule: one paragraph mapping each record to its table, naming
the views that join or filter records, and pointing at `juju-db-repl`'s
`.ddl <name>`.

Why kept: the mapping cost drafting and review time; it is the source
material for the generated "tables by topic" page (TODOS item 000000) and
would be the restore source if the paragraphs ever return to the pages.

Fates, session 92 (2026-10-21, the session 92 density test in
`page-recipe.md`):

- `offer.md`, `charm.md`: the rules these paragraphs carried moved into
  their record's bullets (the offer description fallback;
  `COALESCE(o.description, cm.description)`, `0032-offer.sql`; the charm
  insert-delete-only rule, `model.go:222-234`).
- `subnet.md`: the availability-zone sentence stayed in the page.
- `database.md`: not here; its subject is the storage layer, so its own
  mapping stays in the page.
- Everything else: dropped; the entity pages must not read as a code dump.

The paragraphs, verbatim, one section per page:


## action.md

An operation is a row in the table `operation`. Its parameters are rows in `operation_parameter`. Its link to a charm action is a row in `operation_action`. A task is a row in `operation_task`. The target of a task is a row in `operation_unit_task` or `operation_machine_task`. Its output path is a row in `operation_task_output`, its status is a row in `operation_task_status`, and its log messages are rows in `operation_task_log`. The allowed statuses come from the lookup table `operation_task_status_value`. {ref}`juju-db-repl` shows the definition of any of them with `.ddl <name>`.

## agent-version.md

An agent version is a row in the table `agent_version` of the model database. Its stream is a row in the lookup table `agent_stream`. An agent binary is a row in `agent_binary_store`, which exists in the controller database and in each model database; the view `v_agent_binary_store` joins each binary with its architecture name, its size, its hashes, and its path. {ref}`juju-db-repl` shows the definition of any of them with `.ddl <name>`.

## annotation.md

The annotations of a model are rows in `annotation_model`; the others are rows in `annotation_application`, `annotation_charm`, `annotation_machine`, `annotation_unit`, `annotation_storage_instance`, `annotation_storage_volume`, and `annotation_storage_filesystem`, each named after the entity it serves. {ref}`juju-db-repl` shows the definition of any of them with `.ddl <name>`.

## application.md

An application is a row in the table `application`. Its platform, channel, status, and workload version are rows in `application_platform`, `application_channel`, `application_status`, and `application_workload_version`. Its controller mark and agent are rows in `application_controller` and `application_agent`. Its life comes from the lookup table `life`, the operating system from `os`, the architecture from `architecture`, the hash algorithm from `password_hash_algorithm`, and the status values from `workload_status_value`. Its config items are rows in `application_config`, with their types from `charm_config_type`. Its config hash and setting are rows in `application_config_hash` and `application_setting`. Its constraint is a row in `application_constraint`, which refers to a row of `constraint`. Its device constraints and their attributes are rows in `device_constraint` and `device_constraint_attribute`. Its endpoints are rows in `application_endpoint`. Its extra bindings are rows in `application_extra_endpoint`. Its exposed spaces and ranges are rows in `application_exposed_endpoint_space` and `application_exposed_endpoint_cidr`. Its scale is a row in `application_scale`, its provisioner mark a row in `application_k8s_resources_managed`, its operator status a row in `operator_status`, and its Kubernetes service a row in `k8s_service`. The view `v_application_exposed_endpoint` joins the exposed spaces and ranges. The view `v_application_platform_channel` joins an application's platform and channel. The view `v_application_constraint` joins an application's constraint with its tags, spaces, and zones. {ref}`juju-db-repl` shows the definition of any of them with `.ddl <name>`.

## charm.md

A charm is a row in the table `charm`. Its metadata is a row in `charm_metadata`. Its relations are rows in `charm_relation`. The other records of a charm are rows in `charm_extra_binding`, `charm_config`, `charm_action`, `charm_resource`, `charm_storage` (with `charm_storage_property`), `charm_device`, `charm_container` (with `charm_container_mount`), `charm_manifest_base`, `charm_hash`, `charm_download_info`, `charm_term`, `charm_tag`, and `charm_category`. The allowed values come from the lookup tables `charm_source`, `charm_relation_role`, `charm_relation_scope`, `charm_config_type`, `charm_resource_kind`, `charm_storage_kind`, `charm_run_as_kind`, `charm_provenance`, `hash_kind`, `os`, and `architecture`. A database trigger refuses to change a row of every table above except `charm`, `charm_download_info`, `charm_tag`, `charm_category`, `charm_storage_property`, and the lookup tables, so that only an insertion or a deletion alters it. The view `v_application_charm_download_info` joins an application to the download information of its charm. {ref}`juju-db-repl` shows the definition of any table with `.ddl <name>`.

## cloud.md

A cloud is a row in the table `cloud`. Its regions, CA certificates, and admitted authentication types are rows in `cloud_region`, `cloud_ca_cert`, and `cloud_auth_type`, and the allowed cloud types and authentication types come from the lookup tables `cloud_type` and `auth_type`. {ref}`juju-db-repl` shows the definition of any of them with `.ddl <name>`.

## constraint.md

A constraint is a row in the table `constraint`. Its tags, spaces, and zones are rows in `constraint_tag`, `constraint_space`, and `constraint_zone`. The view `v_constraint` shows each constraint with the name of its container type. Each holder's constraint is a row in `model_constraint`, `application_constraint`, or `machine_constraint`. {ref}`juju-db-repl` shows the definition of any of them with `.ddl <name>`.

## controller.md

A controller is the one row of the table `controller`. Its settings are rows in `controller_config`. A controller node is a row in `controller_node`. Its records are rows in `controller_node_agent_version`, `controller_node_password`, `controller_agent_address`, `controller_client_address`, and `controller_peer_address`. The tables `controller_node` and `controller_node_agent_version` use the lookup tables `life` and `architecture`. The table `controller_node_password` uses `password_hash_algorithm`. {ref}`juju-db-repl` shows the definition of any of them with `.ddl <name>`.

## credential.md

A credential is a row in the table `cloud_credential`. Its attributes are rows in `cloud_credential_attribute`. The allowed authentication types come from the lookup table `auth_type`. {ref}`juju-db-repl` shows the definition of any of them with `.ddl <name>`.

## external-controller.md

An external controller is a row in the table `external_controller`. Its addresses are rows in `external_controller_address`. Its models are rows in `external_model`. {ref}`juju-db-repl` shows the definition of any of them with `.ddl <name>`.

## image-metadata.md

An image is a row in the table `cloud_image_metadata` of the controller database. {ref}`juju-db-repl` shows its definition with `.ddl cloud_image_metadata`.

## lease.md

A lease is a row in the table `lease`. Its type is a row in the lookup table `lease_type`. A pin is a row in `lease_pin`. {ref}`juju-db-repl` shows the definition of any of them with `.ddl <name>`.

## link-layer-device.md

A network node is a row in the table `net_node`. A device is a row in `link_layer_device`; its type and virtual port type come from the lookup tables `link_layer_device_type` and `virtual_port_type`. Its parent is a row in `link_layer_device_parent`. Its search domains are rows in `link_layer_device_dns_domain`, its DNS servers are rows in `link_layer_device_dns_address`, and its routes are rows in `link_layer_device_route`. Its addresses are rows in `ip_address`, whose type, configuration type, origin, and scope come from the lookup tables `ip_address_type`, `ip_address_config_type`, `ip_address_origin`, and `ip_address_scope`. The cloud IDs are rows in `provider_link_layer_device` and `provider_ip_address`. A FQDN is a row in `fqdn_address` and its links are rows in `net_node_fqdn_address`; a hostname is a row in `hostname_address` and its links are rows in `net_node_hostname_address`; the scopes of both come from the lookup table `network_address_scope`. The view `v_ip_address_with_names` shows each address with the names of its type, configuration type, origin, and scope. The view `v_all_unit_address` shows the addresses of each unit together with the addresses of its application's Kubernetes service. {ref}`juju-db-repl` shows the definition of any of them with `.ddl <name>`.

## machine.md

A machine is a row in the table `machine`. Its status is a row in `machine_status`. Its platform, parent, and placement are rows in `machine_platform`, `machine_parent`, and `machine_placement`, and its agent presence and block devices are rows in `machine_agent_presence` and `block_device`, with the link names in `block_device_link_device`. Its cloud instance is a row in `machine_cloud_instance`. The instance's status is a row in `machine_cloud_instance_status`. The tags are rows in `instance_tag`. The remaining records are rows in `machine_agent_version`, `machine_requires_reboot`, `machine_constraint`, `machine_container_type`, `machine_manual`, and `machine_reprovision`. The values of the statuses come from the lookup tables `machine_status_value` and `machine_cloud_instance_status_value`. {ref}`juju-db-repl` shows the definition of any of them with `.ddl <name>`.

## model-defaults.md

A cloud default is a row in the table `cloud_defaults`. A region default is a row in `cloud_region_defaults`. {ref}`juju-db-repl` shows the definition of either with `.ddl <name>`.

## model-migration.md

An export is a row in the table `model_migration_export`; its history in `model_migration_export_phase`; its status message in `model_migration_export_status`; its minion reports in `model_migration_export_minion_sync`; its offers in `model_migration_export_offer`; its target authorization in `model_migration_export_target_auth`. The phases are rows in the lookup table `model_migration_phase`. A redirect is a row in `model_migration_redirect`. Its users are rows in `model_migration_redirect_user`. An import is a row in `model_migration_import`, with its phase in the lookup table `model_migration_import_phase_type`, its offers in `model_migration_import_offer`, and its external models in `model_migration_import_external_controller_model`. All of these are in the controller database; the migrating marker is a row in `model_migrating` and the log transfer progress in `log_transfer_progress`, both in the model database. {ref}`juju-db-repl` shows the definition of any of them with `.ddl <name>`.

## model.md

A model is a row in the table `model`. Its secret backend and last logins are rows in `model_secret_backend` and `model_last_login`. The model type comes from the lookup table `model_type`. The migration records are rows in the tables whose names start with `model_migration`. A model's contents are rows in the tables `model`, `model_config`, `model_constraint`, `model_life`, `model_migrating`, `model_storage_pool`, and `agent_version` of its model database. {ref}`juju-db-repl` shows the definition of any of them with `.ddl <name>`.

## object-store.md

A stored object is a row in the table `object_store_metadata`, which exists in the controller database and in each model database. Its paths are rows in `object_store_metadata_path` and its placements are rows in `object_store_placement`, which exist in both databases too. The backends are rows in `object_store_backend`, which exists only in the controller database; an S3 backend's configuration is a row in `object_store_backend_s3_config` and a drain is a row in `object_store_drain_info`. The view `v_object_store_metadata` joins each stored object with its path. {ref}`juju-db-repl` shows the definition of any of them with `.ddl <name>`.

## offer.md

An offer is a row in the table `offer` of the offering model's database. The endpoints it exposes are rows in `offer_endpoint`, each pointing to an application endpoint. Each offer connection is a row in `offer_connection`. The view `v_offer_detail` joins an offer with its application, {ref}`charm <charm>`, endpoints, and connection counts. It also applies the rule that an offer without a description shows the description of the application's charm. A model's consumed offers are rows in `application_remote_offerer`. A permission is a row in the controller database table `permission`, whose column `grant_on` holds the offer's UUID. The view `v_permission_offer` lists the permissions that name an offer. {ref}`juju-db-repl` shows the definition of any of them with `.ddl <name>`.

## relation.md

A relation is a row in the table `relation`. Its endpoints are rows in `relation_endpoint`. Its units in scope are rows in `relation_unit`. Its status is a row in `relation_status` whose values come from the lookup table `relation_status_type`. The unit settings are rows in `relation_unit_setting`. The application settings are rows in `relation_application_setting`. The archived settings are rows in `relation_unit_setting_archive`. The departed units are rows in `relation_unit_departure`. The CIDRs are rows in `relation_network_ingress` and `relation_network_egress`. The view `v_relation_status` shows each status by name. The view `v_relation_endpoint` shows each endpoint with its application, endpoint name, interface, and role. {ref}`juju-db-repl` shows the definition of any of them with `.ddl <name>`.

## resource-charm.md

A charm resource is a row in the table `charm_resource`. Its kind is a row of `charm_resource_kind`. A resource is a row in the table `resource`. Its origin and state are rows of `resource_origin_type` and `resource_state`. An application resource is a row in `application_resource`. A pending resource is a row in `pending_application_resource`. A unit resource is a row in `unit_resource`. The retrieved-by record is a row in `resource_retrieved_by`, with its type in `resource_retrieved_by_type`. A file store is a row in `resource_file_store`. An image store is a row in `resource_image_store`. Image metadata is a row in `resource_container_image_metadata_store`. The views `v_resource`, `v_application_resource`, and `v_unit_resource` join these records for listing. {ref}`juju-db-repl` shows any definition with `.ddl <name>`.

## secret-backend.md

A secret backend is a row in the table `secret_backend`, its type comes from the lookup table `secret_backend_type`, and its settings are rows in `secret_backend_config`. A token rotation is a row in `secret_backend_rotation`, a model's backend is a row in `model_secret_backend`, and a secret reference is a row in `secret_backend_reference`. {ref}`juju-db-repl` shows the definition of any of them with `.ddl <name>`.

## secret.md

A secret is a row in the table `secret_metadata`, with a row in `secret` that holds its ID. Its owner is a row in `secret_model_owner`, `secret_application_owner`, or `secret_unit_owner`. Its consumers are rows in `secret_unit_consumer`, its grants are rows in `secret_permission`, and its rotation is a row in `secret_rotation`. Its revisions are rows in `secret_revision`. The content items of a revision are rows in `secret_content`, its backend reference is a row in `secret_value_ref`, its expiry is a row in `secret_revision_expire`, and its obsolete mark is a row in `secret_revision_obsolete`. The allowed values come from the lookup tables `secret_rotate_policy`, `secret_role`, `secret_grant_subject_type`, and `secret_grant_scope_type`. The views `v_secret_metadata`, `v_secret_owner`, and `v_secret_permission` join these records and replace the UUIDs of owners, subjects, and scopes with their names. The trigger `trg_secret_permission_guard_update` enforces the rule that a grant keeps its subject type and scope. {ref}`juju-db-repl` shows the definition of any of them with `.ddl <name>`.

## space.md

A space is a row in the table `space`. A cloud's ID for it is a row in `provider_space`. {ref}`juju-db-repl` shows the definition of any of them with `.ddl <name>`.

## ssh-key.md

An SSH key is a row in the table `user_public_ssh_key`. The algorithm of its fingerprint comes from the lookup table `ssh_fingerprint_hash_algorithm`. Each model authorization is a row in `model_authorized_keys`. The view `v_model_authorized_keys` applies the rule about disabled users: query the view, not the table, to see the keys a model honors. {ref}`juju-db-repl` shows the definition of any of them with `.ddl <name>`.

## ssh-server.md

The controller's host key is a row in the table `controller_ssh_host_key` and its port is a row in `controller_ssh_server_port`. In the model database, a machine's own host keys are rows in `machine_ssh_host_key`, its virtual host key is a row in `machine_virtual_ssh_host_key`, a Kubernetes unit's virtual host key is a row in `unit_virtual_ssh_host_key`, and a connection request is a row in `ssh_connection_request`. Both databases keep the lookup table `ssh_key_algorithm_type`, which holds the three algorithm names. {ref}`juju-db-repl` shows the definition of any of them with `.ddl <name>`.

## storage.md

A storage is a row in the table `storage_instance`. Its attachments are rows in `storage_attachment`, its owner is a row in `storage_unit_owner`, and what backs it is a row in `storage_volume` or `storage_filesystem`, linked by a row in `storage_instance_volume` or `storage_instance_filesystem`. A directive is a row in `application_storage_directive` or `unit_storage_directive`. A pool is a row in `storage_pool`, its attributes are rows in `storage_pool_attribute`, and the model's default pools are rows in `model_storage_pool`, one per kind in `storage_kind`. A volume or filesystem status is a row in `storage_volume_status` or `storage_filesystem_status`, with its values in the lookup tables `storage_volume_status_value` and `storage_filesystem_status_value`. An attachment is a row in `storage_volume_attachment` or `storage_filesystem_attachment`, a plan is a row in `storage_volume_attachment_plan` with its attributes in `storage_volume_attachment_plan_attr` and its device type in the lookup table `storage_volume_device_type`, and the machines that host a volume or a filesystem are rows in `machine_volume` and `machine_filesystem`. The provision scope of a volume, a filesystem, or an attachment is one of the values in the lookup table `storage_provision_scope`. {ref}`juju-db-repl` shows the definition of any of them with `.ddl <name>`.

## subnet.md

A subnet is a row in the table `subnet`. Its cloud ID is a row in `provider_subnet`. Its provider network is linked by a row in `provider_network_subnet` to a row in `provider_network`. {ref}`juju-db-repl` shows the definition of any of them with `.ddl <name>`. The {ref}`availability zones <zone>` in which a subnet is available are linked to it by their own records.

## telemetry.md

The workload tracing configuration is a set of rows in the table `workload_tracing_config`. The charm tracing configuration is a set of rows in `charm_tracing_config`. Each row is one field and its value. The log forwarding configuration is one row in `logging_loki_config`. {ref}`juju-db-repl` shows the definition of any of them with `.ddl <name>`.

## unit.md

A unit is a row in the table `unit`. Its principal is a row in `unit_principal`. Its workload status, agent status, and pod status are rows in `unit_workload_status`, `unit_agent_status`, and `k8s_pod_status`, whose values come from the lookup tables `workload_status_value`, `unit_agent_status_value`, and `k8s_pod_status_value`. Its agent presence, workload version, agent version, and resolved marker are rows in `unit_agent_presence`, `unit_workload_version`, `unit_agent_version`, and `unit_resolved`, and the resolve modes come from the lookup table `resolve_mode`. Its unit state, charm state, and relation state are rows in `unit_state`, `unit_state_charm`, and `unit_state_relation`. Its pod and the pod's ports are rows in `k8s_pod` and `k8s_pod_port`. The leader is a row in the controller database table `lease`. The views `v_unit_agent_status`, `v_unit_workload_status`, and `v_full_unit_status` join a unit with its statuses and its presence. {ref}`juju-db-repl` shows any definition with `.ddl <name>`.

## upgrade.md

An upgrade is a row in the table `upgrade_info`. Its state is a row in the lookup table `upgrade_state_type`. A node's part is a row in `upgrade_info_controller_node`. {ref}`juju-db-repl` shows the definition of any of them with `.ddl <name>`.

## user.md

A user is a row in the table `user`. Its authentication is a row in `user_authentication`, its password a row in `user_password`, and its activation key a row in `user_activation_key`. A permission is a row in `permission`, which names its object in the column `grant_on` (the name of a cloud, or the UUID of a controller, model, or offer). The allowed pairs of object type and access level come from the lookup tables `permission_object_type`, `permission_access_type`, and `permission_object_access`. A last login is a row in `model_last_login`. The view `v_user_auth` joins a user with its disabled flag, and the view `v_user_last_login` gives the latest login of each user. The views `v_permission_controller`, `v_permission_cloud`, and `v_permission_model` list only the permissions whose object exists. {ref}`juju-db-repl` shows the definition of any of them with `.ddl <name>`.

## zone.md

A zone is a row in the table `availability_zone`. The link to a subnet is a row in `availability_zone_subnet`. {ref}`juju-db-repl` shows the definition of any of them with `.ddl <name>`.
