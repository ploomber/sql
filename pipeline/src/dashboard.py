import ipywidgets as widgets

import matplotlib.pyplot as plt
import seaborn as sns

from sql.ggplot import ggplot, aes, geom_boxplot, geom_histogram


class Seaborn_Barplot:
    """
    This class creates a radio button widget to select the data to be plotted.

    Attributes
    ----------
    fuel_count : pandas.DataFrame
        dataframe containing the count of unique fuel-only cars by model year
    hybrid_electric_count : pandas.DataFrame
        dataframe containing the count of unique hybrid and electric cars by
        model year

    Methods
    -------
    create_radio_button()
        Creates a radio button widget to select the data to be plotted.
    draw_bar_year_count(data)
        Draws a bar plot of the count of unique fuel-only cars by model year
        or the count of unique hybrid and electric cars by model year.

    """

    def __init__(self, fuel_count, hybrid_electric_count):
        self.fuel_count = fuel_count
        self.hybrid_electric_count = hybrid_electric_count
        self.create_radio_button()

    def create_radio_button(self):
        self.radio_button = widgets.RadioButtons(
            options=["fuel_count", "hybrid_electric_count"],
            description="Select Data:",
            disabled=False,
            style={"description_width": "initial"},
        )

    def draw_bar_year_count(self, data):
        sns.set()  # Set the Seaborn style
        plt.figure(figsize=(10, 5), dpi=150)

        if data == "fuel_count":
            sns.barplot(
                data=self.fuel_count,
                x="model_year",
                y="num_vehicles",
                color="orange",
                errorbar=None,
                width=0.4,
            )
            sns.pointplot(
                data=self.fuel_count,
                x="model_year",
                y="num_vehicles",
                color="red",
                linestyles="--",
                errorbar=None,
            )
            plt.xlabel("Car Model Year")
            plt.ylabel("Count")
            plt.xticks(rotation=45)
            plt.title("Count of Unique Fuel-Only Cars by Model Year")
            plt.show()

        else:
            sns.barplot(
                data=self.hybrid_electric_count,
                x="model_year",
                y="num_vehicles",
                hue="vehicle_type",
                palette={"hybrid": "blue", "electric": "green"},
                width=0.4,
            )
            sns.pointplot(
                data=self.hybrid_electric_count,
                x="model_year",
                y="num_vehicles",
                color="red",
                linestyles="--",
                errorbar=None,
            )
            plt.xlabel("Car Model Year")
            plt.ylabel("Count")
            plt.xticks(rotation=45)
            plt.title("Count of Unique Hybrid and Electric Cars by Model Year")
            plt.legend(bbox_to_anchor=(0.75, 1), loc="upper left")
            plt.show()


class Boxplot_ggplot:
    """
    This class creates a widget to select the column(s) to be plotted.

    Attributes
    ----------
    selection_button : ipywidgets.SelectMultiple
        Widget to select the column(s) to be plotted.

    Methods
    -------
    create_selection_button()
        Creates a widget to select the column(s) to be plotted.
    fuel_co2_boxplot(columns)
            Draws a boxplot of the fuel consumption and CO2 emissions
            by column(s).
    """

    def __init__(self):
        self.create_selection_button()

    def create_selection_button(self):
        self.selection_button = widgets.SelectMultiple(
            options=[
                "fuelconsumption_city_l_100km",
                "fuelconsumption_hwy_l_100km",
                "fuelconsumption_comb_l_100km",
                "co2emissions_g_km",
            ],
            value=["fuelconsumption_comb_l_100km"],
            description="Column(s):",
            disabled=False,
        )

    def fuel_co2_boxplot(self, columns):
        # plt.rcParams["figure.figsize"] = (12, 3)

        (
            ggplot(
                table="boxplot_fuel_consum",
                with_="boxplot_fuel_consum",
                mapping=aes(x=columns),
            )
            + geom_boxplot()
        )


