import re,glob,os,json,collections,io,contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import e17
dom,D,SRC=e17.dom,e17.D,e17.SRC
def nontest(fs): return [f for f in fs if not f.endswith('_test.go') and 'mock' not in f]
meth=collections.defaultdict(set)
for d in dom:
    for f in nontest(glob.glob(f'{SRC}/domain/{d}/service/**/*.go',recursive=True)):
        for m in re.finditer(r'^func \([^)]*\) ([A-Z]\w+)\(',open(f).read(),flags=re.M): meth[d].add(m.group(1))
cnt=collections.Counter(n for s in meth.values() for n in s)
uniq={d:{n for n in s if cnt[n]==1 and len(n)>6} for d,s in meth.items()}
def corpus(sub): return '\n'.join(open(f).read() for f in nontest(glob.glob(f'{SRC}/apiserver/facades/{sub}/**/*.go',recursive=True)))
T1=corpus('client'); T2=corpus('agent')+corpus('controller')
res={}
for d in D:
    t1=sorted(n for n in uniq.get(d,()) if re.search(r'\.'+n+r'\(',T1)); t2=sorted(n for n in uniq.get(d,()) if re.search(r'\.'+n+r'\(',T2))
    res[d]=(len(t1),len(t2),len(uniq.get(d,())))
P=json.load(open('pages.json')); paged=sorted(set(P.values())&set(D))
ex=lambda d:res[d][0]>0 or res[d][1]>0
print('paged exposed:',sum(ex(d) for d in paged),'/',len(paged),'unexposed paged:',[d for d in paged if not ex(d)])
old=['sequence','objectstore','lease','externalcontroller','controllerconfig','upgrade','autocert','flag']
print('formerly unexposed now exposed:',[(d,res[d]) for d in old if ex(d)])
print('still unexposed (all):',[(d,res[d][2]) for d in D if not ex(d)])
json.dump(res,open('e20c.json','w'),indent=1)
