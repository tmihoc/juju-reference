---
myst:
  html_meta:
    description: "Juju relation reference: a connection between two application endpoints, or between the units of one application. Covers relation kinds, records, settings, status, and the calls that add, change, and remove relations."
---

(relation)=
# Relation

```{ibnote}
See also: {ref}`manage-relations`
```

A **relation** connects an {ref}`endpoint <application-endpoint>` of one {ref}`application <application>` to an endpoint of a different application. A **peer** relation is the exception: it has one endpoint, and it connects the units of one application to each other. Each relation has an ID that is unique in its model, a key, a life, and a status.

## Relation kinds

The endpoints decide the kind of a relation. A relation is either non-peer or peer. A non-peer relation has global scope (a regular relation) or container scope (a subordinate relation), and a regular relation can be cross-model.

(non-peer-relation)=
### Non-peer relation

A **non-peer** relation connects an endpoint of one application to an endpoint of a different application. The two endpoints have the same interface and opposite roles: one is `provides` and the other is `requires`.

(non-subordinate-relation)=
#### Non-subordinate relation

A **non-subordinate** relation, also called a **regular** relation, is a non-peer relation with global scope. A relation has global scope unless one of its two endpoints has container scope.

(cross-model-relation)=
##### Cross-model relation

```{ibnote}
See also: {ref}`manage-relations`
```

A **cross-model** relation is a regular relation in which one application is a **remote application**. A remote application is a stand-in, in one model, for an application of another model. The model that offers the application is the offering model, and the model that consumes the offer is the consuming model. The two models can be on different controllers and on different clouds.

The consuming model holds one remote application for the offer, under the name the consuming model gives it. The offering model holds one remote application for each relation with a consumer. Its name is `remote-` followed by 32 hexadecimal digits from a generated UUID, for example `remote-76cd96ab50f146b284912afd1cc13a0e`. Each remote application has exactly one endpoint.

The rules of a cross-model relation are:

- Peer endpoints cannot take part in it.
- Both applications cannot be remote.
- It is the only kind of relation that can be suspended and resumed.
- Egress CIDRs (the networks that the consuming units connect from) can be given for it only.
- Units of a subordinate application cannot enter it.

The controllers of the two models must reach each other. A Kubernetes controller advertises the address that its `controller-external-name` or `controller-external-ips` bootstrap setting gives to other controllers, so that address must resolve from them.

The offering model opens network access for a relation only when its own endpoint is the provider. The consuming model publishes the networks it connects from to the offering model. The offering model allows the networks that its `saas-ingress-allow` setting permits. When the offering model refuses the networks, the relation in the consuming model takes the status `error`, with the refusal as its message.

(subordinate-relation)=
#### Subordinate relation

A **subordinate** relation is a non-peer relation with container scope. A relation has container scope when either of its two endpoints has container scope, and Juju requires at least one of the two applications to be a subordinate application. The other application is a principal application or a subordinate application.

A subordinate application has no units when it is deployed. Each time a unit of the principal application enters the scope of the relation, Juju creates a unit of the subordinate application on the same machine. The two applications must run on compatible bases.

(the-implicit-juju-info-relation-endpoint)=
##### The implicit `juju-info` endpoint

Every application has an implicit endpoint named `juju-info`, with the `provides` role, the `juju-info` interface, and global scope. Juju adds the endpoint to a charm unless the charm declares one named `juju-info`. The units of the application that provides the endpoint run no relation hooks for it.

A subordinate charm attaches to any principal application by requiring an endpoint with the `juju-info` interface and container scope. The principal application always provides `juju-info`, so the subordinate charm needs no interface in common with the principal charm. The name of the requiring endpoint is free, and `juju-info` is the convention.

When two applications have more than one pair of compatible endpoints, Juju returns an "ambiguous relation" error and the caller names the two endpoints. That happens, for example, when the subordinate charm has an explicit endpoint whose interface the principal charm also provides, besides its `juju-info` endpoint. The call `juju integrate <subordinate>:<requires-endpoint> <principal>:juju-info` names the `juju-info` pair.

