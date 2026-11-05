# Cross-family stress test for the content-planning algorithm — session 119

**Status:** planning stress test, not a documentation edit or rollout approval.
This applies `work/content-planning-algorithm-119.md` outside the calibrated
`model` entity case. It uses existing session-117/119 artifacts, not new source
inspection. The denied `HookCommandPages` scope remains a gap and is not worked
around.

## 1. Question and verdict

**Question:** Can the algorithm generate useful page-boundary and internal-section
plans for unlike reference families, while preserving the useful results of the
old `database schema → change streams → calls` form for errors and diagrams?

**Verdict:** bounded pass. The algorithm gives usable first-pass plans for a
tool/interface, process, shared mechanism, provider intersection and generated
CLI command. The hook/action command case is only a family-level/partial pass
because individual command derivations are blocked by the prior 402 denial.

The old `database schema → change streams → calls` form should be preserved as a
**conditional entity form**, not as the universal skeleton. Its useful result was
not the exact headings; it was the separation of:

- structural contracts that diagrams can visualize;
- change/notification contracts that stream diagrams can visualize;
- interactions where caller/rules/errors naturally live.

The new algorithm keeps that room by assigning diagrams and errors to the
contract kind:

- entity/relationship diagrams attach to records, participants and invariants;
- sequence/state diagrams attach to processes, streams and tool flows;
- errors attach to the call, phase, selector or validation step that raises or
  returns them.

## 2. Case plans

### Case A — `juju-db-repl`: tool/interface

```text
Subject: juju-db-repl
Reader-needed contract: a privileged local tool selects controller/model databases and executes SQL/dot commands, including mutable SQL.
Supported surface: jujuagentd db-repl command and REPL implementation; current docs page; E64 synthetic schema exercise for `.switch` ambiguity.
Classification: tool/interface, with links to database and model identity.
Owner/address: `juju-db-repl` page; selection/navigation section owns `.switch`/`.open`; `model` owns qualified identity.
Action: update/investigate tool contract when edits are allowed; do not move model identity into the tool page.
Sections needed: purpose/access warning; host prerequisites; initial namespace and navigation; input/dot commands/SQL execution; result/error scope; links to database/model/backup.
Source checks needed: real worker/database behavior for duplicate model names if available; HA/topology access claims; SQL transaction/mutation guarantees.
Links needed: `database`, `model` identity, DB inspection facets, backup/restore warnings.
Unresolved ties: whether ambiguity is documentation warning, source defect, or both.
Do-not-claim limits: no live REPL/controller duplicate-name result; no deterministic row selection without evidence; DB REPL is not read-only.
```

**Boundary result:** A66 keeps the selector rule with the interface and target
identity with `model`. It does not collapse `.switch model-<name>` into the
model's qualified-name invariant. This matches E64.

**Diagram/error room:** no database schema heading needed. A small flow diagram
could show helper/agent/REPL/database selection. Errors belong with entry,
selection and SQL execution steps.

### Case B — `model-migration`: process

```text
Subject: model migration
Reader-needed contract: moving one existing model from a source controller to a target controller through guarded phases.
Supported surface: migration initiation API/CLI, migration worker phases, import/export records and migration status/errors from existing artifacts.
Classification: process.
Owner/address: `model-migration` page owns phases; `model` page owns initiating call and links.
Action: keep/create process page; model page should not own full migration process.
Sections needed: participants; initiation/prechecks; quiescence/transfer/import/activation/adoption/reap phases; observations/status; abort/failure/recovery limits; links to model, controller, credential, external-controller, image metadata, object-store and log.
Source checks needed: exact phase order/worker paths, access restrictions during import/export, retry/cleanup boundaries, all provider/resource outcomes.
Links needed: `model`, `controller`, `external-controller`, `credential`, `agent-version`, `log`, `object-store`, `database`.
Unresolved ties: none on page-vs-section at current evidence; process span supports its own address. Exact subsections still need source verification.
Do-not-claim limits: request acceptance is not migration completion; target import success and source cleanup have separate failure modes; no live migration was run.
```

**Boundary result:** A66 treats migration as a process character/mechanism, not a
leg of `model`. The model character participates but does not own the phase
contract.

**Diagram/error room:** old `calls` form is insufficient; process state/sequence
diagrams are the natural diagram home. Errors belong to initiation, precheck,
transfer/import, agent reporting, abort and cleanup phases.

### Case C — model command blocks: shared mechanism / model leg

