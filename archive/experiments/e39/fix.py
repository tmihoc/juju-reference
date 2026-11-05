# applies the E39 fixes to the shared instruments (idempotent)
import re
p='../e15/e15.py'; s=open(p).read()
old="lookup=bool(V['seeds'].get(t)) and cols(body)<=3)"
new="lookup=bool(V['seeds'].get(t)) and cols(body)<=3 and not re.search(r'\\buuid\\b[^,()]*PRIMARY KEY|PRIMARY KEY\\s*\\(\\s*uuid',body))"
assert old in s or new in s
s=s.replace(old,new)
open(p,'w').write(s)
# lead-table rule: prefer the table named like the page
for p,old,new in (('../e33/e35.py',"lead=sorted(G,key=lambda t:(-indeg[t],len(t),t))[0] if G else None","lead=(name.replace('-','_') if name.replace('-','_') in G else sorted(G,key=lambda t:(-indeg[t],len(t),t))[0]) if G else None"),
                  ('../e37/e37.py',"lead=sorted(G,key=lambda t:(-indeg[t],len(t),t))[0]","lead=name.replace('-','_') if name.replace('-','_') in G else sorted(G,key=lambda t:(-indeg[t],len(t),t))[0]")):
    s=open(p).read(); assert old in s or new in s,p; open(p,'w').write(s.replace(old,new))
print('fixes applied')
