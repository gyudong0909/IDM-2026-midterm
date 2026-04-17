import sys
import time
import math
import numpy as np


def is_prime(n): # Deterministic primality test via trial division up to sqrt(n)
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def next_prime(n): # Return the smallest prime >= n
    while not is_prime(n):
        n += 1
    return n


def extract_shingles(text, k=3): # Extract k-shingles: keep only [a-z] and space, lowercase, sliding window of k chars
    cleaned = []
    for ch in text.lower():
        if ch.isalpha() or ch == ' ':
            cleaned.append(ch)
    s = ''.join(cleaned)
    # set: deduplication is automatic; membership testing is O(1)
    return {s[i:i + k] for i in range(len(s) - k + 1)}


def main():
    start = time.time()

    input_path = sys.argv[1]
    k = 3
    b = 6  # number of LSH bands
    r = 20 # rows per band -> threshold ~ (1/b)^(1/r) ~ 0.9
    num_hashes = b * r
    sim_threshold = 0.9

    # Step 1 (Shingle extraction): Parse each article; build its 3-shingle set.
    article_ids = []
    article_shingle_sets = []

    with open(input_path, 'r') as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            sp = line.index(' ')
            article_ids.append(line[:sp])
            article_shingle_sets.append(extract_shingles(line[sp + 1:], k))

    D = len(article_ids)

    # Step 2 (Global shingle list)
    all_shingles = set()
    for sh in article_shingle_sets:
        all_shingles.update(sh)

    shingle_list = sorted(all_shingles)
    shingle_to_row = {s: i for i, s in enumerate(shingle_list)}
    n = len(shingle_list)

    # Step 3 (MinHash): h(x) = (a*x + b) % c, c = smallest prime >= n
    # a, b drawn uniformly from [0, c-1] with np.random.seed(0)
    c = next_prime(n)
    np.random.seed(0)
    a_arr = np.random.randint(0, c, size=num_hashes, dtype=np.int64)
    b_arr = np.random.randint(0, c, size=num_hashes, dtype=np.int64)

    sig = np.full((D, num_hashes), c, dtype=np.int64)  # initialise to c (> any hash value)

    for doc_idx, shingles in enumerate(article_shingle_sets):
        if not shingles:
            continue
        rows = np.array([shingle_to_row[s] for s in shingles], dtype=np.int64)
        # Fully vectorised: all num_hashes hash values in one matrix op, then column-min.
        # Shape (num_hashes, |shingles|) — avoids a Python loop over hash functions.
        hash_mat = (a_arr[:, None] * rows[None, :] + b_arr[:, None]) % c
        sig[doc_idx] = hash_mat.min(axis=1)

    # Step 4 (LSH)
    candidate_pairs = set()

    for band in range(b):
        row_start = band * r
        row_end = row_start + r
        buckets = {}
        for doc_idx in range(D):
            # tuple key: hashable; O(1) average dict lookup
            key = tuple(sig[doc_idx, row_start:row_end].tolist())
            if key not in buckets:
                buckets[key] = []
            buckets[key].append(doc_idx)
        for docs in buckets.values():
            if len(docs) < 2:
                continue
            for i in range(len(docs)):
                for j in range(i + 1, len(docs)):
                    candidate_pairs.add((min(docs[i], docs[j]), max(docs[i], docs[j])))

    # Step 5 (Output): Signature similarity = matching positions / num_hashes; print pairs with similarity >= 0.9.
    for i, j in sorted(candidate_pairs):
        similarity = float(np.sum(sig[i] == sig[j])) / num_hashes
        if similarity >= sim_threshold:
            print(f"{article_ids[i]}\t{article_ids[j]}\t{similarity:.6f}")

    #elapsed = time.time() - start
    #ys.stderr.write(f"Elapsed: {elapsed:.2f}s\n")


if __name__ == '__main__':
    main()
