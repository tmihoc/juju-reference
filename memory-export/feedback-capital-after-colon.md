---
name: capital-after-colon
description: "In prose, comments, commit messages and PR text, capitalize the first word after a colon when a full proposition (clause) follows"
metadata:
  node_type: memory
  type: feedback
  originSessionId: db19251f-8c6b-43fd-8330-22792539a403
  modified: 2026-09-29T16:15:46.492Z
---

Start with a capital letter after a colon when what follows is propositional (a full clause), e.g. "NOTE: In Juju 4.1 this limit is not implemented: It was not carried over." Lists, labels and fragments after a colon stay lowercase.

**Why:** the user corrected this on PR 2 (2026-09-29).
**How to apply:** check Go comments, doc prose, commit bodies and PR text before committing or presenting them. Related: [[juju-pr-workflow]].
