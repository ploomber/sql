import csv
import urllib.request
import zipfile
import os
from urllib.request import urlretrieve
from zipfile import ZipFile
import pandas as pd


class BankingData:
    def __init__(self, url, data_name):
        self.url = url
        self.data_name = data_name

    def extract_to_csv(self):
        # check if "bank_data" folder exists, if not, create it
        if not os.path.exists("bank_data"):
            os.mkdir("bank_data")
        # Retrieve the zip file from the url link
        file = os.path.basename(self.url)
        urlretrieve(self.url, file)
        # Extract the zip file's contents
        with ZipFile(file, "r") as zf:
            zf.extractall("bank_data")
        # The file containing our data
        csv_file_name = f"{self.data_name}.csv"
        # Data clean up
        df = pd.read_csv(f"bank_data/{csv_file_name}", sep=";")
        # Save the cleaned up CSV file
        df.to_csv(df.to_csv(f"{self.data_name}_cleaned.csv", index=False))


class MarketData:
    def __init__(self, url, output_folder):
        self.url = url
        self.output_folder = output_folder

    def extract_asc_to_csv(self):
        """
        This function extracts the banking data provided from PKDD.
        It downloads the ZIP file from the "url".
        Then, it converts the .asc files to the .csv format.
        The function outputs a folder with a name from output_folder.
        This created folder will be in the current directory.

        Args:
            url (str): the URL containing the public data
            output_folder (str): the name of the folder where
            files will be stored
        """

        # Columns to rename for district table
        district_column_names = [
            "district_id",
            "district_name",
            "region",
            "no_of_inhabitants",
            "no_of_municipalities_lt_499",
            "no_of_municipalities_500_1999",
            "no_of_municipalities_2000_9999",
            "no_of_municipalities_gt_10000",
            "no_of_cities",
            "ratio_of_urban_inhabitants",
            "average_salary",
            "unemployment_rate_95",
            "unemployment_rate_96",
            "no_of_entrepreneurs_per_1000_inhabitants",
            "no_of_committed_crimes_95",
            "no_of_committed_crimes_96",
        ]

        # Download the ZIP file
        zip_file_path, _ = urllib.request.urlretrieve(self.url)
        # Extract the ZIP file
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(self.output_folder)
        # Process ASC files and convert them to CSV
        for file_name in zip_ref.namelist():
            if file_name.endswith(".asc"):
                asc_path = os.path.join(self.output_folder, file_name)
                csv_file_name = file_name[:-4] + ".csv"
                csv_path = os.path.join(self.output_folder, csv_file_name)
                with open(asc_path, "r") as asc_file, open(
                    csv_path, "w", newline=""
                ) as csv_file:
                    asc_reader = csv.reader(asc_file, delimiter=";")
                    csv_writer = csv.writer(csv_file, delimiter=",")
                    if file_name == "district.asc":
                        next(asc_reader)
                        new_header = district_column_names
                        csv_writer.writerow(new_header)
                        csv_writer.writerows(asc_reader)
                    else:
                        for row in asc_reader:
                            csv_writer.writerow(row)
                print(f"Converted {asc_path} to CSV.")
        print("All ASC files converted to CSV.")


# Example usage
# link = "http://sorry.vse.cz/~berka/challenge/pkdd1999/data_berka.zip"
# output = "expanded_data"
# extract_asc_to_csv(link, output)
