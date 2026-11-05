import re,io,contextlib,statistics
with contextlib.redirect_stdout(io.StringIO()):
    import e17
dom,D,V,e15=e17.dom,e17.D,e17.V,e17.e15
owner={}
for d,r in dom.items():
    for t in r['tabs']: owner[t]=d
fan={}
for d in D:
    refs=set()
    for t in dom[d]['tabs']:
        sc,tb=t.split(':')
        for ref in re.findall(r'REFERENCES\s+"?(\w+)',V[sc]['tables'][tb]):
            o=owner.get(sc+':'+ref)
            if o and o!=d: refs.add(o)
    fan[d]=refs
rank=sorted(D,key=lambda d:-len(fan[d]))
for i,d in enumerate(rank[:10],1): print(i,d,len(fan[d]),sorted(fan[d]))
print('annotation rank',rank.index('annotation')+1,len(fan['annotation']),'constraints rank',rank.index('constraints')+1,len(fan['constraints']))
ent=[d for d in D if dom[d]['life']]; med=statistics.median(len(fan[d]) for d in ent)
print('entity (life) domains',ent,'median fan-out',med)
