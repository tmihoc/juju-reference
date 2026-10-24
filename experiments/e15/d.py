# E15 criterion (d): compare the DDL changed set C with the tables named on changed lines of
# `git diff v4.0.15 HEAD` under domain/schema (tests and release DDL files excluded).
import re,subprocess,json,os,sys
import e15
WT=os.path.expanduser('~/git/misc/juju-v2-preview')
r=json.load(open(os.path.join(e15.HERE,'e15_result.json')))
O=e15.load(e15.OLD);N=e15.load(e15.NEW)
out={}
for k in ('model','controller'):
    names=set(O[k]['tables'])|set(N[k]['tables'])
    C=set(r[k]['changed_C'])&names   # tables only (seed-only keys such as sqlite names dropped)
    diff=subprocess.run(['git','-C',WT,'diff','-U0','v4.0.15','HEAD','--',
        f'domain/schema/{k}',f'domain/schema/{k}triggers.go',':(exclude)*_test.go',':(exclude)*.ddl'],capture_output=True,text=True).stdout
    literal=set();strict=set();ctx=set();cur=None;lit_files={}
    for line in diff.split('\n'):
        if line.startswith('diff --git'): cur=line.split(' b/')[-1]
        if line.startswith('@@'):
            m=re.search(r'@@.*?@@\s*(?:CREATE (?:TABLE|VIEW)|ALTER TABLE)\s+"?([a-z_][a-z0-9_]*)',line)
            if m and m.group(1) in names: ctx.add(m.group(1))
        if not line or line[0] not in '+-' or line[:3] in ('+++','---'): continue
        t=line[1:].strip()
        if t.startswith(('--','//','/*','*')): continue
        for tok in set(re.findall(r'[a-z_][a-z0-9_]*',t)):
            if tok in names: literal.add(tok); lit_files.setdefault(tok,set()).add(cur)
        for m in re.finditer(r'\b(?:CREATE TABLE|ALTER TABLE|DROP TABLE|INSERT INTO|INSERT OR \w+ INTO|UPDATE|DELETE FROM|ON|CREATE TRIGGER \w+ \w+ \w+ ON|CREATE UNIQUE INDEX \w+ ON|CREATE INDEX \w+ ON|TABLE)\s+"?([a-z_][a-z0-9_]*)',t,flags=re.I):
            if m.group(1) in names: strict.add(m.group(1))
    deleted={l.split('\t')[1] for l in subprocess.run(['git','-C',WT,'diff','--name-status','v4.0.15','HEAD','--',f'domain/schema/{k}'],capture_output=True,text=True).stdout.split('\n') if l.startswith('D\t')}
    ctxall=strict|ctx
    nn=sorted(literal-C)
    only_deleted=[t for t in nn if lit_files[t]<=deleted]
    out[k]=dict(ctx=len(ctxall),C_in_ctx=len(C&(literal|ctxall)),only_deleted_files=len(only_deleted),named_literal_not_C=len(nn),C=len(C),literal=len(literal),strict=len(strict),
        C_in_literal=len(C&literal),C_in_strict=len(C&strict),
        literal_in_C=len(literal&C),strict_in_C=len(strict&C),
        C_not_named_strict=sorted(C-strict),named_strict_not_C=sorted(strict-C),
        C_not_named_literal=sorted(C-literal))
json.dump(out,open(os.path.join(e15.HERE,'e15_d.json'),'w'),indent=1)
for k,v in out.items():
    print(k,{a:b for a,b in v.items() if not isinstance(b,list)})
    print('  C not named (strict):',v['C_not_named_strict'])
    print('  C not named (literal):',v['C_not_named_literal'])
    print('  named strict but not in C:',len(v['named_strict_not_C']),v['named_strict_not_C'][:40])
