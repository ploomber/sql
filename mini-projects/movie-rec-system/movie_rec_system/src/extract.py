import duckdb
import requests
from dotenv import load_dotenv
import os

# Parameter to get 500 English movies
language_count = {
    "en": 500,
}

# Load API key from .env file
load_dotenv(".env")
api_key = os.getenv("API_KEY")


def init_duck_db_movies(duckdb_file_path, res):
    """
    Create table for movies API call in DuckDB
    If the table exists, new data is inserted

    Parameters
    ----------
    duckdb_file_path : str
        Path to the DuckDB database file
    res : requests object
        API call results
    """
    conn = duckdb.connect(duckdb_file_path, read_only=False)

    tables = conn.execute("SHOW TABLES;").fetchall()
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

    conn.close()


def init_duck_db_genres(duckdb_file_path, genres_data):
    conn = duckdb.connect(duckdb_file_path, read_only=False)

    tables = conn.execute("SHOW TABLES;").fetchall()
    if ("genres",) not in tables:
        conn.execute(
            """
            CREATE TABLE genres (
                id INTEGER,
                name VARCHAR
            );
        """
        )

    for genre in genres_data:
        conn.execute(
            f"""
            INSERT INTO genres VALUES ({genre['id']},
            '{genre['name']}');
        """
        )

    conn.close()


def drop_existing_movies_table(duckdb_file_path):
    """
    Drops existing movies tables

    Parameters
    ----------
    duckdb_file_path : str
        Path to the DuckDB database file
    """
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


def drop_existing_genres_table(duckdb_file_path):
    """
    Drops existing genres table

    Parameters
    ----------
    duckdb_file_path : str
        Path to the DuckDB database file
    """
    conn = duckdb.connect(duckdb_file_path, read_only=False)

    genres_table_exists = conn.execute(
        "SELECT 1 FROM information_schema.tables WHERE table_name = 'genres'"
    ).fetchone()

    if genres_table_exists:
        conn.execute("DROP TABLE genres;")
        print("Table 'genres' dropped.")
    else:
        print("Table 'genres' does not yet exist. Creating 'genres' now.")

    conn.close()


def get_movies(lang, freq, duckdb_file_path):
    """
    Inserts API call results into DuckDB

    Parameters
    ----------
    lang : str
        Language of movies
    freq : int
        Amount of movies to extract
    duckdb_file_path : str
        Path to the DuckDB database file
    """
    url = "https://api.themoviedb.org/3/movie/popular?api_key={api_key}&with_original_language={lang}".format(  # noqa E501
        api_key=api_key, lang=lang
    )
    movies = 0
    page = 1
    progress = 0

    drop_existing_movies_table(duckdb_file_path)

    while movies < freq:
        try:
            res = requests.get(url + "&page=" + str(page))
        except requests.exceptions.RequestException as e:
            print("An error occurred during the request:", e)
            break
        if res.status_code != 200:
            print("error")
            return []

        res = res.json()

        if "errors" in res.keys():
            print("api error !!!")
            return movies

        movies += len(res["results"])

        init_duck_db_movies(duckdb_file_path, res)

        if progress != round(movies / freq * 100):
            progress = round(movies / freq * 100)
            if progress % 5 == 0:
                print(progress, end="%, ")

        page = page + 1
    return movies


def get_genres(lang, duckdb_file_path):
    """
    Inserts API call results into DuckDB

    Parameters
    ----------
    lang : str
        Language of movies
    freq : int
        Amount of movies to extract
    duckdb_file_path : str
        Path to the DuckDB database file
    """
    url = "https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&with_original_language={lang}".format(  # noqa E501
        api_key=api_key, lang=lang
    )

    drop_existing_genres_table(duckdb_file_path)

    try:
        res = requests.get(url)
    except requests.exceptions.RequestException as e:
        print("An error occurred during the request:", e)
        return []

    if res.status_code != 200:
        print("error")
        return []

    res = res.json()

    if "errors" in res.keys():
        print("api error !!!")
        return []

    genres_data = res["genres"]
    init_duck_db_genres(duckdb_file_path, genres_data)

    return len(genres_data)


for key in language_count:
    # print(key,language_count[key])
    print("Downloading", key, end=": ")
    movies = get_movies(key, language_count[key], "movies_data.duckdb")
    print("Total movies found:", movies)
    genres = get_genres(key, "movies_data.duckdb")
    print("Total genres found:", genres)
