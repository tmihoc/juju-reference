# Entity reference page form (ADR-016)

Binding record: `~/git/ggarch/adr/016-diagnostic-locality-layer-anchored-rules.md`.
Worked example: `machine-rewrite-draft.md` (verified against 4.1 source,
2026-09-30). Applies to reference pages of type 1 and 2 in
`reference-page-types.md`.

## Goal

Diagnostic locality and preattentive scanning: a reader holding an error
string or a rule lands on the place where it arises, inside its layer. Replaces
the storage-optimised pattern (flat Rules and Errors lists at the bottom of
each layer, or a separate rules-and-errors section).

## Rules

1. **No free-standing rules-and-errors list.** Nest each rule, error, trigger
   and remediation under the bullet it constrains.
2. **Anchor per layer.**
   - Declaration: lifecycle action (create, designate, consume, remove).
   - Persistence: stored record component (primary entry, parent record,
     cloud instance record, status records, lookups). A schema does not run a
     lifecycle, so persistence bullets are not phrased as actions.
   - Execution: operational loop (controller-side provisioning, agent-side
     provisioning, removal, watchers).
3. **File by raise site.** Find the error's `errors.go` constant and every
   `Add(...)` or `%w` site in the Go source. The layer whose code raises it
   owns it. Write the literal Go message.
4. **Status values are not errors.** `provisioning error` is a value of a
   status record: list it with the record.
5. **Fidelity.** Keep every verified fact, `{ref}` link, anchor and error
   string. Drop or correct anything the source does not support and list it
   in the PR notes. Stack every old anchor on the place its content moves to.
6. **Sentence case** in bullet titles, rules, triggers and remediations.
7. **Empty layer:** one sentence saying so; invent no bullets.

## Item shapes

Declaration:

```
- **Action name:** What happens.
  - *Rule:* ...
  - *Related error:*
    - **`error string`**: *Trigger:* ... *Remediation:* ...
```

Persistence and execution use the same shape with a record component or an
operational loop as the bold name.

## Per-page checklist

1. List the page's errors and rules (prep branch version).
2. For each error: grep the constant, list the raise sites, pick the layer.
3. For each rule: find the enforcing code; note the error it produces, if any.
4. Check every stated remediation against the code (supported values,
   retries). A remediation with no code behind it is dropped or marked.
5. List the old anchors and stack them on the new locations.
6. Grep `docs/` for inbound references to each old anchor.
7. Re-point the ggarch catalogue's Insert-at strings.
8. Purged docs build: no new warnings against the 4.1 baseline.

## Defects found in the first machine pass (another model's rewrite)

Recorded so the next pages do not repeat them:

- Dropped the rule "a machine goes dead only when units, containers and
  storage clear" (the removal service enforces it: `entity still alive`,
  `machine has containers`, `machine has units`, `machine has storage`).
- Dropped the string `machine constraint violation` and kept the claim it
  belonged to; the claim overstated the check (arch only).
- Dropped four anchors: `machine-declaration-rules`,
  `machine-persistence-rules`, `machine-execution-rules`,
  `the-machines-machinery` (the watcher page links the third).
- Kept two errors in the declaration layer that are not raised there
  (`grandparent machine are not supported currently`: reboot state code;
  `machine already exists`: the model-import path only).
- Merged the nesting cap into the grandparent remediation; the cap is enforced
  by name validation (`machine name %q has too many containers`).
- `invalid container type` remediation said "check the cloud's supported
  container types"; 4.1 knows `lxd` and `none` only.
- Listed a status value (`provisioning error`) as an error, and kept a retry
  claim with no source support (held out).
- Broke list nesting in the paste, so sub-bullets floated to the wrong parent.

## Rollout notes (session 76)

Applied to 24 pages; see ADR-016 "Rollout" for the findings. Tooling used, kept
in `tools/`: `raise_sites.py` (error string to Go constant to raise
sites, per page) and `loss_check.py` (prep sentences missing from the new page,
by 4-word shingles). Conventions that settled:

- One claim, one page: an error raised by the machine state is listed on the
  machine page only; the constraint page links there.
- Stack every old anchor on the layer heading (`(x-declaration-rules)=`,
  `(x-persistence-rules)=`, `(x-execution-rules)=` and the pre-existing operation
  and watcher anchors); no label was dropped.
- Persistence bullets name the record component; rules that describe behaviour
  move to the loop that performs it.
- A link to a label that only the prep branch defines (`data-model-full-spine`,
  `upgrading-things`) points at the 4.1 page that replaced it.

## v2 (proposed, 2026-10-19)

Error tables, operation bullets, the three message kinds, the generated error
index and the howto-pointer rule are specified in ADR-016 "Amendment
2026-10-19" and worked through in `entity-page-form-v2-proposal.md`. Pages
written so far (the 24 in #23451) use the v1 nested-bullet shape for errors;
they convert to tables when their operation is taken up.

## v3 (proposed, 2026-10-19, session 78): page shape and the actor part

Page = lede (basic facts, multiplicities, one level above everything), data model, change streams, optional actor part, operations (the causal chain: records, announcement, listener, action). The actor part appears only where the entity has its own process or engine (controller agent, machine agent, unit agent, the model's worker engine); it is named by the actor, follows the change streams, lists the workers as labelled items with their manifold names, and states identity, gating and the relation to the other actors. Operations name the actor and their trigger; other workers are listed once in the part of the entity whose engine runs them. Reasons and evidence: `structure-discovery-plan.md`, "Actors in the template".

Operations (session 78, user): an operation entry is the client-agnostic description of what the platform does for a request from any client, so every client's how-to can point to it. Fixed shape: trigger, precondition and errors, sequence (actors and steps; a sequence view where the order matters), effect on records, effect on software. Processes with states also get a state view. How-tos keep the client-specific "how to ask".
