# Juju reference structure: proposed specification and case suite

**Status: research draft, not an approved change to the reference, its existing
skeleton or repository rules.** This consolidates prior work; it is not a new
source investigation or a claim that the entire reference has been verified.
The existing documentation guidance remains in force until a concrete
replacement is approved. Code citations refer to the Juju 4.1 research anchor
`/tmp/juju-41-tree` at `e5db99d585` unless otherwise noted.

**Session 123 revision:** the organization procedure and equal-facts case below
now reflect the user's character/leg, cross-page abstraction and minimal-reuse
clarifications. The actual candidate regression and proposed page consequences
are in `work/structure-review-123.md`. This remains an unapproved research draft;
no reference page, skeleton or repository rule has been changed.

**User emphasis:** reference describes all relevant primitives at the right
granularity, including abstractions and relationships—not only CLI commands,
API endpoints, fields or schemas. The underlying concepts and their behavior
must be accounted for even when no single interface names them directly.

**User's subsequent framework:** reference is the foundation: a complete
description of relevant software at the right granularity, including abstract
concepts and relationships, so that it builds an accurate mental model. A fact
is not explanation merely because it helps readers understand a concept. At
first order, how-tos should follow entity lifecycles; cross-subject processes and
other operational tasks can also need guides. Explanation, when warranted, covers
overarching why and so what, not a duplicate explanation for each reference
subject or a repository for neglected conceptual reference. Evidence is needed
for design rationale. Grice's maxims are the proposed overarching framework;
information typing can inform presentation and reader context but does not
establish truth, structural boundaries or completeness. These principles are a
research specification, not approval to edit how-tos, pages or rules.

**User clarification:** the eventual algorithm should help a person make
reliable content-placement decisions—specific pages and sections—while applying
Grice at the level of the entire documentation set and every sublevel. The
current tree is a proposal, not proof that this objective is achieved. Accuracy,
coverage and organization require source evidence and evaluable judgments;
the quality framework alone does not decide them.

**Maintainer quality:** the user distinguishes “is it true?” from “is it easy
to keep true?” The latter informs generated docs, drift checks and simple,
sound information architecture across the documentation set and sublevels.
Generation is only as reliable as its source, scope and validation; it does
not automatically establish backend truth or require maximal reuse.

## 1. Purpose and scope

Reference documentation should let its readers identify Juju's subjects and
predict supported behavior under the stated conditions. Similar subjects should
have similar forms where the system warrants it; different subjects should not
be forced into a single template. The goal covers the whole reference, including
entities, relationships, processes, mechanisms, interfaces and provider-specific
behavior—not just the 35 selected error-counter pages. These are provisional
classifications, not a mandated taxonomy.

Two different guarantees are needed:

1. **Behavioral accuracy:** definitions, scope, conditions, results, errors and
   timing agree with the supported software path.
2. **Structural predictability:** the organization places related contracts in
   identifiable, linked locations and is consistent across genuinely similar
   cases. A *semantic address* is a location that can be linked to, whether a
   page, section, anchor or generated entry.

Code can establish the first and provide constraints for the second. It does not
always decide a unique physical page or prove readers find a particular layout
faster. The currently proposed skeleton is in `work/global-skeleton-119.md`;
this draft records its obligations and counterexamples, not an approved rewrite.

## 2. Evidence and inclusion

- Trace claims to a supported reader-facing or explicitly scoped inspection
  surface and the relevant implementation; qualify actor, target, conditions,
  timing and observation where they affect the result. Internal implementation
  may explain an exposed behavior, but an internal table or independently varying
  value alone does not establish user relevance.
- Distinguish the request, accepted state change, agent/worker/provider action,
  and eventual observation. A returned identifier, status, event or schema row
  is not automatically evidence of downstream success.
- Derive subject and contract distinctions from identity, dependencies and
  actual behavior—not source package names, database ownership, existing page
  layout, filename counts, or a reader question alone. Questions check relevance
  and coverage, not the owner, boundary or ordering.
