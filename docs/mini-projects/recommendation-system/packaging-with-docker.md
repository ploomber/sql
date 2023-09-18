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

# Writing a Dockerfile for a FastAPI Application with Ploomber, SQL, and DuckDB

FastAPI has quickly become one of the go-to frameworks for building high-performance web APIs in Python. In this post, we'll walk you through creating a Dockerfile for a FastAPI application that leverages Ploomber for data pipelines, SQL for data wrangling, and DuckDB as the database. This application will also transform data through an NLP recommendation system.

## Why DuckDB?

Before we dive into the Dockerfile, let's discuss the choice of DuckDB as our database. DuckDB is an in-memory analytical database that supports full SQL. It's designed for interactive data analysis and edge computing. Some of its features include:

* In-Memory Execution: DuckDB processes data in memory, making it incredibly fast for analytical queries.

* SQL Support: It provides full SQL support, allowing for complex data wrangling and transformation tasks.

* Edge Computing: DuckDB is lightweight and can be embedded in various applications, making it suitable for edge computing scenarios.

Given these features, DuckDB becomes an excellent choice for applications that require fast data processing and analytics.

## Folder structure

Please ensure you have followed the previous posts:

1. [Package management with Poetry](setting-up-poetry.md)
2. [Setting up an Extract-Transform-Load (ETL) pipeline with Ploomber](setting-up-etl.md)
3. [Data wrangling with SQL and DuckDB](eda-with-jupyter.md)
4. [Building a recommendation system with NLP](setting-up-a-recommendation-system.md)
5. [Setting up a FastAPI application](setting-up-fastapi.md)

The folder structure for the project is as follows:

```bash
mini-projects
├──movie-rec-system
├──├── movies_data.duckdb
├──├── movies_data.duckdb.wal
├──├── .movies_data.duckdb.metadata
├──├── pipeline.yaml
├──├── pyproject.toml
├──├── README.md
├──├── app
├──│   └── app.py
├──│   └── recommender.py
├──│   └── recommenderhelper.py
├──├── etl
├──│   └── extract.py
├──│   └── eda.ipynb
├──├── products
├──     └── eda-pipeline.ipynb
├──     └── extract-pipeline.ipynb
├──     └── .eda-pipeline.ipynb.metadata
├──     └── .extract-pipeline.ipynb.metadata
├──└── tests
├──│       └── test_app.py
├──│       └── __init__.py
├──└── .env
```

## Adding a Dockerfile

To package our application, we'll use Docker. Docker is a tool that allows us to package our application into a container. A container is a lightweight, standalone, executable package of software that includes everything needed to run an application. It provides a consistent environment for our application to run in, regardless of the environment it's running on. We will create a file called `Dockerfile` in the root directory (under `movie-rec-system`) of our project. This file will contain the instructions for building our Docker image.

When writing a Dockerfile, two of the most commonly used instructions are `RUN` and `CMD`. While they might seem similar at first glance, they serve distinct purposes. Let's delve into each of these commands and understand their differences.

### `RUN` Command

The `RUN` instruction is used to execute commands as part of the image build process. Every time a `RUN` command is encountered in the Dockerfile, Docker executes the command and then commits the result as a new layer in the image. This is how Docker images are built up from a series of layers.

Use Cases:

* Installing software packages.
* Setting up local databases.
* Building code.
* Any other setup that needs to be part of the container image.

Example:

```dockerfile
RUN apt-get update && apt-get install -y curl
```

In the example above, the `RUN` command updates the package list and installs the curl utility in the image.

### `CMD` Command

The `CMD` instruction defines the default command that will be executed when a container is run from the image. Unlike `RUN`, it does not create a new layer in the image but simply provides metadata to the image indicating what command should be run by default when a container is started from it. If the user specifies a command when starting the container, it will override the `CMD` instruction.

Use Cases:

* Starting an application.
* Running a service.
* Any command that should be the default behavior when a container is started from the image.

Example:

```dockerfile
CMD ["nginx", "-g", "daemon off;"]
```

