---
name: page-form-rules
description: The user's wording and structure rules for entity reference pages (definitions, no metalanguage, no table names, no CLI links, link jargon, gerund operations, figures first); full list in juju-reference/page-recipe.md
metadata:
  type: feedback
---

Rules the user gave while the SSH key page was written (about twenty rounds); the full list with reasons is `~/git/misc/juju-reference/page-recipe.md` and the end of `skeleton-v6.md`. The ones I broke most: every opening sentence is a definition (kind of thing plus what sets it apart), never "is how"; no metalanguage ("this section covers", counting intros); say what is true, never what is absent; the page's own subject is the grammatical subject; no CLI links or CLI-led sentences; no table names outside one closing paragraph; link or define jargon at first mention in each section; American spelling; `Required access`, not `Authority`; a list needs a substantive intro sentence; a figure comes first in its section and stands alone; operations are gerund subsections in the how-to's order; plain-noun chip labels, `context-record` for other pages' records.

**Why:** the user reads for clarity as a human and for retrieval as an AI reader, and keeps the docs client agnostic.

**How to apply:** check a new page against the recipe and `tools/check_page_rules.py` before showing it. See [[no-unearned-negation]], [[client-agnostic-sweep-todo]], [[caption-style]].
