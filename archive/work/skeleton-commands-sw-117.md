# CLI invocation page structures: secret-backends through whoami — 117

Proposal for the 48 generated CLI pages listed at `work/skeleton-nested-117.md:193-198`, not a generated reference or a complete option/error inventory. Every entry is an individual invocation interface. Read the labels in order as proposed page sections: **Target**, **Inputs/scope**, **Operation/output**, and **Conditions** where traced, followed by the affected semantic subject. Source paths are relative to `/tmp/juju-41-tree` at `e5db99d585`. A successful request, observed controller record, local client state, and eventual provider/agent outcome are different things. These are bounded static traces, not evidence of a live execution. Alphabetical order is a manifest convenience, not semantic ownership.

## `secret-backends`

1. **Target:** inspect secret-backend summaries on a controller. 2. **Inputs/scope:** controller selection, output format and optional reveal. 3. **Operation/output:** `ListSecretBackends` API read with no name filter; format backend type, status and secret counts, or report none. 4. **Conditions:** tabular output disables reveal; the facade checks admin access for a reveal request (`cmd/juju/secretbackends/list.go:84-107,111-145`; `apiserver/facades/client/secretbackends/secrets.go:140-168`). **Subject:** secret backend and controller.

## `secrets`

1. **Target:** list secrets in a model. 2. **Inputs/scope:** optional application/unit owner, revision-metadata display and output format. 3. **Operation/output:** `ListSecrets` API read with owner filter, then format returned information. Without owner the traced facade lists general secrets; with owner it calls the charm-secret list. 4. **Conditions:** invalid owner fails; the command registers no reveal flag even though its run path contains reveal handling. The facade checks read access for ordinary listing (`cmd/juju/secrets/list.go:25-33,51-56,86-95,152-184`; `apiserver/facades/client/secrets/secrets.go:66-75,92-120`). **Subject:** secret, owner and revision.

## `set-constraints`

1. **Target:** change constraints for one application, not the model default. 2. **Inputs/scope:** valid application name and parsed constraint arguments in selected model. 3. **Operation/output:** send `SetConstraints` to application API; return the result rather than a machine provisioning outcome. 4. **Conditions:** the facade checks write access and the model change block, then resolves the application (`cmd/juju/application/constraints.go:179-201`; `apiserver/facades/client/application/application.go:1393-1415`). **Subject:** application and constraints.

## `set-credential`

1. **Target:** change the selected model's cloud-credential reference, not edit the credential's content. 2. **Inputs/scope:** cloud and credential names, current account and model. 3. **Operation/output:** inspect controller credentials; if the named one is not found remotely, look locally and upload it, then call `ChangeModelCredential` and report the changed reference. 4. **Conditions:** remote lookup failure can fall back to local lookup; the change facade checks controller superuser or model admin and the model change block. Upload can succeed before a later reference change fails (`cmd/juju/model/setcredential.go:81-93,97-163`; `apiserver/facades/client/modelmanager/modelmanager.go:1357-1400`). **Subject:** model and credential.

## `set-firewall-rule`

1. **Target:** deprecated interface to selected model's service allowlist configuration, not direct proof of applied firewall behavior. 2. **Inputs/scope:** service `ssh` or `juju-application-offer`, comma-separated CIDRs. 3. **Operation/output:** print deprecation warning; call `ModelSet` for the corresponding SSH-allow or ingress-allow config key. 4. **Conditions:** a valid allowlist is required; conflicting allowlist flags, unsupported service and invalid CIDR fail (`cmd/juju/firewall/setrule.go:81-117,126-153`). **Subject:** model configuration and firewall rule.

## `set-model-constraints`

1. **Target:** change selected model's constraints, distinct from application constraints. 2. **Inputs/scope:** parsed constraint arguments. 3. **Operation/output:** send `SetModelConstraints` to model-config API; return result rather than later resource allocation. 4. **Conditions:** facade checks write access and change block and maps model/space/container errors (`cmd/juju/model/constraints.go:164-189`; `apiserver/facades/client/modelconfig/modelconfig.go:339-370`). **Subject:** model and constraints.

## `show-action`

