# Findings and change set: docs/reference/status.md at 52e983a435

Addressees: O = operator reading `juju status` (browser); A = charm author; L = literal reader (includes non-native readers); AI = AI reading one retrieved section. Source paths are at 52e983a435; abbreviations as in trace.md. Ledger rows cited from rule-derivation.md by name (Fig = figures ledger, Text = text ledger, Str = structure ledger). Page line numbers are those of upstream `status.md`.

## Findings

| # | Where | Quoted | Type | Evidence | Fix | Sev | Conf | Addressee |
|---|---|---|---|---|---|---|---|---|
| F1 | 10 | "application ... can be inferred from the latter" | Conditional truth stated flat | DSV 370-372: a leader-set status replaces the derived one | Rewrite: derived unless the leader set it; home Application status | high | determined | O, A |
| F2 | 19 | "if even just one workload is blocked, the application will also be marked blocked" | Conditional truth stated flat | DSS 544-552: `error` (100) outranks `blocked` (90); a leader-set status wins (DSV 370-372) | State the order and the exception | high | determined | O |
| F3 | 19 | "highest-priority status" | Not enough (T10) | Order is in DSS 542-552 and stated nowhere in the docs set | Add the seven-step order as an ordered list | high | determined | O, L |
| F4 | 19 | (silence on ties, no units, which unit's message) | Gap (T10) | DSS 554-606; release note juju_4.0.15.md:101-103 | Add tie rule and no-unit case | medium | determined | O |
| F5 | 19 | "can be specified by the charm author" | Not enough (T1: who may, how) | LS 68-107; SS 43-44, 116-119: only the leader, via `status-set --application`; others get an error | Add who, how, and the error | medium | determined | A |
| F6 | 21-23 | figure "application_status" with arrows | Contradicts | The figure shows `terminated` as "The Application is being destroyed" reached by "a command, such as destroy-model"; no source maps this to an application (application `terminated` is only a derived unit status, severity 50, DSS 550). Arrows such as active to waiting "related Application can't be reached" are not enforced anywhere: `status-set` accepts any of four values from any state (SS 130-154). `error` and `unknown` are missing | Delete figure and image; state the facts in prose (Fig: "A transitions figure only if each arrow is an enforced rule") | high | determined | O, A |
| F7 | 21 | "lists the reasons for the transitions" | Prose defers + Figure-only fact | The reasons exist only in the figure (alt text is the file name) | Delete with the figure; the enforced Juju-set transitions are restated in the lifecycle list | high | determined | AI, screen reader |
| F8 | 21 | "The following figure provides an illustration" | Metalanguage | Contract table | Delete | low | determined | all |
| F9 | 23 | `![application_status](status.png)` | Role swap / alt text carries no inventory | The alt text is the file name | Delete with the figure | medium | determined | screen reader |
| F10 | 31 | "usually expressed as `<workload status>/<agent status>`, e.g. `active/idle` or `unknown/lost`" | Unverifiable | OT 248-249 prints two columns; output_oneline.go 38-42 prints `agent:<s>, workload:<s>`; no 4.1 output prints `a/b` | Delete; the two-value structure is stated in the lede | medium | determined | O |
| F11 | 41 | "Except for `error`, `terminated` and `unknown`, which are set by Juju, the workload status is generally speaking set by the charm" | Relies on implicature | Charm can set exactly four values (SS 130-135) and Juju also sets `waiting` and `maintenance` itself (DAU 1004-1008, UN 695, RH 213-216) | State the four accepted values and where Juju sets the others | medium | determined | A, L |
| F12 | 41 | "generally speaking ... ultimately up to the charm author ... ideal case" | Ambiguous | | State that the charm decides the value; give meanings as the convention in the hook tool's doc (SS 49-58) | low | determined | L |
| F13 | 47 | `error`: "The unit is in error, likely from a hook failure." | Not enough (T3) | UN 895-919, 520-522: hook failure or failed upgrade; message form `hook failed: "<hook>"` | Name both causes and the message | medium | determined | O |
| F14 | 52 | `unknown`: "It may be still setting up, or something might have gone wrong." | Ambiguous | RH 259-268 (start hook done, no status set) and DSS 317-327 (agent lost) | Name the two causes | high | determined | O |
| F15 | 50 | `waiting`: "waiting for another charm it's integrated with" | Not enough | CS 157-160, SS 53-56: "an external factor", example a related application; creation messages are `waiting` too (DAU 1004-1008) | Widen to the source meaning | medium | determined | O |
| F16 | 53 | `terminated`: "The workload is being destroyed, e.g. as a consequence of `juju destroy-model`" | False / Unverifiable | RH 254-258: set after the remove hook has finished, so the workload is gone; destroy-model link is untraced | Restate as "remove hook finished" | medium | determined | O |
| F17 | 61 | `allocating`: "The charm pod has not come up yet." | Not enough / Scope | DAU 989-1009 sets it in machine and Kubernetes models; CS 104-107 says the machine is being spun up | Remove pod wording; state both cases | medium | determined | O |
| F18 | 62, 63, 64 | "in the charm container" (idle, executing, error) | False for machine models | The agent runs on a machine in machine models | Delete "in the charm container" | medium | determined | O |
| F19 | 64 | agent `error`: "has run but has encountered an uncaught charm exception" | Stored but never shown | DSS 418-439: agent `error` is displayed as agent `idle` plus workload `error` | Remove the row; state the display in one sentence in Agent status and in the workload `error` row | high | determined | O |
| F20 | 59-65 | (agent table) | Gap | `rebooting` (CX 1542) and `failed` (AG 33) are agent statuses a unit can show | Add both rows | medium | determined | O |
| F21 | 65 | `lost`: "unresponsive, or its pod/container has unexpectedly come down" | Mirrors implementation / Not enough | DSS 262-270: derived from agent presence; effect on workload (DSS 317-327) is unstated | Restate; add the effect on the displayed workload status | medium | determined | O |
| F22 | 67 | "determined and set by the Juju agent, so it cannot be directly controlled by the charm or a human operator" | Conditional truth stated flat | `lost` is set by the controller from presence (DSS 262-270); a reboot request from the charm sets `rebooting` (CX 1542) | Say Juju sets it; name the two exceptions in their rows | low | determined | A |
| F23 | 71 | "starts in `maintenance/allocating`" | False | DAU 1001-1008: `waiting/allocating` with message `waiting for machine` or `installing agent` | Replace by the lifecycle list | high | determined | O |
| F24 | 71 | "by the time the install hook (if any) returns, ... no workload status, the unit will go to `unknown/idle`" | False | RH 259-268: `unknown` is set after the start hook | Replace | high | determined | O, A |
| F25 | 71 | "the user should set active" | False | The charm sets it (SS 36-38) | Replace | low | determined | A |
| F26 | 71 | "quickly going to `maintenance/executing`" | Unverifiable | `maintenance` is set before install (RH 213-216) and `executing` while a hook runs (OC 158); "quickly" is unmeasured | Replace by the list | low | determined | O |
| F27 | 69-73 | note block holding the only statement of the creation sequence | Misplaced (T2, T5) | The sequence answers "which follow which" and belongs under a heading, with the stop and remove steps | Move into a section titled for the unit's life | medium | determined | O |
| F28 | 75, 77 | "`Application > Status`" and "`Unit > Workload, Agent`" | Ambiguous | OT 143-145, 267-269: tables headed `App` and `Unit` with columns `Status`, `Workload`, `Agent` | Name the tables and columns | low | determined | O |
| F29 | 77 | "consisting, as we said, of..." | Metalanguage | | Delete | low | determined | all |
| F30 | 82-83 | sample header `SLA` column | Stale sample | OT 64-75: header is Model, Controller, Cloud/Region, Version, then optional Timestamp and Notes; no SLA | Remove the column | medium | determined | O |
| F31 | 8, 4 | title "Status", description "status transition diagrams" | Scope claim exceeds content | The page covers application and unit status; the source lists status for machines, models, relations, storage, volumes (CS 14-16, 192-225); no figure of transitions after F6 | Retitle "Application and unit status"; fix description; keep anchor `(status)=` | medium | determined | O, AI |
| F32 | 10 | "In Juju, **status** can describe the status of an application or a unit" | Not enough (T1) | Same as F31: the other entities with status are not named | Open(Q1): which page owns machine, model, relation, and storage status values; none exists in docs (grep of docs found no value list) | medium | open(Q1) | O |
| F33 | 30-32 | note block "A unit's status is usually expressed..." | Excess | Removing it (after F10) leaves no question unanswered | Delete | low | determined | O |
| F34 | 12 | heading "Types of status" | Uninformative title | Replace by first sentence test: "the application status reports ..." carries subject terms | Replace by "Unit status" and "Application status" as top sections | low | determined | AI |
| F35 | 34-37 | headings `Workload / charm status`, `Agent status` | Mixed section? | Tie | Keep `Workload status`, `Agent status` (anchors kept) | low | tie | all |
| F36 | 15-23, 25-73 | application section before the unit sections, though the application status derives from unit workload statuses | Crossed wire (depends on another section's facts to be read) | DSS 574-585 | Move Application status after Unit status | medium | determined | AI |
| F37 | 96-98 | `ibnote` "See more: `command-juju-status`" | Duplicate? | Pointer is correct and the command page owns options | Keep | low | tie | O |
| F38 | (absent) | Hook-tool side: which values a charm may set and what a non-leader gets | Gap (T1 "who may", T3) | SS 130-154, 116-119 | Add in Workload status and Application status | medium | determined | A |
| F39 | (absent) | Kubernetes pod status overriding the charm's workload status | Gap (T6) | DSS 477-520 | Add one paragraph in Workload status | medium | determined | O (Kubernetes) |
| F40 | (absent) | Behavior of `error` on an agent upgrade conflict | Gap | UN 520-522 | Included in the `error` row | low | determined | O |

Batch line (low severity, one per page): F8, F12, F25, F26, F28, F29, F33, F34.

Not a finding: the application anchors `application-status` (page 14), `unit-status` (25, linked from docs/howto/manage-units.md:111), `workload--charm-status` (34) have inbound links or may have external ones (R15 in the contract); all three stay. `(status)=` has inbound links from docs/reference/index.md:98 and docs/tutorial/index.md:184.

## Change set

| Action | Home | Category | Requirement | Finding | Confidence |
|---|---|---|---|---|---|
| Retitle page and description | page head | Reference | Scope claim | F31 | determined |
| Replace "Types of status" by two top sections ("Unit status", "Application status"), unit first | page | Reference | Relation, Manner | F34, F36 | judged |
| Delete figure and image `status.png` | page | Reference | Fig: transitions figure only if enforced; Fig: figure never carries a fact the prose lacks | F6-F9 | determined |
| Rewrite workload table: causes, who sets, accepted values | Workload status | Reference | Quantity, Quality | F11-F16 | determined |
| Add Kubernetes pod paragraph | Workload status | Reference | Quantity | F39 | determined |
| Rewrite agent table: remove `error`, add `rebooting` and `failed`, drop "charm container", fix `lost`, `allocating` | Agent status | Reference | Quality | F17-F22 | determined |
| Replace the new-unit note by the lifecycle ordered list | Unit life subsection | Reference (T2, T5) | Quality | F23-F27 | determined |
| Write Application status: derived default, severity list, ties, no units, leader set | Application status | Reference (T10) | Quantity | F1-F5, F38 | determined |
| Rewrite `juju status` section: name tables and columns; fix sample | `juju status` section | Reference (T6) | Quality | F28-F30 | determined |
| Delete `<workload>/<agent>` note | page | | Unverifiable | F10, F33 | determined |
| Keep anchors `status`, `unit-status`, `application-status`, `workload--charm-status` | page | | R15 | (not a finding) | determined |
| Machine, model, relation, storage status | none yet | | Gap | F32 | open(Q1) |
