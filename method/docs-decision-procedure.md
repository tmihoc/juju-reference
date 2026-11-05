# Documentation decision procedure (v2, 2026-11-05)

**Status:** research proposal, not an approved method, rule or edit. It operationalizes `method/requirement-set.md` into steps an AI (or a person) can run on a development. v1 was tested in E83 (`method/evidence/e83-results.md`); v2 repairs the failures that test found and has not been tested. The next test uses new cases (E84) and does not reuse the six of E83.

**Task:** given a development (a merged pull request or a series merged together), decide what documentation must change, where, in what category and form, and with what justification traced to a requirement. The output is a change set, plus a backlog of gaps found on the way, each with a confidence class.

**Inputs:** the diff and description of the development; the documentation set as it stood before it; the source after it.

## Steps

**1. Observable delta.** List every change a named audience can observe, with its surface class and its kind.

| Surface class | Examples |
|---|---|
| CLI | command, flag, default, output, help text |
| API | facade method, parameter, result, error message or code, access level, HTTP route |
| Configuration | key, default, allowed values, scope |
| State and signals | status value, event, log line, watcher payload, hook or hook-command behavior |
| Records | database schema, constraints, migration of data |
| Provider-specific | a provider's constraint, placement, storage, image or API-version behavior |
| Cross-cutting | a mechanism that several surfaces depend on |
| Internal | no observable effect |

| Kind | Meaning |
|---|---|
| **Change** | The observable behavior is different after the development |
| **Clarification** | The behavior is unchanged; the development states, validates or messages it |
| **Removal** | A surface (command, flag, route, key) no longer exists |

Internal items go to `doc.go` or nowhere (R1). A cross-cutting item stays only if a surfaced behavior cannot be predicted without it (R7).

**2. Audience questions.** For each delta item and each audience that can meet it (R3), instantiate the question templates below and keep the questions whose answer the delta changes. A delta that changes no answer for any audience is dropped, with the reason recorded.

| Template | Question |
|---|---|
| T1 | What is it, what can I do with it, and who may? |
| T2 | Which states can it be in, and which follow which? |
| T3 | What can fail, and what do I do? |
| T4 | What must be reachable, installed, permitted or configured for it to work? (ports, credentials, versions) |
| T5 | What happens to it during migration, upgrade, backup or removal? |
| T6 | Where do I see it, and what does what I see mean? |
| T7 | What replaced what I used? (applies to Removal and to changed defaults) |
| T8 | For a client developer: which call, request, result, error and code? |

Source of the templates: the audience table in the paradigm draft (`archive/work/docs-paradigm-draft-104.md`, section 2) with T4 and T7 added after E83 (ports in the hardening guide; the removed `--jump` and `download-backup`).

**3. Locate.** Search the whole documentation set. Collect every statement that (i) names an identifier of the delta (flag, key, error text, record, call), (ii) invokes a changed command or surface, whatever the statement is about, or (iii) answers a kept template question for the delta. Classify each statement against the delta:

- **Contradicted:** the statement is now false.
- **Enumeration extended:** the statement lists the members of a set (values, options, attributes, supported items) and the delta adds, removes or changes a member.
- **Outcome changed:** following the statement, or relying on its precondition, now gives a different result.
- **Unaffected:** none of the above. A statement that is merely silent about a new fact is unaffected, because a statement owes the reader only what its own scope claims (Quantity applied to the statement). Exception: a statement that a reader takes as exhaustive (a list of values, options or supported items, or "only", "all", "always") is an enumeration, and silence about a new member is then false for a reader who computes the exhaustivity from it (see the addressee model in `review-mode-contract.md`).

**4. Decide per item.**

- **Contradicted, enumeration extended, outcome changed:** fix at that statement's home, or move the fact to its owner and link (R17). Required for contradictions (Quality).
- **Delta fact has no statement anywhere (gap), kind Change or Removal:** in scope when R7 holds. The home is the owner:
  - the target entity's contract → the entity page, in the section whose source class fits (R18);
  - one interface's selection or syntax → that interface's page (R12, R24);
  - a fact shared by several surfaces → the mechanism's chunk. If none exists, propose one: reference states what happens, in what order, under which conditions (ports, authentication, limits); explanation is added only when the rationale is evidenced (R8);
  - a provider's behavior → the provider's page.
- **Kind Clarification:** the fact's owner is updated (for a CLI flag, the help text in the source, which the generator publishes). Hand-written statements change only if contradicted or an enumeration is extended. An unaffected statement that is silent is not part of the change set.
- **Generated surface (CLI help, hook commands, configuration keys):** run the generator and take its diff as the set (R4). Then apply this step to the hand-written statements.
- **Gap that predates the development** (a statement was already missing or already wrong, and the delta did not cause it): record it in the **backlog**, with its kind of defect. It is not part of the change set.

