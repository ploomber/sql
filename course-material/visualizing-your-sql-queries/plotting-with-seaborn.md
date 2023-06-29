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

Seaborn is a library for making statistical graphics in Python. It builds on top of matplotlib and integrates closely with pandas data structures. It provides a high-level interface for drawing attractive and informative statistical graphics.

Its plotting functions operate on dataframes and arrays containing whole datasets and internally perform the necessary semantic mapping and statistical aggregation to produce informative plots.

Its dataset-oriented, declarative API lets you focus on what the different elements of your plots mean, rather than on the details of how to draw them.

For more see: https://seaborn.pydata.org/

## Install - execute this once.

```{important}
<b>Note:</b> The `--save` and `%sqlcmd` features used require the latest JupySQL version. Ensure you run the code below to update JupySQL.
```

This code installs JupySQL, DuckDB, and Pandas in your environment. We will be using these moving forward.

```{code-cell} ipython3
%pip install jupysql --upgrade duckdb-engine pandas seaborn --quiet
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

## Matplotlib inheritance

Seaborn is built on top of Matplotlib. Therefore, depending on the seaborn plotting command, it will return either a Matplotlib axes or figure object. If the plotting function is axes-level, a single `matplotlib.pyplot.Axes` object is returned. This object accepts an `ax=` argument, which integrates with Matplotlib's <b>object-oriented interface</b> and allows composing plots with other plots. On the other hand, if the plotting function is figure-level, a `FacetGrid` object is returned. This object, unlike the axes-level object, is more standalone, but "smart" about subplot organization. To learn about these objects in greater detail, visit seaborn's website [here](https://seaborn.pydata.org/tutorial/function_overview.html#figure-level-vs-axes-level-functions). 

A few examples denoting this distinction are shown below.

### Axes-level

Suppose we want to identify whether gentrification increases the average salary of two regions, using the data we downloaded above. We first save our CTE named `levels_example` that takes in the columns, `average_salary`, `ratio_of_urban_inhabitants`, and `region`, and filters for two regions, 'central Bohemia' and 'east Bohemia', from the `s1.district` table. 

```{code-cell} ipython3
%%sql --save levels_example
SELECT average_salary, ratio_of_urban_inhabitants, region
FROM s1.district
WHERE region IN ('central Bohemia', 'east Bohemia');
```

The result of the CTE is saved as a pandas dataframe:

```{code-cell} ipython3
result = %sql SELECT * FROM levels_example
df = result.DataFrame()
```

You can determine what is returned using Python's `type()` function:

```{code-cell} ipython3
import seaborn as sns
import matplotlib.pyplot as plt

