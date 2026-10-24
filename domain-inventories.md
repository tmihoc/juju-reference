# Generated part inventories for 36 domains (4.1, session 79)

Produced by `experiments/e17/gen_inventory.py`; heuristics and caveats as in the plan (E19, E20c, E21 to E21c). Read as drafts for authors, not as pages.

## access

**Identity.** Scope: controller database. Life column: none. Lifecycle kinds: deletable. Removal job types: none.

**State.**
- `bakery_config` (controller) 
- `macaroon_root_key` (controller) 
- `permission` (controller) 
- `permission_access_type` (controller) lookup: add-model, admin, consume, login, read, superuser, write
- `permission_object_access` (controller) lookup: 
- `permission_object_type` (controller) lookup: cloud, controller, model, offer
- `user` (controller) 
- `user_activation_key` (controller) 
- `user_authentication` (controller) watched
- `user_password` (controller) 
- views touching these tables: v_cloud_credential, v_everyone_external, v_model_all, v_model_authorized_keys, v_permission, v_user_auth

**Observation (Watch methods and who uses them).**
- none

**Dynamics (service mutators).** AddExternalUser, AddUser, CreatePermission, DeletePermission, DeletePermissionsByGrantOnUUID, DisableUserAuthentication, EnableUserAuthentication, EnsureExternalUser, ImportExternalUsers, ImportLastModelLogins, ImportModelPermissions, ImportModelUsers, ImportOfferAccess, RemoveUser, ResetPassword, SetLastModelLogin, SetPassword, SetPasswordWithActivationKey, UpdateLastModelLogin, UpdatePermission

**Interface (facades importing the domain).** client/applicationoffers, client/cloud, client/controller, client/keymanager, client/modelmanager, client/usermanager

**Failure.** 18 error constants: `user not found`; `user creator UUID not found`; `username not valid`; `User UUID not valid`; `user already exists`; `user authentication disabled`; `user unauthorized`; `permission not valid`; `permission not found`; `permission already exists`; `permission target invalid`; `permission access invalid` ...

**Agent (workers importing the domain).** bootstrap, controlsocket

**Migration.** modelmigration package: True; legacy import registered: True; owned tables read by the generic export: 0 of 10.

## agentbinary

**Identity.** Scope: controller, model database. Life column: none. Lifecycle kinds: append-only, pruned. Removal job types: none.

**State.**
- `agent_binary_store` (controller) 
- `agent_binary_store` (model) 
- views touching these tables: v_agent_binary_store, v_agent_binary_store

**Observation (Watch methods and who uses them).**
- none

**Dynamics (service mutators).** AddAgentBinaryWithSHA256, AddAgentBinaryWithSHA384

**Interface (facades importing the domain).** client/machinemanager, client/modelconfig, client/modelupgrader

**Failure.** 6 error constants: `agent binary already exists`; `agent binary is immutable`; `agent binary not found`; `agent binary has mismatch`; `agent binary object not found`; `agent binary stream not found`

**Agent (workers importing the domain).** agentbinaryfetcher, computeprovisioner

**Migration.** modelmigration package: False; legacy import registered: False; owned tables read by the generic export: 1 of 1.

## annotation

**Identity.** Scope: model database. Life column: none. Lifecycle kinds: deletable. Removal job types: none.

**State.**
- `annotation_application` (model) 
- `annotation_charm` (model) 
- `annotation_machine` (model) 
- `annotation_model` (model) 
- `annotation_storage_filesystem` (model) 
- `annotation_storage_instance` (model) 
- `annotation_storage_volume` (model) 
- `annotation_unit` (model) 
- views touching these tables: none

**Observation (Watch methods and who uses them).**
- none

**Dynamics (service mutators).** SetAnnotations, SetCharmAnnotations

**Interface (facades importing the domain).** client/annotations

**Failure.** 4 error constants: `unknown kind`; `invalid id parts`; `not found`; `invalid key`

**Agent (workers importing the domain).** none

**Migration.** modelmigration package: True; legacy import registered: True; owned tables read by the generic export: 8 of 8.

## application

**Identity.** Scope: model database. Life column: model. Lifecycle kinds: life-column, pruned. Removal job types: unit, application.

**State.**
- `application` (model) life watched
- `application_agent` (model) 
- `application_channel` (model) 
- `application_config` (model) 
- `application_config_hash` (model) watched
- `application_constraint` (model) 
- `application_controller` (model) immutable
- `application_exposed_endpoint_cidr` (model) watched
- `application_exposed_endpoint_space` (model) watched
- `application_k8s_resources_managed` (model) 
- `application_platform` (model) 
- `application_scale` (model) watched
- `application_setting` (model) watched
- `application_status` (model) status watched
- `application_workload_version` (model) 
- `charm` (model) watched
- `charm_action` (model) immutable
- `charm_category` (model) 
- `charm_config` (model) immutable
- `charm_config_type` (model) lookup: boolean, float, int, secret, string
- `charm_container` (model) immutable
- `charm_container_mount` (model) immutable
- `charm_device` (model) immutable
- `charm_download_info` (model) 
- `charm_extra_binding` (model) immutable
- `charm_hash` (model) immutable
- `charm_manifest_base` (model) immutable
- `charm_metadata` (model) immutable
- `charm_provenance` (model) lookup: bootstrap, download, migration, upload
- `charm_relation` (model) immutable
- `charm_relation_role` (model) lookup: peer, provider, requirer
- `charm_relation_scope` (model) lookup: container, global
- `charm_resource` (model) immutable
- `charm_resource_kind` (model) lookup: file, oci-image
- `charm_run_as_kind` (model) lookup: default, non-root, root, sudoer
- `charm_source` (model) lookup: charmhub, cmr, local
- `charm_storage` (model) immutable
- `charm_storage_kind` (model) lookup: block, filesystem
- `charm_storage_property` (model) 
- `charm_tag` (model) 
- `charm_term` (model) immutable
- `device_constraint` (model) 
- `device_constraint_attribute` (model) 
- `hash_kind` (model) lookup: sha256
- `k8s_pod` (model) 
- `k8s_pod_port` (model) 
- `k8s_pod_status` (model) status watched
- `k8s_pod_status_value` (model) lookup: blocked, error, running, unset, waiting
- `k8s_service` (model) watched
- `operator_status` (model) status
- `resolve_mode` (model) lookup: no-hooks, retry-hooks
- `unit` (model) life watched
- `unit_agent_presence` (model) 
- `unit_agent_status` (model) status watched
- `unit_agent_status_value` (model) lookup: allocating, error, executing, failed, idle, lost, rebooting
- `unit_agent_version` (model) 
- `unit_principal` (model) watched
- `unit_resolved` (model) watched
- `unit_state` (model) 
- `unit_state_charm` (model) 
- `unit_state_relation` (model) 
- `unit_workload_status` (model) status watched
- `unit_workload_version` (model) 
- views touching these tables: v_all_unit_address, v_application_charm_download_info, v_application_config, v_application_constraint, v_application_endpoint, v_application_endpoint_uuid, v_application_exposed_endpoint, v_application_origin, v_application_platform_channel, v_application_resource, v_application_subordinate, v_charm_annotation_index, v_charm_config, v_charm_container, v_charm_manifest, v_charm_metadata, v_charm_relation, v_charm_resource, v_charm_storage, v_endpoint, v_full_unit_status, v_machine_is_controller, v_model_metrics, v_offer_detail, v_port_range, v_relation_endpoint, v_relation_endpoint_identifier, v_resource, v_revision_updater_application, v_revision_updater_application_unit, v_secret_owner, v_secret_permission, v_unit_agent_status, v_unit_attribute, v_unit_password_hash, v_unit_relation_network, v_unit_resource, v_unit_target_agent_version, v_unit_workload_agent_status, v_unit_workload_status

