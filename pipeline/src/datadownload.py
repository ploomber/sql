import pandas as pd
import requests
import sys
import os
from pathlib import Path
import re
import duckdb

# Get the current working directory
current_working_directory = os.getcwd()

# Convert the current working directory to a Path object
script_dir = Path(current_working_directory)

global model_dict
global transmission_dict
global fuel_dict
global stats_can_dict
global month_dic

model_dict = {
    "4wd/4X4": "Four-wheel drive",
    "awd": "All-wheel drive",
    "ffv": "Flexible-fuel vehicle",
    "swb": "Short wheelbase",
    "lwb": "Long wheelbase",
    "ewb": "Extended wheelbase",
    "cng": "Compressed natural gas",
    "ngv": "Natural gas vehicle",
    "#": "High output engine that \
            provides more power than the standard \
            engine of the same size",
}

transmission_dict = {
    "A": "automatic",
    "AM": "automated manual",
    "AS": "automatic with select Shift",
    "AV": "continuously variable",
    "M": "manual",
    "1 – 10": "Number of gears",
}

fuel_dict = {
    "X": "regular gasoline",
    "Z": "premium gasoline",
    "D": "diesel",
    "E": "ethanol (E85)",
    "N": "natural gas",
    "B": "electricity",
}

hybrid_fuel_dict = {
    "B/X": "electricity & regular gasoline",
    "B/Z": "electricity & premium gasoline",
    "B/Z*": "electricity & premium gasoline",
    "B/X*": "electricity & regular gasoline",
    "B": "electricity",
}

stats_can_dict = {
    "new_motor_vehicle_reg": "https://www150.statcan.gc.ca/n1/tbl/csv/20100024-eng.zip",  # noqa E501
    "near_zero_vehicle_registrations": "https://www150.statcan.gc.ca/n1/tbl/csv/20100025-eng.zip",  # noqa E501
    "fuel_sold_motor_vehicles": "https://www150.statcan.gc.ca/n1/tbl/csv/23100066-eng.zip",  # noqa E501
    "vehicle_registrations_type_vehicle": "https://www150.statcan.gc.ca/n1/tbl/csv/23100067-eng.zip",  # noqa E501
}

month_dic = {
    "jan": "01",
    "feb": "02",
    "mar": "03",
    "apr": "04",
    "may": "05",
    "jun": "06",
    "jul": "07",
    "aug": "08",
    "sep": "09",
    "oct": "10",
    "nov": "11",
    "dec": "12",
}


def fuel_consumption_metadata_extraction() -> pd.DataFrame:
    """
    Extract metadata from fuel consumption data

    Returns
    -------
    final_result : pd.DataFrame
        Dataframe containing metadata from fuel consumption data
    """
    try:
        # Extract data in JSON format from URL
        url_open_canada = "https://open.canada.ca/data/api/action/package_show?id=98f1a129-f628-4ce4-b24d-6f16bf24dd64"  # noqa E501
        json_resp = requests.get(url_open_canada)
        # Check response is successful and application is of type JSON
        if (
            json_resp.status_code == 200
            and "application/json" in json_resp.headers.get("Content-Type", "")
        ):
            # Format data and obtain entries in english
            open_canada_data = json_resp.json()
            data_entries = pd.json_normalize(
                open_canada_data["result"], record_path="resources"
            )
            data_entries["language"] = data_entries["language"].apply(
                lambda col: col[0]
            )
            data_entries_english = data_entries[
                data_entries["language"] == "en"
            ]  # noqa E501
            final_result = data_entries_english[["name", "url"]]
        else:
            print(
                "Error - check the url is still valid \
                https://open.canada.ca/data/api/action/package_show?id=98f1a129-f628-4ce4-b24d-6f16bf24dd64"  # noqa E501
            )
            final_result = pd.DataFrame(columns=["name", "url"])
            sys.exit(1)
        return final_result
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)


# +
def extract_raw_data(url: str):
    """
    Extract raw data from a URL

    Parameters
    ----------
    url : str
        URL to extract data from

    """
    try:
        # Perform query
        csv_req = requests.get(url)
        # Parse content
        url_content = csv_req

        return url_content
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)


# +
def save_raw_data(folder_path: str, url_content: str, file_name: str) -> None:
    """
    This function saves the raw data obtained using
    extract_raw_data() into a CSV file

    Parameters
    ----------
    folder_path : str
        Path to the folder where the data will be saved
    url_content : str
        Content of the URL to be saved
    file_name : str
        Name of the file to save the data

    Returns
    -------
    None.
    """
    # Save content into file
    csv_file = open(Path(folder_path, file_name), "wb")
    csv_file.write(url_content.content)
    csv_file.close()


