# H3: census of exported declarations in the entity/mechanism domain packages, by Go kind and file role.
import re,glob,os,json,collections
SRC=os.path.expanduser('~/git/misc/juju-v2-preview')
doms=sorted(d for d in os.listdir(SRC+'/domain') if os.path.isdir(f'{SRC}/domain/{d}') and d not in ('testing','schema'))
def role(path):
    p=path.split('/domain/')[1]
    if '/errors' in p or p.endswith('/errors.go'): return 'errors'
    if '/modelmigration/' in p: return 'migration'
    if '/state/' in p: return 'state-layer'
    if '/service/' in p: return 'service'
    if '/watcher' in p or p.endswith('watcher.go'): return 'watcher'
    if '/internal/' in p: return 'internal'
    return 'package-root'
rows=[]
for d in doms:
    for f in glob.glob(f'{SRC}/domain/{d}/**/*.go',recursive=True):
        if f.endswith('_test.go') or 'mock' in f: continue
        r=role(f); txt=open(f).read()
        for m in re.finditer(r'^type ([A-Z]\w*) (struct|interface|\w[\w.\[\]]*)',txt,flags=re.M):
            kind='struct' if m.group(2)=='struct' else 'interface' if m.group(2)=='interface' else 'named-'+('func' if m.group(2).startswith('func') else 'basic')
            rows.append((d,r,'type-'+kind,m.group(1)))
        for m in re.finditer(r'^func ([A-Z]\w*)\(',txt,flags=re.M): rows.append((d,r,'func',m.group(1)))
        for m in re.finditer(r'^\s+([A-Z]\w*)\s+(?:\w+\s+)?=\s',txt,flags=re.M): rows.append((d,r,'const/var',m.group(1)))
print(len(rows),'exported declarations in',len(doms),'domains')
c=collections.Counter((r,k) for _,r,k,_ in rows)
for (r,k),n in sorted(c.items(),key=lambda x:-x[1])[:30]: print('%-14s %-18s %5d'%(r,k,n))
json.dump(rows,open('census.json','w'))
