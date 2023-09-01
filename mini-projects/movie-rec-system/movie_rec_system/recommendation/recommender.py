import json
import pandas as pd
import duckdb
from functools import lru_cache
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from recommender_helper import (
    content_movie_recommender,
    get_popularity_rmse,
    get_vote_avg_rmse,
    get_vote_count_rmse,
)


@lru_cache(maxsize=None)
def get_data() -> pd.DataFrame:
    """
    Function that automatically connects
    to duckdb as a GET call upon launch
    of FastAPI
    """
    con = duckdb.connect("../../movies_data.duckdb")
    query = "SELECT * FROM movie_genre_data"
    df = con.execute(query).fetchdf()
    con.close()
    return df


def create_combined(df: pd.DataFrame, weight=2) -> pd.DataFrame:
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
    """
    Generate movie recommendations based on
    content similarity and computes associated metrics.

    This function retrieves movie data,
    calculates cosine similarity between movies using
    TF-IDF vectorization of their combined overview
    and genre, and returns a list of recommended
    movies along with certain metrics
    (popularity, vote average, and vote count RMSE).

    Parameters
    ----------
    movie : str
        The title of the movie for which
        recommendations are to be generated.

    num_rec : int, optional
        The number of movie recommendations
        to generate. Default is 10.

    stop_words : str, optional
        The language of stop words to be
        used when vectorizing the "combined" column.
        Default is "english".

    Returns
    -------
    str
        A JSON-formatted string containing
        the original movie, a list of recommendations,
        and associated metrics
        (popularity, vote average, and vote count RMSE).

    Examples
    --------
    >>> result = get_recommendation("Inception", num_rec=5)
    >>> print(json.loads(result))
    {
        "movie": "Inception",
        "recommendations": [...],
        "metrics": {
            "popularity": ...,
            "vote_avg": ...,
            "vote_count": ...
        }
    }

    """
    df = get_data()
    df["title"] = df["title"].str.lower()  # Convert titles to lowercase once
    movie = movie.lower()  # Convert input movie to lowercase

    df = create_combined(df)
    tfidf = TfidfVectorizer(stop_words=stop_words)
    tfidf_matrix = tfidf.fit_transform(df["combined"])

    similarity = cosine_similarity(tfidf_matrix)
    
    # Make sure the dataframe's columns and indices are in lowercase
    similarity_df = pd.DataFrame(
        similarity, index=df.title.values, columns=df.title.values
    )

    movie_list = similarity_df.columns.values
    recommendations = content_movie_recommender(movie, similarity_df, movie_list, num_rec)

    if not recommendations:
        return None

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
