---
name: epic-9635-state
description: Epic JUJU-9635 is one PR on 4.1-docs-illustrate-docs-juju-9635 (worktree juju-tutorial-diagrams); pages done, order, ggarch pin, what is not pushed; resume from ~/git/misc/juju-reference/NEXT-PROMPT.md
metadata:
  type: project
---

One PR for the whole epic (user, 2026-10-20), branch `4.1-docs-illustrate-docs-juju-9635` in `~/git/misc/juju-tutorial-diagrams`, nothing pushed; commits: tutorial diagrams, SSH key page, cloud page, plus fixups to autosquash (`GIT_SEQUENCE_EDITOR=true git rebase -i --autosquash upstream/4.1`) before asking to push. ggarch pin `tmihoc/ggarch@000384e250377b3f57d7b4f75bb8ec14c66ec31e`. Next pages: model, SSH server (dissolve explanation/juju-ssh.md), space+subnet+zone, secret-backend, controller, machine. Held-back figures: local branch `4.1-docs-held-back-figures`.

**Why:** the user wants the epic resolved with content updated by the new skeleton, not figures dropped onto unsettled pages; the epic's topic list is only a source of ideas.

**How to apply:** read `~/git/misc/juju-reference/NEXT-PROMPT.md`, `page-recipe.md` and the end of `skeleton-v6.md`; PR description notes are in `pr-epic-notes.md` (the user will ask for the text). See [[page-form-rules]], [[juju-docs-epics]], [[juju-pr-workflow]].

Session 83 (2026-10-20): model page written (uncommitted in the worktree; commit plan in NEXT-PROMPT.md); next SSH server, then controller with a one-hour Agent-rule probe. Handoff: `~/git/misc/juju-reference/NEXT-PROMPT.md` (archived as prompts/session-84.md). The user allowed pushing to their ggarch repo; ask before any push to juju.

**Update 2026-10-21 (end of session 86):** pushed tip `21b7494df3`, sixteen reference pages rewritten. The user's priority: get all the reference docs into the new shape, in parallel batches (draft, review, fix, commit per page). PR title and text are in `~/git/misc/juju-reference/pr-description.md`; the next-chat prompt is `~/git/misc/juju-reference/NEXT-PROMPT.md`.
