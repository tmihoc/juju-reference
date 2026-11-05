# E29 exploratory pass (not registered): structure of the life tables and their dependants in the 4.1 schema.
import sys,re,collections,json
sys.path.insert(0,'../e15')
import e15
def run(scope):
    V=e15.parse(e15.NEW[scope]); T=V['tables']
    fk={t:set(re.findall(r'REFERENCES\s+"?(\w+)',b)) for t,b in T.items()}
    lookup={t for t in T if e15.typing(V,t)['lookup']}
    life={t for t in T if e15.typing(V,t)['life']}
    # nearest life ancestors by FK, stopping at the first life table
    def anc(t,seen=()):
        out=set()
        for p in fk[t]-lookup:
            if p==t or p in seen: continue
            if p in life: out.add(p)
            else: out|=anc(p,seen+(t,))
        return out
    comp=collections.defaultdict(list); free=[]; multi=[]
    for t in T:
        if t in lookup or t in life: continue
        a=anc(t)
        if len(a)==1: comp[next(iter(a))].append(t)
        elif not a: free.append(t)
        else: multi.append((t,sorted(a)))
    return V,fk,life,lookup,comp,free,multi,anc
for scope in ('model','controller'):
    V,fk,life,lookup,comp,free,multi,anc=run(scope)
    print('=====',scope,'life tables',len(life))
    for l in sorted(life):
        parents=sorted(p for p in fk[l] if p in life and p!=l)
        print(f'{l}: life parents {parents}; components {len(comp[l])}: {sorted(comp[l])[:12]}')
    print('multi-owner tables:',len(multi),multi[:14])
    print('free tables (no life ancestor):',len(free),sorted(free)[:40])
