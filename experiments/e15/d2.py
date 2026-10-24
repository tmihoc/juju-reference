# Post hoc test of the reverse-direction failure of criterion (d): are the changed source lines
# that name a table outside C already present in the 4.0.15 DDL (a move/consolidation) ?
import re,subprocess,json,os,e15
WT=os.path.expanduser('~/git/misc/juju-v2-preview')
r=json.load(open(os.path.join(e15.HERE,'e15_result.json')))
O=e15.load(e15.OLD);N=e15.load(e15.NEW)
res={}
for k in ('model','controller'):
    names=set(O[k]['tables'])|set(N[k]['tables']); C=set(r[k]['changed_C'])&names
    old=e15.norm(open(e15.OLD[k]).read())
    diff=subprocess.run(['git','-C',WT,'diff','-U0','v4.0.15','HEAD','--',f'domain/schema/{k}',f'domain/schema/{k}triggers.go',':(exclude)*_test.go',':(exclude)*.ddl'],capture_output=True,text=True).stdout
    lines={}
    for line in diff.split('\n'):
        if not line or line[0] not in '+-' or line[:3] in ('+++','---'): continue
        t=line[1:].strip()
        if t.startswith(('--','//','/*','*')) or len(t)<12: continue
        for tok in set(re.findall(r'[a-z_][a-z0-9_]*',t)):
            if tok in names and tok not in C: lines.setdefault(tok,[]).append((line[0],t))
    explained=[];open_=[]
    for t,ls in lines.items():
        # a removed line is a move if its text exists in the old DDL; an added line is a move if
        # its text exists in the old DDL too (same content, different file/position)
        unmoved=[(s,x) for s,x in ls if e15.norm(x) not in old]
        (explained if not unmoved else open_).append((t,unmoved[:3]))
    res[k]=dict(tables_named_outside_C=len(lines),all_lines_already_in_old_ddl=len(explained),others=len(open_),
                others_detail=[(t,u) for t,u in open_][:60])
    print(k,{a:b for a,b in res[k].items() if a!='others_detail'})
json.dump(res,open(os.path.join(e15.HERE,'e15_d2.json'),'w'),indent=1)
