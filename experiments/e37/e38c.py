import sys,re,os,json,sqlite3,collections
sys.path.insert(0,'../e15')
import e15
man=json.load(open('../e33/page-manifest.json')); home={t:p for p,d in man['pages'].items() for t in d['tables']}
dbs={}
for s in ('model','controller'):
    db=sqlite3.connect(':memory:')
    for st in e15.split(open(e15.NEW[s]).read()): db.executescript(st.rstrip().rstrip(';')+';')
    dbs[s]=db
def info(t):
    for s,db in dbs.items():
        rows=db.execute(f'PRAGMA table_info("{t}")').fetchall()
        if rows:
            pk={r[1] for r in rows if r[5]>0}
            fks=[(r[3],r[2]) for r in db.execute(f'PRAGMA foreign_key_list("{t}")').fetchall()]
            return pk,fks
    return set(),[]
weak={}; strong=[]
for t in home:
    pk,fks=info(t)
    ident=[(c,p) for c,p in fks if c in pk and p in home]
    if ident: weak[t]=sorted({home[p] for c,p in ident})
    else: strong.append(t)
same=[t for t,o in weak.items() if home[t] in o]; cross=[t for t,o in weak.items() if home[t] not in o]
print('tables',len(home),'weak',len(weak),'strong',len(strong))
print('(1) weak tables homed with their owner: %d / %d = %.0f%%'%(len(same),len(weak),100*len(same)/len(weak)))
print('cross-page weak tables (candidate misplacements):')
for t in sorted(cross,key=lambda t:(home[t],t)): print(f'   {t:44s} homed on {home[t]:18s} owner page(s): {weak[t]}')
ann=[t for t in home if t.startswith('annotation_')]; print('(2) annotation tables cross-page:',sum(1 for t in ann if t in cross),'/',len(ann),'| cloud_defaults, cloud_region_defaults cross-page:',[t in cross for t in ('cloud_defaults','cloud_region_defaults')])
audit=['bakery_config','macaroon_root_key','flag','block_device','block_device_link_device','application_storage_directive','unit_storage_directive','model_database_deletion']
print('(3) tables the E34 audit moved that the principle flags:',[t for t in audit if t in cross])
print('(4) strong?:',[(t,t in strong) for t in ('permission','resource','port_range','secret','user_public_ssh_key')])
json.dump(dict(weak=weak,cross=cross,strong=strong),open('e38c_result.json','w'),indent=1)
