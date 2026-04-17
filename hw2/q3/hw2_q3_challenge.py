import sys
import numpy as np

if __name__ == "__main__":
    # Train Data set is argument 1
    train_data = sys.argv[1]
    # Test Data set is argument 2
    test_data = sys.argv[2]

    test_data_lines = []
    with open('output3b.txt', 'w') as out:
        for line in open(test_data):
            # <USER ID>,<MOVIE ID>,<TIMESTAMP>
            (user_id, movie_id, timestamp) = line.strip().split(',')
            test_data_lines.append((int(user_id), int(movie_id), int(timestamp)))
            # <USER ID>,<MOVIE ID>,<SCORE FOR MOVIE><TIMESTAMP>
            score_placeholder = np.random.rand()
            out.write(f"{user_id},{movie_id},{score_placeholder},{timestamp}\n")