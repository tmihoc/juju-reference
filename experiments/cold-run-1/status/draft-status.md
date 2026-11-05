---
myst:
  html_meta:
    description: "Juju status reference: application status, unit workload status, unit agent status, status during unit start-up and removal, and status in the output of juju status."
---

(status)=
# Status

A **status** is a value that Juju reports for an entity, together with a message and the time of the last update. An application has one status, which Juju derives from its units unless the application's leader unit sets it. A unit has two statuses: a workload status, which the charm reports, and an agent status, which Juju reports. Machines, models, relations, storage, and tasks have statuses with values of their own.

(application-status)=
## Application status

Juju derives the status of an application from the workload statuses that its units display. It picks the status with the highest severity. From the highest to the lowest, the severities are `error`, `blocked`, `maintenance`, `waiting`, `active`, `terminated`, and `unknown`. One `blocked` unit therefore makes the application `blocked`, unless another unit is in `error`.

When several units share the highest severity, Juju takes the status of the leader unit if the leader is among them, and otherwise the status of the unit with the lowest number. An application without units has the status `unknown`.

The leader unit can set the status of its application instead, with `status-set --application` (see {ref}`status-set <hook-command-status-set>`). The value is one of `maintenance`, `blocked`, `waiting`, or `active`. This status replaces the derived one. A unit that is not the leader gets the error `this unit is not the leader`.

(unit-status)=
## Unit status

The status of a {ref}`unit <unit>` is the pair of its workload status and its agent status.

(workload--charm-status)=
### Workload status

The workload status reports whether the unit's workload is providing its service. The charm sets it with the {ref}`status-set <hook-command-status-set>` hook command to one of `maintenance`, `blocked`, `waiting`, or `active`, at any time and in any order. Any other value gets the error `invalid status "<value>", expected one of [maintenance blocked waiting active]`. Juju sets `error`, `unknown`, and `terminated`. Juju also sets `waiting` and `maintenance` while a unit starts and while it is removed.

Because the charm chooses the value, the meaning of a charm-set value is ultimately up to the charm author. Each value tells an operator whether to act:

| Status | Meaning |
|--|--|
| `active` | The unit believes it is correctly offering all the services it was asked to offer. |
| `maintenance` | The unit is not yet providing its service but is busy preparing to, for example while installing software or formatting storage. No human intervention is required. |
| `waiting` | The unit is not in error and requires no intervention. It cannot provide its service because it depends on an external factor, for example a related application that is not running. |
| `blocked` | The unit cannot continue without user input. The message says how to unblock it, for example `Add a database relation`. |
| `error` | A hook of the unit failed. Juju sets the message, which names the hook, as in `hook failed: "install"`. |
| `unknown` | Juju sets it when the start hook has finished and the charm has set no status. Juju also shows it, with a message that points to the unit's logs and status history, when the unit agent is lost. |
| `terminated` | Juju sets it when the unit's remove hook has finished. The unit is gone. |

(agent-status)=
### Agent status

The agent status reports what the {ref}`unit agent <unit-agent>` is doing. The unit agent and the controller set it. The `status-set` hook command sets only the workload status.

| Status | Meaning |
|--|--|
| `idle` | The unit agent is installed and running, and has nothing to do. It stays `idle` until a hook or task needs to run. |
| `executing` | The unit agent is running a hook or task. The message says which. |
| `allocating` | Juju created the unit. Juju sets this value on machine models and Kubernetes models alike. |
| `rebooting` | The machine that hosts the unit agent is being rebooted, for example after the `juju-reboot` hook command. The status should return to `idle` when the reboot is complete. |
| `error` | A hook failed. The message is `hook failed: "<hook>"`. |
| `failed` | An operation of the unit agent failed. |
| `lost` | The controller has not heard from the unit agent. The message is `agent is not communicating with the server`. |

Setting `allocating` or `lost` is refused. When the agent status is `error`, `juju status` shows the unit with the workload status `error` and the agent status `idle`. The workload message is then the agent's message.

## Status during unit start-up and removal

A new unit goes through these statuses:

1. Juju creates the unit with the agent status `allocating` and the workload status `waiting`. The message is `waiting for machine` on a machine model and `installing agent` on a Kubernetes model.
2. The unit agent starts and changes the workload message to `agent initialising`.
3. Before the {ref}`install hook <hook-install>` runs, Juju sets the workload status `maintenance` with the message `installing charm software`, unless the charm has already set a workload status.
4. While hooks run, the agent status is `executing`. It becomes `idle` when nothing is left to do.
5. After the {ref}`start hook <hook-start>` finishes, Juju sets the workload status `unknown` if the charm has set no workload status.

The charm can replace the workload status at any step with `status-set`.

A unit that is removed goes through these workload statuses:

1. Before the {ref}`stop hook <hook-stop>` runs, Juju sets `maintenance` with the message `stopping charm software`. After the stop hook, Juju sets `maintenance` without a message.
2. Before the {ref}`remove hook <hook-remove>` runs, Juju sets `maintenance` with the message `cleaning up prior to charm deletion`.
3. After the remove hook, Juju sets `terminated`.

## Workload status on Kubernetes

On a Kubernetes model, Juju also tracks the status of the unit's pod, and the workload status that `juju status` shows can be the pod's. The shown status is chosen in this order:

1. The charm's status, when the unit has no pod status yet.
2. The charm's status, when it is `terminated`, `blocked`, or `maintenance`.
3. The pod's status, when it is `blocked`.
4. The pod's status, when it is `waiting` and the charm's status is `active`.
5. The pod's status, when it is `running` and the charm's status is the start-up `waiting` with the message `waiting for container`, `agent initialising`, or `installing agent`.
6. The charm's status in every other case.

## Status in the output of `juju status`

`juju status` shows the application status in the `Status` column of the `App` section. It shows the unit statuses in the `Workload` and `Agent` columns of the `Unit` section.

````{dropdown} Expand to view a sample 'juju status' output

```text
Model        Controller           Cloud/Region        Version  Timestamp
charm-model  tutorial-controller  microk8s/localhost  4.0.15   14:23:55+02:00

App             Version  Status  Scale  Charm           Channel    Rev  Address         Exposed  Message
demo-api-charm  1.0.0    active      1  demo-api-charm               0  10.152.183.175  no
postgresql-k8s  14.7     active      1  postgresql-k8s  14/stable   73  10.152.183.237  no       Primary

Unit               Workload  Agent  Address      Ports  Message
demo-api-charm/0*  active    idle   10.1.157.72
postgresql-k8s/0*  active    idle   10.1.157.74         Primary
```

````

```{ibnote}
See more: {ref}`command-juju-status`
```
