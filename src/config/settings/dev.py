import os

from config.settings.base import *  # NOQA

CURRENT_ENV = "DEV"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

# INSTALLED_APPS += ...

if os.environ.get("GITHUB_WORKFLOW"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "github_actions",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "127.0.0.1",
            "PORT": 5432,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        },
        # "default_postgres_docker": {
        #     "ENGINE": 'django.db.backends.postgresql',
        #     "NAME": os.environ.get('POSTGRES_DB'),
        #     "USER": os.environ.get('POSTGRES_USER'),
        #     "PASSWORD": os.environ.get('POSTGRES_PASSWORD'),
        #     "HOST": os.environ.get('POSTGRES_HOST'),
        #     "PORT": os.environ.get('POSTGRES_PORT'),
        # },
        # "default_postgres_local": {
        #     "ENGINE": 'django.db.backends.postgresql',
        #     "NAME": 'zhydyk',
        #     "USER": 'postgres',
        #     "PASSWORD": 'admin',
        #     "HOST": 'localhost',
        #     "PORT": 5432,
        # },
    }

STATIC_URL = "/static/"
STATIC_ROOT = ""
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = 'media/'


LOCATION_FIELD = {
    "provider.google.api": "//maps.google.com/maps/api/js?sensor=false",
    "provider.google.api_key": "AIzaSyBCc9LvVmOWLRGWu5Ct8pt4i4om0R3sBmE",
    "provider.google.api_libraries": "",
}

GOOGLE_MAPS_API_KEY = "AIzaSyBCc9LvVmOWLRGWu5Ct8pt4i4om0R3sBmE"
