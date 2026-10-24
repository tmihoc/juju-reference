# layer 1b (unregistered extension): a --flag atom must be registered as a flag, not just occur as a string.
import sys,subprocess,re,glob,os
sys.path.insert(0,'../e16')
import e16
FL=set()
for f,t in e16.TXT.items():
    for m in re.finditer(r'\.(?:String|Bool|Int|Duration|Var|StringVar|BoolVar|IntVar|DurationVar|Uint|UintVar|Float64Var)\w*\([^"\n]*"([a-z][\w-]*)"',t): FL.add(m.group(1))
    for m in re.finditer(r'gnuflag\.\w+\([^"\n]*"([a-z][\w-]*)"',t): FL.add(m.group(1))
print('registered flag names:',len(FL))
files=subprocess.run(['git','-C',e16.SRC,'ls-tree','--name-only','upstream/4.1','docs/reference/'],capture_output=True,text=True).stdout.split()
bad=[];n=0
for f in files:
    if not f.endswith('.md'): continue
    md=subprocess.run(['git','-C',e16.SRC,'show',f'upstream/4.1:{f}'],capture_output=True,text=True).stdout
    md=re.sub(r'\{[a-z:]+\}`[^`\n]*`','',md); md=re.sub(r'```.*?```','',md,flags=re.S)
    for a in e16.atoms(md):
        if a.startswith('--'):
            n+=1
            if a[2:] not in FL: bad.append((f.split('/')[-1],a))
print('--flag atoms:',n,'not a registered flag:',bad)
