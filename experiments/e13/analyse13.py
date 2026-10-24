import json,os,collections,re
SRC='/home/dora/git/misc/juju-v2-preview/'
pages=['machine','cloud','relation','secret']
tot=collections.Counter(); resid=collections.Counter(); art=collections.Counter(); bad=[]; per={}
for p in pages:
    claims={c['id']:c['claim'] for c in json.load(open(f'e13_{p}.json'))}
    out={o['id']:o for o in json.load(open(f'e13_out_{p}.json'))}
    c=collections.Counter(o['verdict'] for o in out.values()); per[p]=(len(claims),dict(c),len(out))
    for i,o in out.items():
        tot[o['verdict']]+=1
        if o['verdict'] in('derivable','partly'):
            art[o.get('artifact')]+=1
            ev=o.get('evidence') or ''
            m=re.match(r'(.+?):(\d+)',ev)
            ok=False
            if m and os.path.exists(SRC+m.group(1)):
                n=int(m.group(2)); L=open(SRC+m.group(1),errors='ignore').read().split('\n')
                ok= 0<n<=len(L)
            if not ok: bad.append((p,i,ev))
        else: resid[o.get('residue_kind')]+=1
n=sum(tot.values())
print('claims judged',n); print('verdicts',dict(tot)); print('recall (derivable)',round(tot['derivable']/n,2),'| derivable+partly',round((tot['derivable']+tot['partly'])/n,2))
for p,v in per.items(): print(p,v)
print('artifact classes licensing derivable/partly claims:',art.most_common())
print('residue kinds (not derivable or contradicted):',resid.most_common())
print('evidence citations that do not resolve to a real file:line:',len(bad),bad[:8])
