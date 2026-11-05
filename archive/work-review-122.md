# Review of `work/`: evidence, working set and proposed pruning

**Status: review and pruning proposal, not authorization to move or delete.**
The 69 tracked files below were assigned in five non-overlapping groups and
reported read in full, including all 13,400 lines of the ggarch session
snapshot and 1,950 lines of its queue snapshot. There were no reported unread
ranges. The review retains original sources as evidence and does not retest
historical claims. Agent findings used in this synthesis were independently
spot-checked against the 4.1 source or original files; those spot checks do not
validate every statement in each artifact.

## The resulting working set

Start from these five existing research files, plus the new separate
`reference-spec-proposal.md`:

1. `work/system-model-115.md` — connected system model, supported paths and
   conditions, with later disk/authentication qualifications.
2. `work/global-skeleton-119.md` — current proposed cross-reference structure,
   not an approved or fully verified skeleton.
3. `work/content-planning-algorithm-119.md` — candidate classification and
   planning procedure; read its character/leg thresholds and one-home policy as
   heuristics, not source theorems.
4. `work/application-disposition-115.md` — 35 selected-page disposition plus
   supporting pages, not a full-reference semantic audit.
5. `work/reference-skeletons-117.md` — index to the per-page/family evidence and
   explicit gaps. Its linked files remain needed for their source traces.

The proposed specification and case suite are at
`reference-spec-proposal.md`; they are **drafts, not adopted documentation
rules or tests run by this review**. The live queue remains `TODOS.md`, with
registration and failed experiments in `structure-discovery-plan.md`. Historic
records stay searchable. This working set simplifies navigation, not the
underlying evidence: a summary is not a replacement for a source trace.

## What the review changed about our understanding

- **No finished theorem of page ownership.** Source distinguishes behavior and
  scope, but page versus anchored section and one full statement versus qualified
  copies are editorial choices where the same facts are preserved. E68's
  no-duplicate-owner/no-orphan result checks a proposed assignment, not a real
  link audit or proof of unique ownership (`work/content-planning-slice-relation-
  120.md:114-129`; `work/boundary-rules-e63.md:47-65`).
- **Keep negative evidence.** E44 did not establish a reader benefit and lacked
  an equal-content control; E59 originally failed its registered four-of-four
  threshold; E60's SSH paths and E62/E63 cases have documented contamination.
  Later bounded passes, inventories and builder successes do not erase these
  limits (`structure-discovery-plan.md:393-421,2065-2073`).
- **Do not revive the old space correction.** Historical `db-refusal-103.md:15`
  confuses the constraint-related rename refusal with the separate `alpha`
  facade guard. The release DDL's `constraint_space.space` foreign key refers to
  `space(name)` (`domain/schema/model/4.0.15-model-release.ddl:1365-1375`),
  while the facade separately rejects renaming `alpha`
  (`apiserver/facades/client/spaces/rename.go:19-37`). Current
  `docs/reference/space.md:136-146` distinguishes the two. Neither old wording
  nor this review authorizes an edit.
- **A diagram-model discrepancy was found and independently checked.** The
  `cloud_credential_attribute` primary key is `(cloud_credential_uuid, "key")`
  in `domain/schema/controller/sql/0005-cloud.sql:183-191`, but
  `work/cr-schema.ggarch:39-44` and the docs worktree's `docs/juju.ggarch:175-180`
  mark only `key` as a primary-key field. The current credential view hides
  fields (`docs/juju.ggarch:3792-3801`), so a visibly wrong PK label has **not**
  been shown. The research generator's quoted-field restoration hard-codes a
  text PK marker (`tools/build_page_schema.py:20-23`); its wider impact is
  unverified. Queued in `TODOS.md`; no model, generator or page was changed.
- **Snapshot equality is not disposal authority.** SHA-256 checks in this
  review matched the two `work/ggarch-state` history files to their counterparts
  in `~/git/ggarch`. The originals are untracked there by convention; the
  snapshot was intentionally preserved in this archive. Keep it, including its
  provenance and historical links, regardless of this momentary equality.
