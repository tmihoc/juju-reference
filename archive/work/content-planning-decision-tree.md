# Content-planning decision tree

**Status:** unapproved research proposal. The user asked whether to switch and
later clarified they had not confirmed; the earlier adoption claim was wrong.
The tree and its classifications are working judgments, not a proven universal
algorithm or approval to change the research workflow, reference, skeleton,
figures, rules, checker or source. The three-epic plan, denied scopes and
existing approval gates remain in force.

## Purpose

Derive a connected reference plan from relevant software behavior. For every
material decision, return a provisional semantic address and its page, error
and figure consequences, or an explicit unresolved decision and next useful
source check. A **semantic address** is a linkable page, section, anchor or
generated entry; it is not necessarily a separate file. A **contract** is a
relevant rule, identity, behavior, observation or interface condition. A
**character** is a subject-level notion; a **leg** is an aspect or relationship
adequately explained through a particular subject.

The branches guide architectural judgment. They do not infer correct granularity
from counts, infer absence from a limited search, establish reader benefit or
force a unique filename. Multiple roles can coexist: a database mechanism may
also be a shared abstraction; an overarching concept need not absorb constituent
characters. A character need not have multiple consumers or independent user
management. The source is evidence for the judgment, not a proof of it.

## Decision tree

Apply this to a connected slice, not separately to every source noun. Preserve
the outcome and evidence in the candidate using the record below.

1. **Is the proposed decision material?** Can it change a relevant concept,
   relationship, claim, semantic address, condition or linked consequence?
   - **No:** retain as background; do not start an investigation merely to
     classify it.
   - **Unknown:** identify what decision could change, or park it as a lead.
   - **Yes:** continue. Existing paths, reader questions and current page names
     help identify relevance and coverage, not ownership or ordering.
2. **What contract and evidence are involved?** Identify participants, actor,
   scope/version, supported user or inspection surface, inputs, state, result,
   timing and failures as applicable. Distinguish request, recorded change,
   later worker/provider effect and observation.
   - **Insufficient or blocked:** record exactly what is missing and the best
     next check. Do not infer that a concept is irrelevant because it lacks a
     direct command: a relevant abstraction can explain exposed behavior.
   - **Sufficient for the decision:** separate established facts from inference;
     continue. Do not claim a live outcome from a source trace.
3. **How does the notion relate to the participants?** Ask independently:
   - Can a particular subject adequately explain it as that subject's aspect or
     relationship? If yes, propose a **leg** and name that subject; retain each
     participant's conditions for multi-party relationships.
   - Does it have a coherent subject-level role not adequately explained as an
     aspect of one participant? If yes, propose a **character**. Multiple uses
     may support this, but are neither necessary nor sufficient.
   - Is there a substantive common contract across subjects, beyond a repeated
     name? If yes, propose a **shared abstraction** and state its common rule
     and participant-specific differences. It may coexist with a character or
     leg; a broad category by itself does not settle the level.
   - Are roles a process, tool/interface, provider intersection, observation or
     catalog instead or as well? Record the actual behavior and applicable form;
     do not force every entry into character/leg headings.
   - If a material alternative remains inadequately traced, **investigate or
     mark unresolved**. Do not turn an imagined equal-facts layout or broader
     umbrella into contrary evidence by itself, or turn equal expressibility
     into a blanket page/section tie.
4. **Is the proposed address justified?** Compare the strongest materially
   different account against the actual role and evidence. Record why the
   proposed semantic level fits, its limitation, and what evidence could change
   it. Classify provisionally once the traced contracts establish the role and
   no known material contrary evidence remains. Reopen when evidence changes
   that role. If the semantic level is settled but physical placement remains a
   choice, state the choice and tradeoff without claiming source forces it.
5. **What changes follow?** Propose create/update/link/investigate, with affected
   subjects and anchors, applicable internal form, conditions and errors, and
   figure question/model/accessible alternative if relevant. Preserve existing
   anchors and figures until an approved cutover. State platform/API semantics
   separately from CLI syntax and client rendering. Keep call-local guards,
   results and errors local; use shared material minimally and repeat applicable
   facts where a verified isolated-reader need warrants it.
6. **Is the decision ready to use?** Check that the candidate represents the
   supported contract, competing account, relevant differences and links, and
   does not conceal defects or claim untraced behavior. If not, return to the
   precise missing decision or check; if blocked, say by what. A provisional
   proposal is not finished content or permission to edit. Carry the full
   reference family scope, and mark blocked/untraced areas instead of narrowing.

For applicable entity entries retain the user's causal order: definition and
scope → records/invariants → change streams → actors → interactions →
configuration/failure index. These are conditional roles, not mandatory
headings; processes, tools, provider intersections and catalogs use their
actual forms. A vocabulary prerequisite may precede a fact that uses it.

## Decision-and-evidence record

Keep this compact record in the candidate or its existing subject artifact,
not a mandatory second ledger. One record may cover a connected set of decisions.

```text
Decision and affected addresses:
Evidence: source/revision, supported surfaces, conditions, limits:
Strongest material alternative; what evidence would distinguish it:
Judgment: provisional / unresolved / blocked; rationale and contrary evidence:
Consequences: pages/links and preserved anchors; errors; figures; next check:
```

Before inspecting a new path, write the decision and competing account plus the
specific evidence that could change it. Then record surprises, counterevidence,
failed predictions and post-hoc observations honestly in the same place; revise
the judgment when warranted. Trace only what can change the decision or
consequences. Use a formal controlled experiment or runtime check when the
question genuinely needs one; neither numbered experiments nor a score of
passes is a default deliverable. Prior failures, contamination and denied
scopes remain in the historical records, not erased by the new method.

