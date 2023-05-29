---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.5
  kernelspec:
    display_name: jupyblog
    language: python
    name: python3
---

<!-- #region -->
# Dataset: Absenteeism at work

Source: UCI Machine Learning Repository 

URL: https://archive.ics.uci.edu/ml/datasets/Absenteeism+at+work

### Dataset description 

The data set allows for several new combinations of attributes and attribute exclusions, or the modification of the attribute type (categorical, integer, or real) depending on the purpose of the research.The data set (Absenteeism at work - Part I) was used in academic research at the Universidade Nove de Julho - Postgraduate Program in Informatics and Knowledge Management.


### Categorical data information 

The data contains the following categories without (CID) patient follow-up (22), medical consultation (23), blood donation (24), laboratory examination (25), unjustified absence (26), physiotherapy (27), dental consultation (28).

1. Individual identification (ID)
2. Reason for absence (ICD).
3. Month of absence
4. Day of the week (Monday (2), Tuesday (3), Wednesday (4), Thursday (5), Friday (6))
5. Seasons (summer (1), autumn (2), winter (3), spring (4))
6. Transportation expense
7. Distance from Residence to Work (kilometers)
8. Service time
9. Age
10. Work load Average/day
11. Hit target
12. Disciplinary failure (yes=1; no=0)
13. Education (high school (1), graduate (2), postgraduate (3), master and doctor (4))
14. Son (number of children)
15. Social drinker (yes=1; no=0)
16. Social smoker (yes=1; no=0)
17. Pet (number of pet)
18. Weight
19. Height
20. Body mass index
21. Absenteeism time in hours (target)

<!-- #endregion -->

<!-- #region -->
## 5 minute crash course into JupySQL

Play the following video to get familiar with JupySQL to execute queries on Jupyter using DuckDB.

<b>If you get stuck, join our Slack community!</b> https://ploomber.io/community


