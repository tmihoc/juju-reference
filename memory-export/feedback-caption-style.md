---
name: caption-style
description: "Figure captions in the juju docs: technical detail lives in the caption, main text stays light, captions start with their subject and point (never 'The figure follows...')"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 11bbabe8-762f-40b8-8557-35a16d46409d
  modified: 2026-09-30T13:29:20.696Z
---

Captions carry the technical detail of the layer their figure shows (terms defined in brackets on first use). The main text around the figure stays light and does not repeat that detail. Start every caption with its subject and its point, like the other captions in the doc ("Juju sits between the user and the applications."). Captions that open with "The figure follows...", "This diagram shows..." are out of style.

**Why:** the user said so on 2026-09-30 on PR 23439 after I had shortened the topology caption to "The figure follows your goal state..." to satisfy a review-bot note about duplication and moved its details into the numbered steps. The user called the opener "really bad and different from all the other captions", and the layering (light text, technical caption at the relevant layer) is the internal guideline.

**How to apply:** when a reviewer says a caption duplicates the prose, cut the prose side, not the caption. Check every caption and slide caption before committing. The rule is written in `docs/agents/AGENTS.documentation.rules.md` (Diagrams section). Related: [[pr4-architecture-rewrite-state]], [[no-unearned-negation]].
