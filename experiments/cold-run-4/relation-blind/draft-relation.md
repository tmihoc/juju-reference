---
myst:
  html_meta:
    description: "Juju relation reference: connections between application endpoints, their types (peer, non-peer, subordinate, non-subordinate, cross-model), the rules for establishing them, their ID and key, their status, and their settings."
---

(relation)=
# Relation

```{ibnote}
See also: {ref}`manage-relations`
```

In Juju, a **relation** is a connection between two {ref}`endpoints <application-endpoint>` of two different applications, or the connection of an application to itself through one of its `peers` endpoints.

An operator creates a relation between two applications with the integrate operation and needs write access to the model for it. Juju creates the relation of an application to itself when it creates the application.

(peer-relation)=
## Peer relation

A **peer** relation is a relation that an application has to itself. It has one endpoint, with role `peers`.

Juju creates one peer relation for each `peers` endpoint of the charm when it creates the application. Juju assigns the relation IDs in the alphabetical order of the endpoint names. The remove operation refuses to remove a peer relation.

Charm authors use the application settings of a peer relation to store data that all units of the application share.

(non-peer-relation)=
## Non-peer relation

A **non-peer** relation is a relation between two different applications. One endpoint has role `provides`, the other has role `requires`, and both have the same interface.

A non-peer relation has a scope, `global` or `container`. The scope is `container` when at least one of the two endpoints has scope `container`, and `global` otherwise.

(subordinate-relation)=
### Subordinate relation

A **subordinate** relation is a non-peer relation with scope `container`. At least one of its two applications is a subordinate.

When a unit of the other application enters the relation's scope, Juju creates a unit of the subordinate application on the machine of that unit. Juju creates no second subordinate unit for a unit that already has one. A subordinate application therefore has no unit until the first such unit enters the relation, and then has one unit for each unit of the other application in the relation. For the charm side, see {ref}`subordinate charm <subordinate-charm>`.

A subordinate charm declares at least one `requires` endpoint with scope `container`. Without one, Juju rejects the charm metadata with `subordinate charm "<name>" lacks "requires" relation with container scope`.

(the-implicit-juju-info-relation-endpoint)=
#### The implicit `juju-info` relation endpoint

Every charm has an implicit endpoint named `juju-info`, with role `provides`, interface `juju-info`, and scope `global`. Juju adds the endpoint when it records the charm, unless the charm metadata already declares an endpoint named `juju-info`. The charm metadata (`metadata.yaml` / `charmcraft.yaml`) therefore needs no declaration of it.

A subordinate charm consumes the endpoint by declaring a `requires` endpoint with interface `juju-info` and scope `container`. The convention is to name that endpoint `juju-info`, and any other name works too (for example, `info` or `general-info`). Juju rejects charm metadata that declares an endpoint named `juju` or `juju-*`. Three declarations are exempt: a container-scoped `requires` endpoint of a subordinate charm, the implicit `juju-info` endpoint itself, and any endpoint of a charm whose own name starts with `juju-`.

A relation through `juju-info` is a subordinate relation, because the subordinate's endpoint has scope `container`. The endpoint is useful for machine charms, because subordinate charms are machine charms. General-purpose subordinates that need no application-specific data from the principal use it, for example [`ntp`](https://charmhub.io/ntp), [`telegraf`](https://charmhub.io/telegraf), [`nrpe`](https://charmhub.io/nrpe), and [`canonical-livepatch`](https://charmhub.io/canonical-livepatch).

For example, `juju integrate <subordinate> <principal>` relates a subordinate to a principal when exactly one pair of their endpoints is compatible. If the subordinate also has an explicit endpoint whose interface matches an endpoint of the principal, two pairs are compatible, and Juju refuses with `ambiguous relation`. Naming the implicit endpoint on either side selects it:

```text
juju integrate <subordinate>:<requires-endpoint> <principal>:juju-info
```

(non-subordinate-relation)=
### Non-subordinate relation

A **non-subordinate** relation (also called a regular relation) is a non-peer relation with scope `global`. It creates no units.

(cross-model-relation)=
### Cross-model relation

A **cross-model** relation (also called a CMR) is a non-peer relation in which one of the two applications is a remote application. A remote application is a proxy, in one model, for an application of another model. The two models can belong to different controllers. For example, a CMR can connect databases that run on bare metal, for I/O performance, to applications that run on Kubernetes, for scalability and application density.

A CMR has two sides. The offering side is the model that hosts the offered application. The consuming side is the model that consumes the offer, and it holds a remote application (also called a saas) that stands for the offer. An offer cannot include an endpoint with scope `container`. See {ref}`offer <offer>`.

