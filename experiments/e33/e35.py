import sys,re,os,glob,json,sqlite3,collections
sys.path.insert(0,'../e15')
import e15
SRC=os.path.expanduser('~/git/misc/juju-v2-preview')
man=json.load(open('page-manifest.json')); home={t:p for p,d in man['pages'].items() for t in d['tables']}
dbs={}
for s in ('model','controller'):
    db=sqlite3.connect(':memory:')
    for st in e15.split(open(e15.NEW[s]).read()): db.executescript(st.rstrip().rstrip(';')+';')
    dbs[s]=db
def pk(t):
    for s,db in dbs.items():
        rows=db.execute(f'PRAGMA table_info("{t}")').fetchall()
        if rows: return [r[1] for r in sorted(rows,key=lambda r:r[5]) if r[5]>0], s
    return [],None
def fks(t):
    out=[]
    for s,db in dbs.items():
        for r in db.execute(f'PRAGMA foreign_key_list("{t}")').fetchall(): out.append((r[3],r[2]))   # col, parent table
    return out
VERBS=set('add remove list show set get update create delete change grant revoke enable disable attach detach register unregister import export find retry resolve switch use run cancel wait expose unexpose download upload scale refresh consume suspend resume bind trust info destroy kill trace debug dump login logout whoami'.split())
def fold(w):
    w=w.lower()
    for suf in ('manager','client'):
        if w.endswith(suf) and len(w)>len(suf)+2: w=w[:-len(suf)]
    return w[:-1] if w.endswith('s') and not w.endswith('ss') else w
cmds=set()
for f in glob.glob(SRC+'/cmd/juju/**/*.go',recursive=True)+glob.glob(SRC+'/cmd/plugins/**/*.go',recursive=True):
    if f.endswith('_test.go'): continue
    for m in re.finditer(r'Name:\s+"([a-z][a-z0-9-]+)"',open(f).read()): cmds.add(m.group(1))
cmdtok={fold(t) for c in cmds for t in c.split('-') if t not in VERBS}
cmdfold={'-'.join(fold(t) for t in c.split('-')) for c in cmds}
facs={fold(d) for d in os.listdir(SRC+'/apiserver/facades/client')}
hooks=[re.sub(r'\.go$','',os.path.basename(f)) for f in glob.glob(SRC+'/internal/worker/uniter/runner/jujuc/*.go') if not f.endswith('_test.go')]
hooktok={fold(t) for h in hooks for t in h.split('-')}
RM=('remove','delete','destroy','kill','revoke','unset','cancel')
rmcmd=[c for c in cmds if c.split('-')[0] in RM]
rmfac=set()
for f in glob.glob(SRC+'/apiserver/facades/client/**/*.go',recursive=True):
    if f.endswith('_test.go'): continue
    for m in re.finditer(r'^func \([^)]*\) ((?:Remove|Delete|Destroy|Kill|Revoke|Unset|Cancel)[A-Za-z]*)\(',open(f).read(),flags=re.M): rmfac.add(m.group(1).lower())
def props(name,tables,lookups=()):
    toks=[fold(t) for t in name.split('-')]
    comp='-'.join(toks)
    if len(toks)==1: a_cmd=toks[0] in cmdtok or toks[0] in facs; a_hook=toks[0] in hooktok
    else: a_cmd=any(comp in c for c in cmdfold) or ''.join(toks) in facs; a_hook=any(comp in '-'.join(fold(t) for t in h.split('-')) for h in hooks)
    G=set(tables)
    # lead table
    indeg=collections.Counter()
    for t in G:
        for c,p in fks(t):
            if p in G and p!=t: indeg[p]+=1
    lead=e15.lead_table(name,G,indeg) if G else None
    b=None
    if lead:
        cols,_=pk(lead); f=fks(lead)
        ext=len(cols)==1 and any(c==cols[0] and p not in G for c,p in f)
        b=not ext
    # referenced elsewhere
    ref=set()
    for t,p in home.items():
        if t in G: continue
        for c,par in fks(t):
            if par in G: ref.add(home[t])
    # life / removal verb
    life=any(any(e15.typing(e15.parse.__globals__.get('V',{}) if False else None,'x') for _ in []) for _ in [])
    d_life=False
    V={s:e15.parse(e15.NEW[s]) for s in ('model','controller')} if not hasattr(props,'V') else props.V
    props.V=V
    for t in G:
        for s in V:
            if t in V[s]['tables'] and e15.typing(V[s],t)['life']: d_life=True
    nounrm=[c for c in rmcmd if comp in '-'.join(fold(t) for t in c.split('-')[1:])]
    nounrmf=[m for m in rmfac if ''.join(toks) in m]
    d=d_life or bool(nounrm) or bool(nounrmf)
    return dict(a=a_cmd,a_hook=a_hook,b=b,c=sorted(ref),d=d,d_life=d_life,lead=lead)
