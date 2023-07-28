from ipywidgets import widgets, VBox, HBox

style = {"description_width": "initial"}


def setup_menu(
    widget_vehicle_type, widget_year, widget_vehicle_class, widget_make, widget_co2
):  # noqa E501
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
