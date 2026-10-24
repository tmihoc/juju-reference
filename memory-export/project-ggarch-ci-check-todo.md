---
name: ggarch-ci-check-todo
description: "The ggarch CI check was deliberately skipped in PR 4; when and how to add it, plus the PR 4 ggarch decisions"
metadata:
  type: project
---

PR 4 (architecture explanation, branch `4.1-docs-rewrite-architecture-explanation`) ships WITHOUT a ggarch CI check. Decided 2026-09-29: the docs build already turns a bad model into `ggarch parse/validate error` warnings and the RTD PR preview shows them, so the gate adds cost for little gain on a one-model POC.

**Why:** the docs `html` job is informational and RTD has `fail_on_warning: false`, so a broken diagram would not block a merge, but a new required check and a per-PR ggarch install are not worth it yet.
**How to apply:** revisit when several people edit `docs/juju.ggarch` or the model grows across the entity-reference PRs (plan item 5). Add ONE step to the existing `.github/workflows/docs.yml` (run on `docs/*.ggarch` changes): install ggarch from the pinned SHA, `ggarch check docs/*.ggarch`, fail on `ggarch parse/validate error` build lines. Later port the prep branch's grounding gate (`docs/tools/check-grounding.py`) with the entity pages. Full notes: `~/git/misc/juju-architecture/pr-split-plan-4.1.md` ("TODO: ggarch CI check"). Related: [[juju-docs-epics]], [[juju-pr-workflow]].

Other PR 4 decisions: ggarch pinned by full SHA in `docs/requirements.txt` (public repo tmihoc/ggarch), no committed SVGs (reviewers use the RTD preview), one model `docs/juju.ggarch` for the whole doc set, colour means ownership only.
