import re,glob,os,json,collections
SRC=os.path.expanduser('~/git/misc/juju-v2-preview')
PAT=re.compile(r'CanRead|CanWrite|CanAdmin|HasPermission|Authoriz|authorizer|checkCan|canRead|canWrite|canAdmin|IsSuperUser|HasModel|HasControllerPermission|AuthClient|AuthController|check\w*Permission|checkAccess|assertCan|mustHave|requireAdmin|authFunc',re.I)
def body(txt,start):
    i=txt.index('{',start); d=0
    for j in range(i,len(txt)):
        if txt[j]=='{': d+=1
        elif txt[j]=='}':
            d-=1
            if d==0: return txt[i:j+1]
    return txt[i:]
rows=[];perfacade=collections.defaultdict(lambda:[0,0])
for f in glob.glob(SRC+'/apiserver/facades/client/**/*.go',recursive=True):
    if f.endswith('_test.go') or 'mock' in f or '/params' in f: continue
    t=open(f).read()
    helpers={m.group(1):body(t,m.start()) for m in re.finditer(r'^func (?:\([^)]*\) )?([a-z]\w*)\(',t,flags=re.M)}
    for m in re.finditer(r'^func \((\w+) \*?(\w+)\) ([A-Z]\w*)\((?:ctx|_)\s+context\.Context',t,flags=re.M):
        name=m.group(3)
        if name in('Close','Stop','Kill','Wait'): continue
        b=body(t,m.start()); ok=bool(PAT.search(b))
        if not ok:
            for h,hb in helpers.items():
                if re.search(r'\b'+h+r'\(',b) and PAT.search(hb): ok=True;break
        fac=f.split('/facades/client/')[1].split('/')[0]
        rows.append(dict(facade=fac,type=m.group(2),method=name,ok=ok,file=f[len(SRC)+1:],line=t[:m.start()].count('\n')+1))
        perfacade[fac][0]+=ok;perfacade[fac][1]+=1
n=len(rows);ok=sum(r['ok'] for r in rows)
print('methods',n,'with authority statement',ok,'=%.0f%%'%(100*ok/n))
for k,(a,b) in sorted(perfacade.items(),key=lambda x:x[1][0]-x[1][1]): 
    if a<b: print(' ',k,a,'/',b)
json.dump(rows,open('authority.json','w'),indent=1)
