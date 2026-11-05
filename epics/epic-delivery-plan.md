# Integrated delivery plan: reference, errors and diagrams

**Status:** research and delivery plan, not permission to edit Juju pages, the
skeleton, diagrams, repository rules, tooling or PR, to create an agent repository,
or to push. It supersedes older sequencing suggestions in historical records.
A pasted PR-review batch preempts it. Deliver JUJU-10585, JUJU-10586 and
JUJU-9635 as separate acceptance tracks in the **one integrated PR**; do not
silently narrow the full reference to the selected 35 pages, or the error and
figure ambitions to the current increments. The user pastes the PR body.

## Principles and scope

- **Reference is the foundation:** a complete description of the relevant system
  at the appropriate granularity, including abstractions, relationships,
  entities, processes and tools, not merely API/CLI/field catalogs. Reference
  should provide an accurate mental model; conceptual description is not
  automatically explanation. Similar behaviors should have corresponding roles;
  material differences must remain visible without invented headings.
- Derive behavior and relevant distinctions from the software; use explicit
  documentation principles, purposes and constraints for placement rather than
  claim source alone dictates boundaries. Character versus a character's leg
  matters, and a demonstrated cross-subject abstraction can also warrant a page.
  A single table, ID, lifecycle, operation, repeated word or equal-facts layout
  does not decide it. Investigate material unresolved cases and preserve the
  user's Juju causal order for applicable entity roles.
- At first order, how-to guides should follow the actual entity lifecycle. Other
  cross-subject processes and operational tasks can warrant guides too. Explanation,
  when warranted, addresses overarching why and so what, not an obligatory
  parallel page for each concept or a hiding place for reference facts. Preserve
  evidence for asserted design rationale. These are principles to develop and
  apply, not an instruction to rewrite how-tos or explanation pages now.
- The user prefers **from principles** to the potentially misleading **from
  first principles**. The aim is principles giving new material a clear,
  predictable home throughout the connected set, naturally accommodating
  client-visible errors and appropriate figures. Placement alone does not prove
  source truth, coverage, findability, per-call error reachability, figure
  accuracy or ease of maintenance; those require separate evidence. Diátaxis is
  a company mandate and the existing `ibnote` links interweave categories.
  The reference itself should pass strong Gricean checks: truthful and easy to
  keep true, sufficiently complete at the stated scope, relevant to context,
  and clear and well ordered. Errors and figures support these qualities and
  need natural homes; neither is a mandatory section on every page. Test the
  actual content and evidence, not just the skeleton's ability to host them.
- Grice's quality, quantity, relation and manner are the proposed overarching
  quality framework. Information typing, including Diátaxis, can help manner and
  reader context but cannot establish truth, boundaries or completeness by itself.
  Apply the maxims through explicit source and supported-surface evidence,
  accessibility, safety, build and drift checks. Do not assert empirical
  completeness of the theory or universal applicability from Juju alone.
  The user clarified the intended destination: an algorithm that helps people
  make reliable content-placement decisions across the entire documentation set
  and at every sublevel, including specific pages and sections, applying Grice
  at each level. This goal is not evidence that the current tree or any method
  achieves it; source truth and relevant coverage still require direct evidence.
  The user adds a maintainer perspective to quality: is a statement true, and
  is it easy to keep true as the software changes? Source-backed generation,
  drift checks and simple, sound information architecture may help; none is
  automatically correct or a mandate to generate everything. Keep this aligned
  with the user's minimal-reuse and isolated-reader qualifications.
- Use reuse minimally: favor an accurate mental model; an isolated cloud-page
  workflow may justify repeating applicable common material. Verify applicability;
  no compulsory one-home-plus-links, always-repeat or always-reuse rule.
  Client-agnostic platform facts precede client-specific syntax and behavior.
- Derive general principles from each target's sources, not a fixed Juju ontology,
  heading list, programming language or mandatory profile for every version.
  A future different-codebase challenge is useful for a general helper, but is
  **not a prerequisite** for delivering the Juju-specific three-epic PR.

## Current baseline and hard blockers

- Source anchor `/tmp/juju-41-tree` at `e5db99d585`; docs worktree
  `/home/dora/git/misc/juju-tutorial-diagrams` was at `48ef1fca17` at session
  123's check. Recheck on startup; never touch the main checkout `~/git/juju`.
  PR #23661 was open/draft with that head/base at the same check. Existing
  selected-page counts 960/674/204/182 are historical measurements, not
  completeness claims. Do not widen the selected counter or PR links.
