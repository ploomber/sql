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

# Joining data in SQL

This section introduces a fundamental concept in SQL: <b>joining</b>. Joining is a powerful technique used to combine data from multiple tables based on their relationships. It allows you to supplement a dataset with additional information from another related dataset.

To show the capabilites of joining, we move away from the single bank dataset we initially used in this course. We will be incorporating several new datasets illustrated below.

## Datasets

The datasets we will be using originates from another bank's financial data. 

Source: https://web.archive.org/web/20180506061559/http://lisp.vse.cz/pkdd99/Challenge/chall.htm

We first focus on just two datasets, the `account` and `district` dataset. To expedite our progress, we will skip the detailed explanation of each dataset's variables and dive straight into how joining works.

For a comprehensive understanding of the data structure and attributes, please refer to the datasets' documentation.

Documentation: https://web.archive.org/web/20180506035658/http://lisp.vse.cz/pkdd99/Challenge/berka.htm

Below is a display of `account` and `district` in an Entity-Relationship Diagram (ERD). 

![diagram](joining-data-ERD.png)

ERDs are visual representations that help understand the relationship between two or more datasets. In an ERD, each table in the diagram represents a dataset. The variables of each dataset are represented as rows under each respective table. In our case, the first column of our table is the variable's name while the second column is the variable's value type. The notations of the line connecting our two tables indicate their relationship type and is defined as "Crow's Foot Notation". To learn more about this notation, we recommend visiting this article: https://vertabelo.com/blog/crow-s-foot-notation/

There exists only two value types in the `accounts` and `district` table: "INT" and "VARCHAR". The "INT" value type indicates that the corresponding value is an integer, while "VARCHAR" represents a variable-length string that can contain various characters. These value types help SQL understand the appropriate operations that can be performed on each value. Alongside this, the second column of our tables also show if a variable is a primary key (PK) or foreign key (FK). We introduce these concepts below.

### What is a primary key and a foreign key?

In a database, a <b>primary key</b> is a unique identifier for each record in a table. For instance, our `accounts` table has the primary key of "account_id". This makes sense because every single row in the `accounts` table corresponds to "account_id" which represents one single account. The `district` table has the primary key of "District ID". This means that each row under the `district` table represents one single district (or district id). So under the `accounts` table, there should not be any rows with the same "account_id" value. Similarly, the `district` table should not have any rows with the same "district_id" value. 

A foreign key, on the other hand, establishes a relationship between two tables. It refers to the primary key of another table and helps connect the records across multiple tables. In our example, the "district_id" in the account table is a foreign key, indicating that it references the primary key of the district table. This allows us to associate each account with its corresponding district.

By using primary and foreign keys, we establish relationships between tables, enabling us to perform joins and retrieve meaningful information by linking related data together. Let's jump straight into demonstrating these joins and how primary keys and foreign keys work.

<!-- #region -->
## Install - execute this once. 
<b>Note:</b> If you are following these lessons locally and <b>not</b> on Google Colab, then there is no need to reinstall these packages.

This code installs JupySQL, DuckDB, and Pandas in your environment. We will be using these moving forward.

```{code-cell} ipython3
%pip install jupysql --upgrade duckdb-engine pandas --quiet
```

## Load the data
We extract the financial data by retrieving it from it's URL download link. The link may be a zip file (which it is in this case), so we extract the zip file and convert the .asc files to .csv files. Finally, we save converted data into a folder.

The script we call can be found under `sql/course-material/intro-to-sql/banking_data_script.py`. This script downloads and stores the necessary data into a folder within the current directory. Please reference the script for more information.

```{code-cell} ipython3
import banking_data_script

# ZIP file download link
link = "http://sorry.vse.cz/~berka/challenge/pkdd1999/data_berka.zip"
# Naming our folder that will hold our .csv files
output = "expanded_data"
banking_data_script.extract_asc_to_csv(link, output)
```

<!-- #endregion -->

If you ran the above cell, you should have a folder `expanded_data` in your current directory that contains the `.csv` files we will be using.

## Load Engine
We now load in our SQL extension that allows us to execute SQL queries in Jupyter Notebooks. 

<b>Note</b> Ensure you restart any previous notebook that has the same database name as the one initialized below.

```{code-cell} ipython3
# Loading in SQL extension
%reload_ext sql
# Initiating a DuckDB database named 'bank_data.duck.db'
%sql duckdb:///bank_data.duck.db
```

## Queries


### Creating a Schema

A schema helps define how our data is organized. Think of it as a container that holds certain datasets that relate to each other. In our `bank_data.duck.db` database, we could have several schemas, each having their own datasets that relate to each other. For now we will create one schema to hold our `accounts` and `district` dataset.

```{code-cell} ipython3
%%sql
CREATE SCHEMA s1;
CREATE TABLE s1.account AS
FROM read_csv_auto('expanded_data/account.csv', header=True, sep=',');
CREATE TABLE s1.district AS
FROM read_csv_auto('expanded_data/district.csv', header=True, sep=',');
```

