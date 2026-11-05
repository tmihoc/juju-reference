# Notes for the PR description of epic JUJU-9635 (single PR, branch `4.1-docs-illustrate-docs-juju-9635`)

The user will ask for the PR text later: write it against `upstream/4.1`, in a fenced block, never hard-wrapped, no Jira, target 4.1.

## Must be in the description
- **What the SSH key rewrite adds over 4.1's page** (user, 2026-10-20: "make sure to mention this"):
  - Fixes three inaccuracies: the definition ("accessing a machine provisioned by Juju individually": in 4.1 keys are not placed on machines after bootstrap, the controller's SSH server opens the session); "per-model cache of public SSH keys" (a key is stored once per user, a model authorizes it through a separate record); the CLI-led wording.
  - A correct mechanism, traced to code: the session lands as `ubuntu` through the controller, with passwordless sudo on machines Juju creates; on Kubernetes it is a shell in the unit's container through the Kubernetes API server.
  - Client-visible errors with their codes and messages, taken from the facade (`apiserver/facades/client/keymanager/keymanager.go`), each with trigger and remediation.
  - Required access and block checks per operation; two undocumented behaviors: removal ignores a target that matches no key, import can name any existing user (a question for Juju developers is in TODOS).
  - Effect of a model migration on keys.
  - Two figures: the data model with cardinalities (from the 4.1 controller schema) and a sequence for importing keys with the code cited per step.
  - Client agnostic: no CLI links; See also links to the Juju and Terraform how-tos.
- **Reviewers should check** (not verified by running): the block definitions, import for another user, the Kubernetes session identity, the cloud-init `ubuntu` sudo statement, and the removal rule.
- **Not covered by the epic's list:** storage, backup and restore, relation databag flow, cross-model relations.
- **Not yet reader-tested:** E44 showed no structural gain; the page's earlier gain came from added facts.
- **ggarch dependency:** pin moves to `tmihoc/ggarch` commit `aeb653ab3d08e4399f2ca5d4762ea0fed5f9aa0e` (branch `hide-fields`): `fields: hidden`, `charmed-entity`, `context-record`.
- **The explanation page `explanation/juju-ssh.md` is dissolved** into a reference page `SSH server` (content is reference, not explanation; moves the four existing diagrams; keeps the `juju-ssh` label; redirect added; history to release notes).
- **Cloud page, to verify:** the change streams paragraph says only the broker worker of a Kubernetes model watches the cloud spec (`internal/worker/caasbroker/broker.go:136-181`, `apiserver/facades/agent/caasagent/caasagent.go:99`); `CloudSpec` contents (definition, region, credential) stated from reading, not traced.

## Model page (session 83): corrections and facts for the PR
- The page replaces a 35-line page; it adds the data model across the controller and model databases, change streams, and seven operations with required access, rules, and errors (about 40 messages with trigger and remediation).
- Corrections found from the code: the migration is superuser-only; every user with access must exist on the target (and external users need the same identity provider); the agent version cannot exceed the controller's and needs binaries; log transfer is skipped when Loki forwarding is on; a migration cannot be aborted after `validation`; `reap-failed` leaves the model live on the target; a workload model upgrade can cross minor versions up to the controller's version although its error says "patch version increase"; the controller model upgrades by patch version only; the 4.1 server has no "agent version skew" error; the old how-to messages for a missing owner differ from 4.1's.
- Not covered on the page: model workers (belong with the controller page), block commands and model defaults as entities, operator troubleshooting beyond the error lists, recovery of agents that do not restart after an upgrade (how-to keeps it).
- Unverified by running: see `NEXT-PROMPT.md`, "Known weak spots".

