# Focused content-planning slice: model creation across model, command, defaults, credential and LXD — session 119

**Status:** focused validation artifact, not a documentation edit or rollout approval.
E68 was preregistered before this slice was classified. This uses existing
artifacts only; no broad new source inspection was needed and no deviation from
the registered plan was made.

Slice members:

1. `model` — character and owner of model identity/scope.
2. `add-model` — generated CLI invocation.
3. `model-defaults` — neighboring configuration/default mechanism.
4. model credential reference — relationship/facet between model and credential.
5. `lxd` — provider intersection.

## 1. A66 content plans

### 1.1 `model`

```text
Subject: model
Reader-needed contract: a controller-managed scope with identity, qualifier, type, life, cloud/region/credential relationship, configuration, access, hosted contents and model-scoped operations.
Supported surface: ModelManager/API model info and creation paths, model database/controller database records, current model reference page, prior skeleton-control derivation.
Classification: character.
Owner/address: `model` page; identity/scope and model-local legs live here.
Action: update/maintain model page as character page when edits are approved; link out neighboring mechanisms/processes.
Sections needed: definition/scope; identity and dependencies; relevant model records/invariants; applicable streams/actors only where traced; model interactions including creation, show/list/config/reference change/destroy; configuration/failure index; links to migration, agent-version, model-defaults, credential, cloud/provider, status, removal.
Source checks needed: complete watcher inventory; exact create rollback states; list/show details; per-call block inventory; lifecycle/provider outcomes.
Links needed: controller, cloud, credential, user/access, configuration, model-defaults, model-migration, status, storage/removal, provider pages including LXD.
Unresolved ties: exact physical anchor for model command blocks; how much stream material remains local versus watcher/shared mechanism.
Do-not-claim limits: model accepted/created is not provider success; status is composed observation; state writes and worker/provider completion have separate clocks.
```

Owner facts in this slice:

- model owns model identity, qualifier, type, life and model-local scope;
- model owns the fact that it has a cloud/region/credential relationship, but
  not full cloud, credential or LXD provider behavior;
- model owns the initiating create-model interaction as a model operation, while
  `add-model` owns CLI invocation and local selection.

### 1.2 `juju add-model`

```text
Subject: `juju add-model`
Reader-needed contract: one CLI invocation requests model creation on a selected controller and may update local client selection.
Supported surface: generated command page/help plus `skeleton-commands-ad-117.md:25-27` source-derived outline.
Classification: generated command / tool invocation.
Owner/address: generated `juju-cli/list-of-juju-cli-commands/add-model` invocation page; semantic links to model/cloud/credential/defaults/provider.
Action: generated entry should carry invocation syntax/context/output/errors or link to a companion semantic explanation; do not make it the owner of model creation semantics.
Sections needed: purpose/target; syntax/options; context/controller/model-name resolution; cloud/region/owner/credential/config inputs; requested operation/output; local switch behavior; bounded conditions/errors; related subjects.
Source checks needed: full option precedence; local selection and ownership branch; exact error messages/codes; command-generation publication path.
Links needed: model creation section, cloud, credential, model-defaults/configuration, controller, user/access, client selection, provider pages when provider-specific inputs are mentioned.
Unresolved ties: generated output versus companion source-derived annotations; publication mechanics are not decided by this algorithm.
Do-not-claim limits: generated help is not backend proof; successful command return is not worker/provider readiness or a live LXD instance.
```

Owner facts in this slice:

- `add-model` owns command syntax, flags, local context, local switching and
  command-specific output/errors;
- it links the model page for creation semantics and provider pages for
  provider-qualified consequences.

### 1.3 `model-defaults`

```text
Subject: model defaults
Reader-needed contract: controller-managed cloud and cloud-region defaults used as inputs to model configuration and new model creation.
Supported surface: ModelManager defaults facade/service, model-config service consumers, current model-defaults page, skeleton-control derivation.
Classification: shared configuration/default mechanism, not a leg of one model.
Owner/address: `model-defaults` page.
Action: keep as neighboring mechanism page; model and add-model link to it when defaults are consumed.
Sections needed: cloud/region default scopes; values/components returned; read/set/unset interactions; consumption by model configuration/creation; validation/errors; links to key catalog, model, cloud, configuration and command blocks.
Source checks needed: exact per-key precedence; propagation to existing models; provider validation/default additions; relevant change streams.
Links needed: model, cloud/region, configuration, list of model configuration keys, add-model/model-config commands.
Unresolved ties: none for page-vs-section in this slice; exact per-key behavior remains untraced.
Do-not-claim limits: default update is not a guarantee that existing models change; returned field names do not prove universal precedence; provider-specific defaults can differ.
```

