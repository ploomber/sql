import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from recommender_helper import (
    content_movie_recommender,
    get_popularity_rmse,
    get_vote_avg_rmse,
    get_vote_count_rmse,
)


def connect_duckdb():
    """
    Function that automatically connects
    to duckdb as a GET call upon launch
    of FastAPI

    Returns a connection
    """
    # Will have to adjust this based on
    # how we set up duckdb instance
    pass


def create_combined(df, weight=2):
    df["combined"] = df["overview"] + " " + (df["genre_names"] + ", ") * weight
    return df


def get_recommendation(movie: str, num_rec: int = 10, stop_words="english"):
    # conn = connect_duckdb()

    # use sql/jupysql to query data
    # convert data to pandas pd called df

    # Create column with overview and genres
    df = create_combined(1)

    # Vectorize "combined"
    tfidf = TfidfVectorizer(stop_words=stop_words)
    tfidf_matrix = tfidf.fit_transform(df["combined"])

    # Compute similarity
    similarity = cosine_similarity(tfidf_matrix)

    similarity_df = pd.DataFrame(
        similarity, index=df.title.values, columns=df.title.values
    )

    movie_list = similarity_df.columns.values

    # Get movie recommendations
    recommendations = content_movie_recommender(
        movie, similarity_df, movie_list, num_rec
    )

    # Compute metrics
    popularity_rmse = get_popularity_rmse(df, movie, recommendations)

    vote_avg_rmse = get_vote_avg_rmse(df, movie, recommendations)

    vote_count_rmse = get_vote_count_rmse(df, movie, recommendations)

    result = {
        "movie": movie,
        "recommendations": recommendations,
        "metrics": {
            "popularity": popularity_rmse,
            "vote_avg": vote_avg_rmse,
            "vote_count": vote_count_rmse,
        },
    }

    result_json = json.dumps(result)

    return result_json
