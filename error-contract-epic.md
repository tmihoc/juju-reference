# Epic draft: Document and enforce Juju's error contract (Jira number TBD; drafted session 88, 2026-10-21)

## Description (short; paste into the epic)

Before: when a client — a person or an agent — hits an error, the docs have nothing to say. Juju's reference pages describe what things are, not what goes wrong with them; the how-tos carry scattered troubleshooting tips; the error texts, their codes, and their remedies live only in the source. Nobody can say whether the docs and the code agree, because nothing checks.

Target: every operation in the reference docs carries its client-visible errors — the exact message, its error code, what triggers it, and what to do — each traced to the source and kept true by a CI check that re-extracts the errors from the code and fails when a documented message or code drifts. The how-tos link their troubleshooting to these entries, so one contract explains every error, and the explanation cannot silently rot.

## Work to date (the first increment — done, in PR #23661)

- 960 error entries / 674 distinct messages, attached to 182 of the 204 calls on 33 pages in the PR preview-link set. This count excludes the changed log page. The entries give client-visible messages, codes, triggers, and remediation, traced to the 4.1 source during drafting and review. The counts describe documented entries, not a complete audit of every client-visible path.
- The method exists and is repeatable: facade extraction (`tools/extract_facade.py`) → read the code around each method (the extractor misses helper layers) → independent review → verify-then-apply fixes.
- Composition chains are documented explicitly where they were caught: the wrap segments a message acquires through layers (`saving S3 config: transitioning backend to S3: validating S3 credentials: …`), statuses that differ per route (400/413/415), and verbatim quirks quoted as-is (the code's own `minimum has prefix length is 7` typo).
- Error tracing surfaced code questions for the developers (in the PR text and the research `TODOS.md`) — errors that look like bugs or API irregularities.
- Recorded limitation: the error contract and access levels were traced from code, not verified against a live controller. A local probe exercised the model-defaults tag parser, wrapper and API error conversion, but not the facade.
  The PR includes a CI guard that matches messages against a repository-wide template corpus and checks machine-shaped code notes against the code vocabulary. It does not establish call/message/code attribution or cover every composition or source-only workflow trigger.

## What's left (the epic's streams)

| Stream | Work | Exit criterion |
|---|---|---|
| CI lint (the guard -- the heart of the epic) | Extend the guard in PR #23661 to cover relevant source-only changes and verify the documented call/message/code associations, including composed and parameterized texts. | A code change to an error text or code without a docs change fails CI, and vice versa; limitations and exclusions are explicit. |
| Coverage audit | Walk every client-visible error path the extractor misses — helper layers, HTTP routes, the control socket, db-shell messages — and diff against the documented set. | Every client-visible error is documented or explicitly excluded, on a list that says why. |
| Composed errors, generalized | For each composition chain a client can meet, document the outer wrap and the reason families it carries (the object-store review caught three missing wraps; make that class impossible). | No documented message is a fragment of what a client actually sees. |
| Verification by running | The "not verified by running" list: exercise documented errors against a live controller; cross-link integration tests that already assert the same strings. | Every documented message backed by a source citation or a runtime assertion. |
| Consumers | How-to troubleshooting links to the entries; triage the code questions with the developers (fix in code or explain in docs); optionally cross-reference from CLI error output. | A user hitting any error can reach the contract from where they hit it. |

## One-liner for the talk

674 distinct documented error messages, traced to the code with triggers and remediation, plus an initial CI guard whose limits are explicit.
