"""Development settings"""

import os
from server.settings import *

DEBUG = True

DATABASES = {

    # PostgreSQL Database

    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DEV_DB_NAME"),
        "USER": os.getenv("DEV_DB_USER"),
        "PASSWORD": os.getenv("DEV_DB_PASSWORD"),
        "HOST": os.getenv("DEV_DB_HOST"),
        "PORT": os.getenv("DEV_DB_PORT"),
    },

}