The {ref}`application endpoint <application-endpoint>` reference defines the endpoint itself.

(peer-relation)=
### Peer relation

A **peer** relation connects the units of one application to each other. Its single endpoint has the `peer` role. Juju creates it when it deploys an application whose charm declares a peer endpoint, and no client adds it.

## Relation database schema

A relation is stored in these records:

- **Relation.** A relation has an ID, a life, a scope, and a suspended flag with a reason.
  - Rules:
    - The ID comes from a sequence of the model, is unique, and is never reused in the life of the model.
    - The life is `alive`, `dying`, or `dead`. A relation is dead only after all its units have left its scope.
    - The scope is `global` or `container`.
  - The key of a non-peer relation joins its two endpoints with a space, the requirer first and the provider second, each as `<application>:<endpoint>`. The key of a peer relation is its one endpoint.
- **Relation endpoint.** A relation endpoint links a relation to an application endpoint. A non-peer relation has two relation endpoints, and a peer relation has one.
  - Rules:
    - An application endpoint appears at most once in a relation.
- **Relation unit.** A relation unit records that a unit has entered the scope of a relation at one of its endpoints.
  - Rules:
    - A unit has at most one relation unit for each relation endpoint.
- **Unit settings.** Unit settings are key-value pairs of one relation unit.
  - Rules:
    - A key and a value are never empty.
    - A key is unique for its relation unit.
- **Application settings.** Application settings are key-value pairs of one relation endpoint, and so of one application in the relation.
  - Rules:
    - A key and a value are never empty.
    - A key is unique for its relation endpoint.
- **Departed unit settings.** When a unit leaves a relation, Juju copies its unit settings. The copy is kept until the relation is removed.
- **Relation status.** A relation has one status, with a message and a time of last update. The status is `joining`, `joined`, `broken`, `suspending`, `suspended`, or `error`.
  - `joined` is the normal status of a healthy, alive relation.
  - `broken` is the status of a relation whose life is dead.
  - `suspended` means the relation is temporarily broken until someone resumes it.

## Relation calls

The callers of a relation are clients and unit agents. A **unit agent** is the process that runs the unit's charm; it is logged in as its unit and acts only for that unit. A client adds, removes, suspends, and resumes relations. A unit agent enters and leaves the scope of relations, reads and writes relation settings, and sets the relation status.

### Adding relations

Adding relations creates a relation between two application endpoints.

- Caller: a client, for a user with write access to the model, while no change block is set.
- Rules:
  - The call takes exactly two endpoints. Each endpoint is `<application>` or `<application>:<endpoint>`.
  - For an endpoint without a name, Juju pairs every endpoint of one application with every endpoint of the other, keeps the pairs that can be related, and requires exactly one pair.
  - Two endpoints can be related when they belong to different applications, have the same interface, and have opposite roles.
  - Both applications are alive.
  - The two endpoints are not already related.
  - Neither endpoint has reached its limit of relations.
  - A relation with container scope needs at least one subordinate application and compatible bases.
  - A relation joins at most one remote application.
  - The call accepts egress CIDRs for a cross-model relation only. Each CIDR must be valid.
  - The new relation is alive, takes the next ID, takes its scope from its endpoints, and has the status `joining`.
  - The result holds the charm relation of each endpoint, by application name.
