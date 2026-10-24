---
name: oxford-comma
description: Use the Oxford comma in every list of three or more, in docs, comments and PR text
metadata:
  type: feedback
---

Write "a, b, and c", never "a, b and c".

**Why:** the user (2026-10-20) asked for it after seeing "required access, rules and errors" in a reference page, and said "here and everywhere else".
**How to apply:** every list of three or more in pages, captions, alt text, commits and PR text. After editing prose, scan for ", X and Y" patterns. Recorded in `~/git/misc/juju-reference/page-recipe.md`. See [[feedback-page-form-rules]].
