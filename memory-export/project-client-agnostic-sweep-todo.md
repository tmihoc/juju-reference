---
name: client-agnostic-sweep-todo
description: TODO for #23451 and follow-ups: sweep the entity reference pages for CLI-led phrasing and make them platform-first, with the CLI only as an example
metadata:
  type: project
---

Entity reference pages are client agnostic: Terraform, the dashboard and other clients read the same platform facts, and the CLI may be split from the rest of the platform one day. Facts such as error messages and migration status messages belong to the controller; the CLI only renders them.

**TODO (user said "We'll get to it", 2026-10-19):** sweep the pages in #23451 (branch `4.1-docs-entity-reference-layers`) and every later PR for CLI-led phrasing. Lead with the platform fact (controller, API, record), and name the CLI command only as an example ("for example, with `juju migrate`"). Known hits: `juju reprovision-machine` in the machine page's Reprovisioning bullet; `--background` and `--wait` in the action page's "Waiting and results" bullet; check remediation cells for CLI flags. Do it as its own commit; a push needs the user's go.

**Why:** the user's reasoning on 2026-10-19: errors are identical for every client, other clients' docs already link to this reference, so the link does more work if the reference stays neutral.

**How to apply:** when writing or editing any reference row or bullet, state what the controller does or reports first. Related: [[entity-reference-form]], [[no-unearned-negation]].

**Vocabulary sweep (added 2026-10-19, same TODO, do it once after the structure settles):** replace our internal jargon in operator- and client-facing text, or define it at first use. Counts across the 26 reference pages: satellite 27 (13 pages), baseline snapshot 15 (15), natural key 11 (8), foreign key 10 (4), join handle 6 (6), primary entry 6 (6), native record 4 (4), derived view 4 (4), cached cloud fact 3 (2), decoupled 2 (2), projection 1 (1). Database terms such as foreign key and natural key are fine at the platform-developer level (the data-model part). "Native record" only makes sense where it contrasts with a cached cloud fact (zone, subnet). Test: can a reader in a named audience paraphrase the term without Juju's source?


**Cross-reference sweep (added 2026-10-19):** every piece of jargon links to its reference page at first mention in a page, ledes first; terms with no page get a plain in-place explanation. Part of the same sweep as the vocabulary and CLI-phrasing passes. Done so far only in the controller and machine pilots (scratch worktree).

**Reinforced 2026-10-20 (session 82):** do not link to CLI command pages from entity reference pages, and do not add a "the CLI offers ..." paragraph; define operator concepts (such as block commands) in place with a parenthetical until a platform page exists. I linked CLI commands in the `ssh-key` pilot and the user corrected it.

