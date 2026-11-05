# E70: operation and task boundary across actions and exec

**Status:** source-grounded structural proposal, not an authorized page or
repository-rule change. E70 was registered in `structure-discovery-plan.md`
before inspecting these paths. Source paths below are relative to the established
4.1 anchor `/tmp/juju-41-tree`, revision `e5db99d585`. Existing action/exec
research makes this a repeated, not held-out, challenge.

## Result in plain language

An **action** is work defined by a charm. Administrative **exec** runs a command;
it is not a charm action. Both can create an **operation**, the controller's
record of one request, and **tasks**, individual records for its targets. The
same inspection API can show either kind of operation and its unit or machine
tasks. An operation or task number means work was enqueued; it does not mean
that work ran successfully. The API can report an operation number alongside
errors for individual targets.

**E70 passes on the traced source paths**, not as a live-controller or
end-to-end runtime result. It supports a neutral, shared semantic address for
operation/task concepts and observation, with action and exec initiation kept
separate. It does not prove that the shared address must physically be in
`script.md`, or that a single copy with links is better for readers than fully
qualified repetitions. `script.md` has existing neutral `operation` and `task`
anchors, but its unit-only definitions at lines 15 and 24 omit the traced
machine-exec path. That is an already-queued correction, not an edit.

## Traces: from request to observable records

| Stage | Charm action | Administrative exec |
|---|---|---|
| Exposed initiating API and actor | A client calls `ActionAPI.EnqueueOperation`. It checks model write permission, requires at least one action, parses unit tags or a leader-unit selector, and checks application consistency (`apiserver/facades/client/action/operation.go:32-98`; permission helper `action.go:145-150`). | A client calls `ActionAPI.Run`. It checks model admin permission and the model change block, accepts application, machine and unit inputs, validates command parameters and calls `AddExecOperation` (`operation.go:241-261,314-328`; `action.go:305-321`). `RunOnAllMachines` is a separate, model-type-restricted path (`operation.go:264-293`). |
| Request-specific definition | A task uses the named action and parameters; state finds the application's charm and verifies/inserts the action association (`domain/operation/state/start.go:142-167,385-425`). | The request contains a command and timeout; the state stores those as operation parameters (`state/start.go:197-229,336-346`). |
| Result and partial failures | The service resolves units/leaders and invokes `AddActionOperation`; state creates an operation and attempts each unit task (`service/start.go:169-186,198-207,245-263`; `state/start.go:101-194`). The facade returns an operation tag and per-input action results (`operation.go:113-133`); when no valid receiver remains, it instead returns per-action errors without starting the service (`:77-98`). | The service resolves leader inputs and passes machine/unit/application receivers to `AddExecOperation` (`service/start.go:93-112`); state inserts the operation, attempts machine and unit tasks and returns a `RunResult` (`state/start.go:197-276`). The facade converts the operation ID and both receiver kinds into the same `params.EnqueuedActions` form (`operation.go:296-311`). |
| Common recorded task and initial state | Both call the same `addUnitTask` path; each successful inserted unit task receives `pending` (`state/start.go:169-187,259-275,565-617`). | A machine task uses the same operation-task and task-status record functions and also starts `pending`, with a separate machine association (`state/start.go:516-561,620-685`). |
| Shared supported observation | `ActionAPI.Operations` checks model read access, parses each operation tag, and calls `GetOperationByID` (`operation.go:215-236`; `action.go:141-143`). Service/state read the operation and its tasks and return one `OperationInfo` with unit and machine task lists (`service/query.go:71-103`; `state/query.go:123-163,217-266`). Facade conversion returns operation status and converted task results (`action.go:332-384`). The same reader does not branch on whether creation was action or exec. |

These are implementation traces, not proof that an actual deployment has
executed either request. In particular, a request can pass the facade but fail
at service/state; success can include **per-target** errors. Task creation is
attempted per target inside an operation transaction, with individual errors
returned in task results rather than automatically failing the entire request
(`state/start.go:169-194,234-257`). Do not promise that every named target got
a task, or describe an operation tag as proof of successful task completion.

The action consistency check compares the first two incoming action parameter
sets: its return is inside the loop after comparing the second (`operation.go:
136-170`). That known limitation is not proof all later parameter sets were
validated. Application-consistency checking is a separate receiver loop.

## Executable checks

A temporary program called Juju's actual unit/machine tag parsers and
`operation.ActionReceiver.Validate`. It printed, in relevant part:

