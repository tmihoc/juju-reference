# Gricean end-to-end review wave — session 96 (queue item 20)

Read-only scout agents, one page each, waves of 2-3; prompt base
`experiments/e48/grice-review-prompt.md`. Findings below are the agents'
output. Every row must be verified against the 4.1 code in
`/tmp/juju-41-tree` before any fix is applied; rejects are recorded here
with evidence. Nothing speculative while unattended.

Wave 1 (session 96): application.md, relation.md, unit.md — the two
session-95 commits (the application.md five-section schema restructure;
the hook-commands rename + name-linking) never Grice-read after their
change, plus unit.md as a sample of the session-94 sweep.

## unit.md — GriceUnit (completed)

Special-focus checks (session-95 changes): PASS. No "hook tools" wording;
every specific hook/hook-command name links to an existing anchor
(`config-changed` → `hook-config-changed` hook.md:700, `stop` →
`hook-stop` hook.md:789, `remove` → `hook-remove` hook.md:742,
`status-set`, `state-set`, `unit-get` → the list-of-hook-commands pages);
`leader-elected` / `leader-deposed` (unit.md:94) stay plain code font
(no sections on hook.md). Schema figure vs DDL: 16 boxes, edges match
`model.ddl` FKs (`k8s_pod` 3133-3143, `k8s_pod_status` joined to Unit
3214-3222, `k8s_pod_port` → `k8s_pod` 3146-3154, Principal double join
3047-3056), alt-text row orders match the view's positions block.

Findings (most serious first; NOT yet verified against the code):

| Line | Maxim | Label | Problem | Evidence | Replacement |
|---|---|---|---|---|---|
| 213 | Quality | UNTRACED | Removal-job actions (revokes leadership, deletes owned secrets, deletes controller node for a controller-application unit) not traced to the removal job | searched `/tmp/juju-41-tree/domain/removal/`, no direct hit | Re-trace against `domain/removal` before the fix commit; cite or drop |
| 214 | Quality | UNTRACED | Deletion-cascade list (tasks, annotations, pod, ports, status, secret consumer records) not traced record by record | `domain/removal/state/model/unit.go` not read exhaustively | Trace each to the cascade; keep only what the code deletes |
| 31 | Relation | MISPLACED (redundant) | "A `dying` unit never becomes `alive`. A `dead` unit never becomes `dying`." restates the preceding sentence; all three come from the one trigger `NEW.life_id < OLD.life_id` | model.ddl:6838-6844 (`trg_unit_guard_life`) | Keep only: "A unit's life never moves backward." |
| 60 | Quality | UNTRACED | "A unit with no marker has the mode `none`" — DDL knows only `retry-hooks`/`no-hooks`; `none` must be an application default in `UniterAPI.Resolved`, not traced | model.ddl:3341-3343; uniter.go:508 not read | Trace `Resolved`'s no-row answer; reword if not `none` |
| 357 | Quality | UNTRACED | Relation state items replace-all + keep-only-existing not traced to `domain/unitstate` | no hit found this pass | Trace in `domain/unitstate/state`; move to the call only if the code keeps it |

## application.md — GriceApplication (completed)

Special-focus checks (the five-section schema restructure + the
hook-commands rename): PASS. The five `###` groups match the five
figure views; the intro's group list matches; every tested schema rule
has DDL enforcement (unique name `idx_application_name`, life trigger,
config-key/type/status/OS/architecture/hash lookups). No "hook tools"
wording; every hook/hook-command link resolves. Caveat (agent): judged
against DDL and facade coverage, not a parent-revision diff.

Findings and session-96 dispositions (each verified before disposition):

| Line | Maxim | Label | Problem | Disposition |
|---|---|---|---|---|
| 211 | Quality | FALSE | Deploy base fallback order reversed on the page | APPLIED: request → placement machines → model `default-base` (code-verified: deployrepository.go:879-881, :870-871) |
| 100-103 | Quantity | MISSING | `device_constraint_attribute` drawn in the view, no bullet | APPLIED: record bullet added |
| 165 | Relation | MISPLACED | Provisioner-mark removal rule duplicates line 453 | RECORDED, not applied (time) |
| 87 | Relation | MISPLACED | Config-hash comparison duplicates change-streams bullet (187) | RECORDED, not applied |
| 65 | Relation | MISPLACED | Password-setting worker behavior duplicated (192) | RECORDED, not applied |
| 50 | Relation | MISPLACED | `unset` derivation duplicated at 482 | RECORDED, not applied |
| 148 | Relation | MISPLACED | Machine-cloud scale absence duplicated (225) + life-stage absence | RECORDED, not applied |
| 45 | Relation | MISPLACED | Channel local-charm absence is a deploy effect, not DB-enforced | RECORDED, not applied (its replacement moves a sentence into the Deploying rules) |

The two applied rows are one commit (`docs(reference): fix the deploy
base fallback order and add the device attribute record`), checker at
baseline, counts 956/674/204/182, dirhtml clean. The six recorded rows
are simple deletions with the agent's exact wording — verify each pair
by reading both lines, then apply as one commit in the attended
session.

## relation.md — GriceRelation (completed)

Special-focus checks (session-95 changes): PASS. All hook-command links
resolve (`relation-get`, `relation-set`, `relation-ids`, `relation-list`,
`relation-model-get` → the list-of-hook-commands pages; `relation-joined`
hook.md:370, `relation-departed` hook.md:316). No hook name without a page
appears. Schema figure vs `model.ddl`: 8 boxes, every cardinality and rule
DB-enforced (PKs, unique indexes, check constraints, triggers; the agent
cites lines, spot-verified).

Findings and session-96 dispositions (each row re-verified against the
files before disposition):

| Line | Maxim | Label | Problem | Disposition |
|---|---|---|---|---|
| 323 | Manner | MISSING | `relation-broken` in plain code font though the anchor exists (hook.md:235) — the session-95 rename commit missed it | APPLIED: linked to `hook-relation-broken` |
| 41 | Relation | MISPLACED | Key-order sentence duplicates line 32 (Identification) | APPLIED: sentence deleted |
| 93 | Relation | MISPLACED | Offer pointer duplicates line 50 (cross-model bullet) | APPLIED: sentence deleted from the calls intro |
| 27/38 | Relation | MISPLACED | "The endpoints decide its kind" stated twice (schema intro + Endpoint bullet lead-in) | RECORDED, not applied: the proposed replacement rewrites the schema intro; wording decision for the attended session |
| 229-230 | Manner | MISSING | Figure caption/alt name `relation-changed` in plain text | RECORDED, not applied: needs a check whether `:caption:` accepts a `{ref}`; alt text cannot carry a link |

The three applied rows are one commit (verified: checker identical to
HEAD baseline, counts 956/674/204/182, dirhtml build clean). Other
traced-claim spot-checks by the agent passed (status transitions
`domain/status/status.go:186-211`, status IDs 0-5 `model.ddl:4353-4360`,
`suspending`→`suspended` message retention, error prefixes).

## Disposition

- The verified relation.md rows (323, 41, 93) landed as one commit this
  session (see9f159dc4's successor; checker/counts/build verified); the
  two wording-level rows stay above for the attended session.
- unit.md rows are all UNTRACED-verification work: queued for the
  attended session (removal-job actions, deletion cascade, resolved-mode
  `none`, unit-state replace rules); row 31 is a wording decision.
- application.md (GriceApplication) was still running at close-out;
  its findings arrive next session — read `history://GriceApplication`.
- The session-85 e48 rerun folds into this wave for these three pages.