- **Current guidance is not silently superseded.** `page-recipe.md` and
  `docs/agents/AGENTS.documentation.rules.md:435-477` contain older ownership
  and form rules; later user guidance puts questions in the relevance/coverage
  role rather than using them to decide ownership. The reconciliation is a
  proposal (`work/application-disposition-115.md:55-61`), not an applied rule.

## Disposition key and gate

- **W — working entry:** part of the small current starting set.
- **E — supporting evidence:** retain accessible as source, counterexample,
  unresolved lead or detailed per-page trace; read when needed, not every time.
- **H — historical archive:** preserve in place for provenance, corrections,
  failures, adopted decisions and reproducibility; not current instructions.
- **S — scratch, review for removal:** only a *candidate* after checking
  provenance, regeneration and consumers. No file below is approved for removal.

No disposition here moves a file. `README.md`, `HANDOFF.md`, `TODOS.md`,
`page-recipe.md`, `SESSIONS.md`, old prompts and other `work/` artifacts cite
these paths; an archive move needs an approved link-preserving plan and a complete
inbound-reference check. Searches reported here are bounded to the searched
repositories and do not rule out external or indirect users. Superseded
hypotheses, failed results and dated decisions are useful history, not rubbish.

## Complete per-file inventory

Paths below are relative to `work/`. The selected category is for the original
artifact, not a claim that every statement in it has been newly verified.

