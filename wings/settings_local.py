import dj_database_url

DEBUG = True
SECRET_KEY = "local-dev-insecure-do-not-use-in-production"
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": dj_database_url.config(
        env="DATABASE_URL",
        conn_max_age=600,
    )
}
