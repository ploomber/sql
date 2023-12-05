---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.6
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Sample Ploomber Cloud Deployment

In this blog we will explore how we can deploy Python applications with Ploomber Cloud and GitHub actions. We will use a sample project to demonstrate the process. Imagine you need to extract weather data from an API periodically and store it for analysis. You can achieve this by creating a Python script and scheduling its execution with GitHub Actions. 

```{important}
<b>Note:</b> Please ensure you have reviewed the [deployment with Ploomber Cloud](./deploying-with-ploomber-cloud.md) and [GitHub Actions](./automate-ci-cd-with-github-actions.md) tutorials before proceeding.
```

## Initialize data extraction and data loading script

This script defines functions to extract weather data, transform it into a DataFrame, and populates a Motherduck instance. To review how to initialize a MotherDuck instance, visit the [MotherDuck documentation](https://motherduck.com/docs/getting-started/connect-query-from-python/installation-authentication). You will need to create an account and generate a token. 

The executable script takes as input a list of coordinates and extracts weather data for each coordinate. The script then concatenates all the data frames and saves the result into a CSV file. The CSV file is then uploaded to a Motherduck instance.

You can create a Python script called `dataextraction.py` with the following code. The code has four functions: `extract_weather_by_lat_lon`, `transform_json_to_dataframe`, `extraction_df_lat_lon`, and `save_to_motherduck`. 

* The `extract_weather_by_lat_lon` function extracts weather data from the RapidAPI. 

* The `transform_json_to_dataframe` function transforms the JSON response to a DataFrame. 

* The `extraction_df_lat_lon` function extracts weather data from the RapidAPI and transforms it to a DataFrame. 

* The `save_to_motherduck` function saves the DataFrame to a Motherduck instance.

The main function of the script is the `__main__` function. It loads the API key from an environment variable, extracts weather data for a list of coordinates, concatenates the dataframes, and saves the result to a CSV file. The CSV file is then uploaded to a Motherduck instance.

```{code-cell} ipython3
:tags: [hide-input]

import requests
import pandas as pd
import duckdb


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


def save_to_motherduck(df, motherduck):
    """
    Saves dataframe to MotherDuck

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe to save
    motherduck : str
        MotherDuck service token
    """
    try:
        # Save to csv
        df.to_csv("weather_data.csv", index=False)

        # initiate the MotherDuck connection through a service token through
        con = duckdb.connect(f"md:?motherduck_token={motherduck}")

        # Delete table weatherdata if exists
        con.execute("DROP TABLE IF EXISTS weatherdata")

        # Create table weatherdata
        con.sql("CREATE TABLE weatherdata AS SELECT * FROM 'weather_data.csv'")

    except Exception as e:
        print("Error:", e)
```

To download weather data for different locations, you can replace the latitude and longitude coordinates in the script. The following locations were used in the sample script using the coordinates corresponding to the cities listed below:

|Continent | Cities |
| --- | --- | 
| North America | New York City,  Los Angeles , Toronto | 
| South America | São Paulo ,Buenos Aires, Bogotá |
| Europe | London, Paris,  Berlin |
| Asia | Tokyo , Beijing,Mumbai  |
| Africa | Cairo ,Lagos, Johannesburg  |
| Australia | Sydney ,  Melbourne , Brisbane  |

```python
import os 
from dotenv import load_dotenv 
import pandas as pd 
from dataextraction import extraction_df_lat_lon, save_to_motherduck 
import duckdb 

if __name__ == "__main__":
    # Load api key
    load_dotenv()
    api_key = os.getenv("RapidAPI")
    motherduck = os.getenv("motherduck")
    
   
    # Extract data
    latitudes = [
        40.7128,
        34.0522,
        43.6532,
        -23.5505,
        -34.6037,
        4.7110,
        51.5074,
        48.8566,
        52.5200,
        35.6762,
        39.9042,
        19.0760,
        30.0444,
        6.5244,
        -26.2041,
        -33.8688,
        -37.8136,
        -27.4698,
    ]
    longitudes = [
        -74.0060,
        -118.2437,
        -79.3832,
        -46.6333,
        -58.3816,
        -74.0721,
        -0.1278,
        2.3522,
        13.4050,
        139.6503,
        116.4074,
        72.8777,
        31.2357,
        3.3792,
        28.0473,
        151.2093,
        144.9631,
        153.0251,
    ]
    master_list = []
    for lat, lon in zip(latitudes, longitudes):
        master_list.append(extraction_df_lat_lon(api_key, lat, lon))

    # Concatenate all data frames
    df = pd.concat(master_list)

    # Save to MotherDuck
    save_to_motherduck(df, motherduck)

```

Once you have created the script, you can run it to extract the data. You can also schedule its execution with GitHub Actions. 

## Visualize the data

Let's visualize the data to see what it looks like. We will use the Plotly package. For the purpose of the blog, we read the CSV file, to see what loading the data directly from MotherDuck, please review [this notebook](https://github.com/ploomber/sql/blob/main/mini-projects/end-to-end/app.ipynb).

```{code-cell} ipython3
import pandas as pd  # noqa E402
import plotly.express as px  # noqa E402


df = pd.read_csv("weather.csv")

fig = px.scatter_geo(
    df,
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

The code above creates an interactive map that shows the wind forecast for the next 5 days for the cities in the world. Press the Play > button to see the animation. Let's save this into a notebook called `app.ipynb`.

## Create a GitHub repository and initialize Ploomber Cloud deployment


Create a GitHub repository and add the Python script and Jupyter notebook to it. You can also add a README file to describe your project. 

Next, create a Ploomber Cloud account and initialize the deployment. You can do this by running the following command in your terminal:

```bash
ploomber cloud init
```

This will generate a `ploomber-cloud.json` file. This file contains the configuration for your deployment. You can edit this file to add more information about your deployment. We will create a Dockerfile for our application. 

```python
{
    "id": "generated-id",
    "type": "docker"
}
```

Let's take a look at the Dockerfile. For our deployment we will assume that we are using a Python 3.11 image. We will copy the Jupyter notebook and the `.env` file containing our RapidAPI and MotherDuck tokens to the image. We will install the dependencies and configure the entrypoint.

```dockerfile
FROM python:3.11

# Copy all files 
COPY app.ipynb app.ipynb
COPY .env .env

# install dependencies
RUN pip install voila==0.5.1 pandas==2.0.3 plotly python-dotenv requests duckdb==v0.9.2

# this configuration is needed for your app to work, do not change it
ENTRYPOINT ["voila", "app.ipynb","--port 5000:80"]
```

To deploy this from the terminal, we simply run

```bash
ploomber cloud deploy
```

This will build the image and push it to the Ploomber Cloud registry. You can see the status of your deployment in the Ploomber Cloud dashboard.

## Create a GitHub workflow

The following action is triggered every day at midnight. It runs the Python script to extract the data and deploys the application to Ploomber Cloud. It assumes we have stored our RapidAPI and MotherDuck tokens as GitHub secrets.

```yaml
name: Ploomber cloud deploy,en

on:
  schedule:
    - cron: '0 0 * * *' 

jobs:

  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python 3.10
      uses: actions/setup-python@v3
      with:
        python-version: "3.10"
    - name: Set up credentials
      run: |
          cd mini-projects/end-to-end/
          touch .env
          echo RapidAPI=${{ secrets.RapidAPI }} >> .env
          echo motherduck=${{ secrets.motherduck }} >> .env
    - name: Install dependencies
      run: |
          cd mini-projects/end-to-end/
          pip install -r requirements.txt
    - name: Execute data download
      run: |
          cd mini-projects/end-to-end/
          python dataextraction.py
    - name: Deploy to Ploomber cloud
      run: |
          cd mini-projects/end-to-end/
          ploomber-cloud deploy
```

## Conclusion

In this blog we explored how to deploy Python applications with Ploomber Cloud and GitHub actions. We used a sample project to demonstrate the process. We created a Python script to extract weather data from an API and load it into a Motherduck instance. We then created a Jupyter notebook to visualize the data. We created a GitHub repository and initialized the deployment with Ploomber Cloud. We created a GitHub workflow to run the Python script and deploy the application to Ploomber Cloud.