1. **Target:** inspect a charm action's definition for an application, not the result of an invocation. 2. **Inputs/scope:** application and action name in selected model. 3. **Operation/output:** read `ApplicationCharmActions`, select action, print description and YAML argument properties. 4. **Conditions:** missing or invalid input and unknown action fail; the traced action facade checks write access even for this lookup (`cmd/juju/action/show.go:38-54,72-112`; `apiserver/facades/client/action/action.go:228-245,252-254`). **Subject:** charm action and application; contrast `show-task`.

## `show-application`

1. **Target:** inspect one or more model applications. 2. **Inputs/scope:** validated application names and format. 3. **Operation/output:** `ApplicationsInfo` API read and formatted application-keyed output. 4. **Conditions:** per-application errors are combined and returned before formatting, rather than printing partial successes (`cmd/juju/application/show.go:69-94,110-144`). **Subject:** application and endpoint binding.

## `show-cloud`

1. **Target:** inspect one named cloud definition, with local and controller copies distinguished. 2. **Inputs/scope:** cloud name, source selection, format and optional available configuration details. 3. **Operation/output:** read local metadata and/or request controller cloud info; render each selected copy, including separate errors or missing notices. 4. **Conditions:** a local and controller definition can differ, so a successful read of one is not proof of the other (`cmd/juju/cloud/show.go:86-106,124-178,181-236,254-266`). **Subject:** cloud definition and controller.

## `show-controller`

1. **Target:** inspect named controllers, or the locally current controller if none named. 2. **Inputs/scope:** local controller records and per-controller API access. 3. **Operation/output:** combine stored information with remote version, access and other controller details; when access is superuser, request all models and update the client model cache; format a controller-keyed result. 4. **Conditions:** some remote errors are attached to output while connection/store failures return; absence of a model listing for other access levels is not proof that the controller has no models (`cmd/juju/controller/showcontroller.go:66-69,139-194,208-224,226-265`). **Subject:** controller, client registration and model.

## `show-credential`

1. **Target:** inspect locally stored and/or controller credential records. 2. **Inputs/scope:** zero arguments for all or both cloud and credential names; source selection and optional secret-attribute display. 3. **Operation/output:** local cache read and/or `CredentialContents` API read, then render separately labeled copies. 4. **Conditions:** one positional name alone fails; local secret attributes are removed unless requested; no entries produce a notice (`cmd/juju/cloud/showcredential.go:52-77,98-145,147-182`). **Subject:** cloud credential and controller.

## `show-machine`

1. **Target:** inspect selected machines' model status. 2. **Inputs/scope:** machine IDs and output/time format. 3. **Operation/output:** fetch full model status using `Status(ctx, nil)`, then locally select and format machines; this is not a machine-scoped API query. 4. **Conditions:** a partial status can be printed with an error on stderr; no result fails (`cmd/juju/machine/show.go:42-58`; `cmd/juju/machine/base.go:63-88`). **Subject:** machine and model status.

## `show-model`

1. **Target:** inspect one selected model. 2. **Inputs/scope:** optional model identifier resolved to model UUID and controller. 3. **Operation/output:** `ModelInfo` API read and model-keyed formatted record. 4. **Conditions:** per-model API errors propagate, with redirect information handled specially (`cmd/juju/model/show.go:77-122,125-155`). **Subject:** model and controller.

## `show-offer`

1. **Target:** inspect a cross-model application offer. 2. **Inputs/scope:** one offer URL or valid application-name shorthand; missing model and qualifier are resolved from current model/account, and source can select another controller. 3. **Operation/output:** `ApplicationOffer` API read, convert returned access/endpoints/users and format by offer. 4. **Conditions:** malformed non-name input, resolution and API errors propagate (`cmd/juju/crossmodel/show.go:65-70,87-150,159-167`). **Subject:** application offer, controller and cross-model relation.

## `show-operation`

1. **Target:** inspect an operation's aggregate result, not one task's streamed output. 2. **Inputs/scope:** validated operation ID; optional wait or indefinite watch, time and output format. 3. **Operation/output:** default takes one API snapshot; waiting repeatedly fetches the operation until it is no longer pending/running and formats the result. 4. **Conditions:** watch and wait conflict; timeout while pending/running returns an error (`cmd/juju/action/showoperation.go:59-69,89-138,141-194`). **Subject:** operation and task.

