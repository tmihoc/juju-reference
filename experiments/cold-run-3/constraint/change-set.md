# Change set for docs/reference/constraint.md

Format: `action | file and section | category | requirement | confidence`. Every line cites findings (a change with no finding is a defect). Confidence: determined, tie, or open(Qn).

| # | Action | File and section | Category | Requirement | Confidence | Findings |
|---|---|---|---|---|---|---|
| 1 | Rewrite lede: definition, then levels in one sentence; drop "the rest of this document", the caution block, and the client-first wording | constraint.md, lede | reference | R22, R24, R18 lede length | determined | F17, batch |
| 2 | Add section "Constraint syntax" (pairs, space escape, list items, three parser errors with trigger and remediation, client example with links) | constraint.md, new section, label `constraint-syntax` | reference | R6, R19 (errors have message, trigger, remediation), R24 | determined for facts; open(Q5) for the home of the errors | F20 |
| 3 | Replace the precedence sentences with a section "Constraint levels and precedence" (three overlays, per-key rule, conflicts, `ambiguous constraints` error, default `amd64`) | constraint.md, new section, label `constraint-levels` | reference (mechanism chunk) | R7 second condition, procedure step 4 (mechanism shared by several surfaces) | determined | F16, F7 |
| 4 | Add section "Cloud support for constraints" (unsupported means warning; value not accepted means error; links to the nine cloud sections and Kubernetes) | constraint.md, new section, label `constraint-cloud-support` | reference | R7, R16, R5 | determined for facts; tie for the placement against the cloud pages | F17 |
| 5 | Replace the minimum/maximum sentence with section "Minimums and maximums" (four quantity keys, definition as minimum, LXD and Kubernetes exceptions) | constraint.md, new section, label `constraint-minimum-maximum` | reference | R6 (T9) | determined | F1 |
| 6 | Rename H2 "List of constraints" to "Constraint keys"; keep label `list-of-constraints` and all 16 `constraint-<key>` labels | constraint.md | reference | R15, Manner (informative title) | determined | batch |
| 7 | Rewrite entries as prose (no `<p>`, `<br>`, bold labels) | constraint.md, all 16 entries | reference | R22 | determined | batch |
| 8 | `allocate-public-ip`: per-cloud defaults, EC2 behavior, unsupported list | entry | reference | R7, Quality | determined (EC2: open(source)) | F5, F6 |
| 9 | `arch`: per-cloud subsets, Kubernetes behavior, error | entry | reference | R7 | determined | F7 |
| 10 | `container`: values, add-machine rejection, unsupported list; drop "If not nil" | entry | reference | Quality, Manner | determined; effect left unstated | F8 |
| 11 | `cores`: deprecated alias with warning; Kubernetes unsupported; error | entry | reference | R7 | determined | F9 |
| 12 | `cpu-power`: ECU; unsupported list; portability advice by cloud | entry | reference | Quality | determined | F10, F11 |
| 13 | `image-id`: explicit-base rule and error; supporting and unsupporting clouds; base option plus model default | entry | reference | R24, T3, T4 | determined | F12 |
| 14 | `instance-role`: add GCE; delete the version scope | entry | reference | R23 | determined | F13 |
| 15 | `instance-type`: source of names; per-cloud conflict sets; unsupported list | entry | reference | T3 | determined | F14 |
| 16 | `ip-family`: only Azure acts; Azure values and two errors; delete `versionadded` | entry | reference | R23, T3, T4 | determined | F15 |
| 17 | `mem`: correct multipliers, case, fraction, error | entry | reference | Quality | determined | F4 |
| 18 | `root-disk`: state the suffix rule in the entry | entry | reference | Isolated reader (Addressee: AI reading one section) | determined | F21 |
| 19 | `root-disk-source`: one clause per cloud | entry | reference | R16 against isolated reader | tie | F22 |
| 20 | `spaces`: correct description and support statement; error | entry | reference | Quality | determined | F2, F3 |
| 21 | `tags`: MAAS and Kubernetes forms; unsupported list | entry | reference | Quality | determined | F18 |
| 22 | `virt-type`: add MAAS; per-cloud values; unsupported list | entry | reference | Quality | determined | F19 |
| 23 | `zones`: bootstrap failure; cloud without zones; directive precedence | entry | reference | T3 | determined | F23 |
| 24 | Update meta description to the page's actual scope | constraint.md front matter | reference | Manner (scope claim) | determined | batch |

## Backlog (not in the change set)

- Other upstream pages that contradict the source and are outside this page: `reference/cloud/list-of-supported-clouds/reuse/k8s/constraints.md` says `arch` and `zones` are unsupported on Kubernetes, while `kubernetes/application/constraints.go:44-68, 93-112` applies both and neither is in `kubernetes/constraints.go:12-21`. `amazon-ec2.md:255` lists `container` as supported although `container` has no reader (F8). `microsoft-azure.md:225` says `zones` is unsupported on Azure, which the Azure validator does not declare.
[A source observation about error handling in the constraint validation path was withheld from this public record. It is to be reported to the maintainers through the project's normal channel.]

## Chunks examined and left unchanged

- The `spaces` example `spaces=storage,db,^logging,^public` and the `tags` example `tags=virtual,^dualnic`: true and necessary, kept.
- The `zones` EC2 example: kept.
- The 16 anchors `constraint-<key>` and `constraint`: kept, none moved.
