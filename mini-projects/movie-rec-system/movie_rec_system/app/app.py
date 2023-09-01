from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from .recommender import get_recommendation
from fastapi.responses import JSONResponse
import json

app = FastAPI()


class RecommendationRequest(BaseModel):
    movie: str
    num_rec: int = 10

    @validator("movie", pre=True, always=True)
    def format_movie_name(cls, movie_name):
        """Ensure the movie name is formatted with the
        first letter capitalized."""
        return movie_name.title()  # Convert to title case


@app.get("/")
async def root():
    return {
        "message": "Welcome! You can use this API to get movie recommendations based on viewers' votes. Visit /docs for more information and to try it out!"  # noqa E501
    }


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
