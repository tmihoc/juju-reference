# E15: version stability of the typing, 4.0.15 against 4.1 (pre-registered criterion in the plan).
# usage: python3 e15.py <v4015 code root> <4.1 code root>
import re,sys,os,glob,json,collections
HERE=os.path.dirname(os.path.abspath(__file__))
E11=os.path.join(HERE,'..','e11')
OLD={'model':HERE+'/v4015-model.ddl','controller':HERE+'/v4015-controller.ddl'}
NEW={'model':E11+'/model.ddl','controller':E11+'/controller.ddl'}
def norm(s):
    s=re.sub(r'--[^\n]*','',s)   # comments are not schema
    return re.sub(r'\s+',' ',s).strip()
import sqlite3
HEAD=re.compile(r'^(CREATE|INSERT|ALTER|DROP|UPDATE|DELETE)\b')
def split(text):
    # Statement heads at column 0 (the release DDL has a view without a closing semicolon and
    # triggers whose bodies start at column 0).
    out=[];cur=None
    for line in text.split('\n'):
        in_trigger=cur is not None and cur[0].startswith('CREATE TRIGGER') and not any(l.strip().upper()=='END;' for l in cur)
        if HEAD.match(line) and not in_trigger:
            if cur: out.append('\n'.join(cur))
            cur=[line]
        elif cur is not None and not line.startswith('--'): cur.append(line)
    if cur: out.append('\n'.join(cur))
    return out
def parse(path):
    """Replay the DDL in SQLite and read the final state from sqlite_master (the release DDLs
    are statement histories with ALTER/DROP/RENAME, so a text parser would read them wrongly)."""
    db=sqlite3.connect(':memory:')
    for st in split(open(path).read()): db.executescript(st.rstrip().rstrip(';')+';')
    V=dict(tables={},indexes=collections.defaultdict(set),triggers=collections.defaultdict(dict),
           seeds=collections.defaultdict(set),views={},ns={})
    for typ,name,tbl,sql in db.execute("select type,name,tbl_name,sql from sqlite_master where sql is not null"):
        sql=norm(sql)
        if typ=='table':
            V['tables'][name]=sql[sql.index('(')+1:]
        elif typ=='index': V['indexes'][tbl].add(sql)
        elif typ=='trigger': V['triggers'][tbl][name]=sql
        elif typ=='view': V['views'][name]=sql
    V['tables']={t:b for t,b in V['tables'].items() if not t.startswith('sqlite_')}
    for i,n,*_ in db.execute('select * from change_log_namespace'): V['ns'][i]=n
    # Namespace ids are renumbered between versions: key triggers and seeds by namespace name.
    for tbl,trs in V['triggers'].items():
        for n,sql in trs.items():
            trs[n]=re.sub(r'(VALUES \(\d+, )(\d+)(,)',lambda m:m.group(1)+'ns:'+V['ns'].get(int(m.group(2)),'?')+m.group(3),sql)
    for t in V['tables']:
        for row in db.execute('select * from "%s"'%t): V['seeds'][t].add(repr(row))
    V['seeds']['change_log_namespace']={repr(r[1:]) for r in db.execute('select * from change_log_namespace')}
    return V
def cols(body):
    n=0
    for part in re.split(r',\s*(?![^()]*\))',body):
        p=part.strip()
        if p and not re.match(r'(PRIMARY|FOREIGN|UNIQUE|CHECK|CONSTRAINT)\b',p): n+=1
    return n
def typing(V,t):
    body=V['tables'][t]; tr=V['triggers'].get(t,{})
    watched=set()
    for n,s in tr.items():
        if n.startswith('trg_log_'):
            op=re.search(r'AFTER (INSERT|UPDATE|DELETE) ON',s).group(1)
            nid=re.search(r'VALUES \(\d+, ns:(\w+),',s)
            watched.add((op,nid.group(1) if nid else '?'))
    return dict(life='life_id' in body,
        status=t.endswith('_status') or 'status_id' in body,
        watched=sorted(watched),
        immutable=any(('_immutable' in n or '_unmodifiable' in n) for n in tr),
        guard=sorted(n for n in tr if 'guard' in n),
        lookup=bool(V['seeds'].get(t)) and cols(body)<=3 and not re.search(r'\buuid\b[^,()]*PRIMARY KEY|PRIMARY KEY\s*\(\s*uuid',body))
def load(S):
    return {k:parse(p) for k,p in S.items()}
def fingerprint(V,t):
    return (V['tables'].get(t), tuple(sorted(V['indexes'].get(t,()))),
            tuple(sorted(V['triggers'].get(t,{}).items())), tuple(sorted(V['seeds'].get(t,()))))
