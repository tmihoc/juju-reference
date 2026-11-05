# Blind-structure runs: do the questions and maxims give the entity grammar? (2026-11-05)

Two cold runs at upstream 4.1 `52e983a435` with the section grammar withheld. Inputs: the contract and the rule ledger with the grammar rows removed, plus upstream. Residual leaks: the question list still says "call" and "error" (T3, T8), and upstream's own pages and labels were readable.

## Result

| Page | Sections the run chose | Entity grammar sections reproduced |
|---|---|---|
| `status` (non-entity) | lede; unit status; workload status; agent status; unit status from deployment to removal; application status; status in `juju status` | none expected; the structure is sensible for a non-entity page |
| `relation` (entity) | lede; peer relation; non-peer relation (subordinate, `juju-info`, non-subordinate, cross-model); rules for establishing a relation; relation ID and key; relation status; relation settings | **None by name.** No `X database schema`, no `X calls`, no `X change streams`, no `X and model migration`. |

## What this shows

1. **The questions and maxims do not by themselves produce the entity grammar.** The `relation` run grouped by sub-subject and by question (kinds, rules, identity, status, settings). The grammar groups by source artifact class (records, watchers, calls, migration).
2. **The content is mostly the same.** Facts the grammar puts under "schema" appear under ID and key, status and settings. Facts it puts under "calls" appear under rules for establishing. What is missing: change streams (watchers) and migration, because the question list has no question that yields them (T5 is only partly used).
3. **Two axes, two justifications.** Grouping by reader question follows Quantity and Relation. Grouping by source artifact class follows Quality on the maintainer side: a change to the database schema lands in one section, a change to a facade in another (R10, change coupling). The grammar is justified by the second and by uniformity across the set (a predictable home for a reader, for an AI and for a maintainer); it is not derived from the questions.
4. **Where the run could not decide:** exclusive types (peer against non-peer is exclusive; the other kinds are not provably so); where `juju-info` lives (source owner says application, reading path says relation; two measures disagree); a fragment kept only because a label has an inbound link (R15); where rules end and the call's errors begin (Q5); who owns relation status (Q1).
5. **A proposed addition to the question list, from the run:** "who may do it, and what does the refusal say?" (it called it T11). My separate proposal for T11 is "how does a client or agent learn that it changed?" (change streams). They are different questions; renumber when added.

## Open question this creates

Which grouping serves readers and maintainers better is empirical. The tests: the task scenarios (does an AI-mediated reader get the right action from each structure?) and a maintenance test (apply a past development: how many sections does the change touch under each structure?). Neither has been run.
