"""E43 reading rule (pre-registered): a level on which the E35 judge, the E43
judge and the E41 rule agree is code-supported at this evidence; a split is open.
section-ish: E35 leg, E43 of, E41 'section of X'. page-ish: E35 character,
E43 own, E41 page. Mechanism / process / across carry no level and are listed."""
import json,collections
IO='../judges/io'
n43={r['name']:r for r in json.load(open(f'{IO}/e43_out.json'))}
e35={r['name']:r['verdict'] for r in json.load(open(f'{IO}/e35_judge_out.json'))}
rule={g:r['level'] for g,r in json.load(open('../e41/e41_result.json')).items()}
def lv35(v): return {'leg':'S','character':'P'}.get(v,'-')
def lv43(l): return {'of':'S','own':'P'}.get(l,'-')
def lvr(l): return 'S' if l.startswith('section') else 'P'
rows=[]
for n in n43:
    a,b,c=lv35(e35.get(n,'')),lv43(n43[n]['label']),lvr(rule[n]) if n in rule else '-'
    rows.append((n,a,b,c))
three=[r for r in rows if '-' not in r[1:]]
agree=[r for r in three if len({r[1],r[2],r[3]})==1]
print('items with a level in all three instruments:',len(three))
print('all three agree: %d  (S %d, P %d)'%(len(agree),sum(r[1]=='S' for r in agree),sum(r[1]=='P' for r in agree)))
print('  S:',[r[0] for r in agree if r[1]=='S'])
print('  P:',len(agree),'P items (not listed)') if False else None
print('\nsplit (open):')
for r in sorted(three,key=lambda r:r[0]):
    if len({r[1],r[2],r[3]})>1: print('  %-22s E35=%s E43=%s rule=%s  E43parent=%s'%(r[0],r[1],r[2],r[3],n43[r[0]].get('parent')))
nolevel=[(r[0],e35.get(r[0]),n43[r[0]]['label'],rule.get(r[0])) for r in rows if '-' in r[1:]]
print('\nno level in at least one instrument:')
for x in nolevel: print('  ',x)
json.dump(dict(agree=[r[0] for r in agree],split=[r[0] for r in three if len({r[1],r[2],r[3]})>1],nolevel=[x[0] for x in nolevel]),open('e43_concord.json','w'),indent=1)
