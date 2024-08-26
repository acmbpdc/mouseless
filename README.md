# Mouseless

This is a web server that can host quizzes.

## Installation

*   Clone this repository 
    ```bash
    git clone https://github.com/acmbpdc/mouseless.git
    ``` 
## Configuration
*   Install dependencies

    ### Fix Conf URL Path
    First, make and activate a virtual env
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
    Now that the virtual environment is activated, install the required libraries. Note: every time you start the project, you will have to activate the venv.
    ```bash
    pip install -r requirements.txt
    ```
    In the virtual env: ```\venv\lib\site-packages\markdownx\urls.py```

Replace:
    ```
    from django.conf.urls import url
    ```
    With:
    ```
    from django.urls import re_path as url
    ```
* Perform migrations
    ```bash
        python manage.py makemigrations
        python manage.py migrate
    ```
* Create a super user

    ```bash
    python manage.py createsuperuser
    ```

    ### Adding environment variables for OAuth
* Create a new file ```.env``` and add in the secrets needed

    ```bash
    CLIENT_ID = XXX.apps.googleusercontent.com
    CLIENT_SECRET=XXX-YYY-ZZZ
    SECRET_KEY = XXX
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
