import re,json,random,os,glob
random.seed(21)
OUT='/tmp/claude-1000/-home-dora-git-juju/a9d923a1-5ac4-4320-a949-6663e0ff977c/scratchpad/'
base=os.path.expanduser('~/git/misc/juju-entity-ref/docs/')
def clean(s):
    s=re.sub(r'^---.*?---\n','',s,flags=re.S)
    s=re.sub(r'```.*?```','',s,flags=re.S)
    s=re.sub(r'\{ref\}`([^`<]*?)\s*<[^>]*>`',r'\1',s); s=re.sub(r'\{ref\}`([^`]*)`',r'\1',s)
    s=re.sub(r'\[([^\]]*)\]\([^)]*\)',r'\1',s)
    s=s.replace('**','').replace('*Rule:*','Rule:')
    return s
def sentences(path):
    s=clean(open(path).read()); out=[]; err=[]
    blocks=re.split(r'\n\s*\n',s)
    for b in blocks:
        lines=[l for l in b.split('\n') if l.strip() and not l.strip().startswith('#') and not re.match(r'^\(.*\)=$',l.strip()) and not l.strip().startswith((':','|','!['))]
        # join hard-wrapped lines of one bullet/paragraph
        para=[];cur=''
        for l in lines:
            st=l.strip()
            if re.match(r'^([-*]|\d+\.)\s',st):
                if cur: para.append(cur)
                cur=re.sub(r'^([-*]|\d+\.)\s+','',st)
            else: cur=(cur+' '+st).strip()
        if cur: para.append(cur)
        for p in para:
            if '*Trigger:*' in p:
                err.append(p.replace('*Trigger:*','Trigger:').replace('*Remediation:*','Remediation:')); continue
            for t in re.split(r'(?<=[.!?])\s+(?=[A-Z`])',p):
                t=t.strip()
                if 60<=len(t)<=420 and t[-1] in '.!?' and t[0] not in '|<': out.append(t)
    return out,err
items=[];errs=[]
refpages=[f for f in glob.glob(base+'reference/**/*.md',recursive=True) if not f.endswith('index.md')]
random.shuffle(refpages)
for f in refpages[:70]:
    s,e=sentences(f); src='reference/'+os.path.relpath(f,base+'reference')
    for t in random.sample(s,min(3,len(s))): items.append({'corpus':'ref','source':src,'text':t})
    errs+=[{'corpus':'err','source':src,'text':x} for x in e]
for d,n in [('howto',1),('explanation',2)]:
    fs=[f for f in glob.glob(base+d+'/*.md') if not f.endswith('index.md')]
    random.shuffle(fs)
    for f in fs[:14]:
        s,_=sentences(f)
        for t in random.sample(s,min(n,len(s))): items.append({'corpus':d,'source':d+'/'+os.path.basename(f),'text':t})
items+=random.sample(errs,min(30,len(errs)))
random.shuffle(items)
for i,o in enumerate(items): o['id']=i+1
json.dump(items,open(OUT+'e10_sample.json','w'),indent=1)
json.dump([{'id':o['id'],'text':o['text']} for o in items],open(OUT+'e10_items.json','w'),indent=1)
import collections
print(len(items),collections.Counter(o['corpus'] for o in items),len(refpages))
