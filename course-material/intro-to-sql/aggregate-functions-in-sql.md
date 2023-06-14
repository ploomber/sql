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

# Aggregate functions in SQL

In the last section, we learned the basics of SQL. We now build upon those basics to learn a common use case of SQL: <b>aggregation functions</b>. 

Aggregation functions are useful for summarizing your data and for finding meaningful insights. The most common of these functions are `COUNT()`, `AVG()`, `SUM()`, `MIN()`, and `MAX()`. We will go over each of these functions in detail with our bank marketing dataset.

We will also introduce the important clause `GROUP BY`. This clause can only be used if, and only if, aggregation functions are used. However, note that aggregation functions can be used without `GROUP BY`. `GROUP BY` groups unique values in columns together and runs an aggregation function on each unique group. Examples of using `GROUP BY` will be provided after introducing aggregate functions.

Let's first run the installations and setup before running any queries, just like the last lesson `making-your-first-query`.

<!-- region -->

## Install - execute this once. 
<b>Note:</b> If you are following these lessons locally and <b>not</b> on Google Colab, then there is no need to reinstall these packages.

This code installs JupySQL, DuckDB, and Pandas in your environment. We will be using these moving forward.

```{code-cell} ipython3
%pip install jupysql --upgrade duckdb-engine --quiet
```

## Load the data
<b>Note:</b> If you are following these lessons locally and <b>not</b> on Google Colab, then there is no need to load the data again.

The data is downloaded from https://archive-beta.ics.uci.edu/dataset/222/bank+marketing via the url https://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank.zip.

We extract the bank marketing data by retrieving it from it's URL download link. The link may be a zip file (which it is in this case), so we extract the zip file, read the file containing the data within the zip file, and clean the data. Finally, we save this cleaned data to it's own seperate file called `bank_cleaned.csv`.  

Dataset citation:
 
Moro,S., Rita,P., and Cortez,P.. (2012). Bank Marketing. UCI Machine Learning Repository. https://doi.org/10.24432/C5K306.

```{code-cell} ipython3
from urllib.request import urlretrieve
from zipfile import ZipFile
import pandas as pd
import os


def extract_to_csv(url, data_name):
    """
    This function extracts data from a URL with a .zip file,
    cleans the data and saves the clean data
    """
    # Set path
    file = os.path.basename(url)
    urlretrieve(url, file)
    # Extract data
    with ZipFile(file, "r") as zf:
        zf.extractall()
    # Clean data and save
    csv_file_name = f"{data_name}.csv"
    df = pd.read_csv(csv_file_name, sep=";")
    df.to_csv(f"{data_name}_cleaned.csv", index=False)
```

```{code-cell} ipython3
# Running the above function
extract_to_csv("https://tinyurl.com/uci-marketing-data", "bank")
```

After running this code, you should have `bank_cleaned.csv` in the current directory. 

## Load Engine
We now load in our SQL extension that allows us to execute SQL queries in Jupyter Notebooks. 

<b>Note</b> Ensure you restart any previous notebook that has the same database name as the one initialized below.

```{code-cell} ipython3
# Loading in SQL extension
%reload_ext sql
# Initiating a DuckDB database named 'bank.duck.db' to run our SQL queries on
%sql duckdb:///bank.duck.db
```

Let's now return to our initial dataset of bank marketing records. 

## Queries

### Creating Table

Let's start off with loading our `bank_cleaned.csv` file from our local directory to our newly created DuckDB database. Here we `CREATE OR REPLACE TABLE` in DuckDB called 'bank' `FROM` our `bank_cleaned.csv` file. The `read_csv_auto` is a function that helps SQL understand our local .csv file for creation into our database.

```{code-cell} ipython3
%%sql
CREATE OR REPLACE TABLE bank AS
FROM read_csv_auto('bank_cleaned.csv', header=True, sep=',')
```

