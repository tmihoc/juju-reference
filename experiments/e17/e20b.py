import re,glob,os,json
SRC=os.path.expanduser('~/git/misc/juju-v2-preview')
VERBS=set('add remove list show set get update create delete change grant revoke enable disable attach detach register unregister import export find retry resolve switch use run cancel wait expose unexpose download upload scale refresh consume offer suspend resume bind trust config info destroy kill trace debug dump status login logout whoami'.split())-{'offer','status','config'}
def fold(w):
    w=w.lower()
    for suf in ('manager','client'): 
        if w.endswith(suf) and len(w)>len(suf)+2: w=w[:-len(suf)]
    return w[:-1] if w.endswith('s') and not w.endswith('ss') else w
cmdn=set()
for f in glob.glob(SRC+'/cmd/juju/**/*.go',recursive=True):
    if f.endswith('_test.go'): continue
    for m in re.finditer(r'Name:\s+"([a-z][a-z-]+)"',open(f).read()):
        for t in m.group(1).split('-'):
            if t not in VERBS: cmdn.add(fold(t))
fac={fold(d) for d in os.listdir(SRC+'/apiserver/facades/client')}
P=json.load(open('pages.json')); pn={fold(k) for k in P}|{fold(w) for k in P for w in k.split('-')}
pages=list(P)
hit=[p for p in pages if fold(p) in cmdn|fac or any(fold(w) in cmdn|fac for w in p.split('-'))]
print('pages with a matching interface noun:',len(hit),'/',len(pages),'; misses:',[p for p in pages if p not in hit])
print('interface nouns without a page:',sorted((cmdn|fac)-pn))
print('command nouns',len(cmdn),'covered by a page',len(cmdn&pn))
