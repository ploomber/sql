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

# Advanced aggregation operations in SQL

In the last section, we learned about advanced joins. In similar fashion, aggregate functions, which were introduced in the [Introduction to SQL](https://ploomber-sql.readthedocs.io/en/latest/intro-to-sql/aggregate-functions-in-sql.html) module, also have advanced operations.

Recall that aggregation functions are useful for summarizing your data and for finding meaningful insights. The most common of these functions are `COUNT()`, `AVG()`, `SUM()`, `MIN()`, `MAX()`, `GROUPBY()`, and `HAVING`. However, in this section, we will focus on operations that help us handle tasks that are hard to implement efficiently with
basic aggregation features.

Specifically, we will learn about ranking (`RANK()`), windowing (`OVER()`), pivoting (`PIVOT()`), and rollup (`ROLLUP()`).

Let's first run the installations and setup before running any queries.

<!-- region -->

## Load the data
<b>Note:</b> If you are following these lessons locally and <b>not</b> on Google Colab, then there is no need to load the data again. 

This section was covered in detail in the tutorial: [Joining Data in SQL](https://ploomber-sql.readthedocs.io/en/latest/intro-to-sql/joining-data-in-sql.html#load-the-data). We will be using the same data in this tutorial as well.

```{code-cell} ipython3
import banking_data_script

# ZIP file download link
link = "http://sorry.vse.cz/~berka/challenge/pkdd1999/data_berka.zip"
# Naming our folder that will hold our .csv files
output = "expanded_data"
banking_data_script.extract_asc_to_csv(link, output)
```

If you ran the above cell, you should have a folder `expanded_data` in your current directory that contains the `.csv` files we will be using. However, in this tutorial, we will focus on one file: `loan.csv`.

## Load Engine
We now load in our SQL extension that allows us to execute SQL queries in Jupyter Notebooks.

<b>Note</b> Ensure you restart any previous notebook that has the same database name as the one initialized below.

```{code-cell} ipython3
# Loading in SQL extension
%reload_ext sql
# Initiating a DuckDB database named 'bank_data.duck.db' to run SQL queries
%sql duckdb:///bank_data.duck.db
```

Let's now return to our initial dataset of bank marketing records.

## Queries

### Creating Table

Let's start off with loading the `loan.csv` file from the `expanded_data` folder in the current directory to our newly created DuckDB database. Because we will be working with one table, [creating a schema](https://ploomber-sql.readthedocs.io/en/latest/intro-to-sql/joining-data-in-sql.html#creating-a-schema) is not required.

```{code-cell} ipython3
%%sql
CREATE TABLE loan AS
FROM read_csv_auto('expanded_data/loan.csv', header=True, sep=',');
```

### Ranking

`RANK()` finds the position of a value within a result set. For instance, we may wish to assign customers a rank based on the date when the loan was granted, with the rank 1 going to the customer with the highest date, the rank 2 to the customer with the next highest date, and so on.

<b>Note:</b> The `date` variable in the `loan` data is an integer, in the format YYMMDD, and will be used throughout the examples below.

#### General Syntax

The general syntax of the rank function is:

```python
%%sql 
RANK() OVER (ORDER BY expr [ASC|DESC] [, expr [ASC|DESC]] ...)
```

`RANK()` is executed by the attributes (or expressions) specified in the `OVER (ORDER BY())` clause. <b>Without this clause, `RANK()` will return the same value for each row</b>. 

Each order by expression optionally it can be followed by `ASC` or `DESC` to indicate the sort direction. <b>The default is `ASC` if no direction is specified</b>. `NULL` values are sorted first for ascending sorts and last for descending sorts.

The following query gives the rank of each customer:

```{code-cell} ipython3
%%sql 
SELECT account_id, RANK() OVER (ORDER BY (date) DESC) AS c_rank
FROM loan;
```

Although the tuples above are ordered by rank, sometimes they may not. Therefore, an extra, outer `ORDER BY()` clause is needed to ensure they are:

```python
%%sql 
SELECT account_id, RANK() OVER (ORDER BY (date) DESC) as c_rank
FROM loan
ORDER BY c_rank;
```

```{important}
The `RANK()` function gives the same rank to all tuples that are equal on the `ORDER BY()` attributes. For instance, if the highest date is shared by two customers, both would get rank 1. The next rank given would be 3, not 2, so if three customers have the next highest date, they would all get rank 3, and the next 10 customer(s) would get rank 6, and so on. 
```

There is also a `DENSE_RANK` clause that does not create gaps in the ordering and an example is as follows:

```{code-cell} ipython3
%%sql 
SELECT account_id, RANK() OVER (ORDER BY (date) DESC) as c_rank, DENSE_RANK() OVER (ORDER BY (date) DESC) AS d_rank
FROM loan
ORDER BY c_rank;
```

Several other functions can be used apart from `RANK` or `DENSE_RANK`:

- `PERCENT_RANK` returns the rank of each tuple as a fraction between 0 and 1
- `CUME_DIST` returns the cumulative distribution of each tuple
- `NTILE` takes tuples in each partition (more below!) and divides them into buckets
- `ROW_NUMBER` sorts the rows and gives each row a unique number corresponding to its position in the sort order

#### Partitioning/Grouping

`RANK()` can also be used to rank tuples within groups. For instance, we may wish to rank customers by the date when the loan was granted, grouped by their status of paying off the loan. This can be done by partitioning the tuples, with a `PARTITION BY` clause within `OVER()`, by `status` (A, B, C, or D) and then ordering them by `date` within each `status`:

```{code-cell} ipython3
%%sql
SELECT account_id, status, DENSE_RANK() OVER (PARTITION BY status ORDER BY (date) DESC) AS grouped_rank
FROM loan
ORDER BY grouped_rank;
```

For reference, the different statuses represent:

- 'A' stands for contract finished, no problems
- 'B' stands for contract finished, loan not payed
- 'C' stands for running contract, OK so far
- 'D' stands for running contract, client in debt

#### Question 1 (Medium):
Rank, in <b>descending</b> order, the customers by the `date` when the loan was granted, grouped by their `status` of paying off the loan. Also, find the average loan `amount` of customers by `status` and `date` and round it to 0 decimal places.

<b>Hint</b> Think about which basic aggregation clauses you will need to use to find the average loan amount by `status` and `date`. Once that is done, arrange the tuples in descending order of their rank.

<!-- #region -->
<details>

<summary>Answers</summary>

The SQL query here is very similar to the `DENSE_RANK` query above. The only difference is that we need to find the average loan amount by `status` and `date` and round it to 0 decimal places. To do this we need two basic aggregation clauses: `AVG()` and `GROUP BY()`. Without the `GROUP BY()` clause, the appropriate average amount cannot be found. Moreover, the correct columns need to be specified in it, including `account_id`, `status`, and `date`, to obtain the rank of each customer by `status` and `date`. Lastly, to order the tuples in descending order of their rank, we need to add the `DESC` clause.

```{code-cell} ipython3
%%sql
SELECT account_id, status, ROUND(AVG(amount), 0) as avg_amount, DENSE_RANK() OVER (PARTITION BY status ORDER BY date DESC) AS grouped_rank
FROM loan
GROUP BY account_id, status, date
ORDER BY grouped_rank DESC;
```

```{important}
Try changing the `DENSE_RANK()` clause to `RANK()`. What do you notice? Why do you think this is the case?
```

</details>
<!-- #endregion -->

### Windowing

It is relatively easy to write an SQL query using those features we have already studied to compute an aggregate over one window, for example, loan amounts over a fixed 3-day period. However, if we want to do this for <b>every</b> 3-day period, like a moving-average, the query becomes cumbersome.

Window queries compute an aggregate function over ranges of tuples by accessing the records right before or after the current record. A set of rows to which this aggregation function applies to is referred to as a <b>window</b>. 

```{important}
Windows may overlap, in which case a tuple may contribute to more than one window. <b>This is unlike the partitions we learnt about earlier</b>, where a tuple could contribute to only one partition.
```

#### General Syntax

Windowing is performed with the following syntax: `OVER` ( [partition] [order] [frame] )

It allows a <b>frame</b> to move within a partition depending on the position of the current row within its partition. The offsets of the current row and frame rows are the <b>row numbers</b> if the frame unit is `ROWS` and <b>row values</b> if the frame unit is `RANGE`.

Frames and its operations can be represented with the following:

- frame: {<i>frame_start</i> | <i>frame_between</i>}

- frame_between: `BETWEEN` <i>frame_start</i> AND <i>frame_end</i>

- frame_start, frame_end: {
  `CURRENT ROW`
  | `UNBOUNDED PRECEDING`
  | `UNBOUNDED FOLLOWING`
  | <i>expr</i>  `PRECEDING`
  | <i>expr</i>  `FOLLOWING` }

![](windowing.jpg)

#### Examples

1. The first 14 rows of the `loan` table have unique, non-consecutive dates ranging from July 5th 1993 to December 1st 1993. Therefore, we can compute the average loan amount over the three preceding tuples in the specified sort order. Note that this example makes sense only because each date, for the first 14 records, appears only once in `loan`. The example is as follows:

```{code-cell} ipython3
%%sql
SELECT date, AVG(amount) OVER (ORDER BY date ROWS 3 PRECEDING) AS avg_amount
FROM loan
WHERE date <= 931201;
```

This is not the case across the whole table, which means there are several possible orderings of tuples since tuples for the same date could be in any order. To tackle this, we introduce in the example below a windowing query that uses a <b>range</b> of values instead of a specific number of tuples.

2. Suppose that instead of going back a fixed number of tuples, we want the window to consist of all prior dates. That means the number of prior dates considered is not fixed and, hence, we can perform this on the entire dataset. To get the average amount over all prior dates, we write:

```{code-cell} ipython3
%%sql
SELECT date, AVG(amount) OVER (ORDER BY date RANGE UNBOUNDED PRECEDING) AS avg_amount
FROM loan;
```

```{important}
The `ROUND()` function is not recognized as an aggregate function in DuckDB. In the above query, If we modified the above `SELECT` clause to have `ROUND(AVG(amount),0)`, we would get an error because we tried to use the `ROUND()` function within the `OVER` clause, which is not supported in DuckDB. To fix it, use a subquery in the `FROM` clause as follows:
```

```{code-cell} ipython3
%%sql
SELECT date, ROUND(avg_amount, 2) AS rounded_avg_amount
FROM (SELECT date, AVG(amount) OVER (ORDER BY date ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING) AS avg_amount FROM loan);
```

<b>Note:</b> It is possible to use the keyword `FOLLOWING` in place of `PRECEDING`. If we did this in our example, the year value specifies the beginning of the window instead of the end. However, we will need to specify it using `BETWEEN`, explained below!

3. Using `BETWEEN` for `UNBOUNDED FOLLOWING` is necessary because DuckDB does not allow a frame to start with `UNBOUNDED FOLLOWING`:

```{code-cell} ipython3
%%sql
SELECT date, ROUND(avg_amount, 2) AS rounded_avg_amount
FROM (SELECT date, AVG(amount) OVER (ORDER BY date ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING) AS avg_amount FROM loan);
```

#### Question 2 (Hard):

Return the maximum loan `amount`, rounded to 0 decimals, by the customer's `status` for paying off the loan for every three dates preceding and every two dates following the current date of a tuple . Also, order the output by ascending order of `date`.

<b>Hint</b> Think about which advanced aggregation clause is needed to return the loan `amount` by `status`. Then, think about how to build the query for rounding the values.

<!-- #region -->
<details>

<summary>Answers</summary>

The SQL query here is very similar to the third windowing function example. We can write windowing queries that treat each status separately by partitioning by `status`. Therefore, we need to add a `PARTITION BY` clause before the `ORDER BY` clause, like the ranking example, to account for `status`, use the `MAX` aggregation clause instead of `AVG`, add an extra `ORDER BY` clause at the end of the query, and change the frame selection to include both `PRECEDING` and `FOLLOWING` as follows:

```{code-cell} ipython3
%%sql
SELECT date, status, ROUND(max_amount, 0) AS rounded_max_amount
FROM (SELECT date, status, MAX(amount) OVER (PARTITION BY status ORDER BY date ROWS BETWEEN 3 PRECEDING AND 2 FOLLOWING) AS max_amount FROM loan)
ORDER BY date;
```

Try playing around with different frame selections and aggregation functions to develop your intuition!

+++

</details>
<!-- #endregion -->

### Pivoting

Using SQL aggregation functions, we can easily create cross-tabulations (or cross-tabs for short), which takes a column of data and turns it into multiple columns, one for each unique value in the original column. It can also perform aggregations on the data, such as calculating the average or sum of the values in each column, useful for summarizing data.

```{important}
DuckDB supports the `PIVOT` operator, but other databases, such as MySQL, do not. Yet, pivoting can be made possible and we shall explore below.
```

#### General Syntax

The syntax for `PIVOT` is as follows:

```python
PIVOT [dataset] 
ON [column(s)] 
USING [value(s)] 
GROUP BY [row(s)]
```

For other databases (and DuckDB), the `CASE WHEN` clause can be used to pivot data:

```python
SELECT pivot_column,
SUM(
    CASE 
        WHEN pivot_column = pivot_value THEN aggregate_column
        WHEN pivot_column = pivot_value THEN aggregate_column
        ELSE 0
    END
) AS alias
FROM table
GROUP BY pivot_column;
```

#### Examples

Suppose we want to obtain the total loan `amount` by both the customer's `status` of paying off the loan and the `duration` of the loan. We can do this by pivoting the `status` column, summing the `amount` column, and grouping the `duration` column:

```{code-cell} ipython3
%%sql
PIVOT loan ON status USING SUM(amount) GROUP BY duration;
```

Using, `CASE WHEN` we get identical results:

```{code-cell} ipython3
%%sql
SELECT duration,
    SUM(CASE WHEN status = 'A' THEN amount ELSE 0 END) AS A,
    SUM(CASE WHEN status = 'B' THEN amount ELSE 0 END) AS B,
    SUM(CASE WHEN status = 'C' THEN amount ELSE 0 END) AS C,
    SUM(CASE WHEN status = 'D' THEN amount ELSE 0 END) AS D,
FROM loan
GROUP BY duration;
```

#### Question 3 (Medium):

For all the customers' `status` of paying off the loan, `duration` of the loan, and `date` of the loan, return both the average loan `amount`. Make sure to return `date` in the first column and only those columns that have combinations of `status` and `duration` values in them (i.e no columns with only `None` values should be displayed).

<b>Hint</b> Because the output should contain the `date` column first, we use a `GROUP BY` for it. Multiple `ON` columns and expressions can be specified in the `PIVOT` clause along with multiple `USING` expressions. The expression `||'_'||` can be used not only to concatenate the columns, but also to pivot only the combinations of values that are present in the data. The order of the columns will, hence, be: date, A_12_sum(amount), A_24_sum(amount), A_36_sum(amount),..., D_60_sum(amount)

<!-- #region -->
<details>

<summary>Answers</summary>

```{code-cell} ipython3
%%sql
PIVOT loan ON status ||'_'|| duration USING SUM(amount) GROUP BY date;
```

Try playing with multiple variables in the `ON`, `USING`, and `GROUP BY` clauses and see if you can explore the data more closely!

</details>
<!-- #endregion -->

### Grouping Sets, Rollup, and Cube

To perform a grouping over multiple dimensions within the same query, the following clauses can be used with `GROUP BY`:

- `GROUPING SETS` perform the same aggregate across different `GROUP BY` clauses in a single query.
- `ROLLUP` produces all <b>“sub-groups”</b> of a grouping set, e.g. `ROLLUP (country, city, zip)` produces the grouping sets (country, city, zip), (country, city), (country), () where () denotes an <b>empty group by</b> list. Therefore, placement of variables matters here because only the first variable's individual aggregation is output. This produces <b>n+1 grouping sets</b> where n is the number of terms in the `ROLLUP` clause.
- `CUBE`: produces grouping sets for all combinations of the inputs, e.g. `CUBE (country, city, zip)` will produce (country, city, zip), (country, city), (country, zip), (city, zip), (country), (city), (zip), (). This produces <b>2^n grouping sets</b>.

```{important}
Neither the `ROLLUP` nor the CUBE` clause gives complete control on the groupings that are generated. Therefore, `GROUPING SETS` is the most flexible of the three.
```

#### Examples

Suppose we want to obtain the number of `account_id`'s by the customer's `status` of paying off the loan and the `duration` of the loan together and separately. We can do this by using `GROUPING SETS`:

```{code-cell} ipython3
%%sql
SELECT status, duration, COUNT(account_id) AS count_account_id
FROM loan
GROUP BY GROUPING SETS ((), status, (status, duration), duration);
```

Using `CUBE`, which helps us condense the above `GROUP BY` clause, we can get identical results:

```{code-cell} ipython3
%%sql
SELECT status, duration, COUNT(account_id) AS count_account_id
FROM loan
GROUP BY CUBE (status, duration);
```

#### Question 4 (Easy):

Find the maximum loan `amount` in the following groupings: {(date, duration), (status, duration)}.

<!-- #region -->
<details>

<summary>Answers</summary>

Recall the note at the beginning of this section, which stated that neither `ROLLUPS` nor `CUBE` can be used to specify restricted groupings, like in the question above. Therefore, we use `GROUPING SETS`:

```{code-cell} ipython3
%%sql
SELECT date, duration, status, MAX(amount) AS max_amount
FROM loan
GROUP BY GROUPING SETS ((date, duration), (status, duration));
```

</details>
<!-- #endregion -->

## Wrapping Up

In this section, we introduced advanced aggregation functions. To summarize:

- `RANK()` : Returns the rank of each row in the result set. It needs to be used with the `OVER (ORDER BY())` clause. It can also be used with `PARTITION BY` to rank within a group.

- Windowing : Helps obtain moving-aggregations either through the whole dataset or a subset of it, depending on the frame selection. Executed with the syntax `OVER` ( [partition] [order] [frame] ).

- `PIVOT()` : Produces a cross-tab for summarizing datasets based on one or many column(s). Can be emulated with `CASE WHEN` statements for compatibility with other SQL dialects.

- Groupings : `GROUPING SETS` provides the most flexibility out of `ROLLUP` and `CUBE`.

This ends the module <b>Advanced querying techniques</b> and we hope you enjoyed it! Next, we will learn about how to visualize your queries using popular Python libraries, including `matplotlib` and `seaborn`, and `ggplot`!

<!-- #endregion -->

## References

Silberschatz, A., Korth, H. F., &amp; Sudarshan, S. (2020). Database system concepts. McGraw-Hill.

DuckDB. (n.d.). https://duckdb.org/docs/
