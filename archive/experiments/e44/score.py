"""E44 scoring (pre-registered criteria 1 to 6, amendment A2 'exposed' as main).
Answerable question score = fraction of key facts 'present'. Contradicted =
any key fact 'contradicted'. Unanswerable: correct = abstained and not invented.
Output: e44_result.json and a printed table."""
import collections, json, os, re, sys
IO = os.path.expanduser("~/git/misc/juju-reference/experiments/judges/io")
HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = ["machine", "controller", "access", "ssh-key"]

def load(p): return [json.loads(l) for l in open(p)]

def parse(text):
    m = re.search(r"\{.*\}", text, re.S)
    return json.loads(m.group(0)) if m else None

def rows(setname):
    qf = f"{IO}/e44_questions{'' if setname=='A' else '_b'}.json"
    qs = {(q["page"], q["id"]): q for q in json.load(open(qf))}
    jobs = {j["job"]: j for j in load(f"{IO}/e44_reader_jobs_{setname}.jsonl")}
    reader = {r["job"]: r["text"] for r in load(f"{IO}/e44_reader_out_{setname}.jsonl")}
    out, bad = [], []
    last = {}
    for g in load(f"{IO}/e44_grader_out_{setname}.jsonl"):
        try: d = parse(g["text"]); assert d is not None and "facts" in d; last[g["job"]] = d
        except Exception: last.setdefault(g["job"], None)
    for job, d in last.items():
        j = jobs[job]; q = qs[(j["page"], j["qid"])]
        g = {"job": job}
        if d is None: bad.append(job); continue
        n = len(q["key_facts"])
        facts = d.get("facts", [])
        if q["type"] == "unanswerable":
            # registered rule: correct only if the reader says the page does not say.
            # 'strict' (post hoc, reported beside it) also requires no invented specifics.
            score = 1.0 if d.get("abstained") else 0.0
            contra = 0
        else:
            if len(facts) != n: bad.append(g["job"] + " nfacts"); continue
            score = sum(1 for f in facts if f == "present") / n
            contra = 1 if any(f == "contradicted" for f in facts) else 0
        out.append({**{k: j[k] for k in ("page", "qid", "version", "cond", "run")}, "type": q["type"],
                    "exposure": q.get("exposure", "n/a"), "cross": bool(q.get("cross_area")),
                    "score": score, "contra": contra, "abstained": bool(d.get("abstained")), "strict": 1.0 if d.get("abstained") and not d.get("invented") else 0.0,
                    "invented": bool(d.get("invented"))})
    return out, bad

def mean(xs): xs = list(xs); return sum(xs) / len(xs) if xs else float("nan")

def agg(rs, **flt):
    sel = [r for r in rs if all(r[k] == v for k, v in flt.items())]
    return sel

def table(rs, label, flt=lambda r: True):
    rs = [r for r in rs if flt(r)]
    ans = [r for r in rs if r["type"] != "unanswerable"]
    un = [r for r in rs if r["type"] == "unanswerable"]
    res = {}
    print(f"--- {label}: {len(rs)} graded answers ({len(ans)} answerable, {len(un)} unanswerable)")
    print(f"{'cond':5}{'ver':9}{'score%':>8}{'contra%':>9}{'abstain%':>10}{'notstrict%':>11}")
    for c in "WHF":
        for v in ("base", "pattern"):
            a = [r for r in ans if r["cond"] == c and r["version"] == v]
            u = [r for r in un if r["cond"] == c and r["version"] == v]
            res[(c, v)] = dict(score=100 * mean(r["score"] for r in a), contra=100 * mean(r["contra"] for r in a),
                               abst=100 * mean(r["score"] for r in u), inv=100 * mean(1 - r["strict"] for r in u))
            x = res[(c, v)]
            print(f"{c:5}{v:9}{x['score']:8.1f}{x['contra']:9.1f}{x['abst']:10.1f}{x['inv']:11.1f}")
    return res

def criteria(rs, label, flt=lambda r: True):
    rs = [r for r in rs if flt(r)]
    ans = [r for r in rs if r["type"] != "unanswerable"]
    un = [r for r in rs if r["type"] == "unanswerable"]
    def d(c, key, pop):
        return mean(r[key] for r in pop if r["cond"] == c and r["version"] == "pattern") - \
               mean(r[key] for r in pop if r["cond"] == c and r["version"] == "base")
    out = {}
    out["c1_H_score_diff"] = 100 * d("H", "score", ans)
    out["c2_W_score_diff"] = 100 * d("W", "score", ans)
    out["c3_contra_diff_W/H/F"] = [100 * d(c, "contra", ans) for c in "WHF"]
    out["c4_abstain_diff_W/H/F"] = [100 * d(c, "score", un) for c in "WHF"]
    out["c4_strict_diff_W/H/F (post hoc)"] = [100 * d(c, "strict", un) for c in "WHF"]
    cnt = lambda c, v: sum(r["contra"] for r in ans if r["cond"] == c and r["version"] == v)
    out["c3_contra_answers_W/H/F_pattern_vs_base"] = {c: [cnt(c, "pattern"), cnt(c, "base")] for c in "WHF"}
    # per page and per run for H
    per_page = {p: 100 * d("H", "score", [r for r in ans if r["page"] == p]) for p in PAGES}
    per_run = {k: 100 * (mean(r["score"] for r in ans if r["cond"] == "H" and r["version"] == "pattern" and r["run"] == k) -
                         mean(r["score"] for r in ans if r["cond"] == "H" and r["version"] == "base" and r["run"] == k)) for k in (1, 2, 3)}
    out["c5_H_by_page"] = per_page; out["c5_H_by_run"] = per_run
    out["c5_pages_ge5"] = sum(1 for v in per_page.values() if v >= 5)
    out["c5_pages_positive"] = sum(1 for v in per_page.values() if v > 0)
    out["c5_runs_ge5"] = sum(1 for v in per_run.values() if v >= 5)
    out["c6_F_score_diff"] = 100 * d("F", "score", ans)
    out["W_by_page"] = {p: 100 * d("W", "score", [r for r in ans if r["page"] == p]) for p in PAGES}
    out["F_by_page"] = {p: 100 * d("F", "score", [r for r in ans if r["page"] == p]) for p in PAGES}
    print(f"=== criteria on {label}")
    for k, v in out.items():
        print(" ", k, json.dumps(v if not isinstance(v, float) else round(v, 1)))
    return out

if __name__ == "__main__":
    result = {}
    for s in ("A", "B"):
        rs, bad = rows(s)
        print(f"##### set {s}: parse/shape failures {len(bad)}", bad[:5])
        result[s] = {"bad": bad, "n": len(rs)}
        for label, flt in (("all", lambda r: True), ("exposed", lambda r: r["exposure"] == "exposed"),
                           ("internal", lambda r: r["exposure"] == "internal"),
                           ("cross_area", lambda r: r["cross"])):
            if s == "B" and label != "all": continue
            table(rs, f"set {s} {label}", flt)
            result[s][label] = criteria(rs, f"set {s} {label}", flt)
    json.dump(result, open(f"{HERE}/e44_result.json", "w"), indent=1, default=str)