**Observation (Watch methods and who uses them).**
- WatchApplication: T2; facades ['agent/uniter']; workers ['caasapplicationprovisioner']
- WatchApplicationConfig: T0; facades -; workers -
- WatchApplicationConfigHash: T2; facades ['agent/uniter']; workers -
- WatchApplicationExposed: T3; facades -; workers ['firewaller']
- WatchApplicationScale: T3; facades -; workers ['caasapplicationprovisioner']
- WatchApplicationSettings: T3; facades -; workers ['caasapplicationprovisioner']
- WatchApplicationUnitLife: T3; facades -; workers ['caasapplicationprovisioner']
- WatchApplications: T3; facades -; workers ['caasapplicationprovisioner', 'caasfirewaller']
- WatchApplicationsWithPendingCharms: T3; facades -; workers ['asynccharmdownloader']
- WatchCharms: T0; facades -; workers -
- WatchUnitAddRemoveOnMachine: T2; facades ['agent/deployer']; workers ['firewaller']
- WatchUnitAddresses: T0; facades -; workers -
- WatchUnitAddressesHash: T2; facades ['agent/uniter']; workers -
- WatchUnitForLegacyUniter: T2; facades ['agent/uniter']; workers -
- WatchUnitLife: T2; facades ['agent/lifeflag']; workers -

**Dynamics (service mutators).** AddCAASUnits, AddCharm, AddIAASUnits, AddStorageForCAASUnit, AddStorageForIAASUnit, AttachStorageInstanceToUnit, AttachStorageToUnit, ChangeApplicationScale, CreateCAASApplication, CreateIAASApplication, DetachStorage, DetachStorageForUnit, ImportCAASApplication, ImportIAASApplication, MergeApplicationEndpointBindings, MergeExposeSettings, RegisterCAASUnit, SetApplicationCharm, SetApplicationConstraints, SetApplicationHasK8sResources, SetApplicationScale, SetApplicationScalingState, SetApplicationScalingStateWithStart, SetCharmAvailable, SetUnitWorkloadVersion, UnsetApplicationConfigKeys, UnsetExposeSettings, UpdateApplicationConfig, UpdateCAASUnit, UpdateK8sService, UpdateUnitCharm

**Interface (facades importing the domain).** agent/agent, agent/caasapplication, agent/deployer, agent/provisioner, agent/resourceshookcontext, agent/secretsmanager, agent/storageprovisioner, agent/uniter, agent/upgrader, client/action, client/application, client/applicationoffers, client/bundle, client/charms, client/client, client/machinemanager, client/resources, client/sshclient, client/storage, controller/crossmodelrelations

**Failure.** 70 error constants: `application not found`; `application already exists`; `application is not alive`; `application is dead`; `application has units`; `application has relations`; `application not subordinate`; `scaling state is inconsistent`; `scale change invalid`; `incompatible base for charm`; `no storage directive specified`; `application name not valid` ...

**Agent (workers importing the domain).** asynccharmdownloader, bootstrap, caasapplicationprovisioner, caasfirewaller, charmrevisioner, firewaller, migrationmaster, remoterelationconsumer, storageprovisioner

**Migration.** modelmigration package: True; legacy import registered: True; owned tables read by the generic export: 50 of 63.

## autocert

**Identity.** Scope: controller database. Life column: none. Lifecycle kinds: deletable. Removal job types: none.

**State.**
- `autocert_cache` (controller) 
- `autocert_cache_encoding` (controller) lookup: x509
- views touching these tables: none

**Observation (Watch methods and who uses them).**
- none

**Dynamics (service mutators).** Delete

**Interface (facades importing the domain).** none by import

**Failure.** 1 error constants: `cert not found`

**Agent (workers importing the domain).** none

**Migration.** modelmigration package: False; legacy import registered: False; owned tables read by the generic export: 0 of 2.

## blockcommand

**Identity.** Scope: model database. Life column: none. Lifecycle kinds: deletable. Removal job types: none.

**State.**
- `block_command` (model) 
- `block_command_type` (model) lookup: change, destroy, remove
- views touching these tables: none

**Observation (Watch methods and who uses them).**
- none

**Dynamics (service mutators).** RemoveAllBlocks

**Interface (facades importing the domain).** client/block, client/controller, client/machinemanager, client/modelconfig, client/modelmanager

**Failure.** 2 error constants: `block not found`; `block not found`

**Agent (workers importing the domain).** none

**Migration.** modelmigration package: True; legacy import registered: True; owned tables read by the generic export: 2 of 2.

## blockdevice

**Identity.** Scope: model database. Life column: none. Lifecycle kinds: deletable. Removal job types: none.

**State.**
- `block_device` (model) watched
- `block_device_link_device` (model) watched
- `block_device_provenance` (model) lookup: machine, provider
- views touching these tables: none

**Observation (Watch methods and who uses them).**
- WatchBlockDevicesForMachine: T2; facades ['agent/storageprovisioner', 'agent/uniter']; workers ['storageprovisioner']

**Dynamics (service mutators).** SetBlockDevicesForMachineByName, UpdateBlockDevicesForMachine

**Interface (facades importing the domain).** agent/storageprovisioner, agent/uniter

**Failure.** 1 error constants: `block device not found`

**Agent (workers importing the domain).** storageprovisioner

**Migration.** modelmigration package: True; legacy import registered: True; owned tables read by the generic export: 2 of 3.

## cloud

**Identity.** Scope: controller database. Life column: none. Lifecycle kinds: deletable. Removal job types: none.

**State.**
- `auth_type` (controller) lookup: access-key, certificate, clientcertificate, empty, httpsig, instance-role, interactive, jsonfile, managed-identity, oauth1, oauth2, oauth2withcert, service-account, service-principal-secret, userpass
- `cloud` (controller) watched
- `cloud_auth_type` (controller) 
- `cloud_ca_cert` (controller) watched
- `cloud_credential` (controller) watched
- `cloud_credential_attribute` (controller) watched
- `cloud_defaults` (controller) 
- `cloud_region` (controller) 
- `cloud_region_defaults` (controller) 
- `cloud_type` (controller) lookup: azure, ec2, gce, kubernetes, lxd, maas, oci, openstack, unmanaged, vsphere
- views touching these tables: v_cloud, v_cloud_auth, v_cloud_credential, v_cloud_credential_attribute, v_model, v_model_all, v_model_state, v_permission_cloud

