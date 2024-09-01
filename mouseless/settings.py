import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
# print("CLIENT_ID: ", client_id )
# print("CLIENT_SECRET: ", client_secret)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# with open(os.path.join(BASE_DIR, 'secret.key')) as f:
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
 
SITE_ID = 1

ALLOWED_HOSTS = [
    '*',
    'anurag.pythonanywhere.com',
    'localhost',
    '172.16.100.14',
    '172.16.100.15',
    '127.0.0.1'
]


# Application definition

INSTALLED_APPS = [
    'quiz.apps.QuizConfig',
    'player.apps.PlayerConfig',
    'crispy_forms',
    'phonenumber_field',
    'markdownx',
    'adminsortable2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mathfilters',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
]

SOCIALACCOUNT_LOGIN_ON_GET=True

AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',  # Allauth backend
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware", 
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'mouseless.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id':client_id,
            'secret': client_secret,
          
        },
        'SCOPE': ['profile','email',],
         'AUTH_PARAMS': {'access_type': 'online'},
        'METHOD': 'oauth2',
        'VERIFIED_EMAIL': True,
    },
    # 'github': {
    #     'APP': {
    #         'client_id': '',
    #         'secret': '',
           
    #     }
    # }
   
}

# SOCIALACCOUNT_LOGIN_ON_GET=True

WSGI_APPLICATION = 'mouseless.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# Use below for prod
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DATABASE'),
        'USER': os.getenv('MYSQL_USERNAME'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD'),
        'HOST': os.getenv('MYSQL_HOST')
    }
}
"""


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

CRISPY_TEMPLATE_PACK = 'bootstrap4'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home' 
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
# STATIC_ROOT = os.path.join(BASE_DIR, "static")

# In production mode
# When using command collectstatic.py , comment out STATICFILES_DIRS... It looks like:

# #STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
# STATIC_ROOT=os.path.join(BASE_DIR,"/static/")
# And after that comment out STATIC_ROOT, so that it looks like:

# STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
# #STATIC_ROOT=os.path.join(BASE_DIR,"/static/")
# On server uncommenting both was working best

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
