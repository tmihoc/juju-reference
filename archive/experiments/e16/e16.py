# E16: entity-scoped artifact index against held-out pages (criteria in the plan).
import re,os,json,glob,subprocess,collections
SRC=os.path.expanduser('~/git/misc/juju-v2-preview'); HERE=os.path.dirname(os.path.abspath(__file__))
A=json.load(open(HERE+'/anchors.json'))
def ok(f): return f.endswith(('.go','.sql')) and not f.endswith('_test.go') and '/testing/' not in f and '/docs/' not in f and 'mock' not in os.path.basename(f)
ALL=[f for f in glob.glob(SRC+'/**/*',recursive=True) if os.path.isfile(f) and ok(f)]
TXT={f:open(f,errors='ignore').read() for f in ALL}
def files_for(a):
    fs=set()
    for t in a['schema']:
        fs|={f for f in ALL if f.endswith('.sql') and '/domain/schema/' in f and t in os.path.basename(f)}
        fs|={f for f in ALL if '/domain/schema/' in f and '/triggers/' in f and t in os.path.basename(f)}
    for d in a['domain']: fs|={f for f in ALL if f'/domain/{d}/' in f}
    for c in a['core']: fs|={f for f in ALL if f'/core/{c}/' in f}
    for x in a['facade']: fs|={f for f in ALL if f'/apiserver/facades/client/{x}/' in f}
    for x in a['cmd']: fs|={f for f in ALL if f'/cmd/juju/{x}/' in f}
    return fs
SCOPE={e:files_for(a) for e,a in A.items()}
SCOPETXT={e:'\n'.join(TXT[f] for f in fs) for e,fs in SCOPE.items()}
BIG='\n'.join(TXT.values())
def atoms(md):
    out=[]
    for span in re.findall(r'`([^`\n]+)`',md):
        for a in re.split(r'[\s,;()\[\]{}=]+',span):
            a=a.strip('\'".:!?')
            if not a or a=='juju' or '<' in a or '>' in a: continue
            if re.match(r'^--?[A-Za-z][\w-]*$',a) or (re.match(r'^[A-Za-z_][\w./-]{2,}$',a) and (re.search(r'[_./-]',a) or re.search(r'[a-z][A-Z]',a))):
                out.append(a)
    return sorted(set(out))
def found(a,txt): return re.search(r'(?<![\w-])'+re.escape(a)+r'(?![\w-])',txt) is not None
def where(a):
    c=collections.Counter()
    for f,t in TXT.items():
        if found(a,t): 
            rel=f[len(SRC)+1:]; c[rel.split('/')[0] if rel.split('/')[0] not in ('internal','domain','apiserver','cmd','core') else '/'.join(rel.split('/')[:2])]+=1
    return c
def run():
    pages={e:subprocess.run(['git','-C',SRC,'show',f'upstream/4.1:docs/reference/{e}.md'],capture_output=True,text=True).stdout for e in A}
    R={};resid=collections.Counter();tot=0;own=0;cross=[]
    for e,md in pages.items():
        at=atoms(md); incode=[a for a in at if found(a,BIG)]
        ins=[a for a in incode if found(a,SCOPETXT[e])]
        others={o:sum(1 for a in incode if found(a,SCOPETXT[o]))/max(1,len(incode)) for o in A if o!=e}
        out=[a for a in incode if a not in ins]
        R[e]=dict(atoms=len(at),in_code=len(incode),in_scope=len(ins),scope_files=len(SCOPE[e]),cross_mean=sum(others.values())/len(others),
                  not_in_code=[a for a in at if a not in incode],out_of_scope=out,in_scope_atoms=ins)
        tot+=len(incode);own+=len(ins);cross.append((sum(others.values())/len(others))*len(incode))
        for a in out:
            for k in where(a): resid[k]+=1
    R['_total']=dict(in_code=tot,in_scope=own,own_frac=own/max(1,tot),cross_frac=sum(cross)/max(1,tot),residue_dirs=resid.most_common(12))
    return R
if __name__=='__main__':
    R=run(); json.dump(R,open(HERE+'/e16_result.json','w'),indent=1)
    for e,v in R.items():
        if e=='_total': print(v)
        else: print(e,{k:v[k] for k in ('atoms','in_code','in_scope','scope_files')},'cross %.2f'%v['cross_mean'],'out:',v['out_of_scope'])
