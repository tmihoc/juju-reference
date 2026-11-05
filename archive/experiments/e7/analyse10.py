import json,collections,itertools
S={o['id']:o for o in json.load(open('e10_sample.json'))}
A={x['id']:x for x in json.load(open('e10_a.json'))}; B={x['id']:x for x in json.load(open('e10_b.json'))}
ids=sorted(S)
C=['identity','interface','state','dynamics','agent','observation','failure','none']
def kap(x,y,cats=C):
    n=len(x); po=sum(a==b for a,b in zip(x,y))/n
    cx=collections.Counter(x); cy=collections.Counter(y); pe=sum(cx[c]*cy[c] for c in cats)/n/n
    return round(po,3),(round((po-pe)/(1-pe),3) if pe<1 else None)
a=[A[i]['primary'] for i in ids]; b=[B[i]['primary'] for i in ids]
print('overall',kap(a,b))
for corp in ['ref','err','howto','explanation']:
    sel=[i for i in ids if S[i]['corpus']==corp]
    x=[A[i]['primary'] for i in sel]; y=[B[i]['primary'] for i in sel]
    print(corp,len(sel),kap(x,y),'none A/B',x.count('none'),y.count('none'))
print('class counts A',collections.Counter(a)); print('class counts B',collections.Counter(b))
print('per-class agreement (both say X / either says X):')
for c in C:
    both=sum(1 for i in ids if A[i]['primary']==c==B[i]['primary']); either=sum(1 for i in ids if c in (A[i]['primary'],B[i]['primary']))
    print(' ',c,both,'/',either)
print('off-diagonal',collections.Counter((x,y) for x,y in zip(a,b) if x!=y).most_common(12))
# none kinds
print('--- none statements (either)')
for i in ids:
    if 'none' in (A[i]['primary'],B[i]['primary']) :
        print(i,S[i]['corpus'],A[i]['primary'],B[i]['primary'],'|',A[i]['none_reason'] or B[i]['none_reason'],'|',S[i]['text'][:100])
# errors: what do raters call the err corpus
print('err corpus labels A',collections.Counter(A[i]['primary'] for i in ids if S[i]['corpus']=='err'),'B',collections.Counter(B[i]['primary'] for i in ids if S[i]['corpus']=='err'))
# flags
for f in ['applicability','guidance']:
    both=sum(1 for i in ids if A[i][f] and B[i][f]); either=sum(1 for i in ids if A[i][f] or B[i][f])
    print(f,'both',both,'either',either,'of',len(ids))
# presupposition / order on agreed
agree=[i for i in ids if A[i]['primary']==B[i]['primary'] and A[i]['primary'] not in ('none',)]
M=collections.Counter();N=collections.Counter()
for i in agree:
    p=A[i]['primary']; N[p]+=1
    for q in set(A[i]['presupposes'])&set(B[i]['presupposes']): M[(p,q)]+=1
dims=['identity','interface','state','dynamics','agent','observation','failure']
print('presup share (row presupposes col)'); print('%-12s'%'',*['%-11s'%d[:10] for d in dims],'n')
for p in dims: print('%-12s'%p,*['%-11s'%(round(M[(p,q)]/N[p],2) if N[p] else '-') for q in dims],N[p])
best=[]
for perm in itertools.permutations(dims):
    pos={d:k for k,d in enumerate(perm)}
    v=sum(M[(p,q)] for p in dims for q in dims if p!=q and pos[q]>pos[p]); best.append((v,perm))
best.sort(); print('total pairs',sum(M.values()),'best orders',best[:4])
for name in [('identity','interface','state','dynamics','failure','agent','observation'),('identity','interface','state','agent','observation','dynamics','failure')]:
    pos={d:k for k,d in enumerate(name)}; print(name,sum(M[(p,q)] for p in dims for q in dims if p!=q and pos[q]>pos[p]))