**Observation (Watch methods and who uses them).**
- WatchCloud: T2; facades ['agent/agent']; workers -

**Dynamics (service mutators).** CreateCloud, DeleteCloud, UpdateCloud

**Interface (facades importing the domain).** agent/caasapplication, client/cloud, client/imagemetadatamanager, client/modelmanager, controller/caasoperatorupgrader

**Failure.** 3 error constants: `cloud already exists`; `cloud not found`; `cloud still in use`

**Agent (workers importing the domain).** none

**Migration.** modelmigration package: False; legacy import registered: False; owned tables read by the generic export: 0 of 10.

## cloudimagemetadata

**Identity.** Scope: controller database. Life column: none. Lifecycle kinds: deletable, pruned. Removal job types: none.

**State.**
- `cloud_image_metadata` (controller) 
- views touching these tables: none

**Observation (Watch methods and who uses them).**
- none

**Dynamics (service mutators).** DeleteMetadataWithImageID, ImportCloudImageMetadata

**Interface (facades importing the domain).** client/imagemetadatamanager

**Failure.** 4 error constants: `invalid metadata`; `metadata not found`; `image id is empty`; `image metadata already exists`

**Agent (workers importing the domain).** none

**Migration.** modelmigration package: True; legacy import registered: True; owned tables read by the generic export: 0 of 1.

## constraints

**Identity.** Scope: model database. Life column: none. Lifecycle kinds: append-only. Removal job types: none.

**State.**
- `constraint_space` (model) 
- `constraint_tag` (model) 
- `constraint_zone` (model) 
- views touching these tables: v_application_constraint, v_machine_constraint, v_model_constraint_space, v_model_constraint_tag, v_model_constraint_zone

**Observation (Watch methods and who uses them).**
- none

**Dynamics (service mutators).** none in this domain (a writer may be another domain)

**Interface (facades importing the domain).** client/application, client/machinemanager

**Failure.** 0 error constants: 

**Agent (workers importing the domain).** none

**Migration.** modelmigration package: True; legacy import registered: False; owned tables read by the generic export: 3 of 3.

## controller

**Identity.** Scope: controller database. Life column: none. Lifecycle kinds: append-only. Removal job types: none.

**State.**
- `controller` (controller) 
- views touching these tables: v_cloud, v_controller_config, v_model_all, v_model_secret_backend, v_permission_controller

**Observation (Watch methods and who uses them).**
- none

**Dynamics (service mutators).** none in this domain (a writer may be another domain)

**Interface (facades importing the domain).** agent/upgrader, client/applicationoffers, client/highavailability, client/modelupgrader

**Failure.** 1 error constants: `controller agent info not found`

**Agent (workers importing the domain).** apiaddresssetter, apiremotecaller, bootstrap, dbaccessor, proxyupdater

**Migration.** modelmigration package: False; legacy import registered: False; owned tables read by the generic export: 0 of 1.

## controllerconfig

**Identity.** Scope: controller database. Life column: none. Lifecycle kinds: deletable. Removal job types: none.

**State.**
- `controller_config` (controller) watched
- views touching these tables: v_controller_config

**Observation (Watch methods and who uses them).**
- WatchControllerConfig: T3; facades -; workers ['agentconfigupdater', 'apiaddresssetter', 'apiserver', 'auditconfigupdater']

**Dynamics (service mutators).** UpdateControllerConfig

**Interface (facades importing the domain).** none by import

**Failure.** 0 error constants: 

**Agent (workers importing the domain).** none

**Migration.** modelmigration package: False; legacy import registered: False; owned tables read by the generic export: 0 of 1.

## controllernode

**Identity.** Scope: controller database. Life column: controller. Lifecycle kinds: life-column. Removal job types: none.

**State.**
- `controller_agent_address` (controller) watched
- `controller_api_address` (controller) watched
- `controller_client_address` (controller) watched
- `controller_node` (controller) life watched
- `controller_node_agent_version` (controller) 
- `controller_node_nonce` (controller) 
- `controller_node_password` (controller) 
- `controller_peer_address` (controller) watched
- views touching these tables: none

**Observation (Watch methods and who uses them).**
- WatchControllerAddressesForCertificates: T3; facades -; workers ['certupdater']
- WatchControllerAgentAddresses: T2; facades ['agent/deployer', 'agent/machine', 'agent/proxyupdater', 'agent/uniter']; workers ['caasapplicationprovisioner', 'caasmodeloperator', 'proxyupdater']
- WatchControllerClientAddresses: T2; facades ['controller/crosscontroller']; workers -
- WatchControllerNodes: T3; facades -; workers ['apiaddresssetter']
- WatchControllerPeerAddresses: T3; facades -; workers ['apiremotecaller']

**Dynamics (service mutators).** AddDqliteNode, AddDqliteNodeID, SetAPIAddresses, SetControllerNodeReportedAgentVersion

**Interface (facades importing the domain).** agent/upgrader, client/highavailability

**Failure.** 5 error constants: `controller not found`; `controller address not valid`; `no controller IDs found`; `no API addresses found`; `stale controller membership`

**Agent (workers importing the domain).** apiaddresssetter, apiremotecaller, bootstrap, dbaccessor, proxyupdater

**Migration.** modelmigration package: False; legacy import registered: False; owned tables read by the generic export: 0 of 8.

## crossmodelrelation

**Identity.** Scope: model database. Life column: model. Lifecycle kinds: life-column. Removal job types: remote application offerer, relation with remote offerer, relation with remote consumer.

**State.**
- `application_remote_consumer` (model) life watched
- `application_remote_offerer` (model) life watched
- `application_remote_offerer_relation_macaroon` (model) 
- `application_remote_offerer_status` (model) status
- `offer` (model) watched
- `offer_connection` (model) 
- `offer_endpoint` (model) immutable
- `relation_network_egress` (model) immutable watched
- `relation_network_ingress` (model) immutable watched
- views touching these tables: v_offer_detail

**Observation (Watch methods and who uses them).**
- WatchConsumerRelations: T3; facades -; workers ['firewaller']
- WatchDyingModel: T3; facades -; workers ['remoterelationconsumer']
- WatchOffererRelations: T3; facades -; workers ['firewaller']
- WatchRelationEgressNetworks: T2; facades ['controller/crossmodelrelations']; workers ['firewaller']
- WatchRelationIngressNetworks: T3; facades -; workers ['firewaller']
- WatchRemoteApplicationConsumers: T0; facades -; workers -
- WatchRemoteApplicationOfferers: T3; facades -; workers ['remoterelationconsumer']
- WatchRemoteConsumedSecretsChanges: T2; facades ['controller/crossmodelrelations']; workers -

**Dynamics (service mutators).** AddConsumedRelation, AddRelationNetworkIngress, AddRemoteApplicationOfferer, CreateOffer, EnsureUnitsExist, ImportGrantedSecrets, ImportOffers, ImportRelationNetworks, ImportRemoteApplicationConsumers, ImportRemoteApplicationOfferers, ImportRemoteSecrets, SetOffererControllerForOffererModel, SetOffererControllerForOffererModels, UpdateOfferPermission, UpdateRemoteConsumedRevision, UpdateRemoteSecretRevision

