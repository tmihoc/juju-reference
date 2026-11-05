# Review mode contract (draft v0, 2026-11-05)

**Status:** research proposal, untested. Not an approved rule, method or edit. It extends `docs-decision-procedure.md` (development-driven) with a page-driven mode: given upstream's docs and the source, say what is wrong, why, and what to do, the way a competent reviewer would, and draft the fix. Every change to a page must cite a finding. A change with no finding is a defect of the run.

**Aim:** apply the Gricean check directly to upstream and produce a PR as good as or better than the current one. The current PR is a candidate, not the answer key; it has known defects (`method/evidence/audit-pr23661.md`).

## Pipeline

| Stage | Input | Output |
|---|---|---|
| 1. Extract | Upstream page; 4.1 source | Claims (one checkable statement each), figures, errors, headings, addresses |
| 2. Review | Claims; question list; requirement set | Findings (format below) |
| 3. Decide | Findings | Change set: action, home, category, requirement, confidence (procedure steps 4 to 9) |
| 4. Draft | Change set; page form (`page-recipe.md`) | Page text, traced statement by statement |
| 5. Verify | Draft; source | Trace per statement; error and figure checks; rule checker |

A cold run sees only upstream's docs, the source, this contract, the procedure, the requirement set and the page recipe. It never sees our PR or the audit.

## Finding format

One claim about one statement, figure, error or page.

| Field | Content |
|---|---|
| Where | file and line at upstream |
| Quoted | the statement, or the figure's view name |
| Type | one value from the tables below |
| Evidence | source path and line; or the page that owns the fact; or the audience question left open |
| Fix | correct, move, merge, delete, add; with home and category |
| Severity | high: a reader acts wrongly and cannot tell; medium: a reader is blocked or must search; low: costs time |
| Confidence | determined, tie, or open(Qn) |

A low-severity finding is reported only in a batch line per page. Nitpicks that change no reader's action are not findings.

## Defect types: statements and pages

| Type | Maxim | Test |
|---|---|---|
| False | Quality | The 4.1 source contradicts it |
| Stale | Quality | True of an earlier version, false in 4.1 |
| Unverifiable | Quality | No source or probe supports it |
| Not enough | Quantity | A named audience question about the subject is unanswered or half answered |
| Gap | Quantity | A fact in scope is stated nowhere in the set |
| Excess | Quantity | Removing it leaves no audience question unanswered |
| Duplicate | Relation | Another page owns the same fact |
| Misplaced | Relation | Wrong owner, or the wrong category for what it says |
| Crossed wire | Relation | The page or section answers more than one reader's question, or depends on another page's facts to be read |
| Metalanguage | Manner | The text talks about the document ("below", "this page", "the records, with the rules that apply to each, are:") instead of the subject |
| Uninformative title | Manner | A title is generic or names structure. Test: replace the title by the first sentence of its section; if the sentence carries more distinct subject terms, the title fails |
| Mixed section | Manner | The facts in a section have different owners or change for different reasons (R10) |
| Mirrors implementation | Manner, Relation | The statement is filed or worded by where the code enforces it (database, service, facade) or leaks an internal message (a raw database failure in `<reason>`), and would have to change if the check moved without changing observable behavior (refactor-invariance test, below) |
| Ambiguous | Manner | A reader can take two meanings |
| Broken address | Manner | A label, anchor or URL does not resolve and has no redirect (R15) |

## Defect types: boundaries (pages and sections)

A boundary is unprincipled when it violates R10 (a chunk is facts that change for the same reason and answer the same reader question) on evidence. The evidence is one of four measures; no single measure decides.

| Measure | How to read it |
|---|---|
| Source owner | The facts of a unit trace to one package, record or facade, or to several unrelated ones |
| Audience question | The unit answers one question of one audience, or several unrelated ones |
| Change coupling | The statements of the unit are edited together in the history (`git log --follow`, co-edit counts), or they are not |
| Reading path | The unit is entered from the same links and read in one sitting, or its parts have disjoint inbound links and the parts do not link to each other |

| Type | Test |
|---|---|
| Grab-bag page | Its sections have disjoint source owners and disjoint audiences. Example at upstream: `reference/charm.md`, with a taxonomy on five unrelated axes (substrate, function, role, architecture, generation) and an anatomy of revision and channel |
| Grab-bag section | The same test one level down |
| Split subject | One subject's facts sit on several pages with the same owner, audience and change history, and the pages link to each other for basics |
| Fragment | A page or section holds too few facts to answer a question alone and is always read with its neighbor |
| Over-fine split | Sections that no reader reaches separately, with heavy cross-links between them |
| Category mix | A page holds both what something is and the steps to use it (R8) |
| Boundary follows an accident | The unit exists because of the old file layout, a naming history, or one author, with no measure above supporting it |

