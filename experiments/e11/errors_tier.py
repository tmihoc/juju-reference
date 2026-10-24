# Error constants of a domain: exposure tier (which facade group's code names the constant) and whether the pilot page documents the message.
import re,glob,os,sys,collections
SRC=os.path.expanduser('~/git/misc/juju-v2-preview')
def nt(fs): return [f for f in fs if not f.endswith('_test.go') and 'mock' not in f]
facs={f:open(f).read() for f in nt(glob.glob(SRC+'/apiserver/**/*.go',recursive=True))}
dom_files={f:open(f).read() for f in nt(glob.glob(SRC+'/domain/**/*.go',recursive=True)+glob.glob(SRC+'/internal/**/*.go',recursive=True))}
def tier_of(path):
    p=path.split('/apiserver/')[1]
    if p.startswith('facades/client/'): return 'T1'
    if p.startswith(('facades/agent/','facades/controller/')): return 'T2'
    return 'T2'  # other apiserver code (common mapping, auth) serves every caller
def run(dom,page):
    doc=open(os.path.expanduser(page)).read()
    consts=[]
    for f in nt(glob.glob(f'{SRC}/domain/{dom}/errors/*.go')+glob.glob(f'{SRC}/domain/{dom}/errors.go')):
        for m in re.finditer(r'^\s*([A-Z]\w*)\s*=\s*\w*\.?ConstError\("([^"]*)"\)',open(f).read(),flags=re.M): consts.append((m.group(1),m.group(2)))
    imp=f'domain/{dom}/errors"'
    rows=[]
    for name,msg in consts:
        tiers=set(); raised_in_domain=False
        for f,t in facs.items():
            if imp in t and re.search(r'\.'+name+r'\b',t): tiers.add(tier_of(f))
        for f,t in dom_files.items():
            if f'/domain/{dom}/' in f and re.search(r'\.'+name+r'\b',t): raised_in_domain=True
        tier='T1' if 'T1' in tiers else 'T2' if tiers else ('T3' if raised_in_domain else 'T0')
        rows.append((name,msg,tier,msg in doc or msg.split('%')[0].strip() in doc and len(msg.split('%')[0].strip())>8))
    c=collections.Counter((r[2],r[3]) for r in rows)
    print('==',dom,len(rows),'constants; (tier, documented):',dict(sorted(c.items())))
    for r in rows:
        if not r[3] and r[2] in ('T1','T2'): print('   UNDOCUMENTED',r[2],r[0],'|',r[1])
    for r in rows:
        if r[3] and r[2] in ('T3','T0'): print('   documented but internal/unused',r[2],r[0],'|',r[1])
for dom,page in [('machine','~/git/misc/juju-v2-preview/docs/reference/machine.md'),('model','~/git/misc/juju-v2-preview/docs/reference/model.md'),('controllernode','~/git/misc/juju-v2-preview/docs/reference/controller.md'),('access','~/git/misc/juju-v2-preview/docs/reference/access.md'),('relation','~/git/misc/juju-entity-ref/docs/reference/relation.md')]: run(dom,page)
