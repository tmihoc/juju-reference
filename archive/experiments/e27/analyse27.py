import json,glob,os,re,collections,sys
S='/tmp/claude-1000/-home-dora-git-juju/8c1e4c6e-570b-417b-bc47-eea27d0d6ac3/scratchpad/'
SRC=os.path.expanduser('~/git/misc/juju-v2-preview')
rows=[]
for f in sorted(glob.glob(S+'e27_out*.json')):
    rows+=json.load(open(f))
claims={}
for f in glob.glob(S+'e27_batch*.json'):
    for c in json.load(open(f)): claims[c['key']]=c
c=collections.Counter(r['verdict'] for r in rows)
print('judged',len(rows),dict(c),'of',len(claims),'claims; missing',len(set(claims)-{r['key'] for r in rows}))
dec=[r for r in rows if r['verdict'] in('holds','overstated','wrong','outdated')]
fail=[r for r in dec if r['verdict']!='holds']
print('decidable',len(dec),'failing',len(fail),'= %.0f%%'%(100*len(fail)/max(1,len(dec))))
ok=tot=0;bad=[]
for r in rows:
    e=r.get('evidence')
    if not e: continue
    for part in re.split(r'[;,]\s*',e) if isinstance(e,str) else e:
        m=re.match(r'([\w./-]+):(\d+)',part.strip())
        if not m: continue
        tot+=1; p=os.path.join(SRC,m.group(1))
        if os.path.isfile(p) and len(open(p,errors='ignore').read().split('\n'))>=int(m.group(2)): ok+=1
        else: bad.append(part)
print('citations resolving',ok,'/',tot,'= %.0f%%'%(100*ok/max(1,tot)),bad[:5])
per=collections.defaultdict(lambda:collections.Counter())
for r in rows: per[r['key'].split(':')[0]][r['verdict']]+=1
for p,v in per.items(): print(p,dict(v))
json.dump(fail,open('e27_failing.json','w'),indent=1)
