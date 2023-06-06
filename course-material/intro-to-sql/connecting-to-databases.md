---
jupyter:
  jupytext:
    formats: md:myst
    notebook_metadata_filter: myst
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.6
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Connecting to Database Engines

In this tutorial you will learn how to connect to various databases using JupySQL.

## Connect with a URL string

Connection strings follow the [SQLAlchemy URL format](http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls). This is the fastest way to connect to your database and the recommended way if you're using SQLite or DuckDB.

Database URLs have the following format:

```
dialect+driver://username:password@host:port/database
```


```{important}
If you're using a database that requires a password, keep reading for more secure methods.
```

+++

## Building URL strings securely

To connect in a more secure way, you can dynamically build your URL string so your password isn't hardcoded:

```python
from getpass import getpass

password = getpass()
```

When you execute the cell above in a notebook, a text box will appear and whatever you type will be stored in the `password` variable.

```{code-cell} ipython3
:tags: [remove-cell]

# this cell is hidden in the docs, only used to simulate
# the getpass() call
password = "mysupersecretpassword"
```

Then, you can build your connection string:

```{code-cell} ipython3
db_url = f"postgresql://user:{password}@localhost/database"
```

Create an engine and connect:

```{code-cell} ipython3
:tags: [remove-cell]

# this cell is hidden in the docs, only used to fake
# the db_url
db_url = "duckdb://"
```

```{code-cell} ipython3
from sqlalchemy import create_engine

engine = create_engine(db_url)
```

## Secure Connections


**It is highly recommended** that you do not pass plain credentials.

```{code-cell} ipython3
:tags: [remove-output]

%load_ext sql
```

```{code-cell} ipython3
%sql engine
```

+++ {"user_expressions": []}

```{important}
Unlike `ipython-sql`, JupySQL doesn't allow expanding your database URL with the `$` character:

~~~python
# this doesn't work in JupySQL!
db_url = "dialect+driver://username:password@host:port/database"
%sql $db_url
~~~
```

+++ {"user_expressions": []}

## Securely storing your password

