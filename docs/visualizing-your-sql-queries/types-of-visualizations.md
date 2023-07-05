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

# Types of data visualizations

Welcome to the <b>Visualizing your SQL queries</b> module of the course! This part of the course will introduce data visualizations and commonly used packages. After getting familiar with the types of data visualizations and visualization packages, we'll revisit SQL and teach you JupySQL's unique feature of utilizing `ggplot` to visualize queries.

In this module, we will learn about the `seaborn` and `plotly` packages. Before we get into the details of each package, we first introduce the common types of data visualization with one of the most basic visualization packages: `matplotlib`. The purpose of this section is to not teach you the ins and outs of `matplotlib`, but more so to introduce some basic data visualizations. 

## Getting started

To demonstrate these visualizations, we're going to revisit our familiar bank data set from the [Making Your First Query](https://ploomber-sql.readthedocs.io/en/latest/intro-to-sql/making-your-first-query.html) section.

As always, let's first follow the steps of ensuring we have our necessary packages ready for use.

<!-- #region -->
## Install - execute this once. 

This code installs JupySQL, DuckDB, Pandas, and Matplotlib in your environment. We will be using these moving forward.

```{code-cell} ipython3
%pip install jupysql --upgrade duckdb-engine pandas matplotlib --quiet
```

## Load the data
We extract the bank marketing data by retrieving it from it's URL download link. The link may be a zip file (which it is in this case), so we extract the zip file, read the file containing the data within the zip file, and clean the data. Finally, we save this cleaned data to it's own seperate file called `bank_cleaned.csv`. We also import the `matplotlib` package as `plt`.

```{code-cell} ipython3
import sys
import matplotlib.pyplot as plt

sys.path.insert(0, "../../")
import banking  # noqa: E402

_ = banking.BankingData("https://tinyurl.com/jb-bank", "bank")
_.extract_to_csv()
```

After running this code, you should have `bank_cleaned.csv` in the current directory. 

## Load Engine
We now load in our SQL extension that allows us to execute SQL queries in Jupyter Notebooks. 

<b>Note</b> Ensure you restart any previous notebook that has the same database name as the one initialized below.

```{code-cell} ipython3
# Loading in SQL extension
%reload_ext sql
# Initiating a DuckDB database named 'bank.duck.db' to run our SQL queries on
%sql duckdb:///bank.duck.db
```

## Creating Table

Now that we have our `bank_cleaned.csv` file, let's load it into our DuckDB database and take a look at the data.

```{code-cell} ipython3
%%sql
CREATE OR REPLACE TABLE bank AS
FROM read_csv_auto('bank_cleaned.csv', header=True, sep=',')
```

```{code-cell} ipython3
%sqlcmd explore --table bank
```

The visualization packages we will be introducing in this module work best with the <b>Pandas DataFrame</b> data structure. Prior to visualizing our queries, we will always first convert them into Pandas DataFrames.

We convert the `bank` table below as an example.

```{code-cell} ipython3
bank = %sql SELECT * FROM bank
bank_df = bank.DataFrame()
bank_df
```

<!-- #region -->

Now we can jump into one of the most simple, yet essential, data visualizations: the bar plot.

## Bar Plot

Let's use a bar plot that visualizes the count of each job type in our data. To do so, we will query the counts of each job and convert the query into a Pandas DataFrame.

```{code-cell} ipython3
%%sql --save jobs
SELECT job, COUNT(*) as count
FROM bank 
GROUP BY job
```

```{code-cell} ipython3
jobs = %sql SELECT * FROM jobs
jobs_df = jobs.DataFrame()
```

Now that we have our query in a Pandas DataFrame, we can use `matplotlib` to visualize a bar plot.

```{code-cell} ipython3
plt.figure(figsize=(10, 6))
plt.bar(data=jobs_df, x="job", height="count")

plt.xlabel("Job")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.title("Count of Each Job")

plt.show()
```

The second line in the above code cell, `plt.bar(data=jobs_df, x="job", height="count")`, is really all we need to create a baseline bar plot. The remaining statements are supplemental elements that labels and customizes the y-axis, x-axis, size, and title of the plot. 

We can easily see that `management` and `blue-collar` jobs are the most prominent job category in this data set. Box plots are a great option when you need to visualize distributions of groups in a categorical variable.

## Scatter Plot

We first query the `age` and `balance` of single individuals and save it as a table called `age_balance` with a CTE.

```{code-cell} ipython3
%%sql --save age_balance
SELECT age, balance, marital
FROM bank
WHERE marital = 'single'
```

Then we again convert the table as a Pandas DataFrame.

```{code-cell} ipython3
age_balance_query = %sql SELECT * FROM age_balance
age_balance_df = age_balance_query.DataFrame()
```

```{code-cell} ipython3
plt.figure(figsize=(10, 6))
plt.scatter(data=age_balance_df, x="age", y="balance")

plt.xlabel("Age")
plt.ylabel("Balance")
plt.title("Age by Balance of Single Clients")
```

Scatter plots are great when analyzing the relationship between two numerical variables. In this example, we plot the relationship between one's `age` and `balance` for single individuals in our data set. 

## Box Plot

```{code-cell} ipython3
%%sql --save edu_balance
SELECT education, age
FROM bank
```

```{code-cell} ipython3
edu_balance_query = %sql SELECT * FROM edu_balance
edu_df = edu_balance_query.DataFrame()
```

```{code-cell} ipython3
# group the data by 'education'
edu_group = edu_df.groupby("education")["age"].apply(list)

plt.figure(figsize=(10, 6))
plt.boxplot(edu_group)

# customize x-axis tick labels
plt.xticks(range(1, len(edu_group) + 1), edu_df["education"].unique())

plt.xlabel("Education Level")
plt.ylabel("Age")
plt.title("Boxplot of Education Level by Age")

plt.show()
```

Box plots can be used when examining the relationship between a categorical feature and a numerical feature. In this plot, our categorical feature is the `education` variable. Each box represents a group within `education` and their respective ages in quantiles. This allows for a quick comparison of the distribution of groups within this categorical variable.

## Heat Map

```{code-cell} ipython3
%%sql --save job_education
SELECT job, education, COUNT(*) as count
FROM bank 
GROUP BY job, education
```

```{code-cell} ipython3
job_edu_query = %sql SELECT * FROM job_education
job_df = job_edu_query.DataFrame()
```

```{code-cell} ipython3
data = job_df.pivot(index="education", columns="job", values="count")

plt.figure(figsize=(10, 6))
plt.imshow(data)

plt.colorbar(label="Count")
plt.xticks(range(len(data.columns)), data.columns, rotation=45)
plt.yticks(range(len(data.index)), data.index)
plt.title("Heatmap of Job and Education")

plt.show()
```

The above plot displays the counts of `job` and `education` level of our data set. Heat maps are generally easy to understand because viewers can quickly point out extremes based on darker or lighter boxes. Here, we easily see people with management jobs have a high count of having a tertiary level education in our data set. You can think of heat maps as illustrating three dimensions: the x-axis, the y-axis, and the color gradient (which is usually a numerical feature).

## Wrapping Up

In this section, we introduced some basic data visualization plots: bar plots, scatter plots, box plots, and heat maps. The sections moving forward will teach you how to implement each of these plots using the `seaborn` and `plotly` libraries using the familiar banking data sets from the previous modules.
