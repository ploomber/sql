import numpy as np
import pandas as pd


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
    sample_movie_popularity = df[df["title"] == sample_movie].vote_count.iloc[
        0
    ]  # noqa E501
    recommendations_popularity = df[
        df["title"].isin(recommendations)
    ].vote_count.values  # noqa E501

    squared_diffs = (recommendations_popularity - sample_movie_popularity) ** 2
    rmse = np.sqrt(squared_diffs.mean())

    return round(float(rmse), 3)