**Interface (facades importing the domain).** agent/secretsmanager, agent/uniter, client/application, client/applicationoffers, client/client, controller/crossmodelrelations, controller/crossmodelsecrets

**Failure.** 15 error constants: `application not remote`; `macaroon not found`; `missing endpoints`; `offer already consumed`; `offer already exists`; `offer not found`; `offer URL not valid`; `remote relation not found`; `relation not remote`; `relation not cross-model`; `remote relation already registered`; `remote application has relations` ...

**Agent (workers importing the domain).** remoterelationconsumer

**Migration.** modelmigration package: True; legacy import registered: True; owned tables read by the generic export: 8 of 9.

## externalcontroller

**Identity.** Scope: controller database. Life column: none. Lifecycle kinds: deletable. Removal job types: none.

**State.**
- `external_controller` (controller) watched
- `external_controller_address` (controller) 
- `external_model` (controller) 
- views touching these tables: none

**Observation (Watch methods and who uses them).**
- none

**Dynamics (service mutators).** ImportExternalControllers, UpdateExternalController

**Interface (facades importing the domain).** none by import

**Failure.** 1 error constants: `external controller not found`

**Agent (workers importing the domain).** apiremoterelationcaller, externalcontrollerupdater

**Migration.** modelmigration package: True; legacy import registered: True; owned tables read by the generic export: 0 of 3.

## flag

**Identity.** Scope: controller database. Life column: none. Lifecycle kinds: append-only. Removal job types: none.

**State.**
- `flag` (controller) 
- views touching these tables: none

**Observation (Watch methods and who uses them).**
- none

**Dynamics (service mutators).** SetFlag

**Interface (facades importing the domain).** none by import

**Failure.** 0 error constants: 

**Agent (workers importing the domain).** none

**Migration.** modelmigration package: False; legacy import registered: False; owned tables read by the generic export: 0 of 1.

## keymanager

**Identity.** Scope: controller database. Life column: none. Lifecycle kinds: deletable. Removal job types: none.

**State.**
- `model_authorized_keys` (controller) watched
- `ssh_fingerprint_hash_algorithm` (controller) lookup: md5, sha256
- `user_public_ssh_key` (controller) 
- views touching these tables: v_model_authorized_keys

**Observation (Watch methods and who uses them).**
- none

**Dynamics (service mutators).** AddPublicKeysForUser, DeleteKeysForModel, DeleteKeysForUser, ImportAuthorizedKeys, ImportPublicKeysForUser

**Interface (facades importing the domain).** client/keymanager

**Failure.** 5 error constants: `public key already exists`; `import subject not found`; `invalid public key`; `key contains a reserved comment`; `unknown import source`

**Agent (workers importing the domain).** none

**Migration.** modelmigration package: True; legacy import registered: True; owned tables read by the generic export: 0 of 3.

## lease

**Identity.** Scope: controller database. Life column: none. Lifecycle kinds: deletable. Removal job types: none.

**State.**
- `lease` (controller) 
- `lease_pin` (controller) 
- `lease_type` (controller) lookup: application-leadership, backup-creation, singular-controller
- views touching these tables: none

**Observation (Watch methods and who uses them).**
- none

**Dynamics (service mutators).** DeleteLeadershipForModel, ImportApplicationLeadership, RevokeLease

**Interface (facades importing the domain).** none by import

**Failure.** 0 error constants: 

**Agent (workers importing the domain).** lease

**Migration.** modelmigration package: True; legacy import registered: True; owned tables read by the generic export: 0 of 3.

## logging

**Identity.** Scope: controller database. Life column: none. Lifecycle kinds: deletable. Removal job types: none.

**State.**
- `logging_loki_config` (controller) watched
- views touching these tables: none

**Observation (Watch methods and who uses them).**
- WatchLokiConfig: T2; facades ['agent/logger']; workers -

**Dynamics (service mutators).** DeleteLokiConfig, SetLokiConfig

**Interface (facades importing the domain).** agent/caasapplication, agent/logger

**Failure.** 1 error constants: `loki config not found`

**Agent (workers importing the domain).** controlsocket

**Migration.** modelmigration package: False; legacy import registered: False; owned tables read by the generic export: 0 of 1.

## machine

**Identity.** Scope: model database. Life column: model. Lifecycle kinds: life-column. Removal job types: machine.

**State.**
- `container_type` (model) lookup: lxd, none
- `instance_tag` (model) 
- `machine` (model) life watched
- `machine_agent_presence` (model) 
- `machine_agent_version` (model) 
- `machine_cloud_instance` (model) life watched
- `machine_cloud_instance_status` (model) status
- `machine_cloud_instance_status_value` (model) lookup: allocating, pending, provisioning error, running, unknown
- `machine_constraint` (model) 
- `machine_container_type` (model) 
- `machine_filesystem` (model) watched
- `machine_lxd_profile` (model) watched
- `machine_manual` (model) 
- `machine_parent` (model) watched
- `machine_placement` (model) 
- `machine_placement_scope` (model) lookup: provider
- `machine_platform` (model) 
- `machine_reprovision` (model) watched
- `machine_requires_reboot` (model) watched
- `machine_ssh_host_key` (model) watched
- `machine_status` (model) status
- `machine_status_value` (model) lookup: down, error, pending, started, stopped
- `machine_volume` (model) watched
- views touching these tables: v_application_constraint, v_constraint, v_hardware_characteristics, v_machine_agent_version, v_machine_cloud_instance_status, v_machine_constraint, v_machine_is_controller, v_machine_platform, v_machine_status, v_machine_target_agent_version, v_model_constraint, v_model_metrics

**Observation (Watch methods and who uses them).**
- WatchMachineCloudInstances: T2; facades ['agent/storageprovisioner']; workers ['storageprovisioner']
- WatchMachineContainerLife: T2; facades ['agent/provisioner']; workers ['computeprovisioner']
- WatchMachineLife: T2; facades ['agent/lifeflag']; workers -
- WatchMachineLifeAndDependants: T2; facades ['agent/machine']; workers -
- WatchMachineReboot: T0; facades -; workers -
- WatchMachineSSHHostKeys: T0; facades -; workers -
- WatchModelMachineLifeAndStartTimes: T1; facades ['client/controller', 'client/modelmanager']; workers ['instancepoller']
- WatchModelMachines: T1; facades ['agent/instancemutater', 'client/controller', 'client/modelmanager']; workers ['computeprovisioner', 'containerprovisioner', 'firewaller']
- WatchSSHHostKeysByMachineName: T3; facades -; workers ['sshtunneler']

**Dynamics (service mutators).** AddMachine, CreateMachine, CreateSubordinateMachine, SetKeepInstance, SetMachineCloudInstance, SetMachineHostname, SetSSHHostKeys

**Interface (facades importing the domain).** agent/agent, agent/diskmanager, agent/hostkeyreporter, agent/keyupdater, agent/machine, agent/machineactions, agent/provisioner, agent/reboot, agent/storageprovisioner, agent/uniter, agent/upgrader, client/application, client/machinemanager, client/modelconfig, client/storage

