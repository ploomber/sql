---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.6
kernelspec:
  display_name: jupyblog
  language: python
  name: python3
---

# Combining data from multiple tables

<!-- #region -->
## Install - execute this once. 
<b>Note:</b> If you are following these lessons locally and <b>not</b> on Google Colab, then there is no need to reinstall these packages.

This code installs JupySQL, DuckDB, and Pandas in your environment. We will be using these moving forward.

```{code-cell} ipython3
%pip install jupysql --upgrade duckdb-engine pandas --quiet
```

## Load the data
We extract the financial data by retrieving it from it's URL download link. The link may be a zip file (which it is in this case), so we extract the zip file and conver the .asc files to .csv files. Finally, we save converted data into a folder.

``` {code-cell} ipython3
import csv
import urllib.request
import zipfile
import os
def extract_asc_to_csv(url, output_folder):
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
                for row in asc_reader:
                    csv_writer.writerow(row)
            print(f"Converted {asc_path} to CSV.")
    print("All ASC files converted to CSV.")
# Example usage
link = "http://sorry.vse.cz/~berka/challenge/pkdd1999/data_berka.zip"
output = "expanded_data"
extract_asc_to_csv(link, output)
```
<!-- #endregion -->
