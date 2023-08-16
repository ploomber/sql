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

## Install and Load Libraries

```{important}
<b>Note:</b> The `--save` and `%sqlcmd` features used require the latest JupySQL version. Ensure you run the code below to update JupySQL.
```

This code installs JupySQL, DuckDB, Matplotlib (required dependency), and ipywidgets in your environment. We will be using these moving forward.

```{code-cell} ipython3
%pip install jupysql matplotlib ipywidgets --quiet
```

Finally, we load in the libraries we will be using in this tutorial.

```{code-cell} ipython3
import matplotlib.pyplot as plt
from sql.ggplot import ggplot, aes, geom_boxplot, geom_histogram, facet_wrap
import ipywidgets as widgets
from ipywidgets import interact
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

1. Suppose the finance manager wants to visualize boxplots of `average_salary` and loan `payments` of those customers who have loans. We can do so in a single plot! We will first join all three tables to obtain the relevant data, save the output as a CTE, and use that CTE for `%sqlplot boxplot`:

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
plt.rcParams["figure.dpi"] = 300  # high resolution
plt.rcParams["figure.figsize"] = (12, 4)

%sqlplot boxplot --table sqlplot_boxplot_example --column payments average_salary
plt.show()
```

Several attributes of the plot can be customized because it is a `matplotlib.Axes` object. Below is a customized, cleaner version of the above plot:

```{code-cell} ipython3
ax = %sqlplot boxplot --table sqlplot_boxplot_example --column payments average_salary --orient h
ax.set_title("Boxplot of Loan Payments and Average Salary ($)")
ax.set_xlabel("Amount ($)")
plt.show()
```

2. Suppose the manager wants to get a closer look of both distributions, loan `payments` and `average_salary` of those customers who have loans. You can quickly produce a histogram by using the saved CTE:

```{code-cell} ipython3
ax = %sqlplot histogram --table sqlplot_boxplot_example --column payments average_salary --bins 25
ax.set_title("Histogram of Loan Payments and Average Salary ($)")
ax.set_xlabel("Amount ($)")
plt.show()
```

### Question 1 (Easy)

+++

The finance manager is impressed with how quickly you produced these plots! He wants another easy deliverable: facet the multiple column boxplot and histogram in a single graph. Make sure to customize the plot with clear axes labels and titles!

