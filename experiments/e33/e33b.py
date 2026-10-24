import sys,re,json,collections,os,glob
sys.path.insert(0,'../e15'); sys.path.insert(0,'../e17')
import e15
import io,contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import e17
SRC=os.path.expanduser('~/git/misc/juju-v2-preview')
S=('model','controller')
V={s:e15.parse(e15.NEW[s]) for s in S}
tabs={}
for s in S:
    for t,b in V[s]['tables'].items():
        d=tabs.setdefault(t,dict(scopes=set(),body='')); d['scopes'].add(s); d['body']+=' '+b
typing={t:{s:e15.typing(V[s],t) for s in tabs[t]['scopes']} for t in tabs}
lookup={t for t in tabs if all(typing[t][s]['lookup'] for s in typing[t])}-{'space'}   # 'space' is a record (defect in the heuristic, E33)
life={t for t in tabs if any(typing[t][s]['life'] for s in typing[t])}
fk={t:set(re.findall(r'REFERENCES\s+"?(\w+)',tabs[t]['body']))-{t} for t in tabs}
nonlook=[t for t in tabs if t not in lookup]
EXCL={'removal','export','modelimport','recovery','schema','testing'}
files=[f for f in glob.glob(SRC+'/domain/*/state/**/*.go',recursive=True) if not f.endswith('_test.go') and 'mock' not in f]
ins=collections.defaultdict(collections.Counter); ref=collections.defaultdict(collections.Counter)
names=sorted(tabs,key=len,reverse=True)
pat=re.compile(r'\b('+'|'.join(map(re.escape,names))+r')\b')
for f in files:
    d=f.split('/domain/')[1].split('/')[0]
    if d in EXCL: continue
    t=open(f).read()
    for m in re.finditer(r'INSERT\s+(?:OR\s+\w+\s+)?INTO\s+"?(\w+)',t):
        if m.group(1) in tabs: ins[m.group(1)][d]+=1
    for m in re.finditer(r'(?:FROM|JOIN|UPDATE)\s+"?(\w+)',t):
        if m.group(1) in tabs: ref[m.group(1)][d]+=1
owner={};how={}
tt={}
for d,r in e17.dom.items():
    for x in r['tabs']: tt.setdefault(x.split(':')[1],d)
def pick(t):
    c=ins.get(t) or collections.Counter()
    if not c: 
        c=ref.get(t) or collections.Counter()
        if c: how[t]='refs'
    else: how[t]='insert'
    if not c: return None
    top=max(c.values()); cands=[d for d,v in c.items() if v==top]
    if len(cands)>1:
        fi=t.split('_')[0]
        pref=[d for d in cands if d==fi or fi.startswith(d) or d.startswith(fi)]
        if pref: cands=pref
        else:
            r=ref.get(t) or collections.Counter(); cands.sort(key=lambda d:-r.get(d,0))
    return cands[0]
for t in nonlook:
    o=pick(t)
    if o is None:
        o=tt.get(t); how[t]='fallback'
    owner[t]=o
grp=collections.defaultdict(list)
for t,o in owner.items(): grp[o].append(t)
# lookups
shared=[];lkowner={}
for l in lookup:
    refs=[t for t in nonlook if l in fk[t]]
    c=collections.Counter(owner.get(t) for t in refs)
    if refs and c.most_common(1)[0][1]>len(refs)/2: lkowner[l]=c.most_common(1)[0][0]
    else: shared.append(l)
for l,o in lkowner.items(): grp[o].append(l)
json.dump(dict(owner=owner,how=how,groups={g:sorted(ts) for g,ts in grp.items()},shared=sorted(shared)),open('e33b.json','w'),indent=1)
fb=[t for t in nonlook if how[t]=='fallback']; none=[t for t in nonlook if owner[t] is None]
print('non-lookup',len(nonlook),'by insert',sum(1 for t in nonlook if how[t]=='insert'),'by refs',sum(1 for t in nonlook if how[t]=='refs'),'fallback',len(fb),'unowned',len(none))
print('groups',len(grp),'shared vocabulary lookups',len(shared),sorted(shared))
# criterion 1
dest={'model_migration':'modelmigration','secret_backend':'secretbackend','cloud_credential':'credential','cloud_image_metadata':'cloudimagemetadata','cloud_defaults':'modeldefaults','cloud_region_defaults':'modeldefaults',
 'agent_binary_store':'agentbinary','agent_stream':'modelagent','agent_version':'modelagent','ssh_connection_request':'ssh','machine_virtual_ssh_host_key':'ssh','permission':'access','permission_object_access':'access','model_last_login':'access','upgrade_info':'upgrade','model_authorized_keys':'keymanager','model_storage_pool':'storage','storage_kind':'storage','machine_filesystem':'storage','machine_volume':'storage','provider_space':'network','provider_subnet':'network','provider_network':'network','provider_network_subnet':'network','provider_ip_address':'network','provider_link_layer_device':'network','space':'network','application_remote_offerer':'crossmodelrelation','application_remote_offerer_status':'crossmodelrelation','application_remote_offerer_relation_macaroon':'crossmodelrelation','application_remote_consumer':'crossmodelrelation','application_resource':'resource','model_secret_backend':'secretbackend','log_transfer_progress':'modelmigration','model_migrating':'modelmigration'}
ok=0;miss=[]
for t,d in dest.items():
    o=owner.get(t) or lkowner.get(t) or ('shared' if t in shared else None)
    if t.startswith('model_migration'): o=owner.get(t)
    if o==d: ok+=1
    else: miss.append((t,o,d))
print('criterion 1 (checked tables with a stated destination):',ok,'/',len(dest),'= %.0f%%'%(100*ok/len(dest)))
print('misses:',miss)
big=sorted(((g,len(ts)) for g,ts in grp.items()),key=lambda x:-x[1]); print('largest groups:',big[:14]); print('small:',[x for x in big if x[1]<3])
