import sys
import time
from pyspark import SparkConf, SparkContext


def parse_line(line): # Return (user_id: int, friends: list[int]) from a tab-separated line.
    parts = line.strip().split('\t')
    user = int(parts[0])
    if len(parts) < 2 or not parts[1].strip():
        return (user, [])
    friends = [int(x) for x in parts[1].split(',')]
    return (user, friends)


def emit_mutual_candidates(record): # Yield ((min(fi,fj), max(fi,fj)), 1) for every pair in the friend list.
    _, friends = record
    pairs = []
    n = len(friends) 
    for i in range(n): # nested loop instead of itertools (library restriction); O(|F|^2) per user
        for j in range(i + 1, n):
            a = min(friends[i], friends[j])
            b = max(friends[i], friends[j])
            pairs.append(((a, b), 1))
    return pairs


def emit_existing_friendships(record): # Yield ((min(u,f), max(u,f)), True) for each direct friendship of user u.
    user, friends = record
    return [((min(user, f), max(user, f)), True) for f in friends]


def main():
    start = time.time()

    conf = SparkConf().setAppName("MutualFriends")
    sc = SparkContext(conf=conf)

    input_path = sys.argv[1]

    # Step 1 (Parse)
    graph = sc.textFile(input_path).map(parse_line).cache()

    # Step 2 (Emit mutual-friend candidates)
    mutual_candidates = graph.flatMap(emit_mutual_candidates)

    # Step 3 (Emit existing friendships): Mark direct-friend pairs to be excluded in Step 4.
    existing = graph.flatMap(emit_existing_friendships)

    # Step 4 (Count and filter)
    mutual_counts = mutual_candidates.reduceByKey(lambda a, b: a + b)
    recommendations = mutual_counts.subtractByKey(existing)

    # Step 5 (Sort and output): Count DESC, first user ID ASC, second user ID ASC.
    top10 =  recommendations.sortBy(lambda x: (-x[1], x[0][0], x[0][1])).take(10)

    sc.stop()

    for (u1, u2), count in top10:
        print(f"{u1}\t{u2}\t{count}")

    #elapsed = time.time() - start
    #sys.stderr.write(f"Elapsed: {elapsed:.2f}s\n")


if __name__ == '__main__':
    main()
