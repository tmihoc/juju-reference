# For each Watch* method of a domain's WatchableService: which facade groups expose it, which workers consume it.
import re,glob,os,collections,json,sys
SRC=os.path.expanduser('~/git/misc/juju-v2-preview')
def nt(fs): return [f for f in fs if not f.endswith('_test.go') and 'mock' not in f]
fac=nt(glob.glob(SRC+'/apiserver/facades/**/*.go',recursive=True)); wk=nt(glob.glob(SRC+'/internal/worker/**/*.go',recursive=True))
facT={f:open(f).read() for f in fac}; wkT={f:open(f).read() for f in wk}
out={}
for d in sys.argv[1:]:
    ms=[]
    for f in nt(glob.glob(f'{SRC}/domain/{d}/service/**/*.go',recursive=True)):
        ms+=re.findall(r'^func \(\w+ \*?\w*Service\) (Watch\w*)\(',open(f).read(),flags=re.M)
    res={}
    for m in sorted(set(ms)):
        g=collections.Counter(); w=set()
        for f,t in facT.items():
            if re.search(r'\b'+m+r'\b',t): g[f.split('/facades/')[1].split('/')[0]+'/'+f.split('/facades/')[1].split('/')[1]]+=1
        for f,t in wkT.items():
            if re.search(r'\b'+m+r'\b',t): w.add(f.split('/internal/worker/')[1].split('/')[0])
        res[m]=dict(facades=sorted(g),workers=sorted(w))
    out[d]=res
    print('==',d)
    for m,r in res.items(): print('  %-38s facades=%s workers=%s'%(m,r['facades'],r['workers']))
json.dump(out,open('observe.json','w'),indent=1)