**Failure.** 23 error constants: `machine is dead`; `machine is not alive`; `machine not found`; `availability zone not found`; `machine not provisioned`; `invalid container type`; `grandparent machine are not supported currently`; `machine already exists`; `machine has no parent`; `machine cloud instance already exists`; `machine cloud instance changed`; `invalid machine constraints` ...

**Agent (workers importing the domain).** computeprovisioner, firewaller, instancepoller, storageprovisioner

**Migration.** modelmigration package: True; legacy import registered: True; owned tables read by the generic export: 19 of 23.

## model

**Identity.** Scope: controller, model database. Life column: controller, model. Lifecycle kinds: life-column. Removal job types: model, controller-model.

**State.**
- `model` (controller) life watched
- `model_database_deletion` (controller) watched
- `model_last_login` (controller) 
- `model_namespace` (controller) 
- `model_type` (controller) lookup: caas, iaas
- `model` (model) immutable
- `model_config` (model) watched
- `model_constraint` (model) 
- `model_life` (model) life watched
- `model_migrating` (model) immutable watched
- views touching these tables: v_cloud, v_model, v_model_all, v_model_config, v_model_constraint, v_model_constraint_space, v_model_constraint_tag, v_model_constraint_zone, v_model_secret_backend, v_model_state, v_permission_model, v_secret_owner, v_secret_permission, v_user_last_login

**Observation (Watch methods and who uses them).**
- WatchActivatedModels: T3; facades -; workers ['modelworkermanager']
- WatchModel: T3; facades -; workers ['modellife', 'modelworkermanager', 'objectstore', 'providertracker']
- WatchModelCloudCredential: T2; facades ['agent/caasagent', 'agent/credentialvalidator']; workers ['credentialvalidator', 'modelworkermanager', 'providertracker']
- WatchModelMigrationDeletions: T3; facades -; workers ['undertaker']
- WatchModelRemovals: T0; facades -; workers -
- WatchModels: T3; facades -; workers ['undertaker']

**Dynamics (service mutators).** CreateImportingModelWithAgentVersionStream, CreateModel, DeleteImportedModel, ImportModel, ImportModelLegacy, RemoveModelDatabaseDeletion, SetModelConstraints, UpdateCredential

**Interface (facades importing the domain).** agent/agent, agent/credentialvalidator, agent/migrationminion, agent/upgrader, client/applicationoffers, client/client, client/controller, client/machinemanager, client/modelconfig, client/modelmanager, client/modelupgrader, controller/caasoperatorupgrader, controller/migrationmaster, controller/migrationtarget

**Failure.** 13 error constants: `agent stream not valid`; `agent version not supported`; `model already exists`; `model already activated`; `model constraints not found`; `model constraint not found`; `model credential not valid`; `model namespace not found`; `model not found`; `secret backend already set`; `user not found on model`; `model not activated` ...

**Agent (workers importing the domain).** apiremoterelationcaller, credentialvalidator, errors.go, migrationflag, migrationmaster, modellife, objectstore, providertracker, toolsversionchecker, undertaker

**Migration.** modelmigration package: True; legacy import registered: True; owned tables read by the generic export: 4 of 9.

## modelagent

**Identity.** Scope: model database. Life column: none. Lifecycle kinds: append-only. Removal job types: none.

**State.**
- `agent_stream` (model) lookup: devel, proposed, released, testing
- `agent_version` (model) watched
- `model_agent` (model) 
- views touching these tables: v_machine_target_agent_version, v_model_config, v_unit_target_agent_version

**Observation (Watch methods and who uses them).**
- WatchMachineTargetAgentVersion: T2; facades ['agent/upgrader']; workers -
- WatchModelTargetAgentVersion: T2; facades ['agent/upgrader']; workers -
- WatchUnitTargetAgentVersion: T2; facades ['agent/upgrader']; workers -

**Dynamics (service mutators).** SetMachineReportedAgentVersion, SetModelAgentStream, SetUnitReportedAgentVersion, UpdateLatestAgentVersion

**Interface (facades importing the domain).** client/modelupgrader

**Failure.** 8 error constants: `agent stream not valid`; `agent version not found`; `agent version not set`; `agent version not supported`; `controller model cannot be upgraded`; `downgrade not supported`; `latest version downgrade not supported`; `missing agent binaries`

**Agent (workers importing the domain).** toolsversionchecker

**Migration.** modelmigration package: True; legacy import registered: True; owned tables read by the generic export: 3 of 3.

## network

**Identity.** Scope: model database. Life column: none. Lifecycle kinds: deletable. Removal job types: none.

**State.**
- `availability_zone` (model) 
- `availability_zone_subnet` (model) 
- `fqdn_address` (model) watched
- `hostname_address` (model) 
- `ip_address` (model) watched
- `ip_address_config_type` (model) lookup: dhcp, dhcpv6, loopback, manual, slaac, static, unknown
- `ip_address_origin` (model) lookup: machine, provider
- `ip_address_scope` (model) lookup: link-local, local-cloud, local-machine, public, unknown
- `ip_address_type` (model) lookup: ipv4, ipv6
- `link_layer_device` (model) watched
- `link_layer_device_dns_address` (model) 
- `link_layer_device_dns_domain` (model) 
- `link_layer_device_parent` (model) 
- `link_layer_device_route` (model) 
- `link_layer_device_type` (model) lookup: 802.1q, bond, bridge, ethernet, loopback, unknown, veth, vxlan
- `net_node` (model) 
- `net_node_fqdn_address` (model) watched
- `net_node_hostname_address` (model) 
- `network_address_scope` (model) lookup: local-cloud, local-host, public
- `provider_ip_address` (model) 
- `provider_link_layer_device` (model) 
- `provider_network` (model) 
- `provider_network_subnet` (model) 
- `provider_space` (model) 
- `provider_subnet` (model) 
- `space` (model) watched lookup: 656b4a82-e28c-53d6-a014-f0dd53417eb6
- `subnet` (model) watched
- `virtual_port_type` (model) lookup: , openvswitch
- views touching these tables: v_all_unit_address, v_application_constraint, v_hardware_characteristics, v_ip_address_with_names, v_machine_constraint, v_machine_is_controller, v_model_constraint_space, v_space_subnet, v_unit_relation_network

**Observation (Watch methods and who uses them).**
- WatchControllerNetwork: T3; facades -; workers ['apiaddresssetter']
- WatchSubnets: T3; facades -; workers ['firewaller']

**Dynamics (service mutators).** AddSpace, AddSubnet, ImportK8sServices, ImportLinkLayerDevices, MoveSubnetsToSpace, RemoveSpace, RemoveSubnet, SetMachineNetConfig, SetProviderNetConfig, UpdateSpace, UpdateSubnet

**Interface (facades importing the domain).** agent/machine, agent/provisioner, agent/uniter, client/client, client/modelconfig, client/spaces

**Failure.** 10 error constants: `host machine not provisioned`; `network node not found`; `space already exists`; `space not found`; `subnet not found`; `space name is not valid`; `subnet CIDR is not valid`; `availability zone not found`; `space requirement conflict`; `space requirements unsatisfiable`

