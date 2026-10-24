import sys,re,collections,io,contextlib,json
sys.path.insert(0,'../e15')
import e15
with contextlib.redirect_stdout(io.StringIO()):
    import e17
V={s:e15.parse(e15.NEW[s]) for s in ('model','controller')}
T={s:set(V[s]['tables']) for s in V}
life={(s,t) for s in V for t in T[s] if e15.typing(V[s],t)['life']}
lifenouns={t.split('_')[0] for s,t in life}|{'model','application','machine','unit','relation','storage'}
def group(name):
    out=[]
    for s in V:
        for t in T[s]:
            if e15.typing(V[s],t)['lookup']: continue
            toks=t.split('_')
            if t==name or toks[0]==name or toks[-1]==name or t.startswith(name+'_') or t.endswith('_'+name): out.append((s,t))
    return out
def facts(name):
    g=group(name); tabs=[t for s,t in g]
    haslife=any((s,t) in life for s,t in g) or any(t.split('_')[0]==name and (s,t) in life for s,t in g)
    targets=set()
    for s,t in g:
        toks=t.split('_')
        for tok in toks:
            if tok!=name and tok in lifenouns: targets.add(tok)
        # fk life ancestors of a different noun
        fk=set(re.findall(r'REFERENCES\s+"?(\w+)',V[s]['tables'][t]))
        for p in fk:
            if (s,p) in life and p.split('_')[0]!=name: targets.add(p.split('_')[0])
    return dict(tables=len(g),life=haslife,targets=sorted(targets))
hand={'constraint':'facet','status':'facet','credential':'entity','resource':'entity','relation':'entity','annotation':'facet'}
def rule(f):
    if f['life']: return 'entity'
    if len(f['targets'])>=3: return 'facet'
    return 'record'
agree=0;n=0
for name,h in hand.items():
    f=facts(name); r=rule(f)
    if name!='annotation': n+=1; agree+= (r==h)
    print(f'{name:11s} hand={h:7s} rule={r:7s} tables={f["tables"]:2d} life={f["life"]} targets={f["targets"]}')
print('T2: rule agrees with hand type on',agree,'of',n,'(annotation shown but not counted: typed outside E21c)')
# T3
K=json.load(open('e24.json'))
dom=e17.dom; D=e17.D
empty=[d for d in D if not (dom[d]['life'] or K.get(d) or dom[d]['tables'])]
print('T3: domains with no non-empty identity clause:',empty,'of',len(D))
