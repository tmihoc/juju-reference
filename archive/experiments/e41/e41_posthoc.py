"""E41 post hoc variant (labelled): a table of G's own page that references G's
lead table and ALSO references a table of another page is an association of G
with that page, so G has a dependent. Computed after seeing the E41 result."""
import os, sys, json, collections
HERE=os.path.dirname(os.path.abspath(__file__))
sys.argv=['x']
import importlib.util
spec=importlib.util.spec_from_file_location('e41',os.path.join(HERE,'e41.py')); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
e15=m.e15; chunk=m.chunk
dbs=m.build(e15.NEW)
R=m.classify(e15.NEW)
V={s:e15.parse(e15.NEW[s]) for s in ('model','controller')}
lookup={t for s in V for t in V[s]['tables'] if e15.typing(V[s],t)['lookup']}-{'space'}
assoc=collections.defaultdict(set)
for t,c in chunk.items():
    if t in lookup: continue
    rows=m.fk_rows(dbs,t)
    pars=[(par,chunk.get(par)) for _,par,_,_ in rows if par not in lookup and chunk.get(par)]
    for par,pc in pars:
        if pc==c and par==R[c]['lead']:
            others={q for _,q in pars if q!=c}
            if others and t!=R[c]['lead']: assoc[c].add((t,tuple(sorted(others))))
print('sections by E41:',[g for g,r in R.items() if r['level'].startswith('section')])
print()
for g,r in sorted(R.items()):
    if r['level'].startswith('section'):
        a=sorted(assoc[g])
        print('%-20s association dependents: %s  -> %s'%(g,a[:3],'PAGE (post hoc)' if a else 'section'))