- Errors:
  - `a relation should have exactly two endpoints`, code `bad request`.
    - Trigger: the call has any number of endpoints other than two.
    - Remediation: Give two endpoints.
  - `adding relation between endpoints "<a>" and "<b>": cannot relate endpoints "<a>" and "<b>": no candidates for <endpoint>: relation endpoint not found`.
    - Trigger: an application has no endpoint of that name.
    - Remediation: Use an endpoint name that the charm of the application declares.
  - `adding relation between endpoints "<a>" and "<b>": cannot relate endpoints "<a>" and "<b>": no compatible endpoints found between applications`.
    - Trigger: no pair of endpoints has the same interface and opposite roles, or a pair has container scope and neither application is a subordinate.
    - Remediation: Name two endpoints that share an interface and have opposite roles.
  - `adding relation between endpoints "<a>" and "<b>": cannot relate endpoints "<a>" and "<b>": ambiguous relation: "<a> <b>" could refer to "<pair>"; "<pair>"`.
    - Trigger: more than one pair of endpoints can be related.
    - Remediation: Name the endpoint on one or both sides, as in one of the pairs listed.
  - `adding relation between endpoints "<a>" and "<b>": already exists`, code `already exists`.
    - Trigger: the two endpoints are already related.
    - Remediation: Use the existing relation.
  - `adding relation between endpoints "<a>" and "<b>": quota limit exceeded`, code `quota limit exceeded`.
    - Trigger: an endpoint is already in as many relations as its limit allows.
    - Remediation: Remove one of the relations of that endpoint.
  - `adding relation between endpoints "<a>" and "<b>": unable to integrate two cross model applications together`.
    - Trigger: both applications are remote.
    - Remediation: Relate a local application to one of them.
  - `adding relation between endpoints "<a>" and "<b>": cannot add relation "<a>", "<b>": relation <endpoint> <endpoint>: application <name> is not alive`.
    - Trigger: an application is dying, or the remote application of an offer is dying.
    - Remediation: Wait until the removal has finished, then deploy the application again.
  - `adding relation between endpoints "<a>" and "<b>": cannot add relation "<a>", "<b>": relation <endpoint> <endpoint>: no compatible bases found for application "<a>" and "<b>"`.
    - Trigger: the relation has container scope and the bases of the two applications are not compatible.
    - Remediation: Deploy the subordinate application on a base that is compatible with the principal application.
  - `adding relation between endpoints "<a>" and "<b>": integrating via subnets for non cross model relations`.
    - Trigger: the call gave egress CIDRs for a relation between local applications.
    - Remediation: Leave out the CIDRs.
  - `adding relation between endpoints "<a>" and "<b>": CIDR "<cidr>" is not valid: <reason>`.
    - Trigger: a CIDR cannot be parsed.
    - Remediation: Give CIDRs in the form `<address>/<prefix length>`.
  - `adding relation between endpoints "<a>" and "<b>": CIDR cannot be empty`.
    - Trigger: a CIDR is an empty string.
    - Remediation: Leave out the empty CIDR.

### Removing relations

Removing relations ends a relation and everything stored for it.

- Caller: a client, for a user with write access to the model, while no remove block is set.
- Rules:
  - The call takes the two endpoints or the relation ID.
  - After the call the relation is no longer alive, and Juju has removed it or scheduled its removal.
  - With force and a maximum wait, Juju forces the removal when the normal removal has not finished within the wait.
  - The removal of a cross-model relation also removes its offer connection and remote application records.
- Errors:
  - `relation with endpoints [<a> <b>] or id <n> not found`, code `not found`.
    - Trigger: no relation matches the endpoints or the ID.
    - Remediation: List the relations of the model and use an existing endpoint pair or ID.
  - `endpoints "[<a> <b>]" are ambiguous, specify relation endpoints or id`.
    - Trigger: the two applications have more than one relation, and the endpoints do not pick one.
    - Remediation: Give the endpoint names, or give the relation ID.

### Suspending and resuming relations

Suspending relations stops a cross-model relation until it is resumed.

- Caller: a client, for a user with write access to the model, while no change block is set.
- Rules:
  - The call takes relation IDs, a suspended flag, and a message. Each ID has its own result.
  - A relation already in the requested state stays as it is.
  - Only a cross-model relation can be suspended or resumed.
  - Suspending sets the suspended flag, keeps the message as the reason, and sets the status `suspending` with the message.
  - Resuming sets the status `joining` with an empty message.
- Errors:
  - `relation <id> not found`, code `not found`.
    - Trigger: no relation has that ID.
    - Remediation: List the relations of the model and use an existing ID.
  - `relation must be a remote relation to be suspended`.
    - Trigger: the relation is between local applications.
    - Remediation: Suspend a cross-model relation.

### Entering a relation scope

Entering a relation scope records that a unit takes part in a relation.

