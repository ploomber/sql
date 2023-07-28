# Use the official Python image as the base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port that the app runs on
EXPOSE 8000

# Install ploomber
RUN pip install ploomber

# Remove files ending in .metadata from the notebooks folder
RUN find notebooks -type f -name "*.metadata" -exec rm -f {} \;

RUN ploomber build