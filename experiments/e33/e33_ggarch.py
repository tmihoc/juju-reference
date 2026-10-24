import re,sys
def hand_edges(path):
    t=open(path).read(); out=set()
    for m in re.finditer(r'(\w+)\s*->\s*(\w+)\s*\[[^\]]*ground:\s*"model:(\w+)\.(\w+)"',t):
        if not m.group(1).startswith('life_'): out.add((m.group(1),m.group(2),m.group(4)))
    return out
def scaffold_edges(path):
    t=open(path).read(); out=set()
    for m in re.finditer(r'(\w+)\.(\w+)\s*->\s*(\w+)\.(\w+)\s*\[type:\s*data',t): out.add((m.group(1),m.group(3),m.group(2)))
    return out
if __name__=='__main__':
    S=sys.argv[1]
    hand=hand_edges('/home/dora/git/misc/juju-v2-preview/docs/machine.ggarch'); gen=scaffold_edges(S+'machine_scaffold.ggarch')
    nodes={x for e in hand for x in e[:2]}
    inter=hand&gen
    print('hand edges',len(hand),'generated edges',len(gen))
    print('recall of the hand-written data edges: %d / %d = %.0f%%'%(len(inter),len(hand),100*len(inter)/len(hand)))
    gin={e for e in gen if e[0] in nodes and e[1] in nodes}
    print('precision over the shared node set: %d / %d = %.0f%%'%(len(gin&hand),len(gin),100*len(gin&hand)/max(1,len(gin))))
    print('hand edges missed:',sorted(hand-gen)); print('generated among hand nodes but not hand:',sorted(gin-hand))
