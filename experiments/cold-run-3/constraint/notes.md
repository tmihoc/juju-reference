# Notes: where the method failed, conflicted, or needed a judgment

## Contract failures and gaps

1. **No defect type for a derived rule.** The ledger says "a derived rule with no defect type is a gap in the contract". Four rules that this page violates have no type: client-agnostic (R24: "juju commands /command flags" names the client first), version scoping (R23: `versionadded 4.1.0`, "starting with Juju 3.6"), layout markup in prose (`<p>`, `<br>`), and American spelling. I filed them under "batch" and under Not enough or Stale, which misdescribes them.
2. **Error format requires a code; parser errors have none.** `malformed constraint`, `unknown constraint`, and `bad "<key>" constraint` come from `core/constraints` and carry no API code. The contract's error entry (message, code, trigger, remediation) cannot express them. I wrote entries with message, trigger, and remediation.
3. **Error home (Q5) blocks the draft.** The parser errors are raised by every call that takes constraints. I nested them under the syntax section, labeled open(Q5), and did not claim the contract allowed it. The contract says "do not move the entry"; there was no entry, so the rule gave no instruction for a new one.
4. **Client rendering of the parser errors is not traceable.** The flag wrapper is gnuflag (an external library not in the allowed inputs). Wrong message and Wrong code cannot be ruled out. The draft states the messages as raised.
5. **A source that contradicts itself has no confidence value.** EC2 declares `allocate-public-ip` unsupported and also acts on it (`ec2/environ.go:270` against `750-765`). The contract's confidence values are determined, tie, or open(Qn). I used open(source) and stated both traced facts in the draft. Similar: `Value`'s Go comments are stale in two places (`constraints.go:92-95` instance-role "only AWS"; `121-124` image-id "only MAAS"), so a comment is not an authority even in the source.
6. **Boundary measures: two of four are unavailable cold.** Change coupling and reading path need git history and inbound links. The tie rule ("at least two measures agree") then cannot fire, and per-key cloud support (P8) stays a tie by default. The contract should say what a cold run reports when two measures are unreadable.
7. **R16 against the isolated reader is not resolved** (contract "Not settled" (a)). It decided P8, P9, P10, P14, P15, and P18. I kept per-key support and per-cloud values on the constraint page and called each a judgment. A generator from the `unsupportedConstraints` lists would serve both and is not in the allowed inputs.
8. **No rule for a non-entity page's section grammar** (Q3). The syntax, levels, support, and minimum/maximum sections follow no recipe. I used the procedure's "mechanism chunk" (step 4) and R7's second condition as the only available justification. Whether a page with four mechanism sections and a key list is one page or two (grab-bag test) cannot be decided from the measures; the key list and the mechanism sections share one source owner (`core/constraints`) and one audience, so I kept one page.
9. **"Prose defers" has no entry for a pointer that carries content to a page that does not have it.** `ip-family`: "See the cloud-specific documentation for supported values and behavior." Closest type is Prose defers (figures) or Not enough. I used Not enough.
10. **Figure rules had nothing to say.** I considered a table of key against cloud support (16 by 10) built from the unsupported lists. The contract treats tables like figures only by analogy (Stale sample). I did not add one: the prose states each support fact per key, and a table would need the same statements, so it would be redundant under the figure rule, and the decorative test (R26) says it earns no place unless it makes the multiplicity easier to hold. That claim is untested (the ledger marks the empirical premise open).
11. **Severity for an enumeration read as complete.** The contract gives high for "a plausible rule presented as a rule"; F2 (spaces) and F19 (virt-type) are enumerations that read as complete ("the only providers"). I rated F2 high and F19 medium. The scale does not separate them.

## Judgments the draft makes

- `container`: the draft does not state what the key does at provisioning. No 4.1 code that acts on it was found (grep over all `*.go` for `HasContainer`, `.Container` outside core, state, tests). A probe on a real controller is needed (`juju deploy --constraints container=lxd`). The upstream sentence was kept only as "states the container type" with the Go comment as the source.
- `allocate-public-ip` on EC2: both traced facts are stated, with no verdict.
- Remediations for the three parser errors, the conflict error, and the invalid-value error are derived, not quoted (trace rows S10, V10, C3).
- `bootstrap constraints also apply to later HA controller machines`: help text only (`bootstrap.go:89-90`); the enable-ha path was not read.
- The `cores`/`cpu-power` portability sentence is a derived statement from ten unsupported lists.
- Kubernetes `mem`/`cpu-power` as request and limit is the V2 path (`kubernetes/application/constraints.go:350-374`). The V1 path (agents older than `charmContainerResourceVersion`) sets requests on the first container only and limits on all (`331-346`). The page documents the 4.1 behavior and does not state the older path.

## Source observations outside the page

[A source observation about error handling in the constraint validation path was withheld from this public record; it is to be reported to the maintainers through the project's normal channel.]
- `Value.String()` (`constraints.go:282-351`) writes `mem=` and `root-disk=` with a trailing `M`, and `Merge` round-trips through `Parse` (`465-471`). An empty `mem=` parses to a non-nil zero (`parseSize`), which `withFallbacks` treats as set. That suggests an empty value at the specific level clears an inherited value; I did not state it because no test or help text confirms the intent.
- Other upstream pages that disagree with the source are listed in the change set backlog (Kubernetes snippet, EC2, Azure).

## Method observations

- The procedure's step 3 classes (Contradicted, Enumeration extended, Outcome changed, Unaffected) are for developments; in page-driven mode the review types worked. The two that did most of the work here were Conditional truth stated flat and False by enumeration read as complete. The second is described only in the addressee model ("Relies on implicature") and appears nowhere in the defect table: I filed these as False.
- Checking each key against `unsupportedConstraints` needed 10 provider files and was the most productive single check (found F2, F5, F13, F19). The contract names it only in the task, not in the pipeline.
