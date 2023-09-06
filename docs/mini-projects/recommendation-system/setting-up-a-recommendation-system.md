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

# Setting up a recommendation system

Recall from the previous section that we have already extracted movie data from an API and stored it in a DuckDB database. We will be using this database to build our recommendation system. For a refresher on recommendation systems, visit [this guide](./intro-to-rec-systems.md).

```{important}
This guide assumes you have executed the Ploomber pipeline introduced in the previous section. If you haven't, please do so before proceeding. Visit [this guide](./setting-up-etl.md) and [this guide](./eda-with-jupyter.md) for a refresher.
```

## A Closer Look at Content-Based Recommendation Systems
For the remainder of this article, we'll focus on one specific type: content-based recommendation systems. Instead of relying on user interaction history, these systems suggest items based on their content. Think of it like this: if you've enjoyed a book because of its genre and author, a content-based recommender might suggest another book with a similar genre and author.

## How do they Work?

Imagine you're building a movie recommendation system. The system would look at various movie attributes like its genre, director, lead actors, and even its synopsis. It then compares these attributes with movies you've previously shown interest in. In essence, it's matching movie attributes with your preferences.

Content-based recommenders thrive on the principle of similarity. If you liked a particular item, you're likely to enjoy another item that's similar to it. This method shines especially when each item has clear, descriptive attributes. For instance, movies have metadata like genre, director, and cast, which can be compared to find resemblances.

## Diving Deeper: Using TF-IDF and Cosine Similarity

### What's TF-IDF?

TF-IDF stands for Term Frequency-Inverse Document Frequency. It's a method to quantify the importance of words in a document relative to a collection of documents. Here's a simple way to understand it:

* Term Frequency (TF): How often a word appears in a document.
* Inverse Document Frequency (IDF): Reduces the weight of words that appear frequently across many documents (like "the" or "and").

For instance, if you're searching for "latest European soccer games" on a search engine, the word "the" might appear more often than "soccer games". But for our search, "soccer games" is clearly more important. TF-IDF helps in weighing words in such a manner.

### What's Cosine Similarity?

Once we've transformed our content into numerical form using TF-IDF, we need a way to determine similarity between items. That's where cosine similarity comes in. It measures the cosine of the angle between two vectors. If the vectors are identical, the cosine is 1, and if they're completely different, the cosine is 0.

In the context of our movie recommender, after converting movie descriptions into vectors using TF-IDF, we use cosine similarity to find movies that have similar descriptions.

By combining TF-IDF with cosine similarity, we can find movies that are closely related based on their descriptions. This method can be further enhanced by adding more attributes like genres, cast, and crew to the mix.

## Setting up a Content-Based Movie Recommender

Let's take a closer look at the code that powers our content-based recommendation system.

Let's start by setting up our environment and importing necessary libraries:

```python
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
```

### 1. The Core Recommender: `content_movie_recommender`

This function is the heart of our recommendation system. Given an input movie, it uses a precomputed similarity matrix to find movies that are most similar to the input.

Parameters:
* `input_movie`: The movie title we want recommendations for.
* `similarity_database`: A precomputed matrix that stores the similarity scores between movies.
* `movie_database_list`: A list of all movie titles in our database.
* `top_n`: The number of recommendations we want.

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


To evaluate how good our recommendations are, we use the Root Mean Square Error (RMSE). RMSE is a standard metric used to measure the differences between predicted and observed values. In our context, we're using it to measure how similar our recommended movies are to the input movie in terms of popularity, vote average, and vote count.

`get_popularity_rmse`: This function computes the RMSE between the popularity of the input movie and the popularity of the recommended movies.

This function converts the movie titles in the dataframe (df) and the sample_movie string to lowercase. This ensures that when we compare movie titles, the comparison is case-insensitive, preventing potential mismatches due to different letter cases. It then filters the dataframe to retrieve rows where the movie title matches the sample_movie. The result is stored in filtered_df. We then check if the chosen movie is in the dataframe. If the `sample_movie` exists in the dataframe, the code fetches its popularity value. It also retrieves the popularity values of all movies in the recommendations list. If it doesn't exist, a `NaN` value is returned instead. 

The RMSE is a measure of the differences between values. Here, it's used to measure the difference between the popularity of the sample_movie and the popularity of the recommended movies. The differences are squared, averaged, and then the square root is taken to compute the RMSE.

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

`get_vote_avg_rmse`: This function calculates the Root Mean Square Error (RMSE) between the vote average of a given movie (`sample_movie`) and the vote averages of a list of recommended movies.

