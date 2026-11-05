# E14: summarise the close-scrutiny verdicts on the 68 claims that E13 left as not derivable or contradicted.
# Inputs here: e14_batch1..5.json (the claims, with the E13 residue kind), e14_out1..5.json (the judges' output).
import json,collections,glob,os,re
HERE=os.path.dirname(os.path.abspath(__file__))
SRC=os.path.expanduser('~/git/misc/juju-v2-preview/')
rows=[]
for f in sorted(glob.glob(HERE+'/e14_out*.json')): rows+=json.load(open(f))
claims={}
for f in sorted(glob.glob(HERE+'/e14_batch*.json')):
    for c in json.load(open(f)): claims[c['key']]=c
print(len(rows),'claims scrutinised')
print('verdicts',dict(collections.Counter(r['verdict'] for r in rows)))
print('reference_worthy',dict(collections.Counter(r.get('reference_worthy') for r in rows)))
by=collections.defaultdict(collections.Counter)
for r in rows: by[claims[r['key']]['prior_kind']][r['verdict']]+=1
for k,c in by.items(): print(' ',k,dict(c))
ok=sum(1 for r in rows if r.get('evidence') and re.match(r'(.+?):(\d+)',r['evidence']) and (os.path.exists(SRC+re.match(r'(.+?):',r['evidence']).group(1)) or os.path.exists(os.path.expanduser('~/go/pkg/mod/'+re.match(r'(.+?):',r['evidence']).group(1)))))
print('evidence citations resolving to a real file:',ok)
for r in rows:
    if r['verdict'] in('wrong','overstated','outdated'):
        print(f"[{r['verdict']}] {r['key']} | {claims[r['key']]['claim'][:110]}\n   -> {(r.get('correction') or '')[:160]} @ {r.get('evidence')}")