**Agent (workers importing the domain).** apiaddresssetter, bootstrap, instancepoller

**Migration.** modelmigration package: True; legacy import registered: True; owned tables read by the generic export: 27 of 28.

## objectstore

**Identity.** Scope: controller, model database. Life column: controller. Lifecycle kinds: life-column. Removal job types: none.

**State.**
- `object_store_backend` (controller) life watched
- `object_store_backend_s3_config` (controller) 
- `object_store_backend_type` (controller) lookup: file, s3
- `object_store_drain_info` (controller) watched
- `object_store_drain_phase_type` (controller) lookup: completed, draining, error, unknown
- `object_store_metadata` (controller) 
- `object_store_metadata_path` (controller) watched
- `object_store_placement` (controller) 
- `object_store_metadata` (model) 
- `object_store_metadata_path` (model) watched
- `object_store_placement` (model) 
- views touching these tables: v_agent_binary_store, v_agent_binary_store, v_object_store_metadata, v_object_store_metadata

**Observation (Watch methods and who uses them).**
- WatchDraining: T3; facades -; workers ['objectstoredrainer', 'objectstoreguard']
- WatchObjectStoreBackend: T3; facades -; workers ['objectstoredrainer', 'objectstores3caller']

**Dynamics (service mutators).** AddControllerIDHint, RemoveMetadata, SetDrainingPhase

**Interface (facades importing the domain).** none by import

**Failure.** 16 error constants: `empty path`; `path not found`; `hash exists already exists`; `path already exists with different hash`; `missing hash`; `minimum hash prefix length is 7`; `invalid hash prefix`; `invalid hash`; `invalid hash length`; `draining phase not found`; `draining already in progress`; `missing controller ID` ...

**Agent (workers importing the domain).** controlsocket, objectstore, objectstoredrainer, objectstores3caller

**Migration.** modelmigration package: False; legacy import registered: False; owned tables read by the generic export: 3 of 8.

## operation

**Identity.** Scope: model database. Life column: none. Lifecycle kinds: append-only, pruned. Removal job types: none.

**State.**
- `operation` (model) 
- `operation_action` (model) 
- `operation_machine_task` (model) immutable
- `operation_parameter` (model) immutable
- `operation_task` (model) 
- `operation_task_log` (model) watched
- `operation_task_output` (model) 
- `operation_task_status` (model) status watched
- `operation_task_status_value` (model) lookup: aborted, aborting, cancelled, completed, error, failed, pending, running
- `operation_unit_task` (model) immutable
- views touching these tables: none

**Observation (Watch methods and who uses them).**
- WatchMachineTaskNotifications: T2; facades ['agent/machineactions', 'agent/uniter']; workers -
- WatchTaskLogs: T1; facades ['client/action']; workers -
- WatchUnitTaskNotifications: T2; facades ['agent/uniter']; workers -

**Dynamics (service mutators).** AddActionOperation, AddExecOperation, AddExecOperationOnAllMachines

**Interface (facades importing the domain).** agent/machineactions, agent/uniter, client/action

**Failure.** 3 error constants: `operation not found`; `task not found`; `task not pending`

**Agent (workers importing the domain).** none

**Migration.** modelmigration package: True; legacy import registered: True; owned tables read by the generic export: 7 of 10.

## port

**Identity.** Scope: model database. Life column: none. Lifecycle kinds: append-only. Removal job types: none.

**State.**
- `port_range` (model) watched
- `protocol` (model) lookup: icmp, tcp, udp
- views touching these tables: v_port_range

**Observation (Watch methods and who uses them).**
- WatchOpenedPorts: T3; facades -; workers ['firewaller']
- WatchOpenedPortsForApplication: T3; facades -; workers ['caasfirewaller']

**Dynamics (service mutators).** ImportOpenUnitPorts

**Interface (facades importing the domain).** client/client

**Failure.** 3 error constants: `unit not found`; `port range conflict`; `invalid endpoint(s)`

**Agent (workers importing the domain).** none

**Migration.** modelmigration package: True; legacy import registered: True; owned tables read by the generic export: 2 of 2.

## relation

**Identity.** Scope: model database. Life column: model. Lifecycle kinds: life-column. Removal job types: relation.

**State.**
- `application_endpoint` (model) watched
- `application_extra_endpoint` (model) 
- `relation` (model) life watched
- `relation_application_setting` (model) 
- `relation_application_settings_hash` (model) watched
- `relation_endpoint` (model) 
- `relation_status` (model) status
- `relation_status_type` (model) lookup: 0, 1, 2, 3, 4, 5
- `relation_unit` (model) watched
- `relation_unit_departure` (model) 
- `relation_unit_setting` (model) 
- `relation_unit_setting_archive` (model) 
- `relation_unit_settings_hash` (model) watched
- views touching these tables: v_application_endpoint, v_application_endpoint_uuid, v_application_subordinate, v_offer_detail, v_relation_endpoint, v_relation_endpoint_identifier, v_relation_status

**Observation (Watch methods and who uses them).**
- WatchRelatedUnits: T2; facades ['agent/uniter']; workers -
- WatchRelationLifeSuspendedStatus: T2; facades ['controller/crossmodelrelations']; workers -
- WatchRelationUnitApplicationLifeSuspendedStatus: T2; facades ['agent/uniter']; workers -
- WatchRelationUnits: T2; facades ['agent/uniter', 'controller/crossmodelrelations']; workers ['remoterelationconsumer', 'uniter']
- WatchRelationsLifeSuspendedStatusForApplication: T3; facades -; workers ['remoterelationconsumer']

**Dynamics (service mutators).** AddRelation, ImportConsumerProxyRelationSettingsAndUnits, ImportRelations, SetRelationErrorStatus, SetRelationRemoteApplicationAndUnitSettings, SetRelationUnitSettings, SetRemoteRelationSuspendedState

**Interface (facades importing the domain).** agent/uniter, client/application, client/client, client/controller, controller/crossmodelrelations, controller/crossmodelsecrets, controller/migrationmaster

**Failure.** 22 error constants: `ambiguous relation`; `application not found in relation`; `both endpoints are remote applications`; `no compatible endpoints found between applications`; `quota limit exceeded`; `cannot enter scope, unit or relation not alive`; `cannot enter scope, subordinate unit exists but is not alive`; `entering scope for peer relation`; `entering scope, unit application is a subordinate`; `potential relation unit not valid`; `relation endpoint not found`; `already exists` ...

**Agent (workers importing the domain).** firewaller, remoterelationconsumer

**Migration.** modelmigration package: True; legacy import registered: True; owned tables read by the generic export: 11 of 13.

## removal

**Identity.** Scope: model database. Life column: none. Lifecycle kinds: deletable, pruned. Removal job types: none.

**State.**
- `removal` (model) watched
- `removal_type` (model) lookup: application, charm secret, controller-model, machine, model, obsolete user secret revisions, relation, relation with remote consumer, relation with remote offerer, remote application offerer, resource, storage attachment, storage filesystem, storage filesystem attachment, storage instance, storage volume, storage volume attachment, storage volume attachment plan, unit, user secret
- views touching these tables: none

