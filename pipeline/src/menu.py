import ipywidgets as widgets
from ipywidgets import interact, widgets, Layout, VBox, HBox

style = {'description_width': 'initial'}

def setup_menu(all_the_widgets, func):
    # Button widget
    CD_button = widgets.Button(
        button_style='success',
        description="Fetch data", 
        layout=Layout(width='15%', height='30px'),
        style=style
    )
    CD_button.on_click( func )

    # user menu using categories found above
    tab3 = VBox(children=[HBox(children=all_the_widgets[0:2]),
                        HBox(children=all_the_widgets[2:4]),
                        HBox(children=all_the_widgets[4:]),
                            CD_button])
    tab = widgets.Tab(children=[tab3])
    tab.set_title(0, 'Choose Parameters')
    return tab


def init_widgets(years, makes, classes, vehicle_type, style):
    """Initialize widgets"""

    widget_vehicle_type = widgets.Dropdown(
            options=vehicle_type,
            description="Vehicle type",
            value='fuel-only',
            style=style,
        )

    widget_year = widgets.Combobox(
            options=years,
            description="Model Year",
            value='2023',
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
        description="Vehicle Class (range selection)",
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
        widget_co2
    )  # noqa E501

