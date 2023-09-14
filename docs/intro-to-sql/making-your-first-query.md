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

# Making your first SQL query
<!-- #region -->

## SQL Overview

SQL (Structured Query Language) is the widely adopted language used for managing and manipulating data. It's the language that inspired its other popular variants you may have heard of, such as PostgreSQL, MySQL, and more. 

In this lesson, you will learn how to make your first SQL query.

## Dataset

To perform your first SQL query, we will be working with one main dataset throughout this course:
- Bank Marketing Data

Source: UCI Machine Learning Repository

URL: https://archive-beta.ics.uci.edu/dataset/222/bank+marketing

Data Citation

Moro,S., Rita,P., and Cortez,P.. (2012). Bank Marketing. UCI Machine Learning Repository. https://doi.org/10.24432/C5K306.

## Data Description

The data is related with direct marketing campaigns of a Portuguese banking institution. The marketing campaigns were based on phone calls. Often, more than one contact to the same client was required, in order to access if the product (bank term deposit) would be ('yes') or not ('no') subscribed. 

The data contains the following categories:

1. age (numeric)
2. job: type of job (categorical: 'admin.','blue-collar','entrepreneur','housemaid','management','retired','self-employed','services','student','technician','unemployed','unknown')
3. marital: marital status (categorical: 'divorced','married','single','unknown')
4. education (categorical: 'basic.4y','basic.6y','basic.9y','high.school','illiterate','professional.course','university.degree','unknown')
5. default: has credit in default? (categorical: 'no','yes','unknown')
6. housing: has housing loan? (categorical: 'no','yes','unknown')
7. loan: has personal loan? (categorical: 'no','yes','unknown')
8. contact: contact communication type (categorical: 'cellular','telephone') 
9. month: last contact month of year (categorical: 'jan', 'feb', 'mar', ..., 'nov', 'dec')
10. day_of_week: last contact day of the week (categorical: 'mon','tue','wed','thu','fri')
11. duration: last contact duration, in seconds (numeric)
12. campaign: number of contacts performed during this campaign and for this client (numeric)
13. pdays: number of days that passed by after the client was last contacted from a previous campaign (numeric; 999 means client was not previously contacted)
14. previous: number of contacts performed before this campaign and for this client (numeric)
15. poutcome: outcome of the previous marketing campaign (categorical: 'failure','nonexistent','success')
16. y: has the client subscribed a term deposit? (binary: 'yes','no')

<!-- #endregion -->

<!-- #region -->
## Install - execute this once. 

This code installs JupySQL, DuckDB, and Pandas in your environment. We will be using these moving forward.

```bash
%pip install jupysql duckdb-engine --quiet
```

## Helper script

