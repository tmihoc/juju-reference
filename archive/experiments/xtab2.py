import re,subprocess,glob,collections,shlex
def sh(c): return subprocess.run(c,shell=True,capture_output=True,text=True).stdout
# constants: message -> const name
consts={}
for l in sh("git grep -n --no-color -E 'ConstError\\(\"' -- '*.go' ':!*_test.go'").splitlines():
    m=re.search(r'^(\S+?):\d+:\s*(\w+)\s*=\s*\w*\.?ConstError\("([^"]*)"\)',l)
    if m: consts.setdefault(m.group(3),[]).append((m.group(1),m.group(2)))
def cat(path):
    if path.startswith('apiserver/'): return 'facade'
    if '/state/' in path or 'schema' in path: return 'state'
    if '/service/' in path: return 'service'
    if path.startswith('internal/worker') or path.startswith('cmd/jujuagentd') or '/worker/' in path: return 'worker'
    return 'other'
rows=[]
for f in sorted(glob.glob('docs/reference/*.md')):
    sect=None
    for line in open(f):
        h=re.match(r'## (.*)',line)
        if h:
            t=h.group(1).lower()
            sect='D' if 'declaration' in t else 'P' if 'persistence' in t else 'E' if 'execution' in t else None
        m=re.match(r'\s*[-*] \*\*`([^`]+)`\*\*|\s+\* - `([^`]+)`',line)
        for msg in re.findall(r'\*\*`([^`]+)`\*\*',line):
            if sect: rows.append((f.split('/')[-1],sect,msg))
res=collections.Counter(); unres=0; tot=0
detail=[]
seen=set()
for page,sect,msg in rows:
    if (page,sect,msg) in seen: continue
    seen.add((page,sect,msg)); tot+=1
    if msg not in consts: unres+=1; continue
    cats=set()
    for path,name in consts[msg]:
        out=sh(f"git grep -n --no-color -w {shlex.quote(name)} -- '*.go' ':!*_test.go' ':!*/mocks/*'")
        for l in out.splitlines():
            p=l.split(':')[0]
            if p==path and re.search(rf'{name}\s*=\s*',l): continue
            if p.endswith('errors.go') or '/errors/' in p: continue
            code=l.split(':',2)[2]
            if re.search(r'\bIs\(|\bAs\(|case |ErrorIs|Cause\(|params\.|Code',code): continue
            cats.add(cat(p))
    key=tuple(sorted(cats)) or ('none',)
    res[(sect,key)]+=1
    detail.append((page,sect,msg,key))
print('errors listed:',tot,' resolved to constants:',tot-unres,' unresolved (composed/templated/other):',unres)
by=collections.defaultdict(collections.Counter)
for (sect,key),n in res.items():
    for k in key: by[sect][k]+=n
for s in 'DPE':
    print(s,'filed:',sum(n for (ss,k),n in res.items() if ss==s),dict(by[s]))
print()
multi=collections.Counter()
for (sect,key),n in sorted(res.items()): print(sect,key,n)