If you want to store your password securely (and don't get prompted whenever you start a connection), you can use [keyring](https://github.com/jaraco/keyring):

```{code-cell} ipython3
:tags: [remove-output]

%pip install keyring --quiet
```

+++ {"user_expressions": []}

Execute the following in your notebook:

```{code-cell} ipython3
import keyring

keyring.set_password("my_database", "my_username", "my_password")
```

+++ {"user_expressions": []}

Then, delete the cell above (so your password isn't hardcoded!). Now, you can retrieve your password with:

```{code-cell} ipython3
from sqlalchemy import create_engine
import keyring

password = keyring.get_password("my_database", "my_username")
```

```{code-cell} ipython3
:tags: [remove-cell]

# this cell is hidden in the docs, only used to fake
# the password variable
password = "password"
```

```{code-cell} ipython3
db_url = f"postgresql://user:{password}@localhost/database"
```

```{code-cell} ipython3
:tags: [remove-cell]

# this cell is hidden in the docs, only used to fake
# the db_url
db_url = "duckdb://"
```

+++ {"user_expressions": []}

Create an engine and connect:

```{code-cell} ipython3
engine = create_engine(db_url)
```

```{code-cell} ipython3
:tags: [remove-output]

%load_ext sql
```

```{code-cell} ipython3
%sql engine
```

```{tip}
If you have issues using `keyring`, send us a message on [Slack.](https://ploomber.io/community)
```

+++

## Passing custom arguments to a URL

+++

Connection arguments not whitelisted by SQLALchemy can be provided with `--connection_arguments`. See [SQLAlchemy Args](https://docs.sqlalchemy.org/en/13/core/engines.html#custom-dbapi-args).

Here's an example using SQLite:

```{code-cell} ipython3
:tags: [remove-output]

%load_ext sql
```

```{code-cell} ipython3
%sql --connection_arguments '{"timeout":10}' sqlite://
```

## Connecting via an environment variable

+++

Set the `DATABASE_URL` environment variable, and `%sql` will automatically load it. You can do this either by setting the environment variable from your terminal or in your notebook:

```{code-cell} ipython3
from getpass import getpass
from os import environ

password = getpass()
environ["DATABASE_URL"] = f"postgresql://user:{password}@localhost/database"
```

```{code-cell} ipython3
:tags: [remove-cell]

# this cell is hidden in the docs, only used to fake
# the environment variable
from os import environ

environ["DATABASE_URL"] = "sqlite://"
```

```{code-cell} ipython3
:tags: [remove-output]

%load_ext sql
```

```{code-cell} ipython3
%sql
```

## Using an existing `sqlalchemy.engine.Engine`

You can use an existing `Engine` by passing the variable name to `%sql`.

```{code-cell} ipython3
import pandas as pd
from sqlalchemy.engine import create_engine
```

```{code-cell} ipython3
engine = create_engine("sqlite://")
```

```{code-cell} ipython3
df = pd.DataFrame({"x": range(5)})
df.to_sql("numbers", engine)
```

```{code-cell} ipython3
:tags: [remove-output]

%load_ext sql
```

```{code-cell} ipython3
%sql engine
```

```{code-cell} ipython3
%%sql
SELECT * FROM numbers
```

## Custom Connection

If you are using a database that is not supported by SQLAlchemy but follows the [DB API 2.0 specification](https://peps.python.org/pep-0249/), you can still use JupySQL.

```{note}
We currently support `%sql`, `%sqlplot`, and the `ggplot` API when using custom connection. However, please be advised that there may be some features/functionalities that won't be fully compatible with JupySQL.
```

For this example we'll generate a `DuckDB` connection, using its native `connect` method.

First, let's import the library and initiazlie a new connection

```{code-cell} ipython3
import duckdb

conn = duckdb.connect()
```

Now, load `%sql` and initialize it with our DuckDB connection.

```{code-cell} ipython3
%sql conn
```

Download some data

```{code-cell} ipython3
import urllib

urllib.request.urlretrieve(
    "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv",
    "penguins.csv",
)
```

You're all set

```{code-cell} ipython3
%sql select * from penguins.csv limit 3
```

Example: show the first 5 rows.

```sql
SELECT *
FROM absenteeism 
LIMIT 5
```

#### Question 1.1 (Easy):
How many records are there in the 'absenteeism' table? 


<!-- #region -->
<details>

<summary>Answers</summary>

You can use the `%%sql` magic and the `COUNT(*)` function to count the total number of records. 

```python
%%sql
SELECT COUNT(*) 
FROM absenteeism
```
</details>
<!-- #endregion -->

#### Question 1.2 (Easy):
How many unique employees are listed in the dataset?



<!-- #region -->
<details>

<summary>Answers</summary>

You can use the `%%sql` magic and the `COUNT(DISTINCT ID)` function to count the total number of unique instances of the `Age` column. 

```python
%%sql
SELECT COUNT(DISTINCT ID) 
FROM absenteeism;
```
</details>
<!-- #endregion -->

#### Question 1.3 (Easy):
What is the average distance from residence to work? 


<!-- #region -->
<details>

<summary>Show Answers</summary>

You can use the `%%sql` magic and the `AVG(Distance_from_Residence_to_Work)` function to calculate the average distance from residence to work.. 

```python
%%sql
SELECT AVG(Distance_from_Residence_to_Work) 
FROM absenteeism;
```
</details>
<!-- #endregion -->

#### Question 2.1 (Medium):
On which days of the week does the average absenteeism time exceed 4 hours? 


<!-- #region -->
<details>

<summary>Answers</summary>

You can use the `%%sql` magic and break down the query as follows:

1. Select the column with name `Day_of_the_week`
2. From the table called `absenteeism`
3. Then group the values by day of the week that have an average value (use `AVG`) of more than 4 hours in absenteeism. 

```python
%%sql
SELECT Day_of_the_week 
FROM absenteeism 
GROUP BY Day_of_the_week 
HAVING AVG(Absenteeism_time_in_hours) > 4;
```
</details>
<!-- #endregion -->

#### Question 2.2 (Medium):
What is the average transportation expense for each season?


<!-- #region -->
<details>

<summary>Answers</summary>

You can use the `%%sql` magic and. Use the `AVG(Transportation_expense)` with the alias `AVG_Transportation_Expense` function to count the average transporation expense, then group by seasons.

```python
%%sql
SELECT Seasons, AVG(Transportation_expense) AS AVG_Transportation_Expense
FROM absenteeism 
GROUP BY Seasons;

```
</details>
<!-- #endregion -->

<!-- #region -->
#### Question 2.3 (Medium):


What is the average absenteeism time for employees with BMI higher than the average BMI
<!-- #endregion -->


<!-- #region -->
<details>

<summary>Show Answers</summary>

You can use the `%%sql` magic and. Use the `AVG(Absenteeism_time_in_hours)` with the alias `AVG_Absenteeism_time_in_hours` function to count the average absenteeism (time units hours). 

`WHERE Body_mass_index > (`: This part begins a condition that the data must meet to be included in our average calculation. Here, we're only interested in rows where the `Body_mass_index` is greater than a certain value.

`SELECT AVG(Body_mass_index) FROM absenteeism)`: This is a subquery, a query within a query. It's calculating the average `Body_mass_index` for the entire absenteeism table.

```python
%%sql
SELECT AVG(Absenteeism_time_in_hours) as AVG_Absenteeism_time_in_hours
FROM absenteeism 
WHERE Body_mass_index > (
    SELECT AVG(Body_mass_index) 
    FROM absenteeism);

```
</details>
<!-- #endregion -->

#### Question 3.1 (Hard):
Find the top 3 ages with the highest total absenteeism hours, excluding disciplinary failures.



<!-- #region -->


<details>

<summary>Answers</summary>

You can use the `%%sql` magic and break down the query as follows:

1. Select the column with name `Age`, compute the Sum of `Absenteeism_time_in_hours`. Give this sum an alias `Sum_Absenteeism`.
2. From the table called `absenteeism`
3. The keywork WHERE is used to filter the data that meets a specific condition, in this case `Disciplinary_failure` is equal to zero.
4. Group values by the `Age` column.
5. Sort the values by the sum and show the first 3 values.

```python
%%sql
SELECT Age, SUM(Absenteeism_time_in_hours) AS Sum_Absenteeism
FROM absenteeism 
WHERE Disciplinary_failure = 0 
GROUP BY Age 
ORDER BY Sum_Absenteeism
DESC LIMIT 3;
```
</details>
<!-- #endregion -->

#### Question 3.2 (Hard):

Find the age of employees who have been absent for more than 5 hours with an unjustified absence.

Hint: investigate encoding on the data source.


<!-- #region -->
<details>

<summary>Answers</summary>

You can use the `%%sql` magic. 'Unjustified absence' is coded with 26. From there all that is required is selecting the age, and using `WHERE` to set up the appropriate conditions. 

```python
%%sql
SELECT Age 
FROM absenteeism 
WHERE Reason_for_absence = 26 AND Absenteeism_time_in_hours > 5;

```
</details>
<!-- #endregion -->

#### Question 3.3 (Hard):

Which reasons for absence are more frequent for social drinkers than social non-drinkers?


<!-- #region -->
<details>

<summary>Show Answers</summary>

You can use the `%%sql` magic. We use `SELECT` to extract the `Reason_for_absence` from the `absenteeism` table. 

The column `Social_drinker` is encoded using binary notation, 0=is not a social drinker, 1=is a social drinker. 

We next group by their reason for absence. 

`HAVING COUNT() > (`  begins the condition that the groups must meet to be included in the results. Only groups where the count of rows (representing the number of instances of each `Reason_for_absence` among social drinkers) is greater than a certain value will be included.

`SELECT COUNT() FROM absenteeism WHERE Social_drinker = 0 GROUP BY Reason_for_absence)`  is a subquery that calculates the count of rows for each `Reason_for_absence` where `Social_drinker` is 0 (indicating the employee is not a social drinker), effectively giving us the number of instances of each `Reason_for_absence` among non-social drinkers.

```python
%%sql
SELECT Reason_for_absence 
FROM absenteeism 
WHERE Social_drinker = 1 
GROUP BY Reason_for_absence 
HAVING COUNT() > (
    SELECT COUNT() 
    FROM absenteeism 
    WHERE Social_drinker = 0 
    GROUP BY Reason_for_absence);

```
</details>
<!-- #endregion -->

## Bonus

### In-memory Database with DuckDB

Although URL-based connections are more secure, can handle various types of workloads, and offer more functionality, in-memory databases are a great option for quick querying and testing. In this tutorial, we'll use [DuckDB](https://jupysql.ploomber.io/en/latest/integrations/duckdb.html) to create an in-memory database with JupySQL.

The first step is to install the dependencies:

```{code-cell} ipython3
%pip install jupysql duckdb duckdb-engine --quiet
```

Then, load the ipython-sql library using the `%load_ext` iPython extension syntax and connect to the database:

```{code-cell} ipython3
:tags: [remove-output]

%load_ext sql
```

Finally, load `%sql` and initialize the database:

```{code-cell} ipython3
%sql duckdb://
```

Download some data:

```{code-cell} ipython3
import urllib

urllib.request.urlretrieve(
    "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv",
    "penguins.csv",
)
```

You're all set!

```{code-cell} ipython3
%sql select * from penguins.csv limit 3
```

### Databases Supported by JupySQL

Check out our guides for connecting to supported databases:

- [PostgreSQL](https://jupysql.ploomber.io/en/latest/integrations/postgres-connect.html)
- [ClickHouse](https://jupysql.ploomber.io/en/latest/integrations/clickhouse.html)
- [MariaDB](https://jupysql.ploomber.io/en/latest/integrations/mariadb.html)
- [MindsDB](https://jupysql.ploomber.io/en/latest/integrations/mindsdb.html)
- [MSSQL](https://jupysql.ploomber.io/en/latest/integrations/mssql.html)
- [MySQL](https://jupysql.ploomber.io/en/latest/integrations/mysql.html)
- [QuestDB](https://jupysql.ploomber.io/en/latest/integrations/questdb.html)
- [Oracle](https://jupysql.ploomber.io/en/latest/integrations/oracle.html)
- [Trino](https://jupysql.ploomber.io/en/latest/integrations/trinodb.html)

+++


 

