---
myst:
  html_meta:
    description: "Juju reference for the status of units and applications: workload status, agent status, application status, who sets each, the order in which Juju derives the application status, and where `juju status` shows them."
---

(status)=
# Application and unit status

A unit has two statuses: the workload status and the agent status. An application has one status. Each status consists of a value, a message, and the time it was set.

(unit-status)=
## Unit status

The workload status of a unit reports on the charmed software. The agent status of a unit reports on the unit agent, the Juju process that runs the charm's hooks.

(workload--charm-status)=
### Workload status

The charm sets the workload status with the {ref}`status-set <hook-command-status-set>` hook tool. The hook tool accepts `maintenance`, `blocked`, `waiting`, and `active`, and rejects every other value. The charm decides which of these values to set and when. Juju sets `error`, `unknown`, and `terminated`. Juju also sets `waiting` and `maintenance` at fixed points of the unit's life (see {ref}`unit-status-life`).

The workload status values are:

| Status | Meaning |
|--|--|
| `error` | A hook of the unit failed, or a charm upgrade of the unit failed. The unit needs human intervention. Juju sets this status and the message names the failed hook (`hook failed: "<hook>"`) or the upgrade (`upgrade failed`). |
| `blocked` | The unit cannot continue without user input. The message tells the user how to unblock the unit. |
| `maintenance` | The unit is not yet providing a service and is doing work on itself in preparation, for example installing software. No human intervention is required. |
| `waiting` | The unit is not in error and is not yet in service, because it depends on an external factor, for example a related application that is not running. No human intervention is required. |
| `active` | The unit believes it is offering all the services it is installed to provide. A message is optional and, when present, describes a degradation of service. |
| `unknown` | Juju sets this status in two cases: the start hook has finished and the charm has set no status in any hook so far, or the agent is `lost` (see below). |
| `terminated` | The remove hook of the unit has finished. Juju sets this status. |

The `status-set` message is shown to users and is kept in the status history.

In a Kubernetes model, the status of the unit's pod can replace the workload status that Juju displays. A workload status of `terminated`, `blocked`, or `maintenance` is always displayed. When the workload status is `active`, `waiting`, or `unknown` and the pod status is `blocked`, the pod status is displayed. When the workload status is `active` and the pod status is `waiting`, the pod status is displayed.

### Agent status

Juju sets the agent status. The `status-set` hook tool sets only the workload status. The agent status values are:

| Status | Meaning |
|--|--|
| `allocating` | The unit exists and its agent is not running yet. |
| `idle` | The agent has no operation to run and waits for events. |
| `executing` | The agent is running a hook or task. The message names it. |
| `rebooting` | The machine that hosts the agent is rebooting. The agent returns to `idle` when the reboot is complete. A reboot request from the charm causes this status. |
| `failed` | An operation of the agent failed. The message says which. |
| `lost` | The controller has not heard from the agent for an unexpectedly long time. The controller sets this status. While the agent is `lost`, the displayed workload status is `unknown`, unless the workload status is `error` or `terminated`. |

When a hook fails, `juju status` shows the workload status `error` and the agent status `idle`. The workload message is the message of the failure.

(unit-status-life)=
### Status of a unit from deployment to removal

Juju sets these statuses at fixed points of the life of a unit. A `status-set` call by the charm replaces the workload status at any point. The points, in order, are:

1. Juju creates the unit with the agent status `allocating` and the workload status `waiting`. The message is `waiting for machine` in a machine model and `installing agent` in a Kubernetes model.
2. The agent starts. If the workload status is `waiting` with one of the two creation messages, Juju sets `waiting` with the message `agent initialising`.
3. Before the install hook runs, Juju sets `maintenance` with the message `installing charm software`, unless the charm has already set a status.
4. After the start hook finishes, Juju sets `unknown` if the charm has set no status.
5. Before the stop hook runs, Juju sets `maintenance` with the message `stopping charm software`. After it finishes, Juju sets `maintenance` with no message.
6. Before the remove hook runs, Juju sets `maintenance` with the message `cleaning up prior to charm deletion`. After it finishes, Juju sets `terminated`.

(application-status)=
## Application status

Unless the leader unit has set the application status, Juju derives the application status from the units. The derived status is the displayed workload status of the unit with the highest severity, together with that unit's message. The severity of the workload statuses, from highest to lowest, is:

1. `error`
2. `blocked`
3. `maintenance`
4. `waiting`
5. `active`
6. `terminated`
7. `unknown`

One `blocked` unit therefore makes the application `blocked`, unless another unit is in `error`. When several units share the highest severity, Juju uses the leader unit if it is one of them, and otherwise the unit with the lowest number. An application without units has the derived status `unknown`.

The leader unit sets the application status with `status-set --application`. Juju displays a status that the leader has set in place of the derived status. When a unit that is not the leader calls `status-set --application`, the call fails with the error `this unit is not the leader`.

(juju-status-output)=
## Status in `juju status`

`juju status` shows the application status in the `Status` column of the application table. It shows the workload status and the agent status of each unit in the `Workload` and `Agent` columns of the unit table. An asterisk marks the leader unit.

````{dropdown} Expand to view a sample 'juju status' output

```text
Model        Controller           Cloud/Region        Version  Timestamp
charm-model  tutorial-controller  microk8s/localhost  4.1.0    14:23:55+02:00

App             Version  Status  Scale  Charm           Channel    Rev  Address         Exposed  Message
demo-api-charm  1.0.0    active      1  demo-api-charm               0  10.152.183.175  no
postgresql-k8s  14.7     active      1  postgresql-k8s  14/stable   73  10.152.183.237  no       Primary

Unit               Workload  Agent  Address      Ports  Message
demo-api-charm/0*  active    idle   10.1.157.72
postgresql-k8s/0*  active    idle   10.1.157.74         Primary
```

````

```{ibnote}
See more: `command-juju-status`
```
