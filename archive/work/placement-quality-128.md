# Placement, confirmation bias and generated reference: session 128

Research only. The desired result is a reliable procedure for locating content
at every level of the documentation set, including specific pages and sections,
with Gricean reader and maintainer quality. Neither the proposed decision tree
nor the simpler record is approved or demonstrated to achieve that result. The
three-epic candidate and gates in `epic-delivery-plan.md` remain in force.

## Fair comparison on existing evidence, not a trial

Compare two methods that receive the same contract facts, supported surfaces and
constraints, and that must record the same competing accounts and uncertainty:

* **Tree:** `content-planning-decision-tree.md` asks a sequence of relevance,
  evidence, role, address and consequence questions, then records a decision.
* **Simpler record:** identify the decision and affected addresses; record the
  evidence and limits, strongest alternative and distinguishing evidence, the
  provisional or unresolved judgment, and consequences. It has no prescribed
  character/leg decision tree. Existing preregistration remains in force for
  testing under either approach.

| Question | Tree: strongest case / risk | Record: strongest case / risk |
|---|---|---|
| Forgotten dimensions | Named branches can prompt consideration of shared abstractions and exceptional forms; predetermined labels can anchor and exclude alternatives. | The same evidence and counterargument fields allow an alternative ontology; blank fields do not prompt a missing participant or scope. |
| Deciding a boundary | Explicit character, leg and shared-role questions make the judgment inspectable; “adequately explained” and “material” still require the judgment they purport to guide. | Can state the best rival directly and admit an unresolved level; a record alone offers no decision rule. |
| Effort and drift | A repeatable checklist could reduce omissions; it may also add redundant classifications. | Potentially shorter and easier to modify; it may omit a useful systematic check. Neither effort claim has been measured. |
| Applicability to all docs | Roles help with reference subjects; they do not determine how-to, explanation, tutorial or nested-section placement. | Can accommodate any kind of decision; it does not derive a coherent whole-set architecture or prove coverage. |

The strongest objection to the tree is not merely its length: even faithfully
following it can assign different levels to equally defensible source-backed
accounts without a reproducible reason. The strongest objection to the record
is that logging evidence and dissent can produce a careful description of an
unreliable placement decision; it is not a substitute for an algorithm. They
share source-selection and author-anchoring bias. Neither was independently
compared, and neither has demonstrated lower bias, better decisions, lower
maintenance cost or reader benefit. The pool and allocator judgments are inputs
used to construct the tree, not its validation. Their real differences do not
force the proposed opposing labels. No new contrary source evidence about pool
is claimed.

A defensible comparison, if a method choice is materially actionable, would
pre-register the same less-studied eligible decisions, actual acceptance and
failure thresholds, equal evidence, competing outcomes, time accounting and
contamination limits before applying either method. Ensure both have access to
the same source and scope, do not select cases by their predicted winner, and
retain unresolved and failed outcomes. An independent source check can detect
false conditions or omitted effects; it cannot by itself prove that a particular
page boundary is the uniquely correct one. Agreement is not correctness, nor
would such a trial alone establish reader benefit or universal validity. No
such trial is run here; do not reuse the four denied scopes to obtain cases.

## What an eventual placement procedure must resolve

These are requirements for a research target, not an adopted algorithm or a
proof that the criteria are sufficient:

1. At whole-set and family level, enumerate supported subjects, relationships,
   interfaces, lifecycles, distinct tasks and relevant explanation questions;
   retain an explicit unknown/blocked perimeter instead of deriving coverage
   from current filenames or a complete-looking navigation tree.
2. At page level compare source-backed subject roles and competing structures,
   including a genuine shared abstraction where warranted. At section and
   statement level preserve conditional causal order, relevant context,
   applicability, stable anchors, and local call errors. State which decisions
   are unsupported or normative; source does not produce a unique filename.
3. Apply Grice at each level: quality includes source truth and how it stays
   true; quantity includes relevant coverage and limits; relation asks whether
   material belongs in that context; manner includes understandable order,
   explicit scope and accessible figures. These are review questions, not an
   independent oracle for correctness, relevance or level.
4. Keep API/platform semantics client-agnostic, CLI syntax and local errors at
   the CLI, per-call errors at the actual operation and later worker/provider
   failures at their actual stage. First-order how-tos follow entity lifecycles;
   other cross-subject guides can be warranted; source-supported overarching
   rationale belongs in explanation when needed, not all conceptual reference.
5. For each proposed generated or reused fragment identify its source,
   publication path, revision, consumers, conditions and detection mechanism;
   distinguish fresh generation, source truth and actual supported behavior.
   Minimize reuse subject to correct mental models and the possible isolated
   cloud-reader exception. A passing check has only its actual scope.

