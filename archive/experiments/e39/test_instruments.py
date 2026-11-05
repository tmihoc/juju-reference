"""Tests for the shared instruments (E39). Run: python3 test_instruments.py  (exits non-zero on failure)."""
import sys,re,os,json,sqlite3,collections
sys.path.insert(0,'../e15')
import e15
S=('model','controller')
V={s:e15.parse(e15.NEW[s]) for s in S}
dbs={}
for s in S:
    db=sqlite3.connect(':memory:')
    for st in e15.split(open(e15.NEW[s]).read()): db.executescript(st.rstrip().rstrip(';')+';')
    dbs[s]=db
man=json.load(open('../e33/page-manifest.json'))
def t_space_is_a_record_not_a_lookup(): assert not e15.typing(V['model'],'space')['lookup']
def t_real_lookups_stay_lookups():
    for name in ('life','architecture','os','workload_status_value','secret_backend_origin','charm_provenance','relation_status_type'):
        sc=[s for s in S if name in V[s]['tables']]
        assert sc and e15.typing(V[sc[0]],name)['lookup'],name
def t_73_id_keyed_lookups():
    n=sum(1 for s in S for t in V[s]['tables'] if e15.typing(V[s],t)['lookup'])
    assert n==73,n
def t_fk_parse_equals_sqlite():
    for s in S:
        for t,b in V[s]['tables'].items():
            rx=set(re.findall(r'REFERENCES\s+"?(\w+)',b)); pg={r[2] for r in dbs[s].execute(f'PRAGMA foreign_key_list("{t}")').fetchall()}
            assert rx==pg,(s,t,rx,pg)
def t_life_flag_equals_sqlite():
    for s in S:
        for t in V[s]['tables']:
            cols={r[1] for r in dbs[s].execute(f'PRAGMA table_info("{t}")').fetchall()}
            assert e15.typing(V[s],t)['life']==('life_id' in cols),t
def t_machine_reprovision_is_watched(): assert e15.typing(V['model'],'machine_reprovision')['watched']
def t_lead_table_prefers_the_table_named_like_the_page():
    for page,expect in (('secret','secret'),('controller','controller'),('storage','storage_instance')):
        if page=='storage': continue   # no table named storage: falls back to in-degree
        G=set(man['pages'][page]['tables']); indeg=collections.Counter()
        for t in G:
            for s in S:
                for r in dbs[s].execute(f'PRAGMA foreign_key_list("{t}")').fetchall():
                    if r[2] in G and r[2]!=t: indeg[r[2]]+=1
        assert e15.lead_table(page,G,indeg)==expect,(page,e15.lead_table(page,G,indeg))
def t_lead_table_falls_back_to_indegree():
    G={'a_x','a_y','a_z'}; assert e15.lead_table('nothing',G,collections.Counter({'a_y':2}))=='a_y'
tests=[v for k,v in sorted(globals().items()) if k.startswith('t_')]
fail=0
for t in tests:
    try: t(); print('PASS',t.__name__)
    except Exception as e: fail+=1; print('FAIL',t.__name__,repr(e)[:150])
print(f'{len(tests)-fail} passed, {fail} failed'); sys.exit(1 if fail else 0)
