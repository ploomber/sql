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

# Introduction to the dataset and problem: CO2 emissions of vehicles

To help consumers in Canada find fuel-efficient vehicles, the Government of Canada released a [fuel consumption ratings search tool](https://fcr-ccc.nrcan-rncan.gc.ca/en?_gl=1*1y4enqn*_ga*NzI2ODg1Njg2LjE2NjcyNDA3NTU.*_ga_C2N57Y7DX5*MTY2ODYzOTkyMy40LjAuMTY2ODYzOTkyMy4wLjAuMA). 

In it, they provide users the ability to search vehicles by model, class and make and obtain information on the fuel consumption of various vehicles in three settings: city, highway and combined. Vehicles undergo 2-cycle and 5-cycle fuel consumption in each of these settings, and a co2 emissions score is assigned to the vehicle (for more information see [here](https://www.nrcan.gc.ca/energy-efficiency/transportation-alternative-fuels/fuel-consumption-guide/understanding-fuel-consumption-ratings/fuel-consumption-testing/21008) and here[https://www.nrcan.gc.ca/energy-efficiency/transportation-alternative-fuels/personal-vehicles/choosing-right-vehicle/buying-electric-vehicle/understanding-the-tables/21383]). 

Additionally, they provide access through their [open data portal](https://open.canada.ca/data/en/dataset/98f1a129-f628-4ce4-b24d-6f16bf24dd64) as part of the [Open Government License Canada](https://open.canada.ca/en/open-government-licence-canada). 

While this tool allows consumers to obtain information via the website, it is recommended to develop an automated approach to extract information on the most recent vehicle models and analyze the data to answer important questions:

1. What is the average CO2 emissions of vehicles by class, make and model?
2. Which vehicles are better suited for different driving scenarios (city, highway, and combined) with a focus on lower CO2 emissions?
3. Can we identify trends in car manufacturing based on the number of vehicles produced per model year or by vehicle class (size) for different fuel types (gas, hybrid, and electric)?
4. How can fuel efficiency be analyzed for different fuel types (gas, hybrid, and electric)?
5. What are benefits of using hybrid vehicles over non-hybrid vehicles?

In the next sections, we will explore how we can combine Python and SQL to answer these questions. We will learn how to automate the process of extracting the data, cleaning it and setting up an Extract Transform Load (ETL) pipeline to load the data into a database. We will then learn how to use SQL to answer the questions like the ones above. 

## The dataset

Source: Open Canada Portal
Title: Fuel consumption ratings
Link: https://open.canada.ca/data/en/dataset/98f1a129-f628-4ce4-b24d-6f16bf24dd64
Format: metadata (API), CSV files

The metadata contains information in English and French, and points at links with CSV files containing information on fuel-based, electric and hybrid vehicles by year, make, model, along with their results for city, highway and combined fuel consumption tests for 2-cycle and 5-cycle tests.

## The problem

As the data is refreshed on a regular basis, the goal is to develop a workflow that eases the process of extracting the data, cleaning it and loading it into a database for exploration and analysis.

## Approach

We will use the `requests` library to extract the metadata. We will then use `pandas` to process the content of each file, perform data cleaning, and load the data into a `DuckDB` database with `sqlalchemy`.

For the analysis, we will then use `SQL` to answer the questions above and `JupySQL`' functionality to perform exploratory data analysis, save interesting queries into the database, and later reuse these tables in the form of a dashboard. 

In the next section, we will dive into the process of extracting the data and cleaning it through Python scripting. We will explore how to use `requests` to extract the metadata, and how to use `pandas` to process the content of each file, perform data cleaning, and load the data into a `DuckDB` database with `sqlalchemy`. Furthermore, we will explore how to write clean and reusable functions to ensure our process can be maintained. 