Let's take a brief look at both of our tables before we get started.

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

Before we jump into joins, I highly recommend following along with <a href="https://joins.spathon.com/">this resource</a>.


### Inner Join

The most basic join is the inner join. Inner joins result in a query that returns rows where both tables have the specified key. For example, the query below inner joins our `s1.account` and `s1.district` table `ON` the "accounts_id" variable.

```{code-cell} ipython3
%%sql
SELECT *,
FROM s1.account
INNER JOIN s1.district 
    ON s1.account.district_id = s1.district.district_id
LIMIT 5
```

This query results in joining our `s1.account` and `s1.district` tables wherever the "district_id" exists in both tables. In this inner join, the "district_id" value must exist in both tables. For demonstration purposes, let's hypothetically assume that there is a row in the `s1.account` table that has a "district_id" value of 99999. We `INSERT` this value `INTO` our `s1.account` table below.

```{code-cell} ipython3
%%sql 
INSERT INTO s1.account
VALUES (9999, 99999, 'POPLATEK MESICNE', 930101)
```

Because the value 99999 does not exist under the "district_id" column in the `s1.district` table, this row from the `s1.account` will not appear in our join.

```{code-cell} ipython3
%%sql 
SELECT COUNT(*)
FROM s1.account
```

```{code-cell} ipython3
%%sql 
SELECT COUNT(*)
FROM s1.account
INNER JOIN s1.district 
    ON s1.account.district_id = s1.district.district_id
```

We see that the `COUNT(*)` of `s1.account` is 4501 and the `COUNT(*)` of our join is 4500. This is because our inner join excludes the row with an "district_id" value of 99999 from our `s1.account` table since it does not appear anywhere under the "district_id" column of our `s1.district` table.

Also notice that the "district_id_1" column in our original inner join query. This column does not inherit the "district_id" column name from our `s1.district` table because we would then have two columns with both "district_id" due to the inclusion of `s1.account`. To avoid this ambiguity, SQL automatically adds "_1" to the end of identical columns resulting from a join. If we are joining more than two tables (seen in the next section), then SQL will automatically increment the number to distinguish each identical column. 

#### Question 1 (Medium):
How many counts of each "district_id" appear in `s1.account`? Query the district_id, the respective count, and the district name. Filter the results to only have district id's with a count greater than 40.

<b>Hint:</b> Try breaking the problem down step by step. First, take a look at the results of an inner join. What can you do from there to achieve the correct results?

<!-- #region -->
<details>

<summary>Answers</summary>

We first inner join `s1.account` and `s1.district` on "district_id" to have a query that has the information necessary in answering this question. Then, we group by "district_id" and "district_name" in order to aggregate and have them in our select statement. The last filter step is through the `HAVING` clause because we filter post-aggregation.

```{code-cell} ipython3
%%sql 
SELECT s1.district.district_id, COUNT(*), s1.district.district_name
FROM s1.account
INNER JOIN s1.district 
    ON s1.account.district_id = s1.district.district_id
GROUP BY s1.district.district_id, s1.district.district_name
HAVING COUNT(*) > 40
```

</details>
<!-- #endregion -->

### Left Join

A left join guarantees that every row in the table before the `ON` clause (the left table) appears in our query, regardless if the key from that row matches the "right" table being joined.

```{code-cell} ipython3
%%sql 
SELECT COUNT(*)
FROM s1.account
LEFT JOIN s1.district 
    ON s1.account.district_id = s1.district.district_id
```

Recall the row we `INSERT` into the `s1.account` table. This row is included in our left join because `s1.account` appears before the `JOIN` clause in our SQL statement. This is why the `COUNT(*)` matches the number of rows of our `s1.account` table after we inserted the row. Let's take a look at what this row looks like after our left join.

```{code-cell} ipython3
%%sql
SELECT *
FROM s1.account
LEFT JOIN s1.district 
    ON s1.account.district_id = s1.district.district_id
WHERE s1.account.district_id = 99999
```

The first 4 columns have values, but the resulting values from the "right table" are all "None"! Since `s1.district` does not have the value 99999 under its "district_id" column, there is no information on this particular district_id to supplement the left table.

Also notice the particular syntax for our column in our `WHERE` clause. Since "district_id" appears in both `s1.account` and `s1.district`, we have to specify which table to run our `WHERE` clause on. 

### Right Join

Right join is identical to the nature of the left join. A right join will guarantee the inclusion of every row from the "right table", regardless if the key being joined on appears in the "left table."

Here we replace the `LEFT JOIN` in our last example with `RIGHT JOIN`.

```{code-cell} ipython3
%%sql 
SELECT COUNT(*)
FROM s1.account
RIGHT JOIN s1.district 
    ON s1.account.district_id = s1.district.district_id
```

