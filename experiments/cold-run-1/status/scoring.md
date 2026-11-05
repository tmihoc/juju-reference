# Scoring sheet: docs/reference/status.md (cold run 1)

Columns: Upstream (e5db99d585) and Cold output (draft-status.md). The "Our PR" column is not filled (not an input of this run). Counting units are stated so that a second scorer can recount.

| Measure | Upstream | Cold output |
|---|---|---|
| Statements failing the source trace (text statements, counting each sentence of a claim once) | 11: F1, F2, F3, F5, F6, F11, F13, F16 (False, Stale, Ambiguous-with-wrong-actor), F17 (Unverifiable), F19 (sample), F7 (implicature), F10 (silent about display statuses). Strict count of False or Stale only: 7 (F1, F2, F5, F6, F11, F16, F19) | 0 known false. 1 flagged Unverifiable: sample rows and version `4.0.15` (J3) not regenerated. 1 partly traced to help text only: error text `this unit is not the leader` (A9). 1 simplification: Kubernetes rule 5 omits the unset case (K6) |
| Figure statements failing trace (separate count) | 8 transitions Unverifiable, 1 False (Terminated), 2 Contradicts or Unverifiable descriptions (Waiting "package installation", Maintenance "paused for event") = 11 | 0 (no figure) |
| Facts upstream had that are stated nowhere (losses) | n/a | 2 dropped for no trace: the written form `<workload>/<agent>`; the "missing or malformed config item" example. Zero true losses of facts that trace |
| Gaps against the question list | T1 partly (scope), T2 (states and order of derivation, start-up, removal), T3 (error and blocked remediation), T6 partly (lost and error display), T8 (API), T9 n/a, T10 (priority order). Count: 6 of 9 applicable | T3 (no remediation), T8 (no API view). Count: 2 of 9. T2 and T10 closed; T6 closed for the surfaces read |
| Excess statements | 4: "charm(ed) service" gloss, figure examples not in source (3 in F28), "paused/stopped" etc. Count 4 | 1 candidate: the Kubernetes overlay section (answers T6 for Kubernetes operators; would be Excess if that audience is out of scope; Q2 open) |
| Errors: traced entries; entries with a finding | Entries: 0 (no error entries on the page). Error-contract checker not run | 2 error texts quoted (`invalid status ...`, `this unit is not the leader`). Traced: 1 to raise form (status-set.go:153), 1 to help text only. Findings: 0. The per-call trace of the checker was not done |
| Figures: figure-removal test failures | 1 of 1 figure fails (Figure-only fact, Prose defers) | 0 of 0 |
| Manner findings (titles, scaffolding, mixed sections) | F20, F21, F22, F23, F24 = 5 | Self-check: lede says "Machines, models, relations, storage, and tasks have statuses with values of their own" (a non-page scope remark, acceptable); heading "Status during unit start-up and removal" fails the title test in part (the first sentence carries "new unit" terms); draft Workload section lead-in "Each value tells an operator whether to act:" is a stretched intro. Count 2 |
| Page rules and the error checker | Not run (tools not in permitted inputs). By eye against WORKING-RULES and the recipe: lede present, no figure at top of section (figure is mid-section), metalanguage 3 instances | Not run. By eye: Oxford comma yes; no metalanguage found; lists introduced by colon sentences; no "databag"; figure none. Open: the draft keeps one CLI link (F34) against the recipe's "never link CLI page" |
| Blind rank (user, 1 to 3) | | |

## Scoring uncertainties

- "Statements failing the trace" depends on what counts as a statement. The count above is one per sentence-level claim; a two-claim sentence counts once.
- Excess is judged against the question list, which Q1 says is incomplete.
