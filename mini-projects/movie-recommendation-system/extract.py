import duckdb
import requests

# Parameter to get 500 English movies
language_count = {
    'en':500, 
}

api_key = ''

def init_duck_db(duckdb_file_path, res):
    """
    Initialize DuckDB database and create tables for each dataframe

    Parameters
    ----------
    duckdb_file_path : str
        Path to the DuckDB database file

    """
    conn = duckdb.connect(duckdb_file_path, read_only=False)

    tables = conn.execute("SHOW TABLES;").fetchall()
    if ('movies',) not in tables:
        conn.execute("""
            CREATE TABLE movies (
                genre_ids INTEGER[],
                id INTEGER,
                original_language VARCHAR,
                overview VARCHAR,
                popularity FLOAT,
                release_date VARCHAR,
                title VARCHAR,
                vote_average FLOAT,
                vote_count INTEGER
            );
        """)

    # Step 4: Insert the results from the API into the movies table
    for movie in res['results']:
        genre_ids_str = ",".join(map(str, movie['genre_ids'])) 
        conn.execute(f"""
            INSERT INTO movies VALUES (ARRAY[{genre_ids_str}], {movie['id']}, '{movie['original_language']}', '{movie['overview'].replace("'", "''")}', {movie['popularity']}, '{movie['release_date']}', '{movie['title'].replace("'", "''")}', {movie['vote_average']}, {movie['vote_count']});
        """)


    conn.close()
    
def drop_existing_table(duckdb_file_path):
    conn = duckdb.connect(duckdb_file_path, read_only=False)
    conn.execute("DROP TABLE movies;")
    conn.close()
    
def get_movies(lang, freq, duckdb_file_path):
  url = 'https://api.themoviedb.org/3/movie/popular?api_key={api_key}&with_original_language={lang}'.format(api_key=api_key,lang=lang)
  movies = 0
  page = 1
  progress = 0
  
  drop_existing_table(duckdb_file_path)
  
  while movies<freq:
    try:
        res = requests.get(url+"&page="+str(page))
    except:
        raise ('not connected to internet or movidb issue')

    if res.status_code != 200:
        print ('error')
        return []

    res = res.json()
    
    if 'errors' in res.keys():
      print('api error !!!')
      return movies

    movies +=  len(res['results'])

    init_duck_db(duckdb_file_path, res)
    
    if progress != round(movies/freq*100):
      progress = round(movies/freq*100)
      if progress%5==0:
        print( progress, end="%, ")
      
    
    
    page = page + 1
  return movies

for key in language_count:
  # print(key,language_count[key])
  print("Downloading", key, end=": ")
  movies = get_movies(key,language_count[key], "movies.duckdb")
  print('Total movies found:', movies)