rows={}
for p,d in man['pages'].items():
    if not d['tables']: rows[p]=None; continue
    rows[p]=props(p,d['tables'])
controls={'cloud-instance':['machine_cloud_instance','machine_cloud_instance_status','instance_tag'],'unit-state':['unit_state','unit_state_charm','unit_state_relation'],
 'relation-unit':['relation_unit','relation_unit_departure','relation_unit_setting','relation_unit_setting_archive','relation_unit_settings_hash'],
 'application-endpoint':['application_endpoint','application_extra_endpoint'],'application-scale':['application_scale'],'machine-placement':['machine_placement']}
crow={n:props(n,t) for n,t in controls.items()}
def char(r): return bool((r['a'] or r['a_hook']) and r['b'] and r['c'])
out=dict(pages={p:(r and dict(r,character=char(r))) for p,r in rows.items()},controls={n:dict(r,character=char(r)) for n,r in crow.items()})
json.dump(out,open('e35_result.json','w'),indent=1)
ch=[p for p,r in rows.items() if r and char(r)]; leg=[p for p,r in rows.items() if r and not char(r)]
print('pages with tables',len([1 for r in rows.values() if r]),'characters',len(ch),'candidate legs',len(leg))
print('CANDIDATE LEGS (fails a,b or c):')
for p in sorted(leg): r=rows[p]; print(f"  {p:20s} a={r['a']!s:5} (hook {r['a_hook']!s:5}) b={r['b']!s:5} c={r['c']} d={r['d']}")
print('\nprediction 2 (port, zone, agent-version, model-defaults, telemetry fail):',[(p,p in leg) for p in ('port','zone','agent-version','model-defaults','telemetry')])
life9=['application','machine','unit','relation','storage','model','controller','object-store','offer']
print('prediction 3 (life pages pass):',[(p,p in ch) for p in life9])
print('\nNEGATIVE CONTROLS:'); 
for n,r in crow.items(): print(f"  {n:22s} a={r['a']!s:5} b={r['b']!s:5} c={r['c']} d={r['d']} -> {'CHARACTER (control fails to fail)' if char(r) else 'leg'}  lead={r['lead']}")
print('controls failing the definition:',sum(1 for r in crow.values() if not char(r)),'/ 6')
print('d reported: pages with d false:',[p for p,r in rows.items() if r and not r['d']])

# ---- post hoc variant (c'): other nouns' interface operations reach this page's tables (E30 call graph)
R=json.load(open('../e30/e30_roots.json')); VM=json.load(open('../e30/viewmap.json'))
page_of=dict(home)
for p,d in man['pages'].items():
    for l in d['lookups']: page_of[l]=p
def facnoun(pkg): return fold(pkg.split('/')[-1])
reach=collections.defaultdict(set)   # page -> set of other facade packages reaching it
for r in R:
    if r['kind']!='facade': continue
    ts=set(r['tables'] or [])
    for t in list(ts):
        if t in VM: ts|=set(VM[t])
    for t in ts:
        p=page_of.get(t)
        if not p: continue
        toks={fold(x) for x in p.split('-')}|{''.join(fold(x) for x in p.split('-'))}
        if facnoun(r['pkg']) not in toks: reach[p].add(r['pkg'].split('/')[-1])
def charp(p,r): return bool((r['a'] or r['a_hook']) and r['b'] and len(reach.get(p,()))>=1)
chp=[p for p,r in rows.items() if r and charp(p,r)]
print('\n=== post hoc (c-prime): referenced by operations of another facade ===')
print('characters',len(chp),'of',len([1 for r in rows.values() if r]))
print('still legs:',sorted(p for p,r in rows.items() if r and not charp(p,r)))
print('prediction 2 under c-prime:',[(p,p not in chp) for p in ('port','zone','agent-version','model-defaults','telemetry')])
print('prediction 3 under c-prime:',[(p,p in chp) for p in life9])
print('other facades reaching each page (count):',{p:len(reach.get(p,())) for p in sorted(rows) if rows[p]})
