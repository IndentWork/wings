"""
Overlay for any Azure deployment target (App Service today, AKS tomorrow).

Loaded by settings.py when WINGS_SETTINGS=azure.

Only reads from os.environ. No Azure SDK imports, no API calls.
The platform (Terraform on App Service) is responsible for setting these env vars.

Env-var names follow the Microsoft Azure Django reference template
(Azure-Samples/azure-django-postgres-flexible-appservice) — POSTGRES_*
prefix matches the convention used by Azure Service Connector and
Microsoft Learn tutorials, making the stack recognisable to anyone who
has shipped Django on App Service before.
"""

import os

DEBUG = False

SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ["POSTGRES_HOST"],
        "NAME": os.environ.get("POSTGRES_DATABASE", "wings"),
        "USER": os.environ["POSTGRES_USERNAME"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        "CONN_MAX_AGE": 600,
        "OPTIONS": {"sslmode": os.environ.get("POSTGRES_SSL", "require")},
    }
}
