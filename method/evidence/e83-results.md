# E83 results: procedure v1 against six real developments (2026-11-05)

Registration: `archive/structure-discovery-plan.md` > E83. Predictions: `method/evidence/e83-predictions.md` (written before any case's docs diff was opened). Procedure: `method/docs-decision-procedure.md` v1, unchanged during the run.

## What the registered oracle contained

The documentation edits made in the case's own commit or PR:

| Case | Hand-written files edited | Generated files edited |
|---|---|---|
| C1 `--show-command` | none | `ssh.md`, `scp.md`, `debug-code.md`, `debug-hooks.md` |
| C2 `--jump` default | none | the same four |
| C3 GCE `image-id` | `google-gce.md` (one line in the constraints list) | none |
| C4 OpenStack Cinder pool | `openstack.md` (three sites) | none |
| C5 charm revision and resources | none | `deploy.md`, `refresh.md` |
| C6 create-backup | `redirects.txt` | `create-backup.md`, `download-backup.md` (removed) |

Four of six developments changed no hand-written page in their own commit. The oracle is therefore thin: it says what the developer remembered to touch, and for most cases that is the generated pages.

## Scores against the registered thresholds

| Threshold | Result | Reading |
|---|---|---|
| (1) File-level recall of edited hand-written files at least 80 percent | 3 of 3 (100 percent) | Pass, on three files |
| (2) Section-level recall at least 60 percent | 5 of 5 edit sites (100 percent) | Pass, on five sites |
| (3) P-extra at most 40 percent of predicted chunks | 8 of 21 items (38 percent) counting generated items; 8 of 17 (47 percent) on hand-written items only | The registration did not say which. Read against me: not passed. |
| (4) No now-false statement left unflagged | Not shown violated. One case is unresolved (`manage-logs.md`, C2). | Pass, with the unresolved case recorded |
| (5) At least 70 percent of items Determined | 16 of 21 (76 percent) | Pass (descriptive) |

Generated files are counted separately, as registered: 8 of 12 actual generated files were predicted (67 percent). The four misses are `debug-code.md` and `debug-hooks.md`, which embed the same flags, in C1 and C2.

## Adjudication of every disagreement

Labels as registered. Evidence beyond the registered oracle is marked post hoc: it comes from later upstream documentation commits whose subjects I saw in the initial history listing (before predicting) but whose contents I read only after. That is a mild contamination.

| Item | Label | Basis |
|---|---|---|
| 1.2 `manage-machines.md` add `--show-command` | M-miss | Commit `25668c0cca` (about six weeks later) added exactly this text (post hoc) |
| 2.2 `manage-machines.md` default path, port, `--direct` | M-miss | The same commit rewrote the "two ways to connect" paragraph and removed its claim about admin access (post hoc) |
| 2.4 `ssh-key.md` sentence on `juju ssh` access | M-miss | The same commit rewrote that sentence region (post hoc); the source requires model admin for the SSH server (`internal/worker/sshserver/authorization.go:59`) |
| 2.3 `manage-controllers.md` ports | P-extra | Wrong file. Commit `c4cd6f5912` later added the ports to `harden-your-juju-deployment.md`, which I did not flag (a P-miss) |
| 3.2 `base-image-path` entry | P-extra (conservative) | The source does resolve short names through the base image path (`gce/config.go:108`, `image.go:56-62`), but whether omitting it harms a reader is undecided |
| 4.3 Cinder attribute list | M-miss | The page lists only `volume-type` as a configuration option; the source schema adds `tag` and `disk-bus` (source-verified) |
| 4.4 compute microversion requirement | P-extra (conservative) | The requirement is in the source; no evidence that an operator observes a failure |
| 5.2, 5.3 how-to updates for `--revision` | P-extra | The behavior existed before; the help text now states it; no task step changes. This is a materiality question the procedure cannot decide (Q1). |
| 5.4 owner of "resources released with a revision" | P-extra | Unresolved owner; no evidence of need |
| 6.3 upgrade guide, "create-backup fails with not-implemented" | M-miss | At the anchor the backups facade has no not-implemented error, and the guide still says it fails (source-verified) |
| 6.4 backup how-to section | P-extra (conservative) | No backup how-to exists at the anchor either. The gap is real under R9, but the development did not need it. |
| 6.5 home for the download endpoint | P-extra (conservative) | No route reference exists |

Missed by the procedure (P-miss), by later evidence or source: `harden-your-juju-deployment.md` (ports), `manage-logs.md` (a how-to fallback that assumed a different connection path; falsity not shown), a new explanation page on how `juju ssh` works with a diagram (commits `25668c0cca` and `d2cf9fc1fb`), and the two generated pages.

Not counted against the procedure: `manage-ssh-keys.md` changed in the same later commit for a different development (the `--ssh-key` flag).

## What the result shows

1. **The procedure finds the right chunks.** Every hand-written chunk the developers touched was predicted, at section level too.
2. **It finds more than the developers did, and some of the extras are real.** Three M-misses are confirmed by the maintainers' own later edits (1.2, 2.2, 2.4). Two are confirmed by the source (4.3, 6.3). The 6.3 case is a live defect: the upgrade guide at the anchor says create-backup fails with a not-implemented error, and the code no longer does.
3. **The confidence classes carry information.** Of 16 Determined items, 12 were matched, confirmed later or confirmed by source (75 percent); of 5 Open items, 1 was (20 percent). Four Determined items were over-flagged (3.2, 4.4, 5.2, 5.3).
4. **Over-flagging comes from one missing criterion.** "Incomplete" has no materiality test, so a statement that is silent about a new fact gets flagged whether or not a reader's outcome depends on it.
5. **Under-flagging comes from the search and the questions.** The locate step searched for statements about the changed option and missed statements that exercise the changed command (`manage-logs.md`) or that concern a standing question the delta raises (ports, in the hardening guide).
6. **The "document the mechanism" decision is unresolved.** The maintainers wrote an explanation page for the proxy; the PR under test wrote a reference page for the SSH server. The procedure's category rule did not predict either.

## Limits

- n = 6; four cases have an empty hand-written oracle, so recall is close to vacuous. The post hoc evidence is more informative than the registered oracle and is weaker evidence.
- I wrote the procedure and the predictions and adjudicated the disagreements. The adjudications that rest on the maintainers' later edits and on source checks are the least subjective; the conservative P-extra labels are the most.
- C6 is a commit inside a series; the unit of a development should be the merged PR.
- The parent docs are the pre-rewrite set; nothing here tests placement in the rewritten structure.
- Source checks were source reads and no live runs.

## Revisions the result requires (applied in procedure v2)

1. Take the generated file set from running the generator.
2. Add a materiality criterion for "incomplete".
3. Distinguish a behavior change from a clarification of existing behavior.
4. Add standing questions by delta class, and widen the locate step to every statement that exercises a changed command.
5. Make the unit of a development the merged PR.
6. State how a new cross-surface mechanism gets a home and a category.
7. Add a release-notes and upgrade-guide step for removed or changed defaults, flags and commands. This was a known gap before the run; no case exercised it.