## `show-secret`

1. **Target:** inspect one model secret. 2. **Inputs/scope:** URI or name, optional specific revision, revision metadata or reveal. 3. **Operation/output:** call `ListSecrets` with URI/name/revision filter and format returned detail including grants. 4. **Conditions:** revisions conflicts with reveal or an explicit revision; negative revision and no result fail; reveal path's facade requires admin (`cmd/juju/secrets/show.go:84-116,120-153`; `apiserver/facades/client/secrets/secrets.go:66-75`). **Subject:** secret, revision and grant.

## `show-secret-backend`

1. **Target:** inspect one controller secret backend. 2. **Inputs/scope:** backend name, output format and optional reveal. 3. **Operation/output:** call `ListSecretBackends` with a name filter and format detail; an empty result prints a no-backends notice rather than a not-found error. 4. **Conditions:** missing name fails; the facade checks admin access for a reveal request (`cmd/juju/secretbackends/show.go:78-109`; `apiserver/facades/client/secretbackends/secrets.go:140-147`). **Subject:** secret backend.

## `show-space`

1. **Target:** inspect one network space in the selected model. 2. **Inputs/scope:** exactly one name and format. 3. **Operation/output:** `ShowSpace` API read and output space/subnets, applications and machine count. 4. **Conditions:** unsupported and unauthorized errors receive distinct messages; request errors return (`cmd/juju/space/show.go:72-120`). **Subject:** space, subnet and application binding.

## `show-status-log`

1. **Target:** inspect status history for one model entity, distinct from the current `status` snapshot. 2. **Inputs/scope:** history kind and entity, with model kind requiring no entity; one of count, days or date filters, default count 20. 3. **Operation/output:** resolve entity tag, request `StatusHistory` from available controller clients, merge and sort records by time. 4. **Conditions:** incompatible filters/invalid kind or entity fail; multiple-client connection failures may warn, and no status history fails (`cmd/juju/status/history.go:140-198,213-311,340-380`). **Subject:** status history, model and entity.

## `show-storage`

1. **Target:** inspect one or more model storage instances. 2. **Inputs/scope:** validated storage IDs and output format. 3. **Operation/output:** `StorageDetails` API read, then format results. 4. **Conditions:** missing/invalid IDs fail; per-instance errors are combined and returned instead of partial formatted output (`cmd/juju/storage/show.go:53-58,78-130`). **Subject:** storage instance.

## `show-task`

1. **Target:** inspect one task result, distinct from an aggregate operation. 2. **Inputs/scope:** validated task ID, optional bounded wait or indefinite watch, output format. 3. **Operation/output:** default reads one task result; while waiting on pending/running task, subscribe to action progress and poll the result, stream logs, then format final result. 4. **Conditions:** watch and wait conflict; request/watcher errors return (`cmd/juju/action/showtask.go:69-80,101-119,124-186`). **Subject:** task, action and operation.

## `show-unit`

1. **Target:** inspect one or more units in a model. 2. **Inputs/scope:** valid unit names and optional endpoint, related-unit and application-data filters. 3. **Operation/output:** `UnitsInfo` API read and unit-keyed formatted information, with relation data filtered locally. 4. **Conditions:** invalid names and any per-unit result errors fail before formatted output (`cmd/juju/application/showunit.go:89-119,137-175,189-260`). **Subject:** unit and relation data.

## `show-user`

1. **Target:** inspect one controller user. 2. **Inputs/scope:** optional username defaults to stored current account; exact-time/format options. 3. **Operation/output:** `UserInfo` API read excluding disabled users, convert one record and output it. 4. **Conditions:** request errors or result counts other than one fail; local users receive connection/creation times in the conversion (`cmd/juju/user/info.go:53-55,97-106,116-165`). **Subject:** user and controller access.

## `spaces`

1. **Target:** inspect model network spaces. 2. **Inputs/scope:** selected model; optional short form. 3. **Operation/output:** `ListSpaces` API read; render space names alone or detailed records in chosen format, with an empty notice. 4. **Conditions:** unsupported or other API errors are returned (`cmd/juju/space/list.go:70-114,117-127,167-170`). **Subject:** space and subnet.

