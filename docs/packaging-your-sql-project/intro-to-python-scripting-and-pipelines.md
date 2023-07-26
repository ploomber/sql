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

# Introduction to Python scripting and data pipelines

In this section of the course, we will delve into the world of Python scripting and explore how it plays a crucial role in building data pipelines. You'll learn about `.py` scripts and good software development practices for scripting. Through the power of Python scripting, you will gain insights into data pipelines and how they automate data ingestion tasks, providing you with the tools to create robust and efficient data workflows.

## `.py` script vs Jupyter Notebook

A `.py` script is a standalone file that contains Python code, which can be written with the help of text editors or IDE's (integrated development environment).

Unlike Jupyter notebooks, which are interactive environments for code execution and documentation, `.py` scripts are designed for running Python code in a more traditional, non-interactive manner. They are commonly used for writing programs that can be executed from the command line, as shown below, or integrated into software projects due to [modularization](https://ploomber-sql.readthedocs.io/en/latest/packaging-your-sql-project/intro-to-python-scripting-and-pipelines.html#modularization) (variables and functions inside a Python script can be imported from another script).

After writing and saving a Python script, you can run it by executing the `python` command on your terminal, like so:

```bash
python my_script.py
```

<b>Note:</b> The command above assumes that your terminal is currently inside the folder where the `my_script.py` file is located.

IDE's, such as [Visual Studio Code](https://code.visualstudio.com/) and [Pycharm](https://www.jetbrains.com/pycharm/) on the other hand, offer a more interactive way of writing and running Python scripts. They provide features such as syntax highlighting, code completion, and debugging tools, making it easier to write and test your code.

```{important}
`.py` scripts are always executed linearly from top to bottom, unlike Jupyter notebooks, where you can run cells in any order. This makes debugging easier in `.py` scripts, as you can easily trace the flow of execution.
```

Jupyter Notebooks are loved by Data Scientists for their interactive nature. Outputs, such as messages, plots, and dataframes, appear under each cell upon execution, and look great out-of-the-box. Moreover, Jupyter Notebooks are great for data analysis and sharing results with colleagues. However, they must be served and accessed through a web browser, making them slightly harder to use than scripts.

Let's now shift our focus to explore good software development practices for scripting. Adopting these practices will help you write clean, maintainable, and efficient Python code for integration into larger projects or data pipelines.

## Good Software Development Practices for Scripting

When writing Python scripts, it's essential to follow good software development practices to ensure maintainability and readability of the code. The [`PEP 8` (Python Enhancement Proposals) – Style Guide](https://peps.python.org/pep-0008/), which is a written standard for scripting for Python Code, encompasses all best practices discussed in this section. Here are some key elements to consider:

### Imports at the Top

In Python scripting, it is recommended to place all imports at the top of the script. This practice helps improve code readability and makes it easier for others to understand the dependencies of the script. Additionally, adhering to this convention enables code linters, tools that format the code to comply with `PEP8` standards, like [`flake8`](https://flake8.pycqa.org/en/latest/) to enforce the rule ([`E402`](https://www.flake8rules.com/rules/E402.html)) that requires imports to be at the top of the file.

<b>Note:</b> IDE's like [Visual Studio Code](https://code.visualstudio.com/) come with built-in linters that can be configured to enforce `flake8` rules.

Furthermore, it is essential to be cautious about importing modules that are not used in the script. Linters like [`flake8`](https://flake8.pycqa.org/en/latest/) can help identify such unused imports ([`F401`](https://www.flake8rules.com/rules/F401.html)). Removing these unused imports reduces unnecessary clutter and improves the script's performance and maintainability.

```{important}
Did you know: Eduardo Blancas, Ploomber's co-founder, is the creator of the package `pkgmt`, which automatically formats and lints Python code! In fact, the Ploomber team uses it religiously to ensure best coding practices in our projects. `pip install pkgmt` to try it out!
```

### Function Definition

In general, a function should only perform one action and be named accordingly. Below are guidelines to follow when defining functions:

#### Naming Conventions

- Function names should be lowercase, with words separated by underscores as necessary to improve readability. Variable names follow the same convention as function names.
- Avoid "and" in function names. Dedicate a single function to a single task.
- Adequately describe the function’s purpose by using a verb first and a noun following it. An example of a good function name is `get_data()`, which describes the action of the function and the data it returns.
- Same goes for parameter names in functions: banish “x” and “y” from your code and use descriptive names instead.

#### Docstrings

- Docstrings are used to describe the purpose of a function, specifically its parameters and what it returns. They are placed immediately after the function definition and are enclosed in `"""triple double quotes"""`.
- Blank lines should be removed from the beginning and end of the docstring.
- It is best to list each argument on a separate line, followed by a description of the argument.
- See [`PEP 257` guidelines](https://peps.python.org/pep-0257/) for more information on docstrings.

An example is as follows:

```{code-cell} ipython3
def divide(num1, num2):
    """
    Divide two two numbers.

    Parameters:
    num1 (float or int): The numerator.
    num2 (float or int): The denominator.

    Returns:
    float or int: The result of the division operation.
    """
    if num2 == 0:
        raise ValueError("Cannot divide by zero.")
    else:
        return num1 / num2
```

#### Modularization

- Modularization is the technique of breaking down your script into smaller, self-contained modules or functions. Each module or function performs a specific task, making the code more readable, maintainable, and reusable.
- Moreover, modularization enhances collaboration as multiple developers can work on different modules simultaneously, promoting collaboration and parallel development. This speeds up the overall development process and allows teams to work on specific parts of the project independently.
- Modularization is often used in conjunction with the main program, which calls the functions defined in the modules to execute the main logic of the script. This is discussed in more detail below.

### The Main Program

#### What does `if __name__ == "__main__:"` mean?

Typically, a script will have a `main` function that calls other functions to execute the main logic of the script. The `main` function is called from the `if __name__=="__main__":` block, which is executed when the script is run directly (not imported as a module). This allows you to have reusable code in your script that can be imported into other scripts without unintended side effects.

Inside the `if __name__=="__main__":` block, you can call the functions you defined earlier to execute the main logic of your script:

```{code-cell} ipython3
if __name__ == "__main__":
    # call divide() function here
    valid_result = divide(10, 5)
    print("Valid Result: ", valid_result)
```

#### Calling Functions from the Main Program

Modularized scripts can be called in the main program as follows:

```{code-cell} ipython3
def add(int1, int2):
    """This function adds two integers"""
    return int1 + int2


def subtract(int1, int2):
    """This function subtracts two integers"""
    return int1 - int2


if __name__ == "__main__":
    num1 = 10
    num2 = 5

    result_add = add(num1, num2)
    result_subtract = subtract(num1, num2)

    print(f"Addition: {result_add}")
    print(f"Subtraction: {result_subtract}")
```

#### Advanced Scripting Techniques

In addition to understanding the basics of Python scripting, there are advanced techniques that can help you organize your code into reusable modules and create a well-structured project.

When you call if `__name__ == "__main__":` in different scripts, it allows you to use the scripts with your functions as reusable modules that can be imported into other scripts. For instance, the above example could be modularized with the functions placed in a separate script called `math_operations.py` and the main logic in an another script called `main.py`. `main.py` would `import math_operations` as a module and call the functions like so: `math_operations.add(num1, num2)`.

However, in order to call `math_operations.py` in `main.py`, we need to explore two important concepts: `__init__.py` files and good folder structure.

##### `__init__.py` Files

- `__init__.py` files are used to mark directories on disk as Python package directories.
- If you have the files `__init__.py` and `math_operations.py` in the same directory, you can import the `math_operations` module like so: `import math_operations`.

##### Folder Structure

- A good folder structure is essential for organizing your code and making it reusable.

A sample folder structure for our `math_operations` module is as follows:


project/
│   README.md
│   requirements.txt
│   setup.py
│   .gitignore
│   .env
│
└───src/
│   │   __init__.py
│   │   main.py
│   │
│   └───math_operations/
│       │   __init__.py
│       │   math_operations.py
│
└───tests/
    │   test_math_operations.py


Therefore, given the above folder structure, the `math_operations` module can be imported into `main.py` as follows:

```python
from math_operations import add, subtract

if __name__ == "__main__":
    num1 = 10
    num2 = 5

    result_add = add(num1, num2)
    result_subtract = subtract(num1, num2)

    print(f"Addition: {result_add}")
    print(f"Subtraction: {result_subtract}")
```

## Python Scripting for Data Pipelines

Python scripting is a powerful way to automate data tasks, such as downloading data from the web, cleaning and transforming data, and saving it to a database. The combination of [`pandas`](https://pandas.pydata.org/docs/user_guide/index.html#user-guide) and [`SQLAlchemy`](https://docs.sqlalchemy.org/en/20/core/index.html) provides a robust toolkit for working with data in Python.

By using `pandas`, you can easily read and write data from various file formats, perform data cleaning and manipulation, and create insightful visualizations. All of these steps must be coded in different functions, to ensure both readability and reusability, and called from the main program. The modularized code can then be packaged into a Python package and imported into other scripts.

`SQLAlchemy` is an object-relational mapper (ORM) for Python that enables seamless interaction with databases, allowing you to save your cleaned and processed data to a database for further analysis. Code that helps create a database connection and save the data as tables to the respective database can be included in the main program itself. At Ploomber, [`SQLAlchemy Core`](https://docs.sqlalchemy.org/en/20/core/index.html) is leveraged as the foundation for interacting with databases. `SQLAlchemy Core` provides a powerful and flexible toolkit for working directly with SQL and relational databases, offering a lower-level, yet highly expressive approach compared to the full [`SQLAlchemy ORM`](https://docs.sqlalchemy.org/en/20/orm/index.html).

The `datadownload.py` [script](https://github.com/ploomber/sql/blob/main/pipeline/src/datadownload.py) used in this module of the course combines `pandas` and `DuckDB` to create a data ingestion pipeline for our project. It downloads data from the web, cleans and transforms it, and saves it to a `DuckDB` database. In this script, `SQLAlchemy` was not explicitly imported and used to form a connection because `DuckDB` is lightweight and easy to deploy. However, `SQLAlchemy` can be used in other projects to interact with different databases, such as [`PostgreSQL`](https://jupysql.ploomber.io/en/latest/integrations/postgres-connect.html) and [`MySQL`](https://jupysql.ploomber.io/en/latest/integrations/mysql.html), allowing for database operations using [`JupySQL`](https://jupysql.ploomber.io/en/latest/quick-start.html#)!

 The next section on [ETL Pipelines](https://ploomber-sql.readthedocs.io/en/latest/packaging-your-sql-project/intro-to-etl-pipelines-with-python-and-sql#) will discuss the use of `pandas` and `DuckDB` in more detail.

## References

“Python Enhancement Proposals.” PEP 8 – Style Guide for Python Code, n.d. https://peps.python.org/pep-0008/.

“The Big Ol’ List of Rules.” Flake8 Rules, n.d. https://www.flake8rules.com/.
