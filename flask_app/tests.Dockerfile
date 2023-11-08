# pull official base image
FROM python:3.11.3-slim

WORKDIR /app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install build-essential -y
COPY ./requirements.txt /app
COPY ./requirements.tests.txt /app
RUN pip install -r /app/requirements.tests.txt
