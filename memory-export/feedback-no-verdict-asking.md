---
name: no-verdict-asking
description: "Stop asking the user for verdicts or option picks on writing/structure calls; untangle the knots until the right answer is obvious, then present it"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 5e68ea26-c714-4923-83c0-903502e1b0ab
  modified: 2026-09-29T21:30:15.830Z
---

Once the knots are teased out, the right answer should pop off the page. If it does not, the answer has not been found yet: keep thinking instead of handing the user a menu.

**Why:** the user said so on 2026-09-29 while reworking the architecture explanation (PR 4), after several turns where I ended with "which do you prefer?" questions and menus of options. Verdict requests push the thinking back onto the user.

**How to apply:** for prose, structure and diagram decisions, work out the causal chain, choose, make the edit, and report what changed and why. Ask only when a fact is missing that the code, the docs or the conversation cannot supply (for example, an unreadable image). Keep the user's own framing of the argument (they supply the vanishing point); test candidate wordings against it. Related: [[no-unearned-negation]], [[juju-pr-workflow]].
