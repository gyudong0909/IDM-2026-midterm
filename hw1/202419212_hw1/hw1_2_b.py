import sys
import time
import numpy as np


def triangular_index(i, j, n): # Flat-array index for pair (i, j), i < j, in a triangular matrix of n items.
    return i * n - i * (i + 1) // 2 + (j - i - 1)


def main():
    start = time.time()

    input_path = sys.argv[1]
    support_threshold = 100
    confidence_threshold = 0.50

    # Step 1 (Pass 1). Count every item; load all baskets into memory.
    # dict: O(1) average update, compact for a sparse item universe.
    item_counts = {}
    baskets = []

    with open(input_path, 'r') as fh:
        for line in fh:
            tokens = line.strip().split()
            if not tokens:
                continue
            baskets.append(tokens)
            for tok in tokens:
                item_counts[tok] = item_counts.get(tok, 0) + 1

    frequent_items = {item for item, cnt in item_counts.items()
                      if cnt >= support_threshold}

    # Step 2 (Index mapping). Sort N frequent items lexicographically; assign indices 0..N-1.
    # Lexicographic sort: deterministic index mapping across runs.
    freq_list = sorted(frequent_items)
    item_to_idx = {item: i for i, item in enumerate(freq_list)}
    n = len(freq_list)

    # Step 3 (Pass 2 / triangular matrix). Count pairs of frequent items.
    # numpy int32 array of size N*(N-1)//2: stores only (i,j) with i<j,
    # halving memory vs a full matrix; int32 avoids Python object overhead.
    tri_size = n * (n - 1) // 2
    tri = np.zeros(tri_size, dtype=np.int32)

    for basket in baskets:
        indices = sorted({item_to_idx[tok] for tok in basket if tok in item_to_idx})
        m = len(indices)
        for a in range(m):
            for b in range(a + 1, m):
                idx = triangular_index(indices[a], indices[b], n)
                tri[idx] += 1

    frequent_pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            sup = int(tri[triangular_index(i, j, n)])
            if sup >= support_threshold:
                frequent_pairs.append((freq_list[i], freq_list[j], sup))

    num_frequent_pairs = len(frequent_pairs)

    # Step 4 (Association rules). For each frequent pair (A, B), generate A→B and B→A;
    # keep rules with confidence >= 50%; sort by confidence DESC, tie-break support DESC.
    rules = []
    for a, b, sup_ab in frequent_pairs:
        conf_ab = sup_ab / item_counts[a]
        conf_ba = sup_ab / item_counts[b]
        if conf_ab >= confidence_threshold:
            rules.append((a, b, conf_ab, sup_ab))
        if conf_ba >= confidence_threshold:
            rules.append((b, a, conf_ba, sup_ab))

    num_valid_rules = len(rules)
    rules.sort(key=lambda x: (-x[2], -x[3]))

    print(num_frequent_pairs)
    print(num_valid_rules)
    for a, b, conf, sup in rules[:10]:
        print(f"Rule: {a} -> {b}, Confidence: {conf:.6f}, Support: {sup}")

    #elapsed = time.time() - start
    #sys.stderr.write(f"Elapsed: {elapsed:.2f}s\n")


if __name__ == '__main__':
    main()
