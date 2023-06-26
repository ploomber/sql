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

In this section, we will combine the learnings from the two previous sections, [Intro to `ipywidgets`](https://ploomber-sql.readthedocs.io/en/latest/interactive-queries-and-parameterization/introduction-to-ipywidgets.html) and [Parameterizing SQL Queries](https://ploomber-sql.readthedocs.io/en/latest/interactive-queries-and-parameterization/parameterize-sql-queries.html), to create interactive SQL queries using JupySQL. This technique is useful for exploratory data analysis, as it allows us to filter our data and visualize the tabular results interactively.

```{code-cell} ipython3
:tags: [remove-cell]

# this cell is hidden in the docs for linting
import ipywidgets as widgets
```

The installation of `ipywidgets` was covered previously [here](https://ploomber-sql.readthedocs.io/en/latest/interactive-queries-and-parameterization/introduction-to-ipywidgets.html#ipywidgets).

## Load Engine

We will load in our SQL extension and DuckDB that allow us to execute SQL queries in Jupyter Notebooks.

```{code-cell} ipython3
# Loading in SQL extension
%reload_ext sql
# Initiating a DuckDB database named 'bank.duck.db' to run our SQL queries on
%sql duckdb:///bank.duck.db
```

## Creating Table

We will be using the [bank marketing data](https://ploomber-sql.readthedocs.io/en/latest/intro-to-sql/making-your-first-query.html#dataset) as we have been in previous sections. Downloading it was covered previously [here](https://ploomber-sql.readthedocs.io/en/latest/intro-to-sql/aggregate-functions-in-sql.html#load-the-data). Let's start off with loading our `bank_cleaned.csv` file from our local directory to our newly created DuckDB database.

```{code-cell} ipython3
%%sql
CREATE OR REPLACE TABLE bank AS
FROM read_csv_auto('bank_cleaned.csv', header=True, sep=',')
```

## `%sql --interact {{widget_variable}}`

First, you need to define the variable as the form of a basic data type or `ipywidgets` Widget.
Then, pass the variable name into the `--interact` argument and use a `WHERE` clause to filter using the specified widgets variables. In this section, we shall delve into the different types of widgets and how to use them.

### Basic Data Types

The simplest way is to declare a variable with basic data types (Numeric, Text, Boolean...). [ipywidgets](https://ipywidgets.readthedocs.io/en/stable/examples/Using%20Interact.html?highlight=interact#Basic-interact) autogenerates UI controls for that variable.

An example with a numeric variable `duration`, which creates a slider for its values as a UI, is as follows:

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

There are many widgets distributed with `ipywidgets` that are designed to display numeric values. Widgets exist for displaying integers and floats, both bounded and unbounded. The integer widgets share a similar naming scheme to their floating point counterparts. By replacing "Float" with "Int" in the widget name, you can find the Integer equivalent.

#### `IntSlider` and `FloatSlider`

Numeric widgets provide further flexibility over basic data types. For example, the `IntSlider` and the `FloatSlider`, the simplest numeric widgets, can be employed to filter <b>integer</b> and <b>float</b> values respectively within a range (`min` and `max`) of your choice along with a `step` size and the `value` at which the slider is initialized. Moreover, we can create a bounded slider, indicated by the `<=` operator, or an unbounded slider, indicated by the `>=` operator, to filter the dataset within or outside our range of values respectively.

There are several other arguments, which can be found [here](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#IntSlider), that can be passed into these sliders.

An example for the `IntSlider` is as follows:

```{code-cell} ipython3
duration_lower_bound = widgets.IntSlider(min=5, max=3000, step=500, value=1500)

%sql --interact duration_lower_bound SELECT * FROM bank WHERE duration <= {{duration_lower_bound}} LIMIT 5
```

<b>Note</b>: Other Numeric Widgets can be found [here](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#floatlogslider).

### Selection Widgets

There are several widgets that can be used to display single selection lists, and two that can be used to select multiple values. All inherit from the same base class. You can specify the <b>enumeration of selectable options by passing a list</b>. Options are either (label, value) pairs, or simply values for which the labels are derived by calling `str`.

#### `RadioButtons`

The `RadioButtons` widget displays a list of options, of which <b>exactly one</b> can be selected. The user can <b>select one of the options</b> by clicking on the radio button. The current selected value can be accessed from the `value` attribute, which is by default the label of the selected option.

An example is as follows:

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
LIMIT 5
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
<!-- #region -->
<details>
<summary>Answers</summary>

<b>Hint</b> Did you know we can also create animated sliders for integer data types? This question requires exactly that! See the documentation [here](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#play-animation-widget) for more details.

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

+++

</details>
<!-- #endregion -->

<!-- #region -->

## Wrapping Up

In this section, we learnt about how to create widgets to make our SQL queries interactive, helping us gain a better intuition of the EDA process! To summarize:

- Numeric widgets, although commonly used as sliders, can also be used in text boxes or dropdowns, for example. This is useful when you want to specify a value.

- For categorical or text data, we can use either Selection or Boolean widgets. Some examples include radio buttons, toggle buttons, and dropdowns.

In the next section, you will learn how to parameterize your queries.

<!-- #endregion -->

## References

“Simple Widget Introduction#.” Simple Widget Introduction - Jupyter Widgets 8.0.5 documentation, n.d. https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20Basics.html.

“Widget List#.” Widget List - Jupyter Widgets 8.0.5 documentation, n.d. https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html.


