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

# Setting up an API using FastAPI

We've so far extracted data from an API, performed EDA on said data, and created a recommender system. Let's put everything into action by serving our recommender system using an easy to use tool called FastAPI.

[FastAPI](https://fastapi.tiangolo.com/) is **fast**. Serving our recommender system using this tool can be done in just one `.py` script. Let's first go through a brief overview of FastAPI before implementing it into our project. If you're already familiar with FastAPI, feel free to skip to ... 

## What is FastAPI?

FastAPI is an extremely easy to use web framework to build APIs using just only Python. To quickly summarize its capabilities for our purposes, let's run through an example script called `app.py`.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

The code above is all you need to create a simple API that, when accessed at its index, returns a JSON object containing "Hello World." Now imagine utilizing a recommender function we've created in the [last section](./setting-up-a-recommendation-system.md). We can utilize a `POST` function that returns recommended movies after inputting an initial movie. We're getting a little ahead of ourselves by introducing a `POST` method, but don't worry, we'll cover it soon.

For now, let's demonstrate how easy it is to actual start the app. With our example above, we would start the app by running this command in the terminal:

```bash
uvicorn app:app
```

Running the above command would start the server using `Uvicorn` and create an output in your terminal that includes a link to said server. [Uvicorn](https://www.uvicorn.org/) is an [AGSI](https://asgi.readthedocs.io/en/latest/) web server implementation tool for Python. This is a little out of scope, but if you're interested in learning more, navigate to the provided hyperlinks.

Now that you understand that `Uvicorn` creates a server for our application, let's go through *how* we can have the server communicate.

## HTTP Request Methods

HTTP request methods are used when communicating with servers. There are several methods, but for our case, we'll go through two of the most common methods: `GET` and `POST`.

### `GET` Method

The `GET` method is used to request data from a specified resource. In FastAPI, we use the `@app.get()` decorator to define a function that will handle `GET` requests. In a `GET` request, we usually don't send a payload (data) to the server but rather request information based on the URL or URL parameters.

For example, let's create a simple `GET` endpoint that returns movie details based on an ID:
```python
@app.get("/movie/{movie_id}")
def get_movie(movie_id: int):
    movie = get_movie_details(movie_id)  # An arbitrary function for demonstration purposes
    if movie:
        return {"movie": movie}
    return {"error": "Movie not found"}
```
Here, `{movie_id}` in the URL will be replaced by the actual movie ID when making a request, and FastAPI will automatically pass it as an argument to your `get_movie()` function.

### `POST` Method

The `POST` method is used to send data to the server to create a new resource. In FastAPI, you use the `@app.post()` decorator to define a function that will handle `POST` requests. The data you want to send to the server is typically included in the request body.

For example, let's create an endpoint to handle recommendations. The user will send a movie ID via a `POST` request, and the server will return a list of recommended movies:

```python
from pydantic import BaseModel

class Movie(BaseModel):
    id: int

@app.post("/recommend")
def recommend_movie(movie: Movie):
    recommendations = get_recommendations(movie.id)  # Assuming this is a function you've defined elsewhere
    return {"recommendations": recommendations}
```

In this example, FastAPI will automatically validate that the incoming request body conforms to the Movie Pydantic model and parse it into the movie parameter. [Pydantic](https://docs.pydantic.dev/latest/) is a tool used to validate data types, we'll get into how it's used for our recommender soon. 

There are several types of HTTP request methods. This project only requires the use of the `GET` and `POST` method. [Here's](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods) a comprehensive list of HTTP methods if you'd like to learn more about the differing methods.

## Creating the Recommender App

Let's now break down the `app.py` file used in this project.

We start with importing the necessary dependencies. Notice how we're utilizing the `get_recommender` function we mentioned in the [previous section](https://ploomber-sql.readthedocs.io/en/latest/mini-projects/recommendation-system/setting-up-a-recommendation-system.html#setting-up-a-content-based-movie-recommender).

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from .recommender import get_recommendation
from fastapi.responses import JSONResponse
import json

app = FastAPI()
```

Then, we create the FastAPI with..

Moving forward, we use a `GET` method to ...

```python 
@app.get("/")
async def root():
    return {
        "message": "Welcome! You can use this API to get movie recommendations based on viewers' votes. Visit /docs for more information and to try it out!"  # noqa E501
    }
```

Then, we use a `POST` method for the main functionality of the app...

```python
@app.post("/recommendations/")
def get_movie_recommendations(recommendation_request: RecommendationRequest):
    """
    Get movie recommendations for a given movie.

    Parameters:
    - movie: The name of the movie for which you want recommendations.
    - num_rec: The number of movie recommendations you want. Default is 10.

    Returns:
    JSON containing recommended movies and metrics.
    """
    recommendations = get_recommendation(
        recommendation_request.movie,
        recommendation_request.num_rec,
        "english",
    )

    if isinstance(recommendations, str):
        recommendations = json.loads(recommendations)

    if not recommendations:
        raise HTTPException(
            status_code=404,
            detail="Movie not found or no recommendations available",  # noqa E501
        )

    return JSONResponse(content=recommendations)
```

Navigate to ... and run the app by

```bash
uvicorn app:app
```

In a browser, go to https://localhost:8000 to access the API. This is the index page. FastAPI has a built in interface using Swagger UI. Insert picture here and work example using Swagger.