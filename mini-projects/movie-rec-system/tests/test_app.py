from fastapi.testclient import TestClient
from movie_rec_system.app.app import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome! You can use this API to get movie recommendations based on viewers' votes. Visit /docs for more information and to try it out!"  # noqa E501
    }


def test_recommendation_endpoint():
    test_data = {"movie": "Inception", "num_rec": 5}
    response = client.post("/recommendations/", json=test_data)
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["movie"] == "inception"


def test_recommendation_for_nonexistent_movie():
    test_data = {"movie": "NonExistentMovie", "num_rec": 5}
    response = client.post("/recommendations/", json=test_data)
    assert response.status_code == 404


def test_recommendation_result():
    test_data = {"movie": "Inception", "num_rec": 5}
    response = client.post("/recommendations/", json=test_data)
    assert response.status_code == 200

    response_data = response.json()

    assert isinstance(response_data["movie"], str)

    assert isinstance(response_data["recommendations"], list)
    assert len(response_data["recommendations"]) == test_data["num_rec"]

    assert isinstance(response_data["metrics"], dict)
    metrics = response_data["metrics"]

    assert "popularity" in metrics
    assert "vote_avg" in metrics
    assert "vote_count" in metrics

    assert isinstance(metrics["popularity"], float)
    assert isinstance(metrics["vote_avg"], float)
    assert isinstance(metrics["vote_count"], float)
