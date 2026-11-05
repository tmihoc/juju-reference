# Notes on the run

## Access and boundary
- The Bash sandbox failed to start (apply-seccomp, nested userns). I re-ran the read-only `git -C ... show` and `git grep` commands with the sandbox disabled, because they were the only permitted way to read upstream. No working tree was read. No file under /home/dora/git/juju or juju-reference-principles was read. I read only the two contract files and wrote only into status-blind/.
- Found no prescribed section template in the contract or the ledger ("The contract fixes no section structure for a page"). None was followed.
- One file, `old-status.png`, sits in the output folder (the old figure, written for viewing as the task allowed).

## Method failures and limits
1. The question list has no entity-scope question, so nothing decides whether machine, model, relation, and storage statuses belong here. Logged as open(Q1).
2. An inbound anchor (`unit-status`) shaped the structure (parent heading). The method has R15 for addresses but no statement of how far anchors may drive structure.
3. The Fig ledger forbids a transitions figure unless every arrow is enforced. The only enforced transitions are the Juju-set lifecycle steps; I put them in an ordered list. The method does not say whether an ordered list of enforced steps is a Workload-status fact or a unit-life fact; I made it a section.
4. The contract's Stored-but-never-shown test applied cleanly to agent `error` (DSS 418-439). It had no test for a value that is shown only under a model type (Kubernetes override).
5. T3 asks for remediation, but the allowed sources hold little: only the hook-tool doc for `blocked` messages. I did not add remedies I could not trace.
6. Partial trace: the setter of `state.StatusSet` (RH 212, 248) was not read, so "the charm has set no status in any hook so far" rests on how the field is used, not where it is written. Marked in trace D18. The rendered text of `statuserrors.UnitNotLeader` was not read; the draft quotes the hook-tool doc text.
7. The full set of hook tools that touch agent status was not enumerated; the draft says only that `status-set` sets only the workload status (corrected during tracing, trace C1).

## Source observations beyond the page
- The message in DSS 324 names `juju debug-logs`; the command is `debug-log` in other places I did not read. Not verified. Not used in the draft.
- CS 14-16 comment says status "applies to ... workloads as well, which we don't currently model, for no very clear reason"; and `ValidWorkloadStatus` (CS 385-398) accepts six values while the hook tool accepts four (SS 130-135): the platform accepts `unknown` and `terminated` for application status via `encodeWorkloadStatusType` (DSS 150-172), so a leader could in principle set `unset`, `unknown`, or `terminated`; no hook tool path was found for it. Not stated in the draft.
- Pod `running` case (DSS 512-517) yields the status value `running` as the displayed workload status when the charm's status is unset or a creation waiting message; this looks surprising. Left out of the draft; worth a probe.

## Draft style check (self)
Oxford commas, ` -- ` not used in the body (no parentheticals needed), no metalanguage ("below", "this page"), no figure. The lead of the severity list and the lifecycle list name the kind of list. Two uses of "not"-shaped statements remain ("unless another unit is in `error`" is a condition, kept).
