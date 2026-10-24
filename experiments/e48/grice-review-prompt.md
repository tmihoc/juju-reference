# Grice review of one reference page (session 85; the nine runs failed with a 402 before any finding)

Use with `agent: task`, one page per agent, read-only. Replace PAGE and the code areas.

Review `docs/reference/PAGE.md` in `~/git/misc/juju-tutorial-diagrams` against Grice's four maxims. Read `page-recipe.md` first. Never edit a file, never run a build, never touch `~/git/juju`. The code is `~/git/misc/juju-v2-preview` (4.1); DDL copies are in `experiments/e11/{controller,model}.ddl`. Figure sources are in `docs/juju.ggarch` (read the view, the `:caption:` and the `:alt:`).

- QUALITY: trace every factual claim (access level, block, rule, default, error text and code, count, name, order) to a file:line. UNTRACED if you cannot; FALSE if the code contradicts it. Error texts must match the code; codes must match `apiserver/errors/errors.go`.
- QUANTITY: a fact belongs only if an interface shows it (API method, parameter, result, error text, CLI output, hook tool, route, db shell). Flag Go identifiers, worker names and table names used as explanation beyond that, and any operation or rule a client would meet that is missing (compare with the facade methods).
- RELATION: flag facts that belong on another page, facts stated twice, operation rules in a data model section (a data model rule must be enforced by the database: unique index, not null, check, foreign key, trigger, or a fixed lookup; cite the DDL line), sentences that anticipate the next block, metalanguage.
- MANNER: jargon not linked or defined at first mention in each section; negation about absence nobody expects; a lede longer than a definition plus two sentences; a list not introduced by a paragraph that ends in a colon; a caption or alt text that states a fact the figure does not show or omits one it does (check nodes, edges and cardinalities against the DDL foreign keys); inconsistent names; British spelling; missing Oxford commas; remediations that state a consequence instead of an action.

Output: a table, most serious first, at most 30 rows: line | maxim | label (FALSE / UNTRACED / MISSING / MISPLACED / UNCLEAR) | problem in one sentence | evidence | exact replacement wording. Then the counts. If a call fails with a provider error, say so and stop.
