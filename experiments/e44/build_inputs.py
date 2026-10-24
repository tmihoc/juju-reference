"""E44: build reader jobs (prompts) for question set A or B.
Conditions: W whole page, H heading chunks top 3, F fixed 500-char chunks top 3.
Versions: base, pattern. Runs: 1..3. One job per (page, question, version,
condition, run). Output: experiments/judges/io/e44_reader_jobs_<set>.jsonl"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import chunk

HERE = os.path.dirname(os.path.abspath(__file__))
IO = os.path.expanduser("~/git/misc/juju-reference/experiments/judges/io")
TEMPLATE = open(os.path.expanduser("~/git/misc/juju-reference/experiments/judges/reader44.txt")).read()
RUNS = 3
HDR_W = "DOCUMENTATION (one page):"
HDR_C = ("DOCUMENTATION EXCERPTS retrieved from one page for this question (they may be incomplete; "
         "answer from them only):")

def build(setname):
    qfile = {"A": "e44_questions.json", "B": "e44_questions_b.json"}[setname]
    qs = json.load(open(f"{IO}/{qfile}"))
    pages = {(v, p): open(f"{HERE}/pages/{v}/{p}.md").read()
             for v in ("base", "pattern") for p in ("machine", "controller", "access", "ssh-key")}
    jobs = []
    for q in qs:
        for v in ("base", "pattern"):
            text = pages[(v, q["page"])]
            body = {"W": (HDR_W, chunk.strip_front_matter(text))}
            h, _ = chunk.retrieve(q["question"], chunk.heading_chunks(text))
            body["H"] = (HDR_C, "\n---\n".join(h))
            f, _ = chunk.retrieve(q["question"], chunk.fixed_chunks(text))
            body["F"] = (HDR_C, "\n---\n".join(f))
            for cond, (hdr, doc) in body.items():
                prompt = TEMPLATE.replace("{DOC_HEADER}", hdr).replace("{DOC}", doc).replace("{QUESTION}", q["question"])
                for r in range(1, RUNS + 1):
                    jobs.append({"job": f"{setname}|{q['page']}|{q['id']}|{v}|{cond}|{r}", "set": setname,
                                 "page": q["page"], "qid": q["id"], "version": v, "cond": cond, "run": r,
                                 "prompt": prompt})
    out = f"{IO}/e44_reader_jobs_{setname}.jsonl"
    with open(out, "w") as fh:
        for j in jobs:
            fh.write(json.dumps(j) + "\n")
    return jobs

if __name__ == "__main__":
    for s in sys.argv[1:] or ["A", "B"]:
        jobs = build(s)
        chars = sum(len(j["prompt"]) for j in jobs)
        print(s, "jobs", len(jobs), "prompt chars", chars, "~tokens", chars // 4)