**Observation (Watch methods and who uses them).**
- WatchEntityRemovals: T0; facades -; workers -
- WatchRemovals: T3; facades -; workers ['removal']

**Dynamics (service mutators).** DeleteModel, MarkFilesystemAttachmentAsDead, MarkInstanceAsDead, MarkMachineAsDead, MarkStorageAttachmentAsDead, MarkUnitAsDead, MarkVolumeAttachmentAsDead, MarkVolumeAttachmentPlanAsDead, RemoveApplication, RemoveController, RemoveDeadFilesystem, RemoveDeadVolume, RemoveMachine, RemoveMigratingModel, RemoveModel, RemoveOffer, RemoveRelation, RemoveRelationWithRemoteConsumer, RemoveRelationWithRemoteOfferer, RemoveRemoteApplicationOfferer, RemoveRemoteApplicationOffererByApplicationUUID, RemoveStorageAttachment, RemoveStorageInstance, RemoveUnit

**Interface (facades importing the domain).** agent/machine, agent/provisioner, agent/storageprovisioner, agent/uniter, client/application, client/controller, client/machinemanager, client/modelmanager, client/storage, controller/crossmodelrelations

**Failure.** 22 error constants: `removal job type not supported`; `removal job type not valid`; `removal job args invalid`; `model removed`; `entity still alive`; `entity not dead`; `removal job incomplete`; `relation is cross model`; `units still in relation scope`; `machine has containers`; `machine has units`; `machine has storage` ...

**Agent (workers importing the domain).** caasapplicationprovisioner, remoterelationconsumer, removal, storageprovisioner, undertaker

**Migration.** modelmigration package: False; legacy import registered: False; owned tables read by the generic export: 2 of 2.

## resource

**Identity.** Scope: model database. Life column: none. Lifecycle kinds: deletable. Removal job types: resource.

**State.**
- `application_resource` (model) 
- `pending_application_resource` (model) 
- `resource` (model) 
- `resource_container_image_metadata_store` (model) 
- `resource_file_store` (model) 
- `resource_image_store` (model) 
- `resource_origin_type` (model) lookup: store, upload
- `resource_retrieved_by` (model) 
- `resource_retrieved_by_type` (model) lookup: application, unit, user
- `resource_state` (model) lookup: available, potential
- `unit_resource` (model) 
- views touching these tables: v_application_resource, v_charm_container, v_resource, v_unit_resource

**Observation (Watch methods and who uses them).**
- none

**Dynamics (service mutators).** AddResourcesBeforeApplication, DeleteApplicationResources, DeleteResourcesAddedBeforeApplication, DeleteUnitResources, ImportResources, SetRepositoryResources, SetUnitResource, UpdateUploadResource

**Interface (facades importing the domain).** agent/resourceshookcontext, client/resources

**Failure.** 14 error constants: `charm ID not valid`; `argument not valid`; `resource not found`; `charm resource not found`; `retrieved by type not valid`; `resource name not valid`; `resource state not valid`; `cleanup state not valid`; `stored resource not found`; `resource revision not valid`; `stored resource already exists`; `resource already found in storage` ...

**Agent (workers importing the domain).** charmrevisioner

**Migration.** modelmigration package: True; legacy import registered: True; owned tables read by the generic export: 10 of 11.

## secret

**Identity.** Scope: model database. Life column: none. Lifecycle kinds: deletable, pruned. Removal job types: user secret, obsolete user secret revisions, charm secret.

**State.**
- `secret` (model) 
- `secret_application_owner` (model) 
- `secret_content` (model) 
- `secret_deleted_value_ref` (model) watched
- `secret_grant_scope_type` (model) lookup: application, model, relation, unit
- `secret_grant_subject_type` (model) lookup: application, model, unit
- `secret_metadata` (model) watched
- `secret_model_owner` (model) 
- `secret_permission` (model) 
- `secret_reference` (model) watched
- `secret_remote_unit_consumer` (model) 
- `secret_reservation` (model) 
- `secret_revision` (model) watched
- `secret_revision_expire` (model) watched
- `secret_revision_obsolete` (model) watched
- `secret_role` (model) lookup: manage, none, view
- `secret_rotate_policy` (model) lookup: daily, hourly, monthly, never, quarterly, weekly, yearly
- `secret_rotation` (model) watched
- `secret_unit_consumer` (model) 
- `secret_unit_owner` (model) 
- `secret_value_ref` (model) 
- views touching these tables: v_secret_metadata, v_secret_owner, v_secret_permission

**Observation (Watch methods and who uses them).**
- WatchConsumedSecretsChanges: T2; facades ['agent/secretsmanager', 'controller/crossmodelrelations']; workers ['remoterelationconsumer', 'uniter']
- WatchDeletedSecrets: T2; facades ['agent/secretsmanager']; workers -
- WatchObsoleteSecrets: T2; facades ['agent/secretsmanager']; workers -
- WatchObsoleteUserSecretsToPrune: T2; facades ['controller/usersecrets']; workers ['secretspruner']
- WatchSecretRevisionsExpiryChanges: T2; facades ['agent/secretsmanager']; workers ['secretexpire']
- WatchSecretsRotationChanges: T2; facades ['agent/secretsmanager']; workers ['secretrotate']

**Dynamics (service mutators).** ChangeSecretBackend, CreateSecretURIs, CreateUserSecret, DeleteObsoleteUserSecretRevisions, DeleteSecret, GrantSecretAccess, ImportSecrets, RevokeSecretAccess, UpdateUserSecret

**Interface (facades importing the domain).** agent/secretsmanager, agent/uniter, client/modelconfig, client/modelmanager, client/secretbackends, client/secrets, controller/crossmodelrelations, controller/crossmodelsecrets, controller/usersecretsdrain

**Failure.** 10 error constants: `permission denied`; `secret not found`; `secret is from a different model`; `secret label already exists`; `secret revision not found`; `secret consumer not found`; `charm secrets do not support auto prune`; `cannot change a secret permission scope or subject type`; `secret access scope not found`; `missing secret backend id`

**Agent (workers importing the domain).** secretsdrainworker, uniter

**Migration.** modelmigration package: True; legacy import registered: True; owned tables read by the generic export: 20 of 21.

## secretbackend

**Identity.** Scope: controller database. Life column: none. Lifecycle kinds: deletable. Removal job types: none.

**State.**
- `model_secret_backend` (controller) watched
- `secret_backend` (controller) immutable
- `secret_backend_config` (controller) 
- `secret_backend_origin` (controller) lookup: built-in, user
- `secret_backend_reference` (controller) 
- `secret_backend_rotation` (controller) watched
- `secret_backend_type` (controller) lookup: controller, kubernetes, vault
- views touching these tables: v_model_secret_backend

**Observation (Watch methods and who uses them).**
- WatchModelSecretBackendChanged: T3; facades -; workers ['secretsdrainworker']
- WatchSecretBackendRotationChanges: T3; facades -; workers ['secretbackendrotate']

