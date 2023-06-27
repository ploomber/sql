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

This module will teach you the `seaborn` and `plotly` packages. Before we get into the details of each package, we first introduce the common types of data visualization with one of the most basic visualization packages: `matplotlib`. The purpose of this section is to not teach you the ins and outs of `matplotlib`, but more so to introduce some basic data visualizations. 

## Getting started

Let's first create a toy dataset. This dataset will be in the perspective of a boutique produce store in Southern California that wants to analyze their purchase data. Run the cell below to load the data.

```{code-cell} ipython3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# random seed for reproducibility
np.random.seed(42)

# number of rows in our toy dataset
num_rows = 100

# list of cities
cities = ['Irvine', 'Los Angeles', 'Venice', 'San Diego', 'Long Beach']

# list of fruits
fruits = ['strawberries', 'blueberries', 'bananas', 'apples', 'kiwis']

# type of fruits
fruit_type = ['organic', 'conventional']

# prices of each fruit by type
prices = {'organic': {'strawberries': 4,
                      'blueberries': 3.75,
                      'bananas': 1,
                      'apples': 1.25,
                      'kiwis': 2},
          'conventional': {'strawberries': 3.25,
                      'blueberries': 3,
                      'bananas': .75,
                      'apples': 1,
                      'kiwis': 1.50}}

time_of_day = ['morning', 'noon', 'evening']

# random customer IDs
customer_ids = np.random.choice(range(1, 21), size=num_rows)

# random customer cities
customer_cities = np.random.choice(cities, size=num_rows)

# random customer purchases
customer_purchases = np.random.choice(fruits, size=num_rows)

# random purchase counts
purchase_counts = np.random.randint(1, 10, size=num_rows)

fruit_type = np.random.choice(fruit_type, size = num_rows)

# total purchase amount
purchase_total = [prices[purchase[1]][purchase[0]] * purchase[2] for purchase in zip(customer_purchases, fruit_type, purchase_counts)]

time_bought = np.random.choice(time_of_day, size = num_rows)

# create a pandas DataFrame
df = pd.DataFrame({
    'customer_id': customer_ids,
    'customer_city': customer_cities,
    'customer_purchase': customer_purchases,
    'fruit_type': fruit_type,
    'purchase_count': purchase_counts,
    'purchase_total': purchase_total,
    'time_bought': time_bought
})

# display the data
df
```

Each row of this dataset represents a purchase. The variables are defined as follows:

- customer_id: customer's unique id
- customer_city: where the customer resides
- customer_purchase: what fruit the customer purchased
- fruit type: if the fruit(s) they purchased were organic or conventional
- purchase_count: the amount of fruit they purchased
- purchase_total: the total amount of their purchase
- time_bought: the time of purchase

Let's now jump into one of the most simple, yet essential, data visualizations: the bar plot.

## Bar Plot

```{code-cell} ipython3
# determines how large the plot will be
plt.figure(figsize=(10, 6))

# get the counts of each unique city
city_counts = df.customer_city.value_counts()
plt.bar(city_counts.index, city_counts.values)

plt.xlabel('City')
plt.ylabel('Count')
plt.title('Count of Customer by City Origin')
```

The first three lines in the above code cell is really all we need to create a baseline bar plot. The last three lines are supplemental elements that labels the y-axis, x-axis, and title of the plot. We can easily see that the city where most customers come from are from Irvine. Box plots are a great option when you need to visualize distributions of groups in categorical variables.

## Scatter Plot

```{code-cell} ipython3
plt.figure(figsize=(10, 6))

plt.scatter(df.purchase_count, df.purchase_total)

plt.xlabel('Purchase Count')
plt.ylabel('Total Purchase Amount')
plt.title('Scatter Plot of Purchase Count by Total Purchase Amount')
```

Scatter plots are great when analyzing the relationship between two numerical variables. In this example, we plot the relationship between the amount of fruits a customer buys and their total purchase amount. This plot shows a positive relationship between these two variables, which is expected.

## Box Plot
```{code-cell} ipython3
# group the data by 'time_bought'
grouped_data = df.groupby('time_bought')['purchase_total'].apply(list)

# create a list of purchase_total values for each time_bought category
data = [grouped_data[time_bought] for time_bought in ['morning', 'noon', 'evening']]

plt.figure(figsize=(10, 6))
plt.boxplot(data)

# customize x-axis tick labels
plt.xticks(range(1, len(data) + 1), ['Morning', 'Noon', 'Evening'])

plt.xlabel('Time Bought')
plt.ylabel('Purchase Total')
plt.title('Boxplot of Purchase Total by Time Bought')

plt.show()
```

Box plots can be used when examining the relationship between a categorical feature and a numerical feature. In this plot, our categorical feature is the `time_bought` variable. Each box represents a group within `time_bought` and their respective purchase totals in quantiles. This allows for a quick comparison of the distribution of groups within this categorical variable.

## Heat Map

```{code-cell} ipython3
heatmap_data = df.pivot_table(index='customer_city', columns='customer_purchase', values='purchase_count', aggfunc='sum', fill_value=0)

plt.figure(figsize=(10, 6))
heatmap = plt.pcolor(heatmap_data, cmap='YlGnBu')
plt.colorbar(heatmap)
plt.title('Purchase Counts by City and Fruit Type')
plt.xlabel('Customer Purchase')
plt.ylabel('Customer City')

# customize tick labels
plt.xticks(np.arange(heatmap_data.shape[1]) + 0.5, heatmap_data.columns, rotation=45)
plt.yticks(np.arange(heatmap_data.shape[0]) + 0.5, heatmap_data.index)

plt.show()
```

The above plot displays the purchase counts given the customer's city of residence and what they purchased. Heat maps are generally easy to understand because viewers can quickly point out extremes based on darker or lighter boxes. Here, we easily see that the highest purchase count by city origin and fruit type are customers from Irvine who buy bananas. You can think of heat maps as illustrating three dimensions: the x-axis, the y-axis, and the color gradient (which is usually a numerical feature).

## Wrapping Up

In this section, we introduced some basic data visualization plots: bar plots, scatter plots, box plots, and heat maps. The sections moving forward will teach you how to implement each of these plots using the `seaborn` and `plotly` libraries using the familiar banking data sets from the previous modules.