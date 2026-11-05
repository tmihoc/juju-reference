import re,glob,os,collections
SRC=os.path.expanduser('~/git/misc/juju-v2-preview')
def body(txt,start):
    i=txt.index('{',start); d=0
    for j in range(i,len(txt)):
        if txt[j]=='{': d+=1
        elif txt[j]=='}':
            d-=1
            if d==0: return txt[i+1:j]
    return ''
tot=collections.Counter();dead=collections.defaultdict(list)
for f in glob.glob(SRC+'/apiserver/facades/**/*.go',recursive=True):
    if f.endswith('_test.go') or 'mock' in f or '/params' in f: continue
    kind=f.split('/facades/')[1].split('/')[0]
    t=open(f).read()
    for m in re.finditer(r'^func \((\w+) \*?(\w+)\) ([A-Z]\w*)\((?:ctx|_)\s+context\.Context',t,flags=re.M):
        b=body(t,m.start()); code=re.sub(r'//[^\n]*','',b)
        tot[kind]+=1
        if re.search(r'Not(Implemented|Supported)f?\(',code) and len(re.findall(r'\n',code.strip()))<=6 and not re.search(r'Service|service|\.st\.|state',code):
            dead[kind].append(f"{m.group(2)}.{m.group(3)}")
for k in tot: print(k,tot[k],'dead',len(dead[k]),'=%.0f%%'%(100*len(dead[k])/tot[k]))
print(sum(tot.values()),sum(len(v) for v in dead.values()))
