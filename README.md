# Blog Post API

High-level API wrapper around the existing blog post API at *https://api.hatchways.io/assessment/blog/posts* with improvements and new features as follow:

- Async API built with [FastAPI](https://fastapi.tiangolo.com)
- Now can take multiple tags as comma separated query parameter _(`"history,tech"`)_
- Sort results by _id_, _likes_, _reads_, _popularity_
- New Caching system for faster and efficient responses

## Installation

The installation is pretty straightforward

1. Unzip the repo with unzip _(anything can be used unzip)_ and change the directory to it

   ```bash
   $ unzip test_assessment.zip
   $ cd test_assessment
   ```

2. Create a python3.8 environment with virtualenv python package and activate the virtual environment

   ```bash
   $ pip3 install virtualenv
   $ python -m venv env
   $ source env/bin/activate
   ```

3. Install required packages from requirements/main.txt

   ```bash
   $ pip3 install -r requirements/main.txt
   ```

4. Change environment variable `.env.example` file to `.env` file and set required and optional variables

   ```bash
   $ mv .env.example .env
   $ nano .env

   BLOG_POST_ROUTE = "https://api.hatchways.io/assessment/blog/posts"

   # API CACHING VARIABLES
   CACHING = true
   CACHE_EXPIRY = 10 # in minutes
   ```

## Start API

FastAPI uses uvicorn ASGI server which is lightning fast. Run the API server with

```bash
$ uvicorn api.server:app --host 0.0.0.0 --port 8000

INFO:     Started server process [1494]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

If you want to run the server in debug mode then add `--reload` parameter

```bash
$ uvicorn api.server:app --host 0.0.0.0 --port 8000 --reload

INFO:     Will watch for changes in these directories: ['/Users/saad/Desktop/assessment2']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [1523] using watchgod
INFO:     Started server process [1525]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Routes

These are two routes in the api

**_GET_** `/api/ping`

**_GET_** `/api/posts?tags=history,tech&sortBy=likes&direction=desc`

## Testing

Run tests with pytest with following steps

1. Activate the virtual environment and install dev requirements

   ```bash
   $ source env/bin/activate
   $ pip3 install -r requirements/dev.txt
   ```

2. Run tests with

   ```bash
   $ pytest tests

   collected 17 items

   tests/test_database.py ...                                                                   [ 17%]
   tests/test_models.py ....                                                                    [ 41%]
   tests/test_server.py .......                                                                 [ 82%]
   tests/test_utils.py ...                                                                      [100%]
   ```

3. Test coverage with

   ```bash
   $ pytest --cov=api tests/

   collected 17 items

   tests/test_database.py ...                                                                   [ 17%]
   tests/test_models.py ....                                                                    [ 41%]
   tests/test_server.py .......                                                                 [ 82%]
   tests/test_utils.py ...                                                                      [100%]

   ---------- coverage: platform darwin, python 3.8.3-final-0 -----------
   Name              Stmts   Miss  Cover
   -------------------------------------
   api/__init__.py       2      0   100%
   api/database.py      29      1    97%
   api/models.py        19      0   100%
   api/routes.py        17      0   100%
   api/server.py         4      0   100%
   api/utils.py         27      0   100%
   -------------------------------------
   TOTAL                98      1    99%

   ```
