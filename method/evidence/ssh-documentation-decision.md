# How SSH should be documented: a decision by the requirement set (2026-11-05)

**Status:** a decision produced by `method/docs-decision-procedure.md` v2 and `method/requirement-set.md`, with each step traced. It changes no page. Source: the 4.1 anchor `e5db99d585` and the PR worktree at `48ef1fca17`. The deleted page is `docs/explanation/juju-ssh.md` (added by the maintainers in `25668c0cca` and `d2cf9fc1fb`, removed by this PR in `bf7f6491e4`).

## Decision

1. **The SSH server is documented by one reference page, `reference/ssh-server.md`.** Keep it.
2. **No explanation page for the SSH proxy mechanism.** The deletion of `explanation/juju-ssh.md` is right.
3. **`reference/ssh-key.md` stays a separate reference page** for the key and its authorization on a model. It links to the server page and does not restate it.
4. **The `juju ssh` and `juju scp` flags, defaults and examples are owned by the command help text** in the source, which the generator publishes. Hand-written pages do not copy them.
5. **How-tos carry the tasks:** `manage-machines.md` (connect, print the OpenSSH command, connect when the proxy is unavailable), `manage-units.md` (Kubernetes units), `manage-ssh-keys.md` (keys). Each links to the reference for what happens.
6. **The change of default and the removal of `--jump` belong in the release notes and the upgrade guide**, never in a reference or how-to page.
7. **No rationale text for now.** An explanation of why the controller proxies SSH is added only when its rationale is evidenced; today it is not (see the audit).

## Trace

| Step | Result |
|---|---|
| Surface class (procedure step 1) | A cross-cutting mechanism with records (host keys, connection requests), watchers (port, configuration, connection requests), calls (finding the server, addressing, host keys, answering requests, relay) and a listener. Kind: Change. |
| Page or section (R11, R18) | It has its own records, its own facade calls and its own configuration, so it is a page of the entity grammar. The deleted page was the same subject in another category. |
| Category (R8) | Reference states what happens and under which conditions. Explanation gives evidenced rationale. Splitting the deleted page by statement gives the audit below; nothing is left that is explanation. |
| One owner (R16, R17) | The deleted page restated the mechanism that `ssh-server.md` states in more detail, with its source-checked rules and errors. Two pages for one mechanism is the duplication R17 forbids. |

## Audit of the deleted page, statement by statement

| Statement | Class | Where it lives now |
|---|---|---|
| "Juju 4.1 introduced changes... Previously Juju let users connect directly..." | History of a version | Release notes and the upgrade guide (R23, T7). Not a page statement. |
| An SSH server in the controller on port 17022; the existing commands are proxied | Mechanism (reference) | `ssh-server.md` lede |
| Two SSH connections, a fixed outer host key and a virtual inner host key | Mechanism (reference) | `ssh-server.md` > connecting to machines, with the slides |
| Kubernetes targets through the API server; machines through a reverse tunnel | Mechanism (reference) | `ssh-server.md` > connecting to Kubernetes units; > answering connection requests |
| The client verifies host keys through the API; another client must verify them by hand | Mechanism plus task | `ssh-server.md` > checking host keys; `manage-machines.md` > print the OpenSSH command |
| Authentication by stored key, authorization needs model admin, session runs as `ubuntu` | Mechanism (reference) | `ssh-server.md` Caller and Rules; `ssh-key.md` |
| Needs the controller and, for a machine, its agent; alternatives are cloud tools and cloud-init | Rule plus task | `ssh-server.md` rule; `manage-machines.md` > connect when the proxy is not available |
| Goal: connect without direct network connectivity | Rationale, evidenced by the behavior | The `ssh-server.md` lede ("with no direct network path from the client to the target") |
| Goal: avoid storing user credentials on machines, with a central view of who has access and when they log in | Rationale | Not carried. The source shows central authorization but no login record; the "when they log in" part is not evidenced. |
| "Allowing Juju to inspect any commands before they reach the destination" | Capability claim | Not carried. The SSH server worker proxies sessions and does not inspect or log commands at the anchor (`internal/worker/sshserver/proxy.go`); the command help says audit logging is intended for the future. The lede says only that Juju "can check who connects and to what", which the authorization code supports. |

## Why this is a clear conclusion and not a preference

- The deleted page has no statement that only an explanation can carry. Every statement is reference, a task, history, or a claim the source does not support.
- Keeping it would create two owners for the same mechanism, and it would carry one claim (command inspection) that is false today (Quality).
- The destination pages already contain what the page carried: the how-to has the proxy alternatives, the `--show-command` task and the port, and the reference has the rest.

## Residual checks (not decided here; each has a test)

1. **Old heading fragments.** `redirects.txt` maps `explanation/juju-ssh` to `reference/ssh-server`, but the old fragments (`#ssh-proxy-architecture`, `#authentication-and-authorization`, and so on) do not land anywhere. Test a fragment-aware redirect before claiming R15 is met.
2. **Wording in `manage-machines.md`** says "a full explanation" and links the reference page. Change it to say what the reader gets (what happens, the rules and the errors).
3. **Release notes and upgrade guide** for the changed default and the removed `--jump`: check that entries exist (procedure step 6). Not checked here.
4. **Overlap of `ssh-key.md` and `ssh-server.md`** on the `ubuntu` account and root access: each fact needs one owner. The server page owns "a session logs in as `ubuntu`"; the key page owns "authorizing a key grants root". Verify the sentences match that split.
5. **Diagram views.** The maintainers' model had four views (`SSH proxy overview`, `SSH proxy connections`, `SSH proxy Kubernetes`, `SSH proxy machine reverse tunnel`). The PR's model keeps `SSH proxy connections` and `SSH proxy Kubernetes`, and has replaced the other two with the sequences `Connecting to a machine: authorization` and `Connecting to a machine: reverse tunnel`. The reference page embeds all four. Nothing is lost, but the first view's role (an overview of client, controller and target) now rests on the first slide of `SSH proxy connections`; verify that slide does not omit the overview's content.
