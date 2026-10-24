"""Every citation in skeleton-v6.md outside the 'missing piece', 'Open' and change
sections is a settled row written bare, or a partial row written with a star;
falsified and open rows are never cited there (E40 rule)."""
import json,re,sys
from pathlib import Path
R={r['id']:r['status'] for r in json.load(open(Path(__file__).with_name('ledger.json')))}
txt=(Path(__file__).resolve().parents[2]/'skeleton-v6.md').read_text().split('\n')
ok={'supported','user','convention'}
sec='';bad=[]
for i,l in enumerate(txt,1):
    if l.startswith('## '): sec=l
    if sec.startswith(('## Rules with a missing piece','## Open','## What changed','## Not carried')): continue
    for c,star in re.findall(r'\b(C\d\d)(\*?)',l):
        st=R.get(c)
        if st in ok and not star: continue
        if st=='partial' and star: continue
        bad.append((i,c+star,st,sec[:30]))
print('violations:',len(bad))
for b in bad: print(' ',b)
sys.exit(1 if bad else 0)
