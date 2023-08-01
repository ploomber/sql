---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.6
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Connecting Postgres to Python in Jupyter notebooks

## Install the necessary packages

```{code-cell} ipython3
%pip install jupysql --upgrade pandas --quiet
```

## Use a Docker Image for Postgres 

```{code-cell} ipython3
%%bash
docker run --name postgres -e POSTGRES_DB=db \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 -d postgres
```

## Load the data


```{important}
<b>Note:</b> If you are following these lessons locally and <b>not</b> on Google Colab, then there is no need to load the data again. 
```

This section was covered in detail in the previous tutorial: [Joining Data in SQL](https://ploomber-sql.readthedocs.io/en/latest/intro-to-sql/joining-data-in-sql.html#load-the-data). We will be using the same data in this tutorial as well.

```{code-cell} ipython3
import sys

sys.path.insert(0, "../../")
import banking  # noqa: E402


_ = banking.MarketData("https://tinyurl.com/jb-bank-m", "expanded_data")
_.extract_asc_to_csv()
```