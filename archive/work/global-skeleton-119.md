# Candidate global reference skeleton — session 119

**Status:** candidate structure for review, not an approved documentation, page-layout,
repository-rule, selected-counter or PR-link change. Source paths and cited work artifacts
refer to the established 4.1 anchor `/tmp/juju-41-tree` at `e5db99d585` unless stated
otherwise. This artifact synthesizes existing evidence; it does not claim live controller,
provider, cloud, UI, database or charm execution beyond the recorded probes.

## 1. Decision policy

A reference entry gets a stable **semantic address** when a reader needs a supported
contract: identity or vocabulary, a condition-dependent behavior, an observation, or a
specific tool/interface rule. A semantic address may be a page, section or generated
entry. The source can establish scope, participants, conditions and outcomes; it often
does **not** choose a unique physical file.

Use this page/section policy consistently:

1. **Candidate pages:** independently managed subjects; cross-subject mechanisms whose
   semantics are genuinely shared by otherwise independent entries; tool/interface
   families with their own invocation context; provider intersections when generic
   contracts must be qualified by provider behavior.
2. **Candidate sections:** subject-specific behavior, a relationship facet, a provider
   branch under a cloud page, a command-specific invocation rule, or an interface
   selector that does not define the target's identity.
3. **Explicit ties:** if two layouts preserve the same facts, conditions and links,
   record an editorial tie. Existing URLs are a conservative tie-breaker only after
   semantic equivalence, not evidence that the old chunking was right.
4. **Local conditions stay local:** shared rules get one address and links only when the
   common contract is source-demonstrated. Validation, permission, target selection,
   timing, errors and provider results stay with the interaction where they differ.

This follows the prior distinction between target invariants and interface selectors in
E64 (`operational-boundaries-e64.md:7-23,47-55`) and the E63 finding that same facts can
fit a shared section or standalone page with identical source support (`boundary-rules-e63.md:47-65`).

## 2. Global candidate map

Arrows below mean “link needed to interpret this contract,” not a universal execution
order. The user's settled causal order remains the default for applicable entity entries:
definition and scope → records/invariants → streams → actors → interactions → configuration
and failure indexing. Process and tool entries use their own flow.

### Control, identity and access

Candidate entries and addresses:

- `controller`: controller scope, hosted models, API root restrictions, destruction,
  backup address tie, HA/upgrade links (`skeleton-control-117.md:33-44`).
- `model`: model identity, qualified name, cloud/region/credential relationship,
  command blocks, destruction, migration and configuration links (`skeleton-control-117.md:138-150`).
- `cloud`, `credential`, `model-defaults`, `configuration`: separate cloud/provider
  context, cloud credential content and references, scoped defaults, and configuration
  namespaces (`skeleton-control-117.md:20-31,59-71,152-163`; `skeleton-nested-117.md:9-23`).
- `user` / shared access: principal identity, target-specific grants, login versus
  authorization, user lifecycle (`skeleton-control-117.md:209-220`).
- `agent`, `agent-version`: agent identities and authentication; target software,
  reported versions and binary availability (`skeleton-mechanisms-117.md:15-24`; `skeleton-control-117.md:7-18`).
- `database`, `object-store`, `lease`, `backup` address: persistence/inspection,
  object content, coordination, and the unresolved backup home (`skeleton-control-117.md:73-84,125-136,179-193`).

Cross-links:

- Model creation links `cloud` + optional `credential` + `model-defaults` + `user/access`.
- Any protected operation links both access and model command blocks where that call is
  actually checked; no blanket “every call checks block” rule.
- Agent authentication links to agent kind and target-specific authorization; login is
  not global authorization.
- Backup links controller, database, object store and lease; its physical home remains
  a controller-vs-neutral mechanism tie.

### Workload, integration and execution

Candidate entries and addresses:

- `charm`: declaration vocabulary for options, endpoints, actions, resources and storage
  (`skeleton-workload-117.md:44-53`).
- `application`: realization of a charm in a model; endpoint bindings, trust, units and
  application configuration (`skeleton-workload-117.md:31-42`).
- `unit`: unit identity, agent, relations, attachments and unit-specific interactions
  (`skeleton-workload-117.md:112-122`).