scatter_plt=sns.scatterplot(data=df, x="ratio_of_urban_inhabitants", y="average_salary", hue="region")
print(type(scatter_plt))
```

Notice that the `sns.scatterplot()` function returns a Matplotlib `Axes` object, a single plot that is inclusive of the data from both regions. Other seaborn functions, including `regplot`, `boxplot`, `kdeplot`, and many others, also return Matplotlib `Axes` objects. Therefore, we can use various Matplotlib axes [commands](https://seaborn.pydata.org/generated/seaborn.axes_style.html) to modify the Seaborn figure.

### Figure-level

On the other hand, we can show that `sns.relplot()` returns a `FacetGrid` object, creating separate plots for the regions:

```{code-cell} ipython3
facet_plt = sns.relplot(data=df, x="ratio_of_urban_inhabitants", y="average_salary", col="region")
print(type(facet_plt))
```

Other Figure-level seaborn functions include `catplot`, `displot`, `pairplot`, and `jointplot`. Let's now jump into one of the most simple, yet essential, data visualizations: the bar plot.

## Barplots

A good use of a bar plot might be to show counts of something, while poor use of a bar plot might be to show group means. Numerous studies have discussed inappropriate uses of bar plots, noting that "because the bars always start at zero, they can be misleading: for example, part of the range covered by the bar might have never been observed in the sample." Despite the numerous reports on incorrect usage, bar plots remain one of the most common problems in data visualization.

The most basic [`seaborn.barplot()`](https://seaborn.pydata.org/generated/seaborn.barplot.html) function takes in a categorical and a numeric variable as <b>encodings</b>. A second layer of grouping, preferably with another categorical variable, can be added with the `hue` argument. 

### Example

Suppose the marketing manager wants to see a visualization for the number of <b>unique</b> loan ID's associated with each status of paying off the loan. To tackle this question, we will, first, create a CTE from the `s1.loan` table and obtain the counts for each status in different columns:

```{code-cell} ipython3
%%sql --save bar_plot_example
SELECT DISTINCT status, COUNT(loan_id) AS count_loan_id
FROM s1.loan
GROUP BY status
ORDER BY status;
```

Save the CTE in a dataframe:

```{code-cell} ipython3
result = %sql SELECT * FROM bar_plot_example
df = result.DataFrame()
```

Finally, use `seaborn.barplot()` to produce a bar plot:

```{code-cell} ipython3
sns.barplot(data=df, x="status", y="count_loan_id")
plt.xlabel("Status of Paying off Loan")
plt.ylabel("Count")
plt.title("Count of Loan ID's by Loan Status")
```

### Question 1 (Medium)

The marketing manager now wants you to provide the same information as the example above, but with an added grouping of the frequency of issuance of statements, which corresponds to the `frequency` variable in the `s1.account` table. Create a grouped bar plot with  clear axes labels, axes tick marks, title, and legend.

<b>Hint</b> Since the `frequency` variable is not in `s1.loan`, think of which SQL operation you can employ to combine both tables. Moreover, the `s1.loan` is a subset of the `s1.account` so use the appropriate technique that provides all rows from `s1.account`.

<!-- #region -->
<details>
<summary>Answers</summary>

We start off by creating a CTE from both the `s1.loan` and `s1.account` table with the help of a `LEFT JOIN` on `account_id`. The reason for choosing this join is because all `account_id`'s in `s1.loan` are present in `s1.account`, so we obtain all accounts in the database. Next, because we also want counts by `frequency`, we add it to the `GROUP BY` clause and ensure we pass `DISTINCT` in the `SELECT` clause:

```{code-cell} ipython3
%%sql --save bar_plot_question
SELECT DISTINCT status, frequency, COUNT(loan_id) AS count_loan_id
FROM s1.account
LEFT JOIN s1.loan 
    ON s1.account.account_id = s1.loan.account_id
GROUP BY status, frequency
ORDER BY status;
```

Save the CTE in a dataframe:

```{code-cell} ipython3
result = %sql SELECT * FROM bar_plot_question
df = result.DataFrame()
```

Finally, use `seaborn.barplot()`, this time with the `hue` argument, to produce a <b>grouped bar plot</b>:

```{code-cell} ipython3
sns.barplot(data=df, x="status", y="count_loan_id", hue="frequency")
plt.xlabel("Status of Paying off Loan")
plt.ylabel("Count")
plt.title("Count of Loan ID's by Loan Status and Frequency of Statement Issuance")
```

</details>
<!-- #endregion -->

<!-- #region -->

## Scatter plots

Scatter plots help us analyze relationships between two numeric variables. In the example below we will introduce a Figure-level function `relplot()` to create faceted scatter plots that help us easily visualize data from multiple tables and columns.

### Example

sns.relplot(
    data=tips, x="total_bill", y="tip", col="time",
    hue="time", size="size", style="sex",
    palette=["b", "r"], sizes=(10, 100)
)

### Question 2 (Hard)

join district and account, filter 

## Density plots

### Example

### Question 3 (Medium)

## Box and whisker plot

### Example

### Question 4 (Easy)

## Heatmap

### Example

### Question 5 (Medium)

+++
