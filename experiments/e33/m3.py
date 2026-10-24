import json,re,collections,sys,glob,os
sys.path.insert(0,'../e15')
import e15
man=json.load(open('page-manifest.json'))
home={t:p for p,d in man['pages'].items() for t in d['tables']}
S=('model','controller'); V={s:e15.parse(e15.NEW[s]) for s in S}
tabs={}
for s in S:
    for t,b in V[s]['tables'].items(): tabs.setdefault(t,'')
    for t,b in V[s]['tables'].items(): tabs[t]+=' '+b
fk={t:set(re.findall(r'REFERENCES\s+"?(\w+)',b))-{t} for t,b in tabs.items()}
nonlook=set(home)
edges=[(t,p) for t in nonlook for p in fk[t] if p in nonlook]
def share(part): 
    return sum(1 for a,b in edges if part.get(a) and part.get(a)==part.get(b)),len(edges)
firstword={t:t.split('_')[0] for t in nonlook}
e33=json.load(open('e33.json'))['groups']; r1={t:g for g,x in e33.items() for t in x['tables'] if t in nonlook}
b=json.load(open('e33b.json')); wd={t:o for t,o in b['owner'].items() if t in nonlook}
SRC=os.path.expanduser('~/git/misc/juju-v2-preview'); topic={}
for s in S:
    for f in sorted(glob.glob(f'{SRC}/domain/schema/{s}/sql/*.sql')):
        n=re.sub(r'\.PATCH','',re.sub(r'^\d+-','',os.path.basename(f)))[:-4]
        for t in re.findall(r'CREATE TABLE (\w+)',open(f).read()): topic.setdefault(t,n)
for name,part in (('manifest',home),('first word (R1 with merges)',r1),('first word (plain)',firstword),('writer domain (E33b)',wd),('schema topic file',topic)):
    a,n=share(part); print('%-30s intra %3d / %3d = %.1f%%  groups %d'%(name,a,n,100*a/n,len(set(part.get(t) for t in nonlook))))

print('\n--- edges kept by R1 (with merges) but cut by the manifest, and the reverse')
cut=[(a,b) for a,b in edges if r1.get(a)==r1.get(b) and home[a]!=home[b]]
gain=[(a,b) for a,b in edges if r1.get(a)!=r1.get(b) and home[a]==home[b]]
print('cut',len(cut)); 
for a,b in sorted(cut): print('  ',a,'->',b,'|',home[a],'/',home[b])
print('gained',len(gain))
for a,b in sorted(gain): print('  ',a,'->',b,'|',home[a])
print('\n--- all foreign keys the manifest cuts, by page pair')
c=collections.Counter((home[a],home[b]) for a,b in edges if home[a]!=home[b])
for (x,y),n in c.most_common(25): print(f'  {x} -> {y}: {n}')
