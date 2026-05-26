#!/usr/bin/env bash
set -e

# ── Python / Django setup ────────────────────────────────────────────────────

uv init --no-readme
uv add django
uv run django-admin startproject wings .
uv run python manage.py migrate

# Create superuser (admin/admin) — dev only
DJANGO_SUPERUSER_PASSWORD=admin \
  uv run python manage.py createsuperuser \
    --username admin \
    --email admin@example.com \
    --noinput

# ── Azure service principal ──────────────────────────────────────────────────

SUBSCRIPTION_ID=$(az account show --query id -o tsv)

az ad sp create-for-rbac \
  --name wings-github-actions-sp \
  --role Contributor \
  --scopes /subscriptions/"$SUBSCRIPTION_ID"
