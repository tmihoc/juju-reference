---
name: separate-review-commits
description: "Commit reviewer-driven fixes as separate commits, not fixups squashed into the original commits"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 11bbabe8-762f-40b8-8557-35a16d46409d
  modified: 2026-09-30T11:48:40.759Z
---

When you commit fixes in response to a reviewer, make separate commits (one per reviewer concern or logical fix), each with a conventional-commit subject and a detailed body naming the review feedback. Push them as ordinary commits on top of the branch.

**Why:** the user said so on 2026-09-30, right after review round 1 on the five 4.1 docs PRs, where I had folded every fix into the original commits with `amend!`/`fixup!` plus autosquash and force-pushed. Separate commits let reviewers see exactly what changed since their last look.

**How to apply:** this replaces the fixup/autosquash/force-push routine in [[juju-pr-workflow]] for review feedback: commit on top, push normally (no force), still ask before every push. Keep autosquash only for cleanups the user asks for explicitly. The round-1 pushes of 2026-09-30 (PRs 1-4, #23436, #23437) were squashed into the original commits; apply this rule from round 2 onward.