- Client-agnostic reference pages state the platform/API contract first; CLI,
  Terraform, dashboard and other clients are examples or separate interfaces.
  An interface's syntax, selection, local state and errors remain qualified to
  that interface. Generated help alone is not proof of backend behavior.
- Explicitly record unsupported, untraced and blocked scopes rather than
  silently treating them as absent. A synthetic probe demonstrates only what it
  exercised; a source path is not a live controller/provider result.

**Session 126 follow-up — proposed causal-role principle.** Treat a notion as a
character when its coherent role is needed to understand multiple contracts and
is not adequately explained as an aspect of one participant. Treat it as a leg
when it is adequately explained as an aspect or relationship of a particular
subject. A substantive cross-subject abstraction may coexist with constituent
characters; a broad category alone does not absorb them. Multiple uses are
supporting evidence, not a numeric test, and a character need not have multiple
consumers. The source constrains the judgment but does not mathematically force
granularity or establish reader benefit. This is a proposed methodological
refinement discussed with the user, not a tested universal rule or approval to
change reference pages, the skeleton or repository rules.

Classify provisionally when traced contracts establish the role and no material
contrary evidence is known; state supported surfaces, limits and the inference.
Reopen for evidence that changes the role, not merely because a broader category
or an equal-facts layout can be imagined. Continue investigation if a material
alternative remains insufficiently traced. Apply and challenge this principle
against other cases before claiming it makes the algorithm generally complete.

Applied to E75/E76, the proposed classification is a **pool character**: its
provider configuration participates in machine root-disk and managed-storage
allocation, neither of which alone explains that role. GCE disk-type behavior is
provider-specific; the machine deletion trace remains partial. Storage may also
be a meaningful umbrella; its existence does not alone demote the pool. This is
a reasoned proposal, not a source-forced theorem or an approved page edit.

**Session 127 challenge:** E77–E79 apply the principle to allocator and backup
(`work/causal-boundaries-127.md`). The sequence allocator is provisionally a
model-database leg and a shared mechanism across machine/storage identifiers;
its traced supported role is transaction-bound internal numbering with
privileged inspection, not an independently established managed subject. This
does not make independent management a necessary character criterion. Backup
has a controller-scoped interaction and a substantive cross-subject abstraction
across model/controller exports and inventoried object reads; these roles can
coexist. Neither physical page choice nor reader benefit follows from source.
The augmented candidate passes all 11 E71 outline criteria on these provisional
judgments, not as finished or held-out content. Full family coverage remains
blocked; continue to challenge material boundaries.

## 3. Proposed organization procedure

The decision tree and decision-and-evidence record in
`work/content-planning-decision-tree.md` are an unapproved research proposal,
not a user-adopted replacement for the current preregistration discipline. The
user asked for protection against confirmation bias; distinguish source evidence
from the tree's architectural judgments and do not count old cases as proof.


1. **Define the contract and participants.** Identify what varies, what depends
   on what, the actor, supported surface, inputs, state, effects, observation and
   relevant failure boundaries. A character is a subject-level notion; a leg is
   its dependent aspect. Derive their relationship from software behavior, not a
   numerical threshold or any single identity, table, operation or lifecycle.
   A shared abstraction over notions on multiple pages is a separate reason for
   a page: establish its actual common semantics, not just a repeated word.
2. **Separate different contracts.** Distinguish subject identity from an
   interface's selector; declaration from a realized application binding;
   shared behavior from interaction-specific validation; state from observation;
   and platform rules from provider/client-specific branches.
3. **Assign linkable homes.** Propose an address for each relevant contract and
   retain local conditions and errors with the actual interaction. Use reuse
   minimally: usually help readers build the shared mental model, but an isolated
   provider-page workflow can warrant repeating applicable common material. Check
   applicability; do not impose one-home-only, always-repeat or always-reuse.
4. **Choose page or section from the classification.** A character or an actual
   cross-page abstraction can warrant a page; a character's leg belongs with it.
   Investigate uncertain relationships and preserve unresolved cases. Two layouts
   expressing the same facts and links do not by themselves make classification
   an unconstrained editorial tie. Once the semantic level is established,
   preserve stable addresses and anchors when choosing implementation details;
   a table, method or independently changing value alone does not force a page.
