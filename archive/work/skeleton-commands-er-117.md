# CLI invocation interfaces: source-traced page structures

Scope: the generated command pages named at `work/skeleton-nested-117.md:185-192`, except the copied index. Each entry is a proposed outline for one invocation interface, not a complete options/errors inventory. Source paths are relative to `/tmp/juju-41-tree` at `e5db99d585`; citations name implementation paths and line ranges, not generated help. Subject links point to proposed semantic addresses, not claims that the current documentation already has those anchors. A request, an accepted asynchronous process, a later observation and a completed external effect are different things. Local client-store operations are not controller mutations. No live deployment or provider behavior is inferred. Alphabetical order is navigation only, not conceptual ownership.

## `enable-user`

1. **Target and inputs:** Re-enable one named controller user; reject missing or extra positional arguments.
2. **Operation and observation:** Call the controller user-manager API `EnableUser`, process blocked-change errors, and report the enabled user on success. This is a controller mutation, not a local login.
3. **Subject:** [user](skeleton-control-117.md#user). Evidence: `cmd/juju/user/disenable.go:83-107,143-158`.

## `exec`

1. **Target and inputs:** Request a shell command on selected model machines, units or applications, or all machines; the target must be specified and `--all` cannot be combined with explicit targets.
2. **Operation and observation:** Send `RunOnAllMachines` or a targeted `Run` request to the action API, with wait and execution grouping controls. Enqueued operations/tasks are rendered; foreground mode waits for results, while background mode does not. Submission alone is not successful execution.
3. **Conditions and subjects:** Explicit machine targets are rejected for CAAS models; API change-block errors propagate. [script/operation](skeleton-mechanisms-117.md#script) and [unit](skeleton-workload-117.md#unit). Evidence: `cmd/juju/action/exec.go:173-205,235-273`; `cmd/juju/action/common.go:92-112,123-185`; `apiserver/facades/client/action/operation.go:241-261,296-310`.

## `export-bundle`

1. **Target and inputs:** Read a bundle representation of the selected model; no positional arguments; optionally include charm defaults and choose a local output filename.
2. **Operation and observation:** Call the bundle API `ExportBundle`; only if it succeeds, write returned content to stdout or create/truncate the specified local file and report its name. The traced server method returns not implemented (`apiserver/facades/client/bundle/bundle.go:197-200`), so this server path does not reach that output branch. The bundle is deployment input, not the model itself or a deployment request.
3. **Subject:** [bundle](skeleton-mechanisms-117.md#bundle). Evidence: `cmd/juju/model/exportbundle.go:64-83,92-132`.

## `expose`

1. **Target and inputs:** Set exposure for one application in the selected model, optionally specifying endpoint, space and CIDR lists.
2. **Operation and observation:** Build a map of exposed endpoints and issue `Expose` to the application API. No granular inputs produce a nil map; when spaces/CIDRs are supplied without endpoints the empty endpoint represents all endpoints. Blocked-change errors are processed. A successful request does not establish actual network reachability.
3. **Subjects:** [application](skeleton-workload-117.md#application) and [space](skeleton-infrastructure-117.md#space). Evidence: `cmd/juju/application/expose.go:140-200`.

## `find`

1. **Target and inputs:** Search Charm Hub for charms/bundles using an optional query and type, channel, category or publisher filters; format/column options control presentation.
2. **Operation and observation:** Construct the Charm Hub client and call `Find`, then format returned results. A not-found API error is contextualized; an empty tabular result prints a message. This is a catalog read, not a model mutation.
3. **Subjects:** [charm](skeleton-workload-117.md#charm) and [bundle](skeleton-mechanisms-117.md#bundle). Evidence: `cmd/juju/charmhub/find.go:72-97,104-130,135-177`.

## `find-offers`

1. **Target and inputs:** Discover application offers on a selected source controller using optional offer URL/name and interface filters. Default source is the current controller; an omitted URL qualifier is filled from the current account.
2. **Operation and observation:** Send `FindApplicationOffers` with model/offer/endpoint filters, convert the results and print them. No matches return an error. This reads offer metadata; it does not consume an offer or create a relation.
3. **Subject:** [offer](skeleton-workload-117.md#offer). Evidence: `cmd/juju/crossmodel/find.go:60-75,91-101,104-176`.

## `firewall-rules`

1. **Target and inputs:** Display selected-model known-service ingress rule configuration; no positional arguments; this is an IAAS-only command and emits a deprecation warning.
2. **Operation and observation:** Read model configuration via `ModelGet`, construct SSH and application-offer ingress rule views from the configured CIDRs and format them. It does not inspect or verify actual network enforcement.
3. **Subjects:** [model](skeleton-control-117.md#model), [offer](skeleton-workload-117.md#offer). Evidence: `cmd/juju/firewall/listrules.go:37-65,73-118`.

## `grant`

1. **Target and inputs:** Grant a user an access level on a controller, named models or offer URLs. Input shape determines scope; model names and offer URLs cannot be mixed and access levels are checked against the specified scope.
2. **Operation and observation:** Controller scope calls `GrantController`; model scope resolves model UUIDs then calls `GrantModel`; offer scope fills missing qualifiers and calls `GrantOffer`. These are separate API mutations, with blocked-change errors handled; the CLI does not itself prove every downstream authorization consequence.
3. **Subjects:** [user/access](skeleton-control-117.md#user), [model](skeleton-control-117.md#model), [offer](skeleton-workload-117.md#offer). Evidence: `cmd/juju/model/grantrevoke.go:120-174,245-295`.

## `grant-cloud`

1. **Target and inputs:** Grant one user's access level on one or more clouds known to a controller; require cloud names and validate the cloud-specific access value.
2. **Operation and observation:** Use the controller cloud API `GrantCloud` and process blocked-change errors. This changes a user/cloud access relation, not the cloud credential used by a model.
3. **Subjects:** [user](skeleton-control-117.md#user), [cloud](skeleton-control-117.md#cloud). Evidence: `cmd/juju/model/grantrevokecloud.go:57-94,123-148`.

## `grant-secret`

1. **Target and inputs:** Grant access to one selected-model secret, named by URI or label, to a comma-separated list of applications.
2. **Operation and observation:** Send `GrantSecret` to the secrets API and aggregate any returned per-application errors. An access grant is not a secret revision or creation of an application relation.
3. **Subjects:** [secret](skeleton-workload-117.md#secret), [application](skeleton-workload-117.md#application). Evidence: `cmd/juju/secrets/grantrevoke.go:36-48,61-113`; `api/client/secrets/client.go:249-269`.

## `help`

1. **Target and inputs:** Local CLI command/topic help, optionally choosing a topic or nested subcommand.
2. **Operation and observation:** Resolve a registered command or topic and render command/global flags or topic text; a missing-command callback may be consulted, otherwise an unknown target errors. This is local dispatcher output, not an API or command execution.
3. **Subject:** [CLI](skeleton-tools-117.md). Evidence: `cmd/supercommand.go:249-250`; `cmd/cmd/help.go:138-181,184-227,230-290`.

## `help-action-commands`

1. **Target and inputs:** Local help about action-context commands; accept zero or one command name.
2. **Operation and observation:** Without a name, enumerate action command names and print their purposes; with one, construct that command for help using a dummy context, then render its flags and help. It does not run the action command or require a live action.
3. **Subject:** [hook/action command interface](skeleton-mechanisms-117.md#hook-command). Evidence: `cmd/juju/commands/help_action_commands.go:17-58,75-98`.

## `help-hook-commands`

1. **Target and inputs:** Local help about hook-context commands; accept zero or one command name.
2. **Operation and observation:** Without a name, enumerate hook command names and print their purposes; with one, construct it for help using a dummy context and render flags/help. This is not execution inside a live hook.
3. **Subject:** [hook command interface](skeleton-mechanisms-117.md#hook-command). Evidence: `cmd/juju/commands/help_hook_commands.go:90-131,148-171`.

## `import-filesystem`

1. **Target and inputs:** Import an existing provider-identified filesystem into the selected model as a named storage instance; accept storage pool, provider ID, storage name and optional force. Initialization requires three inputs and validates pool/name syntax.
2. **Operation and observation:** `ImportStorage` is a model API request with filesystem kind and the supplied values; the command reports the import attempt and returned storage ID. The returned ID is the observed result, not a separate proof of attachment or workload readiness.
3. **Subject:** [storage instance and pool](skeleton-infrastructure-117.md#storage). Evidence: `cmd/juju/storage/import.go:101-144,158-179,198-202`.

## `import-ssh-key`

1. **Target and inputs:** Import one or more authorized SSH key IDs into the selected model; the CLI accepts only `lp:` and `gh:` prefixes.
2. **Operation and observation:** Send `ImportKeys` through the key manager API using the command's `admin` user value. A top-level blocked change is returned; individual result errors are printed to stderr while the command continues to report the other results. Do not confuse an accepted key-import request with a successful SSH connection.
3. **Subject:** [SSH key](skeleton-infrastructure-117.md#ssh-key). Evidence: `cmd/juju/sshkeys/import_sshkeys.go:48-51,75-115`.

## `info`

1. **Target and inputs:** Inspect a Charm Hub charm or bundle by one name, with optional revision, channel, architecture, base, track, config and output controls; the implementation rejects incompatible revision/track combinations and non-Charm-Hub names.
2. **Operation and observation:** Construct a Charm Hub client, request `Info`, convert/filter the returned view and print it; formats include tabular, YAML and JSON. A not-found response gets a contextual error. This is an information read, not a deployment or a model configuration request.
3. **Subject:** [charm](skeleton-workload-117.md#charm) and [bundle](skeleton-mechanisms-117.md#bundle). Evidence: `cmd/juju/charmhub/info.go:69-102,107-151,156-209`.

## `integrate`

1. **Target and inputs:** Create a relation between exactly two application endpoints in the selected model; endpoints can include a remote offer and cross-model egress CIDRs can be supplied.
2. **Operation and observation:** For a remote offer, obtain consume details from its source and call `Consume` on the target first; then request `AddRelation`. Unauthorized, already-existing, blocked and selected remote-offer failure cases are handled. The API request result is not evidence that related units have completed their subsequent work.
3. **Subjects:** [relation](skeleton-workload-117.md#relation) and [offer](skeleton-workload-117.md#offer). Evidence: `cmd/juju/application/integrate.go:164-197,206-227,234-283,286-328`.

## `kill-controller`

1. **Target and inputs:** Destroy the selected/named controller and its managed resources; timeout and the inherited destruction/confirmation controls govern the attempt.
2. **Operation and observation:** Attempt a controller API connection, obtain controller environment details, and where connected request destruction of models and storage. The command waits for model removal and can attempt direct cleanup of remaining resources; if the controller API is unavailable or the destruction request fails, the code takes a direct environment-destruction path. It prints progress and failures. This is a multi-stage destructive process, not just a local unregister or proof that every external resource has disappeared.
3. **Conditions and subjects:** Permission failure aborts; controller-model-config API and environment acquisition must also succeed before the fallback. Confirmation applies when required. See [controller](skeleton-control-117.md#controller) and [model](skeleton-control-117.md#model). Evidence: `cmd/juju/controller/kill.go:70-93,98-170`.

## `login`

1. **Target and inputs:** Authenticate to a known controller, or to a supplied controller domain under a controller name; optional local user and prompt/trust controls affect the path.
2. **Operation and observation:** The client selects current/named controller, performs existing-controller or public-controller login, then updates its local account and current-controller records. A newly discovered controller is stored; when the account changes, it lists available models, stores their details, prints a welcome and may select a current model. Reusing the same user returns before that listing.
3. **Conditions and subjects:** A requested local username is rejected for a controller recorded as OIDC-enabled; a domain resolving to a different controller UUID is rejected. [user](skeleton-control-117.md#user) and [controller](skeleton-control-117.md#controller). Evidence: `cmd/juju/user/login.go:118-153,170-181,193-215,227-301`.

## `logout`

1. **Target and inputs:** Log out the locally stored account for the selected controller; no positional arguments, optional force.
2. **Operation and observation:** This is local client-store work: clear the controller's stored macaroons and remove account credentials, then report how many other controllers still have account details. A missing local account is already a no-op. The command does not request deletion of a controller user.
3. **Condition and subject:** A stored password blocks logout unless force is supplied. [user](skeleton-control-117.md#user) and [controller](skeleton-control-117.md#controller). Evidence: `cmd/juju/user/logout.go:61-109,112-148`.

## `machines`

1. **Target and inputs:** List machines in the selected model; no positional arguments, with output/time/color controls.
2. **Operation and observation:** The inherited execution asks the status API for full status and formats its machine view. If the API returns both status and an error, the error is printed and the available status is still formatted; no status on an error fails. This is a status read, not machine provisioning.
3. **Subjects:** [machine](skeleton-infrastructure-117.md#machine), [status](skeleton-mechanisms-117.md#status). Evidence: `cmd/juju/machine/list.go:27-35,39-60`; `cmd/juju/machine/base.go:43-52,55-88`.

## `migrate`

1. **Target and inputs:** Initiate transfer of a named model to a named target controller; optional dry-run requests prechecks without starting migration. Source model scope and target controller are distinct.
2. **Operation and observation:** Read the target controller/account details from the client store, resolve the model UUID, check feasibility, then send `InitiateMigration` to the source controller. Empty returned ID reports a successful dry-run; a nonempty ID is reported as migration started, not completed.
3. **Conditions and subject:** The feasibility check compares model users against target users and, when external users are present, controller identity-provider configuration. [model migration](skeleton-control-117.md#model-migration). Evidence: `cmd/juju/commands/migrate.go:105-169,172-202,266-339`.

## `model-config`

1. **Target and inputs:** Read or modify configuration of the selected model; actions derive from key, key=value, file and reset inputs and may be executed in sequence.
2. **Operation and observation:** Open the model-config API; get one/all values, read a local file for a set, send `ModelSet`, or send `ModelUnset` for reset. Reads produce formatted values; a successful mutation call is not a promise that every dependent component has converged.
3. **Conditions and subject:** Validate known keys and block changes via the common blocked-change path. Some read-only keys require other commands; on newer API versions secret backend uses its dedicated command. [model](skeleton-control-117.md#model). Evidence: `cmd/juju/model/config.go:231-276,281-324,327-377,380-400`.

## `model-constraints`

1. **Target and inputs:** Read machine constraints at selected-model scope, with no positional inputs and selectable constraints/YAML/JSON output.
2. **Operation and observation:** Call `GetModelConstraints` through the model-config API and format the returned value. This is a read; it neither changes application constraints nor demonstrates available capacity.
3. **Subject:** [constraint](skeleton-infrastructure-117.md#constraint). Evidence: `cmd/juju/model/constraints.go:77-105,108-133`.

## `model-defaults`

1. **Target and inputs:** Read, set or reset controller-managed default model configuration for a cloud and optionally a region; accept key, key=value, file or reset actions. Cloud and region are distinct from a specific model's current config.
2. **Operation and observation:** Validate the selected cloud/region through the cloud API; if no cloud is supplied, infer it only when exactly one is returned. Read defaults or send set/unset requests through the defaults API. Reads are formatted; setters use blocked-change handling.
3. **Conditions and subject:** Conflicting cloud syntax, unknown region, no accessible clouds and ambiguous cloud selection fail. [model defaults](skeleton-control-117.md#model-defaults). Evidence: `cmd/juju/model/defaults.go:284-315,317-387,390-424,437-457,483-499,529-569`.

## `model-secret-backend`

1. **Target and inputs:** Inspect or set the backend selected for the current model: no argument reads, one nonempty backend name sets.
2. **Operation and observation:** Call `GetModelSecretBackend` and print its name, or call `SetModelSecretBackend`; this selection is distinct from adding a backend configuration or creating a secret.
3. **Conditions and subject:** Unsupported API returns guidance to use model config; backend-not-found and invalid-name responses have specific guidance. [secret backend](skeleton-workload-117.md#secret-backend). Evidence: `cmd/juju/secretbackends/modelsecretbackend.go:36-47,65-95,98-129`.

## `models`

1. **Target and inputs:** List model summaries on the selected controller for the current or specified user, or all models; output and UUID/time controls apply.
2. **Operation and observation:** `ListModelSummaries` is an API read, after which successful summaries are formatted and the client updates its locally cached model records. Per-model errors are reported without discarding the other summaries; a tabular empty list gets guidance.
3. **Condition and subject:** The server checks access and requires administrator access for `--all`. [model](skeleton-control-117.md#model). Evidence: `cmd/juju/controller/listmodels.go:82-137,159-196`; `apiserver/facades/client/modelmanager/modelmanager.go:580-600`.

## `move-to-space`

1. **Target and inputs:** Move one or more named subnets, specified as CIDRs, to an existing model space; optional force. This is an IAAS-only interface.
2. **Operation and observation:** Resolve the CIDRs to subnet tags, call `MoveSubnets` with the destination and force setting, and render moved subnet/from/to results. A CIDR that does not resolve fails before the move. A returned change is not proof of downstream network reachability.
3. **Subjects:** [subnet](skeleton-infrastructure-117.md#subnet), [space](skeleton-infrastructure-117.md#space). Evidence: `cmd/juju/space/move.go:26-34,75-120,121-160`; `apiserver/facades/client/spaces/move.go:20-70`.

## `offer`

1. **Target and inputs:** Publish selected endpoints of an application in a selected/named model, with optional offer name; the application name supplies the default offer name.
2. **Operation and observation:** Resolve model, endpoints and logged-in user, then issue the `Offer` API call. The returned success is logged with the offer URL. Creating an offer does not itself consume it or establish a cross-model relation.
3. **Condition and subject:** The server checks model administration in the traced create path. [offer](skeleton-workload-117.md#offer). Evidence: `cmd/juju/crossmodel/offer.go:95-200`; `apiserver/facades/client/applicationoffers/applicationoffers.go:113-175`.

## `offers`

1. **Target and inputs:** List offers in a model, optionally filtering offer/application, interface, connected user or allowed consumer and active connections.
2. **Operation and observation:** Resolve model qualification, call `ListOffers` with the requested filter, then format returned offer details. This is a read, unlike `offer` creation or `find-offers` discovery across sources.
3. **Subject:** [offer](skeleton-workload-117.md#offer). Evidence: `cmd/juju/crossmodel/list.go:96-135,138-206`; `api/client/applicationoffers/client.go:69-106`.

## `operations`

1. **Target and inputs:** Query model operations using optional application, unit, machine, action or status filters and paging.
2. **Operation and observation:** Call `ListOperations`, then render returned operation data or report no matches; paging information is displayed when applicable. This is an observation of queued or finished work, not a request to run or cancel it.
3. **Condition and subject:** The traced server handler checks read access. [script/operation](skeleton-mechanisms-117.md#script), [action](skeleton-workload-117.md#action). Evidence: `cmd/juju/action/listoperations.go:74-92,110-212`; `apiserver/facades/client/action/operation.go:181-208`.

## `refresh`

1. **Target and inputs:** Refresh one application's charm with optional local path, switch, revision/channel, resource, configuration and binding inputs. Mutually incompatible switch/path/revision combinations are rejected.
2. **Operation and observation:** Read the existing charm origin and application, invoke the refresher, handle resources and merge endpoint bindings, then request `SetCharm` with the resulting charm/config/resource/storage/binding settings. An already-current charm may return early or continue for channel/resource changes; logs describe selected progress, not convergence of every unit.
3. **Conditions and subjects:** A local charm needs a path or switch when refreshing; blocked-change and terms errors are handled. Refresher internals and later unit convergence are beyond this trace. [application](skeleton-workload-117.md#application), [charm](skeleton-workload-117.md#charm). Evidence: `cmd/juju/application/refresh.go:384-405,410-447,483-495,518-541,554-578,588-622`.

## `regions`

1. **Target and inputs:** List regions of one cloud from the client, a controller or both, according to the optional source selection and prompt.
2. **Operation and observation:** The local branch reads local cloud metadata; the controller branch calls the cloud API. Results are separately labeled/formatted, with messages for missing regions and lookup errors. This is a metadata read, not a provider region-availability probe.
3. **Subject:** [cloud](skeleton-control-117.md#cloud). Evidence: `cmd/juju/cloud/regions.go:107-117,120-186`.

## `register`

1. **Target and inputs:** Register a controller from registration data or a public controller host; a controller alias and optional replacement govern the local association.
2. **Operation and observation:** Check known endpoints, obtain controller and account details via the public or registration-data path, and add/replace local client records. Then log in, list and cache accessible models, select the controller and potentially a model, and print a welcome. This is a remote authentication exchange plus local state changes, not creation of a controller.
3. **Conditions and subject:** Non-public registration prompts for a new password; failures can occur after local record updates. The remote registration handler's full behavior is outside this trace. [controller](skeleton-control-117.md#controller), [user](skeleton-control-117.md#user). Evidence: `cmd/juju/controller/register.go:143-151,160-230,241-247,544-580`.

## `reload-spaces`

1. **Target and inputs:** Request a reload of spaces and subnets for the selected model, with no positional arguments.
2. **Operation and observation:** Call the space API `ReloadSpaces`; a not-supported result is reported specially, other errors use blocked-change handling. The server's traced handler calls the network service; this request is not proof that every external network observation is refreshed.
3. **Condition and subjects:** The server checks model-admin access and change permission. [space](skeleton-infrastructure-117.md#space), [subnet](skeleton-infrastructure-117.md#subnet). Evidence: `cmd/juju/space/reload.go:36-63`; `apiserver/facades/client/spaces/spaces.go:253-263`.

## `remove-application`

1. **Target and inputs:** Remove one or more applications from the selected model, with force, storage-destruction, dry-run and confirmation controls.
2. **Operation and observation:** Preview with `DestroyApplications(DryRun)` when requested or when confirmation is needed, then submit the actual destruction request and report per-application results. A preview is not a mutation; accepted removal is not proof that units, relations and external storage have finished cleanup.
3. **Conditions and subjects:** `--no-wait` requires force; dry-run needs a supported API version, though the confirmation path can warn and proceed without preview on an older API. [application](skeleton-workload-117.md#application), [removal](skeleton-mechanisms-117.md#removing-things). Evidence: `cmd/juju/application/removeapplication.go:104-127,161-236`.

## `remove-cloud`

1. **Target and inputs:** Remove a named cloud's local client definition, controller definition, or both, depending on source selection and prompt.
2. **Operation and observation:** Delete a local personal cloud from personal metadata and/or call the controller's `RemoveCloud` API. Local built-in/public clouds are not removed; missing controller cloud is reported separately. Partial success is possible because the branches are independent.
3. **Subject:** [cloud](skeleton-control-117.md#cloud). Evidence: `cmd/juju/cloud/remove.go:100-136,139-190`.

## `remove-credential`

1. **Target and inputs:** Remove a named cloud credential on the client, the selected controller, or both; optional force applies to the controller request.
2. **Operation and observation:** Check cloud availability, then delete the named entry in the local credential store and/or request controller `RevokeCredential` under the current account. The two paths may have different outcomes; the command reports them individually.
3. **Conditions and subjects:** A missing cloud at both locations is an error; force is passed to the controller-side revocation. [credential](skeleton-control-117.md#credential), [cloud](skeleton-control-117.md#cloud). Evidence: `cmd/juju/cloud/removecredential.go:121-170,213-255`.

## `remove-k8s`

1. **Target and inputs:** Remove a Kubernetes cloud by name from the local client, a controller or both after source selection.
2. **Operation and observation:** When both sides are selected, attempt credential-associated RBAC cleanup first; then the client branch removes local personal cloud metadata and clears its credential entry, and the controller branch calls `RemoveCloud`. These steps are ordered and can fail separately; individual RBAC cleanup errors are logged as warnings.
3. **Subjects:** [cloud](skeleton-control-117.md#cloud), [credential](skeleton-control-117.md#credential). Evidence: `cmd/juju/caas/remove.go:94-145,147-176,179-192`.

## `remove-machine`

1. **Target and inputs:** Remove specified model machines, with force, optional instance retention, dry-run and confirmation controls.
2. **Operation and observation:** Preview with `DestroyMachinesWithParams` in dry-run mode when requested or needed for confirmation; the real request carries force, keep-instance and maximum wait. Report per-machine effects/errors. Initiated removal and its preview do not prove that resource cleanup has finished.
3. **Condition and subjects:** `--no-wait` requires force; the preview can flag dependent units or containers as requiring force. [machine](skeleton-infrastructure-117.md#machine), [removal](skeleton-mechanisms-117.md#removing-things). Evidence: `cmd/juju/machine/remove.go:90-113,152-223`.

## `remove-offer`

1. **Target and inputs:** Remove one or more application offers by URL or by current-model offer name; all resolved URLs must use the same source controller and must not name individual endpoints.
2. **Operation and observation:** Resolve names, prompt before force unless confirmation is bypassed, and call `DestroyOffers` on the source controller. The force warning explicitly includes relations to the offers; a request result is not proof of completed cross-model cleanup.
3. **Subjects:** [offer](skeleton-workload-117.md#offer), [relation](skeleton-workload-117.md#relation). Evidence: `cmd/juju/crossmodel/remove.go:84-89,107-166`.

## `remove-relation`

1. **Target and inputs:** Remove one relation in the selected model by nonnegative relation ID or two application endpoints; force and wait controls apply.
2. **Operation and observation:** Call either `DestroyRelationId` or endpoint-based `DestroyRelation` and process blocked-removal errors. No-wait without force is rejected; success of this request does not mean all participant-side work is complete.
3. **Subject:** [relation](skeleton-workload-117.md#relation). Evidence: `cmd/juju/application/removerelation.go:98-109,112-158`.

## `remove-saas`

1. **Target and inputs:** Remove one or more consumed remote-application records from the selected model; names are validated and force/wait controls apply.
2. **Operation and observation:** Send `DestroyConsumedApplication` with the named SAAS applications; report per-name failures. This is consumer-side removal, distinct from removing the source offer. No-wait requires force; accepted requests do not establish completed remote cleanup.
3. **Subjects:** [offer](skeleton-workload-117.md#offer), [relation](skeleton-workload-117.md#relation). Evidence: `cmd/juju/application/removesaas.go:77-87,90-149`.

## `remove-secret`

1. **Target and inputs:** Remove a model secret specified by URI or label, optionally specifying one positive revision.
2. **Operation and observation:** Call the secrets API `RemoveSecret` with a revision pointer only when the revision is positive; otherwise no revision is specified. This targets secret/revision state, not deletion of the backend itself.
3. **Subject:** [secret](skeleton-workload-117.md#secret). Evidence: `cmd/juju/secrets/remove.go:61-100`; `api/client/secrets/client.go:221-245`.

## `remove-secret-backend`

1. **Target and inputs:** Remove one named controller secret backend, with an optional force setting for a backend storing in-use content.
2. **Operation and observation:** Call `RemoveSecretBackend(name, force)`; the command renders a particular not-supported response as backend-still-contains-content and returns a silent error. Backend configuration is distinct from the model's selection and each secret's identity.
3. **Subject:** [secret backend](skeleton-workload-117.md#secret-backend). Evidence: `cmd/juju/secretbackends/remove.go:63-106`.

## `remove-space`

1. **Target and inputs:** Remove one named model network space, with optional force and confirmation; this is an IAAS-only interface.
2. **Operation and observation:** When force requires confirmation, request a non-forced dry-run and display references first; then call `RemoveSpace` with the requested force value. Returned constraints, bindings and controller-setting references can be presented as errors. Success prints the removed name.
3. **Conditions and subjects:** The traced server path checks whether spaces are mutable; do not infer external network changes from CLI success. [space](skeleton-infrastructure-117.md#space), [subnet](skeleton-infrastructure-117.md#subnet). Evidence: `cmd/juju/space/remove.go:85-108,112-170,173-193`; `apiserver/facades/client/spaces/remove.go:22-70`.

## `remove-ssh-key`

1. **Target and inputs:** Remove one or more public SSH key identifiers from the selected model's authorized-key interface.
2. **Operation and observation:** Call `DeleteKeys` with the command's `admin` user value; an API error is returned via blocked-change handling, while individual key errors are printed to stderr. A returned key change does not prove every existing session is terminated.
3. **Subject:** [SSH key](skeleton-infrastructure-117.md#ssh-key). Evidence: `cmd/juju/sshkeys/remove_sshkeys.go:46-70,74-93`.

## `remove-storage`

1. **Target and inputs:** Remove one or more storage IDs from the selected model, with optional force, no-destroy and wait controls.
2. **Operation and observation:** Send `Remove` with `destroyAttachments` determined by force and `destroyStorage` by the inverse of no-destroy. Print individual success/error results; a removal request is distinct from storage destruction and attachment teardown completing.
3. **Conditions and subject:** Forced detachment is rejected for CAAS models; no-wait without force is rejected. [storage](skeleton-infrastructure-117.md#storage). Evidence: `cmd/juju/storage/remove.go:89-111,115-171`; `api/client/storage/client.go:232-265`.

## `remove-storage-pool`

1. **Target and inputs:** Remove a named storage pool in the selected model, not an individual storage instance.
2. **Operation and observation:** Call `RemovePool`; a not-found result is printed and returned as a silent error. This API mutation does not by itself establish destruction of any existing storage instance.
3. **Subject:** [storage pool](skeleton-infrastructure-117.md#storage). Evidence: `cmd/juju/storage/pooldelete.go:49-86`.

## `remove-unit`

1. **Target and inputs:** Remove units, with a model-type-specific target: IAAS accepts explicit unit names; CAAS accepts one application and a positive count, not named units.
2. **Operation and observation:** IAAS can preview/confirm and calls `DestroyUnits` with force, storage and wait settings; CAAS instead calls `ScaleApplication` with a negative scale change and reports the returned scale. Either result is a request/process observation, not proof that all dependent resources have been cleaned up.
3. **Conditions and subjects:** CAAS rejects dry-run and destroy-storage in this command; no-wait requires force. [unit](skeleton-workload-117.md#unit), [scaling](skeleton-mechanisms-117.md#scaling), [removal](skeleton-mechanisms-117.md#removing-things). Evidence: `cmd/juju/application/removeunit.go:131-202,231-317,383-396`.

## `remove-user`

1. **Target and inputs:** Remove one named user from the selected controller; confirmation is requested unless explicitly bypassed.
2. **Operation and observation:** Call the user-manager `RemoveUser` API and print the removed name on success; an already-permanently-deleted response is rendered distinctly. This changes controller user state, unlike local `logout`.
3. **Subject:** [user](skeleton-control-117.md#user). Evidence: `cmd/juju/user/remove.go:97-160`.

## `rename-space`

1. **Target and inputs:** Rename a model network space, providing distinct valid old and new names; IAAS only.
2. **Operation and observation:** Call `RenameSpace` and report the old and new names on success. This is a space mutation, not a command to move a subnet to a different space.
3. **Subjects:** [space](skeleton-infrastructure-117.md#space), [subnet](skeleton-infrastructure-117.md#subnet). Evidence: `cmd/juju/space/rename.go:19-27,67-101`.

## `reprovision-machine`

1. **Target and inputs:** Request reprovisioning of exactly one named non-container machine in the selected model.
2. **Operation and observation:** Call the machine-manager `ReprovisionMachine` API and report that reprovisioning is in progress; individual result errors propagate. The message is not proof that a replacement instance is ready.
3. **Conditions and subject:** Container IDs are rejected and a not-implemented response advises upgrading the controller. [machine](skeleton-infrastructure-117.md#machine). Evidence: `cmd/juju/machine/reprovisionmachine.go:70-87,90-125`.

## `resolved`

1. **Target and inputs:** Mark specified units' errors resolved or use `--all`; optionally suppress retry. The two targeting forms are exclusive.
2. **Operation and observation:** Call `ResolveUnitErrors` with the unit list, all flag, and inverse of no-retry; blocked changes are processed. This requests resolution/retry, not proof that the failed hook subsequently succeeds.
3. **Subjects:** [unit](skeleton-workload-117.md#unit), [hook](skeleton-mechanisms-117.md#hook). Evidence: `cmd/juju/application/resolved.go:43-76,96-103`.

## `resources`

1. **Target and inputs:** List charm resources for one application or unit in the selected model; optional details control presentation.
2. **Operation and observation:** Validate/resolve the target to its application, call `ListResources`, sort returned repository/application/unit resources and render the application or selected-unit view. Empty results are reported. This is a read, not attachment or upload of a resource.
3. **Subject:** [charm resource](skeleton-workload-117.md#resource-charm). Evidence: `cmd/juju/resource/list.go:68-99,103-155,159-195`.

## `resume-relation`

1. **Target and inputs:** Resume one or more selected-model relations by nonnegative numeric IDs. The implementation parses each argument as an integer; despite its help argument label, the traced `Init` does not split comma-separated IDs.
2. **Operation and observation:** Call `SetRelationSuspended` with suspension false and process blocked-change errors. This is a relation-state request, not evidence that cross-model communication has resumed successfully.
3. **Subject:** [relation](skeleton-workload-117.md#relation). Evidence: `cmd/juju/application/resumerelation.go:54-81,84-91`.

## `retry-provisioning`

1. **Target and inputs:** Request retry of provisioning for specified non-container machine IDs or `--all`; the two forms cannot be mixed.
2. **Operation and observation:** Call machine-manager `RetryProvisioning`; print per-machine result errors and process a top-level blocked change. The request is not evidence that a machine was provisioned successfully.
3. **Subject:** [machine](skeleton-infrastructure-117.md#machine). Evidence: `cmd/juju/model/retryprovisioning.go:66-83,86-114`.

## `revoke`

1. **Target and inputs:** Revoke a user's access level on a controller, named models or offer URLs; argument shape selects the scope, and model/offer targets cannot be mixed.
2. **Operation and observation:** Controller scope calls `RevokeController`; model scope resolves UUIDs and calls `RevokeModel`; offer scope fills missing qualifiers and calls `RevokeOffer`. Blocked-change errors are handled. Scope-specific access semantics remain at the user/target subject, not one universal access rule.
3. **Subjects:** [user/access](skeleton-control-117.md#user), [model](skeleton-control-117.md#model), [offer](skeleton-workload-117.md#offer). Evidence: `cmd/juju/model/grantrevoke.go:120-174,364-399,406-441`.

## `revoke-cloud`

1. **Target and inputs:** Revoke a user's cloud-specific access level on one or more named clouds in a controller.
2. **Operation and observation:** Validate cloud names and access level, call `RevokeCloud` and process blocked-change errors. Revoking user access is separate from revoking a cloud credential.
3. **Subjects:** [user](skeleton-control-117.md#user), [cloud](skeleton-control-117.md#cloud). Evidence: `cmd/juju/model/grantrevokecloud.go:57-94,152-201`.

## `revoke-secret`

1. **Target and inputs:** Revoke applications' access to one selected-model secret specified by URI or label; applications are comma-separated.
2. **Operation and observation:** Send `RevokeSecret` to the secrets API and aggregate per-application errors. This changes access, not the identity or revision of the secret.
3. **Subjects:** [secret](skeleton-workload-117.md#secret), [application](skeleton-workload-117.md#application). Evidence: `cmd/juju/secrets/grantrevoke.go:96-113,151-183`.

## `run`

1. **Target and inputs:** Invoke a named charm action on one or more units or leader targets belonging to one application, with key/value or YAML parameters and wait/background controls.
2. **Operation and observation:** Build per-target action payloads and call `EnqueueOperation`; foreground mode waits for task results, while background returns scheduled-operation information. Enqueue acceptance is not action completion or success. This is a charm action, unlike arbitrary commands sent by `exec`.
3. **Subject:** [action](skeleton-workload-117.md#action), [script/operation](skeleton-mechanisms-117.md#script). Evidence: `cmd/juju/action/run.go:126-182,185-208,234-251`; `cmd/juju/action/common.go:92-112,143-185`.

## `scale-application`

1. **Target and inputs:** Set the desired unit count of one CAAS application; the integer scale must be nonnegative.
2. **Operation and observation:** Call `ScaleApplication` and report the scale returned by the API. This is a desired-allocation change, not proof that the requested units are ready or that storage/network dependencies have converged.
3. **Subjects:** [application](skeleton-workload-117.md#application), [scaling](skeleton-mechanisms-117.md#scaling). Evidence: `cmd/juju/application/scaleapplication.go:34-42,70-89,97-117`.

## `scp`

1. **Target and inputs:** Copy between local and model-targeted paths, selecting model and optionally direct or controller-jump routing; at least two arguments are required.
2. **Operation and observation:** Resolve model type and initialize the selected transfer provider. Non-CAAS jump and direct-machine paths resolve targets and invoke local SSH copy; CAAS jump transfers through tar over SSH, while direct CAAS resolves file resources and calls the container execution client's `Copy`. On the non-CAAS jump path `--show-command` renders instead of copying.
3. **Conditions and subjects:** `--show-command` cannot be combined with direct mode and is rejected for CAAS jump transfers; CAAS direct and jump require one source and one destination, and the jump path requires exactly one remote target. Copy return is not a separate proof of the target's future state. [SSH server](skeleton-infrastructure-117.md#ssh-server), [machine](skeleton-infrastructure-117.md#machine), [unit](skeleton-workload-117.md#unit). Evidence: `cmd/juju/ssh/scp.go:160-165,180-220`; `cmd/juju/ssh/ssh_jump.go:459-479,536-567,570-608`; `cmd/juju/ssh/ssh_machine.go:232-255`; `cmd/juju/ssh/ssh_container.go:299-336`.
