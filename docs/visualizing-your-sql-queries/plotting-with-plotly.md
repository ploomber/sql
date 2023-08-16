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

# Plotting with `plotly`

Plotly is a visualization library specifically designed for dynamic interactive plots. The library offers several additional effects to visualizations, such as zooming, panning, and hovering effects. This library is especially known for being easily deployed with web applications.

For more on plotly, visit: https://plotly.com/python/

Let's see how we can apply plotly to our familiar bank marketing data sets.

## Install - execute this once.

```{important}
<b>Note:</b> The `--save` and `%sqlcmd` features used require the latest JupySQL version. Ensure you run the code below to update JupySQL.
```

This code installs JupySQL, DuckDB, and Pandas in your environment. We will be using these moving forward.

```{code-cell} ipython3
%pip install jupysql pandas plotly --quiet
```

## Load the data

```{important}
<b>Note:</b> If you are following these lessons locally and <b>not</b> on Google Colab, then there is no need to load the data again.
```

This section was covered in detail in the previous tutorial: [Joining Data in SQL](https://ploomber-sql.readthedocs.io/en/latest/intro-to-sql/joining-data-in-sql.html#load-the-data). We will be using the same data in this tutorial as well.

```{code-cell} ipython3
import sys
import plotly.express as px
import pandas as pd

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

Let's take a look at each table.

```{code-cell} ipython3
%sqlcmd explore --table s1.account
```

```{code-cell} ipython3
%sqlcmd explore --table s1.district
```

```{code-cell} ipython3
%sqlcmd explore --table s1.loan
```

## Bar Plots

Let's create a bar plot in `plotly` using the `s1.district` table. This plot will visualize the count of each `region` in the data set.

First, let's query the count of each region in SQL.

```{code-cell} ipython3
%%sql --save region_count
SELECT region, COUNT(*) as count
FROM s1.district
GROUP BY region
ORDER BY count DESC
```

Then, let's save the CTE as a Pandas DataFrame.

```{code-cell} ipython3
query = %sql SELECT * FROM region_count
region_count_df = pd.DataFrame(query)
region_count_df
```

We can now plot the count of each `region` with this Pandas DataFrame.

```{code-cell} ipython3
fig = px.bar(
    region_count_df,
    x="region",
    y="count",
    title="Region Count",
    color_discrete_sequence=["#7d26cd"],
)
fig.show()
```

Notice how the `plotly` outputs a plot that looks noticeably different than `matplotlib` or `seaborn` outputs. Try interacting around with the plot by hovering, zooming, and panning! Double click the plot to autoscale the plot.

There are three core arguments that are applied above: the Pandas DataFrame, the x variable, and the y variable. We also set the title and color of the bars to purple by providing the `title` and `color_discrete_sequence` arguments with values.

### Question 1 (Hard):

Your boss wants you to create a bar plot showing the average loan amount for each region. Your boss also specified that they want to you to also incorporate the average salary of each region as well.

<b>Hint</b>: The `color` variable that you learned in the `seaborn` section is also usable in `plotly`. You will also most likely have to use a CTE to solve this question.

<!-- #region -->
<details>

<summary>Answers</summary>

We first need to join the `s1.district`, `s1.loan`, and `s1.account` tables in order to have the necessary information to solve this problem.

```{code-cell} ipython3
%%sql --save average_loan_per_district
SELECT d.district_id,
       d.region,
       d.average_salary,
       ROUND(AVG(l.amount),2) AS avg_loan_amount
FROM s1.district d
JOIN s1.account a 
     ON d.district_id = a.district_id
JOIN s1.loan l 
     ON a.account_id = l.account_id
GROUP BY d.district_id,
         d.region, 
         d.average_salary
ORDER BY avg_loan_amount DESC
```

This resulting CTE give us the average salary of each district. This is because `district_id` was the primary key for the `s1.district` table. However, we are now able to `GROUP BY` each `region` and average the averages for the desired output.

```{code-cell} ipython3
%%sql --save average_loan_per_region
SELECT region, ROUND(AVG(average_salary),2) AS average_salary, 
       ROUND(AVG(avg_loan_amount),2) AS average_loan_amount
FROM average_loan_per_district
GROUP BY region
```

Now, convert the `average_loan_per_region` table to a Pandas DataFrame.

```{code-cell} ipython3
average_loan_per_region = %sql SELECT * FROM average_loan_per_region
avg_loans_df = pd.DataFrame(average_loan_per_region)
avg_loans_df
```

And finally output the bar plot with `plotly`.

```{code-cell} ipython3
fig = px.bar(
    avg_loans_df,
    x="region",
    y="average_loan_amount",
    color="average_salary",
    labels={
        "total_loan_amount": "Total Loan Amount",
        "district_name": "District Name",
        "average_salary": "Average Salary",
    },
    title="Total Loan Amount by District with Average Salary color scale",
)

fig.show()
```

</details>
<!-- #endregion -->

## Scatter Plots

Let's now demonstrate a scatter plot in `plotly` by also using the `s1.district` table. This plot will visualize the relationship between the `average_salary` of a district with the unemployment rate in 1996. The plot also provides another dimension of visualization by incorporating the `ratio_of_urban_inhabitants` variable in size and color.

First, let's load our data into a Pandas DataFrame.

```{code-cell} ipython3
district = %sql SELECT * FROM s1.district
district_df = pd.DataFrame(district)
```

We can now plot the Pandas DataFrame using `plotly`.

```{code-cell} ipython3
fig = px.scatter(
    district_df,
    x="no_of_inhabitants",
    y="no_of_cities",
    color="ratio_of_urban_inhabitants",
    size="ratio_of_urban_inhabitants",
    labels={
        "no_of_cities": "Number of Cities",
        "no_of_inhabitants": "Number of Inhabitants",
    },
    title="Number of Cities by Number of Inhabitants",
    color_continuous_scale="Viridis",
)
fig.show()
```

Here we renamed the axis titles with the `labels` argument and changed the color scale with the `color_continuous_scale` argument to make the plot more visually appealing. 

### Question 2 (Medium):

Your boss didn't quite like the bar plot you've made. They've asked you to now instead create an interactive scatter plot showing the relationship between the `average_loan_amount` and `average_salary` by district.

<b>Hint</b>: Is there a way to reuse our work from question 1?

<!-- #region -->
<details>

<summary>Answers</summary>

We can reuse the `average_loan_per_district` table we created with CTEs from the last question.

```{code-cell} ipython3
df = %sql SELECT * FROM average_loan_per_district
avg_loans_df = pd.DataFrame(df)
avg_loans_df
```

```{code-cell} ipython3
fig = px.scatter(
    avg_loans_df,
    x="average_salary",
    y="avg_loan_amount",
    title="Average Loan Amount vs Average Salary per District",
)
fig.show()
```

</details>
<!-- #endregion -->

## Histograms

Histograms are similar to bar plots. The only difference is that the x-axis should be a numerical feature rather than a categorical one. We demonstrate a `plotly` histogram below.

```{code-cell} ipython3
loans = %sql SELECT amount FROM s1.loan
loans_df = pd.DataFrame(loans)
loans_df
```

```{code-cell} ipython3
fig = px.histogram(loans_df, x="amount", nbins=20, title="Loan Amounts")
fig.show()
```

Above we use a histogram to visualize the distribution of loan amounts. Try adjusting the `nbins` argument to see how it influences the plot.

### Question 3 (Easy):

A colleague asks you for a visualization of the distribution of loan amounts for loans with an 'A' or 'D' status.

<!-- #region -->
<details>

<summary>Answers</summary>

Try clicking the boxes next to "A" and "D" under the "status" legend symbol to see a useful `plotly` feature.

```{code-cell} ipython3
%%sql --save loan_status
SELECT *
FROM s1.loan
WHERE status = 'A' or status = 'D'
```

```{code-cell} ipython3
loan_status_table = %sql SELECT * FROM loan_status
loan_status_df = pd.DataFrame(loan_status_table)
loan_status_df
```

```{code-cell} ipython3
fig = px.histogram(
    loan_status_df,
    x="amount",
    color="status",
    nbins=25,
    title="'A' and 'D' Loan Amounts",
)
fig.show()
```

</details>
<!-- #endregion -->


## Box and Whiskers

When you interact with `Plotly` box plots by hovering over them, they provide a wealth of information. For example, take a look of this box plot displaying the distribution of a loan's `amount` with each distinct loan `status`.

```{code-cell} ipython3
loans = %sql SELECT * FROM s1.loan
loans_df = pd.DataFrame(loans)

category_order = ["A", "B", "C", "D"]

fig = px.box(
    loans_df,
    x="status",
    y="amount",
    color="status",
    category_orders={"status": category_order},
    title="Distribution of Loan Status By Amount",
)

fig.show()
```

The `category_orders` argument is just to have the boxes be in alphabetical order.

Hovering over each box plot displays additional information on the respective loan status. You can also check and uncheck the boxes under the "status" legend to adjust the plot.

### Question 4 (Easy):

A colleague asks you for a box plot displaying the relationship of loan duration by loan status.

<!-- #region -->
<details>

<summary>Answers</summary>

```{code-cell} ipython3
%%sql --save loan_duration
SELECT
    l.status,
    l.duration AS loan_duration
FROM
    s1.loan l
```

```{code-cell} ipython3
loan_duration = %sql SELECT * FROM loan_duration
loan_duration_df = pd.DataFrame(loan_duration)
```

```{code-cell} ipython3
category_order = ["A", "B", "C", "D"]


fig = px.box(
    loan_duration_df,
    x="status",
    y="loan_duration",
    color="status",
    category_orders={"status": category_order},
    labels={"status": "Loan Status", "loan_duration": "Loan Duration"},
    title="Distribution of Loan Durations by Loan Status",
)

fig.show()
```

</details>
<!-- #endregion -->

Delete tables

```{code-cell} ipython3
%%sql
DROP TABLE IF EXISTS s1.loan;
DROP TABLE IF EXISTS s1.account;
DROP TABLE IF EXISTS s1.district;
DROP SCHEMA s1;
```

## Wrapping Up

In this section, you learned how to create interactive displays with `plotly`. The syntax for `seaborn` and `plotly` is quite similar, allowing for a seamless transition between the two libraries.

In the next section, you'll learn how to visualize your SQL queries with `ggplot`!

## References

Plotly 5.15.0 documentation https://plotly.com/python/