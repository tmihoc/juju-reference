# Review mode, trial 1 (by hand, 2026-11-05)

Purpose: test whether `method/review-mode-contract.md` can express the defects already known, with the right type and evidence, and what it cannot express. The reviewer (me) has read our PR, so this is a format test, not a cold run. Upstream is base `e5db99d585`.

## Findings on upstream

| # | Where | Quoted | Type | Evidence | Fix | Sev | Conf |
|---|---|---|---|---|---|---|---|
| 1 | `reference/status.md:19` | "it is the highest-priority status of the workload statuses" | Not enough (T10) | `domain/status/service/status.go:544-552` ranks `error 100`, `blocked 90`, `maintenance 80`, `waiting 70`, `active 60`, `terminated 50`, `unknown 40`; the page never gives the order | Add the order in prose at the application-status section | medium | determined |
| 2 | `reference/status.md:21-23` (figure `status.png`) | "illustration of the status ... and lists the reasons for the transitions" | Figure-only fact; Contradicts | The transitions exist only in the image; source derives the status from the units, with no transition table for it | Delete the figure; state the derivation and the order in prose | medium | determined |
| 3 | `reference/secret.md` (name regex sentence) | "Secret names ... `^([a-z](?:-?[a-z0-9]){2,})$`" | False | `core/secrets/createsecret.go:21,110`: the regex validates content keys | Say it of keys | medium | determined |
| 4 | `reference/secret.md` (Vault table) | "`mount-point`" | False | `internal/secrets/provider/vault/config.go:21`: `mount-path` | Rename | medium | determined |
| 5 | `howto/manage-models.md:407-419` | "Error: some agents have not upgraded ... `--ignore-agent-versions`" | Stale; Misplaced | No Go code raises the message; `IgnoreAgentVersions` is sent by the client and read by no server code; the how-to carries an error entry that belongs to the reference call | Delete; link to the call's errors | medium | determined |
| 6 | `reference/high-availability.md:20-22` (caption) | "use a database replicaset" | Stale | The 4.x database is Dqlite with Raft (`reference/database.md`) | Correct | low | determined |
| 7 | `reference/metadata.md` ("index.(s)json") | `streams/v1/index.(s)json` | Stale | `environs/simplestreams/simplestreams.go:333`: default `streams/%s/index2` | Correct | medium | determined |
| 8 | `reference/constraint.md` (lede) | "a constraint ... represents a minimum ... maximum" | Fine upstream; lost in our PR (see audit) | | | | |
| 9 | `reference/relation.md` (CMR section) | "If the network topology is anything other than flat ..." | Fine upstream; lost in our PR (see audit) | | | | |
| 10 | `reference/charm.md` (whole page) | `## Charm taxonomy` By substrate, function, role, architecture, generation; `## Charm anatomy` revision, channel | Grab-bag page | Audience: five taxonomy axes answer different questions (where it runs, what it does, how it attaches, how it is built, how it is written). Source owner: role is a relation fact (`principal` and `subordinate` also on `relation.md`, so Duplicate); generation is about authoring frameworks, not about a charm's contract; revision and channel are Charmhub release facts. Change coupling and reading path: 17 commits on the file; inbound links not counted | Open: measures 3 and 4 not run | medium | open(Q2) |
| 11 | `reference/metadata.md` (title) | "Simplestreams metadata" with image, agent binary and private-cloud steps | Mixed section; Category mix | The page holds the format reference, the product contents and the deployment steps (task); the steps are already in `howto/manage-metadata.md` | Split steps out; keep the format reference | medium | determined |

## Findings on our PR (same format)

| # | Where | Type | Evidence | Fix | Conf |
|---|---|---|---|---|---|
| P1 | `reference/relation.md` | Gap | Items 9 (a), (b), (c) of the audit | Restore in prose at the cross-model section | open(source check) |
| P2 | `reference/constraint.md` | Gap | Item 8 | Restore in the lede or in each key that it affects | open(source check) |
| P3 | `reference/status.md:4` | Stale | Meta description names "status transition diagrams" that no longer exist | Trim | determined |
| P4 | `reference/*.md` ggarch blocks | Withdrawn | I read the placement rule wrongly. The user's rule is that a figure sits at the top of the section it embeds in, at that section's scope, as a redundancy. The PR's blocks open their sections, which conforms. What remains to check per block is scope (the view depicts what the section covers, no more or less) and that the prose beneath states every fact | | | |
| P5 | `reference/secret.md` caption | Caption carries unique facts | "its owners sit to the left ... its revisions to the right" states layout, not a fact; the facts named (owners, revisions, grants) are in the prose | None: layout is not a statement | low, determined |
| P6 | `reference/image-metadata.md` | Broken address (duplicate index entry) | `{ref}metadata` and `{ref}image-metadata` both listed in `reference/index.md` | Drop one | low, determined |

## What the trial shows

- The format expresses all nine known upstream defects and the six defects of our PR. Each type found its test.
- Findings 1, 2 and 7 needed a source read to be determined; the contract's "Evidence" column forced that. A claim without evidence would have been Unverifiable.
- **Boundaries cannot be fully judged yet.** Finding 10 stays open because two of the four measures (change coupling, reading path) have no tool. Cheap to build: co-edit counts from `git log` and an inbound-link count from the labels graph. Both are mechanical.
- **The figure rule produced no placement finding.** My first reading (figure after the prose) was wrong; the user corrected it: top of the embedding section, at the section's scope. P4 is withdrawn. The open check is scope per block.
- **Not tested:** the error types (no per-call trace was run), the title test, the scaffold phrase scan, and precision (the reviewer already knew the answers).

## Next

1. Build the two boundary measures as scripts in `tools/` (needs approval, since `tools/` is a gate).
2. Run the error types on one call with its full trace (`secret.md`, `Adding secret backends`).
3. Cold run on `status`, `relation` and `constraint` in fresh agents (needs approval).