## `ssh`

1. **Target:** connect to a model machine or unit. 2. **Inputs/scope:** target, optional remote command and SSH options; jump is default, direct uses container provider for CAAS or machine provider otherwise. 3. **Operation/output:** initialize selected provider, resolve target, optionally populate proxy routing, then open SSH; terminal detection supplies PTY default. Output/termination follow that connection, not a controller mutation acknowledgement. 4. **Conditions:** missing target and incompatible direct/show-command fail; resolution or connection errors propagate (`cmd/juju/ssh/ssh.go:214-265,302-338`). **Subject:** machine, unit and compute access.

## `ssh-keys`

1. **Target:** inspect keys used in selected model. 2. **Inputs/scope:** fingerprint default or full-key display. 3. **Operation/output:** key-manager `ListKeys` read, then print model identifier and returned keys; report empty results. 4. **Conditions:** the implementation supplies `admin` as key-manager user; request and individual result errors propagate (`cmd/juju/sshkeys/list_sshkeys.go:70-108`). **Subject:** SSH key and model.

## `status`

1. **Target:** observe selected model's current status, not a completion guarantee. 2. **Inputs/scope:** filters, format, optional relations and storage sections. 3. **Operation/output:** request status with patterns and storage selection, format response; print empty-model or no-match message as applicable. Partial status can be printed alongside an error. 4. **Conditions:** a failed request is retried up to configured count except model migration; a complete failure returns error (`cmd/juju/status/status.go:145-184,187-208,230-238,241-284,291-344,357-365`). **Subject:** model status, application, unit and storage.

## `storage`

1. **Target:** list selected model's storage and its filesystem/volume views. 2. **Inputs/scope:** default combined view or filesystem-only/volume-only with IDs. 3. **Operation/output:** API-backed combined info is formatted; empty tabular result gives a notice. 4. **Conditions:** filesystem and volume flags are mutually exclusive; IDs need one of them (`cmd/juju/storage/list.go:74-132,143-167`). **Subject:** storage instance, filesystem and volume.

## `storage-pools`

1. **Target:** list model storage pool definitions. 2. **Inputs/scope:** optional provider-type and pool-name filters. 3. **Operation/output:** `ListPools` API read and formatted returned records, or empty notice. 4. **Conditions:** API errors propagate (`cmd/juju/storage/poollist.go:104-133`). **Subject:** storage pool and storage provider.

## `subnets`

1. **Target:** inspect model subnets. 2. **Inputs/scope:** optional space and zone filters; no positional arguments. 3. **Operation/output:** `ListSubnets` API read; output CIDR-keyed subnet information including provider IDs, zones, space and interpreted lifecycle. 4. **Conditions:** invalid space, invalid returned CIDR/space or API errors fail; no results have an appropriate notice (`cmd/juju/subnet/list.go:76-125,130-168`). **Subject:** subnet and space.

## `suspend-relation`

1. **Target:** request suspension of relations in a selected model. 2. **Inputs/scope:** one or more nonnegative relation IDs and optional reason. 3. **Operation/output:** `SetRelationSuspended(ids, true, message)` API mutation; return its result, not proof all subsequent effects have completed. 4. **Conditions:** invalid IDs fail before call; model change-block errors are processed (`cmd/juju/application/suspendrelation.go:72-105`). **Subject:** relation/integration.

## `switch`

1. **Target:** inspect or change the client's current controller/model selection. 2. **Inputs/scope:** optional target, controller/model flag or previous-selection shorthand; unqualified target is ambiguous. 3. **Operation/output:** without target print current selection; otherwise try an ambiguous name as controller before model and update selection through client-store helpers, logging the transition. Model resolution may use the API; this is not a model mutation. 4. **Conditions:** conflicting flags and controller/model environment overrides reject switching (`cmd/juju/commands/switch.go:103-145,201-289,296-301`). **Subject:** client selection, model and controller.

## `sync-agent-binary`

