# Content-planning algorithm from character versus leg — session 119

**Status:** planning algorithm proposal, not an approved documentation edit or
repository-rule change. This converts the current JUJU-10585 research into an
operational procedure for deciding what to create, update, link or investigate
when a new thing needs documenting. It is calibrated on the `model` reference
page because that page contains a likely character plus many legs, relationships,
processes, observations and interface effects.

Source and docs references use the established session context: docs worktree
`/home/dora/git/misc/juju-tutorial-diagrams`, source anchor
`/tmp/juju-41-tree` at `e5db99d585`, and research artifacts in `work/`.

**Historical draft.** The active proposed procedure remains
`reference-spec-proposal.md` and its causal-role principle; the decision tree
in `content-planning-decision-tree.md` is a further unapproved proposal, not a
user-adopted method. This draft's count-like character/leg tests, reader-question
test and equal-facts page-choice rule below are not active decision criteria.
Prior cases are historical evidence, not approval to edit pages or rules.

## 1. Goal

Given a proposed documentation subject, the algorithm should return a content
plan:

- create a page;
- add or update a section on an existing page;
- update a shared mechanism/process/tool/interface page;
- add links only;
- or investigate because the boundary is not decidable yet.

It must also say why, which sections are needed, which facts need source checks,
which existing pages are touched, and which ties remain editorial.

## 2. Definitions

A **contract** is the reader-needed claim: identity, vocabulary,
condition-dependent behavior, observation, tool/interface rule, or provider
intersection.

A **character** is a reference subject with independent reader-facing identity.
It can carry a page when enough of the following are true:

1. It has its own identity or stable address.
2. It has lifecycle, state changes, operations or observations of its own.
3. It can vary independently of a parent.
4. Other subjects refer to it by name.
5. A reader can ask useful questions about it without primarily asking about its
   parent.
6. Its conditions and effects are not fully predictable from one parent
   character's rules.

A **leg** is real, nameable and sometimes inspectable, but dependent. It should
usually be a section or subsection of a character when most of the following are
true:

1. It is meaningful only as part of one character.
2. It has no independent lifecycle or management surface.
3. It is an attribute, selector, copied record, scoped rule or relationship end.
4. Readers reach it through the parent character's task.
5. Other entries need to link to it only to interpret the parent.

Other contract types:

- **Relationship:** participant-dependent rule between two or more characters.
- **Process:** phased behavior over time where request, state change,
  observation and completion can differ.
- **Shared mechanism:** reusable rule across otherwise independent entries.
- **Tool/interface:** invocation, selection, context, output and error contract.
- **Provider intersection:** generic Juju contract qualified by one provider.
- **Catalog/generated entry:** scoped list of many small contracts, often
  generated or index-like.

A semantic address can be a page, section, generated entry or anchor. Page choice
is editorial when two layouts preserve the same facts, conditions and links.

## 3. Algorithm

### Step 0 — State the proposed subject

Write the candidate in one sentence:

> We need to document **X** because readers must predict **Y**.

If **Y** is not a reader-visible or supported-inspection contract, park it as a
source/developer note, not a reference-doc candidate.

### Step 1 — Name the contract

Classify the reader-needed claim:

- identity/vocabulary;
- stored state or invariant;
- request/operation;
- asynchronous process;
- observation/status/log/history;
- tool/interface selector;
- provider-specific behavior;
- configuration/key/default;
- generated command/help surface.

Do not classify by filename, Go package, table name, current page, or a reader
question alone. Questions test relevance and coverage, not ownership.

For non-CLI reference pages, keep the plan client-agnostic: state the platform
or API fact first, and treat CLI, Terraform, dashboard or other clients as
examples or separate interface pages. A generated command page can own command
syntax and local client behavior; it must not become the semantic owner for the
platform contract.

### Step 2 — Find the supported surface

Record the surface that makes the claim reference-worthy:

- CLI or generated command help;
- API/facade/client call;
- hook/action command;
- status, log, audit, telemetry or watcher output;
- database inspector/DB REPL;
- UI or external project version;
- provider request/result path;
- documented generated catalog.

No supported surface means no user-facing claim yet. Internal state can still be
a lead.

### Step 3 — Identify participants and clocks

List:

- target;
- actor/caller;
- request inputs/context;
- stored state read or changed;
- downstream worker/agent/provider/charm;
- observation or returned result;
- timing: synchronous return, later process, eventual observation;
- failure/error boundary.

This prevents collapsing request, state write, worker reaction and realized
effect.

### Step 4 — Apply character versus leg

Ask the character tests. If yes, propose a page or existing page owner.

Ask the leg tests. If yes, attach it to the owning character and give it a
semantic address if links need it.

If neither fits, classify as relationship, process, shared mechanism,
tool/interface, provider intersection or catalog/generated entry.

### Step 5 — Decide content action

