# Error exposure by reachability: raise-site function -> callers (by name, up to 3 hops within the domain) -> facade groups / workers.
import re,glob,os,sys,collections
SRC=os.path.expanduser('~/git/misc/juju-v2-preview')
def nt(fs): return [f for f in fs if not f.endswith('_test.go') and 'mock' not in f and '/testing/' not in f]
fac={f:open(f).read() for f in nt(glob.glob(SRC+'/apiserver/facades/**/*.go',recursive=True))}
wkr={f:open(f).read() for f in nt(glob.glob(SRC+'/internal/worker/**/*.go',recursive=True))}
def funcs(txt):
    # list of (name,start,end)
    ms=list(re.finditer(r'^func (?:\([^)]*\) )?([A-Za-z_]\w*)\(',txt,flags=re.M))
    return [(m.group(1),m.start(),(ms[i+1].start() if i+1<len(ms) else len(txt))) for i,m in enumerate(ms)]
def run(dom,page):
    doc=open(os.path.expanduser(page)).read()
    dfiles={f:open(f).read() for f in nt(glob.glob(f'{SRC}/domain/{dom}/**/*.go',recursive=True)) if '/errors/' not in f}
    consts=[]
    for f in nt(glob.glob(f'{SRC}/domain/{dom}/errors/*.go')+glob.glob(f'{SRC}/domain/{dom}/errors.go')):
        for m in re.finditer(r'^\s*([A-Z]\w*)\s*=\s*\w*\.?ConstError\("([^"]*)"\)',open(f).read(),flags=re.M): consts.append((m.group(1),m.group(2)))
    # index: function name -> body text across domain files
    bodies=collections.defaultdict(list)
    for f,t in dfiles.items():
        for n,s,e in funcs(t): bodies[n].append(t[s:e])
    def callers(name):
        out=set()
        for n,bs in bodies.items():
            if n==name: continue
            if any(re.search(r'\b'+re.escape(name)+r'\(',b) or re.search(r'\.'+re.escape(name)+r'\b',b) for b in bs): out.add(n)
        return out
    rows=[]
    for name,msg in consts:
        raise_fns=set()
        for f,t in dfiles.items():
            for n,s,e in funcs(t):
                if re.search(r'\.'+name+r'\b',t[s:e]): raise_fns.add(n)
        frontier=set(raise_fns); seen=set(raise_fns)
        for _ in range(3):
            nxt=set()
            for n in frontier: nxt|=callers(n)-seen
            seen|=nxt; frontier=nxt
        groups=set(); wk=set()
        for n in seen:
            if len(n)<6: continue
            for f,t in fac.items():
                if re.search(r'\b'+re.escape(n)+r'\b',t): groups.add(f.split('/facades/')[1].split('/')[0])
            for f,t in wkr.items():
                if re.search(r'\b'+re.escape(n)+r'\b',t): wk.add(f.split('/internal/worker/')[1].split('/')[0])
        tier='T1' if 'client' in groups else 'T2' if groups else 'T3' if wk else 'T0'
        documented= msg in doc or (len(msg.split('%')[0].strip())>8 and msg.split('%')[0].strip() in doc)
        rows.append((name,msg,tier,documented,bool(raise_fns)))
    c=collections.Counter((r[2],r[3]) for r in rows)
    print('==',dom,len(rows),'(tier, documented):',dict(sorted(c.items())))
    for r in rows:
        if not r[3] and r[2] in ('T1','T2'): print('   UNDOCUMENTED',r[2],r[0],'|',r[1])
    for r in rows:
        if r[3] and r[2] in ('T0',): print('   documented but unreachable',r[0],'|',r[1],'| raised:',r[4])
for dom,page in [('machine','~/git/misc/juju-v2-preview/docs/reference/machine.md'),('model','~/git/misc/juju-v2-preview/docs/reference/model.md'),('controllernode','~/git/misc/juju-v2-preview/docs/reference/controller.md'),('access','~/git/misc/juju-v2-preview/docs/reference/access.md'),('relation','~/git/misc/juju-entity-ref/docs/reference/relation.md')]: run(dom,page)
