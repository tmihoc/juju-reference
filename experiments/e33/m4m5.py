import json,re,os,glob,collections
man=json.load(open('page-manifest.json')); home={t:p for p,d in man['pages'].items() for t in d['tables']}
SRC=os.path.expanduser('~/git/misc/juju-v2-preview')
# M5
pages={'machine':'machine','application':'application','unit':'unit','relation':'relation','storage':'storage','model':'model','secret':'secret','charm':'charm','resource-charm':'resource','action':'action',
 'offer':'offer','constraint':'constraint','status':'status','space':'space','subnet':'subnet','zone':'zone','cloud':'cloud','credential':'credential','user':'user','controller':'controller','ssh-key':'ssh-key','access':'permission','agent':None}
ok=[p for p,m in pages.items() if m in man['pages']]
print('M5: existing pages mapping to a manifest page:',len(ok),'/',len(pages),'| no page:',[p for p,m in pages.items() if m not in man['pages']])
print('  (agent is the page about the agent program; it has no table group)')
print('  of the five the first-word rule could not match (status, space, zone, access, agent):',[(p,pages[p] in man['pages']) for p in ('status','space','zone','access','agent')])
# M4 fallback for new tables
new=json.load(open('../e15/e15_result.json')); newt=set(new['model']['added'])|set(new['controller']['added'])
topic={}
for s in ('model','controller'):
    for f in sorted(glob.glob(f'{SRC}/domain/schema/{s}/sql/*.sql')):
        b=re.sub(r'\.PATCH','',re.sub(r'^\d+-','',os.path.basename(f)))[:-4]
        for t in re.findall(r'CREATE TABLE (\w+)',open(f).read()): topic.setdefault(t,[]).append((s,b))
DEFAULT=json.load(open('page-manifest.json'))  # not used
import importlib.util,sys
sys.path.insert(0,'.')
fb={}
files=collections.defaultdict(list)
for t,l in topic.items():
    for x in l: files[x].append(t)
exec(open('manifest.py').read().split("DEFAULT={")[1].split("}\nOVERRIDE")[0].join(["DEFAULT={","}"]))
for t in sorted(newt):
    if t not in home: continue
    cands=[]
    for x in topic.get(t,[]):
        others=[o for o in files[x] if o!=t and o in home and o not in newt]
        c=collections.Counter(home[o] for o in others)
        if c: cands.append(c.most_common(1)[0][0])
    page=cands[0] if cands else DEFAULT.get(t.split('_')[0])
    fb[t]=(page,'file' if cands else 'first word')
json.dump(fb,open('m4_fallback.json','w'),indent=1)
print('M4 fallback for',len(fb),'new tables; manifest agreement:',sum(1 for t,(p,h) in fb.items() if home[t]==p),'/',len(fb))
for t,(p,h) in fb.items(): print(f'  {t:40s} fallback={p:18s} ({h}) manifest={home[t]}')
