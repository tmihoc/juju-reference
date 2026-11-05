---
myst:
  html_meta:
    description: "Juju status reference: the application status, the unit workload status and the unit agent status, with their values, meanings, and who sets them."
---

(status)=
# Status

A status is a value that reports the condition of an application or a unit, with a message and a timestamp. Each application has one status. Each unit has two: a workload status, which reports its charm's workload, and an agent status, which reports the {ref}`unit agent <unit-agent>` that runs the charm.

(application-status)=
## Application status

An application's status is the status its charm has set for it. When the charm has set none, the application status is taken from the application's units.

Only the {ref}`leader unit <leader-unit>` can set the application status. It does so with the {ref}`status-set <hook-command-status-set>` hook command and its `--application` option.

The status that an application takes from its units is the workload status shown for the unit with the highest severity. From the highest to the lowest, the severities are `error`, `blocked`, `maintenance`, `waiting`, `active`, `terminated`, and `unknown`. One unit in `blocked` makes the application `blocked` when no unit is in `error`. The application also takes the message of that unit.

When several units have the same severity, the application takes the status of the leader unit, or, when there is no leader, of the unit with the lowest unit number. An application with no units is `unknown`.

(unit-status)=
## Unit status

A unit's status has two parts: the workload status and the agent status. A client shows them as two separate values.

(workload--charm-status)=
### Workload status

The workload status reports the condition of the unit's charm and its workload. A charm sets it with the {ref}`status-set <hook-command-status-set>` hook command to one of `active`, `maintenance`, `waiting`, and `blocked`. The command accepts each of the four at any time and rejects every other value. Juju sets `error`, `unknown`, and `terminated`.

| Status | Set by | Meaning |
|--|--|--|
| `active` | Charm | The unit believes it is correctly offering all the services it has been asked to offer. |
| `maintenance` | Charm, Juju | The unit is not providing a service yet, but expects to soon, for example while installing. It needs no action from a person. Juju sets it with the messages `installing charm software`, `stopping charm software`, and `cleaning up prior to charm deletion` before the {ref}`install <hook-install>`, stop, and {ref}`remove <hook-remove>` hooks run. |
| `waiting` | Charm, Juju | The unit needs no action from a person, but it does not provide a service yet because it depends on an external factor, for example an application it is integrated with that is not running. Juju sets it on a new unit. |
| `blocked` | Charm | The unit cannot continue without input from a person. The message tells the person what to do. |
| `error` | Juju | A hook of the unit failed, or a charm upgrade of the unit failed. The message is `hook failed: "<hook>"` for a hook and `upgrade failed` for an upgrade. For a hook, the status data names the hook. |
| `unknown` | Juju | The {ref}`start <hook-start>` hook has finished and the charm has set no workload status. Juju also shows `unknown` in place of a stored workload status other than `error` and `terminated` while the unit agent is not communicating with the controller. |
| `terminated` | Juju | The unit's {ref}`remove <hook-remove>` hook has finished. |

#### Workload status of a new unit

A new unit has the workload status `waiting` and the agent status `allocating`. The workload message is `waiting for machine` for a machine unit and `installing agent` for a Kubernetes unit. When the unit agent starts, the message changes to `agent initialising`. Before the install hook runs, Juju sets `maintenance` with the message `installing charm software`, unless the charm has already set a status. After the start hook finishes, the workload status is `unknown` unless the charm has set one.

#### Workload status of a Kubernetes unit

For a Kubernetes unit, the workload status shown can be the status of the unit's pod: `blocked`, `waiting`, or `running`. The charm's own status is shown when it is `terminated`, `blocked`, or `maintenance`. For any other charm status, the pod's status is shown in exactly these cases:

- The pod is `blocked`.
- The pod is `waiting` and the charm's status is `active`.
- The pod is `running` and the charm's status is still the one Juju gave the new unit: `waiting` with the message `waiting for container`, `installing agent`, or `agent initialising`.

In every other case the charm's status is shown.

### Agent status

The agent status reports what the unit agent is doing. The unit agent and Juju set it. A charm sets only the workload status.

| Status | Meaning |
|--|--|
| `idle` | The agent is running and has no work. It stays `idle` until a hook or a task needs to run. |
| `executing` | The agent is running a hook or a task. The message names which one. |
| `allocating` | The unit exists and the machine, or the pod, that is to host it is not yet running the agent. |
| `rebooting` | A hook requested a reboot of the machine. The status returns to `idle` when the reboot is complete. |
| `failed` | An operation of the agent itself failed. The message names the operation. |
| `lost` | The agent has not communicated with the controller for an unexpectedly long time. The message is `agent is not communicating with the server`. |

When a hook fails, the agent status is shown as `idle` and the unit's workload status is `error`, with the message of the failure.

(status-in-output)=
## Status in client output

A client reports the application status and the two unit statuses separately. The `juju status` command shows the application status in the `Status` column of its `App` table, and the unit's workload status and agent status in the `Workload` and `Agent` columns of its `Unit` table.

```{ibnote}
See more: `command-juju-status`
```
