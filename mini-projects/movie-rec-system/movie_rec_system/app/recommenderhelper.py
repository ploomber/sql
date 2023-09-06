import numpy as np
import pandas as pd
import duckdb
from functools import lru_cache
from sklearn.feature_extraction.text import TfidfVectorizer

def content_movie_recommender(
    input_movie: str,
    similarity_database: pd.DataFrame,
    movie_database_list: list,
    top_n=10,
) -> list:
    """
    Function that uses a similarity matrix to find similar movies

    Parameters
    ----------
    input_movie : str
        reference movie to find similarities
    similarity_database : pandas.DataFrame
        similarity matrix of movies
    movie_database_list : numpy.ndarray
        movies in our similarity matrix
    top_n : int
        number of similar movies to output
    """
    try:
        # get movie similarity records
        movie_sim = similarity_database[
            similarity_database.index == input_movie
        ].values[0]

        # get movies sorted by similarity
        sorted_movie_ids = np.argsort(movie_sim)[::-1]
        recommended_movies = movie_database_list[
            sorted_movie_ids[1 : top_n + 1]  # noqa E203
        ]  # noqa E501
        return list(recommended_movies)
    except IndexError:
        return []


def get_popularity_rmse(
    df: pd.DataFrame, sample_movie: str, recommendations: list
) -> float:
    """
    Compute RMSE for popularity, vote average, and vote count
    for the provided movie and recommendations.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame which must contain
        a "title" column.

    sample_movie : str
        The title of the movie for which
        recommendations are to be generated.

    recommendations : list
        A list of recommended movies.

    Returns
    -------
    popularity_rmse : float
        The RMSE for popularity.
    """
    # Convert titles in dataframe and sample_movie to lowercase
    df["title"] = df["title"].str.lower()
    sample_movie = sample_movie.lower()

    filtered_df = df[df["title"] == sample_movie]

    if not filtered_df.empty:
        sample_movie_popularity = filtered_df.popularity.iloc[0]
        recommendations_popularity = df[
            df["title"].isin(recommendations)
        ].popularity.values

        squared_diffs = (
            sample_movie_popularity - recommendations_popularity
        ) ** 2  # noqa E501
        rmse = np.sqrt(squared_diffs.mean())

        return round(float(rmse), 3)
    else:
        return float("nan")


def get_vote_avg_rmse(
    df: pd.DataFrame, sample_movie: str, recommendations: list
) -> float:
    """
    Compute RMSE for popularity, vote average, and vote count
    for the provided movie and recommendations.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame which must contain
        a "title" column.

    sample_movie : str
        The title of the movie for which
        recommendations are to be generated.

    recommendations : list
        A list of recommended movies.

    Returns
    -------
    popularity_rmse : float
        The RMSE for popularity.
    """
    sample_movie_vote_average = df[
        df["title"] == sample_movie
    ].vote_average.iloc[  # noqa E501
        0
    ]
    recommendations_vote_average = df[
        df["title"].isin(recommendations)
    ].vote_average.values

    squared_diffs = (
        sample_movie_vote_average - recommendations_vote_average
    ) ** 2  # noqa E501
    rmse = np.sqrt(squared_diffs.mean())

    return round(float(rmse), 3)


def get_vote_count_rmse(
    df: pd.DataFrame, sample_movie: str, recommendations: list
) -> float:
    """

    Compute RMSE for popularity, vote average, and vote count
    for the provided movie and recommendations.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame which must contain
        a "title" column.

    sample_movie : str
        The title of the movie for which
        recommendations are to be generated.

    recommendations : list
        A list of recommended movies.

    Returns
    -------
        popularity_rmse : float
        The RMSE for popularity.
    """
    sample_movie_popularity = df[df["title"] == sample_movie].vote_count.iloc[
        0
    ]  # noqa E501
    recommendations_popularity = df[
        df["title"].isin(recommendations)
    ].vote_count.values  # noqa E501

    squared_diffs = (recommendations_popularity - sample_movie_popularity) ** 2
    rmse = np.sqrt(squared_diffs.mean())

    return round(float(rmse), 3)

@lru_cache(maxsize=None)
def get_data() -> pd.DataFrame:
    """
    Function that automatically connects
    to duckdb as a GET call upon launch
    of FastAPI
    """
    con = duckdb.connect("./movies_data.duckdb")
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


def retrieve_and_transform_data() -> pd.DataFrame:
    """
    Retrieve data from duckdb and transform it
    into a format that can be used for generating
    movie recommendations.

    Returns
    -------
    pd.DataFrame
        The transformed DataFrame with an additional "combined" column.
    """
    df = get_data()
    df["title"] = df["title"].str.lower()
    df = create_combined(df)
    return df


def compute_tfidf_vectorization(df, stop_words="english"):
    """
    Compute TF-IDF vectorization of the "combined" column
    in the provided DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame which must contain
        a "combined" column.

    stop_words : str, optional
        The language of stop words to be
        used when vectorizing the "combined" column.
        Default is "english".

    Returns
    -------
    tfidf_matrix:    scipy.sparse.csr.csr_matrix
        The TF-IDF vectorization of the "combined" column."""
    tfidf = TfidfVectorizer(stop_words=stop_words)
    tfidf_matrix = tfidf.fit_transform(df["combined"])
    return tfidf_matrix


def compute_metrics(df, movie, recommendations):
    """
    Compute RMSE for popularity, vote average, and vote count
    for the provided movie and recommendations.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame which must contain
        a "combined" column.

    movie : str
        The title of the movie for which
        recommendations are to be generated.

    recommendations : list
        A list of recommended movies.

    Returns
    -------
    popularity_rmse : float
        The RMSE for popularity.

    vote_avg_rmse : float
        The RMSE for vote average.

        ote_count_rmse : float
        The RMSE for vote count.
    """
    popularity_rmse = get_popularity_rmse(df, movie, recommendations)
    vote_avg_rmse = get_vote_avg_rmse(df, movie, recommendations)
    vote_count_rmse = get_vote_count_rmse(df, movie, recommendations)
    return popularity_rmse, vote_avg_rmse, vote_count_rmse