def rename_fuel_data_columns(folder_path, csv_file_name) -> pd.DataFrame:
    """
    This function reads a csv and changes its column names
    to lowecase, removes spaces and replaces them with underscores
    and removes the pound sign from the column names

    This function assumes the original csv file has two headers!!!

    Parameters
    ----------
    folder_path : str
        Path to the folder where the data is saved
    csv_file_name : str
        Name of the csv file to be read

    Returns
    -------
        final_df : pd.DataFrame
    """

    # Read CSV file
    df = pd.read_csv(
        Path(folder_path, csv_file_name),
        sep=",",
        low_memory=False,
        encoding="cp1252",  # noqa E501
    )

    # Data cleaning
    sample_df_col = df.dropna(thresh=1, axis=1).dropna(thresh=1, axis=0)
    sample_df_col.columns = [item.lower() for item in sample_df_col.columns]
    sample_df_no_footer = sample_df_col.dropna(thresh=3, axis=0)

    # Remove Unnamed cols
    cols = sample_df_no_footer.columns
    cleaned_cols = [
        re.sub(r"unnamed: \d*", "fuel consumption", item)
        if "unnamed" in item
        else item  # noqa E501
        for item in cols
    ]

    # Clean row 1 on df
    str_item_cols = [
        str(item) for item in sample_df_no_footer.iloc[0:1,].values[0]
    ]  # noqa E501
    str_non_nan = ["" if item == "nan" else item for item in str_item_cols]

    # Form new columns
    new_cols = []
    for itema, itemb in zip(cleaned_cols, str_non_nan):
        new_cols.append(
            f"{itema}_{itemb}".lower()
            .replace("*", "")
            .replace(" ", "")
            .replace(r"#=highoutputengine", "")
        )

    # Reset column names
    final_df = sample_df_no_footer.iloc[1:,].copy()
    final_df.columns = new_cols

    return final_df


# +
def read_and_clean_csv_file(folder_path, csv_file_name) -> pd.DataFrame:
    """
    This function reads a csv file and performs data cleaning

    Parameters
    ----------
    folder_path : str
        Path to the folder where the data is saved
    csv_file_name : str
        Name of the csv file to be read

    Returns
    -------
    final_df : pd.DataFrame
        Dataframe containing the cleaned data

    """

    final_df = rename_fuel_data_columns(folder_path, csv_file_name)

    # Additional data cleaning
    final_df.drop_duplicates(keep="first", inplace=True)

    # Turn make, model.1_, vehicleclass_ into lowercase
    final_df["make_"] = final_df["make_"].str.lower().str.strip()
    final_df["model.1_"] = final_df["model.1_"].str.lower()
    final_df["vehicleclass_"] = final_df["vehicleclass_"].str.lower()

    # Character cleaning for vehicleclass_: replace ":" with "-"
    final_df["vehicleclass_"] = final_df["vehicleclass_"].str.replace(
        ":", " -"
    )  # noqa E501

    # Turn make, model.1_, vehicleclass_ into categorical variables
    final_df["make_"] = final_df["make_"].astype("category")
    final_df["model.1_"] = final_df["model.1_"].astype("category")
    final_df["vehicleclass_"] = final_df["vehicleclass_"].astype("category")

    # Mappings
    final_df = final_df.join(
        final_df["transmission_"]
        .str.split(r"(\d+)", expand=True)
        .drop(columns=[2])
        .rename(columns={0: "transmission_type", 1: "number_of_gears"})
    )
    final_df["transmission_type"] = final_df["transmission_type"].map(
        transmission_dict
    )  # noqa E501

    return final_df


# +
def convert_model_key_words(s, dictionary):
    """
    Add values from footnote
    Parameters
    ----------
    s : pd.Series
        row of dataframe
    dictionary : dict
        one of the dictionaries defined globally.
    """

    group = "unspecified"
    for key in dictionary:
        if key in s:
            group = dictionary[key]
            break
    return group


