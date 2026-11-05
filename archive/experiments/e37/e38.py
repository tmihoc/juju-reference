import sys,re,os,json,collections
sys.path.insert(0,'../e15')
import e15
man=json.load(open('../e33/page-manifest.json'))
CARVE={'storage-pool':['storage_pool','storage_pool_attribute'],
 'relation-unit':['relation_unit','relation_unit_departure','relation_unit_setting','relation_unit_setting_archive','relation_unit_settings_hash'],
 'application-endpoint':['application_endpoint','application_extra_endpoint'],'application-scale':['application_scale'],
 'cloud-instance':['machine_cloud_instance','machine_cloud_instance_status','instance_tag'],'machine-placement':['machine_placement'],
 'unit-state':['unit_state','unit_state_charm','unit_state_relation']}
chunk={}
for p,d in man['pages'].items():
    for t in d['tables']: chunk[t]=p
carved=set(t for ts in CARVE.values() for t in ts)
for c,ts in CARVE.items():
    for t in ts: chunk[t]=c
chunks=sorted(set(chunk.values()))
def fkmap(ddl):
    V={s:e15.parse(ddl[s]) for s in ('model','controller')}
    body={}
    for s in V:
        for t,b in V[s]['tables'].items(): body[t]=body.get(t,'')+' '+b
    lookup={t for s in V for t in V[s]['tables'] if e15.typing(V[s],t)['lookup']}-{'space'}
    return {t:set(re.findall(r'REFERENCES\s+"?(\w+)',b))-{t} for t,b in body.items()},lookup
fk,lookup=fkmap(e15.NEW)
def structural(fk,chunk,lookup,only=None):
    ref=collections.defaultdict(set)
    for t,ps in fk.items():
        if t not in chunk or t in lookup: continue
        for p in ps:
            if p in chunk and p not in lookup and chunk[p]!=chunk[t]:
                if only is None or (t in only and p in only): ref[chunk[p]].add(chunk[t])
    return ref
S=structural(fk,chunk,lookup)
# behavioural
FACMAP={'keymanager':'ssh-key','spaces':'space','subnets':'subnet','storage':'storage','applicationoffers':'offer','action':'action','secrets':'secret','secretbackends':'secret-backend','machinemanager':'machine','modelmanager':'model','modelconfig':'model','usermanager':'user','cloud':'cloud','controller':'controller','application':'application','credentialmanager':'credential','charms':'charm','resources':'resource','block':'block-command','annotations':'annotation','imagemetadatamanager':'image-metadata','uniter':'unit','machine':'machine','provisioner':'machine','storageprovisioner':'storage','deployer':'unit','secretsmanager':'secret','crossmodelrelations':'offer','crosscontroller':'external-controller','migrationmaster':'model-migration','migrationtarget':'model-migration','upgrader':'agent-version','modelupgrader':'agent-version','controllerupgrader':'upgrade','usersecretsdrain':'secret','sshserver':'ssh','sshclient':'ssh','keyupdater':'ssh-key','lifeflag':'unit','diskmanager':'storage'}
R=json.load(open('e37_roots.json')); VM=json.load(open('../e30/viewmap.json'))
B=collections.defaultdict(set); unmapped=collections.Counter()
for r in R:
    if r['kind']!='facade': continue
    pkgd=r['pkg'].split('/')[-1]; P=FACMAP.get(pkgd)
    if not P: unmapped[pkgd]+=1; continue
    ts=set(r['tables'] or [])
    for t in list(ts):
        if t in VM: ts|=set(VM[t])
    for t in ts:
        g=chunk.get(t)
        if g and g!=P and t not in lookup: B[g].add(P)
rows={}
for g in chunks:
    s=sorted(S.get(g,())); b=sorted(B.get(g,())); u=sorted(set(s)|set(b))
    robust=len(s)<=1 and len(b)<=1 and len(u)<=1
    level='page' if len(u)!=1 else 'section of '+u[0]
    rows[g]=dict(structural=s,behavioural=b,union=u,level=level,robust_section=(len(u)==1 and robust),strength=('weak(behavioural)' if len(s)<2 and len(u)>=2 else 'structural' if len(s)>=2 else 'none'))
json.dump(rows,open('e38_result.json','w'),indent=1)
print('chunks',len(chunks),'unmapped facade pkgs',sum(unmapped.values()))
print('\n%-22s %-24s struct behav'%('chunk','level'))
for g,r in sorted(rows.items(),key=lambda x:(x[1]['level']=='page',x[0])):
    print('%-22s %-24s %2d %2d  %s | %s'%(g,r['level'],len(r['structural']),len(r['behavioural']),','.join(r['structural'][:4]),','.join(r['behavioural'][:4])))
print('\nPREDICTIONS')
ctrl=['application-scale','cloud-instance','machine-placement','unit-state']
print('(1) controls robust sections of parent:',[(c,rows[c]['level'],rows[c]['robust_section']) for c in ctrl],'->',sum(1 for c in ctrl if rows[c]['robust_section']),'/4')
hubs=['model','charm','machine','application','unit','cloud','controller','user']
print('(2) hubs are pages with >=2 structural referrers:',[(h,rows[h]['level'],len(rows[h]['structural'])) for h in hubs],'->',sum(1 for h in hubs if rows[h]['level']=='page' and len(rows[h]['structural'])>=2),'/8')
print('(3) port, telemetry:',[(c,rows[c]['level'],rows[c]['robust_section']) for c in ('port','telemetry')])
print('(4) storage-pool, relation-unit, application-endpoint:',[(c,rows[c]['level'],rows[c]['structural'],rows[c]['behavioural'][:5]) for c in ('storage-pool','relation-unit','application-endpoint')])
# (b) stability on 4.0.15
fk0,look0=fkmap(e15.OLD)
common={t for t in chunk if t in fk0 and t in fk}
S0=structural(fk0,chunk,look0,only=common); S1=structural(fk,chunk,lookup,only=common)
chg=set(json.load(open('../e15/e15_result.json'))['model']['changed_C'])|set(json.load(open('../e15/e15_result.json'))['controller']['changed_C'])
unchanged=[g for g in chunks if not any(t in chg for t in [t for t,c in chunk.items() if c==g])]
same=[g for g in unchanged if S0.get(g,set())==S1.get(g,set())]
print('\n(b) chunks with no changed table:',len(unchanged),'structural referrer set equal in 4.0.15 and 4.1:',len(same),'= %.0f%%'%(100*len(same)/len(unchanged)))
print('    differing:',[(g,sorted(S0.get(g,set())),sorted(S1.get(g,set()))) for g in unchanged if g not in same][:6])