We developed a `banking.py` script to help you extract the data from the URL and load it into a DuckDB database. This script is located [here](https://github.com/ploomber/sql/blob/main/banking.py)

## Load the data
We extract the bank marketing data by retrieving it from it's URL download link. The link may be a zip file (which it is in this case), so we extract the zip file, read the file containing the data within the zip file, and clean the data. Finally, we save this cleaned data to it's own seperate file called `bank_cleaned.csv`.

```{code-cell} ipython3
import sys

sys.path.insert(0, "../../")
import banking  # noqa: E402

_ = banking.BankingData("https://tinyurl.com/jb-bank", "bank")
_.extract_to_csv()
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

## Queries

### Creating Table

Let's start off with loading our `bank_cleaned.csv` file from our local directory to our newly created DuckDB database. Here we `CREATE OR REPLACE TABLE` in DuckDB called 'bank' `FROM` our `bank_cleaned.csv` file. The `read_csv_auto` is a function that helps SQL understand our local .csv file for creation into our database.

```{code-cell} ipython3
%%sql
CREATE OR REPLACE TABLE bank AS
FROM read_csv_auto('bank_cleaned.csv', header=True, sep=',')
```

### Simple Query

Now that we have our `bank` table in our DuckDB database, we can run our first query on the table. Let's start off with a simple query that looks at the first five rows from our table.

```{code-cell} ipython3
%%sql
SELECT *
FROM bank
LIMIT 5
```

`SELECT`, `FROM` and `LIMIT` are considered "clauses" in SQL. You can think of these clauses as functions that serve specific task. `SELECT` is used to specify what the user wants `FROM` the table. The "*" next to our `SELECT` clause means to "select all" `FROM` our bank table. The `LIMIT` clause tells SQL to show only the top 5 rows from our `SELECT` clause.

#### Filtering
The `WHERE` clause allows users to filter the query on specific conditions. Below, we query the table `WHERE` the "job" variable equals 'unemployed'.

```{code-cell} ipython3
%%sql 
SELECT *
FROM bank 
WHERE job = 'unemployed'
```

The 'unemployed' is in quotes because the "job" variable has values which are strings. If you unfamiliar with strings, you can find a quick introduction here.

We can extend filtering even further by filtering on two or more conditions. This introduces the `AND` and `OR` clauses.

```{code-cell} ipython3
%%sql 
SELECT *
FROM bank 
WHERE job = 'unemployed' AND education = 'primary'
```

This query filters the data `WHERE` "job" equals 'unemployed' `AND` where "education" equals 'primary'. The `OR` clause behaves identically to its verbal counterpart.

```{code-cell} ipython3
%%sql 
SELECT *
FROM bank 
WHERE job = 'unemployed' OR job = 'blue-collar'
```

#### Sorting

We can sort the outputs of our query based on certain conditions. Below, we sort our query by "balance" using the `ORDER BY` clause in `DESC` (descending) order.

```{code-cell} ipython3
%%sql 
SELECT *
FROM bank 
ORDER BY balance DESC
```

To order the query by ascending order, you can omit the `DESC` or add `ASC` in the above SQL statement.

<!-- #endregion -->


### You try: Use JupySQL to perform the queries and answer the questions.

Example: show the first 5 rows of the "job" variable.

```{code-cell} ipython3
%%sql
SELECT job
FROM bank 
LIMIT 5
```

#### Question 1 (Easy):
Query records where the month is in April ("apr")

<!-- #region -->
<details>

<summary>Answers</summary>

You can use the `WHERE` clause to specify where month equals 'apr'.

```{code-cell} ipython3
%%sql
SELECT *
FROM bank
WHERE month = 'apr'
```

</details>
<!-- #endregion -->

#### Question 2 (Medium):
Query the first 5 records where "balance" is greater than or equal to 1000. Sorted this query by ascending order.
<b>Hint</b> Equal, greater than, and less can be represented as =, <, >, respectively. Greater than or equal to can be represented as >=

<!-- #region -->
<details>

<summary>Answers</summary>

You can use the `WHERE` clause and with the greater than operator ">=" to declare records with a balance greater than or equal to 1000. The query is then sorted by balance in descending order in the last line with `ORDER BY` and `DESC`.

```{code-cell} ipython3
%%sql
SELECT *
FROM bank
WHERE balance >= 1000
ORDER BY balance DESC
```

</details>
<!-- #endregion -->

#### Question 3 (BONUS):
Show the count of records where 'housing' is 'no' and where 'loan' is yes. 

<b>Hint</b> `COUNT()` is a aggregating function in SQL (more on aggregation later!). Try experimenting with `COUNT()` in your `SELECT` clause to see if you can find the correct count.

<!-- #region -->
<details>
<summary>Answers</summary>

You can use `COUNT(*)` to get the count of total records after filtering `WHERE` 'housing' is 'no' and 'loan' is yes.

```{code-cell} ipython3
%%sql
SELECT COUNT(*)
FROM bank
WHERE housing = 'no' AND loan = 'yes'
```

</details>
<!-- #endregion -->

<!-- #region -->

Delete table

```{code-cell} ipython3
%%sql
DROP TABLE bank;
```

### Wrapping Up

To summarize this section, we first introduced our primary dataset we will be using for the next few sections. Then, we ran our first query by first installing `JupySQL` and other packages into our notebook, properly loaded our data with some `Python`, and established a connection to a DuckDB database. 

We learned the basics of `SQL` by going over some of its most necessary clauses:

- `SELECT` : "Selects" what to extract from the query. This clause can be followed by a specific variable name or by using "*" to select the whole table.

- `FROM` : Tells SQL what table in the database to run our query on. We used this clause primarily on 'bank' which we first created when setting up our DuckDB database.

- `LIMIT` : Limits the number of rows from our query

- `WHERE` : Filters the query on specific conditions. This clause can be combined with `AND` and `OR` clauses for more complex filters.

- `ORDER BY` : Sorts the output on variables in our query. This clause can include `DESC` to sort by descending order.

These clauses lay the foundation of `SQL`. They will be necessary for our next section, which will introduce aggregation functions. We showed a sneak peek of an aggregation function `COUNT()` in Question 3. More on that in the next section!

#### A Little Extra

As you may have noticed, SQL code is straight forward. It's clauses translate well to what you want SQL to do in natural verbal terms. These clauses make it so easy it's like you are "declaring" SQL to do what you would like it to do. This nature is what defines SQL to be a "declarative programming language". 

<a href="https://365datascience.com/tutorials/sql-tutorials/sql-declarative-language/" target="_blank">This article</a> is a great resource if you're curious on this topic.

<!-- #endregion -->