| Classification | Default action | Exceptions |
|---|---|---|
| Character | Create or update a page for the character | If existing page already owns it, update sections/links only. |
| Leg | Add/update section under owning character | If several independent characters use the same leg contract, test shared mechanism. |
| Relationship | Add section under strongest owner or shared address | Page only if independently managed or heavily cross-subject. |
| Process | Shared process page or existing process page | Keep initiating call details local. |
| Shared mechanism | One shared address plus links | Do not hide call-specific validation/results. |
| Tool/interface | Tool/interface page or generated command entry | Link target invariants; keep selector/context local. |
| Provider intersection | Provider page section | Link generic cloud/machine/storage/credential owners. |
| Catalog/generated entry | Catalog page or generated entry | Generated help is not backend proof. |
| Unresolved tie | Record tie and needed discriminating evidence | Existing URL can break only a semantic-equivalent tie. |

### Step 6 — Choose the section skeleton

Use the kind-specific form, not one universal template.

| Kind | Section skeleton |
|---|---|
| Character/entity | definition and scope → relevant records/invariants → applicable streams → actors → interactions → configuration/failure index → migration/process links where relevant |
| Leg | parent relationship → exact rule/value → where it is read/changed/observed → links and limits |
| Relationship | participants → participant-specific rules → operations/effects → observations/errors → links to each participant |
| Process | participants → initiation/guards → phases/dependencies → observations → failure/recovery/rollback limits |
| Shared mechanism | common rule/vocabulary → consumers → exceptions → links from affected interactions → failure/limit notes |
| Tool/interface | context/prerequisites → invocation/input → target selection → effects/output/errors → target links |
| Provider page | provider identity/auth → model/bootstrap config → allocation/network/storage intersections → provider failures → generic links |
| Catalog/key | scope/key → type/default/source → validation/mutability → consumers/effects → read/set/unset errors |
| Generated command | purpose → syntax/options → target/context → requested effect/output → bounded errors → owner links |

### Step 7 — Return a content plan

The algorithm output must be explicit:

```text
Subject:
Reader-needed contract:
Supported surface:
Classification:
Owner/address:
Action: create / update / link / investigate
Sections needed:
Source checks needed:
Links needed:
Unresolved ties:
Do-not-claim limits:
```

## 4. Worked calibration: the model page

The current `model.md` defines a model as a controller workspace that holds a
deployment and links applications, machines, storage, spaces, relations, secrets,
cloud, credential, configuration and users (`docs/reference/model.md:14`). Its
schema section records name/qualifier uniqueness, model type, model database
copy, cloud/region/credential references, secret backend and last login
(`model.md:26-40`). It then has change streams and calls (`model.md:41-254`).

### Classification table

| Candidate on/near `model.md` | Classification | Why | Planning consequence |
|---|---|---|---|
| Model | Character | Controller-scoped identity, lifecycle, access, configuration, hosted contents and operations; many other subjects refer to it. | Keep/create model page as character page. |
| Model name + qualifier | Leg of model identity | Unique only together and meaningful as model identity; no independent lifecycle. | Model identity/scope section. Link from selectors that use model names. |
| Model UUID | Leg of model identity; interface selector for some tools | Stable identifier of model; `.open` uses UUID in DB REPL but UUID is not a separate subject. | Model identity section; tool-specific selection stays with DB REPL. |
| Model type (`iaas`/`caas`) | Leg of model; condition for other contracts | Decides model-type restrictions and substrate behavior, but no independent management. | Model records/invariants; link CAAS/IAAS-specific operations. |
| Model life | Leg of model lifecycle | Alive/dying/dead belongs to model and removal/migration interactions. | Model lifecycle/removal section; link removal and migration process pages. |
| Model database identity copy | Leg / database-inspection facet | Copied record can lag authority; meaningful for model processes and DB inspectors, not independently managed. | Model records section with database limits; link database/DB REPL. |
| Model constraints | Leg of model plus shared constraint mechanism | Model can hold constraints, but merge/validation is shared with application/machine consumers. | Model records/config section links `constraint`; keep merge/provider details at constraint/consumer paths. |
| Cloud/region reference | Relationship/facet between model and cloud | Model points to cloud/region; cloud has separate identity/provider behavior. | Model dependency section plus links to cloud/provider pages. |
| Credential reference | Relationship/facet between model and credential | Changing a model's credential reference differs from updating credential content; credential has own lifecycle. | Model config/call section links credential; do not put full credential contract on model. |
| Model configuration | Leg/settings namespace plus configuration mechanism | Settings are model-scoped, but configuration as a concept spans controller/model/application and keys. | Model configuration section links `configuration` and key catalog. |
| Model defaults | Shared configuration/default mechanism, not a leg of one model | Controller/cloud/region defaults are inputs to future model config; not owned by a single model. | Separate `model-defaults` address; model links when defaults are consumed. |
| Secret backend selection | Relationship/facet between model and secret backend | Model selects backend; backend identity/config and secret storage are separate. | Model config section links `secret-backend`; backend rules stay there. |
| Last login | Leg / observation of model-user relationship | Per-user model access observation; meaningful through model listing/user access. | Model listing or user/access section; source-check exact writer/reader before broad claims. |
| Active-model stream | Stream/observation touching model; maybe model leg if holder/payload traced | It concerns model processes starting, but watcher contract is not model identity. | Model stream section only with holder/payload/limit; link watcher. |
| Migration phase stream | Process observation | Migration phase belongs to model migration process and agents. | Model stream can link; full phase contract belongs to `model-migration`. |
| Credential stream | Relationship observation | Follows credential changes for model cloud credential, not full credential contract. | Link credential/provider-tracker; keep limits local. |
| Target agent version | Leg of model plus `agent-version` shared subject | Model holds target version; upgrade behavior belongs to agents/agent-version and controller upgrade. | Model record/call links `agent-version`; no instant upgrade claim. |
| Model command block | Likely model leg with shared control address | Model-scoped control reused by multiple calls; separate from access. | Candidate `[model command blocks]` section/address on model; per-call enforcement remains local. |
| Adding model | Model interaction | Creates model records and dependencies, but provider preflight and worker start have separate clocks. | Model call section; separate request/state/write/later worker observations. |
| Listing/showing model | Model observation interaction | Reads model and related summaries/details. | Model calls; link status/users/secret backend details. |
| Configuring model | Mixed model interaction and neighboring contracts | Changes keys, constraints, credential reference, secret backend, defaults. | Model call section with links to config, constraints, credential, backend, defaults. |
| Upgrading model | Process/shared agent-version interaction | Model target version changes; agents upgrade later; controller model touches controller-upgrade. | Model call links `agent-version` and `controller-upgrade`; local access/block/error details stay. |
| Migrating model | Process | Source/target controllers, quiescence, import/export, agents and phases exceed model as character. | `model-migration` page owns process; model page links and keeps initiating call. |
| Destroying model | Process / model interaction | Model life changes and removal jobs schedule dependent cleanup; provider/storage outcomes conditional. | Model call plus `removing-things` and storage links; avoid completed-provider-cleanup wording. |
| Status/history | Observation mechanism | Status composes model and contents; history has separate recording/query contract and possible kind mismatch. | Link `status`; model page should not own full history contract. |
| Database inspection of model records | Tool/interface + database facet | DB REPL exposes model DB/controller DB; selection and SQL behavior are tool-specific. | Link `database` and `juju-db-repl`; keep `.switch` ambiguity at DB REPL. |

