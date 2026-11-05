import re,json,math,collections
Q=[
("Q1","What does the error `machine constraint violation` mean, and what should I do about it?",
 ["constraints are set on a machine whose recorded cloud instance has a different architecture from the one required","only architecture is compared","require the architecture the machine has, or request a new machine"]),
("Q2","Reprovisioning a machine fails with `machine agent is still present`. Why, and what should I do?",
 ["the machine agent still reports presence","stop the agent or confirm the machine is lost"]),
("Q3","Can a controller machine or a container be reprovisioned?",
 ["no: a controller machine or a container is not eligible (errors `machine is a controller machine`, `machine is a container`)","only an alive, provider-provisioned machine that hosts no containers qualifies"]),
("Q4","Under what conditions does a machine become dead?",
 ["only when it is dying","and hosts no containers, units or storage"]),
("Q5","What does the error `machine not provisioned` mean?",
 ["an action that needs the cloud instance ran before the cloud reported an instance ID","wait until the compute provisioner has recorded the instance"]),
("Q6","Which container types can I name in a machine designation in Juju 4.1?",
 ["only lxd","another type fails with `invalid container type`"]),
("Q7","What does the machine designation `0/lxd/4` refer to?",
 ["the existing LXD container 4 on machine 0"]),
("Q8","How many levels deep can containers be nested, and what happens if I go deeper?",
 ["one level","a deeper name is refused with `machine name \"<name>\" has too many containers`"]),
("Q9","What drives the compute provisioner, i.e. what triggers it to provision machines?",
 ["the model machines change stream / watcher","it monitors unprovisioned machines"]),
("Q10","I remove a machine that still hosts units. What happens, and which error might I see?",
 ["the machine is marked dying","it does not become dead while it still hosts units","`machine has units`: remove or move the units first"]),
("Q11","What does the error `grandparent machine are not supported currently` mean?",
 ["the reboot logic found a machine whose parent itself has a parent","name validation refuses containers nested deeper than one level, so it guards an unsupported layout","no remediation"]),
("Q12","Which record holds a machine's hardware details (CPU, memory, root disk), and what else does it hold?",
 ["the cloud instance record","also arch, virtualisation type, availability zone and the creation state (instance id empty until the cloud reports it)"]),
("Q13","Who writes a machine's status?",
 ["the machine agent reports the health status (pending, started, stopped, error)","the controller and the providers/container broker write the provisioning status (allocating, running, provisioning error)"]),
("Q14","What happens to relation settings of the units on a machine that is reprovisioned?",
 ["the units depart their relation scopes","their settings are archived so the remaining units see a consistent departure"]),
("Q15","Which parts of Juju, besides the machine code, read a machine's cloud instance record?",
 ["removal, status, storage provisioning, network, model migration, recovery and agent passwords (not in the layered page: score separately)"]),
("Q16","How many containers can a single host machine run?",
 ["NOT STATED on the page: the correct answer says the documentation does not say; any specific number is fabricated"]),
("Q17","Does the reprovision request accept a force option to skip the liveness checks?",
 ["NOT STATED on the page: the correct answer says the documentation does not say; asserting a force option or its absence as fact is fabricated"]),
]
json.dump(Q,open('questions.json','w'),indent=1)
def toks(t): return re.findall(r"[a-z0-9_`]+",t.lower())
def chunks(text,size=800,ov=100):
    out=[];i=0
    while i<len(text):
        out.append(text[i:i+size]); i+=size-ov
    return out
def retrieve(question,cs,k=4):
    df=collections.Counter()
    ct=[collections.Counter(toks(c)) for c in cs]
    for c in ct:
        for w in c: df[w]+=1
    N=len(cs); qt=toks(question)
    def score(c):
        return sum((1+math.log(c[w]))*math.log(1+N/df[w]) for w in set(qt) if w in c)
    ranked=sorted(range(N),key=lambda i:-score(ct[i]))[:k]
    return [cs[i] for i in sorted(ranked)]
pages={'pr':open('/tmp/llmbuild-pr/reference/machine.md').read(),'pilot':open('/tmp/llmbuild/reference/machine.md').read()}
HEAD="""You are a documentation assistant. Answer each question using ONLY the documentation provided. If the documentation does not contain the answer, say exactly "The documentation does not say." and do not guess. Be concise (1-3 sentences). Do NOT use any tools and do NOT read any files. Reply with ONLY a JSON object mapping each question id to your answer string.
"""
for name,txt in pages.items():
    # whole page mode
    qs="\n".join(f"{qid}. {q}" for qid,q,_ in Q)
    open(f'{name}-whole.txt','w').write(HEAD+"\nDOCUMENTATION (one page):\n\n"+txt+"\n\nQUESTIONS:\n"+qs+"\n")
    cs=chunks(txt)
    parts=[]
    for qid,q,_ in Q:
        top=retrieve(q,cs)
        parts.append(f"### {qid}. {q}\nRetrieved documentation excerpts for this question:\n"+"\n---\n".join(top))
    open(f'{name}-chunk.txt','w').write(HEAD+"\nFor each question below you are given excerpts retrieved from the documentation (they may be incomplete). Answer from the excerpts only.\n\n"+"\n\n".join(parts)+"\n")
    print(name,'chars',len(txt),'chunks',len(cs))
import os
for f in sorted(os.listdir('.')):
    if f.endswith('.txt'): print(f,os.path.getsize(f))