The names of remote applications are:

- In the consuming model, the remote application has the saas name, for example `prometheus`.
- In the offering model, each consuming relation has its own remote application. Its name is `remote-` followed by 32 hexadecimal digits, for example `remote-76cd96ab50f146b284912afd1cc13a0e`, and it has one endpoint.

Egress subnets can be set only on a cross-model relation.

On the consuming side, the firewall behavior depends on the role of the consuming application's endpoint. When the consuming application is the requirer, its model publishes the egress addresses to the offering model. When the consuming application is the provider, its model opens ingress for the egress addresses of the offering model.

For a Kubernetes controller, the addresses that Juju advertises to other controllers come from the bootstrap configuration keys `controller-external-name` and `controller-external-ips` (set with `--config` at bootstrap). The other controllers must be able to resolve those addresses for a cross-controller relation to work. Juju reads these keys only at bootstrap.

## Rules for establishing a relation

Juju creates a non-peer relation only when all of these conditions hold:

- Each endpoint identifier, of the form `<application>` or `<application>:<endpoint>`, matches at least one endpoint of its application. Otherwise Juju reports `relation endpoint not found`.
- Exactly one pair of endpoints is compatible. A pair is compatible when its endpoints belong to different applications, have the same interface, and have opposite roles `provides` and `requires`. When no pair is compatible, Juju reports `no compatible endpoints found between applications`. When several are, Juju reports `ambiguous relation` and lists the candidate pairs, and the operator names the endpoints to choose one.
- An endpoint with scope `container` is used only if at least one of the two applications is a subordinate, and the bases of the two applications are compatible.
- The two applications are not both remote applications.
- Both applications are alive, including a remote application.
- No relation exists yet between the two endpoints. Otherwise the client receives the code `already exists`.
- Neither endpoint has reached its limit. A charm sets the limit with `limit` on the endpoint, and a limit above zero caps the number of relations of that endpoint. Otherwise the client receives the code `quota limit exceeded` and the message `adding relation between endpoints "<endpoint>" and "<endpoint>": quota limit exceeded`.
- Egress subnets are given only for a cross-model relation.

## Relation ID and key

A relation has a **relation ID**, a number that Juju assigns from a sequence of the model when it creates the relation. The ID is unique in the model.

A relation also has a **relation key**, made of the endpoints. The key of a non-peer relation is `<requirer-application>:<requirer-endpoint> <provider-application>:<provider-endpoint>`, with the requirer first. The key of a peer relation is `<application>:<peer-endpoint>`. Every endpoint in a key carries its endpoint name.

The remove operation takes either the two endpoints of the relation or its relation ID, and needs write access to the model. If several relations exist between the two applications, the endpoints are ambiguous and the operation requires the relation ID.

## Relation status

A relation has one of six statuses: `joining`, `joined`, `broken`, `suspending`, `suspended`, and `error`. Juju sets `joining` when it creates the relation.

- `joining`: The relation should become joined soon.
- `joined`: The relation is alive and healthy.
- `broken`: The life of the relation has gone to dead.
- `suspended`: The relation is temporarily broken until an action resumes it.
- `error`: The relation is in an error state. Setting this status requires a message.

Only the leader unit of an application in the relation sets the status of the relation.

The rules for a change of status are:

- Setting the current status again is always accepted.
- `broken` can be set from any status.
- `error` can be set from any status.
- `joined` and `suspended` cannot be set from `broken`.
- `joining` cannot be set from `broken` or `joined`.
- `suspending` cannot be set from `broken` or `suspended`.

A refused change fails with `relation status transition not valid`.

## Relation settings

A relation has settings at two levels. Each unit that has entered the relation has unit settings, and each application endpoint of the relation has application settings. Keys and values are non-empty strings. Setting a key to an empty value removes the key.

The writers and readers of each kind of relation settings are:

| Settings | Written by | Read by |
|---|---|---|
| Unit settings of a unit | That unit | Every unit in the relation |
| Application settings of an application | The leader unit of that application | Every unit in the relation |

In a peer relation, the only application is the local one, so all settings belong to the application that the units are part of. In a non-peer relation, the settings of the other application are read-only for every unit.

Juju writes the keys `ingress-address` and `egress-subnets` in the unit settings, and drops any value that a charm sets for them. When a unit leaves the relation, Juju keeps a copy of its last settings, and they stay readable until the relation is removed.

A unit that is not the leader and tries to write application settings receives `cannot write relation settings`.
