# CLI invocation page structures: actions through enable-destroy-controller — E117

These are proposed **per-invocation** page outlines, not complete option, permission, or error inventories. The alphabetical range is only a research partition, not conceptual ownership. Source paths are relative to `/tmp/juju-41-tree` at `e5db99d585`; semantic-subject links point to the separately derived outlines in this work directory. Source describes what the client requests and prints, not proof that external provisioning or subsequent convergence has completed. Each entry orders target, input/scope, operation/observation, traced conditions and links; omit an inapplicable section rather than forcing common headings. No generated help or filename alone establishes behavior. No build, tests, lint, formatter, live controller or provider execution was run.

## `actions`

1. **Target:** read charm-declared action definitions for one application in the selected model; it is not an invocation or a list of operation results. 2. **Inputs:** one validated application name; optional full schema and output format. 3. **Read/output:** `ApplicationCharmActions` fetches a map; compact output uses action descriptions (substituting “No description”), sorted in the tabular path; full schema emits parameter specs, defaulting to YAML, while compact defaults to table. An empty table produces an informational message. 4. **Condition:** schema plus tabular format is rejected. `cmd/juju/action/list.go:47-68,86-104,108-164`. Subject: [action](skeleton-workload-117.md#action).

## `add-cloud`

1. **Target:** register a cloud definition locally, on a selected controller, or both. 2. **Inputs:** optional name, definition file or interactive input, controller/client selection and optional credential/force. 3. **Effect/observation:** read a file, reuse an existing local definition, or prompt; synthesize a default region if none exists. The local path updates local cloud metadata; the controller path calls `AddCloud`, then attempts to upload a matching local credential when required. Print each outcome. 4. **Conditions:** existing local definitions return an already-exists error rather than overwrite; an already-present remote cloud or incompatible cloud is reported on its special path; a credential-upload failure after successful cloud addition is reported without undoing that addition. `cmd/juju/cloud/add.go:207-242,265-291,295-400`. Subjects: [cloud](skeleton-control-117.md#cloud), [credential](skeleton-control-117.md#credential).

## `add-credential`

1. **Target:** a named cloud's local and/or selected-controller credentials, not a model by itself. 2. **Inputs:** cloud name, optional YAML credential file and region, or interactive entry; client/controller target. 3. **Effect/observation:** find a remote or local cloud definition, validate credential data against available schema, save new local entries if requested, and upload verified entries to the controller if its cloud exists there; print local and remote outcomes. 4. **Conditions:** a cloud requiring no credentials is rejected; an existing local name is reported and other entries can still be processed, so local and remote results need not be identical. `cmd/juju/cloud/addcredential.go:153-169,171-291,294-320,596-647`. Subjects: [credential](skeleton-control-117.md#credential), [cloud](skeleton-control-117.md#cloud).

## `add-k8s`

1. **Target:** register a Kubernetes cluster as a cloud with its credential in the local client and/or a controller; this is not bootstrap. 2. **Inputs:** cluster registration name, Kubernetes context or cluster selection, optional cloud/region and storage settings, client/controller target. 3. **Effect/observation:** read supplied or local kubeconfig, select context, ensure a cluster role, service account and role binding to resolve credentials, derive cloud and credential, optionally obtain storage metadata, and then write local cloud/credential and/or call the controller cloud and credential APIs; report registration outcomes. Cluster-side work precedes registration. 4. **Conditions:** context and cluster options cannot both be supplied; storage metadata processing is skipped when requested; local or controller additions can fail independently after earlier work. `cmd/juju/caas/add.go:191-216,233-249,260-283,456-524,536-575,593-672`; `caas/kubernetes/clientconfig/k8s.go:30-38`; `caas/kubernetes/clientconfig/plugins.go:60-118`. Subjects: [cloud](skeleton-control-117.md#cloud), [credential](skeleton-control-117.md#credential).

## `add-machine`

1. **Target:** add a machine/container to the selected model or manually provision an SSH-specified machine. 2. **Inputs:** optional placement, count, base, constraints, disks and manual SSH keys. 3. **Operation/output:** load model config; SSH placement takes the manual provisioner path, while other placements form `AddMachines` requests and report returned machine/container IDs and per-result failures. The request result is not a readiness guarantee. 4. **Conditions:** explicit placement directive cannot be combined with multiple machines; a bare machine ID is rejected; unauthorized model-config retrieval emits a permissions message and blocked requests are translated. `cmd/juju/machine/add.go:190-220,271-388,396-432`. Subjects: [machine](skeleton-infrastructure-117.md#machine), [constraint](skeleton-infrastructure-117.md#constraint), [placement](skeleton-nested-117.md#placement-directivemd).

## `add-model`

1. **Target:** create a model on a selected controller. 2. **Inputs:** model name, optional cloud/region, owner, credential and configuration, plus switch choice. 3. **Operation/output:** resolve cloud and credential, optionally upload an explicitly selected local credential, then call `CreateModel`; on success record a model belonging to the current user locally and normally select it, unless `--no-switch`. Report the returned cloud/region and credential where present. 4. **Conditions:** invalid names are rejected; unauthorized creation gets a permissions message; local selection only follows successful creation and is restricted by the ownership branch. `cmd/juju/controller/addmodel.go:127-161,188-211,219-269,276-305,308-340`. Subjects: [model](skeleton-control-117.md#model), [cloud](skeleton-control-117.md#cloud), [credential](skeleton-control-117.md#credential).

## `add-secret`

1. **Target:** create a user secret in the selected model. 2. **Inputs:** secret name, optional description, key-value arguments and/or a YAML data file; file values overlay argument values and resulting data must be nonempty. 3. **Operation/output:** call `CreateSecret` and print its returned URI; this is an identity result, not a consumer grant. 4. **Conditions:** missing name/content fails before the API call; API errors are returned. `cmd/juju/secrets/common.go:15-43`; `cmd/juju/secrets/add.go:18-24,84-114`. Subject: [secret](skeleton-workload-117.md#secret).

## `add-secret-backend`

1. **Target:** create a controller secret backend, separate from creating an individual secret. 2. **Inputs:** backend name/type, optional import ID, config file and/or key-value attributes. 3. **Operation/output:** merge file and command attributes, extract rotation setting, validate via the backend's config validator when provided, and call `AddSecretBackend`; success has no command-specific printed result in `Run`. 4. **Conditions:** missing config and malformed/duplicate key-value entries are rejected; token rotation and provider config can fail validation. `cmd/juju/secretbackends/add.go:68-74,102-144,172-236`. Subject: [secret backend](skeleton-workload-117.md#secret-backend).

## `add-space`

1. **Target:** create an IAAS model network space, optionally associating existing subnets. 2. **Inputs:** space name and zero or more CIDRs. 3. **Operation/output:** sort supplied CIDRs, call `AddSpace`, and report the space and associated subnets or “no subnets”. 4. **Conditions:** unsupported and unauthorized API responses receive specific messages; blocked changes are processed as such. `cmd/juju/space/add.go:21-32,60-95`. Subjects: [space](skeleton-infrastructure-117.md#space), [subnet](skeleton-infrastructure-117.md#subnet).

## `add-ssh-key`

1. **Target:** add public SSH keys to the selected model's key manager. 2. **Inputs:** one or more key arguments. 3. **Operation/output:** send `AddKeys` with the client’s `admin` user value; print individual result errors to stderr, with no command-specific success output. 4. **Conditions:** no key is rejected; a top-level blocked error is processed; per-key errors are printed but this `Run` returns nil after examining the results. `cmd/juju/sshkeys/add_sshkeys.go:44-54,72-103`. Subject: [SSH key](skeleton-infrastructure-117.md#ssh-key).

## `add-storage`

1. **Target:** request additional storage instances for an existing unit in a model. 2. **Inputs:** unit name and one or more storage directives, including parsed pool, size and count. 3. **Operation/output:** create deterministically sorted `AddToUnit` requests, report returned storage IDs or, for a response without IDs, the storage name; aggregate per-directive failures. The response is not proof of finished attachment. 4. **Conditions:** invalid unit or missing directive fails locally; unauthorized is messaged; partial failures are reported. `cmd/juju/storage/add.go:117-131,150-205,214-233`. Subjects: [storage and attachment](skeleton-infrastructure-117.md#storage), [unit](skeleton-workload-117.md#unit).

## `add-unit`

1. **Target:** add units to an existing application in a selected model. 2. **Inputs:** application, positive count, optional placement and existing storage attachment. 3. **Operation/output:** CAAS models call `ScaleApplication` with a positive scale change; other model types call `AddUnits` with placements/count. On success this `Run` prints no per-unit result; a successful request does not establish unit readiness. 4. **Conditions:** placement is rejected for CAAS; attaching existing storage cannot be combined with multiple units; excess placements generate a warning; unauthorized and blocked responses are handled. `cmd/juju/application/addunit.go:97-130,160-194,216-270`. Subjects: [application](skeleton-workload-117.md#application), [unit](skeleton-workload-117.md#unit), [scaling](skeleton-mechanisms-117.md#scaling).

## `add-user`

1. **Target:** create a user on a selected controller. 2. **Inputs:** username and optional display name. 3. **Operation/output:** call `AddUser` without an initial password, locally construct registration information from its returned key, and print a registration command plus a notice about model access. User creation occurs before token generation, so a later local error does not imply the creation was rolled back. 4. **Conditions:** missing name/extra args fail; unauthorized and blocked errors are handled. `cmd/juju/user/add.go:82-91,95-138`. Subject: [user](skeleton-control-117.md#user).

## `attach-resource`

1. **Target:** update one charm resource of a deployed application in the selected model, not persistent storage. 2. **Inputs:** application and one `resource-name=value` pair. 3. **Operation/output:** query existing application resources to determine type, open the resource locally, and send it to the upload client; no command-specific success message is emitted. The internals and downstream completion of upload are not traced here. 4. **Conditions:** missing or invalid arguments and open/upload errors fail; blocked upload errors are processed. `cmd/juju/resource/upload.go:116-150,153-193`. Subjects: [charm resource](skeleton-workload-117.md#resource-charm), [application](skeleton-workload-117.md#application).

## `attach-storage`

1. **Target:** attach existing storage instances to one unit in an IAAS model. 2. **Inputs:** unit ID and one or more storage IDs. 3. **Operation/output:** call `Attach` and report “attaching” or failure per ID; this result does not itself prove completed attachment. 4. **Conditions:** missing arguments fail; unauthorized calls get a permissions message, blocked calls are processed, and any per-item failure returns a silent command error. `cmd/juju/storage/attach.go:24-35,58-65,79-109`; `api/client/storage/client.go:200-222`. Subjects: [storage attachment](skeleton-infrastructure-117.md#storage), [unit](skeleton-workload-117.md#unit).

## `autoload-credentials`

1. **Target:** discover local credentials and optionally write them to the local client and/or upload them to a controller. 2. **Inputs:** optional cloud type, destination selection, interactive selection of detected credential and cloud. 3. **Operation/output:** combine locally known and selected-controller clouds, invoke registered credential detectors, prompt for selections and save local entries during the loop; afterward upload verified selections whose clouds exist on the controller. Print discovery, save and upload results. 4. **Conditions:** detection errors for individual providers are logged and skipped; no detected credentials prints a message; incompatible selections are rejected. `cmd/juju/cloud/detectcredentials.go:137-146,167-205,207-260,298-323,364-458,474-516`. Subjects: [credential](skeleton-control-117.md#credential), [cloud](skeleton-control-117.md#cloud).

## `bind`

1. **Target:** change a deployed application's endpoint-to-space bindings. 2. **Inputs:** application, optional default space and endpoint-space expressions, with optional force. 3. **Operation/output:** list model spaces, parse the binding expression, read existing application bindings, validate endpoints and merge locally, then request `MergeBindings`; print the change list only after successful API return. 4. **Conditions:** a cloud that reports spaces unsupported produces a no-op message; empty bindings fail; force is passed to the server. `cmd/juju/application/bind.go:96-113,117-181,196-220`. Subjects: [application](skeleton-workload-117.md#application), [space](skeleton-infrastructure-117.md#space).

## `bootstrap`

1. **Target:** create a controller in a selected cloud/region and establish local client context; not creation of an ordinary workload model. 2. **Inputs:** cloud/region and controller name, credential, constraints, configuration and optional interactive/switch/cleanup choices. 3. **Operation/output:** resolve cloud, region and credentials, prepare the controller environment, set local selection, validate inputs and invoke the bootstrap implementation; refresh controller details and wait for agent initialisation before returning success. Report controller creation and a model-creation hint. 4. **Conditions/timing:** region validation, storage config and SSH-key checks can fail. Once the corresponding deferred cleanup is installed, a later failure attempts local cleanup and, unless keep-broken is selected, environment cleanup; earlier failures need not reach both cleanup stages. The called provider-specific provisioning internals are not traced here. `cmd/juju/commands/bootstrap.go:572-660,662-704,725-748,766-818,862-916,934-954,996-1023`. Subjects: [controller](skeleton-control-117.md#controller), [cloud](skeleton-control-117.md#cloud), [credential](skeleton-control-117.md#credential).

## `cancel-task`

1. **Target:** request cancellation of pending or running tasks in the selected model, not the entire application or operation. 2. **Inputs:** one or more task IDs or prefixes. 3. **Operation/output:** call the action API's `Cancel`, format returned successful cancellations and warn about individual failures. An accepted cancellation is not evidence of completion of subsequent task teardown. 4. **Conditions:** invalid or absent IDs and an empty result fail; individual failure results are warned rather than necessarily becoming the command's returned error. `cmd/juju/action/cancel.go:52-74,76-126`. Subjects: [script and task](skeleton-mechanisms-117.md#script), [action](skeleton-workload-117.md#action).

## `change-user-password`

1. **Target:** change a current or named controller user's password, or reset another user's registration. 2. **Inputs:** optional user, reset choice, interactive password confirmation or stdin. 3. **Operation/output:** normal branch calls `SetPassword`; when applicable it refreshes and updates local account details afterward. Reset branch calls `ResetPassword` and prints a registration command derived from the returned key. 4. **Conditions:** own reset prints a refusal and returns without resetting; unnamed external user, empty password, and prompt confirmation errors are handled. A local update can fail after the server password change. `cmd/juju/user/change_password.go:76-104,115-174,185-248`. Subject: [user](skeleton-control-117.md#user).

## `charm-resources`

1. **Target:** read the resource definitions of a Charmhub charm, rather than an already deployed application's current resources. 2. **Inputs:** one charm and optional channel/output format. 3. **Operation/output:** resolve the charm, call controller `ListCharmResources` with origin/channel and format the resource list; the tabular path reports empty results. 4. **Conditions:** unsupported non-Charmhub identifiers fail; unsupported controller API returns a targeted message; bundle handling takes a special empty-result path when resolution reports unsupported. `cmd/juju/resource/charmresources.go:129-150,152-206,227-243,251-281`. Subject: [charm resource](skeleton-workload-117.md#resource-charm).

## `clouds`

1. **Target:** list cloud definitions known to the local client and/or selected controller. 2. **Inputs:** destination selection, optional `--all` and output format. 3. **Read/output:** gather local metadata when selected; query controller `Clouds` and `CloudInfo` when selected; render combined details in table, YAML or JSON. By default the traced filter removes public clouds with no registered credentials and reports omitted results. 4. **Conditions:** local/controller errors are accumulated after best-effort output, not evidence of an empty total catalogue. `cmd/juju/cloud/list.go:125-137,139-223,278-298,308-344`. Subject: [cloud](skeleton-control-117.md#cloud).

## `config`

1. **Target:** read, set or reset a deployed application's charm/application configuration in a selected model. 2. **Inputs:** application, optional key/value arguments, reset keys, YAML file or stdin; output format for full reads. 3. **Operation/output:** dispatch configured actions to application `Get`, `SetConfig` or `UnsetApplicationConfig`; a single-key read prints its value, a full read formats settings, and mutation paths have no command-specific success output. Argument values beginning with `@` read a local file. 4. **Conditions:** invalid UTF-8, missing key and blocked updates fail; a single-key read searches charm settings before application settings. `cmd/juju/application/config.go:177-188,204-241,243-361`. Subjects: [application](skeleton-workload-117.md#application), [configuration](skeleton-nested-117.md#configurationmd).

## `constraints`

1. **Target:** read machine constraints for one application in the selected model; distinct from model constraints or changing constraints. 2. **Inputs:** one validated application name and output format. 3. **Operation/output:** call `GetConstraints` and format the returned value; it is a configured constraint, not proof of allocated capacity. 4. **Conditions:** missing, invalid or extra application arguments fail locally; API errors propagate. `cmd/juju/application/constraints.go:119-152`. Subjects: [constraint](skeleton-infrastructure-117.md#constraint), [application](skeleton-workload-117.md#application).

## `consume`

1. **Target:** add a remote application offer to the selected consumer model. 2. **Inputs:** offer URL and optional local application alias; missing model qualifier defaults to the current account. 3. **Operation/output:** look up consume details from the source controller, then call `Consume` on the target model and report the returned local name. Source and target are distinct API contexts; the result is not an integration request. 4. **Conditions:** an endpoint in the offer URL is rejected; invalid alias fails; target write errors include blocked-change handling. `cmd/juju/application/consume.go:76-119,124-187`. Subjects: [offer](skeleton-workload-117.md#offer), [application](skeleton-workload-117.md#application).

## `controller-config`

1. **Target:** read or update the selected controller's configuration, not a model or application configuration. 2. **Inputs:** optional key, key-value updates or local config file, output format and read-only-field handling. 3. **Operation/output:** read one or all attributes through `ControllerConfig`; for writes filter and coerce input then call `ConfigSet`. Full reads are formatted; updates emit no command-specific success output. 4. **Conditions:** read-only/invalid keys fail unless the ignore option is used; the traced server write checks controller superuser access. `cmd/juju/controller/config.go:126-142,163-228,230-298`; `apiserver/facades/client/controller/controller.go:788-791`. Subjects: [controller](skeleton-control-117.md#controller), [configuration](skeleton-nested-117.md#configurationmd).

## `controllers`

1. **Target:** list controllers registered in the local client, optionally refreshing their cached details. 2. **Inputs:** optional `--refresh` and output format. 3. **Operation/output:** without refresh, read local store and current-controller selection only; with refresh, contact each controller concurrently, fetch models/status and update cached model/controller details, then format the reloaded store. 4. **Conditions:** per-controller refresh errors are reported while other controllers continue; no registered controllers in tabular format yields the no-controllers error. `cmd/juju/controller/listcontrollers.go:65-83,102-150,152-210`. Subjects: [controller](skeleton-control-117.md#controller), [client](skeleton-tools-117.md#clientmd--user-facing-client-and-controller-connection).

## `create-backup`

1. **Target:** request a controller backup and download the archive to a local file; this is not a restore interface. 2. **Inputs:** optional notes and filename. 3. **Operation/output:** send `POST /backup`, receive metadata and a stream, write and hash the local archive, then print metadata and destination only after verification. The source-traced handler creates and streams the archive and cleans up the server-side temporary output when the request ends; its creator exports controller/model state and object inventory separately, so the trace does not establish an atomic cross-database snapshot. 4. **Conditions:** route requires controller-admin authorization; missing or unsupported checksum fails, incomplete downloads are removed, and a mismatched archive is retained with a `.corrupt` suffix when rename succeeds. `cmd/juju/backups/create.go:89-110,113-146,148-210`; `api/client/backups/create.go:20-61`; `apiserver/apiserver.go:1087-1093`; `apiserver/internal/handlers/backups/backups.go:95-138`; `internal/worker/backupcreation/creator.go:178-233,284-315`. Subjects: [controller backup](backup-subject-113.md#subject-ownership-decision), [database](skeleton-control-117.md#database), [object store](skeleton-control-117.md#object-store).

## `create-storage-pool`

1. **Target:** define a storage pool in the selected model, not create a unit attachment. 2. **Inputs:** pool name, provider and optional key-value attributes; CAAS supplies the Kubernetes provider type when omitted. 3. **Operation/output:** send `CreatePool` to the storage API; the server invokes `CreateStoragePool`; the client prints no command-specific success message. 4. **Conditions:** argument/attribute shape is checked locally; the server requires model write access and maps invalid attributes, missing provider and duplicate pool to errors. `cmd/juju/storage/poolcreate.go:66-115,133-141`; `api/client/storage/client.go:94-108`; `apiserver/facades/client/storage/pool.go:58-90,92-125`. Subject: [storage pool](skeleton-infrastructure-117.md#storage).

## `credentials`

1. **Target:** inspect credentials in the local client and/or selected controller. 2. **Inputs:** optional cloud name, destination selection, format and optional inclusion of secret attributes. 3. **Read/output:** obtain local cloud credential entries when requested and controller `CredentialContents` when selected, then format the resulting maps. 4. **Conditions:** tabular output disables secret-attribute display; local and remote errors may be reported while a partial map is still printed; server entries with individual errors are skipped with a warning. The cloud argument is used in local selection; do not claim the traced remote request filters by it. `cmd/juju/cloud/listcredentials.go:182-202,211-228,241-353`. Subjects: [credential](skeleton-control-117.md#credential), [cloud](skeleton-control-117.md#cloud).

## `dashboard`

1. **Target:** obtain a connection to a controller's dashboard and expose a local access interface; dashboard UI behavior is separate. 2. **Inputs:** selected controller, local port, browser/open choice and credential-display choice. 3. **Operation/output:** request `DashboardConnectionInfo`; if connection data were returned, choose a proxy or SSH tunnel, print/open the URL and remain attached until the runner exits or is stopped. 4. **Condition in this source:** the traced server handler unconditionally returns `NotImplemented`, so that server path cannot reach the client's tunnel branch; this does not prove anything about independently deployed dashboard interfaces. `cmd/juju/dashboard/dashboard.go:113-118,121-212,278-321`; `apiserver/facades/client/controller/controller.go:283-293`. Subject: [dashboard](skeleton-tools-117.md#juju-dashboardmd--external-ui-and-juju-access-integration).

## `debug-code`

1. **Target:** interactive debugging session on a unit or application's leader. 2. **Inputs:** unit/leader, optional hook/action names and `--at` debug setting. 3. **Operation/output:** initialize model APIs and reuse the debug-hooks validation and SSH session setup, passing the `--at` value into the generated unit-debug script; a PTY is forced. 4. **Conditions:** unknown hook/action names fail against charm metadata; leader must resolve; the remote script's internal debugging behavior is not traced here. `cmd/juju/ssh/debugcode.go:87-106`; `cmd/juju/ssh/debughooks.go:100-142,155-214,240-280`. Subjects: [unit](skeleton-workload-117.md#unit), [hook](skeleton-mechanisms-117.md#hook), [action](skeleton-workload-117.md#action).

## `debug-hooks`

1. **Target:** interactive unit or leader hook/action debug session, distinct from the hook-command interface itself. 2. **Inputs:** unit/leader and optional hook/action names; `*` selects the unfiltered path. 3. **Operation/output:** resolve target, check specified names using application/charm APIs, build a unit-debug client script and run it over SSH with a forced PTY; model type selects the shell entry point. 4. **Conditions:** invalid targets or unknown requested hook/action names fail before SSH; subsequent remote execution is not traced. `cmd/juju/ssh/debughooks.go:100-142,155-214,240-291`. Subjects: [hook](skeleton-mechanisms-117.md#hook), [unit](skeleton-workload-117.md#unit), [SSH server](skeleton-infrastructure-117.md#ssh-server).

## `debug-log`

1. **Target:** stream or replay model debug-log observations, not status or proof an operation completed. 2. **Inputs:** entity/module/label and severity filters; tail, replay, limit, retry and formatting choices. 3. **Operation/output:** discover controller endpoints, open available debug-log clients and run `WatchDebugLog` streams into a buffered formatter; multi-controller ordering is best effort. Without explicit tail choice, a terminal tails and a non-terminal does not. 4. **Conditions:** incompatible tail/replay/count choices fail locally; multiple-controller connection failures can be warned and skipped; retry applies to closed connections when selected. `cmd/juju/commands/debuglog.go:240-281,283-321,448-483,494-584,588-645`. Subject: [log](skeleton-mechanisms-117.md#log).

## `default-credential`

1. **Target:** read, set or unset the local client's default credential name for a cloud; it does not itself change a controller credential. 2. **Inputs:** cloud name, optional credential name, reset flag. 3. **Operation/output:** read the local credential store; no value/reset prints the existing default, otherwise write the selected or empty default and report the change. 4. **Conditions:** a selected credential must exist in the local cloud entry; local cloud lookup and store errors propagate. `cmd/juju/cloud/defaultcredential.go:77-93,104-136`. Subjects: [credential](skeleton-control-117.md#credential), [cloud](skeleton-control-117.md#cloud).

## `default-region`

1. **Target:** read, set or unset a cloud's default region in this client's credential store, not the controller's model defaults. 2. **Inputs:** cloud, optional region and reset flag. 3. **Operation/output:** read local cloud and credential metadata; without a change print the default, otherwise validate/normalize a supplied region and update the local store. 4. **Conditions:** a cloud with no regions fails; an unknown region or store error propagates. `cmd/juju/cloud/defaultregion.go:55-58,74-128`. Subjects: [cloud](skeleton-control-117.md#cloud), [credential](skeleton-control-117.md#credential).

## `deploy`

1. **Target:** request deployment of a charm application or bundle in the selected model. 2. **Inputs:** charm/bundle reference and optional application name; relevant placement, constraints, configuration, bindings, units, storage, resource, revision and overlay options. 3. **Operation/output:** parse base/constraints, read model constraints and spaces for bindings, choose a deployer, and invoke `PrepareAndDeploy`; the traced repository-charm branch sends `DeployFromRepository` and reports its warnings/errors. A dry-run value is passed through; success is not proof units have become ready. 4. **Conditions:** missing target/invalid application name and placement in non-IAAS models fail; blocked changes are processed. Local charm and bundle deployer internals are not fully traced here. `cmd/juju/application/deploy.go:640-717,720-731,765-823,851-886`; `cmd/juju/application/deployer/charm.go:369-426`. Subjects: [application](skeleton-workload-117.md#application), [charm](skeleton-workload-117.md#charm), [bundle](skeleton-mechanisms-117.md#bundle).

## `destroy-controller`

1. **Target:** initiate removal of a controller and its hosted model resources, then perform controller-environment cleanup. 2. **Inputs:** controller name, optional destroy-all-models, destroy/release-storage, force and timing controls; confirmation when required. 3. **Operation/output:** connect to controller and model-config APIs, inspect model/storage status, request `DestroyController`, poll until hosted models are removed and controller machines reclaimed, then call environment cleanup; progress is printed. This is a multi-stage operation rather than merely a local deregistration. 4. **Conditions:** storage destruction and release conflict; live hosted models and persistent storage require the corresponding choices; selected server/status mismatches are retried with a bounded storage retry. Cleanup internals are not traced here. `cmd/juju/controller/destroy.go:195-213,250-410`. Subjects: [controller](skeleton-control-117.md#controller), [removal](skeleton-mechanisms-117.md#removing-things), [storage](skeleton-infrastructure-117.md#storage).

## `destroy-model`

1. **Target:** initiate destruction of a specified non-controller model. 2. **Inputs:** model identifier, storage destruction/release choice, force, no-wait and timeout controls; confirmation when required. 3. **Operation/output:** inspect local controller/model details and remote model status, submit `DestroyModel`, poll for model disappearance, then remove the local model record. Interruption reports destruction still running; no-wait changes forced destruction step waiting, not the client's explicit status polling. 4. **Conditions:** the controller model is refused; detachable storage requires an explicit disposition; destroy/release conflict and `--no-wait` requires `--force`; blocks are translated. `cmd/juju/model/destroy.go:158-188,236-347,358-418`. Subjects: [model](skeleton-control-117.md#model), [removal](skeleton-mechanisms-117.md#removing-things), [storage](skeleton-infrastructure-117.md#storage).

## `detach-storage`

1. **Target:** remove storage-to-unit attachments in the selected model, not necessarily destroy storage instances. 2. **Inputs:** one or more storage IDs and optional force/no-wait. 3. **Operation/output:** send a detach request and print “detaching” or a failure for each result; report does not establish the detach process has finished. 4. **Conditions:** `--no-wait` requires `--force`; unauthorized gets a permissions message; any item failure returns a silent command error. `cmd/juju/storage/detach.go:74-87,105-154`; `api/client/storage/client.go:264-288`. Subjects: [storage attachment](skeleton-infrastructure-117.md#storage), [unit](skeleton-workload-117.md#unit).

## `diff-bundle`

1. **Target:** compare a desired bundle with the selected model's current representation; this is a read/plan operation, not deployment. 2. **Inputs:** bundle file or name, optional overlays, base, machine and annotation choices. 3. **Operation/output:** load and compose bundle plus overlays, warn about missing relation endpoints, fetch full model status and construct a model representation, calculate a diff and print YAML. 4. **Conditions:** loading, verification and model reads can fail; diff and composition internals are not traced here. `cmd/juju/application/diffbundle.go:157-190,194-249,366-384`. Subjects: [bundle](skeleton-mechanisms-117.md#bundle), [model](skeleton-control-117.md#model).

## `disable-command`

1. **Target:** switch on a model-scoped command-set block; this is not disabling a user or removing an installed CLI command. 2. **Inputs:** command-set name and optional message. 3. **Operation/output:** map the selected set to a block type and call `SwitchBlockOn`; no command-specific success output. 4. **Conditions:** unknown or missing sets fail locally; the traced block facade checks model write permission. `cmd/juju/block/disable.go:34-47,69-78`; `cmd/juju/block/protection.go:20-43`; `apiserver/facades/client/block/client.go:83-110`. Subject: [model command blocks](model-command-blocks-113.md#subject-ownership-decision).

## `disable-user`

1. **Target:** disable one user on the selected controller. 2. **Inputs:** one username. 3. **Operation/output:** call `DisableUser` through the user-manager API and print the user-disabled confirmation. 4. **Conditions:** missing or extra arguments fail; blocked change errors are processed. `cmd/juju/user/disenable.go:99-107,125-141`. Subject: [user](skeleton-control-117.md#user).

## `disabled-commands`

1. **Target:** list model command blocks, or with `--all` list blocked models across the selected controller. 2. **Inputs:** model/controller selection, all-model choice and table/YAML/JSON format. 3. **Read/output:** call model `List` or controller `ListBlockedModels` according to scope; format block details, with a special empty table message. 4. **Conditions:** the traced model-list facade checks model read access; the all-model path is a distinct controller API rather than a model query. `cmd/juju/block/list.go:72-87,92-136`; `apiserver/facades/client/block/client.go:45-70`. Subject: [model command blocks](model-command-blocks-113.md#subject-ownership-decision).

## `documentation`

1. **Target:** generate local Markdown from the command tree, not query a controller or establish runtime semantics. 2. **Inputs:** optional output directory, split/index choices, base URL and mapping file. 3. **Operation/output:** emit a single document to stdout or a file, or recursively write per-command files in split mode. 4. **Conditions:** split requires an output directory; file access and formatting failures propagate. `cmd/cmd/documentation.go:72-99,102-122,193-245`. Subject: [CLI command interface](skeleton-nested-117.md#cli-command-family--per-invocation-tool-surfaces).

## `download`

1. **Target:** fetch a Charmhub charm or bundle artifact to a local file or stdout; unlike deploy it does not request a model deployment. 2. **Inputs:** entity name; optional channel/base/architecture or revision, filepath, resources and progress choice; a trailing hyphen selects stdout. 3. **Operation/output:** resolve release metadata, download the archive, verify its checksum for file output and optionally download/verify resources, then print a deploy hint. Stdout takes an earlier return path. 4. **Conditions:** revision cannot be combined with architecture/base/channel; stdout and resources cannot be combined; failed downloads/checksums return errors. `cmd/juju/charmhub/download.go:94-154,159-206,211-267,269-331`. Subjects: [charm](skeleton-workload-117.md#charm), [bundle](skeleton-mechanisms-117.md#bundle), [charm resource](skeleton-workload-117.md#resource-charm).

## `enable-command`

1. **Target:** switch off one previously configured model command-set block, rather than enable a user. 2. **Inputs:** one command-set name. 3. **Operation/output:** map the set to its block type and call `SwitchBlockOff`; no command-specific success output. 4. **Conditions:** missing/unknown sets or extra arguments fail locally; the traced block facade checks model write permission. `cmd/juju/block/enable.go:33-45,68-77`; `cmd/juju/block/protection.go:20-43`; `apiserver/facades/client/block/client.go:83-110`. Subject: [model command blocks](model-command-blocks-113.md#subject-ownership-decision).

## `enable-destroy-controller`

1. **Target:** remove command blocks across all models of a controller, which is broader than enabling a single model's destroy command. 2. **Inputs:** selected controller; no command-specific positional target. 3. **Operation/output:** call controller `RemoveBlocks` with `All: true`; the server iterates model IDs and removes all blocks, with no command-specific success output. It does not itself destroy the controller. 4. **Conditions:** the server requires controller superuser access; an error can stop iteration after earlier models were processed. `cmd/juju/controller/enabledestroy.go:40-68`; `api/controller/controller/controller.go:186-190`; `apiserver/facades/client/controller/controller.go:517-544`. Subjects: [controller](skeleton-control-117.md#controller), [model command blocks](model-command-blocks-113.md#subject-ownership-decision).
