"""E44 chunkers and retrieval (pre-registered: heading chunks with heading path,
fixed 500-character chunks, top 3 by lexical overlap).

Lexical overlap is the BM25-like score used in experiments/agent-test/build.py
(tf-idf with log weights over the chunks of one page version), so the retrieval
is the same family as E9 and uses no model.
"""
import collections
import math
import re

TOP_K = 3
FIXED = 500


def strip_front_matter(text):
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + 5:].lstrip("\n")
    return text


def heading_chunks(text):
    """Split by markdown headings (levels 1 to 6, outside code fences).
    Each chunk is 'path > of > headings' plus the text up to the next heading.
    Chunks with no body text (heading only) are dropped."""
    text = strip_front_matter(text)
    chunks, path, buf, fence = [], [], [], False

    def flush():
        body = "\n".join(buf).strip()
        if body and path:
            chunks.append("[" + " > ".join(h for _, h in path) + "]\n" + body)
        elif body:
            chunks.append(body)

    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fence = not fence
        m = None if fence else re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            flush()
            buf = []
            level = len(m.group(1))
            while path and path[-1][0] >= level:
                path.pop()
            path.append((level, m.group(2).strip()))
        else:
            buf.append(line)
    flush()
    return chunks


def fixed_chunks(text, size=FIXED):
    text = strip_front_matter(text)
    return [text[i:i + size] for i in range(0, len(text), size)]


def toks(t):
    return re.findall(r"[a-z0-9_`]+", t.lower())


def retrieve(question, cs, k=TOP_K):
    ct = [collections.Counter(toks(c)) for c in cs]
    df = collections.Counter()
    for c in ct:
        for w in c:
            df[w] += 1
    n = len(cs)
    qt = set(toks(question))

    def score(c):
        return sum((1 + math.log(c[w])) * math.log(1 + n / df[w]) for w in qt if w in c)

    ranked = sorted(range(n), key=lambda i: (-score(ct[i]), i))[:k]
    return [cs[i] for i in sorted(ranked)], sorted(ranked)


if __name__ == "__main__":
    import sys
    for p in sys.argv[1:]:
        t = open(p).read()
        print(p, "heading", len(heading_chunks(t)), "fixed", len(fixed_chunks(t)))