### What the worked case teaches

1. `model` is a strong character, but many model-touching contracts are not
   model-owned.
2. The model page can legitimately have sections for identity, records, streams
   and interactions, but each section must label when it is only a link to a
   relationship, process, shared mechanism or tool.
3. A real named thing is not automatically a page: name/qualifier, model type,
   life, identity copy and target agent version are legs or facets unless a
   separate supported contract appears.
4. A model-touching process is not automatically a model section: migration,
   upgrade and removal need process addresses because request, state changes,
   agents/workers/providers and observations differ over time.
5. Source evidence can force distinctions, but often cannot force file layout.
   Model command blocks, status-history recording and backup-like mechanisms may
   still have section-versus-page ties.

## 5. Example output for a new-topic request

If the user says, “We need to document model command blocks,” the algorithm
returns:

```text
Subject: model command blocks
Reader-needed contract: a model-scoped control that refuses selected operations
Supported surface: block/enable/disable/list commands and affected API calls
Classification: leg of model plus shared model-control mechanism
Owner/address: candidate section/address under model, with links from each traced call
Action: update model/shared control address; link from affected operations; investigate full call inventory before claiming universal enforcement
Sections needed: definition/scope, block kinds, switch/read operations, enforcement precedence, per-call links, errors/limits
Source checks needed: every operation claimed to check a block; block kind precedence; messages/codes
Links needed: model, user/access, affected command pages, controller/model removal/config calls
Unresolved ties: model section vs standalone block-command page if cross-subject span grows
Do-not-claim limits: not authorization; not every call checks it; not proof operation never changes state before a later error unless traced
```

If the user says, “We need to document model name ambiguity in the DB REPL,” the
algorithm returns:

```text
Subject: DB REPL model name selection
Reader-needed contract: `.switch model-<name>` selector can differ from model qualified identity
Supported surface: DB REPL source and synthetic schema exercise
Classification: tool/interface selector, linked to model identity
Owner/address: `juju-db-repl` selection/navigation section; model identity section links qualified identity only
Action: update/investigate DB REPL contract, not model identity; investigate possible defect before public guarantee
Sections needed: model identity link, `.switch` by name, `.open` by UUID, ambiguity limits, write-risk warning if approved
Source checks needed: real worker/database behavior under duplicate names if available; error/selection behavior
Links needed: model identity, database, DB REPL warning
Unresolved ties: prose warning vs source fix/contract defect
Do-not-claim limits: no live REPL/controller result yet; no deterministic row choice without evidence
```

## 6. Current verdict

E66 passes as an algorithm draft: it classifies the hard `model` cases without
making every real noun a page or every model-touching behavior a model-owned
section. It gives a reusable output format for future content planning.

It is not final. Remaining tests should apply the same algorithm to one
non-entity tool, one provider page and one generated command page, using the
same output format and recording any contradictions.