- Caller: a unit agent, for its own unit.
- Rules:
  - The unit and the relation are alive.
  - The unit's application is one of the applications of the relation.
  - A unit that is already in scope stays as it is, and the call succeeds.
  - The unit's settings start with `ingress-address`, the first ingress address of the unit, and `egress-subnets`, its egress subnets as a comma-separated list, each when the unit has any.
  - When the relation has container scope and the unit belongs to the principal application, Juju creates a subordinate unit on the same machine, with storage from the storage directives of the subordinate application.
  - A subordinate unit that enters a container-scoped relation with an application other than its principal is left out, and the call succeeds.
- Errors:
  - `checking unit valid in relation: cannot enter scope, unit or relation not alive`, code `cannot enter scope`.
    - Trigger: the unit or the relation is dying or dead.
    - Remediation: None for a person. The unit agent drops the relation from its local state.
  - `cannot enter scope, subordinate unit exists but is not alive`, code `cannot enter scope yet`.
    - Trigger: the relation needs a subordinate unit, and one exists but is dying.
    - Remediation: None for a person. The unit agent waits until the subordinate unit is removed.
  - `checking unit valid in relation: unit not in relation`.
    - Trigger: the unit's application is not one of the applications of the relation.
    - Remediation: Enter the scope of a relation of the unit's application.

### Reading relation settings

Reading relation settings returns the key-value pairs of a unit or an application in a relation.

- Caller: a unit agent, for its own unit.
- Rules:
  - A unit reads its own unit settings.
  - Only the leader unit reads the application settings of its own application.
  - A unit reads the unit settings of any remote unit and the application settings of the remote application, whether or not it is the leader.
  - In a peer relation, the remote side is the reading unit's own application: every unit reads the unit settings of every unit of the application, and the application settings.
  - The unit settings of a unit that has left the relation stay readable until the relation is removed.
- Errors:
  - `permission denied`, code `unauthorized access`.
    - Trigger: the unit settings belong to another unit, a unit that is not the leader reads the application settings of its own application, or the relation does not exist.
    - Remediation: Read the application settings of the unit's own application from the leader unit.

### Writing relation settings

Writing relation settings changes the key-value pairs of a unit or an application in a relation. A unit agent writes them in the call that commits the changes of a hook.

- Caller: a unit agent, for its own unit.
- Rules:
  - A unit writes only its own unit settings.
  - Only the leader unit writes the application settings of its own application.
  - A key with an empty value is removed from the settings.
  - Juju alone writes `ingress-address` and `egress-subnets`. The values a unit gives for these keys are discarded.
  - The keys and values of one set of settings together hold at most 16 MiB.
- Errors:
  - `permission denied`, code `unauthorized access`.
    - Trigger: the settings belong to another unit.
    - Remediation: Write the unit's own settings.
  - `... checking relation unit settings size: max allowed total size (16777216): quota limit exceeded`, code `quota limit exceeded`.
    - Trigger: the settings would hold more than 16 MiB.
    - Remediation: Store less data in the settings.

### Setting the relation status

Setting the relation status changes the status and the message of a relation.

- Caller: a unit agent, for its own unit, and only the leader unit of its application. After the leader unit enters scope, its agent sets `joined`.
- Rules:
  - A status can be set to the value it already has.
  - Any status can be set to `broken`.
  - `suspending` cannot follow `broken` or `suspended`.
  - `joining` cannot follow `broken` or `joined`.
  - `joined` and `suspended` cannot follow `broken`.
  - `error` needs a message.
  - A `suspended` status that follows `suspending` keeps the earlier message when the new message is empty.
- Errors:
  - `cannot set status <new> when relation has status <current>: ...`.
    - Trigger: the current status does not allow the new status.
    - Remediation: Set a status that the current status allows.
  - `cannot set status error without message`.
    - Trigger: the status is `error` and the message is empty.
    - Remediation: Give a message.
  - `permission denied`, code `unauthorized access`.
    - Trigger: the relation does not exist, the unit's application is not in the relation, or the caller is not the unit named.
    - Remediation: None for a person.
