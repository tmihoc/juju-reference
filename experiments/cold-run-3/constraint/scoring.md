# Scoring sheet: constraint page

Columns: upstream at 52e983a435 and the cold output (`draft-constraint.md`). The "Our PR" column is not available to a cold run and is left empty. Rows that need the checkers, the builds, or the boundary measures from history are marked "parent" and left for the parent session.

| Measure | Upstream | Our PR | Cold output |
|---|---|---|---|
| Statements failing the source trace | 16 of 49 claims (list below) | n/a | 0 of 114 trace rows fail. Rows resting on help text or on judgment only: V4, and the remediations S10, V10, C3 (marked in `trace.md`). The EC2 source conflict (F5) is stated as two traced facts (K5, K6) |
| Facts upstream had that are stated nowhere (losses) | n/a | n/a | 0 true facts lost. Dropped on purpose: the false or unverifiable statements as written (U3, U5, U9, U12, U14 as flat, U15, U16, U20, U22 as flat, U25 as flat, U27, U36, U43, U45, U47 as incomplete, U48), the `versionadded` and "Juju 3.6" scopes (R23), and "more commonly" (no source). Rephrased and kept: all 16 key entries, the three examples, the `--base` fact, the root-disk exclusion of attached storage |
| Gaps against the question list | T1 met; T3 missing (no errors, no unsupported-key behavior); T4 half (support notes on 8 of 16 keys, wrong on 4); T9 wrong; T10 half (precedence flat); T2, T5, T6, T7, T8 not in scope or absent (T6: the commands that show constraints are not named; T7: the `cpu-cores` deprecation is not stated). Count: 5 gaps (T3, T4, T6, T7, T10) plus T9 wrong | n/a | T1, T3, T4, T9, T10 met; T6, T7 met in one clause; T5 (what happens at migration or upgrade) not addressed: `domain/constraints/modelmigration` exists and is unread; T8 (client developer: which call carries constraints) not addressed. Count: 2 gaps (T5, T8) |
| Excess statements | 2 (U9 "generic note" pointer; "The rest of this document ...") | n/a | 2 candidates: the per-cloud lists of valid `arch` values (P9) and the Azure `dual` errors (P14) duplicate cloud pages and are kept on judgment (tie); no statement fails the removal test as flat excess |
| Errors: traced entries; entries with a finding | 0 entries; 0 findings (gap F20 counted under gaps) | n/a | 15 error forms documented, all traced to raise sites (S7-S9, C2, V9, K7, K14, K20, K25, K44, K45, K47, K51, K64, K74). 0 with a finding I can show; 1 caveat: the client wrapper of the parser messages (gnuflag) was not traced, so "Wrong message" cannot be ruled out. The parser errors have no code; the contract's error format requires a code (see notes) |
| Figures: figure-removal test failures | 0 figures | n/a | 0 figures; the page has no relational fact that earns one under R26 (a table of key against cloud support was considered and rejected, see notes) |
| Manner findings (titles, scaffolding, mixed sections) | 6: H2 "List of constraints"; metalanguage at "The rest of this document"; "Below this is indicated"; `<p>`/`<br>` layout markup; British spelling; section mix (concept intro and key reference are fine, the caution block mixes support policy with the lede). Count: 6 | n/a | 1 candidate: "The sixteen constraint keys, in alphabetical order, are:" leads into headings, not a list (a lead-in whose content is structure); "Cloud support for constraints" mixes the unsupported-key rule, the invalid-value rule, and links (three facts, one subject; mixed-section test says tie) |
| Page rules and the error checker | parent | n/a | parent |
| Blind rank (user, 1 to 3) | parent | n/a | parent |

Not measured here: the builds (html, latex), the ggarch check, and `check_page_rules.py`. The draft was written to the text rules by hand.

## Upstream claim extraction (stage 1) and verdicts

49 claims, one checkable statement each. F = failing the trace, with the finding.

