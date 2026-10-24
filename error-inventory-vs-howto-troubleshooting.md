# Can the entity reference pages replace the how-to troubleshooting notes?

Analysis of 2026-09-30 (session 76), prompted by the question of how the error
information on `model.md` compares to the troubleshooting notes in
`docs/howto/manage-models.md#migrate-a-model`. Sources: the branch
`4.1-docs-entity-reference-layers` (worktree `~/git/misc/juju-entity-ref`) and the
4.1 Go source. Status: analysis only; nothing implemented. Related: ggarch
ADR-016, `entity-page-form.md`, `pr-entity-reference-layers.md`.

## 1. How the two compare (model.md vs the migration howto)

| | `model.md` | howto "Migrate a model" > Troubleshooting |
|---|---|---|
| Kind of error | Domain error constants (`model not found`, `model not activated`, `model already activated`, `model not redirected`) and the target-format precheck error | Three status messages shown by `juju status` / `juju show-model` |
| Organised by | Layer and record | Symptom, with cause and fix |
| Migration coverage | Two errors | Three messages |
| Overlap | None in the strings | None in the strings |

The howto messages are composed by the migration-master worker
(`internal/worker/migrationmaster/worker.go`) around the target controller's
error: `aborted, removing model from target controller: model data transfer
failed, <target error>`.

Checked against the 4.1 source:

- `machine sanity check failed, N errors found` is still emitted
  (`worker.go:635`): accurate.
- `granting admin permission to the owner … user is permanently deleted` does not
  exist in the 4.1 source. The entry's own note ("Starting with Juju 4 …")
  suggests 3.x-era text.
- `credential "<credential>" not found (not found)` does not exist in 4.1. The
  nearest 4.1 messages are `credential for model %q not found`
  (`domain/modelprovider/state`) and the precheck `model has revoked
  credentials`.

Neither page covers the roughly 20 precheck errors in
`internal/migration/precheck.go` that a user can hit before anything transfers:

- model named "X" already exists; model with same UUID already exists
- model has higher version than target controller; source controller has higher
  version than target controller
- model's cloud "X" not found on target controller
- machine X is dying (or dead); upgrade in progress
- model is being imported as part of another migration; model has revoked
  credentials; model is <life>
- unit X hasn't joined relation Y yet
- all charms now require a manifest.yaml file
- fan networking not supported (two variants)
- the target-format check (facade version 8, Juju 4.1 or later)

The howto mentions two of them as advice ("same name", "same or newer version")
without the messages. The phase messages the worker sets are also undocumented:
performing source prechecks, importing model, checking machines in migrated
model, timed out waiting for agents to report, some agents reported failure, and
so on.

## 2. Can the entity pages obsolete the howto notes?

Mostly yes, with changes; not for everything.

### What the form supports

The raise-site form gives every domain error constant one home with trigger and
remediation, and completeness can be checked mechanically. Measured on 4.1:
363 domain error constants, 180 (49%) appear in `docs/reference/*.md`. Coverage
is uneven and the gaps sit in domains with no entity page:

| Domain | Defined | Documented |
|---|---|---|
| application | 70 | 44 |
| machine | 23 | 12 |
| removal | 22 | 6 |
| relation | 22 | 17 |
| access | 18 | 10 |
| objectstore | 16 | 0 |
| crossmodelrelation | 15 | 5 |
| resource | 14 | 12 |
| storage | 14 | 10 |
| model | 13 | 12 |
| modelmigration | 13 | 1 |
| secretbackend | 7 | 0 |
| agentbinary | 6 | 0 |

The undocumented remainder needs classifying as user-reachable or internal.

### Where the form breaks down

1. Symptom versus raise site. A user arrives from an operation; the error's home
   is the entity that raised it. Migration touches model, user, credential,
   machine and cloud, so its errors spread across pages. The howto is indexed by
   operation; the reference is not.
2. Messages that are not constants. The prechecks and status messages (about 30
   in `precheck.go`, about 36 in `worker.go`) are formatted strings with variable
   text. A hand-written list cannot be checked for completeness by a script.
   Wrapped chains (wrapper plus inner error) split across two homes, and the
   wrapper is documented nowhere.
3. Provider and store errors (cloud APIs, Charmhub) pass through. They can only
   be described as "read the message".
4. Remediation. The howto's fixes are commands (`juju set-credential`, create
   the user on the target). A client-agnostic reference can hold a one-line
   remediation with a command as an example, not the procedure.

### Recommendation

Make the reference the authority for error strings, causes and remediations. Cut
each howto's troubleshooting to a short "if it fails" pointer with links, keeping
any real procedure. Three additions make that work:

- Operation lists on the entity page: a migration bullet set in `model.md` listing
  every precheck and phase message, with cross-entity errors as links to their
  pages; the same for deploy, remove and upgrade. This restores the
  operation-indexed view without duplicating claims.
- A generated error index (error string to page anchor, alphabetical) plus a
  coverage check that every user-reachable constant is documented or marked
  internal. It would run like the planned ggarch check and can be built from
  `tools/raise_sites.py`.
- A message-shape convention: an item shape for wrapped and templated messages
  (`<prefix>: <inner>`, placeholders), documented once on the loop that composes
  them.

Keep the ad-hoc precheck and status messages as a manual list with a source
reference. State in the form that the completeness guarantee covers constants
and documented operations, not every string in the codebase.

Evidence of drift: two of the three migration troubleshooting entries are absent
from the 4.1 source. That is the strongest argument for moving this content to a
generated, checked pipeline.

## 3. Open

- Add the migration bullet set to `model.md` plus the index and coverage script
  as the first proof (offered; the user has not decided).
- Fix or retire the two stale howto entries (outside this PR's 24 pages).
- The non-entity domains that need pages or sections: modelmigration, removal,
  secretbackend, objectstore, agentbinary, crossmodelrelation.
- Decide how ADR-016 should state the completeness guarantee and the
  message-shape item.

## 4. Follow-up (2026-10-19)

The template change that follows from this analysis is drafted, with the
migration section as its worked example, in `entity-page-form-v2-proposal.md`.

## 5. Status after session 78 (2026-10-19)

Recommendation items: (a) operation lists on the entity page: done for migration in the `model.md` pilot (stage table and failure table with messages, triggers, remediations), not for deploy, remove, upgrade; (b) generated error index by string with a coverage check: not built, and now better supported (E10: raters recognise "failure" as a reader kind with 94% agreement, and the red team found that many errors violate no rule, so nesting under rules alone cannot be the lookup); (c) message-shape convention: drafted in the v2 proposal, not applied; (d) the two stale howto entries: not fixed; (e) the non-entity domains without pages (modelmigration, removal, secretbackend, objectstore, agentbinary, crossmodelrelation): untouched; the coverage figures above (180 of 363) were not re-measured. The v4 shape (errors nested under the operation or record that raises them, plus an index by string; rule-less errors such as lookup misses, races and transient failures filed under the operation) agrees with section 2.
