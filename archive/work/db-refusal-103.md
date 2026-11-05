# The "database refuses" audit (session 103)

Question: which "the database refuses X" / "life never moves backward" claims in the reference schema sections are enforced by the database itself, and which are service or facade checks stated as database refusals? Verified read-only against /tmp/juju-41-tree (juju 4.1, e5db99d585) by scout `DBRefusalCheck`; the trigger bodies were read in the consolidated release DDL, not inferred from names.

## Verdict table

| # | Claim | Table(s) | Mechanism | Verdict |
|---|---|---|---|---|
| 1 | application.md:37 — DB refuses to move application life backwards | `application` | `trg_application_guard_life`: `BEFORE UPDATE ... WHEN NEW.life_id < OLD.life_id ... RAISE(FAIL, 'Cannot transition life for application backwards')` — `domain/schema/model/4.0.15-model-release.ddl:6123-6129` | **DB-ENFORCED — stays** |
| 2 | application.md:63 — DB refuses to update a controller mark; insert/delete only | `application_controller` (singleton row, `idx_singleton_application_controller`) | `trg_application_controller_immutable_update`: `RAISE(FAIL, 'application_controller table is unmodifiable, only insertions and deletions are allowed')` — DDL `:6074-6079` | **DB-ENFORCED — stays** |
| 3 | charm.md:40 — DB refuses a change to the row of any charm-related table except the charm itself, its download info, its tags… | 13 `charm_*` child tables (charm_action, charm_config, charm_container, charm_container_mount, charm_device, charm_extra_binding, charm_hash, charm_manifest_base, charm_metadata, charm_relation, charm_resource, charm_storage, charm_term) | one immutable-update trigger per table (`RAISE(FAIL, '<table> table is unmodifiable, only insertions and deletions are allowed')`) — DDL `:5983-6072`; no such trigger on `charm`, `charm_download_info`, `charm_tag`, `charm_origin` | **DB-ENFORCED — stays; wording: "a change to the row" → "an update" (the freeze is a full-row UPDATE trigger, unconditional)** |
| 4 | external-controller.md:94 — refuses to move a model another controller already hosts, which fails the import | `external_model` (controller DB) | no trigger/CHECK (PK + FK only, controller DDL `:363-369`); the check is `ensureExternalModelMatchesOrInsert`, `domain/modelmigration/state/controller/import.go:476-517` (`"external model %q already registered to a different controller"`, import.go:513-516); the other writer (`domain/externalcontroller/state/state.go:250-253`) deliberately upserts and moves models | **SERVICE-ONLY — move to the import call** |
| 5 | machine.md:32 — DB refuses to move machine life backwards | `machine` | `trg_machine_guard_life` — DDL `:6137-6143`; tested `domain/schema/model_schema_test.go:925-926` | **DB-ENFORCED — stays** |
| 6 | machine.md:40 — DB refuses to move the instance's life backwards | `machine_cloud_instance` | `trg_machine_cloud_instance_guard_life` — DDL `:6144-6150`; registered `domain/schema/model.go:273` | **DB-ENFORCED — stays** |
| 7 | space.md:138 — the default/alpha space names cannot be renamed: "the database refuses the change" | `space` | no trigger (only the name unique index, DDL `:260`); the refusal is in the API facade `apiserver/facades/client/spaces/rename.go:34-37` (`"the %q space cannot be renamed"`); the domain allows it (`domain/network/service/space.go:56-62`, state `:274-311`; proven by `space_test.go:199-203`) | **SERVICE-ONLY — move to the rename call (the guard is facade-level)** |
| 8 | unit.md:32 — a unit's life never moves backward | `unit` | `trg_unit_guard_life` — DDL `:6130-6136` | **DB-ENFORCED — stays** |

## Architecture note

`domain/schema/model.go:269-279` registers hand-written guard triggers (life guards: application, unit, machine, machine_cloud_instance, storage…; immutability triggers: application_controller, the charm_* children) plus the triggergen changelog triggers; all consolidate into the release DDL (`:5983-6199`). The changelog triggers only record; the `RAISE(FAIL)` guards are the only DB-level refusals in the model schema. The controller schema has no life/hosting guards — those invariants are domain responsibilities, which is exactly why claims 4 and 7 are service/facade checks.

## Retraction recorded

The session-103 generalization sample (scout `UnitMachineCheck`) reported machine.md:32/:40 and unit.md:32 as class-(c) drift ("false DB-enforcement claims") because it found no CHECK/trigger in the per-table SQL patches (`0018-machine.sql`, `0020-unit.sql`). The guards live in the consolidated release DDL. Those three sentences are TRUE as written. Standing lesson: re-verify subagent schema verdicts against `domain/schema/*/4.0.15-*-release.ddl`, never the per-table patches alone.
