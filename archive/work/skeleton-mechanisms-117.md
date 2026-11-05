# Proposed cross-cutting reference skeletons — session 117

**Proposal, not authorized page edits.** This covers ten direct pages outside the 35 selected PR pages, plus the reference index; the selected counter is unchanged. Source paths are relative to `/tmp/juju-41-tree` at `e5db99d585`. Each ordered outline is a proposed reader-facing contract, not a complete API inventory or a claim that every listed detail is already verified. Mechanisms follow their own dependencies rather than an artificial entity schema; source-traced examples are bounded. `Verify` means evidence still needed, not a fact to publish. Links and possible section titles do not authorize changes to existing anchors, pages or rules. No live controller/provider/charm was exercised.

## index

**Boundary.** The reference landing page is navigation over independently derived subjects, tools and generated lists, not a system subject or evidence for ownership. The current index contains a grouped landing page and a hidden alphabetical glob (`work/subject-map-112.md:63-77`); landing-page policy was set by a stakeholder and is outside the current edit authorization.

1. **Reference scope and entry points** — short orientation to subjects, mechanisms, tools and generated interfaces, linking their actual stable addresses without restating their contracts.
2. **Navigation and discovery** — preserve the current stakeholder-set organization while evaluating missing or broken links; the glob is a lookup convention, not a completeness proof.
3. **Generated and nested references** — link command, hook-command, configuration and cloud families at their own entry points; do not claim a generated list proves backend reachability.

**Open.** No landing-page restructure is proposed without stakeholder direction; no source evidence dictates one grouping or proves findability.

## agent

**Boundary.** An agent is an authenticated Juju process/actor associated with an identity; it is not the user, the machine, the application or a unit. The common authenticator switches on unit, machine, controller-agent, application and model tags; successful authentication does not authorize all later requests (`apiserver/authentication/agent.go:83-105`; `apiserver/apiserver.go:1773-1785`; `work/authentication-challenge-116.md`).

1. **Agent identities and roles** — distinguish agent kinds and target relationship; link model, machine, application and unit. Qualify model/platform-specific availability rather than claim all kinds exist in every deployment.
2. **Agent state and identity** — inspector-relevant agent identity, credentials and version relationships only as needed; do not publish private values. Link `agent-version` for version semantics.
3. **Agent watches and execution** — describe sourced watcher/actor paths, such as the unit agent's hook runner; link `watcher`, `hook`, task execution and per-subject streams, not a complete worker census.
4. **Agent interactions and authorization** — shared identity authentication, then per-kind/target-specific access with links to the corresponding actor/subject contracts. Separate login from permission for a specific operation.
5. **Agent configuration, observation and failures** — links to configuration, status, logs, tracing and binary tools; verify supported controls and each troubleshooting claim before including it. No universal restart/failover guarantee.

## bundle

**Boundary.** A bundle is deployment input rather than the applications and relations created from it. The Bundle facade reads and merges YAML, verifies constraints/storage/devices, and returns planned changes with IDs, arguments and dependencies (`apiserver/facades/client/bundle/bundle.go:102-172`); this planning path does not prove execution or successful deployment.

1. **Bundle and resulting model** — define the input, distinguish bundle data and overlays from resulting model entities; link application, charm, relation and deploy. Verify source merge semantics before specifying precedence.
2. **Bundle input structure** — identify declarations and references that the parser accepts, including validation and source/overlay scope only after their actual rules are traced; link key-specific owners rather than copy them.
3. **Planning and deployment** — parse/merge and validation; change-plan response and dependencies; execution through supported deployment paths. Include caller and per-stage errors as separately evidenced; do not imply returned plan means applied changes.
4. **Export and limitations** — the traced Bundle `ExportBundle` method returns not implemented (`bundle.go:197-200`); check the CLI/version path before generalizing to every export workflow. No storage schema or watcher required without independent evidence.

## hook

**Boundary.** A hook is a unit-agent invocation of charm code with a particular context; it is not itself a database change, watcher notification, action or generic command (`internal/worker/uniter/runner/runner.go:320-344,381-388,546-561`).