This function starts by retrieving the vote average for the sample_movie from the dataframe `df`, it then fetches the vote averages for all the movies in the recommendations list. It then computes the RMSE. The RMSE is calculated by:

1. Finding the squared differences between the vote average of the sample_movie and the vote averages of the recommended movies.
2. Averaging these squared differences.
3. Taking the square root of the average to get the RMSE.

The function then returns the RMSE value rounded to three decimal places.


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

`get_vote_count_rmse`: This function calculates the Root Mean Square Error (RMSE) between the vote count of a given movie (sample_movie) and the vote counts of a list of recommended movies.

It first retrieves the vote count (which is a measure of popularity) for the sample_movie from the dataframe `df`, it then fetches the vote counts (popularity measures) for all the movies in the `recommendations` list.

The RMSE is calculated by:

1. Finding the squared differences between the vote count of the sample_movie and the vote counts of the recommended movies.
2. Averaging these squared differences.
3. Taking the square root of the average to get the RMSE.

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


### 3. Extrtacting Movie Data

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

Let's add a few more functions. First, we'll need to ensure that `df` contains a `combined column`

```python
def create_combined(df: pd.DataFrame, weight=2):
    df["combined"] = df["overview"] + " " + (df["genre_names"] + ", ") * weight
    return df
```

We can now fetch the data and begin processing it, the function below enforces all titles to be lowercase and adds the `combined` column:

```python
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
```

Once the data is retrieved and transformed, we can compute the TF-IDF vectorization of the `combined` column:


```python
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
```

We can now use the metrics functions we defined previously and compute RMSE for popularity, vote average, and vote count for the input movie and the recommended movies:

```python
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

```

We are now ready to obtain recommendations. Our goal will be to provide as input a movie title, and as a result obtain a JSON object containing the recommendations. 

The key steps in this function are:

1. Retrieve and transform data
2. Compute TF-IDF vectorization
3. Compute cosine similarity
4. Create Similarity DataFrame
5. Generate recommendations
6. Compute metrics
7. Prepare results
8. Convert the results to JSON

Note the structure of the results:

```python
result = {
    "movie": movie,
    "recommendations": recommendations,
    "metrics": {
        "popularity": popularity_rmse,
        "vote_avg": vote_avg_rmse,
        "vote_count": vote_count_rmse,
    },
}
```

This format will be useful once we start developing an API to serve our recommendations.

```python
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
    movie = movie.lower()
    df = retrieve_and_transform_data()

    tfidf_matrix = compute_tfidf_vectorization(df, stop_words)
    similarity = cosine_similarity(tfidf_matrix)

    similarity_df = pd.DataFrame(
        similarity, index=df.title.values, columns=df.title.values
    )
    movie_list = similarity_df.columns.values
    recommendations = content_movie_recommender(
        movie, similarity_df, movie_list, num_rec
    )

    if not recommendations:
        return None

    popularity_rmse, vote_avg_rmse, vote_count_rmse = compute_metrics(
        df, movie, recommendations
    )

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
```

## Bringing all pieces together

We can package the functions above as follows. We will create a new folder called `app` and a set of files called `recommender.py` and  `recommenderhelper.py`

```bash
mini-projects
├──movie-rec-system
├──├── movies_data.duckdb
├──├── pipeline.yaml
├──├── pyproject.toml
├──├── README.md
├──├── app
├──│   └── recommender.py
├──│   └── recommenderhelper.py
├──├── etl
├──│   └── extract.py
├──│   └── eda.ipynb
├──├── products
├──     └── extract-pipeline.ipynb
├──└── tests
├──│       └── __init__.py
├──└── .env
```

Where:

* `recommender.py` contains the `get_recommendation` function
* `recommenderhelper.py` contains all other functions

To import the functions from `recommenderhelper.py` we need to add the following to `recommender.py`:

```python
from .recommenderhelper import (
    content_movie_recommender,
    compute_metrics,
    retrieve_and_transform_data,
    compute_tfidf_vectorization,
)
```

You can find a full version of `recommender.py` [here](https://github.com/ploomber/sql/blob/main/mini-projects/movie-rec-system/movie_rec_system/app/recommender.py) and a full version of `recommenderhelper.py` [here](https://github.com/ploomber/sql/blob/main/mini-projects/movie-rec-system/movie_rec_system/app/recommenderhelper.py)

## Summary

In this section, we learned how to build a content-based movie recommendation system. We started by understanding the core concepts behind content-based recommendation systems. We then built a recommendation system using TF-IDF and cosine similarity. Finally, we packaged our recommendation system into a Python package. In the next section, we will learn how to build a FastAPI application that can serve our recommendations as an API.