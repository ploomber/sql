from fastapi import FastAPI, HTTPException
from functools import lru_cache

from recommender import get_recommendation

app = FastAPI()

@app.get("/recommendations/")
def get_movie_recommendations(movie: str, num_rec: int = 10, stop_words: str = "english"):
    """
    Get movie recommendations for a given movie.

    Parameters:
    - movie: The name of the movie for which you want recommendations.
    - num_rec: The number of movie recommendations you want. Default is 10.
    - stop_words: The language for stop words. Default is "english".

    Returns:
    JSON containing recommended movies and metrics.
    """
    recommendations = get_recommendation(movie, num_rec, stop_words)
    
    if not recommendations:
        raise HTTPException(status_code=404, detail="Movie not found or no recommendations available")

    return recommendations
