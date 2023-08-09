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

# Parameterizing Queries 

In the last module, you learned how to use SQL within Jupyter notebooks with JupySQL, and you learned how you can combine it with usage of widgets to create interactive graphical user interfaces (GUIs) for your SQL queries. This module will take you a step further. Here, we will discuss how to parameterize your SQL queries and effectively utilize ipywidgets to create more interactive data workflows. Let's dive in!

## Set up and data access


```{important}
<b>Note:</b> The --save and %sqlcmd features used require the latest JupySQL version. Ensure you run the code below.
```

This code installs JupySQL, and DuckDB in your environment. We will be using these moving forward.

```{code-cell} ipython3
%pip install jupysql jupysql-plugin --quiet
```

We continue to work with the Bank and Marketing data set. 

```{important}
Source: UCI Machine Learning Repository

URL: https://archive-beta.ics.uci.edu/dataset/222/bank+marketing

Data Citation

Moro,S., Rita,P., and Cortez,P.. (2012). Bank Marketing. UCI Machine Learning Repository. https://doi.org/10.24432/C5K306.
```

We can use the following function to extract the downloaded data from the UCI repository.

```{code-cell} ipython3
import sys

sys.path.insert(0, "../../")
import banking  # noqa: E402

_ = banking.BankingData("https://tinyurl.com/jb-bank", "bank")
_.extract_to_csv()
```

Initialize a DuckDB Instance:

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

```{code-cell} ipython3
%sqlcmd columns -t bank
```

## Variable Expansion

JupySQL supports variable expansion in the form of ``{{variable}}``. This allows you to write a query with placeholders that can be replaced by variables dynamically. The benefits of using parameterized SQL queries are that they can be reused with different values, prepared ahead of time, and used with dynamic data.

Let's start with a simple query template with placeholders, and substitute the placeholders with a couple of variables using variable expansion.

We are going to select two columns (`age` and `job`) from the table `bank` with the variable `dynamic_column` and show only 5 rows. We can control this via another variable `dynamic_limit`.

```{code-cell} ipython3
dynamic_limit = 5
dynamic_column = "age, job"
%sql SELECT {{dynamic_column}} FROM bank LIMIT {{dynamic_limit}}
```

### Sample case

The HR department would like to determine top five oldest and youngest employees in two different jobs: services, management.

We can combine Python with SQL code using the `%sql` magic. With Python we can iterate over the jobs in the list `jobs`. With parameterization, we can
then insert the job into the SQL query via the `{{variable}}` notation.

```{code-cell} ipython3
jobs = ["services", "management"]

for job in jobs:
    print(f"Top 5 oldest in {job}")
    order = "DESC"
    o_ = %sql SELECT * FROM bank WHERE job='{{job}}' ORDER BY age {{order}} LIMIT 5
    print(o_)

    print(f"Top 5 youngest in {job}")
    order = "ASC"
    y_ = %sql SELECT * FROM bank WHERE job='{{job}}' ORDER BY age {{order}} LIMIT 5
    print(y_)
```

### Mini Exercise:

The marketing team is interested in understanding the distribution of age for their marketing campaigns. Select the top 5 oldest and youngest people who have been part of the marketing campaign (`campaign` column).

Your task: use a loop with variable expansion to accomplish this. 

<!-- #region -->
<details>

<summary>Answers</summary>

```{code-cell} ipython3
campaign = %sql SELECT DISTINCT campaign FROM bank
campaign = campaign.DataFrame()

campaigns = campaign["campaign"].tolist()[:2]

for campaign in campaigns:
    print(f"Top 5 oldest in campaign {campaign}")
    order = "DESC"
    oldest_camppaing = %sql SELECT * FROM bank WHERE campaign={{campaign}} ORDER BY age {{order}} LIMIT 5
    print(oldest_camppaing)

    print(f"Top 5 youngest in campaign {campaign}")
    order = "ASC"
    youngest_campaign = %sql SELECT * FROM bank WHERE campaign={{campaign}} ORDER BY age {{order}} LIMIT 5
    print(youngest_campaign)
```

</details>
<!-- #endregion -->

## Variable Expansion Using Loops

We can also use loops inside SQL to parameterize our queries. For example, let's calculate the average age for each job role in the `bank` table.

The query below will iterate over four kinds of jobs: blue collar, technician, services and management. For each job, it will compute the average age for people with that job and create a new column for the average of each job.

The resulting query can be reused as it is being saved as `avg_age` with the `--save` option.

```{code-cell} ipython3
%%sql --save avg_age
{% set jobs = [ "blue_collar", "technician", "services", "management"] %}
select
    {% for job in jobs %}
    avg(case when job = '{{job.replace('_', '-')}}' then age end) as avg_age_{{job}},
    {% endfor %}
from bank
```

We can see the final compiled query using:

```{code-cell} ipython3
final = %sqlrender avg_age
print(final)
```

### Sample case

The HR department would like to determine the average balance for employees by job (for jobs technician, services and management) and education level. We can achieve this by using the `job` and `education` columns from the `bank` table.

```{code-cell} ipython3
%%sql --save avg_balance
{% set jobs = [ "technician", "services", "management"] %}
{% set education_levels = [ "primary", "secondary", "tertiary", "unknown"] %}
select
    {% for job in jobs %}
    {% for education in education_levels %}
    avg(case when job = '{{job}}' and education = '{{education}}' then balance end) as avg_balance_{{job}}_{{education}},
    {% endfor %}
    {% endfor %}
from bank
```

### Mini Exercise:

Calculate the count of people for each job role for jobs  "blue_collar", "technician", "services", "management".