1. **Hook and context** — define unit/charm relation, hook kind, execution context and links to `unit`, `charm`, `hook-command` and action tasks.
2. **Hook triggers and selection** — state that some hooks follow watched state; the traced `update-status` timer updates local state and the resolver chooses its hook after earlier eligible work (`internal/worker/uniter/remotestate/watcher.go:685-688,720-729`; `internal/worker/uniter/resolver.go:362-390`). Do not generalize all triggers from these cases.
3. **Hook execution** — actor, context/environment, command dispatch, completion, failure/retry as separately verified; retain sourced rules and affected anchors without claiming a universal event ordering.
4. **Hook kinds** — each kind's triggers, context and restrictions, grouped by real behavior; link relation, storage, secret and lifecycle subjects. Verify each rather than infer actual firing from the registry.
5. **Commands, configuration and failures** — link `hook-command` for command grammar/context; describe configuration/timing and troubleshooting only where traced.

**Pending correction.** Replace both universal controller-state/database → watcher assertions at `hook.md:12,45` within the trigger/execution sections; keep watcher links for applicable paths (`work/story-form-110.md`).

## hook-command

**Boundary.** Hook/action commands are an interface made available in a unit-agent context; they are not Juju CLI commands or a guarantee that every command is valid in every event (`internal/worker/uniter/runner/jujuc/server.go:38-107,192-203`; `internal/worker/uniter/hook/hook.go:81-140`).

1. **Hook-command interface** — purpose, relation to hook/action context and `jujuc`; link `hook`, `agent` and relevant commands.
2. **Invocation and context** — naming, required environment/context and how a command reaches the unit agent; trace successful and error behavior per command before generalizing.
3. **Command families and index** — link generated individual command references; link each subject contract (relation, secret, storage, resource, status, leadership, actions) instead of duplicating it.
4. **Failures and limits** — context, permissions/leadership and per-command outcomes belong with the relevant command; registration alone is not success. No database schema or change-stream section without a separately evidenced contract.

## log

**Boundary.** Logs and audit records are observations, not an operation's return value, a status or proof of completed provider work. Debug-log and agent logsink use different endpoints/authorization (`apiserver/apiserver.go:864-885,1074-1085`); API audit is a separate recorder (`work/held-out-116.md`).

1. **Log and observation scope** — distinguish agent logs, controller audit and forwarding; identify their consumers and link status/telemetry.
2. **Log sources and records** — record format and storage only where traced; `audit.log` contains conversation/request/response records when the configured path records them (`core/auditlog/auditlog.go:189-245`).
3. **Actors and flows** — agent logsink → controller/debug-log as supported; API audit recorder → configured sink separately. Explain observable results without promising every source or retained line.
4. **Reading and filtering** — each relevant client/operator interaction, permissions and context; audit is installed for enabled user logins, configured exclusions filter conversations, and excluded calls may be flushed with a later interesting call (`apiserver/admin.go:170-179,197-221`; `apiserver/observer/auditfilter.go:37-76,117-139`).
5. **Configuration and failures** — link controller/model key definitions and forwarding/telemetry; argument capture is optional and response-error extraction is shape-limited (`apiserver/observer/recorder.go:53-121`). Verify retention and platform-specific log locations.

**Pending correction.** Replace `log.md:30`'s universal audit promise in sections 3–5. Do not present an all-calls/all-errors guarantee or expand the selected 35-page counter.

## removing-things

**Boundary.** Removal is a cross-subject process initiated by a request; advancing life and scheduling jobs is not proof that all dependent/provider work has completed. Unit, application, machine, model and storage have different paths (`domain/removal/service/unit.go:85-125`; `domain/removal/service/application.go:86-130`; `domain/removal/state/model/machine.go:120-225`).

1. **Removal and participants** — initiating actor, subject, dependencies, options; distinguish delete request, life transition, job processing and external cleanup.
2. **Shared lifecycle and job observation** — only transitions and observation surfaces that have been traced; do not infer identical states or timings for every subject. Link subject status and applicable watcher contracts.
3. **Initiating removal** — per-subject authorization/blocks and request parameters belong with their calls; the process page links to those calls and explains actual shared controls.
4. **Dependencies and cascades** — exemplify machine force: non-dead units or child machines reject ordinary removal, whereas forced path advances related lives and schedules work; link unit/machine/storage contracts. Avoid a universal cascade order.
5. **Storage, force and external effects** — distinguish scheduling/detachment and destruction; cite E58's provider/removal qualifications rather than promise filesystem loss or survival. Link model removal and tri-state storage choice where separately traced.
6. **Failures and recovery** — per-stage errors, forced cleanup and completion checks only where source-supported; provider completion, data integrity and all retry sequences remain open.

