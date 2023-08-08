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

# Using subqueries

A subquery is a technique that essentially embeds a query within another query. It enables users to run a query that has some kind of relation to another query in the same SQL statement. 

Let's demonstrate how powerful subqueries are by continuing with our banking data.

<!-- region -->

## Install - execute this once.

```{important}
<b>Note:</b> The `--save` and `%sqlcmd` features used require the latest JupySQL version. Ensure you run the code below to update JupySQL.
```

This code installs JupySQL, DuckDB, and Pandas in your environment. We will be using these moving forward.

```{code-cell} ipython3
%pip install jupysql duckdb-engine pandas --quiet
```

## Load the data

```{important}
<b>Note:</b> If you are following these lessons locally and <b>not</b> on Google Colab, then there is no need to load the data again. 
```

This section was covered in detail in the previous tutorial: [Joining Data in SQL](https://ploomber-sql.readthedocs.io/en/latest/intro-to-sql/joining-data-in-sql.html#load-the-data). We will be using the same data in this tutorial as well.

```{code-cell} ipython3
import sys

sys.path.insert(0, "../../")
import banking  # noqa: E402

_ = banking.MarketData("https://tinyurl.com/jb-bank-m", "expanded_data")
_.extract_asc_to_csv()
```

If you ran the above cell, you should have a folder `expanded_data` in your current directory that contains the `.csv` files we will be using. In this tutorial, we will be focusing on three of these files: `loan.csv`, `account.csv`, `district.csv`.

## Load Engine

We now load in our SQL extension that allows us to execute SQL queries in Jupyter Notebooks.

```{important}
<b>Note</b> Ensure you restart any previous notebook that has the same database name as the one initialized below.
```

```{code-cell} ipython3
# Loading in SQL extension
%reload_ext sql
# Initiating a DuckDB database named 'bank_data.duck.db' to run SQL queries
%sql duckdb:///bank_data.duck.db
```

<!-- endregion -->

## Creating Tables

Let's start off with loading three of the eight `.csv` files from the `expanded_data` folder in the current directory to our newly created DuckDB database. Like in the previous tutorial, we will [create a schema](https://ploomber-sql.readthedocs.io/en/latest/intro-to-sql/joining-data-in-sql.html#creating-a-schema) `s1` in which we will store the tables. Here we use the `CREATE TABLE` syntax in DuckDB to ingest four of the eight `.csv` files. The `read_csv_auto` is a function that helps SQL understand our local `.csv` file for creation into our database.


```{code-cell} ipython3
%%sql
CREATE SCHEMA s1;
CREATE TABLE s1.account AS
FROM read_csv_auto('expanded_data/account.csv', header=True, sep=',');
CREATE TABLE s1.district AS
FROM read_csv_auto('expanded_data/district.csv', header=True, sep=',');
CREATE TABLE s1.loan AS
FROM read_csv_auto('expanded_data/loan.csv', header=True, sep=',');
```

## Queries

Let's first load each table for reference and to better understand their contents.

```{code-cell} ipython3
%%sql
SELECT *
FROM s1.account
LIMIT 5
```

```{code-cell} ipython3
%%sql
SELECT *
FROM s1.district
LIMIT 5
```

```{code-cell} ipython3
%%sql
SELECT *
FROM s1.loan
LIMIT 5
```

### Subquery in SELECT

The query belows results in the average loan amount for each `account_id` by having a subquery in the `SELECT` clause.

```{code-cell} ipython3
%%sql
SELECT s1.account.account_id, s1.account.date, 
      (SELECT AVG(s1.loan.amount) 
      FROM s1.loan 
      WHERE s1.loan.account_id = s1.account.account_id
      ) AS average_loan_amount
FROM s1.account 
WHERE average_loan_amount IS NOT NULL
ORDER BY average_loan_amount
LIMIT 5
```

The above SQL statement is quite verbose. Let's instead utilize aliases to make the query more readable.

```{code-cell} ipython3
%%sql
SELECT a.account_id,
      (SELECT AVG(l.amount) 
      FROM s1.loan AS l 
      WHERE l.account_id = a.account_id
      ) AS average_loan_amount
FROM s1.account AS a
WHERE average_loan_amount IS NOT NULL
ORDER BY average_loan_amount
```

Let's first focus on the "outer query" of this statement. The outer query is everything in the SQL statement besides the second argument in the `SELECT` clause. This outer query results in just the `account_id` from the `s1.account` table. The "inner query" is the second argument in the `SELECT` statement. This query is called for each row from the outer query, which finds the average loan amount for each account by relation in the inner query's `WHERE` clause.

In these datasets, each account actually only has one loan. We solely specify the `AVG()` function for demonstration purposes. We also specify `IS NOT NULL` because only 682 accounts actually have loans. The remaining accounts would have a `NULL` value. 

### Subquery in FROM

In the query below, we find the average loan amount by district name while utilizing a subquery in a `FROM` clause.

```{code-cell} ipython3
%%sql
SELECT d.district_name, 
       ROUND(AVG(inner_query.amount),2) AS average_loan_amount
FROM 
    (SELECT l.loan_id, 
            l.amount, 
            a.district_id 
    FROM s1.loan AS l 
    INNER JOIN s1.account AS a 
      ON l.account_id = a.account_id
    ) AS inner_query
INNER JOIN s1.district AS d
  ON inner_query.district_id = d.district_id
GROUP BY d.district_name
```
This query demonstrates how to have a subquery act as another table when performing an `INNER JOIN` in the outer query. There is also an `INNER JOIN` in the inner query that creates a joined table between the `s1.account` and `s1.loan` tables. This subquery then gives us the necessary information to join with our `s1.district` table.

The query shown above can be easily implemented using JupySQL's `--save` feature. This feature essentially allows us to save a query and use it for future use. We implement the `--save` feature below by recreating the previous query.

We first `--save` the subquery as `loan_amount_district_id`.

```{code-cell} ipython3
%%sql --save loan_amount_district_id
SELECT l.loan_id, 
        l.amount, 
        a.district_id 
FROM s1.loan AS l 
INNER JOIN s1.account AS a 
    ON l.account_id = a.account_id
```

Then call the saved subquery and use it to complete our overall query.

```{code-cell} ipython3
%%sql 
SELECT d.district_name, 
       ROUND(AVG(inner_query.amount),2) AS average_loan_amount
FROM (SELECT *
      FROM loan_amount_district_id) AS inner_query
INNER JOIN s1.district AS d 
    ON inner_query.district_id = d.district_id
GROUP BY d.district_name
```

### Subquery in WHERE

This example calls a subquery from a statement's `WHERE` clause.

```{code-cell} ipython3
%%sql
SELECT *
FROM s1.loan
WHERE amount > (
  SELECT AVG(amount) 
  FROM s1.loan 
  WHERE status = 'A'
)
```

With this query, we are able to see all loans that are greater than the average loan amount for 'A' status loans.

Let's again demonstrate how we can use `--save` to recreate this query.

```{code-cell} ipython3
%%sql --save avg_A_amount
SELECT AVG(amount) 
FROM s1.loan 
WHERE status = 'A'
```

```{code-cell} ipython3
%%sql
SELECT *
FROM s1.loan
WHERE amount > (
  SELECT *
  FROM avg_A_amount) 
```

Note that we do not have to assign an alias to our saved query because none of its variables are in the outer query's `SELECT` clause.

## Examining Our Snippets with JupySQL

To examine all of our saved queries with `--save`, we can use `%sqlcmd snippets`.

```{code-cell} ipython3
%sqlcmd snippets
```

Our saved queries (also known as snippets) can be deleted with the `--delete` feature.
For more information on snippets, please visit JupySQL's official documentation [here].(https://jupysql.ploomber.io/en/latest/api/magic-snippets.html)

## Viewing Our Tables with JupySQL

JupySQL also has features that allow for quick displays of tables and their columns. We can examine them with `%sqlcmd tables` and `%sqlcmd columns`.

```{code-cell} ipython3
%sqlcmd tables -s s1
```

The above code cell shows all tables under the `s1` schema. Recall that we assigned a schema to these tables at the beginning of this section.

`%sqlcmd columns` allows us to examine each column in a table with added additional information.

```{code-cell} ipython3
%sqlcmd columns -s s1 -t account
```

In the above code-cell, we specify the schema and the table under the schema to examine.

<b>Note:</b> for now, JupySQL does not support the use of these magic commands with queries saved with `--save`. 

For more information on these magic commands, please visit JupySQL's official documentation [here].(https://jupysql.ploomber.io/en/latest/api/magic-tables-columns.html)

## You try: Use JupySQL to perform the queries and answer the questions.

### Question 1 (Easy):
Query loans with an `amount` greater than or equal to the `AVG()` loan amount. Utilize the `--save` feature to help you solve this question.

<!-- #region -->
<details>

<summary>Answers</summary>

First, create a snippet with `--save` containing the `AVG()` loan amount.

```{code-cell} ipython3
%%sql --save average_loan_amount
SELECT AVG(amount)
FROM s1.loan
```

Then we reference `average_loan_amount` as a subquery to filter for loan id's that are greater than or equal to this average.

```{code-cell} ipython3
%%sql
SELECT loan_id
FROM s1.loan
WHERE amount >= (SELECT * 
                FROM average_loan_amount)
```

</details>
<!-- #endregion -->


### Question 2 (Medium):
Find all `account_id`'s that have a loan alongside with their loan status, their loan amount, and the average loan amount for their loan's loan status. Order by `account_id`.


<!-- #region -->
<details>

<summary>Answers</summary>

The difficult part of this question lies in the second `INNER JOIN`. This second `INNER JOIN` uses a subquery to have the average amount of each 'status'. This information is used when calling the last `INNER JOIN` on the outer query's 'status' variable.


```{code-cell} ipython3
%%sql
SELECT a.account_id, 
       l.status AS loan_status, 
       l.amount AS loan_amount, 
       ROUND(avg_status_loan.amount,2) AS average_loan_amount
FROM 
    s1.account AS a
INNER JOIN 
    s1.loan AS l ON a.account_id = l.account_id
INNER JOIN (SELECT status, 
                   AVG(amount) AS amount
            FROM s1.loan
            GROUP BY status
            ) AS avg_status_loan ON l.status = avg_status_loan.status
ORDER BY a.account_id
```

</details>
<!-- #endregion -->

### Question 3 (Hard):
Query the `district_id` and `district_name` that have the highest amount of loans for each loan status type.

To answer this question, let's quickly learn about `UNION ALL`. `UNION ALL` is a clause that concatenates rows on top of each other. An example is shown below.

Using `UNION ALL`, we can achieve the correct results. Try to incorporate the `--save` feature to make your query easier to read.

<!-- #region -->
<details>
<summary>Answers</summary>

We find the district with the highest loan status type by first joining the three necessary tables `s1.account`, `s1.district`, and `s1.loan`. These three tables are used in an inner query for each loan status type. Then, in each of these inner queries, we query the district id, district name, and the count of the first row after ordering by count. We finalize the query by "stacking" these results with `UNION ALL`.

```{code-cell} ipython3
%%sql
SELECT district_id, district_name, 'A' as status, count
FROM
    (SELECT a.district_id, d.district_name, COUNT(*) as count
    FROM s1.account a
    JOIN s1.loan l ON a.account_id = l.account_id
    JOIN s1.district d ON a.district_id = d.district_id
    WHERE l.status = 'A'
    GROUP BY a.district_id, d.district_name
    ORDER BY count DESC
    LIMIT 1) as A_max
UNION ALL
SELECT district_id, district_name, 'B' as status, count
FROM
    (SELECT a.district_id, d.district_name, COUNT(*) as count
    FROM s1.account a
    JOIN s1.loan l ON a.account_id = l.account_id
    JOIN s1.district d ON a.district_id = d.district_id
    WHERE l.status = 'B'
    GROUP BY a.district_id, d.district_name
    ORDER BY count DESC
    LIMIT 1) as B_max
UNION ALL
SELECT district_id, district_name, 'C' as status, count
FROM
    (SELECT a.district_id, d.district_name, COUNT(*) as count
    FROM s1.account a
    JOIN s1.loan l ON a.account_id = l.account_id
    JOIN s1.district d ON a.district_id = d.district_id
    WHERE l.status = 'C'
    GROUP BY a.district_id, d.district_name
    ORDER BY count DESC
    LIMIT 1) as C_max
UNION ALL
SELECT district_id, district_name, 'D' as status, count
FROM
    (SELECT a.district_id, d.district_name, COUNT(*) as count
    FROM s1.account a
    JOIN s1.loan l ON a.account_id = l.account_id
    JOIN s1.district d ON a.district_id = d.district_id
    WHERE l.status = 'D'
    GROUP BY a.district_id, d.district_name
    ORDER BY count DESC
    LIMIT 1) as D_max
```

We can make the above query easier to understand by using JupySQL's `--save` feature.

```{code-cell} ipython3
%%sql --save A
SELECT a.district_id, d.district_name, COUNT(*) as count
FROM s1.account a
JOIN s1.loan l ON a.account_id = l.account_id
JOIN s1.district d ON a.district_id = d.district_id
WHERE l.status = 'A'
GROUP BY a.district_id, d.district_name
ORDER BY count DESC
LIMIT 1
```

```{code-cell} ipython3
%%sql --save B
SELECT a.district_id, d.district_name, COUNT(*) as count
FROM s1.account a
JOIN s1.loan l ON a.account_id = l.account_id
JOIN s1.district d ON a.district_id = d.district_id
WHERE l.status = 'B'
GROUP BY a.district_id, d.district_name
ORDER BY count DESC
LIMIT 1
```

```{code-cell} ipython3
%%sql --save C
SELECT a.district_id, d.district_name, COUNT(*) as count
FROM s1.account a
JOIN s1.loan l ON a.account_id = l.account_id
JOIN s1.district d ON a.district_id = d.district_id
WHERE l.status = 'C'
GROUP BY a.district_id, d.district_name
ORDER BY count DESC
LIMIT 1
```

```{code-cell} ipython3
%%sql --save D
SELECT a.district_id, d.district_name, COUNT(*) as count
FROM s1.account a
JOIN s1.loan l ON a.account_id = l.account_id
JOIN s1.district d ON a.district_id = d.district_id
WHERE l.status = 'D'
GROUP BY a.district_id, d.district_name
ORDER BY count DESC
LIMIT 1
```

We can then use these saved snippets and concatenate their results using `UNION ALL`.

```{code-cell} ipython3
%%sql
SELECT * 
FROM A 
UNION ALL 
SELECT *
FROM B
UNION ALL
SELECT *
FROM C
UNION ALL
SELECT *
FROM D
```

</details>
<!-- #endregion -->

### Question 4 (Bonus):
Output the `COUNT()` of of each unique 'status' variable under `s1.loan` that are greater than the average of 'A' type loans. Have the outputs be only five columns for each 'status' type with a single value each alongside with the total number of loans. You must use one or more subqueries.

<b>Hint</b> `CASE WHEN` is a clause that acts as a conditional statement when performing other SQL actions. Try to see how you can incorporate `CASE WHEN` with `COUNT()` to answer this question.

<!-- #region -->
<details>
<summary>Answers</summary>

For each `SELECT` argument, we are finding the count of each status using `CASE WHEN` to have a "1" count when aggregating the 'status' values. This allows our query to have the correct counts for each value given that the loan amount is less than the average 'A' loan amount. 

```{code-cell} ipython3
%%sql 
SELECT COUNT(CASE WHEN status = 'A' THEN 1 END) AS A,
       COUNT(CASE WHEN status = 'B' THEN 1 END) AS B,
       COUNT(CASE WHEN status = 'C' THEN 1 END) AS C,
       COUNT(CASE WHEN status = 'D' THEN 1 END) AS D,
       COUNT(*) AS Total
FROM s1.loan
WHERE amount > (
        SELECT AVG(amount)
        FROM s1.loan
        WHERE status = 'A'
    )

```
</details>
<!-- #endregion -->


## Wrapping Up

In this section, we introduced subqueries and how they can be implemented with common clauses. Subqueries are an incredibly powerful and intuitive technique that can serve as an alternative to joins, as well as enable users to utilize the results of one query within another query.

We also explored how we can make subqueries more readable using JupySQL's `--save` feature. Alongside this, we introduced some additional JupySQL magic commands such as `%sqlcmd tables` and `%sqlcmd columns` to view current tables in our schema.

In the next section, you will learn how to implement more advanced join techniques to your queries.