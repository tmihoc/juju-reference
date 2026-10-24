import json,re,random,os
D=json.load(open('../e37/fn_stm.json'))
tables=open('../e37/tables.txt').read().split()
alt='|'.join(sorted(tables,key=len,reverse=True))
rI=re.compile(r'INSERT\s+(?:OR\s+\w+\s+)?INTO\s+"?('+alt+r')\b',re.I); rD=re.compile(r'DELETE\s+FROM\s+"?('+alt+r')\b',re.I); rU=re.compile(r'\bUPDATE\s+"?('+alt+r')\b',re.I); rT=re.compile(r'\b('+alt+r')\b')
def body(pos):
    f,line,col=pos.rsplit(':',2); lines=open(f).read().split('\n')
    off=sum(len(l)+1 for l in lines[:int(line)-1])+int(col)-1
    txt=open(f).read(); i=txt.find('{',off)
    if i<0: return ''
    d=0
    for j in range(i,len(txt)):
        if txt[j]=='{': d+=1
        elif txt[j]=='}':
            d-=1
            if d==0: return txt[off:j+1]
    return txt[off:]
random.seed(39)
sample=random.sample([d for d in D if d['tables']],30)
bad=[];rows=[]
for d in sample:
    b=body(d['pos'])
    src=dict(ins=sorted(set(m.lower() for m in rI.findall(b))),del_=sorted(set(m.lower() for m in rD.findall(b))),upd=sorted(set(m.lower() for m in rU.findall(b))),tab=sorted(set(rT.findall(b))))
    comp=dict(ins=sorted(d['ins'] or []),del_=sorted(d['del'] or []),upd=sorted(d['upd'] or []),tab=sorted(d['tables']))
    diff={k:(sorted(set(comp[k])-set(src[k])),sorted(set(src[k])-set(comp[k]))) for k in comp}
    ok=all(not a and not b for a,b in diff.values())
    rows.append((d['name'].split('/')[-1][:60],ok,{k:v for k,v in diff.items() if v[0] or v[1]}))
    if not ok: bad.append(rows[-1])
print(f'Z7: {len(bad)} of 30 functions differ between the compiled constants and the source text ({100*len(bad)/30:.0f}%); limit 5% (needs adjudication)')
for n,ok,df in bad: print('  ',n,df)
json.dump(rows,open('z7.json','w'),indent=1)
