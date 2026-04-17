import sys
import math
from collections import defaultdict

# Number of nearest neighbors to use.
TOPK_USERS = 10
TOPK_ITEMS = 10

# Candidate movies for recommendation are movie IDs in [1, CANDIDATE_MAX_MOVIE_ID].
CANDIDATE_MAX_MOVIE_ID = 1000

# Output the top-5 predicted movies.
TOPK_OUTPUT = 5

# This dataset works better with a user who actually rated many movies in 1..1000.
TARGET_USER_ID = 414

# Ignore similarities computed from too few common ratings.
MIN_OVERLAP = 5

# Numerical stability threshold.
EPS = 1e-12


def cosine_similarity_from_dicts(vec_a, vec_b):
    """
    Compute cosine similarity between two sparse vectors represented as dicts.

    vec_a: {index: value}
    vec_b: {index: value}
    """
    ######### TODO #########

    return ...
    ########################


def load_ratings(ratings_path):
    """
    Reads ratings.txt and returns:
      - user_ratings: {user_id: {movie_id: rating}}
      - item_ratings: {movie_id: {user_id: rating}}
      - user_means:   {user_id: average rating of that user}
      - item_means:   {movie_id: average rating of that movie}

    ratings.txt format:
      <USER ID>,<MOVIE ID>,<RATING>,<TIMESTAMP>
    """
    user_ratings = defaultdict(dict)
    item_ratings = defaultdict(dict)

    with open(ratings_path, "r", encoding="utf-8") as f:
        for line in f:
            user_id_str, movie_id_str, rating_str, _timestamp_str = line.strip().split(",")
            user_id = int(user_id_str)
            movie_id = int(movie_id_str)
            rating = float(rating_str)

            user_ratings[user_id][movie_id] = rating
            item_ratings[movie_id][user_id] = rating
    
    user_means = {}
    ######### TODO #########

    ########################

    item_means = {}
    ######### TODO #########

    ########################

    return user_ratings, item_ratings, user_means, item_means


def mean_center_by_user(user_ratings, user_means):
    """
    Returns a mean-centered version of the utility matrix:
      centered_user_ratings[user_id][movie_id] = rating - user_mean
    """
    centered_user_ratings = {}
    ######### TODO #########

    ########################

    return centered_user_ratings


def transpose_user_to_item(user_dict):
    """
    Converts {user_id: {movie_id: value}} into {movie_id: {user_id: value}}.
    """
    item_dict = defaultdict(dict)
    for user_id, inner_dict in user_dict.items():
        for movie_id, value in inner_dict.items():
            item_dict[movie_id][user_id] = value
    return item_dict


def get_overlap_count(dict_a, dict_b):
    """
    Returns the number of common keys between two sparse vectors.
    """
    return len(set(dict_a.keys()) & set(dict_b.keys()))


def predict_user_based(
    target_user_id,
    candidate_movie_id,
    user_ratings,
    centered_user_ratings,
    user_means,
    topk_users=TOPK_USERS,
    min_overlap=MIN_OVERLAP,
):
    """
    Predict target user's rating on candidate_movie_id using user-based CF.

    Similarity is computed on mean-centered ratings with cosine similarity.
    Use only neighbors who:
      1) rated the candidate movie,
      2) have at least `min_overlap` co-rated movies with the target user.

    Prediction rule (similarity-weighted residual):
      r_hat(u, i) = mean_u + sum_v s(u,v) * (r(v,i) - mean_v) / sum_v |s(u,v)|

    Finally, clip the prediction into [0.5, 5.0].
    """
    ######### TODO #########

    return ...
    ########################