- `relation`: composition of application endpoints and participant-specific data;
  relation-unit watcher and hook context (`skeleton-workload-117.md:76-87`).
- `offer`, `external-controller`: cross-model offer and stored remote-controller record
  (`skeleton-workload-117.md:64-74`; `skeleton-control-117.md:86-97`).
- `action` + shared `script`/`operation`/`task`: declared action versus invocation records
  and administrative exec (`skeleton-workload-117.md:7-18`; `skeleton-mechanisms-117.md:89-100`).
- `hook`, `hook-command`, `jujuc`: hook trigger/execution context and hook/action command
  transport (`skeleton-mechanisms-117.md:34-54`; `skeleton-tools-117.md:114-126`).
- `secret`, `secret-backend`, `resource-charm`: secret identity/revisions/backend and
  charm-resource declaration/content/fetch paths (`skeleton-workload-117.md:54-62,89-110`).

Cross-links:

- Charm endpoint declaration → application endpoint/binding → relation composition → hook
  and hook-command context.
- Action declaration → script/operation/task records → task output/object-store/status.
- Secret selector vocabulary links from each call, but selector precedence and error scope
  remain call-local.
- Hook pages link watcher only for traced watcher-driven cases; `update-status` preserves
  the timer exception.

### Infrastructure and dependent resources

Candidate entries and addresses:

- `constraint` and `placement-directive`: reusable request inputs, merge/precheck and
  provider-specific placement grammar (`skeleton-infrastructure-117.md:7-20`; `skeleton-nested-117.md:17-23`).
- `machine`: model-managed machine identity, provisioning actor, status, disk-inspection
  facet, removal and provider realization links (`skeleton-infrastructure-117.md:37-53`).
- `storage`: pool, directive, instance, backing filesystem/volume, unit/machine
  attachments and provider interactions as separately linkable sections on one page
  initially (`skeleton-infrastructure-117.md:103-119`).
- `space`, `subnet`, `zone`, `link-layer-device`: network grouping, CIDR/zone association,
  provider-reported zones and observed network devices (`skeleton-infrastructure-117.md:22-35,55-69,121-150`).
- `ssh-key`, `ssh-server`: persistent public key/model association versus connection
  request/authorization/route (`skeleton-infrastructure-117.md:71-101`).
- Provider-specific cloud pages: nine machine-cloud pages and five Kubernetes cloud pages
  as provider intersections over cloud, credential, bootstrap, model config, allocation,
  networking and storage (`skeleton-nested-117.md:59-85`; `skeleton-cloud-machines-117.md:5-8`).

Cross-links:

- Machine allocation links model, constraint, placement, image metadata, provider cloud,
  network and storage; accepted state does not imply cloud instance success.
- Storage removal links machine/unit removal, attachment, backing resource and provider;
  no universal filesystem-survives or filesystem-dies rule.
- Spaces/subnets/zones link application endpoint binding and exposure; firewall/provider
  application remains provider- and path-specific.
- Cloud pages link generic owners and add only provider-conditioned intersections; repeated
  fragments are not standalone contracts.

### Cross-cutting processes and observations

Candidate entries and addresses:

- `model-migration`, `controller-upgrade`, `removing-things`, `scaling`: process entries
  with participants, initiation/guards, phases, observations, failure/recovery limits
  (`skeleton-control-117.md:46-57,165-177`; `skeleton-mechanisms-117.md:67-87`).
- `watcher`: holder, payload, initial delivery and limits, linked from each subject's
  actual stream (`skeleton-mechanisms-117.md:115-123`).
- `status`: composed current observation and separate history query/recording contract
  (`skeleton-mechanisms-117.md:101-114`).
- `log`: agent/debug logs, API audit records, filtering and forwarding links
  (`skeleton-mechanisms-117.md:55-66`).
- `telemetry`: Charmhub metrics, tracing and forwarding as separate observation mechanisms
  (`skeleton-control-117.md:195-207`).
- `object-store`, `database`, `juju-db-repl`: inspection/storage tools and persisted
  artifacts connected to backup, resource, task-output and migration paths.

Cross-links:

- Processes link their participating subjects; individual initiating calls retain their
  access, guards and return values.
