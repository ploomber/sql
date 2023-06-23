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

# Introduction to `ipywidgets`

```{code-cell} ipython3
:tags: [remove-cell]

# this cell is hidden in the docs, only used to simulate
# the getpass() call
import ipywidgets as widgets
```
Welcome back! We hope you gained a solid introduction to SQL and JupySQL in the first module.

Before we begin, did you know that you can use widgets, eventful Python objects that have a representation in the browser, to build fully interactive GUIs for your SQL query?

In this section of Interactive Queries and Parameterization, we introduce `ipywidgets` and demonstrate how to create widgets and their functionality. Moreover, you can use widgets to synchronize stateful and stateless information between Python and JavaScript.

`ipywidgets`, which is part of the Jupyter Widgets project, is a Python package that provides interactive HTML widgets for Jupyter notebooks and the IPython kernel. The package provides a basic, lightweight set of controls that allows for easy implementations of interactive user interfaces. These controls comprise a text area, text box, select and multiselect controls, checkbox, sliders, tab panels, grid layout, etc.

See more for a complete [Widget List](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html)!

## `ipywidgets`

Let's start off with an easy introduction to the `ipywidgets` package.

First, install `ipywidgets` in your environment by executing the following code:

```{code-cell} ipython3
pip install ipywidgets --quiet
```

Next, import `ipywidgets` into your notebook:

```{code-cell} ipython3
import ipywidgets as widgets
```

The `ipywidgets` package is necessary to provide an interface for widgets. We introduce these widgets moving forward.

### Numeric Widgets

There are many widgets distributed with `ipywidgets` that are designed to display numeric values. Widgets exist for displaying integers and floats, both bounded and unbounded. The integer widgets share a similar naming scheme to their floating point counterparts. By replacing "Float" with "Int" in the widget name, you can find the Integer equivalent.

#### `IntSlider` and `FloatSlider`

Numeric widgets provide further flexibility over basic data types. For example, the `IntSlider` and the `FloatSlider`, the simplest numeric widgets, can be employed to filter <b>integer</b> and <b>float</b> values respectively within a range (`min` and `max`) of your choice along with a `step` size and the `value` at which the slider is initialized. Moreover, we can create a bounded slider, indicated by the `<=` operator, or an unbounded slider, indicated by the `>=` operator, to filter the dataset within or outside our range of values respectively.