The check reports a boundary finding only when at least two measures agree. When layouts are equal on all four measures the finding is a **tie** and no change is justified (E63, E64 and E82: source can disprove a scope but cannot choose a layout). Q2 stays open for the choice between a page and a section; this section decides only whether the current boundary is defensible.

## Defect types: errors (JUJU-10586)

An error is a documented entry at a call: message, code, trigger, remediation (R19, R25).

| Type | Test |
|---|---|
| Unreachable | No path from the call reaches the raise site |
| Misattributed | The raise site belongs to another call or to a worker, and the client never sees it |
| Wrong message | The client text differs from the raise form, after the code's wrapping |
| Wrong code | The client code differs from the rendering of the raise |
| Wrong trigger | The condition named does not cause the raise |
| Wrong remediation | The remediation does not clear the cause, or the reader cannot do it from the client |
| Unactionable | The entry has a trigger and no remediation, or a remediation that restates the message |
| Gap | A client-visible error of the call has no entry |
| Duplicate | The same message is documented in several places with no owner (Q5) |
| Misplaced | Error text sits in a how-to, an explanation or another call, where the entry should be the single owner and the how-to should link |
| Mixed entry | One entry joins errors with different triggers or remediations |

Placement rule (R19): an error nests under the call that raises it. For an error raised by several calls the home is Q5 and stays open; until Q5 is decided, record the finding as open(Q5) and do not move the entry. How-tos link to the entry for their step's failures (TODOS 5); they never carry their own copy of the trigger and remediation.

Per-call trace (the work the checker does not do): raise site, call chain to the facade method, error wrapping, client code, message as rendered, trigger, remediation. A finding of type Wrong message, Wrong code, Misattributed or Unreachable needs this trace as evidence.

## Defect types: figures (JUJU-9635)

**Rule (user, 2026-11-05):** a figure is redundant with the main text. It is never the only statement of a fact, never incorporated into the prose (no sentence depends on it to be understood), and never a way to avoid stating something in prose. A reader who cannot see the figure, such as an AI reading the text or a person using a screen reader, loses nothing in what the page states.

**Figure-removal test.** Delete the figure, its caption and its alt text. Does any audience question lose its answer? If yes, the prose is missing a statement and the finding is *Figure-only fact*.

