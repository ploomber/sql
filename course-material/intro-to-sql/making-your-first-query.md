---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.5
---

# Making your first SQL query
<!-- #region -->
### Datasets

To perform your first SQL query, we will be working with 3 datasets:
- Bank Marketing Data
  - URL : https://archive-beta.ics.uci.edu/dataset/222/bank+marketing
- Credit Card Default Data
  - URL : https://archive-beta.ics.uci.edu/dataset/350/default+of+credit+card+clients
- Wholesale Customer Data
  - URL : https://archive-beta.ics.uci.edu/dataset/292/wholesale+customers

Source: UCI Machine Learning Repository

URL: https://archive-beta.ics.uci.edu/dataset/222/bank+marketing

### Dataset descriptions

#### Bank Marketing Data: 
The data is related with direct marketing campaigns of a Portuguese banking institution. The marketing campaigns were based on phone calls. Often, more than one contact to the same client was required, in order to access if the product (bank term deposit) would be ('yes') or not ('no') subscribed. 

The data contains the following categories:

1. age (numeric)
2. job: type of job (categorical: 'admin.','blue-collar','entrepreneur','housemaid','management','retired','self-employed','services','student','technician','unemployed','unknown')
3. marital: marital status (categorical: 'divorced','married','single','unknown')
4. education (categorical: 'basic.4y','basic.6y','basic.9y','high.school','illiterate','professional.course','university.degree','unknown')
5. default: has credit in default? (categorical: 'no','yes','unknown')
6. housing: has housing loan? (categorical: 'no','yes','unknown')
7. loan: has personal loan? (categorical: 'no','yes','unknown')
8. contact: contact communication type (categorical: 'cellular','telephone') 
9. month: last contact month of year (categorical: 'jan', 'feb', 'mar', ..., 'nov', 'dec')
10. day_of_week: last contact day of the week (categorical: 'mon','tue','wed','thu','fri')
11. duration: last contact duration, in seconds (numeric)
12. campaign: number of contacts performed during this campaign and for this client (numeric)
13. pdays: number of days that passed by after the client was last contacted from a previous campaign (numeric; 999 means client was not previously contacted)
14. previous: number of contacts performed before this campaign and for this client (numeric)
15. poutcome: outcome of the previous marketing campaign (categorical: 'failure','nonexistent','success')
16. y: has the client subscribed a term deposit? (binary: 'yes','no')

<!-- #endregion -->

<!-- #region -->
## 5 minute crash course into JupySQL

Play the following video to get familiar with JupySQL to execute queries on Jupyter using DuckDB.

<b>If you get stuck, join our Slack community!</b> https://ploomber.io/community


[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/CsWEUYLaYU0/0.jpg)](https://www.youtube.com/watch?v=CsWEUYLaYU0)

<!-- #endregion -->

#### Install - execute this once. 

```python
try:
    %pip install jupysql --upgrade duckdb-engine pandas --quiet
    print("Success")
except:
    print("retry installing")
```

#### Load the data
```python
from urllib.request import urlretrieve
from zipfile import ZipFile
import pandas as pd
import os

def extract_to_csv(url):
  file = os.path.basename(url)
  urlretrieve(url, file)

  with ZipFile(file, 'r') as zf:
    zf.extractall()

  csv_file_name = 'bank.csv'

  # Data clean up
  df = pd.read_csv(csv_file_name, sep = ";")

  # Save the cleaned up CSV file
  df.to_csv('bank_cleaned.csv', index=False) 

  extract_to_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank.zip')
  ```
  #### Load Engine

<b>Note</b> Ensure you restart any previous notebook that has the same database name as the one initialized below.

```python
%reload_ext sql
%sql duckdb:///bank.duck.db
```

```sql
%%sql
create or replace table bank as
from read_csv_auto('bank_cleaned.csv', header=True, sep=',')
```

```sql
SELECT count(*) FROM absenteeism
```

#### Use JupySQL to perform the queries and answer the questions.

Example: show the first 5 rows.

```sql
SELECT *
FROM absenteeism 
LIMIT 5
```