| File | Class | Useful content / reason to preserve or review |
|---|---|---|
| `operation-task-boundary-121.md` | E | Action/exec target, guard and common task reader trace; synthetic aborted-status lead; no live execution. |
| `content-planning-slice-relation-120.md` | E | Relation data/context, entry precedence, blocked command details; corrects E68's overstrong owner reading. |
| `content-planning-stress-119.md` | H | Tool/process/provider/command forms, conditional diagrams and errors; reuse exercise, not new behavioral proof. |
| `content-planning-slice-model-119.md` | H | Model/default/credential/LXD split and generator-publication uncertainty; its pass is internal consistency. |
| `content-planning-algorithm-119.md` | W | Candidate procedure and conditional forms; thresholds and ownership remain editorial. |
| `global-skeleton-119.md` | W | Connected reference candidate, families, cross-links, explicit gaps and physical-layout ties. |
| `knowledge-structure-118.md` | H | Earlier synthesis, examples, queued corrections and coordinated rule-change proposal. |
| `operational-boundaries-e64.md` | E | Model identity versus DB REPL selector; actual local plugin probes; equal-facts tradeoff. |
| `boundary-rules-e63.md` | E | Competing boundary rules, contaminated cases, image-priority and annotation-result leads. |
| `reference-skeletons-117.md` | W | Index, scope and limits for per-page/family artifacts and denied scopes. |
| `skeleton-mechanisms-117.md` | E | Per-mechanism source leads: hooks, watcher, audit, task/status, scaling and removal. |
| `structure-challenge-e62.md` | E | Status-history kind mismatch and synthetic probe; object-store contamination; tags distinction. |
| `skeleton-infrastructure-117.md` | E | Machine, storage, network, SSH and constraints; source and per-page gaps. |
| `skeleton-control-117.md` | E | Controller/model, credentials, migration, backup/object-store and other control traces. |
| `skeleton-nested-117.md` | E | Nested authored/generated families, generator caveats, provider leads and path snapshot. |
| `skeleton-cloud-machines-117.md` | E | Nine individually qualified machine-cloud provider traces and unresolved comparisons. |
| `skeleton-commands-er-117.md` | E | Source-derived CLI invocation outlines, enable-user through scp; not complete backend audit. |
| `skeleton-commands-ad-117.md` | E | Source-derived CLI invocation outlines, actions through enable-destroy-controller. |
| `skeleton-tools-117.md` | E | Client/tool context, DB REPL, dashboard and Pebble paths and limits. |
| `skeleton-commands-sw-117.md` | E | Source-derived CLI invocation outlines, secret-backends through whoami. |
| `skeleton-workload-117.md` | E | Existing bounded action/relation/secret/workload traces, not a replacement for denied workload scope. |
| `application-disposition-115.md` | W | Selected-page disposition, supporting pages, and proposed shared guidance. |
| `system-model-115.md` | W | Connected system narrative and causal/order distinctions, with supplements. |
| `disk-inspection-116.md` | E | Post-hoc inspector surface for E59; not a general inventory API. |
| `authentication-challenge-116.md` | E | Bounded agent authentication and certificate-cache distinctions; no live login. |
| `held-out-116.md` | E | E60 audit trace, contaminated SSH cases, and no-live-connection limit. |
| `held-out-115.md` | E | Original E59 failure and credential/provider inconclusiveness; preserve alongside later disk evidence. |
| `control-infra-model-115.md` | E | Detailed model/credential/removal/migration/provider path conditions. |
| `filesystem-lifetime-114.md` | E | EBS storage ownership and force-detachment counterexample, source and helper limits. |
| `storage-boundary-114.md` | E | Pool/instance/attachment distinction, detach and pool facade limitations. |
| `subject-map-delta-113.md` | H | Historical map delta and neutral-anchor correction; cited by later syntheses. |
| `model-command-blocks-113.md` | E | Model block kinds/check order and bounded affected-call evidence. |
| `backup-subject-113.md` | E | Bounded backup request/archive path and unresolved placement/recovery. |
| `surface-inventory-113.md` | H | Dated CLI/hook-name accounting and exclusions, not behavior coverage. |
| `surface-ledger-113.md` | H | Historical source-surface leads, generated indexes and conditional restrictions. |
| `subject-map-112.md` | H | Historical direct-page subject map, caveats and failed reachability smoke. |
| `surface-ledger-112.md` | H | Historical surface and negative findings, including `dump-db` and firewall smoke limits. |
| `system-derivation-111.md` | H | Earlier derivation, helper evidence and ordering hypotheses; later causal decision prevails. |
| `endpoint-boundary-111.md` | E | Declaration/binding/relation boundary and refresh caveat; helper was not a deployment. |
| `surface-probe-111.md` | E | Secret selector asymmetries and possible v1 registration defect, with scoped evidence. |
| `story-form-110.md` | H | Timer counterexample and earlier form proposal; reader-question ownership advice was superseded. |
| `db-refusal-103.md` | E | DDL enforcement audit and retractions; space-refusal row is corrected above. |
| `docs-paradigm-draft-104.md` | H | Adopted-era charter, bot skills and stale-claim table; not current universal authority. |
| `held-work-justification-103.md` | H | Historical held-batch reasoning and migration/watcher leads; space row and held status need later corrections. |
| `cq-rubric-103.md` | E | Audience/relevance history and source leads; ownership premise superseded, cited by `page-recipe.md`. |
| `duplicate-facts-99.md` | E | Recorded overlap candidates and negative cases; some later resolved, not blanket deletion instructions. |
| `general-method-101.md` | H | Earlier schema-first method; ends mid-sentence and is still linked from root README. |
| `decisions-100.md` | H | User decisions, completed page/figure work and dated open items; later outcomes qualify them. |
| `agent-facades-99.md` | E | Historical agent-facade map and open authentication questions; security/publication restrictions apply. |
| `grice-review-95.md` | H | Historical review rows and corrections; later session results disposition several stale leads. |
| `table-mapping-paragraphs.md` | E | Extracted 33 page mappings; possible generator input, not current schema truth. |
| `storage-split.md` | H | Prior storage diagram/table grouping; later E57/E58 limit schema-only inferences. |
| `cr-schema.ggarch` | S | Credential scaffold; preserve composite-key discrepancy and check regeneration/consumers first. |
| `cr-labels.json` | S | Credential display labels and quoted-key restoration input. |
| `sp-schema.ggarch` | S | Historical space/network scaffold; not the current separate live views. |
| `sp-labels.json` | S | Space/network scaffold display labels. |
| `m-trim.ggarch` | H | Historical 12-record machine trim; differs from the current selected view. |
| `m-schema.ggarch` | S | Wider machine scaffold with lookup/context neighbors; not the trimmed figure. |
| `m-labels.json` | S | Machine scaffold display labels. |
| `juju.ggarch.bak` | H | Historical complete model and diagram/source leads; differs from current model. |
| `sb-append.ggarch` | H | Trimmed secret-backend schema and view; records a different layout/context. |
| `sb-schema.ggarch` | S | Wider secret-backend scaffold, not equivalent to the trimmed view. |
| `sb-labels.json` | S | Secret-backend display labels. |
| `ctrl-append.ggarch` | H | Controller schema, bootstrap sequence and HA draft with unique source leads. |
| `ctrl-schema.ggarch` | S | Controller scaffold; overlaps but is not a replacement for the append artifact. |
| `ctrl-labels.json` | S | Controller display labels and quoted-key restoration. |
| `ggarch-state/README.md` | H | Snapshot provenance and link to the designated live, untracked ggarch records. |
| `ggarch-state/SESSIONS.md` | H | Full dated ggarch decision, reversal, diagram and 4.1-transition history. |
| `ggarch-state/TODOS.md` | H | Dated ggarch queue and verbatim decisions; not the current queue. |