| Id | Line | Claim | Verdict |
|---|---|---|---|
| U1 | 10 | A constraint is a key-value pair passed to certain commands or flags | pass |
| U2 | 10 | It customises compute resources of four kinds | pass |
| U3 | 12 | Bare metal or VM: a constraint is a minimum; system or Kubernetes container: a maximum | F (F1) |
| U4 | 14 | Constraints can be set directly on machines of machine clouds | pass |
| U5 | 14 | More commonly set at controller, model, or application | F, Unverifiable frequency and loose "controller" (F16) |
| U6 | 14 | The more specific level takes precedence | pass, with a Not enough (F16) |
| U7 | 16 | The document describes all the existing constraints | pass (16 of 16) |
| U8 | 20 | Availability and meaning of keys vary by cloud | pass |
| U9 | 20 | The variation is indicated with a generic note below | F (F17) |
| U10 | 30 | allocate-public-ip determines whether machines get an externally reachable address | pass |
| U11 | 30 | Valid values true, false | pass |
| U12 | 30 | Applies to GCE, EC2, Azure, and OpenStack | F (F5) |
| U13 | 30 | Public cloud instances get a public IP by default | pass for GCE and Azure; flat for OpenStack (F6, low); counted pass |
| U14 | 35 | arch valid values are the five | F (F7) |
| U15 | 40 | container: a machine must be the specified container type | F, Unverifiable (F8) |
| U16 | 40 | container valid values: lxd | F (F8) |
| U17 | 45 | cores: number of effective CPU cores; integer | pass |
| U18 | 45 | Alias cpu-cores | pass (incomplete, F9) |
| U19 | 49 | cpu-power: abstract CPU power; integer | pass |
| U20 | 49 | 100 units is roughly a 2007-era Xeon, as reflected by 1 Amazon vCPU | F (F10) |
| U21 | 49 | In Kubernetes a unit of milli is implied | pass |
| U22 | 49 | Not supported by all providers; use cores for portability | F (F11) |
| U23 | 54 | image-id: the machine must use the specified image | pass |
| U24 | 56 | Not supported by all providers; provider-specific value | pass |
| U25 | 56 | With deploy it must be used with --base | F (F12) |
| U26 | 61 | instance-role: the role or profile for the cloud is used | pass |
| U27 | 61 | Only AWS and (from 3.6) Azure | F (F13) |
| U28 | 66 | instance-type: cloud-specific name | pass |
| U29 | 66 | Values vary by provider, and individual deployment in some cases | pass (the names come from the account), ambiguous (F14) |
| U30 | 66 | Use cores, mem, root-disk for cross-cloud compatibility | pass |
| U31 | 71 | ip-family added in 4.1.0 | pass for truth; R23 violation (F15) |
| U32 | 74 | Valid values ipv4, ipv6, dual | pass |
| U33 | 74 | ipv6-only is not supported by any provider | pass |
| U34 | 77 | See cloud docs for supported values | pass, prose defers (F15) |
| U35 | 82 | mem is in MiB | pass |
| U36 | 82 | Suffix M/G/T/P means mega/giga/tera/peta bytes | F (F4) |
| U37 | 87 | root-disk is in MiB | pass |
| U38 | 87 | Same suffixes as mem | pass |
| U39 | 87 | Separately attached storage does not count | pass |
| U40 | 92 | root-disk-source names a storage pool or location | pass |
| U41 | 92 | Behavior differs per provider | pass |
| U42 | 97 | spaces: comma-delimited space names | pass |
| U43 | 97 | Names are positive (an attribute of the space) or negative (something the space does not have) | F (F3) |
| U44 | 97 | Example spaces=storage,db,^logging,^public means ... | pass |
| U45 | 97 | EC2 and MAAS are the only providers supporting spaces | F (F2) |
| U46 | 102 | tags: comma-delimited, positive or negative | pass |
| U47 | 102 | Supported by MAAS and Kubernetes, used for pod affinity and anti-affinity | F (F18, incomplete) |
| U48 | 107 | virt-type supported only by LXD and OpenStack | F (F19) |
| U49 | 110 | zones: list; machine created within one of them; zone also a placement directive | pass |

Failures: U3, U5, U9, U12, U14, U15, U16, U20, U22, U25, U27, U36, U43, U45, U47, U48 = 16 of 49.
