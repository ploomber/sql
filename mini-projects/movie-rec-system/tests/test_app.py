from fastapi.testclient import TestClient
from movie_rec_system.app.app import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome! You can use this API to get movie recommendations based on viewers' votes. Visit /docs for more information and to try it out!"
    }

def test_recommendation_endpoint():
    test_data = {
        "movie": "Inception",
        "num_rec": 5
    }
    response = client.post("/recommendations/", json=test_data)
    assert response.status_code == 200
    
    response_data = response.json()
    assert response_data["movie"] == "inception"    

def test_recommendation_for_nonexistent_movie():
    test_data = {
        "movie": "NonExistentMovie",
        "num_rec": 5
    }
    response = client.post("/recommendations/", json=test_data)
    assert response.status_code == 404