```text
Subject: model command blocks
Reader-needed contract: model-scoped block switches refuse selected operations independently of user access.
Supported surface: disable/enable/list commands, block facade, common checker and representative affected calls from `work/model-command-blocks-113.md`; generated command outlines for `disable-command`, `enable-command`, `disabled-commands`, `enable-destroy-controller`.
Classification: model leg with shared mechanism address.
Owner/address: candidate `[model command blocks]` semantic address under `model` unless cross-subject span later justifies a standalone mechanism page.
Action: update/link when edits allowed; trace per-call applicability before universal statements.
Sections needed: definition/scope; block kinds and precedence; switching/listing operations; affected call links; errors/messages; limits.
Source checks needed: every operation claimed to check blocks; exact block precedence; controller-wide `enable-destroy-controller` effects and partial iteration behavior.
Links needed: model, user/access, model operations, generated block command pages, controller destroy where applicable.
Unresolved ties: section under `model` versus standalone block-command page if maintenance/address metrics later favor a page.
Do-not-claim limits: not authorization; not every call checks it; no claim that state cannot change before later errors unless traced.
```

**Boundary result:** This is the clearest character-versus-leg test. The block
belongs to a model enough to be a model leg, but its reuse across calls needs a
shared address. A66 can express both without forcing a new page.

**Diagram/error room:** a small guard/precondition table or flow fits here better
than an ERD. Errors belong at block-setting/listing calls and each affected
operation's local call section.

### Case D — `lxd`: provider intersection

```text
Subject: LXD supported-cloud page
Reader-needed contract: how generic cloud/credential/model/machine/network/storage contracts are qualified for the LXD provider.
Supported surface: provider schema/finalization, credential finalization, placement/virt-type/profile/network and storage provider traces summarized in `skeleton-cloud-machines-117.md`.
Classification: provider intersection.
Owner/address: `cloud/list-of-supported-clouds/lxd` page; generic behavior remains with `cloud`, `credential`, `machine`, `constraint`, `placement-directive`, `space`, `subnet`, `storage`.
Action: provider page plan; link generic owners and state only LXD-conditioned intersections.
Sections needed: local/remote cloud definition; credential enrollment versus runtime certificate credential; placement/cluster member/virt-type constraints; profile/network behavior; LXD storage provider/pool limits; unresolved version/host caveats.
Source checks needed: local credential discovery/access prerequisites; image source priority; project lifecycle; forwarding/network backend; storage-driver list including `ceph` discrepancy.
Links needed: cloud, credential, machine, placement, constraint, image metadata, network/space/subnet, storage.
Unresolved ties: repeated machine-cloud fragment versus provider-specific prose; current evidence favors provider page with generic links, not generic duplication.
Do-not-claim limits: provider schema/checks are not live host/cloud success; LXD host behavior and external state are conditional.
```

**Boundary result:** A66 prevents provider pages from becoming forks of generic
cloud/machine/storage docs. They are intersections: what changes when the generic
contract is LXD.

**Diagram/error room:** provider pages may need small decision/flow diagrams for
credential finalization or placement/storage selection, not generic database
schema diagrams. Errors belong to provider-specific validation, precheck and
operation paths.

### Case E — generated CLI command: `add-model`

```text
Subject: `juju add-model` generated command page
Reader-needed contract: one CLI invocation creates a model request and local client selection effects under specific inputs/conditions.
Supported surface: generated CLI help plus source-derived command outline in `skeleton-commands-ad-117.md:25-27`.
Classification: generated command / tool invocation.
Owner/address: generated `juju-cli/list-of-juju-cli-commands/add-model` page owns invocation syntax/context; `model` and related subjects own semantic contracts.
Action: generated command entry links semantic owners; source-derived behavior should live in generator/help or companion semantic sections, not hand-edited generated output.
Sections needed: purpose/target; syntax/options; context/selection; requested effect/output; bounded conditions/errors; related subjects.
Source checks needed: full option precedence; local selection behavior; error messages/codes; provider/credential consequences beyond command dispatch.
Links needed: model, cloud, credential, controller, user/access, client selection, model defaults/configuration.
Unresolved ties: generated output versus companion source-derived annotations; no current authorization to alter generation.
Do-not-claim limits: generated help is not backend proof; successful command return is not full worker/provider readiness.
```

**Boundary result:** A66 treats generated command pages as invocation surfaces, not
as subjects. The semantic owner for model creation remains `model`; command page
records invocation-specific context and output.

**Diagram/error room:** errors live naturally here because command pages are
caller-facing. A sequence diagram could show CLI → controller create-model →
local selection only if source-derived and stable; entity schema belongs on
`model`, not the command page.

Client-agnostic check: this split is required. The generated command page owns
CLI syntax, local selection and command rendering; the non-CLI `model` page owns
the platform/API model-creation contract. A non-CLI reference page may link to
how-to or CLI material as an example, but not as the semantic owner.

