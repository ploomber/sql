---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.5
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Intro to Voila

In this section, we will learn how to use the [`Voila`](https://voila.readthedocs.io/en/stable/index.html) Python library to create a dashboard from our SQL queries and visualizations. Additionally, we will explore how the [ETL](https://en.wikipedia.org/wiki/Extract,_transform,_load) process is integrated with the dashboard, examine the dashboard's structure and deployment, and discuss interesting insights gathered from it.

## What is Voila?

`Voila` is a Python library that allows users to effortlessly create standalone web applications from Jupyter notebooks. `Voila` takes the output of your notebook, while hiding code cells by default, and renders it in a web browser, so that you can share your work or use it in a production setting. With the help of [`ipywidgets`](https://ipywidgets.readthedocs.io/en/stable/index.html), we can transform the rendered web application into an interactive dashboard and this module does covers it in detail!

Moreover, `Voila` offers several ways to [customize](https://voila.readthedocs.io/en/stable/customize.html) your dashboard, including changing themes, creating templates, and controlling cell output. This allows you to create a visually aesthetic dashboard from a Jupyter notebook with minimal additional code! `Markdown` cells are also displayed in the dashboard, allowing you to add text and images to your dashboard.

[Install](https://github.com/voila-dashboards/voila) `Voila` with the following command:

```bash
pip install voila
```

## Questions to Answer in the Dashboard

The interactive dashboard contains 4 tables and 5 plots, created using `JupySQL`'s `ggplot` API, `seaborn`, and `ipywidgets`. It answers the following questions:

1. How do yearly manufacturing trends of fuel-only, electric, and hybrid cars compare?
2. How are fuel consumption and $CO2$ emissions distributed for all types of cars?
3. What is the relationship between charging time and travel range for electric vehicles by car size and model year?
4. How are $CO_2$ emissions distributed by vehicle type (fuel-only, electric, and hybrid) and fuel type (gasoline, diesel, ethanol, natural gas, and electricty)?
5. Which US fuel-only and hybrid car manufacturers emit the least $CO_2$ and how does this differ by transmission type?

## ETL and Voila

Recall the [ETL Pipeline](https://ploomber-sql.readthedocs.io/en/latest/packaging-your-sql-project/intro-to-etl-pipelines-with-python-and-sql.html) walkthrough in the previous module. The `datadownload.py` [script](https://github.com/ploomber/sql/blob/main/pipeline/src/datadownload.py) extracted, transformed, and loaded the car emissions data, as four tables (`fuel`, `electric`, `hybrid`, and `all_vehicles`) in an in-memory `DuckDB` database. Now, in our [`voila-app.ipynb` notebook](https://github.com/ploomber/sql/blob/main/pipeline/src/voila-app.ipynb) that serves as the dashboard's source, we can connect to the database and query the data to create our dashboard. This is done in the following code cell:

```python
%load_ext sql

%sql duckdb:///../data/database/car_data.duckdb
```

The `%sql` magic command allows us to connect to the database and query the data. The `duckdb:///` prefix specifies the database type and location. The `../data/database/car_data.duckdb` path specifies the location of the database relative to the notebook. The `%sql` magic command is used in the following code cells to create CTE's for generating visualizations.

<b>Note:</b> The `duckdb:///` prefix is not required if the database is in the same directory as the notebook.

## Dashboard Structure

### Introduction and Tables

The dashboard, firstly, needs to have a relevant title and description for the user to understand what the dashboard is about. The date the fuel emissions data was last updated is also displayed because the data is updated monthly and, accordingly, the tables and visualizations may have novel insights since the last update. Next, we display all the tables, integrated with `ipywidgets` and outputted from our ETL Pipeline, to allow the user interact with different columns in each table. The user can, hence, begin the EDA process by filtering columns to find interesting patterns and relationships.

Specifically, `SelectMultiple` and `IntSlider` widgets are employed to filter categorical columns, such as the car brand, model year, and vehicle size, and the $CO_2$ ratings column (a higher rating suggesting lower $CO_2$ emissions) respectively.

```{important}
During this process, it is essential to become acquainted with the various types of data present in each table, such as numerical, categorical, boolean, and others, before proceeding with data visualization. This familiarity aids the user in developing an intuition about the most suitable visualizations for emphasizing columns individually or exploring relationships between them.
```

### Questions Answered through Visualizations

After the user interacts with the tables, questions that the dashboard answers with the help of visualizations are then listed (see above). It is recommended to begin with simpler, more high-level questions about the data, such as addressing counts of different vehicle types or distributions of emissions, before diving into relationships between columns. This allows the user to make more informed decisions about the types of visualizations to use for answering more complex questions.

### Interactive Visualizations

#### `Seaborn` Bar Plots

The first visualization is a `barplot()`, built with `seaborn` and `ipywidgets`, of the number of unique fuel-only, electric, and hybrid car models, visualized across the years they were released. A trend overlay line (`pointplot()`) is added to clearly spot yearly manufacturing patterns in these vehicles. Interactivity is enabled through `RadioButtons`, which helps the user toggle between a bar plot of either fuel-only cars or a column chart of hybrid and electric cars. The decision to provide this separation is because fuel-only cars' models date back to 1995 in the dataset, while hybrid and electric cars' models date back to 2012. Therefore, the previous recommendation that the user should get familiar with the data before visualizing it is important here, which also assists in thinking about both the type of widget and where it could be utilized with respect to the data.

Lastly, notice that <b>two CTE's</b>, one that uses the `fuel` table for the fuel-only bar plot and another that uses the `all_vehicles` table for the electric and hybrid bar plot, were created and converted into `pandas` DataFrames to pass into our `seaborn` function that initializes the plots. From `ipywidgets`, the [`interact` function](https://ipywidgets.readthedocs.io/en/latest/examples/Using%20Interact.html), which takes as input the `seaborn` function and its parameter, is then called to visualize the plots with the `RadioButtons`. A basic example of the `interact` function is shown below:

```{code-cell} ipython3
def f(x):
    return x
interact(f, x=10);
```

Read the insights gained from this plot [below](https://ploomber-sql.readthedocs.io/en/latest/intro-to-dashboards-and-apps/connecting-etl-to-dashboard-with-voila.html#id1)

#### `ggplot` API Boxplot

To keep a user engaged and interested in your dashboard, it is important to use different libraries too along with visualizations and widgets. This dashboard also makes use of `JupySQL`s `ggplot` API, and the second visualization is a boxplot of fuel consumption and $CO_2$ emissions of all types of vehicles created from it. Recall this [example](https://ploomber-sql.readthedocs.io/en/latest/visualizing-your-sql-queries/plotting-with-ggplot.html#question-2-easy) from the Visualizing Your SQL Queries module.

The boxplots can be visualized either individually or together with the use of the `SelectMultiple` widget. There are three fuel consumption variables in the dataset, one for city driving, one for highway driving, and one for combined driving. The `SelectMultiple` widget allows the user to select one or more of these variables to visualize in the boxplot. However, the $CO_2$ emissions variable, `co2emissions_g_km`, is <b>measured in a different scale</b>, grams per kilometer, than the fuel consumption variables scale, liters per 100 kilometers. Therefore, <b>it is recommended to visualize `co2emissions_g_km` individually</b> to avoid confusion.

The process of building the boxplot is slightly different to the bar plot. A CTE is created from the `all_vehicles` table, but <b>not</b> converted into a `pandas` DataFrame because  the `ggplot` function takes in only a `SQL` table name, instead of a dataset. Then, the `SelectMultiple` widget is stored in a variable `columns` because it will be fed into the `ggplot` function as `x=columns` to select between the four filtered columns. Finally, the `interact` function is called to visualize the boxplot with the `SelectMultiple` widget.

Read the insights gained from this plot [below](https://ploomber-sql.readthedocs.io/en/latest/intro-to-dashboards-and-apps/connecting-etl-to-dashboard-with-voila.html#id2)

#### `Seaborn` Scatterplot

After answering some simple questions about the data, we can dive into unravelling complex relationships. The third visualization, therefore, is a seaborn `scatterplot()` to visualize the positive correlation between the recharge time and distance range of electric vehicles. Moreover, by including `hue`s, we can further explore the relationship between the recharge time and distance range of electric vehicles with respect to their size and the year of release. Note that both categorical variables, car size and model year, are discretized to avoid overplotting. If we recall the first bar plot, we saw an increasing rate of growth in unique electric car models between 2021 and 2023. Given this finding, it was feasible to discretize all electric cars' model year data into 2012-2021 and 2022-2023 to obtain a clear understanding of recent technological advancements in car battery and performance. Electric car size has nine unique categories, and are discretized into sedans (or smaller) and SUV's (or larger) to avoid overplotting.

Also, since we are visualizing more than one `hue`, a way to make this plot interactive is by adding a `Dropdown` widget to toggle between the size and model year hues. The `Dropdown` widget is also stored in a variable `hue` because it will be fed into the `scatterplot()` function as `hue=hue` to select between size or model year. Furthermore, we have added a `None` option in the `Dropdown` widget to remove the hue from the scatterplot.

Also notice that only a single CTE is created from the `electric` table and converted into a `pandas` DataFrame for the `scatterplot()` function. Like before, the `interact` function is called to visualize the scatterplot with the `Dropdown` widget.

Read the insights gained from this plot [below](https://ploomber-sql.readthedocs.io/en/latest/intro-to-dashboards-and-apps/connecting-etl-to-dashboard-with-voila.html#id3)

#### `ggplot` API Histogram

The boxplot of $CO_2$ emissions of all types of vehicles is a good starting point for exploring the distribution of $CO_2$ emissions. However, it is also important to visualize the distribution of $CO_2$ emissions by vehicle type (fuel-only, electric, and hybrid) and fuel type. Therefore, the fourth visualization is a `ggplot` histogram of $CO_2$ emissions of fuel-only cars, electric cars, and hybrid cars. This histogram is similar to the [example](https://ploomber-sql.readthedocs.io/en/latest/visualizing-your-sql-queries/plotting-with-ggplot.html#categorical-histogram-with-select-widget) from the Visualizing Your SQL Queries module. Three widgets, two Selection and an `IntSlider`, are employed for this visualization. The `RadioButtons` widget is used for mapping `fill` with either vehicle type or fuel type. The `Dropdown` widget allows the user to choose any of the five `cmap` options, which changes the color of the bars. The `IntSlider` allows selecting the number of bins, between 1 and 20, for the histogram. Unlike the boxplot, this visualization makes use of one CTE, created from the `all_vehicles` table.

Read the insights gained from this plot [below](https://ploomber-sql.readthedocs.io/en/latest/intro-to-dashboards-and-apps/connecting-etl-to-dashboard-with-voila.html#id4)

#### `Seaborn` Boxplot

The dataset contains five clean fuel (electric and hybrid) US car manufacturers. To assesses the cleanest, a (grouped) boxplot is visualized of $CO_2$ emissions by vehicle type and transmission type. Similar to the `scatterplot()` explained above, the `hue` attribute is integrated with a `Dropdown` widget to toggle between vehicle type, transmission type, or no `hue`. The seaborn `boxplot()` function and widget building process is also similar to the `scatterplot()` above.

Read the insights gained from this plot [below](https://ploomber-sql.readthedocs.io/en/latest/intro-to-dashboards-and-apps/connecting-etl-to-dashboard-with-voila.html#id5)

## Launching the Dashboard Locally

Whether your Jupyter Notebook is incomplete or complete, `Voila` will still be able to render it locally on the web! This will help you in prototyping your dashboard and fit it exactly to your needs. To launch the dashboard, run the following command in your terminal, given that you are in the same directory as the `dashboard.ipynb` file:

```bash
voila dashboard.ipynb
```

With that, you will see your Jupyter Notebook come to life as a dashboard!

## Dashboard Insights

The following insights were obtained from the dashboard and are also described in it:

### `Seaborn` Bar Plots

From the bar plot of fuel-only cars, we can see that the <b>number of unique car brand models</b> introduced to the Canadian automobile market had been increasing from the turn of the 21st century to the year 2005. This increasing trend then plateued and remained fairly constant until 2022, with 2015 experiencing the largest spike. On December 21, 2022, Steven Guilbeault, Canada's minister of environment and climate change, unveiled a regulation that would require increasing percentages of vehicle sales in Canada to be zero-emissions vehicles up to 100% by the year 2035[$^1$](https://www.canada.ca/en/environment-climate-change/news/2022/12/let-it-roll-government-of-canada-moves-to-increase-the-supply-of-electric-vehicles-for-canadians.html). These efforts seem to have had an immediate impact on the number of fuel-only cars introduced to the Canadian market, with 2023 experiencing a sharp decline and reaching 2003 levels.

The above insights are reinforced by the bar plot of the number of unique hybrid and electric car brands and their respective models introduced to the Canadian automobile market. In 2012, only two electric car models, Nissan's Leaf and Mitsubishi's i-MiEV, and one hybrid car manufacturer, Chevrolet's Volt, were present in the market. Since then, this figure has grown to 134 electric car models and 32 hybrid car models in 2023 in Canada.

### `ggplot` API Boxplot

The boxplots of fuel consumption, measured in litres per 100 kilometers, above show the distribution of fuel consumption in the city, highway, or as their combination for all types of cars. The median fuel consumption in the city for all cars is around 12 litres per 100 kilometers, while the median fuel consumption on the highway for all cars is around 10 litres per 100 kilometers. The combined fuel consumption for all cars is the vehicle's city's and highway's average fuel consumption, which is around 11 litres per 100 kilometers.

Fuel consumption and $CO2$ emissions have a strong, positive relationship. The higher the fuel consumption, the higher the $CO2$ emissions. The boxplot of $CO2$ emissions, measured in grams per kilometer, above shows the distribution of $CO2$ emissions for all types of cars. The median $CO2$ emission for all cars is around 250 grams per kilometer. Moreover, this column has outliers on either side of the boxplot, implying that electric cars have zero $CO2$ emissions and fuel-only luxury sports cars have very high $CO2$ emissions.

### `Seaborn` Scatterplot

The above scatterplot helps us compare the ranges and charging times of electric cars by their size or model year. Although one could deduce that higher recharge times (depending on the car's battery size, quality, etc.) would lead to travelling greater ranges, the graph offers more details that are worth exploring. For example, electric cars manufactured recently (2022 and onwards) have a much higher range, on average, than those manufactured between 2012 and 2021. This is likely due to the advancements in battery technology and the increased demand for electric cars. Moreover, some electric cars recently manufactured provide a better range with 10 hours of recharge time than those manufactured previously with 12 hours of recharge time. Furthermore, some new electric cars with recharge times of 10 hours provide as good a range as both new and older electric cars with recharge times greater than 10 hours (13 hours being the outlier). Maybe 10 hours is the sweet spot for recharge time?

If we shift our focus to vehicle size, there are more electric sedans (and smaller) than there are SUV's (and larger) for lower recharge times between 4 to 7 hours and this is expected due to the difference in car sizes. Sedans, on average, also seem to provide greater ranges than SUV's for recharge times greater than 7 hours. However, for recharge times less than 7 hours, SUV's provide greater ranges than sedans. This could be due to the fact that SUV's have larger batteries and, therefore, can travel greater ranges with less recharge time. Moreover, some sedans with 10 hours of recharge time provide better ranges than all SUV's do with greater than 10 hours of recharge time!

Therefore, consumers have a wide range of options to choose from when it comes to electric cars! Choosing wisely by assessing the tradeoff between recharge time and range is key and this graph helps us do just that.

### `ggplot` API Histogram

The histogram above represents the distribution of $CO_2$ emissions, measured in grams per kilometer. If we select the `fill` attribute to `vehicle_type`, we obtain a clear view that fuel-only cars emit the most $CO_2$. In fact, they can pollute up to 6x more than hybrid cars! Hybrid cars have both an electric motor and a gasoline engine, which allows them to emit less $CO_2$ than fuel-only cars. The range of $CO_2$ emitted from hybrid vehicles ranges between 10 to 80 grams per kilometer, while the distribution of $CO_2$ emissions for fuel-only cars ranges from 100 to 500 grams per kilometer, with the bulk of vehicles emitting between 200 to 300 grams per kilometer. Electric cars have zero carbon dixoide emissions and are, hence, fittingly also known as zero-emission vehicles.

Given these findings, the efforts of the Canadian government to increase the supply of electric vehicles in Canada by 2035[$^2$](https://www.canada.ca/en/environment-climate-change/news/2022/12/let-it-roll-government-of-canada-moves-to-increase-the-supply-of-electric-vehicles-for-canadians.html) will likely have a positive impact on the environment.

Selecting the `fill` attribute to `mapped_fuel_type` and adjusting the histogram to 12 bins allows us to see that the majority of vehicles in Canada run on gasoline, premium being more harmful to the environment than regular as it is the only fuel type that emits greater than 450 grams per kilometer in some cars. However, since most cars run on regular gasoline, the area occupied for it in the histogram is greater. Diesel and Ethanol (E85) are slightly cleaner than gasoline as their emissions range from 150 to 400 grams per kilometer with the bulk of vehicles emitting between 200 to 300 grams per kilometer (similar to both gasoline types).

### `Seaborn` Boxplot

The boxplots above show the distribution of $CO_2$ emissions for hybrid and fuel-only US manufactured cars. Viewing the boxplot at its highest level i.e without a `hue`, suggests that Chrysler has the lowest median $CO_2$ emission, at around 250 grams per kilometer, out of all car brands. Chevrolet, on the other hand, has the highest median $CO_2$ emission, at around 300 grams per kilometer, out of all car brands. Chrysler also has also the lowest interquartile range, which could imply that the $CO_2$ emissions of its cars are more consistent than those of other car brands.

However, upon selecting `hue` as `vehicle_type`, we see that Chevrolet's hybrid cars have the lowest median $CO_2$ emission out of all hybrid car brands. Yet, its fuel-only cars pollute the most on average. Jeep's hybrid cars pollute the most, on average, out of all US hybrid car brands, while its fuel-only cars' median $CO_2$ emissions are at par with that of Chrysler's, the cleanest fuel-only US brand.

Lastly, the boxplot of $CO_2$ emissions for hybrid and fuel-only US manufactured cars by transmission type portrays that continuously variable transmission cars pollute the least out of the other available transmissions. These cars would likely correspond to the hybrid cars of the US brands, which are the cleanest out of all hybrid cars. Another interesting observation is that all brands, apart from Chrysler, have lower median $CO_2$ emissions for manual transmission cars than for automatic transmission cars. In fact, the Environmental Protection Agency (EPA) found that vehicles with a manual transmission were more efficient than their automatic counterparts through about 2010, but modern automatic transmissions are now more efficient [$^3$](https://www.epa.gov/sites/default/files/2021-01/documents/420r21003.pdf). Only Ford has an automated manual transmission available for its cars, which has a significantly wide distribution for $CO_2$ emissions, similar to Cadillac's continuously variable transmissions cars, but a median $CO_2$ emission that is lower than that of its automatic transmission cars.