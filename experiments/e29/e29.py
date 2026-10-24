import sys,re,collections,json,io,contextlib
sys.path.insert(0,'../e15')
import e15
def analyse(scope):
    V=e15.parse(e15.NEW[scope]); T=V['tables']
    fk={t:set(re.findall(r'REFERENCES\s+"?(\w+)',b)) for t,b in T.items()}
    lookup={t for t in T if e15.typing(V,t)['lookup']}; life={t for t in T if e15.typing(V,t)['life']}
    def anc(t,seen=()):
        out=set()
        for p in fk[t]-lookup:
            if p==t or p in seen: continue
            out|= {p} if p in life else anc(p,seen+(t,))
        return out
    noun=lambda t:t.split('_')[0]
    single=[];multi=[];free=[]
    for t in T:
        if t in lookup or t in life: continue
        a=anc(t)
        (single if len(a)==1 else multi if a else free).append((t,a))
    c1=[(t,noun(t),noun(next(iter(a)))) for t,a in single]
    ok1=[x for x in c1 if x[1]==x[2]]
    c2=[(t,noun(t),{noun(x) for x in a}) for t,a in multi]
    ok2=[x for x in c2 if x[1] in x[2]]
    groups=collections.Counter(noun(t) for t in T if t not in lookup)
    return dict(single=len(c1),ok1=len(ok1),bad1=[x for x in c1 if x not in ok1],multi=len(c2),ok2=len(ok2),bad2=[x for x in c2 if x not in ok2],groups=groups,free=len(free))
for scope in ('model','controller'):
    r=analyse(scope)
    print('=====',scope)
    print('C1 single-owner: S1==S2',r['ok1'],'/',r['single'],'= %.0f%%'%(100*r['ok1']/max(1,r['single'])),'; disagreements:',[(t,a,b) for t,a,b in r['bad1']])
    print('C2 multi-owner: noun in owners',r['ok2'],'/',r['multi'],'; disagreements:',[(t,n,sorted(o)) for t,n,o in r['bad2']])
    if scope=='model':
        print('groups >=3:',[(k,v) for k,v in r['groups'].most_common() if v>=3])
