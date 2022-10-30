"""Production settings"""

import os
from server.settings import *

DEBUG = False

DATABASES = {

    # AWS PostgreSQL Database

    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("PROD_DB_NAME"),
        "USER": os.getenv("PROD_DB_USER"),
        "PASSWORD": os.getenv("PROD_DB_PASSWORD"),
        "HOST": os.getenv("PROD_DB_HOST"),
        "PORT": os.getenv("PROD_DB_PORT"),
    }
}