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

# Plotting with `ggplot`

Before we dive into how you can use JupySQL's `ggplot` API, we will quickly go over JupySQL's [`%sqlplot` magic command](https://jupysql.ploomber.io/en/latest/api/magic-plot.html) to make you comfortable with the general overlapping notation.

+++

## Install - execute this once.

```{important}
<b>Note:</b> The `--save` and `%sqlcmd` features used require the latest JupySQL version. Ensure you run the code below to update JupySQL.
```

This code installs JupySQL, DuckDB, Matplotlib (required dependency), and ipywidgets in your environment. We will be using these moving forward.

```{code-cell} ipython3
%pip install jupysql --upgrade duckdb-engine matplotlib ipywidgets --quiet
```

## Load the data

```{important}
<b>Note:</b> If you are following these lessons locally and <b>not</b> on Google Colab, then there is no need to load the data again.
```

This section was covered in detail in the previous tutorial: [Joining Data in SQL](https://ploomber-sql.readthedocs.io/en/latest/intro-to-sql/joining-data-in-sql.html#load-the-data). We will be using the same data in this tutorial as well.

```{code-cell} ipython3
:tags: [hide-output]

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
%load_ext sql
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

## `%sqlplot`

The `%sqlplot` magic command is the easiest JupySQL plotting command to learn. Currently, it supports four different types of visualizations, including `boxplot`, `histogram`, `bar`plot, and `pie`chart. All `%sqlplot` visualizations return customizable [`matplotlib.Axes` objects](https://ploomber-sql.readthedocs.io/en/latest/visualizing-your-sql-queries/plotting-with-seaborn.html#axes-level) and have three magic commands in common:

- `--table/-t` Table to use

- `--column/-c` Column(s) to plot. <b>Note</b> only `boxplot` and `histogram` can accept multiple columns

- `--with/-w` Use a previously saved query (CTE) as input data

There are other magic commands unique to the aforementioned visualizations as well. Let us learn from a few examples below.

### Examples

1. Suppose the finance manager wants to visualize boxplots of `average_salary` and loan `payments` in a single graph. We will, first, join all three tables to obtain the relevant data, save the output as a CTE, and use that CTE for `%sqlplot boxplot`:

```{code-cell} ipython3
%%sql --save sqlplot_boxplot_example
SELECT payments, average_salary
FROM s1.account AS a
LEFT JOIN s1.loan AS l
ON a.account_id = l.account_id
LEFT JOIN s1.district AS d
ON d.district_id = a.district_id
```

```{code-cell} ipython3
import matplotlib.pyplot as plt  # noqa: E402

plt.rcParams["figure.dpi"] = 300  # high resolution
plt.rcParams["figure.figsize"] = (12, 4)

%sqlplot boxplot --table sqlplot_boxplot_example --column payments average_salary
```

Several attributes of the plot can be customized because it is a `matplotlib.Axes` object. Below is a customized, cleaner version of the above plot:

```{code-cell} ipython3
ax = %sqlplot boxplot --table sqlplot_boxplot_example --column payments average_salary --orient h
ax.set_title("Boxplot of Loan Payments and Average Salary ($)")
ax.set_xlabel("Amount ($)")
```

2. Suppose the manager wants to get a closer look of both distributions, loan `payments` and `average_salary`. You can quickly produce a histogram by using the saved CTE:

```{code-cell} ipython3
ax = %sqlplot histogram --table sqlplot_boxplot_example --column payments average_salary --bins 25
ax.set_title("Histogram of Loan Payments and Average Salary ($)")
ax.set_xlabel("Amount ($)")
```

### Question 1 (Easy)

+++

The finance manager is impressed with how quickly you produced these plots! He wants another easy deliverable: facet the multiple column boxplot and histogram in a single graph. Make sure to customize the plot with clear axes labels and titles!

<b>Hint</b> Recall the seaborn [tutorial](https://ploomber-sql.readthedocs.io/en/latest/visualizing-your-sql-queries/plotting-with-seaborn.html#id2) of how to add/position multiple matplotlib axes subplots.

<!-- #region -->
<details>
<summary>Answers</summary>

We can use the same CTE from the example above as well as `%sqlplot` functions for the individual visualizations. The only change is that we employ `plt.subplots()` for each `%sqlplot` call and use base matplotlib functions for customizing labels:

```{code-cell} ipython3
plt.figure(figsize=(12, 3), dpi=300)  # Initialize blank canvas

plt.subplot(1, 2, 1)  # first quadrant
%sqlplot boxplot --table sqlplot_boxplot_example --column payments average_salary --orient h
plt.title("Boxplot of Loan Payments and Average Salary ($)")  # Set title
plt.xlabel("Loan Amount ($)")  # Set x-axis label

plt.subplot(1, 2, 2)  # second quadrant
%sqlplot histogram --table sqlplot_boxplot_example --column payments average_salary --bins 25
plt.title("Histogram of Loan Payments and Average Salary ($)")  # Set title
plt.xlabel("Loan Amount ($)")  # Set x-axis label
```

</details>
<!-- #endregion -->

<!-- #region -->

```{important}
Initializing the whole figure with `fig` and assigning individual axes with `ax1` and `ax2`, [like in this example](https://ploomber-sql.readthedocs.io/en/latest/visualizing-your-sql-queries/plotting-with-seaborn.html#question-3-easy), would not work.
```

## `ggplot` API

You might be wondering "how can ggplot, the R package, function in Jupyter Notebooks?". Do not worry! In this tutorial, we will be learning about JupySQL's `ggplot` API to visualize our SQL queries. This plotting technique will be useful for avid R programmers, who are familiar with `ggplot2`, and for first-time learners.

The `ggplot` API is built on top of `matplotlib` and is structured around the principles of the Grammar of Graphics, allowing you to build any graph using the same `ggplot2` components: a data set, a coordinate system, and geoms (geometric objects). However, to make the API suitable for JupySQL, we <b>input a SQL table name, instead of a dataset</b>. Therefore, the same [workflow](https://ploomber-sql.readthedocs.io/en/latest/visualizing-your-sql-queries/plotting-with-seaborn.html#barplots) of creating our CTE, which was employed in the `seaborn` tutorial, will be in action here as well (no need to convert the CTE into a pandas `DataFrame()`).

<b>Note</b> at this point, JupySQL's `ggplot` API supports:

Aes:

- `x` - a SQL column mapping

- `color` and `fill` to apply edgecolor and fill colors to plot shapes

Geoms:

- `geom_boxplot` similar to `%sqlplot boxplot`

- `geom_histogram` similar to `%sqlplot histogram`

Facet:

- `facet_wrap` to display multiple plots in a single layout

### `geom_boxplot`

### Question 2 (Medium)

### `geom_histogram`

### Question 3 (Medium)

### `facet_wrap`

### Question 4 (Hard)

## Interactive `ggplot`

### Question 5 (Hard)

```{code-cell} ipython3

```

```{code-cell} ipython3

```

```{code-cell} ipython3

```

```{code-cell} ipython3

```

```{code-cell} ipython3

```

## Box and whisker plot

A box and whisker plot (box plot for short) displays the five-number summary of a set of data. The five-number summary is the minimum, first quartile, median, third quartile, and maximum. In a box plot, we draw a box from the first quartile (25th percentile) to the third quartile (75th percentile). A vertical line goes through the box at the median, which is also the 50th percentile.

In seaborn, `boxplot` is an Axes-level function and has the same object-oriented functionality as the `kdeplot`. There are several visual variations of boxplots in seaborn, such as the `violinplot`, `swarmplot` or `stripplot`, and `boxenplot`. All of these functions are also at the Axes-level.

### Example

Suppose the finance manager wants boxplots of the moving-average of loan `amount`, rounded to 0 decimals, for every three dates preceding and every two dates following the current date of a record. These amounts should be displayed with the the loan's `duration`. If we recall, we saw this example in the Advanced Aggregations [section](https://ploomber-sql.readthedocs.io/en/latest/advanced-querying-techniques/advanced-aggregations.html#question-2-hard).

Let us create the CTE and turn it into a pandas `Dataframe()` first:

```{code-cell} ipython3
%%sql --save boxplot_example
SELECT date, duration, ROUND(avg_amount, 0) AS avg_amount
FROM (SELECT date, duration, AVG(amount) OVER (ORDER BY date ROWS BETWEEN 3 PRECEDING AND 2 FOLLOWING) AS avg_amount FROM s1.loan)
ORDER BY date;
```

```{code-cell} ipython3
result = %sql SELECT * FROM boxplot_example
df = result.DataFrame()
```

```{code-cell} ipython3
plt.figure(figsize=(15, 5), dpi=300)  # Initialize blank canvas
sns.boxplot(data=df, x="duration", y="avg_amount")
plt.ylabel("Moving-Average Loan Amount ($)")
plt.xlabel("Loan Duration (months)")
```

### Question 4 (Medium)

The manager comes back and asks for another grouping layer, loan `status`, on top of the boxplot in the example. The idea should remain the same, but this time calculate the moving-average of loan `amount` for every five dates following the current date of a record. Also, output the loan `duration` in years rather than months and rename the legend title to "Loan Status".

<b>Hint</b> Recall the clause used to group the data when using windowing queries. Also, use [`matplotlib.pyplot`](https://matplotlib.org/stable/api/pyplot_summary.html) functions to quickly and easily customize the plot.

<!-- #region -->
<details>

<summary>Answers</summary>

The additional clause in the CTE is `PARTITION BY`, which adds the additional grouping by `status`. The windowing frame is also changed to incorporate five rows ahead of the current row:

```{code-cell} ipython3
%%sql --save boxplot_question
SELECT date, duration, status, ROUND(avg_amount, 0) AS avg_amount
FROM (SELECT date, duration, status, AVG(amount) OVER (PARTITION BY status ORDER BY date ROWS BETWEEN CURRENT ROW AND 5 FOLLOWING) AS avg_amount FROM s1.loan)
ORDER BY date;
```

```{code-cell} ipython3
result = %sql SELECT * FROM boxplot_question
df = result.DataFrame()
```

Unlike the previous section in which we employed the `matplotlib.axes` functions to customize the plot, we use the simpler `matplotlib.pyplot` functions because we have not faceted the boxplot:

```{code-cell} ipython3
plt.figure(figsize=(15, 5), dpi=300)  # Initialize blank canvas
sns.boxplot(data=df, x="duration", y="avg_amount", hue="status")
plt.ylabel("Moving-Average Loan Amount ($)")
plt.xlabel("Loan Duration (years)")
plt.xticks([0, 1, 2, 3, 4], ["1", "2", "3", "4", "5"])
plt.legend(title="Loan Status")
```

</details>
<!-- #endregion -->

+++

## Wrapping Up

In this section, we learned about plotting four types of visualizations with seaborn. To summarize:

- `geom_boxplot` is useful for visualizing the summary distribution of numeric variables, grouped by none, one, or multiple catgeorical variables. Several variations of the boxplot are provided by seaborn

- `geom_histogram` is useful for visualizing the summary distribution of numeric variables, grouped by none, one, or multiple catgeorical variables. Several variations of the boxplot are provided by seaborn

This ends the Visualizing Your Queries module! We hope

## References
