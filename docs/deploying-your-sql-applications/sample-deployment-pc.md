---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.5
---

# Sample Ploomber Cloud Deployment

In this blog we will explore how we can deploy Python applications with Ploomber Cloud and GitHub actions. We will use a sample project to demonstrate the process. Imagine you need to extract weather data from an API periodically and store it for analysis. You can achieve this by creating a Python script and scheduling its execution with GitHub Actions. 

## Initialize data extraction script

This script defines functions to extract weather data, transform it into a DataFrame, and save it as a CSV file. You can replace the latitude and longitude coordinates with locations of your choice.

```python
import requests
import pandas as pd
from dotenv import load_dotenv
import os


def extract_weather_by_lat_lon(api_key, lat, lon):
    """
    Extracts weather data from RapidAPI
    
    Parameters
    ----------
    api_key : str
        API key for RapidAPI    
    lat : float
        Latitude
    lon : float
        Longitude
    """
    try:
        # Perform call
        url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

        querystring = {"q": f"{lat},{lon}", "days": "5"}

        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com",
        }

        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(e.response.text)
        return {}


def transform_json_to_dataframe(response):
    """
    Transforms JSON response to dataframe

    Parameters
    ----------
    response : dict
        Response from API call
    """
    try:
        unnested_df = pd.json_normalize(
            response,
            record_path=["forecast", "forecastday", "hour"],
            meta=["location", "current"],
        )
        unnested_df.drop(columns=["location", "current"], inplace=True)

        location_df = pd.json_normalize(response["location"])

        for col_name in location_df.columns:
            unnested_df[col_name] = location_df[col_name][0]

        return unnested_df

    except KeyError as e:
        print("Key Error:", e)
        return pd.DataFrame()
    except Exception as e:
        print("Other Error:", e)
        return pd.DataFrame()


def extraction_df_lat_lon(api_key, lat, lon):
    """
    Extracts weather data from RapidAPI and transforms it to a dataframe

    Parameters
    ----------
    api_key : str
        API key for RapidAPI
    lat : float
    lon : float

    Returns
    -------
    df : pandas.DataFrame
        Weather data

    """
    response = extract_weather_by_lat_lon(api_key, lat, lon)
    return transform_json_to_dataframe(response)

if __name__ == "__main__":
    # Load api key
    load_dotenv()
    api_key = os.getenv("RapidAPI")

    # Extract data
    latitudes = [
        40.7128,
        34.0522,
        43.6532
    ]
    longitudes = [
        -74.0060,
        -118.2437,
        -79.3832
    ]
    master_list = []
    for lat, lon in zip(latitudes, longitudes):
        master_list.append(extraction_df_lat_lon(api_key, lat, lon))

    # Concatenate all dataframes
    df = pd.concat(master_list)

    # Save to csv
    df.to_csv("weather.csv", index=False)

```

## Visualize the data

Let's visualize the data to see what it looks like. We will use the Plotly package.

```{code-cell} ipython3
import pandas as pd
import plotly.express as px

df = pd.read_csv("weather.csv")

fig = px.scatter_geo(
    df[df["time"] > "2023-12-02"],
    lat="lat",
    lon="lon",
    color="region",
    hover_name="country",
    size="wind_kph",
    animation_frame="time",
    projection="natural earth",
    title="Wind forecast (next 5 days) in kph for cities in the world",
)

fig.show()
```

## Create a GitHub repository and initializing Ploomber Cloud deployment

Create a GitHub repository and add the Python script and Jupyter notebook to it. You can also add a README file to describe your project. 

Next, create a Ploomber Cloud account and initialize the deployment. You can do this by running the following command in your terminal:

```bash
ploomber cloud init
```