<b>Hint:</b> Recall the seaborn [tutorial](https://ploomber-sql.readthedocs.io/en/latest/visualizing-your-sql-queries/plotting-with-seaborn.html#id2) of how to add/position multiple matplotlib axes subplots.

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
plt.show()
```

</details>
<!-- #endregion -->

<!-- #region -->

```{important}
Initializing the whole figure with `fig` and assigning individual axes with `ax1` and `ax2`, [like in this example](https://ploomber-sql.readthedocs.io/en/latest/visualizing-your-sql-queries/plotting-with-seaborn.html#question-3-easy), would not work.
```

## `ggplot` API

You might be wondering "how can ggplot, the R package, function in Jupyter Notebooks?". Do not worry! In this tutorial, we will be learning about JupySQL's `ggplot` API to visualize our SQL queries. This plotting technique will be useful for avid R programmers, who are familiar with `ggplot2`, and for first-time learners.

The `ggplot` API is built on top of `matplotlib` and is structured around the principles of the [Grammar of Graphics](https://bookdown.org/alhdzsz/data_viz_ir/ggbasics.html), allowing you to build any graph using the same `ggplot2` components: a data set, a coordinate system, and geoms (geometric objects). However, to make the API suitable for JupySQL, we <b>input a SQL table name, instead of a dataset</b>. Therefore, the same [workflow](https://ploomber-sql.readthedocs.io/en/latest/visualizing-your-sql-queries/plotting-with-seaborn.html#barplots) of creating our CTE, which was employed in the `seaborn` tutorial, will be in action here as well (no need to convert the CTE into a pandas `DataFrame()`).

<b>Note</b> at this point, JupySQL's `ggplot` API supports:

Aes:

- `x` - a SQL column mapping

- `color` and `fill` to apply edgecolor and fill colors to plot shapes

Geoms:

- `geom_boxplot` similar to `%sqlplot boxplot`

- `geom_histogram` similar to `%sqlplot histogram`

Facet:

- `facet_wrap` to display multiple plots in a single layout

```{important}
Lastly, unlike `%sqlplot` that returns a `matplotlib.Axes` object, the `ggplot` API returns a `ggplot` object, which cannot be customized like we did when using `%sqlplot`. Therefore, customizing axes labels and titles is not possible in `ggplot` API yet.
```

### `ggplot` Template

To build a graph, we first should initialize a `ggplot` instance with a reference to our SQL table using the `table` parameter, and a mapping object. Here’s is the complete template to build any graph:

```python
(
    ggplot(table='sql_table_name', mapping=aes(x='table_column_name'))
    +
    geom_func() # geom_histogram or geom_boxplot (required)
    +
    facet_func() # facet_wrap (optional)
)
```

```{important}
When working with CTE's, we must include it along with `table` using the `with_` parameter. In this tutorial, we will be using CTE's throughout our examples.
```

### `ggplot` CTE

We will create a CTE to use throughout the `ggplot` examples. All the information from the three tables, `account`, `district`, and `loan`, will be present in this CTE, named `ggplot_CTE`, for convenience. The `--no-execute` function tells JupySQL to <i>skip the execution of the stored query</i>.

```{code-cell} ipython3
%%sql --save ggplot_CTE --no-execute
SELECT *
FROM s1.account AS a
LEFT JOIN s1.loan AS l
ON a.account_id = l.account_id
LEFT JOIN s1.district AS d
ON d.district_id = a.district_id
```

Now, let's look at different types of visualizations using the `ggplot` API and test ourselves on them!

### `geom_boxplot`

To visualize the loan `amount` and `average_salary` of those customers who have loans, we can create a boxplot in `ggplot` using the saved CTE.

```{code-cell} ipython3
(
    ggplot(
        table="ggplot_CTE",
        with_="ggplot_CTE",
        mapping=aes(x=["amount", "average_salary"]),
    )
    + geom_boxplot()
)
```

From the graph above, it is strange to see that customers are opting for loans that are significantly greater than their average salary. However, it could be the case that the earning population's salaries are skewed to the right and the customers actually obtaining loans are relatively wealthier.

### Question 2 (Easy)

Create the same boxplot from the `%sqplplot` example using the `ggplot` API. The columns used were `payments` and `average_salary`.

<!-- #region -->
<details>
<summary>Answers</summary>

```{code-cell} ipython3
(
    ggplot(
        table="ggplot_CTE",
        with_="ggplot_CTE",
        mapping=aes(x=["payments", "average_salary"]),
    )
    + geom_boxplot()
)
```

</details>
<!-- #endregion -->

<!-- #region -->

### `geom_histogram`

Unlike `geom_boxplot`, `geom_histogram` is more flexible because we can not only modify the `fill` and `color` attributes, but also facet the histograms for a categorical variable. `fill` corresponds to the color of the bars and `color` corresponds to the bars` border color.

We can recreate the histogram produced in the `%sqplplot` example, with the columns `payments` and `average_salary`, and specify our own colors for each histogram:

```{code-cell} ipython3
(
    ggplot(
        table="ggplot_CTE",
        with_="ggplot_CTE",
        mapping=aes(
            x=["payments", "average_salary"],
            fill=["#d500f9", "#fb8c00"],
            color="black",
        ),
    )
    + geom_histogram(bins=10)
)
```

Moreover, we can also map the `fill` attribute to a variable, such as `status`, and the bars will stack automatically. For example, if we want to visualize the histogram of `payments` with `status` as the `fill` attribute, then each colored rectangle on the stacked bars will represent a unique combination of `payments` and `status`:

```{code-cell} ipython3
(
    ggplot(
        table="ggplot_CTE",
        with_="ggplot_CTE",
        mapping=aes(x="payments", color="black"),
    )
    + geom_histogram(bins=10, fill="status")
)
```

```{important}
When mapping `fill` with a variable, make sure to specify it in `geom_histogram()` rather than in `aes()`. `color` can optionally be specified, but only in `aes()`.
```

### Question 3 (Medium)

Create a categorical histogram for the columns `status` and `region`. Filter `region` to only include "Prague" and "central Bohemia". Use `fill` colors of your choice, but make sure the borders of each bar are prominent.

<!-- #region -->
<details>
<summary>Answers</summary>

We will filter the regions from the `ggplot_CTE` to create a new CTE for this question:

```{code-cell} ipython3
%%sql --save ggplot_hist_q3 --no-execute
SELECT *
FROM ggplot_CTE
WHERE region IN ('Prague', 'central Bohemia')
```

```{code-cell} ipython3
(
    ggplot(
        table="ggplot_hist_q3",
        with_="ggplot_hist_q3",
        mapping=aes(
            x=["status", "region"],
            fill=["#008080", "#d500f9"],
            color="black",
        ),
    )
    + geom_histogram(bins=10)
)
```

</details>
<!-- #endregion -->

<!-- #region -->

### `facet_wrap`

Histograms produced with `ggplot` API can also be arranged in a sequence of panels into a 2D grid, which is beneficial when dealing with a single variable that has multiple levels, or when you want to arrange the plots in a more space efficient manner.

For example, the histogram for `payments` filled by all eight regions is tough to make sense of in a single plot. Therefore, `facet_wrap` can make visualizing the individual histograms easy:

```{code-cell} ipython3
plt.rcParams["figure.figsize"] = (15, 6)  # increase size of canvas

(
    ggplot(
        table="ggplot_CTE",
        with_="ggplot_CTE",
        mapping=aes(
            x="payments",
        ),
    )
    + geom_histogram(bins=10)
    + facet_wrap("region", legend=False)
)
```

### Question 4 (Medium)

Produce the same faceted histograms as above, but account for `fill` mapping to `status`. Make sure the legend is presented in the plots.

<b>Hint:</b> To present the legends clearly and to not distort the histograms because of the legends, specify `plt.rcParams["figure.figsize"] = (15,7)` before the `ggplot` function.

<!-- #region -->
<details>
<summary>Answers</summary>

```{code-cell} ipython3
plt.rcParams["figure.figsize"] = (15, 7)  # increase size of canvas

(
    ggplot(
        table="ggplot_CTE",
        with_="ggplot_CTE",
        mapping=aes(x="payments"),
    )
    + geom_histogram(bins=10, fill="status")
    + facet_wrap("region")
)
```

</details>
<!-- #endregion -->

<!-- #region -->

## Interactive `ggplot`

Similar to the Interactive Queries and Parameterization [module](https://ploomber-sql.readthedocs.io/en/latest/interactive-queries-and-parameterization/introduction-to-ipywidgets.html#putting-it-together), we can use the use the [interact](https://ipywidgets.readthedocs.io/en/stable/examples/Using%20Interact.html#using-interact) API from [Jupyter Widgets](https://ipywidgets.readthedocs.io/en/stable/index.html#jupyter-widgets). Widgets can be used with either `geom_boxplot` or `geom_histogram`, with the latter providing scope for greater flexibility due to the `fill` and `color` mappings.

Interact autogenerates UI controls for function arguments, and then calls the function with those arguments when you manipulate the controls interactively.

To use interact, you need to define:

1. Widgets to be controlled

2. The plot function that includes `ggplot` with dynamic argument(s) specified with the respective widget variable

3. Invoke `interact()` API

Let’s see examples below!

### Histogram - Basic Usage (with Dropdown and Slider widgets)

In this example, we will create multiple widgets: one for the `fill` argument specified in `aes()`, another for the `bins` argument in `geom_histogram`, and lastly for the `x` argument for specifying multiple columns:

```{code-cell} ipython3
dropdown = widgets.Dropdown(
    options=["red", "blue", "green", "magenta"],
    value="blue",
    description="Color:",
    disabled=False,
)
b = widgets.IntSlider(
    value=10,
    min=1,
    max=20,
    step=1,
    description="Bins:",
    orientation="horizontal",
)
columns = widgets.RadioButtons(
    options=["payments", "average_salary", "amount"],
    description="Column:",
    disabled=False,
)
```

```{code-cell} ipython3
def plot_fct(columns, color, b):
    (
        ggplot(
            table="ggplot_CTE",
            with_="ggplot_CTE",
            mapping=aes(x=columns, fill=color),
        )
        + geom_histogram(bins=b)
    )


interact(plot_fct, color=dropdown, b=b, columns=columns)
```

### Boxplot - Multiple Columns (with Select Widget)

To visualize all three financial variables, `payments`, `average_salary`, `amount`, in a single box plot, we can use the `SelectMultiple` widget:

```{code-cell} ipython3
columns = widgets.SelectMultiple(
    options=["payments", "average_salary", "amount"],
    value=["average_salary"],
    description="Column(s):",
    disabled=False,
)
```

```{code-cell} ipython3
plt.rcParams["figure.figsize"] = (12, 3)  # increase size of canvas


def plot(columns):
    (
        ggplot(table="ggplot_CTE", with_="ggplot_CTE", mapping=aes(x=columns))
        + geom_boxplot()
    )


interact(plot, columns=columns)
```

### Categorical Histogram (with Select widget)

+++

With `geom_histogram`, we can specify the following widgets:

- Multiple columns using the `SelectMultiple` widget like in the examples above. It is recommended to not use any of `fill`, `color`, or `cmap` when creating a widget for multiple columns because different colors will not be mapped to multiple columns.
- Number of Bins using the `IntSlider` widget, which was shown in the Basic Usage example
- Manually changing the color of the bars (when not mapping `fill` with a categorical variable) by using a selection widget (as shown in the Basic Usage example)
- Changing the color of the bars with a colormap (`cmap`) when mapping `fill` with a categorical variable by using a selection widget

+++

Below is an example that utilizes widgets for `cmap`, `fill`, and `bins` to visualize `payments` by `status` or `frequency`:

```{code-cell} ipython3
b = widgets.IntSlider(
    value=10,
    min=1,
    max=20,
    step=1,
    description="Bins:",
    orientation="horizontal",
)
cmap = widgets.Dropdown(
    options=["viridis", "plasma", "inferno", "magma", "cividis"],
    value="plasma",
    description="Colormap:",
    disabled=False,
)
fill = widgets.RadioButtons(
    options=["status", "frequency"],
    # value="status",
    description="Fill by:",
    disabled=False,
)
```

```{code-cell} ipython3
def plot(b, cmap, fill):
    (
        ggplot(
            table="ggplot_CTE", with_="ggplot_CTE", mapping=aes(x="payments")
        )  # noqa E501
        + geom_histogram(bins=b, fill=fill, cmap=cmap)
    )


interact(plot, b=b, cmap=cmap, fill=fill)
```

### Question 5 (Hard)

We can also employ widgets in the `facet_wrap` function and this question will make you practice that as well as some of the above widgets in the Categorical Histogram example! Create four widgets: one each for `bins`, `cmap`, `fill`, and `legend`. Visualize the histogram of loan `amount` by either `status` or `frequency` (this will require a widget) and facet it by `region`. Use the same widgets as the examples for `bins` and `cmap` and create a `ToggleButton` widget for `legend`. Make sure that all widgets used are unique and the plot size is big enough to incorporate the legends!

<!-- #region -->
<details>
<summary>Answers</summary>

```{code-cell} ipython3
b = widgets.IntSlider(
    value=10,
    min=1,
    max=20,
    step=1,
    description="Bins:",
    orientation="horizontal",
)
cmap = widgets.Dropdown(
    options=["viridis", "plasma", "inferno", "magma", "cividis"],
    value="plasma",
    description="Colormap:",
    disabled=False,
)
fill = widgets.RadioButtons(
    options=["status", "frequency"],
    # value="status",
    description="Fill by:",
    disabled=False,
)
show_legend = widgets.ToggleButton(
    value=False,
    description="Show legend",
    disabled=False,
    button_style="",
    tooltip="Is show legend",
)
```

```{code-cell} ipython3
plt.rcParams["figure.figsize"] = (15, 7)  # increase size of canvas


def plot(b, cmap, fill, show_legend):
    (
        ggplot(table="ggplot_CTE", with_="ggplot_CTE", mapping=aes(x="amount"))
        + geom_histogram(bins=b, fill=fill, cmap=cmap)
        + facet_wrap("region", legend=show_legend)
    )


interact(plot, b=b, cmap=cmap, fill=fill, show_legend=show_legend)
```

</details>
<!-- #endregion -->

<!-- #region -->

+++

Delete tables

```{code-cell} ipython3
%%sql
DROP TABLE IF EXISTS s1.loan;
DROP TABLE IF EXISTS s1.account;
DROP TABLE IF EXISTS s1.district;
DROP SCHEMA s1;
```

## Wrapping Up

In this section, we learned about plotting boxplots and histograms with `%sqlplot` and `ggplot` API. We also employed widgets to interactively query with `ggplot` API. To summarize:

- `%sqlplot` is a great tool for not only creating plots quickly, but also customizing them at a low level because it returns a `matplotlib.Axes` object

- `geom_boxplot` and `geom_histogram` are useful when integrating with `ipywidgets` and when dealing with categorical variables with a lot of unique values.

This ends the Visualizing Your Queries module, we hope the skills imbibed in this module will assist you to visually uncover interesting insights from your data! The next module focuses on how to package your SQL project.

## References

“Simple Widget Introduction#.” Simple Widget Introduction - Jupyter Widgets 8.0.5 documentation, n.d. https://ipywidgets.readthedocs.io/en/stable/examples/Widget Basics.html.

“Widget List#.” Widget List - Jupyter Widgets 8.0.5 documentation, n.d. https://ipywidgets.readthedocs.io/en/stable/examples/Widget List.html.

