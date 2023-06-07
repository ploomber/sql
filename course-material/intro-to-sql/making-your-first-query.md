---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.5
---

# Making your first SQL query
<!-- #region -->
### SQL Overview

SQL (Structured Query Language) is the widely adopted language used for managing and manipulating data. It's the language that inspired its other popular variants you may have heard of, such as PostgreSQL, MySQL, and more. 

In this lesson, you will learn how to make your first SQL query.

### Dataset

To perform your first SQL query, we will be working with one main dataset throughout this course:
- Bank Marketing Data

Source: UCI Machine Learning Repository

URL: https://archive-beta.ics.uci.edu/dataset/222/bank+marketing

### Data Description

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
### 5 minute crash course into JupySQL

Play the following video to get familiar with JupySQL to execute queries on Jupyter using DuckDB.

<b>If you get stuck, join our Slack community!</b> https://ploomber.io/community


[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/CsWEUYLaYU0/0.jpg)](https://www.youtube.com/watch?v=CsWEUYLaYU0)

<!-- #endregion -->

<!-- #region -->
### Install - execute this once. 

This code installs JupySQL, DuckDB, and Pandas in your environment. We will be using these moving forward.

```python
try:
    %pip install jupysql --upgrade duckdb-engine pandas --quiet
    print("Success")
except:
    print("retry installing")
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

#### Load Engine
We now load in our SQL extension that allows us to execute SQL queries in Jupyter Notebooks. 

<b>Note</b> Ensure you restart any previous notebook that has the same database name as the one initialized below.

```python
#Loading in SQL extension
%reload_ext sql
#Initiating a DuckDB database named 'bank.duck.db' to run our SQL queries on
#Maybe give a hyperlink about DuckDB
%sql duckdb:///bank.duck.db
```

### Queries

#### Creating Table

Let's start off with loading our `bank_cleaned.csv` file from our local directory to our newly created DuckDB database. Here we create a table in DuckDB called 'bank' from our `bank_cleaned.csv` file. The read_csv_auto function helps SQL understand our local .csv file for creation into our database.

```sql
%%sql
CREATE OR REPLACE TABLE bank AS
FROM read_csv_auto('bank_cleaned.csv', header=True, sep=',')
```

#### Simple Query

Now that we have our `bank` table in our DuckDB database, we can run our first query on the table. Let's start off with a simple query that looks at the first five rows from our table.

```sql 
%%sql
SELECT *
FROM bank
LIMIT 5
```

`SELECT`, `FROM` and `LIMIT` are considered "clauses" in SQL. You can think of these clauses as functions that serve specific task. `SELECT` is used to specify what the user wants `FROM` the table. The "*" next to our `SELECT` clause means to "select all" `FROM` our bank table. The `LIMIT` clause tells SQL to show only the top 5 rows from our `SELECT` clause.

#### Filtering
The `WHERE` clause allows users to filter the query on specific conditions. Below, we query the table `WHERE` the "job" variable equals 'unemployed'.

```sql
%%sql 
SELECT *
FROM bank 
WHERE job = 'unemployed'
```
The 'unemployed' is in quotes because the "job" variable has values which are strings. If you unfamiliar with strings, you can find a quick introduction here.

We can extend filtering even further by filtering on two or more conditions. This introduces the `AND` and `OR` clauses. 

```sql
%%sql 
SELECT *
FROM bank 
WHERE job = 'unemployed' AND education = 'primary'
```

This query filters the data `WHERE` "job" equals 'unemployed' `AND` where "education" equals 'primary'. The `OR` clause behaves identically to its verbal counterpart. 

```sql
%%sql 
SELECT *
FROM bank 
WHERE job = 'unemployed' OR job = 'blue-collar'
```

#### Sorting

We can sort the outputs of our query based on certain conditions. Below, we sort our query by "balance" using the `ORDER BY` clause in `DESC` (descending) order.

```sql
%%sql 
SELECT *
FROM bank 
ORDER BY balance DESC
```
To order the query by ascending order, you can omit the `DESC` or add `ASC` in the above SQL statement.

<!-- #endregion -->

<!-- #region -->

### You try: Use JupySQL to perform the queries and answer the questions.

Example: show the first 5 rows of the "job" variable.

```sql
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

```sql
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

```sql
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

```sql
%%sql
SELECT COUNT(*)
FROM bank
WHERE housing = 'no' AND loan = 'yes'
```
</details>
<!-- #endregion -->
<!-- #endregion -->

<!-- #region -->
As you may have noticed, SQL code is straight forward. It's clauses translate well to what you want SQL to do in natural verbal terms. These clauses make it so easy it's like you are "declaring" SQL to do what you would like it to do. This nature is what defines SQL to be a "declaritive programming language".
<!-- #endregion -->