### Count and Distinct Count
`COUNT()` allows users to query the count of records in a given query. A common argument to this function is `*`. `COUNT(*)` tells SQL to return the total number of rows from our query, including NULL values. This can be combined with queries that filter for certain conditions.

A common function to be used with `COUNT()` is `DISTINCT()`. For example, selecting `COUNT(DISTINCT(job))` would return the count of distinct values under the "job" column.

```{code-cell} ipython3
%%sql 
SELECT COUNT(DISTINCT(job))
FROM bank 
```

The output of the above query can be an eyesore. Instead of getting SQL's default column name when running these aggregation function, users can utilize the `AS` clause. The text following `AS` changes the output of the `SELECT` clause to that text. Our next example with demonstrate this.

Here's an example with `COUNT()` that counts the number of rows of our query `WHERE` we filter for "balance" greather than or equal to 500 `AND` where "martial" equals married. We also use the `AS` clause to change the column of our query to "Count".

```{code-cell} ipython3
%%sql 
SELECT COUNT(*) AS Count
FROM bank 
WHERE balance > 500 AND martial = 'married'
```

`COUNT()` can also have the arguments of a single row, such as `COUNT(job)`. `COUNT(job)` would count the number of rows of just the "job" column. If "job" were to have any NULL values in its query, those NULL values would be subtracted from the total row counts of the query. 

### Average

`AVG()` allows users to take the average of columns. This clause can also be used with filtering. An example of finding the average balance of unemployed observations is as follows:

```{code-cell} ipython3
%%sql 
SELECT AVG(balance) AS average_unemployed_balance
FROM bank 
WHERE job = 'unemployed'
```

The value of our `AVG(balance)` function can be rounded to better represent a monetary balance with `ROUND()`. `ROUND()` accepts two arguments. The first is the actual value to round and the second is the number of decimal places to round to. We apply `ROUND()` to the same query below.

Note that aliasing query column outputs with the AS clause should not have any spaces. By convention, this makes it easier for SQL to later reference these aliases and avoid ambiguity for the parser.

```{code-cell} ipython3
%%sql 
SELECT ROUND(AVG(balance),2) AS average_unemployed_balance
FROM bank 
WHERE job = 'unemployed'
```

### Sum

`SUM()` aggregates the sum of columns. Below, we find the `SUM()` of the balance column `WHERE` "job" equals 'management' `OR` `WHERE` "job" equals 'services'.

```{code-cell} ipython3
%%sql 
SELECT SUM(balance) AS sum_balance_of_managers
FROM bank 
WHERE job = 'management' OR job = 'services'
```

### Minimum and Maximum

The `MIN()` and `MAX()` functions do exactly what you would think. Below we find the `MIN()` and `MAX()` of "balance".

```{code-cell} ipython3
%%sql 
SELECT MIN(balance) AS minimum_balance
FROM bank 
```

```{code-cell} ipython3
%%sql 
SELECT MAX(balance) AS maximum_balance
FROM bank 
```

Accumulating everything we have learned so far, can you think of another way of finding the minimum and maximum of balance without `MIN()` and `MAX()`? <b>Hint:</b> try recreating these queries with `ORDER BY`.

### Grouping

Grouping is an extremely useful clause. It allows users to examine the results of aggregate functions within each unique group. Note that grouping with `GROUP BY` comes after filtering with `WHERE`. Below, we find the `COUNT()` of all rows `GROUP BY` "housing". Since housing only has the unique values of 'yes' and 'no', there will be only two groups.

```{code-cell} ipython3
%%sql 
SELECT COUNT(*) AS Count
FROM bank 
GROUP BY housing
```

The problem with the above query is we can not determine what value belongs to which group. To fix this, `SELECT` both the "housing" variable and the `COUNT(*)` function. Let's also change 'housing' to 'Housing' in our final output just for demonstration purposes.

```{code-cell} ipython3
%%sql 
SELECT housing as Housing, COUNT(*) AS Count
FROM bank 
GROUP BY housing
```

We can now clearly see which count belongs to which group under "housing". 