- Observations link producers, timing and filters; a current value, watcher event, log line
  or audit record is not a completion guarantee.
- Status-history shared recording can be one `status` section linked from unit/machine
  setters, but the history-kind mismatch blocks final contract wording.

### Interfaces, tools, catalogs and generated families

Candidate entries and addresses:

- `juju`, `client`, `juju-cli`: platform orientation, client transport/context and local
  dispatcher/environment/plugin behavior (`skeleton-tools-117.md:9-53`).
- `juju-web-cli`, `juju-dashboard`: external UI/versioned dashboard behavior and the local
  dashboard access command, both undertraced (`skeleton-tools-117.md:55-82`).
- `jujuagentd`, `containeragent`, `jujuc`, `pebble`, `resource-compute`: host executables,
  Kubernetes unit agent, command transport, external supervisor integration and local
  diagnostic tools (`skeleton-tools-117.md:84-172`).
- `juju-db-repl`: privileged local database inspection/mutation interface; `.switch` and
  `.open` are interface selectors, not model identity rules (`skeleton-tools-117.md:143-156`).
- CLI command family: 159 generated invocation pages plus index; command form is purpose →
  invocation/options → target/context → effects/output/errors → related subjects
  (`skeleton-nested-117.md:31-40,181-202`).
- Hook/action command family: 38 generated command pages plus copied index; command context
  and subject effects must be derived per command, but the individual derivation is blocked
  (`skeleton-nested-117.md:41-48,165-171`).
- Configuration-key catalogs: generated controller/model key lists plus authored key-detail
  pages; key entries are scoped setting addresses, not standalone entities
  (`skeleton-nested-117.md:49-56,161-163`).
- Local compute-resource commands and introspection macro pages: host-local tool addresses,
  not remote controller API commands (`skeleton-nested-117.md:118-141,204-211`).
- Compatibility, environment-variable and plugin-metadata nested pages remain authored
  interfaces/policy pages requiring source/policy verification (`skeleton-nested-117.md:105-112`).

Cross-links:

- Generated pages link back to semantic owners rather than copying full subject contracts.
- Generated help proves representation and formatting, not backend success, permissions,
  model-type support or live output.
- Tool pages describe local execution context, target selection and result/errors; they do
  not inherit entity record/stream sections unless source establishes that role.

## 3. Internal forms by entry kind

| Entry kind | Candidate internal form | Non-negotiable limits |
|---|---|---|
| Entity/subject | definition and scope → relevant records/invariants → applicable streams → actors → interactions → configuration/failure index → migration links where relevant | Roles are conditional; no fake stream/actor section just for uniformity. |
| Relationship/facet | participants and scope → records/rules → participant-specific validation/effects → operations/observations → links to each participant | A relationship can be a section when its owner is clear; file split is not automatic. |
| Shared mechanism | common vocabulary/rule → participants/consumers → conditions and exceptions → affected calls/links → failure/observation limits | Shared address requires demonstrated common contract; local differences stay local. |
| Process | participants → initiation/guards → stages and dependencies → observations → failure/recovery and rollback boundaries | Request acceptance is not process completion. |
| Tool/interface | execution context → invocation/inputs → target selection → effects/result/output/errors → related subjects | Interface selector rules do not redefine target identity. |
| Generated command | purpose → syntax/options → target/context → requested effect/output → bounded conditions/errors → owner links | Generated help alone is not behavioral proof. |
| Provider/cloud page | cloud/credential → bootstrap/controller context → model config → allocation/network/storage intersections → provider-specific failures → generic links | Provider schema or repeated prose is not live cloud evidence. |
| Catalog/key page | key/scope → type/default/source → mutability/validation → consuming behavior → set/unset/read errors → owner links | Generator defaults/comments are not exhaustive runtime behavior. |

## 4. Concrete page/section candidates, not implementation authorization

1. Keep existing direct subject pages as review addresses for now; introduce or preserve
   stable sections for shared contracts instead of moving files prematurely.
2. Use `script`'s existing `operation`/`task` anchors as the candidate neutral home for
   shared action/exec run records after verifying diagrams, streams and links.
3. Use `status` as the candidate home for status-history recording, linked from traced
   setters, but block final wording on the history-kind mismatch.
