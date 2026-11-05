import sys,subprocess,re,json,os
sys.path.insert(0,'../e16')
import e16
files=subprocess.run(['git','-C',e16.SRC,'ls-tree','--name-only','upstream/4.1','docs/reference/'],capture_output=True,text=True).stdout.split()
def clean(md):
    md=re.sub(r'\{[a-z:]+\}`[^`\n]*`','',md); md=re.sub(r'```.*?```','',md,flags=re.S); return md
out=[]
for f in files:
    if not f.endswith('.md'): continue
    md=subprocess.run(['git','-C',e16.SRC,'show',f'upstream/4.1:{f}'],capture_output=True,text=True).stdout
    c=clean(md)
    for a in e16.atoms(c):
        if not e16.found(a,e16.BIG):
            sent=[s.strip() for s in re.split(r'(?<=[.!?])\s+|\n',c) if '`'+a in s or a+'`' in s or a in s][:1]
            out.append(dict(page=f.split('/')[-1],atom=a,sentence=(sent[0][:200] if sent else '')))
json.dump(out,open('gate_flags.json','w'),indent=1)
print(len(out))
for o in out: print(o['page'],'|',o['atom'],'|',o['sentence'][:110])