```text
unit-web-0: unit-error=<nil> ... machine-error="unit-web-0" is not a valid machine tag
machine-0: unit-error="machine-0" is not a valid unit tag ... machine-error=<nil>
action receiver unit="" leader="": one of Unit or LeaderUnit must be set
action receiver unit="web/0" leader="": <nil>
action receiver unit="" leader="web": <nil>
action receiver unit="web/0" leader="web": only one of Unit or LeaderUnit should be set
```

This exercises the actual parser used by the action facade and the service's
receiver validator, not the facade or an exec operation. The machine parser
comparison is illustrative: the traced exec facade passes machine names, not
machine tags, to the service. The temporary program was removed.

### Post hoc status observation

After reading the aggregation code, a separately registered follow-up exercised
the actual `operationStatus` helper through a temporary exported wrapper, and
`CompletedTaskResult.Validate` with synthetic inputs:

```text
completed-task aborted validation: <nil>
statuses=[aborted] result="" error=unknown status
statuses=[aborted completed] result="completed" error=<nil>
statuses=[pending aborted] result="pending" error=<nil>
```

Both temporary files were removed. The helper does not include `aborted` in its
active or completed precedence lists (`service/query.go:21-36,106-130`). A
further separately registered program called the **real** `GetOperationByID`
service with a synthetic state implementation returning one unit task. It
returned `operation=pending error=<nil>` for an `aborted` task and
`operation=completed error=<nil>` for a `completed` task. The service logged an
aggregation error for the aborted input; the temporary program was removed.
This proves the service's fallback on synthetic state, not a live database,
facade/RPC or controller.

An authorized unit agent's `FinishActions` checks the task's receiver and passes
the provided status to `FinishTask` (`apiserver/facades/agent/uniter/uniter.go:
1289-1305,1309-1331`); the machine facade has the analogous ownership check
(`machineactions/machineactions.go:134-150,155-173`). The completed-result
validator accepts `aborted`, and state finish updates the status
(`domain/operation/types.go:18-34`; `state/task.go:233-250,262-297`). In the
unit agent's actual action runner, an observed `aborting` status closes its
cancellation channel (`internal/worker/uniter/operation/runaction.go:95-119`);
when the channel is closed and action failure or execution error occurs, the
finalizer chooses `aborted`, subject to its later flush-error override, and calls
the uniter finish API (`internal/worker/uniter/runner/context/context.go:
1768-1820`; `api/agent/uniter/uniter.go:286-301`). This is a source-traced
path, not a live cancel/run; the separately known cancellation SQL issue may
prevent normal entry into `aborting` and remains unresolved.

The all-aborted `pending` result is a potential implementation/contract issue,
not an authorized prose-only fix. It is **not a newly discovered documentation
omission**: `action.md:207-209` already states the fallback. The intended
aggregate status and the outcome of a real controller cancellation remain open.

## Proposed content map

A **semantic address** is a link target for a contract; it can be a page or a
section. The following are proposals for future review, not edits or proof of
unique physical placement.

| Subject | Contract and candidate address | What belongs locally / links |
|---|---|---|
| Charm action | `action`: definition, declaration, action parameters and action enqueue. | Unit/leader selection, same-application check, model-write guard, definition validation, per-input errors and timing remain with action enqueue. Link to charm, application, unit and shared operation/task. |
| Administrative exec | A neutral administrative-exec interaction address; current `action-running-commands` is a candidate link location, not a source-derived file decision. | Model-admin and change-block guards; command/timeout and machine/unit/application target rules; per-target errors and separate all-machines constraints. Link machine, unit, model controls and shared operation/task. Do not characterize exec as a charm action. |
| Operation | Neutral shared address, with existing `script` → `operation` as a conservative candidate. | Operation identity, common request/grouping record, optional action association versus exec parameters, creation result, inspection and derived-status limits. Link both initiating interactions and task; never imply all targets succeeded. |
| Task | Neutral shared address, with existing `script` → `task` as a conservative candidate. | Per-target identity; unit/machine distinction; pending creation; individual observation, status/result/logs where actually traced. Separate unit/machine execution and task-specific permissions. Link operation, target, result/output and agents. |
| Interface examples | CLI `run`/`exec` generated pages remain invocation examples. | CLI syntax and local handling stay at the interface; API/shared contract must not depend on a CLI-only explanation. Publication/generation mechanics remain unresolved. |

