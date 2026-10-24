# E33: page inventory from the registered rule (see the plan). Output: ../../page-inventory.md and e33.json
import sys,re,json,collections,os
sys.path.insert(0,'../e15')
import e15
S=('model','controller')
V={s:e15.parse(e15.NEW[s]) for s in S}
tabs={}                      # name -> dict(scopes, body)
for s in S:
    for t,b in V[s]['tables'].items():
        d=tabs.setdefault(t,dict(scopes=set(),body=''))
        d['scopes'].add(s); d['body']+=' '+b
typing={t:{s:e15.typing(V[s],t) for s in tabs[t]['scopes']} for t in tabs}
lookup={t for t in tabs if all(typing[t][s]['lookup'] for s in typing[t])}
life={t for t in tabs if any(typing[t][s]['life'] for s in typing[t])}
fk={t:set(re.findall(r'REFERENCES\s+"?(\w+)',tabs[t]['body']))-{t} for t in tabs}
noun=lambda t:t.split('_')[0]
nonlook=[t for t in tabs if t not in lookup]
# R1
grp={t:noun(t) for t in nonlook}
G=collections.defaultdict(list)
for t,g in grp.items(): G[g].append(t)
# R2: small groups without life merge into the single ancestor noun
merged={}
for g in sorted(G,key=lambda g:len(G[g])):
    ts=G[g]
    if len(ts)>=3 or any(t in life for t in ts): continue
    tgt=set()
    for t in ts:
        for p in fk[t]:
            if p in lookup or noun(p)==g: continue
            tgt.add(noun(p))
    if len(tgt)==1:
        merged[g]=next(iter(tgt))
for g,to in merged.items():
    for t in G[g]: grp[t]=to
G=collections.defaultdict(list)
for t,g in grp.items(): G[g].append(t)
# R3: lookups
lk={}
for l in lookup:
    c=collections.Counter(grp[t] for t in nonlook if l in fk[t])
    lk[l]=sorted(c.items(),key=lambda x:(-x[1],x[0]))[0][0] if c else None
for l,g in lk.items():
    if g: G[g].append(l)
# views
views={}
for s in S:
    for v,sql in V[s]['views'].items():
        m=[t for t in tabs if re.search(r'\b'+re.escape(t)+r'\b',sql)]
        first=min(m,key=lambda t:sql.find(t)) if m else None
        views[v]=grp.get(first) or lk.get(first)
# R4 facets (E26b reading: tables anywhere with the facet token as first or last token, other token being another group's name)
groupnames=set(G)
cand=collections.defaultdict(set)
for t in nonlook:
    toks=t.split('_')
    if len(toks)<2: continue
    for f,o in ((toks[0],toks[-1]),(toks[-1],toks[0])):
        if o in groupnames and o!=f: cand[f].add(o)
facet_loose={f:sorted(o) for f,o in cand.items() if len(o)>=3}
# R4' (tuning after seeing results): the facet token must not name an entity group (a group with a life table or at least 10 tables),
# and at least 3 of the groups it attaches to must carry a life table
lifegroups={g for g,ts in G.items() if any(t in life for t in ts)}
entitygroups={g for g,ts in G.items() if any(t in life for t in ts) or len([t for t in ts if t not in lookup])>=10}
facet={f:sorted(o) for f,o in cand.items() if len(o)>=3 and f not in entitygroups and len([x for x in o if x in lifegroups])>=3}
# attachments (E29): table whose noun differs from its single life ancestor's noun
def lifeanc(t,seen=()):
    out=set()
    for p in fk[t]:
        if p in lookup or p in seen: continue
        out|= {p} if p in life else lifeanc(p,seen+(t,))
    return out
attach=collections.defaultdict(list)
for t in nonlook:
    if t in life: continue
    a=lifeanc(t)
    if len(a)==1:
        an=noun(next(iter(a)))
        if noun(t)!=an and grp[t]!=grp.get(next(iter(a))): attach[grp.get(next(iter(a)),an)].append(t)
# exposure
R=json.load(open('../e30/e30_roots.json')); VM=json.load(open('../e30/viewmap.json'))
exp=collections.defaultdict(lambda:collections.defaultdict(int))
t2g={t:grp[t] for t in nonlook}
t2g.update({l:g for l,g in lk.items() if g})
for r in R:
    ts=set(r['tables'] or [])
    for t in list(ts):
        if t in VM: ts|=set(VM[t])
    gs={t2g[t] for t in ts if t in t2g}
    kind=r['kind']; tier=r['tier'] if kind=='facade' else kind
    for g in gs: exp[g][tier]+=1
def tier_of(g):
    e=exp.get(g,{})
    if e.get('client'): return 'client'
    if e.get('agent') or e.get('controller'): return 'agent/controller'
    if e.get('http'): return 'http'
    if e.get('hook'): return 'hook'
    return 'none'
pages={'machine':['machine'],'application':['application'],'unit':['unit'],'relation':['relation'],'storage':['storage'],'model':['model'],'secret':['secret'],
 'charm':['charm'],'resource-charm':['resource'],'action':['operation'],'offer':['offer'],'constraint':['constraint'],'status':['status'],'space':['space'],
 'subnet':['subnet'],'zone':['availability'],'cloud':['cloud'],'credential':['cloud'],'user':['user'],'controller':['controller'],'ssh-key':['user'],'access':['permission'],'agent':['agent']}