if __name__ == "__main__":
    # Variable initialization
    raw_data_path = script_dir / "data" / "raw"
    clean_data_path = script_dir / "data" / "processed"
    clean_data_DB_path = current_working_directory

    print("Raw data path: ", raw_data_path)
    print("Clean data path: ", clean_data_path)
    print("Clean data DB path: ", clean_data_DB_path)

    # Master dataframe initialization
    fuel_based_df = []

    # Fuel consumption metadata extraction urls
    data_entries_english = fuel_consumption_metadata_extraction()

    # Iterate over entries
    for item in data_entries_english.iterrows():
        name, url = item[1]["name"], item[1]["url"]

        if "Original" in name:
            continue

        # Form file name
        file_name = f'{name.replace(" ","_")}.csv'

        # Extract raw data
        item_based_url = extract_raw_data(url)

        # Save raw data into a csv file
        save_raw_data(raw_data_path, item_based_url, file_name)

        # Read and clean csv file
        final_df = read_and_clean_csv_file(
            raw_data_path, name.replace(" ", "_") + ".csv"
        )

        # Populate dataframe with information from the footnotes
        if "hybrid" in name:
            # Strip numbers from file_name
            name = re.sub(r"\d+", "", name)
            # Strip parenthesis and - from name
            name = name.replace("(", "").replace(")", "").replace("-", "")
            # Form file name
            file_name = f'{name.replace(" ","_")}.csv'

            final_df.rename(
                columns={
                    "fuel.1_type2": "fuel_type2",
                    "consumption.1_city(l/100km)": "fuelconsumption_city(l/100km)",  # noqa E501
                },
                inplace=True,
            )
            final_df["mapped_fuel_type"] = final_df["fuel_type2"].map(
                fuel_dict
            )  # noqa E501
            final_df["hybrid_fuels"] = final_df["fuel_type1"].map(
                hybrid_fuel_dict
            )  # noqa E501

            final_df["id"] = range(1, len(final_df) + 1)
            final_df["vehicle_type"] = "hybrid"
            final_df.to_csv(Path(clean_data_path, file_name), index=False)
        elif "electric" in name and "hybrid" not in name:
            # Strip numbers from file_name
            name = re.sub(r"\d+", "", name)
            # Strip parenthesis and - from name
            name = name.replace("(", "").replace(")", "").replace("-", "")
            # Form file name
            file_name = f'{name.replace(" ","_")}.csv'

            final_df["mapped_fuel_type"] = final_df["fuel_type"].map(fuel_dict)
            final_df["id"] = range(1, len(final_df) + 1)
            final_df["vehicle_type"] = "electric"
            final_df.to_csv(Path(clean_data_path, file_name), index=False)
        else:
            final_df["mapped_fuel_type"] = final_df["fuel_type"].map(fuel_dict)
            final_df["type_of_wheel_drive"] = final_df["model.1_"].apply(
                lambda x: convert_model_key_words(x, model_dict)
            )
            fuel_based_df.append(final_df)

    # Concatenate all dataframes
    fuel_based_df = pd.concat(fuel_based_df)

    # add an id column where each row is a unique id (1, 2, 3, 4, ...)
    fuel_based_df["id"] = range(1, len(fuel_based_df) + 1)

    # Add a column called vehicle_type
    fuel_based_df["vehicle_type"] = "fuel-only"

    # Save dataframes
    fuel_based_df.to_csv(
        Path(clean_data_path, "1995_today_vehicle_fuel_consumption.csv"),
        index=False,  # noqa E501
    )


# Path to processed data directory
gas_vehicles_csv = os.path.join(
    current_working_directory,
    "data",
    "processed",
    "1995_today_vehicle_fuel_consumption.csv",
)
electric_vehicles_csv = os.path.join(
    current_working_directory,
    "data",
    "processed",
    "Batteryelectric_vehicles__.csv",  # noqa E501
)
hybrid_vehicles_csv = os.path.join(
    current_working_directory,
    "data",
    "processed",
    "Plugin_hybrid_electric_vehicles__.csv",
)

# Creating a new directory for DuckDB tables
database_directory = os.path.join(
    current_working_directory, "data", "database"
)  # noqa E501
Path(database_directory).mkdir(parents=True, exist_ok=True)

# Creating DuckDB file at new directory
duckdb_file_path = os.path.join(database_directory, "car_data.duck.db")

con = duckdb.connect(duckdb_file_path)

# Drop tables if they exist
con.execute("DROP TABLE IF EXISTS fuel")
con.execute("DROP TABLE IF EXISTS electric")
con.execute("DROP TABLE IF EXISTS hybrid")

# Creating tables
con.execute(
    f"CREATE TABLE fuel AS SELECT * FROM read_csv_auto ('{gas_vehicles_csv}')"
)  # noqa E501
con.execute(
    f"CREATE TABLE electric AS SELECT * FROM read_csv_auto ('{electric_vehicles_csv}')"  # noqa E501
)
con.execute(
    f"CREATE TABLE hybrid AS SELECT * FROM read_csv_auto ('{hybrid_vehicles_csv}')"  # noqa E501
)


con.close()
