import re,glob,os,json,collections
SRC=os.path.expanduser('~/git/misc/juju-v2-preview')
doms=sorted(d for d in os.listdir(SRC+'/domain') if os.path.isdir(f'{SRC}/domain/{d}'))
def read(f): return open(f).read()
nontest=lambda fs:[f for f in fs if not f.endswith('_test.go') and 'mock' not in f]
VERB=[('create',r'^(Add|Create|Register|Import|Insert)'),('change',r'^(Set|Update|Change|Rename|Replace|Merge|Mark|Ensure|Record|Reset|Claim|Grant|Revoke|Refresh|Enable|Disable|Move|Attach|Detach|Pin|Unpin)'),
      ('remove',r'^(Remove|Delete|Destroy|Prune|Drop|Cancel)'),('read',r'^(Get|List|Is|Has|Find|Lookup|Exists|Count|Show|Resolve|Search|All|Check|Allowed|Can)'),('watch',r'^Watch')]
rows={}
for d in doms:
    base=f'{SRC}/domain/{d}'
    svc=nontest(glob.glob(base+'/service/**/*.go',recursive=True))
    st=nontest(glob.glob(base+'/state/**/*.go',recursive=True))
    meth=collections.Counter(); watch=0; names=set()
    for f in svc:
        for m in re.finditer(r'^func \((?:\w+ )?\*?(\w*Service)\) ([A-Z]\w*)\(',read(f),flags=re.M):
            n=m.group(2); names.add(n)
            for k,p in VERB:
                if re.match(p,n): meth[k]+=1; break
            else: meth['other']+=1
    errs=0
    for f in nontest(glob.glob(base+'/errors/*.go')+glob.glob(base+'/errors.go')):
        errs+=len(re.findall(r'errors\.ConstError|internalerrors\.ConstError|ConstError\(',read(f)))
    mm=os.path.isdir(base+'/modelmigration')
    # facades & workers importing the domain
    imp=f'"github.com/juju/juju/domain/{d}'
    fac=collections.Counter(); wk=set()
    for f in nontest(glob.glob(SRC+'/apiserver/facades/**/*.go',recursive=True)):
        if imp in read(f): fac[f.split('/facades/')[1].split('/')[0]]+=1
    for f in nontest(glob.glob(SRC+'/internal/worker/**/*.go',recursive=True)):
        if imp in read(f): wk.add(f.split('/internal/worker/')[1].split('/')[0])
    rows[d]=dict(svc_methods=sum(meth.values()),**{k:meth[k] for k in ['create','change','remove','read','watch','other']},errors=errs,migration=mm,
                 facades=sum(fac.values()),facade_kinds=dict(fac),workers=len(wk),worker_names=sorted(wk)[:6],has_state=bool(st),doc_go=os.path.exists(base+'/doc.go'))
json.dump(rows,open('artifacts.json','w'),indent=1)
print('%-22s %4s %4s %4s %4s %4s %4s %4s %5s %4s %4s %4s'%('domain','svc','crt','chg','rm','read','wtch','err','migr','fac','wkrs','doc'))
for d,r in sorted(rows.items(),key=lambda x:-x[1]['svc_methods']):
    if r['svc_methods']==0 and r['errors']==0: continue
    print('%-22s %4d %4d %4d %4d %4d %4d %4d %5s %4d %4d %4s'%(d,r['svc_methods'],r['create'],r['change'],r['remove'],r['read'],r['watch'],r['errors'],'Y' if r['migration'] else '',r['facades'],r['workers'],'Y' if r['doc_go'] else ''))
