# Rules from principles (draft v0, 2026-11-05)

**Status:** research proposal, unapproved. Direction (user, 2026-11-05): reduce the list of rules by convention as far as possible. A rule is in effect because it makes sense, and it makes sense when it falls out of the maxims and the addressee model. Some rules stay purely conventional, especially where they are bigger than docs (Conventional Commits, the PR template, the CLA). Those are listed as such and kept short.

## What counts as a derivation

A rule is **derived** when the ledger names (1) the maxim it serves, (2) the premise about the addressee it needs (`review-mode-contract.md`, Addressee model), and (3) an observable test that a violation fails. Three safeguards against rationalizing after the fact:

1. **Exclusion.** The derivation must also exclude the opposite rule. If it would justify "figure after the prose" as easily as "figure at the top", it is vacuous. (The figure-position derivation uses scope-by-position, which excludes the opposite.)
2. **Prediction.** The rule must predict at least one finding that a competent reviewer would also raise, without knowing the rule.
3. **Cost.** If the derivation names a cost to another maxim, the ledger says so.

A rule that fails these is **conventional**. A conventional rule is allowed in two cases only: it is adopted from an external standard (Diátaxis, Conventional Commits, Canonical's style guide), or it is a tie-breaker. A tie-breaker is itself derived from Manner (predictability): where several forms are equally good, one form applied uniformly spares the reader and the maintainer a decision. Every other conventional rule leaves the list.

## Ledger: figures (JUJU-9635)

| Rule | Maxim | Addressee premise | Test | Class |
|---|---|---|---|---|
| A figure never carries a fact the prose lacks | Quantity | Readers without image access exist (text export, AI, screen reader) | Figure-removal test | Derived |
| A figure earns its place only by clarity | Manner (and Quantity: a fact-free figure is excess) | A relational fact is slow to hold in prose | A reader answers a multiplicity or order question faster with it (untested) | Derived; the empirical premise is open |
| A figure sits at the top of its section, at that section's scope | Relation, Manner | Readers read position as scope | Scope of the view equals scope of the section; the prose beneath states every fact | Derived (position implicature excludes "after the prose") |
| One view per figure | Manner (one point), Quantity (excess: the whole model on every page measured 84% of `llms-full.txt`) | Isolated readers | A view with several unrelated points fails | Derived |
| Caption states the takeaway; alt text names what is shown | Relation, Quantity | A non-visual reader needs the inventory | Swap test (role swap) | Derived |
| A figure of records and a figure of software stay separate | Manner (one point per figure) | | A view mixing both fails the one-point test | Derived from the row above |
| No committed rendered images | Quality, maintainer side | A figure that cannot be regenerated from the model can drift from it | Image differs from the model's rendering | Derived |
| Colour means ownership only | Manner (one meaning per signal) | | A colour used for a second meaning fails | Derived |
| A transitions figure only if each arrow is an enforced rule | Quality | Readers act on a rule | Each arrow cites the call that enforces it | Derived |

## Ledger: text

| Rule | Maxim | Premise | Class |
|---|---|---|---|
| Definition as the opening sentence | Quantity (T1 is the first question) | | Derived |
| Base case first, then the exceptions | Manner (orderly); a literal reader reads the first statement as the rule | Literal readers | Derived |
| One subject per sentence; no comma-and clause for two facts with different subjects | Manner (ambiguity) | | Derived |
| A list is led into by a sentence that names the kind of list | Manner (orderly), Relation | A literal reader will not infer how the items relate | Derived; the closing colon is a convention |
| Terms linked or defined at first use | Quantity | An AI or isolated reader sees one section | Derived |
| One term for one meaning ("call", "operation"; "settings" not "databag") | Manner, Quality (difference in wording implies a difference in meaning) | | Derived |
| No metalanguage | Relation (the text is about the subject, not the document) | | Derived |
| No "Prerequisites" or "Tips" sections | Manner (informative titles); the content is required (T4) and integrates into the task | | Derived (the rule bans a heading, not the content) |
| Pages state the documented release's behavior, with no scoping to it | Relation (the version is common ground) | The docs are versioned | Derived |
| Client-agnostic: platform first, client as example | Relation, Quantity (the contract is what holds across clients) | Several clients exist | Derived |
| Oxford comma, always | Manner (ambiguity): without it a list can be read as an appositive ("my parents, Ada and Ben"). A writer cannot reliably spot every case while writing, so a blanket rule costs less than a judgment each time | | Derived |
| American spelling | | | Conventional, external (house style) |
| The parenthetical dash is written ` -- ` and renders as a dash distinct from a hyphen | Manner (ambiguity): a distinct glyph from the range dash and the hyphen; genre: spaced form common in web and software prose, the unspaced book form reads as stilted; the source form is plain ASCII and survives text exports and AI pipelines. A triple hyphen is too long as rendered (user) | Readers of software docs expect that genre (genre row, addressee model) | Derived. The user confirmed (2026-11-05) that ` -- ` renders fine; use it and never `---` |
| Colon placement in bold list terms (`**Term:**` or `**Term**:`) | | | Conventional, tie-breaker; upstream and our PR differ, choose one |

## Ledger: structure

| Rule | Maxim | Class |
|---|---|---|
| Four categories (reference, how-to, explanation, tutorial) | Relation: they serve different reader goals | External (Diátaxis), with a derivation |
| One home per fact; others link | Quantity (excess), Quality (maintainer side) | Derived; conflicts with the isolated reader (open) |
| "Types of X" for exclusive alternatives; "X architecture" for coexisting parts | Manner (a title says what kind of statement follows) | Derived |
| A call states its caller, its rules and its errors | Quantity: T3 and T8 | Derived |
| An error has message, code, trigger and remediation | Quantity: a reader must recognise it, understand it and act on it | Derived |
| An error nests under the call that raises it | Relation | Derived for single-call errors; multi-call is Q5 |
| A chunk is facts that change for the same reason and answer the same question | Relation, Quality (maintainer) | Derived; measures defined in the contract |
| Entity page section grammar (R18) | Relation, via source artifact classes | Partly derived; Q3 open |
| Conventional Commits, PR template, CLA, Jira link | | Conventional, external; cite and keep short |

## Consequences

- **The rule files shrink.** `docs/agents/AGENTS.documentation.rules.md` can state the maxims, the addressee model and the derived rules as one line each with a pointer to the derivation, plus a short list of conventions. Enumerations of "do not" items become instances of a maxim.
- **A rule with no derivation leaves.** The conventions left are few: the exact dash sequence, colon placement in bold list terms, American spelling, and the external standards. The Oxford comma and the dash form are derived (Manner, with the reader's genre expectations).
- **A new rule needs a ledger row.** A reviewer's "we should do it this way" gets a derivation or the label conventional.
- **The check and the rules coincide.** A defect type in the contract is the failure of one derived rule. A derived rule with no defect type, or the reverse, is a gap in the contract.

## Not settled

Whether the derivations survive the exclusion test when the user reads them (the user judges). The empirical premise behind the figure rule. The conflict between one-home and the isolated reader. Which conventional tie-breakers to keep in upstream's rules without a derivation, if any.
