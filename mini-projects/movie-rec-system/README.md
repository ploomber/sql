## Set up

1. Create new environment

```
conda create --name poetry-env python=3.10
```

2. Activate environment

``` 
conda activate poetry-env
```

3. Install poetry

```
pip install poetry
```

4. Install dependencies

```
poetry lock
poetry install
```

5. Run the app

```
cd mini-projects/
poetry run python movie_rec_system/src/extract.py
```