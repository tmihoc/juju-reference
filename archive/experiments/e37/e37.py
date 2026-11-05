import sys,re,os,json,sqlite3,collections
sys.path.insert(0,'../e15'); sys.path.insert(0,'../e33')
import e15
SRC=os.path.expanduser('~/git/misc/juju-v2-preview')
man=json.load(open('../e33/page-manifest.json')); home={t:p for p,d in man['pages'].items() for t in d['tables']}
J={x['name']:x for x in json.load(open('../e33/e35_judge_out.json'))}
V={s:e15.parse(e15.NEW[s]) for s in ('model','controller')}
dbs={}
for s in V:
    db=sqlite3.connect(':memory:')
    for st in e15.split(open(e15.NEW[s]).read()): db.executescript(st.rstrip().rstrip(';')+';')
    dbs[s]=db
def pk(t):
    for s,db in dbs.items():
        rows=db.execute(f'PRAGMA table_info("{t}")').fetchall()
        if rows: return [r[1] for r in sorted(rows,key=lambda r:r[5]) if r[5]>0]
    return []
def fkl(t):
    out=[]
    for s,db in dbs.items():
        for r in db.execute(f'PRAGMA foreign_key_list("{t}")').fetchall(): out.append((r[3],r[2]))
    return out
life={t for s in V for t in V[s]['tables'] if e15.typing(V[s],t)['life']}
lookup={t for s in V for t in V[s]['tables'] if e15.typing(V[s],t)['lookup']}-{'space'}
R=[r for r in json.load(open('e37_roots.json')) if r['kind'] in ('facade','http','hook')]
for r in R:
    for k in ('ins','del','upd'): r[k]=set(r[k] or [])
RT=set(re.findall(r"'([^']+)'",' '.join(re.findall(r"\(\d+, '([^']+)'\)",open(SRC+'/domain/schema/model/sql/0028-cleanup.sql').read()))))
RT=set(re.findall(r"\(\d+, '([^']+)'\)",open(SRC+'/domain/schema/model/sql/0028-cleanup.sql').read()))
REMALIAS={'storage':['storage'],'offer':['remote application offerer','relation with remote'],'model':['model','controller-model'],'secret':['secret'],'unit':['unit'],'application':['application'],'machine':['machine'],'relation':['relation'],'resource':['resource']}
def lifeanc(G):
    seen=set(); out=set(); stack=[p for t in G for c,p in fkl(t)]
    while stack:
        p=stack.pop()
        if p in seen or p in G or p in lookup: continue
        seen.add(p)
        if p in life: out.add(p)
        stack+=[q for c,q in fkl(p)]
    return out
def props(name,G):
    G=set(G); indeg=collections.Counter()
    for t in G:
        for c,p in fkl(t):
            if p in G and p!=t: indeg[p]+=1
    lead=e15.lead_table(name,G,indeg) if G else None
    pkc=pk(lead); fkc={c for c,p in fkl(lead)}
    I=bool(pkc) and not (set(pkc)&fkc)
    anc=lifeanc(G)
    C=[r for r in R if r['ins']&G and not (r['ins']&anc)]
    D=[r for r in R if r['del']&G and not (r['del']&anc)]
    jobs=[x for x in RT if any(a in x for a in REMALIAS.get(name,[name.replace('-',' ')]))]
    Rr=bool(D) or bool(jobs)
    W=[r for r in R if (r['ins']&G or r['del']&G) and (r['tier']=='client' or r['kind']=='hook')]
    return dict(lead=lead,pk=pkc,I=I,anc=sorted(anc),C=bool(C),C_n=len(C),R=Rr,R_roots=len(D),jobs=jobs,W=bool(W),W_n=len(W),prim=I and bool(C) and Rr,
                C_ex=[r['name'].split('.')[-1] for r in C[:3]],D_ex=[r['name'].split('.')[-1] for r in D[:3]])
groups={p:d['tables'] for p,d in man['pages'].items() if d['tables']}
groups['storage-pool']=['storage_pool','storage_pool_attribute']
ctrl={'cloud-instance':['machine_cloud_instance','machine_cloud_instance_status','instance_tag'],'unit-state':['unit_state','unit_state_charm','unit_state_relation'],
 'relation-unit':['relation_unit','relation_unit_departure','relation_unit_setting','relation_unit_setting_archive','relation_unit_settings_hash'],
 'application-endpoint':['application_endpoint','application_extra_endpoint'],'application-scale':['application_scale'],'machine-placement':['machine_placement']}
res={p:props(p,t) for p,t in groups.items()}
cres={p:props(p,t) for p,t in ctrl.items()}
json.dump(dict(groups=res,controls=cres),open('e37_result.json','w'),indent=1,default=list)
mark=lambda b:'Y' if b else '-'
print('%-22s I C R | W | prim | judge     | lead table (pk) | anc'%'group')
for p,r in sorted(res.items(),key=lambda x:(not x[1]['prim'],x[0])):
    print('%-22s %s %s %s | %s | %s | %-9s | %s %s | %s'%(p,mark(r['I']),mark(r['C']),mark(r['R']),mark(r['W']),'PRIM' if r['prim'] else '    ',J.get(p,{}).get('verdict','-'),r['lead'],r['pk'],r['anc'][:3]))
print('\nprimitives:',sum(1 for r in res.values() if r['prim']),'of',len(res))
print('\nPREDICTIONS')
pos=['machine','application','unit','relation','model','secret','offer','storage','resource']
print('(1) positive controls pass:',[(p,res[p]['prim']) for p in pos])
print('(2) negative controls fail:',[(p,not r['prim'],''.join(k for k in 'ICR' if not r[k])) for p,r in cres.items()],' ->',sum(1 for r in cres.values() if not r['prim']),'/ 6')
print('(3) permission, storage-pool pass:',[(p,res[p]['prim']) for p in ('permission','storage-pool')])
print('(4) annotation fails (I):',res['annotation']['I'])