Owner facts in this slice:

- `model-defaults` owns default scope, read/set/unset and default-value
  semantics;
- `model` and `add-model` mention defaults only as inputs/selection context.

### 1.4 Model credential reference

```text
Subject: model credential reference
Reader-needed contract: a model may refer to an optional cloud credential; selecting/changing that reference differs from updating the credential's stored content.
Supported surface: model creation and ChangeModelCredential paths summarized in `skeleton-control-117.md:59-71,138-150`; credential reference and update/removal traces.
Classification: relationship/facet between model and credential.
Owner/address: shared between model and credential by scope: model owns the model's reference and reference-change operation; credential owns credential identity/content, validation and removal consequences.
Action: represent as a model dependency/reference section plus links to credential; do not duplicate credential update/removal contract on model.
Sections needed: on model: optional credential reference, use in creation, reference change rules, block/access conditions, do-not-claim provider success. On credential: key/content/associations, update content, forced removal/reference clearing, provider aftermath limits.
Source checks needed: complete validation/provider preflight behavior, downstream provider tracker effects, reference-change errors.
Links needed: model, credential, cloud, user/access, model command blocks, provider page.
Unresolved ties: exact anchor name for the reference facet; no separate page indicated by current slice.
Do-not-claim limits: successful reference change is not credential content update; successful credential update does not prove model cloud reachability; forced removal provider aftermath is inconclusive.
```

Owner facts in this slice:

- the model page owns “this model points to credential X” and reference-change
  interaction;
- the credential page owns what credential X is, how content changes, and removal
  consequences;
- provider pages own provider-specific credential acceptance/credential
  finalization.

### 1.5 `lxd` supported-cloud page

```text
Subject: LXD supported-cloud page
Reader-needed contract: LXD-specific qualifications of generic Juju cloud, credential, model, machine, network and storage behavior.
Supported surface: provider schema/finalization, credential finalization, placement, profile/network and storage-provider traces summarized in `skeleton-cloud-machines-117.md:32-42`.
Classification: provider intersection.
Owner/address: `cloud/list-of-supported-clouds/lxd` provider page.
Action: keep provider page as intersection; link generic owners and state only LXD-conditioned behavior.
Sections needed: local versus remote LXD cloud record; credential enrollment versus runtime certificate credential; model/bootstrap/provider validation caveats; placement/cluster member and virt-type constraints; profile/network behavior; LXD storage provider/pool behavior; version/host caveats.
Source checks needed: local credential discovery/access; image source priority; LXD project lifecycle; forwarding/network backend; `ceph` storage-driver discrepancy; live host/version applicability if making deployment claims.
Links needed: cloud, credential, model, add-model/bootstrap context, machine, constraint, placement-directive, image metadata, space/subnet, storage.
Unresolved ties: provider-local prose versus reusable machine-cloud fragments; current evidence favors provider page with generic links and provider-local qualifications.
Do-not-claim limits: provider validation is not live LXD host success; interactive enrollment is not runtime auth; storage-driver support is provider/version conditioned.
```

Owner facts in this slice:

- `lxd` owns only LXD-qualified behavior;
- generic cloud/credential/model/machine/storage pages own generic contracts;
- `add-model` and `model` link to LXD only when provider-specific behavior is
  relevant.

## 2. Combined slice checks

### Check 1 — No duplicate owner

| Fact family | Owner/address | Link-only/context mentions |
|---|---|---|
| Model identity, qualifier, type, life | `model` | `add-model`, DB/tools, provider pages link when selecting or qualifying. |
| Model creation semantics | `model` interaction | `add-model` owns CLI invocation; provider pages own provider preflight/finalization specifics. |
| CLI syntax, local context and switching | `add-model` generated command | `model` does not repeat CLI flags except as links. |
| Cloud/region default values used by new models | `model-defaults` | `model` and `add-model` mention default consumption only. |
| Model credential reference | `model` facet / reference-change section | `credential` owns credential content; `add-model` mentions selected credential input. |
| Credential identity/content/update/removal | `credential` | `model` links; LXD provider only qualifies accepted/runtime credential form. |
| LXD provider behavior | `lxd` provider page | `model`, `cloud`, `credential`, `storage` link to provider-specific qualification. |
| Error lists | Raising/returning interaction | Shared pages link; no generic page-level bucket. |
| Diagrams | Structure/dynamics/interaction home by contract | No duplicate diagram homes required. |

**Result:** pass. The only split owner is the model credential reference, and it
is a deliberate relationship/facet split: model owns the reference; credential
owns the credential.

### Check 2 — No orphan anchor

