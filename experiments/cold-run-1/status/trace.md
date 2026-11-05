# Trace of the draft (draft-status.md) to 4.1 source at e5db99d585

Paths are in the tree at e5db99d585. "U:" means a statement of the upstream page itself kept as is. Class: S = source, H = source help text (documentation string in source), U = upstream doc statement, X = Unverifiable (marked in draft or dropped).

| Id | Statement (short) | Trace | Class |
|---|---|---|---|
| S1 | A status is a value with a message and the time of last update | core/status/status.go:23-29 (Status, Message, Data, Since); status-set help: "last updated" attribute, internal/worker/uniter/runner/jujuc/status-set.go:31-33 | S |
| S2 | An application has one status, derived from units unless leader sets it | domain/status/service/service.go:348-352, 370-372; leaderservice.go:68-72, 172-182 | S |
| S3 | A unit has workload and agent statuses | domain/status/service/status.go:441-450 | S |
| S4 | The charm reports workload status; Juju reports agent status | status-set.go:30-31, 163-172 (workload); uniter/agent.go:15-22 (agent set by uniter); status.go:265-270 (lost derived) | S |
| S5 | Machines, models, relations, storage, tasks have statuses with values of their own | core/status/status.go:14-15, 57-92 (machines), 178-196 (storage), 198-210 (models), 212-231 (relations), 233-251 (tasks) | S |
| A1 | Application status derived from workload statuses its units display | status.go:558-586 (uses decodeUnitDisplayAndAgentStatus display status, so includes agent-error to workload-error and K8s overlay) | S |
| A2 | Severity order error, blocked, maintenance, waiting, active, terminated, unknown | status.go:544-552 | S |
| A3 | One blocked unit makes the app blocked unless another is in error | status.go:581 (strictly greater wins) with 544-552 | S |
| A4 | Ties: leader if among them, otherwise lowest number | status.go:572, 581, 588-606 (leader sorts first, then ascending ordinal; first unit with the top severity is kept) | S |
| A5 | No units gives unknown | status.go:562-566 | S |
| A6 | Leader sets app status with `status-set --application` | status-set.go:43-44, 138, 168-169; leaderservice.go:73-107 | S |
| A7 | Value one of maintenance, blocked, waiting, active | status-set.go:130-135, 145-154 | S |
| A8 | This status replaces the derived one | service.go:370-372; leaderservice.go:172-182 | S |
| A9 | Non-leader gets `this unit is not the leader` | leaderservice.go:100-106 (UnitNotLeader); message text in status-set.go:116-119 (help text example only; the rendered text from statuserrors.UnitNotLeader was not traced) | H |
| U1 | A unit's status is the pair workload and agent | status.go:441-450 | S |
| W1 | Workload status reports whether the workload provides its service | status.go:172-175, 146-150 (definitions); the summary sentence is editorial | S/editorial |
| W2 | Charm sets one of the four with status-set at any time and any order | status-set.go:130-135; domain/status/service/service.go:401-425 (encode only, no check of the previous value) | S |
| W3 | Other value gives `invalid status "<value>", expected one of [maintenance blocked waiting active]` | status-set.go:152-154 (`%v` of a slice of Status prints `[maintenance blocked waiting active]`) | S |
| W4 | Juju sets error, unknown, terminated | error: uniter.go:893-919, status.go:423-438; unknown: runhook.go:259-268, status.go:320-326, 562-566; terminated: runhook.go:254-258 | S |
| W5 | Juju also sets waiting and maintenance at start and removal | application/service/unit.go:989-1009; uniter.go:693-696; runhook.go:209-227, 250-253 | S |
| W6 | Meaning of a charm-set value is up to the charm author | U (upstream status.md L41); consistent with status-set.go:46-84 (charm-facing guidance) | U |
| W7 | active meaning | core/status/status.go:172-175 | S |
| W8 | maintenance meaning, examples, no intervention | status.go:146-150; status-set.go:50-51, 90-91, 88-89 ("self-resolve"); "No human intervention is required" is U (L49) | S/U |
| W9 | waiting meaning | status.go:163-166; status-set.go:53-56 | S |
| W10 | blocked meaning; message says how to unblock; example | status.go:168-170; status-set.go:52, 67-70, 105 | S |
| W11 | error: a hook of the unit failed; message names the hook, `hook failed: "install"` | uniter.go:893-919 (message built with %q of the hook name); status.go:437 (agent message copied to workload) | S |
| W12 | unknown after start hook with no charm status | runhook.go:259-268; status.go:158-161 | S |
| W13 | unknown when the agent is lost, with a message pointing to logs and history | status.go:320-327 (message text mentions `juju debug-logs` or `juju show-status-log`; the draft says "the unit's logs and status history" to avoid repeating the source's `debug-logs` spelling) | S |
| W14 | terminated after the remove hook; the unit is gone | runhook.go:254-258; status.go:153-156 | S |
| G1 | Agent status reports what the unit agent is doing | status.go:107-135; uniter.go:387-396 | S |
| G2 | Unit agent and the controller set it; status-set sets workload only | status-set.go:30-31; status.go:265-270; unit.go:1000-1003 | S |
| G3 | idle: installed, running, nothing to do, stays until a hook or task | status.go:125-129; uniter.go:387-396 (idle only when nothing queued and not in error) | S |
| G4 | executing: running a hook or task; message says which | status.go:120-123; uniter/op_callbacks.go:156-159 | S |
| G5 | allocating: Juju created the unit; on machine and Kubernetes models | application/service/unit.go:989-1009 (IAAS and CAAS both use makeUnitStatusArgs with allocating) | S |
| G6 | rebooting: machine being rebooted after juju-reboot; should return to idle | status.go:115-118; uniter/runner/context/context.go:1530-1550 | S |
| G7 | error: a hook failed; message `hook failed: "<hook>"` | uniter.go:893-919 | S |
| G8 | failed: an operation of the unit agent failed | uniter/agent.go:25-37; status.go:97-104 | S |
| G9 | lost: controller has not heard from the unit agent; message text | status.go:131-134, 261-270 | S |
| G10 | Setting allocating or lost is refused | domain/status/service/service.go:465-466 | S |
| G11 | With agent error, juju status shows workload error + agent idle; workload message is agent's | status.go:423-438 | S |
| L1 | Start-up step 1: allocating + waiting, messages by model type | application/service/unit.go:989-1009 | S |
| L2 | Step 2: agent changes message to `agent initialising` | uniter.go:683-698 | S |
| L3 | Step 3: install hook sets maintenance `installing charm software` unless charm set status | runhook.go:209-217 (state.StatusSet) | S |
| L4 | Step 4: executing while hooks run; idle when nothing left | op_callbacks.go:156-159; uniter.go:387-396 | S |
| L5 | Step 5: after start hook, unknown if no charm status | runhook.go:259-268 | S |
| L6 | Charm can replace workload at any step | status-set.go:163-172; no transition check (service.go:401-425) | S |
| R1 | Stop hook: maintenance `stopping charm software`; after, maintenance no message | runhook.go:218-222, 250-253 | S |
| R2 | Remove hook: maintenance `cleaning up prior to charm deletion` | runhook.go:223-227 | S |
| R3 | After remove hook, terminated | runhook.go:254-258 | S |
| K1 | On K8s Juju tracks the pod status; shown workload can be the pod's | status.go:477-520 | S |
| K2 | Order 1: no pod status gives charm status | status.go:485-491 | S |
| K3 | Order 2: terminated, blocked, maintenance of the charm win | status.go:492-498 | S |
| K4 | Order 3: pod blocked | status.go:500-504 | S |
| K5 | Order 4: pod waiting while charm active | status.go:506-510 | S |
| K6 | Order 5: pod running when charm status is start-up waiting with one of the three messages | status.go:512-517, 522-540 (legacyIsStatusModified false only for status unset or waiting with one of three messages; the unset case is not stated in the draft, a simplification) | S |
| K7 | Order 6: charm status otherwise | status.go:519 | S |
| J1 | juju status shows app status in Status column of App section; unit statuses in Workload and Agent columns of Unit section | cmd/juju/status/output_tabular.go:143-145 (App, Status), 267-269 (Unit, Workload, Agent) | S |
| J2 | Sample output without SLA column | output_tabular.go:64-75 (header Model, Controller, Cloud/Region, Version, optional Timestamp, optional Notes; no SLA anywhere in the file) | S |
| J3 | Sample rows | U (upstream sample); the version `4.0.15` and the rows were not regenerated; needs a live 4.1 run | X (flagged) |
| J4 | Link to command page | docs/reference/juju-cli/list-of-juju-cli-commands/status.md:1 label `command-juju-status` | S |

## Links used (labels verified at e5db99d585)

`unit` (docs/reference/unit.md:7), `unit-agent` (docs/reference/agent.md:31), `hook-command-status-set` (hook-command/list-of-hook-commands/status-set.md:1), `hook-install`, `hook-start`, `hook-stop`, `hook-remove` (docs/reference/hook.md:722, 761, 789, 742), `command-juju-status` (above). Preserved addresses: `status`, `application-status`, `unit-status`, `workload--charm-status`. New: `agent-status`.

## Statements dropped for lack of a trace

- `<workload status>/<agent status>` written form (upstream L31): no formatter in cmd/juju/status produces it (grep of `%s/%s` and workload/agent joins found nothing).
- "missing or malformed config item" as a blocked example (figure): no source line; kept only the traced `Add a database relation`.
- All eight transition arrows of the old figure: see findings F-fig-1.
- "charm pod" in `allocating`, "container" in `idle`/`executing`: Kubernetes-only wording; source describes the unit agent generally.
- "Unit agent ... as it interacts with the juju controller": editorial; dropped.

## Checks run on the draft

- Oxford comma: checked by eye in every list of three or more.
- Lists are introduced by a sentence ending in a colon that says something.
- No version scoping, no "databag", American spelling.
- Page-rules checker `tools/check_page_rules.py` and error checker: not run (not in the permitted inputs).
- Docs builder (html, latex): not run.