5. **Choose the applicable internal form.** For entity entries, preserve the
   user's settled causal order as applicable: definition/scope → relevant
   records/invariants → change streams → actors → interactions → configuration
   and failure indexing. A vocabulary prerequisite may appear before the fact
   that uses it. The roles are conditional, not mandatory headings or a claim that
   every event follows a database→watcher→actor chain. Processes, tools,
   provider intersections and generated entries use their own causal forms.
6. **Place diagnostics and figures by contract.** A call's guard, result and
   errors stay with that call; a process step's failure stays with the step.
   Figures belong with the structure, dynamics or interaction they actually
   explain. Preserve established anchors and figures until a specific edit is
   approved; do not infer a complete error contract or diagram from the form.

## 4. Acceptance obligations, not a claim of success

A proposed reference design is reviewable only when it has:

- a connected map of subjects, relations and shared mechanisms, with supported
  surfaces, conditions, source evidence, explicit exclusions and unresolved
  coverage; path counts are accounting aids, not semantic completeness;
- a proposed address and applicable form for each covered contract, plus links
  and an honest disposition for gaps, rejected claims and page-level ties;
- a per-page disposition across the agreed scope, preserving anchors, errors and
  diagrams, with the 35-page selected error count kept distinct from the full
  reference goal;
- discriminating challenges registered before new testing, with failures and
  post-hoc readings retained and previously studied paths not counted as
  held-out; and
- shared human/AI contributor guidance and mechanical checks limited to what
  they can actually verify. No new documentation/rule changes follow from this
  draft; obtain approval after the structure is settled.

The prior E44 comparison did **not** establish a structural benefit: it did not
meet all registered criteria and lacked an equal-content control. The original
E59 four-case challenge failed; later disk-inspector evidence was post hoc and
credential/provider aftermath remained inconclusive. E60 had contaminated SSH
cases. Later bounded passes do not prove global coverage, reader benefit or a
unique filename (`structure-discovery-plan.md:393-421,2028-2073`).

## 5. Proposed regression cases

These cases use already studied evidence and are not held out. E71 applies them
to the actual candidate in `work/structure-review-123.md`; a pass there applies
to the outline only, not completed rendered documentation. A cited source trace
does not by itself verify a placement, and equal facts do not settle page level.

