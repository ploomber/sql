import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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