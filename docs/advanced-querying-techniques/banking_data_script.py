import csv
import urllib.request
import zipfile
import os


def extract_asc_to_csv(url: str, output_folder: str):
    """
    This function extracts the banking data provided from PKDD.
    It downloads the ZIP file from the "url".
    Then, it converts the .asc files to the .csv format.
    The function outputs a folder with a name from output_folder.
    This created folder will be in the current directory.

    Args:
        url (str): the URL containing the public data
        output_folder (str): the name of the folder where files will be stored
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
    zip_file_path, _ = urllib.request.urlretrieve(url)
    # Extract the ZIP file
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(output_folder)
    # Process ASC files and convert them to CSV
    for file_name in zip_ref.namelist():
        if file_name.endswith(".asc"):
            asc_path = os.path.join(output_folder, file_name)
            csv_path = os.path.join(output_folder, file_name[:-4] + ".csv")
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
