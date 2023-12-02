FROM python:3.11

# Copy all files 
COPY . .

# install dependencies
RUN pip install -r requirements.txt

# this configuration is needed for your app to work, do not change it
ENTRYPOINT ["voila", "app.ipynb"]