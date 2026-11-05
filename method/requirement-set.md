# The documentation requirement set (draft, session 130 continuation, 2026-11-05)

**Status:** proposal for review, not an approved change to any page, rule, tool or the PR. It collects the conclusions of the investigations to date, tests them for consistency, and marks every entry as derived, user-given, settled in practice, or open. Open entries name the missing understanding and the test that would supply it; they carry no default ruling. Source references use the 4.1 anchor (`/tmp/juju-41-tree` at `e5db99d585`) and the PR worktree at `48ef1fca17`.

**Aim:** make Grice applicable without impressions. A maxim becomes applicable when it names (1) the object assessed, (2) the standard it is compared with, (3) an observable test, and (4) a failure that can be recorded. Section 1 does this for each maxim. Section 2 lists the requirements, each with the fact that makes it follow. Section 3 checks them against each other. Section 4 lists what is still unknown.

**Entry format.** Each requirement has a statement, the maxims it serves, the maxims it costs (where a trade-off is known), its grounds (the fact about the product, the readers or the maintainers from which it follows), a status, and a test. A maxim named on a requirement needs its own test from Section 1; a maxim with no test is dropped from the entry until one exists. Status values:

- **Derived:** follows from other entries and stated facts.
- **User-given:** a decision or mandate by the user, with its date where known.
- **Settled in practice:** applied across the PR and checked mechanically or by review, without an independent test of benefit.
- **Open:** the grounds are incomplete.

## 1. Grice, made operational

The maxims apply at five levels: the whole documentation set, a family of pages, a page, a section, and a statement. The same four questions apply at each level; only the object changes.

| Maxim | Object assessed | Standard | Observable test | Recorded failure |
|---|---|---|---|---|
| **Quality** (true) | A statement | The 4.1 source, the supported surface, or a recorded probe | Trace the statement to code with file and line; name the evidence class (source path, synthetic probe, live run) | Contradicted, untraceable, or true only under a condition the text omits |
| **Quality, maintainer side** (easy to keep true) | A statement or section | A single extractable source and a drift check | Does one generator, checker or single source exist for it? What changes in the code would falsify it? | No source, several hand copies, or no check |
| **Quantity, sufficiency** | A set, family, page or section | The questions a named audience asks at the relevant level (open: Q1) | Enumerate the observable behaviors and surfaces in scope; count which have a statement | A behavior a named reader can observe and the set never states |
| **Quantity, minimality** | A statement | The same question set | Remove the statement; does any question lose its answer? | A statement that answers no question |
| **Relation** | A statement and its home | The question this page or section owns | Name the audience, the question, and why this location owns the answer | Answers another page's question, or restates a fact owned elsewhere |
| **Manner** | A statement, section, page or the set | Form properties that serve human and AI readers and maintainers | Mechanical: the page-rules checker, link and build checks, ggarch check. Reader performance: untested (E44 gave no structural evidence) | Violates a rule, or is unclear to a reader in a test |

Consequences that keep the table honest:

- Placement and form cannot establish truth, completeness or findability. Those need the source evidence, the question inventory and the reader evidence named in the table.
- The mechanically checkable columns are Quality, the maintainer side, and part of Manner. Sufficiency, minimality and relation depend on the question set, which is Q1 below.
- A pass on one maxim at one level says nothing about another level.

## 2. Requirements

### A. Scope: what `docs/` holds

