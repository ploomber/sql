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

## Building the Pipeline

To implement an ETL pipeline with Canada's vehicle emissions data (introduced in the previous sections), we will use Python's `pandas` and `SQLAlchemy` like so:

1. Use Python's `requests` package to extract the data, documentation [found here](https://pypi.org/project/requests/)
2. Use `pandas` to appropriately transform the data for later use, documentation [found here](https://pandas.pydata.org/docs/)
3. Use `SQLAlchemy` to load the data into a DuckDB file, documentation [found here](https://docs.sqlalchemy.org/en/20/)

In fact, all of these steps are already included in a single script: `datadownload.py`. Navigate to the `pipeline` folder of this course and run the script with this line in your terminal: `python src/datadownload.py`. The script will extract, load, and transform the data and output a DuckDB file in the current folder with the name `car_data.duckdb`.

Before we dive into understanding how this script fundamentally follows an ETL pipeline, note that `pandas` is an extensive package. Comprehensively going through the entire library's documentation would be time-consuming and unnecessary for our understanding of the script. The script relies only on typical `pandas` functions. These include renaming columns appropriately, cleaning data for null values, and creating new columns. 

Let's now dissect `datadownload.py` and focus specifically on key lines of its ETL process.

### Extracting with Python


### Transforming with Python `pandas`

### Loading with `SQL`

Make sure to talk about DB naming conventions.

## Conclusion

Why is it useful from the data science perspective? Why are we choosing to do both the ETL and EDA with these tools?

## Reference 

Informatica, What is ETL (extract transform load)? https://www.informatica.com/resources/articles/what-is-etl.html