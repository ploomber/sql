---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.5
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
---
tags: [remove-cell]
---
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
---
tags: [remove-cell]
---
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
---
tags: [remove-output]
---
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
---
tags: [remove-cell]
---
# this cell is hidden in the docs, only used to fake
# the password variable
password = "password"
```

```{code-cell} ipython3
db_url = f"postgresql://user:{password}@localhost/database"
```

```{code-cell} ipython3
---
tags: [remove-cell]
---
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
---
tags: [remove-output]
---
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
---
tags: [remove-output]
---
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
---
tags: [remove-cell]
---
# this cell is hidden in the docs, only used to fake
# the environment variable
from os import environ

environ["DATABASE_URL"] = "sqlite://"
```

```{code-cell} ipython3
---
tags: [remove-output]
---
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
---
tags: [remove-output]
---
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

First, let's import the library and initialize a new connection

```{code-cell} ipython3
import duckdb

conn = duckdb.connect()
```

Now, load `%sql` and initialize it with our DuckDB connection.

```{code-cell} ipython3
%sql conn
```

Download some data.

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

## Use JupySQL to perform the queries and answer the questions.

### Question 1 (Easy):
Load a CSV file into a DuckDB instance. The Bonus section can help you with this.


<!-- #region -->
<details>

<summary>Show Answers</summary>

Recall that a connection string has the following format:

```
dialect+driver://username:password@host:port/database
```

To connect to a DuckDB database, you can use the `%sql` magic command the appropriate `duckdb://` URL string:

```{code-cell} ipython3
%sql "duckdb://"
```

Download CSV data from GitHub:

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

</details>
<!-- #endregion -->

### Question 2 (Medium):
Write a code snippet to establish a **secure** connection for a PostgreSQL database by using a connection string, the `get_pass()` function, and by creating an engine.


<!-- #region -->
<details>

<summary>Show Answers</summary>

To securely connect to a PostgreSQL database, you can use the `getpass` function from the `getpass` module to prompt the user for a password. This way, the password is not hardcoded in the notebook.

```python
from getpass import getpass

password = getpass()
```

Then, you can build your connection string:

```python
db_url = f"postgresql://user:{password}@localhost/database"
```

Create an engine and connect:

```python
from sqlalchemy import create_engine

engine = create_engine(db_url)
```

</details>
<!-- #endregion -->

### Question 3 (Hard):
If you have a database that is not supported by SQLAlchemy but follows the DB API 2.0 specification, how can you still use JupySQL? 


<!-- #region -->
<details>

<summary>Show Answers</summary>

The answer is using a Custom Connection. For this example, we'll generate a `SQLite` connection, using its native `connect` method, and a custom table to query from.

First, let's import the library and create a new database connection to our custom table, `my_numbers`.

```{code-cell} ipython3
import sqlite3

with sqlite3.connect("a.db") as conn:
    conn.execute("CREATE TABLE my_numbers (number FLOAT)")
    conn.execute("INSERT INTO my_numbers VALUES (1)")
    conn.execute("INSERT INTO my_numbers VALUES (2)")
    conn.execute("INSERT INTO my_numbers VALUES (3)")
```

Next, load `%sql` and create a schema, `a_schema`, for the table.

```{code-cell} ipython3
%%sql
ATTACH DATABASE 'a.db' AS a_schema
```

You're all set!

```{code-cell} ipython3
%sql select * from a_schema.my_numbers limit 3
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
---
tags: [remove-output]
---
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