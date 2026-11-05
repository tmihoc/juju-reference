# Trace of the draft (draft-status.md) to the 4.1 source at e5db99d585

Paths are relative to the repository root at e5db99d585. "U" means an upstream doc statement (docs/reference/status.md, line). Verdict: T = traced, T* = traced with a stated caveat, U = Unverifiable (dropped from the draft unless marked).

| # | Draft statement | Source (file:lines) | Verdict |
|---|---|---|---|
| 1 | A status is a value with a message and a timestamp | core/status/status.go:24-29 (`StatusInfo`: Status, Message, Data, Since) | T |
| 2 | Each application has one status | domain/status/service/service.go:364-395 (one application status or derived) | T |
| 3 | Each unit has a workload status and an agent status | domain/status/service/status.go:409-451 (returns agent and workload) | T |
| 4 | Workload status reports the charm's workload; agent status reports the unit agent | core/status/status.go:107-176 (comments "specific to unit agents", "reflecting the state of the software itself"); status-set.go:31 ("Sets the workload status of the charm") | T |
| 5 | An application's status is the status the charm has set; when none set it is taken from units | domain/status/service/service.go:348-395 (if status != Unset, use it; else derive from units) | T |
| 6 | Only the leader unit can set the application status, with status-set --application | internal/worker/uniter/runner/jujuc/status-set.go:43-44, 116-119, 138 | T |
| 7 | App status from units is the workload status shown for the highest-severity unit | domain/status/service/status.go:558-586 (uses display status via decodeUnitDisplayAndAgentStatus, line 577) | T |
| 8 | Severity order error, blocked, maintenance, waiting, active, terminated, unknown | domain/status/service/status.go:544-552 | T |
| 9 | One unit blocked makes app blocked when no unit in error | derived from 8 and 581 (strictly greater severity replaces) | T |
| 10 | App also takes the message of that unit | domain/status/service/status.go:577-582 (`result = displayStatus`, whole StatusInfo) | T |
| 11 | Ties: leader first, else lowest unit number | domain/status/service/status.go:572, 591-606; 581 (strict `>` keeps the first); service.go:379-389 (leader lookup failure leaves leader empty) | T |
| 12 | No units: unknown | domain/status/service/status.go:562-566 | T |
| 13 | A client shows the two unit statuses as separate values | domain/status/service/service.go:1252-1257 (separate agentStatus, workloadStatus); cmd/juju/status/output_tabular.go:267-269 | T |
| 14 | A charm sets maintenance, waiting, blocked, active; command accepts each at any time, rejects every other value | status-set.go:130-135, 141-160 (membership check only; error text line 153) | T |
| 15 | Juju sets error, unknown, terminated | error: status.go:418-439, uniter.go:918-919; unknown: runhook.go:259-268, status.go:317-327; terminated: runhook.go:254-258 | T |
| 16 | active meaning | status-set.go:57-58; core/status/status.go:172-175 | T |
| 17 | maintenance meaning, needs no person | status-set.go:50-51, 88-89 ("short downtime that should self-resolve"); core/status/status.go:146-151 | T |
| 18 | Juju sets maintenance with the three messages before install, stop, remove hooks | internal/worker/uniter/operation/runhook.go:209-228 (install only when `!state.StatusSet`, stop and remove always). The draft says "before the install, stop and remove hooks run" and omits the install exception in the table; the exception is in the new-unit paragraph. | T* |
| 19 | waiting meaning, external factor, example related application not running | status-set.go:53-56 | T |
| 20 | Juju sets waiting on a new unit | domain/application/service/unit.go:997-1009; domain/application/state/unit.go:893-897 | T |
| 21 | blocked meaning; message tells the person what to do | status-set.go:52, 67-70 | T |
| 22 | error: hook failed or upgrade failed; messages; status data names the hook | uniter.go:895-919 (message `hook failed: %q`, data["hook"]), uniter.go:520-522 (`upgrade failed`); status.go:423-439 copies agent message and data to the workload error. The word "charm upgrade failed" is my paraphrase of a DeployConflictError during resolver loop, uniter.go:520. | T* |
| 23 | unknown after start hook with no status set | runhook.go:259-268 | T |
| 24 | unknown shown when agent not communicating, except error and terminated | domain/status/service/status.go:317-327 | T |
| 25 | terminated after remove hook finished | runhook.go:254-258 | T |
| 26 | New unit: waiting and allocating; messages `waiting for machine` (machine) and `installing agent` (Kubernetes) | domain/application/service/unit.go:989-1009; domain/application/state/unit.go:890-896; core/status/status.go:277-281 | T |
| 27 | Message becomes `agent initialising` when the agent starts | internal/worker/uniter/uniter.go:692-698 | T |
| 28 | Install: maintenance `installing charm software` unless charm already set status | runhook.go:209-217 | T |
| 29 | After start hook workload is unknown unless charm set one | runhook.go:259-268 | T |
| 30 | Kubernetes: pod status can be shown; values blocked, waiting, running | domain/status/service/status.go:477-520; pod values status.go:87-102 | T |
| 31 | Charm status shown when terminated, blocked, maintenance | status.go:492-498 | T |
| 32 | Pod blocked replaces; pod waiting and charm active replaces; pod running and charm unmodified replaces; every other case charm | status.go:500-519; unmodified = status.go:522-540 | T* caveat: "unmodified" also covers workload status `unset`, which the draft omits. A stored `unset` workload with a startup message is not reachable from the draft's other statements; the omission narrows the claim. |
| 33 | The three startup messages `waiting for container`, `installing agent`, `agent initialising` | core/status/status.go:277-281; status.go:531-535 | T |
| 34 | Agent status is set by the unit agent and Juju; a charm sets only the workload status (draft wording after revision) | status-set.go:31 and 130-135 (charm command sets only workload). "The agent sets it" for the shown values: uniter.go:158 (executing), 396 (idle), agent.go:33 (failed), context.go:1542 (rebooting), and lost is computed status.go:261-270. | T* ("agent sets it": lost and allocating are set by Juju on the agent's behalf; service.go:465-466 refuses to set them via SetUnitAgentStatus. The draft's sentence is slightly wider than the source.) |
| 35 | idle meaning | core/status/status.go:125-129; uniter.go:387-396 | T |
| 36 | executing; message names hook or task | core/status/status.go:120-123; op_callbacks.go:156-158 | T |
| 37 | allocating meaning | core/status/status.go:110-113; unit.go:997-1003 | T* (machine wording from the comment; the pod wording is inferred from the CAAS unit also getting `allocating`, state/unit.go:890) |
| 38 | rebooting set when a hook requests a reboot; returns to idle | context.go:1525-1546; core/status/status.go:115-118 | T |
| 39 | failed: operation of the agent itself failed; message names it | internal/worker/uniter/agent.go:25-37 (`reportAgentError` userMessage) | T |
| 40 | lost: not communicated for an unexpectedly long time; message text | core/status/status.go:131-134; domain/status/service/status.go:261-270 | T |
| 41 | Hook failure shown as agent idle, workload error | domain/status/service/status.go:418-439 | T |
| 42 | juju status App table Status column; Unit table Workload and Agent columns | cmd/juju/status/output_tabular.go:143-145, 267-269 | T |
| 43 | Link targets exist: unit-agent, leader-unit, hook-command-status-set, hook-install, hook-remove, hook-start | docs/reference/agent.md:31; unit.md:22; status-set.md:1; hook.md:722, 742, 761 | T |

