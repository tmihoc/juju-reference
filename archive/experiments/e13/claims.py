# E13 out-of-sample recall: extract claims from the upstream/4.1 reference pages (written before the skeleton work).
import re,subprocess,json,sys
OUT='/tmp/claude-1000/-home-dora-git-juju/a9d923a1-5ac4-4320-a949-6663e0ff977c/scratchpad/'
def page(p): return subprocess.run(['git','-C','/home/dora/git/misc/juju-v2-preview','show',f'upstream/4.1:docs/reference/{p}.md'],capture_output=True,text=True).stdout
def clean(s):
    s=re.sub(r'^---.*?---\n','',s,flags=re.S)
    s=re.sub(r'```\{(ggarch|ibnote|figure)\}.*?```','',s,flags=re.S)
    s=re.sub(r'```.*?```','',s,flags=re.S)
    s=re.sub(r'\{ref\}`([^`<]*?)\s*<[^>]*>`',r'\1',s); s=re.sub(r'\{ref\}`([^`]*)`',r'\1',s)
    s=re.sub(r'\[([^\]]*)\]\([^)]*\)',r'\1',s)
    return s.replace('**','')
res={}
for p in sys.argv[1:]:
    s=clean(page(p)); claims=[]
    for b in re.split(r'\n\s*\n',s):
        lines=[l for l in b.split('\n') if l.strip() and not l.strip().startswith(('#','(',':','|','!['))]
        para=[];cur=''
        for l in lines:
            st=l.strip()
            if re.match(r'^([-*]|\d+\.)\s',st):
                if cur: para.append(cur)
                cur=re.sub(r'^([-*]|\d+\.)\s+','',st)
            else: cur=(cur+' '+st).strip()
        if cur: para.append(cur)
        for pp in para:
            for t in re.split(r'(?<=[.!?])\s+(?=[A-Z`])',pp):
                t=t.strip()
                if len(t)>=35 and t[-1] in '.!?:' or (len(t)>=35 and '`' in t): claims.append(t)
    res[p]=claims
    json.dump([{'id':i+1,'claim':c} for i,c in enumerate(claims)],open(f'{OUT}e13_{p}.json','w'),indent=1)
    print(p,len(claims))
