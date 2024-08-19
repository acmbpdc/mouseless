# Mouseless

A web server to host quizzes.

## Installation

*   Clone this repository

    ```bash
    git clone https://pypi.org/project/vocabulum/
    ```
*   Install dependencies

```bash
pip install -r requirements.txt
```

### Fix Conf URL Path
In the virtual env: \venv\lib\site-packages\markdownx\urls.py

Replace:

```bash
from django.conf.urls import url
```

With:

```bash
from django.urls import re_path as url
```

## Configuration

*   Make migrations

    ```bash
    python manage.py makemigrations
    ```
* Perform migration

    ```bash
    python manage.py migrate
    ```
* Create a super user

    ```bash
    python manage.py createsuperuser
    ```

## Usage

Start server

```bash
python manage.py runserver 0.0.0.0:8000
```

## Features

*   A single `User` can be associated with 1-2 `Player`s
*   A timer for the entire `Quiz`
*   A `User` is timed only if the complete a `Task`.

    Their time metric is the duration since the start of the challenge till their last successful `Task` completion.
*   A leaderboard showcasing the `User`s with the most points.

    Ties are settled based on the time taken to complete `Task`s