`GROUP BY` also allows for grouping with several variables. For instance, let's first `GROUP BY` "housing" and then `GROUP BY` "marital". Then, find the `COUNT()` of these groups.

```{code-cell} ipython3
%%sql 
SELECT housing AS Housing, marital AS Marital, COUNT(*) AS Count
FROM bank 
GROUP BY housing, marital
```

There are six total groups from our query. "housing" has two groups and "marital" has three groups. Since "housing" has only two groups, 'yes' and 'no', let's think about these groups as two seperate blocks. The 'yes' and 'no' blocks will then each be `GROUP BY` the groups under the "marital" column, which are 'married', 'single', and 'divorced'. Thus, since each 'yes' and 'no' group has three groups each, there are a total of six groups.

![diagram](aggregate-functions-diagram.png)

<!-- #endregion -->

## You try: Use JupySQL to perform the queries and answer the questions.

### Question 1 (Easy):
Find the average "duration" of phone calls. Name the column of your output as "Average Phone Call Length". Round to 0 decimal places.

<!-- #region -->
<details>

<summary>Answers</summary>

You can use the `ROUND` clause to specify where 0 decimal places.

```{code-cell} ipython3
%%sql 
SELECT ROUND(AVG(duration),0) AS average_phone_call_length
FROM bank 
```

</details>
<!-- #endregion -->

### Question 2 (Medium):
Show each education group's count of whether they have housing or not. Also, make it so that this query only include married individuals.

<!-- #region -->
<details>

<summary>Answers</summary>

The `WHERE` clause must appear first before the `GROUP BY` clause. Then, grouping by first education and then housing gives the correct `COUNT()` of each group. Notice that 'primary' under the "education" column does not have a "housing" group of 'yes' If no records exist where an observation with an "education" of 'primary' has a "housing" value of 'yes', then it is omitted from `GROUP BY` queries. This is saying that this particular group does not exist.

```{code-cell} ipython3
%%sql
SELECT education, housing, COUNT(*)
FROM bank  
WHERE marital = 'married'
GROUP BY education, housing
```

</details>
<!-- #endregion -->

### Question 3 (Medium):
Find the average, minimum, and maximum of balance and the count of records where there has not been a default. Group this query by "job" and "married". Round the averages by 2 decimal places.

<b>Hint</b> `COUNT()` is a aggregating function in SQL (more on aggregation later!). Try experimenting with `COUNT()` in your `SELECT` clause to see if you can find the correct count.

<!-- #region -->
<details>
<summary>Answers</summary>

You may have had some problems with the `WHERE` clause. If you had "default" as just default, you encountered an error. Reading this error would inform that `DEFAULT` is an existing SQL clause and having it in our `WHERE` clause is not acceptable. In situations like this, you can double quotes "" surrounding the column name. This helps SQL distinguish clauses and literal strings of text.

```{code-cell} ipython3
%%sql
SELECT job, marital, AVG(balance), COUNT(*), MIN(balance), MAX(balance)
FROM bank 
WHERE "default" = 'no'
GROUP BY job, marital
```

</details>
<!-- #endregion -->

<!-- #region -->

## Wrapping Up

In this section, we introduced aggregate functions and the `GROUP BY` utility. To summarize:

- `COUNT()` : Returns the number of rows in our query. This function can count the number of rows of a specific column or of the entire query by passing "*" into the function.

- `AVG()` : Returns the average of a numeric column in our query. `ROUND()` is a useful function often applied with this aggregate function.

- `MIN()` and `MAX()` : Returns the minimum and maximum of a numeric column in our query.

- `GROUP BY ` : A powerful clause that groups the data based on a given column. This clause must be used with aggregation functions.

We have also learned other details from this section, such as how `WHERE` must appear before any `GROUP BY` clause and how to tell SQL to distinguish a literal string when that string is a clause. 

Next up, we will use everything we have thus far learned in joining tables.

<!-- #endregion -->