## scaling

**Boundary.** Scaling changes desired application/unit allocation, but a constraint value is not proof of provisioned capacity or in-place vertical resizing. Different model types have different paths (`domain/machine/service/provider.go:191-219`; `apiserver/facades/client/application/addunit.go:23-47`; `apiserver/facades/client/application/application.go:1267-1318`).

1. **Scaling and scope** — distinguish application unit count, machine allocation inputs and capacity; link application, unit, constraints and provider-dependent placement.
2. **Scaling on machine and Kubernetes models** — explain only traced call paths: `AddUnits` rejects CAAS; `ScaleApplications` rejects non-CAAS, checks write access/change block, then sets or changes desired scale. A returned desired scale is not proof every unit is ready.
3. **Constraints and storage effects** — input merge and allocation link to `constraint` and machine; attaching storage during the traced CAAS scale call returns not implemented (`application.go:1291-1303`). Do not claim setting constraints resizes an existing machine without a distinct trace.
4. **Observation, errors and availability** — link unit/application status and call-specific errors; application high availability depends on the workload and infrastructure, not merely count. Verify scale-down/removal consequences and provider behavior.

**CLI smoke check:** `go run ./cmd/juju help add-unit` and `go run ./cmd/juju help scale-application` both ran at the source anchor. The first describes adding units and machine-only `--to`; the second describes setting desired Kubernetes units. These are live CLI help outputs, not executed scaling or evidence that backend/provider work succeeds.

## script

**Boundary.** A script invocation creates an operation, which groups tasks for targets; action runs are one source and administrative exec is another. The `Run` path checks model admin and change blocks, builds machine/unit/application targets and enqueues an exec operation (`apiserver/facades/client/action/operation.go:241-261,296-310`). An action invocation has its own checks and unit-only target semantics (`:32-98`).

1. **Script, operation and task** — preserve existing `script`, `operation`, `task` anchors; distinguish declaration, operation and per-target task. Correct unit-only descriptions: machine targets are supported on the traced exec path, not for charm actions.
2. **Operation/task records and status** — shared identities, target relationships and relevant task output/log records; place any shared diagram and invariants here if verified against source. Link object-store output and action declaration. The proposed relocation from `action` is not yet approved.
3. **Operation/task streams and actors** — describe only verified agent/client streams and target-specific differences; link machine and unit agents, action command context and watcher.
4. **Creating and observing operations** — action and exec entry points, inspect operation/task output, cancellation/pruning only once each path is traced. State caller, conditions and errors at the actual interaction; do not equate task creation with success.
5. **Operation/task migration** — shared migration exception and affected output only after verifying source; link model migration.

**Open.** The currently proposed shared task/operation home makes semantic sense because both actions and exec use them, but the exact location of current diagrams, historical anchors and existing incoming links must be examined before a move. Findability is untested.

## status

**Boundary.** Status is an observation of subject state, not the desired configuration, the API request result, a log or a guarantee that cloud work finished. `FullStatus` checks controller-superuser or model-read access (`apiserver/facades/client/client/client.go:49-60`) and composes model, applications, units, machines and related information; offer details are admin-only (`client/status.go:126-181`).

1. **Status and scope** — distinguish model, application, unit, machine, task and storage observations; link subject-specific transitions and API errors.
2. **Status values and records** — common vocabulary only where shared semantics are traced; keep independently varying status fields and their subject-specific meaning at the subject. Verify state/value lists and inspector relevance.
3. **Producers and update paths** — distinguish agent/workload reporting, controller composition and provider-derived status only where each actual source is traced; no universal freshness claim.
4. **Reading status and history** — caller, permission, filtering and response per interaction; note admin-only offer detail on the traced `FullStatus` path; verify history retention and availability before describing it.
5. **Errors, logs and changes** — link `log`, watchers and subject failure contracts; an accepted request or one status snapshot is not proof of completion. Preserve any status/transition anchors.

**E62 refinement, proposal:** Distinguish current unit agent/workload status from its history: each traced setter writes current state and only then calls the history recorder; if the recorder returns an error, the setter logs a warning rather than returning that error (`domain/status/service/service.go:401-424,452-484`). A client history query has its own kind/tag/filter and log-reader conditions (`apiserver/facades/client/client/status.go:53-109`; `domain/status/service/statushistory.go:17-58`). The source does not guarantee recording, retention, completeness or that a particular normal input triggers a post-write recorder error. Place the common conditional behavior once with links or keep complete call-local copies only as an editorial proposal; preserve per-kind validation. Whether the history contract is a distinct section, page or unit facet is not decided by source (`work/structure-challenge-e62.md`).

