# pull official base image
FROM python:3.8

WORKDIR /app

RUN apt-get update
RUN apt-get install -y postgresql-client

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD poetry.lock pyproject.toml ./

# System deps:
RUN pip install poetry

# install dependencies
RUN poetry config virtualenvs.create false
RUN poetry install

# copy project
COPY . .