1. **Target:** synchronize agent binaries rather than start an upgrade. 2. **Inputs/scope:** required agent version; stream/source, dry-run and optional local destination. 3. **Operation/output:** construct a sync context; local destination writes storage/metadata (optionally mirrors), otherwise use model-upgrader upload API; dry-run is passed into sync. Progress is logged and API success does not establish an agent is running the binary. 4. **Conditions:** invalid/missing version and blocked sync errors return (`cmd/juju/commands/synctools.go:78-96,117-164,174-176`). **Subject:** agent binary and agent-version.

## `trust`

1. **Target:** set or remove an application's trust configuration in selected model. 2. **Inputs/scope:** application, optional remove, scope. 3. **Operation/output:** `SetConfig` API mutation sends trust true or false; returned call result is not evidence of later provider access. 4. **Conditions:** granting trust in CAAS requires scope `cluster`; model change-block errors are handled (`cmd/juju/application/trust.go:68-71,88-121`). **Subject:** application trust and model.

## `unexpose`

1. **Target:** request removal of application exposure in selected model. 2. **Inputs/scope:** application name and optional comma-delimited endpoints. 3. **Operation/output:** send `Unexpose` to application API; completion of request is distinct from later network behavior. 4. **Conditions:** missing application fails locally; change-block errors are processed (`cmd/juju/application/unexpose.go:78-88,104-112`). **Subject:** application exposure and endpoint.

## `unregister`

1. **Target:** remove a controller's connection information from the local client, not destroy the controller. 2. **Inputs/scope:** validated controller name; confirmation policy. 3. **Operation/output:** look up client-store entry, request confirmation when needed, then `RemoveController` locally. 4. **Conditions:** missing/invalid/unknown name and declined confirmation fail (`cmd/juju/controller/unregister.go:77-88,94-115`). **Subject:** client controller registration.

## `update-cloud`

1. **Target:** update cloud definition in selected client and/or controller copy. 2. **Inputs/scope:** cloud name and optional definition file, destination selection. 3. **Operation/output:** read supplied file; local destination requires it and writes local metadata; controller destination sends supplied definition or the local definition via `UpdateCloud`; report individual outcomes. 4. **Conditions:** destinations are processed separately, so local success does not imply controller success (`cmd/juju/cloud/updatecloud.go:93-108,126-178,191-209`). **Subject:** cloud definition and controller.

## `update-credential`

1. **Target:** update cloud credential content, not a model's credential reference. 2. **Inputs/scope:** optional cloud and credential filters, credentials file or local cache, region, destination and force. 3. **Operation/output:** select input, possibly update local credentials, and separately verify/upload remote credentials via controller API, printing per-result/model information. 4. **Conditions:** no file and no cloud returns usage; failures can coexist with work for other entries or destinations. Controller-side owner/admin and forced-update conditions and the limits of model validation are separately traced in `work/skeleton-control-117.md` § `credential`; no promise of live resource reachability (`cmd/juju/cloud/updatecredential.go:140-198,281-344,347-396,421-455`; `apiserver/facades/client/cloud/cloud.go:524-575`; `domain/credential/service/service.go:284-373`). **Subject:** credential, cloud and model.

## `update-k8s`

1. **Target:** update a Kubernetes cloud definition and possibly associated controller credential. 2. **Inputs/scope:** cloud name, optional file and client/controller destinations; built-in, file or local metadata are distinct sources. 3. **Operation/output:** reject non-Kubernetes definition; if a credential is available, check cluster metadata; update selected local metadata/proxy and/or send `UpdateCloud` and optional credential update to controller, reporting outcomes separately. 4. **Conditions:** a built-in cloud rejects a supplied file; the check is conditional on having a credential and is not a general guarantee of deployed operation (`cmd/juju/caas/update.go:131-153,216-275,277-324,327-336`). **Subject:** Kubernetes cloud, credential and controller.

## `update-public-clouds`

1. **Target:** refresh published public-cloud metadata in selected client and/or controller copies. 2. **Inputs/scope:** destination selection. 3. **Operation/output:** fetch published list, optionally compare/write local copy, then update controller copy if selected; print result or errors. 4. **Conditions:** retrieval with no returned clouds aborts; a local write failure can coexist with a usable list and attempted controller update (`cmd/juju/cloud/updatepublicclouds.go:143-177,187-218,221-231`). **Subject:** public cloud definitions and client/controller copies.

