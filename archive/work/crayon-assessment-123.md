# Crayon assessment — session 123

**Decision:** use Crayon as the first candidate workflow to evaluate, not build a competing agent now. Its planning and writing instructions overlap substantially with the proposed helper; whether its review can satisfy our independent review requirements is unknown. A target-specific, source-checked specification and integration checks may be needed, but neither a separate bot nor a fork is yet established as necessary. This is a proposal, not permission to create a repository or alter tools, rules or pages.

**Later assessment, superseding the integration-first recommendation above:**
start from our own Grice-grounded requirements and source-investigation method;
do not adopt Crayon's inspected method unchanged. Its writing instructions say
to mirror siblings and state a fact once with links elsewhere
(`skills/crayon-write/references/writing-standards.md:91-97`), while dynamic
planning samples nearby documentation and proposes homes from the current tree
(`skills/crayon-plan/references/context-bootstrap.md:14-38`). These conflict
with source-derived boundaries and the user's qualified reuse decision. Its
completeness check covers plan items and promised inventories, but does not
establish that the plan covers the full conceptual system. Locate/confirm/
corroborate is useful, but a second signal alone does not prove call reachability,
conditions, messages or remedies. The writer asks for file:line claim evidence
in its report while the specified `origins` are plain repository-relative paths
(`writing-standards.md:57-74`; `skills/crayon-write/SKILL.md:363-378`). The
inspected `crayon.py:4790-4878` makes `--report` optional and validates report
shape, not claim truth. These are instruction/code observations, not an agent
trial. The denied review/evaluation scope remains unexamined; do not conclude
it lacks capabilities. Do not rebuild Crayon's workflow by assumption: after
our specification is developed, assess reuse or extension only if useful; no
new implementation or repository is authorized. See `epic-delivery-plan.md`.

## Scope and evidence

Clone: `~/git/crayon`, public `canonical/crayon` revision [`437a4196fcbba24354df9c00ab366862dd6ac144`](https://github.com/canonical/crayon/tree/437a4196fcbba24354df9c00ab366862dd6ac144). The existing destination was checked absent before cloning. Tool 0.2.0, contract 1. This assessment reads the architecture, context, planning and writing surfaces and selected deterministic tool checks. **The review skill, rubric, evaluation cases/scripts and related error/diagram review coverage were assigned to `CrayonEvaluation`, denied 402; they remain unexamined.** Do not relaunch or work around that denial. Thus this is not a full review of Crayon, nor proof of the absence of functionality in the unexamined scope.

- **Instructions:** planning starts with context and adjacent docs, asks for intent and audience, derives a docs-tree placement and allows multiple signed targets (`skills/crayon-plan/SKILL.md:68-83,97-143,161-176`). Writing starts with declared sources, may navigate freely, calls for locating and corroborating claims, and requires promised inventories to be read and materialized (`skills/crayon-write/SKILL.md:298-319`). These are agent instructions, not proof an agent follows them or produces accurate, complete output. The plan also requires human signoff. Crayon's reference intake defines accurate, complete descriptive machinery but its examples are mostly interface/field inventories (`skills/crayon-plan/references/reference-intake.md:5-24`); examples do not establish that abstractions, relationships or processes cannot be described. Its stated neutral reference stance and division between lookup reference and explanation may need explicit alignment with a reference that builds an accurate mental model; no conflict is established without a real trial.
- **Deterministic checks:** `crayon.py:578-638` accepts only docs-relative `.md` and `.rst` targets; `:3834-3849,5010-5051` checks recorded signoff before draft. The architecture says one unit at a time, a hash-chained provenance ledger, local commits and no build/push/publish (`docs/architecture.md:9-47,53-63`). Scope these guarantees to Crayon's workflow; a recorded signature or file digest does not establish source truth. Context records identify five recognized context names and allow external source records (`docs/context.md:11-24,35-52,70-96`); context drift is reported, not refused. The writing instructions identify origin files and gaps but the report is not, by itself, proof of a per-claim trace (`skills/crayon-write/SKILL.md:356-390`).
- **Actually exercised:** C2 in `structure-discovery-plan.md` used the real pinned CLI in a disposable synthetic Git repo. Before simulated signoff `draft` refused `no_signoff`, leaving the target absent and state declared; after signoff the same draft was accepted. No AI skill, review, Juju model, controller or provider ran. The temporary repo was removed. This session did not repeat that smoke.

## Three acceptance tracks

| Track | Overlap and remaining evidence | Smallest next check |
|---|---|---|
| JUJU-10585: source-derived reference structure and planning | Crayon can plan multi-page units, record project context and instruct source-grounded reference authoring. Existing-doc placement is useful context but is not sufficient evidence for Juju's first-principles boundaries. It is not established that the skill cannot derive abstractions, relationships or a coherent global map; a single unit workflow does not itself demonstrate cross-reference consistency. | After authorization, use the same explicit target revision and a source-derived plan/spec as input to a bounded Crayon planning trial across comparable and contrasting subjects; inspect actual plan and evidence, not examples. Preserve the user-set Juju causal order and unresolved scopes. |
| JUJU-10586: client-visible per-call errors | Crayon's reference intake mentions error-code lists, source grounding and promised completeness. A signoff or origin-file list cannot show that a particular call returns a particular code/message under a trigger, or that remediation is sound. The existing Juju checker is only an increment, not the desired per-call drift enforcement. Review/eval coverage was denied, so do not claim Crayon lacks it. | Specify per-call source-to-client message/code, trigger and remediation fixtures including negative association and drift cases; compare existing checker and Crayon integrations once denied review scope is explicitly unblocked. |
| JUJU-9635: figures and contributor process | Crayon targets `.md`/`.rst`; a shared `.ggarch` model cannot itself be a signed target in that path. This does not rule out external tools, references, integration, or extension. Native source-grounded shared-model authoring, visual grammar, accessibility, figure selection, feedback and build verification have not been demonstrated here; review/diagram coverage was denied. Crayon architecture states it does not build. | Specify source-to-model invariants and figure selection, editable model/visual grammar, alt text, both builders and contributor feedback. Investigate an external ggarch/build step and integration before proposing a fork or duplicate bot. |

All three tracks remain distinct in the one integrated PR. The current selected-page counts do not establish any epic's completeness.

## Grice and integration

Grice's quality (truth/evidence), quantity (appropriate completeness), relation (relevance), and manner (clear and orderly expression) are plausible overarching principles for human and AI contributions, including this broader reference. They do not themselves specify which source/revision proves an assertion, whether a diagram represents a composite key, if a call can reach an error, whether a figure has accessible equivalent text, if a build passes, or how a drift alert is produced. Those are operational interpretations and checks of the maxims, not a competing philosophy. The credential diagram's composite key is a concrete counterexample to treating a general instruction alone as evidence of correctness. Conversely, this assessment has not shown that Crayon plus explicit context, external checks and an independent review cannot satisfy them.

**Recommendation:** preserve one inspectable principles/evidence base and trial Crayon's existing planning/writing plus external project checks; evaluate the blocked review surface only when the denial is resolved. Prefer configuration/integration or targeted extension over a parallel helper/reviewer; choose a standalone project only if a demonstrated requirement cannot be met economically by that path. No per-version profile, common language, fixed Juju ontology or universal headings are presumed. Challenge any claimed generality on genuinely different repositories and documentation kinds. Existing `docs/agents/` also covers general docs, cloud, `doc.go` and stakeholder-directed landing pages; no replacement or retirement is authorized.