**5. Category (R8).** Reference for the contract. A how-to changes when a task step, a prerequisite or the order of steps differs, and its step statements are located by rule (ii) in step 3. Explanation changes only when its rationale or architecture picture is contradicted. A tutorial changes only when one of its steps breaks. Cross-links follow (R5).

**6. Removals and changed defaults.** For every Removal or Change of a default, flag, command, route or key that existing users meet: a release-notes entry (R23), the upgrade guide section if one exists for the version transition, and a redirect for a removed page (R15).

**7. Errors and figures.** A new or changed client-visible error gets an entry at its call with message, code, trigger and remediation (R19, R25). A figure is updated when its view depicts a changed record, status or sequence; a new figure is proposed only when R26's criteria hold.

**8. Form.** Write each item in the form of its home: entity grammar (R18, R19), tool-page sections, cloud-page template, how-to lifecycle step. Apply the text rules (R22).

**9. Output.** One line per item: `action | file and section (or new file) | category | requirement | confidence`, then the backlog, then one line for each examined chunk left unchanged with its reason. Confidence classes:

- **Determined:** every rule used is derived, settled in practice, or user-given, and the classification in step 3 is source-verified.
- **Tie:** layouts equal on all recorded properties (R14).
- **Open(Qn):** depends on an open question; name it.

## Auditing an existing change (refactor mode)

Use this when the change already exists and the question is whether it is justified: a pull request that adds, moves, rewrites and deletes documentation. The unit is the diff between the base and the change, not the new pages alone.

**Inputs:** the base set (the PR's merge base), the changed set, and the source at the base and at the change.

1. **Classify each changed file:** added, deleted, renamed or moved, or modified. For a modified file, take its removed and added statements from the line diff.
2. **For every removed statement, find where it went:** the same page reworded, another page (a move), or nowhere. Search the changed set by distinctive terms from the statement, not by page.
3. **Classify each removed statement:**
   - **Moved:** it now lives at an owner (R17); check the link or label from its old place.
   - **Obsolete:** the source at the change contradicts it (Quality). Removal is right; record the evidence.
   - **Duplicate:** another page owns the same fact (R16). Removal is right if the link exists.
   - **Dropped:** true, in scope (R7), asked about by an audience, and now stated nowhere. This is a Quantity regression. Action: restore at its owner, corrected against the source where the old text was out of date.
4. **Classify each added statement:** true (source check), necessary (R27: no equivalent in the base set), and correctly placed (steps 4 and 5 of the procedure). Untrue or unnecessary additions are trimmed or moved.
5. **Check addresses:** every label, anchor and URL of the base set must resolve in the changed set, or have a redirect (R15). A redirect that lands on a page with a different subject is flagged.
6. **Output per page:** keep, trim, move, or restore, with the statements concerned, the evidence, and the confidence class. Order the work by lines removed, because removals hide regressions.

The first pilot is `method/evidence/audit-pilot-metadata.md`.

## What this procedure does not do

- It does not check that a new statement is true. Every added or changed statement is traced to the source afterward (Quality).
- It does not establish findability or reader benefit.
- It is not tested on a documentation set different in kind from Juju's, or on development types beyond the six of E83.
- It does not decide which question templates are complete (Q1). The templates are derived from the audience table and extended by failures.

## Version history

- **v1:** the first version, tested in E83 on six developments. The tests: file-level recall of the developers' hand-written edits 3 of 3; 5 maintainer misses found (3 confirmed by later maintainer edits, 2 by source); 8 of 17 hand-written items over-flagged; missed a standing question (ports), a statement that invokes the changed command, and the generated files that share flags.
- **v2.1:** adds the refactor mode (auditing an existing change) after the user pointed out that the PR also refactored heavily, and the metadata pilot found a regression that the new pages alone do not show.
- **v2:** this file. Changes and the failure each answers:
  - Generated set comes from the generator (missed `debug-code.md`, `debug-hooks.md`).
  - Step 1 kinds (Change, Clarification, Removal) and the unaffected rule in step 3 (over-flagged items 5.2, 5.3, 3.2, 4.4).
  - Locate rule (ii) (missed `manage-logs.md`).
  - Question templates T1 to T8, T4 and T7 added (missed the ports statement; the removed flag and command).
  - Backlog separate from the change set (6.4, 6.5, 5.4).
  - Unit of development is the merged PR (C6 was an intermediate commit).
  - Step 6 for removals and changed defaults (the known gap).
  - Mechanism home and category rule (the SSH proxy: explanation by the maintainers, reference in the rewritten PR).