## `update-secret`

1. **Target:** request update of an existing model secret. 2. **Inputs/scope:** secret URI or name, data, optional new name, description and auto-prune. 3. **Operation/output:** pass these values to `UpdateSecret` API; its return is a request result, not proof of observer convergence. 4. **Conditions:** missing identifier fails locally; an unparseable URI is treated as a name (`cmd/juju/secrets/update.go:98-123`). **Subject:** secret, revision and observer.

## `update-secret-backend`

1. **Target:** update a controller secret-backend definition. 2. **Inputs/scope:** backend name, configuration file/key-values or resets, optional force; name and token rotation interval are extracted from attributes. 3. **Operation/output:** merge attributes, form update request and call `UpdateSecretBackend`. 4. **Conditions:** an update requires at least one config/reset source; request includes force rather than proving backend reachability (`cmd/juju/secretbackends/update.go:101-124,130-164`). **Subject:** secret backend and secret storage.

## `update-storage-pool`

1. **Target:** change a model storage-pool definition. 2. **Inputs/scope:** pool name and configuration key-values; a type key is extracted separately as provider type. 3. **Operation/output:** call `UpdatePool` API and return its result; no claim about already provisioned storage. 4. **Conditions:** missing name/attributes and malformed key-values fail (`cmd/juju/storage/poolupdate.go:60-80,99-110`). **Subject:** storage pool and provider.

## `upgrade-controller`

1. **Target:** initiate controller upgrade through its controller model. 2. **Inputs/scope:** selected controller, optional version/stream, dry-run, agent-version check override and optional local build. 3. **Operation/output:** inspect locally recorded account access and controller model; choose explicit/server-selected/built target and call `UpgradeModel` with controller-model UUID. A start/result is not agent convergence. 4. **Conditions:** last-known access must be superuser; build-agent is rejected for CAAS and cannot be combined with explicit version; further server prechecks and eventual propagation belong to controller-upgrade (`cmd/juju/commands/upgradecontroller.go:103-112,182-211,369-401,414-432`; `work/skeleton-control-117.md` § `controller-upgrade`). **Subject:** controller-upgrade and agent-version.

## `upgrade-model`

1. **Target:** initiate agent-version upgrade for a selected model, not controller-model upgrade. 2. **Inputs/scope:** optional target version/stream, dry-run and agent-version check override. 3. **Operation/output:** fetch model configuration, request `UpgradeModel` with model UUID and options, then report best version and started/dry-run result; no convergence guarantee. 4. **Conditions:** if the client establishes this is the controller model it directs use of `upgrade-controller`; up-to-date/not-found handling can print no-upgrade message (`cmd/juju/commands/upgrademodel.go:102-123,184-203,227-264,267-289`). **Subject:** model upgrade and agent-version.

## `users`

1. **Target:** inspect controller users or users of one specified model. 2. **Inputs/scope:** optional model name; controller-only disabled-user inclusion and output format. 3. **Operation/output:** no model queries `UserInfo`; specified model resolves UUID and queries `ModelUserInfo`; print formatted users or no-users notice. 4. **Conditions:** model not found or API error propagates (`cmd/juju/user/list.go:100-117,120-181`). **Subject:** user and model access.

## `version`

1. **Target:** inspect the local CLI client build version, not an agent or controller's actual running version. 2. **Inputs/scope:** optional all-details output and output format. 3. **Operation/output:** construct version from current build and host OS/architecture; print version, or build metadata with `--all`; no controller request in `Run` (`cmd/juju/commands/version.go:61-110`). **Subject:** CLI client version and agent-version.

## `whoami`

1. **Target:** inspect locally selected controller, model and stored account identity. 2. **Inputs/scope:** current client store and output format. 3. **Operation/output:** read current controller/model/account from store, qualify the model when present, and print fields. 4. **Conditions:** no current controller or no stored account produces a notice; other store errors return. This is not a fresh controller authorization check (`cmd/juju/user/whoami.go:54-61,69-123`). **Subject:** client selection and user identity.
