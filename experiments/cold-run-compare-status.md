# Cold runs 1 and 2 on `status.md`: comparison (parent, 2026-11-05)

Both runs read upstream at `e5db99d585` and the same method (run 2 with the contract as frozen before the addressee-model and rules edits). Neither saw our PR.

## Findings

About 80% of the substantive findings coincide (matched by eye, not by script): the priority order is never given; the figure is wrong and unneeded (its transitions are not Juju rules); a new unit starts `waiting/allocating`, not `maintenance/allocating`; `unknown` is set after the start hook, not the install hook; `terminated` is set after the remove hook; a hook failure shows as agent `idle` and workload `error`; the agent table omits `failed` and `rebooting`; the Kubernetes pod override is missing; the `<workload>/<agent>` form and the sample output are untraceable or stale; only the leader sets the application status.

Only in run 1: scope claim larger than the content (values exist for machines, models, relations, storage and tasks); "set by the Juju agent" partly false. Only in run 2: "blocked beats active unless a unit is in `error`" (conditional truth stated flat); the meanings of the four charm-settable statuses duplicate the `status-set` help.

## Drafts

Both drafts keep the anchors `status`, `application-status`, `unit-status`, `workload--charm-status`; run 1 adds `agent-status` and gives start-up and removal and the Kubernetes overlay their own sections; run 2 adds `status-in-output`, and puts the new-unit and Kubernetes cases under the workload status. Neither draft has a figure.

## A real disagreement

The tie rule for the application status.
- Run 1: "the status of the leader unit if the leader is among them, and otherwise the status of the unit with the lowest number".
- Run 2: "the status of the leader unit, or, when there is no leader, of the unit with the lowest unit number".

Source (`domain/status/service/status.go:558-606`, read at `e5db99d585`; the file has no diff at `52e983a435`): the units are sorted with the leader first and the rest ascending by ordinal, and the loop keeps the first unit with the highest severity (`>`, not `>=`). So the leader wins a tie only if the leader has the highest severity. If the leader exists and has a lower severity, the lowest-numbered unit of the highest severity wins. **Run 1 is correct; run 2's sentence is wrong when a leader exists but is not among the units with the top severity.**

This is the kind of error a single cold run can introduce. It supports running two independent reviewers and verifying every drafted statement, not only the findings.

## What this adds to the evidence

- Two independent runs reach nearly the same upstream defects; each adds findings the other missed.
- The drafts each contain a statement the other does not; at least one is wrong. The trace column in run 2 cited the source and the draft still misstated it, so a trace is a claim until a second reader checks it (reviewer agent, stage 2).