def predict_item_based(
    target_user_id,
    candidate_movie_id,
    user_ratings,
    centered_item_ratings,
    item_means,
    topk_items=TOPK_ITEMS,
    min_overlap=MIN_OVERLAP,
):
    """
    Predict target user's rating on candidate_movie_id using item-based CF.

    Similarity is computed between mean-centered item vectors.
    Here, item vectors are obtained by first mean-centering ratings by user,
    then transposing into movie -> user form.

    Use only neighbor items j such that:
      1) target user rated j,
      2) overlap between item i and item j is at least `min_overlap`.

    Prediction rule (similarity-weighted residual):
      r_hat(u, i) = mean_i + sum_j s(i,j) * (r(u,j) - mean_j) / sum_j |s(i,j)|

    Finally, clip the prediction into [0.5, 5.0].
    """
    ######### TODO #########

    return ...
    ########################


def top_k_recommendations(predictions, topk=TOPK_OUTPUT):
    """
    predictions: list of (movie_id, predicted_rating)

    Sort by:
      1) predicted_rating descending
      2) movie_id ascending

    Return top-k results.
    """
    predictions.sort(key=lambda x: (-x[1], x[0]))
    return predictions[:topk]


def user_based_recommendations(
    target_user_id,
    user_ratings,
    centered_user_ratings,
    user_means,
    candidate_max_movie_id=CANDIDATE_MAX_MOVIE_ID,
):
    """
    Predict all candidate movies in [1, candidate_max_movie_id] that the target
    user has NOT rated, then return the top-5 recommendations.
    """
    predictions = []
    rated_by_target = user_ratings[target_user_id]

    for candidate_movie_id in range(1, candidate_max_movie_id + 1):
        if candidate_movie_id in rated_by_target:
            continue

        pred = predict_user_based(
            target_user_id,
            candidate_movie_id,
            user_ratings,
            centered_user_ratings,
            user_means,
            TOPK_USERS,
            MIN_OVERLAP,
        )
        predictions.append((candidate_movie_id, pred))

    return top_k_recommendations(predictions, TOPK_OUTPUT)


def item_based_recommendations(
    target_user_id,
    user_ratings,
    centered_item_ratings,
    item_means,
    candidate_max_movie_id=CANDIDATE_MAX_MOVIE_ID,
):
    """
    Predict all candidate movies in [1, candidate_max_movie_id] that the target
    user has NOT rated, then return the top-5 recommendations.
    """
    predictions = []
    rated_by_target = user_ratings[target_user_id]

    for candidate_movie_id in range(1, candidate_max_movie_id + 1):
        if candidate_movie_id in rated_by_target:
            continue

        pred = predict_item_based(
            target_user_id,
            candidate_movie_id,
            user_ratings,
            centered_item_ratings,
            item_means,
            TOPK_ITEMS,
            MIN_OVERLAP,
        )
        predictions.append((candidate_movie_id, pred))

    return top_k_recommendations(predictions, TOPK_OUTPUT)


def write_output(output_path, results):
    """
    Writes one result per line:
      <MOVIE ID>\t<PREDICTED RATING>
    """
    with open(output_path, "w", encoding="utf-8") as f:
        for movie_id, predicted_rating in results:
            f.write(f"{movie_id}\t{predicted_rating:.6f}\n")


def main():
    if len(sys.argv) != 2:
        print("Usage: python hw2_q3_cf.py path/to/ratings.txt")
        sys.exit(1)

    ratings_path = sys.argv[1]

    # Load data.
    user_ratings, item_ratings, user_means, item_means = load_ratings(ratings_path)

    # Build normalized matrix for similarity computation.
    centered_user_ratings = mean_center_by_user(user_ratings, user_means)
    centered_item_ratings = transpose_user_to_item(centered_user_ratings)

    # Generate recommendations.
    ub_results = user_based_recommendations(
        TARGET_USER_ID,
        user_ratings,
        centered_user_ratings,
        user_means,
        CANDIDATE_MAX_MOVIE_ID,
    )
    ib_results = item_based_recommendations(
        TARGET_USER_ID,
        user_ratings,
        centered_item_ratings,
        item_means,
        CANDIDATE_MAX_MOVIE_ID,
    )

    # Save outputs.
    write_output("output3a_user.txt", ub_results)
    write_output("output3a_item.txt", ib_results)


if __name__ == "__main__":
    main()
