import sys,re,os,json,sqlite3,collections
sys.path.insert(0,'../e15')
import e15
exec(open('e38.py').read().split("fk,lookup=fkmap(e15.NEW)")[0])   # chunk definitions (man, CARVE, chunk, chunks, fkmap)
def build(ddl):
    dbs={}
    for s in ('model','controller'):
        db=sqlite3.connect(':memory:')
        for st in e15.split(open(ddl[s]).read()): db.executescript(st.rstrip().rstrip(';')+';')
        dbs[s]=db
    return dbs
def notnull_fks(dbs,t):
    out=[]
    for s,db in dbs.items():
        info={r[1]:r for r in db.execute(f'PRAGMA table_info("{t}")').fetchall()}
        if not info: continue
        pkcols={c for c,r in info.items() if r[5]>0}
        for r in db.execute(f'PRAGMA foreign_key_list("{t}")').fetchall():
            col,par=r[3],r[2]
            out.append((col,par,bool(info[col][3]) or col in pkcols,col in pkcols))
        break
    return out
def lead(g,G,dbs):
    named=[t for t in G if t==g.replace('-','_')]
    if named: return named[0]
    indeg=collections.Counter()
    for t in G:
        for c,p,nn,pk in notnull_fks(dbs,t):
            if p in G and p!=t: indeg[p]+=1
    return sorted(G,key=lambda t:(-indeg[t],len(t),t))[0]
def owners(ddl,tabs=None):
    dbs=build(ddl); V={s:e15.parse(ddl[s]) for s in ('model','controller')}
    lookup={t for s in V for t in V[s]['tables'] if e15.typing(V[s],t)['lookup']}-{'space'}
    res={}
    for g in chunks:
        G=[t for t,c in chunk.items() if c==g and (tabs is None or t in tabs)]
        if not G: continue
        L=lead(g,G,dbs); own=set(); ident=set(); attr=set()
        for col,par,nn,pk in notnull_fks(dbs,L):
            if par in lookup or par not in chunk or chunk[par]==g: continue
            (own if nn else attr).add(chunk[par])
            if pk: ident.add(chunk[par])
        res[g]=dict(lead=L,owners=sorted(own),identifying=sorted(ident),attr=sorted(attr-own))
    return res
if __name__=='__main__':
    R1=owners(e15.NEW)
    def level(r): return 'section of '+r['owners'][0] if len(r['owners'])==1 else 'association (page)' if len(r['owners'])>=2 else 'root (page)'
    for g,r in sorted(R1.items(),key=lambda x:(len(x[1]['owners']),x[0])): print('%-22s %-26s lead=%-26s owners=%s ident=%s attr=%s'%(g,level(r),r['lead'],r['owners'],r['identifying'],r['attr'][:4]))
    json.dump(R1,open('e38b_result.json','w'),indent=1)
    print('\nPREDICTIONS')
    P1=['unit-state','application-scale','machine-placement','cloud-instance','port']
    print('(1) sections:',[(g,level(R1[g])) for g in P1],'->',sum(1 for g in P1 if level(R1[g]).startswith('section')),'/5')
    P2=['model','charm','machine','application','cloud','user','space','storage-pool','agent-version','telemetry']
    print('(2) roots:',[(g,level(R1[g])) for g in P2],'->',sum(1 for g in P2 if level(R1[g]).startswith('root')),'/10')
    P3=['relation-unit','application-endpoint','permission']
    print('(3) associations:',[(g,level(R1[g])) for g in P3],'->',sum(1 for g in P3 if level(R1[g]).startswith('association')),'/3')
    P4=['unit','relation','secret','resource']
    print('(4) one or two owners:',[(g,level(R1[g]),R1[g]['owners']) for g in P4])
    # (b) stability
    chg=set(json.load(open('../e15/e15_result.json'))['model']['changed_C'])|set(json.load(open('../e15/e15_result.json'))['controller']['changed_C'])
    common={t for t in chunk if t in e15.parse(e15.OLD['model'])['tables'] or t in e15.parse(e15.OLD['controller'])['tables']}
    R0=owners(e15.OLD,tabs=common)
    unchanged=[g for g in R1 if g in R0 and not any(t in chg for t,c in chunk.items() if c==g)]
    same=[g for g in unchanged if R0[g]['owners']==R1[g]['owners']]
    print('\n(b) chunks with no changed table:',len(unchanged),'owner sets equal in 4.0.15 and 4.1:',len(same),'= %.0f%%'%(100*len(same)/max(1,len(unchanged))))