## Critical assessment: what is not established

The tree may make the decision, evidence and uncertainty easier to inspect. It
has **not** been shown to produce better boundaries, reduce bias, save time or
improve reader outcomes compared with a simpler source-grounded decision record.
The three records below were constructed from cases already studied and from
the same judgments used to write the tree. Reproducing them is a circular
consistency check, not independent predictive evidence.

The central branches ask whether one subject *adequately* explains a notion and
whether an alternative is *material*. Those words name a judgment, but the tree
does not yet give an independently reliable way to make it. For example, both
pool and sequence allocation connect machine and storage. The pool's directly
selectable policy and allocator's database-internal numbering are real
differences, but the draft does not establish why those differences necessarily
make the pool a character and the allocator a database leg. A model-scoped
policy account of pool or a shared-subject account of sequence can be stated
without denying the traced facts. This is a limitation of the decision rule,
not newly discovered evidence that the provisional pool classification is wrong.

The rule to classify when no contrary evidence is known is vulnerable to a
shallow search: lack of a discovered objection is not proof none exists. A
tree can also anchor investigators on its existing categories and give a false
impression of precision. A compact evidence record without a tree might retain
the benefits of explicitly presenting alternatives with less overhead; it too
could miss important alternatives or relevant concepts. Neither approach is
shown superior here.

A meaningful future comparison would use the same genuinely less-studied,
source-grounded decisions for both methods, identify meaningful alternatives
before scoring, check source claims and unresolved cases, and retain failures;
the earlier denied scopes cannot be reused or worked around. Compare decision
quality and effort rather than output counts. Even agreement or disagreement
would not by itself establish reader benefit or universal correctness. No such
comparison was run, and it should be undertaken only if it would inform a real
workflow choice under the prior registration discipline.

## Worked records using existing evidence

These are reapplications of already studied source, not independent tests or
new runtime observations. They illustrate different branches and the unresolved
route; they do not prove the tree complete or settle every semantic boundary.

### Pool

- **Decision/addresses:** whether model storage-pool policy is a character or a
  leg of storage; links from storage, machine, constraint and provider.
- **Evidence:** on traced GCE paths, pool attributes participate in a machine
  root-disk request and in managed volume allocation, with a common disk-type
  rule and different lifecycles (`storage-machine-boundary-126.md:18-32,34-66`).
  Machine deletion is only partially traced; provider behavior is not universal.
- **Alternative:** an encompassing storage concept could describe both. It can
  coexist with a pool character; its mere possibility is not contrary evidence.
- **Judgment:** provisionally a pool character: the reusable, directly selected
  provider policy spans distinct allocation contracts and neither consumer alone
  explains it. This is an inference, not a mathematical consequence of two uses.
- **Consequences:** propose a pool address and affected links, retain provider
  limits and local failure timing; no page or figure edit is authorized.

### Sequence allocator

- **Decision/addresses:** how to describe numbering shared by machine and
  storage, and whether the allocator itself is a character.
- **Evidence:** both traced paths call a namespace-based allocator inside the
  caller transaction; they construct different identifiers. A privileged model
  database inspector can see the sequence state (`causal-boundaries-127.md:12-47`).
  These are bounded paths, not an exhaustive search for other interfaces.
- **Alternative:** treat the shared mechanism as an independently meaningful
  subject. A supported independent sequence policy or lifecycle could change
  the assessment; simple reuse or a table alone does not establish one.
- **Judgment:** provisionally both a database leg and shared abstraction: its
  observed role is transaction-bound model-database numbering, not merely an
  aspect of either generated identifier. This is not a rule that characters
  require independent management; a material new supported role would reopen it.
- **Consequences:** retain the existing database allocation address and link
  machine/storage IDs; distinguish migration and inspection limits. A schema
  diagram does not establish transactional or migration success.

### Operations and tasks

- **Decision/addresses:** where to describe the shared operation/task contract
  used by charm actions and administrative exec, and how it relates to `script`.
- **Evidence:** both create operation/task records and share an operation reader;
  actions use unit/leader targets and write access, exec also permits machine
  targets and requires admin/change-block checks. Per-target errors can coexist
  with an operation ID (`operation-task-boundary-121.md:9-44`). No live action
  or exec ran. Existing neutral anchors are in `script`, but current unit-only
  definitions omit the machine path.
- **Alternative:** a neutral shared operation/task address could be separate
  from `script`; existing anchors can be preserved or redirected. Clarify what
  `script` denotes and whether its actual contract adequately explains both
  initiation paths; physical location alone does not determine semantics.
- **Judgment:** shared operation/task abstraction is supported; its relationship
  to `script` and final physical placement remain unresolved. Do not invent a
  verdict from the current filename or count of callers.
- **Consequences:** keep initiation, guards, target and partial-result details
  at their calls; preserve `operation` and `task` anchors, link shared reading,
  and keep the synthetic aborted-status issue qualified. Investigate only the
  specific `script` role if that can change the proposed structure.

## Boundaries and continuity

Keep `WorkloadModel`, `HookCommandPages`, `KubernetesCloudAttributes` and
`CrayonEvaluation` blocked; do not relaunch or work around their denied scopes.
Retain E44's failure to establish benefit, E59's original failure, E74's
contamination, and E71's outline-only limitations. Source defects and pending
corrections remain in `TODOS.md`; never document them away. Actual Jira criteria
remain unavailable. No page, rule, figure, checker or source changes follow
from this method without the existing explicit approval gates.
