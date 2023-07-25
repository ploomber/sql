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

# Building an ETL pipeline with Python and SQL

In this section of the course, you'll learn how to create your own ETL pipeline with Python and SQL. But before we get into the nitty gritty, we first have to answer the question: what are **ETL Pipelines**?

## ETL Pipelines

![](etl-process-explained-diagram.png)

ETL (Extract, Transform, Load) pipelines are essential tools in the world of data engineering and analysis. They play a crucial role in collecting, cleaning, and preparing data for analysis or storage in databases. The three stages of ETL each serve a distinct purpose in the data pipeline:

1. Extract: In the extraction phase, data can be collected from multiple sources, such as databases, APIs, files, or web scraping. Python provides powerful libraries and modules, such as `pandas` and `requests`, that simplify data extraction tasks.

2. Transform: Once data is extracted, it often needs to be transformed to make it suitable for analysis or to meet specific requirements. Data transformation involves tasks like cleaning, filtering, aggregating, and/or joining, all things you should be familiar with by this point. This process can be done with either Python's `pandas` or SQL. 

3. Load: The final stage of the ETL pipeline is loading the transformed data, typically into a database. This step ensures that the data is stored in an easy to access format that allows for additional analysis. SQL is commonly used for interacting with databases, and Python provides libraries like `SQLAlchemy` for seamless integration. For this course, we'll focus on loading our data into a familiar database: DuckDB.

ETLs are essential for the data science work flow, as it aligns with the day-to-day tasks of modern day data scientist. This process provides data in a format that allows data scientists to readily use the data for predictive or inference modeling. Ultimately, this framework handles a significant portion of data preparation, allowing data scientists to concentrate on the modeling phase of their work. 

## Building the Pipeline

To implement an ETL pipeline with Canada's vehicle emissions data (introduced in the previous sections), we will use Python's `pandas` and `SQLAlchemy` like so:

