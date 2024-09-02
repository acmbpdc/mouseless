# Mouseless

This is a web server that can host quizzes.

## Installation

*   Clone this repository 
    ```bash
    git clone https://github.com/acmbpdc/mouseless.git
    ``` 
## Configuration
*   Install dependencies

    ### Environment Setup
    First, make and activate a virtual env
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
    Now that the virtual environment is activated, install the required libraries. Note: every time you start the project, you will have to activate the venv.
    ```bash
    pip install -r requirements.txt
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
* Create a new file ```.env``` and add in the secrets needed (For Development)

    ```bash
    CLIENT_ID=XXX.apps.googleusercontent.com
    CLIENT_SECRET=XXX-YYY-ZZZ
    SECRET_KEY=XXX
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

## Configuration for Production

### Adding environment variables for MYSQL

* Update the new file ```.env``` and add in the secrets needed for using MySQL

```bash
CLIENT_ID=XXX.apps.googleusercontent.com
CLIENT_SECRET=XXX-YYY-ZZZ
SECRET_KEY=XXX
MYSQL_HOST=XXX
MYSQL_USERNAME=XXX
MYSQL_DATABASE=‘XXX’
MYSQL_PASSWORD=XXX
```

### Change backend to MySQL

In [settings.py](mouseless/settings.py), update the backend from SQLite3 to MySQL.

Change this:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
To this:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DATABASE'),
        'USER': os.getenv('MYSQL_USERNAME'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD'),
        'HOST': os.getenv('MYSQL_HOST')
    }
}
```

### Updating the static path

In [settings.py](mouseless/settings.py), comment out the `STATIC_DIR` variable and add `STATIC_ROOT` as below:
```bash
# STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATIC_ROOT = os.path.join(BASE_DIR, "static")
```
Then in the bash console, run the command:
```
python manage.py collectstatic
```
This will now put all static files into one static folder

Now, add this static folder path into PythonAnywhere's Web section:

| URL   | Directory |
| -------- | ------- |
| /static/  | /home/{{USERNAME}}/{{PATH_TO_STATIC_FOLDER}} |

If you're adding the reorder functionality to an already existing db, run the command:
```bash
python manage.py reorder quiz.Task
```
This will now set the order attr of each record

Then you can migrate the changes:
```bash
python manage.py makemigrations
python manage.py migrate
```