Operational stopping criteria remain unresolved: neither “adequate” nor
“material” has a reliable independent threshold for choosing character, leg,
shared abstraction or page/section. An explicit abstention with the competing
accounts and missing discriminator is preferable to turning absence of found
contrary evidence into proof. The status of the provisional pool and allocator
labels is unchanged, not newly proved or disproved.

## E80: current generator and cross-boundary quality

The actual `go run scripts/docgen.go --split --no-index --out <temporary-dir>`
produced `add-machine.md` containing the disk flag description, example and
directive text; the temporary output was removed. This exercises the CLI
generator only, not the Python wrapper, forced regeneration, `verify-docs`,
backend semantics or a live controller.

The prior nested-family research (`skeleton-nested-117.md:31-39,53-56`) already
identified these paths; a file-location search also preceded E80 registration.
This is a contaminated source-and-existing-probe synthesis, not a held-out
experiment, full generator audit or new comparison of the methods. E80 was
registered before reading the generator bodies for this session.

* At docs worktree `48ef1fca17`, `docs/scripts/autogenerate-docs.py:69-112`
  skips CLI generation when the output directory is nonempty unless `--force`
  is used; forced generation replaces the directory, runs `go run
  scripts/docgen.go --split --no-index --out ...`, adds labels and copies the
  authored index. `docs/scripts/docgen.go:9-14` invokes the tree's `documentation`
  command. The formatter renders command metadata, flags, examples and help
  (`/tmp/juju-41-tree/cmd/cmd/markdown.go:46-101`).
* `docs/Makefile:89-116` forces regeneration then checks `git status --porcelain`
  for the CLI, hook-command and two configuration-key output paths, including
  newly untracked files; `.github/workflows/docs.yml:7-12,35-44` invokes this
  and a separate error checker. This is code inspection, not an assertion that
  the check ran, is enabled in every workflow invocation, or proves semantics.
  No individual hook/action derivation was performed.
* The authored `add-machine` help includes the disk option and an example
  (`cmd/juju/machine/add.go:119-121,175-195`); the existing generated page
  contains the same flag and example (`docs/reference/juju-cli/list-of-juju-cli-commands/add-machine.md:13-19,55-57`).
  Its text claims disks can be added (`:109-110`); on the separately exercised
  v11/v12 synthetic success path the facade discarded the requested directives
  (`add-machine-disks-127.md:19-28,43-75`). This is a concrete example of
  text faithfully reflecting help while a backend contract can diverge, not a
  claim that all generation is false, that verify-docs passed, or that a live
  cloud request was tested. Investigate intended fix with appropriate permission;
  do not repair the apparent conflict solely in prose.
* The existing error checker constructs a global source-template corpus and
  matches documented entries and code vocabulary (`docs/scripts/check_error_contract.py:1-38,469-495`).
  It does not bind a template/code to a reachable particular call, condition,
  client rendering or remediation; it also only iterates direct Markdown pages
  in the supplied reference directory (`:479-482`). No checker run here.

## Connected candidate and three-track implications

* **JUJU-10585 reference:** keep the generated `add-machine` entry as the CLI
  invocation surface and propose the machine allocation interaction on the
  client-agnostic machine reference, linking storage/pool and provider-specific
  semantics. For this defect leave actual additional-disk behavior unresolved
  pending intended source fix and applicability; separate root-disk constraints
  and acceptance from subsequent provider outcome. Existing labels and links
  must survive any approved cutover. This is a bounded consequence overlay, not
  an approved or complete global skeleton. The other selected dispositions and
  broader family map remain as recorded in `causal-boundaries-127.md`.
* **JUJU-10586 errors:** a per-call record must separately cover whole-call
  authorization/change-block, per-item validation and provider-precheck errors,
  client rendering and later asynchronous failures. A result item and its error
  must remain associated; a global template match or fresh command help is not
  such evidence. Existing synthetic outcomes have the limits in
  `add-machine-disks-127.md`; no exhaustive messages/codes or remediation is
  established. Design drift enforcement after approval, with explicit missing
  and unsupported cases and negative wrong-call fixtures.
* **JUJU-9635 figures:** a proposed interaction view could distinguish CLI
  parsing/serialization, facade guards and per-item result, service/state and
  later provider, with the lost input marked as an unresolved defect rather
  than a guaranteed disk effect. Whether a figure earns its place remains
  untested; schema views cannot demonstrate the missing forwarding. If approved,
  derive a shared editable model/view from source and give accessible equivalent
  text, grammar, feedback and revision/maintenance ownership. No figure/model
  is changed; existing schema-field mismatch and hidden-view caveats remain.

Existing E44 and E59 failures, E74 contamination and E71's outline-only status
remain; the four 402-denied scopes are not reopened. Jira acceptance text is
still unavailable. No repo page, source, figure, rule, checker or counter edit,
method adoption, new repository, or push is authorized by this analysis.
