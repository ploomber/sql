from ipywidgets import widgets, VBox, HBox
import pandas as pd
import numpy as np

style = {"description_width": "initial"}


def setup_menu(
    widget_vehicle_type,
    widget_year,
    widget_vehicle_class,
    widget_make,
    widget_co2,  # noqa: E501
):
    """
    Setup the menu for the app

    Parameters
    ----------
    widget_vehicle_type : ipywidgets.Dropdown
        dropdown widget for vehicle type
    widget_year : ipywidgets.Combobox
        combobox widget for year
    widget_make : ipywidgets.Combobox
        combobox widget for make
    widget_vehicle_class : ipywidgets.SelectMultiple
        select multiple widget for vehicle class
    widget_co2 : ipywidgets.IntSlider
        int slider widget for CO2 rating


    Returns
    -------
    tab : ipywidgets.Tab
        tab object containing the menu
    """

    # user menu using categories found above
    tab3 = VBox(
        children=[
            HBox(children=[widget_vehicle_type, widget_year]),
            HBox(children=[widget_vehicle_class, widget_make]),
            HBox(children=[widget_co2]),
        ]
    )
    tab = widgets.Tab(children=[tab3])
    tab.set_title(0, "Choose Parameters")
    return tab


def init_widgets(years, makes, classes, vehicle_type, style):
    """Initialize widgets

    Parameters
    ----------
    years : list
        list of years
    makes : list
        list of car makes
    classes : list
        list of car classes
    vehicle_type : list
        list of vehicle types
    style : dict
        style dictionary for widgets

    Returns
    -------
    widget_vehicle_type : ipywidgets.Dropdown
        dropdown widget for vehicle type
    widget_year : ipywidgets.Combobox
        combobox widget for year
    widget_make : ipywidgets.Combobox
        combobox widget for make
    widget_vehicle_class : ipywidgets.SelectMultiple
        select multiple widget for vehicle class
    widget_co2 : ipywidgets.IntSlider
        int slider widget for CO2 rating

    """

    widget_vehicle_type = widgets.Dropdown(
        options=vehicle_type,
        description="Vehicle type",
        value="fuel-only",
        style=style,
    )

    widget_year = widgets.Combobox(
        options=years,
        description="Model Year",
        value="2023",
        style=style,
        description_tooltip="Select or type a year",
    )

    widget_make = widgets.Combobox(
        placeholder="Select or type a car brand",
        options=makes,
        value="acura",
        description="Car Brand",
    )

    widget_vehicle_class = widgets.SelectMultiple(
        options=classes,
        description="Vehicle Class",
        value=classes,
        style=style,
    )

    widget_co2 = widgets.IntSlider(
        value=5,
        min=0,
        max=10,
        step=1,
        description="CO2 Rating >=",
        disabled=False,
        style=style,
    )

    return (
        widget_vehicle_type,
        widget_year,
        widget_make,
        widget_vehicle_class,
        widget_co2,
    )  # noqa E501


def select_table(vehicle_type, year, vehicle_class, make, co2):
    """
    Select table based on vehicle type

    Parameters
    ----------
    vehicle_type : str
        Vehicle type (fuel-only, hybrid, or electric)
    year : int
        Model year
    vehicle_class : list
        Vehicle class (compact, midsize, etc.)
    make : str
        Car manufacturer
    co2 : int
        CO2 rating

    Returns
    -------
    df : DataFrame
        Filtered DataFrame
    """
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

    return query


def clean_electric_range(electric_range):
    """
    Cleans the electric range DataFrame.

    Parameters
    ----------
    electric_range : pd.DataFrame
        DataFrame containing electric range data.

    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame.
    """
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

    return electric_range
