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

A `.py` script is a standalone file that contains Python code, which can be written with the help of text editors or IDE's (integrated development environment). Unlike Jupyter notebooks, which are interactive environments for code execution and documentation, `.py` scripts are designed for running Python code in a more traditional, non-interactive manner. They are commonly used for writing programs that can be executed from the command line, as shown above, or integrated into software projects due to [modularization](https://ploomber-sql.readthedocs.io/en/latest/packaging-your-sql-project/intro-to-python-scripting-and-pipelines#) (variables and functions inside a Python script can be imported from another script).

After writing and saving a Python script, you can run it by executing the `python` command on your terminal, like so:

```bash
python my_script.py
```

<b>Note:</b> The command above assumes that your terminal is currently inside the folder where the `my_script.py` file is located.

IDE's, such as [Visual Studio Code](https://code.visualstudio.com/) and [Pycharm](https://www.jetbrains.com/pycharm/) on the other hand, offer a more interactive way of writing and running Python scripts. They provide features such as syntax highlighting, code completion, and debugging tools, making it easier to write and test your code.

```important
`.py` scripts are always executed linearly from top to bottom, unlike Jupyter notebooks, where you can run cells in any order. This makes debugging easier in `.py` scripts, as you can easily trace the flow of execution.
```

Jupyter Notebooks are loved by Data Scientists for their interactive nature. Outputs, such as messages, plots, and dataframes, appear under each cell upon execution, and look great out-of-the-box. Moreover, Notebooks are great for data analyses and sharing results with colleagues. However, Notebooks must be served and accessed through a web browser, making them slightly harder to use than scripts.

Let's now shift our focus to explore good software development practices for scripting. Adopting these practices will help you write clean, maintainable, and efficient Python code for integration into larger projects or data pipelines.

## Good Software Development Practices for Scripting

When writing Python scripts, it's essential to follow good software development practices to ensure maintainability and readability of the code. Here are some key elements to consider:

### Imports at the Top

- code formatting and linting
- `flake8` rule (E402) for imports at top
- also be wary of module imported but unused (F401)

### Function Definition

In general, a function should only perform one action. -> clarity!

#### Naming Conventions

- avoid "and" in function names, dedicate a single function to a single task
- adequately describe the function’s purpose by using a verb first and a noun following it
- same goes for parameter names: banish “x” and “y” from your code

#### Docstrings

- begin with a brief statement describing what the function does
- PEP 257: use triple quotes for multi-line docstrings

#### Modularization and Pythonic Principles

Break down your script into smaller, reusable functions. This promotes code modularity and makes the script easier to test and maintain.

Follow Pythonic principles and idioms to write clean and concise code. Embrace the Python way of doing things to make your code more readable and efficient.

### Calling Functions from the Main Program

The `if __name__=="__main__":` block is used to ensure that certain code only runs when the script is executed directly, not when it's imported as a module. This allows you to have reusable code in your script that can be imported into other scripts without unintended side effects.

calling functions from the Main Program:

Inside the `if __name__=="__main__":` block, you can call the functions you defined earlier to execute the main logic of your script:

```python
if __name__=="__main__":
    # call functions here
    pass
```

## Python Scripting for Data Pipelines

`datadownload.py` [script]()

Python scripting is a powerful way to automate data tasks, such as downloading data from the web, cleaning and transforming data, and saving it to a database. The combination of `pandas` and `SQLAlchemy` provides a robust toolkit for working with data in Python.

Using pandas, you can easily read and write data from various file formats, perform data cleaning and manipulation, and create insightful visualizations. `SQLAlchemy` enables seamless interaction with databases, allowing you to save your cleaned and processed data to a database for further analysis.

In the following sections, we will learn about and explore the ETL (Extract, Transform, Load) Pipeline.