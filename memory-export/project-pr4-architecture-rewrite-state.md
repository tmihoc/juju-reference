---
name: pr4-architecture-rewrite-state
description: "State at 2026-09-30 evening: the five 4.1 docs PRs after review round 1 (all pushed), PR 4 tip 1eef9f9f85, what is open"
metadata:
  node_type: memory
  type: project
  originSessionId: 11bbabe8-762f-40b8-8557-35a16d46409d
  modified: 2026-09-30T15:38:56.500Z
---

PR tips on the tmihoc fork (updated 2026-09-30 evening; upstream/4.1 = a0d308a3ff after #23436 MERGED; the user said HOLD rebases until their next merge, the others merge cleanly): #23427 PR 1 = 03ec8ddc55 (18 commits), #23434 PR 2 = 383746df0c, #23437 CLI links = 4bba4427f6 (rebased + force-pushed; CI attempt 1 of Unit Tests failed, cause unread, flake suspected), #23438 PR 3 = c4cd6f5912 (plain push: ports list in the hardening guide after Gvantsats' comment; approved by gfouillet and Gvantsats, nvinuesa and the bot pending), #23439 PR 4 = bfe919f92b (plain push: technical topology caption restored, steps lightened). Worktrees: ../juju-pr2, ../juju-pr3, ../juju-pr4, ../juju-upgrade-guide; PR 1 sits in a session scratchpad worktree (the `../juju-pr1` allowWrite entry did not apply mid-session); #23437 is in the main checkout.

**Later the same day (evening):** the five PRs above MERGED into upstream/4.1 (tip 70591a13ec); RTD build 4504812 then FAILED in the PDF step (no latex visitor for the ggarch node). Fix: ggarch 85546a9 (pushed to origin main) and juju PR #23449 (branch 4.1-docs-fix-rtd-pdf-build, 5f7714b89c; bot review: 0 issues). The docs pin is now 85546a97f1a5, not 9462603. After #23449 merges, confirm the next RTD 4.1 build is green. See [[check-every-docs-builder]].

**PR 4 (#23439) content:** four-section architecture page (problem, insight, basic topology, under the hood as Kubernetes/Machines slideshows), ggarch pinned at 9462603, no ggarch CI check (skipped on purpose). Bot round 1 handled: "Hook execution guarantees" section in `docs/reference/hook.md` (label `hook-execution-guarantees`, verified in the 4.1 uniter), topology caption cut to one sentence with the unit-agent/node/Unix-socket details moved into the numbered list, Python 3.11 note in CONTRIBUTING. PR text: ~/git/misc/juju-architecture/pr4-text.md (needs the hook-guarantees line; the user edits PRs by hand, gh is not installed).

**Open:**
- Merge hazard: #23427 adds `(jujuagentd)=` to `jujud.md`; #23438 renames that page to `jujuagentd.md` with the same label. Whichever merges second deletes `jujud.md` and keeps the label in `jujuagentd.md`. `docs/conf.py` and `docs/redirects.txt` also overlap across PRs.
- Bot asked to mirror ggarch under a canonical-owned org (owner decision); the ggarch CI check is due at PR 5a.
- Entity-reference split 5a-5d awaits the user's go-ahead (plan file `~/git/misc/juju-architecture/pr-split-plan-4.1.md`); the prep branch's hook.md execution diagrams belong to 5c.
- PR descriptions for #23434, #23436, #23437 and #23439 need hand edits; reply drafts were given in the conversation.
- Follow-ups: `juju.is` links (cmd/doc.go:22, docs/reference/log.md:26), robots.txt sitemap host, stale comment on hook.Info.MachineUpgradeTarget.

Persona and style decisions from earlier in the day still apply ("you" in prose, SRE only in diagram 1, User afterwards, diagram first in each section, links only in end-of-section See-more notes, tabs alphabetical). Related: [[juju-pr-workflow]], [[ggarch-ci-check-todo]], [[ggarch-session-notes]], [[no-verdict-asking]], [[tabs-alphabetical]].