- `archive/work/structure-review-123.md` is a proposed global structure and disposition,
  not finished pages. E71's actual baseline produced 1 pass, 1 fail and 9
  unresolved; a separate provider-reuse conflict was found. Those cases are
  previously studied, not held out. E44 did not show reader benefit; E59 failed
  its registered original threshold. Preserve both results.
- `docs/scripts/check_error_contract.py` matches documented message templates
  against a global corpus of source raise forms and validates code vocabulary;
  some formats and entries are explicitly excluded. It does **not** establish
  per-call reachability, actual client mapping, trigger or remediation. Do not
  claim the current count/checker fulfills JUJU-10586.
- `WorkloadModel`, `HookCommandPages`, `KubernetesCloudAttributes`, and
  `CrayonEvaluation` were denied 402. Do not relaunch or work around them. The
  38 individual hook/action derivations and five Kubernetes refinements remain
  incomplete, as does the earlier workload scope. Full-epic completion cannot
  be claimed while relevant scopes are blocked. Surface the exact missing scopes
  and request user-directed resolution when they become a delivery dependency;
  do not silently replace them or continue the same assignment elsewhere.
- Potential source/contract issues, especially DB REPL same-name selection,
  status-history kinds, aborted-task aggregation, annotation result shape,
  image priority and provider/version discrepancies, remain in `TODOS.md`.
  Investigate or report them; do not document away potential defects. The
  credential diagram model has a composite-key mismatch, but the current view
  hides fields: no visibly incorrect key marker has been established.

## Critical path: fastest safe sequence

### 1. Settle the reference structure before editing it

**Current candidate:** E77–E79, in `archive/work/causal-boundaries-127.md`, propose
the sequence allocator as both a shared abstraction and a model-database leg,
and backup as both controller-scoped and a cross-subject abstraction. These
are source-grounded provisional judgments, not proof or authorization to
edit. The augmented candidate explicitly reassesses E71 as 11 bounded outline
passes, none held out or finished content. Pool remains a provisional character;
preserve GCE/provider limits and E76's partial machine-deletion trace.

**Method status:** `archive/work/content-planning-decision-tree.md` is an unapproved
proposal, not an adopted method. The user asked about switching but clarified
that they had not confirmed and asked for protection against confirmation bias.
Prior short preregistration discipline remains in force pending a user decision.
Do not assume that a decision tree is effective merely because it can encode
existing judgments. Record competing accounts, limits and counterevidence.

**Next bounded step:** address the user's bias concern first, and use existing
evidence to identify what the proposed tree does and does not establish. Any
future challenge should compare it fairly with a simpler alternative on cases
not selected to favor it. Retain all scope, defect, denied and approval gates.

**Exit:** one coherent, source-backed structure and page/section consequence map,
with applicable forms, stable-address/anchor strategy, supporting evidence and
explicit unresolved/blocked areas. Investigate remaining material uncertainties;
if a denied scope prevents global settlement, say so and obtain user-directed
resolution instead of claiming it settled. Only after settlement present the
specific page, structure and rule edits and obtain explicit approval.

### 2. In parallel with structure research, prepare—not implement—the other tracks

Read existing source traces and work products once and attach error and figure
implications to the same candidate boundaries. No denied-scope substitution, new
checker, ggarch/model edits, page edits or repository-rule edits. This overlap
avoids tracing the same call or diagram twice while respecting the approval gate.

- **Errors:** specify a source-revision-bound per-call evidence record: supported
  entry point and version, actor/guard, reachable error path, client-visible
  message template and code, trigger, remediation, source evidence and
  uncertainty. Distinguish whole-call versus per-item failures and API versus
  CLI-local/rendered errors. Reuse the existing checker as a limited template and
  vocabulary check, not proof of association.
- **Figures:** specify how a selected figure follows an evidenced structural,
  dynamic or interaction question; identify underlying ggarch model/view,
  source/version, visual grammar, accessible alternative, and contributor/feedback
  path. Check proposed schema facts against actual DDL, including composite keys;
  do not imply a hidden model defect is visibly rendered. Compare existing guide,
  selected views and pending feedback before prescribing new work.

**Exit:** a small source-backed task/evidence map per track and the exact changes
needed after approval. This is preparation, not a claim the tracks are done.

### 3. Obtain approval for the concrete cutover, then deliver in integrated slices

Once the structure is settled, present the actual page moves/sections, preserved
anchors and figures, source-traced corrections, rule changes, checker and diagram
work for explicit approval. Checker-script moves and the ggarch tasks await the
user's word; do not combine this approval with permission to push. If a defect
needs code change or a denied scope needs resolution, report that separately;
no prose-only workaround or implicit scope reduction.

