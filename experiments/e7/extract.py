# Extract statements from the pilot pages, tagged with the part they sit in.
import re, json, random, sys
pages = sys.argv[1:]
PART = [('data model','state'),('change streams','observation'),('agent','agent'),('workers','agent'),('operations','dynamics')]
out=[]
for p in pages:
    s=open(p).read()
    s=re.sub(r'^---.*?---\n','',s,flags=re.S)
    s=re.sub(r'```\{ggarch\}.*?```','',s,flags=re.S)
    s=re.sub(r'```\{ibnote\}.*?```','',s,flags=re.S)
    s=re.sub(r'```\{list-table\}.*?```','',s,flags=re.S)
    part='identity'; sub=None
    for blk in re.split(r'\n\s*\n',s):
        for line in blk.split('\n'):
            m=re.match(r'^(#{2,3}) (.*)',line)
            if m:
                if m.group(1)=='##':
                    t=m.group(2).lower()
                    part=next((v for k,v in PART if k in t),'identity')
                continue
        if blk.strip().startswith('#') or blk.strip().startswith('(') and blk.strip().endswith(')='):
            continue
        # bullets: one statement per top-level or nested bullet line
        for line in blk.split('\n'):
            l=line.strip()
            if not l or l.startswith('#') or re.match(r'^\(.*\)=$',l) or l.startswith(':') or l.startswith('```'): continue
            txt=re.sub(r'^[-*]\s+','',l)
            txt=re.sub(r'^\d+\.\s+','',txt)
            if re.match(r'^\*?(Related errors?|Trigger)',txt) or txt.startswith('*Related error'): continue
            if '*Trigger:*' in txt: continue   # errors are classified with their rule
            if txt.endswith(':') and len(txt)<60: continue
            txt=re.sub(r'\{ref\}`([^`<]*?)\s*<[^>]*>`',r'\1',txt)
            txt=re.sub(r'\{ref\}`([^`]*)`',r'\1',txt)
            txt=txt.replace('**','').replace('*Rule:*','Rule:')
            if len(txt)<40: continue
            out.append({'page':p.split('/')[-1],'filed':part,'text':txt})
json.dump(out,open('/tmp/claude-1000/-home-dora-git-juju/a9d923a1-5ac4-4320-a949-6663e0ff977c/scratchpad/all.json','w'),indent=1)
from collections import Counter
print(Counter((o['page'],o['filed']) for o in out))
