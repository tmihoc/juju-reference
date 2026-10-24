"""E44: select 12 questions per page from the verified set A (4 lookup,
4 mechanism, 2 failure, 2 unanswerable), by a fixed rule: drop the questions
listed in DROPS, then take the first N of each type in id order. Corrected key
facts from the verifier replace the author's text. Set B (independent writer)
is kept separate in questions_b.json."""
import json, os
IO = os.path.expanduser("~/git/misc/juju-reference/experiments/judges/io")
PAGES = ["machine", "controller", "access", "ssh-key"]
NEED = {"lookup": 4, "mechanism": 4, "failure": 2, "unanswerable": 2}
DROPS = {
    ("machine", "A-Q16"): "answerable via the generic start-instance retry (10 retries, 10 s), verifier: exists",
    ("machine", "A-Q07"): "ground truth states the wrong order (machiner EnsureDead precedes the provisioner step); verifier: partly",
    ("ssh-key", "A-Q08"): "ground truth overstates: in 4.1 the keys reach only the bootstrap machine and the provisioning script; verifier: partly",
}
sel, qb, dropped = [], [], []
for p in PAGES:
    inp = json.load(open(f"{IO}/e44_verify_in_{p}.json"))
    out = {x["id"]: x for x in json.load(open(f"{IO}/e44_verify_out_{p}.json"))}
    taken = {t: 0 for t in NEED}
    for q in inp:
        o = out[q["id"]]
        for k in o["key_fact_verdicts"]:
            if k["verdict"] == "partly" and k["corrected"]:
                q["key_facts"][k["fact_index"]] = k["corrected"]
        q["page"] = p
        q["verifier"] = o["ground_truth_verdict"]
        if q["id"].startswith("B-"):
            qb.append(q); continue
        if (p, q["id"]) in DROPS:
            dropped.append({"page": p, "id": q["id"], "reason": DROPS[(p, q["id"])]}); continue
        t = q["type"]
        if taken[t] < NEED[t]:
            taken[t] += 1; sel.append(q)
json.dump(sel, open(f"{IO}/e44_questions.json", "w"), indent=1)
json.dump(qb, open(f"{IO}/e44_questions_b.json", "w"), indent=1)
json.dump(dropped, open(f"{IO}/e44_dropped.json", "w"), indent=1)
print(len(sel), len(qb), dropped)
for q in sel:
    files = ",".join(sorted({e["file"] for e in q["evidence"]}))
    print(q["page"], q["id"], q["type"][:4], "X" if q.get("cross_area") else "-", q["question"][:90], "|", files[:150])