After approval, apply the agreed structure and validated corrections in cohesive
subject slices, reusing the source/evidence record for all three tracks. Start
with the settled storage slice if it remains the best demonstrator; then cover
all affected selected pages and broader reference families according to the
approved disposition. Preserve link targets/figures, test generated-publication
mechanics rather than hand-editing overwritten output, and account for every
pending item as applied, explicitly deferred with the user's agreement, or
blocked. The 35-page counter remains the same separate measurement.

Implement only the approved per-call enforcement and figure/model improvements;
run a real changed-path smoke and appropriate regression checks. Validate each
claim and cite revision/source in inspectable evidence; don't infer reachability,
provider success, timing or remediation from a template match, a diagram or
an accepted request. Independent review traces source rather than rubber-stamping
its own draft; confirm key findings. Check actual diagrams in light and dark,
alt text, links, `ggarch check`, and Sphinx `dirhtml` and `latex` builders; build
PDF if the agreed acceptance requires it. Confirm feedback and contributor
process with evidence, not just a guide file.

### 4. Verify each acceptance track, then finish the one PR

| Track | Completion evidence required; open areas are blockers, not passes |
|---|---|
| **JUJU-10585 — reference** | Applicable full reference families and the agreed page disposition have source-grounded subject/relationship boundaries, appropriate conditional roles and links, preserved anchors, and accurate relevant content. Abstractions/processes/tools count; inventories or existing page names do not establish semantic completeness. Report source revision, supported surfaces, untraced/denied cases and failures. The user-approved concrete changes are applied and independently reviewed. |
| **JUJU-10586 — errors** | For each call in the agreed client-visible scope, record reachable message/code, trigger and actionable remediation, including per-item results, supported version and any uncertainty. CI detects a changed or missing association in the covered scope, not just existence of a message elsewhere. Exercise positive and negative fixtures: wrong-call same message, changed/deleted message or code, missing evidence, and explicit unsupported/unresolved cases. Demonstrate what remains outside enforcement; never mark it verified merely because a checker passes. Existing selected counts are not a coverage target or proof. |
| **JUJU-9635 — figures/process** | Figure selection is source-grounded and recorded, relevant diagrams use an editable shared ggarch model with correct source-derived facts, visual grammar and readable layout, accessible equivalent text, and checked builds. Validate model/views and inspect actual output. Contributor guide and feedback process are usable, with actual feedback evidence or an explicitly open acceptance item—not a claim of completion without it. |

Before calling an epic complete, reconcile against its actual Jira acceptance
text as well as these working obligations; if the Jira record is unavailable,
state that limitation and do not invent its wording. Verify the PR's actual
head/base and all three track outcomes, preserve the single integrated PR and
existing selected links, and provide the user a precise PR-body draft for them
to paste. Check before every push and obtain approval; never push material that
reveals security issues except hardening-style warnings. If any blocked scope or
acceptance criterion remains unresolved, report that honestly and do not call
full delivery complete.

## Agent/tool choice is not on the critical path

Develop the documentation requirements and evidence first. Crayon's inspected
writer says to mirror sibling structure and say once/link elsewhere, and its
planning derives homes from existing docs; those defaults conflict with our
method. Its signoff gate was exercised only in a synthetic repo, while its review
and evaluation scope remains 402-denied. Do not adopt Crayon's method unchanged,
claim it cannot be extended, or build a duplicate ledger by assumption. Later,
a bounded comparison may determine whether its process can be reused; a separate
implementation is only a candidate if integration requires overriding core
behavior. Existing `docs/agents/` covers general docs, clouds, `doc.go` and
landing pages too; no agent repository, tool move, rule retirement or cutover is
authorized by this plan.

## Session-to-session discipline

Each session starts with `NEXT-PROMPT.md` and `HANDOFF.md`; read the current plan,
relevant evidence, `TODOS.md` and preregister any investigation before source
inspection. Keep a short active result, next discriminating question, exact
blockers, approvals and verification state; append decisions and evidence to
`archive/SESSIONS.md`, not a new inventory. Update the live queue and next prompt when
new user decisions supersede old ones; retain archived prompts and failures.
Check preview port 8003 before starting, confirm listener and HTTP 200, and stop
the session preview. Check worktree/tracking, PR API, source anchor and existing
selected counts at startup; report only checks actually run. At close-out update
handoff/log and next prompt, archive the prompt, commit only the session's archive
records locally, and never push without approval.
