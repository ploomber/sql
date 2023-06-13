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
# Joining data in SQL

This section demonstrates an important part of SQL: <b>joining</b>. Joining is useful when given two or more datasets that relate to each other. In other words, in a given dataset, additional information can be supplemented from another dataset.

To show the capabilites of joining, we move away from the single bank dataset we initially used in this course. We introduce several new datasets to help introduce this topic.

## Datasets

The datasets we will be using originates from a new bank's financial data. These datasets are public and can be found here: https://web.archive.org/web/20180506061559/http://lisp.vse.cz/pkdd99/Challenge/chall.htm

We first focus on just two datasets, the `account` and `district` dataset. We skip over defining each datasets variables to clearly demonstrate joining. To learn more about the data, please reference the datasets documentations: https://web.archive.org/web/20180506035658/http://lisp.vse.cz/pkdd99/Challenge/berka.htm

Below is a display of `account` and `district` in an Entity-Relationship Diagram (ERD). 

# Insert ERD of account and district

ERDs are useful visuals to help understand the relationship between two or more datasets. Each table in the diagram represents a dataset. The variables of each dataset a represented as rows. The first column is the variable name while the second column is the variable's value type alongside if the variable is a primary key or foreign key. 

What is a primary key and a foreign key? Explain here:

In our case, the "account_id" variable is the primary key for the account table and the "district_id" is the primary key for the district table. "district_id" is a foreign key in the account table. 

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
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(output_folder)
    # Process ASC files and convert them to CSV
    for file_name in zip_ref.namelist():
        if file_name.endswith('.asc'):
            asc_file_path = os.path.join(output_folder, file_name)
            csv_file_path = os.path.join(output_folder, file_name[:-4] + '.csv')
            with open(asc_file_path, 'r') as asc_file, open(csv_file_path, 'w', newline='') as csv_file:
                asc_reader = csv.reader(asc_file, delimiter=';')  # Specify the delimiter used in the .asc file
                csv_writer = csv.writer(csv_file, delimiter=',')
                for row in asc_reader:
                    csv_writer.writerow(row)
            print(f'Converted {asc_file_path} to CSV.')
    print('All ASC files converted to CSV.')

# Running the above function
extract_asc_to_csv('http://sorry.vse.cz/~berka/challenge/pkdd1999/data_berka.zip', 'expanded_data')
```
<!-- #endregion -->
