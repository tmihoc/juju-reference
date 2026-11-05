# Trace of draft-status.md

Revision for all paths: 52e983a435. Abbreviations:
CS = core/status/status.go; DSS = domain/status/service/status.go; DSV = domain/status/service/service.go; LS = domain/status/service/leaderservice.go; SS = internal/worker/uniter/runner/jujuc/status-set.go; RH = internal/worker/uniter/operation/runhook.go; UN = internal/worker/uniter/uniter.go; AG = internal/worker/uniter/agent.go; OC = internal/worker/uniter/op_callbacks.go; CX = internal/worker/uniter/runner/context/context.go; OT = cmd/juju/status/output_tabular.go; DAU = domain/application/service/unit.go; DOC = an upstream doc statement.

| Id | Draft statement | Source (file:line) | Verdict |
|---|---|---|---|
| D1 | A unit has two statuses, workload and agent | DSS 409-451 (display and agent statuses are two values); OT 248-249 (two columns) | Verified |
| D2 | An application has one status | DSV 353-396 (one display status) | Verified |
| D3 | Each status = value, message, time set | CS 23-29 (Status, Message, Data, Since) | Verified |
| D4 | Workload status reports on the charmed software | SS 31-38 ("Sets the workload status of the charm"; "describe their current status") | Verified |
| D5 | Agent status reports on the unit agent, the process that runs the hooks | UN 387-396 (agent sets idle when no operation), OC 157-158 (executing while running an operation); DOC docs/reference/status.md:57 | Verified (the phrase "the Juju process" is a gloss on the uniter) |
| D6 | Charm sets workload status with `status-set` | SS 15-18, 31-38, 168-171 | Verified |
| D7 | Hook tool accepts maintenance, blocked, waiting, active and rejects every other value | SS 130-135 (validStatus), 145-154 (invalid status error) | Verified |
| D8 | Charm decides which value and when | SS 36-38 ("responsibility on the charm to know its status") | Verified |
| D9 | Juju sets error, unknown, terminated | error: DSS 423-438; unknown: RH 259-268 and DSS 317-327; terminated: RH 254-258 | Verified |
| D10 | Juju also sets waiting and maintenance at fixed points | DAU 997-1009; UN 693-698; RH 209-217, 218-228 | Verified |
| D11 | error row: hook failure or failed charm upgrade; needs human intervention | UN 895-919 (hook failed), UN 520-522 (upgrade failed); CS 44-48 | Verified |
| D12 | error message form `hook failed: "<hook>"` and `upgrade failed` | UN 918, UN 522; DSS 430-438 (workload message = agent message) | Verified |
| D13 | blocked: cannot continue without user input; message tells how to unblock | SS 52, 67-70; CS 162-164 | Verified |
| D14 | maintenance: not yet providing a service, doing work on itself, e.g. installing; no human intervention | CS 140-145 ("not yet providing services ... reflects activity on the unit itself"); SS 50-51, 88-91; upstream status.md:49 | Verified |
| D15 | waiting: not in error, not in service, depends on external factor, e.g. related application not running; no intervention | SS 53-56; CS 157-160 | Verified |
| D16 | active: believes it is offering all the services it is installed to provide | SS 57-58; CS 166-169 | Verified |
| D17 | active message optional; describes a degradation | SS 72-76 | Verified |
| D18 | unknown case 1: start hook finished, charm set no status in any hook so far | RH 248 (hasRunStatusSet = hook-set or state.StatusSet), 259-268; CS 152-155 | Verified (state.StatusSet semantics taken from its use at RH 212 and 248; its setter was not read) |
| D19 | unknown case 2: agent lost | DSS 317-327 (not present and not error/terminated gives unknown) | Verified |
| D20 | terminated: remove hook has finished; Juju sets it | RH 254-258 | Verified |
| D21 | Message shown to users and kept in history | SS 63-66 | Verified |
| D22 | Kubernetes: pod status can replace displayed workload status | DSS 477-520 | Verified |
| D23 | terminated, blocked, maintenance always displayed | DSS 492-498 | Verified |
| D24 | workload active/waiting/unknown and pod blocked: pod status displayed | DSS 500-504 (comment at 500 names active, waiting, unknown) | Verified |
| D25 | workload active and pod waiting: pod status displayed | DSS 506-510 | Verified |
| D26 | Juju sets the agent status | DSS 260-290, 414-439; service.go SetUnitAgentStatus DSV 449-485 | Verified |
| D27 | Hook tools set only the workload status | SS 31 (workload); the set of hook tools was not enumerated; `juju-reboot` sets agent status (D31) | Partly verified: `status-set` is the status hook tool; `juju-reboot` is a second tool with an agent-status side effect. The draft statement is false as written. See notes.md, correction C1 |
| D28 | allocating: the unit exists and its agent is not running yet | DAU 997-1003; DSS 412-416; CS 104-107 | Verified |
| D29 | idle: no operation to run, waits for events | UN 387-396; CS 119-123 | Verified |
| D30 | executing: running a hook or task; message names it | CS 114-117; OC 156-158 | Verified |
| D31 | rebooting: machine rebooting; returns to idle after; `juju-reboot` causes it | CS 109-112; CX 1530-1548 (the reboot request path sets Rebooting). The hook tool name `juju-reboot` is not in the files read | Partly verified: the tool name is Unverifiable here; reword to "A reboot request from the charm causes this status" (see C1) |
| D32 | failed: an operation of the agent failed; message says which | AG 25-37; CS 91-98 | Verified |
| D33 | lost: controller has not heard from the agent for an unexpectedly long time; controller sets it | CS 125-128; DSS 262-270 (not present gives lost); DSV 465-466 (setting lost rejected) | Verified |
| D34 | While lost, displayed workload is unknown unless error or terminated | DSS 317-327 | Verified |
| D35 | Hook failure displays workload error and agent idle; message is the failure's | DSS 418-439 | Verified |
| D36 | Life step 1: agent allocating, workload waiting; messages by model type | DAU 989-1009 (IAAS: waiting for machine; CAAS: installing agent); domain/application/state/unit.go 888-898 | Verified |
| D37 | Step 2: on agent start, waiting with creation message becomes waiting `agent initialising` | UN 683-698; CS 271-274 | Verified |
| D38 | Step 3: before install, maintenance `installing charm software` unless charm set status | RH 209-217 | Verified |
| D39 | Step 4: after start, unknown if charm set none | RH 259-268 | Verified |
| D40 | Step 5: stop hook before and after | RH 218-222, 250-253 | Verified |
| D41 | Step 6: remove hook before and after | RH 223-228, 254-258 | Verified |
| D42 | A `status-set` call replaces the workload status at any point | SS 39-41 ("applied without waiting for a hook execution to end") | Verified |
| D43 | Application: unless leader has set status, derived from units | DSV 348-351, 364-396 | Verified |
| D44 | Derived status = displayed workload status of highest-severity unit with that unit's message | DSS 574-585 (result = displayStatus, a full StatusInfo) | Verified |
| D45 | Severity order error > blocked > maintenance > waiting > active > terminated > unknown | DSS 542-552 | Verified |
| D46 | One blocked unit makes app blocked unless another unit is in error | DSS 544-552, 581; error includes agent error shown as workload error (DSS 423-438) | Verified |
| D47 | Ties: leader if among them, else lowest number | DSS 554-557, 588-606; DOC docs/releasenotes/juju_4.0.x/juju_4.0.15.md:101-103 | Verified |
| D48 | No units: derived status unknown | DSS 562-566 | Verified |
| D49 | Leader sets app status with `status-set --application` | SS 43-44, 108-114; LS 68-107 | Verified |
| D50 | A leader-set status is displayed in place of the derived one | DSV 370-372 | Verified |
| D51 | Non-leader call fails with `this unit is not the leader` | SS 116-119 (documented text); LS 103-106 (UnitNotLeader) | Verified (text as documented; the rendered text of statuserrors.UnitNotLeader was not read) |
| D52 | `juju status` Status column of app table | OT 143-145, 204 | Verified |
| D53 | Workload and Agent columns of unit table | OT 267-269, 248-249 | Verified |
| D54 | Asterisk marks leader | OT 244-246; DOC docs/reference/unit.md:33 | Verified |
| D55 | Sample output: header without SLA; Timestamp column | OT 64-75 (Model, Controller, Cloud/Region, Version, optional Timestamp, optional Notes); app columns OT 143; unit columns OT 267 | Verified for format. Cell values are illustrative; version `4.1.0` is an example value |
| D56 | Lead description sentence in html_meta | restates D1, D2, D43, D45, D52 | Verified by those rows |

## Corrections to the draft found during the trace

C1. D27 and D31. "The hook tools set only the workload status" is false as written (a reboot request sets the agent status, CX 1542). Reworded in the draft: see draft-status.md, Agent status, where the sentence now reads "Juju sets the agent status. The `status-set` hook tool sets only the workload status." and the rebooting row says "A reboot request from the charm causes this status."

## Dropped from upstream (no source support)

- `<workload status>/<agent status>` as the usual expression, and the `unknown/lost` example as an expression: no 4.1 output prints this form (OT 248-249 prints two columns; output_oneline.go 38-42 prints `agent:<s>, workload:<s>`). The pair `unknown` and `lost` itself is real (DSS 317-327).
- "terminated ... as a consequence of `juju destroy-model`": no source read ties destroy-model to the status; the remove hook does (RH 254-258).
- New unit "starts in `maintenance/allocating`": False (DAU 1001-1008 gives `waiting/allocating`).
- "install hook returns, no workload status, unknown/idle": False (the start hook sets `unknown`, RH 259-268).
- "the user should set active": the charm sets it (SS 36-38).
