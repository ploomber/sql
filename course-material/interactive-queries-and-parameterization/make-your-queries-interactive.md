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

# Make your queries interactive

In this section, we will combine the learnings from the two previous sections, [Intro to `ipywidgets`](https://ploomber-sql.readthedocs.io/en/latest/interactive-queries-and-parameterization/introduction-to-ipywidgets.html) and [Parameterizing SQL Queries](https://ploomber-sql.readthedocs.io/en/latest/interactive-queries-and-parameterization/parameterize-sql-queries.html), to create interactive SQL queries using <b>JupySQL</b>. This technique is useful for conducting exploratory data analysis with SQL, as it allows us to filter our data and visualize the tabular results interactively.

```{code-cell} ipython3
:tags: [remove-cell]

# this cell is hidden in the docs for linting
import ipywidgets as widgets
```

The installation of `ipywidgets` was covered previously [here](https://ploomber-sql.readthedocs.io/en/latest/interactive-queries-and-parameterization/introduction-to-ipywidgets.html#ipywidgets).

## Set up and data access

```{important}
<b>Note:</b> The --save and %sqlcmd features used require the latest JupySQL version. Ensure you run the code below.
```

This code installs JupySQL, and DuckDB in your environment. We will be using these moving forward.

```{code-cell} ipython3
%pip install jupysql --upgrade jupysql-plugin --upgrade duckdb-engine --quiet
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
from urllib.request import urlretrieve
from zipfile import ZipFile
import pandas as pd
import os


def extract_to_csv(url, data_name):
    # Retrieve the zip file from the url link
    file = os.path.basename(url)
    urlretrieve(url, file)

    # Extract the zip file's contents
    with ZipFile(file, "r") as zf:
        zf.extractall()

    # The file containing our data
    csv_file_name = f"{data_name}.csv"

    # Data clean up
    df = pd.read_csv(csv_file_name, sep=";")

    # Save the cleaned up CSV file
    df.to_csv(df.to_csv(f"{data_name}_cleaned.csv", index=False))


# Running the above function
extract_to_csv("https://tinyurl.com/uci-marketing-data", "bank")
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

```{code-cell} ipython3
%sqlcmd columns -t bank
```

## `%sql --interact {{widget_variable}}`

In the [Intro to `ipywidgets`](https://ploomber-sql.readthedocs.io/en/latest/interactive-queries-and-parameterization/introduction-to-ipywidgets.html) section of this module, we learned how to apply python functions and decorators to create `ipywidgets`. In this section, we apply JupySQL's `--interact` argument, which allows us to create interactive SQL queries using `ipywidgets`. We also learned in the [previous section](https://ploomber-sql.readthedocs.io/en/latest/interactive-queries-and-parameterization/parameterize-sql-queries.html#variable-expansion) about variable expansion using placeholders for `{{variable}}`. We will combine these two concepts to create interactive SQL queries!

First, you need to define the `{{variable}}` as the form of a basic data type or `ipywidgets` Widget.
Then, pass the variable name into the `--interact` argument and use a `WHERE` clause to filter using the specified widgets variables. Below, we will delve into the different types of widgets and how to use them with JupySQL.

### Basic Data Types

The simplest way is to declare a variable with basic data types (Numeric, Text, Boolean...). [ipywidgets](https://ipywidgets.readthedocs.io/en/stable/examples/Using%20Interact.html?highlight=interact#Basic-interact) autogenerates UI controls for that variable.

An example with a numeric variable `duration`, which creates a slider UI for its values by default, is as follows:

```{code-cell} ipython3
duration_min = 1500
%sql --interact duration_min SELECT * FROM bank WHERE duration > {{duration_min}} LIMIT 5
```

<b>Note above</b> that we are filtering records by the variable `duration` if it is <b>greater than</b> the value of the slider widget `duration_min`.

An example with a categorical variable `loan`, which creates a text box for the user to type in values as a UI, is as follows:

```{code-cell} ipython3
loan = "yes"  # Try inputting "no" in the output's text box
%sql --interact loan SELECT * FROM bank WHERE loan == '{{loan}}' LIMIT 5
```

### Numeric Widgets

#### `IntSlider` and `FloatSlider`

These widgets were introduced in this [section](https://ploomber-sql.readthedocs.io/en/latest/interactive-queries-and-parameterization/introduction-to-ipywidgets.html#intslider-and-floatslider) of the module. Here, we will see how to use them with JupySQL.

An example for the `IntSlider` is as follows:

```{code-cell} ipython3
duration_lower_bound = widgets.IntSlider(min=5, max=3000, step=500, value=1500)

%sql --interact duration_lower_bound SELECT * FROM bank WHERE duration <= {{duration_lower_bound}} LIMIT 5
```

<b>Note</b>: Other Numeric Widgets can be found [here](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#floatlogslider).

### Selection Widgets

#### `RadioButtons`

These widgets were also introduced in the previous [section](https://ploomber-sql.readthedocs.io/en/latest/interactive-queries-and-parameterization/introduction-to-ipywidgets.html#radiobuttons) of this module.

An example of its usage with `--interact` is as follows:

```{code-cell} ipython3
outcome_selection = widgets.RadioButtons(
    options=["failure", "other", "success", "unknown"],
    description="Outcome",
    disabled=False,
)
```

```{code-cell} ipython3
%%sql --interact outcome_selection 
SELECT * FROM bank 
WHERE poutcome == '{{outcome_selection}}' 
LIMIT 5;
```

```{important}
When using selection widgets that only allow selecting one value, use `== '{{ widget_variable }}'` for the query to run without errors. On the other hand, if using multiple selection widgets, use `IN {{ widget_variable }}`.
```

<b>Note</b>: Other Selection Widgets can be found [here](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#selection-widgets).

### Complete Example

Now, we can demonstrate a way to combine multiple `ipywidgets` to make a more complex interactive SQL query, inclusive of different data types and widgets.

The code chunk below initializes multiple `ipywidgets`: <b>radio buttons</b> and <b>multiple selection</b> for the categorical variables `poutcome` and `loan` respectively and a <b>basic unbounded slider</b> for the numeric variable `duration`. The `show_limit` variable is a basic data type that creates a slider by default and is used to limit the number of rows, in this case between 0 to 10 with a step size of 1.

<b>Note</b>: For `poutcome`, multiple values can be selected with `shift` and/or `ctrl` (or `command`) pressed and mouse clicks or arrow keys.

```{code-cell} ipython3
duration_lower_bound = 500
show_limit = (0, 10, 1)
loan_selection = widgets.RadioButtons(
    options=["yes", "no"], description="Personal Loan", disabled=False
)
outcome_selection = widgets.SelectMultiple(
    options=["failure", "other", "success", "unknown"],
    value=["success", "failure"],
    description="Previous Campaign Outcome",
    disabled=False,
)
```

Next, we can use the `--interact` argument to create UI's for the above widgets, which will help us interactively filter our output, and pass them into the SQL query:

```{code-cell} ipython3
%%sql --interact show_limit --interact duration_lower_bound --interact loan_selection --interact outcome_selection
SELECT * FROM bank
WHERE poutcome IN {{outcome_selection}} AND 
duration > {{duration_lower_bound}} AND 
loan == '{{loan_selection}}'
LIMIT {{show_limit}} 
```

Try out other widgets, such as Boolean, String, and Datetime, detailed [here](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#) and see what you can come up with!

## Macros + `%sql --interact {{widget_variable}}`

The `--interact` argument can also be used with Macros, using the {% macro %} tag. Recall that a macro is <b>saved</b> in a variable with the `--save` flag. Therefore, JupySQL supports the use of multiple flags in a `%%sql` command. Applying macros to `ipywidgets` is useful when we want to use the same widget variable in multiple SQL queries. For a refresher on Macros, see this [section](https://ploomber-sql.readthedocs.io/en/latest/interactive-queries-and-parameterization/parameterize-sql-queries.html#macros-+-variable-expansion)

To show an example, consider the contact `duration` variable, measured in seconds, from the bank marketing dataset. Suppose the marketing manager wants to not only measure this variable in <b>minutes</b> but also filter it interactively across all other queries. We can, hence, use a macro to transform the variable and create a slider widget for it!

We first create our bounded `FloatSlider` numeric widget variable, just like previous instances. <b>Note</b> when using a macro, we need to initialize the widget variable in a python code-cell outside of the macro's code-cell, which will be executed as an SQL cell wholly.

```{code-cell} ipython3
duration_slider = widgets.FloatSlider(
    min=0.05, max=51, step=1, value=5, description="Contact Duration (mins)"
)
```

Next, we initialize our macro function and specify the SQL query with the widget variable that produces the UI for the slider and the tabular output for the saved query:

```{code-cell} ipython3
%%sql --save convert --interact duration_slider
{% macro sec_to_min(column_name, precision=2) %}
    ({{ column_name }} / 60)::numeric(16, {{ precision }})
{% endmacro %}

SELECT
  job, marital,
  {{ sec_to_min('duration') }} as duration_in_mins
FROM bank
WHERE duration_in_mins <= {{duration_slider}};
```

Finally, we have the option to display our query using the `%sqlrender` command as seen in the parameterizing your queries [section](https://ploomber-sql.readthedocs.io/en/latest/interactive-queries-and-parameterization/parameterize-sql-queries.html#macros-+-variable-expansion) section. Because we applied a widget to it, the `WHERE` clause in the rendered query will reflect the latest value of the slider UI, so you do not have to go back and forth!

```{code-cell} ipython3
final = %sqlrender convert
print(final)
```

## You try: Use JupySQL to perform the queries and answer the questions

### Question 1 (Easy):
Using the `bank` dataset, create an `IntSlider` widget called `balance_lower` for the `balance` column. Specifically, include a <b>bounded</b> slider with values ranging between -1000 and 20000, a step size of 1000, and initial value set to 10000. Show only the first 5 rows of the output.
<!-- #region -->
<details>

<summary>Answers</summary>

We start off by initializing a variable called `balance_lower` and assigning it to the `IntSlider` widget with the required <b>integer</b> arguments. To limit the number of rows to only 5, we <b>do not need a basic slider</b>, as shown with the `show_limit` variable in the Complete Example above.

```{code-cell} ipython3
balance_lower = widgets.IntSlider(min=-1000, max=20000, step=1000, value=10000)
```

```{code-cell} ipython3
%%sql --interact balance_lower 
SELECT * FROM bank 
WHERE balance <= {{balance_lower}} 
LIMIT 5
```

</details>
<!-- #endregion -->

<!-- #region -->

#### Question 2 (Medium):
Using the `bank` dataset, create a `ToggleButtons` Selection Widget for the `month` column. Show a range of records from 1 to 10 with a step size of 5.

<!-- #region -->
<details>

<summary>Answers</summary>

```{important}
When in doubt about the syntax of a particular widget, refer to the `ipywidgets` [documentation](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#selection-widgets).
```

We start off by initializing a variable called `month_toggle` and assigning it to the `ToggleButtons` widget. The `options` argument is set to a list of the unique values in the `month` column. We do not need to specify the `value` argument here as it will, by default, select the first value in the `options` list, which is "jan" in this case.

To show a range of records, we can modify the `show_limit` variable from the Complete Example above.

```{code-cell} ipython3
month_toggle = widgets.ToggleButtons(
    options=[
        "jan",
        "feb",
        "mar",
        "apr",
        "may",
        "jun",
        "jul",
        "aug",
        "sep",
        "oct",
        "nov",
        "dec",
    ],
    description="Month:",
    disabled=False,
)
show_limit = (1, 10, 5)
```

Finally, we use the `--interact` argument to create a UI for the `contact_dropdown` widget.

```{code-cell} ipython3
%sql --interact show_limit --interact month_toggle SELECT * FROM bank WHERE month == '{{month_toggle}}' LIMIT {{show_limit}} 
```

</details>
<!-- #endregion -->

<!-- #region -->

#### Question 3 (BONUS):
Create an <b>unbounded</b> numeric widget for the integer variable `duration` with a range of values from 0 to 2000, a step size of 500, and an initial `value` of 1000. <b>However</b>, make sure that the table changes output upon clicking a play button! Also add a `ToggleButton`, a Boolean Widget, for the variable `housing` that has `value` = "yes", `button_style` = "success", and a check `icon`. Lastly, limit the output to only show 10 records.

<b>Hint</b> Did you know that we can also create animated sliders for integer data types? This question requires exactly that! See the documentation [here](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#play-animation-widget) for more details.

<!-- #region -->
<details>
<summary>Answers</summary>

We start off by initializing a variable called `play` and assigning it to the `Play` Animation widget with the required <b>integer</b> arguments.

```{code-cell} ipython3
play = widgets.Play(
    value=0,
    min=0,
    max=2000,
    step=500,
    interval=1000,  # time interval in milliseconds
    description="Press play",
    disabled=False,
)
```

For the `ToggleButton` widget, we initialize a variable called `housing_toggle` and assign it to the `ToggleButton` widget with the required arguments.

```{code-cell} ipython3
housing_toggle = widgets.ToggleButtons(
    options=["yes", "no"],
    description="Housing:",
    disabled=False,
)
```

Before calling `--interact`, we need to add UI's for the `Play` and `IntSlider` widgets. This is attained with both `jslink()` and `HBox` `ipywidgets` methods. We then use the `--interact` argument to create the UI's. In the `WHERE` clause, because we want an <b>unbounded</b> slider, we use the `>=` operator for `duration`. To limit the number of rows to only 10, we <b>do not need a basic slider</b>.

```{code-cell} ipython3
%%sql --interact play --interact housing_toggle 
SELECT * FROM bank
WHERE duration >= {{play}} AND                                                         
housing == '{{housing_toggle}}' 
LIMIT 10
```

```{important}
Because we set the minimum value and initial value upon rendering to 0, the maximum value to 2000, and a step size of 500, the table will change or "blink" four times upon pressing the "play" button. Normally, an `IntSlider` is recommended to be added next to the `Play` widget; however, JupySQL does not support this at the moment.
```

</details>
<!-- #endregion -->

<!-- #region -->

#### Question 4 (Hard):
Consider the `pdays` variable from the bank marketing dataset. The value in this column is -1 when the client was not contacted since the previous campaign and an integer > 0 otherwise. The marketing manager wants you to create a macro named `dummify` that transforms this numeric variable into a binary categorical variable, named `pdays_dummy`, taking on either "no" if `pdays` = -1 or "yes" otherwise. You are also expected to create both a `RadioButtons` selection widget for the transformed `pdays_dummy` variable and a `SelectMultiple` selection widget for the `poutcome` variable to help the manager filter for campaign performance on the fly. Finally, output the rendered query after displaying the tabular results.

<b>Hint</b> Create the selection widgets first, making sure that no SQL statements are present in their code cells. Then, use `--save` for creating the macro and `--interact` for using the widgets. Make sure to account for both widgets in the `WHERE` clause!

<!-- #region -->
<details>
<summary>Answers</summary>

We start off by initializing our selection widget variables:

```{code-cell} ipython3
contact_selection = widgets.RadioButtons(
    options=["yes", "no"], description="Previously Contacted?", disabled=False
)
```

```{code-cell} ipython3
outcome_selection = widgets.SelectMultiple(
    options=["failure", "other", "success", "unknown"],
    value=["success", "failure"],
    description="Campaign Outcome:", 
    style= {'description_width': 'initial'},
    disabled=False,
)
```

Because we are creating a macro, we need to use the `--save` argument. The `--interact` argument initializes the UI for our widget variables. We then proceed to create the discretization macro function. Here, because we want to output "yes" or "no", using `::numeric(16, {{ precision }}` after the `CASE WHEN` statement will be incorrect; hence, we use `::varchar`.

The SQL query is then written in the same code-cell the macro is present in and the macro is called in the `SELECT` clause on the `pdays` variable, which is aliased as `pdays_dummy` for readability. The `poutcome` variable is present in both the `SELECT` and `WHERE` clauses to show it in the tabular output and to create the multiple selection widget for it respectively. Lastly, `pdays_dummy`  is used in the `WHERE` clause to create its radio button widget:

```{code-cell} ipython3
%%sql --save dummify --interact contact_selection --interact outcome_selection
{% macro days_to_dummy(column_name) %}
    (case when {{ column_name }} = -1 then 'no' else 'yes' end)::varchar
{% endmacro %}

SELECT
  job, marital, poutcome,
  {{ days_to_dummy('pdays') }} as pdays_dummy
FROM bank
WHERE poutcome IN {{outcome_selection}} AND
pdays_dummy == '{{contact_selection}}';
```

Finally, `%sqlrender` helps us display the query, accounting for the last chosen values in the widgets:

```{code-cell} ipython3
final = %sqlrender dummify
print(final)
```

</details>
<!-- #endregion -->

<!-- #region -->

## Wrapping Up

In this section, we learned about how to use JupySQL to create widgets with variable expansion and macros. To summarize:

- Numeric widgets, although commonly used as sliders, can also be used in text boxes or dropdowns, for example. This is useful when you want to specify a value.

- For categorical or text data, we can use either Selection or Boolean widgets. Some examples include radio buttons, toggle buttons, and dropdowns.

- `%sql --interact {{widget_variable}}` is a powerful tool in your arsenal to quickly create `ipywidgets`

- The main difference between the `%sql` and `%%sql` magic commands in Jupyter notebooks is that `%sql` only allows for a single statement to be executed, while `%%sql` allows a block of SQL to be executed. Make sure to use `%%sql` when creating macros!

- JupySQL provides incredible flexibility because it allows chaining `--` options, including `--save` and `--interact`, as we saw in this section. This helps us combine SQL queries with macros and widgets, making the EDA process less repetitive and more interactive!

This ends the Interactive Queries and Parameterization module. We hope you use these skills to boost your productivity in creating interactive queries! In the next module, we will introduce Advanced Querying Techniques.

<!-- #endregion -->

## References

“Simple Widget Introduction#.” Simple Widget Introduction - Jupyter Widgets 8.0.5 documentation, n.d. https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20Basics.html.

“Widget List#.” Widget List - Jupyter Widgets 8.0.5 documentation, n.d. https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html.
