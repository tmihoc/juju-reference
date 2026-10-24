---
name: project-actor-part-template
description: "Entity page template v3 — optional actor part first (Machine agent, Controller agent, Model workers, Unit agent), only where the entity has its own process or engine"
metadata:
  node_type: memory
  type: project
  originSessionId: a9d923a1-5ac4-4320-a949-6663e0ff977c
  modified: 2026-10-19T18:20:31.617Z
---

Decided in session 78 (2026-10-19), proposed to the user, not ratified: an entity page is lede, optional actor part, data model, change streams, operations. The actor part is named by the actor (not "software"), exists only for an own process or per-instance engine (controller, machine, unit, model), comes first because every later part names the actor, and is the one home (`agent.md` only points to it). Pilots machine, controller, model done in `~/git/misc/juju-v2-preview` (local commit 7e27ac4f86 on wip-entity-reference-pilots); the unit page is still layered.

**Why:** the earlier "machine and model are entity-only" verdict read current text; the code shows the machiner marks machines dead, the deployer runs unit agents inside the machine agent, and the model has a worker engine per activated model inside the controller agent (plus a model operator pod on Kubernetes).

**How to apply:** before reopening, read "Actors in the template" at the end of `~/git/misc/juju-reference/structure-discovery-plan.md`. See [[project-entity-reference-form]].

**Status update (session 78, later):** the five-kind skeleton was stress-tested (E7-E9, reader test, red team; see the plan). It holds as a backbone (identity, state, dynamics) for entity pages only; agent and observation are conditional parts, and interface, applicability, guidance and an error index by string are missing. Not frozen; theory v4 is proposed.
