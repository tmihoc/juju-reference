import subprocess,re,collections,itertools,sys
rng=sys.argv[1]
out=subprocess.run(['git','log','--no-merges','--name-only','--format=@@%h',rng],capture_output=True,text=True).stdout
def area(p):
    if p.endswith('_test.go') or '/mocks/' in p or 'mock' in p.split('/')[-1] or p.endswith('.gen.go'): return None
    if p.startswith('domain/schema/'): return 'schema'
    m=re.match(r'domain/([^/]+)/(state|service)/',p)
    if m: return m.group(2)
    if p.startswith('apiserver/') or p.startswith('rpc/params') or p.startswith('api/'): return 'api'
    if p.startswith('internal/worker/') or p.startswith('cmd/jujuagentd'): return 'worker'
    if p.startswith('cmd/juju/'): return 'cli'
    if p.startswith('core/'): return 'core'
    if p.startswith('docs/'): return 'docs'
    return None
commits=[]
cur=None
for l in out.splitlines():
    if l.startswith('@@'): cur=set(); commits.append(cur)
    elif l.strip() and cur is not None:
        a=area(l.strip())
        if a: cur.add(a)
commits=[c for c in commits if c]
N=len(commits)
areas=['schema','state','service','api','worker','cli','core']
cnt=collections.Counter(a for c in commits for a in c if a in areas)
print('commits with code in these areas (non-test, non-generated):',sum(1 for c in commits if c&set(areas)),'of',N)
print('P(area):',{a:round(cnt[a]/N,2) for a in areas})
print('\nP(col | row)  -- when the row area changes, how often the column changes too')
print('%-8s'%''+''.join('%8s'%b for b in areas))
for a in areas:
    row=[]
    for b in areas:
        both=sum(1 for c in commits if a in c and b in c)
        row.append('%8.2f'%(both/cnt[a] if cnt[a] else 0))
    print('%-8s'%a+''.join(row))
# commits touching exactly one area
single=collections.Counter(next(iter(c&set(areas))) for c in commits if len(c&set(areas))==1)
multi=sum(1 for c in commits if len(c&set(areas))>1)
print('\nsingle-area commits:',dict(single),' multi-area commits:',multi)
sizes=collections.Counter(len(c&set(areas)) for c in commits if c&set(areas))
print('areas touched per commit:',dict(sorted(sizes.items())))
