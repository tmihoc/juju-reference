import re,json,random,os
random.seed(11)
OUT='/tmp/claude-1000/-home-dora-git-juju/a9d923a1-5ac4-4320-a949-6663e0ff977c/scratchpad/'
base=os.path.expanduser('~/git/misc/juju-entity-ref/docs/reference/')
pages=['bundle','constraint','placement-directive','resource-charm','script','high-availability','scaling','status','watcher','controller','removing-things','configuration','hook','resource-compute']
old={o['text'] for o in json.load(open(OUT+'e8_sample.json'))}
items=[]
for p in pages:
    s=open(base+p+'.md').read()
    s=re.sub(r'^---.*?---\n','',s,flags=re.S)
    for pat in [r'```\{ggarch\}.*?```',r'```\{ibnote\}.*?```',r'```\{list-table\}.*?```',r'```\{figure\}.*?```',r'```.*?```']:
        s=re.sub(pat,'',s,flags=re.S)
    cand=[]
    for line in s.split('\n'):
        l=line.strip()
        if not l or l.startswith('#') or re.match(r'^\(.*\)=$',l) or l.startswith(':') or l.startswith('|') or l.startswith('!['): continue
        t=re.sub(r'^[-*]\s+','',l); t=re.sub(r'^\d+\.\s+','',t)
        if '*Trigger:*' in t or t.startswith('*Related error'): continue
        if t.endswith(':') and len(t)<60: continue
        t=re.sub(r'\{ref\}`([^`<]*?)\s*<[^>]*>`',r'\1',t); t=re.sub(r'\{ref\}`([^`]*)`',r'\1',t)
        t=t.replace('**','').replace('*Rule:*','Rule:')
        if len(t)<70 or t in old: continue
        cand.append({'source':p,'text':t})
    items+=random.sample(cand,min(8,len(cand)))
random.shuffle(items)
for i,o in enumerate(items): o['id']=i+1
json.dump(items,open(OUT+'e9_sample.json','w'),indent=1)
json.dump([{'id':o['id'],'text':o['text']} for o in items],open(OUT+'e9_items.json','w'),indent=1)
print(len(items))
