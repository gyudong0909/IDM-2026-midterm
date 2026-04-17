import sys
import time
import math
import numpy as np


def tokenize(text): # Lowercase and split on whitespace
    return text.lower().split()


def main():
    start = time.time()

    input_path = sys.argv[1]
    num_hyperplanes = 10
    dist_threshold = 0.1

    # Step 1 (Tokenisation)
    article_ids = []
    article_tokens = []

    with open(input_path, 'r') as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            sp = line.index(' ')
            article_ids.append(line[:sp])
            article_tokens.append(tokenize(line[sp + 1:]))

    D = len(article_ids)

    # Step 2 (Global vocabulary). Collect all unique tokens; sort lexicographically;
    # assign dimension indices 0..V-1 for a deterministic mapping across runs.
    vocab_set = set()
    for tokens in article_tokens:
        vocab_set.update(tokens)

    vocab = sorted(vocab_set)
    term_to_idx = {t: i for i, t in enumerate(vocab)}
    V = len(vocab)

    # Step 3 (TF-IDF). TF = raw count, IDF = log(N/df), TFIDF = TF * IDF.
    tf_dicts = []
    for tokens in article_tokens:
        counts = {}
        for tok in tokens:
            idx = term_to_idx[tok]
            counts[idx] = counts.get(idx, 0) + 1
        tf_dicts.append(counts)

    df = np.zeros(V, dtype=np.int32)
    for counts in tf_dicts:
        for t_idx in counts:
            df[t_idx] += 1

    idf = np.log(D / df.astype(np.float64))

    tfidf_dicts = []
    for counts in tf_dicts:
        tfidf_dicts.append({t_idx: cnt * idf[t_idx] for t_idx, cnt in counts.items()})

    norms = np.array([
        math.sqrt(sum(v * v for v in d.values()))
        for d in tfidf_dicts
    ])

    # Step 4 (LSH / SimHash). 10 random hyperplanes from N(0,1); hash bit = sign(tfidf_d · h_k).
    np.random.seed(0)
    hyperplanes = np.random.randn(num_hyperplanes, V)

    projections = np.zeros((D, num_hyperplanes), dtype=np.float64)
    for t_idx in range(V):
        h_col = hyperplanes[:, t_idx]
        for doc_idx, tfidf_d in enumerate(tfidf_dicts):
            if t_idx in tfidf_d:
                projections[doc_idx] += tfidf_d[t_idx] * h_col

    # tuple of bools as bucket key: hashable, minimal memory
    hashes = (projections > 0)
    buckets = {}
    for doc_idx in range(D):
        key = tuple(hashes[doc_idx].tolist())
        if key not in buckets:
            buckets[key] = []
        buckets[key].append(doc_idx)

    # Step 5 (Cosine similarity): Exact computation for candidate pairs in the same bucket.
    # Sparse dot product: iterate over the shorter dict, look up keys in the longer one -> O(min(|da|, |db|)) instead of O(V).
    for doc_list in buckets.values():
        if len(doc_list) < 2:
            continue
        for i in range(len(doc_list)):
            for j in range(i + 1, len(doc_list)):
                a, b = doc_list[i], doc_list[j]
                if norms[a] == 0.0 or norms[b] == 0.0:
                    continue
                da, db = tfidf_dicts[a], tfidf_dicts[b]
                if len(da) > len(db):
                    da, db = db, da
                dot = sum(v * db[k] for k, v in da.items() if k in db)
                cos_sim = dot / (norms[a] * norms[b])
                if 1.0 - cos_sim < dist_threshold:
                    print(f"{article_ids[a]}\t{article_ids[b]}\t{cos_sim:.6f}")

    #elapsed = time.time() - start
    #sys.stderr.write(f"Elapsed: {elapsed:.2f}s\n")


if __name__ == '__main__':
    main()
