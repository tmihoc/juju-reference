# E82 and constrained placement: session 129

Research only; not a settled algorithm or permission to change pages, figures,
rules, checker, source or PR. Baseline: PR worktree `48ef1fca17`, source
`e5db99d585`. Existing evidence is repeatedly studied, not held out. Diátaxis
and existing `ibnote` cross-category links are constraints, not competing
preferences. See `knowledge-structure-118.md`, `subject-map-112.md`, E70/E81,
`storage-boundary-114.md` and `causal-boundaries-127.md` for bounded source paths.

## Candidate procedure and decisions it does not yet settle

For each claim, record (1) purpose: reference describes what is true and the
conditions; how-to directs a task; explanation supplies evidenced overarching
rationale; tutorial teaches through an exercise; (2) subject and participants;
(3) role: identity, relation, mechanism, interaction, observation or figure;
(4) supported version, actor, scope, timing and result; (5) prerequisite facts,
and existing links, labels and emitted HTML addresses. This is a working input
form, not a replacement ontology or new inventory. A claim may support more than
one purpose, with purpose-appropriate wording and links.

**Reject a candidate**, rather than score it, when it conflates demonstrably
different actors, conditions or stages; asserts behavior beyond evidence; loses
an applicable context, existing address/figure or mandated category/ibnote; or
places a client-specific/local error as an unconditional platform fact. If
compatibility mechanisms have not been tested, mark the candidate conditional,
not passed. Unknown truth or scope is unresolved, not proof of absence. Preserve
request errors versus per-item errors versus later status or provider failures.

**Compare survivors** by explicit objectives: (a) coherence—subject, causal
prerequisites and boundaries remain intelligible throughout related pages;
(b) access—each participant and relevant guide/command has contextual entry
points, without treating links as proof of findability; (c) maintenance—avoid
unnecessary independent copies, identify source/generator and drift scope, and
retain changes locally when conditions differ; (d) compatibility—minimize and
verify address and figure disruption. Actual truth, coverage, relevance and
clear wording must be checked in the content at set, family, page, section and
statement level: passing a placement filter is not a Gricean pass.

**Operational parent candidates:** list (i) each participant, (ii) an existing
neutral subject/process containing the entire supported scope, and (iii) a new
neutral subject only when neither existing candidate can express it without
misleading scope. Parent-specific facts remain at that participant's relevant
interaction. Compare actual content, context and addresses rather than assuming
that a shared name or number of callers creates a new subject. This inclusion
rule is a value judgment favoring existing coherent subjects, not a source law;
a new neutral page may still be preferable, so do not discard it merely because
an existing one can be made to work.

**Operational page/section candidates:** for a coherent subject, compare a
standalone page against a linkable section in each plausible parent using the
same facts and local interactions. A section must introduce the subject and
scope without implying the parent is its only participant; a page must introduce
its dependencies and provide paths to each participant. Count required address
preservation work and independent copies, and enumerate—not score away—extra
navigation/context. There is no justified threshold for subject independence,
acceptable indirection or amount of context, and no defensible numerical weights
for these objectives. Thus this procedure generates and filters placements but
cannot yet reliably choose page versus section. When objectives conflict, leave
the decision open and identify evidence which could distinguish them. Source
can disprove a scope, not choose one equal-content layout as uniquely optimal.

## One connected candidate against the actual PR

Paths below are under `docs/reference/` unless noted; named new anchors are
proposals only. Existing labels must survive with their meaning. This overlay
retains the broader map and `causal-boundaries-127.md` dispositions, including
sequence under `database` and the provisional pool/backup judgments.

| Case and dependencies | Candidate page / section; links and tradeoff | Error and figure obligations |
|---|---|---|
| Controller composition versus shared agent engine: controller nodes, controller/model/unit agents and worker engine. | Keep controller-specific composition and worker examples at `controller.md#controller-workers`, link `agent.md#agent-workers` for shared engine/dependency semantics and `#controller-agent` for controller agent; keep model-specific engine context under `agent.md#model-agent`. Preserve controller `manage-controllers` and agent `bootstrap-a-controller` / `manage-machines` ibnotes. An agent-only composition alternative gives shared engine one place but obscures controller-specific arrangement; controller-only duplicates common engine behavior. Existing statements need source review; E47 failed its original single-owner worker criteria. | Keep bootstrap errors with `controller-bootstrapping` and actual client boundary, not with shared engine. Preserve controller schema and `Bootstrapping a controller` figures; they do not prove worker topology. No additional figure mandated. |
| Action and administrative exec share operation/task records, not initiation guards. | Working candidate: preserve `script.md#task` and `#operation` for neutral task/operation subject, with shared schema/status there only if `(script)` meaning and old addresses are resolved; action definition/initiation at `action.md#action-running`; exec at `action.md#action-running-commands` until a neutral interaction home is justified. Retain action's `manage-actions`, `ops:manage-actions`, `tfjuju:manage-actions` ibnotes, task/operation guide ibnotes and machine-guide exec path. Action-only shared records or a new neutral page remain viable; `script` might be misleading. | Keep write/receiver/definition errors for action enqueue, admin/change-block and per-target errors for exec, read and per-ID errors for inspection. A pending task is not completion. Preserve `Action database schema`, `Running actions`, `Task status` views and contextual caption/alt; their correctness and full call scopes remain unverified. E82 below limits relocation. |
| Storage attachment relates instance, unit and machine-side backing; owner is distinct. | Propose linkable `storage.md` section `storage-attachments` (new label, not existing), alongside `storage-pool` and a proposed `storage-instance` label; link participant `unit` and `machine` and preserve `storage-attaching` / `storage-detaching` interactions. Keep `attach-storage`, `reuse-storage`, `detach-storage` ibnotes. Another participant-owned section can contain the same qualified contract with reverse links; a distinct file is not forced. | Keep attach's whole-call write/change-block and per-item guard errors at `storage-attaching`, detach's separately scoped errors at `storage-detaching` (`storage.md:239-298`; reachability/codes still need source checking). Preserve `Storage database schema` with verified accessible text; schema alone cannot show asynchronous removal. Do not repeat the unqualified filesystem lifetime claim or promise provider detach/data survival. |
| Migration is a model operation and multi-controller process. | Keep initiation and initial errors at `model.md#model-migrating`; keep process at `model-migration.md#model-migration-phases`, `#model-migration-drivers`, `#model-migration-database-schema`, linked from `controller` and `model`. Preserve `migrate-a-model` and `tfjuju:migrate-a-model` ibnotes. Source/controller ownership alone does not justify moving all process material to `controller`; a model section could contain it but must represent source and target. | Distinguish request/precheck failure from later migration status at the relevant step (`model.md:192-225` is existing prose, not a verified complete error contract). Preserve phase/slides and database ggarch views and their captions/alt; validate against source separately. Sequence conversion links to database and migration subject are version-scoped, not a live continuity guarantee. |

