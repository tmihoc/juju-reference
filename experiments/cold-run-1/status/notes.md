# Notes on the method (cold run 1, status page)

## What worked

- Pipeline stages 1 to 3 ran directly. The finding format forced an evidence line for each claim, which made the false statements (F1, F2, F5) easy to prove against runhook.go and unit.go.
- The figure-removal test found that the old figure's eight arrows and five descriptions exist only in the image, and that no 4.1 rule enforces them.
- The defect-type table fits statements well. "Relies on implicature" (from the addressee model) fit F6 and F7 better than any other type.
- The procedure's step 3 classification (contradicted, enumeration extended) is development-driven; in page-driven mode the contract's types replaced it without trouble. "Enumeration extended" had no analogue for a page that lists values with no development; F14 used Gap with the implicature note.

## Where the contract failed or was unclear

1. **Metalanguage conflict.** The contract names "the records, with the rules that apply to each, are:" as Metalanguage. The page recipe prescribes the lead-in "The caller, the rules, and the errors are:" and a colon-ended intro before every list. The two rules conflict for list intros. I wrote intros that say something about the subject and then a colon. No rule says which of the two wins.
2. **No type for a scope claim larger than the content** (F20), nor for a stale generated artifact (F19, the sample output). Used Not enough, Uninformative title and Stale.
3. **Severity scale** has no tier between "false" and "plausible example presented as a rule" (the figure arrows, F26).
4. **Placement rule for figures** says a figure sits at top of the section whose scope it depicts. The status page has no entity and no ggarch view; the contract does not say whether a non-entity page may drop its figure when the picture is a set of charm-chosen transitions (no records, no sequence of software). R26 requires "relation, multiplicity, order or containment"; the old figure had arrows only for an unenforced pattern. I removed it and proposed none. Whether a ggarch view exists or is wanted is Open.
5. **Page recipe is for entity pages.** Sections `database schema`, `change streams`, `calls`, `and model migration` do not apply to a status page. Rules that applied: lede, no metalanguage, base case first, Oxford comma, no comma-and, no version scoping, client-agnostic, jargon links at first mention. Rules that did not apply: section grammar, Caller line, Rules and Errors groups. Reference headings "nominal and carry the entity name": "Status during unit start-up and removal" is nominal but long; the contract's title test is not decisive.
6. **Client-agnostic rule against T6.** The recipe says never link a CLI command page; the page's subject includes what `juju status` prints. I kept one link as an example (R24 permits a client as an example). Marked a tie (F34).
7. **Question list lacks a remediation template for status values** (what do I do on `blocked` or `error`). T3 covers errors of calls, not state values. Used T3 loosely.
8. **No place to record "partly traced to help text only"** (A9). The contract says trace to source with line; a help-text example is a documentation string, not the raise site. I recorded class H.
9. **Boundary check**: with two measures needed and change coupling not measured (git history out of bounds for the permitted commands), B1 stays a tie by construction.
10. **Scoring sheet** has one column for "statements failing the trace"; figure statements and text statements need separate counts, and the Upstream figure alone carries 11 of them.

## Ambiguities I resolved without a rule

- Order of the workload table. Base case first (active) against the contract's T10 (severity order). Chose base case first in the table, severity order stated in prose once.
- Whether to keep the `Kubernetes` section. R7 allows it (a reader meets the overlay in `juju status`). Q2 open for page versus section.
- Whether the sample may be edited without a live run. I removed only the SLA column (provable) and flagged the rest.

## Process problem

- The Write tool refused to create findings.md in the output folder ("Subagents should return findings as text, not write report files"), although the task asked for that file. It accepted change-set.md, trace.md, scoring.md, draft-status.md and this file. I did not work around the refusal; the findings table is in the final report instead, and change-set.md refers to finding ids F1 to F35.

## Time sinks

- Reading uniter and domain/status code to establish the start-up sequence and the Kubernetes overlay: about half of the effort. The overlay logic (status.go:477-540) is the hardest to state precisely and needed a simplification (K6).
- Locating which facts the old figure carried: the image read was quick; deciding which arrows were facts rather than examples took the longest conceptual step.
- No tool in the permitted inputs for the page-rules checker or the error checker, so the "Page rules" row is by eye.