**Post-hoc applicability issue:** `show-status-log` help and `HistoryKind.Valid()` include `filesystem`, `volume`, `task`, `saas`, `container` and `juju-container`, but the traced history filter does not handle those kinds and its caller drops the default error (`core/status/status_history.go:73-115`; `domain/status/service/statushistory.go:29-43,74-104`). A real service/reader probe with synthetic records returned one workload match and zero filesystem matches, both with nil error. This is a potential implementation/contract defect, not a live controller result. Do not state those kinds work merely because they appear in help, or conceal the issue by a documentation-only fix; investigate before finalizing the history section (`work/structure-challenge-e62.md`).

## watcher

**Boundary.** A watcher delivers changes or notifications to a particular holder; it is distinct from the underlying state, a complete status snapshot and the hook that may follow. Different watcher payloads and holder permissions must be traced per watcher.

1. **Watcher and stream** — define subscription, holder, initial delivery and payload at the general level supported by implementations; distinguish an empty notification from a payload containing changes.
2. **Watcher lifecycle and delivery** — on the traced generic `NotifyWatcher`, subscribe, drain the initial event, dispatch an initial empty notification, filter/map later changes and stop on tomb/subscription closure (`core/watcher/eventsource/notify.go:93-151`). Do not turn this one implementation into a universal no-loss, ordering or payload guarantee.
3. **Reading subject changes** — link each subject's actual watcher with caller, filter and payload. The relation-unit watcher exposes a different payload (`apiserver/facades/agent/uniter/watcherrelationunit.go:104-139`).
4. **Errors and limits** — failed subscription/closed watcher, reconnect and stream-specific rules only where traced; `update-status` timer shows not every hook follows a watcher. No unnecessary database-schema section.

## Comparison with current pages, after derivation

Current headings are navigation and review leads, not evidence of runtime behavior. Preserve all current anchors, figures and facts until source tracing assigns or corrects them; these outlines are not instructions to delete unlisted material.

| Page | Existing material and proposed treatment |
|---|---|
| `index.md` | Current grouped landing and alphabetical glob are navigation, not an ontology. The landing-page stakeholder owns its policy; no restructure is proposed without direction. |
| `agent.md:17-66` | Kinds, facades, workers and credentials already have stable sections. The common login/target checks and selected unit runner support part of the model; full facade eligibility, worker dependencies and credentials behavior remain unverified. |
| `bundle.md:14-26` | Existing bundle/overlay definitions can be compared with the traced YAML merge and planning path; overlay precedence and execution still need tracing. Export's traced API error does not by itself establish the CLI workflow. |
| `hook.md:21-148,149-891` | Preserve kinds, execution guarantees, ordering, errors, event-specific hooks and environment anchors. Replace the two universal initiation claims; do not infer the remaining kinds, ordering or guarantees from one timer case. |
| `hook-command.md` | Retain the command index and subject links; derive each command's context and effects separately from the runtime, not its generated help. The individually assigned hook-command investigation was denied with a 402 and is not available in this session. |
| `log.md:16-102` | Preserve machine/Kubernetes log and agent-stream/call addresses; audit filtering and log-sink flow are distinct. Correct the all-calls assertion, while independently tracing retention and the current watcher contracts. |
| `removing-things.md:12-34` | The existing terms and force narrative need individual command/cascade evidence. A specific forced machine-removal trace does not prove one universal severity ordering or every force outcome. |
| `scaling.md:14-17` | Separate machine unit addition from CAAS desired scale and provider allocation. The generic constraints example does not establish that an existing resource is resized. |
| `script.md:7-24` | Existing neutral script/task/operation anchors need the machine-exec correction. The proposed shared task-record/stream move from action depends on verifying current anchors, diagrams and each actual path. |
| `status.md:12-73` | Existing application/unit status vocabulary and CLI output are comparison data; `FullStatus` composition does not establish every status transition or historical field claim. |
| `watcher.md:13-61` | Retain kind, lifecycle, backing-stream and holder addresses; the notify implementation does not by itself establish identical behavior for all watcher kinds, all clients or all hooks. |
