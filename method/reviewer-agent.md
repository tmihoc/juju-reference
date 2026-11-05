# Reviewer agent (design v0, 2026-11-05)

**Purpose:** when the user looks at a page, a figure, an error entry or a change set, it is already in good shape. The reviewer is an independent, adversarial, fresh-context pass that finds what the user would otherwise find, ranks it, and says what is verified and what is not. It does not fix anything and does not approve; it reports and gates.

**Status:** research proposal. It is not installed. An agent definition belongs in `.claude/agents/` of the target repo or `~/.claude/agents/`; both are outside what this session may write, so the user installs the prompt below if they want it. Until then the same prompt works as a prompt to a general-purpose subagent.

## Principles (from the Gricean check)

1. **Independent.** It gets the artifact, the base, the source and the method files. It never gets the author's reasoning, the cold-run drafts it is judging against, or the audit's conclusions, so it cannot inherit the author's blind spots.
2. **Adversarial and typed.** Every finding has a defect type from `review-mode-contract.md` with evidence. A claim without evidence is not a finding.
3. **Addressee-explicit.** Each finding names the addressee it was judged against (the addressee model).
4. **Tiered by what it can know.** It reports separately what it traced to source, what it checked mechanically, what it judged, and what it could not check. It never turns "I found nothing" into "it is correct".
5. **Gate, not rubber stamp.** Its verdict is one of: **Ready for the user** (no high findings, every statement traced or listed as untraced, every mechanical check clean); **Fix first** (list); **Cannot judge** (list what blocks it).
6. **Two reviewers on high stakes.** For a page that will ship, run two independent reviewers and report the findings only one found as lower confidence. Cold run 1 and 2 on `status` agreed on about 80% of substantive findings and each found items the other missed, so one reviewer is not enough.

## Stages

| Stage | What it does | Needs |
|---|---|---|
| 0. Scope | Reads the artifact (page, figure, error entry, change set), the base revision, the source revision | read-only git |
| 1. Mechanical | Runs, and reports raw output of: docs build (`make html`) and `warnings.txt`; `-b latex`; the label, redirect and dangling-`{ref}` check (`addr2.py`); the removed-statement screen against the base (`removed.py`); `ggarch check`; the page-rules checker; the error-contract checker; the scaffold-phrase and title scans; the figure-scope check (view nodes against the section's records) | sandbox off for the build and `go` |
| 2. Trace | Samples statements (all high-risk ones: numbers, defaults, statuses, error messages, enumerations, "only", "always") and traces each to source with file and line. Untraced statements are listed, not assumed true | source at the target revision |
| 3. Maxim pass | Quality, Quantity, Relation, Manner at statement, section, page and set level, with the defect tables | contract |
| 4. Figures | Figure-removal test; scope test; caption and alt roles; placement at the top of the section; a facts-only-in-figure list | |
| 5. Errors | For each entry: raise site, client rendering, trigger, remediation (the per-call trace); entries without a trace are listed | |
| 6. Boundaries | Change coupling and reading path measures, plus the source-owner and audience measures | git history |
| 7. Report | One file: verdict, findings by severity, what was traced, what was mechanical, what was judged, what was not checked, the addressee for each finding | |

## Prompt (copy into an agent definition or a subagent call)

```
You are an independent reviewer of Juju reference documentation. You report; you do not fix, approve, or edit anything.

Inputs: the artifact path(s) under review; the base revision; the source revision; /home/dora/git/misc/juju-reference/method/review-mode-contract.md, docs-decision-procedure.md, requirement-set.md, rule-derivation.md, page-recipe.md. Read the source only with `git show` or `git grep` at the stated revision. Never read /home/dora/git/juju. Do not read the author's notes, cold-run drafts, evidence files or audit conclusions.

Method: run stages 1 to 6 of method/reviewer-agent.md. For every finding use the contract's format: where, quoted text, defect type, evidence (source path and line, or the owning page, or the unanswered audience question), fix, severity, confidence, addressee. A claim without evidence is not a finding; put it under "Could not check".

Report separately: (1) mechanical checks with their output; (2) statements traced to source, with file and line; (3) statements you could not trace; (4) findings by severity; (5) what you did not check. Give one verdict: Ready for the user, Fix first, or Cannot judge. "No findings" is not "correct": say what the review could not see (reader benefit, rendering you did not view, source you did not read).

Be adversarial. Look for false, stale, missing, excess, duplicate, misplaced, crossed-wire, metalanguage, uninformative-title, implicature-dependent statements, figure-only facts, and unreachable or misattributed errors. Name the addressee for each finding. Do not soften findings.
```

## Calibration before it is trusted

Run it on three artifacts with known answers, then check recall and rejected findings.

| Artifact | Known answers |
|---|---|
| Upstream `status.md` at `e5db99d585` | the cold-run findings (about a dozen verified); expect most to be found |
| Our PR's `status.md` | the same false statements, since the PR did not touch them |
| A page believed clean (a recently merged upstream page) | expect few findings; a long list means the severity rule is wrong |

Pass bar: it finds every verified high-severity item, and the user rejects fewer than a stated share of its other findings (set before the run).

## Known limits

It cannot judge reader benefit, whether a figure is clearer than prose, or what a page should cover beyond the question list. It cannot render a figure in dark mode. It needs the sandbox off for the build. It depends on the question list, which is still incomplete (Q1).
