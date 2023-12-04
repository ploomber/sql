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

    # Concatenate all dataframes
    df = pd.concat(master_list)

    # Save to csv
    df.to_csv("weather.csv", index=False)