1. Use Python's `requests` package to extract the data, documentation [found here](https://pypi.org/project/requests/)
2. Use `pandas` to appropriately transform the data for later use, documentation [found here](https://pandas.pydata.org/docs/)
3. Use `SQLAlchemy` to load the data into a DuckDB file, documentation [found here](https://docs.sqlalchemy.org/en/20/)

In fact, all of these steps are already included in a single script: `datadownload.py`. This script can be found from the course's GitHub repo that you can clone from here:

`git clone https://github.com/ploomber/sql.git`

Once you clone the repo, make sure that you have the correct dependencies by following the "Setup" instructions under the `CONTRIBUTING.md` files. Once you have the correct dependencies and environment, navigate to the `pipeline` folder and run the script with this line in your terminal: `python src/datadownload.py`. The script will extract, load, and transform the data and output a DuckDB file in the current folder with the name `car_data.duckdb`.

Before we dive into understanding how this script fundamentally follows an ETL pipeline, we have to briefly expand on some key points regarding DuckDB and `pandas`:

1. We use DuckDB because it allows us to store data in an in-memory database. Typically, the "loading" part of ETLs would require a server that hosts a database and usually requires additional configurations. DuckDB disregards the need for servers and allows users to locally load data. In our case, you can think of `car_data.duckdb` as our local database that we will be running queries against. DuckDB is an efficient and easy to set up database that is especially useful the in initial stages of the data science workflow. This database allows data scientists to check the usefulness of the data without having to cumbersomely set up a server to host the data. Reference the [previous module](https://ploomber-sql.readthedocs.io/en/latest/packaging-your-sql-project/intro-to-python-scripting-and-pipelines.html) to learn more about using Python with DuckDB. 

2. `pandas` is an extensive package. Comprehensively going through the entire library's documentation would be time-consuming and unnecessary for your understanding of the script. The script relies only on typical `pandas` functions, such as ones that help rename columns appropriately, clean data for null values, and create new columns. 

Let's now dissect `datadownload.py` and focus specifically on key lines of its ETL process.

![](etl-co2-sample.jpg)

### Extracting with Python

Take a look at the function `fuel_consumption_metadata_extraction`. On lines 100 - 115, we access the Government of Canada's API and extract data regarding fuel consumption ratings that are in English. The output of this function is a `pandas` data frame with two columns: "name" and "url". Each row in the data frame corresponds to a single data set under the fuel consumptions ratings portfolio that is in English.  

```python
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
```

We then finalize the extraction process by saving each data set in its raw format as its own `pandas` data frame from  `final_result`. This is done with the `extract_raw_data` functions under a `for loop` in the script's main call on lines 342 - 358.

```python
# Fuel consumption metadata extraction urls
data_entries_english = fuel_consumption_metadata_extraction()

for item in data_entries_english.iterrows():
    name, url = item[1]["name"], item[1]["url"]

    if "Original" in name:
        continue

    # Form file name
    file_name = f'{name.replace(" ","_")}.csv'

    # Extract raw data
    item_based_url = extract_raw_data(url)

    # Read and clean as pandas df
    df = pd.read_csv(StringIO(item_based_url.text), low_memory=False)
```


### Transforming with Python `pandas`

We clean each of the extracted data sets with the `read_and_clean` function prior to any other transformations. This function is called immediately after the above lines on line 359. 

```python
final_df = read_and_clean_df(df)
```

A large bulk of the script is dedicated to transforming the data into our desired format. Under the `for loop` and after the extraction process described in the above section, we condition the values of the `name` column of our `data_entries_english` `pandas` data frame that contains the name and url of each data set. The script then perform the appropriate transformations conditioned on whether the data set regards hybrid, electric, or gas type vehicles. 

Much of the `pandas` transformations in this section are repeatedly used throughout this script. These functions are easily inferred based on their syntax, such as `replace`, `rename`, and `map`. Because of how repetitive and lengthy the code is, we won't show it in detail for this section. Rather, the main takeaway is that `pandas` transformations are not that difficult to grasp and that they do not stray too far away from SQL functionality. 

After performing the appropriate transformations, we create one last additional `pandas` data frame in memory with the `concatenate_dataframes` function on line 461. This data frame is the concatenation of all the transformed datasets thus far.

```python
all_vehicles_df = concatenate_dataframes(fuel_based_df, hybrid_df, electric_df)
```

With this, we're ready to move forward and complete the last step of loading our data into a DuckDB file.

### Loading with `SQL`

Our last step simply loads our transformed data from their `pandas` data frame format into a DuckDB data base. 

We first create a directory to store our DuckDB file based on our current working directory. We then populate this newly created directory under `pipeline/data/database` with a file called `car_data.duckdb`. This can be seen on lines 463 - 470.

```python
# Creating a new directory for DuckDB tables
database_directory = os.path.join(
    current_working_directory, "data", "database"
)  # noqa E501
Path(database_directory).mkdir(parents=True, exist_ok=True)

# Creating DuckDB file at new directory
duckdb_file_path = os.path.join(database_directory, "car_data.duckdb")
```

Why are we naming the DuckDB file `car_data.duckdb`? We thought it would be appropriate given our data and because we think it follows the de facto standard of database naming conventions. [This article](https://dev.to/ovid/database-naming-standards-2061) is a great resource to learn more about this good to follow practice.

Focusing back to our script, we finalize this process with loading our data into `car_data.duckb` by using `duckdb`, a DuckDB `python` API. Lines 472 - 487 ensures that `car_data.duckb` creates the appropriate tables in our newly created data base. For more information on DuckDB's python API, please visit the official documentation [found here](https://duckdb.org/docs/api/python/overview).

```python
con = duckdb.connect(duckdb_file_path)

# Drop tables if they exist
con.execute("DROP TABLE IF EXISTS fuel")
con.execute("DROP TABLE IF EXISTS electric")
con.execute("DROP TABLE IF EXISTS hybrid")
con.execute("DROP TABLE IF EXISTS all_vehicles")

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
con.execute(
    f"CREATE TABLE all_vehicles AS SELECT * FROM read_csv_auto ('{all_vehicles_csv}')"  # noqa E501
)

con.close()
```

And that's it! You've just learned an overview of an ETL pipeline regarding the `co2_data` we'll be working with. 

## Conclusion

We've just demonstrated how the `datadownload.py` script creates an ETL pipeline with `pandas`, `requests` and DuckDB. You may be wondering why we're working with this specific tech stack. To be honest, it's because they're widely used, and for good reason. You've just seen first hand of how easy it is to create an ETL pipeline with just these tools. Remember, these are **just tools** that are one of many in a sea of others. We decided to use them because of how easy they are to use and to understand, especially in a course setting.

Moving forward, we can finally officially start running some EDA on our data in the `car_data.duckdb` DuckDB database and with `JupySQL`. Stay tuned!

## References

Informatica, What is ETL (extract transform load)? https://www.informatica.com/resources/articles/what-is-etl.html

Python `requests` 2.31.0, Updated May 22, 2023 https://pypi.org/project/requests/

Python `pandas` 2.0.3 https://pypi.org/project/requests/

SQL Alchemy 2.0 https://docs.sqlalchemy.org/en/20/

SQL Course Repository https://github.com/ploomber/sql

Database Naming Standard, Mar. 2 2021, Ovid https://dev.to/ovid/database-naming-standards-2061

DuckDB Python API https://dev.to/ovid/database-naming-standards-2061


