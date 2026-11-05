# What the research settled (digest, 2026-11-05)

A short account of what 130 sessions established, what failed, and what is still open. The evidence lives in `archive/` (the plan `archive/structure-discovery-plan.md` holds every experiment E0 to E82 with its registration). Cite an experiment by number when you need its detail; this page is enough to work from.

## Settled and in use

| Result | Basis |
|---|---|
| **The entity page form**: lede; `X database schema`; `X change streams`; `X calls`; `X and model migration`. Each section only when its facts exist. Rules: `method/page-recipe.md`. | The `ssh-key` pilot (about twenty review rounds), then 33 pages. Checked by `tools/check_page_rules.py`. Not tested on readers (E44 showed no structural gain). |
| **Facts come from the source, not from old prose.** The 4.1 code is the authority. Every statement is traced with file and line. | Standing practice; independent review found real defects in the old pages. |
| **A schema rule stays only if the database enforces it** (a constraint, index, trigger or foreign key) or the schema fixes the allowed values. Other rules belong to the call. | Audited against the consolidated release DDL. |
| **An entity with its own typed ID, facade method and lifecycle is a page.** A table group that cannot exist without one owner is a section of that owner. | E35 to E43. Per `archive/skeleton-v6.md`, 23 of 33 groups agree across three instruments; ten stay open. Treated as a sufficient condition for a page, not a full rule. |
| **The error contract**: 960 entries, 674 distinct messages, on 182 of 204 calls of 33 pages. | `tools/count_errors.py`. The CI guard matches message text only; it does not establish per-call reachability, attribution or remediation. |
| **One ggarch model, one view per figure**; caption carries the takeaway, alt text carries the inventory. | Measured: embedding the whole model in every page made 84 percent of `llms-full.txt` (queued in ggarch as alt-only emission). |
| **Inclusion rule**: a fact stays if it is true, a reader can meet it on a supported surface, and a named audience asks for it on this page. | Applied across the PR; now refined in `method/requirement-set.md` (R1, R2, R7). |

## Tried and failed (keep these)

| Attempt | Result |
|---|---|
| Boundaries from referrer counts and from worker ownership (E37, E38, E47) | Falsified. |
| Reader test of the pattern (E44) | No structural benefit. The `ssh-key` gain came from added content, with no control to separate structure from content. |
| Held-out system-model challenge (E59) | Failed its registered four-of-four threshold. |
| A decision tree for content planning | Unapproved, and no better than a simple evidence record. |
| Choosing page or section from source and equal-fact layouts (E63, E64, E82) | No winner. Equal content fits either; source can disprove a scope but cannot choose a layout. Resolved in principle by `method/requirement-set.md` Q2, not yet by evidence. |
| Procedure v1 on six real past developments (E83) | Found the right places and five maintainer misses, over-flagged 8 of 17 items, and missed a standing question (ports). Repaired in v2, untested. |

## Where things stand

- **The mechanism:** `method/requirement-set.md` (27 requirements with grounds and status) and `method/docs-decision-procedure.md` (v2). One worked decision: `method/evidence/ssh-documentation-decision.md`.
- **Open questions:** Q1 the relevant level and question set; Q2 page versus section by change-coupling and reading paths; Q3 whether the section grammar follows source artifact classes; Q5 the home of an error raised by several calls; Q6 watcher names on 16 pages; Q8 the unit of a development.
- **Defects and leads found along the way:** `epics/source-questions.md`.

## What no result establishes

Reader benefit; completeness of the reference; that the procedure generalizes beyond Juju or beyond the six development types tested. Four research scopes were denied (HTTP 402): `WorkloadModel`, `HookCommandPages`, `KubernetesCloudAttributes`, `CrayonEvaluation`. Do not relaunch or work around them; ask the user.