def run():
    O,N=load(OLD),load(NEW)
    res={}
    for k in ('model','controller'):
        o,n=O[k],N[k]
        names=set(o['tables'])|set(n['tables'])|set(o['seeds'])|set(n['seeds'])
        C=sorted(t for t in names if fingerprint(o,t)!=fingerprint(n,t))
        typ={}
        for t in set(o['tables'])|set(n['tables']):
            typ[t]=(typing(o,t) if t in o['tables'] else None, typing(n,t) if t in n['tables'] else None)
        tdiff=sorted(t for t,(a,b) in typ.items() if a!=b)
        outside=[t for t in tdiff if t not in C]
        views_diff=sorted(v for v in set(o['views'])|set(n['views']) if o['views'].get(v)!=n['views'].get(v))
        # inventories
        inv={}
        for f in ('life','status','immutable','lookup'):
            a={t for t,(x,y) in typ.items() if x and x[f]}; b={t for t,(x,y) in typ.items() if y and y[f]}
            inv[f]=dict(added=sorted(b-a),removed=sorted(a-b))
        a={(t,)+w for t,(x,y) in typ.items() if x for w in x['watched']}; b={(t,)+w for t,(x,y) in typ.items() if y for w in y['watched']}
        inv['watched']=dict(added=sorted(b-a),removed=sorted(a-b))
        a={(t,g) for t,(x,y) in typ.items() if x for g in x['guard']}; b={(t,g) for t,(x,y) in typ.items() if y for g in y['guard']}
        inv['guard']=dict(added=sorted(b-a),removed=sorted(a-b))
        look={}
        for t in set(o['seeds'])|set(n['seeds']):
            if (typ.get(t,(None,None))[0] or {}).get('lookup') or (typ.get(t,(None,None))[1] or {}).get('lookup'):
                if o['seeds'].get(t,set())!=n['seeds'].get(t,set()):
                    look[t]=dict(added=sorted(n['seeds'].get(t,set())-o['seeds'].get(t,set())),removed=sorted(o['seeds'].get(t,set())-n['seeds'].get(t,set())))
        inv['lookup_values']=look
        # (b): inventory elements attributable to C; C tables that change typing appear in the inventory diff
        elems=set()
        for f,d in inv.items():
            if f=='lookup_values': elems|=set(d)
            else:
                for key in ('added','removed'):
                    for e in d[key]: elems.add(e if isinstance(e,str) else e[0])
        unattributed=sorted(elems-set(C))
        # C tables whose typing tuple differs must be in elems (completeness)
        missing=sorted(t for t in tdiff if t not in elems and not (typ[t][0] is None or typ[t][1] is None) )
        # an added/removed table with no typed artifact is reported, not an error
        res[k]=dict(n_old=len(o['tables']),n_new=len(n['tables']),added=sorted(set(n['tables'])-set(o['tables'])),
            removed=sorted(set(o['tables'])-set(n['tables'])),changed_C=C,n_C=len(C),typing_diff=tdiff,
            typing_diff_outside_C=outside,views_diff=views_diff,inventory=inv,unattributed=unattributed,
            typing_diff_not_in_inventory=missing,
            typed_new={t:typ[t][1] for t in set(n['tables'])-set(o['tables'])})
    return res
if __name__=='__main__':
    r=run()
    json.dump(r,open(HERE+'/e15_result.json','w'),indent=1,default=list)
    for k,v in r.items():
        print('==',k,'tables old/new',v['n_old'],v['n_new'],'added',v['added'],'removed',v['removed'])
        print(' |C|',v['n_C'],'typing diffs',len(v['typing_diff']),'outside C',v['typing_diff_outside_C'])
        print(' views changed',len(v['views_diff']))
        print(' unattributed inventory elements',v['unattributed'],' typing diffs not in inventory',v['typing_diff_not_in_inventory'])
        for f,d in v['inventory'].items():
            if f=='lookup_values': print(' ',f,{t:(len(x['added']),len(x['removed'])) for t,x in d.items()})
            else: print(' ',f,'+',len(d['added']),'-',len(d['removed']))


def lead_table(name,tables,indeg):
    """The table that carries the identity of a group: the table named like the group when there is one,
    otherwise the table with the most foreign keys pointing into it from the group (ties: shorter name)."""
    G=set(tables); named=name.replace('-','_')
    if named in G: return named
    return sorted(G,key=lambda t:(-indeg.get(t,0),len(t),t))[0]