## Pruning sequence — proposal only

1. Use the working-set index above and the separate specification draft now;
   leave all source evidence and historical paths intact.
2. For each H item proposed for relocation, first preserve unique decisions,
   negative results, references and dates; then explicitly approve a destination
   and update or preserve inbound links. A history file being old is not evidence
   it can be deleted.
3. Review each S artifact together with its label/scaffold companions: capture
   provenance and any unique finding; check current consumers and regeneration;
   then request approval for any specific removal. The snapshot histories and
   nonidentical backups are **not** on that list.
4. Do not move or delete files merely because a newer summary cites them; many
   summaries contain abbreviated source evidence. No page, diagram or rule changes
   are implied. The three 402-denied scopes and the possible implementation
   defects in `TODOS.md` remain open.

## Review verification and incident

- All five reviewers reported full reads of their assigned files; the per-file
  list above accounts for all 69 tracked artifacts. Their reports are research
  aids, not independent proof of all source claims. Key samples were rechecked:
  status-history matcher, credential validation, relation-entry precedence,
  space rename/foreign key, and the credential PK flags.
- Inventory accounting compared all filesystem entries, including ignored/hidden
  entries, with the tracked-file list and the 69 unique table rows: 69/69, no
  missing or extra files. Categories: 5 W, 31 E, 23 H, 10 S. This proves file
  accounting only, not truth, completeness of source claims or link safety.
- An exact-filename search for the ten S entries across the research archive and
  separate docs worktree found only the references created in this review and
  the new credential-model TODO. This bounded search does not establish that
  external consumers are absent or that the files are reproducible; the TODO
  and review references must also be preserved if that scaffold moves.
- Cached `dirhtml` and `latex` Sphinx builds succeeded for the unchanged docs
  worktree; no PDF was built. They do not verify this research proposal.
- No new behavioral test was run, no `work/` artifact moved or deleted, and no
  reference page, production source, figure, repository rule or selected counter
  was changed. Past synthetic/live results retain their original limits.
- **Instruction breach:** the historical reviewer reported a read-only filename
  search under `/home/dora/git/juju/docs`, despite the standing instruction not
  to touch the main Juju checkout. It reported no edits. Its main-checkout search
  results are not needed for the conclusions above; this does not excuse the
  access. Other evidence was checked against `/tmp/juju-41-tree` and the separate
  documentation worktree.
