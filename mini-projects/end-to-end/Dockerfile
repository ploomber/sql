FROM python:3.11

# Copy all files 
COPY app.ipynb app.ipynb
COPY .env .env

# install dependencies
RUN pip install voila==0.5.1 pandas==2.0.3 plotly python-dotenv requests duckdb==v0.9.2

# this configuration is needed for your app to work, do not change it
ENTRYPOINT ["voila", "app.ipynb","--port 5000:80"]