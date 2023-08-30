import json
import pandas as pd
import duckdb
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from recommender_helper import (
    content_movie_recommender,
    get_popularity_rmse,
    get_vote_avg_rmse,
    get_vote_count_rmse,
)


def get_data():
    """
    Function that automatically connects
    to duckdb as a GET call upon launch
    of FastAPI

    Returns a connection
    """
    con = duckdb.connect("../../movies_data.duckdb")
    query = "SELECT * FROM movie_genre_data"
    df = con.execute(query).fetchdf()
    con.close()
    return df


def create_combined(df: pd.DataFrame, weight=2):
    """
    Generates a "combined" column by combining the
    "overview" and "genre_names" columns.

    The "genre_names" column will be multiplied by the
    provided weight, essentially repeating the genre names
    the specified number of times.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame which must contain
        both "overview" and "genre_names" columns.

    weight : int, default=2
        The number of times "genre_names" should be
        repeated in the "combined" column.

    Returns
    -------
    pd.DataFrame
        The modified DataFrame with an additional "combined" column.

    Examples
    --------
    >>> df = pd.DataFrame({
    ...     'overview': ['A story about...'],
    ...     'genre_names': ['Action']
    ... })
    >>> create_combined(df)
         overview        genre_names         combined
    0  A story about...    Action  A story about... Action, Action,

    """
    df["combined"] = df["overview"] + " " + (df["genre_names"] + ", ") * weight
    return df


def get_recommendation(movie: str, num_rec: int = 10, stop_words="english"):
    df = get_data()

    # Create column with overview and genres
    df = create_combined(df)

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
