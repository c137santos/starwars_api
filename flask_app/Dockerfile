# pull official base image
FROM python:3.11.3-slim

WORKDIR /app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install build-essential -y
RUN mkdir -p /setup
COPY ./requirements.txt /setup
COPY ./wsgi.ini /setup
RUN pip install -r /setup/requirements.txt
EXPOSE 5000