| Case / evidence | Required result | Fails if |
|---|---|---|
| **Action vs administrative exec:** `apiserver/facades/client/action/operation.go:32-98,215-261,296-311`; `domain/operation/state/start.go:101-194,197-276,516-617`. | A common operation/task contract can represent both unit and machine tasks. Charm-action initiation and exec retain their distinct targets, guards and per-target errors; `pending` is not completion. | Every task is said to target a unit, machine exec is called a charm action, or enqueue is presented as successful execution. |
| **Endpoint declaration, application binding, relation:** `domain/application/state/application_endpoint.go:341-378,398-433`; `domain/relation/state/relation.go:80-111`; `work/endpoint-boundary-111.md`. | Preserve the distinction between a charm's declaration, an application's realization/binding and a relation composing participants. Link the contracts without assuming unique physical pages. | A charm definition is equated with the application-specific binding, or an endpoint is equated with a relation. |
| **Model identity vs DB REPL selection:** `domain/schema/controller/sql/0007-model.sql:25-59`; `internal/worker/dbrepl/worker.go:277-335`; `work/operational-boundaries-e64.md`. | Name plus qualifier uniqueness is distinct from `.switch` name-only selection and `.open` UUID selection; flag the unresolved ambiguity. | Claim model names are globally unique, or claim `.switch` reliably disambiguates owners. Do not choose a row absent ordering evidence. |
| **Hook timing:** `internal/worker/uniter/remotestate/watcher.go:685-688,720-729`; `internal/worker/uniter/resolver.go:362-390`; `work/story-form-110.md`. | A conditional watcher-driven path may be described, but a timer can initiate `update-status` work. | Assert all hooks begin with a controller database change and watcher. The timer case does not establish every other trigger. |
| **Storage lifetime:** `work/filesystem-lifetime-114.md:7-17,21-48`, including source and synthetic real-helper probe. | Distinguish instance, attachment, filesystem and model-owned EBS-backed volume on the traced forced-machine path, with provider/force limits. | State that every filesystem storage instance dies with its host, or promise cloud data survival, detachment or reattachment from the trace. |
| **Credential update:** `domain/credential/service/service.go:323-373`. | Auth-type compatibility and per-model cloud-connectivity validation are distinct; the traced per-model validator returns no errors without testing connectivity. | Assert this update path proves each model can reach its cloud. This is a proposed correction, not an approved doc edit. |
| **Distinct space refusals:** `domain/schema/model/4.0.15-model-release.ddl:1365-1375`; `apiserver/facades/client/spaces/rename.go:19-37,59-67`; `work/db-refusal-103.md`. | Distinguish a constraint's foreign-key reference to the space name from the facade's separate prohibition on renaming `alpha`. | Move or reattribute the constraint-related database refusal merely because the facade checks a different rename rule. The old review conflated these; `space.md:136-146` separates them. |
| **Credential schema diagram:** `domain/schema/controller/sql/0005-cloud.sql:183-191`; `docs/juju.ggarch:175-180,3792-3801`. | A model that exposes primary-key flags must represent both `cloud_credential_uuid` and `key` as members of the composite primary key. The current credential view hides fields. | Treat the key alone as the complete primary key or claim the current figure visibly shows the bad field marker. This is a queued model/generator discrepancy, not an authorized fix. |
| **Shared task status:** `domain/operation/service/query.go:21-36,71-103,106-130`; `work/operation-task-boundary-121.md`. | Distinguish the observed synthetic service result and the unresolved implementation/contract question from a promise of intended semantics. | Treat `pending` for an aborted-only task as proof that work will resume, or claim this was observed in a live controller. Existing `action.md:209` already records the fallback. |
| **Equal-facts physical placement:** `work/boundary-rules-e63.md:47-65`; `work/operational-boundaries-e64.md:35-51`. | Determine character versus leg and any cross-page abstraction from actual software behavior. Equal facts and links alone do not make page versus section arbitrary; record unresolved classifications. | Treat equal expressibility as sufficient to bypass classification, declare a layout factually false solely from its physical page, or call statement/link counts a reader-performance result. |
| **Blocked individual hook commands:** `work/content-planning-slice-relation-120.md:9-19,114-129`. | Mark individual `relation-set` details and the other denied hook-command scope incomplete; keep hook metadata validation distinct from command availability. | Present the family outline as complete per-command behavior or route around the 402 denial. |

A future test should register its question, competing predictions, falsifiers,
threshold and caveats before inspecting the new path; identify contamination and
report failed or inconclusive results. The decision-tree replacement is proposed,
not adopted. Mechanical tests may check anchors and links, but a source-message
match alone does not establish that a particular call returns a message/code.
Reader benefit remains unproved.

## 6. Explicit blockers and proposal boundaries

`WorkloadModel`, `HookCommandPages` and `KubernetesCloudAttributes` were denied
with 402 and must not be relaunched or worked around. Their incomplete scopes
remain gaps in the global goal. Other open code/contract or applicability leads
include DB REPL name selection, status-history kinds, aborted-task aggregation,
image priority, annotation results, dashboard behavior and provider/version
discrepancies; consult `TODOS.md` before public wording. Do not silently
resolve a possible code defect by changing prose.

The existing `page-recipe.md` and `docs/agents/AGENTS.documentation.rules.md`
contain older rules, including a reader-question ownership premise. The later
user direction is recorded in `structure-discovery-plan.md:7-20` and the
proposed reconciliation in `work/application-disposition-115.md:55-61`. Neither
this draft nor that comparison changes the current repository rules. JUJU-10585
(reference structure), JUJU-10586 (client-visible errors) and JUJU-9635 (figures
and process) remain separate criteria within the one integrated PR.
