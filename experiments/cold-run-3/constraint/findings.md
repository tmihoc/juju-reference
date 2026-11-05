# Cold run 3, `constraint.md` at 52e983a435: findings (recorded by the parent)

The subagent's Write tool refused this file and it returned the findings inline. This is a condensed record. Line numbers are those of upstream `constraint.md`; paths are 4.1 source. **Verified by the parent at 52e983a435:** F1 (Kubernetes part), F2, F4, F10. All others are the subagent's claims.

## Verified
- **F1 (high), partly:** "a constraint is a minimum on a VM and a maximum on a container" is not a clean rule. The Go struct comments say "at least" for `cores`, `cpu-power` and `mem` (`core/constraints/constraints.go:61-70`). On Kubernetes `configureWorkloadConstraint` sets both a request and a limit from the same value (`internal/provider/kubernetes/application/constraints.go:331-345`). LXD limits (`internal/container/lxd/container.go:58-63`, `lxd/environ_broker.go:205-214`) are the subagent's claim.
- **F2 (high):** upstream says only EC2 and MAAS support `spaces`; GCE (`internal/provider/gce/environ_network.go:101-125`), Azure (`azure/environ_network.go:388`) and LXD (the subagent's claim) act on it.
- **F4 (medium):** the suffixes are 1024-based: `M=1, G=1024, T=1024*1024, P=1024^3` (MiB), `constraints.go:912-917`.
- **F10 (low):** the source says 100 `cpu-power` is 1 Amazon ECU (`constraints.go:65-67`), not "1 Amazon vCPU".

## Claimed
F3 (the `^` text for `spaces` is copied from `tags`), F5/F6 (`allocate-public-ip` provider list and default), F7 (`arch` values per cloud; default `amd64`), F8 (`container` key unverifiable; values `lxd`, `none`), F9 (`cpu-cores` deprecated), F11 (`cores` not portable to Kubernetes? `cpu-power` unsupported on five clouds), F12 (`image-id` needs an explicit base, error `base must be explicitly provided when image-id constraint is used`), F13 (GCE supports `instance-role`; "Juju 3.6" scoping), F14 (conflict sets), F15 (`ip-family` is acted on only by Azure), F16 (precedence is key by key), F17 (unsupported key logs a warning), F18 (Kubernetes `tags` are labels or node affinity), F19 (MAAS `virt-type`), F20 (constraint syntax and parser errors stated nowhere), F21 to F23 (low).

## Subagent's scoring
16 of 49 upstream claims fail the source trace; draft has 0 failing rows of 114.

## Contract failures reported
1. Derived rules without defect types: R24 (client-agnostic), R23 (version scope), layout markup in prose, spelling. 2. Parser errors have no code; Q5 blocked placing multi-call errors. 3. No client-wrapper trace outside the allowed inputs. 4. No confidence value for a source that contradicts itself. 5. Change coupling and reading path unavailable cold. 6. R16 against the isolated reader decided six placements, all judged. 7. No grammar for a non-entity page (Q3). 8. "False by enumeration" ("the only providers") is not in the defect table, and the severity scale does not separate F2 from F19.

## Source observations outside the page (not for the docs PR)
[A source observation about error handling in the constraint validation path was withheld from this public record. It is to be reported to the maintainers through the project's normal channel.]
