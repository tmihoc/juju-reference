# Reader model (draft v0, 2026-11-05)

**Status:** research proposal. The five audiences below come from `archive/work/docs-paradigm-draft-104.md` (section 2) and R3 in `requirement-set.md`; everything else is new and unverified. The aim is a model of the readers that the maxims are judged against: who they are, what they are trying to do, how they reach a page, what they know, and what a wrong or missing statement costs them.

## Two layers, not one list

1. **The person** (what they want to do): an operator, a charm developer, a client developer, an incident inspector, and the readers still missing from the list.
2. **How the words reach them** (the channel): reading a page, searching, asking an AI assistant that has our docs, or an AI agent acting on their behalf. Each channel changes what a page must contain (the AI sees one retrieved section, asks no clarifying question, repeats a false statement confidently, and takes silence as absence).

The earlier rule that the AI reader "changes how pages are written and never what goes in" is probably too strong. An AI that answers a task question needs conditions, remediation and the limits of a rule written out. That is added content.

## Profile fields (filled for each person)

| Field | Question it answers |
|---|---|
| Goal and tasks | What are they trying to do, in their words? |
| State | Incident under pressure, learning, designing, or auditing? Under pressure a reader wants the cause and the action, and has no patience for background. |
| Entry | How do they reach the page: search, an error message pasted into an AI, a link from a how-to, the sidebar? |
| Knows and does not know | Juju terms, the cloud, Linux, Go, SQL, Kubernetes? |
| Channel | Page, AI assistant, agent, or screen reader? |
| Cost of a false statement | Lost hours, data loss, a failed upgrade, a security gap? |
| Cost of a missing statement | Blocked, or able to find it elsewhere? |
| Typical questions | Scenarios in their words, used as the closed-book and task tests |
| Evidence | Where we know this from: issues, support questions, Matrix threads, the user's own experience |
| Confidence | determined, plausible, or guessed |

## Persons: current, and candidates to add

| Person | Source | Notes |
|---|---|---|
| Operator or SRE | Existing | The most common reader of reference. Needs status, logs, errors and remediation; usually under time pressure. Splits into the person who runs a long-lived controller and the person who deploys applications. |
| Charm developer | Existing | Bounded to what Juju does toward the charm (hooks, status, secrets, relations), not charm craft. Reads while writing code; wants exact semantics and ordering. |
| Client or tool developer | Existing | Includes people writing against the API, the Terraform provider and AI agents. Needs exact calls, strings and codes. |
| Storage or incident inspector | Existing | Reads the database. Smallest group; needs the records and their invariants. |
| Juju developer | Existing, excluded | The code is their documentation; included only in a labeled corner. |
| Platform or cloud administrator | Candidate | Installs and sizes a controller, plans HA, backup, upgrade and ports. Covers T4 and T5. |
| Evaluator or newcomer | Candidate | Decides whether Juju fits and follows the tutorial. Served by tutorial and explanation more than reference. |
| Security and compliance reviewer | Candidate | Asks who may do what, what is stored where, what is logged. Served by access levels, secrets and the database. |
| IaC practitioner (Terraform, Pulumi) | Candidate | A client developer whose client is a provider. |

## What I know and what I need from you

Known (from the archive): the five audiences and their question lists, the AI reader as the union, the inclusion test (true, meetable, asked for).

Unknown: who actually reads the reference, with what questions, and in what state. Without that the closed-book and task tests measure my guesses.

Needed from the user, as the domain expert:
1. The readers you see most (and the ones you wish you saw). A line each is enough.
2. Real questions you remember: from support threads, Matrix, issues, feedback. Even five per person is useful. Where they live, so I can harvest more.
3. The incidents or tasks that go wrong for each person: where the docs have misled someone, or where people give up.

## What the model is used for

- The addressee on every finding (`review-mode-contract.md`).
- The scenarios for the task tests (a person, a state, a channel, a question, the correct action traced to source).
- The weights: a false statement costs an operator in an incident more than a missing background paragraph.

## Not settled

Whether the AI assistant is a reader or a channel (this file treats it as a channel). Whether the person list should be fixed or whether a page declares its audience. How to weigh two readers when their needs conflict (an incident reader wants the action first, a developer wants the semantics first).
