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

# How to package your pipeline

In the previous sections, we learned key components that will help us automate an Extract-Transform-Load (ETL) pipeline:

1. Python scripting and best practices to ensure reproduceability and
    maintainability
2. The ETL processes with Python through `requests`, `pandas`,
    and `duckdb`

The process above ensures that we can run our pipeline locally, and automates the process of downloading data, transforming it, and loading it into a database. However, we still need to run the pipeline manually. In this section, we will learn how to package our pipeline so that it can be run on any machine.

## What is packaging?

Packaging is the process of bundling your code and its dependencies into a single unit that can be run on any machine. In the Python ecosystem, the most common way to package code is through Docker containers.

## A word on virtual environments

Virtual environments are a great way to isolate your Python dependencies. However, they are not portable. This is because virtual environments are tied to the operating system they were created on. Docker containers, on the other hand, are portable and can be run on any machine. Still, virtual environments are a great way to ensure that your code runs on your machine before packaging it into a Docker container.

You can start a virtual environment with `conda`. Let's suppose we name it `myenv`, we can specify the Python version as follows: 

```bash
conda create -n myenv python==3.10
```

We can then active it:

```bash
conda activate myenv
```

Working within virtual environments ensures that we are not using any system-wide Python packages. We can install packages as follows:

```bash
pip install requests pandas duckdb==0.8.1 duckdb-engine==0.9.1
```

We can then document what versions and added dependencies are in our virtual environment by running:

```bash
pip freeze > requirements.txt
```

This will be used in the Dockerfile when we build our Docker image.

To deactivate the virtual environment, we can run:

```bash
conda deactivate
```

```{important}
Ideally you should create a virtual environment for each project. This ensures that you can run your code on any machine. 
```

## Key ingredients to package a Python pipeline

To package a Python pipeline, we need:

1. A `.py` script
2. A `requirements.txt` file listing any dependencies and their versions
3. A `Dockerfile` to build a Docker image

We covered the first two items in the previous sections. In this section, we will learn how to create a `Dockerfile` to build a Docker image.


## Pipeline directory structure

For this blog, we will assume the following directory structure:

```bash
├── Dockerfile
├── README.md
├── pipeline
│   ├── src
│   │   ├── datadownload.py
│   ├── data
│   │   ├── database
│   │   │   ├── car_data.duckdb
└── requirements.txt
```

## What is a Docker container?

A Docker container is a lightweight, standalone, executable package of software that includes everything needed to run an application: code, runtime, system tools, system libraries, and settings. Containers isolate software from its surroundings, for example, differences between development and staging environments and help reduce conflicts between teams running different software on the same infrastructure.

## Why use Docker containers?

Docker containers are a great way to package your code because they are:

1. **Lightweight**: Containers leverage and share the host kernel, making them much more efficient in terms of system resources than virtual machines.
2. **Portable**: You can build locally, deploy to the cloud, and run anywhere.
3. **Loosely coupled**: Containers are highly self sufficient and encapsulated, allowing you to replace or upgrade one without disrupting others.
4. **Scalable**: You can increase and automatically distribute container replicas across a datacenter.
5. **Secure**: Containers apply aggressive constraints and isolations to processes without any configuration required on the part of the user.

## Setting up the Dockerfile

The `Dockerfile` is a text file that contains all the commands a user could call on the command line to assemble an image. Using `docker build` users can create an automated build that executes several command-line instructions in succession.

Let's create a `Dockerfile` in the root of our project:

```bash
touch Dockerfile
```

The first line of the `Dockerfile` is the `FROM` command. This specifies the base image that we will use to build our image. We will use the official Python image as the base image:

```dockerfile
# Use the official Python image as the base image
FROM python:3.10
```

Next, we need to set the working directory. This is the directory where the commands specified in the `Dockerfile` will be executed. We will set the working directory to `/app`.

```dockerfile
# Set the working directory
WORKDIR /app
```

Next, we need to copy the `requirements.txt` file to the working directory. This will ensure that the dependencies are installed when we build the image. We can then use the `RUN` command to install the dependencies:


```dockerfile
# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

Next, we need to copy the pipeline directory to the working directory. This will ensure that the pipeline is available when we build the image:

```dockerfile
# Copy the rest of the application code
COPY . .
```

Finally, we need to specify the command that will be executed when the container is run. In this case, we will run the `datadownload.py` script:

```dockerfile
# Expose the port that the app runs on
EXPOSE 8000

# Execute pipeline
CMD ["python", "./src/datadownload.py"]
```

The final `Dockerfile` should look like this:

```dockerfile
# Use the official Python image as the base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Execute pipeline
CMD ["python", "./src/datadownload.py"]
```

## Building the Docker image

The Docker image can be built using the following command:

```bash
docker build -t etlp:latest -f Dockerfile .
```

The `-t` flag is used to tag the image. The `-f` flag is used to specify the `Dockerfile` to use. The `.` at the end of the command specifies the build context. This is the path to the directory containing the `Dockerfile`. In this case, the `Dockerfile` is in the root of the project, so we use `.`.

## Running the Docker image

To run the Docker image, use the following command:

```bash
docker run -it --rm -p 8000:8000 etlp
```

The `-it` flag is used to run the container in interactive mode. The `--rm` flag is used to remove the container after it exits. The `-p` flag is used to map the port `8000` from the container to the port `8000` on the host machine. The `etlp` argument is the name of the image to run.

## Summary

In this section, we learned how to package our pipeline into a Docker container. We learned how to create a `Dockerfile` to build a Docker image, and how to run the Docker image. In the next section, we will learn how to incorporate exploratory data analysis (EDA) into our pipeline.