**Dynamics (service mutators).** AddSecretBackendReference, Changes, CreateSecretBackend, DeleteSecretBackend, ImportSecretBackendReferences, SetModelSecretBackend, UpdateSecretBackend

**Interface (facades importing the domain).** agent/secretsmanager, client/modelconfig, client/modelmanager, client/secretbackends, client/secrets, controller/crossmodelsecrets, controller/usersecretsdrain

**Failure.** 7 error constants: `secret backend already exists`; `secret backend reference count already exists`; `secret backend reference count not found`; `secret backend not found`; `secret backend not valid`; `secret backend operation forbidden`; `secret backend not supported`

**Agent (workers importing the domain).** secretsdrainworker

**Migration.** modelmigration package: False; legacy import registered: False; owned tables read by the generic export: 0 of 7.

## sequence

**Identity.** Scope: model database. Life column: none. Lifecycle kinds: append-only. Removal job types: none.

**State.**
- `sequence` (model) 
- views touching these tables: none

**Observation (Watch methods and who uses them).**
- none

**Dynamics (service mutators).** ImportSequences

**Interface (facades importing the domain).** none by import

**Failure.** 1 error constants: `duplicate namespace sequence`

**Agent (workers importing the domain).** none

**Migration.** modelmigration package: True; legacy import registered: True; owned tables read by the generic export: 1 of 1.

## ssh

**Identity.** Scope: controller, model database. Life column: none. Lifecycle kinds: deletable, pruned. Removal job types: none.

**State.**
- `controller_ssh_host_key` (controller) 
- `controller_ssh_server_port` (controller) watched
- `ssh_key_algorithm_type` (controller) lookup: ecdsa-sha2-nistp256, ssh-ed25519, ssh-rsa
- `machine_virtual_ssh_host_key` (model) 
- `ssh_connection_request` (model) watched
- `ssh_key_algorithm_type` (model) lookup: ecdsa-sha2-nistp256, ssh-ed25519, ssh-rsa
- `unit_virtual_ssh_host_key` (model) 
- views touching these tables: none

**Observation (Watch methods and who uses them).**
- WatchSSHConnRequest: T2; facades ['agent/sshsession']; workers ['sshsession']
- WatchSSHServerPort: T3; facades -; workers ['firewaller', 'sshserver']

**Dynamics (service mutators).** RemoveSSHConnRequest, SetSSHServerPort

**Interface (facades importing the domain).** agent/sshsession

**Failure.** 1 error constants: `ssh server port not found`

**Agent (workers importing the domain).** sshserver, sshtunneler

**Migration.** modelmigration package: False; legacy import registered: False; owned tables read by the generic export: 4 of 6.

## storage

**Identity.** Scope: model database. Life column: model. Lifecycle kinds: life-column. Removal job types: storage instance, storage attachment, storage volume, storage filesystem, storage volume attachment, storage volume attachment plan, storage filesystem attachment.

**State.**
- `application_storage_directive` (model) 
- `model_storage_pool` (model) 
- `storage_attachment` (model) life watched
- `storage_filesystem` (model) life watched
- `storage_filesystem_attachment` (model) life watched
- `storage_filesystem_status` (model) status
- `storage_filesystem_status_value` (model) lookup: attached, attaching, destroying, detached, detaching, error, pending, tombstone
- `storage_instance` (model) life
- `storage_instance_filesystem` (model) watched
- `storage_instance_volume` (model) watched
- `storage_kind` (model) lookup: block, filesystem
- `storage_pool` (model) 
- `storage_pool_attribute` (model) 
- `storage_pool_origin` (model) lookup: provider-default, user
- `storage_provision_scope` (model) lookup: machine, model
- `storage_unit_owner` (model) 
- `storage_volume` (model) life watched
- `storage_volume_attachment` (model) life watched
- `storage_volume_attachment_plan` (model) life watched
- `storage_volume_attachment_plan_attr` (model) 
- `storage_volume_device_type` (model) lookup: iscsi, local
- `storage_volume_status` (model) status
- `storage_volume_status_value` (model) lookup: attached, attaching, destroying, detached, detaching, error, pending, tombstone
- `unit_storage_directive` (model) 
- views touching these tables: none

**Observation (Watch methods and who uses them).**
- none

**Dynamics (service mutators).** CreateStoragePool, DeleteStoragePool, ImportFilesystemsCAAS, ImportFilesystemsIAAS, ImportStorageInstances, ImportStoragePools, ImportVolumes, ReplaceStoragePool, SetRecommendedStoragePools

**Interface (facades importing the domain).** agent/storageprovisioner, agent/uniter, client/application, client/client, client/machinemanager, client/storage

**Failure.** 14 error constants: `filesystem not found`; `invalid storage name`; `provider type is invalid`; `storage provider type not found`; `pooled storage entity not found`; `storage entity adoption is not supported`; `storage attachment not found`; `storage instance not alive`; `storage instance not found`; `storage pool already exists`; `storage pool name is invalid`; `storage pool is not found` ...

**Agent (workers importing the domain).** bootstrap, caasapplicationprovisioner, storageprovisioner

**Migration.** modelmigration package: True; legacy import registered: True; owned tables read by the generic export: 18 of 24.

## tracing

**Identity.** Scope: controller database. Life column: none. Lifecycle kinds: deletable. Removal job types: none.

**State.**
- `charm_tracing_config` (controller) 
- `workload_tracing_config` (controller) watched
- views touching these tables: none

**Observation (Watch methods and who uses them).**
- WatchWorkloadTracingConfig: T2; facades ['agent/tracer']; workers ['trace']

**Dynamics (service mutators).** SetCharmTracingConfig, SetWorkloadTracingConfig

**Interface (facades importing the domain).** agent/caasapplication, agent/provisioner, agent/tracer, agent/uniter

**Failure.** 0 error constants: 

**Agent (workers importing the domain).** caasmodeloperator, controlsocket, trace

**Migration.** modelmigration package: False; legacy import registered: False; owned tables read by the generic export: 0 of 2.

## upgrade

**Identity.** Scope: controller database. Life column: none. Lifecycle kinds: append-only. Removal job types: none.

**State.**
- `upgrade_info` (controller) watched
- `upgrade_info_controller_node` (controller) watched
- `upgrade_state_type` (controller) lookup: created, db-completed, error, started, steps-completed
- views touching these tables: none

**Observation (Watch methods and who uses them).**
- WatchForUpgradeReady: T3; facades -; workers ['upgradedatabase']
- WatchForUpgradeState: T3; facades -; workers ['upgradedatabase', 'upgradestepscontroller']

**Dynamics (service mutators).** CreateUpgrade, SetControllerDone, SetControllerReady, SetDBUpgradeCompleted, SetDBUpgradeFailed

**Interface (facades importing the domain).** none by import

**Failure.** 3 error constants: `upgrade already started`; `upgrade already exists`; `upgrade not found`

**Agent (workers importing the domain).** upgradedatabase, upgradestepscontroller

**Migration.** modelmigration package: False; legacy import registered: False; owned tables read by the generic export: 0 of 3.

