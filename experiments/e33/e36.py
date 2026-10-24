import sys,re,os,glob,json,subprocess,collections
sys.path.insert(0,'../e15')
import e15
SRC=os.path.expanduser('~/git/misc/juju-v2-preview')
man=json.load(open('page-manifest.json')); J={x['name']:x for x in json.load(open('e35_judge_out.json'))}
V={s:e15.parse(e15.NEW[s]) for s in ('model','controller')}
body={}
for s in V:
    for t,b in V[s]['tables'].items(): body[t]=body.get(t,'')+' '+b
def cols(t):
    b=body[t]; n=0
    for part in re.split(r',\s*(?![^()]*\))',b):
        p=part.strip()
        if p and not re.match(r'(PRIMARY|FOREIGN|UNIQUE|CHECK|CONSTRAINT)\b',p): n+=1
    return n
VERBS=set('add remove list show set get update create delete change grant revoke enable disable attach detach register unregister import export find retry resolve switch use run cancel wait expose unexpose download upload scale refresh consume suspend resume bind trust info destroy kill trace debug dump login logout whoami'.split())
def fold(w):
    w=w.lower()
    for suf in ('manager','client'):
        if w.endswith(suf) and len(w)>len(suf)+2: w=w[:-len(suf)]
    return w[:-1] if w.endswith('s') and not w.endswith('ss') else w
cmds=set()
for f in glob.glob(SRC+'/cmd/juju/**/*.go',recursive=True)+glob.glob(SRC+'/cmd/plugins/**/*.go',recursive=True):
    if f.endswith('_test.go'): continue
    for m in re.finditer(r'Name:\s+"([a-z][a-z0-9-]+)"',open(f).read()): cmds.add(m.group(1))
hooks=[re.sub(r'\.go$','',os.path.basename(f)) for f in glob.glob(SRC+'/internal/worker/uniter/runner/jujuc/*.go') if not f.endswith('_test.go')]
FACMAP={'keymanager':'ssh-key','spaces':'space','subnets':'subnet','storage':'storage','applicationoffers':'offer','action':'action','secrets':'secret','secretbackends':'secret-backend','machinemanager':'machine','modelmanager':'model','modelconfig':'model','usermanager':'user','cloud':'cloud','controller':'controller','application':'application','credentialmanager':'credential','charms':'charm','resources':'resource','block':'block-command','annotations':'annotation','imagemetadatamanager':'image-metadata','highavailability':'controller'}
facm=collections.Counter()
for f in glob.glob(SRC+'/apiserver/facades/client/**/*.go',recursive=True):
    if f.endswith('_test.go') or 'mock' in f: continue
    d=f.split('/facades/client/')[1].split('/')[0]
    if d not in FACMAP: continue
    for m in re.finditer(r'^func \((\w+) \*?(\w+)\) ([A-Z]\w*)\((?:ctx|_)\s+context\.Context',open(f).read(),flags=re.M): facm[FACMAP[d]]+=1
def ops(p):
    toks=[fold(t) for t in p.split('-')]; comp='-'.join(toks)
    n=0
    for c in cmds:
        ct=[fold(t) for t in c.split('-') if t not in VERBS]
        if (len(toks)==1 and toks[0] in ct) or (len(toks)>1 and comp in '-'.join(fold(t) for t in c.split('-'))): n+=1
    for h in hooks:
        ht=[fold(t) for t in h.split('-')]
        if (len(toks)==1 and toks[0] in ht) or (len(toks)>1 and comp in '-'.join(ht)): n+=1
    return n+facm.get(p,0)
mass={};mass2={}
for p,d in man['pages'].items():
    if not d['tables']: continue
    ts=d['tables']; lv=0
    for l in d['lookups']:
        for s in V:
            lv+=len(V[s]['seeds'].get(l,[])) if l in V[s]['tables'] else 0
    watched=sum(1 for t in ts for s in V if t in V[s]['tables'] and e15.typing(V[s],t)['watched'])
    o=ops(p)
    mass[p]=len(ts)+lv+watched+o
    mass2[p]=mass[p]+sum(cols(t) for t in ts)
