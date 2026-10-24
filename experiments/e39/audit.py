import sys,re,os,glob,json,sqlite3,collections
sys.path.insert(0,'../e15')
import e15
SRC=os.path.expanduser('~/git/misc/juju-v2-preview')
S=('model','controller')
V={s:e15.parse(e15.NEW[s]) for s in S}
dbs={}
for s in S:
    db=sqlite3.connect(':memory:')
    for st in e15.split(open(e15.NEW[s]).read()): db.executescript(st.rstrip().rstrip(';')+';')
    dbs[s]=db
out={}
# Z1 foreign-key parse
bad=[];n=0
for s in S:
    for t,b in V[s]['tables'].items():
        n+=1
        rx=set(re.findall(r'REFERENCES\s+"?(\w+)',b))
        pg={r[2] for r in dbs[s].execute(f'PRAGMA foreign_key_list("{t}")').fetchall()}
        if rx!=pg: bad.append((s,t,sorted(rx-pg),sorted(pg-rx)))
print(f'Z1 foreign-key parse: {len(bad)} of {n} tables differ ({100*len(bad)/n:.1f}%); limit 1%'); print('   ',bad[:6]); out['Z1']=(len(bad),n)
# Z2 replay completeness
src=set()
for s in S:
    for f in glob.glob(f'{SRC}/domain/schema/{s}/sql/*.sql'): src|={(s,t) for t in re.findall(r'CREATE TABLE (\w+)',open(f).read())}
rep={(s,t) for s in S for t in V[s]['tables']}
missing=sorted(src-rep); extra=sorted(rep-src)
print(f'Z2 replay: source tables missing from replay: {len(missing)} {missing[:8]}; replay-only tables: {len(extra)} {extra[:8]}'); out['Z2']=(len(missing),len(src))
# Z3 life / watched / immutable
b3=[]
for s in S:
    db=dbs[s]
    trig=collections.defaultdict(list)
    for name,tbl,sql in db.execute("select name,tbl_name,sql from sqlite_master where type='trigger'"): trig[tbl].append((name,sql or ''))
    for t in V[s]['tables']:
        cols={r[1] for r in db.execute(f'PRAGMA table_info("{t}")').fetchall()}
        ty=e15.typing(V[s],t)
        life_truth='life_id' in cols
        watched_truth=any(n.startswith('trg_log_') for n,_ in trig[t])
        imm_truth=any(('RAISE' in sql.upper()) and 'guard' not in n and not n.startswith('trg_log_') for n,sql in trig[t])
        for k,tr in (('life',life_truth),('watched',watched_truth),('immutable',imm_truth)):
            if bool(ty[k])!=tr: b3.append((s,t,k,bool(ty[k]),tr))
tot3=sum(len(V[s]['tables']) for s in S)*3
print(f'Z3 life/watched/immutable: {len(b3)} flag disagreements of {tot3} ({100*len(b3)/tot3:.2f}%); limit 1%'); print('   ',b3[:10]); out['Z3']=(len(b3),tot3)
# Z4 status flag
st=[(s,t) for s in S for t in V[s]['tables'] if e15.typing(V[s],t)['status']]
odd=[(s,t) for s,t in st if not t.endswith('_status')]
print(f'Z4 status flag: {len(st)} flagged; those not named *_status: {len(odd)}'); 
for s,t in odd: print('    ',s,t,[r[1] for r in dbs[s].execute(f'PRAGMA table_info("{t}")').fetchall()][:8])
# Z5 lookup
def info(s,t):
    cols=dbs[s].execute(f'PRAGMA table_info("{t}")').fetchall()
    pk=[r[1] for r in cols if r[5]>0]; types={r[1]:r[2] for r in cols}
    fkc={r[3] for r in dbs[s].execute(f'PRAGMA foreign_key_list("{t}")').fetchall()}
    return len(cols),pk,types,fkc
referenced=collections.Counter()
for s in S:
    for t in V[s]['tables']:
        for r in dbs[s].execute(f'PRAGMA foreign_key_list("{t}")').fetchall(): referenced[(s,r[2])]+=1
def new_rule(s,t):
    n,pk,types,fkc=info(s,t)
    seeded=len(V[s]['seeds'].get(t,()))>0
    keyok=(len(pk)==1 and types[pk[0]].upper().startswith('INT')) or (len(pk)>=2 and set(pk)<=fkc)
    return referenced[(s,t)]>0 and seeded and n<=3 and keyok
old=[(s,t) for s in S for t in V[s]['tables'] if e15.typing(V[s],t)['lookup']]
newl=[(s,t) for s in S for t in V[s]['tables'] if new_rule(s,t)]
seeded_not_old=[(s,t) for s in S for t in V[s]['tables'] if V[s]['seeds'].get(t) and (s,t) not in old]
print(f'Z5 lookup: old rule flags {len(old)}, candidate rule flags {len(newl)}; flagged only by old: {sorted(set(old)-set(newl))}; only by new: {sorted(set(newl)-set(old))}')
print('   seeded tables not flagged by the old rule:',[(s,t) for s,t in seeded_not_old])
json.dump(dict(old=old,new=newl,seeded_not_old=seeded_not_old),open('z5.json','w'),indent=1)
# Z6 lead-table rule
man=json.load(open('../e33/page-manifest.json'))
def fkl(t):
    o=[]
    for s in S:
        for r in dbs[s].execute(f'PRAGMA foreign_key_list("{t}")').fetchall(): o.append(r[2])
    return o
bad6=[];n6=0
for p,d in man['pages'].items():
    G=set(d['tables']); named=p.replace('-','_')
    if named in G:
        n6+=1
        indeg=collections.Counter(q for t in G for q in fkl(t) if q in G and q!=t)
        lead=sorted(G,key=lambda t:(-indeg[t],len(t),t))[0]
        if lead!=named: bad6.append((p,lead))
print(f'Z6 lead-table rule: {len(bad6)} of {n6} pages with a table named like the page have another lead ({100*len(bad6)/n6:.0f}%); limit 10%'); print('   ',bad6); out['Z6']=(len(bad6),n6)
json.dump(out,open('audit_mech.json','w'))