[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/CsWEUYLaYU0/0.jpg)](https://www.youtube.com/watch?v=CsWEUYLaYU0)

<!-- #endregion -->

#### Install - execute this once. Can be commented out afterwards if running from Syzygy or locally. 

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

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00445/Absenteeism_at_work_AAA.zip"

# download the file
urlretrieve(url, "./raw-data/Absenteeism_at_work_AAA.zip")

# Extract the CSV file
with ZipFile("./raw-data/Absenteeism_at_work_AAA.zip", 'r') as zf:
    zf.extractall("./raw-data/")

# Check the extracted CSV file name (in this case, it's "Absenteeism_at_work.csv")
csv_file_name = "./raw-data/Absenteeism_at_work.csv"

# Data clean up
df = pd.read_csv(csv_file_name, sep=",")
df.columns = df.columns.str.replace(' ', '_')

# Save the cleaned up CSV file
df.to_csv("Absenteeism_at_work_cleaned.csv", index=False)
```

#### Load Engine

<b>Note</b> Ensure you restart any previous notebook that has the same database name as the one initialized below.

```python
%reload_ext sql
%sql duckdb:///absenteeism.duck.db
```

```sql
create or replace table absenteeism as
from read_csv_auto('Absenteeism_at_work_cleaned.csv', header=True, sep=';')
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

#### Question 1.1 (Easy):
How many records are there in the 'absenteeism' table? 


<!-- #region -->
<details>

<summary>Answers</summary>

You can use the `%%sql` magic and the `COUNT(*)` function to count the total number of records. 

```python
%%sql
SELECT COUNT(*) 
FROM absenteeism
```
</details>
<!-- #endregion -->

#### Question 1.2 (Easy):
How many unique employees are listed in the dataset?



<!-- #region -->
<details>

<summary>Answers</summary>

You can use the `%%sql` magic and the `COUNT(DISTINCT ID)` function to count the total number of unique instances of the `Age` column. 

```python
%%sql
SELECT COUNT(DISTINCT ID) 
FROM absenteeism;
```
</details>
<!-- #endregion -->

#### Question 1.3 (Easy):
What is the average distance from residence to work? 


<!-- #region -->
<details>

<summary>Show Answers</summary>

You can use the `%%sql` magic and the `AVG(Distance_from_Residence_to_Work)` function to calculate the average distance from residence to work.. 

```python
%%sql
SELECT AVG(Distance_from_Residence_to_Work) 
FROM absenteeism;
```
</details>
<!-- #endregion -->

#### Question 2.1 (Medium):
On which days of the week does the average absenteeism time exceed 4 hours? 


<!-- #region -->
<details>

<summary>Answers</summary>

You can use the `%%sql` magic and break down the query as follows:

1. Select the column with name `Day_of_the_week`
2. From the table called `absenteeism`
3. Then group the values by day of the week that have an average value (use `AVG`) of more than 4 hours in absenteeism. 

```python
%%sql
SELECT Day_of_the_week 
FROM absenteeism 
GROUP BY Day_of_the_week 
HAVING AVG(Absenteeism_time_in_hours) > 4;
```
</details>
<!-- #endregion -->

#### Question 2.2 (Medium):
What is the average transportation expense for each season?


<!-- #region -->
<details>

<summary>Answers</summary>

You can use the `%%sql` magic and. Use the `AVG(Transportation_expense)` with the alias `AVG_Transportation_Expense` function to count the average transporation expense, then group by seasons.

```python
%%sql
SELECT Seasons, AVG(Transportation_expense) AS AVG_Transportation_Expense
FROM absenteeism 
GROUP BY Seasons;

```
</details>
<!-- #endregion -->

<!-- #region -->
#### Question 2.3 (Medium):


What is the average absenteeism time for employees with BMI higher than the average BMI
<!-- #endregion -->


<!-- #region -->
<details>

<summary>Show Answers</summary>

You can use the `%%sql` magic and. Use the `AVG(Absenteeism_time_in_hours)` with the alias `AVG_Absenteeism_time_in_hours` function to count the average absenteeism (time units hours). 

`WHERE Body_mass_index > (`: This part begins a condition that the data must meet to be included in our average calculation. Here, we're only interested in rows where the `Body_mass_index` is greater than a certain value.

`SELECT AVG(Body_mass_index) FROM absenteeism)`: This is a subquery, a query within a query. It's calculating the average `Body_mass_index` for the entire absenteeism table.

```python
%%sql
SELECT AVG(Absenteeism_time_in_hours) as AVG_Absenteeism_time_in_hours
FROM absenteeism 
WHERE Body_mass_index > (
    SELECT AVG(Body_mass_index) 
    FROM absenteeism);

```
</details>
<!-- #endregion -->

#### Question 3.1 (Hard):
Find the top 3 ages with the highest total absenteeism hours, excluding disciplinary failures.



<!-- #region -->


<details>

<summary>Answers</summary>

You can use the `%%sql` magic and break down the query as follows:

1. Select the column with name `Age`, compute the Sum of `Absenteeism_time_in_hours`. Give this sum an alias `Sum_Absenteeism`.
2. From the table called `absenteeism`
3. The keywork WHERE is used to filter the data that meets a specific condition, in this case `Disciplinary_failure` is equal to zero.
4. Group values by the `Age` column.
5. Sort the values by the sum and show the first 3 values.

```python
%%sql
SELECT Age, SUM(Absenteeism_time_in_hours) AS Sum_Absenteeism
FROM absenteeism 
WHERE Disciplinary_failure = 0 
GROUP BY Age 
ORDER BY Sum_Absenteeism
DESC LIMIT 3;
```
</details>
<!-- #endregion -->

#### Question 3.2 (Hard):

Find the age of employees who have been absent for more than 5 hours with an unjustified absence.

Hint: investigate encoding on the data source.


<!-- #region -->
<details>

<summary>Answers</summary>

You can use the `%%sql` magic. 'Unjustified absence' is coded with 26. From there all that is required is selecting the age, and using `WHERE` to set up the appropriate conditions. 

```python
%%sql
SELECT Age 
FROM absenteeism 
WHERE Reason_for_absence = 26 AND Absenteeism_time_in_hours > 5;

```
</details>
<!-- #endregion -->

#### Question 3.3 (Hard):

Which reasons for absence are more frequent for social drinkers than social non-drinkers?


<!-- #region -->
<details>

<summary>Show Answers</summary>

You can use the `%%sql` magic. We use `SELECT` to extract the `Reason_for_absence` from the `absenteeism` table. 

The column `Social_drinker` is encoded using binary notation, 0=is not a social drinker, 1=is a social drinker. 

We next group by their reason for absence. 

`HAVING COUNT() > (`  begins the condition that the groups must meet to be included in the results. Only groups where the count of rows (representing the number of instances of each `Reason_for_absence` among social drinkers) is greater than a certain value will be included.

`SELECT COUNT() FROM absenteeism WHERE Social_drinker = 0 GROUP BY Reason_for_absence)`  is a subquery that calculates the count of rows for each `Reason_for_absence` where `Social_drinker` is 0 (indicating the employee is not a social drinker), effectively giving us the number of instances of each `Reason_for_absence` among non-social drinkers.

```python
%%sql
SELECT Reason_for_absence 
FROM absenteeism 
WHERE Social_drinker = 1 
GROUP BY Reason_for_absence 
HAVING COUNT() > (
    SELECT COUNT() 
    FROM absenteeism 
    WHERE Social_drinker = 0 
    GROUP BY Reason_for_absence);

```
</details>
<!-- #endregion -->

### Bonus: Save the tables you created using the `--save` option, use the saved tables to generate visualizations.

Here are a few tutorials to get you started:

Parameterizing SQL queries: https://jupysql.ploomber.io/en/latest/user-guide/template.html

SQL Plot: https://jupysql.ploomber.io/en/latest/api/magic-plot.html

Organizing Large queries: https://jupysql.ploomber.io/en/latest/compose.html

Plotting with ggplot: https://jupysql.ploomber.io/en/latest/user-guide/ggplot.html

Turning your notebook into a Voila dashboard: https://ploomber.io/blog/voila-tutorial/


### References   

Martiniano, A., Ferreira, R. P., Sassi, R. J., & Affonso, C. (2012). Application of a neuro fuzzy network in prediction of absenteeism at work. In Information Systems and Technologies (CISTI), 7th Iberian Conference on (pp. 1-4). IEEE.

### Acknowledgements

Thank you Mark Needham for producing the 5 minute crash course on using JupySQL.



