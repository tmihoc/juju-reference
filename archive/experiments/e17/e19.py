import json,io,contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import e17
dom,D=e17.dom,e17.D
A=json.load(open('../e11/artifacts.json'))
parts={
 'state':lambda d:dom[d]['tables']>0,
 'dynamics':lambda d:A[d]['create']+A[d]['change']+A[d]['remove']>0,
 'failure':lambda d:A[d]['errors']>0,
 'interface':lambda d:A[d]['facade_kinds'].get('client',0)>0,
 'cross-process':lambda d:any(k!='client' for k in A[d]['facade_kinds']),
 'observation':lambda d:dom[d]['watch']>0,
 'lifecycle':lambda d:dom[d]['life'],
 'removal':lambda d:dom[d]['removal'],
 'migration':lambda d:dom[d]['migration'],
 'worker':lambda d:A[d]['workers']>0,
 'status':lambda d:dom[d]['status'],
}
band={'state':'spine','dynamics':'spine','lifecycle':'rare','removal':'rare'}
ok=0;out={}
for p,f in parts.items():
    n=sum(bool(f(d)) for d in D); r=n/len(D)
    actual='spine' if r>=.9 else 'rare' if r<.25 else 'conditional'
    pred=band.get(p,'conditional'); ok+=actual==pred
    out[p]=(n,r,pred,actual)
    print(f'{p:14s} {n:2d}/{len(D)} = {r:4.0%} predicted {pred:11s} actual {actual:11s} {"" if actual==pred else "MISS"}')
print('bands matched:',ok,'of',len(parts))
print('absent state?',[d for d in D if not parts['dynamics'](d)])
print('no dynamics:',[d for d in D if not parts['dynamics'](d)])
print('no failure:',[d for d in D if not parts['failure'](d)])
print('no interface:',[d for d in D if not parts['interface'](d)])
print('no interface and no cross-process:',[d for d in D if not parts['interface'](d) and not parts['cross-process'](d)])
# co-occurrence of parts: distinct part-sets
import collections
sets=collections.Counter(tuple(p for p,f in parts.items() if f(d)) for d in D)
print('distinct part sets:',len(sets),'largest:',[(len(k),v) for k,v in sets.most_common(5)])
