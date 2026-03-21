from .base import *
from decouple import config

DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1", "localhost", ".onrender.com"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST"),
        "PORT": config("POSTGRES_DB_PORT", cast=int),
    }
}