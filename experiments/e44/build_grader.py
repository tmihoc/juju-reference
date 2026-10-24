"""E44: build grader prompts from reader outputs. The grader prompt carries the
question, type, ground truth, key facts and the answer only (no page, version,
condition or run). Output: e44_grader_jobs_<set>.jsonl"""
import json, os, sys
IO = os.path.expanduser("~/git/misc/juju-reference/experiments/judges/io")
TEMPLATE = open(os.path.expanduser("~/git/misc/juju-reference/experiments/judges/grader44.txt")).read()
for s in sys.argv[1:]:
    qs = {(q["page"], q["id"]): q for q in json.load(open(f"{IO}/e44_questions{'' if s=='A' else '_b'}.json"))}
    jobs = {json.loads(l)["job"]: json.loads(l) for l in open(f"{IO}/e44_reader_jobs_{s}.jsonl")}
    n = 0
    with open(f"{IO}/e44_grader_jobs_{s}.jsonl", "w") as fh:
        for l in open(f"{IO}/e44_reader_out_{s}.jsonl"):
            r = json.loads(l); j = jobs[r["job"]]; q = qs[(j["page"], j["qid"])]
            kf = "\n".join(f"{i+1}. {k}" for i, k in enumerate(q["key_facts"])) or "(none: UNANSWERABLE)"
            typ = "UNANSWERABLE" if q["type"] == "unanswerable" else q["type"]
            p = (TEMPLATE.replace("{QUESTION}", q["question"]).replace("{TYPE}", typ)
                 .replace("{GROUND_TRUTH}", q["ground_truth"]).replace("{KEY_FACTS}", kf)
                 .replace("{ANSWER}", r["text"]))
            fh.write(json.dumps({"job": r["job"], "prompt": p}) + "\n"); n += 1
    print(s, n)