Your task: use Variable Expansion Using Loops and the `%%sql` magic

<!-- #region -->
<details>

<summary>Answers</summary>

```{code-cell} ipython3
%%sql --save count_jobs
{% set jobs = [ "blue_collar", "technician", "services", "management"] %}
select
    {% for job in jobs %}
    count(case when job = '{{job.replace('_', '-')}}' then 1 end) as count_{{job}},
    {% endfor %}
from bank
```

</details>
<!-- #endregion -->

## Macros + Variable Expansion


`Macros` is a construct analogous to functions that promote re-usability. We define a `macro` using the {% macro %} tag and use this macro in the query using variable expansion.

For example, let's define a macro to convert a value from days to years, and use this macro in our query. This macro will be called `days_to_years` and it takes as input the `column_name` and `precision`. With the default `precision` set to 2.

We can obtain the number of years by dividing the number of days by 365. 

We can then use the `days_to_years` macro in the query, where we are passing `age` as the input column.

```{code-cell} ipython3
%%sql --save convert
{% macro days_to_years(column_name, precision=2) %}
    ({{ column_name }} / 365)::numeric(16, {{ precision }})
{% endmacro %}

select
  job, marital,
  {{ days_to_years('age') }} as age_in_years
from bank
```

In this query, we're converting age from days to years using our macro. The results are saved in a variable `convert`.

The final rendered query can be viewed using:

```{code-cell} ipython3
final = %sqlrender convert
print(final)
```

### Sample usage

Let's use macros to handle `NULL` values. The macro below checks if the chosen column has `NULL` values.

The code block defines a macro that will be used later in the SQL query. The macro is named `months_to_years_handle_null`, and its purpose is to convert the values in a specified column from months to years. Additionally, this macro is designed to handle null values in a column, hence its name. 

If the value in the column is null, the macro will return `NULL`; otherwise, it will convert the value from months to years.

```{code-cell} ipython3
%%sql --save convert_duration_handle_null
{% macro months_to_years_handle_null(column_name, precision=2) %}
    (case when {{ column_name }} is not null then {{ column_name }} / 12 else null end)::numeric(16, {{ precision }})
{% endmacro %}

select
  job, marital,
  {{ months_to_years_handle_null('duration') }} as duration_in_years
from bank
```

```{code-cell} ipython3
final = %sqlrender convert_duration_handle_null
print(final)
```

### Mini exercise

Use the `months_to_years_handle_null` macro to iterate over the `jobs`: "blue_collar", "technician", "services", "management". For each job in the loop, calculate the average duration for the specified job. Save this query as `avg_duration`. Display the query.

<!-- #region -->
<details>

<summary>Answers</summary>

This modification is using the `months_to_years_handle_null` macro that you had defined earlier. This macro will convert duration from months to years for each job category, while also handling null values. The macro will apply to the average duration of each job category (where the job is equal to the current job in the loop). The output for each job category is then given an alias that indicates the job category and that it represents average duration in years.

Just like before, the code below will dynamically generate the SQL query, and the --save directive will save the query result into the avg_duration variable.

```{code-cell} ipython3
%%sql --save avg_duration
{% macro months_to_years_handle_null(column_name, precision=2) %}
    (case when {{ column_name }} is not null then {{ column_name }} / 12 else null end)::numeric(16, {{ precision }})
{% endmacro %}
{% set jobs = [ "blue_collar", "technician", "services", "management"] %}
select
    {% for job in jobs %}
    {{ months_to_years_handle_null('avg(case when job = \'' + job.replace('_', '-') + '\' then duration end)') }} as avg_duration_{{job}},
    {% endfor %}
from bank
```

Display the query:

```{code-cell} ipython3
final = %sqlrender avg_duration
print(final)
```

</details>
<!-- #endregion -->


## Creating multiple tables dynamically

We'll finish off this section by showing you how you can generate multiple tables dynamically. 

Your task now is to create separate tables for each job. This can easily be accomplished using a loop and variable expansion:

```{code-cell} ipython3
%%sql
DROP TABLE IF EXISTS services;
DROP TABLE IF EXISTS management;
```

```{code-cell} ipython3
jobs = ["services", "management"]
for job in jobs:
    %sql CREATE TABLE {{job}} AS (SELECT * from bank WHERE job = '{{job}}')
```

Let's check the tables in our schema:

```{code-cell} ipython3
%sqlcmd tables
```

Delete table

```{code-cell} ipython3
%%sql
DROP TABLE bank;
DROP TABLE services;
DROP TABLE management;
```


## Conclusion
In this module, we have explored how to parameterize SQL queries and effectively integrate with Python for a more interactive data analysis workflow within Jupyter notebooks. This method is facilitated using JupySQL and DuckDB. We've also demonstrated how to dynamically create and use variables within SQL queries, further enhancing the flexibility and interactivity of the notebooks.

We delved into the basics of variable expansion, using loops within SQL to iterate over arrays, and how to define and use macros to promote reusability and reduce redundancy. We further illustrated the potential of these techniques through several practical examples, including determining the top five oldest and youngest employees in various jobs, calculating average ages and balances by job and education level, handling `NULL` values with `macros`, and dynamically creating multiple tables.

Through these exercises, it has been made evident that integrating SQL into Jupyter notebooks provides an intuitive and powerful approach to data exploration and analysis. The techniques demonstrated in this module can be widely applied across various datasets, making it a useful skillset for data scientists and analysts. By merging the strengths of Python's flexibility and SQL's data management capabilities, we can create more powerful and interactive data workflows.

In the next section, you'll learn how to combine paramaterization with `ipywidgets`.