The resulting `COUNT(*)` of our join omits the one row we `INSERT` into `s1.account` previously. Let's double check and see if our inserted row exists after this join.

```{code-cell} ipython3
%%sql 
SELECT *
FROM s1.account
RIGHT JOIN s1.district 
    ON s1.account.district_id = s1.district.district_id
WHERE s1.account.district_id = 99999
```

Exactly what we expect.

What would happen if we reverse the placement of our tables in our `RIGHT JOIN` clause? The results of reversing the table placements are below.

```{code-cell} ipython3
%%sql 
SELECT COUNT(*)
FROM s1.district
RIGHT JOIN s1.account 
    ON s1.account.district_id = s1.district.district_id
```

```{code-cell} ipython3
%%sql 
SELECT *
FROM s1.district
RIGHT JOIN s1.account 
    ON s1.account.district_id = s1.district.district_id
WHERE s1.account.district_id = 99999
```

We get near exact results from our previous `LEFT JOIN` demonstration. The only difference is the order of our columns in the query output. The `s1.account` table appears on the far right whil the `s1.district` table appears on the left. To ensure complete visibility of the output, please utilize the scroll bar.

#### Question 2 (Easy):
Show the maximum "account_id" value corresponding with that account's district information, regardless if there is any or not. Name the resulting query colum "max_acc_id". You must include a join.

<!-- #region -->
<details>

<summary>Answers</summary>

We first left join `s1.account` and `s1.district` on "district_id" to have a query that guarantees completed information from the `s1.account` table. Then, we find the max of "account_id" and rename it accordingly.

```{code-cell} ipython3
%%sql 
SELECT MAX(s1.account.account_id) AS max_acc_id
FROM s1.account
LEFT JOIN s1.district
    ON s1.account.district_id = s1.district.district_id
```

</details>
<!-- #endregion -->

### Full Join
Full join (also known as outer join) results in the inclusion of all rows from both tables. To showcase the full capability of full joins, we first `INSERT` another row into the `s1.district` table with a "district_id" value not present in the `s1.account` table. In other words, we are creating new value for `s1.district`'s primary key that does not appear in `s1.account`'s foreign key.

```{code-cell} ipython3
%%sql 
INSERT INTO s1.district
VALUES (3333, 'Hypothetical District', 'Hypothetical Region',1,1,1,1,1,1,1,1,1,1,1,1,1)
```

```{code-cell} ipython3
%%sql 
SELECT COUNT(*)
FROM s1.account 
FULL JOIN s1.district 
    ON s1.account.district_id = s1.district.district_id
```

```{code-cell} ipython3
%%sql 
SELECT *
FROM s1.account
FULL JOIN s1.district 
    ON s1.account.district_id = s1.district.district_id
WHERE s1.account.district_id = 99999 OR s1.district.district_id = 3333
```

The full join on `s1.district` and `s1.account` results in a query that includes all rows from both tables. The `OR` clause in the last SQL statement verifies this by querying the hypothetical rows we created in each table.

#### Question 3 (Medium):
What is the average "account_id" value for accounts in the "Prague" region? Round the average by 3 decimal places.

It doesn't really make sense to average by the "account_id" as it is an arbitrary number to uniquely identify each account. However, try to ignore that for the purpose of practice.

<!-- #region -->
<details>

<summary>Answers</summary>

We first join `s1.account` and `s1.district` on "district_id" to have a query of completed information between the two tables. Then, we `GROUP BY` region and `SELECT` the region name and the average value of "account_id" within regions. Finally, we use `HAVING` to filter where region has the value 'Prague' post grouping with `GROUP BY`.

```{code-cell} ipython3
%%sql
SELECT s1.district.region, ROUND(AVG(s1.account.account_id), 3) 
FROM s1.account
INNER JOIN s1.district
    ON s1.account.district_id = s1.district.district_id
GROUP BY s1.district.region
HAVING s1.district.region = 'Prague'
```

</details>
<!-- #endregion -->

## Wrapping Up

In this section, we learned the basic join types and how to use them when given two tables. We also learned the definiton of primary and foriegn keys along with an introduction to ERDs. To recap:

- `FULL JOIN` -  Guarantees that every row from both joined tables is included in the resulting query, regardless of whether a matching key exists in the other table or not. A `FULL JOIN` essentially combines the results of a `RIGHT JOIN` and `LEFT JOIN`

- `LEFT JOIN` - Guarantees that every row from the left table is included in the resulting query, regardless of whether a matching key exists in the other table or not. 

- `LEFT JOIN` - Guarantees that every row from the right table is included in the resulting query, regardless of whether a matching key exists in the other table or not. 

- Primary key - The column in a table that uniquely identifies each row of the table.

- Foreign key - A column in a table that establishes a link or relationship to the primary key of another table.

In the next section, you will learn how to implement joins in more than two tables.
