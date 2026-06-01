"""
Overlay for any Azure deployment target (App Service today, AKS tomorrow).

Loaded by settings.py when WINGS_SETTINGS=azure.

Only reads from os.environ. No Azure SDK imports, no API calls.
The platform (Terraform on App Service) is responsible for setting these env vars.
"""

import os

import dj_database_url

DEBUG = False

SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")

DATABASES = {
    "default": dj_database_url.config(
        env="DATABASE_URL",
        conn_max_age=600,
        ssl_require=True,
    )
}
