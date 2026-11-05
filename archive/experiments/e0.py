import subprocess,shlex,os,collections,re
def sh(c): return subprocess.run(c,shell=True,capture_output=True,text=True).stdout
def files(pat,fixed=True,extra=""):
    flag='-F' if fixed else '-E'
    out=sh(f"git grep -l --no-color {flag} -e {shlex.quote(pat)} -- '*.go' '*.sql' ':!*_test.go' ':!*/mocks/*' ':!*mock*' ':!docs/*' ':!*.gen.go' {extra}")
    return [f for f in out.split() if f]
def lca(fs):
    if not fs: return None
    parts=[f.split('/')[:-1] for f in fs]
    c=os.path.commonprefix(parts)
    return '/'.join(c) or '(repo root)'
def root_area(f):
    if f.startswith('domain/schema'): return 'schema'
    m=re.match(r'domain/([^/]+)/(state|service|errors|bootstrap|modelmigration)?',f)
    if m: return 'domain:'+m.group(1)
    if f.startswith('apiserver/'): return 'apiserver'
    if f.startswith('api/') or f.startswith('cmd/juju/'): return 'client'
    if f.startswith('internal/worker') or f.startswith('cmd/jujuagentd'): return 'worker/agent'
    if f.startswith('core/'): return 'core'
    if f.startswith('internal/provider') or f.startswith('environs'): return 'provider'
    return f.split('/')[0]
S=[
("Names nest one container level ('too many containers')","too many containers"),
("Only lxd container type supported","invalid container type"),
("Invalid machine constraints (container type/space)","invalid machine constraints"),
("Constraint violation compares architecture only","machine constraint violation"),
("Machine primary record, unique name","CREATE TABLE machine (",),
("machine not found","machine not found"),
("machine already exists (import)","machine already exists"),
("Life values alive/dying/dead","dying"),
("Parent record for containers","machine_parent"),
("Cloud instance record","machine_cloud_instance"),
("Agent status vs instance status records","machine_status"),
("Machine kinds derived by views","v_machine_is_controller"),
("Manual machine flag record","machine_manual"),
("Compute provisioner provisions instances","ProvisionerTask"),
("LXD broker provisions containers on host","NewLXDBroker"),
("Manual provisioning script","ProvisioningScript"),
("Removal marks dying, jobs purge records","MachineJob"),
("Reboot decision (shutdown/reboot/none)","grandparent machine are not supported"),
("Reprovision lost machine","ReprovisionMachine"),
("Keep-instance flag decides release","ShouldKeepInstance"),
("Machine watchers (life, containers, instance states)","WatchMachineLife"),
("Machine designation grammar (0, lxd:25, 0/lxd/4)","ParsePlacement"),
("Base format ubuntu@22.04","ParseBaseFromString"),
]
rows=[]
for desc,pat in S:
    fs=files(pat)
    if len(fs)>60: fs=[]  # too generic to anchor
    areas=sorted({root_area(f) for f in fs})
    rows.append((desc,len(fs),lca(fs),areas))
for d,n,l,a in rows:
    print(f"{d[:52]:52} files={n:3} LCA={str(l)[:34]:34} areas={','.join(a)[:70]}")
