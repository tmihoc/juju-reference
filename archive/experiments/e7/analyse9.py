import json,collections
S={o['id']:o for o in json.load(open('e9_sample.json'))}
R={k:{x['id']:x for x in json.load(open(f'e9_{k}.json'))} for k in ['rule1','rule2','norule1','norule2']}
ids=sorted(S)
C=['identity','state','observation','agent','dynamics','none']
def kappa(x,y):
    n=len(x); po=sum(a==b for a,b in zip(x,y))/n
    cx=collections.Counter(x); cy=collections.Counter(y); pe=sum(cx[c]*cy[c] for c in C)/n/n
    return round(po,3),round((po-pe)/(1-pe),3)
def arm(a,b,name):
    x=[R[a][i]['primary'] for i in ids]; y=[R[b][i]['primary'] for i in ids]
    sd=lambda r,i: {R[r][i]['primary'],R[r][i].get('secondary')}>={'state','dynamics'}
    strad_each=[sum(sd(r,i) for i in ids) for r in (a,b)]
    both=[i for i in ids if R[a][i]['primary']==R[b][i]['primary']]
    diffsec=sum(1 for i in both if R[a][i].get('secondary')!=R[b][i].get('secondary'))
    anysec=[sum(1 for i in ids if R[r][i].get('secondary')) for r in (a,b)]
    sdconf=sum(1 for i in ids if {R[a][i]['primary'],R[b][i]['primary']}=={'state','dynamics'})
    print(name,'primary agree/kappa',kappa(x,y),'| state<->dynamics labelled by rater (primary+secondary):',strad_each,'| primaries split state/dynamics:',sdconf,'| any secondary:',anysec,'| none:',x.count('none'),y.count('none'),'| agreed primary but different secondary:',diffsec,'of',len(both))
print(len(ids),'items')
arm('norule1','norule2','NO RULE'); arm('rule1','rule2','RULE   ')
