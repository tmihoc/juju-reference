# Epic draft: Document and enforce Juju's error contract (Jira number TBD; drafted session 88, 2026-10-21)

## Description (short; paste into the epic)

Before: when a client — a person or an agent — hits an error, the docs have nothing to say. Juju's reference pages describe what things are, not what goes wrong with them; the how-tos carry scattered troubleshooting tips; the error texts, their codes, and their remedies live only in the source. Nobody can say whether the docs and the code agree, because nothing checks.

Target: every operation in the reference docs carries its client-visible errors — the exact message, its error code, what triggers it, and what to do — each traced to the source and kept true by a CI check that re-extracts the errors from the code and fails when a documented message or code drifts. The how-tos link their troubleshooting to these entries, so one contract explains every error, and the explanation cannot silently rot.

## Work to date (the first increment — done, in PR #23661)

- 956 error entries / 674 distinct client-visible messages, attached to 182 of the 204 calls on 33 of the 34 pages (34 with the model-migration records page, which points at the model page's call). Each entry: the message verbatim, its error code (matched to `apiserver/errors`; HTTP status for routes), trigger, remediation. Every entry was traced to file:line in the 4.1 source during drafting and review; the per-entry citations become a generated, checkable artifact with the CI-lint stream. Counted against the upstream 4.1 tree: every documented entry re-checked against it; the pages keep no entry the 4.1 code does not raise.
- The method exists and is repeatable: facade extraction (`tools/extract_facade.py`) → read the code around each method (the extractor misses helper layers) → independent review → verify-then-apply fixes.
- Composition chains are documented explicitly where they were caught: the wrap segments a message acquires through layers (`saving S3 config: transitioning backend to S3: validating S3 credentials: …`), statuses that differ per route (400/413/415), and verbatim quirks quoted as-is (the code's own `minimum has prefix length is 7` typo).
- Error tracing surfaced code questions for the developers (in the PR text and the research `TODOS.md`) — errors that look like bugs or API irregularities.
- Recorded limitation: everything was read from the code, never run — the PR text carries the "Not verified by running" list.

## What's left (the epic's streams)

| Stream | Work | Exit criterion |
|---|---|---|
| CI lint (the guard — the heart of the epic) | Close the loop: a checker that parses the documented (message, code) pairs and verifies them against the source. Must handle composed errors (match the wrap skeleton and its reason slot, not the literal string) and parameterized texts (`"<name>"`, `<n>` → template matching). Wire into docs CI against the pinned Juju version. | A code change to an error text without a docs change fails CI, and vice versa. |
| Coverage audit | Walk every client-visible error path the extractor misses — helper layers, HTTP routes, the control socket, db-shell messages — and diff against the documented set. | Every client-visible error is documented or explicitly excluded, on a list that says why. |
| Composed errors, generalized | For each composition chain a client can meet, document the outer wrap and the reason families it carries (the object-store review caught three missing wraps; make that class impossible). | No documented message is a fragment of what a client actually sees. |
| Verification by running | The "not verified by running" list: exercise documented errors against a live controller; cross-link integration tests that already assert the same strings. | Every documented message backed by a source citation or a runtime assertion. |
| Consumers | How-to troubleshooting links to the entries; triage the code questions with the developers (fix in code or explain in docs); optionally cross-reference from CLI error output. | A user hitting any error can reach the contract from where they hit it. |

## One-liner for the talk

674 distinct error messages, extracted from the code, each with its code, trigger, remediation, and a file:line citation — and a checker that keeps them true.