# upstream page length
words={}
for p,alias in {'machine':'machine','application':'application','unit':'unit','relation':'relation','storage':'storage','model':'model','secret':'secret','charm':'charm','resource':'resource-charm','action':'action','offer':'offer','constraint':'constraint','space':'space','subnet':'subnet','zone':'zone','cloud':'cloud','credential':'credential','user':'user','controller':'controller','ssh-key':'ssh-key'}.items():
    t=subprocess.run(['git','-C',SRC,'show',f'upstream/4.1:docs/reference/{alias}.md'],capture_output=True,text=True).stdout
    words[p]=len(re.sub(r'```.*?```','',t,flags=re.S).split())
HOWTO={'action','application','resource','charm','cloud','controller','credential','machine','image-metadata','model','offer','relation','secret-backend','secret','space','ssh-key','storage','subnet','unit','user'}
kind={p:J[p]['verdict'] for p in mass if p in J}
def auc(pos,neg,m):
    c=0;n=0
    for a in pos:
        for b in neg:
            n+=1; c+= 1 if m[a]>m[b] else 0.5 if m[a]==m[b] else 0
    return c/n
chars=[p for p,k in kind.items() if k=='character']; legs=[p for p,k in kind.items() if k=='leg']
def rank(xs):
    s=sorted(range(len(xs)),key=lambda i:xs[i]); r=[0]*len(xs); i=0
    while i<len(s):
        j=i
        while j+1<len(s) and xs[s[j+1]]==xs[s[i]]: j+=1
        for k in range(i,j+1): r[s[k]]=(i+j)/2+1
        i=j+1
    return r
def spearman(a,b):
    ra,rb=rank(a),rank(b); n=len(a); ma=sum(ra)/n; mb=sum(rb)/n
    num=sum((x-ma)*(y-mb) for x,y in zip(ra,rb)); den=(sum((x-ma)**2 for x in ra)*sum((y-mb)**2 for y in rb))**.5
    return num/den
print('characters',len(chars),'legs',len(legs))
print('mass by page:',sorted(mass.items(),key=lambda x:-x[1]))
print('\n(1) AUC mass separating characters from legs: %.2f (composite 2 with columns: %.2f)'%(auc(chars,legs,mass),auc(chars,legs,mass2)))
ex=[p for p in words if p in mass]
print('(2) Spearman mass vs upstream page words over %d pages: %.2f (composite 2: %.2f)'%(len(ex),spearman([mass[p] for p in ex],[words[p] for p in ex]),spearman([mass2[p] for p in ex],[words[p] for p in ex])))
med_c=sorted(mass[p] for p in chars)[len(chars)//2]; med_l=sorted(mass[p] for p in legs)[len(legs)//2]
print('(3) median mass: characters',med_c,'legs',med_l)
for p in ('link-layer-device','object-store'): print('   large leg',p,mass[p],'above character median' if mass[p]>med_c else 'not above character median')
for p in ('permission','image-metadata','block-command'): print('   small character',p,mass[p],'below leg median' if mass[p]<med_l else 'not below leg median')
cw=[p for p in chars if p in HOWTO]; lw=[p for p in legs if p in HOWTO]
print('(4) lifecycle story (how-to) among characters: %d/%d = %.0f%%; among legs: %d/%d = %.0f%%'%(len(cw),len(chars),100*len(cw)/len(chars),len(lw),len(legs),100*len(lw)/len(legs)))
allp=chars+legs
def best(clf):
    best=0
    for th in sorted(set(clf.values())):
        acc=sum(1 for p in allp if (clf[p]>=th)==(p in HOWTO))/len(allp); best=max(best,acc)
    return best
life={p:1 if J[p].get('own_lifecycle','').lower().startswith('yes') else 0 for p in allp}
print('   classifier accuracy for how-to presence: judge own-lifecycle %.2f | mass (best threshold) %.2f | judge kind (character) %.2f'%(best(life),best(mass),best({p:1 if kind[p]=='character' else 0 for p in allp})))
json.dump(dict(mass=mass,mass2=mass2,words=words,kind=kind,howto=sorted(HOWTO)),open('e36_result.json','w'),indent=1)
print('\nlegs with how-to:',lw); print('characters without how-to:',[p for p in chars if p not in HOWTO])
