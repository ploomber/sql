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

# Designing a Movie Recommender System Pipeline

Once we have set up our folder structure and environment with the help of Poetry, we can start building our pipeline. We will be using Ploomber to build our pipeline. Ploomber is a Python library that allows you to build data pipelines using Python scripts and Jupyter notebooks. It is a great tool for data scientists who want to build data pipelines without having to learn new tools or languages. 

## Pipeline Overview

Here's a high-level summary of what the pipeline entails:

1. **Data Extraction:** Utilize a Python script to call a movie database API.
2. **Data Storage**: Populate a DuckDB instance with the extracted movie data.
3. **Exploratory Data Analysis (EDA):** Dive deep into the data with SQL-based analysis in a Jupyter notebook. This step will involve extracting data, data wrangling, and creating new tables.
4. **Build a Recommender System:** Use another Jupyter notebook to create a movie recommendation system based on the data you've wrangled.
5. **Packaging:** Package your entire workflow, including notebooks, using Ploomber/Ploomber-engine.
6. **API Deployment:** Serve your recommender system's results as an API using FastAPI.
7. **Dockerization:** Containerize your application using Docker for easy deployment and scaling.

In this blog, we will focus on data extraction and data storage. We will be using a Python script to extract data from the Movie Database API. We will then store the data into a DuckDB instance.

## Data extraction

