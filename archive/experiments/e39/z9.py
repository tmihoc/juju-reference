import sys,json,io,contextlib
import os; os.chdir('../e33'); sys.path.insert(0,'.')
with contextlib.redirect_stdout(io.StringIO()):
    import e35
R=e35.rows
# hand-verified truth, written from reading the command and hook tool names (juju CLI, plugins, jujuc): is the page's noun addressed by a command, a client facade or a hook tool?
TRUTH={'application':1,'unit':1,'machine':1,'relation':1,'storage':1,'model':1,'model-migration':1,'secret':1,'secret-backend':1,'charm':1,'resource':1,'action':1,'offer':1,'cloud':1,'credential':1,
 'model-defaults':1,'image-metadata':1,'controller':1,'upgrade':1,'user':1,'permission':1,'ssh-key':1,'ssh':1,'object-store':0,'agent-version':0,'space':1,'subnet':1,'zone':0,'link-layer-device':0,
 'external-controller':0,'constraint':1,'annotation':0,'block-command':1,'removal':0,'lease':0,'port':1,'telemetry':0,'database':0,'storage-pool':1}
bad=[];n=0
for p,r in R.items():
    if r is None or p not in TRUTH: continue
    n+=1; got=bool(r['a'] or r['a_hook'])
    if got!=bool(TRUTH[p]): bad.append((p,got,bool(TRUTH[p])))
print(f'Z9 address match: {len(bad)} of {n} pages differ from the hand-verified answer ({100*len(bad)/n:.0f}%); limit 10%'); print('   ',bad)
