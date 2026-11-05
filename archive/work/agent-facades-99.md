# Agent facades: the per-facade diff (session 99)

Derived from the 4.1 code at `/tmp/juju-41-tree` (e5db99d585), constructor checks unless noted. The scout agent's table had errors; every row below was re-verified against the code in-session (grep + direct reads). Key semantics: `AuthMachineAgent` also admits a login with a controller-agent tag (`apiserver/root.go:278-283`), so "machine agents" below includes the controller agent; `AuthController` (`root.go:310-312`) is the `authInfo.Controller` login (the controller itself).

| Facade (registered) | Serves | Evidence |
|---|---|---|
| `Agent` | machine, unit | agent/register.go:25 |
| `AgentLifeFlag` | machine, unit, model; refuses only a login as an application | lifeflag/facade.go:62 (`if !AuthUnitAgent() && AuthApplicationAgent()`) |
| `CAASAdmission` | machine | caasadmission/register.go (newStateFacade) |
| `CAASAgent` v2 | model | caasagent/register.go:33 |
| `CAASAgent` v3 | model, controller agent | caasagent/register.go:68 |
| `CAASApplication` | application, unit | caasapplication/register.go:24 |
| `CredentialValidator` | machine, unit, application | credentialvalidator/register.go:38 |
| `Deployer` | machine | deployer/register.go:26 |
| `DiskManager` | machine | diskmanager/register.go:42 |
| `HostKeyReporter` | no kind check; per-entity `AuthOwner` | hostkeyreporter/facade.go:38-42 |
| `InstanceMutater` | no check | (none in package) |
| `KeyUpdater` | machine | keyupdater/register.go:35 |
| `LeadershipService` | unit, application | leadership/leadership.go:34 |
| `Logger` | machine, unit, application, model | logger/logger.go:71-74 |
| `Machiner` | machine | machine/machiner.go:161 |
| `MachineActions` | machine | machineactions/machineactions.go:70 |
| `MigrationFlag` | machine, unit | migrationflag/facade.go:35 |
| `MigrationMinion`, `MigrationStatusWatcher` | machine, unit | migrationminion.go:33, migrationstatuswatcher.go:28 |
| `PayloadsHookContext` | unit, application | payloadshookcontext/register.go:27,37 |
| `Provisioner` | machine, controller | provisioner/provisioner.go:77 |
| `ProxyUpdater` | machine, unit, application, model | proxyupdater/proxyupdater.go:54 |
| `Reboot` | machine | reboot/reboot.go:46 |
| `ResourcesHookContext` | unit, application | resourceshookcontext/register.go:27 |
| `RetryStrategy` | unit, application | retrystrategy/retrystrategy.go:51 |
| `SecretsDrain` | unit | secretsdrain/register.go:26 |
| `SecretsManager` | unit | secretsmanager/register.go:43 |
| `SSHSession` | machine | sshsession/register.go:28 |
| `StorageProvisioner` | machine; its `VolumeAttachmentsWatcher`, `VolumeAttachmentPlansWatcher`, `FilesystemAttachmentsWatcher` serve machine, unit, model | storageprovisioner.go:102, watcher.go:147 |
| `Tracer` | machine, unit, application, model | tracer/tracer.go:31-34 |
| `Uniter` | unit | uniter/register.go:97 |
| `Upgrader` | machine, unit, model | upgrader/register.go:36-38 |

Applied to `docs/reference/agent.md` as the `## Agent facades` section (anchor `(agent-facades)=`), grouped by agent kind, with the controller-agent and application-login rules stated in the intro and the unit bullet.

## Code questions for the Juju developers

- `lifeflag/facade.go:62`: `if !authorizer.AuthUnitAgent() && authorizer.AuthApplicationAgent() { return ErrPerm }` denies only a login that is an application agent and not a unit agent. Machine and model logins pass. Is the intended check not `!AuthUnitAgent() && !AuthMachineAgent()`? As written, a model agent (the model operator) can read an application's life flag.
- `caasapplicationprovisioner/worker.go:171` sets application agent passwords, so a login as an application exists on Kubernetes; no `containeragent` subcommand for it was found. Who logs in with it?

## Scout corrections (why the table was re-derived)

The FacadeDiff scout (history://FacadeDiff) reported logger as machine+unit (code: all four kinds), upgrader with an application check (code: none), sshsession/diskmanager/deployer/keyupdater/machiner/machineactions/reboot as machine+unit (code: machine only), leadership as machine+unit (code: unit+application), uniter/secretsmanager/secretsdrain as unit+application (code: unit only), hostkeyreporter as machine+unit (code: no kind check). Standing rule (re-verify each subagent finding) caught them.