**R1. Locality sets the tier.** Document a fact at the smallest scope where it can be accurately documented. A fact that a package can own goes into that package's `doc.go`. A fact that no single package can own goes into `docs/`.
- Maxim: Quality (accuracy needs the owner's context), Relation, and the maintainer side (the nearest owner keeps it true).
- Grounds: `AGENTS.doc-dot-go-rules.md` states the locality principle. The dissolved `docs/contributor/` tree is its application: content moved down into `doc.go` files or up into `docs/`. The Dqlite core-dump guide and the guide for compiling and running agents on different architectures moved up because they span packages.
- Status: user-given, applied in practice.
- Test: for any fact, find the smallest package scope that can state it truthfully; if none, it belongs in `docs/`.

**R2. The audience test differs by tier.** `docs/` holds what no lower document can own, for any named audience. `docs/reference/` additionally applies the surface-and-prediction test of R6 and R7. A Juju developer is an audience of cross-package how-tos and explanation, such as the Dqlite and compile guides, labeled as developer content.
- Maxim: Relation.
- Grounds: derived from R1 plus the existing rule that how-to guides may keep a labeled developer corner (`AGENTS.documentation.rules.md`, "What Goes On a Reference Page").
- Status: derived. The earlier paradigm draft stated "Juju developers are not an audience" as a property of `docs/`; it holds only for `docs/reference/`.
- Test: each page names its audience and the tier rule that admits it.

**R3. Named audiences.** Operator, client or tool developer, charm developer, storage or incident inspector with database access, and Juju developer (cross-package procedures). The AI reader is the union; it changes how pages are written and not what goes in.
- Status: settled in practice (the first four), derived (the fifth).

**R4. Generated pages are never hand-edited.** CLI command pages, hook command pages and configuration-key pages are regenerated from source, and `make verify-docs` blocks merge on drift.
- Maxim: Quality, maintainer side.
- Status: settled in practice.

### B. Category and purpose

**R5. Each fact has one category, and links join the categories.** Reference, how-to, explanation and tutorial each carry what their purpose requires. `ibnote` links connect them.
- Grounds: Diátaxis is a company mandate, and the `ibnote` system already interweaves categories.
- Status: user-given.

**R6. Reference is a complete description of the product at the relevant level, in modular, maintainable and easily digestible chunks.**
- Maxim: Quantity (sufficiency and minimality), Manner, maintainer side.
- Grounds: user-given 2026-11-05. It extends the earlier statement that reference includes abstractions and relationships beyond catalogs of fields, calls and commands.
- Status: user-given. "The relevant level" is open (Q1).
- Test: after Q1 is answered, the exposure inventory and the question set in Section 1.

**R7. Reference admits a fact when it is true, an audience asks for it, and one of two conditions holds.** Either a reader can meet the fact on a supported surface (command output, API reply, status, log line, database tooling), or the fact belongs to a cross-cutting mechanism that a reader needs to predict surfaced behavior, stated in surfaced vocabulary.
- Maxim: Quantity and Relation. Costs: Quality if the mechanism is described without a source trace, and Manner if the description leaves surfaced vocabulary.
- Grounds: the surface test alone excludes mechanisms such as the sequence allocator and backup, which the spec proposal wants as a complete description. The second condition reconciles this with R6.
- Status: open. The second condition is a candidate (Q1) and has not been run on the allocator or backup.

**R8. Category follows purpose.** Reference states what is true and under which conditions. A how-to directs a task along the entity lifecycle. Explanation gives evidenced overarching rationale. A tutorial teaches by exercise. A subject can need distinct material in more than one category.
- Status: user-given (Diátaxis), applied in practice.

**R9. First-order how-tos follow entity lifecycles.** Other cross-subject guides are allowed. Explanation is not a parallel page for each concept and does not hold reference facts.
- Status: user-given.

### C. Chunking: pages, sections and addresses

**R10. A chunk is a set of facts that change for the same reason and answer the same reader question.** It has a stable semantic address, which can be a page, a section or a generated entry.
- Maxim: maintainer side and Manner.
- Grounds: modularity is a stated aim (R6). The definition ties the chunk to the two properties a maintainer and a reader act on.
- Status: open as an operational definition (Q2): neither "change for the same reason" nor "read together" has been measured.

**R11. An entity with its own typed ID, its own facade method and its own lifecycle is a page.**
- Grounds: the E35 to E43 studies. A group of tables whose lead table holds a NOT NULL foreign key into exactly one other page and that nothing else references is a section of that page. The audit found the rule different from "misplaced", and E37, E38 and E47 falsified mechanical boundary and worker-owner rules.
- Status: settled in practice as a sufficient condition for a page. It does not decide groups that fail it.

**R12. Separate the target's invariant, an interface's selector, and the shared contract, and give each its own address with links.** Example: a model's qualified identity belongs to the model, the name-only `.switch` query belongs to the database REPL, and the plugin `-m` and `-c` precedence belongs to the plugin interface.
- Maxim: Quality (scope), Relation.
- Grounds: E64 traced each case. A statement true of the interface becomes false when attributed to the target.
- Status: derived from the traced cases.

**R13. A notion that explains several contracts and that no single participant can explain is a character; a notion that one participant explains is a leg.** A substantive cross-subject abstraction can coexist with its constituents.
- Grounds: the session 126 proposal, applied to pool, allocator and backup (E75 to E79).
- Status: proposed, unapproved. It needs counterexample checks (Q2).

**R14. Page or section for equal content: open.** Equal facts, equal links and equal conditions can be laid out as a page or as a section (E63, E64, E82).
- Status: open (Q2). No default is set. A rule is needed only if a difference between the layouts matters; if none does, either layout is acceptable and the choice is recorded.

**R15. Preserve every address that readers and other content use.** Heading fragments, MyST labels, rendered element IDs and full URLs all count. A moved label does not preserve the fragment of the page it left.
- Grounds: external links and bookmarks exist (E82 inspected the rendered IDs). The missing `action-task-status` target is a live defect of this class.
- Status: user-given constraint, partly unmet.

### D. Ownership and reuse

**R16. Every fact has a single source.** The rendered text can appear in more than one place only when it comes from that one source (a reuse snippet or transclusion) or when an isolated reader needs it repeated. Any other mention links.
- Maxim: Quantity (no excess), the maintainer side, Manner. Costs: Manner for an isolated reader when a link replaces a repeat.
- Grounds: truth must be easy to keep. A hand copy is a second thing to keep true. An isolated reader, such as someone following one provider's workflow, is better served by a self-contained page, and a single source serves both.
- Status: derived. The repository rule "content appears in ONE location only" is stricter than this entry and conflicts with the cloud template's reuse snippets (Section 3).
- Test: for any repeated text, find the single source or record the exception.

**R17. The reader's question decides the owner of a fact.** The subject and the place in the code do not. Mentioning a fact with a link is allowed; restating it is not.
- Status: settled in practice.

### E. The entity page form

**R18. Entity pages use one section grammar.** Lede; `X database schema`; `X change streams`; `X calls`; `X and model migration`. Each section appears only when its facts exist.
- Grounds: the pilot on the `ssh-key` page, about twenty rounds of review, then 33 pages. Each section maps to a source artifact class: schema from the DDL, streams from watchers, calls from the facade. Whether this mapping explains the form's stability, and what fits no section, is Q3.
- Status: settled in practice. Not tested against readers (E44).

**R19. A call states its caller, its rules and its errors.** Errors carry the message, the code, a trigger and a remediation. Errors nest under the call that raises them.
- Status: settled in practice. The home of an error raised by several calls is Q5.

**R20. A schema rule stays only if the database enforces it or the schema fixes the allowed values.** A rule that a service, facade or worker applies belongs to the call. A record or sentence stays only if a reader meets it through a surface the page documents; otherwise hide it, contain it as a linked context record, or move it.
- Maxim: Quality, Relation.
- Status: settled in practice, checked against the consolidated release DDL.

**R21. A status's allowed values live in the schema and its transitions live in the call that changes it.** A mechanism with its own page keeps its machine there.
- Status: user-given.

**R22. Text rules.** American spelling, Oxford comma, base case first, definitions as opening sentences, one subject per sentence, a list built up to by an intro that ends in a colon, terms linked or defined at first mention, "settings" and never "databag", em dash as ` -- `, "call" for one API interaction and "operation" for a run of a script.
- Maxim: Manner.
- Status: user-given, checked by `tools/check_page_rules.py` (which lives in the archive and not yet in the repository).

**R23. Pages state the current behavior of the documented release.** They carry no scoping to that release (no "in 4.1", no `versionadded`). A fact about another version as an input to this one, such as importing a model exported by an earlier controller, is ordinary content.
- Grounds: a version note goes stale, and release notes and per-version docs carry it. The conflict with E79 and E82 came from reading the traced-path caveat as page content; it does not need a version scope on the page.
- Status: user-given (rule) and derived (the distinction). The upgrade guide is the existing example.

**R24. Pages are client-agnostic.** The platform contract comes first. A client, such as the CLI, Terraform or the dashboard, appears as an example, or as a separate interface page that the call links.
- Grounds: R12.
- Status: user-given, derived for the placement.

### F. Errors and figures

**R25. Errors are a separate acceptance track (JUJU-10586).** Each documented error is traced to one call, one client-visible message and code, a trigger and a remediation. The checker `check_error_contract.py` matches messages against a corpus of raise forms; it does not establish reachability, attribution or remediation.
- Status: user-given. Counts 960, 674, 204 and 182 are documented entries and not an audit.

**R26. Figures are a separate acceptance track (JUJU-9635).** One shared ggarch model has one view per figure; the caption carries the takeaway and the alt text the inventory; a schema figure shows records and a sequence figure shows software; a figure is checked against its source, caption, alt text, rendering and the build.
- Status: user-given. The E82 finding shows a figure can exist while its anchor target is missing.

### G. Necessity

**R27. New content is justified when the set lacks a fact an audience asks for or states it wrongly.** The test compares the fact against the set before and after, for the supported version. It separates missing, inaccurate, inaccessible, redundant and already adequate. Exposure alone does not make content necessary, and absence from one page is not absence from the set.
- Maxim: Quantity, Relation. Costs: Quantity (over-flagging) when "incomplete" has no materiality test.
- Grounds: derived from R6 and the Quantity row in Section 1. E83 added the rule that a statement owes the reader only what its own scope claims: a statement is affected only when the development contradicts it, extends an enumeration it makes, or changes an outcome it promises. Silence about a new fact is not a defect of the statement.
- Status: derived. It depends on Q1 for the question set. No audit of the PR's additions exists; E44's `ssh-key` comparison is a lead and not proof.

## 3. Consistency check

| Conflict | What conflicted | Resolution | Status |
|---|---|---|---|
| Charter scope | The paradigm draft said `docs/` documents only what the code exports, yet the Dqlite and compile guides sit in `docs/howto/`. | R1 and R2: locality sets the tier; the surface test applies to reference. | Resolved, derived |
| Surface test against completeness | R7's first condition excludes unsurfaced mechanisms; R6 requires a complete description. | The second condition of R7. | Candidate, awaiting Q1 |
| One home against reuse | The repository rule allows one location; research and the cloud template allow repetition. | R16: a single source with possibly several placements. | Resolved, derived. The repository rule's wording needs amending once approved. |
| Level decided against tie | R11 treats the level as derived; E63, E64 and E82 treat it as a tie. | R11 is a sufficient condition for a page; R14 covers the remainder. | Partly resolved; the remainder is Q2 |
| Version scoping | R23 forbids it; E79 and E82 mention version-specific conditions. | R23: the page states current behavior; another version appearing as an input is content. | Resolved, derived |
| Client-agnostic against interface selectors | Entity pages are client-agnostic; E64 places selectors with the interface. | R24 with R12. | Resolved, derived |
| Section grammar against mechanisms | The entity grammar has no slot for cross-cutting mechanisms, the actor, or relationships. | None. | Open, Q3 |

## 4. What is not yet understood

Each item names the missing understanding and a test to register before running. Thresholds are set before inspecting data; earlier studies of the same cases are contaminated and are not held out.

**Q1. What is the relevant level, and what is the question set?** (E83 result: the question set needs templates by audience, now T1 to T8 in `method/docs-decision-procedure.md`; ports and removed surfaces were missing from the first list, so the list is not complete.)
- Candidate: the least detailed model that lets a named audience predict every supported observable behavior. Sufficiency is the predictions covered; minimality is the statements that support none.
- Test: take the exposure inventory for one bounded family and list the observable behaviors of the allocator and backup that need each mechanism. If no behavior needs it, R7's second condition excludes it; if some do, it includes it. Falsifier: a behavior the model predicts incorrectly, or an included statement that no prediction needs.
- Also settles whether reference serves a developer through observable behaviors (R2) and gives R27 its question set.

**Q2. What does the level change, and does it follow from change-coupling and reading paths?**
- A page or a section changes the address, the scope the parent implies, the navigation unit and the maintenance unit.
- Candidate measures: which facts change together in the git history of the source and the docs, and which pages readers reach together (inbound links, search paths where available). E64 registered a similar topology metric and did not run it on real history.
- Test: for the four connected cases (controller and agent engine, operation and task, storage attachment, model migration), compare the layout each measure predicts with the current layout. Falsifier: the measures predict no layout difference, in which case R14 stays an acknowledged tie with a recorded choice. I have not checked whether the history supports this.
- The character and leg principle (R13) is tested in the same step against a counterexample.

**Q3. Is the section grammar determined by source artifact classes, and what fits none?**
- Hypothesis: each section of R18 corresponds to one extraction source (DDL, watchers, facade, migration export).
- Test: map every section of the 33 entity pages to its source, and list the facts that fit none (actor, relationship, cross-cutting mechanism, process). Falsifier: sections whose facts come from several artifact classes, or common facts with no section.
- If confirmed, the form is stable because each section is mechanically maintainable, and the missing slots are where non-entity facts need their own forms (the 117 skeletons).

**Q4. Does reference serve a Juju developer through the observable behavior only?** Answered by Q1.

**Q5. Where does an error raised by several calls live (for example a bootstrap failure)?** The form nests errors in calls; the error epic wants how-tos to link to entries. Needs a trace of one cross-call error from raise site to client rendering before choosing a home.

**Q7. When a development adds a mechanism that several surfaces use, which category carries it?** Resolved for the SSH proxy (`method/evidence/ssh-documentation-decision.md`). A mechanism that has its own records, calls and configuration is a reference page of the entity grammar. A competing explanation page is split statement by statement; it survives only for rationale that the behavior or the source evidences, and the SSH page had none. The general rule is now step 4 of `method/docs-decision-procedure.md` and is a candidate for R8.

**Q8. What is the unit of a development?** E83 treated one commit as a development (C6) and found it an intermediate step of a series. The unit is the merged PR or series; the boundary of a series is not yet defined.

**Q6. Do the watcher method names in 16 reference pages belong?** They are facade method names on the API wire, so they may meet R7's surface condition. The standing preference is against naming Go watcher methods. Decide by checking whether each is client-visible.

## 5. What this document does not establish

- It does not establish that any proposed rule makes the reference pass Grice. Passing needs the tests in Section 1 on the content.
- It does not establish reader benefit; E44 gave none and E59 failed its threshold.
- It does not approve a page, rule, tool, figure or PR change. The four denied scopes, the Jira acceptance text and the approval and push gates stand.
