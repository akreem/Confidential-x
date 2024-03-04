FROM python:3.9-slim

# copy the requirements file into the image
COPY requirements.txt /flaskexcel/

# setting up the working directory
WORKDIR /flaskexcel

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["app.py"]