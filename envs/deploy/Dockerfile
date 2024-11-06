FROM python:3.11.4-slim

WORKDIR /app

RUN pip install poetry==1.5.1

RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./

RUN poetry install --with=app

COPY . ./
