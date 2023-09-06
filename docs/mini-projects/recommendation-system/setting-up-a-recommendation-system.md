---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.6
kernelspec:
  display_name: jupyblog
  language: python
  name: python3
---

# An introduction to Recommendation Systems

Recommendation systems have become an integral part of our digital lives. From suggesting movies on Netflix to recommending products on Amazon, these systems play a pivotal role in enhancing user experience and driving business metrics. In this blog, we'll delve deep into the world of recommendation systems, focusing on content-based recommenders.

## What are Recommendation Systems?

Recommendation systems are algorithms designed to suggest relevant items to users. These items could be anything from movies, songs, and books to products, news articles, or even search queries. The primary goal is to provide personalized recommendations that enhance the user's experience.

## Why are they Important?

In today's digital age, the sheer volume of choices can be overwhelming. Recommendation systems help users navigate through this vast sea of information, providing them with tailored suggestions that align with their preferences and behaviors. This not only enhances user satisfaction but also boosts business metrics like sales, retention, and engagement.

## Types of Recommendation Systems

Recommendation systems can be broadly classified into two categories:

* **Collaborative Filtering**: This method uses the past behavior of users and items to generate recommendations. For instance, if a user has previously purchased a book, the system might recommend similar books based on the purchase history of other users who have bought the same book.
* **Content-Based Filtering**: This method uses the attributes of items to recommend other items with similar attributes. For instance, if a user has previously purchased a book, the system might recommend similar books based on the genre, author, or publisher of the book.
* **Matrix Factorization**: Matrix factorization techniques, like Singular Value Decomposition (SVD), decompose the user-item interaction matrix into multiple matrices representing latent factors. It's especially popular for its effectiveness in collaborative filtering and its ability to handle sparse data.
* **Hybrid Methods**: hybrid methods combine the strengths of both collaborative and content-based filtering. Hybrid models can be implemented in several ways:

1. Separate models for each approach that are combined at the end.
2. Incorporating collaborative and content-based methods into a single model.
3. Unifying the models into a single model.

* **Deep Learning**: With the rise of neural networks and deep learning, these techniques are increasingly being applied to recommendation systems. Autoencoders or Recurrent Neural Networks (RNNs) can be used to predict the next item in a sequence, making them useful for recommending items like the next song in a playlist or the next video in a series.
* **Association Rule Mining**: Used mainly in market basket analysis, this method identifies associations between items. A classic example is the association between diapers and beer in a supermarket setting. Tools like Apriori or Eclat algorithms are used to extract these associations.
* **Knowledge-Based Recommendations**: In situations where user-item interactions are sparse and it's challenging to compute reliable recommendations, knowledge-based techniques come in handy. They provide personalized recommendations by leveraging explicit knowledge about users and items. They often involve asking users to give more input or provide feedback.
* **Session-Based Recommendations**: In many scenarios, especially in e-commerce, the user might not have a past history, or their current intent might be different from their past behavior. Session-based recommenders focus on short-term behavior and use techniques like RNNs to predict the next item a user might be interested in during a session.

## A Closer Look at Content-Based Recommendation Systems
For the remainder of this article, we'll focus on one specific type: content-based recommendation systems. Instead of relying on user interaction history, these systems suggest items based on their content. Think of it like this: if you've enjoyed a book because of its genre and author, a content-based recommender might suggest another book with a similar genre and author.

## How do they Work?

Imagine you're building a movie recommendation system. The system would look at various movie attributes like its genre, director, lead actors, and even its synopsis. It then compares these attributes with movies you've previously shown interest in. In essence, it's matching movie attributes with your preferences.

Content-based recommenders thrive on the principle of similarity. If you liked a particular item, you're likely to enjoy another item that's similar to it. This method shines especially when each item has clear, descriptive attributes. For instance, movies have metadata like genre, director, and cast, which can be compared to find resemblances.

### Diving Deeper: Using TF-IDF and Cosine Similarity


#### What's TF-IDF?

TF-IDF stands for Term Frequency-Inverse Document Frequency. It's a method to quantify the importance of words in a document relative to a collection of documents. Here's a simple way to understand it:

* Term Frequency (TF): How often a word appears in a document.
* Inverse Document Frequency (IDF): Reduces the weight of words that appear frequently across many documents (like "the" or "and").

For instance, if you're searching for "latest European soccer games" on a search engine, the word "the" might appear more often than "soccer games". But for our search, "soccer games" is clearly more important. TF-IDF helps in weighing words in such a manner.

#### What's Cosine Similarity?

Once we've transformed our content into numerical form using TF-IDF, we need a way to determine similarity between items. That's where cosine similarity comes in. It measures the cosine of the angle between two vectors. If the vectors are identical, the cosine is 1, and if they're completely different, the cosine is 0.

In the context of our movie recommender, after converting movie descriptions into vectors using TF-IDF, we use cosine similarity to find movies that have similar descriptions.

By combining TF-IDF with cosine similarity, we can find movies that are closely related based on their descriptions. This method can be further enhanced by adding more attributes like genres, cast, and crew to the mix.

## Setting up a Content-Based Movie Recommender

Let's take a closer look at the code that powers our content-based recommendation system.

### 1. The Core Recommender: `content_movie_recommender``

This function is the heart of our recommendation system. Given an input movie, it uses a precomputed similarity matrix to find movies that are most similar to the input.

Parameters:
* input_movie: The movie title we want recommendations for.
* similarity_database: A precomputed matrix that stores the similarity scores between movies.
* movie_database_list: A list of all movie titles in our database.
* top_n: The number of recommendations we want.

The function first fetches the similarity scores of the input movie with all other movies. It then sorts these scores in descending order and fetches the top n movies.

```python
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
```


### 2. Evaluating Recommendations: RMSE Functions

Let's start by setting up our environment and importing necessary libraries:

```python
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
```

To evaluate how good our recommendations are, we use the Root Mean Square Error (RMSE). RMSE is a standard metric used to measure the differences between predicted and observed values. In our context, we're using it to measure how similar our recommended movies are to the input movie in terms of popularity, vote average, and vote count.

`get_popularity_rmse`: This function computes the RMSE between the popularity of the input movie and the popularity of the recommended movies.

```python
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
```

`get_vote_avg_rmse`: Similar to the above, but this function computes the RMSE for the vote average.

```python
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
        The RMSE for popularity."""
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
```

`get_vote_count_rmse`: This function calculates the RMSE for the vote count.

```python
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

```

Each of these functions works similarly:

1. Fetch the attribute (popularity, vote average, or vote count) of the input movie.
2. Fetch the same attribute for all recommended movies.
3. Compute the squared differences between the input movie's attribute and the recommended movies' attributes.
4. Calculate the mean of these squared differences.
5. Return the square root of this mean as the RMSE.

In essence, these functions give us a numerical measure of how close our recommendations are to the input movie in terms of popularity, vote average, and vote count. The lower the RMSE, the closer the recommended movies are to the input movie in terms of these attributes.

By combining a robust recommendation function with evaluation metrics, we can ensure that our system not only provides relevant recommendations but also allows us to measure and improve its performance over time.


### Extrtacting Movie Data

In previous sections, we build an ETL pipeline to extract, transform, and load movie data from an API file into a DuckDB database. We'll use the same database to fetch movie data for our recommender. By this point we have performed all data wrangling operations we need. If you need a refresher, please consult [this guide](./eda-with-jupyter.md)

```python
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
```