---
name: feedback-no-comma-and-clauses
description: "Do not glue two facts with different subjects using \", and\"; split them or name the relation. \"And\" for same-kind items or one subject's verbs is fine."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8b64a5ea-58c9-45cc-8be7-2ae725b82b31
  modified: 2026-10-20T21:58:24.492Z
---

The user hates sentences of the form "X does A, and Y does B" where the two clauses have different subjects and state different facts. Example they quoted: "A request can carry a batch of credentials, and the answer has one result for each." They said "and" is not always bad, only in these structures.

**Why:**
- The "and" claims a relationship (also, then, therefore) and never says which.
- The second clause leans on a vague noun in the first ("batch", "each of what?"), so the reader parses backwards.
- The cadence sounds like an explanation while the content is trivial.
- Two rules end up in one bullet, which cannot be scanned or cited.

**How to apply:**
- Two facts with their own subjects become two short sentences.
- A real relation gets its own word: so, then, because, when.
- Name the concrete thing ("takes a list of credentials", "each credential gets its own result"). No "batch", no "carry".
- "And" stays for same-kind items (three-item lists with the Oxford comma) and for two verbs of one subject.
- Applies to docs, commit messages, PR text, and chat replies.

See also [[feedback-no-unearned-negation]] and [[feedback-page-form-rules]].
