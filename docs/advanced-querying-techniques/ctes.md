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

# Common Table Expressions (CTEs) in SQL

In this tutorial, you will learn about Common Table Expressions (CTEs) in SQL and how they can simplify your code. CTEs are temporary result sets that you can reference within other `SELECT`, `INSERT`, `UPDATE`, or `DELETE` statements. They are a powerful tool for constructing complex queries in a readable and user-friendly way. By the end of this tutorial, you will understand how to create and use CTEs in your own SQL queries.

## Set up and data access

```{important}
<b>Note:</b> The --save and %sqlcmd features used require the latest JupySQL version. Ensure you run the code below.
```

This code installs JupySQL, and DuckDB in your environment. We will be using these moving forward.

```{code-cell} ipython3
%pip install jupysql==0.7.0 jupysql-plugin --upgrade duckdb-engine --quiet
```

We continue to work with the Bank and Marketing data set.

```{important}
Source: UCI Machine Learning Repository

URL: https://archive-beta.ics.uci.edu/dataset/222/bank+marketing

Data Citation

Moro,S., Rita,P., and Cortez,P.. (2012). Bank Marketing. UCI Machine Learning Repository. https://doi.org/10.24432/C5K306.
```

We can use the following function to extract the downloaded data from the UCI repository.

```{code-cell} ipython3 :tags: [hide-output]
import sys

sys.path.insert(0, "../../")
import banking  # noqa: E402

_ = banking.BankingData("https://tinyurl.com/jb-bank", "bank")
_.extract_to_csv()
```

Initialize a DuckDB Instance

```{code-cell} ipython3
# Loading in SQL extension
%reload_ext sql
# Initiating a DuckDB database named 'bank.duck.db' to run our SQL queries on
%sql duckdb:///bank.duck.db
```

Load the data

```{code-cell} ipython3
%%sql
CREATE OR REPLACE TABLE bank AS
FROM read_csv_auto('bank_cleaned.csv', header=True, sep=',')
```

We confirm the table was loaded

```{code-cell} ipython3
%sqlcmd tables
```

