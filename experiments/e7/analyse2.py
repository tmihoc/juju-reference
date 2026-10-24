import json,collections,math,itertools
S={o['id']:o for o in json.load(open('e8_sample.json'))}
A={x['id']:x for x in json.load(open('e8_a.json'))}; B={x['id']:x for x in json.load(open('e8_b.json'))}
Ctl={x['id']:x['label'] for x in json.load(open('e8_control.json'))}
ids=sorted(S)
C=['identity','state','observation','agent','dynamics','none']
def kappa(x,y,cats):
    n=len(x); po=sum(a==b for a,b in zip(x,y))/n
    cx=collections.Counter(x); cy=collections.Counter(y)
    pe=sum(cx[c]*cy[c] for c in cats)/n/n
    return round(po,3),round((po-pe)/(1-pe),3)
def nmi(x,y):
    n=len(x); cx=collections.Counter(x); cy=collections.Counter(y); cxy=collections.Counter(zip(x,y))
    hx=-sum(v/n*math.log(v/n) for v in cx.values()); hy=-sum(v/n*math.log(v/n) for v in cy.values())
    mi=sum(v/n*math.log((v/n)/((cx[a]/n)*(cy[b]/n))) for (a,b),v in cxy.items())
    return round(mi/math.sqrt(hx*hy),3)
for name,sel in [('all',ids),('A layered pages',[i for i in ids if S[i]['corpus']=='A']),('B Go docs',[i for i in ids if S[i]['corpus']=='B'])]:
    a=[A[i]['primary'] for i in sel]; b=[B[i]['primary'] for i in sel]
    print(name,len(sel),'raters agree/kappa',kappa(a,b,C),'| none share A,B',round(a.count('none')/len(a),3),round(b.count('none')/len(b),3))
a=[A[i]['primary'] for i in ids]; b=[B[i]['primary'] for i in ids]
print('primary distribution A',collections.Counter(a)); print('B',collections.Counter(b))
print('confusion A->B off-diagonal',collections.Counter((x,y) for x,y in zip(a,b) if x!=y).most_common(12))
# control
agree=[i for i in ids if A[i]['primary']==B[i]['primary']]
dim=[A[i]['primary'] for i in agree]; ctl=[Ctl[i] for i in agree]
print('NMI dims vs control (items raters agree on):',nmi(dim,ctl),'| control dist',collections.Counter(Ctl.values()))
# old layers vs dims (corpus A)
la=[i for i in agree if S[i]['corpus']=='A']
print('NMI dims vs old layer heading (A):',nmi([A[i]['primary'] for i in la],[S[i]['layer'] for i in la]))
# none statements
print('--- none (either rater)')
for i in ids:
    if 'none' in (A[i]['primary'],B[i]['primary']):
        print(i,S[i]['corpus'],S[i]['source'],A[i]['primary'],B[i]['primary'],'|',(A[i]['none_reason'] or B[i]['none_reason']),'|',S[i]['text'][:110])
# presupposition matrix on agreed items
M=collections.Counter(); N=collections.Counter()
for i in agree:
    p=A[i]['primary']
    if p=='none': continue
    N[p]+=1
    for q in set(A[i]['presupposes'])&set(B[i]['presupposes']):
        M[(p,q)]+=1
dims=['identity','state','observation','agent','dynamics']
print('--- presupposition: row statement class presupposes column class (both raters), as share of row')
print('%-12s'%'',*['%-12s'%d for d in dims])
for p in dims:
    print('%-12s'%p,*['%-12s'%(round(M[(p,q)]/N[p],2) if N[p] else '-') for q in dims],N[p])
best=None
for perm in itertools.permutations(dims):
    pos={d:k for k,d in enumerate(perm)}
    v=sum(M[(p,q)] for p in dims for q in dims if p!=q and pos[q]>pos[p])
    if best is None or v<best[0]: best=(v,perm)
    if perm==('identity','agent','state','observation','dynamics'): print('forward refs, identity>agent>state>obs>dyn',v)
    if perm==('identity','state','observation','agent','dynamics'): print('forward refs, identity>state>obs>agent>dyn',v)
    if perm==('identity','state','observation','dynamics','agent'): print('forward refs, identity>state>obs>dyn>agent',v)
print('best order',best, 'total presupposition pairs',sum(M.values()))
# straddlers
st=[i for i in ids if (A[i].get('secondary') or B[i].get('secondary')) ]
print('items with any secondary:',len(st))
split=[i for i in agree if A[i].get('secondary')!=B[i].get('secondary')]
print('agreed primary but different secondary:',len(split))
print(collections.Counter((A[i]['primary'],A[i].get('secondary') or B[i].get('secondary')) for i in agree if (A[i].get('secondary') or B[i].get('secondary'))).most_common(12))
