# PR description: what each epic's lens let the PR cover (v0, 2026-11-05)

Draft material for the PR body of `4.1-docs-reference-principles`. The user writes and pastes the body. Every item below is backed by a finding in `method/evidence/` or `experiments/`; items marked (claimed) are the cold agents' claims, not yet traced by the parent. Written for the base `4.1`. The items describe what the PR will cover once the changes land; no page on the new branch has been changed yet, and each claim about the new pages is a target, not a fact.

## Why going deep reaches wide

A shallow review of `status.md` finds a stale sample and a missing figure. Tracing each statement to source found, in the same page, a wrong start-up state, a wrong trigger for `unknown`, a wrong meaning for `terminated`, and an application priority order that was never stated. Two independent cold runs, each with no knowledge of the other, reached about 80% the same defects.

## JUJU-10585: the reference paradigm (principles that give each fact a home)

| Maxim | Covered because of the lens | Evidence |
|---|---|---|
| Truth | Every statement traced to the 4.1 source, with file and line | `status.md`: new units start `waiting/allocating`, not `maintenance/allocating` (`domain/application/service/unit.go:989-1009`); `unknown` follows the start hook (`runhook.go:259-268`); `terminated` follows the remove hook (`runhook.go:254-258`). `secret.md`: the name regex validates content keys (`core/secrets/createsecret.go:110`); the Vault option is `mount-path` (`internal/secrets/provider/vault/config.go:21`). |
| Truth (stale) | Statements checked against the current release, not the page's history | The upgrade troubleshooting for "some agents have not upgraded" is obsolete: no code raises it and the server never reads `--ignore-agent-versions`. The HA caption said "database replicaset"; the database is Dqlite. |
| Sufficiency | A question list per audience | The application priority order and tie rule, the ordering of statuses a charm can set (claimed), the `failed` and `rebooting` agent statuses (claimed), the Kubernetes status overlay (claimed), who may set the application status (the leader, `leaderservice.go:68-101`) |
| Placement | Facts filed with their owner, by rule, with ties reported | Backend options moved to the secret backend page; hook behavior for user secrets to the hook page; cross-model facts to the relation page |
| Clarity | Titles, scaffolding and ambiguity as defect types | Metalanguage and uninformative titles flagged; lists and "only" statements made explicit for literal readers |
| Redundancy | A fact has one home, others link | Duplicate meanings of the four charm statuses in the `status-set` help and on the status page (claimed) |

## JUJU-10586: the per-call error contract

| Lens | Covered | Evidence |
|---|---|---|
| Per call: message, code, trigger, remediation | 960 entries on 182 of 204 calls of 33 pages; entries nest under the call that raises them | `tools/count_errors.py`; the checker matches message text |
| Reach from the client | An error the client never sees is not documented as one | Misattributed and unreachable errors are defect types in the review contract |
| Implementation mirroring | A raw database failure in an error's `<reason>` is a leak; the logical rule is stated once | `space.md` rename: a space that a constraint references cannot be renamed |
| Open | The home of an error raised by several calls (Q5); per-call traces for the remaining calls | `TODOS.md` item 4 |

## JUJU-9635: figures

| Lens | Covered | Evidence |
|---|---|---|
| Redundancy with the prose | A figure never carries a fact the prose lacks; the figure-removal test | `status.png` carried eight transitions that no code enforces and a false "being destroyed" description; the new status page states the true facts in prose (target) |
| Scope and position | A figure sits at the top of its section at that section's scope | The placement rule and the scope check in the contract |
| One view per figure; caption takeaway; alt inventory | The embedding of the whole model in every page measured 84% of `llms-full.txt` | `llms-full.txt` measurement |
| Process | A contributor can add a figure by one documented path | The existing ggarch section of `CONTRIBUTING.md`; the figure rules added to the rules |
| Open | Acceptance per figure (source, caption, alt text, light and dark render, `ggarch check`) | `TODOS.md` item 7 |

## Drive-by improvements (real fixes, not cleanup)

- False statements in `status.md` (`unit.go:989-1009`, `runhook.go`) and `secret.md`.
- Obsolete upgrade troubleshooting in `howto/manage-models.md`.
- A stale simplestreams index path and product-ID text.
- The generated CLI help for `--ignore-agent-versions` documents behavior the server no longer has. That is a Go help-text change; propose it separately, with the code checklist.
