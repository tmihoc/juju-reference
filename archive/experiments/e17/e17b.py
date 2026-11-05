import json,collections,sys
sys.argv=['x']
import io,contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import e17
dom,D,V,e15=e17.dom,e17.D,e17.V,e17.e15
def scope_of(d): return tuple(sorted(s for s in ('model','controller') if any(t.startswith(s+':') for t in dom[d]['tabs'])))
def life_scope(d):
    return tuple(sorted(s for s in ('model','controller') if any(t.startswith(s+':') and e15.typing(V[s],t.split(':')[1])['life'] for t in dom[d]['tabs'])))
A=lambda d:(bool(life_scope(d)),)
B=lambda d:(scope_of(d),life_scope(d))
C=lambda d:(scope_of(d),life_scope(d),dom[d]['watched']>0)
T={'watch':lambda d:dom[d]['watch']>0,'removal':lambda d:bool(dom[d]['removal']),'migration':lambda d:bool(dom[d]['migration'])}
def loo(typing,target):
    ok=0;bad=[]
    for d in D:
        others=[x for x in D if x!=d and typing(x)==typing(d)]
        pool=others or [x for x in D if x!=d]
        votes=collections.Counter(target(x) for x in pool)
        pred=votes.most_common(1)[0][0] if votes[True]!=votes[False] else collections.Counter(target(x) for x in D if x!=d).most_common(1)[0][0]
        if pred==target(d): ok+=1
        else: bad.append(d)
    return ok/len(D),bad
res={}
for nm,ty in (('A',A),('B',B),('C',C)):
    res[nm]={t:loo(ty,f) for t,f in T.items()}
    print(nm,'types',len({ty(d) for d in D}),{t:'%.0f%%'%(100*a) for t,(a,b) in res[nm].items()},'mean %.0f%%'%(100*sum(a for a,b in res[nm].values())/3))
print('baseline majority:',{t:'%.0f%%'%(100*max(sum(f(d) for d in D),len(D)-sum(f(d) for d in D))/len(D)) for t,f in T.items()})
for t in T: print(' C misses for',t,res['C'][t][1])
types=collections.defaultdict(list)
for d in D: types[C(d)].append(d)
for k,v in sorted(types.items(),key=lambda x:-len(x[1])): print(k,v)