We can use [JupySQL's Table Explorer](https://jupysql.ploomber.io/en/latest/user-guide/table_explorer.html) to take a quick look at the table.

```{code-cell} ipython3
%sqlcmd explore --table bank
```

## Simple CTE

Let's create a CTE that finds the average balance for each job type.

```{code-cell} ipython3
%%sql
WITH Job_Avg_Balance AS (
    SELECT job, AVG(balance) AS AverageBalance
    FROM bank
    GROUP BY job
)
SELECT * 
FROM Job_Avg_Balance;
```

In this example, the `WITH` keyword indicates the start of the CTE, which we call `Job_Avg_Balance`.

Within the `Job_Avg_Balance` CTE, we form a query that returns the average balance for each job by computing the average of `balance` and grouping by `job`. 

After closing the `WITH` statement, we then select all columns from the `Job_Avg_Balance` CTE. This returns two columns: `job` and `AverageBalance`. The final `SELECT` statement then retrieves the data from the CTE.

With the `JupySQL` magics `%sql, %%sql` and the `--save` option, you can furthermore save your CTE for later use on a different code cell:

```{code-cell} ipython3
%%sql --save avg_balance_by_job
WITH Job_Avg_Balance AS (
    SELECT job, AVG(balance) AS AverageBalance
    FROM bank
    GROUP BY job
)
SELECT * 
FROM Job_Avg_Balance;
```

```{code-cell} ipython3
%%sql
SELECT * FROM avg_balance_by_job
```

## Multiple CTEs

You can use multiple CTEs in a single query. Let's find the average balance per job type and average campaign per job type.

```{code-cell} ipython3
%%sql
WITH Job_Avg_Balance AS (
    SELECT job, AVG(balance) AS AverageBalance
    FROM bank
    GROUP BY job
),
Job_Avg_Campaign AS (
    SELECT job, AVG(campaign) AS AverageCampaign
    FROM bank
    GROUP BY job
)
SELECT * 
FROM Job_Avg_Balance, Job_Avg_Campaign 
WHERE Job_Avg_Balance.job = Job_Avg_Campaign.job;
```

In this example, the first CTE is the same as in the previous example. The second CTE `Job_Avg_Campaign` returns two columns: `job_1` and `AverageCampaign`. The final SELECT statement retrieves data from both CTEs. 

You will notice `job` and `job_1` in the final result. This is because we are doing a Cartesian product (cross join) between two CTEs and both have a column named `job`. We can avoid this by explicitly specifying the columns you want to select in our final `SELECT` statement instead of using `SELECT *`.

```{code-cell} ipython3
%%sql
WITH Job_Avg_Balance AS (
    SELECT job, AVG(balance) AS AverageBalance
    FROM bank
    GROUP BY job
),
Job_Avg_Campaign AS (
    SELECT job, AVG(campaign) AS AverageCampaign
    FROM bank
    GROUP BY job
)
SELECT Job_Avg_Balance.job, AverageBalance, AverageCampaign
FROM Job_Avg_Balance
JOIN Job_Avg_Campaign 
ON Job_Avg_Balance.job = Job_Avg_Campaign.job;
```

## Recursive CTEs

A recursive CTE is one in which an initial CTE is repeatedly executed to return subsets of data until the complete result set is obtained.

The given dataset doesn't lend itself to a recursive CTE, as these are generally used for hierarchical or recursive data problems, which the bank dataset does not present.

Here is an example of a recursive CTE

```{code-cell} ipython3
%%sql
WITH RECURSIVE numbers AS (
    SELECT 1 AS value
    UNION ALL
    SELECT value + 1 FROM numbers WHERE value < 10
)
SELECT * FROM numbers;
```

This will output a list of numbers from 1 to 10. The CTE works as follows:

* The `WITH RECURSIVE` clause marks the start of the recursive CTE.
* The `SELECT 1 AS value` is the "anchor member" of the CTE and provides the base result set for the recursion to start.
* The `UNION ALL` clause is used to combine the results of the anchor member with the results of the "recursive member", which is `SELECT value + 1 FROM numbers WHERE value < 10`.
* The recursion continues until `value < 10` returns false, at which point the CTE stops executing.

## Using CTEs to modify information in a table

```{important}
Without a unique identifier for each row in your table, performing UPDATE or DELETE operations using a CTE would be risky because they could affect more rows than you intend. 
```

It's generally not recommended to use UPDATE or DELETE without a unique identifier or precise condition to pinpoint exactly which rows you want to affect. We're going to load data from the [Joining Data in SQL tutorial](https://ploomber-sql.readthedocs.io/en/latest/intro-to-sql/joining-data-in-sql.html#load-the-data) as this data has tables with unique ID's.

```{code-cell} ipython3
_ = banking.MarketData("https://tinyurl.com/jb-bank-m", "expanded_data")
_.extract_asc_to_csv()
```

Let's work on a separate DuckDB instance

```{code-cell} ipython3
# Loading in SQL extension
%reload_ext sql
# Initiating a DuckDB database named 'bank_data.duck.db' to run SQL queries
%sql duckdb:///bank_data.duck.db
```

```{code-cell} ipython3
%%sql
CREATE SCHEMA s1;
CREATE TABLE s1.district AS
FROM read_csv_auto('expanded_data/district.csv', header=True, sep=',');
```

Let's take a look at the entries

```{code-cell} ipython3
%sqlcmd explore --table s1.district
```

Let's say `district_id` is a unique identifier for each district.

## CTE with UPDATE

When working with `UPDATE` or `DELETE` operations, it is highly recommended to check your data before and after the operations. This helps to verify that the operations were successful and only affected the intended data.

Suppose we want to update the `average_salary` for districts that had more than 5000 committed crimes in 1996 to be increased by 10%.


Check data before the operation:

```{code-cell} ipython3
%%sql
SELECT district_id, average_salary
FROM s1.district
WHERE no_of_committed_crimes_96 > 5000;
```

This is returning all entries that satisfy number of crimes committed in '96 exceeds 5000.

Perform the update:

```{code-cell} ipython3
%%sql
WITH High_Crime_Districts AS (
    SELECT district_id
    FROM s1.district
    WHERE no_of_committed_crimes_96 > 5000
)
UPDATE s1.district
SET average_salary = average_salary * 1.10
WHERE district_id IN (SELECT district_id FROM High_Crime_Districts);
```

In this example, we are writing a CTE that selects the `district_id` entries that satisfy the condition `no_of_committed_crimes_96 > 5000`. We can all this CTE `High_Crime_Districts`. 

We then use `High_Crime_Districts` to change entries in average salary by increasing it by 10% (`average_salary = average_salary * 1.10`), and ensure this is done in only those entries in the `district_id` found in the CTE `High_Crime_Districts`.

Check data after the operation:

```{code-cell} ipython3
%%sql
SELECT district_id, average_salary
FROM s1.district
WHERE no_of_committed_crimes_96 > 5000;
```

## CTE with DELETE

Suppose we want to delete records for all districts with unemployment rate in '96 greater than 4.

The query below selects only those entries for which `unemployment_rate_96` is at least 4.

Check data before the operation:

```{code-cell} ipython3
%%sql
SELECT * 
FROM s1.district
WHERE unemployment_rate_96 > 4;
```

Perform the update.

```{code-cell} ipython3
%%sql
WITH High_Unemployment_Districts AS (
    SELECT district_id
    FROM s1.district
    WHERE unemployment_rate_96 > 4
)
DELETE FROM s1.district
WHERE district_id IN (SELECT district_id FROM High_Unemployment_Districts);
```

We create a CTE called `High_Unemployment_Districts` that selects only those `district_id` whose unemployment rate in '96 exceeds 4. 

We then use the `DELETE` operation to remove all entries from the `s1.district` for only those `district_id` in the CTE `High_Unemployment_Districts`.

Check data after the operation:

```{code-cell} ipython3
%%sql
SELECT * 
FROM s1.district
WHERE unemployment_rate_96 > 4;
```

In both these examples, the operation will only affect the rows that match the conditions specified in the CTEs. The `UPDATE` operation will increase the `average_salary` of high crime districts by 10%, and the `DELETE` operation will remove all districts with high unemployment rate.

## Exercise 1 (Easy)

What is a Common Table Expression (CTE), and what is its primary use in SQL queries?

<!-- #region -->
<details>

<summary>Answers</summary>

A Common Table Expression (CTE) is a temporary result set that you can reference within another SELECT, INSERT, UPDATE, or DELETE statement. The main use of CTEs is to simplify complex SQL queries, particularly those involving multiple levels of subqueries. They make your SQL code more readable and maintainable.


</details>
<!-- #endregion -->

## Exercise 2 (Medium)

Write a SQL query using a CTE that returns the total number of inhabitants for each region in the provided dataset. Save the CTE into a variable called `region_inhabitants`

<!-- #region -->
<details>
<summary>Answers</summary>

```{code-cell} ipython3
%%sql --save region_inhabitants
WITH Region_Inhabitants AS (
    SELECT region, SUM(no_of_inhabitants) AS TotalInhabitants
    FROM s1.district
    GROUP BY region
)
SELECT * 
FROM Region_Inhabitants;
```

This CTE, `Region_Inhabitants`, groups the dataset by region and calculates the total number of inhabitants for each region using the `SUM()` function. The final SELECT statement retrieves all records from the CTE.

</details>
<!-- #endregion -->

## Exercise 3 (hard)

Suppose we want to increase the average_salary by 10% for districts that had more than 5000 committed crimes in '96, and then delete districts with an unemployment rate in '96 less than 4. Write a SQL query using CTEs to accomplish this, and explain the importance of checking the data before and after these operations.

<!-- #region -->
<details>
<summary>Answers</summary>

First, let's check the data before the operation:

```{code-cell} ipython3
%%sql 
SELECT * 
FROM s1.district
WHERE no_of_committed_crimes_96 > 5000 OR unemployment_rate_96 < 4;
```

Next, we perform the update and delete operations:

```{code-cell} ipython3
%%sql
WITH High_Crime_Districts AS (
    SELECT district_id
    FROM s1.district
    WHERE no_of_committed_crimes_96 > 5000
)
UPDATE s1.district
SET average_salary = average_salary * 1.10
WHERE district_id IN (SELECT district_id FROM High_Crime_Districts);

WITH High_Unemployment_Districts AS (
    SELECT district_id
    FROM s1.district
    WHERE unemployment_rate_96 < 4
)
DELETE FROM s1.district
WHERE district_id IN (SELECT district_id FROM High_Unemployment_Districts);
```

Finally, let's check the data after the operation:

```{code-cell} ipython3
%%sql
SELECT * 
FROM s1.district
WHERE no_of_committed_crimes_96 > 5000 OR unemployment_rate_96 < 4;
```

The importance of checking the data before and after the operations is to verify that the operations were successful and only affected the intended data. It's generally not recommended to use UPDATE or DELETE without a unique identifier or precise condition to pinpoint exactly which rows you want to affect. Checking the data before and after helps to prevent or identify potential mistakes or unexpected results in the data modification process.

</details>
<!-- #endregion -->

## Summary

In this tutorial we learned:

1. Examples of simple and multiple CTEs, as well as how to join multiple CTEs.
2. An introduction to Recursive CTEs with an example of generating a sequence of numbers.
3. A demonstration of how to use CTEs in conjunction with UPDATE and DELETE commands, as well as the importance of checking data before and after these operations.
4. A caution against performing `UPDATE` or `DELETE` operations without a unique identifier or precise condition.

In the next chapter, we will show how you can visualize the results of your SQL queries.
