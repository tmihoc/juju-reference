import json,collections,math
S=json.load(open('sample.json')); A={x['id']:x for x in json.load(open('rater_a.json'))}; B={x['id']:x for x in json.load(open('rater_b.json'))}
filed={o['id']:o['filed'] for o in S}
C=['identity','state','observation','agent','dynamics']
def kappa(x,y):
    n=len(x); po=sum(a==b for a,b in zip(x,y))/n
    cx=collections.Counter(x); cy=collections.Counter(y)
    pe=sum(cx[c]*cy[c] for c in C)/n/n
    return po,(po-pe)/(1-pe)
ids=sorted(filed)
a=[A[i]['primary'] for i in ids]; b=[B[i]['primary'] for i in ids]; f=[filed[i] for i in ids]
print('A vs B',kappa(a,b)); print('A vs filing',kappa(a,f)); print('B vs filing',kappa(b,f))
both=[i for i in ids if A[i]['primary']==B[i]['primary']]
print('raters agree on',len(both),'of',len(ids),'; of those agree with filing',sum(A[i]['primary']==filed[i] for i in both))
print('confusion filing->rater A/B')
for fl in C:
    row=collections.Counter()
    for i in ids:
        if filed[i]==fl: row[(A[i]['primary'],B[i]['primary'])]+=1
    print(fl,dict(row))
print('--- disagreements with filing (both raters agree, differ from filing)')
for i in ids:
    if A[i]['primary']==B[i]['primary']!=filed[i]:
        o=[x for x in S if x['id']==i][0]
        print(i,o['page'],'filed',filed[i],'raters',A[i]['primary'],'|',o['text'][:170])
sec=[i for i in ids if A[i].get('secondary') or B[i].get('secondary')]
print('items with a secondary label from either rater:',len(sec))
