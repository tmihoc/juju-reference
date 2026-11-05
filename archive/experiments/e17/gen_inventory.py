# Per-domain part inventory generated from the 4.1 code (E19 definitions; see skeleton-v5.md).
# usage: python3 gen_inventory.py <domain> [<domain> ...]
import sys,re,glob,os,json,io,contextlib,collections
with contextlib.redirect_stdout(io.StringIO()):
    import e17
dom,V,e15,SRC=e17.dom,e17.V,e17.e15,e17.SRC
def nt(fs): return [f for f in fs if not f.endswith('_test.go') and 'mock' not in f]
FAC=nt(glob.glob(SRC+'/apiserver/facades/**/*.go',recursive=True)); WK=nt(glob.glob(SRC+'/internal/worker/**/*.go',recursive=True))
FT={f:open(f).read() for f in FAC}; WT={f:open(f).read() for f in WK}
LEG=open(SRC+'/internal/migration/legacy/importoperations.go').read()
EXPORT=open(SRC+'/domain/export/state/model/export.go').read()
KINDS=json.load(open(os.path.dirname(os.path.abspath(__file__))+'/e24.json'))
REM=e17.TP['removal_types']
def run(d):
    r=dom[d]; out=[f'## {d}','']
    scopes=sorted({t.split(':')[0] for t in r['tabs']})
    lifes=sorted({s for s in scopes if any(t.startswith(s+':') and e15.typing(V[s],t.split(':')[1])['life'] for t in r['tabs'])})
    out.append(f"**Identity.** Scope: {', '.join(scopes) or 'none'} database. Life column: {', '.join(lifes) or 'none'}. Lifecycle kinds: {', '.join(KINDS.get(d,[])) or 'n/a'}. Removal job types: {', '.join(k for k,v in REM.items() if v==d) or 'none'}.")
    out.append('\n**State.**')
    for t in sorted(r['tabs']):
        sc,tb=t.split(':'); ty=e15.typing(V[sc],tb)
        fl=[k for k in ('life','status','immutable') if ty[k]]+(['watched'] if ty['watched'] else [])+(['lookup'] if ty['lookup'] else [])
        line=f"- `{tb}` ({sc}) {' '.join(fl)}"
        if ty['lookup']:
            vals=[re.findall(r"'([^']*)'",x)[:1] for x in V[sc]['seeds'][tb]]; line+=': '+', '.join(sorted(v[0] for v in vals if v))
        out.append(line)
    owned={t.split(':')[1] for t in r['tabs']}
    views=sorted(v for sc in scopes for v,sql in V[sc]['views'].items() if any(re.search(r'\b'+re.escape(t)+r'\b',sql) for t in owned))
    out.append(f"- views touching these tables: {', '.join(views) or 'none'}")
    base=f'{SRC}/domain/{d}'
    # observation with tiers
    ms=sorted({m for f in nt(glob.glob(base+'/service/**/*.go',recursive=True)) for m in re.findall(r'^func \([^)]*\) (Watch\w+)\(',open(f).read(),flags=re.M)})
    out.append('\n**Observation (Watch methods and who uses them).**')
    for m in ms:
        cl=sorted({f.split('/facades/')[1].split('/')[0]+'/'+f.split('/facades/')[1].split('/')[1] for f,t in FT.items() if re.search(r'\b'+m+r'\b',t)})
        wk=sorted({f.split('/internal/worker/')[1].split('/')[0] for f,t in WT.items() if re.search(r'\b'+m+r'\b',t)})
        tier='T1' if any(c.startswith('client') for c in cl) else 'T2' if cl else 'T3' if wk else 'T0'
        out.append(f"- {m}: {tier}; facades {cl or '-'}; workers {wk[:4] or '-'}")
    if not ms: out.append('- none')
    # dynamics
    mut=sorted({m for f in nt(glob.glob(base+'/service/**/*.go',recursive=True)) for m in re.findall(r'^func \([^)]*\) ((?:Add|Create|Register|Import|Set|Update|Change|Remove|Delete|Unset|Mark|Ensure|Record|Reset|Grant|Revoke|Enable|Disable|Move|Attach|Detach|Rename|Replace|Merge)\w*)\(',open(f).read(),flags=re.M)})
    out.append(f"\n**Dynamics (service mutators).** {', '.join(mut) or 'none in this domain (a writer may be another domain)'}")
    # interface
    fk=collections.Counter()
    for f,t in FT.items():
        if f'"github.com/juju/juju/domain/{d}' in t: fk[f.split('/facades/')[1].split('/')[0]+'/'+f.split('/facades/')[1].split('/')[1]]+=1
    out.append(f"\n**Interface (facades importing the domain).** {', '.join(sorted(fk)) or 'none by import'}")
    # failure
    errs=[]
    for f in nt(glob.glob(base+'/errors/*.go')+glob.glob(base+'/errors.go')):
        errs+=re.findall(r'(\w+)\s*=\s*(?:\w+\.)?ConstError\("([^"]+)"\)',open(f).read())
    out.append(f"\n**Failure.** {len(errs)} error constants: "+'; '.join(f'`{m}`' for _,m in errs[:12])+(' ...' if len(errs)>12 else ''))
    # agent
    wk=sorted({f.split('/internal/worker/')[1].split('/')[0] for f,t in WT.items() if f'"github.com/juju/juju/domain/{d}' in t})
    out.append(f"\n**Agent (workers importing the domain).** {', '.join(wk) or 'none'}")
    # migration
    leg=bool(re.search(r'\b'+d+r'\.Register\w*Import',LEG)); pkg=os.path.isdir(base+'/modelmigration')
    gen=sorted(t for t in owned if f'FROM "{t}"' in EXPORT)
    out.append(f"\n**Migration.** modelmigration package: {pkg}; legacy import registered: {leg}; owned tables read by the generic export: {len(gen)} of {len(owned)}.")
    return '\n'.join(out)+'\n'
if __name__=='__main__':
    for d in sys.argv[1:]: print(run(d))