These are exact candidate addresses, not executed moves or guarantees. Proposed
new labels and corresponding full URL compatibility need review after approval.
Reference concepts are not automatically explanation; lifecycle guides and
cross-subject guides remain linked in the mandated categories.

## E82: rendered baseline changes the compatibility analysis

E82 was registered before inspecting these PR bodies or rendered IDs in this
session. Prior E70/E81 study and earlier source reads contaminate it. The running
cached dirhtml preview returned HTTP 200; its actual `/reference/action/` HTML
contains `section id="action-database-schema"`, `section id="running-commands"`
and `span id="action-running-commands"`. `/reference/script/` contains heading
IDs `script-task`, `script-operation` and separate `task`, `operation` spans.
Thus direct full addresses include `/reference/action/#action-database-schema`
and `/reference/action/#running-commands`, not just MyST labels. A label moved
to another page cannot by itself keep the old page's fragment target. Retaining
an old target plus contextual link, or an actually verified fragment-aware
redirect, is needed. Which is feasible and best is not yet tested. The HTTP
server does not receive fragments, and HTTP 200 does not establish navigation.
This is a compatibility constraint, not proof against relocation: retaining the
current action home avoids that specific relocation burden but needs a neutral
semantic entry point; moving can also preserve old URLs if properly implemented.
No alternate layout or redirect was built; the selection remains a tie.

**New baseline defect candidate:** `action.md:176` declares `(action-task-status)`
before its `ggarch` directive and `:244` links to it. In the served HTML that
link is `#action-task-status`, but the parsed page has no element with that ID;
the figure appears in `section id="canceling-action-tasks"`. A fresh dirhtml
build also succeeded and its output had one link and zero matching IDs. This
does not prove every builder/version or authorize a fix. A 200 response cannot
detect it; preserve the figure and working `#canceling-action-tasks` /
`#action-cancelling` addresses as well.

After the follow-up registration, the cached Sphinx doctree was inspected with
the actual `docutils` node classes: its `ggarch` node carries both ID and name
`action-task-status`. The installed extension's `GgarchDirective.run` returns a
custom node (`ggarch/sphinxcontrib_ggarch.py:83-85,109-136,173`); the single-view
HTML visitor constructs `<figure class="...">` directly without emitting that
node's IDs (`:893-905,1018-1058`). This explains the observed missing HTML ID
on the successful rendered path; it is not an audit of slides, other builders,
all directives or ggarch versions. No fix was applied.

## Order and new-claim challenge

A manual application—not an automated reproducibility test—processed (A)
controller→execution→storage→migration and (B) migration→storage→execution→
controller against the fixed candidate list above. The named addresses do not
change because each row evaluates all participant and neutral homes against the
same global constraints, rather than committing the first encountered parent.
This is a property of this written candidate, not evidence independent authors
would make the same judgments; no independent run occurred.

Add the already known E70 claim that exec may target machines, then rerun the
execution row: `script.md`'s unit-only definition fails truth/scope, while the
candidate must cover machines; the controller, attachment and migration rows
need no address change. This is a known, deliberately selected perturbation,
not a new source discovery, general stability guarantee or reason to erase the
`script` meaning. A newly discovered cross-subject contract could legitimately
change multiple related homes; unknown thresholds and objective weights still
make output path-dependent in actual human application.

## Three independent acceptance tracks

* JUJU-10585: validate actual reference claims and full supported family
  coverage, including purpose/category and all sublevels. Known `storage.md:14`
  and `script.md:15,24` conflicts show the existing content does not yet pass;
  incomplete denied scopes prevent a completeness claim.
* JUJU-10586: trace each supported call/version through its client-visible
  message, code, trigger, remediation and result boundary; design and exercise
  association-level drift detection after approval. Existing template checker
  and 960/674/204/182 counts cannot prove reachability or coverage.
* JUJU-9635: validate each selected view's source/model, caption, alt text,
  visual rendering, grammar, shared editable model and contributor/feedback
  process; E82's missing target demonstrates that figure placement and a build
  alone are insufficient. No universal figure requirement follows.

Actual Jira acceptance text remains unavailable; `WorkloadModel`,
`HookCommandPages`, `KubernetesCloudAttributes` and `CrayonEvaluation` remain
402-denied and must be resolved only by user direction. No reader study, live
controller, cloud, RPC or provider exercise took place. E44/E59 failures and E74
contamination remain. The required resolution is a discriminating, preregistered
challenge for page/section decisions and actual fresh HTML target behavior,
not adoption of a threshold by fiat.
