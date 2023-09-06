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

# Expose the port that the app runs on
EXPOSE 8000

# pipeline 
RUN poetry run ploomber build