class Seaborn_Scatter:
    """
    This class creates a dropdown widget to select the hue of the
    scatter plot.

    Attributes
    ----------
    electric_range : pandas.DataFrame
        dataframe containing the electric vehicle range and recharge time
    create_dropdown : ipywidgets.Dropdown
        Widget to select the hue of the scatter plot.

    Methods
    -------
    create_dropdown()
        Creates a dropdown widget to select the hue of the scatter plot.
    draw_scatter_electric_range(hue)
        Draws a scatter plot of the electric vehicle range and recharge
        time by hue.
    """

    def __init__(self, electric_range):
        self.electric_range = electric_range
        self.create_dropdown()

    def create_dropdown(self):
        self.dropdown = widgets.Dropdown(
            options=["vehicle_size", "model_year_grouped", None],
            description="(Un)select Hue:",
            disabled=False,
            style={"description_width": "initial"},
        )

    def draw_scatter_electric_range(self, hue):
        plt.figure(figsize=(10, 5), dpi=150)
        sns.scatterplot(
            data=self.electric_range,
            x="recharge_time_h",
            y="range1_km",
            hue=hue,  # noqa: E501
        )
        plt.title(
            f"Scatter Plot of Electric Vehicle Range and Recharge Time by {hue}"  # noqa: E501
        )
        plt.xlabel("Recharge Time (hrs)")
        plt.ylabel("Range (km)")


class Histogram_ggplot:
    """
    This class creates a widget to select the column to be plotted.

    Methods
    -------
    create_intslider()
        Creates a widget to select the number of bins.
    create_dropdown()
        Creates a widget to select the colormap.
    create_radio_button()
        Creates a widget to select the column to be plotted.
    co2_histogram(b, cmap, fill)
        Draws a histogram of the CO2 emissions by column.

    """

    def __init__(self):
        self.create_intslider()
        self.create_dropdown()
        self.create_radio_button()

    def create_intslider(self):
        self.intslider = widgets.IntSlider(
            value=10,
            min=1,
            max=20,
            step=1,
            description="Bins:",
            orientation="horizontal",
        )

    def create_dropdown(self):
        self.dropdown = widgets.Dropdown(
            options=["viridis", "plasma", "inferno", "magma", "cividis"],
            value="plasma",
            description="Colormap:",
            disabled=False,
        )

    def create_radio_button(self):
        self.radio_button = widgets.RadioButtons(
            options=["vehicle_type", "mapped_fuel_type"],
            description="Fill by:",
            disabled=False,
        )

    def co2_histogram(self, b, cmap, fill):
        """
        Draws a histogram of the CO2 emissions by column.

        Parameters
        ----------
        b : int
            Number of bins.
        cmap : str
            Colormap.
        fill : str
            Column to be plotted.
        """
        (
            ggplot(
                table="hist_co2",
                with_="hist_co2",
                mapping=aes(x="co2emissions_g_km"),
            )
            + geom_histogram(bins=b, fill=fill, cmap=cmap)
        )


class Seaborn_Boxplot:
    """
    This class creates a dropdown widget to select the hue of the boxplot.

    Attributes
    ----------
    co2_usa : pandas.DataFrame
        dataframe containing the CO2 emissions by US car make,
        gas and hybrid run

    Methods
    -------
    create_dropdown()
        Creates a dropdown widget to select the hue of the boxplot.
    draw_boxplot_usa(hue)
        Draws a boxplot of the CO2 emissions by US car make, gas and
        hybrid run by hue.
    """

    def __init__(self, co2_usa):
        self.co2_usa = co2_usa
        self.create_dropdown()

    def create_dropdown(self):
        self.dropdown = widgets.Dropdown(
            options=["vehicle_type", "transmission_type", None],
            description="(Un)select Hue:",
            disabled=False,
            style={"description_width": "initial"},
        )

    def draw_boxplot_usa(self, hue):
        """
        Draws a boxplot of the CO2 emissions by US car make, gas
        and hybrid run by hue.

        Parameters
        ----------
        hue : str
            Column to be plotted.

        """
        plt.figure(figsize=(15, 6), dpi=100)
        sns.boxplot(
            data=self.co2_usa, x="make_", y="co2emissions_g_km", hue=hue  # noqa: E501
        )
        plt.xticks(rotation=90)
        plt.xlabel("Car Make")
        plt.ylabel("CO2 Emissions (g/km)")
        plt.title("CO2 Emissions (g/km) by Gas and Hybrid Run US Car Brands")