Operation and task have distinct identities and observations, but a task is
linked to an operation on these paths. The distinction justifies independently
linkable *concepts*, not necessarily two files. A shared contract could be a
section under `script`, a neutral dedicated page, or a qualified section under
`action` linked from exec; those can preserve the same facts, links and scope.
`script` is a conservative candidate because its neutral anchors already exist,
not because the code selects that filename. A client-facing label `action` in
`params.ActionResult` or an `action-` tag does not turn machine exec into a
charm action.

### Errors, diagrams and timing

- Preserve action enqueue's write/receiver/definition errors at **action
  initiation**, exec's admin/block/command errors at **exec initiation**, and
  per-target errors in each result. The operation reader's read permission and
  per-ID errors belong at **inspection**. Do not combine these into one
  authorization rule for every task.
- A shared operation→task→unit/machine figure belongs with the **shared record
  structure** if its details are independently verified. An action execution
  sequence belongs with **action initiation and execution**; an exec sequence
  needs its own machine/unit actors and source checks. Preserve existing diagram
  and anchor links until a concrete approved edit.
- Keep request → state insertion → response → agent execution → observation
  separate. Only insertion, pending result and later common read are traced
  here; full agent execution, watcher delivery, result storage and their order
  are not established by this slice.

## Registered checks

| Prediction or criterion | Result | Evidence and limits |
|---|---|---|
| Both creation paths lead to a common observable operation/task contract | Supported by source | Common inserted operation/task records, API result conversion and `Operations` retrieval above. No actual operation was created in the smoke. |
| Action is unit-targeted; exec accepts machine targets on these paths | Supported | Facade receiver parsing, state task creation and parser/validator probe; no live target. |
| At least one initiation guard differs | Supported | Action enqueue checks write; exec checks admin and change block. Do not infer universal authorization from these calls. |
| Enqueue is not completion | Supported | Both successful task creation helpers return `pending`; task execution is a separate actor/process. No guarantee that every target succeeds. |
| Shared and interaction-specific facts have usable addresses, error and diagram homes | Supported as a proposed plan | Table and distinctions above. Incoming anchor preservation, diagram correctness and publication require later review. |
| Physical location uniquely follows from source | Not predicted; unresolved | Different physical arrangements can carry equally qualified facts and links. No reader study was performed. |
| Post hoc aborted-status follow-ups | Predictions supported | Real aggregation helper and service with synthetic state; authorized finish and conditional unit-agent abort paths source-traced. No live controller or actual cancellation; existing action page already mentions the fallback. |

No page or rule was changed. The 402-denied `WorkloadModel`,
`HookCommandPages`, and `KubernetesCloudAttributes` scopes remain blocked and
were not relaunched or replaced. No live controller, agent, database, charm,
provider, or actual action/exec request was exercised.

## E81: placement comparison against the actual PR

This is a continuation using the existing `knowledge-structure-118.md` map,
E70 and the actual PR worktree at `48ef1fca17`, not a new inventory or an
approved page/skeleton/figure/rule edit. E81 was registered in
`structure-discovery-plan.md` before the detailed comparison, but E70/E71 and
the openings of `action.md` and `script.md` were already studied: this is
contaminated, not a held-out comparison, independent validation or reader study.
The company requires Diátaxis and the existing `ibnote` links interweave its
categories; preserve them. Source is evidence of behavior and scope, not a
unique physical page or a substitute for documentation-purpose decisions.

### What is actually there

- `docs/reference/script.md:7-24` has `(script)`, `(task)` and `(operation)`.
  Its task and operation definitions say the targets are units, even though
  E70's exec path includes machines. Its umbrella definition calls both charm
  actions and commands scripts; whether this is an appropriate shared concept
  is unresolved. The reference index links `script` under Models and
  applications (`docs/reference/index.md:69-85`).
- `docs/reference/action.md:20-51` already has a substantial shared
  operation/task schema and `Action database schema` ggarch view, explicitly
  including machine targets and an optional action association. The existing
  `(action-running)` action-specific call is followed by
  `(action-running-commands)` with exec's admin/change-block conditions
  (`:86-148`); task/operation observation and the `Task status` figure follow
  (`:150-244`). The first is not an omission. The current `(action-running-commands)`
  ibnote points to the action guide; `howto/manage-machines.md:259-276` instead
  demonstrates `juju exec` and links its generated CLI reference. The action
  guide links `(task)` and `(operation)` from its task/operation sections
  (`howto/manage-actions.md:113-180`). A limited ref search found these inbound
  uses; this is not an exhaustive external/HTML-fragment link audit.
