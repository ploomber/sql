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

# Testing with Pytest


Testing is an essential part of developing any kind of application, it helps ensure that our code is performing as expected. [Pytest](https://docs.pytest.org/en/7.4.x/index.html) is a tool that helps expedite the testing process. Pytest has a neat functionality of identifying any files that follow the format of `test_*.py` or `*_test.py` in the current directory and its subdirectories. 

Specifically, let's focus on the `/tests` folder. Pytest will automatically run tests on the `test_app.py` file under the `/tests` folder. To see Pytest in action, navigate to `mini-projects/movie-rec-system` and run the following command:

```bash
pytest
```
Let's take a closer look at `test_app.py` to understand exactly what we're testing in this project.

## Testing the FastAPI Application

We begin with importing the necessary dependencies.

```python
from fastapi.testclient import TestClient
from movie_rec_system.app.app import app

client = TestClient(app)
```

We import the `app` we've made from the [previous section](https://ploomber-sql.readthedocs.io/en/latest/mini-projects/recommendation-system/setting-up-fastapi.html#creating-the-recommender-app) under the `app.py` file. Then, we initialize the `TestClient` object by passing in our FastAPI app. What the `TestClient` object does is simulate HTTP requests to the FastAPI application, allowing us to test its responses and behavior. You can find more details about this in the [TestClient](https://fastapi.tiangolo.com/tutorial/testing/) documentation.

Let's now break down each of our tests.

### Test Root Endpoint

We begin with just testing if the root endpoint is accessible and returns the expected message.

```python
def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome! You can use this API to get movie recommendations based on viewers' votes. Visit /docs for more information and to try it out!"  # noqa E501
    }
```

In this test, we use the client.get("/") to simulate a GET request to the root endpoint and then make assertions to check if the status code is `200` and the message returned is as expected.

### Test Recommendation Endpoint

Then we test if our endpoint can handle movie recommendations.

```python
def test_recommendation_endpoint():
    test_data = {"movie": "Inception", "num_rec": 5}
    response = client.post("/recommendations/", json=test_data)
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["movie"] == "inception"
```

Here, we send a `POST` request with the `movie` and `num_rec` as part of the request payload. We then assert that the returned status code is `200` and that the movie name in the response data matches the movie name we sent.

### Test for Nonexistent Movie

As for edge cases, let's test what happens when a nonexistent movie is provided:

```python
def test_recommendation_for_nonexistent_movie():
    test_data = {"movie": "NonExistentMovie", "num_rec": 5}
    response = client.post("/recommendations/", json=test_data)
    assert response.status_code == 404
```
In this test, we are ensuring that our API correctly handles the situation where a user requests a movie that doesn't exist. We expect a `404` status code for this case.

### Test Recommendation Result

Finally, let's have just one final test that validates the structure and the types of the fields in the response:

```python
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
```

This comprehensive test ensures that the movie name is a string, that recommendations are returned as a list of the expected size, and that various metrics (like popularity, average votes, and vote counts) are included in the response and have the correct types.

And there you have it! We now have a set of tests that can validate various aspects of your FastAPI application.

Happy testing!