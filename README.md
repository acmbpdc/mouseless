# Mouseless

This is a web server that can host quizzes.

## Features

*   A timer for the entire `Quiz`
*   A `User` is timed only if they complete a `Task`.

    Their **time metric** is the duration since the start of the challenge till their last successful `Task` completion.
*   A leaderboard showcasing the `User`s with the most points.

    Ties for points are settled based on the time taken to complete `Task`s

## Installation
Clone the repository:
```bash
git clone https://github.com/acmbpdc/mouseless.git
``` 
## Development Configuration
### Environment Setup
Create virtual environent and install dependencies.

First, make and activate a virtual env
```bash
python -m venv venv
.\venv\Scripts\activate
```
Now that the virtual environment is activated, install the required libraries. 

**Note:** Every time you start the project, you will have to activate the venv.
```bash
pip install -r requirements.txt
```

Perform migrations
```bash
    python manage.py makemigrations
    python manage.py migrate
```
Create a super user

```bash
python manage.py createsuperuser
```

### Adding environment variables for OAuth
Create a new file ```.env``` and add in the secrets needed **(For Development)**

```bash
CLIENT_ID=XXX.apps.googleusercontent.com
CLIENT_SECRET=XXX-YYY-ZZZ
SECRET_KEY=XXX
```
1. CLIENT_ID and CLIENT_SECRET: [Set up your Google OAuth 2.0 client](https://support.google.com/cloud/answer/6158849?hl=en)

2. SECRET_KEY: The django app secret key for cryptographically signing session cookies

## Usage

Start server

```bash
python manage.py runserver 127.0.0.1:8000
```

## Configuration for Production

### Setup virtual environment on PythonAnywhere (Optional)

* Change setuptools version <= 70.x (Done to support the virtualenvwrapper tool)

    ```bash
    pip install setuptools==70.3.1
    ```
* Then create the virtual environment:
    ```bash
    mkvirtualenv {{VIRTUAL_ENV_NAME}} --python=/usr/bin/python3.9
    ```

* Now that the virtual environment is activated, install the required libraries.
    ```bash
    pip install -r requirements.txt
    ```

* Add virtualenv path: Navigate to the Web tab and scroll, then add the path:
`/home/{{USERNAME}}/.virtualenvs/{{VIRTUAL_ENV_NAME}}`

The app is now configured to use the virtual environment.

### Add the environment variables

* Create a `.env` file in the same folder as [settings.py](mouseless/settings.py)

* Update the new file ```.env``` and add in the following secrets:

    ```bash
    CLIENT_ID=XXX.apps.googleusercontent.com
    CLIENT_SECRET=XXX-YYY-ZZZ
    SECRET_KEY=XXX
    MYSQL_HOST=XXX
    MYSQL_USERNAME=XXX
    MYSQL_DATABASE=‘XXX’
    MYSQL_PASSWORD=XXX
    ```

1. **CLIENT_ID** and **CLIENT_SECRET**: [Set up your Google OAuth 2.0 client](https://support.google.com/cloud/answer/6158849?hl=en)

2. **SECRET_KEY**: Django app secret key for cryptographically signing session cookies

3. **MYSQL_USERNAME**: The username you set from the 'Databases' tab in pythonanywhere

4. **MYSQL_PASSWORD**: The password you set from the 'Databases' tab

5. **MYSQL_HOST**: The database host address you set from the 'Databases' tab

6. **MYSQL_DATABASENAME**: The name of the database you set

(**Note:** If your secret in the `.env` contains special characters, enclose it in quotes)

Now, pass in absolute path to load_dotenv: in [settings.py](mouseless/settings.py) 

Change:
```python
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
```
To:
```python
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
```

### Change backend to MySQL

First off install the `mysqlclient` package for accessing MySQL db

```bash
pip install mysqlclient==2.2.4
```

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

Perform migrations
```bash
    python manage.py makemigrations
    python manage.py migrate
```
Create a super user
```bash
python manage.py createsuperuser
```

### Updating the static path

In [settings.py](mouseless/settings.py), comment out the `STATIC_DIR` variable and add `STATIC_ROOT` as below:
```python
# STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATIC_ROOT = os.path.join(BASE_DIR, "static")
```
Then in the bash console, run the command:
```bash
python manage.py collectstatic
```
This will now put all static files into one static folder.

Now, add this static folder path into PythonAnywhere's Web section:

| URL   | Directory |
| -------- | ------- |
| /static/  | /home/{{USERNAME}}/{{PATH_TO_STATIC_FOLDER}} |

If you're adding the **reorder** functionality to an already existing db, run the commands:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py reorder quiz.Task
```
This will now set the `order` attribute of each Task auto-incrementally.

And now we are ready for production 🚀
