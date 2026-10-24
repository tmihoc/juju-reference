import re,json,random,sys,glob,os
random.seed(7)
OUT='/tmp/claude-1000/-home-dora-git-juju/a9d923a1-5ac4-4320-a949-6663e0ff977c/scratchpad/'
# corpus A: layered pages
base=os.path.expanduser('~/git/misc/juju-entity-ref/docs/reference/')
pages=['access','application','cloud','credential','machine','model','relation','secret','space','subnet','unit','user','storage','offer','charm','action','ssh-key','zone']
A=[]
for p in pages:
    s=open(base+p+'.md').read()
    s=re.sub(r'^---.*?---\n','',s,flags=re.S)
    for pat in [r'```\{ggarch\}.*?```',r'```\{ibnote\}.*?```',r'```\{list-table\}.*?```',r'```\{figure\}.*?```']:
        s=re.sub(pat,'',s,flags=re.S)
    layer='lede'; items=[]
    for line in s.split('\n'):
        m=re.match(r'^## (.*)',line)
        if m:
            t=m.group(1).lower()
            layer=next((k for k in ['declaration','persistence','execution'] if k in t),'other-heading')
            continue
        l=line.strip()
        if not l or l.startswith('#') or re.match(r'^\(.*\)=$',l) or l.startswith(':') or l.startswith('```'): continue
        t=re.sub(r'^[-*]\s+','',l); t=re.sub(r'^\d+\.\s+','',t)
        if '*Trigger:*' in t or t.startswith('*Related error'): continue
        if t.endswith(':') and len(t)<60: continue
        t=re.sub(r'\{ref\}`([^`<]*?)\s*<[^>]*>`',r'\1',t); t=re.sub(r'\{ref\}`([^`]*)`',r'\1',t)
        t=t.replace('**','').replace('*Rule:*','Rule:')
        if len(t)<50: continue
        items.append({'corpus':'A','source':p,'layer':layer,'text':t})
    A+=random.sample(items,min(7,len(items)))
# corpus B: Go package docs
B=[]
for f in sorted(glob.glob(os.path.expanduser('~/git/misc/juju-v2-preview/domain/*/doc.go'))):
    lines=[l for l in open(f).read().split('\n') if l.startswith('//')]
    paras=[];cur=[]
    for l in lines:
        t=l[2:]
        if t.startswith('\t') or t.strip().startswith(('+','|')) or t.strip().startswith('Copyright') or t.strip().startswith('Licensed'):
            if cur: paras.append(' '.join(cur)); cur=[]
            continue
        t=t.strip()
        if not t or t.startswith('#'):
            if cur: paras.append(' '.join(cur)); cur=[]
            continue
        cur.append(t)
    if cur: paras.append(' '.join(cur))
    paras=[re.sub(r'^Package \w+ ','The package ',p) for p in paras if len(p)>70 and not p.startswith('See ') and 'github.com' not in p[:60]]
    name=f.split('/')[-2]
    for p in paras: B.append({'corpus':'B','source':name,'layer':None,'text':p})
B=random.sample(B,min(80,len(B)))
items=A+B; random.shuffle(items)
for i,o in enumerate(items): o['id']=i+1
json.dump(items,open(OUT+'e8_sample.json','w'),indent=1)
json.dump([{'id':o['id'],'text':o['text']} for o in items],open(OUT+'e8_items.json','w'),indent=1)
print(len(A),len(B),len(items))
