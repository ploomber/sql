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

# Plotting with `seaborn`

Seaborn is a library for making statistical graphics in Python. It builds on top of matplotlib and integrates closely with `pandas` data structures. It provides a high-level interface for drawing attractive and informative statistical graphics.

The plotting functions operate on dataframes and arrays containing whole datasets. Internally, they perform the necessary semantic mapping and statistical aggregation to produce informative plots.

Its dataset-oriented, declarative API lets you focus on what the different elements of your plots mean, rather than on the details of how to draw them.

For more see: https://seaborn.pydata.org/

## Install and Load Libraries

```{important}
<b>Note:</b> The `--save` and `%sqlcmd` features used require the latest JupySQL version. Ensure you run the code below to update JupySQL.
```

This code installs JupySQL, DuckDB, and Pandas in your environment. We will be using these moving forward.

```bash
%pip install jupysql pandas seaborn --quiet
```

Finally, we load in the libraries we will be using in this tutorial.

```{code-cell} ipython3
import sys
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
```

## Load the data

```{important}
<b>Note:</b> If you are following these lessons locally and <b>not</b> on Google Colab, then there is no need to load the data again.
```

This section was covered in detail in the previous tutorial: [Joining Data in SQL](https://ploomber-sql.readthedocs.io/en/latest/intro-to-sql/joining-data-in-sql.html#load-the-data). We will be using the same data in this tutorial as well.

```{code-cell} ipython3
sys.path.insert(0, "../../")
import banking  # noqa: E402

_ = banking.MarketData(
    "https://web.archive.org/web/20070214120527/http://lisp.vse.cz/pkdd99/DATA/data_berka.zip",  # noqa E501
    "expanded_data",
)

_.convert_asc_to_csv(banking.district_column_names)
```

If you run the above cell, you should have a folder `expanded_data` in your current directory that contains the `.csv` files we will be using. In this tutorial, we will be focusing on three of these files: `loan.csv`, `account.csv`, `district.csv`.

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

Delete tables and schema if they already exist.

## Creating Tables

Let's start off with loading three of the eight `.csv` files from the `expanded_data` folder in the current directory to our newly created DuckDB database. Like in the previous tutorial, we will [create a schema](https://ploomber-sql.readthedocs.io/en/latest/intro-to-sql/joining-data-in-sql.html#creating-a-schema) `b1` in which we will store the tables. Here we use the `CREATE TABLE` syntax in DuckDB to ingest four of the eight `.csv` files. The `read_csv_auto` is a function that helps SQL understand our local `.csv` file for creation into our database.

Delete tables

```{code-cell} ipython3
%%sql
DROP TABLE IF EXISTS b1.loan;
DROP TABLE IF EXISTS b1.account;
DROP TABLE IF EXISTS b1.district;
DROP SCHEMA IF EXISTS b1;
```

```{code-cell} ipython3
%%sql
CREATE SCHEMA b1;
CREATE TABLE b1.account AS
FROM read_csv_auto('expanded_data/account.csv', header=True, sep=',');
CREATE TABLE b1.district AS
FROM read_csv_auto('expanded_data/district.csv', header=True, sep=',');
CREATE TABLE b1.loan AS
FROM read_csv_auto('expanded_data/loan.csv', header=True, sep=',');
```

The code above will create three tables in the database schema: `b1.account`, `b1.district`, `b1.loan`.

## Exploring the data

Let's take a look at its entries.

```{code-cell} ipython3
%sqlcmd explore --table b1.account
```

```{code-cell} ipython3
%sqlcmd explore --table b1.district
```

```{code-cell} ipython3
%sqlcmd explore --table b1.loan
```

## Matplotlib inheritance

Seaborn is built on top of Matplotlib. Therefore, depending on the seaborn plotting command, it will return either a Matplotlib axes or figure object. If the plotting function is axes-level, a single `matplotlib.pyplot.Axes` object is returned. This object accepts an `ax=` argument, which integrates with Matplotlib's <b>object-oriented interface</b> and allows composing plots with other plots. On the other hand, if the plotting function is figure-level, a `FacetGrid` object is returned. This object, unlike the axes-level object, is more standalone, but "smart" about subplot organization. To learn about these objects in greater detail, visit seaborn's website [here](https://seaborn.pydata.org/tutorial/function_overview.html#figure-level-vs-axes-level-functions).

A few examples denoting this distinction are shown below.

### Axes-level

Suppose we want to identify whether gentrification increases the average salary of two regions, using the data we downloaded above. We first save our [CTE (Common Table Expression)](https://ploomber-sql.readthedocs.io/en/latest/advanced-querying-techniques/ctes) named `levels_example` that takes in the columns, `average_salary`, `ratio_of_urban_inhabitants`, and `region`, and filters for two regions, 'central Bohemia' and 'east Bohemia', from the `b1.district` table.

```{code-cell} ipython3
%%sql --save levels_example
SELECT average_salary, ratio_of_urban_inhabitants, region
FROM b1.district
WHERE region IN ('central Bohemia', 'east Bohemia');
```

The result of the CTE is saved as a pandas `DataFrame()`:

```{code-cell} ipython3
result = %sql SELECT * FROM levels_example
df = pd.DataFrame(result)
```

You can determine what is returned using Python's `type()` function:

```{code-cell} ipython3
plt.rcParams["figure.dpi"] = 300  # high resolution

scatter_plt = sns.scatterplot(
    data=df, x="ratio_of_urban_inhabitants", y="average_salary", hue="region"
)
print(type(scatter_plt))
plt.show()
```

Notice that the `sns.scatterplot()` function returns a Matplotlib `Axes` object, a single plot that is inclusive of the data from both regions. Other seaborn functions, including `regplot`, `boxplot`, `kdeplot`, and many others, also return Matplotlib `Axes` objects. Therefore, we can use various Matplotlib axes [commands](https://seaborn.pydata.org/generated/seaborn.axes_style.html) to modify the Seaborn figure.

### Figure-level

On the other hand, we can show that `sns.relplot()` returns a `FacetGrid` object, creating separate plots for the regions:

```{code-cell} ipython3
facet_plt = sns.relplot(
    data=df, x="ratio_of_urban_inhabitants", y="average_salary", col="region"
)
print(type(facet_plt))
plt.show()
```

Other figure-level seaborn functions include `catplot`, `displot`, `pairplot`, and `jointplot`.

```{important}
The legends are placed outside the plot if a Figure-level plotting function is used. See scatterplot section below.
```

Let's now jump into one of the most simple, yet essential, data visualizations: the bar plot.

## Barplots

The most basic [`seaborn.barplot()`](https://seaborn.pydata.org/generated/seaborn.barplot.html) function takes a categorical and a numeric variable as <b>encodings</b>. A second layer of grouping, preferably with another categorical variable, can be added to the `hue` argument.

### Example

Suppose the marketing manager wants to see a visualization for the number of <b>unique</b> loan ID's associated with each status of paying off the loan. To tackle this question, we will, first, create a CTE from the `b1.loan` table and obtain the counts for each status in different columns:

```{code-cell} ipython3
%%sql --save bar_plot_example
SELECT DISTINCT status, COUNT(loan_id) AS count_loan_id
FROM b1.loan
GROUP BY status
ORDER BY status;
```

Save the CTE as a pandas `DataFrame()`:

```{code-cell} ipython3
result = %sql SELECT * FROM bar_plot_example
df = pd.DataFrame(result)
```

Finally, use `seaborn.barplot()` to produce a bar plot:

```{code-cell} ipython3
plt.figure(figsize=(15, 5), dpi=300)  # Initialize blank canvas
sns.barplot(data=df, x="status", y="count_loan_id")
plt.xlabel("Status of Paying off Loan")
plt.ylabel("Count")
plt.title("Count of Loan ID's by Loan Status")
plt.show()
```

### Question 1 (Medium)

The marketing manager now wants you to provide the same information as the example above, but with an added grouping of the frequency of issuance of statements, which corresponds to the `frequency` variable in the `b1.account` table. Create a grouped bar plot with  clear axes labels, axes tick marks, title, and legend.

<b>Hint</b> Since the `frequency` variable is not in b1.loan`, think of which SQL operation you can employ to combine both tables. Moreover, the b1.loan` is a subset of the `b1.account` so use the appropriate technique that provides all rows from `b1.account`.

<!-- #region -->
<details>
<summary>Answers</summary>

We start off by creating a CTE from both the `b1.loan` and `b1.account` table with the help of a `LEFT JOIN` on `account_id`. The reason for choosing this join is because all `account_id`'s in `b1.loan` are present in `b1.account`, so we obtain all accounts in the database. Next, because we also want counts by `frequency`, we add it to the `GROUP BY` clause and ensure we pass `DISTINCT` in the `SELECT` clause:

```{code-cell} ipython3
%%sql --save bar_plot_question
SELECT DISTINCT status, frequency, COUNT(loan_id) AS count_loan_id
FROM b1.account
LEFT JOIN b1.loan
    ON b1.account.account_id = b1.loan.account_id
GROUP BY status, frequency
ORDER BY status;
```

Save the CTE as a pandas `DataFrame()`:

```{code-cell} ipython3
result = %sql SELECT * FROM bar_plot_question
df = pd.DataFrame(result)
```

Finally, use `seaborn.barplot()`, this time with the `hue` argument, to produce a <b>grouped bar plot</b>:

```{code-cell} ipython3
plt.figure(figsize=(15, 5), dpi=300)  # Initialize blank canvas
sns.barplot(data=df, x="status", y="count_loan_id", hue="frequency")
plt.xlabel("Status of Paying off Loan")
plt.ylabel("Count")
plt.title("Count of Loan ID's by Loan Status and Freq. of Statement Issuance")
plt.show()
```

</details>
<!-- #endregion -->

<!-- #region -->

## Scatter plots

Scatter plots help us analyze relationships between two numeric variables. In the [Matplotlib inheritance](https://ploomber-sql.readthedocs.io/en/latest/visualizing-your-sql-queries/plotting-with-seaborn.html#matplotlib-inheritance) section above, we saw examples of the `scatterplot` function, which create axes-level objects, to analyze the effect of `ratio_of_urban_inhabitants` on `average_salary` by `region`. Below, we will introduce a figure-level function `relplot`, along with some customizations, to create faceted scatter plots that help us easily visualize data from multiple tables and columns.

### Example

Let us travel back some decades for the purpose of this example! Suppose the local municipality wants to visually assess, using the bank data, their hypothesis that an increasing unemployment rate leads to clients opting for good-standing (status either "A" or "C"), short-term (<= 1 year) loans of lower amounts in the districts of south Moravia and north Moravia in the year 1996 by duration and status.

Instead of not only creating multiple sub-scatterplots manually but also filtering the joined dataset multiple times, we can do this in one line using `relplot`! The encodings (`x` and `y`), semantics (`hue`, etc.), and facet positions (`row` and `col`) are the only arguments we have to worry about when creating the faceted figure. However, before doing so, we need to get the data in order by performing `LEFT JOIN` on all the three tables and filtering by `region`, `duration`, and `status`. We shall save this table in a CTE named

```{code-cell} ipython3
%%sql --save relplot_example
SELECT status, duration, amount, region, unemployment_rate_96
FROM b1.account AS a
LEFT JOIN b1.loan AS l
ON a.account_id = l.account_id
LEFT JOIN b1.district AS d
ON d.district_id = a.district_id
WHERE region IN ('north Moravia', 'south Moravia') AND
duration <= 24 AND status IN ('A', 'C');
```

Like before, save the CTE as a pandas `DataFrame()`:

```{code-cell} ipython3
result = %sql SELECT * FROM relplot_example
df = pd.DataFrame(result)
```

In this `sns.relplot`, we we assign the `col` argument to the variable `region` and the `row` argument to the variable `status` that creates a faceted figure with multiple subplots arranged across both rows and columns of the grid:

```{code-cell} ipython3
sns.relplot(
    data=df,
    x="unemployment_rate_96",
    y="amount",
    hue="duration",
    col="region",
    row="status",
    height=3,
    aspect=1.5,
)
plt.show()
```

This visualization should definitely help the local municipality obtain a first glance of their hypothesis! Upon eyeballing it, we do not see any apparent correlation of unemployment rate with the loan amount, but we can see that higher duration loans lead to higher amounts. Therefore, using faceted plots, we can accelerate our EDA process and focus on important relationships in the data.

However, there are still some problems with this plot. The axes labels and legend title are not descriptive enough and the plot lacks a title. We can customize `FacetGrid` figures by using Matplotlib figure-level functions that affect all facets to reduce duplication of labels. See the functions below and consult the [`FacetGrid` documentation](https://seaborn.pydata.org/generated/seaborn.FacetGrid.html) and [Matplotlib documentation](https://matplotlib.org/stable/gallery/subplots_axes_and_figures/) to know more:

```{code-cell} ipython3
g = sns.relplot(
    data=df,
    x="unemployment_rate_96",
    y="amount",
    hue="duration",
    col="region",
    row="status",
    facet_kws={"margin_titles": True},
    height=4,
    aspect=1,
)

g.set(xlabel=None, ylabel=None)  # remove duplicate x and y axis labels
g.set_titles(  # facet titles
    row_template="Status: {row_name}", col_template="{col_name}"
)

g._legend.set_title("Duration (months)")
g.legend.set_bbox_to_anchor((1.25, 0.5))  # Shift legend to the right

g.fig.suptitle(  # main title of the figure
    "Unemployment Rate vs Loan Amount by Loan", x=0.235, fontsize=12
)
g.fig.text(  # subtitle of the figure
    0.235,
    0.95,
    "Data subsetted on Region and Status",
    ha="right",
    va="top",
    fontsize=10,
)

g.fig.supylabel("Loan Amount ($)")  # y-axis label for all facets
g.fig.supxlabel("Unemployment Rate (%)")  # x-axis label for all facets
g.fig.subplots_adjust(top=0.9)  # adjust the Figure position

plt.show(g)
```

If we wanted to access individual facets of the plot, we could use axes-level methods. For example, `g.axes[0,0].set_xlabel('axes label 1')` will set the x-axis label of the first quadrant facet and `g.axes[0,1].set_xlabel('axes label 2')` will set the x-axis label of the facet row-adjacent to the first quadrant facet and so on.

Consult the previously linked docs and the [documentation](https://seaborn.pydata.org/generated/seaborn.relplot.html) of `relplot` to answer the question below!

### Question 2 (Hard)

Suppose that the local municipality now comes back to ask for a similar plot, but with all loan durations included. Their feedback on the previous graph was that they would only like to see two facets or subplots at max for readability. Your job is to modify the CTE from the above example to produce a `relplot` figure that incorporates the <b>same encodings</b> but <b>additional visual semantics</b>, including `style` for `region`, `size` for `duration`, and subplots by `status`. Make sure to use a blue-red color palette for the subplots and customize axes labels for clarity.

<b>Hint</b> Try to find an example that does exactly what the question asks in the [documentation](https://seaborn.pydata.org/generated/seaborn.relplot.html)

<!-- #region -->
<details>

<summary>Answers</summary>

We first modify the `relplot_example` CTE by removing the filter for `duration`:

```{code-cell} ipython3
%%sql --save relplot_question
SELECT status, duration, amount, region, unemployment_rate_96
FROM b1.account AS a
LEFT JOIN b1.loan AS l
ON a.account_id = l.account_id
LEFT JOIN b1.district AS d
ON d.district_id = a.district_id
WHERE region IN ('north Moravia', 'south Moravia') AND
status IN ('A', 'C');
```

Save the CTE as a pandas `DataFrame()`:

```{code-cell} ipython3
result = %sql SELECT * FROM relplot_question
df = pd.DataFrame(result)
```

Finally, `sns.relplot` is called and stored in a variable for customizing the x-axis label. Note that the `sizes` argument specifies magnitude of the point `size`, which is used to control the visibility of the points:

```{code-cell} ipython3
g = sns.relplot(
    data=df,
    x="unemployment_rate_96",
    y="amount",
    size="duration",
    style="region",
    hue="status",
    col="status",
    palette=["b", "r"],
    sizes=(10, 100),
)
g.set(xlabel=None, ylabel="Loan Amount ($)")  # remove duplicate x axis label
g.fig.supxlabel("Unemployment Rate (%)")  # x-axis label for whole figure
plt.show(g)
```

</details>
<!-- #endregion -->

## Density plots

A kernel density estimate (KDE) plot is a method for visualizing the distribution of observations in a dataset, analogous to a histogram. KDE represents the data using a continuous probability density curve in one or more dimensions. Relative to a histogram, KDE can produce a plot that is less cluttered and more interpretable, especially when drawing multiple distributions.

```{important}
The bandwidth, or standard deviation of the smoothing kernel, is an important parameter. Misspecification of the bandwidth can produce a distorted representation of the data.
```

### Example

Seaborn's [`kdeplot` <b>axes-level function</b>](https://seaborn.pydata.org/generated/seaborn.kdeplot.html) can help us easily visualize KDE's of multiple numeric variables. Its figure-level equivalent is the [`displot` function](https://seaborn.pydata.org/generated/seaborn.displot.html#seaborn.displot) with which we can produce KDE plots by specifying `kind="kde"`.

Suppose the finance manager wants a visual representation of two distributions, the loan `amount` by loan `status` and loan `amount` by loan `duration`. We can easily produce a `kdeplot` to not only draw multiple distributions in a single plot but also create axes subplots. Before this, we first produce a CTE with the two variables and save it as a pandas `DataFrame()`:

```{code-cell} ipython3
%%sql --save kde_example
SELECT amount, status, payments, duration
FROM b1.loan
ORDER BY status;
```

```{code-cell} ipython3
result = %sql SELECT * FROM kde_example
df = pd.DataFrame(result)
```

```{code-cell} ipython3
plt.figure(figsize=(10, 3), dpi=300)  # Initialize blank canvas

plt.subplot(1, 2, 1)  # first quadrant
sns.kdeplot(data=df, x="amount", hue="status")
plt.title("KDE of Loan Amount ($) by Loan Status")  # Set title
plt.xlabel("Loan Amount ($)")  # Set x-axis label

plt.subplot(1, 2, 2)  # second quadrant
sns.kdeplot(data=df, x="amount", hue="duration")
plt.title("KDE of Loan Amount ($) by Loan Duration (months)")  # Set title
plt.xlabel("Loan Amount ($)")  # Set x-axis label
plt.show()
```

### Question 3 (Easy)

Similar to the way we customized our figure-level plots for the previous section, we can do the same for axes-level plots too! Your task is to remove the duplicate axes labels and rename the legend titles to provide a cleaner, publication-level visualization. For loan `duration`, provide the units in years rather than months.

<b>Hint</b> Consult Matplotlib's axes class [documentation](https://matplotlib.org/stable/api/axes_api.html) to find the right functions!

<!-- #region -->
<details>

<summary>Answers</summary>

We do not need to make a new CTE and can jump straight into programming with seaborn. Since we are using the same plot as the example, copy pasting the code and building on top of it is a nice idea. Instead of using multiple `plt.subplot()` functions, we initialize the whole figure with `fig` and the individual axes, in this case only two (`ax1` and `ax2`), with `plt.subplots(1, 2, ...)`. The first and second plots are customized with their respective axes objects and the functions from `matplotlib.axes` class:

```{code-cell} ipython3
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4), sharex=True, sharey=True)

sns.kdeplot(data=df, x="amount", hue="status", ax=ax1)
ax1.set_title("KDE of Loan Amount ($) by Loan Status")
ax1.set_xlabel("")  # Remove x-axis label
ax1.legend(["A", "B", "C", "D"], title="Loan Status")

sns.kdeplot(data=df, x="amount", hue="duration", ax=ax2)
ax2.set_title("KDE of Loan Amount ($) by Loan Duration (years)")
ax2.set_xlabel("")  # Remove x-axis label
ax2.legend(["1", "2", "3", "4", "5"], title="Loan Duration (years)")

fig.supxlabel("Loan Amount ($)")  # x-axis label for whole figure

plt.show()
```

</details>
<!-- #endregion -->

The plot above is cleaner, with less overplotting, and has the correct units across all labels. It is worth taking the extra time to produce good quality visualizations, especially for assignment or paper/conference submissions.

## Box and whisker plot

A box and whisker plot (box plot for short) displays the five-number summary of a set of data. The five-number summary is the minimum, first quartile, median, third quartile, and maximum. In a box plot, we draw a box from the first quartile (25th percentile) to the third quartile (75th percentile). A vertical line goes through the box at the median, which is also the 50th percentile.

In seaborn, `boxplot` is an Axes-level function and has the same object-oriented functionality as the `kdeplot`. There are several visual variations of boxplots in seaborn, such as the `violinplot`, `swarmplot` or `stripplot`, and `boxenplot`. All of these functions are also at the axes-level.

### Example

Suppose the finance manager wants boxplots of the moving-average of loan `amount`, rounded to 0 decimals, for every three dates preceding and every two dates following the current date of a record. These amounts should be displayed with the the loan's `duration`. If we recall, we saw this example in the Advanced Aggregations [section](https://ploomber-sql.readthedocs.io/en/latest/advanced-querying-techniques/advanced-aggregations.html#question-2-hard).

Let us create the CTE and turn it into a pandas `Dataframe()` first:

```{code-cell} ipython3
%%sql --save boxplot_example
SELECT date, duration, ROUND(avg_amount, 0) AS avg_amount
FROM (SELECT date, duration, AVG(amount) OVER (ORDER BY date ROWS BETWEEN 3 PRECEDING AND 2 FOLLOWING) AS avg_amount FROM b1.loan)
ORDER BY date;
```

```{code-cell} ipython3
result = %sql SELECT * FROM boxplot_example
df = pd.DataFrame(result)
```

```{code-cell} ipython3
plt.figure(figsize=(15, 5), dpi=300)  # Initialize blank canvas
sns.boxplot(data=df, x="duration", y="avg_amount")
plt.ylabel("Moving-Average Loan Amount ($)")
plt.xlabel("Loan Duration (months)")
plt.show()
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
FROM (SELECT date, duration, status, AVG(amount) OVER (PARTITION BY status ORDER BY date ROWS BETWEEN CURRENT ROW AND 5 FOLLOWING) AS avg_amount FROM b1.loan)
ORDER BY date;
```

```{code-cell} ipython3
result = %sql SELECT * FROM boxplot_question
df = pd.DataFrame(result)
```

Unlike the previous section in which we employed the `matplotlib.axes` functions to customize the plot, we use the simpler `matplotlib.pyplot` functions because we have not faceted the boxplot:

```{code-cell} ipython3
plt.figure(figsize=(15, 5), dpi=300)  # Initialize blank canvas
sns.boxplot(data=df, x="duration", y="avg_amount", hue="status")
plt.ylabel("Moving-Average Loan Amount ($)")
plt.xlabel("Loan Duration (years)")
plt.xticks([0, 1, 2, 3, 4], ["1", "2", "3", "4", "5"])
plt.legend(title="Loan Status")
plt.show()
```

</details>
<!-- #endregion -->

+++

## Wrapping Up

In this section, we learned about plotting four types of visualizations with seaborn. To summarize:

- Axes-level functions plot onto a single subplot that may or may not exist at the time the function is called

- Figure-level functions internally create a matplotlib figure, potentially including multiple subplots

- `seaborn.barplot`, an axes-level function, should be used for visualizing count data

- `seaborn.scatterplot`, an axes-level function, helps visualize correlations between two numeric variables, subsetted on categorical variables if needed. `seaborn.relplot` is a figure-level function that that combines `scatterplot`with a FacetGrid and can expedite the EDA process when combining multiple types of columns into a single visualization

- `seaborn.kdeplot`, an axes-level function, creates a Kernel Density Estimate plot, analogous to a histogram. KDE represents the data using a continuous probability density curve in one or more dimensions. The function can also account for categorical levels. Its figure-level alternative is `seaborn.distplot`

- `seaborn.boxplot` is useful for visualizing the summary distribution of numeric variables, grouped by none, one, or multiple catgeorical variables. Several variations of the boxplot are provided by seaborn

In the next section, you will learn how to plot similar visualizations using the `plotly` python library.

## References

API reference - seaborn 0.12.2 documentation. (n.d.). https://seaborn.pydata.org/api.html

API Reference - Matplotlib 3.7.1 documentation. (n.d.). https://matplotlib.org/stable/api/index
