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

# Data wrangling and exploratory data analysis in Jupyter

In the previous tutorial, we used a Python script to call a movie database API and populate a DuckDB instance with the extracted movie data. Furthermore, we packaged the script within a Ploomber pipeline. In this tutorial, we will expand our pipeline to incorporate exploratory data analysis and data wranging with SQL using a Jupyter notebook. This step will involve extracting data, data wrangling, and creating new tables.

```{important}
This tutorial assumes you have completed the previous tutorial and have a DuckDB instance populated with movie data.
```

Ensure you have completed all steps up to this point and execute

```bash
cd mini-projects/movie-rec-system
ploomber build
```


## Setup

Within our folder structure, we will create a Jupyter notebook called `eda.ipynb` in the `etl` folder. From last time, our folder structure should look like this:

```bash
mini-projects
├──movie-rec-system
├──├── movies_data.duckdb
├──├── movies_data.duckdb.wal
├──├── pipeline.yaml
├──├── pyproject.toml
├──├── README.md
├──├── etl
├──│   └── extract.py
├──│   └── eda.ipynb
├──├── products
├──     └── extract-pipeline.ipynb
├──└── tests
├──│       └── __init__.py
├──└── .env
```

```{important}
If running the notebook in VSCode, you will need to install the [Jupyter extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) to run the notebook.
```

To load the data from our DuckDB instance within Jupyter, we will use [JupySQL](https://github.com/ploomber/jupysql). JupySQL allows you to run SQL and plot large datasets in Jupyter via a %sql, %%sql, and %sqlplot magics. 

## Imports

Let's start by importing the libraries we will need for this tutorial. As we focus on EDA, we will use SQL for data wrangling, and `pandas` dataframes and `matplotlib` for plotting.

```{code-cell} ipython3
import pandas as pd
import matplotlib.pyplot as plt
```

To set up access to the database, we will use the `%sql` extension from `jupysql`. 

```{code-cell} ipython3
%reload_ext sql
```

```{important}
Did you know you can configure the default behavior of the `%sql` magic? The configuration above will transform SQL query results into `pandas` format automatically. Learn more in the video below ⬇️⬇️⬇️ [![JupySQL 0.9 release](1.jpg)](https://www.youtube.com/watch?v=dJl-MMNoMXk).
```

We can then form a connection string to our DuckDB instance. We will use the `%%sql` magic to run SQL queries in our notebook. Notice that when creating and executing this notebook, we are using the same environment as our pipeline. This ensures that we are using the same dependencies and versions as our pipeline.

We need to give our notebook access to the DuckDB instance. To do this, we will use the `duckdb:///` prefix. This prefix tells JupySQL to use the DuckDB engine to connect to the database. We will then specify the path to our DuckDB instance.

```{code-cell} ipython3
%sql duckdb:///movies_data.duckdb
```

## Challenge

Explore the tables in the `movies_data.duckdb` instance. Use the `%sql` magic to run SQL queries to explore the tables. How many tables are there? What are the columns in each table? What are the data types of each column? What are the primary keys? What are the foreign keys? What are the relationships between the tables?

## Data Wrangling 

### Handling Nested Data

Let's take a look at the data. We will start by looking at the `movies` table. We can use the `%%sql` magic to run SQL queries in our notebook. We will use the `SELECT` statement to select all columns from the `movies` table. We will then use the `LIMIT` statement to limit the number of rows returned to 5.

```{code-cell} ipython3
%%sql 
SELECT *
FROM movies
LIMIT 2;
```

We see that the `genre_ids` column contains a lists of integers. 

```{code-cell} ipython3
%%sql 
SELECT *
FROM genres
LIMIT 2;
```

We see the genre ids in the `movies` table correspond to the `id` column in the `genres` table. Let's do some data wrangling:

```{code-cell} ipython3
%%sql 
WITH ExpandedGenres AS (
    SELECT 
        m.id AS movie_id,
        mg.movie_genre_id,
        g.name AS genre_name
    FROM 
        (SELECT UNNEST(movies.genre_ids) as movie_genre_id, movies.id FROM movies) AS mg
    JOIN 
        movies m ON mg.id = m.id
    JOIN 
        genres g ON mg.movie_genre_id = g.id
)

SELECT
    movie_id,
    STRING_AGG(genre_name, ', ') AS genre_names
FROM 
    ExpandedGenres
GROUP BY 
    movie_id;
```

**The query is transforming a structure where movies have a list of genre IDs into a more readable format where you get a single row for each movie and a comma-separated string of all its genres by name.**

**In Depth Explanation:**

1. Common Table Expression (CTE) - `ExpandedGenres`:

* This CTE is aiming to "expand" or "flatten" movies based on their genres. It looks like each movie in the movies table has an array (or similar list-type structure) of genre IDs in `genre_ids`.
* `SELECT UNNEST(movies.genre_ids) as movie_genre_id, movies.id FROM movies`: This line is unnesting (or exploding) the `genre_ids` list for each movie. This means if a movie has multiple genre IDs in its `genre_ids`, each genre ID will become a separate row, paired with the movie's ID.
* The resulting table of `movie_id` and `movie_genre_id` is then joined with the original movies table (to fetch the movie's full details, although only the id is used in this CTE) and the genres table to fetch the genre's name corresponding to each `movie_genre_id`.
* The result of the CTE will be a table with movie_id, `movie_genre_id`, and the genre's name (`genre_name`) for every movie. Note that if a movie has multiple genres, it will appear in multiple rows, one for each genre.

2. Main Query:

* The main query then operates on the `ExpandedGenres` CTE.
* It groups the rows by `movie_id` (i.e., each movie will only appear once in the final output).
* For each `movie_id`, it aggregates the genre names using `STRING_AGG`. The `STRING_AGG` function is concatenating the genre names together with a comma and space (', ') in between them. So, for each movie, you'll get a single string that lists all its genres.
* The result will be a table where each row contains a movie's ID and a concatenated string of all its genres.