pg={}
for p,gs in pages.items():
    for g in gs: pg.setdefault(g,[]).append(p)
out={}
for g,ts in G.items():
    n=sum(1 for t in ts if t not in lookup)
    out[g]=dict(tables=sorted(ts),n=n,life=sorted(t for t in ts if t in life),merged_from=sorted(k for k,v in merged.items() if v==g),
      facet=facet.get(g),attachments=sorted(attach.get(g,[])),tier=tier_of(g),exposure=dict(exp.get(g,{})),pages=pg.get(g,[]))
json.dump(dict(groups=out,merged=merged,facets=facet,views=views,unassigned=[l for l,g in lk.items() if not g]),open('e33.json','w'),indent=1)
big=[g for g,d in out.items() if d['n']>=3 or d['life']]
print('tables non-lookup',len(nonlook),'lookups',len(lookup),'groups',len(out),'groups>=3 or life',len(big),'merged by R2',merged)
print('lookups unassigned',[l for l,g in lk.items() if not g])
print('facets, R4 as registered (E26b reading):',len(facet_loose),sorted(facet_loose));print('facets, R4-prime:',facet)
sizes=sorted(out.items(),key=lambda x:-x[1]['n'])
print('largest:',[(g,d['n']) for g,d in sizes[:12]])
small=[g for g,d in out.items() if d['n']<3 and not d['life']]
print('small groups left (<3, no life):',len(small),sorted(small))

# ---- reports
matched=[(g,d) for g,d in out.items() if d['pages']]
print('\nI3a: groups matched to existing pages',len(matched),'exposed',sum(1 for g,d in matched if d['tier']!='none'),[(g,d['tier'],d['pages']) for g,d in matched])
pageless=[(g,d['n'],d['tier']) for g,d in out.items() if (d['n']>=3 or d['life']) and not d['pages']]
print('I3b: groups >=3 tables or life with no page:',sorted(pageless,key=lambda x:-x[1]))
unexp=[(g,d['n']) for g,d in out.items() if (d['n']>=3 or d['life']) and d['tier']=='none']
print('I3c: unexposed groups >=3 tables:',unexp)
pages_without_group=[p for p,gs in pages.items() if not any(g in out for g in gs)]
print('pages with no group:',pages_without_group)
L=['# Proposed page inventory (generated, 4.1, session 79)','',
 'Generated by `experiments/e33/e33.py` from the rule registered in `structure-discovery-plan.md` (E33): R1 first token of the table name, R2 merge small groups into their single parent noun, R3 lookups and views follow their referrers, R4-prime facets (tuning after seeing results). Exposure comes from the E30 call graph (over-approximates through interface dispatch; misses the control socket, the CLI-to-server hop and function values). Read as a draft for review, not as a decision.','',
 '## Facets (pages across entities)','']
for f,o in facet.items(): L.append(f'- **{f}**: attaches to {", ".join(o)}')
L+=['','## Noun groups','','| group | tables | life tables | exposure | existing page | attachments (other nouns) | merged in |','|---|---|---|---|---|---|---|']
for g,d in sorted(out.items(),key=lambda x:-x[1]['n']):
    L.append(f"| {g} | {d['n']} | {', '.join(d['life']) or ''} | {d['tier']} | {', '.join(d['pages'])} | {', '.join(d['attachments'][:6])}{' ...' if len(d['attachments'])>6 else ''} | {', '.join(d['merged_from'])} |")
open('../../page-inventory.md','w').write('\n'.join(L)+'\n')

# ---- supplementary signal (post hoc, labelled): noun addressing as in E20b
import glob
SRC=os.path.expanduser('~/git/misc/juju-v2-preview')
VERBS=set('add remove list show set get update create delete change grant revoke enable disable attach detach register unregister import export find retry resolve switch use run cancel wait expose unexpose download upload scale refresh consume suspend resume bind trust info destroy kill trace debug dump login logout whoami'.split())
def fold(w):
    w=w.lower()
    for suf in ('manager','client'):
        if w.endswith(suf) and len(w)>len(suf)+2: w=w[:-len(suf)]
    return w[:-1] if w.endswith('s') and not w.endswith('ss') else w
cmdn=set()
for f in glob.glob(SRC+'/cmd/juju/**/*.go',recursive=True):
    if f.endswith('_test.go'): continue
    for m in re.finditer(r'Name:\s+"([a-z][a-z0-9-]+)"',open(f).read()):
        for t in m.group(1).split('-'):
            if t not in VERBS: cmdn.add(fold(t))
fac={fold(d) for d in os.listdir(SRC+'/apiserver/facades/client')}
addressed=lambda g: fold(g) in cmdn|fac
print('\nnoun-addressed groups (>=3 tables or life):',[(g,addressed(g)) for g,d in sorted(out.items(),key=lambda x:-x[1]['n']) if d['n']>=3 or d['life']])
for g,d in out.items(): d['addressed']=addressed(g)
json.dump(dict(groups=out,merged=merged,facets=facet,views=views),open('e33.json','w'),indent=1)
