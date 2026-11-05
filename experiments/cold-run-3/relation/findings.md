# Cold run 3, `relation.md` at 52e983a435: findings (recorded by the parent)

The subagent's Write tool refused this file; it returned the findings inline. Condensed record. **Verified by the parent at 52e983a435:** F2, F3 (status formatter part), F11. Others are the subagent's claims.

## Verified
- **F2 (high):** upstream defines a subordinate relation by application kind. In 4.1 the scope of a relation is container if either endpoint is container-scoped, so a container-scoped relation can be plugged into a global endpoint (`domain/relation/state/relation.go:292-298`); a relation between two subordinates is allowed (`relation.go:1990-1998`); the status formatter calls a relation `subordinate` when its scope is `container`, `peer` when both sides are the same application, and `regular` otherwise (`cmd/juju/status/formatter.go:342-348`).
- **F3 (medium, formatter part):** a cross-model relation is labeled `regular` by the client, which contradicts the taxonomy figure's footnote "non-cross model" (the figure part is the subagent's claim).
- **F11 (high):** `--controller-external-ips` and `--controller-external-name` are valid only for Kubernetes controllers; for any other cloud bootstrap fails with "are only allowed for kubernetes controllers" (`cmd/juju/commands/bootstrap.go:664-670`). The upstream page tells operators of any cloud with a non-flat topology to bootstrap with them.

## Claimed
High: F6 (peers as "the mechanism behind high availability" has no source support). Medium: F1 (lede states no multiplicity, ID, life or status), F4 (figure roles: caption on dark variant only), F5 ("every relation creates databags"; unit settings on entering scope, application settings only after the leader writes), F10 (explicit endpoints take precedence over `juju-info`: stale; `inferEndpoints` returns "ambiguous relation", needs a probe), F12 (offerer and saas "interchangeable" is contradicted by the next sentence; the firewaller acts on the offering side only if its endpoint is the provider), F13 (cross-model facts missing: peers cannot be consumed, both endpoints cannot be remote, only cross-model relations can be suspended, `via` egress), F15 (key and ID), F16 ("a local copy of all the databags"), F19 (settings rules incomplete: Juju alone writes `ingress-address` and `egress-subnets`, empty values dropped, 16 MiB cap), F22 (no status or life), F23 (no calls or errors), F24 (no removal or migration facts), F9 (`juju-info` section duplicates `application.md`). Low batch as reported.

## Subagent's draft
Entity grammar: lede, kinds, schema, 7 calls, 25 error entries, no figures; about 190 statements traced; code missing in 13 error entries and the message suffix open in 2.

## Contract failures reported
No error class for an entry consumed by an agent (`cannot enter scope yet`); R19 demands a code but the chain inside the `juju/errors` library is untraceable cold (message traced, code open); the source disagrees with itself (`bundledata.go:960-965` gives `juju-info` container scope, `metadata.go:468-475` global); no figure type for a theme-variant mismatch; no denominator rule on the scoring sheet; rule conflicts: genre row against "settings, not databag", R15 against the one-term rule, recipe against R15 for kinds, R16 against the isolated reader.
