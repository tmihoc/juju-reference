import re,glob,os,json,io,contextlib,collections
with contextlib.redirect_stdout(io.StringIO()):
    import e17
dom,D,SRC=e17.dom,e17.D,e17.SRC
def nontest(fs): return [f for f in fs if not f.endswith('_test.go') and 'mock' not in f]
res={}
for d in D:
    base=f'{SRC}/domain/{d}'
    code=nontest(glob.glob(base+'/**/*.go',recursive=True))
    txt='\n'.join(open(f).read() for f in code)
    owned={t.split(':')[1] for t in dom[d]['tabs']}
    dels=[t for t in owned if re.search(r'DELETE\s+FROM\s+"?'+re.escape(t)+r'\b',txt)]
    svc=re.findall(r'^func \([^)]*\) (Remove\w*|Delete\w*|Unset\w*)\(',txt,flags=re.M)
    c=set()
    if dom[d]['life']: c.add('life-column')
    if (dels or svc) and not dom[d]['life']: c.add('deletable')
    if re.search(r'\b\w*(Prune|Expire|TTL|Purge|Cleanup|Reap)\w*',txt): c.add('pruned')
    if not dom[d]['life'] and not dels and not svc: c.add('append-only')
    res[d]=sorted(c)
cnt=collections.Counter(x for c in res.values() for x in c)
print(dict(cnt)); print('none:',[d for d,c in res.items() if not c])
for k in ('life-column','deletable','pruned','append-only'): print(k,[d for d,c in res.items() if k in c])
json.dump(res,open('e24.json','w'),indent=1)
