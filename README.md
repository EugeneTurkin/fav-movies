# fav-movies

CRUD application for managing favorite movies with Unofficial Kinopoisk API (https://kinopoiskapiunofficial.tech/).


## System requirements

[Poetry](https://python-poetry.org/docs/#installation)


## First time setup

Commands below will help you to set up this project for development.

Go to the project root directory.

1. Create virtual environment and install dependencies.
```bash
poetry install --with app,lint,test
```

2. Activate virual environment.
```bash
poetry shell
```


## Run app for local development

1. Generate .env file from example

   _(it should work out of the box but you can adjust it)_
```bash
cp envs/dev/example.env envs/dev/.env
```

2. Start database for local development.
```bash
docker compose -f envs/dev/docker-compose.yml up -d
```

3. Apply migrations.
```bash
# to pass environment variable in Windows PowerShell run:
# $env:FAV_MOVIES_ENV = 'dev';
FAV_MOVIES_ENV=dev alembic upgrade head
```

4. Run uvicorn.
```bash
# to pass environment variable in Windows PowerShell run:
# $env:FAV_MOVIES_ENV = 'dev';
FAV_MOVIES_ENV=dev uvicorn src.app:app --reload

# link for swagger docs
http://localhost:8000/docs

# link for redoc docs
http://localhost:8000/redoc
```



## Run linters

To run linters you need to do all steps from [First time setup](#first-time-setup) section.

Linters order below is a preferred way to run and fix them one by one.

1. Mypy.
```bash
mypy src
```

2. Ruff.
```bash
ruff check src
```


## Run containerized app

1. Generate .env file from example

   _(it should work out of the box but you can adjust it)_
```bash
cp envs/deploy/example.env envs/deploy/.env
```

2. Start dockerized app and database.
```bash
docker compose -f envs/deploy/docker-compose.yml up -d

# link for swagger docs
http://localhost:8000/docs

# link for redoc docs
http://localhost:8000/redoc
```
