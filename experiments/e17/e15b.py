import re,os,json,glob,sys,subprocess,io,contextlib
sys.path.insert(0,'../e15')
import e15
SRC=os.path.expanduser('~/git/misc/juju-v2-preview'); HERE=os.path.dirname(os.path.abspath(__file__))
TP=json.load(open(HERE+'/topics.json'))
R=json.load(open('../e15/e15_result.json'))
O={k:e15.parse(p) for k,p in e15.OLD.items()};N={k:e15.parse(p) for k,p in e15.NEW.items()}
def sqlfiles(rev,scope):
    names=subprocess.run(['git','-C',SRC,'ls-tree','--name-only',rev,f'domain/schema/{scope}/sql/'],capture_output=True,text=True).stdout.split()
    return {re.sub(r'\.PATCH','',re.sub(r'^\d+-','',os.path.basename(n)))[:-4]:[] for n in names}, names
def topic_tables(rev,scope,topic):
    out=set()
    _,names=sqlfiles(rev,scope)
    for n in names:
        b=re.sub(r'\.PATCH','',re.sub(r'^\d+-','',os.path.basename(n)))[:-4]
        if b==topic:
            out|=set(re.findall(r'CREATE TABLE (\w+)',subprocess.run(['git','-C',SRC,'show',f'{rev}:{n}'],capture_output=True,text=True).stdout))
    return out
def build(rev,V):
    dom={}
    for scope,m in TP.items():
        if scope=='removal_types': continue
        for d,topics in m.items():
            r=dom.setdefault(d,dict(tabs=set(),life=set(),watched=0,scopes=set()))
            for t in topics:
                for tb in topic_tables(rev,scope,t):
                    if tb not in V[scope]['tables']: continue
                    ty=e15.typing(V[scope],tb)
                    if ty['lookup']: continue
                    r['tabs'].add((scope,tb)); r['scopes'].add(scope)
                    if ty['life']: r['life'].add(scope)
                    if ty['watched']: r['watched']+=1
    return {d:(tuple(sorted(r['scopes'])),tuple(sorted(r['life'])),r['watched']>0) for d,r in dom.items() if r['tabs']},{d:r['tabs'] for d,r in dom.items()}
To,Tabo=build('ac643a09f7',O);Tn,Tabn=build('HEAD',N)
C={k:set(R[k]['changed_C'])|set(R[k]['added']) for k in R}
rows=[];viol=[];unexpl=[]
for d in sorted(set(To)|set(Tn)):
    owned=set(Tabo.get(d,set()))|set(Tabn.get(d,set()))
    touches=any(tb in C[s] for s,tb in owned)
    a,b=To.get(d),Tn.get(d)
    if a is None or b is None: rows.append((d,'only in '+('4.1' if a is None else '4.0.15'),touches)); continue
    if a!=b:
        rows.append((d,'CHANGED',touches,a,b))
        if not touches: viol.append(d)
    elif not touches: rows.append((d,'same, no changed table',False))
    else: rows.append((d,'same, has changed table',True))
untouched=[r for r in rows if r[1]=='same, no changed table']
print('domains in both:',sum(1 for r in rows if not r[1].startswith('only')),'; untouched by C:',len([r for r in rows if not r[1].startswith('only') and not r[2]]))
print('criterion 1: untouched domains whose typing changed:',viol)
print('criterion 2: typing changes:',[(r[0],r[3],r[4],r[2]) for r in rows if r[1]=='CHANGED'])
print('criterion 3, only in one version:',[(r[0],r[1]) for r in rows if r[1].startswith('only')])
