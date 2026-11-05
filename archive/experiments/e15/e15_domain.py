# E15 criterion (e): domain typing under the 4.0.15 and the 4.1 owner map.
import re,glob,os,json,collections,sys
import e15
S='/tmp/claude-1000/-home-dora-git-juju/8c1e4c6e-570b-417b-bc47-eea27d0d6ac3/scratchpad/v4015'
OLDROOT=S; NEWROOT=os.path.expanduser('~/git/misc/juju-v2-preview')
CROSS={'removal','recovery','modelmigration','export','modelimport','schema','testing'}
def owners(root,names):
    files=sorted({f for f in glob.glob(root+'/domain/*/state/**/*.go',recursive=True)+glob.glob(root+'/domain/*/*.go') if not f.endswith('_test.go')})
    pat=re.compile(r'\b('+'|'.join(sorted(map(re.escape,names),key=len,reverse=True))+r')\b')
    writes=collections.defaultdict(collections.Counter);refs=collections.defaultdict(collections.Counter)
    for f in files:
        dom=f.split('/domain/')[1].split('/')[0]
        if dom in CROSS: continue
        txt=open(f).read()
        for m in re.finditer(r'(INSERT INTO|INSERT OR \w+ INTO)\s+(\w+)',txt):
            if m.group(2) in names: writes[m.group(2)][dom]+=1
        for m in pat.finditer(txt): refs[m.group(1)][dom]+=1
    out={}
    for t in names:
        c=writes.get(t) or refs.get(t)
        out[t]=c.most_common(1)[0][0] if c else None
    return out
def domtyping(V,own,tabs):
    D=collections.defaultdict(lambda:dict(tables=set(),life=set(),watched=set(),immutable=set()))
    for t in tabs:
        d=own[t] or '(unowned)'; ty=e15.typing(V,t)
        D[d]['tables'].add(t)
        if ty['life']: D[d]['life'].add(t)
        if ty['watched']: D[d]['watched'].add(t)
        if ty['immutable']: D[d]['immutable'].add(t)
    return D
O=e15.load(e15.OLD);N=e15.load(e15.NEW);R=json.load(open(e15.HERE+'/e15_result.json'))
res={}
for k in ('model','controller'):
    ot=set(O[k]['tables']);nt=set(N[k]['tables'])
    oown=owners(OLDROOT,ot|nt);nown=owners(NEWROOT,ot|nt)
    Do=domtyping(O[k],oown,sorted(ot));Dn=domtyping(N[k],nown,sorted(nt))
    C=set(R[k]['changed_C'])
    rows=[]
    for d in sorted(set(Do)|set(Dn)):
        a=Do.get(d);b=Dn.get(d)
        sig=lambda x:None if x is None else (bool(x['life']),bool(x['watched']),bool(x['immutable']))
        owned_C=bool((Dn[d]['tables'] if d in Dn else set())&C) or bool((Do[d]['tables'] if d in Do else set())&C) or bool(((Dn[d]['tables'] if d in Dn else set())^(Do[d]['tables'] if d in Do else set())))
        rows.append(dict(domain=d,old=sig(a),new=sig(b),n_old=len(a['tables']) if a else 0,n_new=len(b['tables']) if b else 0,touches_C=owned_C,differs=sig(a)!=sig(b)))
    # owner changes for tables present in both versions
    moved=sorted(t for t in ot&nt if oown[t]!=nown[t])
    res[k]=dict(rows=rows,moved_owner=[(t,oown[t],nown[t]) for t in moved])
    unchanged_domains=[r for r in rows if not r['touches_C']]
    viol=[r for r in unchanged_domains if r['differs']]
    print('==',k,'domains',len(rows),'no table in C or added/removed',len(unchanged_domains),'typing differs among them',len(viol),viol)
    print('  differing domains (touching C):',[(r['domain'],r['old'],r['new']) for r in rows if r['differs'] and r['touches_C']])
    print('  tables whose owner changed between the two code versions:',len(moved),[(t,oown[t],nown[t]) for t in moved][:15])
json.dump(res,open(e15.HERE+'/e15_domain.json','w'),indent=1)

# literal form of (e): domains with no owned table (4.1 owner map) in C
print('--- literal (e)')
for k in ('model','controller'):
    ot=set(O[k]['tables']);nt=set(N[k]['tables'])
    oown=owners(OLDROOT,ot|nt);nown=owners(NEWROOT,ot|nt)
    Do=domtyping(O[k],oown,sorted(ot));Dn=domtyping(N[k],nown,sorted(nt));C=set(R[k]['changed_C'])
    sig=lambda x:None if x is None else (bool(x['life']),bool(x['watched']),bool(x['immutable']))
    free=[d for d in Dn if not (Dn[d]['tables']&C)]
    bad=[(d,sig(Do.get(d)),sig(Dn[d])) for d in free if sig(Do.get(d))!=sig(Dn[d])]
    print(k,'domains without a C table (4.1 map):',len(free),'differing:',bad)
    for d in set(Do)|set(Dn):
        a=Do.get(d);b=Dn.get(d)
        if sig(a)!=sig(b):
            for f in ('life','watched','immutable'):
                x=(a[f] if a else set());y=(b[f] if b else set())
                if x!=y: print('   ',d,f,'old-only',sorted(x-y),'new-only',sorted(y-x),'| in C:',sorted((x^y)&C),'| owner moved:',[(t,oown[t],nown[t]) for t in sorted((x^y)) if t in oown and oown[t]!=nown[t]])
