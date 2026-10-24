import sqlite3,glob,re,sys,textwrap
def load(dirn):
    con=sqlite3.connect(':memory:')
    for f in sorted(glob.glob(f'/home/dora/git/misc/juju-v2-preview/domain/schema/{dirn}/sql/*.sql')): con.executescript(open(f).read())
    return con
def unique_single(con,t,col):
    pk=[r[1] for r in con.execute(f"pragma table_info({t})") if r[5]]
    if pk==[col]: return True
    for idx in con.execute(f"pragma index_list({t})"):
        if idx[2]:
            cols=[r[2] for r in con.execute(f"pragma index_info({idx[1]})")]
            if cols==[col]: return True
    return False
def nullable(con,t,col):
    for r in con.execute(f"pragma table_info({t})"):
        if r[1]==col: return not r[3] and not r[5]
def wrap(cols,width=24):
    return "\\n".join(textwrap.wrap(cols,width=width,break_long_words=False))
def chips(con,salient,extra_edges=(),dirn='model'):
    nodes=[];edges=[]
    for t,c in salient.items():
        lab=t if not c else t+"\\n("+wrap(c)+")"
        # wrap closes the bracket on the last line
        nodes.append(f'    {t} [type: record, label: "{lab}", ground: "{dirn}:{t}"]')
    for t in salient:
        for r in con.execute(f"pragma foreign_key_list({t})"):
            if r[2] in salient:
                col=r[3]; child="1" if unique_single(con,t,col) else "m"
                if nullable(con,t,col) and child=="1": child="0..1"
                edges.append(f'    {t} -> {r[2]} [type: data, ends: "{child}:1", ground: "{dirn}:{t}.{col}"]')
    for a,b,ends,ground in extra_edges:
        edges.append(f'    {a} -> {b} [type: data, ends: "{ends}", ground: "{ground}"]')
    return nodes,edges
def check(con,salient):
    for t,cols in salient.items():
        have={r[1] for r in con.execute(f"pragma table_info({t})")}
        assert t in {r[0] for r in con.execute("select name from sqlite_master where type='table'")},t
        miss=[c.strip() for c in cols.split(',') if c.strip() and c.strip() not in have]
        assert not miss,(t,miss)