Required reader entry points in this slice:

| Entry point | Proposed address | Status |
|---|---|---|
| What is a model? | `model` definition/scope | Addressed. |
| Why can two models share a name? | `model` identity/name+qualifier | Addressed. |
| How does `juju add-model` choose/request? | generated `add-model` page | Addressed; publication mechanics unresolved. |
| What defaults feed model creation/config? | `model-defaults` | Addressed. |
| What credential does a model use? | model credential-reference facet + `credential` page | Addressed. |
| What does LXD change about cloud/credential/machine/storage behavior? | `cloud/list-of-supported-clouds/lxd` | Addressed. |
| Where do provider-specific credential forms live? | LXD provider credential section + generic `credential` link | Addressed. |
| Where do create-model errors live? | platform/API creation errors on the client-agnostic `model` creation interaction; CLI-local validation, store and switch errors on generated `add-model` | Addressed. |
| Where do diagrams live? | model structure, add-model interaction flow, LXD provider decision flow if warranted | Addressed. |

**Result:** pass with one explicit unresolved publication issue: generated command
output versus companion semantic annotations.

### Check 3 — Errors and diagrams have homes

#### Errors

| Error type | Home |
|---|---|
| Invalid model name/qualifier | `model` creation interaction; `add-model` may expose CLI-local validation. |
| Unauthorized model creation | `model` creation interaction and `add-model` invocation output. |
| Missing/default cloud/region/credential selection errors | `model` creation interaction with links to cloud/credential/model-defaults. |
| Provider-open/preflight errors | `model` creation interaction, provider-specific detail on LXD/provider page when provider-specific. |
| Model-defaults unknown cloud/region/key validation | `model-defaults` read/set/unset interactions. |
| Credential content/update/removal validation | `credential` update/removal interactions. |
| Credential reference change blocked/unauthorized/not found | model reference-change interaction, linked to credential identity. |
| LXD credential finalization/placement/storage validation | `lxd` provider page sections; command pages link if the invocation exposes them. |
| Local CLI store/switch errors after create | `add-model` command page. |

Client-agnostic check: platform/API errors stay on `model` or neighboring
semantic owners. `add-model` owns only command syntax, local validation, local
store/switch behavior and command rendering. Non-CLI reference pages should not
link to generated CLI pages as the semantic source.

#### Diagrams

| Diagram type | Home |
|---|---|
| Model identity/dependency ERD | `model` structure section. |
| Model creation request flow | either `model` creation interaction or `add-model` command flow, depending on whether it includes CLI-local selection; keep one owner and link. |
| Defaults consumption diagram | `model-defaults` if explaining default scopes/components; model links. |
| Credential reference diagram | model/credential relationship facet; likely small relationship diagram, not full credential internals. |
| LXD credential finalization or placement decision flow | `lxd` provider page, because branches are provider-specific. |

**Result:** pass. The old `schema/streams/calls` headings are not necessary as
literal headings. Their roles survive as structure/dynamics/interactions.

## 3. Duplication/orphan risk notes

1. **Highest duplication risk:** model creation and `add-model`. Fix by making
   `model` own creation semantics and `add-model` own invocation/local client
   behavior. Both can mention the same operation, but not as duplicate owners.
2. **Second duplication risk:** model credential reference and credential update.
   Fix by drawing the line between a model's pointer and credential content.
3. **Third duplication risk:** LXD credentials and generic credentials. Fix by
   keeping generic credential identity/content on `credential`, and LXD-specific
   enrollment/runtime branches on the provider page.
4. **Anchor risk:** generated command pages may be overwritten. Source-derived
   semantic details need either generator/help integration or companion links;
   this is a publication decision, not an algorithm failure.
5. **Diagram risk:** model creation flow could live on either model or `add-model`.
   Use one owner based on diagram scope: if it includes CLI local selection, put
   it with `add-model`; if it shows controller-side creation, put it with
   `model`.

## 4. Focused verdict

E68 passes under the preregistered success plan.

- No duplicate owner appears when relationship/facet splits are named.
- No reader entry point in the slice is orphaned; the only unresolved issue is
  generated-page publication mechanics.
- Errors and diagrams keep principled homes after moving from mandatory
  schema/streams/calls headings to structure/dynamics/interactions roles.
- No new evidence compelled deviation from the success plan.

This supports using A66 for focused first-pass rollout planning. It still does
not prove global correctness. The next focused slice should test a non-model
cluster, such as `relation` + `relation-set` + `hook-command` + `relation` data
rules, but that slice is partly blocked by the `HookCommandPages` 402 unless the
user explicitly chooses how to handle the gap.
