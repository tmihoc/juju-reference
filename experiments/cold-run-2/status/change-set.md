# Findings and change set: docs/reference/status.md at e5db99d585

Page audience (Q1 not answered, so this is my instantiation): operator reading `juju status` (T6, T2, T3, T10); charm author setting statuses (T1, T2); AI reader of one retrieved section; reader who takes statements literally. Each finding names the addressee it was judged against.

Upstream line numbers are from `git show e5db99d585:docs/reference/status.md`. Source references use the 4.1 tree at e5db99d585; full trace in trace.md.

## Findings

| # | Where | Quoted | Type | Evidence | Fix | Sev | Conf | Addressee |
|---|---|---|---|---|---|---|---|---|
| F1 | L10 | "the former can be inferred from the latter" | Ambiguous; Not enough | Application status is inferred from units only when the charm has set none: domain/status/service/service.go:370-395 | Rewrite lede: one application status, two unit statuses; state when it is derived. Home: lede + Application status | medium | determined | operator, literal reader |
| F2 | L10 | "This document gives more information about all of these different kinds of status" | Metalanguage | contract Manner row | Delete | low (batch) | determined | AI reader |
| F3 | L19 | "highest-priority status of the workload statuses" | Not enough (T10); Relies on implicature | Order is error, blocked, maintenance, waiting, active, terminated, unknown: domain/status/service/status.go:544-552; ties and no-units rules 558-606 | Add the order, the tie rule, the no-units case, and the message. Home: Application status | high: the operator cannot predict the shown status when units differ | determined | operator |
| F4 | L19 | "if even just one workload is blocked, the application will also be marked blocked" | False when any unit is in `error`; Relies on implicature | status.go:544-552 (error 100 > blocked 90) | Correct with "when no unit is in error" | medium | determined | operator |
| F5 | L19 | "can be specified by the charm author" | Not enough | Only the leader, via `status-set --application`: status-set.go:43-44 | State who and how; link the hook command. Home: Application status | medium | determined | charm author |
| F6 | L21-23 | figure `status.png`, alt "application_status" | Figure-only fact; Prose defers; Contradicts; Uninformative alt text | Facts only in the figure: the five states and 11 transitions with reasons. Terminated labelled "The Application is being destroyed" and reached by "A command, such as destroy-model": no path in source; application `terminated` appears only for a removed offer (crossmodelrelation.go:44-86); unit `terminated` follows the remove hook (runhook.go:254-258). Transitions are not enforced: status-set accepts any of four at any time (status-set.go:141-160). The figure omits `error` and `unknown`, the two statuses Juju sets most visibly. Alt text is a file name. | Delete the figure. State in prose: any of four at any time; terminated meaning; error and unknown. Do not restore the transitions as rules (Unverifiable) | high: a reader believes destroy-model produces `terminated` and that the shown transitions are the rules | determined | operator, charm author, screen reader |
| F7 | L21 | "The following figure provides an illustration ... and lists the reasons for the transitions" | Metalanguage; Prose defers | contract Figure table | Delete with the figure | medium | determined | screen reader, AI |
| F8 | L31 | "usually expressed as `<workload status>/<agent status>`, e.g. , `active/idle` or `unknown/lost`" | Unverifiable | Client prints separate columns: cmd/juju/status/output_tabular.go:267-269 | Delete; state that a client shows two values | low | determined | operator |
| F9 | L41 | "which are set by Juju, the workload status is generally speaking set by the charm" | (true) with Metalanguage "listed below" and Ambiguous "semantics ... up to the charm author" | status-set.go:130-135 | Keep the who-sets fact as a column; delete the semantics sentence (Unverifiable) | low | determined | charm author |
| F10 | L47 | "`error` ... The unit is in error, likely from a hook failure." | Not enough | Hook failure, or upgrade failure; the message; the agent's error is shown as workload `error` with the agent `idle`: status.go:418-439; uniter.go:520-522, 918-919 | Add trigger, message, and the agent-side presentation | medium | determined | operator |
| F11 | L50 | "waiting for another charm it's integrated with to be ready" | Ambiguous (narrower than source); Gap | Source: "an external factor, e.g. an application to which it is related": status-set.go:53-56. Juju also sets `waiting` on every new unit: unit.go:997-1009 | Widen to the source wording; add the new-unit case | low | determined | charm author |
| F12 | L52 | "`unknown` ... may be still setting up, or something might have gone wrong" | Not enough; Ambiguous | Two exact triggers: start hook finished with no status set (runhook.go:259-268); agent not communicating (status.go:317-327) | Replace with the two triggers | medium | determined | operator |
| F13 | L53 | "`terminated` ... being destroyed, e.g. as a consequence of `juju destroy-model`" | False / Unverifiable | runhook.go:254-258: set after the remove hook has finished | Correct | medium | determined | operator |
| F14 | L61 | "`allocating` | The charm pod has not come up yet." | Not enough | Same status for machine units: unit.go:989-1009 | Cover machine and pod | medium | determined | operator on machines |
| F15 | L64 | "`error` | The Juju agent ... has run but has encountered an uncaught charm exception." | False as displayed | Agent error is shown as `idle` and the workload is `error`: status.go:418-439 | Replace with the displayed presentation, remove the agent `error` row | high: an operator or script looking for agent `error` never finds it | determined | operator, tool author |
| F16 | L65 | "`lost` ... or its pod/container has unexpectedly come down" | Unverifiable; Not enough | Lost is computed from presence, status.go:261-270; the workload then reads `unknown` with a message (317-327) | State the presence trigger and the paired workload | medium | determined | operator |
| F17 | L59-65 | the agent table as a complete list | Gap; Relies on implicature (list read as complete) | `failed` (agent.go:25-37) and `rebooting` (context.go:1525-1546) are shown statuses | Add both | medium | determined | operator, literal reader |
| F18 | L67 | "cannot be directly controlled by the charm or a human operator" | Unverifiable (human operator) | status-set.go:31, 130-135 cover the charm only | Keep only the charm part | low (batch) | determined | operator |
| F19 | L71 | "Each newly deployed unit starts in `maintenance/allocating`" | False | New unit is `waiting` with agent `allocating`: unit.go:997-1009; state/unit.go:890-896. `maintenance` first appears when the install hook starts: runhook.go:209-217 | Replace with the startup sequence in Workload status of a new unit | high: operator and charm author mis-predict the first statuses | determined | operator, charm author |
| F20 | L71 | "If, by the time the install hook ... returns, the charm has set no workload status, the unit will go to `unknown/idle`" | False | The check is after the start hook: runhook.go:259-268 | Correct | high: a charm author sets status at the wrong hook | determined | charm author |
| F21 | L71 | "the user should set active" | Ambiguous | The charm sets it, not the user | Reword (draft drops the advice because it is a recommendation without a source) | low | determined | charm author |
| F22 | page | (absent) | Gap | (a) Kubernetes pod status can replace the workload status: status.go:477-540. (b) Which statuses a charm can set and in what order (T2): status-set.go:130-161. (c) T8: the status call, fields, and errors; FullStatus facade not read in this run. (d) T3: what an operator does about `error`; resolution call not read. | Add (a) and (b) to the draft. (c) and (d) stay open | medium | (a),(b) determined; (c),(d) open(Q1) | operator on Kubernetes, client developer |
| F23 | L12 | "## Types of status" | Uninformative title | First sentence of its section carries more distinct subject terms | Delete the heading; promote the three subsections | low (batch) | determined | browser reader |
| F24 | L17 | "As its name indicates, the application status reports on the status of each deployed application." | Excess | removing it leaves no question unanswered | Delete | low (batch) | determined | AI |
| F25 | L77 | "as we said" ; "`Application > Status`" | Metalanguage; Ambiguous notation | output_tabular.go:143-145, 267-269 | Name the table and column | low (batch) | determined | operator |
| F26 | L75-92 | section "Status in the output of `juju status`" | Misplaced (R24: CLI first) | Platform fact is the unit-statuses-as-two-values; the CLI is an example | Keep, rewrite as "Status in client output" with the CLI as example | low (batch) | determined by R24 | AI, tool author |
| F27 | L79-92 | sample output, version `4.0.15` | Unverifiable; Excess | Version and timestamps not traceable to 4.1; the prose states the columns | Delete | low (batch) | determined by the maxim test, but a person in a browser may benefit; judgment | browser reader |
| F28 | L10-98 | whole page | Boundary: no finding | Source owner core/status and domain/status (one); audience question (operator reading, charm author setting): two, related; change coupling and reading path not measured (only the allowed git commands were used). Fewer than two measures agree | None. The boundary is a tie | - | tie | - |
| F29 | L45-53 | meanings of the four charm-settable statuses | Duplicate (against the `status-set` help, which also lists the four and links here) | status-set.go:49-58 | Open: which of the two owns the meanings (R16). I keep them here and leave the help text alone | low | open(Q5-like, owner of a fact shared by a hook command and a status page) | charm author |