There are several other arguments, which can be found [here](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#IntSlider), that can be passed into these sliders.

After creating a widget, you can display it using the `display()` function. An example for the `IntSlider` and its display is as follows:

```{code-cell} ipython3
duration_lower_bound = widgets.IntSlider(min=0, max=1000, step=200, value=500)
display(duration_lower_bound)
```

<b>Note</b>: Other Numeric Widgets can be found [here](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#floatlogslider).

### Boolean Widgets

Boolean widgets display interfaces specifically for boolean values. There are three available boolean widgets that all have the same functionality: `ToggleButton`, `Checkbox`, and `Valid`. Let's see how `Checkbox` works with an example.

#### `Checkbox`

`Checkbox` is a great boolean widget because it allows users to interact with a checkbox. We demonstrate its use below.

```{code-cell} ipython3
balance_over_500 = widgets.Checkbox(
    value=False, description="Balance > 500", disabled=False, indent=False
)
display(balance_over_500)
```

### Selection Widgets

There are several widgets that can be used to display single selection lists, and two that can be used to select multiple values. All inherit from the same base class. You can specify the <b>enumeration of selectable options by passing a list</b>. Options are either (label, value) pairs, or simply values for which the labels are derived by calling `str`.

#### `RadioButtons`

The `RadioButtons` widget displays a list of options, of which <b>exactly one</b> can be selected. The user can <b>select one of the options</b> by clicking on the radio button. The current selected value can be accessed from the `value` attribute, which is by default the label of the selected option.

We show an example of using a `RadioButton` below.

```{code-cell} ipython3
seasons = widgets.RadioButtons(
    options=["Spring", "Summer", "Fall", "Winter"],
    #    value='Spring', # Defaults to 'Spring'
    description="Season:",
    disabled=False,
)
display(seasons)
```

#### `Select` and `SelectMultiple`

The `Select` and `SelectMultiple` widgets display a dropdown menu where one or more options can be selected. These two widgets are very similar to `RadioButtons`. The main difference is the type of display they output and how `SelectMultiple` allow for more than one option to be selected by holding down "shift". 

Try out the differences between `Select` and `SelectMultiple` below.

```{code-cell} ipython3
one_season = widgets.Select(
    options=["Spring", "Summer", "Fall", "Winter"],
    description="Season:",
    disabled=False,
)
display(seasons)
```

```{code-cell} ipython3
multiple_season = widgets.SelectMultiple(
    options=["Spring", "Summer", "Fall", "Winter"],
    description="Season:",
    disabled=False,
)
display(seasons)
```

### Container/Layout Widgets

We can position multiple widgets in a single cell's output by utilizing container widgets. These container widgets' main functionality is to hold other widgets, called children. There are several ways to layout your widgets, but we solely demonstrate `VBox` below with our previous example.

#### `Vbox`

```{code-cell} ipython3
# The "children" widgets go into a list when used as an argument
widgets.VBox([one_season, multiple_season])
```

For more ways to layout your widgets, visit `ipywidgets` documentation [here](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#vbox).

## Applying `ipywidgets` with Functions

We can integrate `ipywidgets` with functions and see the outputs of functions in real time! For example, say we have a function that multiples variable `x` and `y`. We can create widgets for `x` and `y` and show outputs of our function every time we adjust either widgets.

To demonstrate this, we need to first understand some more `ipywidgets` fundamentals, such as `Output` and `.observe()`.

### `Output` and `.clear_output()`

`Output` is a widget that displays and handles cell outputs. We can use `Output` to have a certain cell act as the output for other widgets or functions.

```{code-cell} ipython3
out = widgets.Output()
display(out)
```

```{code-cell} ipython3
with out:
    for i in range(10):
        print(f"Output {i}")
```

We can clear the the above cell's output with `.clear_output()` attached to the `Output` widget.

```{code-cell} ipython3
out.clear_output()
```

### `.observe()`

`.observe()` is used to to register a function to an existing widget. By registering a function, the function is called whenever the widget's value changes.

## Putting It Together

Let's implement everything we've learned with the multiplication function using `ipywidgets`.

```{code-cell} ipython3
# Create the IntSlider widgets
x_slider = widgets.IntSlider(description="x:", min=0, max=10, value=5)
y_slider = widgets.IntSlider(description="y:", min=0, max=10, value=5)

# Create the Output widget
output = widgets.Output()

# Multiplication function


def multiply(x, y):
    return x * y


# Define a function to update the output when sliders are changed


def update_output(change):
    # Clear the Output widget every time the function is called
    output.clear_output()
    with output:
        result = multiply(x_slider.value, y_slider.value)
        print(f"{x_slider.value} * {y_slider.value} is: {result}")


# Register the update_output function for slider value changes
x_slider.observe(update_output)
y_slider.observe(update_output)

display(x_slider, y_slider, output)
```

A great alternative to the above code is using the `interact` function. The `interact` function automatically generates the appropriate widgets based on the task at hand. Below is an implementation of the same task with the `interact` function.

```{code-cell} ipython3
# Create the Output widget
output = widgets.Output()


@widgets.interact(x=(0, 10), y=(0, 10))
def multiply(x, y):
    # Clear the Output widget every time the function is called
    output.clear_output()
    with output:
        result = x * y
        print(f"{x_slider.value} * {y_slider.value} is: {result}")


display(output)
```

Notice all the changes from using the `interact` function. We no longer explicitly create `x` and `y` with widgets. Instead, a range of them are given when using the `@widgets.interact()` decorator that is defined above the associated function.

## Wrapping Up 

In this section we introduced `ipywidgets` and how they provide user interfaces within Jupyter environments. In the upcoming sections, we will delve back into SQL by showcasing how we can utilize `ipywidgetes` to create interactive queries. Further along the course, we will also revisit `ipywidgets` to demonstrate how they can be used to create interactive visualizations.
