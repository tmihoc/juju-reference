# Change set for docs/reference/status.md (cold run 1)

Format per the procedure step 9: action | file and section | category | requirement | confidence. Each line cites findings (findings are in the final report because the Write of findings.md was refused by the tool).

| Action | Home | Category | Requirement | Conf | Findings |
|---|---|---|---|---|---|
| Delete figure `status.png` and its sentence | status.md, Application status | reference | R26 (redundant, never sole carrier) | determined | F25-F30 |
| Rewrite application derivation: order, ties, empty case, leader-set | Application status | reference | R6, R27 | determined | F8-F10 |
| Correct unit workload table (unknown, terminated, error); add who sets what | Workload status | reference | Quality | determined | F5-F7 |
| Correct and extend agent table; add `rebooting`, `failed`; correct who sets | Agent status | reference | Quality, Quantity | determined | F11-F16 |
| Move and correct the start-up note into a section; add the removal sequence | new section "Status during unit start-up and removal" | reference | R10, R17 | determined | F1-F4, F31 |
| Add Kubernetes pod overlay | new section "Workload status on Kubernetes" | reference | R7 (surfaced in `juju status`) | determined for content, open whether it belongs here (Q2) | F31 |
| Drop `<workload>/<agent>` form | Unit status | reference | Quality | determined | F17 |
| Name printed sections and columns; drop SLA in sample | Status in the output of `juju status` | reference | Quality | determined (SLA), open (rest of the sample needs a live run) | F18, F19 |
| Remove metalanguage and "Types of status" heading; scope the lede | whole page | reference | Manner | determined / open(Q1) | F20-F23 |
| Keep anchors `status`, `application-status`, `unit-status`, `workload--charm-status`; add `agent-status` | whole page | reference | R15 | determined | F24, B2 |
| Update `html_meta` description | front matter | reference | Quality | determined | F35 |
| Release-note or redirect | none | n/a | R23, R15 | no removed page; `status.png` removal needs no redirect | determined |

## Backlog (gaps that predate any development)

- Client developer view of status values (T8), F32.
- Remediation for `error` and `blocked` (T3), F33.
- Statuses of machines, models, relations, storage, tasks: separate pages or this page (Q1, Q2), F20.
- Regenerate the sample from a real 4.1 run, F19.
- `docs/reference/hook-command/.../status-set.md` and the Go help text say "see the status reference page https://juju.is/docs/juju/status" (status-set.go:60-61); the URL was not verified.

## Chunks examined and left unchanged

- `(status)=` label and `reference/index.md` link: unchanged.
- The dropdown wrapper for the sample: unchanged.
