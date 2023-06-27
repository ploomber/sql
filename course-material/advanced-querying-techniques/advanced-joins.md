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

# Advanced join operations in SQL


## Install - execute this once.

```{important}
<b>Note:</b> The `--save` and `%sqlcmd` features used require the latest JupySQL version. Ensure you run the code below to update JupySQL.
```

This code installs JupySQL, DuckDB, and Pandas in your environment. We will be using these moving forward.

```{code-cell} ipython3
%pip install jupysql --upgrade duckdb-engine pandas --quiet
```

## Load the data

```{important}
<b>Note:</b> If you are following these lessons locally and <b>not</b> on Google Colab, then there is no need to load the data again. 
```

This section was covered in detail in the previous tutorial: [Joining Data in SQL](https://ploomber-sql.readthedocs.io/en/latest/intro-to-sql/joining-data-in-sql.html#load-the-data). We will be using the same data in this tutorial as well.

```{code-cell} ipython3
import banking_data_script

# ZIP file download link
link = "http://sorry.vse.cz/~berka/challenge/pkdd1999/data_berka.zip"
# Naming our folder that will hold our .csv files
output = "expanded_data"
banking_data_script.extract_asc_to_csv(link, output)
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

The code above will create three tables in the database schema: `s1.account`, `s1.district`, `s1.loan`. 

## Exploring the data

Let's take a look at its entries.

```{code-cell} ipython3
%sqlcmd explore --table s1.account
```

```{code-cell} ipython3
%sqlcmd explore --table s1.district
```

```{code-cell} ipython3
%sqlcmd explore --table s1.loan
```

## Nested-loop joins

A nested loop join compares each row from the first table with each row from the second table to find all pairs of rows which satisfy the join predicate.

### When to use

This strategy is generally used when one of the tables in the join is significantly smaller than the other. The small table (or sometimes just a subset of it) can be kept in memory while the larger table is scanned, allowing for efficient access to the smaller table.


```{code-cell} ipython3
%%sql
SELECT DISTINCT a.account_id, a.district_id, a.frequency, a.date, l.loan_id, l.date as date_1, l.amount, l.duration, l.payments, l.status
FROM s1.account a, s1.loan l
WHERE a.account_id = l.account_id
LIMIT 5;
```

## Merge joins

Merge join combines two sorted lists like a zipper based on the join predicates.

### When to use

This is a very efficient join strategy when the join columns of both tables are sorted, or when the database can efficiently sort them. If you know that your tables are sorted on the join column, this strategy is likely to be chosen.

```{code-cell} ipython3
%%sql
SELECT *
FROM s1.account a
INNER JOIN s1.district d
ON a.district_id = d.district_id
LIMIT 5;
```

## Hash joins

A hash join uses a hash table for finding matching rows. The table is partitioned based on the hash value of the join column(s).

### When to use

This strategy is typically used when the join columns are not sorted, and neither table is much smaller than the other. The database builds a hash table from one of the tables, then scans the other table and uses the hash table to find matching rows. If your tables are large and not sorted on the join columns, the database is likely to use this strategy.

Since `DuckDB` doesn't support join hints, the corresponding SQL query example for join hints (SELECT /*+ HASH_JOIN(a, l) */ *...) it's just for illustration purposes and doesn't actually force a hash join in `DuckDB`.

```{code-cell} ipython3
%%sql
SELECT *
FROM s1.account a
JOIN s1.district d
ON a.district_id = d.district_id
LIMIT 5;
```

## Internal joins

An internal join combines rows from different tables if the join condition is true.

### When to use

In the context of DuckDB, we can't explicitly choose an "internal join". But in terms of a join operation that uses indexes to expedite the join process, this would be most applicable when you have indexed your join columns, and these indexes can be effectively used by the database engine to perform the join operation faster.

```{code-cell} ipython3
%%sql
SELECT *
FROM s1.account a
JOIN s1.district d ON a.district_id = d.district_id
JOIN s1.loan l ON a.account_id = l.account_id
LIMIT 5;
```

## Join hints

Join hints are a way to influence the join strategy chosen by the SQL server. For instance, you can suggest using a loop, hash, or merge join.

### When to use

DuckDB does not support join hints. The optimizer in DuckDB chooses the join method based on the table statistics and query specifics. In most cases, letting the optimizer make this decision is the best choice.

```{code-cell} ipython3
%%sql
SELECT /*+ HASH_JOIN(a, l) */ *
FROM s1.account a
JOIN s1.loan l ON a.account_id = l.account_id
LIMIT 5;
```

## Exercise 1

Given an account id (e.g., 1787), retrieve all loan records for that account.

<!-- #region -->
<details>

<summary>Answers</summary>

We can use a Nested-loop Join on `s1.account` as `a` and `s1.loan` as `l` where the `account_id` matches in each table, and where the `account_id` is `1787`.

```{code-cell} ipython3
%%sql 
SELECT *
FROM s1.account a
JOIN s1.loan l ON a.account_id = l.account_id
WHERE a.account_id = 1787;
```


</details>
<!-- #endregion -->

## Exercise 2

Retrieve all account and district information for accounts with district_id between 10 and 20.

<!-- #region -->
<details>

<summary>Answers</summary>

We can use a Merge Join on `s1.account` as `a` and `s1.district` as `d` where the `district_id` matches in each table, and where the `district_id` is between 10 and 20.

```{code-cell} ipython3
%%sql 
SELECT *
FROM s1.account a
JOIN s1.district d ON a.district_id = d.district_id
WHERE d.district_id BETWEEN 10 AND 20;
```


</details>
<!-- #endregion -->

## Exercise 3

Retrieve all account, loan and district information.

<!-- #region -->
<details>

<summary>Answers</summary>

We can use a Hash Join on `s1.account` as `a` and `s1.district` as `d` where the `district_id` matches in each table. We can then join this to the `s1.loan` table as `l` where the `account_id` in `a` and `l` match. 

```{code-cell} ipython3
%%sql 
SELECT *
FROM s1.account a
JOIN s1.district d ON a.district_id = d.district_id
JOIN s1.loan l ON a.account_id = l.account_id;
```


</details>
<!-- #endregion -->

## Conclusion

In this tutorial, we have explored advanced join operations in SQL, including nested-loop joins, merge joins, hash joins, internal joins, and the concept of join hints. We learned how to utilize these different join methods in SQL queries and understood the specific scenarios in which each type of join is most efficient.

We used DuckDB as our SQL engine and the banking dataset for our exercises. DuckDB is an excellent tool for SQL queries because of its ease of use and integration with the Jupyter notebook environment. However, it's important to note that DuckDB's query optimizer chooses the join method based on the table statistics and query specifics. So while the SQL examples in this tutorial illustrate the syntax and usage of different types of joins, the actual join type chosen by DuckDB might differ.

