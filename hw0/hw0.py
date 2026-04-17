import re
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf()
sc = SparkContext(conf=conf)

lines = sc.textFile(sys.argv[1])
words = lines.flatMap(lambda l: re.split(r'[^\w]+', l))

# unique words per starting letter (case-insensitive, alpha only)
counts = (
    words
    .map(lambda w: w.lower())
    .filter(lambda w: w and w[0].isalpha())
    .distinct()
    .map(lambda w: (w[0], 1))
    .reduceByKey(lambda a, b: a + b)
    .collectAsMap()
)

sc.stop()

for ch in 'abcdefghijklmnopqrstuvwxyz':
    print(f"{ch}\t{counts.get(ch, 0)}")