| Type | Test |
|---|---|
| Figure-only fact | The figure, caption or alt text carries a fact that the prose of the page does not state |
| Prose defers | A sentence points to the figure for content ("as the figure shows", "see the figure for the transitions") or is unintelligible without it |
| Contradicts | The figure disagrees with the prose or with the source |
| Decorative | The figure shows no relation, multiplicity, order or containment that the prose does not already make easy to hold; it earns no place (R26) |
| Wrong kind | A schema figure shows software, or a sequence figure shows records (R26) |
| Role swap | The caption holds the inventory or the alt text holds the takeaway (R26) |
| Caption carries unique facts | The caption states a fact the prose of the section does not, beyond a takeaway |
| Broken target | The anchor, view name or rendered ID is missing (E82), or the view does not build in light and dark |
| Misplaced | The figure is not at the top of the section whose scope it depicts, or its scope is wider or narrower than that section (a page-level figure in a subsection, or a subsection's facts under a page-wide figure) |

Placement rule (user, 2026-11-05): a figure sits at the top of the section it embeds in, and that section's scope is the figure's scope. The figure is a redundancy, so its place is set by scope, not by reading order, and the prose beneath it still states every fact. Reason (Relation, Manner): position is read as scope. A figure placed after the prose reads as belonging to the material above it, a part of the section, so only the top of the section signals that the figure depicts the whole section. One view per figure; a view appears once per page unless a second section depends on the same records. A removed upstream figure is read as statements first (procedure, refactor mode step 1) and each statement is classified; if the prose lacks it, restore the statement in prose, then decide on a figure.

## Question list (starter; Q1 is open)

Instantiate for the named audience at the level of the page. Grown from E83 and the PR audit; it is not complete.

| Id | Question | Surfaced by |
|---|---|---|
| T1 | What is it, what can I do with it, and who may? | |
| T2 | Which states, and which follow which? | status priority order (audit) |
| T3 | What can fail, and what do I do? | |
| T4 | What must be reachable, installed, permitted or configured? | ports (E83); CMR external addresses (audit) |
| T5 | What happens at migration, upgrade, backup or removal? | |
| T6 | Where do I see it, and what does it mean? | |
| T7 | What replaced what I used? | removed `--jump` (E83) |
| T8 | For a client developer: which call, request, result, error and code? | |
| T9 | Is a number or limit a floor or a cap, and for which kinds of resource? | constraint min and max (audit) |
| T10 | In what order does Juju choose when several values compete? | status severity (audit) |

## Scoring sheet (per page)

| Measure | Upstream | Our PR | Cold output |
|---|---|---|---|
| Statements failing the source trace | | | |
| Facts upstream had that are stated nowhere (losses) | | | |
| Gaps against the question list | | | |
| Excess statements | | | |
| Errors: traced entries; entries with a finding | | | |
| Figures: figure-removal test failures | | | |
| Manner findings (titles, scaffolding, mixed sections) | | | |
| Page rules and the error checker | | | |
| Blind rank (user, 1 to 3) | | | |

There is no column for "matches our PR". A disagreement between the cold output and our PR is a finding against one of them, settled by the source trace, then the maxim test, then the user.

## Rules and errors as objects (hypothesis, untested)

A rule is a proposition. Give each rule: the proposition; its scope (every state, or one call); who is guaranteed it (every writer, or this call's path); the surfaces where a reader can observe it (the database schema through `juju-db-repl`, a read call, a write call); and the errors it produces. An error is a relation: which rule, in which call, with which message and code, and a call-specific remediation.

Placement: an invariant that a reader can meet through several surfaces is stated once at the record it constrains; a call-specific precondition at the call; an error under the call that raises it, as the main route, with a message-keyed index if Q5 requires one for readers who arrive from an error text. A rule enforced at two sites is one proposition: state it once and link.

**Refactor-invariance test.** Imagine the check moved from one enforcement site to another (a service check into a database constraint) with the same observable behavior. If the documented statement or its home would change, the statement mirrors implementation. A rule's home may differ by audience surface; it may not differ by enforcement site.

Worked case (our PR, `reference/space.md` renaming): the rule "a space that a constraint names cannot be renamed" is stated through "the database refuses the change", and the error carries `<reason>` from the database. Logical statement: a space referenced by a constraint cannot be renamed, stated once at the record, with the error referring to it.

## Addressee model

The maxims are defined relative to an addressee and the common ground (Quantity: as informative as is required for the purpose of the exchange; Manner: clear to that reader). A finding is meaningless without the addressee it was judged against, so each finding names one. The model is evidence-based and listed here; extend it only with evidence.

| Addressee | Assumed capabilities and limits | Consequence for the check |
|---|---|---|
| Person reading the page in a browser | Sees figures; scans headings; follows links | Figures help Manner; headings carry signal |
| Person using a screen reader or a text export | No image access | Prose states every fact; alt text names what the figure shows (figure-removal test) |
| AI reading a retrieved section | Often sees one section or chunk alone; no image access | Each section is self-sufficient: terms defined or linked at first use, no "see above" for content |
| Reader who takes statements literally (including non-native readers and some neurodivergent readers) | Does not reliably compute implicatures from "can", "by default", "usually", from a list, or from silence | Exhaustivity, necessity and defaults are stated ("only", "all of", "always unless") wherever they matter |
| Charm author, operator, client developer | As in R3 | Question list per audience (T1 to T10) |

Defect type for this model (Manner): **Relies on implicature.** A statement that is true only if the reader infers exhaustivity, necessity or absence the text does not state. Examples: a list read as complete, "can" read as "does", "by default" read as "always", a silent page read as "does not apply". In refactor mode a list read as complete counts as an *enumeration extended* when a member is added or removed, because the reader computes the exhaustivity from the list.

## Calibration

- Gold set 1: the defects already found in upstream (`mount-point`, the name regex, the stale agent-version troubleshooting, the HA caption's "replicaset", the status priority order, the simplestreams layout) and in our PR (`audit-pr23661.md`).
- Gold set 2: later upstream commits that fixed wrong docs statements. Run the check on the page before the fix.
- Precision: a sample of findings on pages with no known defect, judged by the user. A high rejection rate means the severity rule is wrong.
- Overfitting: tune on one set of pages and test on another.

## Not settled

Q1 (relevant level and complete question set), Q2 (page versus section), Q5 (home of a multi-call error), the threshold for the title and mixed-section tests, and whether a figure may ever be a schema's only statement of multiplicity (the user's rule says no; a prose statement of each multiplicity is the cost).
