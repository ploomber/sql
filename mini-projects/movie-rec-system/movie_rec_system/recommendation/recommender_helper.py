import numpy as np


def content_movie_recommender(
    input_movie,
    similarity_database,
    movie_database_list,
    top_n=10,
):
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
    # movie list
    movie_list = movie_database_list

    # get movie similarity records
    movie_sim = similarity_database[
        similarity_database.index == input_movie
    ].values[  # noqa E501
        0
    ]
    # get movies sorted by similarity
    sorted_movie_ids = np.argsort(movie_sim)[::-1]

    # get recommended movie names
    recommended_movies = movie_list[sorted_movie_ids[1 : top_n + 1]]  # noqa E203

    print(
        "\n\nTop Recommended Movies for:",
        input_movie,
        "are:-\n",
        recommended_movies,
    )
    return recommended_movies


def get_popularity_rmse(df, sample_movie, recommendations):
    sample_movie_popularity = df[df["title"] == sample_movie].popularity[1]
    recommendations_popularity = df[
        df["title"].isin(recommendations)
    ].popularity.values  # noqa E501

    squared_diffs = (sample_movie_popularity - recommendations_popularity) ** 2
    rmse = np.sqrt(squared_diffs.mean())

    return rmse


def get_vote_avg_rmse(df, sample_movie, recommendations):
    sample_movie_vote_average = df[df["title"] == sample_movie].vote_average[1]
    recommendations_vote_average = df[
        df["title"].isin(recommendations)
    ].vote_average.values

    squared_diffs = (
        sample_movie_vote_average - recommendations_vote_average
    ) ** 2  # noqa E501
    rmse = np.sqrt(squared_diffs.mean())

    return rmse


def get_vote_count_rmse(df, sample_movie, recommendations):
    sample_movie_popularity = df[df["title"] == sample_movie].vote_count[1]
    recommendations_popularity = df[
        df["title"].isin(recommendations)
    ].vote_count.values  # noqa E501

    squared_diffs = (recommendations_popularity - sample_movie_popularity) ** 2
    rmse = np.sqrt(squared_diffs.mean())

    return rmse