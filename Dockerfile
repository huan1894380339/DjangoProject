# pull official base image
FROM python:3.9-slim-buster

WORKDIR /app

RUN apt-get update
RUN apt-get install -y postgresql-client

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD poetry.lock pyproject.toml ./

# System deps:
RUN pip install poetry==1.1.13

# install dependencies
RUN poetry config virtualenvs.create false
RUN poetry install

# copy project
COPY . .