- The actual facade checks write for action enqueue and admin plus a change
  block for exec, while the shared operation reader checks read
  (`apiserver/facades/client/action/operation.go:32-35,215-261`). If every
  action receiver is invalid, enqueue returns per-item errors without calling
  the service (`:77-98`); do not state that every request returns an operation.
  Earlier real-code synthetic status checks and the separate cancellation SQL
  issue remain unresolved (`:70-111` above). No action/exec request ran here.
- The existing generated `exec.md:1-30,42-50` exposes machine and unit options
  and refers to admin users. The actual local `go run ./cmd/juju help exec`
  printed the same named targets and options. This is CLI help only; it is not
  an API, controller, agent or execution test.

### Alternatives and actual consequences

All three can potentially satisfy the registered outline conditions if they
preserve distinct calls, machine targets, anchors and figures. No alternative
has been built, fully link-checked or tested with readers; the following are
tradeoffs, not observed reader or maintenance outcomes.

| Shared contract home | Benefit | Strongest objection / necessary work |
|---|---|---|
| Keep under `action.md` | Existing schema, figure and detailed call sections stay together. | Exec is not a charm action; a page explicitly named action can imply the wrong scope. Add clear neutral entry points and context from exec; avoid claiming existing links alone establish discoverability. |
| Use existing `script.md` | Existing neutral `(task)` and `(operation)` anchors and their inbound guide links can remain on their current page. | The page calls both cases scripts, a disputed umbrella, and must be corrected for machine targets; common schema/observation is currently elsewhere. A label or existing file is not a proof of its semantic fitness. |
| Neutral operation/task page | Names the common contract without making either initiation its parent. | New/relabelled address and potential URL/anchor moves; keeping existing figure, incoming links, and usable context needs a concrete migration plan. More separation can impose extra navigation and maintenance. |

**Working recommendation, not a settled algorithm:** a neutral shared
operation/task subject is the clearest semantic account of both traced paths;
retain `script.md` as the provisional physical file, with a neutral page title
and the existing `(task)` and `(operation)` anchors. This is a conservative
address choice, not proof the title/filename is best. Retain `(script)` and
its intended meaning at a verified, compatible target; the `script` concept and
what happens to its existing index entry remain explicitly unresolved. If that
cannot be done coherently, the neutral new-page alternative remains available.

**Conditional proposed delta, not implementation:**

1. At the neutral shared address, define operation and task for action and exec,
   including unit *and* machine targets, partial results and request versus
   completion. Present the current common record/schema account and its ggarch
   view there only after verifying the figure and migration mechanics. Keep
   existing `(task)` and `(operation)` references working.
2. At `action.md`, retain action definition, listing and action enqueue with
   its write/receiver/definition errors and the action-specific sequence view.
   Give exec its own neutral interaction address and retain its admin/change
   block, target-specific results and errors. `(action-running-commands)` is
   already an address and must remain compatible; whether to keep it on
   `action.md` or relocate it follows the still-unresolved page-level rule.
3. Treat showing/listing/cancelling/running tasks and operation inspection as
   shared or initiation-specific **only after** tracing each actual call and
   its anchors; do not blindly move every `Action` facade section. Preserve
   `(action-database-schema)`, `(action-task-status)`, their figure views and
   all other affected legacy anchors, including direct URL fragments; a MyST
   label alone does not prove an old URL remains valid after relocation.
4. Retain the action guide's action-specific tasks and ibnotes. Add an exec
   path from the real machine-guide section and the existing command reference
   to the shared contract where appropriate; the machine-guide section has no
   explicit label at `:259`, so a section-level target needs a proposed anchor
   or verified generated heading target. Do not assert one exists. Preserve
   command-local syntax in generated help rather than editing generated output.
5. For JUJU-10586 retain exact per-call authorization, whole-call/per-item
   error, code, trigger and remediation at their originating interaction, with
   source/version evidence. No exhaustive error reclassification or per-call
   drift enforcement follows from this comparison. For JUJU-9635 retain both
   existing ggarch views, accessible alternatives and relevant context; neither
   their present location nor this outline verifies their complete correctness.

### Missing rule exposed

The map supports the **semantic distinction** between an action-specific
interaction and the shared operation/task contract. A useful proposed rule is:
do not subordinate a shared contract to a participant when its scope includes
another distinct participant; retain participant-specific interactions locally.
It predicts a neutral shared subject in this case. But this still does not
determine page versus section, resolve what constitutes an appropriate umbrella,
or prove that the neutral home helps users. The current case cannot establish
that those distinctions generalize; action, script and E70 were already known.
Do not replace the full-reference family map or call E81 a held-out pass. No
new process, docs page, error checker, figure, source, PR or repo rule was changed.
