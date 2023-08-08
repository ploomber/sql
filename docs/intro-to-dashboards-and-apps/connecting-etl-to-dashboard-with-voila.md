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

# Intro to Voila

In this section, we will learn how to use the [`Voila`](https://voila.readthedocs.io/en/stable/index.html) Python library to create a dashboard from our SQL queries and visualizations. Additionally, we will explore how the [ETL](https://ploomber-sql.readthedocs.io/en/latest/packaging-your-sql-project/intro-to-etl-pipelines-with-python-and-sql.html) (<b>E</b>xtract, <b>T</b>ransform, <b>L</b>oad) - [EDA](https://ploomber-sql.readthedocs.io/en/latest/packaging-your-sql-project/etl-eda-pipeline-with-ploomber.html) (<b>E</b>xploratory <b>D</b>ata <b>A</b>nalysis) pipeline, introduced in the previous module, are integrated with the dashboard, examine the dashboard's structure and deployment, and discuss interesting insights gathered from it.

## What is Voila?

`Voila` is a Python library that allows users to effortlessly create standalone web applications from Jupyter notebooks. `Voila` takes the output of your notebook, while hiding code cells by default, and renders it in a web browser, so that you can share your work or use it in a production setting. With the help of [`ipywidgets`](https://ipywidgets.readthedocs.io/en/stable/index.html), we can transform the rendered web application into an interactive dashboard and this module does covers it in detail!

Moreover, `Voila` offers several ways to [customize](https://voila.readthedocs.io/en/stable/customize.html) your dashboard, including changing themes, creating templates, and controlling cell output. This allows you to create a visually aesthetic dashboard from a Jupyter notebook with minimal additional code! `Markdown` cells are also displayed in the dashboard, allowing you to add text and images to your dashboard.

[Install](https://github.com/voila-dashboards/voila) `Voila` with the following command:

```bash
!pip install voila
```

## Questions to Answer in the Dashboard

The interactive dashboard contains 4 tables and 5 plots, created using `JupySQL`'s `ggplot` API, `seaborn`, and `ipywidgets`. It answers the following questions:

1. How do yearly manufacturing trends of fuel-only, electric, and hybrid cars compare?
2. How are fuel consumption and $CO2$ emissions distributed for all types of cars?
3. What is the relationship between charging time and travel range for electric vehicles by car size and model year?
4. How are $CO_2$ emissions distributed by vehicle type (fuel-only, electric, and hybrid) and fuel type (gasoline, diesel, ethanol, natural gas, and electricty)?
5. Which US fuel-only and hybrid car manufacturers emit the least $CO_2$ and how does this differ by transmission type?

## ETL and Voila

Recall the [ETL Pipeline](https://ploomber-sql.readthedocs.io/en/latest/packaging-your-sql-project/intro-to-etl-pipelines-with-python-and-sql.html) walkthrough in the previous module. The [Ploomber pipeline](https://ploomber-sql.readthedocs.io/en/latest/packaging-your-sql-project/etl-eda-pipeline-with-ploomber.html) executes the `datadownload.py` ETL [script](https://github.com/ploomber/sql/blob/main/pipeline/src/datadownload.py) as well as the EDA Jupyter [notebook](https://github.com/ploomber/sql/blob/main/pipeline/src/eda-pipeline.ipynb) with selected queries. It then stores the tables in an in-memory DuckDB database. We can connect our dashboard to the DuckDB instance and generate queries for our visualizations. This is done in the following code cell:

```python
%load_ext sql

%sql duckdb:///../data/database/car_data.duckdb
```

The `%sql` magic command allows us to connect to the database and query the data. The `duckdb:///` prefix specifies the database type and location. The `../data/database/car_data.duckdb` path specifies the location of the database relative to the notebook. The `%sql` magic command is used in the following code cells to create CTE's for generating visualizations.

<b>Note:</b> The `../` prefix is not required if the database is in the same directory as the notebook.

The pipeline process entailed above can be better understood with the following diagram:

![ETL Pipeline](../packaging-your-sql-project/dashboard-comp.jpg)

## Dashboard Structure

### Introduction and Tables

The dashboard, firstly, needs to have a relevant title and description for the user to understand what the dashboard is about. The date the fuel emissions data was last updated is also displayed because the data is updated monthly and, accordingly, the tables and visualizations may have novel insights since the last update. Next, we display the interactive table, integrated with `ipywidgets` and outputted from our ETL Pipeline, to allow the user interact with numerical and categorical columns in each table (`fuel-only`, `hybrid`, and `electric`). The user can, hence, begin the EDA process by filtering columns to find interesting patterns and relationships.

Specifically, `SelectMultiple`, `Dropdown`, and `Combobox` widgets are employed to filter categorical columns, including the car's fuel type, size, model, and model year. Note that `Combobox`, which is a [String widget](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#combobox), was not introduced earlier in the course and we recommend taking a look at its documentation. The $CO_2$ ratings column (a higher rating suggesting lower $CO_2$ emissions) can also be filtered with the `IntSlider` widget. The aforementioned widgets and table are shown below:

```{code-cell} ipython3
:tags: [hide-output, hide-input]

import os
import sys

os.chdir("../../")

sys.path.append(os.path.join(os.getcwd(), "pipeline", "src"))

print(sys.path)

import ipywidgets as widgets
from ipywidgets import interactive_output, interact
from menu import init_widgets, style, setup_menu
from dashboard import (
    Seaborn_Barplot,
    Boxplot_ggplot,
    Seaborn_Scatter,
    Histogram_ggplot,
    Seaborn_Boxplot,
)
from IPython.display import display, clear_output
import pandas as pd
import numpy as np
from itables import init_notebook_mode, show
```

```{code-cell} ipython3
:tags: [hide-output, hide-input]

# flake8: noqa
init_notebook_mode(all_interactive=True)


def select_table(vehicle_type, year, vehicle_class, make, co2):
    query = f"""SELECT model_year,
                make_,
                model,
                vehicleclass_,
                vehicle_type
                co2_rating,
            FROM all_vehicles
            WHERE model_year = {year}
            AND vehicleclass_ IN {vehicle_class}
            AND vehicle_type = '{vehicle_type}'
            AND make_ = '{make}'
            AND co2_rating >= {co2}
            """

    print("Performing query")
    # Use JupySQL magic %sql to execute the query
    result = %sql {{query}}

    # Convert the result to a Pandas DataFrame
    df = result.DataFrame()

    clear_output(wait=True)

    show(df, classes="display nowrap compact")
```

```{code-cell} ipython3
:tags: [hide-output, hide-input]

%load_ext sql

%sql duckdb:///pipeline/data/database/car_data.duckdb

%config SqlMagic.displaycon = False
```

```{code-cell} ipython3
:tags: [hide-output, hide-input]

years = %sql select DISTINCT(model_year) from all_vehicles
years = [model_year[0] for model_year in years]

makes = %sql select DISTINCT(make_) from all_vehicles
makes = [m[0] for m in makes]

classes = %sql select DISTINCT(vehicleclass_) from all_vehicles
classes = [c[0] for c in classes]

co2 = %sql select DISTINCT(co2_rating) from all_vehicles where co2_rating is not null
co2 = [c[0] for c in co2]
# convert to int
co2 = [eval(c) for c in co2]

vehicle_type = %sql select DISTINCT(vehicle_type) from all_vehicles
vehicle_type = [v[0] for v in vehicle_type]
```

```{code-cell} ipython3
:tags: [hide-input]

(
    widget_vehicle_type,
    widget_year,
    widget_make,
    widget_vehicle_class,
    widget_co2,
) = init_widgets(years, makes, classes, vehicle_type, style)

tab = setup_menu(
    widget_vehicle_type, widget_year, widget_vehicle_class, widget_make, widget_co2
)  # noqa E501

output = interactive_output(
    select_table,  # noqa f821
    {
        "vehicle_type": widget_vehicle_type,
        "year": widget_year,
        "vehicle_class": widget_vehicle_class,
        "make": widget_make,
        "co2": widget_co2,
    },
)

display(tab, output)
```

```{important}
During this process, it is essential to become acquainted with the various types of data present in each table, such as numerical, categorical, boolean, and others, before proceeding with data visualization. This familiarity aids the user in developing an intuition about the most suitable visualizations for emphasizing columns individually or exploring relationships between them.
```

### Questions Answered through Visualizations

After the user interacts with the tables, questions that the dashboard answers with the help of visualizations are then listed (see [above](https://ploomber-sql.readthedocs.io/en/latest/intro-to-dashboards-and-apps/connecting-etl-to-dashboard-with-voila.html#questions-to-answer-in-the-dashboard)). It is recommended to begin with simpler, more high-level questions about the data, such as addressing counts of different vehicle types or distributions of emissions, before diving into relationships between columns. Doing so allows you to make informed decisions about the types of visualizations to use for answering complex questions.

### Interactive Visualizations

#### `Seaborn` Bar Plots

The first visualization is a `barplot()`, built with `seaborn` and `ipywidgets`, of the number of unique fuel-only, electric, and hybrid car models, visualized across the years they were released. Interactivity is enabled through `RadioButtons`, which helps the user toggle between a bar plot of either fuel-only cars or a column chart of hybrid and electric cars. The decision to provide this separation is because fuel-only cars' models date back to 1995 in the dataset, while hybrid and electric cars' models date back to 2012.

Notice that <b>two CTE's</b>, one that uses the `fuel` table for the fuel-only bar plot and another that uses the `all_vehicles` table for the electric and hybrid bar plot, were created and converted into `pandas` DataFrames to pass into our `barplot()` function that initializes the plots. The CTE's generated are shown below:

```{code-cell} ipython3
%%sql --save q_1_hybrid_electric
SELECT DISTINCT model_year, vehicle_type, COUNT(id) AS num_vehicles
FROM all_vehicles
WHERE vehicle_type = 'hybrid' OR vehicle_type = 'electric'
GROUP BY model_year, vehicle_type
ORDER BY num_vehicles DESC;
```

```{code-cell} ipython3
%%sql --save q_1_fuel
SELECT DISTINCT model_year, vehicle_type, COUNT(id) AS num_vehicles
FROM fuel
GROUP BY model_year, vehicle_type
ORDER BY model_year;
```

```{code-cell} ipython3
:tags: [hide-output, hide-input]

hybrid_electric_count = %sql SELECT * FROM q_1_hybrid_electric
fuel_count = %sql SELECT * FROM q_1_fuel

hybrid_electric_count = pd.DataFrame(hybrid_electric_count)
hybrid_electric_count = hybrid_electric_count.sort_values(by=["model_year"])
fuel_count = pd.DataFrame(fuel_count)
fuel_count = fuel_count.sort_values(by=["model_year"])
```

From `ipywidgets`, the [`interact` function](https://ipywidgets.readthedocs.io/en/latest/examples/Using%20Interact.html), which takes as input the `seaborn` function and its parameter, is then called to visualize the plots with the `RadioButtons`. A basic example of the `interact` function is shown below:

```{code-cell} ipython3
def f(x):
    return x


interact(f, x=10);
```

A preview of the barplot and its widgets are displayed below:

```{code-cell} ipython3
barplot = Seaborn_Barplot(fuel_count, hybrid_electric_count)
interact(barplot.draw_bar_year_count, data=barplot.radio_button)
```

##### Insights

The bar plot shows the <b>number of unique car brand models</b> for fuel-only cars in the Canadian market. It reveals an increasing trend until 2005, followed by a plateau until 2022. Notably, there was a significant spike in 2015. The introduction of regulations requiring higher percentages of zero-emissions vehicles seems to have influenced the market[$^1$](https://www.canada.ca/en/environment-climate-change/news/2022/12/let-it-roll-government-of-canada-moves-to-increase-the-supply-of-electric-vehicles-for-canadians.html), as 2023 experienced a sharp decline, reaching levels similar to those in 2003.

<b>Note:</b> To visualize the bar plot of the number of unique hybrid and electric car brands models, we recommend deploying the dashboard and interacting with the `RadioButtons`.

In 2012, only two electric car models, Nissan's Leaf and Mitsubishi's i-MiEV, and one hybrid car manufacturer, Chevrolet's Volt, were present in the market. Since then, this figure has grown to 134 electric car models and 32 hybrid car models in 2023 in Canada.

#### `ggplot` API Boxplot

To keep a user engaged and interested in your dashboard, it is important to use different libraries too along with visualizations and widgets. This dashboard also makes use of `JupySQL`s `ggplot` API for the second visualization, a boxplot of fuel consumption and $CO_2$ emissions of all types of vehicles. Recall this [example](https://ploomber-sql.readthedocs.io/en/latest/visualizing-your-sql-queries/plotting-with-ggplot.html#question-2-easy) from the Visualizing Your SQL Queries module.

The $CO_2$ emissions variable, `co2emissions_g_km`, is <b>measured in a different scale</b>, grams per kilometer, than the fuel consumption variables scale, liters per 100 kilometers. Therefore, <b>it is recommended to visualize `co2emissions_g_km` individually</b> to avoid confusion.

The process of building the boxplot is slightly different to the bar plot. A CTE is created from the `all_vehicles` table, but <b>not</b> converted into a `pandas` DataFrame because the `ggplot` function takes in only a `SQL` table name, instead of a dataset. The CTE is shown below:

```{code-cell} ipython3
%%sql --save boxplot_fuel_consum
SELECT fuelconsumption_city_l_100km::FLOAT as fuelconsumption_city_l_100km,
fuelconsumption_hwy_l_100km::FLOAT as fuelconsumption_hwy_l_100km,
fuelconsumption_comb_l_100km::FLOAT as fuelconsumption_comb_l_100km,
co2emissions_g_km::FLOAT as co2emissions_g_km
FROM all_vehicles
```

Then, the `SelectMultiple` widget is stored in a variable `columns`, to be passed in to the `ggplot` function as `x=columns` to select between the four filtered columns. Finally, the `interact` function is called to visualize the boxplot with the `SelectMultiple` widget. A preview of the boxplot and its widgets are displayed below:

```{code-cell} ipython3
boxplot = Boxplot_ggplot()
interact(boxplot.fuel_co2_boxplot, columns=boxplot.selection_button)
```

##### Insights

The boxplots above illustrate fuel consumption and $CO2$ emissions for various types of cars. The median fuel consumption in the city, on the highway, and combined (average) for all cars is approximately 12, 10, and 11 litres per 100 kilometers, respectively. There is a positive correlation between fuel consumption and $CO2$ emissions, with the median $CO2$ emission for all cars being around 250 grams per kilometer. Electric cars have <b>zero $CO2$ emissions</b>, while fuel-only luxury sports cars exhibit the highest $CO2$ emissions.

#### `Seaborn` Scatterplot

After answering some simple questions about the data, we can dive into unravelling complex relationships. The third visualization, therefore, is a seaborn `scatterplot()` to visualize the positive correlation between the recharge time and distance range of electric vehicles with respect to their size and the year of release.

The bar plot [above](https://ploomber-sql.readthedocs.io/en/latest/intro-to-dashboards-and-apps/connecting-etl-to-dashboard-with-voila.html#seaborn-bar-plots) indicates a rising number of unique electric car models from 2021 to 2023. To better analyze recent technological advancements in car battery and range, we grouped the data into two periods: 2012-2021 and 2022-2023. To avoid overplotting, electric car size is grouped into sedans (or smaller) and SUV's (or larger). Also, since we are visualizing more than one `hue`, a way to make this plot interactive is by adding a `Dropdown` widget to toggle between the size and model year hues.

A single CTE is created from the `electric` table and converted into a `pandas` DataFrame, which is passed into the `scatterplot()` function. The CTE is shown below:

```{code-cell} ipython3
%%sql --save electric_range_charge
SELECT range1_km, recharge_time_h, vehicleclass_, model_year
FROM electric
```

Like before, the `interact` function is called to visualize the scatterplot with the `Dropdown` widget, as shown below:

```{code-cell} ipython3
:tags: [hide-output, hide-input]

electric_range = %sql SELECT * FROM electric_range_charge

electric_range = pd.DataFrame(electric_range)

# convert model_year to int, range and recharge to float

electric_range["model_year"] = electric_range["model_year"].astype(int)
electric_range["range1_km"] = pd.to_numeric(
    electric_range["range1_km"], errors="coerce"
)
electric_range["recharge_time_h"] = pd.to_numeric(
    electric_range["recharge_time_h"], errors="coerce"
)

# group vehicle class into sedan or SUV

electric_range["vehicle_size"] = np.where(
    electric_range["vehicleclass_"].isin(
        ["subcompact", "compact", "mid-size", "full-size", "two-seater"]
    ),
    "Sedan or smaller",
    "SUV or larger",
)

# group model year into 2012-2021 and 2022-2023

electric_range["model_year_grouped"] = np.where(
    electric_range["model_year"] <= 2021, "2012-2021", "2022-2023"
)
```

```{code-cell} ipython3
scatter = Seaborn_Scatter(electric_range)
interact(scatter.draw_scatter_electric_range, hue=scatter.dropdown)
```

##### Insights

The scatterplot provides insights into electric cars' ranges and charging times based on their size and model year. Recent electric cars (manufactured from 2022 onwards) generally have a higher average range compared to those made between 2012 and 2021, likely due to advancements in battery technology and increased demand[$^2$](https://www.technologyreview.com/2023/01/04/1066141/whats-next-for-batteries/). Interestingly, some newer electric cars with a 10-hour recharge time offer better ranges than older cars with a 12-hour recharge time.

<b>Note:</b> To visualize this scatterplot by vehicle size, we recommend deploying the dashboard and interacting with the `Dropdown`.

Regarding vehicle size, there are more electric sedans (and smaller cars) than SUVs (and larger vehicles) with recharge times between 4 to 7 hours, as expected. Sedans also tend to offer greater ranges than SUVs for recharge times over 7 hours. However, for recharge times less than 7 hours, SUVs provide greater ranges, likely due to their larger batteries. Notably, some sedans with a 10-hour recharge time offer better ranges than all SUVs with recharge times exceeding 10 hours.

Therefore, consumers have diverse options when it comes to electric cars, and making an informed choice involves considering the tradeoff between recharge time and range. This scatterplot aids in understanding and assessing these factors for different electric car models.

#### `ggplot` API Histogram

The boxplot of $CO_2$ emissions of all types of vehicles is a good starting point for exploring the distribution of $CO_2$ emissions. Still, further insights can be drawn by visualizing the distribution of $CO_2$ emissions by vehicle type (fuel-only, electric, and hybrid) and fuel type. Therefore, the fourth visualization is a `ggplot` histogram of $CO_2$ emissions of fuel-only cars, electric cars, and hybrid cars. This histogram is similar to the [example](https://ploomber-sql.readthedocs.io/en/latest/visualizing-your-sql-queries/plotting-with-ggplot.html#categorical-histogram-with-select-widget) from the Visualizing Your SQL Queries module.

Three widgets, two Selection and an `IntSlider`, are employed for this visualization. The `RadioButtons` widget is used for mapping `fill` with either vehicle type or fuel type. The `Dropdown` widget allows the user to choose any of the five `cmap` options, which changes the color of the bars. The `IntSlider` allows selecting the number of bins for the histogram.

The CTE, created from the `all_vehicles` table, is shown below:

```{code-cell} ipython3
%%sql --save hist_co2
SELECT vehicle_type, mapped_fuel_type,
co2emissions_g_km::INTEGER as co2emissions_g_km
FROM all_vehicles
WHERE co2emissions_g_km is not null
```

A preview of the histogram and its widgets are displayed below:

```{code-cell} ipython3
histogram = Histogram_ggplot()
interact(
    histogram.co2_histogram,
    b=histogram.intslider,
    cmap=histogram.dropdown,
    fill=histogram.radio_button,
)
```

##### Insights

The histogram illustrates the distribution of $CO_2$ emissions (measured in grams per kilometer) for different vehicle or fuel types. Fuel-only cars emit the most $CO_2$, approximately 6 times more than hybrid cars, which combine an electric motor and a gasoline engine. Hybrid cars emit between 10 to 80 grams per kilometer, while fuel-only cars emit between 100 to 500 grams per kilometer, with the majority emitting between 200 to 300 grams per kilometer. In contrast, electric cars have zero $CO_2$ emissions and are fittingly known as zero-emission vehicles.

<b>Note:</b> To visualize this histogram by fuel type, we recommend deploying the dashboard and interacting with the `RadioButtons`.

Additionally, analyzing the histogram with the `mapped_fuel_type` attribute shows that most vehicles in Canada run on regular gasoline, with premium gasoline emitting greater than 450 grams per kilometer in some cars. Diesel and Ethanol (E85) vehicles emit slightly less $CO_2$ than gasoline, with emissions ranging from 150 to 400 grams per kilometer and the majority emitting between 200 to 300 grams per kilometer.

#### `Seaborn` Boxplot

The dataset contains five clean fuel (electric and hybrid) US car manufacturers. To assesses the cleanest, a grouped boxplot is visualized of $CO_2$ emissions by vehicle type and transmission type. Similar to the `scatterplot()` [above](https://ploomber-sql.readthedocs.io/en/latest/intro-to-dashboards-and-apps/connecting-etl-to-dashboard-with-voila.html#seaborn-scatterplot), the `hue` attribute is integrated with a `Dropdown` widget to toggle between vehicle type, transmission type, or no `hue`.

The CTE is shown below:

```{code-cell} ipython3
%%sql --save co2_usa
SELECT vehicle_type, make_, co2emissions_g_km, transmission_type
FROM all_vehicles
WHERE co2emissions_g_km is not null AND
vehicle_type IN ('fuel-only', 'hybrid') AND
make_ IN ('cadillac', 'chevrolet', 'chrysler', 'ford', 'jeep', 'lincoln')
```

A preview of the boxplot and its widgets are displayed below:

```{code-cell} ipython3
:tags: [hide-output, hide-input]

co2_usa = %sql SELECT * FROM co2_usa
co2_usa = pd.DataFrame(co2_usa)

# convert co2 to float

co2_usa["co2emissions_g_km"] = pd.to_numeric(co2_usa["co2emissions_g_km"])
```

```{code-cell} ipython3
boxplot = Seaborn_Boxplot(co2_usa)
interact(boxplot.draw_boxplot_usa, hue=boxplot.dropdown)
```

##### Insights

The boxplots depict the distribution of $CO_2$ emissions for hybrid and fuel-only cars manufactured in the US. Chrysler shows the lowest median $CO_2$ emission (around 250 grams per kilometer) among all car brands, indicating consistent emissions. Chevrolet, however, has the highest median $CO_2$ emission (around 300 grams per kilometer) among US car brands.

When considering the vehicle type, Chevrolet's hybrid cars have the lowest median $CO_2$ emission among all hybrid car brands. In contrast, Jeep's hybrid cars have the highest median $CO_2$ emission among US hybrid car brands. However, among fuel-only cars, Chrysler and Chevrolet have comparable median $CO_2$ emissions, with Chrysler being the cleanest.

<b>Note:</b> To visualize this boxplot by transmission type, we recommend deploying the dashboard and interacting with the `Dropdown`.

Moreover, continuously variable transmission (CVT) cars generally have the lowest $CO_2$ emissions among various transmission types. Hybrid cars from US brands, which are the cleanest among hybrids, often utilize CVT. With the exception of Chrysler, all brands have lower median $CO_2$ emissions for manual transmission cars compared to automatic transmission cars. This aligns with the EPA's findings [$^3$](https://www.epa.gov/sites/default/files/2021-01/documents/420r21003.pdf) that manual transmissions were more efficient than automatic transmissions until around 2010, but modern automatic transmissions have since improved in efficiency. Ford is the sole brand offering an automated manual transmission, which exhibits a wide distribution of $CO_2$ emissions similar to Cadillac's CVT cars, but its median $CO_2$ emission is lower than that of its automatic transmission cars.

## Launching the Dashboard Locally

Whether your Jupyter Notebook is incomplete or complete, `Voila` will still be able to render it locally on the web! This will help you in prototyping your dashboard and fit it exactly to your needs. Before launching, make sure you have satisfied the following requirements:

### Directory Structure

For this blog, we will assume the following directory structure:

```bash
├── environment.yml
├── pipeline
│   ├── src
│   │   ├── menu.py
│   │   ├── dashboard.py
│   │   ├── voila-app.ipynb
│   │   ├── datadownload.py
│   ├── data
│   │   ├── database
│   │   │   ├── car_data.duckdb
└── README.md
```

The [`voila-app.ipynb`](https://github.com/ploomber/sql/blob/main/pipeline/src/voila-app.ipynb) file in the `sql/pipeline/src` directory serves as our dashboard notebook. Additionally, all necessary files and modules, including the `menu.py` and `dashboard.py` files, are in the same directory as the notebook.

### Dependencies

 The `environment.yml` file in the root directory of this course contains the dependencies for the project. You can create a conda environment using that file and then activate the environment to run `voila-app.ipynb`, as shown below:

```bash
conda env create -f environment.yml
```

```bash
conda activate sql-course
```

### Running the Pipeline

If you have not already done so, you need to [build](https://ploomber-sql.readthedocs.io/en/latest/packaging-your-sql-project/intro-to-etl-pipelines-with-python-and-sql.html), [package](https://ploomber-sql.readthedocs.io/en/latest/packaging-your-sql-project/containerizing-etl-with-docker.html) and [run](https://ploomber-sql.readthedocs.io/en/latest/packaging-your-sql-project/etl-eda-pipeline-with-ploomber.html#defining-our-pipeline) the pipeline by following the steps outlined in the previous module.

After running the pipeline, you will have the `car_data.duckdb` database, under `sql/data/database`, ready to be queried by the dashboard. We can now launch the dashboard!

### Launching the Dashboard

To launch the dashboard, run the following command in your terminal, given that you are in the same directory as the `voila-app.ipynb` file:

```bash
voila voila-app.ipynb
```

With that, you will see your Jupyter Notebook come to life as a dashboard!

## References

${^1}$ Canada, Service. “Government of Canada.” Service Canada, n.d. https://www.canada.ca/.

${^2}$ Crownhart, Casey. “What’s next for Batteries.” MIT Technology Review, 5 Jan. 2023, www.technologyreview.com/2023/01/04/1066141/whats-next-for-batteries/.

${^3}$ The 2020 EPA Automotive Trends Report: Greenhouse gas emissions, fuel ..., n.d. https://www.epa.gov/sites/default/files/2021-01/documents/420r21003.pdf.

“Widget List#.” Widget List - Jupyter Widgets 8.0.5 documentation, n.d. https://ipywidgets.readthedocs.io/en/stable/examples/Widget List.html.

API reference - seaborn 0.12.2 documentation. (n.d.). https://seaborn.pydata.org/api.html

API Reference - Matplotlib 3.7.1 documentation. (n.d.). https://matplotlib.org/stable/api/index