4. Use `model` or a linked model-control section for model command blocks, with per-call
   enforcement only after tracing each call.
5. Keep storage on one page initially but treat pool, directive, instance, backing and
   attachment as separate semantic addresses.
6. Treat backup as a stable `[controller backup]`-style address whose physical home is
   unresolved between controller and a neutral/database-adjacent mechanism.
7. Keep provider pages as provider intersections, not forks of every generic cloud,
   machine, network and storage contract.
8. Keep generated CLI and hook/action command pages as invocation pages linked to semantic
   owners; do not hand-edit overwritten generated output to carry source-derived behavior.
9. Preserve existing anchors and figures until concrete changes are approved.

## 5. E65 challenge result

**Verdict:** P119 passes the bounded session-119 challenge as a connected candidate, not as
a locked skeleton. It covers direct pages, nested families, generated command families,
tool/platform pages and provider pages with explicit gaps and blocked scopes. It preserves
the key behavioral distinctions from prior traces and records physical-layout ties.

Challenge checks:

- **Entity:** `model` separates qualified identity, cloud/credential references, command
  blocks, destruction and migration. E64's DB REPL `.switch` remains an interface selector
  risk rather than a model identity rule.
- **Relationship:** `relation` keeps endpoint composition and participant-specific data
  distinct from charm declaration and application binding.
- **Cross-subject mechanism:** `status`/history and `model command blocks` can be shared
  addresses, but each call's validation/result remains local; equal-content call-local
  copies remain expressive alternatives.
- **Tool/interface:** `juju-cli` plugin dispatch and `juju-db-repl` selection rules are
  interface contracts, not target invariants.
- **Generated/nested family:** CLI commands, hook/action commands, configuration keys,
  provider pages and local diagnostic pages all receive family forms; generation/accounting
  counts are treated as coverage aids, not semantic proof.

What this does **not** prove:

- reader benefit, findability or reduced wrong turns;
- unique filenames or page-vs-section decisions in tied cases;
- complete source truth for every page statement;
- live controller/provider/UI/database behavior beyond recorded smoke probes;
- individual hook/action command completeness or Kubernetes cloud refinements.

## 6. Unresolved cases and blockers to carry forward

Blocked by 402 and not to be relaunched or worked around:

- `WorkloadModel`: earlier workload scope remains incomplete.
- `HookCommandPages`: individual derivations for the 38 generated hook/action command pages
  are absent; family outline is not per-command proof.
- `KubernetesCloudAttributes`: provider-specific refinements for five Kubernetes cloud pages
  remain incomplete.

Possible code/contract defects, not prose-only fixes:

- DB REPL `.switch model-<name>` uses a name-only query despite model name/qualifier
  uniqueness; synthetic schema exercise returned one of two rows. `.open` accepts UUID.
- Status-history filter ignores several valid/help-listed kinds in the traced service path.
- Image metadata priority/order may conflict with current reference wording; helper-only
  probe, not live provider.
- Annotation `Set` result shape may be error-only, not one result per entity.
- `juju dashboard` source path returns `NotImplemented`; this does not prove external
  dashboard absence.
- Provider/cloud discrepancies for OCI, LXD, MAAS and others require provider/version and
  live-capability qualification before page edits.

Editorial ties still open:

- backup home: controller section versus neutral mechanism/database-adjacent page;
- shared status-history: `status` section versus repeated per-call text;
- shared operation/task records: `script` anchors versus action-local copies;
- annotation and sequence allocation: standalone page versus shared section;
- provider fragments: reuse inclusion versus repeated provider-page prose where facts differ.

## 7. Next discriminating work

Do not edit pages yet. The next useful work is either:

1. turn this candidate into a reviewable approval request with explicit concrete page/rule
   changes and unchanged anchors, or
2. run one registered challenge that can decide an actual remaining tie: for example a
   maintenance/address metric for backup or operation/task placement using equal facts and
   stable-link consequences, or a targeted source investigation of a possible code/contract
   defect before public wording is chosen.

Any new held-out inspection must be registered in `structure-discovery-plan.md` before
source inspection. JUJU-10585 reference structure, JUJU-10586 error contracts and JUJU-9635
figures/process remain separate deliverables in one integrated PR.
