FROM python:3.11

# Copy all files 
COPY app.ipynb app.ipynb
COPY weather.csv weather.csv

# install dependencies
RUN pip install voila==0.5.1 pandas==2.0.3 plotly python-dotenv requests

# this configuration is needed for your app to work, do not change it
RUN ["voila", "app.ipynb"]