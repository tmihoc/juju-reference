# Cold run 1, `status.md`: findings (recorded by the parent session)

The subagent could not write this file (its Write tool refused report files) and returned the findings as text. This is a condensed record of that report. Verified by the parent against the 4.1 source at `e5db99d585`: F1, F2, F5 (below). All other findings are the subagent's claims until traced; line numbers refer to upstream `status.md` and 4.1 source paths as the subagent cited them.

## Verified by the parent

- **F1 False (L71):** upstream says a new unit "starts in `maintenance/allocating`". Source: agent `allocating`, workload `waiting` with "waiting for machine" (machine clouds) or "installing agent" (Kubernetes) (`domain/application/service/unit.go:989-1009`).
- **F2 False (L71):** "unknown/idle after the install hook". `unknown` is set after the start hook when the charm has set no status (`internal/worker/uniter/operation/runhook.go:259-268`); the install hook sets `maintenance` (`runhook.go:209-217`).
- **F5 False (L53):** `terminated` is "being destroyed". It is set after the remove hook completes (`runhook.go:254-258`); during stop and remove the status is `maintenance` (`runhook.go:218-227`).

## Claimed, not yet verified

High: F6 (`unknown` is not "still setting up"; three triggers), F8 (priority order and tie rule: leader, then lowest unit number; app with no units is `unknown`), F13 (agent error shows as workload `error` and agent `idle`), F25-F27 and F30 (the figure's eight transitions are not Juju rules; prose defers to it for them).
Medium: F3, F4, F7 (the charm can set exactly four values), F9 (only the leader sets the application status), F10, F11, F12, F14 (agent table omits `rebooting` and `failed`), F15, F16, F17, F19 (sample output has an SLA column), F21, F28, F31, F32 (T8 gap, open Q1), F33 (no remediation for `error` or `blocked`).
Low: F18, F20 (scope claim larger than content), F22, F23, F24, F29, F34 (tie), F35, B1 (boundary tie), B2 (inbound anchors `status`, `unit-status`).

## Contract failures reported by the run

1. "X, with the rules that apply to each, are:" is Metalanguage in the contract; the page recipe prescribes a colon lead-in before lists. Conflict.
2. No defect type for a title or lede that claims more than the page covers (F20), or for a stale generated sample (F19).
3. Severity has no tier between "false" and "plausible example presented as a rule".
4. Figure rules assume records or software; nothing for a non-entity figure of charm-chosen transitions with no ggarch view.
5. The page recipe is for entity pages; none of its section grammar applies to `status.md`.
6. The recipe forbids linking CLI pages; T6 for this page is about `juju status` output.
7. The run could not use the page-rules or error checkers, or git history, so those rows are by eye and the boundary measures partial.

## Second verification pass (parent, same session)

- **F6 supported:** `unknown` is also produced when the agent is lost and the workload was not `error` or `terminated` (`domain/status/service/status.go:318-326`), and for an application with no units (`status.go:562-566`).
- **F13 supported:** a failed hook sets the agent status to `error` with message `hook failed: "<hook>"` (`internal/worker/uniter/uniter.go:893-919`).
- **F9 supported:** the application status is set through the leader (`domain/status/service/leaderservice.go:68-101`).
- **F14 partly supported:** `rebooting` and `failed` exist as statuses (`core/status/status.go:97-118`); whether each is set for unit agents in 4.1 is not traced.
- **F8:** the order `error 100, blocked 90, maintenance 80, waiting 70, active 60, terminated 50, unknown 40` (`status.go:544-552`) was verified in the earlier audit; the tie rule (leader, then lowest ordinal) is at `status.go:558-606`, seen in the same read.
- Still unverified: F7, F10 to F12, F15 to F17, F19, F25 to F27 (figure transitions) and F28.