The first step is to extract data from the [Movie Database API](https://developer.themoviedb.org/docs/getting-started). We will be using a Python script to do this. The script will call the API and extract the data into a DuckDB database instance. 

```{important}
You can create a free account on the Movie Database website to get an API key. 
[Link here](https://developer.themoviedb.org/themoviedb/v3/reference/intro/authentication#api-key-quick-start)
If you face issues, please join the Ploomber community on [Slack](https://ploomber.io/community)
```

### API Structure

We will explore two entry points:

1. Movies - With URL structure `https://api.themoviedb.org/3/movie/popular?api_key=<api_key>&with_original_language=<lang>`
2. Genres - With URL structure `https://api.themoviedb.org/3/genre/movie/list?api_key=<api_key>&with_original_language=<lang>`

Where `<api_key>` is the API key we created earlier and `<lang>` is the language code for the language we want to extract data for. We will work with English via the code `en`. 


### Creating a `.env` file to store API keys

Before we start writing our script, we need to create a `.env` file to store our API keys. This file will be used by the script to access the API. It is a good practice to not leak our keys within our script or Jupyter notebook. The `.env` file is one of the ways to do this. 

Recall our directory structure:

```bash
mini-projects
├──movie-rec-system
├──├── pyproject.toml
├──├── README.md
├──├── movie-rec-system
├──│   └── __init__.py
├──└── tests
├──│       └── __init__.py
```

From VSCode, select "File", then "Open Folder" and select the `mini-projects` folder. Let's create a `.env` file in the `movie-rec-system` directory of our project. Press "File", then "New File" and name it `.env`. Within the `.env` file, we will create a variable:

```bash
API_KEY = <your API key>
```

To keep the process cleaner, let's rename the `movie-rec-system` folder to `etl`. 


After this, your folder structure should look like this:

```bash
mini-projects
├──movie-rec-system
├──├── pyproject.toml
├──├── README.md
├──├── etl
├──│   └── __init__.py
├──└── tests
├──│       └── __init__.py
├──└── .env
```

### Creating a Python script to extract data

Once we have our API key, and have stored it into a `.env` file, we can start building our Python script. The key steps we will follow are:

1. Make a request to the API using the API key.
2. Extract the data from the API response.
3. Create a DuckDB instance and populate it with the extracted data.

Let's create a Python script called `extract.py` in the `etl` folder.

#### Key imports

We will be using the `requests` library to make a request to the API. We will also be using the `dotenv` library to access the API key stored in the `.env` file. Finally, we will be using the `duckdb` library to create a DuckDB instance and populate it with the extracted data. 

```python
import requests
from dotenv import load_dotenv
import duckdb
import os
```

#### Loading the API key

We will use the `load_dotenv()` function to load the API key from the `.env` file. 

```python
# Load API key from .env file
load_dotenv(".env")
api_key = os.getenv('API_KEY')
```

#### Making a request to the API

We will use the `requests` library to make a request to the API. We will use the `get()` function to make a `GET` request to the API. We will pass the URL of the API as an argument to the `get()` function. We will also pass the API key as a parameter to the `get()` function. Below are building blocks:

```python
# Construct URL
url = "https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&with_original_language={lang}".format(  # noqa E501
        api_key=api_key, lang=lang
    )
# Make a request
res = requests.get(url)

# Transform content to JSON
res = res.json()
```

#### Adding `try-except` blocks

Sometimes when we make a call to an API, things can go wrong. For example, the API might be down, or the API key might be invalid. To handle such situations, we will add `try-except` blocks to our code. 

```python
url = "https://api.themoviedb.org/3/movie/popular?api_key={api_key}&with_original_language={lang}".format(  # noqa E501
        api_key=api_key, lang=lang
    )

try:
    res = requests.get(url)
except requests.exceptions.RequestException as e:
    print("An error occurred during the request:", e)
    return []
```

#### Challenge: Extracting data from the Movies API

Develop a function to extract data from the Movies API for the `movie` entry point and for the `genres` entry point. The function should take the API key and language code as arguments. It should return a JSON object.

Explore the results you obtained. Pay close attention to the structure, fields and values of the JSON object. This will guide you in the next step of the process.

### Storing the data into a `DuckDB` instance

Once we have functionality to extract the data from the API, our next goal is to store it into a `DuckDB` instance. We will be using the `duckdb` library to do this. We can initialize the connection as follows:

```python
# Initialize connection
duckdb_file_path = "movies_data.duckdb"
conn = duckdb.connect(duckdb_file_path, read_only=False)
```

Our next goal is to create tables that correspond to the data we have extracted. We will create two tables:

1. `movies` - This table will contain information about the movies.
2. `genres` - This table will contain information about the genres.

If you completed the challenge, you will notice the following fields in the `movies` entry point. You can observe this by printing the `res["results"]` variable:

```python
genre_ids
id 
original_language 
overview
popularity 
release_date
title 
vote_average 
vote_count 
```

We can create and populate the `movies` in our `DuckDB` instance with `conn.execute()`, which can take as input a SQL command as a string. We will use the `CREATE TABLE` command to create the table and the `INSERT INTO` command to populate it.

```python
# Create the table if it doesn't exist
if ("movies",) not in tables:
        conn.execute(
            """
            CREATE TABLE movies (
                genre_ids INT[],
                id INTEGER,
                original_language VARCHAR,
                overview VARCHAR,
                popularity DOUBLE,
                release_date TIMESTAMP,
                title VARCHAR,
                vote_average DOUBLE,
                vote_count INTEGER
            );
        """
        )

# Populate it by iterating over the records in the JSON object
for movie in res["results"]:
    genre_ids_str = ",".join(map(str, movie["genre_ids"]))
    conn.execute(
        f"""
        INSERT INTO movies VALUES (ARRAY[{genre_ids_str}], {movie['id']},
        '{movie['original_language']}',
        '{movie['overview'].replace("'", "''")}',
        {movie['popularity']},
        '{movie['release_date']}',
        '{movie['title'].replace("'", "''")}',
        {movie['vote_average']},
        {movie['vote_count']});
    """
    )

# Close connection
conn.close()
```

#### Challenge

Write a function `init_duck_db_movies` that will take as input the path to the DuckDB database file, and a JSON response from the Movies API. The function should create a `DuckDB` instance and populate it with the data from the JSON response.

Write a function `init_duck_db_genres` that will take as input the path to the DuckDB database file, and a JSON response from the Genres API. The function should create a `DuckDB` instance and populate it with the data from the JSON response.

#### Handling errors

We saw that one of the things that can go wrong is that the API is not available. We saw how to handle this using `try-except` blocks. Another thing that can go wrong is that the data we are trying to create is a table that already exists. We can handle this by checking if the table exists before creating it. 


```python
conn = duckdb.connect(duckdb_file_path, read_only=False)

movies_table_exists = conn.execute(
    "SELECT 1 FROM information_schema.tables WHERE table_name = 'movies'"
).fetchone()

if movies_table_exists:
    conn.execute("DROP TABLE movies;")
    print("Table 'movies' dropped.")
else:
    print("Table 'movies' does not yet exist. Creating 'movies' now.")

conn.close()
```

#### Challenge

Write a function or set of functions that will check if the `movies` and `genres` tables exist in the `DuckDB` instance. If they do, drop them. If they don't, create them.

## Find a sample script

The workflow above is a good starting point for building our pipeline. However, it is not complete. We need to add a few more things to make it production-ready. For example, we need to add logging, error handling, and more. A simple starter script [can be found here](https://github.com/ploomber/sql/blob/main/mini-projects/movie-rec-system/movie_rec_system/etl/extract.py). Note there may be different ways of solving this problem, and further improving this current script. As such the script above is just a starting point.

## Build a Ploomber pipeline

Now that we have a script to extract data from the API and store it into a `DuckDB` instance, we can build a Ploomber pipeline. We will be using Ploomber to build our pipeline. Ploomber is a Python library that allows you to build data pipelines using Python scripts and Jupyter notebooks. It is a great tool for data scientists who want to build data pipelines without having to learn new tools or languages.

Ploomber allows you to execute your pipeline from the command line. This is useful because it allows you to automate your pipeline. For example, you can set up a cron job to run your pipeline every day at a certain time. You can add steps to the pipeline through YAML files. The structure of a sample YAML file we will use in this example is:

```yaml
tasks:
  - source: path-to-script/myscript.py
    product:
      nb: path-to-notebook-file/notebook-name.ipynb
      data: path-to-data-file/data-file-name.duckdb
```

To learn about different ways to structure your pipelines, refer to the Ploomber cookbook [here](https://docs.ploomber.io/en/latest/cookbook/index.html).


### Creating a `pipeline.yaml` file

We will start by creating a `pipeline.yaml` file in the `movie-rec-system` folder. This file will contain the steps of our pipeline. We will also add a `products` folder.

```bash
mini-projects
├──movie-rec-system
├──├── pipeline.yaml
├──├── pyproject.toml
├──├── README.md
├──├── etl
├──│   └── extract.py
├──├── products
├──└── tests
├──│       └── __init__.py
├──└── .env
```

The `pipeline.yaml` file will be structured as follows:

```yaml
tasks:
  - source: movie_rec_system/etl/extract.py
    product:
      nb: movie_rec_system/products/extract-pipeline.ipynb
      data: movies_data.duckdb
```

To execute the pipeline, we will use the `ploomber build` command. We will execute this command from the `movie-rec-system` folder. 

```bash
cd mini-projects/movie-rec-system
ploomber build
```

This should show

```bash
Loading pipeline...
Notebook movie_rec_system/etl/extract.py is missing the parameters cell, adding it at the top of the file...
Executing: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████| 10/10 [00:12<00:00,  1.26s/cell]
name     Ran?      Elapsed (s)    Percentage
-------  ------  -------------  ------------
extract  True          12.5755       50.9231
```

The resulting folder structure should look like this:

```bash
mini-projects
├──movie-rec-system
├──├── movies_data.duckdb
├──├── movies_data.duckdb.wal
├──├── .movies_data.duckdb.metadata
├──├── pipeline.yaml
├──├── pyproject.toml
├──├── README.md
├──├── etl
├──│   └── extract.py
├──│   └── eda.ipynb
├──├── products
├──     └── extract-pipeline.ipynb
├──     └── .extract-pipeline.ipynb.metadata
├──└── tests
├──│       └── __init__.py
├──└── .env
```

The `.metadata` files are created by Ploomber and can be ignored. The `.wal` file is a write-ahead log file created by DuckDB. It can also be ignored. Within `products`, the `extract-pipeline.ipynb` file is the Jupyter notebook that was created by Ploomber, this notebook will contain a trace back of the execution.

## Summary

In this blog, we learned how to extract data from an API and store it into a `DuckDB` instance. We also learned how to handle errors and check if tables exist in a `DuckDB` instance. In the next blog, we will learn how to use Jupyter notebooks to perform exploratory data analysis on the data we have extracted. Our focus is going to be to perform exploratory data analysis and data wrangling using SQL. 



