---
name: entity-reference-form
description: "Entity reference pages take the ADR-016 layer-anchored form; rolled out to all 24 entity pages, branch pushed to origin; resume from ~/git/misc/juju-reference/pr-entity-reference-layers.md (PR text against upstream 4.1, open items)"
metadata:
  node_type: memory
  type: project
  originSessionId: 4a023ab4-794c-4538-aad3-4820d3c2141e
  modified: 2026-09-30T15:47:06.890Z
---

**Resume here:** `~/git/misc/juju-reference/pr-entity-reference-layers.md` holds the PR title and description (written against upstream 4.1), the compare link, the preview script, the open items and the list of 4.1 prose the restructure drops (charm channels, secret identifiers, machine base, action workflow, credential notes, relation figures). Restoring it, deleting the orphaned relation images and pushing the extra commits await the user's go.

Entity reference pages follow ggarch ADR-016: no free-standing rules-and-errors list; declaration anchored by lifecycle action, persistence by stored record component, execution by operational loop; sentence case; every verified fact, link, anchor and error string kept. Page types and the form: `~/git/misc/juju-reference/{reference-page-types,entity-page-form}.md`, tools in `tools/` (`raise_sites.py`, `loss_check.py`), removed diagram fences in `fence-manifest.md`.

**State (2026-09-30):** all 24 type 1-2 pages are rolled out on branch `4.1-docs-entity-reference-layers`, worktree `~/git/misc/juju-entity-ref` (25 commits on upstream/4.1 70591a13ec, tip 2576a81b14, PUSHED to origin; PR not opened yet; baseline worktree `~/git/misc/juju-base`). Build clean against baseline. Diagrams not ported (41 fences removed; 4.1 docs/juju.ggarch has only the architecture views). Types 3-11 not yet checked against 4.1. Live preview: `~/git/misc/juju-reference/preview-entity-ref.sh` (port 8001).

**Why:** the user wants diagnostic locality. The prep branch pages were a source of structure, not truth: the raise-site pass corrected many errors and stale 4.1 facts (see ADR-016 "Rollout"). A PR is reviewed against its base: the user pointed out the first PR text was written relative to the prep branch.

**How to apply:** per page, resolve each error to its Go constant and raise sites, file by layer, read the source page in FULL (never a clipped preview), stack old anchors, run the shingle fidelity check against BOTH the prep page and the base branch's (upstream/4.1) page, build purged (sandbox off) and diff warnings against the baseline. Push to origin only, never upstream, and ask first. PR text in a fenced block, written against the base branch, no Jira. The user's own DPE improvement ideas are still to come: ask before proposing. Related: [[pr4-architecture-rewrite-state]], [[no-verdict-asking]], [[ggarch-session-notes]], [[separate-review-commits]].
