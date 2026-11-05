import json,sys,io,contextlib,collections,re
sys.path.insert(0,'../e17')
with contextlib.redirect_stdout(io.StringIO()):
    import e17
dom=e17.dom
owner={}
for d,r in dom.items():
    for t in r['tabs']: owner[t.split(':')[1]]=d
R=json.load(open('e30_roots.json'))
VM=json.load(open('viewmap.json'))
for r in R:
    ts=set(r['tables'] or [])
    for t in list(ts):
        if t in VM: ts|=set(VM[t])
    r['tables']=sorted(ts)
print('roots by kind:',collections.Counter(r['kind'] for r in R),' with tier:',collections.Counter((r['kind'],r['tier']) for r in R if r['kind']=='facade'))
def reach(table):
    c=collections.Counter()
    for r in R:
        if table in (r['tables'] or []): c[(r['kind'],r['tier'])]+=1
    return c
print('--K1/K2')
for t in ['controller_config','agent_binary_store','object_store_metadata','object_store_backend','constraint','application_constraint','sequence','lease','autocert_cache']:
    c=reach(t); print(t,dict(c))
    ex=[ (r['kind'],r['pkg'],r['name'].split('.')[-1]) for r in R if t in (r['tables'] or [])][:4]
    print('   e.g.',ex)
# K3
A=json.load(open('../e11/artifacts.json'))
cl={}
for d in dom:
    cl[d]=set()
for r in R:
    if r['kind']=='facade' and r['tier']=='client':
        for t in r['tables'] or []:
            if t in owner: cl[owner[t]].add(r['pkg'])
imp={d for d in dom if A.get(d,{}).get('facade_kinds',{}).get('client',0)>0}
cg={d for d in dom if cl[d]}
print('--K3 import-measure client-exposed',len(imp),'call-graph client-exposed',len(cg),'import found also by graph',len(imp&cg),'/',len(imp),'; lost:',sorted(imp-cg),'; added:',sorted(cg-imp))
# K4
print('--K4 action CLI roots')
tabs=collections.Counter(); roots=[r for r in R if r['kind']=='cli' and r['pkg'].startswith('cmd/juju/action')]
for r in roots:
    for t in r['tables'] or []: tabs[t]+=1
print(len(roots),'roots; tables reached:',len(tabs)); print(sorted(tabs.items(),key=lambda x:-x[1])[:25])
