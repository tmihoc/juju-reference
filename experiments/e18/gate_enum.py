import sys,re,subprocess,json,collections
sys.path.insert(0,'../e15'); sys.path.insert(0,'../e16')
import e15
SRC=e15.NEW
lk={}
for scope in ('model','controller'):
    V=e15.parse(SRC[scope])
    for t in V['tables']:
        if e15.typing(V,t)['lookup']:
            vals=set()
            for row in V['seeds'][t]:
                m=re.findall(r"'([^']*)'",row)
                vals|=set(m[:1]) if m else set()
            if len(vals)>=3: lk[scope+':'+t]=vals
WT='/home/dora/git/misc/juju-v2-preview'
files=subprocess.run(['git','-C',WT,'ls-tree','--name-only','upstream/4.1','docs/reference/'],capture_output=True,text=True).stdout.split()
out=[]
for f in files:
    if not f.endswith('.md'): continue
    md=subprocess.run(['git','-C',WT,'show',f'upstream/4.1:{f}'],capture_output=True,text=True).stdout
    md=re.sub(r'\{[a-z:]+\}`[^`\n]*`','',md); md=re.sub(r'```.*?```','',md,flags=re.S)
    for sent in re.split(r'(?<=[.!?])\s+|\n',md):
        toks=set(re.findall(r'`([^`]+)`',sent))|set(re.findall(r'\*\*([^*]+)\*\*',sent))
        for t,vals in lk.items():
            hit=toks&vals
            if len(hit)>=3: out.append(dict(page=f.split('/')[-1],lookup=t,hit=sorted(hit),missing=sorted(vals-hit),extra=sorted(x for x in toks-vals if re.match(r'^[a-z][a-z -]+$',x))[:8],sentence=sent.strip()[:260]))
json.dump(out,open('gate_enum.json','w'),indent=1)
print(len(lk),'lookups with >=3 values;',len(out),'candidate enumerations')
for o in out: print(o['page'],o['lookup'],'| hit',o['hit'],'| missing',o['missing'][:6],'| extra',o['extra'][:5],'\n   ',o['sentence'][:200])
