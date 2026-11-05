# E17: schema-only features against Go-level parts (criteria in the plan).
import re,os,json,glob,sys,collections
sys.path.insert(0,'../e15')
import e15
SRC=os.path.expanduser('~/git/misc/juju-v2-preview'); HERE=os.path.dirname(os.path.abspath(__file__))
TP=json.load(open(HERE+'/topics.json'))
V={'model':e15.parse(e15.NEW['model']),'controller':e15.parse(e15.NEW['controller'])}
def topic_tables(scope,topic):
    out=set()
    for f in glob.glob(f'{SRC}/domain/schema/{scope}/sql/*.sql'):
        b=re.sub(r'\.PATCH','',re.sub(r'^\d+-','',os.path.basename(f)))[:-4]
        if b==topic: out|=set(re.findall(r'CREATE TABLE (\w+)',open(f).read()))
    return out
def nontest(fs): return [f for f in fs if not f.endswith('_test.go') and 'mock' not in f]
dom={}
for scope,m in TP.items():
    if scope=='removal_types': continue
    for d,topics in m.items():
        r=dom.setdefault(d,dict(tables=0,life=False,watched=0,immutable=0,lookups=0,status=False,tabs=[]))
        for t in topics:
            for tb in topic_tables(scope,t):
                if tb not in V[scope]['tables']: continue
                ty=e15.typing(V[scope],tb)
                r['tabs'].append(scope+':'+tb)
                if ty['lookup']: r['lookups']+=1; continue
                r['tables']+=1; r['life']|=ty['life']; r['status']|=ty['status']
                r['watched']+= 1 if ty['watched'] else 0; r['immutable']+=1 if ty['immutable'] else 0
removal_doms=set(TP['removal_types'].values())
for d,r in dom.items():
    base=f'{SRC}/domain/{d}'
    svc=nontest(glob.glob(base+'/service/**/*.go',recursive=True))
    r['watch']=len({m for f in svc for m in re.findall(r'^func \([^)]*\) (Watch\w+)\(',open(f).read(),flags=re.M)})
    r['removal']=d in removal_doms
    r['migration']=os.path.isdir(base+'/modelmigration')
    r['errors']=sum(len(re.findall(r'ConstError',open(f).read())) for f in nontest(glob.glob(base+'/errors/*.go')+glob.glob(base+'/errors.go')))
    r['pkg']=os.path.isdir(base)
def rule(name,pred_fn,act_fn,ds,note=''):
    ok=[d for d in ds if pred_fn(dom[d])==act_fn(dom[d])]
    bad=[d for d in ds if d not in ok]
    maj=max(sum(act_fn(dom[d]) for d in ds),len(ds)-sum(act_fn(dom[d]) for d in ds))/len(ds)
    print(f'{name}: accuracy {len(ok)}/{len(ds)} = {len(ok)/len(ds):.0%}, majority baseline {maj:.0%}; violations {bad} {note}')
    return len(ok)/len(ds)
D=[d for d,r in dom.items() if r['tables']>0 and r['pkg']]
print('domains with tables and a package:',len(D),sorted(D))
print('domains without package:',[d for d,r in dom.items() if not r['pkg']])
rule('R1 watch iff watched table',lambda r:r['watched']>0,lambda r:r['watch']>0,D)
L=[d for d in D if dom[d]['life']]
ok=[d for d in L if dom[d]['removal']]
print(f'R2 life => removal: {len(ok)}/{len(L)} = {len(ok)/max(1,len(L)):.0%}; violations {[d for d in L if d not in ok]}')
conv=[d for d in D if dom[d]['removal'] and not dom[d]['life']]
print('   converse failures (removal without life):',conv)
rule('R3 migration iff owns table',lambda r:r['tables']>0,lambda r:r['migration'],D)
json.dump({d:{k:v for k,v in r.items() if k!='tabs'} for d,r in dom.items()},open(HERE+'/e17_result.json','w'),indent=1)
print({d:(r['tables'],int(r['life']),r['watched'],r['watch'],int(r['removal']),int(r['migration'])) for d,r in sorted(dom.items())})

# post hoc (not registered): restrict by schema scope
def scope_of(d): return {s for s in ('model','controller') if any(t.startswith(s+':') for t in dom[d]['tabs'])}
M=[d for d in D if 'model' in scope_of(d)]; Cn=[d for d in D if scope_of(d)=={'controller'}]
print('--- post hoc')
print('model-scope domains',len(M),'controller-only',len(Cn),sorted(Cn))
# life tables by scope
def life_in(d,s): return any(t.startswith(s+':') and e15.typing(V[s],t.split(':')[1])['life'] for t in dom[d]['tabs'])
Lm=[d for d in M if life_in(d,'model')]
print('R2 (life column in the model schema => removal job):',sum(dom[d]['removal'] for d in Lm),'/',len(Lm),'violations',[d for d in Lm if not dom[d]['removal']])
print('life in controller schema only:',[d for d in D if life_in(d,'controller') and not life_in(d,'model')],'removal job:',[dom[d]['removal'] for d in D if life_in(d,'controller') and not life_in(d,'model')])
ok=[d for d in M if dom[d]['migration']]
print('R3 (model-scope tables => modelmigration):',len(ok),'/',len(M),'violations',[d for d in M if not dom[d]['migration']])
print('controller-only domains with migration:',[d for d in Cn if dom[d]['migration']])
print('R1 within model scope:',sum((dom[d]['watched']>0)==(dom[d]['watch']>0) for d in M),'/',len(M),' controller-only:',sum((dom[d]['watched']>0)==(dom[d]['watch']>0) for d in Cn),'/',len(Cn))