In this example, the `CMD` command specifies that the Nginx server should be started in the foreground when a container is run from the image.

### Key differences

1. Execution Time:

* `RUN`: Executes during the image build process.
* `CMD`: Specifies the default command to run when the container starts.

2. Purpose:

* `RUN`: Used for installing software, setting up the environment, or other tasks that modify the filesystem.
* `CMD`: Defines the default behavior of the container when it's run. It doesn't modify the image or create a new layer.

3. Overriding:

* `RUN`: Cannot be overridden at runtime.
* `CMD`: Can be overridden by providing arguments to the docker run command.

4. Number of Commands:

* `RUN`: Multiple RUN commands result in multiple layers in the Docker image.
* `CMD`: If there are multiple CMD commands in a Dockerfile, only the last one will take effect.

## Crafting the Dockerfile

Let's break down the Dockerfile step by step:

```dockerfile
# Use the official Python image as the base image
FROM python:3.10
```

We start by using the official Python 3.10 image. This ensures our application runs in a clean environment with the specified Python version.

```dockerfile
# Set the working directory in the container to /app
WORKDIR /app
```

We set `/app` as our working directory inside the container. All subsequent commands will be run from this directory.

```dockerfile
# Copy the poetry files
COPY pyproject.toml poetry.lock /app/
```

We copy the `pyproject.toml` and `poetry.lock` files to the container. These files are used by Poetry, a dependency management tool, to manage our project's dependencies.

```dockerfile
# Install poetry
RUN pip install poetry
```

We install Poetry in the container. Poetry is a tool for dependency management and packaging in Python. It allows us to specify our project's dependencies in a `pyproject.toml` file and then install them with a single command.

```dockerfile
# Install project dependencies
RUN poetry lock
RUN poetry install
```

We then lock the dependencies to ensure consistent installations and install the project's dependencies using Poetry.

```dockerfile
# Copy the .env file
COPY .env .env
```

If our application uses environment variables stored in a .env file, we copy that file into the container.

```dockerfile
# Copy the rest of the application code
COPY . .
```

We copy the rest of our application code into the container.

```dockerfile
# Extract data for app
RUN poetry run ploomber build
```

Before our application starts, we run our Ploomber pipeline to fetch and process the data. This ensures that our application has the necessary data ready when it starts.

```dockerfile
# Expose the port that the app runs on
EXPOSE 8000
```

We expose port 8000, which is the default port for FastAPI applications.

```dockerfile
# Execute the script when the container starts
CMD ["poetry", "run", "uvicorn", "movie_rec_system.app.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

Finally, we specify the command to run when the container starts. This command starts our FastAPI application using Uvicorn.

### Bringing all the pieces together

Putting all the pieces together, our Dockerfile looks like this:

```dockerfile
# Use the official Python image as the base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the poetry files
COPY pyproject.toml poetry.lock /app/

# Install poetry
RUN pip install poetry

# Install project dependencies
RUN poetry lock
RUN poetry install

# Copy the .env file
COPY .env .env

# Copy the rest of the application code
COPY . .

# Extract data for app
RUN poetry run ploomber build

# Expose the port that the app runs on
EXPOSE 8000

# Execute the script when the container starts
CMD ["poetry", "run", "uvicorn", "movie_rec_system.app.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

We can save the Dockerfile and move on to building our Docker image.

## Building the Docker Image

Now that we have our Dockerfile, we can build our Docker image. To do this, we run the following command:

```bash
docker build -t movie-rec-system .
```

This command builds the Docker image and tags it with the name `movie-rec-system`. The `-t` flag is used to specify the name of the image.

## Running the Docker Image

Once we have our Docker image, we can run it using the following command:

```bash
docker run -p 8000:8000 movie-rec-system
```

This command runs the Docker image and maps port 8000 on the host to port 8000 on the container. The `-p` flag is used to specify the port mapping.

## Conclusion

In this post, we learned how to package our FastAPI application into a Docker image. We also learned about the differences between the `RUN` and `CMD` commands in Dockerfiles. We hope you found this post useful and that it helps you get started with Dockerizing your applications!