### Case F — hook/action command: `relation-set` partial

```text
Subject: `relation-set` hook/action command page
Reader-needed contract: a unit-context command writes relation settings under relation and leadership context.
Supported surface: generated hook-command help and family-level source trace in `skeleton-nested-117.md:41-48`; individual command derivation blocked by `HookCommandPages` 402.
Classification: hook/action command interface; partial plan only.
Owner/address: generated `hook-command/list-of-hook-commands/relation-set` invocation page for syntax/context; `relation` owns relation data rules; `hook-command` owns shared context rules.
Action: preserve as unresolved individual derivation; do not claim complete per-command semantics from generated help alone.
Sections needed: purpose/affected subject; required hook/action/relation context; invocation/options/input precedence; write effect/leadership conditions; result/errors; links to relation and hook-command.
Source checks needed: complete runtime context matrix, file/CLI value precedence, leadership/application-data behavior, deletion semantics, relation-changed propagation/flush timing, exact errors.
Links needed: relation, unit, hook, hook-command, leadership/application data.
Unresolved ties: individual command content blocked; family outline is not proof of every command.
Do-not-claim limits: dummy generated context is not real runtime context; registration/help is not success in every hook or action.
```

**Boundary result:** A66 classifies the family correctly but refuses to overclaim
individual completeness. This is a partial pass with a real blocker, not a hidden
workaround.

**Diagram/error room:** command pages are good homes for command-local errors;
relation data rules and any relation lifecycle diagrams belong on `relation`.

## 3. Result for the old `database schema → change streams → calls` form

The evidence points **away from preserving it as a universal skeleton** and
**toward preserving its successful functions**.

### Preserve

1. **Structural room for diagrams.** Entity and relationship pages still need a
   structural section when records/participants/invariants are reader-relevant.
   This is where ERDs or schema-like diagrams belong.
2. **Temporal room for diagrams.** Streams, processes and actors still need
   temporal/flow sections when source establishes holder, payload, phases or
   reactions. This is where sequence/state diagrams belong.
3. **Interaction room for errors.** Calls, commands and process phases remain
   the natural home for caller/rules/errors. This directly supports JUJU-10586.
4. **Stable anchors.** Existing schema/stream/call anchors can remain useful
   semantic addresses even if headings become conditional.

### Change

1. Do not force a database schema section on tools, provider pages, generated
   commands, process pages or external UI pages.
2. Do not treat a change stream as mandatory for every entity or as proof of
   actor completion.
3. Do not make `calls` the owner of every mechanism touched by a call; shared
   mechanisms/processes get their own address and the call links them.
4. Do not place errors under a generic page-level error bucket when the error is
   tied to a particular selector, validation step, process phase or downstream
   observation.

### Practical replacement

Use kind-specific forms, but keep three cross-cutting slots:

| Slot | Purpose | Diagram/error effect |
|---|---|---|
| Structure | identity, participants, records, invariants, relationships | ERDs and record diagrams live here. |
| Dynamics | streams, actors, phases, processes, async reactions | Sequence/state diagrams live here. |
| Interactions | calls, commands, selectors, validation, output, errors | Error tables/lists live here, close to the raising/returning path. |

Those slots appear only when the subject kind supports them. They are roles, not
mandatory headings.

## 4. Contradictions and ties found

No contradiction to A66 in these cases. The stress test found these ties/gaps:

- `model command blocks`: model section versus standalone mechanism page remains
  tied unless cross-subject span or maintenance metric justifies a page.
- Provider pages: repeated shared fragments versus provider-local prose remains a
  maintenance/editorial tradeoff; source requires qualification, not one layout.
- Generated CLI pages: generator/help versus companion semantic annotations is a
  publication/process decision, not solved by source.
- Hook/action commands: individual completeness blocked by `HookCommandPages` 402;
  family form cannot substitute for per-command derivation.
- `juju-db-repl`: duplicate-name `.switch` is possible code/contract defect;
  public wording should wait for real worker/database investigation or an
  explicit risk-warning decision.

## 5. Algorithm status after E67

A66 can now be used for first-pass content planning across unlike cases:

- it creates pages for characters/processes/tools/provider intersections when
  their independent contract justifies one;
- it makes legs into sections/anchors;
- it routes errors to interactions/phases/selectors;
- it routes diagrams to structural or temporal contracts;
- it records editorial ties instead of pretending source chooses filenames.

It is still not a proof of final page boundaries for every page. Next confidence
step would be applying it to a full small slice end-to-end, for example
`model` + `add-model` + `model-defaults` + `credential reference` + one provider
page, and checking whether the resulting content plan catches all existing facts
without duplication or orphaned anchors.
