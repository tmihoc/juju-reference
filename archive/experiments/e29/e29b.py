import sys,re,collections,os,glob,io,contextlib
sys.path.insert(0,'../e15')
import e15
SRC=os.path.expanduser('~/git/misc/juju-v2-preview')
V=e15.parse(e15.NEW['model']); T=V['tables']
fk={t:set(re.findall(r'REFERENCES\s+"?(\w+)',b)) for t,b in T.items()}
lookup={t for t in T if e15.typing(V,t)['lookup']}; life={t for t in T if e15.typing(V,t)['life']}
def anc(t,seen=()):
    out=set()
    for p in fk[t]-lookup:
        if p==t or p in seen: continue
        out|= {p} if p in life else anc(p,seen+(t,))
    return out
roots={'relation':{'relation'},'unit':{'unit'},'application':{'application'},'machine':{'machine'},'storage':{t for t in life if t.startswith('storage_')}}
tot_d=tot_in=tot_k=tot_kd=0
for X,rs in roots.items():
    txt=open(f'{SRC}/domain/removal/state/model/{X}.go').read()
    D={t for t in set(re.findall(r'DELETE\s+FROM\s+"?(\w+)',txt)) if t in T and t not in lookup}
    K={t for t in T if t not in lookup and t not in life and anc(t)&rs}
    G={t for t in T if t not in lookup and t.split('_')[0]==X}
    inK=D&(K|G); out=D-(K|G)
    rec=K&D
    tot_d+=len(D);tot_in+=len(inK);tot_k+=len(K);tot_kd+=len(rec)
    print(f'## {X}: |D|={len(D)} in K or noun group {len(inK)}; |K|={len(K)} of which deleted {len(rec)}; outside: {sorted(out)}; K not deleted: {sorted(K-D)[:12]}')
print('precision %d/%d = %.0f%%; recall %d/%d = %.0f%%'%(tot_in,tot_d,100*tot_in/tot_d,tot_kd,tot_k,100*tot_kd/tot_k))