## Upstream statements dropped for lack of a trace

| Upstream line | Statement | Reason |
|---|---|---|
| U53 | terminated is "as a consequence of juju destroy-model" | The source sets it after the remove hook (runhook.go:254-258). No path found from destroy-model. |
| U23 and figure | Transitions between application statuses, with reasons; "Active to Terminated: a command such as destroy-model" | No transition check exists in status-set (status-set.go:141-160); application terminated appears only for a removed offer (domain/status/service/crossmodelrelation.go:44-86). Not traceable as rules. |
| U31 | Notation `<workload>/<agent>` | The client prints separate columns (output_tabular.go:267-269); no source for the slash notation. |
| U41 | Semantics of charm statuses is up to the charm author | No source. |
| U65 | "or its pod/container has unexpectedly come down" for lost | Lost is computed from presence only (status.go:261-270). |
| U67 | Cannot be controlled by "a human operator" | No source either way. |
| U83-92 | Sample output with version 4.0.15 | Version does not match 4.1; the columns are in the prose instead. |

## Not drafted, not traced

- T8 (client developer: which call, request, result, error and code). The `FullStatus` facade method was not read in this run. Open gap, see change-set.md F22.
- What an operator does about `error` (resolve the hook failure). Needs a remediation traced to the resolved call; not read.
