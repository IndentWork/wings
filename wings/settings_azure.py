"""
Overlay for any Azure deployment target (App Service today, AKS tomorrow).

Loaded by settings.py when WINGS_SETTINGS=azure.

Only reads from os.environ. No Azure SDK imports, no API calls.
The platform (Terraform on App Service) is responsible for setting these env vars.
"""

import os

DEBUG = False

SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ["DB_HOST"],
        "NAME": os.environ.get("DB_NAME", "wings"),
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "PORT": "5432",
        "CONN_MAX_AGE": 600,
        "OPTIONS": {"sslmode": "require"},
    }
}
