import ipywidgets as widgets

import matplotlib.pyplot as plt
import seaborn as sns

from sql.ggplot import ggplot, aes, geom_boxplot, geom_histogram


class Seaborn_Barplot:
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
        (
            ggplot(
                table="hist_co2",
                with_="hist_co2",
                mapping=aes(x="co2emissions_g_km"),
            )
            + geom_histogram(bins=b, fill=fill, cmap=cmap)
        )


class Seaborn_Boxplot:
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
        plt.figure(figsize=(15, 6), dpi=100)
        sns.boxplot(
            data=self.co2_usa, x="make_", y="co2emissions_g_km", hue=hue  # noqa: E501
        )
        plt.xticks(rotation=90)
        plt.xlabel("Car Make")
        plt.ylabel("CO2 Emissions (g/km)")
        plt.title("CO2 Emissions (g/km) by Gas and Hybrid Run US Car Brands")
