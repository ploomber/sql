---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.5
kernelspec:
  display_name: jupyblog
  language: python
  name: python3
---


# Aggregate functions in SQL

In the last section, we learned the basics of SQL. We now build upon those basics to learn a common use case of SQL: <b>aggregation functions</b>. 

Aggregation functions are useful for summarizing your data and for finding meaningful insights. The most common of these functions are `COUNT()`, `AVG()`, `SUM()`, `MIN()`, and `MAX()`. We will go over each of these functions in detail with our bank marketing dataset.

Let's first run the installations and setup before running any queries, just like the last lesson `making-your-first-query`.

### Install - execute this once. 

This code installs JupySQL, DuckDB, and Pandas in your environment. We will be using these moving forward.

```{code-cell} ipython3
%pip install jupysql --upgrade duckdb-engine pandas --quiet
```

### Load the data
We extract the bank marketing data by retrieving it from it's URL download link. The link may be a zip file (which it is in this case), so we extract the zip file, read the file containing the data within the zip file, and clean the data. Finally, we save this cleaned data to it's own seperate file called `bank_cleaned.csv`.  
```python
from urllib.request import urlretrieve
from zipfile import ZipFile
import pandas as pd
import os

def extract_to_csv(url):
  #Retrieve the zip file from the url link
  file = os.path.basename(url)
  urlretrieve(url, file)

  #Extract the zip file's contents
  with ZipFile(file, 'r') as zf:
    zf.extractall()

  #The file containing our data
  csv_file_name = 'bank.csv'

  # Data clean up
  df = pd.read_csv(csv_file_name, sep = ";")

  # Save the cleaned up CSV file
  df.to_csv('bank_cleaned.csv', index=False) 

#Running the above function
extract_to_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank.zip')
  ```
After running this code, you should have `bank_cleaned.csv` in the current directory. 

### Load Engine
We now load in our SQL extension that allows us to execute SQL queries in Jupyter Notebooks. 

<b>Note</b> Ensure you restart any previous notebook that has the same database name as the one initialized below.

```{code-cell} ipython3
# Loading in SQL extension
%reload_ext sql
# Initiating a DuckDB database named 'bank.duck.db' to run our SQL queries on
%sql duckdb:///bank.duck.db
```

Let's now return to our initial dataset of bank marketing records. 

### Queries

#### Creating Table

Let's start off with loading our `bank_cleaned.csv` file from our local directory to our newly created DuckDB database. Here we `CREATE OR REPLACE TABLE` in DuckDB called 'bank' `FROM` our `bank_cleaned.csv` file. The `read_csv_auto` is a function that helps SQL understand our local .csv file for creation into our database.

```{code-cell} ipython3
%%sql
CREATE OR REPLACE TABLE bank AS
FROM read_csv_auto('bank_cleaned.csv', header=True, sep=',')
```

#### Count and Distinct Count
`COUNT()` allows users to query the count of records in a given query. A common argument to this function is `*`. `COUNT(*)` tells SQL to return the total number of rows from our query, including NULL values. This can be combined with queries that filter for certain conditions.

A common function to be used with `COUNT()` is `DISTINCT()`. For example, selecting `COUNT(DISTINCT(job))` would return the count of distinct values under the "job" column.

```{code-cell} ipython3
%%sql 
SELECT COUNT(DISTINCT(job))
FROM bank 
```

Here's an example with `COUNT()` that counts the number of rows of our query `WHERE` we filter for "balance" greather than or equal to 500 `AND` where "martial" equals married.

```{code-cell} ipython3
%%sql 
SELECT COUNT(*)
FROM bank 
WHERE balance > 500 AND martial = 'married'
```

`COUNT()` can also have the arguments of a single row, such as `COUNT(job)`. `COUNT(job)` would count the number of rows of just the "job" column. If "job" were to have any NULL values in its query, those NULL values would be subtracted from the total row counts of the query. 

#### Average