Batch line for low findings: F2, F8, F9, F11, F18, F21, F23, F24, F25, F26, F27.

## Change set

Format: action | file and section | category | requirement | finding | confidence.

| # | Action | Home | Category | Requirement | Finding | Conf |
|---|---|---|---|---|---|---|
| C1 | Rewrite lede: statuses, multiplicity | status.md lede | Reference | R6, R18 | F1 | determined |
| C2 | Add severity order, tie rule, message, no-units, leader sets | Application status | Reference | R7, T10 | F3, F4, F5 | determined |
| C3 | Delete figure and its two prose sentences; state facts in prose | Application status; Workload status | Reference | R26, figure rule | F6, F7 | determined |
| C4 | Workload table: add "Set by" column, correct meanings for error, unknown, terminated, waiting | Workload status | Reference | R7, Quality | F9-F13 | determined |
| C5 | Replace the "newly deployed" note with a section on the startup sequence | Workload status of a new unit | Reference | Quality | F19, F20 | determined |
| C6 | Add Kubernetes pod override | Workload status of a Kubernetes unit | Reference | R6, R7 | F22a | determined |
| C7 | Agent table: remove `error`, add `failed`, `rebooting`, fix `allocating` and `lost`; add presentation of hook failure | Agent status | Reference | Quality | F14-F18 | determined |
| C8 | Delete the notation note, the "Types of status" heading, the tautology sentence, the sample output, the metalanguage | various | Reference | Manner | F2, F8, F21, F23-F27 | determined |
| C9 | Keep anchors `status`, `application-status`, `unit-status`, `workload--charm-status`; add `status-in-output` | whole page | Reference | R15 | - | determined |
| C10 | Note upgrade? No release-notes entry proposed: no behavior changed, the page was wrong | - | - | R23 | - | tie |

## Unchanged

- Anchors listed in C9: kept (R15).
- The `ibnote` pointer to `command-juju-status`: kept.
- `juju status` column names: kept, checked against output_tabular.go.
